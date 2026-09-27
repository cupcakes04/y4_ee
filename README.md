# Y4 Study System — MEng Mechatronics

> Pipeline: `raw PDF` → `extracted text` → `verbose notes` → `mental model` → `drills` → `gap log`
> Rule: flow is **one direction only**. Never edit upstream from where you are.

---

## Subjects

| Folder | Code | Subject | Credits | Semester | Status |
|---|---|---|---|---|---|
| [EEEE3116_adv_eng_math](./EEEE3116_adv_eng_math/) | EEEE-3116 | Advanced Engineering Mathematics | 10 | Autumn | ⬜ not started |
| [EEEE4064_adv_control_system](./EEEE4064_adv_control_system/) | EEEE-4064 | Advanced Control System Design | 10 | Autumn | ⬜ not started |
| [EEEE4076_hdl_prog_logic](./EEEE4076_hdl_prog_logic/) | EEEE-4076 | HDL for Programmable Logic | 10 | Autumn | ⬜ not started |
| [EEEE4077_mechatronics_proj](./EEEE4077_mechatronics_proj/) | EEEE-4077 | Mechatronics Industrial Project | 40 | Full Year | ⬜ not started |
| [EEEE4133_ai_intelligent_sys](./EEEE4133_ai_intelligent_sys/) | EEEE-4133 | Artificial Intelligence & Intelligent Systems | 20 | Spring | ⬜ not started |
| [EEEE4138_aerial_robotics](./EEEE4138_aerial_robotics/) | EEEE-4138 | Aerial Robotics | 10 | Autumn | ⬜ not started |
| [EEEE4145_hdl_prog_logic_proj](./EEEE4145_hdl_prog_logic_proj/) | EEEE-4145 | HDL for Programmable Logic with Project | 10 | Spring | ⬜ not started |
| [MMME4127_digital_manufacturing](./MMME4127_digital_manufacturing/) | MMME-4127 | Digital Manufacturing | 10 | Spring | ⬜ not started |

Status key: ⬜ not started · 🟡 in progress · 🟢 model done · ✅ drills done

---

## Pipeline Stages (per chapter)

```
Stage 1 — Ingest       raw/ → extracted/      dump PDF content (manual or script)
Stage 2 — Structure    extracted/ → notes/    Gemini: verbose chapter note
Stage 3 — Model        notes/ → models/       Gemini: subject mental model (run after all chapters)
Stage 4 — Drill        models/ → drills/      Gemini: understanding-test questions
Stage 5 — Gap log      self-test → gaps/      log what broke, which stage to re-run
```

**Re-run rule:** gaps trigger a re-run of Stage 2 or 3 **for that chapter only**. Never cascade.

---

## How to Use Gemini Chat

1. Open [gemini.google.com](https://gemini.google.com)
2. Upload the PDF (or paste extracted text if PDF is unreadable)
3. Paste the relevant prompt from [`_pipeline/prompts/`](./_pipeline/prompts/)
4. Copy the output into the appropriate `.md` file in `notes/` or `models/`

---

## Tooling

| Script | Purpose |
|---|---|
| [`_pipeline/scripts/pdf_extract.py`](./_pipeline/scripts/pdf_extract.py) | Extract text + tables from PDF → `extracted/` |

---

## Notes on EEEE-4076 vs EEEE-4145

`EEEE4076` (Autumn) is the core HDL theory module. `EEEE4145` (Spring) is the same content + project component.
Shared notes live in `EEEE4076_hdl_prog_logic/`. The project-specific material (deliverables, design files) lives in `EEEE4145_hdl_prog_logic_proj/`.
