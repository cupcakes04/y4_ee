# Architectural Decision Records & Open Items

## 1. Architectural Decisions (ADRs)

- **D1 — ROS 2 Distribution:** Propose ROS 2 **Jazzy Jalisco** with **Gazebo Harmonic**. Iron reached EOL in Dec 2024; Humble reaches EOL in May 2027 (simultaneous with final submission).
- **D2 — Simulation Platform:** **Gazebo Harmonic is primary.** Isaac Sim is removed from committed scope to eliminate setup risk; reserved as optional stretch.
- **D3 — Two-Tier Specifications:** Every numeric target is structured with a Minimum threshold (baseline pass) and Target aspiration (research aim) to prevent binary failure.
- **D4 — FPS Measurement Hardware:** Core FPS benchmark committed on host NVIDIA RTX 4070 Ti Super. Jetson Orin validation is scoped as stretch goal S2.
- **D5 — Dataset Grounding:** O3 distillation training and held-out validation are conducted on real walkthrough video footage, ensuring distillation claims are not sim-only artifacts.
- **D6 — Detector Decoupling:** Tracker development (O1) initiates using standard pre-trained COCO object detectors (person/forklift) so perception development is not blocked by O3 distillation pipeline maturation. Swapping to the distilled model occurs in integration task T5.
- **D7 — Sensor Modality Selection (2D LiDAR + Monocular RGB over Stereo/3D LiDAR):** Retains 2D LiDAR for wide horizontal FOV ($270^\circ–360^\circ$), mm-accuracy Time-of-Flight ranging at $8+\text{ m}$, and direct compatibility with brownfield commercial AMR fleets. Stereo cameras were evaluated and rejected due to narrow FOV ($<85^\circ$), depth noise degradation beyond $4\text{ m}$, and failure on textureless warehouse walls (detailed in `research/08_design_tradeoffs_and_alternatives.md`).
- **D8 — Two-Stage Tracking Architecture (Decoupled 2D MOT over 3D Hungarian Matching):** Uses ByteTrack (`boxmot`) directly in 2D image space to handle visual data association, occlusion bridging, and persistent `track_id`s, followed by planar LiDAR frustum gating and a clean per-track linear Kalman filter (CV). This eliminates the need to build fragile combinatorial metric-space cluster association engines from scratch.
- **D9 — Scope of Semantic Context vs. Deterministic Safety (CAD for Walls, Vision for Flat/Transient Hazards):** Retains hand-drawn deterministic CAD / vector costmap filters for certified permanent infrastructure (walls, machinery) under ISO 3691-4. The prompt-distillation and IPM vision pipeline is explicitly scoped to augment CAD by detecting transient, non-geometric surface hazards ($Z \approx 0$, fluid spills, temporary lane markings) and dynamic obstacle classes where LiDAR physically fails (detailed in `research/08_design_tradeoffs_and_alternatives.md` §8.6).
- **D10 — Alignment with Supervisor Specification (`SD-MEng-26-01`):** Adopts official project title *Vision-Augmented Mobile Robot Navigation in Dynamic Environments* (Code: `SD-MEng-26-01`). Aligns core deliverables strictly with the supervisor's 0% HW / 60% SW / 40% Research mandate: O1 (Multi-Modal Tracking), O2 (Predictive MPPI Critic), and O3 (Systematic 3-Way Comparative Ablation Benchmark). `avp` and floor hazard segmentation are positioned as an exploratory research track (S1).

---

## 2. Open Items Before Proposal Submission

1. **Supervisor Consultation:** Confirm meeting cadence, exact dates for Progress Reviews 1–5, and weekly commitment with Dr. Shalini Darmaraju.
2. **Appendix Integration (RESOLVED):** Official supervisor project brief `SD-MEng-26-01` obtained from Dr Shalini Darmaraju and Ir Dr Daniel Pu; full text integrated into Appendix A.
3. **Primary-Source Bibliography Verification:** Verify primary DOI pages for L1, L4, L5, and confirm nominal pedestrian walking speed literature.
4. **Environment Decision:** Finalise host OS configuration (Ubuntu 24.04 bare-metal dual boot vs. WSL2 with CUDA passthrough).
5. **Toolchain Prototype Audit:** Verify end-to-end execution of `avp` repo to confirm baseline auto-labelling pipeline feasibility.
