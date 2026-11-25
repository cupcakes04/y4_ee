# T3 worked examples

Picture ↔ equation ↔ answer shape: [T3_dynamics_lab.html](T3_dynamics_lab.html). This page is for practising the steps.
Sources: T3 slides (printed slide numbers), Tutorial 2 + official solutions. Every number was recomputed. *(added)* = not from the slides.

## Facts card

| Block | Equation | Kind | Lab line |
|---|---|---|---|
| Position | $\dot{\mathbf p}^n = R_b^n\,\mathbf v_b$ (sl.27) | kinematics | `pos_dot = R*vb` |
| Translation | $\dot{\mathbf v}_b = \dfrac{\mathbf F^b}{m} - \boldsymbol\omega_b\times\mathbf v_b$ (sl.12) | dynamics | `vb_dot = F/m - cross(omega,vb)` |
| Attitude | $[\dot\phi\ \dot\theta\ \dot\psi]^T = E(\phi,\theta)\,[p\ q\ r]^T$ (sl.28, 38) | kinematics | `euler_dot = E*omega` |
| Rotation | $\dot{\boldsymbol\omega}_b = J^{-1}\big(\mathbf M^b - \boldsymbol\omega_b\times J\boldsymbol\omega_b\big)$ (sl.21) | dynamics | `omega_dot = J\(M - cross(omega,J*omega))` |

- **Kinematics** has no $m, J, F, M$: it just turns one rate into another. **Dynamics** has $F/m$ or $M/J$.
- $\mathbf v_b = [u\ v\ w]^T$ is the velocity **along** the body axes. $\boldsymbol\omega_b = [p\ q\ r]^T$ is the spin rate **about** them.
- **Cross product** (sl.6) and the cyclic rule $\hat x\times\hat y=\hat z,\ \hat y\times\hat z=\hat x,\ \hat z\times\hat x=\hat y$ (reversed order gives a minus):

$$\boldsymbol\omega\times\mathbf v = \begin{bmatrix} q\,w - r\,v\\ r\,u - p\,w\\ p\,v - q\,u\end{bmatrix}
\quad\Rightarrow\quad
\begin{aligned}\dot u &= r v - q w + F_x/m\\ \dot v &= p w - r u + F_y/m\\ \dot w &= q u - p v + F_z/m\end{aligned}\quad\text{(sl.13)}$$

- **Diagonal $J$** (sl.22):

$$\dot p = \frac{M_x + (J_y-J_z)\,q r}{J_x},\qquad \dot q = \frac{M_y + (J_z-J_x)\,p r}{J_y},\qquad \dot r = \frac{M_z + (J_x-J_y)\,p q}{J_z}$$

- **Gravity in body axes** = $(R_b^n)^T[0\ 0\ mg]^T$ = $mg\times$ (row 3 of $R_b^n$) (sl.37):

$$\mathbf F_g^b = mg\begin{bmatrix}-\sin\theta\\ \sin\phi\cos\theta\\ \cos\phi\cos\theta\end{bmatrix}$$

- T3 writes **n** for NED. $R_b^n$ is T2's $R_b^v$.

---

## 1 · Rotating direction (sl.9)

$\mathbf a_b = [1\ 0\ 0]^T$ (fixed along body x), $\boldsymbol\omega_b = [0\ 0\ 2]^T$. The components are fixed, so $\dot{\mathbf a}_b = \mathbf 0$.

$$\Big(\frac{d\mathbf a}{dt}\Big)_n = \dot{\mathbf a}_b + \boldsymbol\omega\times\mathbf a_b = \mathbf 0 + \begin{bmatrix}0\cdot0 - 2\cdot0\\ 2\cdot1 - 0\cdot0\\ 0\cdot0 - 0\cdot1\end{bmatrix} = \begin{bmatrix}0\\2\\0\end{bmatrix}$$

The direction swings toward $+y_b$ at 2 rad/s.

## 2 · Vertical acceleration (sl.15) and Tutorial 2 Q1

**sl.15.** Level, $m = 2.00$ kg, $T = 24.0$ N up. With z down, $F_z = mg - T$:

$$F_z = 2.00(9.81) - 24.0 = 19.62 - 24.0 = -4.38\ \text{N},\qquad \dot w = \frac{-4.38}{2.00} = -2.19\ \text{m/s}^2$$

Negative with z down means **2.19 m/s² upward**. This doesn't tell you whether the UAV is already moving up: $\dot w$ is the change in $w$, not $w$ itself.

**Tutorial 2 Q1.** $m = 1.60$ kg, $T = 18.0$ N.

(a) $\dot z = w,\quad \dot w = g - T/m$

(b) $\dot w = 9.81 - \dfrac{18.0}{1.60} = 9.81 - 11.25 = -1.44\ \text{m/s}^2$, so **upward**.

(c) $w = +0.800$ m/s means it's moving down, and $\dot w < 0$ means it's being pushed up, so it's **descending but slowing down**.

(d) Hover needs **both** $w = 0$ **and** $T = mg = 1.60(9.81) = 15.696$ N.

sl.32: $T = mg$ alone isn't hover. If $w \neq 0$, the UAV keeps moving at a constant $w$.

## 3 · $\boldsymbol\omega\times\mathbf v$ (sl.16–17, Tutorial 2 Q2)

**sl.16.** $m = 2.00$, $\mathbf v_b = [4\ 0\ 0]^T$, $\boldsymbol\omega_b = [0\ 0\ 0.5]^T$, $\mathbf F^b = [2\ 0\ 0]^T$.

$$\boldsymbol\omega\times\mathbf v = \begin{bmatrix}0\cdot0 - 0.5\cdot0\\ 0.5\cdot4 - 0\cdot0\\ 0\cdot0 - 0\cdot4\end{bmatrix} = \begin{bmatrix}0\\2\\0\end{bmatrix},\qquad
\dot{\mathbf v}_b = \begin{bmatrix}2/2\\0\\0\end{bmatrix} - \begin{bmatrix}0\\2\\0\end{bmatrix} = \begin{bmatrix}1\\-2\\0\end{bmatrix}$$

So $\dot u = 1.00$, $\dot v = -2.00$, $\dot w = 0$ m/s². Why is $\dot v \ne 0$ when $F_y = 0$? Because the body axes rotate, so the components along them change.

**Tutorial 2 Q2.** $m = 2.50$, $\mathbf v_b = [3\ 1\ 0]^T$, $\boldsymbol\omega_b = [0\ 0\ 0.400]^T$, $\mathbf F^b = [5.00\ 0\ 0]^T$.

$$\boldsymbol\omega\times\mathbf v = \begin{bmatrix}0\cdot0 - 0.4\cdot1\\ 0.4\cdot3 - 0\cdot0\\ 0\cdot1 - 0\cdot3\end{bmatrix} = \begin{bmatrix}-0.400\\1.20\\0\end{bmatrix},\qquad
\dot{\mathbf v}_b = \begin{bmatrix}5.00/2.50\\0\\0\end{bmatrix} - \begin{bmatrix}-0.400\\1.20\\0\end{bmatrix} = \begin{bmatrix}2.40\\-1.20\\0\end{bmatrix}\ \text{m/s}^2$$

Official check: $\mathbf a_b = \dot{\mathbf v}_b + \boldsymbol\omega\times\mathbf v_b = [2.40 - 0.400,\ -1.20 + 1.20,\ 0] = [2.00\ 0\ 0] = \mathbf F/m$ ✓

<details><summary>Note: probe Q1, the same thing with no force (added)</summary>

$\mathbf v_b = [4\ 0\ 0]^T$, $\boldsymbol\omega_b = [0\ 0\ 0.5]^T$, $\mathbf F = \mathbf 0$ gives $\dot{\mathbf v}_b = -[0\ 2\ 0]^T$. The NED velocity is constant (a straight line):
the nose swings right, so the fixed velocity slides toward the drone's left ($-y$). Yaw doesn't turn the path; only a force does (lab panel 2, "turn").
</details>

## 4 · Gravity in body axes *(added, probe Q2)*

Nose up $\theta = 30°$, $\phi = \psi = 0$, $m = 1.5$ kg (invented):

$$\mathbf F_g^b = 1.5(9.81)\begin{bmatrix}-\sin30°\\ 0\\ \cos30°\end{bmatrix} = 14.715\begin{bmatrix}-0.5\\0\\0.866\end{bmatrix} = \begin{bmatrix}-7.36\\0\\12.74\end{bmatrix}\ \text{N}$$

x is negative (it pulls toward the tail, because the nose points up) and z is positive (toward the belly). y is 0 because there's no roll: roll is what puts gravity into y, and pitch puts it into x.

## 5 · Rotational dynamics (sl.23–25, Tutorial 2 Q3)

**sl.23.** $J_x = 0.020$, $M_x = 0.060$, $q = r = 0$: $\dot p = 0.060/0.020 = \mathbf{3.00}$ rad/s². If $J_x$ doubles: $0.060/0.040 = 1.50$.

**sl.24.** $J = (0.020, 0.030, 0.040)$, $p = 0,\ q = 1.00,\ r = 2.00$, $M_x = 0.060$, $M_y = M_z = 0$:

$$(J_y - J_z)\,qr = (0.030 - 0.040)(1.00)(2.00) = -0.020\ \text{N m}$$

$$\dot p = \frac{0.060 + (-0.020)}{0.020} = 2.00\ \text{rad/s}^2\ \ (\text{down from }3.00),\qquad
\dot q = \frac{0 + (J_z-J_x)\cdot\underbrace{p}_{0}\cdot r}{J_y} = 0,\qquad \dot r = \frac{0 + (J_x-J_y)\cdot\underbrace{p}_{0}\cdot q}{J_z} = 0$$

**Tutorial 2 Q3.** $J = (0.0250, 0.0350, 0.0450)$, $M_x = 0.0800$.

(a) $p=q=r=0$: $\dot p = 0.0800/0.0250 = 3.20$ rad/s²

(b) $p = 0,\ q = 1.50,\ r = 2.00$:

$$(J_y - J_z)\,qr = (0.0350 - 0.0450)(1.50)(2.00) = -0.0300\ \text{N m},\qquad \dot p = \frac{0.0800 - 0.0300}{0.0250} = 2.00\ \text{rad/s}^2$$

$\dot q = \dot r = 0$, since both contain $p = 0$.

(c) The existing $q$ and $r$ add a coupling moment $(J_y - J_z)qr$, which here opposes $M_x$.

## 6 · Position rates (sl.27 quick check)

Level, facing east ($\psi = 90°$), $u = 5$ m/s. $R_b^n = R_z(90°)$:

$$\dot{\mathbf p}^n = \begin{bmatrix}\cos90° & -\sin90° & 0\\ \sin90° & \cos90° & 0\\ 0&0&1\end{bmatrix}\begin{bmatrix}5\\0\\0\end{bmatrix} = \begin{bmatrix}0\cdot5 - 1\cdot0\\ 1\cdot5 + 0\cdot0\\ 0\end{bmatrix} = \begin{bmatrix}0\\5\\0\end{bmatrix}\ \text{m/s}$$

## 7 · Block diagram (Tutorial 2 Q4, official solution)

- **(a)** $X = [p_N, p_E, p_D,\ u, v, w,\ \phi, \theta, \psi,\ p, q, r]^T$, grouped as position, body velocity, Euler angles, body rates.
- **(b)** Inputs: $\mathbf F = [F_x\ F_y\ F_z]$, $\mathbf M = [M_x\ M_y\ M_z]$. Parameters: $m, J$.
- **(c)** What each block needs:
  - rotational dynamics ← $\mathbf M$, $p\,q\,r$ (and $J$)
  - translational dynamics ← $\mathbf F$, $u\,v\,w$, $p\,q\,r$ (and $m$)
  - attitude kinematics ← $p\,q\,r$, $\phi\,\theta\,\psi$ (official list). ⚠ $E$ only actually contains $\phi$ and $\theta$, so $\psi$ isn't needed. Flagged, not changed
  - position kinematics ← $u\,v\,w$, $\phi\,\theta\,\psi$
- **(d)** Each integrator needs its initial state: $X(0) = X_0$.
