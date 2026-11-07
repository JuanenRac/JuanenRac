#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_code.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The block "code" of the data the status dashboard embeds: the lines of code, tests and documentation of every repository.

The figures are produced once a day by scripts/code_stats.py (workflow code-stats.yml) and kept in `data/code-stats.json` and `data/code-history.json`. The
page generator only reads them. `build` rebuilds the block from a whitelist: a field that is not known is dropped, a number that is not a plain number is
replaced by zero, and a repository of an ecosystem the document does not declare is ignored, so the page never embeds what it did not expect. A document that
cannot be read gives `read: false` and the tab says "not verified" instead of showing zeros. Stdlib only.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Mapping

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATS_PATH = DATA_DIR / "code-stats.json"
HISTORY_PATH = DATA_DIR / "code-history.json"
MAX_NUMBER = 10 ** 10
MAX_POINTS = 800
DAY = re.compile(r"\d{4}-\d{2}-\d{2}")
NAME = re.compile(r"[A-Za-z0-9._-]{1,100}")
KEY = re.compile(r"[a-z0-9-]{1,40}")
STATES = ("ok", "lastknown", "unread")


def _num(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= MAX_NUMBER else 0


def _day(value: object) -> str | None:
    return value if isinstance(value, str) and DAY.fullmatch(value) else None


def _counts(raw: object, fields: tuple[str, ...]) -> dict:
    raw = raw if isinstance(raw, Mapping) else {}
    return {field: _num(raw.get(field)) for field in fields}


def _text(value: object, limit: int = 120) -> str:
    return value[:limit] if isinstance(value, str) else ""


def _listed(raw: object, kinds: int, limit: int) -> list:
    out = []
    for item in (raw if isinstance(raw, list) else [])[:limit]:
        if isinstance(item, list) and len(item) == 2 and isinstance(item[0], int) and not isinstance(item[0], bool) and 0 <= item[0] < kinds:
            out.append([item[0], _text(item[1])])
    return out


def _changes(raw: object, kind_keys: list[str]) -> dict | None:
    """The statistics of a changelog, rebuilt from a whitelist (None when the repository has none)."""
    if not isinstance(raw, Mapping):
        return None
    n_kinds = len(kind_keys)

    def kinds(value: object) -> dict:
        value = value if isinstance(value, Mapping) else {}
        return {k: _num(value.get(k)) for k in kind_keys}
    versions = []
    for row in (raw.get("v") if isinstance(raw.get("v"), list) else [])[:60]:
        if not (isinstance(row, list) and len(row) >= 3 and isinstance(row[0], str) and isinstance(row[2], list) and len(row[2]) == n_kinds):
            continue
        item = [_text(row[0], 60), _num(row[1]), [_num(c) for c in row[2]]]
        if len(row) > 3:
            item.append(_listed(row[3], n_kinds, 80))
        versions.append(item)
    avg = raw.get("avg")
    return {"versions": _num(raw.get("versions")), "entries": _num(raw.get("entries")), "unreleased": _num(raw.get("unreleased")),
            "avg": round(avg, 1) if isinstance(avg, (int, float)) and not isinstance(avg, bool) and 0 <= avg < 10 ** 6 else 0,
            "kinds": kinds(raw.get("kinds")), "published_kinds": kinds(raw.get("published_kinds")), "u": _listed(raw.get("u"), n_kinds, 60), "v": versions}


def _rel(raw: object) -> dict | None:
    if not isinstance(raw, Mapping):
        return None
    gap = raw.get("gap")
    return {"tags": _num(raw.get("tags")), "last": _day(raw.get("last")), "d30": _num(raw.get("d30")), "d90": _num(raw.get("d90")),
            "gap": round(gap, 1) if isinstance(gap, (int, float)) and not isinstance(gap, bool) and 0 <= gap < 10 ** 5 else None}


def _repo(raw: object, ecos: set[str], types: set[str], kind_keys: list[str]) -> dict | None:
    if not isinstance(raw, Mapping) or raw.get("eco") not in ecos or raw.get("type") not in types or raw.get("state") not in STATES:
        return None
    out: dict = {"eco": raw["eco"], "type": raw["type"], "state": raw["state"], "pushed": _day(raw.get("pushed"))}
    if raw["state"] == "unread":
        return out
    langs = raw.get("langs") if isinstance(raw.get("langs"), Mapping) else {}
    out.update({
        "commit": _day(raw.get("commit")), "files": _num(raw.get("files")), "size": _num(raw.get("size")),
        "langs": {str(name)[:40]: _counts(value, ("files", "code", "comment", "blank")) for name, value in sorted(langs.items())[:60]},
        "code": _counts(raw.get("code"), ("files", "code", "comment", "blank")),
        "tests": _counts(raw.get("tests"), ("files", "code", "comment", "blank", "cases")),
        "docs": _counts(raw.get("docs"), ("files", "lines", "blank")),
        "l10n": _counts(raw.get("l10n"), ("files", "lines")),
        "data": _counts(raw.get("data"), ("files", "lines")),
    })
    out["changes"] = _changes(raw.get("changes"), kind_keys)
    out["rel"] = _rel(raw.get("rel"))
    if isinstance(raw.get("declared_tests"), int) and not isinstance(raw.get("declared_tests"), bool):
        out["declared_tests"] = _num(raw["declared_tests"])
    return out


def _group(raw: object, keys: set[str]) -> dict:
    raw = raw if isinstance(raw, Mapping) else {}
    return {key: _counts(value, ("repos", "code", "tests", "docs")) for key, value in raw.items() if key in keys}


CHANGE_FIELDS = ("repos", "versions", "entries", "unreleased", "fix", "unclassified")


def _point(raw: object, ecos: set[str], types: set[str]) -> dict | None:
    if not isinstance(raw, Mapping) or _day(raw.get("d")) is None:
        return None
    ce = raw.get("ce") if isinstance(raw.get("ce"), Mapping) else {}
    return {"d": raw["d"], "t": _counts(raw.get("t"), ("repos", "code", "comment", "tests", "docs", "files", "size", "cases", "l10n_files")),
            "e": _group(raw.get("e"), ecos), "y": _group(raw.get("y"), types),
            "c": _counts(raw.get("c"), CHANGE_FIELDS), "ce": {k: _counts(v, CHANGE_FIELDS) for k, v in ce.items() if k in ecos}}


def load(path: Path = STATS_PATH) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def load_history(path: Path = HISTORY_PATH) -> list[dict]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    points = value.get("points") if isinstance(value, dict) else None
    return [p for p in points if isinstance(p, dict)] if isinstance(points, list) else []


def build(doc: object, history: object = None, today: str | None = None) -> dict:
    """The block embedded in the page. `today` (YYYY-MM-DD) gives the age of the figures in days."""
    empty = {"read": False, "day": None, "age": None, "ecos": [], "types": [], "kinds": [], "repos": {}, "history": [], "totals": {}}
    if not isinstance(doc, Mapping) or doc.get("schema") != 1 or not isinstance(doc.get("repos"), Mapping):
        return empty
    ecos = [{"key": e["key"], "label": str(e.get("label", e["key"]))[:40]} for e in (doc.get("ecosystems") or []) if isinstance(e, Mapping) and isinstance(e.get("key"), str) and KEY.fullmatch(e["key"])]
    types = [t for t in (doc.get("types") or []) if isinstance(t, str) and KEY.fullmatch(t)]
    eco_keys, type_keys = {e["key"] for e in ecos}, set(types)
    kind_keys = [k for k in (doc.get("kinds") or []) if isinstance(k, str) and KEY.fullmatch(k)]
    repos = {}
    for name, raw in doc["repos"].items():
        if isinstance(name, str) and NAME.fullmatch(name):
            record = _repo(raw, eco_keys, type_keys, kind_keys)
            if record is not None:
                repos[name] = record
    points = [p for p in (_point(raw, eco_keys, type_keys) for raw in (history if isinstance(history, list) else [])) if p is not None]
    points = sorted({p["d"]: p for p in points}.values(), key=lambda p: p["d"])[-MAX_POINTS:]
    day = _day(doc.get("day"))
    age = None
    if day and today and DAY.fullmatch(today):
        age = (date.fromisoformat(today) - date.fromisoformat(day)).days
    read = any(r["state"] != "unread" for r in repos.values())
    return {"read": read, "day": day, "age": age, "ecos": ecos, "types": types, "kinds": kind_keys, "repos": repos, "history": points,
            "totals": _counts(doc.get("totals"), ("repos", "files", "size", "code", "comment", "blank", "tests", "test_files", "cases", "docs", "l10n_files", "data"))}
