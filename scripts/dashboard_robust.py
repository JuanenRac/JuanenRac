#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_robust.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Robustness of the status dashboard: the manifest health, the figures of the generation and the last known data.

  * `manifest_health` is "valid manifests / repositories", counted from the same problems the Errors / unknown indicator counts,
  * `generation_html` writes the figures of the generation (when, how long, what was resolved out of what was attempted) between two comments,
    the region `dashboard_health.merge_build_info` keeps stable so the page does not change on every run,
  * `activity_from_page` and `previous_asof` read the CI, release and commit data of the page that is already published, so that when GitHub cannot be
    read the dashboard shows the last known version, marked as such and never as current,
  * `previous_ecosystem_counts` says how many repositories each ecosystem had on that page.

Nothing here reads the network. A figure that is not known is None and the page says "not verified". Stdlib only.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterable, Mapping

import dashboard_health
import dashboard_integrity
from dashboard_charts import Activity, Commit, esc

# A manifest the dashboard lists but whose maturity or evidence is not a known value, and a manifest it cannot list.
UNLISTED_KINDS = ("invalid_manifest", "unlisted_manifest")
_DATA_RE = re.compile(r'<script type="application/json" id="dashboard-data">(.*?)</script>', re.S)
_ASOF_RE = re.compile(r'data-activity-asof="(\d{4}-\d{2}-\d{2})"')


def manifest_health(listed: Iterable[str], raw_manifests: "Mapping[str, object] | None", issues: Iterable[object]) -> dict:
    """{"valid", "repos", "percent", "unread"}: valid manifests over repositories. A repository is valid when its manifest was read and declares a known
    maturity and evidence; one whose manifest cannot be read, or that has a manifest the dashboard did not list, counts in `repos` but not in `valid`.
    `percent` is None when there is no repository at all or when no manifest could be read (nothing was verified, so no percentage is claimed)."""
    names = list(listed)
    unlisted = {getattr(i, "repo", "") for i in issues if getattr(i, "kind", "") in UNLISTED_KINDS and getattr(i, "repo", "")} - set(names)
    raw = raw_manifests or {}
    valid = 0
    read = 0
    for name in names:
        data = getattr(raw.get(name), "data", raw.get(name))
        if not isinstance(data, dict):
            continue
        read += 1
        if data.get("maturity") in dashboard_integrity.MATURITIES and data.get("evidence") in dashboard_integrity.EVIDENCES:
            valid += 1
    repos = len(names) + len(unlisted)
    unread = bool(names) and read == 0
    return {"valid": valid, "repos": repos, "unread": unread,
            "percent": None if (not repos or unread) else round(valid * 100 / repos, 1)}


def percent_text(health: Mapping[str, object]) -> str:
    value = health.get("percent")
    return "–" if value is None else f"{value:g}%"


@dataclass(frozen=True)
class Generation:
    """What the generator did in this run. `built` is an ISO 8601 UTC time, `seconds` the duration; each step is (key, answered, attempted)."""
    built: str
    seconds: float
    steps: tuple[tuple[str, int, int], ...]
    asof: str   # the date of the CI, release and commit data (the day they were read, or the one of the last known version)


STEP_KEYS = ("versions", "manifests", "commits", "activity")


def generation_html(gen: "Generation | None", stale: bool = False) -> str:
    """The card of the figures of the generation. Everything between the two comments moves on every run and is ignored when the page is compared."""
    en = _en()
    if gen is None:
        inner = f'<p class="muted" data-i18n="gen_unknown" data-testid="gen-unknown">{esc(en["gen_unknown"])}</p>'
    else:
        when = gen.built.replace("T", " ")[:16]
        built = (f'<p data-testid="gen-built" data-i18n-template="gen_built" data-when="{esc(when)}" data-seconds="{gen.seconds:.0f}">'
                 f'{esc(en["gen_built"].replace("{when}", when).replace("{seconds}", format(gen.seconds, ".0f")))}</p>')
        rows = "".join(
            f'<li data-testid="gen-step-{esc(key)}" data-ok="{ok}" data-total="{total}" data-i18n-template="gen_step_{esc(key)}">'
            f'{esc(en["gen_step_" + key].replace("{ok}", str(ok)).replace("{total}", str(total)))}</li>'
            for key, ok, total in gen.steps if key in STEP_KEYS)
        inner = f'{built}<ul class="gen-steps">{rows}</ul>'
    asof = gen.asof if gen is not None else ""
    return (
        '<section class="card card-gen" aria-labelledby="gen-t" data-testid="gen-info">'
        f'<h2 class="card-title" id="gen-t" data-i18n="gen_title">{esc(en["gen_title"])}</h2>'
        f'{dashboard_health.GEN_BEGIN}<div data-activity-asof="{esc(asof)}" data-stale="{1 if stale else 0}">{inner}</div>{dashboard_health.GEN_END}'
        f'<p class="muted" data-i18n="gen_errors_hint">{esc(en["gen_errors_hint"])}</p></section>'
    )


def stale_banner_html(date: str | None) -> str:
    """The notice shown above everything else in the summary when the CI, release and commit data are the last known version."""
    if not date:
        return ""
    en = _en()
    return (f'<p class="stale-banner" role="status" data-testid="stale-banner" data-i18n-template="stale_banner" data-date="{esc(date)}">'
            f'<span class="stale-glyph" aria-hidden="true">▲</span> {esc(en["stale_banner"].replace("{date}", date))}</p>')


def _en() -> dict:
    import dashboard_robust_texts
    return dashboard_robust_texts.TEXTS["en"]


def _page_data(html: str | None) -> dict | None:
    match = _DATA_RE.search(html or "")
    if not match:
        return None
    try:
        data = json.loads(match.group(1))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def activity_from_page(html: str | None) -> dict[str, Activity]:
    """The CI, release and commit data of the page that is already published (the data it embeds for its own script). A repository whose data were
    not read there is left out; an unreadable page gives {}."""
    data = _page_data(html)
    repos = data.get("repos") if data else None
    if not isinstance(repos, dict):
        return {}
    out: dict[str, Activity] = {}
    for name, repo in repos.items():
        if not isinstance(repo, dict) or repo.get("known") is not True or not isinstance(name, str):
            continue
        release = repo.get("release") if isinstance(repo.get("release"), dict) else None
        commits = tuple(Commit(str(c[0]), c[1] or None, c[2] or None) for c in (repo.get("commits") or []) if isinstance(c, list) and len(c) == 3)
        ci = repo.get("ci") if repo.get("ci") in ("success", "failure", "pending", "none") else "none"
        out[name] = Activity(
            release_tag=(release.get("tag") or None) if release else None,
            release_date=(release.get("date") or None) if release else None,
            commit_date=repo.get("commitDate") if isinstance(repo.get("commitDate"), str) else None,
            ci=ci, commits=commits,
            signature=repo.get("sig") if repo.get("sig") in ("present", "none", "norelease") else None)
    return out


def previous_asof(html: str | None) -> str | None:
    """The date of the data of the published page, None when it does not say."""
    match = _ASOF_RE.search(html or "")
    if match and match.group(1):
        return match.group(1)
    snap = (_page_data(html) or {}).get("snap")
    date = snap.get("date") if isinstance(snap, dict) else None
    return date if isinstance(date, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", date) else None


def previous_ecosystem_counts(html: str | None) -> dict[str, int]:
    """How many repositories each ecosystem had on the published page."""
    data = _page_data(html)
    repos = data.get("repos") if data else None
    counts: dict[str, int] = {}
    if isinstance(repos, dict):
        for repo in repos.values():
            if isinstance(repo, dict) and isinstance(repo.get("eco"), str):
                counts[repo["eco"]] = counts.get(repo["eco"], 0) + 1
    return counts


def lost_ecosystems(previous: Mapping[str, int], current: Mapping[str, int], failed: Iterable[str]) -> list[str]:
    """The ecosystems whose discovery failed in this run and that had repositories on the published page: publishing now would erase them."""
    return [eco for eco in failed if previous.get(eco, 0) > 0 and current.get(eco, 0) == 0]


__all__ = ["manifest_health", "percent_text", "Generation", "generation_html", "stale_banner_html", "activity_from_page", "previous_asof",
           "previous_ecosystem_counts", "lost_ecosystems"]
