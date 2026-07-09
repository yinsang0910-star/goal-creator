#!/usr/bin/env python3
"""Install this repository as the local Codex goal-creator skill."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS = [
    "SKILL.md",
    "examples",
    "scripts",
    "agents",
]


def user_home() -> Path:
    return Path.home()


def remove_inside(path: Path, parent: Path) -> None:
    resolved = path.resolve()
    root = parent.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"refusing to remove outside {root}: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def copy_item(name: str, target: Path) -> None:
    src = ROOT / name
    if not src.exists():
        return
    dst = target / name
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def run_check(target: Path, *parts: str) -> None:
    subprocess.run([sys.executable, str(target.joinpath(*parts))], check=True)


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] in {"-h", "--help"}:
        print("Usage: install_local.py [--no-check]")
        return 0

    run_checks = "--no-check" not in argv[1:]
    codex_skills = user_home() / ".codex" / "skills"
    agents_skills = user_home() / ".agents" / "skills"
    target = codex_skills / "goal-creator"
    stale_disabled = agents_skills / "goal-creator.disabled"

    codex_skills.mkdir(parents=True, exist_ok=True)
    remove_inside(target, codex_skills)
    target.mkdir(parents=True)
    for item in ITEMS:
        copy_item(item, target)

    if stale_disabled.exists():
        remove_inside(stale_disabled, agents_skills)

    if run_checks:
        run_check(target, "scripts", "smoke_test.py")
        subprocess.run(
            [
                sys.executable,
                str(target / "scripts" / "lint_goal_file.py"),
                str(target / "examples" / "full-spec-goal.md"),
            ],
            check=True,
        )

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
