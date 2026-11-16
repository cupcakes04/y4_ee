# L19: SVG-MPPI: Stein Variational Guided Model Predictive Path Integral Control

- **Key:** L19
- **Authors:** Kohei Honda, Naoki Akai, Kosuke Suzuki, Mizuho Aoki, Hirotaka Hosogaya, Hiroyuki Okuda, Tatsuya Suzuki
- **Venue / Year:** arXiv:2309.11040, 2023 (revised Feb 2024)
- **URL:** [https://arxiv.org/abs/2309.11040](https://arxiv.org/abs/2309.11040) · Code: [kohonda/proj-svg_mppi](https://github.com/kohonda/proj-svg_mppi)
- **Status:** S (arXiv listing via search)
- **Scope Track:** Conditional Track X1 (D10)

---

## Technical Summary
- MPPI's Gaussian approximation of the optimal action distribution struggles with **multimodal** optima (e.g. pass-left vs. pass-right).
- A modified **Stein Variational Gradient Descent** on a small particle set roughly estimates the target mode, which is embedded into MPPI to give a closed-form mode-seeking solution.
- Validated on 1/10-scale vehicles (F1TENTH); reported better path tracking and obstacle avoidance than MPPI and other sampling-based SOC methods.

---

## Project Relevance
- Direct fix for the head-on mode-averaging risk in Scenario B.
- Highest implementation cost of the X1 options; requires forking `nav2_mppi_controller`. SVGD is pairwise in particles, so only viable on a small guide set within the CPU budget.

---

## BibTeX
```bibtex
@misc{honda2023svgmppi,
  author = {Honda, Kohei and Akai, Naoki and Suzuki, Kosuke and Aoki, Mizuho and Hosogaya, Hirotaka and Okuda, Hiroyuki and Suzuki, Tatsuya},
  title  = {Stein Variational Guided Model Predictive Path Integral Control: Proposal and Experiments with Fast Maneuvering Vehicles},
  year   = {2023},
  eprint = {2309.11040},
  archivePrefix = {arXiv}
}
```
