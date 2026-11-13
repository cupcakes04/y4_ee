# Practical 2 — Section 3 Guide: Rotor Loads and Allocation

This guide covers **Section 3** of `EEEE4138 Practical 2 Guided Laboratory.pdf` for `Practical2_Quadrotor.slx` using `practical2_parameters.m` (`student_id = 19`, X configuration).

---

## 1. Simulink Blocks Needed (Section 3 Only)

Add these blocks to `Practical2_Quadrotor.slx`:

1. **Rotor speed input & limits**
   - **Constant** (*Simulink → Sources*) → set **Constant value** to `Omega_cmd`
   - **Saturation** (*Simulink → Discontinuities*) → set **Upper limit** to `Omega_max`, **Lower limit** to `0`
2. **Parameter Constant blocks** (4 separate **Constant** blocks from *Simulink → Sources*):
   - `rotor_xy` (`2 × 4`)
   - `sigma` (`4 × 1`)
   - `kT` (scalar)
   - `kM` (scalar)
3. **Calculation block**
   - **MATLAB Function** (*Simulink → User-Defined Functions*) → rename the block to `RotorLoads`
4. **Optional check (before building Section 4)**
   - Two **Display** blocks (*Simulink → Sinks*) connected to `Fprop` and `Mprop` to inspect the `3 × 1` outputs.

> **Important:** Do **not** add gravity inside `RotorLoads`. Gravity is added later inside `StateDerivative` (Section 4).

---

## 2. Wiring Diagram

```text
[Constant: Omega_cmd] ──► [Saturation (0 to Omega_max)] ──► Omega
[Constant: rotor_xy]  ────────────────────────────────────► rotor_xy   ┌────────────┐ ──► Fprop (3x1)
[Constant: sigma]     ────────────────────────────────────► sigma      │ RotorLoads │
[Constant: kT]        ────────────────────────────────────► kT         └────────────┘ ──► Mprop (3x1)
[Constant: kM]        ────────────────────────────────────► kM
```

Simulink automatically creates the 5 input ports and 2 output ports on `RotorLoads` from the function signature below.

---

## 3. Code Inside `RotorLoads`

Double-click the `RotorLoads` MATLAB Function block and enter:

```matlab
function [Fprop,Mprop] = RotorLoads(Omega,rotor_xy,sigma,kT,kM)
% Sum the thrust forces and moments from all 4 rotors in body axes
% (x forward, y right, z down).

Fprop = zeros(3,1);
Mprop = zeros(3,1);

for i = 1:4
    Ti = kT * Omega(i)^2;
    Fi = [0; 0; -Ti];
    ri = [rotor_xy(1,i); rotor_xy(2,i); 0];
    Mi = cross(ri, Fi) + [0; 0; sigma(i) * kM * Omega(i)^2];

    Fprop = Fprop + Fi;
    Mprop = Mprop + Mi;
end
end
```

### Fixed Port Dimensions (Ports and Data Manager / Edit Data)
If automatic size inference fails, open **Edit Data** (or **Ports and Data Manager**) in the MATLAB Function Editor and set **Size** explicitly:

| Port | Direction | Size |
| :--- | :--- | :--- |
| `Omega` | Input | `[4 1]` |
| `rotor_xy` | Input | `[2 4]` |
| `sigma` | Input | `[4 1]` |
| `kT` | Input | `1` |
| `kM` | Input | `1` |
| `Fprop` | Output | `[3 1]` |
| `Mprop` | Output | `[3 1]` |

---

## 4. Verification & Allocation Task (`student_id = 19`, X Configuration)

1. Run `practical2_parameters` in the MATLAB Command Window so workspace variables are loaded.
2. In Simulink, press **Ctrl+D** (Update Diagram) to confirm there are no port or dimension errors.
3. **Hover check:** At `Omega_cmd = Omega_hover * ones(4,1)`, each rotor produces $T_i = m_{\text{nom}} g / 4$, so:
   - `Fprop` = `[0; 0; -m_nom*g]`
   - `Mprop` = `[0; 0; 0]`
4. **Allocation matrix $A$** mapping $[T_1, T_2, T_3, T_4]^T \mapsto [T_{\text{total}}, M_x, M_y, M_z]^T$:
   - Each column $i$ is $[1,\; -y_i,\; x_i,\; \sigma_i (k_M/k_T)]^T$.
   - For `student_id = 19` (`rotor_xy = [d d -d -d; -d d d -d]`, $d = l/\sqrt{2}$, `sigma = [1; -1; 1; -1]`, $k_{MT} = k_M/k_T = 0.020$):

   $$A = \begin{bmatrix} 1 & 1 & 1 & 1 \\ d & -d & -d & d \\ d & d & -d & -d \\ k_{MT} & -k_{MT} & k_{MT} & -k_{MT} \end{bmatrix}$$

   Verify in MATLAB that `rank(A) == 4`.
5. **Conceptual check:** Zero propulsive moment ($\mathbf{M}_{\text{prop}} = \mathbf{0}$) means zero external torque, not necessarily zero angular velocity $\boldsymbol{\omega}$ — a rigid body with zero torque can still have a non-zero initial or coasting angular velocity.

---

# Practical 2 — Section 4 Guide: Frame Transformations and Dynamics

This guide covers **Section 4** of `EEEE4138 Practical 2 Guided Laboratory.pdf` for `Practical2_Quadrotor.slx` using `practical2_parameters.m` (`student_id = 19`, X configuration).

---

## 1. Simulink Blocks Needed (Section 4 Only)

Add these blocks to `Practical2_Quadrotor.slx` (connecting to `Fprop` and `Mprop` from `RotorLoads` in Section 3):

1. **Calculation block**
   - **MATLAB Function** (*Simulink → User-Defined Functions*) → rename the block to `StateDerivative`
2. **Parameter Constant blocks** (4 separate **Constant** blocks from *Simulink → Sources*):
   - `m` (scalar, `2.505` kg for `student_id = 19` nominal)
   - `J` (`3 × 3` diagonal inertia matrix)
   - `g` (scalar, `9.81` m/s²)
   - `c_drag` (scalar, `0` N·s/m nominal)
3. **State integrator (plant feedback loop)**
   - **Integrator** (*Simulink → Continuous*) → set **Initial condition** to `X0` (`12 × 1` zeros)
   - *(Optional static check before connecting the Integrator)*: Temporarily feed a **Constant** block set to `X0` into the `X` port of `StateDerivative` and connect a **Display** block (*Simulink → Sinks*) to `Xdot` to verify the `12 × 1` initial derivative vector.

> **Important:**
> - Gravity is included **exactly once** inside `StateDerivative` via $\mathbf{F}_g = R^T [0,\; 0,\; mg]^T$.
> - The baseline model includes **no** aerodynamic moment.
> - Use explicit parameter ports (`m`, `J`, `g`, `c_drag`); MATLAB Function blocks do not automatically read base-workspace variables.

---

## 2. Wiring Diagram

```text
                ┌─────────────────────────────────────────────────────────────┐
                │                     State feedback (X: 12x1)                │
                ▼                                                             │
         ┌───►  X                                                             │
[Fprop] ─┼───►  Fprop  ┌─────────────────┐                                    │
[Mprop] ─┼───►  Mprop  │                 │                                    │
[m]     ─┼───►  m      │ StateDerivative │ ──► Xdot (12x1) ──► [Integrator] ──┴──► X (12x1)
[J]     ─┼───►  J      │                 │                     (IC: X0)
[g]     ─┼───►  g      └─────────────────┘
[c_drag]─┴───►  c_drag
```

- `Fprop` (`3 × 1`) and `Mprop` (`3 × 1`) come directly from the `RotorLoads` outputs built in Section 3.
- `X` (`12 × 1`) state order:
  - `X(1:3)`: NED position `[pN; pE; pD]` (m)
  - `X(4:6)`: Body velocity `[u; v; w]` (m/s)
  - `X(7:9)`: Euler angles `[phi; theta; psi]` (rad)
  - `X(10:12)`: Body angular rates `[p; q; r]` (rad/s)

---

## 3. Code Inside `StateDerivative`

Double-click the `StateDerivative` MATLAB Function block and enter:

```matlab
function Xdot = StateDerivative(X,Fprop,Mprop,m,J,g,c_drag)
% Compute 12-state rigid-body quadrotor derivatives in NED / body axes.

% Extract states
vb    = X(4:6);
phi   = X(7);
theta = X(8);
psi   = X(9);
omega = X(10:12);

% Body-to-NED rotation matrix R = Rz * Ry * Rx
Rx = [1 0 0; 0 cos(phi) -sin(phi); 0 sin(phi) cos(phi)];
Ry = [cos(theta) 0 sin(theta); 0 1 0; -sin(theta) 0 cos(theta)];
Rz = [cos(psi) -sin(psi) 0; sin(psi) cos(psi) 0; 0 0 1];
R  = Rz * Ry * Rx;

% Position kinematics (NED)
pos_dot = R * vb;

% Translational dynamics (body axes)
Fg     = R.' * [0; 0; m*g];
Fdrag  = -c_drag * vb;
vb_dot = (Fg + Fprop + Fdrag)/m - cross(omega, vb);

% Attitude kinematics (Euler angle rates)
E = [1  sin(phi)*tan(theta)   cos(phi)*tan(theta);
     0  cos(phi)             -sin(phi);
     0  sin(phi)/cos(theta)   cos(phi)/cos(theta)];
euler_dot = E * omega;

% Rotational dynamics (body axes)
omega_dot = J \ (Mprop - cross(omega, J * omega));

% Assemble 12x1 state derivative
Xdot = zeros(12,1);
Xdot(1:3)   = pos_dot;
Xdot(4:6)   = vb_dot;
Xdot(7:9)   = euler_dot;
Xdot(10:12) = omega_dot;
end
```

### Fixed Port Dimensions (Ports and Data Manager / Edit Data)
If automatic size inference fails, open **Edit Data** (or **Ports and Data Manager**) in the MATLAB Function Editor and set **Size** explicitly:

| Port | Direction | Size |
| :--- | :--- | :--- |
| `X` | Input | `[12 1]` |
| `Fprop` | Input | `[3 1]` |
| `Mprop` | Input | `[3 1]` |
| `m` | Input | `1` |
| `J` | Input | `[3 3]` |
| `g` | Input | `1` |
| `c_drag` | Input | `1` |
| `Xdot` | Output | `[12 1]` |

---

## 4. Verification Checks (Before Running Full Validation Tests)

1. **Diagram & dimension check:** Run `practical2_parameters` in the MATLAB Command Window, then press **Ctrl+D** (Update Diagram) in Simulink. Confirm there are no dimension errors and that `X` and `Xdot` are `12 × 1` while `Fprop` and `Mprop` are `3 × 1`.
2. **Frame-mapping checks (in MATLAB Command Window):**
   - **Zero angles:** At `phi = 0; theta = 0; psi = 0;`, verify `R` equals `eye(3)`.
   - **East-facing velocity:** At `phi = 0; theta = 0; psi = pi/2;` and `vb = [5; 0; 0]`, verify `R * vb` equals `[0; 5; 0]` m/s (due East).
   - **Orthogonality & determinant:** Verify `R * R.'` is `eye(3)` (within floating-point precision) and `det(R) == 1`.
3. **Nominal hover derivative check:** At `X = zeros(12,1)` and `Omega_cmd = Omega_hover * ones(4,1)` with `c_drag = 0`:
   - `Fprop = [0; 0; -m_nom*g]` cancels `Fg = [0; 0; m_nom*g]`, and `Mprop = [0; 0; 0]`.
   - Every entry of `Xdot` should evaluate to `0`.
4. **Euler singularity & rate note:**
   - At `phi = theta = 0`, `E = eye(3)` so `euler_dot = omega` ($[\dot{\phi},\dot{\theta},\dot{\psi}]^T = [p,q,r]^T$); this equality does **not** hold at nonzero roll/pitch.
   - Keep pitch $\theta$ away from $\pm 90^\circ$ ($\pm \pi/2$ rad), where $\cos(\theta) = 0$ causes a singularity in `E`.

---

# Practical 2 — Section 5 Guide: Assemble, Configure, and Log the Model

This guide covers **Section 5** of `EEEE4138 Practical 2 Guided Laboratory.pdf` for `Practical2_Quadrotor.slx` using `practical2_parameters.m` (`student_id = 19`, X configuration).

---

## 1. Full Plant Wiring & Logging Blocks

Assemble the complete open-loop plant (`RotorLoads` → `StateDerivative` → `Integrator` with state feedback `X`) and attach **5 `To Workspace` blocks** (*Simulink → Sinks*):

```text
[Constant: Omega_cmd] ─► [Saturation (0 to Omega_max)] ─┬─► Omega ──► [RotorLoads] ──┬─► Fprop ──┬─► [StateDerivative] ──┬─► Xdot ──► [Integrator (IC: X0)] ──┬─► X
                                                        │                            │           │                       │                                 │
                                                        ▼                            ▼           │                       ▼                                 ├──► [To Workspace: X_log]
                                             [To Workspace: Omega_log]   [To Workspace: Fprop_log]│           [To Workspace: Xdot_log]                      │
                                                                                                 ▼                                                         │
                                                                                   Mprop ────────┴──► [To Workspace: Mprop_log]                            │
                                                                                                                                                           │
                                                        ▲                                                                                                  │
                                                        └─────────────────────────────── State feedback X (12x1) ──────────────────────────────────────────┘
```

*(Note: Keep all parameter `Constant` blocks connected as in Sections 3 & 4: `rotor_xy`, `sigma`, `kT`, `kM` to `RotorLoads`, and `m`, `J`, `g`, `c_drag` to `StateDerivative`.)*

### `To Workspace` Block Settings (All 5 Blocks)

| Signal | Connect From | Variable name | Save format | Sample time |
| :--- | :--- | :--- | :--- | :--- |
| State vector `X` | Output of `Integrator` | `X_log` | `Timeseries` | `0.01` |
| Applied rotor speeds | Output of `Saturation` | `Omega_log` | `Timeseries` | `0.01` |
| Propulsive force `Fprop` | Output 1 of `RotorLoads` | `Fprop_log` | `Timeseries` | `0.01` |
| Propulsive moment `Mprop` | Output 2 of `RotorLoads` | `Mprop_log` | `Timeseries` | `0.01` |
| State derivative `Xdot` | Output of `StateDerivative` | `Xdot_log` | `Timeseries` | `0.01` |

---

## 2. Model Settings (`Ctrl+E` / Configuration Parameters)

Open **Modeling → Model Settings** (`Ctrl+E`) and configure both tabs:

1. **Solver**
   - **Type:** `Variable-step`
   - **Solver:** `ode45` (Dormand-Prince)
   - **Max step size:** `0.01`
   - **Relative tolerance:** `1e-6`
   - **Absolute tolerance:** `1e-8`
   - **Stop time:** `2` (initially `2` s; shorten to `0.20` s for differential-moment tests in Section 6)
2. **Data Import/Export**
   - Enable **Single simulation output**
   - **Single simulation output** variable name: `out`

---

## 3. Pre-Run Diagram Check

1. Save `Practical2_Quadrotor.slx`.
2. Run `practical2_parameters` in the MATLAB Command Window.
3. Press **Ctrl+D** (Update Diagram) in Simulink and confirm:
   - No compilation or dimension errors.
   - `X` and `Xdot` signals show `12 × 1` (`12`).
   - `Fprop` and `Mprop` signals show `3 × 1` (`3`).

---

## 4. Run and Save the Nominal Hover Test (`run_hover_test.m`)

Run [run_hover_test.m](file:///d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/drills/Lab2_S20617556/run_hover_test.m) (or paste the commands below into the MATLAB Command Window):

```matlab
practical2_parameters
out = sim('Practical2_Quadrotor');
if ~exist('results','dir'), mkdir('results'); end
save('results/hover.mat','out','X0','Omega_cmd','m','J');

ts = out.X_log;
if ts.IsTimeFirst
    X = reshape(ts.Data,numel(ts.Time),[]);
else
    X = reshape(ts.Data,[],numel(ts.Time)).';
end

figure;
plot(ts.Time,X(:,1:3));
xlabel('Time (s)'); ylabel('NED position (m)');
legend('North','East','Down'); grid on;
saveas(gcf,'results/hover_position.png');
```

### Expected Result & Multi-Test Workflow
- **Nominal hover check:** All three NED position traces (`North`, `East`, `Down`) and body velocities stay close to `0` over the `2 s` run.
- **Test isolation rules (for Sections 6 & 7):**
  1. Run `practical2_parameters` first to reset all workspace variables.
  2. Apply the test-specific overrides (e.g., `Omega_cmd`, `X0`, `m`, `c_drag`, or `StopTime`) **after** running `practical2_parameters`. Do **not** re-run `practical2_parameters` after applying overrides.
  3. Save each `out` object under a distinct filename in `results/` before running the next test.

---

# Practical 2 — Section 6 Guide: Isolated Validation Tests

This guide covers **Section 6** of `EEEE4138 Practical 2 Guided Laboratory.pdf` for `Practical2_Quadrotor.slx` using `practical2_parameters.m` (`student_id = 19`, X configuration).

Key baseline numbers for `student_id = 19`:
- `m_nom = 2.5050` kg, `l = 0.27` m, $d = l/\sqrt{2} = 0.190919$ m
- `Jdiag = [0.038958; 0.038958; 0.064930]` kg·m²
- Hover thrust per rotor: $T_{i0} = m_{\text{nom}} g / 4 = 6.143513\text{ N}$ ($T_{\text{total}} = 24.574050\text{ N}$)
- Differential thrust increment: $\delta = 0.05\, T_{i0} = 0.307176\text{ N}$

---

## 1. Analytical Predictions (`student_id = 19`, X Geometry)

Compute and verify these **before** looking at simulation outputs:

1. **Frame mapping ($\phi = \theta = 0,\; \psi = \pi/2,\; \mathbf{v}_b = [5;\; 0;\; 0]\text{ m/s}$)**
   - $R = R_z(\pi/2) R_y(0) R_x(0) = \begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}$
   - NED velocity: $R \mathbf{v}_b = [0;\; 5;\; 0]\text{ m/s}$ (due East).
   - Orthogonality & right-handedness: $R R^T = I_3$ and $\det(R) = +1$.

2. **Hover (`X0 = zeros(12,1)`, `Omega_cmd = Omega_hover*ones(4,1)`, `c_drag = 0`, `2 s`)**
   - $\mathbf{F}_{\text{prop}} = [0;\; 0;\; -24.574050]\text{ N}$ cancels $\mathbf{F}_g = [0;\; 0;\; +24.574050]\text{ N}$; $\mathbf{M}_{\text{prop}} = \mathbf{0}$.
   - Predicted $\dot{\mathbf{X}}(0) = \mathbf{0}_{12\times 1}$; position and velocity drift $\approx 0$ over $2\text{ s}$.

3. **Free fall (`X0 = zeros(12,1)`, `Omega_cmd = zeros(4,1)`, `2 s`)**
   - $\mathbf{F}_{\text{prop}} = \mathbf{0}$, $\mathbf{M}_{\text{prop}} = \mathbf{0}$, so $\dot{w}(0) = +g = +9.81\text{ m/s}^2$ (Down is $+z$).
   - At $t = 2\text{ s}$:
     - $w(2) = g t = 9.81 \times 2 = 19.62\text{ m/s}$
     - $p_D(2) = \frac{1}{2} g t^2 = 0.5 \times 9.81 \times 2^2 = 19.62\text{ m}$
   - Unchanged attitude and rates: $\phi = \theta = \psi = 0$, $p = q = r = 0$.

4. **Differential pitch (`T_target = [Ti0+delta; Ti0+delta; Ti0-delta; Ti0-delta]`, `0.20 s`)**
   - `Omega_cmd = sqrt(T_target / kT)` $= [579.6551;\; 579.6551;\; 551.3620;\; 551.3620]\text{ rad/s}$ (all within $[0,\; 800]$).
   - Using X-geometry allocation $A$:
     - $T_{\text{total}} = 4 T_{i0} = 24.574050\text{ N}$ ($F_{\text{prop},z} = -24.574050\text{ N}$)
     - $M_x = d(T_1 - T_2 - T_3 + T_4) = 0\text{ N}\cdot\text{m}$
     - $M_y = d(T_1 + T_2 - T_3 - T_4) = 4 d \delta = 4(0.190919)(0.307176) = +0.234582\text{ N}\cdot\text{m}$
     - $M_z = k_{MT}(T_1 - T_2 + T_3 - T_4) = 0\text{ N}\cdot\text{m}$
   - Initial $q$ derivative ($\boldsymbol{\omega}(0)=\mathbf{0} \implies \boldsymbol{\omega}\times J\boldsymbol{\omega} = \mathbf{0}$):
     $$\dot{q}(0) = \frac{M_y}{J_{yy}} = \frac{0.234582}{0.03895776} = +6.021456\text{ rad/s}^2$$
   - Pure pitch rotation about principal $y$-axis ($\dot{q}$ stays constant over $0.20\text{ s}$, so $q(0.20) \approx 1.204291\text{ rad/s}$, $\theta(0.20) \approx 0.120429\text{ rad}$).

5. **Yaw reaction (`T_target = [Ti0+delta; Ti0-delta; Ti0+delta; Ti0-delta]`, `0.20 s`)**
   - `Omega_cmd = sqrt(T_target / kT)` $= [579.6551;\; 551.3620;\; 579.6551;\; 551.3620]\text{ rad/s}$ (all within $[0,\; 800]$).
   - Using `sigma = [1; -1; 1; -1]` and $k_{MT} = 0.020$:
     - $T_{\text{total}} = 24.574050\text{ N}$, $M_x = 0\text{ N}\cdot\text{m}$, $M_y = 0\text{ N}\cdot\text{m}$
     - $M_z = k_{MT}(T_1 - T_2 + T_3 - T_4) = 4 k_{MT} \delta = 4(0.020)(0.307176) = +0.024574\text{ N}\cdot\text{m}$
   - Initial $r$ derivative ($\boldsymbol{\omega}(0)=\mathbf{0}$):
     $$\dot{r}(0) = \frac{M_z}{J_{zz}} = \frac{0.024574}{0.0649296} = +0.378472\text{ rad/s}^2$$
   - Positive $M_z$ gives $+r$ and $+\psi$ (clockwise viewed from above in NED body axes, matching `+1` reaction torque on rotors 1 & 3). Over $0.20\text{ s}$, $r(0.20) \approx 0.075694\text{ rad/s}$, $\psi(0.20) \approx 0.007569\text{ rad}$.

> **Important conceptual rules (PDF pp. 6–7):**
> - Record **initial derivative** comparisons separately from **final state** comparisons.
> - Do **not** assume later angular rates equal $M/J$; $J^{-1} M$ is initial angular acceleration, and the full 12-state plant evolves over time.
> - Body velocity derivatives $\dot{\mathbf{v}}_b$ are not simply inertial acceleration in body axes; $-\boldsymbol{\omega} \times \mathbf{v}_b$ accounts for the rotating body frame.

---

## 2. MATLAB Script (`run_validation_tests.m`)

Run [run_validation_tests.m](file:///d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/drills/Lab2_S20617556/run_validation_tests.m) in MATLAB (ensure [run_hover_test.m](file:///d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/drills/Lab2_S20617556/run_hover_test.m) has already produced `results/hover.mat`). Each test resets via `practical2_parameters` first, applies its overrides, runs `sim` with the required `StopTime`, saves a distinct `.mat` file and plot in `results/`, and exports the Section 6 comparison table to `results/section6_validation.csv`.

```matlab
%% Section 6: Isolated Validation Tests (student_id = 19, X configuration)
if ~exist('results','dir'), mkdir('results'); end

%% 1. Frame mapping check (analytic)
phi = 0; theta = 0; psi = pi/2;
Rx = [1 0 0; 0 cos(phi) -sin(phi); 0 sin(phi) cos(phi)];
Ry = [cos(theta) 0 sin(theta); 0 1 0; -sin(theta) 0 cos(theta)];
Rz = [cos(psi) -sin(psi) 0; sin(psi) cos(psi) 0; 0 0 1];
R  = Rz*Ry*Rx;
v_ned_pred = [0; 5; 0];
v_ned = R * [5; 0; 0];
ortho_err = norm(R*R.' - eye(3));
det_R = det(R);
fprintf('Frame mapping: v_ned = [%.4f %.4f %.4f], norm(R*R''-I) = %.2e, det(R) = %.6f\n', ...
    v_ned(1), v_ned(2), v_ned(3), ortho_err, det_R);

%% 2. Hover (load Section 5 baseline to inspect initial derivative & drift)
load('results/hover.mat');
X_hov  = extract_ts(out.X_log);
Xd_hov = extract_ts(out.Xdot_log);
hov_xdot0_max = max(abs(Xd_hov(1,:)));
hov_xend_max  = max(abs(X_hov(end,:)));
fprintf('Hover: max|Xdot(0)| = %.2e, max|X(end)| = %.2e\n', hov_xdot0_max, hov_xend_max);

%% 3. Free fall (2 s)
practical2_parameters
X0 = zeros(12,1);
Omega_cmd = zeros(4,1);
out = sim('Practical2_Quadrotor','StopTime','2');
save('results/freefall.mat','out','X0','Omega_cmd','m','J');

t_ff = out.X_log.Time;
X_ff = extract_ts(out.X_log);
pD_ff_pred = 0.5 * g * 2^2;
w_ff_pred  = g * 2;
pD_ff_sim  = X_ff(end,3);
w_ff_sim   = X_ff(end,6);
att_ff_max = max(abs(X_ff(end,7:12)));
fprintf('Free fall (t=2 s): pD = %.6f m, w = %.6f m/s, max|att,rates| = %.2e\n', ...
    pD_ff_sim, w_ff_sim, att_ff_max);

figure;
plot(t_ff, X_ff(:,3), 'LineWidth', 1.5); hold on;
plot(t_ff, X_ff(:,6), '--', 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('Down position (m) / w (m/s)');
legend('p_D (m)', 'w (m/s)', 'Location', 'northwest'); grid on;
title('Section 6: Free Fall Response');
saveas(gcf,'results/freefall.png');

%% 4. Differential pitch (0.20 s)
practical2_parameters
Ti0 = m_nom*g/4;
delta = 0.05*Ti0;
T_target = [Ti0+delta; Ti0+delta; Ti0-delta; Ti0-delta];
Omega_cmd = sqrt(T_target/kT);
assert(all(Omega_cmd >= 0 & Omega_cmd <= Omega_max), 'Omega_cmd out of bounds!');
out = sim('Practical2_Quadrotor','StopTime','0.20');
save('results/diff_pitch.mat','out','X0','Omega_cmd','m','J','T_target');

t_dp  = out.X_log.Time;
X_dp  = extract_ts(out.X_log);
Xd_dp = extract_ts(out.Xdot_log);
F_dp  = extract_ts(out.Fprop_log);
M_dp  = extract_ts(out.Mprop_log);

d_arm        = l/sqrt(2);
Ttotal_pred  = 4*Ti0;
My_pred      = 4*d_arm*delta;
qdot0_pred   = My_pred / J(2,2);
Ttotal_dp    = -F_dp(1,3);
Mx_dp        = M_dp(1,1);
My_dp        = M_dp(1,2);
Mz_dp        = M_dp(1,3);
qdot0_dp     = Xd_dp(1,11);
q_end_dp     = X_dp(end,11);
theta_end_dp = X_dp(end,8);

fprintf('Diff pitch: Fprop(0) = [%.4f %.4f %.4f] N, Mprop(0) = [%.6f %.6f %.6f] N*m\n', ...
    F_dp(1,1), F_dp(1,2), F_dp(1,3), Mx_dp, My_dp, Mz_dp);
fprintf('Diff pitch: qdot(0) = %.6f rad/s^2, q(0.20) = %.6f rad/s, theta(0.20) = %.6f rad\n', ...
    qdot0_dp, q_end_dp, theta_end_dp);

figure;
subplot(2,1,1); plot(t_dp, X_dp(:,11), 'LineWidth', 1.5);
ylabel('q (rad/s)'); title('Section 6: Differential Pitch (0.20 s)'); grid on;
subplot(2,1,2); plot(t_dp, X_dp(:,8), 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('\theta (rad)'); grid on;
saveas(gcf,'results/diff_pitch.png');

%% 5. Yaw reaction (0.20 s)
practical2_parameters
Ti0 = m_nom*g/4;
delta = 0.05*Ti0;
T_target = [Ti0+delta; Ti0-delta; Ti0+delta; Ti0-delta];
Omega_cmd = sqrt(T_target/kT);
assert(all(Omega_cmd >= 0 & Omega_cmd <= Omega_max), 'Omega_cmd out of bounds!');
out = sim('Practical2_Quadrotor','StopTime','0.20');
save('results/yaw_reaction.mat','out','X0','Omega_cmd','m','J','T_target');

t_yaw  = out.X_log.Time;
X_yaw  = extract_ts(out.X_log);
Xd_yaw = extract_ts(out.Xdot_log);
F_yaw  = extract_ts(out.Fprop_log);
M_yaw  = extract_ts(out.Mprop_log);

Mz_pred     = 4*kMT*delta;
rdot0_pred  = Mz_pred / J(3,3);
Ttotal_yaw  = -F_yaw(1,3);
Mx_yaw      = M_yaw(1,1);
My_yaw      = M_yaw(1,2);
Mz_yaw      = M_yaw(1,3);
rdot0_yaw   = Xd_yaw(1,12);
r_end_yaw   = X_yaw(end,12);
psi_end_yaw = X_yaw(end,9);

fprintf('Yaw reaction: Fprop(0) = [%.4f %.4f %.4f] N, Mprop(0) = [%.6f %.6f %.6f] N*m\n', ...
    F_yaw(1,1), F_yaw(1,2), F_yaw(1,3), Mx_yaw, My_yaw, Mz_yaw);
fprintf('Yaw reaction: rdot(0) = %.6f rad/s^2, r(0.20) = %.6f rad/s, psi(0.20) = %.6f rad\n', ...
    rdot0_yaw, r_end_yaw, psi_end_yaw);

figure;
subplot(2,1,1); plot(t_yaw, X_yaw(:,12), 'LineWidth', 1.5);
ylabel('r (rad/s)'); title('Section 6: Yaw Reaction (0.20 s)'); grid on;
subplot(2,1,2); plot(t_yaw, X_yaw(:,9), 'LineWidth', 1.5);
xlabel('Time (s)'); ylabel('\psi (rad)'); grid on;
saveas(gcf,'results/yaw_reaction.png');

%% 6. Export validation summary table (matches PDF Section 6 table) to CSV
Test = { ...
    'Frame mapping'; ...
    'Hover'; ...
    'Free fall'; ...
    'Differential pitch'; ...
    'Yaw reaction' };

Predicted_quantity_and_value = { ...
    'v_ned = [0; 5; 0] m/s; R*R'' = I3; det(R) = 1'; ...
    'Xdot(0) = 0 (12x1); drift = 0 m over 2 s'; ...
    sprintf('pD(2s) = %.6f m; w(2s) = %.6f m/s; att,rates = 0', pD_ff_pred, w_ff_pred); ...
    sprintf('My = %.6f N*m; qdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = Mz = 0', My_pred, qdot0_pred, Ttotal_pred); ...
    sprintf('Mz = %.6f N*m; rdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = My = 0', Mz_pred, rdot0_pred, Ttotal_pred) };

Simulated_value = { ...
    sprintf('v_ned = [%.4f; %.4f; %.4f] m/s; norm(R*R''-I) = %.2e; det(R) = %.6f', v_ned(1), v_ned(2), v_ned(3), ortho_err, det_R); ...
    sprintf('max|Xdot(0)| = %.2e; max|X(2s)| = %.2e', hov_xdot0_max, hov_xend_max); ...
    sprintf('pD(2s) = %.6f m; w(2s) = %.6f m/s; max|att,rates| = %.2e', pD_ff_sim, w_ff_sim, att_ff_max); ...
    sprintf('My = %.6f N*m; qdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = %.2e, Mz = %.2e N*m; q(0.20) = %.6f rad/s, theta(0.20) = %.6f rad', My_dp, qdot0_dp, Ttotal_dp, Mx_dp, Mz_dp, q_end_dp, theta_end_dp); ...
    sprintf('Mz = %.6f N*m; rdot(0) = %.6f rad/s^2; Ttotal = %.6f N; Mx = %.2e, My = %.2e N*m; r(0.20) = %.6f rad/s, psi(0.20) = %.6f rad', Mz_yaw, rdot0_yaw, Ttotal_yaw, Mx_yaw, My_yaw, r_end_yaw, psi_end_yaw) };

Difference_and_explanation = { ...
    sprintf('max|v_err| = %.2e m/s; orthogonal R (det = +1) maps +x body to +y NED East at psi = pi/2.', max(abs(v_ned - v_ned_pred))); ...
    sprintf('max|X(2s)| = %.2e m; hover thrust cancels gravity (Fg + Fprop = 0) with Mprop = 0 up to roundoff.', hov_xend_max); ...
    sprintf('dpD = %.2e m, dw = %.2e m/s; +g acts along +z Down with zero thrust and unchanged attitude.', abs(pD_ff_sim - pD_ff_pred), abs(w_ff_sim - w_ff_pred)); ...
    sprintf('dMy = %.2e N*m, dqdot(0) = %.2e rad/s^2; +My about body y accelerates q linearly over 0.20 s (zero initial coupling).', abs(My_dp - My_pred), abs(qdot0_dp - qdot0_pred)); ...
    sprintf('dMz = %.2e N*m, drdot(0) = %.2e rad/s^2; sigma = [1;-1;1;-1] produces +Mz and +r/+psi yaw acceleration with Mx = My = 0.', abs(Mz_yaw - Mz_pred), abs(rdot0_yaw - rdot0_pred)) };

T_val = table(Test, Predicted_quantity_and_value, Simulated_value, Difference_and_explanation, ...
    'VariableNames', {'Test', 'Predicted quantity and value', 'Simulated value', 'Difference and explanation'});
writetable(T_val, 'results/section6_validation.csv');
disp(T_val);

%% Local helper
function A = extract_ts(ts)
    if ts.IsTimeFirst
        A = reshape(ts.Data, numel(ts.Time), []);
    else
        A = reshape(ts.Data, [], numel(ts.Time)).';
    end
end
```

---

## 3. Validation Summary Table (`student_id = 19`)

Fill in the **Simulated value** and **Difference and explanation** columns after running the script above:

| Test | Predicted quantity and value | Simulated value | Difference and explanation |
| :--- | :--- | :--- | :--- |
| Frame mapping | $R\mathbf{v}_b = [0;\; 5;\; 0]\text{ m/s}$, $R R^T = I_3$, $\det(R) = 1$ | | |
| Hover | $\dot{\mathbf{X}}(0) = \mathbf{0}_{12\times 1}$; zero drift over $2\text{ s}$ | | |
| Free fall | $p_D(2) = 19.62\text{ m}$, $w(2) = 19.62\text{ m/s}$, $\phi=\theta=\psi=0$ | | |
| Differential pitch | $M_y = 0.234582\text{ N}\cdot\text{m}$, $\dot{q}(0) = 6.021456\text{ rad/s}^2$, $T_{\text{total}} = 24.574050\text{ N}$, $M_x = M_z = 0$ | | |
| Yaw reaction | $M_z = 0.024574\text{ N}\cdot\text{m}$, $\dot{r}(0) = 0.378472\text{ rad/s}^2$, $T_{\text{total}} = 24.574050\text{ N}$, $M_x = M_y = 0$ | | |



