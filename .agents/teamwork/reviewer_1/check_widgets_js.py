import re
import subprocess

for w in ["widget_1_flight_envelope.html", "widget_2_frames_gimbal_lock.html"]:
    wpath = f"modules/EEEE4138_aerial_robotics/widgets/{w}"
    with open(wpath, encoding="utf-8") as f:
        html = f.read()

    scripts = re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>", html, re.DOTALL)
    print(f"{w}: Found {len(scripts)} inline script(s)")
    for idx, s in enumerate(scripts, 1):
        # We can check JS syntax using node --check
        res = subprocess.run(["node", "--check", "-"], input=s, text=True, encoding="utf-8", capture_output=True)
        if res.returncode == 0:
            print(f"  Script #{idx} ({len(s.splitlines())} lines): Syntax OK")
        else:
            print(f"  Script #{idx} Syntax ERROR:\n{res.stderr}")
