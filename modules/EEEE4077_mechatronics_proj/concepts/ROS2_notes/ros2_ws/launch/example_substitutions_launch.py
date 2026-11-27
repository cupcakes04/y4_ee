from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    # 1. Reference arguments as dynamic substitutions (evaluated at runtime)
    turtlesim_ns = LaunchConfiguration('turtlesim_ns')
    use_provided_red = LaunchConfiguration('use_provided_red')
    new_background_r = LaunchConfiguration('new_background_r')

    # 2. Declare launch arguments with defaults and descriptions (inspectable via --show-args)
    turtlesim_ns_launch_arg = DeclareLaunchArgument(
        'turtlesim_ns',
        default_value='turtlesim1',
        description='Top-level namespace for the turtlesim node'
    )

    use_provided_red_launch_arg = DeclareLaunchArgument(
        'use_provided_red',
        default_value='False',
        description='Whether to change the background red color via timer'
    )

    new_background_r_launch_arg = DeclareLaunchArgument(
        'new_background_r',
        default_value='200',
        description='New red channel value to apply if use_provided_red is true'
    )

    # 3. Turtlesim Node using dynamic namespace substitution
    turtlesim_node = Node(
        package='turtlesim',
        namespace=turtlesim_ns,
        executable='turtlesim_node',
        name='sim'
    )

    # 4. Process execution constructing CLI strings with substitutions:
    # Spawn a second turtle inside the dynamically namespaced simulation
    spawn_turtle = ExecuteProcess(
        cmd=[[
            'ros2 service call ',
            turtlesim_ns,
            '/spawn ',
            'turtlesim/srv/Spawn ',
            '"{x: 2, y: 2, theta: 0.2}"'
        ]],
        shell=True
    )

    # Initial parameter change
    change_background_r = ExecuteProcess(
        cmd=[[
            'ros2 param set ',
            turtlesim_ns,
            '/sim background_r ',
            '120'
        ]],
        shell=True
    )

    # 5. Conditional execution using PythonExpression inside TimerAction:
    # Evaluates (new_background_r == 200 and use_provided_red) dynamically at runtime
    change_background_r_conditioned = ExecuteProcess(
        condition=IfCondition(
            PythonExpression([
                new_background_r,
                ' == 200',
                ' and ',
                use_provided_red
            ])
        ),
        cmd=[[
            'ros2 param set ',
            turtlesim_ns,
            '/sim background_r ',
            new_background_r
        ]],
        shell=True
    )

    return LaunchDescription([
        turtlesim_ns_launch_arg,
        use_provided_red_launch_arg,
        new_background_r_launch_arg,
        turtlesim_node,
        spawn_turtle,
        change_background_r,
        TimerAction(
            period=2.0,
            actions=[change_background_r_conditioned],
        )
    ])

