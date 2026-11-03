#!/usr/bin/env python3
"""
study_audit.py — Audit study notes, track progress, and verify markdown links across all subjects.

Usage:
    python study_audit.py [--check-links] [--verbose]

Examples:
    # 1. Show overall study progress dashboard:
    python study_audit.py

    # 2. Check for broken links across all markdown notes:
    python study_audit.py --check-links
"""

import argparse
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = WORKSPACE_ROOT / "modules"

LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def get_files_excluding_gitkeep(directory: Path, pattern: str = "*") -> list[Path]:
    """Return all non-.gitkeep files matching pattern."""
    if not directory.exists():
        return []
    return [
        f for f in directory.rglob(pattern)
        if f.is_file() and f.name != ".gitkeep" and not f.name.startswith(".system")
    ]


def audit_module(mod_dir: Path) -> dict:
    raw_files = get_files_excluding_gitkeep(mod_dir / "raw")
    chapter_files = get_files_excluding_gitkeep(mod_dir / "chapters", "*.md")
    concept_files = get_files_excluding_gitkeep(mod_dir / "concepts", "*.md")
    drill_files = get_files_excluding_gitkeep(mod_dir / "drills")

    # Determine status
    if not raw_files and not chapter_files and not concept_files and not drill_files:
        status_icon = "⬜"
        status_text = "Not Started"
    elif len(concept_files) >= 5 and len(chapter_files) >= 3:
        status_icon = "✅"
        status_text = "Completed"
    elif concept_files or chapter_files or raw_files:
        status_icon = "🟡"
        status_text = "In Progress"
    else:
        status_icon = "⬜"
        status_text = "Not Started"

    return {
        "name": mod_dir.name,
        "raw": len(raw_files),
        "chapters": len(chapter_files),
        "concepts": len(concept_files),
        "drills": len(drill_files),
        "status_icon": status_icon,
        "status_text": status_text,
    }


def check_markdown_links() -> list[tuple[Path, str, str]]:
    """Scan all markdown files for broken relative links."""
    broken = []
    md_files = list(WORKSPACE_ROOT.glob("modules/**/*.md")) + [WORKSPACE_ROOT / "README.md"]

    for md_file in md_files:
        if not md_file.exists():
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for label, url in LINK_REGEX.findall(content):
            # Ignore web links, anchors, mailto, file URIs
            if url.startswith(("http://", "https://", "mailto:", "#", "file://")):
                continue
            # Strip anchors in relative paths
            clean_url = url.split("#")[0].strip()
            if not clean_url or " " in clean_url:
                continue

            target_path = (md_file.parent / clean_url).resolve()
            if not target_path.exists():
                broken.append((md_file, label, url))

    return broken


def main():
    parser = argparse.ArgumentParser(description="Audit study progress and link integrity.")
    parser.add_argument("--check-links", action="store_true", help="Audit all relative links for 404 dead links")
    parser.add_argument("--verbose", action="store_true", help="Show detailed breakdown")
    args = parser.parse_args()

    modules = sorted([d for d in MODULES_DIR.iterdir() if d.is_dir()])
    stats = [audit_module(m) for m in modules]

    print("\n" + "=" * 78)
    print(" 📚 Year 4 Study Progress Dashboard")
    print("=" * 78)
    header = f"{'Subject Module':<38} | {'Raw':<4} | {'Chap':<4} | {'Conc':<4} | {'Drill':<5} | Status"
    print(header)
    print("-" * 78)

    total_raw = sum(s["raw"] for s in stats)
    total_chap = sum(s["chapters"] for s in stats)
    total_conc = sum(s["concepts"] for s in stats)
    total_drill = sum(s["drills"] for s in stats)

    for s in stats:
        name = s["name"]
        if len(name) > 37:
            name = name[:34] + "..."
        print(f"{name:<38} | {s['raw']:<4} | {s['chapters']:<4} | {s['concepts']:<4} | {s['drills']:<5} | {s['status_icon']} {s['status_text']}")

    print("-" * 78)
    print(f"{'TOTALS':<38} | {total_raw:<4} | {total_chap:<4} | {total_conc:<4} | {total_drill:<5} |")
    print("=" * 78)

    if args.check_links:
        print("\n🔍 Checking Relative Markdown Links...")
        broken = check_markdown_links()
        if not broken:
            print("✅ All relative links are intact! No broken links found.")
        else:
            print(f"⚠️  Found {len(broken)} broken link(s):")
            for src, label, target in broken:
                rel_src = src.relative_to(WORKSPACE_ROOT)
                print(f"  • In {rel_src}: '[{label}]({target})' → Target not found!")
    print("")


if __name__ == "__main__":
    main()
