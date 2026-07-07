#!/usr/bin/env python3
"""Small self-check for save_goal.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "save_goal.py"
LINT = ROOT / "scripts" / "lint_goal_file.py"
INSTALL = ROOT / "scripts" / "install_local.py"
CHECK_EVALS = ROOT / "scripts" / "check_eval_cases.py"
SKILL = ROOT / "SKILL.md"
EVALS = ROOT / "examples" / "evals" / "cases.json"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
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

## 安全 / 约束

- 不触碰真实仓库。

## 迭代策略

- 每次有意义改动后重跑检查。

## 多代理协同

- 主会话先冻结原始目标、成功标准、不可降级项、共享接口和文件边界。
- 主会话默认先拆分至少两个实质性、低冲突、可并行的垂直切片并派发给子代理；无法拆分时写入暂停条件。

## 派发表

| 切片 | 代理角色 | 目标 | 允许文件 | 禁止文件 | 输入 | 必交输出 | 验证 | 依赖 | 合并负责人 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| implementation | 子代理 | 更新保存脚本行为 | scripts/save_goal.py | README.md, SKILL.md | 现有 CLI 和保存格式 | 改动文件、验证命令、结果、风险、交接说明 | 运行 smoke test | 无 | 主会话 |
| verification | 子代理 | 扩展质量检查覆盖 | scripts/smoke_test.py, scripts/lint_goal_file.py | README.md, SKILL.md | 新协议验收标准 | 改动文件、验证命令、结果、风险、交接说明 | 运行 smoke test 和 goal file lint | implementation | 主会话 |

## 共享文件归属

Main-session-owned:
- README.md
- SKILL.md

Subagent-owned:
- scripts/save_goal.py
- scripts/smoke_test.py
- scripts/lint_goal_file.py

## 子代理结果

切片:
状态: adopted | needs-main-merge | blocked | rejected
改动文件:
验证命令:
验证结果:
越界情况:
风险:
交接说明:

## 合并策略

- 主会话串行消费子代理结果并合并。

## 拒绝条件

- 越界、无验证、弱化目标、接口冲突或交接不可合并。

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


def run_lint(path: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LINT), str(path)],
        text=True,
        capture_output=True,
        check=check,
    )


def run_script(path: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *args],
        text=True,
        capture_output=True,
        check=check,
    )


def check_skill_frontmatter() -> None:
    text = SKILL.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    keys = {
        line.split(":", 1)[0]
        for line in frontmatter.splitlines()
        if line and not line.startswith(" ")
    }
    assert keys == FRONTMATTER_KEYS, keys


def check_eval_cases() -> None:
    cases = json.loads(EVALS.read_text(encoding="utf-8"))
    assert len(cases) >= 5
    required = {"name", "request", "mode", "language", "must_include", "must_not_include"}
    for case in cases:
        assert required <= set(case), case


def main() -> int:
    check_skill_frontmatter()
    check_eval_cases()
    assert OPENAI_YAML.exists()
    assert "Goal Creator" in OPENAI_YAML.read_text(encoding="utf-8")
    assert "Usage: install_local.py" in run_script(INSTALL, "--help").stdout
    assert "eval cases ok" in run_script(CHECK_EVALS).stdout

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
        assert "## 多代理协同" in text
        assert "## 派发表" in text
        assert "## 共享文件归属" in text
        assert "## 子代理结果" in text
        assert "| 切片 | 代理角色 | 目标 | 允许文件 | 禁止文件 | 输入 | 必交输出 | 验证 | 依赖 | 合并负责人 |" in text

        good = run_lint(first)
        assert "goal file lint ok" in good.stdout

        bad = tmp / "bad.md"
        bad.write_text(
            "---\ntitle: bad\nmode: full-spec\nlanguage: zh\nformats:\n  - codex\n---\n\n"
            "# bad\n\n## Objective\n\nTODO\n",
            encoding="utf-8",
        )
        failed = run_lint(bad, check=False)
        assert failed.returncode == 1
        assert "missing section" in failed.stderr

        one_slice = tmp / "one-slice.md"
        one_slice.write_text(text.replace("| verification | 子代理 | 扩展质量检查覆盖 | scripts/smoke_test.py, scripts/lint_goal_file.py | README.md, SKILL.md | 新协议验收标准 | 改动文件、验证命令、结果、风险、交接说明 | 运行 smoke test 和 goal file lint | implementation | 主会话 |\n", ""), encoding="utf-8")
        failed = run_lint(one_slice, check=False)
        assert failed.returncode == 1
        assert "Dispatch Matrix needs at least 2 data rows" in failed.stderr

        missing_owner = tmp / "missing-owner.md"
        missing_owner.write_text(text.replace("Subagent-owned:", "Subagent owned:"), encoding="utf-8")
        failed = run_lint(missing_owner, check=False)
        assert failed.returncode == 1
        assert "Shared File Ownership missing `Subagent-owned:`" in failed.stderr

        missing_matrix_header = tmp / "missing-matrix-header.md"
        missing_matrix_header.write_text(text.replace("合并负责人 |", "|"), encoding="utf-8")
        failed = run_lint(missing_matrix_header, check=False)
        assert failed.returncode == 1
        assert "Dispatch Matrix missing required column" in failed.stderr

        fake_slice = tmp / "fake-slice.md"
        fake_slice.write_text(text.replace("更新保存脚本行为", "只阅读并总结保存脚本"), encoding="utf-8")
        failed = run_lint(fake_slice, check=False)
        assert failed.returncode == 1
        assert "Dispatch Matrix contains read-only or summary-only slice" in failed.stderr

        vague = tmp / "vague.md"
        vague.write_text(text.replace("- 检查通过。", "- 看起来可以。"), encoding="utf-8")
        failed = run_lint(vague, check=False)
        assert failed.returncode == 1
        assert "vague completion language" in failed.stderr

        skill_text = SKILL.read_text(encoding="utf-8")
        assert "Quality bar before saving" in skill_text
        assert "under 140 characters" in skill_text
        assert "Use one target language for all visible headings and prose" in skill_text
        assert "do not keep English headings" in skill_text
        assert "Chinese label map" in skill_text
        assert "`Allowed` -> `允许`" in skill_text
        assert "`Codex Subagent Capacity Setup` -> `Codex 子代理并发配置`" in skill_text
        assert "`Required Output` -> `必交输出`" in skill_text
        assert "render visible field labels in the target language" in skill_text
        assert "Original Request preserves" in skill_text
        assert "must not weaken user-provided acceptance criteria" in skill_text
        assert "Do not silently reduce scope" in skill_text
        assert "saved goal is the higher-level contract" in skill_text
        assert "Full-spec goals default to forced subagent dispatch" in skill_text
        assert "Dispatch protocol default" in skill_text
        assert "Dispatch Matrix" in skill_text
        assert "Shared File Ownership" in skill_text
        assert "Subagent Result" in skill_text
        assert "`Dispatch Matrix` -> `派发表`" in skill_text
        assert "`Shared File Ownership` -> `共享文件归属`" in skill_text
        assert "`Subagent Result` -> `子代理结果`" in skill_text
        assert "Subagents must not be used only for simple reading" in skill_text
        assert "inventing fake parallel work" in skill_text
        assert "Do not bypass completed subagent work" in skill_text
        assert "Reject or return a subagent result" in skill_text
        assert "Codex subagent capacity setup" in skill_text
        assert "~/.codex/config.toml" in skill_text
        assert "max_threads = 2147483647" in skill_text
        assert "codex --strict-config doctor --summary --ascii" in skill_text
        assert "lint_goal_file.py" in skill_text
        assert "install_local.py" in skill_text
        assert "check_eval_cases.py" in skill_text

    print("smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
