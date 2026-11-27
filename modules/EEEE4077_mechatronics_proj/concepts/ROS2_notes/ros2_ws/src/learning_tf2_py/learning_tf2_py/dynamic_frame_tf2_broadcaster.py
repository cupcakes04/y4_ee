#!/usr/bin/env python3
"""
Practical tf2 Sample 3: Dynamic Sub-Frame Broadcaster (The 'Carrot' Frame)

Publishes a moving child frame (e.g. 'carrot1') relative to another moving frame
(e.g. 'turtle1'). Demonstrates multi-level frame hierarchies in the tf tree:
    world  -->  turtle1  -->  carrot1

Usage:
    ros2 run learning_tf2_py dynamic_frame_tf2_broadcaster
    ros2 run learning_tf2_py dynamic_frame_tf2_broadcaster --ros-args -p parent_frame:=turtle1 -p child_frame:=carrot1 -p radius:=1.5
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class DynamicFrameTF2Broadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')

        # Configurable parameters
        self.declare_parameter('parent_frame', 'turtle1')
        self.declare_parameter('child_frame', 'carrot1')
        self.declare_parameter('radius', 1.5)        # Orbit radius in meters
        self.declare_parameter('orbit_speed', 1.0)   # Orbit angular velocity (rad/s)
        self.declare_parameter('mode', 'orbit')       # 'orbit' or 'fixed_ahead'

        self.parent_frame = self.get_parameter('parent_frame').get_parameter_value().string_value
        self.child_frame = self.get_parameter('child_frame').get_parameter_value().string_value
        self.radius = self.get_parameter('radius').get_parameter_value().double_value
        self.orbit_speed = self.get_parameter('orbit_speed').get_parameter_value().double_value
        self.mode = self.get_parameter('mode').get_parameter_value().string_value

        self.tf_broadcaster = TransformBroadcaster(self)

        # 30 Hz timer to broadcast moving subframe
        self.timer = self.create_timer(1.0 / 30.0, self.broadcast_timer_callback)
        self.start_time = self.get_clock().now()

        self.get_logger().info(
            f'Broadcasting sub-frame: {self.parent_frame} -> {self.child_frame} (mode={self.mode}, radius={self.radius}m)'
        )

    def broadcast_timer_callback(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self.parent_frame
        t.child_frame_id = self.child_frame

        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        if self.mode == 'orbit':
            # Revolves in a circle around parent turtle
            angle = self.orbit_speed * elapsed
            t.transform.translation.x = self.radius * math.cos(angle)
            t.transform.translation.y = self.radius * math.sin(angle)
            t.transform.translation.z = 0.0
        else:
            # Fixed 1.5 meters directly in front of the turtle
            t.transform.translation.x = self.radius
            t.transform.translation.y = 0.0
            t.transform.translation.z = 0.0

        # Identity orientation (relative to parent)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = DynamicFrameTF2Broadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

