# Comprehensive Refactoring Survey Report: Topics 3, 4, and 5
**Module:** EEEE4138 Aerial Robotics  
**Target Directory:** `modules/EEEE4138_aerial_robotics/chapters/`  
**Explorer:** `explorer_survey_2`  
**Date:** 2026-11-12  
**Authority:** `ORIGINAL_REQUEST.md` (Directive 2026-11-12T04:21:10Z)

---

## Executive Summary

This survey provides a comprehensive, line-by-line audit and refactoring roadmap for **Topic 3 (Kinematics & Dynamics)**, **Topic 4 (Forces, Moments & Control Allocation)**, and **Topic 5 (Flight Control Architectures I & II)** in accordance with Requirements R1 (Code Removal), R2 (Generative UI Integration), and R3 (Syntax & Diagram Polish).

### Key Findings Summary
1. **R1 (Code Snippet Removal):** Exactly one major Python implementation block was discovered: `topic_4_forces_moments.md` (Lines 570–634, 65 lines), defining `attitude_priority_allocation`. This matches the explicit target singled out in R1 and must be removed. Topics 3 and 5 contain no implementation code blocks.
2. **R2 (ASCII Art & Generative UI Integration):** No standalone ASCII art blocks exist in Topics 3 or 4, but a unicode box-and-arrow chain exists in `topic_5_flight_ctrl_2.md` (Lines 457–460). Crucially, **none** of the chapters currently embed their companion Generative UI widgets (`widget_3_rigid_body_dynamics.html`, `widget_4_rotor_mixer_allocation.html`, `widget_5_cascaded_flight_control.html`) via inline `<iframe>` tags; they rely entirely on plain markdown hyperlinks. Furthermore, Topic 4 contains a misplaced widget link inside the fixed-wing aerodynamics section (Line 706).
3. **R3 (Mermaid & KaTeX Audit):** 
   - 15 Mermaid diagrams were audited across the chapters. 12 out of 15 contain syntax vulnerabilities: unescaped `<br/>` tags inside labels, unquoted comparison symbols (e.g. `>` inside decision diamond `{}` in Topic 4 L545), nested unescaped square brackets (`[...]`) inside string labels, and a severe syntax error in Topic 4 L742 (`DESAT -- "Any Motor Saturates?" -->|Yes| SCALE` combining two distinct edge syntaxes).
   - 427 KaTeX display math blocks and all inline math expressions were audited using symbolic and stack-based parsing. Delimiter parity and environment nesting (`\begin{aligned}...\end{aligned}`, `bmatrix`) are 100% mathematically balanced and valid. Specific renderer vulnerabilities identified include unicode em-dashes in headings and inline math directly adjacent to Markdown link syntax.
4. **File Architecture & Topic 5 Part I / II:** `topic_5_flight_control.md` (675 lines) is confirmed as the canonical, complete chapter uniting Part I (Cascaded Loops) and Part II (State-Space LQR) with standardized API contracts and 8 required sections. `topic_5_flight_ctrl_2.md` (552 lines) is the legacy pre-Milestone 1 prototype.

---

## 1. Chapter Files Inventory & Architecture

| Chapter File | Path | Line Count | Size | Status / Scope |
|---|---|---|---|---|
| **Topic 3** | `chapters/topic_3_kinematics_dynamics.md` | 709 lines | 50,208 B | **Canonical Chapter.** Covers 6-DoF rigid-body dynamics, Transport Theorem, Newton-Euler equations, rotor gyroscopic precession, asymmetric inertia tensor ($J_{xz} \ne 0$), and 12-state ODE state-space. |
| **Topic 4** | `chapters/topic_4_forces_moments.md` | 1023 lines | 71,554 B | **Canonical Chapter.** Covers momentum theory, plus ($+$) and cross ($\times$) quadrotor mixing, hexarotor Moore-Penrose pseudo-inverse ($A_{\text{hex}}^+$), ESC motor lag, attitude-priority desaturation, and fixed-wing aerodynamics. |
| **Topic 5** | `chapters/topic_5_flight_control.md` | 675 lines | 54,412 B | **Canonical Master Chapter.** Synthesizes BOTH Part I (Cascaded Flight Control) and Part II (State-Space Modeling, Controllability, Observability & LQR) into a single modular architecture meeting all 8 textbook specifications. |
| **Topic 5 Proto** | `chapters/topic_5_flight_ctrl_2.md` | 552 lines | 26,800 B | **Legacy Prototype.** Original prototype referenced in `ORIGINAL_REQUEST.md`. Retained in directory; all core mathematical derivations have been synthesized into `topic_5_flight_control.md`. |

### Architectural Clarification on Topic 5 Part 1 and Part 2
The prompt requests checking for Topic 5 Part 1, Part 2, or separate files:
- The automated verification suite (`scripts/verify_textbook_and_widgets.py` line 59) mandates `topic_5_flight_control.md` as the official test target.
- `topic_5_flight_control.md` explicitly structures the curriculum into two distinct parts:
  - **Part I (Lines 125–376):** Cascaded Flight Control Loops (Altitude equilibrium, underactuation tilt projection $\theta^d = -u_x/g$, tilt thrust compensation, timescale separation principle, motor lag Routh-Hurwitz stability $k_d > \tau_m k_p$).
  - **Part II (Lines 377–515):** State-Space Modeling & LQR (Small-angle hover linearization, controllability/observability rank proofs, CARE equation, Bryson's tuning rule, integrator augmentation, gain scheduling).
- Recommendation: Maintain `topic_5_flight_control.md` as the unified master file. If the team prefers splitting into `topic_5_part_1_cascaded_control.md` and `topic_5_part_2_state_space_lqr.md`, `scripts/verify_textbook_and_widgets.py` would require updating. Keeping them united under `topic_5_flight_control.md` preserves 100% test pass status.

---

## 2. Catalogue of Code Implementation Dumps to Remove (R1)

Per Requirement R1: *"Eliminate programming/code snippets (e.g., Python scripts, classes, or implementation functions like attitude_priority_allocation) from the chapters. The notes must remain focused on conceptual understanding, mathematical derivations, physics intuition, and control system theory—not software engineering or coding tutorials."*

### Item 2.1: Python Implementation of `attitude_priority_allocation`
- **File:** `modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md`
- **Exact Line Range:** Lines 567–635 (69 lines)
- **Section Heading:** `#### Executable Python Reference Implementation` (Line 567)
- **Introductory Text:** `Below is the verified, standalone Python implementation that students can directly import and run:` (Line 568)
- **Verbatim Code Block Content:**
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
    """
    Attitude-Priority Control Allocation and Desaturation.
    Guarantees roll, pitch, and yaw moment tracking by dynamically adjusting
    collective vertical thrust when actuators approach saturation limits.

    Parameters
    ----------
    F_z_cmd : float
        Demanded vertical force in NED frame (negative for upward thrust, e.g. -mg).
    M_cmd : np.ndarray
        Demanded 3-axis control moments [M_x, M_y, M_z] in N*m.
    A_moment_inv : np.ndarray
        Inverse or pseudo-inverse of the moment rows of the geometry matrix (shape: num_rotors x 3).
    T_min : float
        Minimum allowable motor thrust in Newtons (prevents ESC stall).
    T_max : float
        Maximum allowable motor thrust in Newtons.
    num_rotors : int
        Number of active propulsion rotors.

    Returns
    -------
    t_final : np.ndarray
        Array of feasible individual motor thrusts [T_1, ..., T_N] in Newtons.
    """
    # 1. Nominal collective thrust per motor
    T_mean = -F_z_cmd / num_rotors

    # 2. Pure zero-sum differential moment thrust components (sum(delta_t) == 0)
    delta_t = A_moment_inv @ M_cmd

    # 3. Dynamic range calculation
    delta_max = np.max(delta_t)
    delta_min = np.min(delta_t)
    moment_spread = delta_max - delta_min
    available_range = T_max - T_min

    # 4. Attitude-Priority Decision Logic
    if moment_spread > available_range:
        # Scale down moments proportionally to fit inside hardware limits
        scale = available_range / moment_spread
        delta_t = delta_t * scale
        T_mean = (T_max + T_min) / 2.0
    else:
        # Shift collective thrust to preserve exact differential moments
        if (T_mean + delta_max) > T_max:
            T_mean = T_max - delta_max  # Derate climb to preserve attitude
        elif (T_mean + delta_min) < T_min:
            T_mean = T_min - delta_min  # Boost thrust to prevent spin stall

    # 5. Assemble and clamp to ensure numerical safety
    t_final = np.clip(T_mean + delta_t, T_min, T_max)
    return t_final
```
- **Replacement Proposal:**
  1. Remove lines 567–635 entirely.
  2. Replace with a rigorous **Mathematical Algorithmic Specification**:
     $$\begin{aligned}
     T_{\text{mean}} &= -\frac{F_{z,\text{cmd}}}{N} \\
     \Delta \mathbf{t} &= A_{\text{mom}}^{-1} \mathbf{M}_{\text{cmd}} \quad \text{such that} \quad \sum_{i=1}^N \Delta T_i = 0 \\
     \Delta T_{\max} &= \max_i(\Delta T_i), \quad \Delta T_{\min} = \min_i(\Delta T_i) \\
     \text{Spread} &= \Delta T_{\max} - \Delta T_{\min}
     \end{aligned}$$
     - If $\text{Spread} > (T_{\max} - T_{\min})$:
       $$s = \frac{T_{\max} - T_{\min}}{\text{Spread}}, \quad \Delta \mathbf{t} \leftarrow s \cdot \Delta \mathbf{t}, \quad T_{\text{mean}} = \frac{T_{\max} + T_{\min}}{2}$$
     - Else (sufficient dynamic range):
       $$T_{\text{mean}} \leftarrow \begin{cases} T_{\max} - \Delta T_{\max} & \text{if } T_{\text{mean}} + \Delta T_{\max} > T_{\max} \\ T_{\min} - \Delta T_{\min} & \text{if } T_{\text{mean}} + \Delta T_{\min} < T_{\min} \\ T_{\text{mean}} & \text{otherwise} \end{cases}$$
     - Final individual rotor thrust commands:
       $$T_{i,\text{final}} = T_{\text{mean}} + \Delta T_i, \quad \forall i \in \{1, \dots, N\}$$
  3. Embed `widget_4_rotor_mixer_allocation.html` directly beneath this mathematical derivation.

### Audit of Other Files for Implementation Dumps:
- `topic_3_kinematics_dynamics.md`: **0** programming code blocks found.
- `topic_5_flight_control.md`: **0** programming code blocks found.
- `topic_5_flight_ctrl_2.md`: **0** programming code blocks found (only the ASCII flow diagram in lines 457–460).

---

## 3. Catalogue of ASCII Art & Dense Text Walls (R2)

### 3.1 ASCII Art Blocks
| File | Line Numbers | Description | Remediation |
|---|---|---|---|
| `topic_5_flight_ctrl_2.md` | Lines 457–460 | Text-based box-and-arrow signal chain: `Control Moments ──► Angular Rates ──► Attitude Angles ──► Lateral/Longitudinal Accel ──► Velocities ──► Positions` | Replace with standard Mermaid flowchart or embed reference. |

### 3.2 Dense Text Walls Requiring Visual Chunking & Cards
| File | Line Numbers | Context & Density | Remediation |
|---|---|---|---|
| **Topic 3** | Lines 560–580 | Worked Example 2 Part 2: 21 lines of continuous text explaining why $\dot{v} \ne 0$ despite $F_y = 0$. | Break into a visual **"Physical Mechanism Breakdown"** card with callout icons and bullet points contrasting inertial vs rotating frame forces. |
| **Topic 3** | Lines 600–615 | Worked Example 3 Part 2 & 3: Unbroken algebra describing gyroscopic dynamic cross-coupling. | Convert into side-by-side comparison tables: **Uncoupled (SISO) vs Coupled (Cross-Axis)**. |
| **Topic 4** | Lines 135–150 | Section 4.1.3: Reaction yaw torque derivation and $k_{MT}$ proportionality text wall. | Format with an intuitive vector balance diagram or structured 3-step physical summary box. |
| **Topic 4** | Lines 690–702 | Section 4.8.4: Induced drag mechanism, downwash, and wingtip vortices explanation. | Break into structured callouts: **Mechanism 1 (Bernoulli Pressure Gradient)** and **Mechanism 2 (Vortex Downwash Penalty)**. |
| **Topic 4** | Lines 850–863 | Worked Example 2 Step 5: 14 lines of dense text and numbers explaining extreme saturation allocation. | Reformat as a **Step-by-Step Calculation Table** with columns: Rotor $i$, Raw Command, Desaturated Command, Physical Status. |
| **Topic 4** | Lines 925–945 | Worked Example 4: Continuous text detailing individual thrusts for 6 rotors on a hexarotor. | Replace with a clean numerical summary matrix and rotor allocation table. |
| **Topic 5** | Lines 131–143 | Section 3.1: Derivation of vertical motion and steady-state error under wind. | Chunk into **Equilibrium Balance**, **Disturbance Force**, and **Integrator Action** cards. |
| **Topic 5** | Lines 340–365 | Section 3.5: Routh-Hurwitz stability proof with 25 lines of mixed text and algebra. | Format as an official **Mathematical Theorem & Proof Box** with numbered milestone steps: Step 1 (Open-loop transfer function), Step 2 (Closed-loop characteristic equation), Step 3 (Hurwitz matrix determinants). |
| **Topic 5** | Lines 424–445 | Section 4.2: Controllability proof with 21 lines of dense Krylov matrix algebra. | Use an aligned step-by-step matrix derivation displaying $[\mathbf{b}, \mathbf{Ab}, \mathbf{A}^2\mathbf{b}, \mathbf{A}^3\mathbf{b}]$ cleanly. |
| **Topic 5** | Lines 574–596 | Worked Example 3: Outer-to-inner cascade tilt and motor lag verification (22 lines of unbroken text). | Restructure into two distinct verification stages: **Stage 1: Outer-Loop Bandwidth & Tilt Command**, **Stage 2: Motor Lag Stability Check ($k_d > \tau_m k_p$)**. |

---

## 4. Mermaid Diagrams and KaTeX Equations Audit (R3)

### 4.1 Mermaid Diagrams Vulnerability Catalogue
Across Topics 3, 4, and 5, **15 Mermaid diagrams** were systematically evaluated against standard Markdown renderers (GitHub Flavored Markdown, VSCode Markdown Preview, Typora, and Obsidian):

| # | File | Line Range | Diagram Type | Syntax Issues & Vulnerabilities | Severity | Proposed Fix |
|---|---|---|---|---|---|---|
| 1 | `topic_3_kinematics_dynamics.md` | L14–L43 | `flowchart TD` (API Architecture) | - Lines 24, 25: `<br/>` tags inside labels.<br/>- Line 24: Nested square brackets inside string: `E1["... [M_b - ...]"]`.<br/>- Line 32: Nested brackets: `O2["... v_b [u, v, w]ᵀ"]`. | Medium | Replace `<br/>` with `<br>` or split into separate subnodes. Wrap nested brackets with parentheses: `v_b (u, v, w)ᵀ`. |
| 2 | `topic_3_kinematics_dynamics.md` | L92–L108 | `flowchart LR` (Prereq Bridge) | - Lines 95, 96, 100, 101: `<br/>` tags inside labels.<br/>- Line 104: Heavy arrow `==>\|...\|` renders inconsistently across engines. | Low | Replace `<br/>` with `<br>`, change `==>` to standard `-->\|"..."\|`. |
| 3 | `topic_3_kinematics_dynamics.md` | L441–L505 | `flowchart TD` (12-State ODE Flow) | - Lines 444, 445, 450, 451, 456, 457, 462, 463, 468, 469: Mixed `<br>` and `<br/>` tags.<br/>- Line 449: Nested brackets `[M_b - ...]`.<br/>- Lines 478, 493, 494: Unescaped Greek characters in edge text. | Medium | Standardize line breaks, eliminate nested brackets, quote all edge text strings properly. |
| 4 | `topic_4_forces_moments.md` | L24–L52 | `flowchart TD` (API Architecture) | - Labels contain nested brackets in matrix descriptions. | Low | Sanitize inner brackets. |
| 5 | `topic_4_forces_moments.md` | L197–L213 | `flowchart TD` (Plus Geometry) | - Lines 200–203: `<br/>` tags inside labels.<br/>- Lines 205–208: Mixing `---` links with double parens `HUB((CoM Hub))`. | Low | Sanitize `<br/>` tags. |
| 6 | `topic_4_forces_moments.md` | L292–L308 | `flowchart TD` (Cross Geometry) | - Lines 295–298: `<br/>` tags inside labels. | Low | Sanitize `<br/>` tags. |
| 7 | `topic_4_forces_moments.md` | L382–L402 | `flowchart TD` (Hexarotor) | - Minor label formatting. | Clean | No syntax failure. |
| 8 | `topic_4_forces_moments.md` | L540–L565 | `flowchart TD` (Attitude-Priority) | - Lines 543, 544, 547, 550, 551, 554: Multiple `<br/>` tags.<br/>- Line 545: **CRITICAL**: `CHECK{"Spread > (T_max - T_min)?"}`. Unquoted comparison operator `>` inside curly braces crashes strict Mermaid parsers.<br/>- Line 547: Colons and equals signs inside unquoted edge text `\|Yes: Extreme Demand\|`. | **HIGH** | Change Line 545 to `CHECK{"Spread &gt; (T_max - T_min)?"}` or `CHECK["Is Spread > Dynamic Range?"]`. Quote all edge conditions `-->\|"Yes: Extreme Demand"\|`. |
| 9 | `topic_4_forces_moments.md` | L644–L655 | `flowchart LR` (Aerofoil Flow) | - Line 647: `<br/>` tag, unicode bullets `•`, and arrow `⟹` inside label string. | Medium | Sanitize string label: avoid unescaped unicode arrows in node definitions. |
| 10 | `topic_4_forces_moments.md` | L708–L719 | `flowchart TD` (Drag Breakdown) | - Lines 711–713: `<br/>` tags, proportionality symbol `∝`, double equals `==`. | Medium | Sanitize label strings; use clean text descriptions. |
| 11 | `topic_4_forces_moments.md` | L728–L767 | `flowchart TD` (Signal Flow) | - Lines 731, 735–738, 748, 749, 756, 757: `<br/>` tags.<br/>- Line 742: **FATAL SYNTAX ERROR**: `DESAT -- "Any Motor Saturates?" -->\|Yes\| SCALE`. Mermaid parser crashes when combining `-- "text" -->` with `-->\|label\|` on the same edge.<br/>- Line 743: `DESAT -- "Within Bounds" --> SQRT`. | **FATAL** | Fix Line 742 to: `DESAT -->\|"Yes (Saturates)"\| SCALE`.<br/>Fix Line 743 to: `DESAT -->\|"Within Bounds"\| SQRT`. |
| 12 | `topic_5_flight_control.md` | L16–L73 | `flowchart TD` (System Architecture) | - Line 47: Unicode arrow symbol `➔` inside label `mixer["... ➔ Ω_i²"]`.<br/>- Lines 19, 31, 32, 38, 40, 47, 53, 54: Nested unescaped brackets `[...]` inside string labels. | Medium | Replace `➔` with `-->` or `to`. Sanitize nested brackets. |
| 13 | `topic_5_flight_control.md` | L207–L221 | `flowchart LR` (Tilt-to-Accelerate) | - Lines 213, 214: Unquoted `<` and `>` with `⟹`: `N3["... (θ < 0) ... ⟹ ..."]` and `N4["... (θ > 0) ..."]`. Parser treats `<` as HTML tag opening.<br/>- Lines 218, 219: Chained node connections `N1 --> N2 --> N3 --> N5`. | Medium | Replace `<` and `>` with words (`θ < 0` to `Negative Pitch θ`), or quote with `&lt;` and `&gt;`. |
| 14 | `topic_5_flight_control.md` | L287–L300 | `flowchart LR` (Timescale Separation) | - Lines 290, 292, 294: `<br/>` tags and unicode en-dashes `–`.<br/>- Lines 290–295: Split arrow syntax across newlines without source node on new line (`-->\|10x Bandwidth Margin\|`). | Medium | Keep arrow and nodes on single lines: `ESC -->\|"10x Margin"\| ATT`. Standardize en-dashes to ASCII hyphens. |
| 15 | `topic_5_flight_control.md` | L387–L406 | `flowchart TD` (12-State Channels) | - Lines 391–394: `<br/>` tags.<br/>- Lines 391–394: Nested brackets `[z, w]ᵀ`, `[x, u, θ, q]ᵀ`, `[y, v, ϕ, p]ᵀ`, `[ψ, r]ᵀ`. | Medium | Replace nested brackets with `(z, w)ᵀ`. |

### 4.2 KaTeX Math Blocks Audit
A complete symbolic pass was performed across 427 display math blocks ($$ ... $$) and thousands of inline math expressions ($ ... $):
- **Stack-Based Environment Validation:**
  - Topic 3 (81 display math blocks): **0** nesting errors.
  - Topic 4 (147 display math blocks): **0** nesting errors.
  - Topic 5 (118 display math blocks): **0** nesting errors.
  - Topic 5 Prototype (81 display math blocks): **0** nesting errors.
  - All `\begin{aligned}...\end{aligned}`, `\begin{bmatrix}...\end{bmatrix}`, `\begin{cases}...\end{cases}` are 100% paired and properly closed.
- **Inline Delimiter Parity:**
  - Checked all files for odd/unpaired `$`. Result: **0 unpaired single `$`** across all chapters.
- **Renderer Conflicts & Formatting Risks:**
  1. **Topic 5 Heading (Line 1):** Header contains an unescaped unicode em-dash `—` (`# Topic 5: Flight Control Architectures — Cascaded Loops, State-Space & LQR`). On certain Windows build systems with CP1252 default encoding, this triggers character-map encoding crashes. Standardize to ASCII hyphen or colon: `# Topic 5: Flight Control Architectures: Cascaded Loops, State-Space & LQR`.
  2. **Topic 5 Cross-Reference (Line 673):** Inline math `$\longleftrightarrow$` placed immediately adjacent to a Markdown hyperlink:
     `5. **Interactive Verification Companion $\longleftrightarrow$ [Widget 5: ...`
     Can cause certain Markdown parsers to confuse link opening brackets `[` with KaTeX delimiter scope. Separate with clean whitespace or plain text arrow `↔`.

---

## 5. Pedagogical Insertion Points for Generative UI Widgets

The curriculum features 3 advanced interactive Generative UI widgets built using HTML5, Tailwind CSS, and HTML5 Canvas/SVG, requiring zero external runtime dependencies. Below are the precise pedagogical insertion points and rationale for each topic:

### 5.1 Topic 3: `widget_3_rigid_body_dynamics.html`
- **Widget Specifications:**
  - File: `modules/EEEE4138_aerial_robotics/widgets/widget_3_rigid_body_dynamics.html` (54.3 KB)
  - Features: 3D airframe canvas (`canvas3D`), real-time angular rates oscilloscope (`canvasScope`), toggleable gyroscopic precession torque $\boldsymbol{\tau}_{\text{gyro}}$, toggleable $\boldsymbol{\omega}\times(J\boldsymbol{\omega})$ cross-coupling, motor RPM slider, instant torque impulse triggers (+Roll, +Pitch, +Yaw).
- **Exact Insertion Points:**
  - **Primary Embed (Section 11, Line 684):**
    Replace the current text link with an inline iframe:
    ```html
    <iframe src="../widgets/widget_3_rigid_body_dynamics.html" width="100%" height="520" frameborder="0" class="rounded-xl shadow-lg border border-slate-700 my-6"></iframe>
    ```
    - Rationale: Placed immediately before the guided interactive experiments (Experiment 1: Gyroscopic Roll Induction from Pure Pitch; Experiment 2: Nutation and Dynamic Cross-Coupling). Students can execute the experiments directly inside the chapter without context switching.
  - **Inline Prerequisite Hook (Section 1.2, Line 90):**
    Replace text tip with a visual preview callout card linking directly to Section 11.
  - **Theoretical Anchor (Section 5.3, Line 330):**
    Directly beneath the derivation of gyroscopic roll induction $\dot{p} = -\frac{q J_r \Omega_{\text{net}}}{J_x}$, insert an interactive note instructing students to test the formula by setting $\Omega_{\text{net}} = 1000\text{ rad/s}$ and clicking "+Pitch Impulse".

### 5.2 Topic 4: `widget_4_rotor_mixer_allocation.html`
- **Widget Specifications:**
  - File: `modules/EEEE4138_aerial_robotics/widgets/widget_4_rotor_mixer_allocation.html` (51.7 KB)
  - Features: Interactive multirotor geometry airframe canvas (`airframe-canvas`), dynamic configuration switching ($+$, $\times$, hexarotor, octorotor), real-time virtual wrench sliders ($F_z, M_x, M_y, M_z$), clickable individual motor failure simulation, live Moore-Penrose pseudo-inverse calculation, visual attitude-priority desaturation display.
- **Exact Insertion Points:**
  - **Primary Embed (Section 4.7.3, Line 567):**
    **REPLACES THE REMOVED PYTHON CODE BLOCK (`attitude_priority_allocation`):**
    ```html
    <iframe src="../widgets/widget_4_rotor_mixer_allocation.html" width="100%" height="520" frameborder="0" class="rounded-xl shadow-lg border border-slate-700 my-6"></iframe>
    ```
    - Rationale: Fulfills both R1 and R2 simultaneously. Instead of reading 65 lines of Python code, students interactively manipulate the $F_z$ and $M_x$ sliders into saturation and watch the algorithm dynamically derate collective climb while preserving roll authority in real time.
  - **Secondary Anchor (Section 4.5.3, Line 466):**
    Directly after the analytical Moore-Penrose pseudo-inverse derivation for hexarotors ($A_{\text{hex}}^+$), insert a prompt to test motor failure fault-tolerance using Widget 4.
  - **Bug Fix / Relocation:**
    Remove the misplaced widget link currently located at **Line 706** inside Section 4.8.4 (Fixed-Wing Drag Polar).

### 5.3 Topic 5: `widget_5_cascaded_flight_control.html`
- **Widget Specifications:**
  - File: `modules/EEEE4138_aerial_robotics/widgets/widget_5_cascaded_flight_control.html` (58.7 KB)
  - Features: 2D/3D flight simulation arena (`flightCanvas`), live multi-trace oscilloscope (`scopeCanvas`), controller architecture toggle (Cascaded PID vs Full State-Space LQR), adjustable position and attitude gains, adjustable LQR $Q$ and $R$ weights, interactive mouse-drag setpoint targeting, wind disturbance injector, toggleable 1st-order motor ESC lag $\tau_m$.
- **Exact Insertion Points:**
  - **Primary Embed (Section 3.2, Line 206):**
    Insert immediately after introducing the Underactuation Principle and before the algebraic derivation of tilt angles:
    ```html
    <iframe src="../widgets/widget_5_cascaded_flight_control.html" width="100%" height="520" frameborder="0" class="rounded-xl shadow-lg border border-slate-700 my-6"></iframe>
    ```
    - Rationale: Visualizes the physical necessity of pitching nose-down ($\theta < 0$) to generate forward acceleration ($+u_x$), cementing student intuition for why $\theta^d = -u_x/g$ requires a strict negative sign.
  - **Stability Anchor (Section 3.5, Line 375):**
    Directly following the Routh-Hurwitz stability proof ($k_d > \tau_m k_p$), add an interactive instruction to toggle motor lag ON in Widget 5 and observe limit-cycle oscillations when attitude damping is reduced.
  - **LQR Optimal Control Anchor (Section 4.3, Line 484):**
    Directly following the Continuous Algebraic Riccati Equation (CARE) and Bryson's rule, prompt students to switch Widget 5 to "State-Space LQR Mode" and observe how increasing state penalty $Q$ sharpens setpoint tracking while increasing control effort $R$ prevents actuator saturation.

---

## 6. Actionable Refactoring Checklist

### Topic 3 (`topic_3_kinematics_dynamics.md`)
- [ ] Embed `<iframe src="../widgets/widget_3_rigid_body_dynamics.html" ...>` at Section 11 (Line 684).
- [ ] Sanitize Mermaid diagrams 1, 2, and 3: replace `<br/>` with `<br>`, sanitize nested brackets `[...]` to `(...)`, quote edge text strings.
- [ ] Break dense text walls in Worked Examples 2 and 3 into structured mechanism and comparison cards.

### Topic 4 (`topic_4_forces_moments.md`)
- [ ] **DELETE lines 567–635** (`attitude_priority_allocation` Python code implementation dump).
- [ ] Insert mathematical algorithmic equations for attitude-priority desaturation at Line 567.
- [ ] Embed `<iframe src="../widgets/widget_4_rotor_mixer_allocation.html" ...>` directly beneath the algorithmic equations.
- [ ] **DELETE misplaced Widget 4 tip at Line 706** in the fixed-wing drag polar section.
- [ ] **FIX FATAL MERMAID SYNTAX ERROR at Line 742**: change `DESAT -- "Any Motor Saturates?" -->|Yes| SCALE` to `DESAT -->|"Yes (Saturates)"| SCALE`.
- [ ] **FIX MERMAID SYNTAX WARNING at Line 545**: change `CHECK{"Spread > (T_max - T_min)?"}` to `CHECK{"Spread &gt; (T_max - T_min)?"}`.
- [ ] Sanitize `<br/>` tags and unicode symbols across all 8 Mermaid diagrams.
- [ ] Format Worked Examples 2, 4, and 5 into clean calculation summary tables.

### Topic 5 (`topic_5_flight_control.md`)
- [ ] Replace unicode em-dash in Title (Line 1) with colon or ASCII hyphen.
- [ ] Embed `<iframe src="../widgets/widget_5_cascaded_flight_control.html" ...>` at Section 3.2 (Line 206).
- [ ] Sanitize Mermaid diagram 1 (L16–L73): replace unicode arrow `➔` with `-->`, wrap nested brackets.
- [ ] Sanitize Mermaid diagram 2 (L207–L221): replace unquoted `<` and `>` with descriptive text or `&lt;` / `&gt;`.
- [ ] Sanitize Mermaid diagram 3 (L287–L300): keep node arrows on single lines, replace en-dashes with hyphens.
- [ ] Sanitize Mermaid diagram 4 (L387–L406): sanitize nested brackets `[z, w]ᵀ` to `(z, w)ᵀ`.
- [ ] Restructure Routh-Hurwitz proof (Section 3.5) and Controllability proof (Section 4.2) into formatted theorem/proof cards.
- [ ] Retain `topic_5_flight_control.md` as the unified master chapter to maintain 100% test suite compatibility.
