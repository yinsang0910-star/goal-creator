---
schema: goal/v1
authority: subordinate
title: Goal Creator Simplification
created: 2026-07-12
status: draft
language: en
mode: full-spec
formats:
  - codex
  - markdown
---

# Goal Creator Simplification

<!-- goal:launcher -->
## Short Command

```text
/goal Execute only `.goals/2026-07-12-goal-creator-simplification.md`.
```

<!-- goal:objective -->
## Objective

Keep goal creation concise, explicit about persistence, and subordinate to current project truth.

<!-- goal:original_request -->
## Original Request

Simplify goal-creator now that Codex handles its own agent orchestration.

<!-- goal:non_negotiables -->
## Non-Negotiables

- Never execute a created goal automatically.
- Never modify global Codex configuration.
- Do not prescribe agent tiers, counts, models, providers, or reasoning levels.

<!-- goal:success_criteria -->
## Success Criteria

- Ordinary tasks produce compact copyable text without file writes.
- Persistence occurs only after an explicit request.
- Saved contracts use stable canonical markers and preserve current-project authority.
- UTF-8 translated headings do not control machine validation.

<!-- goal:scope -->
## Scope

Allowed:
- Modify this repository's skill, scripts, example, metadata, and README.

Forbidden:
- Do not modify global configuration, other skills, plugin caches, or external repositories.

<!-- goal:plan -->
## Execution Plan

1. Encode compact/full-spec and persistence selection rules.
2. Validate stable canonical markers instead of translated headings.
3. Make installation validate, back up, and replace only goal-creator.
4. Run focused checks and compare repository and installed hashes.

<!-- goal:verification -->
## Verification

- Run `python scripts/smoke_test.py`.
- Run `python scripts/lint_goal_file.py examples/full-spec-goal.md`.
- Run the skill validator and `git diff --check`.

<!-- goal:safety -->
## Safety / Constraints

- Keep repository writes inside `C:\goal-creator`.
- Back up the installed goal-creator before replacement.
- Do not push or publish externally.

<!-- goal:iteration -->
## Iteration Policy

- Fix concrete failing evidence without weakening the requested outcome or safety boundary.

<!-- goal:authority -->
## Authority

- Read and obey applicable `AGENTS.md` and current project authority documents.
- Current code and fresh runtime evidence override stale checkboxes, chat, summaries, and this goal's factual claims.
- This goal preserves intent and boundaries; it is not a second source of runtime truth.

<!-- goal:stop -->
## Stop

- Repository and installed-package checks pass, and their expected file hashes match.

<!-- goal:pause -->
## Pause

- Pause before external publication, unrelated writes, or any operation requiring new credentials.
