# Project: EEEE4138 Aerial Robotics Chapters Refactoring & Polish

## Architecture
- Target Content Directory: `d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters/`
- Target Widgets Directory: `d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\widgets/`
- Chapters Scope:
  - Topic 1: `topic_1_uav_architectures.md`
  - Topic 2: `topic_2_coordinate_frames.md`
  - Topic 3: `topic_3_rigid_body_dynamics.md`
  - Topic 4: `topic_4_forces_moments.md`
  - Topic 5: `topic_5_flight_control.md` (and legacy prototype `topic_5_flight_ctrl_2.md` if retained/cleaned)
- Verification Suite: Automated python verification script checking code block absence, valid iframe tags, Mermaid syntax, and KaTeX delimiters.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | R1-T4-CodeRemoval | Eliminate 65-line Python script (`attitude_priority_allocation`) in Topic 4 (lines 567–634) | M3 | survey |
| 2 | R1-Global-NoCode | Ensure 0 standalone programming code implementations (Python/MATLAB) exist across all chapters | M1, M5 | survey |
| 3 | R2-T1-Widget1Embed | Embed `widget_1_flight_envelope.html` in Topic 1 at Section 6.5 with `<iframe>` and fallback link | M2 | survey |
| 4 | R2-T2-Widget2Embed | Embed `widget_2_frames_gimbal_lock.html` in Topic 2 at Section 7 / 10 with `<iframe>` and fallback link | M2 | survey |
| 5 | R2-T3-Widget3Embed | Embed `widget_3_rigid_body_dynamics.html` in Topic 3 at Section 11 with `<iframe>` and fallback link | M3 | survey |
| 6 | R2-T4-Widget4Embed | Embed `widget_4_rotor_mixer_allocation.html` in Topic 4 at Section 4.7 with `<iframe>` and relocate misplaced link | M3 | survey |
| 7 | R2-T5-Widget5Embed | Embed `widget_5_cascaded_flight_control.html` in Topic 5 at Section 3.2 with `<iframe>` and fallback link | M4 | survey |
| 8 | R2-TextWalls-Breakdown | Break down dense text walls into comparison tables and callout cards (Topic 1, 2, 3, 5) | M2, M3, M4 | survey |
| 9 | R2-ASCII-Elimination | Remove any remaining ASCII / Unicode box-and-arrow diagrams (e.g. Topic 5) | M4 | survey |
| 10 | R3-T1-MermaidFix | Fix Topic 1 Diag 7 unquoted `&` / `\n` in labels, Diag 4 & 9 `<` characters | M2 | survey |
| 11 | R3-T2-KaTeXFix | Fix Topic 2 tab corruptions (`\t` in `\theta`, `\to`) and remove unsafe `\href` in `$$\boxed{...}$$` | M2 | survey |
| 12 | R3-T2-MermaidFix | Fix non-standard arrow `<==>` and `<br/>` tags in Topic 2 Mermaid diagrams | M2 | survey |
| 13 | R3-T4-MermaidFix | Fix Topic 4 Mermaid syntax error at line 742 (`DESAT -- "..." -->|Yes| SCALE`) and node condition at 545 | M3 | survey |
| 14 | R3-T3-T5-RenderAudit | Audit and ensure 100% clean KaTeX and Mermaid rendering across Topic 3 and Topic 5 | M3, M4 | survey |
| 15 | E2E-VerificationSuite | Develop and execute automated verification script confirming 0 code blocks, 5 valid iframes, 0 syntax errors | M1, M5 | survey |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | E2E Verification Infrastructure | Automated verification script (`verify_e2e.py`) validating R1, R2, R3 across all 5 chapters | none | DONE |
| M2 | Refactor Topics 1 & 2 | Implement R2, R3 in `topic_1_uav_architectures.md` and `topic_2_coordinate_frames.md` | none | DONE |
| M3 | Refactor Topics 3 & 4 | Implement R1, R2, R3 in `topic_3_rigid_body_dynamics.md` and `topic_4_forces_moments.md` | none | DONE |
| M4 | Refactor Topic 5 | Implement R2, R3 in `topic_5_flight_control.md` (and `topic_5_flight_ctrl_2.md`) | none | DONE |
| M5 | E2E Testing & Forensic Audit | Run verification suite, independent Reviewers, Challengers, and Forensic Auditor | M1, M2, M3, M4 | IN_PROGRESS |

## Code Layout
- Chapters: `modules/EEEE4138_aerial_robotics/chapters/`
  - `topic_1_uav_architectures.md` (Worker M2)
  - `topic_2_coordinate_frames.md` (Worker M2)
  - `topic_3_rigid_body_dynamics.md` (Worker M3)
  - `topic_4_forces_moments.md` (Worker M3)
  - `topic_5_flight_control.md` (Worker M4)
  - `topic_5_flight_ctrl_2.md` (Worker M4)
- Widgets: `modules/EEEE4138_aerial_robotics/widgets/` (Read-only reference)
- Automated Test Runner: `modules/EEEE4138_aerial_robotics/verify_chapters_e2e.py` (Worker M1)

## Interface Contracts
### Iframe Embedding Specification:
```html
<div align="center" style="margin: 20px 0;">
  <iframe src="../widgets/widget_X_name.html" width="100%" height="520" frameborder="0" style="border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);"></iframe>
  <p><em>Interactive Visualizer: <a href="../widgets/widget_X_name.html" target="_blank">Open in standalone tab ↗</a></em></p>
</div>
```
### Mermaid Diagram Rules:
- All labels with spaces, ampersands `&`, or punctuation MUST be enclosed in double quotes: `["Board & ESCs"]`.
- No raw `<br/>` tags inside node labels or link labels if they cause parser warnings.
- No raw unescaped `<` or `>` symbols in labels. Use text equivalents (`less than`, `greater than`) or HTML entities (`&lt;`, `&gt;`).
- Standard link arrows only: `-->`, `---|...|`, `-.->`.

### KaTeX Formula Rules:
- No raw tabs `\t` where `\theta` or `\to` was intended.
- No `\href` commands inside math display blocks `$$ ... $$`.
- Balanced math delimiters `$$` and `$` throughout.
