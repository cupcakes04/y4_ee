from pathlib import Path
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config_file = Path(__file__).resolve().parent / 'config' / 'turtlesim.yaml'

    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
            parameters=[str(config_file)],
        ),
    ])

