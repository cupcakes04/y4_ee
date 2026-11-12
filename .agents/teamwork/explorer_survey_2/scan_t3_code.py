import os
import re

filepath = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters\topic_3_kinematics_dynamics.md"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines, 1):
    if line.strip().startswith("```"):
        print(f"L{idx}: {line.strip()}")
    # Check for python or script keywords
    if any(k in line for k in ["def ", "class ", "import ", "numpy", "def attitude", "return "]):
        # check if it's not a mermaid or normal english word
        print(f"Keyword at L{idx}: {line.strip()[:100]}")
