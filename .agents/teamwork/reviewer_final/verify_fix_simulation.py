import re
import sys
sys.path.insert(0, "modules/EEEE4138_aerial_robotics")
from verify_chapters_e2e import _count_unescaped_braces, check_katex_syntax

with open("modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md", "r", encoding="utf-8") as f:
    text = f.read()

fixed = text.replace("$$$", "$$")

triple = list(re.finditer(r"(?<!\\)\${3,}", fixed))
print(f"Triple dollar signs in fixed text: {len(triple)}")

lines = fixed.splitlines(keepends=True)
issues, _, _, errs = check_katex_syntax(lines, "topic_2_coordinate_frames.md")
print(f"check_katex_syntax on fixed text: issues={len(issues)}, errs={errs}")
for iss in issues:
    print(f"  {iss.message}")

disp_blocks = re.findall(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", fixed, re.DOTALL)
imbalances = 0
for idx, b in enumerate(disp_blocks, 1):
    o, c = _count_unescaped_braces(b)
    if o != c:
        imbalances += 1
        print(f"Imbalance in block {idx}: {o} vs {c}")

print(f"Total display math blocks: {len(disp_blocks)}")
print(f"Total brace imbalances in fixed text: {imbalances}")
