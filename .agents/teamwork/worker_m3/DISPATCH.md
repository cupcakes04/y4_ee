## 2026-11-12T03:06:15Z
Identity: You are Worker M3 (Topic 3 Synthesis & Widget Developer) for the EEEE4138 Aerial Robotics project.
Working Directory: d:\gdrive\study_notes\degree\y4\.agents\teamwork\worker_m3

MANDATORY: You MUST read the full user request and acceptance criteria in:
d:\gdrive\study_notes\degree\y4\.agents\teamwork\ORIGINAL_REQUEST.md

Project Plan & Survey References:
- Project Plan: d:\gdrive\study_notes\degree\y4\.agents\teamwork\orchestrator_1\PROJECT.md
- Survey Reports:
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_1\handoff.md
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_2\handoff.md
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_3\handoff.md

Exclusive Write Ownership:
- `modules/EEEE4138_aerial_robotics/chapters/topic_3_kinematics_dynamics.md`
- `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task Deliverables:
1. `chapters/topic_3_kinematics_dynamics.md`:
   - Title & Topic Metadata block (Topic 3: 6-DoF Rigid-Body Dynamics & Newton-Euler Equations).
   - Standardized API Contract Table (Inputs: collective thrust T, moments \tau_b = [M_x, M_y, M_z]^T, rotor speeds \Omega_i, mass m, inertia J; Outputs: inertial accelerations \ddot{p}^n, angular accelerations \dot{\omega}_b, 12-state vector x_12; Invariants: conservation of momentum, J strictly positive definite; Downstream: Topic 4, 5).
   - Prerequisite Bridge (Particle dynamics F=ma, single-axis rotational plant \tau = J\ddot{\theta} / 1/Js^2).
   - Step-by-Step Derivations: Transport Theorem in rotating frames proving Coriolis term \dot{v}_b = F_b/m - \omega_b \times v_b; Component expansion of \dot{u}, \dot{v}, \dot{w}; Euler's rotational equations expanding \omega_b \times (J\omega_b) term-by-term for principal axes; Rotor gyroscopic coupling moment \tau_gyro = \omega_b \times [0, 0, J_r \Omega_net]^T; Asymmetric fixed-wing inertia tensor with J_xz \ne 0 and determinant \Gamma = J_x J_z - J_xz^2. Full 12-state nonlinear ODE state-space representation.
   - Worked Numerical Examples from Tutorial 2 (Level UAV vertical motion with m = 1.6 kg, T = 18 N -> \ddot{z} = -1.44 m/s^2; Coriolis acceleration with u = 3, v = 1, r = 0.4 -> \dot{u} = 2.4, \dot{v} = -1.2; Angular acceleration with gyroscopic cross-coupling).
   - Mermaid diagram of the 12-state dynamic system block diagram.
   - Common student pitfalls (Coriolis term causing nonzero \dot{v} despite F_y = 0; confusing body thrust direction with inertial acceleration).
   - Bidirectional markdown cross-links to Topic 1, Topic 2, Topic 4, Topic 5, and companion Widget 3.
2. `widgets/widget_3_rigid_body_dynamics.html`:
   - Self-contained, responsive Generative UI HTML widget using Tailwind CSS CDN + Canvas.
   - 6-DoF dynamic rigid-body simulation running sub-stepped Runge-Kutta 4th Order (RK4) numerical integrator at 240 Hz.
   - Dual Visual Canvases: Left Canvas (3D dynamic quadrotor airframe responding to applied torques, rendering angular velocity \omega and angular momentum H vectors) + Right Canvas (Real-time 3-channel scrolling oscilloscope showing p(t), q(t), r(t)).
   - Interactive controls: Impulse torque buttons (+Pitch, +Roll, +Yaw), sustained torque sliders, motor rotor speed slider \Omega_rotor (0 to 1200 rad/s), toggles for nonlinear cross-terms \omega \times (J\omega) and rotor gyroscopic precession \tau_gyro.
   - Interactive pedagogical experiment banner demonstrating gyroscopic roll induction under pure pitch torque.
   - Offline CSS fallback styling.
3. Test & verify deliverables, update `progress.md`, write `handoff.md`, and call `send_message` when complete.
