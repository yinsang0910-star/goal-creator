---
title: Create goal-creator skill
created: 2026-06-20
status: draft
language: en
formats:
  - codex
  - claude
  - gemini
  - cursor
  - github
  - markdown
---

# Create goal-creator skill

## Canonical Goal

Objective:
Create the first working version of `goal-creator`, a concise multi-format goal skill that saves Markdown goal files under `.goals/`.

Verify:
- Inspect one existing goal skill for scope, not text reuse.
- Create `SKILL.md`, `scripts/save_goal.py`, README, and one example.
- Run the save script once and confirm a `.goals/*.md` file is created.

Boundaries:
- Write only inside the `goal-creator` repository.
- Do not modify installed skills or global agent config during implementation.

Stop:
- The skill files exist and the save script produces a valid goal file.

Pause:
- Publishing credentials, repo ownership, or license changes are required.

## Codex

```text
/goal Create the first working version of `goal-creator`, a concise multi-format goal skill that saves Markdown goal files under `.goals/`.

Verify:
- Inspect one existing goal skill for scope, not text reuse.
- Create `SKILL.md`, `scripts/save_goal.py`, README, and one example.
- Run the save script once and confirm a `.goals/*.md` file is created.

Boundaries:
- Write only inside the `goal-creator` repository.
- Do not modify installed skills or global agent config during implementation.

Stop:
- The skill files exist and the save script produces a valid goal file.

Pause:
- Publishing credentials, repo ownership, or license changes are required.
```

## GitHub Issue

```markdown
## Objective

Create the first working version of `goal-creator`, a concise multi-format goal skill that saves Markdown goal files under `.goals/`.

## Acceptance Criteria

- `SKILL.md`, `scripts/save_goal.py`, README, and one example exist.
- The save script writes a `.goals/*.md` file.
- No installed skills or global agent config are modified.
```
