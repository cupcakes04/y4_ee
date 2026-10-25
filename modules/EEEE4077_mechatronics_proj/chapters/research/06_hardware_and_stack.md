# 6. Compute Platform, Simulated Sensors & Software Stack

This chapter specifies the development workstation, simulated sensor models, mobile robot base URDF, and software package architecture supporting the project. In strict alignment with supervisor specification `SD-MEng-26-01` (HW 0% / SW 60% / Research 40%), all physical hardware procurement and lab deployment are omitted, committing 100% of engineering effort to high-fidelity software simulation.

---

## 6.1 Simulation Environment & Compute Specifications

### 6.1.1 Development & Simulation Workstation
All development, model compilation, Gazebo Harmonic simulation, and automated ablation benchmarking are hosted on a dedicated high-performance workstation:
- **CPU:** High-performance multi-core x86_64 processor (AMD Ryzen 7 / Intel Core i7).
- **GPU:** NVIDIA GeForce RTX 4070 Ti Super (16GB VRAM, CUDA Compute 8.9).
- **RAM:** 32GB DDR5.
- **Operating System:** Ubuntu 24.04 LTS (Noble Numbat) with ROS 2 Jazzy Jalisco.

### 6.1.2 Edge Compute Constraints (Benchmarking Reference)
While running inside workstation simulation, the software algorithms are designed and budgeted to respect realistic edge compute envelopes typical of commercial brownfield AMRs:
- **Reference Compute Profile:** Low-power onboard industrial CPU (x86/ARM) with modest SIMD capabilities (AVX2/NEON).
- **Execution Budget:** Sustained $\ge 20\text{ Hz}$ end-to-end control loop rate and $<0.3\text{ ms}$ MPPI critic evaluation latency. Avoids heavy GPU-bound libraries (e.g., RAPIDS cuML or multi-gigabyte foundation model inference) inside the real-time control loop.

### 6.1.3 Sensor Configuration
- **1x 2D Planar Laser Scanner:**
  - Range: $0.1\text{--}12\text{ m}$.
  - Scan Rate: $20\text{--}40\text{ Hz}$.
  - Horizontal Angular Resolution: $0.5^\circ\text{--}1.0^\circ$ ($360^\circ$ scanning plane).
  - Representative Hardware: Slamtec RPLiDAR S2/A3 or industrial safety single-layer scanner.
- **1x Global Shutter Monocular USB/MIPI Camera:**
  - Resolution: 1080p ($1920 \times 1080$) or 720p ($1280 \times 720$).
  - Frame Rate: $30\text{ FPS}$.
  - Horizontal Field of View: $70^\circ\text{--}90^\circ$.
  - Shutter: Global shutter (minimizes rolling-shutter distortion during robot motion).
- *(Note: Detailed engineering justification comparing this pairing against stereo RGB-D cameras and 3D LiDAR is recorded in `08_design_tradeoffs_and_alternatives.md` §8.1).*

### 6.1.4 Mobile Robot Base
- **Simulation Base:** Differential-drive TurtleBot 4 / standard industrial AMR URDF in Gazebo Harmonic.
- **Kinematic Constraints:** Maximum linear velocity $v_{\max} = 1.0\text{ m/s}$, maximum angular velocity $\omega_{\max} = 1.5\text{ rad/s}$.

---

## 6.2 Software Package Architecture (ROS 2 Workspace)

The software stack is organized into four modular ROS 2 packages adhering to standard colcon build conventions:

```
colcon_ws/src/
├── custom_interfaces/
│   ├── msg/
│   │   ├── TrackedObstacle.msg
│   │   └── TrackedObstacleArray.msg
│   └── CMakeLists.txt
├── lidar_vision_tracker/
│   ├── config/ (detector params, calibration matrices [R|t], EKF noise matrices)
│   ├── src/
│   │   ├── tensorrt_detector_node.cpp
│   │   ├── bytetrack_node.py (or C++ wrapper)
│   │   ├── frustum_gating_node.cpp
│   │   └── kalman_filter_node.cpp
│   └── CMakeLists.txt
├── nav2_mppi_dynamic_critic/
│   ├── include/nav2_mppi_dynamic_critic/
│   │   └── dynamic_obstacles_critic.hpp
│   ├── src/
│   │   └── dynamic_obstacles_critic.cpp
│   ├── dynamic_critics.xml (pluginlib export)
│   └── CMakeLists.txt
└── ablation_benchmark_harness/
    ├── launch/ (simulation bringup, scenario launch files)
    ├── worlds/ (Gazebo Harmonic industrial warehouse models)
    ├── scripts/ (automated batch scenario runner, metrics logger, report generator)
    └── CMakeLists.txt
```

### 1. `custom_interfaces`
Defines the standard dynamic obstacle array message:
```
# TrackedObstacle.msg
uint32 track_id
string label
geometry_msgs/Point position
geometry_msgs/Vector3 velocity
float64[16] covariance
float32 confidence
```

### 2. `lidar_vision_tracker` (Perception Subsystem)
- **Object Detection:** Loads TensorRT-optimized YOLO engine (INT8/FP16) on GPU.
- **Visual Association:** Implements ByteTrack algorithm maintaining consistent integer IDs across frames.
- **Spatial Alignment:** Applies Zhang & Pless extrinsic projection $[R \mid t]$ to gate planar LiDAR returns through visual bounding boxes.
- **State Estimation:** Instantiates per-track linear Kalman filters updating $[x, y, v_x, v_y]^T$ and broadcasting `/tracked_obstacles`.

### 3. `nav2_mppi_dynamic_critic` (Local Control Plugin)
- Implements `DynamicObstaclesCritic` derived from `mppi::critics::CriticFunction`.
- Exported via `pluginlib` and loaded dynamically by `nav2_mppi_controller` at runtime.
- Evaluates forward-projected obstacle positions against sampled trajectory rollouts across the preview horizon.

### 4. `ablation_benchmark_harness` (Evaluation Subsystem)
- Manages Gazebo Harmonic worlds, actor kinematics, and launch scripts.
- Orchestrates automated batch executions across configurations C0, C1, and C2.
- Subscribes to ground truth simulator topics and generates comprehensive statistical CSV datasets.

---

## 6.3 Stack Selection Rationale: ROS 2 Jazzy + Gazebo Harmonic

- **Distribution Choice:** **ROS 2 Jazzy Jalisco** (LTS release supported through May 2029) paired with **Gazebo Harmonic**.
- **Alternative Evaluated: ROS 2 Iron Irwini:** End-of-Life reached in December 2024; unsuitable for an active MEng dissertation.
- **Alternative Evaluated: ROS 2 Humble Hawksbill:** EOL in May 2027 (coinciding with the final submission of this project). Furthermore, Nav2's MPPI implementation underwent substantial performance enhancements, SIMD optimizations, and cleaner plugin APIs between Humble and Jazzy.
- **Simulator Modernization:** Gazebo Harmonic replaces deprecated Gazebo Classic (Gazebo 11), providing modern physics solvers, unified sensor plugins, and native ROS 2 integration via `ros_gz`.

