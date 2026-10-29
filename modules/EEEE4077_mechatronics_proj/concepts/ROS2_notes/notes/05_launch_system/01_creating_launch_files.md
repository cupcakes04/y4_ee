# 01. Creating Launch Files & Remappings

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Creating-Launch-Files.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Launch/Creating-Launch-Files.rst)  
> - Web: [Creating a Launch File](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)

---

## 1. Mental Model: Why Launch Files?

Instead of opening 5 terminal tabs to run `ros2 run` for each node, a **Launch File** defines your entire system as an executable graph.

```
                  ┌───────────────────────────────┐
                  │   turtlesim_mimic_launch.py   │
                  └───────────────┬───────────────┘
            ┌─────────────────────┼─────────────────────┐
            ▼                     ▼                     ▼
 ┌──────────────────────┐ ┌──────────────┐ ┌──────────────────────┐
 │ Node: /turtlesim1    │ │ Node: /mimic │ │ Node: /turtlesim2    │
 │ (Leader)             │ │              │ │ (Follower)           │
 │ pub: /turtle1/pose ──┼─┼─> input/pose │ │                      │
 │                      │ │ output/cmd_vel─┼─> sub: /turtle1/cmd_vel│
 └──────────────────────┘ └──────────────┘ └──────────────────────┘
```

The launch system solves three core problems:
1. **Concurrency:** Starts and stops multiple nodes in a coordinated fashion.
2. **Namespace Isolation:** Runs multiple identical nodes without name collisions (e.g. `/turtlesim1` vs `/turtlesim2`).
3. **Decoupled Wiring (Remapping):** Connects topics between nodes without modifying node source code.

---

## 2. Walkthrough: The `turtlesim_mimic` Example

Save this file as `launch/turtlesim_mimic_launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # 1. Leader Turtle (Isolated under /turtlesim1)
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='sim',
            arguments=['--ros-args', '--log-level', 'warn'],
        ),

        # 2. Follower Turtle (Isolated under /turtlesim2)
        Node(
            package='turtlesim',
            namespace='turtlesim2',
            executable='turtlesim_node',
            name='sim',
            ros_arguments=['--log-level', 'warn'],
        ),

        # 3. Mimic Bridge (Wires /turtlesim1 pose -> /turtlesim2 cmd_vel)
        Node(
            package='turtlesim',
            executable='mimic',
            name='mimic',
            remappings=[
                ('/input/pose', '/turtlesim1/turtle1/pose'),
                ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
            ]
        )
    ])
```

### Key Python Concepts Explained:
* **`generate_launch_description()`:** The required entrypoint function ROS 2 looks for. It must return a `LaunchDescription` object containing a list of actions.
* **`namespace='...'`:** Prefixes all node topics, services, and parameters (e.g., `/turtle1/pose` becomes `/turtlesim1/turtle1/pose`).
* **`remappings=[('from_topic', 'to_topic')]`:** Rewires topic connections. Here, `mimic` listens to `/turtlesim1/turtle1/pose` and publishes velocity directly to `/turtlesim2/turtle1/cmd_vel`.
* **`arguments` vs `ros_arguments`:**
  * `arguments`: Direct arguments to the executable (requires explicit `--ros-args` flag).
  * `ros_arguments`: Directly passes ROS 2 specific flags (e.g. `--log-level warn`).

---

## 3. Running Launch Files

### Method A: Run directly by file path (Standalone)
You do not need to build a package to test a launch file:
```bash
ros2 launch launch/turtlesim_mimic_launch.py
```

### Method B: Run via an installed package
```bash
ros2 launch <package_name> turtlesim_mimic_launch.py
```

---

## 4. Testing the Mimic Behavior

With the launch file running in Terminal 1, open Terminal 2 and publish velocity to the leader:

```bash
ros2 topic pub -1 /turtlesim1/turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
```

**Observation:**
* Turtle 1 moves in an arc.
* The `mimic` node reads Turtle 1's position and commands Turtle 2 to drive in the identical path!

---

## 5. The Package Installation Trap

If you want `ros2 launch <my_pkg> <my_launch.py>` to work, you must declare installation rules.

### For Python Packages (`setup.py`):
> [!CAUTION]
> The `launch/` folder **must be placed at the package root** (sibling to `setup.py`), NOT inside `src/my_pkg/my_pkg/launch/`.
```python
import os
from glob import glob

setup(
    # ...
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
)
```

### For C++ Packages (`CMakeLists.txt`):
```cmake
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
```

