#!/usr/bin/env python3
"""Lint saved full-spec goal files for contract quality."""

from __future__ import annotations

import re
import sys
from pathlib import Path


PLACEHOLDERS = [
    r"<[^>]+>",
    r"\bTBD\b",
    r"\bTODO\b",
    r"待补充",
    r"待定",
]

EN_REQUIRED = [
    "Short Command",
    "Objective",
    "Original Request",
    "Non-Negotiables",
    "Success Criteria",
    "Scope",
    "Verification",
    "Safety / Constraints",
    "Iteration Policy",
    "Stop",
    "Pause",
]

ZH_REQUIRED = [
    "短启动命令",
    "目标",
    "原始需求",
    "不可降级项",
    "成功标准",
    "范围",
    "验证",
    "安全 / 约束",
    "迭代策略",
    "停止",
    "暂停",
]

MULTI_AGENT_EN = [
    "Multi-Agent Collaboration",
    "Slice Table",
    "Subagent Deliverables",
    "Merge Policy",
    "Rejection Conditions",
]

MULTI_AGENT_ZH = [
    "多代理协同",
    "切片表",
    "子代理交付物",
    "合并策略",
    "拒绝条件",
]

EN_LABELS_IN_ZH = [
    "Short Command",
    "Objective",
    "Original Request",
    "Non-Negotiables",
    "Success Criteria",
    "Scope",
    "Verification",
    "Safety / Constraints",
    "Iteration Policy",
    "Multi-Agent Collaboration",
    "Slice Table",
    "Subagent Deliverables",
    "Merge Policy",
    "Rejection Conditions",
    "Stop",
    "Pause",
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    try:
        _, raw, body = text.split("---", 2)
    except ValueError:
        return {}, text
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, body


def headings(body: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^##\s+(.+)$", body, re.MULTILINE)}


def is_zh(frontmatter: dict[str, str], body: str) -> bool:
    language = frontmatter.get("language", "").lower()
    if language.startswith("zh") or "chinese" in language:
        return True
    cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
    latin = len(re.findall(r"[A-Za-z]", body))
    return cjk > 80 and cjk > latin


def has_config_setup(sections: set[str]) -> bool:
    return "Codex Subagent Capacity Setup" in sections or "Codex 子代理并发配置" in sections


def lint_text(text: str, source: str) -> list[str]:
    errors: list[str] = []
    frontmatter, body = parse_frontmatter(text)
    sections = headings(body)
    zh = is_zh(frontmatter, body)
    mode = frontmatter.get("mode", "")

    required = ZH_REQUIRED if zh else EN_REQUIRED
    for section in required:
        if section not in sections:
            errors.append(f"{source}: missing section `{section}`")

    multi_agent = MULTI_AGENT_ZH if zh else MULTI_AGENT_EN
    if mode == "full-spec" or not mode:
        for section in multi_agent:
            if section not in sections:
                errors.append(f"{source}: missing full-spec multi-agent section `{section}`")

    goal_lines = [line.strip() for line in body.splitlines() if line.strip().startswith("/goal")]
    if not goal_lines:
        errors.append(f"{source}: missing `/goal` launcher")
    for line in goal_lines:
        if len(line) > 140:
            errors.append(f"{source}: launcher exceeds 140 chars")
        if "`.goals/" not in line:
            errors.append(f"{source}: launcher should point to `.goals/<file>.md`")
        if "execute only" not in line and "只执行" not in line:
            errors.append(f"{source}: launcher should say to execute only the saved file")

    for pattern in PLACEHOLDERS:
        if re.search(pattern, body, flags=re.IGNORECASE):
            errors.append(f"{source}: unresolved placeholder matched `{pattern}`")

    if zh:
        for label in EN_LABELS_IN_ZH:
            if re.search(rf"^##\s+{re.escape(label)}\s*$", body, flags=re.MULTILINE):
                errors.append(f"{source}: English heading `{label}` in Chinese goal")
        if re.search(r"^(Allowed|Forbidden):\s*$", body, flags=re.MULTILINE):
            errors.append(f"{source}: English scope label in Chinese goal")

    if has_config_setup(sections):
        for required_text in [
            "~/.codex/config.toml",
            "max_threads = 2147483647",
            "max_depth = 2147483647",
            "codex --strict-config doctor --summary --ascii",
            "loaded",
        ]:
            if required_text not in body:
                errors.append(f"{source}: Codex capacity setup missing `{required_text}`")

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
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("goal file lint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
