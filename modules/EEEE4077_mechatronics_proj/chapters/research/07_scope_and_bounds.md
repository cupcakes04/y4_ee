# 7. Strategic Scope & Methodological Boundaries

This chapter defines the methodological principles governing the system design and formalizes explicit non-goals (out-of-scope boundaries) to maintain engineering rigor and project feasibility within the 450-hour dissertation allocation.

---

## 7.1 Methodological Principles

1. **Decoupled Visual Association and Metric State Estimation:**
   - Solving multi-object tracking in 2D image coordinates via ByteTrack leverages dense visual textures and spatial IoU overlap, bypassing fragile 3D point cloud clustering and combinatorial geometric data association.
   - Projecting planar 2D LiDAR rays into established image bounding frustums grounds each track in millimeter-accurate metric distance, eliminating monocular scale ambiguity at negligible computational overhead.
2. **Analytical Kinematic Extrapolation vs. Heavy Neural Forecasters:**
   - Deep neural trajectory prediction networks (e.g., social transformers, diffusion-based path generators) require substantial GPU memory and introduce variable latencies ($50\text{--}200\text{ ms}$) unsuitable for deterministic edge safety loops.
   - For typical AMR lookahead horizons ($T \le 2.0\text{ s}$), analytical constant-velocity extrapolation evaluated within a linear Kalman filter provides sufficient accuracy ($<0.15\text{ m/s}$ RMSE) while executing in $<0.2\text{ ms}$ on CPU, guaranteeing deterministic $30\text{--}50\text{ Hz}$ control cycles.
3. **Nav2 `pluginlib` Critic Integration vs. Static Costmap Pollution:**
   - Standard 2D costmaps (`nav2_costmap_2d`) represent spatial occupancy at time $t = 0$. Marking dynamic agents as occupied cells creates artificial static obstacles that cause the robot to freeze.
   - Processing dynamic obstacles directly inside a custom MPPI trajectory critic preserves the costmap for static infrastructure while allowing trajectory rollouts to evaluate spatio-temporal risk conditioned on lookahead arrival time $\tau$.
4. **Empirical Isolation via 3-Way Ablation:**
   - To provide defensible scientific insight rather than monolithic benchmark scores, the system systematically decouples the contribution of visual object detection (C1) from predictive temporal motion modeling (C2) relative to baseline Nav2 (C0).

---

## 7.2 Explicit Non-Goals (Out of Scope)

To ensure high technical depth, robust verification, and on-time delivery, the following areas are strictly out of scope:

1. **Fleet Management & Multi-Robot Coordination:**
   The project investigates single-robot local navigation in dynamic environments. Centralized fleet management (e.g., Open-RMF) and inter-robot negotiation protocols are excluded.
2. **Novel SLAM or Global Path Planning Research:**
   Global map generation and robot localization utilize standard, verified ROS 2 tools (Cartographer / Nav2 AMCL). Global path planning relies on the standard `nav2_navfn_planner` or `SmacPlanner2D`.
3. **Long-Horizon Social Intention & Game-Theoretic Modeling:**
   Obstacle motion prediction is restricted to short-term kinematic lookahead horizons ($\tau \le 2.0\text{ s}$). Multi-agent game theory, psychological social compliance modeling, and complex intent inferencing are out of scope.
4. **Physical Hardware Procurement & Real-World Lab Deployment:**
   In accordance with supervisor specification `SD-MEng-26-01` (HW 0% / SW 60% / Research 40%), all physical hardware procurement, fabrication, and real-world laboratory deployment are strictly excluded. All development, testing, and comparative benchmarking are 100% committed to high-fidelity software simulation in Gazebo Harmonic.
5. **Full 3D Volumetric Scene Reconstruction:**
   The system deliberately eschews computationally expensive 3D voxel grids, octrees, and dense TSDF reconstructions, maintaining a lean planar perception and control architecture.
6. **Formal Industrial Safety Certification:**
   The project is an experimental engineering investigation. The robot's primary hardware emergency stop (E-stop) and low-level laser safety zone interlocks remain untouched and out of scope.
7. **Offline VLM Floor-Hazard Distillation & Surface Semantics:**
   Offline foundation model prompt-distillation (`avp`) and ground-plane homography (IPM) for non-geometric fluid spills ($Z \approx 0$) are parked in `chapters/explore/` and strictly excluded from the assessed engineering deliverables.
