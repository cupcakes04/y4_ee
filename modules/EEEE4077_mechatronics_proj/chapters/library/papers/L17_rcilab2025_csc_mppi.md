# L17: CSC-MPPI: Constrained Sampling MPPI Framework with DBSCAN for Reliable Obstacle Avoidance

- **Key:** L17
- **Authors:** Robot Control and Intelligence Lab (RCILab)
- **Venue / Year:** *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2025
- **URL:** [https://github.com/RCILab/RCI_cscmppi](https://github.com/RCILab/RCI_cscmppi)
- **Status:** S (Publication specifications and implementation verified)
- **Scope Track:** Comparative Literature / Constrained MPPI Optimization

---

## Technical Architecture & Performance
- **The Multi-Modal Averaging Pathology:** Conventional MPPI relies on exponential softmax averaging across all sampled trajectories. In symmetrical obstacle encounters (e.g., an obstacle directly along the heading line), rollouts bifurcate into left and right avoidance maneuvers. Standard MPPI averages these modes, synthesizing a straight nominal trajectory that drives directly into the obstacle.
- **GPU DBSCAN Clustering:** CSC-MPPI deploys GPU-accelerated DBSCAN (via RAPIDS `cuML`) directly on the rollout trajectory space, clustering sampled rollouts into topologically distinct maneuver modes (e.g., distinct left-pass vs. right-pass clusters).
- **Primal-Dual Constraint Enforcement:** Employs a primal-dual optimization formulation to enforce hard constraints on the sampled controls, actively filtering out infeasible control domains before final trajectory synthesis.
- **Unified GPU Pipeline:** Both clustering and trajectory rollouts run in unified GPU memory (JAX + cuML), avoiding CPU-to-GPU memory transfer bottlenecks.

---

## Project Relevance & Comparison
- **Methodological Spirit:** Directly targets the mathematical averaging vulnerabilities of naive MPPI in multi-obstacle dynamic environments.
- **Conceptual Divergence:** CSC-MPPI solves multi-modal trajectory bifurcation via clustering and dual optimization on an edge GPU. In our work, dynamic pedestrian velocity vectors ($\mathbf{v}_{\text{obs}}$) inherently break spatial symmetry across the preview horizon ($\tau \in [0, 2.0]\text{ s}$), causing trajectories passing behind the pedestrian to incur significantly lower dynamic cost than trajectories cutting across their forward path, thereby mitigating mode-averaging collapse within a lightweight C++ CPU plugin.
- **Role in FYP:** Provides critical theoretical depth in literature review and viva defense regarding MPPI's stochastic averaging limitations and how spatio-temporal cost asymmetry resolves mode collapse without heavy GPU clustering libraries.

---

## BibTeX
```bibtex
@inproceedings{rcilab2025_cscmppi,
  author    = {{Robot Control and Intelligence Lab (RCILab)}},
  title     = {Constrained Sampling {MPPI} Framework with {DBSCAN} for Reliable Obstacle Avoidance},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2025},
  howpublished = {\url{https://github.com/RCILab/RCI_cscmppi}}
}
```

