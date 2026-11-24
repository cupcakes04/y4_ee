# A3 eigen: worked examples

**What this page is for:** worked calculations, every step written out. Read an example, cover the solution, then redo it on paper.
**Concepts and gaps** live in the [A3 eigen lab](https://claude.ai/artifact/2snCA8AUw4sUWqbbmrHcdb) (`A3_eigen_lab.html`, same folder).
Notation follows the A3 slides: eigenvalues $k_i$, eigenvectors as the columns of $\mathbf X$, $\mathbf d = \mathbf X^T\mathbf b$, $c_i = d_i/k_i$, $\mathbf x = \mathbf X\mathbf c$.
Progress: [`progress.md`](progress.md).

<details>
<summary>Note: sources</summary>

Part A is A3 sl.34–35, numbers verbatim. Part B's problem comes from the practical session and is kept exactly as given. Part C applies A3 sl.30–32 and 39–41 to Part B's matrix. Every number here was recomputed with sympy (2026-11-19). Tips I added that aren't on the slides are tagged *(added)*.

</details>

**The recipe** (from A3 sl.24–35):
1. $\det(\mathbf A - k\mathbf I) = 0$ → eigenvalues $k_i$
2. $(\mathbf A - k_i\mathbf I)\mathbf x_i = \mathbf 0$ → eigenvectors $\mathbf x_i$ (set one element to 1 and solve for the rest)
3. Check the eigenvectors are perpendicular, then normalise them → $\mathbf X$
4. Solve with three moves: $\mathbf d = \mathbf X^T\mathbf b$ → $c_i = d_i / k_i$ → $\mathbf x = \mathbf X\mathbf c$

---

## Part A: warm-up, 2×2 (A3 sl.35)

### A1. Find all the eigensolutions of $\mathbf A = \begin{bmatrix}1 & 2\\ 2 & 5\end{bmatrix}$.

**Solution**

**Eigenvalues.** Use the 2×2 determinant $ad - bc$ (sl.34):

$$\det(\mathbf A - k\mathbf I) = (1-k)(5-k) - 2\cdot 2 = 5 - 6k + k^2 - 4 = k^2 - 6k + 1 = 0$$

$$k = \frac{6 \pm \sqrt{36 - 4}}{2} = 3 \pm 2\sqrt2 \quad\Rightarrow\quad k_0 = 0.172,\; k_1 = 5.83$$

**Eigenvectors.** Set the first element to 1 (the slide's choice). The top row of $(\mathbf A - k_i\mathbf I)\mathbf x_i = \mathbf 0$ then reads:

$$(1 - k_i)\cdot 1 + 2\,x_{i1} = 0 \;\Rightarrow\; x_{i1} = -\frac{1-k_i}{2}$$

- $k_0 = 0.172$: $x_{01} = -\frac{0.828}{2} = -0.414$, so $\mathbf x_0 = (1,\,-0.41)$
- $k_1 = 5.83$: $x_{11} = -\frac{-4.83}{2} = 2.414$, so $\mathbf x_1 = (1,\,2.41)$

**Check.** Dot product: $1\cdot1 + (-0.414)(2.414) = 1 - 1.000 = 0$ ✓. They're perpendicular, as expected for a symmetric $\mathbf A$.

---

## Part B: the practical problem, 3×3

$$\mathbf A = \begin{bmatrix} 3 & -2 & -1 \\ -2 & 3 & 1 \\ -1 & 1 & 4 \end{bmatrix},\qquad \mathbf b = \begin{bmatrix} -4 \\ 7 \\ 13 \end{bmatrix}$$

$\mathbf A$ is symmetric ($\mathbf A^T = \mathbf A$), so it has perpendicular eigenvectors and $\mathbf X^T = \mathbf X^{-1}$ (sl.26).

### B1. Write out $\det(\mathbf A - k\mathbf I)$ as a cubic in $k$ and find the three eigenvalues.

**Solution**

$$\mathbf A - k\mathbf I = \begin{bmatrix} 3-k & -2 & -1 \\ -2 & 3-k & 1 \\ -1 & 1 & 4-k \end{bmatrix}$$

**Cofactor expansion along row 0.** The signs go $+,-,+$:

$$\det = (3-k)\begin{vmatrix}3-k & 1\\ 1 & 4-k\end{vmatrix} - (-2)\begin{vmatrix}-2 & 1\\ -1 & 4-k\end{vmatrix} + (-1)\begin{vmatrix}-2 & 3-k\\ -1 & 1\end{vmatrix}$$

The three 2×2 minors:
- $\begin{vmatrix}3-k & 1\\ 1 & 4-k\end{vmatrix} = (3-k)(4-k) - 1 = k^2 - 7k + 11$
- $\begin{vmatrix}-2 & 1\\ -1 & 4-k\end{vmatrix} = -2(4-k) - (1)(-1) = -8 + 2k + 1 = 2k - 7$
- $\begin{vmatrix}-2 & 3-k\\ -1 & 1\end{vmatrix} = (-2)(1) - (3-k)(-1) = -2 + 3 - k = 1 - k$

Put them back together:

$$\begin{aligned}
\det &= (3-k)(k^2 - 7k + 11) + 2(2k - 7) - (1 - k)\\
&= (-k^3 + 10k^2 - 32k + 33) + (4k - 14) + (k - 1)\\
&= -k^3 + 10k^2 - 27k + 18
\end{aligned}$$

Set it to 0 and multiply by $-1$: $\;k^3 - 10k^2 + 27k - 18 = 0$.

**Factorise.** *(added)* Try the whole-number divisors of 18 (±1, ±2, ±3, ±6, …):
- $k = 1$: $1 - 10 + 27 - 18 = 0$ ✓, so $(k-1)$ is a factor.
- Divide it out: $k^3 - 10k^2 + 27k - 18 = (k-1)(k^2 - 9k + 18) = (k-1)(k-3)(k-6)$.

$$\boxed{k_0 = 1,\quad k_1 = 3,\quad k_2 = 6}$$

<details>
<summary>Note: quick checks on the eigenvalues (added)</summary>

The eigenvalues add up to $\text{trace}(\mathbf A)$: $1+3+6 = 10 = 3+3+4$ ✓. They multiply to $\det\mathbf A$: $1\cdot3\cdot6 = 18$ ✓ (sl.32).

</details>

### B2. Find an eigenvector for each $k_i$.

**Solution**

**$k_0 = 1$:** $\;\mathbf A - \mathbf I = \begin{bmatrix} 2 & -2 & -1 \\ -2 & 2 & 1 \\ -1 & 1 & 3 \end{bmatrix}$

- Row 1 is $-1\times$ row 0, so it adds no new information. That's expected, because $\det = 0$ means one row is redundant.
- Row 2: $-x_0 + x_1 + 3x_2 = 0 \Rightarrow x_1 = x_0 - 3x_2$
- Substitute into row 0: $2x_0 - 2(x_0 - 3x_2) - x_2 = 0 \Rightarrow 5x_2 = 0 \Rightarrow x_2 = 0$, so $x_1 = x_0$
- Set $x_0 = 1$: $\;\mathbf x_0 = (1,\,1,\,0)$

**$k_1 = 3$:** $\;\mathbf A - 3\mathbf I = \begin{bmatrix} 0 & -2 & -1 \\ -2 & 0 & 1 \\ -1 & 1 & 1 \end{bmatrix}$

- Row 0: $-2x_1 - x_2 = 0 \Rightarrow x_2 = -2x_1$
- Row 1: $-2x_0 + x_2 = 0 \Rightarrow x_2 = 2x_0$
- Set them equal: $2x_0 = -2x_1 \Rightarrow x_1 = -x_0$
- Set $x_0 = 1$: $\;\mathbf x_1 = (1,\,-1,\,2)$
- Check with row 2: $-1 + (-1) + 2 = 0$ ✓

**$k_2 = 6$:** $\;\mathbf A - 6\mathbf I = \begin{bmatrix} -3 & -2 & -1 \\ -2 & -3 & 1 \\ -1 & 1 & -2 \end{bmatrix}$

- Row 2: $-x_0 + x_1 - 2x_2 = 0 \Rightarrow x_1 = x_0 + 2x_2$
- Substitute into row 0: $-3x_0 - 2(x_0 + 2x_2) - x_2 = -5x_0 - 5x_2 = 0 \Rightarrow x_2 = -x_0$
- Then $x_1 = x_0 - 2x_0 = -x_0$
- Set $x_0 = -1$: $\;\mathbf x_2 = (-1,\,1,\,1)$. Any multiple works. $(1,-1,-1)$ is equally correct.

**Always verify** $\mathbf A\mathbf x_i = k_i\mathbf x_i$. For example, $\mathbf A(1,1,0) = (3-2,\; -2+3,\; -1+1) = (1,1,0) = 1\cdot\mathbf x_0$ ✓

### B3. Show that the eigenvectors are perpendicular, then build the normalised $\mathbf X$.

**Solution**

**Perpendicular:**
- $\mathbf x_0\cdot\mathbf x_1 = 1 - 1 + 0 = 0$
- $\mathbf x_0\cdot\mathbf x_2 = -1 + 1 + 0 = 0$
- $\mathbf x_1\cdot\mathbf x_2 = -1 - 1 + 2 = 0$ ✓

**Lengths:** $|\mathbf x_0| = \sqrt2$, $\;|\mathbf x_1| = \sqrt{1+1+4} = \sqrt6$, $\;|\mathbf x_2| = \sqrt3$

$$\mathbf X = \begin{bmatrix} \tfrac{1}{\sqrt2} & \tfrac{1}{\sqrt6} & -\tfrac{1}{\sqrt3} \\[2pt] \tfrac{1}{\sqrt2} & -\tfrac{1}{\sqrt6} & \tfrac{1}{\sqrt3} \\[2pt] 0 & \tfrac{2}{\sqrt6} & \tfrac{1}{\sqrt3} \end{bmatrix},\qquad \mathbf X^T\mathbf X = \mathbf I$$

<details>
<summary>Note: why normalise?</summary>

Without it, $\mathbf X^T\mathbf X$ is not $\mathbf I$, as we saw with $(1,2)$ and $(2,-1)$ in the session, where it came out as $5\mathbf I$.

</details>

### B4. Solve $\mathbf A\mathbf x = \mathbf b$ with the three moves: $\mathbf d = \mathbf X^T\mathbf b$, then $c_i = d_i/k_i$, then $\mathbf x = \mathbf X\mathbf c$.

**Solution**

**Move 1: rewrite b in eigen axes,** $d_i = \mathbf e_i\cdot\mathbf b$:
- $d_0 = \frac{1}{\sqrt2}(-4 + 7 + 0) = \frac{3}{\sqrt2}$
- $d_1 = \frac{1}{\sqrt6}(-4 - 7 + 26) = \frac{15}{\sqrt6}$
- $d_2 = \frac{1}{\sqrt3}(4 + 7 + 13) = \frac{24}{\sqrt3}$

**Move 2: divide by k:**
- $c_0 = \frac{3/\sqrt2}{1} = \frac{3}{\sqrt2}$
- $c_1 = \frac{15/\sqrt6}{3} = \frac{5}{\sqrt6}$
- $c_2 = \frac{24/\sqrt3}{6} = \frac{4}{\sqrt3}$

**Move 3: add up the pieces,** $\mathbf x = \sum c_i\mathbf e_i$. The roots cancel because each $\mathbf e_i$ also carries a $1/\sqrt{\cdot}$:

$$\mathbf x = \tfrac{3}{2}(1,1,0) + \tfrac{5}{6}(1,-1,2) + \tfrac{4}{3}(-1,1,1)$$

Work it out in sixths:
- $x_0 = \tfrac{9}{6} + \tfrac{5}{6} - \tfrac{8}{6} = 1$
- $x_1 = \tfrac{9}{6} - \tfrac{5}{6} + \tfrac{8}{6} = 2$
- $x_2 = 0 + \tfrac{10}{6} + \tfrac{8}{6} = 3$

$$\boxed{\mathbf x = (1,\,2,\,3)}$$

<details>
<summary>Note: shortcut without square roots (added)</summary>

You can skip normalising. Use the raw eigenvectors $\mathbf v_i$ and
$$\text{amount of } \mathbf v_i \text{ in } \mathbf x = \frac{\mathbf v_i\cdot\mathbf b}{(\mathbf v_i\cdot\mathbf v_i)\,k_i}.$$
Here that gives $\frac{3}{2\cdot1} = \frac32$, $\;\frac{15}{6\cdot3} = \frac56$, $\;\frac{24}{3\cdot6} = \frac43$, the same three numbers.

</details>

### B5. Check your answer.

**Solution**

$\mathbf A(1,2,3)$:
- row 0: $3 - 4 - 3 = -4$
- row 1: $-2 + 6 + 3 = 7$
- row 2: $-1 + 2 + 12 = 13$

That gives $(-4,\,7,\,13) = \mathbf b$ ✓

---

## Part C: the end of A3 (sl.30–32, 39–41), same matrix

### C1. Solvability (sl.30–32): Without doing any more work, is $\mathbf A\mathbf x = \mathbf b$ uniquely solvable? What is $\det\mathbf A$? What is $\mathbf A^{-1}$ in eigen form?

**Solution**

- $\det\mathbf A = k_0k_1k_2 = 1\cdot3\cdot6 = 18 \neq 0$ (sl.32). No eigenvalue is 0, so there is a unique solution. A zero $k$ would leave you dividing by zero in move 2, the same failure as a zero on the diagonal of R in QR (sl.30).
- $\mathbf A^{-1} = \mathbf X\,\text{diag}(1,\ \tfrac13,\ \tfrac16)\,\mathbf X^T$ (sl.31). The same eigenvectors, with each $k$ flipped to $1/k$.

### C2. Powers (sl.39–40): What are the eigenvalues of $\mathbf A^2$? Write $\mathbf A^M\mathbf b$ as a sum over the eigenvectors, check it for $M = 1$, and say which direction $\mathbf A^M\mathbf b$ points in when $M$ is large.

**Solution**

$\mathbf A^M = \mathbf X\,\text{diag}(k_0^M, k_1^M, k_2^M)\,\mathbf X^T$, with the same eigenvectors. So $\mathbf A^2$ has eigenvalues $1, 9, 36$.

$\mathbf A^M\mathbf b$ follows the same three moves, except you **multiply** by $k^M$ instead of dividing by $k$:

$$\mathbf A^M\mathbf b = \tfrac{3}{2}\cdot1^M(1,1,0) + \tfrac{15}{6}\cdot3^M(1,-1,2) + \tfrac{24}{3}\cdot6^M(-1,1,1)$$

**Check with $M = 1$:** $1.5(1,1,0) + 7.5(1,-1,2) + 48(-1,1,1) = (-39,\ 42,\ 63)$.
Directly: $\mathbf A\mathbf b = (-12-14-13,\ \ 8+21+13,\ \ 4+7+52) = (-39,\ 42,\ 63)$ ✓

**Large $M$:** the $6^M$ term swamps the others, so $\mathbf A^M\mathbf b$ points along $(-1,1,1)$.

<details>
<summary>Note: link to sl.38 and the lab</summary>

This is the fibre "settling to one pattern" (sl.38). It's also what the feedback-loop button in the A3 lab (panel 1) shows: repeated multiplication picks out the largest |k|.

</details>

### C3. Feedback stability (sl.41): Using A's eigenvalues, put $\mathbf A$ in a loop with scalar feedback $\beta$, so that $(\mathbf I + \beta\mathbf A)\mathbf V_{out} = \mathbf A\mathbf V_{in}$. What are the eigenvalues of the overall system? For which values of $\beta$ does it go unstable?

**Solution**

$\mathbf I + \beta\mathbf A$ is a function of $\mathbf A$, so it has the same eigenvectors with eigenvalues $1 + \beta k_i$ (sl.40–41). Therefore

$$\mathbf V_{out} = \mathbf X\,\text{diag}\!\left(\frac{k_i}{1+\beta k_i}\right)\mathbf X^T\,\mathbf V_{in}$$

- Overall eigenvalues: $\dfrac{1}{1+\beta},\ \dfrac{3}{1+3\beta},\ \dfrac{6}{1+6\beta}$
- Unstable when any $1 + \beta k_i = 0$: $\;\beta = -1,\ -\tfrac13,\ -\tfrac16$
- *(Invented example)* With $\beta = 0.5$ the eigenvalues are $\tfrac{1}{1.5} = 0.667,\ \tfrac{3}{2.5} = 1.2,\ \tfrac{6}{4} = 1.5$. All are finite, so it's stable.
