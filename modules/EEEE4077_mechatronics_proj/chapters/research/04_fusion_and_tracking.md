# 4. Modules 2 & 3: Metric LiDAR-Vision Fusion, Tracking & MPPI Control

## 4.1 Module 2: Metric LiDAR-Vision Fusion & State Estimation

### Objective
Deliver robust metric dynamic obstacle tracking at ranges up to $8\text{ m}$ using existing 2D LiDAR scanners and a low-cost monocular RGB camera.

### Sensor Association & Depth Anchoring
1. **Camera Bounding Boxes:** The camera network outputs 2D bounding boxes and semantic class labels (`Pedestrian`, `Forklift`, `Cart`).
2. **LiDAR-to-Camera Projection:** 2D LiDAR planar range points are mapped to pixel coordinates via camera-laser calibration:

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \left( R \begin{bmatrix} X_{\text{lidar}} \\ Y_{\text{lidar}} \\ 0 \end{bmatrix} + t \right)$$

3. **Frustum Ray Gating:**
   - Scan points falling outside the horizontal image span $[u_{\min}, u_{\max}]$ of detected dynamic boxes are eliminated.
   - Within each bounding frustum, a median cluster distance filter extracts the primary obstacle reflection, eliminating background wall penetration and assigning an exact metric $(X, Y)$ coordinate to the detected agent.

### Multi-Target Tracking & State Estimation
An Extended Kalman Filter (EKF) tracks each target's state vector:

$$\mathbf{x}_k = [x, y, v_x, v_y, \psi]^T$$

- Motion models: Constant Turn Rate and Velocity (CTRV) or Constant Velocity (CV) smooth velocity estimates across visual dropouts, temporary occlusions, and sensor jitter.
- Tracks maintain unique track IDs and track confidence lifetimes.

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
