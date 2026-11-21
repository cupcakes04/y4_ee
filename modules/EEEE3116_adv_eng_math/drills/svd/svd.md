# SVD drill: hand calculation (A4)

**How to use:** do each step on paper first, then open the solution and compare.
Notation follows the A4 slides: $\mathbf A = \mathbf Q\boldsymbol\sigma\mathbf P^T$, singular values $\sigma_0 \ge \sigma_1 \ge \dots$, columns $\mathbf q_i$ of $\mathbf Q$ and $\mathbf p_i$ of $\mathbf P$ (counting from 0).
Intuition first: [A4 SVD lab](https://claude.ai/artifact/FhzUauXrbSSswToXwniqws) (local copy `../../chapters/lecture/A4_svd_lab.html`).
Progress across Section A: [`section_A_progress.md`](../../chapters/lecture/section_A_progress.md).

Sources: Part A uses A4 sl.15 and 36 and the derivation in the A4 practical. Part B is the practical's problem, kept exactly as given. Part C uses the slides' own examples (sl.26–28, 37, 38, 41), with numbers verbatim. Every number here was recomputed with numpy/sympy (2026-11-21). Tips I added that aren't on the slides are tagged *(added)*.

**Scope (sl.35):** the lecture says it doesn't cover computing an SVD, and that the exam may give you an SVD and ask you to *use* it (Part C). The practical does have you compute one (Part B), so both are here.

**The two equations everything comes from:**

| | Equation | In words |
|---|---|---|
| 1 | $\boldsymbol\sigma(\mathbf P^T\mathbf x) = \mathbf Q^T\mathbf b$ (sl.36–37) | σᵢ × (amount of $\mathbf p_i$ in x) = (amount of $\mathbf q_i$ in b) |
| 2 | $\mathbf A\mathbf p_i = \sigma_i\mathbf q_i$ (A1 below; the practical uses it) | input axis $\mathbf p_i$ lands on output axis $\mathbf q_i$, stretched by $\sigma_i$ |

---

## Part A: why it works (no numbers)

**A1.** Start from $\mathbf A = \mathbf Q\boldsymbol\sigma\mathbf P^T$. Multiply both sides on the right by $\mathbf P$ and show that $\mathbf A\mathbf p_i = \sigma_i\mathbf q_i$. Say what it means in words, and compare it with A3's $\mathbf A\mathbf x_i = k_i\mathbf x_i$.

<details><summary>Solution</summary>

$$\mathbf A\mathbf P = \mathbf Q\boldsymbol\sigma\underbrace{\mathbf P^T\mathbf P}_{\mathbf I} = \mathbf Q\boldsymbol\sigma$$

Read it one column at a time. Column $i$ of $\mathbf A\mathbf P$ is $\mathbf A\mathbf p_i$. Column $i$ of $\mathbf Q\boldsymbol\sigma$ is $\sigma_i\mathbf q_i$, because $\boldsymbol\sigma$ is diagonal and just scales column $i$ of $\mathbf Q$. So:

$$\boxed{\mathbf A\mathbf p_i = \sigma_i\mathbf q_i}$$

**In words:** feed in the input axis $\mathbf p_i$ and you get the output axis $\mathbf q_i$, stretched by $\sigma_i$. This is the link between P and Q. Q is where the P axes land.

**Compared with A3:** $\mathbf A\mathbf x_i = k_i\mathbf x_i$ means an eigen axis lands *on itself*. SVD relaxes that, so $\mathbf p_i$ can land on a *different* direction $\mathbf q_i$. What SVD keeps is perpendicularity: the P axes are perpendicular, and so are the places they land. That's what the lab's x / x⊥ sweep shows.

**Mirror version** *(added, used in B4)*: transpose first, $\mathbf A^T = \mathbf P\boldsymbol\sigma^T\mathbf Q^T$, then multiply by $\mathbf Q$. That gives $\mathbf A^T\mathbf q_i = \sigma_i\mathbf p_i$.
</details>

**A2.** Show that $\mathbf A^T\mathbf A = \mathbf P(\boldsymbol\sigma^T\boldsymbol\sigma)\mathbf P^T$. Why does that mean P is made of the eigenvectors of $\mathbf A^T\mathbf A$? What are its eigenvalues?

<details><summary>Solution</summary>

$$\mathbf A^T\mathbf A = (\mathbf P\boldsymbol\sigma^T\mathbf Q^T)(\mathbf Q\boldsymbol\sigma\mathbf P^T) = \mathbf P\boldsymbol\sigma^T\underbrace{\mathbf Q^T\mathbf Q}_{\mathbf I}\boldsymbol\sigma\mathbf P^T = \mathbf P(\boldsymbol\sigma^T\boldsymbol\sigma)\mathbf P^T$$

This is exactly A3's form $\mathbf X\mathbf K\mathbf X^T$: an orthogonal matrix, a diagonal matrix, then the transpose. $\mathbf A^T\mathbf A$ is always symmetric, so A3 applies. Therefore:
- **P** = the eigenvectors of $\mathbf A^T\mathbf A$
- **its eigenvalues** = the diagonal of $\boldsymbol\sigma^T\boldsymbol\sigma$ = $\sigma_0^2, \sigma_1^2, \dots$, so $\sigma_i = \sqrt{k_i}$

The same argument with the order swapped gives $\mathbf A\mathbf A^T = \mathbf Q(\boldsymbol\sigma\boldsymbol\sigma^T)\mathbf Q^T$. So **Q** = the eigenvectors of $\mathbf A\mathbf A^T$, with the same nonzero eigenvalues.

**So the SVD is two A3 eigen problems.** That's why A3 came first.
</details>

**A3.** For a 2×3 matrix A, give the shapes of Q, σ, Pᵀ, AAᵀ and AᵀA (sl.15, full form). Which of AAᵀ and AᵀA is quicker to solve by hand?

<details><summary>Solution</summary>

$$\underset{2\times3}{\mathbf A} = \underset{2\times2}{\mathbf Q}\;\underset{2\times3}{\boldsymbol\sigma}\;\underset{3\times3}{\mathbf P^T},\qquad \underset{2\times2}{\mathbf A\mathbf A^T},\qquad \underset{3\times3}{\mathbf A^T\mathbf A}$$

$\mathbf A\mathbf A^T$ is quicker: a 2×2 eigen problem is just a quadratic, while 3×3 needs a cubic. *(added)* Both have the same nonzero eigenvalues, so the smaller one gives you all the σ. Then use $\mathbf A^T\mathbf q_i = \sigma_i\mathbf p_i$ to get P without ever solving the 3×3.
</details>

---

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

**B1.** Compute $\mathbf A\mathbf A^T$ and $\mathbf A^T\mathbf A$.

<details><summary>Solution</summary>

Entry $(i,j)$ of $\mathbf A\mathbf A^T$ is (row $i$ of A)·(row $j$ of A):

$$\mathbf A\mathbf A^T = \begin{bmatrix} 2\cdot2+0\cdot0+1\cdot1 & 2(-1)+0\cdot2+1\cdot9 \\ \cdot & (-1)^2+2^2+9^2 \end{bmatrix} = \begin{bmatrix} 5 & 7 \\ 7 & 86 \end{bmatrix}$$

Entry $(i,j)$ of $\mathbf A^T\mathbf A$ is (column $i$)·(column $j$). The columns are $(2,-1)$, $(0,2)$ and $(1,9)$:

$$\mathbf A^T\mathbf A = \begin{bmatrix} 5 & -2 & -7 \\ -2 & 4 & 18 \\ -7 & 18 & 82 \end{bmatrix}$$

Both are symmetric, as A2 says they must be.
</details>

**B2.** Find $\sigma_0$ and $\sigma_1$.

<details><summary>Solution</summary>

$$\det\begin{bmatrix} 5-k & 7 \\ 7 & 86-k \end{bmatrix} = (5-k)(86-k) - 49 = k^2 - 91k + 381 = 0$$

$$k = \frac{91 \pm \sqrt{91^2 - 4\cdot381}}{2} = \frac{91 \pm \sqrt{6757}}{2} = \frac{91 \pm 82.201}{2}$$

$$k_0 = 86.600,\quad k_1 = 4.400 \qquad\Rightarrow\qquad \boxed{\sigma_0 = \sqrt{86.600} = 9.3059,\quad \sigma_1 = \sqrt{4.400} = 2.0975}$$

**Quick checks** (the A3 tricks): $k_0 + k_1 = 91 = $ trace $= 5 + 86$ ✓, and $k_0 k_1 = 381 = \det = 5\cdot86 - 7^2$ ✓.

*(added)* The 3×3 $\mathbf A^T\mathbf A$ has eigenvalues 86.600, 4.400 and **0**. Its trace is $5+4+82 = 91$ ✓. The 0 belongs to $\mathbf p_2$, which has no partner σ.
</details>

**B3.** Find $\mathbf q_0$ and $\mathbf q_1$, the normalised eigenvectors of $\mathbf A\mathbf A^T$.

<details><summary>Solution</summary>

Set the first element to 1 (A3's method). The top row of $(\mathbf A\mathbf A^T - k_i\mathbf I)\mathbf x = \mathbf 0$ reads:

$$(5-k_i)\cdot1 + 7x_1 = 0 \;\Rightarrow\; x_1 = \frac{k_i - 5}{7}$$

- $k_0 = 86.600$: $x_1 = \frac{81.600}{7} = 11.657$. Length $\sqrt{1 + 11.657^2} = \sqrt{136.89} = 11.700$, so $\mathbf q_0 = \frac{(1,\;11.657)}{11.700} = (0.0855,\; 0.9963)$
- $k_1 = 4.400$: $x_1 = \frac{-0.600}{7} = -0.0858$. Length $\sqrt{1 + 0.0858^2} = 1.0037$, so $\mathbf q_1 = (0.9963,\; -0.0855)$

**Check:** $\mathbf q_0\cdot\mathbf q_1 = 0.0855(0.9963) + 0.9963(-0.0855) = 0$ ✓. Each has length 1, so $\mathbf Q$ is orthogonal.
</details>

**B4.** Find $\mathbf p_0$ and $\mathbf p_1$ using $\mathbf p_i = \mathbf A^T\mathbf q_i/\sigma_i$.

<details><summary>Solution</summary>

$\mathbf A^T = \begin{bmatrix} 2 & -1 \\ 0 & 2 \\ 1 & 9 \end{bmatrix}$, so $\mathbf A^T\mathbf q = (2q_0 - q_1,\; 2q_1,\; q_0 + 9q_1)$, where $q_0, q_1$ are the two elements of $\mathbf q$.

**$\mathbf p_0$:**
$$\mathbf A^T\mathbf q_0 = (2(0.0855) - 0.9963,\;\; 2(0.9963),\;\; 0.0855 + 9(0.9963)) = (-0.8254,\; 1.9927,\; 9.0525)$$
$$\mathbf p_0 = \frac{(-0.8254,\; 1.9927,\; 9.0525)}{9.3059} = (-0.0887,\; 0.2141,\; 0.9728)$$

**$\mathbf p_1$:**
$$\mathbf A^T\mathbf q_1 = (2(0.9963) + 0.0855,\;\; 2(-0.0855),\;\; 0.9963 - 9(0.0855)) = (2.0782,\; -0.1709,\; 0.2271)$$
$$\mathbf p_1 = \frac{(2.0782,\; -0.1709,\; 0.2271)}{2.0975} = (0.9908,\; -0.0815,\; 0.1083)$$

These come out at length 1 automatically (the practical notes this too), and their signs are already matched to $\mathbf q_0, \mathbf q_1$. *(The numbers above were carried at full precision. Working at 4 dp, your 4th decimal may differ by 1.)*
</details>

**B5.** Find $\mathbf p_2$. No σ pairs with it. Use $\mathbf A\mathbf p_2 = \mathbf 0$.

<details><summary>Solution</summary>

$\mathbf p_2 = (x_0, x_1, x_2)$ must give zero from both rows of A:
- Row 0: $2x_0 + x_2 = 0 \Rightarrow x_2 = -2x_0$
- Row 1: $-x_0 + 2x_1 + 9x_2 = 0 \Rightarrow -x_0 + 2x_1 - 18x_0 = 0 \Rightarrow x_1 = 9.5\,x_0$

Set $x_0 = 1$: $(1,\; 9.5,\; -2)$, with length $\sqrt{1 + 90.25 + 4} = \sqrt{95.25} = 9.760$:

$$\mathbf p_2 = (0.1025,\; 0.9734,\; -0.2049)$$

*(added)* The sign is free here (numpy gives the negative), since $\mathbf p_2$ has no $\mathbf q$ partner. A shortcut for 2×3: $\mathbf p_2$ is perpendicular to both rows, so (row 0) × (row 1) $= (-2, -19, 4)$ gives the same direction.

**Check:** $\mathbf p_0\cdot\mathbf p_2 = -0.0887(0.1025) + 0.2141(0.9734) + 0.9728(-0.2049) = -0.0091 + 0.2084 - 0.1993 = 0.0000$ ✓
</details>

**B6.** Write out the full SVD. Then rebuild the entry $a_{12} = 9$ (row 1, column 2) to check it.

<details><summary>Solution</summary>

$$\mathbf A = \underbrace{\begin{bmatrix} 0.0855 & 0.9963 \\ 0.9963 & -0.0855 \end{bmatrix}}_{\mathbf Q}\underbrace{\begin{bmatrix} 9.3059 & 0 & 0 \\ 0 & 2.0975 & 0 \end{bmatrix}}_{\boldsymbol\sigma}\underbrace{\begin{bmatrix} -0.0887 & 0.2141 & 0.9728 \\ 0.9908 & -0.0815 & 0.1083 \\ 0.1025 & 0.9734 & -0.2049 \end{bmatrix}}_{\mathbf P^T\text{ (rows } \mathbf p_0,\mathbf p_1,\mathbf p_2)}$$

$a_{12}$ = row 1 of $\mathbf Q$, scaled by σ, dotted with column 2 of $\mathbf P^T$:

$$a_{12} = 0.9963(9.3059)(0.9728) + (-0.0855)(2.0975)(0.1083) = 9.0194 - 0.0194 = 9.000 \;✓$$

The $\mathbf p_2$ row never contributes, because it meets the zero column of σ.
</details>

**B7.** *(added, from lab panel 2; sl.40 names this case but the lecture skips it)* Using B5, explain why $\mathbf A\mathbf x = \mathbf b$ has infinitely many solutions for this A.

<details><summary>Solution</summary>

$\mathbf A(\mathbf x + t\,\mathbf p_2) = \mathbf A\mathbf x + t\,\mathbf A\mathbf p_2 = \mathbf A\mathbf x + \mathbf 0$. So if $\mathbf x$ solves it, so does $\mathbf x + t\,\mathbf p_2$ for any $t$. With 3 knobs and 2 outputs, one combination of knobs ($\mathbf p_2$) moves nothing. This is the "more unknowns than equations, under-specified" case on sl.40.
</details>

---

## Part C: using a given SVD (exam style, sl.35)

**C1.** (sl.37, verbatim) Solve $\mathbf A\mathbf x = \mathbf b$, given

$$\mathbf A = \begin{bmatrix} 0.940 & -0.342 \\ 0.342 & 0.940 \end{bmatrix}\begin{bmatrix} 2 & 0 \\ 0 & 0.1 \end{bmatrix}\begin{bmatrix} 0.643 & 0.766 \\ -0.766 & 0.643 \end{bmatrix},\qquad \mathbf b = \begin{bmatrix} 3 \\ -7 \end{bmatrix}$$

<details><summary>Solution</summary>

**Move 1: $\mathbf Q^T\mathbf b$**, the amounts of $\mathbf q_0, \mathbf q_1$ in b. The rows of $\mathbf Q^T$ are the columns of $\mathbf Q$:
$$\mathbf Q^T\mathbf b = \begin{bmatrix} 0.940(3) + 0.342(-7) \\ -0.342(3) + 0.940(-7) \end{bmatrix} = \begin{bmatrix} 2.820 - 2.394 \\ -1.026 - 6.580 \end{bmatrix} = \begin{bmatrix} 0.43 \\ -7.61 \end{bmatrix}$$

**Move 2: ÷σ**, the amounts of $\mathbf p_0, \mathbf p_1$ in x:
$$\boldsymbol\sigma^{-1}\mathbf Q^T\mathbf b = \begin{bmatrix} 0.43/2 \\ -7.61/0.1 \end{bmatrix} = \begin{bmatrix} 0.21 \\ -76.1 \end{bmatrix}$$

**Move 3: P(…).** $\mathbf P$ is the transpose of the given $\mathbf P^T$:
$$\mathbf x = \begin{bmatrix} 0.643 & -0.766 \\ 0.766 & 0.643 \end{bmatrix}\begin{bmatrix} 0.21 \\ -76.1 \end{bmatrix} = \begin{bmatrix} 0.135 + 58.29 \\ 0.161 - 48.93 \end{bmatrix} = \begin{bmatrix} 58.4 \\ -48.8 \end{bmatrix}$$

That matches the slide. *(Carrying more digits gives $x_1 = -48.7$. The slide's $-48.8$ comes from rounding the middle step.)*

**Note:** a small σ₁ = 0.1 turned b's −7.61 into −76.1, a 10× amplification. That's the sensitivity sl.38 calls "borderline".
</details>

**C2.** (sl.38) For $\mathbf A = \begin{bmatrix}1&2&4\\2&3&5\\3&5&9\end{bmatrix}$, a computer gives $\sigma = 13.2,\; 0.49,\; 1.16\times10^{-16}$, and $\mathbf P^T$ has rows $(-0.28, -0.47, -0.83)$, $(-0.80, -0.37, 0.48)$ and $(-0.53, 0.80, -0.27)$. (a) What do the σ values tell you? (b) *(added)* Which direction can you add to any solution x without changing Ax? Check it.

<details><summary>Solution</summary>

(a) $1.16\times10^{-16}$ is the computer's version of 0 (sl.38). One zero singular value means the system has no unique solution. It matches the slide's observation that row 2 = row 0 + row 1.

(b) The P axis paired with the zero σ: $\mathbf p_2 = (-0.53,\; 0.80,\; -0.27)$, the third row of $\mathbf P^T$. Check $\mathbf A\mathbf p_2$:
- row 0: $1(-0.53) + 2(0.80) + 4(-0.27) = -0.53 + 1.60 - 1.08 = -0.01$
- row 1: $2(-0.53) + 3(0.80) + 5(-0.27) = -1.06 + 2.40 - 1.35 = -0.01$
- row 2: $3(-0.53) + 5(0.80) + 9(-0.27) = -1.59 + 4.00 - 2.43 = -0.02$

All are ≈ 0 (the leftovers come from 2-dp rounding) ✓. This is B7's situation, in a square matrix.
</details>

**C3.** (sl.41) A 3×3 grey-scale image $\mathbf V = \begin{bmatrix}150&200&180\\77&202&100\\127&200&98\end{bmatrix}$ has $\sigma = 461.3,\; 60.6,\; 30.2$, $\mathbf q_0 = (-0.66, -0.51, -0.55)$ and $\mathbf p_0 = (-0.45, -0.75, -0.49)$. You keep only the σ₀ term. (a) What do you store, and how many values is that compared with the full image? (b) Rebuild the top-left pixel from what you kept.

<details><summary>Solution</summary>

(a) You store $\mathbf q_0$ (N = 3 values), $\mathbf p_0$ (M = 3 values) and $\sigma_0$ (1 value): **M + N + 1 = 7** values, against **M × N = 9** for the full image (sl.41). The saving grows with size. *(Invented example: a 256×256 image goes from 65 536 values to 513.)*

(b) The kept term is $\sigma_0\,\mathbf q_0\mathbf p_0^T$, so pixel $(0,0)$ is $\sigma_0 \times q_{0,0} \times p_{0,0}$:
$$461.3 \times (-0.66) \times (-0.45) = 137.0 \quad\text{(true value 150)}$$
It's a rough version of the image: the "big picture" that sl.41 starts from before adding detail back.

*(Slide typo, flagged:* sl.41's $\mathbf P^T$ shows "23" in row 1. numpy gives 0.38 there. It doesn't affect this question.)
</details>

**C4.** (sl.26–28) The delivery driver's 4 destinations give $\sigma_0 = 20.3$. Using sl.26, what is the RMS distance travelled along $\mathbf q_0$?

<details><summary>Solution</summary>

Sl.26: $\sigma_i$ = the square root of the sum of squared distances along axis $i$, so RMS $= \sigma_i/\sqrt{M}$, where M is the number of data points.

$$d_0^{RMS} = \frac{20.3}{\sqrt4} = 10.15$$

That matches sl.28: roughly, the driver heads about 10 units along $\mathbf q_0$.
</details>
