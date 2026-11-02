#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_charts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Data and charts of the status dashboard: plain functions with no network (except fetch_activity, whose transport can be replaced).

  * the progress and the eight status areas of every ecosystem, read from the tables the README already carries
    (scripts/ecosystem_progress.py and scripts/ecosystem_status.py write them from the manifests),
  * the counts of maturity and evidence per ecosystem,
  * the latest release, the latest commit and the CI state of every repository (one GraphQL request for the whole account),
  * SVG charts written on the server: stacked bars, a ring and columns. They carry no translatable text of their own: the labels are
    HTML next to them, and every chart is wrapped with a caption and a data table for screen readers.

A value that is not known is None or absent and the page says "no data"; nothing here invents a figure. Stdlib only.
"""
from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Sequence

AREAS = ("software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production")
ECOSYSTEM_KEYS = ("hydra-umc", "urtc", "armor", "eh3d")
MATURITY_KEYS = ("scaffolding", "functional", "established", "production")
EVIDENCE_KEYS = ("none", "host-test", "simulator", "bench", "field")
CI_KEYS = ("success", "failure", "pending", "none")
LIGHT_CLASS = {"🟢": "good", "🟡": "fair", "🟠": "poor", "🔴": "bad"}
UNKNOWN = "unknown"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


# ---------------------------------------------------------------------------
# Progress and status areas, from the README
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Area:
    light: str          # one of the four lights, as written in the README
    percent: int
    count: int | None   # repositories that meet the area (None when the note could not be read)
    total: int | None   # repositories counted


_STATUS_ROW = re.compile(r"^\|\s*(?P<label>[^|]+?)\s*\|\s*(?P<light>[🟢🟡🟠🔴])\s*\|\s*`[^`]*?(?P<pct>\d+)%`\s*\|\s*(?P<note>.*?)\s*\|\s*$", re.M)
_NOTE_COUNTS = re.compile(r"(\d+) of (?:the )?(\d+)")
_PROGRESS = re.compile(r"`\[[^\]`]*\]\s*(?P<pct>\d+)%`.*?its (?P<count>\d+) repositories", re.S)


def _block(text: str, tag: str, eco: str) -> str:
    match = re.search(rf"<!-- {tag}:{re.escape(eco)} -->(.*?)<!-- /{tag}:{re.escape(eco)} -->", text, re.S)
    return match.group(1) if match else ""


def parse_status(readme: str, ecosystems: Iterable[str] = ECOSYSTEM_KEYS) -> dict[str, dict[str, Area]]:
    """The eight status areas of each ecosystem, in the order of ecosystem_status.AREAS; an ecosystem whose table is not exactly eight rows is left out."""
    out: dict[str, dict[str, Area]] = {}
    for eco in ecosystems:
        rows = list(_STATUS_ROW.finditer(_block(readme, "status", eco)))
        if len(rows) != len(AREAS):
            continue
        areas: dict[str, Area] = {}
        for area, row in zip(AREAS, rows):
            counts = _NOTE_COUNTS.search(row.group("note"))
            areas[area] = Area(row.group("light"), int(row.group("pct")), int(counts.group(1)) if counts else None, int(counts.group(2)) if counts else None)
        out[eco] = areas
    return out


def parse_progress(readme: str, ecosystems: Iterable[str] = ECOSYSTEM_KEYS) -> dict[str, tuple[int, int | None]]:
    """(percent, repositories counted) of each ecosystem from the progress bar of the README."""
    out: dict[str, tuple[int, int | None]] = {}
    for eco in ecosystems:
        match = _PROGRESS.search(_block(readme, "progress", eco))
        if match:
            out[eco] = (int(match.group("pct")), int(match.group("count")))
    return out


# ---------------------------------------------------------------------------
# Counts per ecosystem
# ---------------------------------------------------------------------------

def count_by_ecosystem(values: Mapping[str, str | None], ecosystem_by_name: Mapping[str, str], keys: Sequence[str],
                       ecosystems: Sequence[str]) -> dict[str, dict[str, int]]:
    """{ecosystem: {key: repositories}}; a value that is missing or not in `keys` is counted under UNKNOWN, never dropped or guessed."""
    out = {eco: {key: 0 for key in (*keys, UNKNOWN)} for eco in ecosystems}
    for name, eco in ecosystem_by_name.items():
        if eco not in out:
            continue
        value = values.get(name)
        out[eco][value if value in keys else UNKNOWN] += 1
    return out


def evidence_values(raw_manifests: Mapping[str, object]) -> dict[str, str | None]:
    """The evidence each raw manifest declares (RawManifest objects of dashboard_integrity, or plain dicts)."""
    out: dict[str, str | None] = {}
    for name, manifest in raw_manifests.items():
        data = getattr(manifest, "data", manifest)
        value = data.get("evidence") if isinstance(data, dict) else None
        out[name] = value if isinstance(value, str) else None
    return out


# ---------------------------------------------------------------------------
# Activity of the repositories (releases, commits, CI)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Activity:
    release_tag: str | None = None
    release_date: str | None = None     # ISO 8601 as GitHub writes it
    commit_date: str | None = None
    ci: str = "none"                    # success | failure | pending | none (no check or not known)


_CI_STATE = {"SUCCESS": "success", "FAILURE": "failure", "ERROR": "failure", "PENDING": "pending", "EXPECTED": "pending"}

ACTIVITY_QUERY = """
query($owner: String!, $cursor: String) {
  repositoryOwner(login: $owner) {
    repositories(first: 100, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        latestRelease { tagName publishedAt }
        defaultBranchRef { target { ... on Commit { committedDate statusCheckRollup { state } } } }
      }
    }
  }
}
"""


def parse_activity(nodes: Iterable[Mapping]) -> dict[str, Activity]:
    out: dict[str, Activity] = {}
    for node in nodes:
        if not isinstance(node, Mapping) or not node.get("name"):
            continue
        release = node.get("latestRelease") or {}
        target = ((node.get("defaultBranchRef") or {}).get("target")) or {}
        rollup = (target.get("statusCheckRollup") or {}).get("state")
        out[str(node["name"])] = Activity(
            release_tag=release.get("tagName") or None,
            release_date=release.get("publishedAt") or None,
            commit_date=target.get("committedDate") or None,
            ci=_CI_STATE.get(str(rollup), "none"),
        )
    return out


Poster = Callable[[bytes, dict], "dict | None"]


def _post(body: bytes, headers: dict) -> "dict | None":
    request = urllib.request.Request("https://api.github.com/graphql", data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return None


def fetch_activity(owner: str, token: str, post: Poster = _post, max_pages: int = 5) -> dict[str, Activity]:
    """The latest release, the latest commit and the CI state of every public repository of the owner in a handful of requests.
    Without a token (GraphQL needs one) or on any failure it returns {}: the page then says "no data" instead of showing a guess."""
    if not token:
        return {}
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard", "Content-Type": "application/json"}
    found: dict[str, Activity] = {}
    cursor = None
    for _ in range(max_pages):
        answer = post(json.dumps({"query": ACTIVITY_QUERY, "variables": {"owner": owner, "cursor": cursor}}).encode("utf-8"), headers)
        try:
            page = answer["data"]["repositoryOwner"]["repositories"]
            found.update(parse_activity(page["nodes"]))
            if not page["pageInfo"]["hasNextPage"]:
                return found
            cursor = page["pageInfo"]["endCursor"]
        except (TypeError, KeyError):
            return {}
    return found


def month_of(iso: str | None) -> str | None:
    """'2026-09' from an ISO date, None when it is not one."""
    match = re.match(r"^(\d{4})-(\d{2})-\d{2}", iso or "")
    return f"{match.group(1)}-{match.group(2)}" if match else None


def last_months(values: Iterable[str | None], count: int = 6) -> list[tuple[str, int]]:
    """Repositories per month for the `count` months that end at the newest date found (so the result depends on the data, not on today's date)."""
    months = [m for m in (month_of(v) for v in values) if m]
    if not months:
        return []
    year, month = (int(part) for part in max(months).split("-"))
    window: list[str] = []
    for _ in range(count):
        window.append(f"{year:04d}-{month:02d}")
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    window.reverse()
    return [(label, sum(1 for m in months if m == label)) for label in window]


def newest(activity: Mapping[str, Activity], field: str, limit: int, names: Iterable[str] | None = None) -> list[tuple[str, Activity]]:
    allowed = set(names) if names is not None else None
    rows = [(name, act) for name, act in activity.items() if getattr(act, field) and (allowed is None or name in allowed)]
    return sorted(rows, key=lambda item: (getattr(item[1], field), item[0]), reverse=True)[:limit]


def oldest(activity: Mapping[str, Activity], field: str, limit: int, names: Iterable[str] | None = None) -> list[tuple[str, Activity]]:
    allowed = set(names) if names is not None else None
    rows = [(name, act) for name, act in activity.items() if getattr(act, field) and (allowed is None or name in allowed)]
    return sorted(rows, key=lambda item: (getattr(item[1], field), item[0]))[:limit]


# ---------------------------------------------------------------------------
# SVG charts
# ---------------------------------------------------------------------------

def stacked_bars_svg(rows: Sequence[tuple[str, Mapping[str, int]]], keys: Sequence[str], css_prefix: str, *,
                     width: int = 380, bar_height: int = 26, gap: int = 12, label_width: int = 76) -> str:
    """One horizontal stacked bar per row. Each segment prints its own count (so no meaning rests on colour alone) and has a class
    `seg seg-<prefix>-<key>` for the fill. Rows with nothing counted show an empty track and a dash."""
    height = len(rows) * (bar_height + gap) + gap
    track = width - label_width - 34
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" class="chart chart-stacked" viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMid meet" aria-hidden="true" focusable="false">']
    for index, (label, counts) in enumerate(rows):
        y = gap + index * (bar_height + gap)
        total = sum(counts.get(key, 0) for key in keys)
        parts.append(f'<text class="chart-label" x="0" y="{y + bar_height / 2 + 4:.1f}">{esc(label)}</text>')
        parts.append(f'<rect class="chart-track" x="{label_width}" y="{y}" width="{track}" height="{bar_height}" rx="5"/>')
        x = float(label_width)
        for key in keys:
            value = counts.get(key, 0)
            if not value or not total:
                continue
            segment = track * value / total
            parts.append(f'<rect class="seg seg-{css_prefix}-{esc(key)}" x="{x:.1f}" y="{y}" width="{segment:.1f}" height="{bar_height}"><title>{esc(label)}: {esc(key)} {value}</title></rect>')
            if segment >= 18:
                parts.append(f'<text class="seg-count seg-count-{css_prefix}-{esc(key)}" x="{x + segment / 2:.1f}" y="{y + bar_height / 2 + 4:.1f}" text-anchor="middle">{value}</text>')
            x += segment
        parts.append(f'<text class="chart-total" x="{width}" y="{y + bar_height / 2 + 4:.1f}" text-anchor="end">{total if total else "–"}</text>')
    parts.append("</svg>")
    return "".join(parts)


def ring_svg(percent: int | None, css_class: str = "", *, size: int = 112, stroke: int = 12) -> str:
    """A ring with the percentage in the middle; `None` draws an empty ring with a dash."""
    radius = (size - stroke) / 2
    circumference = 2 * 3.141592653589793 * radius
    shown = max(0, min(100, percent)) if percent is not None else 0
    dash = circumference * shown / 100
    centre = size / 2
    text = f"{shown}%" if percent is not None else "–"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" class="chart chart-ring {esc(css_class)}" viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false">'
        f'<circle class="ring-track" cx="{centre}" cy="{centre}" r="{radius:.2f}" fill="none" stroke-width="{stroke}"/>'
        f'<circle class="ring-value" cx="{centre}" cy="{centre}" r="{radius:.2f}" fill="none" stroke-width="{stroke}" stroke-linecap="round" '
        f'stroke-dasharray="{dash:.2f} {circumference:.2f}" transform="rotate(-90 {centre} {centre})"/>'
        f'<text class="ring-text" x="{centre}" y="{centre + 7}" text-anchor="middle">{text}</text></svg>'
    )


def columns_svg(items: Sequence[tuple[str, int]], css_class: str = "", *, width: int = 480, height: int = 170) -> str:
    """Vertical columns with the value above each one and the label below; an empty list gives an empty string."""
    if not items:
        return ""
    top = max((value for _label, value in items), default=0) or 1
    slot = width / len(items)
    bar = slot * 0.56
    plot = height - 44
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" class="chart chart-columns {esc(css_class)}" viewBox="0 0 {width} {height}" aria-hidden="true" focusable="false">',
             f'<line class="chart-axis" x1="0" y1="{plot + 8}" x2="{width}" y2="{plot + 8}"/>']
    for index, (label, value) in enumerate(items):
        x = slot * index + (slot - bar) / 2
        h = plot * value / top
        parts.append(f'<rect class="col" x="{x:.1f}" y="{plot + 8 - h:.1f}" width="{bar:.1f}" height="{max(h, 1.5):.1f}" rx="3"><title>{esc(label)}: {value}</title></rect>')
        parts.append(f'<text class="col-value" x="{x + bar / 2:.1f}" y="{plot + 2 - h:.1f}" text-anchor="middle">{value}</text>')
        parts.append(f'<text class="chart-label" x="{x + bar / 2:.1f}" y="{height - 12}" text-anchor="middle">{esc(label)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def data_table(caption_key: str, caption: str, headers: Sequence[tuple[str, str]], rows: Sequence[Sequence[object]]) -> str:
    """A table with the numbers of a chart, hidden from sight but read by assistive technology. `headers` are (i18n key or "", text)."""
    head = "".join(f'<th scope="col"{f" data-i18n={chr(34)}{esc(key)}{chr(34)}" if key else ""}>{esc(text)}</th>' for key, text in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>" for row in rows)
    return (f'<div class="sr-only"><table><caption data-i18n="{esc(caption_key)}">{esc(caption)}</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")
