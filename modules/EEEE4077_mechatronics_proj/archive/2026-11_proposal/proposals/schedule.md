# Planned Work Schedule & Milestone Roadmap

> **Purpose**: Formal project schedule, workload budget, and progress review milestones for supervisor agreement, Project Planning Report (§6), and thesis timeline reflections.

---

## 1. Workload Budget & Phase Overview

- **Total Allocation:** 450 hours across Weeks 5–30 (26 active weeks following Week 5 start date).
- **True Start:** Week 5 (following project allocation; Weeks 1–4 pre-allocation).
- **Supervisor Reviews:** 5 formal review checkpoints (PR1–PR5) starting in W11–12 and packed sequentially.

| Phase | Weeks | Tasks & Allocation | Total Load | Review Checkpoint |
|---|---|---|---|---|
| **A: Foundations & Baseline** | W5–W12 | **T1:** Setup environment & Docker (W5–W8, 45 h)<br>**T2:** Simulate world, actors & C0 baseline (W7–W12, 45 h) | 90 h | **PR1 (W11–12):** Baseline C0 measured on Scenarios A–D; toolchain frozen. |
| **B: Dynamic Tracker** | W9–W15 | **T3:** O1 LiDAR-vision tracker (W9–W15, 90 h)<br>**T4a:** O3 automated testing harness start (W11–W15, 20 h) | 110 h | **PR2 (W13–15):** O1 velocity RMSE measured; scenario framework ready. |
| **C: Controller & Critic** | W13–W20 | **T5:** O2 MPPI dynamic critic C++ plugin (W13–W20, 75 h)<br>**T4b:** O3 automated testing harness completion (W16–W20, 25 h) | 100 h | **PR3 (W19–20):** Critic running vs C0/C1; ablation harness operational. |
| **D: Multi-Scenario Ablation** | W19–W24 | **T6:** Run comparative simulation benchmarks (W19–W24, 60 h) | 60 h | **PR4 (W23–24):** 3-way ablation results compiled across speeds and densities. |
| **E: Analysis & Thesis** | W23–W30 | **T7:** Analyze results & statistical metrics (W23–W28, 30 h)<br>**T8:** Write final thesis & prepare video demos (W25–W30, 60 h) | 90 h | **PR5 (W27–28):** Statistical analysis complete; final thesis & demo videos ready by W30. |

**Total Hours:** T1 (45) + T2 (45) + T3 (90) + T4 (45) + T5 (75) + T6 (60) + T7 (30) + T8 (60) = **450 hours**.

---

## 2. Gantt Schedule

| Project Task | W1-2 | W3-4 | W5-6 | W7-8 | W9-10 | W11-12 | W13-15 | W16-18 | W19-20 | W21-22 | W23-24 | W25-26 | W27-28 | W29-30 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1. Setup environment & Docker (W5–W8, 45 h) | | | █ | █ | | | | | | | | | | |
| 2. Simulate world, actors & C0 baseline (W7–W12, 45 h) | | | | █ | █ | **PR1** | | | | | | | | |
| 3. Prepare vision-LiDAR tracker (O1) (W9–W15, 90 h) | | | | | █ | █ | **PR2** | | | | | | | |
| 4. Setup automated testing harness (O3) (W11–W20, 45 h) | | | | | | █ | █ | █ | █ | | | | | |
| 5. Develop predictive MPPI critic (O2) (W13–W20, 75 h) | | | | | | | █ | █ | **PR3** | | | | | |
| 6. Run comparative simulation benchmarks (W19–W24, 60 h) | | | | | | | | | █ | █ | **PR4** | | | |
| 7. Analyze results & statistical metrics (W23–W28, 30 h) | | | | | | | | | | | █ | █ | **PR5** | |
| 8. Write final thesis & prepare video demos (W25–W30, 60 h) | | | | | | | | | | | | █ | █ | █ |

---

## 3. Workload Management & Buffers

- **Exam & Coursework Windows:** Lighter workloads (5–8 h/wk) are scheduled during January and April exam periods, offset by higher productivity windows in November and February.
- **Contingency Reserve:** Week 30 provides a final buffer strictly reserved for document polishing, final proofreading, and submission checks.
