# Slide 1: Project Title & System Architecture

**Slide Goal:** Introduce yourself, explain what problem you are solving in simple terms, and walk through the block diagram.  
**Target Duration:** ~1.5 to 2 minutes.

---

## 1. Quick Summary (What This Slide Is About)
Standard warehouse robots freeze whenever someone walks in front of them because their 2D laser scanner only sees "points on the floor" and treats people like static walls. Your project adds a simple camera to track people, predict where they are walking, and guide the robot smoothly around them in simulation without freezing.

---

## 2. What to Point to on Screen (Visual Walkthrough)
1. **Title & Info:** Point to project title, your name, Dr. Shalini (Supervisor), and Ir Dr. Daniel Pu (Moderator).
2. **Top Boxes (Sensors):** Point to the RGB camera on the left and 2D LiDAR on the right.
3. **Middle Section (Perception / Tracking - O1):**
   - Camera gives bounding boxes with YOLO and ByteTrack.
   - Frustum gating combines camera box with laser points to get clean distance.
   - Kalman filter smooths the motion and calculates the person's walking velocity.
4. **Bottom Right (Planning - O2):**
   - The MPPI planner takes that predicted velocity and plans forward paths that steer safely behind the person.
   - Static walls stay in the 2D costmap; moving people are handled dynamically.

---

## 3. Conversational Spoken Script (Natural & Comfortable)

> *"Good morning Dr. Shalini, Ir Dr. Daniel Pu. My name is Nicholas Khor, and today I'm presenting the plan for my Final Year Project: **'Vision-Augmented Mobile Robot Navigation in Dynamic Environments'**.*
>
> *To give some quick context: in modern warehouses and factories, thousands of autonomous mobile robots share narrow aisles with human workers and carts. Most of these robots use a standard 2D safety laser scanner mounted near the floor.*
>
> *The big issue with this setup is what researchers call the **'Freezing Robot Problem'**. Because a 2D laser scanner only cuts across a person's legs at ankle height, the navigation system just sees two random dots. It treats those dots as an immovable brick wall. So whenever someone walks across a hallway, the robot panics, freezes in place, or spins around trying to find an exit.*
>
> *My project aims to solve this freezing issue in simulation by pairing the existing 2D laser scanner with an inexpensive monocular camera.*
>
> *Looking at the system architecture diagram here:*
> - *On the left, the camera detects people using lightweight YOLO and keeps track of them across frames using ByteTrack.*
> - *We then match the camera box with the laser scan to find exactly how far away the person is, and feed that into a Kalman filter. This gives us the person's real-time walking speed and direction.*
> - *Finally, over on the right, we pass these predicted movements into a custom plugin for the Nav2 MPPI controller. Instead of assuming the obstacle is stuck where it is right now, the controller predicts where the person will be over the next two seconds and gently steers the robot behind them.*
>
> *This lets the robot navigate smoothly around moving traffic without expensive 3D sensors and entirely on normal CPU compute."*

---

## 4. Key Bullet Points (If You Prefer Speaking Freely)
- **The Problem:** 2D LiDAR can't tell if an obstacle is moving or static $\rightarrow$ robot freezes when people cross the corridor.
- **The Idea:** Camera gives semantic recognition + tracking; 2D LiDAR gives accurate depth; Kalman filter gives velocity.
- **The Controller:** Nav2 MPPI controller uses the velocity to predict where obstacles will be 2 seconds ahead, so the robot doesn't freeze.
- **The Setup:** 100% simulation in Gazebo Harmonic and ROS 2 Jazzy.

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
> *"In short: 2D laser alone makes the robot freeze when people cross; adding camera tracking lets the planner anticipate their motion and steer smoothly around them."*
