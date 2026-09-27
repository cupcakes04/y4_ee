# {Concept Name}
**Subject:** {SUBJECT_CODE} — {Subject Name}
**Triggered by:** {the confusion or question that started this session}
**Depends on:** → [concept_name](../concepts/concept_name.md), [cross_subject_concept](../../../EEEE0000_subject/concepts/concept_name.md)
**Date:** YYYY-MM-DD
**Status:** draft

> Status: `draft` = captured but links not fully declared · `solid` = understood, no open gaps · `linked` = all dependencies confirmed and cross-linked

---

## The Intuition
> What is actually happening here — no equations, just the engineering story.
> Explain WHY before HOW. If you can't do this section without math, the intuition isn't there yet.

---

## The Detail
> Full verbose explanation.
> Every term defined with units and sign convention.
> Every equation:
>   - What it physically describes
>   - What each variable means (units, direction, sign)
>   - Assumptions required for it to hold
>   - What breaks it (edge cases, saturation, ignored effects)

---

## The Link Declarations
> For each upstream dependency — why this concept can't be understood without it.
> Format: "Depends on [X] because without understanding [X], [specific part of this concept] doesn't make sense."
> Upstream only. Never declare forward/downstream links here.

---

## Anti-Patterns
> What gets confused here. What the wrong mental model looks like.
> Format: "Anti-pattern: [wrong thinking]. Why it's wrong: [reason]. Correct understanding: [right model]."

---

## Open / Unresolved
> Anything still unclear after this session. Each item should also be logged in `../gaps/gap_log.md`.

- [ ] ...
