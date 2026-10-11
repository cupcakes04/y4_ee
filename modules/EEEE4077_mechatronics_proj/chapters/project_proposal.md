# Engineering Project Proposal

**Project Title:** A Rapid-Deployment Visual Context and Dynamic Tracking Pipeline for Cost-Constrained AMRs in Brownfield Logistics

**Target Domain:** Brownfield Industrial Logistics, Warehouse Automation, Low-Cost Autonomous Mobile Robots (AMRs)

**Core Stack:** ROS 2 (Humble/Iron), Nav2 (`nav2_mppi_controller`, Costmap Filters), TensorRT, 2D Planar LiDAR, Monocular RGB Camera, Offline Foundation Models (Florence-2 / Grounded-SAM)

---

## 1. Executive Summary & Problem Statement

### 1.1 The Brownfield Deployment Bottleneck

In brownfield industrial environments (legacy manufacturing plants and mid-tier distribution centers), Autonomous Mobile Robots (AMRs) must operate alongside human foot traffic and manual material handling equipment without the benefit of facility redesigns. To remain economically viable, these platforms avoid multi-thousand-dollar 3D LiDAR arrays and instead rely on single-plane 2D safety LiDARs paired with classical 2D occupancy grids (Nav2 costmaps).

While 2D LiDAR SLAM and static localization (e.g., AMCL, Cartographer) are mature, this architecture exhibits severe operational bottlenecks when deployed in active brownfield environments:

1. **Dynamic Deadlock ("Freezing Robot Problem"):** 2D LiDAR observes dynamic cross-traffic (pedestrians, forklifts, tuggers) only as sparse, disconnected planar point clusters (e.g., two leg cross-sections or isolated wheel hubs). Lacking visual features, the sensor cannot infer object class, heading angle ($\psi$), or velocity vectors. Standard local costmaps mark these points as static obstacles, triggering abrupt emergency halts, recovery rotations, and severe throughput bottlenecks.
2. **Semantic Blindness ("Stuff" vs. Geometry):** Standard 2D occupancy grids evaluate traversability purely through physical reflection. They cannot differentiate between clear epoxy flooring, slick chemical/water puddles, preferred forklift transit corridors, or temporary staging bays. Mitigating this traditionally requires engineering teams to perform laborious site surveys and manually draw static CAD keepout vectors, a process that is fragile and requires complete re-engineering whenever floor layouts shift.

### 1.2 Proposed Solution: Rapidly Deployable Context Augmentation

Rather than replacing existing, robust 2D LiDAR hardware or attempting to solve general unconstrained navigation, this project introduces a **modular, prompt-distilled visual context and tracking pipeline** designed to retrofit low-cost 2D LiDAR AMRs:

* **Zero-Shot Prompt-to-Edge Distillation:** An offline pipeline ingests raw facility walkthrough video and utilizes large Vision-Language Models (VLMs) and segmentation foundation models to auto-label site-specific hazards and operational rules from text prompts (e.g., `"forklift transit lane"`, `"fluid spill"`). This knowledge is distilled into an edge-optimized instance segmenter running on TensorRT.
* **Metric Planar & Kinetic Augmentation:** The edge model feeds into two deterministic online modules:
1. *Semantic Costmap Filters:* Planar floor masks are mapped via homography into Nav2 Costmap Filters as keepout and speed zones without manual CAD drafting.
2. *Metric Sensor Fusion:* Monocular bounding boxes resolve 2D LiDAR identity fragmentation, while 2D LiDAR range gates resolve monocular scale ambiguity, supplying $(x, y, v_x, v_y, \psi)$ obstacle vectors directly into predictive trajectory control (`nav2_mppi_controller`).



---

## 2. System Architecture & Information Flow

The architecture enforces strict decoupling between high-capacity, zero-shot foundation models (offline/setup) and low-latency, deterministic execution on the edge robot (online runtime).

```
                             OFFLINE / ZERO-SHOT SETUP
  [Walkthrough Video] + [Text Prompts] ──► [VLM / Teacher Model (Florence-2 / SAM)]
                                                            │
                                                            ▼ Auto-Generated Pseudo-Labels
                                               [Distillation & Quantization]
                                                            │
════════════════════════════════════════════════════════════╪═════════════════════════════════
                                   ON-ROBOT RUNTIME         ▼
                                              [TensorRT Edge Model: YOLO-Seg]
                                                            │
                       ┌────────────────────────────────────┴───────────────────────────┐
                       ▼ Dynamic Agent BBoxes                                           ▼ Floor Hazard / Lane Masks
 [RGB Camera] ──► [Extrinsic Calib]                                                     │
                       │                                                                ▼
 [2D LiDAR]   ──► [Ray Gating & Depth Association]                             [Planar Homography (IPM)]
                       │                                                                │
                       ▼ Filtered Metric Clusters                                       ▼ Geometry Polygons
              [Multi-Target CTRV / CV EKF]                                     [Nav2 Costmap Filters]
                       │                                                       (Keepout / Speed Limit Zones)
                       ▼ Dynamic States [x, y, vx, vy, ψ]                               │
              [Nav2 MPPI Dynamic Obstacle Critic]                                       ▼
                       │                                                      [Nav2 Local Costmap]
                       └────────────────────────────────────┬───────────────────────────┘
                                                            ▼
                                                [cmd_vel (Base Actuation)]

```

---

## 3. Core Technical Modules

### Module 1: Prompt-Driven Semantic Context Distillation & Costmap Filtering

* **Objective:** Enable rapid, zero-manual-CAD adaptation to site-specific floor context and non-geometric hazards.
* **Offline Distillation Pipeline:**
* Facility operators record a continuous walkthrough video of the operational area.
* An offline pipeline prompts open-vocabulary foundation models (Florence-2 / Grounded-SAM) with domain-specific labels (e.g., `"forklift lane line"`, `"oil slick"`, `"pallet drop zone"`).
* Auto-generated mask annotations are filtered and distilled into a lightweight edge architecture (YOLOv8-Seg / YOLOv11-Seg) quantized to FP16 via TensorRT.


* **Planar Ground-Plane Projection:**
* Edge segmentation contours are projected onto the ground plane using planar Inverse Perspective Mapping (IPM) derived from the camera intrinsic matrix $K$ and extrinsic pose $[R \mid t]$:

$$\begin{bmatrix} X_w \\ Y_w \\ 1 \end{bmatrix} \sim H^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$


* Projected boundary polygons are converted into the global robot frame via the TF2 transform tree.


* **Nav2 Integration:**
* Polygons are streamed to ROS 2 `nav2_costmap_2d::CostmapFilterInfo` layers, modulating local and global costmaps dynamically as Keepout or Speed Restriction Zones.



### Module 2: Metric LiDAR-Vision Fusion & State Estimation

* **Objective:** Deliver robust metric dynamic obstacle tracking at ranges up to $8\text{ m}$ using existing 2D LiDAR scanners and a low-cost monocular camera.
* **Sensor Association & Depth Anchoring:**
* The camera network outputs 2D bounding boxes and semantic class labels (`Pedestrian`, `Forklift`, `Cart`).
* 2D LiDAR planar range points are mapped to pixel coordinates via camera-laser calibration:

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \left( R \begin{bmatrix} X_{\text{lidar}} \\ Y_{\text{lidar}} \\ 0 \end{bmatrix} + t \right)$$


* Scan points falling outside the horizontal image span $[u_{\min}, u_{\max}]$ of detected dynamic boxes are eliminated.
* Within each bounding frustum, a median cluster distance filter extracts the primary obstacle reflection, eliminating background wall penetration and assigning an exact metric $(X, Y)$ coordinate to the detected agent.


* **Tracking & State Estimation:**
* An Extended Kalman Filter (EKF) tracks each target's state vector:

$$\mathbf{x}_k = [x, y, v_x, v_y, \psi]^T$$


* Constant Turn Rate and Velocity (CTRV) or Constant Velocity (CV) motion models smooth velocity estimates across visual dropouts and occlusions.



### Module 3: Dynamic Critic for Predictive MPPI Control

* **Objective:** Transform reactive emergency halts into proactive speed yielding and evasive path modifications.
* **MPPI Integration:**
* State estimates $(x, y, v_x, v_y, \psi)$ are fed directly to a custom trajectory evaluation critic inside `nav2_mppi_controller`.
* For each sampled trajectory rollout, the critic projects target obstacle positions forward across the preview horizon ($T = 2.0\text{ s}$):

$$\mathbf{x}_{\text{obs}}(t+\tau) = \mathbf{x}_{\text{obs}}(t) + \mathbf{v}_{\text{obs}} \cdot \tau, \quad \tau \in [0, T]$$


* The critic penalizes rollouts that intersect the forward-propagating collision covariance ellipse, driving the optimizer to proactively yield or swerve around crossing traffic while adhering to Nav2 Costmap Filter boundaries.



---

## 4. Hardware & Software Deliverables

### Hardware Specifications

* **Edge Compute:** NVIDIA Jetson Orin Nano (8GB) or Orin NX (or an equivalent x86 mini-PC with an entry-level mobile GPU).
* **Sensors:**
* 1x Low-cost 2D Planar Laser Scanner (e.g., Slamtec RPLiDAR S2/A3 or industrial safety single-layer scanner).
* 1x Global Shutter Monocular USB/MIPI Camera (1080p, $60^\circ\text{–}90^\circ$ horizontal FoV).


* **Mobile Base:** Differential drive or omnidirectional ROS 2 AMR base (TurtleBot4, custom industrial mobile platform, or Gazebo/Isaac Sim simulation model).

### Software Deliverables

1. **`semantic_context_layer` (ROS 2 Package):**
* Real-time TensorRT segmentation node.
* Planar homography projection node converting pixel masks to `geometry_msgs/msg/PolygonStamped`.
* ROS 2 Costmap Filter publisher for dynamic Keepout and Speed Limit zones.


2. **`lidar_vision_tracker` (ROS 2 Package):**
* Target association node filtering LiDAR ranges through visual bounding frustums.
* Multi-target EKF tracking node publishing dynamic agent state arrays.


3. **`nav2_mppi_dynamic_critic`:**
* Custom dynamic obstacle prediction critic plugin for Nav2 MPPI controller.


4. **Offline Distillation Toolkit:**
* Automated CLI scripts for video ingestion, zero-shot VLM prompting, dataset generation, and TensorRT model compilation.



---

## 5. Evaluation Metrics & Experimental Benchmarks

Validation will be conducted across structured simulation environments (Isaac Sim / Gazebo) and verified on physical hardware:

| Benchmark Category | Metric | Baseline (Standard Nav2 + 2D LiDAR) | Target (Proposed System) |
| --- | --- | --- | --- |
| **Dynamic Cross-Traffic** | Robot Recovery Count (Freezes) | High ($>5$ halts per 10 crossing encounters) | **0 freezes** (smooth yield or trajectory deflection) |
| **Mission Efficiency** | Average Route Completion Time | High variance due to sudden emergency halts | **15–25% reduction** in total route duration |
| **Hazard Compliance** | Keepout Zone Infraction Rate | 100% traversal (unaware of un-mapped floor hazards) | **0% traversal** through detected hazard polygons |
| **Setup & Adaptation** | New Zone Deployment Time | Hours/days (manual CAD drafting & site re-tuning) | **$<30$ minutes** (walkthrough video + text prompting) |
| **Edge Compute** | Real-Time Execution Frame Rate | N/A | **$\ge 25\text{ FPS}$** sustained on edge hardware |
| **State Estimation** | Velocity Vector RMSE | N/A (static costmap) | **$< 0.15\text{ m/s}$** linear velocity error |

---

## 6. Strategic Scope & Methodological Boundaries

* **Decoupling Foundation Models from the Safety Loop:** Running heavy VLMs (e.g., full SAM or multimodal LLMs) directly on an AMR edge computer introduces unacceptable latency ($>500\text{ ms}$). Limiting foundation models to an offline pseudo-labeling role preserves deterministic sub-30ms control loops on the physical robot.
* **Mutual Sensor Augmentation over Standalone Perception:** Pure monocular visual depth suffers from scale drift and optical noise, while 2D LiDAR suffers from identity loss and semantic blindness. Pairing them as mutual anchors (vision provides identity and angle; 2D LiDAR provides ground-truth metric scale) achieves high-fidelity dynamic tracking at minimal sensor cost.
* **Planar Costmap Filters vs. 3D Voxel Reconstruction:** Industrial warehouse floors are predominantly planar surfaces. Projecting segmented visual boundaries directly into 2D Costmap Filters via homography eliminates the high compute and memory overhead of 3D voxel back-projection, maintaining high frame rates on constrained edge compute.