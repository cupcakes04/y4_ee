# 05. MessageFilters (Sensor Sync) & tf2 Debugging

> **Raw Doc References:**  
> - Local: [`ros2_documentation/.../Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter.rst)  
> - Local: [`ros2_documentation/.../Debugging-Tf2-Problems.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.rst)  
> - Web: [tf2 MessageFilter](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter.html)

---

## 1. The Sensor Sync Race Condition

> [!IMPORTANT]
> **The Problem:**  
> A LiDAR or camera publishes a point message at timestamp $t$. Your node receives it instantly in a topic callback and tries to transform it into `odom` or `map`.  
> However, because odometry and wheel encoders publish on different threads, the transform for timestamp $t$ **has not arrived on `/tf` yet**!  
> Calling `lookup_transform` immediately crashes or drops the point.

**The Solution:** Use `tf2_ros.MessageFilter`.  
It holds incoming sensor messages in a queue and **only calls your callback when the required transform has arrived in the tf2 buffer!**

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
from message_filters import Subscriber
from tf2_ros.message_filter import MessageFilter


class SynchronizedSensorNode(Node):

    def __init__(self):
        super().__init__('synchronized_sensor_node')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 1. MessageFilter subscriber (replaces create_subscription)
        self.point_sub = Subscriber(self, PointStamped, 'sensor_point')

        # 2. Wrap subscriber in MessageFilter targeting 'map' frame
        self.tf_filter = MessageFilter(
            self.point_sub,
            self.tf_buffer,
            'map',      # Target frame required before firing
            10,         # Queue size
            self
        )

        # 3. Register callback with the filter
        self.tf_filter.registerCallback(self.point_callback)

    def point_callback(self, point_msg):
        # 100% Guaranteed that transform from point_msg frame to 'map' is present!
        transformed_point = self.tf_buffer.transform(point_msg, 'map')
        self.get_logger().info(
            f'Point in map frame: x={transformed_point.point.x:.2f}, y={transformed_point.point.y:.2f}'
        )
```

---

## 2. The 3-Step tf2 Debugging Protocol

When a node logs: *"Could not transform frame A to frame B"*:

### Step 1: Generate Visual Tree (`view_frames`)
```bash
ros2 run tf2_tools view_frames
# Generates 'frames.pdf' in your terminal's current directory.
evince frames.pdf
```
Inspect the diagram for:
1. **Disconnected components:** Are there two separate trees that don't connect?
2. **0.0 Hz broadcasters:** Did a node crash or forget to send timestamps?
3. **Leading slashes:** Did someone name a frame `/base_link` instead of `base_link`?

### Step 2: Live Transform Echo (`tf2_echo`)
To see the continuous position and orientation updates between two frames in real-time:
```bash
ros2 run tf2_ros tf2_echo map laser_frame
```

### Step 3: Frequency & Latency Monitor (`tf2_monitor`)
To check if odometry or static transforms are arriving too slowly:
```bash
ros2 run tf2_ros tf2_monitor odom base_link
```

