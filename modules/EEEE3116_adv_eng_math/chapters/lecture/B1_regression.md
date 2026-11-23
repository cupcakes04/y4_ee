# B1 regression, covariance and rotation: worked examples

**What this page is for:** worked calculations with every step written out. Read an example, cover the solution, then redo it on paper.
**Concepts and gaps** live in the B1 lab (`B1_regression_lab.html`, same folder).
Progress: [`progress.md`](progress.md).

Sources:
- Parts 1–4 and 6 use B1's own example (the 5 current–voltage points, sl.8) and its exercise (sl.23), with the numbers exactly as given.
- Parts 5 and 7 are the Section B practical's Q3 (covariance) and Q2 (rotation), with the numbers exactly as given (`drills/data_vec_tf/q3.png`, `q2.png`).
- The slides don't define the "reconstruction SNR" in Q2, so the definition used here is marked *(added)*.

Every number was recomputed with exact fractions in Python (2026-11-23). Where a value doesn't terminate, it's shown to 4 dp.

---

## Recipe cards

| Step | Formula | Slide |
|---|---|---|
| Mean, variance | $\bar y = \frac1N\sum y_i$, $\;\sigma_y^2 = \frac1N\sum (y_i-\bar y)^2$ (÷N, not N−1) | sl.9–10 |
| Total sum of squares | $SS_{tot} = \sum (y_i-\bar y)^2 = N\sigma_y^2$ | sl.11 |
| Residual | $r_i = y_i - (c + m x_i)$, $\;SS_{res} = \sum r_i^2$ | sl.12–13 |
| Normal equations | $\begin{bmatrix} N & \sum x \\ \sum x & \sum x^2\end{bmatrix}\begin{bmatrix} c\\ m\end{bmatrix} = \begin{bmatrix}\sum y\\ \sum xy\end{bmatrix}$, and that matrix is exactly $\mathbf X^T\mathbf X$ | sl.15–20 |
| 2×2 solve (Cramer) | $c = \dfrac{\sum x^2\sum y - \sum x\sum xy}{N\sum x^2 - (\sum x)^2}$, $\;m = \dfrac{N\sum xy - \sum x\sum y}{N\sum x^2 - (\sum x)^2}$ | sl.17 |
| Line goes through the mean point | $\bar y = c + m\bar x$ | sl.15 |
| Gradient descent | $m_{k+1} = m_k - \mu\,\dfrac{dSS_{res}}{dm}$, stable only if $\mu < 2/(2\sum x^2)$ | sl.26–27 |
| Fit quality | $r^2 = 1 - SS_{res}/SS_{tot}$ | sl.30 |
| Covariance matrix | $\mathbf A$ = deviations (one row per sample), $\;\mathbf S = \frac1N\mathbf A^T\mathbf A$ | sl.44–46 |
| Correlation | $\rho = \dfrac{\text{cov}(x,y)}{\sigma_x\sigma_y}$, $\;\rho^2 = r^2$ for a straight-line fit | sl.48–49 |
| z-score | $z_i = (x_i-\bar x)/\sigma_x$, $\;\rho = \frac1N\sum z_{x,i}z_{y,i}$ | sl.57 |
| Rotate the axes | $\begin{bmatrix}x'\\y'\end{bmatrix} = \begin{bmatrix}\cos\theta & \sin\theta\\ -\sin\theta & \cos\theta\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}$, $\;\mathbf S^R = \mathbf R\mathbf S\mathbf R^T$, trace kept | sl.66–67 |
| Best angle | $\tan 2\theta = \dfrac{2\,\text{cov}(x,y)}{\sigma_x^2-\sigma_y^2}$ = the top eigenvector of S. The variances on the new axes are the eigenvalues | sl.69 |
| Reconstruct | $\mathbf R^{-1} = \mathbf R^T$: $\;x = x'\cos\theta - y'\sin\theta$, $\;y = x'\sin\theta + y'\cos\theta$ | sl.66 (RᵀR = I); B2 does this step in full |

**Watch the R convention.** sl.66's R rotates the **axes** by +θ. A1's $[\cos\theta\; -\sin\theta;\ \sin\theta\;\cos\theta]$ rotates the **points**. The two matrices are transposes of each other.

---

## Part 1: the circuit, fitted by hand (sl.8–20, 30–32)

Data (current x in mA, voltage y in V, sl.8):

| i | 1 | 2 | 3 | 4 | 5 | **Sum** |
|---|---|---|---|---|---|---|
| $x_i$ | 0 | 3 | 5 | 8 | 10 | **26** |
| $y_i$ | 2 | 5 | 6 | 9 | 11 | **33** |
| $x_i^2$ | 0 | 9 | 25 | 64 | 100 | **198** |
| $x_iy_i$ | 0 | 15 | 30 | 72 | 110 | **227** |

### a. Build the design matrix and XᵀX (sl.19–20)

One equation per point, $\mathbf X\mathbf v = \mathbf y$:

$$\underbrace{\begin{bmatrix}1 & 0 \\ 1 & 3 \\ 1 & 5 \\ 1 & 8 \\ 1 & 10\end{bmatrix}}_{\mathbf X\ (5\times2)}\begin{bmatrix}c\\m\end{bmatrix} = \begin{bmatrix}2 \\ 5 \\ 6 \\ 9 \\ 11\end{bmatrix}$$

That's 5 equations in 2 unknowns, and the noise makes them disagree. Multiply both sides by $\mathbf X^T$. Each entry is a row of $\mathbf X^T$ (a column of X) dotted with a column of X:

$$\begin{aligned}
(\mathbf X^T\mathbf X)_{00} &= \text{ones}\cdot\text{ones} = N = 5 \\
(\mathbf X^T\mathbf X)_{01} &= \text{ones}\cdot x = 0 + 3 + 5 + 8 + 10 = 26 \\
(\mathbf X^T\mathbf X)_{11} &= x\cdot x = 0(0) + 3(3) + 5(5) + 8(8) + 10(10) = 198 \\
(\mathbf X^T\mathbf y)_{0} &= \text{ones}\cdot y = 2 + 5 + 6 + 9 + 11 = 33 \\
(\mathbf X^T\mathbf y)_{1} &= x\cdot y = 0(2) + 3(5) + 5(6) + 8(9) + 10(11) = 227
\end{aligned}$$

$$\begin{bmatrix}5 & 26\\ 26 & 198\end{bmatrix}\begin{bmatrix}c\\m\end{bmatrix} = \begin{bmatrix}33\\ 227\end{bmatrix}$$

These are the normal equations (sl.16): the table's sums, in the same places.

### b. Solve the 2×2 (sl.17)

$$\begin{aligned}
\det &= N\textstyle\sum x^2 - (\sum x)^2 = 5(198) - (26)^2 = 990 - 676 = 314 \\
c &= \frac{\sum x^2\sum y - \sum x\sum xy}{\det} = \frac{198(33) - 26(227)}{314} = \frac{6534 - 5902}{314} = \frac{632}{314} = 2.0127 \\
m &= \frac{N\sum xy - \sum x\sum y}{\det} = \frac{5(227) - 26(33)}{314} = \frac{1135 - 858}{314} = \frac{277}{314} = 0.8822
\end{aligned}$$

**Check (sl.15):** $c + m\bar x = \dfrac{632 + 277(5.2)}{314} = \dfrac{632 + 1440.4}{314} = \dfrac{2072.4}{314} = 6.6 = \bar y$ ✓ ($\bar y = 33/5 = 6.6$). Exact fractions are used here so it comes out exact.

**Answer:** $y = 2.01 + 0.88x$ (slide: y = 2.01 + 0.88x) ✓

**Predict (sl.18):** at $x = 6$, $y = \dfrac{632 + 277(6)}{314} = \dfrac{2294}{314} = 7.3057 \approx 7.31$ V.

### c. How good is the fit? r² (sl.11, 30–32)

**SS_tot**, the spread of y about its own mean $\bar y = 6.6$:

$$SS_{tot} = (−4.6)^2 + (−1.6)^2 + (−0.6)^2 + (2.4)^2 + (4.4)^2 = 21.16 + 2.56 + 0.36 + 5.76 + 19.36 = 49.2$$

**SS_res**, the spread of the points about the line:

| i | $x_i$ | $f_i = c + m x_i$ | $y_i$ | $r_i = y_i - f_i$ | $r_i^2$ |
|---|---|---|---|---|---|
| 1 | 0 | 2.0127 + 0.8822(0) = 2.0127 | 2 | −0.0127 | 0.0002 |
| 2 | 3 | 2.0127 + 0.8822(3) = 4.6593 | 5 | 0.3407 | 0.1161 |
| 3 | 5 | 2.0127 + 0.8822(5) = 6.4237 | 6 | −0.4237 | 0.1795 |
| 4 | 8 | 2.0127 + 0.8822(8) = 9.0703 | 9 | −0.0703 | 0.0049 |
| 5 | 10 | 2.0127 + 0.8822(10) = 10.8347 | 11 | 0.1653 | 0.0273 |
| | | | | **Σ** | **0.328** |

$$r^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{0.328}{49.2} = 1 - 0.0067 = 0.9933$$

So 99.3 % of the variation in y is explained by x. (The table uses c and m rounded to 4 dp, so every line adds up as shown. At full precision, SS_res = 0.3280.)

---

## Part 2: the sl.23 exercise (same steps)

Data (sl.23):

| i | 1 | 2 | 3 | 4 | 5 | **Sum** |
|---|---|---|---|---|---|---|
| $x_i$ | −1 | 2 | 4 | 6 | 9 | **20** |
| $y_i$ | −3 | 0 | 3 | 5 | 10 | **15** |
| $x_i^2$ | 1 | 4 | 16 | 36 | 81 | **138** |
| $x_iy_i$ | 3 | 0 | 12 | 30 | 90 | **135** |

### a. Build the design matrix and XᵀX (sl.19–20)

One equation per point, $\mathbf X\mathbf v = \mathbf y$:

$$\underbrace{\begin{bmatrix}1 & −1 \\ 1 & 2 \\ 1 & 4 \\ 1 & 6 \\ 1 & 9\end{bmatrix}}_{\mathbf X\ (5\times2)}\begin{bmatrix}c\\m\end{bmatrix} = \begin{bmatrix}−3 \\ 0 \\ 3 \\ 5 \\ 10\end{bmatrix}$$

That's 5 equations in 2 unknowns, and the noise makes them disagree. Multiply both sides by $\mathbf X^T$. Each entry is a row of $\mathbf X^T$ (a column of X) dotted with a column of X:

$$\begin{aligned}
(\mathbf X^T\mathbf X)_{00} &= \text{ones}\cdot\text{ones} = N = 5 \\
(\mathbf X^T\mathbf X)_{01} &= \text{ones}\cdot x = (−1) + 2 + 4 + 6 + 9 = 20 \\
(\mathbf X^T\mathbf X)_{11} &= x\cdot x = (−1)(−1) + 2(2) + 4(4) + 6(6) + 9(9) = 138 \\
(\mathbf X^T\mathbf y)_{0} &= \text{ones}\cdot y = (−3) + 0 + 3 + 5 + 10 = 15 \\
(\mathbf X^T\mathbf y)_{1} &= x\cdot y = (−1)(−3) + 2(0) + 4(3) + 6(5) + 9(10) = 135
\end{aligned}$$

$$\begin{bmatrix}5 & 20\\ 20 & 138\end{bmatrix}\begin{bmatrix}c\\m\end{bmatrix} = \begin{bmatrix}15\\ 135\end{bmatrix}$$

These are the normal equations (sl.16): the table's sums, in the same places.

### b. Solve the 2×2 (sl.17)

$$\begin{aligned}
\det &= N\textstyle\sum x^2 - (\sum x)^2 = 5(138) - (20)^2 = 690 - 400 = 290 \\
c &= \frac{\sum x^2\sum y - \sum x\sum xy}{\det} = \frac{138(15) - 20(135)}{290} = \frac{2070 - 2700}{290} = \frac{−630}{290} = −2.1724 \\
m &= \frac{N\sum xy - \sum x\sum y}{\det} = \frac{5(135) - 20(15)}{290} = \frac{675 - 300}{290} = \frac{375}{290} = 1.2931
\end{aligned}$$

**Check (sl.15):** $c + m\bar x = \dfrac{−630 + 375(4)}{290} = \dfrac{−630 + 1500}{290} = \dfrac{870}{290} = 3 = \bar y$ ✓ ($\bar y = 15/5 = 3$). Exact fractions are used here so it comes out exact.

**Answer:** $y = −2.17 + 1.29x$ (slide: c ≈ −2.17, m ≈ 1.29) ✓

### c. How good is the fit? r² (sl.11, 30–32)

**SS_tot**, the spread of y about its own mean $\bar y = 3$:

$$SS_{tot} = (−6)^2 + (−3)^2 + (0)^2 + (2)^2 + (7)^2 = 36 + 9 + 0 + 4 + 49 = 98$$

**SS_res**, the spread of the points about the line:

| i | $x_i$ | $f_i = c + m x_i$ | $y_i$ | $r_i = y_i - f_i$ | $r_i^2$ |
|---|---|---|---|---|---|
| 1 | −1 | −2.1724 + 1.2931(−1) = −3.4655 | −3 | 0.4655 | 0.2167 |
| 2 | 2 | −2.1724 + 1.2931(2) = 0.4138 | 0 | −0.4138 | 0.1712 |
| 3 | 4 | −2.1724 + 1.2931(4) = 3 | 3 | 0 | 0 |
| 4 | 6 | −2.1724 + 1.2931(6) = 5.5862 | 5 | −0.5862 | 0.3436 |
| 5 | 9 | −2.1724 + 1.2931(9) = 9.4655 | 10 | 0.5345 | 0.2857 |
| | | | | **Σ** | **1.0172** |

$$r^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{1.0172}{98} = 1 - 0.0104 = 0.9896$$

So 99.0 % of the variation in y is explained by x. (The table uses c and m rounded to 4 dp, so every line adds up as shown. At full precision, SS_res = 1.0172.)

Slide's check value: r² ≈ 0.990 ✓ (0.9896).

---

## Part 3: gradient descent on m, with c fixed at 2.01 (sl.25–27)

### a. The slope formula

From sl.14, with c held fixed:

$$\frac{dSS_{res}}{dm} = -2\sum x_i(y_i - c - m x_i) = -2\left(\textstyle\sum xy - c\sum x - m\sum x^2\right)$$

$$= -2\left(227 - 2.01(26) - 198m\right) = -2\left(174.74 - 198m\right) = 396m - 349.48$$

### b. Three steps with μ = 0.0018 from m₀ = 4

$$\begin{aligned}
\text{slope at } m_0 &= 396(4) - 349.48 = 1584 - 349.48 = 1234.52 \\
m_1 &= 4 - 0.0018(1234.52) = 4 - 2.2221 = 1.7779 \\[4pt]
\text{slope at } m_1 &= 396(1.7779) - 349.48 = 704.0484 - 349.48 = 354.5684 \\
m_2 &= 1.7779 - 0.0018(354.5684) = 1.7779 - 0.6382 = 1.1397 \\[4pt]
\text{slope at } m_2 &= 396(1.1397) - 349.48 = 451.3212 - 349.48 = 101.8412 \\
m_3 &= 1.1397 - 0.0018(101.8412) = 1.1397 - 0.1833 = 0.9564 \\[4pt]
\end{aligned}$$

Slide: 4.00 → 1.78 → 1.14 → 0.96 ✓

### c. The largest safe μ (sl.27)

$$\frac{d^2SS_{res}}{dm^2} = 2\textstyle\sum x^2 = 396$$

Each step multiplies the distance to the bottom by $(1 - 396\mu)$ *(added: this way of saying it)*. With μ = 0.0018 the factor is $1 - 0.7128 = 0.2872$. The method converges only if $|1 - 396\mu| < 1$, so $\mu < 2/396 = 0.0051$ (sl.27: ≈ 0.0051).

---

## Part 4: covariance and correlation of the circuit data (sl.45–49, 57)

### a. Remove the means and build A (sl.45–46)

$\bar x = 26/5 = 5.2$, $\;\bar y = 33/5 = 6.6$

$$\mathbf A = \begin{bmatrix} x_i - \bar x & y_i - \bar y\end{bmatrix} = \begin{bmatrix}−5.2 & −4.6 \\ −2.2 & −1.6 \\ −0.2 & −0.6 \\ 2.8 & 2.4 \\ 4.8 & 4.4\end{bmatrix}\quad(5\times2)$$

### b. AᵀA entry by entry (column · column)

$$\begin{aligned}
(\mathbf A^T\mathbf A)_{00} &= (−5.2)(−5.2) + (−2.2)(−2.2) + (−0.2)(−0.2) + 2.8(2.8) + 4.8(4.8) = 62.8 \\
(\mathbf A^T\mathbf A)_{01} &= (−5.2)(−4.6) + (−2.2)(−1.6) + (−0.2)(−0.6) + 2.8(2.4) + 4.8(4.4) = 55.4 \\
(\mathbf A^T\mathbf A)_{11} &= (−4.6)(−4.6) + (−1.6)(−1.6) + (−0.6)(−0.6) + 2.4(2.4) + 4.4(4.4) = 49.2
\end{aligned}$$

$$\mathbf S = \frac15\begin{bmatrix}62.8 & 55.4\\ 55.4 & 49.2\end{bmatrix} = \begin{bmatrix}12.56 & 11.08\\ 11.08 & 9.84\end{bmatrix}$$

The diagonal holds the variances: σₓ² = 12.56 mA² and σᵧ² = 9.84 V², which matches sl.10. 49.2 is SS_tot from Part 1. The off-diagonal is cov(x, y) = 11.08 mA·V.

### c. Correlation coefficient (sl.48–49)

$$\rho = \frac{\text{cov}}{\sigma_x\sigma_y} = \frac{11.08}{\sqrt{12.56}\sqrt{9.84}} = \frac{11.08}{3.544\times3.1369} = \frac{11.08}{11.1172} = 0.9967$$

$\rho^2 = 0.9933 = r^2$ from Part 1 ✓ (sl.49).

### d. The same ρ from z-scores (sl.57)

| i | $x_i-\bar x$ | $z_{x,i} = (x_i-\bar x)/3.5440$ | $y_i-\bar y$ | $z_{y,i} = (y_i-\bar y)/3.1369$ | $z_{x,i}z_{y,i}$ |
|---|---|---|---|---|---|
| 1 | −5.2 | −1.4673 | −4.6 | −1.4664 | 2.1516 |
| 2 | −2.2 | −0.6208 | −1.6 | −0.5101 | 0.3167 |
| 3 | −0.2 | −0.0564 | −0.6 | −0.1913 | 0.0108 |
| 4 | 2.8 | 0.7901 | 2.4 | 0.7651 | 0.6045 |
| 5 | 4.8 | 1.3544 | 4.4 | 1.4027 | 1.8998 |
| | | | | **Σ** | **4.9834** |

$$\rho = \frac15\sum z_{x,i}z_{y,i} = \frac{4.9834}{5} = 0.9967$$

✓ (matches (c); any 4th-dp difference is rounding in the z columns).

---

## Part 5: practical Q3, what drives PM2.5? (three variables)

A roadside station logs six days. The numbers are exactly as given:

| Day | PM2.5 (µg/m³) | Traffic (×1000) | Wind (m/s) |
|---|---|---|---|
| 1 | 33 | 40 | 3.5 |
| 2 | 41 | 45 | 2 |
| 3 | 37 | 50 | 3.5 |
| 4 | 41 | 50 | 2.5 |
| 5 | 39 | 55 | 4 |
| 6 | 49 | 60 | 2.5 |

Questions (verbatim): 1. Remove the means and form the deviation matrix A. 2. Compute S = (1/N)AᵀA. 3. Convert S to the correlation matrix. 4. Which pairs are correlated, and in which direction? Is the small PM2.5–wind covariance a weak link? 5. How much of the PM2.5 variation do traffic and wind explain together?

### Q1. Means and the deviation matrix A

$$\bar P = \frac{33 + 41 + 37 + 41 + 39 + 49}{6} = \frac{240}{6} = 40,\quad \bar T = \frac{300}{6} = 50,\quad \bar W = \frac{18}{6} = 3$$

$$\mathbf A = \begin{bmatrix} P-\bar P & T-\bar T & W-\bar W\end{bmatrix} = \begin{bmatrix}−7 & −10 & 0.5 \\ 1 & −5 & −1 \\ −3 & 0 & 0.5 \\ 1 & 0 & −0.5 \\ −1 & 5 & 1 \\ 9 & 10 & −0.5\end{bmatrix}\quad(6\times3)$$

### Q2. AᵀA entry by entry, then S

AᵀA is symmetric, so only 6 entries need computing:

$$\begin{aligned}
P\cdot P &= (−7)(−7) + 1(1) + (−3)(−3) + 1(1) + (−1)(−1) + 9(9) = 142 \\
P\cdot T &= (−7)(−10) + 1(−5) + (−3)(0) + 1(0) + (−1)(5) + 9(10) = 150 \\
P\cdot W &= (−7)(0.5) + 1(−1) + (−3)(0.5) + 1(−0.5) + (−1)(1) + 9(−0.5) = −12 \\
T\cdot T &= (−10)(−10) + (−5)(−5) + 0(0) + 0(0) + 5(5) + 10(10) = 250 \\
T\cdot W &= (−10)(0.5) + (−5)(−1) + 0(0.5) + 0(−0.5) + 5(1) + 10(−0.5) = 0 \\
W\cdot W &= 0.5(0.5) + (−1)(−1) + 0.5(0.5) + (−0.5)(−0.5) + 1(1) + (−0.5)(−0.5) = 3
\end{aligned}$$

$$\mathbf A^T\mathbf A = \begin{bmatrix}142 & 150 & −12 \\ 150 & 250 & 0 \\ −12 & 0 & 3\end{bmatrix},\qquad \mathbf S = \frac16\mathbf A^T\mathbf A = \begin{bmatrix}23.6667 & 25 & −2 \\ 25 & 41.6667 & 0 \\ −2 & 0 & 0.5\end{bmatrix}$$

The rows and columns are in the order P, T, W. The diagonal holds the variances (µg²/m⁶, (×1000)², m²/s²). The off-diagonal entries are covariances.

### Q3. Correlation matrix

Divide each entry by the two standard deviations it involves: $\rho_{ab} = S_{ab}/(\sigma_a\sigma_b)$. The diagonal becomes 1.

$$\sigma_P = \sqrt{23.6667} = 4.8648,\quad \sigma_T = \sqrt{41.6667} = 6.455,\quad \sigma_W = \sqrt{0.5} = 0.7071$$

$$\begin{aligned}
\rho_{PT} &= \frac{25}{4.8648\times6.455} = \frac{25}{31.4023} = 0.7961 \\
\rho_{PW} &= \frac{−2}{4.8648\times0.7071} = \frac{−2}{3.4399} = −0.5814 \\
\rho_{TW} &= \frac{0}{6.455\times0.7071} = 0
\end{aligned}$$

$$\mathbf P = \begin{bmatrix}1 & 0.7961 & −0.5814 \\ 0.7961 & 1 & 0 \\ −0.5814 & 0 & 1\end{bmatrix}$$

### Q4. Which pairs, which direction, and is wind a weak link?

- **PM–traffic: ρ = 0.80, strong and positive.** More traffic, more PM.
- **PM–wind: ρ = −0.58, moderate and negative.** More wind, less PM (it disperses the particles).
- **Traffic–wind: ρ = 0.** They're uncorrelated in this data.
- **The small covariance is not a weak link.** cov(P, W) = −2 looks tiny next to cov(P, T) = 25, but only because wind varies by σ = 0.71 m/s while traffic varies by σ = 6.46 (×1000). Covariance carries the units of both variables. ρ divides them out (sl.48), and ρ = −0.58 is a real link.
- Correlation is not causation (sl.51): with six days of data, these are candidates, not proven causes.

### Q5. How much of the PM variation do traffic and wind explain together?

Fit $P = c + aT + bW$. This is sl.22's "add a column to X", with a wind column next to the traffic column, and r² measures how well it fits.

**Shortcut *(added, but it follows from sl.15)*.** The best fit passes through the mean point, so work with the deviations and c drops out:

$$\begin{bmatrix} T\cdot T & T\cdot W\\ T\cdot W & W\cdot W\end{bmatrix}\begin{bmatrix}a\\b\end{bmatrix} = \begin{bmatrix}T\cdot P\\ W\cdot P\end{bmatrix}$$

All these dot products come from AᵀA in Q2:

$$\begin{bmatrix}250 & 0\\ 0 & 3\end{bmatrix}\begin{bmatrix}a\\b\end{bmatrix} = \begin{bmatrix}150\\ −12\end{bmatrix}$$

The matrix is diagonal because traffic and wind are uncorrelated, so each unknown comes out by itself: $a = 150/250 = 0.6$ and $b = −12/3 = −4$.

$$c = \bar P - a\bar T - b\bar W = 40 - 0.6(50) - (−4)(3) = 40 - 30 + 12 = 22$$

$$\boxed{P = 22 + 0.6\,T − 4\,W}$$

**Cross-check with the full 3×3 normal equations (sl.20, XᵀX v = XᵀP):**

$$\mathbf X^T\mathbf X = \begin{bmatrix}6 & 300 & 18 \\ 300 & 15250 & 900 \\ 18 & 900 & 57\end{bmatrix},\quad \mathbf X^T\mathbf P = \begin{bmatrix}240 \\ 12150 \\ 708\end{bmatrix}$$

$$\begin{aligned}
6(22) + 300(0.6) + 18(−4) &= 132 + 180 + (−72) = 240 = 240\ ✓ \\
300(22) + 15250(0.6) + 900(−4) &= 6600 + 9150 + (−3600) = 12150 = 12150\ ✓ \\
18(22) + 900(0.6) + 57(−4) &= 396 + 540 + (−228) = 708 = 708\ ✓
\end{aligned}$$

**r²:**

| Day | $f = c + aT + bW$ | $P$ | $r = P - f$ | $r^2$ |
|---|---|---|---|---|
| 1 | 22 + 0.6(40) − 4(3.5) = 32 | 33 | 1 | 1 |
| 2 | 22 + 0.6(45) − 4(2) = 41 | 41 | 0 | 0 |
| 3 | 22 + 0.6(50) − 4(3.5) = 38 | 37 | −1 | 1 |
| 4 | 22 + 0.6(50) − 4(2.5) = 42 | 41 | −1 | 1 |
| 5 | 22 + 0.6(55) − 4(4) = 39 | 39 | 0 | 0 |
| 6 | 22 + 0.6(60) − 4(2.5) = 48 | 49 | 1 | 1 |
| | | | **Σ** | **4** |

$$r^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{4}{142} = 0.9718$$

**Traffic and wind together explain 97.2 % of the PM2.5 variation.** (SS_tot = P·P = 142 from AᵀA.)

*Added:* because traffic and wind are uncorrelated, their shares just add: $\rho_{PT}^2 + \rho_{PW}^2 = 0.6338 + 0.3380 = 0.9718$. Traffic alone explains 63.4 %, and wind alone explains 33.8 %. That sum only works when the two inputs are uncorrelated.

---

## Part 6: rotating the circuit data (sl.65–69)

Start from S in Part 4: $\mathbf S = \begin{bmatrix}12.56 & 11.08\\ 11.08 & 9.84\end{bmatrix}$, with trace = 12.56 + 9.84 = 22.4.

### a. Rotate by the regression angle θ = tan⁻¹ m (sl.65)

$\theta = \tan^{-1}(0.8822) = 41.42°$, so $\cos\theta = 0.749908$ and $\sin\theta = 0.661543$. (R is kept to 6 dp: at 4 dp it stops being orthogonal enough for the trace check to work.)

$$\mathbf R = \begin{bmatrix}0.749908 & 0.661543\\ −0.661543 & 0.749908\end{bmatrix}$$

**Step 1: RS** (row of R · column of S):

$$\begin{aligned}
(\mathbf{RS})_{00} &= 0.749908(12.56) + 0.661543(11.08) = 16.7487 \\
(\mathbf{RS})_{01} &= 0.749908(11.08) + 0.661543(9.84) = 14.8186 \\
(\mathbf{RS})_{10} &= (−0.661543)(12.56) + 0.749908(11.08) = 0 \\
(\mathbf{RS})_{11} &= (−0.661543)(11.08) + 0.749908(9.84) = 0.0492
\end{aligned}$$

**Step 2: (RS)Rᵀ**. Column j of Rᵀ is row j of R:

$$\begin{aligned}
(\mathbf S^R)_{00} &= 16.7487(0.749908) + 14.8186(0.661543) = 22.3631 \\
(\mathbf S^R)_{01} &= 16.7487(−0.661543) + 14.8186(0.749908) = 0.0326 \\
(\mathbf S^R)_{10} &= 0(0.749908) + 0.0492(0.661543) = 0.0325 \\
(\mathbf S^R)_{11} &= 0(−0.661543) + 0.0492(0.749908) = 0.0369
\end{aligned}$$

$$\mathbf S^R = \begin{bmatrix}22.36 & 0.03\\ 0.03 & 0.04\end{bmatrix}\quad\text{(sl.68: 22.36, 0.03, 0.04 ✓)}$$

- Trace: 22.3631 + 0.0369 = 22.4, the same as before ✓ (sl.67).
- Share on x′: 22.3631/22.4 = 99.8 % (sl.68: 99.8 %).
- The covariance dropped from 11.08 to about 0.033. (The two off-diagonal entries differ in the 4th dp only through rounding; Sᴿ is symmetric.) That's almost zero, but **not exactly**, because the regression angle isn't quite the best angle.
- Side note *(added)*: $(\mathbf{RS})_{10} = 0$ exactly at the regression angle. Row 1 of RS is $-\sin\theta\,\sigma_x^2 + \cos\theta\,\text{cov} = \cos\theta(\text{cov} - m\sigma_x^2)$, and $m = \text{cov}/\sigma_x^2$.

### b. The best angle (sl.69)

$$\tan 2\theta = \frac{2\,\text{cov}}{\sigma_x^2 - \sigma_y^2} = \frac{2(11.08)}{12.56 - 9.84} = \frac{22.16}{2.72} = 8.1471\ \Rightarrow\ 2\theta = 83.00°,\ \theta = 41.50°$$

### c. The same angle as an eigenvector (A3 recipe: det(S − λI) = 0)

$$\det(\mathbf S - \lambda\mathbf I) = (12.56 - \lambda)(9.84 - \lambda) - 11.08^2 = \lambda^2 - 22.4\lambda + (123.5904 - 122.7664) = \lambda^2 - 22.4\lambda + 0.824 = 0$$

$$\lambda = \frac{22.4 \pm \sqrt{22.4^2 - 4(0.824)}}{2} = \frac{22.4 \pm \sqrt{501.76 - 3.296}}{2} = \frac{22.4 \pm 22.3263}{2}\ \Rightarrow\ \lambda_0 = 22.3632,\ \lambda_1 = 0.0369$$

Eigenvector for λ₀, from row 0 of $(\mathbf S - \lambda_0\mathbf I)\mathbf u = 0$:

$$(12.56 - 22.3632)u_0 + 11.08u_1 = 0\ \Rightarrow\ \frac{u_1}{u_0} = \frac{9.8032}{11.08} = 0.8848$$

$$\mathbf u = \frac{1}{\sqrt{1 + 0.8848^2}}\begin{bmatrix}1\\ 0.8848\end{bmatrix} = \begin{bmatrix}0.7489\\ 0.6627\end{bmatrix},\qquad \theta = \tan^{-1}(0.8848) = 41.50°$$

This matches (b) ✓, and the slide gives u = (0.749, 0.663) ✓. The variances on the new axes are the eigenvalues, 22.36 and 0.04 (sl.69). In these axes, Sᴿ is exactly diagonal.

**Why it's 41.50° and not 41.42°:** regression minimises the *vertical* residuals, and the eigenvector minimises the *perpendicular* ones (sl.69). The eigenvector slope is 0.8848, against the regression's m = 0.8822.

---

## Part 7: practical Q2, sending one channel instead of two

A 2-axis accelerometer is tilted, so both channels see the vibration. LoRa only allows a small payload. Six samples, with the means already removed (m/s²):

| Sample | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| x | 3.7 | −7.7 | 12 | −4.3 | 8.3 | −12 |
| y | 3.4 | −6.4 | 9 | −2.6 | 5.6 | −9 |

Questions (verbatim): 1. Compute the covariance matrix S (divide by N = 6) and the correlation coefficient. 2. Find the rotation angle θ that removes the covariance between the new axes. 3. Rotate the data to get x′ and y′. 4. What fraction of the total energy lies on x′? 5. Send x′ only. Reconstruct x and y and find the reconstruction SNR. 6. Compare with dropping y without rotating (θ = 0) and with guessing θ = 45°.

Check the means are 0: Σx = 0, Σy = 0 ✓, so A is just the data.

### Q1. S and ρ

$$\begin{aligned}
x\cdot x &= 3.7(3.7) + (−7.7)(−7.7) + 12(12) + (−4.3)(−4.3) + 8.3(8.3) + (−12)(−12) = 448.36 \\
x\cdot y &= 3.7(3.4) + (−7.7)(−6.4) + 12(9) + (−4.3)(−2.6) + 8.3(5.6) + (−12)(−9) = 335.52 \\
y\cdot y &= 3.4(3.4) + (−6.4)(−6.4) + 9(9) + (−2.6)(−2.6) + 5.6(5.6) + (−9)(−9) = 252.64
\end{aligned}$$

$$\mathbf S = \frac16\begin{bmatrix}448.36 & 335.52\\ 335.52 & 252.64\end{bmatrix} = \begin{bmatrix}74.7267 & 55.92\\ 55.92 & 42.1067\end{bmatrix}$$

$$\rho = \frac{\text{cov}}{\sigma_x\sigma_y} = \frac{335.52}{\sqrt{448.36\times252.64}} = \frac{335.52}{\sqrt{113273.6704}} = \frac{335.52}{336.5615} = 0.9969$$

(The 1/6 factors cancel, so you can use the raw dot products directly; sl.47 makes the same point about N vs N−1.) The two channels are almost perfectly correlated, so one number per sample should be enough.

### Q2. The angle that removes the covariance

$$\tan 2\theta = \frac{2\,\text{cov}}{\sigma_x^2 - \sigma_y^2} = \frac{2(335.52)}{448.36 - 252.64} = \frac{671.04}{195.72} = 3.4286 = \frac{24}{7}$$

The 1/6 factors cancel here too. tan 2θ = 24/7 is a 7-24-25 triangle, so cos 2θ = 7/25. Then use the half-angle formula *(added, an exact-value shortcut)*:

$$\cos\theta = \sqrt{\frac{1 + \cos 2\theta}{2}} = \sqrt{\frac{1 + 7/25}{2}} = \sqrt{\frac{16}{25}} = 0.8,\qquad \sin\theta = \sqrt{1 - 0.64} = 0.6,\qquad \theta = 36.87°$$

$$\mathbf R = \begin{bmatrix}0.8 & 0.6\\ -0.6 & 0.8\end{bmatrix}$$

### Q3. Rotate: x′ = 0.8x + 0.6y, y′ = −0.6x + 0.8y

| Sample | x | y | x′ = 0.8x + 0.6y | y′ = −0.6x + 0.8y |
|---|---|---|---|---|
| 1 | 3.7 | 3.4 | 2.96 + 2.04 = **5** | −2.22 + 2.72 = **0.5** |
| 2 | −7.7 | −6.4 | −6.16 + (−3.84) = **−10** | 4.62 + (−5.12) = **−0.5** |
| 3 | 12 | 9 | 9.6 + 5.4 = **15** | −7.2 + 7.2 = **0** |
| 4 | −4.3 | −2.6 | −3.44 + (−1.56) = **−5** | 2.58 + (−2.08) = **0.5** |
| 5 | 8.3 | 5.6 | 6.64 + 3.36 = **10** | −4.98 + 4.48 = **−0.5** |
| 6 | −12 | −9 | −9.6 + (−5.4) = **−15** | 7.2 + (−7.2) = **0** |

The numbers were designed: x′ = ±5, ±10, ±15 and y′ = ±0.5 or 0. The sensor is tilted by a 3-4-5 angle.

### Q4. Fraction of the energy on x′

$$E_{x'} = \sum x'^2 = 25 + 100 + 225 + 25 + 100 + 225 = 700,\qquad E_{y'} = \sum y'^2 = 0.25 + 0.25 + 0 + 0.25 + 0.25 + 0 = 1$$

$$E_{total} = x\cdot x + y\cdot y = 448.36 + 252.64 = 701 = E_{x'} + E_{y'}\ ✓\ (\text{rotation keeps the total, sl.67})$$

$$\text{fraction on }x' = \frac{700}{701} = 0.9986 = 99.86\,\%$$

Check with S: the eigenvalues of AᵀA are 700 and 1, so Sᴿ = diag(116.6667, 0.1667). The covariance is exactly 0.

### Q5. Send x′ only, reconstruct, SNR

At the receiver y′ is unknown, so set it to 0 and undo the rotation with Rᵀ (sl.66, RᵀR = I):

$$\begin{bmatrix}\hat x\\ \hat y\end{bmatrix} = \mathbf R^T\begin{bmatrix}x'\\ 0\end{bmatrix} = \begin{bmatrix}0.8 & -0.6\\ 0.6 & 0.8\end{bmatrix}\begin{bmatrix}x'\\ 0\end{bmatrix} = \begin{bmatrix}0.8x'\\ 0.6x'\end{bmatrix}$$

| Sample | x′ | x̂ = 0.8x′ | ŷ = 0.6x′ | error² = (x − x̂)² + (y − ŷ)² |
|---|---|---|---|---|
| 1 | 5 | 4 | 3 | (3.7 − 4)² + (3.4 − 3)² = (−0.3)² + (0.4)² = 0.25 |
| 2 | −10 | −8 | −6 | (−7.7 − (−8))² + (−6.4 − (−6))² = (0.3)² + (−0.4)² = 0.25 |
| 3 | 15 | 12 | 9 | (12 − 12)² + (9 − 9)² = (0)² + (0)² = 0 |
| 4 | −5 | −4 | −3 | (−4.3 − (−4))² + (−2.6 − (−3))² = (−0.3)² + (0.4)² = 0.25 |
| 5 | 10 | 8 | 6 | (8.3 − 8)² + (5.6 − 6)² = (0.3)² + (−0.4)² = 0.25 |
| 6 | −15 | −12 | −9 | (−12 − (−12))² + (−9 − (−9))² = (0)² + (0)² = 0 |
| | | | **Σ** | **1** |

The total error energy is 1, which is exactly $E_{y'}$. **What you lose is what you dropped**, because R preserves lengths.

**SNR *(added definition: the slides don't define it)*:** signal energy over error energy, in dB:

$$\text{SNR} = 10\log_{10}\frac{E_{total}}{E_{error}} = 10\log_{10}\frac{701}{1} = 28.46\text{ dB}$$

### Q6. Compare with θ = 0 and θ = 45°

**θ = 0 (send x, drop y):** the error is all of y, so $E_{error} = y\cdot y = 252.64$.

$$\text{fraction kept} = \frac{448.36}{701} = 63.96\,\%,\qquad \text{SNR} = 10\log_{10}\frac{701}{252.64} = 4.43\text{ dB}$$

**θ = 45° (guess):** cos = sin = 1/√2, so $x' = (x + y)/\sqrt2$ and $E_{x'} = \sum (x+y)^2/2 = (x\cdot x + 2\,x\cdot y + y\cdot y)/2$:

$$E_{x'} = \frac{448.36 + 2(335.52) + 252.64}{2} = \frac{1372.04}{2} = 686.02,\qquad E_{error} = 701 - 686.02 = 14.98$$

$$\text{fraction kept} = 97.86\,\%,\qquad \text{SNR} = 10\log_{10}\frac{701}{14.98} = 16.70\text{ dB}$$

| Angle | Energy kept | Error energy | SNR |
|---|---|---|---|
| θ = 0 (no rotation) | 63.96 % | 252.64 | 4.43 dB |
| θ = 45° (guess) | 97.86 % | 14.98 | 16.70 dB |
| **θ = 36.87° (eigenvector)** | **99.86 %** | **1** | **28.46 dB** |

Even the 45° guess beats not rotating, but the eigenvector angle is about 12 dB better than the guess. Same payload, much better signal.

---

## Part 8: one-line recall

| Question | Answer |
|---|---|
| Why square the residuals? | No cancelling, big errors cost more, and SS_res is a smooth bowl, so the derivatives = 0 give *linear* equations (sl.13) |
| Why can't you solve Xv = y exactly? | X is tall (N×2) and the noise makes the equations disagree. Rank is fine (2). Multiply by Xᵀ to get the square XᵀX v = Xᵀy (sl.19–20, A2 tall case) |
| MATLAB | `X\y` uses QR. Avoid `inv(X'*X)`: it squares the condition number (sl.21) |
| "Linear" regression | Linear in the parameters. x², x³ columns are fine (sl.22) |
| μ too big / too small | Too small: slow. Too big: overshoots, then diverges once μ > 2/(2Σx²) (sl.27) |
| Long thin bowl | Zig-zags and is slow. z-score first (sl.28) |
| r² = 0 / 1 | 0: no better than guessing ȳ. 1: every point on the line (sl.31) |
| cov(x, x) | σₓ² (sl.42) |
| Why ρ, not cov? | cov carries units, so "large" means nothing. ρ ∈ [−1, 1] and is unit-free (sl.48) |
| ρ = 0 rules out…? | Only a *linear* link. A circle or parabola can have ρ = 0. One outlier can fake ρ (sl.50) |
| ρ² vs r² | Equal for a straight-line fit (sl.49) |
| N or N−1? | The lecture uses N. MATLAB `var/std/cov` use N−1 (sl.10, 47). ρ is the same either way |
| What does rotation change? | It moves variance between the axes and removes covariance. trace S is unchanged (sl.67) |
| Best θ | tan 2θ = 2cov/(σₓ² − σᵧ²) = the top eigenvector of S. The variances on the new axes = the eigenvalues (sl.69) |
| Regression θ vs eigen θ | Vertical vs perpendicular errors: 41.4° vs 41.5° here (sl.69) |
| Undo a rotation | Rᵀ (RᵀR = I, sl.66). Error energy = energy of what you dropped |
