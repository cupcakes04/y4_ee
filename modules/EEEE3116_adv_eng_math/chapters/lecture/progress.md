# EEEE3116 — progress

To continue in a new session, say: *"adv math, continue from progress.md"* (and name the section: A or B).

**Now on:** Section B, B2 + B3 together (started 2026-11-23). Next step: answer the 8-question B2/B3 probe, then the lab and md get built, weighted by the answers. B1 still has its own to-dos: the lab (panel 4 first, then 3), explain it back, then work `B1_regression.md` by hand. Section A has open items: see *Section A → Next*.

# Section A — matrices (A1–A5)

### The storyline (A2 sl.2–3, 10)
Multiplying is easy and solving is hard. Only diagonal, bidiagonal and triangular matrices are easy to solve.
Every method in Section A is a way of turning a hard **A** into a product of easy ones.

| Lecture | Method | Turns A into |
|---|---|---|
| A2 | Givens / Householder → QR | orthogonal × triangular |
| A2 | LU | lower × upper triangular |
| A3 | Eigendecomposition | X K Xᵀ (diagonal, in eigen axes) |
| A4 | SVD | U Σ Vᵀ (works for any matrix) |
| A5 | Sparse / iterative | no factorisation: guess → residual → adjust |

### Where things live
Work happens in `chapters/lecture/`. `drills/` holds the lecturer's practical notebooks and is kept untouched, as a reference.

Every lecture has two files. Their weights differ by lecture, but both exist:
- **`<lecture>_<topic>_lab.html` (concept page):** go here to *understand* an idea or close a gap. Sliders, predict-first prompts, and derivations behind reveal buttons.
- **`<lecture>_<topic>.md` (worked examples):** go here to *practise the steps* for the exam. Every calculation is written out in full with nothing hidden, and exact answers are given. The practicals' problems are kept as given.

### Status

| Lecture | Topic | Understanding | Worked examples (md) | Concept page (html) |
|---|---|---|---|---|
| A1 | matrix as a system (×, cascade, identity, transpose, rotation) | ✓ 2026-11-22 (quick check; fixed: in AB, B acts first; PA = rows, AP = columns) | — (not needed) | — |
| A2 | easy vs hard, back-substitution | ✓ | — | lab header |
| A2 | Givens → QR | ✓ 2026-11-22 (order (1,0) → (2,0) → (2,1)) | [`A2_qr_lu.md`](A2_qr_lu.md) Parts 1–2, **to do** | [A2 QR lab](https://claude.ai/artifact/DvMjRDPedttK8nKWvHjXCa) (`A2_qr_lab.html`) panels 1–2 |
| A2 | Householder → QR | ✓ 2026-11-22 (reflect onto one axis, then repeat on the N−1 sub-block; u = x − x′. Refined: the sign is about digits cancelling, not exact ÷0) | A2_qr_lu.md Part 3, **to do** | lab panel 3 |
| A2 | LU, cost, solvability / rank, non-square | ✓ 2026-11-22 (LU = two triangular solves; rank 2 → R's last row all 0). Non-square: the three sentences only, 5c steps 2–4 and panel 5 optional | A2_qr_lu.md Parts 4–5, **to do** | lab panels 4–5 |
| A3 | eigen idea, basis, X K Xᵀ, d = Xᵀb | ✓ 2026-11-19 | [`A3_eigen.md`](A3_eigen.md) Parts A–B | [A3 eigen lab](https://claude.ai/artifact/2snCA8AUw4sUWqbbmrHcdb) (`A3_eigen_lab.html`) panels 1–3 |
| A3 | tail: det(A−kI)=0, det = ∏k, A⁻¹, Aᴹ, feedback (sl.30–41) | ✓ 2026-11-19 | A3_eigen.md Part C | lab panel 4 |
| A4 | SVD A = QσPᵀ (same picture, two sets of axes) | mostly ✓ 2026-11-21 (open: P–Q link → lab panel 4, Fact 1) | [`A4_svd.md`](A4_svd.md), done by hand 2026-11-22 | [A4 SVD lab](https://claude.ai/artifact/FhzUauXrbSSswToXwniqws) (`A4_svd_lab.html`) panels 1–4 |
| A5 | sparse, fill-in, CSR, power method, SD / MRA / CG, Jacobi / Gauss-Seidel, preconditioning, domain decomposition | probe 2026-11-22: ✓ fill-in, residual; half ✓ power method (got size, missed shape); ✓ d intuition; ✗ Jacobi/GS, CG, preconditioning, domain decomp → lab | [`A5_iterative.md`](A5_iterative.md) Parts 0–9, **to do** | [A5 iterative lab](https://claude.ai/artifact/8ANFiz2BFrzNQd6iMsey6v) (`A5_iterative_lab.html`) panels 1–6, **to do** |

### What clicked for A3 (2026-11-19)
- Eigenvectors are the input directions where A only scales. k is the scale and depends only on A, not on |x| (because A is linear).
- To solve: Xᵀ takes b into eigen axes (these are projections), divide each part by k, then X brings the result back. So A⁻¹ = X K⁻¹ Xᵀ.
- "Orthogonal" means perpendicular **and** length 1. Only a symmetric A guarantees perpendicular eigen axes.
- det = 0 means some k = 0: one direction gets squashed flat, and there's no unique solution. That's a different case from A = k·I, where every direction is an eigenvector.

- **A3 tail (one sentence):** f(A) = X f(K) Xᵀ, so the axes stay the same and each k becomes f(k): 1/k, kᴹ, k − s, k/(1+βk).
- **A − sI:** subtracting s lowers every stretch by s. When s = kᵢ that axis flattens and det = 0, which is why det(A − kI) = 0 gives the
  eigen**values**. The eigen**vector** is the flattened direction: solve (A − kᵢI)x = 0.

### Slide typos (human errors, so use the corrected form)
| Slide | Slide says | Use |
|---|---|---|
| A4 sl.36 | amount of Pᵢ in x = σᵢ × amount of Qᵢ in b | **÷ σᵢ** |
| A4 sl.38 | (pdftotext 0.80) | middle σ = 0.49 |
| A4 sl.41 | Pᵀ entry "23" | 0.38 |
| A5 sl.10 | R = Qᵀb | **Rx** = Qᵀb |
| A5 sl.11 | double = 16 bytes | 8 bytes (13.4 GB only works with the slide's 16) |
| A5 sl.19 | x₂ = Ax₂ | x₂ = Ax₁ |
| A5 sl.29 (CG) | x₊ = x + α**r**,  p₊ = **r_k** + βp | x₊ = x + α**p**,  p₊ = **r_{k+1}** + βp |

### How we work (see `.agents/learn/modules/EEEE3116.md`)
1. Concept page for the idea: sliders and predict-first prompts.
2. You explain it back in your own words.
3. The AI names the specific gaps, and the concept page gets a fix if a gap needs one.
4. Worked-examples md for the steps, using the slides' and practicals' own numbers.

How much goes into each file depends on the lecture. Abstract lectures (A3, A4) lean on the html. Procedural ones (A2) lean on the md. Every lecture still gets both.

### Next
1. **A3/A4 confirmation check** (parked 2026-11-22): start with the P–Q link (A4 lab panel 4, Fact 1).
2. **A2:** concepts in the A2 QR lab, then work through `A2_qr_lu.md` by hand.
3. **A5:** go through lab panels 2, 4, 5, 6 (the probe gaps) and explain each back, then work `A5_iterative.md` by hand.
4. **A1 done 2026-11-22.** Things worth keeping from it:
   - The matrix nearest x acts first: in QσPᵀx, Pᵀ goes first.
   - PA reorders rows, AP reorders columns.
   - R = [c −s; s c], and RᵀR = I keeps lengths the same.

# Section B — signal representation (B1–B3)

### The storyline (B1 sl.4, 73)
How can data be represented so that its content becomes more obvious? Section B uses one dataset (5 current–voltage points) and looks at it three ways:
fit a line → measure how the variables move together → rotate the axes so one coordinate carries almost everything.
That last step is where Section A comes back: the best rotation is the eigenvectors of the covariance matrix (A3), and B2 and B3 lead into PCA and the eigenfaces coursework.

| Lecture | Topic | Link back to A |
|---|---|---|
| B1 | linear regression, covariance and correlation, axis rotation | XᵀX v = Xᵀy is a tall-system solve (A2 sl.57, QR); best θ = eigenvector of S (A3) |
| B2 | data, vectors, transformations: rows of R (or B) = basis vectors, coefficient Xᵢ = Bᵢ·x, rebuild with Bᵀ, keep M of N for compression | A3's d = Xᵀb (with rows instead of columns), A1's RᵀR = I, A4's truncation |
| B3 | Gram–Schmidt: u₂ = v₂ − αu₁, α = u₁·v₂ / u₁·u₁; QR via Gram–Schmidt (Q = the u's, R = QᵀA) | A2's QR, a third route after Givens and Householder |

B2 and B3 are really one lecture (25 + 22 slides). B2 says *what* an orthonormal basis does for data, and B3 says *how to build one*.

### Status

| Lecture | Topic | Understanding | Worked examples (md) | Concept page (html) |
|---|---|---|---|---|
| B1 | Part 1: regression (normal equations, XᵀX, gradient descent, r²) | probe 2026-11-23: ✓ why square; ½ XᵀX (said rank; it's tall + noisy); ½ μ (missed zig-zag); ½ r² (missed r² = 0) | [`B1_regression.md`](B1_regression.md) Parts 1–3, **to do** | `B1_regression_lab.html` panels 1–2, **to do** |
| B1 | Part 2: covariance, S = (1/N)AᵀA, ρ, z-scores | ✓ cov sign, z-score; ✗ ρ (forgot); missed cov(x,x) = var | Parts 4–5 (5 = practical Q3), **to do** | panel 3, **to do** |
| B1 | Part 3: axis rotation, Sᴿ = RSRᵀ, eigenvector of S | ✗ what rotation changes and why eigenvector → lab | Parts 6–7 (7 = practical Q2), **to do**. 6c now has "the link" (cov′ = v·Su → Su = λu) and "why only one row / only u" | panel 4, **to do** |
| B2 | basis vectors, transform coefficients, rebuild, compression | probe 2026-11-23, **to do** | not built yet | not built yet |
| B3 | Gram–Schmidt (2D and 3D), QR via Gram–Schmidt, practical Q1 (CDMA) | probe 2026-11-23, **to do** | not built yet | not built yet |

### B2/B3 facts checked (sympy, 2026-11-23)
- B2 sl.7: (3, 5) rotated by 45° gives (8/√2, 2/√2) = (5.66, 1.41) ✓. sl.9: (4, 4) gives (5.66, 0) ✓.
- B3 sl.10–12: α = 19/29 = 0.6552 and u₂ = (−2.276, 5.690), with u₁·u₂ = 0 ✓. sl.16–21: α₁₂ = 2, α₁₃ = 4, α₂₃ = 6, R = [1 2 4; 0 3 6; 0 0 5] ✓.
- Practical Q1 (CDMA): c₁·c₂ = 2, so the codes are not orthogonal. With the plain correlator, z₁ = −1/2, which decodes A's +1 as **−1 (wrong)**, and z₂ = −5/2, which decodes B correctly as −1. Gram–Schmidt gives α = 1/2, u₂ = (½, ½, ½, −3/2) and |u₂|² = 3, so R = [2 1; 0 √3] and Qᵀr = (−1, −3√3). Back-substituting gives s = (1, −3), which is **both bits exactly**.
- Rendered slides checked: no typos. One note: B3 sl.17 defines QR for a square m×m A with QQᵀ = I. In the practical, C is 4×2 (tall), so QᵀQ = I but QQᵀ ≠ I (the same economy form as A4).

### B1 facts checked (numpy, 2026-11-23)
All of the slides' numbers check out:
- c = 2.0127, m = 0.8822; at x = 6, y = 7.31
- var y = 9.84, TSS = 49.2, SS_res = 0.328, r² = 0.9933
- S = [12.56 11.08; 11.08 9.84], ρ = 0.9967
- θ = tan⁻¹ m = 41.4°. After rotating, Sᴿ = [22.363 0.033; 0.033 0.037], so 99.8% of the variance is on x′.
- eig(S) = 22.363, 0.037. The eigenvector angle is **41.5°**, not quite the regression's 41.4° (sl.69: vertical vs perpendicular errors).
- sl.23 exercise: c = −2.1724, m = 1.2931, r² = 0.9896.
- sl.26 gradient descent (μ = 0.0018, c fixed at 2.01): m = 4 → 1.778 → 1.140 → 0.956 → 0.904 → 0.889 → 0.884.

The Section B practical (`drills/data_vec_tf/q1–q3.png`) covers B1: **Q2 = rotation**, **Q3 = covariance and multiple regression**. Q1 (Gram–Schmidt) belongs to B3. sl.23's exercise is the other official example.
- Practical Q2: tan 2θ = 24/7, so θ = 36.87° (a 3-4-5 triangle) and x′ = ±5, ±10, ±15. 99.86 % of the energy is on x′. SNR: 28.46 dB, against 4.43 dB at θ = 0 and 16.70 dB at θ = 45°. The SNR definition (total energy / error energy) is added; the slides don't define it.
- Practical Q3: cov(traffic, wind) = 0. ρ(PM, traffic) = 0.796 and ρ(PM, wind) = −0.581 (not weak: wind's σ is just small). PM = 22 + 0.6T − 4W, and r² = 69/71 = 0.9718.

**Slide check (rendered equation slides, 2026-11-23):** no typos found in sl.9–69. sl.27 already derives μ < 2/396. Note that sl.66's R rotates the *axes*; it's the transpose of A1's R, which rotates points.
