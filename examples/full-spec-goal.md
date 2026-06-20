---
title: Goal Creator v0.2
created: 2026-06-20
status: draft
language: en
mode: full-spec
formats:
  - codex
  - markdown
---

# Goal Creator v0.2

## Short Command

```text
/goal Read `.goals/2026-06-20-goal-creator-v0-2.md` first, then execute only the work defined there. Follow its Objective, Scope, Verification, Safety, Iteration, Stop, and Pause sections. Stop only when the file's completion evidence is satisfied; pause if any pause condition is met.
```

## Objective

Upgrade `goal-creator` so the chat command stays short while the saved `.goals/*.md` file carries the full execution contract.

## Success Criteria

- `SKILL.md` describes `full-spec` as the default mode.
- The saved file includes `Short Command`, objective, success criteria, scope, execution plan, verification, safety, iteration policy, stop, and pause.
- The short Codex `/goal` points to the saved file and requires the future executing agent to read it first.
- Creating the goal does not execute the goal.
- The smoke test verifies `mode: full-spec` and the `Short Command` section.

## Scope

Allowed:
- Modify `SKILL.md`, README, examples, and scripts.
- Keep `scripts/save_goal.py` as a small persistence helper.

Forbidden:
- Do not add a database, web UI, template engine, or external dependency.
- Do not modify unrelated local projects or global agent configuration.

## Execution Plan

1. Update the skill instructions to define compact and full-spec modes.
2. Add `mode` to saved goal frontmatter.
3. Add a full-spec example.
4. Update the smoke test.
5. Run checks, sync the local installed skill, commit, push, and tag the release.

## Verification

- Run `python scripts/smoke_test.py`.
- Run `python scripts/save_goal.py --help`.
- Run the repository privacy scan and confirm no sensitive local data is present.
- Confirm `git status --short --branch` is clean after push.

## Safety / Constraints

- Keep the short command under the input-box limit.
- Keep full details in the saved Markdown file.
- Preserve no-dependency operation.

## Iteration Policy

- Make one focused change set.
- Rerun the smoke test after script or example edits.
- If a check fails, inspect the exact output before retrying.

## Stop

- The new default behavior is documented, tested, installed locally, pushed to GitHub, and tagged.

## Pause

- GitHub publishing permissions, destructive Git operations, or unexpected sensitive data exposure require user confirmation.
