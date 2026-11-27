from pathlib import Path
from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace


def generate_launch_description():
    launch_dir = Path(__file__).resolve().parent

    return LaunchDescription([
        # 1. Turtlesim World 1 (parameters defined inside launch description)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(launch_dir / 'turtlesim_world_1_launch.py')
            )
        ),

        # 2. Turtlesim World 2 (grouped under /turtlesim2 namespace, loading YAML parameters)
        GroupAction(
            actions=[
                PushRosNamespace('turtlesim2'),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        str(launch_dir / 'turtlesim_world_2_launch.py')
                    )
                ),
            ]
        ),

        # 3. TF Broadcaster & Listener (overriding default target_frame to carrot1)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(launch_dir / 'broadcaster_listener_launch.py')
            ),
            launch_arguments={'target_frame': 'carrot1'}.items()
        ),

        # 4. Mimic node (remapping /turtle2/pose -> /turtlesim2/turtle1/cmd_vel)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(launch_dir / 'mimic_launch.py')
            )
        ),

        # 5. Fixed frame broadcaster using EnvironmentVariable substitution
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(launch_dir / 'fixed_broadcaster_launch.py')
            )
        ),

        # 6. RViz visualization node
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(launch_dir / 'turtlesim_rviz_launch.py')
            )
        ),
    ])

