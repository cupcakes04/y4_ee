# Pedagogical Architecture & Generative UI Widgets Blueprint (Topics 1 to 5)

**Document:** EEEE4138 Aerial Robotics — Survey & Architectural Specification  
**Author:** Explorer 3 (Generative UI Widgets & Pedagogical Architecture Explorer)  
**Target Delivery Path:** `d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_3\handoff.md`  
**Date:** 2026-11-12  
**Scope:** Topics 1 through 5 (Topic 6 Trajectory Generation deferred per User Directive `2026-11-12T02:58:57Z`)

---

## 1. Observations

### 1.1 Source Material & Curriculum Baseline
* **Original Request & Acceptance Criteria (`ORIGINAL_REQUEST.md`, lines 16–51):** Mandates comprehensive topic synthesis, student gap-bridging with prerequisite anchors ($F=ma$, $1/Js^2$, Laplace transfer functions, eigenvalues), explicit intermediate algebraic derivations without leaps, standardized API contract tables (Inputs, Outputs, Assumptions/Invariants, Downstream Blocks), bidirectional cross-referencing, and self-contained interactive Generative UI widgets using HTML5 + Tailwind CSS + Canvas/SVG with zero external runtime dependencies.
* **Scope Amendment Directive (`DISPATCH.md`, timestamp 2026-11-12T02:58:57Z):** *"USER DIRECTIVE: Topic 6 (Trajectory Generation) is put aside for now. Please focus your pedagogical architecture and interactive Generative UI widgets fully on Topics 1 through 5 (Widgets 1 through 5, cross-references across Topics 1 to 5)."*
* **Prototype Note Analysis (`chapters/topic_5_flight_ctrl_2.md`):** Demonstrates high technical rigor in KaTeX formatting, ASCII signal flow architecture (outer loop position, inner loop attitude, control allocation), hover linearization ($\ddot{x} \approx -g\theta, \ddot{z} \approx -\delta T/m$), and state-space controllability proofs ($\det(\mathcal{C}) = (g/J_y)^2$).
* **Primary Source Lecture Decks (`modules/EEEE4138_aerial_robotics/raw/`):**
  * `Topic 1 Introduction (Parts 1 & 2)`: 65 pages covering UAV classifications, 4 forces of flight, multirotor geometries (+ vs $\times$, hexarotor, octorotor), disc loading, battery discharge characteristics, and ESC motor drives.
  * `Topic 2 Reference Frames (Parts 1 & 2)`: 54 pages establishing inertial NED frame $\mathcal{F}_i$, vehicle frames $\mathcal{F}_v, \mathcal{F}_{v1}, \mathcal{F}_{v2}$, body FRD frame $\mathcal{F}_b$, ZYX Euler rotation matrices, kinematic mapping matrices $W_\eta$, gimbal lock singularity at $\theta = \pm 90^\circ$, and quaternion algebra.
  * `Topic 3 Kinematics and Dynamics`: 42 pages deriving Coriolis derivatives in rotating frames ($\dot{\mathbf{v}}_I = \dot{\mathbf{v}}_B + \boldsymbol{\omega} \times \mathbf{v}_B$), body-axis accelerations, principal-axis Newton-Euler rotational equations ($J\dot{\boldsymbol{\omega}} + \boldsymbol{\omega}\times(J\boldsymbol{\omega}) = \boldsymbol{\tau}$), and rotor gyroscopic precession.
  * `Topic 4 Forces and Moments`: 50 pages covering blade element / momentum theory ($T_i = k_t \Omega_i^2, Q_i = k_q \Omega_i^2$), alternating rotor spin directions for torque cancellation, $+$ and $\times$ quadrotor mixer matrices, hexarotor pseudo-inverses, actuator saturation, and motor first-order time lag.
  * `Topic 5 Flight Control I & II`: 85 pages deriving vertical hover equilibrium, PD/PID height and position control, timescale separation ($\omega_n^{att} \gg \omega_n^{pos}$), hover linearization, 4-state longitudinal state-space modeling, controllability matrix rank, pole placement, and LQR optimal feedback design.
* **Tutorial Drills (`modules/EEEE4138_aerial_robotics/drills/` Tutorials 1–5):** Demand exact calculations of rotation sequences, Coriolis cross-terms, mixer matrix inversions, motor speed allocation, closed-loop pole locations, and LQR gain matrices.

---

## 2. Logic Chain

1. **Student Cognitive Load & Pedagogical Gap Analysis:**
   * Students transitioning from 2nd/3rd-year classical control (single-input single-output $1/Js^2$, scalar $F=ma$, root locus) to aerial robotics experience severe cognitive dissonance when confronted with coupled multi-input multi-output (MIMO) 6-DoF systems, non-commutative 3D rotation groups $SO(3)$, and underactuation.
   * *Resolution:* Every topic must begin with an explicit **Prerequisite Anchor** that grounds the new concept in familiar undergraduate theory before introducing 3D extensions.
2. **Intermediate Derivations without Unexplained Leaps:**
   * Textbooks routinely skip intermediate matrix multiplications or state "it can be shown that $\ddot{x} = -g\theta$". This causes sign confusion (NED vs NWU frames) and hides critical assumptions (e.g., small-angle approximations, decoupling of second-order perturbations $\delta T \cdot \theta \approx 0$).
   * *Resolution:* All derivations must show every intermediate step, sign verification, and trigonometric substitution.
3. **API Contract Standardization:**
   * Flight software (e.g., PX4, ArduPilot, ROS 2 Autoware) is structured into modular microservices. Treating textbook chapters as formal API interfaces with typed inputs, outputs, invariants, and downstream consumers enforces systems-engineering rigor.
4. **Interactive Generative UI Widgets (Zero External Dependencies):**
   * Abstract dynamics like gyroscopic precession, gimbal lock, control allocation under motor failure, and cascaded timescale separation cannot be internalized through static 2D figures alone.
   * Real-time interactive simulators running in modern browsers (using standard HTML5 Canvas 2D/3D projection, vanilla JavaScript numerical solvers, and Tailwind CSS via CDN) provide immediate tactile reinforcement. Zero external dependencies guarantee offline usability, zero build-step friction, and permanent reproducibility.

---

## 3. Pedagogical Architecture Blueprint (Topics 1 to 5)

### 3.1 Prerequisite Anchors: Connecting Fundamentals to Aerial Robotics

| Topic | Undergraduate Prerequisite Anchor | Mathematical Concept Bridged | Common Student Stumbling Block | Pedagogical Bridge Mechanism |
|---|---|---|---|---|
| **Topic 1: Architectures & Envelopes** | Fluid Mechanics (Momentum conservation $\dot{m} \Delta v$), Electrical circuits ($P=VI, E=Pt$) | Actuator disc momentum theory, specific energy scaling, thrust-to-weight ratio ($TWR$) | Believing infinite battery capacity yields infinite flight time; ignoring battery mass scaling | Derive the nonlinear endurance curve: $m = m_{dry} + m_{bat}$; show diminishing returns as $m_{bat} \to \infty$ due to $P_h \propto m^{3/2}$. |
| **Topic 2: Coordinate Frames & Kinematics** | 2D Rotation matrices $\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}$, Vector dot/cross products | 3D Direction Cosine Matrices $R \in SO(3)$, ZYX Euler angles, Euler rate mapping $W_\eta$, Quaternions | Confusing passive change-of-basis $R_B^I$ with active vector rotation; sign errors in NED vs Cartesian $z$-down | Step-by-step vector projection; prove $R^{-1} = R^T$; visually demonstrate how $\theta = 90^\circ$ causes roll and yaw axes to align (Gimbal Lock). |
| **Topic 3: 6-DoF Dynamics & Newton-Euler** | Particle dynamics $F=ma$, Single-axis rotational dynamics $\tau = J \ddot{\theta}$ (plant $1/Js^2$) | Transport Theorem (Coriolis cross-terms $\boldsymbol{\omega} \times \mathbf{v}$), Euler's rotational equations $J\dot{\boldsymbol{\omega}} + \boldsymbol{\omega}\times(J\boldsymbol{\omega}) = \boldsymbol{\tau}$ | Expecting 3D rotation to decouple into three independent $J_i \ddot{\theta}_i = \tau_i$ equations; overlooking gyroscopic precession | Expand $\boldsymbol{\omega}\times(J\boldsymbol{\omega})$ term-by-term; show how spinning rotors inject gyroscopic cross-coupling torque $\tau_{gyro} = \boldsymbol{\omega}\times \mathbf{h}_{rotors}$. |
| **Topic 4: Forces, Moments & Allocation** | Linear algebra systems $A\mathbf{x} = \mathbf{b}$, Matrix inversion, Newton's 3rd Law (torque reaction) | Aerodynamic scaling $T = k_t \Omega^2, Q = k_q \Omega^2$, Mixer matrix geometry, Moore-Penrose pseudo-inverse $M^\dagger$ | Not understanding why CW/CCW rotor pairing cancels yaw; confusion over $+$ vs $\times$ arm geometry | Derive moment arms $L$ and $L/\sqrt{2}$ explicitly; demonstrate pseudo-inverse allocation for over-actuated hexarotors under motor failure. |
| **Topic 5: Flight Control Architectures** | Classical control: standard second-order systems $s^2 + 2\zeta\omega_n s + \omega_n^2$, PID tuning, State-space $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$ | Timescale separation theorem, small-angle hover linearization, controllability rank, LQR optimal state-feedback | Attempting to tune position and attitude loops at identical bandwidths, causing catastrophic instability | Prove why the inner attitude loop must be $5\times\text{--}10\times$ faster than outer position loop; derive hover linearization step-by-step. |

---

### 3.2 Step-by-Step Intermediate Algebraic Proof Steps (Zero Unexplained Leaps)

#### Derivation 1: Actuator Disc Momentum Theory & Hover Power (Topic 1)
* **Goal:** Prove that hover induced power scales as $P_i = \frac{T^{3/2}}{\sqrt{2\rho A}}$.
1. *Conservation of Mass:* Incompressible air mass flow rate across rotor disc of area $A = \pi R^2$ with induced velocity $v_i$:
   $$\dot{m} = \rho A v_i$$
2. *Conservation of Linear Momentum:* Thrust $T$ equals rate of momentum change from far upstream ($v_\infty = 0$) to far wake slipstream ($v_w$):
   $$T = \dot{m}(v_w - 0) = \rho A v_i v_w$$
3. *Conservation of Kinetic Energy:* Work done by thrust per unit time equals kinetic energy imparted to slipstream:
   $$P = T v_i = \frac{1}{2}\dot{m}(v_w^2 - 0^2) = \frac{1}{2}(\rho A v_i) v_w^2$$
4. *Wake Velocity Relation:* Substitute $T = \rho A v_i v_w$ into the energy equation:
   $$(\rho A v_i v_w) v_i = \frac{1}{2}\rho A v_i v_w^2 \implies v_w = 2 v_i$$
5. *Induced Velocity in Hover:* Substitute $v_w = 2 v_i$ back into momentum equation:
   $$T = \rho A v_i (2 v_i) = 2 \rho A v_i^2 \implies \boxed{v_i = \sqrt{\frac{T}{2\rho A}}}$$
6. *Hover Induced Power:*
   $$\boxed{P_i = T v_i = T \sqrt{\frac{T}{2\rho A}} = \frac{T^{3/2}}{\sqrt{2\rho A}}}$$

#### Derivation 2: Direction Cosine Matrix $R_B^I$ ZYX Expansion & Inversion (Topic 2)
* **Goal:** Expand $R_B^I = R_z(\psi) R_y(\theta) R_x(\phi)$ explicitly and show orthogonality $R^{-1} = R^T$.
1. Elementary principal axis rotation matrices:
   $$R_z(\psi) = \begin{bmatrix} \cos\psi & -\sin\psi & 0 \\ \sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix}, \quad R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}, \quad R_x(\phi) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\phi & -\sin\phi \\ 0 & \sin\phi & \cos\phi \end{bmatrix}$$
2. Intermediate product $R_{zy} = R_z(\psi) R_y(\theta)$:
   $$R_{zy} = \begin{bmatrix} \cos\psi\cos\theta & -\sin\psi & \cos\psi\sin\theta \\ \sin\psi\cos\theta & \cos\psi & \sin\psi\sin\theta \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}$$
3. Final product $R_B^I = R_{zy} R_x(\phi)$:
   $$R_B^I = \begin{bmatrix} 
   \cos\psi\cos\theta & \cos\psi\sin\theta\sin\phi - \sin\psi\cos\phi & \cos\psi\sin\theta\cos\phi + \sin\psi\sin\phi \\
   \sin\psi\cos\theta & \sin\psi\sin\theta\sin\phi + \cos\psi\cos\phi & \sin\psi\sin\theta\cos\phi - \cos\psi\sin\phi \\
   -\sin\theta & \cos\theta\sin\phi & \cos\theta\cos\phi
   \end{bmatrix}$$
4. *Proof of Orthogonality:* Since each elementary matrix satisfies $R_i^T R_i = I$, by the matrix product transpose property:
   $$(R_z R_y R_x)^T (R_z R_y R_x) = R_x^T R_y^T R_z^T R_z R_y R_x = R_x^T R_y^T I R_y R_x = R_x^T I R_x = I \implies \boxed{(R_B^I)^{-1} = (R_B^I)^T = R_I^B}$$

#### Derivation 3: Angular Velocity Kinematic Inversion & Gimbal Lock Singularity (Topic 2)
* **Goal:** Prove the singularity in mapping body rates $[p, q, r]^T$ to Euler rates $[\dot{\phi}, \dot{\theta}, \dot{\psi}]^T$.
1. Angular velocity vector in body frame as sum of three non-orthogonal rotations:
   $$\boldsymbol{\omega}_b = \begin{bmatrix} p \\ q \\ r \end{bmatrix} = \begin{bmatrix} \dot{\phi} \\ 0 \\ 0 \end{bmatrix} + R_x^T(\phi)\begin{bmatrix} 0 \\ \dot{\theta} \\ 0 \end{bmatrix} + R_x^T(\phi) R_y^T(\theta)\begin{bmatrix} 0 \\ 0 \\ \dot{\psi} \end{bmatrix}$$
2. Expanding the rotation products:
   $$\begin{bmatrix} p \\ q \\ r \end{bmatrix} = \begin{bmatrix} 1 & 0 & -\sin\theta \\ 0 & \cos\phi & \sin\phi\cos\theta \\ 0 & -\sin\phi & \cos\phi\cos\theta \end{bmatrix} \begin{bmatrix} \dot{\phi} \\ \dot{\theta} \\ \dot{\psi} \end{bmatrix} = M_{\omega}(\boldsymbol{\eta}) \dot{\boldsymbol{\eta}}$$
3. Inverting $M_{\omega}(\boldsymbol{\eta})$ using Cramer's rule / cofactors:
   $$\det(M_{\omega}) = 1 \cdot (\cos^2\phi\cos\theta + \sin^2\phi\cos\theta) - \sin\theta(0) = \cos\theta$$
4. Computing the inverse matrix $W_\eta = M_{\omega}^{-1}$:
   $$\boxed{\begin{bmatrix} \dot{\phi} \\ \dot{\theta} \\ \dot{\psi} \end{bmatrix} = \begin{bmatrix} 1 & \sin\phi\tan\theta & \cos\phi\tan\theta \\ 0 & \cos\phi & -\sin\phi \\ 0 & \sin\phi/\cos\theta & \cos\phi/\cos\theta \end{bmatrix} \begin{bmatrix} p \\ q \\ r \end{bmatrix}}}$$
5. *Gimbal Lock Singularity:* When $\theta \to \pm \frac{\pi}{2}$ ($\pm 90^\circ$ pitch up/down):
   $$\cos\theta \to 0 \implies \tan\theta \to \pm\infty, \quad \sec\theta \to \pm\infty$$
   $\dot{\phi}$ and $\dot{\psi}$ become linearly dependent ($p$ and $r$ project onto the same physical axis), causing numerical divergence and loss of one rotational degree of freedom.

#### Derivation 4: Euler's Rotational Equations & Gyroscopic Cross-Coupling (Topic 3)
* **Goal:** Derive the exact angular acceleration equations for a quadrotor with symmetric diagonal inertia $J = \text{diag}(J_x, J_y, J_z)$ and rotor gyroscopic torques.
1. Angular momentum of airframe: $\mathbf{H}_b = J \boldsymbol{\omega}_b = [J_x p, J_y q, J_z r]^T$.
2. Transport theorem in rotating body frame: $\dot{\mathbf{H}}_I = \dot{\mathbf{H}}_b + \boldsymbol{\omega}_b \times \mathbf{H}_b = \boldsymbol{\tau}_{net}$.
3. Cross-product expansion:
   $$\boldsymbol{\omega}_b \times (J \boldsymbol{\omega}_b) = \begin{bmatrix} p \\ q \\ r \end{bmatrix} \times \begin{bmatrix} J_x p \\ J_y q \\ J_z r \end{bmatrix} = \begin{bmatrix} q(J_z r) - r(J_y q) \\ r(J_x p) - p(J_z r) \\ p(J_y q) - q(J_x p) \end{bmatrix} = \begin{bmatrix} (J_z - J_y) q r \\ (J_x - J_z) p r \\ (J_y - J_x) p q \end{bmatrix}$$
4. Spinning rotor angular momentum: Each rotor $i$ spinning at $\Omega_i$ around $+z_b$ with rotor inertia $J_r$ possesses angular momentum $\mathbf{h}_{r,i} = [0, 0, (-1)^i J_r \Omega_i]^T$.
5. Rotor gyroscopic reaction torque on airframe:
   $$\boldsymbol{\tau}_{gyro} = \sum_{i=1}^4 \boldsymbol{\omega}_b \times \mathbf{h}_{r,i} = \boldsymbol{\omega}_b \times \begin{bmatrix} 0 \\ 0 \\ J_r \Omega_{net} \end{bmatrix} = \begin{bmatrix} p \\ q \\ r \end{bmatrix} \times \begin{bmatrix} 0 \\ 0 \\ J_r \Omega_{net} \end{bmatrix} = \begin{bmatrix} q J_r \Omega_{net} \\ -p J_r \Omega_{net} \\ 0 \end{bmatrix}$$
   where $\Omega_{net} = -\Omega_1 + \Omega_2 - \Omega_3 + \Omega_4$.
6. Component equations of motion:
   $$\boxed{\dot{p} = \frac{1}{J_x}\left[ \tau_\phi - (J_z - J_y) q r - q J_r \Omega_{net} \right]}$$
   $$\boxed{\dot{q} = \frac{1}{J_y}\left[ \tau_\theta - (J_x - J_z) p r + p J_r \Omega_{net} \right]}$$
   $$\boxed{\dot{r} = \frac{1}{J_z}\left[ \tau_\psi - (J_y - J_x) p q \right]}$$

#### Derivation 5: Mixer Allocation Matrix Inversion for $\times$-Configuration (Topic 4)
* **Goal:** Derive and invert the mixer matrix $M_\times$ mapping rotor speeds to virtual forces/torques.
1. Geometry: 4 motors located at radius $L$ at angles $45^\circ, 135^\circ, 225^\circ, 315^\circ$ from $+x_b$ (forward):
   * Motor 1 (Front-Right, CCW): $x_1 = L/\sqrt{2}, y_1 = L/\sqrt{2}$
   * Motor 2 (Rear-Right, CW): $x_2 = -L/\sqrt{2}, y_2 = L/\sqrt{2}$
   * Motor 3 (Rear-Left, CCW): $x_3 = -L/\sqrt{2}, y_3 = -L/\sqrt{2}$
   * Motor 4 (Front-Left, CW): $x_4 = L/\sqrt{2}, y_4 = -L/\sqrt{2}$
2. Let $d = \frac{L}{\sqrt{2}}$. Formulate forces and torques:
   * Total Thrust: $T = k_t(\Omega_1^2 + \Omega_2^2 + \Omega_3^2 + \Omega_4^2)$
   * Roll Moment ($\tau_\phi = \sum y_i T_i$): $\tau_\phi = d k_t (-\Omega_1^2 - \Omega_2^2 + \Omega_3^2 + \Omega_4^2)$
   * Pitch Moment ($\tau_\theta = \sum -x_i T_i$): $\tau_\theta = d k_t (-\Omega_1^2 + \Omega_2^2 + \Omega_3^2 - \Omega_4^2)$
   * Yaw Moment ($\tau_\psi = \sum (-1)^i Q_i$): $\tau_\psi = k_q (\Omega_1^2 - \Omega_2^2 + \Omega_3^2 - \Omega_4^2)$
3. Matrix representation $\mathbf{u} = M_\times \mathbf{\Omega}^2$:
   $$M_\times = \begin{bmatrix} k_t & k_t & k_t & k_t \\ -d k_t & -d k_t & d k_t & d k_t \\ -d k_t & d k_t & d k_t & -d k_t \\ k_q & -k_q & k_q & -k_q \end{bmatrix}$$
4. Algebraic Inversion of $M_\times$:
   Notice that rows of $M_\times$ are mutually orthogonal! Therefore:
   $$\boxed{\begin{bmatrix} \Omega_1^2 \\ \Omega_2^2 \\ \Omega_3^2 \\ \Omega_4^2 \end{bmatrix} = \begin{bmatrix} 
   \frac{1}{4 k_t} & -\frac{1}{4 d k_t} & -\frac{1}{4 d k_t} & \frac{1}{4 k_q} \\
   \frac{1}{4 k_t} & -\frac{1}{4 d k_t} & \frac{1}{4 d k_t} & -\frac{1}{4 k_q} \\
   \frac{1}{4 k_t} & \frac{1}{4 d k_t} & \frac{1}{4 d k_t} & \frac{1}{4 k_q} \\
   \frac{1}{4 k_t} & \frac{1}{4 d k_t} & -\frac{1}{4 d k_t} & -\frac{1}{4 k_q}
   \end{bmatrix} \begin{bmatrix} T \\ \tau_\phi \\ \tau_\theta \\ \tau_\psi \end{bmatrix}}}$$

#### Derivation 6: Hover Linearization, Decoupling & Controllability Proof (Topic 5)
* **Goal:** Prove small-angle decoupling around hover and evaluate controllability matrix rank.
1. Nonlinear translational equations in NED:
   $$\ddot{x} = -\frac{T}{m}(\cos\psi\sin\theta\cos\phi + \sin\psi\sin\phi)$$
   $$\ddot{y} = -\frac{T}{m}(\sin\psi\sin\theta\cos\phi - \cos\psi\sin\phi)$$
   $$\ddot{z} = g - \frac{T}{m}(\cos\theta\cos\phi)$$
2. Hover equilibrium: $x_0 = y_0 = z_0 = 0$, $\psi_0 = 0, \theta_0 = 0, \phi_0 = 0$, $T_0 = mg$.
3. Perturbations: $T = mg + \delta T, \theta \ll 1, \phi \ll 1, \psi = 0$.
   Using first-order Taylor expansions ($\sin\alpha \approx \alpha, \cos\alpha \approx 1$):
   * $\ddot{x} = -\frac{mg + \delta T}{m} (\theta) = -g\theta - \frac{\delta T\theta}{m} \approx \boxed{-g\theta}$
   * $\ddot{y} = -\frac{mg + \delta T}{m} (-\phi) = g\phi + \frac{\delta T\phi}{m} \approx \boxed{g\phi}$
   * $\ddot{z} = g - \frac{mg + \delta T}{m}(1) = \boxed{-\frac{\delta T}{m}}$
4. Longitudinal State-Space Model ($x_1 = x, x_2 = \dot{x}, x_3 = \theta, x_4 = q$):
   $$\dot{\mathbf{x}} = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & -g & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \end{bmatrix} \mathbf{x} + \begin{bmatrix} 0 \\ 0 \\ 0 \\ 1/J_y \end{bmatrix} M_y$$
5. Controllability Matrix $\mathcal{C} = [B \quad AB \quad A^2 B \quad A^3 B]$:
   * $B = \begin{bmatrix} 0 & 0 & 0 & 1/J_y \end{bmatrix}^T$
   * $AB = \begin{bmatrix} 0 & 0 & 1/J_y & 0 \end{bmatrix}^T$
   * $A^2 B = A(AB) = \begin{bmatrix} 0 & -g/J_y & 0 & 0 \end{bmatrix}^T$
   * $A^3 B = A(A^2 B) = \begin{bmatrix} -g/J_y & 0 & 0 & 0 \end{bmatrix}^T$
6. Determinant of $\mathcal{C}$:
   $$\mathcal{C} = \begin{bmatrix} 0 & 0 & 0 & -g/J_y \\ 0 & 0 & -g/J_y & 0 \\ 0 & 1/J_y & 0 & 0 \\ 1/J_y & 0 & 0 & 0 \end{bmatrix} \implies \det(\mathcal{C}) = \left(\frac{g}{J_y^2}\right)^2 = \frac{g^2}{J_y^4} \ne 0$$
   Since $\det(\mathcal{C}) \ne 0$, $\text{rank}(\mathcal{C}) = 4 = n$. **The system is fully controllable!**

---

### 3.3 Standardized API Contract Tables (Topics 1 to 5)

#### Topic 1 API Contract: Multi-Rotor Configuration & Flight Envelopes
| Direction | Parameter / Variable | Symbol | Units | Type / Dim | Physical Meaning | Source / Consumer Block |
|---|---|---|---|---|---|---|
| **Input** | Airframe Topology | `topol` | - | String enum | `quad_plus`, `quad_x`, `hex_x`, `octo_x` | User specification / CAD |
| **Input** | Arm Radius | $L$ | $\text{m}$ | $\mathbb{R}^+$ | Distance from center of mass to rotor hub | Structural geometry |
| **Input** | Dry & Battery Mass | $m_{dry}, m_{bat}$ | $\text{kg}$ | $\mathbb{R}^+$ | Structural airframe mass and battery pack mass | Mass balance |
| **Input** | Battery Specific Energy | $e_{bat}$ | $\text{Wh/kg}$ | $\mathbb{R}^+$ | Gravimetric energy density of LiPo / Li-ion | Battery datasheet |
| **Input** | Propeller Diameter | $D$ | $\text{m}$ | $\mathbb{R}^+$ | Rotor blade diameter | Propeller specs |
| **Output** | Total Mass & Inertia | $m, J$ | $\text{kg}, \text{kg}\cdot\text{m}^2$ | $\mathbb{R}^+, \mathbb{R}^{3\times 3}$ | Rigid body mass and diagonal moment of inertia tensor | $\to$ Topic 3 (Rigid Body Dynamics) |
| **Output** | Hover Operating Point | $T_0, \Omega_0$ | $\text{N}, \text{rad/s}$ | $\mathbb{R}^+$ | Baseline hover thrust and motor equilibrium angular speed | $\to$ Topic 4 (Rotor Allocation), Topic 5 (Control) |
| **Output** | Flight Envelope Limits | $v_{max}, \theta_{max}$ | $\text{m/s}, \text{rad}$ | $\mathbb{R}^+$ | Safe forward speed and maximum allowable bank/pitch angle | $\to$ Topic 5 (Trajectory tracking limits) |
| **Invariants** | Hover Equilibrium | $T_{total} = mg$ | $\text{N}$ | Equation | Total vertical rotor thrust must equal aircraft weight at hover | Maintained across all valid configurations |
| **Failures** | Insufficient Thrust | $TWR < 1.2$ | - | Boolean | Aircraft cannot hover safely or reject downward wind gusts | Triggers design abort / config warning |

#### Topic 2 API Contract: Coordinate Frames & Attitude Kinematics
| Direction | Parameter / Variable | Symbol | Units | Type / Dim | Physical Meaning | Source / Consumer Block |
|---|---|---|---|---|---|---|
| **Input** | Euler Angles (ZYX) | $\boldsymbol{\eta} = [\phi, \theta, \psi]^T$ | $\text{rad}$ | $\mathbb{R}^3$ | Roll, Pitch, and Yaw angles relative to NED frame | IMU / State Estimator |
| **Input** | Body Angular Rates | $\boldsymbol{\omega}_b = [p, q, r]^T$ | $\text{rad/s}$ | $\mathbb{R}^3$ | Angular rate vector measured along body axes | Gyroscope sensor |
| **Input** | Unit Quaternion | $\mathbf{q} = [q_w, q_x, q_y, q_z]^T$ | - | $\mathbb{R}^4, \|\mathbf{q}\|=1$ | Singularity-free attitude representation | AHRS filter |
| **Output** | Direction Cosine Matrix | $R_B^I$ | - | $SO(3), \mathbb{R}^{3\times 3}$ | Orthonormal frame transformation from Body to Inertial | $\to$ Topic 3 (Gravity projection, thrust rotation) |
| **Output** | Euler Angle Rates | $\dot{\boldsymbol{\eta}} = [\dot{\phi}, \dot{\theta}, \dot{\psi}]^T$ | $\text{rad/s}$ | $\mathbb{R}^3$ | Rate of change of Euler angles ($W_\eta \boldsymbol{\omega}_b$) | $\to$ Topic 5 (Attitude error derivative) |
| **Output** | Quaternion Derivative | $\dot{\mathbf{q}}$ | $\text{s}^{-1}$ | $\mathbb{R}^4$ | Kinematic derivative ($\frac{1}{2} \mathbf{q} \otimes \bar{\boldsymbol{\omega}}$) | $\to$ Topic 3 (Kinematic integration) |
| **Invariants** | Orthonormality & Unit Norm | $R^T R = I, \|\mathbf{q}\|=1$ | - | Equations | Rotation matrix must have determinant $+1$; quaternion norm $= 1$ | Maintained at every numerical step |
| **Failures** | Gimbal Lock Hazard | $|\theta| \ge 85^\circ$ | $\text{rad}$ | Boolean | Pitch approaches $\pm 90^\circ$, causing $W_\eta$ denominator to vanish | Switches controller to Quaternion mode |

#### Topic 3 API Contract: 6-DoF Rigid-Body Dynamics
| Direction | Parameter / Variable | Symbol | Units | Type / Dim | Physical Meaning | Source / Consumer Block |
|---|---|---|---|---|---|---|
| **Input** | Net Collective Thrust | $T$ | $\text{N}$ | $\mathbb{R}^+$ | Total aerodynamic thrust vector $\mathbf{f}_b = [0, 0, -T]^T$ | Topic 4 (Rotor Allocation) |
| **Input** | Body Control Torques | $\boldsymbol{\tau}_b = [\tau_\phi, \tau_\theta, \tau_\psi]^T$ | $\text{N}\cdot\text{m}$ | $\mathbb{R}^3$ | Differential moments produced by rotors | Topic 4 (Rotor Allocation) |
| **Input** | Wind Disturbances | $\mathbf{f}_w, \boldsymbol{\tau}_w$ | $\text{N}, \text{N}\cdot\text{m}$ | $\mathbb{R}^3, \mathbb{R}^3$ | Environmental aerodynamic force and moment disturbances | Wind field model |
| **Output** | Inertial Acceleration | $\ddot{\mathbf{p}}_I = [\ddot{x}, \ddot{y}, \ddot{z}]^T$ | $\text{m/s}^2$ | $\mathbb{R}^3$ | Linear acceleration in North-East-Down frame | $\to$ Numerical Integrator / GPS filter |
| **Output** | Angular Acceleration | $\dot{\boldsymbol{\omega}}_b = [\dot{p}, \dot{q}, \dot{r}]^T$ | $\text{rad/s}^2$ | $\mathbb{R}^3$ | Rotational acceleration around body principal axes | $\to$ Numerical Integrator / Gyro model |
| **Output** | Full State Vector | $\mathbf{x}_{12}$ | mixed | $\mathbb{R}^{12}$ | $[x, y, z, u, v, w, \phi, \theta, \psi, p, q, r]^T$ | $\to$ Topic 5 (Full State Feedback) |
| **Invariants** | Conservation of Momentum | $\frac{d}{dt}\mathbf{P} = \sum \mathbf{F}$ | - | Equation | Linear and angular momentum satisfy Newton-Euler equations | Validated against energy balance |
| **Failures** | Angular Divergence | $\|\boldsymbol{\omega}_b\| > 25\text{ rad/s}$ | $\text{rad/s}$ | Boolean | Tumbling / loss of attitude control | Triggers emergency motor cut / parachute |

#### Topic 4 API Contract: Forces, Moments & Rotor Allocation
| Direction | Parameter / Variable | Symbol | Units | Type / Dim | Physical Meaning | Source / Consumer Block |
|---|---|---|---|---|---|---|
| **Input** | Virtual Control Demands | $\mathbf{u}_{cmd} = [T^d, \tau_\phi^d, \tau_\theta^d, \tau_\psi^d]^T$ | $\text{N}, \text{N}\cdot\text{m}$ | $\mathbb{R}^4$ | Commanded total thrust and 3-axis moments | Topic 5 (Flight Controller) |
| **Input** | Actuator Health Status | $\mathbf{s}_{health}$ | - | $\{0, 1\}^N$ | Motor operational mask ($1 = \text{healthy}, 0 = \text{failed}$) | Health & Usage Monitoring (HUMS) |
| **Output** | Motor Speed Commands | $\Omega_{cmd,i}$ | $\text{rad/s}$ | $\mathbb{R}^N$ | Individual rotor angular velocity commands | $\to$ ESC PWM drivers |
| **Output** | Delivered Forces/Moments | $\mathbf{u}_{act} = [T, \boldsymbol{\tau}]^T$ | $\text{N}, \text{N}\cdot\text{m}$ | $\mathbb{R}^4$ | Realized wrench after motor lag and saturation clipping | $\to$ Topic 3 (Rigid Body Dynamics) |
| **Output** | Saturation Flags | $\mathbf{f}_{sat}$ | - | Boolean vector | Identifies which motors hit upper/lower RPM bounds | $\to$ Topic 5 (Anti-windup reset) |
| **Invariants** | Non-Negative Rotor Speed | $\Omega_i \ge 0$ | $\text{rad/s}$ | Inequality | Non-reversible ESCs cannot produce negative thrust | Enforced by clamp function |
| **Failures** | Rank Deficiency / Loss of Control | $\text{rank}(M_{active}) < 4$ | - | Boolean | Airframe cannot independently control 4 DoF (e.g. quad rotor failure) | Alerts flight controller to enter fail-safe |

#### Topic 5 API Contract: Cascaded Flight Control & State-Space Architecture
| Direction | Parameter / Variable | Symbol | Units | Type / Dim | Physical Meaning | Source / Consumer Block |
|---|---|---|---|---|---|---|
| **Input** | Reference Waypoint | $\mathbf{p}^d(t), \psi^d(t)$ | $\text{m}, \text{rad}$ | $\mathbb{R}^3, \mathbb{R}$ | Target position $[x^d, y^d, z^d]^T$ and desired heading | Trajectory Planner / Guidance |
| **Input** | State Estimate | $\hat{\mathbf{x}}$ | mixed | $\mathbb{R}^{12}$ | Estimated positions, velocities, attitudes, angular rates | Topic 2/3 (State Estimator / EKF) |
| **Input** | Controller Gains | $K_{pos}, K_{att}, Q, R$ | mixed | Matrices | PID gains or LQR state/control penalty weight matrices | Tuning engineer / Gain scheduler |
| **Output** | Virtual Demands | $\mathbf{u}_{cmd} = [T^d, \boldsymbol{\tau}^d]^T$ | $\text{N}, \text{N}\cdot\text{m}$ | $\mathbb{R}^4$ | Total thrust and attitude moment demands | $\to$ Topic 4 (Rotor Mixer / Allocation) |
| **Output** | Desired Tilt Angles | $\theta^d, \phi^d$ | $\text{rad}$ | $\mathbb{R}^2$ | Outer-loop generated attitude references | Inner-loop setpoints |
| **Invariants** | Timescale Separation | $\omega_{n,att} \ge 5 \omega_{n,pos}$ | $\text{rad/s}$ | Inequality | Inner attitude loop must settle before position loop responds | Stability invariant |
| **Failures** | Large Angle Linearization Breakdown | $|\theta| > 35^\circ \lor |\phi| > 35^\circ$ | $\text{rad}$ | Boolean | Tilt exceeds small-angle assumption ($\sin\theta \approx \theta$) | Switches to geometric SE(3) non-linear control |

---

### 3.4 Bidirectional Cross-Referencing Matrix & Dependency Graph

```
                              ┌───────────────────────────────────┐
                              │     TOPIC 1: UAV ARCHITECTURES    │
                              │  Geometry, Mass m, Inertia J,     │
                              │  Hover Thrust T₀, Flight Bounds   │
                              └──────┬─────────────────────▲──────┘
                                     │ (m, J, L)           │ (Attitude limits,
                                     ▼                     │  Power envelope)
                              ┌────────────────────────────┴──────┐
                              │     TOPIC 2: COORDINATE FRAMES    │
                              │  NED ↔ Body FRD, R_B^I, W_η, q,   │
                              │  Gimbal Lock Singularity          │
                              └──────┬─────────────────────▲──────┘
                                     │ (R_B^I, ω_b, η)     │ (Attitude kinematics,
                                     ▼                     │  Euler rate mapping)
                              ┌────────────────────────────┴──────┐
                              │     TOPIC 3: 6-DoF DYNAMICS       │
                              │  Newton-Euler, Coriolis ω×(Jω),   │
                              │  Gyroscopic Torques, 12-DoF ODE   │
                              └──────┬─────────────────────▲──────┘
                                     │ (Plant states x₁₂)  │ (Delivered wrench
                                     ▼                     │  [T, τ_b]ᵀ)
                              ┌────────────────────────────┴──────┐
                              │     TOPIC 4: FORCES & ALLOCATION  │
                              │  T_i = k_t Ωᵢ², Mixer Matrix M,   │
                              │  Pseudo-inverse M†, Saturation    │
                              └──────┬─────────────────────▲──────┘
                                     │ (Actuator limits,   │ (Demanded wrench
                                     ▼  Saturation flags)  │  u_cmd = [T, τ]ᵀ)
                              ┌────────────────────────────┴──────┐
                              │     TOPIC 5: FLIGHT CONTROL       │
                              │  Cascaded Loops, Hover Decouple,  │
                              │  State-Space, LQR, Integrator Aug │
                              └───────────────────────────────────┘
```

#### Detailed Bidirectional Cross-Reference Registry

1. **Topic 1 $\longleftrightarrow$ Topic 2:**
   * *Forward (1 $\to$ 2):* Physical placement of arms and sensors on the airframe establishes the Forward-Right-Down (FRD) body axes relative to the vehicle center of mass.
   * *Reverse (2 $\to$ 1):* Coordinate transformation $R_B^I$ determines the tilt angle $\theta, \phi$, establishing the effective vertical thrust $T\cos\theta\cos\phi \ge mg$ that dictates the horizontal flight speed boundary.
2. **Topic 2 $\longleftrightarrow$ Topic 3:**
   * *Forward (2 $\to$ 3):* Attitude rotation matrix $R_B^I$ projects inertial gravity into body coordinates ($R_I^B \mathbf{g}^I$) and projects body thrust into inertial accelerations ($m \ddot{\mathbf{p}}_I = m \mathbf{g}^I + R_B^I \mathbf{f}_b$).
   * *Reverse (3 $\to$ 2):* Integration of body angular accelerations $\dot{\boldsymbol{\omega}}_b$ in Euler's equations yields body angular velocity $\boldsymbol{\omega}_b = [p, q, r]^T$, which feeds directly into kinematic equations $\dot{\boldsymbol{\eta}} = W_\eta \boldsymbol{\omega}_b$ and $\dot{\mathbf{q}} = \frac{1}{2}\mathbf{q}\otimes\bar{\boldsymbol{\omega}}$.
3. **Topic 3 $\longleftrightarrow$ Topic 4:**
   * *Forward (3 $\to$ 4):* Dynamic body rates $\boldsymbol{\omega}_b$ and rotor spin speeds $\Omega_i$ generate gyroscopic cross-coupling torque $\boldsymbol{\tau}_{gyro}$, which the allocation mixer must compensate for.
   * *Reverse (4 $\to$ 3):* Control allocation matrix $M$ maps motor speeds $[\Omega_1^2, \dots, \Omega_N^2]^T$ into the net thrust $T$ and moments $\boldsymbol{\tau}_b$ that drive the Newton-Euler equations of motion.
4. **Topic 4 $\longleftrightarrow$ Topic 5:**
   * *Forward (4 $\to$ 5):* Actuator physical limits ($\Omega_{min}, \Omega_{max}$) and motor time constant $\tau_m$ determine maximum control bandwidth and enforce anti-windup clamping on controller integrators.
   * *Reverse (5 $\to$ 4):* Outer-loop position and inner-loop attitude controllers output virtual generalized demands $[T^d, \tau_\phi^d, \tau_\theta^d, \tau_\psi^d]^T$, which serve as direct inputs to the mixer matrix.
5. **Topic 1 $\longleftrightarrow$ Topic 5:**
   * *Forward (1 $\to$ 5):* Baseline airframe mass $m$, arm length $L$, and hover thrust $T_0 = mg$ parameterize the linearized plant matrices $A, B$ in state-space and LQR designs.
   * *Reverse (5 $\to$ 1):* Closed-loop disturbance rejection bandwidth defines the safe operational wind envelope in which the multi-rotor can maintain station without control saturation.

---

## 4. Interactive Generative UI Widgets Blueprints (Widgets 1 to 5)

All widgets adhere to the following universal architectural standards:
* **Target Directory:** `modules/EEEE4138_aerial_robotics/widgets/`
* **Zero External Dependencies:** Built with pure HTML5, standard Canvas 2D/3D projection, SVG, and vanilla JavaScript. Uses official Tailwind CSS CDN `<script src="https://cdn.tailwindcss.com"></script>` for responsive styling.
* **Theme & UI Design:** Dark-mode engineering aesthetic (`bg-slate-950`, text in `slate-100`, accents in `cyan-400`, `emerald-400`, `amber-400`, and `rose-400`, monospace telemetry readouts in `font-mono text-xs`).
* **Frame Rate & Physics Loop:** Fixed 60 FPS requestAnimationFrame loop with sub-stepped numerical integration ($\Delta t = 1/240\text{ s}$ for stiff rotational dynamics).

---

### 4.1 Widget 1: Multi-Rotor Configuration & Flight Envelope Visualizer
* **Target File:** `modules/EEEE4138_aerial_robotics/widgets/widget_1_flight_envelope.html`
* **Pedagogical Objective:** Eliminates the misconception that battery capacity can be increased without bound to gain infinite endurance. Visually demonstrates disc loading ($DL = T/A$), power scaling ($P \propto T^{3/2}/\sqrt{A}$), and the nonlinear payload vs flight time tradeoff.

#### Technical Specifications & Layout
1. **Header & Preset Bar:**
   * Dropdown selector: Quad $+$, Quad $\times$, Hexarotor, Octorotor.
   * Presets: "Ultralight Racer" (TWR=4.5), "Photography Drone" (TWR=2.2), "Heavy-Lift Delivery" (TWR=1.6).
2. **Interactive Controls Panel (Left / Top):**
   * Arm Radius Slider $L$: $0.15\text{ m}$ to $0.80\text{ m}$ (Step: $0.01$)
   * Propeller Diameter Slider $D$: $5\text{ in}$ to $22\text{ in}$ (Step: $0.5$)
   * Battery Capacity Slider: $1000\text{ mAh}$ to $22000\text{ mAh}$ (Step: $200$)
   * Battery Cell Count Radio: $3S (11.1V), 4S (14.8V), 6S (22.2V)$
   * Payload Mass Slider: $0.0\text{ kg}$ to $5.0\text{ kg}$ (Step: $0.1$)
3. **Dual Visual Displays:**
   * **Left Canvas (Top-Down Airframe Schematic):** Renders animated rotating prop discs (green CW, red CCW), dimension lines for arm length $L$, center-of-mass indicator, and prop clearance checks (highlights disc overlap warning in amber if $2R > L\sqrt{2}$).
   * **Right Canvas (Flight Envelope & Endurance Curve):** Real-time 2D plot showing Flight Time (minutes) on vertical axis vs Battery Mass / Capacity on horizontal axis, plotting current operating point with an animated marker at the peak of efficiency.
4. **Telemetry HUD (Bottom Bar):**
   * Total All-Up Mass $m_{total}$ (kg)
   * Disc Loading $DL = T/A$ ($\text{kg/m}^2$ and $\text{N/m}^2$)
   * Hover Power Required $P_h$ (Watts)
   * Thrust-to-Weight Ratio ($TWR$) with color-coded safety badge ($<1.5$ Red, $1.5\text{--}2.5$ Green, $>2.5$ Cyan)
   * Estimated Hover Endurance (minutes:seconds)

#### Mathematical & Physics Equations
* Total mass: $m = m_{dry} + m_{payload} + m_{bat}$, where $m_{bat} = C_{mAh} \cdot V_{nom} \cdot \frac{1}{1000} \cdot \frac{1}{e_{bat}}$ with $e_{bat} \approx 180\text{ Wh/kg}$.
* Total disc area: $A_{tot} = N_{rotors} \cdot \pi (D/2)^2$.
* Hover thrust per rotor: $T_i = \frac{m g}{N_{rotors}}$.
* Induced hover velocity: $v_i = \sqrt{\frac{T_i}{2 \rho (\pi R^2)}}$.
* Induced hover power: $P_{induced} = N_{rotors} \cdot T_i v_i = \frac{(mg)^{3/2}}{\sqrt{2\rho A_{tot}}}$.
* Electrical power: $P_{elec} = \frac{P_{induced}}{\eta_{aero} \eta_{motor} \eta_{esc}} + P_{avionics}$, where $\eta_{combined} \approx 0.65$.
* Hover endurance: $t_{hover} = \frac{E_{battery\_usable}}{P_{elec}} = \frac{C_{Ah} \cdot V_{nom} \cdot 0.80 \times 60}{P_{elec}}$ (minutes, assuming 80% Depth of Discharge).

---

### 4.2 Widget 2: 3D Coordinate Frame & Gimbal Lock Simulator
* **Target File:** `modules/EEEE4138_aerial_robotics/widgets/widget_2_frames_gimbal_lock.html`
* **Pedagogical Objective:** Solves the difficult 3D spatial visualization hurdle of non-commutative rotations and demystifies why the Euler rate matrix $W_\eta$ blows up at $\theta = \pm 90^\circ$ while quaternions remain perfectly smooth and singularity-free.

#### Technical Specifications & Layout
1. **Interactive Controls Panel:**
   * Yaw Slider $\psi$: $-180^\circ$ to $+180^\circ$ (Step: $1^\circ$)
   * Pitch Slider $\theta$: $-90^\circ$ to $+90^\circ$ (Step: $0.5^\circ$) with "Snap to $90^\circ$" button
   * Roll Slider $\phi$: $-180^\circ$ to $+180^\circ$ (Step: $1^\circ$)
   * Rotation Sequence Toggle: ZYX (Aeronautical standard) vs ZYZ
   * Mouse Orbit Controls: Click and drag on canvas to rotate the 3D viewing perspective!
2. **Main 3D Canvas Display:**
   * Software-rendered 3D perspective projection on HTML5 Canvas (zero WebGL required).
   * Fixed Inertial Frame NED axes: $+X$ North (Red), $+Y$ East (Green), $+Z$ Down (Blue).
   * Moving Body Frame FRD axes: $+X_B$ Forward (Bright Red), $+Y_B$ Right (Bright Green), $+Z_B$ Down (Bright Blue).
   * Concentric 3D Gimbal Rings: Yaw Ring (outer), Pitch Ring (middle), Roll Ring (inner).
   * Airframe Model: 3D quadrotor mesh showing carbon fiber arms, central fuselage, and 4 colored rotors.
   * Gimbal Lock Indicator: When $|\theta| \to 90^\circ$, visual rings turn pulsing red, and the roll and yaw rotation planes visually merge into one single plane.
3. **Telemetry & Mathematical Readout Matrix:**
   * Direction Cosine Matrix $R_B^I$ ($3 \times 3$ grid with live numerical values).
   * Quaternion components $[q_w, q_x, q_y, q_z]^T$ showing norm $\equiv 1.000$.
   * Euler Rate Matrix Determinant: $\det(W_\eta^{-1}) = \cos\theta$. Live warning banner:
     *"GIMBAL LOCK DETECTED: $\cos\theta = 0$. $\dot{\phi}$ and $\dot{\psi}$ axes are collinear! Degree of freedom lost!"*

#### Mathematical & 3D Projection Engine
* 3D Point Transformation: $\mathbf{p}_I = R_B^I \mathbf{p}_B$.
* Camera View Projection:
  $$\begin{bmatrix} x_{cam} \\ y_{cam} \\ z_{cam} \end{bmatrix} = R_{cam} (\mathbf{p}_I - \mathbf{c}_{cam})$$
  $$x_{screen} = x_{center} + f \frac{x_{cam}}{z_{cam}}, \quad y_{screen} = y_{center} - f \frac{y_{cam}}{z_{cam}}$$
* Live Quaternion conversion:
  $$q_w = \cos\frac{\phi}{2}\cos\frac{\theta}{2}\cos\frac{\psi}{2} + \sin\frac{\phi}{2}\sin\frac{\theta}{2}\sin\frac{\psi}{2}$$
  $$q_x = \sin\frac{\phi}{2}\cos\frac{\theta}{2}\cos\frac{\psi}{2} - \cos\frac{\phi}{2}\sin\frac{\theta}{2}\sin\frac{\psi}{2}$$
  $$q_y = \cos\frac{\phi}{2}\sin\frac{\theta}{2}\cos\frac{\psi}{2} + \sin\frac{\phi}{2}\cos\frac{\theta}{2}\sin\frac{\psi}{2}$$
  $$q_z = \cos\frac{\phi}{2}\cos\frac{\theta}{2}\sin\frac{\psi}{2} - \sin\frac{\phi}{2}\sin\frac{\theta}{2}\cos\frac{\psi}{2}$$

---

### 4.3 Widget 3: 6-DoF Rigid Body Dynamics & Gyroscopic Precession Explorer
* **Target File:** `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html`
* **Pedagogical Objective:** Visualizes Euler's rotational equations and cross-coupling terms $\boldsymbol{\omega} \times (J \boldsymbol{\omega})$. Directly proves why pitching a quadrotor while motors are spinning induces a gyroscopic roll torque.

#### Technical Specifications & Layout
1. **Interactive Controls Panel:**
   * Moment Impulse Buttons: "+Pitch Torque $\tau_\theta$", "+Roll Torque $\tau_\phi$", "+Yaw Torque $\tau_\psi$"
   * Sustained Torque Sliders: $\tau_\phi, \tau_\theta, \tau_\psi \in [-2.0\text{ Nm}, +2.0\text{ Nm}]$
   * Motor Spin Speed $\Omega_{rotor}$: $0$ to $1200\text{ rad/s}$ (slider to amplify gyroscopic precession)
   * Toggle: "Enable Nonlinear Cross-Terms $\boldsymbol{\omega}\times(J\boldsymbol{\omega})$" vs "Linear Decoupled Model ($J\dot{\boldsymbol{\omega}} = \boldsymbol{\tau}$)"
   * Toggle: "Enable Rotor Gyroscopic Precession $\boldsymbol{\tau}_{gyro}$"
   * Play / Pause / Reset buttons.
2. **Dual Visual Displays:**
   * **Left Canvas (3D Dynamic Rigid Body):** 3D model of quadrotor responding dynamically in real time to torques. Renders the angular velocity vector $\boldsymbol{\omega}$ (yellow vector) and angular momentum vector $\mathbf{H} = J \boldsymbol{\omega}$ (cyan vector). Students can visually observe nutation and precession!
   * **Right Canvas (Real-Time Oscilloscope):** 3-channel scrolling strip chart showing $p(t)$ (red), $q(t)$ (green), $r(t)$ (blue) over the last 10 seconds.
3. **Pedagogical Experiment Banner:**
   * Instructs students: *"Set Rotor Speed to 1000 rad/s. Click '+Pitch Torque'. Observe that despite ZERO applied roll torque ($\tau_\phi = 0$), the vehicle develops a pronounced roll rate $p(t)$ due to rotor gyroscopic coupling $J_r \Omega_{net} q$!"*

#### Mathematical Simulation Loop
* State Vector: $\mathbf{x} = [\phi, \theta, \psi, p, q, r]^T$.
* Sub-stepped 4th-order Runge-Kutta (RK4) integrator running at 240 Hz ($\Delta t = 0.00416\text{ s}$):
  $$\dot{\mathbf{x}} = f(\mathbf{x}, \boldsymbol{\tau}_b)$$
  $$k_1 = f(\mathbf{x}_n, \boldsymbol{\tau}_b)$$
  $$k_2 = f(\mathbf{x}_n + \frac{\Delta t}{2} k_1, \boldsymbol{\tau}_b)$$
  $$k_3 = f(\mathbf{x}_n + \frac{\Delta t}{2} k_2, \boldsymbol{\tau}_b)$$
  $$k_4 = f(\mathbf{x}_n + \Delta t k_3, \boldsymbol{\tau}_b)$$
  $$\mathbf{x}_{n+1} = \mathbf{x}_n + \frac{\Delta t}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
* Kinematic update uses quaternion integration or $W_\eta$ with small-angle damping to prevent singularity blow-up.

---

### 4.4 Widget 4: Rotor Mixer & Control Allocation Sandbox
* **Target File:** `modules/EEEE4138_aerial_robotics/widgets/widget_4_rotor_mixer_allocation.html`
* **Pedagogical Objective:** Demystifies the mapping from virtual flight commands $[T, \tau_\phi, \tau_\theta, \tau_\psi]^T$ to physical motor speeds. Demonstrates why a standard quadrotor cannot survive a single motor loss, while a hexarotor can reallocate thrust via pseudo-inverse $M^\dagger$ to maintain controlled hover!

#### Technical Specifications & Layout
1. **Airframe Configuration Selector:**
   * Radio options: Quadrotor $+$, Quadrotor $\times$, Hexarotor $\times$, Octorotor $\times$.
2. **Virtual Command Sliders:**
   * Collective Thrust Demand $T$: $0$ to $2 T_{hover}$
   * Roll Moment Demand $\tau_\phi$: $-2.0$ to $+2.0\text{ Nm}$
   * Pitch Moment Demand $\tau_\theta$: $-2.0$ to $+2.0\text{ Nm}$
   * Yaw Moment Demand $\tau_\psi$: $-1.0$ to $+1.0\text{ Nm}$
3. **Motor Failure Sandbox (Interactive Graphic):**
   * Visual layout of airframe with clickable motor pods.
   * Clicking Motor $k$ toggles its health: Normal (Green) $\to$ Failed / Dead (Red $X$, $\Omega_k \equiv 0$).
   * Desaturation Strategy Toggle:
     * Mode 1: "Strict Clamping" (simply clips motor commands to $[0, \Omega_{max}]$)
     * Mode 2: "Attitude-Priority Desaturation" (scales down collective thrust $T$ to satisfy moment demands $\tau_\phi, \tau_\theta$, preventing uncontrollable flip).
4. **Live Mathematical Displays:**
   * **Allocation Matrix Table:** Live numerical display of mixer matrix $M$ and its calculated inverse $M^{-1}$ (or Moore-Penrose pseudo-inverse $M^\dagger = M^T (M M^T)^{-1}$).
   * **Actuator Speed Bar Gauges:** $N$ vertical gauges showing $\Omega_1, \dots, \Omega_N$ with colored indicator lines for $\Omega_{hover}$, $\Omega_{min}$, and $\Omega_{max}$ (flags saturation in bright red).
   * **Realized vs Commanded Telemetry:** Side-by-side comparison of demanded $[T^d, \boldsymbol{\tau}^d]$ vs actual delivered $[T_{act}, \boldsymbol{\tau}_{act}]$.

#### Mathematical Allocation Engine
* Healthy forward model: $\mathbf{u} = M \mathbf{\Omega}^2$.
* For Quadrotor ($4 \times 4$ full rank): $\mathbf{\Omega}^2 = M^{-1} \mathbf{u}$.
* For Hexarotor ($4 \times 6$ under-determined):
  $$M^\dagger = M^T (M M^T)^{-1}$$
  $$\mathbf{\Omega}^2 = M^\dagger \mathbf{u}$$
* Motor Failure Reconfiguration:
  If motor $k$ fails, zero out column $k$ in $M \to M_{reduced}$.
  Recalculate $M_{reduced}^\dagger = M_{reduced}^T (M_{reduced} M_{reduced}^T)^{-1}$.
  If $\det(M_{reduced} M_{reduced}^T) < 10^{-6}$, display: *"CRITICAL: Controllability Lost! Under-actuated spinning descent mode activated."*

---

### 4.5 Widget 5: Cascaded PID & LQR Flight Controller Interactive Simulation
* **Target File:** `modules/EEEE4138_aerial_robotics/widgets/widget_5_cascaded_flight_control.html`
* **Pedagogical Objective:** Visually demonstrates the Timescale Separation Principle ($\omega_n^{att} \gg \omega_n^{pos}$) and small-angle hover linearization. Allows students to physically experience how violating timescale separation causes catastrophic oscillatory instability, and how integrator augmentation rejects wind disturbances.

#### Technical Specifications & Layout
1. **Interactive 2D Flight Canvas:**
   * Drone simulation in the vertical $x\text{--}z$ plane running at 60 FPS.
   * Target Waypoint: Draggable circular crosshair $[x^d, z^d]$. Click anywhere on canvas to command instant step response!
   * Quadrotor Visual: Realistic 2D drone cross-section with tilting arms, spinning rotor thrust vectors (scaled to motor forces), and trailing trajectory path.
   * Dynamic Environment: Visual wind stream particles blowing across canvas when wind disturbance is active.
2. **Dual Controller Mode Tabs:**
   * **Tab A: Cascaded PID Controller**
     * Outer Loop Position Sliders: $K_{p,pos}, K_{d,pos}, K_{i,pos}$
     * Inner Loop Attitude Sliders: $K_{p,att}, K_{d,att}, K_{i,att}$
     * Preset Buttons: "Perfect Tuning (5x separation)", "Sluggish Attitude (Oscillatory Crash)", "Aggressive Outer Loop".
   * **Tab B: State-Space LQR Controller**
     * Position Error Penalty $q_x$: $0.1$ to $100$
     * Velocity Error Penalty $q_v$: $0.1$ to $50$
     * Tilt Error Penalty $q_\theta$: $0.1$ to $100$
     * Control Effort Penalty $r_u$: $0.01$ to $10$
     * Live Riccati solver calculating feedback gain vector $\mathbf{K} = [k_1, k_2, k_3, k_4]$.
3. **Disturbance & Physics Knobs:**
   * Horizontal Wind Force $F_{wind,x}$: $-5.0\text{ N}$ to $+5.0\text{ N}$ (demonstrates steady-state offset without integrator and automatic leveling with $K_i$).
   * Drone Mass Slider $m$: $0.5\text{ kg}$ to $3.0\text{ kg}$.
4. **Real-Time Oscilloscope HUD (3 Plots):**
   * Plot 1: Position Tracking $x(t)$ (cyan) vs Setpoint $x^d(t)$ (white dashed).
   * Plot 2: Attitude Angle $\theta(t)$ (emerald) vs Desired Tilt $\theta^d(t)$ (amber dashed).
   * Plot 3: Commanded Moment $M_y(t)$ and Thrust $T(t)$.

#### Mathematical Simulation & Control Engine
* Continuous Plant Equations:
  $$\ddot{x} = -\frac{T}{m}\sin\theta + \frac{F_{wind,x}}{m}$$
  $$\ddot{z} = g - \frac{T}{m}\cos\theta$$
  $$\ddot{\theta} = \frac{M_y}{J_y}$$
* Cascaded Controller Logic:
  1. Position Error: $e_x = x^d - x, \quad \dot{e}_x = \dot{x}^d - \dot{x}$.
  2. Commanded horizontal acceleration:
     $$u_x = K_{p,pos} e_x + K_{d,pos} \dot{e}_x + K_{i,pos} \int e_x dt$$
  3. Desired Tilt Angle (from hover linearization $\ddot{x} \approx -g\theta$):
     $$\theta^d = -\text{clamp}\left(\frac{u_x}{g}, -\theta_{max}, \theta_{max}\right) \quad (\theta_{max} = 30^\circ)$$
  4. Commanded vertical acceleration:
     $$u_z = K_{p,z} (z^d - z) + K_{d,z} (\dot{z}^d - \dot{z}) + K_{i,z} \int (z^d - z) dt$$
  5. Total Thrust Command:
     $$T = \frac{m(g - u_z)}{\cos\theta}$$
  6. Inner Loop Attitude Control:
     $$e_\theta = \theta^d - \theta, \quad e_q = 0 - q$$
     $$M_y = J_y \left( K_{p,att} e_\theta + K_{d,att} e_q + K_{i,att} \int e_\theta dt \right)$$

---

## 5. Implementation Roadmap & File Deployment Plan

| Component Deliverable | Target File Path | Target Topic | Primary Responsibility |
|---|---|---|---|
| **Topic 1 Chapter** | `modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md` | Topic 1 | Authoritative chapter text, API contract, derivations |
| **Topic 2 Chapter** | `modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md` | Topic 2 | Authoritative chapter text, API contract, derivations |
| **Topic 3 Chapter** | `modules/EEEE4138_aerial_robotics/chapters/topic_3_kinematics_dynamics.md` | Topic 3 | Authoritative chapter text, API contract, derivations |
| **Topic 4 Chapter** | `modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md` | Topic 4 | Authoritative chapter text, API contract, derivations |
| **Topic 5 Chapter** | `modules/EEEE4138_aerial_robotics/chapters/topic_5_flight_control.md` | Topic 5 | Upgrade & synthesis of prototype `topic_5_flight_ctrl_2.md` |
| **Widget 1 HTML** | `modules/EEEE4138_aerial_robotics/widgets/widget_1_flight_envelope.html` | Topic 1 | Standalone interactive flight envelope visualizer |
| **Widget 2 HTML** | `modules/EEEE4138_aerial_robotics/widgets/widget_2_frames_gimbal_lock.html` | Topic 2 | Standalone interactive 3D frame & gimbal lock simulator |
| **Widget 3 HTML** | `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html` | Topic 3 | Standalone interactive 6-DoF dynamics & precession visualizer |
| **Widget 4 HTML** | `modules/EEEE4138_aerial_robotics/widgets/widget_4_rotor_mixer_allocation.html` | Topic 4 | Standalone interactive control allocation sandbox |
| **Widget 5 HTML** | `modules/EEEE4138_aerial_robotics/widgets/widget_5_cascaded_flight_control.html` | Topic 5 | Standalone interactive cascaded PID & LQR simulation |

---

## 6. Caveats & Assumptions

1. **Topic 6 Exclusion:** In strict compliance with User Directive `2026-11-12T02:58:57Z`, Topic 6 (Trajectory Generation) and Widget 6 are deferred from this blueprint. All focus, derivations, and widgets target Topics 1 through 5.
2. **CDN Internet Requirement for Styling:** Widgets utilize Tailwind CSS via public CDN (`https://cdn.tailwindcss.com`). In fully offline environments, vanilla CSS fallback rules should be included in the `<style>` block to maintain readable layout and dark theme contrast.
3. **Small-Angle Linearization Bounds:** All linearized control models in Topic 5 assume $|\phi|, |\theta| \le 30^\circ$. Beyond $30^\circ$, trigonometric errors exceed 15%, requiring full nonlinear SE(3) geometric tracking controllers (which will be noted as an advanced caveat in the chapter text).
4. **Zero External Runtime JS Libraries:** No three.js, MathJax, or Chart.js dependencies are used in the widgets. All 3D projection, charting, and differential equation solvers are implemented directly in standard vanilla JavaScript.

---

## 7. Conclusion

This blueprint establishes a mathematically uncompromising, pedagogically scaffolded foundation for Topics 1 through 5 of EEEE4138 Aerial Robotics. By bridging undergraduate prerequisites ($F=ma$, $1/Js^2$, transfer functions, matrix algebra) directly into multirotor flight dynamics, supplying every intermediate algebraic proof step, formalizing modular API contracts, and providing complete technical architectures for 5 zero-dependency interactive Generative UI widgets, downstream implementation agents have an exact, unambiguous recipe to produce world-class textbook chapters and interactive simulations.

---

## 8. Verification Method

1. **Mathematical Derivations:**
   * Verify all elementary rotation products and matrix determinants ($R_B^I, W_\eta, \mathcal{C}$) via SymPy:
     `python -c "import sympy; ..."`
2. **API Contract Completeness:**
   * Cross-reference each input/output variable in Section 3.3 against the raw lecture slides in `modules/EEEE4138_aerial_robotics/raw/` to ensure 100% symbol consistency.
3. **Widget Code Integrity:**
   * Once implemented in `modules/EEEE4138_aerial_robotics/widgets/`, open each HTML file in a local browser or run a local HTTP server:
     `python -m http.server 8000`
   * Inspect browser console for zero syntax errors, verify responsive Canvas rendering at 60 FPS, and validate numerical convergence of the RK4 and Riccati solvers.
