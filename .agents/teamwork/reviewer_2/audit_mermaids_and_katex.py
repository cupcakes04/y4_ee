import glob
import re
import sys

def audit_file(file_path):
    print(f"\n=======================================================")
    print(f"Auditing: {file_path}")
    print(f"=======================================================")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    in_mermaid = False
    mermaid_blocks = []
    curr_m = []
    start_m = 0
    
    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            curr_m = []
            start_m = idx
        elif in_mermaid and stripped.startswith("```"):
            in_mermaid = False
            mermaid_blocks.append((start_m, idx, curr_m))
        elif in_mermaid:
            curr_m.append((idx, line))

    print(f"Found {len(mermaid_blocks)} Mermaid diagram blocks.")
    for s, e, block in mermaid_blocks:
        first_line = block[0][1].strip() if block else "EMPTY"
        print(f"\n--- Mermaid Diagram at lines {s}-{e} [{first_line}] ---")
        full_text = "\n".join(b[1] for b in block)
        
        # Check delimiter balances
        quotes = full_text.count('"') - full_text.count(r'\"')
        open_sq, close_sq = full_text.count('['), full_text.count(']')
        open_cu, close_cu = full_text.count('{'), full_text.count('}')
        open_pa, close_pa = full_text.count('('), full_text.count(')')
        
        issues = []
        if quotes % 2 != 0:
            issues.append(f"Unbalanced double quotes: {quotes}")
        if open_sq != close_sq:
            issues.append(f"Unbalanced square brackets: {open_sq} vs {close_sq}")
        if open_cu != close_cu:
            issues.append(f"Unbalanced curly braces: {open_cu} vs {close_cu}")
        if open_pa != close_pa:
            issues.append(f"Unbalanced parentheses: {open_pa} vs {close_pa}")
            
        for lno, text in block:
            t = text.strip()
            if not t or t.startswith("%%"):
                continue
            if "<==>" in t:
                issues.append(f"Line {lno}: Invalid arrow '<==>'")
            if re.search(r'--\s*"[^"]+"\s*-->\|', t):
                issues.append(f"Line {lno}: Malformed mixed arrow syntax")
            
            # Check for unquoted ampersand & in node labels
            no_quotes = re.sub(r'"[^"]*"', '', t)
            if re.search(r'\[[^\]]*&[^\]]*\]', no_quotes) or re.search(r'\{[^\}]*&[^\}]*\}', no_quotes):
                issues.append(f"Line {lno}: Unquoted ampersand '&' in node label")
            if re.search(r'\[[^\]]*[<>][^\]]*\]', no_quotes) or re.search(r'\{[^\}]*[<>][^\}]*\}', no_quotes):
                issues.append(f"Line {lno}: Unescaped comparison '<' or '>' in node label")
            if "<br/>" in no_quotes and re.search(r'\[[^\]]*<br\s*/?>[^\]]*\]', no_quotes):
                issues.append(f"Line {lno}: Warning - unquoted <br/> in node label")
        
        if issues:
            for iss in issues:
                print(f"  [ERROR/WARN] {iss}")
        else:
            print("  [PASS] Clean Mermaid syntax.")

    # KaTeX delimiter check
    content = "".join(lines)
    content_no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    
    double_dollars = list(re.finditer(r"(?<!\\)\$\$", content_no_code))
    temp = re.sub(r"(?<!\\)\$\$", "__DM__", content_no_code)
    single_dollars = list(re.finditer(r"(?<!\\)\$", temp))
    
    print(f"\nKaTeX Delimiters:")
    print(f"  Display Math ($$): {len(double_dollars)} matches (Blocks: {len(double_dollars)//2})")
    print(f"  Inline Math ($): {len(single_dollars)} matches (Pairs: {len(single_dollars)//2})")
    
    if len(double_dollars) % 2 != 0:
        print(f"  [ERROR] Unbalanced $$ display math delimiters!")
    else:
        print(f"  [PASS] $$ delimiters are balanced.")
        
    if len(single_dollars) % 2 != 0:
        print(f"  [ERROR] Unbalanced $ inline math delimiters!")
    else:
        print(f"  [PASS] $ delimiters are balanced.")

    # Check for raw tabs
    tab_corruptions = []
    re_corrupted = re.compile(r"\t(heta|o|au|ilde|ext|imes|an|op|artial|beta|gamma|sigma|omega|alpha|lambda|mu|rho|phi|psi)\b")
    for idx, l in enumerate(lines, 1):
        if re_corrupted.search(l):
            tab_corruptions.append((idx, l.strip()))
    if tab_corruptions:
        print(f"  [ERROR] Found {len(tab_corruptions)} raw tab corruptions in LaTeX commands!")
        for idx, t in tab_corruptions[:5]:
            print(f"    Line {idx}: {t}")
    else:
        print(f"  [PASS] Zero tab corruptions in LaTeX commands.")

    # Check for \href inside $$ ... $$
    hrefs = list(re.finditer(r"\$\$(?:(?!\$\$).)*\\href\b(?:(?!\$\$).)*\$\$", content_no_code, re.DOTALL))
    if hrefs:
        print(f"  [ERROR] Found {len(hrefs)} unsupported \\href inside $$ blocks!")
    else:
        print(f"  [PASS] Zero \\href inside $$ blocks.")

chapters = [
    "modules/EEEE4138_aerial_robotics/chapters/topic_3_rigid_body_dynamics.md",
    "modules/EEEE4138_aerial_robotics/chapters/topic_3_kinematics_dynamics.md",
    "modules/EEEE4138_aerial_robotics/chapters/topic_4_forces_moments.md",
    "modules/EEEE4138_aerial_robotics/chapters/topic_5_flight_control.md",
    "modules/EEEE4138_aerial_robotics/chapters/topic_5_flight_ctrl_2.md",
]

for ch in chapters:
    audit_file(ch)
