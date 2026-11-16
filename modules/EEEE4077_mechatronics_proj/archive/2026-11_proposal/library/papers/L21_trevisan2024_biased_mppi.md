# L21: Biased-MPPI: Informing Sampling-Based MPC by Fusing Ancillary Controllers

- **Key:** L21
- **Authors:** Elia Trevisan, Javier Alonso-Mora (TU Delft)
- **Venue / Year:** *IEEE Robotics and Automation Letters*, vol. 9, no. 6, pp. 5871–5878, 2024, doi:10.1109/LRA.2024.3397083 (arXiv:2401.09241)
- **URL:** [https://arxiv.org/abs/2401.09241](https://arxiv.org/abs/2401.09241)
- **Status:** S (arXiv + TU Delft repository listing via search)
- **Scope Track:** Conditional Track X1 (D10)

---

## Technical Summary
- MPPI performance depends heavily on the sampling distribution; centring a Gaussian on the previous solution causes local minima and failures.
- Re-derives MPPI to allow **arbitrary sampling distributions**, then fuses samples from multiple classical and learned **ancillary controllers** into the rollout set.
- Evaluated for robustness to model uncertainty, reactivity to sudden changes, local minima, and sample efficiency (sim + real).

---

## Project Relevance
- First choice if X1 activates: inject a few deterministic pass-left / pass-right / brake sequences into the batch. Cheap, explainable, and theoretically grounded by this paper.

---

## BibTeX
```bibtex
@article{trevisan2024biasedmppi,
  author  = {Trevisan, Elia and Alonso-Mora, Javier},
  title   = {Biased-{MPPI}: Informing Sampling-Based Model Predictive Control by Fusing Ancillary Controllers},
  journal = {IEEE Robotics and Automation Letters},
  volume  = {9},
  number  = {6},
  pages   = {5871--5878},
  year    = {2024},
  doi     = {10.1109/LRA.2024.3397083}
}
```
