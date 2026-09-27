# Gemini Prompt — Untangle (Start of Confused Session)

> Use this when you're hitting a wall — concepts feel blurry, terminology is mixing, or you don't know where to start.
> Run this BEFORE asking Gemini to explain anything.
> It forces decomposition first, so you're not explained 5 things at once.

---

## Prompt

```
I'm confused about something in {subject / topic area}. Before explaining anything, I need you to help me untangle it.

Here is what I'm confused about:
{describe the confusion — paste slide text, a diagram description, a question you can't answer, or just write what feels wrong}

Do this ONLY — do not explain the concepts yet:

1. List all the distinct sub-concepts or ideas that are involved in what I just described.
   Give each one a clear, searchable name (e.g. "Z-transform region of convergence", not just "ROC").

2. Order them by dependency — which ones must be understood before the others?
   Format: A → B → C (A must come first)

3. Tell me which single concept is the actual blocker — the one that, once I understand it, will make the others click.

4. Tell me if I'm missing any foundational concept that I probably haven't mentioned but need.

After I confirm, we'll work through the blocker first and only the blocker.
```

---

## After the Untangle

Once Gemini gives you the decomposition:
- Confirm the blocker concept
- Say: "Explain only {blocker concept}. When I say I understand it, we'll move to the next."
- Work through them in order, one at a time
- At the end of each one, run `produce_note.md` to capture it
