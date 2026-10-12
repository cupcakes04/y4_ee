# 3. Module 1: Semantic Context Distillation & Costmap Filtering

## 3.1 Objective
Enable rapid, zero-manual-CAD adaptation to site-specific floor context and non-geometric hazards using off-the-shelf vision-language foundation models.

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
  - **Keepout Zones:** Mark areas such as oil slicks, chemical spills, or temporary staging bays as non-traversable (cost = 254).
  - **Speed Restriction Zones:** Mark high-traffic corridors or forklift transit lanes with reduced maximum linear velocity limits.
- Eliminates manual drafting of CAD keepout vectors, reducing reconfiguration from hours to under 30 minutes.
