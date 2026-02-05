#!/usr/bin/env python3
"""
TechNews Complete Workflow - Fetch, extract, and summarize tech news
"""

import json
import sys
import subprocess
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def fetch_techmeme_stories(num_stories: int = 10) -> list:
    """Fetch stories from TechMeme."""
    try:
        result = subprocess.run(
            ["python3", "techmeme_scraper.py", str(num_stories)],
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("stories", [])
    except Exception as e:
        print(f"Error fetching TechMeme: {e}", file=sys.stderr)
    return []


def format_stories(stories: list, max_stories: int = 5) -> str:
    """Format stories for display."""
    output = ["📰 **TechNews - 最新科技新闻**\n"]

    for i, story in enumerate(stories[:max_stories], 1):
        title = story.get("title", "无标题")
        url = story.get("url", "")
        summary = story.get("summary", "")[:150]

        output.append(f"{i}. **{title}**")
        if summary:
            output.append(f"   {summary}...")
        output.append(f"   🔗 {url}")
        output.append("")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="TechNews - Latest Tech News")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of stories")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Fetch stories
    stories = fetch_techmeme_stories(args.count)

    if not stories:
        print("❌ 无法获取新闻", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps({"stories": stories[:args.count]}, indent=2, ensure_ascii=False))
    else:
        print(format_stories(stories[:args.count]))


if __name__ == "__main__":
    main()
