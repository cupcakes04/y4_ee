# Gemini Prompt — Chapter Digest (PDF → Markdown)

> **How to use:**
> 1. Open a new Gemini chat.
> 2. Attach the chapter/lecture PDF directly.
> 3. Paste the prompt below (fill in the `{placeholders}`).
> 4. Copy the output into `modules/{SUBJECT}/chapters/L##_{title}.md`.
>    If you have multiple PDFs for the same chapter, use a subfolder instead: `chapters/L##_{title}/part1.md`.

> **Goal:** One dense, self-contained markdown note per chapter — not a summary, a reference.
> Run this once per PDF. If a concept needs deeper work, open a separate session with `untangle.md`.

---

## Prompt

```
I am attaching the PDF for {Chapter number and title} from {SUBJECT_CODE} — {Subject Name}.

Your job is to produce a dense, structured chapter note I will save as a reference.

RULES:
1. Do not summarise — capture everything in the PDF, verbosely.
2. For every equation: write it out, name every variable (with units), state the assumptions, and state what breaks it.
3. For every diagram or figure described: write a text reconstruction as if I cannot see the figure.
4. Flag any concept that requires background knowledge I might not have as: ⚠️ DEPENDS ON: {concept name}.
5. Use the exact section headings from the slides/PDF where they exist.
6. At the end, produce a "Concept Index" — a flat list of every named concept, term, or technique introduced, one per line.
7. Flag anything that seems incomplete, ambiguous, or that the lecturer left as an exercise as: ❓ UNRESOLVED.

Output format below — do not deviate:

---

# {Chapter Number}: {Chapter Title}
**Subject:** {SUBJECT_CODE} — {Subject Name}
**Source:** {PDF filename or lecture number}
**Date captured:** {today's date}

---

## Overview
[2–3 sentence engineering-level answer to: what is this chapter actually about and why does it matter?]

---

## {Section heading from PDF}
[Full verbose content for this section]

[Repeat for every section in the PDF]

---

## Key Equations
[For every equation in the chapter, one block each:]

**{Equation name or description}**
$$
{equation in LaTeX}
$$
- **Variables:** {list every symbol, its meaning, and units}
- **Assumes:** {conditions required for this to hold}
- **Breaks when:** {edge cases or violations}

---

## Concept Index
- {concept / term / technique — one per line, flat list}

---

## Open / Unresolved
- ❓ {anything ambiguous, incomplete, or that needs a separate session}
```

---

## After Running This Prompt

- Save output to `modules/{SUBJECT}/chapters/{chNN}/{chapter_title}.md`
- Skim the **Concept Index** — any concept that surprises you or that you can't explain in 10 seconds → open a new session with `untangle.md`
- Any `⚠️ DEPENDS ON` that you haven't captured yet → add to the queue for your next session
- Once you've worked a concept deeply → run `produce_note.md` → save to `concepts/`
