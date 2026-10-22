# =============================================================================
# Electro Hobby 3D - scripts/link_check.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
#
# Link check of the READMEs of the four ecosystems: every link to another repository of the account must point to a repository that
# exists, and every relative link (a document, an image) must point to a file that is in that repository. The eight languages are
# checked. Only the links that live inside the account are followed: nothing outside is fetched, so the check is quick and does not
# depend on other people's servers.
# =============================================================================
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from posixpath import normpath

from ecosystem_inventory import Api, Repo, inventory, of_ecosystems, sync_issue, write_summary

README_NAMES = ["README.md", "README_spa.md", "README_deu.md", "README_fra.md", "README_ita.md", "README_jpn.md", "README_zho.md", "README_por.md"]
LABEL = "link-check"
TITLE = "Link check: broken links in the READMEs"
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)")
HTML_SRC = re.compile(r"""(?:src|href)=["']([^"']+)["']""")


def fetch(owner: str, repo: Repo, name: str) -> str | None:
    url = f"https://raw.githubusercontent.com/{owner}/{repo.name}/{repo.branch}/{name}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "electro-hobby-3d-monitor"}), timeout=30) as reply:
            return reply.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def links_of(text: str) -> list[str]:
    found = MARKDOWN_LINK.findall(text) + HTML_SRC.findall(text)
    return [link.strip() for link in found if link.strip()]


def problems_in(text: str, owner: str, repo: Repo, names: set[str], existing_files: set[str]) -> list[str]:
    """What is wrong with the links of one README: a repository of the account that does not exist, or a relative file that is not there."""
    own = re.compile(rf"^https://github\.com/{re.escape(owner)}/([A-Za-z0-9_.-]+)(?:[/#?].*)?$", re.IGNORECASE)
    out: list[str] = []
    for link in links_of(text):
        match = own.match(link)
        if match:
            target = match.group(1)
            if target.endswith(".git"):
                target = target[:-4]
            if target.lower() not in names:
                out.append(f"link to a repository that does not exist: {link}")
        elif not re.match(r"^([a-z][a-z0-9+.-]*:|#|//|mailto:)", link, re.IGNORECASE):
            path = normpath(link.split("#", 1)[0].split("?", 1)[0].lstrip("/"))
            if path and not path.startswith("..") and path not in existing_files and not any(f.startswith(path + "/") for f in existing_files):
                out.append(f"relative link to a file that is not in the repository: {link}")
    return out


def check(owner: str, repos: list[Repo], getter=fetch, workers: int = 8, all_names: set[str] | None = None) -> dict[str, list[str]]:
    names = all_names if all_names is not None else {repo.name.lower() for repo in repos}
    result: dict[str, list[str]] = {}

    def one(repo: Repo) -> tuple[str, list[str]]:
        found: list[str] = []
        for name in README_NAMES:
            text = getter(owner, repo, name)
            if text is None:
                if name in repo.files or name == "README.md":
                    found.append(f"{name}: missing" if name == "README.md" else f"{name}: listed but not readable")
                continue
            found += [f"{name}: {problem}" for problem in problems_in(text, owner, repo, names, repo.files)]
        return repo.name, found

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for name, found in pool.map(one, [repo for repo in repos if not repo.archived]):
            if found:
                result[name] = found
    return result


def report(result: dict[str, list[str]], checked: int) -> tuple[str, str | None]:
    lines = ["## Link check", "", f"{checked} repositories, eight READMEs each: **{sum(len(v) for v in result.values())} broken link(s) in {len(result)} repositories**.", ""]
    if not result:
        lines.append("Every link inside the account resolves.")
        return "\n".join(lines), None
    for name in sorted(result, key=str.lower):
        lines.append(f"### {name}")
        lines += [f"- {problem}" for problem in result[name][:25]]
        lines.append("")
    text = "\n".join(lines)
    return text, text.replace("## Link check\n\n", "") + "\nThis issue is kept up to date by the *Link check* workflow and closes by itself when every link resolves."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the links that stay inside the account in the READMEs of the four ecosystems")
    parser.add_argument("--owner", default="JuanenRac")
    parser.add_argument("--issue-repo", default="JuanenRac")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    api = Api()
    everything = inventory(api, args.owner)
    repos = of_ecosystems(everything)
    result = check(args.owner, repos, all_names={repo.name.lower() for repo in everything})
    text, body = report(result, len(repos))
    write_summary(text)
    if not args.dry_run:
        print("issue:", sync_issue(api, args.owner, args.issue_repo, LABEL, TITLE, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
