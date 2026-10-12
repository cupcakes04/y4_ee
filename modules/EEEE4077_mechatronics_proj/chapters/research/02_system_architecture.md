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
          [2D MOT: ByteTrack (BoxMOT)]                                                  │
                       │ Persistent Track IDs                                           ▼
 [RGB Camera] ──► [Extrinsic Calib]                                            [Planar Homography (IPM)]
                       │                                                                │
 [2D LiDAR]   ──► [Ray Gating & Depth Association]                                      ▼ Geometry Polygons
                       │ Metric (X, Y) per Track ID                            [Nav2 Costmap Filters]
          [Per-Track Linear Kalman Filter (CV)]                                (Keepout / Speed Limit Zones)
                       │                                                                │
                       ▼ Dynamic States [x, y, vx, vy] per Track ID                     ▼
              [Nav2 MPPI Dynamic Obstacle Critic]                              [Nav2 Local Costmap]
                       │                                                                │
                       └────────────────────────────────────┬───────────────────────────┘
                                                            ▼
                                                [cmd_vel (Base Actuation)]
```

---

## 2.2 Operational Decoupling Rationale

1. **Safety Loop Determinism:**
   - Foundation models (Florence-2, Grounded-SAM) possess high representational capacity but exhibit inference times $>500\text{ ms}$, unsuitable for the $\ge 20\text{ Hz}$ control loops required by AMR safety and trajectory generation.
   - Restricting foundation models to the offline setup stage yields sub-millisecond deterministic inference via TensorRT on edge hardware.
2. **Decoupled 2D Vision Tracking & Metric Filtering:**
   - 2D multi-object tracking (ByteTrack) runs in image space to handle data association, occlusion recovery, and persistent identity management.
   - Planar 2D LiDAR ray gating provides unambiguous metric depth without stereo/depth camera overhead.
   - A per-track linear Kalman filter estimates smooth metric velocities $(v_x, v_y)$ without requiring complex combinatorial metric data association algorithms from scratch.
3. **Deterministic Geometry & Kinetics:**
   - Instead of learning an end-to-end black-box navigation policy, semantic outputs interface directly with standard, predictable ROS 2 components: Nav2 Costmap Filters (`CostmapFilterInfo`) and Model Predictive Path Integral control (`nav2_mppi_controller`).
