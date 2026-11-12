# Project: EEEE4138 Aerial Robotics Textbook Synthesis & Interactive Generative UI

## Architecture
The EEEE4138 Aerial Robotics textbook synthesis is structured as a modular, API-like pedagogical framework connecting foundational flight physics to advanced modern control. The architecture decouples into 5 sequential core curriculum modules (Topics 1 through 5) plus interactive Generative UI widgets, unified by standardized data structures, coordinate invariants, and bidirectional cross-references.

```
+---------------------------------------------------------------------------------------------------------+
|                                    AERIAL ROBOTICS DATA & CONTROL FLOW                                  |
+---------------------------------------------------------------------------------------------------------+

  [ Topic 1: UAV Architectures & Envelopes ]
       │ Airframe Topology, Mass m, Inertia J, Disc Loading DL, Power Ph, Bounds (θ_max, v_max)
       ▼
  [ Topic 2: Coordinate Frames & Kinematics ]
       │ Inertial NED ↔ Body FRD, Rotation Matrix R_B^I, Euler Rates W_η, Unit Quaternions q
       ▼
  [ Topic 3: 6-DoF Rigid-Body Dynamics ]
       │ Translational Dynamics m·v̇, Rotational Euler Equations J·ω̇ + ω×(Jω) + τ_gyro = τ_b
       ▼
  [ Topic 4: Rotor Forces, Moments & Mixing ]
       │ Thrust T_i = k_T·Ω_i², Torque Q_i = k_M·Ω_i², Mixer Allocation M·Ω² = [T, τ_b]ᵀ, Saturation
       ▼
  [ Topic 5: Flight Control Architectures (Parts I & II) ]
       │ Cascaded Loops (Pos → Att → Rate), Hover Linearization (ẍ ≈ -gθ), State-Space LQR, Integrator Aug
       ▼
  [ Interactive Generative UI Widgets 1–5 ]
       Standalone HTML5 + Tailwind + Canvas/SVG simulations enabling real-time student experimentation
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | Topic 1 Chapter Text | UAV Architectures, classification, 4 forces, sizing, battery endurance math, and flight envelope boundaries | M1 | Topic 1 raw slides & survey |
| F02 | Topic 1 API Contract & Prerequisite Bridge | Formal API table (inputs, outputs, invariants, downstream blocks) and undergraduate prerequisite anchors | M1 | Survey specs |
| F03 | Topic 1 Derivation & Worked Examples | Actuator disc momentum theory, hover power derivation, numerical sizing example | M1 | Survey specs |
| F04 | Widget 1: Flight Envelope Visualizer | Standalone HTML5 + Tailwind + Canvas interactive multi-rotor sizing, disc loading, and battery endurance explorer | M1 | Widget blueprint |
| F05 | Topic 2 Chapter Text | Reference frames (NED, Vehicle, Body FRD), direction cosine matrices, Euler angles, Quaternions | M2 | Topic 2 raw slides & Tutorial 1 |
| F06 | Topic 2 API Contract & Prerequisite Bridge | Formal API table, 2D-to-3D rotation bridge, and intermediate ZYX expansion without unexplained leaps | M2 | Survey specs |
| F07 | Topic 2 Gimbal Lock Derivation & Worked Example | Inversion of Euler rate mapping $W_\eta$, singularity at $\theta=\pm 90^\circ$, and numerical rotation exercises | M2 | Tutorial 1 & Survey specs |
| F08 | Widget 2: 3D Frame & Gimbal Lock Simulator | Standalone HTML5 + Tailwind + Canvas 3D interactive Euler pitch/roll/yaw, body frame vs NED axes, gimbal lock alert | M2 | Widget blueprint |
| F09 | Topic 3 Chapter Text | 6-DoF rigid-body dynamics, Transport Theorem, Newton-Euler translational and rotational equations | M3 | Topic 3 raw slides & Tutorial 2 |
| F10 | Topic 3 API Contract & Prerequisite Bridge | Formal API table, $F=ma$ / $1/Js^2$ prerequisite anchor, and 12-state nonlinear ODE block diagram | M3 | Survey specs |
| F11 | Topic 3 Coriolis & Gyroscopic Derivations | Intermediate algebraic derivation of $\boldsymbol{\omega}\times(J\boldsymbol{\omega})$, rotor gyroscopic precession, worked examples | M3 | Tutorial 2 & Survey specs |
| F12 | Widget 3: 6-DoF Dynamics & Precession Explorer | Standalone HTML5 + Tailwind + Canvas 6-DoF dynamics simulator, RK4 integration, gyroscopic precession demonstration | M3 | Widget blueprint |
| F13 | Topic 4 Chapter Text | Rotor aerodynamics ($T_i, Q_i$), mixer matrices for + and $\times$ quadrotors and hexarotors, motor first-order lag | M4 | Topic 4 raw slides & Tutorial 3 |
| F14 | Topic 4 API Contract & Prerequisite Bridge | Formal API table, linear algebra matrix inversion / pseudo-inverse bridge, and actuator saturation rules | M4 | Survey specs |
| F15 | Topic 4 Mixer Inversion Derivations & Worked Examples | Step-by-step algebraic inversion of $M_+$, $M_\times$, Moore-Penrose pseudo-inverse $M_{\text{hex}}^\dagger$, numerical tutorial drills | M4 | Tutorial 3 & Survey specs |
| F16 | Widget 4: Rotor Mixer & Allocation Sandbox | Standalone HTML5 + Tailwind + Canvas control allocation sandbox, motor failure toggle, attitude-priority desaturation | M4 | Widget blueprint |
| F17 | Topic 5 Chapter Text (Part I & II) | Cascaded flight control, timescale separation, hover linearization, state-space decoupling, LQR design, motor lag stability | M5 | Topic 5 raw slides, Tutorials 4 & 5, Prototype |
| F18 | Topic 5 API Contract & Prerequisite Bridge | Formal API table, second-order SISO control bridge, and Routh-Hurwitz stability proof ($k_d > \tau_m k_p$) | M5 | Survey specs |
| F19 | Topic 5 Controllability Proof & Worked Examples | Full algebraic proof that $\det(\mathcal{C}_{\text{long}}) = (g/J_y^2)^2 \ne 0$, 4 worked numerical tutorial examples | M5 | Tutorials 4 & 5, Prototype |
| F20 | Widget 5: Cascaded Flight Control Simulation | Standalone HTML5 + Tailwind + Canvas 2D flight simulator, real-time cascaded PID & LQR, wind disturbance rejection | M5 | Widget blueprint |
| F21 | E2E Test Suite Infrastructure & Automation | Automated Python validation suite (`scripts/verify_textbook_and_widgets.py`) verifying file existence, syntax, links, and math | M-TEST | Dual-track testing |
| F22 | Cross-Topic Bidirectional Link Graph | Comprehensive bidirectional hyperlinks connecting Topics 1 through 5 and companion widgets | M-FINAL | Final synthesis |
| F23 | Forensic Integrity Verification | Rigorous audit proving authentic derivations, zero hardcoded facade strings, zero plagarism, and layout compliance | M-FINAL | Forensic audit |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M-TEST | E2E Testing Track | Design & implement automated validation harness (`scripts/verify_textbook_and_widgets.py`) covering Tiers 1–4, and publish `TEST_READY.md` | none | DONE |
| M1 | Topic 1 Synthesis & Widget | Create `chapters/topic_1_uav_architectures.md` and `widgets/widget_1_flight_envelope.html` (F01–F04) | none | DONE |
| M2 | Topic 2 Synthesis & Widget | Create `chapters/topic_2_coordinate_frames.md` and `widgets/widget_2_frames_gimbal_lock.html` (F05–F08) | M1 contracts | DONE |
| M3 | Topic 3 Synthesis & Widget | Create `chapters/topic_3_kinematics_dynamics.md` and `widgets/widget_3_rigid_body_dynamics.html` (F09–F12) | M2 contracts | DONE |
| M4 | Topic 4 Synthesis & Widget | Create `chapters/topic_4_forces_moments.md` and `widgets/widget_4_rotor_mixer_allocation.html` (F13–F16) | M3 contracts | DONE |
| M5 | Topic 5 Synthesis & Widget | Create `chapters/topic_5_flight_control.md` and `widgets/widget_5_cascaded_flight_control.html` (F17–F20), integrating & refactoring prototype | M4 contracts | DONE |
| M-FINAL | Integration & Adversarial Verification | Run 100% of E2E validation test suite, verify bidirectional links, adversarial review, and Forensic Integrity Audit (F22–F23) | M-TEST, M1–M5 | DONE |

## Interface Contracts

### Topic 1 $\to$ Downstream Modules
- **Data Export:** Aircraft mass $m\ [\text{kg}]$, inertia tensor $J = \text{diag}(J_x, J_y, J_z)\ [\text{kg}\cdot\text{m}^2]$, arm radius $l\ [\text{m}]$, hover thrust $T_0 = mg\ [\text{N}]$, max tilt angle $\theta_{\max} = \arccos(1/TWR)$.
- **Guarantees:** $TWR \ge 1.5$; $DL < 250\text{ N/m}^2$; strictly right-handed physical coordinate assumptions.

### Topic 2 $\to$ Downstream Modules
- **Data Export:** Direction Cosine Matrix $R_b^n \in SO(3)$, body angular rates to Euler rates mapping $W_\eta$, unit quaternion $\mathbf{q} \in \mathbb{S}^3$, inertial velocity $\dot{\mathbf{p}}^n = R_b^n \mathbf{v}_b$.
- **Guarantees:** Orthonormality $(R_b^n)^T R_b^n = I$; $\det(R_b^n) = +1.0$; Gimbal lock detection at $|\theta| \ge 85^\circ$ where singularity switches attitude propagation to unit quaternion.

### Topic 3 $\to$ Downstream Modules
- **Data Export:** 12-state nonlinear ODE state derivative $\dot{\mathbf{x}} = [\dot{\mathbf{p}}^n, \dot{\mathbf{v}}^n, \dot{\mathbf{\eta}}, \dot{\mathbf{\omega}}_b]^T$; Coriolis cross-terms $\boldsymbol{\omega}_b \times \mathbf{v}_b$; rotational cross-coupling $\boldsymbol{\omega}_b \times (J \boldsymbol{\omega}_b)$; rotor gyroscopic moment $\mathbf{M}_{\text{gyro}}^b = [-qH, pH, 0]^T$.
- **Guarantees:** Conservative energy balance in free flight; positive-definite inertia matrix $J \succ 0$.

### Topic 4 $\to$ Downstream Modules
- **Data Export:** Control allocation matrices $A_+$, $A_\times$, $A_{\text{hex}}$; motor speed transformation $\Omega_{i,\text{cmd}} = \sqrt{T_i / k_T}$; motor first-order lag filter $\tau_m \dot{\Omega} + \Omega = \Omega_{\text{cmd}}$; attitude-priority desaturation algorithm.
- **Guarantees:** Moment preservation invariant: $\sum \mathbf{r}_i \times \mathbf{F}_i \equiv \mathbf{M}_{\text{cmd}}$ preserved when motors saturate, scaling collective thrust $F_z$ down to maintain stable attitude.

### Topic 5 $\to$ Actuators & Simulation
- **Data Export:** Commanded total thrust $T_{\text{cmd}} = \frac{m(g - u_z)}{\cos\phi\cos\theta}$; commanded moments $\mathbf{M}_{\text{cmd}} = [M_x, M_y, M_z]^T$; tilt setpoints $\theta^d = -u_x/g, \phi^d = +u_y/g$; state feedback gain matrix $K$.
- **Guarantees:** Timescale separation $\omega_{n,\text{att}} \ge 5 \omega_{n,\text{pos}}$; motor lag stability condition $k_d > \tau_m k_p$; tilt angle clamping $|\theta^d|, |\phi^d| \le 35^\circ$.

## Code Layout
```
modules/EEEE4138_aerial_robotics/
├── chapters/
│   ├── topic_1_uav_architectures.md         # Topic 1 Chapter
│   ├── topic_2_coordinate_frames.md          # Topic 2 Chapter
│   ├── topic_3_kinematics_dynamics.md        # Topic 3 Chapter
│   ├── topic_4_forces_moments.md             # Topic 4 Chapter
│   ├── topic_5_flight_control.md             # Topic 5 Chapter (Synthesized & Refactored Parts I & II)
│   └── topic_5_flight_ctrl_2.md              # Original prototype retained/archived for reference
├── widgets/
│   ├── widget_1_flight_envelope.html         # Interactive Sizing & Flight Envelope
│   ├── widget_2_frames_gimbal_lock.html      # Interactive 3D Coordinate Frames & Gimbal Lock
│   ├── widget_3_rigid_body_dynamics.html     # Interactive 6-DoF Dynamics & Gyroscopic Precession
│   ├── widget_4_rotor_mixer_allocation.html  # Interactive Rotor Mixer & Control Allocation
│   └── widget_5_cascaded_flight_control.html # Interactive Cascaded PID & LQR Flight Simulation
└── scripts/
    ├── verify_textbook_and_widgets.py        # Automated E2E verification test suite (74 tests)
    └── test_adversarial_physics.py           # Adversarial physics stress test suite (24 tests)
```
