# 1. Executive Summary & Problem Statement

**Project Title:** A Rapid-Deployment Visual Context and Dynamic Tracking Pipeline for Cost-Constrained AMRs in Brownfield Logistics  
**Target Domain:** Brownfield Industrial Logistics, Warehouse Automation, Low-Cost Autonomous Mobile Robots (AMRs)  
**Core Stack:** ROS 2 (Jazzy + Gazebo Harmonic), Nav2 (`nav2_mppi_controller`, Costmap Filters), TensorRT, 2D Planar LiDAR, Monocular RGB Camera, Offline Foundation Models (Florence-2 / Grounded-SAM)

---

## 1.1 The Brownfield Deployment Bottleneck

In brownfield industrial environments (legacy manufacturing plants and mid-tier distribution centers), Autonomous Mobile Robots (AMRs) must operate alongside human foot traffic and manual material handling equipment without the benefit of facility redesigns. To remain economically viable, these platforms avoid multi-thousand-dollar 3D LiDAR arrays and instead rely on single-plane 2D safety LiDARs paired with classical 2D occupancy grids (Nav2 costmaps).

While 2D LiDAR SLAM and static localization (e.g., AMCL, Cartographer) are mature, this architecture exhibits severe operational bottlenecks when deployed in active brownfield environments:

1. **Dynamic Deadlock ("Freezing Robot Problem"):**
   - 2D LiDAR observes dynamic cross-traffic (pedestrians, forklifts, tuggers) only as sparse, disconnected planar point clusters (e.g., two leg cross-sections or isolated wheel hubs).
   - Lacking visual features, the sensor cannot infer object class, heading angle ($\psi$), or velocity vectors.
   - Standard local costmaps mark these points as static obstacles, triggering abrupt emergency halts, recovery rotations, and severe throughput bottlenecks.
2. **Semantic Blindness ("Stuff" vs. Geometry):**
   - Standard 2D occupancy grids evaluate traversability purely through physical reflection.
   - They cannot differentiate between clear epoxy flooring, slick chemical/water puddles, preferred forklift transit corridors, or temporary staging bays.
   - Mitigating this traditionally requires engineering teams to perform laborious site surveys and manually draw static CAD keepout vectors, a process that is fragile and requires complete re-engineering whenever floor layouts shift.

---

## 1.2 Proposed Solution: Rapidly Deployable Context Augmentation

Rather than replacing existing, robust 2D LiDAR hardware or attempting to solve general unconstrained navigation, this project introduces a **modular, prompt-distilled visual context and tracking pipeline** designed to retrofit low-cost 2D LiDAR AMRs:

* **Zero-Shot Prompt-to-Edge Distillation:**
  - An offline pipeline ingests raw facility walkthrough video and utilizes large Vision-Language Models (VLMs) and segmentation foundation models to auto-label site-specific hazards and operational rules from text prompts (e.g., `"forklift transit lane"`, `"fluid spill"`).
  - This knowledge is distilled into an edge-optimized instance segmenter running on TensorRT.
* **Metric Planar & Kinetic Augmentation:** The edge model feeds into two deterministic online modules:
  1. *Semantic Costmap Filters:* Planar floor masks are mapped via homography into Nav2 Costmap Filters as keepout and speed zones without manual CAD drafting.
  2. *Metric Sensor Fusion:* Monocular bounding boxes resolve 2D LiDAR identity fragmentation, while 2D LiDAR range gates resolve monocular scale ambiguity, supplying $(x, y, v_x, v_y, \psi)$ obstacle vectors directly into predictive trajectory control (`nav2_mppi_controller`).
