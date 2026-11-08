#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_tests_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Tests" of the dashboard: the automated tests each repository declares, per ecosystem (bars and evolution) and per project (horizontal bars).

The markup is a frame; the charts and lists are drawn in the browser from the JSON the page already embeds (`tests`, see dashboard_tests.py), so the page makes
no request of its own. Every chart has a table with the same figures, nothing relies on colour alone and the motion stops with prefers-reduced-motion. The script
is placed into the shell's own scope (it uses `DATA`, `make`, `tpl`, `svgEl`, `marker`, `dayNumber`, `currentDict` and `openPanel`); `tsRender` is called by
`evoApplied` whenever the language changes. Stdlib only.
"""
from __future__ import annotations

import dashboard_tests_texts
from dashboard_charts import esc

EN = dashboard_tests_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def panel_html() -> str:
    return (
        '<section class="ins ts" id="ts-root" aria-labelledby="ts-title" data-testid="tests-root">'
        f'<header class="ins-head"><h2 class="card-title" id="ts-title" {_t("ts_title")}</h2>'
        f'<span class="ts-badge" data-testid="ts-badge" {_t("ts_badge")}</span></header>'
        f'<p class="muted" {_t("ts_hint")}</p>'
        '<details class="ts-help" data-testid="ts-help">'
        f'<summary {_t("ts_help_summary")}</summary><p id="ts-help-body" data-testid="ts-help-body"></p></details>'
        '<p class="stale-banner" id="ts-stale" role="status" data-testid="ts-stale" hidden></p>'
        '<p class="muted" id="ts-unverified" role="status" data-testid="ts-unverified" hidden></p>'
        f'<p class="no-data" id="ts-not-read" data-testid="ts-not-read" hidden {_t("ts_not_read")}</p>'
        # 1. total per ecosystem
        '<section class="card" aria-labelledby="ts-eco-title"><header class="card-head">'
        f'<h3 class="card-title" id="ts-eco-title" {_t("ts_eco_title")}</h3></header>'
        '<div class="ts-eco-grid"><div class="ts-chart" id="ts-eco-chart" data-testid="ts-eco-chart"></div>'
        '<div class="ins-table-wrap" tabindex="0" role="region" aria-labelledby="ts-eco-title">'
        '<table class="ins-table" id="ts-eco-table" data-testid="ts-eco-table"><thead><tr><th scope="col" data-i18n="ts_col_eco">Ecosystem</th></tr></thead></table></div></div></section>'
        # 2. evolution
        '<section class="card" aria-labelledby="ts-evo-title"><header class="card-head">'
        f'<h3 class="card-title" id="ts-evo-title" {_t("ts_evo_title")}</h3></header><p class="muted" {_t("ts_evo_hint")}</p>'
        '<p class="no-data" id="ts-evo-msg" data-testid="ts-evo-msg" role="status" hidden></p>'
        f'<div class="ts-chart" id="ts-evo-wrap" data-testid="ts-evo-wrap" hidden><svg id="ts-evo-svg" class="evo-svg" viewBox="0 0 900 280" role="img" aria-label="{esc(EN["ts_evo_title"])}" data-testid="ts-evo-svg"></svg>'
        '<ul class="evo-legend" id="ts-evo-legend" data-testid="ts-evo-legend"></ul></div>'
        '<div class="sr-only"><table id="ts-evo-table" data-testid="ts-evo-table"><thead><tr><th scope="col" data-i18n="ts_col_date">Date</th></tr></thead></table></div></section>'
        # 3. per project
        '<section class="card" aria-labelledby="ts-proj-title"><header class="card-head">'
        f'<h3 class="card-title" id="ts-proj-title" {_t("ts_proj_title")}</h3></header><p class="muted" {_t("ts_proj_hint")}</p>'
        '<div class="ev-controls"><div class="ev-group" role="group" aria-labelledby="ts-eco-filter-t">'
        f'<span class="scope-title" id="ts-eco-filter-t" {_t("ts_filter_eco")}</span><span class="chip-row" id="ts-eco-chips" data-testid="ts-eco-chips"></span></div>'
        '<div class="ts-field"><label class="scope-title" for="ts-family" data-i18n="ts_filter_family">Family</label>'
        '<select id="ts-family" data-testid="ts-family"></select></div>'
        '<div class="ts-field"><label class="scope-title" for="ts-search" data-i18n="ts_search">Search a project</label>'
        '<input type="search" id="ts-search" data-testid="ts-search" autocomplete="off" maxlength="80"></div></div>'
        '<p class="matches" id="ts-matches" aria-live="polite" data-testid="ts-matches"></p>'
        '<div class="ts-list-wrap" id="ts-list-wrap" tabindex="0" role="region" aria-labelledby="ts-proj-title" data-testid="ts-list-wrap">'
        '<ul class="ts-list" id="ts-list" data-testid="ts-list"></ul></div>'
        f'<p class="no-data" id="ts-none" data-testid="ts-none" hidden {_t("ts_none")}</p>'
        '<div class="sr-only"><table id="ts-proj-table" data-testid="ts-proj-table"><thead><tr><th scope="col" data-i18n="ts_col_project">Project</th></tr></thead></table></div></section>'
        '</section>'
    )


CSS = r"""
  /* ======================= Tests: declared per ecosystem and per project ======================= */
  .ts-badge { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border: 1px dashed var(--border-strong); border-radius: 999px; font-size: 12px; color: var(--text); background: var(--panel-2); }
  .ts-badge::before { content: "\2139"; font-weight: 700; }
  .ts-help { margin: 6px 0 10px; font-size: 13px; }
  .ts-help summary { cursor: pointer; font-weight: 600; width: fit-content; }
  .ts-help p { margin: 6px 0 0; line-height: 1.5; max-width: 90ch; }
  .ts-chart { margin: 6px 0 10px; min-width: 0; }
  .ts-eco-grid { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 8px 22px; align-items: center; }
  @media (max-width: 1500px) { .ts-eco-grid { grid-template-columns: minmax(0, 1fr); } }
  .ts-svg { width: 100%; height: auto; max-height: 340px; display: block; }
  .ts-grid { stroke: var(--border); stroke-width: 1; }
  .ts-axis-text { fill: var(--dim); font-size: 11px; }
  .ts-name { fill: var(--text); font-size: 12px; font-weight: 600; }
  .ts-value { fill: var(--text); font-size: 13px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .ts-bar { transform-box: fill-box; transform-origin: bottom center; }
  .ts-bar-top { fill: #fff; opacity: .34; pointer-events: none; }
  .ts-bar-g { outline-offset: 3px; cursor: default; }
  .ts-bar-g:hover .ts-bar, .ts-bar-g:focus-visible .ts-bar { filter: brightness(1.2); }
  .ts-e-hydra-umc { fill: var(--c-hydra-umc); background: var(--c-hydra-umc); } .ts-e-urtc { fill: var(--c-urtc); background: var(--c-urtc); }
  .ts-e-armor { fill: var(--c-armor); background: var(--c-armor); } .ts-e-eh3d { fill: var(--c-eh3d); background: var(--c-eh3d); }
  .ts-e-electro-hobby-3d { fill: var(--c-electro-hobby-3d); background: var(--c-electro-hobby-3d); }
  .ts-field { display: inline-flex; flex-direction: column; gap: 3px; }
  .ts-field label { margin: 0; }
  .ts-field select, .ts-field input { background: var(--bg); color: var(--text); border: 1px solid var(--border-strong); border-radius: 8px; padding: 5px 8px; font: inherit; font-size: 13px; min-width: 170px; }
  .ts-list-wrap { max-height: 52vh; overflow: auto; border: 1px solid var(--border); border-radius: 10px; padding: 6px; }
  .ts-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 3px; }
  .ts-row { appearance: none; display: grid; grid-template-columns: minmax(150px, 280px) minmax(60px, 1fr) minmax(110px, 190px); gap: 12px; align-items: center; width: 100%; text-align: left;
            background: none; border: 0; border-radius: 8px; padding: 5px 8px; color: var(--text); font: inherit; font-size: 13px; cursor: pointer; }
  .ts-row:hover { background: var(--panel-2); }
  .ts-row-name { display: inline-flex; gap: 8px; align-items: center; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .ts-dot { flex: 0 0 auto; width: 9px; height: 9px; border-radius: 50%; }
  .ts-track { height: 12px; border-radius: 6px; background: var(--panel-2); box-shadow: inset 0 1px 2px rgba(0,0,0,.3); overflow: hidden; }
  .ts-fill { display: block; height: 100%; width: var(--w, 0%); border-radius: 6px; transform-origin: left center; background-image: linear-gradient(rgba(255,255,255,.3), rgba(255,255,255,0) 55%, rgba(0,0,0,.18)); }
  .ts-row-value { font-variant-numeric: tabular-nums; font-weight: 600; text-align: right; }
  .ts-row-value.ts-muted { color: var(--dim); font-weight: 400; font-style: italic; }
  td.tests-cell { font-variant-numeric: tabular-nums; white-space: nowrap; }
  td.tests-cell.ts-muted { color: var(--dim); font-style: italic; }
  @media (prefers-reduced-motion: no-preference) {
    .ts-bar { animation: t25-grow-y .7s cubic-bezier(.2,.7,.2,1) both; animation-delay: calc(var(--i, 0) * 90ms); }
    .ts-value { animation: t25-fade .45s ease both; animation-delay: calc(var(--i, 0) * 90ms + 380ms); }
    .ts-fill { animation: t25-grow-x .7s cubic-bezier(.2,.7,.2,1) both; }
  }
  @media (max-width: 760px) { .ts-row { grid-template-columns: minmax(0, 1fr) minmax(90px, 40%); } .ts-track { display: none; } .ts-field select, .ts-field input { min-width: 0; width: 100%; } }
  @media print { .ts-list-wrap { max-height: none !important; overflow: visible !important; } .ts-bar, .ts-fill, .ts-value { animation: none !important; } }
"""

JS = r"""
  // ---------------- Tests: the automated tests each repository DECLARES (README or glance file); the dashboard does not run them ----------------
  // Drawn from the JSON embedded in the page. Nothing read = "not verified", never a zero.
  const TS = (DATA.tests && typeof DATA.tests === "object" && DATA.tests.repos) ? DATA.tests : { read: false, repos: {}, series: [], sources: {}, staleDate: null };
  const TS_ECOS = ["hydra-umc", "urtc", "armor", "eh3d"];
  const TS_ALL = TS_ECOS.concat(["electro-hobby-3d"]);
  const TS_LABEL = { "hydra-umc": "HYDRA-UMC", urtc: "URTC", armor: "A.R.M.O.R.", eh3d: "EH3D", "electro-hobby-3d": "Tools" };
  const tsState = { eco: "all", family: "all", q: "" };
  function tsCounts(rec) { return rec && (rec.state === "declared" || rec.state === "lastknown") && rec.unit === "tests" && typeof rec.n === "number"; }
  function tsEcoOf(name) { return (DATA.repos[name] && DATA.repos[name].eco) || ""; }
  function tsAggregate(eco) {
    const out = { n: 0, k: 0, total: 0, checks: 0, undeclared: 0, unread: 0 };
    Object.keys(TS.repos).forEach(function (name) {
      if (tsEcoOf(name) !== eco) { return; }
      const rec = TS.repos[name];
      out.total += 1;
      if (tsCounts(rec)) { out.n += rec.n; out.k += 1; }
      else if (rec.state === "declared" && rec.unit === "checks" && typeof rec.n === "number") { out.checks += rec.n; }
      else if (rec.state === "undeclared") { out.undeclared += 1; }
      else { out.unread += 1; }
    });
    return out;
  }
  function tsSourceText(rec) { return rec && rec.src === "glance" ? "glance.json" : "README"; }
  function tsValueText(rec, dict) {
    if (!rec) { return dict.not_verified; }
    if (rec.state === "declared" && rec.unit === "checks") { return tpl(dict.ts_unit_checks, { n: rec.n }); }
    if (rec.state === "declared") { return tpl(dict.ts_value_tests, { n: rec.n }); }
    if (rec.state === "lastknown") { return tpl(dict.ts_value_tests, { n: rec.n }) + " · " + tpl(dict.ts_st_lastknown, { date: rec.asof }); }
    if (rec.state === "undeclared") { return dict.ts_st_undeclared; }
    return dict.not_verified;
  }
  function tsPanelText(name, dict) {
    const rec = TS.repos[name];
    if (!rec) { return null; }
    return tsValueText(rec, dict) + (rec.state === "declared" ? " · " + tsSourceText(rec) : "");
  }
  function tsNice(max) {
    if (!(max > 0)) { return 10; }
    const pow = Math.pow(10, Math.floor(Math.log(max) / Math.LN10));
    const steps = [1, 2, 2.5, 5, 10];
    for (let i = 0; i < steps.length; i++) { if (steps[i] * pow >= max) { return steps[i] * pow; } }
    return 10 * pow;
  }
  function tsNum(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function tsTable(table, caption, heads, rows, rowHeader) {
    table.textContent = "";
    table.appendChild(make("caption", "", caption));
    const hr = make("tr");
    heads.forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    rows.forEach(function (cells) {
      const tr = make("tr");
      cells.forEach(function (c, i) {
        if (i === 0 && rowHeader) { tr.appendChild(make("th", "", c)).setAttribute("scope", "row"); } else { tr.appendChild(make("td", "", c)); }
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
  }
  function tsRenderEco(dict) {
    const holder = document.getElementById("ts-eco-chart");
    holder.textContent = "";
    const stats = TS_ECOS.map(function (eco) { return { eco: eco, agg: tsAggregate(eco) }; });
    const W = 640, H = 300, L = 58, R = 16, T = 26, B = 46;
    const max = tsNice(Math.max.apply(null, stats.map(function (s) { return s.agg.n; })));
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + H, class: "ts-svg", role: "group", "aria-label": dict.ts_eco_aria, "data-testid": "ts-eco-svg" });
    const py = function (v) { return T + (1 - v / max) * (H - T - B); };
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: py(max * f), y2: py(max * f), class: "ts-grid" }));
      svg.appendChild(svgEl("text", { x: L - 6, y: py(max * f) + 4, "text-anchor": "end", class: "ts-axis-text" }, tsNum(Math.round(max * f))));
    });
    const band = (W - L - R) / stats.length;
    stats.forEach(function (s, i) {
      const cx = L + band * i + band / 2;
      const bw = Math.min(84, band * 0.58);
      const g = svgEl("g", { class: "ts-bar-g", tabindex: "0", role: "img", "data-eco": s.eco, "data-n": s.agg.k ? s.agg.n : "" });
      const tip = s.agg.k ? tpl(dict.ts_bar_tip, { eco: TS_LABEL[s.eco], n: s.agg.n, k: s.agg.k, total: s.agg.total }) : TS_LABEL[s.eco] + ": " + dict.not_verified;
      g.setAttribute("aria-label", tip);
      g.appendChild(svgEl("title", {}, tip));
      if (s.agg.k) {
        const y = py(s.agg.n);
        const h = Math.max(2, H - B - y);
        const bar = svgEl("rect", { x: cx - bw / 2, y: H - B - h, width: bw, height: h, rx: 3, class: "ts-bar ts-e-" + s.eco, style: "--i:" + i });
        g.appendChild(bar);
        g.appendChild(svgEl("rect", { x: cx - bw / 2, y: H - B - h, width: bw, height: Math.min(4, h), rx: 2, class: "ts-bar-top" }));
        g.appendChild(svgEl("text", { x: cx, y: H - B - h - 7, "text-anchor": "middle", class: "ts-value", style: "--i:" + i }, tsNum(s.agg.n)));
      } else {
        g.appendChild(svgEl("text", { x: cx, y: H - B - 8, "text-anchor": "middle", class: "ts-axis-text" }, dict.not_verified));
      }
      g.appendChild(svgEl("text", { x: cx, y: H - B + 20, "text-anchor": "middle", class: "ts-name" }, TS_LABEL[s.eco]));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
    tsTable(document.getElementById("ts-eco-table"), dict.ts_eco_caption,
      [dict.ts_col_eco, dict.ts_col_tests, dict.ts_col_checks, dict.ts_col_declared, dict.ts_col_undeclared, dict.ts_col_unread],
      stats.map(function (s) {
        return [TS_LABEL[s.eco], s.agg.k ? tsNum(s.agg.n) : dict.not_verified, s.agg.checks ? tsNum(s.agg.checks) : "–", s.agg.k + " / " + s.agg.total, String(s.agg.undeclared), String(s.agg.unread)];
      }), true);
  }
  function tsRenderEvo(dict) {
    const wrap = document.getElementById("ts-evo-wrap");
    const msg = document.getElementById("ts-evo-msg");
    const svg = document.getElementById("ts-evo-svg");
    const legend = document.getElementById("ts-evo-legend");
    const table = document.getElementById("ts-evo-table");
    svg.textContent = ""; legend.textContent = ""; table.textContent = "";
    const pts = (TS.series || []).slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; });
    wrap.hidden = true; msg.hidden = true;
    if (!pts.length) { msg.textContent = dict.ts_evo_none; msg.hidden = false; return; }
    const first = pts[0].date, last = pts[pts.length - 1].date;
    tsTable(table, tpl(dict.ts_evo_aria, { first: first, last: last }), [dict.ts_col_date].concat(TS_ECOS.map(function (e) { return TS_LABEL[e]; })),
      pts.map(function (p) { return [p.date].concat(TS_ECOS.map(function (e) { return p.eco[e] ? tpl(dict.ts_evo_cell, { n: p.eco[e].n, k: p.eco[e].k }) : dict.not_verified; })); }), true);
    if (pts.length < 2) { msg.textContent = tpl(dict.ts_evo_one, { date: first }); msg.hidden = false; return; }
    const W = 900, H = 280, L = 56, R = 110, T = 14, B = 30;
    let top = 0;
    pts.forEach(function (p) { TS_ECOS.forEach(function (e) { if (p.eco[e]) { top = Math.max(top, p.eco[e].n); } }); });
    const max = tsNice(top);
    const d0 = dayNumber(first), d1 = dayNumber(last);
    const px = function (iso) { return L + (dayNumber(iso) - d0) / Math.max(1, d1 - d0) * (W - L - R); };
    const py = function (v) { return T + (1 - v / max) * (H - T - B); };
    svg.setAttribute("aria-label", tpl(dict.ts_evo_aria, { first: first, last: last }));
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: py(max * f), y2: py(max * f), class: "evo-grid" }));
      svg.appendChild(svgEl("text", { x: L - 6, y: py(max * f) + 4, "text-anchor": "end", class: "evo-axis-text" }, tsNum(Math.round(max * f))));
    });
    [[first, "start", L], [last, "end", W - R]].forEach(function (t) { svg.appendChild(svgEl("text", { x: t[2], y: H - 8, "text-anchor": t[1], class: "evo-axis-text" }, t[0])); });
    const ends = [];
    TS_ECOS.forEach(function (eco, kind) {
      const cls = "evo-s-" + eco;
      let seg = [];
      let prev = null;
      let lastPt = null;
      const flush = function () { if (seg.length > 1) { svg.appendChild(svgEl("path", { d: "M" + seg.join(" L"), class: "evo-line " + cls, pathLength: 1 })); } seg = []; };
      pts.forEach(function (p) {
        const v = p.eco[eco] ? p.eco[eco].n : null;
        if (v === null) { flush(); prev = null; return; }
        if (prev !== null && dayNumber(p.date) - prev > 1) { flush(); }
        prev = dayNumber(p.date);
        seg.push(px(p.date).toFixed(1) + "," + py(v).toFixed(1));
        lastPt = { y: py(v), v: v };
      });
      flush();
      pts.forEach(function (p, i) {
        const v = p.eco[eco] ? p.eco[eco].n : null;
        if (v !== null && (pts.length <= 31 || i === pts.length - 1 || i % 7 === 0)) {
          svg.appendChild(marker(kind, px(p.date), py(v), cls, tpl(dict.ts_evo_point, { eco: TS_LABEL[eco], date: p.date, n: v, k: p.eco[eco].k })));
        }
      });
      if (lastPt) { ends.push({ eco: eco, y: lastPt.y, v: lastPt.v }); }
    });
    ends.sort(function (a, b) { return a.y - b.y; });
    for (let i = 1; i < ends.length; i++) { if (ends[i].y - ends[i - 1].y < 13) { ends[i].y = ends[i - 1].y + 13; } }
    ends.forEach(function (e) { svg.appendChild(svgEl("text", { x: W - R + 6, y: e.y + 4, class: "evo-end-label evo-s-" + e.eco }, TS_LABEL[e.eco] + " " + tsNum(e.v))); });
    TS_ECOS.forEach(function (eco, kind) {
      const li = make("li"); const key = svgEl("svg", { viewBox: "0 0 16 12", "aria-hidden": "true" });
      key.appendChild(svgEl("line", { x1: 0, x2: 16, y1: 6, y2: 6, class: "evo-line evo-s-" + eco, style: "animation:none;stroke-dasharray:none;stroke-dashoffset:0" }));
      key.appendChild(marker(kind, 8, 6, "evo-s-" + eco, TS_LABEL[eco]));
      li.appendChild(key); li.appendChild(make("span", "", TS_LABEL[eco])); legend.appendChild(li);
    });
    wrap.hidden = false;
  }
  function tsSortKey(rec) {
    if (tsCounts(rec)) { return [0, -rec.n]; }
    if (rec.state === "declared") { return [1, 0]; }
    if (rec.state === "undeclared") { return [2, 0]; }
    return [3, 0];
  }
  function tsRenderProjects(dict) {
    const chips = document.getElementById("ts-eco-chips");
    chips.textContent = "";
    const all = Object.keys(TS.repos);
    [["all", dict.ts_filter_all, all.length]].concat(TS_ALL.map(function (e) { return [e, TS_LABEL[e], all.filter(function (n) { return tsEcoOf(n) === e; }).length]; })).forEach(function (c) {
      if (c[0] !== "all" && c[2] === 0) { return; }
      const b = make("button", "chip"); b.type = "button"; b.setAttribute("data-ts-eco", c[0]); b.setAttribute("data-testid", "ts-eco-" + c[0]);
      b.setAttribute("aria-pressed", tsState.eco === c[0] ? "true" : "false");
      b.appendChild(make("span", "", c[1])); b.appendChild(document.createTextNode(" ")); b.appendChild(make("b", "", String(c[2])));
      b.addEventListener("click", function () { tsState.eco = c[0]; tsState.family = "all"; tsRenderProjects(currentDict()); });
      chips.appendChild(b);
    });
    const inEco = all.filter(function (n) { return tsState.eco === "all" || tsEcoOf(n) === tsState.eco; });
    const families = Array.from(new Set(inEco.map(function (n) { return (DATA.repos[n] || {}).family || ""; }).filter(Boolean))).sort();
    if (tsState.family !== "all" && families.indexOf(tsState.family) < 0) { tsState.family = "all"; }
    const sel = document.getElementById("ts-family");
    sel.textContent = "";
    const o0 = make("option", "", dict.ts_filter_family_all); o0.value = "all"; sel.appendChild(o0);
    families.forEach(function (f) { const o = make("option", "", f); o.value = f; sel.appendChild(o); });
    sel.value = tsState.family;
    const q = tsState.q.trim().toLowerCase();
    const names = inEco.filter(function (n) {
      if (tsState.family !== "all" && (DATA.repos[n] || {}).family !== tsState.family) { return false; }
      return !q || n.toLowerCase().indexOf(q) >= 0;
    }).sort(function (a, b) {
      const ka = tsSortKey(TS.repos[a]), kb = tsSortKey(TS.repos[b]);
      if (ka[0] !== kb[0]) { return ka[0] - kb[0]; }
      if (ka[1] !== kb[1]) { return ka[1] - kb[1]; }
      return a.toLowerCase() < b.toLowerCase() ? -1 : 1;
    });
    let max = 0;
    names.forEach(function (n) { if (tsCounts(TS.repos[n])) { max = Math.max(max, TS.repos[n].n); } });
    const list = document.getElementById("ts-list");
    list.textContent = "";
    names.forEach(function (name, i) {
      const rec = TS.repos[name];
      const eco = tsEcoOf(name);
      const li = make("li");
      const b = make("button", "ts-row"); b.type = "button"; b.setAttribute("data-repo", name); b.setAttribute("data-state", rec.state);
      if (tsCounts(rec)) { b.setAttribute("data-n", String(rec.n)); }
      const text = tsValueText(rec, dict);
      b.setAttribute("aria-label", tpl(dict.ts_row_aria, { name: name, value: text }));
      if (rec.state === "declared") { b.title = tpl(dict.ts_tip_source, { src: tsSourceText(rec) }); }
      const nameEl = make("span", "ts-row-name"); const dot = make("span", "ts-dot ts-e-" + eco); dot.setAttribute("aria-hidden", "true");
      nameEl.appendChild(dot); nameEl.appendChild(make("span", "", name)); b.appendChild(nameEl);
      const track = make("span", "ts-track"); track.setAttribute("aria-hidden", "true");
      if (tsCounts(rec) && max > 0) { const fill = make("span", "ts-fill ts-e-" + eco); fill.style.setProperty("--w", Math.max(1.5, rec.n / max * 100).toFixed(1) + "%"); fill.style.animationDelay = Math.min(i, 30) * 25 + "ms"; track.appendChild(fill); }
      b.appendChild(track);
      b.appendChild(make("span", "ts-row-value" + (tsCounts(rec) || rec.state === "declared" ? "" : " ts-muted"), text));
      b.addEventListener("click", function () { openPanel(name, b); });
      li.appendChild(b); list.appendChild(li);
    });
    document.getElementById("ts-none").hidden = names.length > 0 || all.length === 0;
    document.getElementById("ts-list-wrap").hidden = names.length === 0;
    const counter = document.getElementById("ts-matches");
    counter.textContent = tpl(dict.ts_matches, { shown: names.length, total: all.length });
    counter.setAttribute("data-shown", String(names.length)); counter.setAttribute("data-total", String(all.length));
    tsTable(document.getElementById("ts-proj-table"), dict.ts_proj_caption, [dict.ts_col_project, dict.ts_col_eco, dict.ts_col_tests, dict.ts_col_state, dict.ts_col_source],
      names.map(function (n) {
        const r = TS.repos[n];
        return [n, TS_LABEL[tsEcoOf(n)] || "", tsCounts(r) ? String(r.n) : r.state === "declared" ? tpl(dict.ts_unit_checks, { n: r.n }) : "–",
          r.state === "lastknown" ? tpl(dict.ts_st_lastknown, { date: r.asof }) : dict["ts_st_" + r.state], r.state === "declared" ? tsSourceText(r) : "–"];
      }), true);
  }
  function tsRenderCells(dict) {
    document.querySelectorAll("td.tests-cell[data-tests-for]").forEach(function (cell) {
      const rec = TS.repos[cell.getAttribute("data-tests-for")];
      let text = dict.not_verified, muted = true;
      if (rec && tsCounts(rec)) { text = rec.state === "lastknown" ? tsNum(rec.n) + " (" + rec.asof + ")" : tsNum(rec.n); muted = false; }
      else if (rec && rec.state === "declared") { text = tpl(dict.ts_unit_checks, { n: rec.n }); muted = false; }
      else if (rec && rec.state === "undeclared") { text = dict.ts_st_undeclared; }
      cell.textContent = text;
      cell.classList.toggle("ts-muted", muted);
      cell.title = rec && rec.state === "declared" ? tpl(dict.ts_tip_source, { src: tsSourceText(rec) }) : "";
    });
  }
  function tsRender(dict) {
    if (!document.getElementById("ts-root")) { return; }
    const names = Object.keys(TS.repos);
    const stale = names.filter(function (n) { return TS.repos[n].state === "lastknown"; });
    const unread = names.filter(function (n) { return TS.repos[n].state === "unread"; });
    const banner = document.getElementById("ts-stale");
    banner.hidden = stale.length === 0;
    banner.textContent = stale.length ? tpl(dict.ts_stale, { n: stale.length, date: TS.staleDate || "" }) : "";
    const note = document.getElementById("ts-unverified");
    note.hidden = unread.length === 0 || unread.length === names.length;
    note.textContent = tpl(dict.ts_unverified_note, { n: unread.length });
    document.getElementById("ts-not-read").hidden = !(names.length > 0 && unread.length === names.length);
    const src = TS_ALL.filter(function (e) { return TS.sources && TS.sources[e]; }).map(function (e) {
      const s = TS.sources[e];
      return TS_LABEL[e] + ": " + [s.glance || "", s.readme ? "README" : ""].filter(Boolean).join(" + ");
    }).join("; ");
    document.getElementById("ts-help-body").textContent = tpl(dict.ts_help_body, { sources: src });
    tsRenderEco(dict); tsRenderEvo(dict); tsRenderProjects(dict); tsRenderCells(dict);
  }
  (function () {
    const sel = document.getElementById("ts-family");
    const search = document.getElementById("ts-search");
    if (sel) { sel.addEventListener("change", function () { tsState.family = sel.value; tsRenderProjects(currentDict()); }); }
    if (search) { search.addEventListener("input", function () { tsState.q = search.value; tsRenderProjects(currentDict()); }); }
  })();
"""
