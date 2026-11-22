# EEEE3116 Section A — progress

To continue in a new session, say: *"adv math, continue Section A from section_A_progress.md"*.

## The storyline (A2 sl.2–3, 10)
Multiplying is easy and solving is hard. Only diagonal, bidiagonal and triangular matrices are easy to solve.
Every method in Section A is a way of turning a hard **A** into a product of easy ones.

| Lecture | Method | Turns A into |
|---|---|---|
| A2 | Givens / Householder → QR | orthogonal × triangular |
| A2 | LU | lower × upper triangular |
| A3 | Eigendecomposition | X K Xᵀ (diagonal, in eigen axes) |
| A4 | SVD | U Σ Vᵀ (works for any matrix) |
| A5 | Sparse / iterative | no factorisation: guess → residual → adjust |

## Where things live
Work happens in `chapters/lecture/`. `drills/` holds the lecturer's practical notebooks and is kept untouched, as a reference.

Every lecture has two files. Their weights differ by lecture, but both exist:
- **`<lecture>_<topic>_lab.html` (concept page):** go here to *understand* an idea or close a gap. Sliders, predict-first prompts, and derivations behind reveal buttons.
- **`<lecture>_<topic>.md` (worked examples):** go here to *practise the steps* for the exam. Every calculation is written out in full with nothing hidden, and exact answers are given. The practicals' problems are kept as given.

## Status

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

## What clicked for A3 (2026-11-19)
- Eigenvectors are the input directions where A only scales. k is the scale and depends only on A, not on |x| (because A is linear).
- To solve: Xᵀ takes b into eigen axes (these are projections), divide each part by k, then X brings the result back. So A⁻¹ = X K⁻¹ Xᵀ.
- "Orthogonal" means perpendicular **and** length 1. Only a symmetric A guarantees perpendicular eigen axes.
- det = 0 means some k = 0: one direction gets squashed flat, and there's no unique solution. That's a different case from A = k·I, where every direction is an eigenvector.

- **A3 tail (one sentence):** f(A) = X f(K) Xᵀ, so the axes stay the same and each k becomes f(k): 1/k, kᴹ, k − s, k/(1+βk).
- **A − sI:** subtracting s lowers every stretch by s. When s = kᵢ that axis flattens and det = 0, which is why det(A − kI) = 0 gives the
  eigen**values**. The eigen**vector** is the flattened direction: solve (A − kᵢI)x = 0.

## Slide typos (human errors, so use the corrected form)
| Slide | Slide says | Use |
|---|---|---|
| A4 sl.36 | amount of Pᵢ in x = σᵢ × amount of Qᵢ in b | **÷ σᵢ** |
| A4 sl.38 | (pdftotext 0.80) | middle σ = 0.49 |
| A4 sl.41 | Pᵀ entry "23" | 0.38 |
| A5 sl.10 | R = Qᵀb | **Rx** = Qᵀb |
| A5 sl.11 | double = 16 bytes | 8 bytes (13.4 GB only works with the slide's 16) |
| A5 sl.19 | x₂ = Ax₂ | x₂ = Ax₁ |
| A5 sl.29 (CG) | x₊ = x + α**r**,  p₊ = **r_k** + βp | x₊ = x + α**p**,  p₊ = **r_{k+1}** + βp |

## How we work (see `.agents/learn/modules/EEEE3116.md`)
1. Concept page for the idea: sliders and predict-first prompts.
2. You explain it back in your own words.
3. The AI names the specific gaps, and the concept page gets a fix if a gap needs one.
4. Worked-examples md for the steps, using the slides' and practicals' own numbers.

How much goes into each file depends on the lecture. Abstract lectures (A3, A4) lean on the html. Procedural ones (A2) lean on the md. Every lecture still gets both.

## Next
1. **A3/A4 confirmation check** (parked 2026-11-22): start with the P–Q link (A4 lab panel 4, Fact 1).
2. **A2:** concepts in the A2 QR lab, then work through `A2_qr_lu.md` by hand.
3. **A5:** go through lab panels 2, 4, 5, 6 (the probe gaps) and explain each back, then work `A5_iterative.md` by hand.
4. **A1 done 2026-11-22.** Things worth keeping from it:
   - The matrix nearest x acts first: in QσPᵀx, Pᵀ goes first.
   - PA reorders rows, AP reorders columns.
   - R = [c −s; s c], and RᵀR = I keeps lengths the same.
