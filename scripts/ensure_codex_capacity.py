#!/usr/bin/env python3
"""One-time Codex subagent capacity setup."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


THREADS = "2147483647"
DEPTH = "2147483647"


def ensure_agents_block(text: str) -> tuple[str, bool]:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "[agents]"), None)
    if start is None:
        prefix = "\n\n" if text.strip() else ""
        block = f"{prefix}[agents]\nmax_threads = {THREADS}\nmax_depth = {DEPTH}\n"
        return text.rstrip() + block, True

    end = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("[") and lines[i].rstrip().endswith("]")), len(lines))
    seen = {"max_threads": False, "max_depth": False}
    changed = False

    for i in range(start + 1, end):
        stripped = lines[i].strip()
        if stripped.startswith("max_threads"):
            wanted = f"max_threads = {THREADS}"
            changed |= lines[i] != wanted
            lines[i] = wanted
            seen["max_threads"] = True
        elif stripped.startswith("max_depth"):
            wanted = f"max_depth = {DEPTH}"
            changed |= lines[i] != wanted
            lines[i] = wanted
            seen["max_depth"] = True

    inserts = []
    if not seen["max_threads"]:
        inserts.append(f"max_threads = {THREADS}")
    if not seen["max_depth"]:
        inserts.append(f"max_depth = {DEPTH}")
    if inserts:
        lines[end:end] = inserts
        changed = True

    return "\n".join(lines) + "\n", changed


def run_doctor(timeout: int) -> str:
    commands = [
        ["codex", "--strict-config", "doctor", "--summary", "--ascii"],
        ["codex.cmd", "--strict-config", "doctor", "--summary", "--ascii"],
    ]
    errors = []
    for command in commands:
        if shutil.which(command[0]) is None:
            errors.append(f"{command[0]} not found")
            continue
        try:
            proc = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            errors.append(f"{command[0]} timed out after {timeout}s")
            continue
        except OSError as exc:
            errors.append(f"{command[0]} failed to start: {exc}")
            continue
        output = (proc.stdout + proc.stderr).strip()
        if proc.returncode == 0 and "loaded" in output.lower():
            return output
        errors.append(output or f"{command[0]} exited {proc.returncode}")
    return "warning: doctor check skipped: " + "; ".join(errors)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Ensure Codex subagent capacity is configured once.")
    parser.add_argument("--config", default=str(Path.home() / ".codex" / "config.toml"))
    parser.add_argument("--marker", default=str(Path.home() / ".codex" / "goal-creator-capacity.ok"))
    parser.add_argument("--doctor", action="store_true", help="Also run codex doctor; off by default to avoid slow Windows shims.")
    parser.add_argument("--skip-doctor", action="store_true", help="Deprecated alias; doctor is skipped unless --doctor is passed.")
    parser.add_argument("--doctor-timeout", type=int, default=20)
    args = parser.parse_args(argv[1:])

    config = Path(args.config)
    marker = Path(args.marker)
    text = config.read_text(encoding="utf-8") if config.exists() else ""
    updated, changed = ensure_agents_block(text)

    already_marked = marker.exists()
    if changed:
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(updated, encoding="utf-8", newline="\n")

    if args.doctor and not args.skip_doctor:
        result = run_doctor(args.doctor_timeout)
        if result.startswith("warning:"):
            print(result, file=sys.stderr)

    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("ok\n", encoding="utf-8")
    if already_marked and not changed:
        print("capacity already ok")
    else:
        print("capacity ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
