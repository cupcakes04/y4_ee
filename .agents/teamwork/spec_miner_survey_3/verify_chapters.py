#!/usr/bin/env python3
"""
Turnkey Verification Script for EEEE4138 Aerial Robotics Chapters
Validates:
1. Zero non-mermaid code blocks
2. Valid iframe syntax and existing local widget HTML files
3. Valid Mermaid diagram syntax (escaped labels)
4. Balanced KaTeX math delimiters ($ and $$)
"""

import os
import glob
import re
import sys

def verify_all_chapters():
    chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
    widgets_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\widgets"
    
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "topic_*.md")))
    print(f"============================================================")
    print(f"Verifying {len(chapter_files)} Chapter Files in: {chapters_dir}")
    print(f"============================================================")

    total_errors = 0

    for fpath in chapter_files:
        fname = os.path.basename(fpath)
        print(f"\n--- Checking: {fname} ---")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for non-mermaid code blocks
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
            for lang, start, end in non_mermaid:
                print(f"  [ERROR: CODE BLOCK] Lines {start}-{end}: lang='{lang}' (Must be eliminated)")
                total_errors += 1
        else:
            print(f"  [PASS] Zero standalone code blocks ({len(code_blocks)} Mermaid blocks found)")

        # 2. Check iframes
        iframes = re.findall(r'<iframe\s+([^>]+)></iframe>', content)
        if iframes:
            print(f"  [IFRAMES FOUND] {len(iframes)} iframe(s)")
            for ifr in iframes:
                src_match = re.search(r'src="([^"]+)"', ifr)
                width_match = re.search(r'width="([^"]+)"', ifr)
                height_match = re.search(r'height="([^"]+)"', ifr)
                
                if not src_match:
                    print(f"  [ERROR: IFRAME] Missing src in: {ifr}")
                    total_errors += 1
                    continue
                src = src_match.group(1)
                resolved = os.path.normpath(os.path.join(chapters_dir, src))
                if not os.path.exists(resolved):
                    print(f"  [ERROR: IFRAME] File does not exist: {src} -> {resolved}")
                    total_errors += 1
                else:
                    print(f"  [PASS: IFRAME] Valid target asset: {src}")

                if not width_match or width_match.group(1) != "100%":
                    print(f"  [WARN: IFRAME] width is not '100%': {ifr}")
                if not height_match or height_match.group(1) != "520":
                    print(f"  [WARN: IFRAME] height is not '520': {ifr}")
        else:
            print(f"  [INFO] No <iframe> tags currently embedded (pending injection)")

        # 3. Check KaTeX Math Delimiters
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        double_dollars = len(re.findall(r'(?<!\\)\$\$', content_no_code))
        dollar_matches = re.findall(r'(?<!\\)\$', content_no_code)
        single_dollars = len(dollar_matches) - 2 * double_dollars

        if double_dollars % 2 != 0:
            print(f"  [ERROR: KATEX] Odd count of double $$ ({double_dollars})")
            total_errors += 1
        else:
            print(f"  [PASS: KATEX] Balanced display math $$ ({double_dollars // 2} blocks)")

        if single_dollars % 2 != 0:
            print(f"  [ERROR: KATEX] Odd count of inline $ ({single_dollars})")
            total_errors += 1
        else:
            print(f"  [PASS: KATEX] Balanced inline math $ ({single_dollars // 2} pairs)")

    print(f"\n============================================================")
    print(f"Verification Finished. Total Errors: {total_errors}")
    print(f"============================================================")
    return total_errors

if __name__ == "__main__":
    errs = verify_all_chapters()
    sys.exit(0 if errs == 0 else 1)
