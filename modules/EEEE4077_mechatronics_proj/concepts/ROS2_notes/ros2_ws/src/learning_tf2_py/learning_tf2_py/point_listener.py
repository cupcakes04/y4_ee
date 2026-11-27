#!/usr/bin/env python3
"""
Practical tf2 Sample 5B: Sensor Point Transformer

Listens to /detected_point (PointStamped) in the local sensor frame ('turtle1_laser'),
and transforms the point coordinates into the global 'world' frame.

Addresses the two classic tf2 timing scenarios:
1. Exact timestamp lookup (can raise ExtrapolationException if transform is ~10ms behind)
2. Latest available transform (rclpy.time.Time()) which safely maps the point immediately

Usage:
    ros2 run learning_tf2_py point_listener
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf2_geometry_msgs


class PointListener(Node):

    def __init__(self):
        super().__init__('point_listener')

        self.declare_parameter('target_frame', 'world')
        self.declare_parameter('use_latest_time', True)

        self.target_frame = self.get_parameter('target_frame').get_parameter_value().string_value
        self.use_latest_time = self.get_parameter('use_latest_time').get_parameter_value().bool_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.point_sub = self.create_subscription(
            PointStamped,
            '/detected_point',
            self.on_point_received,
            10
        )
        self.get_logger().info(
            f'PointListener active: listening to /detected_point and transforming to [{self.target_frame}] '
            f'(use_latest_time={self.use_latest_time})'
        )

    def on_point_received(self, msg: PointStamped):
        try:
            # When use_latest_time=True (default), we request rclpy.time.Time() (time=0).
            # This fetches the most recent transform currently cached in the buffer,
            # avoiding "extrapolation into the future" race conditions when sensor messages
            # arrive faster than the robot base pose updates.
            query_time = rclpy.time.Time() if self.use_latest_time else rclpy.time.Time.from_msg(msg.header.stamp)

            transform = self.tf_buffer.lookup_transform(
                target_frame=self.target_frame,
                source_frame=msg.header.frame_id,
                time=query_time
            )

            # Apply transform to PointStamped
            transformed_point = tf2_geometry_msgs.do_transform_point(msg, transform)

            self.get_logger().info(
                f'Obs in [{msg.header.frame_id}]: ({msg.point.x:.2f}, {msg.point.y:.2f}) '
                f'--> In [{self.target_frame}]: ({transformed_point.point.x:.2f}, {transformed_point.point.y:.2f})'
            )

        except TransformException as ex:
            self.get_logger().warn(
                f'Unable to transform point from {msg.header.frame_id} to {self.target_frame}: {ex}',
                throttle_duration_sec=2.0
            )


def main(args=None):
    rclpy.init(args=args)
    node = PointListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
