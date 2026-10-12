# L03: From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in ROS 2

- **Key:** L3
- **Authors:** Steven Macenski et al.
- **Venue / Year:** *Robotics and Autonomous Systems*, 2023
- **arXiv:** [arXiv:2307.15236](https://arxiv.org/abs/2307.15236)
- **Status:** V (arXiv abstract opened and verified)

---

## Abstract Summary & Core Mechanics
A comprehensive survey by ROS and Nav2 core maintainers documenting the current state of mobile robotics algorithms in ROS 2. It covers modern path planning (Smac Planner), controller servers (including DWB, TEB, and MPPI), costmap filters (Keepout and Speed zones), and behavior trees.

---

## Project Relevance & Usage
- **State-of-the-Art Baseline:** Establishes the authoritative baseline for modern ROS 2 mobile robotics algorithms.
- **Controller Context:** Demonstrates that predictive MPPI is the cutting-edge controller in Nav2, motivating our choice to build the dynamic obstacle critic on top of MPPI.

---

## BibTeX
```bibtex
@article{macenski2023survey,
  author    = {Macenski, Steven and others},
  title     = {From the Desks of {ROS} Maintainers: A Survey of Modern \& Capable Mobile Robotics Algorithms in the Robot Operating System 2},
  journal   = {Robotics and Autonomous Systems},
  year      = {2023},
  eprint    = {2307.15236},
  archivePrefix = {arXiv}
}
```
