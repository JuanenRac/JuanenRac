#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/code_stats.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Code statistics of every repository of the ecosystems, for the "Code" tab of the status dashboard.

It lists the public repositories of the owner, takes a shallow clone (`git clone --depth 1`) of each one into a temporary directory of its own, counts the
lines and deletes the clone. Nothing is installed and nothing outside the standard library is used.

What is counted, per repository:

  code      lines of the programming languages in files that are not tests: code lines, comment lines and blank lines, by language
  tests     the same for the files of tests (a folder or a file name from `tests` in the configuration), plus the number of test cases found
  docs      lines of documentation (Markdown, reStructuredText, AsciiDoc, text files), the translated READMEs included
  l10n      translation files (folders and names from `translations`; a translated README counts here and in docs)
  data      lines of configuration and data files (JSON, YAML, TOML...), apart: they are never added to the code

What is left out: generated files (a `linguist-generated` or `linguist-vendored` attribute of the `.gitattributes`, generated names), vendored code and
dependencies, build output, binaries, images, lock files and files that look minified or are too big (all listed in `code-stats-config.json`; the table
of languages and the rules for comments are below, in this file). A comment that shares a line with code counts as code; a docstring counts as code.

The result is two documents: `code-stats.json` (the figures of the day) and `code-history.json` (one snapshot per day, thinned out as it gets older). Both
hold only repository names, counts and dates, and the same inputs give the same files, so an unchanged day makes no commit.

    python scripts/code_stats.py --out data [--workdir DIR] [--local-root DIR]

`GITHUB_TOKEN` (optional) raises the limit of the API and is handed to git through the environment, never in a URL or an argument. `--local-root` counts
already-cloned directories (`DIR/<repository>`) instead of cloning, which is how the tests run.
"""
from __future__ import annotations

import argparse
import base64
import fnmatch
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "code-stats-config.json"
STATS_FILE = "code-stats.json"
HISTORY_FILE = "code-history.json"
SCHEMA = 1
API = "https://api.github.com"


# ---------------------------------------------------------------------------
# Languages: extension -> name, comment syntax
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Language:
    name: str
    line: tuple[str, ...] = ()
    block: tuple[str, str] | None = None
    case_regex: str = ""      # what counts as a test case when the file is a test


C_STYLE = dict(line=("//",), block=("/*", "*/"))
HASH = dict(line=("#",))

_TABLE: tuple[tuple[tuple[str, ...], Language], ...] = (
    (("c", "h"), Language("C", **C_STYLE, case_regex=r"\b(?:TEST|TEST_F|TEST_P|TEST_CASE|TEST_CASE_METHOD)\s*\(|^\s*(?:static\s+)?void\s+test_\w+\s*\(")),
    (("cpp", "cc", "cxx", "hpp", "hh", "hxx", "ipp", "ino", "inl"), Language("C++", **C_STYLE, case_regex=r"\b(?:TEST|TEST_F|TEST_P|TEST_CASE|TEST_CASE_METHOD)\s*\(|^\s*(?:static\s+)?void\s+test_\w+\s*\(")),
    (("rs",), Language("Rust", **C_STYLE, case_regex=r"#\[(?:\w+::)?test\]")),
    (("go",), Language("Go", **C_STYLE, case_regex=r"^func\s+Test\w+\(")),
    (("java",), Language("Java", **C_STYLE, case_regex=r"@Test\b")),
    (("kt", "kts"), Language("Kotlin", **C_STYLE, case_regex=r"@Test\b")),
    (("swift",), Language("Swift", **C_STYLE, case_regex=r"\bfunc\s+test\w*\s*\(")),
    (("dart",), Language("Dart", **C_STYLE, case_regex=r"\b(?:test|testWidgets)\s*\(")),
    (("cs",), Language("C#", **C_STYLE, case_regex=r"\[(?:Fact|Test|TestMethod)\]")),
    (("m", "mm"), Language("Objective-C", **C_STYLE)),
    (("ts", "tsx", "mts", "cts"), Language("TypeScript", **C_STYLE, case_regex=r"\b(?:it|test)(?:\.(?:only|skip|each))?\s*\(")),
    (("js", "jsx", "mjs", "cjs"), Language("JavaScript", **C_STYLE, case_regex=r"\b(?:it|test)(?:\.(?:only|skip|each))?\s*\(")),
    (("vue", "svelte"), Language("Vue/Svelte", block=("<!--", "-->"))),
    (("qml",), Language("QML", **C_STYLE)),
    (("py", "pyi"), Language("Python", **HASH, case_regex=r"^\s*(?:async\s+)?def\s+test\w*\s*\(")),
    (("sh", "bash", "zsh"), Language("Shell", **HASH)),
    (("bat", "cmd"), Language("Batch", line=("rem ", "::", "@rem "))),
    (("ps1", "psm1"), Language("PowerShell", line=("#",), block=("<#", "#>"))),
    (("cmake",), Language("CMake", **HASH)),
    (("mk",), Language("Makefile", **HASH)),
    (("sql",), Language("SQL", line=("--",), block=("/*", "*/"))),
    (("html", "htm"), Language("HTML", block=("<!--", "-->"))),
    (("css", "scss", "sass", "less"), Language("CSS", block=("/*", "*/"))),
    (("lua",), Language("Lua", line=("--",), block=("--[[", "]]"))),
    (("rb",), Language("Ruby", **HASH)),
    (("php",), Language("PHP", line=("//", "#"), block=("/*", "*/"))),
    (("gradle", "groovy"), Language("Gradle/Groovy", **C_STYLE)),
    (("proto",), Language("Protocol Buffers", **C_STYLE)),
    (("glsl", "vert", "frag", "wgsl"), Language("Shaders", **C_STYLE)),
    (("s", "asm"), Language("Assembly", line=(";", "//"), block=("/*", "*/"))),
)
BY_EXTENSION: dict[str, Language] = {ext: lang for exts, lang in _TABLE for ext in exts}
BY_NAME: dict[str, Language] = {
    "CMakeLists.txt": Language("CMake", **HASH), "Makefile": Language("Makefile", **HASH), "makefile": Language("Makefile", **HASH),
    "Dockerfile": Language("Dockerfile", **HASH), "Kconfig": Language("Kconfig", **HASH), "Kconfig.projbuild": Language("Kconfig", **HASH),
}
DATA_EXTENSIONS = frozenset({"json", "yaml", "yml", "toml", "ini", "cfg", "conf", "xml", "plist", "csv", "tsv", "jsonc", "properties", "gitignore"})


def language_names() -> list[str]:
    return sorted({lang.name for lang in BY_EXTENSION.values()} | {lang.name for lang in BY_NAME.values()})


# ---------------------------------------------------------------------------
# Counting lines
# ---------------------------------------------------------------------------

def count_lines(text: str, lang: Language) -> tuple[int, int, int]:
    """(code, comment, blank). A line with code and a comment is code; a line inside a block comment is a comment."""
    code = comment = blank = 0
    end: str | None = None
    for raw in text.splitlines():
        rest = raw.strip()
        if not rest:
            blank += 1
            continue
        has_code = False
        while rest:
            if end is not None:
                at = rest.find(end)
                if at < 0:
                    rest = ""
                    break
                rest = rest[at + len(end):].strip()
                end = None
                continue
            lowered = rest.lower()
            if any(lowered.startswith(prefix) for prefix in lang.line):
                rest = ""
                break
            if lang.block and rest.startswith(lang.block[0]):
                end = lang.block[1]
                rest = rest[len(lang.block[0]):]
                continue
            has_code = True
            break
        if has_code:
            code += 1
        else:
            comment += 1
    return code, comment, blank


def count_cases(text: str, lang: Language) -> int:
    if not lang.case_regex:
        return 0
    return len(re.findall(lang.case_regex, text, flags=re.MULTILINE))


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config(path: Path = CONFIG_PATH) -> dict:
    """The configuration, checked: a missing key is an error, not a silent default (a wrong exclusion list would change every figure)."""
    config = json.loads(path.read_text(encoding="utf-8"))
    problems = check_config(config)
    if problems:
        raise ValueError("code-stats-config.json: " + "; ".join(problems))
    return config


def check_config(config: object) -> list[str]:
    if not isinstance(config, dict):
        return ["not an object"]
    problems: list[str] = []
    for key, kind in (("owner", str), ("ecosystems", list), ("exclude_repos", list), ("types", dict), ("exclude", dict), ("tests", dict), ("translations", dict),
                      ("docs", dict), ("history", dict), ("clone", dict), ("declared_tests", dict)):
        if not isinstance(config.get(key), kind):
            problems.append(f"{key} is missing or has the wrong type")
    if problems:
        return problems
    keys = [e.get("key") for e in config["ecosystems"] if isinstance(e, dict)]
    if len(keys) != len(config["ecosystems"]) or len(set(keys)) != len(keys) or not all(isinstance(k, str) and k for k in keys):
        problems.append("ecosystems need distinct keys")
    for e in config["ecosystems"]:
        if not isinstance(e.get("prefixes"), list) or not e.get("prefixes") or not isinstance(e.get("label"), str):
            problems.append(f"ecosystem {e.get('key')}: label and prefixes are required")
    types = config["types"]
    if not isinstance(types.get("rules"), list) or not isinstance(types.get("order"), list) or not isinstance(types.get("default"), str):
        problems.append("types needs default, order and rules")
    else:
        known = set(types["order"])
        if types["default"] not in known:
            problems.append("types.default is not in types.order")
        for rule in types["rules"]:
            if not isinstance(rule, dict) or rule.get("type") not in known or not isinstance(rule.get("match"), list):
                problems.append(f"a type rule is wrong: {rule!r}")
    for section, names in (("exclude", ("dirs", "files", "binary_extensions")), ("tests", ("dirs", "files")), ("translations", ("dirs", "files", "extensions")),
                           ("docs", ("extensions", "not_docs"))):
        for name in names:
            if not isinstance(config[section].get(name), list):
                problems.append(f"{section}.{name} must be a list")
    for name in ("max_file_bytes", "max_line_chars"):
        if not isinstance(config["exclude"].get(name), int) or config["exclude"][name] <= 0:
            problems.append(f"exclude.{name} must be a positive number")
    for name in ("daily_days", "weekly_days", "max_points"):
        if not isinstance(config["history"].get(name), int) or config["history"][name] <= 0:
            problems.append(f"history.{name} must be a positive number")
    return problems


def _matches(name: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)


def ecosystem_of(name: str, config: Mapping) -> str | None:
    """The key of the ecosystem whose prefix the repository name starts with (the longest prefix wins), or None."""
    best: tuple[int, str] | None = None
    for eco in config["ecosystems"]:
        for prefix in eco["prefixes"]:
            if name == prefix or name.startswith(prefix):
                if best is None or len(prefix) > best[0]:
                    best = (len(prefix), eco["key"])
    return best[1] if best else None


def type_of(name: str, config: Mapping) -> str:
    """The first rule whose pattern matches the name; the default type otherwise."""
    for rule in config["types"]["rules"]:
        if _matches(name, rule["match"]):
            return rule["type"]
    return config["types"]["default"]


# ---------------------------------------------------------------------------
# Which file is what
# ---------------------------------------------------------------------------

def gitattributes_rules(text: str) -> list[tuple["re.Pattern[str]", bool]]:
    """[(regular expression of the path, excluded)] from a `.gitattributes`: `linguist-generated` and `linguist-vendored` set (not `-attr`, not `=false`).

    A later line wins over an earlier one, so a rule that unsets the attribute is kept as `False`.
    """
    rules: list[tuple[re.Pattern[str], bool]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        pattern, attrs = parts[0], parts[1:]
        verdict: bool | None = None
        for attr in attrs:
            name, _, value = attr.partition("=")
            plain = name.lstrip("-!")
            if plain not in ("linguist-generated", "linguist-vendored"):
                continue
            if name.startswith("-") or name.startswith("!") or value.lower() in ("false", "0"):
                verdict = False if verdict is None else verdict
            else:
                verdict = True
        if verdict is None:
            continue
        rules.append((_attribute_regex(pattern), verdict))
    return rules


def _attribute_regex(pattern: str) -> "re.Pattern[str]":
    anchored = pattern.startswith("/") or ("/" in pattern.rstrip("/"))
    directory = pattern.endswith("/")
    body = pattern.strip("/")
    out = ""
    i = 0
    while i < len(body):
        char = body[i]
        if char == "*":
            if body[i:i + 3] == "**/":
                out += "(?:.*/)?"
                i += 3
                continue
            if body[i:i + 2] == "**":
                out += ".*"
                i += 2
                continue
            out += "[^/]*"
        elif char == "?":
            out += "[^/]"
        else:
            out += re.escape(char)
        i += 1
    prefix = "" if anchored else "(?:.*/)?"
    suffix = "/.*" if directory else "(?:/.*)?"
    return re.compile("^" + prefix + out + suffix + "$")


def attributed(rel: str, rules: Sequence[tuple["re.Pattern[str]", bool]]) -> bool:
    verdict = False
    for regex, excluded in rules:
        if regex.match(rel):
            verdict = excluded
    return verdict


def is_test_path(rel: str, config: Mapping) -> bool:
    parts = rel.lower().split("/")
    dirs = {d.lower() for d in config["tests"]["dirs"]}
    if any(part in dirs for part in parts[:-1]):
        return True
    return _matches(rel.rsplit("/", 1)[-1], config["tests"]["files"])


def is_translation_path(rel: str, config: Mapping) -> bool:
    name = rel.rsplit("/", 1)[-1]
    if _matches(name, config["translations"]["files"]):
        return True
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    dirs = {d.lower() for d in config["translations"]["dirs"]}
    if ext in config["translations"]["extensions"] and any(part.lower() in dirs for part in rel.split("/")[:-1]):
        return True
    return bool(re.search(r"(^|/)values-[a-z]{2}(-r[A-Z]{2})?/", rel)) and ext == "xml"


def is_readme_translation(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    return bool(re.fullmatch(r"README(_[a-z]{3}|\.[a-z]{2}(-[A-Za-z]{2})?)\.md", name))


def classify(rel: str, config: Mapping) -> str:
    """'skip', 'l10n', 'doc', 'test', 'code' or 'data' for the path alone (the content decides what else is skipped)."""
    name = rel.rsplit("/", 1)[-1]
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    exclude = config["exclude"]
    if ext in exclude["binary_extensions"] or _matches(name, exclude["files"]):
        return "skip"
    if is_translation_path(rel, config) and not is_readme_translation(rel):
        return "l10n"
    if ext in config["docs"]["extensions"] and not _matches(name, config["docs"]["not_docs"]) and name not in BY_NAME:
        return "doc"
    if name in BY_NAME or ext in BY_EXTENSION:
        return "test" if is_test_path(rel, config) else "code"
    if ext in DATA_EXTENSIONS:
        return "data"
    return "skip"


def language_of(rel: str) -> Language | None:
    name = rel.rsplit("/", 1)[-1]
    if name in BY_NAME:
        return BY_NAME[name]
    return BY_EXTENSION.get(name.rsplit(".", 1)[-1].lower()) if "." in name else None


# ---------------------------------------------------------------------------
# One repository
# ---------------------------------------------------------------------------

def _blank_counts() -> dict:
    return {"files": 0, "code": 0, "comment": 0, "blank": 0}


def scan_tree(root: Path, config: Mapping) -> dict:
    """The figures of a directory (a clone): see the module text for what each block holds."""
    exclude = config["exclude"]
    skip_dirs = {d.lower() for d in exclude["dirs"]}
    attr_rules: list[tuple[re.Pattern[str], bool]] = []
    attributes = root / ".gitattributes"
    if attributes.is_file():
        try:
            attr_rules = gitattributes_rules(attributes.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            attr_rules = []

    langs: dict[str, dict] = {}
    code, tests = _blank_counts(), dict(_blank_counts(), cases=0)
    docs = {"files": 0, "lines": 0, "blank": 0}
    l10n = {"files": 0, "lines": 0}
    data = {"files": 0, "lines": 0}
    size = files = skipped = 0

    for current, dirs, names in os.walk(root, followlinks=False):
        rel_dir = Path(current).relative_to(root).as_posix()
        rel_dir = "" if rel_dir == "." else rel_dir
        dirs[:] = sorted(d for d in dirs if d.lower() not in skip_dirs and not os.path.islink(os.path.join(current, d))
                         and not attributed((rel_dir + "/" if rel_dir else "") + d + "/x", attr_rules))
        for name in sorted(names):
            rel = (rel_dir + "/" if rel_dir else "") + name
            path = Path(current) / name
            kind = classify(rel, config)
            if kind == "skip" or path.is_symlink() or attributed(rel, attr_rules):
                continue
            try:
                length = path.stat().st_size
                if length > exclude["max_file_bytes"]:
                    skipped += 1
                    continue
                raw = path.read_bytes()
            except OSError:
                skipped += 1
                continue
            if b"\0" in raw[:8000]:
                continue
            text = raw.decode("utf-8", errors="replace").lstrip("﻿")
            if max((len(line) for line in text.splitlines()), default=0) > exclude["max_line_chars"]:
                skipped += 1                              # minified or bundled: not written by hand
                continue
            lines = text.splitlines()
            total = len(lines)
            blank = sum(1 for line in lines if not line.strip())
            if is_readme_translation(rel):
                l10n["files"] += 1
                l10n["lines"] += total - blank
            if kind == "l10n":
                l10n["files"] += 1
                l10n["lines"] += total - blank
                continue
            if kind == "doc":
                docs["files"] += 1
                docs["lines"] += total - blank
                docs["blank"] += blank
                size += length
                files += 1
                continue
            if kind == "data":
                data["files"] += 1
                data["lines"] += total - blank
                continue
            lang = language_of(rel)
            if lang is None:
                continue
            c, m, b = count_lines(text, lang)
            bucket = tests if kind == "test" else code
            bucket["files"] += 1
            bucket["code"] += c
            bucket["comment"] += m
            bucket["blank"] += b
            if kind == "test":
                tests["cases"] += count_cases(text, lang)
            entry = langs.setdefault(lang.name, _blank_counts())
            entry["files"] += 1
            entry["code"] += c
            entry["comment"] += m
            entry["blank"] += b
            size += length
            files += 1
    return {"files": files, "size": size, "skipped": skipped, "langs": dict(sorted(langs.items())), "code": code, "tests": tests, "docs": docs,
            "l10n": l10n, "data": data}


# ---------------------------------------------------------------------------
# Git and GitHub
# ---------------------------------------------------------------------------

Runner = Callable[..., "subprocess.CompletedProcess[str]"]


def git_env(token: str | None) -> dict[str, str]:
    env = dict(os.environ)
    env.update({"GIT_TERMINAL_PROMPT": "0", "GIT_LFS_SKIP_SMUDGE": "1", "GIT_CONFIG_NOSYSTEM": "1"})
    if token:
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        env.update({"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader", "GIT_CONFIG_VALUE_0": f"AUTHORIZATION: basic {basic}"})
    return env


def clone(owner: str, name: str, dest: Path, token: str | None, timeout: int, run: Runner = subprocess.run) -> bool:
    command = ["git", "clone", "--depth", "1", "--quiet", "--no-tags", "--single-branch", "-c", "core.symlinks=false", "-c", "core.hooksPath=/dev/null",
               "-c", "advice.detachedHead=false", f"https://github.com/{owner}/{name}.git", str(dest)]
    try:
        done = run(command, env=git_env(token), capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError):
        return False
    return done.returncode == 0


def last_commit_day(path: Path, run: Runner = subprocess.run) -> str | None:
    try:
        done = run(["git", "-C", str(path), "log", "-1", "--format=%cs"], capture_output=True, text=True, timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return None
    text = done.stdout.strip()
    return text if done.returncode == 0 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", text) else None


def list_repos(owner: str, token: str | None, opener: Callable = urllib.request.urlopen) -> list[dict]:
    """The public repositories of the owner: [{name, pushed (YYYY-MM-DD), fork, archived}]. Raises when GitHub cannot be read."""
    out: list[dict] = []
    for page in range(1, 11):
        request = urllib.request.Request(f"{API}/users/{owner}/repos?per_page=100&type=owner&page={page}", headers={
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "code-stats"})
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        with opener(request, timeout=60) as response:
            batch = json.loads(response.read().decode("utf-8"))
        if not isinstance(batch, list):
            raise ValueError("unexpected answer of the repository list")
        for item in batch:
            if isinstance(item, dict) and isinstance(item.get("name"), str):
                out.append({"name": item["name"], "pushed": str(item.get("pushed_at") or "")[:10] or None,
                            "fork": bool(item.get("fork")), "archived": bool(item.get("archived"))})
        if len(batch) < 100:
            break
    return out


def select(repos: Sequence[Mapping], config: Mapping) -> list[dict]:
    """The repositories to measure, with their ecosystem and type, sorted by name."""
    chosen = []
    for repo in repos:
        name = repo["name"]
        if name in config["exclude_repos"] or (config.get("skip_forks") and repo.get("fork")) or (config.get("skip_archived") and repo.get("archived")):
            continue
        eco = ecosystem_of(name, config)
        if eco is None:
            continue
        chosen.append({"name": name, "eco": eco, "type": type_of(name, config), "pushed": repo.get("pushed")})
    return sorted(chosen, key=lambda r: r["name"])


def _remove_tree(path: Path) -> None:
    """Delete a clone; a read-only file (git objects on Windows) is made writable first."""
    def writable(function, target, _error):
        os.chmod(target, stat.S_IWRITE)
        function(target)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=writable)
    else:
        shutil.rmtree(path, onerror=writable)


def measure(repo: Mapping, config: Mapping, workdir: Path, token: str | None, local_root: Path | None = None,
            run: Runner = subprocess.run) -> tuple[dict | None, dict]:
    """(record or None when the repository could not be read, {path: text} of the declared-test files wanted from it)."""
    name = repo["name"]
    wanted = config["declared_tests"].get(name)
    if local_root is not None:
        target, owned = local_root / name, False
        if not target.is_dir():
            return None, {}
    else:
        target, owned = workdir / name, True
        if not clone(config["owner"], name, target, token, config["clone"].get("timeout_seconds", 300), run):
            if target.exists():
                _remove_tree(target)
            return None, {}
    try:
        figures = scan_tree(target, config)
        commit = last_commit_day(target, run) if (target / ".git").exists() else None
        side: dict = {}
        if wanted and (target / wanted).is_file():
            try:
                side[wanted] = (target / wanted).read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
    finally:
        if owned and target.exists():
            _remove_tree(target)
    record = {"eco": repo["eco"], "type": repo["type"], "state": "ok", "pushed": repo.get("pushed"), "commit": commit, **figures}
    return record, side


def declared_tests_from(text: str, repo: str) -> int | None:
    """`repos.<repo>.tests.count` of a glance file, when it is a real number."""
    try:
        value = json.loads(text)["repos"][repo]["tests"]["count"]
    except (ValueError, KeyError, TypeError):
        return None
    return value if isinstance(value, int) and not isinstance(value, bool) and 0 <= value < 10_000_000 else None


# ---------------------------------------------------------------------------
# Totals, the document and the history
# ---------------------------------------------------------------------------

def totals(repos: Mapping[str, Mapping]) -> dict:
    """Sums over the repositories that have figures (state ok or lastknown)."""
    out = {"repos": 0, "files": 0, "size": 0, "code": 0, "comment": 0, "blank": 0, "tests": 0, "test_files": 0, "cases": 0, "docs": 0, "l10n_files": 0, "data": 0}
    for record in repos.values():
        if record.get("state") not in ("ok", "lastknown"):
            continue
        out["repos"] += 1
        out["files"] += record["files"]
        out["size"] += record["size"]
        out["code"] += record["code"]["code"]
        out["comment"] += record["code"]["comment"]
        out["blank"] += record["code"]["blank"]
        out["tests"] += record["tests"]["code"]
        out["test_files"] += record["tests"]["files"]
        out["cases"] += record["tests"]["cases"]
        out["docs"] += record["docs"]["lines"]
        out["l10n_files"] += record["l10n"]["files"]
        out["data"] += record["data"]["lines"]
    return out


def _group(repos: Mapping[str, Mapping], field: str) -> dict:
    groups: dict[str, dict] = {}
    for record in repos.values():
        if record.get("state") not in ("ok", "lastknown"):
            continue
        entry = groups.setdefault(record[field], {"repos": 0, "code": 0, "tests": 0, "docs": 0})
        entry["repos"] += 1
        entry["code"] += record["code"]["code"]
        entry["tests"] += record["tests"]["code"]
        entry["docs"] += record["docs"]["lines"]
    return dict(sorted(groups.items()))


def snapshot_point(day: str, repos: Mapping[str, Mapping]) -> dict:
    """One point of the history: the totals, by ecosystem and by type."""
    whole = totals(repos)
    return {"d": day, "t": {k: whole[k] for k in ("repos", "code", "comment", "tests", "docs", "files", "size", "cases", "l10n_files")},
            "e": _group(repos, "eco"), "y": _group(repos, "type")}


def make_document(day: str, config: Mapping, repos: Mapping[str, Mapping]) -> dict:
    return {"schema": SCHEMA, "day": day, "owner": config["owner"],
            "ecosystems": [{"key": e["key"], "label": e["label"]} for e in config["ecosystems"]],
            "types": list(config["types"]["order"]),
            "repos": dict(sorted(repos.items())), "totals": totals(repos)}


def prune_history(points: Sequence[Mapping], today: str, config: Mapping) -> list[dict]:
    """Every day for `daily_days`, then the last point of each week up to `weekly_days`, then the last of each month; at most `max_points` (the newest)."""
    limits = config["history"]
    now = date.fromisoformat(today)
    unique: dict[str, dict] = {}
    for point in points:
        try:
            date.fromisoformat(point["d"])
        except (KeyError, ValueError, TypeError):
            continue
        unique[point["d"]] = dict(point)
    ordered = [unique[d] for d in sorted(unique)]
    keep: dict[object, dict] = {}
    for point in ordered:
        age = (now - date.fromisoformat(point["d"])).days
        day = date.fromisoformat(point["d"])
        if age <= limits["daily_days"]:
            key: object = ("d", point["d"])
        elif age <= limits["weekly_days"]:
            iso = day.isocalendar()
            key = ("w", iso[0], iso[1])
        else:
            key = ("m", day.year, day.month)
        keep[key] = point              # a later point of the same period replaces the earlier one
    result = sorted(keep.values(), key=lambda p: p["d"])
    return result[-limits["max_points"]:]


def merge_history(old: Sequence[Mapping], point: Mapping | None, today: str, config: Mapping) -> list[dict]:
    points = [p for p in old if p.get("d") != (point or {}).get("d")]
    if point is not None:
        points.append(dict(point))
    return prune_history(points, today, config)


def read_json(path: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_previous(out_dir: Path) -> tuple[dict, list[dict]]:
    stats = read_json(out_dir / STATS_FILE)
    history = read_json(out_dir / HISTORY_FILE)
    repos = stats.get("repos") if isinstance(stats, dict) and isinstance(stats.get("repos"), dict) else {}
    points = history.get("points") if isinstance(history, dict) and isinstance(history.get("points"), list) else []
    return repos, [p for p in points if isinstance(p, dict)]


def render(document: object) -> str:
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def run_all(config: Mapping, out_dir: Path, workdir: Path, token: str | None, today: str, *, repos: Sequence[Mapping] | None = None,
            local_root: Path | None = None, run: Runner = subprocess.run, log: Callable[[str], None] = lambda text: print(text, file=sys.stderr)) -> dict:
    """Measure everything and write both documents into `out_dir`. Returns {'fresh': n, 'wanted': n, 'history_written': bool}."""
    listing = list(repos) if repos is not None else list_repos(config["owner"], token)
    chosen = select(listing, config)
    previous, old_points = load_previous(out_dir)
    log(f"{len(chosen)} repositories to measure.")

    def one(repo: Mapping):
        try:
            return repo, *measure(repo, config, workdir, token, local_root, run)
        except Exception as error:               # one broken repository must not stop the others
            log(f"{repo['name']}: {type(error).__name__}")
            return repo, None, {}

    workers = 1 if local_root is not None else max(1, int(config["clone"].get("workers", 4)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, chosen))

    records: dict[str, dict] = {}
    side: dict[str, dict] = {}
    fresh = 0
    for repo, record, extra in results:
        name = repo["name"]
        if record is not None:
            records[name] = record
            side[name] = extra
            fresh += 1
        elif isinstance(previous.get(name), dict) and previous[name].get("state") in ("ok", "lastknown"):
            kept = dict(previous[name])
            kept.update({"state": "lastknown", "eco": repo["eco"], "type": repo["type"]})
            records[name] = kept
            log(f"{name}: could not be read, the last known figures are kept.")
        else:
            records[name] = {"eco": repo["eco"], "type": repo["type"], "state": "unread", "pushed": repo.get("pushed")}
            log(f"{name}: could not be read.")

    declared: dict[str, int] = {}
    for docs_repo, path in config["declared_tests"].items():
        text = side.get(docs_repo, {}).get(path)
        if text is None:
            continue
        for name in records:
            count = declared_tests_from(text, name)
            if count is not None:
                declared[name] = count
    for name, record in records.items():
        if record.get("state") in ("ok", "lastknown"):
            if name in declared:
                record["declared_tests"] = declared[name]
            elif record["state"] == "ok":
                record.pop("declared_tests", None)

    document = make_document(today, config, records)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / STATS_FILE).write_text(render(document), encoding="utf-8", newline="\n")
    enough = bool(chosen) and fresh * 2 >= len(chosen)
    points = merge_history(old_points, snapshot_point(today, records) if enough else None, today, config)
    (out_dir / HISTORY_FILE).write_text(render({"schema": SCHEMA, "points": points}), encoding="utf-8", newline="\n")
    log(f"{fresh} of {len(chosen)} repositories measured now; {document['totals']['code']} lines of code in {document['totals']['repos']}.")
    if not enough:
        log("Fewer than half of the repositories could be read: today's point is not added to the history.")
    return {"fresh": fresh, "wanted": len(chosen), "history_written": enough}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Code statistics of the repositories of the ecosystems.")
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--out", type=Path, default=ROOT / "data", help="directory that holds code-stats.json and code-history.json")
    parser.add_argument("--workdir", type=Path, default=None, help="directory for the temporary clones (default: a new temporary one)")
    parser.add_argument("--local-root", type=Path, default=None, help="count DIR/<repository> instead of cloning")
    args = parser.parse_args(argv)
    config = load_config(args.config)
    token = os.environ.get("GITHUB_TOKEN") or None
    today = datetime.now(timezone.utc).date().isoformat()
    created = args.workdir is None
    workdir = Path(tempfile.mkdtemp(prefix="code-stats-")) if created else args.workdir
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        result = run_all(config, args.out, workdir, token, today, local_root=args.local_root)
    except (urllib.error.URLError, OSError, ValueError) as error:
        print(f"The repositories could not be listed ({type(error).__name__}); nothing was changed.", file=sys.stderr)
        return 1
    finally:
        if created:
            shutil.rmtree(workdir, ignore_errors=True)
    if result["fresh"] == 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
