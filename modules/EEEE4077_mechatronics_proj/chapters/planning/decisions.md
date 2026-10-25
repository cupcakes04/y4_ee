# Architectural Decision Records & Open Items

> **Purpose**: Formal architectural decisions (ADRs) recorded for supervisor review, Project Planning Report, and thesis defense.

---

## 1. Architectural Decisions (ADRs)

- **D1 — ROS 2 Distribution:** Propose ROS 2 **Jazzy Jalisco** with **Gazebo Harmonic**. Iron reached EOL in Dec 2024; Humble reaches EOL in May 2027 (simultaneous with final graduation).
- **D2 — Simulation Platform:** **Gazebo Harmonic is primary and exclusive.** In strict adherence to supervisor specification `SD-MEng-26-01` (HW 0% / SW 60% / Research 40%), all development and evaluation are committed to software simulation.
- **D3 — Two-Tier Specifications:** Every numeric target is structured with a Minimum threshold (baseline pass) and Target aspiration (research aim) to prevent binary failure modes.
- **D4 — Execution & Measurement Hardware:** Core benchmarks and loop rates are committed on the host workstation (AMD/Intel multi-core CPU + NVIDIA RTX 4070 Ti Super).
- **D5 — Decoupled Sensor Fusion (2D MOT in Image Space over 3D Point Clustering):** Uses ByteTrack (`boxmot`) directly in 2D image space to handle visual data association, occlusion bridging, and persistent `track_id`s, followed by planar LiDAR frustum gating and a clean per-track linear Kalman filter (CV). This avoids building fragile combinatorial metric-space cluster association engines from scratch.
- **D6 — Native Nav2 C++ Critic Plugin over External Controller Rewrites:** Develops a native `mppi::critics::CriticFunction` plugin inside `nav2_mppi_controller`. This maintains 100% compatibility with Nav2 costmaps, recoveries, and Behavior Trees, avoiding the massive overhead of rewriting the controller in Python or external GPU runtimes.
- **D7 — Sensor Modality Selection (2D LiDAR + Monocular RGB over Stereo/3D LiDAR):** Retains 2D LiDAR for wide horizontal FOV ($270^\circ–360^\circ$), mm-accuracy Time-of-Flight ranging at $8+\text{ m}$, and direct compatibility with brownfield commercial AMR fleets. Stereo cameras were evaluated and rejected due to narrow FOV ($<85^\circ$), quadratic depth noise degradation beyond $4\text{ m}$, and failure on textureless warehouse walls (detailed in `research/08_design_tradeoffs_and_alternatives.md` §8.1–§8.2).
- **D8 — Geometric LiDAR Frustum Gating over Deep Monocular Depth Estimation:** Uses deterministic checkerboard extrinsic projection ($K[R \mid t]$) to gate laser returns in $<0.1\text{ ms}$, rather than running heavy monocular depth estimation models (e.g. Metric3D) which introduce scale drift, domain shift, and $>30\text{ ms}$ GPU latency.
- **D9 — Positioning vs. Modern SOTA MPPI Variants (SE-MPPI, EXACT-MPPI, CSC-MPPI):** Recognizes recent MPPI frameworks in literature as conceptual baselines. Rejects them as direct code drop-in benchmarks to avoid confounding variables (GPU vs. CPU runtimes, non-convex mesh inputs vs. semantic tracking). Our system targets the low-cost brownfield AMR CPU budget.

---

## 2. Active Open Items

1. **Supervisor Consultation:** Confirm meeting cadence, exact calendar dates for Progress Reviews 1–5, and weekly commitment with Dr. Shalini Darmaraju.
2. **Primary-Source Bibliography Verification:** Complete verification of primary IEEE/arXiv page ranges for L1, L4, L5, L15, L16, L17 prior to final dissertation submission.
3. **Host Environment Finalization:** Confirm host OS configuration (Ubuntu 24.04 bare-metal dual-boot vs. WSL2 with CUDA passthrough).
