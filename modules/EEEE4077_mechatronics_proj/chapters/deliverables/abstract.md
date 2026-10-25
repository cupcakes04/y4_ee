# Vision-Augmented Mobile Robot Navigation in Dynamic Environments

**Project Code:** SD-MEng-26-01 | **Supervisor:** Dr Shalini Darmaraju | **Moderator:** Ir Dr Daniel Pu

> Supervisor-facing draft, **derived** from `../research/`, `../planning/`, and `../library/register.md` (the modular sources of truth). The assessed submission is [project_proposal.md](project_proposal.md). Sync rules are in `.agents/skills/fyp-proposal-sync/SKILL.md`.
> ROS 2 terms appear in `code font` the first time. Each has a plain-language gloss, so you can read this without ROS knowledge and still map it to the actual implementation.

---

## 1. The problem, in plain language

Factories and warehouses increasingly deploy **autonomous mobile robots (AMRs)** to transport materials. In brownfield legacy facilities, the floor layout cannot be redesigned, and moving human workers and carts share narrow transit aisles with the robots. To remain commercially cost-effective, these robots rely on **planar 2D LiDAR** scanners ($360^\circ$ range sensing in a single horizontal slice) coupled to the open-source **ROS 2 Navigation stack (`Nav2`)**.

That setup suffers from a severe, long-standing operational pathology:

**The robot freezes around moving traffic.** A planar 2D LiDAR detects a walking person only as two isolated, disconnected dots (cross-sections of their lower limbs). The sensor cannot identify what the object is, which direction it is heading, or how fast it is moving. Nav2's local occupancy grid (the `costmap`) registers these reflections as stationary, impassable walls. When a pedestrian crosses an aisle ahead of the robot, the planner assumes the corridor is completely blocked and initiates an emergency stop, recovery rotations, or task abort—even though the person would have cleared the aisle before the robot arrived. This is formalized in robotics literature as the **"Freezing Robot Problem"** (Trautman & Krause, 2010). Conversely, if an agent converges toward an open space, the static costmap registers that space as free, causing the robot to drive directly into cross-traffic paths.

---

## 2. Gap in current practice

| What exists today | What is still missing for low-cost 2D-LiDAR AMRs |
|---|---|
| Planar Camera–LiDAR extrinsic calibration is well established (Zhang & Pless, 2004) and 2D multi-object tracking is mature (ByteTrack: Zhang et al., 2022). | An integrated, open-source pipeline that bridges 2D visual tracking and planar LiDAR ranges directly into **Nav2 local controller velocity predictions**, avoiding robot freezing without requiring expensive multi-channel 3D LiDAR ($>\$3,000$). |
| Nav2 provides the modern `nav2_mppi_controller` (a Model Predictive Path Integral controller that evaluates thousands of candidate trajectories using plug-in critics). | All 11 default critics shipped with Nav2 evaluate obstacles strictly against static 2D costmaps at $t=0$. Incorporating *tracked obstacle velocity* over the preview horizon requires a custom C++ critic plugin (`pluginlib`) forward-projecting obstacle positions ($\mathbf{p}_0 + \mathbf{v}\tau$). |
| Recent advanced MPPI research (EXACT-MPPI, CSC-MPPI) explores GPU-accelerated continuous Signed Distance Functions and trajectory clustering. | These frameworks require high-end edge GPUs running Python/JAX and CUDA/cuML. There is no lightweight, native C++ Nav2 plugin delivering predictive dynamic obstacle avoidance within standard CPU/SIMD compute budgets. |

> [!NOTE]
> This project is fundamentally **translational systems engineering and rigorous empirical validation**, rather than proposing speculative mathematical algorithms. It integrates published open-source techniques to solve a genuine industrial problem.

---

## 3. Problem statement

> Low-cost 2D-LiDAR AMRs operating in brownfield industrial environments **stall and freeze around moving workers and vehicles** because standard Nav2 costmaps treat dynamic agents as stationary walls. Existing solutions rely on cost-prohibitive 3D LiDARs or heavy GPU research frameworks. There is no open-source, computationally lean pipeline that:
> 1. Tracks dynamic obstacle velocities ($v_x, v_y$) on low-cost AMRs by fusing a planar 2D LiDAR with a single monocular camera.
> 2. Predicts short-term obstacle motion inside local MPPI trajectory rollouts via a native Nav2 C++ plugin to eliminate controller freezing.
> 3. Provides a systematic 3-way comparative ablation benchmark isolating the specific contribution of visual detection versus motion prediction.

---

## 4. Research question

**Can a camera-augmented 2D-LiDAR AMR, using open-source ROS 2 components and standard CPU compute, eliminate navigation stalls around dynamic obstacles and validate the isolated benefits of motion prediction, compared with standard Nav2 using 2D LiDAR alone?**

---

## 5. Objectives

All targets are **hypotheses to be tested**, not assumed promises. The project strictly focuses on three committed core engineering objectives in software simulation, in full alignment with the supervisor specification (`SD-MEng-26-01`: HW 0% / SW 60% / Research 40%):

| # | Objective | Key ROS 2 / Tech Terms | Assessment Method | Deliverable |
|---|---|---|---|---|
| **O1** | **Track moving obstacles.** Combine camera detections with 2D LiDAR ranges to estimate position and velocity of dynamic agents. | `lidar_vision_tracker` node; camera-LiDAR extrinsic calibration; frustum gating; Linear Kalman Filter (CV) | Velocity error (RMSE) against simulator ground truth in Gazebo. **Hypothesis: < 0.15 m/s at ≤ 8 m.** | ROS 2 package + test scenarios + tracking accuracy dataset |
| **O2** | **Stop freezing via predictive control.** Feed tracked velocities into Nav2's MPPI controller so it yields or smoothly swerves instead of halting. | `nav2_mppi_controller`; custom `nav2_mppi_dynamic_critic` plugin | Per scenario, compare against baseline Nav2 C0: number of stops/recoveries per 10 crossings, route completion time. **Hypothesis: zero freezes and 15–25% shorter route time.** | C++ critic plugin + comparative trajectory logs |
| **O3** | **Systematic 3-Way Comparative Ablation.** Isolate the contributions of visual detection vs. motion prediction across varying obstacle speeds ($0.5–2.0\text{ m/s}$), patterns, and densities. | C0 (LiDAR only) vs. C1 (Vision without prediction) vs. C2 (Full motion prediction); ANOVA / paired t-test | Waiting time reduction ($\ge 50\%$, target $\le 5\text{ s}$); route completion time; controller loop rate $\ge 20\text{ Hz}$. **Hypothesis: statistically significant gain ($p < 0.01$).** | Automated ablation test harness + statistical benchmark report |

### Explicitly Out of Scope
- Physical robot hardware fabrication, component procurement, or real-world laboratory testing.
- Fleet coordination, multi-robot traffic management, SLAM or localisation research.
- Running heavy multi-billion-parameter foundation models or neural transformers on the robot.
- Formal functional safety certification under ISO 3691-4 (standard Nav2 safety collision monitors remain untouched as the final line of defence).

---

## 6. Feasibility & Compute Allocation
- **Development & Simulation Platform:** High-performance desktop workstation equipped with an AMD/Intel multi-core CPU and NVIDIA RTX 4070 Ti Super GPU, running Ubuntu 24.04 LTS, ROS 2 Jazzy Jalisco, and Gazebo Harmonic.
- **Resource Budget:** 450 hours allocated across 30 weeks (~15 hours/week) structured across five progress review milestones agreed with the supervisor.
- **Key Risks & Mitigations:**
  - *Risk R2 (First custom MPPI C++ plugin):* Mitigated via an early W8 spike and an architectural fallback (`VelocityInflationLayer` in local costmap).
  - *Risk R1 (Toolchain setup):* Mitigated via containerized reproducibility (Docker).
  - *Risk R4 (Calibration/association jitter):* Mitigated via simulation-first calibration validation.

---

## 7. Glossary
- **AMR:** Autonomous Mobile Robot.
- **Brownfield:** An existing industrial facility retrofitted with automation rather than purpose-built.
- **2D LiDAR:** Time-of-Flight laser rangefinder measuring distance in a single planar horizontal sweep.
- **ROS 2 / Nav2:** Robot Operating System 2 and its production navigation framework.
- **Costmap:** 2D occupancy grid representing traversability costs around the robot (`nav2_costmap_2d`).
- **MPPI:** Model Predictive Path Integral control; a stochastic optimal controller evaluating sampled trajectory batches via critic plugins.
- **ByteTrack:** Association algorithm performing multi-object tracking directly in 2D image coordinates.
- **Linear Kalman Filter:** Recursive Bayesian state estimator tracking $[x, y, v_x, v_y]^T$ under a Constant Velocity (CV) kinematic model.

---

## 8. Master Literature References

All citations correspond to verified entries in [`chapters/library/register.md`](../library/register.md):

1. P. Trautman and A. Krause, "Unfreezing the robot: Navigation in dense, interacting crowds," *IEEE/RSJ IROS*, 2010.
2. S. Macenski, F. Martín, R. White and J. Ginés Clavero, "The Marathon 2: A Navigation System," *IEEE/RSJ IROS*, 2020.
3. S. Macenski et al., "From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in the Robot Operating System 2," *Robotics and Autonomous Systems*, 2023.
4. G. Williams et al., "Information theoretic MPC for model-based reinforcement learning," *IEEE ICRA*, 2017.
5. Q. Zhang and R. Pless, "Extrinsic calibration of a camera and laser range finder," *IEEE/RSJ IROS*, 2004.
6. Y. Zhang et al., "ByteTrack: Multi-Object Tracking by Associating Every Detection Box," *ECCV*, 2022.
7. S. Thrun, W. Burgard and D. Fox, *Probabilistic Robotics*, MIT Press, 2005.
8. D. Helbing and P. Molnar, "Social force model for pedestrian dynamics," *Physical Review E*, 1995.
9. Nav2 Development Team, "Nav2 MPPI Controller: Model Predictive Path Integral Trajectory Optimization," 2024.
10. J. M. Kang, "SE-MPPI: Nav2-Native Safe-Escape MPPI Controller with Control Barrier Functions," 2024.
11. C. Peng, "EXACT-MPPI: Exact Signed-Distance Navigation for Arbitrary-Footprint Robots from Point Clouds," 2024.
12. Robot Control and Intelligence Lab (RCILab), "Constrained Sampling MPPI Framework with DBSCAN for Reliable Obstacle Avoidance," *IEEE/RSJ IROS*, 2025.
