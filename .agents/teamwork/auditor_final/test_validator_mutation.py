import sys
import os

sys.path.insert(0, os.path.abspath("modules/EEEE4138_aerial_robotics"))
import verify_chapters_e2e as v

def run_tests():
    # Test 1: _count_unescaped_braces
    c1 = v._count_unescaped_braces(r"\{ a \} { b }")
    assert c1 == (1, 1), f"Failed on escaped braces: got {c1}"
    c2 = v._count_unescaped_braces(r"\\{ a \\}")
    assert c2 == (1, 1), f"Failed on double escaped braces: got {c2}"
    c3 = v._count_unescaped_braces(r"\boxed{a + b}}")
    assert c3 == (1, 2), f"Failed on unbalanced: got {c3}"
    print("PASS: _count_unescaped_braces")

    # Test 2: check_katex_syntax catches bad display math
    issues, d, i, errs = v.check_katex_syntax([r"$$\boxed{A = B}}]$$"], "dummy.md")
    assert errs >= 1, f"Expected error, got {errs}"
    assert any("Unbalanced curly braces in display math" in iss.message for iss in issues)
    print("PASS: check_katex_syntax detects display math brace imbalance")

    # Test 3: check_katex_syntax passes good display math
    issues, d, i, errs = v.check_katex_syntax([r"$$\boxed{A = B}$$"], "dummy.md")
    assert errs == 0, f"Expected 0 errors, got {errs}: {issues}"
    print("PASS: check_katex_syntax accepts balanced display math")

    # Test 4: check_katex_syntax catches inline math brace imbalance
    issues, d, i, errs = v.check_katex_syntax([r"The value $x_{1$ is invalid."], "dummy.md")
    assert errs >= 1, f"Expected error, got {errs}"
    assert any("Unbalanced curly braces in inline math" in iss.message for iss in issues)
    print("PASS: check_katex_syntax detects inline math brace imbalance")

    # Test 5: check_mermaid_syntax catches unquoted & in pipe label
    bad_m = [
        "```mermaid",
        "flowchart TD",
        "    A -->|Speed & Velocity| B",
        "```",
    ]
    issues, errs = v.check_mermaid_syntax(bad_m, "dummy.md")
    assert errs >= 1, f"Expected error, got {errs}"
    assert any("Unquoted ampersand" in iss.message for iss in issues)
    print("PASS: check_mermaid_syntax detects unquoted & in pipe label")

    # Test 6: check_mermaid_syntax passes quoted & in pipe label
    good_m = [
        "```mermaid",
        "flowchart TD",
        "    A -->|\"Speed & Velocity\"| B",
        "```",
    ]
    issues, errs = v.check_mermaid_syntax(good_m, "dummy.md")
    assert errs == 0, f"Expected 0 errors, got {errs}: {issues}"
    print("PASS: check_mermaid_syntax accepts quoted & in pipe label")

    print("\nALL 6 MUTATION TESTS PASSED CONFIRMING VALIDATOR SENSITIVITY!")

if __name__ == "__main__":
    run_tests()
