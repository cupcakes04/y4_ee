# Autonomous Mobile Robot (AMR) Navigation Tech Stack & Development Roadmap

> **Purpose:**  
> A sequential, step-by-step developer guide to learning, building, and verifying the complete FYP stack in 100% simulation without wasting time on mechanical fabrication or academic tangents.
>
> It bridges the **foundational robotics stack** (ROS 2, Gazebo, Nav2) directly into the **three core FYP engineering deliverables** (`lidar_vision_tracker`, `nav2_mppi_dynamic_critic`, and `ablation_benchmark_harness`).

---

## The 4-Phase Development Conveyor

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: FOUNDATIONAL SIMULATION & NAV2 BASELINE (Weeks 1–6)                     │
│  Step 1: ROS 2 Jazzy Core & Spatial TF2 Frames                                   │
│  Step 2: Gazebo Harmonic Testbed (URDF + Diff-Drive + 2D LiDAR + Camera)         │
│  Step 3: 2D Mapping (slam_toolbox) & Localization (AMCL)                         │
│  Step 4: Baseline Nav2 MPPI Bringup (Observe the "Freezing Robot" failure mode)   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: PERCEPTION & STATE ESTIMATION — Module 1 (Weeks 7–12)                   │
│  Step 5: lidar_vision_tracker Package                                            │
│   ├── 2D Detection (YOLO via TensorRT) + Multi-Object Tracking (ByteTrack)       │
│   ├── Camera-LiDAR Extrinsic Projection & Frustum Gating                         │
│   └── Per-Track Linear Kalman Filter (CV) -> Publishes /tracked_obstacles        │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: PREDICTIVE TRAJECTORY CONTROL — Module 2 (Weeks 13–18)                  │
│  Step 6: nav2_mppi_dynamic_critic Package                                        │
│   ├── C++ pluginlib architecture extending mppi::critics::CriticFunction         │
│   ├── Spatio-temporal dynamic forward projection: p_obs(tau) = p0 + v*tau        │
│   └── Verification: Proactive yielding & swerving (Zero Freezes)                 │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: AUTOMATED BENCHMARK & 3-WAY ABLATION — Module 3 (Weeks 19–24)           │
│  Step 7: ablation_benchmark_harness Package                                      │
│   ├── Scripted Gazebo dynamic actors (Scenarios A–E, varying speeds & densities) │
│   ├── Automated 3-way test runner (C0: Baseline vs C1: Detection vs C2: Predict) │
│   └── Automated ground-truth logging (Freezes, Min TTC, Velocity RMSE)           │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundational Simulation & Baseline Nav2 (Weeks 1–6)

### Step 1: Middleware & Spatial Transformations (ROS 2 Core)
- **Objective:** Master communication plumbing and spatial reference frames. Do not write complex algorithms yet; learn how data moves through the robot.
- **Key Concepts:**
  - **Topics vs. Actions:** Topics stream continuous sensor feeds (`/scan`, `/camera/image_raw`, `/cmd_vel`). Actions handle asynchronous, cancelable goals with progress feedback (`navigate_to_pose`).
  - **The Coordinate Tree (`tf2`):** Navigation is entirely frame transformations:
    $$\text{map} \xrightarrow{\text{SLAM / AMCL}} \text{odom} \xrightarrow{\text{wheel integration}} \text{base\_link} \xrightarrow{\text{sensor mounting}} \text{laser\_link} \ / \ \text{camera\_link}$$
  - Understand why `base_link` represents the robot's physical center and how transformations are buffered across time.
- **Verification Milestone:** Write a minimal ROS 2 node that broadcasts a dynamic coordinate frame, and view the transform tree using `ros2 run tf2_tools view_frames`.
- **What to Skip:** Multi-threaded executor internals, custom DDS middleware configurations, and building ROS 2 from source.

> Skip these:
> - Managing Dependencies with rosdep: Standard package installation via apt suffices for now.
> - Writing a Composable Node (C++) & Composing multiple nodes in a single process: Useful later when eliminating IPC latency between your detector and MPPI on edge hardware, but premature overhead for learning spatial plumbing.
> - Using the Node Interfaces Template Class (C++): Internal architecture abstraction; unnecessary for standard application pipelines.
> - Monitoring for parameter changes (C++ / Python): You will use standard dynamic parameters later when tuning MPPI, but it is not needed to master tf2.
> - Testing: Standard unit/integration testing framework; non-blocking for step 1.
> - RViz: Skim the basic display tutorial only if you have never used RViz. Otherwise, you will interact with RViz naturally while visualizing TF and robot models during the tf2 and URDF tutorials.

### Step 2: Virtual Kinematics & Physics (URDF & Gazebo Harmonic)
- **Objective:** Build a simulated mobile robot and its sensors in Gazebo Harmonic. This completely replaces the physical hardware.
- **The Core Stack:**
  - **URDF / Xacro:** XML description of the differential-drive chassis (`<link>`) and wheels (`<joint>`).
  - **Gazebo Plugins:**
    1. *Diff-Drive Plugin:* Subscribes to `/cmd_vel` to drive wheels and publishes odometry (`odom -> base_link`).
    2. *2D LiDAR Plugin (Ray):* Simulates $360^\circ$ planar range returns on `/scan` (`sensor_msgs/msg/LaserScan`).
    3. *Camera Plugin:* Publishes 30 FPS RGB frames on `/camera/image_raw` (`sensor_msgs/msg/Image`) with `/camera/camera_info`.
- **Verification Milestone:** Spawn the robot in Gazebo, drive it with `teleop_twist_keyboard`, and view the laser scan beams and live camera stream in RViz2 relative to `base_link`.
- **What to Skip:** Complex collision mesh textures, micro friction tuning, and suspension dynamics. Use basic primitives (cylinders and boxes).

### Step 3: Environment Mapping & Localization (`slam_toolbox` & AMCL)
- **Objective:** Convert 2D range measurements and noisy odometry into a persistent 2D floorplan.
- **The Core Stack:**
  - **`slam_toolbox` (Mapping):** Place nodes along the robot trajectory, perform laser scan matching, and close loops to generate an occupancy grid (`map`).
  - **AMCL (Localization):** Adaptive Monte Carlo Localization (particle filter) that tracks the robot's pose against the saved map once mapping is complete, continuously broadcasting `map -> odom`.
- **Verification Milestone:** Launch `slam_toolbox`, drive the robot through a multi-room Gazebo world to close a loop, save the map (`map.yaml`, `map.pgm`), and re-localize using AMCL.
- **What to Skip:** Mathematical proofs of non-linear least squares (Ceres Solver) or 3D visual-inertial SLAM.

### Step 4: Baseline Nav2 Bringup & Observing Controller Freezing
- **Objective:** Run stock ROS 2 Nav2 and observe the "freezing robot" problem firsthand.
- **The Core Stack:**
  - **Global Planner:** `nav2_navfn_planner` or `SmacPlanner2D` generating static $A^*$ paths.
  - **Local Controller:** `nav2_mppi_controller` configured with default static critics (`ObstaclesCritic`, `CostCritic`, `PathAlignCritic`, `GoalCritic`).
  - **Costmaps (`nav2_costmap_2d`):** Static layer (walls) + Obstacle layer (raw LiDAR points) + Inflation layer.
- **Verification Milestone:** Drop a navigation goal behind a crossing dynamic actor in Gazebo. Observe standard Nav2 mark the actor's legs as occupied costmap cells, causing the robot to abruptly freeze, trigger recovery spins, or abort the goal.
- **What to Skip:** Writing custom behavior trees. Use standard `navigate_to_pose_w_replanning_and_recovery.xml`.

---

## Phase 2: Multi-Modal Perception & State Estimation (Weeks 7–12)

### Step 5: `lidar_vision_tracker` (Deliverable O1)
- **Objective:** Fuse monocular camera frames with 2D planar LiDAR scans to publish smoothed, metric dynamic obstacle state vectors $(x, y, v_x, v_y)$.
- **Subsystem Components:**
  1. **Visual Detection (YOLO via TensorRT):** Run an edge-optimized object detector (YOLOv8n / YOLOv11n) on GPU producing bounding boxes $[u_{\min}, v_{\min}, u_{\max}, v_{\max}]$ and classes (`Pedestrian`, `Cart`).
  2. **Image-Space 2D MOT (ByteTrack via `boxmot`):** Maintain persistent integer identities (`track_id`) across frames by matching high- and low-confidence detections via IoU, recovering from visual occlusions.
  3. **Extrinsic Projection & Frustum Gating:**
     - Using rigid extrinsic calibration $[R \mid t]$ (Zhang & Pless), project 2D laser scan points into image coordinates:
       $$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{K} \left( \mathbf{R} \begin{bmatrix} X_L \\ Y_L \\ 0 \end{bmatrix} + \mathbf{t} \right)$$
     - Isolate laser rays falling within the horizontal span $[u_{\min}, u_{\max}]$ of each active tracked box.
     - Apply a median distance filter to reject background wall penetrations, yielding an exact metric measurement $(z_x, z_y)$ assigned to `track_id`.
  4. **Per-Track Linear Kalman Filter:**
     - State vector: $\mathbf{x} = [x, y, v_x, v_y]^T$ using a discrete Constant Velocity (CV) model.
     - Smooth out sensor noise and calculate velocity vectors with uncertainty covariances.
- **Output Interface:** Publish `/tracked_obstacles` (`custom_interfaces/msg/TrackedObstacleArray`) at $30\text{ Hz}$.
- **Verification Milestone:** Measure velocity vector RMSE against Gazebo simulator ground truth. Target: $\text{RMSE}_v < 0.15\text{ m/s}$ across crossing pedestrians.
- **What to Skip:** Heavy 3D point cloud clustering algorithms (e.g. Euclidean cluster extraction on raw clouds), deep visual ReID appearance feature extractors, and end-to-end multi-modal deep networks.

---

## Phase 3: Predictive Local Planning in Nav2 (Weeks 13–18)

### Step 6: `nav2_mppi_dynamic_critic` (Deliverable O2)
- **Objective:** Extend Nav2's MPPI controller with a custom C++ `pluginlib` critic that evaluates dynamic obstacle positions forward across rollout horizons.
- **Subsystem Architecture:**
  1. **`pluginlib` Interface:** Create a C++ class inheriting from `mppi::critics::CriticFunction`:
     ```cpp
     namespace nav2_mppi_dynamic_critic {
     class DynamicObstaclesCritic : public mppi::critics::CriticFunction {
     public:
       void initialize() override;
       void score(mppi::models::CriticData & data) override;
       void reset() override;
     };
     }
     ```
  2. **Temporal Forward Projection:**
     - Inside `score(data)`, subscribe to `/tracked_obstacles`.
     - For each candidate trajectory rollout $m \in [1, 2000]$ and horizon step $k$ at lookahead time $\tau_k = k \cdot \Delta t$:
       $$\mathbf{p}_{\text{obs}}(\tau_k) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}} \cdot \tau_k$$
     - Evaluate distance $d = \|\mathbf{p}_{\text{robot}}(\tau_k) - \mathbf{p}_{\text{obs}}(\tau_k)\|$.
     - Apply exponential repulsion penalty:
       $$\text{Cost} = w_{\text{dyn}} \cdot \exp\left( -\frac{d^2}{2 \, \sigma^2(\tau_k)} \right)$$
  3. **Preserving Costmap Integrity:** Dynamic obstacles are **not** marked onto the static 2D costmap. Static critics handle walls; the dynamic critic handles moving traffic.
- **Verification Milestone:** Re-run the crossing scenario from Step 4. Confirm the robot smoothly yields or swerves around the crossing pedestrian with **0 freezing events** and zero emergency stops.
- **Architectural Fallback (Risk R2 / F1):** If C++ `pluginlib` linking encounters blocking issues, implement a custom `nav2_costmap_2d::Layer` that projects velocity-inflated directional cost cones along $\mathbf{v}_{\text{obs}}$.

---

## Phase 4: Systematic 3-Way Ablation Benchmark (Weeks 19–24)

### Step 7: `ablation_benchmark_harness` (Deliverable O3)
- **Objective:** Fulfill the supervisor specification (`SD-MEng-26-01`) by designing and automating an empirical 3-way ablation study.
- **The 3 Configurations Tested:**
  - **C0 (Baseline):** 2D LiDAR only + standard static Nav2 MPPI critics.
  - **C1 (Detection Only):** 2D LiDAR + Camera detection, but zeroing velocity ($\mathbf{v}_{\text{obs}} = \mathbf{0}$) to isolate whether visual detection alone prevents freezing.
  - **C2 (Full Proposed System):** Multi-modal tracking + Predictive MPPI dynamic critic forward-propagating rollouts.
- **Testing Scenarios (Gazebo Harmonic):**
  - **Scenario A:** Perpendicular corridor crossing ($1.2\text{ m/s}$).
  - **Scenario B:** Oncoming head-on encounter down a shared aisle.
  - **Scenario C:** Oblique cross-traffic vehicle ($1.8\text{--}2.0\text{ m/s}$).
  - **Scenario D:** Multi-agent bottleneck (2–4 staggered crossing pedestrians).
  - **Scenario E:** Static baseline control (regression testing).
- **Automated Metric Suite:**
  - Freezing Episode Count ($N_{\text{freeze}}$)
  - Minimum Time-to-Collision ($\text{TTC}_{\min}$)
  - Mission Completion Time ($T_{\text{mission}}$)
  - Kinematic Smoothness / Normalized Jerk ($J_{\text{norm}}$)
- **Verification Milestone:** Execute 30 automated paired runs per configuration with identical random seeds. Generate automated comparison boxplots and paired Student's t-test / ANOVA tables ($p < 0.05$).

---

## Development Environment & Pinned Tool Versions

All packages run on Ubuntu 24.04 LTS (desktop workstation with NVIDIA RTX 4070 Ti Super):

| Software Component | Target Version | Purpose |
|---|---|---|
| **OS** | Ubuntu 24.04 LTS (Noble Numbat) | Host OS / Pinned Docker container |
| **ROS Distribution** | **ROS 2 Jazzy Jalisco** (LTS until May 2029) | Core robotics middleware & Nav2 |
| **Simulator** | **Gazebo Harmonic** (gz-sim 8) | Modern physics, sensors, and actor plugins |
| **Navigation Stack** | Nav2 (`nav2_mppi_controller`, `slam_toolbox`) | Global & local trajectory generation |
| **Perception Framework** | TensorRT 10.x, PyTorch 2.x, OpenCV 4.x | Real-time GPU inference & image processing |
| **Tracking Library** | `boxmot` (ByteTrack integration) | 2D multi-object tracking in image space |
| **Linear Algebra** | Eigen3 (C++) | Matrix operations for Kalman filter and MPPI |

---

## What to Deliberately Skip (Boundary Enforcement)

To avoid cognitive overload and finish within the 450-hour budget:
1. **NO Physical Fabrication:** 0% hardware fabrication. 100% simulated in Gazebo Harmonic.
2. **NO Deep Trajectory Transformers:** Do not implement heavy generative or diffusion-based pedestrian prediction models. A linear Kalman filter executes in $<0.2\text{ ms}$ and provides all necessary velocity accuracy over a $2.0\text{ s}$ horizon.
3. **NO Online Foundation Models:** Foundation models (Florence-2, SAM) are strictly out of the real-time loop; any exploratory VLM work remains in `explore/`.
4. **NO Multi-Robot Fleet Dispatchers:** Do not install Open-RMF or VDA 5050. Focus exclusively on single-robot local collision avoidance.
5. **NO 3D Mesh / Voxel Reconstruction:** Adhere strictly to planar LiDAR + 2D image coordinates to maintain $\ge 30\text{ FPS}$ execution.