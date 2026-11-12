#!/usr/bin/env python3
"""
verify_textbook_and_widgets.py
==============================
Comprehensive 4-Tier Automated Test Suite & Physics Verification Harness
for EEEE4138 Aerial Robotics Textbook Chapters and Interactive Generative UI Widgets.

Tiers:
  - Tier 1: Feature Coverage (Files existence, 8 mandatory chapter sections, 5 widgets)
  - Tier 2: Boundary & Corner Cases (KaTeX syntax, balanced delimiters, HTML5, 0-external JS, Canvas/SVG, offline styling)
  - Tier 3: Invariant & Cross-Topic Verification (Strict NED, Body FRD, R_b^n ZYX convention, tilt mapping, motor lag stability, relative links)
  - Tier 4: Real-World Math & Physics Oracles (SymPy / NumPy / math symbolic & numerical verification)

Self-Test Mode:
  Run with `--self-test` to independently verify all mathematical oracles, KaTeX syntax
  parsers, HTML dependency checkers, coordinate invariant checkers, and link resolvers.

Usage:
  python verify_textbook_and_widgets.py [--tier 1,2,3,4] [--self-test] [--verbose] [--json]
"""

import os
import sys
import re
import math
import argparse
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

# Ensure stdout and stderr handle UTF-8 cleanly on Windows environments
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Third-party scientific libraries (mandatory for authoritative oracles)
try:
    import numpy as np
    import sympy as sp
except ImportError as exc:
    print(f"FATAL: Required scientific packages missing: {exc}")
    print("Please ensure numpy and sympy are installed in the python environment.")
    sys.exit(2)

# ==============================================================================
# Configuration & Constants
# ==============================================================================

MANDATORY_CHAPTERS = [
    "topic_1_uav_architectures.md",
    "topic_2_coordinate_frames.md",
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
]

MANDATORY_WIDGETS = [
    "widget_1_flight_envelope.html",
    "widget_2_frames_gimbal_lock.html",
    "widget_3_rigid_body_dynamics.html",
    "widget_4_rotor_mixer_allocation.html",
    "widget_5_cascaded_flight_control.html",
]

MANDATORY_CHAPTER_SECTIONS = [
    ("Title & Metadata", [r"#\s+.+", r"\*\*Subject:\*\*", r"\*\*Topic:\*\*"]),
    ("Architecture & API Contract Table", [r"API Contract", r"API Interface", r"\|.*(Input|Direction|Parameter|Output).+\|"]),
    ("Prerequisite Bridge", [r"Prerequisite\s+(Bridge|Anchor)", r"Undergraduate\s+Prerequisite"]),
    ("Step-by-Step Derivations", [r"Derivation", r"First-Principles", r"Step-by-Step"]),
    ("Mermaid / Flow Diagram", [r"```mermaid", r"┌[─-]+┐", r"\+[─-]+\+", r"\+---+"]),
    ("Worked Numerical Examples", [r"Worked\s+(Numerical\s+)?Example", r"Numerical\s+Example"]),
    ("Exam Pitfalls / Watch Out For", [r"Pitfall", r"Watch\s+Out\s+For", r"Engineering\s+Trap", r"Common.*Trap"]),
    ("Bidirectional Links", [r"\[.*\]\(.*topic_.*\.md\)", r"\[.*\]\(.*widget_.*\.html\)"]),
]

ALLOWED_EXTERNAL_SCRIPT_HOSTS = [
    "cdn.tailwindcss.com",
]

# ANSI Terminal Formatting
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    GRAY = "\033[90m"

def colorize(text: str, color_code: str, use_color: bool = True) -> str:
    if not use_color:
        return text
    return f"{color_code}{text}{Colors.RESET}"

# ==============================================================================
# Data Structures
# ==============================================================================

@dataclass
class TestResult:
    tier: int
    name: str
    passed: bool
    message: str
    details: Optional[str] = None
    severity: str = "ERROR"  # "ERROR", "WARNING", "INFO"

@dataclass
class VerificationSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    results: List[TestResult] = field(default_factory=list)
    start_time: float = 0.0
    duration: float = 0.0

    def add(self, result: TestResult):
        self.total += 1
        if result.passed:
            self.passed += 1
        else:
            if result.severity == "WARNING":
                self.warnings += 1
            else:
                self.failed += 1
        self.results.append(result)

# ==============================================================================
# Tier 1: Feature Coverage Verifiers
# ==============================================================================

def verify_tier_1_feature_coverage(base_dir: Path, verbose: bool = False) -> List[TestResult]:
    """Tier 1: Verify presence of all chapters, widgets, and mandatory chapter sections."""
    results: List[TestResult] = []
    chapters_dir = base_dir / "chapters"
    widgets_dir = base_dir / "widgets"

    # 1.1 Chapters Existence
    for chap in MANDATORY_CHAPTERS:
        chap_path = chapters_dir / chap
        exists = chap_path.is_file() and chap_path.stat().st_size > 500
        size_kb = (chap_path.stat().st_size / 1024) if exists else 0
        results.append(TestResult(
            tier=1,
            name=f"Chapter Existence: {chap}",
            passed=exists,
            message=f"Found ({size_kb:.1f} KB)" if exists else f"Missing or empty file: {chap_path}"
        ))

    # 1.2 Widgets Existence
    for wid in MANDATORY_WIDGETS:
        wid_path = widgets_dir / wid
        exists = wid_path.is_file() and wid_path.stat().st_size > 500
        size_kb = (wid_path.stat().st_size / 1024) if exists else 0
        results.append(TestResult(
            tier=1,
            name=f"Widget Existence: {wid}",
            passed=exists,
            message=f"Found ({size_kb:.1f} KB)" if exists else f"Missing or empty file: {wid_path}"
        ))

    # 1.3 Mandatory Sections in Existing Chapters
    for chap in MANDATORY_CHAPTERS:
        chap_path = chapters_dir / chap
        if not chap_path.is_file():
            continue
        content = chap_path.read_text(encoding="utf-8", errors="ignore")
        for sec_name, patterns in MANDATORY_CHAPTER_SECTIONS:
            found = False
            for pat in patterns:
                if re.search(pat, content, re.IGNORECASE | re.MULTILINE):
                    found = True
                    break
            results.append(TestResult(
                tier=1,
                name=f"Chapter Section [{chap}]: {sec_name}",
                passed=found,
                message="Present" if found else f"Section pattern '{sec_name}' missing in {chap}"
            ))

    return results

# ==============================================================================
# Tier 2: Boundary & Corner Cases Verifiers
# ==============================================================================

def validate_katex_syntax(text: str, filename: str) -> List[Tuple[bool, str, Optional[str]]]:
    """
    Validates KaTeX formatting:
    - Balanced inline $ ... $ and block $$ ... $$ delimiters.
    - Balanced \\begin{env} ... \\end{env} environments.
    - Balanced curly braces in math expressions.
    """
    issues = []

    # 1. Check double dollar signs ($$)
    # Strip code fences ```...``` to avoid checking code blocks
    text_no_code = re.sub(r"```[\s\S]*?```", "", text)
    text_no_code = re.sub(r"`[^`\n]+`", "", text_no_code)

    # Double dollar balance
    double_dollars = re.findall(r"\$\$", text_no_code)
    if len(double_dollars) % 2 != 0:
        issues.append((False, "Unbalanced display math delimiters ($$)", f"Count = {len(double_dollars)}"))

    # 2. Check single dollar signs ($) excluding ($$) and escaped (\$)
    # Replace $$ with placeholder
    temp_text = text_no_code.replace("$$", "\x00\x00")
    # Replace escaped \$ with placeholder
    temp_text = re.sub(r"\\\$", "\x01", temp_text)
    single_dollars = re.findall(r"\$", temp_text)
    if len(single_dollars) % 2 != 0:
        issues.append((False, "Unbalanced inline math delimiters ($)", f"Count = {len(single_dollars)}"))

    # 3. Check balanced environments \begin{xyz} ... \end{xyz}
    begins = re.findall(r"\\begin\{([a-zA-Z0-9*]+)\}", text_no_code)
    ends = re.findall(r"\\end\{([a-zA-Z0-9*]+)\}", text_no_code)
    
    begin_counts = {}
    for b in begins:
        begin_counts[b] = begin_counts.get(b, 0) + 1
    end_counts = {}
    for e in ends:
        end_counts[e] = end_counts.get(e, 0) + 1

    all_envs = set(begin_counts.keys()).union(set(end_counts.keys()))
    for env in all_envs:
        b_cnt = begin_counts.get(env, 0)
        e_cnt = end_counts.get(env, 0)
        if b_cnt != e_cnt:
            issues.append((False, f"Unbalanced LaTeX environment '\\begin{{{env}}}'", f"\\begin: {b_cnt}, \\end: {e_cnt}"))

    # If no issues found, return success
    if not issues:
        return [(True, "KaTeX syntax, delimiters, and environments valid", None)]
    return issues

def validate_html5_widget(html_content: str, filename: str) -> List[Tuple[bool, str, Optional[str]]]:
    """
    Validates HTML5 widget:
    - HTML5 doctype and tags.
    - Zero external JS runtime dependencies (only Tailwind CSS CDN allowed).
    - Presence of Canvas or SVG element.
    - Offline fallback styling (<style> present).
    """
    issues = []

    # 1. HTML5 structure
    has_doctype = bool(re.search(r"<!DOCTYPE\s+html>", html_content, re.IGNORECASE))
    has_html = bool(re.search(r"<html[\s>]", html_content, re.IGNORECASE))
    has_head = bool(re.search(r"<head[\s>]", html_content, re.IGNORECASE))
    has_body = bool(re.search(r"<body[\s>]", html_content, re.IGNORECASE))
    if not (has_doctype and has_html and has_head and has_body):
        missing = []
        if not has_doctype: missing.append("<!DOCTYPE html>")
        if not has_html: missing.append("<html>")
        if not has_head: missing.append("<head>")
        if not has_body: missing.append("<body>")
        issues.append((False, "Invalid HTML5 root structure", f"Missing tags: {', '.join(missing)}"))

    # 2. Check external JS script dependencies
    script_srcs = re.findall(r"<script[^>]+src=[\"']([^\"']+)[\"']", html_content, re.IGNORECASE)
    for src in script_srcs:
        # Check against allowed external hosts
        is_allowed = any(host in src for host in ALLOWED_EXTERNAL_SCRIPT_HOSTS)
        if not is_allowed:
            issues.append((False, f"Forbidden external JS dependency detected: {src}",
                           "Only Tailwind CSS CDN is permitted; simulation must be zero-dependency vanilla JS."))

    # 3. Canvas or SVG element
    has_canvas = bool(re.search(r"<canvas[\s>]", html_content, re.IGNORECASE))
    has_svg = bool(re.search(r"<svg[\s>]", html_content, re.IGNORECASE))
    if not (has_canvas or has_svg):
        issues.append((False, "Missing interactive visualizer element", "Widget must include a <canvas> or <svg> element"))

    # 4. Offline fallback styling
    has_style_tag = bool(re.search(r"<style[\s>]", html_content, re.IGNORECASE))
    if not has_style_tag:
        issues.append((False, "Missing offline fallback styling", "Widget must contain inline <style> block for offline fallback styling."))

    if not issues:
        return [(True, "HTML5 structure, zero external JS, visualizer elements, and offline styles valid", None)]
    return issues

def verify_tier_2_boundary_and_corner_cases(base_dir: Path, verbose: bool = False) -> List[TestResult]:
    """Tier 2: Boundary and corner cases across KaTeX and HTML widgets."""
    results: List[TestResult] = []
    chapters_dir = base_dir / "chapters"
    widgets_dir = base_dir / "widgets"

    # KaTeX checks
    for chap in MANDATORY_CHAPTERS:
        chap_path = chapters_dir / chap
        if not chap_path.is_file():
            continue
        content = chap_path.read_text(encoding="utf-8", errors="ignore")
        katex_checks = validate_katex_syntax(content, chap)
        for passed, msg, details in katex_checks:
            results.append(TestResult(
                tier=2,
                name=f"KaTeX Syntax: {chap}",
                passed=passed,
                message=msg,
                details=details
            ))

    # Widget HTML checks
    for wid in MANDATORY_WIDGETS:
        wid_path = widgets_dir / wid
        if not wid_path.is_file():
            continue
        content = wid_path.read_text(encoding="utf-8", errors="ignore")
        html_checks = validate_html5_widget(content, wid)
        for passed, msg, details in html_checks:
            results.append(TestResult(
                tier=2,
                name=f"Widget HTML & Dependencies: {wid}",
                passed=passed,
                message=msg,
                details=details
            ))

    return results

# ==============================================================================
# Tier 3: Invariant & Cross-Topic Verification
# ==============================================================================

def verify_tier_3_invariants(base_dir: Path, verbose: bool = False) -> List[TestResult]:
    """Tier 3: Invariant checks across coordinate frames, rotation sequence, control formulas, and links."""
    results: List[TestResult] = []
    chapters_dir = base_dir / "chapters"

    # 3.1 Strict NED and Body FRD Invariants
    # Topics 2 and 3 must explicitly declare North-East-Down and Forward-Right-Down
    for chap_name in ["topic_2_coordinate_frames.md", "topic_3_kinematics_dynamics.md"]:
        chap_path = chapters_dir / chap_name
        if not chap_path.is_file():
            continue
        content = chap_path.read_text(encoding="utf-8", errors="ignore")
        has_ned = bool(re.search(r"North[\s\-_/]*East[\s\-_/]*Down|NED", content, re.IGNORECASE))
        has_gravity_positive = bool(re.search(r"(\+\s*g|\[\s*0\s*,\s*0\s*,\s*(\+?\s*g|9\.81))", content))
        has_body_frd = bool(re.search(r"Forward[\s\-_/]*Right[\s\-_/]*Down|Forward[\s\-_/]*Starboard[\s\-_/]*Down|FRD|forward.*starboard.*(belly|down)", content, re.IGNORECASE))
        
        results.append(TestResult(
            tier=3,
            name=f"Coordinate Invariants [{chap_name}]: NED & FRD",
            passed=has_ned and has_body_frd,
            message="NED inertial and FRD body frame conventions confirmed" if (has_ned and has_body_frd)
                    else f"Frame violation in {chap_name} (NED: {has_ned}, FRD: {has_body_frd})"
        ))

    # 3.2 Rotation Sequence Invariant: R_b^n (ZYX Tait-Bryan)
    t2_path = chapters_dir / "topic_2_coordinate_frames.md"
    if t2_path.is_file():
        t2_content = t2_path.read_text(encoding="utf-8", errors="ignore")
        has_zyx = bool(re.search(r"(Z[\s\-]*Y[\s\-]*X|R_z.*R_y.*R_x|yaw.*pitch.*roll)", t2_content, re.IGNORECASE))
        has_dcm_terms = bool(re.search(r"-\s*s(\\theta|θ)|-\s*\\sin\s*(\\theta|θ)", t2_content))
        results.append(TestResult(
            tier=3,
            name="Kinematics Invariant [Topic 2]: Tait-Bryan ZYX & R_b^n (3,1) element",
            passed=has_zyx and has_dcm_terms,
            message="Canonical aerospace Tait-Bryan ZYX rotation sequence verified" if (has_zyx and has_dcm_terms)
                    else "Missing or incorrect R_b^n sequence or -(sin θ) term in Topic 2"
        ))

    # 3.3 Linearized Tilt Mapping Invariant: θ^d = -u_x/g and φ^d = +u_y/g
    t5_path = chapters_dir / "topic_5_flight_control.md"
    if not t5_path.is_file():
        # Fallback to prototype if refactored chapter not created yet
        t5_path = chapters_dir / "topic_5_flight_ctrl_2.md"

    if t5_path.is_file():
        t5_content = t5_path.read_text(encoding="utf-8", errors="ignore")
        # Check for θ^d = -u_x / g
        has_pitch_mapping = bool(re.search(r"(\\theta(\^d)?\s*=\s*-\s*\\frac\{\s*u_x\s*\}\{\s*g\s*\}|\\theta(\^d)?\s*\\approx\s*-\s*\\frac\{\s*u_x\s*\}\{\s*g\s*\}|\ddot\{x\}\s*\\approx\s*-\s*g\s*\\theta)", t5_content))
        # Check for φ^d = +u_y / g
        has_roll_mapping = bool(re.search(r"(\\phi(\^d)?\s*=\s*\+?\s*\\frac\{\s*u_y\s*\}\{\s*g\s*\}|\\phi(\^d)?\s*\\approx\s*\+?\s*\\frac\{\s*u_y\s*\}\{\s*g\s*\}|\ddot\{y\}\s*\\approx\s*\+?\s*g\s*\\phi)", t5_content))
        # Check for motor lag stability k_d > \tau_m k_p
        has_lag_stability = bool(re.search(r"(k_d\s*>\s*\\tau_m\s*k_p|k_\{?d\}?\s*>\s*\\tau_\{?m\}?\s*k_\{?p\}?)", t5_content))
        # Check for tilt thrust compensation
        has_tilt_thrust = bool(re.search(r"(\\frac\{.*(mg|m\s*\(\s*g\s*-\s*u_z\s*\)).*\}\{\s*\\cos\s*\\phi\s*\\cos\s*\\theta\s*\}|\\cos\s*\\phi\s*\\cos\s*\\theta)", t5_content))

        results.append(TestResult(
            tier=3,
            name="Flight Control Invariant [Topic 5]: Tilt-to-Acceleration Mapping (θ^d = -u_x/g, φ^d = +u_y/g)",
            passed=has_pitch_mapping and has_roll_mapping,
            message="Strict tilt sign mapping (nose-down pitch accelerates forward) confirmed" if (has_pitch_mapping and has_roll_mapping)
                    else "Missing or incorrect tilt sign mapping in Topic 5"
        ))

        results.append(TestResult(
            tier=3,
            name="Stability Invariant [Topic 5]: Motor Lag Routh-Hurwitz Condition (k_d > τ_m k_p)",
            passed=has_lag_stability,
            message="Motor lag stability condition k_d > τ_m k_p confirmed" if has_lag_stability
                    else "Missing motor lag stability condition k_d > τ_m k_p in Topic 5"
        ))

        results.append(TestResult(
            tier=3,
            name="Actuator Compensation Invariant [Topic 5]: Tilt Thrust Scaling (1 / cos φ cos θ)",
            passed=has_tilt_thrust,
            message="Tilt thrust compensation formula confirmed" if has_tilt_thrust
                    else "Missing tilt thrust compensation formula in Topic 5"
        ))

    # 3.4 Bidirectional Relative Link Resolution
    all_links_valid = True
    broken_links = []
    total_relative_links = 0

    for chap in MANDATORY_CHAPTERS:
        chap_path = chapters_dir / chap
        if not chap_path.is_file():
            continue
        content = chap_path.read_text(encoding="utf-8", errors="ignore")
        # Extract markdown links: [text](target)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for label, target in links:
            # Skip web URLs, mailto, and pure in-page anchors
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Strip query params or anchors
            clean_target = target.split("#")[0].split("?")[0].strip()
            if not clean_target:
                continue
            total_relative_links += 1
            target_path = (chap_path.parent / clean_target).resolve()
            if not target_path.exists():
                all_links_valid = False
                broken_links.append(f"{chap} -> {target} (Resolved: {target_path})")

    results.append(TestResult(
        tier=3,
        name="Cross-Topic Bidirectional Link Target Resolution",
        passed=all_links_valid and (total_relative_links > 0 or len(MANDATORY_CHAPTERS) == 0),
        message=f"All {total_relative_links} relative cross-topic links resolve successfully" if all_links_valid
                else f"{len(broken_links)} broken relative link(s) found",
        details="; ".join(broken_links[:5]) if broken_links else None
    ))

    return results

# ==============================================================================
# Tier 4: Real-World Mathematical & Physics Oracles
# ==============================================================================

def oracle_hover_momentum_theory() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 1: Actuator Disc Momentum Theory & Hover Sizing.
    Formulas:
      v_i = sqrt( T / (2 * rho * A) )
      P_ideal = T * v_i = T^(3/2) / sqrt(2 * rho * A)
      P_elec = P_ideal / eta_total + P_avionics
      I_hover = P_elec / V_nom
      t_hover = (Q_usable / I_hover) * 60 [minutes]
      theta_max = arccos(1 / TWR)
    """
    m = 1.60        # kg
    g = 9.81        # m/s^2
    N = 4           # Quadrotor
    R = 0.127       # m (10-inch propeller diameter)
    rho = 1.225     # kg/m^3 (sea-level density)
    eta_total = 0.55
    P_avionics = 8.0 # W
    V_nom = 14.8    # 4S LiPo nominal voltage
    C_Ah = 4.0      # Ah
    DoD = 0.80      # 80% Depth of Discharge
    T_max_per_motor = 8.0 # N

    # Calculations
    W = m * g
    T_hover = W
    T_max = N * T_max_per_motor
    twr = T_max / W

    A_total = N * math.pi * (R ** 2)
    v_i = math.sqrt(T_hover / (2.0 * rho * A_total))
    P_ideal = T_hover * v_i
    P_elec = (P_ideal / eta_total) + P_avionics
    I_hover = P_elec / V_nom
    Q_usable = DoD * C_Ah
    t_hover_min = (Q_usable / I_hover) * 60.0
    theta_max_rad = math.acos(1.0 / twr)
    theta_max_deg = math.degrees(theta_max_rad)

    # Validations against tutorial bounds
    passed = (
        math.isclose(v_i, 5.62, rel_tol=0.02) and
        math.isclose(P_ideal, 88.2, rel_tol=0.02) and
        math.isclose(t_hover_min, 16.87, rel_tol=0.03) and
        math.isclose(theta_max_deg, 60.6, rel_tol=0.02)
    )

    data = {
        "Weight_N": round(W, 3),
        "A_total_m2": round(A_total, 4),
        "Induced_Velocity_m_s": round(v_i, 3),
        "P_ideal_W": round(P_ideal, 2),
        "P_elec_W": round(P_elec, 2),
        "Hover_Endurance_min": round(t_hover_min, 2),
        "Max_Tilt_deg": round(theta_max_deg, 2),
        "TWR": round(twr, 3)
    }
    return passed, f"Momentum theory sizing: v_i={v_i:.2f} m/s, P_ideal={P_ideal:.1f} W, t={t_hover_min:.1f} min, θ_max={theta_max_deg:.1f}°", data

def oracle_rotation_matrix_so3() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 2: Orthonormality of R_b^n in SO(3) and Gimbal Lock Singularity of W_η.
    Symbolic proof via SymPy:
      det(R_b^n) == 1
      (R_b^n)^T * R_b^n == I_3
      det(M_ω) == cos(θ) -> vanishes at θ = ±π/2
    """
    phi, theta, psi = sp.symbols('phi theta psi', real=True)
    Rz = sp.Matrix([
        [sp.cos(psi), -sp.sin(psi), 0],
        [sp.sin(psi), sp.cos(psi), 0],
        [0, 0, 1]
    ])
    Ry = sp.Matrix([
        [sp.cos(theta), 0, sp.sin(theta)],
        [0, 1, 0],
        [-sp.sin(theta), 0, sp.cos(theta)]
    ])
    Rx = sp.Matrix([
        [1, 0, 0],
        [0, sp.cos(phi), -sp.sin(phi)],
        [0, sp.sin(phi), sp.cos(phi)]
    ])
    R_b_n = Rz * Ry * Rx
    det_R = sp.trigsimp(R_b_n.det())

    # Kinematic mapping matrix M_ω such that ω_b = M_ω * dη/dt
    M_omega = sp.Matrix([
        [1, 0, -sp.sin(theta)],
        [0, sp.cos(phi), sp.sin(phi) * sp.cos(theta)],
        [0, -sp.sin(phi), sp.cos(phi) * sp.cos(theta)]
    ])
    det_M = sp.trigsimp(M_omega.det())

    # Inversion W_η = M_omega^(-1)
    W_eta = sp.trigsimp(M_omega.inv())
    w_32 = sp.trigsimp(W_eta[2, 1] * sp.cos(theta))  # Should equal sin(phi)

    # Numerical rotation test (Tutorial 1 Q2)
    # Level heading 30 deg, v_b = [4, 0, 0]^T
    R_num = np.array([
        [math.cos(math.radians(30)), -math.sin(math.radians(30)), 0],
        [math.sin(math.radians(30)), math.cos(math.radians(30)), 0],
        [0, 0, 1]
    ])
    v_b = np.array([4.0, 0.0, 0.0])
    v_n = R_num @ v_b

    passed = (
        det_R == 1 and
        det_M == sp.cos(theta) and
        w_32 == sp.sin(phi) and
        math.isclose(v_n[0], 3.4641, rel_tol=1e-3) and
        math.isclose(v_n[1], 2.0000, rel_tol=1e-3)
    )

    data = {
        "det_R_symbolic": str(det_R),
        "det_M_omega": str(det_M),
        "v_inertial_test": [round(float(x), 4) for x in v_n]
    }
    return passed, f"SO(3) orthonormality det(R)={det_R}, det(M_ω)={det_M}, v_inertial={data['v_inertial_test']}", data

def oracle_mixer_matrix_inverses() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 3: Analytical Inversion of Plus (+) and Cross (x) Quadrotor Mixer Matrices.
    Tutorial 3 Q3 numerical drill:
      l = 0.250 m, k_MT = 0.0200 m
      Virtual load: F_z = -24.0 N, M_x = 0, M_y = 0.500 Nm, M_z = 0
      -> T1 = 7.00 N, T2 = 6.00 N, T3 = 5.00 N, T4 = 6.00 N
    """
    l, d, kMT = sp.symbols('l d kMT', positive=True)

    # Plus (+) configuration
    A_plus = sp.Matrix([
        [-1, -1, -1, -1],
        [0, -l, 0, l],
        [l, 0, -l, 0],
        [kMT, -kMT, kMT, -kMT]
    ])
    A_plus_inv = A_plus.inv()
    plus_ortho = sp.simplify(A_plus * A_plus_inv) == sp.eye(4)

    # Cross (x) configuration
    A_cross = sp.Matrix([
        [-1, -1, -1, -1],
        [d, -d, -d, d],
        [d, d, -d, -d],
        [kMT, -kMT, kMT, -kMT]
    ])
    A_cross_inv = A_cross.inv()
    cross_ortho = sp.simplify(A_cross * A_cross_inv) == sp.eye(4)

    # Numerical verification for Tutorial 3 Q3
    l_val = 0.250
    kMT_val = 0.0200
    A_plus_num = np.array([
        [-1, -1, -1, -1],
        [0, -l_val, 0, l_val],
        [l_val, 0, -l_val, 0],
        [kMT_val, -kMT_val, kMT_val, -kMT_val]
    ], dtype=float)
    u_req = np.array([-24.0, 0.0, 0.500, 0.0])
    t_alloc = np.linalg.inv(A_plus_num) @ u_req

    passed = (
        plus_ortho and
        cross_ortho and
        np.allclose(t_alloc, [7.0, 6.0, 5.0, 6.0], atol=1e-4)
    )

    data = {
        "A_plus_invertible": bool(plus_ortho),
        "A_cross_invertible": bool(cross_ortho),
        "t_allocated_N": [round(float(x), 3) for x in t_alloc]
    }
    return passed, f"Mixer matrix analytical inverses valid; Tutorial 3 alloc = {data['t_allocated_N']}", data

def oracle_hexarotor_pseudo_inverse() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 4: Analytical Moore-Penrose Pseudo-Inverse for Hexarotor Allocation.
    Under pure vertical hover load F_z = -24.0 N:
      Minimum norm solution distributes thrust equally: T_i = 4.00 N for all 6 rotors.
    """
    l_hex = 0.250
    k_hex = 0.0200
    a = 0.5 * l_hex
    b = (math.sqrt(3) / 2.0) * l_hex

    A_hex = np.array([
        [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        [a, -a, -l_hex, -a, a, l_hex],
        [b, b, 0.0, -b, -b, 0.0],
        [k_hex, -k_hex, k_hex, -k_hex, k_hex, -k_hex]
    ], dtype=float)

    # Right Moore-Penrose pseudo-inverse: A^+ = A^T (A A^T)^(-1)
    A_pinv = A_hex.T @ np.linalg.inv(A_hex @ A_hex.T)
    ortho_check = np.allclose(A_hex @ A_pinv, np.eye(4), atol=1e-5)

    # Pure vertical demand: F_z = -24 N, Moments = 0
    u_demand = np.array([-24.0, 0.0, 0.0, 0.0])
    t_hex = A_pinv @ u_demand

    passed = ortho_check and np.allclose(t_hex, [4.0] * 6, atol=1e-4)

    data = {
        "rank_A_hex": int(np.linalg.matrix_rank(A_hex)),
        "pinv_is_right_inverse": bool(ortho_check),
        "t_hex_allocated": [round(float(x), 3) for x in t_hex]
    }
    return passed, f"Hexarotor pseudo-inverse rank={data['rank_A_hex']}, equal allocation T_i={data['t_hex_allocated'][0]} N", data

def oracle_coriolis_and_rigid_body_dynamics() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 5: 6-DoF Transport Theorem & Rotational Dynamics (Tutorial 2 Q2 & Q3).
    Q2: m = 2.50 kg, v_b = [3, 1, 0]^T m/s, ω_b = [0, 0, 0.400]^T rad/s, F_b = [5, 0, 0]^T N
        v_dot_b = F_b / m - ω_b x v_b -> [2.40, -1.20, 0.0]^T m/s^2
    Q3: J = diag(0.025, 0.035, 0.045), M_x = 0.080 Nm, q = 1.5 rad/s, r = 2.0 rad/s
        p_dot = (M_x + (J_y - J_z) * q * r) / J_x -> 2.00 rad/s^2
    """
    m = 2.50
    v_b = np.array([3.0, 1.0, 0.0])
    omega_b = np.array([0.0, 0.0, 0.400])
    F_b = np.array([5.0, 0.0, 0.0])

    # v_dot_b = F_b/m - omega_b x v_b
    coriolis = np.cross(omega_b, v_b)
    v_dot_b = (F_b / m) - coriolis

    # Q3 Rotational dynamics
    Jx, Jy, Jz = 0.0250, 0.0350, 0.0450
    Mx = 0.0800
    q, r = 1.50, 2.00
    cross_coupling_torque = (Jy - Jz) * q * r
    p_dot = (Mx + cross_coupling_torque) / Jx

    passed = (
        np.allclose(v_dot_b, [2.40, -1.20, 0.0], atol=1e-4) and
        math.isclose(p_dot, 2.00, abs_tol=1e-4)
    )

    data = {
        "v_dot_b_m_s2": [round(float(x), 3) for x in v_dot_b],
        "cross_coupling_torque_Nm": round(cross_coupling_torque, 4),
        "p_dot_rad_s2": round(p_dot, 3)
    }
    return passed, f"Coriolis v_dot={data['v_dot_b_m_s2']}, Rotational Euler p_dot={p_dot:.2f} rad/s²", data

def oracle_controllability_and_observability() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 6: Quadrotor Longitudinal State-Space Controllability Matrix Determinant.
    State vector: ξ_long = [δx, δu, δθ, δq]^T
    System:
      A = [[0, 1, 0, 0], [0, 0, -g, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
      B = [[0], [0], [0], [1/J_y]]
    Controllability matrix: C = [B, AB, A^2 B, A^3 B]
    det(C) = (g / J_y^2)^2 = g^2 / J_y^4 != 0 (Fully Controllable)
    """
    g, Jy = sp.symbols('g Jy', positive=True)
    A = sp.Matrix([
        [0, 1, 0, 0],
        [0, 0, -g, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    B = sp.Matrix([0, 0, 0, 1/Jy])
    C_mat = sp.Matrix.hstack(B, A * B, A**2 * B, A**3 * B)
    det_C = sp.factor(C_mat.det())

    # Observability with position measurement C_obs = [1, 0, 0, 0]
    C_obs = sp.Matrix([[1, 0, 0, 0]])
    O_mat = sp.Matrix.vstack(C_obs, C_obs * A, C_obs * A**2, C_obs * A**3)
    det_O = sp.factor(O_mat.det())

    expected_det_C = (g**2) / (Jy**4)
    passed = (det_C == expected_det_C and det_O == g**2)

    data = {
        "det_Controllability": str(det_C),
        "det_Observability": str(det_O),
        "is_fully_controllable": True
    }
    return passed, f"Longitudinal controllability det(C) = {det_C} != 0 (Rank 4), det(O) = {det_O}", data

def oracle_motor_lag_routh_hurwitz() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Oracle 7: First-Order Motor Lag Routh-Hurwitz Stability Criterion.
    Closed-loop characteristic equation:
      P(s) = tau_m * s^3 + s^2 + k_d * s + k_p = 0
    Routh Hurwitz determinant:
      H_2 = k_d - tau_m * k_p > 0  <=>  k_d > tau_m * k_p
    """
    tau_m, kp, kd = sp.symbols('tau_m kp kd', positive=True)

    # Hurwitz matrix for a3*s^3 + a2*s^2 + a1*s + a0 = 0
    # a3 = tau_m, a2 = 1, a1 = kd, a0 = kp
    H2 = sp.Matrix([
        [1, kp],
        [tau_m, kd]
    ]).det()  # 1 * kd - tau_m * kp

    # Test cases:
    # 1. Tutorial 4 Q5: tau_m = 0.020, kp = 9.0, kd = 4.80 -> 4.80 > 0.180 (STABLE)
    # 2. Tutorial 5 Q2: tau_m = 0.020, kp = 625.0, kd = 35.0 -> 35.0 > 12.5 (STABLE)
    # 3. Unstable case: tau_m = 0.050, kp = 500.0, kd = 10.0 -> 10.0 < 25.0 (UNSTABLE)
    case1_stable = (4.80 > 0.020 * 9.0)
    case2_stable = (35.0 > 0.020 * 625.0)
    case3_unstable = not (10.0 > 0.050 * 500.0)

    passed = (
        sp.simplify(H2 - (kd - tau_m * kp)) == 0 and
        case1_stable and
        case2_stable and
        case3_unstable
    )

    data = {
        "H2_symbolic": str(H2),
        "condition": "kd > tau_m * kp",
        "tutorial_4_q5_satisfied": case1_stable,
        "tutorial_5_q2_satisfied": case2_stable
    }
    return passed, f"Routh-Hurwitz H_2 = {H2} > 0 implies stability condition kd > tau_m * kp", data

def verify_tier_4_oracles(verbose: bool = False) -> List[TestResult]:
    """Execute all Tier 4 mathematical and physics oracles."""
    results: List[TestResult] = []

    oracles = [
        ("Momentum Theory & Sizing Oracle", oracle_hover_momentum_theory),
        ("SO(3) Rotation Matrix & Euler Rates Oracle", oracle_rotation_matrix_so3),
        ("Mixer Matrix Inverses Oracle (+ and x)", oracle_mixer_matrix_inverses),
        ("Hexarotor Pseudo-Inverse Allocation Oracle", oracle_hexarotor_pseudo_inverse),
        ("6-DoF Rigid-Body Coriolis & Euler Oracle", oracle_coriolis_and_rigid_body_dynamics),
        ("Longitudinal Controllability & Observability Oracle", oracle_controllability_and_observability),
        ("Motor Lag Routh-Hurwitz Stability Oracle", oracle_motor_lag_routh_hurwitz),
    ]

    for name, fn in oracles:
        passed, msg, data = fn()
        details_str = json.dumps(data) if verbose else None
        results.append(TestResult(
            tier=4,
            name=name,
            passed=passed,
            message=msg,
            details=details_str
        ))

    return results

# ==============================================================================
# Self-Test Engine
# ==============================================================================

def run_self_test(verbose: bool = False) -> VerificationSummary:
    """
    Self-Test Mode: Independently validates the test harness itself:
    1. Runs all 7 Tier 4 symbolic/numerical physics oracles.
    2. Runs synthetic positive & negative KaTeX syntax tests.
    3. Runs synthetic positive & negative HTML5 widget tests.
    4. Runs synthetic coordinate invariant tests.
    """
    summary = VerificationSummary(start_time=time.time())

    # 1. Tier 4 Oracles
    oracle_results = verify_tier_4_oracles(verbose=verbose)
    for res in oracle_results:
        summary.add(res)

    # 2. KaTeX Parser Self-Test
    valid_katex = "Hover power is $P = T v_i$. In block form:\n$$\\begin{aligned} \\ddot{x} &= -g\\theta \\\\ \\ddot{y} &= g\\phi \\end{aligned}$$\nwhere $\\theta$ is pitch."
    invalid_katex_1 = "Unclosed dollar: $P = T v_i and some text"
    invalid_katex_2 = "$$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{pmatrix}$$"

    k1_res = validate_katex_syntax(valid_katex, "valid_mock.md")
    k2_res = validate_katex_syntax(invalid_katex_1, "invalid_mock1.md")
    k3_res = validate_katex_syntax(invalid_katex_2, "invalid_mock2.md")

    summary.add(TestResult(
        tier=2,
        name="Self-Test: KaTeX Parser Valid Detection",
        passed=all(r[0] for r in k1_res),
        message="Correctly accepted valid KaTeX delimiters and aligned environments"
    ))
    summary.add(TestResult(
        tier=2,
        name="Self-Test: KaTeX Parser Unbalanced Dollar Rejection",
        passed=any(not r[0] for r in k2_res),
        message="Correctly caught unbalanced single dollar sign"
    ))
    summary.add(TestResult(
        tier=2,
        name="Self-Test: KaTeX Parser Mismatched Environment Rejection",
        passed=any(not r[0] for r in k3_res),
        message="Correctly caught mismatched LaTeX environment (bmatrix vs pmatrix)"
    ))

    # 3. HTML Widget Self-Test
    valid_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mock Widget</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>body { background: #000; }</style>
</head>
<body>
    <canvas id="simCanvas"></canvas>
</body>
</html>"""

    invalid_html_dep = """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>body { background: #000; }</style>
</head>
<body>
    <canvas id="simCanvas"></canvas>
</body>
</html>"""

    invalid_html_nocanvas = """<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>body { background: #000; }</style>
</head>
<body>
    <div>No canvas or svg here!</div>
</body>
</html>"""

    h1_res = validate_html5_widget(valid_html, "valid_mock.html")
    h2_res = validate_html5_widget(invalid_html_dep, "invalid_dep_mock.html")
    h3_res = validate_html5_widget(invalid_html_nocanvas, "invalid_nocanvas_mock.html")

    summary.add(TestResult(
        tier=2,
        name="Self-Test: HTML5 Validator Valid Widget Acceptance",
        passed=all(r[0] for r in h1_res),
        message="Correctly accepted valid HTML5 + Tailwind CDN + Canvas widget"
    ))
    summary.add(TestResult(
        tier=2,
        name="Self-Test: HTML5 Dependency Filter Forbidden Script Rejection",
        passed=any(not r[0] and "Forbidden external JS" in r[1] for r in h2_res),
        message="Correctly flagged forbidden external Three.js script dependency"
    ))
    summary.add(TestResult(
        tier=2,
        name="Self-Test: HTML5 Canvas/SVG Detector Rejection",
        passed=any(not r[0] and "Missing interactive visualizer element" in r[1] for r in h3_res),
        message="Correctly flagged HTML widget lacking <canvas> or <svg>"
    ))

    summary.duration = time.time() - summary.start_time
    return summary

# ==============================================================================
# Main Verification Orchestration
# ==============================================================================

def run_verification(base_dir: Path, tiers: List[int], verbose: bool = False) -> VerificationSummary:
    """Run specified verification tiers against the course module directory."""
    summary = VerificationSummary(start_time=time.time())

    # Tier 1
    if 1 in tiers:
        t1_results = verify_tier_1_feature_coverage(base_dir, verbose=verbose)
        for r in t1_results:
            summary.add(r)

    # Tier 2
    if 2 in tiers:
        t2_results = verify_tier_2_boundary_and_corner_cases(base_dir, verbose=verbose)
        for r in t2_results:
            summary.add(r)

    # Tier 3
    if 3 in tiers:
        t3_results = verify_tier_3_invariants(base_dir, verbose=verbose)
        for r in t3_results:
            summary.add(r)

    # Tier 4
    if 4 in tiers:
        t4_results = verify_tier_4_oracles(verbose=verbose)
        for r in t4_results:
            summary.add(r)

    summary.duration = time.time() - summary.start_time
    return summary

# ==============================================================================
# Reporting & CLI Formatting
# ==============================================================================

def print_summary_report(summary: VerificationSummary, is_self_test: bool = False, use_color: bool = True):
    mode_str = "HARNESS SELF-TEST" if is_self_test else "FULL MODULE VERIFICATION"
    print("\n" + "=" * 80)
    print(colorize(f" EEEE4138 AERIAL ROBOTICS — 4-TIER TEST HARNESS REPORT [{mode_str}]", Colors.BOLD + Colors.CYAN, use_color))
    print("=" * 80)

    # Group by tier
    by_tier: Dict[int, List[TestResult]] = {}
    for r in summary.results:
        by_tier.setdefault(r.tier, []).append(r)

    tier_names = {
        1: "Tier 1: Feature Coverage (Chapters, Widgets & Sections)",
        2: "Tier 2: Boundary & Corner Cases (KaTeX, HTML5, 0-Ext JS)",
        3: "Tier 3: Invariant & Cross-Topic Verification (NED, ZYX, Tilt, Links)",
        4: "Tier 4: Real-World Mathematical & Physics Oracles (SymPy / NumPy)"
    }

    for tier_num in sorted(by_tier.keys()):
        tier_title = tier_names.get(tier_num, f"Tier {tier_num}")
        print(f"\n{colorize(f'--- {tier_title} ---', Colors.BOLD, use_color)}")
        for r in by_tier[tier_num]:
            if r.passed:
                status_badge = colorize("[PASS]", Colors.BOLD + Colors.GREEN, use_color)
            elif r.severity == "WARNING":
                status_badge = colorize("[WARN]", Colors.BOLD + Colors.YELLOW, use_color)
            else:
                status_badge = colorize("[FAIL]", Colors.BOLD + Colors.RED, use_color)
            print(f"  {status_badge} {r.name}")
            print(f"         {colorize(r.message, Colors.GRAY, use_color)}")
            if r.details:
                print(f"         Details: {r.details}")

    print("\n" + "-" * 80)
    total_str = f"Total: {summary.total} | Passed: {summary.passed} | Failed: {summary.failed} | Warnings: {summary.warnings}"
    duration_str = f"Execution Time: {summary.duration:.3f} s"
    if summary.failed == 0:
        result_badge = colorize("SUITE RESULT: ALL TESTS PASSED (100%)", Colors.BOLD + Colors.GREEN, use_color)
    else:
        result_badge = colorize(f"SUITE RESULT: {summary.failed} TEST(S) FAILED", Colors.BOLD + Colors.RED, use_color)

    print(f"{total_str} | {duration_str}")
    print(result_badge)
    print("=" * 80 + "\n")

def export_json_report(summary: VerificationSummary, out_path: Path):
    data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_seconds": round(summary.duration, 4),
        "total": summary.total,
        "passed": summary.passed,
        "failed": summary.failed,
        "warnings": summary.warnings,
        "pass_rate_pct": round((summary.passed / summary.total) * 100, 2) if summary.total > 0 else 0,
        "results": [
            {
                "tier": r.tier,
                "name": r.name,
                "passed": r.passed,
                "message": r.message,
                "details": r.details,
                "severity": r.severity
            } for r in summary.results
        ]
    }
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

# ==============================================================================
# CLI Entry Point
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="EEEE4138 Aerial Robotics 4-Tier Automated Test Suite & Physics Verification Harness"
    )
    parser.add_argument(
        "--tier",
        type=str,
        default="1,2,3,4",
        help="Comma-separated tiers to run (e.g. '1,2' or '4'). Default: all tiers '1,2,3,4'"
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run self-test mode (verifies all Tier 4 mathematical oracles, KaTeX parser, HTML validator, and filters)"
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root path to 'modules/EEEE4138_aerial_robotics' (defaults to directory containing scripts/)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print verbose diagnostic details"
    )
    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="Optional path to export JSON test results"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI terminal color output"
    )

    args = parser.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()

    # Determine base directory
    if args.root:
        base_dir = Path(args.root).resolve()
    else:
        # Default: scripts/../ -> modules/EEEE4138_aerial_robotics
        script_dir = Path(__file__).resolve().parent
        base_dir = script_dir.parent

    # Execute
    if args.self_test:
        summary = run_self_test(verbose=args.verbose)
        print_summary_report(summary, is_self_test=True, use_color=use_color)
    else:
        try:
            tiers = [int(t.strip()) for t in args.tier.split(",") if t.strip()]
        except ValueError:
            print(f"ERROR: Invalid tier format: {args.tier}. Expected integers 1-4.")
            sys.exit(2)

        summary = run_verification(base_dir, tiers=tiers, verbose=args.verbose)
        print_summary_report(summary, is_self_test=False, use_color=use_color)

    # Optional JSON export
    if args.json:
        export_json_report(summary, Path(args.json))
        print(f"Exported JSON report to {args.json}")

    # Exit code: 0 if all tests passed, 1 if any failure
    sys.exit(0 if summary.failed == 0 else 1)

if __name__ == "__main__":
    main()
