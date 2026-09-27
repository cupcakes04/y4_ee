# Gemini Prompt — Subject Map (derived from concepts/)

> Run this after you've accumulated several concept files for a subject (not before).
> Paste all concept files for the subject into the prompt below.
> Copy output into `maps/subject_map.md`.
> Re-run whenever you've added significantly more concepts.

---

## Prompt

```
I have built concept notes for {subject name}. I will paste them all below.

Your job is to produce a SUBJECT MAP — a derived view of how my concepts connect.
Do not add information that isn't in the concept notes. Only derive from what I've captured.

Produce:

## The Core Narrative
[One paragraph: what is this subject actually about at the engineering level?
 Derived from the concepts I've captured — not the module descriptor.]

## Load-Bearing Concepts
[The 3–5 concepts that, if understood deeply, make everything else derivable.
 Name them using my exact concept file names. Explain WHY each is load-bearing.]

## Dependency Graph
[Text form. Use: A → B → C
 Each concept I've captured should appear somewhere.
 If a concept has no declared dependencies, mark it as (root).]

## Orphaned Concepts
[Any concept that has Link Declarations pointing to a concept I haven't captured yet.
 List them as: "{concept_name}.md" declares dependency on "{missing_concept}" — not yet captured.]

## Subject-Level Anti-Patterns
[Confusion patterns that appear across multiple concepts.
 Only include patterns that appear in at least two of my concept notes.]

## Gaps to Fill Next
[Based on the orphaned concepts and open/unresolved sections across all notes,
 what concept should I capture next to strengthen the map most?]

---

Concept notes below:

{paste all concepts/*.md files here}
```
