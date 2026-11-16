# L16: EXACT-MPPI: Exact Signed-Distance Navigation for Arbitrary-Footprint Robots via Path Integral Control

- **Key:** L16
- **Authors:** Chen Peng et al. (caseypen)
- **Venue / Year:** Robotics Preprint / GitHub Repository, 2024–2025
- **URL:** [https://github.com/caseypen/EXACT-mppi](https://github.com/caseypen/EXACT-mppi)
- **Status:** S (Repository specifications and architecture inspected)
- **Scope Track:** Comparative Literature / High-Performance GPU MPPI

---

## Technical Architecture & Performance
- **Exact Continuous Footprint Geometry:** Conventional local planners reduce the robot footprint to an inscribed/circumscribed disc or conservative axis-aligned bounding box. EXACT-MPPI computes exact Signed Distance Functions (SDF) directly between arbitrary, non-convex robot footprints (e.g., T-shaped chassis, forklift tines, articulated bases) and obstacle fields (raw point clouds or polygonal maps).
- **JAX JIT Acceleration:** Developed in Python using JAX with Just-In-Time (JIT) CUDA compilation. It compiles analytical geometry and trajectory rollouts into parallel GPU kernels, executing thousands of rollouts per control cycle on edge hardware (NVIDIA Jetson) at high frame rates.
- **Dynamic Obstacle Projection:** Vectorized operators analytically propagate dynamic obstacle trajectories across parallel rollouts without training or relying on heavy neural trajectory-prediction models.

---

## Project Relevance & Comparison
- **Methodological Spirit:** Shares the concept of spatio-temporal dynamic obstacle forward projection during MPPI rollout evaluations.
- **Conceptual Divergence:** EXACT-MPPI addresses **geometric footprint conservatism** (non-convex shapes vs. raw point clouds) and shifts the computational paradigm to Python/JAX on an edge GPU. In contrast, our project targets the **brownfield semantic freezing problem** on standard industrial AMR CPUs using 2D LiDAR + monocular vision late-fusion and an idiomatic C++ Nav2 plugin.
- **Role in FYP:** Acts as the high-end GPU / continuous-geometry literature reference, contrasting our lean CPU-native discrete Kalman tracking approach.

---

## BibTeX
```bibtex
@misc{peng2024_exact_mppi,
  author       = {Chen Peng},
  title        = {{EXACT-MPPI}: Exact Signed-Distance Navigation for Arbitrary-Footprint Robots from Point Clouds via Path Integral Control},
  year         = {2024},
  howpublished = {\url{https://github.com/caseypen/EXACT-mppi}}
}
```

