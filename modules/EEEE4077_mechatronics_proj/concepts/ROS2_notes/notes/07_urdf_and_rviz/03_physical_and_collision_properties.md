# 03. Physical & Collision Properties

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Adding-Physical-and-Collision-Properties-to-a-URDF-Model.rst`](../../ros2_documentation/source/Tutorials/Intermediate/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model.rst)  
> - Web: [Adding Physical and Collision Properties](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model.html)

---

## 1. The 3 Aspects of Every Functional Link

A link in a production robot requires three distinct sub-tags:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. <visual>:   High-poly CAD meshes/colors for human eyes   │
├─────────────────────────────────────────────────────────────┤
│ 2. <collision>: Simplified geometric primitives for physics │
├─────────────────────────────────────────────────────────────┤
│ 3. <inertial>:  Mass + Inertia tensor for dynamics/forces   │
└─────────────────────────────────────────────────────────────┘
```

> [!WARNING]
> **Performance Rule of Thumb:** Never use high-polygon CAD meshes for `<collision>` tags! It causes physics engines (Gazebo, Isaac Sim) and motion planners (MoveIt2, Nav2) to crawl. Always wrap your visual parts with simple geometric bounding shapes (`<box>`, `<cylinder>`, `<sphere>`).

---

## 2. Link Structure with Collision & Inertial

```xml
<link name="chassis">
  <!-- 1. Visual (How it looks) -->
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://my_robot_description/meshes/chassis.dae"/>
    </geometry>
  </visual>

  <!-- 2. Collision (Simplified bounding box for collision detection) -->
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.5 0.3 0.15"/>
    </geometry>
  </collision>

  <!-- 3. Inertial (Physical mass and resistance to rotation) -->
  <inertial>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <mass value="5.0"/> <!-- Mass in kilograms -->
    <inertia ixx="0.047" ixy="0.0" ixz="0.0"
             iyy="0.114" iyz="0.0"
             izz="0.142"/>
  </inertial>
</link>
```

---

## 3. Moment of Inertia Formulas Cheatsheet

For physics engines to simulate realistic acceleration without instability, calculate inertias using these formulas:

### 1. Solid Box (width $w$, height $h$, depth $d$, mass $m$):
$$I_{xx} = \frac{m}{12}(h^2 + d^2), \quad I_{yy} = \frac{m}{12}(w^2 + d^2), \quad I_{zz} = \frac{m}{12}(w^2 + h^2)$$

### 2. Solid Cylinder (radius $r$, height $h$ along $z$ axis, mass $m$):
$$I_{xx} = I_{yy} = \frac{m}{12}(3r^2 + h^2), \quad I_{zz} = \frac{m}{2}r^2$$

### 3. Solid Sphere (radius $r$, mass $m$):
$$I_{xx} = I_{yy} = I_{zz} = \frac{2}{5}mr^2$$

