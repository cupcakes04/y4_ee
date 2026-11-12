import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
files = [
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
    "topic_5_flight_ctrl_2.md"
]

report = []

def log(msg=""):
    report.append(msg)

for fname in files:
    fpath = os.path.join(chapters_dir, fname)
    if not os.path.exists(fpath):
        log(f"FILE NOT FOUND: {fname}")
        continue
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.splitlines()

    log("="*70)
    log(f"AUDIT FOR: {fname} (Total Lines: {len(lines)}, Bytes: {len(text.encode('utf-8'))})")
    log("="*70)

    # 1. Code blocks / implementation blocks
    log("\n--- 1. FENCED CODE BLOCKS ---")
    in_code = False
    start_line = 0
    lang = ""
    block_lines = []
    fenced_blocks = []

    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                start_line = idx
                lang = line.strip()[3:].strip()
                block_lines = []
            else:
                in_code = False
                fenced_blocks.append((start_line, idx, lang, block_lines))
        elif in_code:
            block_lines.append(line)

    for start, end, blang, blines in fenced_blocks:
        log(f"Block L{start}-L{end} [lang='{blang}'] ({len(blines)} lines)")
        if blang.lower() not in ["mermaid", ""]:
            log(f"  >>> CODE IMPLEMENTATION FOUND! lang={blang}")
            log("  Preview:")
            for pline in blines[:10]:
                log(f"    {pline}")
            if len(blines) > 10:
                log(f"    ... [{len(blines)-10} more lines]")

    # Check for non-fenced or raw code blocks or pseudo-code
    # 2. ASCII Art / Box-and-arrow diagrams
    log("\n--- 2. POTENTIAL ASCII ART / BOX-AND-ARROW DIAGRAMS ---")
    # Patterns like +---+, |    |, ---->, ====>, etc.
    ascii_candidates = []
    consecutive_box_lines = []
    
    for idx, line in enumerate(lines, 1):
        # Check if line looks like ascii art
        is_box = bool(re.search(r'(\+[-=+]+\+|\|[\s\w\d\-_\+\*\/]{4,}\||\+[-]{3,}|[-]{3,}\+|[-=]{2,}>|<[-=]{2,}|┌|┐|└|┘|├|┤|│|─)', line))
        # Ignore markdown tables
        if line.strip().startswith("|") and line.strip().endswith("|"):
            # Check if it's a markdown table separator like |---|---|
            if re.match(r'^\|[\s:-]+(?:\|[\s:-]+)+\|$', line.strip()):
                continue
            # Markdown table line
            parts = line.strip().split("|")
            if len(parts) >= 3 and not any(c in line for c in ['┌', '┐', '└', '┘', '+---', '-->']):
                # likely regular markdown table
                continue

        if is_box:
            consecutive_box_lines.append((idx, line))
        else:
            if len(consecutive_box_lines) >= 3:
                ascii_candidates.append(list(consecutive_box_lines))
            consecutive_box_lines = []
    if len(consecutive_box_lines) >= 3:
        ascii_candidates.append(list(consecutive_box_lines))

    if ascii_candidates:
        for group in ascii_candidates:
            start_l = group[0][0]
            end_l = group[-1][0]
            log(f"Potential ASCII diagram at L{start_l}-L{end_l}:")
            for l_num, l_text in group[:15]:
                log(f"  L{l_num:4d}: {l_text}")
            if len(group) > 15:
                log(f"  ... [{len(group)-15} more lines]")
    else:
        log("No multi-line ASCII art blocks detected via heuristic.")

    # 3. Mermaid Diagrams Audit
    log("\n--- 3. MERMAID DIAGRAMS AUDIT ---")
    mermaid_blocks = [b for b in fenced_blocks if b[2].lower() == "mermaid"]
    log(f"Found {len(mermaid_blocks)} Mermaid blocks.")
    for start, end, _, blines in mermaid_blocks:
        log(f"Mermaid Block L{start}-L{end} ({len(blines)} lines):")
        # Check for known mermaid issues:
        # 1. <br/> or <br> inside labels
        # 2. unescaped quotes or parentheses inside square brackets without quotes: e.g. A[Something (here)]
        # 3. unescaped characters like &, #, etc.
        # 4. empty lines or bad syntax
        for line_offset, mline in enumerate(blines, 1):
            curr_lineno = start + line_offset
            if "<br/>" in mline or "<br>" in mline or "<br />" in mline:
                log(f"  [WARN L{curr_lineno}] Contains <br> tag: {mline.strip()}")
            if re.search(r'\[[^"\]]*[\(\)][^"\]]*\]', mline):
                log(f"  [WARN L{curr_lineno}] Unquoted parentheses inside label brackets: {mline.strip()}")
            if re.search(r'\[[^"\]]*[;{}][^"\]]*\]', mline):
                log(f"  [WARN L{curr_lineno}] Special chars (;{{}}) inside label: {mline.strip()}")

    # 4. KaTeX Math Blocks Audit
    log("\n--- 4. KATEX MATH BLOCKS AUDIT ---")
    # Check for $$ ... $$ blocks and $ ... $ inline math
    # Look for unescaped _, \, unclosed $$, or syntax issues
    dollar_blocks = []
    in_math_block = False
    math_start = 0
    math_lines = []
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("$$"):
            if not in_math_block:
                in_math_block = True
                math_start = idx
                math_lines = [line]
                # Check if closed on same line (e.g. $$ expr $$)
                if stripped.endswith("$$") and len(stripped) > 2:
                    in_math_block = False
                    dollar_blocks.append((math_start, idx, math_lines))
            else:
                in_math_block = False
                math_lines.append(line)
                dollar_blocks.append((math_start, idx, math_lines))
        elif in_math_block:
            math_lines.append(line)

    if in_math_block:
        log(f"  [CRITICAL] Unclosed $$ math block starting at line {math_start}!")

    log(f"Total multi-line / standalone $$ math blocks: {len(dollar_blocks)}")
    # Audit math blocks for common KaTeX breakage:
    # \begin{align} without proper syntax, \\ at end, unicode characters inside math, unescaped percent %
    for mstart, mend, mblines in dollar_blocks:
        mcontent = "\n".join(mblines)
        # Check for unescaped % (comment in LaTeX)
        if "%" in mcontent and "\\%" not in mcontent:
            log(f"  [WARN Math L{mstart}-L{mend}] Contains unescaped % (LaTeX comment): {mcontent[:100]}")
        # Check for align vs aligned (KaTeX requires aligned or align* depending on renderer)
        if "\\begin{align}" in mcontent and "\\begin{aligned}" not in mcontent:
            log(f"  [NOTICE Math L{mstart}-L{mend}] Uses \\begin{{align}} (in KaTeX, \\begin{{aligned}} inside $$ is safer): {mcontent[:80]}")
        # Check for broken commands
        if "\\text{" in mcontent and "}" not in mcontent:
            log(f"  [WARN Math L{mstart}-L{mend}] Unclosed \\text{{")

    # 5. Generative UI Widget Embeds
    log("\n--- 5. GENERATIVE UI WIDGET EMBEDS & REFERENCES ---")
    widget_refs = []
    for idx, line in enumerate(lines, 1):
        if "widget" in line.lower() or "iframe" in line.lower() or ".html" in line.lower():
            widget_refs.append((idx, line.strip()))
    log(f"Found {len(widget_refs)} lines referencing widgets/iframes:")
    for lno, ltext in widget_refs:
        log(f"  L{lno:4d}: {ltext}")

    # 6. Dense Text Walls
    log("\n--- 6. DENSE TEXT WALL ANALYSIS ---")
    # Identify paragraphs that are unusually long without headings, equations, or lists (> 200 words or > 10 lines of unbroken text)
    curr_para = []
    para_start = 0
    for idx, line in enumerate(lines, 1):
        if line.strip() == "" or line.startswith("#") or line.startswith("```") or line.startswith("$$") or line.startswith("|") or line.startswith("- ") or line.startswith("* "):
            if len(curr_para) >= 8:
                word_count = sum(len(p.split()) for p in curr_para)
                if word_count > 120:
                    log(f"  Dense paragraph at L{para_start}-L{idx-1} ({len(curr_para)} lines, ~{word_count} words):")
                    log(f"    Preview: {curr_para[0][:90]}...")
            curr_para = []
            para_start = idx + 1
        else:
            if not curr_para:
                para_start = idx
            curr_para.append(line)

    log("\n")

out_path = r"d:\gdrive\study_notes\degree\y4\.agents\teamwork\explorer_survey_2\raw_audit_report.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print(f"Audit completed. Output written to {out_path}")
