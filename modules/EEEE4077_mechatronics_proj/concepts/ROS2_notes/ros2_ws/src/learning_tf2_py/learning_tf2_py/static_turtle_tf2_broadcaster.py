#!/usr/bin/env python3
"""
Practical tf2 Sample 1: Static Transform Broadcaster

Publishes a fixed, unchanging transformation between a parent frame and a child frame
(e.g., from 'turtle1' to 'turtle1_laser') onto the /tf_static topic using 'Transient Local' QoS.

Usage:
    ros2 run learning_tf2_py static_turtle_tf2_broadcaster
    ros2 run learning_tf2_py static_turtle_tf2_broadcaster --ros-args -p frame_id:=turtle1 -p child_frame_id:=turtle1_laser -p x:=0.5 -p yaw:=0.0
"""

import math
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


def quaternion_from_euler(roll: float, pitch: float, yaw: float):
    """
    Convert Euler angles (roll, pitch, yaw) in radians to a unit quaternion (x, y, z, w).
    Formula:
        qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
        qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
        qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
        qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    """
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    qw = cr * cp * cy + sr * sp * sy
    return qx, qy, qz, qw


class StaticTurtleTF2Broadcaster(Node):

    def __init__(self):
        super().__init__('static_turtle_tf2_broadcaster')

        # Declare configurable parameters with sensible defaults
        self.declare_parameter('frame_id', 'turtle1')
        self.declare_parameter('child_frame_id', 'turtle1_laser')
        self.declare_parameter('x', 0.5)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('z', 0.2)
        self.declare_parameter('roll', 0.0)
        self.declare_parameter('pitch', 0.0)
        self.declare_parameter('yaw', 0.0)

        # Allow passing CLI arguments: node_name child_frame_id x y z roll pitch yaw
        # (similar to ROS 2 official static_transform_publisher style)
        if len(sys.argv) >= 8:
            child_frame_id = sys.argv[1]
            x = float(sys.argv[2])
            y = float(sys.argv[3])
            z = float(sys.argv[4])
            roll = float(sys.argv[5])
            pitch = float(sys.argv[6])
            yaw = float(sys.argv[7])
            frame_id = sys.argv[8] if len(sys.argv) >= 9 else 'turtle1'
        else:
            frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
            child_frame_id = self.get_parameter('child_frame_id').get_parameter_value().string_value
            x = self.get_parameter('x').get_parameter_value().double_value
            y = self.get_parameter('y').get_parameter_value().double_value
            z = self.get_parameter('z').get_parameter_value().double_value
            roll = self.get_parameter('roll').get_parameter_value().double_value
            pitch = self.get_parameter('pitch').get_parameter_value().double_value
            yaw = self.get_parameter('yaw').get_parameter_value().double_value

        # Instantiate the StaticTransformBroadcaster
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)

        # Construct and send the static transform
        self.make_transforms(frame_id, child_frame_id, x, y, z, roll, pitch, yaw)

    def make_transforms(self, frame_id, child_frame_id, x, y, z, roll, pitch, yaw):
        t = TransformStamped()

        # Header metadata
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = frame_id
        t.child_frame_id = child_frame_id

        # Translation
        t.transform.translation.x = float(x)
        t.transform.translation.y = float(y)
        t.transform.translation.z = float(z)

        # Rotation (Euler -> Quaternion)
        qx, qy, qz, qw = quaternion_from_euler(float(roll), float(pitch), float(yaw))
        t.transform.rotation.x = qx
        t.transform.rotation.y = qy
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw

        # Static broadcaster latches onto /tf_static (QoS Transient Local)
        self.tf_static_broadcaster.sendTransform(t)
        self.get_logger().info(
            f'Published static transform: {frame_id} -> {child_frame_id} '
            f'xyz=({x:.2f}, {y:.2f}, {z:.2f}) rpy=({roll:.2f}, {pitch:.2f}, {yaw:.2f})'
        )


def main(args=None):
    rclpy.init(args=args)
    node = StaticTurtleTF2Broadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

