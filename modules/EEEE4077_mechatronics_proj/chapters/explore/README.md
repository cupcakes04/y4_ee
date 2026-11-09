# Exploratory Research Archive (Parked Tracks)

> **Context & Purpose**: This directory archives exploratory research prototypes, mathematical derivations, and conceptual paradigms that were investigated during project formulation but formally decoupled and parked outside the assessed MEng dissertation deliverables.
>
> The official assessed project specification (**`SD-MEng-26-01`**) commits **100% of the engineering effort to software simulation in Gazebo Harmonic** (HW 0% / SW 60% / Research 40%), focusing strictly on **Multi-Modal Dynamic Obstacle Tracking, Predictive MPPI Control, and Systematic 3-Way Comparative Ablation in ROS 2 Nav2**.

---

## Research Handover Packets (Pre-Research Briefs & Specs)

| File | Date | Status | Scope & Target Modules |
|---|---|---|---|
| [`20261108_fyp_core_research_brief.md`](./20261108_fyp_core_research_brief.md) | 2026-11-08 | **Outward Brief (Mode 1)** | End-to-end constraints, I/O schemas, and open research questions for O1 (`lidar_vision_tracker`), O2 (`nav2_mppi_dynamic_critic`), and costmap dynamic obstacle masking. |
| [`brief.md`](./brief.md) | 2026-11-08 | **Inward Synthesis (Mode 2 Ingested)** | External Deep Research literature synthesis on 2D LiDAR + monocular fusion (ABD breakpoint clustering, ByteTrack, CV vs CTRV) and O2 resolution spec (`/scan_static` masking & anisotropic MPPI critic). |

---

## Index of Parked Explorations

| File | Topic | Key Concepts Investigated | Rationale for Parking |
|---|---|---|---|
| [`01_vlm_hazard_distillation.md`](./01_vlm_hazard_distillation.md) | **Offline VLM Hazard Distillation** | `avp`, Florence-2, Grounded-SAM pseudo-labelling for non-geometric fluid spills ($Z \approx 0$). | Decoupled from critical path; permanent walls already use deterministic CAD masks under ISO 3691-4. |
| [`02_planar_ipm_homography.md`](./02_planar_ipm_homography.md) | **Planar IPM Homography & Nav2 Costmap Filters** | Analytical ground homography ($H^{-1}$), Douglas-Peucker polygon simplification, `CostmapFilterInfo`. | Highly sensitive to vehicle pitch variations; outside core dynamic obstacle focus of `SD-MEng-26-01`. |
| [`03_dynamic_philosophy_and_open_world.md`](./03_dynamic_philosophy_and_open_world.md) | **Dynamic Philosophy & Open-World Semantics** | Open-world cognitive representations, intent estimation, foundation-model world models. | Parked to eliminate academic fluff and focus on defensible, deterministic translational systems engineering. |

---

## Re-Integration Criteria
These tracks remain fully preserved for future reference, post-graduate research, or optional demonstration video recordings if the core deliverables (O1, O2, O3) are completed significantly ahead of schedule.
