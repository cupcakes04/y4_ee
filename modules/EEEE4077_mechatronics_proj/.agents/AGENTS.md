# EEEE4077 Mechatronics FYP Agent Instructions

## Core Working Principle: Practical Engineering Over Academic Fluff

The user is fundamentally building a real, functioning mechatronics engineering pipeline and prioritizes working, maintainable software and hardware reality over decorative academic theater or grade-rubric chasing.

Every agent interacting with this project (`EEEE4077_mechatronics_proj`) MUST adhere to the following rules:

1. **Practical Engineering First:**
   - Always prioritize battle-tested, proven, open-source industrial solutions (e.g., standard ROS 2 / Nav2 packages, Ultralytics, BoxMOT, OpenCV, standard Kalman filtering) over ungrounded "novel" algorithms.
   - If a standard industrial tool exists, USE IT. Never suggest inventing a new algorithm when an idiomatic standard exists.
   - Do not propose decorative complexity (e.g., unnecessary deep learning networks, complex non-linear models) where linear or simple methods suffice.

2. **Zero Mark-Chasing Bias (Rubric Fluffing Forbidden):**
   - The user gives zero weight to chasing rubric criteria or pandering to grading rubrics purely to sound academically impressive.
   - Do NOT propose architectural additions, research directions, or scope expansions purely for marks.
   - However, **rubrics and guides in `raw/` define the structural baseline and examiner expectations** (e.g., required sections, formatting, evaluation categories). Use them strictly to ensure proper structure, completeness, and clarity without injecting fluff.
   - When preparing reports, trade-offs, or defense notes, base every argument on real physical and computational constraints (field of view, memory, frame rates, sensor physics, wall-clock engineering time).
   - Be completely blunt and transparent about what works, what doesn't, and where practical engineering trade-offs lie.

3. **Workspace Zoning & Responsibilities:**
   - **`raw/proposals/` and `raw/thesis/`**: Ground truth requirements and examiner expectations. Every non-markdown file has an equivalent `.md` file for fast, reliable cross-referencing. Agents across all sessions MUST consult these files when preparing or checking proposals and thesis work.
   - **`chapters/research/`**: Engineering truth. Technical details, models, architecture, trade-offs, and algorithms. This is where user and agent actively negotiate and build.
   - **chapters/research/notes/**: Personal concept understanding notes (titled and indexed after research sections, e.g., section 4.1.1 becomes 4_1_1_<topic>.md). Dedicated to building intuitive personal understanding and unpacking complex mathematical/theoretical foundations for the student; these are personal study aids, not assessed deliverables.
   - **`chapters/proposals/` (or `chapters/proposals/`)**: The agent's working area for proposal sections. Can be modularized into discrete section files or subfolders for clean organization, drafting, and iterative refinement.
   - **`chapters/deliverables/`**: Strictly the outward-facing output repository. Holds polished, final-ready submission documents meant for examiners / 3rd parties (e.g., `project_proposal.md`, `abstract.md`, future `thesis.md`). Do not use this as a working draft area or internal reference dump.
   - **Thesis workflow**: Will follow a similar decoupled working structure later.

4. **Respect Student Engineering Bandwidth:**
   - Never inflate project scope with unrealistic academic ambitions.
   - Keep the critical path achievable and decoupled so that unexpected hurdles do not cascade into project failure.

