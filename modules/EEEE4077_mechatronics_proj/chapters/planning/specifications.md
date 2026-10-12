# Project Specifications & Scope Tiers

## 1. Scope Tiers

| Tier | ID | Item | Maps to Research Module | Depends on |
|---|---|---|---|---|
| **Core** | O1 | LiDAR–vision dynamic-obstacle tracker (`lidar_vision_tracker`) | Module 2 | Sim baseline (T1) |
| **Core** | O2 | Velocity-aware MPPI critic (`nav2_mppi_dynamic_critic`) | Module 3 | O1 |
| **Core** | O3 | Prompt-to-edge distillation toolkit and segmenter (extends own prototype `avp`) | Module 1 (offline half) | Independent of O1/O2 |
| Stretch | S1 | Planar homography → Nav2 Keepout/Speed filters (`semantic_context_layer`) | Module 1 (online half) | O3 |
| Stretch | S2 | Physical-robot / Jetson validation (personal-budget hardware, outside committed scope) | All | O1–O3 |

**Out of scope:** Fleet management, SLAM/localisation research, running foundation models on the robot, 3D reconstruction, safety certification.

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
| **O3-a** | Setup time: walkthrough video → deployed TensorRT engine | $< 60\text{ min}$ | **$< 30\text{ min}$** | Replaces hours or days of manual CAD zoning. | Scripted end-to-end run on RTX 4070 Ti Super. Timer logs each stage. | M |
| **O3-b** | Segmentation agreement with human labels (mIoU) on held-out frames | $\ge 0.60$ | **$\ge 0.70$** | Working hypothesis; recalibrate after label audit (W10). | $\ge 200$ hand-checked frames unseen during training. | H |
| **O3-c** | Inference rate on target GPU (TensorRT FP16) | $\ge 15\text{ FPS}$ | **$\ge 25\text{ FPS}$** | Must exceed LiDAR rate (~10 Hz) so vision is not the bottleneck. | Sustained mean over 5 minutes. | L |
| **S1** | Hazard-polygon infractions | $\le 10\%$ of runs | **0%** | Complete avoidance is the intent of keepout filtering. | Runs in worlds with spawned hazards; log entry into polygon. | H |
| **S2** | Hardware replication of a subset of O1/O2 | Qualitative | **Quantitative** | Best-effort hardware validation on personal budget. | Repeated crossing tests on physical robot. | H |
| **NF1** | Reproducibility: one launch file + pinned container reproduces results | Yes | **Yes** | Required for marker evaluation and future research. | Clean-container execution reproduces headline tables. | L |
