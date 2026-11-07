#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_changes_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The "Changelog" tab: statistics of the CHANGELOG of every repository, drawn in the browser from the embedded `code` data.

Figures (published versions and entries, entries waiting, the kind of each entry decided by words, the pace of the tags of GitHub), a donut and stacked
bars of the kinds, evolution from the daily history, a ranking, the detail of a repository (its versions and, for the newest ones, its entries, searchable
and filterable by kind), a sortable and filterable table and an export of what the table shows (CSV and JSON). It shares the shell's scope and the helpers of
dashboard_code_ui.py (`cdNum`, `cdTable`, `cdTipped`, `cdLineChart`, `cdLegendItem`, `CD`). Every chart has a table with the same figures, a name and a
tooltip on hover and on focus. Stdlib only.
"""
from __future__ import annotations

import dashboard_code_texts
from dashboard_charts import esc

EN = dashboard_code_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def _alt(ident: str) -> str:
    return f'<div class="sr-only"><table id="{ident}" data-testid="{ident}"><thead><tr><th scope="col" data-i18n="cd_col_name">{esc(EN["cd_col_name"])}</th></tr></thead></table></div>'


def _card(ident: str, title: str, hint: str | None, body: str) -> str:
    hint_html = f'<p class="muted" {_t(hint)}</p>' if hint else ""
    return (f'<section class="card" aria-labelledby="{ident}-title"><header class="card-head"><h3 class="card-title" id="{ident}-title" {_t(title)}</h3></header>'
            f'{hint_html}{body}</section>')


def panel_html() -> str:
    return (
        '<section class="ins cd" id="ch-root" aria-labelledby="ch-title" data-testid="changelog-root">'
        '<div id="ch-body" data-testid="ch-body">'
        f'<header class="ins-head"><h2 class="card-title" id="ch-title" {_t("ch_title")}</h2>'
        f'<span class="ts-badge" data-testid="ch-badge" {_t("ch_badge")}</span></header>'
        f'<p class="muted" {_t("ch_hint")}</p>'
        '<details class="ts-help" data-testid="ch-help">'
        f'<summary {_t("cd_help_summary")}</summary><p id="ch-help-body" data-testid="ch-help-body"></p></details>'
        '<p class="no-data" id="ch-not-read" data-testid="ch-not-read" hidden></p>'
        '<div id="ch-main" data-testid="ch-main">'
        # filters
        '<div class="ev-controls"><div class="ev-group" role="group" aria-labelledby="ch-eco-t">'
        f'<span class="scope-title" id="ch-eco-t" {_t("cd_filter_eco")}</span><span class="chip-row" id="ch-eco-chips" data-testid="ch-eco-chips"></span></div>'
        '<div class="ev-group" role="group" aria-labelledby="ch-type-t">'
        f'<span class="scope-title" id="ch-type-t" {_t("cd_filter_type")}</span><span class="chip-row" id="ch-type-chips" data-testid="ch-type-chips"></span></div>'
        '<div class="ts-field"><label class="scope-title" for="ch-search" data-i18n="cd_search">Search a repository</label>'
        '<input type="search" id="ch-search" data-testid="ch-search" autocomplete="off" maxlength="80"></div></div>'
        '<p class="matches" id="ch-matches" aria-live="polite" data-testid="ch-matches"></p>'
        '<ul class="ac-kpis cd-kpis" id="ch-kpis" data-testid="ch-kpis"></ul>'
        + _card("ch-donut", "ch_donut_title", "ch_donut_hint",
                '<div class="ch-donut-grid"><div class="cd-chart" id="ch-donut-chart" data-testid="ch-donut-chart"></div>'
                '<ul class="cd-legend ch-legend" id="ch-donut-legend" data-testid="ch-donut-legend"></ul></div>' + _alt("ch-donut-table"))
        + _card("ch-stack", "ch_stack_title", None, '<div class="cd-chart" id="ch-stack-chart" data-testid="ch-stack-chart"></div>'
                '<ul class="cd-legend" id="ch-stack-legend" data-testid="ch-stack-legend"></ul>' + _alt("ch-stack-table"))
        + _card("ch-evo", "ch_evo_title", "ch_evo_hint",
                '<p class="no-data" id="ch-evo-msg" data-testid="ch-evo-msg" role="status" hidden></p><div id="ch-evo-wrap" data-testid="ch-evo-wrap" hidden>'
                f'<h4 class="cd-sub" {_t("ch_evo_total_title")}</h4><div class="cd-chart" id="ch-evo-total" data-testid="ch-evo-total"></div>'
                '<ul class="cd-legend" id="ch-evo-total-legend" data-testid="ch-evo-total-legend"></ul>'
                f'<h4 class="cd-sub" {_t("ch_evo_eco_title")}</h4><div class="cd-chart" id="ch-evo-eco" data-testid="ch-evo-eco"></div>'
                '<ul class="cd-legend" id="ch-evo-eco-legend" data-testid="ch-evo-eco-legend"></ul></div>' + _alt("ch-evo-table"))
        + _card("ch-rank", "ch_rank_title", None,
                '<div class="ev-controls"><div class="ts-field"><label class="scope-title" for="ch-top-n" data-i18n="cd_top_n">How many</label>'
                '<select id="ch-top-n" data-testid="ch-top-n"><option value="10">10</option><option value="15" selected>15</option><option value="30">30</option></select></div></div>'
                f'<h4 class="cd-sub" {_t("ch_rank_vol_title")}</h4><div class="cd-chart" id="ch-rank-vol" data-testid="ch-rank-vol"></div>'
                '<ul class="cd-legend" id="ch-rank-legend" data-testid="ch-rank-legend"></ul>'
                f'<h4 class="cd-sub" {_t("ch_rank_fix_title")}</h4><p class="muted" id="ch-rank-fix-hint"></p><div class="cd-chart" id="ch-rank-fix" data-testid="ch-rank-fix"></div>'
                + _alt("ch-rank-vol-table") + _alt("ch-rank-fix-table"))
        + _card("ch-det", "ch_det_title", "ch_det_hint",
                '<div class="ev-controls"><div class="ts-field"><label class="scope-title" for="ch-repo" data-i18n="ch_det_repo">Repository</label>'
                '<select id="ch-repo" data-testid="ch-repo"></select></div>'
                '<div class="ts-field"><label class="scope-title" for="ch-range" data-i18n="ch_det_range">Versions shown</label><select id="ch-range" data-testid="ch-range"></select></div></div>'
                '<p class="no-data" id="ch-det-none" data-testid="ch-det-none" hidden></p><div id="ch-det-wrap" data-testid="ch-det-wrap">'
                '<div class="cd-chart" id="ch-det-chart" data-testid="ch-det-chart"></div>'
                '<div class="cd-table-wrap" tabindex="0" role="region" aria-labelledby="ch-det-title"><table class="cd-table" id="ch-det-table" data-testid="ch-det-table">'
                '<thead><tr><th scope="col" data-i18n="ch_det_version">Version</th></tr></thead></table></div>'
                '<section class="ch-entries" id="ch-entries" data-testid="ch-entries" aria-labelledby="ch-entries-title" hidden>'
                '<h4 class="cd-sub" id="ch-entries-title" data-testid="ch-entries-title"></h4>'
                '<p class="muted" id="ch-entries-note" data-testid="ch-entries-note" hidden></p>'
                '<div class="ev-controls"><div class="ts-field"><label class="scope-title" for="ch-entry-search" data-i18n="ch_det_search">Search the entries</label>'
                '<input type="search" id="ch-entry-search" data-testid="ch-entry-search" autocomplete="off" maxlength="80"></div>'
                '<div class="ev-group" role="group" aria-labelledby="ch-entry-kind-t"><span class="scope-title" id="ch-entry-kind-t" data-i18n="ch_det_kind">Kind</span>'
                '<span class="chip-row" id="ch-entry-kinds" data-testid="ch-entry-kinds"></span></div></div>'
                '<p class="matches" id="ch-entry-count" aria-live="polite" data-testid="ch-entry-count"></p>'
                '<ul class="ch-entry-list" id="ch-entry-list" data-testid="ch-entry-list"></ul></section></div>' + _alt("ch-det-alt"))
        + '<section class="card" aria-labelledby="ch-table-title"><header class="card-head">'
        f'<h3 class="card-title" id="ch-table-title" {_t("ch_table_title")}</h3></header><p class="muted" {_t("ch_table_hint")}</p>'
        '<div class="ev-controls"><div class="ts-field"><label class="scope-title" for="ch-group" data-i18n="cd_group">Group rows by</label><select id="ch-group" data-testid="ch-group"></select></div>'
        '<div class="ev-group" role="group" aria-labelledby="ch-export-t"><span class="scope-title" id="ch-export-t" data-i18n="ch_export_label">Export</span>'
        f'<button type="button" class="btn" id="ch-export-csv" data-testid="ch-export-csv" {_t("ch_export_csv")}</button>'
        f'<button type="button" class="btn" id="ch-export-json" data-testid="ch-export-json" {_t("ch_export_json")}</button></div></div>'
        f'<p class="muted" {_t("ch_export_note")}</p><p class="sr-only" id="ch-live" role="status" data-testid="ch-live"></p>'
        '<div class="cd-table-wrap" id="ch-table-wrap" tabindex="0" role="region" aria-labelledby="ch-table-title" data-testid="ch-table-wrap">'
        '<table class="cd-table" id="ch-table" data-testid="ch-table"><thead><tr><th scope="col" data-i18n="cd_col_name">Repository</th></tr></thead></table></div>'
        f'<p class="no-data" id="ch-none" data-testid="ch-none" hidden {_t("cd_none")}</p></section>'
        '</div></div></section>'
    )


CSS = r"""
  /* ======================= Changes: statistics of the changelogs ======================= */
  #ch-body { display: grid; gap: 14px; min-width: 0; }
  #ch-main[hidden] { display: none !important; }
  #ch-main { display: grid; gap: 14px; min-width: 0; }
  #ch-main > * { min-width: 0; max-width: 100%; }
  .ch-donut-grid { display: grid; grid-template-columns: minmax(0, 340px) minmax(0, 1fr); gap: 8px 28px; align-items: center; }
  .ch-donut-grid .cd-chart { max-width: 340px; }
  .ch-legend { flex-direction: column; flex-wrap: nowrap; gap: 5px; font-size: 13px; }
  .ch-legend li { display: grid; grid-template-columns: 14px minmax(0, 1fr) auto; gap: 8px; align-items: center; font-variant-numeric: tabular-nums; }
  .ch-legend b { font-weight: 600; }
  .ch-donut-total { fill: var(--text); font-size: 26px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .ch-donut-label { fill: var(--dim); font-size: 12px; }
  .cd-seg path { stroke: var(--panel); stroke-width: 1.5; }
  .cd-seg:hover path, .cd-seg:focus-visible path { filter: brightness(1.18); }
  .ch-entry-list { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 4px; max-height: 50vh; overflow: auto; }
  .ch-entry-list li { display: grid; grid-template-columns: minmax(110px, 160px) minmax(0, 1fr); gap: 10px; align-items: baseline; padding: 4px 8px; border-bottom: 1px solid var(--border); font-size: 13px; }
  .ch-kind-tag { display: inline-flex; gap: 6px; align-items: center; font-size: 12px; color: var(--dim); }
  .ch-open { appearance: none; background: none; border: 1px solid var(--border-strong); border-radius: 8px; padding: 2px 8px; color: var(--text); font: inherit; font-size: 12px; cursor: pointer; }
  .ch-open:hover, .ch-open[aria-pressed="true"] { border-color: var(--accent); color: var(--accent); }
  .ch-open:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
  .ch-share { fill: var(--cd-code); }
  @media (max-width: 1250px) { .ch-donut-grid { grid-template-columns: minmax(0, 1fr); } }
  @media (max-width: 760px) { .ch-entry-list li { grid-template-columns: minmax(0, 1fr); } }
  @media print { .ch-entry-list { max-height: none !important; overflow: visible !important; } }
"""

JS = r"""
  // ---------------- Changes: the CHANGELOG of every repository (read once a day by scripts/code_stats.py) ----------------
  const CH_MIN = 10;
  const chState = { eco: "all", type: "all", q: "", group: "repo", sort: "entries", dir: -1, repo: "", range: 10, top: 15, version: null, vq: "", vkind: "all" };
  function chKinds() { return CD.kinds || []; }
  function chKindClass(i) { return chKinds()[i] === "unclassified" ? "cd-l-o" : "cd-l-" + Math.min(i, 9); }
  function chKindLabel(key, dict) { return dict["ch_kind_" + key] || key; }
  function chHas(name) { const r = CD.repos[name]; return !!(r && cdOk(r) && r.changes); }
  function chAll() { return cdRepoNames().filter(chHas); }
  function chNames() {
    const q = chState.q.trim().toLowerCase();
    return chAll().filter(function (n) {
      const r = CD.repos[n];
      if (chState.eco !== "all" && r.eco !== chState.eco) { return false; }
      if (chState.type !== "all" && r.type !== chState.type) { return false; }
      return !q || n.toLowerCase().indexOf(q) >= 0;
    });
  }
  function chKindSum(names) {
    const out = {};
    chKinds().forEach(function (k) { out[k] = 0; });
    names.forEach(function (n) { chKinds().forEach(function (k) { out[k] += CD.repos[n].changes.kinds[k] || 0; }); });
    return out;
  }
  function chTotals(names) {
    const t = { repos: names.length, versions: 0, entries: 0, unreleased: 0, fix: 0, unclassified: 0, d30: 0, d90: 0, tags: 0 };
    names.forEach(function (n) {
      const c = CD.repos[n].changes, rel = CD.repos[n].rel;
      t.versions += c.versions; t.entries += c.entries; t.unreleased += c.unreleased; t.fix += c.kinds.fix || 0; t.unclassified += c.kinds.unclassified || 0;
      if (rel) { t.d30 += rel.d30; t.d90 += rel.d90; t.tags += rel.tags; }
    });
    return t;
  }
  function chStackRows(holder, rows, dict, testid, aria) {
    // rows: [{name, label, kinds: {kind: n}, total, home}], drawn as stacked horizontal bars
    holder.textContent = "";
    const W = 900, L = 250, R = 90, ROW = 24;
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + (rows.length * ROW + 8), class: "cd-svg", role: "group", "aria-label": aria, "data-testid": testid });
    const max = Math.max.apply(null, [1].concat(rows.map(function (r) { return r.total; })));
    rows.forEach(function (r, i) {
      const y = 4 + i * ROW;
      const g = svgEl("g", { "data-row": r.name });
      g.appendChild(svgEl("text", { x: 0, y: y + 15, class: "cd-text" }, r.label || r.name));
      let x = L;
      chKinds().forEach(function (k, ki) {
        const v = r.kinds[k] || 0;
        if (v <= 0) { return; }
        const w = (W - L - R) * v / max;
        const seg = svgEl("g", { class: "cd-seg", "data-kind": k, "data-value": String(v), style: "--i:" + i });
        cdTipped(seg, tpl(dict.ch_seg_tip, { name: r.label || r.name, kind: chKindLabel(k, dict), n: cdNum(v), total: cdNum(r.total), pc: cdNum(cdPct(v, r.total)) }));
        seg.appendChild(svgEl("rect", { x: x, y: y + 2, width: Math.max(1, w), height: ROW - 7, rx: 2, class: chKindClass(ki) }));
        g.appendChild(seg);
        x += w;
      });
      g.appendChild(svgEl("text", { x: W, y: y + 15, "text-anchor": "end", class: "cd-val" }, cdNum(r.total)));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
  }
  function chKindLegend(list, dict) {
    list.textContent = "";
    chKinds().forEach(function (k, i) { list.appendChild(cdLegendItem(chKindClass(i), chKindLabel(k, dict))); });
  }
  function chKindRowCells(kinds) { return chKinds().map(function (k) { return cdNum(kinds[k] || 0); }); }
  /* ---- KPIs ---- */
  function chRenderKpis(dict, names) {
    const t = chTotals(names), list = document.getElementById("ch-kpis");
    list.textContent = "";
    const total = t.entries + t.unreleased;
    const items = [["repos", cdNum(t.repos), dict.ch_k_repos], ["versions", cdNum(t.versions), dict.ch_k_versions], ["entries", cdNum(t.entries), dict.ch_k_entries],
      ["unreleased", cdNum(t.unreleased), dict.ch_k_unreleased], ["avg", t.versions ? cdNum(Math.round(t.entries / t.versions * 10) / 10) : "–", dict.ch_k_avg],
      ["fix", cdNum(t.fix) + " (" + cdNum(cdPct(t.fix, total)) + " %)", dict.ch_k_fix], ["unclassified", cdNum(t.unclassified) + " (" + cdNum(cdPct(t.unclassified, total)) + " %)", dict.ch_k_unclassified],
      ["d30", cdNum(t.d30), dict.ch_k_d30], ["d90", cdNum(t.d90), dict.ch_k_d90]];
    items.forEach(function (it) {
      const li = make("li", "ac-kpi"); li.setAttribute("data-testid", "ch-k-" + it[0]); li.setAttribute("data-value", it[1]);
      li.appendChild(make("b", "", it[1])); li.appendChild(make("span", "", it[2])); list.appendChild(li);
    });
  }
  /* ---- donut ---- */
  function chArc(cx, cy, r0, r1, a0, a1) {
    const p = function (r, a) { return (cx + r * Math.cos(a)).toFixed(2) + "," + (cy + r * Math.sin(a)).toFixed(2); };
    const large = a1 - a0 > Math.PI ? 1 : 0;
    return "M" + p(r1, a0) + " A" + r1 + "," + r1 + " 0 " + large + " 1 " + p(r1, a1) + " L" + p(r0, a1) + " A" + r0 + "," + r0 + " 0 " + large + " 0 " + p(r0, a0) + " Z";
  }
  function chRenderDonut(dict, names) {
    const kinds = chKindSum(names), total = chKinds().reduce(function (a, k) { return a + kinds[k]; }, 0);
    const holder = document.getElementById("ch-donut-chart"), legend = document.getElementById("ch-donut-legend");
    holder.textContent = ""; legend.textContent = "";
    const svg = svgEl("svg", { viewBox: "0 0 240 240", class: "cd-svg", role: "group", "aria-label": dict.ch_donut_aria, "data-testid": "ch-donut-svg" });
    let angle = -Math.PI / 2;
    chKinds().forEach(function (k, i) {
      const v = kinds[k];
      const li = make("li"); const sw = make("span", "cd-swatch " + chKindClass(i)); sw.setAttribute("aria-hidden", "true");
      li.appendChild(sw); li.appendChild(make("span", "", chKindLabel(k, dict))); li.appendChild(make("b", "", cdNum(v) + " · " + cdNum(cdPct(v, total)) + " %"));
      li.setAttribute("data-kind", k); li.setAttribute("data-value", String(v)); legend.appendChild(li);
      if (v <= 0 || total <= 0) { return; }
      const sweep = Math.min(v / total, 0.9999) * Math.PI * 2;
      const seg = svgEl("g", { class: "cd-seg", "data-kind": k, "data-value": String(v) });
      cdTipped(seg, tpl(dict.ch_donut_tip, { kind: chKindLabel(k, dict), n: cdNum(v), pc: cdNum(cdPct(v, total)) }));
      seg.appendChild(svgEl("path", { d: chArc(120, 120, 62, 108, angle, angle + sweep), class: chKindClass(i) }));
      svg.appendChild(seg);
      angle += sweep;
    });
    svg.appendChild(svgEl("text", { x: 120, y: 123, "text-anchor": "middle", class: "ch-donut-total" }, cdNum(total)));
    svg.appendChild(svgEl("text", { x: 120, y: 144, "text-anchor": "middle", class: "ch-donut-label" }, dict.ch_entries));
    holder.appendChild(svg);
    cdTable(document.getElementById("ch-donut-table"), dict.ch_donut_title, [dict.ch_det_kind, dict.ch_det_entries, "%"],
      chKinds().map(function (k) { return [chKindLabel(k, dict), cdNum(kinds[k]), cdNum(cdPct(kinds[k], total))]; }));
  }
  /* ---- stacked bars by ecosystem and type ---- */
  function chRenderStack(dict) {
    const names = chAll();
    const rows = [{ name: "all", label: dict.cd_all, kinds: chKindSum(names), group: "all" }];
    CD.ecos.forEach(function (e) { const n = names.filter(function (x) { return CD.repos[x].eco === e.key; }); if (n.length) { rows.push({ name: e.key, label: e.label, kinds: chKindSum(n) }); } });
    CD.types.forEach(function (t) { const n = names.filter(function (x) { return CD.repos[x].type === t; }); if (n.length) { rows.push({ name: t, label: cdTypeLabel(t, dict), kinds: chKindSum(n) }); } });
    rows.forEach(function (r) { r.total = chKinds().reduce(function (a, k) { return a + r.kinds[k]; }, 0); });
    chStackRows(document.getElementById("ch-stack-chart"), rows, dict, "ch-stack-svg", dict.ch_stack_aria);
    chKindLegend(document.getElementById("ch-stack-legend"), dict);
    cdTable(document.getElementById("ch-stack-table"), dict.ch_stack_title, [dict.cd_col_name].concat(chKinds().map(function (k) { return chKindLabel(k, dict); }), [dict.cd_total]),
      rows.map(function (r) { return [r.label].concat(chKindRowCells(r.kinds), [cdNum(r.total)]); }));
  }
  /* ---- evolution ---- */
  function chRenderEvolution(dict) {
    const wrap = document.getElementById("ch-evo-wrap"), msg = document.getElementById("ch-evo-msg"), table = document.getElementById("ch-evo-table");
    table.textContent = "";
    const pts = (CD.history || []).filter(function (p) { return p.c && p.c.repos > 0; }).sort(function (a, b) { return a.d < b.d ? -1 : 1; });
    wrap.hidden = true; msg.hidden = true;
    if (!pts.length) { msg.textContent = dict.cd_evo_none; msg.hidden = false; return; }
    const totalSeries = [["entries", dict.ch_s_entries], ["unreleased", dict.ch_s_unreleased], ["fix", dict.ch_s_fix]].map(function (s) {
      return { id: s[0], name: s[1], cls: "cd-s-" + (s[0] === "entries" ? "code" : s[0] === "unreleased" ? "docs" : "tests"), get: function (p) { return p.c && typeof p.c[s[0]] === "number" ? p.c[s[0]] : null; } };
    });
    const ecoSeries = CD.ecos.map(function (e) { return { id: e.key, name: e.label, cls: "cd-s-" + e.key, get: function (p) { return p.ce && p.ce[e.key] ? p.ce[e.key].entries : null; } }; });
    cdTable(table, dict.ch_evo_title, [dict.cd_evo_date].concat(totalSeries.map(function (s) { return s.name; }), ecoSeries.map(function (s) { return s.name; })),
      pts.map(function (p) { return [p.d].concat(totalSeries.concat(ecoSeries).map(function (s) { const v = s.get(p); return v === null ? "–" : cdNum(v); })); }));
    if (pts.length < 2) { msg.textContent = tpl(dict.cd_evo_one, { date: pts[0].d }); msg.hidden = false; return; }
    cdLineChart(document.getElementById("ch-evo-total"), document.getElementById("ch-evo-total-legend"), totalSeries, pts, dict, dict.ch_evo_title, "ch-evo-total-svg");
    cdLineChart(document.getElementById("ch-evo-eco"), document.getElementById("ch-evo-eco-legend"), ecoSeries, pts, dict, dict.ch_evo_eco_title, "ch-evo-eco-svg");
    wrap.hidden = false;
  }
  /* ---- ranking ---- */
  function chRenderRank(dict, names) {
    const rows = names.map(function (n) {
      const c = CD.repos[n].changes;
      return { name: n, kinds: c.kinds, total: c.entries + c.unreleased, entries: c.entries + c.unreleased, fix: c.kinds.fix || 0 };
    });
    const byVol = rows.slice().sort(function (a, b) { return b.total - a.total || (a.name < b.name ? -1 : 1); }).slice(0, chState.top);
    chStackRows(document.getElementById("ch-rank-vol"), byVol, dict, "ch-rank-vol-svg", tpl(dict.ch_rank_vol_aria, { n: byVol.length }));
    chKindLegend(document.getElementById("ch-rank-legend"), dict);
    cdTable(document.getElementById("ch-rank-vol-table"), dict.ch_rank_vol_title, [dict.cd_col_name].concat(chKinds().map(function (k) { return chKindLabel(k, dict); }), [dict.cd_total]),
      byVol.map(function (r) { return [r.name].concat(chKindRowCells(r.kinds), [cdNum(r.total)]); }));
    const byFix = rows.filter(function (r) { return r.entries >= CH_MIN; }).map(function (r) { return Object.assign({ share: r.fix / r.entries }, r); })
      .sort(function (a, b) { return b.share - a.share || (a.name < b.name ? -1 : 1); }).slice(0, chState.top);
    document.getElementById("ch-rank-fix-hint").textContent = tpl(dict.ch_rank_fix_hint, { min: CH_MIN });
    const holder = document.getElementById("ch-rank-fix");
    holder.textContent = "";
    const W = 900, L = 250, R = 90, ROW = 24;
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + (byFix.length * ROW + 8), class: "cd-svg", role: "group", "aria-label": tpl(dict.ch_rank_fix_aria, { n: byFix.length }), "data-testid": "ch-rank-fix-svg" });
    byFix.forEach(function (r, i) {
      const y = 4 + i * ROW;
      const g = svgEl("g", { "data-row": r.name });
      g.appendChild(svgEl("text", { x: 0, y: y + 15, class: "cd-text" }, r.name));
      svg.appendChild(svgEl("rect", { x: L, y: y + 2, width: W - L - R, height: ROW - 7, rx: 2, class: "cd-track" }));
      const seg = svgEl("g", { class: "cd-seg", "data-value": String(Math.round(r.share * 1000) / 10), style: "--i:" + i });
      cdTipped(seg, tpl(dict.ch_rank_fix_tip, { name: r.name, fix: cdNum(r.fix), n: cdNum(r.entries), pc: cdNum(cdPct(r.fix, r.entries)) }));
      seg.appendChild(svgEl("rect", { x: L, y: y + 2, width: Math.max(1, (W - L - R) * r.share), height: ROW - 7, rx: 2, class: "cd-c-code" }));
      g.appendChild(seg);
      g.appendChild(svgEl("text", { x: W, y: y + 15, "text-anchor": "end", class: "cd-val" }, cdNum(cdPct(r.fix, r.entries)) + " %"));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
    cdTable(document.getElementById("ch-rank-fix-table"), dict.ch_rank_fix_title, [dict.cd_col_name, dict.ch_k_fix, dict.ch_det_entries, dict.ch_rank_share],
      byFix.map(function (r) { return [r.name, cdNum(r.fix), cdNum(r.entries), cdNum(cdPct(r.fix, r.entries)) + " %"]; }));
  }
  /* ---- detail of one repository ---- */
  function chVersions(name) {
    const c = CD.repos[name].changes;
    const keys = chKinds();
    const rows = [];
    if (c.unreleased > 0 || c.u.length) {
      const counts = {}; keys.forEach(function (k) { counts[k] = 0; });
      c.u.forEach(function (e) { counts[keys[e[0]]] += 1; });
      rows.push({ id: "unreleased", name: null, n: c.unreleased, kinds: counts, entries: c.u, detail: true });
    }
    c.v.forEach(function (v) {
      const counts = {}; keys.forEach(function (k, i) { counts[k] = v[2][i]; });
      rows.push({ id: v[0], name: v[0], n: v[1], kinds: counts, entries: v.length > 3 ? v[3] : null, detail: v.length > 3 });
    });
    return rows;
  }
  function chRenderDetail(dict) {
    const sel = document.getElementById("ch-repo"), rangeSel = document.getElementById("ch-range");
    const names = chAll().filter(function (n) { return CD.repos[n].changes.versions > 0 || CD.repos[n].changes.unreleased > 0; });
    sel.textContent = "";
    names.forEach(function (n) { const o = make("option", "", n); o.value = n; sel.appendChild(o); });
    if (!chState.repo || names.indexOf(chState.repo) < 0) {
      chState.repo = names.slice().sort(function (a, b) { return CD.repos[b].changes.versions - CD.repos[a].changes.versions || (a < b ? -1 : 1); })[0] || "";
    }
    sel.value = chState.repo;
    rangeSel.textContent = "";
    [5, 10, 20, 0].forEach(function (n) { const o = make("option", "", n ? tpl(dict.ch_range_last, { n: n }) : dict.ch_range_all); o.value = String(n); rangeSel.appendChild(o); });
    rangeSel.value = String(chState.range);
    const none = document.getElementById("ch-det-none"), wrap = document.getElementById("ch-det-wrap");
    if (!chState.repo) { none.textContent = dict.ch_det_none; none.hidden = false; wrap.hidden = true; return; }
    none.hidden = true; wrap.hidden = false;
    let rows = chVersions(chState.repo);
    const waiting = rows.filter(function (r) { return r.id === "unreleased"; });
    let published = rows.filter(function (r) { return r.id !== "unreleased"; });
    if (chState.range > 0) { published = published.slice(0, chState.range); }
    rows = waiting.concat(published);
    const label = function (r) { return r.name === null ? dict.ch_det_unreleased : r.name; };
    chStackRows(document.getElementById("ch-det-chart"), rows.map(function (r) { return { name: r.id, label: label(r), kinds: r.kinds, total: r.n }; }), dict, "ch-det-svg", tpl(dict.ch_det_chart_aria, { name: chState.repo }));
    const table = document.getElementById("ch-det-table");
    table.textContent = "";
    table.appendChild(make("caption", "sr-only", chState.repo));
    const hr = make("tr");
    [dict.ch_det_version, dict.ch_det_entries].concat(chKinds().map(function (k) { return chKindLabel(k, dict); }), [""]).forEach(function (h, i) {
      const th = make("th", i === 0 ? "cd-left" : "", h); th.setAttribute("scope", "col"); hr.appendChild(th);
    });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    rows.forEach(function (r) {
      const tr = make("tr"); tr.setAttribute("data-version", r.id);
      tr.appendChild(make("td", "cd-left", label(r)));
      tr.appendChild(make("td", "", cdNum(r.n)));
      chKinds().forEach(function (k) { tr.appendChild(make("td", "", cdNum(r.kinds[k]))); });
      const td = make("td", "cd-left"); const b = make("button", "ch-open", dict.ch_det_open); b.type = "button"; b.setAttribute("data-version", r.id); b.setAttribute("data-testid", "ch-open-" + r.id);
      b.setAttribute("aria-label", dict.ch_det_open + ": " + label(r)); b.setAttribute("aria-pressed", chState.version === r.id ? "true" : "false");
      b.addEventListener("click", function () { chState.version = r.id; chState.vq = ""; chState.vkind = "all"; document.getElementById("ch-entry-search").value = ""; chRenderDetail(currentDict()); });
      td.appendChild(b); tr.appendChild(td); body.appendChild(tr);
    });
    table.appendChild(body);
    cdTable(document.getElementById("ch-det-alt"), chState.repo, [dict.ch_det_version, dict.ch_det_entries].concat(chKinds().map(function (k) { return chKindLabel(k, dict); })),
      rows.map(function (r) { return [label(r), cdNum(r.n)].concat(chKindRowCells(r.kinds)); }));
    chRenderEntries(dict, rows);
  }
  function chRenderEntries(dict, rows) {
    const box = document.getElementById("ch-entries");
    const row = (rows || []).filter(function (r) { return r.id === chState.version; })[0];
    if (!row) { box.hidden = true; return; }
    box.hidden = false;
    document.getElementById("ch-entries-title").textContent = tpl(dict.ch_det_entries_title, { version: row.name === null ? dict.ch_det_unreleased : row.name });
    const note = document.getElementById("ch-entries-note");
    note.hidden = row.detail; note.textContent = row.detail ? "" : tpl(dict.ch_det_nodetail, { n: Math.max(0, CD.repos[chState.repo].changes.v.filter(function (v) { return v.length > 3; }).length) });
    const kinds = document.getElementById("ch-entry-kinds");
    kinds.textContent = "";
    [["all", dict.cd_filter_all, row.n]].concat(chKinds().map(function (k) { return [k, chKindLabel(k, dict), row.kinds[k]]; })).forEach(function (c) {
      if (c[0] !== "all" && !c[2]) { return; }
      const b = make("button", "chip"); b.type = "button"; b.setAttribute("data-kind", c[0]); b.setAttribute("data-testid", "ch-entry-kind-" + c[0]); b.setAttribute("aria-pressed", chState.vkind === c[0] ? "true" : "false");
      b.appendChild(make("span", "", c[1])); b.appendChild(document.createTextNode(" ")); b.appendChild(make("b", "", String(c[2])));
      b.addEventListener("click", function () { chState.vkind = c[0]; chRenderEntries(currentDict(), rows); });
      kinds.appendChild(b);
    });
    const list = document.getElementById("ch-entry-list");
    list.textContent = "";
    const entries = row.entries || [];
    const q = chState.vq.trim().toLowerCase();
    const shown = entries.filter(function (e) { return (chState.vkind === "all" || chKinds()[e[0]] === chState.vkind) && (!q || e[1].toLowerCase().indexOf(q) >= 0); });
    shown.forEach(function (e) {
      const li = make("li"); li.setAttribute("data-kind", chKinds()[e[0]]);
      const tag = make("span", "ch-kind-tag"); const sw = make("span", "cd-swatch " + chKindClass(e[0])); sw.setAttribute("aria-hidden", "true");
      tag.appendChild(sw); tag.appendChild(make("span", "", chKindLabel(chKinds()[e[0]], dict)));
      li.appendChild(tag); li.appendChild(make("span", "", e[1])); list.appendChild(li);
    });
    const count = document.getElementById("ch-entry-count");
    count.textContent = row.detail ? (shown.length ? tpl(dict.ch_det_count, { shown: shown.length, total: entries.length }) : dict.ch_det_empty) : "";
    count.setAttribute("data-shown", String(shown.length)); count.setAttribute("data-total", String(entries.length));
  }
  /* ---- the table and its export ---- */
  const CH_COLUMNS = function () {
    return [["name", "cd_col_name", false], ["eco", "cd_col_eco", false], ["type", "cd_col_type", false], ["versions", "ch_col_versions", true], ["entries", "ch_col_entries", true],
      ["unreleased", "ch_col_unreleased", true], ["avg", "ch_col_avg", true]].concat(chKinds().map(function (k) { return ["kind:" + k, "ch_kind_" + k, true]; }),
      [["unclassifiedPc", "ch_col_unclassified_pc", true], ["tags", "ch_col_tags", true], ["last", "ch_col_last", false], ["d30", "ch_col_d30", true], ["d90", "ch_col_d90", true], ["gap", "ch_col_gap", true]]);
  };
  function chFigures(name) {
    const r = CD.repos[name], c = r.changes, rel = r.rel;
    const f = { versions: c.versions, entries: c.entries, unreleased: c.unreleased, tags: rel ? rel.tags : null, last: rel ? rel.last : null, d30: rel ? rel.d30 : null, d90: rel ? rel.d90 : null, gap: rel ? rel.gap : null, kinds: c.kinds };
    return f;
  }
  function chRowOf(label, extra, figs) {
    const row = Object.assign({ name: label.name, eco: label.eco || "", type: label.type || "", repo: label.repo || null }, extra);
    row.versions = figs.versions; row.entries = figs.entries; row.unreleased = figs.unreleased; row.avg = figs.versions ? Math.round(figs.entries / figs.versions * 10) / 10 : null;
    chKinds().forEach(function (k) { row["kind:" + k] = figs.kinds[k] || 0; });
    const total = figs.entries + figs.unreleased;
    row.unclassifiedPc = total ? cdPct(figs.kinds.unclassified || 0, total) : null;
    row.tags = figs.tags; row.last = figs.last; row.d30 = figs.d30; row.d90 = figs.d90; row.gap = figs.gap;
    return row;
  }
  function chMerge(list) {
    const out = { versions: 0, entries: 0, unreleased: 0, tags: null, last: null, d30: null, d90: null, gap: null, kinds: {} };
    chKinds().forEach(function (k) { out.kinds[k] = 0; });
    list.forEach(function (f) {
      out.versions += f.versions; out.entries += f.entries; out.unreleased += f.unreleased;
      chKinds().forEach(function (k) { out.kinds[k] += f.kinds[k] || 0; });
      ["tags", "d30", "d90"].forEach(function (k) { if (f[k] !== null) { out[k] = (out[k] || 0) + f[k]; } });
      if (f.last && (!out.last || f.last > out.last)) { out.last = f.last; }
    });
    return out;
  }
  function chModel(dict) {
    const names = chNames();
    let rows;
    if (chState.group === "repo") {
      rows = names.map(function (n) { const r = CD.repos[n]; return chRowOf({ name: n, eco: r.eco, type: r.type, repo: n }, {}, chFigures(n)); });
    } else {
      const field = chState.group;
      rows = Array.from(new Set(names.map(function (n) { return CD.repos[n][field]; }))).map(function (key) {
        const inGroup = names.filter(function (n) { return CD.repos[n][field] === key; });
        return chRowOf({ name: field === "eco" ? cdEcoLabel(key) : cdTypeLabel(key, dict), key: key }, { key: key }, chMerge(inGroup.map(chFigures)));
      });
    }
    const key = chState.sort, dir = chState.dir;
    const textual = key === "name" || key === "eco" || key === "type" || key === "last";
    rows.sort(function (a, b) {
      let va = a[key], vb = b[key];
      if (key === "eco") { va = cdEcoLabel(a.eco); vb = cdEcoLabel(b.eco); }
      if (key === "type") { va = cdTypeLabel(a.type, dict); vb = cdTypeLabel(b.type, dict); }
      if (textual) { va = String(va || "").toLowerCase(); vb = String(vb || "").toLowerCase(); return (va < vb ? -1 : va > vb ? 1 : 0) * dir || (a.name < b.name ? -1 : 1); }
      if (va === null || va === undefined) { va = -1; } if (vb === null || vb === undefined) { vb = -1; }
      return (va - vb) * dir || (a.name < b.name ? -1 : 1);
    });
    const grouped = chState.group !== "repo";
    const cols = CH_COLUMNS().filter(function (c) { return !(grouped && (c[0] === "eco" || c[0] === "type")); });
    const total = chRowOf({ name: dict.cd_total }, {}, chMerge(names.map(chFigures)));
    return { rows: rows, cols: cols, total: total, names: names };
  }
  function chCell(row, key, dict) {
    const v = row[key];
    if (key === "eco") { return row.eco ? cdEcoLabel(row.eco) : ""; }
    if (key === "type") { return row.type ? cdTypeLabel(row.type, dict) : ""; }
    if (v === null || v === undefined || v === "") { return key === "last" || key === "tags" || key === "d30" || key === "d90" || key === "gap" || key === "avg" || key === "unclassifiedPc" ? dict.ch_unknown : ""; }
    if (key === "unclassifiedPc") { return cdNum(v) + " %"; }
    return typeof v === "number" ? cdNum(v) : String(v);
  }
  function chRenderTable(dict) {
    const model = chModel(dict), table = document.getElementById("ch-table");
    table.textContent = "";
    table.appendChild(make("caption", "sr-only", dict.ch_table_title));
    const hr = make("tr");
    model.cols.forEach(function (c) {
      const th = make("th", c[2] ? "" : "cd-left"); th.setAttribute("scope", "col");
      const label = c[0] === "name" ? (chState.group === "eco" ? dict.cd_filter_eco : chState.group === "type" ? dict.cd_filter_type : dict.cd_col_name) : dict[c[1]];
      const b = make("button", "cd-sort"); b.type = "button"; b.setAttribute("data-sort", c[0]); b.setAttribute("data-testid", "ch-sort-" + c[0].replace(":", "-"));
      b.appendChild(make("span", "", label));
      const active = chState.sort === c[0];
      b.appendChild(make("span", "cd-sort-mark", active ? (chState.dir < 0 ? "↓" : "↑") : "")).setAttribute("aria-hidden", "true");
      th.setAttribute("aria-sort", active ? (chState.dir < 0 ? "descending" : "ascending") : "none");
      b.addEventListener("click", function () {
        if (chState.sort === c[0]) { chState.dir = -chState.dir; } else { chState.sort = c[0]; chState.dir = (c[2] || c[0] === "last") ? -1 : 1; }
        chRenderTable(currentDict());
        const again = document.querySelector('#ch-table [data-sort="' + c[0] + '"]'); if (again) { again.focus(); }
        document.getElementById("ch-live").textContent = tpl(currentDict().cd_sorted, { col: label, dir: chState.dir < 0 ? currentDict().cd_desc : currentDict().cd_asc });
      });
      th.appendChild(b); hr.appendChild(th);
    });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    model.rows.forEach(function (row) {
      const tr = make("tr"); tr.setAttribute("data-row", row.repo || row.key || row.name); tr.setAttribute("data-entries", String(row.entries));
      model.cols.forEach(function (c) {
        const td = make("td", c[2] ? "" : "cd-left");
        if (c[0] === "name" && row.repo) {
          const b = make("button", "cd-name-btn", row.name); b.type = "button"; b.setAttribute("data-repo", row.repo);
          b.addEventListener("click", function () { openPanel(row.repo, b); }); td.appendChild(b);
        } else { td.textContent = c[0] === "name" ? row.name : chCell(row, c[0], dict); }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
    const foot = make("tfoot"), ft = make("tr"); ft.setAttribute("data-testid", "ch-total");
    model.cols.forEach(function (c, i) {
      if (i === 0) { const th = make("th", "", dict.cd_total); th.setAttribute("scope", "row"); ft.appendChild(th); return; }
      ft.appendChild(make("td", c[2] ? "" : "cd-left", ["eco", "type", "last"].indexOf(c[0]) >= 0 && c[0] !== "last" ? "" : chCell(model.total, c[0], dict)));
    });
    foot.appendChild(ft); table.appendChild(foot);
    document.getElementById("ch-none").hidden = model.rows.length > 0;
    document.getElementById("ch-table-wrap").hidden = model.rows.length === 0;
    const counter = document.getElementById("ch-matches");
    counter.textContent = tpl(dict.cd_matches, { shown: model.names.length, total: chAll().length });
    counter.setAttribute("data-shown", String(model.names.length)); counter.setAttribute("data-total", String(chAll().length));
  }
  function chDownload(filename, mime, text) {
    const blob = new Blob([text], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename; a.style.display = "none";
    document.body.appendChild(a); a.click(); a.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
  }
  function chCsvCell(value) {
    let text = value === null || value === undefined ? "" : String(value);
    if (/^[=+\-@\t\r]/.test(text) && isNaN(Number(text))) { text = "'" + text; }            // a spreadsheet must never read a cell as a formula
    return /[",\n\r]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
  }
  function chExport(kind) {
    const dict = currentDict(), model = chModel(dict);
    const rows = model.rows.concat([model.total]);
    const keys = model.cols.map(function (c) { return c[0]; });
    const raw = function (row, key) {
      if (key === "eco") { return row.eco ? cdEcoLabel(row.eco) : ""; }
      if (key === "type") { return row.type || ""; }
      const v = row[key]; return v === undefined ? null : v;
    };
    if (kind === "csv") {
      const lines = [model.cols.map(function (c) { return chCsvCell(c[0] === "name" ? dict.cd_col_name : dict[c[1]]); }).join(",")];
      rows.forEach(function (row) { lines.push(keys.map(function (k) { return chCsvCell(raw(row, k)); }).join(",")); });
      chDownload("changelog-statistics.csv", "text/csv;charset=utf-8", "﻿" + lines.join("\r\n") + "\r\n");
    } else {
      const list = rows.map(function (row) { const o = {}; keys.forEach(function (k) { o[k.replace("kind:", "")] = raw(row, k); }); return o; });
      chDownload("changelog-statistics.json", "application/json", JSON.stringify(list, null, 2) + "\n");
    }
    document.getElementById("ch-live").textContent = tpl(dict.ch_exported, { n: rows.length });
  }
  function chRenderControls(dict) {
    [["ch-eco-chips", "eco", [["all", dict.cd_filter_all, chAll().length]].concat(CD.ecos.map(function (e) { return [e.key, e.label, chAll().filter(function (n) { return CD.repos[n].eco === e.key; }).length]; }))],
     ["ch-type-chips", "type", [["all", dict.cd_filter_all, chAll().length]].concat(CD.types.map(function (t) { return [t, cdTypeLabel(t, dict), chAll().filter(function (n) { return CD.repos[n].type === t; }).length]; }))]
    ].forEach(function (def) {
      const holder = document.getElementById(def[0]);
      holder.textContent = "";
      def[2].forEach(function (c) {
        if (c[0] !== "all" && c[2] === 0) { return; }
        const b = make("button", "chip"); b.type = "button"; b.setAttribute("data-" + def[1], c[0]); b.setAttribute("data-testid", "ch-" + def[1] + "-" + c[0]);
        b.setAttribute("aria-pressed", chState[def[1]] === c[0] ? "true" : "false");
        b.appendChild(make("span", "", c[1])); b.appendChild(document.createTextNode(" ")); b.appendChild(make("b", "", String(c[2])));
        b.addEventListener("click", function () { chState[def[1]] = c[0]; chRenderAll(currentDict()); });
        holder.appendChild(b);
      });
    });
    const sel = document.getElementById("ch-group");
    sel.textContent = "";
    [["repo", dict.cd_by_repo], ["eco", dict.cd_by_eco], ["type", dict.cd_by_type]].forEach(function (o) { const el = make("option", "", o[1]); el.value = o[0]; sel.appendChild(el); });
    sel.value = chState.group;
  }
  function chRenderAll(dict) {
    const names = chNames();
    chRenderControls(dict); chRenderKpis(dict, names); chRenderDonut(dict, names); chRenderRank(dict, names); chRenderTable(dict);
  }
  function chRender(dict) {
    if (!document.getElementById("ch-body")) { return; }
    const all = chAll();
    const missing = !CD.read || all.length === 0;
    const none = document.getElementById("ch-not-read");
    none.hidden = !missing; none.textContent = missing ? dict.ch_not_read : "";
    document.getElementById("ch-main").hidden = missing;
    let unclassified = 0, entries = 0;
    all.forEach(function (n) { const c = CD.repos[n].changes; unclassified += c.kinds.unclassified || 0; entries += c.entries + c.unreleased; });
    document.getElementById("ch-help-body").textContent = tpl(dict.ch_help_body, { unclassified: cdNum(unclassified), n: cdNum(entries) });
    if (missing) { return; }
    chRenderAll(dict); chRenderStack(dict); chRenderEvolution(dict); chRenderDetail(dict);
  }
  (function () {
    const search = document.getElementById("ch-search"), group = document.getElementById("ch-group"), top = document.getElementById("ch-top-n");
    const repo = document.getElementById("ch-repo"), range = document.getElementById("ch-range"), entrySearch = document.getElementById("ch-entry-search");
    if (search) { search.addEventListener("input", function () { chState.q = search.value; chRenderAll(currentDict()); }); }
    if (group) { group.addEventListener("change", function () { chState.group = group.value; chState.sort = "entries"; chState.dir = -1; chRenderTable(currentDict()); }); }
    if (top) { top.addEventListener("change", function () { chState.top = parseInt(top.value, 10) || 15; chRenderRank(currentDict(), chNames()); }); }
    if (repo) { repo.addEventListener("change", function () { chState.repo = repo.value; chState.version = null; chRenderDetail(currentDict()); }); }
    if (range) { range.addEventListener("change", function () { chState.range = parseInt(range.value, 10) || 0; chRenderDetail(currentDict()); }); }
    if (entrySearch) { entrySearch.addEventListener("input", function () { chState.vq = entrySearch.value; chRenderDetail(currentDict()); }); }
    const csv = document.getElementById("ch-export-csv"), json = document.getElementById("ch-export-json");
    if (csv) { csv.addEventListener("click", function () { chExport("csv"); }); }
    if (json) { json.addEventListener("click", function () { chExport("json"); }); }
  })();
"""
