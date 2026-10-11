### 1. Has Sensor Fusion Already Been Done? Yes, and That Is an Advantage

The core mechanics of **late-fusion 2D LiDAR + monocular vision** are well-documented:

* Camera-LiDAR calibration (Zhang & Pless planar checkerboard methods).
* Frustum bounding box association ($u_{\min}$ to $u_{\max}$ horizontal ray gating).
* Kalman Filter (EKF/UKF) tracking using Constant Velocity (CV) or Constant Turn Rate and Velocity (CTRV) models.

Trying to invent a completely novel low-level fusion algorithm at the undergraduate level often results in messy edge cases. Because this sensor pairing is already grounded in literature, your engineering contribution is **modular integration**: taking reliable open-source methods, packaging them into clean ROS 2 Humble/Iron packages, and anchoring them into a practical pipeline.

---

### 2. Is Distilling VLMs for Edge Navigation Grounded in Literature?

Yes, this is an active and prominent research frontier in robotics. Recent academic literature validates your proposed workflow:

* **Foundation Models for Costmap & Path Adaptation**:
* *ViLAM (2025/2026)* and related works demonstrate distilling large VLMs into lightweight attention/costmap features for local navigation planners, eliminating the need to query slow foundation models directly on the robot.
* *Grounded-SAM / Florence-2 / MobileSAM*: Research in robotic zero-shot instance segmentation shows that large vision-language models can automatically annotate unlabelled spatial data (crops, indoor corridors, industrial obstacles) via text prompts.


* **Open-Vocabulary 3D/2D Scene Representation**:
* Papers on *VLM-to-Edge Distillation* demonstrate running heavy models (like SAM or GPT-4o) offline on site-survey videos to produce pseudo-ground-truth labels, which are then used to train lean edge networks (like YOLO-Seg) that execute on low-power Jetson hardware at 30+ FPS.



---

### 3. Where Most Literature Stops vs. Where Your FYP Fits

While recent literature proves that VLM distillation works, academic papers usually test it in narrow, idealized settings (e.g., social etiquette in university hallways or broad object recognition in clean labs).

They leave a major engineering gap that aligns directly with your brownfield AMR scope:

| What Existing VLM Robotics Papers Do | What Your Project Delivers (The Practical Contribution) |
| --- | --- |
| Focus on abstract benchmarks or high-end 3D LiDAR/RGB-D rigs. | **Target low-cost, legacy 2D LiDAR AMRs** that cannot afford 3D sensors or complex compute. |
| Output high-latency semantic maps or abstract neural navigation policies. | **Direct integration into deterministic ROS 2 Nav2 Costmap Filters** and the `nav2_mppi_controller` critic stack. |
| Assume greenfield conditions with clear object classes. | **Solve brownfield floor ambiguity**: quickly prompting for site-specific, non-geometric hazards (oil spills, temporary staging boxes, forklift transit boundaries) via zero-shot prompt pipelines. |

---

### 4. How to Frame This in Your Literature Review Chapter

Structure the Literature Review section of your proposal into three clean pillars:

1. **Sensor Fusion & Dynamic Tracking (The Baseline)**: Cite classic 2D LiDAR + Camera calibration (Zhang & Pless) and multi-target tracking (ByteTrack + EKF). Conclude that while late-fusion ranging is mathematically solved, it traditionally relies on static class detectors (like standard COCO YOLO) that cannot adapt to new industrial objects without manual annotation.
2. **Foundation Models & Distillation in Robotics (The Enabler)**: Cite recent works utilizing VLMs (Florence-2, Grounded-SAM, ViLAM) for prompt-driven robotic context. Point out the computational bottleneck: large models are too heavy for real-time edge control on low-cost hardware ($<5\text{ FPS}$), necessitating offline distillation into edge engines (YOLOv8/v11-Seg via TensorRT).
3. **Semantic Costmaps & Nav2 Control (The Downstream Consumer)**: Discuss traditional 2D occupancy grids vs. Nav2 Costmap Filters (Keepout and Speed Zones). Highlight that CAD-drawn keepouts are brittle, and your pipeline automates planar floor affordance using homography directly from the distilled edge segmenter.



---

## 5. Reference register (verified status, last checked 2026-10-11)

> This section is the **single list of citable sources**. `abstract.md` and `project_proposal.md` must only cite entries from here. Keys (L1, L2, ...) are stable. The submission renumbers them in order of first appearance.
> Status key: **V** = the source page or abstract was opened and the bibliographic data matched. **S** = found only through a search summary, so open the primary source before submission. **T** = textbook or well-known work, not opened.

| Key | Reference | Used for | Status |
|---|---|---|---|
| L1 | P. Trautman and A. Krause, "Unfreezing the robot: Navigation in dense, interacting crowds," *IEEE/RSJ IROS*, 2010, pp. 797–803, doi:10.1109/IROS.2010.5654369 | The "freezing robot problem" | S (bibliographic data confirmed by search only) |
| L2 | S. Macenski, F. Martín, R. White, J. Ginés Clavero, "The Marathon 2: A Navigation System," *IEEE/RSJ IROS*, 2020, arXiv:2003.00368 | Nav2 architecture, warehouse and pedestrian context | V (arXiv abstract opened) |
| L3 | S. Macenski et al., "From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in the Robot Operating System 2," *Robotics and Autonomous Systems*, 2023, arXiv:2307.15236 | Nav2 state of the art, controller and costmap background | V (arXiv abstract opened) |
| L4 | G. Williams et al., "Information theoretic MPC for model-based reinforcement learning," *IEEE ICRA*, 2017, pp. 1714–1721, doi:10.1109/ICRA.2017.7989202 | Theory behind MPPI | S |
| L5 | Q. Zhang and R. Pless, "Extrinsic calibration of a camera and laser range finder (improves camera calibration)," *IEEE/RSJ IROS*, 2004 | Camera–laser calibration | S |
| L6 | B. Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," *CVPR*, 2024, arXiv:2311.06242 | Prompt-driven teacher model | V (arXiv abstract opened). Check the author list. |
| L7 | T. Ren et al., "Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks," arXiv:2401.14159, 2024 | Prompt-driven segmentation / auto-labelling | V (arXiv abstract opened). Check the author list. |
| L8 | "ViLAM: Distilling Vision-Language Reasoning into Attention Maps for Social Robot Navigation," arXiv:2503.09820, 2025 | Prior VLM→edge distillation for navigation costmaps | V (arXiv abstract opened). Add the authors. |
| L9 | International Federation of Robotics, "World Robotics 2025 – Service Robots" press release, <https://ifr.org/ifr-press-releases/news/service-robots-see-global-growth-boom> | Commercial context. Transport and logistics was the top professional-service-robot application in 2024, with 102,900 units (+14%). | V (page opened) |
| L10 | Nav2 docs (rolling): MPPI Controller; Navigating with Keepout Zones; Navigating with Speed Limits; Using Collision Monitor (URLs in `abstract.md` §8) | Existence of MPPI, keepout/speed filters and Collision Monitor | S (the pages exist and the titles match, but the body text could not be retrieved) |
| L11 | Nav2 MPPI controller README, <https://github.com/ros-navigation/navigation2/tree/main/nav2_mppi_controller> | MPPI is plugin-based. Defaults: batch 1000, 56 steps × 0.05 s = 2.8 s horizon. Measured at 50+ Hz on a 4th-gen i5. | V (README opened) |
| L12 | S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005 | EKF / motion models (CV, CTRV) | T |

### Primary-source gaps to close
- L1, L4 and L5: open the primary publisher or DOI page and confirm.
- ROS 2 distro dates. A secondary summary says Iron reached EOL in Dec 2024, Humble reaches EOL on 2027-05-31 and Jazzy on 2029-05-31. `docs.ros.org` blocked the fetch. Add a verified reference (REP-2000 / the distributions page) before relying on it.
- Pedestrian walking speed (about 1.2–1.4 m/s) is used to justify the 0.15 m/s velocity RMSE target. It has no citation yet.
- Cost gap between 2D and 3D LiDAR: a search summary suggests about US\$380–500 for a Slamtec RPLIDAR S2 and thousands of US dollars for a multi-channel 3D sensor. The sources were retail pages, not opened. Keep this qualitative until verified.

---

## 6. Claim audit

| Claim in the notes above | Verdict |
|---|---|
| "Late-fusion 2D LiDAR + monocular vision is well documented" (§1) | Supported only by the Zhang & Pless calibration (L5, S). The frustum-gating and EKF-tracking claims have **no citation yet**. L12 gives the EKF basis. Add one 2D-LiDAR–camera fusion paper. |
| "Papers on VLM-to-Edge distillation ... 30+ FPS on Jetson" (§2) | **Unsupported.** No paper was identified. Either find one or drop the 30+ FPS statement. |
| "ViLAM (2025/2026)" (§2) | The paper is arXiv:2503.09820 (2025). It targets **social navigation** and distils into **attention maps** for a learned navigation policy. It does not use YOLO-Seg or Nav2 Costmap Filters. This strengthens the gap argument, but don't describe it as closely matching your pipeline. |
| "ByteTrack + EKF" (§4) | ByteTrack is not in the register. Add it only if used. |
| "Large models are too heavy (<5 FPS)" (§4, pillar 2) | Plausible but **unsourced**. Replace it with a measured benchmark on your own GPU. |
| "No built-in Nav2 MPPI critic consumes tracked obstacle velocity" | **Supported by inspection**, narrowly. The `critics/` directory on `main` holds 11 headers: constraint, cost, goal_angle, goal, obstacles, path_align, path_angle, path_follow, prefer_forward, twirling, velocity_deadband. None is named for predicted dynamic obstacles. Behaviour was inferred from the names, and the source was not read. |

### Positioning for the literature review (updated)
1. **Fusion and tracking baseline**: calibration (L5), EKF and motion models (L12). *Gap:* class sets are fixed and the output isn't wired into Nav2.
2. **Foundation models and distillation**: L6, L7, L8. *Gap:* they target social navigation or richer sensors, not site-specific floor hazards through standard Nav2 components. The edge-FPS claim needs evidence.
3. **Nav2 as the consumer**: L2, L3, L10, L11. *Gap:* the MPPI critics shipped today don't use obstacle velocity. Keepout masks are separate, static inputs.
4. **Why it matters commercially**: L9. Transport and logistics is the largest professional-service-robot application by units.