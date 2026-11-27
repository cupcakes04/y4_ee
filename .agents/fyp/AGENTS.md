# EEEE4077 FYP — Agent Instructions

Project: vision-augmented (2D LiDAR + camera) dynamic-obstacle avoidance for a diff-drive robot,
using tracked/predicted obstacles inside Nav2 MPPI. Module root: `modules/EEEE4077_mechatronics_proj/`.
Proposal + defense are submitted (Nov 2026). Everything from that phase is in `archive/` — context only.

## 0. Session protocol

**Start:** read `chapters/research/brief.md` → `plan.md` (its **Now / Next / Waiting** block) → `stack.md` (what the student knows) → the `status: active` file(s) in `chapters/scratch/`. Pick up where the scratch file's last note left off. If a report in `chapters/audits/` has no Triage section, triage it first (§5). At a milestone start, read plan.md's *Parked debt* triggers.
**During:** work and notes go in the scratch file. Sources read → register. Unsourced numbers → data debt (register). Shortcuts → *to fix* in the scratch file, or plan.md *Parked debt* with a trigger.
**End:** rewrite plan.md's **Now / Next / Waiting** block and any learning-map status in stack.md. If a task is done and the user agrees, promote it (see `chapters/scratch/README.md`), add one dated line to the `ws/README.md` log, and update the brief's decision log if a decision changed. Leave the scratch file with a clear "next step" line if not done.

## 1. Zones

| Path | What | Agent rights |
|---|---|---|
| `chapters/scratch/` | Shared work-in-progress, one file per task. Promoted into research/library/ws when done, then deleted (see its README) | Read/write freely. **Default place for unfinished work**  (also included an answer.md that user supplies requested cmd runs and answers exercises by ai (defferent from grill/ask in chat))|
| `chapters/research/` | Engineering truth. Small set of living docs (see its README). Only settled content, promoted from scratch | Read/write, negotiate with user |
| `chapters/library/` | Sources: register, cards, PDFs. Only place a citation can come from. | Read/write, strict rules below |
| `ws/` | Colcon workspace (project code) + learn↔build log | Read/write |
| `chapters/deliverables/` | Future outward outputs (midterm slides, thesis, poster) | Write only when asked |
| `raw/` | University requirements, rubrics, spec. Ground truth for *structure* only | Read-only |
| `concepts/`, `chapters/meetings/` | User's own learning notes and meeting records | **Never edit.** Reading is fine |
| `archive/2026-11_proposal/` | Old proposal-phase docs. Known inconsistencies, unsourced numbers | Read for context. **Never cite, never copy numbers from it as fact** |
| `chapters/audits/` | Outside audit reports, one per audit (§5) | Append the Triage section only. Never write a report or run an audit |

## 2. Claim tags (applies to `chapters/research/` and anything derived from it)

Every number or non-obvious factual claim carries one tag:

- `[L#]` — from a library entry (add `§`/page when it matters). Entry status decides if it can be shown (see library README).
- `[M#]` — measured by us; points to a row in `chapters/research/results.md` that names the script/log.
- `[E]` — engineering judgement, design choice, or common knowledge. Honest label, no citation needed.

Untagged numbers do not go in. If a number is needed but unsourced, tag `[E]` and add it to the debt list in `chapters/library/register.md`.
**Never fabricate data or results.** If something is unsourced or unmeasured, omit it or label it — don't invent it.

## 3. Engineering stance

- "SOTA" here = industry-grade engineering rigour, not academic novelty: a properly tuned stock baseline, fair comparisons, reuse standard packages (Nav2, nav2_collision_monitor, standard KF), claims backed by measurement.
- Prefer the smallest thing that can be measured. Add complexity only when a measured failure demands it.
- Modular by interface: modules talk through defined ROS messages so any one can be replaced by ground truth or a mock.
- Perception (detection + 2D tracking, domain adaptation, lighting) is the **user's specialty and is assumed solved**. Agents don't design detectors; in sim, a synthetic detector stands in. Fusion (box + LiDAR → metric track) *is* in scope.
- Hardware is a personal goal, off the thesis critical path. Nothing assessed may depend on it.
- C++ only where Nav2 forces it (the MPPI critic plugin). Everything else Python unless measured too slow.

## 4. Working with the user

- The user must understand everything that ships. Learn↔build loop: explain the concept briefly, then build the smallest piece, then the user runs/reviews it (see `ws/README.md`).
- Build first, literature just-in-time: read a source only when it changes a decision or settles a debt; log it in the register as you go. Nav2 docs, source code and tutorials count as literature (raw/thesis/thesis_guide.md).
- Diagrams (flows, architecture, lifecycles, timelines) in **Mermaid** code blocks, top-down unless a flow is clearer left-right. No ASCII-art diagrams.
- Meeting records are context, not rules. Only the spec (`raw/general/FYP Specification…`) is binding.
- Figures are generated by scripts from logged data (matplotlib), never hand-made. Map `raw/` requirements to content only when a deliverable is being prepared.
- The user handles git (add/commit/push). Don't commit. The repo is shared by all modules and the user commits **per module, separately**: never assume the FYP folder is committed just because the tree looks clean elsewhere. Check `git log -- <path>` before deleting anything.
- Understanding checks are situational (see `ws/README.md` loop step 4): ask 3–5 predict/debug/explain questions via `chapters/scratch/answer.md` when a concept is load-bearing; grade bluntly; don't quiz routine steps.
- The user can verify things directly (open a PDF, screenshot a chart, run a sim). Ask them when that's cheaper than guessing.
- Ask the user to fetch paywalled PDFs; fetch open-access ones (arXiv, docs, GitHub) yourself.
- Be blunt about what works and what doesn't. Rubrics in `raw/` set structure, never scope.

## 5. Audits

An outside agent, on purpose **another model** (its blind spots differ), reads the whole module in a fresh session and writes one report to `chapters/audits/<YYYY-MM-DD>.md`. The user gives it [`audit.md`](audit.md). The agent never runs an audit itself.

- **When:** after M2 (before the wk-16 midterm meeting) and after M4 (before the final runs). The user may call one anytime.
- **The prompt never says what to look for**, only how to write a finding down (file and line). Steering the auditor makes it look where we would.
- **The report is a perspective, not a to-do list.** Triage it at the next session start: check against the code and docs only the findings that would change the next milestone or a decision, give the user a short triage in chat, and append a `## Triage` section to the report: each finding *accepted*, *kept* or *rejected*, one line with a reason. The user decides what becomes work.
- **Only the obligations move out.** Accepted findings become work like any other (scratch file, plan.md, brief decision log). Each kept finding becomes one *Parked debt* row in plan.md with its trigger and a link to the report section. A report is read once, at triage, never again by habit.
