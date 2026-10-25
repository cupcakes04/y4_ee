# FYP Engineering System Contract & Agent Architecture

> **Purpose**: This internal document establishes the operational contract for AI agents collaborating on the EEEE4077 Final Year Project. It defines the boundary between the internal engineering source-of-truth and outward-facing academic deliverables.

---

## 1. Repository Zoning & Governance

| Zone | Directory / Path | Role | Authority & Mutability |
|---|---|---|---|
| **Core Source of Truth** | `chapters/research/`<br>`chapters/library/` | **Engineering Reality & Foundational Research**: System architecture, perception/tracking pipelines, MPPI control mathematics, benchmark ablation specs, and master citation register. | **Primary Source of Truth**. Maintained by student and agent. Technical facts must originate here. |
| **Exploratory & Parked Concepts** | `chapters/explore/` | **Parked / Non-Core Research**: Exploratory prototypes (e.g. offline VLM hazard distillation `avp`, floor homography IPM) and discarded/parked theoretical concepts. | Decoupled from core deliverables. Preserved for academic breadth without cluttering the engineering critical path. |
| **Outward Deliverables & Academic Planning** | `chapters/deliverables/`<br>`chapters/planning/` | **Academic Deliverables & Supervisor Interfaces**: Project proposal (`project_proposal.md`), abstract (`abstract.md`), future thesis (`thesis.md`), defense presentation slides, and planning specs (`specifications.md`, `methodology.md`, `risks.md`, `schedule.md`, `originality.md`, `decisions.md`). | **Derived & Synchronized**. These exist for the supervisor, examiners, and rubric compliance. Must strictly reflect the facts in `research/` and `library/`. |
| **Academic & Module Requirements** | `raw/` | **University & Module Directives**: Coursework briefs (`proj_proposal_guide.md`, `thesis_guide.md`), MEng grading rubrics, meeting proformas, title page templates, and module guides (`EEEE4077.pdf`). | **Read-Only**. Never edit or modify files in `raw/`. |
| **Student Private Sanctum** | `chapters/meetings/`<br>`concepts/` | **Personal Logbook & Exploratory Scratchpads**: Student meeting notes, logbook entries, ROS 2 workspace drills, canvas diagrams, and scratch notes. | **STRICTLY OFF-LIMITS**. Agents must NEVER edit, overwrite, or delete anything in `meetings/` or `concepts/`. |

---

## 2. Derivation Principle: "Single Source of Truth"

```
 ┌─────────────────────────────────────────────────────────┐
 │               CORE SOURCE OF TRUTH (For Us)              │
 │  • chapters/research/ (00_context.md -> 08_tradeoffs.md)│
 │  • chapters/library/  (register.md, synthesis.md, cards)│
 └─────────────┬─────────────────────────────┬─────────────┘
               │                             │
   Governed by │ Requirements    Governed by │ Requirements
   raw/proposals/                raw/thesis/ & raw/general/
               ▼                             ▼
 ┌───────────────────────────┐ ┌───────────────────────────┐
 │   PLANNING & PROPOSALS    │ │   THESIS & DEFENCE SUITE  │
 │ • chapters/planning/      │ │ • chapters/deliverables/  │
 │   - specifications.md     │ │   - project_proposal.md   │
 │   - methodology.md        │ │   - abstract.md           │
 │   - originality.md        │ │   - thesis.md (future)    │
 │   - risks.md              │ │   - defence_slides.md     │
 │   - schedule.md           │ │                           │
 │   - decisions.md          │ │                           │
 └───────────────────────────┘ └───────────────────────────┘
```

1. **Never invent facts in `planning/` or `deliverables/`**:
   Any technical claim, metric, algorithm, or parameter must exist in `research/` or `library/` first.
2. **Align with `raw/` Module Requirements**:
   - Proposal: 7–8 body pages at 12 pt Times New Roman / equivalent, numbered citations, 4-slide defense deck (`raw/proposals/`).
   - Thesis: 40% Design & Implementation, 30% Testing & Validation, 25% Conclusion/Impact, 5% Quality (`raw/thesis/`).
   - Planning: SMART specifications with Minimum and Target hypotheses, quantified risk register ($L \times I$), 450-hour Gantt chart with 5 progress reviews.
3. **Park Fluff in `explore/`**:
   Theoretical or philosophical concepts that do not contribute to working mechatronics software/hardware (e.g., speculative VLM prompts, open-ended cognitive architectures) must be documented in `chapters/explore/`, keeping core deliverables lean, defensible, and realistic.

---

## 3. Working Guidelines for Pair Programming

1. **Practical Engineering Over Academic Fluff**: Prioritize working ROS 2 / Nav2 nodes, real-time loop rates, and clean C++ plugins over decorative complexity.
2. **Deterministic Citations**: All academic citations in deliverables must map directly to stable keys (`L1` to `L17`) in `chapters/library/register.md`.
3. **Continuous Consistency**: Keep requirement IDs (O1–O3, S1–S2), risk IDs (R1–R11), and scenario definitions (A–D) strictly synchronized across all planning and deliverable documents.

