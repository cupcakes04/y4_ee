import os
import re

for chap in ["topic_1_uav_architectures.md", "topic_2_coordinate_frames.md"]:
    chap_path = os.path.join("modules/EEEE4138_aerial_robotics/chapters", chap)
    with open(chap_path, encoding="utf-8") as f:
        content = f.read()
    
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    print(f"{chap}: Total markdown links = {len(links)}")
    for text, url in links:
        if url.startswith("http://") or url.startswith("https://") or url.startswith("#"):
            continue
        # Relative file link
        resolved = os.path.normpath(os.path.join(os.path.dirname(chap_path), url))
        if not os.path.exists(resolved):
            print(f"  [BROKEN LINK] in {chap}: '{url}' -> '{resolved}' does not exist!")
