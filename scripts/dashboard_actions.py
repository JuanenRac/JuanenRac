#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_actions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The builds (GitHub Actions runs) of every repository, for the tab "Actions / Builds" of the status dashboard.

Only state and numbers are kept: the result of each run, how long it took, when it ended, how many were green in the last 24 hours and 7 days, the minutes of
computing they used (wall-clock time of the runs, an approximation) and how many issues labelled `build-failed` / `build-stuck` are open. The page never keeps
who started a run, the branch or the title of a commit.

The reading happens once, in the job that builds the dashboard (read-only token): one GraphQL request per page of 20 repositories (workflows folder and the two
labels) and one REST request per repository that has workflows. Nothing is invented:

  * a repository without a workflows folder     -> "none" (nothing to build),
  * a repository whose lookup failed            -> "unread" (not verified, never a green state),
  * every lookup failed                          -> the last read saved in `data/actions-cache.json` is shown with its date, or "not read" when there is none.

All times of a record are minutes before `asof` (the moment of the reading), so the page can draw the same picture on any day. Stdlib only.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

import ci_rules

CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "actions-cache.json"
CONFIG_PATH = Path(__file__).resolve().parent.parent / "dashboard-config.json"
DAY_MINUTES = 24 * 60
WEEK_MINUTES = 7 * DAY_MINUTES
DEFAULT_CONFIG: dict = {"labels": {"failed": "build-failed", "stuck": "build-stuck"}, "timeline_max": 40, "durations_max": 12,
                        "ignore_paths": {"JuanenRac": [".github/workflows/build-dashboard.yml"]}}
CODES = ("s", "f", "c", "k", "p")     # success, failure, cancelled, other (skipped, neutral, stale...), running or queued
SCHEMA = 1

REPOS_QUERY = """
query($owner: String!, $cursor: String, $failed: [String!], $stuck: [String!]) {
  repositoryOwner(login: $owner) {
    repositories(first: 20, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        workflows: object(expression: "HEAD:.github/workflows") { ... on Tree { entries { name } } }
        bf: issues(states: OPEN, labels: $failed) { totalCount }
        bs: issues(states: OPEN, labels: $stuck) { totalCount }
      }
    }
  }
}
"""

Post = Callable[[bytes, dict], "dict | None"]
Get = Callable[[str], "tuple[str, object]"]


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def check_config(raw: object) -> tuple[dict, list[str]]:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["actions: not an object"]
    labels = raw.get("labels")
    if labels is not None:
        if isinstance(labels, Mapping) and all(isinstance(labels.get(k), str) and 0 < len(labels[k]) <= 50 for k in ("failed", "stuck")):
            config["labels"] = {"failed": labels["failed"], "stuck": labels["stuck"]}
        else:
            problems.append("actions.labels: needs the texts failed and stuck")
    for key, low, high in (("timeline_max", 5, 200), ("durations_max", 3, 60)):
        if key in raw:
            value = raw[key]
            if isinstance(value, int) and not isinstance(value, bool) and low <= value <= high:
                config[key] = value
            else:
                problems.append(f"actions.{key}: needs an integer from {low} to {high}")
    ignore = raw.get("ignore_paths")
    if ignore is not None:
        if isinstance(ignore, Mapping) and all(isinstance(k, str) and isinstance(v, list) and all(isinstance(p, str) for p in v) for k, v in ignore.items()):
            config["ignore_paths"] = {k: list(v) for k, v in ignore.items()}
        else:
            problems.append("actions.ignore_paths: needs {repository: [workflow files]}")
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return check_config(None)
    except (OSError, ValueError) as exc:
        return check_config(None)[0], [f"{path.name} could not be read for the builds ({exc})"]
    return check_config(raw.get("actions") if isinstance(raw, Mapping) else None)


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

def _parse(text: object) -> datetime | None:
    if not isinstance(text, str):
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def code_of(run: Mapping) -> str:
    status, conclusion = run.get("status"), run.get("conclusion")
    if status != "completed":
        return "p"
    if conclusion == "success":
        return "s"
    if ci_rules.is_red(conclusion):
        return "f"
    if conclusion == "cancelled":
        return "c"
    return "k"


def summarize(runs: Iterable[object], asof: datetime, config: Mapping, ignore: Sequence[str] = ()) -> dict:
    """The record of one repository from its runs of the last 7 days (the `workflow_runs` of the API). Only the fields below are read from a run."""
    items = []
    for run in runs:
        if not isinstance(run, Mapping) or run.get("path") in ignore:
            continue
        created = _parse(run.get("created_at"))
        if created is None:
            continue
        started = _parse(run.get("run_started_at")) or created
        updated = _parse(run.get("updated_at")) or started
        code = code_of(run)
        ended = updated if code != "p" else None
        seconds = max(0, int((updated - started).total_seconds())) if code != "p" else None
        age_end = max(0, int((asof - (ended or created)).total_seconds() // 60))
        items.append({"code": code, "age": age_end, "sec": seconds})
    items.sort(key=lambda it: it["age"])
    inside = [it for it in items if it["age"] < WEEK_MINUTES]
    day = [it for it in inside if it["age"] < DAY_MINUTES]
    count = lambda rows: [sum(1 for it in rows if it["code"] == c) for c in CODES]            # noqa: E731
    finished = [it for it in inside if it["code"] != "p"]
    ok = next((it for it in finished if it["code"] == "s"), None)
    return {
        "state": "ok",
        "last": [finished[0]["age"], finished[0]["code"], finished[0]["sec"]] if finished else None,
        "lastOk": ok["age"] if ok else None,
        "running": sum(1 for it in inside if it["code"] == "p"),
        "n": count(day),
        "n7": count(inside),
        "min": round(sum(it["sec"] or 0 for it in day) / 60),
        "min7": round(sum(it["sec"] or 0 for it in inside) / 60),
        "tl": [[it["age"], it["code"]] for it in day][: config["timeline_max"]],
        "dur": [it["sec"] for it in reversed(finished[: config["durations_max"]]) if it["sec"] is not None],
        "truncated": len(items) >= 100,
    }


def rest_get(token: str, timeout: float = 20) -> Get:
    headers = {"User-Agent": "JuanenRac-dashboard-actions", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    def run(url: str):
        outcome: tuple[str, object] = ("error", "no attempt")
        for _attempt in range(2):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as response:
                    return "ok", json.loads(response.read(8_000_000).decode("utf-8", errors="replace"))
            except urllib.error.HTTPError as exc:
                if exc.code in (404, 410):
                    return "absent", None
                outcome = ("error", f"HTTP {exc.code}")
                if exc.code in (401, 403):
                    return outcome
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                outcome = ("error", f"lookup failed: {exc}")
        return outcome
    return run


def graphql_post(body: bytes, headers: dict) -> "dict | None":
    request = urllib.request.Request("https://api.github.com/graphql", data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None


def list_repos(owner: str, token: str, config: Mapping, post: Post = graphql_post, max_pages: int = 20) -> dict[str, dict] | None:
    """{repository: {"workflows": bool, "bf": open issues build-failed, "bs": open issues build-stuck}} or None when GitHub did not answer."""
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard-actions", "Content-Type": "application/json"}
    found: dict[str, dict] = {}
    cursor = None
    for _ in range(max_pages):
        variables = {"owner": owner, "cursor": cursor, "failed": [config["labels"]["failed"]], "stuck": [config["labels"]["stuck"]]}
        body = json.dumps({"query": REPOS_QUERY, "variables": variables}).encode("utf-8")
        answer = post(body, headers) or post(body, headers)
        try:
            page = answer["data"]["repositoryOwner"]["repositories"]
            for node in page["nodes"]:
                if not isinstance(node, Mapping) or not node.get("name"):
                    continue
                entries = (node.get("workflows") or {}).get("entries") or []
                found[str(node["name"])] = {
                    "workflows": any(str(e.get("name", "")).lower().endswith((".yml", ".yaml")) for e in entries if isinstance(e, Mapping)),
                    "bf": int((node.get("bf") or {}).get("totalCount") or 0), "bs": int((node.get("bs") or {}).get("totalCount") or 0)}
            if not page["pageInfo"]["hasNextPage"]:
                return found
            cursor = page["pageInfo"]["endCursor"]
        except (TypeError, KeyError, ValueError):
            return None
    return found


def read_all(owner: str, names: Iterable[str], token: str, config: Mapping | None = None, now: datetime | None = None, post: Post = graphql_post,
             get: Get | None = None, workers: int = 8) -> dict | None:
    """{"asof", "repos": {name: record}, "errors": n} or None when the list of repositories could not be read at all."""
    config = config or check_config(None)[0]
    now = (now or datetime.now(timezone.utc)).replace(microsecond=0)
    listing = list_repos(owner, token, config, post)
    if listing is None:
        return None
    get = get or rest_get(token)
    since = (now - timedelta(minutes=WEEK_MINUTES)).strftime("%Y-%m-%dT%H:%M:%SZ")
    wanted = sorted(set(names))
    out: dict[str, dict] = {}
    errors = 0

    def one(name: str):
        info = listing.get(name)
        if info is None:
            return name, {"state": "unread"}
        if not info["workflows"]:
            return name, {"state": "none", "bf": info["bf"], "bs": info["bs"]}
        url = f"https://api.github.com/repos/{owner}/{name}/actions/runs?per_page=100&created={urllib.parse.quote('>=' + since)}"
        status, payload = get(url)
        if status != "ok" or not isinstance(payload, Mapping) or not isinstance(payload.get("workflow_runs"), list):
            return name, {"state": "unread", "bf": info["bf"], "bs": info["bs"]}
        record = summarize(payload["workflow_runs"], now, config, config["ignore_paths"].get(name, ()))
        record["bf"], record["bs"] = info["bf"], info["bs"]
        return name, record

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for name, record in pool.map(one, wanted):
            out[name] = record
            errors += record["state"] == "unread"
    return {"asof": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": out, "errors": errors}


# ---------------------------------------------------------------------------
# Cache and daily summary
# ---------------------------------------------------------------------------

def load_cache(path: Path = CACHE_PATH) -> dict | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA or _parse(raw.get("asof")) is None or not isinstance(raw.get("repos"), dict):
        return None
    return {"asof": raw["asof"], "repos": raw["repos"], "errors": int(raw.get("errors") or 0)}


def save_cache(path: Path, read: Mapping | None) -> bool:
    """Saved only when this run read at least one repository properly. True when the file was written."""
    if not read or not any(r.get("state") == "ok" for r in read["repos"].values()):
        return False
    text = json.dumps({"schema": SCHEMA, **read}, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
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


def _fingerprint(record: Mapping) -> tuple:
    if record.get("state") != "ok":
        return (record.get("state"), record.get("bf"), record.get("bs"))
    last = record.get("last")
    return ("ok", record.get("running"), tuple(record.get("n7") or ()), last[1] if last else None, record.get("bf"), record.get("bs"))


def stabilize(fresh: dict | None, cache: Mapping | None, max_hours: int = 6) -> dict | None:
    """The page is regenerated every 30 minutes and every record is relative to the moment of the reading, so a new reading would change the page (and make the
    bot commit) even when no build did anything. When no repository has a new result, a new running build or a different number of issues since the saved
    reading, and that reading is younger than `max_hours`, the saved one is kept (with its own moment). Anything that changed, a first reading or an old
    cache gives the fresh reading."""
    if not fresh or not cache:
        return fresh
    before, now = _parse(cache.get("asof")), _parse(fresh.get("asof"))
    if before is None or now is None or not (timedelta(0) <= now - before < timedelta(hours=max_hours)):
        return fresh
    old, new = cache.get("repos") or {}, fresh["repos"]
    if set(old) != set(new) or any(_fingerprint(old[name]) != _fingerprint(new[name]) for name in new):
        return fresh
    return {"asof": cache["asof"], "repos": old, "errors": int(cache.get("errors") or 0)}


def day_summary(read: Mapping | None) -> dict | None:
    """The compact summary of the last 24 hours for the daily history: {"runs", "ok", "fail", "other", "min"} or None when nothing was read this run."""
    if not read:
        return None
    repos = [r for r in read["repos"].values() if r.get("state") == "ok"]
    if not repos:
        return None
    total = [sum(r["n"][i] for r in repos) for i in range(5)]
    return {"runs": sum(total), "ok": total[0], "fail": total[1], "other": total[2] + total[3] + total[4], "min": sum(r["min"] for r in repos)}


def build(read: Mapping | None, cache: Mapping | None, names: Iterable[str], history: Sequence[Mapping], today: str) -> dict:
    """The "actions" block of the page data. `read` is this run's reading (None when GitHub did not answer); `cache` the last good one."""
    names = sorted(set(names))
    source, stale = (read, None) if read else (cache, (cache or {}).get("asof"))
    repos = {}
    for name in names:
        record = (source or {}).get("repos", {}).get(name) if source else None
        repos[name] = dict(record) if isinstance(record, Mapping) else {"state": "unread"}
    daily = []
    for entry in sorted(history, key=lambda e: str(e.get("date"))):
        item = entry.get("actions")
        if isinstance(item, Mapping) and str(entry.get("date")) < today:
            daily.append({"date": str(entry["date"]), **{k: item[k] for k in ("runs", "ok", "fail", "other", "min") if isinstance(item.get(k), int)}})
    current = day_summary(source)
    if current and not stale:
        daily.append({"date": today, **current})
    return {
        "read": bool(source),
        "asof": (source or {}).get("asof"),
        "stale": stale,
        "repos": repos,
        "daily": daily,
        "problems": sum(1 for r in repos.values() if r["state"] == "unread"),
    }
