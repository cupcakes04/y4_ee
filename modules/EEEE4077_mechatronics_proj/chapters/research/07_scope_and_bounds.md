# 7. Strategic Scope & Methodological Boundaries

## 7.1 Architectural Principles

1. **Decoupling Foundation Models from the Safety Loop:**
   - Running heavy VLMs (e.g., full SAM or multimodal LLMs) directly on an AMR edge computer introduces unacceptable latency ($>500\text{ ms}$).
   - Limiting foundation models to an offline pseudo-labeling role preserves deterministic sub-30ms control loops on the physical robot.
2. **Mutual Sensor Augmentation over Standalone Perception:**
   - Pure monocular visual depth suffers from scale drift and optical noise.
   - 2D LiDAR suffers from identity loss and semantic blindness.
   - Pairing them as mutual anchors (vision provides identity and angle; 2D LiDAR provides ground-truth metric scale) achieves high-fidelity dynamic tracking at minimal sensor cost.
3. **Planar Costmap Filters vs. 3D Voxel Reconstruction:**
   - Industrial warehouse floors are predominantly planar surfaces.
   - Projecting segmented visual boundaries directly into 2D Costmap Filters via homography eliminates the high compute and memory overhead of 3D voxel back-projection, maintaining high frame rates on constrained edge compute.

---

## 7.2 Explicit Non-Goals (Out of Scope)

To ensure high technical depth and on-time completion, the following areas are strictly out of scope:
- **Fleet Management & Multi-Robot Coordination:** Single-robot navigation only.
- **SLAM & Novel Localization Research:** Standard SLAM / Cartographer / AMCL stacks are used as black-box utilities.
- **Running Foundation Models Directly on the Robot:** Foundation models run strictly offline.
- **Full 3D Volumetric Scene Reconstruction:** The pipeline adheres strictly to planar representations.
- **Formal Functional Safety Certification (ISO 3691-4 / ISO 13849):** The research is an experimental demonstration; existing low-level hardware safety stops remain untouched.
