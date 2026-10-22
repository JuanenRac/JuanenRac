# =============================================================================
# Electro Hobby 3D - scripts/health_matrix.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
#
# Repository health matrix: which of the files that every project of the four ecosystems is expected to have are missing (licence,
# the eight READMEs, security policy, code of conduct, contributing guide, support file, changelog, a workflow, templates, a banner).
# One line per repository with a gap goes to the job summary and to ONE issue of the profile repository, which closes by itself when
# nothing is missing.
# =============================================================================
from __future__ import annotations

import argparse
import sys

from ecosystem_inventory import Api, Repo, inventory, of_ecosystems, sync_issue, write_summary

LABEL = "repo-health"
TITLE = "Repository health: files that are missing"
READMES = ["README.md", "README_spa.md", "README_deu.md", "README_fra.md", "README_ita.md", "README_jpn.md", "README_zho.md", "README_por.md"]
CHECKS = [
    ("licence", lambda f: "LICENSE" in f or "LICENSE.md" in f),
    ("8 READMEs", lambda f: all(name in f for name in READMES)),
    ("SECURITY.md", lambda f: "SECURITY.md" in f),
    ("CODE_OF_CONDUCT.md", lambda f: "CODE_OF_CONDUCT.md" in f),
    ("CONTRIBUTING.md", lambda f: "CONTRIBUTING.md" in f),
    ("SUPPORT.md", lambda f: "SUPPORT.md" in f),
    ("CHANGELOG.md", lambda f: "CHANGELOG.md" in f),
    ("a workflow", lambda f: any(p.startswith(".github/workflows/") for p in f)),
    ("issue templates", lambda f: any(p.startswith(".github/ISSUE_TEMPLATE/") for p in f)),
    ("pull request template", lambda f: ".github/PULL_REQUEST_TEMPLATE.md" in f),
    ("a banner", lambda f: any(p.startswith("images/") and "BANNER" in p.upper() and p.lower().endswith(".svg") for p in f)),
]


def gaps(repo: Repo) -> list[str]:
    return [name for name, ok in CHECKS if not ok(repo.files)]


def report(repos: list[Repo]) -> tuple[str, str | None]:
    missing = {repo.name: gaps(repo) for repo in repos if not repo.archived and gaps(repo)}
    total = len([r for r in repos if not r.archived])
    lines = ["## Repository health", "", f"{total} repositories checked, **{total - len(missing)} complete, {len(missing)} with something missing**.", ""]
    if not missing:
        lines.append("Every repository has all the expected files.")
        return "\n".join(lines), None
    lines += ["| Repository | Ecosystem | Missing |", "|---|---|---|"]
    by_name = {r.name: r for r in repos}
    for name in sorted(missing, key=str.lower):
        lines.append(f"| {name} | {by_name[name].ecosystem} | {', '.join(missing[name])} |")
    text = "\n".join(lines)
    return text, text.replace("## Repository health\n\n", "") + "\n\nThis issue is kept up to date by the *Repository health* workflow and closes by itself when nothing is missing."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report the expected files that the repositories of the four ecosystems lack")
    parser.add_argument("--owner", default="JuanenRac")
    parser.add_argument("--issue-repo", default="JuanenRac")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    api = Api()
    repos = of_ecosystems(inventory(api, args.owner))
    text, body = report(repos)
    write_summary(text)
    if not args.dry_run:
        print("issue:", sync_issue(api, args.owner, args.issue_repo, LABEL, TITLE, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
