#!/usr/bin/env python3
"""Detect anti-patterns in skill definitions from the catalog."""

import json
import sys
from pathlib import Path

from colorama import Fore, Style, init

init(autoreset=True)

ANTI_PATTERNS = {
    "description": ["learn about", "understand", "know about", "explore"],
    "tags": ["general", "other", "misc"],
    "name": ["skill-", "test-", "temp-", "sample-"],
}


def detect_patterns(catalog_path: Path) -> int:
    with open(catalog_path, encoding="utf-8") as f:
        data = json.load(f)

    issues = 0
    skills = data.get("skills", [])

    for skill in skills:
        name = skill.get("name", "unknown")
        desc = (skill.get("description", "") or "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]
        models = skill.get("models", [])

        for pattern in ANTI_PATTERNS["description"]:
            if pattern in desc:
                print(f"{Fore.YELLOW}{name}: Description contains '{pattern}'{Style.RESET_ALL}")
                issues += 1

        for pattern in ANTI_PATTERNS["name"]:
            if name.lower().startswith(pattern):
                print(f"{Fore.YELLOW}{name}: Name starts with '{pattern}'{Style.RESET_ALL}")
                issues += 1

        for bad_tag in ANTI_PATTERNS["tags"]:
            if bad_tag in tags:
                print(f"{Fore.YELLOW}{name}: Contains generic tag '{bad_tag}'{Style.RESET_ALL}")
                issues += 1

        if len(tags) != len(set(tags)):
            dupes = {t for t in tags if tags.count(t) > 1}
            print(f"{Fore.YELLOW}{name}: Duplicate tags {dupes}{Style.RESET_ALL}")
            issues += 1

        if len(models) >= 2 and set(models) == {"gpt-4", "claude-3"}:
            print(f"{Fore.CYAN}{name}: Default model set (may need update){Style.RESET_ALL}")

    if issues == 0:
        print(f"{Fore.GREEN}No anti-patterns detected{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}{issues} potential issue(s) found{Style.RESET_ALL}")

    return 0


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console
    ensure_utf8_console()
    import argparse
    parser = argparse.ArgumentParser(description="Detect anti-patterns in skills")
    parser.add_argument("filepath", nargs="?", default="skills_catalog.json", help="Path to skills_catalog.json")
    args = parser.parse_args()
    return detect_patterns(Path(args.filepath))


if __name__ == "__main__":
    sys.exit(main())
