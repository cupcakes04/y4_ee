import os

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"

with open(os.path.join(chapters_dir, "topic_5_flight_control.md"), "r", encoding="utf-8", errors="replace") as f:
    t5_main = f.read()

with open(os.path.join(chapters_dir, "topic_5_flight_ctrl_2.md"), "r", encoding="utf-8", errors="replace") as f:
    t5_proto = f.read()

print(f"topic_5_flight_control.md length: {len(t5_main.splitlines())} lines")
print(f"topic_5_flight_ctrl_2.md length: {len(t5_proto.splitlines())} lines")

# Let's check if topic_5_flight_control.md covers everything in topic_5_flight_ctrl_2.md
proto_headings = [l.strip() for l in t5_proto.splitlines() if l.startswith("#")]
main_headings = [l.strip() for l in t5_main.splitlines() if l.startswith("#")]

print("\n--- PROTO HEADINGS ---")
for h in proto_headings[:15]:
    print(h)
print(f"... total {len(proto_headings)} headings in prototype")

print("\n--- MAIN HEADINGS ---")
for h in main_headings[:15]:
    print(h)
print(f"... total {len(main_headings)} headings in main file")
