# 02. Launch Arguments & Substitutions

> **Raw Doc Reference:**  
> - Local: [`ros2_documentation/.../Using-Substitutions.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Launch/Using-Substitutions.rst)  
> - Web: [Using Substitutions](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-Substitutions.html)

---

## 1. Mental Model: Why Substitutions? (The #1 Beginner Trap)

In ROS 2, `generate_launch_description()` only constructs an **abstract graph** of execution; it does not launch nodes immediately.  
When you declare an argument like:
```python
turtlesim_ns = LaunchConfiguration('turtlesim_ns')
```
`turtlesim_ns` is an **opaque future reference** that has no value until the user actually runs:
```bash
ros2 launch my_pkg my_launch.py turtlesim_ns:=turtlesim3
```

> [!CAUTION]
> **The Standard Python Trap:**  
> You **CANNOT** use native Python string operations on launch configurations:
> ```python
> # ❌ CRITICAL BUG: This will fail or yield unreadable object representations!
> file_path = os.path.join('/home/user', turtlesim_ns)
> if turtlesim_ns == 'turtlesim1':
>     ...
> ```
> To manipulate paths or expressions that depend on runtime arguments, you **must use ROS 2 Launch Substitutions**.

---

## 2. Declaring and Consuming Launch Arguments

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    # 1. Declare the argument (CLI configurable flag)
    background_r_arg = DeclareLaunchArgument(
        'background_r',
        default_value='255',
        description='Red channel for turtlesim background color'
    )

    # 2. Reference the argument as a substitution
    background_r = LaunchConfiguration('background_r')

    # 3. Pass it to node parameters
    sim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim',
        parameters=[{
            'background_r': background_r,
            'background_g': 86,
            'background_b': 240
        }]
    )

    return LaunchDescription([
        background_r_arg,
        sim_node
    ])
```

---

## 3. Dynamic Path Construction (`PathJoinSubstitution` & `FindPackageShare`)

Instead of hardcoding absolute paths or using `get_package_share_directory`, use substitutions so paths resolve dynamically on whatever machine the package is installed:

```python
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

# Dynamically resolves to: <install_dir>/share/my_pkg/config/<params_file>
config_file = PathJoinSubstitution([
    FindPackageShare('my_robot_bringup'),
    'config',
    LaunchConfiguration('params_file')  # e.g., 'nav2_params.yaml'
])
```

---

## 4. Runtime Python Expressions (`PythonExpression`)

To evaluate boolean flags or conditional expressions at runtime:

```python
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition, UnlessCondition

# Evaluate expression dynamically:
is_sim = IfCondition(
    PythonExpression(["'", LaunchConfiguration('use_sim'), "' == 'true'"])
)

# Launch node ONLY if condition is met
sim_node = Node(
    package='my_sim_pkg',
    executable='fake_sensor_node',
    condition=is_sim
)
```

---

## 5. CLI Lookup: Working with Arguments

```bash
# 1. Inspect what arguments a launch file accepts:
ros2 launch my_pkg my_launch.py --show-args

# 2. Pass arguments on CLI:
ros2 launch my_pkg my_launch.py background_r:=120 params_file:=custom.yaml
```

