import os
import glob
import re

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))

print(f"Total chapter files: {len(chapter_files)}")

for fpath in chapter_files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check Fenced code blocks
    lines = content.splitlines()
    in_block = False
    cur_lang = ""
    block_start = 0
    code_blocks = []
    for idx, line in enumerate(lines, 1):
        if line.startswith("```"):
            if not in_block:
                in_block = True
                cur_lang = line[3:].strip()
                block_start = idx
            else:
                in_block = False
                code_blocks.append((cur_lang, block_start, idx))

    non_mermaid = [b for b in code_blocks if b[0] != "mermaid"]
    if non_mermaid:
        print(f"\n[CODE BLOCKS] {fname} has non-mermaid code blocks:")
        for lang, start, end in non_mermaid:
            print(f"  Lines {start}-{end}: lang='{lang}'")

    # 2. Check Mermaid diagrams
    mermaid_blocks = re.findall(r"```mermaid\r?\n(.*?)\r?\n```", content, re.DOTALL)
    for m_idx, block in enumerate(mermaid_blocks, 1):
        for line_no, line in enumerate(block.splitlines(), 1):
            s = line.strip()
            # check unquoted node labels with special chars
            # Nodes with [...] or (...) or {...}
            # Look for unquoted labels
            patterns = [
                r'([A-Za-z0-9_]+)\[([^"\'].*?)\]',  # ID[unquoted]
                r'([A-Za-z0-9_]+)\(([^"\'].*?)\)',  # ID(unquoted)
            ]
            for pat in patterns:
                for match in re.finditer(pat, s):
                    node_id, label = match.groups()
                    if node_id in ("style", "subgraph", "direction", "classDef", "class"):
                        continue
                    # Check for dangerous characters in unquoted labels
                    if any(c in label for c in ["<br/>", "<br>", "(", ")", "[", "]", "{", "}", "\"", "'", ";", ":", "&", "%", "#", "*"]):
                        print(f"[MERMAID UNQUOTED] {fname} Diag #{m_idx} L{line_no}: Node '{node_id}' has special chars in unquoted label: {label[:40]}")

    # 3. Check KaTeX blocks: unclosed $ or $$, or invalid syntax
    # Count inline $ (not escaped \$)
    # Note: avoid matching inside code blocks
    content_no_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    dollar_matches = re.findall(r"(?<!\\)\$", content_no_code)
    # Check double dollars
    double_dollars = len(re.findall(r"(?<!\\)\$\$", content_no_code))
    single_dollars = len(dollar_matches) - 2 * double_dollars
    if single_dollars % 2 != 0:
        print(f"[KATEX WARNING] {fname}: Odd number of single $ ({single_dollars})")
    if double_dollars % 2 != 0:
        print(f"[KATEX WARNING] {fname}: Odd number of double $$ ({double_dollars})")

    # 4. Check for broken relative links / widgets
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    for text, link in links:
        if link.startswith("http"):
            continue
        # Strip anchor
        clean_link = link.split("#")[0]
        if clean_link:
            target_path = os.path.normpath(os.path.join(chapters_dir, clean_link))
            if not os.path.exists(target_path):
                print(f"[BROKEN LINK] {fname}: link '{link}' (target: {target_path}) does not exist!")

print("\nAudit complete.")
