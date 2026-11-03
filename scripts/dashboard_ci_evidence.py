#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_ci_evidence.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Technical evidence published by the CI of the repositories, read by the status dashboard: declared against verified.

The manifest of a repository DECLARES how far it has been proven (`evidence`: none, host-test, simulator, bench, field). That is a claim.
A repository whose CI publishes a record of what ran (see docs/evidence-schema.json and docs/CI_EVIDENCE.md) lets the dashboard VERIFY it:

  * a record that passed, on the default branch and not older than the limit of its kind, proves its level;
  * the verified level is the highest proven one; "bench" and "field" need a record that names the hardware;
  * a repository that declares more than it proves is shown as such; one that publishes nothing is "not verified" (never "verified", never "failed").

The states of a repository: verified, below (declares more than it proves), failing (the latest relevant run failed), expired (it only has
old records), nodata (nothing published), invalid (records that break the schema), unread (the records could not be read in this build).

The decision logic is pure and takes plain data; the network sits in `read_all`, which takes the fetch function as an argument so the tests
can simulate every case. The limits come from dashboard-config.json (`ci_evidence`). Stdlib only.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Callable, Iterable, Mapping

SCHEMA_VERSION = "1.0"
LEVELS = ("none", "host-test", "simulator", "bench", "field")
RANK = {level: index for index, level in enumerate(LEVELS)}
# The level of evidence each kind of test proves.
LEVEL_OF_TYPE = {"unit": "host-test", "integration": "host-test", "host-test": "host-test", "simulator": "simulator", "bench": "bench", "field": "field"}
TEST_TYPES = tuple(LEVEL_OF_TYPE)
RESULTS = ("pass", "fail", "partial", "skipped")
HARDWARE_LEVELS = ("bench", "field")
STATES = ("verified", "below", "failing", "expired", "nodata", "invalid", "unread")
REQUIRED = ("repo", "workflow", "commit", "branch", "date", "version", "test_type", "result", "environment", "hardware", "url")
MAX_RECORDS = 50      # the most records of one repository that are looked at
DEFAULT_CONFIG: dict = {
    "branch": "ci-evidence",
    "path": "ci-evidence.json",
    "default_branches": ["main"],
    "expire_days": {"host-test": 14, "simulator": 30, "bench": 180, "field": 365},
}
_COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2})(?::(\d{2}))?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?$")

# (status, payload): ("ok", parsed JSON) | ("absent", None) | ("error", message)
Fetch = Callable[[str, str, str], "tuple[str, object]"]


def parse_config(raw: object) -> "tuple[dict, list[str]]":
    """(config, problems): every part that is wrong is replaced by its default and named in the problems."""
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["ci_evidence: needs an object"]
    for key in ("branch", "path"):
        if key in raw:
            if isinstance(raw[key], str) and re.fullmatch(r"[A-Za-z0-9._/-]{1,100}", raw[key]) and ".." not in raw[key] and not raw[key].startswith("/"):
                config[key] = raw[key]
            else:
                problems.append(f"ci_evidence.{key}: needs a plain branch or file name")
    if "default_branches" in raw:
        value = raw["default_branches"]
        if isinstance(value, list) and value and all(isinstance(v, str) and v for v in value):
            config["default_branches"] = list(value)
        else:
            problems.append("ci_evidence.default_branches: needs a list of branch names")
    if "expire_days" in raw:
        value = raw["expire_days"]
        if isinstance(value, Mapping) and set(value) <= set(DEFAULT_CONFIG["expire_days"]) and all(isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 3650 for v in value.values()):
            config["expire_days"].update(value)
        else:
            problems.append("ci_evidence.expire_days: needs integer days from 1 to 3650 for host-test, simulator, bench and field")
    return config, problems


def load_config(path=None) -> "tuple[dict, list[str]]":
    """The `ci_evidence` part of dashboard-config.json (the limits and the place the records are read from)."""
    from pathlib import Path
    target = Path(path) if path else Path(__file__).resolve().parent.parent / "dashboard-config.json"
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return json.loads(json.dumps(DEFAULT_CONFIG)), [f"{target.name}: {exc}"]
    config, problems = parse_config(raw.get("ci_evidence") if isinstance(raw, Mapping) else None)
    return config, [f"{target.name}: {p}" for p in problems]


def parse_date(text: object) -> "datetime | None":
    match = _DATE_RE.match(text) if isinstance(text, str) else None
    if not match:
        return None
    year, month, day, hour, minute, second = (int(g) if g else 0 for g in match.groups())
    try:
        return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    except ValueError:
        return None


def validate_record(record: object, repo: str, owner: str) -> "tuple[dict | None, list[str]]":
    """(clean record, problems). A record with any problem is dropped: evidence that cannot be trusted proves nothing."""
    if not isinstance(record, Mapping):
        return None, ["a record is not an object"]
    problems: list[str] = []
    for key in REQUIRED:
        if key not in record:
            problems.append(f"{key} is missing")
    if problems:
        return None, problems
    if record["repo"] != repo:
        problems.append(f"repo {record['repo']!r} is not the repository that published it")
    for key in ("workflow", "version", "environment", "branch"):
        if not isinstance(record[key], str) or not record[key].strip():
            problems.append(f"{key} must be a non-empty text")
    if not isinstance(record["commit"], str) or not _COMMIT_RE.match(record["commit"]):
        problems.append("commit must be a hexadecimal commit id")
    if parse_date(record["date"]) is None:
        problems.append("date must be an ISO 8601 date")
    if record["test_type"] not in TEST_TYPES:
        problems.append(f"test_type {record['test_type']!r} is not one of {'|'.join(TEST_TYPES)}")
    if record["result"] not in RESULTS:
        problems.append(f"result {record['result']!r} is not one of {'|'.join(RESULTS)}")
    prefix = f"https://github.com/{owner}/{repo}/"
    if not isinstance(record["url"], str) or not record["url"].startswith(prefix):
        problems.append(f"url must be a link inside {prefix}")
    hardware = record["hardware"]
    if hardware is not None and not (isinstance(hardware, Mapping) and isinstance(hardware.get("bound"), bool)):
        problems.append("hardware must be null or an object with a boolean 'bound'")
    elif record["test_type"] in HARDWARE_LEVELS and not (isinstance(hardware, Mapping) and hardware.get("bound") is True
                                                         and isinstance(hardware.get("device"), str) and hardware["device"].strip()):
        problems.append(f"a {record['test_type']} record must name the hardware (hardware.bound true and hardware.device)")
    if problems:
        return None, problems
    clean = {key: record[key] for key in REQUIRED}
    return clean, []


def evaluate(declared: object, records: "list | None", *, repo: str, owner: str, today: str, config: Mapping, error: str = "") -> dict:
    """The verdict for one repository.
    `records` is None when the repository publishes nothing (no file) and `error` is set when the file could not be read."""
    declared_level = declared if declared in RANK else None
    out = {"declared": declared_level or "", "verified": "", "state": "nodata", "date": "", "url": "", "tests": [], "invalid": 0, "reason": ""}
    if error:
        out.update(state="unread", reason=error)
        return out
    if not records:
        return out
    now = parse_date(today) or datetime.now(timezone.utc)
    default_branches = list(config.get("default_branches") or DEFAULT_CONFIG["default_branches"])
    limits = config.get("expire_days") or DEFAULT_CONFIG["expire_days"]
    valid: list = []
    invalid = 0
    for raw in records[:MAX_RECORDS]:
        clean, problems = validate_record(raw, repo, owner)
        if clean is None:
            invalid += 1
            if not out["reason"]:
                out["reason"] = problems[0]
        else:
            valid.append(clean)
    out["invalid"] = invalid
    shown = []
    fresh_pass: list = []
    fresh_fail: list = []
    expired_any = False
    for rec in valid:
        if rec["branch"] not in default_branches:
            continue
        level = LEVEL_OF_TYPE[rec["test_type"]]
        when = parse_date(rec["date"])
        age = (now - when).days if when else None
        stale = age is None or age > limits.get(level, DEFAULT_CONFIG["expire_days"][level]) or age < -1
        shown.append([rec["test_type"], rec["result"], rec["date"][:10], not stale])
        if stale:
            expired_any = True
        elif rec["result"] == "pass":
            fresh_pass.append((RANK[level], rec))
        elif rec["result"] == "fail":
            fresh_fail.append((RANK[level], rec))
    out["tests"] = sorted(shown, key=lambda r: r[2], reverse=True)[:8]
    if not valid:
        out["state"] = "invalid"
        return out
    if not shown:
        out["state"] = "nodata"
        out["reason"] = out["reason"] or "no record on the default branch"
        return out
    best_rank = max((r for r, _ in fresh_pass), default=0)
    out["verified"] = LEVELS[best_rank] if fresh_pass else "none"
    if fresh_pass:
        top = max(fresh_pass, key=lambda pair: (pair[0], pair[1]["date"]))[1]
        out["date"], out["url"] = top["date"][:10], top["url"]
    need = RANK.get(declared_level, 0) if declared_level else 0
    best_fail = max((r for r, _ in fresh_fail), default=-1)
    if not fresh_pass and not fresh_fail and expired_any:
        out["state"] = "expired"
        latest = max((r for r in valid if r["branch"] in default_branches), key=lambda r: r["date"])
        out["date"], out["url"] = latest["date"][:10], latest["url"]
    elif fresh_pass and best_rank >= need and best_fail <= best_rank:
        out["state"] = "verified"
    elif fresh_fail and best_fail > (best_rank if fresh_pass else -1):
        out["state"] = "failing"
        failed = max(fresh_fail, key=lambda pair: (pair[0], pair[1]["date"]))[1]
        out["date"], out["url"] = failed["date"][:10], failed["url"]
    elif fresh_pass and best_rank >= need:
        out["state"] = "verified"
    elif need > 0 or fresh_pass:
        out["state"] = "below"
    else:
        out["state"] = "nodata"
        out["reason"] = out["reason"] or "only partial or skipped runs"
    return out


def build(declared: Mapping[str, object], read: "Mapping | None", *, owner: str, today: str, config: Mapping) -> dict:
    """The block the page embeds. `read` is {"records": {repo: [..]}, "errors": {repo: text}} or None when nothing was read in this build."""
    repos: dict = {}
    for name, level in declared.items():
        if read is None:
            repos[name] = evaluate(level, None, repo=name, owner=owner, today=today, config=config, error="not read in this build")
        else:
            repos[name] = evaluate(level, (read.get("records") or {}).get(name), repo=name, owner=owner, today=today, config=config, error=(read.get("errors") or {}).get(name, ""))
    return {"read": read is not None, "source": f"{config['branch']}:{config['path']}", "expire": dict(config["expire_days"]), "today": today, "repos": repos}


def counts(block: Mapping) -> dict:
    """{state: number of repositories}, every state present."""
    tally = {state: 0 for state in STATES}
    for item in (block.get("repos") or {}).values():
        tally[item["state"]] += 1
    return tally


def read_all(owner: str, names: Iterable[str], fetch: Fetch, config: Mapping, workers: int = 8) -> dict:
    """{"records": {repo: [..]}, "errors": {repo: text}}: the evidence file of every repository. A repository without the file is simply absent from both."""
    result: dict = {"records": {}, "errors": {}}

    def one(name: str):
        status, payload = fetch(name, config["branch"], config["path"])
        if status == "absent":
            return name, None, ""
        if status == "error":
            return name, None, str(payload)
        if isinstance(payload, Mapping) and isinstance(payload.get("records"), list):
            if payload.get("schema_version") != SCHEMA_VERSION:
                return name, None, f"unknown schema_version {payload.get('schema_version')!r}"
            return name, payload["records"], ""
        return name, None, "the file is not an object with a 'records' list"

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for name, records, error in pool.map(one, list(names)):
            if error:
                result["errors"][name] = error
            elif records is not None:
                result["records"][name] = records
    return result


def raw_fetch(owner: str, timeout: float = 15) -> Fetch:
    """A `fetch` for `read_all`: one file of a branch from raw.githubusercontent.com (no API quota)."""
    def run(repo: str, branch: str, path: str):
        request = urllib.request.Request(f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}", headers={"User-Agent": "JuanenRac-dashboard-ci-evidence"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                text = response.read(2_000_000).decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            return ("absent", None) if exc.code == 404 else ("error", f"HTTP {exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return "error", f"lookup failed: {exc}"
        try:
            return "ok", json.loads(text)
        except ValueError as exc:
            return "error", f"not valid JSON: {exc}"
    return run
