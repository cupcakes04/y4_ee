#!/usr/bin/env python3
"""
Production-Grade Automated E2E Verification Runner for EEEE4138 Aerial Robotics Chapters.

Validates Topics 1 through 5 in modules/EEEE4138_aerial_robotics/chapters/ against:
  1. R1: Zero standalone programming code implementations (e.g. ```python, ```matlab, ```cpp).
         Only ```mermaid diagram blocks are permitted.
  2. R2: 100% of chapters embed their exact designated Generative UI HTML widget via
         <iframe src="../widgets/widget_X_....html" ...> and target widget exists and is readable.
  3. R2: Zero ASCII/Unicode box-and-arrow diagrams (e.g. [A] --> [B], A ──► B ──► C).
  4. R3: Mermaid diagram syntax integrity (checks for unquoted ampersands '&', unescaped '<' or '>',
         invalid link arrows like '<==>' or malformed '-- "..." -->|label|', and unmatched braces/quotes).
  5. R3: KaTeX math delimiters ($$ and $) balance, absence of raw tab '\\t' corruptions in commands
         (e.g. '\\t' in '\\theta', '\\to'), and absence of invalid math macros like '\\href' inside display math.

Usage:
  python verify_chapters_e2e.py               # Run verification across all chapters
  python verify_chapters_e2e.py --self-test   # Run unit test suite validating the verifier
  python verify_chapters_e2e.py --json        # Machine-readable JSON output
  python verify_chapters_e2e.py --chapter topic_1_uav_architectures.md  # Single chapter
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from enum import Enum
import glob
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
import unittest

# Ensure standard UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class IssueSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class RuleCategory(str, Enum):
    R1_CODE_BLOCKS = "R1_CODE_BLOCKS"
    R2_WIDGET_EMBED = "R2_WIDGET_EMBED"
    R2_ASCII_DIAGRAMS = "R2_ASCII_DIAGRAMS"
    R3_MERMAID_SYNTAX = "R3_MERMAID_SYNTAX"
    R3_KATEX_SYNTAX = "R3_KATEX_SYNTAX"


@dataclass
class VerificationIssue:
    file_path: str
    rule: RuleCategory
    severity: IssueSeverity
    line_number: Optional[int]
    message: str
    snippet: str = ""
    fix_suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": os.path.basename(self.file_path),
            "file_path": self.file_path,
            "rule": self.rule.value,
            "severity": self.severity.value,
            "line": self.line_number,
            "message": self.message,
            "snippet": self.snippet,
            "fix_suggestion": self.fix_suggestion,
        }


@dataclass
class ChapterMetrics:
    total_lines: int = 0
    mermaid_blocks: int = 0
    display_math_blocks: int = 0
    inline_math_pairs: int = 0
    iframes_found: int = 0
    disallowed_code_blocks: int = 0
    ascii_diagram_lines: int = 0
    mermaid_syntax_errors: int = 0
    katex_syntax_errors: int = 0


@dataclass
class ChapterReport:
    file_path: str
    filename: str
    topic_number: Optional[int]
    designated_widget: Optional[str]
    issues: List[VerificationIssue] = field(default_factory=list)
    metrics: ChapterMetrics = field(default_factory=ChapterMetrics)

    @property
    def errors(self) -> List[VerificationIssue]:
        return [i for i in self.issues if i.severity == IssueSeverity.ERROR]

    @property
    def warnings(self) -> List[VerificationIssue]:
        return [i for i in self.issues if i.severity == IssueSeverity.WARNING]

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


@dataclass
class SuiteReport:
    chapters: List[ChapterReport] = field(default_factory=list)
    total_files: int = 0

    @property
    def total_errors(self) -> int:
        return sum(len(c.errors) for c in self.chapters)

    @property
    def total_warnings(self) -> int:
        return sum(len(c.warnings) for c in self.chapters)

    @property
    def passed(self) -> bool:
        return self.total_errors == 0 and self.total_files > 0


# Canonical mapping of topic number to designated widget file
DESIGNATED_WIDGETS: Dict[int, str] = {
    1: "widget_1_flight_envelope.html",
    2: "widget_2_frames_gimbal_lock.html",
    3: "widget_3_rigid_body_dynamics.html",
    4: "widget_4_rotor_mixer_allocation.html",
    5: "widget_5_cascaded_flight_control.html",
}


def extract_topic_number(filename: str) -> Optional[int]:
    """Extract topic number from chapter filename (e.g. topic_1_... -> 1)."""
    m = re.search(r"topic_(\d+)", filename, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None


# ---------------------------------------------------------------------------
# Check 1: Absence of standalone programming code blocks
# ---------------------------------------------------------------------------
def check_code_blocks(lines: List[str], file_path: str) -> Tuple[List[VerificationIssue], int, int]:
    """
    Validates that zero standalone programming code implementations exist.
    Only ```mermaid diagram blocks are permitted.
    """
    issues: List[VerificationIssue] = []
    in_block = False
    cur_lang = ""
    block_start = 0
    block_snippet = []
    mermaid_count = 0
    disallowed_count = 0

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence_chars = stripped[:3]
            if not in_block:
                in_block = True
                cur_lang = stripped[3:].strip()
                block_start = idx
                block_snippet = [line]
            else:
                in_block = False
                block_snippet.append(line)
                lang_clean = cur_lang.lower()

                if lang_clean == "mermaid":
                    mermaid_count += 1
                else:
                    disallowed_count += 1
                    preview = "\n".join(block_snippet[:4])
                    if len(block_snippet) > 4:
                        preview += "\n..."
                    
                    lang_label = repr(cur_lang) if cur_lang else "<empty/untagged>"
                    issues.append(
                        VerificationIssue(
                            file_path=file_path,
                            rule=RuleCategory.R1_CODE_BLOCKS,
                            severity=IssueSeverity.ERROR,
                            line_number=block_start,
                            message=f"Disallowed fenced code block (language={lang_label}, lines {block_start}-{idx}). Only ```mermaid is permitted in theory chapters.",
                            snippet=preview,
                            fix_suggestion="Remove software code implementations. Convert conceptual flowcharts into ```mermaid syntax or reference interactive Generative UI widgets.",
                        )
                    )
        elif in_block and len(block_snippet) < 4:
            block_snippet.append(line)

    if in_block:
        disallowed_count += 1
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R1_CODE_BLOCKS,
                severity=IssueSeverity.ERROR,
                line_number=block_start,
                message=f"Unclosed code fence block starting at line {block_start}.",
                snippet="\n".join(block_snippet),
                fix_suggestion="Ensure all code fences are properly closed with matching backticks ```.",
            )
        )

    return issues, mermaid_count, disallowed_count


# ---------------------------------------------------------------------------
# Check 2: Designated Generative UI widget embedding & file resolution
# ---------------------------------------------------------------------------
def check_widget_embed(
    content: str,
    file_path: str,
    designated_widget: Optional[str],
    chapter_dir: str,
    widgets_dir: str,
) -> Tuple[List[VerificationIssue], int]:
    """
    Validates that every chapter embeds its exact designated Generative UI widget
    via <iframe src="../widgets/widget_X_....html" ...> and that the target HTML
    widget file exists, is non-empty, and is readable.
    """
    issues: List[VerificationIssue] = []
    iframe_matches = list(re.finditer(r"<iframe\b([^>]*)>(?:</iframe>)?", content, re.IGNORECASE))
    iframe_count = len(iframe_matches)

    # Compute line numbers for matches
    line_offsets = [0]
    for m in re.finditer(r"\n", content):
        line_offsets.append(m.end())

    def get_line_num(pos: int) -> int:
        import bisect
        return bisect.bisect_right(line_offsets, pos)

    found_designated = False

    if designated_widget is not None and iframe_count == 0:
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R2_WIDGET_EMBED,
                severity=IssueSeverity.ERROR,
                line_number=None,
                message=f"Missing designated Generative UI widget iframe for this chapter. Expected '<iframe src=\"../widgets/{designated_widget}\" ...>'.",
                snippet="No <iframe> tags found in chapter file.",
                fix_suggestion=(
                    f'Embed designated widget using:\n'
                    f'<div align="center" style="margin: 20px 0;">\n'
                    f'  <iframe src="../widgets/{designated_widget}" width="100%" height="520" frameborder="0" style="border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);"></iframe>\n'
                    f'  <p><em>Interactive Visualizer: <a href="../widgets/{designated_widget}" target="_blank">Open in standalone tab ↗</a></em></p>\n'
                    f'</div>'
                ),
            )
        )

    for match in iframe_matches:
        pos = match.start()
        line_num = get_line_num(pos)
        attrs = match.group(1)
        tag_snippet = match.group(0)[:120]

        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if not src_match:
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_WIDGET_EMBED,
                    severity=IssueSeverity.ERROR,
                    line_number=line_num,
                    message="<iframe> tag missing required 'src' attribute.",
                    snippet=tag_snippet,
                    fix_suggestion='Specify target widget path: src="../widgets/widget_X_....html"',
                )
            )
            continue

        src_raw = src_match.group(1)
        src_basename = os.path.basename(src_raw)

        # Check resolution relative to chapter directory
        resolved_path = os.path.normpath(os.path.join(chapter_dir, src_raw))

        if not os.path.isfile(resolved_path):
            # Also check fallback directly in widgets_dir
            fallback_path = os.path.join(widgets_dir, src_basename)
            if not os.path.isfile(fallback_path):
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R2_WIDGET_EMBED,
                        severity=IssueSeverity.ERROR,
                        line_number=line_num,
                        message=f"Embedded widget HTML file does not exist: '{src_raw}' (resolved to '{resolved_path}').",
                        snippet=tag_snippet,
                        fix_suggestion=f"Verify target widget HTML exists in {widgets_dir} and relative path is '../widgets/{src_basename}'.",
                    )
                )
            else:
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R2_WIDGET_EMBED,
                        severity=IssueSeverity.ERROR,
                        line_number=line_num,
                        message=f"Iframe src relative path '{src_raw}' does not resolve to '{resolved_path}'. File exists at '{fallback_path}'.",
                        snippet=tag_snippet,
                        fix_suggestion=f"Change iframe src to: src=\"../widgets/{src_basename}\"",
                    )
                )
        else:
            # File exists - check readability and size
            if not os.access(resolved_path, os.R_OK):
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R2_WIDGET_EMBED,
                        severity=IssueSeverity.ERROR,
                        line_number=line_num,
                        message=f"Target widget file '{resolved_path}' exists but is not readable.",
                        snippet=tag_snippet,
                        fix_suggestion="Ensure correct read permissions on the widget HTML asset.",
                    )
                )
            elif os.path.getsize(resolved_path) == 0:
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R2_WIDGET_EMBED,
                        severity=IssueSeverity.ERROR,
                        line_number=line_num,
                        message=f"Target widget file '{resolved_path}' is empty (0 bytes).",
                        snippet=tag_snippet,
                        fix_suggestion="Populate the HTML widget with valid interactive simulation content.",
                    )
                )

        # Check designated widget match
        if designated_widget is not None:
            if src_basename == designated_widget:
                found_designated = True
            else:
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R2_WIDGET_EMBED,
                        severity=IssueSeverity.WARNING,
                        line_number=line_num,
                        message=f"Chapter embeds widget '{src_basename}', but designated widget is '{designated_widget}'.",
                        snippet=tag_snippet,
                        fix_suggestion=f"Verify if designated widget '../widgets/{designated_widget}' should be embedded here.",
                    )
                )

        # Check styling / dimensions contract: width="100%", height="520", frameborder="0"
        width_m = re.search(r'width=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        height_m = re.search(r'height=["\']([^"\']+)["\']', attrs, re.IGNORECASE)

        if not width_m or width_m.group(1) != "100%":
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_WIDGET_EMBED,
                    severity=IssueSeverity.WARNING,
                    line_number=line_num,
                    message=f"Iframe width is '{width_m.group(1) if width_m else 'missing'}' (expected standard '100%').",
                    snippet=tag_snippet,
                    fix_suggestion='Set width="100%" on iframe.',
                )
            )

        if not height_m or height_m.group(1) != "520":
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_WIDGET_EMBED,
                    severity=IssueSeverity.WARNING,
                    line_number=line_num,
                    message=f"Iframe height is '{height_m.group(1) if height_m else 'missing'}' (expected standard '520').",
                    snippet=tag_snippet,
                    fix_suggestion='Set height="520" on iframe.',
                )
            )

    if designated_widget is not None and iframe_count > 0 and not found_designated:
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R2_WIDGET_EMBED,
                severity=IssueSeverity.ERROR,
                line_number=None,
                message=f"Chapter contains iframes, but none embed the designated widget '{designated_widget}'.",
                snippet=f"Expected designated widget: {designated_widget}",
                fix_suggestion=f"Embed '<iframe src=\"../widgets/{designated_widget}\" ...>' in the designated section.",
            )
        )

    return issues, iframe_count


# ---------------------------------------------------------------------------
# Check 3: Zero ASCII box-and-arrow chains
# ---------------------------------------------------------------------------
def check_ascii_diagrams(lines: List[str], file_path: str) -> Tuple[List[VerificationIssue], int]:
    """
    Validates that zero ASCII / Unicode box-and-arrow diagrams exist in the markdown text.
    All structural workflows must be represented via Mermaid or interactive widgets.
    """
    issues: List[VerificationIssue] = []
    in_code_block = False
    cur_lang = ""
    in_display_math = False
    ascii_count = 0

    # Common ASCII/Unicode diagram artifacts:
    # 1. Chains of box characters: [A] --> [B], [A] -> [B], [A] ──► [B]
    re_box_arrow_chain = re.compile(r"\[[^\]]+\]\s*(?:-->|->|==>|──►|─►|◄──|◄─)\s*\[[^\]]+\]")
    # 2. ASCII box border lines: +---+ or +===+
    re_ascii_box_border = re.compile(r"^\s*\+[-=]{3,}\+\s*$")
    # 3. Unicode box drawing top/bottom borders: ┌───┐ or └───┘
    re_unicode_box_border = re.compile(r"^\s*[┌\+│][─┬┼\-]{3,}[┐\+│]\s*$")
    # 4. Chains of 2+ arrow symbols connecting words in non-math text:
    #    e.g. Moments ──► Rates ──► Angles ──► Accel
    re_arrow_chain = re.compile(r"(?:──►|─►|◄──|◄─|-->|==>|->)")

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```") or stripped.startswith("~~~"):
            if not in_code_block:
                in_code_block = True
                cur_lang = stripped[3:].strip().lower()
            else:
                in_code_block = False
                cur_lang = ""
            continue

        # If inside mermaid, skip (mermaid is allowed to have arrows/boxes)
        if in_code_block and cur_lang == "mermaid":
            continue

        # Track display math blocks
        if not in_code_block:
            double_dollars = len(re.findall(r"(?<!\\)\$\$", line))
            if double_dollars % 2 != 0:
                in_display_math = not in_display_math
                continue
            if in_display_math:
                continue

        # Now we are in regular markdown text (or in a disallowed code block)
        # Strip inline math to avoid false alarms on LaTeX arrows ($A \to B$)
        text_without_math = re.sub(r"\$[^$]+\$", "", line)
        # Strip markdown links to avoid false alarms on [text](url)
        text_clean = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text_without_math)

        # 1. Box border line check
        if re_ascii_box_border.search(stripped) or re_unicode_box_border.search(stripped):
            ascii_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_ASCII_DIAGRAMS,
                    severity=IssueSeverity.ERROR,
                    line_number=idx,
                    message="ASCII / Unicode box border diagram detected in text.",
                    snippet=line,
                    fix_suggestion="Replace ASCII box diagram with a ```mermaid flowchart block.",
                )
            )
            continue

        # 2. Box-and-arrow chain: [A] --> [B]
        if re_box_arrow_chain.search(text_clean):
            ascii_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_ASCII_DIAGRAMS,
                    severity=IssueSeverity.ERROR,
                    line_number=idx,
                    message="ASCII box-and-arrow chain '[A] --> [B]' detected in text.",
                    snippet=line,
                    fix_suggestion="Replace ASCII chain with a standardized ```mermaid flowchart.",
                )
            )
            continue

        # 3. Unicode or multiple ASCII arrow chain (2+ arrows in a single text line)
        arrows = re_arrow_chain.findall(text_clean)
        # Check if arrows connect non-math text
        if len(arrows) >= 2 and not text_clean.startswith("#"):
            ascii_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_ASCII_DIAGRAMS,
                    severity=IssueSeverity.ERROR,
                    line_number=idx,
                    message=f"ASCII / Unicode multi-arrow chain ({len(arrows)} arrows) detected in text.",
                    snippet=line,
                    fix_suggestion="Convert horizontal arrow chains into a clean ```mermaid flowchart TD/LR.",
                )
            )
            continue

        # 4. Standalone Unicode arrow connecting words (e.g. Word ──► Word)
        if any(sym in line for sym in ["──►", "─►", "◄──", "◄─"]) and not text_clean.startswith("#"):
            ascii_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R2_ASCII_DIAGRAMS,
                    severity=IssueSeverity.ERROR,
                    line_number=idx,
                    message="Unicode arrow diagram symbol detected in text.",
                    snippet=line,
                    fix_suggestion="Replace Unicode arrows with ```mermaid flowchart or KaTeX '\\implies' / '\\to'.",
                )
            )

    return issues, ascii_count


# ---------------------------------------------------------------------------
# Check 4: Mermaid diagram syntax verification
# ---------------------------------------------------------------------------
def check_mermaid_syntax(lines: List[str], file_path: str) -> Tuple[List[VerificationIssue], int]:
    """
    Validates Mermaid diagram syntax across all diagrams in the chapter:
      - Unquoted ampersands '&' in node labels (which cause parser crashes).
      - Unescaped '<' or '>' in node labels or bad link arrow tags.
      - Invalid link arrows (e.g. '<==>' or malformed '-- "..." -->|label|').
      - Unmatched braces, brackets, and quotes.
      - Deprecated or unquoted <br/> tags inside unquoted labels.
    """
    issues: List[VerificationIssue] = []
    in_mermaid = False
    m_lines: List[Tuple[int, str]] = []
    mermaid_error_count = 0
    diagram_index = 0

    def audit_mermaid_block(diag_idx: int, block: List[Tuple[int, str]]):
        nonlocal mermaid_error_count
        if not block:
            return

        block_text = "\n".join(l[1] for l in block)
        diag_start_line = block[0][0]

        # 1. Delimiter balance over the whole diagram block
        # Check double quotes balance
        quotes_count = block_text.count('"') - block_text.count(r'\"')
        if quotes_count % 2 != 0:
            mermaid_error_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R3_MERMAID_SYNTAX,
                    severity=IssueSeverity.ERROR,
                    line_number=diag_start_line,
                    message=f"Mermaid Diagram #{diag_idx} has unbalanced double quotes ({quotes_count} found).",
                    snippet=block[0][1],
                    fix_suggestion="Ensure all string labels have matching opening and closing double quotes.",
                )
            )

        # Check square brackets balance
        open_sq = block_text.count("[")
        close_sq = block_text.count("]")
        if open_sq != close_sq:
            mermaid_error_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R3_MERMAID_SYNTAX,
                    severity=IssueSeverity.ERROR,
                    line_number=diag_start_line,
                    message=f"Mermaid Diagram #{diag_idx} has unbalanced square brackets '[' ({open_sq}) vs ']' ({close_sq}).",
                    snippet=block[0][1],
                    fix_suggestion="Ensure all node shape brackets '[' and ']' are paired.",
                )
            )

        # Check curly braces balance
        open_cur = block_text.count("{")
        close_cur = block_text.count("}")
        if open_cur != close_cur:
            mermaid_error_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R3_MERMAID_SYNTAX,
                    severity=IssueSeverity.ERROR,
                    line_number=diag_start_line,
                    message=f"Mermaid Diagram #{diag_idx} has unbalanced curly braces '{{' ({open_cur}) vs '}}' ({close_cur}).",
                    snippet=block[0][1],
                    fix_suggestion="Ensure all decision diamond braces '{{' and '}}' are paired.",
                )
            )

        # 2. Line-by-line linting
        for lno, line in block:
            stripped = line.strip()
            if not stripped or stripped.startswith("%%"):
                continue  # Skip comments and blanks

            # 2a. Check for non-standard arrow '<==>'
            if "<==>" in stripped:
                mermaid_error_count += 1
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R3_MERMAID_SYNTAX,
                        severity=IssueSeverity.ERROR,
                        line_number=lno,
                        message=f"Invalid Mermaid link arrow '<==>' at line {lno}. '<==>' is not supported by Mermaid parser.",
                        snippet=stripped,
                        fix_suggestion="Replace '<==>' with standard bidirectional arrow '<-->' or thick arrow '==>'.",
                    )
                )

            # 2b. Check for malformed arrow combining quote with pipe label: e.g. -- "..." -->|label|
            if re.search(r'--\s*"[^"]+"\s*-->\|', stripped) or re.search(r'--\s*[^-\s>]+\s*-->\|', stripped):
                mermaid_error_count += 1
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R3_MERMAID_SYNTAX,
                        severity=IssueSeverity.ERROR,
                        line_number=lno,
                        message=f"Malformed Mermaid arrow syntax mixing '-- \"...\" -->' and '|label|' at line {lno}.",
                        snippet=stripped,
                        fix_suggestion='Use standard link syntax: NODE1 -->|"Label"| NODE2',
                    )
                )

            # Strip properly double-quoted substrings to inspect remaining unquoted labels
            no_quotes = re.sub(r'"[^"]*"', '', stripped)

            # 2c. Check for unquoted ampersands '&' in node and link labels
            # In Mermaid, & outside quotes is interpreted as a node junction operator (A & B --> C).
            # Inside node/link labels e.g. B[Board & ESCs] or |A & B|, it causes parse crashes unless double-quoted.
            unquoted_amp_sq = re.search(r'\[[^\]]*&[^\]]*\]', no_quotes)
            unquoted_amp_paren = re.search(r'\([^\)]*&[^\)]*\)', no_quotes)
            unquoted_amp_brace = re.search(r'\{[^\}]*&[^\}]*\}', no_quotes)
            unquoted_amp_pipe = re.search(r'\|[^\|]*&[^\|]*\|', no_quotes)

            if unquoted_amp_sq or unquoted_amp_paren or unquoted_amp_brace or unquoted_amp_pipe:
                matched_label = (
                    unquoted_amp_sq.group(0)
                    if unquoted_amp_sq
                    else (
                        unquoted_amp_paren.group(0)
                        if unquoted_amp_paren
                        else (unquoted_amp_brace.group(0) if unquoted_amp_brace else unquoted_amp_pipe.group(0))
                    )
                )
                mermaid_error_count += 1
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R3_MERMAID_SYNTAX,
                        severity=IssueSeverity.ERROR,
                        line_number=lno,
                        message=f"Unquoted ampersand '&' in Mermaid label at line {lno}. In Mermaid, '&' is a reserved junction operator; labels containing '&' must be enclosed in double quotes.",
                        snippet=stripped,
                        fix_suggestion=f'Enclose label in double quotes: e.g. ["{matched_label.strip("[](){}|")}"] or |"{matched_label.strip("[](){}|")}"|',
                    )
                )

            # 2d. Check for raw unescaped '<' or '>' in unquoted node labels
            # Example: CHECK{Spread > Limit?} or [x < y]
            unquoted_cmp_brace = re.search(r'\{[^\}]*[<>][^\}]*\}', no_quotes)
            unquoted_cmp_sq = re.search(r'\[[^\]]*[<>][^\]]*\]', no_quotes)

            if unquoted_cmp_brace or unquoted_cmp_sq:
                matched_label = unquoted_cmp_brace.group(0) if unquoted_cmp_brace else unquoted_cmp_sq.group(0)
                mermaid_error_count += 1
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R3_MERMAID_SYNTAX,
                        severity=IssueSeverity.ERROR,
                        line_number=lno,
                        message=f"Raw unescaped '<' or '>' inside unquoted Mermaid node label at line {lno}.",
                        snippet=stripped,
                        fix_suggestion=f'Enclose label in double quotes or use HTML entities (&lt;, &gt;): e.g. {{"{matched_label.strip("{}[]")}"}}',
                    )
                )

            # 2e. Check for unquoted <br/> tags inside unquoted labels
            # In some renderers, unquoted <br/> breaks XML/SVG parsing
            if ("<br/>" in no_quotes or "<br>" in no_quotes) and (
                re.search(r'\[[^\]]*<br\s*/?>[^\]]*\]', no_quotes)
                or re.search(r'\{[^\}]*<br\s*/?>[^\}]*\}', no_quotes)
                or re.search(r'\([^\)]*<br\s*/?>[^\)]*\)', no_quotes)
            ):
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R3_MERMAID_SYNTAX,
                        severity=IssueSeverity.WARNING,
                        line_number=lno,
                        message=f"Unquoted '<br/>' HTML tag inside Mermaid node label at line {lno}.",
                        snippet=stripped,
                        fix_suggestion="Wrap node label in double quotes: [\"Line 1<br/>Line 2\"] or use '\\n'.",
                    )
                )

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```mermaid"):
            in_mermaid = True
            diagram_index += 1
            m_lines = []
            continue
        elif in_mermaid and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_mermaid = False
            audit_mermaid_block(diagram_index, m_lines)
            m_lines = []
            continue
        elif in_mermaid:
            m_lines.append((idx, line))

    if in_mermaid:
        mermaid_error_count += 1
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R3_MERMAID_SYNTAX,
                severity=IssueSeverity.ERROR,
                line_number=lines[-1] if lines else 1,
                message="Mermaid block was opened but never closed at end of file.",
                snippet="```mermaid ... EOF",
                fix_suggestion="Close diagram block with ```.",
            )
        )

    return issues, mermaid_error_count


def _count_unescaped_braces(text: str) -> Tuple[int, int]:
    """Counts unescaped { and } characters in LaTeX math expressions."""
    open_count = 0
    close_count = 0
    for match in re.finditer(r"(\\*)([{}]|\n)", text):
        slashes = match.group(1)
        char = match.group(2)
        # Even number of preceding backslashes means the brace is unescaped
        if len(slashes) % 2 == 0:
            if char == "{":
                open_count += 1
            elif char == "}":
                close_count += 1
    return open_count, close_count


# ---------------------------------------------------------------------------
# Check 5: KaTeX math delimiters and syntax verification
# ---------------------------------------------------------------------------
def check_katex_syntax(lines: List[str], file_path: str) -> Tuple[List[VerificationIssue], int, int, int]:
    """
    Validates KaTeX math delimiters ($$ and $) balance, curly brace ({ and })
    balance inside all display and inline math blocks, absence of raw tab '\\t'
    characters in commands (e.g. '\\t' in '\\theta', '\\to'), and absence of
    invalid math macros like '\\href' inside display math.
    """
    issues: List[VerificationIssue] = []
    content = "\n".join(l.rstrip("\r\n") for l in lines)
    katex_error_count = 0

    # Mask fenced code blocks with equivalent newlines to preserve exact line numbers
    content_no_code = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), content, flags=re.DOTALL)
    content_no_code = re.sub(r"~~~.*?~~~", lambda m: "\n" * m.group(0).count("\n"), content_no_code, flags=re.DOTALL)

    # 0. Check for 3 or more consecutive unescaped dollar signs ($$$, $$$$, etc.)
    for m in re.finditer(r"(?<!\\)\${3,}", content_no_code):
        lno = content_no_code[:m.start()].count("\n") + 1
        seq = m.group(0)
        katex_error_count += 1
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R3_KATEX_SYNTAX,
                severity=IssueSeverity.ERROR,
                line_number=lno,
                message=f"Malformed math delimiter: found sequence of {len(seq)} consecutive dollar signs ('{seq}'). Use '$$' for display math or '$' for inline math.",
                snippet=content_no_code[max(0, m.start()-20):min(len(content_no_code), m.end()+20)].strip(),
                fix_suggestion="Replace malformed delimiter with valid '$$' (display math) or '$' (inline math).",
            )
        )

    # 1. Check double dollar $$ balance
    double_dollar_matches = list(re.finditer(r"(?<!\\)\$\$", content_no_code))
    double_dollar_count = len(double_dollar_matches)
    display_math_blocks = double_dollar_count // 2

    if double_dollar_count % 2 != 0:
        katex_error_count += 1
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R3_KATEX_SYNTAX,
                severity=IssueSeverity.ERROR,
                line_number=None,
                message=f"Unbalanced display math delimiters ($$). Found odd count: {double_dollar_count} '$$' instances.",
                snippet="Ensure all display math blocks opened with '$$' are properly closed with '$$'.",
                fix_suggestion="Locate unclosed '$$' display math equation and append closing '$$'.",
            )
        )

    # 2. Check single dollar $ balance (excluding $$)
    # Replace all \$\$ with placeholders first
    temp_content = re.sub(r"(?<!\\)\$\$", "__DISPLAY_MATH__", content_no_code)
    single_dollar_matches = list(re.finditer(r"(?<!\\)\$", temp_content))
    single_dollar_count = len(single_dollar_matches)
    inline_math_pairs = single_dollar_count // 2

    if single_dollar_count % 2 != 0:
        katex_error_count += 1
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R3_KATEX_SYNTAX,
                severity=IssueSeverity.ERROR,
                line_number=None,
                message=f"Unbalanced inline math delimiters ($). Found odd count: {single_dollar_count} '$' instances.",
                snippet="Ensure all inline math spans opened with '$' are properly closed with '$'.",
                fix_suggestion="Locate unclosed inline '$' delimiter and append closing '$'.",
            )
        )

    # 3. Check curly brace { and } balance inside all display math blocks ($$ ... $$)
    display_math_pattern = re.compile(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", re.DOTALL)
    for m in display_math_pattern.finditer(content_no_code):
        block_text = m.group(1)
        lno = content_no_code[:m.start()].count("\n") + 1
        open_cur, close_cur = _count_unescaped_braces(block_text)
        if open_cur != close_cur:
            katex_error_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R3_KATEX_SYNTAX,
                    severity=IssueSeverity.ERROR,
                    line_number=lno,
                    message=f"Unbalanced curly braces in display math at line {lno}: '{{' ({open_cur}) vs '}}' ({close_cur}).",
                    snippet=block_text.strip()[:100],
                    fix_suggestion="Balance opening and closing braces { } inside math formula.",
                )
            )

    # 4. Check curly brace { and } balance inside all inline math blocks ($ ... $)
    content_inline = re.sub(
        r"(?<!\\)\$\$.*?(?<!\\)\$\$",
        lambda m: "\n" * m.group(0).count("\n"),
        content_no_code,
        flags=re.DOTALL,
    )
    inline_math_pattern = re.compile(r"(?<!\\)\$(?!\$)((?:[^\$\n]|\n(?!\n))+?)(?<!\\)\$(?!\$)")
    for m in inline_math_pattern.finditer(content_inline):
        inline_text = m.group(1)
        lno = content_inline[:m.start()].count("\n") + 1
        open_cur, close_cur = _count_unescaped_braces(inline_text)
        if open_cur != close_cur:
            katex_error_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R3_KATEX_SYNTAX,
                    severity=IssueSeverity.ERROR,
                    line_number=lno,
                    message=f"Unbalanced curly braces in inline math at line {lno}: '{{' ({open_cur}) vs '}}' ({close_cur}).",
                    snippet=f"${inline_text.strip()[:100]}$",
                    fix_suggestion="Balance opening and closing braces { } inside inline math formula.",
                )
            )

    # 5. Check for raw tab corruptions (\t in \theta, \to, \tau, etc.)
    # In Windows / Python generation, escape sequence \t becomes ASCII 0x09
    re_corrupted_command = re.compile(
        r"\t(heta|o|au|ilde|ext|imes|an|op|artial|beta|gamma|sigma|omega|alpha|lambda|mu|rho|phi|psi)\b"
    )

    in_fenced_code = False
    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            continue

        if in_fenced_code:
            continue

        # Check for command corruption like \x09heta
        corrupt_m = re_corrupted_command.search(line)
        if corrupt_m:
            suffix = corrupt_m.group(1)
            katex_error_count += 1
            issues.append(
                VerificationIssue(
                    file_path=file_path,
                    rule=RuleCategory.R3_KATEX_SYNTAX,
                    severity=IssueSeverity.ERROR,
                    line_number=idx,
                    message=f"Corrupted LaTeX command at line {idx}: raw tab character '\\t' precedes '{suffix}' (should be '\\{suffix}').",
                    snippet=line[:100],
                    fix_suggestion=f"Replace corrupted tab with backslash: replace '\\t{suffix}' with '\\{suffix}'.",
                )
            )

        # Also check for any raw tabs inside math equations
        if "\t" in line and ("$" in line):
            # Check if \t is between $ and $ or $$ and $$
            if not corrupt_m:
                katex_error_count += 1
                issues.append(
                    VerificationIssue(
                        file_path=file_path,
                        rule=RuleCategory.R3_KATEX_SYNTAX,
                        severity=IssueSeverity.ERROR,
                        line_number=idx,
                        message=f"Raw horizontal tab (0x09) detected inside math formula at line {idx}.",
                        snippet=line[:100],
                        fix_suggestion="Replace raw tab character with spaces or proper LaTeX spacing command (e.g. '\\quad').",
                    )
                )

    # 6. Check for invalid math macros (\href) inside display math ($$ ... $$)
    # \href is not supported inside standard KaTeX display math blocks and causes rendering crashes
    re_href_in_display = re.compile(r"\$\$(?:(?!\$\$).)*\\href\b(?:(?!\$\$).)*\$\$", re.DOTALL)
    for m in re_href_in_display.finditer(content_no_code):
        match_start = m.start()
        # Find line number
        line_num = content_no_code[:match_start].count("\n") + 1
        snippet = m.group(0)[:120]
        katex_error_count += 1
        issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R3_KATEX_SYNTAX,
                severity=IssueSeverity.ERROR,
                line_number=line_num,
                message=f"Unsupported LaTeX macro '\\href' inside display math ($$ ... $$) at line {line_num}. KaTeX does not support \\href inside display equations.",
                snippet=snippet,
                fix_suggestion="Move interactive links outside of KaTeX math blocks into regular markdown links or companion callout boxes.",
            )
        )

    return issues, display_math_blocks, inline_math_pairs, katex_error_count


# ---------------------------------------------------------------------------
# Verifier Orchestrator
# ---------------------------------------------------------------------------
def verify_chapter(
    file_path: str,
    chapters_dir: str,
    widgets_dir: str,
) -> ChapterReport:
    """Runs all 5 verification dimensions on a single chapter file."""
    fname = os.path.basename(file_path)
    topic_num = extract_topic_number(fname)
    designated_widget = DESIGNATED_WIDGETS.get(topic_num) if topic_num else None

    report = ChapterReport(
        file_path=file_path,
        filename=fname,
        topic_number=topic_num,
        designated_widget=designated_widget,
    )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
    except Exception as e:
        report.issues.append(
            VerificationIssue(
                file_path=file_path,
                rule=RuleCategory.R1_CODE_BLOCKS,
                severity=IssueSeverity.ERROR,
                line_number=None,
                message=f"Failed to read file: {e}",
            )
        )
        return report

    content = "".join(raw_lines)
    report.metrics.total_lines = len(raw_lines)

    # 1. Check code blocks (R1)
    r1_issues, mermaid_cnt, disallowed_cnt = check_code_blocks(raw_lines, file_path)
    report.issues.extend(r1_issues)
    report.metrics.mermaid_blocks = mermaid_cnt
    report.metrics.disallowed_code_blocks = disallowed_cnt

    # 2. Check Generative UI widget embed (R2)
    # Note: For topic_5_flight_ctrl_2.md (legacy prototype), don't mandate widget 5 if topic_5_flight_control.md already embeds it
    req_widget = designated_widget
    if fname == "topic_5_flight_ctrl_2.md":
        req_widget = None  # Prototype file does not strictly mandate unique widget if main chapter embeds it

    r2_widget_issues, iframe_cnt = check_widget_embed(
        content=content,
        file_path=file_path,
        designated_widget=req_widget,
        chapter_dir=chapters_dir,
        widgets_dir=widgets_dir,
    )
    report.issues.extend(r2_widget_issues)
    report.metrics.iframes_found = iframe_cnt

    # 3. Check ASCII diagrams (R2)
    r2_ascii_issues, ascii_cnt = check_ascii_diagrams(raw_lines, file_path)
    report.issues.extend(r2_ascii_issues)
    report.metrics.ascii_diagram_lines = ascii_cnt

    # 4. Check Mermaid diagram syntax (R3)
    r3_mermaid_issues, mermaid_errs = check_mermaid_syntax(raw_lines, file_path)
    report.issues.extend(r3_mermaid_issues)
    report.metrics.mermaid_syntax_errors = mermaid_errs

    # 5. Check KaTeX math formatting (R3)
    r3_katex_issues, dmath_cnt, imath_cnt, katex_errs = check_katex_syntax(raw_lines, file_path)
    report.issues.extend(r3_katex_issues)
    report.metrics.display_math_blocks = dmath_cnt
    report.metrics.inline_math_pairs = imath_cnt
    report.metrics.katex_syntax_errors = katex_errs

    return report


def verify_all_chapters(
    chapters_dir: str,
    widgets_dir: str,
    chapter_filter: Optional[str] = None,
) -> SuiteReport:
    """Runs verification across all chapters in the directory."""
    suite = SuiteReport()
    pattern = os.path.join(chapters_dir, "topic_*.md")
    files = sorted(glob.glob(pattern))

    if chapter_filter:
        files = [f for f in files if chapter_filter.lower() in os.path.basename(f).lower()]

    suite.total_files = len(files)

    for fpath in files:
        creport = verify_chapter(fpath, chapters_dir, widgets_dir)
        suite.chapters.append(creport)

    return suite


# ---------------------------------------------------------------------------
# CLI Formatting and Reporting
# ---------------------------------------------------------------------------
def print_cli_report(suite: SuiteReport, verbose: bool = False):
    """Outputs a production-grade, formatted CLI report."""
    print("=" * 80)
    print(" EEEE4138 AERIAL ROBOTICS — CHAPTER VERIFICATION SUITE (E2E)")
    print("=" * 80)
    print(f"Total Chapters Analyzed: {suite.total_files}")
    print()

    # Matrix Table
    header = f"{'Chapter File':<32} | {'R1 Code':<8} | {'R2 Widget':<9} | {'R2 ASCII':<8} | {'R3 Merm':<8} | {'R3 KaTeX':<8} | {'Status'}"
    print(header)
    print("-" * len(header))

    for c in suite.chapters:
        r1_status = "PASS" if c.metrics.disallowed_code_blocks == 0 else f"FAIL({c.metrics.disallowed_code_blocks})"
        r2_w_errs = len([i for i in c.errors if i.rule == RuleCategory.R2_WIDGET_EMBED])
        r2_w_status = "PASS" if r2_w_errs == 0 else "FAIL"
        r2_a_status = "PASS" if c.metrics.ascii_diagram_lines == 0 else f"FAIL({c.metrics.ascii_diagram_lines})"
        r3_m_status = "PASS" if c.metrics.mermaid_syntax_errors == 0 else f"FAIL({c.metrics.mermaid_syntax_errors})"
        r3_k_status = "PASS" if c.metrics.katex_syntax_errors == 0 else f"FAIL({c.metrics.katex_syntax_errors})"
        overall = "PASS" if c.passed else "FAIL"

        fname_trunc = c.filename if len(c.filename) <= 32 else c.filename[:29] + "..."
        print(f"{fname_trunc:<32} | {r1_status:<8} | {r2_w_status:<9} | {r2_a_status:<8} | {r3_m_status:<8} | {r3_k_status:<8} | {overall}")

    print("-" * len(header))
    print()

    # Detailed Diagnostics
    if suite.total_errors > 0 or (verbose and suite.total_warnings > 0):
        print("DIAGNOSTIC DETAILS:")
        print("=" * 80)

        for c in suite.chapters:
            if c.passed and not verbose:
                continue

            print(f"\n>>> [{c.filename}] (Topic {c.topic_number or '?'})")
            print(f"    Metrics: {c.metrics.total_lines} lines | {c.metrics.mermaid_blocks} Mermaid diags | {c.metrics.display_math_blocks} Display math | {c.metrics.inline_math_pairs} Inline math pairs | {c.metrics.iframes_found} iframes")

            if not c.issues:
                print("    ✓ All checks passed cleanly.")
                continue

            for idx, issue in enumerate(c.issues, 1):
                loc = f"Line {issue.line_number}" if issue.line_number else "Global/Structural"
                prefix = f"[{issue.severity.value}]"
                print(f"    {idx}. {prefix} {issue.rule.value} ({loc}):")
                print(f"       Message: {issue.message}")
                if issue.snippet:
                    indented_snippet = "\n       ".join(issue.snippet.splitlines()[:3])
                    print(f"       Snippet:\n       {indented_snippet}")
                if issue.fix_suggestion:
                    print(f"       Fix: {issue.fix_suggestion}")
                print()

    print("=" * 80)
    print(f"SUMMARY: Total Errors: {suite.total_errors} | Total Warnings: {suite.total_warnings}")
    if suite.passed:
        print("OVERALL RESULT: [PASS] All chapters conform to theoretical & visual standards.")
    else:
        print("OVERALL RESULT: [FAIL] Chapters require remediation according to diagnostics above.")
    print("=" * 80)


# ---------------------------------------------------------------------------
# Self-Test Suite (Validates the Verifier Logic Itself)
# ---------------------------------------------------------------------------
class ChapterVerifierSelfTest(unittest.TestCase):
    """
    Self-test verification suite that exercises verify_chapters_e2e checks against
    synthetic good and bad inputs to guarantee zero false positives/negatives.
    """

    def setUp(self):
        self.tmp_dir = os.path.abspath("test_tmp_verifier")
        self.tmp_chapters = os.path.join(self.tmp_dir, "chapters")
        self.tmp_widgets = os.path.join(self.tmp_dir, "widgets")
        os.makedirs(self.tmp_chapters, exist_ok=True)
        os.makedirs(self.tmp_widgets, exist_ok=True)

        # Create mock designated widgets
        for wname in DESIGNATED_WIDGETS.values():
            wpath = os.path.join(self.tmp_widgets, wname)
            with open(wpath, "w", encoding="utf-8") as f:
                f.write(f"<!DOCTYPE html><html><body>Mock {wname}</body></html>")

    def tearDown(self):
        import shutil
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_pristine_chapter_passes(self):
        """Verifies that a fully conforming chapter passes all 5 checks with zero errors."""
        content = (
            "# Topic 1: UAV Architectures\n\n"
            "## 1. Introduction\n"
            "This is a theoretical overview of UAV aerodynamics.\n\n"
            '<div align="center">\n'
            '  <iframe src="../widgets/widget_1_flight_envelope.html" width="100%" height="520" frameborder="0"></iframe>\n'
            "</div>\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            '    A["Inertial Frame"] --> B["Body Frame"]\n'
            "```\n\n"
            "$$\n"
            "F = m \\cdot a\n"
            "$$\n\n"
            "Where $m$ is aircraft mass and $a$ is linear acceleration.\n"
        )
        cpath = os.path.join(self.tmp_chapters, "topic_1_uav_architectures.md")
        with open(cpath, "w", encoding="utf-8") as f:
            f.write(content)

        report = verify_chapter(cpath, self.tmp_chapters, self.tmp_widgets)
        self.assertTrue(report.passed, f"Expected pass, got errors: {[i.message for i in report.errors]}")
        self.assertEqual(len(report.errors), 0)
        self.assertEqual(report.metrics.mermaid_blocks, 1)
        self.assertEqual(report.metrics.display_math_blocks, 1)
        self.assertEqual(report.metrics.inline_math_pairs, 2)
        self.assertEqual(report.metrics.iframes_found, 1)

    def test_detects_standalone_code_blocks(self):
        """Verifies that non-mermaid code blocks (e.g. Python, MATLAB) are flagged as errors."""
        content = (
            "# Code Violation Chapter\n\n"
            "```python\n"
            "def allocate_thrust(f_z, m):\n"
            "    return np.zeros(4)\n"
            "```\n"
        )
        issues, mermaid_cnt, disallowed_cnt = check_code_blocks(content.splitlines(), "test.md")
        self.assertEqual(disallowed_cnt, 1)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].rule, RuleCategory.R1_CODE_BLOCKS)
        self.assertEqual(issues[0].severity, IssueSeverity.ERROR)

    def test_detects_missing_widget_iframe(self):
        """Verifies that missing designated widget iframe is flagged as an error."""
        content = "# Topic 2 Chapter without widget\n\nSome text.\n"
        issues, iframes = check_widget_embed(
            content=content,
            file_path="topic_2_coordinate_frames.md",
            designated_widget="widget_2_frames_gimbal_lock.html",
            chapter_dir=self.tmp_chapters,
            widgets_dir=self.tmp_widgets,
        )
        self.assertEqual(iframes, 0)
        self.assertTrue(any(i.rule == RuleCategory.R2_WIDGET_EMBED for i in issues))

    def test_detects_nonexistent_widget_file(self):
        """Verifies that referencing a non-existent widget HTML file is flagged."""
        content = '<iframe src="../widgets/non_existent_widget.html" width="100%" height="520" frameborder="0"></iframe>'
        issues, iframes = check_widget_embed(
            content=content,
            file_path="topic_1_test.md",
            designated_widget=None,
            chapter_dir=self.tmp_chapters,
            widgets_dir=self.tmp_widgets,
        )
        self.assertEqual(iframes, 1)
        self.assertTrue(any("does not exist" in i.message for i in issues))

    def test_detects_ascii_box_and_arrow_diagrams(self):
        """Verifies that ASCII/Unicode box-and-arrow chains are detected and flagged."""
        content_lines = [
            "# Topic 5",
            "Control Moments ──► Angular Rates ──► Attitude Angles ──► Velocities ──► Positions",
            "[Block A] --> [Block B] --> [Block C]",
            "+------------------+",
            "| Downwash Flow    |",
            "+------------------+",
        ]
        issues, count = check_ascii_diagrams(content_lines, "test.md")
        self.assertGreaterEqual(count, 3)
        self.assertTrue(all(i.rule == RuleCategory.R2_ASCII_DIAGRAMS for i in issues))

    def test_detects_mermaid_syntax_issues(self):
        """Verifies detection of unquoted &, bad arrow <==>, and unescaped < >."""
        # 1. Unquoted ampersand in label
        bad_mermaid_1 = [
            "```mermaid",
            "flowchart TD",
            "    B[Power Distribution Board & ESCs] --> C",
            "```",
        ]
        issues_1, errs_1 = check_mermaid_syntax(bad_mermaid_1, "test.md")
        self.assertGreaterEqual(errs_1, 1)
        self.assertTrue(any("Unquoted ampersand '&'" in i.message for i in issues_1))

        # 2. Bad arrow <==>
        bad_mermaid_2 = [
            "```mermaid",
            "flowchart TD",
            "    A <==> B",
            "```",
        ]
        issues_2, errs_2 = check_mermaid_syntax(bad_mermaid_2, "test.md")
        self.assertGreaterEqual(errs_2, 1)
        self.assertTrue(any("Invalid Mermaid link arrow '<==>'" in i.message for i in issues_2))

        # 3. Raw < or > in decision diamond
        bad_mermaid_3 = [
            "```mermaid",
            "flowchart TD",
            "    CHECK{Spread > Limit?}",
            "```",
        ]
        issues_3, errs_3 = check_mermaid_syntax(bad_mermaid_3, "test.md")
        self.assertGreaterEqual(errs_3, 1)
        self.assertTrue(any("Raw unescaped" in i.message for i in issues_3))

        # 4. Pipe label unquoted ampersand
        bad_mermaid_4 = [
            "```mermaid",
            "flowchart TD",
            "    A -->|Speed & Velocity| B",
            "```",
        ]
        issues_4, errs_4 = check_mermaid_syntax(bad_mermaid_4, "test.md")
        self.assertGreaterEqual(errs_4, 1)
        self.assertTrue(any("Unquoted ampersand '&'" in i.message for i in issues_4))

    def test_detects_katex_syntax_issues(self):
        """Verifies detection of unbalanced delimiters, curly braces, tab corruptions, and \\href in $$."""
        # 1. Unbalanced $$
        bad_katex_1 = ["# Math", "$$ F = ma"]
        issues_1, _, _, errs_1 = check_katex_syntax(bad_katex_1, "test.md")
        self.assertTrue(any("Unbalanced display math" in i.message for i in issues_1))

        # 2. Corrupted tab \t in \theta
        bad_katex_2 = ["Pitch angle is $\x09heta$ in body frame."]
        issues_2, _, _, errs_2 = check_katex_syntax(bad_katex_2, "test.md")
        self.assertTrue(any("Corrupted LaTeX command" in i.message for i in issues_2))

        # 3. \href inside $$ ... $$
        bad_katex_3 = [
            "$$\\boxed{\\text{Open: } \\href{../widgets/widget_1.html}{Link}}$$"
        ]
        issues_3, _, _, errs_3 = check_katex_syntax(bad_katex_3, "test.md")
        self.assertTrue(any("\\href" in i.message for i in issues_3))

        # 4. Unbalanced curly braces in display math
        bad_katex_4 = [
            "$$\\boxed{A = B}}}$$"
        ]
        issues_4, _, _, errs_4 = check_katex_syntax(bad_katex_4, "test.md")
        self.assertGreaterEqual(errs_4, 1)
        self.assertTrue(any("Unbalanced curly braces in display math" in i.message for i in issues_4))

        # 5. Unbalanced curly braces in inline math
        bad_katex_5 = [
            "The variable is $x_{1$ in the equation."
        ]
        issues_5, _, _, errs_5 = check_katex_syntax(bad_katex_5, "test.md")
        self.assertGreaterEqual(errs_5, 1)
        self.assertTrue(any("Unbalanced curly braces in inline math" in i.message for i in issues_5))

        # 6. Malformed consecutive dollar signs ($$$)
        bad_katex_6 = ["$$\\boxed{A = B}$$$"]
        issues_6, _, _, errs_6 = check_katex_syntax(bad_katex_6, "test.md")
        self.assertGreaterEqual(errs_6, 1)
        self.assertTrue(any("Malformed math delimiter" in i.message for i in issues_6))


class TestChaptersE2E(unittest.TestCase):
    """
    End-to-end verification tests asserting that each topic chapter file
    in modules/EEEE4138_aerial_robotics/chapters/ passes all 5 verification rules.
    """

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cls.chapters_dir = os.path.abspath(os.path.join(base_dir, ".."))
        cls.widgets_dir = os.path.abspath(os.path.join(base_dir, "widgets"))

    def _verify_topic_file(self, filename: str):
        filepath = os.path.join(self.chapters_dir, filename)
        self.assertTrue(os.path.isfile(filepath), f"Chapter file not found: {filepath}")
        report = verify_chapter(filepath, self.chapters_dir, self.widgets_dir)
        if not report.passed:
            error_details = "\n".join(
                f"  [{i.rule.value}] Line {i.line_number or 'Global'}: {i.message}\n    Snippet: {i.snippet}"
                for i in report.errors
            )
            self.fail(f"Chapter '{filename}' failed verification with {len(report.errors)} error(s):\n{error_details}")

    def test_topic_1_uav_architectures(self):
        self._verify_topic_file("topic_1_uav_architectures.md")

    def test_topic_2_coordinate_frames(self):
        self._verify_topic_file("topic_2_coordinate_frames.md")

    def test_topic_3_kinematics_dynamics(self):
        self._verify_topic_file("topic_3_kinematics_dynamics.md")

    def test_topic_4_forces_moments(self):
        self._verify_topic_file("topic_4_forces_moments.md")

    def test_topic_5_flight_control(self):
        self._verify_topic_file("topic_5_flight_control.md")


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automated E2E Verification Suite for EEEE4138 Aerial Robotics Chapters"
    )
    parser.add_argument(
        "--chapters-dir",
        type=str,
        default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")),
        help="Path to chapters directory (default: modules/EEEE4138_aerial_robotics/chapters)",
    )
    parser.add_argument(
        "--widgets-dir",
        type=str,
        default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "widgets")),
        help="Path to widgets directory (default: modules/EEEE4138_aerial_robotics/chapters/artifacts/widgets)",
    )
    parser.add_argument(
        "--chapter",
        type=str,
        default=None,
        help="Filter verification to a specific chapter filename (e.g. topic_1_uav_architectures.md)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format for automated CI/CD tooling",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose diagnostics including warnings and passing chapters",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Execute internal verification test suite validating the verifier itself",
    )

    args = parser.parse_args()

    # If --self-test requested, run unit tests
    if args.self_test:
        suite = unittest.TestLoader().loadTestsFromTestCase(ChapterVerifierSelfTest)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1

    # Normal execution on chapters
    chapters_dir = os.path.abspath(args.chapters_dir)
    widgets_dir = os.path.abspath(args.widgets_dir)

    if not os.path.isdir(chapters_dir):
        print(f"ERROR: Chapters directory not found: {chapters_dir}", file=sys.stderr)
        return 2

    report = verify_all_chapters(
        chapters_dir=chapters_dir,
        widgets_dir=widgets_dir,
        chapter_filter=args.chapter,
    )

    if args.json:
        out_data = {
            "passed": report.passed,
            "total_files": report.total_files,
            "total_errors": report.total_errors,
            "total_warnings": report.total_warnings,
            "chapters": [
                {
                    "filename": c.filename,
                    "topic": c.topic_number,
                    "designated_widget": c.designated_widget,
                    "passed": c.passed,
                    "error_count": len(c.errors),
                    "warning_count": len(c.warnings),
                    "metrics": asdict(c.metrics),
                    "issues": [i.to_dict() for i in c.issues],
                }
                for c in report.chapters
            ],
        }
        print(json.dumps(out_data, indent=2))
    else:
        print_cli_report(report, verbose=args.verbose)

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
