# L15: SE-MPPI: Safe-Escape Nav2-Native MPPI Controller with Control Barrier Functions

- **Key:** L15
- **Authors:** Jung Mo Kang
- **Venue / Year:** GitHub Repository / Preprint, 2024–2025
- **URL:** [https://github.com/kjungmo/se-mppi-nav2](https://github.com/kjungmo/se-mppi-nav2)
- **Status:** S (Repository architecture and algorithm specifications inspected)
- **Scope Track:** Comparative Baseline / Advanced MPPI Literature

---

## Technical Architecture & Performance
- **Nav2-Native Architecture:** Formulated as a direct C++ local controller plugin within the ROS 2 Nav2 ecosystem (`nav2_mppi_controller` architecture), running on standard x86/ARM CPUs with SIMD vectorization.
- **Dynamic Entrapment & Local Minima:** Identifies when the robot is entrapped in non-convex cost minima or dynamic obstacle pockets, triggering an active online escape heuristic.
- **Analytical Safety Guarantee via CBF:** Couples stochastic MPPI trajectory generation with an onboard Control Barrier Function (CBF) safety filter. The CBF is framed as a Quadratic Program (QP) and solved at high control rates ($>30\text{ Hz}$) using `osqp-eigen`. The filtered command $\mathbf{u}_{\text{safe}}^*$ guarantees forward invariance with respect to obstacle boundaries while staying minimally invasive to MPPI's intended trajectory.

---

## Project Relevance & Comparison
- **Methodological Spirit:** Shares the goal of safe, real-time dynamic obstacle navigation in ROS 2 Nav2 without GPU reliance.
- **Conceptual Divergence:** SE-MPPI acts as an *analytical post-filter* on the nominal control output after MPPI finishes rollout evaluation. In contrast, our approach alters the *internal rollout cost landscape* during trajectory evaluation via dynamic spatio-temporal forward projection ($\mathbf{p}_{\text{obs}}(\tau) = \mathbf{p}_0 + \mathbf{v}_{\text{obs}}\tau$).
- **Role in FYP:** Serves as a premier literature baseline illustrating analytical QP/CBF safety filtering within Nav2, providing the theoretical justification for why spatio-temporal cost shaping is preferred over hard CBF bounds when dynamic obstacle velocity uncertainty is present.

---

## BibTeX
```bibtex
@misc{kang2024_semppi,
  author       = {Jung Mo Kang},
  title        = {{SE-MPPI}: Nav2-Native Safe-Escape {MPPI} Controller with Control Barrier Functions},
  year         = {2024},
  howpublished = {\url{https://github.com/kjungmo/se-mppi-nav2}}
}
```

