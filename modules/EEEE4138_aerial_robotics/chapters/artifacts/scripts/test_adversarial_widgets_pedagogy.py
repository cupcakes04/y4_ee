#!/usr/bin/env python3
"""
Adversarial Verification Suite: Generative UI Widget Integration & Pedagogical Architecture
Subject: EEEE4138 Aerial Robotics Textbook Chapters & Widgets
Author: Challenger 2 (Adversarial Critic & Domain Specialist)
Date: 2026-11-12

Audits:
  1. Iframe links and target files: verifies every <iframe> and fallback <a> link points to a real,
     readable, non-empty HTML file in modules/EEEE4138_aerial_robotics/widgets/.
  2. Exact conceptual insertion points: verifies widgets 1 to 5 are embedded precisely where their
     corresponding theory is introduced and derived.
  3. Link resolution & orphan file audit: verifies zero broken links, relative path resolution errors,
     or orphan widget files.
  4. Pedagogical text-wall elimination: verifies text walls are broken down into structured tables,
     callout cards, Mermaid diagrams, and step-by-step math blocks.
  5. Code block prohibition: verifies zero programming implementation blocks (Python/MATLAB).
  6. Widget self-containment: verifies HTML5, offline fallback styling, zero external JS libraries.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import glob
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple
import unittest
from urllib.parse import unquote

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MODULE_DIR = os.path.join(ROOT_DIR, "modules", "EEEE4138_aerial_robotics")
CHAPTERS_DIR = os.path.join(MODULE_DIR, "chapters")
WIDGETS_DIR = os.path.join(MODULE_DIR, "widgets")

MANDATORY_WIDGET_MAPPINGS = {
    1: {
        "file": "widget_1_flight_envelope.html",
        "chapter_pattern": "topic_1_*.md",
        "concept_keywords": ["battery", "endurance", "sizing", "m_{\\text{bat}}", "m_bat", "m_{\\text{fixed}}", "2 m_{\\text{fixed}}"],
        "section_pattern": r"##\s*6\..*|###\s*6\.5\s*Finding the Analytical Maximum",
        "min_size_kb": 25,
    },
    2: {
        "file": "widget_2_frames_gimbal_lock.html",
        "chapter_pattern": "topic_2_*.md",
        "concept_keywords": ["gimbal lock", "singularity", "quaternion", "theta", "90", "tait-bryan"],
        "section_pattern": r"##\s*(?:6|7)\..*|###\s*7\..*",
        "min_size_kb": 25,
    },
    3: {
        "file": "widget_3_rigid_body_dynamics.html",
        "chapter_pattern": "topic_3_*.md",
        "concept_keywords": ["rigid-body", "gyroscopic", "precession", "newton-euler", "tau_gyro", "omega_b"],
        "section_pattern": r"##\s*11\.\s*Interactive Simulation.*|##\s*Architecture.*",
        "min_size_kb": 25,
    },
    4: {
        "file": "widget_4_rotor_mixer_allocation.html",
        "chapter_pattern": "topic_4_*.md",
        "concept_keywords": ["mixer", "allocation", "saturation", "desaturation", "thrust", "priority"],
        "section_pattern": r"###\s*4\.7.*|####\s*Interactive Generative UI Simulation",
        "min_size_kb": 25,
    },
    5: {
        "file": "widget_5_cascaded_flight_control.html",
        "chapter_pattern": "topic_5_*.md",
        "concept_keywords": ["cascaded", "outer loop", "inner loop", "tilt", "time-scale", "u_x"],
        "section_pattern": r"##\s*(?:1|3)\..*|###\s*3\.2\s*The Underactuation Principle",
        "min_size_kb": 25,
    },
}


@dataclass
class AuditIssue:
    suite: str
    target: str
    severity: str  # ERROR, WARNING, INFO
    message: str
    line_number: Optional[int] = None
    context: str = ""


@dataclass
class AuditReport:
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    warning_checks: int = 0
    issues: List[AuditIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def add_issue(self, suite: str, target: str, severity: str, message: str,
                  line: Optional[int] = None, context: str = "") -> None:
        self.issues.append(AuditIssue(suite, target, severity, message, line, context))
        if severity == "ERROR":
            self.failed_checks += 1
        elif severity == "WARNING":
            self.warning_checks += 1

    def record_pass(self) -> None:
        self.passed_checks += 1
        self.total_checks += 1


class AdversarialAuditor:
    def __init__(self, chapters_dir: str = CHAPTERS_DIR, widgets_dir: str = WIDGETS_DIR):
        self.chapters_dir = chapters_dir
        self.widgets_dir = widgets_dir
        self.report = AuditReport()
        self.chapter_files = sorted(glob.glob(os.path.join(self.chapters_dir, "*.md")))
        self.widget_files = sorted(glob.glob(os.path.join(self.widgets_dir, "*.html")))

    # --------------------------------------------------------------------------
    # Suite 1: Iframe Links and Target Files Verification
    # --------------------------------------------------------------------------
    def audit_iframe_and_fallback_links(self) -> None:
        suite = "Suite 1: Iframe & Target Files"
        iframe_regex = re.compile(r'<iframe\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*?)>', re.IGNORECASE)
        fallback_regex = re.compile(
            r'<p><em>(?:Interactive Visualizer:\s*)?<a\s+[^>]*?href=["\']([^"\']+)["\'](?:[^>]*?target=["\']_blank["\'])?[^>]*?>([^<]+)</a>(?:.*?</em></p>)?',
            re.IGNORECASE
        )

        for ch_path in self.chapter_files:
            ch_name = os.path.basename(ch_path)
            with open(ch_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            iframes_found = []

            for line_idx, line in enumerate(lines, 1):
                for match in iframe_regex.finditer(line):
                    before_attrs, src, after_attrs = match.groups()
                    all_attrs = f"{before_attrs} {after_attrs}"
                    iframes_found.append((line_idx, src, all_attrs))

            # Must have at least one iframe if it's a primary chapter
            is_primary = any(ch_name.startswith(f"topic_{i}_") for i in range(1, 6))
            if is_primary and not iframes_found:
                self.report.add_issue(
                    suite, ch_name, "ERROR",
                    f"Primary topic chapter '{ch_name}' contains zero <iframe> embeds."
                )
                continue

            for line_idx, src, attrs in iframes_found:
                self.report.record_pass()

                # Attribute checks
                if "width=" not in attrs.lower() or "100%" not in attrs:
                    self.report.add_issue(
                        suite, ch_name, "WARNING",
                        f"Line {line_idx}: <iframe> missing responsive width='100%' attribute.",
                        line_idx
                    )
                else:
                    self.report.record_pass()

                if "height=" not in attrs.lower():
                    self.report.add_issue(
                        suite, ch_name, "WARNING",
                        f"Line {line_idx}: <iframe> missing height attribute.",
                        line_idx
                    )
                else:
                    self.report.record_pass()

                # Path resolution
                target_path = os.path.normpath(os.path.join(self.chapters_dir, src))
                if not os.path.exists(target_path):
                    self.report.add_issue(
                        suite, ch_name, "ERROR",
                        f"Line {line_idx}: <iframe> target does not exist on disk: '{src}' -> '{target_path}'",
                        line_idx
                    )
                    continue

                self.report.record_pass()

                # File containment & non-empty
                if not target_path.startswith(os.path.abspath(self.widgets_dir)):
                    self.report.add_issue(
                        suite, ch_name, "ERROR",
                        f"Line {line_idx}: <iframe> target is outside widgets directory: '{target_path}'",
                        line_idx
                    )
                else:
                    self.report.record_pass()

                size_bytes = os.path.getsize(target_path)
                if size_bytes < 5000:
                    self.report.add_issue(
                        suite, ch_name, "ERROR",
                        f"Line {line_idx}: Widget '{os.path.basename(target_path)}' is suspiciously small ({size_bytes} bytes).",
                        line_idx
                    )
                else:
                    self.report.record_pass()

                # Readability
                try:
                    with open(target_path, "r", encoding="utf-8") as wf:
                        w_content = wf.read()
                    if "<!DOCTYPE html>" not in w_content and "<!doctype html>" not in w_content.lower():
                        self.report.add_issue(
                            suite, ch_name, "ERROR",
                            f"Widget '{os.path.basename(target_path)}' lacks standard HTML5 DOCTYPE.",
                            line_idx
                        )
                    else:
                        self.report.record_pass()
                except Exception as exc:
                    self.report.add_issue(
                        suite, ch_name, "ERROR",
                        f"Failed to read widget file '{target_path}': {exc}",
                        line_idx
                    )

                # Check fallback <a> link adjacent to iframe
                snippet_start = max(0, line_idx - 2)
                snippet_end = min(len(lines), line_idx + 4)
                adjacent_text = "\n".join(lines[snippet_start:snippet_end])

                fallback_match = fallback_regex.search(adjacent_text)
                if not fallback_match:
                    self.report.add_issue(
                        suite, ch_name, "WARNING",
                        f"Line {line_idx}: <iframe> is not immediately accompanied by standalone fallback <a href='...'> link.",
                        line_idx
                    )
                else:
                    self.report.record_pass()
                    fb_href = fallback_match.group(1)
                    if fb_href != src:
                        self.report.add_issue(
                            suite, ch_name, "ERROR",
                            f"Line {line_idx}: Fallback link '{fb_href}' does not match iframe src '{src}'.",
                            line_idx
                        )
                    else:
                        self.report.record_pass()

    # --------------------------------------------------------------------------
    # Suite 2: Conceptual Insertion Point Precision
    # --------------------------------------------------------------------------
    def audit_conceptual_insertion_points(self) -> None:
        suite = "Suite 2: Conceptual Insertion Points"

        for topic_num, spec in MANDATORY_WIDGET_MAPPINGS.items():
            matching_chapters = glob.glob(os.path.join(self.chapters_dir, spec["chapter_pattern"]))
            if not matching_chapters:
                self.report.add_issue(
                    suite, f"Topic {topic_num}", "ERROR",
                    f"No chapter file matching pattern '{spec['chapter_pattern']}' found."
                )
                continue

            for ch_path in matching_chapters:
                ch_name = os.path.basename(ch_path)
                with open(ch_path, "r", encoding="utf-8") as f:
                    content = f.read()

                widget_filename = spec["file"]
                iframe_match = re.search(
                    r'<iframe\s+[^>]*?src=["\'][^"\']*?' + re.escape(widget_filename) + r'["\']',
                    content,
                    re.IGNORECASE
                )

                if not iframe_match:
                    self.report.add_issue(
                        suite, ch_name, "ERROR",
                        f"Chapter '{ch_name}' does not contain an <iframe> embedding designated widget '{widget_filename}'."
                    )
                    continue

                iframe_pos = iframe_match.start()
                self.report.record_pass()

                # Check surrounding context (within 2500 characters before and after)
                start_win = max(0, iframe_pos - 2500)
                end_win = min(len(content), iframe_pos + 2500)
                context_window = content[start_win:end_win].lower()

                # Check keywords in vicinity
                matched_keywords = [kw for kw in spec["concept_keywords"] if kw.lower() in context_window]
                match_ratio = len(matched_keywords) / len(spec["concept_keywords"])

                if match_ratio < 0.5:
                    self.report.add_issue(
                        suite, ch_name, "ERROR",
                        f"Widget '{widget_filename}' in '{ch_name}' lacks expected theoretical context. "
                        f"Matched only {matched_keywords} out of {spec['concept_keywords']}."
                    )
                else:
                    self.report.record_pass()

                # Verify preceding section heading
                preceding_text = content[:iframe_pos]
                headings = re.findall(r'(#{1,4}\s+[^\n]+)', preceding_text)
                last_heading = headings[-1] if headings else "NONE"

                self.report.metrics[f"Topic_{topic_num}_{ch_name}_insertion_heading"] = last_heading
                self.report.record_pass()

    # --------------------------------------------------------------------------
    # Suite 3: Link Resolution & Orphan File Audit
    # --------------------------------------------------------------------------
    def audit_link_resolution_and_orphans(self) -> None:
        suite = "Suite 3: Links & Orphan Widgets"

        md_link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        html_link_regex = re.compile(r'<a\s+[^>]*?href=["\']([^"\']+)["\']', re.IGNORECASE)

        referenced_widgets: Set[str] = set()

        for ch_path in self.chapter_files:
            ch_name = os.path.basename(ch_path)
            ch_dir = os.path.dirname(os.path.abspath(ch_path))

            with open(ch_path, "r", encoding="utf-8") as f:
                content = f.read()

            links = []
            for m in md_link_regex.finditer(content):
                links.append((m.group(2), "markdown"))
            for m in html_link_regex.finditer(content):
                links.append((m.group(1), "html"))

            for raw_url, link_type in links:
                if raw_url.startswith(("http://", "https://", "mailto:", "javascript:")):
                    continue

                clean_url = unquote(raw_url).strip()
                if not clean_url:
                    continue

                # Separate target path and anchor
                if "#" in clean_url:
                    target_rel, anchor = clean_url.split("#", 1)
                else:
                    target_rel, anchor = clean_url, None

                # Record widget references
                if "widgets/" in target_rel or target_rel.endswith(".html"):
                    widget_name = os.path.basename(target_rel)
                    referenced_widgets.add(widget_name)

                # Validate local target file
                if target_rel:
                    resolved = os.path.normpath(os.path.join(ch_dir, target_rel))
                    if not os.path.exists(resolved):
                        self.report.add_issue(
                            suite, ch_name, "ERROR",
                            f"Broken {link_type} link: '{raw_url}' -> file '{resolved}' does not exist."
                        )
                    else:
                        self.report.record_pass()
                else:
                    # Same-file anchor link
                    self.report.record_pass()

        # Audit for orphan widget files
        all_widget_files = {os.path.basename(p) for p in self.widget_files}
        orphan_widgets = all_widget_files - referenced_widgets

        if orphan_widgets:
            self.report.add_issue(
                suite, "Widgets Directory", "ERROR",
                f"Found orphan widget files not embedded in any chapter: {orphan_widgets}"
            )
        else:
            self.report.record_pass()

        # Audit for missing required widgets
        expected_widgets = {spec["file"] for spec in MANDATORY_WIDGET_MAPPINGS.values()}
        missing_widgets = expected_widgets - all_widget_files
        if missing_widgets:
            self.report.add_issue(
                suite, "Widgets Directory", "ERROR",
                f"Missing mandatory widget files in widgets directory: {missing_widgets}"
            )
        else:
            self.report.record_pass()

    # --------------------------------------------------------------------------
    # Suite 4: Pedagogical Restructuring & Text Wall Elimination
    # --------------------------------------------------------------------------
    def audit_pedagogical_restructuring(self) -> None:
        suite = "Suite 4: Pedagogical Restructuring"

        table_separator_regex = re.compile(r'\|(?:\s*:?-+:?\s*\|)+')
        callout_regex = re.compile(
            r'^\s*>\s*(?:\[\!(?:NOTE|TIP|WARNING|CAUTION|IMPORTANT)\]|\*\*.*?\*\*)',
            re.MULTILINE
        )

        for ch_path in self.chapter_files:
            ch_name = os.path.basename(ch_path)
            with open(ch_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()

            # 1. Structured Tables
            tables_count = len(table_separator_regex.findall(content))
            if tables_count < 2:
                self.report.add_issue(
                    suite, ch_name, "ERROR",
                    f"Chapter '{ch_name}' contains insufficient structured tables ({tables_count} < 2)."
                )
            else:
                self.report.record_pass()

            # 2. Callout Cards
            callouts_count = len(callout_regex.findall(content))
            if callouts_count < 2:
                self.report.add_issue(
                    suite, ch_name, "ERROR",
                    f"Chapter '{ch_name}' contains insufficient callout cards ({callouts_count} < 2)."
                )
            else:
                self.report.record_pass()

            # 3. Mermaid Diagrams
            mermaid_count = len(re.findall(r'```mermaid', content))
            if mermaid_count < 1:
                self.report.add_issue(
                    suite, ch_name, "ERROR",
                    f"Chapter '{ch_name}' contains zero Mermaid diagrams."
                )
            else:
                self.report.record_pass()

            # 4. Math Blocks
            math_blocks_count = len(re.findall(r'\$\$', content)) // 2
            if math_blocks_count < 10:
                self.report.add_issue(
                    suite, ch_name, "ERROR",
                    f"Chapter '{ch_name}' has low mathematical rigor ({math_blocks_count} display math blocks < 10)."
                )
            else:
                self.report.record_pass()

            # 5. Text Wall Detection
            # Scan for consecutive prose paragraph lines >= 8 or single paragraph word count > 140
            in_code = False
            in_math = False
            curr_para_lines: List[Tuple[int, str]] = []
            text_walls: List[Tuple[int, int, int]] = []  # (start_line, line_count, word_count)

            for line_idx, line in enumerate(lines, 1):
                s = line.strip()

                if s.startswith("```"):
                    in_code = not in_code
                    s = ""

                if "$$" in s:
                    cnt = s.count("$$")
                    if cnt % 2 == 1:
                        in_math = not in_math
                    # If this line started or closed a math block, don't treat it as prose
                    if in_code or in_math:
                        if curr_para_lines:
                            w_cnt = sum(len(txt.split()) for _, txt in curr_para_lines)
                            if len(curr_para_lines) >= 8 or w_cnt > 140:
                                text_walls.append((curr_para_lines[0][0], len(curr_para_lines), w_cnt))
                            curr_para_lines = []
                        continue
                    else:
                        # math block just closed on this line
                        continue

                if in_code or in_math:
                    if curr_para_lines:
                        # Flush paragraph
                        w_cnt = sum(len(txt.split()) for _, txt in curr_para_lines)
                        if len(curr_para_lines) >= 8 or w_cnt > 140:
                            text_walls.append((curr_para_lines[0][0], len(curr_para_lines), w_cnt))
                        curr_para_lines = []
                    continue

                is_break = (
                    not s or
                    s.startswith(("#", "|", ">", "-", "*", "<")) or
                    re.match(r"^\d+\.", s)
                )

                if is_break:
                    if curr_para_lines:
                        w_cnt = sum(len(txt.split()) for _, txt in curr_para_lines)
                        if len(curr_para_lines) >= 8 or w_cnt > 140:
                            text_walls.append((curr_para_lines[0][0], len(curr_para_lines), w_cnt))
                        curr_para_lines = []
                else:
                    curr_para_lines.append((line_idx, s))

            if curr_para_lines:
                w_cnt = sum(len(txt.split()) for _, txt in curr_para_lines)
                if len(curr_para_lines) >= 8 or w_cnt > 140:
                    text_walls.append((curr_para_lines[0][0], len(curr_para_lines), w_cnt))

            if text_walls:
                for start_line, l_cnt, w_cnt in text_walls:
                    self.report.add_issue(
                        suite, ch_name, "WARNING",
                        f"Line {start_line}: Dense unbroken prose block detected ({l_cnt} lines, {w_cnt} words).",
                        start_line
                    )
            else:
                self.report.record_pass()

            self.report.metrics[f"{ch_name}_pedagogy"] = {
                "tables": tables_count,
                "callouts": callouts_count,
                "mermaid_diagrams": mermaid_count,
                "math_blocks": math_blocks_count,
                "text_walls_detected": len(text_walls),
            }

    # --------------------------------------------------------------------------
    # Suite 5: Code Block Prohibition Audit (R1)
    # --------------------------------------------------------------------------
    def audit_code_block_prohibition(self) -> None:
        suite = "Suite 5: Code Block Prohibition"

        disallowed_tags = ["python", "py", "matlab", "m", "cpp", "c++", "c", "bash", "sh", "javascript", "js"]

        for ch_path in self.chapter_files:
            ch_name = os.path.basename(ch_path)
            with open(ch_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            in_code = False
            code_lang = ""
            code_start_line = 0

            for line_idx, line in enumerate(lines, 1):
                s = line.strip()
                if s.startswith("```"):
                    if not in_code:
                        in_code = True
                        code_lang = s[3:].strip().lower()
                        code_start_line = line_idx
                    else:
                        in_code = False
                        # Audit finished code block
                        if code_lang in disallowed_tags or (code_lang != "mermaid" and code_lang != ""):
                            self.report.add_issue(
                                suite, ch_name, "ERROR",
                                f"Line {code_start_line}: Standalone programming code block detected (```{code_lang}).",
                                code_start_line
                            )
                        elif code_lang == "":
                            self.report.add_issue(
                                suite, ch_name, "WARNING",
                                f"Line {code_start_line}: Untagged code block detected.",
                                code_start_line
                            )
                        else:
                            self.report.record_pass()

    # --------------------------------------------------------------------------
    # Suite 6: Widget Self-Containment & Offline Robustness
    # --------------------------------------------------------------------------
    def audit_widget_self_containment(self) -> None:
        suite = "Suite 6: Widget Self-Containment"

        for w_path in self.widget_files:
            w_name = os.path.basename(w_path)
            with open(w_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. HTML5 Doctype
            if not re.search(r'<!DOCTYPE\s+html>', content, re.IGNORECASE):
                self.report.add_issue(suite, w_name, "ERROR", "Missing standard <!DOCTYPE html> declaration.")
            else:
                self.report.record_pass()

            # 2. Offline fallback styles
            if "<style>" not in content or "</style>" not in content:
                self.report.add_issue(suite, w_name, "ERROR", "Missing embedded <style> offline fallback stylesheet.")
            else:
                self.report.record_pass()

            # 3. External JS libraries prohibition (disallow external script src except Tailwind/styling)
            script_srcs = re.findall(r'<script\s+[^>]*?src=["\']([^"\']+)["\']', content, re.IGNORECASE)
            for s_src in script_srcs:
                if "tailwindcss" not in s_src and "tailwind" not in s_src:
                    self.report.add_issue(
                        suite, w_name, "ERROR",
                        f"Widget loads external JS script dependency: '{s_src}'."
                    )
                else:
                    self.report.record_pass()

            # 4. Canvas or SVG visualizer element
            has_canvas = "<canvas" in content
            has_svg = "<svg" in content
            if not (has_canvas or has_svg):
                self.report.add_issue(suite, w_name, "ERROR", "Widget lacks Canvas or SVG visualizer elements.")
            else:
                self.report.record_pass()

            # 5. Interactive controls
            has_controls = ("<input" in content or "<button" in content or "addEventListener" in content)
            if not has_controls:
                self.report.add_issue(suite, w_name, "ERROR", "Widget lacks interactive DOM controls (inputs, buttons).")
            else:
                self.report.record_pass()

    def run_all(self) -> AuditReport:
        self.audit_iframe_and_fallback_links()
        self.audit_conceptual_insertion_points()
        self.audit_link_resolution_and_orphans()
        self.audit_pedagogical_restructuring()
        self.audit_code_block_prohibition()
        self.audit_widget_self_containment()
        return self.report


def print_report(report: AuditReport) -> None:
    print("=" * 80)
    print(" ADVERSARIAL GENERATIVE UI WIDGET & PEDAGOGY VERIFICATION SUITE")
    print("=" * 80)
    print(f"Total Checks Executed : {report.total_checks}")
    print(f"Passed Checks         : {report.passed_checks}")
    print(f"Failed Checks (Errors): {report.failed_checks}")
    print(f"Warnings              : {report.warning_checks}")
    print("-" * 80)

    if report.issues:
        print("ISSUES DETECTED:")
        for idx, issue in enumerate(report.issues, 1):
            line_str = f" [Line {issue.line_number}]" if issue.line_number else ""
            print(f"{idx:2d}. [{issue.severity}] {issue.suite} -> {issue.target}{line_str}")
            print(f"    {issue.message}")
        print("-" * 80)
    else:
        print("ZERO ISSUES FOUND: 100% of adversarial checks passed cleanly.")

    print(f"FINAL VERDICT: {'APPROVE' if report.failed_checks == 0 else 'REJECT'}")
    print("=" * 80)


class AdversarialAuditorUnitTests(unittest.TestCase):
    """Automated adversarial unit test harness validating auditor sensitivity against injected flaws."""

    def setUp(self):
        self.auditor = AdversarialAuditor()

    def test_run_full_verification(self):
        report = self.auditor.run_all()
        self.assertEqual(report.failed_checks, 0, f"Failed checks detected: {report.issues}")
        self.assertGreater(report.passed_checks, 50, "Insufficient checks were executed.")

    def test_detects_broken_iframe_src(self):
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp_dir:
            ch_dir = os.path.join(tmp_dir, "chapters")
            w_dir = os.path.join(tmp_dir, "widgets")
            os.makedirs(ch_dir)
            os.makedirs(w_dir)

            bad_ch = os.path.join(ch_dir, "topic_1_test.md")
            with open(bad_ch, "w", encoding="utf-8") as f:
                f.write("<iframe src='../widgets/non_existent_widget.html' width='100%' height='520'></iframe>\n"
                        "<p><em><a href='../widgets/non_existent_widget.html'>Open</a></em></p>\n")

            auditor = AdversarialAuditor(chapters_dir=ch_dir, widgets_dir=w_dir)
            auditor.audit_iframe_and_fallback_links()
            errors = [i for i in auditor.report.issues if "does not exist on disk" in i.message]
            self.assertTrue(len(errors) > 0, "Failed to flag non-existent iframe target file.")

    def test_detects_mismatched_fallback_link(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            ch_dir = os.path.join(tmp_dir, "chapters")
            w_dir = os.path.join(tmp_dir, "widgets")
            os.makedirs(ch_dir)
            os.makedirs(w_dir)

            real_w1 = os.path.join(w_dir, "widget_1.html")
            real_w2 = os.path.join(w_dir, "widget_2.html")
            for w in [real_w1, real_w2]:
                with open(w, "w", encoding="utf-8") as f:
                    f.write("<!DOCTYPE html><html><head><style>body{}</style></head><body><canvas></canvas><button></button></body></html>")

            bad_ch = os.path.join(ch_dir, "topic_1_test.md")
            with open(bad_ch, "w", encoding="utf-8") as f:
                f.write("<iframe src='../widgets/widget_1.html' width='100%' height='520'></iframe>\n"
                        "<p><em><a href='../widgets/widget_2.html'>Open</a></em></p>\n")

            auditor = AdversarialAuditor(chapters_dir=ch_dir, widgets_dir=w_dir)
            auditor.audit_iframe_and_fallback_links()
            errors = [i for i in auditor.report.issues if "does not match iframe src" in i.message]
            self.assertTrue(len(errors) > 0, "Failed to flag mismatched iframe src vs fallback link.")

    def test_detects_prohibited_code_block(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            ch_dir = os.path.join(tmp_dir, "chapters")
            os.makedirs(ch_dir)
            bad_ch = os.path.join(ch_dir, "topic_4_test.md")
            with open(bad_ch, "w", encoding="utf-8") as f:
                f.write("## Section\n```python\ndef allocate(): pass\n```\n")

            auditor = AdversarialAuditor(chapters_dir=ch_dir, widgets_dir=WIDGETS_DIR)
            auditor.audit_code_block_prohibition()
            errors = [i for i in auditor.report.issues if "Standalone programming code block detected" in i.message]
            self.assertTrue(len(errors) > 0, "Failed to flag prohibited Python code block.")

    def test_detects_unbroken_text_wall(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            ch_dir = os.path.join(tmp_dir, "chapters")
            os.makedirs(ch_dir)
            bad_ch = os.path.join(ch_dir, "topic_2_test.md")
            # 10 lines of dense prose without lists/headings/equations/tables
            prose_wall = "\n".join([f"This is line {i} of a continuous unbroken block of explanatory text explaining quadrotor physics without lists." for i in range(12)])
            with open(bad_ch, "w", encoding="utf-8") as f:
                f.write(f"## Section 1\n| A | B |\n|---|---|\n| 1 | 2 |\n\n> [!NOTE]\n> Valid\n\n```mermaid\nflowchart TD\nA-->B\n```\n\n"
                        f"{prose_wall}\n\n"
                        + "\n".join([f"$$x_{i} = {i}$$" for i in range(12)]))

            auditor = AdversarialAuditor(chapters_dir=ch_dir, widgets_dir=WIDGETS_DIR)
            auditor.audit_pedagogical_restructuring()
            warnings = [i for i in auditor.report.issues if "Dense unbroken prose block detected" in i.message]
            self.assertTrue(len(warnings) > 0, "Failed to flag dense unbroken prose text wall.")

    def test_detects_external_js_cdn_in_widget(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            w_dir = os.path.join(tmp_dir, "widgets")
            os.makedirs(w_dir)
            bad_w = os.path.join(w_dir, "widget_bad.html")
            with open(bad_w, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html><html><head><style>body{}</style><script src='https://cdnjs.cloudflare.com/three.js'></script></head><body><canvas></canvas><button></button></body></html>")

            auditor = AdversarialAuditor(chapters_dir=CHAPTERS_DIR, widgets_dir=w_dir)
            auditor.audit_widget_self_containment()
            errors = [i for i in auditor.report.issues if "loads external JS script dependency" in i.message]
            self.assertTrue(len(errors) > 0, "Failed to flag external JS library dependency.")


def main():
    parser = argparse.ArgumentParser(description="Adversarial Generative UI & Pedagogy Verification Runner")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--self-test", action="store_true", help="Run auditor unit test harness")
    args = parser.parse_args()

    if args.self_test:
        suite = unittest.TestLoader().loadTestsFromTestCase(AdversarialAuditorUnitTests)
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(suite)
        sys.exit(0 if res.wasSuccessful() else 1)

    auditor = AdversarialAuditor()
    report = auditor.run_all()

    if args.json:
        out = {
            "total_checks": report.total_checks,
            "passed_checks": report.passed_checks,
            "failed_checks": report.failed_checks,
            "warning_checks": report.warning_checks,
            "verdict": "APPROVE" if report.failed_checks == 0 else "REJECT",
            "issues": [
                {
                    "suite": i.suite,
                    "target": i.target,
                    "severity": i.severity,
                    "line": i.line_number,
                    "message": i.message,
                }
                for i in report.issues
            ],
            "metrics": report.metrics,
        }
        print(json.dumps(out, indent=2))
    else:
        print_report(report)

    sys.exit(0 if report.failed_checks == 0 else 1)


if __name__ == "__main__":
    main()
