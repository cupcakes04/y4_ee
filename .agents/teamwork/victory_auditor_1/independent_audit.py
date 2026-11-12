import pathlib
import re

p = pathlib.Path('modules/EEEE4138_aerial_robotics/chapters')
for f in sorted(p.glob('*.md')):
    txt = f.read_text('utf-8')
    clean = re.sub(r'```.*?```', '', txt, flags=re.DOTALL)
    display_dollars = clean.count('$$')
    assert display_dollars % 2 == 0, f"{f.name}: Unbalanced display math ($$)"
    clean_no_disp = clean.replace('$$', '')
    inline_dollars = clean_no_disp.count('$')
    assert inline_dollars % 2 == 0, f"{f.name}: Unbalanced inline math ($)"
    print(f"{f.name}: Math delimiters balanced (display pairs: {display_dollars//2}, inline pairs: {inline_dollars//2})")

print("All KaTeX math delimiters balanced!")
