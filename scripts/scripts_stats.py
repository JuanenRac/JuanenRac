#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/scripts_stats.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""What a repository runs: its GitHub workflows and its own scripts. Read-only, standard library only.

`summarize(root)` reads the working tree of one repository (a shallow clone made by code_stats.py) and returns

    {"wf": [[file, name, [triggers], jobs, [runners]], ...],
     "acts": {"owner/repo@ref": [uses, pin]},
     "sc": {"py": [files, lines], "sh": ..., "ps1": ..., "bat": ..., "js": ...}}

* **Workflows** are the files of `.github/workflows`. The YAML is not loaded as YAML (no library): the few keys that matter (`on`, `runs-on`, `jobs`, `uses`) are
  read line by line, which is enough for the workflows of the repositories and never executes anything. A file that cannot be read is skipped.
* **Triggers** are the events under `on` (`push`, `pull_request`, `schedule`, `workflow_dispatch`, `release`, `workflow_run`, `workflow_call`, any other one is `other`).
* **Actions** are the `uses:` of the steps and of the reusable workflows, each with how its version is fixed: `sha` (a full commit), `tag` (a version number
  such as `v4`), `branch` (anything else, such as `main`), `local` (a path of the repository) or `docker` (an image). Whether a pinned action is out of date is
  not known without asking GitHub, so it is not said.
* **Scripts** are the files of `tools/` and `scripts/` (any depth) by language: `py`, `sh`, `ps1`, `bat` (also `.cmd`) and `js` (also `.mjs`, `.cjs`, `.ts`).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping

TRIGGERS = ("push", "pull_request", "schedule", "workflow_dispatch", "release", "workflow_run", "workflow_call", "other")
PINS = ("sha", "tag", "branch", "local", "docker")
LANGS = ("py", "sh", "ps1", "bat", "js")
EXTENSIONS = {"py": "py", "sh": "sh", "ps1": "ps1", "bat": "bat", "cmd": "bat", "js": "js", "mjs": "js", "cjs": "js", "ts": "js"}
SCRIPT_DIRS = ("tools", "scripts")
MAX_WORKFLOWS = 80
MAX_FILE_BYTES = 400_000

_ON = re.compile(r"""^(?:on|"on"|'on')\s*:\s*(.*?)\s*(?:#.*)?$""")
_KEY = re.compile(r"""^(\s*)(?:"([^"]+)"|'([^']+)'|([A-Za-z0-9_.-]+))\s*:\s*(.*?)\s*$""")
_USES = re.compile(r"""^\s*(?:-\s+)?uses\s*:\s*['"]?([^\s'"#]+)['"]?""")
_RUNS_ON = re.compile(r"""^\s*(?:-\s+)?runs-on\s*:\s*(.*?)\s*(?:#.*)?$""")
_NAME = re.compile(r"""^name\s*:\s*['"]?(.*?)['"]?\s*(?:#.*)?$""")
_SHA = re.compile(r"[0-9a-f]{40}")
_VERSION = re.compile(r"v?\d+(\.\d+){0,2}([-+][0-9A-Za-z.-]+)?")


def _unquote(text: str) -> str:
    text = text.strip()
    return text[1:-1] if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"" else text


def trigger_names(lines: list[str]) -> list[str]:
    """The events of the `on` key of a workflow, in the order of TRIGGERS, without repeats."""
    found: list[str] = []
    for index, raw in enumerate(lines):
        match = _ON.match(raw.rstrip())
        if not match:
            continue
        inline = match.group(1)
        if inline:
            names = [_unquote(part) for part in re.split(r"[\s,\[\]{}]+", inline) if part and not part.startswith("#")]
        else:
            names, base = [], None
            for follow in lines[index + 1:]:
                if not follow.strip() or follow.lstrip().startswith("#"):
                    continue
                if not follow.startswith((" ", "\t")):
                    break
                key = _KEY.match(follow.rstrip())
                indent = len(follow) - len(follow.lstrip())
                if base is None:
                    base = indent
                if key and indent == base:
                    names.append(key.group(2) or key.group(3) or key.group(4))
                elif follow.lstrip().startswith("- ") and indent == base:
                    names.append(_unquote(follow.lstrip()[2:].split("#")[0]))
        found = names
        break
    known = {name for name in found}
    out = [t for t in TRIGGERS[:-1] if t in known]
    if known - set(TRIGGERS[:-1]):
        out.append("other")
    return out


def job_count(lines: list[str]) -> int:
    """How many keys sit directly under `jobs:`."""
    for index, raw in enumerate(lines):
        if raw.rstrip() != "jobs:":
            continue
        base, count = None, 0
        for follow in lines[index + 1:]:
            if not follow.strip() or follow.lstrip().startswith("#"):
                continue
            if not follow.startswith((" ", "\t")):
                break
            indent = len(follow) - len(follow.lstrip())
            if base is None:
                base = indent
            if indent == base and _KEY.match(follow.rstrip()):
                count += 1
        return count
    return 0


def runner_names(lines: list[str]) -> list[str]:
    """The distinct `runs-on` values (an expression is written `matrix`), sorted."""
    out = set()
    for raw in lines:
        match = _RUNS_ON.match(raw)
        if not match:
            continue
        value = _unquote(match.group(1))
        if not value:
            continue
        value = "matrix" if "${{" in value else value.strip("[] ").split(",")[0].strip().strip("'\"")
        if value:
            out.add(value[:40])
    return sorted(out)


def pin_of(uses: str) -> str:
    """How the version of a `uses:` value is fixed."""
    if uses.startswith("./"):
        return "local"
    if uses.startswith("docker://"):
        return "docker"
    ref = uses.rpartition("@")[2] if "@" in uses else ""
    if _SHA.fullmatch(ref):
        return "sha"
    return "tag" if _VERSION.fullmatch(ref) else "branch"


def action_uses(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        match = _USES.match(raw)
        if match:
            out.append(match.group(1))
    return out


def workflow_record(name: str, text: str) -> tuple[list, list[str]]:
    lines = text.splitlines()
    title = name
    for raw in lines:
        match = _NAME.match(raw)
        if match and match.group(1):
            title = match.group(1)
            break
    return [name, title[:80], trigger_names(lines), job_count(lines), runner_names(lines)], action_uses(lines)


def count_scripts(root: Path) -> dict:
    out: dict[str, list[int]] = {}
    for folder in SCRIPT_DIRS:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            lang = EXTENSIONS.get(path.suffix.lower().lstrip("."))
            if lang is None or not path.is_file() or path.is_symlink():
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES * 5:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            entry = out.setdefault(lang, [0, 0])
            entry[0] += 1
            entry[1] += len(text.splitlines())
    return out


def summarize(root: Path) -> dict:
    """The workflows, the actions and the scripts of the repository at `root`."""
    workflows: list = []
    actions: dict[str, list] = {}
    folder = root / ".github" / "workflows"
    if folder.is_dir():
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() not in (".yml", ".yaml") or not path.is_file() or path.is_symlink():
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            record, uses = workflow_record(path.name, text)
            workflows.append(record)
            for item in uses:
                key = item[:140]
                actions.setdefault(key, [0, pin_of(item)])[0] += 1
    return {"wf": workflows[:MAX_WORKFLOWS], "acts": dict(sorted(actions.items())[:200]), "sc": count_scripts(root)}


def is_third_party(uses: str, owner: str) -> bool:
    """A `uses:` that is neither a path of the repository, an image nor an action of the owner's own account."""
    return not uses.startswith(("./", "docker://")) and not uses.lower().startswith(owner.lower() + "/")


def totals(repos: Mapping[str, Mapping]) -> dict:
    """Plain sums over the records that carry a `scripts` block (used by the tests and by the page generator)."""
    out = {"repos": 0, "workflows": 0, "jobs": 0, "uses": 0, "unpinned": 0, "files": 0, "lines": 0}
    for record in repos.values():
        block = record.get("scripts")
        if not isinstance(block, Mapping):
            continue
        out["repos"] += 1
        out["workflows"] += len(block.get("wf", []))
        out["jobs"] += sum(row[3] for row in block.get("wf", []))
        for count, pin in block.get("acts", {}).values():
            out["uses"] += count
            if pin in ("branch", "tag"):
                out["unpinned"] += count
        for files, lines in block.get("sc", {}).values():
            out["files"] += files
            out["lines"] += lines
    return out
