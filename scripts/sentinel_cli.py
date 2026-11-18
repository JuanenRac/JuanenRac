#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/sentinel_cli.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Reads the Sentinel figures of the dashboard from a terminal: one command, one table, five output formats. Standard library only, no request.

    python scripts/sentinel_cli.py <command> [--format text|table|plain|json|ndjson|csv] [--data DIR] [--strict]

Commands: `ecosystems` (repositories, red workflows, releases ready and versions raised without a release per group), `supply` (the supply chain card),
`delivery` (the delivery card), `red` (the red workflows) and `ready` (the repositories ready for a version). Every command lists the groups of
`ecosystem-catalog.json` in the order of the tabs, and a group with nothing read says `not verified`, never zero.

It only reads `data/sentinel.json` and `data/scripts-stats.json` (the files the dashboard is built from), so it never calls GitHub and shows exactly what the
page shows: counts, names of repositories, workflow files and version tags. Exit codes: 0 all read, 3 with `--strict` when something is to review, 4 when a
file is missing or unreadable, 2 for a wrong command line.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Mapping, Sequence

ROOT = Path(__file__).resolve().parent.parent
FORMATS = ("text", "table", "plain", "json", "ndjson", "csv")
COMMANDS = ("ecosystems", "supply", "delivery", "red", "ready")
NOT_VERIFIED = "not verified"
EXIT_OK, EXIT_USAGE, EXIT_REVIEW, EXIT_NO_DATA = 0, 2, 3, 4


def load_json(path: Path) -> "dict | None":
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def groups(catalog: "Mapping | None" = None) -> "list[tuple[str, str]]":
    """[(key, label)] of the catalogue, in the order of the tabs."""
    catalog = catalog if catalog is not None else (load_json(ROOT / "ecosystem-catalog.json") or {})
    return [(e["key"], str(e.get("label", e["key"]))) for e in catalog.get("ecosystems", []) if isinstance(e, Mapping) and isinstance(e.get("key"), str)]


def _num(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def ecosystem_rows(sentinel: Mapping, order: Sequence[tuple[str, str]]) -> list[dict]:
    table = sentinel.get("ecosystems") if isinstance(sentinel.get("ecosystems"), Mapping) else {}
    rows = []
    for key, label in order:
        row = table.get(key) if isinstance(table.get(key), Mapping) else None
        if row is None or not _num(row.get("read")):
            rows.append({"group": label, "repositories": NOT_VERIFIED, "read": NOT_VERIFIED, "red": NOT_VERIFIED, "ready": NOT_VERIFIED, "raised": NOT_VERIFIED, "state": NOT_VERIFIED})
            continue
        problems = _num(row.get("red")) + _num(row.get("unpub"))
        rows.append({"group": label, "repositories": _num(row.get("repos")), "read": _num(row.get("read")), "red": _num(row.get("red")), "ready": _num(row.get("cand")),
                     "raised": _num(row.get("unpub")), "state": "to review" if problems else "in order"})
    return rows


def supply_rows(scripts: Mapping, order: Sequence[tuple[str, str]]) -> list[dict]:
    """Per group: repositories read, uses of actions not fixed to a commit, uses that follow a branch, and the linter findings about permissions and the pull request trigger."""
    repos = scripts.get("repos") if isinstance(scripts.get("repos"), Mapping) else {}
    rows = []
    for key, label in order:
        read = unpinned = branch = perm = target = 0
        for record in repos.values():
            block = record.get("scripts") if isinstance(record, Mapping) else None
            if not isinstance(record, Mapping) or record.get("eco") != key or record.get("state") == "unread" or not isinstance(block, Mapping):
                continue
            read += 1
            for uses in (block.get("acts") or {}).values():
                if isinstance(uses, list) and len(uses) == 2:
                    if uses[1] in ("branch", "tag"):
                        unpinned += _num(uses[0])
                    if uses[1] == "branch":
                        branch += _num(uses[0])
            rules = ((block.get("lint") or {}).get("rules") or {}) if isinstance(block.get("lint"), Mapping) else {}
            perm += sum(_num(n) for n in rules.get("permissions", []))
            target += sum(_num(n) for n in rules.get("pr_target", []))
        if not read:
            rows.append({"group": label, "read": NOT_VERIFIED, "unpinned": NOT_VERIFIED, "branch": NOT_VERIFIED, "permissions": NOT_VERIFIED, "pr_target": NOT_VERIFIED, "state": NOT_VERIFIED})
        else:
            rows.append({"group": label, "read": read, "unpinned": unpinned, "branch": branch, "permissions": perm, "pr_target": target,
                         "state": "in order" if unpinned + branch + perm + target == 0 else "to review"})
    return rows


def delivery_rows(sentinel: Mapping, order: Sequence[tuple[str, str]]) -> "list[dict] | None":
    """None when the reading predates the delivery block (the page says so too)."""
    block = sentinel.get("delivery")
    if not isinstance(block, Mapping) or not isinstance(block.get("eco"), Mapping):
        return None
    eco = sentinel.get("ecosystems") if isinstance(sentinel.get("ecosystems"), Mapping) else {}
    rows = []
    for key, label in order:
        row = block["eco"].get(key) if isinstance(block["eco"].get(key), Mapping) else None
        if row is None or not _num(row.get("read")):
            rows.append({"group": label, "read": NOT_VERIFIED, "tag_without_release": NOT_VERIFIED, "release_without_notes": NOT_VERIFIED, "changelog_differs": NOT_VERIFIED,
                         "raised_not_published": NOT_VERIFIED, "state": NOT_VERIFIED})
            continue
        raised = _num((eco.get(key) or {}).get("unpub")) if isinstance(eco.get(key), Mapping) else 0
        total = _num(row.get("tagahead")) + _num(row.get("nonotes")) + _num(row.get("clmis")) + raised
        rows.append({"group": label, "read": _num(row.get("read")), "tag_without_release": _num(row.get("tagahead")), "release_without_notes": _num(row.get("nonotes")),
                     "changelog_differs": _num(row.get("clmis")), "raised_not_published": raised, "state": "in order" if total == 0 else "to review"})
    return rows


def red_rows(sentinel: Mapping) -> list[dict]:
    items = ((sentinel.get("ci") or {}).get("red") or []) if isinstance(sentinel.get("ci"), Mapping) else []
    return [{"repository": str(i.get("repo", "")), "workflow": str(i.get("wf", "")), "in_a_row": _num(i.get("streak")), "since": str(i.get("since") or "")}
            for i in items if isinstance(i, Mapping)]


def ready_rows(sentinel: Mapping) -> list[dict]:
    items = ((sentinel.get("releases") or {}).get("candidates") or []) if isinstance(sentinel.get("releases"), Mapping) else []
    return [{"repository": str(i.get("repo", "")), "entries": _num(i.get("entries")), "last_release": str(i.get("tag") or ""), "published": str(i.get("published") or "")}
            for i in items if isinstance(i, Mapping)]


def render(rows: Sequence[Mapping], fmt: str) -> str:
    """The rows in one of the formats. `text` is a short sentence per row, `table` aligns the columns, `plain` is tab separated with no header (for scripts)."""
    columns = list(rows[0]) if rows else []
    if fmt == "json":
        return json.dumps(list(rows), indent=2, ensure_ascii=False)
    if fmt == "ndjson":
        return "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    if fmt == "csv":
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            writer.writerow([row[c] for c in columns])
        return out.getvalue().rstrip("\n")
    if fmt == "plain":
        return "\n".join("\t".join(str(row[c]) for c in columns) for row in rows)
    if fmt == "table":
        cells = [[c.replace("_", " ")] + [str(row[c]) for row in rows] for c in columns]
        widths = [max(len(x) for x in col) for col in cells]
        lines = ["  ".join(col[0].ljust(w) for col, w in zip(cells, widths))]
        lines.append("  ".join("-" * w for w in widths))
        for i in range(len(rows)):
            lines.append("  ".join(col[i + 1].ljust(w) for col, w in zip(cells, widths)))
        return "\n".join(lines)
    return "\n".join(", ".join(f"{c.replace('_', ' ')}: {row[c]}" for c in columns) for row in rows)


def needs_review(rows: Sequence[Mapping]) -> bool:
    return any(row.get("state") == "to review" for row in rows) or (bool(rows) and "state" not in rows[0])


def run(argv: "Sequence[str] | None" = None, out=None, err=None) -> int:
    out = out or sys.stdout
    err = err or sys.stderr
    parser = argparse.ArgumentParser(prog="sentinel_cli.py", description="Read the Sentinel figures of the dashboard from the data files, with no request to GitHub.")
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("--format", choices=FORMATS, default="text")
    parser.add_argument("--data", default=str(ROOT / "data"), help="folder with sentinel.json and scripts-stats.json")
    parser.add_argument("--strict", action="store_true", help="exit with 3 when something is to review")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return EXIT_USAGE if exc.code else EXIT_OK
    data = Path(args.data)
    order = groups()
    if args.command in ("supply",):
        scripts = load_json(data / "scripts-stats.json")
        if scripts is None:
            print("scripts-stats.json is missing or unreadable", file=err)
            return EXIT_NO_DATA
        rows: "list[dict] | None" = supply_rows(scripts, order)
    else:
        sentinel = load_json(data / "sentinel.json")
        if sentinel is None:
            print("sentinel.json is missing or unreadable", file=err)
            return EXIT_NO_DATA
        if args.command == "ecosystems":
            rows = ecosystem_rows(sentinel, order)
        elif args.command == "delivery":
            rows = delivery_rows(sentinel, order)
            if rows is None:
                print("this reading has no delivery data yet: not verified", file=err)
                return EXIT_NO_DATA
        elif args.command == "red":
            rows = red_rows(sentinel)
        else:
            rows = ready_rows(sentinel)
    print(render(rows or [], args.format), file=out)
    return EXIT_REVIEW if args.strict and rows and needs_review(rows) else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(run())
