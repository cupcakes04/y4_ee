# 04. Large Project Architecture: Modular Includes & Namespaces

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Using-ROS2-Launch-For-Large-Projects.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.rst)  
> - Web: [Managing Large Projects with ROS 2 Launch](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.html)

---

## 1. Mental Model: Modular Include Trees

In real robotic systems, you never write a single 1,000-line monolithic launch file. Instead:
1. Each subsystem (sensors, navigation, localization, visualization) provides its own self-contained launch file.
2. A **top-level bringup package** aggregates them via `IncludeLaunchDescription`.

```
                  ┌───────────────────────────────┐
                  │       robot_bringup.launch.py │ (Top-Level)
                  └───────────────┬───────────────┘
            ┌─────────────────────┼─────────────────────┐
            ▼                     ▼                     ▼
 ┌──────────────────────┐ ┌──────────────┐ ┌──────────────────────┐
 │ rsp.launch.py        │ │ ekf.launch.py│ │ nav2.launch.py       │
 │ (my_robot_description) (localization) │ (navigation stack)     │
 └──────────────────────┘ └──────────────┘ └──────────────────────┘
```

---

## 2. Including Sub-Launch Files (`IncludeLaunchDescription`)

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 1. Include description launch file
    description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_description'),
                'launch',
                'rsp.launch.py'
            ])
        ),
        launch_arguments={'use_sim_time': 'false'}.items()
    )

    # 2. Include localization launch file
    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('my_robot_localization'),
                'launch',
                'ekf.launch.py'
            ])
        )
    )

    return LaunchDescription([
        description_launch,
        localization_launch
    ])
```

---

## 3. Multi-Robot Groups & Namespaces (`GroupAction` & `PushRosNamespace`)

To spawn multi-robot fleets (e.g. `robot1` and `robot2`) without modifying node code:

```python
from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_launch_path = PathJoinSubstitution([
        FindPackageShare('my_robot_bringup'), 'launch', 'single_robot.launch.py'
    ])

    # Spawns entire robot stack under /robot1
    robot1_group = GroupAction(
        actions=[
            PushRosNamespace('robot1'),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(robot_launch_path))
        ]
    )

    # Spawns identical stack under /robot2
    robot2_group = GroupAction(
        actions=[
            PushRosNamespace('robot2'),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(robot_launch_path))
        ]
    )

    return LaunchDescription([
        robot1_group,
        robot2_group
    ])
```

---

## 4. The 4-Tier Industrial Repository Structure

In modern ROS 2 robot repositories, divide your packages into clear layers:

| Package Layer | Naming Convention | Responsibilities |
| :--- | :--- | :--- |
| **Description** | `my_robot_description` | URDF/Xacro models, 3D meshes, RViz configurations, `rsp.launch.py` |
| **Bringup** | `my_robot_bringup` | Top-level launch files (`robot.launch.py`, `sim.launch.py`), master parameters |
| **Hardware / Drivers** | `my_robot_base` | Motor controller nodes, LiDAR/camera drivers, microcontroller bridges |
| **Navigation** | `my_robot_navigation` | Nav2 costmap configs, behavior trees, AMCL localization parameters |

