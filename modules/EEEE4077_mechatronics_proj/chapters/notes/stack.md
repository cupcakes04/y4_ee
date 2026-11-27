# Stack & depth map

What each milestone uses, how deep the student goes in it, and what has clicked. Why these depths: [brief §4](brief.md).
Status: ✅ done · 🎯 next · ⬜ later. Notes: the student's own in [`concepts/`](../../concepts/ROS2_notes/notes/README.md); project concept notes in [`lessons/`](lessons/).

## 1. Depth map

**Depth**: the perception ↔ control interface and how it's judged; derive it, predict it, defend it. **Competent**: build it and debug it (symptom → cause), no more. **Delegate**: syntax and boilerplate; know what each file is for.

| Topic | For | Depth | Status | Done when you can |
|---|---|---|---|---|
| ROS 2 core: colcon, packages, topics/services/actions, params, launch | all | Competent | ✅ concepts | Concepts in ROS2_notes 01–05; code comes with M1 |
| tf2 + REP 105 frames (`map → odom → base_link → laser/camera`) | all | Competent | ✅ concepts | Tell a "which frames" failure from a "when" failure and fix both |
| URDF/xacro, robot_state_publisher, RViz2 | M1, M4 viz | Competent (xacro syntax: Delegate) | 🎯 | Your own robot's frame tree, built and checked in RViz |
| Gazebo Harmonic: worlds, SDF, system plugins, actors | M1 | Competent | 🎯 | Your robot driving in a world, sensors on ROS topics |
| `ros_gz_bridge`, `/clock`, `use_sim_time` | M1 | Competent | ✅ (2026-11-19) | Debug a missing bridge or a clock mismatch |
| Nav2 architecture: map server, planner vs controller, costmaps, BT navigator, lifecycle | M1 | Competent | ⬜ | Read a Nav2 params file and say what each block does |
| MPPI algorithm: sampling, rollouts, critics, softmax weighting, key params | M2–M3 | **Depth** | ⬜ | Predict what changing `temperature`, `batch_size`, `time_steps`, critic weights does. Old note to check: `archive/.../research/notes/4_1_*` |
| pluginlib + MPPI `CriticFunction` (C++) | M1 hello, M3 | **Depth** | ⬜ | Write a critic that reads trajectories and adds cost |
| Driving Nav2 from Python, headless Gazebo, batch runs | M2 | Competent | ⬜ | Harness runs unattended |
| Experiment design + stats: baselines, seeded runs, distributions, paired comparisons | M2+ | **Depth** | ⬜ | Say why N runs, what a CI says, and what makes a comparison fair |
| Camera model + box→LiDAR bearing geometry | M4 | **Depth** | ⬜ (math familiar) | Project a box to a bearing window and back |
| Linear KF (CV model), covariance growth over a horizon | M3–M4 | **Depth** | ⬜ (math familiar) | Tune Q/R from measured error. Old note: `archive/.../notes/3_4_*` |
| Detection + 2D tracking on sim images | M4 | Specialty | ✅ | — |

## 2. What clicked

One line each, in the student's words, added when an explain-back lands or a bug finally makes sense. Newest last.

| Date | Topic | What clicked |
|---|---|---|
| 2026-11-19 | Testing a sensor | A control object (the cylinder) proves the lidar works before you trust a miss on the actor |
| 2026-11-19 | Bridge | `]` = ROS → Gazebo: the direction for actuators like `/cmd_vel` |
| 2026-11-27 | tf2 | Sensors bolted to the robot are static transforms to the base, even while the robot drives; tf2 is links like graph nodes (a tree) and it runs the maths along the chain |
| 2026-11-27 | Odometry | Odom = pose (x, y, θ) integrated from the robot's own velocity over time; knows nothing about the world, so it drifts. `odom` origin = where it started |
| 2026-11-27 | tf2 + time | The timestamp flows with the data so tf2 can look up the robot's pose at measurement time, not now; TF holds frames (robot, sensors), not detected objects |
| 2026-11-27 | map vs odom | Localization compares /scan with the known map, finds odom's error and publishes it as `map → odom`: the drift correction |

## 3. Tools

| Component | Choice | Note |
|---|---|---|
| OS / ROS | Ubuntu 24.04 + ROS 2 Jazzy | Laptop: Ubuntu 24.04.4, ROS 2 Jazzy in `/opt/ros`, 8 cores, 13 GB RAM (checked 2026-11-16: `lsb_release -ds; ls /opt/ros; nproc; free -g`) |
| Simulator | Gazebo Harmonic + `ros_gz` | The Gazebo release paired with Jazzy [E]. Installed: Gazebo Sim 8.15.0 (2026-11-18) |
| Navigation | Nav2 (Jazzy): MPPI, costmap_2d, collision_monitor, AMCL, slam_toolbox (once, to make a map) | [L1][L2] |
| Critic | C++ (pluginlib) | Only C++ in the project |
| Fusion, harness, analysis | Python, NumPy, Matplotlib | Spec names NumPy + Matplotlib |
| Detector (D-cam) | Student's choice (e.g. YOLO-family + ByteTrack-style tracker) | Runs on PC if laptop too slow (Q11) |
| Reproducibility | Pinned package versions + one run script; Docker only if it earns its keep | Decide at M2 |

## 4. Deliberately skip

- Learned trajectory predictors (transformers, diffusion): CV + KF until a measured failure says otherwise.
- Foundation models / VLMs in the loop.
- Fleet management (Open-RMF, VDA 5050), multi-robot.
- 3D point clouds, voxel layers, 3D LiDAR.
- Custom behaviour trees, composable nodes / intra-process comms, building ROS from source, DDS tuning — unless profiling demands it.
- CAD-quality meshes and friction/suspension tuning in sim: boxes and cylinders.
