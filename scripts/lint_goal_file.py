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

EVIDENCE_WORDS = [
    "run",
    "test",
    "build",
    "lint",
    "typecheck",
    "screenshot",
    "log",
    "artifact",
    "file",
    "运行",
    "测试",
    "构建",
    "检查",
    "截图",
    "日志",
    "产物",
    "文件",
    "证据",
    "frontmatter",
]

VAGUE_DONE = [
    "when done",
    "looks good",
    "seems good",
    "看起来可以",
    "感觉可以",
    "完成即可",
    "差不多",
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
    "启动入口",
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
    "Subagent Capacity Prerequisite",
    "Subagent Dispatch Decision",
    "Subagent Execution Liberation",
    "Multi-Agent Collaboration",
    "Dispatch Matrix",
    "Shared File Ownership",
    "Subagent Result",
    "Merge Policy",
    "Rejection Conditions",
]

MULTI_AGENT_ZH = [
    "子代理容量前置",
    "子代理派发决策",
    "子代理执行力释放",
    "多代理协同",
    "派发表",
    "共享文件归属",
    "子代理结果",
    "合并策略",
    "拒绝条件",
]

CODEX_SECTION_EN = "Codex Execution Contract"
CODEX_SECTION_ZH = "Codex 执行契约"
CODEX_CONTRACT_TERMS = ["AGENTS.md", ".goals/", "git status --short", "git diff --check"]
CAPACITY_TERMS = [
    "~/.codex/config.toml",
    "[agents]",
    "max_threads = 2147483647",
    "max_depth = 2147483647",
    "codex --strict-config doctor --summary --ascii",
    "codex.cmd --strict-config doctor --summary --ascii",
    "loaded",
]
DISPATCH_LEVEL_TERMS = ["L0", "L1", "L2", "L3"]
DISPATCH_HARD_TERMS_EN = ["minimum 2", "minimum 4", "pause", "must not continue"]
DISPATCH_HARD_TERMS_ZH = ["最少 2", "最少 4", "暂停", "不得由主会话继续"]
LIBERATION_TERMS_EN = ["scheduler", "merge", "final verification", "delegate"]
LIBERATION_TERMS_ZH = ["调度", "合并", "最终验证", "下放"]

DISPATCH_HEADERS_EN = [
    "Slice",
    "Agent Role",
    "Goal",
    "Allowed Files",
    "Forbidden Files",
    "Inputs",
    "Required Output",
    "Verify",
    "Depends On",
    "Merge Owner",
]

DISPATCH_HEADERS_ZH = [
    "切片",
    "代理角色",
    "目标",
    "允许文件",
    "禁止文件",
    "输入",
    "必交输出",
    "验证",
    "依赖",
    "合并负责人",
]

DISPATCH_REQUIRED_CELLS_EN = ["Allowed Files", "Verify", "Merge Owner"]
DISPATCH_REQUIRED_CELLS_ZH = ["允许文件", "验证", "合并负责人"]
DISPATCH_FAKE_SLICE_FIELDS_EN = ["Agent Role", "Goal", "Required Output"]
DISPATCH_FAKE_SLICE_FIELDS_ZH = ["代理角色", "目标", "必交输出"]

SHARED_OWNER_MARKERS = ["Main-session-owned:", "Subagent-owned:"]

SUBAGENT_RESULT_FIELDS_EN = [
    "Slice:",
    "Status:",
    "Changed Files:",
    "Verification Run:",
    "Verification Result:",
    "Boundary Crossings:",
    "Risks:",
    "Handoff:",
]

SUBAGENT_RESULT_FIELDS_ZH = [
    "切片",
    "状态",
    "改动文件",
    "验证命令",
    "验证结果",
    "越界情况",
    "风险",
    "交接说明",
]

FAKE_SLICE_TERMS = [
    "read only",
    "summary only",
    "inspect only",
    "只读",
    "总结",
    "搜索",
    "只检查",
    "只阅读",
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
    "Codex Execution Contract",
    "Slice Table",
    "Subagent Deliverables",
    "Dispatch Matrix",
    "Shared File Ownership",
    "Subagent Result",
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


def section_body(body: str, names: list[str]) -> str:
    escaped = "|".join(re.escape(name) for name in names)
    match = re.search(rf"^##\s+({escaped})\s*$([\s\S]*?)(?=^##\s+|\Z)", body, flags=re.MULTILINE)
    return match.group(2).strip() if match else ""


def table_cells(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def is_zh(frontmatter: dict[str, str], body: str) -> bool:
    language = frontmatter.get("language", "").lower()
    if language.startswith("zh") or "chinese" in language:
        return True
    cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
    latin = len(re.findall(r"[A-Za-z]", body))
    return cjk > 80 and cjk > latin


def has_config_setup(sections: set[str]) -> bool:
    return "Codex Subagent Capacity Setup" in sections or "Codex 子代理并发配置" in sections


def has_no_reorder_rule(body: str) -> bool:
    lowered = body.lower()
    return (
        "不要删除或重排现有配置" in body
        or "without deleting or reordering existing config" in lowered
        or "do not delete or reorder existing config" in lowered
    )


def lint_dispatch_matrix(body: str, source: str, zh: bool) -> list[str]:
    errors: list[str] = []
    section = section_body(body, ["派发表", "Dispatch Matrix"])
    rows = table_cells(section)
    if not rows:
        errors.append(f"{source}: Dispatch Matrix needs a markdown table")
        return errors

    headers = rows[0]
    data_rows = rows[1:]
    expected_headers = DISPATCH_HEADERS_ZH if zh else DISPATCH_HEADERS_EN
    for header in expected_headers:
        if header not in headers:
            errors.append(f"{source}: Dispatch Matrix missing required column `{header}`")

    if len(data_rows) < 2:
        errors.append(f"{source}: Dispatch Matrix needs at least 2 data rows")

    required_cells = DISPATCH_REQUIRED_CELLS_ZH if zh else DISPATCH_REQUIRED_CELLS_EN
    fake_slice_fields = DISPATCH_FAKE_SLICE_FIELDS_ZH if zh else DISPATCH_FAKE_SLICE_FIELDS_EN
    for row in data_rows:
        if len(row) != len(headers):
            errors.append(f"{source}: Dispatch Matrix row has {len(row)} cells but header has {len(headers)}")
            continue
        mapped = dict(zip(headers, row))
        for header in required_cells:
            if header in mapped and not mapped[header].strip():
                errors.append(f"{source}: Dispatch Matrix row missing `{header}`")
        fake_text = " ".join(mapped.get(header, "") for header in fake_slice_fields).lower()
        if any(term.lower() in fake_text for term in FAKE_SLICE_TERMS):
            errors.append(f"{source}: Dispatch Matrix contains read-only or summary-only slice")

    return errors


def lint_shared_ownership(body: str, source: str) -> list[str]:
    errors: list[str] = []
    section = section_body(body, ["共享文件归属", "Shared File Ownership"])
    for marker in SHARED_OWNER_MARKERS:
        if marker not in section:
            errors.append(f"{source}: Shared File Ownership missing `{marker}`")
    return errors


def lint_subagent_result(body: str, source: str, zh: bool) -> list[str]:
    errors: list[str] = []
    section = section_body(body, ["子代理结果", "Subagent Result"])
    fields = SUBAGENT_RESULT_FIELDS_ZH if zh else SUBAGENT_RESULT_FIELDS_EN
    for field in fields:
        if zh:
            found = re.search(rf"^{re.escape(field)}\s*[:：]", section, flags=re.MULTILINE)
        else:
            found = field in section
        if not found:
            errors.append(f"{source}: Subagent Result missing `{field}`")
    return errors


def lint_codex_contract(body: str, sections: set[str], source: str, zh: bool) -> list[str]:
    errors: list[str] = []
    section_name = CODEX_SECTION_ZH if zh else CODEX_SECTION_EN
    if section_name not in sections:
        errors.append(f"{source}: missing full-spec Codex section `{section_name}`")
        return errors
    section = section_body(body, [CODEX_SECTION_ZH, CODEX_SECTION_EN])
    for term in CODEX_CONTRACT_TERMS:
        if term not in section:
            errors.append(f"{source}: Codex contract missing `{term}`")
    return errors


def lint_capacity_prerequisite(body: str, source: str) -> list[str]:
    errors: list[str] = []
    section = section_body(body, ["子代理容量前置", "Subagent Capacity Prerequisite"])
    if not section:
        errors.append(f"{source}: missing subagent capacity prerequisite body")
        return errors
    for term in CAPACITY_TERMS:
        if term not in section:
            errors.append(f"{source}: subagent capacity prerequisite missing `{term}`")
    if not has_no_reorder_rule(section):
        errors.append(f"{source}: subagent capacity prerequisite missing no-delete/no-reorder rule")
    return errors


def lint_dispatch_decision(body: str, source: str, zh: bool) -> list[str]:
    errors: list[str] = []
    section = section_body(body, ["子代理派发决策", "Subagent Dispatch Decision"])
    if not section:
        errors.append(f"{source}: missing subagent dispatch decision body")
        return errors
    for term in DISPATCH_LEVEL_TERMS:
        if term not in section:
            errors.append(f"{source}: subagent dispatch decision missing `{term}`")
    hard_terms = DISPATCH_HARD_TERMS_ZH if zh else DISPATCH_HARD_TERMS_EN
    for term in hard_terms:
        if term.lower() not in section.lower():
            errors.append(f"{source}: subagent dispatch decision missing hard rule `{term}`")
    return errors


def lint_liberation(body: str, source: str, zh: bool) -> list[str]:
    errors: list[str] = []
    section = section_body(body, ["子代理执行力释放", "Subagent Execution Liberation"])
    if not section:
        errors.append(f"{source}: missing subagent execution liberation body")
        return errors
    terms = LIBERATION_TERMS_ZH if zh else LIBERATION_TERMS_EN
    for term in terms:
        if term.lower() not in section.lower():
            errors.append(f"{source}: subagent execution liberation missing `{term}`")
    return errors


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
        errors.extend(lint_codex_contract(body, sections, source, zh))
        errors.extend(lint_capacity_prerequisite(body, source))
        errors.extend(lint_dispatch_decision(body, source, zh))
        errors.extend(lint_liberation(body, source, zh))
        for section in multi_agent:
            if section not in sections:
                errors.append(f"{source}: missing full-spec multi-agent section `{section}`")
        errors.extend(lint_dispatch_matrix(body, source, zh))
        errors.extend(lint_shared_ownership(body, source))
        errors.extend(lint_subagent_result(body, source, zh))

    goal_lines = [line.strip() for line in body.splitlines() if line.strip().startswith("/goal")]
    if not goal_lines:
        errors.append(f"{source}: missing `/goal` launcher")
    for line in goal_lines:
        if len(line) > 140:
            errors.append(f"{source}: launcher exceeds 140 chars")
        if "`.goals/" not in line:
            errors.append(f"{source}: launcher should point to `.goals/<file>.md`")
        if "execute only" not in line.lower() and "只执行" not in line:
            errors.append(f"{source}: launcher should say to execute only the saved file")

    for pattern in PLACEHOLDERS:
        if re.search(pattern, body, flags=re.IGNORECASE):
            errors.append(f"{source}: unresolved placeholder matched `{pattern}`")

    verification = section_body(body, ["验证", "Verification"])
    if verification and not any(word.lower() in verification.lower() for word in EVIDENCE_WORDS):
        errors.append(f"{source}: verification should name concrete evidence")

    stop_pause = "\n".join([section_body(body, ["停止", "Stop"]), section_body(body, ["暂停", "Pause"])])
    for phrase in VAGUE_DONE:
        if phrase.lower() in stop_pause.lower():
            errors.append(f"{source}: vague completion language `{phrase}`")

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
            "codex.cmd --strict-config doctor --summary --ascii",
            "loaded",
        ]:
            if required_text not in body:
                errors.append(f"{source}: Codex capacity setup missing `{required_text}`")
        if not has_no_reorder_rule(body):
            errors.append(f"{source}: Codex capacity setup missing no-delete/no-reorder rule")

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
