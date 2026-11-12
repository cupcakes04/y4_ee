# Survey & Audit Report: Topic 1 & Topic 2 (EEEE4138 Aerial Robotics)

**Surveyor:** `explorer_survey_1`  
**Working Directory:** `d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_1`  
**Date:** 2026-11-12  
**Target Scope:**
- `modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md`
- `modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md`
- Companion Widgets: `widget_1_flight_envelope.html`, `widget_2_frames_gimbal_lock.html`

---

## 1. Executive Summary & File Inventory

This survey report provides an exhaustive, line-by-line audit of Topic 1 and Topic 2 chapter files in accordance with the authoritative directives in `ORIGINAL_REQUEST.md` (specifically requirements R1, R2, and R3).

| Metric | Topic 1: UAV Architectures | Topic 2: Coordinate Frames |
| :--- | :--- | :--- |
| **File Path** | `modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md` | `modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md` |
| **File Size / Lines** | 37,612 bytes / 573 lines | 68,127 bytes / 992 lines |
| **Mermaid Blocks** | 9 diagrams | 5 diagrams |
| **Code Implementation Dumps (R1)** | **0 lines** (Clean) | **0 lines** (Clean) |
| **ASCII Box Art (R2)** | **0 instances** (Mermaid already used) | **0 instances** (Mermaid already used) |
| **Generative UI `<iframe>` Embeds (R2)** | **0 embedded** (3 plain markdown links) | **0 embedded** (3 plain markdown links + 1 broken LaTeX href) |
| **KaTeX Math Blocks ($$)** | 52 blocks (104 delimiters, 100% balanced) | 161 blocks (246 delimiters, balanced) |
| **KaTeX Syntax Errors / Tabs (R3)** | **0 errors** | **4 critical tab corruptions + 1 unsafe `\href`** |
| **Mermaid Syntax Hazards (R3)** | 6 diagrams with `<br/>`, 1 unquoted with `\n` & `&`, 2 unescaped `<` tags | 5 diagrams with `<br/>`, 1 invalid `<==>` arrow, emojis in nodes |
| **Companion Widget** | `widgets/widget_1_flight_envelope.html` (41.1 KB) | `widgets/widget_2_frames_gimbal_lock.html` (55.1 KB) |

---

## 2. Code Snippet & Implementation Block Audit (R1)

### Directive R1 Review
> *"Eliminate programming/code snippets (e.g., Python scripts, classes, or implementation functions like `attitude_priority_allocation`) from the chapters. The notes must remain focused on conceptual understanding, mathematical derivations, physics intuition, and control system theory—not software engineering or coding tutorials."*

### Detailed Audit Results
1. **Topic 1 (`topic_1_uav_architectures.md`)**:
   - All fenced code blocks evaluated:
     - Lines 25–55: ````mermaid` (Architecture & API flowchart)
     - Lines 80–98: ````mermaid` (Prerequisite bridge flowchart)
     - Lines 110–121: ````mermaid` (Actuator disc streamtube stations)
     - Lines 245–261: ````mermaid` (Battery mass endurance regimes)
     - Lines 272–291: ````mermaid` (Airframe taxonomy)
     - Lines 312–324: ````mermaid` (Four forces of steady flight)
     - Lines 348–360: ````mermaid` (Powertrain electrical architecture)
     - Lines 408–434: ````mermaid` (Sensor suites & EKF fusion)
     - Lines 442–452: ````mermaid` (Flight envelope constraints)
   - **Finding:** **ZERO** software implementation blocks, classes, Python functions, or MATLAB scripts exist.
   - **Action Required:** None. Topic 1 is completely clean under R1.

2. **Topic 2 (`topic_2_coordinate_frames.md`)**:
   - All fenced code blocks evaluated:
     - Lines 25–45: ````mermaid` (Aerospace coordinate hierarchy)
     - Lines 77–91: ````mermaid` (2D planar rotation & Right-Hand Rule)
     - Lines 149–167: ````mermaid` (Inertial NED vs Body FRD frames)
     - Lines 563–574: ````mermaid` (Unit quaternion geometry on $\mathbb{S}^3$)
     - Lines 708–722: ````mermaid` (Homogeneous SE(3) transformation)
   - **Finding:** **ZERO** software implementation blocks, classes, Python functions, or MATLAB scripts exist.
   - **Action Required:** None. Topic 2 is completely clean under R1.

*(Note: The reference snippet `attitude_priority_allocation` mentioned in R1 resides in `topic_4_forces_moments.md:573`, not in Topics 1 or 2).*

---

## 3. ASCII Art, Dense Text Walls & Visual Enhancement (R2)

### 3.1 ASCII Box-and-Arrow Art Audit
- Neither Topic 1 nor Topic 2 contains ASCII box-and-arrow diagrams (e.g., `+----+`, `|    |`, `----->`).
- All architectural and signal flow representations are already expressed using Mermaid or Markdown tables.

### 3.2 Dense Text Wall Identification & Restructuring Plan

#### In Topic 1 (`topic_1_uav_architectures.md`):

1. **Section 7.1: Regulatory & Operational Regimes (Lines 293–305)**
   - *Current State:* 3 long bullet points describing VLOS, EVLOS, BVLOS regulations, pilot observation requirements, and fail-safe sensors.
   - *Deficiency:* Dense paragraphs that students skim rather than absorb for exam questions.
   - *Recommended Enhancement:* Reformat as a crisp, comparative aerospace regulatory matrix table:
     ```markdown
     | Operational Category | Pilot Sight Baseline | Maximum Range / Altitude | Primary Separation Mechanism | Mandatory Avionics & Failsafes |
     | :--- | :--- | :--- | :--- | :--- |
     | **VLOS** (Visual Line of Sight) | Direct, unaided visual contact | Range $\le 500\,\text{m}$, AGL $\le 120\,\text{m}$ ($400\,\text{ft}$) | Pilot "see-and-avoid" | Barometer, basic telemetry, manual override |
     | **EVLOS** (Extended Visual Line of Sight) | Chained visual observers along corridor | Extended via visual relays | Observer radio situational reports | Low-latency voice/data comms, return-to-home |
     | **BVLOS** (Beyond Visual Line of Sight) | Zero direct optical visibility | Unlimited (mission envelope bound) | Automated onboard Sense-and-Avoid (SAA) | ADS-B In/Out, Radar/Optical transponders, Geofencing, Auto-RTH |
     ```

2. **Section 9.3: Lithium-Polymer (LiPo) Batteries & Depth of Discharge (Lines 383–400)**
   - *Current State:* Dense bullet list outlining cell voltages ($3.7\text{V}, 4.2\text{V}, 3.85\text{V}, 3.2\text{V}$), series/parallel notation ($3S, 4S, 6S$), C-rating formula, and the 80% DoD rule.
   - *Recommended Enhancement:* Structure cell parameters into a quick-reference table and enclose the $DoD > 80\%$ failure mechanism in a high-visibility `> [!WARNING]` callout box detailing the irreversible chemical consequences (lithium dendrites, internal resistance spike, thermal runaway).

3. **Section 13: Common Student Pitfalls & Engineering Traps (Lines 544–556)**
   - *Current State:* Numbered list with bold titles followed by explanation paragraphs.
   - *Recommended Enhancement:* Upgrade to formatted pedagogical diagnostic cards (`The Error` $\to$ `The Physics` $\to$ `The Engineering Solution`) matching the proven pedagogical style in Topic 2.

#### In Topic 2 (`topic_2_coordinate_frames.md`):

1. **Section 4.6: Stability & Wind Frames (Lines 208–226)**
   - *Current State:* Dense descriptive text defining $\alpha$ (angle of attack), $\beta$ (sideslip), and coordinate orientations for $\mathcal{F}_s$ and $\mathcal{F}_w$.
   - *Recommended Enhancement:* Add an inline comparative vector table summarizing how Lift ($L$), Drag ($D$), and Sideforce ($Y$) map cleanly onto axes $-\mathbf{k}_w$, $-\mathbf{i}_w$, and $+\mathbf{j}_w$.

2. **Section 6.3.3: Loss of Degree of Freedom & Failure Invariant (Lines 543–551)**
   - *Current State:* Plain quote block mentioning $85^\circ$ clamping.
   - *Recommended Enhancement:* Formalize into an explicit flight-software invariant box (`> [!CAUTION]`) showing the exact conditional algorithm: if $|\theta| \ge 85^\circ$, switch the state estimator from Euler integration to quaternion kinematics $\dot{\mathbf{q}} = \frac{1}{2}\mathbf{q}\otimes\bar{\boldsymbol{\omega}}_b$.

---

## 4. Mermaid Diagrams & KaTeX Equations Technical Audit (R3)

### 4.1 KaTeX Math Block Audit

#### Topic 1 (`topic_1_uav_architectures.md`):
- **Display Math ($$):** 52 equations (104 delimiters), 100% paired and balanced.
- **Inline Math ($):** 100% balanced across all lines.
- **Tab Characters:** 0 tab characters detected.
- **Syntax Quality:** Fully compliant and verified with SymPy/NumPy oracle in `verify_textbook_and_widgets.py`.

#### Topic 2 (`topic_2_coordinate_frames.md`):
- **Display Math ($$):** 161 equations (246 delimiters), balanced.
- **Inline Math ($):** Balanced.
- **CRITICAL DEFECTS IDENTIFIED (Tab Character Corruptions):**
  Four instances of literal horizontal tab characters (`\t`, ASCII 0x09) were injected where LaTeX `\t` was intended, corrupting KaTeX parsing:
  1. **Line 560:**
     - *Corrupted:* `> ... watch how Euler angles lock at $	heta = \pm 90^\circ$ while ...` (literal tab before `heta`)
     - *Render Failure:* KaTeX fails to parse `	heta` as `\theta`.
     - *Correction:* `$\theta = \pm 90^\circ$`
  2. **Line 946:**
     - *Corrupted:* `>    Pitching the aircraft to $|	heta| = 90^\circ$ causes ...` (literal tab before `heta`)
     - *Correction:* `$|\theta| = 90^\circ$`
  3. **Line 946:**
     - *Corrupted:* `The matrix $W_\eta$ has $\cos	heta$ in the denominator ...` (literal tab before `heta`)
     - *Correction:* `$\cos\theta$`
  4. **Line 946:**
     - *Corrupted:* `causing Euler rates to blow up to infinity ($\dot{\phi}, \dot{\psi} 	o \infty$).` (literal tab before `o \infty`)
     - *Correction:* `(\dot{\phi}, \dot{\psi} \to \infty)`

- **CRITICAL DEFECT: Unsafe LaTeX `\href` in Display Math (Line 941)**:
  - *Corrupted:* `$$\boxed{\text{Open Companion Widget: } \textbf{\href{../widgets/widget_2_frames_gimbal_lock.html}{widget\_2\_frames\_gimbal\_lock.html}}}$$`
  - *Render Failure:* Standard KaTeX builds disable `\href` by default for XSS security. In standard markdown renderers, this produces an `#ERROR: \href not allowed` or blank box.
  - *Correction:* Replace with standard Markdown hyperlink and native `<iframe>` container.

---

### 4.2 Mermaid Diagrams Audit & Hazards Catalogue

Modern Markdown viewers and KaTeX renderers (e.g., GitHub, VS Code, GitBook) crash or produce syntax error warnings when Mermaid diagrams contain raw `<br/>` tags, unquoted labels with `&` or `\n`, or unescaped `<` characters.

#### Topic 1 (`topic_1_uav_architectures.md`):

| Diagram # | Lines | Topic / Title | Detected Syntax Hazards | Specific Hazard Detail | Mandatory Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Diag 1** | 25–55 | Architecture & API Contract | Mild | Quoted brackets `topol ∈ {quad_plus, ...}` | Verify quote closure (currently valid). |
| **Diag 2** | 80–98 | Prerequisite Bridge | **HIGH** | 6 lines with `<br/>`, thick link `==>|...|` | Lines 83, 84, 85, 89, 90, 91 contain `<br/>`. Replace with multiline strings or sub-nodes; sanitize `==>` into `-->`. |
| **Diag 3** | 110–121 | 1D Actuator Disc Stations | **MEDIUM** | 3 lines with `<br/>` | Lines 112, 114, 116 contain `<br/>` in stations `S_INF`, `S_DISC`, `S_WAKE`. |
| **Diag 4** | 245–261 | Battery Mass Regimes | **CRITICAL** | 3 lines with `<br/>`, **Unescaped `<`** | Line 247: `subgraph REGIME1["1. Linear Regime (m_bat < m_fixed)"]` has raw `<`. Parsers treat `< m_fixed` as an unclosed HTML tag! Line 248, 251, 254 have `<br/>`. Replace `<` with `&lt;` or text `m_bat <= m_fixed`. |
| **Diag 5** | 272–291 | UAV Taxonomy | **HIGH** | 4 lines with `<br/>` and bullet points `•` | Lines 276–279 have bullet characters and `<br/>` inside nodes `FW`, `SR`, `MR`, `HY`. Remove bullets and `<br/>`. |
| **Diag 6** | 312–324 | Four Forces of Steady Flight | **MEDIUM** | 2 lines with `<br/>` | Lines 315, 318 contain `<br/>` in `L` and `D`. |
| **Diag 7** | 348–360 | Powertrain Architecture | **CRITICAL** | **Unquoted nodes with `\n` and `&`** | Lines 350–353: `A[LiPo Battery\nChemical Energy\nV_nom, C_Ah]`, `B[Power Distribution\nBoard & ESCs]`, `C[...]`, `D[...]`, `E[Rotor Thrust T\n& Reactive Torque Q]`. These crash Mermaid parsers due to unquoted raw `\n` and ampersand `&`. Add quotes and replace `&` with `and`. |
| **Diag 8** | 408–434 | Sensor Suites & Avionics | Clean | Standard quoting | Valid. |
| **Diag 9** | 442–452 | Flight Envelope Constraints | **CRITICAL** | 1 line with `<br/>`, **Unescaped `< mg` tag** | Line 445: `E1["... vertical thrust component T·cos(θ) < mg ⟹ Inevitable Altitude Loss"]`. The `< mg` is an unescaped tag error! Replace with `&lt; mg` or `T cos(theta) < mg`. |

#### Topic 2 (`topic_2_coordinate_frames.md`):

| Diagram # | Lines | Topic / Title | Detected Syntax Hazards | Specific Hazard Detail | Mandatory Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Diag 1** | 25–45 | Aerospace Coordinate Hierarchy | **HIGH** | 7 lines with `<br/>`, Unicode Emojis | Lines 28, 30, 32, 34, 38, 39, 40 contain `<br/>`. Lines 38–39 contain emojis `⚠️`, `✅`. Replace `<br/>` and remove emojis inside node labels. |
| **Diag 2** | 77–91 | Prerequisite 2D Rotation & RHR | **MEDIUM** | 2 lines with `<br/>` | Lines 81, 86 contain `<br/>` in `R_DESC` and `RHR_DESC`. |
| **Diag 3** | 149–167 | Inertial vs Body Frame | **HIGH** | 2 lines with `<br/>`, **Non-standard arrow `<==>`** | Lines 154, 160 contain `<br/>`. Line 163 contains `INERTIAL <==>|"..."| BODY`. In Mermaid flowchart, `<-->` is the valid bidirectional link. |
| **Diag 4** | 563–574 | Unit Quaternion Geometry | **MEDIUM** | Pipe delimiter hazard `\|\|q\|\|` | Line 567: `NORM["Unit Norm Invariant: \|\|q\|\|² = ..."]`. Double pipe `\|\|` can conflict with Mermaid link/event syntax. Replace with `\|q\|²` or `norm(q)²`. |
| **Diag 5** | 708–722 | Homogeneous SE(3) Matrix | **MEDIUM** | 1 line with `<br/>` | Line 717 contains `<br/>` in `H_MAT`. |

---

## 5. Generative UI Widget Integration & Pedagogical Insertion Points

Neither Topic 1 nor Topic 2 currently embeds its interactive Generative UI visualizer widget inline. Both files only feature external markdown links (`[Launch Widget...](../widgets/...)`).

Per Acceptance Criteria:
> *"Every chapter directly references and embeds its corresponding interactive Generative UI widget from `modules/EEEE4138_aerial_robotics/widgets/` at the exact pedagogical point where the concept is introduced."*
> *"Seamless inline embedding via `<iframe src="../widgets/widget_X_....html" width="100%" height="520" frameborder="0"></iframe>` or clear interactive links, allowing students to visualize coordinate frames, tilt vectors, gyroscopic precession, and cascaded loops interactively within the chapter text."*

### 5.1 Topic 1: `widget_1_flight_envelope.html`

- **Widget Capabilities:**
  - Dynamic simulation of Disc Loading $DL$, Induced Inflow Velocity $v_i$, and Hover Electrical Power $P_{\text{elec}}$.
  - Interactive parameter controls: Fixed Mass $m_{\text{fixed}}$, Battery Mass $m_{\text{bat}}$, Propeller Radius $R$, Motor $K_v$, Cell count $S$.
  - Real-time Canvas graph plotting $t_{\text{hover}}(m_{\text{bat}})$ demonstrating the non-linear diminishing returns curve and analytical maximum at $m_{\text{bat}} = 2 m_{\text{fixed}}$ ($66.7\%$ battery mass fraction).
  - Live Thrust-to-Weight Ratio gauge and maximum tilt boundary $\theta_{\max} = \arccos(1/TWR)$.
- **Exact Pedagogical Insertion Point:**
  - **Section 6.5 ("Finding the Analytical Maximum", immediately following Equation 1.22, lines 240–244).**
  - *Pedagogical Rationale:* At this exact mathematical milestone, students have just stepped through the quotient rule derivation proving $m_{\text{bat}} = 2 m_{\text{fixed}}$. Immediately embedding the visualizer allows students to manipulate $m_{\text{bat}}$, observe the peak, drag beyond into the degradation regime, and witness the flight endurance collapse in real time.
- **Recommended Embedding Markup:**
  ```html
  <div class="my-6 rounded-xl overflow-hidden border border-slate-700 shadow-xl bg-slate-900">
    <div class="px-4 py-2 bg-slate-800 border-b border-slate-700 text-xs font-semibold text-sky-400 uppercase tracking-wider flex items-center justify-between">
      <span>Interactive Simulation: Flight Envelope & Hover Endurance Visualizer</span>
      <a href="../widgets/widget_1_flight_envelope.html" target="_blank" class="text-slate-400 hover:text-sky-300">Open in New Tab ↗</a>
    </div>
    <iframe src="../widgets/widget_1_flight_envelope.html" width="100%" height="540" frameborder="0" class="w-full"></iframe>
  </div>
  ```

---

### 5.2 Topic 2: `widget_2_frames_gimbal_lock.html`

- **Widget Capabilities:**
  - Interactive 3D Canvas rendering of Inertial NED and Body FRD coordinate frames.
  - Interactive Euler gimbal rings for intrinsic $Z$-$Y$-$X$ yaw, pitch, and roll rotations.
  - Live computation and display of the $3 \times 3$ Direction Cosine Matrix $R_b^n(\phi, \theta, \psi)$.
  - **Gimbal Lock Detector & Visual Warning:** Visual warning pulse when pitch reaches $\theta = \pm 90^\circ$, highlighting how the roll and yaw gimbal rings become coplanar and lose a degree of freedom.
  - **Singularity-Free Quaternion Readout:** Displays unit quaternion $\mathbf{q} \in \mathbb{S}^3$ smoothly tracking through $\theta = 90^\circ$ without divergence.
- **Exact Pedagogical Insertion Point:**
  - **Section 6.3 / Section 7 ("Mathematical & Physical Analysis of Gimbal Lock" / "Unit Quaternions", lines 554–563).**
  - *Pedagogical Rationale:* Students have just derived that the Euler rate matrix $W_\eta$ has $\cos\theta$ in the denominator and witnessed $R_v^b$ collapse into $(\phi - \psi)$ at $\theta = 90^\circ$. Embedding the 3D gimbal simulator directly at this transition allows students to rotate the pitch ring to $90^\circ$, observe the mechanical alignment, and immediately appreciate why quaternions on $\mathbb{S}^3$ are mandatory for real flight controllers.
  - **Secondary Cleanup:** In Section 10 (Line 941), remove the invalid LaTeX `\href` math box `$$\boxed{\dots \href{\dots} \dots}$$` and replace it with a clean markdown navigation reference.
- **Recommended Embedding Markup:**
  ```html
  <div class="my-6 rounded-xl overflow-hidden border border-slate-700 shadow-xl bg-slate-900">
    <div class="px-4 py-2 bg-slate-800 border-b border-slate-700 text-xs font-semibold text-sky-400 uppercase tracking-wider flex items-center justify-between">
      <span>Interactive Simulation: 3D Coordinate Frames & Gimbal Lock Simulator</span>
      <a href="../widgets/widget_2_frames_gimbal_lock.html" target="_blank" class="text-slate-400 hover:text-sky-300">Open in New Tab ↗</a>
    </div>
    <iframe src="../widgets/widget_2_frames_gimbal_lock.html" width="100%" height="560" frameborder="0" class="w-full"></iframe>
  </div>
  ```

---

## 6. Actionable Implementation Checklist for Editor Agent

When refactoring `topic_1_uav_architectures.md` and `topic_2_coordinate_frames.md`, the implementing agent should execute the following discrete edits:

### In `topic_1_uav_architectures.md`:
- [ ] **Task 1.1:** Embed `widget_1_flight_envelope.html` via `<iframe>` at lines 240–244 (Section 6.5).
- [ ] **Task 1.2:** Sanitize Mermaid Diagram 4 (Line 247): replace raw `<` in `subgraph REGIME1["1. Linear Regime (m_bat < m_fixed)"]` with `&lt;` or text.
- [ ] **Task 1.3:** Sanitize Mermaid Diagram 7 (Lines 348–360): enclose all node labels in double quotes, replace `\n` with clean text, and replace `&` with `and`.
- [ ] **Task 1.4:** Sanitize Mermaid Diagram 9 (Line 445): replace `< mg` with `&lt; mg` to prevent unclosed HTML tag errors.
- [ ] **Task 1.5:** Replace `<br/>` tags across Mermaid Diagrams 2, 3, 4, 5, 6, and 9 with valid Mermaid newline formatting or concise single lines.
- [ ] **Task 1.6:** Reformat Section 7.1 bullet list into a 5-column comparative regulatory table.
- [ ] **Task 1.7:** Add a LiPo cell parameter table and `> [!WARNING]` callout to Section 9.3.
- [ ] **Task 1.8:** Restructure Section 13 pitfalls into pedagogical cards (`The Error` / `The Physics` / `The Mitigation`).

### In `topic_2_coordinate_frames.md`:
- [ ] **Task 2.1:** Fix KaTeX tab corruptions:
  - Line 560: `$	heta$` $\to$ `$\theta$`
  - Line 946: `$|	heta|$` $\to$ `$|\theta|$`
  - Line 946: `$\cos	heta$` $\to$ `$\cos\theta$`
  - Line 946: `($\dot{\phi}, \dot{\psi} 	o \infty$)` $\to$ `(\dot{\phi}, \dot{\psi} \to \infty)`
- [ ] **Task 2.2:** Remove unsafe `\href` in display math at line 941; replace with standard Markdown link and cross-reference.
- [ ] **Task 2.3:** Embed `widget_2_frames_gimbal_lock.html` via `<iframe>` at lines 558–562 (Section 7).
- [ ] **Task 2.4:** Sanitize Mermaid Diagram 3 (Line 163): replace `<==>` with standard bidirectional arrow `<-->`.
- [ ] **Task 2.5:** Sanitize Mermaid Diagram 4 (Line 567): replace `||q||` with `|q|` or `norm(q)`.
- [ ] **Task 2.6:** Replace `<br/>` tags and remove unicode emojis from node labels across Mermaid Diagrams 1, 2, 3, and 5.
- [ ] **Task 2.7:** Add a stability/wind frame vector alignment summary table in Section 4.6.
- [ ] **Task 2.8:** Formalize the $85^\circ$ gimbal lock protection logic in Section 6.3.3 into an explicit `> [!CAUTION]` flight code invariant box.

---

## 7. Verification Method

To verify the chapters after editing:
1. **Automated Verification Harness:**
   ```powershell
   python modules/EEEE4138_aerial_robotics/scripts/verify_textbook_and_widgets.py
   ```
   Must pass all 74+ tests with 0 failures and 0 warnings.
2. **Mermaid & Tab Syntax Audit Script:**
   ```powershell
   python .agents/teamwork/explorer_survey_1/audit_script.py
   ```
   Must report 0 tabs, 0 unquoted special character blocks, 0 dangerous `<` HTML tags, and valid `<iframe>` embeds.
3. **Browser Visual Inspection:**
   Open both markdown files in a standard Markdown previewer (e.g., VS Code Markdown Preview or browser preview) to confirm that:
   - All Mermaid diagrams render cleanly without red parser errors.
   - Both widgets render interactively within their `<iframe>` containers.
   - All KaTeX equations render without syntax flags or truncated symbols.
