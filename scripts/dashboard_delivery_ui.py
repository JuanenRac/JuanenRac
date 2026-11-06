#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_delivery_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Delivery pipeline, signatures, legends, complete address state, collapsible side bar and links of the architecture, as parts of the status dashboard.

The script reads the JSON the page embeds (nothing is requested), uses the functions of the shell and of the other tabs (`openPanel`, `evRender`, `applyFilters`,
`writeHash`...) and is placed after them by dashboard_app.script(). Every text comes from the dictionary of the language in use. Stdlib only.
"""
from __future__ import annotations

import html

import dashboard_delivery_texts

EN = dashboard_delivery_texts.TEXTS["en"]
PIPE_STATES = ("published", "signed", "built", "release_only", "undeclared")
GLYPH = {"undeclared": "–", "release_only": "▸", "built": "◔", "signed": "◑", "published": "●"}


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def side_toggle() -> str:
    """The button of the top bar that hides and shows the side bar of filters (only on screens wide enough to have it beside the content)."""
    return (f'<button type="button" class="btn side-toggle" id="side-toggle" aria-controls="sidebar" aria-expanded="true" data-testid="side-toggle" '
            f'aria-label="{_esc(EN["side_hide"])}" title="{_esc(EN["side_hide"])}" data-i18n-aria-label="side_hide" data-i18n-title="side_hide"><span aria-hidden="true">☰</span></button>')


def pipeline_filter() -> str:
    """The row of chips under the scope bar of the projects that filters the projects by the state of their delivery pipeline."""
    chips = "".join(
        f'<button type="button" class="chip" data-filter-pipeline="{state}" aria-pressed="false" data-testid="filter-pipeline-{state}">'
        f'<span data-i18n="pipe_{state}">{_esc(EN["pipe_" + state])}</span><b>0</b></button>' for state in PIPE_STATES)
    return (f'<div class="scope-row scope-pipe" role="group" aria-labelledby="fg-pipe"><span class="scope-title" id="fg-pipe" data-i18n="filter_pipeline">{_esc(EN["filter_pipeline"])}</span>'
            f'<span class="chip-row">{chips}</span></div>')


def pipeline_th() -> str:
    return f'<th data-i18n="th_pipeline">{_esc(EN["th_pipeline"])}</th>'


def pipeline_td(name: str) -> str:
    return f'<td class="pipe-cell" data-pipe-for="{_esc(name)}"></td>'


CSS = r"""
  /* ======================= Delivery pipeline, signatures, legends, side bar ======================= */
  .side-toggle { display: none; padding: 6px 10px; line-height: 1; }
  @media (min-width: 961px) {
    .side-toggle { display: inline-flex; align-items: center; }
    .app[data-side="collapsed"] { grid-template-columns: 0 minmax(0, 1fr); }
    .app[data-side="collapsed"] .sidebar { display: none; }
  }
  td.pipe-cell { white-space: nowrap; font-size: 12.5px; }
  .pipe-badge { display: inline-flex; gap: 6px; align-items: baseline; }
  .pipe-glyph { color: var(--accent); width: 1em; text-align: center; }
  .pipe-undeclared { color: var(--dim); }
  .ev-why-btn { appearance: none; background: transparent; border: 1px solid transparent; border-radius: 8px; padding: 2px 4px; color: inherit; font: inherit; cursor: pointer; min-height: 24px; }
  .ev-why-btn:hover, .ev-why-btn[aria-expanded="true"] { border-color: var(--border-strong); background: var(--panel-2); }
  .ev-why { margin: 10px 0; padding: 10px 14px; border: 1px solid var(--border-strong); border-left-width: 6px; border-radius: var(--radius); background: var(--panel-2); }
  .ev-why[hidden] { display: none; }
  .ev-why h3 { margin: 0 0 4px; font-size: 14px; }
  .ev-why p { margin: 4px 0 8px; line-height: 1.5; max-width: 90ch; }
  .ev-why .ev-why-links { display: flex; flex-wrap: wrap; gap: 8px; }
  .ev-why .ev-why-links a, .ev-why .ev-why-links button { display: inline-block; padding: 4px 12px; border: 1px solid var(--border-strong); border-radius: 999px; }
  .ev-summary { margin: 8px 0; padding: 10px 14px; border: 1px solid var(--border); border-radius: var(--radius); background: var(--panel-2); }
  .ev-summary h3 { margin: 0 0 4px; font-size: 13px; }
  .ev-summary ul { margin: 0; padding-left: 18px; display: grid; gap: 2px; font-size: 13px; }
  .ev-summary b { font-variant-numeric: tabular-nums; }
  .ra-legend { margin: 8px 0 0; font-size: 12.5px; color: var(--dim); }
  .ra-legend b { color: var(--text); }
  .hist-gap { margin: 0 0 8px; padding: 8px 12px; border: 1px dashed var(--border-strong); border-radius: var(--radius); font-size: 13px; background: var(--panel-2); }
  .hist-gap-glyph { margin-right: 6px; }
  .alert-unsigned { border-left-color: var(--warn-ink); }
  .alert-badsig { border-left-color: var(--err); }
  .repo-fields dd { overflow-wrap: anywhere; word-break: break-word; }
  .pipe-inf { color: var(--dim); font-size: 11px; }
  .area-live { grid-column: 1 / -1; margin: 2px 0 0; font-size: 11.5px; color: var(--dim); cursor: help; }
  .arch-repo { appearance: none; background: transparent; border: 0; padding: 0; color: var(--accent); font: inherit; text-decoration: underline; cursor: pointer; text-align: left; }
  .arch-repo:hover { text-decoration-thickness: 2px; }
  .tabs-more:focus-visible, .side-toggle:focus-visible, .ev-why-btn:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
  @media print { .side-toggle, .tabs-more, .ev-why-links { display: none !important; } .ev-why[hidden] { display: none !important; } }
"""

JS = r"""
  // ---------------- Delivery pipeline, signatures, legends, address state, side bar, architecture links ----------------
  // Everything is drawn from the JSON embedded in the page; a fact that is not in it is printed as "not verified" or "not declared", never guessed.
  const DELIVERY_PIPE = ["published", "signed", "built", "release_only", "undeclared"];
  const DELIVERY_GLYPH = { undeclared: "–", release_only: "▸", built: "◔", signed: "◑", published: "●" };
  function deliveryRepo(name) { return (DATA.repos && DATA.repos[name]) || {}; }
  function deliveryPipe(name) { return deliveryRepo(name).pipeline || "undeclared"; }

  // ---- column and filter of the projects table ----
  function deliveryCells(dict) {
    document.querySelectorAll("tr.project-row").forEach(function (row) {
      const cell = row.querySelector("td.pipe-cell");
      if (!cell) { return; }
      const name = cell.getAttribute("data-pipe-for");
      const state = deliveryPipe(name);
      row.dataset.pipeline = state;
      const span = make("span", "pipe-badge pipe-" + state);
      span.appendChild(make("span", "pipe-glyph", DELIVERY_GLYPH[state])).setAttribute("aria-hidden", "true");
      span.appendChild(make("span", "", dict["pipe_" + state]));
      if (deliveryRepo(name).pipeInf) {
        const mark = make("span", "pipe-inf", "(" + dict.pv_inferred + ")"); mark.title = dict.pv_inferred; span.appendChild(mark);
      }
      cell.textContent = "";
      cell.appendChild(span);
      cell.title = dict.pipe_help;
    });
    DELIVERY_PIPE.forEach(function (state) {
      const chip = document.querySelector("[data-filter-pipeline='" + state + "'] b");
      if (chip) { chip.textContent = String(Object.keys(DATA.repos || {}).filter(function (n) { return deliveryPipe(n) === state && document.querySelector("tr.project-row td[data-pipe-for='" + n + "']"); }).length); }
    });
  }

  // ---- the panel of a repository ----
  function deliveryPanel(name, dict) {
    const repo = deliveryRepo(name);
    const fields = document.getElementById("repo-fields");
    if (!fields) { return; }
    function field(label, value) {
      fields.appendChild(make("dt", "", label));
      const dd = make("dd");
      if (value && value.nodeType) { dd.appendChild(value); } else { dd.textContent = value === "" || value === null || value === undefined ? dict.not_verified : value; }
      fields.appendChild(dd);
    }
    // What a manifest declares always wins; a value inferred from GitHub is used only where nothing is declared and says so.
    const inf = repo.inf || {};
    const tag = " · " + dict.pv_inferred;
    field(dict.pf_pipeline, dict["pipe_" + deliveryPipe(name)] + (repo.pipeInf ? tag : ""));
    const builtOn = repo.builtOn || inf.builtOn;
    field(dict.pf_built_on, builtOn ? dict["pv_" + builtOn] + (repo.builtOn ? "" : tag) : dict.pv_undeclared);
    const sigKind = repo.sigKind || inf.sigKind;
    const kind = sigKind ? dict["pv_" + sigKind] + (repo.sigKind ? "" : tag) : dict.pv_undeclared;
    field(dict.pf_signature, repo.signedOn ? kind + " · " + dict["pv_signed_" + repo.signedOn] : kind);
    field(dict.pf_release_sig, dict["sig_" + (repo.sig || "unverified")] + deliverySigDetail(repo, dict));
    if (typeof prPanel === "function") { prPanel(name, dict); }
    const artifact = repo.artifact || inf.artifact;
    if (artifact) {
      const a = make("a", "", artifact.replace("https://github.com/", ""));
      a.href = artifact; a.target = "_blank"; a.rel = "noopener noreferrer";
      if (repo.artifact) { field(dict.pf_artifact, a); } else { const box = make("span"); box.appendChild(a); box.appendChild(document.createTextNode(tag)); field(dict.pf_artifact, box); }
    } else { field(dict.pf_artifact, dict.pv_undeclared); }
    if (repo.build) {
      field(dict.pf_last_build, tpl(repo.build.art ? dict.pv_build : dict.pv_build_noart, { wf: repo.build.wf, date: String(repo.build.at).slice(0, 10) }));
    }
  }

  // ---- the detail of a signature check: how many files, which scheme, why some could not be checked ----
  function deliverySigDetail(repo, dict) {
    const x = repo && repo.sigx;
    if (!x || typeof x !== "object") { return ""; }
    const parts = [tpl(dict.sig_detail, { ok: x.ok || 0, bad: x.bad || 0, unk: x.unk || 0 })];
    if (Array.isArray(x.sch) && x.sch.length) { parts.push(tpl(dict.sig_scheme, { list: x.sch.join(", ") })); }
    if (x.ho) { parts.push(tpl(dict.sig_detail_ho, { n: x.ho })); }
    (Array.isArray(x.why) ? x.why : []).forEach(function (code) { if (dict["sig_why_" + code]) { parts.push(dict["sig_why_" + code]); } });
    return " (" + parts.join(" · ") + ")";
  }

  // ---- evidence: summary on top and the reason of every cell that is not verified ----
  function deliveryReason(name, item, status, dict) {
    const repo = deliveryRepo(name);
    if (item === "signed") { return dict["ev_why_signed_" + (repo.sig || "unverified")] + deliverySigDetail(repo, dict); }
    if (status === "unverified") { return tpl(dict.ev_why_unverified, { item: dict["ev_item_" + item] }); }
    if (item === "hw") { return dict.ev_why_hw_no; }
    return tpl(dict.ev_why_no, { item: dict["ev_item_" + item] });
  }
  function deliveryWhyBox() {
    let box = document.getElementById("ev-why");
    if (!box) {
      box = make("section", "ev-why"); box.id = "ev-why"; box.hidden = true; box.tabIndex = -1;
      box.setAttribute("aria-live", "polite"); box.setAttribute("data-testid", "ev-why");
      const anchor = document.getElementById("ev-matches");
      if (anchor) { anchor.after(box); }
    }
    return box;
  }
  var deliveryWhyFor = null;
  function deliveryShowWhy(name, item, status, opener) {
    const dict = currentDict();
    const box = deliveryWhyBox();
    const same = deliveryWhyFor && deliveryWhyFor.name === name && deliveryWhyFor.item === item && !box.hidden;
    document.querySelectorAll(".ev-why-btn[aria-expanded='true']").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
    if (same) { box.hidden = true; deliveryWhyFor = null; return; }
    deliveryWhyFor = { name: name, item: item, status: status };
    opener.setAttribute("aria-expanded", "true");
    box.textContent = "";
    box.appendChild(make("h3", "", tpl(dict.ev_why_title, { name: name, item: dict["ev_item_" + item] })));
    box.appendChild(make("p", "", deliveryReason(name, item, status, dict)));
    const links = make("div", "ev-why-links");
    const repoLink = make("a", "", dict.ev_why_repo); repoLink.href = REPO_URL + name; repoLink.target = "_blank"; repoLink.rel = "noopener noreferrer";
    links.appendChild(repoLink);
    if (item === "signed" || item === "release") {
      const rel = make("a", "", dict.ev_why_releases); rel.href = REPO_URL + name + "/releases"; rel.target = "_blank"; rel.rel = "noopener noreferrer"; links.appendChild(rel);
    }
    const panelBtn = make("button", "link-btn", dict.ev_why_panel); panelBtn.type = "button";
    panelBtn.addEventListener("click", function () { openPanel(name, panelBtn); });
    links.appendChild(panelBtn);
    const close = make("button", "link-btn", dict.ev_why_close); close.type = "button";
    close.addEventListener("click", function () { box.hidden = true; deliveryWhyFor = null; opener.setAttribute("aria-expanded", "false"); opener.focus(); });
    links.appendChild(close);
    box.appendChild(links);
    box.hidden = false;
    box.focus();
  }
  function deliveryWhyButton(name, item, status, dict) {
    const b = make("button", "ev-why-btn"); b.type = "button";
    b.setAttribute("aria-controls", "ev-why"); b.setAttribute("aria-expanded", "false");
    b.setAttribute("data-testid", "ev-why-" + item);
    b.title = dict.ev_why_open;
    b.appendChild(evMark(status, dict, item));
    b.addEventListener("click", function () { deliveryShowWhy(name, item, status, b); });
    return b;
  }
  function deliveryEvidence(dict, names) {
    let sum = document.getElementById("ev-summary");
    const controls = document.getElementById("ev-controls");
    if (!sum && controls) { sum = make("section", "ev-summary"); sum.id = "ev-summary"; sum.setAttribute("data-testid", "ev-summary"); controls.after(sum); }
    if (!sum) { return; }
    sum.textContent = "";
    sum.appendChild(make("h3", "", dict.ev_sum_title));
    const col = EV_ITEMS.indexOf("signed"), rel = EV_ITEMS.indexOf("release"), hw = EV_ITEMS.indexOf("hw");
    let unsigned = 0, verified = 0, invalid = 0, present = 0, unread = 0, nohw = 0, needHw = 0;
    names.forEach(function (n) {
      const r = CHECKS[n];
      if (r[rel] === 1 && r[col] === 0) { unsigned += 1; }
      if (r[col] === 4) { verified += 1; }
      if (r[col] === 5) { invalid += 1; }
      if (r[col] === 3) { present += 1; }
      if (r[rel] === 1 && r[col] === null) { unread += 1; }
      if (r[hw] !== 2) { needHw += 1; if (r[hw] !== 1) { nohw += 1; } }
    });
    const ul = make("ul");
    [["unsigned", unsigned, {}], ["verified", verified, {}], ["invalid", invalid, {}], ["present", present, {}], ["sigunk", unread, {}], ["nohw", nohw, { m: needHw }]].forEach(function (row) {
      const li = make("li"); li.setAttribute("data-sum", row[0]); li.setAttribute("data-n", String(row[1]));
      li.textContent = tpl(dict["ev_sum_" + row[0]], Object.assign({ n: row[1] }, row[2]));
      ul.appendChild(li);
    });
    sum.appendChild(ul);
  }

  // ---- the checks of the host programs are not tests ----
  function deliveryTestsNote(dict) {
    const help = document.querySelector(".ts-help");
    if (!help) { return; }
    let note = document.getElementById("ts-checks-note");
    if (!note) { note = make("p", "muted"); note.id = "ts-checks-note"; note.setAttribute("data-testid", "ts-checks-note"); help.before(note); }
    note.textContent = dict.ts_checks_note;
  }

  // ---- the axes of the radars ----
  function deliveryRadar(dict) {
    const grid = document.getElementById("ra-grid");
    if (!grid) { return; }
    let legend = document.getElementById("ra-legend");
    if (!legend) { legend = make("p", "ra-legend"); legend.id = "ra-legend"; legend.setAttribute("data-testid", "ra-legend"); grid.after(legend); }
    const list = INS_AREAS.map(function (a, i) { return (i + 1) + " " + dict["area_" + a]; }).join(" · ");
    legend.textContent = tpl(dict.ra_axes, { list: list });
  }

  // ---- history that is still too short for a view ----
  function deliveryHistory(dict) {
    const need = Number(CFG.history_min_days) || 7;
    const dates = {};
    (Array.isArray(DATA.history) ? DATA.history : []).forEach(function (e) { if (e && typeof e.date === "string") { dates[e.date] = true; } });
    const have = Object.keys(dates).length;
    const missing = Math.max(0, need - have);
    ["deps", "miles", "dates", "debt"].forEach(function (view) {
      const section = document.querySelector("[data-ins-section='" + view + "']");
      if (!section) { return; }
      let note = section.querySelector(".hist-gap");
      if (!missing) { if (note) { note.remove(); } return; }
      if (!note) { note = make("p", "hist-gap"); note.setAttribute("role", "status"); note.setAttribute("data-testid", "hist-gap-" + view); section.prepend(note); }
      const eta = new Date(Date.now() + missing * 86400000).toISOString().slice(0, 10);
      note.textContent = "";
      note.appendChild(make("span", "hist-gap-glyph", "◷")).setAttribute("aria-hidden", "true");
      note.appendChild(document.createTextNode(tpl(dict.hist_gap, { have: have, need: need, n: missing, date: eta })));
      note.setAttribute("data-missing", String(missing));
    });
  }

  // ---- the build that is green but has no signed release (optional alert, off unless the configuration turns it on) ----
  // A signature that does not verify is always an alert (it is a fact, not a threshold).
  function deliveryBadSignatureAlerts(list, dict) {
    const found = Object.keys(DATA.repos || {}).filter(function (name) { return DATA.repos[name].sig === "invalid"; }).sort();
    found.forEach(function (name) {
      const r = DATA.repos[name];
      const li = make("li", "alert alert-badsig"); li.setAttribute("data-kind", "badsig"); li.setAttribute("data-testid", "alert-badsig");
      const kind = make("span", "alert-kind"); kind.appendChild(make("span", "alert-glyph", "⚠")).setAttribute("aria-hidden", "true");
      kind.appendChild(make("span", "", dict.alert_kind_badsig));
      const link = make("a", "", name); link.href = REPO_URL + name + "/releases"; link.target = "_blank"; link.rel = "noopener noreferrer";
      li.appendChild(kind); li.appendChild(link);
      li.appendChild(make("span", "alert-why", tpl(dict.alert_why_badsig, { tag: (r.release && r.release.tag) || "" })));
      list.appendChild(li);
    });
    return found.length;
  }

  function deliveryUnsignedAlerts(list, dict) {
    const cfg = CFG.signature_alert;
    if (!cfg || cfg.enabled !== true) { return 0; }
    const found = [];
    const limitHours = Number(cfg.after_hours) > 0 ? Number(cfg.after_hours) : cfg.after_days * 24;
    Object.keys(DATA.repos || {}).forEach(function (name) {
      const r = DATA.repos[name];
      const inf = r.inf || {};
      const signedAny = r.sig === "verified" || r.sig === "unverifiable" || r.sig === "present" || r.sig === "invalid";
      if (!(r.builtOn === "gha" || inf.builtOn === "gha") || r.ci !== "success" || signedAny) { return; }
      const hours = r.build && r.build.art && r.build.at ? (Date.now() - Date.parse(r.build.at)) / 3600000 : null;
      if (hours !== null) {
        if (hours > limitHours) { found.push({ name: name, hours: Math.floor(hours), days: Math.floor(hours / 24), date: String(r.build.at).slice(0, 10), build: true }); }
        return;
      }
      const days = dayCount(r.commitDate);
      if (days !== null && days * 24 > limitHours) { found.push({ name: name, hours: days * 24, days: days, date: r.commitDate.slice(0, 10), build: false }); }
    });
    found.sort(function (x, y) { return y.hours - x.hours || (x.name < y.name ? -1 : 1); });
    found.forEach(function (item) {
      const li = make("li", "alert alert-unsigned"); li.setAttribute("data-kind", "unsigned"); li.setAttribute("data-testid", "alert-unsigned");
      const kind = make("span", "alert-kind"); kind.appendChild(make("span", "alert-glyph", "✎")).setAttribute("aria-hidden", "true");
      kind.appendChild(make("span", "", dict.alert_kind_unsigned));
      const link = make("a", "", item.name); link.href = REPO_URL + item.name + "/releases"; link.target = "_blank"; link.rel = "noopener noreferrer";
      li.appendChild(kind); li.appendChild(link);
      li.appendChild(make("span", "alert-why", item.build ? tpl(dict.alert_why_unsigned_build, { n: item.hours, date: item.date }) : tpl(dict.alert_why_unsigned, { n: item.days, date: item.date })));
      list.appendChild(li);
    });
    return found.length;
  }

  // ---- the blocks of the architecture open the panel of the repository they name ----
  function deliveryArchitecture(dict) {
    document.querySelectorAll("[data-arch-panel] li, .eh3d-arch li").forEach(function (li) {
      const existing = li.querySelector("button.arch-repo");
      if (existing) { existing.setAttribute("aria-label", tpl(dict.arch_open, { name: existing.textContent })); return; }
      const name = li.textContent.trim();
      if (li.children.length || !DATA.repos || !DATA.repos[name]) { return; }
      const b = make("button", "arch-repo", name); b.type = "button";
      b.setAttribute("aria-label", tpl(dict.arch_open, { name: name }));
      b.setAttribute("data-testid", "arch-repo-" + name);
      b.addEventListener("click", function () { openPanel(name, b); });
      li.textContent = ""; li.appendChild(b);
    });
  }

  // ---- the side bar can be hidden where it is beside the content ----
  const SIDE_KEY = "hydra-dashboard-side";
  const sideBtn = document.getElementById("side-toggle");
  const appRoot = document.querySelector(".app");
  function deliverySide(collapsed, store) {
    if (!sideBtn || !appRoot) { return; }
    appRoot.setAttribute("data-side", collapsed ? "collapsed" : "open");
    sideBtn.setAttribute("aria-expanded", collapsed ? "false" : "true");
    const text = currentDict()[collapsed ? "side_show" : "side_hide"] || "";
    sideBtn.setAttribute("aria-label", text); sideBtn.title = text;
    sideBtn.setAttribute("data-i18n-aria-label", collapsed ? "side_show" : "side_hide"); sideBtn.setAttribute("data-i18n-title", collapsed ? "side_show" : "side_hide");
    if (store) { safeSet(SIDE_KEY, collapsed ? "collapsed" : "open"); }
  }
  if (sideBtn) {
    sideBtn.addEventListener("click", function () { deliverySide(appRoot.getAttribute("data-side") !== "collapsed", true); });
    deliverySide(safeGet(SIDE_KEY) === "collapsed", false);
  }

  // ---- the whole state in the address (tab, scope, filters, search, period, evidence filters, compact mode), only from known lists ----
  function deliveryKnown(kind) { return Array.from(document.querySelectorAll("[data-filter-" + kind + "]")).map(function (b) { return b.getAttribute("data-filter-" + kind); }); }
  function deliveryQuery(text) {
    return String(text || "").replace(/[\u0000-\u001f\u007f<>&"'`\\]/g, "").trim().slice(0, 80);
  }
  const DELIVERY_KEYS = { status: "st", maturity: "mat", role: "role", deploy: "dep", pipeline: "pipe" };
  hashWriters.push(function (query) {
    Object.keys(DELIVERY_KEYS).forEach(function (kind) { if (state[kind] && state[kind] !== "all") { query.push(DELIVERY_KEYS[kind] + "=" + encodeURIComponent(state[kind])); } });
    if (familySelect && familySelect.value !== "all") { query.push("fam=" + encodeURIComponent(familySelect.value)); }
    const q = deliveryQuery(searchInput && searchInput.value);
    if (q) { query.push("q=" + encodeURIComponent(q)); }
    if (evoState.days !== 90) { query.push("days=" + evoState.days); }
    if (evState.eco !== "all") { query.push("evc=" + encodeURIComponent(evState.eco)); }
    if (evState.missing.length) { query.push("evm=" + evState.missing.join(",")); }
    if (evState.unverified) { query.push("evu=1"); }
  });
  hashAppliers.push(function (params) {
    let touched = false;
    Object.keys(DELIVERY_KEYS).forEach(function (kind) {
      const value = params[DELIVERY_KEYS[kind]];
      const next = value && deliveryKnown(kind).indexOf(value) >= 0 ? value : "all";
      if (value !== undefined || state[kind] !== "all") { if (state[kind] !== next) { state[kind] = next; syncButtons(kind); touched = true; } }
    });
    if (familySelect) {
      const f = params.fam;
      const ok = f && Array.from(familySelect.options).some(function (o) { return o.value === f; });
      const next = ok ? f : "all";
      if (familySelect.value !== next && (f !== undefined || familySelect.value !== "all")) { familySelect.value = next; touched = true; }
    }
    if (searchInput && (params.q !== undefined || searchInput.value)) {
      const q = deliveryQuery(params.q);
      if (searchInput.value !== q) { searchInput.value = q; touched = true; }
    }
    if (touched) { applyFilters(true); }
    if (params.days === "30" || params.days === "90") {
      const button = document.querySelector("[data-evo-days='" + params.days + "']");
      if (button && String(evoState.days) !== params.days) { button.click(); }
    }
    const ecoOk = params.evc && (params.evc === "all" || EV_ECOS.indexOf(params.evc) >= 0);
    const missing = (params.evm || "").split(",").filter(function (k, i, all) { return EV_ITEMS.indexOf(k) >= 0 && all.indexOf(k) === i; });
    const unv = params.evu === "1";
    const eco = ecoOk ? params.evc : "all";
    if (evState.eco !== eco || evState.unverified !== unv || evState.missing.join(",") !== missing.join(",")) {
      evState.eco = eco; evState.missing = missing; evState.unverified = unv; evRender(currentDict());
    }
  });
  // Any change of a filter, of the search or of the period rewrites the address.
  ["click", "input", "change"].forEach(function (type) {
    document.addEventListener(type, function (event) {
      const t = event.target;
      if (!t || !t.closest || !hashReady) { return; }
      if (t.closest("[data-filter-status], [data-filter-maturity], [data-filter-role], [data-filter-deploy], [data-filter-pipeline], [data-filter-eco], [data-sub-family], [data-sub-role], [data-ev-eco], [data-ev-missing], [data-ev-unverified], [data-evo-days], #reset-filters, #ev-reset, #project-search, #family-select")) {
        setTimeout(function () { writeHash(); }, 0);
      }
    });
  });
  hashReady = true;
  hashAppliers.forEach(function (apply) { apply(startHash.params); });
  writeHash();

  function deliveryApplied(dict) {
    deliveryCells(dict); deliveryTestsNote(dict); deliveryRadar(dict); deliveryHistory(dict); deliveryArchitecture(dict);
    if (sideBtn) { deliverySide(appRoot.getAttribute("data-side") === "collapsed", false); }
    if (panelFor) { /* the panel is redrawn by renderPanel, which calls deliveryPanel */ }
  }
"""
