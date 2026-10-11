---
name: fyp-proposal-sync
description: Keep the FYP proposal files in sync. core.md and literatures.md are the source of truth. abstract.md (supervisor discussion) and project_proposal.md (assessed submission) are derived from them. Use when asked to update, regenerate, check or sync the proposal, abstract, problem statement, objectives, risks or schedule for EEEE4077.
---

# FYP proposal sync

## Layout (`modules/EEEE4077_mechatronics_proj/`)

| File | Role | Edit by |
|---|---|---|
| `chapters/proposals/core.md` | **Source of truth**: technical design (Part A) and planning layer (Part B: scope, spec, protocol, methodology, originality, risks, schedule, decisions) | Human, or agent on request |
| `chapters/proposals/literatures.md` | **Source of truth**: literature notes, reference register (§5, with keys L1…) and claim audit (§6) | Human, or agent on request |
| `chapters/proposals/abstract.md` | **Derived**: plain-language problem statement and objectives for the supervisor | Agent, from the sources |
| `chapters/proposals/project_proposal.md` | **Derived**: the submitted Project Planning Report (7–8 body pages) | Agent, from the sources |
| `raw/proposals/` | Requirements: `proj_proposal_guide.md`, `Project Planning Report MEng Rubric.pdf`, worksheet, workshop slides | Read-only |

Never write facts that exist only in a derived file. If a derived file needs a new fact, add it to a source file first and then regenerate.

## Workflow

1. **Read** `core.md`, `literatures.md` and `raw/proposals/proj_proposal_guide.md`. Re-read the rubric PDF when checking.
2. **Diff intent.** Say which source sections changed and which derived sections they affect. Use this map:
   - core §1–§2 → abstract §1–§3, proposal §1
   - core §7–§8 → abstract §5, proposal §2
   - core §9–§10 → proposal §2 (protocol), §3
   - core §11 → proposal §4
   - core §12 → proposal §5
   - core §13 → proposal §6
   - literatures §5 → both reference lists
3. **Regenerate** only the affected derived sections. Do not rewrite untouched sections.
4. **Check** against the rubric checklist and the consistency checks below.
5. **Report** what changed, any open `[placeholder]` or `[citation to be added]` markers, and anything unverifiable.

## Style rules

- `abstract.md`: plain language first. ROS 2 keywords go in `code font` with a one-clause gloss at first use. Moderate technical level. Keep a glossary and a "Notes for me" section.
- `project_proposal.md`: academic tone, third person, no "I". Tables and figures are numbered and captioned. Single citation style, numbered by order of first appearance. Body of sections 1–6 should come to 7–8 A4 pages at 12 pt.
- Every numeric target is a hypothesis with a **Minimum** and a **Target**. Never state a target as a result.
- Describe `avp` (https://github.com/cupcakes04/avp) as the author's own incomplete prototype. Never cite it as a result.

## Citation rules (strict)

- Cite only references in `literatures.md` §5. Never invent a citation or a number.
- Before a reference goes into a derived file, open the source (arXiv abstract, DOI or publisher page, official docs) and confirm the title and authors. Then record the status in the register: **V** opened and matched, **S** search summary only, **T** textbook, not opened.
- If a claim has no verified source, either soften it to a qualitative statement or leave a visible marker (`[citation to be added]`) and list it in the report. Do not drop it silently.
- Renumber citations by first appearance whenever text is moved. Check that every `[n]` in the text has a list entry and that every list entry is cited.

## Rubric checklist (`Project Planning Report MEng Rubric.pdf`)

- **Overview (5%)**: aim and importance. Block diagram with styled sub-systems, component-level requirements (interfaces, rates, limits), and dependencies. Engineering and commercial references.
- **Originality (25%)**: need shown from wider background and comparison with current practice. Limitations stated and their effect quantified. Originality in the process as well as the product. More than one type of novelty.
- **Specification (7.5%)**: prioritised, with stretch goals. Each point has a quantitative justification, an assessed challenge, a test with success criteria, and a feasibility argument.
- **Methodology (7.5%)**: development process with tools. Interdependencies. Challenge per step against the student's skills and the extra work it creates. Limitations. Synthesis into a bespoke solution.
- **Risk (15%)**: project risks (not H&S), project-specific. Likelihood and impact are quantified. Timing is stated. Critical risks are rated before and after mitigation. Mitigations are realistic.
- **Time plan (15%)**: Gantt with tasks, milestones and five progress reviews. Dependencies and parallelism. Develop–test–document cycle. Hours per week. Uncertainty.
- **Interview (25%)**: 4 slides (title and block diagram, methods, risk register, Gantt). Build them from the proposal when asked.

## Consistency checks before finishing

- Objective IDs (O1–O3, S1–S2), requirement IDs and risk IDs are identical across `core.md`, `abstract.md` and `project_proposal.md`.
- Task hours in the phase table sum to the stated total. Gantt dates match the week numbers (W1 = Monday 2026-10-12 unless changed in `core.md` §13).
- The project title, student name and ID, and supervisor name match the cover page. Sources: Nicholas Khor Han Le, 20617556, supervisor Dr. Shalini Darmaraju.
- No derived file contains a claim that contradicts `literatures.md` §6 (claim audit).
- Files are UTF-8 and mermaid blocks parse.

## Do not

- Do not edit `raw/`.
- Do not overwrite a source file wholesale. Append or edit sections.
- Do not remove open-item markers until the underlying item is resolved.

