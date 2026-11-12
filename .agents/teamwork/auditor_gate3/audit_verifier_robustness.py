import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.abspath("."))
from modules.EEEE4138_aerial_robotics.verify_chapters_e2e import verify_chapter

def test_violation(name: str, content: str, expected_rule: str, expected_msg_substring: str = ""):
    with tempfile.TemporaryDirectory() as tmp_dir:
        chapters_dir = os.path.join(tmp_dir, "chapters")
        widgets_dir = os.path.join(tmp_dir, "widgets")
        os.makedirs(chapters_dir)
        os.makedirs(widgets_dir)
        
        # Create standard mock widget
        with open(os.path.join(widgets_dir, "widget_1_flight_envelope.html"), "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html><html><body>Mock Widget</body></html>")
            
        cpath = os.path.join(chapters_dir, "topic_1_uav_architectures.md")
        with open(cpath, "w", encoding="utf-8") as f:
            f.write(content)
            
        report = verify_chapter(cpath, chapters_dir, widgets_dir)
        
        if report.passed:
            print(f"FAILED TO CATCH: {name} (verifier reported PASS!)")
            return False
            
        matched_issues = [i for i in report.errors if expected_rule in i.rule.value]
        if not matched_issues:
            print(f"WRONG RULE: {name} (expected {expected_rule}, got {[i.rule.value for i in report.errors]})")
            return False
            
        if expected_msg_substring and not any(expected_msg_substring.lower() in i.message.lower() for i in matched_issues):
            print(f"WRONG MSG: {name} (expected '{expected_msg_substring}' in message, got {[i.message for i in matched_issues]})")
            return False
            
        print(f"SUCCESSFULLY CAUGHT: {name} -> {matched_issues[0].message}")
        return True

base_valid_doc = """# Topic 1: UAV Architectures
## 1. Overview
Theoretical notes.
<iframe src="../widgets/widget_1_flight_envelope.html" width="100%" height="520" frameborder="0"></iframe>

```mermaid
flowchart TD
    A["Block A"] --> B["Block B"]
```

$$
F = m a
$$
"""

tests = [
    ("Triple dollar delimiter", base_valid_doc + "\n$$\\boxed{E = mc^2}$$$\n", "R3_KATEX_SYNTAX", "Malformed math delimiter"),
    ("Unbalanced display math $$", base_valid_doc + "\n$$ F = ma \n", "R3_KATEX_SYNTAX", "Unbalanced display math delimiters"),
    ("Unbalanced braces in math", base_valid_doc + "\n$$\\boxed{A = B}} $$\n", "R3_KATEX_SYNTAX", "Unbalanced curly braces"),
    ("Disallowed Python code block", base_valid_doc + "\n```python\nprint('hello')\n```\n", "R1_CODE_BLOCKS", "Disallowed programming code block"),
    ("Disallowed MATLAB code block", base_valid_doc + "\n```matlab\nA = [1, 2; 3, 4];\n```\n", "R1_CODE_BLOCKS", "Disallowed programming code block"),
    ("Missing widget iframe", "# Topic 1\n## Overview\nNo widgets here.", "R2_WIDGET_EMBED", "Missing required Generative UI widget"),
    ("Nonexistent widget iframe", '# Topic 1\n<iframe src="../widgets/non_existent.html" width="100%" height="520" frameborder="0"></iframe>', "R2_WIDGET_EMBED", "does not exist"),
    ("ASCII box diagram", base_valid_doc + "\n+------------------+\n| ASCII Box        |\n+------------------+\n", "R2_ASCII_DIAGRAMS", "ASCII/Unicode box or border"),
    ("Mermaid unquoted ampersand", base_valid_doc + "\n```mermaid\nflowchart TD\n    A -->|Unquoted & Ampersand| B\n```\n", "R3_MERMAID_SYNTAX", "Unquoted ampersand"),
]

all_passed = True
for name, content, rule, msg in tests:
    ok = test_violation(name, content, rule, msg)
    if not ok:
        all_passed = False

print("\nRobustness Result:", "ALL PASSED" if all_passed else "FAILURES DETECTED")
sys.exit(0 if all_passed else 1)
