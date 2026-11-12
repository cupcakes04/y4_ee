import re
import os

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
files = [
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
    "topic_5_flight_ctrl_2.md"
]

for fname in files:
    fpath = os.path.join(chapters_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_fenced = False
    in_display_math = False
    issues = []

    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue

        # Count $$
        # If line contains $$, handle display math toggle
        # Remove $$ first to analyze single $
        line_clean = line
        while "$$" in line_clean:
            in_display_math = not in_display_math
            line_clean = line_clean.replace("$$", "", 1)
        
        if in_display_math:
            continue

        # Now count unescaped single $
        # Replace \$ with dummy
        temp = line_clean.replace(r"\$", "")
        single_dollars = temp.count("$")
        if single_dollars % 2 != 0:
            issues.append((idx, line.strip(), single_dollars))

    print(f"=== {fname}: {len(issues)} unclosed inline $ lines ===")
    for lno, ltext, count in issues:
        print(f"  L{lno} (count={count}): {ltext[:90]}")
