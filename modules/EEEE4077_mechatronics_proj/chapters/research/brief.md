# Project brief — read this first

Everything a new session needs that isn't in the design: who, what was promised, what the supervisor wants, why things are the way they are.
Update the decision log when a decision changes; don't let it drift into a chat log.

## 0. The project in plain terms

**Problem.** Most indoor mobile robots (warehouse AMRs) navigate with a single-plane 2D LiDAR and Nav2-style costmaps. A costmap is a snapshot grid: a walking person is just occupied cells *now*, with no identity and no velocity. The local controller therefore plans against where people are, not where they will be — so it may brake, hesitate or detour for someone who will be gone by the time the robot arrives, or drive into the spot someone is about to walk into. 3D LiDAR / heavy GPU perception can help but is costly; the cheap robots are the ones stuck with this.

**Idea.** Add a cheap camera. The camera says *which* returns are people/objects and keeps their identity over time; the LiDAR gives their exact range. Fuse the two into tracks with position and velocity (Kalman filter), predict a couple of seconds ahead (constant velocity + growing uncertainty), and let Nav2's MPPI controller score its candidate trajectories against those predictions through a custom critic plugin. Static walls stay in the normal costmap.

**What the project delivers.** (1) A Gazebo simulation of a diff-drive robot with LiDAR + camera in aisle-like spaces with walking people; (2) the fusion/tracking pipeline; (3) the predictive MPPI critic; (4) an automated test harness that compares stock Nav2 against the system, separating "knowing what the obstacle is" from "predicting where it goes", under varying speeds, patterns, crowd density and perception error. Simulation only for the degree; real hardware later as a personal goal.

**Honest status of the idea.** The gap is real (no shipped Nav2 MPPI critic uses tracked obstacles [L1]) but the payoff is unproven: Nav2's maintainers say stock MPPI already copes with moving obstacles [L1]. Measuring that baseline first (Q1) decides how the contribution is framed. Details: [design.md](design.md).

## 1. Identity

| | |
|---|---|
| Title | Vision-Augmented Mobile Robot Navigation in Dynamic Environments |
| Code | SD-MEng-26-01 (spec: [`raw/general/FYP Specification - SD-MEng-26-01.docx`](../../raw/general/)) |
| Supervisor / Moderator | Dr Shalini Darmaraju / Ir Dr Daniel Pu |
| Ratio | HW 0% · SW 60% · Research 40% — simulation only, workstation only |
| Software named in spec | Ubuntu, ROS 2, Nav2, Gazebo; Python or C++; NumPy + Matplotlib |
| SDGs | 9 (Industry, Innovation, Infrastructure), 8 (Decent Work) |

## 2. Binding commitments

### 2a. Spec (supervisor-written, binding)

Objectives: (1) review literature on vision-augmented navigation, camera–range integration, tracking, motion prediction; (2) indoor robot sim + **adapt existing detection/tracking on simulated camera images** combined with planar range for obstacle position & velocity; (3) feed short-term motion predictions into local planning/collision avoidance **using an existing navigation framework**; (4) evaluate vs range-only navigation, plus comparisons separating **visual information** from **motion prediction**, varying speed, movement pattern, density.

Metrics named: **tracking accuracy, navigation success, collisions, travel time, waiting time, computation time**.
Deliverables: literature review · configurable sim + detection/tracking with documented code · navigation prototype · comparative results with **reproducible scenarios and video demos** · final report.

### 2b. Submitted proposal (Nov 2026)

Context only, in [`archive/`](../../archive/2026-11_proposal/). Its numeric targets were unsourced hypotheses: **not goals, don't tune or design toward them.** Only carry-over is naming: C0 / C1 / C2 = B0 / P-v0 / P.

## 3. Supervisor guidance (from meeting records 1–6)

Context, **not rules**. Adopt a point only where it holds on its own merits; the spec (§2a) is the only binding document.

- Baselines/SOTA considered before scope (mtg 2). Holds on merit — a weak baseline invalidates every result → tuned B0, B1, bounded prior-art pass.
- Literature review that "reverse engineers" the built system (mtg 4). Matches how we work: literature justifies choices after the fact.
- Agreed ablation: 2D LiDAR / + detection / + tracking & prediction (mtg 4).
- Presentation style: tables and charts up front, little text; diagrams **top-down**; objectives general (detail goes in methodology); Gantt big with autumn/spring shading; slide 1 should set up the established LiDAR-based space → freezing problem → methods (mtg 5–6).
- Hardware budget context: projects typically capped by hardware cost (~RM700) (mtg 1).
- Meetings roughly weekly, 1 h, recorded in `chapters/meetings/`.

## 4. The student (how to work with them)

- **Perception specialist** (detection, tracking, datasets, domain adaptation). Assume a tuned detector exists; don't teach or design detectors.
- Comfortable with fusion-type maths (homography, frames, control), not a fusion specialist. Strong Python and system architecture; C++ capable but slow — keep C++ to the critic.
- ROS 2 core, launch, tf2, URDF/RViz done (Nov 2026, `concepts/ROS2_notes`). Nav2 and Gazebo not yet.
- Must understand everything that ships (learn↔build loop). Cares about engineering rigour, not marks; wants no fluff and no wasted time chasing data.
- Machines: **laptop** (main dev) Ubuntu 24.04 + ROS 2 Jazzy native, 8 cores / 13 GB, Gazebo not yet installed. **PC** with RTX GPU under WSL2, for heavy jobs only.
- Handles all git themselves. Will build real hardware later as a personal, self-funded goal (Pi/Orange Pi class).

## 5. Decision log

| Date | Decision | Why |
|---|---|---|
| 2026-11-16 | "SOTA" = industry-grade rigour (tuned baselines, fair comparisons, standard packages), not novelty | Student's definition |
| 2026-11-16 | Premise reframed from "fix freezing" to "does prediction help, by how much, under realistic perception error" | Nav2 maintainers state stock MPPI already handles dynamic obstacles well [L1]; must be measured (Q1) |
| 2026-11-16 | Order: harness + B0 → critic on GT → fusion | Risk-first; isolates controller value from perception |
| 2026-11-16 | Detection in sim: real detector on rendered camera images (**P-cam**, satisfies spec) for tracking accuracy + a subset of runs; **synthetic detector** with noise calibrated from P-cam for large batches and sweeps | Spec requires simulated images; batches need speed on the laptop |
| 2026-11-16 | Hardware is personal, off the critical path; spec stays HW 0% | Spec + student bandwidth |
| 2026-11-16 | Literature just-in-time; claim tags `[L]/[M]/[E]`; debt list instead of blocking | Student preference; thesis guide accepts docs/tutorials/libraries as literature |
| 2026-11-16 | Midterm meeting wk 16 (by 18 Dec): sim demo + first B0 numbers | Forcing function for M1–M2 |
