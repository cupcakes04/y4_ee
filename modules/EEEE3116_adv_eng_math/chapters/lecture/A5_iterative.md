# A5 iterative solvers: worked examples

**What this page is for:** worked calculations, every step written out. Read an example, cover the solution, then redo it on paper.
**Concepts and gaps** live in the [A5 iterative lab](https://claude.ai/artifact/8ANFiz2BFrzNQd6iMsey6v) (`A5_iterative_lab.html`, same folder).
Progress: [`progress.md`](progress.md).

<details>
<summary>Note: sources</summary>

Parts 1–5 use the practical session's problem (`drills/iterative_revolution`), kept exactly as given. The algorithms are A5 sl.25 (steepest descent), sl.27 (minimal residual), sl.29 (CG, with the typo fixed: see the card), and sl.33 (Jacobi). Gauss-Seidel is "search the web" on sl.33, so its form here is the standard one *(added)*. Part 6 runs sl.19–20's power method on the same A, from a start vector I picked *(added)*. Part 7 uses sl.9 and sl.11. Part 8 runs the sl.52–53 block-LU route on a small chain I made up *(added numbers)*. Every number was recomputed with exact fractions in Python (2026-11-22).

</details>

---

## Recipe cards

Each iterative method repeats one loop: **residual → direction → step length → update**. Only multiplies by A are used, never a solve.

| Method | Slide | Direction | Step length | Update |
|---|---|---|---|---|
| Steepest descent (SD) | sl.25 | $\mathbf p_k = \mathbf r_k$ | $d_k = \dfrac{\mathbf r_k^T\mathbf r_k}{\mathbf r_k^T\mathbf A\mathbf r_k}$ | $\mathbf x_{k+1} = \mathbf x_k + d_k\mathbf r_k$, then $\mathbf r_{k+1} = \mathbf b - \mathbf A\mathbf x_{k+1}$ |
| Minimal residual (MRA) | sl.27 | $\mathbf p_k = \mathbf r_k$ | $d_k = \dfrac{\mathbf r_k^T\mathbf A\mathbf r_k}{\mathbf r_k^T\mathbf A^T\mathbf A\mathbf r_k} = \dfrac{\mathbf r_k^T(\mathbf A\mathbf r_k)}{(\mathbf A\mathbf r_k)^T(\mathbf A\mathbf r_k)}$ | same as SD |
| Conjugate gradient (CG) | sl.29 | $\mathbf p_0 = \mathbf r_0$, then $\mathbf p_{k+1} = \mathbf r_{k+1} + \beta_k\mathbf p_k$ | $\alpha_k = \dfrac{\mathbf r_k^T\mathbf r_k}{\mathbf p_k^T\mathbf A\mathbf p_k}$, $\;\beta_k = \dfrac{\mathbf r_{k+1}^T\mathbf r_{k+1}}{\mathbf r_k^T\mathbf r_k}$ | $\mathbf x_{k+1} = \mathbf x_k + \alpha_k\mathbf p_k$, $\;\mathbf r_{k+1} = \mathbf r_k - \alpha_k\mathbf A\mathbf p_k$ |
| Gauss-Jacobi | sl.33 | split $\mathbf A = \mathbf D + \mathbf E$ (diagonal + rest) | none | solve $\mathbf D\mathbf x_{k+1} = \mathbf b - \mathbf E\mathbf x_k$ (divide each row by its diagonal) |
| Gauss-Seidel *(added form)* | sl.33 | same split, rows in order | none | as Jacobi, but each row **uses the x values already updated in this sweep** |
| Power method | sl.19–20 | — | — | $\mathbf x_{k} = \mathbf A\mathbf x_{k-1}$ (finds the dominant eigenvector, not a solve) |

<details>
<summary>Note: typo on sl.29</summary>

**Typo on sl.29:** the slide prints $\mathbf x_{k+1} = \mathbf x_k + \alpha_k\mathbf r_k$ and $\mathbf p_{k+1} = \mathbf r_k + \beta_k\mathbf p_k$. Use $\alpha_k\mathbf{p}_k$ and $\mathbf r_{k+1}$, as in the card. With the slide's version CG doesn't finish in 2 steps.

</details>

**Convergence conditions (sl.25, 27, 30):** SD needs A symmetric and positive definite. MRA needs A positive definite only (sl.27 crosses out "symmetric"). CG on a symmetric positive definite A reaches the exact answer in at most N steps *in exact arithmetic*. In practice rounding stops that happening on real problems (sl.30).

---

## Part 0: the practical's problem

$$\mathbf A = \begin{bmatrix}2 & 1 \\ 1 & 3\end{bmatrix},\qquad \mathbf b = \begin{bmatrix}1 \\ 2\end{bmatrix},\qquad \mathbf x_0 = \begin{bmatrix}0 \\ 0\end{bmatrix}$$

### 0a. Is it safe to use SD and CG? (Need symmetric and positive definite.)

**Solution**
- Symmetric: $a_{01} = a_{10} = 1$ ✓
- Positive definite means all eigenvalues are > 0. Use A3's recipe:

$$\det(\mathbf A - k\mathbf I) = (2-k)(3-k) - (1)(1) = 6 - 5k + k^2 - 1 = k^2 - 5k + 5 = 0$$

$$k = \frac{5 \pm \sqrt{25 - 20}}{2} = \frac{5 \pm \sqrt5}{2} \;\Rightarrow\; k_0 = 3.618,\; k_1 = 1.382$$

Both are > 0 ✓. (Shortcut for a 2×2, *added*: if $a_{00} > 0$ and $\det > 0$, both eigenvalues are positive. Here $2 > 0$ and $\det = 5 > 0$.)
- Diagonally dominant *(added term, see Part 4)*: row 0 has $|2| > |1|$ and row 1 has $|3| > |1|$ ✓

### 0b. The exact answer, to check against

$$\mathbf A^{-1} = \frac{1}{\det \mathbf A}\begin{bmatrix} 3 & -1 \\ -1 & 2 \end{bmatrix} = \frac15\begin{bmatrix} 3 & -1 \\ -1 & 2 \end{bmatrix}$$

$$\begin{aligned}
x^*_{0} &= \left(\tfrac{3}{5}\right)(1) + \left(-\tfrac{1}{5}\right)(2) = \tfrac{3}{5} - \tfrac{2}{5} = \frac{3 - 2}{5} = \tfrac{1}{5} \\
x^*_{1} &= \left(-\tfrac{1}{5}\right)(1) + \left(\tfrac{2}{5}\right)(2) = -\tfrac{1}{5} + \tfrac{4}{5} = \frac{-1 + 4}{5} = \tfrac{3}{5}
\end{aligned}$$

$$\mathbf x^* = \begin{bmatrix}\tfrac{1}{5} \\ \tfrac{3}{5}\end{bmatrix} = \begin{bmatrix} 0.2 \\ 0.6 \end{bmatrix}$$

This is the target. A huge sparse A can't be inverted like this, which is the whole point of A5 (sl.10–11).

---

## Part 1: steepest descent (sl.25), two iterations

### Iteration k = 0

**1. Residual** $\mathbf r_0 = \mathbf b - \mathbf A\mathbf x_0$. First multiply:
$$\begin{aligned}
(\mathbf A\mathbf x_0)_{0} &= 2(0) + 1(0) = 0 \\
(\mathbf A\mathbf x_0)_{1} &= 1(0) + 3(0) = 0
\end{aligned}$$
then subtract from b:
$$\begin{aligned}
(r_0)_{0} &= 1 - 0 = 1 \\
(r_0)_{1} &= 2 - 0 = 2
\end{aligned}$$

$$\mathbf r_0 = \begin{bmatrix}1 \\ 2\end{bmatrix}$$

**2. Top of d:**
$$\begin{aligned}
\mathbf r_0^T\mathbf r_0 &= 1(1) + 2(2) = 1 + 4 = 5
\end{aligned}$$

**3. Multiply** $\mathbf A\mathbf r_0$:
$$\begin{aligned}
(\mathbf A\mathbf r_0)_{0} &= 2(1) + 1(2) = 2 + 2 = 4 \\
(\mathbf A\mathbf r_0)_{1} &= 1(1) + 3(2) = 1 + 6 = 7
\end{aligned}$$

$$\mathbf A\mathbf r_0 = \begin{bmatrix}4 \\ 7\end{bmatrix}$$

**4. Bottom of d:**
$$\begin{aligned}
\mathbf r_0^T(\mathbf A\mathbf r_0) &= 1(4) + 2(7) = 4 + 14 = 18
\end{aligned}$$

**5. Step length:**

$$d_0 = \frac{5}{18} \approx 0.277778$$

**6. Update** $\mathbf x_1 = \mathbf x_0 + d_0\mathbf r_0$:
$$\begin{aligned}
(x_1)_{0} &= 0 + \left(\tfrac{5}{18}\right)(1) = \tfrac{5}{18} \\
(x_1)_{1} &= 0 + \left(\tfrac{5}{18}\right)(2) = \tfrac{5}{9}
\end{aligned}$$

$$\mathbf x_1 = \begin{bmatrix}\tfrac{5}{18} \\ \tfrac{5}{9}\end{bmatrix} \approx \begin{bmatrix} 0.277778 \\ 0.555556 \end{bmatrix}$$

### Iteration k = 1

**1. Residual** $\mathbf r_1 = \mathbf b - \mathbf A\mathbf x_1$. First multiply:
$$\begin{aligned}
(\mathbf A\mathbf x_1)_{0} &= 2\left(\tfrac{5}{18}\right) + 1\left(\tfrac{5}{9}\right) = \tfrac{5}{9} + \tfrac{5}{9} = \frac{5 + 5}{9} = \tfrac{10}{9} \\
(\mathbf A\mathbf x_1)_{1} &= 1\left(\tfrac{5}{18}\right) + 3\left(\tfrac{5}{9}\right) = \tfrac{5}{18} + \tfrac{5}{3} = \frac{5 + 30}{18} = \tfrac{35}{18}
\end{aligned}$$
then subtract from b:
$$\begin{aligned}
(r_1)_{0} &= 1 - \tfrac{10}{9} = \frac{9 - 10}{9} = -\tfrac{1}{9} \\
(r_1)_{1} &= 2 - \tfrac{35}{18} = \frac{36 - 35}{18} = \tfrac{1}{18}
\end{aligned}$$

$$\mathbf r_1 = \begin{bmatrix}-\tfrac{1}{9} \\ \tfrac{1}{18}\end{bmatrix}$$

**2. Top of d:**
$$\begin{aligned}
\mathbf r_1^T\mathbf r_1 &= \left(-\tfrac{1}{9}\right)\left(-\tfrac{1}{9}\right) + \left(\tfrac{1}{18}\right)\left(\tfrac{1}{18}\right) = \tfrac{1}{81} + \tfrac{1}{324} = \frac{4 + 1}{324} = \tfrac{5}{324}
\end{aligned}$$

**3. Multiply** $\mathbf A\mathbf r_1$:
$$\begin{aligned}
(\mathbf A\mathbf r_1)_{0} &= 2\left(-\tfrac{1}{9}\right) + 1\left(\tfrac{1}{18}\right) = -\tfrac{2}{9} + \tfrac{1}{18} = \frac{-4 + 1}{18} = -\tfrac{1}{6} \\
(\mathbf A\mathbf r_1)_{1} &= 1\left(-\tfrac{1}{9}\right) + 3\left(\tfrac{1}{18}\right) = -\tfrac{1}{9} + \tfrac{1}{6} = \frac{-2 + 3}{18} = \tfrac{1}{18}
\end{aligned}$$

$$\mathbf A\mathbf r_1 = \begin{bmatrix}-\tfrac{1}{6} \\ \tfrac{1}{18}\end{bmatrix}$$

**4. Bottom of d:**
$$\begin{aligned}
\mathbf r_1^T(\mathbf A\mathbf r_1) &= \left(-\tfrac{1}{9}\right)\left(-\tfrac{1}{6}\right) + \left(\tfrac{1}{18}\right)\left(\tfrac{1}{18}\right) = \tfrac{1}{54} + \tfrac{1}{324} = \frac{6 + 1}{324} = \tfrac{7}{324}
\end{aligned}$$

**5. Step length:**

$$d_1 = \frac{\tfrac{5}{324}}{\tfrac{7}{324}} = \tfrac{5}{7} \approx 0.714286$$

**6. Update** $\mathbf x_2 = \mathbf x_1 + d_1\mathbf r_1$:
$$\begin{aligned}
(x_2)_{0} &= \tfrac{5}{18} + \left(\tfrac{5}{7}\right)\left(-\tfrac{1}{9}\right) = \tfrac{5}{18} - \tfrac{5}{63} = \frac{35 - 10}{126} = \tfrac{25}{126} \\
(x_2)_{1} &= \tfrac{5}{9} + \left(\tfrac{5}{7}\right)\left(\tfrac{1}{18}\right) = \tfrac{5}{9} + \tfrac{5}{126} = \frac{70 + 5}{126} = \tfrac{25}{42}
\end{aligned}$$

$$\mathbf x_2 = \begin{bmatrix}\tfrac{25}{126} \\ \tfrac{25}{42}\end{bmatrix} \approx \begin{bmatrix} 0.198413 \\ 0.595238 \end{bmatrix}$$

### Check: residual after two steps

$$\begin{aligned}
(\mathbf A\mathbf x_2)_{0} &= 2\left(\tfrac{25}{126}\right) + 1\left(\tfrac{25}{42}\right) = \tfrac{25}{63} + \tfrac{25}{42} = \frac{50 + 75}{126} = \tfrac{125}{126} \\
(\mathbf A\mathbf x_2)_{1} &= 1\left(\tfrac{25}{126}\right) + 3\left(\tfrac{25}{42}\right) = \tfrac{25}{126} + \tfrac{25}{14} = \frac{25 + 225}{126} = \tfrac{125}{63}
\end{aligned}$$
$$\begin{aligned}
(r_2)_{0} &= 1 - \tfrac{125}{126} = \frac{126 - 125}{126} = \tfrac{1}{126} \\
(r_2)_{1} &= 2 - \tfrac{125}{63} = \frac{126 - 125}{63} = \tfrac{1}{63}
\end{aligned}$$

$$\mathbf r_2 = \begin{bmatrix}\tfrac{1}{126} \\ \tfrac{1}{63}\end{bmatrix} = \frac{1}{126}\begin{bmatrix}1\\2\end{bmatrix},\qquad \|\mathbf r_2\| \approx 0.0177$$

<details>
<summary>Note: what to notice (added)</summary>

**What to notice** *(added observations, checked)*:
- $\mathbf r_1^T\mathbf r_0 = \left(-\tfrac{1}{9}\right)(1) + \left(\tfrac{1}{18}\right)(2) = 0$. Each new direction is at **90°** to the last one. That's the zig-zag.
- $\mathbf r_2 = \tfrac{1}{126}\mathbf r_0$ points the same way as $\mathbf r_0$. So iteration 2 repeats iteration 0's direction, just 126× smaller. SD never lands exactly. It shrinks the error by the same factor every two steps.
- Step lengths alternate $d = \tfrac{5}{18}, \tfrac57, \tfrac{5}{18}, \tfrac57, \dots$ (matches the practical's log).

</details>

---

## Part 2: minimal residual (sl.27), two iterations

Same loop as SD. Only the step length changes: $d_k = \dfrac{\mathbf r_k^T(\mathbf A\mathbf r_k)}{(\mathbf A\mathbf r_k)^T(\mathbf A\mathbf r_k)}$. It picks the d that makes the **next residual as short as possible**.

### Iteration k = 0

**1. Residual:** $\mathbf x_0 = \mathbf 0$, so $\mathbf r_0 = \mathbf b = \begin{bmatrix}1 \\ 2\end{bmatrix}$.

**2. Multiply** $\mathbf A\mathbf r_0$:
$$\begin{aligned}
(\mathbf A\mathbf r_0)_{0} &= 2(1) + 1(2) = 2 + 2 = 4 \\
(\mathbf A\mathbf r_0)_{1} &= 1(1) + 3(2) = 1 + 6 = 7
\end{aligned}$$

$$\mathbf A\mathbf r_0 = \begin{bmatrix}4 \\ 7\end{bmatrix}$$

**3. Top and bottom of d:**
$$\begin{aligned}
\mathbf r_0^T(\mathbf A\mathbf r_0) &= 1(4) + 2(7) = 4 + 14 = 18 \\
(\mathbf A\mathbf r_0)^T(\mathbf A\mathbf r_0) &= 4(4) + 7(7) = 16 + 49 = 65
\end{aligned}$$

**4. Step length:**

$$d_0 = \frac{18}{65} \approx 0.276923$$

**5. Update** $\mathbf x_1 = \mathbf x_0 + d_0\mathbf r_0$:
$$\begin{aligned}
(x_1)_{0} &= 0 + \left(\tfrac{18}{65}\right)(1) = \tfrac{18}{65} \\
(x_1)_{1} &= 0 + \left(\tfrac{18}{65}\right)(2) = \tfrac{36}{65}
\end{aligned}$$

$$\mathbf x_1 = \begin{bmatrix}\tfrac{18}{65} \\ \tfrac{36}{65}\end{bmatrix} \approx \begin{bmatrix} 0.276923 \\ 0.553846 \end{bmatrix}$$

### Iteration k = 1

**1. Residual** $\mathbf r_1 = \mathbf b - \mathbf A\mathbf x_1$:
$$\begin{aligned}
(\mathbf A\mathbf x_1)_{0} &= 2\left(\tfrac{18}{65}\right) + 1\left(\tfrac{36}{65}\right) = \tfrac{36}{65} + \tfrac{36}{65} = \frac{36 + 36}{65} = \tfrac{72}{65} \\
(\mathbf A\mathbf x_1)_{1} &= 1\left(\tfrac{18}{65}\right) + 3\left(\tfrac{36}{65}\right) = \tfrac{18}{65} + \tfrac{108}{65} = \frac{18 + 108}{65} = \tfrac{126}{65}
\end{aligned}$$
$$\begin{aligned}
(r_1)_{0} &= 1 - \tfrac{72}{65} = \frac{65 - 72}{65} = -\tfrac{7}{65} \\
(r_1)_{1} &= 2 - \tfrac{126}{65} = \frac{130 - 126}{65} = \tfrac{4}{65}
\end{aligned}$$

$$\mathbf r_1 = \begin{bmatrix}-\tfrac{7}{65} \\ \tfrac{4}{65}\end{bmatrix}$$

**2. Multiply** $\mathbf A\mathbf r_1$:
$$\begin{aligned}
(\mathbf A\mathbf r_1)_{0} &= 2\left(-\tfrac{7}{65}\right) + 1\left(\tfrac{4}{65}\right) = -\tfrac{14}{65} + \tfrac{4}{65} = \frac{-14 + 4}{65} = -\tfrac{2}{13} \\
(\mathbf A\mathbf r_1)_{1} &= 1\left(-\tfrac{7}{65}\right) + 3\left(\tfrac{4}{65}\right) = -\tfrac{7}{65} + \tfrac{12}{65} = \frac{-7 + 12}{65} = \tfrac{1}{13}
\end{aligned}$$

$$\mathbf A\mathbf r_1 = \begin{bmatrix}-\tfrac{2}{13} \\ \tfrac{1}{13}\end{bmatrix}$$

**3. Top and bottom of d:**
$$\begin{aligned}
\mathbf r_1^T(\mathbf A\mathbf r_1) &= \left(-\tfrac{7}{65}\right)\left(-\tfrac{2}{13}\right) + \left(\tfrac{4}{65}\right)\left(\tfrac{1}{13}\right) = \tfrac{14}{845} + \tfrac{4}{845} = \frac{14 + 4}{845} = \tfrac{18}{845} \\
(\mathbf A\mathbf r_1)^T(\mathbf A\mathbf r_1) &= \left(-\tfrac{2}{13}\right)\left(-\tfrac{2}{13}\right) + \left(\tfrac{1}{13}\right)\left(\tfrac{1}{13}\right) = \tfrac{4}{169} + \tfrac{1}{169} = \frac{4 + 1}{169} = \tfrac{5}{169}
\end{aligned}$$

**4. Step length:**

$$d_1 = \frac{\tfrac{18}{845}}{\tfrac{5}{169}} = \tfrac{18}{25} \approx 0.72$$

**5. Update** $\mathbf x_2 = \mathbf x_1 + d_1\mathbf r_1$:
$$\begin{aligned}
(x_2)_{0} &= \tfrac{18}{65} + \left(\tfrac{18}{25}\right)\left(-\tfrac{7}{65}\right) = \tfrac{18}{65} - \tfrac{126}{1625} = \frac{450 - 126}{1625} = \tfrac{324}{1625} \\
(x_2)_{1} &= \tfrac{36}{65} + \left(\tfrac{18}{25}\right)\left(\tfrac{4}{65}\right) = \tfrac{36}{65} + \tfrac{72}{1625} = \frac{900 + 72}{1625} = \tfrac{972}{1625}
\end{aligned}$$

$$\mathbf x_2 = \begin{bmatrix}\tfrac{324}{1625} \\ \tfrac{972}{1625}\end{bmatrix} \approx \begin{bmatrix} 0.199385 \\ 0.598154 \end{bmatrix}$$

### Check: residual after two steps

$$\begin{aligned}
(\mathbf A\mathbf x_2)_{0} &= 2\left(\tfrac{324}{1625}\right) + 1\left(\tfrac{972}{1625}\right) = \tfrac{648}{1625} + \tfrac{972}{1625} = \frac{648 + 972}{1625} = \tfrac{324}{325} \\
(\mathbf A\mathbf x_2)_{1} &= 1\left(\tfrac{324}{1625}\right) + 3\left(\tfrac{972}{1625}\right) = \tfrac{324}{1625} + \tfrac{2916}{1625} = \frac{324 + 2916}{1625} = \tfrac{648}{325}
\end{aligned}$$
$$\begin{aligned}
(r_2)_{0} &= 1 - \tfrac{324}{325} = \frac{325 - 324}{325} = \tfrac{1}{325} \\
(r_2)_{1} &= 2 - \tfrac{648}{325} = \frac{650 - 648}{325} = \tfrac{2}{325}
\end{aligned}$$

$$\mathbf r_2 = \begin{bmatrix}\tfrac{1}{325} \\ \tfrac{2}{325}\end{bmatrix},\qquad \|\mathbf r_2\| \approx 0.0069\quad(\text{SD had } 0.0177)$$

<details>
<summary>Note: MRA vs SD here</summary>

MRA's steps are almost the same size as SD's here ($\tfrac{18}{65}$ vs $\tfrac{5}{18}$). The two only differ much when A is far from symmetric or badly stretched.

</details>

---

## Part 3: conjugate gradient (sl.29, typo fixed), two iterations

CG carries **three** vectors forward: $\mathbf x$ (answer), $\mathbf r$ (residual), $\mathbf p$ (direction). It updates $\mathbf r$ from the previous $\mathbf r$ rather than recomputing $\mathbf b - \mathbf A\mathbf x$, so each step needs only **one** multiply, $\mathbf A\mathbf p$.

**Start:** $\mathbf r_0 = \mathbf b - \mathbf A\mathbf x_0 = \begin{bmatrix}1 \\ 2\end{bmatrix}$, $\;\mathbf p_0 = \mathbf r_0 = \begin{bmatrix}1 \\ 2\end{bmatrix}$.

### Iteration k = 0

**1. Multiply** $\mathbf A\mathbf p_0$ (the only multiply this iteration):
$$\begin{aligned}
(\mathbf A\mathbf p_0)_{0} &= 2(1) + 1(2) = 2 + 2 = 4 \\
(\mathbf A\mathbf p_0)_{1} &= 1(1) + 3(2) = 1 + 6 = 7
\end{aligned}$$

$$\mathbf A\mathbf p_0 = \begin{bmatrix}4 \\ 7\end{bmatrix}$$

**2. Top and bottom of α:**
$$\begin{aligned}
\mathbf r_0^T\mathbf r_0 &= 1(1) + 2(2) = 1 + 4 = 5 \\
\mathbf p_0^T(\mathbf A\mathbf p_0) &= 1(4) + 2(7) = 4 + 14 = 18
\end{aligned}$$

$$\alpha_0 = \frac{5}{18} \approx 0.277778$$

**3. Update x** $= \mathbf x_0 + \alpha_0\mathbf p_0$:
$$\begin{aligned}
(x_1)_{0} &= 0 + \left(\tfrac{5}{18}\right)(1) = \tfrac{5}{18} \\
(x_1)_{1} &= 0 + \left(\tfrac{5}{18}\right)(2) = \tfrac{5}{9}
\end{aligned}$$

$$\mathbf x_1 = \begin{bmatrix}\tfrac{5}{18} \\ \tfrac{5}{9}\end{bmatrix}$$

**4. Update r** $= \mathbf r_0 - \alpha_0\mathbf A\mathbf p_0$ (reuses step 1's $\mathbf A\mathbf p_0$):
$$\begin{aligned}
(r_1)_{0} &= 1 - \left(\tfrac{5}{18}\right)(4) = 1 - \tfrac{10}{9} = \frac{9 - 10}{9} = -\tfrac{1}{9} \\
(r_1)_{1} &= 2 - \left(\tfrac{5}{18}\right)(7) = 2 - \tfrac{35}{18} = \frac{36 - 35}{18} = \tfrac{1}{18}
\end{aligned}$$

$$\mathbf r_1 = \begin{bmatrix}-\tfrac{1}{9} \\ \tfrac{1}{18}\end{bmatrix}$$

**5. β, the share of the old direction to keep:**
$$\begin{aligned}
\mathbf r_1^T\mathbf r_1 &= \left(-\tfrac{1}{9}\right)\left(-\tfrac{1}{9}\right) + \left(\tfrac{1}{18}\right)\left(\tfrac{1}{18}\right) = \tfrac{1}{81} + \tfrac{1}{324} = \frac{4 + 1}{324} = \tfrac{5}{324}
\end{aligned}$$

$$\beta_0 = \frac{\mathbf r_1^T\mathbf r_1}{\mathbf r_0^T\mathbf r_0} = \frac{\tfrac{5}{324}}{5} = \tfrac{1}{324}$$

**6. New direction** $\mathbf p_1 = \mathbf r_1 + \beta_0\mathbf p_0$:
$$\begin{aligned}
(p_1)_{0} &= -\tfrac{1}{9} + \left(\tfrac{1}{324}\right)(1) = -\tfrac{1}{9} + \tfrac{1}{324} = \frac{-36 + 1}{324} = -\tfrac{35}{324} \\
(p_1)_{1} &= \tfrac{1}{18} + \left(\tfrac{1}{324}\right)(2) = \tfrac{1}{18} + \tfrac{1}{162} = \frac{9 + 1}{162} = \tfrac{5}{81}
\end{aligned}$$

$$\mathbf p_1 = \begin{bmatrix}-\tfrac{35}{324} \\ \tfrac{5}{81}\end{bmatrix}$$

### Iteration k = 1

**1. Multiply** $\mathbf A\mathbf p_1$ (the only multiply this iteration):
$$\begin{aligned}
(\mathbf A\mathbf p_1)_{0} &= 2\left(-\tfrac{35}{324}\right) + 1\left(\tfrac{5}{81}\right) = -\tfrac{35}{162} + \tfrac{5}{81} = \frac{-35 + 10}{162} = -\tfrac{25}{162} \\
(\mathbf A\mathbf p_1)_{1} &= 1\left(-\tfrac{35}{324}\right) + 3\left(\tfrac{5}{81}\right) = -\tfrac{35}{324} + \tfrac{5}{27} = \frac{-35 + 60}{324} = \tfrac{25}{324}
\end{aligned}$$

$$\mathbf A\mathbf p_1 = \begin{bmatrix}-\tfrac{25}{162} \\ \tfrac{25}{324}\end{bmatrix}$$

**2. Top and bottom of α:**
$$\begin{aligned}
\mathbf r_1^T\mathbf r_1 &= \left(-\tfrac{1}{9}\right)\left(-\tfrac{1}{9}\right) + \left(\tfrac{1}{18}\right)\left(\tfrac{1}{18}\right) = \tfrac{1}{81} + \tfrac{1}{324} = \frac{4 + 1}{324} = \tfrac{5}{324} \\
\mathbf p_1^T(\mathbf A\mathbf p_1) &= \left(-\tfrac{35}{324}\right)\left(-\tfrac{25}{162}\right) + \left(\tfrac{5}{81}\right)\left(\tfrac{25}{324}\right) = \tfrac{875}{52488} + \tfrac{125}{26244} = \frac{875 + 250}{52488} = \tfrac{125}{5832}
\end{aligned}$$

$$\alpha_1 = \frac{\tfrac{5}{324}}{\tfrac{125}{5832}} = \tfrac{18}{25} \approx 0.72$$

**3. Update x** $= \mathbf x_1 + \alpha_1\mathbf p_1$:
$$\begin{aligned}
(x_2)_{0} &= \tfrac{5}{18} + \left(\tfrac{18}{25}\right)\left(-\tfrac{35}{324}\right) = \tfrac{5}{18} - \tfrac{7}{90} = \frac{25 - 7}{90} = \tfrac{1}{5} \\
(x_2)_{1} &= \tfrac{5}{9} + \left(\tfrac{18}{25}\right)\left(\tfrac{5}{81}\right) = \tfrac{5}{9} + \tfrac{2}{45} = \frac{25 + 2}{45} = \tfrac{3}{5}
\end{aligned}$$

$$\mathbf x_2 = \begin{bmatrix}\tfrac{1}{5} \\ \tfrac{3}{5}\end{bmatrix}$$

**4. Update r** $= \mathbf r_1 - \alpha_1\mathbf A\mathbf p_1$ (reuses step 1's $\mathbf A\mathbf p_1$):
$$\begin{aligned}
(r_2)_{0} &= -\tfrac{1}{9} - \left(\tfrac{18}{25}\right)\left(-\tfrac{25}{162}\right) = -\tfrac{1}{9} + \tfrac{1}{9} = \frac{-1 + 1}{9} = 0 \\
(r_2)_{1} &= \tfrac{1}{18} - \left(\tfrac{18}{25}\right)\left(\tfrac{25}{324}\right) = \tfrac{1}{18} - \tfrac{1}{18} = \frac{1 - 1}{18} = 0
\end{aligned}$$

$$\mathbf r_2 = \begin{bmatrix}0 \\ 0\end{bmatrix}$$

### Result

$$\mathbf x_2 = \begin{bmatrix}\tfrac{1}{5} \\ \tfrac{3}{5}\end{bmatrix} = \mathbf x^*,\qquad \mathbf r_2 = \begin{bmatrix}0 \\ 0\end{bmatrix}$$

**Exact answer in N = 2 steps** for this 2×2 (sl.30).

<details>
<summary>Note: why CG lands in 2 steps (added check)</summary>

**Why it lands** *(added check)*: the two directions are **A-conjugate**, meaning $\mathbf p_0^T\mathbf A\mathbf p_1 = 0$:

$$\begin{aligned}
\mathbf p_1^T(\mathbf A\mathbf p_0) &= \left(-\tfrac{35}{324}\right)(4) + \left(\tfrac{5}{81}\right)(7) = -\tfrac{35}{81} + \tfrac{35}{81} = \frac{-35 + 35}{81} = 0
\end{aligned}$$

Plain SD has $\mathbf r_1^T\mathbf r_0 = 0$ (perpendicular in ordinary space), and that isn't enough. "A-perpendicular" is the version that matches the bowl's stretch. A second step along an A-conjugate direction can't undo the first step's progress, so two directions finish a 2-D problem. Picture this in lab panel 5.

</details>

---

## Part 4: Gauss-Jacobi (sl.33), three sweeps

**Split** A into its diagonal and the rest (sl.33):

$$\mathbf A = \begin{bmatrix}2 & 1 \\ 1 & 3\end{bmatrix} = \underbrace{\begin{bmatrix}2 & 0 \\ 0 & 3\end{bmatrix}}_{\mathbf D} + \underbrace{\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}}_{\mathbf E}$$

**Each sweep:** solve $\mathbf D\mathbf x_{k+1} = \mathbf b - \mathbf E\mathbf x_k$. D is diagonal, so "solve" means divide row i by $a_{ii}$. Written out row by row:

$$x_0^{(k+1)} = \frac{1 - x_1^{(k)}}{2},\qquad x_1^{(k+1)} = \frac{2 - x_0^{(k)}}{3}$$

Both lines use only the **old** values $(k)$, so they could run at the same time on two CPUs.

### Sweep 1 (uses $\mathbf x^{(0)} = \begin{bmatrix}0 \\ 0\end{bmatrix}$)

$$\begin{aligned}
x_0^{(1)} &= \frac{1 - 0}{2} = \frac{1}{2} = \tfrac{1}{2} \\
x_1^{(1)} &= \frac{2 - 0}{3} = \frac{2}{3} = \tfrac{2}{3}
\end{aligned}$$

Residual check:
$$\begin{aligned}
(\mathbf A\mathbf x^{(1)})_{0} &= 2\left(\tfrac{1}{2}\right) + 1\left(\tfrac{2}{3}\right) = 1 + \tfrac{2}{3} = \frac{3 + 2}{3} = \tfrac{5}{3} \\
(\mathbf A\mathbf x^{(1)})_{1} &= 1\left(\tfrac{1}{2}\right) + 3\left(\tfrac{2}{3}\right) = \tfrac{1}{2} + 2 = \frac{1 + 4}{2} = \tfrac{5}{2}
\end{aligned}$$
$$\begin{aligned}
r_{0} &= 1 - \tfrac{5}{3} = \frac{3 - 5}{3} = -\tfrac{2}{3} \\
r_{1} &= 2 - \tfrac{5}{2} = \frac{4 - 5}{2} = -\tfrac{1}{2}
\end{aligned}$$

$$\mathbf r^{(1)} = \begin{bmatrix}-\tfrac{2}{3} \\ -\tfrac{1}{2}\end{bmatrix},\qquad \|\mathbf r\| \approx 0.8333$$

### Sweep 2 (uses $\mathbf x^{(1)} = \begin{bmatrix}\tfrac{1}{2} \\ \tfrac{2}{3}\end{bmatrix}$)

$$\begin{aligned}
x_0^{(2)} &= \frac{1 - \left(\tfrac{2}{3}\right)}{2} = \frac{\tfrac{1}{3}}{2} = \tfrac{1}{6} \\
x_1^{(2)} &= \frac{2 - \left(\tfrac{1}{2}\right)}{3} = \frac{\tfrac{3}{2}}{3} = \tfrac{1}{2}
\end{aligned}$$

Residual check:
$$\begin{aligned}
(\mathbf A\mathbf x^{(2)})_{0} &= 2\left(\tfrac{1}{6}\right) + 1\left(\tfrac{1}{2}\right) = \tfrac{1}{3} + \tfrac{1}{2} = \frac{2 + 3}{6} = \tfrac{5}{6} \\
(\mathbf A\mathbf x^{(2)})_{1} &= 1\left(\tfrac{1}{6}\right) + 3\left(\tfrac{1}{2}\right) = \tfrac{1}{6} + \tfrac{3}{2} = \frac{1 + 9}{6} = \tfrac{5}{3}
\end{aligned}$$
$$\begin{aligned}
r_{0} &= 1 - \tfrac{5}{6} = \frac{6 - 5}{6} = \tfrac{1}{6} \\
r_{1} &= 2 - \tfrac{5}{3} = \frac{6 - 5}{3} = \tfrac{1}{3}
\end{aligned}$$

$$\mathbf r^{(2)} = \begin{bmatrix}\tfrac{1}{6} \\ \tfrac{1}{3}\end{bmatrix},\qquad \|\mathbf r\| \approx 0.3727$$

### Sweep 3 (uses $\mathbf x^{(2)} = \begin{bmatrix}\tfrac{1}{6} \\ \tfrac{1}{2}\end{bmatrix}$)

$$\begin{aligned}
x_0^{(3)} &= \frac{1 - \left(\tfrac{1}{2}\right)}{2} = \frac{\tfrac{1}{2}}{2} = \tfrac{1}{4} \\
x_1^{(3)} &= \frac{2 - \left(\tfrac{1}{6}\right)}{3} = \frac{\tfrac{11}{6}}{3} = \tfrac{11}{18}
\end{aligned}$$

Residual check:
$$\begin{aligned}
(\mathbf A\mathbf x^{(3)})_{0} &= 2\left(\tfrac{1}{4}\right) + 1\left(\tfrac{11}{18}\right) = \tfrac{1}{2} + \tfrac{11}{18} = \frac{9 + 11}{18} = \tfrac{10}{9} \\
(\mathbf A\mathbf x^{(3)})_{1} &= 1\left(\tfrac{1}{4}\right) + 3\left(\tfrac{11}{18}\right) = \tfrac{1}{4} + \tfrac{11}{6} = \frac{3 + 22}{12} = \tfrac{25}{12}
\end{aligned}$$
$$\begin{aligned}
r_{0} &= 1 - \tfrac{10}{9} = \frac{9 - 10}{9} = -\tfrac{1}{9} \\
r_{1} &= 2 - \tfrac{25}{12} = \frac{24 - 25}{12} = -\tfrac{1}{12}
\end{aligned}$$

$$\mathbf r^{(3)} = \begin{bmatrix}-\tfrac{1}{9} \\ -\tfrac{1}{12}\end{bmatrix},\qquad \|\mathbf r\| \approx 0.1389$$

---

## Part 5: Gauss-Seidel (sl.33 "search the web"), three sweeps

**The one change from Jacobi:** row 1 uses the $x_0$ that row 0 **has just computed** in this sweep, not last sweep's.

$$x_0^{(k+1)} = \frac{1 - x_1^{(k)}}{2},\qquad x_1^{(k+1)} = \frac{2 - x_0^{(\mathbf{k+1})}}{3}$$

<details>
<summary>Note: matrix form of Gauss-Seidel (added)</summary>

Matrix form *(added)*: split $\mathbf A = \mathbf L_* + \mathbf D + \mathbf U_*$ (strictly lower, diagonal, strictly upper) and solve $(\mathbf D + \mathbf L_*)\mathbf x_{k+1} = \mathbf b - \mathbf U_*\mathbf x_k$. That's a lower-triangular solve, which is still easy (forward substitution, A2).

</details>

### Sweep 1 (starts from $\mathbf x^{(0)} = \begin{bmatrix}0 \\ 0\end{bmatrix}$)

$$\begin{aligned}
x_0^{(1)} &= \frac{1 - 0}{2} = \frac{1}{2} = \tfrac{1}{2} \\
x_1^{(1)} &= \frac{2 - \left(\tfrac{1}{2}\right)}{3} = \frac{\tfrac{3}{2}}{3} = \tfrac{1}{2} \quad\leftarrow\text{uses the new }x_0
\end{aligned}$$

Residual check:
$$\begin{aligned}
(\mathbf A\mathbf x^{(1)})_{0} &= 2\left(\tfrac{1}{2}\right) + 1\left(\tfrac{1}{2}\right) = 1 + \tfrac{1}{2} = \frac{2 + 1}{2} = \tfrac{3}{2} \\
(\mathbf A\mathbf x^{(1)})_{1} &= 1\left(\tfrac{1}{2}\right) + 3\left(\tfrac{1}{2}\right) = \tfrac{1}{2} + \tfrac{3}{2} = \frac{1 + 3}{2} = 2
\end{aligned}$$
$$\begin{aligned}
r_{0} &= 1 - \tfrac{3}{2} = \frac{2 - 3}{2} = -\tfrac{1}{2} \\
r_{1} &= 2 - 2 = 0
\end{aligned}$$

$$\mathbf r^{(1)} = \begin{bmatrix}-\tfrac{1}{2} \\ 0\end{bmatrix},\qquad \|\mathbf r\| \approx 0.5000$$

### Sweep 2 (starts from $\mathbf x^{(1)} = \begin{bmatrix}\tfrac{1}{2} \\ \tfrac{1}{2}\end{bmatrix}$)

$$\begin{aligned}
x_0^{(2)} &= \frac{1 - \left(\tfrac{1}{2}\right)}{2} = \frac{\tfrac{1}{2}}{2} = \tfrac{1}{4} \\
x_1^{(2)} &= \frac{2 - \left(\tfrac{1}{4}\right)}{3} = \frac{\tfrac{7}{4}}{3} = \tfrac{7}{12} \quad\leftarrow\text{uses the new }x_0
\end{aligned}$$

Residual check:
$$\begin{aligned}
(\mathbf A\mathbf x^{(2)})_{0} &= 2\left(\tfrac{1}{4}\right) + 1\left(\tfrac{7}{12}\right) = \tfrac{1}{2} + \tfrac{7}{12} = \frac{6 + 7}{12} = \tfrac{13}{12} \\
(\mathbf A\mathbf x^{(2)})_{1} &= 1\left(\tfrac{1}{4}\right) + 3\left(\tfrac{7}{12}\right) = \tfrac{1}{4} + \tfrac{7}{4} = \frac{1 + 7}{4} = 2
\end{aligned}$$
$$\begin{aligned}
r_{0} &= 1 - \tfrac{13}{12} = \frac{12 - 13}{12} = -\tfrac{1}{12} \\
r_{1} &= 2 - 2 = 0
\end{aligned}$$

$$\mathbf r^{(2)} = \begin{bmatrix}-\tfrac{1}{12} \\ 0\end{bmatrix},\qquad \|\mathbf r\| \approx 0.0833$$

### Sweep 3 (starts from $\mathbf x^{(2)} = \begin{bmatrix}\tfrac{1}{4} \\ \tfrac{7}{12}\end{bmatrix}$)

$$\begin{aligned}
x_0^{(3)} &= \frac{1 - \left(\tfrac{7}{12}\right)}{2} = \frac{\tfrac{5}{12}}{2} = \tfrac{5}{24} \\
x_1^{(3)} &= \frac{2 - \left(\tfrac{5}{24}\right)}{3} = \frac{\tfrac{43}{24}}{3} = \tfrac{43}{72} \quad\leftarrow\text{uses the new }x_0
\end{aligned}$$

Residual check:
$$\begin{aligned}
(\mathbf A\mathbf x^{(3)})_{0} &= 2\left(\tfrac{5}{24}\right) + 1\left(\tfrac{43}{72}\right) = \tfrac{5}{12} + \tfrac{43}{72} = \frac{30 + 43}{72} = \tfrac{73}{72} \\
(\mathbf A\mathbf x^{(3)})_{1} &= 1\left(\tfrac{5}{24}\right) + 3\left(\tfrac{43}{72}\right) = \tfrac{5}{24} + \tfrac{43}{24} = \frac{5 + 43}{24} = 2
\end{aligned}$$
$$\begin{aligned}
r_{0} &= 1 - \tfrac{73}{72} = \frac{72 - 73}{72} = -\tfrac{1}{72} \\
r_{1} &= 2 - 2 = 0
\end{aligned}$$

$$\mathbf r^{(3)} = \begin{bmatrix}-\tfrac{1}{72} \\ 0\end{bmatrix},\qquad \|\mathbf r\| \approx 0.0139$$

<details>
<summary>Note: what to notice (added)</summary>

**What to notice** *(added)*:
- GS's $r_1$ is **0 after every sweep**. Row 1 was just solved exactly using the newest $x_0$.
- Residual sizes: Jacobi 0.833 → 0.373 → 0.139. Gauss-Seidel 0.500 → 0.083 → 0.014, shrinking ×\tfrac{1}{6} every sweep.
- Gauss-Seidel loses Jacobi's "all rows at once" parallelism: row 1 has to wait for row 0.

</details>

### Scoreboard: iterations until $\|\mathbf r\|/\|\mathbf b\| < 10^{-6}$ (matches the practical's table)

| CG | MRA | SD | Gauss-Seidel | Jacobi |
|---|---|---|---|---|
| 2 | 5 | 6 | 8 | 16 |

---

## Part 6: power method (sl.19–20) on the same A

Start from $\mathbf x_0 = (1, 0)$ *(my choice; any start with some of the dominant eigenvector works)*. Repeat $\mathbf x_k = \mathbf A\mathbf x_{k-1}$. Watch two things: the **shape** (ratio $x_1/x_0$) and the **growth** (how much each step multiplies the size).

From Part 0a the eigenvalues are $k_0 = \tfrac{5+\sqrt5}{2} = 3.618$ and $k_1 = 1.382$. The dominant eigenvector has shape $x_1/x_0 = k_0 - 2 = 1.618$ (from row 0 of $(\mathbf A - k_0\mathbf I)\mathbf x = 0$: $(2-k_0)x_0 + x_1 = 0$).

**k = 1:**
$$\begin{aligned}
(x_1)_{0} &= 2(1) + 1(0) = 2 \\
(x_1)_{1} &= 1(1) + 3(0) = 1
\end{aligned}$$

**k = 2:**
$$\begin{aligned}
(x_2)_{0} &= 2(2) + 1(1) = 4 + 1 = 5 \\
(x_2)_{1} &= 1(2) + 3(1) = 2 + 3 = 5
\end{aligned}$$

**k = 3:**
$$\begin{aligned}
(x_3)_{0} &= 2(5) + 1(5) = 10 + 5 = 15 \\
(x_3)_{1} &= 1(5) + 3(5) = 5 + 15 = 20
\end{aligned}$$

**k = 4:**
$$\begin{aligned}
(x_4)_{0} &= 2(15) + 1(20) = 30 + 20 = 50 \\
(x_4)_{1} &= 1(15) + 3(20) = 15 + 60 = 75
\end{aligned}$$

**k = 5:**
$$\begin{aligned}
(x_5)_{0} &= 2(50) + 1(75) = 100 + 75 = 175 \\
(x_5)_{1} &= 1(50) + 3(75) = 50 + 225 = 275
\end{aligned}$$

**k = 6:**
$$\begin{aligned}
(x_6)_{0} &= 2(175) + 1(275) = 350 + 275 = 625 \\
(x_6)_{1} &= 1(175) + 3(275) = 175 + 825 = 1000
\end{aligned}$$

**k = 7:**
$$\begin{aligned}
(x_7)_{0} &= 2(625) + 1(1000) = 1250 + 1000 = 2250 \\
(x_7)_{1} &= 1(625) + 3(1000) = 625 + 3000 = 3625
\end{aligned}$$

**k = 8:**
$$\begin{aligned}
(x_8)_{0} &= 2(2250) + 1(3625) = 4500 + 3625 = 8125 \\
(x_8)_{1} &= 1(2250) + 3(3625) = 2250 + 10875 = 13125
\end{aligned}$$

| k | $\mathbf x_k$ | shape $x_1/x_0$ | growth $\|\mathbf x_k\|/\|\mathbf x_{k-1}\|$ |
|---|---|---|---|
| 1 | (2, 1) | 0.5000 | 2.2361 |
| 2 | (5, 5) | 1.0000 | 3.1623 |
| 3 | (15, 20) | 1.3333 | 3.5355 |
| 4 | (50, 75) | 1.5000 | 3.6056 |
| 5 | (175, 275) | 1.5714 | 3.6162 |
| 6 | (625, 1000) | 1.6000 | 3.6178 |
| 7 | (2250, 3625) | 1.6111 | 3.6180 |
| 8 | (8125, 13125) | 1.6154 | 3.6180 |

<details>
<summary>Note: what the table shows</summary>

- The shape heads to **1.618**, the dominant eigenvector. The other part shrinks relative to it as $(k_1/k_0)^N = (0.382)^N$.
- The growth heads to **3.618 = $k_0$**. That's sl.21's point: the size scales as $k_0^N$, so you can read off the eigenvalue too.
- If $k_0 < 1$ the vector would **shrink** each step but still turn toward the same shape. The shape comes from the *ratio* of the k's, not from their size.

</details>

---

## Part 7: CSR storage (sl.9) and the memory sum (sl.11)

### 7a. The slide's CSR example (sl.9)

$$\mathbf B = \begin{bmatrix} \cdot & B_{01} & \cdot & \cdot \\ \cdot & \cdot & \cdot & B_{13} \\ B_{20} & B_{21} & \cdot & \cdot \\ \cdot & \cdot & \cdot & B_{33}\end{bmatrix}$$

The slide stores three lists, read row by row:

| Row | count | positions (column numbers) | values |
|---|---|---|---|
| 0 | 1 | 1 | $B_{01}$ |
| 1 | 1 | 3 | $B_{13}$ |
| 2 | 2 | 0, 1 | $B_{20}, B_{21}$ |
| 3 | 1 | 3 | $B_{33}$ |

<details>
<summary>Note: textbook CSR (added)</summary>

(Textbook CSR stores running totals of the counts, 0, 1, 2, 4, 5, instead of the counts themselves. It's the same information *(added)*.)

</details>

### 7b. Write the CSR of a 1D chain (tridiagonal, like sl.37) and multiply with it *(added numbers)*

$$\mathbf T = \begin{bmatrix}2 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 2\end{bmatrix},\qquad \mathbf v = \begin{bmatrix}1\\2\\3\\4\end{bmatrix}$$

| Row | count | positions | values |
|---|---|---|---|
| 0 | 2 | 0, 1 | 2, -1 |
| 1 | 3 | 0, 1, 2 | -1, 2, -1 |
| 2 | 3 | 1, 2, 3 | -1, 2, -1 |
| 3 | 2 | 2, 3 | -1, 2 |

**Multiply using only the stored entries.** For each row, walk its positions list:

$$\begin{aligned}
(\mathbf T\mathbf v)_0 &= 2(1) + \left(-1\right)(2) = 2 - 2 = 0 \quad(\text{positions } 0,1) \\
(\mathbf T\mathbf v)_1 &= \left(-1\right)(1) + 2(2) + \left(-1\right)(3) = -1 + 4 - 3 = 0 \quad(\text{positions } 0,1,2) \\
(\mathbf T\mathbf v)_2 &= \left(-1\right)(2) + 2(3) + \left(-1\right)(4) = -2 + 6 - 4 = 0 \quad(\text{positions } 1,2,3) \\
(\mathbf T\mathbf v)_3 &= \left(-1\right)(3) + 2(4) = -3 + 8 = 5 \quad(\text{positions } 2,3)
\end{aligned}$$

$$\mathbf T\mathbf v = \begin{bmatrix}0 \\ 0 \\ 0 \\ 5\end{bmatrix}$$

**10 multiplies instead of 16.** For an N×N chain it's about 3N instead of N². No "if not zero" tests are needed (sl.8), because zeros simply aren't in the list.

### 7c. The memory sum (sl.11)

N = 10⁸ unknowns, each connected to ~7 (so ~7N non-zeros). The slide's sizes: 16 bytes per value, 4 bytes per integer.

- **Dense:** $N^2 = 10^{16}$ values × 16 B $= 1.6\times10^{17}$ B $= 160$ PB
- **CSR:** counts $10^8 × 4$ B $= 0.4$ GB, plus positions $7\times10^8 × 4$ B $= 2.8$ GB, plus values $7\times10^8 × 16$ B $= 11.2$ GB. Total $= 14.4\times10^9$ B $= 13.4$ GiB ✓ (the slide's 13.4 is in GiB)
<details>
<summary>Note: a real double is 8 B</summary>

- Slide note: a real double is **8 B**. With 8 B: dense 80 PB, CSR $8.8\times10^9$ B $= 8.2$ GiB. The conclusion is the same: dense is impossible and sparse fits in a workstation.

</details>

---

## Part 8: domain decomposition, block LU (sl.50–54), on a 5-node chain *(added numbers)*

A 1D thermal chain (an RC ladder, sl.36–37) with 5 nodes. Each node couples to its neighbours: $2x_j - x_{j-1} - x_{j+1} = 1$.

- **Domain a** = nodes 0, 1 (CPU a). **Domain c** = nodes 3, 4 (CPU c). **Interface i** = node 2.
- Order the unknowns as $(x_0, x_1 \,|\, x_3, x_4 \,|\, x_2)$: domains first, interface last (sl.51).

$$\left[\begin{array}{cc|cc|c} 2 & -1 & 0 & 0 & 0 \\ -1 & 2 & 0 & 0 & -1 \\ \hline 0 & 0 & 2 & -1 & -1 \\ 0 & 0 & -1 & 2 & 0 \\ \hline 0 & -1 & -1 & 0 & 2 \end{array}\right]\begin{bmatrix} x_0 \\ x_1 \\ x_3 \\ x_4 \\ x_2 \end{bmatrix} = \begin{bmatrix} 1\\1\\1\\1\\1 \end{bmatrix}$$

In sl.52's names:
- $\tilde{\mathbf A}$ = top-left 4×4 = two **separate** 2×2 blocks $\mathbf A_{aa} = \mathbf A_{cc} = \begin{bmatrix}2&-1\\-1&2\end{bmatrix}$. No coupling between a and c, so each CPU handles its own.
- $\tilde{\mathbf B} = (0, -1, -1, 0)^T$ is the column linking the domains to the interface. $\tilde{\mathbf C} = \tilde{\mathbf B}^T$, and $\tilde{\mathbf D} = 2$.

### 8a. LU of each domain block (each CPU does this for its own block, in parallel)

A2's LU with 1s on L's diagonal (sl.48). Kill $a_{10} = -1$ using multiplier $l_{10} = -1/2$:

$$\mathbf A_{aa} = \begin{bmatrix}2&-1\\-1&2\end{bmatrix} = \underbrace{\begin{bmatrix}1&0\\-\tfrac12&1\end{bmatrix}}_{\mathbf L}\underbrace{\begin{bmatrix}2&-1\\0&\tfrac32\end{bmatrix}}_{\mathbf U}\qquad(\text{check: } u_{11} = 2 - (-\tfrac12)(-1) = \tfrac32)$$

Block c is the same matrix, so it has the same L and U.

### 8b. Forward half (sl.53 top box)

**Step 1, $\mathbf L\mathbf y_{abc} = \mathbf b_{abc}$**, one lower-triangular solve per CPU:

CPU a:
$$\begin{aligned}
y^a_0 &= 1 \\
y^a_1 &= 1 - \left(-\tfrac{1}{2}\right)(1) = \tfrac{3}{2}
\end{aligned}$$
CPU c:
$$\begin{aligned}
y^c_0 &= 1 \\
y^c_1 &= 1 - \left(-\tfrac{1}{2}\right)(1) = \tfrac{3}{2}
\end{aligned}$$

**Step 2, $\mathbf U\mathbf z = \mathbf y_{abc}$** (upper solve), then $y_i = b_i - \tilde{\mathbf C}\mathbf z$:

CPU a:
$$\begin{aligned}
z^a_1 &= \frac{\tfrac{3}{2}}{\tfrac{3}{2}} = 1 \\
z^a_0 &= \frac{1 - \left(-1\right)(1)}{2} = \frac{2}{2} = 1
\end{aligned}$$
CPU c:
$$\begin{aligned}
z^c_1 &= \frac{\tfrac{3}{2}}{\tfrac{3}{2}} = 1 \\
z^c_0 &= \frac{1 - \left(-1\right)(1)}{2} = \frac{2}{2} = 1
\end{aligned}$$

Combine at the interface (the only step that needs both CPUs' results):
$$\begin{aligned}
\tilde{\mathbf C}\mathbf z &= 0(1) + \left(-1\right)(1) + \left(-1\right)(1) + 0(1) = -1 - 1 = -2 \\
y_i &= b_i - \tilde{\mathbf C}\mathbf z = 1 - \left(-2\right) = 3
\end{aligned}$$

### 8c. The Schur complement: the one dense solve (sl.52–54)

$\mathbf S = \tilde{\mathbf D} - \tilde{\mathbf C}\tilde{\mathbf A}^{-1}\tilde{\mathbf B}$. To get $\tilde{\mathbf A}^{-1}\tilde{\mathbf B}$, each CPU solves its block against its slice of $\tilde{\mathbf B}$ (LU forward, then back):

CPU a, right-hand side $(0, -1)$:
$$\begin{aligned}
g^a_0 &= 0 \\
g^a_1 &= -1 - \left(-\tfrac{1}{2}\right)(0) = -1 \\
h^a_1 &= \frac{-1}{\tfrac{3}{2}} = -\tfrac{2}{3} \\
h^a_0 &= \frac{0 - \left(-1\right)\left(-\tfrac{2}{3}\right)}{2} = \frac{-\tfrac{2}{3}}{2} = -\tfrac{1}{3}
\end{aligned}$$
CPU c, right-hand side $(-1, 0)$:
$$\begin{aligned}
g^c_0 &= -1 \\
g^c_1 &= 0 - \left(-\tfrac{1}{2}\right)(-1) = -\tfrac{1}{2} \\
h^c_1 &= \frac{-\tfrac{1}{2}}{\tfrac{3}{2}} = -\tfrac{1}{3} \\
h^c_0 &= \frac{-1 - \left(-1\right)\left(-\tfrac{1}{3}\right)}{2} = \frac{-\tfrac{4}{3}}{2} = -\tfrac{2}{3}
\end{aligned}$$
$$\begin{aligned}
\tilde{\mathbf C}\tilde{\mathbf A}^{-1}\tilde{\mathbf B} &= 0\left(-\tfrac{1}{3}\right) + \left(-1\right)\left(-\tfrac{2}{3}\right) + \left(-1\right)\left(-\tfrac{2}{3}\right) + 0\left(-\tfrac{1}{3}\right) = \tfrac{2}{3} + \tfrac{2}{3} = \frac{2 + 2}{3} = \tfrac{4}{3} \\
S &= \tilde{\mathbf D} - \left(\tfrac{4}{3}\right) = 2 - \left(\tfrac{4}{3}\right) = \tfrac{2}{3}
\end{aligned}$$

**Dense solve** $S\,x_i = y_i$: $\;x_2 = x_i = \dfrac{3}{\tfrac{2}{3}} = \tfrac{9}{2}$

<details>
<summary>Note: size of S in general</summary>

Here S is 1×1 because there's 1 interface node. On sl.50's grid S is (number of interface nodes)², which is dense but **much smaller than N×N**.

</details>

### 8d. Back half (sl.53 bottom box), parallel again

**Step 3, $\mathbf L\mathbf w = \tilde{\mathbf B}x_i$**, then **$\mathbf U\mathbf x_{abc} = \mathbf y_{abc} - \mathbf w$**:

CPU a: $\tilde{\mathbf B}_a x_i = \begin{bmatrix}0 \\ -\tfrac{9}{2}\end{bmatrix}$
$$\begin{aligned}
w^a_0 &= 0 \\
w^a_1 &= -\tfrac{9}{2} - \left(-\tfrac{1}{2}\right)(0) = -\tfrac{9}{2} \\
\mathbf y^a - \mathbf w^a &= (1 - 0,\; \tfrac{3}{2} - \left(-\tfrac{9}{2}\right)) = (1, 6) \\
x^a_1 &= \frac{6}{\tfrac{3}{2}} = 4 \\
x^a_0 &= \frac{1 - \left(-1\right)(4)}{2} = \frac{5}{2}
\end{aligned}$$
CPU c: $\tilde{\mathbf B}_c x_i = \begin{bmatrix}-\tfrac{9}{2} \\ 0\end{bmatrix}$
$$\begin{aligned}
w^c_0 &= -\tfrac{9}{2} \\
w^c_1 &= 0 - \left(-\tfrac{1}{2}\right)\left(-\tfrac{9}{2}\right) = -\tfrac{9}{4} \\
\mathbf y^c - \mathbf w^c &= (1 - \left(-\tfrac{9}{2}\right),\; \tfrac{3}{2} - \left(-\tfrac{9}{4}\right)) = (\tfrac{11}{2}, \tfrac{15}{4}) \\
x^c_1 &= \frac{\tfrac{15}{4}}{\tfrac{3}{2}} = \tfrac{5}{2} \\
x^c_0 &= \frac{\tfrac{11}{2} - \left(-1\right)\left(\tfrac{5}{2}\right)}{2} = \frac{8}{2} = 4
\end{aligned}$$

**Answer** in node order $(x_0, \dots, x_4)$: $(\tfrac{5}{2}, 4, \tfrac{9}{2}, 4, \tfrac{5}{2}) = (2.5, 4, 4.5, 4, 2.5)$. It's symmetric, as the symmetric chain predicts.

**Check row 2:** $-x_1 + 2x_2 - x_3 = -4 + 9 - 4 = 1$ ✓

<details>
<summary>Note: where the parallelism is</summary>

**Where the parallelism is:** every triangular solve ran on one block only (CPU a or CPU c). Only two things needed both CPUs: the interface sums ($y_i$ and S) and the one small dense solve. Ordinary LU (sl.48) builds row k from rows above it, so its rows can't be handed out to different CPUs.

</details>


---

## Part 9: discussion recall (sl.28: "discuss the issues influencing the choices")

| Question | One-line answer (slide) |
|---|---|
| Why are engineering matrices sparse? | Entries are connections, and each node connects to only a few neighbours (~7N non-zeros of N²) (sl.3–6) |
| Why not skip zeros with `if` tests? | The tests cost more than the multiplies saved. Use CSR instead (sl.8–9) |
| Why not QR/LU on a sparse A? | The factors fill in (Q and R are dense), and N² storage is impossible at N = 10⁸ (sl.10–11) |
| Iterative idea | Guess → residual r = b − Ax (one sparse multiply) → adjust. Only multiplies, which are cheap and parallel (sl.13–17) |
| What separates the methods? | The adjustment rule: direction and step length (sl.15) |
| How to judge convergence | Plot ‖r‖ on a log scale against iteration. It falls, then levels off at machine precision (sl.17) |
| Power method | x ← Ax picks out the dominant eigenvector, and the growth rate gives k₀ (sl.19–21) |
| SD vs MRA vs CG | SD needs SPD. MRA needs only positive definite. CG on SPD is exact in ≤ N steps in theory, but rounding breaks that in practice (sl.25–30) |
| When is CG fast? | Close to diagonal (diagonally dominant): 1–2 iterations (sl.31) |
| Preconditioning | A sparse Z ≈ A⁻¹, then solve ZAx = Zb with ZA ≈ I. "If not converged in ~100 iterations, it never will": preconditioning is critical (sl.32, 34) |
| Jacobi | Split A = D + E. Each sweep is an easy diagonal solve. Can also serve as a preconditioner (sl.33) |
| Structured matrices | 1D diffusion and wave give tridiagonal matrices, 2D grids give banded ones. Specialised LU and eigen routines are fast, and cost grows with the bandwidth (sl.36–40) |
| Does node ordering matter? | Not for the answer. It matters for speed (banded vs scattered) and also for accuracy, because of rounding (sl.41) |
| Unstructured (triangle) mesh | Pro: fewer nodes for the same accuracy. Con: no pattern, so you need general iterative methods (sl.42–43) |
| Parallel: what's easy? | Matrix multiply, because each row of y is independent. So iterative methods parallelise well (sl.47, 55) |
| Parallel: what's hard? | Direct LU, because each row needs the rows above it (sl.48) |
| Domain decomposition | Split into blocks that meet only at interfaces → block LU. Block solves run in parallel, and the only dense part is the small Schur complement $\tilde{\mathbf D} - \tilde{\mathbf C}\tilde{\mathbf A}^{-1}\tilde{\mathbf B}$ (sl.50–54) |
