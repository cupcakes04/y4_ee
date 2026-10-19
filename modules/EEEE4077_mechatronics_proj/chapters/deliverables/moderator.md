# FYP Project Summary (version 1: no keywords, super general)

### Title

**A Vision-Augmented Autonomous Mobile Robot Navigation Framework for Dynamic Environments**

---

### Project Description

Low-cost autonomous mobile robots navigating dynamic environments often rely on planar range sensors that lack semantic awareness and velocity estimation. Consequently, robots frequently stall around moving obstacles and fail to recognize ground-level hazards such as surface spills or designated work zones.

This project develops a modular navigation framework that augments standard planar range sensing with monocular vision for edge-class robotic platforms. The framework combines visual detection with distance measurements to estimate obstacle kinematics, incorporates dynamic states into local trajectory planning algorithms to prevent freezing, and utilizes lightweight computer vision models to automatically translate surface hazards into operational spatial constraints.

---

### Objectives

1. **Develop a Multi-Sensor Obstacle Tracking Algorithm:**
Design and implement a fusion algorithm combining camera and planar distance data to estimate the position and velocity of moving obstacles in real time.
2. **Formulate a Predictive Trajectory Avoidance Method:**
Integrate dynamic obstacle velocity predictions into local path planning and control algorithms to proactively avoid moving obstacles and eliminate navigation deadlocks.
3. **Develop an Automated Semantic Hazard Mapping Pipeline:**
Implement a computer vision algorithm to identify site-specific ground hazards and project them into spatial cost maps as navigable and restricted operational zones.

---

# FYP Project Summary (version 2: with keywords)

### Title

**Camera-Augmented Navigation Framework for Low-Cost Autonomous Mobile Robots in Dynamic Industrial Environments**

---

### Project Description

Low-cost autonomous mobile robots (AMRs) operating in shared brownfield environments typically rely on 2D planar LiDAR, which cannot perceive obstacle velocities or non-geometric ground hazards. This causes robots to freeze around moving traffic and ignore surface-level risks like spills or designated operational zones.

This project develops an open-source, edge-compatible framework for ROS 2 / Nav2 that augments 2D LiDAR with monocular vision. The system estimates real-time obstacle velocities to enable proactive trajectory avoidance without freezing, while using vision-based scene understanding to automatically map site-specific floor hazards into standard navigation costmap constraints without manual CAD drafting.

---

### Objectives

1. **Develop a Multi-Modal Dynamic Obstacle Tracking Pipeline:**
Integrate monocular vision with 2D planar LiDAR to detect moving obstacles and estimate their position and velocity states in real time.
2. **Implement Dynamic Predictive Trajectory Control:**
Integrate forward-propagated obstacle velocities into the Nav2 model predictive path integral (MPPI) controller to enable proactive deflection and prevent robot freezing in mixed-traffic scenarios.
3. **Automate Semantic Hazard Mapping and Zone Generation:**
Establish an edge-deployable visual segmentation pipeline that identifies site-specific floor hazards from camera imagery and projects them into standard Nav2 keepout and speed-restricted costmap layers.