# Project Specifications & Scope Tiers

## 1. Scope Tiers

| Tier | ID | Item | Maps to Research Module | Depends on |
|---|---|---|---|---|
| **Core** | O1 | Multi-Modal Dynamic-Obstacle Tracker (`lidar_vision_tracker`) | Module 2 | Sim baseline (T1) |
| **Core** | O2 | Predictive Dynamic MPPI Critic (`nav2_mppi_dynamic_critic`) | Module 3 | O1 |
| **Core** | O3 | Systematic 3-Way Comparative Ablation & Performance Benchmark | Evaluation & Methodology | O1, O2 |
| Stretch | S1 | Semantic Surface Hazard Augmentation (`avp` / `semantic_context_layer` exploratory track) | Module 1 | Baseline |
| Stretch | S2 | Physical-robot / Jetson validation (personal-budget hardware, outside committed scope) | All | O1–O3 |

**Out of scope:** Fleet management, SLAM/localisation research, running heavy foundation models directly on the robot, 3D reconstruction, formal safety certification.

---

## 2. SMART Specifications

All numeric targets are **hypotheses**. "Minimum" is the lowest outcome that still counts as meeting the requirement. "Target" is the aim. Baselines are measured in Phase A (T1). Difficulty is the expected challenge: **L**ow, **M**edium, or **H**igh.

| ID | Requirement | Minimum | Target | Why this number | Test and success criterion | Diff. |
|---|---|---|---|---|---|---|
| **O1-a** | Tracked-obstacle velocity RMSE at $\le 8\text{ m}$ | $< 0.25\text{ m/s}$ | **$< 0.15\text{ m/s}$** | ~10% of nominal walking speed (~1.4 m/s). Gazebo ground truth is exact. | $\ge 30$ randomised crossings per scenario. RMSE of $\|v_{\text{est}} - v_{\text{true}}\|$ over tracked frames. | M |
| **O1-b** | Association: fraction of detections assigned correct LiDAR range | $\ge 85\%$ | **$\ge 95\%$** | Wrong gating yields incorrect velocity. | Compare assigned cluster with ground-truth position ($< 0.3\text{ m}$). | M |
| **O2-a** | Freezes (Nav2 recovery or halt events) per 10 crossings | $\ge 50\%$ below baseline | **0** | Baseline hypothesis $> 5$ per 10. Freezing is a known failure mode (L1). | Count `controller_server` failures, recovery BT activations, stops $> 2\text{ s}$. Paired runs, same seeds. | H |
| **O2-b** | Mean route completion time | $\ge 10\%$ shorter | **15–25% shorter** | Freezing costs time; 15–25% gain is the working hypothesis. | Mean $\pm$ 95% CI over $\ge 30$ runs vs baseline B0. | M |
| **O2-c** | Safety: collisions (hard constraint) | 0 | **0** | Any intervention adding collisions is unacceptable. | Gazebo contact sensor. Any collision fails the run. | M |
| **O3-a** | 3-Way Ablation: Statistically significant separation between configurations C0, C1, and C2 | $p < 0.05$ | **$p < 0.01$** | Proves isolated contributions of (1) visual identification vs. (2) motion prediction over range-only baseline. | Paired Welch's t-test / ANOVA across 30 runs per scenario across speeds ($0.5–2.0\text{ m/s}$) and densities. | M |
| **O3-b** | Waiting time: cumulative duration robot remains stationary ($v < 0.05\text{ m/s}$) | $\ge 50\%$ reduction | **$\le 5\text{ s}$ per run** | Quantifies reduction in freezing delays at intersections. | Log total seconds with near-zero base velocity during active navigation goals. | M |
| **O3-c** | Computational efficiency: end-to-end control loop rate | $\ge 15\text{ Hz}$ | **$\ge 20\text{ Hz}$** | Must exceed LiDAR scan rate (~10 Hz) to guarantee real-time MPPI trajectory generation. | Sustained mean execution frequency of perception-to-critic loop over 5-minute runs. | L |
| **S1** | Exploratory hazard-polygon avoidance (`avp` / IPM track) | $\le 10\%$ infractions | **0%** | Explores dynamic keepout filtering for non-geometric surface hazards. | Runs in worlds with spawned surface hazards; log entry into polygon. | H |
| **S2** | Hardware replication of a subset of O1/O2 | Qualitative | **Quantitative** | Best-effort hardware validation on personal budget. | Repeated crossing tests on physical robot. | H |
| **NF1** | Reproducibility: one launch file + pinned container reproduces results | Yes | **Yes** | Required for marker evaluation and future research. | Clean-container execution reproduces headline tables. | L |
