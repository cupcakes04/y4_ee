# Gemini Prompt — Stage 4: Drills

> Run this after the mental model is done for a subject (or per chapter).
> Paste the mental model + relevant chapter notes.
> Copy output into `drills/ch##_drills.md` or `drills/subject_drills.md`.

---

## Prompt

```
I am drilling myself on a final year MEng engineering module using a mental model I built.

Your job is to generate practice questions that test UNDERSTANDING, not recall.

RULES:
1. Questions must require reasoning, not memory. No "define X" or "state the formula for Y".
2. Question types to use:
   - "Explain the intuition behind X without using equations"
   - "What happens to [output] if [parameter] changes — and why?"
   - "Where does [equation/model] break down, and what does that mean physically?"
   - "Derive [result] from first principles, starting from [basic concept]"
   - "Two scenarios are presented. Which is correct and why?"
   - "A student says [common misconception]. What is wrong with this reasoning?"
3. For each question, also provide:
   - The correct answer (verbose — full reasoning, not a one-liner)
   - Which concept / chapter this tests
   - Difficulty: foundational / intermediate / stretch
4. Include at least 2 "stretch" questions per chapter that combine concepts from multiple chapters.
5. Flag questions that target known anti-patterns from the notes.

Format each question as:

---
**Q#** [Difficulty] [Chapter / Concept]
[Question text]

<details>
<summary>Answer</summary>

[Full verbose answer]

</details>
---

Mental model and chapter notes below:
[PASTE CONTENT HERE]
```
