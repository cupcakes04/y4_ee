# Communication: Actions (Goal, Feedback, & Result)

> **Doc References:**  
> - Local (CLI Concepts): [`ros2_documentation/.../Understanding-ROS2-Actions.rst`](../../ros2_documentation/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.rst)  
> - Local (Intermediate Code): [`ros2_documentation/.../Writing-an-Action-Server-Client/Py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.rst)  
> - Web: [Understanding ROS 2 Actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)

> [!NOTE]
> In the official ROS 2 curriculum, **understanding and using Actions from the CLI** is part of **Beginner: CLI Tools**, whereas **writing custom Action definitions and servers** is the bridge into **Intermediate Tutorials**.

---

## 1. Mental Model: Long-Running & Preemptible Tasks

```
  [Action Client] ────(Goal Request)────> [Action Server]
                  <───(Goal Accepted)────┤
                  <───(Feedback Stream)──┤  (e.g., 20%, 40%, 60%...)
                  <───(Final Result)─────┘
```

- **Nature:** Built from Topics + Services under the hood.
- **Why not a service?** Services block and cannot report progress or be cancelled midway. Actions provide:
  1. **Goal Request / Response** (Server accepts/rejects).
  2. **Feedback Stream** (Periodic updates while executing).
  3. **Cancelability** (Client can abort early).
  4. **Final Result** (Returned on completion).
- **Use cases:** Navigating to a waypoint, robot arm trajectory execution, calibration routines.

---

## 2. Minimal Python Boilerplate (`rclpy.action`)

### Action Server Skeleton
```python
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
# Action interface has 3 parts: Goal, Feedback, Result
from example_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.sequence.append(feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Action Client Skeleton
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        self._action_client.wait_for_server()
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # Send goal with optional feedback callback
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback received: {feedback_msg.feedback.sequence}')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
```

---

## 3. CLI Quick Lookup: Inspecting Actions

| Task | Command |
| :--- | :--- |
| **List action servers** | `ros2 action list` (add `-t` for type) |
| **Inspect action structure** | `ros2 interface show example_interfaces/action/Fibonacci` |
| **Inspect action endpoints** | `ros2 action info /fibonacci` |
| **Send goal from terminal** | `ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}"` |
| **Send goal with live feedback** | `ros2 action send_goal --feedback /fibonacci example_interfaces/action/Fibonacci "{order: 5}"` |
