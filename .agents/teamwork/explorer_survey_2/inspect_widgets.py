import os
import re

widgets_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\widgets"

for wname in ["widget_3_rigid_body_dynamics.html", "widget_4_rotor_mixer_allocation.html", "widget_5_cascaded_flight_control.html"]:
    wpath = os.path.join(widgets_dir, wname)
    with open(wpath, "r", encoding="utf-8") as f:
        html = f.read()
    
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "No title"
    
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    h1 = h1_match.group(1).strip() if h1_match else "No h1"

    print(f"=== {wname} ===")
    print(f"Title: {title}")
    print(f"H1: {h1}")
    print(f"Size: {len(html)} bytes")
    
    # Find buttons, sliders, canvases
    canvases = re.findall(r'<canvas[^>]*id=["\'](.*?)["\']', html)
    inputs = re.findall(r'<input[^>]*id=["\'](.*?)["\'][^>]*>', html)
    print(f"Canvases: {canvases}")
    print(f"Number of inputs/controls: {len(inputs)}")
    print()
