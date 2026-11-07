#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_evo_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The pieces of the dashboard that show the evidence checklist, the progress history, what changed since the last visit and the display modes.

Markup comes from this module; the tables, the line chart and the notices are drawn in the browser from the JSON the page already embeds
(see dashboard_evo.py), so the page makes no request of its own. The style sheet and the script are plain strings placed into the page as they are.
"""
from __future__ import annotations

from typing import Sequence

import dashboard_evo
import dashboard_evo_texts
from dashboard_charts import esc

EN = dashboard_evo_texts.TEXTS["en"]
ECOSYSTEM_CHIPS: tuple[tuple[str, str, str], ...] = (
    ("hydra-umc", "", "HYDRA-UMC"), ("urtc", "", "URTC"), ("armor", "", "A.R.M.O.R."), ("eh3d", "", "EH3D"), ("electro-hobby-3d", "scope_cross", "Cross-cutting"),
)


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def evidence_view() -> str:
    """The top of the evidence tab: filters, the counts per ecosystem and the table; the script fills the tables."""
    eco = ['<button type="button" class="chip" data-ev-eco="all" aria-pressed="true" data-testid="ev-eco-all"><span data-i18n="scope_all">All</span></button>']
    for key, i18n, text in ECOSYSTEM_CHIPS:
        label = f'<span data-i18n="{i18n}">{esc(text)}</span>' if i18n else f"<span>{esc(text)}</span>"
        eco.append(f'<button type="button" class="chip" data-ev-eco="{key}" aria-pressed="false" data-testid="ev-eco-{key}">{label}</button>')
    missing = "".join(
        f'<button type="button" class="chip" data-ev-missing="{item}" aria-pressed="false" data-testid="ev-missing-{item}"><span data-i18n="ev_item_{item}">{esc(EN["ev_item_" + item])}</span></button>'
        for item in dashboard_evo.ITEMS)
    return (
        '<section class="card ev-view" id="evidence-view" aria-labelledby="ev-title" data-testid="evidence-view">'
        f'<header class="card-head"><h2 class="card-title" id="ev-title" {_t("ev_title")}</h2></header>'
        f'<p class="muted" {_t("ev_hint")}</p><p class="muted" {_t("ev_signed_note")}</p>'
        '<div class="ev-controls" id="ev-controls">'
        '<div class="ev-group" role="group" aria-labelledby="ev-eco-t"><span class="scope-title" id="ev-eco-t" data-i18n="filter_ecosystem">Ecosystem</span>'
        f'<span class="chip-row">{"".join(eco)}</span></div>'
        f'<div class="ev-group" role="group" aria-labelledby="ev-miss-t"><span class="scope-title" id="ev-miss-t" {_t("ev_filter_missing")}</span>'
        f'<span class="chip-row">{missing}'
        f'<button type="button" class="chip" data-ev-unverified="1" aria-pressed="false" data-testid="ev-unverified"><span data-i18n="ev_filter_unverified">{esc(EN["ev_filter_unverified"])}</span></button></span></div>'
        f'<button type="button" class="btn btn-ghost" id="ev-reset" data-testid="ev-reset" {_t("ev_reset")}</button>'
        '</div>'
        f'<h3 class="ev-sub" {_t("ev_counts_title")}</h3>'
        '<div class="ev-counts-wrap" tabindex="0" role="region" aria-labelledby="ev-title"><table class="ev-counts" id="ev-counts" data-testid="ev-counts"><thead><tr><th scope="col" data-i18n="ev_col_repo">Repository</th></tr></thead></table></div>'
        '<p class="matches" id="ev-matches" aria-live="polite" data-testid="ev-matches"></p>'
        '<div class="ev-table-wrap" tabindex="0" role="region" aria-labelledby="ev-title" data-testid="ev-table-wrap"><table class="ev-table" id="ev-table" data-testid="ev-table"><thead><tr><th scope="col" data-i18n="ev_col_repo">Repository</th></tr></thead></table></div>'
        f'<p class="no-data" id="ev-none" data-testid="ev-none" hidden {_t("ev_none")}</p>'
        f'<p class="no-data" id="ev-no-checks" data-testid="ev-no-checks" hidden {_t("ev_no_checks")}</p>'
        '</section>'
    )


def panel_evidence() -> str:
    """The checklist inside the side panel of a repository."""
    return (f'<section aria-labelledby="rp-ev-t"><h3 id="rp-ev-t" {_t("ev_title")}</h3>'
            '<ul class="ev-list" id="rp-ev" data-testid="repo-evidence"></ul></section>')


def history_card() -> str:
    metrics = '<option value="overall" data-i18n="evo_metric_overall">Overall progress</option>' + "".join(
        f'<option value="{a}" data-i18n="area_{a}">{a}</option>' for a in ("software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production"))
    return (
        '<section class="card card-evo" id="evo-card" aria-labelledby="evo-title" data-testid="evo-card">'
        f'<header class="card-head"><h2 class="card-title" id="evo-title" {_t("evo_title")}</h2>'
        '<div class="evo-controls">'
        f'<div class="ev-group" role="group" aria-labelledby="evo-period-t"><span class="scope-title" id="evo-period-t" {_t("evo_period")}</span>'
        f'<button type="button" class="chip" data-evo-days="30" aria-pressed="false" data-testid="evo-30"><span {_t("evo_range_30")}</span></button>'
        f'<button type="button" class="chip" data-evo-days="90" aria-pressed="true" data-testid="evo-90"><span {_t("evo_range_90")}</span></button></div>'
        f'<div class="ev-group"><label class="scope-title" for="evo-metric" {_t("evo_measure")}</label>'
        f'<select id="evo-metric" data-testid="evo-metric">{metrics}</select></div></div></header>'
        f'<p class="muted" {_t("evo_hint")}</p>'
        '<figure class="evo-figure" id="evo-figure" data-testid="evo-figure"><svg class="evo-svg" id="evo-svg" role="img" aria-label="Progress over time" data-i18n-aria-label="evo_title" viewBox="0 0 900 280" preserveAspectRatio="xMidYMid meet" hidden></svg>'
        '<ul class="legend evo-legend" id="evo-legend" hidden></ul>'
        '<div class="sr-only"><table id="evo-table" data-testid="evo-table"><thead><tr><th scope="col" data-i18n="evo_col_date">Date</th></tr></thead></table></div></figure>'
        '<p class="no-data" id="evo-msg" role="status" data-testid="evo-msg"></p>'
        '<p class="muted" id="evo-count" data-testid="evo-count"></p>'
        '</section>'
    )


def visit_card() -> str:
    return (
        '<section class="card card-visit" id="visit-card" aria-labelledby="visit-title" data-testid="visit-card" hidden>'
        f'<header class="card-head"><h2 class="card-title" id="visit-title" {_t("visit_title")}</h2>'
        f'<button type="button" class="btn btn-ghost" id="visit-dismiss" data-testid="visit-dismiss" {_t("visit_dismiss")}</button></header>'
        '<p class="muted" id="visit-since" data-testid="visit-since"></p>'
        '<ul class="visit-list" id="visit-list" data-testid="visit-list"></ul>'
        '<p class="muted" id="visit-more" data-testid="visit-more"></p>'
        '<p class="muted" id="visit-none" data-testid="visit-none" hidden></p>'
        '</section>'
    )


def mode_buttons() -> str:
    return (
        '<div class="modes" role="group" aria-label="Display modes" data-i18n-aria-label="mode_group">'
        f'<button type="button" class="btn btn-ghost btn-mode" id="mode-compact" aria-pressed="false" data-testid="mode-compact" title="{esc(EN["mode_compact_title"])}" data-i18n-title="mode_compact_title"><span {_t("mode_compact")}</span></button>'
        f'<button type="button" class="btn btn-ghost btn-mode" id="mode-present" aria-pressed="false" data-testid="mode-present" title="{esc(EN["mode_present_title"])}" data-i18n-title="mode_present_title"><span id="mode-present-label" {_t("mode_present")}</span></button>'
        f'<button type="button" class="btn btn-ghost btn-mode" id="mode-print" data-testid="mode-print" title="{esc(EN["mode_print_title"])}" data-i18n-title="mode_print_title"><span {_t("mode_print")}</span></button>'
        '</div>'
    )


def print_header() -> str:
    """Shown only when printing: the title and the date of the data (filled by the script)."""
    return ('<div class="print-head" id="print-head" data-testid="print-head"><p class="print-title" id="print-title" data-i18n="print_title">Ecosystem status report</p>'
            '<p id="print-data"></p><p id="print-when"></p></div>')


def head_tags(total: int, description: str, site_url: str) -> str:
    """Icon and the cards of social networks (Open Graph and Twitter), with the small image written next to the page."""
    image = f"{site_url}og-image.png"
    title = "Electro Hobby 3D - Ecosystem Status"
    return "\n".join([
        f'<link rel="icon" type="image/svg+xml" href="{dashboard_evo.favicon_data_uri()}">',
        '<meta name="theme-color" content="#0f1420">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="Electro Hobby 3D">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{esc(site_url)}">',
        f'<meta property="og:image" content="{esc(image)}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="One bar per ecosystem, as long as its progress">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(description)}">',
        f'<meta name="twitter:image" content="{esc(image)}">',
    ])


CSS = r"""
  /* ======================= Evidence, history, last visit and modes ======================= */
  .ev-view, .card-evo, .card-visit { margin-bottom: 14px; }
  .card-evo, .card-visit { grid-column: span 12; margin-bottom: 0; }
  .ev-controls { display: flex; flex-wrap: wrap; gap: 10px 22px; align-items: center; margin: 10px 0; }
  .ev-group { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
  .ev-sub { font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--dim); margin: 12px 0 6px; }
  .ev-counts-wrap, .ev-table-wrap { overflow: auto; max-width: 100%; position: relative; }
  .ev-table-wrap { max-height: 46vh; border: 1px solid var(--border); border-radius: 10px; }
  .ev-counts, .ev-table { border-collapse: collapse; width: 100%; font-size: 12.5px; font-variant-numeric: tabular-nums; }
  .ev-counts th, .ev-counts td, .ev-table th, .ev-table td { padding: 5px 8px; border-bottom: 1px solid var(--border); text-align: center; white-space: nowrap; }
  .ev-counts th:first-child, .ev-table th:first-child, .ev-table td.ev-eco-cell { text-align: left; }
  .ev-table thead th { position: sticky; top: 0; background: var(--panel-2); z-index: 1; }
  .ev-counts small { color: var(--dim); margin-left: 4px; }
  .ev-cell { font-weight: 700; }
  .ev-st { display: inline-flex; align-items: center; justify-content: center; min-width: 24px; height: 22px; border-radius: 6px; border: 1px solid currentColor; font-size: 13px; line-height: 1; padding: 0 4px; }
  .ev-present { color: var(--k-pending, var(--warn-ink)); border-style: dotted; } .ev-invalid { color: var(--err); border-style: double; font-weight: 700; } .ev-yes { color: var(--ok); } .ev-no { color: var(--err); } .ev-unverified { color: var(--dim); border-style: dashed; } .ev-na { color: var(--dim); border-color: transparent; }
  .ev-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .ev-list li { display: flex; gap: 8px; align-items: center; justify-content: space-between; font-size: 13px; }
  .ev-legend { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 8px 0 0; padding: 0; list-style: none; font-size: 12px; color: var(--dim); }

  .evo-controls { display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: center; }
  .evo-controls select { background: var(--bg); color: var(--text); border: 1px solid var(--border-strong); border-radius: 8px; padding: 6px 8px; }
  .evo-svg { width: 100%; max-width: 1100px; height: auto; display: block; margin: 0 auto; }
  .evo-svg[hidden], .evo-legend[hidden] { display: none; }
  .evo-grid { stroke: var(--border); stroke-width: 1; }
  .evo-axis-text { fill: var(--dim); font-size: 11px; font-family: "IBM Plex Mono", ui-monospace, monospace; }
  .evo-end-label { font-size: 11.5px; font-weight: 700; font-family: "IBM Plex Sans", system-ui, sans-serif; }
  .evo-line { fill: none; stroke-width: 2.6; stroke-linejoin: round; stroke-linecap: round; }
  .evo-mark { stroke: var(--panel); stroke-width: 1.2; }
  .evo-s-hydra-umc { stroke: var(--c-hydra-umc); fill: var(--c-hydra-umc); } .evo-s-urtc { stroke: var(--c-urtc); fill: var(--c-urtc); }
  .evo-s-armor { stroke: var(--c-armor); fill: var(--c-armor); } .evo-s-eh3d { stroke: var(--c-eh3d); fill: var(--c-eh3d); }
  .evo-line.evo-s-hydra-umc, .evo-line.evo-s-urtc, .evo-line.evo-s-armor, .evo-line.evo-s-eh3d { fill: none; }
  text.evo-end-label.evo-s-hydra-umc, text.evo-end-label.evo-s-urtc, text.evo-end-label.evo-s-armor, text.evo-end-label.evo-s-eh3d { stroke: none; }
  .evo-legend { display: flex; flex-wrap: wrap; gap: 6px 18px; list-style: none; margin: 6px 0 0; padding: 0; font-size: 12px; }
  .evo-legend svg { width: 16px; height: 12px; vertical-align: -1px; margin-right: 5px; }
  .visit-list { margin: 6px 0; padding-left: 18px; font-size: 13px; columns: 2 380px; }
  @media (prefers-reduced-motion: no-preference) {
    .evo-line { stroke-dasharray: 1; stroke-dashoffset: 1; animation: evo-draw .9s ease-out .1s forwards; }
    .evo-mark { opacity: 0; animation: evo-fade .4s ease-out .8s forwards; }
    @keyframes evo-draw { to { stroke-dashoffset: 0; } }
    @keyframes evo-fade { to { opacity: 1; } }
  }

  .modes { display: inline-flex; gap: 4px; }
  .btn-mode { padding: 5px 9px; font-size: 12px; }
  .btn-mode[aria-pressed="true"] { background: var(--accent); color: #fff !important; border-color: var(--accent); }
  :root[data-theme="dark"] .btn-mode[aria-pressed="true"], :root:not([data-theme="light"]) .btn-mode[aria-pressed="true"] { color: #08111f !important; }
  .print-head { display: none; }

  /* Compact mode: a denser layout of the same content. */
  html[data-density="compact"] .panel { padding: 8px 12px 12px; }
  html[data-density="compact"] .card { padding: 8px 10px; }
  html[data-density="compact"] .summary-grid, html[data-density="compact"] .eco-panel { gap: 8px; }
  html[data-density="compact"] .card-title { margin-bottom: 4px; font-size: 12.5px; }
  html[data-density="compact"] .areas { gap: 3px; }
  html[data-density="compact"] .area { font-size: 11.5px; }
  html[data-density="compact"] .kpi { padding: 6px 10px; }
  html[data-density="compact"] .kpi-number { font-size: 22px; }
  html[data-density="compact"] .sidebar { padding: 8px 10px 12px; }
  html[data-density="compact"] .side-group { margin-top: 8px; }
  html[data-density="compact"] .tab { padding: 5px 10px; }
  html[data-density="compact"] .topbar { padding: 4px 14px; }
  html[data-density="compact"] td, html[data-density="compact"] th { padding-top: 2px !important; padding-bottom: 2px !important; }

  /* Presentation mode: no side panel, larger text. */
  html[data-mode="present"] .app { grid-template-columns: minmax(0, 1fr); grid-template-areas: "top" "main" "foot"; }
  html[data-mode="present"] .sidebar, html[data-mode="present"] .app-footer, html[data-mode="present"] .build-badge, html[data-mode="present"] .repo-panel { display: none !important; }
  html[data-mode="present"] main.content { zoom: 1.22; }
  html[data-mode="present"] .tab { font-size: 15px; padding: 9px 16px; }
  html[data-mode="present"] #mode-compact, html[data-mode="present"] #mode-print { display: none; }
  html[data-mode="present"] .brand h1 { font-size: 20px; }

  @media (max-width: 1100px) { .btn-mode { padding: 4px 7px; } }
  @media (max-width: 760px) { .modes #mode-print, .modes #mode-compact { display: none; } }

  /* Print: a clean report of the status. */
  @media print {
    @page { margin: 12mm; }
    :root, :root[data-theme] {
      --bg: #fff; --surface: #fff; --surface-2: #f1f3f6; --panel: #fff; --panel-2: #f1f3f6; --border: #c7ccd6; --border-strong: #8b93a3; --text: #111827; --dim: #374151;
      --accent: #1d4ed8; --ok: #166534; --err: #b91c1c; --shadow: none; --bg-texture: transparent;
      --c-hydra-umc: #1d6fd6; --c-urtc: #7c4dd6; --c-armor: #0f8f68; --c-eh3d: #b45f06;
    }
    html, body { height: auto !important; background: #fff !important; color: #111827 !important; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .app { display: block !important; height: auto !important; overflow: visible !important; }
    .skip-link, .tabs, .top-actions, .sidebar, .app-footer, .repo-panel, .scope, .pager, .filters-toggle, .ev-controls, .evo-controls, .card-visit,
    .btn, .area-caret, .contrib, #panel-projects, #panel-inventory, #panel-architecture, .chart-tip, [data-show-eco] { display: none !important; }
    .topbar { display: block !important; border: 0 !important; padding: 0 !important; background: none !important; }
    .brand { display: none !important; }
    .print-head { display: block !important; margin-bottom: 10px; border-bottom: 2px solid #111827; padding-bottom: 6px; }
    .print-head .print-title { font-size: 20px; font-weight: 700; margin: 0 0 4px; } .print-head p { margin: 0; font-size: 12px; }
    main.content { overflow: visible !important; }
    .panel, .panel[hidden] { display: block !important; height: auto !important; overflow: visible !important; padding: 0 !important; break-before: page; }
    #panel-summary { break-before: auto; }
    .card { box-shadow: none !important; break-inside: avoid; }
    .summary-grid, .eco-panel { display: block !important; }
    .summary-grid > *, .eco-panel > * { margin-bottom: 8px; }
    .alerts-scroll, .ev-table-wrap, .ev-counts-wrap, .table-wrapper { max-height: none !important; overflow: visible !important; }
    .evo-line, .evo-mark { animation: none !important; stroke-dashoffset: 0 !important; opacity: 1 !important; }
    a { color: inherit !important; text-decoration: none !important; }
  }
"""

JS = r"""
  // ---------------- Evidence checklist, history, last visit and display modes ----------------
  // Everything here is drawn from the JSON embedded in the page; no request leaves the browser. A fact that is not in the data is printed as "not verified".
  const EV_ITEMS = ["tests", "ci", "release", "signed", "docs", "sim", "hw"];
  const EV_ECOS = ["hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"];
  const EV_GLYPH = { yes: "✓", no: "✕", unverified: "?", na: "–", present: "◐", invalid: "⚠" };
  const CHECKS = (DATA.checks && typeof DATA.checks === "object") ? DATA.checks : {};
  const evState = { eco: "all", missing: [], unverified: false };
  const evAll = document.getElementById("ev-table");
  const evCounts = document.getElementById("ev-counts");

  function evStatus(value) { return value === 1 || value === 4 ? "yes" : value === 0 ? "no" : value === 2 ? "na" : value === 3 ? "present" : value === 5 ? "invalid" : "unverified"; }
  function evMark(status, dict, itemKey) {
    const cell = make("span", "ev-st ev-" + status);
    cell.appendChild(make("span", "", EV_GLYPH[status])).setAttribute("aria-hidden", "true");
    cell.appendChild(make("span", "sr-only", dict["ev_st_" + status] + (itemKey ? ": " + dict["ev_item_" + itemKey] : "")));
    cell.title = dict["ev_st_" + status];
    return cell;
  }
  function evNames() {
    return Object.keys(CHECKS).sort(function (a, b) { return a.toLowerCase() < b.toLowerCase() ? -1 : 1; });
  }
  function evRepoEco(name) { return (DATA.repos[name] && DATA.repos[name].eco) || ""; }
  function evMatches(name) {
    if (evState.eco !== "all" && evRepoEco(name) !== evState.eco) { return false; }
    const row = CHECKS[name];
    for (let i = 0; i < evState.missing.length; i++) {
      if (row[EV_ITEMS.indexOf(evState.missing[i])] !== 0) { return false; }
    }
    if (evState.unverified && !row.some(function (v) { return v === null; })) { return false; }
    return true;
  }
  function evSyncChips() {
    document.querySelectorAll("[data-ev-eco]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-ev-eco") === evState.eco ? "true" : "false"); });
    document.querySelectorAll("[data-ev-missing]").forEach(function (b) { b.setAttribute("aria-pressed", evState.missing.indexOf(b.getAttribute("data-ev-missing")) >= 0 ? "true" : "false"); });
    const u = document.querySelector("[data-ev-unverified]");
    if (u) { u.setAttribute("aria-pressed", evState.unverified ? "true" : "false"); }
  }
  function evRender(dict) {
    const names = evNames();
    const none = document.getElementById("ev-no-checks");
    document.getElementById("ev-controls").hidden = names.length === 0;
    none.hidden = names.length > 0;
    evCounts.hidden = evAll.hidden = names.length === 0;
    evCounts.textContent = "";
    evAll.textContent = "";
    if (!names.length) { document.getElementById("ev-matches").textContent = ""; document.getElementById("ev-none").hidden = true; return; }
    evSyncChips();
    // Counts per ecosystem
    const head = make("thead"); const hr = make("tr");
    hr.appendChild(make("th", "", dict.filter_ecosystem)).setAttribute("scope", "col");
    EV_ITEMS.forEach(function (item) { hr.appendChild(make("th", "", dict["ev_item_" + item])).setAttribute("scope", "col"); });
    head.appendChild(hr); evCounts.appendChild(head);
    const body = make("tbody");
    EV_ECOS.forEach(function (eco) {
      const members = names.filter(function (n) { return evRepoEco(n) === eco; });
      if (!members.length) { return; }
      const tr = make("tr"); tr.setAttribute("data-eco", eco);
      const label = (DATA.repos[members[0]] || {}).ecoLabel || eco;
      tr.appendChild(make("th", "", label)).setAttribute("scope", "row");
      EV_ITEMS.forEach(function (item, index) {
        const tally = { yes: 0, no: 0, unverified: 0, na: 0, present: 0, invalid: 0 };
        members.forEach(function (n) { tally[evStatus(CHECKS[n][index])] += 1; });
        const td = make("td"); td.setAttribute("data-item", item);
        const applicable = members.length - tally.na;
        td.appendChild(make("span", "", tally.yes + "/" + applicable));
        if (tally.unverified) { const s = make("small", "", "?" + tally.unverified); s.setAttribute("aria-hidden", "true"); td.appendChild(s); }
        if (tally.present) { const s = make("small", "", "◐" + tally.present); s.setAttribute("aria-hidden", "true"); td.appendChild(s); }
        if (tally.invalid) { const s = make("small", "", "⚠" + tally.invalid); s.setAttribute("aria-hidden", "true"); td.appendChild(s); }
        td.appendChild(make("span", "sr-only", tpl(dict.ev_count_sr, { yes: tally.yes, no: tally.no, unv: tally.unverified, na: tally.na })));
        td.title = tpl(dict.ev_count_sr, { yes: tally.yes, no: tally.no, unv: tally.unverified, na: tally.na });
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    evCounts.appendChild(body);
    // Checklist
    const cap = make("caption", "sr-only", dict.ev_table_caption); evAll.appendChild(cap);
    const th = make("thead"); const hr2 = make("tr");
    hr2.appendChild(make("th", "", dict.ev_col_repo)).setAttribute("scope", "col");
    hr2.appendChild(make("th", "", dict.filter_ecosystem)).setAttribute("scope", "col");
    EV_ITEMS.forEach(function (item) { hr2.appendChild(make("th", "", dict["ev_item_" + item])).setAttribute("scope", "col"); });
    th.appendChild(hr2); evAll.appendChild(th);
    const tb = make("tbody");
    let shown = 0;
    names.forEach(function (name) {
      if (!evMatches(name)) { return; }
      shown += 1;
      const tr = make("tr"); tr.setAttribute("data-repo", name);
      const first = make("th"); first.setAttribute("scope", "row");
      const open = make("button", "link-btn", name); open.type = "button";
      open.setAttribute("aria-label", tpl(dict.ev_open_aria, { name: name }));
      open.addEventListener("click", function () { openPanel(name, open); });
      first.appendChild(open); tr.appendChild(first);
      tr.appendChild(make("td", "ev-eco-cell", (DATA.repos[name] || {}).ecoLabel || dict.not_verified));
      CHECKS[name].forEach(function (value, index) {
        const status = evStatus(value);
        const td = make("td", "ev-cell"); td.setAttribute("data-item", EV_ITEMS[index]); td.setAttribute("data-status", status);
        td.appendChild(status === "no" || status === "unverified" || status === "present" || status === "invalid" || (status === "yes" && EV_ITEMS[index] === "signed" && value === 4) ? deliveryWhyButton(name, EV_ITEMS[index], status, dict) : evMark(status, dict, EV_ITEMS[index]));
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    evAll.appendChild(tb);
    const counter = document.getElementById("ev-matches");
    counter.textContent = tpl(dict.ev_matches, { shown: shown, total: names.length });
    counter.setAttribute("data-shown", String(shown)); counter.setAttribute("data-total", String(names.length));
    document.getElementById("ev-none").hidden = shown > 0;
    evAll.hidden = shown === 0;
    deliveryEvidence(dict, names);
    // Legend (text and glyph, never colour alone)
    let legend = document.getElementById("ev-legend");
    if (!legend) { legend = make("ul", "ev-legend"); legend.id = "ev-legend"; document.getElementById("ev-matches").after(legend); }
    legend.textContent = "";
    ["yes", "present", "invalid", "no", "unverified", "na"].forEach(function (status) {
      const li = make("li"); const mark = evMark(status, dict, null); mark.querySelector(".sr-only").remove(); li.appendChild(mark);
      li.appendChild(make("span", "", " " + dict["ev_st_" + status])); legend.appendChild(li);
    });
  }
  document.querySelectorAll("[data-ev-eco]").forEach(function (b) { b.addEventListener("click", function () { evState.eco = b.getAttribute("data-ev-eco"); evRender(currentDict()); }); });
  document.querySelectorAll("[data-ev-missing]").forEach(function (b) {
    b.addEventListener("click", function () {
      const key = b.getAttribute("data-ev-missing"); const at = evState.missing.indexOf(key);
      if (at >= 0) { evState.missing.splice(at, 1); } else { evState.missing.push(key); }
      evRender(currentDict());
    });
  });
  const evUnverifiedButton = document.querySelector("[data-ev-unverified]");
  if (evUnverifiedButton) { evUnverifiedButton.addEventListener("click", function () { evState.unverified = !evState.unverified; evRender(currentDict()); }); }
  const evResetButton = document.getElementById("ev-reset");
  if (evResetButton) { evResetButton.addEventListener("click", function () { evState.eco = "all"; evState.missing = []; evState.unverified = false; evRender(currentDict()); }); }

  function evPanel(name, dict) {
    const list = document.getElementById("rp-ev");
    if (!list) { return; }
    list.textContent = "";
    const row = CHECKS[name];
    EV_ITEMS.forEach(function (item, index) {
      const li = make("li"); li.setAttribute("data-item", item);
      li.appendChild(make("span", "", dict["ev_item_" + item]));
      li.appendChild(evMark(row ? evStatus(row[index]) : "unverified", dict, null));
      list.appendChild(li);
    });
  }

  // ---------------- Progress history ----------------
  const HIST = Array.isArray(DATA.history) ? DATA.history : [];
  const EVO_ECOS = ["hydra-umc", "urtc", "armor", "eh3d"];
  const EVO_LABEL = { "hydra-umc": "HYDRA-UMC", urtc: "URTC", armor: "A.R.M.O.R.", eh3d: "EH3D" };
  const evoState = { days: 90, metric: "overall" };
  const SVGNS = "http://www.w3.org/2000/svg";
  function svgEl(name, attrs, text) {
    const el = document.createElementNS(SVGNS, name);
    Object.keys(attrs || {}).forEach(function (k) { el.setAttribute(k, attrs[k]); });
    if (text !== undefined) { el.textContent = text; }
    return el;
  }
  function setHidden(el, on) { if (on) { el.setAttribute("hidden", ""); } else { el.removeAttribute("hidden"); } }
  function evoValue(entry, eco, metric) {
    const v = metric === "overall" ? (entry.progress || {})[eco] : ((entry.areas || {})[eco] || {})[metric];
    return typeof v === "number" ? v : null;
  }
  function dayNumber(iso) { return Math.floor(Date.parse(iso + "T00:00:00Z") / 86400000); }
  function marker(kind, x, y, cls, title) {
    let el;
    if (kind === 0) { el = svgEl("circle", { cx: x, cy: y, r: 3.4 }); }
    else if (kind === 1) { el = svgEl("rect", { x: x - 3.2, y: y - 3.2, width: 6.4, height: 6.4 }); }
    else if (kind === 2) { el = svgEl("polygon", { points: (x - 4) + "," + (y + 3.4) + " " + (x + 4) + "," + (y + 3.4) + " " + x + "," + (y - 4) }); }
    else { el = svgEl("polygon", { points: x + "," + (y - 4.4) + " " + (x + 4.2) + "," + y + " " + x + "," + (y + 4.4) + " " + (x - 4.2) + "," + y }); }
    el.setAttribute("class", "evo-mark " + cls);
    el.appendChild(svgEl("title", {}, title));
    return el;
  }
  function evoRender(dict) {
    const svg = document.getElementById("evo-svg");
    const legend = document.getElementById("evo-legend");
    const msg = document.getElementById("evo-msg");
    const table = document.getElementById("evo-table");
    const count = document.getElementById("evo-count");
    if (!svg) { return; }
    const sel = document.getElementById("evo-metric");
    sel.querySelectorAll("option").forEach(function (o) { o.textContent = o.value === "overall" ? dict.evo_metric_overall : dict["area_" + o.value]; });
    document.querySelectorAll("[data-evo-days]").forEach(function (b) { b.setAttribute("aria-pressed", Number(b.getAttribute("data-evo-days")) === evoState.days ? "true" : "false"); });
    svg.textContent = ""; legend.textContent = ""; table.textContent = ""; count.textContent = "";
    const entries = HIST.slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; });
    setHidden(svg, true); setHidden(legend, true);
    if (!entries.length) { msg.textContent = dict.evo_no_history; msg.hidden = false; return; }
    const endDay = dayNumber(entries[entries.length - 1].date);
    const startDay = endDay - (evoState.days - 1);
    const view = entries.filter(function (e) { return dayNumber(e.date) >= startDay; });
    const metricName = evoState.metric === "overall" ? dict.evo_metric_overall : dict["area_" + evoState.metric];
    count.textContent = tpl(dict.evo_snapshots, { n: view.length });
    // Accessible table (always present, hidden from sight)
    table.appendChild(make("caption", "", tpl(dict.evo_chart_desc, { metric: metricName, days: evoState.days, first: view[0].date, last: view[view.length - 1].date })));
    const hr = make("tr"); hr.appendChild(make("th", "", dict.evo_col_date)).setAttribute("scope", "col");
    EVO_ECOS.forEach(function (eco) { hr.appendChild(make("th", "", EVO_LABEL[eco])).setAttribute("scope", "col"); });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const tbody = make("tbody");
    view.forEach(function (e) {
      const tr = make("tr"); tr.appendChild(make("th", "", e.date)).setAttribute("scope", "row");
      EVO_ECOS.forEach(function (eco) { const v = evoValue(e, eco, evoState.metric); tr.appendChild(make("td", "", v === null ? dict.evo_unknown_value : v + "%")); });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    if (view.length < 2) { msg.textContent = tpl(dict.evo_one_point, { date: view[0].date }); msg.hidden = false; return; }
    msg.hidden = true; msg.textContent = "";
    // Chart
    const W = 900, H = 280, L = 42, R = 110, T = 14, B = 30;
    const firstDay = dayNumber(view[0].date);
    const px = function (iso) { return L + (dayNumber(iso) - firstDay) / Math.max(1, endDay - firstDay) * (W - L - R); };
    const py = function (v) { return T + (100 - v) / 100 * (H - T - B); };
    svg.setAttribute("aria-label", tpl(dict.evo_chart_desc, { metric: metricName, days: evoState.days, first: view[0].date, last: view[view.length - 1].date }));
    [0, 25, 50, 75, 100].forEach(function (v) {
      svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: py(v), y2: py(v), class: "evo-grid" }));
      svg.appendChild(svgEl("text", { x: L - 6, y: py(v) + 4, "text-anchor": "end", class: "evo-axis-text" }, v + "%"));
    });
    [[view[0].date, "start"], [view[view.length - 1].date, "end"]].forEach(function (pair) {
      svg.appendChild(svgEl("text", { x: pair[1] === "start" ? L : W - R, y: H - 8, "text-anchor": pair[1], class: "evo-axis-text" }, pair[0]));
    });
    const ends = [];
    EVO_ECOS.forEach(function (eco, kind) {
      const cls = "evo-s-" + eco;
      let segment = [];
      const flush = function () {
        if (segment.length > 1) { svg.appendChild(svgEl("path", { d: "M" + segment.join(" L"), class: "evo-line " + cls, pathLength: 1 })); }
        segment = [];
      };
      let last = null;
      let prevDay = null;
      view.forEach(function (e) {
        const v = evoValue(e, eco, evoState.metric);
        if (v === null) { flush(); prevDay = null; return; }
        // A day without a snapshot breaks the line: nothing is drawn for the days that were not recorded.
        if (prevDay !== null && dayNumber(e.date) - prevDay > 1) { flush(); }
        prevDay = dayNumber(e.date);
        segment.push(px(e.date).toFixed(1) + "," + py(v).toFixed(1));
        last = { x: px(e.date), y: py(v), v: v, date: e.date };
      });
      flush();
      view.forEach(function (e, i) {
        const v = evoValue(e, eco, evoState.metric);
        const near = function (j) { return j >= 0 && j < view.length && evoValue(view[j], eco, evoState.metric) !== null && Math.abs(dayNumber(view[j].date) - dayNumber(e.date)) === 1; };
        const alone = v !== null && !near(i - 1) && !near(i + 1);
        if (v !== null && (alone || view.length <= 31 || i === view.length - 1 || (i % 7 === 0 && view.length - 1 - i >= 4))) { svg.appendChild(marker(kind, px(e.date), py(v), cls, EVO_LABEL[eco] + " · " + e.date + " · " + v + "%")); }
      });
      if (last) { ends.push({ eco: eco, y: last.y, v: last.v }); }
    });
    ends.sort(function (a, b) { return a.y - b.y; });
    for (let i = 1; i < ends.length; i++) { if (ends[i].y - ends[i - 1].y < 13) { ends[i].y = ends[i - 1].y + 13; } }
    ends.forEach(function (end) {
      svg.appendChild(svgEl("text", { x: W - R + 6, y: end.y + 4, class: "evo-end-label evo-s-" + end.eco }, EVO_LABEL[end.eco] + " " + end.v + "%"));
    });
    EVO_ECOS.forEach(function (eco, kind) {
      const li = make("li"); const key = svgEl("svg", { viewBox: "0 0 16 12", "aria-hidden": "true" });
      key.appendChild(svgEl("line", { x1: 0, x2: 16, y1: 6, y2: 6, class: "evo-line evo-s-" + eco, style: "animation:none;stroke-dasharray:none;stroke-dashoffset:0" }));
      key.appendChild(marker(kind, 8, 6, "evo-s-" + eco, EVO_LABEL[eco]));
      li.appendChild(key); li.appendChild(make("span", "", EVO_LABEL[eco])); legend.appendChild(li);
    });
    setHidden(svg, false); setHidden(legend, false);
  }
  document.querySelectorAll("[data-evo-days]").forEach(function (b) { b.addEventListener("click", function () { evoState.days = Number(b.getAttribute("data-evo-days")); evoRender(currentDict()); }); });
  const evoMetric = document.getElementById("evo-metric");
  if (evoMetric) { evoMetric.addEventListener("change", function () { evoState.metric = evoMetric.value; evoRender(currentDict()); }); }

  // ---------------- What changed since the last visit ----------------
  const VISIT_KEY = "hydra-dashboard-visit";
  const VISIT_SESSION = "hydra-dashboard-visit-diff";
  const SNAP = DATA.snap && typeof DATA.snap === "object" ? DATA.snap : null;
  const AREA_LIST = ["software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production"];
  let visit = null;
  let visitDismissed = false;
  function flatten(snap) {
    const out = {};
    EVO_ECOS.forEach(function (eco) {
      if (typeof (snap.progress || {})[eco] === "number") { out[eco + "|overall"] = snap.progress[eco]; }
      AREA_LIST.forEach(function (a) { const v = ((snap.areas || {})[eco] || {})[a]; if (typeof v === "number") { out[eco + "|" + a] = v; } });
    });
    return out;
  }
  function computeVisit() {
    if (!SNAP) { return null; }
    const now = flatten(SNAP);
    try { const cached = sessionStorage.getItem(VISIT_SESSION); if (cached) { return JSON.parse(cached); } } catch (e) { /* no session storage */ }
    let stored = null;
    try { stored = JSON.parse(localStorage.getItem(VISIT_KEY) || "null"); } catch (e) { return null; }
    let result = null;
    if (stored && typeof stored === "object" && stored.values && typeof stored.visited === "string") {
      const changes = [];
      Object.keys(now).forEach(function (key) {
        if (typeof stored.values[key] === "number" && stored.values[key] !== now[key]) { changes.push({ key: key, from: stored.values[key], to: now[key] }); }
      });
      result = { since: stored.visited, changes: changes };
    }
    try { localStorage.setItem(VISIT_KEY, JSON.stringify({ visited: new Date().toISOString().slice(0, 10), values: now })); } catch (e) { /* storage blocked */ }
    if (result) { try { sessionStorage.setItem(VISIT_SESSION, JSON.stringify(result)); } catch (e) { /* ignored */ } }
    return result;
  }
  function visitRender(dict) {
    const card = document.getElementById("visit-card");
    if (!card) { return; }
    if (!visit || visitDismissed) { card.hidden = true; return; }
    card.hidden = false;
    document.getElementById("visit-since").textContent = tpl(dict.visit_since, { date: visit.since });
    const list = document.getElementById("visit-list");
    list.textContent = "";
    const none = document.getElementById("visit-none");
    const more = document.getElementById("visit-more");
    none.hidden = visit.changes.length > 0;
    none.textContent = dict.visit_none;
    more.textContent = visit.changes.length > 12 ? tpl(dict.visit_more, { n: visit.changes.length - 12 }) : "";
    visit.changes.slice(0, 12).forEach(function (c) {
      const parts = c.key.split("|");
      const delta = (c.to - c.from > 0 ? "+" : "") + (c.to - c.from);
      list.appendChild(make("li", "", tpl(dict.visit_item, { eco: EVO_LABEL[parts[0]], what: parts[1] === "overall" ? dict.evo_metric_overall : dict["area_" + parts[1]], from: c.from, to: c.to, delta: delta })));
    });
  }
  visit = computeVisit();
  const visitDismiss = document.getElementById("visit-dismiss");
  if (visitDismiss) { visitDismiss.addEventListener("click", function () { visitDismissed = true; visitRender(currentDict()); }); }

  // ---------------- Display modes: compact, presentation, print ----------------
  const MODE_KEY = "hydra-dashboard-modes";
  const rootEl = document.documentElement;
  const modeCompact = document.getElementById("mode-compact");
  const modePresent = document.getElementById("mode-present");
  const modePrint = document.getElementById("mode-print");
  let fullscreenAsked = false;
  try { const saved = JSON.parse(safeGet(MODE_KEY) || "null"); if (saved && saved.compact === true && !modes.fromHash) { modes.compact = true; } } catch (e) { /* ignored */ }
  function presentLabel(dict) {
    const label = document.getElementById("mode-present-label");
    if (label) { label.setAttribute("data-i18n", modes.present ? "mode_exit" : "mode_present"); label.textContent = modes.present ? dict.mode_exit : dict.mode_present; }
  }
  function applyModes(options) {
    options = options || {};
    if (modes.compact) { rootEl.setAttribute("data-density", "compact"); } else { rootEl.removeAttribute("data-density"); }
    if (modes.present) { rootEl.setAttribute("data-mode", "present"); } else { rootEl.removeAttribute("data-mode"); }
    if (modeCompact) { modeCompact.setAttribute("aria-pressed", modes.compact ? "true" : "false"); }
    if (modePresent) { modePresent.setAttribute("aria-pressed", modes.present ? "true" : "false"); }
    presentLabel(currentDict());
    safeSet(MODE_KEY, JSON.stringify({ compact: modes.compact }));
    if (options.write !== false && hashReady) { writeHash(); }
  }
  function setPresent(on, viaUser) {
    if (modes.present === on) { return; }
    modes.present = on;
    applyModes();
    try {
      if (on && viaUser && rootEl.requestFullscreen) { fullscreenAsked = true; const p = rootEl.requestFullscreen(); if (p && p.catch) { p.catch(function () { fullscreenAsked = false; }); } }
      else if (!on && document.fullscreenElement && document.exitFullscreen) { fullscreenAsked = false; const q = document.exitFullscreen(); if (q && q.catch) { q.catch(function () { /* ignored */ }); } }
    } catch (e) { /* fullscreen unavailable: the layout still changes */ }
  }
  if (modeCompact) { modeCompact.addEventListener("click", function () { modes.compact = !modes.compact; applyModes(); }); }
  if (modePresent) { modePresent.addEventListener("click", function () { setPresent(!modes.present, true); }); }
  if (modePrint) { modePrint.addEventListener("click", function () { window.print(); }); }
  document.addEventListener("keydown", function (event) {
    if (event.ctrlKey || event.altKey || event.metaKey) { return; }
    const target = event.target;
    const typing = target && target.closest && target.closest("input, select, textarea, [contenteditable='true']");
    if (event.key === "Escape") { if (modes.present && !event.defaultPrevented) { setPresent(false, true); } return; }
    if (typing || !shortcutsOn) { return; }
    if (event.key === "c" || event.key === "C") { modes.compact = !modes.compact; applyModes(); }
    else if (event.key === "p" || event.key === "P") { setPresent(!modes.present, true); }
  });
  document.addEventListener("fullscreenchange", function () { if (!document.fullscreenElement && modes.present && fullscreenAsked) { fullscreenAsked = false; setPresent(false, false); } });

  // ---------------- Print header ----------------
  function printRender(dict) {
    const data = document.getElementById("print-data");
    const when = document.getElementById("print-when");
    if (!data || !when) { return; }
    data.textContent = SNAP && SNAP.date ? tpl(dict.print_data_of, { date: SNAP.date }) : dict.print_data_unknown;
    when.textContent = tpl(dict.print_printed, { date: new Date().toISOString().slice(0, 10) });
  }
  window.addEventListener("beforeprint", function () { printRender(currentDict()); });

  function evoApplied(dict) {
    evRender(dict); ciRender(dict); tsRender(dict); cdRender(dict); scRender(dict); acRender(dict); snRender(dict); evoRender(dict); insightApplied(dict); visitRender(dict); printRender(dict); presentLabel(dict);
    if (panelFor) { evPanel(panelFor, dict); }
  }
  applyModes({ write: false });
"""
