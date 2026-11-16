# L20: log-MPPI: Autonomous Navigation of AGVs in Unknown Cluttered Environments

- **Key:** L20
- **Authors:** Ihab S. Mohamed, Kai Yin, Lantao Liu
- **Venue / Year:** arXiv:2203.16599, 2022
- **URL:** [https://arxiv.org/abs/2203.16599](https://arxiv.org/abs/2203.16599)
- **Status:** S (arXiv listing via search)
- **Scope Track:** Conditional Track X1 (D10)

---

## Technical Summary
- Replaces MPPI's Gaussian perturbations with samples from a **normal log-normal (NLN) mixture**, giving heavier-tailed exploration.
- Argues the MPPI derivation approximately holds for NLN noise at small noise values.
- Validated on 2D cluttered navigation (sim + real) and cartpole; reported higher success rates than MPPI at similar or lower noise variance (secondary claim — confirm in paper).

---

## Project Relevance
- Smallest code change of the X1 options (noise generator only), but weakest guarantee against left/right mode averaging.

---

## BibTeX
```bibtex
@misc{mohamed2022logmppi,
  author = {Mohamed, Ihab S. and Yin, Kai and Liu, Lantao},
  title  = {Autonomous Navigation of {AGVs} in Unknown Cluttered Environments: log-{MPPI} Control Strategy},
  year   = {2022},
  eprint = {2203.16599},
  archivePrefix = {arXiv}
}
```
