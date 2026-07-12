#!/usr/bin/env python3
"""Validate, back up, and install only the public goal-creator skill."""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS = ("SKILL.md", "examples", "scripts", "agents")


def remove_inside(path: Path, parent: Path) -> None:
    resolved, root = path.resolve(), parent.resolve()
    if resolved == root or root not in resolved.parents:
        raise RuntimeError(f"refusing to remove outside {root}: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def copy_package(target: Path) -> None:
    target.mkdir(parents=True)
    for name in ITEMS:
        src, dst = ROOT / name, target / name
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        elif src.exists():
            shutil.copy2(src, dst)


def check_package(root: Path) -> None:
    subprocess.run([sys.executable, str(root / "scripts" / "smoke_test.py")], check=True)
    subprocess.run(
        [sys.executable, str(root / "scripts" / "lint_goal_file.py"), str(root / "examples" / "full-spec-goal.md")],
        check=True,
    )


def remove_caches(root: Path) -> None:
    for cache in root.rglob("__pycache__"):
        remove_inside(cache, root)


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print("Usage: install_local.py", file=sys.stderr)
        return 2

    check_package(ROOT)
    agents_home = Path.home() / ".agents"
    skills = agents_home / "skills"
    target = skills / "goal-creator"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    staging = skills / f".goal-creator-installing-{stamp}"
    backup = agents_home / "skill-backups" / "goal-creator" / stamp

    skills.mkdir(parents=True, exist_ok=True)
    for stale in skills.glob(".goal-creator-installing-*"):
        remove_inside(stale, skills)
    copy_package(staging)
    check_package(staging)
    remove_caches(staging)

    moved = False
    try:
        if target.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
            moved = True
        shutil.copytree(staging, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        check_package(target)
        remove_caches(target)
    except Exception:
        remove_inside(target, skills)
        if moved and backup.exists():
            backup.rename(target)
        raise

    remove_inside(staging, skills)
    print(target)
    print(backup if moved else "no previous installation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
