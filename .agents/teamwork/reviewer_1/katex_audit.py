import re
import sys

def audit_katex(fpath):
    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    # Split by $$
    parts = content.split("$$")
    print(f"{fpath}: Total $$ count = {len(parts)-1} (balanced: {(len(parts)-1)%2==0})")
    
    # Check display blocks
    dmath_blocks = parts[1::2]
    for idx, block in enumerate(dmath_blocks, 1):
        clean = re.sub(r"\\[{}]", "", block)
        ob = clean.count("{")
        cb = clean.count("}")
        if ob != cb:
            print(f"  [ERROR] Display Math #{idx} unbalanced braces: {ob} open vs {cb} close")
            print(f"  Snippet: {block.strip()[:80]}")

    # Check for raw tabs
    lines = content.splitlines()
    for lno, line in enumerate(lines, 1):
        if "\t" in line:
            print(f"  [ERROR] Line {lno} contains raw tab (0x09): {repr(line[:50])}")

for f in [
    "modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md",
    "modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md",
]:
    audit_katex(f)
