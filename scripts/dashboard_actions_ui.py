#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_actions_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Actions / Builds" of the dashboard: result of the runs of the last 24 hours (ring), success rate and duration per repository, a 24-hour timeline,
the runs per day and a table with the last run of each repository.

The markup is a frame; everything is drawn in the browser from the JSON the page already embeds (`actions`, see dashboard_actions.py), so the page makes no
request of its own. Nothing relies on colour alone (every result has a glyph and a word), every chart has its figures in the table and the motion stops with
prefers-reduced-motion. The script is placed into the shell's own scope (it uses `DATA`, `make`, `tpl`, `svgEl`, `marker`, `currentDict` and `openPanel`);
`acRender` is called by `evoApplied` whenever the language changes. Stdlib only.
"""
from __future__ import annotations

import dashboard_actions_texts
from dashboard_charts import esc

EN = dashboard_actions_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def panel_html() -> str:
    return (
        '<section class="ins ac" id="ac-root" aria-labelledby="ac-title" data-testid="actions-root">'
        f'<header class="ins-head"><h2 class="card-title" id="ac-title" {_t("ac_title")}</h2>'
        f'<span class="ts-badge" data-testid="ac-badge" {_t("ac_badge")}</span>'
        '<span class="muted ac-unv" id="ac-unverified" role="status" data-testid="ac-unverified" hidden></span>'
        '<span class="muted ac-asof" id="ac-asof" data-testid="ac-asof"></span></header>'
        f'<p class="muted ac-hint" {_t("ac_hint")}</p>'
        '<p class="stale-banner" id="ac-stale" role="status" data-testid="ac-stale" hidden></p>'
        f'<p class="no-data" id="ac-not-read" data-testid="ac-not-read" hidden {_t("ac_not_read")}</p>'
        '<ul class="ac-kpis" id="ac-kpis" data-testid="ac-kpis"></ul>'
        '<div class="ac-grid">'
        # 1. ring
        '<section class="card" aria-labelledby="ac-ring-title"><header class="card-head">'
        f'<h3 class="card-title" id="ac-ring-title" {_t("ac_ring_title")}</h3></header>'
        '<div class="ac-ring-box"><div id="ac-ring" data-testid="ac-ring"></div><ul class="ac-legend" id="ac-legend" data-testid="ac-legend"></ul></div></section>'
        # 2. success rate
        '<section class="card" aria-labelledby="ac-rate-title"><header class="card-head">'
        f'<h3 class="card-title" id="ac-rate-title" {_t("ac_rate_title")}</h3></header>'
        '<ul class="ac-bars" id="ac-rate" data-testid="ac-rate"></ul>'
        f'<p class="no-data" id="ac-rate-none" data-testid="ac-rate-none" hidden {_t("ac_rate_none")}</p></section>'
        # 3. duration
        '<section class="card" aria-labelledby="ac-dur-title"><header class="card-head">'
        f'<h3 class="card-title" id="ac-dur-title" {_t("ac_dur_title")}</h3></header>'
        '<ul class="ac-bars" id="ac-dur" data-testid="ac-dur"></ul>'
        f'<p class="no-data" id="ac-dur-none" data-testid="ac-dur-none" hidden {_t("ac_rate_none")}</p></section>'
        # 4. timeline
        '<section class="card ac-wide" aria-labelledby="ac-tl-title"><header class="card-head">'
        f'<h3 class="card-title" id="ac-tl-title" {_t("ac_tl_title")}</h3></header>'
        f'<p class="no-data" id="ac-tl-none" data-testid="ac-tl-none" hidden {_t("ac_tl_none")}</p>'
        f'<svg id="ac-tl" class="ac-tl" viewBox="0 0 900 240" role="img" aria-label="{esc(EN["ac_tl_title"])}" data-testid="ac-tl" hidden style="display:none"></svg></section>'
        # 5. runs per day
        '<section class="card" aria-labelledby="ac-trend-title"><header class="card-head">'
        f'<h3 class="card-title" id="ac-trend-title" {_t("ac_trend_title")}</h3></header>'
        f'<p class="no-data" id="ac-trend-none" data-testid="ac-trend-none" hidden {_t("ac_trend_none")}</p>'
        f'<svg id="ac-trend" class="ac-trend" viewBox="0 0 320 170" role="group" aria-label="{esc(EN["ac_trend_title"])}" data-testid="ac-trend" hidden style="display:none"></svg></section>'
        '</div>'
        # 6. table
        '<section class="card ac-table-card" aria-labelledby="ac-table-title"><header class="card-head">'
        f'<h3 class="card-title" id="ac-table-title" {_t("ac_table_title")}</h3>'
        '<span class="matches" id="ac-matches" aria-live="polite" data-testid="ac-matches"></span></header>'
        '<div class="ev-controls"><div class="ev-group" role="group" aria-labelledby="ac-eco-t">'
        f'<span class="scope-title" id="ac-eco-t" {_t("ac_filter_eco")}</span><span class="chip-row" id="ac-eco-chips" data-testid="ac-eco-chips"></span></div>'
        '<div class="ts-field"><label class="scope-title" for="ac-search" data-i18n="ac_search">Search a repository</label>'
        '<input type="search" id="ac-search" data-testid="ac-search" autocomplete="off" maxlength="80"></div></div>'
        '<div class="ins-table-wrap ac-table-wrap" tabindex="0" role="region" aria-labelledby="ac-table-title" id="ac-table-wrap" data-testid="ac-table-wrap">'
        '<table class="ins-table ac-table" id="ac-table" data-testid="ac-table"><thead><tr><th scope="col" data-i18n="ac_col_repo">Repository</th></tr></thead></table></div>'
        f'<p class="no-data" id="ac-none" data-testid="ac-none" hidden {_t("ac_none_match")}</p>'
        '<div class="ac-foot"><details class="ts-help" data-testid="ac-help">'
        f'<summary {_t("ac_help_summary")}</summary><p id="ac-help-body" data-testid="ac-help-body"></p></details>'
        f'<p class="muted ac-note" data-testid="ac-note" {_t("ac_compute_note")}</p></div></section>'
        '</section>'
    )


CSS = r"""
  /* ======================= Actions / Builds ======================= */
  #panel-actions .panel-inner { height: 100%; max-width: none; }
  .ac { display: flex; flex-direction: column; gap: 8px; height: 100%; min-height: 0; }
  .ac .ins-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
  .ac-asof { font-size: 12px; margin-left: auto; font-variant-numeric: tabular-nums; }
  .ac-hint { margin: 0; font-size: 12.5px; }
  .ac-unv { font-size: 12px; }
  .ac-foot { display: flex; flex-wrap: wrap; gap: 4px 18px; align-items: baseline; margin-top: 4px; }
  .ac-foot .ts-help { margin: 0; }
  .ac-foot .ts-help p { max-width: 110ch; }
  .ac .ts-field { flex-direction: row; align-items: center; gap: 8px; }
  .ac .ev-controls { align-items: center; margin-bottom: 4px; }
  .ac-kpis { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 8px; }
  .ac-kpi { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 7px 12px; display: flex; flex-direction: column; min-width: 0; }
  .ac-kpi b { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 22px; line-height: 1.15; font-variant-numeric: tabular-nums; }
  .ac-kpi span { font-size: 11.5px; color: var(--dim); }
  .ac-kpi.ac-bad { border-color: var(--err); background: var(--err-soft); }
  .ac-kpi.ac-bad b { color: var(--err); }
  .ac-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
  .ac-grid .card { padding: 9px 12px; }
  .ac-grid .card-head { margin-bottom: 4px; }
  .ac-wide { grid-column: span 2; }
  .ac-ring-box { display: flex; align-items: center; gap: 14px; }
  .ac-ring-box svg { width: 128px; height: 128px; flex: 0 0 auto; }
  .ac-ring-seg { fill: none !important; stroke-width: 15; }
  .ac-ring-num { fill: var(--text); font-size: 24px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .ac-ring-sub { fill: var(--dim); font-size: 10px; }
  .ac-legend { list-style: none; margin: 0; padding: 0; display: grid; gap: 3px; font-size: 12.5px; min-width: 0; }
  .ac-legend li { display: flex; align-items: center; gap: 7px; }
  .ac-legend b { margin-left: auto; font-variant-numeric: tabular-nums; }
  .ac-sw { display: inline-flex; align-items: center; justify-content: center; width: 17px; height: 17px; border-radius: 4px; font-size: 11px; font-weight: 800; color: var(--ink-on-fill); flex: 0 0 auto; }
  .ac-c-s { background: var(--k-success); fill: var(--k-success); stroke: var(--k-success); }
  .ac-c-f { background: var(--k-failure); fill: var(--k-failure); stroke: var(--k-failure); }
  .ac-c-c { background: #94a3b8; fill: #94a3b8; stroke: #94a3b8; }
  .ac-c-k { background: #a78bfa; fill: #a78bfa; stroke: #a78bfa; }
  .ac-c-p { background: var(--k-pending); fill: var(--k-pending); stroke: var(--k-pending); }
  .ac-bars { list-style: none; margin: 0; padding: 0; display: grid; gap: 1px; }
  .ac-bar { appearance: none; display: grid; grid-template-columns: minmax(90px, 40%) minmax(30px, 1fr) auto; gap: 8px; align-items: center; width: 100%; text-align: left; background: none; border: 0; border-radius: 6px;
            padding: 2px 6px; min-height: 24px; color: var(--text); font: inherit; font-size: 12px; cursor: pointer; }
  .ac-bar:hover { background: var(--panel-2); }
  .ac-bar-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .ac-track { height: 9px; border-radius: 5px; background: var(--panel-2); overflow: hidden; }
  .ac-fill { display: block; height: 100%; width: var(--w, 0%); border-radius: 5px; transform-origin: left center; }
  .ac-bar-val { font-variant-numeric: tabular-nums; font-weight: 600; text-align: right; white-space: nowrap; }
  .ac-tl { width: 100%; height: auto; max-height: 190px; display: block; }
  .ac-tl-name { fill: var(--text); font-size: 11.5px; }
  .ac-tl-row { stroke: var(--border); stroke-width: 1; }
  .ac-tl-grid { stroke: var(--border); stroke-width: 1; stroke-dasharray: 3 4; }
  .ac-tl-axis { fill: var(--dim); font-size: 11px; }
  .ac-tl .evo-mark { stroke: none; }
  .ac-trend { width: 100%; height: auto; max-height: 176px; display: block; }
  .ac-col { outline-offset: 2px; }
  .ac-col:hover rect, .ac-col:focus-visible rect { filter: brightness(1.2); }
  .ac-table-card { padding: 9px 12px; flex: 1 1 auto; min-height: 190px; display: flex; flex-direction: column; }
  .ac-table-wrap { flex: 1 1 auto; min-height: 0; overflow: auto; }
  #ac-table.ac-table { width: 100% !important; }
  .ac-table th, .ac-table td { white-space: nowrap; font-size: 12px; padding: 3px 8px; }
  .ac-table td.num { font-variant-numeric: tabular-nums; text-align: right; }
  .ac-table th[scope=row] { text-align: left; font-weight: 600; }
  .ac-link { appearance: none; background: none; border: 0; padding: 0; color: var(--accent); font: inherit; font-weight: 600; cursor: pointer; text-decoration: underline; text-underline-offset: 2px; }
  .ac-res { display: inline-flex; align-items: center; gap: 6px; }
  .ac-note { margin: 0; font-size: 11.5px; flex: 1 1 400px; }
  .ac-muted { color: var(--dim); font-style: italic; }
  @media (prefers-reduced-motion: no-preference) {
    .ac-fill { animation: t25-grow-x .7s cubic-bezier(.2,.7,.2,1) both; }
    .ac-ring-seg { animation: t25-fade .6s ease both; }
    .ac-col rect { transform-box: fill-box; transform-origin: bottom center; animation: t25-grow-y .6s cubic-bezier(.2,.7,.2,1) both; }
  }
  @media (max-width: 1250px) { .ac-kpi b { font-size: 19px; } }
  @media (max-width: 1100px) { .ac-kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); } #panel-actions .panel-inner, .ac { height: auto; } .ac-grid { grid-template-columns: minmax(0, 1fr); } .ac-wide { grid-column: auto; } .ac-table-wrap { max-height: 60vh; } }
  @media (max-width: 760px) { .ac-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); } .ac-asof { margin-left: 0; } .ac-ring-box { flex-wrap: wrap; } }
  @media print { #panel-actions .panel-inner, .ac { height: auto !important; } .ac-table-wrap { max-height: none !important; overflow: visible !important; } .ac-fill, .ac-ring-seg, .ac-col rect { animation: none !important; } }
"""

JS = r"""
  // ---------------- Actions / Builds: state and figures of the GitHub Actions runs, read when the page was generated ----------------
  // Drawn from the JSON embedded in the page; nothing is requested. A repository that could not be read is "not verified", never a green state.
  const AC = (DATA.actions && typeof DATA.actions === "object" && DATA.actions.repos) ? DATA.actions : { read: false, repos: {}, daily: [], asof: null, stale: null, problems: 0 };
  const AC_CODES = ["s", "f", "c", "k", "p"];
  const AC_GLYPH = { s: "✓", f: "✕", c: "⊘", k: "–", p: "●" };
  const AC_ECOS = ["hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"];
  const AC_LABEL = { "hydra-umc": "HYDRA-UMC", urtc: "URTC", armor: "A.R.M.O.R.", eh3d: "EH3D", "electro-hobby-3d": "Electro Hobby 3D" };
  const acState = { eco: "all", q: "" };
  const acAsofMs = AC.asof ? Date.parse(AC.asof) : NaN;
  function acEco(name) { return (DATA.repos[name] && DATA.repos[name].eco) || ""; }
  function acNum(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function acSince() { return isNaN(acAsofMs) ? 0 : Math.max(0, (Date.now() - acAsofMs) / 60000); }
  function acAgo(minutes, dict) {
    const m = Math.round(minutes + acSince());
    if (m < 120) { return tpl(dict.ac_ago_min, { n: m }); }
    if (m < 48 * 60) { return tpl(dict.ac_ago_h, { n: Math.round(m / 60) }); }
    return tpl(dict.ac_ago_d, { n: Math.round(m / 1440) });
  }
  function acDuration(sec, dict) {
    if (typeof sec !== "number") { return "–"; }
    if (sec < 90) { return tpl(dict.ac_dur_sec, { n: sec }); }
    if (sec < 3600) { return tpl(dict.ac_dur_min, { n: Math.round(sec / 60) }); }
    return tpl(dict.ac_dur_hour, { h: Math.floor(sec / 3600), m: Math.round((sec % 3600) / 60) });
  }
  function acApprox(min, dict) { return min < 120 ? tpl(dict.ac_approx_min, { n: acNum(min) }) : tpl(dict.ac_approx_h, { n: acNum(Math.round(min / 60)) }); }
  function acOk(rec) { return rec && rec.state === "ok"; }
  function acTotals() {
    const t = { n: [0, 0, 0, 0, 0], min: 0, bf: 0, bs: 0, ok: 0, none: 0, unread: 0, total: 0 };
    Object.keys(AC.repos).forEach(function (name) {
      const rec = AC.repos[name];
      t.total += 1;
      if (rec.state === "ok") { t.ok += 1; t.min += rec.min || 0; AC_CODES.forEach(function (c, i) { t.n[i] += rec.n[i]; }); }
      else if (rec.state === "none") { t.none += 1; } else { t.unread += 1; }
      t.bf += rec.bf || 0; t.bs += rec.bs || 0;
    });
    return t;
  }
  function acRate(counts) { const d = counts[0] + counts[1]; return d ? Math.round(counts[0] / d * 100) : null; }
  function acResultText(code, dict) { return dict["ac_res_" + code]; }
  function acSwatch(code) { const s = make("span", "ac-sw ac-c-" + code, AC_GLYPH[code]); s.setAttribute("aria-hidden", "true"); return s; }
  function acKpis(t, dict) {
    const list = document.getElementById("ac-kpis");
    list.textContent = "";
    const total24 = t.n.reduce(function (a, b) { return a + b; }, 0);
    const rate = acRate(t.n);
    const unknown = !AC.read;
    const items = [
      ["runs", unknown ? dict.not_verified : acNum(total24), dict.ac_k_runs, false],
      ["rate", unknown ? dict.not_verified : (rate === null ? "–" : rate + " %"), dict.ac_k_rate, rate !== null && rate < 80],
      ["min", unknown ? dict.not_verified : acApprox(t.min, dict), dict.ac_k_min, false],
      ["failed", unknown ? dict.not_verified : String(t.bf), dict.ac_k_failed, !unknown && t.bf > 0],
      ["stuck", unknown ? dict.not_verified : String(t.bs), dict.ac_k_stuck, !unknown && t.bs > 0],
      ["read", tpl(dict.ac_of, { n: t.ok + t.none, m: t.total }), dict.ac_k_read, false]
    ];
    items.forEach(function (it) {
      const li = make("li", "ac-kpi" + (it[3] ? " ac-bad" : ""));
      li.setAttribute("data-testid", "ac-k-" + it[0]);
      li.appendChild(make("b", "", it[1])); li.appendChild(make("span", "", it[2]));
      list.appendChild(li);
    });
  }
  function acRing(t, dict) {
    const holder = document.getElementById("ac-ring");
    const legend = document.getElementById("ac-legend");
    holder.textContent = ""; legend.textContent = "";
    const total = t.n.reduce(function (a, b) { return a + b; }, 0);
    const R = 44, C = 2 * Math.PI * R;
    const svg = svgEl("svg", { viewBox: "0 0 120 120", role: "img" });
    const parts = AC_CODES.filter(function (c, i) { return t.n[i] > 0; }).map(function (c) { return acResultText(c, dict) + " " + t.n[AC_CODES.indexOf(c)]; });
    svg.setAttribute("aria-label", total ? tpl(dict.ac_ring_aria, { parts: parts.join(", ") }) : dict.ac_ring_none);
    svg.appendChild(svgEl("circle", { cx: 60, cy: 60, r: R, fill: "none", stroke: "var(--panel-2)", "stroke-width": 15 }));
    let offset = 0;
    AC_CODES.forEach(function (c, i) {
      const n = t.n[i];
      if (!n || !total) { return; }
      const len = n / total * C;
      svg.appendChild(svgEl("circle", { cx: 60, cy: 60, r: R, class: "ac-ring-seg ac-c-" + c, "stroke-dasharray": Math.max(0.5, len - (parts.length > 1 ? 1.5 : 0)).toFixed(2) + " " + C.toFixed(2),
        "stroke-dashoffset": (-offset).toFixed(2), transform: "rotate(-90 60 60)", "data-code": c, "data-n": n }));
      offset += len;
    });
    svg.appendChild(svgEl("text", { x: 60, y: 62, "text-anchor": "middle", class: "ac-ring-num" }, AC.read ? acNum(total) : "–"));
    svg.appendChild(svgEl("text", { x: 60, y: 77, "text-anchor": "middle", class: "ac-ring-sub" }, dict.ac_ring_total));
    holder.appendChild(svg);
    AC_CODES.forEach(function (c, i) {
      const li = make("li"); li.setAttribute("data-code", c);
      li.appendChild(acSwatch(c)); li.appendChild(make("span", "", acResultText(c, dict))); li.appendChild(make("b", "", AC.read ? String(t.n[i]) : "–"));
      legend.appendChild(li);
    });
  }
  function acBarRow(name, fraction, valueText, aria, code, delay) {
    const li = make("li");
    const b = make("button", "ac-bar"); b.type = "button"; b.setAttribute("data-repo", name); b.setAttribute("aria-label", aria); b.title = aria;
    b.appendChild(make("span", "ac-bar-name", name));
    const track = make("span", "ac-track"); track.setAttribute("aria-hidden", "true");
    const fill = make("span", "ac-fill ac-c-" + code); fill.style.setProperty("--w", Math.max(2, fraction * 100).toFixed(1) + "%"); fill.style.animationDelay = (delay * 40) + "ms";
    track.appendChild(fill); b.appendChild(track);
    b.appendChild(make("span", "ac-bar-val", valueText));
    b.addEventListener("click", function () { openPanel(name, b); });
    li.appendChild(b);
    return li;
  }
  function acRates(dict) {
    const list = document.getElementById("ac-rate");
    list.textContent = "";
    const rows = [];
    Object.keys(AC.repos).forEach(function (name) {
      const rec = AC.repos[name];
      if (!acOk(rec)) { return; }
      const ok = rec.n7[0], bad = rec.n7[1];
      if (ok + bad > 0) { rows.push({ name: name, ok: ok, all: ok + bad, p: Math.round(ok / (ok + bad) * 100) }); }
    });
    rows.sort(function (a, b) { return a.p - b.p || b.all - a.all || (a.name < b.name ? -1 : 1); });
    rows.slice(0, 6).forEach(function (r, i) {
      const text = tpl(dict.ac_rate_row, { name: r.name, p: r.p, ok: r.ok, all: r.all });
      list.appendChild(acBarRow(r.name, r.p / 100, r.p + " %", text, r.p >= 90 ? "s" : r.p >= 60 ? "p" : "f", i));
    });
    document.getElementById("ac-rate-none").hidden = rows.length > 0;
  }
  function acDurations(dict) {
    const list = document.getElementById("ac-dur");
    list.textContent = "";
    const rows = [];
    Object.keys(AC.repos).forEach(function (name) {
      const rec = AC.repos[name];
      if (acOk(rec) && rec.last && typeof rec.last[2] === "number") { rows.push({ name: name, sec: rec.last[2], code: rec.last[1] }); }
    });
    rows.sort(function (a, b) { return b.sec - a.sec || (a.name < b.name ? -1 : 1); });
    const max = rows.length ? rows[0].sec : 1;
    rows.slice(0, 6).forEach(function (r, i) {
      const d = acDuration(r.sec, dict);
      list.appendChild(acBarRow(r.name, r.sec / Math.max(1, max), d, tpl(dict.ac_dur_row, { name: r.name, d: d, result: acResultText(r.code, dict) }), r.code, i));
    });
    document.getElementById("ac-dur-none").hidden = rows.length > 0;
  }
  function acTimeline(dict) {
    const svg = document.getElementById("ac-tl");
    const none = document.getElementById("ac-tl-none");
    svg.textContent = "";
    const rows = Object.keys(AC.repos).filter(function (n) { return acOk(AC.repos[n]) && AC.repos[n].tl && AC.repos[n].tl.length; })
      .sort(function (a, b) { return AC.repos[b].tl.length - AC.repos[a].tl.length || (a < b ? -1 : 1); }).slice(0, 5);
    svg.hidden = rows.length === 0; svg.style.display = rows.length ? "" : "none"; none.hidden = rows.length > 0;
    if (!rows.length) { return; }
    const L = 190, R = 14, RH = 22, T = 4, W = 900, H = T + rows.length * RH + 26;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("aria-label", tpl(dict.ac_tl_aria, { n: rows.length }));
    const px = function (age) { return L + (1 - Math.min(1440, age) / 1440) * (W - L - R); };
    [0, 6, 12, 18, 24].forEach(function (h) { svg.appendChild(svgEl("line", { x1: px(h * 60), x2: px(h * 60), y1: T, y2: T + rows.length * RH, class: "ac-tl-grid" })); });
    svg.appendChild(svgEl("text", { x: L, y: H - 8, "text-anchor": "start", class: "ac-tl-axis" }, dict.ac_tl_axis_start));
    svg.appendChild(svgEl("text", { x: W - R, y: H - 8, "text-anchor": "end", class: "ac-tl-axis" }, dict.ac_tl_axis_end));
    rows.forEach(function (name, i) {
      const y = T + i * RH + RH / 2;
      svg.appendChild(svgEl("line", { x1: L, x2: W - R, y1: y, y2: y, class: "ac-tl-row" }));
      svg.appendChild(svgEl("text", { x: L - 8, y: y + 4, "text-anchor": "end", class: "ac-tl-name" }, name.length > 27 ? name.slice(0, 26) + "…" : name));
      AC.repos[name].tl.forEach(function (ev) {
        const kind = AC_CODES.indexOf(ev[1]);
        svg.appendChild(marker(kind < 0 ? 0 : kind, px(ev[0]), y, "ac-c-" + ev[1], tpl(dict.ac_tl_dot, { name: name, result: acResultText(ev[1], dict), ago: acAgo(ev[0], dict) })));
      });
    });
  }
  function acTrend(dict) {
    const svg = document.getElementById("ac-trend");
    const none = document.getElementById("ac-trend-none");
    svg.textContent = "";
    const days = (AC.daily || []).slice(-14);
    svg.hidden = days.length === 0; svg.style.display = days.length ? "" : "none"; none.hidden = days.length > 1;
    if (!days.length) { none.hidden = false; return; }
    svg.setAttribute("aria-label", dict.ac_trend_title);
    const W = 320, H = 170, L = 6, B = 22, T = 14;
    const max = Math.max.apply(null, days.map(function (d) { return d.runs || 0; }).concat([1]));
    const band = (W - L * 2) / Math.max(days.length, 6);
    days.forEach(function (d, i) {
      const g = svgEl("g", { class: "ac-col", tabindex: "0", role: "img", "data-date": d.date });
      const label = tpl(dict.ac_trend_col, { date: d.date, runs: d.runs || 0, ok: d.ok || 0, fail: d.fail || 0 });
      g.setAttribute("aria-label", label); g.appendChild(svgEl("title", {}, label));
      const x = L + band * i + band * 0.12, w = band * 0.76, scale = (H - B - T) / max;
      let y = H - B;
      [["s", d.ok || 0], ["f", d.fail || 0], ["k", d.other || 0]].forEach(function (p) {
        const h = p[1] * scale;
        if (h > 0) { y -= h; g.appendChild(svgEl("rect", { x: x, y: y, width: w, height: h, rx: 1.5, class: "ac-c-" + p[0], style: "animation-delay:" + (i * 40) + "ms" })); }
      });
      g.appendChild(svgEl("text", { x: x + w / 2, y: y - 3, "text-anchor": "middle", class: "ac-tl-axis" }, String(d.runs || 0)));
      if (i === 0 || i === days.length - 1) { g.appendChild(svgEl("text", { x: x + w / 2, y: H - 6, "text-anchor": i === 0 ? "start" : "end", class: "ac-tl-axis" }, d.date.slice(5))); }
      svg.appendChild(g);
    });
  }
  function acSigText(name, dict) {
    const r = DATA.repos[name] || {};
    const sig = r.sig === "verified" ? dict.ac_sig_verified : r.sig === "invalid" ? dict.ac_sig_invalid : r.sig === "unverifiable" ? dict.ac_sig_unverifiable : r.sig === "present" ? dict.ac_sig_present : r.sig === "none" ? dict.ac_sig_none : r.sig === "norelease" ? dict.ac_sig_norelease : dict.ac_sig_unverified;
    return (dict["pipe_" + (r.pipeline || "undeclared")] || "") + " · " + sig;
  }
  function acSortKey(name) {
    const rec = AC.repos[name];
    if (!acOk(rec)) { return [rec.state === "unread" ? 1 : 3, 0]; }
    if (!rec.last) { return [2, 0]; }
    return [rec.last[1] === "f" ? 0 : 2, rec.last[0]];
  }
  function acSummary(name, dict) {
    const rec = AC.repos[name];
    if (rec.state === "unread") { return dict.not_verified; }
    if (rec.state === "none") { return dict.ac_no_workflows; }
    if (!rec.last) { return dict.ac_no_runs; }
    return acResultText(rec.last[1], dict) + ", " + acAgo(rec.last[0], dict) + ", " + acDuration(rec.last[2], dict);
  }
  function acTable(dict) {
    const table = document.getElementById("ac-table");
    table.textContent = "";
    const all = Object.keys(AC.repos);
    const chips = document.getElementById("ac-eco-chips");
    chips.textContent = "";
    [["all", dict.ac_all, all.length]].concat(AC_ECOS.map(function (e) { return [e, AC_LABEL[e], all.filter(function (n) { return acEco(n) === e; }).length]; })).forEach(function (c) {
      if (c[0] !== "all" && c[2] === 0) { return; }
      const b = make("button", "chip"); b.type = "button"; b.setAttribute("data-ac-eco", c[0]); b.setAttribute("data-testid", "ac-eco-" + c[0]);
      b.setAttribute("aria-pressed", acState.eco === c[0] ? "true" : "false");
      b.appendChild(make("span", "", c[1])); b.appendChild(document.createTextNode(" ")); b.appendChild(make("b", "", String(c[2])));
      b.addEventListener("click", function () { acState.eco = c[0]; acTable(currentDict()); });
      chips.appendChild(b);
    });
    const q = acState.q.trim().toLowerCase();
    const names = all.filter(function (n) { return (acState.eco === "all" || acEco(n) === acState.eco) && (!q || n.toLowerCase().indexOf(q) >= 0); })
      .sort(function (a, b) { const ka = acSortKey(a), kb = acSortKey(b); return ka[0] - kb[0] || ka[1] - kb[1] || (a.toLowerCase() < b.toLowerCase() ? -1 : 1); });
    table.appendChild(make("caption", "sr-only", dict.ac_table_caption));
    const hr = make("tr");
    [dict.ac_col_repo, dict.ac_col_result, dict.ac_col_ago, dict.ac_col_lastok, dict.ac_col_ok24, dict.ac_col_min, dict.ac_col_issues, dict.ac_col_pipe].forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    names.forEach(function (name) {
      const rec = AC.repos[name];
      const tr = make("tr"); tr.setAttribute("data-repo", name); tr.setAttribute("data-state", rec.state);
      if (acOk(rec) && rec.last) { tr.setAttribute("data-last", rec.last[1]); }
      const th = make("th"); th.setAttribute("scope", "row");
      const link = make("button", "ac-link", name); link.type = "button"; link.addEventListener("click", function () { openPanel(name, link); });
      th.appendChild(link); tr.appendChild(th);
      const res = make("td"); const ago = make("td", "num"); const lok = make("td", "num"); const ok24 = make("td", "num"); const mn = make("td", "num");
      if (rec.state === "ok" && rec.last) {
        const span = make("span", "ac-res"); span.appendChild(acSwatch(rec.last[1])); span.appendChild(make("span", "", acResultText(rec.last[1], dict) + " · " + acDuration(rec.last[2], dict)));
        res.appendChild(span); ago.textContent = acAgo(rec.last[0], dict);
        lok.textContent = rec.lastOk === null || rec.lastOk === undefined ? dict.ac_over_week : acAgo(rec.lastOk, dict);
        const fin = rec.n[0] + rec.n[1];
        ok24.textContent = fin ? rec.n[0] + " / " + fin : "–";
        mn.textContent = String(rec.min);
      } else {
        const txt = rec.state === "ok" ? dict.ac_no_runs : rec.state === "none" ? dict.ac_no_workflows : dict.not_verified;
        res.appendChild(make("span", "ac-muted", txt));
        [ago, lok, ok24, mn].forEach(function (c) { c.textContent = "–"; });
      }
      const iss = make("td");
      if (rec.state === "unread" && rec.bf === undefined) { iss.appendChild(make("span", "ac-muted", dict.not_verified)); } else { iss.textContent = tpl(dict.ac_issues_cell, { f: rec.bf || 0, s: rec.bs || 0 }); }
      const pipe = make("td", "", acSigText(name, dict));
      [res, ago, lok, ok24, mn, iss, pipe].forEach(function (c) { tr.appendChild(c); });
      tr.setAttribute("aria-label", tpl(dict.ac_row_aria, { name: name, summary: acSummary(name, dict) }));
      body.appendChild(tr);
    });
    table.appendChild(body);
    document.getElementById("ac-none").hidden = names.length > 0;
    document.getElementById("ac-table-wrap").hidden = names.length === 0;
    const counter = document.getElementById("ac-matches");
    counter.textContent = tpl(dict.ac_matches, { shown: names.length, total: all.length });
    counter.setAttribute("data-shown", String(names.length)); counter.setAttribute("data-total", String(all.length));
  }
  function acRender(dict) {
    if (!document.getElementById("ac-root")) { return; }
    const t = acTotals();
    const banner = document.getElementById("ac-stale");
    banner.hidden = !AC.stale;
    banner.textContent = AC.stale ? tpl(dict.ac_stale, { date: String(AC.stale).slice(0, 10) }) : "";
    const note = document.getElementById("ac-unverified");
    note.hidden = !(AC.read && !AC.stale && t.unread > 0);
    note.textContent = tpl(dict.ac_unverified, { n: t.unread });
    document.getElementById("ac-not-read").hidden = AC.read;
    const asof = document.getElementById("ac-asof");
    asof.textContent = AC.asof ? tpl(dict.ac_asof, { time: String(AC.asof).slice(11, 16) }) : "";
    document.getElementById("ac-help-body").textContent = dict.ac_help_body;
    acKpis(t, dict); acRing(t, dict); acRates(dict); acDurations(dict); acTimeline(dict); acTrend(dict); acTable(dict);
  }
  (function () {
    const search = document.getElementById("ac-search");
    if (search) { search.addEventListener("input", function () { acState.q = search.value; acTable(currentDict()); }); }
  })();
"""
