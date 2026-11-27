#!/usr/bin/env python3
"""
Practical tf2 Sample 4: Transform Listener & Chaser Controller

Listens to the coordinate transform between two arbitrary frames in the tf tree
(by default: from target_frame to follower_turtle) using tf2_ros.Buffer and TransformListener,
then computes and publishes /turtle2/cmd_vel to follow the target frame in real time.

Usage:
    ros2 run learning_tf2_py turtle_tf2_listener
    ros2 run learning_tf2_py turtle_tf2_listener --ros-args -p follower_turtle:=turtle2 -p target_frame:=carrot1
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from geometry_msgs.msg import Twist
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class TurtleTF2Listener(Node):

    def __init__(self):
        super().__init__('turtle_tf2_listener')

        # Configurable follower and target frames
        self.declare_parameter('follower_turtle', 'turtle2')
        self.declare_parameter('target_frame', 'turtle1')
        self.declare_parameter('kp_linear', 0.8)
        self.declare_parameter('kp_angular', 2.5)

        self.follower_turtle = self.get_parameter('follower_turtle').get_parameter_value().string_value
        self.target_frame = self.get_parameter('target_frame').get_parameter_value().string_value
        self.kp_linear = self.get_parameter('kp_linear').get_parameter_value().double_value
        self.kp_angular = self.get_parameter('kp_angular').get_parameter_value().double_value

        # Step 1: Create the transform buffer ring (caches ~10s of transforms)
        self.tf_buffer = Buffer()

        # Step 2: Attach the TransformListener.
        # This spawns background subscriptions to /tf and /tf_static.
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Publisher for controlling the follower turtle
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            f'/{self.follower_turtle}/cmd_vel',
            10
        )

        # Control loop running at 25 Hz (every 40ms)
        self.timer = self.create_timer(0.04, self.on_control_loop)

        self.get_logger().info(
            f'Listener active: {self.follower_turtle} will chase target frame [{self.target_frame}]'
        )

    def on_control_loop(self):
        """Query spatial offset from follower to target and command velocities."""
        try:
            # Query transform from target_frame into follower_turtle's local frame
            # target_frame: reference frame (follower_turtle)
            # source_frame: frame to locate (target_frame)
            # time=rclpy.time.Time(): get latest available transform
            # timeout: wait up to 0.05 seconds for transform to arrive in buffer
            transform = self.tf_buffer.lookup_transform(
                target_frame=self.follower_turtle,
                source_frame=self.target_frame,
                time=rclpy.time.Time(),
                timeout=Duration(seconds=0.05)
            )

        except TransformException as ex:
            # Common during startup before initial transforms arrive
            self.get_logger().warn(
                f'Could not transform {self.target_frame} to {self.follower_turtle}: {ex}',
                throttle_duration_sec=2.0
            )
            return

        # Spatial offset of target frame expressed in follower's coordinates
        dx = transform.transform.translation.x
        dy = transform.transform.translation.y
        distance = math.sqrt(dx * dx + dy * dy)
        bearing = math.atan2(dy, dx)

        # Proportional controller:
        # Drive forward proportional to distance, turn proportional to bearing
        msg = Twist()

        # If closer than 0.3m, stop to prevent crashing
        if distance > 0.3:
            msg.linear.x = min(self.kp_linear * distance, 3.0)
            msg.angular.z = self.kp_angular * bearing
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.cmd_vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleTF2Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

