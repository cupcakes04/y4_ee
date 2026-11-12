# ADVERSARIAL STRESS TEST & VERIFICATION REPORT
**Milestone**: M-FINAL Simulation & Widget Stress Challenger (Challenger 2)  
**Agent**: Challenger 2 (`challenger_final_2`)  
**Verdict**: `REQUEST_CHANGES`  
**Overall Risk Assessment**: MEDIUM  

---

## 1. Observation

### Obs 1.1: Project E2E Verification Suite Pass Rate
- Command: `python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py`
- Result: Code 0, Total: 74 | Passed: 74 | Failed: 0 | Warnings: 0 | Execution Time: 0.747 s.
- Self-Test Mode: `python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py --self-test --verbose`
- Result: Code 0, Total: 13 | Passed: 13 | Failed: 0 | Warnings: 0 | Execution Time: 0.737 s.
- All 5 topic chapters, 5 widgets, KaTeX equations, coordinate invariants (NED/FRD), and SymPy/NumPy mathematical oracles passed.

### Obs 1.2: Mathematical Sign Inversion in Widget 3 Coriolis Cross-Terms
- File: `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html`
- Lines 556–567 (Multirotor principal axes branch):
```javascript
556:         if (Math.abs(Jxz) < 1e-6) {
557:           // Principal axes formulation (multirotor standard)
558:           let cross_x = 0.0, cross_y = 0.0, cross_z = 0.0;
559:           if (enableCrossTerms) {
560:             cross_x = (Jz - Jy) * q_in * r_in;
561:             cross_y = (Jx - Jz) * p_in * r_in;
562:             cross_z = (Jy - Jx) * p_in * q_in;
563:           }
564: 
565:           p_dot = (Tx + cross_x - tau_gyro_x - dampingCoeff * p_in) / Jx;
566:           q_dot = (Ty + cross_y - tau_gyro_y - dampingCoeff * q_in) / Jy;
567:           r_dot = (Tz + cross_z - dampingCoeff * r_in) / Jz;
```
- Compare with Lines 569–584 (Fixed-wing asymmetric branch with $J_{xz} \neq 0$):
```javascript
575:           if (enableCrossTerms) {
576:             A += (Jy - Jz) * q_in * r_in + Jxz * p_in * q_in;
577:             B += (Jz - Jx) * p_in * r_in - Jxz * (p_in * p_in - r_in * r_in);
578:             C += (Jx - Jy) * p_in * q_in - Jxz * q_in * r_in;
579:           }
580: 
581:           p_dot = (Jz * A + Jxz * C) / Gamma;
```
- Compare with Authoritative Python Test Suite in `modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py` Lines 690–691:
```python
690:     cross_coupling_torque = (Jy - Jz) * q * r
691:     p_dot = (Mx + cross_coupling_torque) / Jx
```
- Observation: In the multirotor branch of Widget 3, `cross_x` is defined as `(Jz - Jy) * q_in * r_in` and added directly in `Tx + cross_x`, resulting in $+ (J_z - J_y) q r / J_x$. In contrast, the fixed-wing branch and the textbook/Python oracle use $+ (J_y - J_z) q r / J_x = - (J_z - J_y) q r / J_x$. Switching between multirotor and fixed-wing airframes causes an unexpected physical sign reversal of Coriolis cross-coupling moments.

### Obs 1.3: RK4 Integrator Numerical Stability in Widget 3
- Tested with sub-stepped RK4 ($DT = \frac{1}{240} \approx 0.004167$ s) under:
  - Rotor speed: $\Omega = 1200$ rad/s ($H_z = J_r \Omega = 0.060$ N·m·s).
  - Torque impulse $M = [5, 5, 5]$ N·m for 0.2 s: stable, peak angular velocity 48.9 rad/s, quaternion norm $= 1.000000$.
  - Extreme torque impulse $M = [20, -20, 20]$ N·m for 0.5 s: stable, peak rate 376.5 rad/s (~3600 RPM tumbling), quaternion norm $= 1.000000$.
  - Stress impulse limit test: Tested sustained impulses of 10, 50, 100, 200, 500 N·m. Integrator remained strictly stable without NaN or overflow up to 500 N·m (failed only at an unphysical 1000 N·m).

### Obs 1.4: CARE Solver (Newton-Kleinman) Accuracy in Widget 5
- Script: `modules/EEEE4138_aerial_robotics/scripts/stress_care_lqr.py`
- Evaluated against SciPy's `scipy.linalg.solve_continuous_are(A, B, Q, R)`:
  - Nominal UI ($q_x=4, q_v=1, q_\theta=8, q_q=0.5, r_u=2$):
    - JS Gain: `[-1.4142, -1.3818, 4.8878, 0.7695]`, SciPy Gain: `[-1.4142, -1.3818, 4.8878, 0.7695]`
    - Max absolute error: $8.88 \times 10^{-15}$, Relative error: $1.82 \times 10^{-15}$ (6 iterations).
  - Min UI Bounds ($q_x=0.1, q_v=0.1, q_\theta=0.1, q_q=0.05, r_u=20$):
    - Max absolute error: $2.78 \times 10^{-16}$, Relative error: $3.87 \times 10^{-16}$ (8 iterations).
  - Max UI Bounds ($q_x=50, q_v=25, q_\theta=50, q_q=10, r_u=0.1$):
    - Max absolute error: $1.67 \times 10^{-13}$, Relative error: $2.28 \times 10^{-15}$ (11 iterations).
  - Heavy Position Penalty ($q_x=50, q_v=0.1, q_\theta=0.1, q_q=0.05, r_u=1.0$):
    - Max absolute error: $7.11 \times 10^{-14}$ (8 iterations).
  - Cheap Control ($r_u = 0.05$):
    - Max absolute error: $1.28 \times 10^{-13}$ (10 iterations).
  - Extreme Skewed ($q_x=100, q_v=1, q_\theta=100, q_q=5, r_u=0.01$):
    - Max absolute error: $6.58 \times 10^{-12}$ (12 iterations).
  - All tested reachable states converged to double precision machine accuracy.

### Obs 1.5: Gauss-Jordan & Pseudo-Inverse Reallocation in Widget 4
- Script: `modules/EEEE4138_aerial_robotics/scripts/stress_allocation.py`
- Airframes: Quadrotor Plus, Quadrotor Cross, Hexarotor, Octorotor.
- Results:
  - Quadrotor (+ and $\times$): Any single motor failure drops rank to 3. The pivot threshold `maxVal < 1e-7` safely returns `null`. Fallback to best-effort hover allocation executes cleanly without NaN or exceptions.
  - Hexarotor ($N=6$):
    - Single failures: 6 / 6 single failure modes maintain full Rank 4 control and successfully reallocate moments.
    - Double failures (15 combinations): 12 / 15 double failure modes maintain full Rank 4 control. Exactly 3 diametrically opposite 180° rotor pairs (M1+M4, M2+M5, M3+M6 with collinear moment arms) become singular ($\text{det}(G) = 0$). Gauss-Jordan cleanly returns `null` and activates safe best-effort hover allocation.
  - Octorotor ($N=8$):
    - Single failures: 8 / 8 maintain Rank 4.
    - Double failures: 28 / 28 maintain Rank 4.
    - Triple failures: 56 / 56 maintain Rank 4.

### Obs 1.6: Offline Fallback Styling Readability
- All 5 widgets include inline `<style>` tags with dark background `#020617`, off-white text `#f8fafc`, system font fallback stacks, and custom range slider styles.
- Zero external JS libraries (no Three.js, Babylon.js, MathJax, or React).
- Finding: In `widget_3_rigid_body_dynamics.html` (line 120) and `widget_5_cascaded_flight_control.html` (line 132), canvas wrapper elements rely on Tailwind JIT arbitrary classes `aspect-[4/3]` and `aspect-[16/9]`. In environments where external CDN script `cdn.tailwindcss.com` is strictly blocked and the browser does not parse unknown classes, containers without explicit height or canvas fallback sizes could collapse unless inline height/aspect-ratio fallbacks are provided.

---

## 2. Logic Chain

1. **Euler's Equations of Motion (First Principles)**:
   The rotational dynamics of a rigid body in the body frame are governed by:
   $$\mathbf{M}_b = \mathbf{J} \dot{\boldsymbol{\omega}}_b + \boldsymbol{\omega}_b \times (\mathbf{J} \boldsymbol{\omega}_b)$$
   Rearranging for the angular acceleration vector $\dot{\boldsymbol{\omega}}_b$:
   $$\mathbf{J} \dot{\boldsymbol{\omega}}_b = \mathbf{M}_b - \boldsymbol{\omega}_b \times (\mathbf{J} \boldsymbol{\omega}_b)$$
   For a diagonal inertia matrix $\mathbf{J} = \text{diag}(J_x, J_y, J_z)$, the x-component of the cross-product is:
   $$\left( \boldsymbol{\omega}_b \times (\mathbf{J}\boldsymbol{\omega}_b) \right)_x = q (J_z r) - r (J_y q) = (J_z - J_y) q r$$
   Therefore:
   $$J_x \dot{p} = M_x - (J_z - J_y) q r = M_x + (J_y - J_z) q r$$
   Similarly:
   $$J_y \dot{q} = M_y + (J_z - J_x) p r$$
   $$J_z \dot{r} = M_z + (J_x - J_y) p q$$

2. **Connecting Step 1 to Observation 1.2**:
   - In `widget_3_rigid_body_dynamics.html` line 560, the author wrote:
     `cross_x = (Jz - Jy) * q_in * r_in;`
   - In line 565, the acceleration is computed as:
     `p_dot = (Tx + cross_x - tau_gyro_x - dampingCoeff * p_in) / Jx;`
   - Substituting `cross_x` into `p_dot`:
     $$\dot{p} = \frac{T_x + (J_z - J_y) q r - \dots}{J_x}$$
   - This has positive $(J_z - J_y)$, which is $- (J_y - J_z) q r$. This is the exact negative of the physical Coriolis torque.
   - Furthermore, in the asymmetric branch of the same file (line 576):
     `A += (Jy - Jz) * q_in * r_in + ...`
     which yields $\dot{p} = \frac{T_x + (J_y - J_z) q r}{J_x}$.
   - Thus, the multirotor branch in Widget 3 is physically inverted with respect to the asymmetric branch, Topic 3 textbook derivations, and the project test oracle in `verify_textbook_and_widgets.py:690`.

3. **Connecting Step 1 & 2 to Safety & Blast Radius**:
   - When a student tests gyroscopic precession and simultaneous multi-axis rates ($q \neq 0, r \neq 0$), the airframe's simulated roll acceleration will exhibit unphysical positive feedback or reversed damping compared to actual flight test telemetry.
   - Because this project serves as an authoritative undergraduate aeronautical textbook and interactive laboratory, this algebraic discrepancy constitutes a genuine bug requiring correction.

4. **Assessing Solvers & Offline Resilience (Observations 1.3, 1.4, 1.5, 1.6)**:
   - The RK4 integrator, CARE Riccati solver, and Moore-Penrose pseudo-inverse allocation engines perform with outstanding numerical stability, convergence, and singularity protection under high stress.
   - The test suite `verify_textbook_and_widgets.py` passes 100%.

---

## 3. Caveats

- **Scope Boundary**: As Challenger 2, review was restricted to simulation engines, mathematical accuracy, widget JS logic, offline styling, and project test verification. No modifications were made to the implementation code directly, per reviewer constraints.
- **Visual Rendering in Non-Browser Runtimes**: Canvas 2D rasterization was evaluated via DOM inspection and headless AST analysis. Actual visual GPU rendering depends on client browser rendering engines.
- **No Other Caveats**: All numerical tests were executed against exact SciPy and NumPy baselines.

---

## 4. Conclusion & Actionable Recommendation

**Verdict**: `REQUEST_CHANGES`

### Required Changes for Author / Worker:
In `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html`:
Replace lines 560–562:
```javascript
          if (enableCrossTerms) {
            cross_x = (Jy - Jz) * q_in * r_in;
            cross_y = (Jz - Jx) * p_in * r_in;
            cross_z = (Jx - Jy) * p_in * q_in;
          }
```
*(Swapping $J_z - J_y \to J_y - J_z$, $J_x - J_z \to J_z - J_x$, and $J_y - J_x \to J_x - J_y$ ensures consistency with line 565 `Tx + cross_x`, the fixed-wing branch lines 576–578, and `verify_textbook_and_widgets.py:690`)*.

Optional Enhancement:
In `widget_3_rigid_body_dynamics.html` line 120 and `widget_5_cascaded_flight_control.html` line 132, add `min-height: 380px; aspect-ratio: 4/3;` (and `16/9`) into inline CSS style blocks to guarantee canvas dimensions if CDN Tailwind is completely offline.

---

## 5. Verification Method

To independently reproduce and verify this finding:

1. **Verify Sign Inversion Empirically**:
   Inspect line 560 vs line 576 in `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html`:
   - Line 560: `cross_x = (Jz - Jy) * q_in * r_in`
   - Line 576: `A += (Jy - Jz) * q_in * r_in`
   - Line 690 of `modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py`:
     `cross_coupling_torque = (Jy - Jz) * q * r`

2. **Run Authoritative Test Suite**:
   ```powershell
   python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py
   python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py --self-test --verbose
   ```

3. **Run CARE Stress Test**:
   ```powershell
   python modules/EEEE4138_aerial_robotics/scripts/stress_care_lqr.py
   ```
   Confirm max absolute error $< 1.7 \times 10^{-13}$ across nominal, min, and max UI configurations.

4. **Run Matrix Allocation & Failure Stress Test**:
   ```powershell
   python modules/EEEE4138_aerial_robotics/scripts/stress_allocation.py
   ```
   Confirm 100% graceful handling of single and double motor failures across all airframe configurations.
