import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
filepath = os.path.join(chapters_dir, "topic_3_kinematics_dynamics.md")

with open(filepath, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines, 1):
    if line.startswith("#"):
        print(f"L{idx:4d}: {line.strip()}")
