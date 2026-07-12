#!/usr/bin/env python3
"""Dependency-free behavior checks for goal-creator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SAVE = ROOT / "scripts" / "save_goal.py"
LINT = ROOT / "scripts" / "lint_goal_file.py"
EXAMPLE = ROOT / "examples" / "full-spec-goal.md"

BODY = """# 中文契约

<!-- goal:launcher -->
## 启动入口
```text
/goal 只执行 `.goals/example.md`。
```

<!-- goal:objective -->
## 目标
创建可验证、可恢复且服从当前事实的目标契约。

<!-- goal:original_request -->
## 原始需求
精简目标创建工具，不重新发明 agent 编排。

<!-- goal:non_negotiables -->
## 不可降级项
- 不执行目标，不修改全局配置。

<!-- goal:success_criteria -->
## 成功标准
- 保存、检查和中文读取均成功。

<!-- goal:scope -->
## 范围
允许:
- 当前仓库。
禁止:
- 全局配置、其他 skill 和插件缓存。

<!-- goal:plan -->
## 执行计划
1. 修改。
2. 验证。

<!-- goal:verification -->
## 验证
- 运行 `python scripts/smoke_test.py`。
- 检查保存文件。

<!-- goal:safety -->
## 安全 / 约束
- 保持 UTF-8，不对外发布。

<!-- goal:iteration -->
## 迭代策略
- 根据真实失败证据修复，不降低目标。

<!-- goal:authority -->
## 权威顺序
- 读取并遵守适用的 `AGENTS.md` 和项目当前正本。
- 当前代码和最新 runtime evidence 优先于旧 checkbox、聊天、总结和本 goal 的事实陈述。
- 本 goal 只保存意图与边界，不是第二事实权威。

<!-- goal:stop -->
## 停止
- 检查通过且保存产物存在。

<!-- goal:pause -->
## 暂停
- 外部发布或仓库外写入需要用户确认。
"""


def run(path: Path, *args: str, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *args], input=input_text, text=True, capture_output=True, check=check,
    )


def main() -> int:
    skill = SKILL.read_text(encoding="utf-8")
    inline = skill.split("For an unsaved full-spec", 1)[1].split("For a persisted full-spec", 1)[0]
    assert "/goal" in inline and ".goals/" not in inline

    assert "goal file lint ok" in run(LINT, str(EXAMPLE)).stdout

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        args = ("--title", "创建目标", "--language", "zh", "--format", "codex", "--dir", str(tmp / ".goals"))
        first = Path(run(SAVE, *args, input_text=BODY).stdout.strip())
        second = Path(run(SAVE, *args, input_text=BODY).stdout.strip())
        assert first.exists() and second.exists() and first != second

        saved = first.read_text(encoding="utf-8")
        assert "schema: goal/v1" in saved and "authority: subordinate" in saved
        assert "max_threads" not in saved and "max_depth" not in saved
        assert "goal file lint ok" in run(LINT, str(first)).stdout

        translated = tmp / "translated.md"
        translated.write_text(saved.replace("## 原始需求", "## 用户最初要求").replace("## 权威顺序", "## 当前事实优先级"), encoding="utf-8")
        assert "goal file lint ok" in run(LINT, str(translated)).stdout

        fenced = tmp / "fenced.md"
        fenced.write_text(saved.replace("<!-- goal:stop -->", "```markdown\n## 子代理派发决策\n```\n\n<!-- goal:stop -->"), encoding="utf-8")
        assert "goal file lint ok" in run(LINT, str(fenced)).stdout

        obsolete = tmp / "obsolete.md"
        obsolete.write_text(saved.replace("<!-- goal:stop -->", "## 子代理派发决策\n\n- L2: fixed.\n\n<!-- goal:stop -->"), encoding="utf-8")
        assert "obsolete" in run(LINT, str(obsolete), check=False).stderr

        incomplete = run(SAVE, "--title", "incomplete", "--dir", str(tmp / ".goals"), input_text="# Goal\n", check=False)
        assert incomplete.returncode == 1 and "missing canonical field" in incomplete.stderr

        compact = tmp / "compact.md"
        compact.write_text("---\nmode: compact\n---\n\n/goal 修复 README 错别字。\n", encoding="utf-8")
        assert "goal file lint ok" in run(LINT, str(compact)).stdout

    print("smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
