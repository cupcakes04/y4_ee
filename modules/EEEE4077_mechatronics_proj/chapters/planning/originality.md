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

## 2. Comparison with Current Practice & Academic Frontiers

| Capability | Current Industrial Practice | Academic Research SOTA (GPU / SOTA MPPI) | This FYP Project (Brownfield Retrofit) |
|---|---|---|---|
| **Dynamic Obstacle Handling** | Emergency stop / recovery rotate (freezing) | Heavy neural transformers or GPU JAX/cuML rollouts (EXACT-MPPI [L16], CSC-MPPI [L17]) | 2D LiDAR + camera frustum KF → Native Nav2 C++ MPPI dynamic critic plugin |
| **Local Planning Costmap** | Static 2D costmap ($t=0$); dynamic agents treated as walls | Continuous SDF fields or 3D spatio-temporal voxel grids | Decoupled: static costmap for fixed infrastructure + dynamic critic for moving agents |
| **Safety / Yielding Mechanism** | Passive safety zone E-stop | QP Control Barrier Function post-filter on $\mathbf{u}_0^*$ (SE-MPPI [L15]) | Proactive spatio-temporal cost shaping over preview horizon $\tau \in [0, 2.0]\text{ s}$ |
| **Sensor Hardware Cost** | \$400 (2D LiDAR only) | \$4,000–\$10,000 (3D LiDAR + Depth camera rigs) | **\$430–\$480** (2D LiDAR + monocular camera retrofit) |
| **Compute Envelope** | Low-power x86 / ARM CPU | High-end workstation / dedicated edge GPU VRAM | **Standard onboard CPU** ($<0.3\text{ ms}$ SIMD batch evaluation) |
| **Empirical Evaluation** | Ad-hoc obstacle tests | Monolithic benchmark scores | Systematic 3-way ablation isolating detection vs. prediction |

---

## 3. Acknowledged Limitations & Quantified Constraints

- **Simulation-First Baseline:** Primary quantitative benchmarks are conducted within Gazebo Harmonic using scripted actors. Randomized timing, arrival offsets, speeds ($0.5\text{--}2.0\text{ m/s}$), and crossing angles mitigate trajectory predictability.
- **Short-Term Kinematic Assumption:** Obstacle motion prediction relies on a Constant Velocity (CV) model valid over short preview horizons ($T \le 2.0\text{ s}$). Long-horizon social intent inferencing and complex crowd interactions are explicitly out of scope.
- **Sensor Intersection Plane:** Planar LiDAR depth anchoring relies on target obstacles intersecting the laser height plane ($10\text{--}20\text{ cm}$ above the floor). Obstacles outside the plane (e.g., hanging overhead hazards) cannot be metric-anchored without secondary geometric assumptions.
- **Experimental Demonstration vs. Safety Certification:** The software framework demonstrates predictive avoidance in simulation. Low-level safety laser scanner E-stop zones and functional safety hardware interlocks (ISO 3691-4) remain untouched.
