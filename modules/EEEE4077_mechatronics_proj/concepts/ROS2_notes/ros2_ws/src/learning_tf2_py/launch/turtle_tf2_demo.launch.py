#!/usr/bin/env python3
"""
Launch File: Complete tf2 Turtlesim Follower Demo

Spawns turtle2, starts dynamic broadcasters for turtle1 & turtle2,
starts a static sensor broadcaster on turtle1, and runs the listener
chaser node so turtle2 continuously tracks turtle1.
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # 1. Turtlesim simulator GUI node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),

        # 2. Dynamic tf2 broadcaster for turtle1 (publishes world -> turtle1)
        Node(
            package='learning_tf2_py',
            executable='turtle_tf2_broadcaster',
            name='turtle1_tf2_broadcaster',
            parameters=[{'turtlename': 'turtle1'}]
        ),

        # 3. Dynamic tf2 broadcaster for turtle2 (publishes world -> turtle2)
        Node(
            package='learning_tf2_py',
            executable='turtle_tf2_broadcaster',
            name='turtle2_tf2_broadcaster',
            parameters=[{'turtlename': 'turtle2'}]
        ),

        # 4. Static transform broadcaster: mounts a simulated laser 0.5m in front of turtle1
        Node(
            package='learning_tf2_py',
            executable='static_turtle_tf2_broadcaster',
            name='turtle1_laser_broadcaster',
            parameters=[{
                'frame_id': 'turtle1',
                'child_frame_id': 'turtle1_laser',
                'x': 0.5,
                'y': 0.0,
                'z': 0.1,
                'yaw': 0.0
            }]
        ),

        # 5. Spawn turtle2 at coordinates (x=2.0, y=2.0)
        ExecuteProcess(
            cmd=[
                'ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn',
                '{x: 2.0, y: 2.0, theta: 0.0, name: "turtle2"}'
            ],
            output='screen'
        ),

        # 6. tf2 Listener: computes spatial offset and commands turtle2 to chase turtle1
        Node(
            package='learning_tf2_py',
            executable='turtle_tf2_listener',
            name='turtle2_chaser',
            parameters=[{
                'follower_turtle': 'turtle2',
                'target_frame': 'turtle1'
            }]
        ),
    ])

