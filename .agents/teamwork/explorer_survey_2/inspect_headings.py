import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
files = [
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
    "topic_5_flight_ctrl_2.md"
]

for filename in files:
    filepath = os.path.join(chapters_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    lines = content.splitlines()

    print(f"==================================================")
    print(f"FILE: {filename}")
    print(f"Total lines: {len(lines)}")
    print(f"==================================================")
    
    # Print all headers (#, ##, ###)
    for idx, line in enumerate(lines, 1):
        if line.startswith("#"):
            print(f"L{idx:4d}: {line}")
    print()
