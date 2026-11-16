# Slide 2: Methods and Approach

**Slide Goal:** Walk the listener through how you will build and test the system step-by-step, and explain your backup plan.  
**Target Duration:** ~1.5 to 2 minutes.

---

## 1. Quick Summary (What This Slide Is About)
We build and validate the project in 6 logical steps (M0 to M5), paired with a 3-way comparative ablation study (C0 $\rightarrow$ C1 $\rightarrow$ C2). The ablation table makes clear what each step adds, how it changes the system, and what improvement we expect to achieve (culminating in 0 freezes, 0 collisions, and 15–25% faster transit). If the C++ controller plugin gets too difficult, we have a simple backup plan (Fallback F1).

---

## 2. What to Point to on Screen (Visual Walkthrough)
1. **Right Diagram — 6-Step Workflow:**
   - **Critical Path (Solid Red, M0 $\rightarrow$ M1 $\rightarrow$ M2 $\rightarrow$ M3 $\rightarrow$ M5):** Setup Docker (M0), build Gazebo world & C0 baseline (M1), build Vision–LiDAR tracker O1 (M2), write C++ predictive MPPI critic O2 (M3), and run comparative statistics O3 (M5).
   - **Parallel Path (Blue Dashed, M4):** Automated Python scenario runner & rosbag2 logger built in parallel (W11–20) so 450 trials run unattended.
   - **Fallback Path (Dotted Red, F1):** Velocity-inflated 2D costmap bubbles if the C++ critic encounters integration bottlenecks.
2. **Left Bottom — Expected Ablation Evolution Table (C0 $\rightarrow$ C1 $\rightarrow$ C2):**
   - **C0 (Baseline: 2D LiDAR Only):** `20 Hz` 2D LiDAR + static costmap (`2000` rollouts, $\tau = 0\text{ s}$) $\rightarrow$ reference baseline showing frequent freezes ($\Delta t \ge 1.5\text{ s}$ at $v < 0.05\text{ m/s}$) and stop-go delays.
   - **C1 (Vision + LiDAR, $t=0$):** Adds `30 FPS` (`80°` FOV) RGB, YOLOv8 + ByteTrack + frustum gating ($\ge 95\%$ assoc., $v_{\text{obs}} = 0$) $\rightarrow$ cuts leg-split noise, but still yields reactively without lookahead.
   - **C2 (Full Predictive MPPI):** Adds 4-state Kalman CV ($\text{RMSE} < 0.15\text{ m/s}$) + C++ critic ($\tau = 2.0\text{ s}$, `40` steps, $< 0.5\text{ ms}$) $\rightarrow$ **0 freezes, 0 collisions ($d_{\min} \ge 0.35\text{ m}$, $\text{TTC} \ge 1.2\text{ s}$), 15–25% faster transit ($\le 5\text{ s}$ wait), $\ge 20\text{ Hz}$** across `450` paired runs ($p < 0.01$).

---

## 3. Conversational Spoken Script (Natural & Comfortable)

> *"Building on that architecture, here is our methodology, workflow, and expected ablation evolution.*
>
> *On the right, the project is organized into six milestones, M0 through M5. Following the red critical path: we set up ROS 2 Jazzy and Gazebo Harmonic in Docker (M0), build our indoor corridors and record the baseline (M1), implement the camera–LiDAR tracker in M2, develop the native C++ MPPI critic in M3, and run full statistical evaluation in M5. In parallel, M4 builds an automated Python test harness so we can run 450 trials unattended without manual resets.*
>
> *To make sure we prove not just that the system works, but **why** each component helps, M5 evaluates the 3-way ablation evolution summarized in the table on the bottom left:*
> - *First, **C0** is the stock 2D LiDAR baseline using the static costmap—this establishes how often the standard robot freezes and delays.*
> - *Second, **C1** adds YOLOv8, ByteTrack, and laser frustum gating, but zeros out velocity so obstacles are still treated as static circles. This isolates whether semantic detection alone reduces false stops, even without lookahead.*
> - *Third, **C2** is our full proposed system—adding Kalman velocity estimation and the 2.0-second predictive MPPI critic. Because it anticipates where the pedestrian will clear, we expect C2 to achieve **zero freezes, zero collisions, and a 15 to 25% reduction in travel time** compared to C0.*
>
> *Finally, because writing a custom C++ Nav2 plugin carries technical risk, I have an early prototype in Week 13 and a clean backup—Fallback F1—which injects velocity-stretched safety bubbles into the 2D costmap if needed."*

---

## 4. Key Bullet Points (If You Prefer Speaking Freely)
- **Workflow (M0–M5):** M0 Docker $\rightarrow$ M1 Sim & C0 Baseline $\rightarrow$ M2 Tracker (O1) $\rightarrow$ M3 MPPI Critic (O2) $\rightarrow$ M5 Ablation Stats (O3), with **M4** running tests automatically in parallel.
- **Ablation Evolution (C0 $\rightarrow$ C1 $\rightarrow$ C2):**
  - **C0:** 2D LiDAR + static costmap $\rightarrow$ baseline (frequent freezes).
  - **C1:** + Vision/ByteTrack ($t=0$, no velocity) $\rightarrow$ isolates detection/filtering vs. prediction.
  - **C2:** + Kalman velocity + 2.0 s MPPI critic $\rightarrow$ **0 freezes, 0 collisions, 15–25% faster transit**.
- **Fallback F1:** Velocity-inflated costmap layer if C++ plugin hits bottlenecks.

---

## 5. Simple Questions the Moderator Might Ask

- **"Why test C0, C1, and C2 instead of just comparing C0 and C2?"**
  - *Answer:* *"Including C1 lets us separate the effect of better obstacle detection from the effect of motion prediction. It proves whether seeing the person with a camera alone stops freezing, or whether the 2-second velocity prediction in C2 is what actually enables smooth passing."*

- **"Why did you choose a Kalman Filter instead of a deep learning model for trajectory prediction?"**
  - *Answer:* *"A Linear Kalman Filter takes less than 0.2 milliseconds of CPU time, which easily fits within our real-time 20 Hz loop. Since people in corridors usually walk at a steady speed for 1 to 2 seconds, a linear model gives us accurate short-term predictions without needing heavy GPU hardware."*

- **"What programming languages are you using?"**
  - *Answer:* *"Python for the perception and tracking nodes (YOLO, ByteTrack, Kalman filter), C++ for the MPPI controller critic plugin to ensure fast real-time performance, and Python for the automated test harness."*

- **"How does the automated test harness work?"**
  - *Answer:* *"It is a Python script that calls Gazebo's reset services, sets the obstacle speeds, commands the robot to drive to a goal, and records everything into ROS 2 bag files automatically. This saves dozens of hours of manual testing."*

---

## 6. "If You Get Stuck" Anchor Line
If you lose your train of thought, pause, take a breath, look at the diagram and table and say:
> *"In short: we follow a 6-step workflow from baseline to predictive MPPI with Fallback F1 as backup, and our C0-to-C2 ablation table shows how adding tracking and 2-second prediction eliminates freezes and cuts transit time by 15 to 25%."*
