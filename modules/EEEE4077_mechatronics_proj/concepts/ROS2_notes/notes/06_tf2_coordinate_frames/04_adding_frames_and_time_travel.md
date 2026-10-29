# 04. Adding Dynamic Sub-Frames & Time Interpolation

> **Raw Doc References:**  
> - Local: [`ros2_documentation/.../Adding-A-Frame-Py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Adding-A-Frame-Py.rst)  
> - Local: [`ros2_documentation/.../Learning-About-Tf2-And-Time-Cpp.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Learning-About-Tf2-And-Time-Cpp.rst)  
> - Local: [`ros2_documentation/.../Time-Travel-With-Tf2-Cpp.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Time-Travel-With-Tf2-Cpp.rst)  
> - Web: [Adding a frame (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Adding-A-Frame-Py.html)

---

## 1. Adding Dynamic Moving Sub-Frames (e.g. Floating "Carrot" Frame)

Instead of just tracking a robot's body, you often want to track an offset point (such as a target "carrot" 2 meters in front of the robot, or a rotating camera gimbal).

```
  turtle1 (chassis) ────(offset 2.0m ahead)────> carrot1 (virtual target)
```

```python
import math
from geometry_msgs.msg import TransformStamped

t = TransformStamped()
t.header.stamp = self.get_clock().now().to_msg()
t.header.frame_id = 'turtle1'     # Parent frame is the turtle body
t.child_frame_id = 'carrot1'      # Child frame is our new floating carrot

# Move the carrot in an orbit around turtle1:
t.transform.translation.x = 2.0 * math.sin(self.get_clock().now().nanoseconds / 1e9)
t.transform.translation.y = 2.0 * math.cos(self.get_clock().now().nanoseconds / 1e9)
t.transform.translation.z = 0.0
t.transform.rotation.w = 1.0

self.tf_broadcaster.sendTransform(t)
```

Now any other node can directly command:
```python
self.tf_buffer.lookup_transform('turtle2', 'carrot1', rclpy.time.Time())
```
And `turtle2` will track the orbiting carrot instead of the turtle's center!

---

## 2. Time in tf2 & The 10-Second Buffer Ring

`tf2` buffers transforms across time (default ~10 seconds). This allows two different lookup modes:

```
Time:   t=0.0s ────> t=1.0s ────> t=2.0s ────> t=3.0s (Now)
Buffer: [   Stored Transforms Interpolated by tf2   ]
```

### Mode 1: Latest Available (`Time()` or `Time(seconds=0)`)
* *"Give me the most recent transform that has arrived in the buffer right now."*
* Great for general visualization, but introduces subtle timing errors when synchronizing with sensor readings recorded in the past.

### Mode 2: Specific Past Timestamp (`msg.header.stamp`)
* *"Give me the exact robot pose at timestamp $t$ when this camera frame was clicked."*
* `tf2` automatically looks at the transforms immediately before and after $t$ and **linearly interpolates** between them!

---

## 3. The Dreaded `ExtrapolationException` (And How to Fix It)

If your node queries a timestamp that is slightly ahead of the newest transform in the buffer:
```
Lookup would require extrapolation into the future. Requested time X but latest is Y
```

### The Fix: Non-Zero Timeout
Always pass a non-zero timeout (e.g., `50ms`) to `lookup_transform`:
```python
t = self.tf_buffer.lookup_transform(
    'map',
    'base_link',
    target_time,
    timeout=rclpy.duration.Duration(seconds=0.05)  # Waits up to 50ms for transform to arrive!
)
```
This gives the background listener thread time to receive the latest transform packets before raising an error.

