# B2 + B3 basis vectors and Gram–Schmidt: worked examples

**What this page is for:** worked calculations with every step written out. Read an example, cover the solution, then redo it on paper.
**Concepts and gaps** live in the lab: `B23_basis_lab.html`, in the same folder. Progress is tracked in [`progress.md`](progress.md).

<details>
<summary>Note: sources</summary>

- Parts 1–2: B2 sl.6–19, numbers verbatim.
- Part 3 applies sl.23–24 (compression) to sl.6's data. The slides have no numbers for this step, so the calculation is *(added)*.
- Part 4: B3 sl.10–12. Part 5: B3 sl.14–21.
- Part 6: the Section B practical, Q1 (`drills/data_vec_tf/q1.png`), kept as given.
- Every number was recomputed with sympy (2026-11-24). Anything not on the slides is tagged *(added)*.

</details>

<details>
<summary>Note: the words (most of the friction here is terminology)</summary>

| Word on the slides | What it means | Where you've seen it |
|---|---|---|
| basis vector / basis function | one axis direction, length 1. It's a **row of B** (or R) | A3's eigenvectors, which were the **columns** of X |
| transform coefficient Xᵢ | how much of x lies along axis i (its shadow on that axis) | A3's dᵢ in d = Xᵀb |
| dot / scalar / inner product ⟨Bᵢ, x⟩ | Σ Bᵢ(k) x(k), which works out the shadow | A3, A4 (Qᵀb) |
| "correlation" (B2 sl.21) | **the same dot product**, Σ Bᵢ(k) x(k). Big means x looks like Bᵢ, 0 means x has none of Bᵢ in it | B1's ρ is this too, once both variables are z-scored and you ÷N *(added)* |
| orthogonal | dot product = 0 (perpendicular) | A1, A3 |
| orthonormal | orthogonal **and** each length 1, so B⁻¹ = Bᵀ | A1's RᵀR = I |
| projection | the shadow vector: (shadow length) × (unit axis) | A3 lab panel 3 |

</details>

**Recipe card**

| Step | Formula | Slide |
|---|---|---|
| Coefficients | X = Bx, i.e. Xᵢ = Bᵢ · x | B2 sl.20–22 |
| Rebuild | x = BᵀX = Σ Xᵢ Bᵢ (only because B is orthonormal) | B2 sl.10–14 |
| Compress | keep the M big Xᵢ, set the rest to 0, rebuild. The loss is Σ (dropped Xᵢ)² | B2 sl.23–24 |
| Gram–Schmidt | u₁ = v₁. Then uⱼ = vⱼ − Σᵢ<ⱼ αᵢⱼ uᵢ, with αᵢⱼ = (uᵢ · vⱼ)/(uᵢ · uᵢ) | B3 sl.6, 13 |
| QR from GS | Q = [normalised u's], R = QᵀA (upper triangular) | B3 sl.17–21 |

---

## Part 1: rotate a point (B2 sl.7, 9)

### 1a. Rotate the axes by θ = 45° and find the transform coefficients of (3, 5).

**Solution**

$$\mathbf R = \begin{bmatrix}\cos 45° & \sin 45°\\ -\sin 45° & \cos 45°\end{bmatrix} = \frac{1}{\sqrt2}\begin{bmatrix}1 & 1\\ -1 & 1\end{bmatrix}$$

Each row of R is one new axis (a basis vector). Each coefficient is that row dotted with the point:

- $X_1 = \tfrac{1}{\sqrt2}(1\cdot3 + 1\cdot5) = \tfrac{8}{\sqrt2} = 5.66$
- $X_2 = \tfrac{1}{\sqrt2}(-1\cdot3 + 1\cdot5) = \tfrac{2}{\sqrt2} = 1.41$

$$\boxed{(3,5) \to (5.66,\ 1.41)}$$

### 1b. Do the same for (4, 4).

**Solution**

- $X_1 = \tfrac{1}{\sqrt2}(4 + 4) = \tfrac{8}{\sqrt2} = 5.66$
- $X_2 = \tfrac{1}{\sqrt2}(-4 + 4) = 0$

$$\boxed{(4,4) \to (5.66,\ 0)}$$

<details>
<summary>Note: why X₂ = 0 (this was probe Q4)</summary>

(4, 4) points at 45°, and the second axis $\tfrac{1}{\sqrt2}(-1, 1)$ points at 135°. They're 90° apart, so the shadow is 0: **this point has none of axis 2 in it**. In general Xᵢ = |x| cos(angle between x and Bᵢ). It's biggest when x lines up with Bᵢ and zero when they're perpendicular. That's all sl.21's "correlation" means.

</details>

---

## Part 2: rebuild, and why the transpose is the inverse (B2 sl.10–14, 19)

### 2a. Show that RRᵀ = I for any θ (sl.10, exercise).

**Solution**

$$\mathbf R\mathbf R^T = \begin{bmatrix}\cos\theta & \sin\theta\\ -\sin\theta & \cos\theta\end{bmatrix}\begin{bmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{bmatrix}$$

Entry by entry (row of R · column of Rᵀ, i.e. row · row of R):
- (1,1): $\cos^2\theta + \sin^2\theta = 1$
- (1,2): $-\cos\theta\sin\theta + \sin\theta\cos\theta = 0$
- (2,1): $-\sin\theta\cos\theta + \cos\theta\sin\theta = 0$
- (2,2): $\sin^2\theta + \cos^2\theta = 1$

$$\mathbf R\mathbf R^T = \mathbf I \;\Rightarrow\; \mathbf R^{-1} = \mathbf R^T$$

<details>
<summary>Note: what each entry is saying</summary>

The diagonal entries are row · itself, which is length² = 1 (normal). The off-diagonal entries are row 1 · row 2 = 0 (orthogonal). So "RRᵀ = I" is just "the rows are orthonormal", written as a matrix. sl.19 asks you to check this for the 45° pair, and it's the same calculation with θ = 45°.

</details>

### 2b. Rebuild (3, 5) from (5.66, 1.41) (sl.11).

**Solution**

$$\mathbf x = \mathbf R^T\mathbf X = \frac{1}{\sqrt2}\begin{bmatrix}1 & -1\\ 1 & 1\end{bmatrix}\begin{bmatrix}8/\sqrt2\\ 2/\sqrt2\end{bmatrix}$$

- top: $\tfrac{1}{\sqrt2}\left(\tfrac{8}{\sqrt2} - \tfrac{2}{\sqrt2}\right) = \tfrac{6}{2} = 3$
- bottom: $\tfrac{1}{\sqrt2}\left(\tfrac{8}{\sqrt2} + \tfrac{2}{\sqrt2}\right) = \tfrac{10}{2} = 5$ ✓

The same thing as a sum of basis vectors (sl.12–13):

$$\begin{bmatrix}3\\5\end{bmatrix} = 5.66\cdot\tfrac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix} + 1.41\cdot\tfrac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix} \qquad\text{vs}\qquad \begin{bmatrix}3\\5\end{bmatrix} = 3\begin{bmatrix}1\\0\end{bmatrix} + 5\begin{bmatrix}0\\1\end{bmatrix}$$

Same point, two different pairs of basis vectors (θ = 45° and θ = 0).

---

## Part 3: compression on sl.6's data *(added: sl.23–24 applied to sl.6)*

### 3a. Transform all five points of D = [0 3 5 8 10; 2 5 6 9 11] at θ = 45°. How much energy lands on each axis?

**Solution**

$X_1 = (x+y)/\sqrt2$ and $X_2 = (y-x)/\sqrt2$, one column at a time:

| point (x, y) | x + y | y − x | X₁ | X₂ |
|---|---|---|---|---|
| (0, 2) | 2 | 2 | 1.414 | 1.414 |
| (3, 5) | 8 | 2 | 5.657 | 1.414 |
| (5, 6) | 11 | 1 | 7.778 | 0.707 |
| (8, 9) | 17 | 1 | 12.021 | 0.707 |
| (10, 11) | 21 | 1 | 14.849 | 0.707 |

Energy is the sum of squares. Use (x+y)² / 2 so it stays exact:
- axis 1: $\tfrac{4 + 64 + 121 + 289 + 441}{2} = \tfrac{919}{2} = 459.5$
- axis 2: $\tfrac{4 + 4 + 1 + 1 + 1}{2} = \tfrac{11}{2} = 5.5$
- total: 465. Check against the raw data: Σx² + Σy² = 198 + 267 = 465 ✓ (rotating doesn't change the total)

$$\boxed{459.5 / 465 = 98.8\% \text{ on axis 1}}$$

### 3b. Drop X₂ (store 5 numbers instead of 10) and rebuild. What's lost?

**Solution**

With X₂ = 0, x = X₁ · (first column of Rᵀ) = X₁ · $\tfrac{1}{\sqrt2}(1, 1)$ = $\tfrac{x+y}{2}(1, 1)$:

| original | rebuilt |
|---|---|
| (0, 2) | (1, 1) |
| (3, 5) | (4, 4) |
| (5, 6) | (5.5, 5.5) |
| (8, 9) | (8.5, 8.5) |
| (10, 11) | (10.5, 10.5) |

Every point lands on the line y = x. The squared error is exactly the dropped energy, 5.5 (1.2%).

<details>
<summary>Note: rotate vs drop (probe Q3), and the best angle</summary>

- **Rotating loses nothing.** It only moves the energy between the axes (465 before, 465 after). You can always rotate back.
- **Dropping is where the loss happens**, and the loss = Σ (dropped coefficient)². So you want an angle that leaves almost nothing on the axes you drop.
- The best angle is the one that puts the most energy on axis 1: the top eigenvector of DDᵀ = [198 227; 227 267]. That's 49.3°, giving 99.38%. *(added)*
- B1 got 41.5° instead because B1 subtracts the means first (its S is built from centred data). B2's slides rotate the raw data about the origin. Same idea, different matrix.

</details>

---

## Part 4: Gram–Schmidt in 2D (B3 sl.10–12)

### 4a. v₁ = (5, 2), v₂ = (1, 7). Make u₂ perpendicular to u₁ = v₁.

**Solution**

$$\alpha = \frac{\mathbf u_1\cdot\mathbf v_2}{\mathbf u_1\cdot\mathbf u_1} = \frac{5\cdot1 + 2\cdot7}{5\cdot5 + 2\cdot2} = \frac{19}{29} = 0.6552$$

$$\mathbf u_2 = \mathbf v_2 - \alpha\mathbf u_1 = \begin{bmatrix}1\\7\end{bmatrix} - \frac{19}{29}\begin{bmatrix}5\\2\end{bmatrix} = \begin{bmatrix}1 - 95/29\\ 7 - 38/29\end{bmatrix} = \begin{bmatrix}-66/29\\ 165/29\end{bmatrix} = \begin{bmatrix}-2.276\\ 5.690\end{bmatrix}$$

**Check:** $\mathbf u_1\cdot\mathbf u_2 = 5(-2.276) + 2(5.690) = -11.38 + 11.38 = 0$ ✓

<details>
<summary>Note: what αu₁ is (probe Q5)</summary>

αu₁ is the **shadow of v₂ on u₁'s line**: the point on that line closest to v₂. It's exactly Part 1's coefficient idea, with u₁ not yet length 1, hence the ÷ u₁·u₁. Taking the shadow away leaves only the part of v₂ that sticks out sideways, so u₂ is perpendicular **by construction**. No eigenvectors are involved. GS works on any starting vectors.

The "show u₁ · u₂ = 0" exercise (sl.9) in one line: u₁ · (v₂ − αu₁) = u₁·v₂ − α u₁·u₁ = u₁·v₂ − u₁·v₂ = 0.

</details>

### 4b. Normalise both.

**Solution**

- $|\mathbf u_1| = \sqrt{29}$, so $\hat{\mathbf u}_1 = \tfrac{1}{\sqrt{29}}(5, 2)$
- $\mathbf u_2 = \tfrac{33}{29}(-2, 5)$, so $|\mathbf u_2| = \tfrac{33}{29}\sqrt{29}$ and $\hat{\mathbf u}_2 = \tfrac{1}{\sqrt{29}}(-2, 5)$

These are the rows of an orthonormal B, ready for Part 1's steps.

---

## Part 5: Gram–Schmidt in 3D, then QR (B3 sl.14–21)

### 5a. v₁ = (1, 0, 0), v₂ = (2, 0, 3), v₃ = (4, 5, 6). Orthonormalise.

**Solution** (normalise each u as soon as it's made, as the slides do, so every uᵢ · uᵢ = 1)

**u₁:** $\mathbf u_1 = \mathbf v_1 = (1, 0, 0)$, which already has length 1.

**u₂:**
- $\alpha_{12} = \mathbf u_1\cdot\mathbf v_2 = 1\cdot2 + 0 + 0 = 2$
- $\mathbf u_2 = (2, 0, 3) - 2(1, 0, 0) = (0, 0, 3)$, with length 3
- normalised: $\mathbf u_2 = (0, 0, 1)$

**u₃:** take off the shadow on **both** earlier u's:
- $\alpha_{13} = \mathbf u_1\cdot\mathbf v_3 = 4$
- $\alpha_{23} = \mathbf u_2\cdot\mathbf v_3 = 0 + 0 + 6 = 6$
- $\mathbf u_3 = (4, 5, 6) - 4(1, 0, 0) - 6(0, 0, 1) = (0, 5, 0)$, with length 5
- normalised: $\mathbf u_3 = (0, 1, 0)$

### 5b. A = [1 2 4; 0 0 5; 0 3 6] has columns v₁, v₂, v₃. Write A = QR.

**Solution**

$$\mathbf Q = [\mathbf u_1\ \mathbf u_2\ \mathbf u_3] = \begin{bmatrix}1&0&0\\0&0&1\\0&1&0\end{bmatrix}$$

$\mathbf R = \mathbf Q^T\mathbf A$. Entry (i, j) = uᵢ · (column j of A):

| | col 1 = (1,0,0) | col 2 = (2,0,3) | col 3 = (4,5,6) |
|---|---|---|---|
| u₁ = (1,0,0) | 1 | 2 | 4 |
| u₂ = (0,0,1) | 0 | 3 | 6 |
| u₃ = (0,1,0) | 0 | 0 | 5 |

$$\boxed{\mathbf R = \begin{bmatrix}1&2&4\\0&3&6\\0&0&5\end{bmatrix}}$$

**Check** QR, row by row: Q swaps rows 2 and 3 of R → [1 2 4; 0 0 5; 0 3 6] = A ✓

<details>
<summary>Note: you can read R straight off the GS working</summary>

- The diagonal is the lengths before normalising: 1, 3, 5.
- Above the diagonal are the α's: α₁₂ = 2, α₁₃ = 4, α₂₃ = 6.
- The zeros below the diagonal are there because u₂ was built to be ⟂ u₁, and u₃ to be ⟂ u₁ and u₂.

This is A2's QR again. Givens and Householder get there by rotating or reflecting A. Gram–Schmidt builds Q directly from A's columns.

</details>

---

## Part 6: the practical, Q1 (CDMA)

**Given:** two nodes share a channel. A: c₁ = [1 1 1 1], amplitude 1, bit +1. B: c₂ = [1 1 1 −1], amplitude 3, bit −1. The received signal is r = 1·(+1)·c₁ + 3·(−1)·c₂ = [−2 −2 −2 4]. Call s = (s₁, s₂) = amplitude × bit = (1, −3), the thing to recover.

### Q1.1 Are the two codes orthogonal?

$\mathbf c_1\cdot\mathbf c_2 = 1 + 1 + 1 - 1 = 2 \neq 0$. **No.**

### Q1.2 Decode with the correlator z = (r · c)/|c|². Is it right?

|c₁|² = |c₂|² = 4.
- $z_1 = \tfrac{(-2)+(-2)+(-2)+4}{4} = \tfrac{-2}{4} = -\tfrac12$, so the sign is −1. **Wrong** (A sent +1).
- $z_2 = \tfrac{(-2)+(-2)+(-2)-4}{4} = \tfrac{-10}{4} = -\tfrac52$, so the sign is −1. Correct.

<details>
<summary>Note: why A is wrong (probe Q6)</summary>

Dot r = s₁c₁ + s₂c₂ with c₁ and divide by |c₁|²:

$$z_1 = s_1 + s_2\,\frac{\mathbf c_1\cdot\mathbf c_2}{|\mathbf c_1|^2} = 1 + (-3)\cdot\tfrac{2}{4} = 1 - 1.5 = -0.5$$

The second term is **B leaking into A's reading**. It's only there because c₁ · c₂ ≠ 0. B is near and strong (×3), so its leak swamps A's own +1. With perpendicular codes the leak is 0. For example, with c₂ = [1 1 −1 −1] *(added)*, z₁ = 1 and z₂ = −3 exactly. This is Part 1 again: a shadow reading only works if the axes are perpendicular.

</details>

### Q1.3 Gram–Schmidt the codes to get Q, then find R so that C = [c₁ c₂] = QR.

- $\mathbf u_1 = \mathbf c_1 = (1,1,1,1)$, with $|\mathbf u_1| = 2$
- $\alpha = \tfrac{\mathbf u_1\cdot\mathbf c_2}{\mathbf u_1\cdot\mathbf u_1} = \tfrac{2}{4} = \tfrac12$
- $\mathbf u_2 = (1,1,1,-1) - \tfrac12(1,1,1,1) = (\tfrac12, \tfrac12, \tfrac12, -\tfrac32)$
- $|\mathbf u_2|^2 = \tfrac14 + \tfrac14 + \tfrac14 + \tfrac94 = 3$, so $|\mathbf u_2| = \sqrt3$
- $\mathbf q_1 = \tfrac12(1,1,1,1)$, $\;\mathbf q_2 = \tfrac{1}{\sqrt3}(\tfrac12, \tfrac12, \tfrac12, -\tfrac32)$

R = QᵀC, entry by entry:
- $r_{11} = \mathbf q_1\cdot\mathbf c_1 = \tfrac12(4) = 2$
- $r_{12} = \mathbf q_1\cdot\mathbf c_2 = \tfrac12(1+1+1-1) = 1$
- $r_{21} = \mathbf q_2\cdot\mathbf c_1 = \tfrac{1}{\sqrt3}(\tfrac12+\tfrac12+\tfrac12-\tfrac32) = 0$
- $r_{22} = \mathbf q_2\cdot\mathbf c_2 = \tfrac{1}{\sqrt3}(\tfrac12+\tfrac12+\tfrac12+\tfrac32) = \tfrac{3}{\sqrt3} = \sqrt3$

$$\boxed{\mathbf R = \begin{bmatrix}2 & 1\\ 0 & \sqrt3\end{bmatrix}}$$

<details>
<summary>Note: Q here is 4×2, not square</summary>

B3 sl.17 defines QR for a square A with QQᵀ = I. Here C is 4×2 (tall), so QᵀQ = I (2×2) still holds, but QQᵀ ≠ I. It's the same economy form as A4. Only QᵀQ = I is used below, so the method still works.

</details>

### Q1.4 Decode both bits using Qᵀr = Rs and back-substitution.

Qᵀr:
- $\mathbf q_1\cdot\mathbf r = \tfrac12(-2-2-2+4) = -1$
- $\mathbf q_2\cdot\mathbf r = \tfrac{1}{\sqrt3}(-1-1-1-6) = \tfrac{-9}{\sqrt3} = -3\sqrt3$

$$\begin{bmatrix}2 & 1\\ 0 & \sqrt3\end{bmatrix}\begin{bmatrix}s_1\\s_2\end{bmatrix} = \begin{bmatrix}-1\\ -3\sqrt3\end{bmatrix}$$

Back-substitute from the bottom:
- $\sqrt3\,s_2 = -3\sqrt3 \Rightarrow s_2 = -3$
- $2s_1 + 1\cdot(-3) = -1 \Rightarrow s_1 = 1$

$$\boxed{s = (1, -3)}$$

That's A = +1 and B = 3 × (−1): **both bits exact**.

---

## Recall

| Question | One line |
|---|---|
| What is Xᵢ? | Bᵢ · x, the shadow of x on axis i |
| Why can I rebuild with Bᵀ? | B is orthonormal, so B⁻¹ = Bᵀ |
| Where does compression lose information? | Only when you drop coefficients. Loss = Σ (dropped Xᵢ)² |
| What's αu₁ in GS? | the shadow of v₂ on u₁. Subtract it and what's left is ⟂ |
| R from GS? | diagonal = lengths before normalising, above = α's (when you normalise as you go) |
| Why does the plain correlator fail in CDMA? | c₁ · c₂ ≠ 0, so the other user leaks in |
