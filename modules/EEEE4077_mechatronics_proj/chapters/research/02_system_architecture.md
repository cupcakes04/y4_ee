# 2. System Architecture & Information Flow

The architecture enforces strict decoupling between high-capacity, zero-shot foundation models (offline/setup) and low-latency, deterministic execution on the edge robot (online runtime).

---

## 2.1 End-to-End Information Flow Diagram

```
                             OFFLINE / ZERO-SHOT SETUP
  [Walkthrough Video] + [Text Prompts] ──► [VLM / Teacher Model (Florence-2 / SAM)]
                                                            │
                                                            ▼ Auto-Generated Pseudo-Labels
                                               [Distillation & Quantization]
                                                            │
════════════════════════════════════════════════════════════╪═════════════════════════════════
                                   ON-ROBOT RUNTIME         ▼
                                              [TensorRT Edge Model: YOLO-Seg]
                                                            │
                       ┌────────────────────────────────────┴───────────────────────────┐
                       ▼ Dynamic Agent BBoxes                                           ▼ Floor Hazard / Lane Masks
 [RGB Camera] ──► [Extrinsic Calib]                                                     │
                       │                                                                ▼
 [2D LiDAR]   ──► [Ray Gating & Depth Association]                             [Planar Homography (IPM)]
                       │                                                                │
                       ▼ Filtered Metric Clusters                                       ▼ Geometry Polygons
              [Multi-Target CTRV / CV EKF]                                     [Nav2 Costmap Filters]
                       │                                                       (Keepout / Speed Limit Zones)
                       ▼ Dynamic States [x, y, vx, vy, ψ]                               │
              [Nav2 MPPI Dynamic Obstacle Critic]                                       ▼
                       │                                                      [Nav2 Local Costmap]
                       └────────────────────────────────────┬───────────────────────────┘
                                                            ▼
                                                [cmd_vel (Base Actuation)]
```

---

## 2.2 Operational Decoupling Rationale

1. **Safety Loop Determinism:**
   - Foundation models (Florence-2, Grounded-SAM) possess high representational capacity but exhibit inference times $>500\text{ ms}$, unsuitable for the $\ge 20\text{ Hz}$ control loops required by AMR safety and trajectory generation.
   - Restricting foundation models to the offline setup stage yields sub-millisecond deterministic inference via TensorRT on edge hardware.
2. **Deterministic Geometry & Kinetics:**
   - Instead of learning an end-to-end black-box navigation policy, semantic outputs interface directly with standard, predictable ROS 2 components: Nav2 Costmap Filters (`CostmapFilterInfo`) and Model Predictive Path Integral control (`nav2_mppi_controller`).
