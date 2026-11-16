# L18: DRA-MPPI: Dynamic Risk-Aware MPPI for Mobile Robots in Crowds via Efficient Monte Carlo Approximations

- **Key:** L18
- **Authors:** Elia Trevisan, Khaled A. Mustafa, Godert Notten, Xinwei Wang, Javier Alonso-Mora (TU Delft)
- **Venue / Year:** *IEEE/RSJ IROS*, 2025 (arXiv:2506.21205, v1 June 2025, v2 Aug 2025)
- **URL:** [https://arxiv.org/abs/2506.21205](https://arxiv.org/abs/2506.21205)
- **Status:** S (arXiv listing via search; primary PDF not yet read in full)
- **Scope Track:** Comparative Literature — **closest prior art**

---

## Technical Summary
- MPPI planner for mobile robots among pedestrians.
- Monte Carlo approximation of the **joint collision probability** against multiple dynamic obstacles, evaluated for several hundred sampled trajectories in real time.
- Uses that probability either to **reject samples** above a risk threshold or as a **weighted cost term**.
- Handles non-Gaussian obstacle predictions; reported to reduce the freezing robot problem.
- Compared against Scenario-based MPC, a risk-aware Frenét planner, and vanilla MPPI; reported ~98% safety rate in the crowded scenario with competitive task time.

---

## Project Relevance & Comparison
- **Overlap:** Same problem (dynamic obstacles in MPPI, freezing robot) and same mechanism family (predicted obstacle states scored inside rollouts).
- **Expected differentiators (confirm after full read):** this project is a native Nav2 `pluginlib` critic on upstream `nav2_mppi_controller`; includes the brownfield perception chain (2D LiDAR + monocular, ByteTrack, frustum gating, KF); and runs the C0/C1/C2 detection-vs-prediction ablation. DRA-MPPI assumes obstacle predictions are given and adds probabilistic risk handling that this project does not.
- **Role in FYP:** Must be cited and differentiated in originality and lit review. Candidate qualitative comparison point (risk-aware vs. deterministic CV projection).

---

## BibTeX
```bibtex
@inproceedings{trevisan2025dramppi,
  author    = {Trevisan, Elia and Mustafa, Khaled A. and Notten, Godert and Wang, Xinwei and Alonso-Mora, Javier},
  title     = {Dynamic Risk-Aware {MPPI} for Mobile Robots in Crowds via Efficient {Monte Carlo} Approximations},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2025},
  eprint    = {2506.21205},
  archivePrefix = {arXiv}
}
```
