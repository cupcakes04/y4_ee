# 05. Robot State Publisher & RViz2 Setup

> **Raw Doc References:**  
> - Local: [`ros2_documentation/.../Using-URDF-with-Robot-State-Publisher-py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.rst)  
> - Local: [`ros2_documentation/.../RViz-User-Guide.rst`](../../ros2_documentation/source/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.rst)  
> - Web: [Using URDF with Robot State Publisher](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.html)

---

## 1. Mental Model: The Forward Kinematics Pipeline

```
  my_robot.urdf (XML string) ───┐
                                ▼
                       [robot_state_publisher] ───(/tf)───> [RViz2 3D Canvas]
                                ▲
  [/joint_states topic] ────────┘
  (Angles from joint_state_publisher_gui or hardware encoders)
```

1. **`robot_state_publisher` (RSP):** Reads the URDF string (`robot_description` parameter) and listens to `/joint_states`. It computes 3D forward kinematics for all links and publishes their coordinate frames to `/tf`.
2. **`joint_state_publisher_gui`:** A testing GUI with sliders that simulates motor encoders by publishing test angles to `/joint_states`.
3. **`rviz2`:** The 3D visualizer that listens to `/tf` and renders the robot mesh, sensor markers, and camera frames.

---

## 2. All-in-One RViz2 Display Launch File

Save as `launch/display_rviz_launch.py`:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot_description')
    urdf_path = os.path.join(pkg_share, 'urdf', 'my_robot.urdf')

    # Read the URDF file into memory
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    # 1. Robot State Publisher (calculates forward kinematics and /tf)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 2. Joint State Publisher GUI (slider window to move joints)
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # 3. RViz2 3D Visualizer
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        rsp_node,
        jsp_gui_node,
        rviz_node
    ])
```

---

## 3. Initial RViz2 Configuration Checklist

When RViz2 opens for the first time, the screen will be dark with an empty grid. Follow this 4-step checklist:

1. **Set `Fixed Frame`:** In the left *Displays* panel under *Global Options*, set `Fixed Frame` to `base_link` (or `base_footprint`).
2. **Add `RobotModel` Display:** Click **Add** (bottom left) $\rightarrow$ choose **RobotModel** $\rightarrow$ OK.
   * Under *RobotModel* properties, ensure *Description Topic* is set to `/robot_description`.
3. **Add `TF` Display:** Click **Add** $\rightarrow$ choose **TF** $\rightarrow$ OK to view coordinate frame axes ($X=\text{Red}, Y=\text{Green}, Z=\text{Blue}$).
4. **Save Configuration:** Click **File $\rightarrow$ Save Config As** $\rightarrow$ save to `my_robot_description/rviz/view_robot.rviz`.

Next time, you can launch RViz automatically with your saved layout:
```python
Node(
    package='rviz2',
    executable='rviz2',
    arguments=['-d', '/path/to/view_robot.rviz']
)
```

