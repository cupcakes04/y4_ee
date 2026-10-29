# 04. Clean Modeling with Xacro (XML Macros)

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Using-Xacro-to-Clean-Up-a-URDF-File.rst`](../../ros2_documentation/source/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.rst)  
> - Web: [Using Xacro to Clean Up a URDF File](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)

---

## 1. Mental Model: Why Xacro?

Raw URDF is repetitive and hard to maintain:
* A 4-wheeled robot requires copy-pasting the exact same 30 lines of wheel XML 4 times.
* Changing wheel diameter requires hunting down and manually recalculating 10 different origin offsets and inertia formulas.
* A complete robot description quickly balloons past 1,000 lines in a single unmanageable file.

**Xacro (XML Macros)** compiles cleanly into standard URDF using:
1. **Properties:** Reusable constants (variables).
2. **Math Evaluation:** Calculations evaluated at compile-time via `${...}`.
3. **Macros:** Parameterized templates for repeated parts (wheels, legs, sensors).
4. **Includes:** Splitting the robot across clean modular files (`chassis.xacro`, `wheels.xacro`, `lidar.xacro`).

---

## 2. Practical Xacro Example (`robot.urdf.xacro`)

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="my_robot">

  <!-- 1. Include Modular Files -->
  <xacro:include filename="materials.xacro"/>

  <!-- 2. Properties (Variables) -->
  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="wheel_width" value="0.04"/>
  <xacro:property name="wheel_offset_y" value="0.18"/>

  <!-- 3. Reusable Inertia Macro -->
  <xacro:macro name="cylinder_inertia" params="m r h">
    <inertial>
      <mass value="${m}"/>
      <inertia ixx="${(m/12.0)*(3*r*r + h*h)}" ixy="0.0" ixz="0.0"
               iyy="${(m/12.0)*(3*r*r + h*h)}" iyz="0.0"
               izz="${(m/2.0)*(r*r)}"/>
    </inertial>
  </xacro:macro>

  <!-- 4. Parameterized Wheel Macro -->
  <xacro:macro name="wheel" params="prefix y_reflect">
    <link name="${prefix}_wheel_link">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <material name="black"/>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>
      <xacro:cylinder_inertia m="0.5" r="${wheel_radius}" h="${wheel_width}"/>
    </link>

    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${prefix}_wheel_link"/>
      <!-- Math expression evaluates offset: ${wheel_offset_y * y_reflect} -->
      <origin xyz="0.0 ${wheel_offset_y * y_reflect} 0.0" rpy="-1.5708 0 0"/>
      <axis xyz="0 0 1"/>
    </joint>
  </xacro:macro>

  <link name="base_link"/>

  <!-- 5. Instantiate Left and Right Wheels in Two Lines! -->
  <xacro:wheel prefix="left" y_reflect="1"/>
  <xacro:wheel prefix="right" y_reflect="-1"/>

</robot>
```

---

## 3. Loading Xacro in a Python Launch File

You do not need to pre-compile `.xacro` into `.urdf` manually before launching. Use `Command` to evaluate it dynamically at launch:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')

    # Evaluates 'xacro <file>' and captures the resulting XML string
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    return LaunchDescription([rsp_node])
```

