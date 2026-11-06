#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_sentinel.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Sentinel" of the status dashboard: a public-safe watch over the repositories of the ecosystem, decided by rules (no AI).

It answers six questions from public data only, read once in the job that builds the dashboard with the read-only token of the workflow:

  * ci          which workflows are red: the LAST finished run of each workflow on the default branch (cancelled and skipped runs do not count),
  * releases    which repositories are ready for a new version: at least `candidate_min_entries` entries under `[Unreleased]` in the CHANGELOG and a last
                release older than `candidate_days` days (or none),
  * signatures  the state of the signature of the latest release (verified by the signature module; here only counted),
  * hygiene     public settings: an active ruleset `protect-main`; SHA-pinned actions and the allowed actions when the token may read them (the settings
                endpoint needs the admin right of the repository, so with the read-only token they are usually "not verified", never green),
  * compute     approximate minutes of computing (taken from the builds block of the page),
  * trend       the daily figures kept in data/history.json.

WHAT IS NEVER PUBLISHED (by design, and enforced by `clean`, which rebuilds the document from a whitelist): the alerts of code scanning, dependencies and secret
scanning (not even a count), titles of pull requests and issues, people, branches, commit texts, workflow titles or anything written by an outside person.
The document only holds names of repositories of this owner, counts, file names of workflows, version tags and dates.

The result is written to `data/sentinel.json` (the same document the page embeds). All times are absolute UTC moments so an unchanged situation gives an
identical file and the bot makes no commit. Stdlib only.
"""
from __future__ import annotations

import json
import os
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import ci_rules
import dashboard_actions

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sentinel.json"
CONFIG_PATH = Path(__file__).resolve().parent.parent / "dashboard-config.json"
SCHEMA = 1
BAD = ci_rules.RED_CONCLUSIONS             # one criterion for the whole dashboard (see ci_rules.py)
IGNORED = ci_rules.IGNORED_CONCLUSIONS
SIGNATURE_STATES = ("verified", "invalid", "unverifiable", "none", "norelease", "unverified")
SECTIONS = ("ci", "releases", "signatures", "hygiene", "compute", "trend", "ecosystems", "events")
DEFAULT_CONFIG: dict = {
    "enabled": True,
    "candidate_days": 2.0,
    "candidate_min_entries": 1,
    "skip_candidate_prefixes": ["EH3D-", "ELECTRO-HOBBY-3D"],
    "red_streak_warn": 2,
    "compute_warn_minutes_24h": 12000,
    "compute_top": 6,
    "ruleset_name": "protect-main",
    "read_actions_settings": True,
    "list_max": 40,
    "events_max": 30,
    "stale_hours": 6,
    "sections": {name: True for name in SECTIONS},
}
REPO_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
WORKFLOW_RE = re.compile(r"^[A-Za-z0-9_.-]{1,60}\.ya?ml$")
TAG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,39}$")
TIME_RE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
ECO_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,29}$")
EVENT_KINDS = ("red_new", "red_ok", "released")
VERSION_RE = re.compile(r"^v?(\d+(?:\.\d+){0,5})")

QUERY = """
query($owner: String!, $cursor: String) {
  repositoryOwner(login: $owner) {
    repositories(first: 20, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        isArchived
        defaultBranchRef { name }
        latestRelease { tagName publishedAt isDraft }
        changelog: object(expression: "HEAD:CHANGELOG.md") { ... on Blob { text } }
        workflows: object(expression: "HEAD:.github/workflows") { ... on Tree { entries { name } } }
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def check_config(raw: object) -> tuple[dict, list[str]]:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["sentinel: not an object"]
    for key in ("enabled", "read_actions_settings"):
        if key in raw:
            if isinstance(raw[key], bool):
                config[key] = raw[key]
            else:
                problems.append(f"sentinel.{key}: needs true or false")
    for key, low, high in (("candidate_days", 0, 365), ("compute_warn_minutes_24h", 1, 100000)):
        if key in raw:
            value = raw[key]
            if isinstance(value, (int, float)) and not isinstance(value, bool) and low <= value <= high:
                config[key] = value
            else:
                problems.append(f"sentinel.{key}: needs a number from {low} to {high}")
    for key, low, high in (("candidate_min_entries", 1, 100), ("red_streak_warn", 1, 100), ("compute_top", 1, 30), ("list_max", 5, 200), ("stale_hours", 1, 168), ("events_max", 5, 200)):
        if key in raw:
            value = raw[key]
            if isinstance(value, int) and not isinstance(value, bool) and low <= value <= high:
                config[key] = value
            else:
                problems.append(f"sentinel.{key}: needs an integer from {low} to {high}")
    if "skip_candidate_prefixes" in raw:
        value = raw["skip_candidate_prefixes"]
        if isinstance(value, list) and all(isinstance(p, str) and p for p in value):
            config["skip_candidate_prefixes"] = list(value)
        else:
            problems.append("sentinel.skip_candidate_prefixes: needs a list of texts")
    if "ruleset_name" in raw:
        value = raw["ruleset_name"]
        if isinstance(value, str) and 0 < len(value) <= 60:
            config["ruleset_name"] = value
        else:
            problems.append("sentinel.ruleset_name: needs a text")
    if "sections" in raw:
        value = raw["sections"]
        if isinstance(value, Mapping) and all(k in SECTIONS and isinstance(v, bool) for k, v in value.items()):
            config["sections"] = {name: bool(value.get(name, True)) for name in SECTIONS}
        else:
            problems.append("sentinel.sections: needs true or false for " + ", ".join(SECTIONS))
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return check_config(None)
    except (OSError, ValueError) as exc:
        return check_config(None)[0], [f"{path.name} could not be read for the sentinel ({exc})"]
    return check_config(raw.get("sentinel") if isinstance(raw, Mapping) else None)


# ---------------------------------------------------------------------------
# Pure rules (the same criteria as the local monitor of the owner)
# ---------------------------------------------------------------------------

def _stamp(value: object) -> str | None:
    """A UTC moment as `YYYY-MM-DDTHH:MM:SSZ`, or None."""
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


def _parse(value: object) -> datetime | None:
    text = _stamp(value)
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if text else None


def unreleased_count(text: object) -> int | None:
    """Entries (`- ` or `* `) under `## [Unreleased]` of a CHANGELOG; None when there is no CHANGELOG text."""
    if not isinstance(text, str):
        return None
    text = text.replace("\r\n", "\n")
    found = re.search(r"^## \[Unreleased\]\s*\n(.*?)(?=^## \[|\Z)", text, re.S | re.M)
    return len(re.findall(r"^\s*[-*] ", found.group(1) if found else "", re.M))


def red_workflows(runs: Iterable[object], current: Sequence[str] | None = None) -> tuple[list[dict], int]:
    """(red, checked). `runs` are the finished runs of the default branch ({path, conclusion, at}). Single criterion: the last run of each workflow that is not
    cancelled/skipped/neutral decides; a workflow is red when it failed; the streak counts the failures in a row. `current` (file names that exist now) drops
    the workflows that were deleted and would stay red for ever."""
    series: dict[str, list[dict]] = {}
    for run in sorted((r for r in runs if isinstance(r, Mapping)), key=lambda r: str(r.get("at") or "")):
        path = str(run.get("path") or "")
        base = path.rsplit("/", 1)[-1]
        if not ci_rules.decides(run) or not WORKFLOW_RE.match(base):
            continue
        if current is not None and base not in current:
            continue
        series.setdefault(base, []).append(run)
    out = []
    for base, items in sorted(series.items()):
        if items[-1].get("conclusion") not in BAD:
            continue
        streak = 0
        for run in reversed(items):
            if run.get("conclusion") not in BAD:
                break
            streak += 1
        out.append({"wf": base, "streak": streak, "since": _stamp(items[-1].get("at"))})
    return out, len(series)


def release_candidates(unreleased: Mapping[str, int], published: Mapping[str, str | None], tags: Mapping[str, str], now: datetime, days: float, min_entries: int,
                       skip_prefixes: Sequence[str] = ()) -> list[dict]:
    """Rule of the owner: >= `min_entries` under [Unreleased] and a last release older than `days` (or no release at all)."""
    rows = []
    for repo, count in unreleased.items():
        if repo.startswith(tuple(skip_prefixes)) or count < min_entries:
            continue
        moment = _parse(published.get(repo))
        if moment is not None and (now - moment).total_seconds() / 86400 <= days:
            continue
        rows.append({"repo": repo, "entries": count, "tag": tags.get(repo, "") if moment else "", "published": _stamp(published.get(repo))})
    return sorted(rows, key=lambda r: (-r["entries"], r["repo"]))


def version_key(text: object) -> tuple[int, ...] | None:
    """The numbers of a version or tag ("v0.8.0.1" -> (0, 8, 0, 1)); None when it does not start with a number. Missing trailing parts count as zero."""
    found = VERSION_RE.match(str(text or "").strip())
    if not found:
        return None
    parts = [int(p) for p in found.group(1).split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def unpublished_versions(versions: Mapping[str, str | None], tags: Mapping[str, str], skip_prefixes: Sequence[str] = ()) -> list[dict]:
    """Repositories whose manifest declares a newer version than their latest release: a version that was raised and never published. A repository
    without any release, or with a version that is not numeric, is not listed (nothing was raised over a published version)."""
    rows = []
    for repo, version in versions.items():
        if repo.startswith(tuple(skip_prefixes)):
            continue
        tag = tags.get(repo) or ""
        declared, released = version_key(version), version_key(tag)
        if declared is None or released is None or declared <= released:
            continue
        rows.append({"repo": repo, "version": str(version).strip(), "tag": tag})
    return sorted(rows, key=lambda r: r["repo"])


def ecosystem_table(names: Iterable[str], ecosystem_of: Mapping[str, str], ok: Iterable[str], red: Iterable[Mapping], candidates: Iterable[Mapping],
                    unpublished: Iterable[Mapping]) -> dict[str, dict]:
    """{ecosystem: {repos, read, red (repositories with a red workflow), cand, unpub}} from the same lists the rest of the tab uses."""
    ok = set(ok)
    red_repos = {r["repo"] for r in red}
    cand_repos = {c["repo"] for c in candidates}
    unpub_repos = {u["repo"] for u in unpublished}
    table: dict[str, dict] = {}
    for name in sorted(set(names)):
        eco = str(ecosystem_of.get(name) or "other")
        row = table.setdefault(eco, {"repos": 0, "read": 0, "red": 0, "cand": 0, "unpub": 0})
        row["repos"] += 1
        row["read"] += name in ok
        row["red"] += name in red_repos
        row["cand"] += name in cand_repos
        row["unpub"] += name in unpub_repos
    return table


def new_events(saved: Mapping | None, red: Iterable[Mapping], ok: Iterable[str], tags: Mapping[str, str], at: str | None, limit: int) -> list[dict]:
    """The feed: what changed since the saved reading (a workflow that turned red or green again, a release that appeared), newest first, the saved ones after.
    Nothing is invented without a previous reading, and a repository that could not be read this time cannot recover or fail."""
    if not isinstance(saved, Mapping) or at is None:
        return []
    old = [e for e in (saved.get("events") or []) if isinstance(e, Mapping)]
    found: list[dict] = []
    ci = saved.get("ci") if isinstance(saved.get("ci"), Mapping) else {}
    saved_red = ci.get("red") if isinstance(ci.get("red"), list) else []
    if ci.get("red_total") == len(saved_red):                       # a cut list cannot tell what recovered
        before = {(r["repo"], r["wf"]) for r in saved_red if isinstance(r, Mapping) and "repo" in r and "wf" in r}
        now = {(r["repo"], r["wf"]) for r in red}
        readable = set(ok)
        found += [{"at": at, "kind": "red_new", "repo": repo, "wf": wf} for repo, wf in sorted(now - before)]
        found += [{"at": at, "kind": "red_ok", "repo": repo, "wf": wf} for repo, wf in sorted(before - now) if repo in readable]
    before_tags = saved.get("tags") if isinstance(saved.get("tags"), Mapping) else None
    if before_tags:
        found += [{"at": at, "kind": "released", "repo": repo, "tag": tag} for repo, tag in sorted(tags.items()) if tag and before_tags.get(repo) != tag]
    return (found + old)[:limit]


def ruleset_active(rulesets: object, name: str) -> bool | None:
    """True/False for a readable list of rulesets; None when it could not be read."""
    if not isinstance(rulesets, list):
        return None
    return any(isinstance(r, Mapping) and r.get("name") == name and str(r.get("enforcement", "")).lower() == "active" for r in rulesets)


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

def _slim_runs(payload: object) -> list[dict] | None:
    if not isinstance(payload, Mapping) or not isinstance(payload.get("workflow_runs"), list):
        return None
    out = []
    for run in payload["workflow_runs"]:
        if isinstance(run, Mapping):
            out.append({"path": run.get("path"), "conclusion": run.get("conclusion"), "event": run.get("event"), "at": run.get("updated_at") or run.get("created_at")})
    return out


def list_repos(owner: str, token: str, post=dashboard_actions.graphql_post, max_pages: int = 20) -> dict[str, dict] | None:
    """{repository: {branch, tag, published, changelog (entries or None), workflows (file names)}} or None when GitHub did not answer."""
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard-sentinel", "Content-Type": "application/json"}
    found: dict[str, dict] = {}
    cursor = None
    for _ in range(max_pages):
        body = json.dumps({"query": QUERY, "variables": {"owner": owner, "cursor": cursor}}).encode("utf-8")
        answer = post(body, headers) or post(body, headers)
        try:
            page = answer["data"]["repositoryOwner"]["repositories"]
            for node in page["nodes"]:
                if not isinstance(node, Mapping) or not node.get("name") or node.get("isArchived"):
                    continue
                release = node.get("latestRelease") or {}
                draft = bool(release.get("isDraft"))
                entries = (node.get("workflows") or {}).get("entries") or []
                found[str(node["name"])] = {
                    "branch": ((node.get("defaultBranchRef") or {}).get("name")) or "main",
                    "tag": None if draft else release.get("tagName"), "published": None if draft else release.get("publishedAt"),
                    "entries": unreleased_count((node.get("changelog") or {}).get("text")),
                    "workflows": [str(e.get("name")) for e in entries if isinstance(e, Mapping) and str(e.get("name", "")).lower().endswith((".yml", ".yaml"))]}
            if not page["pageInfo"]["hasNextPage"]:
                return found
            cursor = page["pageInfo"]["endCursor"]
        except (TypeError, KeyError, ValueError):
            return None
    return found


def read_all(owner: str, names: Iterable[str], token: str, config: Mapping | None = None, now: datetime | None = None,
             post=dashboard_actions.graphql_post, get=None, workers: int = 8) -> dict | None:
    """{"asof", "repos": {name: record}} or None when the list of repositories could not be read at all. A record is `{"state": "unread"}` when a lookup failed."""
    config = config or check_config(None)[0]
    now = (now or datetime.now(timezone.utc)).replace(microsecond=0)
    listing = list_repos(owner, token, post)
    if listing is None:
        return None
    get = get or dashboard_actions.rest_get(token)
    wanted = sorted(set(names))
    settings_ok = bool(config.get("read_actions_settings"))
    if settings_ok:
        # The settings endpoint needs the admin right of the repository: if none of the first three answers, it is not asked again (the answer would be the same).
        for name in [n for n in wanted if n in listing][:3]:
            if get(f"https://api.github.com/repos/{owner}/{name}/actions/permissions")[0] == "ok":
                break
        else:
            settings_ok = False

    def one(name: str):
        info = listing.get(name)
        if info is None:
            return name, {"state": "unread"}
        base = f"https://api.github.com/repos/{owner}/{name}"
        record: dict = {"state": "ok", "tag": info["tag"], "published": info["published"], "entries": info["entries"], "ci": None, "checked": 0, "rs": None, "perm": None}
        if info["workflows"]:
            status, payload = get(f"{base}/actions/runs?" + urllib.parse.urlencode({"branch": info["branch"], "status": "completed", "per_page": 100, "exclude_pull_requests": "true"}))
            runs = _slim_runs(payload) if status == "ok" else None
            if runs is None:
                record["state"] = "unread"
            else:
                record["ci"], record["checked"] = red_workflows(runs, info["workflows"])
        else:
            record["ci"] = []
        status, payload = get(f"{base}/rulesets")
        record["rs"] = ruleset_active(payload, config["ruleset_name"]) if status == "ok" else None
        if settings_ok:
            status, payload = get(f"{base}/actions/permissions")
            if status == "ok" and isinstance(payload, Mapping):
                record["perm"] = {"sha": payload.get("sha_pinning_required") is True, "allowed": payload.get("allowed_actions") == "selected"}
        return name, record

    out: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for name, record in pool.map(one, wanted):
            out[name] = record
    return {"asof": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": out}


# ---------------------------------------------------------------------------
# The document (whitelist) and the report
# ---------------------------------------------------------------------------

def _repo_list(values: object, names: set[str], limit: int) -> list[str]:
    if not isinstance(values, list):
        return []
    return sorted({v for v in values if isinstance(v, str) and REPO_RE.match(v) and v in names})[:limit]


def _count(value: object, high: int = 10_000_000) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= high else 0


def clean(doc: Mapping, names: Iterable[str], limit: int = 40) -> dict:
    """Rebuilds the document from a whitelist: only names of known repositories, counts, file names of workflows, version tags and UTC moments survive.
    Anything else (a pull request title, a rule of the code scanning, an actor, a branch...) cannot get through, whatever the input holds."""
    known = set(names)
    out: dict = {"schema": SCHEMA, "asof": _stamp(doc.get("asof")), "repos": _count(doc.get("repos")), "read": _count(doc.get("read"))}
    ci = doc.get("ci") if isinstance(doc.get("ci"), Mapping) else {}
    red = []
    for item in (ci.get("red") or []) if isinstance(ci.get("red"), list) else []:
        if isinstance(item, Mapping) and isinstance(item.get("repo"), str) and item["repo"] in known and isinstance(item.get("wf"), str) and WORKFLOW_RE.match(item["wf"]):
            red.append({"repo": item["repo"], "wf": item["wf"], "streak": _count(item.get("streak"), 1000), "since": _stamp(item.get("since"))})
    out["ci"] = {"checked": _count(ci.get("checked")), "red": sorted(red, key=lambda r: (r["repo"], r["wf"]))[:limit], "red_total": max(len(red), _count(ci.get("red_total")))}
    releases = doc.get("releases") if isinstance(doc.get("releases"), Mapping) else {}
    cands = []
    for item in (releases.get("candidates") or []) if isinstance(releases.get("candidates"), list) else []:
        if isinstance(item, Mapping) and isinstance(item.get("repo"), str) and item["repo"] in known:
            tag = item.get("tag")
            cands.append({"repo": item["repo"], "entries": _count(item.get("entries"), 100000), "tag": tag if isinstance(tag, str) and TAG_RE.match(tag) else "",
                          "published": _stamp(item.get("published"))})
    out["releases"] = {"days": float(releases["days"]) if isinstance(releases.get("days"), (int, float)) and not isinstance(releases.get("days"), bool) else 0.0,
                       "min_entries": _count(releases.get("min_entries"), 100), "candidates": sorted(cands, key=lambda r: (-r["entries"], r["repo"]))[:limit], "total": max(len(cands), _count(releases.get("total")))}
    eco_in = doc.get("ecosystems") if isinstance(doc.get("ecosystems"), Mapping) else {}
    out["ecosystems"] = {eco: {k: _count(row.get(k)) for k in ("repos", "read", "red", "cand", "unpub")}
                         for eco, row in sorted(eco_in.items()) if isinstance(eco, str) and ECO_RE.match(eco) and isinstance(row, Mapping)}
    unpub = doc.get("unpublished") if isinstance(doc.get("unpublished"), Mapping) else {}
    rows = []
    for item in (unpub.get("rows") or []) if isinstance(unpub.get("rows"), list) else []:
        if isinstance(item, Mapping) and isinstance(item.get("repo"), str) and item["repo"] in known:
            version, tag = item.get("version"), item.get("tag")
            if isinstance(version, str) and TAG_RE.match(version) and isinstance(tag, str) and TAG_RE.match(tag):
                rows.append({"repo": item["repo"], "version": version, "tag": tag})
    out["unpublished"] = {"rows": sorted(rows, key=lambda r: r["repo"])[:limit], "total": max(len(rows), _count(unpub.get("total")))}
    tags_in = doc.get("tags") if isinstance(doc.get("tags"), Mapping) else {}
    out["tags"] = {repo: tag for repo, tag in sorted(tags_in.items()) if repo in known and isinstance(tag, str) and TAG_RE.match(tag)}
    events = []
    for item in (doc.get("events") or []) if isinstance(doc.get("events"), list) else []:
        if not (isinstance(item, Mapping) and item.get("kind") in EVENT_KINDS and isinstance(item.get("repo"), str) and item["repo"] in known and _stamp(item.get("at"))):
            continue
        event = {"at": _stamp(item["at"]), "kind": item["kind"], "repo": item["repo"]}
        if item["kind"] == "released":
            tag = item.get("tag")
            if not (isinstance(tag, str) and TAG_RE.match(tag)):
                continue
            event["tag"] = tag
        else:
            wf = item.get("wf")
            if not (isinstance(wf, str) and WORKFLOW_RE.match(wf)):
                continue
            event["wf"] = wf
        events.append(event)
    out["events"] = events[:200]                 # the length is chosen by `events_max` where the feed is made
    sigs = doc.get("signatures") if isinstance(doc.get("signatures"), Mapping) else {}
    out["signatures"] = {state: _count(sigs.get(state)) for state in SIGNATURE_STATES}
    out["signatures"]["invalid_repos"] = _repo_list(sigs.get("invalid_repos"), known, limit)
    hyg = doc.get("hygiene") if isinstance(doc.get("hygiene"), Mapping) else {}
    out["hygiene"] = {"ruleset_checked": _count(hyg.get("ruleset_checked")), "ruleset_missing": _repo_list(hyg.get("ruleset_missing"), known, limit),
                      "settings_checked": _count(hyg.get("settings_checked")), "sha_missing": _repo_list(hyg.get("sha_missing"), known, limit),
                      "allowed_missing": _repo_list(hyg.get("allowed_missing"), known, limit), "gaps": _count(hyg.get("gaps"))}
    comp = doc.get("compute") if isinstance(doc.get("compute"), Mapping) else {}
    top = []
    for item in (comp.get("top") or []) if isinstance(comp.get("top"), list) else []:
        if isinstance(item, Mapping) and isinstance(item.get("repo"), str) and item["repo"] in known:
            top.append({"repo": item["repo"], "min24": _count(item.get("min24")), "min7": _count(item.get("min7"))})
    out["compute"] = {"total24": _count(comp.get("total24")), "total7": _count(comp.get("total7")), "top": top[:limit], "warn": comp.get("warn") is True}
    trend = doc.get("trend") if isinstance(doc.get("trend"), Mapping) else {}
    dates = [d for d in (trend.get("dates") or []) if isinstance(d, str) and re.match(r"^\d{4}-\d\d-\d\d$", d)] if isinstance(trend.get("dates"), list) else []
    out["trend"] = {"dates": dates}
    for key in ("red", "cand", "gaps", "min"):
        values = trend.get(key) if isinstance(trend.get(key), list) else []
        out["trend"][key] = [_count(v) for v in values][: len(dates)] if len(values) >= len(dates) else [_count(v) for v in values] + [0] * (len(dates) - len(values))
    out["parte"] = _clean_parte(doc.get("parte"), known, limit)
    return out


PARTE_KEYS = ("head", "all_ok", "red", "cand", "unpub", "sig", "hyg", "settings", "compute", "unread")
LEVELS = ("ok", "info", "warn", "bad")


def _clean_parte(items: object, names: set[str], limit: int) -> list[dict]:
    out = []
    for item in (items or []) if isinstance(items, list) else []:
        if not isinstance(item, Mapping) or item.get("key") not in PARTE_KEYS or item.get("level") not in LEVELS:
            continue
        params = item.get("p") if isinstance(item.get("p"), Mapping) else {}
        clean_params: dict = {}
        for key, value in params.items():
            if key == "list":
                clean_params["list"] = _repo_list(value, names, limit)
            elif key in ("n", "m", "red", "cand", "bad", "hyg", "total", "min", "more") and isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 10_000_000:
                clean_params[key] = value
        out.append({"key": item["key"], "level": item["level"], "p": clean_params})
    return out


def build_parte(doc: Mapping, config: Mapping) -> list[dict]:
    """The short report, by rules: the first item is the headline, then what needs a decision, the worst first. Texts are chosen by the page (8 languages)."""
    sections = config["sections"]
    ci, releases, signatures, hygiene, compute = doc["ci"], doc["releases"], doc["signatures"], doc["hygiene"], doc["compute"]
    red = [r["repo"] for r in ci["red"]] if sections["ci"] else []
    cands = [c["repo"] for c in releases["candidates"]] if sections["releases"] else []
    invalid = signatures["invalid_repos"] if sections["signatures"] else []
    gaps = hygiene["ruleset_missing"] if sections["hygiene"] else []
    head = {"key": "head", "level": "ok", "p": {"red": len(red), "cand": len(cands), "bad": len(invalid), "hyg": hygiene["gaps"] if sections["hygiene"] else 0}}
    lines = []
    if invalid:
        lines.append({"key": "sig", "level": "bad", "p": {"list": invalid, "n": len(invalid)}})
    if red:
        persistent = any(r["streak"] >= config["red_streak_warn"] for r in ci["red"])
        lines.append({"key": "red", "level": "bad" if persistent else "warn", "p": {"list": sorted(set(red)), "n": len(red)}})
    if cands:
        lines.append({"key": "cand", "level": "warn", "p": {"list": cands, "n": len(cands)}})
    unpub = [u["repo"] for u in doc["unpublished"]["rows"]] if sections["releases"] else []
    if unpub:
        lines.append({"key": "unpub", "level": "warn", "p": {"list": unpub, "n": len(unpub)}})
    if gaps:
        lines.append({"key": "hyg", "level": "warn", "p": {"list": gaps, "n": len(gaps)}})
    if sections["hygiene"] and hygiene["settings_checked"] == 0 and doc["read"] > 0:
        lines.append({"key": "settings", "level": "info", "p": {"n": 0, "m": doc["read"]}})
    if sections["compute"] and compute["warn"]:
        lines.append({"key": "compute", "level": "warn", "p": {"min": compute["total24"]}})
    if doc["read"] < doc["repos"]:
        lines.append({"key": "unread", "level": "info", "p": {"n": doc["repos"] - doc["read"], "m": doc["repos"]}})
    level = "bad" if any(line["level"] == "bad" for line in lines) else "warn" if any(line["level"] == "warn" for line in lines) else "ok"
    head["level"] = level
    if level == "ok" and doc["read"] >= doc["repos"]:
        lines.insert(0, {"key": "all_ok", "level": "ok", "p": {}})
    return [head] + lines


def day_summary(doc: Mapping | None) -> dict | None:
    """{"red", "cand", "gaps", "min"} for the daily history, or None when nothing was read."""
    if not doc or not doc.get("read"):
        return None
    return {"red": doc["ci"]["red_total"], "cand": doc["releases"]["total"], "gaps": doc["hygiene"]["gaps"], "min": doc["compute"]["total24"]}


def trend_of(history: Sequence[Mapping], today: str, current: Mapping | None, days: int = 30) -> dict:
    rows = []
    for entry in sorted(history, key=lambda e: str(e.get("date"))):
        item = entry.get("sentinel")
        if isinstance(item, Mapping) and str(entry.get("date")) < today and all(isinstance(item.get(k), int) for k in ("red", "cand", "gaps", "min")):
            rows.append((str(entry["date"]), item))
    if current:
        rows.append((today, current))
    rows = rows[-days:]
    return {"dates": [d for d, _ in rows], **{key: [int(item[key]) for _, item in rows] for key in ("red", "cand", "gaps", "min")}}


def assemble(read: Mapping | None, names: Iterable[str], config: Mapping, signatures: Mapping[str, str] | None, actions_block: Mapping | None,
             history: Sequence[Mapping], today: str, ecosystem_of: Mapping[str, str] | None = None, versions: Mapping[str, str | None] | None = None,
             saved: Mapping | None = None) -> dict | None:
    """The document from a reading. None when there is no reading (the page then uses the last saved document). `ecosystem_of` (repository -> ecosystem) feeds the
    table by ecosystem, `versions` (repository -> version declared by its manifest) the versions raised without a release and `saved` (the previous document) the feed."""
    if not read:
        return None
    names = sorted(set(names))
    now = _parse(read["asof"]) or datetime.now(timezone.utc)
    records = {n: read["repos"].get(n) or {"state": "unread"} for n in names}
    ok = {n: r for n, r in records.items() if r.get("state") == "ok"}
    red, checked = [], 0
    for name, rec in sorted(ok.items()):
        checked += int(rec.get("checked") or 0)
        for item in rec.get("ci") or []:
            red.append({"repo": name, **item})
    unreleased = {n: r["entries"] for n, r in ok.items() if isinstance(r.get("entries"), int)}
    candidates = release_candidates(unreleased, {n: r.get("published") for n, r in ok.items()}, {n: r.get("tag") or "" for n, r in ok.items()}, now,
                                    config["candidate_days"], config["candidate_min_entries"], config["skip_candidate_prefixes"])
    sig = {state: 0 for state in SIGNATURE_STATES}
    invalid = []
    for name in names:
        state = (signatures or {}).get(name)
        state = state if state in SIGNATURE_STATES else "unverified"
        sig[state] += 1
        if state == "invalid":
            invalid.append(name)
    sig["invalid_repos"] = invalid
    missing = [n for n, r in ok.items() if r.get("rs") is False]
    settings = {n: r["perm"] for n, r in ok.items() if isinstance(r.get("perm"), Mapping)}
    sha_missing = [n for n, p in settings.items() if not p.get("sha")]
    allowed_missing = [n for n, p in settings.items() if not p.get("allowed")]
    hygiene = {"ruleset_checked": sum(1 for r in ok.values() if r.get("rs") is not None), "ruleset_missing": missing, "settings_checked": len(settings),
               "sha_missing": sha_missing, "allowed_missing": allowed_missing, "gaps": len(set(missing) | set(sha_missing) | set(allowed_missing))}
    rows = []
    for name, rec in ((actions_block or {}).get("repos") or {}).items():
        if name in records and isinstance(rec, Mapping) and rec.get("state") == "ok" and (rec.get("min") or rec.get("min7")):
            rows.append({"repo": name, "min24": int(rec.get("min") or 0), "min7": int(rec.get("min7") or 0)})
    rows.sort(key=lambda r: (-r["min24"], -r["min7"], r["repo"]))
    total24 = sum(r["min24"] for r in rows)
    compute = {"total24": total24, "total7": sum(r["min7"] for r in rows), "top": rows[: config["compute_top"]], "warn": total24 > config["compute_warn_minutes_24h"]}
    tags = {n: r["tag"] for n, r in ok.items() if r.get("tag")}
    unpublished = unpublished_versions({n: v for n, v in (versions or {}).items() if n in ok}, tags, config["skip_candidate_prefixes"])
    ecosystems = ecosystem_table(names, ecosystem_of or {}, ok, red, candidates, unpublished)
    events = new_events(saved, red, ok, tags, _stamp(read["asof"]), config["events_max"])
    doc = {"asof": read["asof"], "repos": len(names), "read": len(ok), "ecosystems": ecosystems, "unpublished": {"rows": unpublished}, "tags": tags, "events": events,
           "ci": {"checked": checked, "red": red},
           "releases": {"days": config["candidate_days"], "min_entries": config["candidate_min_entries"], "candidates": candidates},
           "signatures": sig, "hygiene": hygiene, "compute": compute, "trend": {}, "parte": []}
    first = clean(doc, names, 10_000)           # whitelist first, so that the counters and the report are computed from what can be published
    first["trend"] = trend_of(history, today, day_summary(first))
    first["parte"] = build_parte(first, config)
    return clean(first, names, config["list_max"])


# ---------------------------------------------------------------------------
# File, stability and the block of the page
# ---------------------------------------------------------------------------

def load_saved(path: Path = DATA_PATH, names: Iterable[str] = ()) -> dict | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA or _stamp(raw.get("asof")) is None:
        return None
    return clean(raw, names, 10_000)


def _without_asof(doc: Mapping) -> str:
    return json.dumps({k: v for k, v in doc.items() if k != "asof"}, sort_keys=True)


def stabilize(fresh: dict | None, saved: Mapping | None, max_hours: int = 6) -> dict | None:
    """An unchanged situation keeps the moment of the saved reading (so the file and the page stay identical and the bot makes no commit) for up to `max_hours`."""
    if not fresh or not saved:
        return fresh
    before, now = _parse(saved.get("asof")), _parse(fresh.get("asof"))
    if before is None or now is None or not (timedelta(0) <= now - before < timedelta(hours=max_hours)):
        return fresh
    return dict(saved) if _without_asof(saved) == _without_asof(fresh) else fresh


def save(path: Path, doc: Mapping | None) -> bool:
    """Written only when it differs from the file. True when the file was written."""
    if not doc:
        return False
    text = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)
    return True


def build(doc: Mapping | None, saved: Mapping | None, config: Mapping, today: str) -> dict:
    """The "sentinel" block of the page data. `doc` is this run's document (None when GitHub did not answer); `saved` the last good one."""
    sections = dict(config["sections"])
    if not config["enabled"]:
        return {"enabled": False, "read": False, "stale": None, "sections": sections, "doc": None}
    source = doc or saved
    stale = None if doc else (saved or {}).get("asof")
    return {"enabled": True, "read": bool(source), "stale": stale, "sections": sections, "doc": dict(source) if source else None}
