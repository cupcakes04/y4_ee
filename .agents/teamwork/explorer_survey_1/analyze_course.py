import fitz
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def dump_deck(pdf_path, max_p=None):
    doc = fitz.open(pdf_path)
    print(f"\n=======================================================")
    print(f"FILE: {os.path.basename(pdf_path)} ({len(doc)} pages)")
    print(f"=======================================================")
    num_pages = len(doc) if max_p is None else min(len(doc), max_p)
    for idx in range(num_pages):
        page = doc[idx]
        text = page.get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        # Filter out redundant header "EEEE4138 Aerial Robotics"
        clean_lines = [l for l in lines if l not in ["EEEE4138 Aerial Robotics", "EEEE4138: Aerial Robotics", "Aerial Robotics", "EEEE4138"]]
        title = clean_lines[0] if clean_lines else "EMPTY"
        sub = clean_lines[1] if len(clean_lines) > 1 else ""
        print(f"--- Page {idx+1}: {title} | {sub} ---")
        # print first few content lines
        for l in clean_lines[2:8]:
            print(f"    {l}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dump_deck(sys.argv[1])
