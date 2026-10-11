# Communication: Services (Service & Client)

> **Doc References:**  
> - Local (Python): [`ros2_documentation/.../Writing-A-Simple-Py-Service-And-Client.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.rst)  
> - Local (C++): [`ros2_documentation/.../Writing-A-Simple-Cpp-Service-And-Client.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Service-And-Client.rst)  
> - Web: [Understanding ROS 2 Services](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)

---

## 1. Mental Model: Request & Response (1-to-1)

```
  [Client Node] ───(Request)───> [Service Server Node]
                <──(Response)───┘
```

- **Nature:** Two-way, point-to-point handshake.
- **Synchronous / Async:** Client asks for an action or calculation, Server computes and answers.
- **Use cases:** Triggering a computation, taking a single camera snapshot, resetting a simulation, configuring a mode.

---

## 2. Minimal Python Boilerplate (`rclpy`)

### Service Node Skeleton (Server)
```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        # create_service(srv_type, srv_name, callback)
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Request: a={request.a}, b={request.b} -> sum={response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MinimalService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Client Node Skeleton (Async Client)
```python
import sys
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        # create_client(srv_type, srv_name)
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service unavailable, waiting...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    node = MinimalClientAsync()
    
    # Send asynchronous request
    a, b = int(sys.argv[1]), int(sys.argv[2])
    future = node.send_request(a, b)
    
    # Spin until response arrives
    rclpy.spin_until_future_complete(node, future)
    response = future.result()
    node.get_logger().info(f'Result: {a} + {b} = {response.sum}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 3. C++ Equivalent Comparison (`rclcpp`)

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

// Service callback in C++
void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
         std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response) {
  response->sum = request->a + request->b;
}

// In Node constructor:
auto service = node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);
```

---

## 4. CLI Quick Lookup: Testing Services

| Task | Command |
| :--- | :--- |
| **List active services** | `ros2 service list` |
| **Check service type** | `ros2 service type /add_two_ints` |
| **Find services by type** | `ros2 service find example_interfaces/srv/AddTwoInts` |
| **Show interface fields** | `ros2 interface show example_interfaces/srv/AddTwoInts` |
| **Call service from CLI** | `ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 7}"` |
