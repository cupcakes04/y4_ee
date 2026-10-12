# Originality & Positioning

## 1. Dimensions of Originality

1. **Translation Across Domains:**
   - Foundation-model auto-labelling and distillation (Florence-2, Grounded-SAM, ViLAM) has previously been restricted to social-navigation etiquette or rich 3D sensor rigs in research labs.
   - This project translates these techniques to **cost-constrained 2D LiDAR AMRs in brownfield industrial environments**, interfacing directly with standard ROS 2 Nav2 costmaps.
2. **Algorithmic Technique & Integration:**
   - Development of a **velocity-aware dynamic obstacle critic** for `nav2_mppi_controller`.
   - The 11 standard critics currently shipped in ROS 2 Nav2 evaluate obstacles statically without forward velocity propagation.
3. **Low-Cost Commercial Focus:**
   - Avoids expensive 3D LiDAR ($>\$3,000$) or heavy compute clusters. Operates on a standard planar LiDAR, single monocular camera, and consumer/embedded GPU, targeting mid-tier industrial logistics.
4. **Process Originality (Prompt-to-Deploy):**
   - The primary contribution includes the *process*: eliminating manual CAD engineering through zero-shot prompt distillation, with deployment wall-clock time rigorously benchmarked as an explicit metric ($<30\text{ min}$).

---

## 2. Comparison with Current Practice

| Capability | Current Industrial Practice | Academic Research SOTA | This FYP Project |
|---|---|---|---|
| **Dynamic Obstacle Avoidance** | Emergency stop / recovery rotate (freezing) | Heavy 3D voxel / learned end-to-end RL | 2D LiDAR + camera frustum EKF → MPPI proactive deflection |
| **Zone Management** | Manual CAD drafting of keepouts | 3D neural radiance fields / high-latency VLMs | Prompt-to-edge distillation → planar homography Nav2 filters |
| **Sensor Cost** | \$400 (2D LiDAR only) | \$4,000–\$10,000 (3D LiDAR + Depth arrays) | \$450–\$600 (2D LiDAR + monocular camera) |
| **Setup Time** | Days / Weeks per site layout shift | N/A (trained on fixed datasets) | $<30$ minutes from walkthrough video |

---

## 3. Acknowledged Limitations & Quantified Constraints

- **Simulation-First Baseline:** Scripted actors in Gazebo follow deterministic trajectories that lack the natural stochasticity of human crowds. Randomised timing and speed variations mitigate this, and real-video validation in O3 grounds visual testing in reality.
- **Planar Geometry Assumption:** The monocular homography projection assumes flat warehouse floors; deviations in surface pitch or slope introduce projection errors that must be bounded.
- **LiDAR Plane Dependency:** Target depth anchoring relies on objects intersecting the planar LiDAR height. Objects outside the scan plane cannot be metric-anchored without secondary geometric assumptions.
