# 02. Movable Joints & Joint States

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Building-a-Movable-Robot-Model-with-URDF.rst`](../../ros2_documentation/source/Tutorials/Intermediate/URDF/Building-a-Movable-Robot-Model-with-URDF.rst)  
> - Web: [Building a Movable Robot Model with URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Building-a-Movable-Robot-Model-with-URDF.html)

---

## 1. The 4 Essential Joint Types

Joints define how a child link moves relative to its parent:

| Joint Type | Motion Allowed | Angle / Distance Limits | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **`fixed`** | No motion (rigid connection) | None | Bolted sensors (LiDAR, camera, IMU) |
| **`continuous`** | Continuous $360^\circ$ rotation | Unlimited rotation | Drive wheels, continuous rollers |
| **`revolute`** | Rotation around an axis | Requires `<limit>` tags | Robot arm elbows, steering knuckles |
| **`prismatic`** | Linear sliding motion | Requires `<limit>` tags | Gantry lifts, linear slides, grippers |

---

## 2. Defining Continuous & Revolute Joints in XML

```xml
<!-- 1. Continuous Wheel Joint (Rotates around Y-axis) -->
<joint name="right_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child link="right_wheel"/>
  <origin xyz="0.0 -0.22 0.0" rpy="-1.5708 0 0"/>
  <!-- Axis of rotation: z-axis of the rotated frame -->
  <axis xyz="0 0 1"/>
</joint>

<!-- 2. Revolute Arm Joint (Limited to -90 to +90 degrees) -->
<joint name="arm_elbow_joint" type="revolute">
  <parent link="arm_base_link"/>
  <child link="forearm_link"/>
  <origin xyz="0.0 0.0 0.3" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <!-- Limit attributes are MANDATORY for revolute and prismatic joints! -->
  <limit lower="-1.5708" upper="1.5708" effort="1000.0" velocity="0.5"/>
</joint>
```

---

## 3. The `/joint_states` Bridge & `joint_state_publisher_gui`

How does ROS 2 know what angle the wheel or arm is currently at?

```
 Motor Encoders ───> [/joint_states topic] ───> [robot_state_publisher] ───> [/tf]
```

1. **`sensor_msgs/msg/JointState`:** Topic broadcasting the current angle (position, velocity, effort) of every movable joint.
2. **`joint_state_publisher_gui`:** A debugging tool that provides interactive sliders in a GUI window. As you move the sliders, it publishes `/joint_states` so you can watch your robot arm bend and wheels turn in RViz before writing any motor driver code!

