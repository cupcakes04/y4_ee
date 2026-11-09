# Slide 2: Methods and Approach

**Slide Goal:** Walk the listener through how you will build and test the system step-by-step, and explain your backup plan.  
**Target Duration:** ~1.5 to 2 minutes.

---

## 1. Quick Summary (What This Slide Is About)
We build the project in 6 logical steps (M0 to M5). We start with setting up the simulation and recording the standard baseline, then build the camera-laser tracker, develop the predictive controller, run batch tests, and analyze the results. If the C++ controller plugin gets too difficult, we have a simple backup plan (Fallback F1).

---

## 2. What to Point to on Screen (Visual Walkthrough)
1. **Critical Path (Red boxes from top to bottom):**
   - **M0 (Setup):** Ubuntu, ROS 2 Jazzy, Gazebo Harmonic in Docker.
   - **M1 (Sim & Baseline C0):** Build the corridor world, add moving human models, and test how badly the standard robot freezes (Condition C0).
   - **M2 (Perception - O1):** Integrate YOLOv8, ByteTrack, and the Kalman Filter to estimate speed.
   - **M3 (Predictive Controller - O2):** Write the C++ dynamic obstacle plugin for MPPI.
   - **M5 (Analysis - O3):** Generate graphs and calculate travel time, waiting time, and freezing stats.
2. **Parallel Path (Blue box on the right):**
   - **M4 (Automated Test Harness):** A Python script that automatically runs trials, resets Gazebo, and logs data in the background so we don't have to manually click 450 times.
3. **Backup Plan (Dotted red arrow F1):**
   - If C++ plugin development takes too long, we use Fallback F1: draw a dynamic bubble in the standard 2D costmap.

---

## 3. Conversational Spoken Script (Natural & Comfortable)

> *"Moving on to our methodology and approach.*
>
> *As shown in the workflow diagram, the project is broken down into six practical milestones, marked M0 through M5.*
>
> *We follow the red critical path:*
> - *We start in M0 and M1 by creating our simulation environment inside Docker using ROS 2 Jazzy and Gazebo Harmonic. Here, we build virtual hallway worlds, add animated walking pedestrians, and record the baseline performance—called **Condition C0**—to see how often the standard robot freezes when people walk past.*
> - *Next, in M2, we build Objective O1: the perception pipeline. We use YOLOv8 for object detection and ByteTrack for multi-object tracking because they run fast on normal CPUs. We then match the camera detection box with the laser scan to find the obstacle's depth, and feed that into a Linear Kalman Filter to get clean, smoothed velocity estimates.*
> - *In M3, we implement Objective O2: the predictive controller. We write a custom plugin in C++ for the Nav2 MPPI local planner. Every control cycle, this plugin projects where the moving person will be over the next two seconds and steers the robot safely around them.*
> - *To make testing manageable, M4 is an automated Python testing harness that runs in parallel. It automatically spawns trials, resets the world, and logs data in the background.*
> - *Finally, in M5, we run 450 automated test runs comparing our predictive system against the baseline, measuring collision rates, route completion times, and how many times the robot stopped or froze.*
>
> *I should also mention that writing a custom C++ plugin for Nav2 is a technical challenge for me. To manage this safely, I have an early prototype scheduled for Week 13, and a complete backup plan—Fallback F1. If the C++ plugin ever gets blocked, F1 draws velocity-stretched safety bubbles directly into the existing costmap, ensuring the project finishes smoothly either way."*

---

## 4. Key Bullet Points (If You Prefer Speaking Freely)
- **M0 & M1:** Setup Docker + Gazebo simulation and test the baseline robot (C0) to measure freezing.
- **M2 (Perception):** Camera detects with YOLO, ByteTrack tracks IDs, laser gives depth, Kalman filter calculates speed.
- **M3 (Controller):** Custom C++ MPPI critic predicts obstacle positions 2 seconds ahead and avoids them.
- **M4 (Automation):** Python script runs tests automatically overnight.
- **M5 (Results):** Compare travel times and freezing across 450 runs.
- **Fallback F1:** If C++ is too complex, use standard costmap inflation bubbles as a proven backup.

---

## 5. Simple Questions the Moderator Might Ask

- **"Why did you choose a Kalman Filter instead of a deep learning model for trajectory prediction?"**
  - *Answer:* *"A Linear Kalman Filter takes less than 0.2 milliseconds of CPU time, which easily fits within our real-time 20 Hz loop. Since people in corridors usually walk at a steady speed for 1 to 2 seconds, a linear model gives us accurate short-term predictions without needing heavy GPU hardware."*

- **"What programming languages are you using?"**
  - *Answer:* *"Python for the perception and tracking nodes (YOLO, ByteTrack, Kalman filter), C++ for the MPPI controller critic plugin to ensure fast real-time performance, and Python for the automated test harness."*

- **"How does the automated test harness work?"**
  - *Answer:* *"It is a Python script that calls Gazebo's reset services, sets the obstacle speeds, commands the robot to drive to a goal, and records everything into ROS 2 bag files automatically. This saves dozens of hours of manual testing."*

---

## 6. "If You Get Stuck" Anchor Line
If you lose your train of thought, pause, take a breath, look at the diagram and say:
> *"To summarize the approach: we build the perception in M2, plug it into the controller in M3, automate the testing in M4, and compare our results against the baseline in M5."*
