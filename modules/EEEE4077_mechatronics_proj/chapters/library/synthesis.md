# Thematic Literature Review Synthesis

This document synthesizes the academic foundations and industrial context supporting the project, organized into three technical pillars and a commercial motivation.

---

## Pillar 1: Sensor Fusion and Dynamic Tracking in Low-Cost Robotics

Autonomous mobile robots operating in brownfield logistics face severe perceptual constraints when relying solely on 2D safety LiDARs. While single-plane LiDAR provides high-precision range measurements ($<1\text{ cm}$ accuracy) over wide operational angles, it collapses three-dimensional geometric structures into sparse, disconnected planar point clusters. When human pedestrians or material handling equipment cross the scan plane, the sensor records isolated reflections (such as cross-sections of human lower limbs) without photometric or volumetric signatures.

In traditional robotic navigation stacks, including the classical ROS navigation pipeline and baseline Nav2 configurations, these point returns are registered directly into 2D occupancy grids as static obstacles. Consequently, crossing dynamic agents provoke the classic **"Freezing Robot Problem"** first formalized by Trautman and Krause [L1]: the robot treats moving agents as immovable barriers, triggering abrupt deceleration, controller aborts, and repeated recovery rotations.

To restore state awareness without escalating hardware costs to multi-channel 3D LiDAR arrays, late-fusion architectures combining 2D planar LiDAR with monocular RGB cameras represent an optimal compromise. The spatial relationship between planar laser scanners and monocular cameras is grounded in planar checkerboard extrinsic calibration techniques developed by Zhang and Pless [L5]. By projecting laser scan points into the calibrated camera image frame:

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \left( R \begin{bmatrix} X_{\text{lidar}} \\ Y_{\text{lidar}} \\ 0 \end{bmatrix} + t \right)$$

the robot establishes an associative link between visual detections and metric ranges. Monocular bounding boxes derived from 2D vision eliminate LiDAR point fragmentation, while bounded LiDAR range returns resolve the fundamental scale ambiguity inherent in monocular vision. Filtering raw ranges through visual bounding frustums and tracking targets using an Extended Kalman Filter (EKF) with Constant Velocity (CV) or Constant Turn Rate and Velocity (CTRV) models [L12] yields full dynamic obstacle state vectors $(x, y, v_x, v_y, \psi)$ at low sensor cost.

---

## Pillar 2: Vision-Language Foundation Models & Edge Distillation

Recent advances in foundation models have revolutionized zero-shot robotic scene understanding. Large Vision-Language Models (VLMs) and promptable segmentation architectures, notably Florence-2 [L6] and Grounded-SAM [L7], demonstrate unprecedented capabilities in localizing open-vocabulary objects and understanding fine-grained visual instructions without task-specific training data.

However, the computational footprint of these foundation models introduces a severe deployment bottleneck. Large vision foundation models require billions of parameters, executing at latencies exceeding $500\text{ ms}$ on high-end server GPUs and failing to achieve viable control frame rates on edge compute. Real-time robotic navigation requires deterministic sensing at frequencies $\ge 20\text{ Hz}$.

To bridge this disparity, the academic frontier has turned to **knowledge distillation**. Rather than querying heavy foundation models during live robot operation, the teacher model is deployed offline as an automated pseudo-labeler. Works such as ViLAM [L8] explore distilling foundation model reasoning into navigation features. In our engineering pipeline, offline walkthrough videos are auto-annotated by Florence-2 and Grounded-SAM from text prompts (e.g., `"forklift transit lane"`, `"fluid spill"`). This knowledge is distilled into lightweight edge architectures (such as YOLOv8-Seg or YOLOv11-Seg) compiled via TensorRT FP16, delivering $\ge 25\text{ FPS}$ sustained execution on low-cost edge platforms.

---

## Pillar 3: Semantic Costmaps and Predictive MPPI Control in Nav2

The ROS 2 navigation framework (Nav2) represents the open-source industrial standard for mobile robot autonomy [L2, L3]. Historically, Nav2 costmaps maintained binary traversability based strictly on physical obstacle occupancy. Recent versions introduced **Nav2 Costmap Filters** [L10], which allow arbitrary geometric spatial layers to encode Keepout Zones and Speed Restriction Zones via `CostmapFilterInfo`. Traditionally, these filters require facilities engineering teams to manually draft CAD vectors, an approach that is brittle and expensive in brownfield facilities with shifting layouts. By employing planar Inverse Perspective Mapping (IPM), our pipeline projects distilled semantic floor masks directly into Nav2 Costmap Filter polygons automatically.

For trajectory generation, Model Predictive Path Integral (MPPI) control [L4, L11] has emerged as a premier algorithm in Nav2. MPPI samples hundreds of candidate trajectory rollouts concurrently on GPU or multi-threaded CPU hardware to optimize non-linear dynamics. However, an analysis of the Nav2 codebase reveals that the 11 built-in trajectory critics evaluate obstacles strictly as static geometrical hazards. Even with MPPI, standard Nav2 robots halt when dynamic cross-traffic intersects their projected path. By formulating a bespoke **dynamic obstacle critic** that propagates tracked obstacle velocities forward across the predictive horizon ($T = 2.0\text{ s}$), the robot transitions from reactive halts to proactive deceleration and smooth evasive navigation.

---

## Pillar 4: Commercial Scale and Industrial Imperative

The practical necessity of retrofitting existing brownfield AMRs is substantiated by commercial robotics market data. According to the International Federation of Robotics (IFR) [L9], professional service robot deployments are dominated by the transportation and logistics sector, which registered over 102,900 commercial units in 2024 (a 14% year-on-year increase). The vast majority of these logistics robots are deployed in cost-sensitive mid-tier warehousing and manufacturing facilities where replacing 2D LiDAR fleets with high-end 3D perception is financially prohibitive. A retrofit pipeline combining rapid prompt-distilled semantic adaptation with late-fusion dynamic tracking addresses this exact commercial demand.
