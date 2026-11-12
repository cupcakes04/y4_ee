filepath = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters\topic_4_forces_moments.md"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_code = False
for idx, line in enumerate(lines, 1):
    if line.strip().startswith("```"):
        in_code = not in_code
        continue
    if not in_code:
        if any(pat in line for pat in ["+---", "---|", "|---", "-->", "--->", "====>", "|   |", "+===", "┌", "└", "│"]):
            if line.strip().startswith("|") and line.strip().endswith("|"):
                continue
            print(f"L{idx}: {line.strip()}")
