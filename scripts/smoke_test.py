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

## 启动入口

```text
/goal 只执行 `.goals/example.md`
```

## 目标

确认 save_goal.py 能写入完整目标文件。

## 原始需求

创建一个不缩小用户原始目标的完整目标文件。

## 不可降级项

- 保留启动入口。
- 保留完整目标合同。

## 成功标准

- 文件存在。

## 范围

允许:
- 只写入临时目录。

禁止:
- 不触碰真实仓库。

## 验证

- 保存文件包含 frontmatter 和启动入口。

## 安全 / 约束

- 不触碰真实仓库。

## 迭代策略

- 每次有意义改动后重跑检查。

## Codex 执行契约

- CWD: 当前项目根目录。
- 指令来源: 读取并遵守适用的 AGENTS.md。
- 可恢复产物: 本文件 `.goals/example.md`。
- 收尾检查: `git status --short`、`git diff --check`、`python scripts/smoke_test.py`。
- 聊天输出: 只报告保存路径、启动入口、验证结果和必要风险。

## 子代理容量前置

- 使用 full-spec / subagent-first 目标前，先检查当前用户的 `~/.codex/config.toml`。
- 如果没有 `[agents]` 段，追加该段；如果已有，只更新 `max_threads = 2147483647` 和 `max_depth = 2147483647`。
- 不要删除或重排现有配置。
- 修改后运行 `codex --strict-config doctor --summary --ascii`。
- Windows 下如果 `codex` 被 PowerShell 执行策略或 shim 拦截，运行 `codex.cmd --strict-config doctor --summary --ascii`。
- 只有输出显示 `Configuration` / `config` 为 `loaded`，才继续执行需要子代理释放的任务。

## 子代理派发决策

- L0: 不派发，适用于单文件小修、简单解释、简单命令。
- L1: 一个子代理，适用于隔离阅读、局部验证或风险检查。
- L2: 最少 2 个子代理，适用于跨模块或代码与测试可并行。
- L3: 最少 4 个子代理，适用于多模块迁移、重构、排查或批量修复。
- 简单任务必须保持 L0，禁止为了形式派发无效子代理。
- 如果选择 L2/L3 但当前会话无法创建足额子代理，必须暂停，不得由主会话继续代替执行。

## 子代理执行力释放

- 主会话默认作为调度者、合并者和最终验证者运行。
- 能隔离、能验证、能交付的执行工作优先下放给子代理。
- 子代理负责读取上下文、实现、局部测试、局部修复和风险回报。
- 主会话只保留目标冻结、边界裁决、合并和最终验证。

## 多代理协同

- 主会话先冻结原始目标、成功标准、不可降级项、共享接口和文件边界。
- 主会话根据派发等级决定 L0/L1/L2/L3，不制造假并行。

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
        assert "## 启动入口" in text
        assert "/goal 只执行 `.goals/example.md`" in text
        assert "## 原始需求" in text
        assert "## 不可降级项" in text
        assert "## 验证" in text
        assert "## Objective" not in text
        assert "## Success Criteria" not in text
        assert "Allowed:" not in text
        assert "Forbidden:" not in text
        assert "## Codex 执行契约" in text
        assert "AGENTS.md" in text
        assert ".goals/example.md" in text
        assert "git status --short" in text
        assert "git diff --check" in text
        assert "## 子代理容量前置" in text
        assert "~/.codex/config.toml" in text
        assert "max_threads = 2147483647" in text
        assert "max_depth = 2147483647" in text
        assert "codex --strict-config doctor --summary --ascii" in text
        assert "codex.cmd --strict-config doctor --summary --ascii" in text
        assert "loaded" in text
        assert "## 子代理派发决策" in text
        assert "最少 2" in text
        assert "最少 4" in text
        assert "不得由主会话继续" in text
        assert "L0" in text and "L1" in text and "L2" in text and "L3" in text
        assert "## 子代理执行力释放" in text
        assert "调度" in text
        assert "下放" in text
        assert "## 多代理协同" in text
        assert "## 派发表" in text
        assert "## 共享文件归属" in text
        assert "## 子代理结果" in text
        assert "| 切片 | 代理角色 | 目标 | 允许文件 | 禁止文件 | 输入 | 必交输出 | 验证 | 依赖 | 合并负责人 |" in text

        good = run_lint(first)
        assert "goal file lint ok" in good.stdout

        fullwidth_colon = tmp / "fullwidth-colon.md"
        fullwidth_colon.write_text(
            text.replace("切片:", "切片：")
            .replace("状态:", "状态：")
            .replace("改动文件:", "改动文件：")
            .replace("验证命令:", "验证命令：")
            .replace("验证结果:", "验证结果：")
            .replace("越界情况:", "越界情况：")
            .replace("风险:", "风险：")
            .replace("交接说明:", "交接说明："),
            encoding="utf-8",
        )
        good = run_lint(fullwidth_colon)
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

        missing_codex_contract = tmp / "missing-codex-contract.md"
        missing_codex_contract.write_text(
            text.replace(
                "## Codex 执行契约\n\n- CWD: 当前项目根目录。\n- 指令来源: 读取并遵守适用的 AGENTS.md。\n- 可恢复产物: 本文件 `.goals/example.md`。\n- 收尾检查: `git status --short`、`git diff --check`、`python scripts/smoke_test.py`。\n- 聊天输出: 只报告保存路径、启动入口、验证结果和必要风险。\n\n",
                "",
            ),
            encoding="utf-8",
        )
        failed = run_lint(missing_codex_contract, check=False)
        assert failed.returncode == 1
        assert "missing full-spec Codex section" in failed.stderr

        missing_capacity = tmp / "missing-capacity.md"
        missing_capacity.write_text(
            text.replace(
                "## 子代理容量前置\n\n- 使用 full-spec / subagent-first 目标前，先检查当前用户的 `~/.codex/config.toml`。\n- 如果没有 `[agents]` 段，追加该段；如果已有，只更新 `max_threads = 2147483647` 和 `max_depth = 2147483647`。\n- 不要删除或重排现有配置。\n- 修改后运行 `codex --strict-config doctor --summary --ascii`。\n- Windows 下如果 `codex` 被 PowerShell 执行策略或 shim 拦截，运行 `codex.cmd --strict-config doctor --summary --ascii`。\n- 只有输出显示 `Configuration` / `config` 为 `loaded`，才继续执行需要子代理释放的任务。\n\n",
                "",
            ),
            encoding="utf-8",
        )
        failed = run_lint(missing_capacity, check=False)
        assert failed.returncode == 1
        assert "missing full-spec multi-agent section `子代理容量前置`" in failed.stderr

        missing_dispatch_decision = tmp / "missing-dispatch-decision.md"
        missing_dispatch_decision.write_text(
            text.replace(
                "## 子代理派发决策\n\n- L0: 不派发，适用于单文件小修、简单解释、简单命令。\n- L1: 一个子代理，适用于隔离阅读、局部验证或风险检查。\n- L2: 最少 2 个子代理，适用于跨模块或代码与测试可并行。\n- L3: 最少 4 个子代理，适用于多模块迁移、重构、排查或批量修复。\n- 简单任务必须保持 L0，禁止为了形式派发无效子代理。\n- 如果选择 L2/L3 但当前会话无法创建足额子代理，必须暂停，不得由主会话继续代替执行。\n\n",
                "",
            ),
            encoding="utf-8",
        )
        failed = run_lint(missing_dispatch_decision, check=False)
        assert failed.returncode == 1
        assert "missing full-spec multi-agent section `子代理派发决策`" in failed.stderr

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
        assert "`Short Command` -> `启动入口`" in skill_text
        assert "`Codex Subagent Capacity Setup` -> `Codex 子代理并发配置`" in skill_text
        assert "`Required Output` -> `必交输出`" in skill_text
        assert "render visible field labels in the target language" in skill_text
        assert "Original Request preserves" in skill_text
        assert "must not weaken user-provided acceptance criteria" in skill_text
        assert "Do not silently reduce scope" in skill_text
        assert "saved goal is the higher-level contract" in skill_text
        assert "Codex Execution Contract" in skill_text
        assert "`Codex Execution Contract` -> `Codex 执行契约`" in skill_text
        assert "Subagent Capacity Prerequisite" in skill_text
        assert "Subagent Dispatch Decision" in skill_text
        assert "Subagent Execution Liberation" in skill_text
        assert "`Subagent Capacity Prerequisite` -> `子代理容量前置`" in skill_text
        assert "`Subagent Dispatch Decision` -> `子代理派发决策`" in skill_text
        assert "`Subagent Execution Liberation` -> `子代理执行力释放`" in skill_text
        assert "L0" in skill_text and "L1" in skill_text and "L2" in skill_text and "L3" in skill_text
        assert "AGENTS.md" in skill_text
        assert "git status --short" in skill_text
        assert "Do not paste the saved goal body back into chat" in skill_text
        assert "Full-spec goals default to subagent-first execution" in skill_text
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
        assert "codex.cmd --strict-config doctor --summary --ascii" in skill_text
        assert "minimum 2 subagents" in skill_text
        assert "minimum 4 subagents" in skill_text
        assert "must not continue as the substitute executor" in skill_text
        assert "lint_goal_file.py" in skill_text
        assert "install_local.py" in skill_text
        assert "check_eval_cases.py" in skill_text

    print("smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
