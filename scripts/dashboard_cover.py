#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_cover.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Coverage of the dashboard and what changed in the account since the last run.

  * `unclassified_card` is the extra card of the ecosystem counters: the public repositories of the owner that no ecosystem lists (no manifest), with the three
    figures "owner / shown / without manifest" and the names. A listing that could not be read says "not verified" and never a zero.
  * `changes` compares the repositories of this run with the ones of the published page and names the NEW ones, the ARCHIVED ones and the ones that DISAPPEARED
    (not on the list any more and not archived: deleted, renamed or made private). A listing that came from the saved copy or failed gives no change at all:
    nothing is claimed that was not read.
  * `changes_html` draws them as a notice above the counters, with the same eight-language texts as the rest of the page.

Nothing here reads the network. Stdlib only.
"""
from __future__ import annotations

from html import escape
from typing import Iterable, Mapping

import dashboard_cover_texts

MAX_NAMES = 12


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def _en() -> dict:
    return dashboard_cover_texts.TEXTS["en"]


def unclassified_card(cover: object) -> str:
    """The card "Unclassified". `cover` is a dashboard_integrity.Coverage (or None when the integrity check did not run)."""
    en = _en()
    public = getattr(cover, "public", None)
    if cover is None or public is None:
        return ('<div class="health-card health-card-unclassified" data-testid="eco-unclassified" data-state="unknown" '
                'title="' + esc(en["cover_unknown_title"]) + '" data-i18n-title="cover_unknown_title">'
                '<div class="number">–</div><div class="label" data-i18n="eco_unclassified">' + esc(en["eco_unclassified"]) + '</div>'
                '<div class="sub" data-i18n="cover_unknown">' + esc(en["cover_unknown"]) + '</div></div>')
    names = list(getattr(cover, "without_manifest", ()) or ())
    shown = getattr(cover, "listed", 0)
    listed_names = ", ".join(names[:MAX_NAMES]) + (f" (+{len(names) - MAX_NAMES})" if len(names) > MAX_NAMES else "")
    state = "gap" if names else "ok"
    title = en["cover_title"].replace("{names}", listed_names or "-")
    sub = en["cover_counter"].replace("{owner}", str(public)).replace("{shown}", str(shown)).replace("{without}", str(len(names)))
    return (f'<div class="health-card health-card-unclassified" data-testid="eco-unclassified" data-state="{state}" title="{esc(title)}" '
            f'data-i18n-title-template="cover_title" data-names="{esc(listed_names or "-")}">'
            f'<div class="number">{len(names)}</div><div class="label" data-i18n="eco_unclassified">{esc(en["eco_unclassified"])}</div>'
            f'<div class="sub" data-i18n-template="cover_counter" data-owner="{public}" data-shown="{shown}" data-without="{len(names)}">{esc(sub)}</div></div>')


def changes(previous: "Iterable[str] | None", current: "Iterable[str] | None", archived: Iterable[str] = (), reliable: bool = True) -> dict:
    """{"new", "archived", "gone"}: sorted lists of names. `previous` are the repositories of the published page, `current` the ones listed now (archived ones
    included, they are still on the list). Empty when either is unknown or the listing is not reliable (saved copy or failed read)."""
    empty = {"new": [], "archived": [], "gone": []}
    if previous is None or current is None or not reliable:
        return empty
    before, now, arch = set(previous), set(current), set(archived)
    if not before or not now:
        return empty
    return {"new": sorted(now - before - arch, key=str.casefold),
            "archived": sorted((now & arch) & before, key=str.casefold),
            "gone": sorted(before - now, key=str.casefold)}


def snapshot(owner_repos: "Iterable[str] | None", archived: Iterable[str], reliable: bool, previous: "Mapping | None") -> "dict | None":
    """The block the page embeds so that the next run can compare: {"repos": [...], "archived": [...]}. When this run's listing is not reliable (saved copy,
    failed read) the previous block is kept as it was, so the comparison of the next good run is made against the last list that was really read."""
    if owner_repos is not None and reliable:
        return {"repos": sorted(set(owner_repos), key=str.casefold), "archived": sorted(set(archived), key=str.casefold)}
    return dict(previous) if isinstance(previous, Mapping) else None


def changes_html(found: Mapping[str, list]) -> str:
    """The notice of the changes, '' when there is none. One line per kind; the names are listed (at most MAX_NAMES)."""
    en = _en()
    rows = []
    for kind in ("new", "archived", "gone"):
        names = list(found.get(kind) or [])
        if not names:
            continue
        shown = ", ".join(names[:MAX_NAMES]) + (f" (+{len(names) - MAX_NAMES})" if len(names) > MAX_NAMES else "")
        text = en[f"changes_{kind}"].replace("{n}", str(len(names))).replace("{names}", shown)
        rows.append(f'<li class="changes-{kind}" data-testid="changes-{kind}" data-i18n-template="changes_{kind}" data-n="{len(names)}" data-names="{esc(shown)}">{esc(text)}</li>')
    if not rows:
        return ""
    return (f'<section class="card card-changes" aria-labelledby="changes-t" data-testid="changes"><h2 class="card-title" id="changes-t" data-i18n="changes_title">{esc(en["changes_title"])}</h2>'
            f'<ul class="changes-list">{"".join(rows)}</ul></section>')


__all__ = ["unclassified_card", "changes", "snapshot", "changes_html"]
