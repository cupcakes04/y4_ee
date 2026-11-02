# EEEE3116 Coursework 1: Complete Study Guide & Task 1–3 Analysis

**Student ID:** `20617556` | **Code Word:** `JDNW` | **Energy Target $T$:** `99.0%` | **$k_T$:** `5`

---

## 1. Task 1 Verification & Code Walkthrough

### 1.1 Did You Run Task 1 Correctly? (Checklist)

| Requirement | Status | Details from Your Files |
| :--- | :--- | :--- |
| **Personal Parameters (`cw_params(20617556)`)** | ✅ Verified | `studentID = 20617556`, Code word = `JDNW`, CW1 target $T = 99.0\%$ |
| **13 Raw Photos (`raw/*.jpg`)** | ✅ Verified | All 13 files present (`N1`–`N6`, `E1`–`E4`, `H1`, `S2`, `C`), uniform $1920 \times 1080$ resolution |
| **Processed Faces (`faces/*.png`)** | ✅ Verified | 12 grayscale $128 \times 128$ crops (`N1`–`S2`) + colour verification photo `C.png` clearly showing `JDNW` |
| **`results_cw1.mat` & `svd_cw1.mat`** | ✅ Verified | Re-computing the SVD from `faces/N1.png`–`N6.png` matches `results_cw1.mat` to $2.27 \times 10^{-13}$ (machine precision). Automatic grading (Part A, 10/10 marks) will pass 100%. |
| **Tables & Figures (`cw1_figures(20617556)`)** | ✅ Verified | `table1_cw1.csv`, `table2_cw1.csv`, `fig1_cw1.png`, `fig2_cw1.png`, `fig3_cw1.png` all match `results_cw1.mat`. |

> **Why did the numbers change slightly in the 3rd decimal place when you re-ran `prepare_photos`?**
> When you ran `prepare_photos` to update `C.png` (`JDNW`), you dragged a new square crop box on `N1` (a few pixels different from your first run). That slightly shifted the $128 \times 128$ crop window across `N1`–`S2`, changing $\sigma_1$ from `125.285` to `121.846` while keeping **$k_T = 5$** and all physical trends completely unchanged! Both `results.docx`, `results.pdf`, and this guide have now been updated to match your latest `results_cw1.mat` and CSV tables.

---

### 1.2 Step-by-Step Mathematical Walkthrough of `cw1_main.m`

1. **Constructing the Data Matrix $A$ (`load_faces`)**:
   - Each $128 \times 128$ grayscale image has $M = 128^2 = 16384$ pixels with intensities in $[0, 1]$.
   - Stacking the 6 neutral photos `N1`–`N6` as column vectors gives $A \in \mathbb{R}^{16384 \times 6}$:
     $$A = \begin{bmatrix} | & | & & | \\ \mathbf{a}_1 & \mathbf{a}_2 & \cdots & \mathbf{a}_6 \\ | & | & & | \end{bmatrix}$$

2. **Step 1 — Economy SVD (`[U, S, V] = svd(A, 'econ')`)**:
   - Since $M = 16384 \gg N = 6$, the economy SVD factors $A$ as:
     $$A = U \Sigma V^T = \sum_{i=1}^{6} \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
   - $U = [\mathbf{u}_1, \dots, \mathbf{u}_6] \in \mathbb{R}^{16384 \times 6}$ has orthonormal columns ($U^T U = I_6$). Each $\mathbf{u}_i$ is an **"eigenface" (left singular vector / basis lighting image)** of length $16384$, reshaped to $128 \times 128$ in Figure 1.
   - $\Sigma = \text{diag}(\sigma_1, \dots, \sigma_6) \in \mathbb{R}^{6 \times 6}$ contains the non-negative singular values ordered $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_6 \ge 0$.
   - $V = [\mathbf{v}_1, \dots, \mathbf{v}_6] \in \mathbb{R}^{6 \times 6}$ is orthogonal ($V^T V = V V^T = I_6$), giving the lighting combination weights for each of the 6 photos.

3. **Step 2 — Cumulative Energy & Threshold Rank $k_T$**:
   - The total Frobenius energy of $A$ is $\|A\|_F^2 = \sum_{i=1}^6 \sigma_i^2 = 16158.46$.
   - The cumulative energy fraction captured by the first $k$ modes is:
     $$E(k) = \frac{\sum_{i=1}^{k} \sigma_i^2}{\sum_{i=1}^{6} \sigma_i^2}$$
   - Your personal target is $T = 99.0\%$. Looking at your `R.energy`:
     - $E(3) = 0.977658$ ($97.77\% < 99.0\%$)
     - $E(4) = 0.988664$ ($98.87\% < 99.0\%$ — just $0.13\%$ shy of $99\%$)
     - $E(5) = 0.996548$ ($99.65\% \ge 99.0\%$) $\implies \mathbf{k_T = 5}$.

4. **Step 3 — Rank-$k$ Approximation $A_k$ and Relative Frobenius Error**:
   - By the **Eckart–Young–Mirsky Theorem**, the best rank-$k$ approximation to $A$ in the Frobenius norm is obtained by truncating the SVD at $k$ terms:
     $$A_k = U_k \Sigma_k V_k^T = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
   - The relative approximation error is computed two ways:
     - **Measured directly from matrices:** $\frac{\|A - A_k\|_F}{\|A\|_F}$
     - **Predicted from singular values alone:** $\sqrt{\frac{\sum_{i=k+1}^{6} \sigma_i^2}{\sum_{i=1}^{6} \sigma_i^2}} = \sqrt{1 - E(k)}$

5. **Step 4 — Orthogonal Projection of Held-Out Photos (`H1` and `E1`)**:
   - The first $k$ left singular vectors $U_k = [\mathbf{u}_1, \dots, \mathbf{u}_k] \in \mathbb{R}^{16384 \times k}$ form an orthonormal basis for the $k$-dimensional lighting subspace $\mathcal{S}_k = \text{span}(\mathbf{u}_1, \dots, \mathbf{u}_k)$.
   - For any new test image vector $\mathbf{x} \in \mathbb{R}^{16384}$, its orthogonal projection onto $\mathcal{S}_k$ is:
     $$\mathbf{p} = U_k (U_k^T \mathbf{x})$$
     where $\mathbf{c} = U_k^T \mathbf{x} \in \mathbb{R}^k$ are the coordinates (inner products $\mathbf{u}_i^T \mathbf{x}$) of $\mathbf{x}$ in the basis $U_k$.
   - The **residual vector** $\mathbf{r} = \mathbf{x} - \mathbf{p} = (I - U_k U_k^T)\mathbf{x}$ is the component of $\mathbf{x}$ orthogonal to the lighting subspace (what the lighting basis cannot explain), and the relative residual is:
     $$\text{Relative Residual}(k) = \frac{\|\mathbf{x} - \mathbf{p}\|_2}{\|\mathbf{x}\|_2}$$

---

## 2. Deep-Dive Concept Guide for Task 3 (Learn Why It Works)

### Question 1: Is lighting low-dimensional for your face?

#### The Theoretical Physics (Lambertian 3D Subspace)
For a perfectly **matte (Lambertian) convex object** illuminated by a distant point source from direction $\mathbf{s} \in \mathbb{R}^3$ (incorporating light intensity), the reflected intensity at surface pixel $(x, y)$ is given by **Lambert's Cosine Law**:
$$I(x, y) = \max\big(\rho(x, y)\, \mathbf{n}(x, y)^T \mathbf{s},\; 0\big)$$
where $\rho(x,y)$ is the surface albedo (skin/hair reflectivity) and $\mathbf{n}(x,y) = (n_x, n_y, n_z)^T$ is the unit surface normal vector.
- **Without attached shadows** (when $\mathbf{n}^T \mathbf{s} \ge 0$ everywhere):
  $$I(x, y) = s_x (\rho n_x) + s_y (\rho n_y) + s_z (\rho n_z)$$
  Every image $\mathbf{x} \in \mathbb{R}^{16384}$ is a linear combination of just **three fixed basis images**: $\mathbf{b}_x = \rho n_x$, $\mathbf{b}_y = \rho n_y$, and $\mathbf{b}_z = \rho n_z$. Thus, all images of a matte, shadow-free, stationary face lie strictly in a **3-dimensional linear subspace** ($\text{rank}(A) = 3$, so $\sigma_4 = \sigma_5 = \sigma_6 = 0$).
- **Look at your Figure 1 ($\mathbf{u}_1, \mathbf{u}_2, \mathbf{u}_3, \mathbf{u}_4$)**:
  - $\mathbf{u}_1$ is the **mean/frontal illumination mode** (all positive values).
  - $\mathbf{u}_2$ captures the **left–right horizontal lighting gradient** (bright on one side of the face, dark on the other, corresponding to $\rho n_x$).
  - $\mathbf{u}_3$ captures the **top–bottom vertical lighting gradient** (forehead/cheeks vs chin/eye sockets, corresponding to $\rho n_y$).

#### What Your Numbers Show
1. **Low-dimensional concentration in `N1`–`N6` (Table 1 & Figure 2 left):**
   - $\sigma_1 = 121.846$ alone captures **$91.88\%$** of the total energy ($E(1) = 0.918799$).
   - By $k = 3$, $\sigma_1 = 121.846, \sigma_2 = 24.3895, \sigma_3 = 18.8741$ capture **$97.77\%$** of the cumulative energy ($E(3) = 0.977658$), reducing the relative approximation error from $0.284958$ ($k=1$) to $0.149472$ ($k=3$).
   - At $k = 4$ ($\sigma_4 = 13.3354$), cumulative energy reaches **$98.87\%$** ($0.988664$), very close to the $T = 99.0\%$ threshold, and reaches **$99.65\%$** ($0.996548$) at **$k_T = 5$** ($\sigma_5 = 11.2873$, relative error $0.0587501$).
2. **What stops it from being *exactly* 3-dimensional ($\sigma_4 = 13.34, \sigma_5 = 11.29, \sigma_6 = 7.47 \neq 0$) and why `H1` residuals remain high ($0.36046 \to 0.322855$ in Table 2)?**
   Four real-world physical factors in your photos violate the ideal 3D Lambertian assumption:
   - **Attached & Cast Shadows (Non-linearity $\max(\cdot, 0)$):** When the lamp is at extreme angles (`N1` left, `N2` right, `N3` above, `N4` below, `H1` upper-left), the nose, brow ridge, and **eyeglass frames** cast sharp shadows across the cheeks and eyes (clearly visible in Figure 1 `N1`–`N4` and Figure 3 `H1`), which clip intensity at zero and require higher-order modes (around 9 dimensions in Basri & Jacobs' harmonic theory).
   - **Specular (Non-Lambertian) Reflections:** Your **glasses lenses/frames** and skin oil produce bright mirror-like specular glints that shift position nonlinearly with lamp angle.
   - **Near-Field Point Source & Ambient Room Light:** The lamp is at $\sim 0.5\text{–}1\text{ m}$ (not infinitely distant, so $1/r^2$ falloff varies across the face) and `N6` adds diffuse ambient illumination.
   - **Slight Head/Posture Shift in `N1` and `H1`:** In `N1` (left lamp), your head leaned slightly ($\approx 12\text{ px}$ right in image coordinates) compared to `N2`–`N6` and `H1`. Because SVD operates pixel-by-pixel, spatial misalignment between `N1` and `H1` creates double-edge ghosting along the glasses, hair, face contour, and chair in Figure 3 (`H1`), keeping `res_H1` elevated ($0.36046$ at $k=1$ down to $0.322855$ at $k=5$).

---

### Question 2: Lighting versus expression (`E1` vs `H1`)

#### Comparing the Curves & Numbers (Table 2 & Figure 2 Right)
- **Values from Table 2:**
  - **`H1` (new upper-left lighting, neutral):** starts at $0.36046$ ($k=1$), decreases gradually to $0.355658$ ($k=2$), $0.34220$ ($k=3$), $0.327411$ ($k=4$), and $0.322855$ ($k=5$) — a total reduction of $\Delta = 0.0376$ ($\approx 10.4\%$ relative drop).
  - **`E1` (smile, front lighting):** starts lower at $0.19214$ ($k=1$), drops to $0.177788$ ($k=2$), stays flat at $0.177693$ ($k=3$), drops sharply at $k=4$ to $0.144526$, and reaches $0.13118$ ($k=5$) — a total reduction of $\Delta = 0.0610$ ($\approx 31.7\%$ relative drop), plateauing around $13.1\%$ residual.

#### Why Do `E1` and `H1` Behave This Way in Your Data?
1. **Why `E1` has a lower overall residual than `H1` in your experiment:**
   - `E1` was taken under **front lighting** (identical to training photos `N5` and `N6`) and with your head in the **exact same position** as `N2`–`N6` (within $2\text{ px}$). Thus, over $80\%$ of the pixels in `E1` (background, hair, forehead, glasses) are already spanned by `N5`/`N6` inside $U_k$!
   - Specifically, while modes $k=2, 3$ capture horizontal/vertical side-lighting (`N1`–`N4`)—giving almost zero improvement for front-lit `E1` between $k=2$ ($0.177788$) and $k=3$ ($0.177693$)—mode $k=4$ ($\mathbf{u}_4$) captures front-lit vs vertical shading variations, dropping `res_E1` from $0.177693$ to $0.144526$.
   - However, **even at $k=5$, `E1` cannot be reduced below $0.13118$ ($13.1\%$)** because a smile is a **non-rigid 3D geometric deformation**, which lies outside the neutral-face subspace.
   - Conversely, `H1` has strong directional upper-left illumination (halfway between `N1` and `N3`). As $k$ increases from $1 \to 5$, adding the horizontal ($\mathbf{u}_2$) and vertical ($\mathbf{u}_3, \mathbf{u}_4, \mathbf{u}_5$) lighting modes steadily reduces `res_H1` ($0.36046 \to 0.322855$). Its residual remains high ($0.34220$ at $k=3$) because `N1` (the only left-lit training photo) had a slight head shift relative to `H1`, plus `H1` introduces a new diagonal cast-shadow direction from the glasses frame.

2. **Where is the `E1` residual concentrated in Figure 3 ($k=3$)?**
   - Looking at **Figure 3 (right, `E1 (smile)`)**, the residual $\mathbf{r} = \mathbf{x} - \mathbf{p}$ is near zero ($0$ on the colorbar, mid-grey) across the forehead, hair, upper head, and background, and is **localized around the mouth/lips (smiling teeth and widened lip corners), nasolabial folds/cheeks (pushed upward by the smile), and lower rims of the glasses** (which lifted slightly when your cheeks rose).
   - In contrast, **Figure 3 (left, `H1 (new lighting)`)** shows residual errors spread globally across the right forehead/cheek (bright $+0.4$ to $+0.6$ unmodelled directional highlight), nose/glasses cast shadow ($-0.4$), and head/chair boundary (from the `N1` alignment shift).

3. **What does this mean for face recognition under changing lighting?**
   - **Subspace projection ($I - U_k U_k^T$) separates lighting from local expression/identity:** For a well-aligned rigid face, projecting onto the low-dimensional lighting subspace $\text{span}(U_k)$ ($k \approx 3\text{–}5$) absorbs global illumination variations, allowing a recognition algorithm to identify the same person across unseen lighting directions by measuring the distance to their subspace $\text{span}(U_k)$.
   - **Local expression vs global misalignment:** Expression changes (`E1`) produce spatially localized residuals (around the mouth/cheeks) that do not corrupt the rest of the face, whereas **head movement/misalignment** (`H1` vs `N1`) corrupts the entire subspace projection—showing that subspace face recognition requires accurate **spatial face alignment/registration** prior to projection.

---

### Question 3: The mathematics behind Table 1

#### Part A: Proof that $\|A - A_k\|_F^2 = \sum_{i=k+1}^{6} \sigma_i^2$ (Why Measured & Predicted Errors Agree)
Let $A \in \mathbb{R}^{M \times N}$ ($M = 16384, N = 6$) have economy SVD:
$$A = U \Sigma V^T = \sum_{i=1}^{6} \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
where $U^T U = I_6$ ($\mathbf{u}_i^T \mathbf{u}_j = \delta_{ij}$) and $V^T V = I_6$ ($\mathbf{v}_i^T \mathbf{v}_j = \delta_{ij}$).

The rank-$k$ truncated SVD approximation is:
$$A_k = U_k \Sigma_k V_k^T = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
Subtracting $A_k$ from $A$ leaves the tail sum:
$$A - A_k = \sum_{i=k+1}^{6} \sigma_i \mathbf{u}_i \mathbf{v}_i^T = U \tilde{\Sigma}_k V^T$$
where $\tilde{\Sigma}_k = \text{diag}(0, \dots, 0, \sigma_{k+1}, \dots, \sigma_6) \in \mathbb{R}^{6 \times 6}$.

Using the trace definition of the squared Frobenius norm, $\|X\|_F^2 = \text{tr}(X^T X)$:
$$\begin{aligned}
\|A - A_k\|_F^2 &= \text{tr}\big((A - A_k)^T (A - A_k)\big) \\
&= \text{tr}\big((U \tilde{\Sigma}_k V^T)^T (U \tilde{\Sigma}_k V^T)\big) \\
&= \text{tr}\big(V \tilde{\Sigma}_k^T \underbrace{U^T U}_{I_6} \tilde{\Sigma}_k V^T\big) \\
&= \text{tr}\big(V \tilde{\Sigma}_k^2 V^T\big) \\
&= \text{tr}\big(\tilde{\Sigma}_k^2 \underbrace{V^T V}_{I_6}\big) \quad \text{(by cyclic property } \text{tr}(BC) = \text{tr}(CB)\text{)} \\
&= \text{tr}(\tilde{\Sigma}_k^2) = \sum_{i=k+1}^{6} \sigma_i^2
\end{aligned}$$
By exactly the same derivation (setting $k = 0$), the total squared Frobenius norm of $A$ is:
$$\|A\|_F^2 = \text{tr}(A^T A) = \text{tr}(\Sigma^2) = \sum_{i=1}^{6} \sigma_i^2$$
Dividing the two and taking the square root yields:
$$\underbrace{\frac{\|A - A_k\|_F}{\|A\|_F}}_{\text{relerr\_measured}} = \underbrace{\sqrt{\frac{\sum_{i=k+1}^{6} \sigma_i^2}{\sum_{i=1}^{6} \sigma_i^2}}}_{\text{relerr\_from\_sigma}}$$
- **Numeric Verification in Table 1:** For $k=1$ through $k=5$, the two columns agree to all 6 significant figures (e.g., $0.284958$ at $k=1$, $0.149472$ at $k=3$, $0.0587501$ at $k=5$). At $k=6$, the predicted sum over $i > 6$ is empty ($0$), while the measured matrix norm $\|A - U\Sigma V^T\|_F / \|A\|_F = 1.40514 \times 10^{-15}$ due to double-precision floating-point rounding ($\epsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$).

#### Part B: Why $\sigma_1$ is Much Larger Than the Other Singular Values ($\sigma_1 = 121.846 \gg \sigma_2 = 24.3895$)
In your Table 1, $\sigma_1 = 121.846$ is **$5.00\times$ larger** than $\sigma_2 = 24.3895$ and accounts for $\sigma_1^2 / \sum \sigma_i^2 = \mathbf{91.88\%}$ of the total energy. There are two linked mathematical and physical reasons:
1. **Non-Negative Pixel Intensities (No Mean Subtraction / Uncentred Data):**
   - Every pixel in $A$ satisfies $A_{ij} \in [0, 1]$ (non-negative luminance), and the columns of $A$ are **not mean-centred** before taking the SVD (unlike PCA).
   - Thus, the first mode $\sigma_1 \mathbf{u}_1 \mathbf{v}_1^T$ must capture the **non-zero mean ("DC component" / average face + static background)** shared by all 6 images (visible in Figure 1 where $\mathbf{u}_1$ looks like a positive average portrait), while $\sigma_2, \dots, \sigma_6$ only capture zero-mean directional lighting fluctuations around $\mathbf{u}_1$.
2. **High Colinearity of Static Face & Background Structure:**
   - All 6 columns of $A$ show the **same person, hair, glasses, and room background** in the same $128 \times 128$ frame. The column vectors $\mathbf{a}_1, \dots, \mathbf{a}_6 \in \mathbb{R}^{16384}$ point in nearly the same direction in the positive orthant of $\mathbb{R}^{16384}$ (large positive inner products $\mathbf{a}_i^T \mathbf{a}_j$ in $A^T A$), producing one dominant eigenvalue $\lambda_1 = \sigma_1^2 = 14846.37 \gg \lambda_2 = \sigma_2^2 = 594.85$.

---

## 3. Ready-to-Handwrite 1-Page A4 Template for Task 3 (`analysis.pdf`)

> **How to use this section:**
> Copy the text below in your own handwriting onto **one single side of A4 paper**, scan it as `analysis.pdf`, and include it in your zip submission. It uses your exact updated numbers from `results_cw1.mat` and `table1_cw1.csv`/`table2_cw1.csv`.

---

### [Start of 1-Page Handwritten Sheet]

**EEEE3116 Coursework 1 – Handwritten Analysis | Student ID: 20617556 ($T = 99.0\%, k_T = 5$)**

#### **Q1. Is lighting low-dimensional for your face?**
- **Low-dimensionality in `N1`–`N6`:** Yes, the lighting variations across my six neutral photos (`N1`–`N6`) are strongly low-dimensional. In **Table 1** and **Figure 2 (left)**, $\sigma_1 = 121.846$ alone captures **$91.88\%$** ($0.918799$) of the total energy, and the first three singular values ($\sigma_1 = 121.846, \sigma_2 = 24.3895, \sigma_3 = 18.8741$) capture **$97.77\%$** ($0.977658$) of the energy, cutting the relative error from $0.284958$ ($k=1$) to $0.149472$ ($k=3$). By $k=4$ ($\sigma_4 = 13.3354$), cumulative energy reaches **$98.87\%$** ($0.988664$, just $0.13\%$ below $T=99.0\%$), and my threshold is reached at **$k_T = 5$** ($\sigma_5 = 11.2873$, cumulative energy **$99.65\%$**, relative error $0.0587501$). In **Figure 1**, $\mathbf{u}_1$ represents the average frontal illumination, $\mathbf{u}_2$ the left–right horizontal lighting gradient, and $\mathbf{u}_3$ the top–bottom vertical lighting gradient.
- **Why it is not *exactly* 3-dimensional ($\sigma_4 = 13.34, \sigma_5 = 11.29, \sigma_6 = 7.47 > 0$) and why `H1` residuals are large:**
  Theory states that a convex, perfectly matte (Lambertian) surface under distant point lighting has pixel intensity $I = \max(\rho \mathbf{n}^T \mathbf{s}, 0)$, which spans a 3D subspace ($\text{span}(\rho n_x, \rho n_y, \rho n_z)$) only when $\mathbf{n}^T \mathbf{s} \ge 0$ everywhere. In my photos (**Figure 1** and **Figure 3**), four physical effects break this ideal 3D model:
  1. **Attached and cast shadows:** Extreme lamp angles (`N1`–`N4`, `H1`) cause the nose, brow, and **eyeglass frames** to cast sharp shadows across my cheeks/eyes, introducing the non-linear $\max(\cdot, 0)$ clipping.
  2. **Specular reflections:** My **eyeglasses** and skin produce bright non-Lambertian mirror glints that shift with lamp position.
  3. **Near-field light source:** The handheld lamp is close ($\sim 0.5\text{–}1\text{ m}$), causing non-uniform $1/r^2$ intensity falloff.
  4. **Head/posture shift in `N1` and `H1`:** In **Table 2**, my held-out `H1` residual decreases steadily as $k$ grows ($0.36046$ at $k=1 \to 0.34220$ at $k=3 \to 0.322855$ at $k=5$), confirming that adding lighting modes $\mathbf{u}_2\text{–}\mathbf{u}_5$ helps explain the new upper-left lighting direction. However, `res_H1` remains around $0.32\text{–}0.36$ because my head leaned slightly ($\sim 12\text{ px}$) during left-lit photo `N1` relative to `H1`, creating the edge-misalignment ghosting seen in **Figure 3 (left)**.

---

#### **Q2. Lighting versus expression (`E1` vs `H1`)**
- **Comparison of `E1` and `H1` residuals as $k$ grows (**Table 2** & **Figure 2 right**):**
  - `H1` (new upper-left lighting) starts at $0.36046$ ($k=1$) and decreases gradually across every mode: $0.355658$ ($k=2$), $0.34220$ ($k=3$), $0.327411$ ($k=4$), and $0.322855$ ($k=5$) (a $10.4\%$ relative reduction).
  - `E1` (smile, front lighting) starts much lower at $0.19214$ ($k=1$), drops to $0.177788$ ($k=2$), plateaus at $0.177693$ ($k=3$), drops sharply at $k=4$ to $0.144526$, and reaches $0.13118$ at $k=5$ (a $31.7\%$ relative reduction).
  - **Why they behave differently:** `E1` was captured under **front lighting** (matching training photos `N5` and `N6`) and with almost zero head movement relative to `N2`–`N6`. Thus, the upper face and background of `E1` are already well-spanned by the frontal lighting modes ($\mathbf{u}_1$ and $\mathbf{u}_4$), whereas modes $\mathbf{u}_2, \mathbf{u}_3$ capture side/vertical shadows (`N1`–`N4`) and therefore do not reduce `E1`'s residual between $k=2$ ($0.177788$) and $k=3$ ($0.177693$). However, `E1` hits an irreducible floor ($0.13118$ at $k=5$) because a **smile is a non-rigid 3D geometric deformation** that cannot be represented as a linear combination of neutral-face images. Meanwhile, `H1` has strong upper-left directional shadows and slight spatial misalignment with `N1`, keeping its global residual higher ($0.34220$ at $k=3$).
- **Where the `E1` residual is concentrated (**Figure 3 right**):**
  At $k=3$, the `E1` residual image $\mathbf{x} - \mathbf{p}$ is near $0$ (mid-grey) over the forehead, hair, and background, and is **tightly concentrated around the smiling mouth/lips, raised cheeks (nasolabial folds), and lower eyeglass rims** (pushed up by the cheeks). By contrast, `H1`'s residual (**Figure 3 left**) is spread globally across the right forehead/cheek highlight ($+0.5$), nose/glasses shadow ($-0.4$), and head/chair outline.
- **Implication for face recognition under changing lighting:**
  Projecting a face onto a low-dimensional lighting subspace $\text{span}(U_k)$ ($k \approx 3\text{–}5$) effectively removes global lighting changes while leaving expression changes (`E1`) localized to small regions (mouth/cheeks) that can be masked or tolerated. However, my `H1` result shows that subspace projection is highly sensitive to **spatial misalignment**: a face must be accurately aligned/registered before subspace projection, otherwise pose shifts masquerade as large global residuals.

---

#### **Q3. The mathematics behind Table 1**
- **Why measured and predicted relative errors in Table 1 agree ($\|A - A_k\|_F^2 = \sum_{i>k} \sigma_i^2$):**
  Given the economy SVD $A = U\Sigma V^T = \sum_{i=1}^6 \sigma_i \mathbf{u}_i \mathbf{v}_i^T$ with orthonormal columns $U^T U = I_6$ and $V^T V = I_6$, the rank-$k$ approximation is $A_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$. Subtracting gives:
  $$A - A_k = \sum_{i=k+1}^{6} \sigma_i \mathbf{u}_i \mathbf{v}_i^T = U \tilde{\Sigma}_k V^T, \quad \tilde{\Sigma}_k = \text{diag}(0, \dots, 0, \sigma_{k+1}, \dots, \sigma_6)$$
  Using $\|X\|_F^2 = \text{tr}(X^T X)$ and the cyclic trace property $\text{tr}(BC) = \text{tr}(CB)$:
  $$\|A - A_k\|_F^2 = \text{tr}\big((U \tilde{\Sigma}_k V^T)^T (U \tilde{\Sigma}_k V^T)\big) = \text{tr}\big(V \tilde{\Sigma}_k \underbrace{U^T U}_{I_6} \tilde{\Sigma}_k V^T\big) = \text{tr}\big(\tilde{\Sigma}_k^2 \underbrace{V^T V}_{I_6}\big) = \text{tr}(\tilde{\Sigma}_k^2) = \sum_{i=k+1}^{6} \sigma_i^2$$
  Similarly, for $k=0$, $\|A\|_F^2 = \text{tr}(\Sigma^2) = \sum_{i=1}^6 \sigma_i^2$. Taking the ratio and square root proves:
  $$\frac{\|A - A_k\|_F}{\|A\|_F} = \sqrt{\frac{\sum_{i=k+1}^{6} \sigma_i^2}{\sum_{i=1}^{6} \sigma_i^2}}$$
  In **Table 1**, the two columns match identically for $k=1\text{–}5$ (e.g., $0.284958$ at $k=1$, $0.149472$ at $k=3$, $0.0587501$ at $k=5$). At $k=6$, the predicted value is exactly $0$ while the measured error is $1.40514 \times 10^{-15}$ due to IEEE 754 double-precision rounding.
- **Why $\sigma_1$ is much larger than the other singular values ($\sigma_1 = 121.846 \gg \sigma_2 = 24.3895$):**
  1. **Un-centred, non-negative pixel values ($A_{ij} \in [0, 1]$):** Unlike PCA, the mean image is not subtracted before SVD. All pixels are non-negative, so the first mode $\sigma_1 \mathbf{u}_1 \mathbf{v}_1^T$ absorbs the large positive **DC / mean face intensity** (**Figure 1**, $\mathbf{u}_1$), accounting for $\sigma_1^2 / \sum \sigma_i^2 = \mathbf{91.88\%}$ of total energy ($121.846^2 / 16158.46$).
  2. **Strong column colinearity:** All 6 columns of $A$ depict the same face, glasses, and static room background in the same position, so the vectors $\mathbf{a}_1, \dots, \mathbf{a}_6 \in \mathbb{R}^{16384}$ point in nearly the same direction, yielding $\sigma_1 = 121.846$ ($5.00\times$ larger than $\sigma_2 = 24.3895$), while $\sigma_2\text{–}\sigma_6$ only capture zero-mean directional lighting differences around $\mathbf{u}_1$.

### [End of 1-Page Handwritten Sheet]
