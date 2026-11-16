# ws — project colcon workspace

Build: `cd ws && colcon build --symlink-install && source install/setup.bash` (ROS 2 Jazzy, Ubuntu 24.04).
Tutorial drills stay in `concepts/ROS2_notes/ros2_ws`; this workspace holds project code only.

## Learn ↔ build loop

For each step of a milestone in [plan.md](../chapters/research/plan.md):

1. **Concept**: the minimum idea needed, in your own words (your notes in `concepts/`, or `chapters/research/notes/` for project-specific concepts).
2. **Build**: the smallest runnable piece. The agent may write it; you must be able to explain every file.
3. **Run & check**: you run it and look at it (RViz, a plot, `ros2 topic echo`). If it matters, log a number in `results.md`.
4. **Log** one line below: what you learned, what broke.

## Packages (planned — created when their milestone starts)

| Package | Milestone | Lang |
|---|---|---|
| `fyp_description` | M1 | xacro/URDF (+ Gazebo sensors) |
| `fyp_bringup` | M1 | launch, Nav2 params, worlds |
| `fyp_harness` | M2 | Python |
| `fyp_msgs` | M3 | msg (unless Q6 finds a standard one) |
| `fyp_dynamic_critic` | M1 hello → M3 | C++ |
| `fyp_fusion` | M4 | Python |

## Log

| Date | Step | Learned / broke |
|---|---|---|
| | | |
