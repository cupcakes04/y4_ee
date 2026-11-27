status: planned (starts when M1 is done)

# M2 — harness + B0 (by Fri 18 Dec 2026, midterm meeting wk 16)

**Done when:** scenario YAML → batch of seeded headless runs → metrics CSV + plots; B0 tuned and measured on scenarios A (crossing) and B (head-on).
**Midterm demo:** robot driving a corridor with a walking person, stock Nav2 MPPI, first baseline numbers from an automated batch.

Same learn ↔ build loop as M1.

## Steps

| # | State | Learn | Build | Check |
|---|---|---|---|---|
| 6 | ⬜ | Driving Nav2 from Python (`nav2_simple_commander`); headless Gazebo | `fyp_harness` runner: scenario YAML → spawn actor → send goal → wait → stop | One scripted run end-to-end without touching the GUI |
| 7 | ⬜ | What to log (GT poses, robot odom, cmd_vel) | Logger → CSV per run; metrics script (success, collision, min separation, time, freeze time) | Metrics for one run make sense vs what you watched |
| 8 | ⬜ | MPPI tuning basics (README tuning guide [L1]) | Batch runner with seeds; scenarios A + B; tune B0 | **Q1, Q4**: B0 distributions + runs/hour on laptop → write-ups in `chapters/research/` (criteria written before the batch) |
| 9 | ⬜ | — | Plot script (matplotlib from CSV) + 4–5 midterm slides | Slides uploaded after meeting |

## Notes / findings
(append; promote when the step is done)

- Carried from M1: headless (`gz sim -s -r --headless-rendering`) works with gpu_lidar on this laptop at RTF ≈ 1.0 for 2 lidars; camera + Nav2 load not yet measured.
