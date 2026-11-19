# ws — project colcon workspace

Build: `cd ws && colcon build --symlink-install && source install/setup.bash` (ROS 2 Jazzy, Ubuntu 24.04).
Tutorial drills stay in `concepts/ROS2_notes/ros2_ws`; this workspace holds project code only.

## Learn ↔ build loop

For each step of a milestone in [plan.md](../chapters/research/plan.md):

1. **Concept**: the minimum idea needed, in your own words (your notes in `concepts/`, or `chapters/research/notes/` for project-specific concepts). You can put 'what i should know' and user (I) will try to answer and discover myself, which you correct me as a teacher (back and forth) 
2. **Build**: the smallest runnable piece. The agent may write it; you must be able to explain every file.
3. **Run & check**: you run it and look at it (RViz, a plot, `ros2 topic echo`). If it matters, log a number in `results.md`.
4. **Check understanding (situational)**: when a step's concept is load-bearing for later steps (sim time, TF, MPPI params, KF tuning…), the agent writes 3–5 short questions into `chapters/scratch/answer.md`. Each question is anchored to a real error message, decision or number the student will meet in the next steps (and says when); if it can't be, it's cut. Purpose: find bugs in the mental model before they become bugs in the system. Graded bluntly; gaps go back into the concept note. Pass criteria = the *"What known means"* column in [stack.md](../chapters/research/stack.md). Skipped for routine steps.
5. **Log** one line below: what you learned, what broke.

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
| 2026-11-19 | M1 step 1: Gazebo Harmonic + ros_gz_bridge + sim time; Q3 test | Learned: Gazebo uses gz-transport not DDS, bridge per topic, sim vs wall time, RTF; TF needed between any two frames RViz must relate. Q3 = actors visible to gpu_lidar [M2]; RTF ≈ 1.0 with 2 lidars [M3]. Broke: conda Python 3.11 shadowing ROS Python 3.12 (`conda deactivate`); RViz dropped `/scan_high` with no TF to the fixed frame |
