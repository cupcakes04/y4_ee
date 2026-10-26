# 3. Perception & Metric Dynamic Obstacle Tracking

This chapter details the mathematical formulation, algorithmic pipeline, and engineering design of the multi-modal dynamic obstacle tracking subsystem (**Module 1**). The subsystem fuses 2D planar LiDAR with monocular RGB vision to produce metric dynamic obstacle states $[x, y, v_x, v_y]^T$ at real-time edge frame rates ($\ge 30\text{ Hz}$).

---

## 3.1 Problem Definition & Sensor Complementarity

Brownfield warehouse AMRs typically rely on single-plane safety LiDARs mounted 10–20 cm above the floor. While providing millimeter-accurate range measurements, planar scans collapse 3D scene geometry into sparse, disconnected point clusters. A human pedestrian moving across the floor appears merely as two transient, oscillating points representing leg slices. Consequently:
1. **Semantic Blindness:** The LiDAR cannot distinguish a moving human from a static pallet leg or structural pillar.
2. **Identity Loss:** Discontinuous point returns and step-phase occlusions cause standard Euclidean clustering algorithms to fail data association, resulting in frequent track fragmentation and false velocity spikes.
3. **Monocular Scale Ambiguity:** Conversely, monocular vision offers rich semantic context and stable visual feature association, but inherently lacks direct metric depth information.

By establishing an associative bridge between monocular vision and planar LiDAR, each sensor directly compensates for the fundamental physical limitation of the other:
- Vision provides **target semantic classification**, **bounding frustum limits**, and **persistent image-space identity**.
- LiDAR provides **absolute metric ground truth distance** without requiring computationally demanding stereo matching or depth neural networks.

---

## 3.2 Stage 1: 2D Multi-Object Tracking in Image Space

Data association across frames is solved entirely in 2D image coordinates prior to metric back-projection. This avoids fragile 3D point cloud clustering and combinatorial geometric matching.

### 3.2.1 Object Detection
Incoming monocular RGB video frames ($1920 \times 1080$ or $1280 \times 720$ at 30 FPS) are passed to an edge-optimized detector (YOLOv8n / YOLOv11n) compiled into an INT8/FP16 engine via NVIDIA TensorRT. The network outputs 2D bounding boxes $B_i = [u_{\min}, v_{\min}, u_{\max}, v_{\max}]$, confidence scores $s_i$, and category labels (`Pedestrian`, `Forklift`, `Cart`).

### 3.2.2 ByteTrack Data Association
Rather than discarding low-confidence bounding boxes—which frequently arise during motion blur, partial occlusion, or long-range encounters—the tracker utilizes **ByteTrack** (Zhang et al., 2022) via `boxmot`:
1. **First Association Step:** High-confidence detections ($s_i \ge \theta_{\text{high}} = 0.6$) are matched against existing active track predictions using Intersection-over-Union (IoU) distance solved via the Hungarian algorithm.
2. **Second Association Step:** Unmatched tracks from the first step are subsequently matched against low-confidence detections ($\theta_{\text{low}} \le s_i < \theta_{\text{high}}$, where $\theta_{\text{low}} = 0.1$). This preserves track continuity when a pedestrian is temporarily obscured or passes through shadow regions without introducing false background tracks.
3. **Track Lifecycle Management:** Tracks maintain state flags: `New`, `Tracked`, `Lost`, and `Removed`. Unmatched tracks are coasted for $N_{\text{max\_lost}} = 30$ frames (1.0 s) before deallocation.

This guarantees persistent integer identifiers (`track_id`) throughout the robot's field of view.

---

## 3.3 Stage 2: Camera-LiDAR Extrinsic Calibration & Frustum Gating

> [!TIP]
> **Foundational Guide:** See [Note 01: Sensor Coordinate Frames, Transformations & Frustum Gating](./notes/01_camera_lidar_frames_and_gating.md) for an intuitive visual walkthrough of LiDAR vs Camera spaces, pinhole projection, and the median filter.

### 3.3.1 Geometric Calibration Formulation
The spatial transformation between the 2D planar LiDAR frame $\mathcal{F}_{\text{lidar}}$ and the monocular camera optical frame $\mathcal{F}_{\text{cam}}$ is established using the classical planar checkerboard method of Zhang & Pless (2004). 

Let a planar LiDAR measurement point be defined in homogeneous coordinates as $\mathbf{P}_{\text{lidar}} = [X_L, Y_L, 0, 1]^T$. The projection to normalised camera pixel coordinates $\mathbf{p} = [u, v, 1]^T$ is governed by:

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{K} \begin{bmatrix} \mathbf{R} & \mathbf{t} \end{bmatrix} \begin{bmatrix} X_L \\ Y_L \\ 0 \\ 1 \end{bmatrix}$$

where:
- $\mathbf{K} \in \mathbb{R}^{3 \times 3}$ is the intrinsic camera calibration matrix obtained via pinhole calibration:
  $$\mathbf{K} = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$
- $\mathbf{R} \in SO(3)$ and $\mathbf{t} \in \mathbb{R}^3$ represent the extrinsic rotation and translation rigidly relating $\mathcal{F}_{\text{lidar}}$ to $\mathcal{F}_{\text{cam}}$.
- $\lambda$ is a projective scale factor corresponding to the optical axis depth $Z_{\text{cam}}$.

### 3.3.2 Frustum Ray Gating & Depth Association
For each laser scan ray $\mathbf{P}_j = (r_j, \theta_j)$ received from `/scan`:
1. The ray is converted to Cartesian coordinates $(X_L, Y_L)$ and projected to pixel coordinates $(u_j, v_j)$ using the calibrated extrinsic matrix.
2. A ray is associated with active track $B_k = [u_{\min}^k, v_{\min}^k, u_{\max}^k, v_{\max}^k]$ if its projected horizontal coordinate falls strictly within the bounding box frustum:
   $$u_{\min}^k \le u_j \le u_{\max}^k$$
3. **Median Range Clustering:** Because a 2D laser ray passing through an image bounding box may penetrate behind the target and hit background walls or shelving, raw range returns within the frustum are clustered. A median distance filter extracts the primary foreground cluster:
   $$d_k^* = \operatorname{median} \{ r_j \mid u_j \in [u_{\min}^k, u_{\max}^k] \text{ and } r_j < r_{\text{background\_threshold}} \}$$
4. The metric Cartesian observation $\mathbf{z}_k = [x_m, y_m]^T$ in the robot base frame $\mathcal{F}_{\text{base}}$ is computed directly from $(d_k^*, \theta_k^*)$, establishing an unambiguous metric position bound to `track_id`.

---

## 3.4 Stage 3: Per-Track Metric State Estimation (Kalman Filter)

> [!TIP]
> **Control Theory Connection:** See [Note 02: The Kalman Filter as a Modern State-Space Observer](./notes/02_kalman_filter_as_state_space_observer.md) for the derivation connecting this filter to state-space control, Luenberger observers, and LQG theory.

Because data association and identity persistence are already guaranteed by ByteTrack in image space, state estimation simplifies to an independent linear discrete Kalman Filter instantiated for each active `track_id`.

### 3.4.1 State Space & Motion Dynamics
The dynamic state of obstacle $i$ at discrete time step $k$ is parameterized in the robot odometry/map frame as:

$$\mathbf{x}_k = \begin{bmatrix} x_k \\ y_k \\ v_{x,k} \\ v_{y,k} \end{bmatrix}$$

Assuming a Constant Velocity (CV) kinematic model (Thrun et al., 2005) with sample interval $\Delta t$:

$$\mathbf{x}_{k+1} = \mathbf{F} \mathbf{x}_k + \mathbf{w}_k, \quad \mathbf{w}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$$

$$\mathbf{F} = \begin{bmatrix} 1 & 0 & \Delta t & 0 \\ 0 & 1 & 0 & \Delta t \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

The process noise covariance matrix $\mathbf{Q}$ models unpredictable pedestrian accelerations:

$$\mathbf{Q} = q_c \begin{bmatrix} \frac{\Delta t^3}{3} & 0 & \frac{\Delta t^2}{2} & 0 \\ 0 & \frac{\Delta t^3}{3} & 0 & \frac{\Delta t^2}{2} \\ \frac{\Delta t^2}{2} & 0 & \Delta t & 0 \\ 0 & \frac{\Delta t^2}{2} & 0 & \Delta t \end{bmatrix}$$

where $q_c$ is the continuous process acceleration spectral density parameter ($q_c \approx 0.5\text{--}1.0\text{ m}^2/\text{s}^3$ for pedestrian dynamics).

### 3.4.2 Measurement Model & Gating
The observation vector corresponds to the Cartesian position extracted from the gated LiDAR return:

$$\mathbf{z}_k = \begin{bmatrix} z_{x,k} \\ z_{y,k} \end{bmatrix} = \mathbf{H} \mathbf{x}_k + \mathbf{v}_k, \quad \mathbf{v}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{R})$$

$$\mathbf{H} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{bmatrix}$$

$$\mathbf{R} = \begin{bmatrix} \sigma_{\text{lidar}}^2 & 0 \\ 0 & \sigma_{\text{lidar}}^2 \end{bmatrix}, \quad \sigma_{\text{lidar}} \approx 0.03\text{ m}$$

Before applying the measurement update, spurious noise and occluded multipath reflections are rejected using a Chi-square Mahalanobis distance gate:

$$d_M^2 = \mathbf{y}_k^T \mathbf{S}_k^{-1} \mathbf{y}_k < \gamma_{\text{gate}}$$

where innovation $\mathbf{y}_k = \mathbf{z}_k - \mathbf{H} \hat{\mathbf{x}}_{k|k-1}$ and innovation covariance $\mathbf{S}_k = \mathbf{H} \mathbf{P}_{k|k-1} \mathbf{H}^T + \mathbf{R}$.

### 3.4.3 Predict & Update Cycle
1. **Time Update (Prediction):**
   $$\hat{\mathbf{x}}_{k|k-1} = \mathbf{F} \hat{\mathbf{x}}_{k-1|k-1}$$
   $$\mathbf{P}_{k|k-1} = \mathbf{F} \mathbf{P}_{k-1|k-1} \mathbf{F}^T + \mathbf{Q}$$
2. **Measurement Update (Correction):**
   $$\mathbf{K}_k = \mathbf{P}_{k|k-1} \mathbf{H}^T \mathbf{S}_k^{-1}$$
   $$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k \mathbf{y}_k$$
   $$\mathbf{P}_{k|k} = (\mathbf{I} - \mathbf{K}_k \mathbf{H}) \mathbf{P}_{k|k-1}$$

---

## 3.5 ROS 2 Interface & Performance Budget

### 3.5.1 Topic Interface
The subsystem is encapsulated in the `lidar_vision_tracker` ROS 2 package:
- **Subscribed Topics:**
  - `/camera/image_raw` (`sensor_msgs/msg/Image`, 30 Hz)
  - `/camera/camera_info` (`sensor_msgs/msg/CameraInfo`)
  - `/scan` (`sensor_msgs/msg/LaserScan`, 20–40 Hz)
  - `/tf`, `/tf_static` (Rigid frame tree: `camera_link` $\to$ `base_link` $\to$ `map`)
- **Published Topic:**
  - `/tracked_obstacles` (`custom_interfaces/msg/TrackedObstacleArray`, 30 Hz)
    ```
    std_msgs/Header header
    TrackedObstacle[] obstacles
      uint32 track_id
      string label
      geometry_msgs/Point position
      geometry_msgs/Vector3 velocity
      float64[16] covariance
      float32 confidence
    ```

### 3.5.2 Execution Latency Budget
To maintain the required 30 Hz pipeline rate, the stage execution budget on edge compute (NVIDIA Jetson / x86 mobile GPU) is constrained as follows:

| Subsystem Stage | Implementation | Latency Budget |
|---|---|---|
| Monocular Object Detection | YOLO TensorRT (INT8/FP16) | $12\text{--}18\text{ ms}$ |
| 2D Visual Tracking | ByteTrack (C++ / Cython) | $1\text{--}2\text{ ms}$ |
| Frustum Ray Gating | Vectorized NumPy / C++ | $1\text{--}2\text{ ms}$ |
| Metric Kalman Filter Update | Linear Eigen3 C++ matrix ops | $<0.2\text{ ms}$ |
| Total Perception Pipeline | Real-Time ROS 2 Node | $\mathbf{\le 25\text{ ms}}$ ($\ge 40\text{ Hz}$ throughput) |

