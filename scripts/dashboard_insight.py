#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_insight.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The analysis tab of the status dashboard: what is computed when the page is generated.

  * `funnel`: how many repositories sit at each maturity level of each ecosystem and how many moved up since the oldest useful snapshot,
  * `radar`: the eight areas of the four ecosystems side by side,
  * `heatmap`: commits and releases per ecosystem and per week (`fetch_commit_weeks` reads the weekly commits with the REST API),
  * `dependencies`: who uses whom, from the `depends_on` of the manifests, with cycles and dependencies on repositories that do not exist,
  * `milestones`: the next steps of the roadmaps (`fetch_projects` reads the GitHub Projects; the plans kept in this repository are the fallback),
  * `debt`: scaffolding for too long, functional without integration tests, real hardware without evidence of it (`fetch_facts` reads the dates and the folders).

Nothing is invented: anything that could not be read is None (or absent) and the page prints "not verified" or "not enough data".
Comparing two dates is done in the browser from the snapshots of the history, and nothing is interpolated. Stdlib only, the network is injectable.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from typing import Callable, Iterable, Mapping, Sequence

from dashboard_charts import AREAS, MATURITY_KEYS, Poster, _post

WEEKS = 12
BASELINE_DAYS = 30
SHORT_HISTORY_DAYS = 28
API = "https://api.github.com"
MILESTONE_ORDER = ("In progress", "Ready", "Backlog", "Blocked")
INTEGRATION_WORDS = ("integration", "e2e", "end_to_end", "end-to-end", "end2end")

FACTS_QUERY = """
query($owner: String!, $cursor: String) {
  repositoryOwner(login: $owner) {
    repositories(first: 25, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        createdAt
        releases(first: 100) { nodes { publishedAt } }
        root: object(expression: "HEAD:") { ... on Tree { entries { name } } }
        tests: object(expression: "HEAD:tests") { ... on Tree { entries { name } } }
        test: object(expression: "HEAD:test") { ... on Tree { entries { name } } }
      }
    }
  }
}
"""

PROJECTS_QUERY = """
query($owner: String!) {
  user(login: $owner) {
    projectsV2(first: 20) {
      nodes {
        title
        items(first: 100) {
          nodes {
            content { ... on Issue { title } ... on DraftIssue { title } ... on PullRequest { title } }
            status: fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
            priority: fieldValueByName(name: "Priority") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
          }
        }
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------

def _day(text: object) -> date | None:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text) if isinstance(text, str) else None
    if not match:
        return None
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def week_starts(today: str, count: int = WEEKS) -> list[str]:
    """The Sundays that start the last `count` weeks, the last one being the week that contains `today` (the weeks of the GitHub statistics)."""
    end = _day(today) or datetime.now(timezone.utc).date()
    last = end - timedelta(days=(end.weekday() + 1) % 7)
    return [(last - timedelta(weeks=count - 1 - n)).isoformat() for n in range(count)]


# ---------------------------------------------------------------------------
# 1. Maturity funnel and radar
# ---------------------------------------------------------------------------

def _level(value: object) -> int | None:
    return MATURITY_KEYS.index(value) if isinstance(value, str) and value in MATURITY_KEYS else None


def baseline(history: Sequence[Mapping], today: str) -> Mapping | None:
    """The snapshot to compare with: the newest one at least BASELINE_DAYS old that records every repository; otherwise the oldest earlier one that does.
    None when no earlier snapshot records them."""
    now = _day(today)
    if now is None:
        return None
    usable = sorted((e for e in history if isinstance(e.get("repos"), Mapping) and e["repos"] and (_day(e.get("date")) or now) < now), key=lambda e: e["date"])
    if not usable:
        return None
    target = now - timedelta(days=BASELINE_DAYS)
    old_enough = [e for e in usable if (_day(e["date"]) or now) <= target]
    return old_enough[-1] if old_enough else usable[0]


def funnel(repos: Mapping[str, Mapping], ecosystems: Sequence[str], history: Sequence[Mapping], today: str) -> dict:
    """{"eco": {eco: {"counts": [4], "total": n, "unknown": k, "up": n|None, "down": n|None, "compared": n}}, "since": {"date", "days"} | None}.
    "up" and "down" are None when no earlier snapshot records the maturity of the repositories."""
    base = baseline(history, today)
    base_repos = base["repos"] if base else {}
    out: dict[str, dict] = {}
    for eco in ecosystems:
        counts = [0, 0, 0, 0]
        unknown = up = down = compared = 0
        for name, repo in repos.items():
            if repo.get("eco") != eco:
                continue
            now = _level(repo.get("maturity"))
            if now is None:
                unknown += 1
                continue
            counts[now] += 1
            before = base_repos.get(name)
            before_level = before[0] if isinstance(before, (list, tuple)) and before and isinstance(before[0], int) else None
            if before_level is not None and 0 <= before_level < len(MATURITY_KEYS):
                compared += 1
                up += now > before_level
                down += now < before_level
        out[eco] = {"counts": counts, "total": sum(counts) + unknown, "unknown": unknown,
                    "up": up if base else None, "down": down if base else None, "compared": compared}
    since = None
    if base:
        then, now = _day(base["date"]), _day(today)
        since = {"date": base["date"], "days": (now - then).days if then and now else None}
    return {"eco": out, "since": since}


def radar(status: Mapping[str, Mapping[str, object]], ecosystems: Sequence[str]) -> dict[str, dict[str, int | None]]:
    """{eco: {area: percent | None}}: the eight areas of the README, None for one that could not be read."""
    out: dict[str, dict[str, int | None]] = {}
    for eco in ecosystems:
        row: dict[str, int | None] = {}
        for area in AREAS:
            pct = getattr(((status.get(eco) or {}).get(area)), "percent", None)
            row[area] = pct if isinstance(pct, int) and not isinstance(pct, bool) and 0 <= pct <= 100 else None
        out[eco] = row
    return out


# ---------------------------------------------------------------------------
# 2. Weekly activity
# ---------------------------------------------------------------------------

def _get(url: str, headers: dict) -> tuple[int, object | None]:
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            return response.status, (json.loads(body) if body.strip() else None)
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return 0, None


Getter = Callable[[str, dict], "tuple[int, object | None]"]


def parse_commit_weeks(payload: object) -> dict[str, int] | None:
    """{Sunday ISO date: commits} from the answer of stats/commit_activity, None when it is not that."""
    if not isinstance(payload, list):
        return None
    out: dict[str, int] = {}
    for item in payload:
        if not isinstance(item, Mapping) or not isinstance(item.get("week"), int) or not isinstance(item.get("total"), int) or item["total"] < 0:
            return None
        out[datetime.fromtimestamp(item["week"], timezone.utc).date().isoformat()] = item["total"]
    return out


def fetch_commit_weeks(owner: str, names: Iterable[str], token: str, get: Getter = _get, workers: int = 6, tries: int = 3,
                       sleep: Callable[[float], None] = time.sleep) -> dict[str, dict[str, int]]:
    """{repository: {week: commits}} for the repositories whose statistics were read. {} without a token. GitHub answers 202 while it computes them: asked again."""
    if not token:
        return {}
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard", "Accept": "application/vnd.github+json"}

    def one(name: str) -> tuple[str, dict[str, int] | None]:
        for attempt in range(tries):
            status, payload = get(f"{API}/repos/{owner}/{name}/stats/commit_activity", headers)
            if status == 202:
                sleep(2.0 * (attempt + 1))
                continue
            return name, parse_commit_weeks(payload) if status == 200 else None
        return name, None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return {name: weeks for name, weeks in pool.map(one, sorted(set(names))) if weeks is not None}


def parse_facts(nodes: Iterable[Mapping]) -> dict[str, dict]:
    """{repository: {"created", "releases": [dates], "files": [names] | None}}; `files` are the names at the top of the repository, of tests/ and of test/."""
    out: dict[str, dict] = {}
    for node in nodes:
        if not isinstance(node, Mapping) or not node.get("name"):
            continue
        root = (node.get("root") or {}).get("entries")
        names = None
        if isinstance(root, list):
            names = [str(e.get("name", "")) for e in root if isinstance(e, Mapping)]
            for key in ("tests", "test"):
                inner = (node.get(key) or {}).get("entries")
                if isinstance(inner, list):
                    names += [f"{key}/{e.get('name', '')}" for e in inner if isinstance(e, Mapping)]
        releases = (node.get("releases") or {}).get("nodes")
        out[str(node["name"])] = {
            "created": node["createdAt"] if isinstance(node.get("createdAt"), str) else None,
            "releases": [r["publishedAt"] for r in releases if isinstance(r, Mapping) and isinstance(r.get("publishedAt"), str)] if isinstance(releases, list) else None,
            "files": names,
        }
    return out


def fetch_facts(owner: str, token: str, post: Poster = _post, max_pages: int = 12) -> dict[str, dict]:
    """The creation date, the release dates and the top-level files of every public repository. {} without a token or on any failure."""
    if not token:
        return {}
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard", "Content-Type": "application/json"}
    found: dict[str, dict] = {}
    cursor = None
    for _ in range(max_pages):
        answer = post(json.dumps({"query": FACTS_QUERY, "variables": {"owner": owner, "cursor": cursor}}).encode("utf-8"), headers)
        try:
            page = answer["data"]["repositoryOwner"]["repositories"]
            found.update(parse_facts(page["nodes"]))
            if not page["pageInfo"]["hasNextPage"]:
                return found
            cursor = page["pageInfo"]["endCursor"]
        except (TypeError, KeyError):
            return {}
    return {}


def heatmap(eco_by_name: Mapping[str, str], ecosystems: Sequence[str], weekly: Mapping[str, Mapping[str, int]], facts: Mapping[str, Mapping], today: str) -> dict:
    """{"weeks": [Sunday dates], "eco": {eco: {"commits": [n|None], "releases": [n|None], "repos": m, "commitRepos": k, "releaseRepos": k}}}.
    A week is None for an ecosystem none of whose repositories could be read. A sum counts only the repositories that were read (`commitRepos` of `repos`)."""
    weeks = week_starts(today)
    out: dict[str, dict] = {}
    for eco in ecosystems:
        members = [n for n, e in eco_by_name.items() if e == eco]
        read = [n for n in members if n in weekly]
        rel_read = [n for n in members if isinstance(facts.get(n, {}).get("releases"), list)]
        commits: list[int | None] = [sum(weekly[n].get(w, 0) for n in read) if read else None for w in weeks]
        releases: list[int | None] = []
        for w in weeks:
            if not rel_read:
                releases.append(None)
                continue
            start = _day(w)
            releases.append(sum(1 for n in rel_read for d in facts[n]["releases"] if start and (_day(d) or date.min) >= start and (_day(d) or date.max) < start + timedelta(days=7)))
        out[eco] = {"commits": commits, "releases": releases, "repos": len(members), "commitRepos": len(read), "releaseRepos": len(rel_read)}
    return {"weeks": weeks, "eco": out}


# ---------------------------------------------------------------------------
# 3. Dependencies
# ---------------------------------------------------------------------------

def _components(graph: Mapping[str, Sequence[str]]) -> list[list[str]]:
    """Strongly connected components with a cycle (more than one repository, or one that depends on itself), Tarjan, no recursion."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on: set[str] = set()
    stack: list[str] = []
    found: list[list[str]] = []
    counter = 0
    for root in sorted(graph):
        if root in index:
            continue
        work = [(root, iter(sorted(graph.get(root, ()))))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        while work:
            node, children = work[-1]
            advanced = False
            for child in children:
                if child not in graph:
                    continue
                if child not in index:
                    index[child] = low[child] = counter
                    counter += 1
                    stack.append(child)
                    on.add(child)
                    work.append((child, iter(sorted(graph.get(child, ())))))
                    advanced = True
                    break
                if child in on:
                    low[node] = min(low[node], index[child])
            if advanced:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
            if low[node] == index[node]:
                part = []
                while True:
                    top = stack.pop()
                    on.discard(top)
                    part.append(top)
                    if top == node:
                        break
                if len(part) > 1 or node in graph.get(node, ()):
                    found.append(sorted(part, key=str.casefold))
    return sorted(found, key=lambda part: part[0].casefold())


def _layers(nodes: Sequence[str], edges: Sequence[tuple[str, str]]) -> dict[str, int]:
    """Layer 0 = used by others only; a repository sits one layer to the right of the deepest thing it uses. Bounded, so a cycle cannot loop."""
    uses: dict[str, list[str]] = {n: [] for n in nodes}
    for a, b in edges:
        uses[a].append(b)
    layer = {n: 0 for n in nodes}
    for _ in range(len(nodes) + 1):
        changed = False
        for n in nodes:
            want = 1 + max((layer[u] for u in uses[n]), default=-1)
            if want > layer[n] and want <= len(nodes):
                layer[n] = want
                changed = True
        if not changed:
            break
    return layer


def dependencies(manifests: Mapping[str, Mapping | None], eco_by_name: Mapping[str, str], ecosystems: Sequence[str]) -> dict:
    """{"repos": {name: {"uses", "usedBy", "missing", "parent", "children"}}, "cycles", "missing", "edges", "declaring", "diagram": {eco: {"nodes": [[name, layer, row]], "edges": [[user, used, in_cycle]]}}}.
    Only repositories with some relation are listed. `uses` comes from depends_on; the family `parent` is shown next to it."""
    declared: dict[str, list[str]] = {}
    parents: dict[str, str] = {}
    for name in eco_by_name:
        manifest = manifests.get(name)
        if not isinstance(manifest, Mapping):
            continue
        raw = manifest.get("depends_on")
        if isinstance(raw, list):
            declared[name] = sorted({str(x) for x in raw if isinstance(x, str) and x and x != ""}, key=str.casefold)
        parent = manifest.get("parent")
        if isinstance(parent, str) and parent:
            parents[name] = parent
    known = set(eco_by_name)
    graph = {n: [d for d in deps if d in known] for n, deps in declared.items()}
    for n in known:
        graph.setdefault(n, [])
    rel: dict[str, dict] = {}

    def entry(name: str) -> dict:
        return rel.setdefault(name, {"uses": [], "usedBy": [], "missing": [], "parent": parents.get(name, ""), "children": []})

    missing: list[list[str]] = []
    edges = 0
    for name, deps in declared.items():
        for dep in deps:
            entry(name)
            if dep in known:
                entry(name)["uses"].append(dep)
                entry(dep)["usedBy"].append(name)
                edges += 1
            else:
                entry(name)["missing"].append(dep)
                missing.append([name, dep])
    for name, parent in parents.items():
        entry(name)
        if parent in known:
            entry(parent)["children"].append(name)
    for row in rel.values():
        for key in ("uses", "usedBy", "children"):
            row[key] = sorted(set(row[key]), key=str.casefold)
    cycles = _components(graph)
    in_cycle = {n for part in cycles for n in part}
    diagram: dict[str, dict] = {}
    for eco in ecosystems:
        inner = sorted(((a, b) for a, deps in graph.items() for b in deps if eco_by_name.get(a) == eco and eco_by_name.get(b) == eco), key=lambda e: (e[0].casefold(), e[1].casefold()))
        nodes = sorted({n for e in inner for n in e}, key=str.casefold)
        # the edges inside one cycle do not count for the layer, so the repositories of a cycle share a column
        acyclic = [(x, y) for x, y in inner if not any(x in part and y in part for part in cycles)]
        layer = _layers(nodes, acyclic)
        rows: dict[int, int] = {}
        placed = []
        for n in sorted(nodes, key=lambda n: (layer[n], n.casefold())):
            placed.append([n, layer[n], rows.get(layer[n], 0)])
            rows[layer[n]] = rows.get(layer[n], 0) + 1
        diagram[eco] = {"nodes": placed, "edges": [[a, b, int(a in in_cycle and b in in_cycle)] for a, b in inner]}
    return {"repos": {k: rel[k] for k in sorted(rel, key=str.casefold)}, "cycles": cycles, "missing": sorted(missing, key=lambda m: (m[0].casefold(), m[1].casefold())),
            "edges": edges, "declaring": sum(1 for deps in declared.values() if deps), "diagram": diagram}


# ---------------------------------------------------------------------------
# 4. Milestones
# ---------------------------------------------------------------------------

_ECO_OF_TITLE = (("hydra", "hydra-umc"), ("urtc", "urtc"), ("a.r.m.o.r", "armor"), ("armor", "armor"), ("eh3d", "eh3d"))


def parse_projects(payload: object) -> dict[str, list[dict]] | None:
    """{eco: [{"title", "status", "priority"}]} from the GraphQL answer, None when the answer holds no project (no permission, an error)."""
    try:
        nodes = payload["data"]["user"]["projectsV2"]["nodes"]  # type: ignore[index]
    except (TypeError, KeyError):
        return None
    out: dict[str, list[dict]] = {}
    for project in nodes if isinstance(nodes, list) else []:
        if not isinstance(project, Mapping):
            continue
        title = str(project.get("title", "")).lower()
        eco = next((key for word, key in _ECO_OF_TITLE if word in title), None)
        items = ((project.get("items") or {}).get("nodes")) if isinstance(project.get("items"), Mapping) else None
        if eco is None or not isinstance(items, list):
            continue
        for item in items:
            content = (item or {}).get("content") or {}
            if isinstance(content, Mapping) and content.get("title"):
                out.setdefault(eco, []).append({
                    "title": str(content["title"]), "repository": "", "status": str(((item or {}).get("status") or {}).get("name") or ""),
                    "priority": str(((item or {}).get("priority") or {}).get("name") or ""), "hardware": "", "blocked": ""})
    return out or None


def fetch_projects(owner: str, token: str, post: Poster = _post) -> dict[str, list[dict]] | None:
    """The cards of the roadmap Projects. None without a token or when the token cannot read them (a user's Projects need a token with the project scope)."""
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard", "Content-Type": "application/json"}
    return parse_projects(post(json.dumps({"query": PROJECTS_QUERY, "variables": {"owner": owner}}).encode("utf-8"), headers))


def planned_items(tools_dir: object) -> dict[str, list[dict]] | None:
    """The roadmap plans kept in this repository (tools/roadmap_defs.py and tools/seed_ecosystem_roadmap.py): {eco: [item]}, None when they cannot be imported."""
    import sys
    path = str(tools_dir)
    added = path not in sys.path
    if added:
        sys.path.insert(0, path)
    try:
        import roadmap_defs
        import seed_ecosystem_roadmap as seed
    except Exception:  # noqa: BLE001 - a plan that cannot be imported means "not verified", never a broken page
        return None
    finally:
        if added and path in sys.path:
            sys.path.remove(path)
    out: dict[str, list[dict]] = {}

    def keep(eco: str, item: Mapping) -> None:
        out.setdefault(eco, []).append({k: str(item.get(k) or "") for k in ("title", "repository", "status", "priority", "hardware")} | {"blocked": str(item.get("blocked_by") or "")})

    for eco, board in roadmap_defs.ROADMAPS.items():
        for item in board["items"]:
            keep(eco, item)
    seen: set[str] = set()
    updates = getattr(seed, "HYDRA_STATUS_UPDATES", {}) or {}
    for group in ("SEED_ITEMS", "DELIVERED_ITEMS", "NEXT_ITEMS", "HARDWARE_ITEMS", "CURRENT_ITEMS", "WAVE_ITEMS", "LATEST_ITEMS", "RECENT_ITEMS"):
        for item in getattr(seed, group, ()):
            if not isinstance(item, Mapping) or not item.get("title") or item["title"] in seen:
                continue
            seen.add(item["title"])
            update = updates.get(item["title"]) if isinstance(updates, Mapping) else None
            if isinstance(update, Mapping):
                item = {**item, "status": update.get("status", item.get("status")), "blocked_by": update.get("blocked_by", item.get("blocked_by"))}
            keep("hydra-umc", item)
    return out


def milestones(live: Mapping[str, Sequence[dict]] | None, planned: Mapping[str, Sequence[dict]] | None, ecosystems: Sequence[str]) -> dict:
    """{"source": "projects" | "plans" | "none", "eco": {eco: {"open": [...], "done": n, "total": n}}}: the open items first by status and by priority."""
    if live:
        source, data = "projects", live
    elif planned:
        source, data = "plans", planned
    else:
        return {"source": "none", "eco": {}}
    priority = {"Critical": 0, "High": 1, "Normal": 2, "Low": 3}
    out: dict[str, dict] = {}
    for eco in ecosystems:
        items = list(data.get(eco) or [])
        opened = [i for i in items if i.get("status", "").lower() not in ("done", "closed")]
        opened.sort(key=lambda i: (MILESTONE_ORDER.index(i["status"]) if i.get("status") in MILESTONE_ORDER else len(MILESTONE_ORDER),
                                   priority.get(i.get("priority", ""), 9), i.get("title", "").casefold()))
        out[eco] = {"open": opened, "done": len(items) - len(opened), "total": len(items)} if items else {"open": [], "done": 0, "total": 0}
    return {"source": source, "eco": out}


# ---------------------------------------------------------------------------
# 6. Technical debt
# ---------------------------------------------------------------------------

def months_between(start: date, end: date) -> int:
    months = (end.year - start.year) * 12 + end.month - start.month
    return max(0, months - (1 if end.day < start.day else 0))


def has_integration_tests(files: Sequence[str] | None) -> bool | None:
    """True when a top-level file or folder (or one in tests/ or test/) is named for integration or end-to-end tests; None when the files were not read."""
    if files is None:
        return None
    return any(word in name.lower() for name in files for word in INTEGRATION_WORDS)


def debt(repos: Mapping[str, Mapping], manifests: Mapping[str, Mapping | None], facts: Mapping[str, Mapping], today: str, months_limit: int) -> dict:
    """{"months": X, "scaffolding": {"items": [[repo, months]], "unverified": [repo]}, "integration": {"items": [repo], "unverified": [repo]},
    "hardware": {"items": [[repo, evidence]], "unverified": [repo]}}. A repository that cannot be judged is `unverified`, never counted as debt."""
    now = _day(today)
    old: list[list] = []
    old_unknown: list[str] = []
    no_integration: list[str] = []
    no_integration_unknown: list[str] = []
    hardware: list[list] = []
    hardware_unknown: list[str] = []
    for name in sorted(repos, key=str.casefold):
        repo = repos[name]
        fact = facts.get(name) or {}
        if repo.get("maturity") == "scaffolding":
            created = _day(fact.get("created"))
            if created is None or now is None:
                old_unknown.append(name)
            elif months_between(created, now) >= months_limit:
                old.append([name, months_between(created, now)])
        if repo.get("maturity") == "functional":
            found = has_integration_tests(fact.get("files") if name in facts else None)
            if found is None:
                no_integration_unknown.append(name)
            elif not found:
                no_integration.append(name)
        manifest = manifests.get(name)
        if repo.get("hardware") is True:
            evidence = manifest.get("evidence") if isinstance(manifest, Mapping) else None
            if not isinstance(evidence, str) or not evidence:
                hardware_unknown.append(name)
            elif evidence not in ("bench", "field"):
                hardware.append([name, evidence])
    old.sort(key=lambda r: (-r[1], r[0].casefold()))
    return {"months": months_limit,
            "scaffolding": {"items": old, "unverified": old_unknown},
            "integration": {"items": no_integration, "unverified": no_integration_unknown},
            "hardware": {"items": hardware, "unverified": hardware_unknown}}


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def build(*, repos: Mapping[str, Mapping], eco_by_name: Mapping[str, str], manifests: Mapping[str, Mapping | None], status: Mapping[str, Mapping[str, object]],
          history: Sequence[Mapping], today: str, config: Mapping, ecosystems: Sequence[str], facts: Mapping[str, Mapping] | None,
          weekly: Mapping[str, Mapping[str, int]] | None, live: Mapping[str, Sequence[dict]] | None, planned: Mapping[str, Sequence[dict]] | None) -> dict:
    """The "insight" block the page embeds. `facts`, `weekly`, `live` and `planned` are None (or empty) when they could not be read."""
    facts = facts or {}
    weekly = weekly or {}
    months = config.get("scaffolding_months")
    return {
        "today": today,
        "funnel": funnel(repos, ecosystems, history, today),
        "radar": radar(status, ecosystems),
        "heat": heatmap(eco_by_name, ecosystems, weekly, facts, today),
        "deps": dependencies(manifests, eco_by_name, ecosystems),
        "miles": milestones(live, planned, ecosystems),
        "debt": debt(repos, manifests, facts, today, months if isinstance(months, int) and not isinstance(months, bool) and months >= 1 else 6),
        "facts": bool(facts),
    }
