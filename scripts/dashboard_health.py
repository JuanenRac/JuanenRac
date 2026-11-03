#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_health.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Health of the ecosystem as the status dashboard shows it: the thresholds, the alerts and the last good build.

  * `load_config` reads dashboard-config.json (the thresholds of the activity badges and of the inactivity alert) and falls back, with a
    message, to the defaults when the file is missing or wrong, so a typo can never blank the page,
  * `static_alerts` turns what the generator already knows (red CI, a manifest that cannot be read, a version that did not resolve) into alerts
    with the repository, the reason and a link; the alert for days without activity depends on today's date, so the browser raises it,
  * `completeness` says why the picture is not complete (a read of the CI or the releases failed); an incomplete picture is never shown as healthy,
  * `fetch_last_good_build` and `merge_build_info` keep the time and the link of the last good build without the page changing on every run.

A value that cannot be read is None or absent and the page says "not verified". Stdlib only, the network is injectable.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

CONFIG_PATH = Path(__file__).resolve().parent.parent / "dashboard-config.json"
DEFAULT_CONFIG: dict = {
    "activity_days": {"green_max": 14, "amber_max": 30},
    "release_days": {"green_max": 90, "amber_max": 180},
    "alert_after_days": 30,
    "scaffolding_months": 6,
}
MANIFEST_KINDS = ("invalid_manifest", "unlisted_manifest", "unknown_maturity", "unknown_evidence", "catalog_missing")
BUILD_BEGIN, BUILD_END = "<!--build-info-->", "<!--/build-info-->"
# The time of the generation and how long it took change on every run too, so they are kept stable the same way.
GEN_BEGIN, GEN_END = "<!--gen-info-->", "<!--/gen-info-->"


def _ordered(block: object, default: Mapping[str, int]) -> dict[str, int] | None:
    """{"green_max": a, "amber_max": b} with 0 <= a <= b <= 3650, or None."""
    if not isinstance(block, Mapping):
        return None
    green, amber = block.get("green_max"), block.get("amber_max")
    if not all(isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 3650 for v in (green, amber)) or green > amber:
        return None
    return {"green_max": green, "amber_max": amber}


def parse_config(raw: object) -> tuple[dict, list[str]]:
    """(config, problems): every part that is wrong is replaced by its default and named in the problems."""
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    problems: list[str] = []
    if not isinstance(raw, Mapping):
        return config, ["the file is not a JSON object"]
    for key in ("activity_days", "release_days"):
        if key in raw:
            good = _ordered(raw[key], DEFAULT_CONFIG[key])
            if good is None:
                problems.append(f"{key}: needs integers green_max <= amber_max (days)")
            else:
                config[key] = good
    if "alert_after_days" in raw:
        value = raw["alert_after_days"]
        if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 3650:
            config["alert_after_days"] = value
        else:
            problems.append("alert_after_days: needs an integer number of days from 1")
    if "scaffolding_months" in raw:
        value = raw["scaffolding_months"]
        if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 120:
            config["scaffolding_months"] = value
        else:
            problems.append("scaffolding_months: needs an integer number of months from 1 to 120")
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return json.loads(json.dumps(DEFAULT_CONFIG)), [f"{path.name}: {exc}"]
    config, problems = parse_config(raw)
    return config, [f"{path.name}: {p}" for p in problems]


def classify(days: int | None, green_max: int, amber_max: int) -> str:
    """'good' | 'warn' | 'bad', or 'unknown' when the number of days is not known. The browser applies the same rule."""
    if days is None:
        return "unknown"
    return "good" if days <= green_max else "warn" if days <= amber_max else "bad"


def days_between(iso: str | None, now_iso: str) -> int | None:
    """Whole days from `iso` to `now_iso` (both ISO 8601), None when either is not a date."""
    from datetime import datetime, timezone

    def parse(text: str | None):
        match = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2}))?", text or "")
        if not match:
            return None
        year, month, day, hour, minute = (int(g) if g else 0 for g in match.groups())
        try:
            return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
        except ValueError:
            return None
    a, b = parse(iso), parse(now_iso)
    return None if a is None or b is None else max(0, (b - a).days)


def last_activity(commit_date: str | None, release_date: str | None) -> str | None:
    """The newer of the last commit and the last release (ISO 8601 text compares correctly), None when neither is known."""
    known = [d for d in (commit_date, release_date) if d]
    return max(known) if known else None


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Alert:
    kind: str      # ci | manifest | version
    repo: str
    detail: str    # the reason as the sources give it (English), may be empty
    url: str       # where to look at it


def static_alerts(*, activity: Mapping[str, object], ecosystem_by_name: Mapping[str, str], issues: Iterable[object],
                  unresolved: Iterable[tuple[str, str]], repo_url: str = "https://github.com/JuanenRac/") -> list[Alert]:
    """The alerts that do not depend on today's date, in a fixed order: red CI, manifests, versions."""
    out: list[Alert] = []
    for name in sorted(activity, key=str.casefold):
        if name in ecosystem_by_name and getattr(activity[name], "ci", "") == "failure":
            out.append(Alert("ci", name, "", f"{repo_url}{name}/actions"))
    for issue in issues:
        kind, repo = getattr(issue, "kind", ""), getattr(issue, "repo", "")
        if kind in MANIFEST_KINDS and repo:
            out.append(Alert("manifest", repo, str(getattr(issue, "detail", "")), f"{repo_url}{repo}"))
    for name, reason in unresolved:
        out.append(Alert("version", name, str(reason or ""), f"{repo_url}{name}"))
    return out


def completeness(*, total: int, activity: Mapping[str, object], ecosystem_by_name: Mapping[str, str], issues: Iterable[object]) -> list[str]:
    """Why the picture is not complete, as codes: nothing_listed | activity_unread | activity_partial | api. Empty = complete."""
    reasons: list[str] = []
    if total == 0:
        reasons.append("nothing_listed")
    if not activity:
        reasons.append("activity_unread")
    elif any(name not in activity for name in ecosystem_by_name):
        reasons.append("activity_partial")
    if any(getattr(issue, "kind", "") == "api" for issue in issues):
        reasons.append("api")
    return reasons


# ---------------------------------------------------------------------------
# Last good build
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BuildInfo:
    url: str
    finished: str   # ISO 8601, as GitHub writes it


Getter = Callable[[str], "dict | list | None"]


def fetch_last_good_build(repository: str, workflow: str, get: Getter) -> BuildInfo | None:
    """The latest successful run of the workflow on main (the run that is going on is not a success yet, so this is the previous one), None if unknown."""
    answer = get(f"https://api.github.com/repos/{repository}/actions/workflows/{workflow}/runs?status=success&branch=main&per_page=1")
    try:
        run = answer["workflow_runs"][0]
        url, finished = run["html_url"], run["updated_at"]
    except (TypeError, KeyError, IndexError):
        return None
    if not (isinstance(url, str) and url.startswith("https://github.com/") and isinstance(finished, str) and re.match(r"^\d{4}-\d{2}-\d{2}T", finished)):
        return None
    return BuildInfo(url, finished)


def _region(text: str) -> tuple[int, int] | None:
    a, b = text.find(BUILD_BEGIN), text.find(BUILD_END)
    return (a, b + len(BUILD_END)) if 0 <= a < b else None


def strip_build_info(text: str) -> str:
    """The page without the regions that move on every run (the last good build and the generation figures)."""
    span = _region(text)
    if span is not None:
        text = text[:span[0]] + text[span[1]:]
    a, b = text.find(GEN_BEGIN), text.find(GEN_END)
    if 0 <= a < b:
        text = text[:a] + text[b + len(GEN_END):]
    return text


def merge_build_info(new: str, old: str | None) -> str:
    """The page to write. The time of the last good build moves every run, and writing it each time would commit the page twice an hour even
    when nothing else changed; so when the rest of the page is the same the published page is kept as it is, and when the new run could not read
    the build (the region is marked data-state="unknown") the old region is carried over instead of a gap."""
    if not old:
        return new
    old_span, new_span = _region(old), _region(new)
    if old_span and new_span and 'data-state="unknown"' in new[new_span[0]:new_span[1]] and 'data-state="unknown"' not in old[old_span[0]:old_span[1]]:
        new = new[:new_span[0]] + old[old_span[0]:old_span[1]] + new[new_span[1]:]
    return old if strip_build_info(new) == strip_build_info(old) else new
