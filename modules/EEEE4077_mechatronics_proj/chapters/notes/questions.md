# Open questions & risks

Each question has the cheapest test that settles it. An experiment gets a write-up in [`research/`](../research/README.md) (question and what counts as an answer, before the first run). Close it by writing the answer + `[M:<write-up>]`/`[L#]`, then move it to *Closed*.
Ordered by how much damage a wrong answer does.

## Open

| Q | Question | Why it matters | Settled by | When |
|---|---|---|---|---|
| Q1 | How badly does a **tuned** stock MPPI (B0) actually do against crossing / head-on people? | Nav2 maintainers say it handles dynamics well [L3]. If B0 rarely fails, scenarios must be chosen where it does — or the result is "no gain", reported honestly | B0 runs in harness, scenarios A/B, several speeds | M2 |
| Q2 | Do Jazzy's MPPI critics / API match `main` [L1]? Same `CriticFunction` interface? | Plugin must compile against Jazzy | Read `jazzy` branch headers; build hello-critic | M1 |
| Q4 | Can the laptop (8 cores, 13 GB) run Gazebo + Nav2 + harness faster than real time, headless? | Decides runs per night | Time a headless batch of 10 runs | M2 |
| Q5 | Is `nav2_loopback_sim` + a fake obstacle publisher usable for fast critic iteration without Gazebo? | Could make critic tuning runs much faster | Try it once the critic exists | M3 |
| Q6 | Is there a standard ROS message for tracked obstacles we should reuse? | Industry practice is to reuse | Search ROS index; check what `nav2_following` / prox_mpc consume | M3 |
| Q7 | What does the critic need beyond v1 (time discounting, footprint, asymmetric cost)? | Avoid designing on paper | Only answered by P-GT failures | M3–M4 |
| Q8 | How sensitive is P to perception latency, dropouts, ID switches? | The real engineering finding | P-sweep | M4 |
| Q9 | Head-on encounters: does MPPI's averaging of left/right options cause hesitation? | Known MPPI weakness [lead]; only add a sampler change if measured | Scenario B logs (lateral oscillation) | M2–M4 |
| Q11 | Does an off-the-shelf detector find Gazebo actors in rendered images, and can the laptop render the camera at a usable rate? | D-cam is a spec requirement; if detection is poor, the user fine-tunes (their domain); if rendering is too slow, run D-cam batches on the PC | Run a pretrained detector on recorded camera frames; measure render FPS | M1 (look), M4 (use) |
| Q10 | Can a Pi-class board run MPPI at control rate? | Hardware track only | Benchmark on board | Hardware |

## Closed

| Q | Answer |
|---|---|
| Q3 | **Yes.** `gpu_lidar` hits Gazebo actors at 0.3 m and 1.0 m in every scan, GUI and headless [[M:q3_lidar_actor](../research/q3_lidar_actor/README.md)]. Use actors directly. Actors still have no collision → collision metric from GT distance |
