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
    blocks = []
    pos = 0
    while True:
        start = text.find("$$", pos)
        if start == -1:
            break
        end = text.find("$$", start + 2)
        if end == -1:
            blocks.append((start, len(text), text[start+2:], False))
            break
        blocks.append((start, end + 2, text[start+2:end], True))
        pos = end + 2
    return blocks

def validate_math_block(content):
    tokens = re.findall(r'(\\begin\{[a-zA-Z0-9*]+\}|\\end\{[a-zA-Z0-9*]+\})', content)
    stack = []
    for token in tokens:
        if token.startswith(r'\begin'):
            env = token[7:-1]
            stack.append(env)
        else:
            env = token[5:-1]
            if not stack:
                return False, f"Unexpected \\end{{{env}}} with empty stack"
            top = stack.pop()
            if top != env:
                return False, f"Mismatched \\end{{{env}}}, expected \\end{{{top}}}"
    if stack:
        return False, f"Unclosed environments: {stack}"
    return True, "OK"

for fname in files:
    fpath = os.path.join(chapters_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()

    blocks = find_math_blocks(text)
    invalid_count = 0
    for idx, (start_char, end_char, content, closed) in enumerate(blocks, 1):
        start_line = text[:start_char].count('\n') + 1
        end_line = text[:end_char].count('\n') + 1
        if not closed:
            print(f"[{fname}] L{start_line}: Unclosed $$ block!")
            invalid_count += 1
            continue
        valid, msg = validate_math_block(content)
        if not valid:
            print(f"[{fname}] L{start_line}-L{end_line}: {msg}")
            invalid_count += 1

    print(f"{fname}: {len(blocks)} blocks checked, {invalid_count} nesting errors.")
