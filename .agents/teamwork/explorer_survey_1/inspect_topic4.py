import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/raw/EEEE4138 Topic 4 Forces and Moments.pdf')
for p in range(21, 26):
    print(f'=== PAGE {p+1} ===')
    print(doc[p].get_text())

print('\n=== TUTORIAL 3 ===')
t3 = fitz.open('d:/gdrive/study_notes/degree/y4/modules/EEEE4138_aerial_robotics/drills/EEEE4138 Tutorial 3 Solutions.pdf')
for p in range(len(t3)):
    text = t3[p].get_text()
    print(f'--- T3 Page {p+1} ---')
    print(text[:400])
