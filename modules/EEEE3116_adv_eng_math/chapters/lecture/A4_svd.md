# A4 SVD: worked examples

**What this page is for:** worked calculations, every step written out. Read an example, cover the solution, then redo it on paper.
**Concepts and gaps** live in the [A4 SVD lab](https://claude.ai/artifact/FhzUauXrbSSswToXwniqws) (`A4_svd_lab.html`, same folder). Panel 4 there derives the three facts below.
Notation follows the A4 slides: $\mathbf A = \mathbf Q\boldsymbol\sigma\mathbf P^T$, singular values $\sigma_0 \ge \sigma_1 \ge \dots$, columns $\mathbf q_i$ of $\mathbf Q$ and $\mathbf p_i$ of $\mathbf P$ (counting from 0).
Progress: [`progress.md`](progress.md).

<details>
<summary>Note: sources and scope</summary>

Sources: Part B is the practical's problem (`../../drills/svd/`), kept exactly as given. Part C uses the slides' own examples (sl.26–28, 37, 38, 41), with numbers verbatim. Every number here was recomputed with numpy/sympy (2026-11-21). Tips I added that aren't on the slides are tagged *(added)*.

**Scope (sl.35):** the lecture says it doesn't cover computing an SVD, and that the exam may give you an SVD and ask you to *use* it (Part C). The practical does have you compute one (Part B), so both are here.

</details>

---

## Key facts used in the calculations

| Fact | Formula | Used in |
|---|---|---|
| Solve | $\boldsymbol\sigma(\mathbf P^T\mathbf x) = \mathbf Q^T\mathbf b$, so $\mathbf x = \mathbf P\boldsymbol\sigma^{-1}\mathbf Q^T\mathbf b$: three moves, Qᵀb → ÷σ → P(…) (sl.36–37) | C1 |
| P–Q link | $\mathbf A\mathbf p_i = \sigma_i\mathbf q_i$ and its mirror $\mathbf A^T\mathbf q_i = \sigma_i\mathbf p_i$ | B4 ($\mathbf p_i = \mathbf A^T\mathbf q_i/\sigma_i$), B5, B7 |
| Two eigen problems | $\mathbf A\mathbf A^T = \mathbf Q(\boldsymbol\sigma\boldsymbol\sigma^T)\mathbf Q^T$, $\;\mathbf A^T\mathbf A = \mathbf P(\boldsymbol\sigma^T\boldsymbol\sigma)\mathbf P^T$, so $\sigma_i = \sqrt{k_i}$ | B2, B3 |
| Shapes (full form, sl.15) | $\underset{N\times M}{\mathbf A} = \underset{N\times N}{\mathbf Q}\,\underset{N\times M}{\boldsymbol\sigma}\,\underset{M\times M}{\mathbf P^T}$. Start from the **smaller** of AAᵀ (N×N) and AᵀA (M×M) *(added)* | B1 |
| Zero σ | no unique solution: $\mathbf p_i$ with $\sigma_i = 0$ (or no partner) satisfies $\mathbf A\mathbf p_i = \mathbf 0$ (sl.38) | B5, B7, C2 |

## Part B: the practical problem, 2×3

$$\mathbf A = \begin{bmatrix} 2 & 0 & 1 \\ -1 & 2 & 9 \end{bmatrix}$$

Find $\mathbf A = \mathbf Q\boldsymbol\sigma\mathbf P^T$.

**The recipe:**
1. $\mathbf A\mathbf A^T$, the small one
2. $\det(\mathbf A\mathbf A^T - k\mathbf I) = 0$ → $k_i$, then $\sigma_i = \sqrt{k_i}$, sorted largest first
3. Eigenvectors of $\mathbf A\mathbf A^T$, normalised → $\mathbf q_i$
4. $\mathbf p_i = \mathbf A^T\mathbf q_i/\sigma_i$ *(added: the mirror of the practical's shortcut $\mathbf q_i = \mathbf A\mathbf p_i/\sigma_i$)*
5. The leftover $\mathbf p_2$: solve $\mathbf A\mathbf p_2 = \mathbf 0$ and normalise
6. Check

### B1. Compute $\mathbf A\mathbf A^T$ and $\mathbf A^T\mathbf A$.

**Solution**

Entry $(i,j)$ of $\mathbf A\mathbf A^T$ is (row $i$ of A)·(row $j$ of A):

$$\mathbf A\mathbf A^T = \begin{bmatrix} 2\cdot2+0\cdot0+1\cdot1 & 2(-1)+0\cdot2+1\cdot9 \\ \cdot & (-1)^2+2^2+9^2 \end{bmatrix} = \begin{bmatrix} 5 & 7 \\ 7 & 86 \end{bmatrix}$$

Entry $(i,j)$ of $\mathbf A^T\mathbf A$ is (column $i$)·(column $j$). The columns are $(2,-1)$, $(0,2)$ and $(1,9)$:

$$\mathbf A^T\mathbf A = \begin{bmatrix} 5 & -2 & -7 \\ -2 & 4 & 18 \\ -7 & 18 & 82 \end{bmatrix}$$

Both are symmetric, as they must be (AᵀA is always symmetric, so A3 applies).

### B2. Find $\sigma_0$ and $\sigma_1$.

**Solution**

$$\det\begin{bmatrix} 5-k & 7 \\ 7 & 86-k \end{bmatrix} = (5-k)(86-k) - 49 = k^2 - 91k + 381 = 0$$

$$k = \frac{91 \pm \sqrt{91^2 - 4\cdot381}}{2} = \frac{91 \pm \sqrt{6757}}{2} = \frac{91 \pm 82.201}{2}$$

$$k_0 = 86.600,\quad k_1 = 4.400 \qquad\Rightarrow\qquad \boxed{\sigma_0 = \sqrt{86.600} = 9.3059,\quad \sigma_1 = \sqrt{4.400} = 2.0975}$$

<details>
<summary>Note: quick checks (trace, det) and the third eigenvalue</summary>

**Quick checks** (the A3 tricks): $k_0 + k_1 = 91 = $ trace $= 5 + 86$ ✓, and $k_0 k_1 = 381 = \det = 5\cdot86 - 7^2$ ✓.

*(added)* The 3×3 $\mathbf A^T\mathbf A$ has eigenvalues 86.600, 4.400 and **0**. Its trace is $5+4+82 = 91$ ✓. The 0 belongs to $\mathbf p_2$, which has no partner σ.

</details>

### B3. Find $\mathbf q_0$ and $\mathbf q_1$, the normalised eigenvectors of $\mathbf A\mathbf A^T$.

**Solution**

Set the first element to 1 (A3's method). The top row of $(\mathbf A\mathbf A^T - k_i\mathbf I)\mathbf x = \mathbf 0$ reads:

$$(5-k_i)\cdot1 + 7x_1 = 0 \;\Rightarrow\; x_1 = \frac{k_i - 5}{7}$$

- $k_0 = 86.600$: $x_1 = \frac{81.600}{7} = 11.657$. Length $\sqrt{1 + 11.657^2} = \sqrt{136.89} = 11.700$, so $\mathbf q_0 = \frac{(1,\;11.657)}{11.700} = (0.0855,\; 0.9963)$
- $k_1 = 4.400$: $x_1 = \frac{-0.600}{7} = -0.0858$. Length $\sqrt{1 + 0.0858^2} = 1.0037$, so $\mathbf q_1 = (0.9963,\; -0.0855)$

**Check:** $\mathbf q_0\cdot\mathbf q_1 = 0.0855(0.9963) + 0.9963(-0.0855) = 0$ ✓. Each has length 1, so $\mathbf Q$ is orthogonal.

### B4. Find $\mathbf p_0$ and $\mathbf p_1$ using $\mathbf p_i = \mathbf A^T\mathbf q_i/\sigma_i$.

**Solution**

$\mathbf A^T = \begin{bmatrix} 2 & -1 \\ 0 & 2 \\ 1 & 9 \end{bmatrix}$, so $\mathbf A^T\mathbf q = (2q_0 - q_1,\; 2q_1,\; q_0 + 9q_1)$, where $q_0, q_1$ are the two elements of $\mathbf q$.

**$\mathbf p_0$:**
$$\mathbf A^T\mathbf q_0 = (2(0.0855) - 0.9963,\;\; 2(0.9963),\;\; 0.0855 + 9(0.9963)) = (-0.8254,\; 1.9927,\; 9.0525)$$
$$\mathbf p_0 = \frac{(-0.8254,\; 1.9927,\; 9.0525)}{9.3059} = (-0.0887,\; 0.2141,\; 0.9728)$$

**$\mathbf p_1$:**
$$\mathbf A^T\mathbf q_1 = (2(0.9963) + 0.0855,\;\; 2(-0.0855),\;\; 0.9963 - 9(0.0855)) = (2.0782,\; -0.1709,\; 0.2271)$$
$$\mathbf p_1 = \frac{(2.0782,\; -0.1709,\; 0.2271)}{2.0975} = (0.9908,\; -0.0815,\; 0.1083)$$

<details>
<summary>Note: why no normalising here, and rounding</summary>

These come out at length 1 automatically (the practical notes this too), and their signs are already matched to $\mathbf q_0, \mathbf q_1$. *(The numbers above were carried at full precision. Working at 4 dp, your 4th decimal may differ by 1.)*

</details>

### B5. Find $\mathbf p_2$. No σ pairs with it. Use $\mathbf A\mathbf p_2 = \mathbf 0$.

**Solution**

$\mathbf p_2 = (x_0, x_1, x_2)$ must give zero from both rows of A:
- Row 0: $2x_0 + x_2 = 0 \Rightarrow x_2 = -2x_0$
- Row 1: $-x_0 + 2x_1 + 9x_2 = 0 \Rightarrow -x_0 + 2x_1 - 18x_0 = 0 \Rightarrow x_1 = 9.5\,x_0$

Set $x_0 = 1$: $(1,\; 9.5,\; -2)$, with length $\sqrt{1 + 90.25 + 4} = \sqrt{95.25} = 9.760$:

$$\mathbf p_2 = (0.1025,\; 0.9734,\; -0.2049)$$

<details>
<summary>Note: sign of p₂, and a cross-product shortcut (added)</summary>

*(added)* The sign is free here (numpy gives the negative), since $\mathbf p_2$ has no $\mathbf q$ partner. A shortcut for 2×3: $\mathbf p_2$ is perpendicular to both rows, so (row 0) × (row 1) $= (-2, -19, 4)$ gives the same direction.

</details>

**Check:** $\mathbf p_0\cdot\mathbf p_2 = -0.0887(0.1025) + 0.2141(0.9734) + 0.9728(-0.2049) = -0.0091 + 0.2084 - 0.1993 = 0.0000$ ✓

### B6. Write out the full SVD. Then rebuild the entry $a_{12} = 9$ (row 1, column 2) to check it.

**Solution**

$$\mathbf A = \underbrace{\begin{bmatrix} 0.0855 & 0.9963 \\ 0.9963 & -0.0855 \end{bmatrix}}_{\mathbf Q}\underbrace{\begin{bmatrix} 9.3059 & 0 & 0 \\ 0 & 2.0975 & 0 \end{bmatrix}}_{\boldsymbol\sigma}\underbrace{\begin{bmatrix} -0.0887 & 0.2141 & 0.9728 \\ 0.9908 & -0.0815 & 0.1083 \\ 0.1025 & 0.9734 & -0.2049 \end{bmatrix}}_{\mathbf P^T\text{ (rows } \mathbf p_0,\mathbf p_1,\mathbf p_2)}$$

$a_{12}$ = row 1 of $\mathbf Q$, scaled by σ, dotted with column 2 of $\mathbf P^T$:

$$a_{12} = 0.9963(9.3059)(0.9728) + (-0.0855)(2.0975)(0.1083) = 9.0194 - 0.0194 = 9.000 \;✓$$

The $\mathbf p_2$ row never contributes, because it meets the zero column of σ.

### B7. *(added, from lab panel 2; sl.40 names this case but the lecture skips it)* Using B5, explain why $\mathbf A\mathbf x = \mathbf b$ has infinitely many solutions for this A.

**Solution**

$\mathbf A(\mathbf x + t\,\mathbf p_2) = \mathbf A\mathbf x + t\,\mathbf A\mathbf p_2 = \mathbf A\mathbf x + \mathbf 0$. So if $\mathbf x$ solves it, so does $\mathbf x + t\,\mathbf p_2$ for any $t$. With 3 knobs and 2 outputs, one combination of knobs ($\mathbf p_2$) moves nothing. This is the "more unknowns than equations, under-specified" case on sl.40.

---

## Part C: using a given SVD (exam style, sl.35)

### C1. (sl.37, verbatim) Solve $\mathbf A\mathbf x = \mathbf b$, given

$$\mathbf A = \begin{bmatrix} 0.940 & -0.342 \\ 0.342 & 0.940 \end{bmatrix}\begin{bmatrix} 2 & 0 \\ 0 & 0.1 \end{bmatrix}\begin{bmatrix} 0.643 & 0.766 \\ -0.766 & 0.643 \end{bmatrix},\qquad \mathbf b = \begin{bmatrix} 3 \\ -7 \end{bmatrix}$$

**Solution**

**Move 1: $\mathbf Q^T\mathbf b$**, the amounts of $\mathbf q_0, \mathbf q_1$ in b. The rows of $\mathbf Q^T$ are the columns of $\mathbf Q$:
$$\mathbf Q^T\mathbf b = \begin{bmatrix} 0.940(3) + 0.342(-7) \\ -0.342(3) + 0.940(-7) \end{bmatrix} = \begin{bmatrix} 2.820 - 2.394 \\ -1.026 - 6.580 \end{bmatrix} = \begin{bmatrix} 0.43 \\ -7.61 \end{bmatrix}$$

**Move 2: ÷σ**, the amounts of $\mathbf p_0, \mathbf p_1$ in x:
$$\boldsymbol\sigma^{-1}\mathbf Q^T\mathbf b = \begin{bmatrix} 0.43/2 \\ -7.61/0.1 \end{bmatrix} = \begin{bmatrix} 0.21 \\ -76.1 \end{bmatrix}$$

**Move 3: P(…).** $\mathbf P$ is the transpose of the given $\mathbf P^T$:
$$\mathbf x = \begin{bmatrix} 0.643 & -0.766 \\ 0.766 & 0.643 \end{bmatrix}\begin{bmatrix} 0.21 \\ -76.1 \end{bmatrix} = \begin{bmatrix} 0.135 + 58.29 \\ 0.161 - 48.93 \end{bmatrix} = \begin{bmatrix} 58.4 \\ -48.8 \end{bmatrix}$$

<details>
<summary>Note: rounding on the slide, and why small σ amplifies</summary>

That matches the slide. *(Carrying more digits gives $x_1 = -48.7$. The slide's $-48.8$ comes from rounding the middle step.)*

**Note:** a small σ₁ = 0.1 turned b's −7.61 into −76.1, a 10× amplification. That's the sensitivity sl.38 calls "borderline".

</details>

### C2. (sl.38) For $\mathbf A = \begin{bmatrix}1&2&4\\2&3&5\\3&5&9\end{bmatrix}$, a computer gives $\sigma = 13.2,\; 0.49,\; 1.16\times10^{-16}$, and $\mathbf P^T$ has rows $(-0.28, -0.47, -0.83)$, $(-0.80, -0.37, 0.48)$ and $(-0.53, 0.80, -0.27)$. (a) What do the σ values tell you? (b) *(added)* Which direction can you add to any solution x without changing Ax? Check it.

**Solution**

(a) $1.16\times10^{-16}$ is the computer's version of 0 (sl.38). One zero singular value means the system has no unique solution. It matches the slide's observation that row 2 = row 0 + row 1.

(b) The P axis paired with the zero σ: $\mathbf p_2 = (-0.53,\; 0.80,\; -0.27)$, the third row of $\mathbf P^T$. Check $\mathbf A\mathbf p_2$:
- row 0: $1(-0.53) + 2(0.80) + 4(-0.27) = -0.53 + 1.60 - 1.08 = -0.01$
- row 1: $2(-0.53) + 3(0.80) + 5(-0.27) = -1.06 + 2.40 - 1.35 = -0.01$
- row 2: $3(-0.53) + 5(0.80) + 9(-0.27) = -1.59 + 4.00 - 2.43 = -0.02$

All are ≈ 0 (the leftovers come from 2-dp rounding) ✓. This is B7's situation, in a square matrix.

### C3. (sl.41) A 3×3 grey-scale image $\mathbf V = \begin{bmatrix}150&200&180\\77&202&100\\127&200&98\end{bmatrix}$ has $\sigma = 461.3,\; 60.6,\; 30.2$, $\mathbf q_0 = (-0.66, -0.51, -0.55)$ and $\mathbf p_0 = (-0.45, -0.75, -0.49)$. You keep only the σ₀ term. (a) What do you store, and how many values is that compared with the full image? (b) Rebuild the top-left pixel from what you kept.

**Solution**

(a) You store $\mathbf q_0$ (N = 3 values), $\mathbf p_0$ (M = 3 values) and $\sigma_0$ (1 value): **M + N + 1 = 7** values, against **M × N = 9** for the full image (sl.41). The saving grows with size. *(Invented example: a 256×256 image goes from 65 536 values to 513.)*

(b) The kept term is $\sigma_0\,\mathbf q_0\mathbf p_0^T$, so pixel $(0,0)$ is $\sigma_0 \times q_{0,0} \times p_{0,0}$:
$$461.3 \times (-0.66) \times (-0.45) = 137.0 \quad\text{(true value 150)}$$
It's a rough version of the image: the "big picture" that sl.41 starts from before adding detail back.

<details>
<summary>Note: slide typo on sl.41</summary>

*(Slide typo, flagged:* sl.41's $\mathbf P^T$ shows "23" in row 1. numpy gives 0.38 there. It doesn't affect this question.)

</details>

### C4. (sl.26–28) The delivery driver's 4 destinations give $\sigma_0 = 20.3$. Using sl.26, what is the RMS distance travelled along $\mathbf q_0$?

**Solution**

Sl.26: $\sigma_i$ = the square root of the sum of squared distances along axis $i$, so RMS $= \sigma_i/\sqrt{M}$, where M is the number of data points.

$$d_0^{RMS} = \frac{20.3}{\sqrt4} = 10.15$$

That matches sl.28: roughly, the driver heads about 10 units along $\mathbf q_0$.
