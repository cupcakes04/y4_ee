import re

def check_katex_delimiters(content: str):
    issues = []
    # 1. 3+ dollar signs
    for m in re.finditer(r"(?<!\\)\${3,}", content):
        lno = content[:m.start()].count("\n") + 1
        seq = m.group(0)
        issues.append(f"Line {lno}: Malformed math delimiter '{seq}' ({len(seq)} consecutive dollar signs)")
    return issues

test_content = """
$$\\boxed{A = B}$$$

$$\\boxed{C = D}$$$
"""

print("Issues found in test:")
for iss in check_katex_delimiters(test_content):
    print(" ", iss)
