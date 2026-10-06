# Engineering Project Proposal

**Project Title:** Multi-Modal Vision & 2D LiDAR Fusion for Predictive Dynamic Navigation and Semantic Context Awareness in Low-Cost AMRs

**Target Domain:** Brownfield Industrial Logistics, Warehouse Automation, Autonomous Mobile Robots (AMRs)

**Core Stack:** ROS 2 (Humble/Iron), Nav2 (`nav2_mppi_controller`, Costmap Filters), TensorRT, 2D Planar LiDAR, Monocular RGB Camera

---

## 1. Executive Summary & Problem Statement

### 1.1 The Industry Bottleneck

Brownfield industrial environments (manufacturing floors, mid-tier warehousing) in regions like Southeast Asia rely heavily on cost-effective Autonomous Mobile Robots (AMRs). To remain economically viable, these platforms avoid multi-thousand-dollar 3D LiDAR pucks and rely on single-plane 2D safety LiDARs combined with classical 2D occupancy grids (Nav2 costmaps).

This sensor setup exhibits two structural operational failures:

1. **Dynamic Deadlock ("Freezing Robot Problem"):** 2D LiDAR observes cross-traffic agents (pedestrians, forklifts, tuggers) only as flat, disconnected 2D point clusters (e.g., two leg slices or wheel hubs). It has zero perception of target orientation, heading, or velocity. When an agent crosses its trajectory, the robot fails to anticipate the crossing path, halts abruptly, enters recovery spins, and degrades throughput.
2. **Semantic Blindness ("Stuff" vs. Geometry):** Standard occupancy grids are purely geometric. They cannot differentiate between clear traversable epoxy flooring, slick chemical/water puddles, preferred forklift transit lanes, or temporary staging zones. Traditional methods require expensive manual CAD drawing of virtual zones that break whenever facility layouts shift.

### 1.2 Proposed Solution

This project develops a hybrid, edge-viable navigation framework integrating:

* **Dynamic Obstacle State Estimation:** Fusing 2D LiDAR range clusters with RGB monocular tracking to extract metric dynamic states ($x, y, v_x, v_y, \psi$) fed directly into predictive local path tracking (`nav2_mppi_controller`).
* **Semantic Context Layering:** Auto-distilling vision-language foundation models into an ultra-lean edge instance segmenter to project traversable lane boundaries and hazard keepouts into Nav2 Costmap Filters without manual CAD labeling.

---

## 2. System Architecture & Information Flow

The proposed system enforces strict decoupling: heavy foundation models operate offline/asynchronously for zero-shot adaptation, while low-latency deterministic pipelines operate on the edge robot.

```
                            OFFLINE / ZERO-SHOT SETUP
  [Walkthrough Video] ──> [Cloud/Workstation VLM (SAM/Florence)] ──> [Auto-Distilled Edge Weights]
                                                                                │
════════════════════════════════════════════════════════════════════════════════╪═════════════════
                                   ON-ROBOT RUNTIME                             │
                                                                                ▼
 [Monocular RGB Camera] ───────────────────────────► [Edge Model: YOLO-Seg / ByteTrack]
           │                                                │                    │
           │ Extrinsic Camera-LiDAR Calibration             │ Static Polygons    │ Dynamic BBoxes
           ▼                                                ▼                    ▼
   [2D Planar LiDAR] ─────────────────────────────► [Sensor Fusion & EKF]        │
           │                                                │                    │
           │                                                ▼ Dynamic States     │
           │                                           [x, y, vx, vy]            │
           ▼                                                │                    │
   [Nav2 Static Map]                                        ▼                    ▼
           │                                   [Nav2 MPPI Controller]   [Nav2 Costmap Filters]
           │                                    (Predictive Dynamic      (Keepout / Speed Zones)
           │                                     Obstacle Avoidance)             │
           ▼                                                │                    │
     [Nav2 Costmap] ◄───────────────────────────────────────┴────────────────────┘
           │
           ▼
     [cmd_vel (Base Actuation)]

```

---

## 3. Core Technical Modules

### Module 1: Semantic Context & Hazard Segmentation (Direction A Grounded)

* **Objective:** Detect floor-level operational context ("stuff" approximated via boundary polygons: forklift lanes, puddles, exclusion zones) and feed them to Nav2.
* **Offline Distillation Pipeline:**
* Ingest site walkthrough video into open-vocabulary foundation models (e.g., Grounded-SAM / Florence-2) with text prompts: `"forklift lane line"`, `"liquid spill on floor"`, `"staging pallet zone"`.
* Auto-generate pseudo-ground-truth bounding polygons and distill down into a lightweight edge checkpoint (e.g., YOLOv8-Seg/YOLOv11-Seg) running on TensorRT FP16.


* **Ground-Plane Projection:**
* For detected planar polygons, apply planar Inverse Perspective Mapping (IPM) using known camera extrinsics $[R \mid t]$ and floor homography:

$$\begin{bmatrix} X_w \\ Y_w \\ 1 \end{bmatrix} \sim H^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$


* Transform projected coordinates into the robot’s `map` frame using the TF2 tree.


* **Nav2 Costmap Integration:**
* Stream polygon contours directly to a custom ROS 2 node publishing to `nav2_costmap_2d::CostmapFilterInfo` or dynamic Keepout Zones, modulating cost values without modifying underlying static occupancy maps.



### Module 2: 2D LiDAR + Monocular Vision Sensor Fusion (Direction C Grounded)

* **Objective:** Track dynamic agents at range ($>8\text{ m}$) with real-world metric velocity vectors, eliminating monocular scale ambiguity and 2D LiDAR identity fragmentation.
* **Sensor Association:**
* The RGB detector outputs dynamic agent 2D bounding boxes and class IDs (Pedestrian, Forklift).
* Project planar 2D LiDAR scan points into the camera image plane using camera intrinsic matrix $K$ and extrinsic calibration matrix $[R \mid t]$:

$$\lambda \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \left( R \begin{bmatrix} X_{\text{lidar}} \\ Y_{\text{lidar}} \\ 0 \end{bmatrix} + t \right)$$


* Filter LiDAR points falling within the horizontal bounds $[u_{\min}, u_{\max}]$ of the detected bounding box.
* Extract the metric depth via median cluster distance, establishing an exact $(X, Y)$ coordinate in the robot frame.


* **State Estimation:**
* An Extended Kalman Filter (EKF) tracks the state vector for each agent:

$$\mathbf{x}_k = [x, y, v_x, v_y, \psi]^T$$


* Constant Turn Rate and Velocity (CTRV) or Constant Velocity (CV) motion models propagate states across temporal dropouts, maintaining smooth velocity estimates.



### Module 3: Predictive Local Trajectory Control

* **Objective:** Enable proactive evasive maneuvers instead of reactive e-stops.
* **Nav2 MPPI Configuration:**
* Integrate the tracked dynamic states into the Model Predictive Path Integral (`nav2_mppi_controller`) critic pipeline.
* Rather than checking collisions against a static footprint, project the obstacle’s predicted trajectory covariance forward across the optimization horizon ($T = 2.0\text{ s}$):

$$\mathbf{x}_{\text{obs}}(t+\tau) = \mathbf{x}_{\text{obs}}(t) + \mathbf{v}_{\text{obs}} \cdot \tau, \quad \tau \in [0, T]$$


* Penalize trajectory rollouts that intersect the expanding collision ellipse, allowing the AMR to smoothly alter heading or yield early.



---

## 4. Hardware & Software Deliverables

### Hardware Requirements

* **Compute:** NVIDIA Jetson Orin Nano (8GB) or Orin NX (or x86 mini-PC with discrete mobile GPU).
* **Sensors:**
* 1x Low-cost 2D Planar Laser Scanner (e.g., Slamtec RPLiDAR S2/A3 or industrial safety single-layer equivalent).
* 1x Global Shutter Monocular USB/MIPI RGB Camera ($1080\text{p}$, $60\text{–}90^\circ$ FOV).


* **Mobile Platform:** Any differential drive or omnidirectional ROS 2 AMR base (TurtleBot4, custom base, or Isaac Sim / Gazebo simulation model).

### Software Deliverables

1. **`semantic_context_layer` (ROS 2 Package):**
* Real-time TensorRT polygon inference node.
* Planar homography projection node converting pixel masks to `geometry_msgs/msg/PolygonStamped`.
* Dynamic Keepout Zone costmap publisher.


2. **`lidar_vision_tracker` (ROS 2 Package):**
* Camera-LiDAR extrinsic calibration utility.
* Frustum-based point-to-box association node.
* Multi-target EKF tracker publishing `nav_msgs/msg/Path` or obstacle state arrays.


3. **`nav2_mppi_dynamic_critic`:**
* Custom MPPI trajectory critic evaluating dynamic obstacle intercept penalties.


4. **Offline Distillation Toolkit:**
* Python scripts to ingest site footage, run open-vocabulary prompts (VLM/SAM), auto-annotate, and export quantized ONNX/TensorRT engines.



---

## 5. Evaluation Metrics & Experimental Benchmarks

The project will be evaluated under controlled factory simulation scenarios (Gazebo / Isaac Sim) and validated on hardware:

| Benchmark Category | Metric | Baseline (Standard Nav2 + 2D LiDAR) | Target (Proposed System) |
| --- | --- | --- | --- |
| **Dynamic Cross-Traffic** | Robot Recovery Count (Freezes) | High ($>5$ per 10 runs during crossing) | **Zero freezes** (proactive yield/swerve) |
| **Mission Efficiency** | Average Travel Time per Route | Extended due to sudden halts | **15–25% reduction** in travel duration |
| **Hazard Compliance** | Keepout Zone Infraction Rate | 100% traversal (unaware of puddles/lines) | **0% traversal** through detected hazard polygons |
| **Edge Compute** | Sensor Pipeline Frame Rate | N/A | **$\ge 25\text{ FPS}$** stable on Jetson hardware |
| **Tracking Accuracy** | Velocity Estimation Error (RMSE) | N/A (static costmap) | **$< 0.15\text{ m/s}$** velocity error |

---

## 6. Strategic Scope & Clarifications (Read-Back Notes)

* **Why STAD is decoupled:** Spatio-Temporal Action Detection classifies human verbs at the micro-level. It is mathematically disconnected from local obstacle avoidance and belongs in fixed ceiling CCTV / fleet-level orchestration. It is excluded from the on-robot real-time safety loop.
* **Why Pure Monocular Depth was rejected:** Without a metric anchor, monocular velocity tracking suffers from scale drift and optical-flow noise. 2D LiDAR supplies exact physical distance; vision supplies identification and orientation.
* **Why Costmap Filters over 3D Voxel Back-Projection:** In industrial indoor logistics, floors are planar. Converting instance polygons directly to 2D costmap keepout zones bypasses high-dimensional voxel projection and spatial hashing, maintaining sub-15ms processing latency on low-power edge hardware.