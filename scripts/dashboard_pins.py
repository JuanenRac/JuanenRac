#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Dependency pins: which version of the shared contracts each repository was last checked against.

Only files the repositories already publish are read, nothing is inferred:

  * A.R.M.O.R.   ARMOR-COMMON/registry/contract_pins.json (consumer -> version) against the version of ARMOR-COMMON/armor.project.json.
  * URTC         tools/urtc_common.lock.json of every URTC repository that has one (its ``urtc_common_version``) against urtc.project.json of URTC-COMMON.
  * HYDRA-UMC    has no machine readable source of pins, so it is listed as "no source" and never guessed.

A pin that cannot be read is "unknown", never "current". Stdlib only; the page makes no request (the result is embedded in it).
"""
from __future__ import annotations

import base64
import json
import re
from typing import Callable, Mapping

# fetch(path) -> (status, payload) with status "ok" | "absent" | "error"; payload is the decoded JSON of the "contents" API answer for "ok".
Fetch = Callable[[str], "tuple[str, object]"]

STATES = ("current", "behind", "ahead", "unknown")
ARMOR_SOURCE = ("ARMOR-COMMON", "registry/contract_pins.json", "armor.project.json")
URTC_SOURCE = ("URTC-COMMON", "urtc.project.json")
URTC_LOCK_PATH = "tools/urtc_common.lock.json"
_VERSION = re.compile(r"^\d+(\.\d+){1,3}$")


def parse_version(text: object) -> "tuple[int, ...] | None":
    if not isinstance(text, str) or not _VERSION.match(text.strip()):
        return None
    return tuple(int(part) for part in text.strip().split("."))


def compare(pin: object, current: object) -> str:
    """current / behind / ahead / unknown; missing trailing components count as zero (0.8.1 equals 0.8.1.0)."""
    a, b = parse_version(pin), parse_version(current)
    if a is None or b is None:
        return "unknown"
    size = max(len(a), len(b))
    a, b = a + (0,) * (size - len(a)), b + (0,) * (size - len(b))
    return "current" if a == b else ("behind" if a < b else "ahead")


def _json_file(fetch: Fetch, owner: str, repo: str, path: str) -> "tuple[str, object]":
    status, payload = fetch(f"/repos/{owner}/{repo}/contents/{path}")
    if status != "ok":
        return status, None
    try:
        raw = base64.b64decode(str(payload.get("content", "")).encode("ascii"), validate=False) if isinstance(payload, Mapping) else b""
        return "ok", json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError):
        return "error", None


def _rows(pins: Mapping[str, object], current: object) -> list[dict]:
    rows = [{"repo": name, "pin": pins[name] if parse_version(pins[name]) else None, "state": compare(pins[name], current)} for name in sorted(pins)]
    order = {"behind": 0, "unknown": 1, "ahead": 2, "current": 3}
    return sorted(rows, key=lambda r: (order[r["state"]], r["repo"]))


def read_armor(fetch: Fetch, owner: str) -> dict:
    repo, pins_path, manifest_path = ARMOR_SOURCE
    s1, manifest = _json_file(fetch, owner, repo, manifest_path)
    s2, pins = _json_file(fetch, owner, repo, pins_path)
    current = manifest.get("version") if s1 == "ok" and isinstance(manifest, Mapping) else None
    consumers = pins.get("consumers") if s2 == "ok" and isinstance(pins, Mapping) else None
    if not parse_version(current) or not isinstance(consumers, Mapping):
        return {"source": "contract_pins", "read": False, "current": None, "rows": []}
    return {"source": "contract_pins", "read": True, "current": current, "rows": _rows({str(k): v for k, v in consumers.items()}, current)}


def read_urtc(fetch: Fetch, owner: str, repos: "list[str]") -> dict:
    repo, manifest_path = URTC_SOURCE
    status, manifest = _json_file(fetch, owner, repo, manifest_path)
    current = manifest.get("version") if status == "ok" and isinstance(manifest, Mapping) else None
    if not parse_version(current):
        return {"source": "lock_files", "read": False, "current": None, "rows": []}
    pins: dict[str, object] = {}
    failed = False
    for name in sorted(repos):
        if name == repo:
            continue
        state, lock = _json_file(fetch, owner, name, URTC_LOCK_PATH)
        if state == "ok" and isinstance(lock, Mapping) and "urtc_common_version" in lock:
            pins[name] = lock["urtc_common_version"]
        elif state == "error":
            failed = True
    return {"source": "lock_files", "read": True, "partial": failed, "current": current, "rows": _rows(pins, current)}


def read_all(owner: str, ecosystem_of: Mapping[str, str], fetch: Fetch) -> dict:
    """The pins of every ecosystem that publishes them. ``fetch`` is the REST helper of the dashboard (dashboard_signatures.LiveFetch.rest)."""
    urtc_repos = [n for n, eco in ecosystem_of.items() if eco == "urtc"]
    return {
        "armor": read_armor(fetch, owner),
        "urtc": read_urtc(fetch, owner, urtc_repos),
        "hydra-umc": {"source": "none", "read": True, "current": None, "rows": []},
    }


def build(doc: "Mapping | None") -> dict:
    """What the page embeds (``DATA.pins``): the pins read, or an empty object when nothing could be read."""
    if not isinstance(doc, Mapping):
        return {"eco": {}}
    eco = {}
    for key, value in doc.items():
        if not isinstance(value, Mapping):
            continue
        rows = [r for r in value.get("rows", []) if isinstance(r, Mapping) and r.get("state") in STATES]
        eco[key] = {"source": value.get("source"), "read": bool(value.get("read")), "current": value.get("current"), "partial": bool(value.get("partial")), "rows": rows}
    return {"eco": eco}
