# 5. Ablation Study & Experimental Evaluation

This chapter details the experimental design, testing environments, standardized scenarios, and quantitative metrics formulated to rigorously validate the system (**Module 3**). In direct fulfillment of the project specification (`SD-MEng-26-01`), the evaluation centers on a systematic three-way comparative ablation study that isolates the contribution of visual object detection from motion prediction.

---

## 5.1 Three-Way Comparative Ablation Matrix

To isolate the specific mechanisms that resolve the "freezing robot" problem, three distinct system configurations are benchmarked under identical conditions:

| Configuration ID | System Name | Sensor Modalities | Tracking & State Estimation | Local Controller Formulation |
|---|---|---|---|---|
| **C0** | **Baseline Nav2 (LiDAR-Only)** | 2D Planar LiDAR only | None (Raw scan points fed directly into local costmap) | Default `nav2_mppi_controller` querying static 2D costmap via `ObstaclesCritic` / `CostCritic` |
| **C1** | **Vision-Augmented Detection (No Prediction)** | 2D Planar LiDAR + Monocular RGB Camera | ByteTrack + LiDAR frustum gating; Instantaneous position $(x_m, y_m)$, but velocity zeroed ($\mathbf{v}_{\text{obs}} = \mathbf{0}$) | MPPI evaluates dynamic obstacles as static spatial clearance circles ($t=0$ position) with no forward temporal projection |
| **C2** | **Full Predictive MPPI (Proposed)** | 2D Planar LiDAR + Monocular RGB Camera | ByteTrack + LiDAR frustum gating + Linear Kalman Filter ($[x, y, v_x, v_y]^T$) | Custom `DynamicObstaclesCriticPlugin` forward-propagating obstacle states over lookahead horizon $\tau \in [0, 2.0]\text{ s}$ |

### 5.1.1 Scientific Rationale of the C0 vs. C1 vs. C2 Ablation
- **C0 $\to$ C1 Comparison:** Isolates the effect of **visual bounding and semantic segmentation**. Demonstrates whether having persistent bounding frustums and eliminating point-cloud noise alone prevents false stops, or whether static costmap representations still cause controller freezes.
- **C1 $\to$ C2 Comparison:** Isolates the effect of **temporal motion prediction**. Directly quantifies the performance gains (reduced freezing, proactive yielding, smoother evasion) attributable strictly to the predictive critic evaluating $\mathbf{p}_{\text{obs}}(\tau) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}} \tau$ rather than static spatial buffers.

### 5.1.2 Methodological Positioning vs. External Advanced MPPI Benchmarks
While recent literature features specialized MPPI variations—such as Control Barrier Function safety filtering (SE-MPPI [L15]), GPU-accelerated non-convex Signed Distance Functions (EXACT-MPPI [L16]), and DBSCAN trajectory clustering (CSC-MPPI [L17])—these frameworks serve as **conceptual and qualitative benchmarks** rather than direct software-drop-in ablation baselines. Substituting the Nav2 controller with external Python/JAX or RAPIDS GPU pipelines would introduce confounding variables (dramatically altering runtime environments, memory overhead, and sensor assumptions). The C0–C2 matrix ensures strict scientific control: all three configurations run inside the identical Nav2 C++ runtime on standard brownfield CPU compute, isolating the precise performance impact of multi-modal tracking and spatio-temporal predictive rollouts.

---

## 5.2 Simulation Testbed & Benchmark Environments

Validation is executed within **Gazebo Harmonic** coupled to ROS 2 Jazzy Jalisco on an AMD/Intel workstation equipped with an NVIDIA RTX 4070 Ti Super GPU.

### 5.2.1 Robot Model & Sensor Configuration
- **Base:** Differential-drive mobile robot (TurtleBot 4 / custom industrial AMR urdf), footprint radius $R_{\text{robot}} = 0.22\text{ m}$, maximum linear velocity $v_{\max} = 1.0\text{ m/s}$, maximum angular velocity $\omega_{\max} = 1.5\text{ rad/s}$.
- **Sensors:**
  - Planar 2D LiDAR: 360° horizontal FoV, 20 Hz scan rate, 12 m range, angular resolution 0.5°, range noise $\sigma = 0.02\text{ m}$.
  - Monocular RGB Camera: Forward-facing, $80^\circ$ horizontal FoV, 1080p resolution rendered at 30 FPS.
  - Ground-Truth Ground Plane Extrinsics rigidly broadcast via `/tf`.

### 5.2.2 Dynamic Actor Simulation
Dynamic obstacles (pedestrians and industrial carts) are simulated using Gazebo actor plugins with kinematic trajectory control. Ground-truth positions, orientations, and linear velocities are continuously broadcast on a private benchmark topic (`/ground_truth/actors`) for automated metric scoring.

---

## 5.3 Standardized Benchmark Scenarios

Five deterministic scenarios simulate the primary failure modes of warehouse navigation:

```
[SCENARIO A: Perpendicular Corridor Crossing]
        Aisle Wall
  ───────────────────────────────
      Robot (v = 0.8 m/s) ──►        ▲ Pedestrian (v_obs = 1.2 m/s)
                                     │
  ───────────────────────────────
        Aisle Wall

[SCENARIO B: Oncoming Head-On Encounter]
  ───────────────────────────────
      Robot ──►             ◄── Pedestrian
  ───────────────────────────────

[SCENARIO C: Oblique Cross-Traffic]
      Robot ──►
                     ▲
                    ╱ Cart (v_obs = 1.8 m/s)
                   ╱
```

### 1. Scenario A: Perpendicular Corridor Crossing
- **Layout:** $2.4\text{ m}$ wide narrow aisle bounded by warehouse racking.
- **Agent Behavior:** Single pedestrian enters from a blind cross-aisle $3.0\text{ m}$ ahead of the approaching robot, traversing perpendicularly at $1.2\text{ m/s}$.
- **Target Phenomenon:** Freezing robot failure. In C0 and C1, the static costmap paints the entire aisle blocked, causing emergency deceleration. In C2, the robot predicts clearance time and performs a subtle speed yield or continuous traversal.

### 2. Scenario B: Oncoming Head-On Encounter
- **Layout:** $3.0\text{ m}$ wide shared transit hallway.
- **Agent Behavior:** Pedestrian walks directly toward the robot along the same centerline at $1.2\text{ m/s}$.
- **Target Phenomenon:** Deadlock vs. lateral deflection. In C0, both agents approach until the safety inflation zone triggers an emergency halt. In C2, the controller detects oncoming velocity and initiates an early lateral deflection maneuver to the right side of the aisle.

### 3. Scenario C: Oblique Cross-Traffic (High Speed)
- **Layout:** Open loading bay intersection ($15\text{ m} \times 15\text{ m}$).
- **Agent Behavior:** Motorized tugger cart crossing diagonally at $1.8\text{--}2.0\text{ m/s}$ intersecting the robot's planned path.
- **Target Phenomenon:** High-speed collision risk. Tests the predictive lookahead horizon ($\tau = 2.0\text{ s}$) in detecting converging trajectories and executing evasive deceleration.

### 4. Scenario D: Multi-Agent Bottleneck (Crowd Density)
- **Layout:** Choke point / $2.0\text{ m}$ doorway between zones.
- **Agent Behavior:** 2–4 pedestrians moving with staggered start times and varying speeds ($0.8\text{--}1.4\text{ m/s}$), creating mutual visual occlusions.
- **Target Phenomenon:** ByteTrack occlusion recovery, multi-track metric Kalman filter stability, and multi-obstacle rollout cost evaluation.

### 5. Scenario E: Static Baseline & Regression Control
- **Layout:** Standard industrial layout with structural pillars, pallets, and walls, with zero dynamic agents.
- **Target Phenomenon:** Algorithmic overhead and path optimality verification. Ensures that adding the perception and critic plugins introduces no regressions in compute latency, path length, or standard clearance.

---

## 5.4 Quantitative Evaluation Metrics

All metrics are recorded automatically across $N \ge 30$ randomized runs per configuration per scenario using fixed paired seeds.

### 5.4.1 Primary Navigation Performance Metrics

1. **Freezing Episode Count ($N_{\text{freeze}}$):**
   A freeze is formally defined as an event where robot linear velocity drops below $v_{\text{threshold}} = 0.05\text{ m/s}$ for a continuous duration $\Delta t_{\text{freeze}} \ge 1.5\text{ s}$ while the goal remains unreached and the obstacle is moving:
   $$N_{\text{freeze}} = \sum \mathbf{1}_{\{v(t) < 0.05 \text{ for } \Delta t \ge 1.5\text{ s}\}}$$
   - *Target:* **0 freezes** in C2 across nominal crossing scenarios.

2. **Minimum Time-to-Collision ($\text{TTC}_{\min}$):**
   Evaluates safety margin under dynamic approach:
   $$\text{TTC}(t) = \frac{\|\mathbf{p}_{\text{robot}}(t) - \mathbf{p}_{\text{obs}}(t)\| - (R_{\text{robot}} + R_{\text{obs}})}{\|\mathbf{v}_{\text{rel}}(t)\|}, \quad \text{for } \mathbf{v}_{\text{rel}} \cdot (\mathbf{p}_{\text{obs}} - \mathbf{p}_{\text{robot}}) < 0$$
   $$\text{TTC}_{\min} = \min_{t} \text{TTC}(t)$$
   - *Target:* Maintain $\text{TTC}_{\min} \ge 1.2\text{ s}$ at all times without emergency halts.

3. **Minimum Clearance Distance ($d_{\min}$):**
   $$d_{\min} = \min_{t} \left( \|\mathbf{p}_{\text{robot}}(t) - \mathbf{p}_{\text{obs}}(t)\| - R_{\text{robot}} - R_{\text{obs}} \right)$$
   - *Target:* $d_{\min} \ge 0.35\text{ m}$ (zero physical collisions).

4. **Mission Efficiency / Completion Time ($T_{\text{mission}}$):**
   Total time elapsed from navigation goal dispatch to reaching goal tolerance ($e_{\text{dist}} < 0.1\text{ m}$, $e_{\text{yaw}} < 0.1\text{ rad}$).
   - *Target:* **15–25% reduction** in total mission time in C2 compared to C0 due to eliminating stop-and-go recovery cycles.

5. **Kinematic Smoothness (Normalized Path Jerk):**
   Quantifies passenger/cargo transport stability and mechanical wear:
   $$J_{\text{norm}} = \frac{1}{T_{\text{mission}}} \int_0^{T_{\text{mission}}} \left( \left(\frac{d a_{\text{linear}}}{dt}\right)^2 + \left(\frac{d \alpha_{\text{angular}}}{dt}\right)^2 \right) dt$$

### 5.4.2 State Estimation & Tracking Accuracy Metrics

1. **Velocity Vector Root Mean Square Error ($\text{RMSE}_v$):**
   Compared against Gazebo simulator ground truth:
   $$\text{RMSE}_v = \sqrt{\frac{1}{K} \sum_{k=1}^K \|\hat{\mathbf{v}}_{\text{obs}}(t_k) - \mathbf{v}_{\text{true}}(t_k)\|^2}$$
   - *Target:* $\text{RMSE}_v < 0.15\text{ m/s}$ under steady-state tracking.

2. **Tracking Robustness Metrics:**
   - **ID Switches (IDSW):** Number of times a persistent agent changes `track_id`.
   - **Track Fragmentation (Frag):** Frequency of track interruptions due to occlusion.

### 5.4.3 Computational Performance Metrics
- **Perception Pipeline Frame Rate:** Sustained FPS of detection, ByteTrack, and gating nodes on target edge compute. Target: $\ge 30\text{ FPS}$.
- **MPPI Critic Evaluation Latency:** Mean and 99th percentile computation time per control cycle. Target: $<0.5\text{ ms}$ for $M = 2000$ trajectories.

---

## 5.5 Statistical Protocol & Testing Matrix

To guarantee statistical rigor:
1. **Paired Seed Design:** For every scenario, 30 randomized parameter sets (pedestrian arrival time offsets $\delta t \in [0, 3.0]\text{ s}$, crossing speeds $v \in [0.5, 2.0]\text{ m/s}$, crossing angles $\theta \in [60^\circ, 120^\circ]$) are pre-generated.
2. **Paired Testing:** Configurations C0, C1, and C2 are run sequentially against each identical seed, ensuring observed differences reflect algorithmic variations rather than random traffic variation.
3. **Statistical Reporting:** Results are reported as mean $\pm$ standard error and 95% confidence intervals. Pairwise hypothesis testing is conducted using two-tailed paired Student's t-tests (or Wilcoxon signed-rank tests for non-normal distributions) at significance level $\alpha = 0.05$.

