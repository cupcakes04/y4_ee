# Library register

## Status levels

| Status | Meaning | Usable for |
|---|---|---|
| **V** | Primary source opened and the cited part read (by agent or user). Location recorded | Anything, including deliverables |
| **U** | User checked it themselves (read, screenshot, ran it) | Anything; note what was checked |
| **lead** | Known to exist, not read | Direction only. Never cite a number from it |

PDFs go in `pdfs/` as `L#_firstauthor_year.pdf`. Cards (`cards/L#_*.md`) only when a source is used for more than one claim: key claims with page numbers, nothing else.
Open-access → agent fetches. Paywalled → ask the user.

## Register

| Key | Source | Status | Used for |
|---|---|---|---|
| L1 | Nav2 `nav2_mppi_controller` README, `ros-navigation/navigation2` **main**, fetched 2026-11-16 | V (main only; Jazzy → Q2) | Critic list, defaults (batch 1000, 56 × 0.05 s), maintainers' note that MPPI handles dynamic obstacles fluidly |
| L2 | `ros-navigation/navigation2` repo package list, main, fetched 2026-11-16 | V | Existence of `nav2_collision_monitor`, `nav2_loopback_sim`, `nav2_following` |
| L3 | S. Macenski et al., "From the Desks of ROS Maintainers…", RAS 2023, arXiv:2307.15236 | lead | Claim that MPPI handles dynamic obstacles without modelling (premise risk Q1) |
| L4 | E. Trevisan et al., "Dynamic Risk-Aware MPPI…", IROS 2025, arXiv:2506.21205 | lead | Closest prior art: dynamic-obstacle MPPI in crowds |
| L5 | "Chance-Constrained Sampling-Based MPC for Collision Avoidance in Uncertain Dynamic Environments", arXiv:2501.08520 | lead | Uncertainty-aware cost for predicted obstacles |
| L6 | MPC planner for Nav2 with VAR obstacle prediction, arXiv:2504.19193 | lead | Prior Nav2-integrated predictive planner |
| L7 | G. Williams et al., "Information theoretic MPC for model-based RL", ICRA 2017 | lead | MPPI foundation (thesis background) |
| L8 | HuNavSim — ROS 2 human navigation simulator, arXiv:2305.01303 | lead | Reactive humans / social-nav metrics (later stress test) |
| L9 | `prox_mpc` / `prox_mpc_obstacle_tracker`, ROS index, release 1.0.0 (2026-07-28 per search summary) | lead | Existing LiDAR tracker + MPC in ROS 2 — possible baseline or message reuse (Q6) |
| L10 | P. Trautman, A. Krause, "Unfreezing the robot…", IROS 2010 | lead | Freezing-robot problem framing (background only) |

Old proposal keys (L1–L17) are in `archive/` and are **not** carried over; re-add only what gets used, after reading it.

## Data debt

Claims we want to make but can't yet source. Pay before anything goes into a deliverable.

| # | Claim | Needed for | Plan |
|---|---|---|---|
| D1 | Stock costmap layers leave stale marks behind moving people | Problem statement | Measure in B0 runs (becomes `[M:<write-up>]`) instead of citing |
| D2 | L3's exact wording/section on MPPI and dynamic obstacles | Q1 framing | Agent reads arXiv PDF |
| D3 | L4 method + whether code is public | Positioning | Agent reads arXiv PDF |
| D4 | Stereo depth error growth with range; 2D vs 3D LiDAR cost gap | Sensor-choice justification (design.md) | Sensor datasheets (user or agent) — only if the thesis shows a number |
