#!/usr/bin/env python3
r"""
draw_diagram.py — Generate publication-grade block diagrams and flowcharts.

Uses system Graphviz (dot) to render crisp, high-DPI (300 DPI) PNG or vector SVG
images ready for insertion into coursework reports, Word docs, and concept notes.

Usage:
    python draw_diagram.py <command> [options]

Commands:
    feedback     Generate classic closed-loop control block diagram
    state-space  Generate modern state-space integrator chain diagram (A, B, C, D)
    flow         Generate a flowchart or processing pipeline from simple arrow string
    dot          Compile custom Graphviz (.dot) file or string to image

Examples:
    # 1. Closed-loop control block diagram:
    python draw_diagram.py feedback --controller "PID C(s)" --plant "Motor G(s)" -o assets/control_loop.png

    # 2. Modern state-space realization (dx/dt = Ax + Bu, y = Cx + Du):
    python draw_diagram.py state-space -o assets/state_space_diagram.png

    # 3. Algorithm or sensor processing pipeline:
    python draw_diagram.py flow "IMU, Camera -> EKF Fusion -> State Estimator -> LQR Controller -> Motors" -o assets/uav_pipeline.png

    # 4. Compile a custom .dot file at 300 DPI:
    python draw_diagram.py dot architecture.dot -o assets/system_arch.png --dpi 300
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_graphviz():
    """Ensure graphviz dot binary is available."""
    if not shutil.which("dot"):
        print("Error: Graphviz 'dot' binary is not installed or not in PATH.", file=sys.stderr)
        print("Install on Ubuntu/Debian via: sudo apt install graphviz", file=sys.stderr)
        sys.exit(1)


def compile_dot(dot_source: str, output_path: str | Path | None, default_name: str, dpi: int = 300) -> Path:
    """Compile DOT source code to PNG or SVG using Graphviz."""
    check_graphviz()

    if output_path is None:
        out = Path("assets") / default_name
    else:
        out = Path(output_path)

    out.parent.mkdir(parents=True, exist_ok=True)
    fmt = "svg" if out.suffix.lower() == ".svg" else "png"

    # Inject DPI if not in source
    if f"-Gdpi={dpi}" not in dot_source and fmt == "png":
        dot_source = dot_source.replace("digraph {", f"digraph {{\n    dpi={dpi};")
        dot_source = dot_source.replace("digraph G {", f"digraph G {{\n    dpi={dpi};")

    cmd = ["dot", f"-T{fmt}", f"-Gdpi={dpi}", f"-o{out}"]
    proc = subprocess.run(cmd, input=dot_source, text=True, capture_output=True)

    if proc.returncode != 0:
        print(f"Graphviz compilation failed:\n{proc.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"Diagram generated → {out}")
    print(f"Markdown snippet:\n  ![{out.stem}]({out.name})\n")
    return out


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

COMMON_STYLE = """
    fontname="DejaVu Sans";
    node [
        fontname="DejaVu Sans",
        fontsize=10,
        shape=rect,
        style="rounded,filled",
        fillcolor="#F8FAFC",
        color="#334155",
        penwidth=1.2,
        height=0.45
    ];
    edge [
        fontname="DejaVu Sans",
        fontsize=9,
        color="#1E293B",
        arrowsize=0.7,
        penwidth=1.1
    ];
"""


def template_feedback(ref: str, controller: str, plant: str, sensor: str, out_label: str) -> str:
    return f"""digraph FeedbackLoop {{
    rankdir=LR;
    {COMMON_STYLE}

    R [shape=plaintext, label="{ref}", fillcolor=none, color=none];
    Sum [shape=circle, width=0.35, fixedsize=true, label="+", fillcolor="#FFFFFF"];
    Controller [label="{controller}", fillcolor="#EFF6FF", color="#2563EB"];
    Plant [label="{plant}", fillcolor="#F0FDF4", color="#16A34A"];
    Sensor [label="{sensor}", fillcolor="#F8FAFC", color="#475569"];
    Y [shape=plaintext, label="{out_label}", fillcolor=none, color=none];

    R -> Sum;
    Sum -> Controller [label=" e(t) "];
    Controller -> Plant [label=" u(t) "];
    Plant -> Y;
    Plant -> Sensor [label=" y(t) "];
    Sensor -> Sum [label=" - y_m(t) "];
}}
"""


def template_state_space() -> str:
    return f"""digraph StateSpace {{
    rankdir=LR;
    {COMMON_STYLE}

    U [shape=plaintext, label="Input u(t)", fillcolor=none, color=none];
    B [label="Input Matrix\\nB", fillcolor="#EFF6FF", color="#2563EB"];
    Sum1 [shape=circle, width=0.35, fixedsize=true, label="+", fillcolor="#FFFFFF"];
    Int [label="Integrator\\n∫ dt", shape=box, fillcolor="#FEF3C7", color="#D97706", width=0.8];
    C [label="Output Matrix\\nC", fillcolor="#EFF6FF", color="#2563EB"];
    Sum2 [shape=circle, width=0.35, fixedsize=true, label="+", fillcolor="#FFFFFF"];
    D [label="Direct Feedthrough\\nD", fillcolor="#F8FAFC", color="#64748B"];
    A [label="System Matrix\\nA", fillcolor="#FEE2E2", color="#DC2626"];
    Y [shape=plaintext, label="Output y(t)", fillcolor=none, color=none];

    U -> B;
    B -> Sum1;
    Sum1 -> Int [label=" dx/dt "];
    Int -> C [label=" x(t) "];
    Int -> A;
    A -> Sum1;
    C -> Sum2;
    U -> D;
    D -> Sum2;
    Sum2 -> Y;
}}
"""


def template_flow(pipeline_str: str, direction: str = "LR") -> str:
    """Parse linear or branching arrow notation like 'A, B -> C -> D -> E'."""
    steps = [s.strip() for s in pipeline_str.split("->") if s.strip()]

    dot_lines = [
        f"digraph Pipeline {{",
        f"    rankdir={direction};",
        COMMON_STYLE,
    ]

    for idx, step in enumerate(steps):
        # Handle comma-separated multiple sources: 'IMU, Camera'
        sub_items = [item.strip() for item in step.split(",") if item.strip()]
        for sub in sub_items:
            node_id = f"node_{idx}_{abs(hash(sub)) % 10000}"
            dot_lines.append(f'    "{sub}" [label="{sub}", fillcolor="#EFF6FF", color="#3B82F6"];')

    # Connect adjacent stages
    for i in range(len(steps) - 1):
        srcs = [s.strip() for s in steps[i].split(",") if s.strip()]
        dsts = [d.strip() for d in steps[i + 1].split(",") if d.strip()]
        for s in srcs:
            for d in dsts:
                dot_lines.append(f'    "{s}" -> "{d}";')

    dot_lines.append("}")
    return "\n".join(dot_lines)


# ---------------------------------------------------------------------------
# CLI Handlers
# ---------------------------------------------------------------------------

def handle_feedback(args):
    ref = args.ref.replace("\\n", "\n")
    ctrl = args.controller.replace("\\n", "\n")
    pl = args.plant.replace("\\n", "\n")
    sens = args.feedback.replace("\\n", "\n")
    out = args.out.replace("\\n", "\n")

    dot = template_feedback(ref, ctrl, pl, sens, out)
    compile_dot(dot, args.output, "control_loop.png", args.dpi)


def handle_state_space(args):
    dot = template_state_space()
    compile_dot(dot, args.output, "state_space_diagram.png", args.dpi)


def handle_flow(args):
    dot = template_flow(args.pipeline, direction=args.dir)
    compile_dot(dot, args.output, "pipeline_flow.png", args.dpi)


def handle_dot(args):
    path = Path(args.file)
    if not path.exists():
        print(f"Error: DOT file not found: {path}", file=sys.stderr)
        sys.exit(1)
    dot = path.read_text(encoding="utf-8")
    default_name = path.with_suffix(".png").name
    compile_dot(dot, args.output, default_name, args.dpi)


def main():
    parser = argparse.ArgumentParser(
        description="Generate publication-grade block diagrams and flowcharts for reports and notes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Diagram type")

    # 1. Feedback Loop
    p_fb = subparsers.add_parser("feedback", help="Closed-loop control block diagram")
    p_fb.add_argument("--ref", default="r(t)\nReference", help="Reference signal label")
    p_fb.add_argument("--controller", default="Controller\nC(s)", help="Controller block label")
    p_fb.add_argument("--plant", default="Plant Dynamics\nG(s)", help="Plant block label")
    p_fb.add_argument("--feedback", default="Sensor\nH(s)", help="Feedback sensor block label")
    p_fb.add_argument("--out", default="y(t)\nOutput", help="Output signal label")
    p_fb.add_argument("-o", "--output", help="Output image file (default: assets/control_loop.png)")
    p_fb.add_argument("--dpi", type=int, default=300, help="Resolution DPI (default: 300)")

    # 2. State-Space
    p_ss = subparsers.add_parser("state-space", help="State-space realization block diagram (A, B, C, D)")
    p_ss.add_argument("-o", "--output", help="Output image file (default: assets/state_space_diagram.png)")
    p_ss.add_argument("--dpi", type=int, default=300, help="Resolution DPI (default: 300)")

    # 3. Flow Pipeline
    p_flow = subparsers.add_parser("flow", help="Flowchart or pipeline from arrow string")
    p_flow.add_argument("pipeline", help="Pipeline string, e.g. 'IMU, Camera -> Fusion -> Controller -> Motors'")
    p_flow.add_argument("--dir", choices=["LR", "TD"], default="LR", help="Layout direction: LR (Left-to-Right) or TD (Top-to-Down)")
    p_flow.add_argument("-o", "--output", help="Output image file (default: assets/pipeline_flow.png)")
    p_flow.add_argument("--dpi", type=int, default=300, help="Resolution DPI (default: 300)")

    # 4. Custom DOT
    p_dot = subparsers.add_parser("dot", help="Compile a custom Graphviz .dot file")
    p_dot.add_argument("file", help="Path to .dot file")
    p_dot.add_argument("-o", "--output", help="Output image file (PNG or SVG)")
    p_dot.add_argument("--dpi", type=int, default=300, help="Resolution DPI (default: 300)")

    args = parser.parse_args()

    dispatch = {
        "feedback": handle_feedback,
        "state-space": handle_state_space,
        "flow": handle_flow,
        "dot": handle_dot,
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()

