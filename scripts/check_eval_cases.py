#!/usr/bin/env python3
"""Validate goal-creator eval case seeds."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "examples" / "evals" / "cases.json"
MODES = {"compact", "full-spec", "review"}
REQUIRED = {"name", "request", "mode", "language", "must_include", "must_not_include"}


def main() -> int:
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    errors: list[str] = []
    names: set[str] = set()

    for index, case in enumerate(cases):
        label = case.get("name", f"case {index}")
        missing = REQUIRED - set(case)
        if missing:
            errors.append(f"{label}: missing keys {sorted(missing)}")
            continue
        if case["name"] in names:
            errors.append(f"{label}: duplicate name")
        names.add(case["name"])
        if case["mode"] not in MODES:
            errors.append(f"{label}: invalid mode {case['mode']}")
        if not case["must_include"]:
            errors.append(f"{label}: must_include is empty")
        if case["language"] == "zh" and any(item.startswith("## ") and item.isascii() for item in case["must_include"]):
            errors.append(f"{label}: zh must_include should not require English headings")
        if "subagent" in case["name"] or "capacity" in case["name"]:
            for token in ["~/.codex/config.toml", "max_threads = 2147483647", "codex --strict-config doctor --summary --ascii"]:
                if token not in case["must_include"]:
                    errors.append(f"{label}: missing config token {token}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("eval cases ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
