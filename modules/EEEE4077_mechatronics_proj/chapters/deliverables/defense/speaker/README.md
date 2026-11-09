# FYP Defence Interview Presentation Guide & Playbook

**Module:** EEEE4077 Mechatronics Project (MEng Final Year Project, 2026/2027)  
**Project Title:** Vision-Augmented Mobile Robot Navigation in Dynamic Environments  
**Student:** Nicholas Khor Han Le (Student ID: 20617556)  
**Supervisor:** Dr. Shalini Darmaraju  
**Moderator:** Ir Dr. Daniel Pu  

---

## 1. How to Think About This Defence Interview

- **The Real Goal:** You do **not** need an intense, academic theoretical defense. The moderator is typically a passive, friendly reviewer who wants to see three simple things:
  1. Do you know what problem you are trying to solve? (Yes: warehouse robots freezing when people cross their path).
  2. Do you have a practical, realistic plan to solve it? (Yes: camera + laser tracking, MPPI controller, and Gazebo simulation).
  3. Are you organized and aware of your risks and timeline? (Yes: 450 hours across Weeks 5–30, 5 progress reviews, and a clear costmap backup plan).
- **Your Tone:** Calm, conversational, structured, and confident. You are simply walking a colleague through your project roadmap.

---

## 2. 4-Slide Presentation Structure (Strict Requirement)

| Slide | File | Visual Asset Used | What You Explain in 90 Seconds |
| :---: | :--- | :--- | :--- |
| **1** | [`01_title_and_architecture.md`](01_title_and_architecture.md) | `../assets/fig1_system_architecture.png` | Why 2D lasers cause robots to freeze, and how adding camera tracking + MPPI planning solves it. |
| **2** | [`02_methods_and_approach.md`](02_methods_and_approach.md) | `../assets/fig2_methodology_flow.png` | Our 6-step roadmap (M0 to M5), why we picked our algorithms, and our C++ backup plan (F1). |
| **3** | [`03_risk_management.md`](03_risk_management.md) | Structured Risk Table | Our 4 technical risks, why R1 (C++ plugin) is our biggest focus, and how our mitigations drop risks to low. |
| **4** | [`04_work_schedule_gantt.md`](04_work_schedule_gantt.md) | `../assets/fig3_gantt_chart.png` | 450h workload across Weeks 5–30 (no W1–4), 5 supervisor reviews, automated testing, and 2-week buffer. |

---

## 3. Simple Delivery Tips for Nicholas

1. **Keep it under 8 minutes:** Aim for ~1.5 to 2 minutes per slide. That leaves plenty of time for casual Q&A.
2. **Point to the diagrams:** Don't memorize a rigid speech. Look at the diagrams and let the arrows guide what you say next.
3. **Use the Anchor Lines:** If your mind goes blank or you stumble, each slide notes file has an **"If You Get Stuck" Anchor Line** at the bottom. Use it to reset and conclude smoothly.
4. **Answer simply:** If the moderator asks a question, give a clear 1-to-2 sentence answer first before elaborating. If you aren't 100% sure, say: *"That's a good point—I'll test that specifically during our milestone review with Dr. Shalini."*
