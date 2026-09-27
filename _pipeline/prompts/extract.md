# Gemini Prompt — Stage 2: Structure (Chapter Notes)

> Paste this prompt into Gemini Chat, then attach the PDF or paste the extracted text below it.
> Copy the output directly into `notes/ch##_name.md` using the chapter template.

---

## Prompt

```
I am building verbose, intuition-first engineering study notes for a final year MEng module.

Your job is to process the attached lecture material and produce a structured chapter note following these rules exactly:

RULES:
1. Never summarize. Always expand. If the source is brief, explain what it means in depth.
2. Lead with physical/engineering intuition before any math. I want to understand WHY before HOW.
3. For every equation:
   - State what it describes physically
   - Define each variable with units and sign convention
   - State the assumptions it requires
   - State what breaks it (edge cases, saturation, non-linearities, ignored effects)
4. Reproduce every table in markdown format. After each table, add a sentence: "What this table tells you: ..."
5. For every figure or diagram: describe what it shows, what changes when key parameters change, and what the key takeaway is. Do not just repeat the caption.
6. Explicitly flag common mistakes and misconceptions with the label: "Anti-pattern: ..."
7. If something is unclear or missing from the source material, say so explicitly: "GAP: ..." — do not fill gaps with assumptions.
8. Do not use bullet points as shortcuts for explanation. Write full sentences.

OUTPUT FORMAT (follow this structure exactly):

## 1. Physical / Engineering Intuition
## 2. Core Concepts
## 3. Key Equations
## 4. Tables & Figures
## 5. Anti-Patterns
## 6. Simulation / Lab Notes (skip if not applicable)
## 7. Upstream Dependencies
## 8. Open Questions / Gaps

Now process the following material:
[ATTACH PDF or PASTE TEXT HERE]
```
