# Stack & learning map

What each milestone uses, and how well the student knows it. Status: ✅ done · 🎯 next · ⬜ later.
Learning notes: ROS 2 basics in [`concepts/ROS2_notes`](../../concepts/ROS2_notes/notes/README.md) (student's); project concepts in [`notes/`](notes/).

## 1. Learning map

| Topic | For | Status | What "known" means |
|---|---|---|---|
| ROS 2 core: colcon, packages, topics/services/actions, params, launch | all | ✅ | ROS2_notes 01–05 |
| tf2 + REP 105 frames (`map → odom → base_link → laser/camera`) | all | ✅ | ROS2_notes 06 |
| URDF/xacro, robot_state_publisher, RViz2, Markers | M1, M4 viz | ✅ | ROS2_notes 07 |
| Gazebo Harmonic: worlds, SDF, system plugins (diff-drive, `gpu_lidar`, camera, joint state), actors | M1 | 🎯 | Robot driving in a world, sensors on ROS topics |
| `ros_gz_bridge`, `/clock`, `use_sim_time` | M1 | 🎯 | Can explain why sim time matters and debug a missing bridge |
| Nav2 architecture: map server, AMCL, planner vs controller, costmap layers, BT navigator, lifecycle | M1 | ⬜ | Can read a Nav2 params file and say what each block does |
| MPPI algorithm: sampling, rollouts, critics, softmax weighting, key params | M2–M3 | ⬜ | Can predict what changing `temperature`, `batch_size`, `time_steps`, critic weights does. Old note to reuse after checking: `archive/.../research/notes/4_1_*` |
| pluginlib + MPPI `CriticFunction` (C++) | M1 hello, M3 | ⬜ | Can write a critic that reads trajectories and adds cost |
| Driving Nav2 from Python (`nav2_simple_commander`), headless Gazebo, batch runs | M2 | ⬜ | Harness runs unattended |
| Experiment stats: seeded runs, distributions, paired comparisons | M2+ | ⬜ | Knows why N runs, what a CI says |
| Camera model + box→LiDAR bearing geometry | M4 | ⬜ (math familiar) | Can project a box to a bearing window and back |
| Linear KF (CV model), covariance growth over a horizon | M3–M4 | ⬜ (math familiar) | Can tune Q/R from measured error. Old note: `archive/.../notes/3_4_*` |
| Detection + 2D tracking on sim images | M4 | ✅ (specialty) | — |

## 2. Tools

| Component | Choice | Note |
|---|---|---|
| OS / ROS | Ubuntu 24.04 + ROS 2 Jazzy | Installed on laptop [M1] |
| Simulator | Gazebo Harmonic + `ros_gz` | The Gazebo release paired with Jazzy [E]. Not installed yet |
| Navigation | Nav2 (Jazzy): MPPI, costmap_2d, collision_monitor, AMCL, slam_toolbox (once, to make a map) | [L1][L2] |
| Critic | C++ (pluginlib) | Only C++ in the project |
| Fusion, harness, analysis | Python, NumPy, Matplotlib | Spec names NumPy + Matplotlib |
| Detector (D-cam) | Student's choice (e.g. YOLO-family + ByteTrack-style tracker) | Runs on PC if laptop too slow (Q11) |
| Reproducibility | Pinned package versions + one run script; Docker only if it earns its keep | Decide at M2 |

## 3. Deliberately skip

- Learned trajectory predictors (transformers, diffusion): CV + KF until a measured failure says otherwise.
- Foundation models / VLMs in the loop.
- Fleet management (Open-RMF, VDA 5050), multi-robot.
- 3D point clouds, voxel layers, 3D LiDAR.
- Custom behaviour trees, composable nodes / intra-process comms, building ROS from source, DDS tuning — unless profiling demands it.
- CAD-quality meshes and friction/suspension tuning in sim: boxes and cylinders.
