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
BODY = """# 冒烟目标

## 短启动命令

```text
/goal 读取 `.goals/example.md`；只执行该文件。
```

## 目标

确认 save_goal.py 能写入完整目标文件。

## 原始需求

创建一个不缩小用户原始目标的完整目标文件。

## 不可降级项

- 保留短启动命令。
- 保留完整目标合同。

## 成功标准

- 文件存在。

## 范围

允许:
- 只写入临时目录。

禁止:
- 不触碰真实仓库。

## 验证

- 保存文件包含 frontmatter 和短启动命令。

## 停止

- 检查通过。

## 暂停

- 脚本失败。
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
        assert "## 短启动命令" in text
        assert "/goal 读取 `.goals/example.md`；只执行该文件。" in text
        assert "## 原始需求" in text
        assert "## 不可降级项" in text
        assert "## 验证" in text
        assert "## Objective" not in text
        assert "## Success Criteria" not in text
        assert "Allowed:" not in text
        assert "Forbidden:" not in text

        skill_text = SKILL.read_text(encoding="utf-8")
        assert "Quality bar before saving" in skill_text
        assert "under 140 characters" in skill_text
        assert "Use one target language for all visible headings and prose" in skill_text
        assert "do not keep English headings" in skill_text
        assert "Chinese label map" in skill_text
        assert "`Allowed` -> `允许`" in skill_text
        assert "render visible field labels in the target language" in skill_text
        assert "Original Request preserves" in skill_text
        assert "must not weaken user-provided acceptance criteria" in skill_text
        assert "Do not silently reduce scope" in skill_text
        assert "saved goal is the higher-level contract" in skill_text
        assert "Multi-agent collaboration extension" in skill_text
        assert "Slice Table" in skill_text
        assert "Subagent Deliverables" in skill_text
        assert "Do not force multi-agent execution" in skill_text
        assert "Do not bypass completed subagent work" in skill_text
        assert "Reject or return a subagent result" in skill_text

    print("smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
