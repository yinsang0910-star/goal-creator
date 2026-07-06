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
  <a href="#中文">中文</a> ·
  <a href="#日本語">日本語</a> ·
  <a href="#한국어">한국어</a>
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
Full-spec goals include a multi-agent-first collaboration contract with slice ownership, subagent deliverables, merge policy, and rejection conditions.
It can also create a Codex subagent capacity setup goal for `~/.codex/config.toml` when requested.
Creating a goal does not execute it. Paste or invoke the returned launcher only when you want the agent to start.

### What It Does

- Creates concise launcher commands from plain-language requests.
- Saves full execution specs for detailed work.
- Saves goals into the current project under `.goals/`.
- Follows the user's language for headings and prose.
- Adds multi-agent coordination rules to full-spec goals by default.
- Adds Codex subagent capacity setup instructions when requested.
- Renders mainstream agent formats:
  - Codex `/goal`
  - Claude Code
  - Gemini / Antigravity
  - Cursor / Windsurf / Cline
  - GitHub issue
  - Generic Markdown

### Beginner Quick Start

1. Clone and copy this repo into your shared skills folder:

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
Copy-Item -Recurse .\goal-creator $env:USERPROFILE\.agents\skills\goal-creator
```

2. Restart your agent.

3. Ask:

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

Create a goal that also prepares Codex subagent capacity:

```text
Use goal-creator to create and save a goal for configuring Codex subagent concurrency.
```

Run a saved goal later:

```text
/goal Read `.goals/<file>.md`; execute only that file.
```

Full-spec goals include multi-agent coordination by default. The executing main session must try substantial low-conflict slices first, consume each subagent handoff, merge serially, and run final project-level verification.

### Example Output

```text
Saved: .goals/2026-06-20-refactor-backtest-module.md

/goal Read `.goals/2026-06-20-refactor-backtest-module.md`; execute only that file.
```

The saved file contains the original request, non-negotiables, full objective, success criteria, scope, execution plan, verification, safety constraints, stop condition, and pause condition.

---

## 中文

`goal-creator` 是一个给 AI 编程 Agent 用的小工具：把模糊需求变成短启动命令和完整目标文件。

你可以把它理解成“任务翻译器”：

```text
“帮我把回测模块整理一下”
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
一条短启动命令 + 一份 Codex / Claude / Gemini / Cursor / GitHub 都看得懂的完整目标文件
```

它不把又长又厚的提示词合同塞进聊天框。聊天里的 `/goal` 保持短，完整流程放进 `.goals/*.md`。
它会保留原始需求，避免后续执行时悄悄降低验收标准。
非英文目标会保持同一种目标语言，包括标题、字段标签、启动命令和正文。
full-spec 目标默认加入多代理优先协同契约，明确切片归属、子代理交付物、合并策略和拒绝条件。
用户需要时，也可以生成调整 `~/.codex/config.toml` 的 Codex 子代理并发配置目标。
创建目标不会自动执行目标。只有当你粘贴或调用返回的启动命令时，Agent 才开始执行。

### 它能做什么

- 把自然语言需求压缩成短启动命令。
- 把完整执行流程保存成目标文件。
- 自动保存到当前项目的 `.goals/` 目录。
- 标题和正文都跟随用户语言输出。
- full-spec 目标默认加入多代理协同规则。
- 按需加入 Codex 子代理并发上限配置步骤。
- 支持主流 Agent 格式：
  - Codex `/goal`
  - Claude Code
  - Gemini / Antigravity
  - Cursor / Windsurf / Cline
  - GitHub issue
  - 通用 Markdown

### 小白快速开始

1. 克隆仓库，并复制到共享 skills 目录：

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
Copy-Item -Recurse .\goal-creator $env:USERPROFILE\.agents\skills\goal-creator
```

2. 重启你的 Agent。

3. 直接说：

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

创建 Codex 子代理并发配置目标：

```text
用 goal-creator 创建并保存一个配置 Codex 子代理并发上限的目标。
```

之后执行已保存的目标：

```text
/goal 读取 `.goals/<file>.md`；只执行该文件。
```

full-spec 目标默认包含多代理协同规则。未来执行的主会话必须先尝试拆分实质性、低冲突切片，消费每个子代理交接结果，串行合并，并运行最终项目级验证。

### 输出长什么样

```text
Saved: .goals/2026-06-20-refactor-backtest-module.md

/goal Read `.goals/2026-06-20-refactor-backtest-module.md`; execute only that file.
```

原始需求、不可降级项、完整目标、成功标准、范围、执行计划、验证方式、安全约束、停止条件和暂停条件都保存在目标文件里。

---

## 日本語

`goal-creator` は、あいまいな作業依頼を短い起動コマンドと完全なゴールファイルに変換する AI コーディング Agent 向けの skill です。

イメージは、小さな「ミッション作成係」です。

```text
「バックテスト機能を整理して」
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
短い起動コマンド + Codex / Claude / Gemini / Cursor / GitHub で使える完全なゴール仕様
```

長すぎるプロンプト契約書をチャット欄に詰め込みません。短いコマンドで開始し、詳細は `.goals/*.md` に保存します。
ゴールを作成しても自動実行はしません。返された起動コマンドを貼り付けたときだけ実行が始まります。

### できること

- 普通の文章から短い起動コマンドを作ります。
- 詳細な実行仕様をゴールファイルとして保存します。
- 現在のプロジェクトの `.goals/` に保存します。
- ユーザーの言語に合わせます。
- 主な Agent 形式に対応します：
  - Codex `/goal`
  - Claude Code
  - Gemini / Antigravity
  - Cursor / Windsurf / Cline
  - GitHub issue
  - 汎用 Markdown

### 初心者向けクイックスタート

1. このリポジトリを clone して、shared skills フォルダへコピーします：

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
Copy-Item -Recurse .\goal-creator $env:USERPROFILE\.agents\skills\goal-creator
```

2. Agent を再起動します。

3. 次のように依頼します：

```text
Use goal-creator to create and save a compact goal for refactoring the backtest module.
```

すべての主要形式が必要な場合：

```text
Use goal-creator to create a saved multi-format goal for building my first MVP.
```

インストール後の確認：

```text
Use goal-creator to create and save a full-spec goal for a small README update.
```

`.goals/` に新しいファイルが作成されれば成功です。

### 出力例

```text
Saved: .goals/2026-06-20-refactor-backtest-module.md

/goal Read `.goals/2026-06-20-refactor-backtest-module.md`; execute only that file.
```

完全な目的、成功条件、スコープ、実行計画、検証方法、安全制約、停止条件、一時停止条件は保存されたゴールファイルに入ります。

---

## 한국어

`goal-creator`는 모호한 작업 요청을 짧은 실행 명령과 완전한 goal 파일로 바꿔 주는 AI 코딩 Agent용 skill입니다.

작은 “미션 정리 담당자”라고 생각하면 됩니다.

```text
"백테스트 모듈 좀 정리해줘"
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
짧은 실행 명령 + Codex / Claude / Gemini / Cursor / GitHub에서 쓸 수 있는 완전한 goal spec
```

길고 무거운 프롬프트 계약서를 채팅창에 넣지 않습니다. 채팅 명령은 짧게 유지하고, 자세한 실행 계획은 `.goals/*.md`에 저장합니다.
goal을 만든다고 바로 실행되지는 않습니다. 반환된 실행 명령을 붙여 넣거나 호출할 때만 Agent가 시작합니다.

### 무엇을 하나요

- 자연어 요청을 짧은 실행 명령으로 바꿉니다.
- 자세한 실행 spec을 goal 파일로 저장합니다.
- 현재 프로젝트의 `.goals/` 디렉터리에 저장합니다.
- 사용자의 언어를 따라갑니다.
- 주요 Agent 형식을 지원합니다:
  - Codex `/goal`
  - Claude Code
  - Gemini / Antigravity
  - Cursor / Windsurf / Cline
  - GitHub issue
  - 일반 Markdown

### 초보자 빠른 시작

1. 이 저장소를 clone한 뒤 shared skills 폴더에 복사합니다:

```powershell
git clone https://github.com/yinsang0910-star/goal-creator.git
Copy-Item -Recurse .\goal-creator $env:USERPROFILE\.agents\skills\goal-creator
```

2. Agent를 다시 시작합니다.

3. 이렇게 요청합니다:

```text
Use goal-creator to create and save a compact goal for refactoring the backtest module.
```

모든 주요 형식이 필요하다면:

```text
Use goal-creator to create a saved multi-format goal for building my first MVP.
```

설치 후 확인:

```text
Use goal-creator to create and save a full-spec goal for a small README update.
```

`.goals/` 아래에 새 파일이 생기면 정상입니다.

### 출력 예시

```text
Saved: .goals/2026-06-20-refactor-backtest-module.md

/goal Read `.goals/2026-06-20-refactor-backtest-module.md`; execute only that file.
```

전체 목표, 성공 기준, 범위, 실행 계획, 검증 방법, 안전 제약, 중지 조건, 일시 중지 조건은 저장된 goal 파일에 들어갑니다.
