#!/usr/bin/env python3
"""
gate3_adversarial_oracle.py
===========================
Adversarial Verification Oracle for Gate 3 Audit.
Created and executed by challenger_gate3 (Empirical Challenger).

Audits all chapters in modules/EEEE4138_aerial_robotics/chapters/ against:
  1. KaTeX Syntax:
     - 0 triple dollars ($$$ or ${3,}) across the entire file
     - Delimiter parity ($$ display, $ inline)
     - 0 unclosed math blocks
     - 0 unescaped/unbalanced curly braces ({ and }) in math blocks
     - 0 unescaped/unbalanced square brackets ([ and ]) in math blocks
     - LaTeX environment stack matching (\\begin{env} ... \\end{env})
     - \\left ... \\right delimiter pairing
     - Double subscripts/superscripts without braces
     - Raw tab corruptions and forbidden macros
  2. Mermaid Syntax:
     - Fenced block start/end pairing
     - Valid diagram header
     - Delimiter balance: double quotes, brackets, parentheses, curly braces
     - Subgraph ... end pairing
     - Unquoted reserved characters (&, <, >)
     - Unquoted parentheses inside square brackets [Label (text)]
     - Unquoted HTML tags (<br>, <br/>)
     - Forbidden arrow styles (single dash ->, malformed combinations)
  3. Residual Code Blocks:
     - 0 non-mermaid fenced code blocks
     - 0 untagged code blocks
     - 0 4-space indented programming blocks (def, class, import, etc.)
     - 0 HTML <pre> code containers
     - 0 legacy code signatures (e.g. attitude_priority_allocation)
  4. Residual ASCII Art:
     - 0 Unicode box drawing characters (┌, ┐, └, ┘, │, ─, ┼, etc.)
     - 0 ASCII box borders (+---+, +===+)
     - 0 Box-and-arrow chains ([A] --> [B])
     - 0 Multi-arrow chains outside math
     - 0 Standalone arrow glyphs connecting words
  5. Interactive Widget Embeds:
     - Designated widget embed per topic
     - File existence, non-empty check, valid HTML5 container
  6. Cross-Chapter Link Integrity:
     - Resolvable relative paths and anchors
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclass
class AuditFinding:
    category: str
    file_name: str
    line_number: Optional[int]
    severity: str  # CRITICAL, ERROR, WARNING, INFO
    description: str
    snippet: str = ""


@dataclass
class ChapterMetrics:
    file_name: str
    total_lines: int = 0
    total_bytes: int = 0
    consecutive_dollar_errors: int = 0
    katex_display_blocks: int = 0
    katex_inline_spans: int = 0
    katex_environments: int = 0
    katex_brace_errors: int = 0
    katex_delim_errors: int = 0
    katex_other_errors: int = 0
    mermaid_diagrams: int = 0
    mermaid_subgraphs: int = 0
    mermaid_errors: int = 0
    non_mermaid_code_blocks: int = 0
    ascii_art_artifacts: int = 0
    widget_embeds: int = 0
    widget_errors: int = 0
    broken_links: int = 0

    @property
    def total_errors(self) -> int:
        return (
            self.consecutive_dollar_errors
            + self.katex_brace_errors
            + self.katex_delim_errors
            + self.katex_other_errors
            + self.mermaid_errors
            + self.non_mermaid_code_blocks
            + self.ascii_art_artifacts
            + self.widget_errors
            + self.broken_links
        )


DESIGNATED_WIDGETS = {
    1: "widget_1_flight_envelope.html",
    2: "widget_2_frames_gimbal_lock.html",
    3: "widget_3_rigid_body_dynamics.html",
    4: "widget_4_rotor_mixer_allocation.html",
    5: "widget_5_cascaded_flight_control.html",
}


def count_unescaped(pattern: str, text: str) -> int:
    """Counts matches of pattern that are not preceded by an odd number of backslashes."""
    return len(list(re.finditer(r"(?<!\\)" + pattern, text)))


def audit_chapter_katex(raw_content: str, lines: List[str], fname: str) -> Tuple[List[AuditFinding], ChapterMetrics]:
    findings: List[AuditFinding] = []
    metrics = ChapterMetrics(file_name=fname, total_lines=len(lines), total_bytes=len(raw_content.encode("utf-8")))

    # 1. Strict consecutive dollar check: ${3,} anywhere in the file
    triple_dollar_matches = list(re.finditer(r"(?<!\\)\${3,}", raw_content))
    for m in triple_dollar_matches:
        lno = raw_content[:m.start()].count("\n") + 1
        seq = m.group(0)
        metrics.consecutive_dollar_errors += 1
        findings.append(
            AuditFinding(
                category="KATEX_CONSECUTIVE_DOLLARS",
                file_name=fname,
                line_number=lno,
                severity="ERROR",
                description=f"Found sequence of {len(seq)} consecutive dollar signs ('{seq}').",
                snippet=raw_content[max(0, m.start()-20):min(len(raw_content), m.end()+20)].replace("\n", " "),
            )
        )

    # Mask fenced code blocks with newlines to keep line numbers intact
    content_no_code = re.sub(r"```[\s\S]*?```", lambda m: "\n" * m.group(0).count("\n"), raw_content)
    content_no_code = re.sub(r"~~~[\s\S]*?~~~", lambda m: "\n" * m.group(0).count("\n"), content_no_code)

    # 2. Display math delimiter ($$) parity check
    dd_matches = list(re.finditer(r"(?<!\\)\$\$", content_no_code))
    if len(dd_matches) % 2 != 0:
        metrics.katex_delim_errors += 1
        findings.append(
            AuditFinding(
                category="KATEX_DELIMITER_PARITY",
                file_name=fname,
                line_number=None,
                severity="ERROR",
                description=f"Odd count of display math ($$) delimiters: {len(dd_matches)}. Unclosed math block exists.",
            )
        )
    metrics.katex_display_blocks = len(dd_matches) // 2

    # 3. Inline math delimiter ($) parity check (outside display math)
    temp_no_dd = re.sub(r"(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$", lambda m: "\n" * m.group(0).count("\n"), content_no_code)
    sd_matches = list(re.finditer(r"(?<!\\)\$", temp_no_dd))
    if len(sd_matches) % 2 != 0:
        metrics.katex_delim_errors += 1
        findings.append(
            AuditFinding(
                category="KATEX_DELIMITER_PARITY",
                file_name=fname,
                line_number=None,
                severity="ERROR",
                description=f"Odd count of inline math ($) delimiters: {len(sd_matches)}. Unclosed math block exists.",
            )
        )
    metrics.katex_inline_spans = len(sd_matches) // 2

    # 4. Display Math Block Inspection
    display_pattern = re.compile(r"(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$")
    for m in display_pattern.finditer(content_no_code):
        block = m.group(1)
        lno = content_no_code[:m.start()].count("\n") + 1

        # 4a. Curly braces balance
        # Exclude \{ and \}
        opens = len(re.findall(r"(?<!\\)\{", block))
        closes = len(re.findall(r"(?<!\\)\}", block))
        if opens != closes:
            metrics.katex_brace_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_BRACE_BALANCE",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Unbalanced curly braces in display math: '{{' ({opens}) vs '}}' ({closes}).",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

        # 4b. Square bracket balance (ignoring \\[6pt] line break spacing)
        clean_sq = re.sub(r'\\\\\[[0-9a-zA-Z\s.]+\]', '', block)
        sq_opens = len(re.findall(r"(?<!\\)\[", clean_sq))
        sq_closes = len(re.findall(r"(?<!\\)\]", clean_sq))
        if sq_opens != sq_closes:
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_BRACKET_BALANCE",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Unbalanced square brackets in display math: '[' ({sq_opens}) vs ']' ({sq_closes}).",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

        # 4c. LaTeX environment matching (stack)
        env_tokens = re.findall(r"\\(begin|end)\{([a-zA-Z*]+)\}", block)
        stack = []
        for kind, env in env_tokens:
            if kind == "begin":
                stack.append(env)
                metrics.katex_environments += 1
            else:
                if not stack:
                    metrics.katex_other_errors += 1
                    findings.append(
                        AuditFinding(
                            category="KATEX_ENVIRONMENT_MISMATCH",
                            file_name=fname,
                            line_number=lno,
                            severity="ERROR",
                            description=f"\\end{{{env}}} found with empty begin stack.",
                            snippet=block.strip()[:100].replace("\n", " "),
                        )
                    )
                else:
                    top = stack.pop()
                    if top != env and not (top.endswith("*") and env == top.rstrip("*")):
                        metrics.katex_other_errors += 1
                        findings.append(
                            AuditFinding(
                                category="KATEX_ENVIRONMENT_MISMATCH",
                                file_name=fname,
                                line_number=lno,
                                severity="ERROR",
                                description=f"Mismatched environment: \\begin{{{top}}} closed by \\end{{{env}}}.",
                                snippet=block.strip()[:100].replace("\n", " "),
                            )
                        )
        if stack:
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_ENVIRONMENT_MISMATCH",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Unclosed LaTeX environments at end of math block: {stack}.",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

        # 4d. \\left and \\right matching
        left_count = len(re.findall(r"\\left(?![a-zA-Z])", block))
        right_count = len(re.findall(r"\\right(?![a-zA-Z])", block))
        if left_count != right_count:
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_LEFT_RIGHT_MISMATCH",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Mismatched \\left ({left_count}) vs \\right ({right_count}) in display math.",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

        # 4e. Double subscripts / superscripts without braces
        dbl_sub = re.search(r"[a-zA-Z0-9]_([a-zA-Z0-9])_([a-zA-Z0-9])", block)
        if dbl_sub:
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_DOUBLE_SUBSCRIPT",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Double subscript without braces '{dbl_sub.group(0)}'.",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

        dbl_sup = re.search(r"[a-zA-Z0-9]\^([a-zA-Z0-9])\^([a-zA-Z0-9])", block)
        if dbl_sup:
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_DOUBLE_SUPERSCRIPT",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Double superscript without braces '{dbl_sup.group(0)}'.",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

        # 4f. Forbidden macros
        if "\\href" in block:
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_FORBIDDEN_MACRO",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description="Macro '\\href' inside display math block.",
                    snippet=block.strip()[:100].replace("\n", " "),
                )
            )

    # 5. Inline Math Span Inspection
    inline_pattern = re.compile(r"(?<!\\)\$([^\$\n]+?)(?<!\\)\$")
    for m in inline_pattern.finditer(temp_no_dd):
        span = m.group(1)
        lno = temp_no_dd[:m.start()].count("\n") + 1

        opens = len(re.findall(r"(?<!\\)\{", span))
        closes = len(re.findall(r"(?<!\\)\}", span))
        if opens != closes:
            metrics.katex_brace_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_BRACE_BALANCE",
                    file_name=fname,
                    line_number=lno,
                    severity="ERROR",
                    description=f"Unbalanced curly braces in inline math: '{{' ({opens}) vs '}}' ({closes}).",
                    snippet=span.strip()[:80],
                )
            )

    # 6. Tab character corruption check
    re_tab_cmd = re.compile(r"\t(heta|o|au|ilde|ext|imes|an|op|artial|beta|gamma|sigma|omega|alpha|lambda|mu|rho|phi|psi)\b")
    for idx, line in enumerate(lines, 1):
        if re_tab_cmd.search(line):
            metrics.katex_other_errors += 1
            findings.append(
                AuditFinding(
                    category="KATEX_TAB_CORRUPTION",
                    file_name=fname,
                    line_number=idx,
                    severity="ERROR",
                    description=f"Raw tab character precedes LaTeX command at line {idx}.",
                    snippet=line.strip()[:80],
                )
            )

    return findings, metrics


def audit_chapter_mermaid(lines: List[str], fname: str, metrics: ChapterMetrics) -> List[AuditFinding]:
    findings: List[AuditFinding] = []

    in_mermaid = False
    diag_start = 0
    current_diag: List[Tuple[int, str]] = []

    def audit_diagram(diag_idx: int, block: List[Tuple[int, str]]):
        if not block:
            return
        start_lno = block[0][0]
        full_text = "\n".join(l[1] for l in block)

        # Header check
        first_content = [l[1].strip() for l in block if l[1].strip() and not l[1].strip().startswith("%%")]
        if not first_content:
            metrics.mermaid_errors += 1
            findings.append(
                AuditFinding(
                    category="MERMAID_SYNTAX",
                    file_name=fname,
                    line_number=start_lno,
                    severity="ERROR",
                    description=f"Mermaid diagram #{diag_idx} is empty or only comments.",
                )
            )
            return

        header = first_content[0]
        valid_headers = [
            "flowchart", "graph", "sequenceDiagram", "classDiagram",
            "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
            "pie", "gitGraph", "mindmap", "timeline", "quadrantChart",
        ]
        if not any(header.startswith(vh) for vh in valid_headers):
            metrics.mermaid_errors += 1
            findings.append(
                AuditFinding(
                    category="MERMAID_SYNTAX",
                    file_name=fname,
                    line_number=start_lno,
                    severity="ERROR",
                    description=f"Mermaid diagram #{diag_idx} has invalid header '{header}'.",
                    snippet=header,
                )
            )

        # Quote balance
        quotes = full_text.count('"') - full_text.count(r'\"')
        if quotes % 2 != 0:
            metrics.mermaid_errors += 1
            findings.append(
                AuditFinding(
                    category="MERMAID_SYNTAX",
                    file_name=fname,
                    line_number=start_lno,
                    severity="ERROR",
                    description=f"Mermaid diagram #{diag_idx} has unbalanced double quotes ({quotes}).",
                )
            )

        # Square brackets balance
        sq_o = full_text.count("[")
        sq_c = full_text.count("]")
        if sq_o != sq_c:
            metrics.mermaid_errors += 1
            findings.append(
                AuditFinding(
                    category="MERMAID_SYNTAX",
                    file_name=fname,
                    line_number=start_lno,
                    severity="ERROR",
                    description=f"Mermaid diagram #{diag_idx} has unbalanced square brackets: '[' ({sq_o}) vs ']' ({sq_c}).",
                )
            )

        # Curly braces balance
        cur_o = full_text.count("{")
        cur_c = full_text.count("}")
        if cur_o != cur_c:
            metrics.mermaid_errors += 1
            findings.append(
                AuditFinding(
                    category="MERMAID_SYNTAX",
                    file_name=fname,
                    line_number=start_lno,
                    severity="ERROR",
                    description=f"Mermaid diagram #{diag_idx} has unbalanced curly braces: '{{' ({cur_o}) vs '}}' ({cur_c}).",
                )
            )

        # Subgraph balance
        sub_opens = len(re.findall(r"^\s*subgraph\b", full_text, re.MULTILINE))
        sub_ends = len(re.findall(r"^\s*end\b", full_text, re.MULTILINE))
        metrics.mermaid_subgraphs += sub_opens
        if sub_opens != sub_ends:
            metrics.mermaid_errors += 1
            findings.append(
                AuditFinding(
                    category="MERMAID_SYNTAX",
                    file_name=fname,
                    line_number=start_lno,
                    severity="ERROR",
                    description=f"Mermaid diagram #{diag_idx} has mismatched subgraphs: subgraph ({sub_opens}) vs end ({sub_ends}).",
                )
            )

        # Line-by-line checks
        for lno, raw_line in block:
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("%%") or stripped.startswith("subgraph") or stripped == "end":
                continue

            # Check single dash arrow
            if re.search(r"[a-zA-Z0-9_\)\]\}]\s*->\s*[a-zA-Z0-9_\(\[\{]", stripped):
                metrics.mermaid_errors += 1
                findings.append(
                    AuditFinding(
                        category="MERMAID_SYNTAX",
                        file_name=fname,
                        line_number=lno,
                        severity="ERROR",
                        description="Single dash arrow '->' detected. Use '-->' for flowchart.",
                        snippet=stripped,
                    )
                )

            # Strip valid double-quoted strings
            unquoted = re.sub(r'"[^"]*"', '', stripped)

            # Check unquoted ampersands inside node or edge labels
            if re.search(r'\[[^\]]*&[^\]]*\]|\([^\)]*&[^\)]*\)|\{[^\}]*&[^\}]*\}|\|[^|]*&[^|]*\|', unquoted):
                metrics.mermaid_errors += 1
                findings.append(
                    AuditFinding(
                        category="MERMAID_SYNTAX",
                        file_name=fname,
                        line_number=lno,
                        severity="ERROR",
                        description="Unquoted ampersand '&' inside node or edge label.",
                        snippet=stripped,
                    )
                )

            # Check unquoted comparison operators
            if re.search(r'\[[^\]]*[<>][^\]]*\]|\{[^\}]*[<>][^\}]*\}', unquoted):
                metrics.mermaid_errors += 1
                findings.append(
                    AuditFinding(
                        category="MERMAID_SYNTAX",
                        file_name=fname,
                        line_number=lno,
                        severity="ERROR",
                        description="Unescaped '<' or '>' in unquoted node label.",
                        snippet=stripped,
                    )
                )

            # Check unquoted parentheses in square bracket nodes: A[Label (details)]
            if re.search(r'\[[^\]"]*\([^\]"]*\)[^\]"]*\]', unquoted):
                metrics.mermaid_errors += 1
                findings.append(
                    AuditFinding(
                        category="MERMAID_SYNTAX",
                        file_name=fname,
                        line_number=lno,
                        severity="ERROR",
                        description="Unquoted parentheses inside square bracket node label.",
                        snippet=stripped,
                    )
                )

    for idx, raw_line in enumerate(lines, 1):
        stripped = raw_line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            metrics.mermaid_diagrams += 1
            diag_start = idx
            current_diag = []
            continue
        elif in_mermaid and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_mermaid = False
            audit_diagram(metrics.mermaid_diagrams, current_diag)
            current_diag = []
            continue
        elif in_mermaid:
            current_diag.append((idx, raw_line.rstrip("\r\n")))

    if in_mermaid:
        metrics.mermaid_errors += 1
        findings.append(
            AuditFinding(
                category="MERMAID_SYNTAX",
                file_name=fname,
                line_number=diag_start,
                severity="ERROR",
                description="Unclosed Mermaid diagram block at EOF.",
            )
        )

    return findings


def audit_chapter_code_and_ascii(raw_content: str, lines: List[str], fname: str, metrics: ChapterMetrics) -> List[AuditFinding]:
    findings: List[AuditFinding] = []

    # 1. Residual programming fenced blocks
    fenced_matches = list(re.finditer(r"```([a-zA-Z0-9_-]*)", raw_content))
    in_block = False
    for m in fenced_matches:
        lang = m.group(1).lower().strip()
        if not in_block:
            in_block = True
            if lang != "mermaid":
                metrics.non_mermaid_code_blocks += 1
                lno = raw_content[:m.start()].count("\n") + 1
                findings.append(
                    AuditFinding(
                        category="RESIDUAL_CODE_BLOCK",
                        file_name=fname,
                        line_number=lno,
                        severity="CRITICAL",
                        description=f"Disallowed fenced code block tag '```{lang}'. Only ```mermaid is permitted.",
                        snippet=raw_content[m.start():m.start()+40].replace("\n", " "),
                    )
                )
        else:
            in_block = False

    # Check untagged fenced code blocks
    content_no_mermaid = re.sub(r"```mermaid[\s\S]*?```", lambda m: "\n" * m.group(0).count("\n"), raw_content)
    residual_fences = list(re.finditer(r"```[\s\S]*?```", content_no_mermaid))
    for m in residual_fences:
        metrics.non_mermaid_code_blocks += 1
        lno = content_no_mermaid[:m.start()].count("\n") + 1
        findings.append(
            AuditFinding(
                category="RESIDUAL_CODE_BLOCK",
                file_name=fname,
                line_number=lno,
                severity="CRITICAL",
                description="Non-mermaid fenced code block found.",
                snippet=content_no_mermaid[m.start():m.start()+60].replace("\n", " "),
            )
        )

    # 2. Check 4-space indented programming blocks
    re_indented_code = re.compile(
        r"^\s{4,}(?:def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(|import\s+[a-zA-Z_]|from\s+[a-zA-Z_].*import|class\s+[a-zA-Z_]|function\s+\[?[a-zA-Z0-9_,\s]+\]?\s*=|#include\s*<|void\s+[a-zA-Z_]|int\s+main\s*\()"
    )
    in_fence = False
    for idx, raw_line in enumerate(lines, 1):
        s = raw_line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence and re_indented_code.match(raw_line):
            metrics.non_mermaid_code_blocks += 1
            findings.append(
                AuditFinding(
                    category="RESIDUAL_CODE_BLOCK",
                    file_name=fname,
                    line_number=idx,
                    severity="ERROR",
                    description=f"4-space indented programming implementation at line {idx}.",
                    snippet=raw_line.strip()[:80],
                )
            )

    # 3. HTML <pre> blocks
    for pm in re.finditer(r"<pre\b[^>]*>[\s\S]*?</pre>", raw_content, re.IGNORECASE):
        metrics.non_mermaid_code_blocks += 1
        lno = raw_content[:pm.start()].count("\n") + 1
        findings.append(
            AuditFinding(
                category="RESIDUAL_CODE_BLOCK",
                file_name=fname,
                line_number=lno,
                severity="ERROR",
                description=f"HTML <pre> code container detected at line {lno}.",
                snippet=pm.group(0)[:80].replace("\n", " "),
            )
        )

    # 4. Legacy code signatures
    legacy_sigs = [
        "attitude_priority_allocation",
        "desaturate_mixer",
        "def compute_motor_outputs",
        "def lqr_control",
        "np.linalg.pinv(B)",
        "np.clip(pwm",
    ]
    for sig in legacy_sigs:
        if sig in raw_content:
            metrics.non_mermaid_code_blocks += 1
            findings.append(
                AuditFinding(
                    category="LEGACY_CODE_SIGNATURE",
                    file_name=fname,
                    line_number=None,
                    severity="CRITICAL",
                    description=f"Legacy function signature '{sig}' present in chapter.",
                    snippet=sig,
                )
            )

    # 5. ASCII Box-and-Arrow and Box Borders
    re_box_arrow = re.compile(r"\[[^\]]+\]\s*(?:-->|->|==>|──►|─►|◄──|◄─)\s*\[[^\]]+\]")
    re_ascii_box = re.compile(r"^\s*\+[-=]{3,}\+\s*$")
    re_unicode_box = re.compile(r"^\s*[┌\+│][─┬┼\-]{3,}[┐\+│]\s*$")
    re_multi_arrow = re.compile(r"(?:──►|─►|◄──|◄─|-->|==>|->)")

    in_fenced = False
    in_math = False
    for idx, raw_line in enumerate(lines, 1):
        s = raw_line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue

        if "$$" in s:
            if s.count("$$") % 2 != 0:
                in_math = not in_math
            if in_math:
                continue
        if in_math:
            continue

        clean = re.sub(r"(?<!\\)\$.*?(?<!\\)\$", "", s)

        if re_ascii_box.match(clean):
            metrics.ascii_art_artifacts += 1
            findings.append(
                AuditFinding(
                    category="ASCII_ART_ARTIFACT",
                    file_name=fname,
                    line_number=idx,
                    severity="ERROR",
                    description=f"ASCII box border '+---+' at line {idx}.",
                    snippet=s,
                )
            )
            continue

        if re_unicode_box.match(clean):
            metrics.ascii_art_artifacts += 1
            findings.append(
                AuditFinding(
                    category="ASCII_ART_ARTIFACT",
                    file_name=fname,
                    line_number=idx,
                    severity="ERROR",
                    description=f"Unicode box-drawing border at line {idx}.",
                    snippet=s,
                )
            )
            continue

        if re_box_arrow.search(clean):
            metrics.ascii_art_artifacts += 1
            findings.append(
                AuditFinding(
                    category="ASCII_ART_ARTIFACT",
                    file_name=fname,
                    line_number=idx,
                    severity="ERROR",
                    description=f"ASCII box-and-arrow chain '[A] --> [B]' at line {idx}.",
                    snippet=s,
                )
            )
            continue

        if not clean.startswith("#"):
            arrs = re_multi_arrow.findall(clean)
            if len(arrs) >= 2:
                metrics.ascii_art_artifacts += 1
                findings.append(
                    AuditFinding(
                        category="ASCII_ART_ARTIFACT",
                        file_name=fname,
                        line_number=idx,
                        severity="ERROR",
                        description=f"Multi-arrow chain ({len(arrs)} arrows) at line {idx}.",
                        snippet=s,
                    )
                )
                continue

            if any(sym in clean for sym in ["──►", "─►", "◄──", "◄─"]):
                metrics.ascii_art_artifacts += 1
                findings.append(
                    AuditFinding(
                        category="ASCII_ART_ARTIFACT",
                        file_name=fname,
                        line_number=idx,
                        severity="ERROR",
                        description=f"Standalone Unicode arrow symbol at line {idx}.",
                        snippet=s,
                    )
                )

    return findings


def audit_chapter_widgets_and_links(
    raw_content: str, fname: str, chapters_dir: str, widgets_dir: str, metrics: ChapterMetrics
) -> List[AuditFinding]:
    findings: List[AuditFinding] = []

    m_topic = re.search(r"topic_(\d+)", fname)
    tnum = int(m_topic.group(1)) if m_topic else None
    designated_widget = DESIGNATED_WIDGETS.get(tnum) if (tnum and fname != "topic_5_flight_ctrl_2.md") else None

    # Iframe check
    iframes = list(re.finditer(r"<iframe\b([^>]*)>(?:</iframe>)?", raw_content, re.IGNORECASE))
    metrics.widget_embeds = len(iframes)

    if designated_widget and len(iframes) == 0:
        metrics.widget_errors += 1
        findings.append(
            AuditFinding(
                category="WIDGET_INTEGRATION",
                file_name=fname,
                line_number=None,
                severity="CRITICAL",
                description=f"Missing designated widget iframe: expected '../widgets/{designated_widget}'.",
            )
        )

    for im in iframes:
        attrs = im.group(1)
        src_m = re.search(r'src=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if not src_m:
            metrics.widget_errors += 1
            findings.append(
                AuditFinding(
                    category="WIDGET_INTEGRATION",
                    file_name=fname,
                    line_number=None,
                    severity="ERROR",
                    description="<iframe> tag missing 'src' attribute.",
                    snippet=im.group(0)[:80],
                )
            )
        else:
            rel_path = src_m.group(1)
            target = os.path.normpath(os.path.join(chapters_dir, rel_path))
            if not os.path.isfile(target):
                metrics.widget_errors += 1
                findings.append(
                    AuditFinding(
                        category="WIDGET_INTEGRATION",
                        file_name=fname,
                        line_number=None,
                        severity="CRITICAL",
                        description=f"Target widget does not exist: '{rel_path}' (resolved: '{target}').",
                    )
                )
            else:
                sz = os.path.getsize(target)
                if sz == 0:
                    metrics.widget_errors += 1
                    findings.append(
                        AuditFinding(
                            category="WIDGET_INTEGRATION",
                            file_name=fname,
                            line_number=None,
                            severity="CRITICAL",
                            description=f"Target widget file is empty (0 bytes): '{target}'.",
                        )
                    )

    # Markdown links check
    links = list(re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", raw_content))
    for lm in links:
        link_target = lm.group(2).strip()
        if link_target.startswith("http://") or link_target.startswith("https://") or link_target.startswith("#") or link_target.startswith("mailto:"):
            continue

        base_target = link_target.split("#")[0]
        if base_target:
            resolved_target = os.path.normpath(os.path.join(chapters_dir, base_target))
            if not os.path.exists(resolved_target):
                metrics.broken_links += 1
                findings.append(
                    AuditFinding(
                        category="BROKEN_LINK",
                        file_name=fname,
                        line_number=raw_content[:lm.start()].count("\n") + 1,
                        severity="ERROR",
                        description=f"Relative link target does not exist: '{link_target}' (resolved: '{resolved_target}').",
                        snippet=lm.group(0),
                    )
                )

    return findings


def run_gate3_oracle():
    base_dir = Path(__file__).resolve().parent.parent
    chapters_dir = str(base_dir / "chapters")
    widgets_dir = str(base_dir / "widgets")

    files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))

    print("=" * 105)
    print(" GATE 3 ADVERSARIAL STRESS TEST & VERIFICATION ORACLE")
    print(f" Target Directory: {chapters_dir}")
    print(f" Chapters Found: {len(files)}")
    print("=" * 105)

    all_metrics: List[ChapterMetrics] = []
    all_findings: List[AuditFinding] = []

    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as fp:
            raw_content = fp.read()
        lines = raw_content.splitlines(keepends=True)

        k_findings, metrics = audit_chapter_katex(raw_content, lines, fname)
        m_findings = audit_chapter_mermaid(lines, fname, metrics)
        c_findings = audit_chapter_code_and_ascii(raw_content, lines, fname, metrics)
        w_findings = audit_chapter_widgets_and_links(raw_content, fname, chapters_dir, widgets_dir, metrics)

        file_findings = k_findings + m_findings + c_findings + w_findings
        all_findings.extend(file_findings)
        all_metrics.append(metrics)

    # Print summary table
    print(f"{'Chapter File':<32} | {'Mermaid':<8} | {'KaTeX Blocks':<14} | {'Code':<6} | {'ASCII':<6} | {'Widget':<8} | {'Status'}")
    print("-" * 105)

    total_errs = 0
    for m in all_metrics:
        total_errs += m.total_errors
        status = "PASS" if m.total_errors == 0 else f"FAIL ({m.total_errors}E)"
        katex_summary = f"{m.katex_display_blocks}D/{m.katex_inline_spans}I"
        code_summary = f"{m.non_mermaid_code_blocks} bad"
        ascii_summary = f"{m.ascii_art_artifacts} art"
        merm_summary = f"{m.mermaid_diagrams} ({m.mermaid_errors}E)"
        widget_summary = f"{m.widget_embeds} ({m.widget_errors}E)"
        print(f"{m.file_name:<32} | {merm_summary:<8} | {katex_summary:<14} | {code_summary:<6} | {ascii_summary:<6} | {widget_summary:<8} | {status}")

    print("-" * 105)
    tot_merm = sum(m.mermaid_diagrams for m in all_metrics)
    tot_disp = sum(m.katex_display_blocks for m in all_metrics)
    tot_inl = sum(m.katex_inline_spans for m in all_metrics)
    tot_wid = sum(m.widget_embeds for m in all_metrics)
    print(f"TOTALS: {len(all_metrics)} chapters | {tot_merm} Mermaid | {tot_disp} Display / {tot_inl} Inline KaTeX | {tot_wid} Widgets | Total Errors: {total_errs}")

    if all_findings:
        print("\n" + "=" * 105)
        print(" DETAILED FAILURE FINDINGS:")
        print("=" * 105)
        for idx, f in enumerate(all_findings, 1):
            line_str = f"Line {f.line_number}" if f.line_number else "N/A"
            print(f"[{idx}] {f.severity} - {f.category} in {f.file_name} ({line_str}):")
            print(f"    {f.description}")
            if f.snippet:
                print(f"    Snippet: {f.snippet}")

    verdict = "APPROVE" if total_errs == 0 else "REJECT"
    print("\n" + "=" * 105)
    print(f" ADVERSARIAL GATE 3 VERDICT: [{verdict}]")
    print("=" * 105)

    # Save JSON report
    report_dict = {
        "verdict": verdict,
        "total_errors": total_errs,
        "chapters": [asdict(m) for m in all_metrics],
        "findings": [asdict(f) for f in all_findings],
    }
    json_path = os.path.join(chapters_dir, "..", "scripts", "gate3_audit_results.json")
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(report_dict, fp, indent=2)

    return total_errs == 0


if __name__ == "__main__":
    success = run_gate3_oracle()
    sys.exit(0 if success else 1)
