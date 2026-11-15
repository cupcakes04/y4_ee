# Autonomous Mobile Robot (AMR) Navigation Tech Stack & Development Roadmap

> **Purpose:**  
> A sequential, step-by-step developer guide to learning, building, and verifying the complete FYP stack in 100% simulation without wasting time on mechanical fabrication or academic tangents.
>
> It bridges the **foundational robotics stack** (ROS 2 Jazzy, Gazebo Harmonic, Nav2) directly into the **workspace packages** (`custom_interfaces`, `lidar_vision_tracker`, `nav2_mppi_dynamic_critic`, and `ablation_benchmark_harness`), synchronized with the formal 450-hour project plan in [`schedule.md`](../chapters/proposals/schedule.md) and [`specifications.md`](../chapters/proposals/specifications.md).

---

## Current Progress & Status Overview

- **Completed (`✅`):**
  - **Step 1 — ROS 2 Jazzy Core & Spatial `tf2` Frames:** Completed all core tutorials covering workspace lifecycle & `colcon`, `ament_python` / `ament_cmake` packaging, Topics / Services / Actions / Parameters, CLI & `rqt_graph` introspection, modular Python launch systems, and `tf2` (`map -> odom -> base_link`, static/dynamic broadcasters, time travel, `tf2_ros.MessageFilter`). See [`ROS2_notes/notes/01`–`06`](ROS2_notes/notes/README.md).
  - **Step 2a — Robot Modeling & RViz2 Visualization:** Completed URDF/Xacro modeling (`<link>`, `<joint>`, visual vs. collision vs. inertial tags, modular macros), `robot_state_publisher`, `joint_state_publisher_gui`, RViz2 setup, and custom `visualization_msgs/msg/Marker` rendering. See [`ROS2_notes/notes/07_urdf_and_rviz`](ROS2_notes/notes/07_urdf_and_rviz/01_visual_robot_urdf.md).
- **Current Focus / Up Next (`🎯`):**
  - **Step 2b — Gazebo Harmonic & `ros_gz` Simulation Testbed (Task T1, W5–W8):** Pin the Ubuntu 24.04 / Docker workstation environment, attach Gazebo Harmonic plugins (Diff-Drive, 2D LiDAR, RGB Camera, Joint State Publisher) to the URDF/Xacro model, configure `ros_gz_bridge` (including `/clock` for `use_sim_time: true`), and spawn the robot in Gazebo Harmonic.
  - **Immediate Follow-On (Task T2, W7–W12 $\to$ PR1):** Bring up `slam_toolbox` & `AMCL` (Step 3), run Baseline C0 Nav2 MPPI on Scenarios A–D, and execute the **W8 "Hello-Critic" C++ `pluginlib` spike** ahead of **Progress Review 1 (W11–12)**.

---

## The 5-Phase Development Conveyor (Weeks 5–30 | 450 Hours)

Synchronized with [`schedule.md`](../chapters/proposals/schedule.md) (Week 5 true start post-allocation; Weeks 1–4 pre-allocation):

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE A: FOUNDATIONS & BASELINE (Weeks 5–12 | 90 h | T1: 45 h, T2: 45 h)             │
│  [x] Step 1:  ROS 2 Jazzy Core, Launch & Spatial tf2 Frames (ROS2_notes 01–06)       │
│  [x] Step 2a: URDF, Xacro, robot_state_publisher & RViz2 Markers (ROS2_notes 07)     │
│  [>] Step 2b: Gazebo Harmonic Testbed (ros_gz_sim, ros_gz_bridge, Sensors, Docker)   │
│  [ ] Step 3:  2D Mapping (slam_toolbox) & Localization (AMCL)                        │
│  [ ] Step 4:  Baseline C0 Nav2 MPPI (Scenarios A–D) + W8 "Hello-Critic" C++ Spike    │
│               ──► PR1 (W11–12): Baseline C0 measured; toolchain & Docker frozen      │
└──────────────────────────────────────────┬───────────────────────────────────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE B: DYNAMIC TRACKER & HARNESS START (Weeks 9–15 | 110 h | T3: 90 h, T4a: 20 h)  │
│  [ ] Step 5:  lidar_vision_tracker Package (Deliverable O1 — T3)                     │
│   ├── 2D Detection (YOLOv8n/v11n via TensorRT) + 2D MOT (ByteTrack via boxmot)       │
│   ├── Camera–LiDAR Extrinsic Projection ([R|t]) & Frustum Gating (median depth)      │
│   └── Per-Track Linear Kalman Filter (CV) -> Publishes /tracked_obstacles (30 Hz)    │
│  [ ] Step 7a: ablation_benchmark_harness Start (Deliverable O3 — T4a)                │
│   └── Scripted Gazebo dynamic actors & scenario framework + /tf RMSE logger          │
│               ──► PR2 (W13–15): O1 velocity RMSE measured; scenario framework ready  │
└──────────────────────────────────────────┬───────────────────────────────────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE C: CONTROLLER & HARNESS COMPLETION (Weeks 13–20 | 100 h | T5: 75 h, T4b: 25 h) │
│  [ ] Step 6:  nav2_mppi_dynamic_critic Package (Deliverable O2 — T5)                 │
│   ├── Native C++ pluginlib critic extending mppi::critics::CriticFunction            │
│   ├── Spatio-temporal forward projection: p_obs(tau) = p0 + v_obs * tau (0..2.0 s)   │
│   └── Proactive yielding & swerving (< 0.3 ms CPU, 0 freezes, clean static costmap)  │
│  [ ] Step 7b: ablation_benchmark_harness Completion (Deliverable O3 — T4b)           │
│   └── Automated 3-way test runner (C0 vs C1 vs C2) & full metric logging             │
│               ──► PR3 (W19–20): Critic running vs C0/C1; ablation harness operational│
└──────────────────────────────────────────┬───────────────────────────────────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE D: MULTI-SCENARIO COMPARATIVE ABLATION (Weeks 19–24 | 60 h | T6: 60 h)         │
│  [ ] Step 8:  Comparative Simulation Benchmarks (T6)                                 │
│   └── >= 30 paired randomized runs per config (C0, C1, C2) on Scenarios A–E          │
│       (0.5–2.0 m/s, varying densities) + optional Stretch Goals (S1–S3)              │
│               ──► PR4 (W23–24): 3-way ablation results compiled across conditions    │
└──────────────────────────────────────────┬───────────────────────────────────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE E: STATISTICAL ANALYSIS & THESIS (Weeks 23–30 | 90 h | T7: 30 h, T8: 60 h)     │
│  [ ] Step 9:  Statistical Evaluation, Final Thesis & Video Demos (T7 & T8)           │
│   ├── Paired Welch's t-test & one-way ANOVA (p < 0.01 target), 95% CI plots          │
│   └── Reproducible Docker launch, demo videos & MEng thesis (W30 final buffer)       │
│               ──► PR5 (W27–28): Stats complete; thesis & demos ready by W30          │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### Schedule & Milestone Sync Table

| Phase | Weeks | Tasks & Hours | Review Checkpoint | Status |
|---|---|---|---|---|
| **A: Foundations & Baseline** | W5–W12 | **T1:** Env & Docker (W5–W8, 45 h)<br>**T2:** Sim world, actors & C0 baseline (W7–W12, 45 h) | **PR1 (W11–12):** C0 measured on Scenarios A–D; toolchain frozen | Step 1 & 2a `✅` · Step 2b `🎯` |
| **B: Dynamic Tracker** | W9–W15 | **T3:** O1 tracker (W9–W15, 90 h)<br>**T4a:** O3 harness start (W11–W15, 20 h) | **PR2 (W13–15):** O1 velocity RMSE measured; scenarios ready | Pending |
| **C: Controller & Critic** | W13–W20 | **T5:** O2 MPPI critic plugin (W13–W20, 75 h)<br>**T4b:** O3 harness end (W16–W20, 25 h) | **PR3 (W19–20):** Critic running vs C0/C1; harness operational | Pending |
| **D: Multi-Scenario Ablation** | W19–W24 | **T6:** Comparative simulation benchmarks (W19–W24, 60 h) | **PR4 (W23–24):** 3-way ablation results compiled | Pending |
| **E: Analysis & Thesis** | W23–W30 | **T7:** Statistical analysis (W23–W28, 30 h)<br>**T8:** Thesis & video demos (W25–W30, 60 h) | **PR5 (W27–28):** Analysis complete; thesis & demos by W30 | Pending |

---

## Phase A: Foundations & Baseline (Weeks 5–12 | 90 h)

### Step 1: Middleware, Launch Architecture & Spatial `tf2` Frames — `✅ Completed`
- **Reference Notes:** [`01_workspace_and_env`](ROS2_notes/notes/01_workspace_and_env/01_workspace_lifecycle.md) through [`06_tf2_coordinate_frames`](ROS2_notes/notes/06_tf2_coordinate_frames/01_tf2_concepts_and_tree.md)
- **Mastered Foundations:**
  - **Workspace & Packaging:** `colcon` build workflow (`--symlink-install`), underlay vs. overlay sourcing, `ament_python` vs. `ament_cmake`, `package.xml`, `setup.py` / `CMakeLists.txt`, and custom `.msg` / `.action` interface packages.
  - **Communication & CLI:** Topics (continuous sensor streams: `/scan`, `/camera/image_raw`, `/cmd_vel`), Services, Actions (`navigate_to_pose`), Parameters, and CLI / `rqt_graph` introspection.
  - **Launch System:** Modular Python `LaunchDescription` orchestration, substitutions (`LaunchConfiguration`, `FindPackageShare`, `PathJoinSubstitution`), and lifecycle event handlers.
  - **Spatial Coordinate Tree (`tf2`):** REP 105 frame hierarchy:
    $$\text{map} \xrightarrow{\text{SLAM / AMCL}} \text{odom} \xrightarrow{\text{wheel integration}} \text{base\_link} \xrightarrow{\text{sensor mounting}} \text{laser\_link} \ / \ \text{camera\_link}$$
    Static and dynamic broadcasters, 10-second transform buffer time travel, diagnostic tools (`view_frames`, `tf2_echo`, `tf2_monitor`), and `tf2_ros.MessageFilter` for race-free sensor synchronization.

> **Still Skip for Now:**
> - **Composable Nodes (C++) & Intra-Process IPC:** Useful later if profiling shows IPC latency between detector and MPPI, but unnecessary overhead until baseline pipelines work.
> - **`Node Interfaces` Template Class, custom DDS middleware configs, and building ROS 2 from source.**

---

### Step 2a: Robot Modeling & RViz2 Visualization — `✅ Completed`
- **Reference Notes:** [`07_urdf_and_rviz`](ROS2_notes/notes/07_urdf_and_rviz/01_visual_robot_urdf.md) (`01`–`06`)
- **Mastered Foundations:**
  - **URDF & Xacro:** XML `<link>` and `<joint>` (`fixed`, `continuous`, `revolute`) syntax, visual vs. simplified collision primitives, mass/inertia formulas, Xacro macros/variables, and launch-time expansion via `Command(['xacro ', file])`.
  - **Kinematics & Display Pipeline:** `robot_state_publisher` publishing `/tf` & `/tf_static` from URDF + `/joint_states`, verified with `joint_state_publisher_gui` and RViz2 Fixed Frame setup.
  - **Custom 3D RViz2 Visuals ([`06_rviz_markers_and_visualization.md`](ROS2_notes/notes/07_urdf_and_rviz/06_rviz_markers_and_visualization.md)):** Publishing `visualization_msgs/msg/Marker` and `MarkerArray` primitives (`CYLINDER`, `ARROW`, `LINE_STRIP`)—directly reusable in Phases B and C to visualize tracked obstacle footprints, velocity vectors, and predicted trajectories in RViz2.

---

### Step 2b: Gazebo Harmonic & `ros_gz` Integration (Task T1: W5–W8, 45 h) — `🎯 Up Next`
- **Objective:** Pin the reproducible simulation environment (Ubuntu 24.04 / Docker + GPU passthrough) and bring the Xacro AMR model alive inside **Gazebo Harmonic (`gz-sim 8`)**.
- **The Core Stack:**
  - **Environment & Docker Freeze (Risk R1 Mitigation):** Finalize Ubuntu 24.04 host setup (RTX 4070 Ti Super driver + CUDA passthrough) and build a pinned Docker image so all simulations reproduce deterministically (`NF1`).
  - **Gazebo Harmonic Plugins (in Xacro/SDF):**
    1. *Differential-Drive System (`gz-sim-diff-drive-system`):* Subscribes to `/cmd_vel` to actuate wheels and publishes odometry (`odom -> base_link`), constrained to AMR limits ($v_{\max} = 1.0\text{ m/s}$, $\omega_{\max} = 1.5\text{ rad/s}$).
    2. *2D Planar LiDAR (`gz-sim-sensors-system` / `gpu_lidar`):* $360^\circ$ planar scan ($0.1\text{--}12\text{ m}$, $20\text{--}40\text{ Hz}$, $0.5^\circ\text{--}1.0^\circ$ angular resolution) on `/scan` (`sensor_msgs/msg/LaserScan`).
    3. *Monocular RGB Camera (`gz-sim-sensors-system` / `camera`):* 30 FPS RGB stream (720p/1080p, $70^\circ\text{--}90^\circ$ HFOV) on `/camera/image_raw` (`sensor_msgs/msg/Image`) with `/camera/camera_info`.
    4. *Joint State Publisher (`gz-sim-joint-state-publisher-system`):* Publishes simulated wheel joint states to `robot_state_publisher`.
  - **ROS–Gazebo Bridge (`ros_gz_bridge` & `ros_gz_sim`):**
    - Spawn robot via `ros_gz_sim` (`create` executable).
    - Configure `parameter_bridge` YAML to map `/clock` (`use_sim_time: true`), `/cmd_vel`, `/odom`, `/scan`, `/camera/image_raw`, `/camera/camera_info`, and `/tf`.
- **Verification Milestone:** Spawn the differential-drive AMR in an empty/warehouse Gazebo Harmonic world, drive it with `teleop_twist_keyboard`, confirm `use_sim_time: true` syncs across nodes, and view live `/scan` beams and `/camera/image_raw` relative to `base_link` in RViz2.
- **What to Skip:** Complex visual CAD mesh textures, micro friction tuning, and suspension dynamics (use cylinders and boxes).

---

### Step 3: Environment Mapping & Localization (`slam_toolbox` & AMCL — Task T2: W7–W12)
- **Objective:** Convert 2D range measurements and noisy simulated odometry into a persistent 2D floorplan.
- **The Core Stack:**
  - **`slam_toolbox` (Mapping):** Perform laser scan matching and loop closure across the simulated warehouse world (`use_sim_time: true`) to generate an occupancy grid (`map`).
  - **AMCL (Localization):** Adaptive Monte Carlo Localization (particle filter) tracking the robot pose against the saved map (`map.yaml`, `map.pgm`) and broadcasting `map -> odom`.
- **Verification Milestone:** Launch `slam_toolbox`, drive through a multi-corridor Gazebo Harmonic warehouse world to close a loop, save the map, and re-localize using AMCL.
- **What to Skip:** Mathematical proofs of Ceres Solver or 3D visual-inertial SLAM.

---

### Step 4: Baseline C0 Nav2 Bringup & W8 "Hello-Critic" Spike (Task T2: W7–W12 $\to$ PR1: W11–12)
- **Objective:** Establish the frozen **C0 (Baseline)** Nav2 benchmark on Scenarios A–D, observe the Freezing Robot failure mode firsthand, and de-risk C++ plugin development early.
- **The Core Stack:**
  - **Global Planner:** `nav2_navfn_planner` or `SmacPlanner2D` generating static $A^*$ paths.
  - **Local Controller:** `nav2_mppi_controller` ($20\text{ Hz}$, $K = 2000$ rollouts, $T = 2.0\text{ s}$) with default static critics (`ObstaclesCritic`, `CostCritic`, `PathAlignCritic`, `GoalCritic`).
  - **Costmaps (`nav2_costmap_2d`):** Static layer + Obstacle layer (raw `/scan`) + Inflation layer, driven by standard `navigate_to_pose_w_replanning_and_recovery.xml` Behavior Tree.
  - **W8 "Hello-Critic" Spike (Risk R2 Mitigation):** Compile and load a minimal stub class inheriting from `mppi::critics::CriticFunction` via `pluginlib` inside `nav2_mppi_controller` during Week 8 to verify C++ headers, SIMD flags, and runtime plugin loading before Phase C begins.
- **PR1 Verification Milestone (W11–12):** Drop a navigation goal behind a crossing Gazebo actor (Scenarios A–D). Observe and record stock Nav2 marking the actor's legs as occupied static cells—causing abrupt freezes, recovery spins, or goal aborts. Freeze Baseline C0 metrics and toolchain.
- **What to Skip:** Custom Behavior Trees.

---

## Phase B: Dynamic Tracker & Harness Start (Weeks 9–15 | 110 h)

### Step 5: `lidar_vision_tracker` (Deliverable O1 — Task T3: W9–W15, 90 h)
- **Objective:** Fuse monocular camera frames with 2D planar LiDAR scans to publish smoothed, metric dynamic obstacle state vectors $(x, y, v_x, v_y)$.
- **Subsystem Components:**
  1. **Visual Detection (YOLO via TensorRT):** Run edge-optimized detector (YOLOv8n / YOLOv11n, FP16/INT8) on GPU producing bounding boxes $[u_{\min}, v_{\min}, u_{\max}, v_{\max}]$ and classes (`Pedestrian`, `Cart`).
  2. **Image-Space 2D MOT (ByteTrack via `boxmot`):** Maintain persistent integer `track_id`s across frames by associating high- and low-confidence detections via 2D IoU ($<3\text{ ms}$ on CPU), recovering from temporary visual occlusions.
  3. **Extrinsic Projection & Frustum Gating:**
     - Using rigid extrinsic calibration $[R \mid t]$ (Zhang & Pless), project 2D laser scan points into image coordinates:
       $$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{K} \left( \mathbf{R} \begin{bmatrix} X_L \\ Y_L \\ 0 \end{bmatrix} + \mathbf{t} \right)$$
     - Gate laser rays falling within $[u_{\min}, u_{\max}]$ of each active tracked box and apply a median distance filter to reject background wall penetrations, yielding a metric measurement $(z_x, z_y)$ per `track_id`.
  4. **Per-Track Linear Kalman Filter (CV):**
     - State vector $\mathbf{x} = [x, y, v_x, v_y]^T$ using a discrete Constant Velocity model to smooth sensor noise and estimate velocities with uncertainty covariances.
- **Output & Visualization Interfaces:**
  - Publish `custom_interfaces/msg/TrackedObstacleArray` on `/tracked_obstacles` at $30\text{ Hz}$.
  - Publish `visualization_msgs/msg/MarkerArray` (building on Step 2a) to inspect tracked bounding cylinders, IDs, and velocity arrows in RViz2.
- **Verification Milestone & Specifications (`specifications.md` O1-a, O1-b):** Evaluate against Gazebo simulator ground-truth `/tf` across $\ge 30$ randomized crossings at range $\le 8\text{ m}$:
  - **Velocity RMSE:** Minimum $< 0.25\text{ m/s}$ | Target **$< 0.15\text{ m/s}$**.
  - **Data Association Accuracy ($< 0.3\text{ m}$ Euclidean error):** Minimum $\ge 85\%$ | Target **$\ge 95\%$**.
- **What to Skip:** 3D point cloud Euclidean clustering, DeepSORT ReID feature extractors, and end-to-end multimodal neural networks.

### Step 7a: `ablation_benchmark_harness` Start (Deliverable O3 — Task T4a: W11–W15, 20 h $\to$ PR2: W13–15)
- **Objective:** Build the Gazebo Harmonic scripted dynamic actor worlds (Scenarios A–D) and automated ground-truth `/tf` logger ahead of PR2.
- **PR2 Verification Milestone (W13–15):** O1 velocity RMSE and association accuracy verified against ground truth; dynamic scenario framework operational.

---

## Phase C: Predictive Controller & Harness Completion (Weeks 13–20 | 100 h)

### Step 6: `nav2_mppi_dynamic_critic` (Deliverable O2 — Task T5: W13–W20, 75 h)
- **Objective:** Extend Nav2's MPPI controller with a native C++ `pluginlib` critic that forward-projects dynamic obstacle positions across candidate trajectory rollouts.
- **Subsystem Architecture:**
  1. **`pluginlib` Interface:** Implement a C++ class inheriting from `mppi::critics::CriticFunction`:
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
     - Subscribe to `/tracked_obstacles`.
     - Across $K = 2000$ candidate rollouts and horizon steps $k \in [0, 39]$ ($\Delta t = 0.05\text{ s}$, $T = 2.0\text{ s}$, lookahead time $\tau_k = k \cdot \Delta t$):
       $$\mathbf{p}_{\text{obs}}(\tau_k) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}} \cdot \tau_k$$
     - Compute separation $d = \|\mathbf{p}_{\text{robot}}(\tau_k) - \mathbf{p}_{\text{obs}}(\tau_k)\|$ and apply an exponential repulsion penalty executing in $< 0.3\text{ ms}$ on CPU:
       $$\text{Cost} = w_{\text{dyn}} \cdot \exp\left( -\frac{d^2}{2 \, \sigma^2(\tau_k)} \right)$$
  3. **Preserving Costmap Integrity:** Dynamic obstacles are **never** marked onto `nav2_costmap_2d`. Static critics handle walls; the dynamic critic handles moving traffic.
- **Architectural Fallback (Risk R2 / Fallback F1):** If native `pluginlib` linking encounters blocking issues, implement a custom `nav2_costmap_2d::Layer` (`VelocityInflationLayer`) projecting velocity-inflated directional cost cones along $\mathbf{v}_{\text{obs}}$.
- **Verification Milestone & Specifications (`specifications.md` O2-a, O2-b, O2-c, O3-c):**
  - **Controller Freezing:** Minimum $\ge 50\%$ below C0 | Target **$0$ freezes** per 10 crossings.
  - **Mean Route Completion Time:** Minimum $\ge 10\%$ shorter | Target **$15\text{--}25\%$ shorter**.
  - **Collision-Free Traversal:** **$0$ physics contact collisions** (hard constraint).
  - **End-to-End Control Loop Rate:** Minimum $\ge 15\text{ Hz}$ | Target **$\ge 20\text{ Hz}$**.

### Step 7b: `ablation_benchmark_harness` Completion (Deliverable O3 — Task T4b: W16–W20, 25 h $\to$ PR3: W19–20)
- **Objective:** Finalize the automated 3-way ablation switch (**C0**, **C1** with $\mathbf{v}_{\text{obs}} = \mathbf{0}$, **C2** full predictive) and complete automated ground-truth logging ($N_{\text{freeze}}$, cumulative waiting time where $|v| < 0.05\text{ m/s}$, $\text{TTC}_{\min}$, $T_{\text{mission}}$, normalized jerk $J_{\text{norm}}$, and loop frequency).
- **PR3 Verification Milestone (W19–20):** `nav2_mppi_dynamic_critic` running smoothly against C0 and C1; automated ablation harness fully operational.

---

## Phase D: Multi-Scenario Comparative Ablation (Weeks 19–24 | 60 h)

### Step 8: Comparative Simulation Benchmarks (Deliverable O3 — Task T6: W19–W24, 60 h $\to$ PR4: W23–24)
- **Objective:** Execute the controlled 3-way comparative ablation benchmark fulfilling supervisor specification `SD-MEng-26-01`:
  - **C0 (Baseline):** 2D LiDAR only + standard static Nav2 MPPI critics.
  - **C1 (Detection Only):** 2D LiDAR + Camera detection, zeroing velocity ($\mathbf{v}_{\text{obs}} = \mathbf{0}$) to isolate visual detection from prediction.
  - **C2 (Full Proposed System):** Multi-modal tracking + Predictive MPPI dynamic critic forward-propagating rollouts.
- **Standardized Gazebo Harmonic Scenarios (A–E):**
  - **Scenario A:** Perpendicular corridor crossing ($1.2\text{ m/s}$).
  - **Scenario B:** Oncoming head-on encounter down a shared aisle.
  - **Scenario C:** Oblique cross-traffic ($1.8\text{--}2.0\text{ m/s}$).
  - **Scenario D:** Multi-agent bottleneck (2–4 staggered crossing pedestrians).
  - **Scenario E:** Static baseline control (regression testing).
- **Trial Protocol:** Run $\ge 30$ automated paired randomized trials per configuration with identical random seeds across crossing speeds ($0.5\text{--}2.0\text{ m/s}$).
- **Optional Stretch Goals (If Ahead of Schedule at PR3 / W22):**
  - **S1:** Multi-agent crowd density stress test (4–6 interacting agents).
  - **S2:** High-speed ($2.5\text{ m/s}$) and non-orthogonal crossing angles ($30^\circ, 45^\circ, 135^\circ$).
  - **S3:** 4-core CPU-only containerized profiling (`cgroups` limit) to validate brownfield edge CPU feasibility.
- **PR4 Verification Milestone (W23–24):** Full 3-way ablation datasets compiled across speeds and densities.

---

## Phase E: Statistical Analysis & Thesis (Weeks 23–30 | 90 h)

### Step 9: Statistical Evaluation, Final Thesis & Video Demos (Tasks T7: 30 h, T8: 60 h $\to$ PR5: W27–28, Submission: W30)
- **Objective:** Quantify statistical significance, finalize reproducible artifacts, and deliver the MEng thesis.
- **Statistical & Reproducibility Verification (`specifications.md` O3-a, O3-b, NF1):**
  - Run **paired Welch's t-tests** and **one-way ANOVA** across C0, C1, and C2: Minimum **$p < 0.05$** | Target **$p < 0.01$**, with 95% confidence intervals and comparison boxplots.
  - Verify **Cumulative Waiting Time Reduction:** Minimum $\ge 50\%$ reduction vs. C0 | Target **$\le 5\text{ s}$ per run**.
  - Archive `rosbag2` logs and verify single-command launch reproducibility inside the pinned Docker container (`NF1`).
- **PR5 & Final Delivery (W27–30):**
  - **PR5 (W27–28):** Statistical analysis complete.
  - **W25–30:** Write final dissertation and record simulation demo videos; **Week 30** is strictly reserved as a final proofreading and submission buffer.

---

## Target ROS 2 Workspace Layout (`colcon_ws/src/`)

Reference architecture from [`06_hardware_and_stack.md`](../chapters/research/06_hardware_and_stack.md):

```
colcon_ws/src/
├── custom_interfaces/
│   ├── msg/ (TrackedObstacle.msg, TrackedObstacleArray.msg)
│   └── CMakeLists.txt
├── lidar_vision_tracker/                 # Deliverable O1
│   ├── config/ (detector params, [R|t] calibration, KF Q/R matrices)
│   ├── src/ (tensorrt_detector, bytetrack, frustum_gating, kalman_filter)
│   └── CMakeLists.txt
├── nav2_mppi_dynamic_critic/             # Deliverable O2
│   ├── include/nav2_mppi_dynamic_critic/dynamic_obstacles_critic.hpp
│   ├── src/dynamic_obstacles_critic.cpp
│   ├── dynamic_critics.xml (pluginlib export)
│   └── CMakeLists.txt
└── ablation_benchmark_harness/           # Deliverable O3
    ├── launch/ (sim bringup, scenario launches)
    ├── worlds/ (Gazebo Harmonic warehouse models)
    ├── scripts/ (batch C0/C1/C2 runner, metrics logger, statistical plots)
    └── CMakeLists.txt
```

---

## Development Environment & Pinned Tool Versions

All packages target **Ubuntu 24.04 LTS** (workstation with NVIDIA RTX 4070 Ti Super, 32 GB RAM) and pinned Docker reproducibility:

| Software Component | Target Version | Purpose |
|---|---|---|
| **OS** | Ubuntu 24.04 LTS (Noble Numbat) | Host OS / Pinned Docker container |
| **ROS Distribution** | **ROS 2 Jazzy Jalisco** (LTS until May 2029) | Core robotics middleware & Nav2 |
| **Simulator & Bridge** | **Gazebo Harmonic** (`gz-sim 8`), `ros_gz_sim`, `ros_gz_bridge` | Physics, sensors (`gpu_lidar`, `camera`), and dynamic actors |
| **Navigation Stack** | Nav2 (`nav2_mppi_controller`, `slam_toolbox`, `nav2_amcl`) | SLAM, localization, global planning, and MPPI control |
| **Perception Framework** | TensorRT 10.x, PyTorch 2.x, OpenCV 4.x | Real-time GPU inference & image processing |
| **Tracking Library** | `boxmot` (ByteTrack integration) | 2D multi-object tracking in image space |
| **Linear Algebra** | Eigen3 (C++) | Matrix operations for Kalman filter and MPPI |

---

## What to Deliberately Skip (Boundary Enforcement)

To avoid cognitive overload and stay strictly within the 450-hour budget:
1. **NO Physical Fabrication:** 0% hardware fabrication. 100% simulated in Gazebo Harmonic (`SD-MEng-26-01`).
2. **NO Deep Trajectory Transformers:** Do not implement generative or diffusion-based pedestrian prediction models. A linear Kalman filter executes in $< 0.2\text{ ms}$ and provides accurate short-horizon velocity over $T = 2.0\text{ s}$.
3. **NO Online Foundation Models:** Foundation models (Florence-2, SAM) stay strictly out of the real-time loop; any exploratory VLM notes remain in `chapters/explore/`.
4. **NO Multi-Robot Fleet Dispatchers:** Do not install Open-RMF or VDA 5050. Focus exclusively on single-robot local collision avoidance.
5. **NO 3D Mesh / Voxel Reconstruction:** Adhere strictly to planar LiDAR + 2D image coordinates to maintain $\ge 20\text{ Hz}$ control execution and $30\text{ FPS}$ perception.
