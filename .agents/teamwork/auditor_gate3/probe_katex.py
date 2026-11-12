import sys
import os

# Add modules directory to path
sys.path.insert(0, os.path.abspath("."))

from modules.EEEE4138_aerial_robotics.verify_chapters_e2e import check_katex_syntax

test_lines = [
    r"$$\boxed{A = B}$$$",
    r"",
    r"$$\boxed{C = D}$$$",
]

issues, d, i, errs = check_katex_syntax(test_lines, "test.md")
print(f"Total issues: {len(issues)}")
print(f"Total errors: {errs}")
for idx, iss in enumerate(issues):
    print(f"Issue {idx+1}: [{iss.severity.value}] Line {iss.line_number}: {iss.message}")
