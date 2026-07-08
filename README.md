<p align="center">
  <img src="assets/icon.svg" width="128" height="128" alt="goal-creator icon">
</p>

<h1 align="center">goal-creator</h1>

<p align="center">
  A concise goal maker for AI coding agents.
  <br>
  Keep the chat command short. Put the full plan in a saved goal file.
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="#中文">中文</a>
</p>

<p align="center">
  <code>codex</code>
  <code>claude-code</code>
  <code>gemini</code>
  <code>cursor</code>
  <code>windsurf</code>
  <code>cline</code>
  <code>github-issues</code>
  <code>markdown</code>
  <code>ai-agents</code>
  <code>goal-management</code>
</p>

---

## English

`goal-creator` is a small skill for turning vague work into compact commands plus complete saved goals.

Think of it as a tidy little mission writer:

```text
"Please improve the backtest module"
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
A short launcher plus a complete Codex / Claude / Gemini / Cursor / GitHub-ready goal spec
```

It avoids giant chat prompts. The chat command stays short; the saved `.goals/*.md` file keeps the full plan.
It also preserves the original request so later execution cannot quietly weaken the acceptance bar.
For non-English goals, headings, labels, launcher wording, and prose stay in the target language.
Full-spec goals include a Codex execution contract, subagent capacity prerequisite, L0/L1/L2/L3 dispatch decision, execution-liberation contract, dispatch matrix, shared file ownership, fixed subagent result template, merge policy, and rejection conditions.
Before relying on full-spec subagent execution, configure Codex agents in `~/.codex/config.toml`.
Creating a goal does not execute it. Paste or invoke the returned launcher only when you want the agent to start.

### What It Does

- Creates concise launcher commands from plain-language requests.
- Saves full execution specs for detailed work.
- Saves goals into the current project under `.goals/`.
- Follows the user's language for headings and prose.
- Adds subagent-first execution rules to full-spec goals by default.
- Requires Codex subagent capacity setup before subagent-first execution.
- Renders mainstream agent formats:
  - Codex `/goal`
  - Claude Code
  - Gemini / Antigravity
  - Cursor / Windsurf / Cline
  - GitHub issue
  - Generic Markdown

### Beginner Quick Start

1. Clone and install this skill into your Codex skills folder:

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
cd .\goal-creator
python scripts\install_local.py
```

2. Configure Codex subagent capacity in `~/.codex/config.toml`:

```toml
[agents]
max_threads = 2147483647
max_depth = 2147483647
```

If `[agents]` already exists, update only those fields. Do not delete or reorder existing config.

3. Verify Codex loads the config:

```powershell
codex --strict-config doctor --summary --ascii
```

Confirm `Configuration` / `config` is `loaded`.

4. Restart your agent.

5. Ask:

```text
Use goal-creator to create and save a compact goal for refactoring the backtest module.
```

For every supported format:

```text
Use goal-creator to create a saved multi-format goal for building my first MVP.
```

Post-install check:

```text
Use goal-creator to create and save a full-spec goal for a small README update.
```

You should see a new file under `.goals/`.

### How To Use

Create a normal full-spec goal:

```text
Use goal-creator to create and save a full-spec goal for <your task>.
```

Create a short copyable goal:

```text
Use goal-creator to create a compact goal for <your task>.
```

Review an existing goal:

```text
Use goal-creator to review this goal for missing verification, weak boundaries, language mixing, and multi-agent gaps.
```

Create a standalone goal for preparing another machine's Codex subagent capacity:

```text
Use goal-creator to create and save a goal for configuring Codex subagent concurrency.
```

Run a saved goal later:

```text
/goal Execute only `.goals/<file>.md`.
```

Full-spec goals are subagent-first by default. The executing main session must choose L0/L1/L2/L3, keep simple tasks at L0, delegate real file-owned slices for complex work, define a `Dispatch Matrix`, keep shared files under `Shared File Ownership`, consume each fixed `Subagent Result`, merge serially, and run final project-level verification.

Saved full-spec goals can be checked locally:

```powershell
python scripts\lint_goal_file.py .goals\<file>.md
```

### Example Output

```text
Saved: .goals/2026-06-20-refactor-backtest-module.md

/goal Execute only `.goals/2026-06-20-refactor-backtest-module.md`.
```

The saved file contains the original request, non-negotiables, full objective, success criteria, scope, execution plan, verification, safety constraints, stop condition, and pause condition.

---

## 中文

`goal-creator` 是一个给 AI 编程 Agent 用的小工具：把模糊需求变成启动入口和完整目标文件。

你可以把它理解成“任务翻译器”：

```text
“帮我把回测模块整理一下”
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
一个启动入口 + 一份 Codex / Claude / Gemini / Cursor / GitHub 都看得懂的完整目标文件
```

它不把又长又厚的提示词合同塞进聊天框。聊天里的 `/goal` 保持短，完整流程放进 `.goals/*.md`。
它会保留原始需求，避免后续执行时悄悄降低验收标准。
非英文目标会保持同一种目标语言，包括标题、字段标签、启动命令和正文。
full-spec 目标默认加入 Codex 执行契约、子代理容量前置、L0/L1/L2/L3 派发决策、执行力释放契约、派发表、共享文件归属、固定子代理结果模板、合并策略和拒绝条件。
在依赖 full-spec 子代理执行前，需要先配置 `~/.codex/config.toml`。
创建目标不会自动执行目标。只有当你粘贴或调用返回的启动命令时，Agent 才开始执行。

### 它能做什么

- 把自然语言需求压缩成启动入口。
- 把完整执行流程保存成目标文件。
- 自动保存到当前项目的 `.goals/` 目录。
- 标题和正文都跟随用户语言输出。
- full-spec 目标默认加入 subagent-first 执行规则。
- 使用 subagent-first 执行前要求配置 Codex 子代理并发上限。
- 支持主流 Agent 格式：
  - Codex `/goal`
  - Claude Code
  - Gemini / Antigravity
  - Cursor / Windsurf / Cline
  - GitHub issue
  - 通用 Markdown

### 小白快速开始

1. 克隆仓库，并安装到 Codex skills 目录：

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
cd .\goal-creator
python scripts\install_local.py
```

2. 配置 Codex 子代理容量，修改 `~/.codex/config.toml`：

```toml
[agents]
max_threads = 2147483647
max_depth = 2147483647
```

如果已经有 `[agents]` 段，只更新这两个字段。不要删除或重排现有配置。

3. 验证 Codex 能加载配置：

```powershell
codex --strict-config doctor --summary --ascii
```

确认 `Configuration` / `config` 是 `loaded`。

4. 重启你的 Agent。

5. 直接说：

```text
用 goal-creator 给“重构回测模块”创建并保存一个简洁目标。
```

如果你想同时兼容所有主流格式：

```text
用 goal-creator 给我的第一个 MVP 创建一个多格式目标文件。
```

安装后验证：

```text
用 goal-creator 给一次小型 README 更新创建并保存一个 full-spec 目标。
```

你应该能在 `.goals/` 目录下看到新文件。

### 怎么使用

创建普通 full-spec 目标：

```text
用 goal-creator 为“<你的任务>”创建并保存一个 full-spec 目标。
```

创建短的可复制目标：

```text
用 goal-creator 为“<你的任务>”创建一个 compact 目标。
```

检查已有目标：

```text
用 goal-creator 检查这个 goal 是否缺少验证、边界、暂停条件，是否中英混用，是否缺少多代理协同。
```

为另一台机器创建 Codex 子代理并发配置目标：

```text
用 goal-creator 创建并保存一个配置 Codex 子代理并发上限的目标。
```

之后执行已保存的目标：

```text
/goal 只执行 `.goals/<file>.md`
```

full-spec 目标默认是 subagent-first。未来执行的主会话必须先判断 L0/L1/L2/L3，简单任务保持 L0，复杂任务把真实、文件边界清楚的切片下放给子代理，明确派发表和共享文件归属，消费每个固定格式的子代理结果，串行合并，并运行最终项目级验证。

保存后的 full-spec 目标可以本地检查：

```powershell
python scripts\lint_goal_file.py .goals\<file>.md
```

### 输出长什么样

```text
Saved: .goals/2026-06-20-refactor-backtest-module.md

/goal Execute only `.goals/2026-06-20-refactor-backtest-module.md`.
```

原始需求、不可降级项、完整目标、成功标准、范围、执行计划、验证方式、安全约束、停止条件和暂停条件都保存在目标文件里。
