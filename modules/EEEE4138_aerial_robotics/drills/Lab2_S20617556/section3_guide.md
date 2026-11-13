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
