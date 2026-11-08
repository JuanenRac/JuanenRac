#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/workflow_lint.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""A small linter for the workflow files of a repository, with the same rules and the same three levels (`info`, `warn`, `error`) as the one of the local Actions monitor,
so the Scripts tab and the monitor never keep two criteria for what is wrong with a workflow. Read-only: it opens text and returns counts. Standard library only.

Rules (each one can be switched off and given another level in `lint.rules` of code-stats-config.json):

  unpinned_uses     a `uses:` of an action or reusable workflow that is not pinned to a full commit (a tag or a branch can be moved by its owner)
  permissions       no `permissions:` block at all (the token gets the broad default) or `write-all`
  secrets_in_clear  what looks like a token, key or password written in the file instead of coming from `secrets.*`. Only a value that LOOKS real is an error (a known token
                    format, or a long string with the entropy of a key); a readable filler (`placeholder`, `dummy`, `changeme`...) is only information, anything else a warning
  injection         a text controlled by someone else (`github.event.*.title`, `body`, `head_ref`...) pasted into a `run:` script
  pr_target         `pull_request_target` together with a checkout of the code of the pull request (it runs untrusted code with the permissions of the repository)

A finding is silenced where it is, or by an exemption `repository:file:rule` of `lint.ignore`. In the file, with a comment on the same line or on the line before: `# lint: ignore secrets_in_clear because it is a filler` (a rule name, or `all`); the
comment form `# monitor-lint: ignore ...` of the monitor is understood too. The VALUE of a suspected secret is never kept: a finding is a line, a rule and a level, nothing else.
The reading is textual (there is no YAML parser on purpose); a line it cannot understand is skipped, never guessed.
"""
from __future__ import annotations

import fnmatch
import math
import re
from typing import Mapping

LEVELS = ("info", "warn", "error")
RULES = ("unpinned_uses", "permissions", "secrets_in_clear", "injection", "pr_target")
DEFAULT_LEVEL = {"unpinned_uses": "warn", "permissions": "warn", "secrets_in_clear": "error", "injection": "warn", "pr_target": "error"}
ORDER = {"info": 0, "warn": 1, "error": 2}
LEGACY_LEVEL = {"bad": "error"}      # the monitor calls its highest level "bad"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*['\"]?([^'\"\s#]+)")
SECRET_PATTERNS = [
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")), ("github_fine_grained_token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")), ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")), ("slack_token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")), ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
]
ASSIGN_RE = re.compile(r"""(?i)\b([\w-]*(?:password|passwd|secret|token|api[_-]?key)[\w-]*)\s*[:=]\s*['"]?([A-Za-z0-9/+_.=-]{8,})['"]?\s*(?:#.*)?$""")
FILLER = ("placeholder", "dummy", "example", "changeme", "change-me", "change_me", "fake", "sample", "not-a-real", "notreal", "redacted", "todo", "xxx", "test", "local", "demo", "nothing", "your-", "your_", "ci-", "-ci", "_ci",
          "value", "secret-here", "insert", "replace", "ignored", "unused", "empty", "none")
IGNORE_RE = re.compile(r"#\s*(?:monitor-)?lint:\s*ignore\s+([a-z_]+)")
UNTRUSTED = re.compile(r"\$\{\{\s*github\.(?:event\.(?:issue|pull_request|comment|review|discussion)\.(?:title|body)|event\.head_commit\.message|head_ref|event\.pages\.\*\.page_name)\s*\}\}")
IGNORE_PATTERN_RE = re.compile(r"^[A-Za-z0-9._*-]{1,100}:[A-Za-z0-9._*/-]{1,100}:[a-z_*]{1,30}$")
DEFAULT_CONFIG: dict = {"enabled": True, "ignore": [], "rules": {rule: {"enabled": True, "level": DEFAULT_LEVEL[rule]} for rule in RULES}}


def check_config(raw: object) -> tuple[dict, list[str]]:
    """`lint` of code-stats-config.json merged over the defaults; a value of the wrong type keeps the default and is named."""
    config = {"enabled": True, "ignore": [], "rules": {rule: dict(DEFAULT_CONFIG["rules"][rule]) for rule in RULES}}
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["lint: not an object"]
    if "enabled" in raw:
        if isinstance(raw["enabled"], bool):
            config["enabled"] = raw["enabled"]
        else:
            problems.append("lint.enabled: needs true or false")
    ignore = raw.get("ignore")
    if ignore is not None:
        if isinstance(ignore, list):
            for pattern in ignore:
                if isinstance(pattern, str) and IGNORE_PATTERN_RE.match(pattern):
                    config["ignore"].append(pattern)
                else:
                    problems.append("lint.ignore: each exemption needs the form repository:file:rule (with * allowed)")
        else:
            problems.append("lint.ignore: not a list")
    rules = raw.get("rules")
    if rules is not None:
        if not isinstance(rules, Mapping):
            problems.append("lint.rules: not an object")
        else:
            for name, item in rules.items():
                if name not in RULES:
                    problems.append(f"lint.rules.{name}: unknown rule")
                elif not isinstance(item, Mapping):
                    problems.append(f"lint.rules.{name}: not an object")
                else:
                    if "enabled" in item:
                        if isinstance(item["enabled"], bool):
                            config["rules"][name]["enabled"] = item["enabled"]
                        else:
                            problems.append(f"lint.rules.{name}.enabled: needs true or false")
                    if "level" in item:
                        level = LEGACY_LEVEL.get(item["level"], item["level"])
                        if level in LEVELS:
                            config["rules"][name]["level"] = level
                        else:
                            problems.append(f"lint.rules.{name}.level: needs info, warn or error")
    return config, problems


def entropy(text: str) -> float:
    """Shannon entropy in bits per character."""
    if not text:
        return 0.0
    counts = {c: text.count(c) for c in set(text)}
    return -sum(n / len(text) * math.log2(n / len(text)) for n in counts.values())


def classify_value(value: str) -> str:
    """"reference", "filler" (a readable stand-in), "real" (it looks like a key) or "unknown". The value itself is only read here, never returned."""
    low = value.lower()
    if value.startswith(("$", "{")) or not value:
        return "reference"
    if any(word in low for word in FILLER):
        return "filler"
    if len(value) >= 20 and entropy(value) >= 3.5 and any(c.isdigit() for c in value) and any(c.isalpha() for c in value):
        return "real"
    if len(value) < 24 and entropy(value) < 3.0:
        return "filler"
    return "unknown"


def lint_text(text: str, config: Mapping | None = None) -> list[dict]:
    """The findings of one workflow file: [{"line", "rule", "level"}]. Nothing from the file is kept: no value, no name, no detail."""
    rules = (config or DEFAULT_CONFIG)["rules"]
    lines = text.replace("\r\n", "\n").split("\n")
    found: list[dict] = []

    def silenced(number: int, rule: str) -> bool:
        for index in (number - 1, number - 2):      # the line itself and the one before
            if 0 <= index < len(lines):
                match = IGNORE_RE.search(lines[index])
                if match and match.group(1) in (rule, "all"):
                    return True
        return False

    def add(rule: str, line: int, level: str | None = None) -> None:
        item = rules.get(rule) or {}
        if item.get("enabled", True) and not silenced(line, rule):
            base = item.get("level", DEFAULT_LEVEL[rule])
            if level and ORDER[level] < ORDER[base]:
                base = level      # a weaker class is never more serious than the rule says, only less
            found.append({"line": line, "rule": rule, "level": base})

    has_permissions = any(re.match(r"^permissions\s*:", l) for l in lines)
    has_job_permissions = any(re.match(r"^\s{2,}permissions\s*:", l) for l in lines)
    in_run = False
    run_indent = 0
    pr_target = any(re.match(r"^\s*(?:on\s*:\s*\[?.*)?pull_request_target\b", l) or re.match(r"^\s+pull_request_target\s*:", l) for l in lines)
    checks_out_pr = False
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        uses = USES_RE.match(line)
        if uses:
            spec = uses.group(1)
            if not spec.startswith(("./", "docker://")) and "@" in spec and not SHA_RE.match(spec.split("@", 1)[1]):
                add("unpinned_uses", number)
            if spec.startswith("actions/checkout"):
                window = "\n".join(lines[number:number + 6])
                if re.search(r"ref:\s*\$\{\{\s*github\.event\.pull_request\.head\.(?:sha|ref)", window) or re.search(r"ref:\s*\$\{\{\s*github\.head_ref", window):
                    checks_out_pr = True
        if re.match(r"^\s*permissions\s*:\s*write-all\s*$", line):
            add("permissions", number)
        if any(pattern.search(line) for _label, pattern in SECRET_PATTERNS):
            add("secrets_in_clear", number)
        else:
            assign = ASSIGN_RE.search(line)
            if assign and "secrets." not in line and "${{" not in line:
                kind = classify_value(assign.group(2))
                if kind == "real":
                    add("secrets_in_clear", number)
                elif kind == "unknown":
                    add("secrets_in_clear", number, "warn")
                elif kind == "filler":
                    add("secrets_in_clear", number, "info")
        run = re.match(r"^(\s*)-?\s*run:\s*(\|[+-]?|>[+-]?)?\s*(.*)$", line)
        if run:
            in_run = True
            run_indent = len(run.group(1))
            if run.group(3) and UNTRUSTED.search(run.group(3)):
                add("injection", number)
        elif in_run:
            indent = len(line) - len(line.lstrip())
            if indent <= run_indent and stripped:
                in_run = False
            elif UNTRUSTED.search(line):
                add("injection", number)
    if not has_permissions and not has_job_permissions and any(re.match(r"^jobs\s*:", l) for l in lines):
        add("permissions", 1)
    if pr_target and checks_out_pr:
        add("pr_target", 1)
    return found


def exempt(repo: str, filename: str, rule: str, patterns: "list[str] | tuple[str, ...]") -> bool:
    """True when an exemption of `lint.ignore` (`repository:file:rule`, `*` allowed) covers the finding of a rule in a workflow file of a repository."""
    return any(fnmatch.fnmatchcase(f"{repo}:{filename}:{rule}", pattern) for pattern in patterns or ())


def tally(findings: list[dict]) -> dict:
    """{"info": n, "warn": n, "error": n, "rules": {rule: [info, warn, error]}} of the findings of a repository (rules without findings are left out)."""
    out: dict = {"info": 0, "warn": 0, "error": 0, "rules": {}}
    for item in findings:
        out[item["level"]] += 1
        slot = out["rules"].setdefault(item["rule"], [0, 0, 0])
        slot[ORDER[item["level"]]] += 1
    return out


__all__ = ["LEVELS", "RULES", "DEFAULT_LEVEL", "check_config", "lint_text", "exempt", "tally", "classify_value"]
