#!/usr/bin/env python3
"""Save a goal markdown document under .goals/."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    if slug:
        return slug
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"goal-{digest}"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def unique_path(directory: Path, stem: str) -> Path:
    path = directory / f"{stem}.md"
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = directory / f"{stem}-{index}.md"
        if not candidate.exists():
            return candidate
        index += 1


def read_body(args: argparse.Namespace) -> str:
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8").strip()
    return sys.stdin.read().strip()


def lint_full_spec(content: str, source: str) -> list[str]:
    try:
        from lint_goal_file import lint_text
    except ImportError as exc:
        return [f"{source}: cannot validate full-spec goal: {exc}"]
    return lint_text(content, source)


def main() -> int:
    parser = argparse.ArgumentParser(description="Save a goal markdown file.")
    parser.add_argument("--title", required=True, help="Goal title.")
    parser.add_argument("--status", default="draft", help="Goal status.")
    parser.add_argument("--language", default="", help="Goal language.")
    parser.add_argument("--mode", default="full-spec", help="Goal mode.")
    parser.add_argument("--format", action="append", dest="formats", default=[])
    parser.add_argument("--body-file", help="Read goal body from a file.")
    parser.add_argument("--dir", default=".goals", help="Output directory.")
    args = parser.parse_args()

    body = read_body(args)
    if not body:
        print("error: goal body is empty", file=sys.stderr)
        return 2

    today = date.today().isoformat()
    out_dir = Path(args.dir)
    stem = f"{today}-{slugify(args.title)}"
    path = unique_path(out_dir, stem)
    formats = args.formats or ["codex", "markdown"]
    language_line = f"language: {args.language}\n" if args.language else ""
    format_lines = "".join(f"  - {item}\n" for item in formats)

    content = (
        "---\n"
        "schema: goal/v1\n"
        "authority: subordinate\n"
        f"title: {yaml_quote(args.title)}\n"
        f"created: {today}\n"
        f"status: {args.status}\n"
        f"{language_line}"
        f"mode: {args.mode}\n"
        "formats:\n"
        f"{format_lines}"
        "---\n\n"
        f"{body}\n"
    )
    if args.mode == "full-spec":
        errors = lint_full_spec(content, path.as_posix())
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
