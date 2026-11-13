---
marp: true
theme: gaia
_class: lead
paginate: true
size: 16:9
style: |
  section {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    padding: 36px 48px;
    background: #FFFFFF;
    color: #0F172A;
  }
  h1 {
    font-size: 26px;
    line-height: 1.25;
    color: #0B2545;
    margin-top: 0;
    margin-bottom: 12px;
    font-weight: 800;
  }
  .sub-tag {
    font-size: 13px;
    font-weight: 800;
    color: #1E40AF;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
  }
  .meta-card {
    background: #EFF6FF;
    border-left: 4px solid #1E40AF;
    padding: 8px 14px;
    border-radius: 4px;
    margin-bottom: 14px;
    font-size: 13.5px;
    line-height: 1.4;
  }
  .card-highlight {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 10px;
    font-size: 13.5px;
    line-height: 1.4;
  }
  .card-highlight strong {
    color: #0B2545;
  }
  /* Slide 2: Compact cards + Ablation Evolution Table */
  section.methods-slide {
    padding: 28px 44px;
  }
  section.methods-slide .card-highlight {
    padding: 7px 12px;
    margin-bottom: 7px;
    font-size: 12.6px;
    line-height: 1.32;
  }
  section.methods-slide .ablation-heading {
    font-size: 13px;
    font-weight: 800;
    color: #0B2545;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 12px 0 6px 0;
  }
  section.methods-slide table.ablation-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0;
    font-size: 11.4px;
    line-height: 1.35;
    border: 1px solid #CBD5E1;
  }
  section.methods-slide table.ablation-table th {
    background: #0B2545;
    color: #FFFFFF;
    padding: 8px 7px;
    text-align: left;
    font-weight: 700;
    font-size: 11.5px;
    border: 1px solid #0B2545;
  }
  section.methods-slide table.ablation-table td {
    padding: 10px 7px;
    border: 1px solid #E2E8F0;
    vertical-align: middle;
    background: #FFFFFF;
  }
  section.methods-slide table.ablation-table tbody tr:nth-child(even) td {
    background: #F8FAFC;
  }
  section.methods-slide table.ablation-table tbody tr.row-proposed td {
    background: #EFF6FF;
  }
  /* Slide 3: Risk Table styling */
  section.risk-slide {
    padding: 30px 48px;
  }
  section.risk-slide table {
    font-size: 14px;
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    border: 1px solid #CBD5E1;
  }
  section.risk-slide th {
    background: #0B2545;
    color: #FFFFFF;
    padding: 11px 12px;
    font-size: 14px;
    font-weight: 700;
  }
  section.risk-slide td {
    padding: 13px 12px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: middle;
    line-height: 1.4;
  }
  section.risk-slide tr:nth-child(even) td {
    background: #F8FAFC;
  }
  .badge-red {
    background: #FEE2E2;
    color: #B91C1C;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
  }
  .badge-green {
    background: #DCFCE7;
    color: #15803D;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
  }
  .badge-amber {
    background: #FEF3C7;
    color: #B45309;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
  }
  /* Slide 4: Gantt styling */
  section.gantt-slide {
    padding: 24px 44px 28px 44px;
  }
---

<!-- Slide 1 -->
![bg right:56% fit](../assets/fig1_system_architecture.png)

<div class="sub-tag">University of Nottingham &middot; EEEE4077 Mechatronics Project</div>

# Vision-Augmented Mobile Robot Navigation in Dynamic Environments

<div class="meta-card">
  Author: <strong>Nicholas Khor Han Le</strong> (ID: 20617556)<br>
  Supervisor: Dr. Shalini Darmaraju &nbsp;|&nbsp; Moderator: Ir Dr. Daniel Pu
</div>

<div class="card-highlight" style="border-left: 4px solid #1E40AF;">
  <strong>Established Space &rarr; Freezing Problem:</strong> Commercial AMRs rely on 2D safety LiDAR + static costmaps for walls. Because planar scans treat walking people as fixed obstacles, robots freeze or spin in shared aisles.
</div>

<div class="card-highlight" style="border-left: 4px solid #0D9488;">
  <strong>Vision-LiDAR Fusion (O1):</strong> Pairs existing 2D LiDAR with a monocular camera (YOLOv8 + ByteTrack + frustum gating) and Kalman filter for real-time obstacle velocities.
</div>

<div class="card-highlight" style="border-left: 4px solid #0B2545;">
  <strong>Predictive MPPI &amp; Methods (O2&ndash;O3):</strong> Custom C++ critic projects motion 2.0s ahead to steer smoothly behind pedestrians on CPU&mdash;built and benchmarked via our 6-step workflow next.
</div>

---

<!-- Slide 2 -->
<!-- _class: methods-slide -->
![bg right:51% fit](../assets/fig2_methodology_flow.png)

<div class="sub-tag">6-Step Lifecycle, Fallback &amp; Ablation Plan</div>

# Methods and Approach

<div class="card-highlight" style="border-left: 4px solid #EF4444; margin-top: 8px;">
  <strong style="color: #B91C1C;">Critical Path (Solid Red):</strong>
  M0 (Docker) &rarr; M1 (Sim &amp; C0) &rarr; M2 (Tracker O1) &rarr; M3 (MPPI Critic O2) &rarr; M5 (Statistical Analysis).
</div>

<div class="card-highlight" style="border-left: 4px solid #3B82F6;">
  <strong style="color: #1E40AF;">Parallel Test Harness (Blue):</strong>
  M4 automated runner (W11&ndash;20) executes Gazebo resets and rosbag2 logging for 450 unattended trials.
</div>

<div class="card-highlight" style="border-left: 4px solid #F59E0B;">
  <strong style="color: #B45309;">Fallback Architecture (F1, Dotted Red):</strong>
  If C++ MPPI critic hits bottlenecks, velocity bubbles are injected directly into standard 2D costmaps.
</div>

<div class="ablation-heading">Expected Ablation Evolution (C0 &rarr; C1 &rarr; C2)</div>

<table class="ablation-table">
  <thead>
    <tr>
      <th style="width: 13%;">ID</th>
      <th style="width: 33%;">Parameters &amp; Stack</th>
      <th style="width: 28%;">Expected Navigation</th>
      <th style="width: 26%;">Target Metrics &amp; Limits</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>C0</strong><br><span style="color:#64748B;font-size:10px;">Baseline</span></td>
      <td>2D LiDAR (20 Hz) + static costmap; 2000 rollouts (&tau; = 0 s)</td>
      <td>Frequent freezes (&Delta;t &ge; 1.5 s, v &lt; 0.05 m/s) &amp; stop&ndash;go delays</td>
      <td>0 collisions (via halts); 0 velocity tracking</td>
    </tr>
    <tr>
      <td><strong>C1</strong><br><span style="color:#64748B;font-size:10px;">Vision</span></td>
      <td>+ RGB (30 FPS, 80&deg; FOV), YOLOv8 + ByteTrack + frustum (v = 0)</td>
      <td>Cuts leg-split false stops; reactive yields only (no lookahead)</td>
      <td>&ge;95% scan&ndash;ID assoc.; &tau; = 0 s clearance</td>
    </tr>
    <tr class="row-proposed">
      <td><strong style="color:#1E40AF;">C2</strong><br><span style="color:#1E40AF;font-size:10px;">Proposed</span></td>
      <td>+ 4-state Kalman CV + C++ critic (&tau; = 2.0 s, 40 steps, &lt;0.5 ms)</td>
      <td><strong>0 freezes, 15&ndash;25% faster</strong> transit (&le;5 s wait), smooth wake steering</td>
      <td><strong>RMSE &lt; 0.15 m/s</strong>, d<sub>min</sub> &ge; 0.35 m, TTC &ge; 1.2 s, <strong>&ge;20 Hz</strong> (450 runs, <em>p</em> &lt; 0.01)</td>
    </tr>
  </tbody>
</table>

---

<!-- Slide 3 -->
<!-- _class: risk-slide -->

<div class="sub-tag">Quantitative Risk Register &middot; Pre- vs Post-Mitigation Ratings</div>

# Risk Management and Mitigation

| ID | Technical Risk Description | Timing | Pre-Score | Mitigation Actions &amp; Fallback Strategy | Post-Score | Shift |
|:--:|:---------------------------|:------:|:---------:|:-------------------------------------------|:----------:|:-----:|
| **R1** | **C++ MPPI critic plugin integration fault or CPU budget overrun** (loop &lt; 20 Hz) | W13–20 | <span class="badge-red">20 (L4, I5)</span> | • Early minimal C++ prototype in Week 13.<br>• Bounded 2.0s horizon + vectorised rollout scoring.<br>• **Fallback F1:** Velocity bubbles in 2D costmap. | <span class="badge-green">6 (L2, I3)</span> | **-70%**<br>(Low) |
| **R2** | **Camera–LiDAR projection error or laser ray bleeding on background walls** | W9–15 | <span class="badge-red">12 (L3, I4)</span> | • Exact sensor transforms from Gazebo SDF.<br>• Median depth filtering inside 2D frustum.<br>• Kalman chi-square innovation outlier rejection. | <span class="badge-green">4 (L1, I4)</span> | **-67%**<br>(Low) |
| **R3** | **Simulation instability or process crash during 450-trial batch evaluation** | W19–24 | <span class="badge-red">12 (L3, I4)</span> | • Pinned Docker container for ROS 2 &amp; Gazebo.<br>• Headless Gazebo execution (cuts RAM by 60%).<br>• Automated Python watchdog reset wrappers. | <span class="badge-green">4 (L1, I4)</span> | **-67%**<br>(Low) |
| **R4** | **Visual occlusion between crossing obstacles causes track ID switching** | W11–15<br>&amp; W21–24 | <span class="badge-amber">9 (L3, I3)</span> | • ByteTrack two-stage association matches low-confidence occluded boxes.<br>• Kalman velocity coasting up to 1.0s. | <span class="badge-green">3 (L1, I3)</span> | **-67%**<br>(Low) |

<p style="font-size: 13.5px; color: #475569; margin-top: 14px; font-style: italic; border-top: 1px solid #E2E8F0; padding-top: 10px;">
  <strong>Governance Takeaway:</strong> All 4 technical risks mitigated to "Low" residual rating. Pure simulation scope (0% hardware) eliminates all physical Health &amp; Safety hazards.
</p>

---

<!-- Slide 4 -->
<!-- _class: gantt-slide -->

<div class="sub-tag">Project Timeline &middot; 26 Weeks &middot; 450 Planned Hours &middot; 5 Supervisory Reviews</div>

# Planned Work Schedule (Weeks 5–30)

<div style="text-align: center; margin: 4px 0 12px 0; border: 1px solid #CBD5E1; border-radius: 6px; padding: 6px 8px; background: #FFFFFF;">
  <img src="../assets/fig3_gantt_chart.png" style="width: 100%; height: auto; display: block;" alt="Gantt Chart">
</div>

<div style="display: flex; gap: 12px; margin-top: 4px;">
  <div class="card-highlight" style="flex: 1.1; border-left: 4px solid #1E40AF; margin-bottom: 0; padding: 7px 12px; font-size: 13px;">
    <strong>Workload: 450 Hours Total</strong><br>
    Autumn (W5–15): 180h (16.4 h/wk) &middot; Spring (W16–30): 270h (18.0 h/wk)
  </div>
  <div class="card-highlight" style="flex: 2; border-left: 4px solid #EF4444; margin-bottom: 0; padding: 7px 12px; font-size: 13px;">
    <strong>5 Progress Reviews (PR1–PR5):</strong><br>
    PR1 (W11): C0 Baseline &middot; PR2 (W14): Tracker &middot; PR3 (W19): MPPI Critic &middot; PR4 (W23): Batch Runs &middot; PR5 (W27): Thesis Draft
  </div>
  <div class="card-highlight" style="flex: 0.9; border-left: 4px solid #10B981; margin-bottom: 0; padding: 7px 12px; font-size: 13px;">
    <strong>Final Safety Buffer:</strong><br>
    Tests finish by W28; final 2 weeks reserved for thesis polishing
  </div>
</div>
