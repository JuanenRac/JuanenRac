#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_contrib.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Which repositories make up each percentage of the status dashboard.

The README (and the progress bars of the page) say "9 of 10 repositories have tests". This module answers *which* ones, with the same
rules as scripts/ecosystem_status.py (the areas) and scripts/ecosystem_progress.py (the points of a repository):

  * `fetch_signals` reads the facts that do not live in the manifest (tags, README files, a tests folder) for the whole account with the GraphQL API,
  * `area_flags` decides, for one repository, whether it meets each of the eight areas (True / False / None when it could not be verified),
  * `build` groups the repositories by ecosystem and area, ready to be written into the page.

Nothing is invented: a fact that could not be read is None and the page prints "not verified". Stdlib only, the network is injectable.
"""
from __future__ import annotations

import json
import re
from typing import Callable, Iterable, Mapping

import ecosystem_progress as progress
from dashboard_charts import AREAS, Activity, Poster, _post

SIGNALS_QUERY = """
query($owner: String!, $cursor: String) {
  repositoryOwner(login: $owner) {
    repositories(first: 25, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        refs(refPrefix: "refs/tags/") { totalCount }
        root: object(expression: "HEAD:") { ... on Tree { entries { name } } }
        readme: object(expression: "HEAD:README.md") { ... on Blob { text } }
      }
    }
  }
}
"""
_README_FILE = re.compile(r"README(_[a-z]{3})?\.md")
_TESTS_BADGE = re.compile(r"Tests-([\d,\.]+)")
_TESTS_FOLDERS = {"tests", "test", "__tests__", "spec"}


def parse_signals(nodes: Iterable[Mapping]) -> dict[str, dict]:
    """{repository: {releases, readmes, tests}} (the CI fact is added later from the CI state of the latest commit)."""
    out: dict[str, dict] = {}
    for node in nodes:
        if not isinstance(node, Mapping) or not node.get("name"):
            continue
        tags = (node.get("refs") or {}).get("totalCount")
        entries = (node.get("root") or {}).get("entries")
        if not isinstance(tags, int) or not isinstance(entries, list):
            continue                      # not readable: the repository stays out and its facts are "not verified"
        names = {str(item.get("name", "")) for item in entries if isinstance(item, Mapping)}
        tests = bool(names & _TESTS_FOLDERS)
        if not tests:
            match = _TESTS_BADGE.search(str((node.get("readme") or {}).get("text") or ""))
            tests = bool(match and re.sub(r"[^\d]", "", match.group(1)) not in ("", "0"))
        out[str(node["name"])] = {"releases": min(tags, 100), "readmes": sum(1 for n in names if _README_FILE.fullmatch(n)), "tests": tests}
    return out


def fetch_signals(owner: str, token: str, activity: Mapping[str, Activity], post: Poster = _post, max_pages: int = 12) -> dict[str, dict]:
    """The delivery and quality facts of every public repository of the owner. {} without a token or on any failure (the page says "not verified").
    A repository that is not in `activity` keeps ci unknown: the key is left out of its facts."""
    if not token:
        return {}
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard", "Content-Type": "application/json"}
    found: dict[str, dict] = {}
    cursor = None
    for _ in range(max_pages):
        answer = post(json.dumps({"query": SIGNALS_QUERY, "variables": {"owner": owner, "cursor": cursor}}).encode("utf-8"), headers)
        try:
            page = answer["data"]["repositoryOwner"]["repositories"]
            found.update(parse_signals(page["nodes"]))
            if not page["pageInfo"]["hasNextPage"]:
                break
            cursor = page["pageInfo"]["endCursor"]
        except (TypeError, KeyError):
            return {}
    for name, facts in found.items():
        if name in activity:
            facts["ci"] = activity[name].ci == "success"
    return found


def area_flags(manifest: Mapping, signals: Mapping | None) -> dict[str, bool | None]:
    """Whether one repository meets each area, by the rules of ecosystem_status.measure. None = could not be verified; an area that does not
    apply to the repository (real hardware for a repository that does not depend on it) is left out."""
    maturity = str(manifest.get("maturity", "")).lower()
    evidence = str(manifest.get("evidence", "")).lower()
    flags: dict[str, bool | None] = {
        "software": maturity in ("functional", "established", "production"),
        "tests": bool(signals.get("tests")) if signals is not None else None,
        "ci": bool(signals["ci"]) if signals is not None and "ci" in signals else None,
        "releases": int(signals.get("releases", 0)) >= 1 if signals is not None else None,
        "docs": int(signals.get("readmes", 0)) >= 8 if signals is not None else None,
        "simulation": evidence in ("simulator", "bench", "field"),
        "production": maturity in ("established", "production"),
    }
    if manifest.get("hardware_bound") is not False:
        flags["hardware"] = evidence in ("bench", "field")
    return {area: flags[area] for area in AREAS if area in flags}


def points_of(manifest: Mapping, signals: Mapping | None) -> int:
    return progress.project_points(dict(manifest), dict(signals) if signals else None)


def build(listed: Mapping[str, str], manifests: Mapping[str, Mapping | None], signals: Mapping[str, Mapping], ecosystems: Iterable[str],
          readme_counts: Mapping[str, Mapping[str, tuple[int | None, int | None]]] | None = None) -> dict:
    """{ecosystem: {"progress": [[repository, maturity, points, verified], ...], "areas": {area: {"yes": [...], "no": [...], "unknown": [...], "readme": [k, n]}}}}
    Only the repositories whose manifest could be read are counted, like the README does; every list is sorted by name."""
    out: dict = {}
    for eco in ecosystems:
        names = sorted((n for n, e in listed.items() if e == eco and isinstance(manifests.get(n), Mapping)), key=str.casefold)
        areas: dict[str, dict] = {a: {"yes": [], "no": [], "unknown": []} for a in AREAS}
        rows = []
        for name in names:
            manifest = manifests[name]
            facts = signals.get(name)
            maturity = str(manifest.get("maturity", "")).lower() or "unknown"
            rows.append([name, maturity, points_of(manifest, facts), facts is not None])
            for area, flag in area_flags(manifest, facts).items():
                areas[area]["unknown" if flag is None else "yes" if flag else "no"].append([name, maturity])
        for area, counts in ((readme_counts or {}).get(eco) or {}).items():
            if area in areas and counts and counts[0] is not None and counts[1] is not None:
                areas[area]["readme"] = [counts[0], counts[1]]
        rows.sort(key=lambda row: (-row[2], row[0].casefold()))
        out[eco] = {"progress": rows, "areas": areas}
    return out
