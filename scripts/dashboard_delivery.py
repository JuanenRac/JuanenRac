#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_delivery.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The delivery pipeline of every repository as the status dashboard shows it: where a release was signed and what the page can prove about it.

  * `signature_state` reads the assets of the latest release: a signature file (.sig, .asc or .minisig) is "present" (the page does not verify it),
    a release without one is "none", no release at all is "norelease" and an answer that could not be read is None (not verified),
  * `manifest_fields` takes the optional fields a manifest may declare (built_on, signature_kind, signed_on, last_build_artifact_url; see
    docs/evidence-schema.json) and keeps only the values of the known lists, so a typo or an address that is not a repository of the owner is dropped,
  * `pipeline_state` derives the state "built on GitHub Actions -> signed locally -> published" from those fields and the real release.

Nothing is invented: a field that is not declared stays empty and the page says "not declared". Stdlib only.
"""
from __future__ import annotations

from typing import Iterable, Mapping

SIGNATURE_SUFFIXES = (".sig", ".sig2", ".asc", ".minisig")
BUILT_ON = ("gha", "local", "unknown")
SIGNATURE_KIND = ("none", "dev", "release")
SIGNED_ON = ("local", "unknown")
ARTIFACT_PREFIX = "https://github.com/JuanenRac/"
PIPELINE_STATES = ("undeclared", "built", "signed", "published", "release_only")
DEFAULT_ALERT = {"enabled": False, "after_days": 14}


def signature_state(has_release: bool | None, assets: Iterable[str] | None) -> str | None:
    """'present' | 'none' | 'norelease' | None (could not be read). `assets` is None when the answer did not include them."""
    if has_release is None:
        return None
    if not has_release:
        return "norelease"
    if assets is None:
        return None
    for name in assets:
        if isinstance(name, str) and name.lower().endswith(SIGNATURE_SUFFIXES):
            return "present"
    return "none"


def _pick(value: object, allowed: tuple[str, ...]) -> str:
    return value if isinstance(value, str) and value in allowed else ""


def manifest_fields(raw: object) -> dict[str, str]:
    """{"builtOn", "sigKind", "signedOn", "artifact"}: each one is the declared value or the empty text (not declared)."""
    data = raw if isinstance(raw, Mapping) else {}
    artifact = data.get("last_build_artifact_url")
    if not (isinstance(artifact, str) and artifact.startswith(ARTIFACT_PREFIX) and len(artifact) <= 300 and not any(c in artifact for c in ' "<>\\\r\n\t')):
        artifact = ""
    return {
        "builtOn": _pick(data.get("built_on"), BUILT_ON),
        "sigKind": _pick(data.get("signature_kind"), SIGNATURE_KIND),
        "signedOn": _pick(data.get("signed_on"), SIGNED_ON),
        "artifact": artifact,
    }


def pipeline_state(fields: Mapping[str, str], has_release: bool | None) -> str:
    """The furthest stage the repository proves: published (a release exists and a build or a signature is declared), signed (signed locally with a dev or
    release key), built (built on GitHub Actions), release_only (a release but nothing declared about how it was made) or undeclared."""
    built = fields.get("builtOn") == "gha"
    signed = fields.get("signedOn") == "local" and fields.get("sigKind") in ("dev", "release")
    if has_release and (built or signed):
        return "published"
    if signed:
        return "signed"
    if built:
        return "built"
    return "release_only" if has_release else "undeclared"


def parse_alert(raw: object) -> tuple[dict, list[str]]:
    """The optional alert 'a green build without a signed release for more than N days' (off by default): (config, problems).
    `after_hours` (optional, from 1 to 87600) replaces `after_days` as the threshold when it is present."""
    config = dict(DEFAULT_ALERT)
    if raw is None:
        return config, []
    if not isinstance(raw, Mapping):
        return config, ["signature_alert: needs an object with enabled and after_days"]
    problems: list[str] = []
    if "enabled" in raw:
        if isinstance(raw["enabled"], bool):
            config["enabled"] = raw["enabled"]
        else:
            problems.append("signature_alert.enabled: needs true or false")
    if "after_hours" in raw:
        value = raw["after_hours"]
        if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 87600:
            config["after_hours"] = value
        else:
            problems.append("signature_alert.after_hours: needs an integer number of hours from 1")
    if "after_days" in raw:
        value = raw["after_days"]
        if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 3650:
            config["after_days"] = value
        else:
            problems.append("signature_alert.after_days: needs an integer number of days from 1")
    return config, problems
