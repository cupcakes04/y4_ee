# T4 worked examples

Picture ↔ equation ↔ answer shape: [T4_forces_lab.html](T4_forces_lab.html). This page is for practising the steps.
Sources: T4 slides (printed slide numbers), Tutorial 3 + official solutions. Every number was recomputed. *(added)* = not from the slides.

## Facts card

| What | Equation | Slide |
|---|---|---|
| Total loads | $\mathbf F = \mathbf F_g + \mathbf F_a + \mathbf F_p$, $\ \mathbf M = \mathbf M_a + \mathbf M_p (+\text{gyro})$. Gravity has **no moment** about the CoM | sl.4 |
| Gravity, body axes | $\mathbf F_g^b = (R_b^n)^T[0\ 0\ mg]^T$ (T3 again) | sl.5 |
| Drag (low speed) | $\mathbf F_d = -c\,\mathbf v_{rel}$ (CW: $c_{drag} = 0.25$ N s/m), opposite to the air-relative motion | sl.6 |
| Thrust, rotor torque | $T_i = k_T\Omega_i^2$, $\ Q_i = k_M\Omega_i^2$ | sl.11–14 |
| Torque in terms of thrust | $M_{z,i} = \sigma_i k_{MT} T_i$, $\ k_{MT} = k_M/k_T$ [m] | sl.15 |
| One rotor's moment | $\mathbf M_i = \mathbf r_i\times\mathbf F_i + \sigma_i k_{MT}T_i\,\mathbf e_z$, $\ \mathbf r_i\times\mathbf F_i = [-y_iT_i,\ x_iT_i,\ 0]^T$ | Tut 3 Q2 |
| Allocation | $[F_z\ M_x\ M_y\ M_z]^T = A\,\mathbf t$, column $i$ = $[-1,\ -y_i,\ x_i,\ \sigma_i k_{MT}]^T$; $\ \mathbf t = A^{-1}(\cdot)$, $\ \Omega_i = \sqrt{T_i/k_T}$, check $0\le T_i\le T_{max}$ | sl.21, 25, 27 |
| Gyroscopic (not the same as reaction torque) | $\mathbf M_{gyro} = -\boldsymbol\omega_b\times\mathbf h_r = [-qH,\ pH,\ 0]^T$, $\ H = J_r\big(\textstyle\sum s_i\Omega_i\big)$, with $s_i = \pm1$ for spin about $\pm z$ (⚠ $s_i$ is the rotor's own spin, so $s_i = -\sigma_i$: a CCW rotor spins about −z, *added*). Zero if the speeds are equal and the rotors counter-rotate. Excluded in the CW baseline | sl.8–9 |

**The two effects:** a rotor's **thrust**, through its **position**, gives roll and pitch ($M_x, M_y$). Its **drag torque**, through its **spin**, gives yaw ($M_z$).
Sign check in words: front rotor up → $M_y>0$ (nose up). Left rotor up → $M_x>0$ (left side up, roll right). CCW rotor ($\sigma=+1$) up → $M_z>0$ (nose right).

---

## 1 · Thrust and reaction torque (Tutorial 3 Q1)

$\Omega = 500$ rad/s, $k_T = 2.00\times10^{-5}$, $k_M = 4.00\times10^{-7}$.

$$T = (2.00\times10^{-5})(500)^2 = 5.00\ \text{N},\qquad Q = (4.00\times10^{-7})(500)^2 = 0.100\ \text{N m}$$

(b) $\Omega^2 = T/k_T$, so $Q = \dfrac{k_M}{k_T}T = k_{MT}T$ with $k_{MT} = \dfrac{4.00\times10^{-7}}{2.00\times10^{-5}} = 0.0200$ m (N m / N = m).

(c) Doubling $\Omega$ quadruples both: $T = 20.0$ N, $Q = 0.400$ N m.

(d) No. Reaction torque balances the motor drive against blade drag, and it exists even when the drone is still. A gyroscopic moment needs the body to rotate and tilt the rotor's angular momentum.

## 2 · + quadrotor: derive the loads (Tutorial 3 Q2)

Positions: 1 $(l,0)$, 2 $(0,l)$, 3 $(-l,0)$, 4 $(0,-l)$. $\sigma = [+1,-1,+1,-1]$.

$$\mathbf r\times\mathbf F = \begin{bmatrix}x\\y\\0\end{bmatrix}\times\begin{bmatrix}0\\0\\-T\end{bmatrix} = \begin{bmatrix}y(-T) - 0\cdot0\\ 0\cdot0 - x(-T)\\ x\cdot0 - y\cdot0\end{bmatrix} = \begin{bmatrix}-yT\\ xT\\ 0\end{bmatrix}$$

Sum over the four rotors (only rotors with $y\neq0$ enter $M_x$, only those with $x\neq0$ enter $M_y$):

$$\begin{aligned}
F_z &= -(T_1+T_2+T_3+T_4)\\
M_x &= -(l)T_2 - (-l)T_4 = l(T_4 - T_2)\\
M_y &= (l)T_1 + (-l)T_3 = l(T_1 - T_3)\\
M_z &= k_{MT}(T_1 - T_2 + T_3 - T_4)
\end{aligned}$$

(b) All $T_i = 6.00$ N: $F_z = -24.0$ N, $M_x = M_y = M_z = 0$. This is propulsion only; gravity is separate.

(c) $T_1 + \delta$, $T_3 - \delta$: $\ \Delta F_z = -(\delta - \delta) = 0$, $\ \Delta M_y = l[\delta - (-\delta)] = 2l\delta$, $\ \Delta M_z = k_{MT}(\delta - \delta) = 0$. A pure pitch change, which is why opposite rotors spin the same way (sl.19).

## 3 · Allocation and limits (Tutorial 3 Q3)

$l = 0.250$ m, $k_{MT} = 0.0200$ m, $k_T = 2.00\times10^{-5}$, $T_{max} = 8.00$ N. Demand: $F_z = -24.0$, $M_x = 0$, $M_y = +0.500$, $M_z = 0$.

$$\begin{aligned}
M_x = 0 &\ \Rightarrow\ T_2 = T_4\\
M_z = 0 &\ \Rightarrow\ T_1 + T_3 = T_2 + T_4\\
-F_z = 24.0 &\ \Rightarrow\ \text{each pair} = 12.0\ \text{N}\\
M_y/l = 0.500/0.250 &\ \Rightarrow\ T_1 - T_3 = 2.00\ \text{N}
\end{aligned}
\qquad\Rightarrow\qquad T_1 = \frac{12+2}{2} = 7.00,\quad T_3 = \frac{12-2}{2} = 5.00,\quad T_2 = T_4 = 6.00\ \text{N}$$

(b) Speeds, using the non-negative root:

$$\Omega_1 = \sqrt{\frac{7.00}{2.00\times10^{-5}}} = 592,\qquad \Omega_2 = \Omega_4 = \sqrt{\frac{6.00}{2.00\times10^{-5}}} = 548,\qquad \Omega_3 = \sqrt{\frac{5.00}{2.00\times10^{-5}}} = 500\ \text{rad/s}$$

(c) All within $0 \le T_i \le 8.00$ N: feasible.

(d) $M_y = 2.00$: $T_1 - T_3 = 2.00/0.250 = 8.00$, so $T_1 = 10.0$, $T_3 = 2.00$, $T_2 = T_4 = 6.00$ N. Since **$T_1 = 10.0 > 8.00$**, it's infeasible.

## 4 · X quadrotor (Tutorial 3 Q4)

Positions: 1 $(d,-d)$ FL, 2 $(d,d)$ FR, 3 $(-d,d)$ RR, 4 $(-d,-d)$ RL, with $d = l/\sqrt2$.

$$\begin{aligned}
M_x &= -\textstyle\sum y_iT_i = -(-d)T_1 - dT_2 - dT_3 - (-d)T_4 = d(T_1 - T_2 - T_3 + T_4)\\
M_y &= \textstyle\sum x_iT_i = d(T_1 + T_2 - T_3 - T_4)\\
M_z &= k_{MT}(T_1 - T_2 + T_3 - T_4)
\end{aligned}$$

(b) The moment about x uses the distance **from the x axis**, which is $|y| = l\cos45° = l/\sqrt2$. The arm $l$ runs along the diagonal.

(c) $\mathbf t = [\delta,\ \delta,\ -\delta,\ -\delta]$: $\ F_z = 0$, $\ M_x = d(\delta - \delta + \delta - \delta) = 0$, $\ M_z = k_{MT}(\delta - \delta - \delta + \delta) = 0$, $\ M_y = d(4\delta) = 4d\delta$. Only pitch changes.
In X, every rotor appears in **both** the roll and pitch rows (in +, each rotor appears in only one of them).

## 5 · Fixed-wing lift and drag (Tutorial 3 Q5)

$m = 3.00$ kg, $\rho = 1.20$ kg/m³, $S = 0.500$ m². Level flight: $L = mg = 3.00(9.81) = 29.43$ N.

$$C_L = \frac{2mg}{\rho V^2 S}:\qquad C_L(10) = \frac{58.86}{1.20(100)(0.500)} = \frac{29.43}{30.0} = 0.981,\qquad C_L(20) = \frac{29.43}{120} = 0.245$$

(b) Doubling V: parasite $\times 4$ → $2.00 \to 8.00$ N. Induced $\div 4$ → $8.00 \to 2.00$ N. Total is **10.0 N at both speeds**.

(c) At fixed lift, a higher speed needs a lower $C_L$ (a smaller α), and induced drag goes with lift squared at fixed speed and geometry (sl.45). So it falls.

*(added)* $D(V) = 2.00(V/10)^2 + 8.00(10/V)^2$ is smallest where the two terms are equal: $V = 10\sqrt2 = 14.1$ m/s, giving $D = 8.00$ N.

**Angles (sl.35):** $\alpha = \theta + i_w - \gamma$. All are in the vertical plane: θ is body vs horizontal, γ is flight path vs horizontal, $i_w$ is chord vs body (fixed), and α is chord vs oncoming air. With θ = 8°, $i_w$ = 2°, γ = 3° *(invented)*: α = 7°.

**NACA 2415 (sl.31):** 2% max camber, at 40% chord, 15% max thickness.

## 6 · Hexarotor allocation (Tutorial 3 Q6, homework)

$\beta = [-30°, 30°, 90°, 150°, 210°, 270°]$, $x_i = l\cos\beta_i$, $y_i = l\sin\beta_i$, $\sigma = [+,-,+,-,+,-]$. Let $a = l/2$, $b = \sqrt3\,l/2$, $k = k_{MT}$.

| Rotor | β | $(x, y)$ | column $[-1,\ -y,\ x,\ \sigma k]$ |
|---|---|---|---|
| 1 | −30° | $(b, -a)$ | $[-1,\ a,\ b,\ k]$ |
| 2 | 30° | $(b, a)$ | $[-1,\ -a,\ b,\ -k]$ |
| 3 | 90° | $(0, l)$ | $[-1,\ -l,\ 0,\ k]$ |
| 4 | 150° | $(-b, a)$ | $[-1,\ -a,\ -b,\ -k]$ |
| 5 | 210° | $(-b, -a)$ | $[-1,\ a,\ -b,\ k]$ |
| 6 | 270° | $(0, -l)$ | $[-1,\ l,\ 0,\ -k]$ |

$$A_{hex} = \begin{bmatrix}-1&-1&-1&-1&-1&-1\\ a&-a&-l&-a&a&l\\ b&b&0&-b&-b&0\\ k&-k&k&-k&k&-k\end{bmatrix}\quad(4\times6,\ \text{sl.27})$$

(c) 4 equations, 6 unknowns: $A$ isn't square, so there's no ordinary inverse. The rank is 4, so solutions exist, and there are infinitely many (A2: a wide matrix).

(d) Equal thrusts $T_i = 24.0/6 = 4.00$ N give $F_z = -24.0$ and zero moments (each moment row sums to 0). $\Omega_i = \sqrt{4.00/2.00\times10^{-5}} = 447$ rad/s.
Another solution, $[4.2,\ 3.9,\ 3.9,\ 4.2,\ 3.9,\ 3.9]$ N, gives the same four outputs, so the allocation isn't unique. A practical allocator picks one feasible solution, e.g. min-norm (sl.28).
