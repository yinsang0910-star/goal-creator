---
name: goal-creator
description: Create concise launcher commands plus complete saved goal files for Codex, Claude Code, Gemini, Cursor/Windsurf/Cline, GitHub issues, and generic Markdown. Trigger when the user says create goal, make a goal, write a goal, save a goal, goal command, /goal, objective file, task objective, execution goal, 创建goal, 创建目标, 生成目标, 写目标, 保存目标, 目标指令, goal指令, 目标文件, 工作目标, 执行目标, or asks to turn a vague task into an agent-executable goal.
---

# Goal Creator

Turn a user's task into a short manual launcher plus a complete goal spec saved under the current project's `.goals/` directory. Create the goal only; do not execute it unless the user separately asks to run it.

## Defaults

- Follow the user's language for goal content.
- Use ASCII field labels for stability: `Objective`, `Verify`, `Boundaries`, `Stop`, `Pause`.
- Save automatically unless the target directory is unclear or unsafe.
- Default mode: `full-spec`.
- Default formats: `codex` and `markdown`.
- If the user asks for all/mainstream formats, include: `codex`, `claude`, `gemini`, `cursor`, `github`, `markdown`.
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

Do not trigger for ordinary planning unless the user wants a saved goal, `/goal` command, objective file, or agent-executable task contract.

## Modes

### full-spec (default)

Use this for most real work.

- The returned `/goal` or task prompt is a short manual launcher for the user to run later.
- The saved `.goals/*.md` file is the complete execution contract.
- The short command must only point to the saved file and say to execute only that file.
- After creating the file, do not execute the short command.

Codex launcher:

```text
/goal Read `.goals/<file>.md`; execute only that file.
```

Saved file structure:

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
/goal Read `.goals/<file>.md`; execute only that file.
```

## Objective

<one concrete outcome>

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

## Stop

- ...

## Pause

- ...
```

Quality bar before saving:

- Objective names one concrete outcome and the main artifact or behavior change.
- Success Criteria has 3-6 observable bullets, including the user-visible result.
- Scope has both Allowed and Forbidden bullets when the task touches code, files, data, money, credentials, or deployment.
- Execution Plan has 4-8 ordered steps that a fresh agent can follow without guessing.
- Verification has 2-5 runnable commands, artifact checks, screenshots, or review evidence.
- Safety / Constraints names no-touch areas and any destructive, credential, production, trading, privacy, or cost risks.
- Stop is a concrete completion evidence, not "when done".
- Pause names the first human or external blocker that should stop the agent.

### compact

Use only when the user asks for a small inline goal or the task is trivial.

Keep normal compact rendered blocks under 12 lines.

## Canonical Fields

Use one canonical goal, then render it into requested formats.

Canonical fields:

- `title`: short noun phrase
- `objective`: one concrete outcome
- `verify`: 2-5 runnable checks, artifacts, screenshots, or review evidence
- `boundaries`: 2-6 write scopes and explicit no-touch areas
- `stop`: one completion condition
- `pause`: one human/external blocker condition
- `notes`: optional assumptions, only when useful

For `full-spec`, include enough detail that a new agent can execute from the saved file alone: execution plan, verification, safety/constraints, iteration policy, stop, and pause. For high-risk work such as money, trading, security, production data, destructive operations, or credentials, make safety explicit.

## Renderers

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
/goal Read `.goals/<file>.md`; execute only that file.
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
