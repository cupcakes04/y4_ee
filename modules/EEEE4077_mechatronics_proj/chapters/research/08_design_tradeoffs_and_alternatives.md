# 8. Design Trade-Offs, Alternatives & Defense Rationales

> **Purpose**: This living document records architectural questions, technical doubts, evaluated alternatives, and turning points. It serves as the definitive engineering defense reference for viva examinations and supervisor technical reviews, grounded in real physical and computational constraints rather than academic theater.

---

## 8.1 Trade-Off 1: Sensor Suite Selection

### The Doubt / Question
*"Why use a 2D planar LiDAR combined with a monocular RGB camera instead of an all-in-one stereo depth camera (e.g., Intel RealSense D435/D455, OAK-D) or a modern 3D LiDAR?"*

### Comparison Matrix

| Evaluation Dimension | 2D LiDAR + Monocular RGB (Selected) | Stereo RGB-D Camera (e.g., RealSense / OAK-D) | 3D Mechanical/Solid-State LiDAR |
|---|---|---|---|
| **Horizontal FOV** | **$270^\circ – 360^\circ$** (LiDAR) + $80^\circ$ (Camera) | Narrow: $\approx 65^\circ – 85^\circ$ only | Full $360^\circ$ |
| **Effective Range & Precision** | $10–25\text{ m}$ (mm-level ToF accuracy) | $3–4\text{ m}$ reliable; error grows quadratically ($\Delta Z \propto Z^2$) | $20–100\text{ m}$ (sub-cm accuracy) |
| **Environmental Robustness** | Active laser pulses unaffected by lighting, shadows, or textureless walls | **Fails on textureless surfaces** (blank white drywall, smooth concrete floors, shiny racks) | Excellent in all lighting conditions |
| **Nav2 / SLAM Integration** | Native `sensor_msgs/LaserScan` with $<2\%$ CPU for 2D AMCL / `slam_toolbox` | Requires heavy 3D voxel grids or lossy `depthimage_to_laserscan` conversion | Heavy point cloud CPU/GPU processing |
| **Sensor Hardware Cost** | **$\approx \$430 – \$480$ total** (\$400 2D LiDAR + \$30–\$80 USB/CSI camera) | $\approx \$350 – \$550$ | **$\approx \$3,000 – \$8,000+$** (violates low-cost constraint) |
| **Industrial Reality** | **Brownfield standard:** Existing commercial fleets (TurtleBot 4, MiR, OTTO) already have 2D LiDAR installed | Rarely used as primary navigation sensor on industrial AMRs; usually secondary obstacle detector | Standard on high-end autonomous cars, but too costly for warehouse logistics |

### Defense Rationale
1. **Blind Spots When Turning:** A single stereo camera leaves the AMR completely blind to objects approaching from the sides ($90^\circ$) or rear. An AMR turning around a warehouse pallet corner would risk side collisions without wide-angle LiDAR.
2. **Brownfield Commercial Retrofit:** Real industrial AMRs already deploy with 2D LiDAR for safety certified navigation. Adding an inexpensive monocular camera is a feasible retrofit; replacing the entire sensor suite with multiple stereo cameras is commercially impractical.
3. **Long-Distance Velocity Estimation:** To yield smoothly at $1.5\text{ m/s}$, the robot must track oncoming pedestrian velocities at $5–8\text{ m}$. Stereo depth noise at $8\text{ m}$ is too noisy for stable velocity differentiation; 2D LiDAR provides crisp metric distance.

---

## 8.2 Trade-Off 2: Tracking Architecture (2D MOT vs. 3D Hungarian Matching)

### The Doubt / Question
*"Should data association and tracking be done in 3D metric space after clustering LiDAR points, or in 2D image space directly from the object detector?"*

### Comparison Matrix

| Evaluation Dimension | Decoupled: 2D MOT (ByteTrack) + Linear KF (Selected) | Coupled: Metric 3D Clustering + Hungarian Matching |
|---|---|---|
| **Data Association Layer** | **Image space:** Uses 2D IoU and visual detection similarity across frames | **Metric space:** Uses Euclidean / Mahalanobis distances on laser clusters |
| **Occlusion Handling** | ByteTrack rescues occluded detections via two-stage matching; visual context persists ID | Laser clusters merge into a single blob or swap IDs when pedestrians cross paths |
| **Algorithmic Complexity** | **Standard library (`boxmot`):** Zero custom association code required | Must build a combinatorial assignment engine (Hungarian algorithm, gating thresholds, birth/death logic) from scratch |
| **State Estimator** | Clean, decoupled 1D/2D **Linear Kalman Filter** per track ID ($[x, y, v_x, v_y]^T$) | Complex multi-target EKF maintaining coupled measurement-to-track association matrices |
| **Execution Speed** | $>30\text{ FPS}$ on edge devices | Dependent on clustering resolution and cluster count |

### Defense Rationale
- Decoupling visual association from metric estimation separates concerns: **Vision handles identity persistence (who is who)**, **LiDAR handles metric scale (exact distance in meters)**, and **the Kalman Filter handles noise reduction (velocity in m/s)**.
- This avoids reinventing fragile clustering association algorithms and eliminates the highest algorithmic failure point in sensor fusion.

---

## 8.3 Trade-Off 3: Motion Control (MPPI Trajectory Critic vs. End-to-End Reinforcement Learning)

### The Doubt / Question
*"Why implement a custom MPPI critic inside Nav2 rather than training an End-to-End Reinforcement Learning (RL) or Imitation Learning navigation policy?"*

### Comparison Matrix

| Evaluation Dimension | Nav2 MPPI Dynamic Critic Plugin (Selected) | End-to-End RL / Policy Learning |
|---|---|---|
| **Safety Guarantees** | **Deterministic & Constrained:** Respects robot kinematic limits and Nav2 safety costmap boundaries | **Black-box:** Susceptible to out-of-distribution hallucinations and collisions |
| **Sample Efficiency** | **Zero training needed:** Mathematical forward propagation ($x + v\tau$) evaluated in real-time | Requires millions of simulated training steps; high sim-to-real gap |
| **ROS 2 Ecosystem Fit** | **Idiomatic plugin:** Plugs directly into `nav2_mppi_controller` via `pluginlib` | Replaces standard Nav2; bypasses costmap filters, recoveries, and BT navigators |
| **Debugging & Tuning** | Transparent cost weights (`critical_weight`, `repulsion_weight`) with interpretable failure modes | Difficult reward engineering; impossible to tune specific behaviors deterministically |

### Defense Rationale
- Industrial mobile robotics demands verifiable safety boundaries. End-to-end RL cannot guarantee that the robot will respect site-specific keepout zones or velocity limits.
- MPPI provides the exact mathematical framework needed: it already samples thousands of candidate paths over future time steps. Feeding it predicted obstacle positions through a clean C++ plugin gives proactive evasive behavior while retaining full Nav2 safety guarantees.

