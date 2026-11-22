# A2 QR and LU: worked examples

**What this page is for:** worked calculations, with every multiplication written out entry by entry. Read one step, then cover it and redo it on paper. Numbers are carried at 4 dp, as you would by hand, so final answers can drift in the 4th dp. The exact answer is given at the end of each part.
**Concepts and gaps** live in the [A2 QR lab](https://claude.ai/artifact/DvMjRDPedttK8nKWvHjXCa) (`A2_qr_lab.html`, same folder). It covers why multiplying by G keeps x, Givens as a rotation, zeroing order, Householder as a mirror, rank, and tall/wide problems.
Progress across Section A: [`section_A_progress.md`](section_A_progress.md).

Sources: Part 1 is the lecture's 2×2 (A2 sl.14, verbatim). Part 2 is the **Givens practical** and Part 3 the **Householder practical** (`../../drills/givens_rotation/`, `../../drills/householder_reflection/`), kept exactly as given. Part 4's L and U are *(added)*: the LU of Part 2's A. Every number was checked with numpy/sympy (2026-11-22).

**Watch out:** the two practicals use different matrices. Row 1 is $(-1, 1, \mathbf 3)$ in Givens and $(-1, 1, \mathbf{-3})$ in Householder.

**How to multiply (A1):** entry $(i,j)$ of $\mathbf{GA}$ = row $i$ of $\mathbf G$ · column $j$ of $\mathbf A$. Where a row of G is just a 1 on the diagonal, that row of A copies straight across.

---

## The three recipes

**Givens.** Kill one entry $b$ using the pivot $a$ on the diagonal above it (pivot row $i$, kill row $k$):
1. $r = \sqrt{a^2 + b^2}$, $\quad c = a/r$, $\quad s = b/r$ (no angle needed)
2. $\mathbf G$ = I, with $G_{ii} = c,\ G_{ik} = s,\ G_{ki} = -s,\ G_{kk} = c$
3. $\mathbf A \leftarrow \mathbf{GA}$ and $\mathbf b \leftarrow \mathbf{Gb}$. Only rows $i$ and $k$ change.
4. Order for 3×3: $(1,0) \to (2,0) \to (2,1)$, i.e. column by column, so you never undo an earlier zero. Then back-substitute.

**Householder.** Clear a whole sub-column $\mathbf x$ in one go:
1. $\alpha = \|\mathbf x\|$
2. $\mathbf u = \mathbf x$, with its top entry replaced by $x_0 + \text{sign}(x_0)\,\alpha$
3. $\mathbf H = \mathbf I - \dfrac{2}{\mathbf u^T\mathbf u}\,\mathbf u\mathbf u^T$. In step 2, put it in the bottom-right corner of $\mathbf I_3$.
4. $\mathbf A \leftarrow \mathbf{HA}$ and $\mathbf b \leftarrow \mathbf{Hb}$. Two steps for 3×3, then back-substitute.

**LU.** Given $\mathbf A = \mathbf{LU}$: solve $\mathbf{Ly} = \mathbf b$ **top-down**, then $\mathbf{Ux} = \mathbf y$ **bottom-up**.

---

## Part 1: Givens on the lecture's 2×2 (sl.14, verbatim)

$$\begin{bmatrix}3\\1\end{bmatrix} = \begin{bmatrix}3 & 7\\5 & 8\end{bmatrix}\begin{bmatrix}x_0\\x_1\end{bmatrix}$$

The lecture uses $\mathbf G = \begin{bmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{bmatrix}$ and aims for **lower** triangular, so it kills the top-right 7.

**1. Pick c and s.** The top-right entry of GA is (row 0 of G)·(column 1 of A) $= 7\cos\theta - 8\sin\theta$. Set it to 0:
$$\tan\theta = \tfrac{7}{8} \;\Rightarrow\; \cos\theta = \tfrac{8}{\sqrt{7^2+8^2}} = \tfrac{8}{10.6301} = 0.7526,\quad \sin\theta = \tfrac{7}{10.6301} = 0.6585$$

**2. Build G.**
$$\mathbf G = \begin{bmatrix}0.7526 & -0.6585\\0.6585 & 0.7526\end{bmatrix}$$

**3. Multiply G·A** (entry $(i,j)$ = row $i$ of G · column $j$ of A):
$$\begin{aligned}
(GA)_{00} &= 0.7526\cdot 3 + (-0.6585)\cdot 5 = 2.2578 - 3.2925 = -1.0347\\
(GA)_{01} &= 0.7526\cdot 7 + (-0.6585)\cdot 8 = 5.2682 - 5.2680 \approx 0\;✓\\
(GA)_{10} &= 0.6585\cdot 3 + 0.7526\cdot 5 = 1.9755 + 3.7630 = 5.7385\\
(GA)_{11} &= 0.6585\cdot 7 + 0.7526\cdot 8 = 4.6095 + 6.0208 = 10.6303
\end{aligned}$$
$$\mathbf{GA} = \begin{bmatrix}-1.0347 & 0\\5.7385 & 10.6303\end{bmatrix}$$

**4. Multiply G·b:**
$$\begin{aligned}
(Gb)_{0} &= 0.7526\cdot 3 + (-0.6585)\cdot 1 = 2.2578 - 0.6585 = 1.5993\\
(Gb)_{1} &= 0.6585\cdot 3 + 0.7526\cdot 1 = 1.9755 + 0.7526 = 2.7281
\end{aligned}$$

**5. Solve top-down** (lower triangular, so row 0 has one unknown):
$$\begin{bmatrix}-1.0347 & 0\\5.7385 & 10.6303\end{bmatrix}\begin{bmatrix}x_0\\x_1\end{bmatrix} = \begin{bmatrix}1.5993\\2.7281\end{bmatrix}$$
$$\begin{aligned}
x_0 &= \frac{1.5993}{-1.0347} = -1.5457\\
x_1 &= \frac{2.7281 - 5.7385\cdot (-1.5457)}{10.6303} = \frac{2.7281 + 8.8700}{10.6303} = 1.0910
\end{aligned}$$

Slide: $x = (-1.55,\ 1.091)$ ✓ (exact: $-\tfrac{17}{11},\ \tfrac{12}{11}$).

## Part 2: Givens on the practical's 3×3

$$\mathbf A = \begin{bmatrix}3 & 4 & 5\\-1 & 1 & 3\\2 & -2 & 3\end{bmatrix},\qquad \mathbf b = \begin{bmatrix}7\\1\\5\end{bmatrix}$$

Goal: **upper** triangular. Kill $(1,0)$, then $(2,0)$, then $(2,1)$: column by column, left to right.

### Step 1: kill $a_{10} = -1$ using the pivot $a_{00} = 3$

**1. c and s** ($a$ = pivot, $b$ = the one to kill):
$$r = \sqrt{3^2 + (-1)^2} = \sqrt{9 + 1} = 3.1623,\qquad c = \frac{3}{3.1623} = 0.9487,\qquad s = \frac{-1}{3.1623} = -0.3162$$

**2. Build G.** Start from I. Put $c, s$ in rows/columns 0 and 1: the pivot row gets $(c, s)$ and the killed row gets $(-s, c)$.
$$\mathbf G_1 = \begin{bmatrix}c & s & 0\\-s & c & 0\\0 & 0 & 1\end{bmatrix} = \begin{bmatrix}0.9487 & -0.3162 & 0\\0.3162 & 0.9487 & 0\\0 & 0 & 1\end{bmatrix}$$

**3. Multiply $\mathbf G_1\mathbf A$.** Row 2 of G is just a 1 on the diagonal, so row 2 of A copies straight across. Only rows 0 and 1 change.
$$\begin{aligned}
(GA)_{00} &= 0.9487\cdot 3 + (-0.3162)\cdot (-1) = 2.8461 + 0.3162 = 3.1623\\
(GA)_{01} &= 0.9487\cdot 4 + (-0.3162)\cdot 1 = 3.7948 - 0.3162 = 3.4786\\
(GA)_{02} &= 0.9487\cdot 5 + (-0.3162)\cdot 3 = 4.7435 - 0.9486 = 3.7949\\
(GA)_{10} &= 0.3162\cdot 3 + 0.9487\cdot (-1) = 0.9486 - 0.9487 \approx 0\;✓\\
(GA)_{11} &= 0.3162\cdot 4 + 0.9487\cdot 1 = 1.2648 + 0.9487 = 2.2135\\
(GA)_{12} &= 0.3162\cdot 5 + 0.9487\cdot 3 = 1.5810 + 2.8461 = 4.4271
\end{aligned}$$

**4. Multiply $\mathbf G_1\mathbf b$:**
$$\begin{aligned}
(Gb)_{0} &= 0.9487\cdot 7 + (-0.3162)\cdot 1 = 6.6409 - 0.3162 = 6.3247\\
(Gb)_{1} &= 0.3162\cdot 7 + 0.9487\cdot 1 = 2.2134 + 0.9487 = 3.1621
\end{aligned}$$

**After step 1:**
$$\mathbf A^{(1)} = \begin{bmatrix}3.1623 & 3.4786 & 3.7949\\0 & 2.2135 & 4.4271\\2 & -2 & 3\end{bmatrix},\qquad \mathbf b^{(1)} = \begin{bmatrix}6.3247\\3.1621\\5\end{bmatrix}$$

### Step 2: kill $a_{20} = 2$ using the pivot $a_{00} = 3.1623$

**1. c and s** ($a$ = pivot, $b$ = the one to kill):
$$r = \sqrt{3.1623^2 + 2^2} = \sqrt{10.0001 + 4} = 3.7417,\qquad c = \frac{3.1623}{3.7417} = 0.8452,\qquad s = \frac{2}{3.7417} = 0.5345$$

**2. Build G.** Start from I. Put $c, s$ in rows/columns 0 and 2: the pivot row gets $(c, s)$ and the killed row gets $(-s, c)$.
$$\mathbf G_2 = \begin{bmatrix}c & 0 & s\\0 & 1 & 0\\-s & 0 & c\end{bmatrix} = \begin{bmatrix}0.8452 & 0 & 0.5345\\0 & 1 & 0\\-0.5345 & 0 & 0.8452\end{bmatrix}$$

**3. Multiply $\mathbf G_2\mathbf A$.** Row 1 of G is just a 1 on the diagonal, so row 1 of A copies straight across. Only rows 0 and 2 change.
$$\begin{aligned}
(GA)_{00} &= 0.8452\cdot 3.1623 + 0.5345\cdot 2 = 2.6728 + 1.0690 = 3.7418\\
(GA)_{01} &= 0.8452\cdot 3.4786 + 0.5345\cdot (-2) = 2.9401 - 1.0690 = 1.8711\\
(GA)_{02} &= 0.8452\cdot 3.7949 + 0.5345\cdot 3 = 3.2074 + 1.6035 = 4.8109\\
(GA)_{20} &= (-0.5345)\cdot 3.1623 + 0.8452\cdot 2 = -1.6902 + 1.6904 \approx 0\;✓\\
(GA)_{21} &= (-0.5345)\cdot 3.4786 + 0.8452\cdot (-2) = -1.8593 - 1.6904 = -3.5497\\
(GA)_{22} &= (-0.5345)\cdot 3.7949 + 0.8452\cdot 3 = -2.0284 + 2.5356 = 0.5072
\end{aligned}$$

**4. Multiply $\mathbf G_2\mathbf b$:**
$$\begin{aligned}
(Gb)_{0} &= 0.8452\cdot 6.3247 + 0.5345\cdot 5 = 5.3456 + 2.6725 = 8.0181\\
(Gb)_{2} &= (-0.5345)\cdot 6.3247 + 0.8452\cdot 5 = -3.3806 + 4.2260 = 0.8454
\end{aligned}$$

**After step 2:**
$$\mathbf A^{(2)} = \begin{bmatrix}3.7418 & 1.8711 & 4.8109\\0 & 2.2135 & 4.4271\\0 & -3.5497 & 0.5072\end{bmatrix},\qquad \mathbf b^{(2)} = \begin{bmatrix}8.0181\\3.1621\\0.8454\end{bmatrix}$$

### Step 3: kill $a_{21} = -3.5497$ using the pivot $a_{11} = 2.2135$

**1. c and s** ($a$ = pivot, $b$ = the one to kill):
$$r = \sqrt{2.2135^2 + (-3.5497)^2} = \sqrt{4.8996 + 12.6004} = 4.1833,\qquad c = \frac{2.2135}{4.1833} = 0.5291,\qquad s = \frac{-3.5497}{4.1833} = -0.8485$$

**2. Build G.** Start from I. Put $c, s$ in rows/columns 1 and 2: the pivot row gets $(c, s)$ and the killed row gets $(-s, c)$.
$$\mathbf G_3 = \begin{bmatrix}1 & 0 & 0\\0 & c & s\\0 & -s & c\end{bmatrix} = \begin{bmatrix}1 & 0 & 0\\0 & 0.5291 & -0.8485\\0 & 0.8485 & 0.5291\end{bmatrix}$$

**3. Multiply $\mathbf G_3\mathbf A$.** Row 0 of G is just a 1 on the diagonal, so row 0 of A copies straight across. Only rows 1 and 2 change. Column 0 of rows 1 and 2 is already 0, and $c\cdot0 + s\cdot0 = 0$, so it stays 0 (skipped below).
$$\begin{aligned}
(GA)_{11} &= 0.5291\cdot 2.2135 + (-0.8485)\cdot (-3.5497) = 1.1712 + 3.0119 = 4.1831\\
(GA)_{12} &= 0.5291\cdot 4.4271 + (-0.8485)\cdot 0.5072 = 2.3424 - 0.4304 = 1.9120\\
(GA)_{21} &= 0.8485\cdot 2.2135 + 0.5291\cdot (-3.5497) = 1.8782 - 1.8781 \approx 0\;✓\\
(GA)_{22} &= 0.8485\cdot 4.4271 + 0.5291\cdot 0.5072 = 3.7564 + 0.2684 = 4.0248
\end{aligned}$$

**4. Multiply $\mathbf G_3\mathbf b$:**
$$\begin{aligned}
(Gb)_{1} &= 0.5291\cdot 3.1621 + (-0.8485)\cdot 0.8454 = 1.6731 - 0.7173 = 0.9558\\
(Gb)_{2} &= 0.8485\cdot 3.1621 + 0.5291\cdot 0.8454 = 2.6830 + 0.4473 = 3.1303
\end{aligned}$$

**After step 3:**
$$\mathbf A^{(3)} = \begin{bmatrix}3.7418 & 1.8711 & 4.8109\\0 & 4.1831 & 1.9120\\0 & 0 & 4.0248\end{bmatrix},\qquad \mathbf b^{(3)} = \begin{bmatrix}8.0181\\0.9558\\3.1303\end{bmatrix}$$

### Step 4: back-substitute (bottom row first)

$$\begin{bmatrix}3.7418 & 1.8711 & 4.8109\\0 & 4.1831 & 1.9120\\0 & 0 & 4.0248\end{bmatrix}\begin{bmatrix}x_0\\x_1\\x_2\end{bmatrix} = \begin{bmatrix}8.0181\\0.9558\\3.1303\end{bmatrix}$$
$$\begin{aligned}
x_2 &= \frac{3.1303}{4.0248} = 0.7778\\
x_1 &= \frac{0.9558 - 1.9120\cdot 0.7778}{4.1831} = \frac{0.9558 - 1.4872}{4.1831} = \frac{-0.5314}{4.1831} = -0.1270\\
x_0 &= \frac{8.0181 - 1.8711\cdot (-0.1270) - 4.8109\cdot 0.7778}{3.7418} = \frac{8.0181 - (-0.2376) - 3.7419}{3.7418} = \frac{4.5138}{3.7418} = 1.2063
\end{aligned}$$

**Exact:** $\mathbf x = (\tfrac{76}{63},\ -\tfrac{8}{63},\ \tfrac{7}{9}) = (1.2063,\ -0.1270,\ 0.7778)$ ✓. Working at 4 dp, your last digit can drift by a few units. That's fine.

**Check** with the original row 0: $3(1.2063) + 4(-0.1270) + 5(0.7778) = 3.6189 - 0.5080 + 3.8890 = 7.000$ ✓

## Part 3: Householder on the practical's 3×3

$$\mathbf A = \begin{bmatrix}3 & 4 & 5\\-1 & 1 & \mathbf{-3}\\2 & -2 & 3\end{bmatrix},\qquad \mathbf b = \begin{bmatrix}7\\1\\5\end{bmatrix}$$

(Note the **−3**: this is not the Givens matrix.)

### Step 1: clear column 0 below the diagonal (rows 0–2)

**1. The sub-column and its length:**
$$\mathbf x = \begin{bmatrix}3\\-1\\2\end{bmatrix},\qquad \alpha = \sqrt{3^2 + (-1)^2 + 2^2} = \sqrt{9 + 1 + 4} = 3.7417$$

**2. Target and u.** The target is $\mathbf x' = \begin{bmatrix}-3.7417\\0\\0\end{bmatrix}$ (same length, zeros below). The sign is opposite to $x_0$ (positive here), as in the practical.
$$\mathbf u = \mathbf x - \mathbf x' = \begin{bmatrix}6.7417\\-1\\2\end{bmatrix}\qquad(\text{only the top entry changes: } 3 + 3.7417 = 6.7417)$$

**3. $\mathbf u\mathbf u^T$ and $\mathbf u^T\mathbf u$** (entry $(i,j)$ of $\mathbf u\mathbf u^T$ is $u_i u_j$):
$$\mathbf u\mathbf u^T = \begin{bmatrix}45.4505 & -6.7417 & 13.4834\\-6.7417 & 1 & -2\\13.4834 & -2 & 4\end{bmatrix},\qquad \mathbf u^T\mathbf u = 45.4505 + 1 + 4 = 50.4505,\qquad \frac{2}{\mathbf u^T\mathbf u} = 0.039643$$

**4. $\mathbf H = \mathbf I - \frac{2}{\mathbf u^T\mathbf u}\mathbf u\mathbf u^T$**, entry by entry. It's symmetric, so only the upper half is shown:
$$\begin{aligned}
H_{00} &= 1 - 0.039643\cdot 45.4505 = -0.8018\\
H_{01} &= 0 - 0.039643\cdot (-6.7417) = 0.2673\\
H_{02} &= 0 - 0.039643\cdot 13.4834 = -0.5345\\
H_{11} &= 1 - 0.039643\cdot 1 = 0.9604\\
H_{12} &= 0 - 0.039643\cdot (-2) = 0.0793\\
H_{22} &= 1 - 0.039643\cdot 4 = 0.8414
\end{aligned}$$
$$\mathbf H_1 = \begin{bmatrix}-0.8018 & 0.2673 & -0.5345\\0.2673 & 0.9604 & 0.0793\\-0.5345 & 0.0793 & 0.8414\end{bmatrix}$$

**5. Multiply HA.** All three rows change, because H is full.
$$\begin{aligned}
(HA)_{00} &= (-0.8018)\cdot 3 + 0.2673\cdot (-1) + (-0.5345)\cdot 2 = -2.4054 - 0.2673 - 1.0690 = -3.7417\\
(HA)_{01} &= (-0.8018)\cdot 4 + 0.2673\cdot 1 + (-0.5345)\cdot (-2) = -3.2072 + 0.2673 + 1.0690 = -1.8709\\
(HA)_{02} &= (-0.8018)\cdot 5 + 0.2673\cdot (-3) + (-0.5345)\cdot 3 = -4.0090 - 0.8019 - 1.6035 = -6.4144\\
(HA)_{10} &= 0.2673\cdot 3 + 0.9604\cdot (-1) + 0.0793\cdot 2 = 0.8019 - 0.9604 + 0.1586 \approx 0\;✓\\
(HA)_{11} &= 0.2673\cdot 4 + 0.9604\cdot 1 + 0.0793\cdot (-2) = 1.0692 + 0.9604 - 0.1586 = 1.8710\\
(HA)_{12} &= 0.2673\cdot 5 + 0.9604\cdot (-3) + 0.0793\cdot 3 = 1.3365 - 2.8812 + 0.2379 = -1.3068\\
(HA)_{20} &= (-0.5345)\cdot 3 + 0.0793\cdot (-1) + 0.8414\cdot 2 = -1.6035 - 0.0793 + 1.6828 \approx 0\;✓\\
(HA)_{21} &= (-0.5345)\cdot 4 + 0.0793\cdot 1 + 0.8414\cdot (-2) = -2.1380 + 0.0793 - 1.6828 = -3.7415\\
(HA)_{22} &= (-0.5345)\cdot 5 + 0.0793\cdot (-3) + 0.8414\cdot 3 = -2.6725 - 0.2379 + 2.5242 = -0.3862
\end{aligned}$$

**6. Multiply Hb:**
$$\begin{aligned}
(Hb)_{0} &= (-0.8018)\cdot 7 + 0.2673\cdot 1 + (-0.5345)\cdot 5 = -5.6126 + 0.2673 - 2.6725 = -8.0178\\
(Hb)_{1} &= 0.2673\cdot 7 + 0.9604\cdot 1 + 0.0793\cdot 5 = 1.8711 + 0.9604 + 0.3965 = 3.2280\\
(Hb)_{2} &= (-0.5345)\cdot 7 + 0.0793\cdot 1 + 0.8414\cdot 5 = -3.7415 + 0.0793 + 4.2070 = 0.5448
\end{aligned}$$

**After step 1:**
$$\mathbf A^{(1)} = \begin{bmatrix}-3.7417 & -1.8709 & -6.4144\\0 & 1.8710 & -1.3068\\0 & -3.7415 & -0.3862\end{bmatrix},\qquad \mathbf b^{(1)} = \begin{bmatrix}-8.0178\\3.2280\\0.5448\end{bmatrix}$$

### Step 2: clear column 1 below the diagonal (rows 1–2 only)

**1. The sub-column and its length:**
$$\mathbf x = \begin{bmatrix}1.8710\\-3.7415\end{bmatrix},\qquad \alpha = \sqrt{1.8710^2 + (-3.7415)^2} = \sqrt{3.5006 + 13.9988} = 4.1832$$

**2. Target and u.** The target is $\mathbf x' = \begin{bmatrix}-4.1832\\0\end{bmatrix}$ (same length, zeros below). The sign is opposite to $x_0$ (positive here), as in the practical.
$$\mathbf u = \mathbf x - \mathbf x' = \begin{bmatrix}6.0542\\-3.7415\end{bmatrix}\qquad(\text{only the top entry changes: } 1.8710 + 4.1832 = 6.0542)$$

**3. $\mathbf u\mathbf u^T$ and $\mathbf u^T\mathbf u$** (entry $(i,j)$ of $\mathbf u\mathbf u^T$ is $u_i u_j$):
$$\mathbf u\mathbf u^T = \begin{bmatrix}36.6533 & -22.6518\\-22.6518 & 13.9988\end{bmatrix},\qquad \mathbf u^T\mathbf u = 36.6533 + 13.9988 = 50.6521,\qquad \frac{2}{\mathbf u^T\mathbf u} = 0.039485$$

**4. $\mathbf H = \mathbf I - \frac{2}{\mathbf u^T\mathbf u}\mathbf u\mathbf u^T$**, entry by entry. It's symmetric, so only the upper half is shown:
$$\begin{aligned}
H_{11} &= 1 - 0.039485\cdot 36.6533 = -0.4473\\
H_{12} &= 0 - 0.039485\cdot (-22.6518) = 0.8944\\
H_{22} &= 1 - 0.039485\cdot 13.9988 = 0.4473
\end{aligned}$$
Embed it in the bottom-right corner of $\mathbf I_3$, so row 0 and column 0 are left alone:
$$\mathbf H_2 = \begin{bmatrix}1 & 0 & 0\\0 & -0.4473 & 0.8944\\0 & 0.8944 & 0.4473\end{bmatrix}$$

**5. Multiply HA.** Row 0 of $\mathbf H_2$ is $(1, 0, 0)$, so row 0 copies. In column 0, rows 1–2 are already 0 and stay 0 (skipped).
$$\begin{aligned}
(HA)_{11} &= (-0.4473)\cdot 1.8710 + 0.8944\cdot (-3.7415) = -0.8369 - 3.3464 = -4.1833\\
(HA)_{12} &= (-0.4473)\cdot (-1.3068) + 0.8944\cdot (-0.3862) = 0.5845 - 0.3454 = 0.2391\\
(HA)_{21} &= 0.8944\cdot 1.8710 + 0.4473\cdot (-3.7415) = 1.6734 - 1.6736 \approx 0\;✓\\
(HA)_{22} &= 0.8944\cdot (-1.3068) + 0.4473\cdot (-0.3862) = -1.1688 - 0.1727 = -1.3415
\end{aligned}$$

**6. Multiply Hb:**
$$\begin{aligned}
(Hb)_{1} &= (-0.4473)\cdot 3.2280 + 0.8944\cdot 0.5448 = -1.4439 + 0.4873 = -0.9566\\
(Hb)_{2} &= 0.8944\cdot 3.2280 + 0.4473\cdot 0.5448 = 2.8871 + 0.2437 = 3.1308
\end{aligned}$$

**After step 2:**
$$\mathbf A^{(2)} = \begin{bmatrix}-3.7417 & -1.8709 & -6.4144\\0 & -4.1833 & 0.2391\\0 & 0 & -1.3415\end{bmatrix},\qquad \mathbf b^{(2)} = \begin{bmatrix}-8.0178\\-0.9566\\3.1308\end{bmatrix}$$

### Step 3: back-substitute

$$\begin{bmatrix}-3.7417 & -1.8709 & -6.4144\\0 & -4.1833 & 0.2391\\0 & 0 & -1.3415\end{bmatrix}\begin{bmatrix}x_0\\x_1\\x_2\end{bmatrix} = \begin{bmatrix}-8.0178\\-0.9566\\3.1308\end{bmatrix}$$
$$\begin{aligned}
x_2 &= \frac{3.1308}{-1.3415} = -2.3338\\
x_1 &= \frac{-0.9566 - 0.2391\cdot (-2.3338)}{-4.1833} = \frac{-0.9566 - (-0.5580)}{-4.1833} = \frac{-0.3986}{-4.1833} = 0.0953\\
x_0 &= \frac{-8.0178 - (-1.8709)\cdot 0.0953 - (-6.4144)\cdot (-2.3338)}{-3.7417} = \frac{-8.0178 - (-0.1783) - 14.9699}{-3.7417} = \frac{-22.8094}{-3.7417} = 6.0960
\end{aligned}$$

**Exact:** $\mathbf x = (\tfrac{128}{21},\ \tfrac{2}{21},\ -\tfrac{7}{3}) = (6.0952,\ 0.0952,\ -2.3333)$ ✓. That's the practical's answer. Ours is within 0.001, which is normal drift from rounding everything to 4 dp across two big steps.

The diagonal of R is negative because of the sign choice in step 2. It's still a valid triangular R.

## Part 4: LU (sl.48 method)

Given *(added: the LU of Part 2's A)*:
$$\underbrace{\begin{bmatrix}3 & 4 & 5\\-1 & 1 & 3\\2 & -2 & 3\end{bmatrix}}_{\mathbf A} = \underbrace{\begin{bmatrix}1 & 0 & 0\\-\frac13 & 1 & 0\\\frac23 & -2 & 1\end{bmatrix}}_{\mathbf L}\underbrace{\begin{bmatrix}3 & 4 & 5\\0 & \frac73 & \frac{14}3\\0 & 0 & 9\end{bmatrix}}_{\mathbf U},\qquad \mathbf b = \begin{bmatrix}7\\1\\5\end{bmatrix}$$

**Check $\mathbf{LU} = \mathbf A$** (row by row):
$$\begin{aligned}
\text{row 0} &= 1\cdot(3, 4, 5) = (3,\ 4,\ 5) \;✓\\
\text{row 1} &= -\tfrac13(3, 4, 5) + 1\cdot(0, \tfrac73, \tfrac{14}3) = (-1,\ -\tfrac43 + \tfrac73,\ -\tfrac53 + \tfrac{14}3) = (-1,\ 1,\ 3) \;✓\\
\text{row 2} &= \tfrac23(3, 4, 5) - 2(0, \tfrac73, \tfrac{14}3) + 1\cdot(0, 0, 9) = (2,\ \tfrac83 - \tfrac{14}3,\ \tfrac{10}3 - \tfrac{28}3 + 9) = (2,\ -2,\ 3) \;✓
\end{aligned}$$

### Step 1: $\mathbf{Ly} = \mathbf b$, top-down

$$\begin{bmatrix}1 & 0 & 0\\-\frac13 & 1 & 0\\\frac23 & -2 & 1\end{bmatrix}\begin{bmatrix}y_0\\y_1\\y_2\end{bmatrix} = \begin{bmatrix}7\\1\\5\end{bmatrix}$$
$$\begin{aligned}
\text{row 0:}\quad y_0 &= 7\\
\text{row 1:}\quad -\tfrac13(7) + y_1 = 1 \;\Rightarrow\; y_1 &= 1 + \tfrac73 = \tfrac{10}{3}\\
\text{row 2:}\quad \tfrac23(7) - 2(\tfrac{10}3) + y_2 = 5 \;\Rightarrow\; y_2 &= 5 - \tfrac{14}3 + \tfrac{20}3 = 7
\end{aligned}$$

### Step 2: $\mathbf{Ux} = \mathbf y$, bottom-up

$$\begin{bmatrix}3 & 4 & 5\\0 & \frac73 & \frac{14}3\\0 & 0 & 9\end{bmatrix}\begin{bmatrix}x_0\\x_1\\x_2\end{bmatrix} = \begin{bmatrix}7\\\frac{10}3\\7\end{bmatrix}$$
$$\begin{aligned}
\text{row 2:}\quad 9x_2 = 7 \;\Rightarrow\; x_2 &= \tfrac79 = 0.7778\\
\text{row 1:}\quad \tfrac73 x_1 + \tfrac{14}3\cdot\tfrac79 = \tfrac{10}3 \;\Rightarrow\; x_1 &= \tfrac37\left(\tfrac{10}3 - \tfrac{98}{27}\right) = \tfrac37\cdot\left(-\tfrac{8}{27}\right) = -\tfrac{8}{63} = -0.1270\\
\text{row 0:}\quad 3x_0 + 4(-\tfrac8{63}) + 5(\tfrac79) = 7 \;\Rightarrow\; x_0 &= \tfrac13\left(7 + \tfrac{32}{63} - \tfrac{245}{63}\right) = \tfrac13\cdot\tfrac{228}{63} = \tfrac{76}{63} = 1.2063
\end{aligned}$$

Same x as Part 2 ✓. It's the same problem solved with a different factorisation.

---

## Part 5: short worked examples (sl.29, 37, 51, 68)

### 5a. Solve with a given QR (sl.37)
If you're handed $\mathbf A = \mathbf{QR}$, there's no rotating to do:
$$\mathbf{QRx} = \mathbf b \;\Rightarrow\; \mathbf{Rx} = \mathbf Q^T\mathbf b \;\Rightarrow\; \text{back-substitute}$$
From Part 2, Q is the steps' transposes in order: $\mathbf G_3\mathbf G_2\mathbf G_1\mathbf A = \mathbf R \Rightarrow \mathbf Q = \mathbf G_1^T\mathbf G_2^T\mathbf G_3^T$ (sl.40). In practice you never build Q. You apply each G to b as you go, which is exactly what Part 2 did.

### 5b. Cost (sl.29)
A matrix × matrix product with N = 500 takes 1 s. How long for N = 5000?
1. Count the work: $N^2$ entries, each an N-term sum, gives $N^3$ multiply-adds, so it's $O(N^3)$.
2. Scale: $\left(\tfrac{5000}{500}\right)^3 = 10^3 = 1000$, so it takes **1000 s**. (N = 50 000: $10^6$ s ≈ 11.6 days.)

### 5c. Underspecified: 2 equations, 3 unknowns (sl.51, verbatim)
$$\begin{bmatrix}11\\14\end{bmatrix} = \begin{bmatrix}3 & 9 & -1\\4 & 8 & 2\end{bmatrix}\mathbf x$$
**What the lecture actually asks** (sl.51, 57, 61):
- 2 equations, 3 unknowns is **underspecified**: infinitely many solutions, so no unique one.
- More equations than unknowns is **overspecified**: no exact solution, and QR gives the best fit.
- When underspecified, QR on $\mathbf A^T$ picks the smallest-norm solution. The lecture gives no numbers for this.

1. **One solution** (the slide's): $\mathbf x = (1,1,1)$. Check: $3 + 9 - 1 = 11$ ✓, $4 + 8 + 2 = 14$ ✓

*Steps 2–4 are optional. They're my own hand shortcuts, not the lecture's method. Skip them if the three points above are clear.*

2. **The free direction** *(added)*: you need $\mathbf d$ with $\mathbf{Ad} = \mathbf 0$, i.e. perpendicular to both rows. That's their cross product:
$$(3,9,-1)\times(4,8,2) = \big(9\cdot2 - (-1)\cdot8,\;\; (-1)\cdot4 - 3\cdot2,\;\; 3\cdot8 - 9\cdot4\big) = (26,\ -10,\ -12) \;\propto\; (13,\ -5,\ -6)$$
Check: $3(13) + 9(-5) - 1(-6) = 39 - 45 + 6 = 0$ ✓, and $4(13) + 8(-5) + 2(-6) = 52 - 40 - 12 = 0$ ✓
3. **Every solution:** $\mathbf x = (1,1,1) + t\,(13,-5,-6)$ for any $t$
4. **The smallest one** (what QR picks, sl.61) *(added: a hand shortcut)*. Pick $t$ so that $\mathbf x \perp \mathbf d$:
$$t = -\frac{(1,1,1)\cdot(13,-5,-6)}{(13,-5,-6)\cdot(13,-5,-6)} = -\frac{13 - 5 - 6}{169 + 25 + 36} = -\frac{2}{230} = -0.0087$$
$$\mathbf x_{min} = (1 - 0.1130,\ \ 1 + 0.0435,\ \ 1 + 0.0522) = (0.887,\ 1.043,\ 1.052)$$

### 5d. Rank (sl.53, 68)
Is $\begin{bmatrix}3 & 9 & -1\\4 & 8 & 2\\8 & 16 & 4\end{bmatrix}$ full rank?
1. Compare rows: row 2 $= (8, 16, 4) = 2\times(4, 8, 2) = 2\times$ row 1. That's the same equation written twice.
2. So there are only 2 independent equations: **rank 2**.
3. QR shows it as a 0 on R's diagonal (numpy):
$$\mathbf R = \begin{bmatrix}-9.434 & -19.822 & -3.922\\0 & 2.844 & -2.370\\0 & 0 & \mathbf 0\end{bmatrix}$$
Back-substitution would have to divide by that 0, so there's no unique x.

*Flag:* the Householder notebook's flop table ("Givens ≈ 4/3 n³, Householder ≈ 2/3 n³") isn't from the slides and looks wrong. 2/3 n³ is LU's usual count. Don't learn those numbers.
