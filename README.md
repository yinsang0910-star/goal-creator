# goal-creator

A concise goal maker for AI coding agents.

It turns vague work requests into short executable goals, renders them for major agent formats, and saves them as Markdown files under `.goals/`.

Built for enough structure to finish, not enough ceremony to drown.

## Formats

- Codex `/goal`
- Claude Code
- Gemini / Antigravity
- Cursor / Windsurf / Cline
- GitHub issue
- Generic Markdown

## Install

Copy this directory to your agent skill directory:

```powershell
Copy-Item -Recurse C:\goal-creator $env:USERPROFILE\.agents\skills\goal-creator
```

Restart your agent so it can discover the skill.

## Usage

Ask your agent:

```text
Use goal-creator to create and save a compact goal for refactoring the backtest module.
```

For all mainstream formats:

```text
Use goal-creator to create a saved multi-format goal for building the first MVP.
```

The saved file goes to the current project's `.goals/` directory.

## Script

The bundled script only saves files; the skill decides the goal content.

````powershell
@'
# Example

```text
/goal Build the first working version.

Verify:
- Run the smoke test.

Boundaries:
- Write only in this repo.

Stop:
- The smoke test passes.

Pause:
- Credentials or production access are needed.
```
'@ | python scripts\save_goal.py --title "first working version" --format codex --format markdown
````
