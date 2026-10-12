# L04: Information Theoretic MPC for Model-Based Reinforcement Learning

- **Key:** L4
- **Authors:** Grady Williams, Paul Drews, Brian Goldfain, James M. Rehg, Evangelos A. Theodorou
- **Venue / Year:** *IEEE International Conference on Robotics and Automation (ICRA)*, 2017, pp. 1714–1721
- **DOI:** [10.1109/ICRA.2017.7989202](https://doi.org/10.1109/ICRA.2017.7989202)
- **Status:** S (Secondary bibliographic match; confirm primary publisher page)

---

## Abstract Summary & Core Mechanics
Formulates Model Predictive Path Integral (MPPI) control within an information-theoretic framework. MPPI uses stochastic sampling of control sequences combined with importance weighting based on trajectory costs, enabling real-time optimization over non-linear dynamics and arbitrary, non-differentiable cost functions.

---

## Project Relevance & Usage
- **Algorithmic Foundation:** Provides mathematical rigor for `nav2_mppi_controller`.
- **Critic Plugin Extension:** Explains how custom critic loss terms (e.g., our velocity obstacle cost) directly shape the importance-weighted control distribution without requiring derivative calculations.

---

## BibTeX
```bibtex
@inproceedings{williams2017mppi,
  author    = {Williams, Grady and Drews, Paul and Goldfain, Brian and Rehg, James M. and Theodorou, Evangelos A.},
  title     = {Information theoretic {MPC} for model-based reinforcement learning},
  booktitle = {IEEE International Conference on Robotics and Automation (ICRA)},
  year      = {2017},
  pages     = {1714--1721},
  doi       = {10.1109/ICRA.2017.7989202}
}
```
