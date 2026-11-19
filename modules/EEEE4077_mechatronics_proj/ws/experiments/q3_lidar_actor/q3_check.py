#!/usr/bin/env python3
"""Q3 check: count lidar hits in the actor's walking lane and on the control cylinder.

Lidar sits at the origin facing +x (see q3_world.sdf). A return at (range r, angle a)
is at x = r cos a, y = r sin a in the lidar frame.
  - actor lane:   1.5 < x < 2.5 and |y| < 3.5   (actor walks along x = 2)
  - control zone: -2.5 < x < -1.5 and |y| < 0.5 (cylinder at x = -2)

Runs for DURATION seconds of SIM time (2 actor loops), then prints one summary line per lidar.
Usage: python3 q3_check.py --ros-args -p use_sim_time:=true
"""
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

DURATION = 28.0  # sim seconds = 2 loops of the 14 s trajectory


def classify(scan: LaserScan):
    lane, control = 0, 0
    for i, r in enumerate(scan.ranges):
        if not (scan.range_min < r < scan.range_max):  # inf / nan / out of range = no hit
            continue
        a = scan.angle_min + i * scan.angle_increment
        x, y = r * math.cos(a), r * math.sin(a)
        if 1.5 < x < 2.5 and abs(y) < 3.5:
            lane += 1
        elif -2.5 < x < -1.5 and abs(y) < 0.5:
            control += 1
    return lane, control


class Q3Check(Node):
    def __init__(self):
        super().__init__('q3_check')
        self.stats = {}
        self.t0 = None
        for topic in ('/scan_low', '/scan_high'):
            self.stats[topic] = {'scans': 0, 'lane_scans': 0, 'lane_max': 0, 'control_scans': 0}
            self.create_subscription(LaserScan, topic, lambda m, t=topic: self.on_scan(t, m), 10)
        self.create_timer(1.0, self.check_done)

    def on_scan(self, topic, msg):
        s = self.stats[topic]
        lane, control = classify(msg)
        s['scans'] += 1
        s['lane_scans'] += lane > 0
        s['lane_max'] = max(s['lane_max'], lane)
        s['control_scans'] += control > 0

    def check_done(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        if now == 0.0:
            self.get_logger().info('sim time is 0: is /clock bridged and use_sim_time set?', once=True)
            return
        if self.t0 is None:
            self.t0 = now
            self.get_logger().info(f'started at sim t = {now:.1f} s, running {DURATION:.0f} sim s')
        if now - self.t0 >= DURATION:
            for topic, s in self.stats.items():
                n = max(s['scans'], 1)
                print(f"{topic}: scans={s['scans']}  "
                      f"actor-lane hit in {s['lane_scans']}/{s['scans']} ({100 * s['lane_scans'] / n:.0f}%), "
                      f"max points on actor={s['lane_max']}  |  "
                      f"control hit in {s['control_scans']}/{s['scans']} ({100 * s['control_scans'] / n:.0f}%)")
            raise SystemExit


def main():
    rclpy.init()
    node = Q3Check()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
