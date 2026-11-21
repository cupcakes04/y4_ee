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

## Status

| Lecture | Topic | Understanding | Hand-calc drill | Material |
|---|---|---|---|---|
| A1 | matrix as a system (×, cascade, identity, transpose, rotation) | not covered | — | — |
| A2 | easy vs hard, back-substitution | ✓ | — | — |
| A2 | Givens → QR | not yet (**next candidate**) | `drills/givens_rotation` (old, unverified) | — |
| A2 | Householder → QR | not yet | `drills/householder_reflection` (old, unverified) | — |
| A2 | LU, cost, solvability / rank, non-square | not yet | — | — |
| A3 | eigen idea, basis, X K Xᵀ, d = Xᵀb | ✓ 2026-11-19 | [`drills/eigen/eigen.md`](../../drills/eigen/eigen.md) ✓ rewritten, verified | [A3 eigen lab](https://claude.ai/artifact/2snCA8AUw4sUWqbbmrHcdb) (`A3_eigen_lab.html`) |
| A3 | tail: det(A−kI)=0, det = ∏k, A⁻¹, Aᴹ, feedback (sl.30–41) | ✓ 2026-11-19 (A − sI understood; the rest is one sentence) | eigen.md Part C | lab panel 4 |
| A4 | SVD A = QσPᵀ (same picture, two sets of axes) | mostly ✓ 2026-11-21 (open: P–Q link, answered in drill A1) | [`drills/svd/svd.md`](../../drills/svd/svd.md) ✓ written, verified | [A4 SVD lab](https://claude.ai/artifact/FhzUauXrbSSswToXwniqws) (`A4_svd_lab.html`) |
| A5 | sparse, Jacobi / Gauss-Seidel | not yet | `drills/iterative_revolution` (old, unverified) | — |

## What clicked for A3 (2026-11-19)
- Eigenvectors are the input directions where A only scales. k is the scale and depends only on A, not on |x| (because A is linear).
- To solve: Xᵀ takes b into eigen axes (these are projections), divide each part by k, then X brings the result back. So A⁻¹ = X K⁻¹ Xᵀ.
- "Orthogonal" means perpendicular **and** length 1. Only a symmetric A guarantees perpendicular eigen axes.
- det = 0 means some k = 0: one direction gets squashed flat, and there's no unique solution. That's a different case from A = k·I, where every direction is an eigenvector.

- **A3 tail (one sentence):** f(A) = X f(K) Xᵀ, so the axes stay the same and each k becomes f(k): 1/k, kᴹ, k − s, k/(1+βk).
- **A − sI:** subtracting s lowers every stretch by s. When s = kᵢ that axis flattens and det = 0, which is why det(A − kI) = 0 gives the
  eigen**values**. The eigen**vector** is the flattened direction: solve (A − kᵢI)x = 0.

## How we work (see `.agents/learn/modules/EEEE3116.md`)
1. A slider widget for the idea.
2. You explain it back in your own words.
3. The AI names the specific gaps.
4. A tiny numeric check on the slide's own example.
5. A hand-calc drill with full steps shown.

## Next
1. **A3 is done.** Practise `drills/eigen/eigen.md` (Parts A–C) by hand.
2. A2 Givens/QR: a widget, then rewrite its drill, keeping the practical's problem.
3. Then Householder, A4 SVD, A5 iterative. A1 is light; skim it last.
