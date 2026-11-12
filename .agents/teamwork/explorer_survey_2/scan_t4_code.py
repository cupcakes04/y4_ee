filepath = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters\topic_4_forces_moments.md"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if idx >= 570 and idx <= 634:
        continue # known python block
    if any(k in line for k in ["def ", "class ", "import ", "numpy", "return "]):
        print(f"L{idx}: {line.strip()[:100]}")
