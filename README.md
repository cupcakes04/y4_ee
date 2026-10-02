# Y4 Study System — MEng Mechatronics

> **Core loop:** confused about concept → Gemini session → `produce_note.md` → paste into `concepts/` → done.

---

## Subjects

| Folder | Code | Subject | Credits | Semester | Status |
|---|---|---|---|---|---|
| [EEEE3116_adv_eng_math](./modules/EEEE3116_adv_eng_math/) | EEEE-3116 | Advanced Engineering Mathematics | 10 | Autumn | 🟡 |
| [EEEE4064_adv_control_system](./modules/EEEE4064_adv_control_system/) | EEEE-4064 | Advanced Control System Design | 10 | Autumn | 🟡 |
| [EEEE4076_hdl_prog_logic](./modules/EEEE4076_hdl_prog_logic/) | EEEE-4076 | HDL for Programmable Logic | 10 | Autumn | ⬜ |
| [EEEE4077_mechatronics_proj](./modules/EEEE4077_mechatronics_proj/) | EEEE-4077 | Mechatronics Industrial Project | 40 | Full Year | ⬜ |
| [EEEE4133_ai_intelligent_sys](./modules/EEEE4133_ai_intelligent_sys/) | EEEE-4133 | Artificial Intelligence & Intelligent Systems | 20 | Spring | ⬜ |
| [EEEE4138_aerial_robotics](./modules/EEEE4138_aerial_robotics/) | EEEE-4138 | Aerial Robotics | 10 | Autumn | ⬜ |
| [EEEE4145_hdl_prog_logic_proj](./modules/EEEE4145_hdl_prog_logic_proj/) | EEEE-4145 | HDL for Programmable Logic with Project | 10 | Spring | ⬜ |
| [MMME4127_digital_manufacturing](./modules/MMME4127_digital_manufacturing/) | MMME-4127 | Digital Manufacturing | 10 | Spring | ⬜ |

Status: ⬜ not started · 🟡 concepts in progress · 🟢 map generated · ✅ drills done

---

## Folder Structure (per subject)

```
modules/{SUBJECT}/
├── raw/              immutable source PDFs and sim files — never edit
├── chapters/         one .md per lecture (flat) — dense reference notes from PDF
│   ├── L01_introduction.md         one file per PDF (typical)
│   └── L05_controllability/        subfolder only if multiple PDFs for one chapter (edge case)
├── concepts/         one .md per concept (the primary output of every session)
├── maps/             subject map — derived from concepts/, not planned upfront
└── drills/           understanding-test questions (generated from map, touch pre-exam only)
```

**Flow:** `raw/*.pdf` → (attach to Gemini + `chapter.md` prompt) → `chapters/{chNN}/` → skim Concept Index → deep sessions → `concepts/`

---

## The Learning Loop

```
0. New lecture PDF available
        ↓
   Attach PDF to Gemini + paste chapter.md prompt → get chapter note
        ↓
   Save to modules/{SUBJECT}/chapters/{chNN}/{title}.md
        ↓
   Skim the Concept Index — flag anything you can't explain
        ↓
1. Confused about a specific concept (from chapter note or elsewhere)
        ↓
2. [if tangled] paste untangle.md prompt → Gemini decomposes into ordered sub-concepts
        ↓
3. Learn in Gemini — ask questions, upload pics, iterate freely
        ↓
4. Paste produce_note.md prompt → Gemini produces a concept note
        ↓
5. Copy output → save as modules/{SUBJECT}/concepts/{concept_name}.md
        ↓
6. Promote status: draft → solid → linked (once all depends-on links are verified)
        ↓
7. Periodically: paste map.md prompt → update modules/{SUBJECT}/maps/subject_map.md
```

**Re-run rule:** if a gap is logged (Open/Unresolved in a concept file), re-run Step 3–5 for that concept only. Never cascade.

---

## Prompts (use these in Gemini Chat)

| Prompt | When to use |
|---|---|
| [`chapter.md`](./pipeline/prompts/chapter.md) | **Per PDF** — attach the lecture PDF to Gemini, get a dense chapter note |
| [`produce_note.md`](./pipeline/prompts/produce_note.md) | **Every session** — end of learning, produces the concept note |
| [`untangle.md`](./pipeline/prompts/untangle.md) | **Start of session** — when you're tangled and don't know where to start |
| [`map.md`](./pipeline/prompts/map.md) | **Periodically** — after accumulating several concepts, to build the subject map |
| [`drill.md`](./pipeline/prompts/drill.md) | **Pre-exam** — generates understanding-test questions from your map |

---

## Concept File Naming

Use `snake_case_concept_name.md`. Name by the concept, not the chapter or slide number.

**Good:** `pid_derivative_noise.md`, `z_transform_roc.md`, `fpga_lut_routing.md`
**Bad:** `ch03_section2.md`, `lecture5_part1.md`

Cross-subject dependency links use relative paths from the concept file:
```markdown
**Depends on:** → [z_transform_roc](../../EEEE3116_adv_eng_math/concepts/z_transform_roc.md)
```

---

## Notes on EEEE-4076 vs EEEE-4145

`EEEE4076` (Autumn) is the core HDL theory module. `EEEE4145` (Spring) is the continuation with project.
Core HDL concepts live in `modules/EEEE4076_hdl_prog_logic/concepts/`. Project deliverables in `modules/EEEE4145_hdl_prog_logic_proj/`.

---

## Optional: PDF Extraction (pre-session)

For heavily visual PDFs, run before the Gemini session to get searchable text:

```powershell
pip install pymupdf tabulate
python pipeline/scripts/pdf_extract.py "path\to\lecture.pdf"
# outputs: path\to\lecture.txt — paste into Gemini alongside your question
```
