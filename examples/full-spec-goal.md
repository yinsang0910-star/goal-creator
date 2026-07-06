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
/goal Read `.goals/2026-06-20-goal-creator-v0-2.md`; execute only that file.
```

## Objective

Upgrade `goal-creator` so the chat command stays short while the saved `.goals/*.md` file carries the full execution contract.

## Original Request

Make `/goal` commands concise while keeping the goal file content substantial and rigorous enough for a future agent to execute without guessing.

## Non-Negotiables

- Keep the launcher short.
- Keep the saved goal as the complete execution contract.
- Do not treat the short launcher as a replacement for full success criteria, scope, verification, safety, stop, and pause details.

## Success Criteria

- `SKILL.md` describes `full-spec` as the default mode.
- The saved file includes `Short Command`, objective, success criteria, scope, execution plan, verification, safety, iteration policy, stop, and pause.
- The short Codex `/goal` points to the saved file and requires the future executing agent to read it first.
- Creating the goal does not execute the goal.
- The smoke test verifies `mode: full-spec` and the `Short Command` section.
- The saved goal preserves original intent and does not weaken user-provided acceptance criteria.

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
3. Add original-request and non-negotiable fields to prevent silent scope reduction.
4. Add a full-spec example.
5. Update the smoke test.
6. Run checks, sync the local installed skill, commit, push, and tag the release.

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

## Multi-Agent Collaboration

- Full-spec goals default to multi-agent-first execution.
- Main session must first attempt at least two substantial low-conflict slices; if impossible, record the reason in `Pause`.
- Require a slice table with owner, allowed files, forbidden files, expected output, verification, and merge risk before dispatch.
- Require every subagent to return changed files, verification commands and results, risks, and handoff notes.
- Main session must consume each subagent result, merge serially, run project-level verification, and report each contribution.
- Reject subagent work that crosses file boundaries, skips verification, weakens the goal, or cannot be merged from the handoff.

## Codex Subagent Capacity Setup

- Include only when the user asks to configure Codex subagent concurrency or capacity.
- Update `~/.codex/config.toml` without deleting or reordering existing config.
- Ensure `[agents]` contains `max_threads = 2147483647` and `max_depth = 2147483647`.
- Run `codex --strict-config doctor --summary --ascii`.
- Verify `Configuration` / `config` is `loaded`.

## Stop

- The new default behavior is documented, tested, installed locally, pushed to GitHub, and tagged.

## Pause

- GitHub publishing permissions, destructive Git operations, or unexpected sensitive data exposure require user confirmation.
