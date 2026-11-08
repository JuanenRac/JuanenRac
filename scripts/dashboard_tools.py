#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The Tools group of the status dashboard: the programs that sit above the four ecosystems (the local Actions monitor and the updater of the suite).

The group is the fifth of the catalogue (`electro-hobby-3d`). Its card in the summary shows how many tools there are, the version of each one (the one their own manifest
declares, which is the version of the tool itself), a progress bar worked out like the ones of the four ecosystems (maturity and evidence of the manifests, plus releases,
tests, green CI and documentation in eight languages) and a button that filters the table of projects by the group. The badge "4 ecosystems" becomes "4 ecosystems + Tools".
Nothing here reads the network. Stdlib only.
"""
from __future__ import annotations

from html import escape
from typing import Mapping

import dashboard_cover_texts

KEY = "electro-hobby-3d"


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def _en() -> dict:
    return dashboard_cover_texts.TEXTS["en"]


def block(ecosystem_by_name: Mapping[str, str], results: Mapping[str, object], progress: "tuple[int, int] | None") -> dict:
    """{"tools": [{"name", "version"}], "percent": int | None, "count": int}. `progress` is (percent, repositories counted) or None when it could not be worked out."""
    tools = []
    for name in sorted((n for n, eco in ecosystem_by_name.items() if eco == KEY), key=str.casefold):
        version = getattr(results.get(name), "version", None)
        tools.append({"name": name, "version": str(version) if version is not None else None})
    percent, counted = progress if progress and progress[1] else (None, 0)
    return {"tools": tools, "percent": percent, "count": counted}


def card_html(group: Mapping, label: str = "Tools") -> str:
    """The card of the group for the ecosystem counters of the summary."""
    en = _en()
    tools = group.get("tools") or []
    items = "".join(
        f'<li data-testid="tool-{esc(t["name"])}"><code>{esc(t["name"])}</code> <b>{esc(t["version"]) if t["version"] else "–"}</b></li>' for t in tools)
    percent = group.get("percent")
    if percent is None:
        bar = ('<div class="tools-bar tools-bar-unknown" aria-hidden="true"><i></i></div>'
               f'<div class="sub" data-testid="tools-progress" data-i18n="tools_progress_unknown">{esc(en["tools_progress_unknown"])}</div>')
    else:
        text = en["tools_progress"].replace("{percent}", str(percent)).replace("{count}", str(group.get("count", 0)))
        bar = (f'<div class="tools-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{percent}" aria-label="{esc(text)}" data-testid="tools-bar">'
               f'<i style="--w:{percent}%"></i></div>'
               f'<div class="sub" data-testid="tools-progress" data-i18n-template="tools_progress" data-percent="{percent}" data-count="{group.get("count", 0)}">{esc(text)}</div>')
    return (f'<div class="health-card health-card-tools" data-testid="eco-tools" data-eco="{KEY}">'
            f'<div class="number">{len(tools)}</div><div class="label" data-i18n="scope_cross">{esc(label)}</div>'
            f'<ul class="tools-versions" data-testid="tools-versions">{items}</ul>{bar}'
            f'<button type="button" class="btn btn-ghost tools-filter" data-scope="{KEY}" data-goto-tab="projects" data-testid="tools-filter" data-i18n="tools_filter">{esc(en["tools_filter"])}</button></div>')


def badge_alt(base: str = "Four ecosystems") -> str:
    """The text of the badge of the profile: the four ecosystems plus the Tools group."""
    return f"{base} + Tools"


CSS = r"""
  .health-card-tools { flex: 2 1 210px !important; }
  .tools-versions { list-style: none; margin: 4px 0 6px; padding: 0; display: grid; gap: 2px; font-size: 11.5px; }
  .tools-versions li { display: flex; justify-content: space-between; gap: 8px; min-width: 0; }
  .tools-versions code { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 10.5px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .tools-versions b { font-variant-numeric: tabular-nums; }
  .tools-bar { height: 8px; border-radius: 5px; background: var(--panel-2); box-shadow: inset 0 1px 2px rgba(0,0,0,.3); overflow: hidden; }
  .tools-bar i { display: block; height: 100%; width: var(--w, 0%); border-radius: 5px; background: var(--c-electro-hobby-3d); background-image: linear-gradient(rgba(255,255,255,.3), rgba(255,255,255,0) 55%, rgba(0,0,0,.18)); transform-origin: left center; }
  .tools-bar-unknown i { width: 100%; background: repeating-linear-gradient(135deg, var(--border) 0 6px, transparent 6px 12px); }
  .tools-filter { margin-top: 6px; padding: 3px 8px; font-size: 11px; }
  @media (prefers-reduced-motion: no-preference) {
    .tools-bar i { animation: t25-grow-x .8s cubic-bezier(.2,.7,.2,1) both; }
  }
  @media print { .tools-bar i { animation: none !important; } }
"""
