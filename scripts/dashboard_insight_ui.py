#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_insight_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The analysis tab of the dashboard: markup, style sheet and script.

The markup is a frame; the charts and tables are drawn in the browser from the JSON the page already embeds (see dashboard_insight.py), so the page makes no
request of its own. Every chart has a table or a list with the same figures, nothing relies on colour alone and the motion stops with prefers-reduced-motion.
"""
from __future__ import annotations

import dashboard_insight_texts
from dashboard_charts import esc

EN = dashboard_insight_texts.TEXTS["en"]
VIEWS: tuple[str, ...] = ("maturity", "activity", "deps", "miles", "dates", "debt")


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def panel_html() -> str:
    buttons = "".join(
        f'<button type="button" class="chip" data-ins-view="{view}" aria-pressed="{"true" if view == VIEWS[0] else "false"}" data-testid="ins-view-{view}"><span {_t("in_view_" + view)}</span></button>'
        for view in VIEWS)
    deps_eco = "".join(
        f'<button type="button" class="chip" data-ins-deps-eco="{key}" aria-pressed="{"true" if key == "hydra-umc" else "false"}" data-testid="ins-deps-eco-{key}"><span>{esc(label)}</span></button>'
        for key, label in (("hydra-umc", "HYDRA-UMC"), ("urtc", "URTC"), ("armor", "A.R.M.O.R."), ("eh3d", "EH3D")))
    return (
        '<section class="ins" id="ins-root" aria-labelledby="ins-title" data-testid="insight-root">'
        f'<header class="ins-head"><h2 class="card-title" id="ins-title" {_t("in_title")}</h2>'
        f'<div class="ev-group" role="group" aria-label="{esc(EN["in_views"])}" data-i18n-aria-label="in_views">{buttons}</div></header>'
        # 1. maturity funnel and areas compared
        '<div class="ins-section" data-ins-section="maturity" data-testid="ins-sec-maturity">'
        '<section class="card" aria-labelledby="fu-title"><header class="card-head">'
        f'<h3 class="card-title" id="fu-title" {_t("fu_title")}</h3></header><p class="muted" {_t("fu_hint")}</p>'
        '<p class="muted" id="fu-since" data-testid="fu-since" role="status"></p>'
        '<div class="fu-grid" id="fu-grid" data-testid="fu-grid"></div>'
        '<div class="sr-only"><table id="fu-table" data-testid="fu-table"><thead><tr><th scope="col" data-i18n="fu_col_eco">Ecosystem</th></tr></thead></table></div></section>'
        '<section class="card" aria-labelledby="ra-title"><header class="card-head">'
        f'<h3 class="card-title" id="ra-title" {_t("ra_title")}</h3></header><p class="muted" {_t("ra_hint")}</p>'
        '<div class="ra-grid" id="ra-grid" data-testid="ra-grid"></div>'
        '<div class="ins-table-wrap" tabindex="0" role="region" aria-labelledby="ra-title"><table class="ins-table" id="ra-table" data-testid="ra-table"><thead><tr><th scope="col" data-i18n="ra_col_area">Area</th></tr></thead></table></div></section>'
        '</div>'
        # 2. heat map
        '<div class="ins-section" data-ins-section="activity" data-testid="ins-sec-activity" hidden>'
        '<section class="card" aria-labelledby="he-title"><header class="card-head">'
        f'<h3 class="card-title" id="he-title" {_t("he_title")}</h3></header><p class="muted" {_t("he_hint")}</p>'
        f'<p class="muted" {_t("he_note")}</p>'
        '<div class="ins-table-wrap" tabindex="0" role="region" aria-labelledby="he-title"><table class="he-table" id="he-table" data-testid="he-table"><thead><tr><th scope="col" data-i18n="he_col_row">Ecosystem and measure</th></tr></thead></table></div>'
        f'<p class="no-data" id="he-none" data-testid="he-none" hidden {_t("he_none")}</p></section>'
        '</div>'
        # 3. dependencies
        '<div class="ins-section" data-ins-section="deps" data-testid="ins-sec-deps" hidden>'
        '<section class="card" aria-labelledby="de-title"><header class="card-head">'
        f'<h3 class="card-title" id="de-title" {_t("de_title")}</h3></header><p class="muted" {_t("de_hint")}</p>'
        '<p class="muted" id="de-counts" data-testid="de-counts" role="status"></p>'
        '<div class="de-split"><div>'
        f'<h4 class="ev-sub" {_t("de_cycles")}</h4><ul class="de-issues" id="de-cycles" data-testid="de-cycles"></ul>'
        f'<h4 class="ev-sub" {_t("de_missing")}</h4><ul class="de-issues" id="de-missing" data-testid="de-missing"></ul>'
        '</div><div>'
        f'<div class="ev-group" role="group" aria-label="{esc(EN["de_title"])}" data-i18n-aria-label="de_title">{deps_eco}</div>'
        '<div class="de-diagram-wrap" tabindex="0" role="region" id="de-diagram-wrap" aria-labelledby="de-title"><div id="de-diagram" data-testid="de-diagram"></div></div>'
        '</div></div>'
        f'<div class="ev-group"><label class="scope-title" for="de-search" {_t("de_search")}</label>'
        '<input type="search" id="de-search" data-testid="de-search" autocomplete="off"><span class="matches" id="de-matches" aria-live="polite" data-testid="de-matches"></span></div>'
        '<ul class="de-list" id="de-list" data-testid="de-list"></ul>'
        f'<p class="no-data" id="de-none" data-testid="de-none" hidden {_t("de_none")}</p></section>'
        '</div>'
        # 4. next milestones
        '<div class="ins-section" data-ins-section="miles" data-testid="ins-sec-miles" hidden>'
        '<section class="card" aria-labelledby="mi-title"><header class="card-head">'
        f'<h3 class="card-title" id="mi-title" {_t("mi_title")}</h3></header>'
        '<p class="muted" id="mi-source" data-testid="mi-source"></p>'
        f'<p class="muted" {_t("mi_titles_note")}</p>'
        '<div class="mi-grid" id="mi-grid" data-testid="mi-grid"></div></section>'
        '</div>'
        # 5. compare dates
        '<div class="ins-section" data-ins-section="dates" data-testid="ins-sec-dates" hidden>'
        '<section class="card" aria-labelledby="cp-title"><header class="card-head">'
        f'<h3 class="card-title" id="cp-title" {_t("cp_title")}</h3></header><p class="muted" {_t("cp_hint")}</p>'
        '<div class="ev-controls" id="cp-controls">'
        f'<div class="ev-group"><label class="scope-title" for="cp-from" {_t("cp_from")}</label><select id="cp-from" data-testid="cp-from"></select></div>'
        f'<div class="ev-group"><label class="scope-title" for="cp-to" {_t("cp_to")}</label><select id="cp-to" data-testid="cp-to"></select></div></div>'
        '<p class="muted" id="cp-count" data-testid="cp-count"></p>'
        '<div id="cp-result" data-testid="cp-result" aria-live="polite"></div></section>'
        '</div>'
        # 6. technical debt
        '<div class="ins-section" data-ins-section="debt" data-testid="ins-sec-debt" hidden>'
        '<section class="card" aria-labelledby="db-title"><header class="card-head">'
        f'<h3 class="card-title" id="db-title" {_t("db_title")}</h3></header><p class="muted" {_t("db_hint")}</p>'
        '<div class="db-grid" id="db-grid" data-testid="db-grid"></div></section>'
        '</div>'
        '</section>'
    )


CSS = r"""
  /* ======================= Analysis tab ======================= */
  .ins { display: grid; gap: 14px; }
  .ins-head { display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: center; justify-content: space-between; }
  .ins-head .card-title { margin: 0; font-size: 16px; }
  .ins-section { display: grid; gap: 14px; }
  .ins-section[hidden], .ins .ev-controls[hidden] { display: none; }
  .ins .link-btn { display: inline-flex; align-items: center; min-height: 24px; }
  .de-split > div { min-width: 0; }
  .ins .card-head { margin-bottom: 4px; }
  .ins-table-wrap { overflow: auto; max-width: 100%; border: 1px solid var(--border); border-radius: 10px; margin-top: 8px; }
  .ins input[type="search"], .ins select { background: var(--bg); color: var(--text); border: 1px solid var(--border-strong); border-radius: 8px; padding: 6px 8px; font: inherit; font-size: 13px; min-width: 150px; }
  .ins-table { width: auto !important; min-width: min(100%, 760px); }
  .ins-table, .he-table { border-collapse: collapse; width: 100%; font-size: 12.5px; font-variant-numeric: tabular-nums; }
  .ins-table th, .ins-table td, .he-table th, .he-table td { padding: 5px 8px; border-bottom: 1px solid var(--border); text-align: center; white-space: nowrap; }
  .ins-table th:first-child, .he-table th:first-child { text-align: left; }
  .ins-table thead th, .he-table thead th { background: var(--panel-2); position: sticky; top: 0; z-index: 1; }
  .ins-table caption, .he-table caption { text-align: left; color: var(--dim); font-size: 12px; padding: 4px 8px; caption-side: bottom; }
  .ins-key { display: inline-flex; align-items: center; justify-content: center; min-width: 18px; height: 18px; border: 1px solid currentColor; border-radius: 50%; font-size: 11px; margin-right: 6px; font-weight: 700; }

  /* Funnel */
  .fu-grid, .ra-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 8px; }
  .fu-card, .ra-card { background: var(--panel-2); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; min-width: 0; }
  .fu-card h4, .ra-card h4 { margin: 0 0 6px; font-size: 13px; display: flex; align-items: center; gap: 8px; }
  .eco-dot { width: 10px; height: 10px; border-radius: 3px; display: inline-block; background: var(--eco, var(--dim)); border: 1px solid var(--text); }
  .fu-svg, .ra-svg { width: 100%; height: auto; display: block; }
  .fu-label { fill: var(--text); font-size: 11.5px; font-family: "IBM Plex Sans", system-ui, sans-serif; }
  .fu-figure { fill: var(--text); font-size: 11.5px; font-weight: 700; font-family: "IBM Plex Mono", ui-monospace, monospace; }
  .fu-bar { stroke: var(--text); stroke-width: 1; stroke-opacity: .6; }
  .fu-m-scaffolding { fill: var(--m-scaffolding); } .fu-m-functional { fill: var(--m-functional); } .fu-m-established { fill: var(--m-established); } .fu-m-production { fill: var(--m-production); }
  .fu-notes { list-style: none; margin: 6px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 12px; }
  .fu-notes li { display: inline-flex; gap: 4px; align-items: center; }
  .fu-bar:hover, .fu-row:focus-visible .fu-bar { stroke-opacity: 1; stroke-width: 2; filter: brightness(1.12); }

  /* Radar */
  .ra-grid-line { fill: none; stroke: var(--border-strong); stroke-width: 1; }
  .ra-axis { stroke: var(--border); stroke-width: 1; }
  .ra-axis-key { fill: var(--text); font-size: 10.5px; font-weight: 700; font-family: "IBM Plex Mono", ui-monospace, monospace; text-anchor: middle; }
  .ra-ring-text { fill: var(--dim); font-size: 8.5px; font-family: "IBM Plex Mono", ui-monospace, monospace; }
  .ra-shape { stroke-width: 2.4; stroke-linejoin: round; fill-opacity: .22; stroke: var(--eco); fill: var(--eco); }
  .ra-mark { stroke: var(--panel); stroke-width: 1.2; fill: var(--eco); }
  .ra-note { font-size: 12px; color: var(--dim); margin: 4px 0 0; }

  /* Heat map */
  .he-table td { padding: 3px; min-width: 52px; }
  .he-table td.he-cell { background: color-mix(in srgb, var(--eco) calc(var(--i, 0) * 80%), transparent); }
  .he-n { display: inline-block; min-width: 28px; padding: 1px 6px; border-radius: 6px; background: var(--panel); border: 1px solid var(--border-strong); color: var(--text); font-weight: 700; }
  .he-unk .he-n { border-style: dashed; color: var(--dim); font-weight: 400; }
  .he-table th small { display: block; color: var(--dim); font-weight: 400; font-size: 11px; }
  .he-table th[scope="row"] { white-space: nowrap; }
  .he-sep th, .he-sep td { border-top: 2px solid var(--border-strong); }

  /* Dependencies */
  .de-split { display: grid; grid-template-columns: minmax(260px, 1fr) minmax(0, 2fr); gap: 16px; margin: 8px 0; align-items: start; }
  .de-issues { list-style: none; margin: 0 0 8px; padding: 0; font-size: 12.5px; display: grid; gap: 3px; }
  .de-issues li { padding-left: 16px; position: relative; }
  .de-issues li::before { content: "▲"; position: absolute; left: 0; color: var(--err); }
  .de-issues li.de-ok::before { content: "✓"; color: var(--ok); }
  .de-diagram-wrap { overflow: auto; max-height: 340px; border: 1px solid var(--border); border-radius: 10px; margin-top: 8px; background: var(--panel-2); }
  .de-svg { display: block; }
  .de-node rect { fill: var(--panel); stroke: var(--eco, var(--border-strong)); stroke-width: 1.6; }
  .de-node text { fill: var(--text); font-size: 11px; font-family: "IBM Plex Mono", ui-monospace, monospace; pointer-events: none; }
  .de-node { cursor: pointer; }
  .de-node:hover rect, .de-node:focus-visible rect { stroke-width: 3; }
  .de-node:focus-visible { outline: none; }
  .de-node:focus-visible rect { stroke: var(--focus); }
  .de-edge { fill: none; stroke: var(--dim); stroke-width: 1.4; }
  .de-edge-cycle { stroke: var(--err); stroke-width: 2; stroke-dasharray: 5 3; }
  .de-arrow { fill: var(--dim); } .de-arrow-cycle { fill: var(--err); }
  .de-list { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 6px; max-height: 42vh; overflow: auto; }
  .de-list li { border: 1px solid var(--border); border-radius: 8px; padding: 6px 10px; font-size: 12.5px; background: var(--panel-2); }
  .de-list li[hidden] { display: none; }
  .de-list dl { display: grid; grid-template-columns: max-content 1fr; gap: 2px 10px; margin: 4px 0 0; }
  .de-list dt { color: var(--dim); } .de-list dd { margin: 0; display: flex; flex-wrap: wrap; gap: 2px 10px; }
  .de-eco { color: var(--dim); font-size: 11.5px; margin-left: 6px; }
  .de-bad { color: var(--err); }

  /* Milestones */
  .mi-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 8px; }
  .mi-card { background: var(--panel-2); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; min-width: 0; }
  .mi-card h4 { margin: 0; font-size: 13px; display: flex; gap: 8px; align-items: center; }
  .mi-scroll { max-height: 52vh; overflow: auto; margin-top: 6px; }
  .mi-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .mi-list li { border-top: 1px solid var(--border); padding-top: 5px; font-size: 12.5px; }
  .mi-st { display: inline-flex; gap: 4px; align-items: center; border: 1px solid var(--text); border-radius: 6px; padding: 0 5px; font-size: 11px; margin-right: 6px; white-space: nowrap; color: var(--text); }
  .mi-st-blocked { border-width: 2px; } .mi-st-backlog { border-style: dashed; } .mi-st-ready { border-radius: 999px; } .mi-st-in_progress { border-style: double; border-width: 3px; }
  .mi-meta { display: block; color: var(--dim); font-size: 11.5px; margin-top: 2px; }

  /* Compare */
  .cp-block { margin-top: 12px; }
  .cp-block h4 { margin: 0 0 4px; font-size: 13px; }
  .cp-list { margin: 0; padding-left: 18px; font-size: 12.5px; columns: 2 320px; }
  .cp-up { color: var(--ok); } .cp-down { color: var(--err); }

  /* Debt */
  .db-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 8px; }
  .db-card { background: var(--panel-2); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; min-width: 0; }
  .db-card h4 { margin: 0 0 4px; font-size: 13px; }
  .db-count { font-size: 26px; font-weight: 700; font-variant-numeric: tabular-nums; margin: 2px 0; }
  .db-list { list-style: none; margin: 6px 0 0; padding: 0; display: grid; gap: 3px; font-size: 12.5px; max-height: 38vh; overflow: auto; }
  .db-card details { margin-top: 8px; font-size: 12.5px; }
  .db-card summary { cursor: pointer; color: var(--dim); }

  @media (max-width: 1500px) { .fu-grid, .ra-grid, .mi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .db-grid { grid-template-columns: 1fr; } }
  @media (max-width: 760px) { .fu-grid, .ra-grid, .mi-grid { grid-template-columns: 1fr; } .de-split { grid-template-columns: 1fr; } }
  @media (prefers-reduced-motion: no-preference) {
    .fu-bar { transform-box: fill-box; transform-origin: center; animation: ins-grow .7s ease-out both; }
    .fu-row:nth-child(2) .fu-bar { animation-delay: .08s; } .fu-row:nth-child(3) .fu-bar { animation-delay: .16s; } .fu-row:nth-child(4) .fu-bar { animation-delay: .24s; }
    .ra-shape { transform-box: view-box; transform-origin: 50% 50%; animation: ins-pop .8s ease-out both; }
    .he-n { animation: ins-fade .5s ease-out both; }
    @keyframes ins-grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @keyframes ins-pop { from { transform: scale(.2); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes ins-fade { from { opacity: 0; } to { opacity: 1; } }
  }
  @media print { #panel-insight { display: none !important; } }
"""

JS = r"""
  // ---------------- Analysis tab: funnel, areas compared, weekly activity, dependencies, milestones, comparing dates, debt ----------------
  // Everything is drawn from DATA.insight and DATA.history, which the page already holds; nothing is requested from the network.
  const INS = (DATA.insight && typeof DATA.insight === "object") ? DATA.insight : null;
  const INS_ECOS = ["hydra-umc", "urtc", "armor", "eh3d"];
  const INS_LABEL = { "hydra-umc": "HYDRA-UMC", urtc: "URTC", armor: "A.R.M.O.R.", eh3d: "EH3D" };
  const INS_LEVELS = ["scaffolding", "functional", "established", "production"];
  const INS_AREAS = ["software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production"];
  const insState = { view: "maturity", depsEco: "hydra-umc", query: "", from: "", to: "" };

  // the first ecosystem that has something to draw is the one shown first (and the one the button of the fixed pair reports as pressed)
  (function () {
    const D = INS && INS.deps && INS.deps.diagram;
    const first = D ? INS_ECOS.filter(function (e) { return D[e] && D[e].nodes.length; })[0] : null;
    if (first) { insState.depsEco = first; }
  })();

  function insEcoStyle(el, eco) { el.style.setProperty("--eco", "var(--c-" + eco + ")"); return el; }
  function insTable(table, caption, headers, rows) {
    table.textContent = "";
    if (caption) { table.appendChild(make("caption", caption === true ? "" : "", typeof caption === "string" ? caption : "")); }
    const hr = make("tr");
    headers.forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const head = make("thead"); head.appendChild(hr); table.appendChild(head);
    const body = make("tbody");
    rows.forEach(function (cells) {
      const tr = make("tr");
      cells.forEach(function (c, i) {
        const cell = make(i === 0 ? "th" : "td", "", typeof c === "object" && c !== null ? "" : String(c));
        if (i === 0) { cell.setAttribute("scope", "row"); }
        if (typeof c === "object" && c !== null) { cell.appendChild(c); }
        tr.appendChild(cell);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
  }
  function insRepoButton(name, dict, label) {
    if (!DATA.repos[name]) { return make("span", "de-bad", name); }
    const b = make("button", "link-btn", label || name); b.type = "button";
    b.setAttribute("aria-label", tpl(dict.de_open, { name: name }));
    b.addEventListener("click", function () { openPanel(name, b); });
    return b;
  }

  // ---- 1. Funnel ----
  function insFunnel(dict) {
    const grid = document.getElementById("fu-grid");
    const since = document.getElementById("fu-since");
    grid.textContent = ""; since.textContent = "";
    const F = INS && INS.funnel;
    if (!F || !F.eco) { since.textContent = dict.not_verified; return; }
    if (!F.since) { since.textContent = dict.fu_nohist; }
    else {
      since.textContent = tpl(dict.fu_since, { date: F.since.date, days: F.since.days === null ? "?" : F.since.days }) + (F.since.days !== null && F.since.days < 28 ? " " + tpl(dict.fu_short, { days: F.since.days }) : "");
    }
    const rows = [];
    INS_ECOS.forEach(function (eco) {
      const e = F.eco[eco]; if (!e) { return; }
      const known = e.counts.reduce(function (a, b) { return a + b; }, 0);
      const card = insEcoStyle(make("div", "fu-card"), eco); card.setAttribute("data-eco", eco);
      const h = make("h4"); h.appendChild(make("span", "eco-dot")).setAttribute("aria-hidden", "true"); h.appendChild(make("span", "", INS_LABEL[eco])); card.appendChild(h);
      const cum = [0, 0, 0, 0];
      for (let i = 3, run = 0; i >= 0; i--) { run += e.counts[i]; cum[i] = run; }
      const svg = svgEl("svg", { viewBox: "0 0 360 150", class: "fu-svg", role: "img" });
      svg.setAttribute("aria-label", tpl(dict.fu_aria, { eco: INS_LABEL[eco], a: e.counts[0], b: e.counts[1], c: e.counts[2], d: e.counts[3] }));
      INS_LEVELS.forEach(function (level, i) {
        const y = 4 + i * 36;
        const g = svgEl("g", { class: "fu-row", "data-level": level });
        g.appendChild(svgEl("text", { x: 0, y: y + 18, class: "fu-label" }, dict["maturity_" + level]));
        const w = known ? Math.max(cum[i] ? 4 : 0, Math.round(150 * cum[i] / known)) : 0;
        const bar = svgEl("rect", { x: 118 + (150 - w) / 2, y: y, width: w, height: 28, rx: 4, class: "fu-bar fu-m-" + level, "data-n": e.counts[i], "data-atleast": cum[i] });
        bar.appendChild(svgEl("title", {}, tpl(dict.fu_exact, { n: e.counts[i] }) + ", " + tpl(dict.fu_atleast, { n: cum[i] })));
        g.appendChild(bar);
        g.appendChild(svgEl("text", { x: 276, y: y + 18, class: "fu-figure" }, e.counts[i] + " · ≥" + cum[i]));
        svg.appendChild(g);
      });
      card.appendChild(svg);
      const notes = make("ul", "fu-notes");
      if (F.since) {
        notes.appendChild(make("li", "", "▲ " + tpl(dict.fu_up, { n: e.up })));
        notes.appendChild(make("li", "", "▼ " + tpl(dict.fu_down, { n: e.down })));
      }
      if (e.unknown) { notes.appendChild(make("li", "", tpl(dict.fu_unknown, { n: e.unknown }))); }
      card.appendChild(notes);
      grid.appendChild(card);
      rows.push([INS_LABEL[eco]].concat(INS_LEVELS.map(function (_l, i) { return tpl(dict.fu_exact, { n: e.counts[i] }) + ", " + tpl(dict.fu_atleast, { n: cum[i] }); }), [F.since ? e.up : dict.fu_nohist, F.since ? e.down : dict.fu_nohist]));
    });
    insTable(document.getElementById("fu-table"), dict.fu_table, [dict.fu_col_eco].concat(INS_LEVELS.map(function (l) { return dict["maturity_" + l]; }), [dict.fu_col_up, dict.fu_col_down]), rows);
  }

  // ---- 1b. Radar ----
  function insMarker(kind, x, y, cls, title) {
    let el;
    if (kind === 0) { el = svgEl("circle", { cx: x, cy: y, r: 3.6 }); }
    else if (kind === 1) { el = svgEl("rect", { x: x - 3.4, y: y - 3.4, width: 6.8, height: 6.8 }); }
    else if (kind === 2) { el = svgEl("polygon", { points: (x - 4.2) + "," + (y + 3.6) + " " + (x + 4.2) + "," + (y + 3.6) + " " + x + "," + (y - 4.2) }); }
    else { el = svgEl("polygon", { points: x + "," + (y - 4.6) + " " + (x + 4.4) + "," + y + " " + x + "," + (y + 4.6) + " " + (x - 4.4) + "," + y }); }
    el.setAttribute("class", cls); el.appendChild(svgEl("title", {}, title));
    return el;
  }
  function insRadar(dict) {
    const grid = document.getElementById("ra-grid");
    grid.textContent = "";
    const R = INS && INS.radar;
    if (!R) { grid.appendChild(make("p", "no-data", dict.not_verified)); return; }
    const cx = 130, cy = 122, rad = 84;
    const point = function (i, v) { const a = -Math.PI / 2 + i * 2 * Math.PI / 8; return [cx + Math.cos(a) * rad * v / 100, cy + Math.sin(a) * rad * v / 100]; };
    const DASH = ["", "7 3", "2 3", "10 3 2 3"];
    INS_ECOS.forEach(function (eco, kind) {
      const values = R[eco] || {};
      const card = insEcoStyle(make("div", "ra-card"), eco); card.setAttribute("data-eco", eco);
      const h = make("h4"); h.appendChild(make("span", "eco-dot")).setAttribute("aria-hidden", "true"); h.appendChild(make("span", "", INS_LABEL[eco])); card.appendChild(h);
      const spoken = INS_AREAS.map(function (a) { return dict["area_" + a] + " " + (typeof values[a] === "number" ? values[a] + "%" : dict.not_verified); }).join(", ");
      const svg = svgEl("svg", { viewBox: "0 0 260 244", class: "ra-svg", role: "img" });
      svg.setAttribute("aria-label", tpl(dict.ra_aria, { eco: INS_LABEL[eco], list: spoken }));
      [25, 50, 75, 100].forEach(function (ring) {
        const pts = INS_AREAS.map(function (_a, i) { return point(i, ring).map(function (n) { return n.toFixed(1); }).join(","); }).join(" ");
        svg.appendChild(svgEl("polygon", { points: pts, class: "ra-grid-line" }));
      });
      [50, 100].forEach(function (ring) { svg.appendChild(svgEl("text", { x: cx + 3, y: cy - rad * ring / 100 - 2, class: "ra-ring-text" }, ring + "%")); });
      INS_AREAS.forEach(function (_a, i) {
        const end = point(i, 100); const label = point(i, 100 + 15);
        svg.appendChild(svgEl("line", { x1: cx, y1: cy, x2: end[0].toFixed(1), y2: end[1].toFixed(1), class: "ra-axis" }));
        svg.appendChild(svgEl("text", { x: label[0].toFixed(1), y: (label[1] + 4).toFixed(1), class: "ra-axis-key" }, String(i + 1)));
      });
      const known = INS_AREAS.every(function (a) { return typeof values[a] === "number"; });
      const style = "--eco:var(--c-" + eco + ")";
      if (known) {
        const pts = INS_AREAS.map(function (a, i) { return point(i, values[a]).map(function (n) { return n.toFixed(1); }).join(","); }).join(" ");
        svg.appendChild(svgEl("polygon", { points: pts, class: "ra-shape", style: style + (DASH[kind] ? ";stroke-dasharray:" + DASH[kind] : "") }));
      }
      INS_AREAS.forEach(function (a, i) {
        if (typeof values[a] !== "number") { return; }
        const p = point(i, values[a]);
        const m = insMarker(kind, p[0], p[1], "ra-mark", INS_LABEL[eco] + " · " + dict["area_" + a] + " · " + values[a] + "%");
        m.setAttribute("style", style); svg.appendChild(m);
      });
      card.appendChild(svg);
      if (!known) { card.appendChild(make("p", "ra-note", dict.ra_missing)); }
      grid.appendChild(card);
    });
    const rows = INS_AREAS.map(function (a, i) {
      const key = make("span"); key.appendChild(make("span", "ins-key", String(i + 1))); key.appendChild(document.createTextNode(dict["area_" + a]));
      return [key].concat(INS_ECOS.map(function (eco) { const v = (R[eco] || {})[a]; return typeof v === "number" ? v + "%" : dict.not_verified; }));
    });
    insTable(document.getElementById("ra-table"), dict.ra_table, [dict.ra_col_area].concat(INS_ECOS.map(function (e) { return INS_LABEL[e]; })), rows);
  }

  // ---- 2. Heat map ----
  function insHeat(dict) {
    const table = document.getElementById("he-table");
    const none = document.getElementById("he-none");
    table.textContent = "";
    const H = INS && INS.heat;
    const anyKnown = H && INS_ECOS.some(function (eco) { const e = (H.eco || {})[eco]; return e && (e.commits.some(function (v) { return v !== null; }) || e.releases.some(function (v) { return v !== null; })); });
    none.hidden = !!anyKnown; table.hidden = !anyKnown;
    if (!anyKnown) { return; }
    const max = { commits: 1, releases: 1 };
    INS_ECOS.forEach(function (eco) { const e = H.eco[eco]; if (!e) { return; } ["commits", "releases"].forEach(function (m) { e[m].forEach(function (v) { if (v !== null && v > max[m]) { max[m] = v; } }); }); });
    table.appendChild(make("caption", "sr-only", dict.he_table));
    const hr = make("tr"); hr.appendChild(make("th", "", dict.he_col_row)).setAttribute("scope", "col");
    H.weeks.forEach(function (w) {
      const th = make("th"); th.setAttribute("scope", "col");
      th.appendChild(make("span", "", w.slice(5)));
      th.appendChild(make("span", "sr-only", tpl(dict.he_week, { date: w })));
      th.title = tpl(dict.he_week, { date: w });
      hr.appendChild(th);
    });
    const head = make("thead"); head.appendChild(hr); table.appendChild(head);
    const body = make("tbody");
    INS_ECOS.forEach(function (eco) {
      const e = H.eco[eco]; if (!e) { return; }
      ["commits", "releases"].forEach(function (metric, mi) {
        const tr = make("tr", mi === 0 ? "he-sep" : ""); tr.setAttribute("data-eco", eco); tr.setAttribute("data-metric", metric);
        const th = make("th"); th.setAttribute("scope", "row");
        th.appendChild(make("span", "", INS_LABEL[eco] + " · " + dict["he_" + metric]));
        const read = metric === "commits" ? e.commitRepos : e.releaseRepos;
        th.appendChild(make("small", "", tpl(dict.he_cover, { k: read, m: e.repos })));
        tr.appendChild(th);
        e[metric].forEach(function (v, i) {
          const td = insEcoStyle(make("td", "he-cell" + (v === null ? " he-unk" : "")), eco);
          const text = v === null ? dict.not_verified : String(v);
          td.setAttribute("data-value", v === null ? "" : String(v));
          td.title = tpl(dict.he_cell, { eco: INS_LABEL[eco], metric: dict["he_" + metric], date: H.weeks[i], n: text });
          if (v !== null) { td.style.setProperty("--i", String(Math.min(1, v / max[metric]).toFixed(2))); }
          td.appendChild(make("span", "he-n", v === null ? "?" : String(v)));
          if (v === null) { td.appendChild(make("span", "sr-only", dict.not_verified)); }
          tr.appendChild(td);
        });
        body.appendChild(tr);
      });
    });
    table.appendChild(body);
  }

  // ---- 3. Dependencies ----
  function insDeps(dict) {
    const D = INS && INS.deps;
    const counts = document.getElementById("de-counts");
    const none = document.getElementById("de-none");
    const list = document.getElementById("de-list");
    const cycles = document.getElementById("de-cycles");
    const missing = document.getElementById("de-missing");
    list.textContent = ""; cycles.textContent = ""; missing.textContent = "";
    if (!D) { counts.textContent = dict.not_verified; none.hidden = true; document.getElementById("de-diagram").textContent = ""; return; }
    none.hidden = D.declaring > 0 || Object.keys(D.repos).length > 0;
    counts.textContent = D.declaring > 0 ? tpl(dict.de_counts, { repos: D.declaring, edges: D.edges }) : dict.de_none;
    if (!D.cycles.length) { cycles.appendChild(make("li", "de-ok", dict.de_cycles_none)); }
    D.cycles.forEach(function (part) { cycles.appendChild(make("li", "", tpl(dict.de_cycle_item, { path: part.concat([part[0]]).join(" → ") }))); });
    if (!D.missing.length) { missing.appendChild(make("li", "de-ok", dict.de_missing_none)); }
    D.missing.forEach(function (m) { missing.appendChild(make("li", "", tpl(dict.de_missing_item, { name: m[0], dep: m[1] }))); });
    const names = Object.keys(D.repos);
    const needle = insState.query.trim().toLowerCase();
    let shown = 0;
    names.forEach(function (name) {
      const r = D.repos[name];
      const li = make("li"); li.setAttribute("data-repo", name);
      const match = !needle || name.toLowerCase().indexOf(needle) >= 0;
      li.hidden = !match; if (match) { shown += 1; }
      const head = make("div"); head.appendChild(insRepoButton(name, dict));
      const repo = DATA.repos[name];
      if (repo && repo.ecoLabel) { head.appendChild(make("span", "de-eco", repo.ecoLabel)); }
      if (D.cycles.some(function (p) { return p.indexOf(name) >= 0; })) { head.appendChild(make("span", "de-eco de-bad", "▲ " + dict.de_in_cycle)); }
      li.appendChild(head);
      const dl = make("dl");
      function row(label, items) {
        dl.appendChild(make("dt", "", label));
        const dd = make("dd");
        if (!items.length) { dd.appendChild(make("span", "muted", dict.de_none_value)); }
        items.forEach(function (n) {
          dd.appendChild(insRepoButton(n, dict));
          const other = DATA.repos[n] && repo && DATA.repos[n].eco !== repo.eco;
          if (other) { dd.appendChild(make("span", "muted", "(" + dict.de_other_eco + ")")); }
        });
        dl.appendChild(dd);
      }
      row(dict.de_uses, r.uses);
      row(dict.de_used_by, r.usedBy);
      if (r.missing.length) { row(dict.de_unlisted, r.missing); }
      if (r.parent) { row(dict.de_parent, [r.parent]); }
      if (r.children.length) { row(dict.de_children, r.children); }
      li.appendChild(dl);
      list.appendChild(li);
    });
    document.getElementById("de-matches").textContent = names.length ? tpl(dict.de_matches, { shown: shown, total: names.length }) : "";
    document.querySelectorAll("[data-ins-deps-eco]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-ins-deps-eco") === insState.depsEco ? "true" : "false"); });
    insDiagram(dict);
  }
  function insDiagram(dict) {
    const host = document.getElementById("de-diagram");
    host.textContent = "";
    const d = INS.deps.diagram && INS.deps.diagram[insState.depsEco];
    if (!d || !d.nodes.length) { host.appendChild(make("p", "no-data", dict.de_diagram_none)); return; }
    const W = 214, Hn = 26, GX = 86, GY = 12, PAD = 54;
    const layers = d.nodes.reduce(function (m, n) { return Math.max(m, n[1]); }, 0) + 1;
    const rowsMax = d.nodes.reduce(function (m, n) { return Math.max(m, n[2]); }, 0) + 1;
    const width = PAD * 2 + layers * W + (layers - 1) * GX, height = PAD * 2 + rowsMax * Hn + (rowsMax - 1) * GY;
    const svg = svgEl("svg", { viewBox: "0 0 " + width + " " + height, width: width, height: height, class: "de-svg", role: "group" });
    svg.setAttribute("aria-label", tpl(dict.de_diagram, { eco: INS_LABEL[insState.depsEco] }));
    const defs = svgEl("defs");
    [["de-arrow", "de-arrow"], ["de-arrow-c", "de-arrow-cycle"]].forEach(function (m) {
      const marker = svgEl("marker", { id: m[0], viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" });
      marker.appendChild(svgEl("path", { d: "M0,0 L10,5 L0,10 z", class: m[1] })); defs.appendChild(marker);
    });
    svg.appendChild(defs);
    const pos = {};
    d.nodes.forEach(function (n) { pos[n[0]] = { x: PAD + n[1] * (W + GX), y: PAD + n[2] * (Hn + GY) }; });
    d.edges.forEach(function (e) {
      const a = pos[e[0]], b = pos[e[1]]; if (!a || !b) { return; }
      const same = a.x === b.x;
      const x1 = a.x, y1 = a.y + Hn / 2, x2 = same ? b.x : b.x + W, y2 = b.y + Hn / 2;
      const mid = (x1 + x2) / 2;
      const curve = same ? "M" + x1 + "," + y1 + " C" + (x1 - 44) + "," + y1 + " " + (x1 - 44) + "," + y2 + " " + x2 + "," + y2
        : "M" + x1 + "," + y1 + " C" + mid + "," + y1 + " " + mid + "," + y2 + " " + x2 + "," + y2;
      const path = svgEl("path", { d: curve, class: "de-edge" + (e[2] ? " de-edge-cycle" : ""), "marker-end": "url(#" + (e[2] ? "de-arrow-c" : "de-arrow") + ")", "aria-hidden": "true" });
      path.appendChild(svgEl("title", {}, tpl(dict.de_edge_aria, { a: e[0], b: e[1] })));
      svg.appendChild(path);
    });
    d.nodes.forEach(function (n) {
      const r = INS.deps.repos[n[0]] || { uses: [], usedBy: [] };
      const g = svgEl("g", { class: "de-node", tabindex: 0, role: "button", "data-repo": n[0], style: "--eco:var(--c-" + insState.depsEco + ")" });
      g.setAttribute("aria-label", tpl(dict.de_node_aria, { name: n[0], u: r.uses.join(", ") || dict.de_none_value, b: r.usedBy.join(", ") || dict.de_none_value }));
      g.appendChild(svgEl("rect", { x: pos[n[0]].x, y: pos[n[0]].y, width: W, height: Hn, rx: 6 }));
      g.appendChild(svgEl("text", { x: pos[n[0]].x + 8, y: pos[n[0]].y + 17 }, n[0]));
      const open = function () { openPanel(n[0], g); };
      g.addEventListener("click", open);
      g.addEventListener("keydown", function (event) { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); open(); } });
      svg.appendChild(g);
    });
    host.appendChild(svg);
  }

  // ---- 4. Milestones ----
  function insMiles(dict) {
    const grid = document.getElementById("mi-grid");
    const source = document.getElementById("mi-source");
    grid.textContent = "";
    const M = INS && INS.miles;
    source.textContent = !M || M.source === "none" ? dict.mi_src_none : M.source === "projects" ? dict.mi_src_projects : dict.mi_src_plans;
    source.setAttribute("data-source", M ? M.source : "none");
    const GLYPH = { in_progress: "▶", ready: "○", backlog: "·", blocked: "■", other: "?" };
    INS_ECOS.forEach(function (eco) {
      const e = M && M.eco ? M.eco[eco] : null;
      const card = insEcoStyle(make("div", "mi-card"), eco); card.setAttribute("data-eco", eco);
      const h = make("h4"); h.appendChild(make("span", "eco-dot")).setAttribute("aria-hidden", "true"); h.appendChild(make("span", "", INS_LABEL[eco])); card.appendChild(h);
      if (!e || !e.total) { card.appendChild(make("p", "no-data", dict.mi_nodata_eco)); grid.appendChild(card); return; }
      card.appendChild(make("p", "muted", tpl(dict.mi_counts, { open: e.open.length, done: e.done })));
      if (!e.open.length) { card.appendChild(make("p", "no-data", dict.mi_none_eco)); grid.appendChild(card); return; }
      const scroll = make("div", "mi-scroll"); scroll.tabIndex = 0; scroll.setAttribute("role", "region"); scroll.setAttribute("aria-label", INS_LABEL[eco] + " · " + dict.mi_title);
      const ul = make("ul", "mi-list");
      e.open.forEach(function (item) {
        const key = (item.status || "").toLowerCase().replace(/\s+/g, "_");
        const known = ["in_progress", "ready", "backlog", "blocked"].indexOf(key) >= 0 ? key : "other";
        const li = make("li");
        const st = make("span", "mi-st mi-st-" + known);
        st.appendChild(make("span", "", GLYPH[known])).setAttribute("aria-hidden", "true");
        st.appendChild(make("span", "", known === "other" && item.status ? item.status : dict["mi_st_" + known]));
        li.appendChild(st); li.appendChild(make("span", "", item.title));
        const meta = [];
        if (item.priority) { meta.push(dict["mi_pr_" + item.priority.toLowerCase()] || item.priority); }
        if (item.repository) { meta.push(item.repository); }
        if (item.hardware && item.hardware !== "None") { meta.push(item.hardware); }
        if (meta.length) { li.appendChild(make("span", "mi-meta", meta.join(" · "))); }
        if (item.blocked && item.blocked !== "None") { li.appendChild(make("span", "mi-meta", tpl(dict.mi_blocked_by, { text: item.blocked }))); }
        ul.appendChild(li);
      });
      scroll.appendChild(ul); card.appendChild(scroll); grid.appendChild(card);
    });
  }

  // ---- 5. Compare two dates ----
  function insHistory() { return (Array.isArray(DATA.history) ? DATA.history : []).slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; }); }
  function insFillDates(dict) {
    const hist = insHistory();
    const from = document.getElementById("cp-from"), to = document.getElementById("cp-to");
    [from, to].forEach(function (sel) { const keep = sel.value; sel.textContent = ""; hist.forEach(function (e) { const o = make("option", "", e.date); o.value = e.date; sel.appendChild(o); }); sel.value = keep; });
    if (hist.length) {
      if (!insState.from || !hist.some(function (e) { return e.date === insState.from; })) { insState.from = hist[0].date; }
      if (!insState.to || !hist.some(function (e) { return e.date === insState.to; })) { insState.to = hist[hist.length - 1].date; }
      from.value = insState.from; to.value = insState.to;
    }
    document.getElementById("cp-controls").hidden = hist.length < 2;
  }
  function insCompare(dict) {
    const hist = insHistory();
    insFillDates(dict);
    const out = document.getElementById("cp-result");
    const count = document.getElementById("cp-count");
    out.textContent = "";
    if (hist.length < 2) { count.textContent = ""; out.appendChild(make("p", "no-data", dict.cp_none)); return; }
    count.textContent = tpl(dict.cp_snapshots, { n: hist.length, first: hist[0].date, last: hist[hist.length - 1].date });
    if (insState.from === insState.to) { out.appendChild(make("p", "no-data", dict.cp_same)); return; }
    let a = hist.filter(function (e) { return e.date === insState.from; })[0], b = hist.filter(function (e) { return e.date === insState.to; })[0];
    if (!a || !b) { return; }
    const rows = [];
    INS_ECOS.forEach(function (eco) {
      const measures = [["overall", dict.evo_metric_overall, (a.progress || {})[eco], (b.progress || {})[eco]]].concat(INS_AREAS.map(function (area) {
        return [area, dict["area_" + area], ((a.areas || {})[eco] || {})[area], ((b.areas || {})[eco] || {})[area]];
      }));
      measures.forEach(function (m) {
        const x = typeof m[2] === "number" ? m[2] : null, y = typeof m[3] === "number" ? m[3] : null;
        if (x === y) { return; }
        const delta = x !== null && y !== null ? (y - x > 0 ? "+" : "") + (y - x) : "—";
        rows.push([INS_LABEL[eco] + " · " + m[1], x === null ? dict.cp_unknown : x + "%", y === null ? dict.cp_unknown : y + "%", delta]);
      });
    });
    const block = make("div", "cp-block"); block.appendChild(make("h4", "", dict.cp_progress));
    if (rows.length) {
      const wrap = make("div", "ins-table-wrap"); wrap.tabIndex = 0; wrap.setAttribute("role", "region"); wrap.setAttribute("aria-label", dict.cp_progress);
      const table = make("table", "ins-table"); table.id = "cp-table"; table.setAttribute("data-testid", "cp-table");
      insTable(table, "", [dict.cp_col_what, insState.from, insState.to, dict.cp_col_delta], rows);
      wrap.appendChild(table); block.appendChild(wrap);
    } else { block.appendChild(make("p", "no-data", dict.cp_nochange)); }
    out.appendChild(block);
    const ra = a.repos, rb = b.repos;
    if (!ra || !rb || typeof ra !== "object" || typeof rb !== "object") { out.appendChild(make("p", "no-data", dict.cp_no_repos)); return; }
    const moved = [], versions = [];
    Object.keys(rb).sort(function (p, q) { return p.toLowerCase() < q.toLowerCase() ? -1 : 1; }).forEach(function (name) {
      const before = ra[name], after = rb[name];
      if (before && after && before[0] !== after[0]) { moved.push([name, before[0], after[0]]); }
      if (after && after[1] && (!before || before[1] !== after[1])) { versions.push([name, before ? before[1] : null, after[1]]); }
    });
    function listBlock(title, items, build) {
      const sec = make("div", "cp-block"); sec.appendChild(make("h4", "", title));
      if (!items.length) { sec.appendChild(make("p", "no-data", dict.cp_none_items)); }
      else {
        const ul = make("ul", "cp-list");
        items.forEach(function (it) { const li = make("li"); build(li, it); ul.appendChild(li); });
        sec.appendChild(ul);
      }
      out.appendChild(sec);
    }
    listBlock(dict.cp_maturity, moved, function (li, it) {
      const up = it[2] > it[1];
      li.appendChild(insRepoButton(it[0], dict));
      li.appendChild(make("span", up ? "cp-up" : "cp-down", " " + (up ? "▲ " : "▼ ") + dict["maturity_" + INS_LEVELS[it[1]]] + " → " + dict["maturity_" + INS_LEVELS[it[2]]]));
    });
    listBlock(dict.cp_versions, versions, function (li, it) {
      li.appendChild(insRepoButton(it[0], dict));
      li.appendChild(make("span", "", " " + (it[1] === null ? tpl(dict.cp_new_repo, { to: it[2] }) : (it[1] || dict.cp_unknown) + " → " + it[2])));
    });
  }

  // ---- 6. Technical debt ----
  function insDebt(dict) {
    const grid = document.getElementById("db-grid");
    grid.textContent = "";
    const B = INS && INS.debt;
    if (!B) { grid.appendChild(make("p", "no-data", dict.not_verified)); return; }
    const groups = [
      ["scaffolding", tpl(dict.db_scaffolding, { months: B.months }), dict.db_scaffolding_rule, function (it) { return tpl(dict.db_scaffolding_item, { n: it[1] }); }, true],
      ["integration", dict.db_integration, dict.db_integration_rule, function () { return dict.db_integration_item; }, true],
      ["hardware", dict.db_hardware, dict.db_hardware_rule, function (it) { return tpl(dict.db_hardware_item, { evidence: dict["evidence_" + it[1]] || it[1] }); }, false]
    ];
    groups.forEach(function (g) {
      const data = B[g[0]];
      const card = make("div", "db-card"); card.setAttribute("data-debt", g[0]);
      card.appendChild(make("h4", "", g[1]));
      card.appendChild(make("p", "muted", g[2]));
      card.appendChild(make("p", "db-count", String(data.items.length))).setAttribute("data-testid", "db-count-" + g[0]);
      card.appendChild(make("p", "muted", tpl(dict.db_count, { n: data.items.length })));
      if (g[4] && !INS.facts) { card.appendChild(make("p", "no-data", dict.db_nodata)); }
      else if (!data.items.length) { card.appendChild(make("p", "no-data", dict.db_none)); }
      const ul = make("ul", "db-list");
      data.items.forEach(function (it) {
        const name = typeof it === "string" ? it : it[0];
        const li = make("li"); li.appendChild(insRepoButton(name, dict));
        const eco = DATA.repos[name] && DATA.repos[name].ecoLabel;
        li.appendChild(make("span", "muted", " · " + (eco ? eco + " · " : "") + g[3](it)));
        ul.appendChild(li);
      });
      if (data.items.length) { card.appendChild(ul); }
      if (data.unverified.length && !(g[4] && !INS.facts)) {
        const d = make("details"); d.appendChild(make("summary", "", tpl(dict.db_unverified, { n: data.unverified.length })));
        const u = make("ul", "db-list");
        data.unverified.forEach(function (name) { const li = make("li"); li.appendChild(insRepoButton(name, dict)); u.appendChild(li); });
        d.appendChild(u); card.appendChild(d);
      }
      grid.appendChild(card);
    });
  }

  function insightApplied(dict) {
    insFunnel(dict); insRadar(dict); insHeat(dict); insDeps(dict); insMiles(dict); insCompare(dict); insDebt(dict);
  }
  function insShow(view) {
    insState.view = view;
    document.querySelectorAll("[data-ins-view]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-ins-view") === view ? "true" : "false"); });
    document.querySelectorAll("[data-ins-section]").forEach(function (s) { s.hidden = s.getAttribute("data-ins-section") !== view; });
  }
  document.querySelectorAll("[data-ins-view]").forEach(function (b) { b.addEventListener("click", function () { insShow(b.getAttribute("data-ins-view")); }); });
  document.querySelectorAll("[data-ins-deps-eco]").forEach(function (b) { b.addEventListener("click", function () { insState.depsEco = b.getAttribute("data-ins-deps-eco"); insDeps(currentDict()); }); });
  const insSearch = document.getElementById("de-search");
  if (insSearch) { insSearch.addEventListener("input", function () { insState.query = insSearch.value; insDeps(currentDict()); }); }
  ["cp-from", "cp-to"].forEach(function (id) {
    const el = document.getElementById(id);
    if (el) { el.addEventListener("change", function () { insState[id === "cp-from" ? "from" : "to"] = el.value; insCompare(currentDict()); }); }
  });
"""
