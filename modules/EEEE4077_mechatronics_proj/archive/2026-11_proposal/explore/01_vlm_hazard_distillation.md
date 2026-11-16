# Exploratory Track 01: Offline VLM Hazard Distillation Pipeline

> **Archive Status**: EXPLORATORY PROTOTYPE / PARKED OUTSIDE ASSESSED SCOPE.  
> **Original Prototype**: [`avp` (Automated Video Dataset Labelling and Annotation Pipeline)](https://github.com/cupcakes04/avp).  
> **Associated Literature**: Florence-2 (Xiao et al., 2024), Grounded-SAM (Ren et al., 2024), ViLAM (2025).

---

## 1. Context & Motivation

Commercial logistics facilities frequently encounter transient surface hazards—such as hydraulic fluid leaks, standing water, chemical spills, or temporary staging zones—that possess no measurable physical elevation ($Z \approx 0$). Traditional Time-of-Flight range sensors (2D/3D LiDAR) either fail to detect fluid pooling due to specular reflection or classify the ground plane as flat traversable space.

Manually curating and bounding thousands of image frames for custom industrial hazards is prohibitively expensive for small-scale robotics deployments. This exploratory track investigated an **offline teacher-student distillation workflow** designed to automate semantic dataset bootstrapping without human manual polygon drawing.

---

## 2. Technical Architecture: Teacher-Student Distillation

```
                     Walkthrough Video Stream (.mp4)
                                  │
                                  ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │ Offline Teacher Pipeline (Workstation GPU: RTX 4070 Ti Super)    │
 │                                                                 │
 │   1. Open-Vocabulary Prompting:                                 │
 │      "fluid spill", "chemical slick", "forklift transit lane"   │
 │   2. Florence-2 (Coarse Bounding Box Generation)                │
 │   3. Grounded-SAM (Zero-Shot Pixel-Level Mask Segmentation)     │
 │   4. Confidence Thresholding & Automated Mask Filtering         │
 └────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼ Pseudo-Label Masks
 ┌─────────────────────────────────────────────────────────────────┐
 │ Human-in-the-Loop Quality Gate (`avp` UI)                       │
 │   - Visual verification of pseudo-labels                        │
 │   - Rapid rejection of hallucinated masks (<5% curation time)   │
 └────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼ Curated Training Set
 ┌─────────────────────────────────────────────────────────────────┐
 │ Student Model Fine-Tuning & Deployment Optimization             │
 │   - Architecture: YOLOv8-Seg / YOLOv11-Seg (Nano profile)       │
 │   - Target: Lightweight real-time edge segmentation (>30 FPS)   │
 │   - Optimization: TensorRT FP16 / INT8 engine compilation       │
 └─────────────────────────────────────────────────────────────────┘
```

---

## 3. Why This Track Was Parked Outside the Core FYP

1. **Alignment with Supervisor Specification (`SD-MEng-26-01`):**  
   The official project brief defines the research effort strictly around:
   - HW: 0%, SW: 60%, Research: 40%.
   - Multi-Modal Obstacle Tracking, Predictive MPPI Control, and Systematic Comparative Ablation in ROS 2 Nav2.
   - Non-geometric floor hazard segmentation is outside the scope agreed with the supervisory team.
2. **Deterministic Industry Reality (CAD vs. AI):**  
   For structural infrastructure and static walls, industrial AMRs certified under ISO 3691-4 require 100% deterministic, safety-certified CAD vector keepout zones. Hand-drawing static keepouts takes minutes and has zero hallucination risk. Using foundation models for general site mapping is an industrial anti-pattern.
3. **Engineering Critical Path Protection:**  
   Focusing the available 450 project hours on delivering a rock-solid C++ Nav2 dynamic obstacle critic and robust 2D LiDAR + monocular tracking pipeline is far more valuable and defensible than chasing speculative VLM auto-annotation pipelines.
