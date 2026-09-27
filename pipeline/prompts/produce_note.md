# Gemini Prompt — Produce Note (End of Session)

> Use this at the **end of every Gemini learning session**, once you feel you've reached an understanding (even partial).
> Copy the output directly into `concepts/{concept_name}.md`.
> Replace everything in `{curly braces}` before pasting.

---

## Prompt

```
We've just worked through {concept name} in {subject name}.

Produce a concept note in this exact format. Do not summarise — expand everything verbosely.

---

# {Concept Name}
**Subject:** {SUBJECT_CODE} — {Subject Name}
**Triggered by:** {paste or summarise the original confusion/question}
**Depends on:** → [list every concept this relies on, as I would search for them]
**Date:** {today's date}
**Status:** draft

---

## The Intuition
[The engineering story — WHY before HOW. No equations. If this section needs math to make sense, the intuition isn't there yet.]

## The Detail
[Full verbose explanation. Every term defined. Every equation:
 - what it physically describes
 - what each variable means with units
 - what assumptions it requires
 - what breaks it]

## The Link Declarations
[For each upstream dependency: "Depends on [X] because without [X], [specific part] doesn't make sense."
 Upstream links only. Never list what this concept enables — only what it needs.]

## Anti-Patterns
[What gets confused here. Format: "Anti-pattern: [wrong]. Why wrong: [reason]. Correct: [right model]."]

## Open / Unresolved
[Anything still unclear from our session. Be specific — vague gaps are useless.]

---

Rules you must follow:
- Never summarise. Always expand.
- Lead The Intuition section with physical/mechanical reasoning, not math.
- The Link Declarations section is mandatory even if there is only one dependency.
- If something was unclear during our session, put it in Open/Unresolved — do not invent an answer.
- Status is always "draft" when first produced.
```
