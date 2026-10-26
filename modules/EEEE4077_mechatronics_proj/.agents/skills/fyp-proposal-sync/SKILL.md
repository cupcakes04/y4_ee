---
name: fyp-proposal-sync
description: Keep the FYP proposal, planning, and deliverable files in sync with internal research source-of-truth. research/ and library/ are the technical truth. proposals/ (or proposals/) is the agent's proposal drafting workspace. deliverables/ is the polished output repository for supervisor and examiners. Use when asked to update, regenerate, check or sync the proposal, thesis, abstract, planning specs, risks, methodology or schedule for EEEE4077.
---

# FYP Synchronization & Deliverable Management

> **Operational Contract**: See [`.agents/docs/system_contract.md`](../docs/system_contract.md) for full architecture rules.

## Layout (`modules/EEEE4077_mechatronics_proj/`)

| Directory / File | Role | Mutability & Rule |
|---|---|---|
| `chapters/research/` | **Source of truth (Internal)**: Technical design, architecture, modules (00–08), hardware stack, trade-offs, and metrics. | Edit by Human or Agent through mutual negotiation. |
| `chapters/library/` | **Source of truth (Internal)**: Reference register (`register.md`), synthesis (`synthesis.md`), and paper cards (`papers/L01`–`L17`). | Edit by Human or Agent on request. |
| `raw/proposals/`<br>`raw/thesis/` | **University Directives & Expectations**: Coursework briefs, rubrics, workshop slides, worksheets, and format rules. | **Read-only Ground Truth**. All non-md files have `.md` equivalents. Always refer here for examiner expectations and structural standards. |
| `chapters/proposals/` | **Proposal Working Workspace**: Agent's workspace for drafting, breaking down, and structuring proposal sections (specifications, methodology, originality, risks, schedule, decisions). | **Derived from research & library, shaped by raw requirements**. Edit and modularize as needed. |
| `chapters/deliverables/` | **Polished Output Repository**: Final submission-ready artifacts (`project_proposal.md` [7–8 pages], `abstract.md`, future `thesis.md`, defense slides). | **Final Output Only**. Clean and polished for supervisor and examiners. No intermediate scratchpads. |
| `chapters/explore/` | **Parked & Exploratory**: Offline VLM hazard distillation (`avp`), IPM homography, and parked theoretical explorations. | Preserved for context, decoupled from core deliverables. |
| `chapters/meetings/` | **Student Logbook**: Official meeting records and supervisory logs. | **STRICTLY OFF-LIMITS**. Do not touch. |
| `concepts/` | **Student Scratchpad**: Student's private notes, canvas diagrams, and ROS 2 test drills. | **STRICTLY OFF-LIMITS**. Do not touch. |

Never write facts that exist only in a derived or planning file. If a planning or deliverable document needs a new technical claim, add it to `research/` or `library/` first, then propagate.

---

## Workflow

1. **Read Sources**: Read `chapters/research/`, `chapters/library/register.md`, and the relevant guidelines in `raw/proposals/` or `raw/thesis/`.
2. **Diff Intent**: Identify which technical facts changed in `research/` or `library/` and propagate to the working proposal workspace (`proposals/` or `proposals/`):
   - `research/01_problem_statement.md`, `02_system_architecture.md`, `04_predictive_mppi_control.md` → `proposals/specifications.md`, `deliverables/abstract.md`, `deliverables/project_proposal.md` §1–§3
   - `research/05_ablation_and_evaluation.md` → `proposals/specifications.md` (O3 metrics), `proposals/methodology.md` (M4–M5), `deliverables/project_proposal.md` §2–§3
   - `research/08_design_tradeoffs_and_alternatives.md` → `proposals/originality.md`, `proposals/decisions.md`, `deliverables/project_proposal.md` §4
   - `proposals/risks.md` → `deliverables/project_proposal.md` §5 (Table 5)
   - `proposals/schedule.md` → `deliverables/project_proposal.md` §6 (Gantt & workload)
   - `library/register.md` → All reference lists
3. **Compile to Deliverables**: When ready for review or submission, compile the structured sections into the polished output deliverable (`deliverables/project_proposal.md`).
4. **Consistency Audit**:
   - Objective IDs (O1–O3, S1–S2) match across all planning and deliverable files.
   - Risk IDs (R1–R11) match across `proposals/risks.md` and `deliverables/project_proposal.md`.
   - Citations use only registered keys (L1–L17) from `register.md`.
   - Hours sum to 450 h across 30 weeks.
5. **Report**: Summarize synced changes, open action items, and verification status.

---

## Style & Rubric Rules

- `abstract.md`: Plain language first, ROS 2 terms glossed in `code font`, moderate technical depth, includes glossary.
- `project_proposal.md`: Academic third-person tone, 7–8 pages A4, 12 pt font, 2.54 cm margins. Figures/tables numbered and captioned.
- `thesis.md`: Follows `raw/thesis/` rubrics (40% Design & Impl, 30% Testing & Validation, 25% Conclusion/Impact, 5% Completeness).
- All numeric targets are hypotheses structured with **Minimum** and **Target**.
- `avp` is described strictly as an exploratory background prototype.
- SOTA MPPI variants (SE-MPPI, EXACT-MPPI, CSC-MPPI) are positioned as conceptual/literature benchmarks, preserving C0–C2 as the controlled experimental ablation.
