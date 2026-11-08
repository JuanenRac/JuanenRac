#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_integrity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The honest "Errors / unknown" count of the dashboard.

The dashboard lists the repositories whose manifest the updaters could read. A repository
whose manifest could not be read, or that no one found, is simply not listed - so counting
only the listed ones could never report anything. This module compares what the dashboard
listed with three independent sources and names every difference:

  * the catalogue tables of the profile README (every repository the profile promises),
  * the public repositories of the owner and the manifest files they carry,
  * the raw manifests of the listed repositories (maturity and evidence must be known values).

It also carries the failures of the GitHub API met while generating (listing, timeouts,
rate limits). The decision logic (`evaluate`) is pure; the network sits in `gather`, which
takes the fetch functions as arguments so the tests can simulate every case.

Stdlib only.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable

import gh_http

MATURITIES = ("scaffolding", "functional", "established", "production")
EVIDENCES = ("none", "host-test", "simulator", "bench", "field")

# The manifest file each ecosystem key of the dashboard is discovered from.
MANIFEST_FILES: dict[str, str] = {
    "hydra-umc": "hydra-umc.project.json",
    "urtc": "urtc.project.json",
    "armor": "armor.project.json",
    "eh3d": "eh3d.project.json",
    "electro-hobby-3d": "electro-hobby-3d.project.json",
}

# The kinds of problem, in the order the dashboard shows them.
KINDS = (
    "catalog_missing",    # the README catalogue lists it, the dashboard does not
    "invalid_manifest",   # it has a manifest the discovery could not read or accept
    "unlisted_manifest",  # it has a manifest of an ecosystem and is not on the dashboard, with no error to explain it
    "unknown_maturity",   # listed, but the maturity is missing or not one of the four levels
    "unknown_evidence",   # listed, but the evidence is missing or not one of the five kinds
    "api",                # a GitHub API failure while generating (listing, timeout, rate limit)
)

# Outcome of reading one manifest file: ("ok", dict) | ("absent", None) | ("error", message).
FetchResult = tuple[str, "dict | str | None"]
Fetcher = Callable[[str, str, str], FetchResult]   # (repo, branch, file) -> FetchResult


@dataclass(frozen=True)
class Issue:
    kind: str
    repo: str          # a repository name, or a short scope for an API failure
    ecosystem: str     # a dashboard ecosystem key, or "" when it is not known
    detail: str
    in_catalog: bool = False   # the repository is listed in the README catalogue (and is not on the dashboard)


@dataclass(frozen=True)
class RawManifest:
    ecosystem: str
    data: "dict | None"
    error: str = ""


def _error_for(repo: str, discovery_errors: Iterable[str]) -> str:
    prefix = f"{repo}:"
    for text in discovery_errors:
        if text.startswith(prefix):
            return text[len(prefix):].strip()
    return ""


def evaluate(
    *,
    catalog: dict[str, list[str]],
    listed: dict[str, str],
    discovery_errors: Iterable[str],
    raw_manifests: dict[str, RawManifest],
    owner_repos: "list[str] | None",
    api_failures: Iterable[tuple[str, str]] = (),
) -> list[Issue]:
    """Every difference between the dashboard and the sources, one `Issue` each (a repository gets at most one issue per kind)."""
    errors = list(discovery_errors)
    issues: dict[tuple[str, str], Issue] = {}

    def add(kind: str, repo: str, ecosystem: str, detail: str) -> None:
        issues.setdefault((kind, repo), Issue(kind, repo, ecosystem, detail))

    # 1. Manifests found by the independent read.
    for repo, raw in raw_manifests.items():
        if repo not in listed:
            reason = _error_for(repo, errors) or raw.error
            if reason:
                add("invalid_manifest", repo, raw.ecosystem, reason)
            else:
                add("unlisted_manifest", repo, raw.ecosystem, "the repository has a manifest the dashboard did not list")
            continue
        if raw.data is None:
            continue
        maturity = raw.data.get("maturity")
        evidence = raw.data.get("evidence")
        if maturity not in MATURITIES:
            add("unknown_maturity", repo, listed[repo], "maturity missing" if maturity is None else f"maturity {maturity!r} is not one of {'|'.join(MATURITIES)}")
        if evidence not in EVIDENCES:
            add("unknown_evidence", repo, listed[repo], "evidence missing" if evidence is None else f"evidence {evidence!r} is not one of {'|'.join(EVIDENCES)}")

    # 2. Discovery errors the independent read did not already explain.
    for text in errors:
        repo, sep, rest = text.partition(":")
        if sep and re.fullmatch(r"[A-Za-z0-9._-]+", repo) and repo not in listed:
            eco = next((key for key, names in catalog.items() if repo in names), "")
            add("invalid_manifest", repo, raw_manifests[repo].ecosystem if repo in raw_manifests else eco, rest.strip())
        elif not sep or not re.fullmatch(r"[A-Za-z0-9._-]+", repo):
            add("api", "discovery", "", text)

    # 3. The README catalogue against the dashboard.
    known_owner = set(owner_repos) if owner_repos is not None else None
    for eco, names in catalog.items():
        for repo in names:
            if repo in listed:
                continue
            explained = issues.get(("invalid_manifest", repo)) or issues.get(("unlisted_manifest", repo))
            if explained is not None:
                # already named with its own reason: say it once, and remember that the catalogue lists it
                issues[(explained.kind, repo)] = Issue(explained.kind, repo, explained.ecosystem or eco, explained.detail, True)
                continue
            if known_owner is not None and repo not in known_owner:
                issues[("catalog_missing", repo)] = Issue("catalog_missing", repo, eco, "listed in the README catalogue but not among the public repositories of the owner", True)
            else:
                issues[("catalog_missing", repo)] = Issue("catalog_missing", repo, eco, "listed in the README catalogue but no manifest of any ecosystem was found in it", True)

    # 4. API failures.
    for scope, message in api_failures:
        add("api", scope, "", message)

    order = {kind: index for index, kind in enumerate(KINDS)}
    return sorted(issues.values(), key=lambda issue: (order[issue.kind], issue.ecosystem, issue.repo.casefold()))


def counts_by_ecosystem(issues: Iterable[Issue], ecosystems: Iterable[str]) -> dict[str, int]:
    result = {key: 0 for key in ecosystems}
    result[""] = 0
    for issue in issues:
        result[issue.ecosystem if issue.ecosystem in result else ""] += 1
    return result


@dataclass(frozen=True)
class Coverage:
    """The criterion of the count: the dashboard lists every public repository of the owner that has the manifest of an ecosystem."""
    listed: int
    public: "int | None"          # None when the listing of the repositories failed
    without_manifest: tuple       # public repositories with no manifest of any ecosystem (the profile repository, for one)


def coverage(listed: dict, owner_repos: "list[str] | None", raw_manifests: dict) -> Coverage:
    if owner_repos is None:
        return Coverage(len(listed), None, ())
    plain = sorted((name for name in owner_repos if name not in listed and name not in raw_manifests), key=str.casefold)
    return Coverage(len(listed), len(owner_repos), tuple(plain))


def blocking(issues: Iterable[Issue]) -> list[Issue]:
    """The issues that make `--strict` fail: a repository of the catalogue that is not on the dashboard (whatever the reason), or an API failure."""
    return [issue for issue in issues if issue.kind in ("catalog_missing", "api") or issue.in_catalog]


def gather(
    *,
    owner: str,
    listed: dict[str, str],
    list_repos: Callable[[], "tuple[list[tuple[str, str]], str]"],
    fetch: Fetcher,
    max_workers: int = 8,
) -> tuple[dict[str, RawManifest], "list[str] | None", list[tuple[str, str]]]:
    """Read the manifests independently of the discovery.

    `list_repos()` returns ([(name, default_branch)], error) with error empty when the listing is complete.
    Returns (raw manifests, owner repository names or None when the listing failed, API failures).
    """
    failures: list[tuple[str, str]] = []
    repos, error = list_repos()
    if error:
        failures.append(("repository list", error))
    branch_of = {name: branch or "main" for name, branch in repos}
    names = sorted(set(branch_of) | set(listed))

    def read(name: str) -> tuple[str, "RawManifest | None", "str | None"]:
        branch = branch_of.get(name, "main")
        if name in listed:
            candidates = [listed[name]]
        else:
            candidates = list(MANIFEST_FILES)
        for eco in candidates:
            status, payload = fetch(name, branch, MANIFEST_FILES[eco])
            if status == "ok" and isinstance(payload, dict):
                return name, RawManifest(eco, payload), None
            if status == "ok":
                return name, RawManifest(eco, None, "manifest is not a JSON object"), None
            if status == "error":
                return name, None, f"{MANIFEST_FILES[eco]}: {payload}"
        return name, None, None

    raw: dict[str, RawManifest] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for name, manifest, failure in pool.map(read, names):
            if manifest is not None:
                raw[name] = manifest
            if failure:
                failures.append((name, failure))
    return raw, (None if error else [name for name, _ in repos]), failures


def _epoch(text: object) -> "int | None":
    """Epoch seconds of an ISO 8601 UTC time of the API (2001-12-21T11:00:00Z), None when it is not one."""
    if not isinstance(text, str):
        return None
    try:
        return int(datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
    except ValueError:
        return None


def github_listing(owner: str, token: str, timeout: float = 15, reader: "Callable | None" = None, details: "dict | None" = None) -> Callable[[], "tuple[list[tuple[str, str]], str]"]:
    """A `list_repos` for `gather`: every public non-fork repository of the owner, following all pages, with the first failure reported.
    The pages are read with the conditional reader of gh_http (a 304 costs no quota; a refused read uses the saved page). When `details` is given it receives
    `archived` (the names of the archived repositories, which stay in the list), `pushed` ({name: epoch seconds of the last push}) and `stale` (True when any page came from the saved copy)."""
    def run() -> "tuple[list[tuple[str, str]], str]":
        found: list[tuple[str, str]] = []
        page = 1
        get = reader or gh_http.shared().get
        if details is not None:
            details["archived"], details["stale"], details["pushed"] = [], False, {}
        while True:
            headers = {"User-Agent": "JuanenRac-dashboard-integrity", "Accept": "application/vnd.github+json"}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            reply = get(f"https://api.github.com/users/{owner}/repos?type=owner&per_page=100&page={page}", headers, timeout=timeout)
            if reply.how == "failed":
                return found, f"{reply.reason or 'unreadable'} listing page {page}"
            payload = reply.data
            if not isinstance(payload, list):
                return found, f"unexpected answer listing page {page}"
            if details is not None and reply.how == "stale":
                details["stale"] = True
            for item in payload:
                if isinstance(item, dict) and isinstance(item.get("name"), str) and item.get("fork") is not True:
                    if details is not None and item.get("archived") is True:
                        details["archived"].append(item["name"])
                    if details is not None:
                        moment = _epoch(item.get("pushed_at"))
                        if moment is not None:
                            details["pushed"][item["name"]] = moment
                    branch = item.get("default_branch")
                    found.append((item["name"], branch if isinstance(branch, str) and branch else "main"))
            if len(payload) < 100:
                return found, ""
            page += 1
    return run


def raw_fetcher(owner: str, timeout: float = 15) -> Fetcher:
    """A `fetch` for `gather`: one manifest file from raw.githubusercontent.com."""
    def run(repo: str, branch: str, file: str) -> FetchResult:
        request = urllib.request.Request(
            f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file}",
            headers={"User-Agent": "JuanenRac-dashboard-integrity"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                text = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            return ("absent", None) if exc.code == 404 else ("error", f"HTTP {exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return "error", f"lookup failed: {exc}"
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return "error", f"not valid JSON: {exc}"
        return "ok", data
    return run


def report(issues: list[Issue]) -> str:
    """The plain-text report printed while generating."""
    if not issues:
        return "INTEGRITY=OK nothing is missing, unreadable or unknown"
    lines = [f"INTEGRITY=PROBLEMS count={len(issues)}"]
    for issue in issues:
        lines.append(f"  - [{issue.kind}] {issue.repo} ({issue.ecosystem or '-'}): {issue.detail}")
    return "\n".join(lines)
