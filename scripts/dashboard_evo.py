#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_evo.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Evidence checklist, progress history and share images of the status dashboard.

  * `checks` decides, for every repository, which pieces of evidence it can show (verified / missing / not verified / not applicable),
  * `snapshot`, `load_history`, `add_snapshot` and `save_history` keep one snapshot per day of the progress and of the eight areas
    of every ecosystem in a small JSON file (at most 90 days, written atomically),
  * `og_png` and `favicon_data_uri` draw the small images the page needs for its icon and for the cards of social networks.

Nothing is invented: a fact that could not be read is None (the page prints "not verified") and a missing snapshot is never interpolated.
Stdlib only.
"""
from __future__ import annotations

import json
import os
import struct
import zlib
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence
from urllib.parse import quote

import dashboard_contrib as contrib
from dashboard_charts import AREAS

HISTORY_DAYS = 90
HISTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "history.json"
SCHEMA = 1

# The pieces of evidence, in the order of the checklist. Values per repository: 1 verified, 0 missing, None not verified, 2 not applicable.
ITEMS: tuple[str, ...] = ("tests", "ci", "release", "signed", "docs", "sim", "hw")
YES, NO, NA = 1, 0, 2


def _flag(value: bool | None) -> int | None:
    return None if value is None else (YES if value else NO)


def checks(listed: Mapping[str, str], manifests: Mapping[str, Mapping | None], signals: Mapping[str, Mapping]) -> dict[str, list[int | None]]:
    """{repository: [tests, ci, release, signed, docs, sim, hw]}.
    A repository whose manifest could not be read has nothing verified. A signed release cannot be read from GitHub: it is None (not verified)
    when a release exists, 0 (missing) when the repository has none, and None when the releases themselves are unknown."""
    out: dict[str, list[int | None]] = {}
    for name in listed:
        manifest = manifests.get(name)
        if not isinstance(manifest, Mapping):
            out[name] = [None] * len(ITEMS)
            continue
        facts = signals.get(name)
        flags = contrib.area_flags(manifest, facts)
        release = _flag(flags.get("releases"))
        out[name] = [
            _flag(flags.get("tests")),
            _flag(flags.get("ci")),
            release,
            NO if release == NO else None,
            _flag(flags.get("docs")),
            _flag(flags.get("simulation")),
            _flag(flags["hardware"]) if "hardware" in flags else NA,
        ]
    return out


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------

def today_utc() -> str:
    """The date of the snapshot: DASHBOARD_TODAY (tests) or the UTC date of the run."""
    forced = os.environ.get("DASHBOARD_TODAY", "")
    if forced:
        try:
            return date.fromisoformat(forced).isoformat()
        except ValueError:
            pass
    return datetime.now(timezone.utc).date().isoformat()


def snapshot(day: str, progress: Mapping[str, tuple[int | None, int | None]], status: Mapping[str, Mapping[str, object]], ecosystems: Iterable[str]) -> dict | None:
    """The entry of one day: {"date", "progress": {eco: percent}, "areas": {eco: {area: percent}}}. None when there is nothing real to record."""
    prog: dict[str, int] = {}
    areas: dict[str, dict[str, int]] = {}
    for eco in ecosystems:
        percent = (progress.get(eco) or (None, None))[0]
        if isinstance(percent, int) and 0 <= percent <= 100:
            prog[eco] = percent
        found: dict[str, int] = {}
        for area, value in (status.get(eco) or {}).items():
            pct = getattr(value, "percent", None)
            if area in AREAS and isinstance(pct, int) and 0 <= pct <= 100:
                found[area] = pct
        if found:
            areas[eco] = found
    if not prog and not areas:
        return None
    return {"date": day, "progress": prog, "areas": areas}


def _valid_entry(entry: object) -> bool:
    if not isinstance(entry, dict) or not isinstance(entry.get("date"), str):
        return False
    try:
        date.fromisoformat(entry["date"])
    except ValueError:
        return False
    return isinstance(entry.get("progress"), dict) and isinstance(entry.get("areas"), dict)


def normalize(entries: Iterable[object], today: str) -> list[dict]:
    """One entry per day (the last one wins), sorted, valid, none in the future and none older than the 90 days that end today."""
    end = date.fromisoformat(today)
    start = end - timedelta(days=HISTORY_DAYS - 1)
    by_day: dict[str, dict] = {}
    for entry in entries:
        if _valid_entry(entry) and start <= date.fromisoformat(entry["date"]) <= end:  # type: ignore[index]
            by_day[entry["date"]] = entry  # type: ignore[index]
    return [by_day[day] for day in sorted(by_day)]


def load_history(path: Path = HISTORY_PATH, today: str | None = None) -> tuple[list[dict], list[str]]:
    """(entries, problems). A missing file is an empty history; a file that cannot be read is an empty history plus a problem to report."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [], []
    except OSError as exc:
        return [], [f"{path.name} could not be read: {exc}"]
    try:
        raw = json.loads(text)
        items = raw["entries"] if isinstance(raw, dict) else raw
        if not isinstance(items, list):
            raise ValueError("entries is not a list")
    except (ValueError, KeyError, TypeError) as exc:
        return [], [f"{path.name} is not valid history data ({exc})"]
    return normalize(items, today or today_utc()), []


def add_snapshot(entries: Sequence[dict], entry: dict | None, today: str) -> list[dict]:
    """The history with the snapshot of today added (it replaces the one of the same day) and cut to the last 90 days."""
    return normalize([*entries, *([entry] if entry else [])], today)


def render_history(entries: Sequence[dict]) -> str:
    return json.dumps({"schema": SCHEMA, "days": HISTORY_DAYS, "entries": list(entries)}, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def save_history(path: Path, entries: Sequence[dict]) -> bool:
    """Writes the file atomically (temporary file in the same folder, then replace) and only when the content changes. True when it was written."""
    text = render_history(entries)
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


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

ECO_RGB = {"hydra-umc": (78, 161, 255), "urtc": (180, 140, 255), "armor": (52, 211, 153), "eh3d": (251, 191, 36)}
_BG, _TRACK, _EDGE = (15, 20, 32), (44, 52, 70), (66, 74, 94)


def _png(width: int, height: int, rows: Sequence[bytes]) -> bytes:
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + row for row in rows)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def og_png(progress: Mapping[str, tuple[int | None, int | None]], ecosystems: Sequence[str]) -> bytes:
    """A 1200x630 card: one bar per ecosystem, as long as its progress (an empty track when the progress is not known). No text, so no font is needed."""
    width, height = 1200, 630
    left, right, bar_h, gap = 120, 1080, 84, 54
    top = (height - (len(ecosystems) * bar_h + (len(ecosystems) - 1) * gap)) // 2

    def row(fill: tuple[int, int, int] | None, percent: int) -> bytes:
        span = right - left
        filled = span * percent // 100
        pixel = lambda rgb: bytes(rgb)  # noqa: E731
        parts = [pixel(_BG) * left]
        if fill is None:
            parts.append(pixel(_TRACK) * span)
        else:
            parts += [pixel(fill) * filled, pixel(_TRACK) * (span - filled)]
        parts.append(pixel(_BG) * (width - right))
        return b"".join(parts)

    blank = bytes(_BG) * width
    band: list[bytes] = []
    rows: list[bytes] = [blank] * top
    for index, eco in enumerate(ecosystems):
        percent = (progress.get(eco) or (None, None))[0]
        known = isinstance(percent, int)
        band = [row(ECO_RGB.get(eco, _EDGE) if known else None, percent if known else 0)] * bar_h
        rows += band
        if index < len(ecosystems) - 1:
            rows += [blank] * gap
    rows += [blank] * (height - len(rows))
    return _png(width, height, rows)


FAVICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0f1420"/>'
    '<rect x="10" y="12" width="44" height="8" rx="3" fill="#4ea1ff"/><rect x="10" y="24" width="34" height="8" rx="3" fill="#b48cff"/>'
    '<rect x="10" y="36" width="40" height="8" rx="3" fill="#34d399"/><rect x="10" y="48" width="26" height="8" rx="3" fill="#fbbf24"/></svg>'
)


def favicon_data_uri() -> str:
    return "data:image/svg+xml," + quote(FAVICON_SVG, safe="/:=,;-")
