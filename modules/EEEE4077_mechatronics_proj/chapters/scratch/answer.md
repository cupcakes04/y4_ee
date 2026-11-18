Part B
B2:

(nic) nicholas@nicholas-IdeaPad-Slim-3-15AMN8:~/projects/y4_ee$ gz sim --version
Gazebo Sim, version 8.15.0
Copyright (C) 2018 Open Source Robotics Foundation.
Released under the Apache 2.0 License.


B3:
nicholas@nicholas-IdeaPad-Slim-3-15AMN8:~$ gz topic -l                          # Gazebo topics: /clock, /stats, /world/...
gz topic -e -t /clock -n 3           # three clock messages
gz topic -l | grep stats 
system {
  sec: 1794962999
  nsec: 284427848
}
real {
  sec: 1
  nsec: 329872391
}
sim {
  nsec: 2000000
}

system {
  sec: 1794962999
  nsec: 287171999
}
real {
  sec: 1
  nsec: 332624154
}
sim {
  nsec: 3000000
}

system {
  sec: 1794962999
  nsec: 289263059
}
real {
  sec: 1
  nsec: 334715773
}
sim {
  nsec: 4000000
}

/stats
/world/shapes/stats

B4
ros2 topic list                      # now /clock exists
ros2 topic echo /clock --once
ros2 topic hz /clock
/clock
/parameter_events
/rosout
clock:
  sec: 318
  nanosec: 357000000
---
average rate: 936.559
        min: 0.000s max: 0.003s std dev: 0.00029s window: 938
average rate: 919.942
        min: 0.000s max: 0.006s std dev: 0.00041s window: 1842
average rate: 943.514
        min: 0.000s max: 0.006s std dev: 0.00035s window: 2833

B5
ros2 pkg list | grep -E 'nav2_mppi_controller|nav2_bringup'
find /opt/ros/jazzy/include -name critic_function.hpp