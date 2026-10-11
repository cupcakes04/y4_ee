# Communication: Parameters (Node Configuration)

> **Doc References:**  
> - Local (Python): [`ros2_documentation/.../Using-Parameters-In-A-Class-Python.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.rst)  
> - Local (CLI): [`ros2_documentation/.../Understanding-ROS2-Parameters.rst`](../../ros2_documentation/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.rst)  
> - Web: [Understanding ROS 2 Parameters](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)

---

## 1. Mental Model: Node-Scoped Configuration

- Parameters belong to a **specific node** (they are not global variables).
- Used to tune values without recompiling or restarting nodes (e.g., PID gains, camera FPS, motor gear ratio).
- Can be set on startup via CLI or YAML file, or updated live at runtime.

---

## 2. Minimal Python Boilerplate (`rclpy`)

```python
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult


class ParamNode(Node):

    def __init__(self):
        super().__init__('param_node')
        
        # 1. Declare parameter with default value
        self.declare_parameter('max_speed', 1.5)
        self.declare_parameter('robot_name', 'turtle_bot')

        # 2. Read parameter value
        speed = self.get_parameter('max_speed').value
        self.get_logger().info(f'Current speed limit: {speed}')

        # 3. Optional: Add callback to react when parameter is changed live
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'max_speed' and param.type_ == param.Type.DOUBLE:
                self.get_logger().info(f'Updated max_speed to: {param.value}')
        return SetParametersResult(successful=True)
```

---

## 3. Passing Parameters on Launch / Run

### From CLI during `ros2 run`:
```bash
ros2 run my_pkg my_node --ros-args -p max_speed:=2.5 -p robot_name:='fast_bot'
```

### From a YAML file:
```yaml
# params.yaml
param_node:
  ros__parameters:
    max_speed: 3.0
    robot_name: "custom_turtle"
```
```bash
ros2 run my_pkg my_node --ros-args --params-file params.yaml
```

---

## 4. CLI Quick Lookup: Managing Parameters Live

| Task | Command |
| :--- | :--- |
| **List parameters of all nodes** | `ros2 param list` |
| **Get value of parameter** | `ros2 param get /param_node max_speed` |
| **Set parameter at runtime** | `ros2 param set /param_node max_speed 2.0` |
| **Dump node parameters to YAML** | `ros2 param dump /param_node > params_backup.yaml` |
| **Load parameters from YAML** | `ros2 param load /param_node params_backup.yaml` |
