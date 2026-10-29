# Communication: Actions (Goal, Feedback, & Result)

> **Doc References:**  
> - Local (CLI Concepts): [`ros2_documentation/.../Understanding-ROS2-Actions.rst`](../../ros2_documentation/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.rst)  
> - Local (Creating Action): [`ros2_documentation/.../Creating-an-Action.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Creating-an-Action.rst)  
> - Local (Intermediate Python): [`ros2_documentation/.../Writing-an-Action-Server-Client/Py.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.rst)  
> - Local (Intermediate C++): [`ros2_documentation/.../Writing-an-Action-Server-Client/Cpp.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.rst)  
> - Web: [Understanding ROS 2 Actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)

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

## 2. Defining Custom Actions (`.action` schema)

Custom actions are defined in `.action` files inside an `action/` directory in an `ament_cmake` package.
The file is divided into **three parts** separated by `---`:

```text
# 1. Goal (What the client requests)
int32 order
---
# 2. Result (What the server sends back on completion)
int32[] sequence
---
# 3. Feedback (What the server periodically streams during execution)
int32[] partial_sequence
```

### Build Setup for Custom Action Package:
In `package.xml`:
```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

In `CMakeLists.txt`:
```cmake
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/Fibonacci.action"
)

ament_package()
```

---

## 3. Python Implementation (`rclpy.action`)

### Python Action Server (with Cancellation Support & Multi-Threading)
> [!IMPORTANT]
> Because action execution is long-running (loops with delays), if you run on a default SingleThreadedExecutor without a `ReentrantCallbackGroup`, cancel requests will be blocked and cannot be processed until the goal finishes!

```python
import time
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Received goal request with order {goal_request.order}')
        # Validate goal
        if goal_request.order < 0:
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            # Check if client requested cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = Fibonacci.Result()
                result.sequence = feedback_msg.partial_sequence
                return result

            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1]
            )
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    action_server = FibonacciActionServer()
    executor = MultiThreadedExecutor()
    rclpy.spin(action_server, executor=executor)
    action_server.destroy_node()
    rclpy.shutdown()
```

### Python Action Client Skeleton
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from custom_action_interfaces.action import Fibonacci


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        self._action_client.wait_for_server()
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback received: {feedback_msg.feedback.partial_sequence}')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)
```

---

## 4. C++ Implementation (`rclcpp_action`)

### C++ Action Server Skeleton
```cpp
#include <functional>
#include <memory>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "custom_action_interfaces/action/fibonacci.hpp"

class FibonacciActionServer : public rclcpp::Node
{
public:
  using Fibonacci = custom_action_interfaces::action::Fibonacci;
  using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;

  FibonacciActionServer() : Node("fibonacci_action_server")
  {
    using namespace std::placeholders;

    this->action_server_ = rclcpp_action::create_server<Fibonacci>(
      this,
      "fibonacci",
      std::bind(&FibonacciActionServer::handle_goal, this, _1, _2),
      std::bind(&FibonacciActionServer::handle_cancel, this, _1),
      std::bind(&FibonacciActionServer::handle_accepted, this, _1));
  }

private:
  rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;

  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID & uuid,
    std::shared_ptr<const Fibonacci::Goal> goal)
  {
    (void)uuid;
    RCLCPP_INFO(this->get_logger(), "Received goal request with order %d", goal->order);
    if (goal->order < 0) {
      return rclcpp_action::GoalResponse::REJECT;
    }
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handle_cancel(
    const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    (void)goal_handle;
    RCLCPP_INFO(this->get_logger(), "Received request to cancel goal");
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    // Execution must run in a separate thread to avoid blocking ROS executor
    std::thread{std::bind(&FibonacciActionServer::execute, this, std::placeholders::_1), goal_handle}.detach();
  }

  void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    RCLCPP_INFO(this->get_logger(), "Executing goal");
    const auto goal = goal_handle->get_goal();
    auto feedback = std::make_shared<Fibonacci::Feedback>();
    auto & sequence = feedback->partial_sequence;
    sequence.push_back(0);
    sequence.push_back(1);
    auto result = std::make_shared<Fibonacci::Result>();

    for (int i = 1; (i < goal->order) && rclcpp::ok(); ++i) {
      if (goal_handle->is_canceling()) {
        result->sequence = sequence;
        goal_handle->canceled(result);
        RCLCPP_INFO(this->get_logger(), "Goal canceled");
        return;
      }
      sequence.push_back(sequence[i] + sequence[i - 1]);
      goal_handle->publish_feedback(feedback);
      std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    if (rclcpp::ok()) {
      result->sequence = sequence;
      goal_handle->succeed(result);
      RCLCPP_INFO(this->get_logger(), "Goal succeeded");
    }
  }
};
```

### C++ Action Client Skeleton
```cpp
#include <chrono>
#include <future>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "custom_action_interfaces/action/fibonacci.hpp"

class FibonacciActionClient : public rclcpp::Node
{
public:
  using Fibonacci = custom_action_interfaces::action::Fibonacci;
  using GoalHandleFibonacci = rclcpp_action::ClientGoalHandle<Fibonacci>;

  FibonacciActionClient() : Node("fibonacci_action_client")
  {
    this->client_ptr_ = rclcpp_action::create_client<Fibonacci>(this, "fibonacci");
  }

  void send_goal(int order)
  {
    if (!this->client_ptr_->wait_for_action_server(std::chrono::seconds(10))) {
      RCLCPP_ERROR(this->get_logger(), "Action server not available after waiting");
      return;
    }

    auto goal_msg = Fibonacci::Goal();
    goal_msg.order = order;

    auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();
    send_goal_options.goal_response_callback =
      [this](const GoalHandleFibonacci::SharedPtr & goal_handle) {
        if (!goal_handle) {
          RCLCPP_INFO(this->get_logger(), "Goal was rejected by server");
        } else {
          RCLCPP_INFO(this->get_logger(), "Goal accepted by server, waiting for result");
        }
      };

    send_goal_options.feedback_callback =
      [this](GoalHandleFibonacci::SharedPtr, const std::shared_ptr<const Fibonacci::Feedback> feedback) {
        RCLCPP_INFO(this->get_logger(), "Received feedback: %zu elements in sequence", feedback->partial_sequence.size());
      };

    send_goal_options.result_callback =
      [this](const GoalHandleFibonacci::WrappedResult & result) {
        switch (result.code) {
          case rclcpp_action::ResultCode::SUCCEEDED:
            break;
          case rclcpp_action::ResultCode::ABORTED:
            RCLCPP_ERROR(this->get_logger(), "Goal was aborted");
            return;
          case rclcpp_action::ResultCode::CANCELED:
            RCLCPP_ERROR(this->get_logger(), "Goal was canceled");
            return;
          default:
            RCLCPP_ERROR(this->get_logger(), "Unknown result code");
            return;
        }
        RCLCPP_INFO(this->get_logger(), "Result received!");
      };

    this->client_ptr_->async_send_goal(goal_msg, send_goal_options);
  }

private:
  rclcpp_action::Client<Fibonacci>::SharedPtr client_ptr_;
};
```

---

## 5. CLI Quick Lookup: Inspecting Actions

| Task | Command |
| :--- | :--- |
| **List action servers** | `ros2 action list` (add `-t` for type) |
| **Inspect action structure** | `ros2 interface show custom_action_interfaces/action/Fibonacci` |
| **Inspect action endpoints** | `ros2 action info /fibonacci` |
| **Send goal from terminal** | `ros2 action send_goal /fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"` |
| **Send goal with live feedback** | `ros2 action send_goal --feedback /fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"` |
