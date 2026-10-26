# Proposal Workspace (`chapters/proposals/`)

> **Role**: This directory is the shared working workspace for drafting, iterating, and structuring all sections of the EEEE4077 Project Planning Report. It bridges the foundational engineering research in `chapters/research/` with the official module expectations in `raw/proposals/`, preparing clean sections that compile into the outward deliverable [`deliverables/project_proposal.md`](../deliverables/project_proposal.md).

---

## 1. Structure & File Map

| Workspace File | Proposal Section Mapped | Primary Focus & Grounding | Governing Raw Standard |
|---|---|---|---|
| **[`overview.md`](./overview.md)** | §1. Overview of the Project | Problem statement, operational bottleneck (freezing robot), purpose, system block diagram, component relationships, literature foundation. | `proj_proposal_guide.md` §2<br>`ee_fyp_proposal_writing_workshop_saleha.md` Slide 3 |
| **[`specifications.md`](./specifications.md)** | §2. Project Specification | Committed core objectives (O1–O3), SMART quantitative hypotheses (Minimum vs Target), stretch goals (S1–S3), deliverables & assessment methods mapping. | `proj_proposal_guide.md` §3<br>`meng_rubric_project_planning_report.md` §2<br>Saleha Slide 4 & 5 |
| **[`methodology.md`](./methodology.md)** | §3. Methodology | Experimental comparative ablation approach, development lifecycle steps (M0–M5), toolchain trade-off analysis, dependency flowchart, critical path. | `proj_proposal_guide.md` §4<br>`meng_rubric_project_planning_report.md` §3<br>Saleha Slide 6 |
| **[`originality.md`](./originality.md)** | §4. Originality & Positioning | Dimensions of novelty, brownfield sensor retrofit, native Nav2 MPPI critic vs SOTA GPU methods, visual comparison matrix, limitations. | `proj_proposal_guide.md` §5<br>`meng_rubric_project_planning_report.md` §4<br>Saleha Slide 7 |
| **[`risks.md`](./risks.md)** | §5. Risk Management | Quantified risk register (R1–R9, $L \times I$), unmitigated impact, mitigations, post-mitigation scores, and explicit technical fallback mechanisms (Fallback F1). | `proj_proposal_guide.md` §6<br>`meng_rubric_project_planning_report.md` §5<br>Saleha Slide 8 |
| **[`schedule.md`](./schedule.md)** | §6. Planned Work Schedule | 450 nominal hours budget across 30 weeks (~15 h/wk), phase breakdown, Mermaid Gantt chart, milestones, and 5 supervisor progress review points (R1–R5). | `proj_proposal_guide.md` §7<br>`meng_rubric_project_planning_report.md` §6 |
| **[`decisions.md`](./decisions.md)** | Architectural Decisions (ADRs) | Engineering decision records (D1–D9), technical trade-offs (e.g. 2D MOT vs 3D clustering, native C++ plugin vs Python rewrite), and supervisor consultation points. | Internal engineering governance & defense justification. |

---

## 2. Derivation & Compilation Workflow

1. **Engineering Source of Truth:** Technical details, algorithms, and models must originate in `chapters/research/` (modules 00–08) and `chapters/library/` (registered citations).
2. **Modular Drafting:** Draft, refine, and review each section independently within this folder.
3. **Compilation to Deliverables:** Once reviewed and aligned with the user, these modular files are compiled into [`chapters/deliverables/project_proposal.md`](../deliverables/project_proposal.md) adhering to the strict 7–8 page A4 format (single-spaced, 12 pt, 2.54 cm margins).

