# ROS 2 Engineering Notes & Workflow Lookup

A decoupled, modular quick-reference lookup system for ROS 2 (Jazzy / modern ROS 2). Designed as an immediate mental model and fast copy-paste reference, with relative links into your local [`ros2_documentation`](../ros2_documentation/source/Tutorials.rst).

[Online documentation here](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries.html)

---

## 🗺️ Master Index & Lookup Map

| Module | Core Purpose | Key Topics Covered |
| :--- | :--- | :--- |
| [**01. Workspace & Environment**](01_workspace_and_env/01_workspace_lifecycle.md) | Workspace lifecycle & build system | Underlays vs overlays, standard 5-step loop, `--symlink-install`, `colcon` optimization, `colcon_cd`, `COLCON_IGNORE` |
| [**02. Package Architecture**](02_package_architecture/01_package_creation.md) | Creating & configuring packages | `ros2 pkg create`, Python vs C++ file layout, `package.xml` tags, `setup.py` entry points vs `CMakeLists.txt` |
| [**03. Communication Paradigms**](03_communication_paradigms/01_topics_pubsub.md) | Inter-node patterns & skeletons | Topics (Pub/Sub), Services (Req/Res), Actions (Goal/Feedback), Parameters |
| [**04. CLI Cheatsheet & Tools**](04_cli_cheatsheet/01_ros2_cli_lookup.md) | Terminal commands & introspection | Fast CLI lookup matrix (`topic`, `service`, `param`, `action`, `bag`), `rqt_graph`, introspection |
| [**05. Launch System**](05_launch_system/01_creating_launch_files.md) | Multi-node orchestration & config | Python launch syntax, `LaunchDescription`, `Node`, parameters, remappings, includes, installation gotchas |
| [**06. tf2 Coordinate Frames**](06_tf2_coordinate_frames/01_tf2_concepts_and_tree.md) | Spatial transforms & kinematics | TF tree rules (`map` $\rightarrow$ `odom` $\rightarrow$ `base_link`), static & dynamic broadcasters, listeners, quaternions |
| [**07. URDF & RViz2**](07_urdf_and_rviz/01_visual_robot_urdf.md) | 3D Robot modeling & visualization | Links & joints, collision/inertials, `robot_state_publisher`, `joint_state_publisher_gui`, RViz2 launch setup |

---

## ⚡ The 30-Second Golden Workflow Loop

Every time you develop in your workspace:

```bash
# 1. Edit code in your package
cd ros2_ws/src/<package_name>

# 2. Build from workspace root (Python needs --symlink-install once)
cd ros2_ws
colcon build --packages-select <package_name> --symlink-install

# 3. Source environment (in EVERY terminal running the node)
source install/setup.bash

# 4. Run executable
ros2 run <package_name> <executable_name>
```

---

## 📁 Detailed Module Breakdown (Chronological Study Order)

### [01. Workspace & Environment](01_workspace_and_env/01_workspace_lifecycle.md)
- [`01_workspace_lifecycle.md`](01_workspace_and_env/01_workspace_lifecycle.md): Directory anatomy (`src`, `build`, `install`, `log`), underlay vs overlay mechanics, execution rules, and moved workspace recovery.
- [`02_colcon_recipes.md`](01_workspace_and_env/02_colcon_recipes.md): Command flags, build parallelization, skipping packages (`COLCON_IGNORE`), disabling tests, and `colcon_cd` navigation setup.

### [02. Package Architecture](02_package_architecture/01_package_creation.md)
- [`01_package_creation.md`](02_package_architecture/01_package_creation.md): `ament_python` vs `ament_cmake` generation, folder structure comparison.
- [`02_config_and_dependencies.md`](02_package_architecture/02_config_and_dependencies.md): `package.xml` dependencies, Python `setup.py` console scripts, C++ `CMakeLists.txt` targets, and custom interface packages.

### [03. Communication Paradigms](03_communication_paradigms/01_topics_pubsub.md)
- [`01_topics_pubsub.md`](03_communication_paradigms/01_topics_pubsub.md): Publish/Subscribe (continuous streaming). Minimal rclpy boilerplate, rclcpp comparison, CLI lookup.
- [`02_services.md`](03_communication_paradigms/02_services.md): Service/Client (synchronous request/response). Minimal rclpy service & client skeletons, C++ comparison, CLI lookup.
- [`03_actions.md`](03_communication_paradigms/03_actions.md): Action Server/Client (long-running goals with feedback & cancellation). Custom `.action` schema, full Python server & client, C++ server & client.
- [`04_parameters.md`](03_communication_paradigms/04_parameters.md): Node parameters (declaration, runtime lookup, callbacks on change, launch parameter loading).

### [04. CLI Cheatsheet & Tools](04_cli_cheatsheet/01_ros2_cli_lookup.md)
- [`01_ros2_cli_lookup.md`](04_cli_cheatsheet/01_ros2_cli_lookup.md): Instant command reference matrix (`ros2 run`, `node`, `topic`, `service`, `param`, `action`, `bag`, `launch`, `tf2`).
- [`02_debugging_and_tools.md`](04_cli_cheatsheet/02_debugging_and_tools.md): `rqt_graph`, `ros2 doctor`, interface inspection (`ros2 interface show`), echoing and calling live entities.

### [05. Launch System (Intermediate)](05_launch_system/01_creating_launch_files.md)
- [`01_creating_launch_files.md`](05_launch_system/01_creating_launch_files.md): Launch files foundations (`turtlesim_mimic_launch.py`), `LaunchDescription`, `Node`, namespaces, remappings, and setup.py install trap.
- [`02_substitutions_and_arguments.md`](05_launch_system/02_substitutions_and_arguments.md): Dynamic launch arguments (`DeclareLaunchArgument`, `LaunchConfiguration`), dynamic path resolution (`PathJoinSubstitution`, `FindPackageShare`), and `PythonExpression`.
- [`03_event_handlers.md`](05_launch_system/03_event_handlers.md): Lifecycle event triggers (`OnProcessStart`, `OnProcessExit`, `Shutdown`), sequential node staging.
- [`04_large_project_architecture.md`](05_launch_system/04_large_project_architecture.md): Large-scale modular include trees (`IncludeLaunchDescription`), multi-robot namespaces (`PushRosNamespace`), and the 4-tier package blueprint.

### [06. tf2 Coordinate Frames (Intermediate)](06_tf2_coordinate_frames/01_tf2_concepts_and_tree.md)
- [`01_tf2_concepts_and_tree.md`](06_tf2_coordinate_frames/01_tf2_concepts_and_tree.md): Why tf2 exists, coordinate frame tree, REP 105 mobile robot standards (`map` $\rightarrow$ `odom` $\rightarrow$ `base_link`), and the single parent rule.
- [`02_static_broadcaster.md`](06_tf2_coordinate_frames/02_static_broadcaster.md): Fixed sensor frame offsets, CLI static publisher vs Python `StaticTransformBroadcaster`, and Euler to Quaternion conversion.
- [`03_broadcaster_and_listener.md`](06_tf2_coordinate_frames/03_broadcaster_and_listener.md): Continuous moving frames (`TransformBroadcaster`), transform cache buffer, and `TransformListener.lookup_transform`.
- [`04_adding_frames_and_time_travel.md`](06_tf2_coordinate_frames/04_adding_frames_and_time_travel.md): Adding dynamic sub-frames (floating carrot goal), time interpolation across the 10-second buffer ring, and fixing `ExtrapolationException`.
- [`05_message_filters_and_debugging.md`](06_tf2_coordinate_frames/05_message_filters_and_debugging.md): Sensor synchronization with `tf2_ros.MessageFilter` (eliminating race conditions), and diagnostic protocol (`view_frames`, `tf2_echo`, `tf2_monitor`).

### [07. URDF & RViz2 (Intermediate)](07_urdf_and_rviz/01_visual_robot_urdf.md)
- [`01_visual_robot_urdf.md`](07_urdf_and_rviz/01_visual_robot_urdf.md): URDF XML syntax (`<robot>`, `<link>`, `<joint type="fixed">`), materials, origin offsets, and geometric primitives.
- [`02_movable_joints.md`](07_urdf_and_rviz/02_movable_joints.md): Joint types (`continuous`, `revolute`, `prismatic`), joint limits, `/joint_states` topic, and `joint_state_publisher_gui` sliders.
- [`03_physical_and_collision_properties.md`](07_urdf_and_rviz/03_physical_and_collision_properties.md): Separating visual CAD meshes from simplified collision primitives, mass, and moment of inertia calculation formulas.
- [`04_clean_modeling_with_xacro.md`](07_urdf_and_rviz/04_clean_modeling_with_xacro.md): Clean modeling with Xacro (variables, math `${...}`, parameterized macros, modular files), and dynamic launch evaluation via `Command(['xacro ', file])`.
- [`05_robot_state_publisher_and_rviz.md`](07_urdf_and_rviz/05_robot_state_publisher_and_rviz.md): The forward kinematics pipeline (`robot_state_publisher`), complete display launch file, Fixed Frame vs Target Frame, and RViz initial setup checklist.
- [`06_rviz_markers_and_visualization.md`](07_urdf_and_rviz/06_rviz_markers_and_visualization.md): Publishing custom 3D shapes, bounding boxes, and path trajectories directly into RViz using `visualization_msgs/msg/Marker`.
