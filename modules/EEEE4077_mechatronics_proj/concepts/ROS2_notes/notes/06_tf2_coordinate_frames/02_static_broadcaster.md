# 02. Static Transform Broadcaster

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Writing-A-Tf2-Static-Broadcaster-Py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.rst)  
> - Web: [Writing a static broadcaster (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html)

---

## 1. When to Use Static Transforms?

Use a **Static Transform** whenever the spatial relationship between two frames is **rigid and permanently fixed** (e.g. a LiDAR bolted 20 cm in front and 15 cm above the robot chassis).

* Published on the `/tf_static` topic (using a `Transient Local` QoS profile so it is delivered once and cached).
* Highly efficient: nodes don't waste CPU or network bandwidth continuously republishing unchanged offsets.

---

## 2. Option A: Zero-Code (CLI or Launch File)

You almost never need to write custom Python/C++ code for static sensors! ROS 2 includes a built-in static publisher executable:

### Terminal Command:
```bash
ros2 run tf2_ros static_transform_publisher --x 0.2 --y 0.0 --z 0.15 --yaw 0.0 --pitch 0.0 --roll 0.0 --frame-id base_link --child-frame-id laser_frame
```

### In a Python Launch File:
```python
from launch_ros.actions import Node

static_laser_tf = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_laser_broadcaster',
    arguments=[
        '--x', '0.2',
        '--y', '0.0',
        '--z', '0.15',
        '--yaw', '0.0',
        '--pitch', '0.0',
        '--roll', '0.0',
        '--frame-id', 'base_link',
        '--child-frame-id', 'laser_frame'
    ]
)
```

---

## 3. Option B: Python Node (`StaticTransformBroadcaster`)

If your static transform parameters are computed programmatically:

```python
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


def euler_to_quaternion(roll, pitch, yaw):
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)

    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    qw = cr * cp * cy + sr * sp * sy
    return qx, qy, qz, qw


class StaticFramePublisher(Node):

    def __init__(self):
        super().__init__('static_frame_publisher')
        self._tf_publisher = StaticTransformBroadcaster(self)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser_frame'

        t.transform.translation.x = 0.2
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.15

        qx, qy, qz, qw = euler_to_quaternion(0.0, 0.0, 0.0)
        t.transform.rotation.x = qx
        t.transform.rotation.y = qy
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw

        self._tf_publisher.sendTransform(t)
        self.get_logger().info('Published static transform base_link -> laser_frame')
```

