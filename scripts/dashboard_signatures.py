#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_signatures.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Verifies the signature of the latest release of every repository against the PUBLIC key its family pins.

The page is built in a job with a read-only token and no secret. For every repository whose latest release has a signature file (.sig, .sig2, .asc,
.minisig), this module reads the release once (REST, with the SHA-256 that GitHub itself computes for every asset), reads the small signature files, rebuilds
the message the family signs and checks the Ed25519 signature with dashboard_ed25519 (pure Python, no package to install):

  * ARMOR   `<image>.sig` of the 32 bytes of the SHA-256 and `<image>.sig2` of `armor-fw/1|<project>|<board>|<version>|<sha256>` (firmware), and
            `armor-pkg/1|<component>|<version>|<sha256>` for `armor-<component>-<version>.tgz`,
  * URTC    `urtc-rel/1|<file name>|<sha256>` for any asset and `urtc-pkg/1|<app>|<version>|<platform>|<sha256>|<size>` for the packages,
  * HYDRA   `hydra-pc-pkg/1|<project>|<version>|<sha256>` for `<project>-<version>.tgz` (hexadecimal signature) and the signature of the WHOLE file in base64
            made by hydra-sign (the file is downloaded, up to the configured size),

each with the key of the family (only public keys are here; the private ones never leave the owner's computer). The answer for a repository is one of:

  verified      every signature that could be checked is valid for the pinned key and the hash GitHub holds for the file,
  invalid       at least one signature is well formed and does NOT verify (a changed file, another key or another message),
  unverifiable  there are signature files but none could be checked here (unknown family, key, format or message; or a file too large to download),
  None          a read failed: not verified (never reported as a good or a bad signature).

The answer is cached by tag plus a fingerprint of the assets (name, size, update time) in data/delivery-cache.json, so a release is read once.
Stdlib only.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping

import dashboard_ed25519

SIGNATURE_SUFFIXES = (".sig", ".sig2", ".asc", ".minisig")
CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "delivery-cache.json"
CONFIG_PATH = Path(__file__).resolve().parent.parent / "dashboard-config.json"
SCHEMA = 1
KEY_ARMOR = "664478b12a8799ab18970f58e974f14a6d0bf5623f0a22c65c3aaa32997054d2"
KEY_URTC = "4020c46d76c8ebacb64c5c7b9f3e7c62475afeb133d7421591988174e0f5dc90"
KEY_HYDRA = "1228393cae6cb9fba1d98e300446956de2bc1e9c5b59cc58035a65dbcf4f2331"
DEFAULT_CONFIG: dict = {
    "enabled": True,
    "max_asset_bytes": 50 * 1024 * 1024,
    "max_repos_per_run": 40,
    "keys": {"armor": KEY_ARMOR, "urtc": KEY_URTC, "hydra": KEY_HYDRA},
}
SIG_MAX_BYTES = 4096
_HEX_KEY = re.compile(r"^[0-9a-f]{64}$")
_HEX_SIG = re.compile(r"^[0-9a-fA-F]{128}$")
_VERSION = r"\d+\.\d+\.\d+(?:\.\d+)?"
_ARMOR_PACKAGE = re.compile(rf"^armor-([a-z]+)-({_VERSION})\.tgz$")
_ARMOR_FIRMWARE = re.compile(r"^([a-z0-9]+_[a-z0-9_]+)-([a-z0-9][a-z0-9-]*)\.bin$")
_URTC_PACKAGE = re.compile(rf"^([a-z][a-z0-9-]*?)-({_VERSION})-([A-Za-z0-9_.]+(?:-[A-Za-z0-9_.]+)*)\.(?:zip|tar\.gz)$")
_URTC_COMMON = (
    (re.compile(rf"^urtc_common-({_VERSION})-py3-none-any\.whl$"), "py3-none-any"),
    (re.compile(rf"^urtc_common-({_VERSION})\.tar\.gz$"), "source"),
    (re.compile(r"^urtc_can_ids\.h$"), "c-header"),
)
_HYDRA_PACKAGE = re.compile(rf"^([A-Za-z][A-Za-z0-9-]{{0,99}})-({_VERSION})\.tgz$")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def check_config(raw: object) -> tuple[dict, list[str]]:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["signatures: not an object"]
    if "enabled" in raw:
        if isinstance(raw["enabled"], bool):
            config["enabled"] = raw["enabled"]
        else:
            problems.append("signatures.enabled: needs true or false")
    for key, low, high in (("max_asset_bytes", 1024, 500 * 1024 * 1024), ("max_repos_per_run", 1, 500)):
        if key in raw:
            value = raw[key]
            if isinstance(value, int) and not isinstance(value, bool) and low <= value <= high:
                config[key] = value
            else:
                problems.append(f"signatures.{key}: needs an integer from {low} to {high}")
    keys = raw.get("keys")
    if keys is not None:
        if isinstance(keys, Mapping):
            for family, value in keys.items():
                if family in config["keys"] and isinstance(value, str) and _HEX_KEY.match(value):
                    config["keys"][family] = value
                else:
                    problems.append(f"signatures.keys.{family}: needs a known family and 64 lowercase hexadecimal digits (a public key)")
        else:
            problems.append("signatures.keys: needs an object {family: public key}")
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return check_config(None)
    except (OSError, ValueError) as exc:
        return check_config(None)[0], [f"{path.name} could not be read for the signatures ({exc})"]
    return check_config(raw.get("signatures") if isinstance(raw, Mapping) else None)


def family_of(repository: str) -> str | None:
    """'armor' | 'urtc' | 'hydra' by the name of the repository, None for any other family (no key is pinned for it)."""
    if repository.startswith("ARMOR-"):
        return "armor"
    if repository == "URTC" or repository.startswith("URTC-"):
        return "urtc"
    if repository == "HYDRA-UMC" or repository.startswith("HYDRA-UMC-"):
        return "hydra"
    return None


# ---------------------------------------------------------------------------
# Network (replaceable in the tests)
# ---------------------------------------------------------------------------

class ReadError(Exception):
    """A read that failed or exceeded its limit: the answer for that repository is 'not verified', never a verdict on the signature."""


class LiveFetch:
    """REST with the read-only token of the workflow; downloads of release assets WITHOUT the token (they redirect to another host)."""

    def __init__(self, owner: str, token: str, timeout: float = 30) -> None:
        self.owner, self.token, self.timeout = owner, token, timeout

    def rest(self, path: str) -> tuple[str, object]:
        headers = {"User-Agent": "JuanenRac-dashboard-signatures", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        outcome: tuple[str, object] = ("error", "no attempt")
        for _attempt in range(2):
            try:
                with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=headers), timeout=self.timeout) as response:
                    return "ok", json.loads(response.read(8_000_000).decode("utf-8", errors="replace"))
            except urllib.error.HTTPError as exc:
                if exc.code in (404, 410):
                    return "absent", None
                outcome = ("error", f"HTTP {exc.code}")
                if exc.code in (401, 403):
                    return outcome
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                outcome = ("error", f"lookup failed: {exc}")
        return outcome

    def download(self, url: str, limit: int) -> bytes:
        if not url.startswith(f"https://github.com/{self.owner}/"):
            raise ReadError("address outside the repositories of the owner")
        request = urllib.request.Request(url, headers={"User-Agent": "JuanenRac-dashboard-signatures"})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = response.read(limit + 1)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ReadError(str(exc)) from exc
        if len(data) > limit:
            raise ReadError("larger than the limit")
        return data


# ---------------------------------------------------------------------------
# Messages each family signs
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Asset:
    name: str
    size: int
    sha256: str | None      # the digest GitHub holds for the file, None when the API did not give one
    url: str


def tag_version(tag: str | None) -> str | None:
    match = re.match(rf"^v?({_VERSION})$", tag or "")
    return match.group(1) if match else None


def messages(family: str, base: Asset, tag: str | None, sha: str, suffix: str) -> list[tuple[str, bytes]]:
    """[(scheme, message)] this family could have signed for the file `base` whose SHA-256 is `sha`; `suffix` is the extension of the signature file (.sig, .sig2)."""
    name, found = base.name, []
    versions = [v for v in (tag_version(tag),) if v]
    if family == "armor":
        match = _ARMOR_PACKAGE.match(name)
        if match and suffix == ".sig":
            found.append(("armor-pkg/1", f"armor-pkg/1|{match.group(1)}|{match.group(2)}|{sha}".encode()))
        match = _ARMOR_FIRMWARE.match(name)
        if match and suffix == ".sig":
            found.append(("armor-fw/1 (hash)", bytes.fromhex(sha)))
        if match and suffix == ".sig2":
            for version in versions:
                found.append(("armor-fw/1", f"armor-fw/1|{match.group(1)}|{match.group(2)}|{version}|{sha}".encode()))
    elif family == "urtc" and suffix == ".sig":
        found.append(("urtc-rel/1", f"urtc-rel/1|{name}|{sha}".encode()))
        match = _URTC_PACKAGE.match(name)
        if match:
            found.append(("urtc-pkg/1", f"urtc-pkg/1|{match.group(1)}|{match.group(2)}|{match.group(3)}|{sha}|{base.size}".encode()))
        for pattern, kind in _URTC_COMMON:
            match = pattern.match(name)
            if match:
                version = match.group(1) if match.groups() else (versions[0] if versions else "")
                if version:
                    found.append(("urtc-pkg/1", f"urtc-pkg/1|urtc-common|{version}|{kind}|{sha}|{base.size}".encode()))
    elif family == "hydra" and suffix == ".sig":
        match = _HYDRA_PACKAGE.match(name)
        if match:
            found.append(("hydra-pc-pkg/1", f"hydra-pc-pkg/1|{match.group(1)}|{match.group(2)}|{sha}".encode()))
    return found


def _sha_of(base: Asset, assets: Mapping[str, Asset], fetch, config: Mapping) -> tuple[str | None, bool]:
    """(sha256, from_sidecar). GitHub's digest first; else the file itself when it is small enough; else the published .sha256 (only the hash is then proven)."""
    if base.sha256:
        return base.sha256, False
    if base.size <= config["max_asset_bytes"]:
        return hashlib.sha256(fetch.download(base.url, config["max_asset_bytes"])).hexdigest(), False
    sidecar = assets.get(base.name + ".sha256")
    if sidecar is None:
        return None, True
    match = re.match(r"^([0-9a-fA-F]{64})(?:\s|$)", fetch.download(sidecar.url, SIG_MAX_BYTES).decode("ascii", errors="replace").strip())
    return (match.group(1).lower() if match else None), True


def check_one(family: str | None, repository: str, sig: Asset, assets: Mapping[str, Asset], tag: str | None, fetch, config: Mapping) -> dict:
    """One signature file -> {"r": "ok" | "bad" | "unk", "scheme": ..., "why": ..., "ho": bool}. Raises ReadError when a needed read fails."""
    suffix = next((s for s in SIGNATURE_SUFFIXES if sig.name.lower().endswith(s)), "")
    if suffix not in (".sig", ".sig2") or family is None:
        return {"r": "unk", "why": "format" if suffix not in (".sig", ".sig2") else "family"}
    base = assets.get(sig.name[: -len(suffix)])
    if base is None:
        return {"r": "unk", "why": "nofile"}
    key = bytes.fromhex(config["keys"][family])
    raw = fetch.download(sig.url, SIG_MAX_BYTES).decode("ascii", errors="replace").strip()
    if _HEX_SIG.match(raw):
        signature = bytes.fromhex(raw)
        sha, sidecar = _sha_of(base, assets, fetch, config)
        if sha is None:
            return {"r": "unk", "why": "toobig"}
        options = messages(family, base, tag, sha, suffix)
        if not options:
            return {"r": "unk", "why": "scheme"}
        for scheme, message in options:
            if dashboard_ed25519.verify(key, message, signature):
                return {"r": "ok", "scheme": scheme, "ho": sidecar}
        return {"r": "bad", "why": "mismatch"}
    try:
        signature = base64.b64decode(raw, validate=True)
    except ValueError:
        signature = b""
    if len(signature) == 64 and family == "hydra":
        if base.size > config["max_asset_bytes"]:
            return {"r": "unk", "why": "toobig"}
        data = fetch.download(base.url, config["max_asset_bytes"])
        if base.sha256 and hashlib.sha256(data).hexdigest() != base.sha256:
            raise ReadError("the downloaded file does not match the digest of GitHub")
        if dashboard_ed25519.verify(key, data, signature):
            return {"r": "ok", "scheme": "hydra-sign", "ho": False}
        return {"r": "bad", "why": "mismatch"}
    return {"r": "unk", "why": "format"}


def aggregate(results: Iterable[Mapping]) -> dict:
    """The answer for one repository: {"s": verified | invalid | unverifiable, "ok", "bad", "unk", "sch": [schemes], "why": [reasons], "ho": n}."""
    rows = list(results)
    ok = [r for r in rows if r["r"] == "ok"]
    bad = [r for r in rows if r["r"] == "bad"]
    unk = [r for r in rows if r["r"] == "unk"]
    state = "invalid" if bad else "verified" if ok else "unverifiable"
    return {"s": state, "ok": len(ok), "bad": len(bad), "unk": len(unk), "sch": sorted({r["scheme"] for r in ok}),
            "why": sorted({r["why"] for r in bad + unk if r.get("why")}), "ho": sum(1 for r in ok if r.get("ho"))}


def verify_release(family: str | None, repository: str, release: Mapping, fetch, config: Mapping) -> dict | None:
    """The answer for the release (a `releases/latest` object of the REST API), or None when something that was needed could not be read."""
    assets: dict[str, Asset] = {}
    for item in release.get("assets") or []:
        if not isinstance(item, Mapping) or not isinstance(item.get("name"), str):
            continue
        digest = item.get("digest")
        sha = digest[7:].lower() if isinstance(digest, str) and digest.startswith("sha256:") and _HEX_KEY.match(digest[7:].lower()) else None
        assets[item["name"]] = Asset(item["name"], int(item.get("size") or 0), sha, str(item.get("browser_download_url") or ""))
    sigs = [a for a in assets.values() if a.name.lower().endswith(SIGNATURE_SUFFIXES)]
    if not sigs:
        return None
    try:
        return aggregate(check_one(family, repository, sig, assets, release.get("tag_name"), fetch, config) for sig in sigs)
    except ReadError:
        return None


# ---------------------------------------------------------------------------
# All repositories, with the cache
# ---------------------------------------------------------------------------

def fingerprint(tag: str | None, assets: Iterable[tuple[str, int, str]]) -> str:
    text = (tag or "") + "\n" + "\n".join(f"{n}|{s}|{u}" for n, s, u in sorted(assets))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_cache(path: Path = CACHE_PATH) -> dict:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return raw if isinstance(raw, dict) and raw.get("schema") == SCHEMA and isinstance(raw.get("signatures"), dict) else {}


def save_cache(path: Path, signatures: Mapping, builds: Mapping | None = None) -> bool:
    """Writes data/delivery-cache.json only when its text changes. The builds part is kept as it is when `builds` is None."""
    previous = load_cache(path)
    body = {"schema": SCHEMA, "signatures": dict(signatures), "builds": dict(builds if builds is not None else previous.get("builds") or {})}
    text = json.dumps(body, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)
    return True


def read_all(owner: str, inputs: Mapping[str, tuple[str | None, list[tuple[str, int, str]]]], fetch, config: Mapping, cache: Mapping | None = None
             ) -> tuple[dict[str, dict | None], dict]:
    """`inputs` = {repository: (tag, [(asset name, size, updated)])} of the repositories whose release has a signature file.
    Returns ({repository: answer or None}, signatures cache to save). A release already read with the same tag and assets is not read again;
    a failed read is None (not verified) and is not cached."""
    old = (cache or {}).get("signatures") or {}
    answers: dict[str, dict | None] = {}
    fresh: dict[str, dict] = {}
    calls = 0
    for name in sorted(inputs):
        tag, assets = inputs[name]
        fp = fingerprint(tag, assets)
        known = old.get(name)
        if isinstance(known, Mapping) and known.get("fp") == fp and isinstance(known.get("r"), Mapping):
            answers[name] = dict(known["r"])
            fresh[name] = dict(known)
            continue
        family = family_of(name)
        if family is None or not any(n.lower().endswith((".sig", ".sig2")) for n, _s, _u in assets):
            count = sum(1 for n, _s, _u in assets if n.lower().endswith(SIGNATURE_SUFFIXES))
            answers[name] = {"s": "unverifiable", "ok": 0, "bad": 0, "unk": count, "sch": [], "why": ["family" if family is None else "format"], "ho": 0}
            fresh[name] = {"fp": fp, "r": answers[name]}
            continue
        if calls >= config["max_repos_per_run"]:
            answers[name] = None
            continue
        calls += 1
        status, release = fetch.rest(f"/repos/{owner}/{name}/releases/latest")
        result = verify_release(family, name, release, fetch, config) if status == "ok" and isinstance(release, Mapping) else None
        answers[name] = result
        if result is not None:
            fresh[name] = {"fp": fp, "r": result}
    return answers, fresh


def verify_activity(owner: str, activity: Mapping, token: str, config: Mapping, cache: Mapping | None = None, fetch=None) -> tuple[dict, dict]:
    """`activity` = {repository: Activity}. Returns (the same with `signature` and `sigx` replaced by the verification, signatures cache to save).
    Only the repositories whose latest release has a signature file (`signature == "present"`) are looked at; any other answer is left as it is."""
    import dataclasses
    if not config.get("enabled", True):
        return dict(activity), dict((cache or {}).get("signatures") or {})
    inputs = {name: (act.release_tag, list(act.assets)) for name, act in activity.items() if act.signature == "present"}
    if not inputs:
        return dict(activity), {}
    answers, fresh = read_all(owner, inputs, fetch or LiveFetch(owner, token), config, cache)
    out = dict(activity)
    for name, answer in answers.items():
        if answer is None:
            out[name] = dataclasses.replace(activity[name], signature=None, sigx=None)      # a read failed: not verified, never a verdict
        else:
            out[name] = dataclasses.replace(activity[name], signature=answer["s"], sigx={k: v for k, v in answer.items() if k != "s"})
    return out, fresh
