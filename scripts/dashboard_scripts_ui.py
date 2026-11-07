#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_scripts_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Scripts" of the dashboard: the GitHub workflows, the actions they use and the own scripts of every repository.

Same pattern as the Code and Changelog tabs: the markup is a frame; the figures, the charts and the table are drawn in the browser from the JSON the page
already embeds (`scripts`, see dashboard_scripts.py), so the page makes no request of its own. The charts are the stacked bars of the other tabs (shadow under the
track, dark lower half and light edge on each segment, the same entrance), each one has a table with the same figures, a name for assistive technology and a
tooltip on hover and on keyboard focus. The script is placed into the shell's own scope and uses the helpers of dashboard_code_ui.py (`cdNum`, `cdPct`, `cdTable`,
`cdTipped`, `cdDepth`, `cdRelief`, `cdLegendItem`, `cdTypeLabel`); `scRender` is called by `evoApplied` whenever the language changes. Stdlib only.
"""
from __future__ import annotations

import dashboard_code_texts
from dashboard_charts import esc

EN = dashboard_code_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def _card(ident: str, title: str, hint: str | None, body: str) -> str:
    hint_html = f'<p class="muted" {_t(hint)}</p>' if hint else ""
    return (f'<section class="card" aria-labelledby="{ident}-title"><header class="card-head"><h3 class="card-title" id="{ident}-title" {_t(title)}</h3></header>'
            f'{hint_html}{body}</section>')


def _alt(ident: str) -> str:
    return f'<div class="sr-only"><table id="{ident}" data-testid="{ident}"><thead><tr><th scope="col" data-i18n="cd_col_name">{esc(EN["cd_col_name"])}</th></tr></thead></table></div>'


def _chart(ident: str, legend: bool = True) -> str:
    return (f'<div class="cd-chart" id="{ident}" data-testid="{ident}"></div>'
            + (f'<ul class="cd-legend" id="{ident}-legend" data-testid="{ident}-legend"></ul>' if legend else "") + _alt(ident + "-table"))


def panel_html() -> str:
    return (
        '<section class="ins cd" id="sc-root" aria-labelledby="sc-title" data-testid="scripts-root">'
        f'<header class="ins-head"><h2 class="card-title" id="sc-title" {_t("sc_title")}</h2>'
        f'<span class="ts-badge" data-testid="sc-badge" {_t("sc_badge")}</span></header>'
        f'<p class="muted" {_t("sc_hint")}</p>'
        '<details class="ts-help" data-testid="sc-help">'
        f'<summary {_t("sc_help_summary")}</summary><p id="sc-help-body" data-testid="sc-help-body"></p></details>'
        '<p class="stale-banner" id="sc-stale" role="status" data-testid="sc-stale" hidden></p>'
        f'<p class="no-data" id="sc-not-read" data-testid="sc-not-read" hidden {_t("sc_not_read")}</p>'
        '<div id="sc-body" data-testid="sc-body">'
        '<ul class="ac-kpis cd-kpis" id="sc-kpis" data-testid="sc-kpis"></ul>'
        + _card("sc-trig", "sc_trig_title", "sc_trig_hint", _chart("sc-trig-chart"))
        + _card("sc-pin", "sc_pin_title", "sc_pin_hint", _chart("sc-pin-chart"))
        + _card("sc-top", "sc_top_title", "sc_top_hint",
                '<div class="ev-controls"><div class="ts-field"><label class="scope-title" for="sc-top-n" data-i18n="cd_top_n">How many</label>'
                '<select id="sc-top-n" data-testid="sc-top-n"><option value="10">10</option><option value="15" selected>15</option><option value="30">30</option></select></div></div>'
                + _chart("sc-top-chart"))
        + _card("sc-lang", "sc_lang_title", "sc_lang_hint", _chart("sc-lang-chart"))
        + _card("sc-rank", "sc_rank_title", "sc_rank_hint", _chart("sc-rank-chart"))
        + _card("sc-unp", "sc_unp_title", "sc_unp_hint",
                f'<p class="no-data" id="sc-unp-none" data-testid="sc-unp-none" hidden {_t("sc_unp_none")}</p>'
                '<ul class="sc-unp" id="sc-unp-list" data-testid="sc-unp-list"></ul>')
        + '<section class="card" aria-labelledby="sc-table-title"><header class="card-head">'
        f'<h3 class="card-title" id="sc-table-title" {_t("sc_table_title")}</h3></header><p class="muted" {_t("sc_table_hint")}</p>'
        '<div class="ev-controls"><div class="ev-group" role="group" aria-labelledby="sc-eco-t">'
        f'<span class="scope-title" id="sc-eco-t" {_t("cd_filter_eco")}</span><span class="chip-row" id="sc-eco-chips" data-testid="sc-eco-chips"></span></div>'
        '<div class="ev-group" role="group" aria-labelledby="sc-type-t">'
        f'<span class="scope-title" id="sc-type-t" {_t("cd_filter_type")}</span><span class="chip-row" id="sc-type-chips" data-testid="sc-type-chips"></span></div>'
        '<div class="ts-field"><label class="scope-title" for="sc-group" data-i18n="cd_group">Group rows by</label><select id="sc-group" data-testid="sc-group"></select></div>'
        '<div class="ts-field"><label class="scope-title" for="sc-search" data-i18n="cd_search">Search a repository</label>'
        '<input type="search" id="sc-search" data-testid="sc-search" autocomplete="off" maxlength="80"></div></div>'
        '<p class="matches" id="sc-matches" aria-live="polite" data-testid="sc-matches"></p>'
        '<p class="sr-only" id="sc-live" role="status" data-testid="sc-live"></p>'
        '<div class="cd-table-wrap" id="sc-table-wrap" tabindex="0" role="region" aria-labelledby="sc-table-title" data-testid="sc-table-wrap">'
        '<table class="cd-table" id="sc-table" data-testid="sc-table"><thead><tr><th scope="col" data-i18n="cd_col_name">Repository</th></tr></thead></table></div>'
        f'<p class="no-data" id="sc-none" data-testid="sc-none" hidden {_t("cd_none")}</p></section>'
        '</div></section>'
    )


CSS = r"""
  /* ======================= Scripts: workflows, actions and own scripts ======================= */
  #sc-body { display: grid; gap: 14px; min-width: 0; }
  #sc-body[hidden] { display: none; }
  .sc-unp { list-style: none; margin: 6px 0 0; padding: 0; display: grid; gap: 3px; max-height: 46vh; overflow: auto; border: 1px solid var(--border); border-radius: 10px; padding: 6px; }
  .sc-unp li { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 4px 12px; align-items: baseline; padding: 4px 8px; border-radius: 8px; font-size: 13px; }
  .sc-unp li:hover { background: var(--panel-2); }
  .sc-unp code { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 12px; overflow-wrap: anywhere; }
  .sc-unp .sc-unp-n { color: var(--dim); font-size: 12px; font-variant-numeric: tabular-nums; }
"""

JS = r"""
  // ---------------- Scripts: the workflows, the actions they use and the own scripts of every repository (read once a day by scripts/code_stats.py) ----------------
  // Drawn from the JSON embedded in the page. Nothing read = "not verified", never a zero.
  const SC = (DATA.scripts && typeof DATA.scripts === "object" && DATA.scripts.repos) ? DATA.scripts : { read: false, repos: {}, ecos: [], types: [], owner: "", day: null, age: null };
  const SC_TRIGGERS = ["push", "pull_request", "schedule", "workflow_dispatch", "release", "workflow_run", "workflow_call", "other"];
  const SC_PINS = ["sha", "tag", "branch", "local", "docker"];
  const SC_LANGS = ["py", "sh", "ps1", "bat", "js"];
  const SC_TRIG_CLASS = ["cd-l-0", "cd-l-1", "cd-l-2", "cd-l-3", "cd-l-4", "cd-l-5", "cd-l-6", "cd-l-o"];
  const SC_PIN_CLASS = { sha: "cd-c-tests", tag: "cd-c-docs", branch: "cd-l-5", local: "cd-l-o", docker: "cd-l-7" };
  const SC_LANG_CLASS = { py: "cd-l-0", sh: "cd-l-2", ps1: "cd-l-6", bat: "cd-l-1", js: "cd-l-3" };
  const scState = { eco: "all", type: "all", q: "", group: "repo", sort: "wf", dir: -1, top: 15 };
  const SC_COLUMNS = [
    ["name", "cd_col_name", false], ["eco", "cd_col_eco", false], ["type", "cd_col_type", false], ["repos", "cd_col_repos", true], ["wf", "sc_col_wf", true], ["jobs", "sc_col_jobs", true],
    ["acts", "sc_col_acts", true], ["unp", "sc_col_unp", true], ["sched", "sc_col_sched", true], ["manual", "sc_col_manual", true], ["files", "sc_col_files", true],
    ["lines", "sc_col_lines", true], ["mix", "sc_col_mix", false]
  ];
  function scEcoLabel(key) { const e = SC.ecos.filter(function (x) { return x.key === key; })[0]; return e ? e.label : key; }
  function scNames() { return Object.keys(SC.repos).sort(); }
  function scHas(r) { return (r.state === "ok" || r.state === "lastknown") && r.scripts; }
  function scMeasured() { return scNames().filter(function (n) { return scHas(SC.repos[n]); }); }
  function scThird(key) { const o = (SC.owner || "").toLowerCase(); return !o || key.toLowerCase().indexOf(o + "/") !== 0; }
  function scFig(r) {
    const s = r.scripts;
    const f = { repos: 1, wf: s.wf.length, jobs: 0, acts: 0, unp: 0, sched: 0, manual: 0, files: 0, lines: 0, trig: {}, pin: {}, lang: {} };
    SC_TRIGGERS.forEach(function (t) { f.trig[t] = 0; }); SC_PINS.forEach(function (p) { f.pin[p] = 0; }); SC_LANGS.forEach(function (l) { f.lang[l] = 0; });
    s.wf.forEach(function (w) {
      f.jobs += w[3];
      w[2].forEach(function (t) { f.trig[t] += 1; });
      if (w[2].indexOf("schedule") >= 0) { f.sched += 1; }
      if (w[2].indexOf("workflow_dispatch") >= 0) { f.manual += 1; }
    });
    Object.keys(s.acts).forEach(function (k) {
      const n = s.acts[k][0], pin = s.acts[k][1];
      f.acts += n; f.pin[pin] += n;
      if ((pin === "tag" || pin === "branch") && scThird(k)) { f.unp += n; }
    });
    Object.keys(s.sc).forEach(function (l) { f.files += s.sc[l][0]; f.lines += s.sc[l][1]; f.lang[l] = s.sc[l][0]; });
    return f;
  }
  function scSum(list) {
    const out = { repos: 0, wf: 0, jobs: 0, acts: 0, unp: 0, sched: 0, manual: 0, files: 0, lines: 0, trig: {}, pin: {}, lang: {} };
    SC_TRIGGERS.forEach(function (t) { out.trig[t] = 0; }); SC_PINS.forEach(function (p) { out.pin[p] = 0; }); SC_LANGS.forEach(function (l) { out.lang[l] = 0; });
    list.forEach(function (f) {
      ["repos", "wf", "jobs", "acts", "unp", "sched", "manual", "files", "lines"].forEach(function (k) { out[k] += f[k]; });
      SC_TRIGGERS.forEach(function (t) { out.trig[t] += f.trig[t]; }); SC_PINS.forEach(function (p) { out.pin[p] += f.pin[p]; }); SC_LANGS.forEach(function (l) { out.lang[l] += f.lang[l]; });
    });
    return out;
  }
  function scGroupFig(field, key) { return scSum(scMeasured().filter(function (n) { return SC.repos[n][field] === key; }).map(function (n) { return scFig(SC.repos[n]); })); }
  function scRows(dict) {
    const rows = [{ head: null, name: dict.cd_all, f: scSum(scMeasured().map(function (n) { return scFig(SC.repos[n]); })), key: "all" }];
    SC.ecos.forEach(function (e, i) { const f = scGroupFig("eco", e.key); if (f.repos) { rows.push({ head: i === 0 ? dict.cd_by_eco : null, name: e.label, f: f, key: e.key }); } });
    SC.types.forEach(function (t, i) { const f = scGroupFig("type", t); if (f.repos) { rows.push({ head: i === 0 ? dict.cd_by_type : null, name: cdTypeLabel(t, dict), f: f, key: t }); } });
    return rows;
  }
  function scKpis(dict) {
    const list = document.getElementById("sc-kpis");
    list.textContent = "";
    const all = scSum(scMeasured().map(function (n) { return scFig(SC.repos[n]); }));
    const withWf = scMeasured().filter(function (n) { return SC.repos[n].scripts.wf.length > 0; }).length;
    const items = [["repos", withWf + " / " + scNames().length, dict.sc_k_repos], ["workflows", cdNum(all.wf), dict.sc_k_workflows], ["jobs", cdNum(all.jobs), dict.sc_k_jobs],
      ["uses", cdNum(all.acts), dict.sc_k_uses], ["unpinned", cdNum(all.unp) + " (" + cdNum(cdPct(all.unp, all.acts)) + " %)", dict.sc_k_unpinned],
      ["files", cdNum(all.files), dict.sc_k_files], ["lines", cdNum(all.lines), dict.sc_k_lines]];
    items.forEach(function (it) {
      const li = make("li", "ac-kpi"); li.setAttribute("data-testid", "sc-k-" + it[0]); li.setAttribute("data-value", it[1]);
      li.appendChild(make("b", "", it[1])); li.appendChild(make("span", "", it[2])); list.appendChild(li);
    });
  }
  /* One chart of stacked bars (the whole, each ecosystem, each type), drawn like the others: shadow, dark lower half, light edge, entrance. */
  function scStack(id, ariaKey, keys, labelOf, classOf, valueOf, tipKey, dict) {
    const holder = document.getElementById(id);
    holder.textContent = "";
    const rows = scRows(dict);
    const W = 900, L = 150, R = 110, ROW = 30, HEAD = 22;
    let y = 4;
    const layout = rows.map(function (r) { if (r.head) { y += HEAD; } const at = y; y += ROW; return { r: r, y: at }; });
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + (y + 4), class: "cd-svg", role: "group", "aria-label": dict[ariaKey], "data-testid": id + "-svg" });
    const track = W - L - R;
    layout.forEach(function (it, i) {
      const sum = keys.reduce(function (a, k) { return a + valueOf(it.r.f, k); }, 0);
      if (it.r.head) { svg.appendChild(svgEl("text", { x: 0, y: it.y - 8, class: "cd-head" }, it.r.head)); }
      const g = svgEl("g", { "data-row": it.r.key });
      g.appendChild(svgEl("text", { x: 0, y: it.y + 17, class: "cd-name" }, it.r.name));
      cdDepth(g, L, it.y + 3, track, ROW - 8, 4);
      g.appendChild(svgEl("rect", { x: L, y: it.y + 3, width: track, height: ROW - 8, rx: 4, class: "cd-track" }));
      let x = L;
      keys.forEach(function (k) {
        const v = valueOf(it.r.f, k), w = sum > 0 ? track * v / sum : 0;
        if (w <= 0) { return; }
        const seg = svgEl("g", { class: "cd-seg", "data-kind": k, "data-value": String(v), style: "--i:" + i });
        cdTipped(seg, tpl(dict[tipKey], { name: labelOf(k, dict), n: cdNum(v), pc: cdNum(cdPct(v, sum)), files: cdNum(v), lines: cdNum(it.r.f.lines) }));
        seg.appendChild(svgEl("rect", { x: x, y: it.y + 3, width: Math.max(1, w), height: ROW - 8, rx: 3, class: classOf(k) }));
        cdRelief(seg, x, it.y + 3, w, ROW - 8);
        if (w > 40) { seg.appendChild(svgEl("text", { x: x + w / 2, y: it.y + 18, "text-anchor": "middle", class: "cd-ink" }, cdNum(v))); }
        g.appendChild(seg);
        x += w;
      });
      g.appendChild(svgEl("text", { x: W, y: it.y + 17, "text-anchor": "end", class: "cd-val" }, cdNum(sum)));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
    const legend = document.getElementById(id + "-legend");
    legend.textContent = "";
    keys.forEach(function (k) { legend.appendChild(cdLegendItem(classOf(k), labelOf(k, dict))); });
    cdTable(document.getElementById(id + "-table"), dict[ariaKey], [dict.cd_col_name].concat(keys.map(function (k) { return labelOf(k, dict); })),
      rows.map(function (r) { return [r.name].concat(keys.map(function (k) { return cdNum(valueOf(r.f, k)); })); }));
  }
  function scTopActions() {
    const map = {};
    scMeasured().forEach(function (n) {
      const a = SC.repos[n].scripts.acts;
      Object.keys(a).forEach(function (k) {
        const name = k.split("@")[0];
        const e = map[name] || (map[name] = { name: name, n: 0, pin: { sha: 0, tag: 0, branch: 0, local: 0, docker: 0 } });
        e.n += a[k][0]; e.pin[a[k][1]] += a[k][0];
      });
    });
    return Object.keys(map).map(function (k) { return map[k]; }).sort(function (a, b) { return b.n - a.n || (a.name < b.name ? -1 : 1); });
  }
  /* Horizontal bars of one list (the most used actions, the repositories with most workflows), stacked by `keys` and scaled to the longest one. */
  function scBars(id, ariaKey, items, keys, labelOf, classOf, valueOf, tipKey, dict) {
    const holder = document.getElementById(id);
    holder.textContent = "";
    const W = 900, L = 260, R = 60, ROW = 26;
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + (items.length * ROW + 8), class: "cd-svg", role: "group", "aria-label": dict[ariaKey], "data-testid": id + "-svg" });
    const track = W - L - R;
    const max = items.reduce(function (a, it) { return Math.max(a, keys.reduce(function (s, k) { return s + valueOf(it, k); }, 0)); }, 1);
    items.forEach(function (it, i) {
      const y = 4 + i * ROW, total = keys.reduce(function (s, k) { return s + valueOf(it, k); }, 0);
      const g = svgEl("g", { "data-row": it.name });
      g.appendChild(svgEl("text", { x: 0, y: y + 15, class: "cd-text" }, it.name.length > 38 ? it.name.slice(0, 37) + "…" : it.name));
      cdDepth(g, L, y + 2, track, ROW - 7, 2);
      g.appendChild(svgEl("rect", { x: L, y: y + 2, width: track, height: ROW - 7, rx: 2, class: "cd-track" }));
      let x = L;
      keys.forEach(function (k) {
        const v = valueOf(it, k), w = track * v / max;
        if (v <= 0) { return; }
        const seg = svgEl("g", { class: "cd-seg", "data-kind": k, "data-value": String(v), style: "--i:" + i });
        cdTipped(seg, tpl(dict[tipKey], { name: it.name + " · " + labelOf(k, dict), n: cdNum(v), pc: cdNum(cdPct(v, total)), files: cdNum(v), lines: "" }));
        seg.appendChild(svgEl("rect", { x: x, y: y + 2, width: Math.max(1, w), height: ROW - 7, rx: 2, class: classOf(k) }));
        cdRelief(seg, x, y + 2, w, ROW - 7);
        g.appendChild(seg);
        x += w;
      });
      g.appendChild(svgEl("text", { x: W, y: y + 15, "text-anchor": "end", class: "cd-val" }, cdNum(total)));
      svg.appendChild(g);
    });
    holder.appendChild(svg);
    const legend = document.getElementById(id + "-legend");
    legend.textContent = "";
    keys.forEach(function (k) { legend.appendChild(cdLegendItem(classOf(k), labelOf(k, dict))); });
    cdTable(document.getElementById(id + "-table"), dict[ariaKey], [dict.cd_col_name].concat(keys.map(function (k) { return labelOf(k, dict); })),
      items.map(function (it) { return [it.name].concat(keys.map(function (k) { return cdNum(valueOf(it, k)); })); }));
  }
  function scTrigLabel(k, dict) { return dict["sc_trig_" + k]; }
  function scPinLabel(k, dict) { return dict["sc_pin_" + k]; }
  function scLangLabel(k, dict) { return dict["sc_lang_" + k]; }
  function scRenderCharts(dict) {
    scStack("sc-trig-chart", "sc_aria_trig", SC_TRIGGERS, scTrigLabel, function (k) { return SC_TRIG_CLASS[SC_TRIGGERS.indexOf(k)]; }, function (f, k) { return f.trig[k]; }, "sc_tip_trig", dict);
    scStack("sc-pin-chart", "sc_aria_pin", SC_PINS, scPinLabel, function (k) { return SC_PIN_CLASS[k]; }, function (f, k) { return f.pin[k]; }, "sc_tip_pin", dict);
    scStack("sc-lang-chart", "sc_aria_lang", SC_LANGS, scLangLabel, function (k) { return SC_LANG_CLASS[k]; }, function (f, k) { return f.lang[k]; }, "sc_tip_lang", dict);
    scBars("sc-top-chart", "sc_aria_top", scTopActions().slice(0, scState.top), SC_PINS, scPinLabel, function (k) { return SC_PIN_CLASS[k]; }, function (it, k) { return it.pin[k]; }, "sc_tip_pin", dict);
    const ranked = scMeasured().map(function (n) { const f = scFig(SC.repos[n]); f.name = n; return f; }).filter(function (f) { return f.wf > 0; })
      .sort(function (a, b) { return b.wf - a.wf || (a.name < b.name ? -1 : 1); }).slice(0, scState.top);
    scBars("sc-rank-chart", "sc_aria_rank", ranked, SC_TRIGGERS, scTrigLabel, function (k) { return SC_TRIG_CLASS[SC_TRIGGERS.indexOf(k)]; }, function (it, k) { return it.trig[k]; }, "sc_tip_trig", dict);
  }
  function scRenderUnpinned(dict) {
    const map = {};
    scMeasured().forEach(function (n) {
      const a = SC.repos[n].scripts.acts;
      Object.keys(a).forEach(function (k) {
        if ((a[k][1] !== "tag" && a[k][1] !== "branch") || !scThird(k)) { return; }
        const e = map[k] || (map[k] = { key: k, n: 0, repos: 0 });
        e.n += a[k][0]; e.repos += 1;
      });
    });
    const list = Object.keys(map).map(function (k) { return map[k]; }).sort(function (a, b) { return b.n - a.n || (a.key < b.key ? -1 : 1); }).slice(0, 40);
    const ul = document.getElementById("sc-unp-list");
    ul.textContent = "";
    document.getElementById("sc-unp-none").hidden = list.length > 0;
    ul.hidden = list.length === 0;
    list.forEach(function (e) {
      const li = make("li"); li.setAttribute("data-action", e.key);
      li.appendChild(make("code", "", e.key));
      li.appendChild(make("span", "sc-unp-n", tpl(dict.sc_unp_row, { n: cdNum(e.n), r: cdNum(e.repos) })));
      ul.appendChild(li);
    });
  }
  /* ---- the sortable, filterable table ---- */
  function scRowsTable(dict) {
    const q = scState.q.trim().toLowerCase();
    const names = scNames().filter(function (n) {
      const r = SC.repos[n];
      if (scState.eco !== "all" && r.eco !== scState.eco) { return false; }
      if (scState.type !== "all" && r.type !== scState.type) { return false; }
      return !q || n.toLowerCase().indexOf(q) >= 0;
    });
    const unread = names.filter(function (n) { return !scHas(SC.repos[n]); });
    const measured = names.filter(function (n) { return scHas(SC.repos[n]); });
    let rows;
    if (scState.group === "repo") {
      rows = measured.map(function (n) { const r = SC.repos[n]; return Object.assign({ name: n, repo: n, eco: r.eco, type: r.type, state: r.state }, scFig(r)); });
    } else {
      const field = scState.group;
      rows = Array.from(new Set(measured.map(function (n) { return SC.repos[n][field]; }))).map(function (key) {
        const f = scSum(measured.filter(function (n) { return SC.repos[n][field] === key; }).map(function (n) { return scFig(SC.repos[n]); }));
        return Object.assign({ name: field === "eco" ? scEcoLabel(key) : cdTypeLabel(key, dict), key: key, group: field, state: "ok" }, f);
      });
    }
    const dir = scState.dir, key = scState.sort;
    const textual = key === "name" || key === "eco" || key === "type";
    rows.sort(function (a, b) {
      let va = a[key], vb = b[key];
      if (key === "eco") { va = scEcoLabel(a.eco || ""); vb = scEcoLabel(b.eco || ""); }
      if (key === "type") { va = cdTypeLabel(a.type || "", dict); vb = cdTypeLabel(b.type || "", dict); }
      if (textual) { return (String(va).toLowerCase() < String(vb).toLowerCase() ? -1 : String(va).toLowerCase() > String(vb).toLowerCase() ? 1 : 0) * dir || (a.name < b.name ? -1 : 1); }
      if (key === "mix") { va = a.files; vb = b.files; }
      return (va - vb) * dir || (a.name < b.name ? -1 : 1);
    });
    return { rows: rows, unread: unread, all: names.length, total: scNames().length };
  }
  function scMix(row, dict) {
    const bar = make("span", "cd-mix cd-tipped");
    cdTipped(bar, SC_LANGS.filter(function (l) { return row.lang[l] > 0; }).map(function (l) { return scLangLabel(l, dict) + " " + cdNum(row.lang[l]); }).join(", ") || "–", false);
    SC_LANGS.forEach(function (l) { const i = make("i", SC_LANG_CLASS[l]); i.style.width = cdPct(row.lang[l], row.files) + "%"; bar.appendChild(i); });
    return bar;
  }
  function scCell(row, key, dict) {
    if (key === "eco") { return row.eco ? scEcoLabel(row.eco) : ""; }
    if (key === "type") { return row.type ? cdTypeLabel(row.type, dict) : ""; }
    if (key === "repos") { return row.group ? cdNum(row.repos) : ""; }
    return cdNum(row[key]);
  }
  function scRenderTable(dict) {
    const table = document.getElementById("sc-table");
    const view = scRowsTable(dict);
    const grouped = scState.group !== "repo";
    const cols = SC_COLUMNS.filter(function (c) { return grouped ? c[0] !== "eco" && c[0] !== "type" : c[0] !== "repos"; });
    table.textContent = "";
    table.appendChild(make("caption", "sr-only", dict.sc_table_title));
    const hr = make("tr");
    cols.forEach(function (c) {
      const th = make("th", c[2] ? "" : "cd-left"); th.setAttribute("scope", "col");
      if (c[0] === "mix") { th.textContent = dict[c[1]]; hr.appendChild(th); return; }
      const label = c[0] === "name" ? (grouped ? (scState.group === "eco" ? dict.cd_filter_eco : dict.cd_filter_type) : dict.cd_col_name) : dict[c[1]];
      const b = make("button", "cd-sort"); b.type = "button"; b.setAttribute("data-sort", c[0]); b.setAttribute("data-testid", "sc-sort-" + c[0]);
      b.appendChild(make("span", "", label));
      const active = scState.sort === c[0];
      b.appendChild(make("span", "cd-sort-mark", active ? (scState.dir < 0 ? "↓" : "↑") : "")).setAttribute("aria-hidden", "true");
      th.setAttribute("aria-sort", active ? (scState.dir < 0 ? "descending" : "ascending") : "none");
      b.addEventListener("click", function () {
        if (scState.sort === c[0]) { scState.dir = -scState.dir; } else { scState.sort = c[0]; scState.dir = c[2] ? -1 : 1; }
        scRenderTable(currentDict());
        const again = document.querySelector('#sc-table [data-sort="' + c[0] + '"]'); if (again) { again.focus(); }
        document.getElementById("sc-live").textContent = tpl(currentDict().cd_sorted, { col: label, dir: scState.dir < 0 ? currentDict().cd_desc : currentDict().cd_asc });
      });
      th.appendChild(b); hr.appendChild(th);
    });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    view.rows.forEach(function (row) {
      const tr = make("tr"); tr.setAttribute("data-row", row.repo || row.key || row.name); tr.setAttribute("data-wf", String(row.wf));
      if (row.state === "lastknown") { tr.setAttribute("data-state", "lastknown"); }
      cols.forEach(function (c) {
        const td = make("td", c[2] ? "" : "cd-left");
        if (c[0] === "name") {
          if (row.repo) { const b = make("button", "cd-name-btn", row.name); b.type = "button"; b.setAttribute("data-repo", row.repo); b.addEventListener("click", function () { openPanel(row.repo, b); }); td.appendChild(b); }
          else { td.textContent = row.name; }
          if (row.state === "lastknown") { td.appendChild(make("span", "cd-muted", " · " + dict.cd_st_lastknown)); }
        } else if (c[0] === "mix") { td.appendChild(scMix(row, dict)); }
        else { td.textContent = scCell(row, c[0], dict); }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    (grouped ? [] : view.unread).forEach(function (n) {
      const r = SC.repos[n];
      const tr = make("tr"); tr.setAttribute("data-row", n); tr.setAttribute("data-state", "unread");
      cols.forEach(function (c, i) {
        const td = make("td", c[2] ? "" : "cd-left");
        if (i === 0) { td.textContent = n; }
        else if (c[0] === "eco") { td.textContent = scEcoLabel(r.eco); }
        else if (c[0] === "type") { td.textContent = cdTypeLabel(r.type, dict); }
        else if (c[0] === "wf") { td.textContent = dict.cd_st_unread; td.className += " cd-muted"; }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
    const total = scSum(view.rows);
    const foot = make("tfoot"); const ft = make("tr"); ft.setAttribute("data-testid", "sc-total");
    cols.forEach(function (c, i) {
      if (i === 0) { const th = make("th", "", dict.cd_total); th.setAttribute("scope", "row"); ft.appendChild(th); return; }
      const td = make("td", c[2] ? "" : "cd-left");
      if (c[0] === "repos") { td.textContent = cdNum(total.repos); }
      else if (c[0] === "mix") { td.appendChild(scMix(total, dict)); }
      else if (c[0] === "eco" || c[0] === "type") { td.textContent = ""; }
      else { td.textContent = cdNum(total[c[0]]); }
      ft.appendChild(td);
    });
    foot.appendChild(ft); table.appendChild(foot);
    const shown = view.rows.length + (grouped ? 0 : view.unread.length);
    document.getElementById("sc-none").hidden = shown > 0;
    document.getElementById("sc-table-wrap").hidden = shown === 0;
    const counter = document.getElementById("sc-matches");
    counter.textContent = tpl(dict.cd_matches, { shown: view.all, total: view.total });
    counter.setAttribute("data-shown", String(view.all)); counter.setAttribute("data-total", String(view.total));
  }
  function scRenderControls(dict) {
    [["sc-eco-chips", "eco", [["all", dict.cd_filter_all, scNames().length]].concat(SC.ecos.map(function (e) { return [e.key, e.label, scNames().filter(function (n) { return SC.repos[n].eco === e.key; }).length]; }))],
     ["sc-type-chips", "type", [["all", dict.cd_filter_all, scNames().length]].concat(SC.types.map(function (t) { return [t, cdTypeLabel(t, dict), scNames().filter(function (n) { return SC.repos[n].type === t; }).length]; }))]
    ].forEach(function (def) {
      const holder = document.getElementById(def[0]);
      holder.textContent = "";
      def[2].forEach(function (c) {
        if (c[0] !== "all" && c[2] === 0) { return; }
        const b = make("button", "chip"); b.type = "button"; b.setAttribute("data-" + def[1], c[0]); b.setAttribute("data-testid", "sc-" + def[1] + "-" + c[0]);
        b.setAttribute("aria-pressed", scState[def[1]] === c[0] ? "true" : "false");
        b.appendChild(make("span", "", c[1])); b.appendChild(document.createTextNode(" ")); b.appendChild(make("b", "", String(c[2])));
        b.addEventListener("click", function () { scState[def[1]] = c[0]; scRenderControls(currentDict()); scRenderTable(currentDict()); });
        holder.appendChild(b);
      });
    });
    const sel = document.getElementById("sc-group");
    sel.textContent = "";
    [["repo", dict.cd_by_repo], ["eco", dict.cd_by_eco], ["type", dict.cd_by_type]].forEach(function (o) { const el = make("option", "", o[1]); el.value = o[0]; sel.appendChild(el); });
    sel.value = scState.group;
  }
  function scRender(dict) {
    if (!document.getElementById("sc-root")) { return; }
    const nothing = !SC.read;
    document.getElementById("sc-not-read").hidden = !nothing;
    document.getElementById("sc-body").hidden = nothing;
    const stale = document.getElementById("sc-stale");
    const old = !nothing && typeof SC.age === "number" && SC.age >= 3;
    stale.hidden = !old;
    stale.textContent = old ? tpl(dict.sc_stale, { days: SC.age, date: SC.day || "" }) : "";
    document.getElementById("sc-help-body").textContent = tpl(dict.sc_help_body, { day: SC.day || "–", n: scMeasured().length });
    if (nothing) { return; }
    scKpis(dict); scRenderCharts(dict); scRenderUnpinned(dict); scRenderControls(dict); scRenderTable(dict);
  }
  (function () {
    const sel = document.getElementById("sc-group"), search = document.getElementById("sc-search"), top = document.getElementById("sc-top-n");
    if (sel) { sel.addEventListener("change", function () { scState.group = sel.value; scState.sort = "wf"; scState.dir = -1; scRenderTable(currentDict()); }); }
    if (search) { search.addEventListener("input", function () { scState.q = search.value; scRenderTable(currentDict()); }); }
    if (top) { top.addEventListener("change", function () { scState.top = parseInt(top.value, 10) || 15; scRenderCharts(currentDict()); }); }
  })();
"""
