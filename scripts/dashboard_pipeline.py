#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_pipeline.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The delivery pipeline "built -> signed -> published" of a repository, inferred from what GitHub shows, without waiting for any manifest.

  * built      the latest successful run of a build workflow of the repository (firmware-build.yml, binaries-build.yml, package-build.yml, apk-build.yml, exe-build.yml,
               dist-build.yml, site-build.yml, release-files-build.yml) still has an artifact that has not expired,
  * signed     the signature of the latest release was verified against the key the family pins (see dashboard_signatures),
  * published  the latest release is published (GitHub never reports a draft as the latest) and holds assets.

What a manifest declares (built_on, last_build_artifact_url, signature_kind, signed_on; see docs/evidence-schema.json) is never overwritten: an inferred value is
used only where nothing is declared and is marked as inferred. Only state and times are kept, never who started a run, the branch or a commit title.
Stdlib only.
"""
from __future__ import annotations

import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Iterable, Mapping

BUILD_WORKFLOWS = ("firmware-build.yml", "binaries-build.yml", "package-build.yml", "apk-build.yml", "exe-build.yml", "dist-build.yml", "site-build.yml",
                   "release-files-build.yml")


def _parse(text: object) -> datetime | None:
    if not isinstance(text, str):
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def build_files(workflows: Iterable[str]) -> list[str]:
    """The build workflows a repository has, in the order of BUILD_WORKFLOWS."""
    present = {w.lower() for w in workflows}
    return [w for w in BUILD_WORKFLOWS if w in present]


def read_repo(owner: str, name: str, files: Iterable[str], fetch, now: datetime, cached: Mapping | None) -> tuple[dict | None, bool]:
    """(record, failed). The record is {"wf", "at", "url", "art", "exp"} of the newest successful run among the build workflows, {} when there is none
    (nothing was built), None with failed=True when a read failed. `exp` is the earliest expiry of its artifacts: until then the artifact answer is reused."""
    newest: Mapping | None = None
    newest_wf = ""
    for wf in files:
        status, payload = fetch.rest(f"/repos/{owner}/{name}/actions/workflows/{urllib.parse.quote(wf)}/runs?status=success&per_page=1&exclude_pull_requests=true")
        if status == "absent":
            continue
        if status != "ok" or not isinstance(payload, Mapping):
            return None, True
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs or not isinstance(runs[0], Mapping):
            continue
        run = runs[0]
        if newest is None or str(run.get("updated_at") or "") > str(newest.get("updated_at") or ""):
            newest, newest_wf = run, wf
    if newest is None:
        return {}, False
    at = _parse(newest.get("updated_at"))
    url = str(newest.get("html_url") or "")
    if at is None or not url.startswith(f"https://github.com/{owner}/{name}/actions/runs/"):
        return None, True
    record = {"wf": newest_wf, "at": at.strftime("%Y-%m-%dT%H:%M:%SZ"), "url": url, "art": False, "exp": ""}
    if isinstance(cached, Mapping) and cached.get("url") == url:
        expiry = _parse(cached.get("exp"))
        if cached.get("art") is True and expiry is not None and expiry > now:
            return {**record, "art": True, "exp": cached["exp"]}, False
        if cached.get("art") is False and cached.get("checked") is True:
            return {**record, "checked": True}, False      # a run whose artifacts had already expired or never existed does not get them back
    status, payload = fetch.rest(f"/repos/{owner}/{name}/actions/runs/{newest.get('id')}/artifacts?per_page=30")
    if status != "ok" or not isinstance(payload, Mapping) or not isinstance(payload.get("artifacts"), list):
        return None, True
    live = [a for a in payload["artifacts"] if isinstance(a, Mapping) and a.get("expired") is False and _parse(a.get("expires_at")) is not None]
    if live:
        record["art"] = True
        record["exp"] = min(a["expires_at"] for a in live)
    record["checked"] = True
    return record, False


def read_all(owner: str, workflows: Mapping[str, Iterable[str]], fetch, now: datetime | None = None, cache: Mapping | None = None, workers: int = 6
             ) -> tuple[dict[str, dict | None], dict]:
    """({repository: record | {} | None}, cache). Only repositories with a build workflow are read; a failed read keeps the last record of the cache."""
    now = (now or datetime.now(timezone.utc)).replace(microsecond=0)
    old = (cache or {}).get("builds") or {}
    todo = {name: build_files(files) for name, files in workflows.items()}
    todo = {name: files for name, files in todo.items() if files}

    def one(name: str):
        record, failed = read_repo(owner, name, todo[name], fetch, now, old.get(name))
        if failed:
            return name, (dict(old[name]) if isinstance(old.get(name), Mapping) and old[name] else None)
        return name, record

    out: dict[str, dict | None] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for name, record in pool.map(one, sorted(todo)):
            out[name] = record
    keep = {name: record for name, record in out.items() if record}
    return out, keep


def stages(declared: Mapping[str, str], has_release: bool | None, assets: int | None, build: Mapping | None, signature: str | None) -> dict:
    """The stages a repository proves, from the manifest (declared) and from GitHub (inferred), and the furthest one.

    {"state": undeclared | release_only | built | signed | published, "inferred": bool (the state needs an inferred stage), "built": declared | inferred | None,
     "signed": declared | inferred | None, "published": bool | None}"""
    built_declared = declared.get("builtOn") == "gha"
    signed_declared = declared.get("signedOn") == "local" and declared.get("sigKind") in ("dev", "release")
    built_inferred = bool(build and build.get("art"))
    signed_inferred = signature == "verified"
    built = "declared" if built_declared else "inferred" if built_inferred else None
    signed = "declared" if signed_declared else "inferred" if signed_inferred else None
    published = None if has_release is None else bool(has_release and (assets is None or assets > 0))

    def state(use_built: bool, use_signed: bool) -> str:
        if published and (use_built or use_signed):
            return "published"
        if use_signed:
            return "signed"
        if use_built:
            return "built"
        return "release_only" if has_release else "undeclared"

    final = state(built is not None, signed is not None)
    declared_only = state(built == "declared", signed == "declared")
    return {"state": final, "inferred": final != declared_only, "built": built, "signed": signed, "published": published}
