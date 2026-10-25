# Project Risk Management

> **Purpose**: Formal project risk register for supervisor review, Project Planning Report (§5, Table 5), and viva presentation. Synchronized with the technical architecture in `chapters/research/`.

---

## 1. Risk Evaluation Framework

- **Scales:** Likelihood ($L = 1–5$), Impact ($I = 1–5$), Score = $L \times I$.
- **Critical Threshold:** Scores $\ge 15$ are classified as **Critical** and require pre- and post-mitigation ratings, explicit fallback mechanisms, and stage-gate milestones.
- **Focus:** Engineering, implementation, and academic schedule risks directly impacting simulation delivery (generic workplace Health & Safety risks excluded as per rubric guidelines).

---

## 2. Risk Register

| ID | Risk Description | L | I | Score | Phase | Unmitigated Impact | Mitigation Strategy | Post Score |
|---|---|---|---|---|---|---|---|---|
| **R1** | Toolchain / OS / GPU setup failure (Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, CUDA on host) | 4 | 4 | **16** | W1–W3 | 2–3 weeks lost | Dedicated environment spike in W1. Evaluate bare-metal dual-boot vs WSL2. Use pinned Docker container image. | $2 \times 3 = \mathbf{6}$ |
| **R2** | Custom MPPI critic C++ plugin takes longer than scheduled (first C++ plugin) | 4 | 5 | **20** | W8, W13–W18 | 3–4 weeks lost | Early "Hello-Critic" spike in W8. **Fallback F1:** Publish predicted obstacles into local costmap layer to trigger stock critics. | $3 \times 3 = \mathbf{9}$ |
| **R3** | Research scope exceeds available hours (450 h across 30 weeks) | 4 | 4 | **16** | All | 3–6 weeks slip | Commit strictly to software simulation (O1–O3). Stage-gate progress reviews R1–R5. Drop complex crowd density scenarios first. | $3 \times 3 = \mathbf{9}$ |
| **R4** | Camera–LiDAR calibration & frustum association error degrades EKF velocity | 3 | 4 | 12 | W7–W12 | 2 weeks lost | Calibrate in simulation with ground truth first. Sensitivity sweep on calibration jitter. | $2 \times 3 = \mathbf{6}$ |
| **R5** | High-density multi-actor occlusions cause track switching or ghost tracks | 3 | 3 | 9 | W9–W14 | 1–2 weeks lost | Leverage ByteTrack's two-stage association to preserve IDs; implement strict track death thresholds ($>0.5\text{ s}$ loss). | $2 \times 2 = \mathbf{4}$ |
| **R6** | Simulation fidelity / scripted actor generalisation limits | 4 | 2 | 8 | W19–W24 | Weakened claims | Paired randomised scenarios with varying speeds ($0.5\text{--}2.0\text{ m/s}$), arrival offsets, and crossing angles. | $3 \times 2 = \mathbf{6}$ |
| **R7** | Competing academic workload (other modules, exams) | 4 | 3 | 12 | Jan, Apr | 2–3 weeks slip | Workload reduction planned during exam windows. Explicit 1-week buffer in W30. | $3 \times 2 = \mathbf{6}$ |
| **R8** | Data / code loss or broken development environment | 2 | 4 | 8 | All | 1–2 weeks lost | Git repository with remote GitHub backup. Weekly semantic tagging. Containerized reproducibility. | $1 \times 4 = \mathbf{4}$ |
| **R9** | Numeric target hypotheses overly ambitious | 3 | 2 | 6 | W19–W24 | Spec failure | Two-tier specification (Minimum vs Target). Transparent reporting of negative results. | $2 \times 2 = \mathbf{4}$ |

---

## 3. Fallback Mechanisms
- **Fallback F1 (for R2 - MPPI Critic):** If compiling a native C++ MPPI critic plugin encounters intractable runtime linking issues within the W8 spike window, an intermediate ROS 2 node will project predicted obstacle positions as synthetic geometric footprints directly into a custom dynamic Nav2 Costmap layer (`VelocityInflationLayer`). This allows stock MPPI obstacle critics to react without modifying controller internals.
