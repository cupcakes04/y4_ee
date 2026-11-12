import glob
import os
import re

chapters = sorted(glob.glob("modules/EEEE4138_aerial_robotics/chapters/topic_*.md"))

for c in chapters:
    fname = os.path.basename(c)
    with open(c, encoding="utf-8") as f:
        content = f.read()

    parts = content.split("$$")
    dollar_count = len(parts) - 1
    dmath = parts[1::2]
    
    unbalanced = []
    for idx, b in enumerate(dmath, 1):
        clean = re.sub(r"\\[{}]", "", b)
        ob = clean.count("{")
        cb = clean.count("}")
        if ob != cb:
            unbalanced.append((idx, ob, cb, b.strip()[:60]))
            
    print(f"{fname}: {len(dmath)} display blocks, {len(unbalanced)} unbalanced")
    for u in unbalanced:
        print(f"   Block #{u[0]}: {u[1]} open vs {u[2]} close | snippet: {u[3]}")
