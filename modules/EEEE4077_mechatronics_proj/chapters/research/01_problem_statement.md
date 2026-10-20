# 1. Executive Summary & Problem Statement

**Project Title:** Vision-Augmented Mobile Robot Navigation in Dynamic Environments  
**Project Code:** SD-MEng-26-01 | **Supervisor:** Dr Shalini Darmaraju | **Moderator:** Ir Dr Daniel Pu  
**Target Domain:** Indoor Logistics, Warehouse Automation, Low-Cost Autonomous Mobile Robots (AMRs)  
**Core Stack:** ROS 2 (Jazzy + Gazebo Harmonic), Nav2 (`nav2_mppi_controller`), 2D Planar LiDAR, Monocular RGB Camera, ByteTrack MOT, Linear Kalman Filter

---

## 1.1 The Brownfield Deployment Bottleneck

In brownfield industrial environments (legacy manufacturing plants and mid-tier distribution centers), Autonomous Mobile Robots (AMRs) must operate alongside human foot traffic and manual material handling equipment without the benefit of facility redesigns. To remain economically viable, these platforms avoid multi-thousand-dollar 3D LiDAR arrays and instead rely on single-plane 2D safety LiDARs paired with classical 2D occupancy grids (Nav2 costmaps).

While 2D LiDAR SLAM and static localization (e.g., AMCL, Cartographer) are mature, this architecture exhibits severe operational bottlenecks when deployed in active brownfield environments:

1. **Dynamic Deadlock ("Freezing Robot Problem"):**
   - 2D LiDAR observes dynamic cross-traffic (pedestrians, forklifts, tuggers) only as sparse, disconnected planar point clusters (e.g., two leg cross-sections or isolated wheel hubs).
   - Lacking visual features, the sensor cannot infer object class, heading angle ($\psi$), or velocity vectors.
   - Standard local costmaps mark these points as static obstacles, triggering abrupt emergency halts, recovery rotations, and severe throughput bottlenecks.
2. **Semantic Blindness to Non-Geometric Surface Hazards ($Z = 0$):**
   - Standard 2D and 3D occupancy grids evaluate traversability purely through physical laser reflection and geometric height ($Z \ne 0$).
   - They are physically incapable of detecting flat surface hazards where elevation is zero ($Z \approx 0$), such as slick chemical/oil spills, standing water puddles, or painted transit lanes. Laser pulses either disperse via specular reflection (treating the slick as traversable free space) or return flat ground reflections, risking dangerous hydroplaning, traction loss, and wheel odometry corruption.
   - While static structural boundaries (walls, permanent machinery) are best handled via deterministic CAD keepout vectors, static CAD maps cannot anticipate transient, unplanned fluid leaks or temporary floor demarcations that arise during active operational shifts.

---

## 1.2 Proposed Solution: Rapidly Deployable Context Augmentation

Rather than replacing existing, robust 2D LiDAR hardware or attempting to replace certified static CAD maps with unverified neural networks, this project introduces a **modular, prompt-distilled visual context and tracking pipeline** designed to retrofit low-cost 2D LiDAR AMRs:

* **Zero-Annotation Prompt-to-Edge Distillation:**
   - An offline pipeline ingests facility walkthrough video and utilizes large Vision-Language Models (VLMs) and segmentation foundation models to auto-label site-specific non-geometric hazards and visual rules from text prompts (e.g., `"fluid spill"`, `"forklift transit lane"`).
   - This knowledge is distilled into an edge-optimized instance segmenter running on TensorRT, eliminating the need for expensive manual bounding-box annotation.
* **Metric Planar & Kinetic Augmentation:** The edge model feeds into two deterministic online modules:
   1. *Semantic Surface Costmap Filters:* Planar floor masks for transient surface hazards and visual lanes are mapped via Inverse Perspective Mapping (IPM) into Nav2 Costmap Filters as dynamic keepout and speed zones, complementing permanent CAD vector maps.
   2. *Metric Sensor Fusion:* Monocular bounding boxes resolve 2D LiDAR identity fragmentation, while 2D LiDAR range gates resolve monocular scale ambiguity, supplying $(x, y, v_x, v_y, \psi)$ obstacle vectors directly into predictive trajectory control (`nav2_mppi_controller`).
