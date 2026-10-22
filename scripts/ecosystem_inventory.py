# =============================================================================
# Electro Hobby 3D - scripts/ecosystem_inventory.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
#
# One look at every public repository of the account: which ecosystem it belongs to (by the manifest file at its root, the same
# contract the dashboard uses) and which files it has. The monitoring workflows (CI watch, link check, release digest, health matrix)
# all start from this, so none of them keeps a list of projects of its own.
#
# Standard library only. The GitHub API is reached through a small `Api` object so the tests can replace it.
# =============================================================================
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

API = "https://api.github.com"
CATALOG = Path(__file__).resolve().parent.parent / "ecosystem-catalog.json"


class Api:
    """GET requests to the GitHub REST API with a token when there is one; raises RuntimeError with a readable message."""

    def __init__(self, token: str | None = None, pause_s: float = 0.0) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
        self.pause_s = pause_s

    def get(self, path: str):
        request = urllib.request.Request(
            API + path,
            headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "electro-hobby-3d-monitor"}
            | ({"Authorization": f"Bearer {self.token}"} if self.token else {}),
        )
        last: Exception | None = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=30) as reply:
                    return json.loads(reply.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                if error.code in (404, 409):   # 409: the repository is empty
                    return None
                last = RuntimeError(f"GET {path}: HTTP {error.code}")
                if error.code not in (429, 500, 502, 503, 504):
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                last = RuntimeError(f"GET {path}: {error}")
            time.sleep(1 + attempt)
        raise last or RuntimeError(f"GET {path} failed")

    def send(self, method: str, path: str, body: dict):
        """POST/PATCH with a JSON body; needs a token with the right to write. Returns the JSON answer."""
        request = urllib.request.Request(
            API + path,
            data=json.dumps(body).encode("utf-8"),
            method=method,
            headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "electro-hobby-3d-monitor",
                     "Content-Type": "application/json", "Authorization": f"Bearer {self.token}"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as reply:
                return json.loads(reply.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"{method} {path}: HTTP {error.code}") from error

    def paged(self, path: str):
        page = 1
        while True:
            items = self.get(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
            if not isinstance(items, list):
                return
            yield from items
            if len(items) < 100:
                return
            page += 1


@dataclass
class Repo:
    name: str
    branch: str
    ecosystem: str | None = None
    files: set[str] = field(default_factory=set)
    archived: bool = False
    description: str = ""


def manifest_files(catalog_text: str | None = None) -> dict[str, str]:
    """manifest file name -> ecosystem key, read from ecosystem-catalog.json."""
    data = json.loads(catalog_text if catalog_text is not None else CATALOG.read_text(encoding="utf-8"))
    return {item["manifest_file"]: item["key"] for item in data["ecosystems"]}


def inventory(api: Api, owner: str, manifests: dict[str, str] | None = None, workers: int = 8) -> list[Repo]:
    """Every public, non-fork repository of `owner` with its ecosystem and the paths of its default branch."""
    manifests = manifests or manifest_files()
    repos = [
        Repo(name=item["name"], branch=item.get("default_branch") or "main", archived=bool(item.get("archived")), description=item.get("description") or "")
        for item in api.paged(f"/users/{owner}/repos?type=owner")
        if isinstance(item, dict) and not item.get("fork")
    ]

    def fill(repo: Repo) -> Repo:
        tree = api.get(f"/repos/{owner}/{repo.name}/git/trees/{repo.branch}?recursive=1")
        if isinstance(tree, dict):
            repo.files = {entry["path"] for entry in tree.get("tree", []) if entry.get("type") == "blob"}
        for filename, key in manifests.items():
            if filename in repo.files:
                repo.ecosystem = key
                break
        return repo

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return sorted(pool.map(fill, repos), key=lambda repo: repo.name.lower())


def of_ecosystems(repos: list[Repo]) -> list[Repo]:
    """Only the repositories that belong to an ecosystem (the others are not part of the family)."""
    return [repo for repo in repos if repo.ecosystem]


def sync_issue(api, owner: str, repo: str, label: str, title: str, body: str | None) -> str:
    """Keep one issue per report: create it or update it when there is something to say, close it when `body` is None (everything is fine).
    Returns what was done: created, updated, unchanged, closed or nothing."""
    open_issues = [i for i in (api.get(f"/repos/{owner}/{repo}/issues?state=open&labels={label}&per_page=20") or []) if "pull_request" not in i]
    current = open_issues[0] if open_issues else None
    if body is None:
        if current is None:
            return "nothing"
        api.send("PATCH", f"/repos/{owner}/{repo}/issues/{current['number']}", {"state": "closed", "state_reason": "completed"})
        return "closed"
    if current is None:
        api.send("POST", f"/repos/{owner}/{repo}/issues", {"title": title, "body": body, "labels": [label]})
        return "created"
    if (current.get("body") or "").strip() == body.strip():
        return "unchanged"
    api.send("PATCH", f"/repos/{owner}/{repo}/issues/{current['number']}", {"body": body})
    return "updated"


def write_summary(text: str, path: str | None = None) -> None:
    """The text goes to the job summary of the workflow (or to the screen when it runs by hand)."""
    target = path or os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as stream:
            stream.write(text + "\n")
    else:
        print(text)
