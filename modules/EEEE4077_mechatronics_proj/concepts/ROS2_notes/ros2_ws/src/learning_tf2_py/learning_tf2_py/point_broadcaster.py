#!/usr/bin/env python3
"""
Practical tf2 Sample 5A: Sensor Stamped Point Publisher

Simulates a sensor (e.g. laser rangefinder mounted on turtle1 at 'turtle1_laser')
detecting an obstacle point in its own local sensor coordinate frame.

Usage:
    ros2 run learning_tf2_py point_broadcaster
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped


class PointBroadcaster(Node):

    def __init__(self):
        super().__init__('point_broadcaster')

        self.declare_parameter('sensor_frame', 'turtle1_laser')
        self.sensor_frame = self.get_parameter('sensor_frame').get_parameter_value().string_value

        self.publisher = self.create_publisher(PointStamped, '/detected_point', 10)
        # Publish detected point at 2 Hz
        self.timer = self.create_timer(0.5, self.publish_point)

        self.get_logger().info(
            f'PointBroadcaster started: publishing simulated sensor detections in frame [{self.sensor_frame}]'
        )

    def publish_point(self):
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.sensor_frame

        # Sensor reading: obstacle detected 1.2m directly in front of the laser sensor
        msg.point.x = 1.2
        msg.point.y = 0.0
        msg.point.z = 0.0

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PointBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

