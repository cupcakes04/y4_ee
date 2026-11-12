import re
import os

chapters_dir = r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters"
files = [
    "topic_3_kinematics_dynamics.md",
    "topic_4_forces_moments.md",
    "topic_5_flight_control.md",
    "topic_5_flight_ctrl_2.md"
]

def find_math_blocks(text):
    # Regex to find all $$ ... $$ blocks including newlines
    blocks = []
    # Find all occurrences of $$
    pos = 0
    while True:
        start = text.find("$$", pos)
        if start == -1:
            break
        end = text.find("$$", start + 2)
        if end == -1:
            # Unclosed $$
            blocks.append((start, len(text), text[start+2:], False))
            break
        blocks.append((start, end + 2, text[start+2:end], True))
        pos = end + 2
    return blocks

for fname in files:
    fpath = os.path.join(chapters_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()

    blocks = find_math_blocks(text)
    print(f"=== {fname} ===")
    print(f"Found {len(blocks)} $$ blocks.")
    
    for idx, (start_char, end_char, content, closed) in enumerate(blocks, 1):
        # find line numbers
        start_line = text[:start_char].count('\n') + 1
        end_line = text[:end_char].count('\n') + 1
        if not closed:
            print(f"  [ERROR L{start_line}] Unclosed $$ display math block!")
            continue
        
        # Check environment balance
        # Find \begin{...} and \end{...}
        begins = re.findall(r'\\begin\{([a-zA-Z0-9*]+)\}', content)
        ends = re.findall(r'\\end\{([a-zA-Z0-9*]+)\}', content)
        if begins != ends:
            print(f"  [ENV MISMATCH L{start_line}-L{end_line}]:")
            print(f"    \\begin: {begins}")
            print(f"    \\end:   {ends}")
            print(f"    Content preview: {content[:100]}...")

        # Check for unescaped %
        clean = content.replace(r'\%', '')
        if '%' in clean:
            print(f"  [WARN L{start_line}-L{end_line}] Unescaped % in display math: {clean[:80]}...")
