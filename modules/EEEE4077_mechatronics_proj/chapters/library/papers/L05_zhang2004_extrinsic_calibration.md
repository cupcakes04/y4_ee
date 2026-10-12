# L05: Extrinsic Calibration of a Camera and Laser Range Finder

- **Key:** L5
- **Authors:** Qian Zhang and Robert Pless
- **Venue / Year:** *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2004
- **Status:** S (Secondary search match; verify primary publisher page)

---

## Abstract Summary & Core Mechanics
Presents the classical geometric method for finding the rigid-body transform (rotation $R$ and translation $t$) between a monocular camera and a single-line 2D laser range finder using a planar checkerboard target placed at arbitrary poses.

---

## Project Relevance & Usage
- **Calibration Foundation:** Solves the extrinsic transformation $[R \mid t]$ mapping 2D planar LiDAR points onto camera image coordinates $(u, v)$, enabling frustum ray gating in Module 2.
- **Sensor Fusion Grounding:** Proves that extrinsic registration between 2D LiDAR and monocular vision is mathematically grounded and established.

---

## BibTeX
```bibtex
@inproceedings{zhang2004extrinsic,
  author    = {Zhang, Qian and Pless, Robert},
  title     = {Extrinsic calibration of a camera and laser range finder (improves camera calibration)},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2004}
}
```
