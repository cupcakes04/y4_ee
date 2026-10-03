To learn mobile robotics autonomy entirely in 1:1 simulation without wasting time on mechanical fabrication or deep academic math, follow this sequential 5-module conveyor path.

Each module defines the scope boundary, what to learn, and what to deliberately skip.

---

### Module 1: Middleware & Spatial Transformations (ROS 2 Core)

*Objective:* Master the communication plumbing and spatial reference frames. Do not learn robotics algorithms here; learn how data moves.

* **Specific Docs Target:** `docs.ros.org` $\rightarrow$ *Beginner: CLI Tools*, *Intermediate: tf2*.
* **The Core Mechanics:**
* **Topics vs. Actions:** Topics stream continuous sensor feeds (`/scan`, `/cmd_vel`). Actions handle asynchronous, interruptible goals with feedback (Nav2 goals).
* **The Coordinate Tree (TF2):** Spatial geometry in robotics is entirely frame transformations:

$$\text{map} \xrightarrow{\text{SLAM / AMCL}} \text{odom} \xrightarrow{\text{wheel integration}} \text{base\_link} \xrightarrow{\text{CAD mounting}} \text{lidar\_link}$$



You must understand why `base_link` represents the robot's physical center and how transformations are buffered across time.


* **Verification Milestone:** Write a minimal ROS 2 Python/C++ node that broadcasts a dynamic coordinate frame, and view the transform tree using `ros2 run tf2_tools view_frames`.
* **What to Skip:** Multi-threading executor internals, custom DDS middleware configurations, and building packages from source.

---

### Module 2: Virtual Kinematics & Physics (URDF & Gazebo)

*Objective:* Define a rigid body and simulate its sensors in Gazebo Harmonic/Ignition. This replaces the physical robot.

* **Specific Docs Target:** `docs.ros.org` $\rightarrow$ *Intermediate: URDF*, Gazebo official tutorials for *Differential Drive* and *Sensors*.
* **The Core Mechanics:**
* **URDF / Xacro:** XML descriptions of rigid bodies (`<link>`) connected by joints (`<joint>`).
* **Gazebo Plugins:** Software hooks inside simulation that mimic real hardware:
1. *Diff-Drive Plugin:* Subscribes to `/cmd_vel` to move wheels and calculates odometry dead-reckoning (`odom -> base_link`).
2. *Ray/LiDAR Plugin:* Casts simulated rays against the 3D world geometry and publishes standard `sensor_msgs/msg/LaserScan` messages.




* **Verification Milestone:** Spawn a basic two-wheeled mobile platform in Gazebo, drive it with `teleop_twist_keyboard`, and view the laser scan beams in RViz2 relative to `base_link`.
* **What to Skip:** Realistic collision mesh textures, complex inertia tensor calculations, and contact physics dynamics. Use simple primitives (cylinders and boxes).

---

### Module 3: Environment Perception & Graph SLAM (SLAM Toolbox)

*Objective:* Convert 2D range measurements and noisy odometry into a persistent global map.

* **Specific Docs Target:** `slam_toolbox` GitHub documentation and ROS 2 package manuals.
* **The Core Mechanics:**
* **Pose-Graph Optimization:** The robot places "nodes" along its path. When the laser scan matches an area visited earlier, it adds a "loop closure constraint" and relaxes the entire trajectory graph to eliminate drift.
* **Occupancy Grids:** Maps are 2D arrays where each grid cell stores an integer ($0$ = free space, $100$ = occupied obstacle, $-1$ = unexplored).
* **Transform Ownership:** SLAM solves for the error between where odometry *thinks* the robot is and where the robot *actually* is, continuously publishing the dynamic transform:

$$\text{map} \longrightarrow \text{odom}$$




* **Verification Milestone:** Launch `slam_toolbox` in mapping mode, drive the simulated robot through a multi-room Gazebo world to close a loop, and save the map using `nav2_map_server map_saver_cli`.
* **What to Skip:** Mathematical proofs of Ceres Solver, non-linear least squares derivations, and 3D visual-inertial SLAM (like LIO-SAM or ORB-SLAM3) until 2D LiDAR planar navigation is understood.

---

### Module 4: Autonomous Navigation Architecture (Nav2)

*Objective:* Plan collision-free trajectories from current pose to goal pose across static and dynamic obstacles.

* **Specific Docs Target:** `docs.nav2.org` $\$rightarrow *Getting Started: Navigation Concepts*, *First-Time Robot Setup Guide*.
* **The Core Mechanics:**
* **Costmaps (2D Voxel Grids):**
* *Global Costmap:* Built from the static SLAM map, inflated by robot radius so paths don't skim walls.
* *Local Costmap:* A high-frequency rolling window centered on the robot, populated in real-time by the LiDAR to detect unexpected dynamic obstacles.


* **Global Planner (e.g., NavFn, Smac Planner):** Calculates the static, macro geometric route ($A^*$ or Dijkstra) from robot to target.
* **Local Controller (e.g., DWB, MPPI):** Evaluates motor dynamics and obstacle vectors 20–50 times per second to generate actual linear and angular velocity commands (`/cmd_vel`).
* **Localization (AMCL):** Once a map exists, SLAM is turned off and Adaptive Monte Carlo Localization uses a particle filter to track the robot pose against the saved map.


* **Verification Milestone:** Launch `nav2_bringup` with your saved map, set an initial pose in RViz, drop a navigation goal behind a wall, and verify the robot navigates around dynamic obstacles to reach it.
* **What to Skip:** Writing custom planner or controller plugins from scratch. Use the battle-tested defaults (`SmacPlanner2D` and `DWBLocalPlanner` or `MPPI`).

---

### Module 5: Orchestration & Fault Tolerance (Behavior Trees)

*Objective:* Control system execution logic, recoveries, and task management.

* **Specific Docs Target:** `docs.nav2.org` $\rightarrow$ *Nav2 Behavior Trees*.
* **The Core Mechanics:**
* **Behavior Trees vs. State Machines:** Nav2 does not use rigid if/else states. It evaluates a tree of control nodes (Sequence, Fallback, Decorator) returning `SUCCESS`, `FAILURE`, or `RUNNING`.
* **Recovery Pipelines:** If the local controller cannot find a valid velocity trajectory (robot is trapped), the Behavior Tree automatically sequences recovery actions: clear costmap $\rightarrow$ backup 0.15m $\rightarrow$ spin 360° to rescan $\rightarrow$ retry path.


* **Verification Milestone:** Intentionally block the robot's simulated path with a spawned obstacle in Gazebo, and observe the Behavior Tree trigger costmap clearing and recovery rotations rather than aborting.
* **What to Skip:** Advanced multi-robot fleet dispatching (Open-RMF, VDA 5050) and cloud fleet management.

---

### Summary Checklist for the Simulation Conveyor

```
[Module 1: ROS 2 Core]      Focus: CLI tools, Action servers, TF2 coordinate trees
       │
[Module 2: Simulation]     Focus: URDF joints, Gazebo diff-drive & laser plugins
       │
[Module 3: Mapping]        Focus: slam_toolbox, loop closure, map_server saves
       │
[Module 4: Navigation]     Focus: Nav2 costmap inflation, Global Planner, Local Controller
       │
[Module 5: Decision Logic] Focus: Behavior Trees (BT Navigator), recovery pipelines

```

To see this modular simulation pipeline implemented end-to-end, follow the [ROS2 SLAM Toolbox Mobile Robot Simulation Tutorial](https://www.youtube.com/watch?v=0G6LDuslqmA). This video walks through the exact workflow of configuring simulated LiDAR parameters, launching the SLAM Toolbox node, and generating an occupancy grid map in RViz2.