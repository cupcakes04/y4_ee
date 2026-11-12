import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def summarize(pdf_path):
    print(f"\n=======================================================")
    print(f"FILE: {pdf_path}")
    print(f"=======================================================")
    doc = fitz.open(pdf_path)
    for p in range(len(doc)):
        text = doc[p].get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        header = " | ".join(lines[:3]) if lines else "EMPTY"
        print(f"P{p+1}: {header[:120]}")

summarize('d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/drills/EEEE4138 Tutorial 4 Solutions I.pdf')
summarize('d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/drills/EEEE4138 Tutorial 5 Flight Control II Solutions.pdf')
