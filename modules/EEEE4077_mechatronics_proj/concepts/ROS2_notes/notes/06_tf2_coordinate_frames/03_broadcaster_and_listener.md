# 03. Dynamic Broadcaster & Transform Listener

> **Raw Doc References:**  
> - Local: [`ros2_documentation/.../Writing-A-Tf2-Broadcaster-Py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.rst)  
> - Local: [`ros2_documentation/.../Writing-A-Tf2-Listener-Py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.rst)  
> - Web: [Writing a broadcaster & listener (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html)

---

## 1. Dynamic Broadcaster: Moving Frames

When a coordinate frame **moves continuously** over time (such as `odom` $\rightarrow$ `base_link` as a robot drives), we publish continuous updates on the `/tf` topic via `TransformBroadcaster`.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


class DynamicBroadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)

        # Listen to position topic and broadcast corresponding TF
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.handle_turtle_pose,
            10
        )

    def handle_turtle_pose(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'turtle1'

        # Set 2D position
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        # Set orientation from yaw angle (theta)
        import math
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(msg.theta / 2.0)
        t.transform.rotation.w = math.cos(msg.theta / 2.0)

        self.tf_broadcaster.sendTransform(t)
```

---

## 2. Transform Listener: Querying Spatial Offsets

To find out where one frame is relative to another (e.g. *"Where is `turtle2` relative to `turtle1`?"*), we create a **`Buffer`** and attach a **`TransformListener`**.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):

    def __init__(self):
        super().__init__('frame_listener')
        # 1. Create Buffer (caches transforms in memory)
        self.tf_buffer = Buffer()
        # 2. Attach Listener (subscribes to /tf and /tf_static in the background)
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.publisher = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.timer = self.create_timer(0.05, self.on_timer)  # 20 Hz loop

    def on_timer(self):
        try:
            # Query the latest transform from turtle1 into turtle2 frame
            t = self.tf_buffer.lookup_transform(
                target_frame='turtle2',  # Reference frame
                source_frame='turtle1',  # Frame to locate
                time=rclpy.time.Time(),  # Latest available time
                timeout=rclpy.duration.Duration(seconds=0.05)
            )

            # Compute tracking velocity based on transform offset
            msg = Twist()
            msg.linear.x = 0.5 * (t.transform.translation.x ** 2 + t.transform.translation.y ** 2) ** 0.5
            import math
            msg.angular.z = 1.0 * math.atan2(t.transform.translation.y, t.transform.translation.x)
            self.publisher.publish(msg)

        except TransformException as ex:
            self.get_logger().info(f'Could not transform turtle1 to turtle2: {ex}')
```

