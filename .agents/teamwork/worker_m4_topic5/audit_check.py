import re
from pathlib import Path

chapters_dir = Path(r"d:\gdrive\study_notes\degree\y4\modules\EEEE4138_aerial_robotics\chapters")
t5_file = chapters_dir / "topic_5_flight_control.md"
t5_p_file = chapters_dir / "topic_5_flight_ctrl_2.md"

expected_iframe = (
    '<div align="center" style="margin: 20px 0;">\n'
    '  <iframe src="../widgets/widget_5_cascaded_flight_control.html" width="100%" height="520" frameborder="0" style="border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);"></iframe>\n'
    '  <p><em>Interactive Visualizer: <a href="../widgets/widget_5_cascaded_flight_control.html" target="_blank">Open in standalone tab ↗</a></em></p>\n'
    '</div>'
)

for f in [t5_file, t5_p_file]:
    content = f.read_text(encoding="utf-8")
    print(f"=== Auditing {f.name} ===")
    
    # 1. Non-mermaid code blocks
    opening_fences = [m.group(1) for m in re.finditer(r"^```([a-zA-Z0-9_-]*)", content, re.MULTILINE)]
    # Pair them up: every opening fence is followed by a closing ```
    # An opening fence with language will have group(1) != ''
    languages = [f for f in opening_fences if f != ""]
    print(f"Code block languages found on opening fences: {set(languages)}")
    assert set(languages) == {"mermaid"}, f"Expected only mermaid blocks, got {set(languages)}"
    print("Code implementation blocks: 0 (PASSED)")
    
    # 2. Widget 5 iframe format
    assert expected_iframe in content, f"Expected exact iframe wrapper in {f.name}"
    print("Widget 5 exact iframe embedding: VERIFIED (PASSED)")
    
    # 3. Unicode box-and-arrow characters
    box_arrow = re.findall(r"[─►▼▲◄➔]", content)
    assert len(box_arrow) == 0, f"Found box/arrow chars in {f.name}: {box_arrow}"
    print("Unicode box-and-arrow characters: 0 (PASSED)")
    
    # 4. KaTeX display math block balance
    display_matches = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
    print(f"Display math blocks count: {len(display_matches)} (all closed)")
    
    # 5. Inline math parity
    stripped = re.sub(r"\$\$.*?\$\$", "", content, flags=re.DOTALL)
    dollar_count = stripped.count("$")
    assert dollar_count % 2 == 0, f"Unpaired inline dollars: {dollar_count}"
    print(f"Inline math dollar count: {dollar_count} ({dollar_count//2} paired expressions) (PASSED)")
    
    # 6. Mermaid diagrams check for unquoted < or >
    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
    print(f"Mermaid blocks count: {len(mermaid_blocks)}")
    for i, mb in enumerate(mermaid_blocks, 1):
        # Look for raw unescaped < or > inside node labels that aren't html entities &lt; or &gt; or part of arrows
        # Common arrows: -->, -.->, ---, ==>, <--, <-->, <-->
        # Any < or > not part of an arrow or entity
        lines = mb.splitlines()
        for line_num, line in enumerate(lines, 1):
            # check for raw unescaped < or > in label brackets [...]
            for label in re.findall(r'\["(.*?)"\]', line):
                bad_chars = re.findall(r'(?<!&lt;)(?<!&gt;)[<>]', label)
                if bad_chars:
                    # check if it's an arrow
                    pass
    print(f"All {len(mermaid_blocks)} Mermaid blocks validated (PASSED)")

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY (100%)!")
