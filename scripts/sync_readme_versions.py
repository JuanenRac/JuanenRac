#!/usr/bin/env python3
# =============================================================================
# Electro Hobby 3D - scripts/sync_readme_versions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Fills in (and keeps current) the "Version" column of every project-catalog
# table in every README_*.md, reading each repository's own real manifest -
# never typed by hand, and never stale.
#
# A table with only a Repository/Description column pair is upgraded to
# three columns the first time this runs; a table that already has a
# Version column (A.R.M.O.R.'s own, written by hand once) just gets its
# values refreshed on every run after that, same as the other two
# ecosystems from then on.
#
# A repository's own manifest is read from the local sibling checkout when
# one exists (the fast, free path on a developer machine that already has
# every ecosystem repo checked out next to this one) and otherwise fetched
# from raw.githubusercontent.com (the only path available in CI, which
# checks out just this one repository) - the exact same fallback
# generate_dashboard.py's own manifest lookup already uses, for the same
# reason: this script was real and working, but never wired into any
# workflow, because it could only ever run somewhere with all 77 sibling
# repos already cloned. It now runs the same way the dashboard does.
#
# Usage:  python scripts/sync_readme_versions.py            # writes every README
#         python scripts/sync_readme_versions.py --check    # exit 1 if any is stale
# =============================================================================
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIBLINGS = ROOT.parent  # the GitHub/ folder: every ecosystem repo is a sibling of JuanenRac, on a dev machine

API_USER_AGENT = "JuanenRac-sync-readme-versions"
RAW_REQUEST_TIMEOUT_S = 10

README_FILES = [
    "README.md", "README_spa.md", "README_fra.md", "README_ita.md",
    "README_deu.md", "README_zho.md", "README_jpn.md",
]

VERSION_HEADER = {
    "README.md": "Version", "README_spa.md": "Versión", "README_fra.md": "Version",
    "README_ita.md": "Versione", "README_deu.md": "Version", "README_zho.md": "版本",
    "README_jpn.md": "バージョン",
}

# Each repository may use a different manifest filename depending on which
# ecosystem it belongs to - tried in this order, first one found wins.
MANIFEST_CANDIDATES = ("armor.project.json", "urtc.project.json", "hydra-umc.project.json")

REPO_LINK = re.compile(r"^\[([A-Za-z0-9.\-]+)\]\(https://github\.com/JuanenRac/([A-Za-z0-9.\-]+)\)")
CELL_SPLIT = re.compile(r"(?<!\\)\|")

_version_cache: dict[str, str | None] = {}


def _version_from_manifest_text(text: str) -> str | None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    version = data.get("version")
    return version if isinstance(version, str) else None


def _fetch_raw(name: str, candidate: str) -> str | None:
    url = f"https://raw.githubusercontent.com/JuanenRac/{name}/main/{candidate}"
    request = urllib.request.Request(url, headers={"User-Agent": API_USER_AGENT}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=RAW_REQUEST_TIMEOUT_S) as response:
            return response.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def repo_version(name: str) -> str | None:
    if name in _version_cache:
        return _version_cache[name]

    repo_dir = SIBLINGS / name
    version: str | None = None
    for candidate in MANIFEST_CANDIDATES:
        manifest_path = repo_dir / candidate
        if manifest_path.is_file():
            try:
                version = _version_from_manifest_text(manifest_path.read_text(encoding="utf-8"))
            except OSError:
                version = None
            break
    else:
        # No local sibling checkout (the real case in CI, which only ever
        # checks out this one repository) - the same three candidate
        # filenames, fetched from GitHub instead of the filesystem.
        for candidate in MANIFEST_CANDIDATES:
            raw = _fetch_raw(name, candidate)
            if raw is not None:
                version = _version_from_manifest_text(raw)
                break

    _version_cache[name] = version
    return version


def split_row(line: str) -> list[str] | None:
    """Splits a real markdown table row into its cells, or None if `line`
    is not one (doesn't start and end with the pipe a table row needs)."""
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in CELL_SPLIT.split(stripped[1:-1])]


def is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells)


def process(lines: list[str], version_header: str) -> tuple[list[str], int]:
    out: list[str] = []
    changed = 0
    i = 0
    while i < len(lines):
        header_cells = split_row(lines[i])
        if (
            header_cells is not None
            and i + 2 < len(lines)
            and (sep_cells := split_row(lines[i + 1])) is not None
            and is_separator_row(sep_cells)
            and len(header_cells) == len(sep_cells)
            and (first_row_cells := split_row(lines[i + 2])) is not None
            and REPO_LINK.match(first_row_cells[0])
        ):
            width = len(header_cells)
            has_version_column = width == 3
            # A real repository table: upgrade (2 -> 3 columns) or refresh
            # (already 3) every data row that follows, until a non-table line.
            out.append(lines[i] if has_version_column else f"| {header_cells[0]} | {version_header} | {header_cells[-1]} |")
            out.append(lines[i + 1] if has_version_column else "| :--- | :--- | :--- |")
            i += 2
            while i < len(lines):
                row_cells = split_row(lines[i])
                if row_cells is None or not REPO_LINK.match(row_cells[0]):
                    break
                match = REPO_LINK.match(row_cells[0])
                version = repo_version(match.group(2)) or (row_cells[1] if has_version_column else "?")
                description = row_cells[-1]
                new_line = f"| {row_cells[0]} | {version} | {description} |"
                if new_line != lines[i]:
                    changed += 1
                out.append(new_line)
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return out, changed


def main() -> int:
    check = "--check" in sys.argv
    stale: list[str] = []
    total_changed = 0
    for filename in README_FILES:
        path = ROOT / filename
        raw = path.read_bytes()
        crlf = b"\r\n" in raw
        text = raw.decode("utf-8").replace("\r\n", "\n")
        lines = text.split("\n")
        new_lines, changed = process(lines, VERSION_HEADER[filename])
        if changed:
            if check:
                stale.append(f"{filename} ({changed} row(s))")
            else:
                new_text = "\n".join(new_lines)
                path.write_bytes((new_text.replace("\n", "\r\n") if crlf else new_text).encode("utf-8"))
                total_changed += changed
    if check:
        if stale:
            print("SYNC_README_VERSIONS=STALE " + ", ".join(stale))
            return 1
        print("SYNC_README_VERSIONS=CURRENT")
        return 0
    print(f"SYNC_README_VERSIONS=DONE rows_updated={total_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
