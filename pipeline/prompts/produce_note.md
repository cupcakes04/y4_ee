# Gemini Prompt — Produce Note (End of Session)

Two versions. Pick the right one:

| | When to use |
|---|---|
| **Quick Note** ↓ | You already get it. Just want it written down cleanly. Revision, reinforcement, simple topic. |
| **Deep Note** ↓ | You were confused, you worked through it, you want the full dissection captured. |

---

## Quick Note

> Use for: revision notes, straightforward topics, things you understood without much struggle.
> Save output to `concepts/{concept_name}.md`.

```
Summarise {concept name} from {subject name} as a clean revision note.

Format:

# {Concept Name}
**Subject:** {Subject Name}
**Date:** {today's date}

## What it is (can be tables or plots or graph, simple)
[1–3 sentences. Plain English. What does this actually do or describe?]

## Key Points
- [bullet — one idea per line, no padding]

## Key Equations (if any)
[Equation, then one line per variable: symbol → meaning + units]

## Watch Out For
[1–3 common mistakes or gotchas. Skip if none.]
```

---

## Deep Note

> Use for: concepts you were confused about, worked through in a full session, and want fully dissected.
> Save output to `concepts/{concept_name}.md`.

```
We've just worked through {concept name} in {subject name}.

Produce a concept note in this exact format. Do not summarise — expand everything (can be in point form and 0 academic bias).

---

# {Concept Name}
**Subject:** {Subject Name}
**Triggered by:** {paste or summarise the original confusion/question}
**Depends on:** → [list every concept this relies on, as I would search for them]
**Date:** {today's date}
**Status:** draft

---

## The Intuition
[The engineering story — WHY before HOW. No equations. If this section needs math to make sense, the intuition isn't there yet.]
Less paragraph, less verbose, more attention/attractive

## The Detail
[Full explanation. Every term defined. Every equation:
 - what it physically describes
 - what each variable means with units
 - what assumptions it requires]
use intuive examples or math to show (or anything that suits the topic best for revision/learning)

## The Link Declarations
[For each upstream dependency: "Depends on [X] because without [X], [specific part] doesn't make sense."
 Upstream links only. Never list what this concept enables — only what it needs.]

## Open / Unresolved
[Anything still unclear from our session. Be specific — vague gaps are useless.]

---

Rules you must follow:
- Lead The Intuition section and detail with physical/mechanical reasoning, math examples, visualisations and equations.
- The Link Declarations section is mandatory even if there is only one dependency.
- If something was unclear during our session, put it in Open/Unresolved — do not invent an answer.
- Status is always "draft" when first produced.
```
