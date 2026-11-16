# X1 — Conditional Track: MPPI Sampler Variants (C3)

> **Status:** **Conditional / dormant.** Not on the critical path. Activated **only** if the C2 evaluation shows the specific failure described in §2. See decision **D10** in [`../proposals/decisions.md`](../proposals/decisions.md).
> **Date opened:** 2026-11-16

---

## 1. Why this track exists

`nav2_mppi_controller` [L11] is a production-hardened implementation of *standard* information-theoretic MPPI [L4]: unimodal Gaussian perturbations around a warm-started nominal sequence, softmax importance weighting, Savitzky–Golay smoothing. Since 2022 the literature has produced several variants that change **how rollouts are sampled or combined** rather than **how they are scored**:

| Key | Variant | What it changes | Fit for this project |
|---|---|---|---|
| L19 | **SVG-MPPI** (Honda et al., 2023/24) | Stein Variational Gradient Descent on a small guide set estimates the dominant mode of a multimodal optimal distribution; MPPI then samples around it. | Strongest fix for mode averaging. Most code; SVGD kernel is $O(M^2)$ per iteration, so only viable on a small guide set (not all $M=1000$–$2000$ rollouts) within the CPU budget. |
| L20 | **log-MPPI** (Mohamed, Yin, Liu, 2022) | Samples from a normal log-normal (NLN) mixture instead of a Gaussian — heavier tails, broader exploration in clutter. | Smallest diff: only the noise generator changes. Weakest guarantee against mode averaging. |
| L21 | **Biased-MPPI** (Trevisan & Alonso-Mora, RA-L 2024) | Derives MPPI for arbitrary sampling distributions; fuses samples from ancillary controllers (e.g. braking, fixed left/right pass) into the rollout set. | Cheap, very explainable: inject a handful of "pass-left / pass-right / brake" sequences. Directly addresses local minima. |

These are **orthogonal** to the project contribution: the `DynamicObstaclesCriticPlugin` reshapes the *cost landscape*; these reshape the *sampling distribution*. That orthogonality is exactly why they are not added by default — swapping both at once confounds the C0→C1→C2 causal story.

---

## 2. Activation trigger (the only reason to open this track)

The project currently argues (originality §4.3, L17 card) that obstacle velocity $\mathbf{v}_{\text{obs}}$ breaks left/right symmetry, so CSC-style mode handling is unnecessary. **This argument holds for crossing traffic (Scenarios A, C) but not for head-on encounters (Scenario B)**: when $\mathbf{v}_{\text{obs}}$ is collinear with the robot path, the dynamic cost field is left/right symmetric and nothing in C2 prefers one side.

Activate X1 **iff** C2 trials in Scenario B (or D) show mode-averaging symptoms:

1. Lateral command oscillation / sign flips of $\omega$ as the pedestrian approaches (left- and right-pass rollouts alternately winning), **or**
2. Hesitation: forward speed collapse without commitment to either side (a "soft freeze"), **or**
3. Minimum separation in Scenario B materially worse than in Scenario A at equal relative speed.

Record these as explicit diagnostics in the C2 runs (per-cycle $\omega$ sign, weighted left-vs-right rollout mass) so the trigger decision is evidence-based, not anecdotal.

**Cheap pre-check before X1:** a small lateral-preference term (e.g. "keep-right" bias in the critic, consistent with Scenario B's stated right-side deflection) may break the symmetry on its own. Try this first; if it suffices, X1 stays closed and the finding is reported as a limitation + fix.

---

## 3. If activated — implementation order

Escalate only as far as needed:

1. **Biased-MPPI-style injected samples** (L21) — add $K \approx 3$–$10$ deterministic ancillary sequences (pass-left, pass-right, brake) to the rollout batch.
2. **log-MPPI noise** (L20) — replace Gaussian noise generator with NLN mixture.
3. **SVG-MPPI guide** (L19) — SVGD on a small particle set to pick the mode, then standard MPPI around it.

All three require **forking `nav2_mppi_controller`** (the optimizer/sampler is not a pluginlib extension point, unlike critics). This breaks the D6 "no core modification" property **for C3 only**; C0–C2 remain on upstream Nav2.

---

## 4. Evaluation if activated

- Add **C3 = C2 + sampler variant** to the ablation, run **only on the scenarios that triggered it** (B, possibly D) plus Scenario E as a regression control. Do **not** expand the full 5-scenario matrix.
- Report C2→C3 as an isolated sampler effect (critic held fixed).
- Report controller cycle time; C3 must stay within the same CPU loop-rate target as C2 or the result is not deployable in the brownfield framing.

---

## 5. If not activated

Report in the dissertation as: *"Head-on symmetry was examined as a known MPPI failure mode (L17, L19); C2 did not exhibit it under the tested conditions [evidence], so sampler modifications were not required."* That is a valid negative result and costs no extra simulation time.
