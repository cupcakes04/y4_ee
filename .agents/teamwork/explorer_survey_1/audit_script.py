import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    'modules/EEEE4138_aerial_robotics/chapters/topic_1_uav_architectures.md',
    'modules/EEEE4138_aerial_robotics/chapters/topic_2_coordinate_frames.md'
]

for filepath in files:
    filename = os.path.basename(filepath)
    print(f"\n==========================================")
    print(f"Auditing {filename}")
    print(f"==========================================")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        content = "".join(lines)

    # 1. Check code blocks / language tags
    print("\n--- Code block fence check ---")
    in_fence = False
    fence_lang = ""
    start_line = 0
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_fence:
                in_fence = True
                fence_lang = line.strip()[3:].strip()
                start_line = idx
            else:
                in_fence = False
                print(f"Lines {start_line}-{idx}: ```{fence_lang}")
                if fence_lang not in ['mermaid']:
                    print(f"  [ALERT] Non-mermaid block detected: {fence_lang}")

    # 2. Check for tabs
    tabs = [idx for idx, l in enumerate(lines, 1) if '\t' in l]
    print(f"\n--- Tab character check ---")
    print(f"Found {len(tabs)} lines with tabs: {tabs}")
    for lnum in tabs:
        print(f"  Line {lnum}: {repr(lines[lnum-1])}")

    # 3. Check math pairs $$
    dd_matches = [idx for idx, l in enumerate(lines, 1) if '$$' in l]
    print(f"\n--- Double Dollar ($$) count ---")
    print(f"Total lines with $$: {len(dd_matches)}")
    # Count occurrences
    total_dd = content.count('$$')
    print(f"Total '$$' count: {total_dd} (balanced: {total_dd % 2 == 0})")

    # 4. Check inline math single dollar
    # Find lines where single $ count is odd (ignoring escaped \$)
    odd_dollar_lines = []
    in_math_block = False
    for idx, l in enumerate(lines, 1):
        if '$$' in l:
            # toggles
            count_dd = l.count('$$')
            if count_dd % 2 != 0:
                in_math_block = not in_math_block
            continue
        if in_math_block:
            continue
        # Count non-escaped $
        clean_l = l.replace('\\$', '')
        dollar_count = clean_l.count('$')
        if dollar_count % 2 != 0:
            odd_dollar_lines.append((idx, dollar_count, l.strip()))
    print(f"\n--- Unbalanced inline dollar check ---")
    print(f"Lines with odd single $: {len(odd_dollar_lines)}")
    for item in odd_dollar_lines:
        print(f"  Line {item[0]} (${item[1]}): {item[2][:80]}")

    # 5. Check Mermaid blocks
    print(f"\n--- Mermaid Block Detailed Audit ---")
    mermaid_blocks = re.finditer(r'```mermaid\r?\n(.*?)```', content, re.DOTALL)
    for b_idx, match in enumerate(mermaid_blocks, 1):
        b_content = match.group(1)
        b_start_offset = match.start()
        b_line_start = content[:b_start_offset].count('\n') + 1
        print(f"\nMermaid #{b_idx} starting at line {b_line_start}:")
        
        # Check for <br/> or <br>
        br_lines = [l for l in b_content.splitlines() if '<br' in l]
        if br_lines:
            print(f"  [ISSUE] {len(br_lines)} lines with <br> tags:")
            for l in br_lines:
                print(f"    {l.strip()}")
                
        # Check unescaped < or > (excluding <br>)
        bad_arrows = []
        for l in b_content.splitlines():
            # strip strings in quotes or check inside quotes
            # In mermaid, < inside quotes like ["... < ..."]
            clean = re.sub(r'<br\s*/?>', '', l)
            if re.search(r'<[^=-]', clean): # < not followed by - or =
                bad_arrows.append(l.strip())
        if bad_arrows:
            print(f"  [ISSUE] Potentially dangerous '<' symbols:")
            for l in bad_arrows:
                print(f"    {l}")

        # Check for unquoted labels with spaces
        unquoted = []
        for l in b_content.splitlines():
            # pattern like NodeName[Text\nMore] without quotes
            m = re.findall(r'(\w+\[[^\"\[\]\n]+\])', l)
            for u in m:
                if '\\n' in u or ' ' in u or ':' in u:
                    unquoted.append(u)
        if unquoted:
            print(f"  [ISSUE] Unquoted node labels with special chars:")
            for u in unquoted:
                print(f"    {u}")

    # 6. Check Generative UI iframe embedding
    print(f"\n--- Generative UI iframe / link check ---")
    iframes = re.findall(r'<iframe[^>]*>', content)
    print(f"Found {len(iframes)} iframe tags:")
    for ifr in iframes:
        print(f"  {ifr}")
    widget_links = re.findall(r'\[.*?\]\(.*?widget.*?\)', content)
    print(f"Found {len(widget_links)} widget links:")
    for wl in widget_links:
        print(f"  {wl}")
