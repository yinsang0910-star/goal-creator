---
name: goal-creator
description: Create concise saved goal files for Codex, Claude Code, Gemini, Cursor/Windsurf/Cline, GitHub issues, and generic Markdown. Use when the user asks to create, shorten, refine, save, version, or multi-format an agent goal, /goal command, objective, task spec, or goal file.
---

# Goal Creator

Turn a user's task into a compact goal file and save it under the current project's `.goals/` directory.

## Defaults

- Follow the user's language for goal content.
- Use ASCII field labels for stability: `Objective`, `Verify`, `Boundaries`, `Stop`, `Pause`.
- Save automatically unless the target directory is unclear or unsafe.
- Default formats: `codex` and `markdown`.
- If the user asks for all/mainstream formats, include: `codex`, `claude`, `gemini`, `cursor`, `github`, `markdown`.
- Keep normal goals under 12 lines per rendered block.
- Ask at most one question only when the missing answer changes risk, ownership, cost, or write location.

## Goal Shape

Use one canonical goal, then render it into requested formats.

Canonical fields:

- `title`: short noun phrase
- `objective`: one concrete outcome
- `verify`: 2-5 runnable checks, artifacts, screenshots, or review evidence
- `boundaries`: 1-4 write scopes and explicit no-touch areas
- `stop`: one completion condition
- `pause`: one human/external blocker condition
- `notes`: optional assumptions, only when useful

Do not include boilerplate iteration policy unless the task is high risk. For high-risk work such as money, trading, security, production data, destructive operations, or credentials, add one extra `Risk` or `Safety` section.

## Renderers

### codex

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

Use the saved file as the Markdown format. Include frontmatter, canonical goal, and rendered blocks.

## Saving

Use `scripts/save_goal.py` from this skill directory when available:

```bash
python scripts/save_goal.py --title "<title>" --format codex --format markdown < goal.txt
```

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
