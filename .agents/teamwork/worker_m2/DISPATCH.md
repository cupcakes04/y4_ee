## 2026-11-12T03:06:15Z
Identity: You are Worker M2 (Topic 2 Synthesis & Widget Developer) for the EEEE4138 Aerial Robotics project.
Working Directory: d:\gdrive\study_notes\degree\y4\.agents\teamwork\worker_m2

MANDATORY: You MUST read the full user request and acceptance criteria in:
d:\gdrive\study_notes\degree\y4\.agents\teamwork\ORIGINAL_REQUEST.md

Project Plan & Survey References:
- Project Plan: d:\gdrive\study_notes\degree\y4\.agents\teamwork\orchestrator_1\PROJECT.md
- Survey Reports:
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_1\handoff.md
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_2\handoff.md
  * d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_3\handoff.md

Exclusive Write Ownership:
- `modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md`
- `modules/EEEE4138_aerial_robotics/widgets/widget_2_frames_gimbal_lock.html`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task Deliverables:
1. `chapters/topic_2_coordinate_frames.md`:
   - Title & Topic Metadata block (Topic 2: Coordinate Frames, Euler Rotations & Attitude Kinematics).
   - Standardized API Contract Table (Inputs: Euler angles \eta = [\phi, \theta, \psi]^T, body angular rates \omega_b = [p, q, r]^T, unit quaternion q; Outputs: R_b^n \in SO(3), \dot{\eta} = W_\eta \omega_b, \dot{q}, inertial velocities \dot{p}^n; Invariants: R^T R = I, \det(R) = +1, ||q|| = 1; Failures: Gimbal lock |\theta| \ge 85^\circ; Downstream: Topic 3, 5).
   - Prerequisite Bridge (2D rotation matrices, vector dot/cross products, active vs passive transformations).
   - Step-by-Step Derivations: ZYX rotation matrix expansion R_b^n = R_z(\psi) R_y(\theta) R_x(\phi) showing every elementary matrix and intermediate product; Proof of orthogonality (R_b^n)^{-1} = (R_b^n)^T; Derivation of angular rate mapping matrix W_\eta with determinant \cos\theta proving gimbal lock singularity at \theta = \pm 90^\circ; Unit quaternion kinematics \dot{q} = 1/2 q \otimes \bar{\omega} and quaternion rotation matrix R(q).
   - Comprehensive chapter text covering all 6 frames: Inertial NED (\mathcal{F}_i), Vehicle (\mathcal{F}_v), Vehicle-1 (\mathcal{F}_{v1}), Vehicle-2 (\mathcal{F}_{v2}), Body FRD (\mathcal{F}_b), Stability (\mathcal{F}_s), Wind (\mathcal{F}_w). Homogeneous transformations H and analytical inverse H^{-1}.
   - Worked Numerical Examples from Tutorial 1 (Body velocity [4, 0, 0]^T rotated by heading 30^\circ into NED velocities [+3.464, +2.000, 0]^T; camera mounting offset transformation).
   - Mermaid diagram of reference frame hierarchy.
   - Common student pitfalls (NED z-down vs Cartesian z-up, gimbal lock).
   - Bidirectional markdown cross-links to Topic 1, Topic 3, Topic 4, Topic 5, and companion Widget 2.
2. `widgets/widget_2_frames_gimbal_lock.html`:
   - Self-contained, responsive Generative UI HTML widget using Tailwind CSS CDN + Canvas.
   - Software-rendered 3D perspective projection (zero external WebGL libraries).
   - Interactive controls: Sliders for Yaw \psi, Pitch \theta (with "Snap to 90^\circ" button), Roll \phi. Mouse click-and-drag 3D orbit camera controls.
   - 3D visual rendering: Fixed Inertial NED axes, moving Body FRD axes, 3 concentric gimbal rings, 3D quadrotor mesh.
   - Telemetry HUD: Live 3x3 Direction Cosine Matrix R_b^n, Quaternion components [q_w, q_x, q_y, q_z]^T (norm = 1.000), determinant of W_\eta^{-1} (\cos\theta), live pulsing red banner when Gimbal Lock occurs at \theta = \pm 90^\circ.
   - Offline CSS fallback styling.
3. Test & verify deliverables, update `progress.md`, write `handoff.md`, and call `send_message` when complete.
