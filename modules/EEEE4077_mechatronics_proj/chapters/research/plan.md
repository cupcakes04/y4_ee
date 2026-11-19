# Plan

**Now (2026-11-19, wk 12):** M1 step 1 done + promoted (Q3 = yes). Step-1 understanding check waiting in `scratch/answer.md`; then step 2 `fyp_description`. Active scratch: [`M1_sim_nav2.md`](../scratch/M1_sim_nav2.md) (M2 queued in [`M2_harness_b0.md`](../scratch/M2_harness_b0.md)).

Rule: each milestone ends in something that **runs and produces a number**. Learn only what the next milestone needs (learn↔build, see [ws/README.md](../../ws/README.md)).
Order is risk-first: harness and baseline before perception; critic on ground truth before fusion; C++ early because it's the biggest skill gap.

| M | Effort [E] | Target date | Done when | Learn for it | Settles |
|---|---|---|---|---|---|
| **M1 — Sim + stock Nav2** | 12 % | Fri 4 Dec 2026 (wk 14) | Your URDF robot (diff-drive, LiDAR, camera) in Gazebo Harmonic; Nav2 + stock MPPI drives it to a goal in a corridor world; one actor walks; hello-critic plugin compiles and loads | Gazebo Harmonic + `ros_gz_bridge`, Nav2 bringup/params, pluginlib basics | Q2, Q3 |
| **M2 — Harness + B0** | 18 % | Fri 18 Dec 2026 (wk 16, **midterm meeting**) | Scenario YAML → batch of seeded headless runs → metrics CSV + plots. B0 tuned and measured on scenarios A (crossing) and B (head-on) | rosbag/logging, Python launch from scripts, basic MPPI tuning | Q1, Q4, Q9 (first look) |
| *break + exams* | 8 % | 21 Dec – 23 Jan | **Prior-art pass** (bounded, ~1–2 days): what Nav2 users actually do for dynamic obstacles; read L3, L4, L6, L9 → fix B1 and the positioning. **Draft lit review** chapter from the register. Read MPPI critic code; C++ refresh | MPPI maths (notes/), how Nav2 MPPI critics touch the rollout tensors | debts D2, D3 |
| **M3 — Critic on GT (P-GT)** | 17 % | Fri 29 Jan 2027 | DynamicObstacleCritic v1 consuming GT tracks; P-GT vs B0 numbers on A/B | C++ critic internals, rollout tensors | Q5, Q6, Q7 |
| *draft thesis* | 5 % | **5 Feb 2027** | System + harness + B0 vs P-GT written up | — | — |
| **M4 — Fusion (P, P-cam, P-v0, sweep)** | 22 % | ~5 Mar 2027 | D-cam on rendered images + fusion + KF + scan masking; tracking accuracy measured; D-syn calibrated from it; P, P-cam, P-v0, noise/latency sweep; more scenarios (oblique, 2–4 agents) | KF tuning, box→bearing geometry | Q7, Q8, Q9, Q11 |
| **M5 — Final runs + thesis** | 18 % | 31 Mar 2027 | Frozen code, full result set, demo videos, thesis + logbook + code submitted | — | — |
| **H — Hardware (personal)** | outside 100 % | from Feb, parallel | Same stack on real robot | Calibration, drivers | Q10 |

Effort = estimated share of total FYP time (sums to 100 %). Heaviest on M2 and M4 because the harness and the fusion/perception integration are where most debugging lives. Re-estimate after M2 from actual time spent.

If something slips: drop M4's extra scenarios first, then P-sweep breadth. Never drop B0 or P-GT — they are the spine.
