# Slide 1: Project Title & System Architecture

**Slide Goal:** Introduce yourself, explain what problem you are solving in simple terms, and walk through the block diagram.  
**Target Duration:** ~1.5 to 2 minutes.

---

## 1. Quick Summary (What This Slide Is About)
Modern warehouse AMRs are built around **2D safety LiDAR** and **static 2D costmaps**, which handle walls well but fail when people walk across corridors—causing the **Freezing Robot Problem**. Our project pairs that existing 2D LiDAR with an inexpensive camera to track people, predict their motion 2.0 seconds ahead in MPPI, and validate the whole pipeline in Gazebo simulation via a structured 6-step engineering methodology.

---

## 2. What to Point to on Screen (Visual Walkthrough)
1. **Title & Info:** Point to project title, your name, Dr. Shalini (Supervisor), and Ir Dr. Daniel Pu (Moderator).
2. **Left Cards (Established Space → Problem → Methods Handoff):**
   - **Established Space & Freezing Problem:** Existing AMRs rely on 2D LiDAR + static costmaps, which treat pedestrians as fixed walls and cause freezing.
   - **Vision-LiDAR Fusion (O1) & Predictive MPPI (O2):** Add a camera + Kalman velocity tracker + 2.0 s predictive critic.
   - **Methods Bridge:** Mention how we implement and benchmark this systematically, transitioning straight into Slide 2.
3. **Right Diagram — 4 Main Category Blocks (Now Enlarged Headers):**
   - **1. Simulated Sensor Inputs:** Monocular RGB camera + Planar 2D Safety LiDAR.
   - **2. Multi-Modal Obstacle Tracker (O1):** YOLOv8 + ByteTrack + Camera–LiDAR Frustum Gate + Linear Kalman Filter.
   - **3. Motion-Aware Local Path Planning (O2):** Dynamic Obstacle Critic Plugin + Nav2 MPPI Trajectory Planner (while static walls stay in the 2D costmap).
   - **4. Closed-Loop Execution & Evaluation (O3):** Simulated Mobile Robot Base + Automated Benchmark Logger.

---

## 3. Conversational Spoken Script (Natural & Comfortable)

> *"Good morning Dr. Shalini, Ir Dr. Daniel Pu. My name is Nicholas Khor, and today I'm presenting the plan for my Final Year Project: **'Vision-Augmented Mobile Robot Navigation in Dynamic Environments'**.*
>
> *To start with the established space: in modern warehouses and factories, commercial autonomous mobile robots almost universally rely on **2D planar safety LiDAR** paired with **static 2D costmaps** in stacks like ROS 2 Nav2. That setup is economical, safety-certified, and works very well for mapping fixed walls and storage racks.*
>
> *However, it breaks down in shared human corridors—causing what is known as the **'Freezing Robot Problem'**. Because a 2D laser only cuts across a person's legs near floor level and the costmap treats every return as an immovable wall, the planner has no idea the person is walking past. All forward paths look blocked, so the robot panics, freezes in place, or spins.*
>
> *To solve this without expensive 3D LiDARs, our system adds a low-cost monocular camera to the existing 2D laser scanner, structured across the four stages shown on the right:*
> - *First, **Sensor Inputs**: the RGB camera and 2D LiDAR in Gazebo.*
> - *Second, **Multi-Modal Tracking (O1)**: lightweight YOLOv8 and ByteTrack identify and track people in 2D, frustum gating fuses those boxes with laser rays for clean depth, and a Kalman filter estimates real-time walking velocity.*
> - *Third, **Motion-Aware Planning (O2)**: a custom Nav2 MPPI dynamic critic projects those velocities two seconds ahead so the robot steers smoothly behind pedestrians, while static walls remain in the standard 2D costmap.*
> - *Fourth, **Execution & Evaluation (O3)**: the simulated robot executes these commands while an automated logger records freezes, collisions, and travel time.*
>
> *To deliver and prove this architecture rigorously on standard CPU compute, we execute it through a 6-step engineering methodology and a 3-way ablation benchmark in ROS 2 Jazzy and Gazebo Harmonic—which brings us right into our methods and approach on the next slide."*

---

## 4. Key Bullet Points (If You Prefer Speaking Freely)
- **Established Space:** Industrial AMRs use 2D safety LiDAR + static 2D costmaps (great for walls, cheap, certified).
- **The Gap (Freezing Problem):** 2D LiDAR sees ankles as static walls $\rightarrow$ robot freezes when people cross the aisle.
- **The Solution (Stages 1–3):** Add monocular camera (YOLO + ByteTrack) + laser frustum gating + Kalman velocity $\rightarrow$ Nav2 MPPI dynamic critic predicts 2.0 s ahead.
- **Methods Transition (Stage 4 → Slide 2):** Built in ROS 2 Jazzy / Gazebo Harmonic and validated via a 6-step workflow and 3-way ablation study.

---

## 5. Simple Questions the Moderator Might Ask

- **"Why use a camera + 2D LiDAR instead of a 3D LiDAR?"**
  - *Answer:* *"3D LiDARs are very expensive—usually thousands of dollars—and take heavy GPU processing to handle point clouds. 2D LiDAR is already standard on warehouse robots, so adding an inexpensive camera is much cheaper and can run easily on normal onboard CPUs."*

- **"Is this tested on a real robot or simulation?"**
  - *Answer:* *"It is 100% in Gazebo simulation as approved in the project specification. This lets us test hundreds of dynamic crossing scenarios safely and collect repeatable data on robot freezing and travel times."*

- **"What does MPPI mean in simple terms?"**
  - *Answer:* *"MPPI stands for Model Predictive Path Integral. Basically, every fraction of a second, the algorithm rolls out thousands of possible driving paths, scores each path to see if it collides with where the obstacle is predicted to walk, and picks the smoothest safe trajectory."*

---

## 6. "If You Get Stuck" Anchor Line
If you lose your train of thought, pause, take a breath, look at the diagram and say:
> *"In short: existing 2D LiDAR setups treat crossing people as static walls and freeze; adding camera tracking and predictive MPPI lets the robot anticipate their motion—which we build and evaluate through the methodology on the next slide."*
