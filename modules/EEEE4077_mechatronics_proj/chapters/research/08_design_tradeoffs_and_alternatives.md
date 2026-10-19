# 8. Design Trade-Offs, Alternatives & Defense Rationales

> **Purpose**: This living document records architectural questions, technical doubts, evaluated alternatives, and turning points. It serves as the definitive engineering defense reference for viva examinations and supervisor technical reviews, grounded in real physical and computational constraints rather than academic theater.

---

## 8.1 Trade-Off 1: Sensor Suite Selection (2D LiDAR + Monocular RGB vs. Standalone Stereo RGB-D vs. 3D LiDAR)

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

## 8.2 Trade-Off 2: Pairing Choice — Why Monocular RGB vs. Stereo/RGB-D (when paired WITH 2D LiDAR)?

### The Doubt / Question
*"If we already retain the 2D LiDAR for $360^\circ$ SLAM, why not pair it with a Stereo Depth camera (e.g., OAK-D, RealSense D435) instead of a simple monocular RGB camera? Wouldn't stereo depth eliminate LiDAR-camera calibration and solve hanging obstacles?"*

### Comparison Matrix

| Evaluation Dimension | 2D LiDAR + Monocular RGB (Selected) | 2D LiDAR + Stereo RGB-D Camera (e.g., OAK-D / RealSense) |
|---|---|---|
| **Ranging Noise at Long Range ($5–8\text{ m}$)** | **Flat $\pm 1–2\text{ cm}$ error:** True physical Time-of-Flight ranging directly from LiDAR | **Quadratic degradation ($\Delta Z \propto Z^2$):** Stereo disparity noise reaches $\pm 0.5–1.0\text{ m}$ at $8\text{ m}$ |
| **Kalman Filter Velocity Stability** | **High stability:** Clean metric position observations allow rapid convergence of $[v_x, v_y]$ | **High variance:** Differentiating $\pm 0.8\text{ m}$ disparity jitter causes severe velocity spikes ($\dot{Z}$) |
| **Vertical Obstacle Coverage** | Planar only (scans at mounting height; blind to hanging forklift tines/tables) | **Full 3D elevation:** $V\text{-FoV} \approx 45^\circ–58^\circ$ captures hanging/overhanging hazards |
| **Lighting & Optical Resilience** | Robust 2D RGB detection under ambient light; metric ranging handled by laser | Active IR speckles wash out under direct sunlight / skylights; passive stereo fails on bare drywall |
| **Edge Compute & USB Bandwidth** | **Minimal:** 1x compressed RGB stream ($\approx 5\text{ MB/s}$); $<0.1\text{ ms}$ geometric ray gating on CPU | **Heavy:** Synchronized RGB + 16-bit Depth stream ($\approx 50–60\text{ MB/s}$); heavy USB interrupt overhead |
| **Total Sensor Suite Cost** | **$\approx \$430 – \$480$** (RPLiDAR + \$30–\$80 USB/CSI camera) | **$\approx \$750 – \$950$** (RPLiDAR + \$350–\$450 RealSense / OAK-D) |

### Defense Rationale
1. **The Quadratic Range Trap in Dynamic Avoidance:** Proactive MPPI trajectory yielding requires predicting crossing agent positions $2.0\text{ s}$ into the future. For a human walking at $1.2\text{ m/s}$ towards a robot moving at $1.0\text{ m/s}$, detection and tracking must begin at $6–8\text{ m}$. Stereo camera depth error grows quadratically:
   $$\Delta Z = \frac{Z^2}{b \cdot f} \Delta d$$
   For a standard compact stereo baseline ($b \approx 50\text{ mm}$), noise at $8\text{ m}$ exceeds $\pm 1.0\text{ m}$. Passing this noisy depth into a Kalman filter creates massive velocity covariance, causing MPPI trajectory evaluation to oscillate erratically. In practice, engineers using stereo + LiDAR still end up discarding stereo depth at $>4\text{ m}$ and falling back to LiDAR range!
2. **Brownfield Industrial Constraints:** Adding a low-cost (\$30–\$60) industrial USB/MIPI camera to an existing warehouse AMR is an economical brownfield upgrade. Upgrading to a $\$450$ stereo camera doubles sensor cost without providing superior velocity estimation.
3. **Handling Vertical Blind Spots:** While stereo provides 3D vertical coverage, industrial AMRs operating on flat warehouse concrete floors primarily encounter full-height dynamic obstacles (pedestrians, other AMRs, pallet jacks). The 2D LiDAR planar slice reliably intersects their lower bodies/chassis, making monocular + 2D LiDAR the optimal Pareto-efficient trade-off.

---

## 8.3 Trade-Off 3: Depth Extraction — Why Geometric LiDAR Frustum Gating vs. Deep Monocular Depth Estimation (MDE)?

### The Doubt / Question
*"If we use a monocular RGB camera, why not run a modern Monocular Depth Estimation (MDE) foundation model (e.g., Depth Anything v2, ZoeDepth, Metric3D) to predict dense depth rather than projecting 2D LiDAR points?"*

### Comparison Matrix

| Evaluation Dimension | Geometric LiDAR Frustum Gating (Selected) | Deep Monocular Depth Estimation (MDE) |
|---|---|---|
| **Depth Accuracy & Ground Truth** | **Deterministic Physical ToF:** Millimeter-accurate physical laser reflection ($\pm 1–2\text{ cm}$) | **Statistical Guess:** Neural network predicts depth based on monocular visual cues |
| **Metric Scale Consistency** | **Exact:** Physically grounded metric coordinates $(x, y)$ in robot base frame | **Scale Ambiguity & Drift:** Standard MDE outputs relative depth; metric MDE suffers domain shift |
| **Runtime Latency on Edge (Jetson Orin Nano)** | **$< 0.1\text{ ms}$** (Single-threaded C++/Python matrix multiplication $K[R \mid t]$) | **$25 – 60\text{ ms}$** (Dense vision transformer / CNN inference; $>1\text{ GB}$ VRAM) |
| **Environmental Generalization** | Unaffected by lighting variations, indoor shadows, or surface texture | Struggles with out-of-distribution warehouse textures, specular reflections, and motion blur |
| **Ground Plane Depth Alternative** | Combined with **Planar Homography / IPM** for ground markings ($<0.2\text{ ms}$) | Required for every frame regardless of whether obstacle is on ground or dynamic |

### Defense Rationale
1. **Avoiding Computational Redundancy:** Running a heavy neural network to predict an estimated depth when the robot *already has* a physical Time-of-Flight laser rangefinder measuring true distance is computationally irrational. A single matrix projection ($<0.1\text{ ms}$) extracts ground truth faster, with zero GPU overhead, preserving edge compute for YOLO-Seg and MPPI rollouts.
2. **Elimination of Metric Scale Hallucination:** Even state-of-the-art metric MDE models (e.g., Metric3D) exhibit $10–25\%$ scale errors when the camera pitch, mounting height, or focal length deviates from their training distribution. In dynamic obstacle avoidance, a $20\%$ scale error creates a $20\%$ velocity error in the Kalman filter, causing MPPI to either yield unnecessarily early or fail to yield before collision.
3. **Role of Analytical Depth (IPM):** For ground hazards (e.g., oil spills, floor signage) where the 2D LiDAR plane does not strike the floor, the system does not need a deep MDE network. It uses analytical **Inverse Perspective Mapping (Planar Homography)** under the flat-ground assumption ($Z=0$), computing exact $(X, Y)$ ground coordinates deterministically in $<0.2\text{ ms}$.

---

## 8.4 Trade-Off 4: Tracking Architecture (2D MOT vs. 3D Hungarian Matching)

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

## 8.5 Trade-Off 5: Motion Control (MPPI Trajectory Critic vs. End-to-End Reinforcement Learning)

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

