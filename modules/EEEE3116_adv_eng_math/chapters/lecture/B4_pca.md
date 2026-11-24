# B4 Principal Component Analysis: worked examples

**What this page is for:** worked calculations with every step written out. Read an example, cover the solution, then redo it on paper.
**Concepts and gaps** live in the lab: `B4_pca_lab.html`, in the same folder. Progress is tracked in [`progress.md`](progress.md).

<details>
<summary>Note: sources</summary>

- Parts 1–5: B4 sl.3–35, the slides' 5 voltage points (the same data as B1). Numbers verbatim.
- Part 6: whitening (sl.41–45). The slides give no numbers for this step, so the calculation is *(added)*.
- Part 7: scree (sl.50–52), numbers verbatim.
- Exercises E1–E3 are **invented** (there is no B4 practical). E4 applies sl.43 to the slides' data *(added)*.
- Every number was recomputed with numpy (2026-11-24). The arithmetic uses 4-dp inputs so each displayed line adds up. Where that drifts from the slide (e.g. −6.9423 vs −6.9426), the slide's full-precision value is given.

</details>

<details>
<summary>Note: the words</summary>

| Word on the slides | What it means | Where you've seen it |
|---|---|---|
| principal component (PC) | one new axis, a unit eigenvector of S. PC1 has the largest λ | B1's x′ axis, B2's B₁ |
| eigenvalue λ | the variance of the data along that PC | B1's σ²x′ = u·Su |
| A (rotation matrix) | its **rows** are the PCs. Y = AX | B1's R, B2's B |
| P×N vs N×P | P = variables (here 2 voltages), N = points (here 5). Notes: P×N, one point per **column**. MATLAB: N×P, one point per **row** | — |
| `coeff` | the PCs as **columns**. A = coeffᵀ | — |
| `score` | one **row per point**: its coordinates along PC1, PC2 | B2's X₁, X₂ |
| `latent` | the λ's, largest first | B1's diagonal of Sᴿ |
| decorrelate | rotate onto the PCs, so cov = 0 | B1 Part 3 |
| whiten | decorrelate, then ÷√λ on each PC, so S = I | — |
| scree plot | λ against PC number, used to decide how many to keep | — |

</details>

**Recipe card**

| Step | Formula | Slide |
|---|---|---|
| Centre | subtract each variable's mean | sl.26, 42 |
| Covariance | S = (1/(N−1)) Σ (dev)(dev)ᵀ. MATLAB `cov` uses **N−1** | sl.6, 29 |
| Eigen | det(S − λI) = 0 → λ. (S − λI)u = 0 → u, normalised | A3, sl.30 |
| Rotate | A = [PC1ᵀ; PC2ᵀ] (rows), Y = A X. MATLAB: score = data′ · coeff | sl.24, 27 |
| Check | S_y = A S_x Aᵀ = diag(λ₁, λ₂). Trace is unchanged | sl.32–35 |
| Keep | λ > average λ (one rule). Share kept = Σ kept λ / Σ all λ | sl.51 |
| Whiten | ÷√λᵢ on each PC → S = I | sl.45 |

---

## Part 1: covariance by hand (sl.5–6, 26, 29)

### 1a. Data (two voltages, five samples): (0, 2), (3, 5), (5, 6), (8, 9), (10, 11). Find S the way MATLAB's `cov` does.

**Solution**

Means: x̄ = (0+3+5+8+10)/5 = 26/5 = **5.2**, ȳ = (2+5+6+9+11)/5 = 33/5 = **6.6**.

| point | dx = x − 5.2 | dy = y − 6.6 | dx² | dx·dy | dy² |
|---|---|---|---|---|---|
| (0, 2) | −5.2 | −4.6 | 27.04 | 23.92 | 21.16 |
| (3, 5) | −2.2 | −1.6 | 4.84 | 3.52 | 2.56 |
| (5, 6) | −0.2 | −0.6 | 0.04 | 0.12 | 0.36 |
| (8, 9) | 2.8 | 2.4 | 7.84 | 6.72 | 5.76 |
| (10, 11) | 4.8 | 4.4 | 23.04 | 21.12 | 19.36 |
| **Σ** | 0 | 0 | **62.8** | **55.4** | **49.2** |

Divide by N − 1 = 4:

$$\mathbf S = \frac14\begin{bmatrix}62.8 & 55.4\\ 55.4 & 49.2\end{bmatrix} = \boxed{\begin{bmatrix}15.7 & 13.85\\ 13.85 & 12.3\end{bmatrix}}$$

<details>
<summary>Note: why this isn't B1's S, and what "S = XXᵀ" means</summary>

- B1 divided by N = 5 and got [12.56 11.08; 11.08 9.84]. That's the same matrix × 4/5. Scaling S scales every λ by the same factor but leaves the eigenvectors and the share λ₁/Σλ unchanged (probe Q1).
- sl.5 writes the formulas with 1/N, but sl.6 onwards use MATLAB's 1/(N−1). Flagged in progress.md.
- sl.6/33/37 write S = XXᵀ. That only holds once X is **centred** (P×N layout) and you divide by N−1: the Σ row above **is** the centred XXᵀ = [62.8 55.4; 55.4 49.2]. The raw XXᵀ would be [198 227; 227 267], which is wrong.

</details>

---

## Part 2: eigenvalues (sl.21, 30)

### 2a. Find λ₁, λ₂ for S = [15.7 13.85; 13.85 12.3], and PC1's share of the variance.

**Solution**

$$\det(\mathbf S - \lambda \mathbf I) = (15.7-\lambda)(12.3-\lambda) - 13.85^2 = 0$$

$$\lambda^2 - (15.7+12.3)\lambda + (15.7\cdot12.3 - 13.85^2) = 0$$

- trace = 15.7 + 12.3 = 28
- det = 193.11 − 191.8225 = 1.2875

$$\lambda^2 - 28\lambda + 1.2875 = 0 \;\Rightarrow\; \lambda = \frac{28 \pm \sqrt{784 - 5.15}}{2} = \frac{28 \pm 27.9079}{2}$$

$$\boxed{\lambda_1 = 27.9539,\quad \lambda_2 = 0.0461}$$

Check: λ₁ + λ₂ = 28 = trace ✓ (sl.21: total variance unchanged).
Share: 27.9539 / 28 = **99.84 %** on PC1 (sl.21 says 99.8 %).

---

## Part 3: eigenvectors → the rotation matrix A (sl.23–24, 30, 34)

### 3a. Find PC1 and PC2 as unit vectors, and write A.

**Solution**

PC1, from (S − λ₁I)u = 0, row 1:

$$(15.7 - 27.9539)\,u_1 + 13.85\,u_2 = 0 \;\Rightarrow\; -12.2539\,u_1 + 13.85\,u_2 = 0$$

Take u = (13.85, 12.2539). Its length is √(191.8225 + 150.1591) = √341.9816 = 18.4927.

$$\text{PC1} = \frac{(13.85,\ 12.2539)}{18.4927} = (0.7489,\ 0.6626)$$

PC2 is PC1 turned 90°: **(−0.6626, 0.7489)**. Check: PC1·PC2 = −0.4962 + 0.4962 = 0 ✓.

$$\mathbf A = \begin{bmatrix}\text{PC1} \\ \text{PC2}\end{bmatrix} = \boxed{\begin{bmatrix}0.7489 & 0.6626\\ -0.6626 & 0.7489\end{bmatrix}} \quad (\text{sl.24's } \mathbf R)$$

Angle: tan⁻¹(0.6626/0.7489) = **41.5°**, the same as B1.

<details>
<summary>Note: the same thing in MATLAB (sl.23, 28, 30): probe Q2–Q3</summary>

- `coeff` = [0.7489 −0.6626; 0.6626 0.7489]. Its **columns** are PC1, PC2, so A = coeffᵀ.
- `[V,D] = eig(S)` gives D = diag(0.0461, 27.9539). That's **ascending**, so PC1 is V's **last** column: (−0.7489, −0.6626) = −PC1. A −1 flips the arrow, not the axis, so it's still PC1.
- `latent` = (27.9539, 0.0461) = the λ's, largest first.

</details>

---

## Part 4: rotate the data → score (sl.25–27)

### 4a. Find point 1's and point 2's coordinates on PC1 and PC2.

**Solution**

Each coordinate is a dot product: a row of A with the **centred** point (B2's Xᵢ = Bᵢ·x).

Point 1, centred: (−5.2, −4.6)
- on PC1: 0.7489 × (−5.2) + 0.6626 × (−4.6) = −3.8943 − 3.0480 = **−6.9423**
- on PC2: −0.6626 × (−5.2) + 0.7489 × (−4.6) = 3.4455 − 3.4449 = **0.0006**

Point 2, centred: (−2.2, −1.6)
- on PC1: 0.7489 × (−2.2) + 0.6626 × (−1.6) = −1.6476 − 1.0602 = **−2.7078**
- on PC2: −0.6626 × (−2.2) + 0.7489 × (−1.6) = 1.4577 − 1.1982 = **0.2595**

The full `score` (sl.25, full precision):

| point | PC1 | PC2 |
|---|---|---|
| 1 | −6.9426 | 0.0006 |
| 2 | −2.7079 | 0.2595 |
| 3 | −0.5474 | −0.3168 |
| 4 | 3.6874 | −0.0579 |
| 5 | 6.5105 | 0.1147 |

(At 4 dp, A gives −6.9423 instead of −6.9426: rounding only.)

<details>
<summary>Note: P×N vs N×P (sl.3–4, 22)</summary>

Notes layout (P×N, points in columns): **Y = A X**. MATLAB layout (N×P, points in rows): **score = data′ · coeff**. It's the same sum, transposed: (A X)ᵀ = Xᵀ Aᵀ = data′ · coeff.

</details>

---

## Part 5: why the rotation diagonalises S (sl.31–35): probe Q4

### 5a. Multiply out S_y = A S_x Aᵀ.

**Solution**

S_x is the **before** covariance: correlated, with 13.85 off the diagonal.

Step 1, A S_x:

$$(\mathbf{AS})_{11} = 0.7489\cdot15.7 + 0.6626\cdot13.85 = 11.7577 + 9.1770 = 20.9347$$
$$(\mathbf{AS})_{12} = 0.7489\cdot13.85 + 0.6626\cdot12.3 = 10.3723 + 8.1500 = 18.5223$$
$$(\mathbf{AS})_{21} = -0.6626\cdot15.7 + 0.7489\cdot13.85 = -10.4028 + 10.3723 = -0.0305$$
$$(\mathbf{AS})_{22} = -0.6626\cdot13.85 + 0.7489\cdot12.3 = -9.1770 + 9.2115 = 0.0345$$

Step 2, (A S_x) Aᵀ: each entry is a row of AS dotted with a row of A.

$$(\mathbf S_y)_{11} = 20.9347\cdot0.7489 + 18.5223\cdot0.6626 = 15.6780 + 12.2729 = 27.9509$$
$$(\mathbf S_y)_{12} = 20.9347\cdot(-0.6626) + 18.5223\cdot0.7489 = -13.8713 + 13.8714 = 0.0001$$
$$(\mathbf S_y)_{21} = -0.0305\cdot0.7489 + 0.0345\cdot0.6626 = -0.0228 + 0.0229 = 0.0001$$
$$(\mathbf S_y)_{22} = -0.0305\cdot(-0.6626) + 0.0345\cdot0.7489 = 0.0202 + 0.0258 = 0.0460$$

$$\mathbf S_y \approx \boxed{\begin{bmatrix}27.95 & 0\\ 0 & 0.046\end{bmatrix}} = \text{latent on the diagonal}$$

(The 4-dp rounding of A leaves 0.0001 off the diagonal and 27.9509 instead of 27.9539. At full precision it is exactly diag(27.9539, 0.0461).)

<details>
<summary>Note: the one-line reason (A3's X K Xᵀ)</summary>

S_x = X K Xᵀ, where the columns of X are the eigenvectors. Choose A = Xᵀ, so the rows of A are the eigenvectors:

S_y = Xᵀ(X K Xᵀ)X = (XᵀX) K (XᵀX) = I K I = **K**.

Look at step 1: row 1 of AS is (20.9347, 18.5223) = 27.9539 × (0.7489, 0.6626) = λ₁·PC1. That's S·u = λu, as in B1 6c. Dotting λ₁PC1 with PC2 gives 0 because they're perpendicular. That's why the off-diagonals vanish.

</details>

---

## Part 6: whitening (sl.41–45): probe Q5 *(numbers added)*

### 6a. Whiten point 1's score (−6.9426, 0.0006).

**Solution**

Step 4 of the pipeline divides each PC coordinate by its own standard deviation, √λ:

- √27.9539 = 5.2871, √0.0461 = 0.2146
- PC1: −6.9426 / 5.2871 = **−1.3131**
- PC2: 0.0006 / 0.2146 = **0.0028** (full precision: 0.0026)

Variance scales by the **square** of the factor, so the new variances are λᵢ/(√λᵢ)² = 1 and S = **I** ✓ (checked on all 5 points).

<details>
<summary>Note: the four steps, and which one does what</summary>

| Step | Does | S afterwards (this data) |
|---|---|---|
| 1 centre | removes the means | [15.7 13.85; 13.85 12.3] |
| 2 z-score (optional) | ÷ each **variable's** σ. Fixes units | [1 0.9967; 0.9967 1]: **still correlated** |
| 3 rotate onto the PCs | **this** step zeroes the covariance | diag(λ₁, λ₂) |
| 4 ÷√λ per PC | equalises the spread | I |

Step 2 divides the *original* variables; step 4 divides the *PCs*. If you do step 2, the PCs change (see E4).

</details>

---

## Part 7: scree, how many PCs to keep (sl.50–52)

### 7a. Three PCs have λ = 16, 4, 0.1. Use the average-λ threshold. Then find the share kept with one PC and with two.

**Solution**

- λ_thresh = (16 + 4 + 0.1)/3 = 20.1/3 = **6.7**. Only 16 > 6.7, so the rule keeps PC1.
- Share with PC1: 16/20.1 = **79.6 %** ≈ 80 % (sl.51).
- Share with PC1 + PC2: (16 + 4)/20.1 = 20/20.1 = **99.5 %**.

Keeping two loses only 0.5 % instead of 20 %. sl.52's point is that the average rule suits many eigenvalues; with three, look at the shares.

---

## Exercises (invented: no B4 practical exists)

### E1. Five samples: (1, 1), (3, 3), (4, 3), (5, 5), (7, 3). Use ÷(N−1).
(a) S. (b) λ₁, λ₂ and PC1's share. (c) A. (d) The score of (1, 1). (e) Show S_y = diag(λ₁, λ₂). (f) The whitening factors.
(g) Suppose `[V,D] = eig(S)` returns D = diag(1, 6) and V = [0.4472 −0.8944; −0.8944 −0.4472]. Which column is PC1?

<details>
<summary>Answers</summary>

(a) Means (4, 3). Centred: (−3, −2), (−1, 0), (0, 0), (1, 2), (3, 0).
Σdx² = 9+1+0+1+9 = 20, Σdxdy = 6+0+0+2+0 = 8, Σdy² = 4+0+0+4+0 = 8. ÷4 → **S = [5 2; 2 2]**.

(b) λ² − 7λ + (10 − 4) = 0 → (λ − 6)(λ − 1) = 0 → **λ = 6, 1**. Share: 6/7 = **85.7 %**.

(c) (S − 6I)u = 0, row 1: −u₁ + 2u₂ = 0 → u = (2, 1)/√5. PC2 = (−1, 2)/√5. **A = (1/√5)[2 1; −1 2]** (26.6°).

(d) Centred (−3, −2): PC1 = (2·(−3) + 1·(−2))/√5 = −8/√5 = **−3.578**; PC2 = (−1·(−3) + 2·(−2))/√5 = −1/√5 = **−0.447**.

(e) AS = (1/√5)[12 6; −1 2] (= rows 6·(2,1) and 1·(−1,2): λu again).
(AS)Aᵀ = (1/5)[12·2+6·1, 12·(−1)+6·2; −1·2+2·1, −1·(−1)+2·2] = (1/5)[30 0; 0 5] = **[6 0; 0 1]** ✓.

(f) ÷√6 = 2.449 on PC1, ÷√1 = 1 on PC2.

(g) D is ascending, so PC1 (λ = 6) is **column 2**: (−0.8944, −0.4472) = −(2, 1)/√5, the same axis with the arrow flipped.

</details>

### E2. Three variables have S = [5 1 0; 1 5 0; 0 0 0.2]. Find the PCs, apply the average-λ rule, and give the share kept.

<details>
<summary>Answers</summary>

det(S − λI) = (0.2 − λ)[(5 − λ)² − 1] = 0 → λ = 0.2, and 5 − λ = ±1 → λ = 6, 4.
- PC1 (λ = 6): (1, 1, 0)/√2. PC2 (λ = 4): (1, −1, 0)/√2. PC3 (λ = 0.2): (0, 0, 1).
- Threshold = 10.2/3 = **3.4** → keep PC1 and PC2.
- Share kept = 10/10.2 = **98.0 %** (PC1 alone: 6/10.2 = 58.8 %).

</details>

### E3. Notes layout: X is 2×N (points in columns). MATLAB gives coeff (2×2). Write Y in terms of coeff and X, and give the shape of Y and of score.

<details>
<summary>Answers</summary>

A = coeffᵀ, so **Y = coeffᵀ X**, which is 2×N. score = Yᵀ is N×2.

</details>

### E4. *(added, sl.43)* z-score the slides' data first. What does S become, and where does PC1 point?

<details>
<summary>Answers</summary>

z-scoring makes each variance 1, so S becomes the correlation matrix:
ρ = 13.85/√(15.7 × 12.3) = 13.85/13.8964 = **0.9967**, giving S = [1 0.9967; 0.9967 1].
λ = 1 ± ρ = **1.9967, 0.0033**. PC1 = (1, 1)/√2, at **45°**: any [1 ρ; ρ 1] has its PCs at 45°. Not 41.5°: z-scoring changes the PC directions, whereas the ÷N vs ÷(N−1) choice doesn't.

</details>
