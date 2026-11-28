# T5 worked examples

The picture, the equations and the answer shapes are in [T5_control_lab.html](T5_control_lab.html). This page is for practising the steps.
Sources: T5-I and T5-II slides (printed slide numbers), Tutorial 4 (= T5-I) and Tutorial 5 (= T5-II) official solutions. Every number has been recomputed. *(added)* = not from the slides.
Conventions throughout: $z$ is positive **down**, positive pitch is nose-up, $g = 9.81$, angles in radians.

## Facts card

| What | Equation | Slide |
|---|---|---|
| Vertical plant | $m\ddot z = mg - T$ | T5-I sl.4 |
| Hover | $T = mg$, $w = 0$. Any constant $z$ works | sl.5 |
| Linearise | $\delta T \approx 2k_T\bar\Omega\,\delta\Omega$ (drop $k_T\delta\Omega^2$) | sl.11 |
| Acceleration command | $T_{cmd} = m(g - u_z)$ ⇒ $\ddot z = u_z$, i.e. $1/s^2$ | sl.14 |
| PD | $u_z = k_p e + k_d\dot e$, $e = z_d - z$, $\dot e = -\dot z$ for a constant target | sl.15 |
| Gains | $\ddot e + k_d\dot e + k_p e = 0$ ⇒ $k_p = \omega_n^2\ [\text{s}^{-2}]$, $k_d = 2\zeta\omega_n\ [\text{s}^{-1}]$ | sl.18 |
| Settling (2 %) | $t_s \approx 4/(\zeta\omega_n)$ | sl.24 |
| PD offset | $\ddot z = u_z + d$ ⇒ $e_{ss} = -d/k_p$ | sl.26 |
| PID | $s^3 + k_d s^2 + k_p s + k_i$, stable iff $0 < k_i < k_d k_p$ | sl.29 |
| Motor | $\Omega/\Omega_{cmd} = 1 - e^{-t/\tau_m}$ (95 % at $3\tau_m$) | sl.39 |
| Motor lag + PD | $\tau_m s^3 + s^2 + k_d s + k_p$, stable iff $k_d > \tau_m k_p$ | sl.40 |
| Tilt → horizontal | $\ddot x \approx -g\theta$, so $\theta_d = -u_x/g$ | T5-II sl.9–10 |
| Outer law | $u_x = \ddot x_d + k_p e_x + k_d\dot e_x$ | sl.10 |
| Inner law | $\alpha_{cmd} = k_\theta e_\theta - k_d q$, $M_{\theta} = J\alpha_{cmd}$; torque gains $K = Jk$ | sl.12–13 |
| Tilted thrust | $T_{cmd} = m(g - u_z)/(\cos\phi\cos\theta)$ | sl.20 |
| State space | $x = [\delta z, w]$, $A = \begin{bmatrix}0&1\\0&0\end{bmatrix}$, $B = [0;1]$ for $v_c$, $B_T = [0;-1/m]$ for $\delta T$ | sl.30–33 |
| Ranks | $[B\ AB]$ controllability, $[C;\ CA]$ observability | sl.35–36 |
| Pole placement | $A - BK = \begin{bmatrix}0&1\\-k_1&-k_2\end{bmatrix}$ → $s^2 + k_2 s + k_1$ | sl.37–39 |
| Back to thrust | $\delta T = -m v_c$, $T_{cmd} = mg + \delta T$ | sl.40 |

**The one sign rule:** $u_z < 0$ means accelerate **up**. $\dot z > 0$ means moving **down** right now. Forward ($u_x > 0$) needs $\theta_d < 0$ (nose **down**).

---

## 1 · Hover and acceleration (Tutorial 4 Q1)

$m = 1.60$ kg. From $m\ddot z = mg - T$ we get $T = m(g - \ddot z)$.

(a) $T_{hover} = 1.60(9.81) = 15.696 \approx 15.7$ N.

(b) $\ddot z = 0$, but $w$ stays at $+0.30$ m/s. Thrust = weight stops the *acceleration*, not the motion, so the drone keeps **descending** at a constant speed.

(c) Upward 1.20 m/s² means $\ddot z = -1.20$:
$$T = 1.60\,[9.81 - (-1.20)] = 17.616 \approx 17.6\ \text{N}$$

(Slide twin, sl.6–7: $m = 1.50$ gives 14.7 N, and $1.00$ m/s² up gives 16.2 N.)

## 2 · Linearise one rotor (Tutorial 4 Q2)

$k_T = 2.00\times10^{-5}$, $\bar\Omega = 400$, $\delta\Omega = 20$ rad/s.

$$T = k_T(\bar\Omega + \delta\Omega)^2 = k_T\bar\Omega^2 + 2k_T\bar\Omega\,\delta\Omega + k_T\delta\Omega^2 \ \Rightarrow\ \delta T = 2k_T\bar\Omega\,\delta\Omega + k_T\delta\Omega^2 \approx 2k_T\bar\Omega\,\delta\Omega$$

- Approximate: $2(2\times10^{-5})(400)(20) = 0.320$ N.
- Exact: $(2\times10^{-5})(420^2 - 400^2) = 0.328$ N.
- Neglected term: $k_T\delta\Omega^2 = 0.00800$ N. The linear estimate **underestimates** the increase. $\bar T = 3.20$ N, and the exact final thrust is 3.528 N.

## 3 · PD design and a climb command (Tutorial 4 Q3)

(a) Constant target: $\ddot e = -\ddot z = -u_z = -(k_p e + k_d\dot e)$, so
$$\ddot e + k_d\dot e + k_p e = 0$$

(b) Match $s^2 + k_d s + k_p$ to $s^2 + 2\zeta\omega_n s + \omega_n^2$ with $\omega_n = 3.00$ and $\zeta = 0.800$:
$$k_p = 3^2 = 9.00\ \text{s}^{-2},\qquad k_d = 2(0.800)(3) = 4.80\ \text{s}^{-1}$$

(c) $m = 1.60$, $z_d = -2.00$, $z = -1.80$, $\dot z = +0.10$:
$$\begin{aligned}
e &= -2.00 - (-1.80) = -0.200\ \text{m}\\
\dot e &= 0 - 0.10 = -0.100\ \text{m/s}\\
u_z &= 9(-0.200) + 4.8(-0.100) = -2.28\ \text{m/s}^2\\
T &= 1.60\,(9.81 + 2.28) = 19.344 \approx 19.3\ \text{N}
\end{aligned}$$

(d) $u_z < 0$, so it accelerates **up**. $\dot z > 0$, so it is still **descending** at this instant, but slowing down. It does not move upward immediately.

(Slide twin, sl.19–21: $\omega_n = 4$, $\zeta = 0.75$ → $16$, $6$, poles $-3.00 \pm j2.65$; $z_d = -1.00$, $z = -0.80$ → $u_z = -3.80$, $T = 20.4$ N.)

## 4 · Offset and integral action (Tutorial 4 Q4)

$\ddot z = u_z + d$, with $d = +0.45$ m/s², $k_p = 9.00$, $k_d = 4.80$.

(a) $\ddot e + k_d\dot e + k_p e = -d$. At steady state $\ddot e = \dot e = 0$:
$$e_{ss} = -\frac{d}{k_p} = -\frac{0.45}{9} = -0.0500\ \text{m}$$
$e = z_d - z < 0$ means $z > z_d$, so it sits 5 cm **below** the target.

(b) At a steady state with $e = 0$, the integral term supplies $k_i\xi = -d$. For $k_i = 10$: $\xi = -0.45/10 = -0.0450$ m s.

(c) $k_d k_p = 4.80 \times 9.00 = 43.2$, and $0 < 10.0 < 43.2$, so the ideal no-lag PID loop is stable.

(d) Windup: while the actuator is saturated, the error persists and $\xi$ keeps growing. When the actuator comes out of saturation, the large $\xi$ causes overshoot. Fixes: conditional integration or back-calculation (sl.30).

## 5 · Motor lag (Tutorial 4 Q5)

(a) $\tau_m = 0.020$ s, $t = 0.060$ s $= 3\tau_m$: $1 - e^{-3} = 0.9502 \approx 95.0\%$.

(b)–(c) $k_p = 100$, $k_d = 3.00$. The characteristic polynomial is $\tau s^3 + s^2 + k_d s + k_p$.
- $\tau = 0.020$: $\tau k_p = 2.00 < 3.00$ → **stable**.
- $\tau = 0.050$: $\tau k_p = 5.00 > 3.00$ → **unstable**.

(d) No. Stability says nothing about overshoot, settling or tracking error. Also check limits, noise and neglected dynamics (sl.42).

(Slide twin, sl.41–42: $k_p = 64$, $k_d = 11.2$; $\tau = 0.020$ gives $1.28 < 11.2$, stable; $\tau = 0.200$ gives $12.8 > 11.2$, unstable.)

## 6 · Cascade: position error → pitch moment (Tutorial 5 Q1–Q2)

**Q1 (words).** The outer loop uses position and velocity to request an acceleration, and from it a tilt. The inner loop uses attitude and rates to request moments. A quadrotor's thrust is along body $-z$, so it can only push sideways by **tilting** (sl.4–5). The outer design assumes the requested tilt arrives promptly, so the inner loop must be faster (sl.16).

**Q2a.** $e_x = +0.0400$, $\dot e_x = -0.0250$, $\ddot x_d = 0$, $k_p = 9.00$, $k_d = 4.80$:
$$u_x = 0 + 9(0.0400) + 4.8(-0.0250) = 0.360 - 0.120 = +0.240\ \text{m/s}^2$$
$$\theta_d = -\frac{0.240}{9.81} = -0.0245\ \text{rad} \approx -1.40^\circ$$
Negative pitch is nose-down, which directs thrust towards $+x$.

**Q2b.** $\theta = 0$, $q = +0.0500$, $J = 0.00800$, $k_\theta = 144$, $k_d = 19.2$:
$$\begin{aligned}
\alpha_{cmd} &= 144(-0.02446) - 19.2(0.0500) = -3.52 - 0.96 = -4.48\ \text{rad/s}^2\\
M_{\theta,cmd} &= J\alpha_{cmd} = 0.008(-4.48) = -0.0359\ \text{N m}\\
K_\theta &= Jk_\theta = 1.152\ \text{N m/rad},\qquad K_d = Jk_d = 0.1536\ \text{N m s/rad}
\end{aligned}$$

(Slide twin, sl.17–19: $J = 0.005$, $\omega_n = 25$, $\zeta = 0.7$ → $k_\theta = 625$, $k_d = 35$, $K = 3.125$, $K_d = 0.175$; motor check $35 > 0.02 \times 625 = 12.5$. $e_x = 0.02$, $k_p = 16$ → $u_x = 0.320$, $\theta_d = -0.0326$ rad $= -1.87^\circ$, $M = -0.102$ N m.)

## 7 · Thrust needed while tilted (T5-II sl.20–21)

The vertical component is $T\cos\phi\cos\theta$. With $\phi = 0$ and zero vertical acceleration, $T = mg/\cos\theta$. At $20^\circ$: $1/\cos 20^\circ = 1.064$, so about **6.4 %** more thrust.

## 8 · State space (Tutorial 5 Q3–Q5)

**Q3a.** $m = 2.00$, input $\delta T$. The rows are $\delta\dot z = w$ and $\dot w = -\delta T/m$:
$$A = \begin{bmatrix}0&1\\0&0\end{bmatrix},\quad B_T = \begin{bmatrix}0\\-0.500\end{bmatrix},\quad C = \begin{bmatrix}1&0\end{bmatrix},\quad D = 0$$
Thrust changes velocity through $-1/m$ (more thrust → upward, i.e. negative). Position responds through velocity.

**Q3b.**
$$AB_T = \begin{bmatrix}-0.500\\0\end{bmatrix},\quad [B_T\ AB_T] = \begin{bmatrix}0&-0.500\\-0.500&0\end{bmatrix}\ (\text{rank }2),\quad \begin{bmatrix}C\\CA\end{bmatrix} = \begin{bmatrix}1&0\\0&1\end{bmatrix}\ (\text{rank }2)$$
The system is controllable and observable. The zero in $B_T$ does **not** make position uncontrollable: the input reaches position through $AB_T$.

**Q4a.** Input $v_c$, so $B = [0;1]$. Poles $-2$, $-5$:
$$(s+2)(s+5) = s^2 + 7s + 10 \ \Rightarrow\ K = [10.0\ \ 7.00],\quad A - BK = \begin{bmatrix}0&1\\-10&-7\end{bmatrix}$$

**Q4b.** $r = -0.300$, $\delta z = -0.100$, $w = +0.0500$, $m = 2.00$:
$$\begin{aligned}
v_c &= 10(-0.300 + 0.100) - 7(0.0500) = -2.35\ \text{m/s}^2\quad(\text{up})\\
\delta T &= -m v_c = +4.70\ \text{N}\\
T_{cmd} &= mg + \delta T = 19.62 + 4.70 = 24.32\ \text{N}
\end{aligned}$$

**Q5.** (a) For a constant target, $r - \delta z = z_d - z$ and $w = \dot z$, so the laws match when $k_1 = k_p$ and $k_2 = k_d$. (b) No. Equivalent laws give identical responses. (c) No. State feedback can be built as cascaded channels or as one combined controller.

(Slide twins: sl.39–40, poles $-2$, $-3$ → $K = [6\ 5]$; $\delta z = 0.1$, $w = 0.2$ → $v_c = -1.60$, $T = 17.115$ N. sl.43–44, poles $-3$, $-4$ → $K = [12\ 7]$; $r = -0.2$, $m = 1$ → $v_c = -2.40$, $T = 12.21$ N.)

---

**Flag (Lab 3 guide, AI-written):** the climb prediction says $T_{cmd} = 2.505(9.81 + 0.5) = 25.822$ N. Recomputed, it's **25.827** N. The +1.25 N step is right. This is minor, but use the recomputed value if you quote it in the CW.
