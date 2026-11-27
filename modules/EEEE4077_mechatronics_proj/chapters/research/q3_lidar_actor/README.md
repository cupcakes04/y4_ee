# Q3: does Gazebo Harmonic's `gpu_lidar` see actors?

*Written up 2026-11-27 from the 2026-11-19 logs. The answer criteria below were set in the experiment README before the runs.*

**Question.** Gazebo actors (animated people) have no collision geometry. Does `gpu_lidar` still return hits on them? If not, scenarios need moving collision models instead of actors, a bigger change. Side measurement for Q4: the laptop's real-time factor (RTF) with two lidars, with GUI and headless.

**What counts as an answer** (from the [experiment README](../../../ws/experiments/q3_lidar_actor/README.md#how-to-read-the-result)):

| Low lidar (0.3 m) | High lidar (1.0 m) | Control cylinder | Meaning |
|---|---|---|---|
| hits | hits | hits | **Yes**: use actors directly |
| none | hits | hits | Seen, but legs too thin at 0.3 m: raise the lidar or add a collision proxy |
| none | none | hits | **No**: need moving collision models |
| any | any | none | Test broken: fix before concluding |

**Setup** (M1 step 1, 2026-11-19; laptop, AMD Radeon 610M iGPU). Code in [`ws/experiments/q3_lidar_actor/`](../../../ws/experiments/q3_lidar_actor/); run output in [`logs/`](logs/) and [`media/`](media/) here.
- World `q3_world.sdf`: two fixed `gpu_lidar`s at 0.3 m and 1.0 m height at the origin (360 samples @ 10 Hz); an actor walking along x = 2 m, y from −3 to +3 and back; a control cylinder (r = 0.25 m) at x = −2 m.
- `bridge.yaml` bridges `/clock`, `/scan_low` and `/scan_high` to ROS. `q3_check.py` (sim time) runs 28 sim-seconds (2 walking loops) and counts the scans with any hit in the actor's lane and on the control.
- RTF: single instantaneous samples of `gz topic -e -t /stats -n 1`, not run averages.
- Runs: run 1 with GUI (the check script failed: conda's Python 3.11 shadowed ROS's 3.12; only RTF and the header were recorded), run 2 with GUI, run 3 headless (`gz sim -s -r --headless-rendering`).

## Results

| Run | Log | Scans | Actor lane hit, 0.3 m / 1.0 m | Control hit, 0.3 m / 1.0 m | Max points on actor | RTF samples |
|---|---|---|---|---|---|---|
| 1, GUI | [run1](logs/2026-11-19_run1_gui.txt) | — | — | — | — | 1.006, 0.996 |
| 2, GUI | [run2](logs/2026-11-19_run2_gui.txt) | 289 | 289/289 / 289/289 | 289/289 / 289/289 | 11 | 1.006, 0.999 |
| 3, headless | [run3](logs/2026-11-19_run3_headless.txt) | 284 | 284/284 / 284/284 | 284/284 / 284/284 | 11 | 1.001 |

`/scan_low` carried `frame_id: lidar_low` in every run. What it looked like: [Gazebo, run 1](media/2026-11-19_run1_gui_scan_low.png), [RViz, run 2](media/2026-11-19_run2_rviz_scan_low.png).

## Verdict

- **Yes.** `gpu_lidar` hits the actor in every scan at both heights, with GUI and headless, and the control proves the sensor and bridge worked. Scenarios use Gazebo actors directly.
- **What it changes:** actors still have no collision, so the collision metric comes from ground-truth distance, not contact ([design.md](../../notes/design.md)).
- **Limits:**
  - The check counts any hit in the actor's lane, not the person's shape (leg vs torso). Enough for yes/no, not for M4's per-person clusters.
  - `q3_check.py` counts from node start, slightly before t0 (289 scans in "28 s" at 10 Hz). Harmless for yes/no.
  - No lidar noise was configured.
  - The RTF is ≈ 1.0 only for this light world: 2 lidars, 1 actor, no camera, no Nav2, single samples. It is not yet an answer to Q4.

  The shape check, the counting window and the RTF averaging are parked in [plan.md](../../notes/plan.md#parked-debt) with triggers.
