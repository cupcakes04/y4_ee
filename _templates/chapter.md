# CH## — Chapter Title
**Subject:** {SUBJECT_CODE} — {Subject Name}
**Pipeline stage:** notes
**Last updated:** YYYY-MM-DD
**Status:** draft | review | locked

---

## 1. Physical / Engineering Intuition
> What is actually happening here, before any math?
> Write as if explaining to someone who has never seen this topic — but is an engineer.
> No equations in this section. Just the "why it behaves this way" story.

---

## 2. Core Concepts
> Every term defined verbosely. Assume nothing is shared knowledge within this section.
> If a concept depends on something from a previous chapter, link it explicitly:
> → depends on: [CH01 — Name](../notes/ch01_name.md)

---

## 3. Key Equations
> For each equation:
> - State what it is
> - What each variable physically represents (units, direction, sign convention)
> - When it applies (assumptions / operating region)
> - What breaks it (edge cases, saturation, non-linearities)

---

## 4. Tables & Figures
> Reproduce all tables in markdown.
> Caption every figure with: what it shows, what to read from it, what changes when parameters change.
> Do not just copy the slide label — explain what the figure is telling you.

---

## 5. Anti-Patterns
> Common mistakes, misconceptions, exam traps.
> Format: "Common mistake: [X]. Why it's wrong: [Y]. Correct understanding: [Z]."

---

## 6. Simulation / Lab Notes
> What the simulation or lab is showing.
> Which parameters do what — change X, Y changes because...
> What would break the real system that the sim ignores.

---

## 7. Upstream Dependencies
> List only what THIS chapter depends on. No downstream links.
> → [CH## — Name](../notes/ch##_name.md): why it's needed here

---

## 8. Open Questions / Gaps
> Anything not fully understood after running the pipeline.
> Each item should be copied to `../gaps/gap_log.md` and flagged for Stage 2 re-run.

- [ ] Gap: ...
