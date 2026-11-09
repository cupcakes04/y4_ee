# 2. System Architecture & Information Flow

The proposed system establishes a deterministic, high-rate multi-modal perception and predictive control pipeline designed to overcome the "freezing robot" problem in dynamic industrial environments. The architecture augments standard 2D safety LiDAR with monocular vision, performs persistent multi-object tracking and metric state estimation, and directly evaluates short-term motion predictions within a custom Nav2 MPPI trajectory critic plugin.

---

## 2.1 End-to-End System Architecture

```
                    ┌────────────────────────────┐
                    │ Monocular RGB Camera Stream│ (30 FPS, base_link / optical_frame)
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ 2D Object Detection & MOT  │ (YOLOv8n / YOLOv11n via TensorRT FP16)
                    │  ByteTrack (boxmot)        │ Persistent track_id in image space
                    └─────────────┬──────────────┘
                                  │ Active 2D Bounding Frustums [u_min, u_max]
                                  ▼
[2D LiDAR Scan] ──► ┌────────────────────────────┐ ──► /scan_static (Dynamic Rays Masked to NaN/Inf)
(/scan @ 20-40 Hz)  │ LiDAR Frustum Gating &     │     │ (Unconfirmed/static rays pass 100% untouched)
                    │ ABD Foreground Clustering  │     ▼
                    └─────────────┬──────────────┘ ┌──────────────────────┐
                                  │ Metric (z_x,z_y)│ nav2_costmap_2d      │
                                  ▼                 │ (Static Walls Only)  │
                    ┌────────────────────────────┐ └──────────┬───────────┘
                    │ Per-Track Kalman Filter    │            │
                    │ State & Covariance Update  │            │
                    └─────────────┬──────────────┘            │
                                  │ /tracked_obstacles (30 Hz)│
══════════════════════════════════╪═══════════════════════════╪════════════════════════════════════
                                  │  NAV2 PREDICTIVE LOCAL PLANNING PIPELINE
                                  ▼                           ▼
                    ┌────────────────────────────────────────────────────────────┐
                    │            nav2_mppi_controller (20-50 Hz)                 │
                    │                                                            │
                    │ ┌──────────────────────┐  ┌──────────────────────────────┐ │
                    │ │ Trajectory Rollouts  │  │ DynamicObstaclesCriticPlugin │ │
                    │ │ {p(tau_k)}_k=1..N    │──►  p_obs(tau) = p0 + v_obs*tau │ │
                    │ └──────────────────────┘  │  Anisotropic Velocity Penalty│ │
                    │                           └──────────────┬───────────────┘ │
                    │ ┌──────────────────────┐                 │                 │
                    │ │ Default Static       │                 │ Penalized Cost  │
                    │ │ Critics (Costmap2D)  │─────────────────┤ Tensor          │
                    │ └──────────────────────┘                 │                 │
                    │                                          ▼                 │
                    │                      Softmax / Temperature Control Weighting│
                    └─────────────────────────────┬──────────────────────────────┘
                                                  │ Optimal Control Command
                                                  ▼
                                      ┌──────────────────────┐
                                      │ cmd_vel (Base Drive) │
                                      └──────────────────────┘
═══════════════════════════════════════════════════════════════════════════════════════════════════
                               ABLATION & BENCHMARK HARNESS
               ┌────────────────────────────────────────────────────────────┐
               │         Gazebo Harmonic Simulation Environment             │
               │  - Scripted Dynamic Pedestrians & Industrial Agv/Carts     │
               │  - Trajectory Ground Truth Logging (/tf, actor states)     │
               │  - Automated Scenario Executor (Scenarios A-E)             │
               │  - Metrics: Freezes, Min TTC, Velocity RMSE, Smoothness    │
               └────────────────────────────────────────────────────────────┘
```

---

## 2.2 Operational Subsystems

The system is decomposed into three cohesive subsystems:

### 1. Multi-Modal Perception & Tracking Subsystem (`lidar_vision_tracker`)
- **Visual Association in Image Space:** Monocular RGB frames are processed by an edge-optimized detector (YOLO via TensorRT). Bounding boxes are tracked across frames using ByteTrack. By solving data association in image space, persistent target identities (`track_id`) are maintained through occlusions without fragile point-cloud clustering.
- **LiDAR Frustum Gating & ABD Foreground Clustering:** Using rigid extrinsic calibration $[R \mid t]$ and positive optical half-space culling ($Z_C > r_{\min}$), 2D planar LiDAR returns are projected into image coordinates. Because up to $70\text{--}80\%$ of horizontal laser rays inside a pedestrian's torso-width bounding box $[u_{\min}, u_{\max}]$ can pass between or beside their legs and hit background walls, a naive statistical median across all frustum rays would falsely lock onto the background wall. Instead, rays inside each frustum are segmented via an **Adaptive Breakpoint Detector (ABD)** (Borges & Aldon range-adaptive jump distance), selecting the **nearest foreground cluster** ($\ge 2$ contiguous points gated by Kalman innovation) to establish unambiguous metric $(x, y)$ positions.
- **Track-Gated Dynamic Scan Masking (`/scan_static`):** To prevent `nav2_costmap_2d::ObstacleLayer` from painting tracked pedestrians as lethal static barriers at $t = 0$ (which would cause default `ObstaclesCritic` to freeze the robot despite our custom dynamic critic), laser rays falling within $R_{\text{mask}} = 0.50\text{ m}$ of confirmed active tracks ($\Delta t_{\text{age}} < 100\text{ ms}$) are masked (`NaN`/`Inf`) on `/scan_static`. Untracked or out-of-FoV rays pass through $100\%$ untouched as a fail-safe fallback.
- **Metric State Filtering:** For each active `track_id`, an independent linear Kalman filter with a Constant Velocity (CV) model in the fixed `odom` frame estimates the full state vector $[x, y, v_x, v_y]^T$ and dynamic uncertainty covariance, publishing `/tracked_obstacles` at $\ge 30\text{ Hz}$.

### 2. Predictive Trajectory Control Subsystem (`nav2_mppi_dynamic_critic`)
- **Idiomatic Nav2 Extension:** Implemented as a C++ `pluginlib` critic inside the standard `nav2_mppi_controller`.
- **Spatio-Temporal Horizon Projection:** For every sampled candidate rollout across the lookahead horizon ($T = 2.0\text{ s}$), the critic extrapolates the dynamic obstacle positions forward in time:
  $$\mathbf{p}_{\text{obs}}(\tau_k) = \mathbf{p}_{\text{obs}}(0) + \mathbf{v}_{\text{obs}} \cdot \tau_k, \quad \tau_k = k \cdot \Delta t$$
- **Velocity-Aware Risk Evaluation:** Candidate trajectories passing close to an obstacle's projected future coordinates receive an exponential cost penalty. This drives the optimizer to proactively yield, slow down, or swerve around moving obstacles well before they intersect the robot's footprint, preventing the costmap "freezing robot" failure mode.

### 3. Simulation & Automated Benchmark Subsystem (`ablation_benchmark_harness`)
- **Gazebo Harmonic Testbed:** Implements deterministic, reproducible industrial scenarios featuring animated pedestrians and mobile machinery.
- **3-Way Comparative Matrix:** Evaluates Baseline 2D LiDAR (C0), Vision Detection without Motion Prediction (C1), and Full Predictive MPPI (C2) under identical seeds, speeds ($0.5\text{--}2.0\text{ m/s}$), and obstacle densities ($1\text{--}4$ dynamic agents).
- **Automated Metric Extraction:** Computes freezing episode counts, Minimum Time-to-Collision ($\text{TTC}_{\min}$), clearance distance, trajectory completion time, and control effort.

---

## 2.3 Architectural Decoupling Rationale

1. **Deterministic Safety Loop ($\ge 30\text{ Hz}$):**
   - Traditional deep neural trajectory prediction networks (e.g., social transformers, diffusion-based path predictors) incur significant compute latency ($50\text{--}200\text{ ms}$) and variable execution times unsuitable for edge deployment.
   - Decoupling visual association (handled in parallel at 30 FPS) from analytical motion extrapolation ($<0.2\text{ ms}$ per critic evaluation) guarantees deterministic loop rates within a lightweight compute footprint.
2. **Complementary Sensor Anchoring:**
   - Monocular vision provides rich semantic classification, angular boundaries, and continuous identity tracking, but suffers from metric scale ambiguity and illumination variance.
   - 2D planar LiDAR provides millimetre-accurate metric distance and immunity to lighting variations, but lacks semantic awareness and identity persistence.
   - The frustum gating fusion links the strengths of both modalities at negligible computational overhead compared to full 3D point cloud processing.
3. **Preserving Costmap Integrity:**
   - Static 2D costmaps (`nav2_costmap_2d`) are retained for permanent infrastructure (walls, structural columns, static pallets).
   - Dynamic agents are handled outside the static costmap layer directly in the MPPI critic, completely eliminating the false-positive inflation and ghost trails that cause standard Nav2 controllers to stall.
