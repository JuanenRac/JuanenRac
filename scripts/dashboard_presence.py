#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_presence.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Presence of a signature and of a build attestation on the latest release of every repository.

This module only says whether the pieces are THERE; it does not check any key or any proof (dashboard_signatures does the first for the families with a
pinned key, and the owner's local monitor does the rest).

  * Signature   the release files of the latest release (the assets that are not themselves a sidecar: .bin, .tgz, .zip, .apk, ...) each have a signature file
                next to them (`<file>.sig`, `.sig2`, `.imgsig`, `.asc` or `.minisig`). Decided from the names of the assets, with no request.
  * Attestation GitHub keeps the build provenance made by actions/attest-build-provenance and returns it for the SHA-256 digest of the file, from
                /repos/{owner}/{repo}/attestations/{digest}. Only its existence is read. A few files per release are asked, inside a budget of requests.

Each answer is one of: present (all), partial (some), absent (none), na (the repository has no release files) or unknown (it could not be read: no release data,
no digest, a refusal of the token or the budget ran out). unknown is never shown as absent. The answer is cached by tag plus a fingerprint of the assets in
data/delivery-cache.json (key "presence"); an attestation that is not present is asked again after `recheck_days`. Stdlib only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, Mapping

import dashboard_signatures as signatures

STATES = ("present", "partial", "absent", "na", "unknown")
SIGNATURE_SUFFIXES = (".sig", ".sig2", ".imgsig", ".asc", ".minisig")
SIDECAR_SUFFIXES = SIGNATURE_SUFFIXES + (".sha256", ".sha256sum", ".sha512", ".hdr2")
CONFIG_PATH = Path(__file__).resolve().parent.parent / "dashboard-config.json"
DEFAULT_CONFIG: dict = {
    "enabled": True,
    "attestations": True,
    "max_repos_per_run": 30,
    "api_budget": 120,
    "attestation_files_per_release": 3,
    "recheck_days": 3,
    "release_extensions": [".bin", ".tgz", ".tar.gz", ".gz", ".xz", ".zip", ".7z", ".apk", ".aab", ".whl", ".exe", ".msi", ".deb", ".img", ".jar"],
}
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def check_config(raw: object) -> tuple[dict, list[str]]:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["presence: not an object"]
    for key in ("enabled", "attestations"):
        if key in raw:
            if isinstance(raw[key], bool):
                config[key] = raw[key]
            else:
                problems.append(f"presence.{key}: needs true or false")
    for key, low, high in (("max_repos_per_run", 1, 500), ("api_budget", 0, 2000), ("attestation_files_per_release", 1, 10), ("recheck_days", 0, 90)):
        if key in raw:
            value = raw[key]
            if isinstance(value, int) and not isinstance(value, bool) and low <= value <= high:
                config[key] = value
            else:
                problems.append(f"presence.{key}: needs an integer from {low} to {high}")
    if "release_extensions" in raw:
        value = raw["release_extensions"]
        if isinstance(value, list) and value and all(isinstance(v, str) and re.match(r"^\.[a-z0-9.]{1,12}$", v) for v in value):
            config["release_extensions"] = list(value)
        else:
            problems.append("presence.release_extensions: needs a non-empty list of extensions such as \".zip\"")
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return check_config(None)
    except (OSError, ValueError) as exc:
        return check_config(None)[0], [f"{path.name} could not be read for the presence of signatures ({exc})"]
    return check_config(raw.get("presence") if isinstance(raw, Mapping) else None)


# ---------------------------------------------------------------------------
# Decisions (no network)
# ---------------------------------------------------------------------------

def primaries(names: Iterable[str], extensions: Iterable[str]) -> list[str]:
    """The release files: assets that are not a sidecar and end with one of the release extensions."""
    ext = tuple(e.lower() for e in extensions)
    return sorted(n for n in names if isinstance(n, str) and not n.lower().endswith(SIDECAR_SUFFIXES) and n.lower().endswith(ext))


def _fold(flags: list[bool]) -> str:
    if not flags:
        return "na"
    return "present" if all(flags) else "absent" if not any(flags) else "partial"


def signature_presence(names: Iterable[str], extensions: Iterable[str]) -> dict:
    """{"s": state, "n": release files, "k": files with a signature file, "h": files with a .sha256}."""
    have = set(names)
    files = primaries(have, extensions)
    signed = [any(f + s in have for s in SIGNATURE_SUFFIXES) for f in files]
    hashed = [f + ".sha256" in have for f in files]
    return {"s": _fold(signed), "n": len(files), "k": sum(signed), "h": sum(hashed)}


def attestation_state(found: list[bool | None]) -> str:
    """found = one entry per file asked: True (an attestation exists), False (none) or None (could not be read)."""
    if not found:
        return "unknown"
    yes = sum(1 for f in found if f is True)
    if any(f is None for f in found):
        return "partial" if yes else "unknown"
    return "present" if yes == len(found) else "absent" if yes == 0 else "partial"


def _unknown(sig: dict | None = None) -> dict:
    out = {"sg": "unknown", "n": 0, "k": 0, "h": 0, "at": "unknown", "an": 0, "ak": 0}
    if sig:
        out.update({"sg": sig["s"], "n": sig["n"], "k": sig["k"], "h": sig["h"]})
    return out


def fingerprint(act) -> str:
    return signatures.fingerprint(act.release_tag, act.assets)


# ---------------------------------------------------------------------------
# Network (the same fetcher as the signatures: replaceable in the tests)
# ---------------------------------------------------------------------------

def _digest_map(release: Mapping) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in release.get("assets") or []:
        if isinstance(item, Mapping) and isinstance(item.get("name"), str) and isinstance(item.get("digest"), str) and _DIGEST.match(item["digest"].lower()):
            out[item["name"]] = item["digest"].lower()
    return out


class _Budget:
    def __init__(self, total: int) -> None:
        self.left = total
        self.blocked = False      # the token was refused: no more requests of this kind in this run

    def take(self) -> bool:
        if self.blocked or self.left <= 0:
            return False
        self.left -= 1
        return True


def _attestations_of(owner: str, name: str, files: list[str], per_release: int, fetch, budget: _Budget) -> tuple[list[bool | None], bool]:
    """Returns (one answer per file asked, whether the release itself could be read)."""
    if not budget.take():
        return [], False
    status, release = fetch.rest(f"/repos/{owner}/{name}/releases/latest")
    if status != "ok" or not isinstance(release, Mapping):
        if status == "error" and str(release).startswith(("HTTP 401", "HTTP 403")):
            budget.blocked = True
        return [], False
    digests = _digest_map(release)
    chosen = [f for f in files if f in digests][:per_release]
    found: list[bool | None] = []
    for f in chosen:
        if not budget.take():
            break
        status, body = fetch.rest(f"/repos/{owner}/{name}/attestations/{digests[f]}")
        if status == "ok" and isinstance(body, Mapping):
            found.append(bool(body.get("attestations")))
        elif status == "absent":
            found.append(False)
        else:
            found.append(None)
            if str(body).startswith(("HTTP 401", "HTTP 403")):
                budget.blocked = True
                break
    return found, True


# ---------------------------------------------------------------------------
# All repositories, with the cache
# ---------------------------------------------------------------------------

def _days_between(older: str, newer: str) -> int | None:
    from datetime import date
    try:
        return (date.fromisoformat(newer) - date.fromisoformat(older)).days
    except ValueError:
        return None


def _fresh(entry: object, fp: str, today: str, recheck_days: int) -> dict | None:
    if not isinstance(entry, Mapping) or entry.get("fp") != fp or not isinstance(entry.get("r"), Mapping):
        return None
    result = dict(entry["r"])
    if result.get("at") == "present":
        return result
    on = entry.get("on")
    age = _days_between(on, today) if isinstance(on, str) and _DATE.match(on) else None
    return result if age is not None and 0 <= age < recheck_days else None


def assess(owner: str, activity: Mapping, fetch, config: Mapping, cache: Mapping | None, today: str) -> tuple[dict[str, dict], dict]:
    """`activity` = {repository: Activity} BEFORE the signatures are verified (the state "present"/"none"/"norelease"/None is the one of the assets).
    Returns ({repository: presence}, the "presence" part of the cache to save). `today` is the UTC date of the pass."""
    old = (cache or {}).get("presence") or {}
    result: dict[str, dict] = {}
    fresh: dict[str, dict] = {}
    budget = _Budget(int(config["api_budget"]))
    network = 0
    for name in sorted(activity):
        act = activity[name]
        if act.signature is None:
            result[name] = _unknown()
            continue
        if act.signature == "norelease":
            result[name] = {"sg": "na", "n": 0, "k": 0, "h": 0, "at": "na", "an": 0, "ak": 0}
            continue
        names = [a[0] for a in act.assets]
        files = primaries(names, config["release_extensions"])
        sig = signature_presence(names, config["release_extensions"])
        if not files:
            result[name] = {"sg": "na", "n": 0, "k": 0, "h": 0, "at": "na", "an": 0, "ak": 0}
            continue
        base = _unknown(sig)
        if not config.get("attestations", True):
            result[name] = base
            continue
        fp = fingerprint(act)
        known = _fresh(old.get(name), fp, today, int(config["recheck_days"]))
        if known is not None:
            result[name] = {**base, **{k: known[k] for k in ("at", "an", "ak") if k in known}}
            fresh[name] = old[name]
            continue
        found: list[bool | None] = []
        read = False
        if network < int(config["max_repos_per_run"]) and not budget.blocked and budget.left > 0:
            network += 1
            found, read = _attestations_of(owner, name, files, int(config["attestation_files_per_release"]), fetch, budget)
        state = attestation_state(found) if read else "unknown"
        entry = {**base, "at": state, "an": len(found), "ak": sum(1 for f in found if f is True)}
        result[name] = entry
        if read and state != "unknown":
            fresh[name] = {"fp": fp, "on": today, "r": {"at": entry["at"], "an": entry["an"], "ak": entry["ak"]}}
        elif isinstance(old.get(name), Mapping) and old[name].get("fp") == fp and isinstance(old[name].get("r"), Mapping):
            fresh[name] = old[name]           # a stale answer of the same release is kept for the next pass, never shown as current
    return result, fresh


def summarize(presence: Mapping[str, Mapping], ecosystem_of: Mapping[str, str]) -> dict[str, dict]:
    """{ecosystem: {"repos": with release files, "sg": {state: n}, "at": {state: n}}}; the repositories with na are not counted in "repos"."""
    out: dict[str, dict] = {}
    for name, p in presence.items():
        eco = ecosystem_of.get(name)
        if not eco:
            continue
        row = out.setdefault(eco, {"repos": 0, "sg": {s: 0 for s in STATES}, "at": {s: 0 for s in STATES}})
        if p.get("sg") == "na" and p.get("at") == "na":
            continue
        row["repos"] += 1
        row["sg"][p.get("sg") if p.get("sg") in STATES else "unknown"] += 1
        row["at"][p.get("at") if p.get("at") in STATES else "unknown"] += 1
    return out


def valid(p: object) -> dict | None:
    """The presence record as the page keeps it, or None when it is not a well formed one (used when the last published page is reused)."""
    if not isinstance(p, Mapping):
        return None
    out = {}
    for key in ("sg", "at"):
        if p.get(key) not in STATES:
            return None
        out[key] = p[key]
    for key in ("n", "k", "h", "an", "ak"):
        v = p.get(key, 0)
        out[key] = v if isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 10000 else 0
    return out
