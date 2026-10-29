# 06. RViz2 Custom 3D Markers & Visuals

> **Raw Doc References:**  
> - Local: [`ros2_documentation/.../Marker-Sending-Basic-Shapes.rst`](../../ros2_documentation/source/Tutorials/Intermediate/RViz/Marker-Sending-Basic-Shapes/Marker-Sending-Basic-Shapes.rst)  
> - Local: [`ros2_documentation/.../Marker-Points-and-Lines.rst`](../../ros2_documentation/source/Tutorials/Intermediate/RViz/Marker-Points-and-Lines/Marker-Points-and-Lines.rst)  
> - Web: [Sending Basic Shapes to RViz](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/Marker-Sending-Basic-Shapes/Marker-Sending-Basic-Shapes.html)

---

## 1. Mental Model: Why Markers?

Sensors (LiDAR, Cameras) give raw data, but robotic algorithms generate **semantic predictions**:
* An obstacle detection node finds a pedestrian.
* A navigation path planner generates a spline path.
* A manipulator calculates target grasp poses.

**Markers (`visualization_msgs/msg/Marker`)** let you publish custom 3D geometric shapes (cubes, spheres, arrows, line trajectories, text) directly from your Python or C++ nodes into the RViz 3D canvas!

---

## 2. Publishing Basic 3D Shapes (`Marker.CYLINDER`, `ARROW`, `CUBE`)

```python
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker


class WaypointMarkerNode(Node):

    def __init__(self):
        super().__init__('waypoint_marker_node')
        self.publisher_ = self.create_publisher(Marker, 'visualization_marker', 10)
        self.timer = self.create_timer(1.0, self.publish_marker)
        self.id = 0

    def publish_marker(self):
        marker = Marker()

        # 1. Coordinate Frame & Timestamp
        marker.header.frame_id = 'map'
        marker.header.stamp = self.get_clock().now().to_msg()

        # 2. Namespace & Unique ID (Reusing same ID updates the shape; New ID spawns another)
        marker.ns = 'waypoints'
        marker.id = self.id

        # 3. Shape Type: ARROW, CUBE, SPHERE, CYLINDER, LINE_STRIP, TEXT_VIEW_FACING
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD

        # 4. 3D Position & Orientation
        marker.pose.position.x = 2.0
        marker.pose.position.y = 1.0
        marker.pose.position.z = 0.25
        marker.pose.orientation.w = 1.0

        # 5. Dimensions in meters
        marker.scale.x = 0.5  # Diameter
        marker.scale.y = 0.5  # Diameter
        marker.scale.z = 0.5  # Height

        # 6. Color (RGBA, normalized 0.0 to 1.0)
        marker.color.r = 0.0
        marker.color.g = 1.0  # Green
        marker.color.b = 0.0
        marker.color.a = 0.8  # 80% opacity

        # 7. Lifetime (0 = stays visible forever until explicitly deleted)
        marker.lifetime = rclpy.duration.Duration(seconds=0).to_msg()

        self.publisher_.publish(marker)
        self.get_logger().info('Published 3D waypoint marker to RViz.')
```

---

## 3. Drawing Robot Paths & Trajectories (`Marker.LINE_STRIP`)

To connect a series of waypoints with a continuous 3D line:

```python
from geometry_msgs.msg import Point

marker = Marker()
marker.header.frame_id = 'map'
marker.header.stamp = self.get_clock().now().to_msg()
marker.type = Marker.LINE_STRIP
marker.action = Marker.ADD

# Line thickness in meters
marker.scale.x = 0.05

# Blue line
marker.color.r = 0.0
marker.color.g = 0.2
marker.color.b = 1.0
marker.color.a = 1.0

# Append 3D waypoints
marker.points = [
    Point(x=0.0, y=0.0, z=0.0),
    Point(x=1.0, y=1.0, z=0.0),
    Point(x=2.5, y=0.8, z=0.0),
    Point(x=3.0, y=2.0, z=0.0)
]

self.publisher_.publish(marker)
```

---

## 4. Viewing Markers in RViz2

1. In RViz2, click **Add** (bottom left in Displays panel).
2. Choose **Marker** (or **MarkerArray** if publishing batches).
3. Set **Marker Topic** to `/visualization_marker`.
4. Ensure your **Fixed Frame** matches `marker.header.frame_id` (e.g. `map`). Your 3D cylinder or trajectory line will appear instantly on the canvas!

