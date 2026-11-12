# E2E Test Infra: EEEE4138 Aerial Robotics

## Test Philosophy
- Opaque-box, requirement-driven verification of textbook chapters.
- Four core verification dimensions:
  1. Code implementation dumps elimination (R1: zero non-mermaid code blocks).
  2. Generative UI widget integration (R2: 100% of chapters embed their target widget via valid relative iframes).
  3. Visual structure (R2: zero ASCII box-and-arrow diagrams, structured tables/callouts).
  4. Diagram & Math syntax integrity (R3: 100% of Mermaid diagrams and KaTeX blocks pass syntax linting without parser errors).

## Feature Inventory Test Mapping
| # | Feature | Test Dimension | Expected Pass Criterion |
|---|---------|----------------|--------------------------|
| 1 | R1 (Code Removal) | Fenced Code Blocks | Zero ```python, ```matlab, ```cpp blocks in chapters |
| 2 | R2 (Widget 1) | Iframe in Topic 1 | `<iframe src="../widgets/widget_1_flight_envelope.html"` present and resolvable |
| 3 | R2 (Widget 2) | Iframe in Topic 2 | `<iframe src="../widgets/widget_2_frames_gimbal_lock.html"` present and resolvable |
| 4 | R2 (Widget 3) | Iframe in Topic 3 | `<iframe src="../widgets/widget_3_rigid_body_dynamics.html"` present and resolvable |
| 5 | R2 (Widget 4) | Iframe in Topic 4 | `<iframe src="../widgets/widget_4_rotor_mixer_allocation.html"` present and resolvable |
| 6 | R2 (Widget 5) | Iframe in Topic 5 | `<iframe src="../widgets/widget_5_cascaded_flight_control.html"` present and resolvable |
| 7 | R2 (ASCII Removal) | Diagram formatting | Zero ASCII box chains (`[A] --> [B]`) in text |
| 8 | R3 (Mermaid Lint) | Mermaid blocks | All ```mermaid blocks parse without unquoted `&`, bad arrows, unclosed `<` |
| 9 | R3 (KaTeX Lint) | Math blocks | Balanced `$$`, no corrupted tab characters `\t`, no invalid math macros |

## Test Runner Architecture
- Script: `modules/EEEE4138_aerial_robotics/verify_chapters_e2e.py`
- Execution: Python 3 CLI runner with exit code 0 on all tests passing, non-zero on any failure.
- Reports detailed test suite matrix.
