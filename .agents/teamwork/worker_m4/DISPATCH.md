## 2026-11-12T03:06:16Z
Identity: You are Worker M4 (Topic 4 Synthesis & Widget Developer) for the EEEE4138 Aerial Robotics project.
Working Directory: d:\gdrive\study_notes\degree\y4\.agents\teamwork\worker_m4

MANDATORY: You MUST read the full user request and acceptance criteria in:
d:\gdrive\study_notes\degree\y4\.agents\teamwork\ORIGINAL_REQUEST.md

Project Plan & Survey References:
- Project Plan: d:\gdrive\study_notes\degree\y4\.agents\teamwork\orchestrator_1\PROJECT.md
- Survey Reports:
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_1\handoff.md
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_2\handoff.md
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_3\handoff.md

Exclusive Write Ownership:
- `modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md`
- `modules/EEEE4138_aerial_robotics/widgets/widget_4_rotor_mixer_allocation.html`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task Deliverables:
1. `chapters/topic_4_forces_moments.md`:
   - Title & Topic Metadata block (Topic 4: Aerodynamic Forces, Rotor Moments & Control Allocation / Mixing).
   - Standardized API Contract Table (Inputs: demanded wrench u_cmd = [F_z, M_x, M_y, M_z]^T, arm length l, k_T, k_M, limits T_min, T_max; Outputs: individual thrusts T_i, motor speed commands \Omega_i, saturation flags; Invariants: moment preservation under saturation; Failures: rank deficiency; Downstream: ESC interface, Topic 3, 5).
   - Prerequisite Bridge (Matrix systems Ax=b, matrix inversion, Newton's 3rd Law of reaction torque).
   - Step-by-Step Derivations: Rotor aerodynamics (T_i = k_T \Omega_i^2, Q_i = k_M \Omega_i^2, k_MT = k_M/k_T); Cross-product formulation r_i \times F_i + M_z,i e_z; Full derivation and explicit algebraic inversion of Plus (+) configuration mixer matrix A_+; Full derivation and explicit algebraic inversion of Cross (\times) configuration mixer matrix A_\times with effective projected arm d = l/\sqrt{2}; Hexarotor geometry (6 arms, \beta_i angles, alternating spins) and derivation of minimum 2-norm allocation via Moore-Penrose pseudo-inverse A_hex^+ = A^T (A A^T)^{-1}.
   - Motor ESC dynamics: 1st-order time lag \tau_m \dot{\Omega} + \Omega = \Omega_cmd. Actuator saturation handling and attitude-priority desaturation (clamping/scaling F_z while preserving differential moments M_x, M_y, M_z). Fixed-wing aerodynamics overview (aerofoil nomenclature, C_L, C_D, dynamic pressure, drag polar).
   - Worked Numerical Examples from Tutorial 3 (Rotor thrust/torque at 500 rad/s; + quad allocation with F_z = -16 N, M_y = 0.100 Nm -> T_1 = 4.2 N, T_3 = 3.8 N; \times quad allocation; hexarotor thrust allocation).
   - Mermaid diagram of control allocation and mixer dataflow.
   - Common student pitfalls (using l instead of l/\sqrt{2} for \times quad; spinning directions and yaw sign cancellation; saturation handling).
   - Bidirectional markdown cross-links to Topic 1, Topic 2, Topic 3, Topic 5, and companion Widget 4.
2. `widgets/widget_4_rotor_mixer_allocation.html`:
   - Self-contained, responsive Generative UI HTML widget using Tailwind CSS CDN + Canvas.
   - Interactive airframe selector: Quadrotor +, Quadrotor \times, Hexarotor \times, Octorotor \times.
   - Virtual command sliders: Collective thrust demand T, roll moment \tau_\phi, pitch moment \tau_\theta, yaw moment \tau_\psi.
   - Interactive motor pod failure sandbox: Clickable motor pods (healthy green -> failed red X with \Omega_k = 0).
   - Desaturation mode toggle: "Strict Clamping" vs "Attitude-Priority Desaturation".
   - Live telemetry and mathematical displays: Mixer matrix M and inverted/pseudo-inverted matrix M^\dagger numerical table, vertical RPM bar gauges for each motor with saturation lines, demanded vs delivered wrench comparison.
   - Offline CSS fallback styling.
3. Test & verify deliverables, update `progress.md`, write `handoff.md`, and call `send_message` when complete.
