import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nicholas/Documents/ROS2_notes/ros2_ws/install/examples_rclpy_minimal_publisher'
