import re
import os

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
files = [
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
    "topic_5_flight_ctrl_2.md"
]

def check_katex_in_file(fname):
    fpath = os.path.join(chapters_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()

    issues = []
    
    # 1. Check for unescaped characters in math blocks:
    # E.g. unescaped &, %, $, #, _, etc.
    # 2. Check for unbalanced environments: \begin{...} and \end{...}
    # 3. Check for invalid commands or truncated equations

    in_fenced = False
    in_math_block = False
    block_start = 0
    math_content = []

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue

        if stripped.startswith("$$"):
            if not in_math_block:
                in_math_block = True
                block_start = idx
                math_content = [line]
                if stripped.endswith("$$") and len(stripped) > 2:
                    in_math_block = False
                    # single line display math
                    full_eq = stripped[2:-2].strip()
                    check_eq(full_eq, block_start, idx, issues)
            else:
                in_math_block = False
                math_content.append(line)
                full_eq = "\n".join(math_content)
                check_eq(full_eq, block_start, idx, issues)
        elif in_math_block:
            math_content.append(line)
        else:
            # Inline math check: find $...$
            # Avoid escaped \$
            inlines = re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$', line)
            for inline_math in inlines:
                if inline_math.strip():
                    check_inline(inline_math, idx, issues)

    if in_math_block:
        issues.append((block_start, len(lines), "CRITICAL: Unclosed $$ block"))

    return issues

def check_eq(eq_str, start_l, end_l, issues):
    # Check environments
    begins = re.findall(r'\\begin\{([a-zA-Z0-9*]+)\}', eq_str)
    ends = re.findall(r'\\end\{([a-zA-Z0-9*]+)\}', eq_str)
    if begins != ends:
        issues.append((start_l, end_l, f"Mismatched environments: \\begin: {begins} vs \\end: {ends}"))

    # Check for empty superscript / subscript like ^ or _ followed immediately by space or end
    trailing_sub = re.findall(r'[\^_]\s', eq_str)
    if trailing_sub:
        issues.append((start_l, end_l, f"Trailing/isolated superscript or subscript: {trailing_sub}"))

    # Check for unescaped percent sign %
    clean = eq_str.replace(r'\%', '')
    if '%' in clean:
        issues.append((start_l, end_l, f"Unescaped % in display math (treats rest as comment): {clean}"))

    # Check for \\ followed immediately by \end without newline, or double backslash issues
    # Check for non-standard latex commands
    unsupported = ['\\label', '\\ref', '\\cite', '\\eqref']
    for cmd in unsupported:
        if cmd in eq_str:
            issues.append((start_l, end_l, f"Potentially unsupported KaTeX command {cmd}"))

def check_inline(eq_str, line_no, issues):
    begins = re.findall(r'\\begin\{([a-zA-Z0-9*]+)\}', eq_str)
    ends = re.findall(r'\\end\{([a-zA-Z0-9*]+)\}', eq_str)
    if begins != ends:
        issues.append((line_no, line_no, f"Inline mismatched environments: {begins} vs {ends}"))
    clean = eq_str.replace(r'\%', '')
    if '%' in clean:
        issues.append((line_no, line_no, f"Unescaped % in inline math"))

for fname in files:
    issues = check_katex_in_file(fname)
    print(f"=== {fname}: {len(issues)} KaTeX issues found ===")
    for s, e, desc in issues:
        print(f"  L{s}-L{e}: {desc}")
