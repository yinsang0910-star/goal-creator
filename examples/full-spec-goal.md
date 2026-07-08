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
/goal Execute only `.goals/2026-06-20-goal-creator-v0-2.md`.
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

## Codex Execution Contract

- CWD: current project root.
- Instruction source: read and obey applicable `AGENTS.md`.
- Resumable artifact: this `.goals/2026-06-20-goal-creator-v0-2.md`.
- Final checks: `git status --short`, `git diff --check`, and `python scripts/smoke_test.py`.
- Chat output: report only saved path, launcher, verification result, and material risks.

## Subagent Capacity Prerequisite

- Before using full-spec / subagent-first goals, check the current user's `~/.codex/config.toml`.
- If `[agents]` exists, update only `max_threads = 2147483647` and `max_depth = 2147483647`; if it does not exist, append it.
- Do not delete or reorder existing config.
- Run `codex --strict-config doctor --summary --ascii`.
- On Windows, if `codex` is blocked by PowerShell execution policy or shim handling, run `codex.cmd --strict-config doctor --summary --ascii`.
- Continue only after the output shows `Configuration` / `config` is `loaded`.

## Subagent Dispatch Decision

- L0: no subagent. Use for single-file small edits, explanations, simple commands, and wording tweaks.
- L1: one subagent. Use for isolated reading, local verification, or risk review.
- L2: minimum 2 subagents. Use for cross-module work, code plus tests, or implementation and verification that can proceed in parallel.
- L3: minimum 4 subagents. Use for multi-module migrations, broad refactors, investigations, and batch fixes.
- This task is L2 because docs, lint, and examples can be split by file ownership.
- If L2/L3 is selected and the session cannot create the required subagents, pause; the main session must not continue as the substitute executor.

## Subagent Execution Liberation

- Main session runs as scheduler, merger, boundary judge, and final verification owner.
- Delegate execution work that can be isolated, verified, and handed off.
- Subagents own context reading, implementation, local tests, local fixes, and risk reporting inside their file range.
- Main session keeps goal freezing, file-boundary decisions, merge decisions, and final verification.

## Multi-Agent Collaboration

- Main session selects L0/L1/L2/L3 before implementation and dispatches only useful slices.
- Main session must avoid fake parallel work and keep file ownership explicit.

## Dispatch Matrix

| Slice | Agent Role | Goal | Allowed Files | Forbidden Files | Inputs | Required Output | Verify | Depends On | Merge Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| docs/handoff | subagent | Document the subagent-first contract in user-facing docs | SKILL.md, README.md | scripts/save_goal.py, unrelated files | Current full-spec contract and user feedback | Changed files, verification command, result, risk, handoff | `python scripts/smoke_test.py` | none | main session |
| verification | subagent | Enforce dispatch levels and liberation checks in examples and lint | scripts/smoke_test.py, scripts/lint_goal_file.py, examples/full-spec-goal.md | unrelated files | Required dispatch matrix and result template | Changed files, verification command, result, risk, handoff | `python scripts/smoke_test.py` and `python scripts/lint_goal_file.py examples/full-spec-goal.md` | docs/handoff | main session |

## Shared File Ownership

Main-session-owned:
- Release tag and final merge decisions.
- Any file touched by both slices.

Subagent-owned:
- Files explicitly listed in each dispatch row's `Allowed Files`.

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
- Main session consumes each subagent result before merging.
- Shared files are merged serially by the main session.
- Final verification runs after all adopted results are merged.

## Rejection Conditions

- Reject subagent work that crosses file boundaries.
- Reject work that skips verification or weakens the goal.
- Reject work that cannot be understood or merged from the handoff.

## Stop

- The new default behavior is documented, tested, installed locally, pushed to GitHub, and tagged.

## Pause

- GitHub publishing permissions, destructive Git operations, or unexpected sensitive data exposure require user confirmation.
