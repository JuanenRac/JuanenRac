#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_code_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Code" of the dashboard: lines of code, tests and documentation per repository, ecosystem and type.

The markup is a frame; the figures, the charts and the table are drawn in the browser from the JSON the page already embeds (`code`, see dashboard_code.py),
so the page makes no request of its own. Every chart is plain SVG with no library, has a table with the same figures, is named for assistive technology,
shows its value in a tooltip on hover and on keyboard focus, and nothing relies on colour alone (values are printed, series have their own marker shape). The
motion stops with prefers-reduced-motion. The script is placed into the shell's own scope (it uses `DATA`, `make`, `tpl`, `svgEl`, `marker`, `dayNumber`,
`currentDict` and `openPanel`); `cdRender` is called by `evoApplied` whenever the language changes. Stdlib only.
"""
from __future__ import annotations

import dashboard_code_texts
from dashboard_charts import esc

EN = dashboard_code_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def _chart_card(ident: str, title_key: str, hint_key: str | None, body: str) -> str:
    hint = f'<p class="muted" {_t(hint_key)}</p>' if hint_key else ""
    return (f'<section class="card" aria-labelledby="{ident}-title"><header class="card-head"><h3 class="card-title" id="{ident}-title" {_t(title_key)}</h3></header>'
            f'{hint}{body}</section>')


def _alt_table(ident: str) -> str:
    return f'<div class="sr-only"><table id="{ident}" data-testid="{ident}"><thead><tr><th scope="col" data-i18n="cd_col_name">{esc(EN["cd_col_name"])}</th></tr></thead></table></div>'


def panel_html() -> str:
    legend = ('<ul class="cd-legend" id="cd-prop-legend" data-testid="cd-prop-legend">'
              + "".join(f'<li><span class="cd-swatch cd-c-{k}" aria-hidden="true"></span><span {_t("cd_series_" + k)}</span></li>' for k in ("code", "tests", "docs")) + '</ul>')
    return (
        '<section class="ins cd" id="cd-root" aria-labelledby="cd-title" data-testid="code-root">'
        f'<header class="ins-head"><h2 class="card-title" id="cd-title" {_t("cd_title")}</h2>'
        f'<span class="ts-badge" data-testid="cd-badge" {_t("cd_badge")}</span></header>'
        f'<p class="muted" {_t("cd_hint")}</p>'
        '<details class="ts-help" data-testid="cd-help">'
        f'<summary {_t("cd_help_summary")}</summary><p id="cd-help-body" data-testid="cd-help-body"></p></details>'
        '<p class="stale-banner" id="cd-stale" role="status" data-testid="cd-stale" hidden></p>'
        '<p class="muted" id="cd-note" role="status" data-testid="cd-note" hidden></p>'
        f'<p class="no-data" id="cd-not-read" data-testid="cd-not-read" hidden {_t("cd_not_read")}</p>'
        '<div id="cd-body" data-testid="cd-body">'
        '<ul class="ac-kpis cd-kpis" id="cd-kpis" data-testid="cd-kpis"></ul>'
        # 1. proportions
        + _chart_card("cd-prop", "cd_prop_title", "cd_prop_hint",
                      '<div class="cd-chart" id="cd-prop-chart" data-testid="cd-prop-chart"></div>' + legend + _alt_table("cd-prop-table"))
        # 2. languages
        + _chart_card("cd-lang", "cd_lang_title", "cd_lang_hint",
                      '<div class="cd-lang-grid"><div class="cd-chart" id="cd-lang-global" data-testid="cd-lang-global"></div>'
                      '<div class="cd-chart" id="cd-lang-eco" data-testid="cd-lang-eco"></div></div>'
                      '<ul class="cd-legend" id="cd-lang-legend" data-testid="cd-lang-legend"></ul>' + _alt_table("cd-lang-table"))
        # 3. evolution
        + _chart_card("cd-evo", "cd_evo_title", "cd_evo_hint",
                      '<p class="no-data" id="cd-evo-msg" data-testid="cd-evo-msg" role="status" hidden></p>'
                      '<div id="cd-evo-wrap" data-testid="cd-evo-wrap" hidden>'
                      f'<h4 class="cd-sub" {_t("cd_evo_total_title")}</h4><div class="cd-chart" id="cd-evo-total" data-testid="cd-evo-total"></div>'
                      '<ul class="cd-legend" id="cd-evo-total-legend" data-testid="cd-evo-total-legend"></ul>'
                      f'<div class="cd-sub-row"><h4 class="cd-sub" {_t("cd_evo_eco_title")}</h4>'
                      f'<span class="chip-row" id="cd-evo-metric" role="group" aria-label="{esc(EN["cd_evo_metric"])}" data-i18n-aria-label="cd_evo_metric" data-testid="cd-evo-metric"></span></div>'
                      '<div class="cd-chart" id="cd-evo-eco" data-testid="cd-evo-eco"></div>'
                      '<ul class="cd-legend" id="cd-evo-eco-legend" data-testid="cd-evo-eco-legend"></ul></div>' + _alt_table("cd-evo-table"))
        # 4. top N
        + _chart_card("cd-top", "cd_top_title", "cd_top_hint",
                      '<div class="ev-controls"><div class="ts-field"><label class="scope-title" for="cd-top-n" data-i18n="cd_top_n">How many</label>'
                      '<select id="cd-top-n" data-testid="cd-top-n"><option value="10">10</option><option value="20" selected>20</option><option value="30">30</option></select></div></div>'
                      '<div class="cd-chart" id="cd-top-chart" data-testid="cd-top-chart"></div>' + _alt_table("cd-top-table"))
        # 5. the table
        + '<section class="card" aria-labelledby="cd-table-title"><header class="card-head">'
        f'<h3 class="card-title" id="cd-table-title" {_t("cd_table_title")}</h3></header><p class="muted" {_t("cd_table_hint")}</p>'
        '<div class="ev-controls"><div class="ev-group" role="group" aria-labelledby="cd-eco-t">'
        f'<span class="scope-title" id="cd-eco-t" {_t("cd_filter_eco")}</span><span class="chip-row" id="cd-eco-chips" data-testid="cd-eco-chips"></span></div>'
        '<div class="ev-group" role="group" aria-labelledby="cd-type-t">'
        f'<span class="scope-title" id="cd-type-t" {_t("cd_filter_type")}</span><span class="chip-row" id="cd-type-chips" data-testid="cd-type-chips"></span></div>'
        '<div class="ts-field"><label class="scope-title" for="cd-group" data-i18n="cd_group">Group rows by</label><select id="cd-group" data-testid="cd-group"></select></div>'
        '<div class="ts-field"><label class="scope-title" for="cd-search" data-i18n="cd_search">Search a repository</label>'
        '<input type="search" id="cd-search" data-testid="cd-search" autocomplete="off" maxlength="80"></div></div>'
        '<p class="matches" id="cd-matches" aria-live="polite" data-testid="cd-matches"></p>'
        '<p class="sr-only" id="cd-live" role="status" data-testid="cd-live"></p>'
        '<div class="cd-table-wrap" id="cd-table-wrap" tabindex="0" role="region" aria-labelledby="cd-table-title" data-testid="cd-table-wrap">'
        '<table class="cd-table" id="cd-table" data-testid="cd-table"><thead><tr><th scope="col" data-i18n="cd_col_name">Repository</th></tr></thead></table></div>'
        f'<p class="no-data" id="cd-none" data-testid="cd-none" hidden {_t("cd_none")}</p></section>'
        '</div>'
        '<div class="cd-tip" id="cd-tip" role="tooltip" data-testid="cd-tip" hidden></div>'
        '</section>'
    )


CSS = r"""
  /* ======================= Code: lines of code, tests and documentation ======================= */
  :root {
    --cd-code: #5aa9ff; --cd-tests: #3ecf8e; --cd-docs: #f5b84b;
    --cd-l0: #56b4e9; --cd-l1: #e69f00; --cd-l2: #2fd0a0; --cd-l3: #e8db4a; --cd-l4: #e88fbf; --cd-l5: #ff7a3d; --cd-l6: #8da2ff; --cd-l7: #b79bff; --cd-l8: #4dd0e1; --cd-l9: #d8a07a; --cd-lo: #8b93a3;
  }
  :root[data-theme="light"] {
    --cd-code: #1d5fbf; --cd-tests: #0b7a55; --cd-docs: #9a5b00;
    --cd-l0: #0072b2; --cd-l1: #b26b00; --cd-l2: #007a5a; --cd-l3: #7a6c00; --cd-l4: #b0457f; --cd-l5: #c2410c; --cd-l6: #3f4fbf; --cd-l7: #6d28d9; --cd-l8: #0e7490; --cd-l9: #8a4b2a; --cd-lo: #5b6472;
  }
  .cd { position: relative; }
  .cd[hidden], #cd-body[hidden] { display: none; }
  .cd, .cd > *, #cd-body, #cd-body > *, .cd-lang-grid > * { min-width: 0; max-width: 100%; }
  #cd-body { display: grid; gap: 14px; }
  #cd-body[hidden] { display: none; }
  .cd-kpis { grid-template-columns: repeat(5, minmax(0, 1fr)); }
  .cd-chart { margin: 6px 0 8px; min-width: 0; }
  .cd-svg { width: 100%; height: auto; display: block; }
  .cd-lang-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 8px 22px; align-items: start; }
  .cd-sub { margin: 10px 0 2px; font-size: 13px; font-weight: 700; }
  .cd-sub-row { display: flex; flex-wrap: wrap; gap: 6px 16px; align-items: center; justify-content: space-between; }
  .cd-text { fill: var(--text); font-size: 12px; }
  .cd-name { fill: var(--text); font-size: 12px; font-weight: 600; }
  .cd-dim { fill: var(--dim); font-size: 11px; }
  .cd-val { fill: var(--text); font-size: 12px; font-variant-numeric: tabular-nums; }
  .cd-ink { fill: var(--ink-on-fill); font-size: 11px; font-weight: 700; font-variant-numeric: tabular-nums; pointer-events: none; }
  :root[data-theme="light"] .cd-ink { fill: #fff; }
  .cd-grid { stroke: var(--border); stroke-width: 1; }
  .cd-head { fill: var(--dim); font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; font-weight: 700; }
  .cd-seg { outline-offset: 2px; cursor: default; }
  .cd-seg rect { stroke: var(--panel); stroke-width: 1.5; }
  .cd-seg:hover rect, .cd-seg:focus-visible rect { filter: brightness(1.18); }
  .cd-seg:focus-visible { outline: 2px solid var(--focus); }
  .cd-track { fill: var(--panel-2); }
  .cd-c-code { fill: var(--cd-code); background: var(--cd-code); } .cd-c-tests { fill: var(--cd-tests); background: var(--cd-tests); } .cd-c-docs { fill: var(--cd-docs); background: var(--cd-docs); }
  .cd-l-0 { fill: var(--cd-l0); background: var(--cd-l0); } .cd-l-1 { fill: var(--cd-l1); background: var(--cd-l1); } .cd-l-2 { fill: var(--cd-l2); background: var(--cd-l2); }
  .cd-l-3 { fill: var(--cd-l3); background: var(--cd-l3); } .cd-l-4 { fill: var(--cd-l4); background: var(--cd-l4); } .cd-l-5 { fill: var(--cd-l5); background: var(--cd-l5); }
  .cd-l-6 { fill: var(--cd-l6); background: var(--cd-l6); } .cd-l-7 { fill: var(--cd-l7); background: var(--cd-l7); } .cd-l-8 { fill: var(--cd-l8); background: var(--cd-l8); }
  .cd-l-9 { fill: var(--cd-l9); background: var(--cd-l9); } .cd-l-o { fill: var(--cd-lo); background: var(--cd-lo); }
  .cd-legend { display: flex; flex-wrap: wrap; gap: 6px 18px; list-style: none; margin: 4px 0 0; padding: 0; font-size: 12px; }
  .cd-legend li { display: inline-flex; align-items: center; gap: 6px; }
  .cd-legend svg { width: 22px; height: 12px; flex: 0 0 auto; }
  .cd-swatch { display: inline-block; width: 12px; height: 12px; border-radius: 3px; flex: 0 0 auto; }
  .cd-line { fill: none; stroke-width: 2.4; stroke-linejoin: round; stroke-linecap: round; }
  .cd-s-code { stroke: var(--cd-code); fill: var(--cd-code); } .cd-s-tests { stroke: var(--cd-tests); fill: var(--cd-tests); } .cd-s-docs { stroke: var(--cd-docs); fill: var(--cd-docs); }
  .cd-s-hydra-umc { stroke: var(--c-hydra-umc); fill: var(--c-hydra-umc); } .cd-s-urtc { stroke: var(--c-urtc); fill: var(--c-urtc); }
  .cd-s-armor { stroke: var(--c-armor); fill: var(--c-armor); } .cd-s-eh3d { stroke: var(--c-eh3d); fill: var(--c-eh3d); }
  .cd-line.cd-s-code, .cd-line.cd-s-tests, .cd-line.cd-s-docs, .cd-line.cd-s-hydra-umc, .cd-line.cd-s-urtc, .cd-line.cd-s-armor, .cd-line.cd-s-eh3d { fill: none; }
  .cd-mark { stroke: var(--panel); stroke-width: 1.2; cursor: default; }
  .cd-mark:hover, .cd-mark:focus-visible { stroke: var(--text); stroke-width: 2; outline: none; }
  .cd-end { font-size: 11.5px; font-weight: 700; stroke: none; }
  .cd-table-wrap { max-height: 62vh; overflow: auto; border: 1px solid var(--border); border-radius: 10px; margin-top: 8px; }
  .cd-table { border-collapse: separate; border-spacing: 0; width: 100%; font-size: 12.5px; font-variant-numeric: tabular-nums; }
  .cd-table th, .cd-table td { padding: 5px 10px; border-bottom: 1px solid var(--border); text-align: right; white-space: nowrap; }
  .cd-table th:first-child, .cd-table td:first-child { text-align: left; position: sticky; left: 0; background: var(--panel); z-index: 1; }
  .cd-table th.cd-left, .cd-table td.cd-left { text-align: left; }
  .cd-table thead th { position: sticky; top: 0; background: var(--panel-2); z-index: 2; vertical-align: bottom; }
  .cd-table thead th:first-child { z-index: 3; }
  .cd-table tfoot td, .cd-table tfoot th { position: sticky; bottom: 0; background: var(--panel-2); font-weight: 700; border-top: 2px solid var(--border-strong); border-bottom: 0; }
  .cd-table tfoot th { text-align: left; left: 0; z-index: 3; }
  .cd-sort { appearance: none; background: none; border: 0; padding: 2px 0; margin: 0; color: var(--text); font: inherit; font-weight: 700; cursor: pointer; display: inline-flex; gap: 4px; align-items: center; }
  .cd-sort:hover { color: var(--accent); }
  .cd-sort:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
  .cd-sort-mark { display: inline-block; min-width: 1ch; color: var(--accent); }
  .cd-name-btn { appearance: none; background: none; border: 0; padding: 0; margin: 0; color: var(--text); font: inherit; cursor: pointer; text-align: left; text-decoration: underline; text-decoration-color: var(--border-strong); text-underline-offset: 3px; }
  .cd-name-btn:hover { color: var(--accent); }
  .cd-name-btn:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
  .cd-muted { color: var(--dim); font-style: italic; }
  .cd-mix { display: inline-flex; width: 110px; height: 10px; border-radius: 5px; overflow: hidden; background: var(--panel-2); vertical-align: middle; }
  .cd-mix i { display: block; height: 100%; }
  .cd-tip { position: fixed; z-index: 60; max-width: min(360px, calc(100vw - 24px)); padding: 6px 10px; border-radius: 8px; border: 1px solid var(--border-strong); background: var(--panel); color: var(--text); font-size: 12px; line-height: 1.4; box-shadow: 0 6px 20px rgba(0,0,0,.35); pointer-events: none; }
  .cd-tip[hidden] { display: none; }
  @media (prefers-reduced-motion: no-preference) {
    .cd-seg rect { transform-box: fill-box; transform-origin: left center; animation: t25-grow-x .6s cubic-bezier(.2,.7,.2,1) both; }
    .cd-line { stroke-dasharray: 1; stroke-dashoffset: 1; animation: evo-draw .9s ease-out .1s forwards; }
  }
  @media (max-width: 1250px) { .cd-kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); } .cd-lang-grid { grid-template-columns: minmax(0, 1fr); } }
  @media (max-width: 760px) { .cd-chart { overflow-x: auto; } .cd-svg { min-width: 640px; } .cd-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); } .cd-table-wrap { max-height: 70vh; } }
  @media print { .cd-table-wrap { max-height: none !important; overflow: visible !important; } .cd-table { table-layout: fixed; width: 100%; font-size: 8px; } .cd-table th, .cd-table td { white-space: normal; overflow-wrap: anywhere; padding: 2px 3px; } .cd-table th:first-child, .cd-table td:first-child, .cd-table thead th, .cd-table tfoot th, .cd-table tfoot td { position: static; } .cd-sort { font-size: 8px; } .cd-mix { width: 100%; } .cd-svg { max-width: 100%; } .cd-seg rect, .cd-line { animation: none !important; stroke-dashoffset: 0 !important; } .cd-tip { display: none; } }
"""

JS = r"""
  // ---------------- Code: lines of code, tests and documentation per repository (counted once a day by scripts/code_stats.py) ----------------
  // Drawn from the JSON embedded in the page. Nothing read = "not verified", never a zero.
  const CD = (DATA.code && typeof DATA.code === "object" && DATA.code.repos) ? DATA.code : { read: false, repos: {}, history: [], ecos: [], types: [], totals: {}, day: null, age: null };
  const CD_KINDS = ["code", "tests", "docs"];
  const CD_SERIES_KEY = { code: "cd_series_code", tests: "cd_series_tests", docs: "cd_series_docs" };
  const CD_TOP_LANGS = 10;
  const cdState = { eco: "all", type: "all", q: "", group: "repo", sort: "code", dir: -1, metric: "code", top: 20 };
  const CD_COLUMNS = [
    ["name", "cd_col_name", false], ["eco", "cd_col_eco", false], ["type", "cd_col_type", false], ["repos", "cd_col_repos", true], ["code", "cd_col_code", true],
    ["comment", "cd_col_comment", true], ["blank", "cd_col_blank", true], ["tests", "cd_col_tests", true], ["testFiles", "cd_col_testfiles", true], ["cases", "cd_col_cases", true],
    ["declared", "cd_col_declared", true], ["docs", "cd_col_docs", true], ["l10n", "cd_col_l10n", true], ["size", "cd_col_size", true], ["commit", "cd_col_commit", false], ["mix", "cd_col_mix", false]
  ];
  function cdNum(n) {
    try { return new Intl.NumberFormat(document.documentElement.lang || "en", { maximumFractionDigits: 1 }).format(n); } catch (e) { return String(n); }
  }
  function cdSize(bytes) {
    if (bytes < 1024) { return cdNum(bytes) + " B"; }
    if (bytes < 1048576) { return cdNum(bytes / 1024) + " KB"; }
    if (bytes < 1073741824) { return cdNum(bytes / 1048576) + " MB"; }
    return cdNum(bytes / 1073741824) + " GB";
  }
  function cdPct(part, whole) { return whole > 0 ? Math.round(part / whole * 1000) / 10 : 0; }
  function cdEcoLabel(key) { const e = CD.ecos.filter(function (x) { return x.key === key; })[0]; return e ? e.label : key; }
  function cdTypeLabel(key, dict) { return dict["cd_type_" + key] || key; }
  function cdOk(r) { return r.state === "ok" || r.state === "lastknown"; }
  function cdDeclared(name, r) {
    if (typeof r.declared_tests === "number") { return r.declared_tests; }
    const t = DATA.tests && DATA.tests.repos && DATA.tests.repos[name];
    if (t && t.unit === "tests" && (t.state === "declared" || t.state === "lastknown") && typeof t.n === "number") { return t.n; }
    return null;
  }
  function cdFigures(name, r) {
    return { repos: 1, code: r.code.code, comment: r.code.comment, blank: r.code.blank, tests: r.tests.code, testFiles: r.tests.files, cases: r.tests.cases,
      declared: cdDeclared(name, r), docs: r.docs.lines, l10n: r.l10n.files, size: r.size, files: r.files };
  }
  function cdSum(list) {
    const out = { repos: 0, code: 0, comment: 0, blank: 0, tests: 0, testFiles: 0, cases: 0, declared: null, docs: 0, l10n: 0, size: 0, files: 0 };
    list.forEach(function (f) {
      Object.keys(out).forEach(function (k) { if (k === "declared") { if (f.declared !== null) { out.declared = (out.declared || 0) + f.declared; } } else { out[k] += f[k]; } });
    });
    return out;
  }
  function cdRepoNames() { return Object.keys(CD.repos).sort(); }
  function cdMeasured() { return cdRepoNames().filter(function (n) { return cdOk(CD.repos[n]); }); }
  function cdGroupFigures(field, key) {
    return cdSum(cdMeasured().filter(function (n) { return CD.repos[n][field] === key; }).map(function (n) { return cdFigures(n, CD.repos[n]); }));
  }
  /* ---- tooltip: one element for every chart, shown on pointer and on keyboard focus ---- */
  function cdTipShow(el, event) {
    const tip = document.getElementById("cd-tip");
    if (!tip || !el.getAttribute("data-tip")) { return; }
    tip.textContent = el.getAttribute("data-tip");
    tip.hidden = false;
    let x, y;
    if (event && event.clientX !== undefined && event.type !== "focusin") { x = event.clientX; y = event.clientY; }
    else { const b = el.getBoundingClientRect(); x = b.left + b.width / 2; y = b.top; }
    const w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, x + 12)) + "px";
    tip.style.top = Math.max(8, (y - h - 12 < 8) ? y + 18 : y - h - 12) + "px";
  }
  function cdTipHide() { const tip = document.getElementById("cd-tip"); if (tip) { tip.hidden = true; } }
  function cdTipped(el, text, focusable) {
    el.setAttribute("data-tip", text); el.setAttribute("aria-label", text); el.setAttribute("role", "img");
    if (focusable !== false) { el.setAttribute("tabindex", "0"); }
    el.classList.add("cd-tipped");
    return el;
  }
  (function () {
    const root = document.getElementById("cd-root");
    if (!root) { return; }
    ["pointerover", "pointermove", "focusin"].forEach(function (type) {
      root.addEventListener(type, function (event) { const el = event.target.closest ? event.target.closest(".cd-tipped") : null; if (el) { cdTipShow(el, event); } });
    });
    ["pointerout", "focusout"].forEach(function (type) {
      root.addEventListener(type, function (event) { const el = event.target.closest ? event.target.closest(".cd-tipped") : null; if (el) { cdTipHide(); } });
    });
    document.addEventListener("keydown", function (event) { if (event.key === "Escape") { cdTipHide(); } });
  })();
  function cdTable(table, caption, heads, rows) {
    table.textContent = "";
    table.appendChild(make("caption", "", caption));
    const hr = make("tr");
    heads.forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    rows.forEach(function (cells) {
      const tr = make("tr");
      cells.forEach(function (c, i) { if (i === 0) { tr.appendChild(make("th", "", c)).setAttribute("scope", "row"); } else { tr.appendChild(make("td", "", c)); } });
      body.appendChild(tr);
    });
    table.appendChild(body);
  }
  function cdLegendItem(cls, text) {
    const li = make("li"); const sw = make("span", "cd-swatch " + cls); sw.setAttribute("aria-hidden", "true");
    li.appendChild(sw); li.appendChild(make("span", "", text));
    return li;
  }
  /* ---- 1. KPIs ---- */
  function cdKpis(dict) {
    const list = document.getElementById("cd-kpis");
    list.textContent = "";
    const all = cdSum(cdMeasured().map(function (n) { return cdFigures(n, CD.repos[n]); }));
    const total = cdRepoNames().length;
    const items = [["repos", all.repos + " / " + total, dict.cd_k_repos], ["code", cdNum(all.code), dict.cd_k_code], ["comment", cdNum(all.comment), dict.cd_k_comment],
      ["blank", cdNum(all.blank), dict.cd_k_blank], ["tests", cdNum(all.tests), dict.cd_k_tests], ["docs", cdNum(all.docs), dict.cd_k_docs],
      ["cases", cdNum(all.cases), dict.cd_k_cases], ["declared", all.declared === null ? "–" : cdNum(all.declared), dict.cd_k_declared],
      ["l10n", cdNum(all.l10n), dict.cd_k_l10n], ["size", cdSize(all.size), dict.cd_k_size]];
    items.forEach(function (it) {
      const li = make("li", "ac-kpi"); li.setAttribute("data-testid", "cd-k-" + it[0]); li.setAttribute("data-value", it[1]);
      li.appendChild(make("b", "", it[1])); li.appendChild(make("span", "", it[2])); list.appendChild(li);
    });
  }
  /* ---- 2. stacked bars: code / tests / docs for the whole, each ecosystem and each type ---- */
  function cdPropRows(dict) {
    const rows = [{ head: null, name: dict.cd_all, f: cdSum(cdMeasured().map(function (n) { return cdFigures(n, CD.repos[n]); })), key: "all" }];
    CD.ecos.forEach(function (e, i) { const f = cdGroupFigures("eco", e.key); if (f.repos) { rows.push({ head: i === 0 ? dict.cd_by_eco : null, name: e.label, f: f, key: e.key }); } });
    CD.types.forEach(function (t, i) { const f = cdGroupFigures("type", t); if (f.repos) { rows.push({ head: i === 0 ? dict.cd_by_type : null, name: cdTypeLabel(t, dict), f: f, key: t }); } });
    return rows;
  }
  function cdStackTip(name, f, dict) {
    const sum = f.code + f.tests + f.docs;
    return tpl(dict.cd_prop_tip, { name: name, code: cdNum(f.code), tests: cdNum(f.tests), docs: cdNum(f.docs), pc: cdNum(cdPct(f.code, sum)), pt: cdNum(cdPct(f.tests, sum)), pd: cdNum(cdPct(f.docs, sum)) });
  }
  function cdRenderProp(dict) {
    const holder = document.getElementById("cd-prop-chart");
    holder.textContent = "";
    const rows = cdPropRows(dict);
    const W = 900, L = 150, R = 130, ROW = 30, HEAD = 22;
    let y = 4;
    const layout = rows.map(function (r) { if (r.head) { y += HEAD; } const at = y; y += ROW; return { r: r, y: at }; });
    const H = y + 4;
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + H, class: "cd-svg", role: "group", "aria-label": dict.cd_prop_aria, "data-testid": "cd-prop-svg" });
    const track = W - L - R;
    layout.forEach(function (it, i) {
      const f = it.r.f, sum = f.code + f.tests + f.docs;
      if (it.r.head) { svg.appendChild(svgEl("text", { x: 0, y: it.y - 8, class: "cd-head" }, it.r.head)); }
      const g = svgEl("g", { "data-row": it.r.key });
      g.appendChild(svgEl("text", { x: 0, y: it.y + 17, class: "cd-name" }, it.r.name));
      g.appendChild(svgEl("rect", { x: L, y: it.y + 3, width: track, height: ROW - 8, rx: 4, class: "cd-track" }));
      let x = L;
      CD_KINDS.forEach(function (k) {
        const w = sum > 0 ? track * f[k] / sum : 0;
        if (w <= 0) { return; }
        const seg = svgEl("g", { class: "cd-seg", "data-kind": k, "data-value": String(f[k]), style: "--i:" + i });
        cdTipped(seg, cdStackTip(it.r.name, f, dict));
        seg.appendChild(svgEl("rect", { x: x, y: it.y + 3, width: Math.max(1, w), height: ROW - 8, rx: 3, class: "cd-c-" + k }));
        if (w > 46) { seg.appendChild(svgEl("text", { x: x + w / 2, y: it.y + 18, "text-anchor": "middle", class: "cd-ink" }, cdNum(cdPct(f[k], sum)) + " %")); }
        g.appendChild(seg);
        x += w;
      });
      g.appendChild(svgEl("text", { x: W, y: it.y + 17, "text-anchor": "end", class: "cd-val" }, cdNum(sum)));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
    const legend = document.getElementById("cd-prop-legend");
    legend.textContent = "";
    CD_KINDS.forEach(function (k) { legend.appendChild(cdLegendItem("cd-c-" + k, dict[CD_SERIES_KEY[k]])); });
    cdTable(document.getElementById("cd-prop-table"), dict.cd_prop_title, [dict.cd_col_name, dict.cd_col_repos, dict.cd_series_code, dict.cd_series_tests, dict.cd_series_docs, "% " + dict.cd_series_code, "% " + dict.cd_series_tests, "% " + dict.cd_series_docs],
      rows.map(function (r) { const s = r.f.code + r.f.tests + r.f.docs; return [r.name, String(r.f.repos), cdNum(r.f.code), cdNum(r.f.tests), cdNum(r.f.docs), cdNum(cdPct(r.f.code, s)), cdNum(cdPct(r.f.tests, s)), cdNum(cdPct(r.f.docs, s))]; }));
  }
  /* ---- 3. languages ---- */
  function cdLanguages() {
    const per = {};
    cdMeasured().forEach(function (n) {
      const r = CD.repos[n];
      Object.keys(r.langs || {}).forEach(function (lang) {
        const l = r.langs[lang];
        const cell = per[lang] || (per[lang] = { all: { files: 0, code: 0, comment: 0, blank: 0 }, eco: {} });
        const e = cell.eco[r.eco] || (cell.eco[r.eco] = { files: 0, code: 0, comment: 0, blank: 0 });
        ["files", "code", "comment", "blank"].forEach(function (k) { cell.all[k] += l[k]; e[k] += l[k]; });
      });
    });
    const order = Object.keys(per).sort(function (a, b) { return per[b].all.code - per[a].all.code || (a < b ? -1 : 1); });
    return { per: per, order: order };
  }
  function cdLangClass(index) { return index < CD_TOP_LANGS ? "cd-l-" + index : "cd-l-o"; }
  function cdRenderLanguages(dict) {
    const data = cdLanguages();
    const top = data.order.slice(0, CD_TOP_LANGS);
    const rest = data.order.slice(CD_TOP_LANGS);
    const sumOf = function (get) { return data.order.reduce(function (a, l) { return a + get(l); }, 0); };
    const allCode = sumOf(function (l) { return data.per[l].all.code; });
    // global bars
    const gHolder = document.getElementById("cd-lang-global");
    gHolder.textContent = "";
    const items = top.map(function (l, i) { return { name: l, cls: cdLangClass(i), code: data.per[l].all.code, comment: data.per[l].all.comment, blank: data.per[l].all.blank, files: data.per[l].all.files }; });
    if (rest.length) {
      const o = { name: dict.cd_lang_other, cls: "cd-l-o", code: 0, comment: 0, blank: 0, files: 0 };
      rest.forEach(function (l) { ["code", "comment", "blank", "files"].forEach(function (k) { o[k] += data.per[l].all[k]; }); });
      items.push(o);
    }
    const W = 520, L = 120, R = 150, ROW = 26;
    const H = items.length * ROW + 8;
    const maxCode = Math.max.apply(null, [1].concat(items.map(function (x) { return x.code; })));
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + H, class: "cd-svg", role: "group", "aria-label": dict.cd_lang_aria, "data-testid": "cd-lang-global-svg" });
    items.forEach(function (it, i) {
      const y = 4 + i * ROW;
      const seg = svgEl("g", { class: "cd-seg", "data-lang": it.name, "data-value": String(it.code), style: "--i:" + i });
      cdTipped(seg, tpl(dict.cd_lang_tip, { lang: it.name, code: cdNum(it.code), pc: cdNum(cdPct(it.code, allCode)), comment: cdNum(it.comment), blank: cdNum(it.blank), files: cdNum(it.files) }));
      seg.appendChild(svgEl("text", { x: 0, y: y + 16, class: "cd-name" }, it.name));
      seg.appendChild(svgEl("rect", { x: L, y: y + 3, width: Math.max(2, (W - L - R) * it.code / maxCode), height: ROW - 8, rx: 3, class: it.cls }));
      seg.appendChild(svgEl("text", { x: W, y: y + 16, "text-anchor": "end", class: "cd-val" }, cdNum(it.code) + " · " + cdNum(cdPct(it.code, allCode)) + " %"));
      svg.appendChild(seg);
    });
    gHolder.appendChild(svg);
    // per ecosystem: 100 % stacked bars
    const eHolder = document.getElementById("cd-lang-eco");
    eHolder.textContent = "";
    const ecoRows = CD.ecos.map(function (e) {
      const parts = top.map(function (l, i) { return { name: l, cls: cdLangClass(i), v: (data.per[l].eco[e.key] || { code: 0 }).code, e: data.per[l].eco[e.key] || { code: 0, comment: 0, blank: 0, files: 0 } }; });
      const other = { name: dict.cd_lang_other, cls: "cd-l-o", v: 0, e: { code: 0, comment: 0, blank: 0, files: 0 } };
      rest.forEach(function (l) { const x = data.per[l].eco[e.key]; if (x) { other.v += x.code; ["code", "comment", "blank", "files"].forEach(function (k) { other.e[k] += x[k]; }); } });
      parts.push(other);
      return { eco: e, parts: parts, total: parts.reduce(function (a, p) { return a + p.v; }, 0) };
    }).filter(function (r) { return r.total > 0; });
    const W2 = 520, L2 = 100, R2 = 90, ROW2 = 32;
    const svg2 = svgEl("svg", { viewBox: "0 0 " + W2 + " " + (ecoRows.length * ROW2 + 8), class: "cd-svg", role: "group", "aria-label": dict.cd_lang_aria, "data-testid": "cd-lang-eco-svg" });
    ecoRows.forEach(function (row, i) {
      const y = 4 + i * ROW2;
      svg2.appendChild(svgEl("text", { x: 0, y: y + 18, class: "cd-name" }, row.eco.label));
      svg2.appendChild(svgEl("rect", { x: L2, y: y + 4, width: W2 - L2 - R2, height: ROW2 - 10, rx: 4, class: "cd-track" }));
      let x = L2;
      row.parts.forEach(function (p) {
        const w = (W2 - L2 - R2) * p.v / row.total;
        if (w <= 0) { return; }
        const seg = svgEl("g", { class: "cd-seg", "data-lang": p.name, "data-eco": row.eco.key, "data-value": String(p.v), style: "--i:" + i });
        cdTipped(seg, row.eco.label + " · " + tpl(dict.cd_lang_tip, { lang: p.name, code: cdNum(p.v), pc: cdNum(cdPct(p.v, row.total)), comment: cdNum(p.e.comment), blank: cdNum(p.e.blank), files: cdNum(p.e.files) }));
        seg.appendChild(svgEl("rect", { x: x, y: y + 4, width: Math.max(1, w), height: ROW2 - 10, rx: 3, class: p.cls }));
        svg2.appendChild(seg);
        x += w;
      });
      svg2.appendChild(svgEl("text", { x: W2, y: y + 18, "text-anchor": "end", class: "cd-val" }, cdNum(row.total)));
    });
    eHolder.appendChild(svg2);
    const legend = document.getElementById("cd-lang-legend");
    legend.textContent = "";
    items.forEach(function (it) { legend.appendChild(cdLegendItem(it.cls, it.name)); });
    const ecoHeads = CD.ecos.map(function (e) { return e.label; });
    cdTable(document.getElementById("cd-lang-table"), dict.cd_lang_title, [dict.cd_lang_col, dict.cd_lang_files, dict.cd_col_code, dict.cd_lang_share].concat(ecoHeads),
      data.order.map(function (l) {
        const a = data.per[l].all;
        return [l, cdNum(a.files), cdNum(a.code), cdNum(cdPct(a.code, allCode)) + " %"].concat(CD.ecos.map(function (e) { return cdNum((data.per[l].eco[e.key] || { code: 0 }).code); }));
      }));
  }
  /* ---- 4. evolution ---- */
  function cdNice(max) {
    if (!(max > 0)) { return 10; }
    const pow = Math.pow(10, Math.floor(Math.log(max) / Math.LN10));
    const steps = [1, 2, 2.5, 5, 10];
    for (let i = 0; i < steps.length; i++) { if (steps[i] * pow >= max) { return steps[i] * pow; } }
    return 10 * pow;
  }
  function cdLineChart(holder, legend, series, pts, dict, metricName, testid) {
    holder.textContent = ""; legend.textContent = "";
    const W = 900, H = 270, L = 64, R = 130, T = 14, B = 30;
    const first = pts[0].d, last = pts[pts.length - 1].d;
    let top = 0;
    series.forEach(function (s) { pts.forEach(function (p) { const v = s.get(p); if (v !== null) { top = Math.max(top, v); } }); });
    const max = cdNice(top);
    const d0 = dayNumber(first), d1 = dayNumber(last);
    const px = function (iso) { return L + (dayNumber(iso) - d0) / Math.max(1, d1 - d0) * (W - L - R); };
    const py = function (v) { return T + (1 - v / max) * (H - T - B); };
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + H, class: "cd-svg", role: "group", "aria-label": tpl(dict.cd_evo_aria, { metric: metricName, first: first, last: last }), "data-testid": testid });
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: py(max * f), y2: py(max * f), class: "cd-grid" }));
      svg.appendChild(svgEl("text", { x: L - 6, y: py(max * f) + 4, "text-anchor": "end", class: "cd-dim" }, cdNum(Math.round(max * f))));
    });
    [[first, "start", L], [last, "end", W - R]].forEach(function (t) { svg.appendChild(svgEl("text", { x: t[2], y: H - 8, "text-anchor": t[1], class: "cd-dim" }, t[0])); });
    const ends = [];
    series.forEach(function (s, kind) {
      const seg = [];
      let lastPt = null;
      pts.forEach(function (p) {
        const v = s.get(p);
        if (v === null) { return; }
        seg.push(px(p.d).toFixed(1) + "," + py(v).toFixed(1));
        lastPt = { y: py(v), v: v };
      });
      if (seg.length > 1) { svg.appendChild(svgEl("path", { d: "M" + seg.join(" L"), class: "cd-line " + s.cls, pathLength: 1, "data-series": s.id })); }
      pts.forEach(function (p, i) {
        const v = s.get(p);
        if (v !== null && (pts.length <= 31 || i === pts.length - 1 || i % 7 === 0)) {
          const m = marker(kind, px(p.d), py(v), s.cls, "");
          m.classList.add("cd-mark");
          while (m.firstChild) { m.removeChild(m.firstChild); }
          cdTipped(m, tpl(dict.cd_evo_point, { series: s.name, date: p.d, n: cdNum(v) }), i === pts.length - 1);
          m.setAttribute("data-series", s.id); m.setAttribute("data-date", p.d); m.setAttribute("data-value", String(v));
          svg.appendChild(m);
        }
      });
      if (lastPt) { ends.push({ s: s, y: lastPt.y, v: lastPt.v }); }
    });
    ends.sort(function (a, b) { return a.y - b.y; });
    for (let i = 1; i < ends.length; i++) { if (ends[i].y - ends[i - 1].y < 13) { ends[i].y = ends[i - 1].y + 13; } }
    ends.forEach(function (e) { svg.appendChild(svgEl("text", { x: W - R + 6, y: e.y + 4, class: "cd-end " + e.s.cls }, e.s.name + " " + cdNum(e.v))); });
    holder.appendChild(svg);
    series.forEach(function (s, kind) {
      const li = make("li"); const key = svgEl("svg", { viewBox: "0 0 22 12", "aria-hidden": "true" });
      key.appendChild(svgEl("line", { x1: 0, x2: 22, y1: 6, y2: 6, class: "cd-line " + s.cls, style: "animation:none;stroke-dasharray:none;stroke-dashoffset:0" }));
      const m = marker(kind, 11, 6, s.cls, ""); while (m.firstChild) { m.removeChild(m.firstChild); } key.appendChild(m);
      li.appendChild(key); li.appendChild(make("span", "", s.name)); legend.appendChild(li);
    });
  }
  function cdRenderEvolution(dict) {
    const wrap = document.getElementById("cd-evo-wrap");
    const msg = document.getElementById("cd-evo-msg");
    const table = document.getElementById("cd-evo-table");
    table.textContent = "";
    const pts = (CD.history || []).slice().sort(function (a, b) { return a.d < b.d ? -1 : 1; });
    wrap.hidden = true; msg.hidden = true;
    if (!pts.length) { msg.textContent = dict.cd_evo_none; msg.hidden = false; return; }
    const metric = cdState.metric;
    const totalSeries = CD_KINDS.map(function (k) { return { id: k, name: dict[CD_SERIES_KEY[k]], cls: "cd-s-" + k, get: function (p) { return p.t && typeof p.t[k] === "number" ? p.t[k] : null; } }; });
    const ecoSeries = CD.ecos.map(function (e) { return { id: e.key, name: e.label, cls: "cd-s-" + e.key, get: function (p) { return p.e && p.e[e.key] ? p.e[e.key][metric] : null; } }; });
    cdTable(table, tpl(dict.cd_evo_aria, { metric: dict.cd_evo_title, first: pts[0].d, last: pts[pts.length - 1].d }),
      [dict.cd_evo_date].concat(totalSeries.map(function (s) { return s.name; }), ecoSeries.map(function (s) { return s.name + " (" + dict[CD_SERIES_KEY[metric]] + ")"; })),
      pts.map(function (p) { return [p.d].concat(totalSeries.concat(ecoSeries).map(function (s) { const v = s.get(p); return v === null ? "–" : cdNum(v); })); }));
    // the buttons that choose the kind of line of the chart by ecosystem
    const chips = document.getElementById("cd-evo-metric");
    chips.textContent = "";
    CD_KINDS.forEach(function (k) {
      const b = make("button", "chip", dict[CD_SERIES_KEY[k]]); b.type = "button"; b.setAttribute("data-metric", k); b.setAttribute("data-testid", "cd-metric-" + k);
      b.setAttribute("aria-pressed", metric === k ? "true" : "false");
      b.addEventListener("click", function () { cdState.metric = k; cdRenderEvolution(currentDict()); });
      chips.appendChild(b);
    });
    if (pts.length < 2) { msg.textContent = tpl(dict.cd_evo_one, { date: pts[0].d }); msg.hidden = false; return; }
    cdLineChart(document.getElementById("cd-evo-total"), document.getElementById("cd-evo-total-legend"), totalSeries, pts, dict, dict.cd_evo_total_title, "cd-evo-total-svg");
    cdLineChart(document.getElementById("cd-evo-eco"), document.getElementById("cd-evo-eco-legend"), ecoSeries, pts, dict, dict[CD_SERIES_KEY[metric]], "cd-evo-eco-svg");
    wrap.hidden = false;
  }
  /* ---- 5. the largest repositories ---- */
  function cdRenderTop(dict) {
    const holder = document.getElementById("cd-top-chart");
    holder.textContent = "";
    const rows = cdMeasured().map(function (n) { return { name: n, f: cdFigures(n, CD.repos[n]) }; })
      .sort(function (a, b) { const sa = a.f.code + a.f.tests + a.f.docs, sb = b.f.code + b.f.tests + b.f.docs; return sb - sa || (a.name < b.name ? -1 : 1); }).slice(0, cdState.top);
    const W = 900, L = 250, R = 110, ROW = 24;
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + (rows.length * ROW + 8), class: "cd-svg", role: "group", "aria-label": tpl(dict.cd_top_aria, { n: rows.length }), "data-testid": "cd-top-svg" });
    const max = Math.max.apply(null, [1].concat(rows.map(function (r) { return r.f.code + r.f.tests + r.f.docs; })));
    rows.forEach(function (r, i) {
      const y = 4 + i * ROW, sum = r.f.code + r.f.tests + r.f.docs;
      const g = svgEl("g", { "data-repo": r.name });
      g.appendChild(svgEl("text", { x: 0, y: y + 15, class: "cd-text" }, r.name));
      let x = L;
      CD_KINDS.forEach(function (k) {
        const w = (W - L - R) * r.f[k] / max;
        if (w <= 0) { return; }
        const seg = svgEl("g", { class: "cd-seg", "data-kind": k, "data-value": String(r.f[k]), style: "--i:" + i });
        cdTipped(seg, cdStackTip(r.name, r.f, dict));
        seg.appendChild(svgEl("rect", { x: x, y: y + 2, width: Math.max(1, w), height: ROW - 7, rx: 2, class: "cd-c-" + k }));
        g.appendChild(seg);
        x += w;
      });
      g.appendChild(svgEl("text", { x: W, y: y + 15, "text-anchor": "end", class: "cd-val" }, cdNum(sum)));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
    cdTable(document.getElementById("cd-top-table"), dict.cd_top_title, [dict.cd_col_name, dict.cd_series_code, dict.cd_series_tests, dict.cd_series_docs],
      rows.map(function (r) { return [r.name, cdNum(r.f.code), cdNum(r.f.tests), cdNum(r.f.docs)]; }));
  }
  /* ---- 6. the sortable, filterable table ---- */
  function cdRows(dict) {
    const q = cdState.q.trim().toLowerCase();
    const names = cdRepoNames().filter(function (n) {
      const r = CD.repos[n];
      if (cdState.eco !== "all" && r.eco !== cdState.eco) { return false; }
      if (cdState.type !== "all" && r.type !== cdState.type) { return false; }
      return !q || n.toLowerCase().indexOf(q) >= 0;
    });
    const unread = names.filter(function (n) { return !cdOk(CD.repos[n]); });
    const measured = names.filter(function (n) { return cdOk(CD.repos[n]); });
    let rows;
    if (cdState.group === "repo") {
      rows = measured.map(function (n) { const r = CD.repos[n]; return Object.assign({ name: n, repo: n, eco: r.eco, type: r.type, commit: r.commit || r.pushed || "", state: r.state }, cdFigures(n, r)); });
    } else {
      const field = cdState.group;
      const keys = Array.from(new Set(measured.map(function (n) { return CD.repos[n][field]; })));
      rows = keys.map(function (key) {
        const f = cdSum(measured.filter(function (n) { return CD.repos[n][field] === key; }).map(function (n) { return cdFigures(n, CD.repos[n]); }));
        return Object.assign({ name: field === "eco" ? cdEcoLabel(key) : cdTypeLabel(key, dict), key: key, group: field, commit: "", state: "ok" }, f);
      });
    }
    const dir = cdState.dir, key = cdState.sort;
    const textual = key === "name" || key === "eco" || key === "type" || key === "commit";
    rows.sort(function (a, b) {
      let va = a[key], vb = b[key];
      if (key === "eco") { va = cdEcoLabel(a.eco || ""); vb = cdEcoLabel(b.eco || ""); }
      if (key === "type") { va = cdTypeLabel(a.type || "", dict); vb = cdTypeLabel(b.type || "", dict); }
      if (textual) { return (String(va).toLowerCase() < String(vb).toLowerCase() ? -1 : String(va).toLowerCase() > String(vb).toLowerCase() ? 1 : 0) * dir || (a.name < b.name ? -1 : 1); }
      if (key === "mix") { va = a.code + a.tests + a.docs; vb = b.code + b.tests + b.docs; }
      if (va === null) { va = -1; } if (vb === null) { vb = -1; }
      return (va - vb) * dir || (a.name < b.name ? -1 : 1);
    });
    return { rows: rows, unread: unread, all: names.length, total: cdRepoNames().length };
  }
  function cdCell(row, key, dict) {
    if (key === "name") { return null; }
    if (key === "eco") { return row.eco ? cdEcoLabel(row.eco) : ""; }
    if (key === "type") { return row.type ? cdTypeLabel(row.type, dict) : ""; }
    if (key === "repos") { return row.repos > 1 || row.group ? cdNum(row.repos) : ""; }
    if (key === "declared") { return row.declared === null ? "–" : cdNum(row.declared); }
    if (key === "size") { return cdSize(row.size); }
    if (key === "commit") { return row.commit || "–"; }
    if (key === "mix") { return null; }
    return cdNum(row[key]);
  }
  function cdMixBar(row, dict) {
    const sum = row.code + row.tests + row.docs;
    const bar = make("span", "cd-mix cd-tipped");
    cdTipped(bar, cdStackTip(row.name, row, dict), false);
    CD_KINDS.forEach(function (k) { const i = make("i", "cd-c-" + k); i.style.width = cdPct(row[k], sum) + "%"; bar.appendChild(i); });
    return bar;
  }
  function cdRenderTable(dict) {
    const table = document.getElementById("cd-table");
    const view = cdRows(dict);
    const grouped = cdState.group !== "repo";
    const cols = CD_COLUMNS.filter(function (c) { return grouped ? c[0] !== "eco" && c[0] !== "type" && c[0] !== "commit" : c[0] !== "repos"; });
    table.textContent = "";
    table.appendChild(make("caption", "sr-only", dict.cd_table_title));
    const hr = make("tr");
    cols.forEach(function (c) {
      const th = make("th", c[2] ? "" : "cd-left"); th.setAttribute("scope", "col");
      if (c[0] === "mix") { th.textContent = dict[c[1]]; hr.appendChild(th); return; }
      const label = c[0] === "name" ? (grouped ? (cdState.group === "eco" ? dict.cd_filter_eco : dict.cd_filter_type) : dict.cd_col_name) : dict[c[1]];
      const b = make("button", "cd-sort"); b.type = "button"; b.setAttribute("data-sort", c[0]); b.setAttribute("data-testid", "cd-sort-" + c[0]);
      b.appendChild(make("span", "", label));
      const active = cdState.sort === c[0];
      b.appendChild(make("span", "cd-sort-mark", active ? (cdState.dir < 0 ? "↓" : "↑") : "")).setAttribute("aria-hidden", "true");
      th.setAttribute("aria-sort", active ? (cdState.dir < 0 ? "descending" : "ascending") : "none");
      b.addEventListener("click", function () {
        if (cdState.sort === c[0]) { cdState.dir = -cdState.dir; } else { cdState.sort = c[0]; cdState.dir = (c[2] || c[0] === "commit") ? -1 : 1; }
        cdRenderTable(currentDict());
        const again = document.querySelector('#cd-table [data-sort="' + c[0] + '"]'); if (again) { again.focus(); }
        document.getElementById("cd-live").textContent = tpl(currentDict().cd_sorted, { col: label, dir: cdState.dir < 0 ? currentDict().cd_desc : currentDict().cd_asc });
      });
      th.appendChild(b); hr.appendChild(th);
    });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    view.rows.forEach(function (row) {
      const tr = make("tr"); tr.setAttribute("data-row", row.repo || row.key || row.name); if (row.state === "lastknown") { tr.setAttribute("data-state", "lastknown"); }
      tr.setAttribute("data-code", String(row.code));
      cols.forEach(function (c) {
        const left = !c[2];
        const td = make("td", left ? "cd-left" : "");
        if (c[0] === "name") {
          if (row.repo) { const b = make("button", "cd-name-btn", row.name); b.type = "button"; b.setAttribute("data-repo", row.repo); b.addEventListener("click", function () { openPanel(row.repo, b); }); td.appendChild(b); }
          else { td.textContent = row.name; }
          if (row.state === "lastknown") { td.appendChild(make("span", "cd-muted", " · " + dict.cd_st_lastknown)); }
        } else if (c[0] === "mix") { td.appendChild(cdMixBar(row, dict)); }
        else { td.textContent = cdCell(row, c[0], dict); }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    (grouped ? [] : view.unread).forEach(function (n) {
      const r = CD.repos[n];
      const tr = make("tr"); tr.setAttribute("data-row", n); tr.setAttribute("data-state", "unread");
      cols.forEach(function (c, i) {
        const td = make("td", c[2] ? "" : "cd-left");
        if (i === 0) { td.textContent = n; }
        else if (c[0] === "eco") { td.textContent = cdEcoLabel(r.eco); }
        else if (c[0] === "type") { td.textContent = cdTypeLabel(r.type, dict); }
        else if (i === 3 || c[0] === "code") { td.textContent = dict.cd_st_unread; td.className += " cd-muted"; }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
    const total = cdSum(view.rows.map(function (r) { return r; }));
    const foot = make("tfoot"); const ft = make("tr"); ft.setAttribute("data-testid", "cd-total");
    cols.forEach(function (c, i) {
      if (i === 0) { const th = make("th", "", dict.cd_total); th.setAttribute("scope", "row"); ft.appendChild(th); return; }
      const td = make("td", c[2] ? "" : "cd-left");
      if (c[0] === "repos") { td.textContent = cdNum(total.repos); }
      else if (c[0] === "mix") { td.appendChild(cdMixBar(Object.assign({ name: dict.cd_total }, total), dict)); }
      else if (["eco", "type", "commit"].indexOf(c[0]) >= 0) { td.textContent = ""; }
      else { td.textContent = cdCell(total, c[0], dict); }
      ft.appendChild(td);
    });
    foot.appendChild(ft); table.appendChild(foot);
    const shownRows = view.rows.length + (grouped ? 0 : view.unread.length);
    document.getElementById("cd-none").hidden = shownRows > 0;
    document.getElementById("cd-table-wrap").hidden = shownRows === 0;
    const counter = document.getElementById("cd-matches");
    counter.textContent = tpl(dict.cd_matches, { shown: view.all, total: view.total });
    counter.setAttribute("data-shown", String(view.all)); counter.setAttribute("data-total", String(view.total));
  }
  function cdRenderControls(dict) {
    [["cd-eco-chips", "eco", [["all", dict.cd_filter_all, cdRepoNames().length]].concat(CD.ecos.map(function (e) { return [e.key, e.label, cdRepoNames().filter(function (n) { return CD.repos[n].eco === e.key; }).length]; }))],
     ["cd-type-chips", "type", [["all", dict.cd_filter_all, cdRepoNames().length]].concat(CD.types.map(function (t) { return [t, cdTypeLabel(t, dict), cdRepoNames().filter(function (n) { return CD.repos[n].type === t; }).length]; }))]
    ].forEach(function (def) {
      const holder = document.getElementById(def[0]);
      holder.textContent = "";
      def[2].forEach(function (c) {
        if (c[0] !== "all" && c[2] === 0) { return; }
        const b = make("button", "chip"); b.type = "button"; b.setAttribute("data-" + def[1], c[0]); b.setAttribute("data-testid", "cd-" + def[1] + "-" + c[0]);
        b.setAttribute("aria-pressed", cdState[def[1]] === c[0] ? "true" : "false");
        b.appendChild(make("span", "", c[1])); b.appendChild(document.createTextNode(" ")); b.appendChild(make("b", "", String(c[2])));
        b.addEventListener("click", function () { cdState[def[1]] = c[0]; cdRenderControls(currentDict()); cdRenderTable(currentDict()); });
        holder.appendChild(b);
      });
    });
    const sel = document.getElementById("cd-group");
    sel.textContent = "";
    [["repo", dict.cd_by_repo], ["eco", dict.cd_by_eco], ["type", dict.cd_by_type]].forEach(function (o) { const el = make("option", "", o[1]); el.value = o[0]; sel.appendChild(el); });
    sel.value = cdState.group;
  }
  function cdRender(dict) {
    const root = document.getElementById("cd-root");
    if (!root) { return; }
    const names = cdRepoNames();
    const unread = names.filter(function (n) { return CD.repos[n].state === "unread"; });
    const kept = names.filter(function (n) { return CD.repos[n].state === "lastknown"; });
    const nothing = !CD.read;
    document.getElementById("cd-not-read").hidden = !nothing;
    document.getElementById("cd-body").hidden = nothing;
    const stale = document.getElementById("cd-stale");
    const old = !nothing && typeof CD.age === "number" && CD.age >= 3;
    stale.hidden = !old;
    stale.textContent = old ? tpl(dict.cd_stale, { days: CD.age, date: CD.day || "" }) : "";
    const note = document.getElementById("cd-note");
    const parts = [];
    if (kept.length) { parts.push(tpl(dict.cd_lastknown_note, { n: kept.length })); }
    if (unread.length && !nothing) { parts.push(tpl(dict.cd_unread_note, { n: unread.length })); }
    note.hidden = parts.length === 0;
    note.textContent = parts.join(" ");
    document.getElementById("cd-help-body").textContent = tpl(dict.cd_help_body, { day: CD.day || "–", n: names.length - unread.length });
    if (nothing) { return; }
    cdKpis(dict); cdRenderProp(dict); cdRenderLanguages(dict); cdRenderEvolution(dict); cdRenderTop(dict); cdRenderControls(dict); cdRenderTable(dict);
  }
  (function () {
    const sel = document.getElementById("cd-group");
    const search = document.getElementById("cd-search");
    const top = document.getElementById("cd-top-n");
    if (sel) { sel.addEventListener("change", function () { cdState.group = sel.value; cdState.sort = "code"; cdState.dir = -1; cdRenderTable(currentDict()); }); }
    if (search) { search.addEventListener("input", function () { cdState.q = search.value; cdRenderTable(currentDict()); }); }
    if (top) { top.addEventListener("change", function () { cdState.top = parseInt(top.value, 10) || 20; cdRenderTop(currentDict()); }); }
  })();
"""
