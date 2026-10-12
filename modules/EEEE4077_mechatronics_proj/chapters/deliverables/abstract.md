# Problem Statement & Research Objectives

> Supervisor-facing draft, **derived** from `../research/`, `../planning/`, and `../library/register.md` (the modular sources of truth). The assessed submission is [project_proposal.md](project_proposal.md). Sync rules are in `.agents/skills/fyp-proposal-sync/SKILL.md`.
> ROS 2 terms appear in `code font` the first time. Each has a plain-language gloss, so you can read this without ROS knowledge and still map it to the actual implementation.

---

## 1. The problem, in plain language

Factories and warehouses increasingly use **autonomous mobile robots (AMRs)** to move materials. Many existing sites are **"brownfield"**. They are legacy plants where the layout can't be redesigned for the robot, and people and forklifts share the floor with it. To keep cost down, these robots often use only a **2D LiDAR**, a laser scanner that measures distance in a single horizontal slice, and they navigate with the open-source **ROS 2 Navigation stack (`Nav2`)**.

That setup has two practical weaknesses:

1. **The robot freezes around moving traffic.** A 2D LiDAR sees a walking person as two small dots (their legs). It can't tell *what* the object is, *which way* it is heading, or *how fast* it is moving. Nav2's local map (the `costmap`) therefore treats the dots as fixed obstacles, so the robot stops, backs off or spins in place while people walk through. This is a long-recognised failure mode, known in the literature as the **"freezing robot problem"** (Trautman & Krause, 2010).
2. **The robot is blind to what the floor *means*.** The map records only where surfaces reflect laser light. It can't distinguish clean floor from a liquid spill, a forklift lane from a staging bay. Today an engineer has to survey the site and hand-draw "no-go" and "slow" zones (`Costmap Filters`: keepout and speed zones). This is slow, and it has to be redone whenever the layout changes.

## 2. Gap in current practice

| What exists | What is still missing for a low-cost 2D-LiDAR AMR |
|---|---|
| Camera + LiDAR calibration and fusion are well established (Zhang & Pless, 2004). | An integrated, packaged pipeline that supplies **tracked obstacle velocity** to Nav2's local controller, using only a 2D LiDAR and one camera. |
| Foundation models (Florence-2, Grounded-SAM) can label images from text prompts without manual annotation (Xiao et al., 2024; Ren et al., 2024). Their output has been distilled into robot navigation (ViLAM, 2025). | These models are too heavy to run on the robot. Published work targets social navigation or richer sensors, not **site-specific floor hazards** feeding **standard Nav2 components**. |
| Nav2 provides `MPPI controller` (a predictive controller that scores many candidate trajectories with plug-in "critics") and `Costmap Filters`. | Using a new critic or a new filter source takes custom engineering. Whether a built-in critic consumes *tracked obstacle velocity* **needs checking against the current Nav2 plugin list** before the originality claim is final. |

> [!NOTE]
> This project is mainly **engineering integration plus validation**. It is not a new fusion algorithm. That is deliberate and is consistent with the literature notes.

## 3. Problem statement

> Low-cost 2D-LiDAR AMRs in brownfield sites **stall around moving people and vehicles** and **ignore floor hazards** that their sensors cannot see. Fixing this today needs expensive sensors or manual site surveys. There is no open, low-cost, rapidly deployable pipeline that (a) gives Nav2 a velocity estimate for each moving obstacle by combining a 2D LiDAR with a single camera, and (b) turns text-described, site-specific hazards into Nav2 keepout and speed zones without hand-drawn CAD.

## 4. Research question

**Can a camera-augmented 2D-LiDAR AMR, using only open-source ROS 2 components and edge-class hardware, reduce navigation stalls around dynamic obstacles and automate site-specific hazard mapping, compared with standard Nav2 using 2D LiDAR alone?**

## 5. Objectives

All targets are **hypotheses to be tested**, not promises. Baselines will be measured in Phase 1 of the project (standard Nav2 + 2D LiDAR, same scenarios). The numbers below come from the working proposal and are not yet backed by literature.

### Core (must deliver)

| # | Objective | Key ROS 2 / tech terms | Assessment method | Deliverable |
|---|---|---|---|---|
| **O1** | **Track moving obstacles.** Combine camera detections with 2D LiDAR ranges to estimate position and velocity of pedestrians and vehicles. | `lidar_vision_tracker` node; camera-LiDAR extrinsic calibration; frustum gating; Extended Kalman Filter (EKF) | Velocity error (RMSE) against simulator ground truth in Gazebo / Isaac Sim. **Hypothesis: < 0.15 m/s at ≤ 8 m.** | ROS 2 package + test scenarios + results table |
| **O2** | **Stop freezing.** Feed tracked velocities into Nav2's controller so it slows or deflects instead of halting. | `nav2_mppi_controller`; custom `nav2_mppi_dynamic_critic` plugin | Per scenario, compare against baseline Nav2: number of stops/recoveries per 10 crossings, route time. **Hypothesis: fewer freezes and 15–25% shorter route time.** | Critic plugin + side-by-side simulation report |
| **O3** | **Teach the robot site-specific hazards quickly.** From a walkthrough video and text prompts, auto-label data and train a lightweight segmenter that runs in real time on the edge computer. | Offline VLM pseudo-labelling (Florence-2 / Grounded-SAM); YOLO-Seg; TensorRT; builds on own prior prototype `avp` (see note below) | Time from video to deployed model; segmentation quality (e.g. mIoU) on a held-out set; inference FPS on target hardware. **Hypothesis: < 30 min setup, ≥ 25 FPS.** | Distillation toolkit (CLI) + trained model + benchmark |

### Stretch (if on schedule)

| # | Objective | Key terms | Assessment | Deliverable |
|---|---|---|---|---|
| **S1** | Convert segmented hazards into **keepout and speed zones** in Nav2. | Inverse Perspective Mapping (floor-plane homography); `CostmapFilterInfo`, Keepout / Speed filters | Fraction of runs where the robot enters detected hazard polygons (**hypothesis: 0%**) | `semantic_context_layer` package |
| **S2** | Validate on a **physical robot** (personal-budget purchase; outside committed scope). | Jetson / mini-PC, real LiDAR + camera | Repeat a subset of O1–O2 tests on hardware | Short hardware validation report |

### Explicitly out of scope
- Fleet coordination, multi-robot traffic management, SLAM or localisation research.
- Running large foundation models on the robot.
- Full 3D reconstruction.
- Safety certification. The deterministic Nav2 safety layer (for example `Collision Monitor`) is kept as the last line of defence.

## 6. Feasibility and preliminary work
- **Compute:** simulation on a desktop RTX 4070 Ti Super (Gazebo / Isaac Sim, offline training).
- **Preliminary work:** `avp`, the candidate's own prototype for raw-data ingestion, auto-labelling with UI refinement, and fine-tuning for edge deployment. It is incomplete and not yet connected to ROS 2. It is listed as prior work, not as a result. Repo: <https://github.com/cupcakes04/avp>
- **Main risks** (full register to follow in the proposal): label noise from the foundation model; calibration error between camera and LiDAR; simulation-to-real gap; scope. The core/stretch split limits scope risk, and O1–O2 do not depend on O3.

## 7. Glossary
- **AMR:** autonomous mobile robot.
- **Brownfield:** an existing facility retrofitted with automation, as opposed to one built for it.
- **2D LiDAR:** laser scanner measuring distance in one horizontal plane.
- **ROS 2 / Nav2:** the standard open-source robot middleware and its navigation stack.
- **Costmap:** the robot's local grid map of "how costly or dangerous is each cell".
- **MPPI:** Model Predictive Path Integral control. It samples many trajectories and scores them with critics.
- **EKF:** Extended Kalman Filter, a standard estimator for position and velocity.
- **VLM:** vision-language model, which can label images from a text prompt.
- **TensorRT:** NVIDIA's runtime for fast model inference on edge devices.

## 8. References

All entries were opened or looked up on 2026-10-11 and the bibliographic details confirmed.

1. P. Trautman and A. Krause, "Unfreezing the robot: Navigation in dense, interacting crowds," *IEEE/RSJ IROS*, 2010, pp. 797–803. doi:10.1109/IROS.2010.5654369
2. S. Macenski, F. Martín, R. White and J. Ginés Clavero, "The Marathon 2: A Navigation System," *IEEE/RSJ IROS*, 2020. arXiv:2003.00368
3. S. Macenski et al., "From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in the Robot Operating System 2," *Robotics and Autonomous Systems*, 2023. arXiv:2307.15236
4. G. Williams et al., "Information theoretic MPC for model-based reinforcement learning," *IEEE ICRA*, 2017, pp. 1714–1721. doi:10.1109/ICRA.2017.7989202 (the theoretical basis cited by Nav2's MPPI)
5. Q. Zhang and R. Pless, "Extrinsic calibration of a camera and laser range finder (improves camera calibration)," *IEEE/RSJ IROS*, 2004.
6. B. Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," *CVPR*, 2024. arXiv:2311.06242
7. T. Ren et al., "Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks," 2024. arXiv:2401.14159
8. "ViLAM: Distilling Vision-Language Reasoning into Attention Maps for Social Robot Navigation," 2025. arXiv:2503.09820
9. Nav2 documentation (rolling):
   - [MPPI Controller](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/controller_plugins/mppi_controller/configuring_mppic/)
   - [Navigating with Keepout Zones](https://docs.nav2.org/rolling/tutorials/general_tutorials/navigation2_with_keepout_filter/navigation2_with_keepout_filter/)
   - [Navigating with Speed Limits](https://docs.nav2.org/rolling/tutorials/general_tutorials/navigation2_with_speed_filter/navigation2_with_speed_filter/)
   - [Using Collision Monitor](https://docs.nav2.org/rolling/tutorials/general_tutorials/using_collision_monitor/using_collision_monitor/)

---
### Notes for me (not for supervisor)
- Metric targets (0 freezes, 15–25%, < 30 min, ≥ 25 FPS, < 0.15 m/s) are unsourced. Keep them as hypotheses until Phase 1 baselines exist.
- Unverified claims to resolve:
  - "No built-in Nav2 MPPI critic uses tracked obstacle velocity". Check the critic list in the MPPI docs and GitHub.
  - Author lists for refs 2, 3 and 7 should be double-checked against the PDFs before final submission.
- The assessed proposal needs a risk register, Gantt chart and methodology (see `raw/proposals/proj_proposal_guide.md`). Sections 5–6 above are the seed for the "Specification" section.

