# ROS 2 Engineering Notes & Workflow Lookup

A decoupled, modular quick-reference lookup system for ROS 2 (Jazzy / modern ROS 2). Designed as an immediate mental model and fast copy-paste reference, with relative links into your local [`ros2_documentation`](../ros2_documentation/source/Tutorials.rst).

---

## 🗺️ Master Index & Lookup Map

| Module | Core Purpose | Key Topics Covered |
| :--- | :--- | :--- |
| [**01. Workspace & Environment**](01_workspace_and_env/workspace_lifecycle.md) | Workspace lifecycle & build system | Underlays vs overlays, standard 5-step loop, `--symlink-install`, `colcon` optimization, `colcon_cd`, `COLCON_IGNORE` |
| [**02. Package Architecture**](02_package_architecture/package_creation.md) | Creating & configuring packages | `ros2 pkg create`, Python vs C++ file layout, `package.xml` tags, `setup.py` entry points vs `CMakeLists.txt` |
| [**03. Communication Paradigms**](03_communication_paradigms/topics_pubsub.md) | Inter-node patterns & skeletons | Topics (Pub/Sub), Services (Req/Res), Actions (Goal/Feedback), Parameters |
| [**04. CLI Cheatsheet & Tools**](04_cli_cheatsheet/ros2_cli_lookup.md) | Terminal commands & introspection | Fast CLI lookup matrix (`topic`, `service`, `param`, `action`, `bag`), `rqt_graph`, introspection |

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

## 📁 Detailed Module Breakdown

### [01. Workspace & Environment](01_workspace_and_env/workspace_lifecycle.md)
- [`workspace_lifecycle.md`](01_workspace_and_env/workspace_lifecycle.md): Directory anatomy (`src`, `build`, `install`, `log`), underlay vs overlay mechanics, execution rules.
- [`colcon_recipes.md`](01_workspace_and_env/colcon_recipes.md): Command flags, build parallelization, skipping packages (`COLCON_IGNORE`), disabling tests, and `colcon_cd` navigation setup.

### [02. Package Architecture](02_package_architecture/package_creation.md)
- [`package_creation.md`](02_package_architecture/package_creation.md): `ament_python` vs `ament_cmake` generation, folder structure comparison.
- [`config_and_dependencies.md`](02_package_architecture/config_and_dependencies.md): `package.xml` dependencies, Python `setup.py` console scripts, C++ `CMakeLists.txt` targets.

### [03. Communication Paradigms](03_communication_paradigms/topics_pubsub.md)
- [`topics_pubsub.md`](03_communication_paradigms/topics_pubsub.md): Publish/Subscribe (continuous streaming). Minimal rclpy boilerplate, rclcpp comparison, CLI lookup.
- [`services.md`](03_communication_paradigms/services.md): Service/Client (synchronous request/response). Minimal rclpy service & client skeletons, C++ comparison, CLI lookup.
- [`actions.md`](03_communication_paradigms/actions.md): Action Server/Client (long-running goals with feedback & cancellation). Minimal boilerplate and lifecycle. *(Note: Action coding is the bridge into Intermediate)*.
- [`parameters.md`](03_communication_paradigms/parameters.md): Node parameters (declaration, runtime lookup, callbacks on change).

### [04. CLI Cheatsheet & Tools](04_cli_cheatsheet/ros2_cli_lookup.md)
- [`ros2_cli_lookup.md`](04_cli_cheatsheet/ros2_cli_lookup.md): Instant command reference matrix (`ros2 run`, `node`, `topic`, `service`, `param`, `action`, `bag`).
- [`debugging_and_tools.md`](04_cli_cheatsheet/debugging_and_tools.md): `rqt_graph`, `ros2 doctor`, interface inspection (`ros2 interface show`), echoing and calling live entities.
