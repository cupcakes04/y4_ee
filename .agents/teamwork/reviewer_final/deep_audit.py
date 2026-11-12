import glob
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

chapters = sorted(glob.glob("modules/EEEE4138_aerial_robotics/chapters/*.md"))

for chap in chapters:
    with open(chap, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip fenced code
    text_clean = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
    text_clean = re.sub(r"~~~.*?~~~", lambda m: "\n" * m.group(0).count("\n"), text_clean, flags=re.DOTALL)

    # 1. Check for 3+ consecutive dollar signs
    triple = list(re.finditer(r"(?<!\\)\${3,}", text_clean))
    if triple:
        print(f"[{chap}] FOUND {len(triple)} instances of 3+ dollar signs:")
        for m in triple:
            lno = text_clean[:m.start()].count("\n") + 1
            print(f"  Line {lno}: {repr(text_clean[max(0, m.start()-25):m.end()+10])}")

    # 2. Check environments
    begins = re.findall(r"\\begin\{([a-zA-Z0-9*]+)\}", text_clean)
    ends = re.findall(r"\\end\{([a-zA-Z0-9*]+)\}", text_clean)
    if len(begins) != len(ends):
        print(f"[{chap}] Mismatched environment count: {len(begins)} begins vs {len(ends)} ends")
    else:
        for b, e in zip(begins, ends):
            # basic check
            pass

    # 3. Check \left vs \right
    disp_blocks = list(re.finditer(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", text_clean, flags=re.DOTALL))
    for idx, m in enumerate(disp_blocks, 1):
        b = m.group(1)
        lno = text_clean[:m.start()].count("\n") + 1
        left_cnt = len(re.findall(r"\\left\b", b))
        right_cnt = len(re.findall(r"\\right\b", b))
        if left_cnt != right_cnt:
            print(f"[{chap}] Line {lno} (disp {idx}): unbalanced \\left ({left_cnt}) vs \\right ({right_cnt})")

print("Deep audit scan complete.")
