#!/usr/bin/env python3
"""Small self-check for save_goal.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "save_goal.py"
SKILL = ROOT / "SKILL.md"
FRONTMATTER_KEYS = {"name", "description"}
BODY = """# Smoke Goal

## Short Command

```text
/goal Read `.goals/example.md`; execute only that file.
```

## Objective

Confirm save_goal.py writes a full-spec goal file.

## Original Request

Create a saved full-spec goal without narrowing the user's requested outcome.

## Non-Negotiables

- Keep the short launcher.
- Keep the full saved goal contract.

## Success Criteria

- File exists.

## Scope

Allowed:
- Write only inside the temp directory.

Forbidden:
- Do not touch the real repository.

## Verification

- Saved file contains frontmatter and short command.

## Stop

- Checks pass.

## Pause

- Script fails.
"""


def run_save(tmp: Path, title: str) -> Path:
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--title",
            title,
            "--language",
            "zh",
            "--format",
            "codex",
        ],
        input=BODY,
        text=True,
        cwd=tmp,
        capture_output=True,
        check=True,
    )
    return tmp / proc.stdout.strip()


def check_skill_frontmatter() -> None:
    text = SKILL.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    keys = {
        line.split(":", 1)[0]
        for line in frontmatter.splitlines()
        if line and not line.startswith(" ")
    }
    assert keys == FRONTMATTER_KEYS, keys


def main() -> int:
    check_skill_frontmatter()

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        first = run_save(tmp, "创建目标")
        second = run_save(tmp, "创建目标")

        assert first.exists(), first
        assert second.exists(), second
        assert first.name != second.name

        text = first.read_text(encoding="utf-8")
        assert 'title: "创建目标"' in text
        assert "mode: full-spec" in text
        assert "formats:\n  - codex" in text
        assert "## Short Command" in text
        assert "/goal Read `.goals/example.md`; execute only that file." in text
        assert "## Original Request" in text
        assert "## Non-Negotiables" in text
        assert "## Verification" in text

        skill_text = SKILL.read_text(encoding="utf-8")
        assert "Quality bar before saving" in skill_text
        assert "under 140 characters" in skill_text
        assert "Original Request preserves" in skill_text
        assert "must not weaken user-provided acceptance criteria" in skill_text
        assert "Do not silently reduce scope" in skill_text
        assert "saved goal is the higher-level contract" in skill_text

    print("smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
