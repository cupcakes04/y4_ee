# 01. Building a Visual Robot Model with URDF

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Building-a-Visual-Robot-Model-with-URDF-from-Scratch.rst`](../../ros2_documentation/source/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.rst)  
> - Web: [Building a Visual Robot Model with URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html)

---

## 1. Mental Model: What is URDF?

URDF (**Unified Robot Description Format**) is an XML schema describing the kinematic tree and physical geometry of a robot.

The two fundamental building blocks are:
1. **`<link>`:** Represents a rigid body part (chassis, wheel, laser housing, gripper).
2. **`<joint>`:** Connects a parent link to a child link, defining their spatial offset and how the child can move relative to the parent.

```
       [base_link] (chassis)
            │
            ▼ (fixed joint)
       [laser_link] (sensor housing)
```

---

## 2. Minimal Visual URDF Example

Save as `urdf/simple_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">

  <!-- 1. Define Materials (Colors) -->
  <material name="blue">
    <color rgba="0.0 0.0 0.8 1.0"/>
  </material>

  <material name="white">
    <color rgba="1.0 1.0 1.0 1.0"/>
  </material>

  <!-- 2. Base Link (Chassis) -->
  <link name="base_link">
    <visual>
      <geometry>
        <!-- Box size: length (x), width (y), height (z) in meters -->
        <box size="0.6 0.4 0.2"/>
      </geometry>
      <!-- Origin relative to link center -->
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <material name="blue"/>
    </visual>
  </link>

  <!-- 3. Sensor Link (Cylinder) -->
  <link name="laser_link">
    <visual>
      <geometry>
        <!-- Cylinder: radius and length (height) in meters -->
        <cylinder radius="0.05" length="0.1"/>
      </geometry>
      <material name="white"/>
    </visual>
  </link>

  <!-- 4. Joint Connecting Base to Sensor -->
  <joint name="base_to_laser_joint" type="fixed">
    <parent link="base_link"/>
    <child link="laser_link"/>
    <!-- Position of laser relative to base_link: 20cm ahead, 25cm high -->
    <origin xyz="0.2 0.0 0.25" rpy="0 0 0"/>
  </joint>

</robot>
```

---

## 3. Geometric Primitives Available in URDF

| Shape Tag | Attributes | Example |
| :--- | :--- | :--- |
| `<box>` | `size="x y z"` | `<box size="0.5 0.3 0.2"/>` |
| `<cylinder>` | `radius="r" length="l"` | `<cylinder radius="0.05" length="0.1"/>` |
| `<sphere>` | `radius="r"` | `<sphere radius="0.04"/>` |
| `<mesh>` | `filename="package://pkg/meshes/part.dae"` | High-poly CAD visual meshes (`.stl`, `.dae`) |

---

## 4. Origin & Orientation (`xyz` and `rpy`)

* **`xyz="x y z"`:** Linear translation in meters along the parent's axes.
* **`rpy="roll pitch yaw"`:** Angular rotation in radians around the X, Y, and Z axes:
  * Roll: Tilt sideways
  * Pitch: Tilt nose up/down
  * Yaw: Rotate left/right (counter-clockwise)
  * $\pi/2 \text{ rad} \approx 1.5708 \text{ rad} = 90^\circ$

