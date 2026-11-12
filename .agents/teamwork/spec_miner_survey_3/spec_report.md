# Specification & Integration Survey Report: Generative UI Widgets (Topics 1–5)
**Module:** EEEE4138 Aerial Robotics  
**Author:** `spec_miner_survey_3`  
**Date:** 2026-11-12  
**Target Scope:** Inventory all Generative UI widgets in `modules/EEEE4138_aerial_robotics/widgets/` and specify exact integration contracts, mapping, iframe embed snippets, and automated verification rules for Topics 1 through 5.

---

## 1. Executive Summary & Authoritative Alignment

In accordance with the directives in `ORIGINAL_REQUEST.md` (specifically Section `## 2026-11-12T04:21:10Z`), this report provides the exhaustive specification for replacing dense text walls and raw code dumps with self-contained, responsive Generative UI HTML widgets.

The module directory contains five fully developed, responsive, client-side interactive visual simulation widgets (`widget_1` through `widget_5`). Each widget is built with Tailwind CSS, HTML5 Canvas 2D/3D mathematics, and zero external runtime dependencies (fully functional offline). This report defines their inventory, exact topic mapping, standardized `<iframe>` embed syntax, fallback links, and automated verification rules.

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Sizing & Aerodynamics | Actuator Disc Momentum Sizer | Computes 1D momentum theory induced velocity $v_i$, induced power $P_i$, disc loading $DL$, and power loading $PL$ across multirotor topologies. | Topology (Quad+, Quad×, Hex×, Octo×), Arm Radius $L \in [0.1, 0.8]\text{ m}$, Prop Diameter $D \in [5, 22]\text{ in}$. | Disc Loading ($DL\text{ [N/m}^2\text{]}$), Induced Power ($P_i\text{ [W]}$), Hover Current ($I\text{ [A]}$). | Propeller collision warning banner if $D > 2L\sin(\pi/N)$. | `widget_1_flight_envelope.html` |
| 2 | Sizing & Aerodynamics | Battery Diminishing Returns Curve | Real-time parametric endurance plot $t_{\text{endurance}}(C_{\text{bat}})$ demonstrating analytical peak at $m_{\text{bat}} = 2m_{\text{fixed}}$ and mass penalty degradation. | Battery Capacity $C \in [1000, 22000]\text{ mAh}$, Cell count (3S, 4S, 6S), Payload mass $[0, 5]\text{ kg}$. | Endurance vs Capacity 2D canvas curve, Operating point marker, Peak mAh statistic, All-up mass. | Underpowered badge and zero tilt if $TWR \le 1.0$. | `widget_1_flight_envelope.html` |
| 3 | Flight Envelope | Envelope Boundaries & Acceleration | Calculates Thrust-to-Weight Ratio $TWR$, maximum tilt angle limit $\theta_{\max} = \arccos(1/TWR)$, and max horizontal acceleration $a_{h,\max} = g\tan\theta_{\max}$. | All-up mass, Total maximum thrust, Gravity ($9.81\text{ m/s}^2$). | TWR badge (Safe, Marginal, Underpowered), $\theta_{\max}$ (deg), $a_{\max}$ (g and $\text{m/s}^2$). | Clamps $\theta_{\max} = 0^\circ$ and $a_{\max}=0$ when $TWR \le 1.0$. | `widget_1_flight_envelope.html` |
| 4 | Coordinate Frames | 3D Intrinsic Euler Gimbal Simulator | Zero-dependency 3D perspective visualization of Tait-Bryan ZYX rotation sequence ($\psi \to \theta \to \phi$) with nested gimbal rings and body/inertial axes. | Yaw $\psi \in [-180^\circ, +180^\circ]$, Pitch $\theta \in [-90^\circ, +90^\circ]$, Roll $\phi \in [-180^\circ, +180^\circ]$, Drag-to-orbit camera. | Interactive 3D Canvas with 3 gimbal rings, Quadrotor wireframe mesh, FRD body vectors, NED inertial vectors. | Pulses red warning banner when $|\theta| \ge 85^\circ$ (singularity approach). | `widget_2_frames_gimbal_lock.html` |
| 5 | Coordinate Frames | Direction Cosine Matrix & Quaternions | Computes live $3\times3$ Direction Cosine Matrix $R_b^n \in SO(3)$, verifies $\det(R)=+1$ and $R^TR=I$, and computes singularity-free unit quaternion $\mathbf{q} \in \mathbb{S}^3$. | Euler angles $[\psi, \theta, \phi]^T$. | $3\times3$ DCM grid display, Unit quaternion components $[q_0, q_1, q_2, q_3]$, Quat norm $\|\mathbf{q}\|$, Condition meter $\cos\theta$. | Displays Euler rate singularity warning $\det(W_\eta^{-1}) \to 0$ at $\theta = \pm 90^\circ$. | `widget_2_frames_gimbal_lock.html` |
| 6 | Coordinate Frames | Body-to-NED Velocity Projector & Angle Recovery | Projects body velocity $[u, v, w]^T$ to inertial $[\dot p_n, \dot p_e, \dot p_d]^T = R_b^n [u, v, w]^T$ and tests Tutorial 1 Q6 angle recovery from DCM. | Body velocities $u, v, w\text{ [m/s]}$, Presets (Tutorial 1 Q6, Banked turn, Level hover). | Inertial velocities $[\dot p_n, \dot p_e, \dot p_d]$, Recovered angles $\theta_{\text{rec}}, \phi_{\text{rec}}, \psi_{\text{rec}}$, Observable $(\phi - \psi)$. | At gimbal lock, isolates observable difference $(\phi - \psi)$ while single angles become indeterminate. | `widget_2_frames_gimbal_lock.html` |
| 7 | Rigid-Body Dynamics | 6-DoF RK4 Dynamics Engine | High-speed Runge-Kutta 4th Order numerical integrator (240 Hz sub-stepping) solving 12-state nonlinear rigid-body equations with quaternion propagation. | Play/Pause, Step (+4.1ms), Applied sustained moments $\mathbf{M}_b$, Instantaneous torque impulses (100ms pulses). | Live 3D quadrotor attitude motion, Kinetic energy $E_{\text{rot}}$, Simulation time clock. | Numerical divergence prevented by quaternion normalization at each sub-step. | `widget_3_rigid_body_dynamics.html` |
| 8 | Rigid-Body Dynamics | Gyroscopic Precession & Oscilloscope | Demonstrates rotor angular momentum cross-coupling $\boldsymbol{\tau}_{\text{gyro}} = \boldsymbol{\omega}_b \times [0, 0, J_r\Omega_{\text{net}}]^T$, generating roll rate $p(t)$ from pure pitch impulse $M_y$. | Rotor speed $\Omega_{\text{rotor}} \in [0, 1200]\text{ rad/s}$, Gyro toggle, Cross-terms toggle, Damping slider. | 3-Channel Scrolling Oscilloscope plotting $p(t)$ (red), $q(t)$ (emerald), $r(t)$ (indigo) in real-time. | Clear Scope button resets history buffer; Zero Rates halts motion. | `widget_3_rigid_body_dynamics.html` |
| 9 | Rigid-Body Dynamics | Inertia Tensor & Nutation Explorer | Evaluates symmetric multirotor, acrobatic quad, and asymmetric fixed-wing aircraft with cross-product of inertia ($J_{xz} \ne 0$) and dynamic nutation. | Inertia preset dropdown (multirotor, racer, fixedwing), Torque inputs. | 3D visual vectors: Angular velocity $\boldsymbol{\omega}_b$ (yellow) and Angular momentum $\mathbf{H}_b = J\boldsymbol{\omega}_b$ (cyan). | Damping slider allows setting zero damping to observe undamped precession. | `widget_3_rigid_body_dynamics.html` |
| 10 | Actuation & Mixing | Airframe Mixer Matrix & Pseudo-Inverse | Computes forward mixer matrix $A \in \mathbb{R}^{4 \times N}$ and Moore-Penrose pseudo-inverse $A^+ = A^T(AA^T)^{-1}$ for Quad+, Quad×, Hex×, Octo× airframes. | Airframe layout buttons, Demanded virtual wrench $\mathbf{u}_{\text{cmd}} = [F_z, M_x, M_y, M_z]^T$ via sliders. | Live rendered matrix entries ($A$ and $A^+$), Individual motor thrusts $T_i$ and RPM gauges, Controllability rank badge. | Detects rank deficiency ($\text{rank}(A) < 4$) and displays red under-actuation alert. | `widget_4_rotor_mixer_allocation.html` |
| 11 | Actuation & Mixing | Motor Failure & Actuator Redundancy | Allows interactive clicking of individual motor pods to simulate hardware failure, immediately updating active health masking in the pseudo-inverse. | Motor pod click toggles, Quick presets (Hex motor #1 failure, Level hover, Aggressive roll). | Dynamic reallocation of motor forces; Airframe canvas with green/red status indicators; Demanded vs Delivered tracking table. | Quadrotor failure causes loss of control (rank < 4); Hexarotor maintains rank 4 and level hover. | `widget_4_rotor_mixer_allocation.html` |
| 12 | Actuation & Mixing | Attitude-Priority Desaturation | Solves motor thrust limit violations ($T_{\min}=0.2\text{ N}, T_{\max}=8.0\text{ N}$) by scaling collective thrust $F_z$ to preserve attitude moments $M_x, M_y, M_z$. | Desaturation mode toggle (Attitude-Priority vs Strict Clamping), High thrust + high moment demand. | Real-time comparison table showing Demanded vs Delivered wrench tracking percentage (100% vs degraded). | In Strict Clamping mode, moment tracking drops to ~20-40%, demonstrating loss of attitude authority. | `widget_4_rotor_mixer_allocation.html` |
| 13 | Flight Control | Cascaded Flight Control Simulator | Closed-loop 2D flight dynamics simulator with outer position loop ($x \to \theta^d$), inner attitude loop ($\theta \to M_y$), and double-integrator altitude channel ($z \to T$). | Interactive canvas drag/click target crosshair, Step test buttons ($\pm 2\text{m X}, \pm 1\text{m Z}$), Tuning sliders. | Dynamic 2D side-view flight animation, Drone position, Attitude tilt, Wind streaks, G-force HUD. | Unstable gains cause drone to accelerate off-screen or oscillate wildly; Reset restores initial state. | `widget_5_cascaded_flight_control.html` |
| 14 | Flight Control | Timescale Separation Analysis | Evaluates bandwidth separation ratio $\omega_{\text{att}} / \omega_{\text{pos}}$ and demonstrates instability caused by sluggish attitude loop bandwidth. | PID tuning sliders ($K_{p,pos}, K_{d,pos}, K_{i,pos}, k_{p,\theta}, k_{d,\theta}$), Presets (5x Separation, Sluggish Att, Aggressive Pos). | Real-time separation ratio badge ($\omega_{\text{att}} / \omega_{\text{pos}} = 6.0\times$ vs $1.0\times$), 3-channel scope ($x(t), \theta(t), M_y(t)$). | Sluggish attitude preset ($1.0\times$) triggers severe phase lag and diverging flight crash. | `widget_5_cascaded_flight_control.html` |
| 15 | Flight Control | State-Space LQR & CARE Solver | Solves the Continuous Algebraic Riccati Equation (CARE) live in browser via Newton-Kleinman iteration, computing optimal state feedback gain $u = -K_{\text{LQR}}\mathbf{x}$. | State weight sliders ($q_x, q_v, q_\theta, q_q$) and control weight slider ($r_u$) via Bryson's rule. | Optimal gain vector $K = [k_x, k_v, k_\theta, k_q]$, Closed-loop eigenvalues (poles) displayed live. | Disallows negative weights; Newton-Kleinman iteration converges within 10 iterations. | `widget_5_cascaded_flight_control.html` |
| 16 | Flight Control | Motor Lag & Disturbance Rejection | Implements first-order ESC lag $\tau_m$, validates Routh-Hurwitz stability criterion $k_{d,\theta} > \tau_m k_{p,\theta}$, and tests wind disturbance rejection. | ESC time constant $\tau_m \in [0.005, 0.060]\text{ s}$, Horizontal wind force slider $F_{\text{wind},x}$, Wind gust pulse buttons. | Motor lag status banner ($k_d > \tau_m k_p$ check), Wind HUD indicator, Steady-state position error vs integral action. | If $k_{d,\theta} \le \tau_m k_{p,\theta}$, banner turns red warning of motor lag instability. | `widget_5_cascaded_flight_control.html` |

---

## Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Widget 1: Airframe Clearance | Arm radius $L = 0.10\text{ m}$, Propeller diameter $D = 22.0\text{ inches}$ ($0.5588\text{ m}$) | Distance between hubs is $2L\sin(\pi/4) = 0.141\text{ m} < 0.5588\text{ m}$. Clearance is negative ($-0.417\text{ m}$). Top-down schematic draws heavily intersecting red rotor discs. Banner displays flashing alert: *"Propeller collision hazard! Increase arm radius L."* |
| 2 | Widget 1: Extreme Battery Sizing | Battery capacity $C = 22,000\text{ mAh}$ on 4S (Battery mass $\approx 1.92\text{ kg}$, Total mass $\approx 3.17\text{ kg}$) | Total hover power escalates to $> 360\text{ W}$ due to $P \propto m^{3/2}$. Hover endurance drops to $\approx 14.2\text{ minutes}$, which is substantially LOWER than the peak endurance of $22.5\text{ minutes}$ achieved at $8,500\text{ mAh}$ ($0.74\text{ kg}$ battery). Directly demonstrates the 2:1 diminishing returns law. |
| 3 | Widget 1: Underpowered Airframe | Payload mass $m_{\text{load}} = 5.0\text{ kg}$, Battery $4000\text{ mAh}$ (Total mass $6.30\text{ kg}$, Weight $61.8\text{ N}$) | Total maximum thrust ($32.0\text{ N}$) is less than aircraft weight ($61.8\text{ N}$). $TWR = 0.52 < 1.0$. HUD badge displays *"UNDERPOWERED"*, Max tilt angle clamps to $0.0^\circ$, max horizontal acceleration is $0.00\text{ g}$. |
| 4 | Widget 2: Positive Gimbal Lock | Click "Snap Lock (+90°)" preset ($\theta = +90.0^\circ, \psi = 0^\circ, \phi = 0^\circ$) | Gimbal lock alert banner pulses red: *"GIMBAL LOCK SINGULARITY ACTIVE ($|\theta| \ge 85^\circ$)"*. Condition meter drops to $\cos\theta = 0.0000$ (progress bar 0%). Pitch ring becomes vertical; Roll axis and Inertial Yaw axis become strictly collinear. Angle recovery analyzer shows recovered pitch $= +90.0^\circ$, single roll/yaw indeterminate, observable $(\phi - \psi) = 0.0^\circ$ appears. Unit quaternion $\|\mathbf{q}\| \equiv 1.0000$ and DCM determinant $\det(R) \equiv +1.0000$ remain perfectly stable. |
| 5 | Widget 2: Negative Gimbal Lock | Click "Snap Lock (-90°)" preset ($\theta = -90.0^\circ$) | Red alert banner triggers, condition meter hits $0.0000$, roll and yaw axes align in opposite orientation. Observable $(\phi + \psi)$ is isolated. Quaternion norm remains exactly $1.0000$. |
| 6 | Widget 3: Pure Pitch Gyroscopic Coupling | $\Omega_{\text{rotor}} = 1000\text{ rad/s}$, Precession ON, Click "+Pitch Impulse (+0.5 N·m)" | Aircraft experiences a 100ms pitch torque impulse. Despite applied roll torque $M_x \equiv 0$, the oscilloscope red trace ($p(t)$, roll rate) immediately spikes to $> 0.8\text{ rad/s}$ ($45^\circ/\text{s}$). Confirming the theoretical cross-coupling equation $\dot{p} = -\frac{q J_r \Omega_{\text{net}}}{J_x}$. |
| 7 | Widget 3: Gyroscopic Precession Disabled | Precession toggle OFF, Click "+Pitch Impulse (+0.5 N·m)" | Only pitch rate $q(t)$ (green trace) responds, while roll rate $p(t)$ (red) and yaw rate $r(t)$ (indigo) remain strictly zero ($0.000\text{ rad/s}$). Confirms that SISO decoupling in textbooks is only an approximation valid when rotor gyroscopic precession is neglected. |
| 8 | Widget 4: Quadrotor Single Motor Failure | Topology Quad+, Click Motor Pod #1 (Front) to set health = 0 | Motor #1 thrust drops to $0.0\text{ N}$ (red X). Matrix rank badge immediately changes from green *"Rank 4: Controllable"* to flashing red *"CRITICAL: Rank Deficient! Under-actuated flight"*. Since $\text{rank}(A) = 3 < 4$, the quadrotor cannot independently control pitch moment and collective thrust. |
| 9 | Widget 4: Hexarotor Single Motor Failure | Topology Hex×, Click Motor Pod #1 (FL) to set health = 0 | Motor #1 fails (red X). However, the rank badge remains green: *"Rank 4: Controllable"*. The Moore-Penrose pseudo-inverse $A^+$ automatically re-allocates thrust across the remaining 5 healthy motors, delivering 100% of demanded collective thrust ($16.0\text{ N}$) and zero moments ($0.0\text{ Nm}$), proving multirotor fault tolerance! |
| 10 | Widget 4: Actuator Saturation Clash | Demanded Thrust $T = 28.0\text{ N}$, Pitch Moment $M_y = +1.5\text{ Nm}$ (Motors hit $T_{\max} = 8.0\text{ N}$) | In **Strict Clamping**: individual motor outputs clip at $8.0\text{ N}$. Delivered pitch moment collapses from $1.50\text{ Nm}$ to $0.38\text{ Nm}$ (only $25\%$ delivered), leading to loss of attitude control! In **Attitude-Priority**: collective thrust is automatically derated from $28.0\text{ N}$ to $22.5\text{ N}$, while pitch moment is delivered at $1.50\text{ Nm}$ ($100\%$ tracking), preserving attitude stabilization. |
| 11 | Widget 5: Timescale Separation Breakdown | Click "Sluggish Att" preset ($k_{p,\theta}=20, k_{d,\theta}=3.0, K_{p,pos}=4.0$) | Bandwidth ratio drops from $6.0\times$ down to $\omega_{\text{att}} / \omega_{\text{pos}} = 1.2\times$. Commanding a 2m position step causes the drone attitude to lag far behind the demanded tilt $\theta^d$. The delayed thrust vector creates positive feedback, resulting in severe overshoot, wild oscillations, and a crash into the ground within 3 seconds. |
| 12 | Widget 5: Motor ESC Lag Instability | Motor time constant $\tau_m$ increased to $0.050\text{ s}$, $k_{p,\theta} = 400.0, k_{d,\theta} = 15.0$ | Condition check $k_{d,\theta} > \tau_m k_{p,\theta}$ evaluates to $15.0 < 20.0$ (VIOLATED). Banner flashes red warning of motor lag instability. The high-frequency phase lag from the ESC causes limit-cycle flutter and divergent attitude oscillation on the oscilloscope. |
| 13 | Widget 5: Constant Wind Disturbance Offset | Inject constant horizontal wind force $F_{\text{wind},x} = +3.0\text{ N}$, set $K_{i,pos} = 0.0$ | The quadrotor hovers with a persistent steady-state offset error $e_{x,ss} \approx 0.75\text{ m}$ downwind. When $K_{i,pos}$ is raised to $1.20$, the integrator winds up, tilts the drone into the wind ($\theta < 0$), and reduces the steady-state position error strictly to $0.00\text{ m}$. |

---

## 2. Comprehensive Inventory of Generative UI Widgets

The table below catalogs the five HTML widgets located in `modules/EEEE4138_aerial_robotics/widgets/`:

| Widget File | Relative Path from Chapters | Size (Bytes) | Primary Topic | Core Subject Matter | Interactive Visualizations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `widget_1_flight_envelope.html` | `../widgets/widget_1_flight_envelope.html` | 41,136 | Topic 1 | Actuator Disc Theory, Sizing, Battery Diminishing Returns, Flight Envelope | Top-down airframe schematic (CW/CCW rotor discs), 2D endurance vs capacity curve, Telemetry HUD. |
| `widget_2_frames_gimbal_lock.html` | `../widgets/widget_2_frames_gimbal_lock.html` | 55,139 | Topic 2 | Coordinate Frames (NED/FRD), Tait-Bryan Rotations, Gimbal Lock Singularity, Quaternions | 3D gimbal ring viewport, $3\times3$ DCM matrix display, Unit quaternion HUD, Condition meter, Velocity projector. |
| `widget_3_rigid_body_dynamics.html` | `../widgets/widget_3_rigid_body_dynamics.html` | 54,386 | Topic 3 | Newton-Euler 6-DoF Dynamics, Gyroscopic Precession, Transport Theorem, Nutation | 3D airframe projection with $\boldsymbol{\omega}$ and $\mathbf{H}$ vectors, 3-Channel live scrolling oscilloscope ($p, q, r$). |
| `widget_4_rotor_mixer_allocation.html` | `../widgets/widget_4_rotor_mixer_allocation.html` | 51,722 | Topic 4 | Rotor Mixer Matrix $A$, Moore-Penrose Pseudo-Inverse $A^+$, Motor Failure, Desaturation | Interactive clickable airframe schematic, Motor thrust & RPM bar gauges, Live solved matrix inspector, Tracking table. |
| `widget_5_cascaded_flight_control.html` | `../widgets/widget_5_cascaded_flight_control.html` | 58,788 | Topic 5 | Cascaded PID, Timescale Separation, State-Space LQR, CARE Solver, Motor ESC Lag | 2D side-view flight canvas with interactive drag setpoint, 3-Channel oscilloscope, Riccati solver telemetry, Disturbance deck. |

All widgets share the following design invariants:
1. **Zero External CDN Dependencies for Runtime Math:** All physical equations (RK4 integrator, Riccati solver, Moore-Penrose pseudo-inverse, 3D projection) are executed in vanilla JavaScript.
2. **Offline Fallback CSS:** Each widget includes internal scoped CSS variables (`--bg-dark: #020617`, etc.) ensuring identical dark-mode rendering even when offline or behind air-gapped university firewalls.
3. **Clean Embed Compatibility:** Designed to render cleanly within an iframe of minimum width $600\text{ px}$ and height $520\text{ px}$ without scrollbars or clipped canvases.

---

## 3. Topic-by-Topic Pedagogical Mapping & Integration Contracts

### Topic 1: UAV Architectures, Classification & Flight Envelopes
* **Target File:** `modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md`
* **Assigned Widget:** `widget_1_flight_envelope.html`
* **Pedagogical Alignment:**
  * **Section 4 (Actuator Disc Momentum Theory):** Reinforces the Rankine-Froude 1D momentum equations ($v_i = \sqrt{T/(2\rho A)}$, $P_i = T^{3/2}/\sqrt{2\rho A}$). Students can adjust propeller diameter $D$ and watch induced power drop as disc area expands.
  * **Section 6 (Diminishing Battery Returns):** Mathematically proves that $m_{\text{bat}} = 2m_{\text{fixed}}$ is the theoretical peak. Widget 1 plots the exact endurance curve, allowing students to observe that adding battery capacity beyond $\approx 8500\text{ mAh}$ degrades flight time.
  * **Section 11 (Flight Envelope Boundaries):** Connects Thrust-to-Weight Ratio to maximum tilt angle $\theta_{\max} = \arccos(1/TWR)$ and horizontal acceleration limits $a_{h,\max} = g\tan\theta_{\max}$.
  * **Section 12 (Comprehensive Worked Numerical Example):** The "Tutorial Benchmark" preset in Widget 1 uses the exact numeric values ($1.6\text{ kg}$ all-up mass, $10\text{-inch}$ props, $4S$ LiPo, $4000\text{ mAh}$) analyzed in the worked problem.
* **Exact Embed Location:**
  * Embed in **Section 6.5** immediately following Equation (1.22) (around Line 243), replacing the standalone text link with the live interactive iframe and fallback link.

---

### Topic 2: Coordinate Frames, Euler Rotations & Attitude Kinematics
* **Target File:** `modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md`
* **Assigned Widget:** `widget_2_frames_gimbal_lock.html`
* **Pedagogical Alignment:**
  * **Section 4 & 5 (Reference Frames & Direction Cosine Matrix):** Visualizes the six reference frames, intrinsic Tait-Bryan ZYX Euler sequence ($\psi \to \theta \to \phi$), and the live entries of $R_b^n \in SO(3)$ with verified orthogonality $R^TR=I$ and $\det(R)=+1.0000$.
  * **Section 6 (Euler Rate Kinematics & Gimbal Lock):** Directly demonstrates how pitching to $\theta = \pm 90^\circ$ causes the roll ($X_b$) and yaw ($Z_v$) gimbal rings to become collinear in 3D space, causing $\det(W_\eta^{-1}) = \cos\theta \to 0$ and rates $[\dot\phi, \dot\psi] \to \infty$.
  * **Section 7 (Unit Quaternions):** Shows how unit quaternions $\mathbf{q} \in \mathbb{S}^3$ maintain smooth, singularity-free attitude propagation ($\|\mathbf{q}\| \equiv 1.0000$) even when Euler angles are locked.
  * **Section 9 & 10 (Tutorial 1 Q6 Angle Recovery Drill):** Demonstrates extracting Euler angles from DCM and isolates the observable difference $(\phi - \psi)$ at singularity.
* **Exact Embed Location:**
  * Embed in **Section 10 (Interactive Generative UI Visualizer Widget)** at Line 941, replacing the static KaTeX box `\boxed{\text{Open Companion Widget: ...}}`.
  * Secondary interactive link in **Section 6.3 / Section 7** (Line 561).

---

### Topic 3: 6-DoF Rigid-Body Dynamics & Newton-Euler Equations
* **Target File:** `modules/EEEE4138_aerial_robotics/chapters/topic_3_kinematics_dynamics.md`
* **Assigned Widget:** `widget_3_rigid_body_dynamics.html`
* **Pedagogical Alignment:**
  * **Section 4 (Euler's Rotational Dynamics):** Illustrates the Newton-Euler equations $\mathbf{M}_b = J\dot{\boldsymbol{\omega}}_b + \boldsymbol{\omega}_b \times (J\boldsymbol{\omega}_b) + \boldsymbol{\tau}_{\text{gyro}}$ and rotational kinetic energy $E_{\text{rot}} = \frac{1}{2}\boldsymbol{\omega}_b^T J \boldsymbol{\omega}_b$.
  * **Section 5 (Rotor Gyroscopic Coupling & Precession):** Provides a direct interactive proof of gyroscopic precession. When students click "+Pitch Impulse (+0.5 N·m)" with rotor speed at $1000\text{ rad/s}$, the right-hand oscilloscope immediately shows a large roll rate $p(t)$ (red trace) despite applied roll torque being zero ($M_x = 0$).
  * **Section 6 (Asymmetric Inertia Tensors for Fixed-Wing $J_{xz} \ne 0$):** Demonstrates cross-product of inertia coupling roll and yaw dynamics.
  * **Section 11 (Interactive Simulation: Companion Widget 3):** The step-by-step guided experiments in the chapter text describe the exact buttons and toggles present in Widget 3.
* **Exact Embed Location:**
  * Embed in **Section 11 (Interactive Simulation: Companion Widget 3)** at Line 684, immediately preceding the "Guided Interactive Experiments" walkthrough.

---

### Topic 4: Aerodynamic Forces, Rotor Moments & Control Allocation / Mixing
* **Target File:** `modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md`
* **Assigned Widget:** `widget_4_rotor_mixer_allocation.html`
* **Pedagogical Alignment:**
  * **Section 4.3 & 4.4 (Plus and Cross Quadrotor Mixers):** Allows toggling between Quad+ and Quad× geometries, inspecting the forward mixer matrix $A$ and inverse $A^{-1}$.
  * **Section 4.5 (Hexarotor Geometry & Pseudo-Inverse Allocation):** Demonstrates over-actuated multirotors ($N=6, 8$) where $A^+ = A^T(AA^T)^{-1}$ minimizes motor 2-norm thrust ($\min \|\mathbf{u}\|_2^2$).
  * **Section 4.7 (Actuator Saturation & Attitude-Priority Desaturation):** Replaces the raw Python script (`attitude_priority_allocation`) with a live sandbox. Students can observe how Attitude-Priority automatically scales collective vertical thrust $F_z$ to preserve 100% of differential moments $M_x, M_y, M_z$, while Strict Clamping causes catastrophic attitude collapse.
  * **Motor Failure Fault-Tolerance:** Students can click individual motor pods to trigger failures. Quadrotors become rank-deficient ($\text{rank} < 4$), whereas Hexarotors reallocate thrust and remain controllable!
* **Exact Embed Location:**
  * Embed in **Section 4.7** (replacing the raw Python code block at Lines 570–634).
  * Relocate the erroneous tip box from Section 4.8.4 (Line 706) to Section 4.7.

---

### Topic 5: Flight Control Architectures (Cascaded Loops, State-Space & LQR)
* **Target File:** `modules/EEEE4138_aerial_robotics/chapters/topic_5_flight_control.md`
* **Assigned Widget:** `widget_5_cascaded_flight_control.html`
* **Pedagogical Alignment:**
  * **Section 3.1 (Vertical Flight & Altitude Loop):** Double-integrator altitude channel with integral anti-windup clamping.
  * **Section 3.2 (Underactuation Principle & Tilt-to-Accelerate):** Demonstrates that horizontal motion requires airframe tilt ($\theta^d = -u_x / g$), explaining the fundamental physical origin of the negative sign in NED coordinates.
  * **Section 3.4 (The Timescale Separation Theorem):** Features the "5x Separation" vs "Sluggish Att" presets, directly showing that violating $\omega_{\text{att}} \gg \omega_{\text{pos}}$ causes phase lag and flight instability.
  * **Section 3.5 (Motor ESC First-Order Lag):** Real-time monitoring of the Routh-Hurwitz stability criterion $k_{d,\theta} > \tau_m k_{p,\theta}$.
  * **Section 4.3 (State-Space LQR & CARE Solver):** Tab B solves the Continuous Algebraic Riccati Equation (CARE) live in browser, displaying optimal gain vector $K$ and closed-loop poles using Bryson's rule penalty sliders.
* **Exact Embed Location:**
  * Embed in **Section 3.2** (Line 205), right where the Underactuation Principle and Tilt-to-Accelerate mapping are introduced.
  * Cross-reference in **Section 4.3** (LQR Optimal Control).

---

## 4. Standardized Iframe Embed Syntax & Fallback Link Specification

To ensure seamless integration across diverse Markdown renderers (Obsidian, VS Code Markdown Preview, GitHub/GitLab web views, static site generators), all embeds must follow a strict standard contract.

### Standard Embed Template
```html
<iframe src="../widgets/widget_X_name.html" width="100%" height="520" frameborder="0"></iframe>
<p align="center"><em><a href="../widgets/widget_X_name.html" target="_blank">👉 Open Widget X in standalone window</a></em></p>
```

### Exact Embed Snippets for Topics 1 through 5

#### Topic 1 Embed Snippet
```html
<iframe src="../widgets/widget_1_flight_envelope.html" width="100%" height="520" frameborder="0"></iframe>
<p align="center"><em><a href="../widgets/widget_1_flight_envelope.html" target="_blank">👉 Open Widget 1: Multi-Rotor Sizing & Flight Envelope Explorer in standalone window</a></em></p>
```

#### Topic 2 Embed Snippet
```html
<iframe src="../widgets/widget_2_frames_gimbal_lock.html" width="100%" height="520" frameborder="0"></iframe>
<p align="center"><em><a href="../widgets/widget_2_frames_gimbal_lock.html" target="_blank">👉 Open Widget 2: 3D Coordinate Frames & Gimbal Lock Simulator in standalone window</a></em></p>
```

#### Topic 3 Embed Snippet
```html
<iframe src="../widgets/widget_3_rigid_body_dynamics.html" width="100%" height="520" frameborder="0"></iframe>
<p align="center"><em><a href="../widgets/widget_3_rigid_body_dynamics.html" target="_blank">👉 Open Widget 3: 6-DoF Rigid-Body Dynamics & Precession Explorer in standalone window</a></em></p>
```

#### Topic 4 Embed Snippet
```html
<iframe src="../widgets/widget_4_rotor_mixer_allocation.html" width="100%" height="520" frameborder="0"></iframe>
<p align="center"><em><a href="../widgets/widget_4_rotor_mixer_allocation.html" target="_blank">👉 Open Widget 4: Rotor Mixer & Control Allocation Sandbox in standalone window</a></em></p>
```

#### Topic 5 Embed Snippet
```html
<iframe src="../widgets/widget_5_cascaded_flight_control.html" width="100%" height="520" frameborder="0"></iframe>
<p align="center"><em><a href="../widgets/widget_5_cascaded_flight_control.html" target="_blank">👉 Open Widget 5: Cascaded Flight Control & LQR Simulation in standalone window</a></em></p>
```

### Rationale for Dimensions & Fallbacks
1. `width="100%"`: Enables fluid responsive layout inside standard Markdown note viewports, whether on mobile, tablet, or ultrawide monitors.
2. `height="520"`: Perfectly fits the multi-column canvas + HUD panels without internal vertical scrollbars, while preventing unnecessary page displacement.
3. `frameborder="0"`: Removes unsightly default iframe borders for seamless dark-theme integration.
4. **Standalone Fallback Link:** Critical for environments where iframe execution is sandboxed or disabled by security policies (e.g. GitHub web previews, certain VS Code extensions). Ensures that students always have a single-click path to launch the simulation in an external browser tab.

---

## 5. Automated Verification Rules & Validation Protocol

To guarantee that the textbook chapters maintain 100% rendering reliability and pedagogical compliance, four automated verification rules have been formulated.

### Rule 1: Zero Code Implementation Dumps
* **Assertion:** Fenced multiline code blocks (` ```...``` `) in chapter files must ONLY be `mermaid`.
* **Prohibited:** Any programming code implementations (e.g., Python `def attitude_priority_allocation`, MATLAB scripts, C/C++ classes).
* **Allowed:** Inline code backticks (`` `u_cmd` ``, `` `A_moment_inv` ``) for mathematical symbols, parameters, and API identifiers.
* **Pass Criterion:**
  $$\sum_{\text{blocks}} \left[ \text{lang} \notin \{\text{"mermaid"}\} \right] \equiv 0$$

### Rule 2: Valid Iframe Syntax & Local Asset Resolution
* **Assertion:** Every `<iframe>` tag must match standard attributes (`width="100%"`, `height="520"`, `frameborder="0"`), and the relative `src` path must resolve to an existing file in `widgets/`.
* **Pass Criterion:**
  $$\forall \, \text{iframe} \in \text{chapters}, \quad \text{os.path.exists}(\text{resolve}(\text{src})) \equiv \text{True}$$

### Rule 3: Robust Mermaid Diagram Formatting
* **Assertion:** All Mermaid diagrams must parse cleanly without crashing standard Markdown rendering engines.
* **Specific Constraints:**
  1. Node labels containing parentheses `()`, brackets `[]`, colons `:`, ampersands `&`, or newlines must be enclosed in explicit double quotes (e.g. `NODE["Label (with) & details"]`).
  2. No raw unquoted `<br/>` tags inside node shapes.
  3. No empty or unreferenced style definitions.

### Rule 4: KaTeX Equation Rendering & Delimiter Balance
* **Assertion:** All mathematical equations must be properly enclosed by matched delimiters without syntax crashes.
* **Specific Constraints:**
  1. Even count of unescaped single `$` delimiters per paragraph (inline math).
  2. Even count of unescaped double `$$` delimiters (display math).
  3. Strict pairing of LaTeX environments (e.g., `\begin{bmatrix} ... \end{bmatrix}`, `\begin{aligned} ... \end{aligned}`).

---

## 6. Audit Findings in Existing Chapters

The automated scan of existing chapters in `modules/EEEE4138_aerial_robotics/chapters/` identified the following specific defects that should be resolved during implementation:

1. **Standalone Python Code Block in Topic 4:**
   * **Location:** `topic_4_forces_moments.md`, Lines 570–634 (`attitude_priority_allocation`).
   * **Defect:** 64 lines of Python reference implementation violating the "zero code blocks" requirement.
   * **Remedy:** Replace this block with the embedded `widget_4_rotor_mixer_allocation.html` iframe and fallback link.

2. **Misplaced Widget 4 Launch Tip in Topic 4:**
   * **Location:** `topic_4_forces_moments.md`, Line 706.
   * **Defect:** The launch link for Widget 4 was placed under Section 4.8.4 (Fixed-Wing Induced Drag), rather than Section 4.7 (Rotor Control Allocation & Desaturation).
   * **Remedy:** Relocate the embed to Section 4.7 where rotor allocation and desaturation are derived.

3. **Mermaid Unquoted Special Characters:**
   * **Location:** `topic_1_uav_architectures.md`, Diagram #7 (Lines 408–434).
   * **Defect:** Nodes `B` (`Power Distribution\nBoard & ESCs`) and `E` (`Rotor Thrust T\n& Reactive Torque Q`) contain raw unquoted ampersands `&`, causing parser warnings in strict renderers.
   * **Remedy:** Enclose labels in explicit double quotes: `B["Power Distribution<br/>Board & ESCs"]`.

4. **Empty Code Fence in Topic 5 Prototype:**
   * **Location:** `topic_5_flight_ctrl_2.md`, Lines 457–460.
   * **Defect:** Empty code fence without language specification.
   * **Remedy:** Remove empty code fence.

---

## 7. Recommended Action Plan for Orchestrator & Implementing Agents

1. **Topic 1 (`topic_1_uav_architectures.md`):**
   * Insert Widget 1 iframe snippet and fallback link at Section 6.5 (Line 243).
   * Fix unquoted `&` in Diagram #7.
2. **Topic 2 (`topic_2_coordinate_frames.md`):**
   * Replace static KaTeX box in Section 10 (Line 941) with Widget 2 iframe snippet and fallback link.
3. **Topic 3 (`topic_3_kinematics_dynamics.md`):**
   * Insert Widget 3 iframe snippet and fallback link in Section 11 (Line 684) directly above Guided Interactive Experiments.
4. **Topic 4 (`topic_4_forces_moments.md`):**
   * Remove lines 570–634 (Python code dump).
   * Insert Widget 4 iframe snippet and fallback link in Section 4.7.
   * Remove misplaced tip box from Section 4.8.4 (Line 706).
5. **Topic 5 (`topic_5_flight_control.md`):**
   * Insert Widget 5 iframe snippet and fallback link in Section 3.2 (Line 205).
6. **Execution of Automated Verification:**
   * Run verification script across all files to assert 0 code blocks, 5 valid iframes, 100% valid Mermaid diagrams, and 100% KaTeX delimiter balance.
