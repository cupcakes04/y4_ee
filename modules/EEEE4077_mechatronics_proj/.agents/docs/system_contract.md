# FYP Engineering System Contract & Agent Architecture

> **Purpose**: This internal document establishes the operational contract for AI agents collaborating on the EEEE4077 Final Year Project. It defines the boundary between the internal engineering source-of-truth, working draft areas, and outward-facing academic deliverables.

---

## 1. Repository Zoning & Governance

| Zone | Directory / Path | Role | Authority & Mutability |
|---|---|---|---|
| **Core Source of Truth** | `chapters/research/`<br>`chapters/library/` | **Engineering Reality & Foundational Research**: System architecture, perception/tracking pipelines, MPPI control mathematics, benchmark ablation specs, and master citation register. | **Primary Source of Truth**. Maintained by student and agent through active discussion and negotiation. Technical facts must originate here. |
| **Academic & Module Requirements** | `raw/proposals/`<br>`raw/thesis/`<br>`raw/general/` | **University & Module Directives**: Coursework briefs (`proj_proposal_guide.md`, `thesis_guide.md`), MEng grading rubrics, meeting proformas, title page templates, and workshop slides/worksheets. | **Read-Only Ground Truth**. All non-markdown files have corresponding `.md` files for direct reference. Agents across all sessions MUST consult here for examiner expectations, structure, and rubrics. |
| **Proposal Working Workspace** | `chapters/proposals/`<br>*(target: `chapters/proposals/`)* | **Proposal Drafting & Section Structuring**: The agent's workspace to iterate, draft, structure, and refine proposal sections. Can be modularized into clean subfolders or separate files per section. | **Working Draft Layer**. Maintained and updated by the agent. Reflects engineering facts from `research/` structured according to `raw/proposals/` expectations. |
| **Outward Assessed Deliverables** | `chapters/deliverables/` | **Polished Output Repository**: Strictly for finalized, polished submission artifacts meant for examiners and external 3rd parties (`project_proposal.md`, `abstract.md`, future `thesis.md`, defense slides). | **Final Output Only**. Derived and compiled from the working workspace. Not for working drafts or miscellaneous notes. |
| **Exploratory & Parked Concepts** | `chapters/explore/` | **Parked / Non-Core Research**: Exploratory prototypes (e.g. offline VLM hazard distillation `avp`, floor homography IPM) and discarded/parked theoretical concepts. | Decoupled from core deliverables. Preserved for academic breadth without cluttering the engineering critical path. |
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
 │ PROPOSAL WORKING WORKSPACE│ │  FUTURE THESIS WORKSPACE  │
 │ • chapters/proposals/      │ │ • chapters/thesis/        │
 │   - specifications.md     │ │   (To be established      │
 │   - methodology.md        │ │    when thesis phase      │
 │   - originality.md        │ │    begins)                │
 │   - risks.md              │ │                           │
 │   - schedule.md           │ │                           │
 │   - decisions.md          │ │                           │
 └─────────────┬─────────────┘ └─────────────┬─────────────┘
               │                             │
               ▼                             ▼
 ┌─────────────────────────────────────────────────────────┐
 │          DELIVERABLES (Polished Output Repository)      │
 │  • chapters/deliverables/                               │
 │    - project_proposal.md (final compiled 7-8 page report)│
 │    - abstract.md (supervisor briefing)                  │
 │    - thesis.md (future final report)                    │
 │    - defence_slides.md (future 4-slide deck)            │
 └─────────────────────────────────────────────────────────┘
```

1. **Never invent facts in working drafts or deliverables**:
   Any technical claim, metric, algorithm, or parameter must exist in `research/` or `library/` first.
2. **Align with `raw/` Module Requirements & Expectations**:
   - Rubrics do not drive mark-chasing or artificial fluff, but they set the examiner's baseline structural expectations.
   - Proposal: 7–8 body pages at 12 pt Times New Roman / equivalent, numbered citations, 4-slide defense deck (`raw/proposals/`).
   - Thesis: 40% Design & Implementation, 30% Testing & Validation, 25% Conclusion/Impact, 5% Quality (`raw/thesis/`).
   - Planning: SMART specifications with Minimum and Target hypotheses, quantified risk register ($L \times I$), 450-hour Gantt chart with 5 progress reviews.
3. **Keep `deliverables/` Clean and Polished**:
   No intermediate drafts or rough notes in `deliverables/`. All drafting and modular structuring live in `chapters/proposals/` (or `chapters/proposals/`).
4. **Park Fluff in `explore/`**:
   Theoretical or philosophical concepts that do not contribute to working mechatronics software/hardware (e.g., speculative VLM prompts, open-ended cognitive architectures) must be documented in `chapters/explore/`, keeping core deliverables lean, defensible, and realistic.

---

## 3. Working Guidelines for Pair Programming

1. **Practical Engineering Over Academic Fluff**: Prioritize working ROS 2 / Nav2 nodes, real-time loop rates, and clean C++ plugins over decorative complexity.
2. **Deterministic Citations**: All academic citations in deliverables must map directly to stable keys (`L1` to `L17`) in `chapters/library/register.md`.
3. **Continuous Consistency**: Keep requirement IDs (O1–O3, S1–S2), risk IDs (R1–R11), and scenario definitions (A–D) strictly synchronized across all planning and deliverable documents.
