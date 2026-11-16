# 1. Executive Summary & Problem Statement

**Project Title:** Vision-Augmented Mobile Robot Navigation in Dynamic Environments  
**Project Code:** SD-MEng-26-01 | **Supervisor:** Dr Shalini Darmaraju | **Moderator:** Ir Dr Daniel Pu  
**Target Domain:** Indoor Logistics, Warehouse Automation, Low-Cost Autonomous Mobile Robots (AMRs)  
**Core Stack:** ROS 2 (Jazzy + Gazebo Harmonic), Nav2 (`nav2_mppi_controller`), 2D Planar LiDAR, Monocular RGB Camera, ByteTrack MOT, Linear Kalman Filter  

---

## 1.1 The Operational Bottleneck in Shared Environments

In modern industrial plants, mid-tier warehouses, and shared indoor facilities, Autonomous Mobile Robots (AMRs) must navigate alongside moving human workers and manual material handling equipment (forklifts, pallet jacks). To remain economically viable and maintain certified functional safety (ISO 3691-4 / SIL-2), commercial AMR platforms rely primarily on single-plane 2D safety laser scanners paired with classical 2D occupancy grids (Nav2 costmaps).

While 2D LiDAR SLAM and static navigation (e.g., AMCL, Cartographer) are mature, this standard architecture suffers from a fundamental operational failure mode in dynamic environments:

1. **The "Freezing Robot Problem" (Trautman & Krause, 2010):**
   - A planar 2D LiDAR scans in a single thin horizontal plane (10–20 cm above the floor). It observes a walking human or crossing vehicle only as sparse, disconnected point clusters (e.g., two leg cross-sections).
   - The sensor has zero visual feature context: it cannot infer object semantic class, orientation, or motion vectors.
   - Standard 2D costmaps (`nav2_costmap_2d`) represent the world as a static, time-invariant grid ($t = 0$), marking dynamic obstacles as stationary brick walls.
   - As a result, when an obstacle enters or crosses the robot's corridor, local trajectory planners (DWB, TEB, or default MPPI) detect an instantaneous obstruction and execute emergency stops, conservative waiting, or erratic recovery spins. The robot frequently freezes, causing severe operational throughput bottlenecks even though the crossing agent will have cleared the corridor seconds before the robot arrives.

2. **The Limitation of Costmap-Only Obstacle Integration:**
   - Standard attempts to address dynamic obstacles by projecting camera or depth sensor data directly into the local costmap (e.g., via `VoxelLayer` or `spatio_temporal_voxel_layer`) actually worsen the freezing behavior.
   - Because costmaps discard target identity and lack velocity storage fields, marking moving humans as occupied costmap cells creates persistent phantom obstacles that linger due to raycasting decay latencies, paralyzing the robot in dense cross-traffic.

---

## 1.2 Proposed Solution: Multi-Modal Tracking & Predictive Trajectory Planning

Rather than attempting to replace proven 2D LiDAR safety hardware or relying on computationally prohibitive multi-camera 3D voxel grids, this project develops a **modular, vision-augmented predictive navigation framework** integrated natively into ROS 2 Nav2:

1. **Multi-Modal Late-Fusion State Estimation (Module 1):**
   - A forward-facing monocular RGB camera detects dynamic agents (pedestrians, vehicles) using a lightweight edge detector (YOLO) and tracks them in image space using **ByteTrack**, maintaining persistent target identities across visual occlusions.
   - Planar 2D LiDAR range points are projected into visual bounding frustums via camera-laser extrinsic calibration, extracting millimeter-accurate Time-of-Flight metric distances without stereo disparity noise.
   - A per-track **Linear Kalman Filter** estimates smooth, decoupled metric obstacle states:
     $$\mathbf{x} = [x, y, v_x, v_y]^T$$

2. **Predictive Dynamic MPPI Control (Module 2):**
   - Tracked dynamic obstacle state vectors are consumed by a bespoke C++ **Dynamic Obstacle Critic plugin** inside `nav2_mppi_controller`.
   - The critic forward-projects obstacle positions across the MPPI preview horizon ($T = 2.0\text{ s}$):
     $$\mathbf{p}_{\text{obs}}(t + \tau) = \mathbf{p}_{\text{obs}}(t) + \mathbf{v}_{\text{obs}} \cdot \tau$$
   - This drives the MPPI optimizer to proactively yield, decelerate, or deflect around crossing agents without freezing, while preserving standard Nav2 safety costmap constraints.

3. **Systematic 3-Way Comparative Ablation Benchmark (Module 3):**
   - An automated simulation benchmark in Gazebo Harmonic evaluates the framework against range-sensor-based navigation across varying obstacle speeds ($0.5–2.0\text{ m/s}$), crossing trajectories, and crowd densities ($1–4$ dynamic agents).
   - Statistically distinguishes the isolated contributions of (a) visual identification versus (b) motion prediction in reducing robot freezing and travel delays.
