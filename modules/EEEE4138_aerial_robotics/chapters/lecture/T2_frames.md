# T1 + T2 worked examples

Picture ↔ equation ↔ answer shape live in [T2_frames_lab.html](T2_frames_lab.html). This page is for practising the steps.
Sources: T1 Part 2, T2 Parts 1–2, Tutorial 1. Tutorial 1 has **no official solutions in the repo**, so Part 5 is
worked by AI and every number is checked with sympy/numpy. Anything not from the slides is marked *(added)*.

## Facts card

| | |
|---|---|
| NED | x = North, y = East, z = **Down**. Altitude $h = -p_d$ |
| Body | x = nose, y = right, z = belly |
| Vehicle frame | NED directions with the origin at the CoM. It never rotates |
| Notation | $\mathbf p^0 = R_1^0\,\mathbf p^1$: $R_1^0$ takes frame-1 coordinates and gives frame-0 coordinates |
| Reverse | $R_0^1 = (R_1^0)^{-1} = (R_1^0)^T$, which is the same as using $-\theta$ |
| Chain | $R_2^0 = R_1^0 R_2^1$. Read right to left: the rightmost matrix acts first |
| Course attitude | $R_v^b = R_x(\phi)\,R_y(\theta)\,R_z(\psi)$: yaw, then pitch, then roll. Vehicle → body |
| Body → NED | $R_b^v = (R_v^b)^T$ (T3 calls it $R_b^n$) |
| Gimbal lock | $\theta = \pm90°$. The rate map has $\tan\theta$ and $1/\cos\theta$ |
| Quaternion | $\mathbf q = [\cos\tfrac\theta2,\ \mathbf a\sin\tfrac\theta2]$, $\lVert\mathbf q\rVert = 1$. $\mathbf q$ and $-\mathbf q$ are the same orientation |

The slide's single-axis matrices (vehicle → body direction, T2 P1):

$$R_z(\psi) = \begin{bmatrix} c\psi & s\psi & 0\\ -s\psi & c\psi & 0\\ 0&0&1\end{bmatrix},\quad
R_y(\theta) = \begin{bmatrix} c\theta & 0 & -s\theta\\ 0&1&0\\ s\theta & 0 & c\theta\end{bmatrix},\quad
R_x(\phi) = \begin{bmatrix} 1&0&0\\ 0& c\phi & s\phi\\ 0 & -s\phi & c\phi\end{bmatrix}$$

$$R_v^b = \begin{bmatrix} c\theta c\psi & c\theta s\psi & -s\theta\\
s\phi s\theta c\psi - c\phi s\psi & s\phi s\theta s\psi + c\phi c\psi & s\phi c\theta\\
c\phi s\theta c\psi + s\phi s\psi & c\phi s\theta s\psi - s\phi c\psi & c\phi c\theta\end{bmatrix}$$

<details><summary>Note: why Tutorial 1 writes R_x(−φ)R_y(−θ)R_z(−ψ)</summary>

Tutorial 1 uses the other sign form, $\begin{bmatrix}c&-s\\s&c\end{bmatrix}$ (the "turn a vector" form). Plugging in −angle flips the signs of the $s$ terms, which gives the slide matrices above. So the two are the same $R_v^b$ (checked symbolically).
</details>

---

## Part 1 · T1 thrust (T1 Part 2 sl.17, 18, 15, 25)

**1a. Hover (sl.17).** $m = 1.2$ kg.

$$T = mg = 1.2(9.81) = 11.772 \approx 11.77\ \text{N},\qquad \text{per rotor} = \frac{11.772}{4} = 2.943 \approx 2.94\ \text{N}$$

With a 0.3 kg payload: $T = 1.5(9.81) = 14.715 \approx 14.72$ N, and $14.715/11.772 = 1.25$, a **25 %** increase.

**1b. Quick Check (sl.18).** $m = 1.5$ kg, $T = 18$ N, level, no drag.

$$\text{up positive: } m a = T - mg \;\Rightarrow\; 1.5\,a = 18 - 14.715 = 3.285 \;\Rightarrow\; a = \frac{3.285}{1.5} = 2.19\ \text{m/s}^2\ \text{(up)}$$

In NED (D positive) the same thing reads $m a_d = mg - T = -3.285$, so $a_d = -2.19$ m/s², where the minus means up.
Does a constant 18 N give a constant climb speed? **No.** A constant net force gives a constant *acceleration*, so the speed keeps growing. A constant speed needs $T = mg$.

**1c. Tilt (sl.15).** Tilted thrust splits into a vertical part $T\cos\alpha$ and a horizontal part $T\sin\alpha$. To hold altitude: $T\cos\alpha = mg$. Example *(added: α = 30°, m = 1.5 kg)*:

$$T = \frac{mg}{\cos\alpha} = \frac{14.715}{0.8660} = 16.99\ \text{N}\ (> 14.715\ \text{hover}),\qquad a_{\text{horiz}} = \frac{T\sin\alpha}{m} = \frac{16.99(0.5)}{1.5} = 5.66\ \text{m/s}^2$$

**1d. Endurance (sl.25).** 14.8 V, 5 Ah, 80 % usable, 250 W average.

$$E = 14.8 \times 5 = 74\ \text{Wh},\quad E_{\text{usable}} = 0.8 \times 74 = 59.2\ \text{Wh},\quad t = \frac{59.2}{250} = 0.2368\ \text{h} = 14.2\ \text{min}$$

---

## Part 2 · One vector, two frames (T2 Part 1 Quiz Q3)

Frame 1 is turned 90° anticlockwise from frame 0, and $\mathbf p^1 = [2\ 0]^T$. Find $\mathbf p^0$.

$$R_1^0 = \begin{bmatrix}\cos90° & -\sin90°\\ \sin90° & \cos90°\end{bmatrix} = \begin{bmatrix}0&-1\\1&0\end{bmatrix},\qquad
\mathbf p^0 = \begin{bmatrix}0\cdot2 + (-1)\cdot0\\ 1\cdot2 + 0\cdot0\end{bmatrix} = \begin{bmatrix}0\\2\end{bmatrix}$$

Back again: $R_0^1 = (R_1^0)^T = \begin{bmatrix}0&1\\-1&0\end{bmatrix}$, and $R_0^1\mathbf p^0 = [0\cdot0 + 1\cdot2,\ -1\cdot0 + 0\cdot2]^T = [2\ 0]^T$ ✓

<details><summary>Note: what the swapped-sign matrix is</summary>

$\begin{bmatrix}c&s\\-s&c\end{bmatrix}$ is the same pair of frames, converted the other way (frame 0 → frame 1). The physical rotation hasn't changed; only the direction of the coordinate conversion has. The slides use both forms, so always check which way a given matrix converts.
</details>

---

## Part 3 · Body velocity → NED (T2 Part 2 exercise)

Level, $\psi = 30°$ (30° east of north), body velocity $[u\ v\ w] = [4\ 0\ 0]$ m/s. Find the NED velocity and the displacement after 5 s.

You need body → NED, which is $R_b^v = (R_v^b)^T$. With $\phi = \theta = 0$, that's $R_z(\psi)^T$:

$$\dot{\mathbf p} = \begin{bmatrix}c\psi & -s\psi & 0\\ s\psi & c\psi & 0\\ 0&0&1\end{bmatrix}\begin{bmatrix}u\\v\\w\end{bmatrix}
= \begin{bmatrix}0.8660(4) - 0.5000(0) + 0\\ 0.5000(4) + 0.8660(0) + 0\\ 0\end{bmatrix} = \begin{bmatrix}3.464\\2.000\\0\end{bmatrix}\ \text{m/s},\qquad
\Delta\mathbf p = 5\,\dot{\mathbf p} = \begin{bmatrix}17.32\\10.00\\0\end{bmatrix}\ \text{m}$$

This matches the slide's level-flight shortcut: North $= u\cos\psi - v\sin\psi$, East $= u\sin\psi + v\cos\psi$.

---

## Part 4 · Camera position (T2 Part 2 exercise, homogeneous transform)

Level, facing **east** ($\psi = 90°$). The UAV is at NED $[10\ 20\ -5]$ m. The camera is 0.30 m forward and 0.10 m body-down: $\mathbf b = [0.30\ 0\ 0.10]^T$.

$$R_b^v = R_z(90°)^T = \begin{bmatrix}0&-1&0\\1&0&0\\0&0&1\end{bmatrix},\qquad
R_b^v\,\mathbf b = \begin{bmatrix}0(0.30) - 1(0) + 0(0.10)\\ 1(0.30) + 0(0) + 0(0.10)\\ 0 + 0 + 1(0.10)\end{bmatrix} = \begin{bmatrix}0\\0.30\\0.10\end{bmatrix}$$

$$\text{camera} = \begin{bmatrix}10\\20\\-5\end{bmatrix} + \begin{bmatrix}0\\0.30\\0.10\end{bmatrix} = \begin{bmatrix}10\\20.30\\-4.90\end{bmatrix}\ \text{m}$$

The same thing as one $H$ (T2 P2):

$$H = \begin{bmatrix}R_b^v & \mathbf p\\ \mathbf 0 & 1\end{bmatrix} = \begin{bmatrix}0&-1&0&10\\1&0&0&20\\0&0&1&-5\\0&0&0&1\end{bmatrix},\qquad
H\begin{bmatrix}0.30\\0\\0.10\\1\end{bmatrix} = \begin{bmatrix}10\\20.30\\-4.90\\1\end{bmatrix}$$

D went from −5 to −4.90, which is a *bigger* D, so the camera is **below** the CoM: $h = 4.90$ m against 5.00 m.
Back-check with the shortcut $H^{-1} = \begin{bmatrix}R^T & -R^T\mathbf D\\ \mathbf 0 & 1\end{bmatrix}$: $R^T(\text{camera} - \mathbf p) = R^T[0\ 0.30\ 0.10]^T = [0.30\ 0\ 0.10]^T$ ✓

---

## Part 5 · Tutorial 1 (AI-worked, no official solutions)

**Q1. Sequences.** 3 choices for the first axis, then 2 for the second (it must differ), then 2 for the third: $3\cdot2\cdot2 = \mathbf{12}$.
- Proper Euler (first axis = last): XYX, XZX, YXY, YZY, ZXZ, ZYZ
- Tait–Bryan (all three different): XYZ, XZY, YXZ, YZX, ZXY, **ZYX** (this course)

The same axis twice in a row is redundant: $R_z(a)R_z(b) = R_z(a+b)$. Two of the angles merge into one, which leaves only two independent angles, and those can't reach every orientation.

**Q2. ZYZ at θ = 0.** $R = R_z(\phi)\,I\,R_z(\psi) = R_z(\phi + \psi)$. It's a valid orientation (a pure turn about z), but only the sum $\phi + \psi$ can be read from $R$.

**Q3. Recover ZYZ** from $R = R_z(\phi)R_y(\theta)R_z(\psi)$ (tutorial slide), with $0 < \theta < 180°$ so $\sin\theta > 0$:

$$R_{33} = c\theta \Rightarrow \theta = \cos^{-1}R_{33};\qquad
\begin{matrix}R_{13} = c\phi\,s\theta\\ R_{23} = s\phi\,s\theta\end{matrix} \Rightarrow \phi = \operatorname{atan2}(R_{23}, R_{13});\qquad
\begin{matrix}R_{31} = -s\theta\,c\psi\\ R_{32} = s\theta\,s\psi\end{matrix} \Rightarrow \psi = \operatorname{atan2}(R_{32}, -R_{31})$$

These fail at $\sin\theta = 0$, because then $R_{13} = R_{23} = R_{31} = R_{32} = 0$ and atan2(0, 0) is undefined (Q2's case).

**Q4. Recover roll, pitch, yaw** from $R_v^b$ (facts card), with $-90° < \theta < 90°$ so $\cos\theta > 0$:

$$\theta = -\sin^{-1}R_{13},\qquad \phi = \operatorname{atan2}(R_{23}, R_{33}),\qquad \psi = \operatorname{atan2}(R_{12}, R_{11})$$

Second branch: $\theta' = 180° - \theta$ has the same $\sin$ but $\cos\theta' < 0$, so flip both atan2 arguments:
$\phi' = \operatorname{atan2}(-R_{23}, -R_{33}) = \phi \pm 180°$ and $\psi' = \operatorname{atan2}(-R_{12}, -R_{11}) = \psi \pm 180°$.
Check: (25°, 40°, −70°) and (−155°, 140°, 110°) give the same matrix ✓ (numpy).
The recovery is singular when $\cos\theta = 0$, because $R_{23}, R_{33}, R_{12}, R_{11}$ all become 0.

**Q5. θ = +90°** ($s\theta = 1$, $c\theta = 0$), using $\sin(\phi-\psi) = s\phi c\psi - c\phi s\psi$ and $\cos(\phi-\psi) = c\phi c\psi + s\phi s\psi$:

$$R = \begin{bmatrix}0&0&-1\\ \sin(\phi-\psi) & \cos(\phi-\psi) & 0\\ \cos(\phi-\psi) & -\sin(\phi-\psi) & 0\end{bmatrix}$$

Only the difference can be found: $\phi - \psi = \operatorname{atan2}(R_{21}, R_{22})$. $\phi$ and $\psi$ can't be recovered separately. (At θ = −90° the same thing happens with $\phi + \psi$.)

**Q6. (φ, θ, ψ) = (120°, 90°, −60°).** $\phi - \psi = 180°$, so $\sin = 0$ and $\cos = -1$:

$$R = \begin{bmatrix}0&0&-1\\0&-1&0\\-1&0&0\end{bmatrix}$$

Not unique: any triple with θ = 90° and φ − ψ = 180° gives the same matrix, e.g. **(180°, 90°, 0°)**, (90°, 90°, −90°), (0°, 90°, −180°) (all checked).

---

## Part 6 · Quaternions (T2 Part 2)

**Normalise and invert** $\mathbf q = [2\ 0\ 0\ 2]$:

$$\lVert\mathbf q\rVert = \sqrt{2^2+0+0+2^2} = \sqrt8 = 2\sqrt2,\qquad \mathbf q_{\text{unit}} = \Big[\tfrac1{\sqrt2}\ 0\ 0\ \tfrac1{\sqrt2}\Big],\qquad \mathbf q_{\text{unit}}^{-1} = \mathbf q_{\text{unit}}^* = \Big[\tfrac1{\sqrt2}\ 0\ 0\ -\tfrac1{\sqrt2}\Big]$$

(For a unit $\mathbf q$, the inverse is the conjugate.)

**90° about z:** $\mathbf a = [0\ 0\ 1]$, $\theta/2 = 45°$, so $\mathbf q = [\cos45°\ 0\ 0\ \sin45°] = [\tfrac1{\sqrt2}\ 0\ 0\ \tfrac1{\sqrt2}]$. The check: $\tfrac12 + \tfrac12 = 1$.

**Your turn (slide): +60° about x.** Try it before opening.
<details><summary>Answer</summary>

$\theta/2 = 30°$, so $\mathbf q = [\cos30°\ \ \sin30°\ \ 0\ \ 0] = [\tfrac{\sqrt3}2\ \ \tfrac12\ \ 0\ \ 0]$. The check: $\tfrac34 + \tfrac14 = 1$.
</details>
