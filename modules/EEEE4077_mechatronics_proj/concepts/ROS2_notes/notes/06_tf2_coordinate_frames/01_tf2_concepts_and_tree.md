# 01. tf2 Concepts & The Coordinate Frame Tree

> **Raw Doc References:**  
> - Local: [`ros2_documentation/.../Introduction-To-Tf2.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.rst)  
> - Local: [`ros2_documentation/.../Tf2-Main.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Tf2-Main.rst)  
> - Web: [Introduction to tf2](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)

---

## 1. Mental Model: Why tf2?

A robot consists of dozens of sensors and links (LiDAR, camera, wheels, robot base, arm gripper). Each produces data in its own **local coordinate frame**:
* The LiDAR says: *"Obstacle detected at $(x=2.0, y=0.5)$ relative to `laser_frame`."*
* The Camera says: *"Human face detected at $(x=0.1, y=1.2, z=0.8)$ relative to `camera_optical_frame`."*
* The Navigation Stack needs to know: *"Where are these obstacles in the global building map (`map`) so I don't crash?"*

**`tf2`** maintains a continuous, time-buffered tree of 3D spatial transformations between all coordinate frames. It handles the matrix mathematics, rotations, and time synchronization automatically.

---

## 2. Standard Frame Tree Hierarchy (REP 105)

Every modern ROS 2 mobile robot follows the REP 105 coordinate convention:

```
       map           <-- Global world fixed frame (SLAM / GPS, discrete jumps)
        │
       odom          <-- Continuous odometry reference (smooth, continuous, drifts over time)
        │
   base_footprint    <-- Ground projection of the robot body (z=0 on floor)
        │
    base_link        <-- Physical body/chassis reference of the robot
   ┌────┴────┐
laser     camera     <-- Sensor mounting positions
```

### The 3 Ground Rules of tf2 Trees:
1. **Tree topology only:** A parent frame can have multiple children (e.g. `base_link` can be parent to `laser` and `camera`), but **each child frame can have at most ONE parent frame**.
2. **No cycles:** Closed loops are mathematically illegal in tf2 trees.
3. **No leading slashes:** Frame names must **never** start with `/`. Use `base_link`, not `/base_link`!

---

## 3. Transformations: Translation + Rotation (Quaternions)

Every transform between a parent and child frame consists of:
1. **Translation Vector:** $(x, y, z)$ in meters.
2. **Rotation:** Represented as a unit quaternion $(x, y, z, w)$ to avoid gimbal lock.

### Quick Euler $\leftrightarrow$ Quaternion Mental Model:
* Roll (tilt side-to-side around X axis)
* Pitch (tilt forward/backward around Y axis)
* Yaw (turn left/right around Z axis — primary rotation for 2D mobile robots)
* Identity quaternion (zero rotation): $(x=0.0, y=0.0, z=0.0, w=1.0)$.

