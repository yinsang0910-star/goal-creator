---
name: goal-creator
description: Create concise launcher commands plus complete saved goal files for Codex, Claude Code, Gemini, Cursor/Windsurf/Cline, GitHub issues, and generic Markdown. Trigger when the user says create goal, make a goal, write a goal, save a goal, goal command, /goal, objective file, task objective, execution goal, 创建goal, 创建目标, 生成目标, 写目标, 保存目标, 目标指令, goal指令, 目标文件, 工作目标, 执行目标, or asks to turn a vague task into an agent-executable goal.
---

# Goal Creator

Turn a user's task into a short manual launcher plus a complete goal spec saved under the current project's `.goals/` directory. Create the goal only; do not execute it unless the user separately asks to run it.

## Defaults

- Follow the user's language for goal content, including headings, launcher wording, and saved-file prose.
- Use canonical field names internally for stability, but render visible field labels in the target language.
- Keep only command names, file paths, code identifiers, format names, and proper nouns in their original language.
- Do not mix English labels into a non-English goal unless the user explicitly asks for English.
- Save automatically unless the target directory is unclear or unsafe.
- Default mode: `full-spec`.
- Default formats: `codex` and `markdown`.
- If the user asks for all/mainstream formats, include: `codex`, `claude`, `gemini`, `cursor`, `github`, `markdown`.
- Use `compact` when the user asks for a short inline goal, direct copyable `/goal`, or a trivial task.
- Use `review` when the user asks to inspect, audit, compare, improve, lint, or fix an existing goal.
- Full-spec goals default to forced subagent dispatch: include the dispatch protocol contract and require the future main session to define real parallel slices before implementation.
- If the user asks to configure Codex subagent concurrency or capacity, include the Codex subagent capacity setup contract.
- Keep the chat command under 140 characters when possible. Put all detail in the saved goal file.
- Creation is manual by default: output and save the goal, but do not start the work described by the goal.
- Ask at most one question only when the missing answer changes risk, ownership, cost, or write location.

## Trigger Examples

Use this skill for requests like:

- `create a goal for this task`
- `make a /goal for the refactor`
- `save this as a goal file`
- `turn this plan into an execution goal`
- `创建 goal`
- `创建目标`
- `生成目标文件`
- `写一个目标指令`
- `把这个任务变成可执行目标`
- `检查这个 goal`
- `review this goal`
- `lint goal`

Do not trigger for ordinary planning unless the user wants a saved goal, `/goal` command, objective file, or agent-executable task contract.

## Modes

### full-spec (default)

Use this for most real work.

- The returned `/goal` or task prompt is a short manual launcher for the user to run later.
- The saved `.goals/*.md` file is the complete execution contract.
- The short command must only point to the saved file and say to execute only that file in the target language.
- After creating the file, do not execute the short command.

Codex launcher examples:

English:

```text
/goal Execute only `.goals/<file>.md`.
```

Chinese:

```text
/goal 只执行 `.goals/<file>.md`
```

Saved file structure (English example; translate all visible labels for non-English goals):

```markdown
---
title: <title>
created: <date>
status: draft
language: <language>
mode: full-spec
formats:
  - codex
  - markdown
---

# <title>

## Short Command

```text
/goal Execute only `.goals/<file>.md`.
```

## Objective

<one concrete outcome that preserves the user's original intent>

## Original Request

<the user's requested outcome/design intent, kept without narrowing>

## Non-Negotiables

- ...

## Success Criteria

- ...

## Scope

Allowed:
- ...

Forbidden:
- ...

## Execution Plan

1. ...

## Verification

- ...

## Safety / Constraints

- ...

## Iteration Policy

- ...

## Multi-Agent Collaboration

- Main session freezes the original goal, success criteria, non-negotiables, shared interfaces, and file boundaries before dispatch.
- Main session attempts to delegate at least two substantial, low-conflict, parallelizable vertical slices before implementation.
- Main session owns scheduling, shared files, conflict handling, merge decisions, and final project-level verification.
- Subagents may decompose implementation but must not weaken the saved goal contract.

## Dispatch Matrix

| Slice | Agent Role | Goal | Allowed Files | Forbidden Files | Inputs | Required Output | Verify | Depends On | Merge Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| implementation | subagent | ... | ... | ... | ... | changed files, verification command, result, risk, handoff | ... | none | main session |
| verification | subagent | ... | ... | ... | ... | changed files, verification command, result, risk, handoff | ... | implementation | main session |

## Shared File Ownership

Main-session-owned:
- ...

Subagent-owned:
- ...

## Subagent Result

Slice:
Status: adopted | needs-main-merge | blocked | rejected
Changed Files:
Verification Run:
Verification Result:
Boundary Crossings:
Risks:
Handoff:

## Merge Policy

- Dispatch independent slices first.
- Merge subagent results serially.
- Keep shared files under main-session ownership unless a slice explicitly allows them.
- Adopt, adapt with explanation, or reject each subagent result; do not bypass completed subagent work silently.

## Rejection Conditions

- Changes files outside the allowed range.
- Omits verification results.
- Weakens the original goal, success criteria, or non-negotiables.
- Conflicts with frozen interfaces or design direction.
- Cannot be understood or merged from the handoff.

## Stop

- ...

## Pause

- ...
```

Chinese label map:

- `Short Command` -> `启动入口`
- `Objective` -> `目标`
- `Original Request` -> `原始需求`
- `Non-Negotiables` -> `不可降级项`
- `Success Criteria` -> `成功标准`
- `Scope` -> `范围`
- `Allowed` -> `允许`
- `Forbidden` -> `禁止`
- `Execution Plan` -> `执行计划`
- `Verification` -> `验证`
- `Safety / Constraints` -> `安全 / 约束`
- `Iteration Policy` -> `迭代策略`
- `Multi-Agent Collaboration` -> `多代理协同`
- `Dispatch Matrix` -> `派发表`
- `Shared File Ownership` -> `共享文件归属`
- `Subagent Result` -> `子代理结果`
- `Merge Policy` -> `合并策略`
- `Rejection Conditions` -> `拒绝条件`
- `Codex Subagent Capacity Setup` -> `Codex 子代理并发配置`
- `Slice` -> `切片`
- `Agent Role` -> `代理角色`
- `Goal` -> `目标`
- `Allowed Files` -> `允许文件`
- `Forbidden Files` -> `禁止文件`
- `Inputs` -> `输入`
- `Required Output` -> `必交输出`
- `Verify` -> `验证`
- `Depends On` -> `依赖`
- `Merge Owner` -> `合并负责人`
- `Changed files` -> `改动文件`
- `Verification Run` -> `验证命令`
- `Verification Result` -> `验证结果`
- `Boundary Crossings` -> `越界情况`
- `Risks` -> `风险`
- `Handoff` -> `交接说明`
- `Stop` -> `停止`
- `Pause` -> `暂停`

Quality bar before saving:

- Use one target language for all visible headings and prose. Exceptions: command names, file paths, code identifiers, format names, and proper nouns.
- For non-English goals, translate labels and launcher wording; do not keep English headings like `Objective`, `Success Criteria`, `Allowed`, or `Forbidden`.
- Objective names one concrete outcome and the main artifact or behavior change, without replacing the user's request with a smaller substitute.
- Original Request preserves the user's requested outcome/design intent before any agent decomposition.
- Non-Negotiables lists user-provided acceptance criteria, design requirements, no-touch boundaries, and must-keep behaviors.
- Success Criteria has 3-6 observable bullets, including the user-visible result, and must not weaken user-provided acceptance criteria.
- Scope has both Allowed and Forbidden bullets when the task touches code, files, data, money, credentials, or deployment.
- Execution Plan has 4-8 ordered steps that a fresh agent can follow without guessing.
- Verification has 2-5 runnable commands, artifact checks, screenshots, or review evidence that test the requested outcome, not only a reduced implementation.
- Safety / Constraints names no-touch areas and any destructive, credential, production, trading, privacy, or cost risks.
- Stop is a concrete completion evidence, not "when done".
- Pause names the first human or external blocker that should stop the agent.
- Do not silently reduce scope. If constraints require a smaller first step, keep the full request in `Original Request`, put the reduction in `Pause` or assumptions needing confirmation, and do not present the reduced scope as the final goal.
- When used with planning, TDD, verification, or superpowers workflows, the saved goal is the higher-level contract: later skills may decompose execution, but must not weaken `Objective`, `Non-Negotiables`, `Success Criteria`, or `Verification`.
- Full-spec goals include `Multi-Agent Collaboration`, `Dispatch Matrix`, `Shared File Ownership`, `Subagent Result`, `Merge Policy`, and `Rejection Conditions` by default.
- The dispatch protocol requires at least two substantial low-conflict slices when possible, and puts unsplittable work in `Pause` instead of inventing fake parallel work.
- Subagents must not be used only for simple reading, summarizing, searching, formatting, or one tiny function.

### Dispatch protocol default

Use this by default for `full-spec` goals.

The future executing main session must first split work into at least two substantial, low-conflict, parallelizable vertical slices before implementation. If the work cannot be split, say so in `Pause` instead of inventing fake parallel work.

Include these sections in the saved full-spec goal:

```markdown
## Multi-Agent Collaboration

- Main session freezes the original goal, success criteria, non-negotiables, shared interfaces, and file boundaries before dispatch.
- Main session delegates at least two substantial low-conflict slices when the task is actually parallelizable.
- Main session owns scheduling, shared files, conflict handling, merge decisions, and final project-level verification.
- Subagents may decompose implementation but must not weaken the saved goal contract.

## Dispatch Matrix

| Slice | Agent Role | Goal | Allowed Files | Forbidden Files | Inputs | Required Output | Verify | Depends On | Merge Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract/interface | subagent | ... | ... | ... | ... | changed files, verification command, result, risk, handoff | ... | none | main session |
| implementation | subagent | ... | ... | ... | ... | changed files, verification command, result, risk, handoff | ... | contract/interface | main session |

Allowed slice types: `contract/interface`, `implementation`, `verification`, `docs/handoff`, `config/tooling`.

## Shared File Ownership

Main-session-owned:
- shared interfaces, global docs, release notes, and files edited by multiple slices

Subagent-owned:
- files explicitly listed in that row's `Allowed Files`

## Subagent Result

Slice:
Status: adopted | needs-main-merge | blocked | rejected
Changed Files:
Verification Run:
Verification Result:
Boundary Crossings:
Risks:
Handoff:

## Merge Policy

- Dispatch independent slices first.
- Merge subagent results serially.
- Shared files are edited by the main session unless the slice explicitly allows them.
- Do not bypass completed subagent work and reimplement it silently; adopt it, adapt it with explanation, or reject it with cause.
- On conflict, narrow boundaries or move the shared-file work back to the main session.
- Consume each `Subagent Result` before merging, then run final project-level tests/builds after all adopted work is merged.

## Rejection Conditions

Reject or return a subagent result if it:
- Changes files outside its allowed range
- Omits verification results
- Reports failed verification without a risk explanation
- Weakens the original goal, success criteria, or non-negotiables
- Conflicts with frozen interfaces or design direction
- Cannot be understood or merged from the handoff
```

### Codex subagent capacity setup

Use this when the user asks to configure Codex subagents, raise subagent limits, tune concurrency, or prepare the environment for high-parallel multi-agent execution. Do not add this global-config step to ordinary implementation goals unless requested.

The saved goal must require:

1. Modify the current user's Codex global config file: `~/.codex/config.toml`.
2. If `[agents]` exists, update only these fields inside it; if not, append:

```toml
[agents]
max_threads = 2147483647
max_depth = 2147483647
```

3. Do not delete or reorder existing config.
4. Run:

```bash
codex --strict-config doctor --summary --ascii
```

5. Verify the output shows `Configuration` / `config` is `loaded`.

### compact

Use only when the user asks for a small inline goal or the task is trivial.

Keep normal compact rendered blocks under 12 lines. For compact mode, prioritize a direct copyable command over a saved full-spec file unless the user asks to save it.

### review

Use when the user provides an existing goal and asks to review, inspect, compare, improve, lint, or fix it.

Check for:

- Missing original request, non-negotiables, success criteria, verification, scope, stop, or pause.
- Silent scope reduction or weakened acceptance criteria.
- Over-broad boundaries or missing no-touch areas.
- Missing multi-agent sections in a full-spec goal.
- English headings or labels inside a non-English goal.
- Long launcher, placeholders, vague verification, or fake parallel work.

Return findings first, then a corrected goal only if the user asks for one or the fix is small.

## Canonical Fields

Use one canonical goal, then render it into requested formats. Canonical field names are internal; visible labels must follow the target language.

Canonical fields:

- `title`: short noun phrase
- `original_request`: the user's requested outcome/design intent, not narrowed
- `objective`: one concrete outcome that preserves the original request
- `non_negotiables`: user-provided acceptance criteria, design requirements, no-touch boundaries, and must-keep behaviors
- `verify`: 2-5 runnable checks, artifacts, screenshots, or review evidence
- `boundaries`: 2-6 write scopes and explicit no-touch areas
- `stop`: one completion condition
- `pause`: one human/external blocker condition
- `notes`: optional assumptions, only when useful

For `full-spec`, include enough detail that a new agent can execute from the saved file alone: execution plan, verification, safety/constraints, iteration policy, stop, and pause. For high-risk work such as money, trading, security, production data, destructive operations, or credentials, make safety explicit.

## Renderers

Renderer snippets are English defaults. Translate visible labels for non-English targets before returning or saving output.

### codex

Compact form:

```text
/goal <objective>

Verify:
- ...

Boundaries:
- ...

Stop:
- ...

Pause:
- ...
```

Full-spec launcher:

```text
/goal Execute only `.goals/<file>.md`.
```

### claude

```text
Objective: <objective>

Acceptance checks:
- ...

Constraints:
- ...

Done when:
- ...

Pause if:
- ...
```

### gemini

```text
Goal: <objective>

Success criteria:
- ...

Constraints:
- ...

Stop when:
- ...

Ask before continuing if:
- ...
```

### cursor

```text
Task: <objective>

Implement only:
- ...

Verify with:
- ...

Do not change:
- ...

Stop when:
- ...
```

### github

```markdown
## Objective

<objective>

## Acceptance Criteria

- ...

## Scope

- ...

## Out of Scope / Pause Conditions

- ...
```

### markdown

Use the saved file as the Markdown format. In `full-spec` mode, include frontmatter, `Short Command`, and the complete execution spec.

## Saving

Use `scripts/save_goal.py` from this skill directory when available:

```bash
python scripts/save_goal.py --title "<title>" --mode full-spec --format codex --format markdown < goal.txt
```

Resolve `scripts/save_goal.py` relative to this `SKILL.md` file, but run it from the user's current project directory so `.goals/` is created in that project.

The script writes to `.goals/YYYY-MM-DD-slug.md` in the current working directory. It creates `.goals/` if needed and avoids overwriting by appending `-2`, `-3`, etc.

If the script is unavailable, create the same file manually.

After saving a full-spec goal, validate it with `scripts/lint_goal_file.py` when available:

```bash
python scripts/lint_goal_file.py .goals/<file>.md
```

Use `scripts/check_eval_cases.py` after editing `examples/evals/cases.json`.

Use `scripts/install_local.py` to install or update this skill in the current user's Codex skills directory:

```bash
python scripts/install_local.py
```

## Response

After saving, return only:

````text
Saved: .goals/<file>.md

```text
<primary rendered block>
```
````

Add one short note only if a risky assumption was made.

Do not continue into implementation. The user must paste or invoke the returned launcher when they want execution to begin.
