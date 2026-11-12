#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_toolspanel.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The own tab of the Tools group (the fifth ecosystem of the catalogue, key `electro-hobby-3d`).

The tab is the one of the other four ecosystems (progress ring, maturity and evidence, CI, latest releases) plus a block that is only drawn here: one row per tool with its
version, its latest release, the state of its CI, its tests and its links, and a card for the Actions monitor with its two editions, how an AI tool is connected to it,
what comes in its next version and how it spends the quota of GitHub. Everything comes from data the page already has (manifests, the release and CI read, the tests the
repositories declare and the Sentinel reading); nothing is read here and nothing that could not be read is shown as fine. The page is generated as plain HTML with
`data-i18n` keys, so the eight languages work like in every other tab. Stdlib only.
"""
from __future__ import annotations

from html import escape
from typing import Callable, Mapping

import dashboard_tools

KEY = dashboard_tools.KEY
OWNER_URL = "https://github.com/JuanenRac/"
MONITOR = "TOOLS-GITHUB-ACTIONS-MONITOR"
UPDATER = "ELECTRO-HOBBY-3D-UPDATER"
GUIDE_AI = OWNER_URL + MONITOR + "/blob/main/monitor/docs/AI_CONNECTION.md"
GUIDE_QUOTA = OWNER_URL + MONITOR + "/blob/main/monitor/docs/QUOTA.md"
CI_STATES = ("success", "failure", "pending", "none")


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def _date(value: object) -> str:
    """The day of an ISO moment (`2001-12-21T..` becomes `2001-12-21`), or an empty text."""
    text = str(value or "")
    return text[:10] if len(text) >= 10 and text[4] == "-" and text[7] == "-" else ""


def build(ecosystem_by_name: Mapping[str, str], versions: Mapping[str, "str | None"], activity: Mapping[str, object], tests_read: "Mapping | None",
          sentinel_doc: "Mapping | None", manifest_of: Callable[[str], "dict | None"]) -> dict:
    """{"rows": [...], "read": {"activity": bool, "tests": bool, "sentinel": bool}} for the tools of the group, in name order. A value that is not known is None."""
    records = ((tests_read or {}).get("records") or {}) if isinstance(tests_read, Mapping) else {}
    red_by_repo: dict[str, int] = {}
    for item in ((sentinel_doc or {}).get("ci") or {}).get("red") or []:
        if isinstance(item, Mapping) and isinstance(item.get("repo"), str):
            red_by_repo[item["repo"]] = red_by_repo.get(item["repo"], 0) + 1
    rows = []
    for name in sorted((n for n, eco in ecosystem_by_name.items() if eco == KEY), key=str.casefold):
        act = activity.get(name)
        manifest = manifest_of(name) or {}
        tests = records.get(name) if isinstance(records, Mapping) else None
        state = getattr(act, "ci", "none") if act is not None else "none"
        state = state if state in CI_STATES else "none"
        reds = red_by_repo.get(name, 0) if sentinel_doc else None
        if reds:
            state = "failure"
        rows.append({
            "name": name, "version": versions.get(name), "maturity": manifest.get("maturity"), "evidence": manifest.get("evidence"),
            "tag": getattr(act, "release_tag", None) if act is not None else None, "published": _date(getattr(act, "release_date", None)) if act is not None else "",
            "ci": state, "red": reds, "tests": int(tests["n"]) if isinstance(tests, Mapping) and isinstance(tests.get("n"), int) else None,
        })
    return {"rows": rows, "read": {"activity": bool(activity), "tests": bool(records), "sentinel": bool(sentinel_doc)}}


def _t(key: str, texts: Mapping[str, str]) -> str:
    return f'data-i18n="{esc(key)}">{esc(texts.get(key, key))}'


def _row(row: Mapping, texts: Mapping[str, str]) -> str:
    name = str(row["name"])
    url = OWNER_URL + name
    ci_key = "tl_ci_" + str(row["ci"])
    glyph = {"success": "●", "failure": "✕", "pending": "◐", "none": "–"}[str(row["ci"])]
    version = esc(row["version"]) if row.get("version") else "–"
    tag = esc(row["tag"]) if row.get("tag") else "–"
    since = f' <span class="muted">{esc(row["published"])}</span>' if row.get("published") else ""
    red = f' <span class="muted">({int(row["red"])})</span>' if row.get("red") else ""
    tests = f'{int(row["tests"])}' if row.get("tests") is not None else f'<span class="muted" {_t("tl_tests_none", texts)}</span>'
    maturity = esc(row["maturity"]) if row.get("maturity") else "–"
    return (f'<tr data-testid="tools-row-{esc(name)}"><th scope="row"><a href="{esc(url)}" rel="noopener">{esc(name)}</a></th>'
            f'<td class="num">{version}</td><td>{maturity}</td><td>{tag}{since}</td>'
            f'<td><span class="tl-ci tl-ci-{esc(row["ci"])}" data-testid="tools-ci-{esc(name)}"><span aria-hidden="true">{glyph}</span> <span {_t(ci_key, texts)}</span>{red}</span></td>'
            f'<td class="num">{tests}</td>'
            f'<td class="tl-links"><a href="{esc(url)}" rel="noopener" {_t("tl_link_repo", texts)}</a> · '
            f'<a href="{esc(url)}/releases" rel="noopener" {_t("tl_link_releases", texts)}</a> · '
            f'<a href="{esc(url)}/blob/main/CHANGELOG.md" rel="noopener" {_t("tl_link_changelog", texts)}</a></td></tr>')


def panel_html(block: Mapping, texts: Mapping[str, str]) -> str:
    """The cards that follow the common ones of the tab: the table of the tools, the Actions monitor and the updater of the suite."""
    rows = block.get("rows") or []
    body = "".join(_row(row, texts) for row in rows)
    head = "".join(f'<th scope="col" {_t(key, texts)}</th>' for key in
                   ("tl_col_tool", "tl_col_version", "tl_col_maturity", "tl_col_release", "tl_col_ci", "tl_col_tests", "tl_col_links"))
    table = (f'<div class="tl-scroll"><table class="tl-table" data-testid="tools-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
             if rows else f'<p class="no-data" data-testid="tools-empty" {_t("tl_none", texts)}</p>')
    monitor = next((r for r in rows if r["name"] == MONITOR), None)
    mon_version = esc(monitor["version"]) if monitor and monitor.get("version") else "–"
    return (
        f'<section class="card tl-card" data-testid="tools-table-card"><header class="card-head"><h2 class="card-title" {_t("tl_title", texts)}</h2></header>'
        f'<p class="muted" {_t("tl_hint", texts)}</p>{table}</section>'
        f'<section class="card tl-card" data-testid="tools-monitor"><header class="card-head"><h2 class="card-title">{esc(MONITOR)} <b data-testid="tools-monitor-version">{mon_version}</b></h2></header>'
        f'<p {_t("tl_mon_intro", texts)}</p>'
        '<div class="tl-grid">'
        f'<div class="tl-box" data-testid="tools-editions"><h3 {_t("tl_mon_ed_title", texts)}</h3>'
        f'<p><b {_t("tl_ed_complete", texts)}</b>: <span {_t("tl_mon_ed_complete", texts)}</span></p>'
        f'<p><b {_t("tl_ed_lite", texts)}</b>: <span {_t("tl_mon_ed_lite", texts)}</span></p></div>'
        f'<div class="tl-box" data-testid="tools-ai"><h3 {_t("tl_mon_ai_title", texts)}</h3><p {_t("tl_mon_ai_body", texts)}</p>'
        f'<p><a href="{esc(GUIDE_AI)}" rel="noopener" data-testid="tools-ai-guide" {_t("tl_link_ai", texts)}</a></p></div>'
        f'<div class="tl-box" data-testid="tools-quota"><h3 {_t("tl_mon_quota_title", texts)}</h3><p {_t("tl_mon_quota_body", texts)}</p>'
        f'<p><a href="{esc(GUIDE_QUOTA)}" rel="noopener" {_t("tl_link_quota", texts)}</a></p></div>'
        f'<div class="tl-box" data-testid="tools-next"><h3 {_t("tl_mon_next_title", texts)}</h3><p {_t("tl_mon_next_body", texts)}</p></div>'
        '</div></section>'
        f'<section class="card tl-card" data-testid="tools-updater"><header class="card-head"><h2 class="card-title">{esc(UPDATER)}</h2></header>'
        f'<p {_t("tl_upd_body", texts)}</p></section>')


CSS = r"""
  .eco-panel > section.card.tl-card { grid-column: span 12; }
  .tl-scroll { overflow-x: auto; }
  .tl-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .tl-table th, .tl-table td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }
  .tl-table thead th { font-size: 11.5px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }
  .tl-table td.num { font-variant-numeric: tabular-nums; }
  .tl-table th[scope="row"] { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 12px; overflow-wrap: anywhere; }
  .tl-links { white-space: normal; font-size: 12px; }
  .tl-ci-success { color: var(--ok, #2ea043); } .tl-ci-failure { color: var(--bad, #d1242f); font-weight: 600; } .tl-ci-pending { color: var(--warn, #b7791f); }
  .tl-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 8px; }
  .tl-box { border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; background: var(--panel-2); min-width: 0; }
  .tl-box h3 { margin: 0 0 6px; font-size: 13px; }
  .tl-box p { margin: 0 0 6px; font-size: 12.5px; overflow-wrap: anywhere; }
"""
