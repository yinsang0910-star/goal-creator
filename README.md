<p align="center">
  <img src="assets/icon.svg" width="128" height="128" alt="goal-creator icon">
</p>

<h1 align="center">goal-creator</h1>

<p align="center">
  A concise goal maker for AI coding agents.
  <br>
  Turn a fuzzy request into a short goal file your agent can actually finish.
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

`goal-creator` is a small skill for turning vague work into compact, saved goals.

Think of it as a tidy little mission writer:

```text
"Please improve the backtest module"
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
A short Codex / Claude / Gemini / Cursor / GitHub-ready goal
```

It avoids giant prompt contracts. A useful goal needs only enough structure to keep the agent on track.

### What It Does

- Creates concise goals from plain-language requests.
- Saves goals into the current project under `.goals/`.
- Follows the user's language.
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

### Example Output

```text
/goal Refactor the backtest module to reduce duplication while preserving current behavior.

Verify:
- Run the existing backtest-related tests.
- Run one sample backtest command and capture output.
- Confirm no public CLI behavior changed unless explicitly listed.

Boundaries:
- Modify only backtest code and directly related tests.
- Do not change storage schema, live trading code, or credentials.

Stop:
- Tests pass and the sample backtest output is preserved or explained.

Pause:
- Required behavior is ambiguous, credentials are needed, or failures point outside the module.
```

### Tags

Recommended GitHub topics:

```text
ai-agents, codex, claude-code, gemini, cursor, windsurf, cline,
goal-management, agent-tools, prompt-engineering, markdown, github-issues
```

---

## 中文

`goal-creator` 是一个给 AI 编程 Agent 用的小工具：把模糊需求变成简洁、可保存、可执行的目标文件。

你可以把它理解成“任务翻译器”：

```text
“帮我把回测模块整理一下”
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
一份 Codex / Claude / Gemini / Cursor / GitHub 都看得懂的短目标
```

它不喜欢又长又厚的提示词合同。一个好目标只需要让 Agent 知道：做什么、怎么验收、哪里不能碰、什么时候停。

### 它能做什么

- 把自然语言需求压缩成短目标。
- 自动保存到当前项目的 `.goals/` 目录。
- 跟随用户语言输出。
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

### 输出长什么样

```text
/goal 在保持现有行为不变的前提下，重构回测模块以减少重复代码。

Verify:
- 运行现有回测相关测试。
- 运行一次示例回测命令并保存输出。
- 确认公开 CLI 行为没有变化，除非目标中明确列出。

Boundaries:
- 只修改回测代码和直接相关测试。
- 不修改存储 schema、实盘交易代码或凭证。

Stop:
- 测试通过，示例回测输出被保留或差异已说明。

Pause:
- 需求行为不明确、需要凭证，或失败原因指向回测模块之外。
```

### 标签

推荐 GitHub topics：

```text
ai-agents, codex, claude-code, gemini, cursor, windsurf, cline,
goal-management, agent-tools, prompt-engineering, markdown, github-issues
```

---

## 日本語

`goal-creator` は、あいまいな作業依頼を短く実行しやすいゴールファイルに変換する AI コーディング Agent 向けの skill です。

イメージは、小さな「ミッション作成係」です。

```text
「バックテスト機能を整理して」
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
Codex / Claude / Gemini / Cursor / GitHub で使える短いゴール
```

長すぎるプロンプト契約書は作りません。必要なのは、何をするか、どう確認するか、どこを触らないか、いつ止まるかです。

### できること

- 普通の文章からコンパクトなゴールを作ります。
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

### 出力例

```text
/goal 既存の動作を保ったまま、バックテストモジュールの重複を減らす。

Verify:
- 既存のバックテスト関連テストを実行する。
- サンプルのバックテストコマンドを 1 回実行して出力を保存する。
- 明示されていない CLI の挙動変更がないことを確認する。

Boundaries:
- バックテストコードと直接関連するテストだけを変更する。
- ストレージ schema、ライブ取引コード、認証情報は変更しない。

Stop:
- テストが通り、サンプル出力が保たれるか差分が説明されている。

Pause:
- 仕様があいまい、認証情報が必要、または失敗原因が対象外にある。
```

### Tags

おすすめ GitHub topics：

```text
ai-agents, codex, claude-code, gemini, cursor, windsurf, cline,
goal-management, agent-tools, prompt-engineering, markdown, github-issues
```

---

## 한국어

`goal-creator`는 모호한 작업 요청을 짧고 실행 가능한 goal 파일로 바꿔 주는 AI 코딩 Agent용 skill입니다.

작은 “미션 정리 담당자”라고 생각하면 됩니다.

```text
"백테스트 모듈 좀 정리해줘"
        ↓
.goals/2026-06-20-refactor-backtest-module.md
        ↓
Codex / Claude / Gemini / Cursor / GitHub에서 바로 쓸 수 있는 짧은 goal
```

길고 무거운 프롬프트 계약서를 만들지 않습니다. 좋은 goal에는 무엇을 할지, 어떻게 확인할지, 어디를 건드리지 말지, 언제 멈출지만 있으면 충분합니다.

### 무엇을 하나요

- 자연어 요청을 간결한 goal로 바꿉니다.
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

### 출력 예시

```text
/goal 기존 동작을 유지하면서 백테스트 모듈의 중복을 줄인다.

Verify:
- 기존 백테스트 관련 테스트를 실행한다.
- 샘플 백테스트 명령을 한 번 실행하고 출력을 저장한다.
- 명시하지 않은 공개 CLI 동작 변경이 없는지 확인한다.

Boundaries:
- 백테스트 코드와 직접 관련된 테스트만 수정한다.
- 저장소 schema, 라이브 트레이딩 코드, 인증 정보는 변경하지 않는다.

Stop:
- 테스트가 통과하고 샘플 출력이 유지되거나 차이가 설명된다.

Pause:
- 요구사항이 모호하거나, 인증 정보가 필요하거나, 실패 원인이 범위 밖에 있다.
```

### Tags

추천 GitHub topics:

```text
ai-agents, codex, claude-code, gemini, cursor, windsurf, cline,
goal-management, agent-tools, prompt-engineering, markdown, github-issues
```
