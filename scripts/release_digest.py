# =============================================================================
# Electro Hobby 3D - scripts/release_digest.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
#
# Release digest: what each ecosystem published in the last days (releases only, drafts and pre-releases left out), grouped by ecosystem.
# It goes to the job summary of the workflow, so it can be read from the Actions page or pasted into a post.
# =============================================================================
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

from ecosystem_inventory import Api, Repo, inventory, of_ecosystems, write_summary

LABELS = {"hydra-umc": "HYDRA-UMC", "urtc": "URTC", "armor": "A.R.M.O.R.", "eh3d": "EH3D", "electro-hobby-3d": "Electro Hobby 3D"}


def published_since(api: Api, owner: str, repo: Repo, since: datetime) -> list[dict]:
    releases = api.get(f"/repos/{owner}/{repo.name}/releases?per_page=5") or []
    out = []
    for item in releases:
        if item.get("draft") or item.get("prerelease") or not item.get("published_at"):
            continue
        when = datetime.fromisoformat(item["published_at"].replace("Z", "+00:00"))
        if when >= since:
            out.append({"repo": repo.name, "ecosystem": repo.ecosystem or "", "tag": item.get("tag_name", ""), "name": item.get("name") or item.get("tag_name", ""),
                        "url": item.get("html_url", ""), "when": when})
    return out


def digest(releases: list[dict], days: int) -> str:
    lines = ["## Release digest", ""]
    if not releases:
        lines.append(f"No release was published in the last {days} days.")
        return "\n".join(lines)
    lines.append(f"{len(releases)} release(s) in the last {days} days.")
    for key in LABELS:
        group = sorted((r for r in releases if r["ecosystem"] == key), key=lambda r: r["when"], reverse=True)
        if not group:
            continue
        lines += ["", f"### {LABELS[key]}"]
        lines += [f"- **{r['repo']}** [{r['tag']}]({r['url']}) - {r['when'].strftime('%Y-%m-%d')}" for r in group]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List the releases published recently across the four ecosystems")
    parser.add_argument("--owner", default="JuanenRac")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args(argv)
    api = Api()
    repos = of_ecosystems(inventory(api, args.owner))
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    with ThreadPoolExecutor(max_workers=8) as pool:
        groups = list(pool.map(lambda repo: published_since(api, args.owner, repo, since), repos))
    write_summary(digest([r for group in groups for r in group], args.days))
    return 0


if __name__ == "__main__":
    sys.exit(main())
