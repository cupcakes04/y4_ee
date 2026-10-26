# Project Specifications & Performance Hypotheses

> **Purpose**: Formal engineering specifications agreed for supervisor review, Project Planning Report (§2), and thesis validation criteria. Directly derived from `chapters/research/05_ablation_and_evaluation.md` and supervisor brief `raw/proposals/` (`SD-MEng-26-01`).

---

## 1. Core Objectives

The project strictly focuses on three committed core engineering objectives in software simulation, in full alignment with the supervisor specification (`SD-MEng-26-01`: HW 0% / SW 60% / Research 40%):

| ID | Title | Scope & Description | Source Module |
|---|---|---|---|
| **O1** | **Multi-Modal Dynamic Obstacle Tracker** | Adapt visual detection and planar LiDAR range gating via extrinsic calibration ($[R \mid t]$) and 2D MOT (ByteTrack) coupled to a linear Kalman filter (CV) to estimate dynamic obstacle positions and velocities. | `research/03_perception_and_tracking.md` |
| **O2** | **Predictive Dynamic MPPI Controller** | Develop a native C++ `pluginlib` MPPI trajectory critic (`DynamicObstaclesCriticPlugin`) that projects obstacle velocities forward across the lookahead horizon ($\tau \in [0, 2.0]\text{ s}$) to eliminate the freezing robot problem. | `research/04_predictive_mppi_control.md` |
| **O3** | **Systematic 3-Way Comparative Ablation** | Benchmark the system within Gazebo Harmonic across standardized dynamic scenarios (crossing speeds $0.5\text{--}2.0\text{ m/s}$, varying angles and densities), rigorously isolating visual detection (C1) from motion prediction (C2) against baseline Nav2 (C0). | `research/05_ablation_and_evaluation.md` |

**Explicitly Out of Scope:** Physical hardware procurement/fabrication, robot fleet management, SLAM/mapping research, running foundation models directly on the robot, and formal safety laser certification (ISO 3691-4).

---

## 2. SMART Specifications & Quantitative Hypotheses

All numeric targets are formulated as research **hypotheses** evaluated in simulation. Each requirement defines a **Minimum** threshold (baseline pass criterion) and an aspirational **Target** (research aim). Difficulty is rated: **L**ow, **M**edium, or **H**igh.

| ID | Requirement | Minimum | Target | Engineering Justification | Test & Success Criterion | Diff. |
|---|---|---|---|---|---|---|
| **O1-a** | Tracked-obstacle velocity RMSE at $\le 8\text{ m}$ | $< 0.25\text{ m/s}$ | **$< 0.15\text{ m/s}$** | ~10% of nominal pedestrian walking speed (~1.4 m/s). Essential for stable MPPI forward projection. | $\ge 30$ randomized crossings per scenario in Gazebo. Compute RMSE against simulator ground-truth velocity. | M |
| **O1-b** | Data Association Accuracy | $\ge 85\%$ | **$\ge 95\%$** | Erroneous ray gating produces massive range spikes and destabilizes Kalman state covariance. | Percentage of visual detections assigned the correct laser cluster ($< 0.3\text{ m}$ Euclidean error). | M |
| **O2-a** | Controller Freezing (Halts / Recovery Activations) | $\ge 50\%$ below baseline | **0** | Baseline Nav2 MPPI treats moving agents as static walls, frequently freezing (Trautman & Krause [L1]). | Count `controller_server` timeouts, recovery behavior tree triggers, and stationary halts $> 2.0\text{ s}$ per 10 crossings. | H |
| **O2-b** | Mean Route Completion Time | $\ge 10\%$ shorter | **15–25% shorter** | Proactive speed modulation and continuous yielding prevent stopping delays at intersections. | Mean transit duration $\pm$ 95% CI over $\ge 30$ paired runs per scenario against baseline C0. | M |
| **O2-c** | Collision-Free Traversal (Hard Constraint) | 0 | **0** | Proactive yielding must not compromise basic collision avoidance safety under any condition. | Monitored via Gazebo physics contact sensor. Any collision invalidates the trial. | M |
| **O3-a** | 3-Way Ablation Separation (C0 vs C1 vs C2) | $p < 0.05$ | **$p < 0.01$** | Proves isolated contributions of (1) visual identification vs. (2) temporal motion prediction over baseline. | Paired Welch's t-test and one-way ANOVA across 30 runs per scenario across crossing speeds ($0.5–2.0\text{ m/s}$). | M |
| **O3-b** | Cumulative Waiting Time Reduction | $\ge 50\%$ reduction | **$\le 5\text{ s}$ per run** | Quantifies reduction in idle freezing delays when crossing dynamic corridors. | Summed seconds where robot linear velocity $|v| < 0.05\text{ m/s}$ while navigation goal is active. | M |
| **O3-c** | End-to-End Control Loop Rate | $\ge 15\text{ Hz}$ | **$\ge 20\text{ Hz}$** | Must exceed typical planar LiDAR scan rates (~10–20 Hz) to maintain real-time MPPI trajectory generation. | Sustained average execution frequency of the perception-tracking-critic pipeline over 5-minute runs. | L |
| **NF1** | Reproducibility & Docker Containerization | Yes | **Yes** | Academic rigor requires that all simulation scenarios, benchmark scripts, and metric loggers be fully reproducible. | Single ROS 2 launch command inside a pinned container reproduces headline evaluation tables. | L |

---

## 3. Stretch Goals

In accordance with proposal guidance and workshop standards, stretch goals provide flexibility and innovation opportunities if development proceeds ahead of schedule:

| ID | Stretch Goal | Description & Scope | Trigger Condition |
|---|---|---|---|
| **S1** | **Multi-Agent Crowd Density Stress Benchmark** | Scale the dynamic scenario from 1–2 crossing agents up to 4–6 interacting agents in constrained corridor intersections to evaluate ByteTrack track persistence and MPPI cost surface non-convexity. | Triggered if O1 and O2 meet Target criteria by Review 3 (Week 18). |
| **S2** | **High-Speed & Non-Orthogonal Crossing Angles** | Evaluate obstacle crossing speeds up to $2.5\text{ m/s}$ and oblique intersection angles ($30^\circ, 45^\circ, 135^\circ$) to probe the kinematic limits of the Constant Velocity (CV) Kalman filter model. | Triggered if core ablation runs on Scenarios A–D complete before Week 22. |
| **S3** | **CPU-Only Real-Time Deployment Profiling** | Benchmark the end-to-end perception and control pipeline on a resource-constrained 4-core embedded CPU profile (simulated or containerized cgroups CPU limit) to prove feasibility on low-cost brownfield AMRs without discrete edge GPUs. | Triggered if primary workstation benchmarking completes with excess compute margins. |

---

## 4. Mapping Objectives to Deliverables & Assessment Methods

Direct alignment between committed project objectives, tangible deliverables, and objective assessment metrics (as required by module rubrics and Saleha's Slide 5):

| Objective ID | Key Tangible Deliverable | Concrete Artifact / Source Code | Assessment Method & Validation Metric |
|---|---|---|---|
| **O1** | Multi-modal dynamic obstacle tracking module | ROS 2 tracker node (`lidar_vision_tracker`), extrinsic calibration package, and ByteTrack wrapper | Velocity RMSE $< 0.15\text{ m/s}$ and association accuracy $\ge 95\%$ evaluated against Gazebo ground-truth `/tf` across $\ge 30$ randomized runs. |
| **O2** | Predictive MPPI dynamic critic plugin | Native C++ `pluginlib` package (`DynamicObstaclesCriticPlugin`) integrated into `nav2_mppi_controller` | Freezing events reduced to 0 per 10 crossings; transit duration reduced by 15–25% vs C0; 0 physics collisions recorded. |
| **O3** | 3-Way comparative ablation benchmark suite | Automated Gazebo Harmonic testbed scripts, scenario generators (A–E), metric loggers, statistical plotting scripts | Paired Welch's t-test and one-way ANOVA showing statistically significant separation ($p < 0.01$) across configurations C0, C1, and C2. |
| **Core** | Complete Project Planning Report & Final Thesis | Compiled proposal document (7–8 pages) and final dissertation | Evaluated against MEng marking rubrics (Scope, Methodology, Originality, Risk Management, and Delivery). |
