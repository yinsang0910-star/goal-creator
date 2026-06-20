#!/usr/bin/env python3
"""Small self-check for save_goal.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "save_goal.py"
BODY = """# Smoke Goal

## Short Command

```text
/goal Read `.goals/example.md` first, then execute only the work defined there.
```

## Objective

Confirm save_goal.py writes a full-spec goal file.

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


def main() -> int:
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
        assert "/goal Read `.goals/example.md` first" in text
        assert "## Verification" in text

    print("smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
