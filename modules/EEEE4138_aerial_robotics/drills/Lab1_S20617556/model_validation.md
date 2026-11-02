# EEEE4138 Aerial Robotics — Practical 1: Vertical Dynamics and Simulink
## Model Validation and Comparison Report

* **Student ID:** S20617556
* **Assigned Unloaded Mass ($m_0$):** $1.31\text{ kg}$
* **Nominal Mass ($m_{\text{nom}} = 1.50 \times m_0$):** $1.965\text{ kg}$
* **Nominal Hover Thrust ($T_{\text{hover}} = m_{\text{nom}} \times g$):** $19.27665\text{ N}$
* **Maximum Actuator Thrust ($T_{\max} = 2 \times T_{\text{hover}}$):** $38.5533\text{ N}$
* **Gravity ($g$):** $9.81\text{ m/s}^2$
* **Initial Position ($z_0$):** $0\text{ m}$ (coordinate $z$ is positive downwards)
* **Simulation Duration:** $t = 2.0\text{ s}$

---

## 1. Governing Equations & Analytical Formulation

From Newton’s Second Law for vertical motion (with downward coordinate $z$ and downward velocity $w$ defined as positive):

$$\Sigma F_z = m g - T$$

$$a(t) = \frac{d^2z}{dt^2} = g - \frac{T}{m}$$

For constant thrust $T$ and constant mass $m$, acceleration $a$ is constant. Integrating with respect to time:

$$w(t) = \int_0^t a \, d\tau = w_0 + a \cdot t$$

$$z(t) = \int_0^t w(\tau) \, d\tau = z_0 + w_0 \cdot t + \frac{1}{2} a \cdot t^2$$

---

## 2. Table 2: Validation Test Conditions & Analytical Reference Values

| Test | Description | Simulation Commands / Overrides | Analytical Acceleration $a$ ($\text{m/s}^2$) | Expected Velocity $w(2)$ ($\text{m/s}$) | Expected Position $z(2)$ ($\text{m}$) |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | **Hover** | `T_cmd = T_hover; w0 = 0;` | $9.81 - \frac{19.27665}{1.965} = \mathbf{0.000}$ | $0 + 0(2) = \mathbf{0.000}$ | $0 + 0 + 0.5(0)(4) = \mathbf{0.000}$ |
| **2** | **Free Fall** | `T_cmd = 0; w0 = 0;` | $9.81 - \frac{0}{1.965} = \mathbf{9.810}$ | $0 + 9.81(2) = \mathbf{19.620}$ | $0 + 0 + 0.5(9.81)(4) = \mathbf{19.620}$ |
| **3** | **Extra Thrust** | `T_cmd = 1.10*T_hover; w0 = 0;` | $9.81 - 1.10(9.81) = \mathbf{-0.981}$ | $0 - 0.981(2) = \mathbf{-1.962}$ | $0 + 0 + 0.5(-0.981)(4) = \mathbf{-1.962}$ |
| **4** | **Existing Descent** | `T_cmd = T_hover; w0 = 0.40;` | $9.81 - 9.81 = \mathbf{0.000}$ | $0.40 + 0(2) = \mathbf{0.400}$ | $0 + 0.40(2) + 0 = \mathbf{0.800}$ |

---

## 3. Table 3: Predicted vs Simulated Results Comparison

Results extracted directly from the logged simulation runs in `results/test[1-4].mat` at the completion time $t = 2.00\text{ s}$:

| Test | Predicted $w(2)$, $z(2)$ | Simulated $w(2)$, $z(2)$ | Difference ($\Delta w, \Delta z$) | Physical Explanation & Solver Notes |
| :---: | :--- | :--- | :---: | :--- |
| **1. Hover** | $w(2) = 0.0000\text{ m/s}$<br>$z(2) = 0.0000\text{ m}$ | $w(2) = 0.0000\text{ m/s}$<br>$z(2) = 0.0000\text{ m}$ | $\Delta w = 0.0000$<br>$\Delta z = 0.0000$ ($0.0\%$) | **Exact equilibrium:** Thrust matches weight identically ($T_{\text{cmd}} = m g$). With zero initial velocity, acceleration remains zero throughout, and the vehicle maintains a stationary hover. |
| **2. Free Fall** | $w(2) = 19.6200\text{ m/s}$<br>$z(2) = 19.6200\text{ m}$ | $w(2) = 19.6200\text{ m/s}$<br>$z(2) = 19.6200\text{ m}$ | $\Delta w = 0.0000$<br>$\Delta z = 0.0000$ ($0.0\%$) | **Pure gravitational acceleration:** Zero thrust ($T = 0$) results in constant downward acceleration $a = g = 9.81\text{ m/s}^2$. Velocity scales linearly, and displacement follows a clean parabola. *(Note: at penultimate solver step $t = 1.9980\text{ s}$, $z = 19.5813\text{ m}$; reaches exactly $19.6200\text{ m}$ at $t = 2.00\text{ s}$)*. |
| **3. Extra Thrust** | $w(2) = -1.9620\text{ m/s}$<br>$z(2) = -1.9620\text{ m}$ | $w(2) = -1.9620\text{ m/s}$<br>$z(2) = -1.9620\text{ m}$ | $\Delta w = 0.0000$<br>$\Delta z = 0.0000$ ($0.0\%$) | **Net upward acceleration:** Thrust exceeds weight by $10\%$ ($T = 1.10 T_{\text{hover}}$), giving net upward acceleration $a = -0.981\text{ m/s}^2$. Negative position and velocity represent climb above the starting launch altitude. *(Note: at penultimate solver step $t = 1.9931\text{ s}$, $w = -1.9552\text{ m/s}$; reaches exactly $-1.9620\text{ m/s}$ at $t = 2.00\text{ s}$)*. |
| **4. Existing Descent** | $w(2) = 0.4000\text{ m/s}$<br>$z(2) = 0.8000\text{ m}$ | $w(2) = 0.4000\text{ m/s}$<br>$z(2) = 0.8000\text{ m}$ | $\Delta w = 0.0000$<br>$\Delta z = 0.0000$ ($0.0\%$) | **Dynamic equilibrium / Steady descent:** Thrust equals weight ($a = 0$), but initial velocity is $w_0 = 0.40\text{ m/s}$. Because net force is zero, velocity does not change, resulting in linear downward displacement $z(t) = w_0 t$. |

---

## 4. In-Depth Differences & Numerical Analysis

### 4.1 Numerical Solver Precision vs. Discrete Step Sampling
* The continuous Simulink plant is solved using the variable-step **`ode45`** (Dormand-Prince Runge-Kutta) solver with maximum step size $\Delta t_{\max} = 0.01\text{ s}$, relative tolerance $10^{-6}$, and absolute tolerance $10^{-8}$.
* Because the differential equation is linear with constant inputs ($\ddot{z} = \text{const}$), the polynomial integration order of `ode45` integrates the state without algorithmic truncation drift. 
* At the exact terminal time $t = 2.0000\text{ s}$, the simulated outputs match the analytical predictions to machine precision:
  * **Test 1:** Error $= 0.0000\text{ m/s}$, $0.0000\text{ m}$
  * **Test 2:** Error $= 0.0000\text{ m/s}$, $0.0000\text{ m}$
  * **Test 3:** Error $= 0.0000\text{ m/s}$, $0.0000\text{ m}$
  * **Test 4:** Error $= 0.0000\text{ m/s}$, $0.0000\text{ m}$

* **Explanation of Penultimate Logging Discrepancies:**  
When inspecting the logged time arrays prior to the final boundary hit, the variable-step solver took its second-to-last evaluations at slightly varied time points:

* **Test 2 (Free Fall)**, at $t = 1.998027\text{ s}$:  
  $z(1.998027) = \frac{1}{2}(9.81)(1.998027)^2 = 19.5813\text{ m}$. This explains the raw value of $19.5813\text{ m}$ recorded prior to the exact $t = 2.0000\text{ s}$ endpoint ($19.6200\text{ m}$).

* **Test 3 (Extra Thrust)**, at $t = 1.993087\text{ s}$:  
  $w(1.993087) = -0.981 \times 1.993087 = -1.95522\text{ m/s}$. This accounts for the interim value of $-1.95522\text{ m/s}$ before the final step evaluated at $-1.9620\text{ m/s}$.
---

## 5. Lab Discussion Questions

### 5.1 Why does the UAV continue to descend in Test 4 despite zero net force?
* **Newton’s First Law of Motion** states that an object continues in its state of rest or uniform motion in a straight line unless acted upon by a net external force.
* In Test 4, $T_{\text{cmd}} = T_{\text{hover}} = m g$, meaning:
  $$\Sigma F_z = m g - T = 0 \implies a = \frac{\Sigma F_z}{m} = 0$$
* A net force of zero produces **zero acceleration** ($\frac{dw}{dt} = 0$), not zero velocity. Acceleration governs the *rate of change* of velocity. Since initial velocity was $w_0 = 0.40\text{ m/s}$, the velocity remains constant at $w(t) = 0.40\text{ m/s}$.
* Consequently, position continues to change linearly at a steady descent rate:
  $$z(t) = z_0 + w_0 \cdot t = 0 + 0.40 \cdot t$$
  reaching $z(2) = 0.80\text{ m}$.
* **Distinction between zero acceleration and zero velocity:**  
  * **Zero acceleration ($a = 0$):** Forces are in equilibrium ($\Sigma F = 0$). Momentum is conserved; velocity is invariant ($\dot{w} = 0$).
  * **Zero velocity ($w = 0$):** Kinematic rest ($\dot{z} = 0$). To transition an existing nonzero velocity ($w > 0$) to rest ($w = 0$), a net decelerating force must be applied ($\Sigma F_z < 0$, i.e., $T > m g$) to generate negative acceleration ($a < 0$). Simply balancing weight with hover thrust maintains whatever velocity already exists.

### 5.2 Trajectory Profiles (Linear vs. Quadratic Verification)
1. **Nonzero Constant Acceleration (Tests 2 & 3):**
   * Velocity varies **linearly** with time ($w(t) \propto t$).
   * Position varies **quadratically** with time ($z(t) \propto t^2$), yielding parabolic trajectories.
2. **Zero Acceleration with Initial Velocity (Test 4):**
   * Velocity is **constant** ($w(t) = w_0$).
   * Position varies **linearly** with time ($z(t) \propto t$), yielding a constant-slope straight line.

---

## 6. Generated Position Plots

The simulated position traces recorded in the `results/` folder confirm the theoretical behavior:

| Test | Output Plot | Motion Behavior |
| :---: | :---: | :--- |
| **Test 1: Hover** | `results/test1_position.png` | Flat horizontal line at $z = 0\text{ m}$. |
| **Test 2: Free Fall** | `results/test2_position.png` | Quadratic downward curve reaching $+19.62\text{ m}$. |
| **Test 3: Extra Thrust** | `results/test3_position.png` | Quadratic upward curve reaching $-1.962\text{ m}$ (ascent). |
| **Test 4: Existing Descent** | `results/test4_position.png` | Linear downward ramp from $0\text{ m}$ to $+0.80\text{ m}$. |
