# Mechatronics Industrial Project (EEEE4077) — Workspace

This workspace organizes the final year project into decoupled areas for engineering research, academic coursework planning, literature management, submission deliverables, and exploratory prototyping.

---

## Workspace Layout

```
modules/EEEE4077_mechatronics_proj/chapters/
├── research/        # Engineering design, algorithms, architecture, MPPI critic & ablation benchmark
├── planning/        # Coursework requirements, SMART specs, risks & schedule
├── library/         # Literature reviews, reference register & paper summaries
├── deliverables/    # Assessed submission reports (abstract & project proposal)
├── explore/         # Decoupled exploratory prototypes (offline VLM distillation & floor hazards)
└── meetings/        # Supervisor meeting records and templates
```

---

## Directory Guides

- **[`research/`](./research/)**  
  Living technical workspace for the project's core engineering deliverables:
  - `00_context.md`: The sensor-to-motion pipeline: how sensors measure reality, spatial models (costmaps vs. states), and how planners steer.
  - `01_problem_statement.md`: Industrial AMR navigation and the freezing robot problem.
  - `02_system_architecture.md`: Multi-modal perception, predictive MPPI control, and ablation harness flow.
  - `03_perception_and_tracking.md`: 2D MOT (ByteTrack), camera-laser calibration, frustum gating, Kalman state filtering.
  - `04_predictive_mppi_control.md`: Nav2 MPPI controller foundations and custom C++ dynamic critic plugin.
  - `05_ablation_and_evaluation.md`: 3-way comparative ablation study (C0 vs C1 vs C2), Scenarios A–E, and quantitative metrics.
  - `06_hardware_and_stack.md`: Hardware specifications, ROS 2 Jazzy workspace packages, and Gazebo Harmonic testbed.
  - `07_scope_and_bounds.md`: Methodological principles and out-of-scope boundaries.
  - `08_design_tradeoffs_and_alternatives.md`: Sensor trade-offs, state estimation models, CAD vs semantics, and costmap vs predictive rollouts.

- **[`planning/`](./planning/)**  
  Coursework management and rubric compliance: SMART specifications, development methodology, originality analysis, project risk register, and the W1–W30 Gantt schedule.

- **[`library/`](./library/)**  
  Literature database and citation management: thematic literature review synthesis, verified reference register (`register.md`), and individual paper reading notes (`papers/`).

- **[`deliverables/`](./deliverables/)**  
  Formal assessed documents generated from the workspace: the supervisor-facing [`abstract.md`](./deliverables/abstract.md) and the formal assessed [`project_proposal.md`](./deliverables/project_proposal.md).

- **[`explore/`](./explore/)**  
  Decoupled background prototype archive: offline prompt distillation of non-geometric surface hazards (`avp`) preserved outside the assessed core deliverables.

- **[`meetings/`](./meetings/)**  
  Supervision meeting notes and formal meeting record forms.
