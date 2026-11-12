# Handoff Report: Survey of Topics 3, 4, and 5
**Agent:** `explorer_survey_2`  
**Working Directory:** `d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_2`  
**Parent Agent:** `orchestrator_2` (`1bd01c7b-be2b-4321-b6ed-533a20ac3644`)  
**Date:** 2026-11-12  
**Handoff Type:** Hard Handoff (Investigation & Survey Complete)

---

## 1. Observation

Direct, empirical observations recorded from inspecting the codebase, chapters, scripts, and test suite:

### 1.1 File Architecture and Scope
* **Tool Command:** `list_dir` on `d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters`
* **Observation:**
  - `topic_3_kinematics_dynamics.md`: 709 lines, 50,208 bytes.
  - `topic_4_forces_moments.md`: 1,023 lines, 71,554 bytes.
  - `topic_5_flight_control.md`: 675 lines, 54,412 bytes.
  - `topic_5_flight_ctrl_2.md`: 552 lines, 26,800 bytes.
* **Tool Command:** `view_file` on `modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py` (Lines 54–60):
  ```python
  MANDATORY_CHAPTERS = [
      "topic_1_uav_architectures.md",
      "topic_2_coordinate_frames.md",
      "topic_3_kinematics_dynamics.md",
      "topic_4_forces_moments.md",
      "topic_5_flight_control.md",
  ]
  ```
  `topic_5_flight_control.md` contains both Part I (`## 3. Part I: Cascaded Flight Control Loops`, Line 125) and Part II (`## 4. Part II: State-Space Modeling, Controllability, Observability & LQR`, Line 377). `topic_5_flight_ctrl_2.md` is the original prototype.

### 1.2 Code Implementation Blocks (R1 Violation)
* **File:** `modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md`
* **Observation:** Line 567 heading `#### Executable Python Reference Implementation`, followed at lines 570–634 by a 65-line Python code block:
  ```python
  import numpy as np

  def attitude_priority_allocation(
      F_z_cmd: float,
      M_cmd: np.ndarray,
      A_moment_inv: np.ndarray,
      T_min: float = 0.5,
      T_max: float = 15.0,
      num_rotors: int = 4
  ) -> np.ndarray:
      ...
  ```
  This is the sole implementation dump across Topics 3, 4, and 5. Topic 3 and Topic 5 contain zero code implementation blocks.

### 1.3 ASCII Art & Missing Generative UI Embeds (R2)
* **Observation 1 (ASCII block):** `chapters/topic_5_flight_ctrl_2.md` Lines 457–460 contains:
  ```
  Control Moments ──► Angular Rates ──► Attitude Angles ──► Lateral/Longitudinal Accel ──► Velocities ──► Positions
  (δMₓ, δMᵧ)          (p, q)            (φ, θ)              (u̇, v̇)                          (u, v)        (x, y)
  ```
* **Observation 2 (Generative UI Embeds Missing):**
  - All 3 widgets exist in `modules/EEEE4138_aerial_robotics/widgets/`:
    - `widget_3_rigid_body_dynamics.html` (54.3 KB)
    - `widget_4_rotor_mixer_allocation.html` (51.7 KB)
    - `widget_5_cascaded_flight_control.html` (58.7 KB)
  - Currently, **zero** `<iframe>` embeds exist across Topics 3, 4, and 5. Only markdown text hyperlinks are present:
    - Topic 3: Line 90 and Line 684 (`👉 [Launch Widget 3: ...](../widgets/widget_3_rigid_body_dynamics.html)`)
    - Topic 4: Line 16, Line 706, Line 1023. Notice Line 706 is misplaced under Fixed-Wing Drag Polar.
    - Topic 5: Line 8, Line 205, Line 673.

### 1.4 Mermaid Diagram Syntax Vulnerabilities (R3)
* **Observation:** 15 Mermaid diagrams audited across the chapters:
  - **Fatal syntax error in Topic 4 (Line 742):**
    `DESAT -- "Any Motor Saturates?" -->|Yes| SCALE`
    Combines `-- "text" -->` with `-->|label|` on the same edge, crashing standard Mermaid renderers.
  - **Syntax warning in Topic 4 (Line 545):**
    `CHECK{"Spread > (T_max - T_min)?"}`
    Unquoted comparison operator `>` inside decision braces.
  - **Tags inside labels:** 12 diagrams across Topics 3, 4, 5 use `<br/>` tags, unescaped nested brackets `[...]`, or unicode arrows (`➔`, `–`, `⟹`).

### 1.5 KaTeX Math Blocks Status
* **Tool Command:** `python stack_validate_math.py` and `python check_inline_math.py`
* **Observation:**
  - Topic 3: 81 display math blocks, 0 nesting errors, 0 unclosed `$`.
  - Topic 4: 147 display math blocks, 0 nesting errors, 0 unclosed `$`.
  - Topic 5: 118 display math blocks, 0 nesting errors, 0 unclosed `$`.
  - Topic 5 Proto: 81 display math blocks, 0 nesting errors, 0 unclosed `$`.
  - Topic 5 Line 1 contains an unescaped unicode em-dash `—` in `# Topic 5: Flight Control Architectures — Cascaded Loops, State-Space & LQR` that failed encoding on Windows CP1252 stdout.
  - Existing verification suite `python scripts/verify_textbook_and_widgets.py` passes 74/74 tests (100%).

---

## 2. Logic Chain

1. **R1 Elimination:** Observation 1.2 confirms that `topic_4_forces_moments.md` (Lines 567–634) contains a 65-line Python script for `attitude_priority_allocation`. Since R1 explicitly demands removing programming/code snippets and keeping theory pure, this block must be removed.
2. **Replacing Implementation with Theory & UI:** Rather than leaving a gap, replacing lines 567–634 with the exact mathematical formulation of the desaturation logic and embedding `widget_4_rotor_mixer_allocation.html` directly satisfies both R1 (theory purity) and R2 (visual Generative UI integration).
3. **Resolving Missing Embeds:** Observation 1.3 shows all three widgets (`widget_3`, `widget_4`, `widget_5`) are fully built and validated (50–58 KB each), but chapters only feature markdown hyperlinks. Replacing or supplementing these hyperlinks with responsive `<iframe src="../widgets/widget_X_....html" width="100%" height="520" frameborder="0"></iframe>` blocks satisfies R2 and fulfills the acceptance criteria.
4. **Relocating Misplaced Widget 4 Link:** Observation 1.3 shows Widget 4 (multirotor control allocation sandbox) is currently linked at Line 706 inside the fixed-wing aerofoil drag polar section. Moving the primary embed to Section 4.7 (actuator desaturation) aligns the interactive simulation with its exact pedagogical topic.
5. **Fixing Mermaid Parser Crashes:** Observation 1.4 confirms a fatal syntax error in Topic 4 Line 742 (`DESAT -- "Any Motor Saturates?" -->|Yes| SCALE`) and syntax warnings in Topic 4 Line 545 (`CHECK{"Spread > (T_max - T_min)?"}`). Correcting these to standard Mermaid syntax guarantees 100% crash-free rendering across GitHub, VSCode, and web renderers, satisfying R3.
6. **Architecture Invariance:** Observation 1.1 proves that `topic_5_flight_control.md` already unifies Part I and Part II, and is hard-coded as the mandatory chapter in `scripts/verify_textbook_and_widgets.py`. Keeping `topic_5_flight_control.md` intact avoids breaking the automated test suite while delivering complete coverage.

---

## 3. Caveats

- **Topic 5 Prototype File:** `topic_5_flight_ctrl_2.md` remains in the directory. It is not currently included in `MANDATORY_CHAPTERS` in `scripts/verify_textbook_and_widgets.py`. We recommend leaving it untouched or archiving it once the team confirms `topic_5_flight_control.md` contains all desired elements.
- **Iframe Height & Responsive Display:** Standard markdown renderers (like GitHub) sanitize or strip `<iframe>` tags for security reasons, displaying raw text or blank space, while local web servers and preview tools render them seamlessly. Fallback interactive text links must be preserved alongside `<iframe>` embeds to ensure graceful degradation.

---

## 4. Conclusion

The survey of Topics 3, 4, and 5 is complete with concrete, line-level findings:
1. **Topic 3 (`topic_3_kinematics_dynamics.md`):** Zero code dumps. Needs iframe embed for `widget_3_rigid_body_dynamics.html` at Section 11 (Line 684), `<br/>` tag sanitization in 3 Mermaid diagrams, and visual chunking of Worked Examples 2 and 3.
2. **Topic 4 (`topic_4_forces_moments.md`):** Must delete 68 lines of Python code at Lines 567–634 (`attitude_priority_allocation`), replace with mathematical equations, embed `widget_4_rotor_mixer_allocation.html` at Line 567, fix fatal Mermaid syntax error at Line 742, fix unquoted `>` at Line 545, and delete misplaced widget tip at Line 706.
3. **Topic 5 (`topic_5_flight_control.md`):** Canonical master file combining Part I and Part II. Zero code dumps. Needs iframe embed for `widget_5_cascaded_flight_control.html` at Section 3.2 (Line 206), sanitization of 4 Mermaid diagrams, and heading em-dash fix.

All actionable items have been documented in `d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_2\survey_report.md`.

---

## 5. Verification Method

To independently verify all findings in this report:
1. **Verify Existing Test Suite Pass:**
   ```powershell
   python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py
   ```
   (Expected: 74/74 tests pass, confirming baseline integrity).
2. **Verify Python Code Snippet in Topic 4:**
   ```powershell
   python -c "content = open('modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md', encoding='utf-8').read(); print('attitude_priority_allocation' in content)"
   ```
   (Expected: `True` at lines 570–634).
3. **Verify Fatal Mermaid Syntax Error in Topic 4:**
   Inspect lines 740–745 in `modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md` to see `DESAT -- "Any Motor Saturates?" -->|Yes| SCALE`.
4. **Verify KaTeX Environment Balancing:**
   ```powershell
   python .agents/teamwork/explorer_survey_2/stack_validate_math.py
   ```
   (Expected: 0 nesting errors across all 4 files).
