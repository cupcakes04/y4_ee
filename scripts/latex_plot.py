#!/usr/bin/env python3
r"""
latex_plot.py — Generate publication-grade, LaTeX-styled engineering plots.

Zero-bloat graphing tool using Matplotlib MathText + SciPy to compute and render
crisp engineering graphs with authentic Computer Modern TeX typography.

Usage:
    python latex_plot.py <command> [options]

Commands:
    step      Underdamped/overdamped step response with metrics (overshoot, ts, tr)
    bode      Bode magnitude (dB) and phase (deg) plot from transfer function
    pz        Pole-Zero map on the s-plane or z-plane with stability boundaries
    func      Plot arbitrary math functions f(x) with LaTeX annotations
    sparsity  Visualize sparse / structured matrix nonzero patterns

Examples:
    # 1. Second-order underdamped step response:
    python latex_plot.py step --zeta 0.4 --wn 2.5 -o assets/step_response.png

    # 2. Bode plot for G(s) = 25 / (s^2 + 3s + 25):
    python latex_plot.py bode --num "25" --den "1 3 25" -o assets/bode_plot.png

    # 3. Pole-Zero map on the s-plane:
    python latex_plot.py pz --poles "-1+2j -1-2j -4" --zeros "0" -o assets/pz_map.png

    # 4. Math function with LaTeX labels:
    python latex_plot.py func "np.sin(x)/x" --range "-12 12" --title r"$\mathrm{sinc}(x) = \frac{\sin x}{x}$" -o assets/sinc.png
"""

import argparse
import os
import sys
from pathlib import Path

# Set cache dir to avoid permission warnings in headless environments
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib_cache")

import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Apply authentic LaTeX styling (Computer Modern serif)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Computer Modern Roman"],
    "mathtext.fontset": "cm",  # Computer Modern TeX fonts
    "mathtext.rm": "serif",
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "figure.titlesize": 13,
    "grid.color": "#e0e0e0",
    "grid.linestyle": "--",
    "grid.linewidth": 0.7,
})


def parse_poly(poly_str: str) -> list[float]:
    """Parse space or comma separated polynomial coefficients."""
    cleaned = poly_str.replace(",", " ").strip()
    return [float(x) for x in cleaned.split()]


def parse_complex_list(c_str: str) -> list[complex]:
    """Parse list of complex numbers like '-1+2j -1-2j -3'."""
    cleaned = c_str.replace(",", " ").strip()
    res = []
    for item in cleaned.split():
        item = item.strip()
        if not item:
            continue
        # Convert standard 'i' to 'j' if user typed engineering 'i'
        if item.endswith("i") and not item.endswith("j"):
            item = item[:-1] + "j"
        res.append(complex(item))
    return res


def save_and_report(fig: plt.Figure, output_path: str | Path | None, default_name: str, dpi: int = 200) -> Path:
    """Save plot, close figure, and output Markdown snippet."""
    if output_path is None:
        out = Path("assets") / default_name
    else:
        out = Path(output_path)

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(str(out), dpi=dpi, bbox_inches="tight")
    plt.close(fig)

    print(f"Graph generated → {out}")
    print(f"Markdown snippet:\n  ![{out.stem}]({out.name})\n")
    return out


# ---------------------------------------------------------------------------
# Command Handlers
# ---------------------------------------------------------------------------

def handle_step(args):
    """Plot step response for 2nd order system or arbitrary transfer function."""
    if args.zeta is not None and args.wn is not None:
        zeta = float(args.zeta)
        wn = float(args.wn)
        num = [wn**2]
        den = [1.0, 2.0 * zeta * wn, wn**2]
        system_label = rf"$\zeta = {zeta},\ \omega_n = {wn}\ \mathrm{{rad/s}}$"
    elif args.num and args.den:
        num = parse_poly(args.num)
        den = parse_poly(args.den)
        system_label = rf"$\mathrm{{Num}} = {num},\ \mathrm{{Den}} = {den}$"
        zeta, wn = None, None
    else:
        # Default: classic underdamped prototype
        zeta, wn = 0.5, 2.0
        num = [wn**2]
        den = [1.0, 2.0 * zeta * wn, wn**2]
        system_label = rf"$\zeta = {zeta},\ \omega_n = {wn}\ \mathrm{{rad/s}}$"

    sys_lti = signal.TransferFunction(num, den)
    t_span = np.linspace(0, args.tmax, 500) if args.tmax else None
    t, y = signal.step(sys_lti, T=t_span)

    # Compute response metrics
    y_final = float(y[-1])
    y_max = float(np.max(y))
    overshoot_pct = max(0.0, ((y_max - y_final) / y_final) * 100.0) if y_final != 0 else 0.0
    t_peak = float(t[np.argmax(y)])

    # 2% settling time
    settled_mask = np.abs(y - y_final) <= 0.02 * abs(y_final)
    t_settling = None
    for i in range(len(t) - 1, -1, -1):
        if not settled_mask[i]:
            t_settling = float(t[min(i + 1, len(t) - 1)])
            break

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(t, y, color="#1f77b4", lw=2, label=r"Step Response $y(t)$")
    ax.axhline(y_final, color="#7f7f7f", linestyle="--", lw=1.2, label=rf"Steady State ($y_\infty = {y_final:.2f}$)")

    # Highlight overshoot if significant
    if overshoot_pct > 0.5:
        ax.plot(t_peak, y_max, "ro", markersize=6)
        ax.annotate(
            rf"$M_p = {overshoot_pct:.1f}\%$" + "\n" + rf"($t_p = {t_peak:.2f}\mathrm{{s}}$)",
            xy=(t_peak, y_max),
            xytext=(t_peak + (t[-1] * 0.05), y_max * 0.96),
            arrowprops=dict(arrowstyle="->", color="#d62728", lw=1),
            fontsize=9.5,
            color="#d62728",
        )

    # Settling band
    ax.fill_between(t, y_final * 0.98, y_final * 1.02, color="#2ca02c", alpha=0.15, label=r"$\pm 2\%$ Settling Band")

    title = args.title or rf"Closed-Loop Step Response ({system_label})"
    ax.set_title(title)
    ax.set_xlabel(r"Time $t$ [seconds]")
    ax.set_ylabel(r"Output $y(t)$")
    ax.grid(True)
    ax.legend(loc="lower right")

    save_and_report(fig, args.output, "step_response.png", args.dpi)


def handle_bode(args):
    """Plot Bode magnitude and phase diagrams."""
    num = parse_poly(args.num) if args.num else [10]
    den = parse_poly(args.den) if args.den else [1, 2, 10]

    sys_lti = signal.TransferFunction(num, den)
    w_min = float(args.wmin) if args.wmin else -2
    w_max = float(args.wmax) if args.wmax else 2
    w = np.logspace(w_min, w_max, 500)
    w, mag, phase = signal.bode(sys_lti, w=w)

    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(7.5, 5.5), sharex=True)

    # Magnitude
    ax_mag.semilogx(w, mag, color="#1f77b4", lw=2)
    ax_mag.axhline(0, color="#7f7f7f", linestyle=":", lw=1)
    ax_mag.set_ylabel(r"Magnitude $|G(j\omega)|$ [dB]")
    ax_mag.set_title(args.title or r"Bode Diagram: $G(s) = \frac{N(s)}{D(s)}$")
    ax_mag.grid(True, which="both")

    # Phase
    ax_phase.semilogx(w, phase, color="#d62728", lw=2)
    ax_phase.axhline(-180, color="#7f7f7f", linestyle=":", lw=1)
    ax_phase.set_ylabel(r"Phase $\angle G(j\omega)$ [deg]")
    ax_phase.set_xlabel(r"Frequency $\omega$ [$\mathrm{rad/s}$]")
    ax_phase.grid(True, which="both")

    save_and_report(fig, args.output, "bode_plot.png", args.dpi)


def handle_pz(args):
    """Plot Pole-Zero map on the s-plane (continuous) or z-plane (discrete)."""
    poles = parse_complex_list(args.poles) if args.poles else []
    zeros = parse_complex_list(args.zeros) if args.zeros else []

    is_z = args.plane.lower() == "z"

    fig, ax = plt.subplots(figsize=(6, 5.5))
    ax.axhline(0, color="#555555", lw=1)
    ax.axvline(0, color="#555555", lw=1)

    if is_z:
        # Draw discrete unit circle |z| = 1
        theta = np.linspace(0, 2 * np.pi, 300)
        ax.plot(np.cos(theta), np.sin(theta), color="#2ca02c", linestyle="--", lw=1.5, label=r"Unit Circle $|z|=1$")
        ax.set_title(args.title or r"Discrete-Time Pole-Zero Map ($z$-plane)")
        ax.set_xlabel(r"$\mathrm{Re}(z)$")
        ax.set_ylabel(r"$\mathrm{Im}(z)$")
    else:
        # Continuous s-plane: highlight stable LHP (Left Half Plane)
        ax.set_title(args.title or r"Continuous-Time Pole-Zero Map ($s$-plane)")
        ax.set_xlabel(r"Real Axis $\sigma$ [$\mathrm{s}^{-1}$]")
        ax.set_ylabel(r"Imaginary Axis $j\omega$ [$\mathrm{rad/s}$]")

    # Plot poles (x)
    if poles:
        p_real = [p.real for p in poles]
        p_imag = [p.imag for p in poles]
        ax.scatter(p_real, p_imag, marker="x", s=90, color="#d62728", linewidths=2.5, label=rf"Poles ({len(poles)})")

    # Plot zeros (o)
    if zeros:
        z_real = [z.real for z in zeros]
        z_imag = [z.imag for z in zeros]
        ax.scatter(z_real, z_imag, marker="o", s=75, facecolors="none", edgecolors="#1f77b4", linewidths=2, label=rf"Zeros ({len(zeros)})")

    ax.grid(True)
    ax.legend(loc="upper right")
    ax.set_aspect("equal", adjustable="datalim")

    save_and_report(fig, args.output, "pole_zero_map.png", args.dpi)


def handle_func(args):
    """Plot arbitrary math formula f(x)."""
    r_parts = [float(x) for x in args.range.replace(",", " ").split()]
    if len(r_parts) != 2:
        raise ValueError("Range must be two numbers e.g. '--range -10 10'")

    x = np.linspace(r_parts[0], r_parts[1], args.points)
    
    # Safe eval namespace with numpy functions
    eval_env = {"x": x, "np": np}
    try:
        y = eval(args.expr, {"__builtins__": {}}, eval_env)
    except Exception as e:
        print(f"Error evaluating expression '{args.expr}': {e}", file=sys.stderr)
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    label = args.label or rf"$f(x) = {args.expr}$"
    ax.plot(x, y, color="#1f77b4", lw=2, label=label)

    ax.axhline(0, color="#888888", lw=0.8, linestyle=":")
    ax.set_title(args.title or rf"Function Plot: ${args.expr}$")
    ax.set_xlabel(args.xlabel or r"$x$")
    ax.set_ylabel(args.ylabel or r"$f(x)$")
    ax.grid(True)
    ax.legend(loc="best")

    save_and_report(fig, args.output, "function_plot.png", args.dpi)


def handle_sparsity(args):
    """Visualize matrix sparsity pattern (Spy plot)."""
    n = args.size
    # Generate structured test matrix or parse file
    if args.type == "tridiag":
        A = np.diag(np.ones(n) * 4) + np.diag(np.ones(n - 1) * -1, 1) + np.diag(np.ones(n - 1) * -1, -1)
        matrix_title = rf"Tridiagonal Matrix Pattern ($n={n}$)"
    elif args.type == "banded":
        A = np.zeros((n, n))
        for k in range(-args.bandwidth, args.bandwidth + 1):
            A += np.diag(np.ones(n - abs(k)), k)
        matrix_title = rf"Banded Matrix Pattern ($n={n}, b={args.bandwidth}$)"
    else:
        # Random sparse
        p = args.density
        A = (np.random.rand(n, n) < p).astype(float)
        matrix_title = rf"Sparse Random Pattern ($n={n}, p={p*100:.0f}\%$)"

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.spy(A, markersize=args.markersize, color="#1f77b4")
    ax.set_title(args.title or matrix_title)
    ax.set_xlabel(r"Column Index $j$")
    ax.set_ylabel(r"Row Index $i$")

    save_and_report(fig, args.output, "matrix_sparsity.png", args.dpi)


# ---------------------------------------------------------------------------
# CLI Argument Parser
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate publication-grade engineering plots with LaTeX typography."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Plot command")

    # 1. Step Response
    p_step = subparsers.add_parser("step", help="Plot step response for second-order system or transfer function")
    p_step.add_argument("--zeta", type=float, help="Damping ratio zeta")
    p_step.add_argument("--wn", type=float, help="Natural frequency wn [rad/s]")
    p_step.add_argument("--num", help="Transfer function numerator coefficients (e.g. '10')")
    p_step.add_argument("--den", help="Transfer function denominator coefficients (e.g. '1 2 10')")
    p_step.add_argument("--tmax", type=float, default=None, help="Max simulation time")
    p_step.add_argument("--title", help="Custom LaTeX plot title")
    p_step.add_argument("-o", "--output", help="Output image file path")
    p_step.add_argument("--dpi", type=int, default=200, help="Output resolution DPI (default: 200)")

    # 2. Bode Plot
    p_bode = subparsers.add_parser("bode", help="Plot Bode magnitude & phase diagrams")
    p_bode.add_argument("--num", help="Numerator coefficients (e.g. '25')")
    p_bode.add_argument("--den", help="Denominator coefficients (e.g. '1 3 25')")
    p_bode.add_argument("--wmin", type=float, default=-2, help="Log10 min frequency (default: -2 for 10^-2 rad/s)")
    p_bode.add_argument("--wmax", type=float, default=2, help="Log10 max frequency (default: 2 for 10^2 rad/s)")
    p_bode.add_argument("--title", help="Custom LaTeX plot title")
    p_bode.add_argument("-o", "--output", help="Output image file path")
    p_bode.add_argument("--dpi", type=int, default=200, help="Output resolution DPI (default: 200)")

    # 3. Pole-Zero Map
    p_pz = subparsers.add_parser("pz", help="Plot Pole-Zero map on s-plane or z-plane")
    p_pz.add_argument("--poles", help="Poles list (e.g. '-1+2j -1-2j -3')")
    p_pz.add_argument("--zeros", help="Zeros list (e.g. '0 2')")
    p_pz.add_argument("--plane", choices=["s", "z"], default="s", help="Plane type: 's' for continuous, 'z' for discrete")
    p_pz.add_argument("--title", help="Custom LaTeX plot title")
    p_pz.add_argument("-o", "--output", help="Output image file path")
    p_pz.add_argument("--dpi", type=int, default=200, help="Output resolution DPI (default: 200)")

    # 4. Function Plot
    p_func = subparsers.add_parser("func", help="Plot arbitrary math function f(x)")
    p_func.add_argument("expr", help="Python/NumPy expression using 'x' (e.g. 'np.sin(x)/x')")
    p_func.add_argument("--range", default="-10 10", help="Range 'min max' (default: '-10 10')")
    p_func.add_argument("--points", type=int, default=400, help="Number of points (default: 400)")
    p_func.add_argument("--label", help="Legend label (LaTeX format)")
    p_func.add_argument("--xlabel", help="X-axis label (LaTeX format)")
    p_func.add_argument("--ylabel", help="Y-axis label (LaTeX format)")
    p_func.add_argument("--title", help="Custom LaTeX plot title")
    p_func.add_argument("-o", "--output", help="Output image file path")
    p_func.add_argument("--dpi", type=int, default=200, help="Output resolution DPI (default: 200)")

    # 5. Matrix Sparsity
    p_spar = subparsers.add_parser("sparsity", help="Visualize matrix sparsity structure")
    p_spar.add_argument("--size", type=int, default=40, help="Matrix dimension n (default: 40)")
    p_spar.add_argument("--type", choices=["tridiag", "banded", "random"], default="tridiag", help="Matrix structure type")
    p_spar.add_argument("--bandwidth", type=int, default=3, help="Bandwidth for banded type")
    p_spar.add_argument("--density", type=float, default=0.15, help="Density for random sparse (default: 0.15)")
    p_spar.add_argument("--markersize", type=float, default=2.5, help="Spy marker size")
    p_spar.add_argument("--title", help="Custom LaTeX plot title")
    p_spar.add_argument("-o", "--output", help="Output image file path")
    p_spar.add_argument("--dpi", type=int, default=200, help="Output resolution DPI (default: 200)")

    args = parser.parse_args()

    dispatch = {
        "step": handle_step,
        "bode": handle_bode,
        "pz": handle_pz,
        "func": handle_func,
        "sparsity": handle_sparsity,
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
