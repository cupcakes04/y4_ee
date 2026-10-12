# L01: Unfreezing the Robot: Navigation in Dense, Interacting Crowds

- **Key:** L1
- **Authors:** Peter Trautman and Andreas Krause
- **Venue / Year:** *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2010, pp. 797–803
- **DOI:** [10.1109/IROS.2010.5654369](https://doi.org/10.1109/IROS.2010.5654369)
- **Status:** S (Bibliographic data confirmed; verify primary publisher page)

---

## Abstract Summary & Core Mechanics
This seminal paper identifies and formalizes the **"Freezing Robot Problem"** in autonomous navigation. When a mobile robot models human pedestrians merely as static obstacles or passively moving entities without cooperative modeling, the robot calculates that all forward trajectories will result in collisions. Consequently, the planner becomes overly conservative and triggers emergency halts, freezing in place even though human pedestrians routinely navigate dense environments through mutual cooperation.

---

## Project Relevance & Usage
- **Problem Formulation:** Directly cited in [§1.1 Problem Statement](../../research/01_problem_statement.md) and §1 of the project proposal to define the freezing phenomenon that occurs when 2D LiDAR costmaps treat crossing agents as static obstacles.
- **Hypothesis Foundation:** Provides theoretical justification for Objective **O2-a** (reducing robot freezes per 10 crossings from $>5$ to 0).

---

## BibTeX
```bibtex
@inproceedings{trautman2010unfreezing,
  author    = {Trautman, Peter and Krause, Andreas},
  title     = {Unfreezing the robot: Navigation in dense, interacting crowds},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2010},
  pages     = {797--803},
  doi       = {10.1109/IROS.2010.5654369}
}
```
