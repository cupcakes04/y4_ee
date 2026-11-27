#!/usr/bin/env python3
"""
Launch File: tf2 Dynamic Sub-frame (Carrot Follower) Demo

Spawns turtle2, starts dynamic broadcasters for turtle1 & turtle2,
starts the orbiting 'carrot1' subframe attached to turtle1,
and configures turtle2 to chase 'carrot1' instead of turtle1's body!
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

        # 4. Dynamic sub-frame broadcaster: creates an orbiting 'carrot1' frame 1.5m from turtle1
        Node(
            package='learning_tf2_py',
            executable='dynamic_frame_tf2_broadcaster',
            name='carrot_broadcaster',
            parameters=[{
                'parent_frame': 'turtle1',
                'child_frame': 'carrot1',
                'radius': 1.5,
                'orbit_speed': 1.0,
                'mode': 'orbit'
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

        # 6. tf2 Listener: commands turtle2 to chase the orbiting 'carrot1' frame!
        Node(
            package='learning_tf2_py',
            executable='turtle_tf2_listener',
            name='turtle2_carrot_chaser',
            parameters=[{
                'follower_turtle': 'turtle2',
                'target_frame': 'carrot1'
            }]
        ),
    ])

