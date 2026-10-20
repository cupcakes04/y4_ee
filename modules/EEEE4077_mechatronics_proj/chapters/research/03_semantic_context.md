# 3. Module 1: Semantic Context Distillation & Costmap Filtering

> **Scope & Track Notice**: This module records exploratory research into zero-shot visual hazard distillation (`avp`) as an independent extension to the core navigation framework. While the primary assessed FYP deliverables focus strictly on multi-modal dynamic obstacle tracking and predictive MPPI control (Supervisor Brief `SD-MEng-26-01`), this track explores future extensions to non-geometric surface hazards ($Z \approx 0$).

---

## 3.1 Objective
Enable rapid, zero-manual-annotation bootstrapping for site-specific non-geometric surface hazards ($Z=0$, fluid slicks, floor lane markings) and dynamic floor context using off-the-shelf vision-language foundation models, cleanly augmenting deterministic CAD base maps.

---

## 3.2 Offline Distillation Pipeline
1. **Video Ingestion:** Facility operators record a continuous walkthrough video of the operational environment (using a phone or handheld camera).
2. **Zero-Shot Auto-Labelling:** An offline pipeline prompts open-vocabulary foundation models (Florence-2 / Grounded-SAM) with domain-specific text prompts (e.g., `"forklift transit lane"`, `"oil slick"`, `"pallet staging zone"`).
3. **Pseudo-Label Curation:** Auto-generated segmentation masks are filtered, thresholded by confidence, and curated (using the `avp` tool UI).
4. **Student Distillation & Optimization:** The curated masks are used to fine-tune a lightweight student model (YOLOv8-Seg / YOLOv11-Seg), which is then compiled to TensorRT FP16 for edge inference.

---

## 3.3 Planar Ground-Plane Projection (Inverse Perspective Mapping)
Edge segmentation contours are projected onto the ground plane using planar Inverse Perspective Mapping (IPM) derived from camera intrinsics $K$ and extrinsics $[R \mid t]$:

$$\begin{bmatrix} X_w \\ Y_w \\ 1 \end{bmatrix} \sim H^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$

- Projected boundary polygons are converted into the global robot navigation frame (`map` or `odom`) via the ROS 2 TF2 transform tree.
- Polygons are simplified using the Douglas-Peucker algorithm to minimize vertex streaming overhead.

---

## 3.4 Nav2 Costmap Filter Integration
- Boundary polygons are published to ROS 2 `nav2_costmap_2d::CostmapFilterInfo` layers.
- The layers modulate local and global costmaps dynamically as:
  - **Keepout Zones:** Mark transient non-geometric hazards such as oil slicks, chemical spills, or temporary staging bays as non-traversable (cost = 254).
  - **Speed Restriction Zones:** Mark high-traffic corridors or forklift transit lanes with reduced maximum linear velocity limits.
- Dynamically augments standard static CAD maps with online perception of transient surface hazards, eliminating the need for manual bounding-box annotation during training while preserving deterministic CAD for permanent physical structures.
