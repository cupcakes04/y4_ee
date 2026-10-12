# Master Reference Register & Claim Audit

> **Single Source of Truth for Citations**: Derived documents (`abstract.md` and `project_proposal.md`) must only cite entries from this register. Keys (L1, L2, ...) are stable across all revisions.  
> **Status Key:**  
> - **V (Verified):** The primary paper, arXiv abstract, or publisher DOI page was directly opened and bibliographic data verified.  
> - **S (Summary/Secondary):** Found via secondary search summaries; confirm primary source prior to final submission.  
> - **T (Textbook/Standard):** Established canonical textbook or standard reference, unverified online.

---

## 1. Reference Register

| Key | Reference | Used For | Paper Card | Status |
|---|---|---|---|---|
| **L1** | P. Trautman and A. Krause, "Unfreezing the robot: Navigation in dense, interacting crowds," *IEEE/RSJ IROS*, 2010, pp. 797–803, doi:10.1109/IROS.2010.5654369 | Freezing robot problem formulation | [L01_trautman2010_unfreezing.md](./papers/L01_trautman2010_unfreezing.md) | S |
| **L2** | S. Macenski, F. Martín, R. White, J. Ginés Clavero, "The Marathon 2: A Navigation System," *IEEE/RSJ IROS*, 2020, arXiv:2003.00368 | Nav2 architecture & warehouse deployment | [L02_macenski2020_marathon2.md](./papers/L02_macenski2020_marathon2.md) | V |
| **L3** | S. Macenski et al., "From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in the Robot Operating System 2," *Robotics and Autonomous Systems*, 2023, arXiv:2307.15236 | ROS 2 Nav2 state of the art | [L03_macenski2023_ros2_survey.md](./papers/L03_macenski2023_ros2_survey.md) | V |
| **L4** | G. Williams et al., "Information theoretic MPC for model-based reinforcement learning," *IEEE ICRA*, 2017, pp. 1714–1721, doi:10.1109/ICRA.2017.7989202 | Mathematical foundations of MPPI control | [L04_williams2017_mppi.md](./papers/L04_williams2017_mppi.md) | S |
| **L5** | Q. Zhang and R. Pless, "Extrinsic calibration of a camera and laser range finder (improves camera calibration)," *IEEE/RSJ IROS*, 2004 | Camera–laser calibration algorithm | [L05_zhang2004_extrinsic_calibration.md](./papers/L05_zhang2004_extrinsic_calibration.md) | S |
| **L6** | B. Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," *CVPR*, 2024, arXiv:2311.06242 | Offline prompt-driven vision teacher model | [L06_xiao2024_florence2.md](./papers/L06_xiao2024_florence2.md) | V |
| **L7** | T. Ren et al., "Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks," arXiv:2401.14159, 2024 | Zero-shot prompt segmentation / auto-labelling | [L07_ren2024_grounded_sam.md](./papers/L07_ren2024_grounded_sam.md) | V |
| **L8** | "ViLAM: Distilling Vision-Language Reasoning into Attention Maps for Social Robot Navigation," arXiv:2503.09820, 2025 | VLM distillation into navigation maps | [L08_vilam2025_social_nav.md](./papers/L08_vilam2025_social_nav.md) | V |
| **L9** | International Federation of Robotics, "World Robotics 2025 – Service Robots" press release, 2025 | Commercial logistics AMR market scale | [L09_ifr2025_service_robots.md](./papers/L09_ifr2025_service_robots.md) | V |
| **L10** | Nav2 Documentation (Rolling): Navigating with Keepout Zones & Speed Limits | Technical basis for Costmap Filters | [L10_nav2_costmap_filters.md](./papers/L10_nav2_costmap_filters.md) | S |
| **L11** | Nav2 MPPI Controller Repository & Technical Documentation | MPPI batching, compute budget, and critic plugins | [L11_nav2_mppi_controller.md](./papers/L11_nav2_mppi_controller.md) | V |
| **L12** | S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005 | Motion models (CV, CTRV) and Kalman filtering | [L12_thrun2005_probabilistic_robotics.md](./papers/L12_thrun2005_probabilistic_robotics.md) | T |
| **L13** | Y. Zhang et al., "ByteTrack: Multi-Object Tracking by Associating Every Detection Box," *ECCV*, 2022, arXiv:2110.06864 | 2D multi-object tracking & data association | [L13_zhang2022_bytetrack.md](./papers/L13_zhang2022_bytetrack.md) | V |

---

## 2. Claim Audit Matrix

| Project Claim | Literature Verdict & Status | Action Required |
|---|---|---|
| "Late-fusion 2D LiDAR + monocular vision is mathematically well documented" | Grounded in calibration (L5) and state estimation (L12). Frustum ray gating lacks an explicit 2D-LiDAR paper citation. | Add one explicit late-fusion 2D LiDAR + camera paper. |
| "Papers demonstrate VLM-to-Edge distillation at 30+ FPS on Jetson" | **Unsupported.** No paper directly confirms 30+ FPS for full VLM distillation on Jetson Orin Nano. | Recalibrate claim: state that YOLO-Seg runs at 30+ FPS, and measure custom TensorRT FPS empirically. |
| "ViLAM demonstrates VLM distillation for navigation" | Supported by L8 (arXiv:2503.09820). However, ViLAM distils into attention maps for social navigation, NOT planar Nav2 Costmap Filters. | Use as evidence of research frontier while positioning Nav2 integration as the distinct engineering gap. |
| "No built-in Nav2 MPPI critic consumes tracked obstacle velocity" | **Confirmed by inspection of Nav2 `critics/` source tree.** The 11 shipped critics evaluate static obstacle distances only. | Validated gap for Module 3 contribution. |
| "Large VLMs are too computationally expensive for AMR control (<5 FPS)" | Empirically consistent with Florence-2 / SAM edge profiles, but lacks a peer-reviewed edge benchmark citation. | Soften to qualitative statement or verify via local benchmark script. |

---

## 3. Primary-Source Action Items Before Final Submission
1. **L1, L4, L5:** Open primary IEEE Xplore / DOI links and confirm full citation metadata.
2. **Pedestrian Velocity Citation:** Add primary reference for nominal human walking speed ($1.2–1.4\text{ m/s}$) to justify velocity error tolerance.
3. **Hardware Pricing Benchmark:** Confirm commercial pricing ranges for 2D vs 3D LiDAR scanners from distributor documentation.
