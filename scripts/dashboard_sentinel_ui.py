#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_sentinel_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Sentinel" of the dashboard: a short report made by rules, the figures that matter (red workflows, releases ready, invalid signatures, hygiene gaps,
computing), one card per question and the daily trend.

The markup is a frame; everything is drawn in the browser from the JSON the page already embeds (`sentinel`, see dashboard_sentinel.py), so the page makes no
request of its own. Nothing relies on colour alone (every level has a glyph and a word), every chart has its figures as text and the motion stops with
prefers-reduced-motion. The script is placed into the shell's own scope (it uses `DATA`, `make`, `tpl`, `svgEl`, `currentDict`, `openPanel` and the helpers of the
builds tab); `snRender` is called by `evoApplied` whenever the language changes. Stdlib only.
"""
from __future__ import annotations

import dashboard_sentinel_texts
from dashboard_charts import esc

EN = dashboard_sentinel_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def _card(ident: str, title_key: str, extra: str = "", body: str = "") -> str:
    return (f'<section class="card sn-card {extra}" aria-labelledby="sn-{ident}-title" data-testid="sn-card-{ident}"><header class="card-head">'
            f'<h3 class="card-title" id="sn-{ident}-title" {_t(title_key)}</h3></header>{body}</section>')


def panel_html() -> str:
    return (
        '<section class="ins sn" id="sn-root" aria-labelledby="sn-title" data-testid="sentinel-root">'
        f'<header class="ins-head"><h2 class="card-title" id="sn-title" {_t("sn_title")}</h2>'
        f'<span class="ts-badge" data-testid="sn-badge" {_t("sn_badge")}</span>'
        '<span class="muted sn-asof" id="sn-asof" data-testid="sn-asof"></span></header>'
        f'<p class="muted sn-hint" {_t("sn_hint")}</p>'
        '<p class="stale-banner" id="sn-stale" role="status" data-testid="sn-stale" hidden></p>'
        f'<p class="no-data" id="sn-not-read" data-testid="sn-not-read" hidden {_t("sn_not_read")}</p>'
        f'<p class="no-data" id="sn-off" data-testid="sn-off" hidden {_t("sn_off")}</p>'
        '<ul class="ac-kpis sn-kpis" id="sn-kpis" data-testid="sn-kpis"></ul>'
        '<div class="sn-grid" id="sn-grid">'
        # parte
        '<section class="card sn-card sn-wide" aria-labelledby="sn-parte-title" data-testid="sn-parte-card"><header class="card-head">'
        f'<h3 class="card-title" id="sn-parte-title" {_t("sn_parte_title")}</h3></header>'
        '<ul class="sn-parte" id="sn-parte" data-testid="sn-parte"></ul></section>'
        # signatures
        + _card("sig", "sn_sig_title", body='<ul class="sn-sigs" id="sn-sigs" data-testid="sn-sigs"></ul><p class="sn-bad-note" id="sn-sig-bad" data-testid="sn-sig-bad" hidden></p>')
        # ci
        + _card("ci", "sn_ci_title", body='<p class="muted sn-small" id="sn-ci-sum"></p><p class="no-data" id="sn-ci-none" data-testid="sn-ci-none" hidden></p>'
                '<div class="sn-scroll" tabindex="0" role="region" aria-labelledby="sn-ci-title" id="sn-ci-wrap"><table class="ins-table sn-table" id="sn-ci-table" data-testid="sn-ci-table"><thead><tr><th scope="col" data-i18n="sn_col_repo">Repository</th></tr></thead></table></div>')
        # releases
        + _card("rel", "sn_rel_title", body='<p class="muted sn-small" id="sn-rel-rule"></p><p class="no-data" id="sn-rel-none" data-testid="sn-rel-none" hidden></p>'
                '<div class="sn-scroll" tabindex="0" role="region" aria-labelledby="sn-rel-title" id="sn-rel-wrap"><table class="ins-table sn-table" id="sn-rel-table" data-testid="sn-rel-table"><thead><tr><th scope="col" data-i18n="sn_col_repo">Repository</th></tr></thead></table></div>')
        # hygiene
        + _card("hyg", "sn_hyg_title", body='<ul class="sn-hyg" id="sn-hyg" data-testid="sn-hyg"></ul>')
        # compute
        + _card("cmp", "sn_cmp_title", body='<p class="muted sn-small" id="sn-cmp-total" data-testid="sn-cmp-total"></p><p class="no-data" id="sn-cmp-none" hidden></p><ul class="ac-bars" id="sn-cmp" data-testid="sn-cmp"></ul>')
        # trend
        + _card("trend", "sn_trend_title", "sn-wide", body='<p class="no-data" id="sn-trend-none" data-testid="sn-trend-none" hidden></p><ul class="sn-trend" id="sn-trend" data-testid="sn-trend"></ul>')
        + '</div>'
        '<div class="ac-foot sn-foot"><details class="ts-help" data-testid="sn-help">'
        f'<summary {_t("sn_help_summary")}</summary><p id="sn-help-body" data-testid="sn-help-body"></p></details>'
        f'<p class="muted ac-note" data-testid="sn-excl"><b data-i18n="sn_excl_title">{esc(EN["sn_excl_title"])}</b>: <span data-i18n="sn_excl_body">{esc(EN["sn_excl_body"])}</span></p></div>'
        '</section>'
    )


CSS = r"""
  /* ======================= Sentinel ======================= */
  #panel-sentinel .panel-inner { height: 100%; max-width: none; }
  .sn { display: flex; flex-direction: column; gap: 8px; height: 100%; min-height: 0; }
  .sn .ins-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
  .sn-asof { font-size: 12px; margin-left: auto; font-variant-numeric: tabular-nums; }
  .sn-hint { margin: 0; font-size: 12.5px; }
  .sn-kpis { grid-template-columns: repeat(6, minmax(0, 1fr)); }
  .sn-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; flex: 1 1 auto; min-height: 0; align-content: start; }
  .sn-card { padding: 9px 12px; min-width: 0; }
  .sn-card .card-head { margin-bottom: 4px; }
  .sn-wide { grid-column: span 2; }
  .sn-small { margin: 0 0 4px; font-size: 11.5px; }
  .sn-scroll { max-height: 128px; overflow: auto; }
  #panel-sentinel .sn-table th, #panel-sentinel .sn-table td { white-space: nowrap; font-size: 12px; padding: 0 8px; height: 26px; text-align: left; }
  .sn-table .ac-link { min-height: 24px; min-width: 24px; }
  #panel-sentinel .sn-table td.num { text-align: right; font-variant-numeric: tabular-nums; }
  .sn-parte { list-style: none; margin: 0; padding: 0; display: grid; gap: 4px; }
  .sn-parte li { display: flex; align-items: baseline; gap: 8px; font-size: 13px; line-height: 1.35; }
  .sn-parte li.sn-head { font-weight: 700; font-size: 14px; }
  .sn-lvl { display: inline-flex; align-items: center; gap: 5px; flex: 0 0 auto; min-width: 92px; font-size: 11.5px; font-weight: 700; }
  .sn-gl { display: inline-flex; align-items: center; justify-content: center; width: 17px; height: 17px; border-radius: 4px; font-size: 11px; font-weight: 800; color: var(--ink-on-fill); }
  .sn-l-ok { background: var(--k-success); }
  .sn-l-bad { background: var(--k-failure); }
  .sn-l-warn { background: var(--k-pending); }
  .sn-l-info, .sn-l-unknown { background: #64748b; }
  .sn-sigs { list-style: none; margin: 0; padding: 0; display: grid; gap: 3px; font-size: 12.5px; }
  .sn-sigs li { display: flex; align-items: center; gap: 7px; }
  .sn-sigs b { margin-left: auto; font-variant-numeric: tabular-nums; }
  .sn-bad-note { margin: 6px 0 0; font-size: 12px; font-weight: 700; color: var(--err); }
  .sn-hyg { list-style: none; margin: 0; padding: 0; display: grid; gap: 4px; font-size: 12px; }
  .sn-hyg li { display: flex; gap: 7px; align-items: baseline; min-width: 0; overflow-wrap: anywhere; }
  .sn-trend { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px 18px; }
  .sn-trend li { display: grid; grid-template-columns: 112px minmax(0, 1fr) 44px; gap: 10px; align-items: center; font-size: 12px; }
  .sn-trend b { text-align: right; }
  .sn-chart { display: block; line-height: 0; min-width: 0; border-bottom: 1px solid var(--border); }
  .sn-spark { width: 100%; height: 38px; display: block; }
  .sn-spark polyline { fill: none; stroke: var(--accent); stroke-width: 2.2; stroke-linejoin: round; stroke-linecap: round; vector-effect: non-scaling-stroke; }
  .sn-trend b { font-variant-numeric: tabular-nums; }
  .sn-foot { margin-top: 0; }
  @media (prefers-reduced-motion: no-preference) {
    .sn-spark polyline { stroke-dasharray: 400; stroke-dashoffset: 400; animation: sn-draw .8s ease forwards; }
    @keyframes sn-draw { to { stroke-dashoffset: 0; } }
  }
  @media (max-width: 1250px) { .sn-kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
  @media (max-width: 1100px) { #panel-sentinel .panel-inner, .sn { height: auto; } .sn-grid { grid-template-columns: minmax(0, 1fr); } .sn-wide { grid-column: auto; } .sn-trend { grid-template-columns: minmax(0, 1fr); } }
  @media (max-width: 760px) { .sn-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); } .sn-asof { margin-left: 0; } .sn-lvl { min-width: 0; } .sn-parte li { flex-wrap: wrap; } .sn-trend li { grid-template-columns: minmax(0, 1fr); } }
  @media print { #panel-sentinel .panel-inner, .sn { height: auto !important; } .sn-scroll { max-height: none !important; overflow: visible !important; } .sn-spark polyline { animation: none !important; stroke-dashoffset: 0 !important; } }
"""

JS = r"""
  // ---------------- Sentinel: public-safe watch decided by rules, read when the page was generated ----------------
  // Drawn from the JSON embedded in the page; nothing is requested. What could not be read is "not verified", never a green state.
  const SN = (DATA.sentinel && typeof DATA.sentinel === "object") ? DATA.sentinel : { enabled: false, read: false, stale: null, sections: {}, doc: null };
  const SN_GLYPH = { ok: "✓", info: "●", warn: "▲", bad: "✕", unknown: "–" };
  const snAsofMs = SN.doc && SN.doc.asof ? Date.parse(SN.doc.asof) : NaN;
  function snOn(section) { return !SN.sections || SN.sections[section] !== false; }
  function snAgoIso(iso, dict) {
    const t = Date.parse(iso || "");
    if (isNaN(t)) { return "–"; }
    const m = Math.max(0, Math.round((Date.now() - t) / 60000));
    if (m < 120) { return tpl(dict.sn_ago_min, { n: m }); }
    if (m < 48 * 60) { return tpl(dict.sn_ago_h, { n: Math.round(m / 60) }); }
    return tpl(dict.sn_ago_d, { n: Math.round(m / 1440) });
  }
  function snNames(list, dict) {
    const shown = list.slice(0, 5).join(", ");
    return list.length > 5 ? shown + " " + tpl(dict.sn_more, { n: list.length - 5 }) : shown;
  }
  function snGlyph(level, dict) {
    const g = make("span", "sn-gl sn-l-" + level, SN_GLYPH[level] || "–"); g.setAttribute("aria-hidden", "true");
    const w = make("span", "sn-lvl"); w.appendChild(g); w.appendChild(document.createTextNode(dict["sn_lvl_" + level] || dict.not_verified));
    return w;
  }
  function snRepoCell(name, parent) {
    if (DATA.repos && DATA.repos[name]) {
      const b = make("button", "ac-link", name); b.type = "button"; b.addEventListener("click", function () { openPanel(name, b); }); parent.appendChild(b);
    } else { parent.textContent = name; }
  }
  function snTable(table, heads, rows, dict) {
    table.textContent = "";
    const hr = make("tr"); heads.forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
    const body = make("tbody");
    rows.forEach(function (cells) {
      const tr = make("tr");
      cells.forEach(function (cell, i) {
        const el = make(i === 0 ? "th" : "td", typeof cell === "number" ? "num" : "");
        if (i === 0) { el.setAttribute("scope", "row"); snRepoCell(String(cell), el); } else { el.textContent = String(cell); }
        tr.appendChild(el);
      });
      body.appendChild(tr);
    });
    table.appendChild(body);
  }
  function snKpis(doc, dict) {
    const list = document.getElementById("sn-kpis");
    list.textContent = "";
    const items = [];
    const val = function (n) { return doc ? String(n) : dict.not_verified; };
    if (snOn("ci")) { items.push(["red", val(doc && doc.ci.red_total), dict.sn_k_red, doc && doc.ci.red_total > 0]); }
    if (snOn("releases")) { items.push(["cand", val(doc && doc.releases.total), dict.sn_k_cand, false]); }
    if (snOn("signatures")) { items.push(["sig", val(doc && doc.signatures.invalid), dict.sn_k_sig, doc && doc.signatures.invalid > 0]); }
    if (snOn("hygiene")) { items.push(["hyg", val(doc && doc.hygiene.gaps), dict.sn_k_hyg, false]); }
    if (snOn("compute")) { items.push(["min", doc ? tpl(dict.sn_min, { n: acNum(doc.compute.total24) }) : dict.not_verified, dict.sn_k_min, false]); }
    items.push(["read", doc ? tpl(dict.sn_of, { n: doc.read, m: doc.repos }) : dict.not_verified, dict.sn_k_read, false]);
    items.forEach(function (it) {
      const li = make("li", "ac-kpi" + (it[3] ? " ac-bad" : "")); li.setAttribute("data-testid", "sn-k-" + it[0]);
      li.appendChild(make("b", "", it[1])); li.appendChild(make("span", "", it[2])); list.appendChild(li);
    });
  }
  function snParte(doc, dict) {
    const ul = document.getElementById("sn-parte");
    ul.textContent = "";
    if (!doc) { const li = make("li"); li.appendChild(snGlyph("unknown", dict)); li.appendChild(make("span", "", dict.not_verified)); ul.appendChild(li); return; }
    doc.parte.forEach(function (item, i) {
      const li = make("li", i === 0 ? "sn-head" : ""); li.setAttribute("data-key", item.key); li.setAttribute("data-level", item.level);
      const p = Object.assign({}, item.p); if (p.list) { p.list = snNames(p.list, dict); }
      li.appendChild(snGlyph(item.level, dict));
      li.appendChild(make("span", "", tpl(dict["sp_" + item.key] || "", p)));
      ul.appendChild(li);
    });
  }
  function snSigs(doc, dict) {
    const ul = document.getElementById("sn-sigs"), note = document.getElementById("sn-sig-bad");
    ul.textContent = ""; note.hidden = true;
    if (!snOn("signatures")) { ul.appendChild(make("li", "muted", dict.sn_off_section)); return; }
    const states = [["verified", "ok"], ["invalid", "bad"], ["unverifiable", "info"], ["none", "warn"], ["norelease", "info"], ["unverified", "unknown"]];
    states.forEach(function (s) {
      const li = make("li"); li.setAttribute("data-state", s[0]);
      const g = make("span", "sn-gl sn-l-" + s[1], SN_GLYPH[s[1]]); g.setAttribute("aria-hidden", "true");
      li.appendChild(g); li.appendChild(make("span", "", dict["sn_sig_" + s[0]])); li.appendChild(make("b", "", doc ? String(doc.signatures[s[0]]) : "–"));
      ul.appendChild(li);
    });
    if (doc && doc.signatures.invalid_repos.length) { note.hidden = false; note.textContent = tpl(dict.sn_sig_bad_note, { list: snNames(doc.signatures.invalid_repos, dict) }); }
  }
  function snCi(doc, dict) {
    const table = document.getElementById("sn-ci-table"), none = document.getElementById("sn-ci-none"), sum = document.getElementById("sn-ci-sum"), wrap = document.getElementById("sn-ci-wrap");
    table.textContent = ""; sum.textContent = "";
    if (!snOn("ci") || !doc) { none.hidden = false; none.textContent = !snOn("ci") ? dict.sn_off_section : dict.not_verified; wrap.hidden = true; return; }
    sum.textContent = tpl(dict.sn_ci_summary, { n: doc.ci.checked, m: doc.read });
    none.hidden = doc.ci.red.length > 0; none.textContent = dict.sn_ci_none; wrap.hidden = doc.ci.red.length === 0;
    if (doc.ci.red.length) {
      snTable(table, [dict.sn_col_repo, dict.sn_col_wf, dict.sn_col_streak, dict.sn_col_since], doc.ci.red.map(function (r) { return [r.repo, r.wf, r.streak, snAgoIso(r.since, dict)]; }), dict);
    }
  }
  function snRel(doc, dict) {
    const table = document.getElementById("sn-rel-table"), none = document.getElementById("sn-rel-none"), rule = document.getElementById("sn-rel-rule"), wrap = document.getElementById("sn-rel-wrap");
    table.textContent = ""; rule.textContent = "";
    if (!snOn("releases") || !doc) { none.hidden = false; none.textContent = !snOn("releases") ? dict.sn_off_section : dict.not_verified; wrap.hidden = true; return; }
    rule.textContent = tpl(dict.sn_rel_rule, { n: doc.releases.min_entries, d: doc.releases.days });
    none.hidden = doc.releases.candidates.length > 0; none.textContent = dict.sn_rel_none; wrap.hidden = doc.releases.candidates.length === 0;
    if (doc.releases.candidates.length) {
      snTable(table, [dict.sn_col_repo, dict.sn_col_entries, dict.sn_col_last], doc.releases.candidates.map(function (r) {
        return [r.repo, r.entries, r.published ? ((r.tag ? r.tag + " · " : "") + snAgoIso(r.published, dict)) : dict.sn_rel_never]; }), dict);
    }
  }
  function snHyg(doc, dict) {
    const ul = document.getElementById("sn-hyg");
    ul.textContent = "";
    if (!snOn("hygiene")) { ul.appendChild(make("li", "muted", dict.sn_off_section)); return; }
    if (!doc) { ul.appendChild(make("li", "muted", dict.not_verified)); return; }
    const h = doc.hygiene;
    const line = function (level, text) { const li = make("li"); li.setAttribute("data-level", level); li.appendChild(snGlyph(level, dict)); li.appendChild(make("span", "", text)); ul.appendChild(li); };
    line(h.ruleset_missing.length ? "warn" : (h.ruleset_checked ? "ok" : "unknown"), tpl(dict.sn_hyg_ruleset, { n: h.ruleset_checked - h.ruleset_missing.length, m: h.ruleset_checked }));
    if (h.ruleset_missing.length) { line("warn", tpl(dict.sn_hyg_missing, { list: snNames(h.ruleset_missing, dict) })); }
    line(h.settings_checked ? "info" : "unknown", tpl(dict.sn_hyg_settings, { n: h.settings_checked, m: doc.read }));
    if (h.sha_missing.length) { line("warn", tpl(dict.sn_hyg_sha, { list: snNames(h.sha_missing, dict) })); }
    if (h.allowed_missing.length) { line("warn", tpl(dict.sn_hyg_allowed, { list: snNames(h.allowed_missing, dict) })); }
    if (!h.gaps && h.ruleset_checked) { line("ok", dict.sn_hyg_ok); }
  }
  function snCompute(doc, dict) {
    const ul = document.getElementById("sn-cmp"), none = document.getElementById("sn-cmp-none"), total = document.getElementById("sn-cmp-total");
    ul.textContent = ""; total.textContent = "";
    if (!snOn("compute") || !doc) { none.hidden = false; none.textContent = !snOn("compute") ? dict.sn_off_section : dict.not_verified; return; }
    none.hidden = doc.compute.top.length > 0; none.textContent = dict.sn_cmp_none;
    total.textContent = tpl(dict.sn_cmp_total, { a: acNum(doc.compute.total24), b: acNum(doc.compute.total7) });
    const max = doc.compute.top.reduce(function (m, r) { return Math.max(m, r.min24); }, 1);
    doc.compute.top.forEach(function (r, i) {
      ul.appendChild(acBarRow(r.repo, r.min24 / max, tpl(dict.sn_min, { n: acNum(r.min24) }), tpl(dict.sn_cmp_row, { repo: r.repo, a: r.min24, b: r.min7 }), "p", i));
    });
  }
  function snSpark(values) {
    const W = 200, H = 36, P = 3, lo = Math.min.apply(null, values), hi = Math.max.apply(null, values), span = Math.max(1, hi - lo);
    const svg = svgEl("svg", { viewBox: "0 0 " + W + " " + H, class: "sn-spark", preserveAspectRatio: "none", "aria-hidden": "true" });
    const pts = values.map(function (v, i) { return [P + i * (W - 2 * P) / Math.max(1, values.length - 1), H - P - (v - lo) / span * (H - 2 * P)]; });
    svg.appendChild(svgEl("polyline", { points: pts.map(function (p) { return p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" ") }));
    return svg;
  }
  function snTrend(doc, dict) {
    const ul = document.getElementById("sn-trend"), none = document.getElementById("sn-trend-none");
    ul.textContent = "";
    if (!snOn("trend") || !doc) { none.hidden = false; none.textContent = !snOn("trend") ? dict.sn_off_section : dict.not_verified; return; }
    const t = doc.trend, enough = t.dates.length >= 2;
    none.hidden = enough; none.textContent = dict.sn_trend_none;
    if (!enough) { return; }
    [["red", "sn_t_red"], ["cand", "sn_t_cand"], ["gaps", "sn_t_gaps"], ["min", "sn_t_min"]].forEach(function (s) {
      const v = t[s[0]], name = dict[s[1]];
      const li = make("li"); li.setAttribute("data-series", s[0]);
      const label = tpl(dict.sn_trend_row, { name: name, last: v[v.length - 1], min: Math.min.apply(null, v), max: Math.max.apply(null, v), values: v.join(", "), from: t.dates[0], to: t.dates[t.dates.length - 1] });
      const chart = make("span", "sn-chart"); chart.setAttribute("role", "img"); chart.setAttribute("aria-label", label); chart.title = label; chart.appendChild(snSpark(v));
      li.appendChild(make("span", "", name)); li.appendChild(chart); li.appendChild(make("b", "", String(v[v.length - 1])));
      ul.appendChild(li);
    });
  }
  function snRender(dict) {
    if (!document.getElementById("sn-root")) { return; }
    const doc = SN.enabled && SN.read ? SN.doc : null;
    document.getElementById("sn-off").hidden = SN.enabled;
    document.getElementById("sn-not-read").hidden = !SN.enabled || SN.read;
    const banner = document.getElementById("sn-stale");
    banner.hidden = !SN.stale; banner.textContent = SN.stale ? tpl(dict.sn_stale, { date: String(SN.stale).slice(0, 10) }) : "";
    document.getElementById("sn-asof").textContent = doc && doc.asof ? tpl(dict.sn_asof, { time: String(doc.asof).slice(11, 16) }) : "";
    document.getElementById("sn-help-body").textContent = dict.sn_help_body;
    snKpis(doc, dict); snParte(doc, dict); snSigs(doc, dict); snCi(doc, dict); snRel(doc, dict); snHyg(doc, dict); snCompute(doc, dict); snTrend(doc, dict);
  }
"""
