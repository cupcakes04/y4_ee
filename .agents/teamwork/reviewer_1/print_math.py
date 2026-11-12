with open("modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md", encoding="utf-8") as f:
    content = f.read()

parts = content.split("$$")
dmath = parts[1::2]

for idx in [37, 53, 76, 77, 78, 79, 81, 83]:
    b = dmath[idx - 1]
    print(f"=== Math #{idx} ===")
    print(b)
    print("=" * 40)
