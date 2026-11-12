filepath = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters\topic_3_kinematics_dynamics.md"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

paras = text.split("\n\n")
print(f"Total paragraphs/blocks: {len(paras)}")
for idx, p in enumerate(paras, 1):
    lines = p.strip().splitlines()
    words = sum(len(l.split()) for l in lines)
    if words > 100 and not p.strip().startswith("```") and not p.strip().startswith("$$") and not p.strip().startswith("|"):
        start_line = text[:text.find(p)].count('\n') + 1
        print(f"Para {idx} (L{start_line}, {len(lines)} lines, {words} words):")
        print(f"  {lines[0][:80]}...")
