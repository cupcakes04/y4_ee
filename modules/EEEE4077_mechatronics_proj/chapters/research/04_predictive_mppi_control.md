# 4. Predictive MPPI Control & Dynamic Obstacle Critic

This chapter details the theoretical foundations, plugin architecture, and implementation of the predictive trajectory planning subsystem (**Module 2**). The subsystem integrates dynamic obstacle motion estimates into Nav2's Model Predictive Path Integral (MPPI) controller via a custom C++ `pluginlib` critic, enabling proactive yielding and evasive swerving while eliminating the freezing robot failure mode.

---

## 4.1 Theoretical Background: Nav2 MPPI Controller

Model Predictive Path Integral (MPPI) control (Williams et al., 2017) is an algorithm based on stochastic optimal control that handles complex, non-linear robot kinematics and arbitrary non-convex cost landscapes without requiring analytical gradients.

### 4.1.1 Sampling and Control Optimization

> [!TIP]
> **Foundational Guide:** See [Note 4_1: MPPI Sampling and Control Optimization Explained](./notes/4_1_mppi_sampling_and_control_optimization.md) for an intuitive step-by-step breakdown of candidate sampling, kinematic rollouts, critic scoring, and softmax importance weighting.

At each control cycle ($\Delta t_{\text{ctrl}} \in [20, 50]\text{ ms}$, corresponding to $20\text{--}50\text{ Hz}$):
1. **Control Sequence Perturbation:** Given a nominal control sequence $\mathbf{U} = [\mathbf{u}_0, \mathbf{u}_1, \dots, \mathbf{u}_{N-1}]$, the controller samples $M$ perturbed control candidate trajectories:
   $$\mathbf{v}_{k, m} = \mathbf{u}_k + \boldsymbol{\epsilon}_{k, m}, \quad \boldsymbol{\epsilon}_{k, m} \sim \mathcal{N}(\mathbf{0}, \boldsymbol{\Sigma}), \quad m \in \{1, \dots, M\}$$
   where $N$ is the preview horizon length ($N = T / \Delta t$, e.g., $N=40$ for $T=2.0\text{ s}$, $\Delta t = 0.05\text{ s}$), and $M$ is the number of rollout batches ($M \in [1000, 2000]$ rollouts).
2. **Kinematic Propagation:** For each sample $m$, the robot state trajectory $\mathbf{X}_m = [\mathbf{p}_0, \mathbf{p}_1, \dots, \mathbf{p}_N]$ is integrated forward in time through the robot kinematic model (differential drive or omnidirectional).
3. **Trajectory Cost Evaluation:** The total cost $S(\mathbf{V}_m)$ of candidate sequence $m$ is evaluated across all active critics:
   $$S(\mathbf{V}_m) = \phi(\mathbf{p}_{N, m}) + \sum_{k=0}^{N-1} \left( \sum_{j \in \text{Critics}} w_j \mathcal{L}_j(\mathbf{p}_{k, m}, \mathbf{v}_{k, m}) + \lambda \mathbf{u}_k^T \boldsymbol{\Sigma}^{-1} \mathbf{v}_{k, m} \right)$$
4. **Softmax Weighting & Optimal Control:** The optimal control sequence is synthesized via importance sampling:
   $$w_m = \frac{\exp\left( -\frac{1}{\lambda} \left( S(\mathbf{V}_m) - \min_j S(\mathbf{V}_j) \right) \right)}{\sum_{l=1}^M \exp\left( -\frac{1}{\lambda} \left( S(\mathbf{V}_l) - \min_j S(\mathbf{V}_j) \right) \right)}$$
   $$\mathbf{u}_k^* = \sum_{m=1}^M w_m \mathbf{v}_{k, m}$$
   The initial action $\mathbf{u}_0^*$ is dispatched to the robot base as `cmd_vel`, and the remaining sequence is warm-started for the subsequent iteration.

---

## 4.2 The "Freezing Robot" Pathology in Standard Nav2

### 4.2.1 Spatial Invariance of 2D Costmaps
Default Nav2 architectures (Macenski et al., 2020, 2023) decouple perception from planning using an intermediate 2D costmap grid (`nav2_costmap_2d`). In dynamic environments:
- When a pedestrian enters the robot's sensor field, the costmap marks the agent's instantaneous spatial coordinates at $t = 0$.
- Shipped MPPI obstacle critics (`ObstaclesCritic`, `CostCritic`) query this static occupancy grid. Because the costmap is time-invariant, it evaluates the risk at horizon step $\tau = 1.5\text{ s}$ against where the obstacle is *right now* ($\tau = 0\text{ s}$).

### 4.2.2 Mathematical Manifestation of Controller Freezing
This spatial invariance creates two severe operational failure modes:
1. **False Path Invalidation (Freezing):**
   If a pedestrian crosses perpendicular to a narrow aisle $3\text{ m}$ ahead of the robot at $1.2\text{ m/s}$, the static costmap paints the corridor blocked. Every sampled MPPI trajectory passing down the aisle receives a massive static collision penalty. Consequently, the softmax optimizer collapses forward velocity to zero ($\mathbf{u}^* = [0, 0]^T$), initiating recovery rotations or aborting the task—even though the pedestrian would have fully cleared the corridor before the robot could physically reach that location.
2. **Blind Interception (Collision Risk):**
   If a dynamic agent is moving toward an open space that the robot plans to traverse, the static costmap registers that future collision point as completely free ($0\text{ cost}$). The robot accelerates directly into the crossing path of the agent, forcing an emergency E-stop when the agent abruptly enters the robot's safety deceleration bubble.

---

## 4.3 Custom Dynamic Obstacle Critic Plugin Architecture

> [!TIP]
> **Foundational Guide:** See [Note 4_3: Custom Dynamic Obstacle Critic Plugin Architecture](./notes/4_3_custom_dynamic_obstacle_critic.md) for an intuitive walkthrough of forward obstacle projection, time-expanding Gaussian safety buffers, and the C++ plugin architecture.

To resolve this limitation without replacing the robust Nav2 infrastructure, we implement a custom C++ critic plugin: `DynamicObstaclesCriticPlugin`, dynamically loaded into `nav2_mppi_controller` via `pluginlib`.

```
           /tracked_obstacles (ROS 2 Topic)
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│ DynamicObstaclesCriticPlugin (mppi::critics::CriticFunction)
│
│  For each candidate rollout m in {1 .. M}:
│    For each horizon step k in {0 .. N-1} (tau_k = k * dt):
│      Robot pose: p_robot(tau_k)
│      For each obstacle i in Obstacles:
│        p_obs,i(tau_k) = p_obs,i(0) + v_obs,i * tau_k
│        dist = || p_robot(tau_k) - p_obs,i(tau_k) ||
│        If dist < d_crit:
│          cost_m += w_dyn * exp( -(dist)^2 / (2 * sigma^2(tau_k)) )
│
│  Output: Dynamic Cost Array added to MPPI batch evaluator
└────────────────────────────────────────────────────────┘
```

### 4.3.1 Costmap Decoupling & Dynamic Scan Masking (`/scan_static`)
Before evaluating dynamic trajectories, a critical architectural coupling must be resolved: if the raw `/scan` topic still feeds directly into `nav2_costmap_2d::ObstacleLayer`, walking pedestrians are simultaneously painted onto the static local costmap as lethal barriers ($C = 254$) at $t = 0$. Consequently, the default shipped `ObstaclesCritic` and `CostCritic` would penalize forward rollouts against the $t = 0$ static costmap and freeze the robot even if `DynamicObstaclesCriticPlugin` predicts the corridor will clear by $\tau = 1.5\text{ s}$.

To achieve clean decoupling without modifying `nav2_costmap_2d` internals:
1. **Track-Gated Ray Masking:** In configurations **C1** and **C2**, `lidar_vision_tracker` publishes `/scan_static` for `nav2_costmap_2d::ObstacleLayer` (**C0** retains raw `/scan`). Any laser ray $(r_j, \theta_j)$ falling within $R_{\text{mask}} = R_{\text{obs}} + \delta_{\text{margin}} = 0.50\text{ m}$ of a confirmed active track's centroid $\mathbf{z}_i$ ($\Delta t_{\text{age}} < 100\text{ ms}$) is masked (`NaN` / $+\infty$ so raycasting clears behind the agent without marking a hit point).
2. **100% Fail-Safe Fallback Invariant:** If YOLO/ByteTrack drops a detection or an obstacle approaches from outside the camera's $80^\circ$ horizontal FoV (side/rear), no confirmed track exists at $(r_j, \theta_j)$. The laser return passes through untouched into `/scan_static`, immediately registering on the static costmap and triggering standard Nav2 collision avoidance.

### 4.3.2 Forward Motion Projection Formulation
The critic subscribes to `/tracked_obstacles` (tracked in the fixed `odom` frame to match `data.trajectories` in `nav2_mppi_controller`) published by the perception subsystem at $30\text{ Hz}$. For each sampled trajectory rollout $m \in \{1, \dots, M\}$ and time index $k \in \{0, \dots, N-1\}$ corresponding to lookahead time $\tau_k = k \cdot \Delta t$:

The dynamic obstacle position $\mathbf{p}_{\text{obs}, i}(\tau_k)$ is projected forward assuming constant velocity:

$$\mathbf{p}_{\text{obs}, i}(\tau_k) = \mathbf{p}_{\text{obs}, i}(0) + \mathbf{v}_{\text{obs}, i} \cdot \tau_k$$

*(Note: In ablation configuration **C1**, $\mathbf{v}_{\text{obs}, i}$ is zeroed via a boolean parameter `zero_velocity_ablation = true` so $\mathbf{p}_{\text{obs}, i}(\tau_k) = \mathbf{p}_{\text{obs}, i}(0)$ across all $k$, isolating perception from prediction with zero confounding code differences).*

### 4.3.3 Spatio-Temporal Anisotropic Dynamic Cost Function
To account for growing state estimation uncertainty over the horizon while breaking spatial symmetry (encouraging the robot to pass *behind* crossing pedestrians rather than cutting in front of them), the instantaneous dynamic risk penalty $\mathcal{L}_{\text{dyn}}(\mathbf{p}_{\text{robot}, m}(\tau_k), \tau_k)$ uses a velocity-oriented anisotropic Gaussian repulsion field:

1. **Time-Expanding Lateral & Rear Buffer:**
   $$\sigma_i(\tau_k) = R_{\text{robot}} + R_{\text{obs}} + \alpha \cdot \tau_k$$
   where $R_{\text{robot}} = 0.22\text{ m}$, $R_{\text{obs}} = 0.35\text{ m}$ ($R_{\text{lethal}} = 0.57\text{ m}$), and $\alpha \ge 0$ is the temporal uncertainty expansion rate ($\approx 0.15\text{ m/s}$).
2. **Forward Velocity-Biased Elongation (Protecting TTC):**
   Projecting the relative displacement $\mathbf{d}_{m,k,i} = \mathbf{p}_{\text{robot}, m}(\tau_k) - \mathbf{p}_{\text{obs}, i}(\tau_k)$ onto the obstacle's unit heading vector $\hat{\mathbf{e}}_{\parallel, i} = \mathbf{v}_{\text{obs}, i} / \|\mathbf{v}_{\text{obs}, i}\|$ yields longitudinal projection $d_{\parallel} = \mathbf{d}_{m,k,i} \cdot \hat{\mathbf{e}}_{\parallel, i}$ and lateral squared distance $d_{\perp}^2 = \|\mathbf{d}_{m,k,i}\|^2 - d_{\parallel}^2$. The longitudinal variance is elongated forward of the moving agent ($d_{\parallel} > 0$) by $\sigma_{\text{front}}(\tau_k) = \sigma_i(\tau_k) + \beta_{\text{ttc}}\|\mathbf{v}_{\text{obs}, i}\|$:
   $$\sigma_{\parallel}(\tau_k) = \begin{cases} \sigma_i(\tau_k) + \beta_{\text{ttc}}\|\mathbf{v}_{\text{obs}, i}\|, & \text{if } d_{\parallel} > 0 \text{ (in front of moving obstacle)} \\ \sigma_i(\tau_k), & \text{if } d_{\parallel} \le 0 \text{ (behind obstacle or } \beta_{\text{ttc}} = 0\text{)} \end{cases}$$
3. **Piecewise Cost Evaluation:**
   $$\mathcal{L}_{\text{dyn}}(\mathbf{p}_{\text{robot}, m}(\tau_k), \tau_k) = \sum_{i=1}^{K} \begin{cases} C_{\text{lethal}}, & \text{if } \|\mathbf{d}_{m,k,i}\| < R_{\text{lethal}} \\ w_{\text{dyn}} \cdot \exp\left( -\frac{1}{2}\left(\frac{d_{\parallel}^2}{\sigma_{\parallel}^2(\tau_k)} + \frac{d_{\perp}^2}{\sigma_i^2(\tau_k)}\right) \right), & \text{if } R_{\text{lethal}} \le \|\mathbf{d}_{m,k,i}\| < 3\sigma_{\parallel}(\tau_k) \\ 0, & \text{otherwise} \end{cases}$$
   where $C_{\text{lethal}} = 10^5$ immediately disqualifies colliding trajectories, and the $3\sigma_{\parallel}$ cutoff avoids unnecessary `std::exp` evaluations on distant trajectories.

### 4.3.4 Plugin Interface & Implementation Footprint
The plugin adheres to Nav2's modern C++ interface:
```cpp
namespace nav2_mppi_dynamic_critic
{
class DynamicObstaclesCritic : public mppi::critics::CriticFunction
{
public:
  void initialize() override;
  void score(mppi::models::CriticData & data) override;
  void reset() override;

private:
  rclcpp::Subscription<custom_interfaces::msg::TrackedObstacleArray>::SharedPtr sub_tracks_;
  std::vector<TrackedObstacle> current_obstacles_;
  std::mutex obstacles_mutex_;
  double dynamic_obstacle_weight_;
  double safety_margin_;
  double temporal_expansion_rate_;
};
}  // namespace nav2_mppi_dynamic_critic
```
- **SIMD Batch Evaluation:** Inside `score(data)`, candidate rollouts are evaluated across time steps using vectorized CPU operations (AVX2/NEON) or parallel OpenMP loops, completing within $<0.3\text{ ms}$ for $M = 2000$ trajectories.
- **Maintainability:** The entire plugin requires fewer than 150 lines of clean, idiomatic modern C++ (C++17), eliminating external dependencies beyond Nav2 core and ROS 2 standard libraries.

---

## 4.4 Architectural Fallback: Velocity-Inflated Costmap Layer (R2)

To mitigate integration risk (Risk R2 in project specifications) if `pluginlib` runtime linking encounters blocking issues during development:
- **Fallback Design:** A custom `nav2_costmap_2d::Layer` plugin (`VelocityInflationLayer`) is implemented.
- **Mechanism:** The layer subscribes to `/tracked_obstacles` and inflates directional, anisotropic cost ellipses along the obstacle's velocity vector $\mathbf{v}_{\text{obs}}$ on the local costmap:
  $$\mathbf{r}_{\text{offset}} = \mathbf{v}_{\text{obs}} \cdot \tau_{\text{lookahead}}$$
- **Operational Trade-Off:** While spatial inflation does not achieve true spatio-temporal decoupling (it penalizes space at all times rather than conditioning cost on arrival time $\tau$), it operates seamlessly with all 11 default Nav2 critics and prevents freezing far more effectively than static circular inflation.

---

## 4.5 Comparative Context: Advanced MPPI Formulations in Contemporary Robotics

To position this subsystem within the broader landscape of modern stochastic optimal control, three state-of-the-art MPPI paradigms from recent literature provide important methodological context:

1. **Analytical Safety Guarantees: SE-MPPI (Kang, 2024):**
   - *Paradigm:* Nav2 C++ plugin coupling MPPI with online local-minima detection and a Control Barrier Function (CBF) filter solved via Quadratic Programming (`osqp-eigen`).
   - *Architectural Contrast:* SE-MPPI acts as an *external boundary projection* on the synthesized command $\mathbf{u}_0^*$, leaving rollout costs unconditioned by dynamic trajectories. Our approach modifies the *internal objective landscape* across all $k \in \{0, \dots, N-1\}$ rollout steps, allowing the planner to proactively discover yielding paths seconds before an E-stop or safety filter would be forced to intervene.
2. **Arbitrary Non-Convex Geometry: EXACT-MPPI (Peng et al., 2024):**
   - *Paradigm:* Vectorized Python/JAX framework computing exact Signed Distance Functions (SDF) between complex robot chassis and raw point clouds on edge GPUs.
   - *Architectural Contrast:* EXACT-MPPI prioritizes exact geometric distance for non-circular footprints against unsegmented 3D/2D point clouds, requiring CUDA/JAX runtimes. Our work focuses on semantic entity tracking (pedestrians, carts) for standard circular/differential AMRs, executing entirely within the standard Nav2 C++ CPU/SIMD budget.
3. **Multi-Modal Bifurcation & Constraint Enforcement: CSC-MPPI (RCILab, IROS 2025):**
   - *Paradigm:* GPU-accelerated MPPI using cuML DBSCAN clustering on rollout candidate trajectories to separate left vs. right avoidance modes, combined with primal-dual optimization.
   - *Architectural Contrast:* CSC-MPPI addresses the classic MPPI failure mode where symmetric obstacles cause rollout averaging to collide into the obstacle. In our system, dynamic obstacle velocity $\mathbf{v}_{\text{obs}}$ naturally breaks spatial symmetry: rollouts passing behind a pedestrian have drastically lower dynamic cost than rollouts attempting to cross ahead, naturally preventing mode averaging without requiring heavy GPU clustering pipelines.


