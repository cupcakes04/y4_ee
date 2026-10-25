# Master Reference Register & Claim Audit

> **Single Source of Truth for Citations**: Derived documents (`abstract.md` and `project_proposal.md`) must only cite entries from this register. Keys (L1, L2, ...) are stable across all revisions.  
> **Status Key:**  
> - **V (Verified):** The primary paper, arXiv abstract, or publisher DOI page was directly opened and bibliographic data verified.  
> - **S (Summary/Secondary):** Found via secondary search summaries; confirm primary source prior to final submission.  
> - **T (Textbook/Standard):** Established canonical textbook or standard reference, unverified online.

---

## 1. Reference Register

| Key | Reference | Used For | Paper Card | Status | Scope Track |
|---|---|---|---|---|---|
| **L1** | P. Trautman and A. Krause, "Unfreezing the robot: Navigation in dense, interacting crowds," *IEEE/RSJ IROS*, 2010, pp. 797–803, doi:10.1109/IROS.2010.5654369 | Freezing robot problem formulation | [L01_trautman2010_unfreezing.md](./papers/L01_trautman2010_unfreezing.md) | S | **Core Deliverable** |
| **L2** | S. Macenski, F. Martín, R. White, J. Ginés Clavero, "The Marathon 2: A Navigation System," *IEEE/RSJ IROS*, 2020, arXiv:2003.00368 | Nav2 architecture & warehouse deployment | [L02_macenski2020_marathon2.md](./papers/L02_macenski2020_marathon2.md) | V | **Core Deliverable** |
| **L3** | S. Macenski et al., "From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in the Robot Operating System 2," *Robotics and Autonomous Systems*, 2023, arXiv:2307.15236 | ROS 2 Nav2 state of the art | [L03_macenski2023_ros2_survey.md](./papers/L03_macenski2023_ros2_survey.md) | V | **Core Deliverable** |
| **L4** | G. Williams et al., "Information theoretic MPC for model-based reinforcement learning," *IEEE ICRA*, 2017, pp. 1714–1721, doi:10.1109/ICRA.2017.7989202 | Mathematical foundations of MPPI control | [L04_williams2017_mppi.md](./papers/L04_williams2017_mppi.md) | S | **Core Deliverable** |
| **L5** | Q. Zhang and R. Pless, "Extrinsic calibration of a camera and laser range finder (improves camera calibration)," *IEEE/RSJ IROS*, 2004 | Camera–laser calibration algorithm | [L05_zhang2004_extrinsic_calibration.md](./papers/L05_zhang2004_extrinsic_calibration.md) | S | **Core Deliverable** |
| **L6** | B. Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," *CVPR*, 2024, arXiv:2311.06242 | Offline prompt-driven vision teacher model | [L06_xiao2024_florence2.md](./papers/L06_xiao2024_florence2.md) | V | *Archived in explore/* |
| **L7** | T. Ren et al., "Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks," arXiv:2401.14159, 2024 | Zero-shot prompt segmentation / auto-labelling | [L07_ren2024_grounded_sam.md](./papers/L07_ren2024_grounded_sam.md) | V | *Archived in explore/* |
| **L8** | "ViLAM: Distilling Vision-Language Reasoning into Attention Maps for Social Robot Navigation," arXiv:2503.09820, 2025 | VLM distillation into navigation maps | [L08_vilam2025_social_nav.md](./papers/L08_vilam2025_social_nav.md) | V | *Archived in explore/* |
| **L9** | International Federation of Robotics, "World Robotics 2025 – Service Robots" press release, 2025 | Commercial logistics AMR market scale | [L09_ifr2025_service_robots.md](./papers/L09_ifr2025_service_robots.md) | V | **Core Deliverable** |
| **L10** | Nav2 Documentation (Rolling): Navigating with Keepout Zones & Speed Limits | Technical basis for Costmap Filters | [L10_nav2_costmap_filters.md](./papers/L10_nav2_costmap_filters.md) | S | *Archived in explore/* |
| **L11** | Nav2 MPPI Controller Repository & Technical Documentation | MPPI batching, compute budget, and critic plugins | [L11_nav2_mppi_controller.md](./papers/L11_nav2_mppi_controller.md) | V | **Core Deliverable** |
| **L12** | S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005 | Motion models (CV, CTRV) and Kalman filtering | [L12_thrun2005_probabilistic_robotics.md](./papers/L12_thrun2005_probabilistic_robotics.md) | T | **Core Deliverable** |
| **L13** | Y. Zhang et al., "ByteTrack: Multi-Object Tracking by Associating Every Detection Box," *ECCV*, 2022, arXiv:2110.06864 | 2D multi-object tracking & data association | [L13_zhang2022_bytetrack.md](./papers/L13_zhang2022_bytetrack.md) | V | **Core Deliverable** |
| **L14** | D. Helbing and P. Molnar, "Social force model for pedestrian dynamics," *Physical Review E*, 1995, doi:10.1103/PhysRevE.51.4282 | Pedestrian dynamics & nominal velocity modeling | [L14_helbing1995_social_force.md](./papers/L14_helbing1995_social_force.md) | V | **Core Deliverable** |
| **L15** | J. M. Kang, "SE-MPPI: Safe-Escape Nav2-Native MPPI Controller with Control Barrier Functions," GitHub / Preprint, 2024 | CBF safety filter & local minima escape in Nav2 | [L15_kang2024_se_mppi.md](./papers/L15_kang2024_se_mppi.md) | S | *Comparative Literature* |
| **L16** | C. Peng et al., "EXACT-MPPI: Exact Signed-Distance Navigation for Arbitrary-Footprint Robots from Point Clouds," GitHub / Preprint, 2024 | Exact non-convex footprint SDF & JAX GPU rollouts | [L16_peng2024_exact_mppi.md](./papers/L16_peng2024_exact_mppi.md) | S | *Comparative Literature* |
| **L17** | RCILab, "Constrained Sampling MPPI Framework with DBSCAN for Reliable Obstacle Avoidance," *IEEE/RSJ IROS*, 2025 | Rollout DBSCAN clustering & primal-dual MPPI | [L17_rcilab2025_csc_mppi.md](./papers/L17_rcilab2025_csc_mppi.md) | S | *Comparative Literature* |

---

## 2. Claim Audit Matrix

| Project Claim | Literature Verdict & Status | Action Required |
|---|---|---|
| "Late-fusion 2D LiDAR + monocular vision is mathematically well documented" | Grounded in calibration (L5) and state estimation (L12). Frustum ray gating connects image bounding boxes to planar range. | Verified foundation. |
| "Default Nav2 MPPI critics evaluate static obstacle distances only" | **Confirmed by inspection of Nav2 `critics/` source tree.** All 11 shipped critics evaluate 2D costmaps at $t=0$, lacking temporal forward projection. | Validated gap for Module 2 contribution. |
| "Static 2D costmaps cause controller freezing around moving agents" | Grounded in Trautman & Krause (L1). Static costmap marking causes path invalidation and emergency halts. | Validated problem statement. |
| "Constant velocity motion modeling is valid over short horizons (T ≤ 2.0s)" | Grounded in Helbing & Molnar (L14) and Thrun et al. (L12). Pedestrian velocity vectors are predominantly unaccelerated over 1–2 second intervals. | Validated design choice. |
| "Ablation study isolates visual detection from motion prediction" | Explicitly requested by supervisor specification (`SD-MEng-26-01`). Realized via C0 (LiDAR only), C1 (Vision detection without prediction), and C2 (Full prediction). | Validated evaluation design. |
| "Advanced MPPI paradigms (CBF, continuous SDF, clustering) address orthogonal failure modes to semantic late-fusion" | Grounded in SE-MPPI (L15), EXACT-MPPI (L16), and CSC-MPPI (L17). They solve analytical safety boundaries, arbitrary footprints, and mode averaging, but assume dense 3D point clouds or known obstacle states on GPU runtimes. | Validates our focus on low-cost brownfield CPU Nav2 C++ plugin integration. |

---

## 3. Primary-Source Action Items Before Final Submission
1. **L1, L4, L5:** Re-verify exact IEEE Xplore page ranges and DOIs prior to final dissertation binding.
2. **L14:** Confirmed (Phys. Rev. E, vol. 51, no. 5, pp. 4282–4286).
