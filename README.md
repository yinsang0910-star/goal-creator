# goal-creator

Creates copyable goals and, only when explicitly requested, resumable `.goals/*.md` contracts.

Ordinary requests stay compact and in chat. Unsaved full-spec stays inline and never points to a saved path. Full-spec is reserved for explicit requests or work whose risk/length needs a complete contract. Saving is never implicit.

Saved contracts use stable `goal:*` markers, remain subordinate to `AGENTS.md`, project authority docs, current code, and fresh runtime evidence, and never prescribe agent counts or global Codex configuration.

## Install

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
cd .\goal-creator
python scripts\install_local.py
```

The installer validates the package, backs up only the existing `goal-creator` installation, and replaces only `~/.agents/skills/goal-creator`.

## Use

```text
Create a /goal for this README fix.
```

```text
Create and save a resumable full-spec goal for this production migration.
```

```text
Review this goal for stale authority, weak verification, hidden writes, or forced agent orchestration.
```

## Check

```powershell
python scripts\smoke_test.py
python scripts\lint_goal_file.py examples\full-spec-goal.md
git diff --check
```

## 中文

普通任务默认返回简短、可复制的目标文本；未保存的 full-spec 保持 inline，不能指向保存路径。只有用户明确要求保存、持久化、目标文件或可恢复契约时，才写入 `.goals/*.md`。full-spec 仅用于明确要求或确实需要完整风险契约的任务。

保存的 goal 使用稳定 `goal:*` 标记，并明确服从 `AGENTS.md`、项目当前正本、最新代码和 runtime evidence；不规定 agent 数量，不修改全局 Codex 配置。
