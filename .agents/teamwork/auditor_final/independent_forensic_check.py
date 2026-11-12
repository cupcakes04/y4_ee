import os
import re
import sys
from pathlib import Path

CHAPTERS_DIR = Path("modules/EEEE4138_aerial_robotics/chapters")
WIDGETS_DIR = Path("modules/EEEE4138_aerial_robotics/widgets")

def count_unescaped_delimiters(text, open_char, close_char):
    opens = 0
    closes = 0
    for match in re.finditer(r"(\\*)([" + re.escape(open_char + close_char) + r"])", text):
        slashes = match.group(1)
        char = match.group(2)
        if len(slashes) % 2 == 0:
            if char == open_char:
                opens += 1
            elif char == close_char:
                closes += 1
    return opens, closes

def validate_environments(block, lno):
    errors = []
    stack = []
    # Find all \begin{env} and \end{env} in order
    pattern = re.compile(r"\\(begin|end)\{([a-zA-Z*]+)\}")
    for m in pattern.finditer(block):
        tag_type = m.group(1)
        env_name = m.group(2)
        if tag_type == "begin":
            stack.append(env_name)
        elif tag_type == "end":
            if not stack:
                errors.append(f"Line {lno}: Unexpected \\end{{{env_name}}} with no matching \\begin")
            else:
                top = stack.pop()
                if top != env_name:
                    errors.append(f"Line {lno}: Mismatched environment nesting: expected \\end{{{top}}}, found \\end{{{env_name}}}")
    if stack:
        errors.append(f"Line {lno}: Unclosed environments at end of block: {stack}")
    return errors

def audit_katex(content, filename):
    errors = []
    # Mask out code blocks
    content_no_code = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), content, flags=re.DOTALL)
    
    # 1. Delimiter count
    dd_matches = list(re.finditer(r"(?<!\\)\$\$", content_no_code))
    if len(dd_matches) % 2 != 0:
        errors.append(f"Odd count of $$ delimiters: {len(dd_matches)}")
        
    temp = re.sub(r"(?<!\\)\$\$", "__DISPLAY__", content_no_code)
    sd_matches = list(re.finditer(r"(?<!\\)\$", temp))
    if len(sd_matches) % 2 != 0:
        errors.append(f"Odd count of $ delimiters: {len(sd_matches)}")
        
    # 2. Display math blocks
    display_pattern = re.compile(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", re.DOTALL)
    for m in display_pattern.finditer(content_no_code):
        block = m.group(1)
        lno = content_no_code[:m.start()].count("\n") + 1
        
        # Check braces
        o_cur, c_cur = count_unescaped_delimiters(block, "{", "}")
        if o_cur != c_cur:
            errors.append(f"Line {lno}: Unbalanced braces in $$: '{'{o_cur} vs '}':{c_cur} | snippet: {block.strip()[:60]}")
            
        # Check brackets
        o_sq, c_sq = count_unescaped_delimiters(block, "[", "]")
        if o_sq != c_sq:
            errors.append(f"Line {lno}: Unbalanced brackets in $$: '[':{o_sq} vs ']':{c_sq} | snippet: {block.strip()[:60]}")
            
        # Check environments with stack
        env_errors = validate_environments(block, lno)
        errors.extend(env_errors)
            
        # Check corrupted tabs
        if re.search(r"\t(heta|o|au|ilde|ext|imes|an|op|artial|beta|gamma|sigma|omega|alpha|lambda|mu|rho|phi|psi)\b", block):
            errors.append(f"Line {lno}: Corrupted tab character preceding LaTeX command")

    # 3. Inline math blocks
    content_inline = re.sub(r"(?<!\\)\$\$.*?(?<!\\)\$\$", lambda m: "\n" * m.group(0).count("\n"), content_no_code, flags=re.DOTALL)
    inline_pattern = re.compile(r"(?<!\\)\$(?!\$)((?:[^\$\n]|\n(?!\n))+?)(?<!\\)\$(?!\$)")
    for m in inline_pattern.finditer(content_inline):
        span = m.group(1)
        lno = content_inline[:m.start()].count("\n") + 1
        o_cur, c_cur = count_unescaped_delimiters(span, "{", "}")
        if o_cur != c_cur:
            errors.append(f"Line {lno}: Unbalanced braces in $: '{'{o_cur} vs '}':{c_cur} | snippet: ${span.strip()[:60]}$")
            
    return errors

def audit_mermaid(content, filename):
    errors = []
    lines = content.splitlines()
    in_mermaid = False
    m_lines = []
    start_lno = 0
    
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            m_lines = []
            start_lno = idx
            continue
        elif in_mermaid and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_mermaid = False
            # Audit diagram block
            subgraphs = 0
            ends = 0
            for lno, m_raw in m_lines:
                m_str = m_raw.strip()
                if not m_str or m_str.startswith("%%"):
                    continue
                if re.match(r"^subgraph\b", m_str):
                    subgraphs += 1
                elif m_str == "end":
                    ends += 1
                
                # Check bad arrows
                if "<==>" in m_str:
                    errors.append(f"Line {lno}: Invalid arrow '<==>' in Mermaid")
                if re.search(r"--\s*\"[^\"]+\"\s*-->\|", m_str):
                    errors.append(f"Line {lno}: Malformed arrow mixing quote and pipe label")
                    
                # Check unquoted ampersands outside double quotes
                no_quotes = re.sub(r'"[^"]*"', '', m_str)
                if re.search(r'\[[^\]]*&[^\]]*\]', no_quotes) or \
                   re.search(r'\([^\)]*&[^\)]*\)', no_quotes) or \
                   re.search(r'\{[^\}]*&[^\}]*\}', no_quotes) or \
                   re.search(r'\|[^\|]*&[^\|]*\|', no_quotes):
                    errors.append(f"Line {lno}: Unquoted '&' in Mermaid label: {m_str}")
                    
                # Check raw comparison < or > inside unquoted node labels
                if re.search(r'\{[^\}]*[<>][^\}]*\}', no_quotes) or \
                   re.search(r'\[[^\]]*[<>][^\]]*\]', no_quotes):
                    errors.append(f"Line {lno}: Raw comparison '<' or '>' in unquoted label: {m_str}")

            if subgraphs != ends:
                errors.append(f"Line {start_lno}: Mismatched subgraphs ({subgraphs}) vs ends ({ends})")
            continue
        elif in_mermaid:
            m_lines.append((idx, line))
            
    if in_mermaid:
        errors.append(f"Line {start_lno}: Unclosed Mermaid block at EOF")
        
    return errors

def audit_code_blocks(content, filename):
    errors = []
    # Scan for disallowed code fences
    disallowed_langs = ["python", "py", "matlab", "m", "cpp", "c", "java", "sh", "bash"]
    for lang in disallowed_langs:
        matches = list(re.finditer(r"```" + lang + r"\b", content, re.IGNORECASE))
        if matches:
            for m in matches:
                lno = content[:m.start()].count("\n") + 1
                errors.append(f"Line {lno}: Disallowed code fence ```{lang}")
                
    # Search for specific forbidden script signatures
    if "attitude_priority_allocation" in content:
        errors.append("Forbidden implementation function 'attitude_priority_allocation' detected!")
        
    return errors

def audit_ascii_art(content, filename):
    errors = []
    lines = content.splitlines()
    in_fenced = False
    box_drawing_chars = set("┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬")
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue
        if any(c in box_drawing_chars for c in line):
            errors.append(f"Line {idx}: Unicode box-drawing character found in text")
        if re.search(r"\+[-=]{4,}\+", line):
            errors.append(f"Line {idx}: ASCII box border '+---+' found in text")
        if re.search(r"\[[A-Za-z0-9_\s]{2,15}\]\s*-->\s*\[[A-Za-z0-9_\s]{2,15}\]", line):
            errors.append(f"Line {idx}: ASCII box-and-arrow chain found in text")
    return errors

def audit_widget_embeds(content, filename):
    errors = []
    iframes = re.findall(r'<iframe\s+src="([^"]+)"', content)
    for src in iframes:
        # Resolve target path relative to chapters dir
        target_path = (CHAPTERS_DIR / src).resolve()
        if not target_path.exists():
            errors.append(f"Referenced iframe widget does not exist: {src} (resolved {target_path})")
        else:
            size = target_path.stat().st_size
            if size < 5000:
                errors.append(f"Widget file {target_path.name} is suspiciously small ({size} bytes)")
    return errors

def audit_relative_links(content, filename):
    errors = []
    # Markdown links [text](path)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, link in links:
        if link.startswith("http://") or link.startswith("https://") or link.startswith("#") or link.startswith("mailto:"):
            continue
        clean_link = link.split("#")[0]
        if not clean_link:
            continue
        target = (CHAPTERS_DIR / clean_link).resolve()
        if not target.exists():
            errors.append(f"Broken markdown link: {link} (resolved {target})")
    return errors

def main():
    chapters = sorted(CHAPTERS_DIR.glob("topic_*.md"))
    print(f"Auditing {len(chapters)} chapter files in {CHAPTERS_DIR}...")
    all_clean = True
    
    for chap in chapters:
        fname = chap.name
        content = chap.read_text(encoding="utf-8")
        
        k_errs = audit_katex(content, fname)
        m_errs = audit_mermaid(content, fname)
        c_errs = audit_code_blocks(content, fname)
        a_errs = audit_ascii_art(content, fname)
        w_errs = audit_widget_embeds(content, fname)
        l_errs = audit_relative_links(content, fname)
        
        total_errs = len(k_errs) + len(m_errs) + len(c_errs) + len(a_errs) + len(w_errs) + len(l_errs)
        if total_errs == 0:
            print(f"  [CLEAN] {fname:<35} | KaTeX: 0 | Mermaid: 0 | Code: 0 | ASCII: 0 | Widgets: OK | Links: OK")
        else:
            all_clean = False
            print(f"  [FAIL]  {fname:<35} | Total Issues: {total_errs}")
            for e in k_errs: print(f"    - KaTeX: {e}")
            for e in m_errs: print(f"    - Mermaid: {e}")
            for e in c_errs: print(f"    - Code: {e}")
            for e in a_errs: print(f"    - ASCII: {e}")
            for e in w_errs: print(f"    - Widgets: {e}")
            for e in l_errs: print(f"    - Links: {e}")

    print("=" * 80)
    if all_clean:
        print("INDEPENDENT FORENSIC VERDICT: ALL 7 CHAPTERS ARE 100% CLEAN")
        return 0
    else:
        print("INDEPENDENT FORENSIC VERDICT: INTEGRITY VIOLATION DETECTED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
