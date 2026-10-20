# Originality & Positioning

## 1. Dimensions of Originality

1. **Translation Across Domains:**
   - Foundation-model auto-labelling and distillation (Florence-2, Grounded-SAM, ViLAM) has previously been restricted to social-navigation etiquette or rich 3D sensor rigs in research labs.
   - This project translates these techniques to **cost-constrained 2D LiDAR AMRs in brownfield industrial environments**, interfacing directly with standard ROS 2 Nav2 costmaps.
2. **Algorithmic Technique & Integration:**
   - Development of a **velocity-aware dynamic obstacle critic** for `nav2_mppi_controller` via native `pluginlib`.
   - The 11 standard critics currently shipped in ROS 2 Nav2 evaluate obstacles statically against 2D costmaps without forward velocity propagation.
3. **Low-Cost Commercial Focus:**
   - Avoids expensive 3D LiDAR ($>\$3,000$) or heavy compute clusters. Operates on a standard planar LiDAR, single monocular camera, and consumer/embedded GPU, targeting mid-tier industrial logistics.
4. **Process Originality (Prompt-to-Deploy):**
   - The primary process contribution is **zero-annotation bootstrapping**: training lightweight edge detectors for novel, site-specific non-geometric surface hazards (fluid slicks, floor lane tape) via zero-shot prompt distillation, eliminating manual bounding-box annotation with setup time benchmarked as an explicit metric ($<30\text{ min}$).

---

## 2. Comparison with Current Practice

| Capability | Current Industrial Practice | Academic Research SOTA | This FYP Project |
|---|---|---|---|
| **Dynamic Obstacle Avoidance** | Emergency stop / recovery rotate (freezing) | Heavy 3D voxel / learned end-to-end RL | 2D LiDAR + camera frustum EKF → MPPI proactive deflection |
| **Hazard & Zone Management** | Manual CAD for static walls; blind to transient $Z=0$ fluid spills | 3D neural radiance fields / high-latency VLMs | Deterministic CAD for walls + prompt-distilled edge IPM for transient $Z=0$ spills |
| **Sensor Cost** | \$400 (2D LiDAR only) | \$4,000–\$10,000 (3D LiDAR + Depth arrays) | \$450–\$600 (2D LiDAR + monocular camera) |
| **Hazard Model Bootstrapping** | Manual bounding-box annotation (days/weeks per class) | N/A (trained on fixed static datasets) | $<30$ minutes from walkthrough video via prompt distillation |

---

## 3. Acknowledged Limitations & Quantified Constraints

- **Simulation-First Baseline:** Scripted actors in Gazebo follow deterministic trajectories that lack the natural stochasticity of human crowds. Randomised timing and speed variations mitigate this, and real-video validation in O3 grounds visual testing in reality.
- **Planar Geometry Assumption:** The monocular homography projection assumes flat warehouse floors; deviations in surface pitch or slope introduce projection errors that must be bounded.
- **LiDAR Plane Dependency:** Target depth anchoring relies on objects intersecting the planar LiDAR height. Objects outside the scan plane cannot be metric-anchored without secondary geometric assumptions.
- **Scope of Visual Costmaps vs. Deterministic Safety:** Deterministic CAD keepout zones remain the certified standard for permanent structural infrastructure (ISO 3691-4). Visual costmap filters via IPM are deliberately scoped to augment CAD by detecting transient, non-geometric surface hazards ($Z=0$) where physical LiDAR fails.
