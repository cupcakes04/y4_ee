# Refactoring Report: Topic 1 & Topic 2 (EEEE4138 Aerial Robotics)

**Worker:** `worker_m2_topics1_2`  
**Milestone:** M2 (Refactor Topics 1 & 2)  
**Date:** 2026-11-12  
**Target Files:**
- `modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md`
- `modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md`

---

## 1. Executive Summary

In strict accordance with directives R1, R2, and R3 from `ORIGINAL_REQUEST.md` and `PROJECT.md`, the chapters `topic_1_uav_architectures.md` and `topic_2_coordinate_frames.md` have been comprehensively refactored and verified:
1. **R1 (Pure Theory & 0 Code Dumps):** Confirmed 0 programming language blocks (Python/MATLAB) exist in either file. All code block fences are strictly reserved for Mermaid architectural diagrams.
2. **R2 (Generative UI Integration & Dense Text Restructuring):**
   - Embedded interactive visualizer widgets directly into the core pedagogical flows via standard `<iframe>` containers (`widget_1_flight_envelope.html` in Topic 1 Section 6.5; `widget_2_frames_gimbal_lock.html` in Topic 2 Section 7).
   - Decomposed dense text walls into comparative aerospace reference tables and diagnostic pedagogical cards:
     - Topic 1 Section 7.1: 5-column regulatory matrix table (VLOS, EVLOS, BVLOS).
     - Topic 1 Section 9.3: LiPo cell parameter table and `> [!WARNING]` chemical degradation callout.
     - Topic 1 Section 13: 5 structured pedagogical pitfall cards (`The Error` $\to$ `The Physics` $\to$ `The Mitigation`).
     - Topic 2 Section 4.6: Aerodynamic vector mapping table for Wind and Stability frames.
     - Topic 2 Section 6.3.3: `> [!CAUTION]` flight-software invariant card with formal mathematical fallback condition.
3. **R3 (Markdown, Mermaid & KaTeX Syntax Sanitization):**
   - Sanitized all 14 Mermaid diagrams across both files: resolved unquoted ampersands `&` and raw `\n` in Topic 1 Diag 7, escaped raw `<` HTML entity hazards in Topic 1 Diags 4 and 9, eliminated non-standard `<==>` arrows in Topic 2 Diag 3, and removed all `<br/>` tags and emojis from node labels.
   - Eliminated all 4 raw tab (`\t`) corruptions in Topic 2 KaTeX expressions (`\theta`, `\to`).
   - Removed the unsafe `\href` macro from display math `$$\boxed{...}$$` in Topic 2 Section 10, replacing it with compliant markdown navigation links.

Both verification harnesses (`audit_script.py` and `verify_textbook_and_widgets.py`) execute with 100% pass rates and 0 warnings.

---

## 2. Granular Inventory of Changes

### 2.1 `topic_1_uav_architectures.md`

| Location | Category | Previous State | Refactored State | Rationale / Benefit |
| :--- | :--- | :--- | :--- | :--- |
| **Diag 2 (lines 80-98)** | R3 / Mermaid | 6 lines with raw `<br/>`, thick link `==>` | Clean single-line descriptions, standard `-->` arrow | Eliminates parser warnings in strict CommonMark renderers |
| **Diag 3 (lines 110-121)** | R3 / Mermaid | 3 lines with raw `<br/>` | Clean single-line station descriptions | Enhances visual readability and prevents layout glitches |
| **Section 6.5 (lines 240-244)** | R2 / Widget | Plain markdown link in `[!TIP]` box | Standard responsive `<iframe>` wrapper embedding `widget_1_flight_envelope.html` | Allows instant live manipulation of battery mass fraction and hover endurance |
| **Diag 4 (lines 245-261)** | R3 / Mermaid | Raw `< m_fixed` tag error, 3 `<br/>` tags | Escaped `&lt; m_fixed`, clean labels | Prevents markdown parsers from treating `< m_fixed` as an unclosed HTML tag |
| **Diag 5 (lines 272-291)** | R3 / Mermaid | Raw `<br/>` tags, bullet characters `•` | Clean pipe-delimited summaries per UAV architecture | Complies with standard Mermaid syntax across all renderers |
| **Section 7.1 (lines 293-305)** | R2 / Text Wall | 3 dense bullet paragraphs | 5-column comparative regulatory matrix table | Transforms dense policy text into rapid-lookup exam material |
| **Diag 6 (lines 308-320)** | R3 / Mermaid | 2 lines with raw `<br/>` | Clean parenthetical force formulas | Clean diagram layout |
| **Diag 7 (lines 344-356)** | R3 / Mermaid | Unquoted labels with raw `\n` and `&` | Quoted string literals, `&` replaced with `and` | Resolves parser crash caused by unquoted special symbols |
| **Section 9.3 (lines 379-405)** | R2 / Text Wall | Bullet list of cell voltages and DoD | Structured cell parameter table + `> [!WARNING]` callout | Highlights irreversible LiPo damage mechanisms (dendrites, thermal runaway) |
| **Diag 9 (lines 441-451)** | R3 / Mermaid | Raw `< mg` tag error, 1 `<br/>` tag | Escaped `&lt; mg`, clean constraint labels | Fixes HTML entity parse error |
| **Section 13 (lines 542-572)** | R2 / Pedagogy | Unstructured numbered list | 5 pedagogical cards (`The Error`, `The Physics`, `The Mitigation`) | Standardizes teaching structure with actionable engineering mitigations |

### 2.2 `topic_2_coordinate_frames.md`

| Location | Category | Previous State | Refactored State | Rationale / Benefit |
| :--- | :--- | :--- | :--- | :--- |
| **Diag 1 (lines 25-45)** | R3 / Mermaid | 7 lines with `<br/>`, emojis `⚠️`, `✅` | Clean labels without `<br/>` or emojis | Strict standard Mermaid compliance across GitHub and VS Code |
| **Diag 2 (lines 77-91)** | R3 / Mermaid | 2 lines with raw `<br/>` | Single-line descriptions of 2D rotation and RHR | Eliminates rendering artifacts |
| **Diag 3 (lines 149-167)** | R3 / Mermaid | 2 lines with `<br/>`, invalid `<==>` arrow | Standard `<-->` bidirectional arrow, clean node labels | Eliminates syntax error in Mermaid flowchart parser |
| **Section 4.6 (lines 208-230)** | R2 / Text Wall | Paragraph descriptions of forces | Comparative vector mapping table ($D, Y, L$) | Clarifies wind and stability frame force projections and sign conventions |
| **Section 6.3.3 (lines 552-560)** | R2 / Pedagogy | Plain quote block | `> [!CAUTION]` flight-software invariant with mathematical fallback equation | Provides concrete flight-software rule ($|\theta| \ge 85^\circ$) without software code blocks |
| **Section 7 (lines 560-570)** | R2 & R3 | Corrupted tab `$	heta$`, plain link | Fixed `$\theta$`, embedded responsive `<iframe>` for `widget_2_frames_gimbal_lock.html` | Delivers inline interactive 3D gimbal visualization at exact pedagogical milestone |
| **Diag 4 (lines 572-583)** | R3 / Mermaid | Pipe hazard `||q||` in node label | Clean `norm(q)²` invariant description | Eliminates delimiter collision with Mermaid event syntax |
| **Diag 5 (lines 717-731)** | R3 / Mermaid | 1 line with `<br/>` | Clean single-line SE(3) matrix label | Standard Mermaid formatting |
| **Section 10 (lines 946-965)** | R3 / KaTeX | Unsafe LaTeX `\href` in `$$\boxed{...}$$`, 3 tab corruptions | Markdown link in `[!TIP]`, fixed tabs in `$|\theta| = 90^\circ$`, `$\cos\theta$`, `\to \infty$` | Fixes KaTeX parser security errors and corrupted equation typography |

---

## 3. Verification & Compliance Evidence

### 3.1 Course Verification Suite (`verify_textbook_and_widgets.py`)
Executed test command:
```powershell
python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py
```
Results:
- **Tier 1 (Structural Integrity):** All 16 section checks for Topic 1 and Topic 2 passed.
- **Tier 2 (Boundary & Corner Cases):** KaTeX syntax valid, widget dependencies valid.
- **Tier 3 (Invariants & Kinematics):** NED/FRD conventions, Tait-Bryan ZYX sequence verified.
- **Tier 4 (Mathematical Oracles):** SymPy/NumPy sizing and SO(3) tests passed.
- **Summary:** **74 Passed / 0 Failed / 0 Warnings (100% Pass Rate)**.

### 3.2 Deep Syntax & Static Analysis (`audit_script.py`)
Executed audit command:
```powershell
python .agents/teamwork/explorer_survey_1/audit_script.py
```
Results:
- **Code Fences:** 0 non-mermaid blocks across both files.
- **Tabs:** 0 tab characters detected in both files (previously 4 tab corruptions in Topic 2).
- **KaTeX Delimiters:** 104 `$$` delimiters in Topic 1 (balanced), 246 `$$` delimiters in Topic 2 (balanced). 0 unbalanced single `$` lines.
- **Mermaid Block Audit:** 0 issues found across all 14 diagrams (0 `<br/>` tags, 0 unescaped `<` tags, 0 unquoted special characters).
- **Generative UI Embeds:** Exactly 1 `<iframe>` tag detected in Topic 1 and 1 `<iframe>` tag in Topic 2, both formatted with the required wrapper.

---

## 4. Conclusion

Both Topic 1 and Topic 2 fully satisfy all requirements R1, R2, and R3. All code implementation blocks have been avoided, interactive visualizers are integrated inline at the optimal pedagogical points, dense text blocks are structured into scannable tables and cards, and all Mermaid and KaTeX syntax hazards have been completely eradicated.
