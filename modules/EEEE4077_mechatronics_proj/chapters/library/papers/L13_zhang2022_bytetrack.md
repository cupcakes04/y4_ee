# L13: ByteTrack: Multi-Object Tracking by Associating Every Detection Box

- **Key:** L13
- **Authors:** Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Fucheng Weng, Zehuan Yuan, Ping Luo, Wenyu Liu, Xinggang Wang
- **Venue / Year:** *European Conference on Computer Vision (ECCV)*, 2022 / arXiv:2110.06864
- **Status:** V (Verified via arXiv / ECCV proceedings)

---

## Abstract Summary & Core Mechanics
ByteTrack is an association method for multi-object tracking (MOT) that addresses the common flaw of discarding low-score detection boxes. Instead of filtering out low-confidence boxes, ByteTrack matches both high-score and low-score detection boxes with tracklets:
1. High-score detections are first associated with tracklets using motion similarity (Kalman filter IoU).
2. Remaining unmatched tracklets are then matched against low-score detections to rescue occluded or blurred targets.
3. The method eliminates the need for expensive appearance feature extractors (ReID networks), achieving state-of-the-art tracking accuracy at real-time speeds (30+ FPS).

---

## Project Relevance & Usage
- **Decoupled 2D Data Association:** Solves target identity persistence and tracklet management (`track_id`) purely in 2D image space within the detection node (using BoxMOT / Ultralytics).
- **Reduces Sensor Fusion Complexity:** Removes the need to implement complex metric-space data association (e.g., Hungarian matching on raw 3D clusters) from scratch.
- **Upstream for Metric Depth Gating:** Gated 2D LiDAR clusters inherit persistent visual `track_id`s, allowing a lightweight per-track linear Kalman filter to compute metric velocities $(v_x, v_y)$.

---

## BibTeX
```bibtex
@inproceedings{zhang2022bytetrack,
  title     = {ByteTrack: Multi-Object Tracking by Associating Every Detection Box},
  author    = {Zhang, Yifu and Sun, Peize and Jiang, Yi and Yu, Dongdong and Weng, Fucheng and Yuan, Zehuan and Luo, Ping and Liu, Wenyu and Wang, Xinggang},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2022}
}
```

