import sys, os, glob, pypdf

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def search_pdf(path, keywords):
    print(f"\n==========================================")
    print(f"SEARCHING: {os.path.basename(path)}")
    print(f"==========================================")
    reader = pypdf.PdfReader(path)
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        found = [kw for kw in keywords if kw.lower() in text.lower()]
        if found:
            print(f"\n--- Page {idx + 1} (matched: {', '.join(found)}) ---")
            for line in text.splitlines():
                line = line.strip()
                if line:
                    print(f"  {line}")

if __name__ == '__main__':
    t2_p1 = 'modules/EEEE4138_aerial_robotics/raw/EEEE4138 - Topic 2 Reference Frames Part 1_v2.pdf'
    t2_p2 = 'modules/EEEE4138_aerial_robotics/raw/EEEE4138 - Topic 2 Reference Frames Part 2.pdf'
    t3 = 'modules/EEEE4138_aerial_robotics/raw/EEEE4138 Topic 3 Kinematics and Dynamics.pdf'
    t4 = 'modules/EEEE4138_aerial_robotics/raw/EEEE4138 Topic 4 Forces and Moments.pdf'

    search_pdf(t2_p1, ['R_v', 'yaw', 'pitch', 'roll', 'matrix'])
    search_pdf(t2_p2, ['quaternion', 'p, q, r', 'kinematics', 'gimbal'])
