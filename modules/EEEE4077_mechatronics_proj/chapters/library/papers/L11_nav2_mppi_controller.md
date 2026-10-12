# L11: Nav2 MPPI Controller: Architecture, Benchmarks, and Critic Plugins

- **Key:** L11
- **Authors:** ROS 2 Nav2 Development Team
- **Venue / Year:** ROS 2 Navigation Stack Repository & Documentation, 2024–2026
- **URL:** [https://github.com/ros-navigation/navigation2/tree/main/nav2_mppi_controller](https://github.com/ros-navigation/navigation2/tree/main/nav2_mppi_controller)
- **Status:** V (README and source directory inspected and verified)

---

## Technical Architecture & Performance
- **Plugin Architecture:** `nav2_mppi_controller` executes Model Predictive Path Integral control using plugin-based trajectory critics.
- **Default Parameters:** 1,000 batch trajectories, 56 prediction steps at $0.05\text{ s}$ per step ($T = 2.8\text{ s}$ lookahead horizon).
- **Benchmark Performance:** Measured executing at $50+\text{ Hz}$ on standard 4th-generation Intel i5 hardware, confirming low CPU overhead.
- **Shipped Critics:** The 11 standard critics on `main` include `ConstraintCritic`, `CostCritic`, `GoalAngleCritic`, `GoalCritic`, `ObstaclesCritic`, `PathAlignCritic`, `PathAngleCritic`, `PathFollowCritic`, `PreferForwardCritic`, `TwirlingCritic`, and `VelocityDeadbandCritic`. None model dynamic obstacle velocities.

---

## Project Relevance & Usage
- **Core Contribution (Module 3):** Serves as the base framework into which our custom `nav2_mppi_dynamic_critic` is built, providing the exact API hooks and plugin architecture needed for predictive velocity yielding.

---

## BibTeX
```bibtex
@misc{nav2_mppi_controller,
  author       = {{Nav2 Development Team}},
  title        = {Nav2 {MPPI} Controller: Model Predictive Path Integral Trajectory Optimization},
  year         = {2024},
  howpublished = {\url{https://github.com/ros-navigation/navigation2/tree/main/nav2_mppi_controller}}
}
```
