#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_scripts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The block "scripts" of the data the status dashboard embeds: the workflows, the actions and the own scripts of every repository.

The figures are produced once a day by scripts/code_stats.py (it calls scripts/scripts_stats.py on the same clones) and kept in `data/scripts-stats.json`.
The page generator only reads them. `build` rebuilds the block from a whitelist: an unknown trigger, pin or language is dropped, a number that is not a plain
number becomes zero, and a repository of an ecosystem the document does not declare is ignored. A document that cannot be read gives `read: false` and the tab
says "not verified" instead of showing zeros. Stdlib only.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Mapping

import scripts_stats

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATS_PATH = DATA_DIR / "scripts-stats.json"
MAX_NUMBER = 10 ** 9
DAY = re.compile(r"\d{4}-\d{2}-\d{2}")
NAME = re.compile(r"[A-Za-z0-9._-]{1,100}")
KEY = re.compile(r"[a-z0-9-]{1,40}")
FILE = re.compile(r"[A-Za-z0-9._ -]{1,100}")
STATES = ("ok", "lastknown", "unread")


def _num(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= MAX_NUMBER else 0


def _day(value: object) -> str | None:
    return value if isinstance(value, str) and DAY.fullmatch(value) else None


def _text(value: object, limit: int) -> str:
    return value[:limit] if isinstance(value, str) else ""


def _scripts(raw: object) -> dict | None:
    if not isinstance(raw, Mapping):
        return None
    workflows = []
    for row in (raw.get("wf") if isinstance(raw.get("wf"), list) else [])[: scripts_stats.MAX_WORKFLOWS]:
        if not (isinstance(row, list) and len(row) >= 5 and isinstance(row[0], str) and FILE.fullmatch(row[0])):
            continue
        triggers = [t for t in (row[2] if isinstance(row[2], list) else []) if t in scripts_stats.TRIGGERS]
        runners = [_text(r, 40) for r in (row[4] if isinstance(row[4], list) else []) if isinstance(r, str)][:6]
        workflows.append([row[0], _text(row[1], 80), triggers, _num(row[3]), runners])
    acts = {}
    for key, value in (raw.get("acts") if isinstance(raw.get("acts"), Mapping) else {}).items():
        if isinstance(key, str) and 0 < len(key) <= 140 and isinstance(value, list) and len(value) == 2 and value[1] in scripts_stats.PINS:
            acts[key] = [_num(value[0]), value[1]]
    sc = {}
    for lang, value in (raw.get("sc") if isinstance(raw.get("sc"), Mapping) else {}).items():
        if lang in scripts_stats.LANGS and isinstance(value, list) and len(value) == 2:
            sc[lang] = [_num(value[0]), _num(value[1])]
    return {"wf": workflows, "acts": acts, "sc": sc}


def load(path: Path = STATS_PATH) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def build(doc: object, today: str | None = None) -> dict:
    """The block embedded in the page. `today` (YYYY-MM-DD) gives the age of the figures in days."""
    empty = {"read": False, "day": None, "age": None, "owner": "", "ecos": [], "types": [], "repos": {}}
    if not isinstance(doc, Mapping) or doc.get("schema") != 1 or not isinstance(doc.get("repos"), Mapping):
        return empty
    ecos = [{"key": e["key"], "label": str(e.get("label", e["key"]))[:40]} for e in (doc.get("ecosystems") or [])
            if isinstance(e, Mapping) and isinstance(e.get("key"), str) and KEY.fullmatch(e["key"])]
    types = [t for t in (doc.get("types") or []) if isinstance(t, str) and KEY.fullmatch(t)]
    eco_keys, type_keys = {e["key"] for e in ecos}, set(types)
    repos = {}
    for name, raw in doc["repos"].items():
        if not (isinstance(name, str) and NAME.fullmatch(name) and isinstance(raw, Mapping)):
            continue
        if raw.get("eco") not in eco_keys or raw.get("type") not in type_keys or raw.get("state") not in STATES:
            continue
        record = {"eco": raw["eco"], "type": raw["type"], "state": raw["state"]}
        if raw["state"] != "unread":
            record["scripts"] = _scripts(raw.get("scripts"))
        repos[name] = record
    day = _day(doc.get("day"))
    age = None
    if day and today and DAY.fullmatch(today):
        age = (date.fromisoformat(today) - date.fromisoformat(day)).days
    read = any(r["state"] != "unread" for r in repos.values())
    owner = doc.get("owner") if isinstance(doc.get("owner"), str) and NAME.fullmatch(doc["owner"]) else ""
    return {"read": read, "day": day, "age": age, "owner": owner, "ecos": ecos, "types": types, "repos": repos}
