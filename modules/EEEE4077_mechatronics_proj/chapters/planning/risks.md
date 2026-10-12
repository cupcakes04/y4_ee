# Project Risk Management

## 1. Risk Evaluation Framework

- **Scales:** Likelihood ($L = 1–5$), Impact ($I = 1–5$), Score = $L \times I$.
- **Critical Threshold:** Scores $\ge 15$ are classified as **Critical** and require both pre-mitigation and post-mitigation ratings, explicit fallback mechanisms, and stage-gate milestones.
- **Scope of Risks:** Strictly focused on engineering, technical execution, procurement, and project delivery risks (not generic workplace Health & Safety).

---

## 2. Risk Register

| ID | Risk Description | L | I | Score | Phase | Unmitigated Impact | Mitigation Strategy | Post Score |
|---|---|---|---|---|---|---|---|---|
| **R1** | Toolchain / OS / GPU setup failure (Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, CUDA on host) | 4 | 4 | **16** | W1–W3 | 2–3 weeks lost | Dedicated environment spike in W1. Evaluate bare-metal dual-boot vs WSL2. Use pinned Docker containers. | $2 \times 3 = \mathbf{6}$ |
| **R2** | Custom MPPI critic C++ plugin takes longer than scheduled (first C++ plugin) | 4 | 5 | **20** | W8, W13–W18 | 3–4 weeks lost | Early "Hello-Critic" spike in W8. **Fallback F1:** Publish predicted obstacles into local costmap layer to trigger stock critics. | $3 \times 3 = \mathbf{9}$ |
| **R3** | Research scope exceeds available hours (450 h across 30 weeks) | 4 | 4 | **16** | All | 3–6 weeks slip | Explicit Core (O1–O3) vs Stretch (S1–S2) tiers. Stage-gate reviews R1–R5. Drop S2 then S1 first. | $3 \times 3 = \mathbf{9}$ |
| **R4** | Camera–LiDAR calibration & frustum association error degrades EKF velocity | 3 | 4 | 12 | W7–W12 | 2 weeks lost | Calibrate in simulation with ground truth first. Sensitivity sweep on calibration jitter. | $2 \times 3 = \mathbf{6}$ |
| **R5** | Foundation-model label noise reduces edge segmenter mIoU below 0.60 | 3 | 3 | 9 | W9–W20 | 1–2 weeks lost | Interactive human curation UI in `avp`. Confidence threshold filtering. Hand-annotated held-out set. | $2 \times 2 = \mathbf{4}$ |
| **R6** | Target Jetson edge compute unavailable / delayed | 4 | 2 | 8 | W20 | Benchmark wording | Primary benchmarks committed on desktop RTX 4070 Ti Super; Jetson validation classified as stretch S2. | $4 \times 1 = \mathbf{4}$ |
| **R7** | Simulation fidelity / scripted actor generalisation limits | 4 | 2 | 8 | W19–W24 | Weakened claims | Paired randomised scenarios with varying speeds/offsets. Real video evaluation for O3. | $3 \times 2 = \mathbf{6}$ |
| **R8** | Competing academic workload (other modules, exams) | 4 | 3 | 12 | Jan, Apr | 2–3 weeks slip | Workload reduction planned during exam windows. Explicit 1-week buffer in W30. | $3 \times 2 = \mathbf{6}$ |
| **R9** | Physical hardware delivery delays (S2) | 4 | 2 | 8 | W16–W24 | S2 delayed | Component orders placed by W16. S2 decoupled from degree pass criteria. | $3 \times 1 = \mathbf{3}$ |
| **R10** | Data / code loss or broken environment | 2 | 4 | 8 | All | 1–2 weeks lost | Git repository with remote backup. Weekly semantic tagging. Containerized reproducibility. | $1 \times 4 = \mathbf{4}$ |
| **R11** | Numeric target hypotheses overly ambitious | 3 | 2 | 6 | W19–W24 | Spec failure | Two-tier specification (Minimum vs Target). Transparent reporting of negative results. | $2 \times 2 = \mathbf{4}$ |

---

## 3. Fallback Mechanisms
- **Fallback F1 (for R2 - MPPI Critic):** If compiling a native C++ MPPI critic plugin proves intractable within the W8 spike window, an intermediate ROS 2 node will project predicted obstacle positions as synthetic geometric footprints directly into a custom dynamic Nav2 Costmap layer. This allows stock MPPI obstacle critics to react without modifying controller internals.
