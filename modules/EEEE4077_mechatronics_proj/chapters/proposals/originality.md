# Originality & Positioning

> **Purpose**: Prepared for supervisor review, Project Planning Report (§4), and final thesis positioning. Grounded in the technical reality documented in `chapters/research/08_design_tradeoffs_and_alternatives.md`.

---

## 1. Dimensions of Originality & Concrete Contributions

The project's originality lies in **translational systems engineering, open-source architectural extension, and rigorous empirical benchmarking**, rather than claiming speculative deep-learning cognitive architectures or ungrounded control formulations:

1. **Idiomatic Open-Source Architectural Extension:**
   - Shipped versions of ROS 2 Nav2 (`nav2_mppi_controller`) evaluate trajectory rollouts strictly against static 2D costmaps (`nav2_costmap_2d` at $t=0$).
   - This project develops and open-sources a native C++ `pluginlib` dynamic obstacle critic (`DynamicObstaclesCriticPlugin`) that projects dynamic obstacle positions forward across candidate rollout horizons ($\mathbf{p}_{\text{obs}}(\tau) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}}\tau$), resolving the "freezing robot" problem without modifying Nav2 core internals.
2. **Brownfield Multi-Modal Sensor Complementarity:**
   - Instead of replacing brownfield 2D LiDARs with cost-prohibitive 3D LiDAR arrays ($>\$3,000$) or heavy stereo depth cameras that degrade quadratically at $>4\text{ m}$, the system retrofits an existing 2D LiDAR with a low-cost monocular RGB camera ($\approx \$450$ total suite).
   - It decouples data association (solved in 2D image space via ByteTrack) from metric depth anchoring (solved via extrinsic frustum ray gating) and state filtering (linear Kalman Filter), avoiding fragile geometric clustering on sparse laser returns while eliminating monocular scale drift.
3. **Empirical Decoupling via 3-Way Comparative Ablation:**
   - In direct fulfillment of the supervisor brief (`SD-MEng-26-01`), the project designs and executes a systematic 3-way comparative ablation benchmark:
     - **C0:** 2D LiDAR baseline with static costmap.
     - **C1:** 2D LiDAR + Camera visual detection without motion prediction ($t=0$ clearance circle).
     - **C2:** Full predictive MPPI with velocity forward projection over lookahead horizon $\tau \in [0, 2.0]\text{ s}$.
   - This isolates whether visual bounding alone prevents freezing, or whether temporal motion prediction is the essential mechanism.
4. **Differentiation from Modern SOTA MPPI Variations:**
   - While recent high-end research introduces heavy GPU-accelerated MPPI pipelines (e.g. continuous signed-distance functions in `EXACT-MPPI` [L16] or rollout clustering in `CSC-MPPI` [L17]) or analytical post-filters (`SE-MPPI` [L15]), this project identifies and occupies the **brownfield AMR sweet spot**: an ultra-lean C++ SIMD plugin running on standard onboard CPUs in $<0.3\text{ ms}$, where dynamic velocity vectors naturally break trajectory symmetry without requiring heavy GPU clustering or external QP solvers.

---

## 2. Reverse-Engineered Literature Review & Gap Taxonomy

To ground the project's engineering contributions in rigorous academic scholarship, the design choices are reverse-engineered from current industrial baselines and recent state-of-the-art literature. The table below structures this justification as an **inverted pyramid**: narrowing from the macro commercial imperative down to the micro-algorithmic implementation and empirical validation.

| Pyramid Level | Subsystem / Focus | Baseline Practice & Canonical Foundations | Failure Mode & Root Cause (**Where & Why**) | Academic SOTA Counterparts & Trade-offs (**How**) | **Unoccupied Gap & Justification for Project Goal** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Level 1: Macro Context** | **Brownfield Logistics AMR Deployment** | Single-plane 2D LiDAR + 2D Costmap stacks (`nav2_costmap_2d`) [Macenski et al., 2020 (L2), 2023 (L3)]. | **Where:** Dense warehousing and mixed manufacturing plants [IFR, 2025 (L9)].<br>**Why:** Replacing deployed fleets with \$3k–\$10k 3D LiDAR arrays or heavy stereo rigs is commercially prohibitive for brownfield facilities. | Multi-beam 3D LiDAR point cloud processing or multi-camera RGB-D depth networks. | **Retrofit Imperative:** Add low-cost monocular vision (\$30–\$50) to existing 2D LiDAR to deliver semantic and dynamic capabilities under a strictly constrained budget ($<\$480$ total). |
| **Level 2: Phenomenon** | **The Freezing Robot Problem** | Occupancy grid mapping & reactive 2D obstacle avoidance [Trautman & Krause, 2010 (L1)]. | **Where:** Dynamic corridors with crossing pedestrians or manual pushcarts.<br>**Why:** Standard 2D costmaps model moving humans as static obstacle cells at $t=0$. Local planners detect imminent path invalidation and trigger emergency stops or oscillating recovery rotations. | Social Force Models (SFM) [Helbing & Molnar, 1995 (L14)] and Interactive Gaussian Processes (IGP) [Trautman, 2010 (L1)]. | **Decoupled Architecture:** Static infrastructure is retained in the 2D occupancy grid; moving agents are extracted into metric state space $[x, y, v_x, v_y]^T$ for forward temporal evaluation, eliminating costmap raycasting clearing latency and phantom trails. |
| **Level 3a: Perception** | **Metric Dynamic Tracking** | Planar laser clustering (Euclidean / DBSCAN) vs. Monocular depth estimation. | **Where:** Intersecting human lower limbs in planar scan plane.<br>**Why:** 2D LiDAR returns are sparse, fragmented cross-sections lacking visual identity; monocular depth suffers from scale ambiguity; stereo depth degrades quadratically beyond 4 m ($O(Z^2)$). | Heavy 3D bounding box detection on dense point clouds (PointPillars, VoxelNet) or monocular metric depth networks (depth-anything) requiring high-end edge GPUs. | **Complementary Late-Fusion:** Exploit ByteTrack [Zhang et al., 2022 (L13)] in 2D image space for identity persistence across occlusions, Zhang-Pless [2004 (L5)] planar frustum projection for metric depth, and a per-track Linear Kalman Filter [Thrun et al., 2005 (L12)] on CPU. |
| **Level 3b: Local Planning** | **Predictive Trajectory Optimization** | Nav2 MPPI Controller [Williams et al., 2017 (L4); Macenski et al., 2023 (L11)]. | **Where:** Dynamic crossing interactions over lookahead horizon $\tau \in [0.5, 2.0]\text{ s}$.<br>**Why:** All 11 shipped Nav2 MPPI critics evaluate trajectories against static costmaps ($t=0$). The optimizer cannot evaluate where an obstacle will be 1–2 s ahead, causing either premature halts or blind path intersections. | • **SE-MPPI** [Kang, 2024 (L15)]: QP Control Barrier Function safety post-filter.<br>• **EXACT-MPPI** [Peng et al., 2024 (L16)]: JAX CUDA exact signed-distance fields.<br>• **CSC-MPPI** [RCILab, 2025 (L17)]: cuML DBSCAN rollout clustering. | **Native Nav2 C++ Dynamic Critic:** Implement a lightweight `pluginlib` critic evaluating dynamic trajectories directly within MPPI rollouts ($\mathbf{p}_{\text{obs}}(\tau) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}}\tau$). Retains full Nav2 architecture, executes in $<0.3\text{ ms}$ on CPU via SIMD vectorization, and breaks path symmetry naturally via dynamic velocity vectors. |
| **Level 4: Evaluation** | **Benchmarking & Validation** | Ad-hoc simulation demonstrations reporting monolithic success rate or time-to-goal. | **Where:** Evaluating dynamic obstacle avoidance frameworks.<br>**Why:** Monolithic benchmarks cannot isolate whether improved navigation stems from visual bounding clearance or true temporal motion prediction. | End-to-end black-box metric reporting against legacy DWB or TEB planners without modular ablation. | **Systematic 3-Way Comparative Ablation:** Isolate detection from prediction across standardized scenarios (A–E) comparing **C0** (2D LiDAR baseline), **C1** (Vision detection without prediction, $t=0$), and **C2** (Full predictive MPPI), directly fulfilling the supervisor brief (`SD-MEng-26-01`). |

---

## 3. Comparison with Current Practice & Academic Frontiers

| Capability | Current Industrial Practice | Academic Research SOTA (GPU / SOTA MPPI) | This FYP Project (Brownfield Retrofit) |
|---|---|---|---|
| **Dynamic Obstacle Handling** | Emergency stop / recovery rotate (freezing) | Heavy neural transformers or GPU JAX/cuML rollouts (EXACT-MPPI [L16], CSC-MPPI [L17]) | 2D LiDAR + camera frustum KF → Native Nav2 C++ MPPI dynamic critic plugin |
| **Local Planning Costmap** | Static 2D costmap ($t=0$); dynamic agents treated as walls | Continuous SDF fields or 3D spatio-temporal voxel grids | Decoupled: static costmap for fixed infrastructure + dynamic critic for moving agents |
| **Safety / Yielding Mechanism** | Passive safety zone E-stop | QP Control Barrier Function post-filter on $\mathbf{u}_0^*$ (SE-MPPI [L15]) | Proactive spatio-temporal cost shaping over preview horizon $\tau \in [0, 2.0]\text{ s}$ |
| **Sensor Hardware Cost** | \$400 (2D LiDAR only) | \$4,000–\$10,000 (3D LiDAR + Depth camera rigs) | **\$430–\$480** (2D LiDAR + monocular camera retrofit) |
| **Compute Envelope** | Low-power x86 / ARM CPU | High-end workstation / dedicated edge GPU VRAM | **Standard onboard CPU** ($<0.3\text{ ms}$ SIMD batch evaluation) |
| **Empirical Evaluation** | Ad-hoc obstacle tests | Monolithic benchmark scores | Systematic 3-way ablation isolating detection vs. prediction |

---

## 4. Differentiation from Modern MPPI Paradigms

A critical aspect of academic positioning is distinguishing this work from contemporary high-performance MPPI variants published in 2024–2025:

1. **Analytical Safety Filters vs. Proactive Trajectory Reshaping (SE-MPPI [L15]):**
   Kang's SE-MPPI introduces an online local-minima escape mechanism paired with a Control Barrier Function (CBF) quadratic program (QP) that projects synthesized control commands $\mathbf{u}_0^*$ onto a safe boundary. While CBFs provide rigorous mathematical guarantees for known moving boundaries, they act as reactive post-filters on the immediate control command and do not reshape the predictive rollout distribution over multi-second horizons. In contrast, our dynamic critic biases the stochastic sampling distribution proactively, enabling early yielding maneuvers before the robot reaches barrier boundaries.
2. **Geometric Complexity vs. Semantic Dynamic Tracking (EXACT-MPPI [L16]):**
   Peng et al. calculate exact continuous signed-distance functions (SDF) between arbitrary non-convex robot footprints and raw point clouds in JAX. While EXACT-MPPI excels at navigating tight passages with asymmetric geometry, it offloads computation to a dedicated GPU runtime in Python/JAX, relies on dense unsegmented point clouds, and treats obstacles as instantaneous geometry rather than tracking velocity vectors. Our work prioritizes semantic dynamic tracking on standard CPU hardware within native Nav2 C++.
3. **Clustering Symmetrical Modes vs. Velocity-Driven Asymmetry (CSC-MPPI [L17]):**
   RCILab addresses MPPI's *mode-averaging collapse*—where symmetrical obstacle encounters cause left- and right-swerving rollouts to average into a fatal head-on collision—by running GPU-accelerated DBSCAN clustering (cuML) and solving primal-dual constrained sampling. In human-robot cross-traffic, however, the dynamic velocity vector of the obstacle ($\mathbf{v}_{\text{obs}}$) naturally breaks spatial symmetry. By penalizing future obstacle locations, our dynamic critic naturally skews rollout costs toward the obstacle's trailing side without requiring heavy GPU clustering.

---

## 5. Acknowledged Limitations & Quantified Constraints

- **Simulation-First Baseline:** Primary quantitative benchmarks are conducted within Gazebo Harmonic using scripted actors. Randomized timing, arrival offsets, speeds ($0.5\text{--}2.0\text{ m/s}$), and crossing angles mitigate trajectory predictability.
- **Short-Term Kinematic Assumption:** Obstacle motion prediction relies on a Constant Velocity (CV) model valid over short preview horizons ($T \le 2.0\text{ s}$). Long-horizon social intent inferencing and complex crowd interactions are explicitly out of scope.
- **Sensor Intersection Plane:** Planar LiDAR depth anchoring relies on target obstacles intersecting the laser height plane ($10\text{--}20\text{ cm}$ above the floor). Obstacles outside the plane (e.g., hanging overhead hazards) cannot be metric-anchored without secondary geometric assumptions.
- **Experimental Demonstration vs. Safety Certification:** The software framework demonstrates predictive avoidance in simulation. Low-level safety laser scanner E-stop zones and functional safety hardware interlocks (ISO 3691-4) remain untouched.
