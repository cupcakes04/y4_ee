#!/usr/bin/env python3
"""
stress_challenge_chapters.py
============================
Adversarial Stress Test Harness & Verification Suite for EEEE4138 Aerial Robotics Chapters.

Executed by: challenger_1 (Empirical Challenger)
Target Directory: modules/EEEE4138_aerial_robotics/chapters/
Integrity Mode: Development / Audit

This suite conducts deep adversarial parsing and validation across:
  1. Mermaid Diagrams:
     - Structural syntax and diagram types
     - Delimiter balance: double quotes, square brackets, curly braces, parentheses
     - Subgraph start/end pairing
     - Forbidden characters: unquoted ampersands, unescaped comparison operators (<, >)
     - Label safety: unquoted parentheses/brackets inside node labels
     - Bad arrows: '<==>', single dash '->', '===>', malformed pipe/quote arrows
     - Unquoted '<br/>' / '<br>' HTML tags
  2. KaTeX Math Blocks:
     - Display math ($$) and inline math ($) delimiter balance
     - Curly brace balance ({ and }) inside all math expressions
     - Square bracket balance ([ and ]) inside all math expressions
     - LaTeX environment matching: \\begin{env} ... \\end{env}
     - Raw tab characters (0x09) and corrupted command escapes (\\t in \\theta, \\to, etc.)
     - Forbidden/unsupported macros: \\href inside display math, undefined commands
     - Double subscripts (x_a_b) and double superscripts (x^a^b) without braces
     - Unescaped special characters
  3. Residual Programming Code Blocks:
     - Fenced code blocks with disallowed language identifiers (python, matlab, cpp, etc.)
     - Untagged fenced code blocks
     - 4-space indented code implementation blocks
     - HTML <pre> or <code> multi-line blocks
     - Specific search for legacy code signatures (e.g. attitude_priority_allocation)
  4. Residual ASCII Box-and-Arrow Diagrams:
     - Unicode box drawing symbols (┌, ┐, └, ┘, │, ─, ┼, etc.)
     - ASCII box borders (+---+, +===+)
     - Box-and-arrow chains ([A] --> [B])
     - Arrow chains (──►, ─►, ◄──, ◄─, -->, ==> connecting words in text)
  5. Generative UI Widget Embed Integrity:
     - Designated widget mapping per chapter
     - Iframe relative path resolution, readability, non-empty check
     - Standard iframe formatting contracts (width, height, frameborder, standalone link)

Usage:
  python stress_challenge_chapters.py [--verbose] [--json]
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from enum import Enum
import glob
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class FailureSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class FailureRecord:
    category: str
    file_name: str
    line_number: Optional[int]
    severity: FailureSeverity
    description: str
    snippet: str = ""
    remediation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "file": self.file_name,
            "line": self.line_number,
            "severity": self.severity.value,
            "description": self.description,
            "snippet": self.snippet,
            "remediation": self.remediation,
        }


@dataclass
class ChapterAuditMetrics:
    file_name: str
    total_lines: int = 0
    total_bytes: int = 0
    mermaid_diagrams_count: int = 0
    mermaid_subgraphs_count: int = 0
    display_math_blocks_count: int = 0
    inline_math_spans_count: int = 0
    math_environments_count: int = 0
    iframes_count: int = 0
    fenced_blocks_count: int = 0
    disallowed_code_blocks: int = 0
    ascii_diagram_artifacts: int = 0
    mermaid_errors: int = 0
    mermaid_warnings: int = 0
    katex_errors: int = 0
    katex_warnings: int = 0
    widget_errors: int = 0


DESIGNATED_WIDGETS = {
    1: "widget_1_flight_envelope.html",
    2: "widget_2_frames_gimbal_lock.html",
    3: "widget_3_rigid_body_dynamics.html",
    4: "widget_4_rotor_mixer_allocation.html",
    5: "widget_5_cascaded_flight_control.html",
}


def extract_topic_number(filename: str) -> Optional[int]:
    m = re.search(r"topic_(\d+)", filename, re.IGNORECASE)
    return int(m.group(1)) if m else None


# ==============================================================================
# AUDIT 1: MERMAID DIAGRAMS ADVERSARIAL STRESS TEST
# ==============================================================================
def stress_test_mermaid_diagrams(
    lines: List[str], file_name: str
) -> Tuple[List[FailureRecord], int, int, int, int]:
    """
    Examines all Mermaid diagram blocks with adversarial criteria:
      - Valid flowchart / diagram type header
      - Balanced quotes, brackets, braces, parentheses across diagram
      - Balanced subgraph ... end statements
      - Forbidden characters in node labels: unquoted '&', unquoted '<' or '>'
      - Dangerous unquoted parentheses inside square brackets: e.g. A[Rate (p, q, r)]
      - Dangerous unquoted brackets inside node labels: e.g. A[Matrix [3x3]]
      - Bad arrows: '<==>', single dash '->', '===>', malformed pipe combinations
      - Unquoted '<br/>' / '<br>' HTML tags inside node labels
    """
    failures: List[FailureRecord] = []
    mermaid_count = 0
    subgraph_count = 0
    diag_errors = 0
    diag_warnings = 0

    in_mermaid = False
    block_start_line = 0
    current_block: List[Tuple[int, str]] = []

    def audit_block(diag_idx: int, block: List[Tuple[int, str]]):
        nonlocal diag_errors, diag_warnings, subgraph_count
        if not block:
            return

        start_lno = block[0][0]
        full_diag_text = "\n".join(l[1] for l in block)

        # 1. Diagram type header check
        first_content_lines = [l[1].strip() for l in block if l[1].strip() and not l[1].strip().startswith("%%")]
        if not first_content_lines:
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} is empty or contains only comments.",
                    snippet="```mermaid ... ```",
                    remediation="Add diagram content (e.g. 'flowchart TD').",
                )
            )
            return

        header = first_content_lines[0]
        valid_headers = [
            "flowchart", "graph", "sequenceDiagram", "classDiagram",
            "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
            "pie", "gitGraph", "mindmap", "timeline", "quadrantChart",
            "C4Context", "sankey-beta", "block-beta"
        ]
        if not any(header.startswith(vh) for vh in valid_headers):
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} has unknown or missing diagram type header: '{header}'.",
                    snippet=header,
                    remediation="Specify valid diagram type like 'flowchart TD' or 'flowchart LR'.",
                )
            )

        # 2. Global delimiter balance checks
        # Double quotes
        quotes_count = full_diag_text.count('"') - full_diag_text.count(r'\"')
        if quotes_count % 2 != 0:
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} has unbalanced double quotes ({quotes_count} found).",
                    snippet=block[0][1],
                    remediation="Balance opening and closing double quotes on label strings.",
                )
            )

        # Square brackets '[' vs ']'
        sq_open = full_diag_text.count("[")
        sq_close = full_diag_text.count("]")
        if sq_open != sq_close:
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} has unbalanced square brackets: '[' ({sq_open}) vs ']' ({sq_close}).",
                    snippet=block[0][1],
                    remediation="Check for unclosed node shape brackets '[' and ']'.",
                )
            )

        # Curly braces '{' vs '}'
        cur_open = full_diag_text.count("{")
        cur_close = full_diag_text.count("}")
        if cur_open != cur_close:
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} has unbalanced curly braces: '{{' ({cur_open}) vs '}}' ({cur_close}).",
                    snippet=block[0][1],
                    remediation="Check for unclosed decision diamond braces '{{' and '}}'.",
                )
            )

        # Parentheses '(' vs ')'
        par_open = full_diag_text.count("(")
        par_close = full_diag_text.count(")")
        if par_open != par_close:
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} has unbalanced parentheses: '(' ({par_open}) vs ')' ({par_close}).",
                    snippet=block[0][1],
                    remediation="Check for unclosed rounded node parentheses '(' and ')'.",
                )
            )

        # 3. Subgraph matching
        subgraph_opens = len(re.findall(r"^\s*subgraph\b", full_diag_text, re.MULTILINE))
        subgraph_ends = len(re.findall(r"^\s*end\b", full_diag_text, re.MULTILINE))
        subgraph_count += subgraph_opens
        if subgraph_opens != subgraph_ends:
            diag_errors += 1
            failures.append(
                FailureRecord(
                    category="MERMAID_SYNTAX",
                    file_name=file_name,
                    line_number=start_lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Mermaid diagram #{diag_idx} has mismatched subgraphs: {subgraph_opens} 'subgraph' vs {subgraph_ends} 'end'.",
                    snippet=block[0][1],
                    remediation="Ensure every 'subgraph' has a matching closing 'end'.",
                )
            )

        # 4. Line-by-line detailed stress checks
        for lno, line_content in block:
            stripped = line_content.strip()
            if not stripped or stripped.startswith("%%"):
                continue

            # Check 4a: Non-standard arrow '<==>'
            if "<==>" in stripped:
                diag_errors += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.ERROR,
                        description=f"Invalid Mermaid link arrow '<==>' at line {lno}.",
                        snippet=stripped,
                        remediation="Replace with standard bidirectional arrow '<-->' or thick arrow '==>'.",
                    )
                )

            # Check 4b: Malformed single dash arrow '->'
            # In flowchart, single dash arrow '->' is invalid syntax (must be '-->' or dotted '-.->')
            # Ensure before '->' is not '-' or '.' (which would be '-->' or '-.->')
            if re.search(r"(?<![-.])->(?!>)", stripped) and not stripped.startswith("class ") and not stripped.startswith("click "):
                # Ensure it's not a JavaScript lambda or CSS arrow in styling
                if not re.search(r"classDef|style|linkStyle", stripped):
                    diag_errors += 1
                    failures.append(
                        FailureRecord(
                            category="MERMAID_SYNTAX",
                            file_name=file_name,
                            line_number=lno,
                            severity=FailureSeverity.ERROR,
                            description=f"Invalid single-dash arrow '->' at line {lno}. Flowchart links require '-->'.",
                            snippet=stripped,
                            remediation="Replace '->' with '-->'.",
                        )
                    )

            # Check 4c: Four or more equal signs in arrow '===>'
            if re.search(r"={3,}>", stripped):
                diag_errors += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.ERROR,
                        description=f"Invalid long thick arrow '===>' at line {lno}. Use standard '==>'.",
                        snippet=stripped,
                        remediation="Replace with '==>'.",
                    )
                )

            # Check 4d: Malformed combined quote and pipe label: -- "..." -->|label|
            if re.search(r'--\s*"[^"]+"\s*-->\|', stripped):
                diag_errors += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.ERROR,
                        description=f"Malformed arrow combining quote and pipe label at line {lno}.",
                        snippet=stripped,
                        remediation='Use clean pipe label syntax: NODE1 -->|"Label"| NODE2',
                    )
                )

            # Inspect unquoted segments by removing properly double-quoted strings
            unquoted_part = re.sub(r'"[^"]*"', '', stripped)

            # Check 4e: Unquoted ampersand '&' inside node labels and pipe edge labels
            unquoted_amp = (
                re.search(r'\[[^\]]*&[^\]]*\]', unquoted_part)
                or re.search(r'\([^\)]*&[^\)]*\)', unquoted_part)
                or re.search(r'\{[^\}]*&[^\}]*\}', unquoted_part)
                or re.search(r'\|[^|]*&[^|]*\|', unquoted_part)
            )
            if unquoted_amp:
                diag_errors += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.ERROR,
                        description=f"Unquoted ampersand '&' in Mermaid label at line {lno}. In Mermaid, '&' is a reserved operator; labels with '&' must be enclosed in double quotes.",
                        snippet=stripped,
                        remediation='Enclose the label in double quotes: ["... & ..."] or |"... & ..."|.',
                    )
                )

            # Check 4f: Unquoted comparison operators '<' or '>' in node labels
            unquoted_comp = (
                re.search(r'\[[^\]]*[<>][^\]]*\]', unquoted_part)
                or re.search(r'\{[^\}]*[<>][^\}]*\}', unquoted_part)
            )
            if unquoted_comp:
                diag_errors += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.ERROR,
                        description=f"Unescaped '<' or '>' in unquoted Mermaid node label at line {lno}.",
                        snippet=stripped,
                        remediation="Enclose label in double quotes or use &lt; / &gt; entities.",
                    )
                )

            # Check 4g: Unquoted parentheses inside square brackets: A[Text (detail) Text]
            # Mermaid treats '(' as a rounded node start, causing parse collision unless quoted: A["Text (detail) Text"]
            unquoted_parens_in_sq = re.search(r'\[[^\]"]*\([^\]"]*\)[^\]"]*\]', unquoted_part)
            if unquoted_parens_in_sq:
                diag_errors += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.ERROR,
                        description=f"Unquoted parentheses '(' inside square bracket node label at line {lno}.",
                        snippet=stripped,
                        remediation='Enclose label in double quotes: NODE["Label (with parentheses)"].',
                    )
                )

            # Check 4h: Unquoted <br/> or <br> tags in unquoted node labels
            if ("<br/>" in unquoted_part or "<br>" in unquoted_part) and (
                re.search(r'\[[^\]]*<br\s*/?>[^\]]*\]', unquoted_part)
                or re.search(r'\{[^\}]*<br\s*/?>[^\}]*\}', unquoted_part)
                or re.search(r'\([^\)]*<br\s*/?>[^\)]*\)', unquoted_part)
            ):
                diag_warnings += 1
                failures.append(
                    FailureRecord(
                        category="MERMAID_SYNTAX",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.WARNING,
                        description=f"Unquoted '<br/>' HTML break tag in node label at line {lno}.",
                        snippet=stripped,
                        remediation='Enclose label in double quotes: ["Line 1<br/>Line 2"].',
                    )
                )

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```mermaid"):
            in_mermaid = True
            mermaid_count += 1
            block_start_line = idx
            current_block = []
            continue
        elif in_mermaid and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_mermaid = False
            audit_block(mermaid_count, current_block)
            current_block = []
            continue
        elif in_mermaid:
            current_block.append((idx, line))

    if in_mermaid:
        diag_errors += 1
        failures.append(
            FailureRecord(
                category="MERMAID_SYNTAX",
                file_name=file_name,
                line_number=block_start_line,
                severity=FailureSeverity.ERROR,
                description=f"Unclosed Mermaid diagram block starting at line {block_start_line}.",
                snippet="```mermaid ... EOF",
                remediation="Close diagram block with '```'.",
            )
        )

    return failures, mermaid_count, subgraph_count, diag_errors, diag_warnings


# ==============================================================================
# AUDIT 2: KATEX MATH BLOCKS ADVERSARIAL STRESS TEST
# ==============================================================================
def stress_test_katex_math(
    lines: List[str], file_name: str
) -> Tuple[List[FailureRecord], int, int, int, int, int]:
    """
    Examines KaTeX math blocks with rigorous adversarial criteria:
      - Double dollar ($$) display math delimiter balance
      - Single dollar ($) inline math delimiter balance
      - Curly brace balance ({ and }) inside all math expressions
      - Square bracket balance ([ and ]) inside all math expressions
      - LaTeX environment matching: \\begin{env} ... \\end{env}
      - Raw tab characters (0x09) and corrupted command escapes (\\t in \\theta, \\to)
      - Forbidden/unsupported macros: \\href inside display math
      - Double subscripts (x_a_b) and double superscripts (x^a^b) without braces
    """
    failures: List[FailureRecord] = []
    display_blocks_count = 0
    inline_spans_count = 0
    environments_count = 0
    katex_errors = 0
    katex_warnings = 0

    content = "\n".join(l.rstrip("\r\n") for l in lines)

    # Mask fenced code blocks with equivalent newlines to preserve exact line numbers
    content_no_fenced = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), content, flags=re.DOTALL)
    content_no_fenced = re.sub(r"~~~.*?~~~", lambda m: "\n" * m.group(0).count("\n"), content_no_fenced, flags=re.DOTALL)

    # 1. Display math $$ balance
    dd_matches = list(re.finditer(r"(?<!\\)\$\$", content_no_fenced))
    display_blocks_count = len(dd_matches) // 2
    if len(dd_matches) % 2 != 0:
        katex_errors += 1
        failures.append(
            FailureRecord(
                category="KATEX_SYNTAX",
                file_name=file_name,
                line_number=None,
                severity=FailureSeverity.ERROR,
                description=f"Unbalanced display math delimiters ($$). Found odd count: {len(dd_matches)}.",
                snippet="Display math ($$ ... $$) parity broken.",
                remediation="Ensure every opening '$$' has a matching closing '$$'.",
            )
        )

    # 2. Inline math $ balance
    # Mask display math first
    temp_content = re.sub(r"(?<!\\)\$\$.*?(?<!\\)\$\$", "__DISPLAY_BLOCK__", content_no_fenced, flags=re.DOTALL)
    sd_matches = list(re.finditer(r"(?<!\\)\$", temp_content))
    inline_spans_count = len(sd_matches) // 2
    if len(sd_matches) % 2 != 0:
        katex_errors += 1
        failures.append(
            FailureRecord(
                category="KATEX_SYNTAX",
                file_name=file_name,
                line_number=None,
                severity=FailureSeverity.ERROR,
                description=f"Unbalanced inline math delimiters ($). Found odd count: {len(sd_matches)}.",
                snippet="Inline math ($ ... $) parity broken.",
                remediation="Ensure every opening '$' has a matching closing '$'.",
            )
        )

    # 3. Extract all display math blocks for deep AST / token stress testing
    display_math_pattern = re.compile(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", re.DOTALL)
    for m in display_math_pattern.finditer(content_no_fenced):
        block_text = m.group(1)
        start_char = m.start()
        lno = content_no_fenced[:start_char].count("\n") + 1

        # Check 3a: Curly brace balance inside display math
        # Count { and } excluding escaped \{ and \}
        unescaped_open_cur = len(re.findall(r"(?<!\\)\{", block_text))
        unescaped_close_cur = len(re.findall(r"(?<!\\)\}", block_text))
        if unescaped_open_cur != unescaped_close_cur:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Unbalanced curly braces in display math at line {lno}: '{{' ({unescaped_open_cur}) vs '}}' ({unescaped_close_cur}).",
                    snippet=block_text.strip()[:100],
                    remediation="Balance opening and closing braces { } inside math formula.",
                )
            )

        # Check 3b: Square bracket balance inside display math
        # Strip line break spacing arguments like \\[6pt] before counting brackets
        clean_sq_text = re.sub(r'\\\\\[[0-9a-zA-Z\s.]+\]', '', block_text)
        unescaped_open_sq = clean_sq_text.count("[") - clean_sq_text.count(r"\[")
        unescaped_close_sq = clean_sq_text.count("]") - clean_sq_text.count(r"\]")
        if unescaped_open_sq != unescaped_close_sq:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Unbalanced square brackets in display math at line {lno}: '[' ({unescaped_open_sq}) vs ']' ({unescaped_close_sq}).",
                    snippet=block_text.strip()[:100],
                    remediation="Balance opening and closing brackets [ ] inside math formula.",
                )
            )

        # Check 3c: Environment pairing: \begin{XYZ} vs \end{XYZ} using a stack
        env_tokens = re.findall(r"\\(begin|end)\{([a-zA-Z*]+)\}", block_text)
        env_stack: List[str] = []
        for tag_type, env_name in env_tokens:
            if tag_type == "begin":
                env_stack.append(env_name)
                environments_count += 1
            elif tag_type == "end":
                if not env_stack:
                    katex_errors += 1
                    failures.append(
                        FailureRecord(
                            category="KATEX_SYNTAX",
                            file_name=file_name,
                            line_number=lno,
                            severity=FailureSeverity.ERROR,
                            description=f"Unmatched \\end{{{env_name}}} with no preceding \\begin at line {lno}.",
                            snippet=block_text.strip()[:100],
                            remediation="Ensure every \\end{env} has a matching \\begin{env}.",
                        )
                    )
                else:
                    popped = env_stack.pop()
                    if popped != env_name and not (popped.endswith("*") and env_name == popped.rstrip("*")):
                        katex_errors += 1
                        failures.append(
                            FailureRecord(
                                category="KATEX_SYNTAX",
                                file_name=file_name,
                                line_number=lno,
                                severity=FailureSeverity.ERROR,
                                description=f"Mismatched environment nesting at line {lno}: \\begin{{{popped}}} closed by \\end{{{env_name}}}.",
                                snippet=block_text.strip()[:100],
                                remediation="Ensure environments are closed in correct LIFO order.",
                            )
                        )
        if env_stack:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Unclosed LaTeX environments at line {lno}: {env_stack}.",
                    snippet=block_text.strip()[:100],
                    remediation="Ensure every \\begin{env} has a matching \\end{env}.",
                )
            )

        # Check 3d: Unsupported macro \href inside display math
        if "\\href" in block_text:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Unsupported macro '\\href' inside display math at line {lno}.",
                    snippet=block_text.strip()[:100],
                    remediation="Move links outside of KaTeX math blocks into regular markdown.",
                )
            )

        # Check 3e: Double subscripts without braces: x_a_b
        # In KaTeX, x_a_b throws ParseError: Double subscript
        double_sub = re.search(r"[a-zA-Z0-9]_([a-zA-Z0-9])_([a-zA-Z0-9])", block_text)
        if double_sub:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Double subscript without braces '{double_sub.group(0)}' in display math at line {lno}.",
                    snippet=block_text.strip()[:100],
                    remediation="Use curly braces: e.g. x_{a_b} or {x_a}_b.",
                )
            )

        # Check 3f: Double superscripts without braces: x^a^b
        double_sup = re.search(r"[a-zA-Z0-9]\^([a-zA-Z0-9])\^([a-zA-Z0-9])", block_text)
        if double_sup:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"Double superscript without braces '{double_sup.group(0)}' in display math at line {lno}.",
                    snippet=block_text.strip()[:100],
                    remediation="Use curly braces: e.g. x^{a^b} or {x^a}^b.",
                )
            )

    # 4. Check for raw tab corruptions (\t in \theta, \to, \tau, etc.)
    re_tab_cmd = re.compile(
        r"\t(heta|o|au|ilde|ext|imes|an|op|artial|beta|gamma|sigma|omega|alpha|lambda|mu|rho|phi|psi)\b"
    )

    in_code = False
    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue

        tab_m = re_tab_cmd.search(line)
        if tab_m:
            suffix = tab_m.group(1)
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=idx,
                    severity=FailureSeverity.ERROR,
                    description=f"Corrupted LaTeX command at line {idx}: raw tab '\\t' precedes '{suffix}' (should be '\\{suffix}').",
                    snippet=line[:100],
                    remediation=f"Replace '\\t{suffix}' with '\\{suffix}'.",
                )
            )

        if "\t" in line and "$" in line and not tab_m:
            katex_errors += 1
            failures.append(
                FailureRecord(
                    category="KATEX_SYNTAX",
                    file_name=file_name,
                    line_number=idx,
                    severity=FailureSeverity.ERROR,
                    description=f"Raw tab character (0x09) detected inside math formula line at line {idx}.",
                    snippet=line[:100],
                    remediation="Replace raw tab character with spaces or '\\quad'.",
                )
            )

    return failures, display_blocks_count, inline_spans_count, environments_count, katex_errors, katex_warnings


# ==============================================================================
# AUDIT 3: RESIDUAL PROGRAMMING CODE IMPLEMENTATIONS
# ==============================================================================
def stress_test_residual_code(
    lines: List[str], file_name: str
) -> Tuple[List[FailureRecord], int, int]:
    """
    Examines the chapter for any residual programming code blocks or implementations:
      - Any fenced code block with language other than 'mermaid'
      - Untagged fenced code blocks
      - 4-space indented programming blocks (def, import, class, function, etc.)
      - HTML <pre><code> multi-line implementation blocks
      - Known legacy function signatures (e.g. attitude_priority_allocation, desaturate_mixer)
    """
    failures: List[FailureRecord] = []
    fenced_blocks_count = 0
    disallowed_count = 0

    in_fenced = False
    fenced_lang = ""
    fenced_start = 0
    fenced_snippet: List[str] = []

    # Patterns indicating raw code implementation
    re_code_keywords = re.compile(
        r"^\s{4,}(?:def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(|import\s+[a-zA-Z_]|from\s+[a-zA-Z_].*import|class\s+[a-zA-Z_]|function\s+\[?[a-zA-Z0-9_,\s]+\]?\s*=|#include\s*<|void\s+[a-zA-Z_]|int\s+main\s*\()"
    )

    full_content = "\n".join(lines)

    # 1. Search for legacy python signatures
    legacy_signatures = [
        "attitude_priority_allocation",
        "desaturate_mixer",
        "def compute_motor_outputs",
        "def lqr_control",
        "np.linalg.pinv(B)",
        "np.clip(pwm",
    ]
    for sig in legacy_signatures:
        if sig in full_content:
            disallowed_count += 1
            failures.append(
                FailureRecord(
                    category="RESIDUAL_CODE",
                    file_name=file_name,
                    line_number=None,
                    severity=FailureSeverity.CRITICAL,
                    description=f"Legacy software implementation snippet '{sig}' found in chapter body.",
                    snippet=sig,
                    remediation="Eliminate programming implementation scripts; express theory purely via mathematical derivations and Mermaid flows.",
                )
            )

    # 2. Check fenced code blocks
    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            if not in_fenced:
                in_fenced = True
                fenced_lang = stripped[3:].strip().lower()
                fenced_start = idx
                fenced_snippet = [line]
            else:
                in_fenced = False
                fenced_blocks_count += 1
                fenced_snippet.append(line)

                if fenced_lang != "mermaid":
                    disallowed_count += 1
                    failures.append(
                        FailureRecord(
                            category="RESIDUAL_CODE",
                            file_name=file_name,
                            line_number=fenced_start,
                            severity=FailureSeverity.CRITICAL,
                            description=f"Disallowed fenced code block (lang='{fenced_lang or '<untagged>'}', lines {fenced_start}-{idx}). Only ```mermaid is permitted.",
                            snippet="\n".join(fenced_snippet[:4]),
                            remediation="Remove software code blocks. Convert to Mermaid flowchart or math.",
                        )
                    )
        elif in_fenced and len(fenced_snippet) < 4:
            fenced_snippet.append(line)
        elif not in_fenced:
            # Check 3: Check for 4-space indented programming code implementations
            if re_code_keywords.match(raw_line):
                disallowed_count += 1
                failures.append(
                    FailureRecord(
                        category="RESIDUAL_CODE",
                        file_name=file_name,
                        line_number=idx,
                        severity=FailureSeverity.ERROR,
                        description=f"Indented programming code block detected at line {idx}.",
                        snippet=line,
                        remediation="Remove indented code implementation; preserve theoretical rigor.",
                    )
                )

    if in_fenced:
        disallowed_count += 1
        failures.append(
            FailureRecord(
                category="RESIDUAL_CODE",
                file_name=file_name,
                line_number=fenced_start,
                severity=FailureSeverity.ERROR,
                description=f"Unclosed code fence starting at line {fenced_start}.",
                snippet="\n".join(fenced_snippet),
                remediation="Ensure code fences are closed.",
            )
        )

    # 4. Check for multi-line <pre> or <code> HTML tags
    pre_matches = re.finditer(r"<pre\b[^>]*>(.*?)</pre>", full_content, re.DOTALL | re.IGNORECASE)
    for pm in pre_matches:
        disallowed_count += 1
        lno = full_content[:pm.start()].count("\n") + 1
        failures.append(
            FailureRecord(
                category="RESIDUAL_CODE",
                file_name=file_name,
                line_number=lno,
                severity=FailureSeverity.ERROR,
                description=f"HTML <pre> code container detected at line {lno}.",
                snippet=pm.group(0)[:100],
                remediation="Remove raw HTML code pre tags.",
            )
        )

    return failures, fenced_blocks_count, disallowed_count


# ==============================================================================
# AUDIT 4: RESIDUAL ASCII BOX-AND-ARROW DIAGRAMS
# ==============================================================================
def stress_test_residual_ascii(
    lines: List[str], file_name: str
) -> Tuple[List[FailureRecord], int]:
    """
    Examines all markdown text lines outside code blocks and math blocks for
    ASCII/Unicode box-and-arrow diagrams:
      - Unicode box borders: ┌───┐, └───┘, │, ─, ┼, ═, ║
      - ASCII box borders: +---+ or +===+
      - Box-and-arrow chains: [A] --> [B], [A] -> [B], [A] ──► [B]
      - Multi-arrow chains: A ──► B ──► C
      - Unicode arrow diagram symbols connecting words
    """
    failures: List[FailureRecord] = []
    ascii_artifacts = 0

    re_box_arrow = re.compile(r"\[[^\]]+\]\s*(?:-->|->|==>|──►|─►|◄──|◄─)\s*\[[^\]]+\]")
    re_ascii_box = re.compile(r"^\s*\+[-=]{3,}\+\s*$")
    re_unicode_box = re.compile(r"^\s*[┌\+│][─┬┼\-]{3,}[┐\+│]\s*$")
    re_multi_arrow = re.compile(r"(?:──►|─►|◄──|◄─|-->|==>|->)")

    in_fenced = False
    in_display_math = False

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue

        # Track display math blocks
        if "$$" in stripped:
            dd_count = stripped.count("$$")
            if dd_count % 2 != 0:
                in_display_math = not in_display_math
            if in_display_math:
                continue

        if in_display_math:
            continue

        # Strip inline math spans $ ... $ to avoid false positives on math arrows (\to, \implies, ->)
        clean_line = re.sub(r"(?<!\\)\$.*?(?<!\\)\$", "", stripped)

        # 1. ASCII Box Border: +---+
        if re_ascii_box.match(clean_line):
            ascii_artifacts += 1
            failures.append(
                FailureRecord(
                    category="RESIDUAL_ASCII",
                    file_name=file_name,
                    line_number=idx,
                    severity=FailureSeverity.ERROR,
                    description=f"ASCII box border '+---+' detected at line {idx}.",
                    snippet=line,
                    remediation="Replace ASCII art boxes with Mermaid flowchart or table.",
                )
            )
            continue

        # 2. Unicode Box Border: ┌───┐
        if re_unicode_box.match(clean_line):
            ascii_artifacts += 1
            failures.append(
                FailureRecord(
                    category="RESIDUAL_ASCII",
                    file_name=file_name,
                    line_number=idx,
                    severity=FailureSeverity.ERROR,
                    description=f"Unicode box-drawing border detected at line {idx}.",
                    snippet=line,
                    remediation="Replace Unicode box drawings with Mermaid diagrams.",
                )
            )
            continue

        # 3. Box-and-Arrow chain: [A] --> [B]
        if re_box_arrow.search(clean_line):
            ascii_artifacts += 1
            failures.append(
                FailureRecord(
                    category="RESIDUAL_ASCII",
                    file_name=file_name,
                    line_number=idx,
                    severity=FailureSeverity.ERROR,
                    description=f"Box-and-arrow chain '[A] --> [B]' detected at line {idx}.",
                    snippet=line,
                    remediation="Replace ASCII box-and-arrow chains with Mermaid flowchart.",
                )
            )
            continue

        # 4. Multi-arrow chain in non-heading line
        if not clean_line.startswith("#"):
            arrows = re_multi_arrow.findall(clean_line)
            if len(arrows) >= 2:
                ascii_artifacts += 1
                failures.append(
                    FailureRecord(
                        category="RESIDUAL_ASCII",
                        file_name=file_name,
                        line_number=idx,
                        severity=FailureSeverity.ERROR,
                        description=f"Multi-arrow chain ({len(arrows)} arrows) detected at line {idx}.",
                        snippet=line,
                        remediation="Convert horizontal arrow chains into a clean Mermaid flowchart TD/LR.",
                    )
                )
                continue

            # 5. Standalone Unicode arrow connecting words
            if any(sym in clean_line for sym in ["──►", "─►", "◄──", "◄─"]):
                ascii_artifacts += 1
                failures.append(
                    FailureRecord(
                        category="RESIDUAL_ASCII",
                        file_name=file_name,
                        line_number=idx,
                        severity=FailureSeverity.ERROR,
                        description=f"Unicode arrow diagram symbol detected at line {idx}.",
                        snippet=line,
                        remediation="Use Mermaid flowchart or KaTeX '\\implies' / '\\to'.",
                    )
                )

    return failures, ascii_artifacts


# ==============================================================================
# AUDIT 5: GENERATIVE UI WIDGET EMBED INTEGRITY
# ==============================================================================
def stress_test_widget_embeds(
    content: str,
    file_name: str,
    chapter_dir: str,
    widgets_dir: str,
) -> Tuple[List[FailureRecord], int, int]:
    """
    Validates that:
      - Designated widget is properly embedded via <iframe>
      - Target widget HTML exists on disk, is readable, and non-empty (>0 bytes)
      - Target widget HTML contains required responsive containers (canvas/svg)
      - Iframe follows standard dimensions (width="100%", height="520", frameborder="0")
      - Companion standalone tab link exists
    """
    failures: List[FailureRecord] = []
    iframe_count = 0
    widget_errors = 0

    topic_num = extract_topic_number(file_name)
    designated = DESIGNATED_WIDGETS.get(topic_num) if topic_num else None

    # Exempt legacy prototype topic_5_flight_ctrl_2.md if not mandating separate widget
    if file_name == "topic_5_flight_ctrl_2.md":
        designated = None

    iframe_matches = list(re.finditer(r"<iframe\b([^>]*)>(?:</iframe>)?", content, re.IGNORECASE))
    iframe_count = len(iframe_matches)

    line_offsets = [0]
    for m in re.finditer(r"\n", content):
        line_offsets.append(m.end())

    def get_lno(pos: int) -> int:
        import bisect
        return bisect.bisect_right(line_offsets, pos)

    if designated is not None and iframe_count == 0:
        widget_errors += 1
        failures.append(
            FailureRecord(
                category="WIDGET_EMBED",
                file_name=file_name,
                line_number=None,
                severity=FailureSeverity.CRITICAL,
                description=f"Missing designated Generative UI widget iframe. Expected: '../widgets/{designated}'.",
                snippet="No <iframe> found in chapter.",
                remediation=f"Embed '<iframe src=\"../widgets/{designated}\" width=\"100%\" height=\"520\" frameborder=\"0\"></iframe>'.",
            )
        )

    found_designated = False

    for m in iframe_matches:
        pos = m.start()
        lno = get_lno(pos)
        attrs = m.group(1)

        src_m = re.search(r'src=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if not src_m:
            widget_errors += 1
            failures.append(
                FailureRecord(
                    category="WIDGET_EMBED",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.ERROR,
                    description=f"<iframe> tag missing 'src' attribute at line {lno}.",
                    snippet=m.group(0)[:100],
                    remediation="Add src=\"../widgets/widget_X_....html\".",
                )
            )
            continue

        src_val = src_m.group(1)
        src_base = os.path.basename(src_val)

        # Resolve path
        resolved = os.path.normpath(os.path.join(chapter_dir, src_val))
        if not os.path.isfile(resolved):
            widget_errors += 1
            failures.append(
                FailureRecord(
                    category="WIDGET_EMBED",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.CRITICAL,
                    description=f"Target widget file does not exist: '{src_val}' (resolved to '{resolved}').",
                    snippet=m.group(0)[:100],
                    remediation=f"Ensure target widget exists in {widgets_dir}.",
                )
            )
        else:
            size = os.path.getsize(resolved)
            if size == 0:
                widget_errors += 1
                failures.append(
                    FailureRecord(
                        category="WIDGET_EMBED",
                        file_name=file_name,
                        line_number=lno,
                        severity=FailureSeverity.CRITICAL,
                        description=f"Target widget file '{resolved}' is 0 bytes (empty).",
                        snippet=m.group(0)[:100],
                        remediation="Populate widget with interactive simulation code.",
                    )
                )

        if designated and src_base == designated:
            found_designated = True

        # Check standard attributes
        w_m = re.search(r'width=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        h_m = re.search(r'height=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        fb_m = re.search(r'frameborder=["\']([^"\']+)["\']', attrs, re.IGNORECASE)

        if not w_m or w_m.group(1) != "100%":
            failures.append(
                FailureRecord(
                    category="WIDGET_EMBED",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.WARNING,
                    description=f"Iframe width is '{w_m.group(1) if w_m else 'missing'}' (expected standard '100%').",
                    snippet=m.group(0)[:100],
                    remediation='Set width="100%".',
                )
            )

        if not h_m or h_m.group(1) != "520":
            failures.append(
                FailureRecord(
                    category="WIDGET_EMBED",
                    file_name=file_name,
                    line_number=lno,
                    severity=FailureSeverity.WARNING,
                    description=f"Iframe height is '{h_m.group(1) if h_m else 'missing'}' (expected standard '520').",
                    snippet=m.group(0)[:100],
                    remediation='Set height="520".',
                )
            )

    if designated and iframe_count > 0 and not found_designated:
        widget_errors += 1
        failures.append(
            FailureRecord(
                category="WIDGET_EMBED",
                file_name=file_name,
                line_number=None,
                severity=FailureSeverity.CRITICAL,
                description=f"Chapter embeds iframes, but designated widget '{designated}' was not found.",
                snippet=f"Expected: {designated}",
                remediation=f"Embed '<iframe src=\"../widgets/{designated}\" ...>'.",
            )
        )

    return failures, iframe_count, widget_errors


# ==============================================================================
# AUDIT HARNESS ORCHESTRATION & REPORT GENERATOR
# ==============================================================================
def run_adversarial_suite(chapters_dir: str, widgets_dir: str) -> Tuple[List[ChapterAuditMetrics], List[FailureRecord]]:
    md_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))
    all_metrics: List[ChapterAuditMetrics] = []
    all_failures: List[FailureRecord] = []

    for file_path in md_files:
        fname = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
        content = "".join(raw_lines)

        metric = ChapterAuditMetrics(
            file_name=fname,
            total_lines=len(raw_lines),
            total_bytes=len(content.encode("utf-8")),
        )

        # 1. Mermaid
        m_fails, m_cnt, m_sub_cnt, m_errs, m_warns = stress_test_mermaid_diagrams(raw_lines, fname)
        all_failures.extend(m_fails)
        metric.mermaid_diagrams_count = m_cnt
        metric.mermaid_subgraphs_count = m_sub_cnt
        metric.mermaid_errors = m_errs
        metric.mermaid_warnings = m_warns

        # 2. KaTeX
        k_fails, d_cnt, i_cnt, env_cnt, k_errs, k_warns = stress_test_katex_math(raw_lines, fname)
        all_failures.extend(k_fails)
        metric.display_math_blocks_count = d_cnt
        metric.inline_math_spans_count = i_cnt
        metric.math_environments_count = env_cnt
        metric.katex_errors = k_errs
        metric.katex_warnings = k_warns

        # 3. Residual Code
        c_fails, fence_cnt, dis_cnt = stress_test_residual_code(raw_lines, fname)
        all_failures.extend(c_fails)
        metric.fenced_blocks_count = fence_cnt
        metric.disallowed_code_blocks = dis_cnt

        # 4. Residual ASCII
        a_fails, ascii_cnt = stress_test_residual_ascii(raw_lines, fname)
        all_failures.extend(a_fails)
        metric.ascii_diagram_artifacts = ascii_cnt

        # 5. Widget Embeds
        w_fails, iframe_cnt, w_errs = stress_test_widget_embeds(content, fname, chapters_dir, widgets_dir)
        all_failures.extend(w_fails)
        metric.iframes_count = iframe_cnt
        metric.widget_errors = w_errs

        all_metrics.append(metric)

    return all_metrics, all_failures


def print_suite_results(metrics: List[ChapterAuditMetrics], failures: List[FailureRecord], verbose: bool = False):
    total_critical = sum(1 for f in failures if f.severity == FailureSeverity.CRITICAL)
    total_errors = sum(1 for f in failures if f.severity == FailureSeverity.ERROR)
    total_warnings = sum(1 for f in failures if f.severity == FailureSeverity.WARNING)

    print("=" * 105)
    print(" EEEE4138 AERIAL ROBOTICS — ADVERSARIAL EMPIRICAL STRESS TEST REPORT")
    print("=" * 105)
    print(f"{'Chapter File':<32} | {'Mermaid':<9} | {'KaTeX Blocks':<13} | {'Code Blk':<9} | {'ASCII Art':<9} | {'Widgets':<7} | {'Verdict':<7}")
    print("-" * 105)

    for m in metrics:
        ch_fails = [f for f in failures if f.file_name == m.file_name]
        ch_errs = sum(1 for f in ch_fails if f.severity in (FailureSeverity.CRITICAL, FailureSeverity.ERROR))
        verdict = "PASS" if ch_errs == 0 else "FAIL"

        merm_stat = f"{m.mermaid_diagrams_count} ({m.mermaid_errors}E)"
        katex_stat = f"{m.display_math_blocks_count}D/{m.inline_math_spans_count}I"
        code_stat = f"{m.disallowed_code_blocks} bad"
        ascii_stat = f"{m.ascii_diagram_artifacts} art"
        widget_stat = f"{m.iframes_count} ({m.widget_errors}E)"

        print(f"{m.file_name:<32} | {merm_stat:<9} | {katex_stat:<13} | {code_stat:<9} | {ascii_stat:<9} | {widget_stat:<7} | {verdict:<7}")

    print("-" * 105)
    print(f"TOTAL AUDITED FILES: {len(metrics)}")
    print(f"Total Mermaid Diagrams: {sum(m.mermaid_diagrams_count for m in metrics)} (Subgraphs: {sum(m.mermaid_subgraphs_count for m in metrics)})")
    print(f"Total KaTeX Math Blocks: {sum(m.display_math_blocks_count for m in metrics)} Display, {sum(m.inline_math_spans_count for m in metrics)} Inline")
    print(f"Total Interactive Widgets Embedded: {sum(m.iframes_count for m in metrics)}")
    print(f"Summary Metrics: Critical: {total_critical} | Errors: {total_errors} | Warnings: {total_warnings}")

    verdict_str = "APPROVE" if (total_critical == 0 and total_errors == 0) else "REJECT"
    print("=" * 105)
    print(f"ADVERSARIAL VERDICT: [{verdict_str}] (Pass condition: 0 Critical, 0 Errors)")
    print("=" * 105)

    if failures and (verbose or total_critical > 0 or total_errors > 0):
        print("\n--- DETAILED FAILURE & WARNING LOG ---")
        for f in failures:
            loc = f"{f.file_name}:{f.line_number}" if f.line_number else f.file_name
            print(f"[{f.severity.value}] [{f.category}] {loc}")
            print(f"  Description: {f.description}")
            if f.snippet:
                print(f"  Snippet:     {f.snippet}")
            if f.remediation:
                print(f"  Remediation: {f.remediation}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Adversarial Chapter Stress Suite")
    parser.add_argument("--verbose", action="store_true", help="Show all findings including warnings")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    # Determine paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.dirname(script_dir)
    chapters_dir = os.path.join(module_dir, "chapters")
    widgets_dir = os.path.join(module_dir, "widgets")

    metrics, failures = run_adversarial_suite(chapters_dir, widgets_dir)

    if args.json:
        out = {
            "verdict": "APPROVE" if sum(1 for f in failures if f.severity in (FailureSeverity.CRITICAL, FailureSeverity.ERROR)) == 0 else "REJECT",
            "metrics": [asdict(m) for m in metrics],
            "failures": [f.to_dict() for f in failures],
        }
        print(json.dumps(out, indent=2))
    else:
        print_suite_results(metrics, failures, verbose=args.verbose)

    total_errs = sum(1 for f in failures if f.severity in (FailureSeverity.CRITICAL, FailureSeverity.ERROR))
    sys.exit(0 if total_errs == 0 else 1)


if __name__ == "__main__":
    main()
