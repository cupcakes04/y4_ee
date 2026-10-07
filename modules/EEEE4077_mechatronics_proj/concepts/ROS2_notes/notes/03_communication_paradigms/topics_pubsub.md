# Communication: Topics (Publisher & Subscriber)

> **Doc References:**  
> - Local (Python): [`ros2_documentation/.../Writing-A-Simple-Py-Publisher-And-Subscriber.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.rst)  
> - Local (C++): [`ros2_documentation/.../Writing-A-Simple-Cpp-Publisher-And-Subscriber.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.rst)  
> - Web: [Understanding ROS 2 Topics](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)

---

## 1. Mental Model: Asynchronous Streaming (1-to-Many)

```
  [Publisher Node] ──(Topic: /topic_name)──> [Subscriber Node A]
                                        └──> [Subscriber Node B]
```

- **Nature:** Continuous, unidirectional streaming.
- **Decoupled:** Publishers broadcast without knowing who is listening; Subscribers read without knowing who produces.
- **Use cases:** Sensor data (LiDAR, camera, encoders, odometry), state telemetry, control velocity commands (`/cmd_vel`).

---

## 2. Minimal Python Boilerplate (`rclpy`)

### Publisher Node Skeleton
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # 1. Create publisher: (msg_type, topic_name, queue_size)
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        # 2. Create timer for periodic publishing
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Subscriber Node Skeleton
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # Create subscription: (msg_type, topic_name, callback, queue_size)
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 3. C++ Equivalent Comparison (`rclcpp`)

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

// Publisher
class MinimalPublisher : public rclcpp::Node {
public:
  MinimalPublisher() : Node("minimal_publisher") {
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(500),
      [this]() {
        auto msg = std_msgs::msg::String();
        msg.data = "Hello C++";
        publisher_->publish(msg);
      });
  }
private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};
```

---

## 4. CLI Quick Lookup: Inspecting Topics

| Task | Command |
| :--- | :--- |
| **List active topics** | `ros2 topic list` (add `-t` to display message types) |
| **Print live messages** | `ros2 topic echo /topic` |
| **Publish message manually** | `ros2 topic pub /topic std_msgs/msg/String "{data: 'hello'}"` |
| **Publish once and exit** | `ros2 topic pub --once /topic std_msgs/msg/String "{data: 'test'}"` |
| **Measure message rate** | `ros2 topic hz /topic` |
| **Measure bandwidth** | `ros2 topic bw /topic` |
| **Inspect topic type & info** | `ros2 topic info /topic -v` |
