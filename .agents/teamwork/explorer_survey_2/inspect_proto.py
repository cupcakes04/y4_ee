import os

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"

with open(os.path.join(chapters_dir, "topic_5_flight_ctrl_2.md"), "r", encoding="utf-8") as f:
    proto_text = f.read()

with open(os.path.join(chapters_dir, "topic_5_flight_control.md"), "r", encoding="utf-8") as f:
    main_text = f.read()

proto_lines = proto_text.splitlines()
main_lines = main_text.splitlines()

# Check what topics/sections are in proto
print(f"Prototype lines: {len(proto_lines)}")
for idx, line in enumerate(proto_lines, 1):
    if line.startswith("## ") or line.startswith("### "):
        print(f"Proto L{idx:4d}: {line}")
