# Slide 3: Risk Management and Mitigation

**Slide Goal:** Show that you have thought about what could go wrong, evaluated the impact, and have sensible solutions and backup plans ready.  
**Target Duration:** ~1.5 to 2 minutes.

---

## 1. Quick Summary (What This Slide Is About)
We evaluated 4 technical risks that could slow us down or affect project quality. The biggest one is writing the C++ controller plugin (R1). We have concrete fixes and backups for all 4 risks, reducing every risk down to a safe, manageable level.

---

## 2. What to Point to on Screen (Visual Walkthrough)
1. **Explain the Rating System:** We score risks by Likelihood (1 to 5) times Impact (1 to 5).
2. **Walk through the 4 Risks:**
   - **R1 (C++ Controller Plugin):** Initial Score: 20 (High) $\rightarrow$ Mitigated Score: 6 (Low).
     - *Issue:* Plugin is hard to write or runs too slowly.
     - *Fix:* Prototype early in Week 13, cap prediction to 2 seconds, and use Fallback F1 (costmap layer) if needed.
   - **R2 (Laser Bleeding on Walls):** Initial Score: 12 (Medium) $\rightarrow$ Mitigated Score: 4 (Low).
     - *Issue:* Laser beams pass between legs and hit the back wall, giving bad depth.
     - *Fix:* Use median depth filter inside the camera box and reject outlier jumps in the Kalman filter.
   - **R3 (Simulation Freezing/Crashing):** Initial Score: 12 (Medium) $\rightarrow$ Mitigated Score: 4 (Low).
     - *Issue:* Gazebo crashes during 450 test runs.
     - *Fix:* Use Docker container, run Gazebo in headless mode (no GUI), and use Python watchdog auto-restarts.
   - **R4 (People Walking in Front of Each Other):** Initial Score: 9 (Medium) $\rightarrow$ Mitigated Score: 3 (Low).
     - *Issue:* Tracking IDs swap when one person walks behind another.
     - *Fix:* ByteTrack tracks low-confidence boxes, and the Kalman filter keeps coasting at the last known speed for 1 second.

---

## 3. Conversational Spoken Script (Natural & Comfortable)

> *"Next is Risk Management and Mitigation.*
>
> *To make sure the project finishes on schedule, I identified the four main technical risks shown in this table, rated by Likelihood and Impact on a 1-to-5 scale.*
>
> *Our highest initial risk is **R1**, which scored a 20. This is the risk of the custom C++ MPPI controller plugin being difficult to integrate or taking too much CPU time. To prevent this, I have an early prototype scheduled for Week 13, I keep the forward prediction strictly capped at two seconds, and we have Fallback F1: if the C++ plugin ever gets stuck, we simply inject safety bubbles into the standard costmap.*
>
> *Our second risk, **R2**, is that 2D laser rays can pass between a person's legs and hit the background wall, which would mess up our distance calculation. We fix this by taking the median depth inside the camera box and filtering out sudden jumps in the Kalman filter.*
>
> *Third is **R3**: simulation instability during our 450 batch test runs. Running hundreds of simulation trials can sometimes crash Gazebo. We mitigate this by locking our environment in a Docker container, running Gazebo headless without graphical display to save memory, and using a Python watchdog script that automatically detects stalls and restarts the trial.*
>
> *Finally, **R4** covers occlusion—when two people walk past each other and block the camera view. We use ByteTrack's two-stage matching to hold onto occluded detections, and let the Kalman filter coast the obstacle forward at its last known speed for up to one second.*
>
> *With these mitigations in place, every single risk drops down to a low rating, meaning the project is well-protected against unexpected setbacks."*

---

## 4. Key Bullet Points (If You Prefer Speaking Freely)
- **R1 (C++ Plugin):** Prototyping early + Fallback F1 backup plan $\rightarrow$ Score drops from 20 to 6.
- **R2 (Laser Wall Bleed):** Median depth filter within camera box $\rightarrow$ Score drops from 12 to 4.
- **R3 (Simulation Crashes):** Docker + Headless mode + auto-restart script $\rightarrow$ Score drops from 12 to 4.
- **R4 (Occlusions):** ByteTrack two-stage matching + Kalman coasting $\rightarrow$ Score drops from 9 to 3.
- All risks drop into the green / low zone.

---

## 5. Simple Questions the Moderator Might Ask

- **"Which risk concerns you the most right now?"**
  - *Answer:* *"Definitely Risk 1—the C++ MPPI plugin—because writing Nav2 plugins in C++ is relatively new to me. But because I scheduled an early prototype in Week 13 and designed the costmap fallback F1, I know the project will still deliver regardless of any hiccups."*

- **"Why aren't there any health and safety risks listed?"**
  - *Answer:* *"Because the project is 100% simulated in software with zero hardware, there are no physical lab or electrical hazards. The guidelines specify that this risk register should focus entirely on technical and project management risks."*

- **"What does 'headless Gazebo' mean in R3?"**
  - *Answer:* *"It means running the physics simulator without rendering the 3D graphical window on the screen. It cuts CPU and RAM usage by more than half, so batch simulations run much faster and rarely crash."*

---

## 6. "If You Get Stuck" Anchor Line
If you lose your train of thought, pause, take a breath, look at the table and say:
> *"The main takeaway is: our biggest technical risk is the C++ plugin, but we have early prototyping and a clear costmap backup plan so the project is fully protected."*
