# =============================================================================
# Electro Hobby 3D - scripts/ci_watch.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
#
# CI watch: the latest finished run of every workflow of every repository of the four ecosystems, on its default branch. A workflow that
# is red is listed in the job summary and in ONE issue of the profile repository (created, updated, and closed when everything is green
# again), so a failure is noticed without opening a hundred Actions pages.
# =============================================================================
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from ecosystem_inventory import Api, Repo, inventory, of_ecosystems, sync_issue, write_summary

RED = {"failure", "timed_out", "startup_failure", "action_required"}
LABEL = "ci-watch"
TITLE = "CI watch: workflows that are red"


@dataclass
class Run:
    repo: str
    ecosystem: str
    workflow: str
    conclusion: str
    url: str
    sha: str


def latest_runs(api: Api, owner: str, repo: Repo) -> list[Run]:
    """The newest finished run of each workflow on the default branch; skipped and cancelled runs say nothing and are passed over."""
    data = api.get(f"/repos/{owner}/{repo.name}/actions/runs?branch={repo.branch}&status=completed&per_page=40") or {}
    seen: dict[str, Run] = {}
    for item in data.get("workflow_runs", []):
        conclusion = item.get("conclusion") or ""
        name = item.get("name") or str(item.get("workflow_id"))
        key = str(item.get("workflow_id") or name)   # by workflow, not by name: a run of an older, invalid version of the file carries its path as name
        if conclusion in ("skipped", "cancelled", "neutral", "") or key in seen:
            continue
        seen[key] = Run(repo.name, repo.ecosystem or "", name, conclusion, item.get("html_url", ""), (item.get("head_sha") or "")[:7])
    return list(seen.values())


def collect(api: Api, owner: str, repos: list[Repo], workers: int = 8) -> list[Run]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        groups = list(pool.map(lambda repo: latest_runs(api, owner, repo), [repo for repo in repos if not repo.archived]))
    return [run for group in groups for run in group]


def report(runs: list[Run], watched: int) -> tuple[str, str | None]:
    """(markdown for the summary, body of the issue or None when nothing is red)."""
    red = [run for run in runs if run.conclusion in RED]
    green = len(runs) - len(red)
    lines = [f"## CI watch", "", f"{watched} repositories watched, {len(runs)} workflows with a finished run: **{green} green, {len(red)} red**.", ""]
    if not red:
        lines.append("Everything is green.")
        return "\n".join(lines), None
    lines += ["| Repository | Ecosystem | Workflow | Result | Commit |", "|---|---|---|---|---|"]
    for run in sorted(red, key=lambda r: (r.ecosystem, r.repo.lower(), r.workflow)):
        lines.append(f"| {run.repo} | {run.ecosystem} | [{run.workflow}]({run.url}) | {run.conclusion} | `{run.sha}` |")
    text = "\n".join(lines)
    body = text.replace("## CI watch\n\n", "") + "\n\nThis issue is kept up to date by the *CI watch* workflow and closes by itself when every workflow is green again."
    return text, body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report the workflows that are red across the four ecosystems")
    parser.add_argument("--owner", default="JuanenRac")
    parser.add_argument("--issue-repo", default="JuanenRac", help="repository whose issue carries the report")
    parser.add_argument("--dry-run", action="store_true", help="print the report; do not touch issues")
    args = parser.parse_args(argv)
    api = Api()
    repos = of_ecosystems(inventory(api, args.owner))
    runs = collect(api, args.owner, repos)
    text, body = report(runs, len(repos))
    write_summary(text)
    if not args.dry_run:
        print("issue:", sync_issue(api, args.owner, args.issue_repo, LABEL, TITLE, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
