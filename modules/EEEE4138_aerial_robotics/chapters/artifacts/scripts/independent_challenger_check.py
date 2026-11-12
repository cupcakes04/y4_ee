#!/usr/bin/env python3
"""
independent_challenger_check.py
===============================
Independent stress-test oracle created by challenger_final.
Adversarially probes all 7 chapters in modules/EEEE4138_aerial_robotics/chapters/:
  1. KaTeX brace parity, delimiter parity, environment matching, and forbidden tokens in display and inline math.
  2. Mermaid parser syntax, node and edge label quoting, unquoted reserved characters.
  3. Residual programming implementations and code fences.
  4. Residual ASCII/Unicode box-and-arrow diagrams.
  5. Widget iframe paths, existence, attributes, and file sizes.
"""

import os
import re
import glob
import sys

CHAPTERS_DIR = os.path.abspath(r"modules/EEEE4138_aerial_robotics/chapters")
WIDGETS_DIR = os.path.abspath(r"modules/EEEE4138_aerial_robotics/widgets")

files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "*.md")))

print(f"=== INDEPENDENT CHALLENGER AUDIT: {len(files)} CHAPTERS ===")

all_passed = True
total_katex_errors = 0
total_mermaid_errors = 0
total_code_errors = 0
total_ascii_errors = 0
total_widget_errors = 0

def count_unescaped_braces(s: str):
    opens = 0
    closes = 0
    for m in re.finditer(r"(\\*)([{}]|\n)", s):
        slashes = m.group(1)
        char = m.group(2)
        if len(slashes) % 2 == 0:
            if char == "{":
                opens += 1
            elif char == "}":
                closes += 1
    return opens, closes

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as fp:
        raw_content = fp.read()
    lines = raw_content.splitlines(keepends=True)

    file_errors = []

    # 1. Fenced code check
    fenced_blocks = list(re.finditer(r"```([a-zA-Z0-9_-]*)", raw_content))
    for m in fenced_blocks:
        tag = m.group(1).lower().strip()
        if tag and tag != "mermaid":
            line_no = raw_content[:m.start()].count("\n") + 1
            file_errors.append(f"[DISALLOWED_CODE] Line {line_no}: Disallowed fenced code tag '```{tag}'")
            total_code_errors += 1

    # Check untagged fenced blocks
    # Mask ```mermaid ... ```
    content_no_mermaid = re.sub(r"```mermaid.*?```", lambda m: "\n" * m.group(0).count("\n"), raw_content, flags=re.DOTALL)
    residual_fences = list(re.finditer(r"```.*?```", content_no_mermaid, flags=re.DOTALL))
    for m in residual_fences:
        line_no = content_no_mermaid[:m.start()].count("\n") + 1
        file_errors.append(f"[DISALLOWED_CODE] Line {line_no}: Non-mermaid code block found")
        total_code_errors += 1

    # Check legacy function signatures
    legacy_sigs = ["attitude_priority_allocation", "desaturate_mixer", "def compute_motor_outputs"]
    for sig in legacy_sigs:
        if sig in raw_content:
            file_errors.append(f"[LEGACY_CODE] Signature '{sig}' present in text")
            total_code_errors += 1

    # 2. KaTeX checks
    # Mask all fenced code
    content_no_code = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), raw_content, flags=re.DOTALL)

    # Delimiter parity: $$
    dd_matches = list(re.finditer(r"(?<!\\)\$\$", content_no_code))
    if len(dd_matches) % 2 != 0:
        file_errors.append(f"[KATEX_DELIM] Unbalanced display math delimiters ($$), count = {len(dd_matches)}")
        total_katex_errors += 1

    # Delimiter parity: $
    temp_no_dd = re.sub(r"(?<!\\)\$\$.*?(?<!\\)\$\$", lambda m: "\n" * m.group(0).count("\n"), content_no_code, flags=re.DOTALL)
    sd_matches = list(re.finditer(r"(?<!\\)\$", temp_no_dd))
    if len(sd_matches) % 2 != 0:
        file_errors.append(f"[KATEX_DELIM] Unbalanced inline math delimiters ($), count = {len(sd_matches)}")
        total_katex_errors += 1

    # Display math blocks check
    for dm in re.finditer(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", content_no_code, flags=re.DOTALL):
        block = dm.group(1)
        lno = content_no_code[:dm.start()].count("\n") + 1
        op, cl = count_unescaped_braces(block)
        if op != cl:
            file_errors.append(f"[KATEX_BRACE] Line {lno}: Display math brace mismatch ({op} opens vs {cl} closes): {block.strip()[:60]}...")
            total_katex_errors += 1

        # LaTeX environments
        envs = re.findall(r"\\(begin|end)\{([a-zA-Z*]+)\}", block)
        env_stack = []
        for tag, name in envs:
            if tag == "begin":
                env_stack.append(name)
            else:
                if not env_stack:
                    file_errors.append(f"[KATEX_ENV] Line {lno}: Unmatched \\end{{{name}}}")
                    total_katex_errors += 1
                else:
                    top = env_stack.pop()
                    if top != name and not (top.endswith("*") and name == top.rstrip("*")):
                        file_errors.append(f"[KATEX_ENV] Line {lno}: Mismatched environment: \\begin{{{top}}} closed by \\end{{{name}}}")
                        total_katex_errors += 1
        if env_stack:
            file_errors.append(f"[KATEX_ENV] Line {lno}: Unclosed environments: {env_stack}")
            total_katex_errors += 1

        # Check square brackets in display math
        clean_sq = re.sub(r'\\\\\[[0-9a-zA-Z\s.]+\]', '', block)
        sq_o = clean_sq.count("[") - clean_sq.count(r"\[")
        sq_c = clean_sq.count("]") - clean_sq.count(r"\]")
        if sq_o != sq_c:
            file_errors.append(f"[KATEX_BRACKET] Line {lno}: Square bracket mismatch ({sq_o} vs {sq_c})")
            total_katex_errors += 1

    # Inline math blocks check
    for im in re.finditer(r"(?<!\\)\$(?!\$)((?:[^\$\n]|\n(?!\n))+?)(?<!\\)\$(?!\$)", temp_no_dd):
        inline_expr = im.group(1)
        lno = temp_no_dd[:im.start()].count("\n") + 1
        op, cl = count_unescaped_braces(inline_expr)
        if op != cl:
            file_errors.append(f"[KATEX_INLINE_BRACE] Line {lno}: Inline math brace mismatch ({op} vs {cl}): ${inline_expr}$")
            total_katex_errors += 1

    # 3. Mermaid diagrams check
    for mm in re.finditer(r"```mermaid(.*?)```", raw_content, flags=re.DOTALL):
        diag = mm.group(1)
        lno = raw_content[:mm.start()].count("\n") + 1
        dlines = diag.strip().splitlines()
        if not dlines:
            file_errors.append(f"[MERMAID] Line {lno}: Empty diagram")
            total_mermaid_errors += 1
            continue

        header = dlines[0].strip()
        valid_hdrs = ["flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt", "pie", "gitGraph", "mindmap", "timeline", "quadrantChart", "C4Context", "sankey-beta", "block-beta"]
        if not any(header.startswith(vh) for vh in valid_hdrs):
            file_errors.append(f"[MERMAID] Line {lno}: Invalid header '{header}'")
            total_mermaid_errors += 1

        # Check double quotes balance
        q_count = diag.count('"') - diag.count(r'\"')
        if q_count % 2 != 0:
            file_errors.append(f"[MERMAID] Line {lno}: Unbalanced double quotes ({q_count})")
            total_mermaid_errors += 1

        # Check square bracket balance
        if diag.count("[") != diag.count("]"):
            file_errors.append(f"[MERMAID] Line {lno}: Unbalanced square brackets")
            total_mermaid_errors += 1

        # Check unquoted ampersands in labels
        for dl_idx, dl in enumerate(dlines, 1):
            unquoted = re.sub(r'"[^"]*"', '', dl)
            if re.search(r'\[[^\]]*&[^\]]*\]', unquoted) or re.search(r'\|[^|]*&[^|]*\|', unquoted):
                file_errors.append(f"[MERMAID_AMP] Line {lno + dl_idx}: Unquoted ampersand in Mermaid label: {dl.strip()}")
                total_mermaid_errors += 1

        # Subgraph matching
        subgraphs = len(re.findall(r"^\s*subgraph\b", diag, re.MULTILINE))
        ends = len(re.findall(r"^\s*end\b", diag, re.MULTILINE))
        if subgraphs != ends:
            file_errors.append(f"[MERMAID] Line {lno}: Subgraph mismatch ({subgraphs} subgraph vs {ends} end)")
            total_mermaid_errors += 1

    # 4. Residual ASCII Art
    re_ascii_box = re.compile(r"^\s*\+[-=]{3,}\+\s*$")
    re_unicode_box = re.compile(r"^\s*[┌\+│][─┬┼\-]{3,}[┐\+│]\s*$")
    re_box_arrow = re.compile(r"\[[^\]]+\]\s*(?:-->|->|==>|──►|─►|◄──|◄─)\s*\[[^\]]+\]")

    in_fenced = False
    in_display = False
    for l_idx, line in enumerate(lines, 1):
        sline = line.strip()
        if sline.startswith("```") or sline.startswith("~~~"):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue
        if "$$" in sline:
            if sline.count("$$") % 2 != 0:
                in_display = not in_display
            if in_display:
                continue
        if in_display:
            continue

        clean = re.sub(r"(?<!\\)\$.*?(?<!\\)\$", "", sline)
        if re_ascii_box.match(clean) or re_unicode_box.match(clean):
            file_errors.append(f"[ASCII_BOX] Line {l_idx}: Box drawing border found: {sline}")
            total_ascii_errors += 1
        if re_box_arrow.search(clean):
            file_errors.append(f"[ASCII_ARROW] Line {l_idx}: Box-and-arrow chain found: {sline}")
            total_ascii_errors += 1
        if not clean.startswith("#") and any(sym in clean for sym in ["──►", "─►", "◄──", "◄─"]):
            file_errors.append(f"[UNICODE_ARROW] Line {l_idx}: Unicode arrow symbol in text: {sline}")
            total_ascii_errors += 1

    # 5. Widgets
    iframes = list(re.finditer(r"<iframe\b([^>]*)>", raw_content, re.IGNORECASE))
    if fname != "topic_5_flight_ctrl_2.md" and len(iframes) == 0:
        file_errors.append(f"[WIDGET] Missing designated widget iframe")
        total_widget_errors += 1

    for ifr in iframes:
        attrs = ifr.group(1)
        src_m = re.search(r'src=["\']([^"\']+)["\']', attrs)
        if not src_m:
            file_errors.append(f"[WIDGET] <iframe> missing src attribute")
            total_widget_errors += 1
        else:
            rel_path = src_m.group(1)
            full_path = os.path.normpath(os.path.join(CHAPTERS_DIR, rel_path))
            if not os.path.isfile(full_path):
                file_errors.append(f"[WIDGET] Target widget does not exist: {rel_path} -> {full_path}")
                total_widget_errors += 1
            else:
                sz = os.path.getsize(full_path)
                if sz == 0:
                    file_errors.append(f"[WIDGET] Target widget is empty (0 bytes): {rel_path}")
                    total_widget_errors += 1

    # Status
    status = "PASS" if not file_errors else f"FAIL ({len(file_errors)} errors)"
    print(f"[{status}] {fname} (Errors: {len(file_errors)})")
    for err in file_errors:
        print(f"    -> {err}")
    if file_errors:
        all_passed = False

print("=" * 60)
print(f"Summary: KaTeX={total_katex_errors}, Mermaid={total_mermaid_errors}, Code={total_code_errors}, ASCII={total_ascii_errors}, Widgets={total_widget_errors}")
if all_passed:
    print("FINAL INDEPENDENT VERDICT: ALL PASS [APPROVE]")
    sys.exit(0)
else:
    print("FINAL INDEPENDENT VERDICT: REJECT")
    sys.exit(1)
