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

import dashboard_delivery

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
class Commit:
    headline: str
    date: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class Activity:
    release_tag: str | None = None
    release_date: str | None = None     # ISO 8601 as GitHub writes it
    commit_date: str | None = None
    ci: str = "none"                    # success | failure | pending | none (no check or not known)
    commits: tuple[Commit, ...] = ()    # the newest commits of the default branch (empty when GitHub did not return them)
    signature: str | None = None        # verified | invalid | unverifiable | none | norelease; None = not verified (see dashboard_delivery.signature_state)
    assets: tuple[tuple[str, int, str], ...] = ()   # (name, size, update time) of the assets of the latest release, empty when none or not returned
    workflows: tuple[str, ...] = ()     # file names in .github/workflows of the default branch
    sigx: Mapping | None = None         # the detail of the signature check (see dashboard_signatures.aggregate), None when no signature was checked
    presence: Mapping | None = None     # presence of a signature file and of a build attestation on the latest release (see dashboard_presence)


_CI_STATE = {"SUCCESS": "success", "FAILURE": "failure", "ERROR": "failure", "PENDING": "pending", "EXPECTED": "pending"}

ACTIVITY_QUERY = """
query($owner: String!, $cursor: String) {
  repositoryOwner(login: $owner) {
    repositories(first: 20, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        latestRelease { tagName publishedAt releaseAssets(first: 100) { nodes { name size updatedAt } } }
        workflows: object(expression: "HEAD:.github/workflows") { ... on Tree { entries { name } } }
        defaultBranchRef { target { ... on Commit { committedDate statusCheckRollup { state } history(first: 5) { nodes { messageHeadline committedDate url } } } } }
      }
    }
  }
}
"""


def _commits(target: Mapping, redact: Callable[[str], str] | None) -> tuple[Commit, ...]:
    found = []
    for node in ((target.get("history") or {}).get("nodes")) or []:
        if not isinstance(node, Mapping) or not node.get("messageHeadline"):
            continue
        headline = str(node["messageHeadline"])[:120]
        found.append(Commit(redact(headline) if redact else headline, node.get("committedDate") or None, node.get("url") or None))
    return tuple(found)


def parse_activity(nodes: Iterable[Mapping], redact: Callable[[str], str] | None = None) -> dict[str, Activity]:
    """`redact` cleans a commit subject before it is kept (the generator hides the names of private notes)."""
    out: dict[str, Activity] = {}
    for node in nodes:
        if not isinstance(node, Mapping) or not node.get("name"):
            continue
        release = node.get("latestRelease") or {}
        target = ((node.get("defaultBranchRef") or {}).get("target")) or {}
        rollup = (target.get("statusCheckRollup") or {}).get("state")
        assets = ((release.get("releaseAssets") or {}).get("nodes")) if release else None
        names = [str(a.get("name", "")) for a in assets if isinstance(a, Mapping)] if isinstance(assets, list) else None
        detail = tuple((str(a.get("name", "")), int(a.get("size") or 0), str(a.get("updatedAt") or "")) for a in assets if isinstance(a, Mapping)) if isinstance(assets, list) else ()
        flows = tuple(str(e.get("name", "")) for e in ((node.get("workflows") or {}).get("entries") or []) if isinstance(e, Mapping))
        out[str(node["name"])] = Activity(
            signature=dashboard_delivery.signature_state(bool(release), names),
            assets=detail, workflows=flows,
            release_tag=release.get("tagName") or None,
            release_date=release.get("publishedAt") or None,
            commit_date=target.get("committedDate") or None,
            ci=_CI_STATE.get(str(rollup), "none"),
            commits=_commits(target, redact),
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


def fetch_activity(owner: str, token: str, post: Poster = _post, max_pages: int = 20, redact: Callable[[str], str] | None = None) -> dict[str, Activity]:
    """The latest release, the latest commit and the CI state of every public repository of the owner in a handful of requests.
    Without a token (GraphQL needs one) or on any failure it returns {}: the page then says "no data" instead of showing a guess."""
    if not token:
        return {}
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "JuanenRac-dashboard", "Content-Type": "application/json"}
    found: dict[str, Activity] = {}
    cursor = None
    for _ in range(max_pages):
        body = json.dumps({"query": ACTIVITY_QUERY, "variables": {"owner": owner, "cursor": cursor}}).encode("utf-8")
        answer = post(body, headers) or post(body, headers)   # one more try: a gateway timeout of GitHub is usually gone a second later
        try:
            page = answer["data"]["repositoryOwner"]["repositories"]
            found.update(parse_activity(page["nodes"], redact))
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

def _pct(n: int, total: int) -> int:
    return round(n * 100 / total) if total else 0


def stacked_bars_svg(rows: Sequence[tuple[str, Mapping[str, int]]], keys: Sequence[str], css_prefix: str, *,
                     width: int = 380, bar_height: int = 26, gap: int = 12, label_width: int = 76,
                     i18n_prefix: str = "", names: Mapping[str, str] | None = None) -> str:
    """One horizontal stacked bar per row. Each segment prints its own count (so no meaning rests on colour alone) and has a class
    `seg seg-<prefix>-<key>` for the fill. Rows with nothing counted show an empty track and a dash.

    Every row is one focusable group with an accessible name (`<row>: <name> <n>, ...`, English here, rewritten in the language of the page by the
    script from the data-* attributes) and every segment carries data-name-key / data-n / data-total for the tooltip. The relief is drawn with plain
    shapes (a shadow under the track, a dark lower half and a light edge on each segment); the entrance is a CSS animation (scale from the left)."""
    names = names or {}
    height = len(rows) * (bar_height + gap) + gap
    track = width - label_width - 34
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" class="chart chart-stacked" viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMid meet" focusable="false">']
    for index, (label, counts) in enumerate(rows):
        y = gap + index * (bar_height + gap)
        total = sum(counts.get(key, 0) for key in keys)
        english = ", ".join(f"{names.get(key, key)} {counts.get(key, 0)}" for key in keys if counts.get(key, 0))
        aria = f"{label}: {english}" if total else f"{label}: no data"
        parts.append(f'<g class="bar-row" tabindex="0" role="img" aria-label="{esc(aria)}" data-aria="row" data-row="{esc(label)}" data-total="{total}">')
        parts.append(f'<text class="chart-label" x="0" y="{y + bar_height / 2 + 4:.1f}">{esc(label)}</text>')
        parts.append(f'<rect class="bar-depth" x="{label_width}" y="{y + 3}" width="{track}" height="{bar_height}" rx="5"/>')
        parts.append(f'<rect class="chart-track" x="{label_width}" y="{y}" width="{track}" height="{bar_height}" rx="5"/>')
        x = float(label_width)
        fills, nums = [], []
        for key in keys:
            value = counts.get(key, 0)
            if not value or not total:
                continue
            segment = track * value / total
            key_i18n = "unknown" if key == UNKNOWN else f"{i18n_prefix}{key}"
            fills.append(f'<rect class="seg seg-{css_prefix}-{esc(key)}" x="{x:.1f}" y="{y}" width="{segment:.1f}" height="{bar_height}" '
                         f'data-name-key="{esc(key_i18n)}" data-name="{esc(names.get(key, key))}" data-n="{value}" data-total="{total}"/>')
            fills.append(f'<rect class="seg-bevel" x="{x:.1f}" y="{y + bar_height / 2:.1f}" width="{segment:.1f}" height="{bar_height / 2:.1f}"/>')
            fills.append(f'<rect class="seg-edge" x="{x:.1f}" y="{y}" width="{segment:.1f}" height="2"/>')
            if segment >= 18:
                nums.append(f'<text class="seg-count seg-count-{css_prefix}-{esc(key)}" x="{x + segment / 2:.1f}" y="{y + bar_height / 2 + 4:.1f}" text-anchor="middle">{value}</text>')
            x += segment
        parts.append(f'<g class="bar-fill" style="--i:{index};transform-origin:{label_width}px 0">{"".join(fills)}</g><g class="bar-nums" style="--i:{index}">{"".join(nums)}</g>')
        parts.append(f'<text class="chart-total" x="{width}" y="{y + bar_height / 2 + 4:.1f}" text-anchor="end">{total if total else "–"}</text></g>')
    parts.append("</svg>")
    return "".join(parts)


def ring_svg(percent: int | None, css_class: str = "", *, size: int = 112, stroke: int = 12) -> str:
    """A ring with the percentage in the middle; `None` draws an empty ring with a dash. The arc is drawn on load by a CSS animation of
    stroke-dashoffset (custom property --dash); a thin light arc on its outer edge gives it a little relief."""
    radius = (size - stroke) / 2
    circumference = 2 * 3.141592653589793 * radius
    shown = max(0, min(100, percent)) if percent is not None else 0
    dash = circumference * shown / 100
    centre = size / 2
    text = f"{shown}%" if percent is not None else "–"
    sheen_radius = radius + stroke * 0.28
    sheen_circ = 2 * 3.141592653589793 * sheen_radius
    sheen_dash = sheen_circ * shown / 100
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" class="chart chart-ring {esc(css_class)}" viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false">'
        f'<circle class="ring-track" cx="{centre}" cy="{centre}" r="{radius:.2f}" fill="none" stroke-width="{stroke}"/>'
        + ('' if percent is None else  # no data: the track alone, not even a zero-length round cap
           f'<circle class="ring-value" cx="{centre}" cy="{centre}" r="{radius:.2f}" fill="none" stroke-width="{stroke}" stroke-linecap="round" '
           f'stroke-dasharray="{dash:.2f} {circumference:.2f}" style="--dash:{dash:.2f}" transform="rotate(-90 {centre} {centre})"/>'
           f'<circle class="ring-sheen" cx="{centre}" cy="{centre}" r="{sheen_radius:.2f}" fill="none" stroke-width="{stroke * 0.22:.2f}" stroke-linecap="round" '
           f'stroke-dasharray="{sheen_dash:.2f} {sheen_circ:.2f}" style="--dash:{sheen_dash:.2f}" transform="rotate(-90 {centre} {centre})"/>') +
        f'<text class="ring-text" x="{centre}" y="{centre + 7}" text-anchor="middle">{text}</text></svg>'
    )


def columns_svg(items: Sequence[tuple[str, int]], css_class: str = "", *, width: int = 480, height: int = 170) -> str:
    """Vertical columns with the value above each one and the label below; an empty list gives an empty string.
    Each column is a light isometric block (front, top and side faces) in a focusable group with its name, count and share; it grows from the axis on load."""
    if not items:
        return ""
    top = max((value for _label, value in items), default=0) or 1
    total = sum(value for _label, value in items)
    slot = width / len(items)
    bar = slot * 0.5
    dx, dy = 7.0, 5.0
    plot = height - 64   # headroom for the isometric top face and the value above the tallest column
    base = plot + 26
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" class="chart chart-columns {esc(css_class)}" viewBox="0 0 {width} {height}" focusable="false">',
             f'<line class="chart-axis" x1="0" y1="{base}" x2="{width}" y2="{base}"/>']
    for index, (label, value) in enumerate(items):
        x = slot * index + (slot - bar - dx) / 2
        h = max(plot * value / top, 1.5)
        y = base - h
        parts.append(f'<g class="col-g" tabindex="0" role="img" aria-label="{esc(f"{label}: {value}")}" data-aria="col" data-name="{esc(label)}" data-n="{value}" data-total="{total}" style="--i:{index}">')
        parts.append(f'<g class="col-body" style="transform-origin:{x + bar / 2:.1f}px {base}px">'
                     f'<rect class="col" x="{x:.1f}" y="{y:.1f}" width="{bar:.1f}" height="{h:.1f}" rx="2"/>'
                     f'<polygon class="col-top" points="{x:.1f},{y:.1f} {x + dx:.1f},{y - dy:.1f} {x + bar + dx:.1f},{y - dy:.1f} {x + bar:.1f},{y:.1f}"/>'
                     f'<polygon class="col-side" points="{x + bar:.1f},{y:.1f} {x + bar + dx:.1f},{y - dy:.1f} {x + bar + dx:.1f},{base - dy:.1f} {x + bar:.1f},{base:.1f}"/></g>')
        parts.append(f'<text class="col-value" x="{x + (bar + dx) / 2:.1f}" y="{y - dy - 5:.1f}" text-anchor="middle">{value}</text>')
        parts.append(f'<text class="chart-label" x="{x + (bar + dx) / 2:.1f}" y="{height - 12}" text-anchor="middle">{esc(label)}</text></g>')
    parts.append("</svg>")
    return "".join(parts)


def data_table(caption_key: str, caption: str, headers: Sequence[tuple[str, str]], rows: Sequence[Sequence[object]]) -> str:
    """A table with the numbers of a chart, hidden from sight but read by assistive technology. `headers` are (i18n key or "", text)."""
    head = "".join(f'<th scope="col"{f" data-i18n={chr(34)}{esc(key)}{chr(34)}" if key else ""}>{esc(text)}</th>' for key, text in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>" for row in rows)
    return (f'<div class="sr-only"><table><caption data-i18n="{esc(caption_key)}">{esc(caption)}</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")
