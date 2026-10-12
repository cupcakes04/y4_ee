# 6. Evaluation Metrics & Experimental Benchmarks

Validation is conducted across structured simulation environments (Gazebo Harmonic with scripted dynamic actors) and verified on physical hardware where feasible.

---

## 6.1 Baseline vs. Proposed Targets

| Benchmark Category | Metric | Baseline (Standard Nav2 + 2D LiDAR) | Target (Proposed System) |
|---|---|---|---|
| **Dynamic Cross-Traffic** | Robot Recovery Count (Freezes) | High ($>5$ halts per 10 crossing encounters) | **0 freezes** (smooth yield or trajectory deflection) |
| **Mission Efficiency** | Average Route Completion Time | High variance due to sudden emergency halts | **15–25% reduction** in total route duration |
| **Hazard Compliance** | Keepout Zone Infraction Rate | 100% traversal (unaware of un-mapped floor hazards) | **0% traversal** through detected hazard polygons |
| **Setup & Adaptation** | New Zone Deployment Time | Hours/days (manual CAD drafting & site re-tuning) | **$<30$ minutes** (walkthrough video + text prompting) |
| **Edge Compute** | Real-Time Execution Frame Rate | N/A | **$\ge 25\text{ FPS}$** sustained on target hardware |
| **State Estimation** | Velocity Vector RMSE | N/A (static costmap) | **$< 0.15\text{ m/s}$** linear velocity error |

---

## 6.2 Testing Protocol & Scenarios

- **Scenarios (Gazebo Harmonic, scripted actors for ground truth):**
  - **Scenario A:** Perpendicular pedestrian crossing in a narrow corridor ($1.0–1.5\text{ m/s}$).
  - **Scenario B:** Oncoming pedestrian along a shared transit line.
  - **Scenario C:** Vehicle-like cross-traffic ($1.5–2.0\text{ m/s}$).
  - **Scenario D:** Two crossing pedestrians with staggered intervals.
  - **Scenario E:** Static baseline control with no dynamic agents (regression testing).
- **Configurations Tested:**
  - **B0:** Nav2 + 2D LiDAR + default MPPI critics (baseline, pinned parameters).
  - **P1:** B0 + O1 (Tracker) + O2 (Critic).
  - **P2:** P1 + S1 (Semantic Keepout/Speed Filters).
- **Statistical Significance:**
  - $\ge 30$ randomized runs per scenario with shared random seeds (paired comparisons).
  - Metrics reported as mean $\pm$ 95% confidence intervals.
