# 03. Event Handlers & Execution Lifecycle

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Using-Event-Handlers.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Launch/Using-Event-Handlers.rst)  
> - Web: [Using Event Handlers](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-Event-Handlers.html)

---

## 1. Mental Model: Sequential & Reactive Launch

By default, ROS 2 launch files start all nodes **concurrently (in parallel)**.
However, real robotic workflows often require:
* Spawning a sensor driver **only after** the robot hardware communication node has started.
* Automatically shutting down the entire launch tree when the primary mission node finishes or crashes.
* Emitting warnings or logs when specific processes exit.

**Event Handlers** listen to process lifecycle states and execute reactions.

---

## 2. Event Handler Recipes

### 1. Execute Action When Node Starts (`OnProcessStart`)
```python
from launch.actions import RegisterEventHandler, LogInfo
from launch.event_handlers import OnProcessStart

start_listener = RegisterEventHandler(
    OnProcessStart(
        target_action=turtlesim_node,
        on_start=[
            LogInfo(msg='Turtlesim node has started! Spawning telemetry...')
        ]
    )
)
```

### 2. Auto-Shutdown When Primary Node Exits (`OnProcessExit`)
In testing or mission execution, you want the launch file to clean up and exit when the main node finishes:

```python
from launch.actions import RegisterEventHandler, LogInfo, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown

shutdown_handler = RegisterEventHandler(
    OnProcessExit(
        target_action=teleop_node,
        on_exit=[
            LogInfo(msg='Teleop closed by user. Shutting down entire launch stack...'),
            EmitEvent(event=Shutdown(reason='Teleop closed'))
        ]
    )
)
```

### 3. Sequential Execution (Run Node B after Node A finishes)
```python
spawn_secondary_node = RegisterEventHandler(
    OnProcessExit(
        target_action=initial_calibration_node,
        on_exit=[
            LogInfo(msg='Calibration complete. Starting main controller...'),
            main_controller_node
        ]
    )
)
```

---

## 3. Assembling Event Handlers in `LaunchDescription`

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    sim = Node(package='turtlesim', executable='turtlesim_node')
    # ... handler definitions ...

    return LaunchDescription([
        sim,
        start_listener,
        shutdown_handler,
        spawn_secondary_node
    ])
```

