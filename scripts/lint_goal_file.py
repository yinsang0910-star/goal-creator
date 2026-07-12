#!/usr/bin/env python3
"""Lint persisted full-spec goal contracts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CANONICAL_FIELDS = (
    "launcher", "objective", "original_request", "non_negotiables", "success_criteria", "scope",
    "plan", "verification", "safety", "iteration", "authority", "stop", "pause",
)
MARKER_RE = re.compile(r"^<!-- goal:([a-z_]+) -->\s*$", re.MULTILINE)
PLACEHOLDERS = [r"<[^>]+>", r"\bTBD\b", r"\bTODO\b", r"待补充", r"待定"]
EVIDENCE_WORDS = [
    "run", "test", "build", "lint", "typecheck", "screenshot", "log", "artifact", "file",
    "运行", "测试", "构建", "检查", "截图", "日志", "产物", "文件", "证据",
]
VAGUE_DONE = ["when done", "looks good", "seems good", "看起来可以", "感觉可以", "完成即可", "差不多"]
EN_HEADINGS_IN_ZH = [
    "Short Command", "Objective", "Original Request", "Non-Negotiables", "Success Criteria", "Scope",
    "Execution Plan", "Verification", "Safety / Constraints", "Iteration Policy", "Authority", "Stop", "Pause",
]
OBSOLETE_HEADINGS = [
    "Subagent Dispatch Decision", "Subagent Execution Liberation", "Dispatch Matrix", "Shared File Ownership",
    "Subagent Result", "子代理派发决策", "子代理执行力释放", "派发表", "共享文件归属", "子代理结果",
]
OBSOLETE_CAPACITY_RE = re.compile(r"\bmax_(?:threads|depth)\s*=", re.IGNORECASE)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    try:
        _, raw, body = text.split("---", 2)
    except ValueError:
        return {}, text
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data, body


def prose_without_fences(text: str) -> str:
    lines: list[str] = []
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            fence = "" if fence == marker else marker if not fence else fence
            continue
        if not fence:
            lines.append(line)
    return "\n".join(lines)


def canonical_sections(prose: str) -> tuple[dict[str, str], set[str]]:
    matches = list(MARKER_RE.finditer(prose))
    sections: dict[str, str] = {}
    duplicates: set[str] = set()
    for index, match in enumerate(matches):
        name = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(prose)
        if name in sections:
            duplicates.add(name)
        sections[name] = prose[match.end():end].strip()
    return sections, duplicates


def is_zh(frontmatter: dict[str, str], body: str) -> bool:
    language = frontmatter.get("language", "").lower()
    if language.startswith("zh") or "chinese" in language:
        return True
    cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
    latin = len(re.findall(r"[A-Za-z]", body))
    return cjk > 80 and cjk > latin


def lint_text(text: str, source: str) -> list[str]:
    errors: list[str] = []
    frontmatter, body = parse_frontmatter(text)
    prose = prose_without_fences(body)
    sections, duplicates = canonical_sections(prose)
    full_spec = frontmatter.get("mode", "") in {"", "full-spec"}

    if full_spec:
        for key, expected in {"schema": "goal/v1", "authority": "subordinate"}.items():
            if frontmatter.get(key) != expected:
                errors.append(f"{source}: frontmatter `{key}` must be `{expected}`")
        for field in CANONICAL_FIELDS:
            if not sections.get(field):
                errors.append(f"{source}: missing canonical field `{field}`")
        for field in sorted(duplicates):
            errors.append(f"{source}: duplicate canonical field `{field}`")

        authority = sections.get("authority", "")
        authority_terms = [
            ("AGENTS.md",), ("current", "当前"), ("runtime", "运行时"),
            ("override", "优先", "覆盖"),
        ]
        for choices in authority_terms:
            if not any(term.lower() in authority.lower() for term in choices):
                errors.append(f"{source}: authority field missing one of {choices}")

        headings = {m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", prose, re.MULTILINE)}
        for heading in OBSOLETE_HEADINGS:
            if heading in headings:
                errors.append(f"{source}: obsolete forced orchestration section `{heading}`")
        if OBSOLETE_CAPACITY_RE.search(body):
            errors.append(f"{source}: obsolete agent capacity override")

    goal_lines = [line.strip() for line in body.splitlines() if line.strip().startswith("/goal")]
    if not goal_lines:
        errors.append(f"{source}: missing `/goal` launcher")
    for line in goal_lines:
        if len(line) > 140:
            errors.append(f"{source}: launcher exceeds 140 chars")
        if full_spec and "`.goals/" not in line:
            errors.append(f"{source}: saved full-spec launcher must point to `.goals/<file>.md`")
        if full_spec and "execute only" not in line.lower() and "只执行" not in line:
            errors.append(f"{source}: saved full-spec launcher must execute only the saved file")

    placeholder_body = MARKER_RE.sub("", body)
    for pattern in PLACEHOLDERS:
        if re.search(pattern, placeholder_body, flags=re.IGNORECASE):
            errors.append(f"{source}: unresolved placeholder matched `{pattern}`")

    verification = sections.get("verification", "")
    if verification and not any(word.lower() in verification.lower() for word in EVIDENCE_WORDS):
        errors.append(f"{source}: verification should name concrete evidence")

    stop_pause = "\n".join([sections.get("stop", ""), sections.get("pause", "")])
    for phrase in VAGUE_DONE:
        if phrase.lower() in stop_pause.lower():
            errors.append(f"{source}: vague completion language `{phrase}`")

    if is_zh(frontmatter, body):
        for label in EN_HEADINGS_IN_ZH:
            if re.search(rf"^##\s+{re.escape(label)}\s*$", prose, flags=re.MULTILINE):
                errors.append(f"{source}: English heading `{label}` in Chinese goal")
        if re.search(r"^(Allowed|Forbidden):\s*$", prose, flags=re.MULTILINE):
            errors.append(f"{source}: English scope label in Chinese goal")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] in {"-h", "--help"}:
        print("Usage: lint_goal_file.py <goal.md> [<goal.md> ...]")
        return 0
    if len(argv) < 2:
        print("Usage: lint_goal_file.py <goal.md> [<goal.md> ...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    for raw in argv[1:]:
        path = Path(raw)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: cannot read file: {exc}")
            continue
        errors.extend(lint_text(text, str(path)))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("goal file lint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
