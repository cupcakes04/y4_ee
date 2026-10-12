# 5. Hardware & Software Deliverables

## 5.1 Hardware Specifications

- **Edge Compute (Deployment Target):** NVIDIA Jetson Orin Nano (8GB) or Orin NX (or equivalent x86 mini-PC with an entry-level mobile GPU).
- **Development Workstation:** AMD / Intel workstation with NVIDIA RTX 4070 Ti Super GPU (used for offline distillation and simulation benchmarks).
- **Sensors:**
  - 1x Low-cost 2D Planar Laser Scanner (e.g., Slamtec RPLiDAR S2/A3, ~$380–500, or industrial safety single-layer scanner).
  - 1x Global Shutter Monocular USB/MIPI Camera (1080p, $60^\circ\text{–}90^\circ$ horizontal FoV).
  - *(Note: Detailed engineering justification comparing this pairing against stereo RGB-D cameras and 3D LiDAR is recorded in `08_design_tradeoffs_and_alternatives.md` §8.1).*
- **Mobile Base:** Differential drive or omnidirectional ROS 2 AMR base (TurtleBot 4 simulation model in Gazebo Harmonic, or physical robot in stretch phase).

---

## 5.2 Software Deliverables & ROS 2 Architecture

1. **`semantic_context_layer` (ROS 2 Package):**
   - Real-time TensorRT segmentation node.
   - Planar homography projection node converting pixel masks to `geometry_msgs/msg/PolygonStamped`.
   - ROS 2 Costmap Filter publisher for dynamic Keepout and Speed Limit zones.
2. **`lidar_vision_tracker` (ROS 2 Package):**
   - 2D Multi-Object Tracking node (ByteTrack via `boxmot`) maintaining persistent visual `track_id`s in image space.
   - Target association node filtering planar LiDAR ranges through visual bounding frustums.
   - Per-track linear Kalman filter (CV) publishing dynamic agent state arrays (`/tracked_obstacles`).
3. **`nav2_mppi_dynamic_critic` (C++ Plugin):**
   - Custom dynamic obstacle prediction critic plugin for `nav2_mppi_controller`.
4. **Offline Distillation Toolkit:**
   - Automated CLI scripts for video ingestion, zero-shot VLM prompting, dataset generation, and TensorRT model compilation (extending prototype `avp`).

---

## 5.3 Stack Selection Rationale: ROS 2 Jazzy + Gazebo Harmonic

- **Distribution Choice:** ROS 2 Jazzy Jalisco (LTS until May 2029) paired with Gazebo Harmonic.
- **Alternatives Evaluated:**
  - *ROS 2 Iron Irwini:* End-of-Life reached in December 2024.
  - *ROS 2 Humble Hawksbill:* EOL in May 2027 (coinciding with the final submission of this project).
  - *Decision:* Jazzy provides the longest support runway and modern Nav2 MPPI improvements.
