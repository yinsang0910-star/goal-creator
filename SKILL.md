---
name: goal-creator
description: Create or review copyable execution goals and, only when explicitly requested, persist resumable goal contracts. Use for /goal text, task objectives, execution contracts, saved goal files, 创建目标, 保存目标, or goal review/lint requests.
---

# Goal Creator

Create the goal only. Never execute it unless the user separately asks.

## Choose the smallest mode

- Use `compact` for ordinary low- or medium-risk work and whenever the user only asks for `/goal` text or a copyable objective.
- Use `full-spec` when the user explicitly asks for it or the work is long-running, cross-cutting, destructive, production-facing, security-sensitive, privacy-sensitive, credentialed, financial, or otherwise needs a complete contract.
- Persistence is separate from mode. Write `.goals/*.md` only when the user explicitly asks to save, persist, create a goal file, or make a resumable contract. Otherwise return copyable content and make no file changes.
- Use `review` to inspect or improve an existing goal.
- Ask at most one question, only when the answer changes risk, scope, cost, ownership, or write location.

## Preserve authority and risk

- Treat every goal as subordinate to applicable `AGENTS.md`, current project authority documents, current code, and fresh runtime evidence. Those sources override stale goal claims, checkboxes, chat text, or prior summaries.
- Preserve the user's intended outcome and explicit boundaries. Never shrink the goal silently.
- Preserve money, security, production access, credentials, private-body, destructive-action, and external-publishing constraints explicitly.
- Do not hardcode a model, provider, reasoning level, or agent topology. If the user requests a tier, record the needed capability, risk tolerance, latency, or quality; let the execution runtime map it.
- Include parallelism only when the user explicitly requests parallel or independent review. Let execution-time independence determine the slices and count.
- Never modify global Codex config, plugin caches, other skills, or unrelated project files.

## compact

Keep ordinary goals short and directly copyable:

```text
/goal <one concrete outcome>

Success:
- <observable result>
Verify:
- <smallest relevant check>
Boundaries:
- <write scope or hard limit>
Pause: <first blocker requiring user input>
```

Translate visible labels to the user's language. Do not save unless explicitly requested.

## full-spec

For an unsaved full-spec, return the complete human-readable contract inline and start it with:

```text
/goal Execute the complete contract below. Do not create files unless the contract explicitly authorizes them.
```

Include objective, original request, non-negotiables, success criteria, scope, plan, verification, safety, iteration, authority, stop, and pause sections. Do not add frontmatter, canonical markers, or a saved-file path.

For a persisted full-spec explicitly requested by the user, use stable canonical markers plus translated human headings:

```markdown
---
schema: goal/v1
authority: subordinate
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

<!-- goal:launcher -->
## Short Command

```text
/goal Execute only `.goals/<file>.md`.
```

<!-- goal:objective -->
## Objective

<one concrete outcome>

<!-- goal:original_request -->
## Original Request

<requested end state without narrowing>

<!-- goal:non_negotiables -->
## Non-Negotiables

- <acceptance requirement or hard boundary>

<!-- goal:success_criteria -->
## Success Criteria

- <observable result>

<!-- goal:scope -->
## Scope

Allowed:
- <write scope>

Forbidden:
- <no-touch area>

<!-- goal:plan -->
## Execution Plan

1. <ordered executable step>

<!-- goal:verification -->
## Verification

- <runnable check or inspectable evidence>

<!-- goal:safety -->
## Safety / Constraints

- <risk control>

<!-- goal:iteration -->
## Iteration Policy

- <respond to failed evidence without weakening the goal>

<!-- goal:authority -->
## Authority

- Read and obey applicable `AGENTS.md` and current project authority documents.
- Current code and fresh runtime evidence override stale checkboxes, chat, summaries, and this goal's factual claims.
- This goal preserves intent and boundaries; it is not a second source of runtime truth.

<!-- goal:stop -->
## Stop

- <concrete completion evidence>

<!-- goal:pause -->
## Pause

- <first human or external blocker>
```

Translate headings and prose, but keep `goal:*` markers, frontmatter keys, commands, paths, identifiers, and proper nouns stable. For Chinese, use natural labels such as `启动入口`, `目标`, `原始需求`, `不可降级项`, `成功标准`, `范围`, `执行计划`, `验证`, `安全 / 约束`, `迭代策略`, `权威顺序`, `停止`, and `暂停`.

Before saving, confirm:

- The objective preserves the original request.
- Success criteria are observable; verification names runnable checks or inspectable evidence.
- Scope and safety cover relevant write, production, money, security, credential, privacy, destructive, and publishing boundaries.
- Authority says current project truth and runtime evidence override stale goal text.
- No unresolved placeholders, invented agent counts, global config changes, or hardcoded runtime model/provider choices remain.

## review

Find missing intent, boundaries, evidence, authority order, stop/pause conditions, silent scope reduction, vague completion language, mixed-language labels, obsolete forced orchestration, or hidden global writes. Report findings first; correct the goal only when asked or clearly implied.

## Formats

Default to `codex` for copyable text and add `markdown` when saving. If requested, render the same canonical intent for Claude, Gemini, Cursor/Windsurf/Cline, or GitHub using that surface's native task labels. Do not change scope or acceptance criteria between formats.

## Save and validate

Only after an explicit persistence request, run from the user's project root:

```bash
python <skill-dir>/scripts/save_goal.py --title "<title>" --mode full-spec --format codex --format markdown < goal.txt
```

Validate saved full-spec goals with:

```bash
python <skill-dir>/scripts/lint_goal_file.py .goals/<file>.md
```

Install or update this skill only when explicitly requested:

```bash
python <skill-dir>/scripts/install_local.py
```

## Response

- Unsaved: return the copyable goal content and one short material-risk note when needed.
- Saved: return the saved path, copyable launcher, and material risks.
- Do not dump test logs, diffs, internal threads, model details, or orchestration traces unless the user asks.
- Do not continue into execution.
