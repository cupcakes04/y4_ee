#!/usr/bin/env python3
"""
Practical tf2 Sample 2: Dynamic Transform Broadcaster

Subscribes to a turtle's continuous 2D pose (/turtlename/pose) and broadcasts
its dynamic spatial transform (world -> turtlename) onto the /tf topic.

Usage:
    ros2 run learning_tf2_py turtle_tf2_broadcaster --ros-args -p turtlename:=turtle1
    ros2 run learning_tf2_py turtle_tf2_broadcaster --ros-args -p turtlename:=turtle2
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


def quaternion_from_euler(roll: float, pitch: float, yaw: float):
    """Convert Euler angles (roll, pitch, yaw) in radians to a unit quaternion."""
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    qw = cr * cp * cy + sr * cp * sy
    return qx, qy, qz, qw


class TurtleTF2Broadcaster(Node):

    def __init__(self):
        super().__init__('turtle_tf2_broadcaster')

        # Declare turtlename parameter so this node can broadcast for turtle1, turtle2, etc.
        self.declare_parameter('turtlename', 'turtle1')
        self.turtlename = self.get_parameter('turtlename').get_parameter_value().string_value

        # Initialize the dynamic transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscribe to the turtle's pose topic
        self.pose_sub = self.create_subscription(
            Pose,
            f'/{self.turtlename}/pose',
            self.handle_turtle_pose,
            10
        )
        self.get_logger().info(
            f'Broadcaster active: broadcasting tf world -> {self.turtlename} from topic /{self.turtlename}/pose'
        )

    def handle_turtle_pose(self, msg: Pose):
        t = TransformStamped()

        # Timestamp and frame definitions
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtlename

        # 2D turtle pose translated to 3D space
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        # Turtlesim gives planar rotation theta (yaw)
        qx, qy, qz, qw = quaternion_from_euler(0.0, 0.0, msg.theta)
        t.transform.rotation.x = qx
        t.transform.rotation.y = qy
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw

        # Broadcast the dynamic transform onto /tf
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleTF2Broadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

