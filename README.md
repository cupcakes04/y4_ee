# Y4 Study Notes — MEng Mechatronics

## Subjects

| Folder | Code | Subject | Credits | Semester | Status |
|---|---|---|---|---|---|
| [EEEE4077_mechatronics_proj](./modules/EEEE4077_mechatronics_proj/) | EEEE-4077 | Mechatronics Industrial Project | 40 | Full Year | 🟡 |
| [EEEE3116_adv_eng_math](./modules/EEEE3116_adv_eng_math/) | EEEE-3116 | Advanced Engineering Mathematics | 10 | Autumn | 🟡 |
| [EEEE4064_adv_control_system](./modules/EEEE4064_adv_control_system/) | EEEE-4064 | Advanced Control System Design | 10 | Autumn | 🟡 |
| [EEEE3054_renewable_tech](./modules/EEEE3054_renewable_tech/) | EEEE-3054 | Renewable Energy Generation Technologies | 10 | Autumn | 🟡 |
| [EEEE4138_aerial_robotics](./modules/EEEE4138_aerial_robotics/) | EEEE-4138 | Aerial Robotics | 10 | Autumn | 🟡 |
| [EEEE4023_digital_signal_processing](./modules/EEEE4023_digital_signal_processing/) | EEEE-4023 | Digital Signal Processing | 20 | Spring | ⬜ |
| [MMME4023_add_manufac_3d_print](./modules/MMME4023_add_manufac_3d_print/) | MMME-4023 | Additive Manufacturing & 3D Printing | 10 | Spring | ⬜ |
| [MMME4127_digital_manufacturing](./modules/MMME4127_digital_manufacturing/) | MMME-4127 | Digital Manufacturing | 10 | Spring | ⬜ |

Status: ⬜ not started · 🟡 in progress · ✅ completed

---

## Folder Structure (per subject)

```text
modules/{SUBJECT}/
├── raw/          source PDFs, lecture slides, and reference files
├── concepts/     study notes and concept breakdowns
├── chapters/     official work, coursework (e.g., cw1), and lecture/chapter material
└── drills/       exercises, practice problems, and worked drills
```

---

## Study Toolkit & Automation Scripts (`scripts/`)

A suite of complementary CLI tools designed for processing engineering lecture slides, managing notes, and maintaining link integrity,  with [skills](./SKILLS.md).

### 1. `pdf_extract.py` — Lecture PDF to Markdown & Assets
Extracts structured text blocks, tables, and embedded images from lecture PDFs into clean Markdown (`.md`).
- **Embedded image extraction:** Saves images to `<pdf_name>_assets/` and auto-links them in the markdown.
- **Table conversion:** Generates GitHub-flavored Markdown tables.
- **Dual-engine:** Uses `pymupdf` when available, with automatic fallback to `poppler-utils` (`pdftotext` / `pdfimages`).

```bash
# Basic extraction to <lecture>.md with companion assets folder
python scripts/pdf_extract.py "modules/EEEE4064_adv_control_system/raw/L01.pdf"

# Render full slide overviews for vector-drawn block diagrams/plots
python scripts/pdf_extract.py "lecture.pdf" output.md --render-slides --dpi 200
```

### 2. `pdf_crop.py` — Visual Diagram & Equation Cropper
High-resolution (200–300 DPI) cropper to grab circuits, Bode plots, state-space diagrams, and math formulas directly into PNGs for embedding into concept notes.
- **Preset crops:** Quick semantic cuts (`--preset top-half`, `bottom-half`, `center`, `slide-body`).
- **Normalized coordinates:** Crop any arbitrary region via `--bbox x0,y0,x1,y1` (0.0 to 1.0 percentages).
- **Full slide render:** Render crisp slide pages with `--full-page`.
- **Markdown embed ready:** Prints the ready-to-paste `![Caption](path.png)` markdown tag.

```bash
# Crop a diagram from slide 5 using presets
python scripts/pdf_crop.py lecture.pdf -p 5 --preset bottom-half -o assets/bode_plot.png

# Crop a specific equation/box (normalized 0.0 - 1.0 bbox)
python scripts/pdf_crop.py lecture.pdf -p 3 --bbox 0.1,0.25,0.9,0.70 -o assets/state_eq.png

# Render full slide 12 at 300 DPI
python scripts/pdf_crop.py lecture.pdf -p 12 --full-page --dpi 300 -o assets/slide12.png
```

### 3. `latex_plot.py` — Computational LaTeX-Styled Engineering Grapher
Generates publication-grade engineering plots with authentic Computer Modern $\TeX$ typography without requiring heavy TeXLive installations (uses pre-installed `matplotlib`, `scipy`, and `numpy`).
- **Control responses:** Underdamped/overdamped step responses with automatic overshoot ($M_p$) and settling time ($t_s$) annotations.
- **Frequency domain:** Bode magnitude (dB) and phase diagrams from transfer function polynomials.
- **Root analysis:** Pole-Zero maps on the continuous $s$-plane or discrete $z$-plane (with unit circle).
- **Matrix & math:** Arbitrary function plots $f(x)$ and sparse matrix sparsity patterns.

```bash
# 1. Step response for a closed-loop system (zeta=0.4, wn=2.5 rad/s)
python scripts/latex_plot.py step --zeta 0.4 --wn 2.5 -o assets/step_response.png

# 2. Bode plot for G(s) = 25 / (s^2 + 3s + 25)
python scripts/latex_plot.py bode --num "25" --den "1 3 25" -o assets/bode.png

# 3. Pole-Zero map on the s-plane
python scripts/latex_plot.py pz --poles "-1+2j -1-2j -4" --zeros "0" -o assets/pz_map.png

# 4. Mathematical function with LaTeX labels
python scripts/latex_plot.py func "np.sin(x)/x" --range "-12 12" --title r"$\mathrm{sinc}(x) = \frac{\sin x}{x}$" -o assets/sinc.png
```

### 4. `draw_diagram.py` — Block Diagram & Flowchart Generator
Generates publication-quality, 300 DPI block diagrams and processing pipelines for coursework reports, Word documents, and concept notes using the system's pre-installed Graphviz engine.
- **Control loops:** Closed-loop feedback diagrams ($r(t), \Sigma, C(s), G(s), H(s), y(t)$).
- **State-space:** Full realization diagrams with integrator blocks ($\int dt$) and matrices $A, B, C, D$.
- **Pipelines:** Linear or branching flowcharts from simple string notation (`"A, B -> C -> D"`).
- **Custom DOT:** Compiles arbitrary `.dot` source files to 300 DPI PNG or vector SVG.

```bash
# 1. Closed-loop control block diagram
python scripts/draw_diagram.py feedback --controller "PID C(s)" --plant "Motor G(s)" -o assets/control_loop.png

# 2. State-space realization diagram (dx/dt = Ax + Bu, y = Cx + Du)
python scripts/draw_diagram.py state-space -o assets/state_space.png

# 3. Processing pipeline / flowchart from arrow string
python scripts/draw_diagram.py flow "IMU, Camera -> EKF Fusion -> State Estimator -> LQR -> Motors" -o assets/uav_pipeline.png

# 4. Compile a custom .dot file to 300 DPI PNG or SVG
python scripts/draw_diagram.py dot system_arch.dot -o assets/system_arch.png --dpi 300
```

### 5. `study_audit.py` — Progress Dashboard & Link Auditor
Tracks study status across all 8 modules and checks relative Markdown link integrity.

```bash
# View the study progress summary across all modules
python scripts/study_audit.py

# Audit all notes for dead/broken links (404 checks)
python scripts/study_audit.py --check-links
```

