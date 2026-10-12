# 4. Modules 2 & 3: Metric LiDAR-Vision Fusion, Tracking & MPPI Control

## 4.1 Module 2: Metric LiDAR-Vision Fusion & State Estimation

### Objective
Deliver robust metric dynamic obstacle tracking at ranges up to $8\text{ m}$ using existing 2D LiDAR scanners and a low-cost monocular RGB camera.

### Two-Stage Decoupled Tracking & Fusion Architecture

#### Stage 1: 2D Multi-Object Tracking in Image Space (ByteTrack)
1. **Object Detection:** The edge segmentation network (YOLO-Seg via TensorRT) outputs 2D bounding boxes and semantic class labels (`Pedestrian`, `Forklift`, `Cart`).
2. **2D Association (ByteTrack):**
   - Instead of discarding low-confidence detections, **ByteTrack (Zhang et al., 2022)** (integrated via `boxmot`) associates both high-score and low-score boxes using 2D motion and IoU similarity.
   - This maintains persistent target identities (`track_id`) across frames, bridges brief visual occlusions, and eliminates the need for expensive visual ReID feature extractors.
   - **Benefit:** Solves data association entirely in image space, avoiding fragile combinatorial matching on raw geometric point clouds.

#### Stage 2: LiDAR Frustum Gating & Depth Anchoring
1. **LiDAR-to-Camera Projection:** 2D LiDAR planar range points are mapped to pixel coordinates via camera-laser extrinsic calibration (Zhang & Pless, 2004):

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \left( R \begin{bmatrix} X_{\text{lidar}} \\ Y_{\text{lidar}} \\ 0 \end{bmatrix} + t \right)$$

2. **Frustum Ray Gating:**
   - Scan points falling within the horizontal image span $[u_{\min}, u_{\max}]$ of each active tracked box are isolated.
   - A median cluster distance filter extracts the primary obstacle reflection, eliminating background wall penetration and assigning an exact metric measurement $(z_x, z_y)$ directly to the corresponding `track_id`.

#### Stage 3: Per-Track Metric State Estimation (Linear Kalman Filter)
Because target identity is already established by Stage 1, state estimation reduces to an independent linear Kalman Filter per active `track_id`:

$$\mathbf{x}_k = [x, y, v_x, v_y]^T$$

- **Motion Model:** Constant Velocity (CV) model smoothly estimates metric velocities $(v_x, v_y)$ and velocity covariances across frame drops and laser jitter (Thrun et al., 2005).
- **Output:** Publishes `/tracked_obstacles` with metric position, velocity, and uncertainty ellipses for direct consumption by the MPPI controller.

---

## 4.2 Module 3: Dynamic Obstacle Critic for Predictive MPPI Control

### Objective
Transform reactive emergency halts into proactive speed yielding and smooth evasive trajectory deflections.

### MPPI Integration Architecture
1. **Dynamic State Consumption:** State estimates $(x, y, v_x, v_y, \psi)$ are fed directly to a custom trajectory evaluation critic inside `nav2_mppi_controller`.
2. **Forward Collision Projection:** For each sampled trajectory rollout, the critic projects target obstacle positions forward across the preview horizon ($T = 2.0\text{ s}$):

$$\mathbf{x}_{\text{obs}}(t+\tau) = \mathbf{x}_{\text{obs}}(t) + \mathbf{v}_{\text{obs}} \cdot \tau, \quad \tau \in [0, T]$$

3. **Trajectory Cost Evaluation:**
   - The critic penalizes rollouts that intersect the forward-propagating collision covariance ellipse.
   - This drives the MPPI optimizer to proactively yield or swerve around crossing traffic while adhering to Nav2 Costmap Filter boundaries.

---

## 4.3 Engineering Rationale & Comparative Nav2 Architecture

### The Nav2 Baseline & The "Freezing Robot" Problem
1. **Static 2D Costmap Limitation:**
   - Default Nav2 obstacle avoidance relies on 2D costmaps (`nav2_costmap_2d`), which represent the environment as a time-invariant grid ($t = 0$).
   - When a pedestrian or vehicle crosses the robot's corridor, the costmap marks only their instantaneous location.
2. **Failure Modes of Fast Reactive Replanning (20–50 Hz):**
   - Standard MPPI evaluates trajectory rollouts against static costmap cells using `CostCritic` / `ObstaclesCritic`.
   - Because it lacks temporal awareness of obstacle motion, the controller cannot anticipate where the obstacle will be at lookahead horizon $\tau \in [0.5, 2.0]\text{ s}$.
   - This results in two major operational pathologies:
     - **Conservative Stalling / Freezing:** The robot abruptly stops because the obstacle currently blocks the path, even if the pedestrian will have cleared the corridor by the time the robot arrives.
     - **Path Crossing Invalidation:** The robot attempts to swerve directly into the future trajectory of a crossing agent.

### Idiomatic Nav2 Extension: Why a Custom MPPI Critic?
Writing a custom MPPI critic is **not** an attempt to invent a new planning paradigm from scratch; it is the official, idiomatic extension pattern provided by Nav2:
- **Built-in Plugins:** Nav2 ships 11 default critics (`ConstraintCritic`, `CostCritic`, `GoalCritic`, `GoalAngleCritic`, `PathAlignCritic`, `PathFollowCritic`, `PathAngleCritic`, `PreferForwardCritic`, `TwirlingCritic`, `VelocityDeadbandCritic`, and `ObstaclesCritic`). All obstacle-scoring critics query the static 2D costmap.
- **`pluginlib` Modularity:** MPPI is explicitly architected around C++ plugin evaluation (`mppi::critics::CriticFunction`).
- **Spatio-Temporal Rollouts:** In MPPI, candidate trajectories are already simulated over discrete time steps $\tau_k = k \cdot \Delta t$. A custom critic simply computes the Euclidean/Mahalanobis distance between the simulated robot pose $\mathbf{p}_{\text{robot}}(\tau_k)$ and the forward-projected obstacle state $\mathbf{p}_{\text{obs}}(\tau_k) = \mathbf{p}_{\text{obs}}(0) + \mathbf{v}_{\text{obs}} \tau_k$.
- **Implementation Footprint:** This requires only a concise C++ plugin (~80–120 LOC), making it technically disciplined and maintainable.

### Architectural Fallback (Risk Mitigation R2)
If the C++ `pluginlib` critic integration encounters unexpected blockers during Milestone M3:
- **Fallback Pattern:** Implement a custom `nav2_costmap_2d::Layer` that subscribes to obstacle tracks and projects directional cost inflation cones along $\mathbf{v}_{\text{obs}}$ ("velocity smearing").
- **Trade-off:** While purely spatial and lacking true spatio-temporal decoupling, it provides a proven, zero-controller-modification fallback that still influences default Nav2 critics.

### Grounding in Literature
- **Extrinsic Geometry:** Camera-LiDAR extrinsic transformation $[R \mid t]$ is established using the classical planar checkerboard method of Zhang & Pless (2004).
- **State Estimation:** Multi-target state tracking utilizes standard Extended Kalman Filtering with constant-velocity motion models (Thrun et al., 2005).
- **Control Integration:** Predictive rollout optimization builds upon Model Predictive Path Integral control principles (Williams et al., 2017) adapted into Nav2's modern controller framework (Macenski et al., 2020, 2023).

