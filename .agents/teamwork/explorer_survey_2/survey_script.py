import os
import re

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
files = [
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
    "topic_5_flight_ctrl_2.md"
]

for filename in files:
    filepath = os.path.join(chapters_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    print(f"=== {filename} ===")
    print(f"Total lines: {len(lines)}, Total bytes: {len(content.encode('utf-8'))}")

    # Check title / first 10 lines
    for i in range(min(10, len(lines))):
        if lines[i].startswith("#"):
            print(f"  Line {i+1}: {lines[i]}")

    # Find code blocks (```...)
    code_blocks = []
    in_code = False
    start_line = 0
    fence_lang = ""
    block_lines = []

    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                start_line = idx
                fence_lang = line.strip()[3:].strip()
                block_lines = []
            else:
                in_code = False
                code_blocks.append((start_line, idx, fence_lang, block_lines))
        elif in_code:
            block_lines.append(line)

    print(f"Total fenced code blocks: {len(code_blocks)}")
    for start, end, lang, blines in code_blocks:
        first_line = blines[0] if blines else ""
        print(f"  Lines {start}-{end} [{lang}]: {len(blines)} lines | Preview: {first_line[:60]}")

    print()
