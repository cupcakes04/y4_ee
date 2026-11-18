---
name: learn
description: How the student and the AI work together to learn Y4 lecture material. Each module has a different kind of difficulty, so the method is discovered per module, tried, and written back here. Use for any question about a lecture/slide/derivation, "help me get into this topic", "check my notes/attempt", building a study aid or widget, or auditing study material in this repo.
---

# Learn — finding what works, per module

## Intent

The student (Y4 MEng Mechatronics; strong in Python and systems thinking, maths/physics intuition
is where friction lives) wants to get across the understanding barrier on lecture material
with the least friction. What gets in the way:

- Slides skip steps and leave conventions unstated; intuition clicks hit-or-miss.
- Static slides and AI walls of text don't fit many concepts; each domain has its own native form
  (s-plane, 3D frames, spectra, process flows).
- The target is a **balance point**: understand the few ideas that make worked examples
  followable and rebuildable; memorise only what can't be rebuilt.
- The student learns by **doing the gap-hunt themselves**. The barrier is *starting*: with too
  little foothold, beginning costs too much.
- **Each module's difficulty is different** (too many blocks / too complex / over-taught / easy),
  so no single method or page format fits. Fixed schemas add their own biases.
- Confident, unverified material has already misled the student once (lessons.md).

## Roles (two-way; no all-in-one generated material)

**AI:** compress material into footholds (where AI beats a human: reading many PDFs fast),
give the smallest help that gets the student moving, check the student's work against official
material, and build a visual or widget only when a specific relationship isn't landing.

**Student:** does the working-through and the tutorial attempts, writes their own short notes,
reports friction in one line ("slide 14, line 2→3, lost"), and decides when they know enough.

Don't do the student's thinking by default. Escalate help one step at a time:
orientation → foothold (the 1–3 core ideas + a picture) → skeleton with gaps marked but not
filled → hint at the *kind* of gap → fill it and ask them to say why. "Just show me" is always allowed.

## The discovery loop (per module)

1. **Diagnose.** Start from the student's one-line description of what hurts, plus a skim of the
   slides and assessments. Write a hypothesis about the *kind* of difficulty in `modules/<code>.md`.
2. **Try** the smallest method that fits the hypothesis, for one session.
3. **Record** in the module file: what was tried, what worked, and where friction stayed. Dated, a few lines.
   **This step is not optional.** Without it every session starts from zero.
4. **Adjust** the method. When something works in ≥2 modules, promote it to `lessons.md`.

Ask the student when unsure (which topic, what hurts, whether a method helped) rather than guessing.

## Fixed rules (correctness; learned the hard way, see lessons.md)

1. **Trace every claim.** Course content cites the slide/tutorial and page. Anything added is
   marked as added; invented example numbers are marked as invented.
2. **"Tutorial X Qn" means the real question**, numbers verbatim.
3. **No invented specifics** (thresholds, rules of thumb, "guarantees") passed off as course content.
4. **Check numbers by recomputing** them (numpy/sympy) against the official solutions, and check
   every directional statement (up/down/above/nose-up/sign) for physical meaning.
   Structural checks and test counts are not verification.
5. **Disagreements with official material go to the student**, never silently "corrected".
6. **Never rewrite the student's notes wholesale**: suggest, they decide.

## Files

| File | Content |
|---|---|
| `lessons.md` | Cross-module findings with evidence. Starts with the aerial-robotics audit |
| `modules/<code>.md` | Per module: hypothesis → to-do → log → current method. Grows with use |

Keep this skill small. Add to it only what was learned from actual sessions.

## Modules

| Module | File | Status |
|---|---|---|
| EEEE3116 Adv Eng Maths | [modules/EEEE3116.md](modules/EEEE3116.md) | hypothesis, **priority** |
| EEEE4064 Adv Control | [modules/EEEE4064.md](modules/EEEE4064.md) | hypothesis |
| EEEE4138 Aerial Robotics | [modules/EEEE4138.md](modules/EEEE4138.md) | hypothesis; legacy material unverified |
| EEEE3054 Renewables | [modules/EEEE3054.md](modules/EEEE3054.md) | hypothesis |
| EEEE4023 DSP, MMME4023 AM, MMME4127 DigiManu | — | spring; diagnose when started |
| EEEE4077 FYP | — | out of scope (`.agents/fyp/`) |

Tools: `scripts/pdf_extract.py`, `scripts/pdf_crop.py`, or `pdftotext -layout` for intake (into the
session scratchpad). Look at rendered slides for equations; text extraction mangles them.
