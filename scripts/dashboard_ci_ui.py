#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_ci_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The view "declared against verified" of the evidence tab: what each manifest claims next to what the CI of the repository proved.

The markup comes from this module; the table is drawn in the browser from the JSON the page already embeds (`ciEvidence`, see dashboard_ci_evidence.py), so the page
makes no request of its own. The script is placed into the shell's own scope (it uses `DATA`, `make`, `tpl`, `currentDict` and `openPanel`) before the script of the
evidence checklist, which calls `ciRender` whenever the language changes. Stdlib only.
"""
from __future__ import annotations

import dashboard_ci_evidence
import dashboard_ci_texts
from dashboard_charts import esc

EN = dashboard_ci_texts.TEXTS["en"]


def _t(key: str) -> str:
    return f'data-i18n="{key}">{esc(EN[key])}'


def view() -> str:
    chips = ['<button type="button" class="chip" data-cie-state="all" aria-pressed="true" data-testid="cie-state-all"><span data-i18n="cie_filter_all">All</span> <b data-cie-count="all"></b></button>']
    for state in dashboard_ci_evidence.STATES:
        chips.append(f'<button type="button" class="chip" data-cie-state="{state}" aria-pressed="false" data-testid="cie-state-{state}">'
                     f'<span data-i18n="cie_st_{state}">{esc(EN["cie_st_" + state])}</span> <b data-cie-count="{state}"></b></button>')
    return (
        '<section class="card ev-view cie-view" id="cie-view" aria-labelledby="cie-title" data-testid="cie-view">'
        f'<header class="card-head"><h2 class="card-title" id="cie-title" {_t("cie_title")}</h2></header>'
        f'<p class="muted" {_t("cie_hint")}</p>'
        '<p class="muted" id="cie-source" data-testid="cie-source"></p>'
        f'<p class="no-data" id="cie-not-read" data-testid="cie-not-read" hidden {_t("cie_not_read")}</p>'
        '<div class="ev-controls"><div class="ev-group" role="group" aria-labelledby="cie-filter-t">'
        f'<span class="scope-title" id="cie-filter-t" {_t("cie_filter_title")}</span><span class="chip-row">{"".join(chips)}</span></div></div>'
        '<p class="matches" id="cie-matches" aria-live="polite" data-testid="cie-matches"></p>'
        '<div class="ev-table-wrap" tabindex="0" role="region" aria-labelledby="cie-title" data-testid="cie-table-wrap">'
        '<table class="ev-table cie-table" id="cie-table" data-testid="cie-table"><thead><tr><th scope="col" data-i18n="cie_col_repo">Repository</th></tr></thead></table></div>'
        f'<p class="no-data" id="cie-none" data-testid="cie-none" hidden {_t("cie_none")}</p>'
        '</section>'
    )


CSS = r"""
  /* ======================= Declared against verified ======================= */
  .cie-st { display: inline-flex; gap: 6px; align-items: center; font-weight: 600; }
  .cie-glyph { display: inline-flex; align-items: center; justify-content: center; min-width: 22px; height: 22px; border-radius: 6px; border: 1px solid currentColor; font-size: 13px; line-height: 1; }
  .cie-verified { color: var(--ok); } .cie-below, .cie-failing, .cie-invalid { color: var(--err); }
  .cie-expired, .cie-nodata, .cie-unread { color: var(--dim); } .cie-expired .cie-glyph, .cie-nodata .cie-glyph, .cie-unread .cie-glyph { border-style: dashed; }
  .cie-table td, .cie-table th { text-align: left; }
  .cie-table .cie-label { color: var(--text); font-weight: 400; }
"""

JS = r"""
  // ---------------- Declared against verified: the evidence the CI of each repository published ----------------
  // Drawn from the JSON embedded in the page; a repository that published nothing is "not verified", never "verified".
  const CIE = (DATA.ciEvidence && typeof DATA.ciEvidence === "object" && DATA.ciEvidence.repos) ? DATA.ciEvidence : { read: false, repos: {}, expire: {} };
  const CIE_STATES = ["verified", "below", "failing", "expired", "nodata", "invalid", "unread"];
  const CIE_ORDER = ["failing", "below", "expired", "invalid", "unread", "nodata", "verified"];
  const CIE_GLYPH = { verified: "✓", below: "▼", failing: "✕", expired: "◷", nodata: "?", invalid: "!", unread: "?" };
  const cieState = { filter: "all" };
  function cieNames() {
    return Object.keys(CIE.repos).sort(function (a, b) {
      const d = CIE_ORDER.indexOf(CIE.repos[a].state) - CIE_ORDER.indexOf(CIE.repos[b].state);
      return d !== 0 ? d : (a.toLowerCase() < b.toLowerCase() ? -1 : 1);
    });
  }
  function cieLevel(dict, level) { return level && dict["evidence_" + level] ? dict["evidence_" + level] : dict.not_verified; }
  function ciRender(dict) {
    const root = document.getElementById("cie-view");
    const table = document.getElementById("cie-table");
    if (!root || !table) { return; }
    const names = cieNames();
    const tally = { all: names.length };
    CIE_STATES.forEach(function (s) { tally[s] = 0; });
    names.forEach(function (n) { tally[CIE.repos[n].state] += 1; });
    root.querySelectorAll("[data-cie-count]").forEach(function (b) { b.textContent = String(tally[b.getAttribute("data-cie-count")]); });
    root.querySelectorAll("[data-cie-state]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-cie-state") === cieState.filter ? "true" : "false"); });
    const exp = CIE.expire || {};
    document.getElementById("cie-source").textContent = tpl(dict.cie_source, { source: CIE.source || "", host: exp["host-test"], sim: exp.simulator, bench: exp.bench, field: exp.field });
    document.getElementById("cie-not-read").hidden = !!CIE.read;
    table.textContent = "";
    table.appendChild(make("caption", "sr-only", dict.cie_caption));
    const head = make("thead"); const hr = make("tr");
    ["cie_col_repo", "filter_ecosystem", "cie_col_maturity", "cie_col_declared", "cie_col_verified", "cie_col_state", "cie_col_run"].forEach(function (key) {
      hr.appendChild(make("th", "", dict[key])).setAttribute("scope", "col");
    });
    head.appendChild(hr); table.appendChild(head);
    const body = make("tbody");
    let shown = 0;
    names.forEach(function (name) {
      const item = CIE.repos[name];
      if (cieState.filter !== "all" && item.state !== cieState.filter) { return; }
      shown += 1;
      const repo = DATA.repos[name] || {};
      const tr = make("tr"); tr.setAttribute("data-repo", name); tr.setAttribute("data-state", item.state);
      const first = make("th"); first.setAttribute("scope", "row");
      const open = make("button", "link-btn", name); open.type = "button";
      open.addEventListener("click", function () { openPanel(name, open); });
      first.appendChild(open); tr.appendChild(first);
      tr.appendChild(make("td", "", repo.ecoLabel || dict.not_verified));
      tr.appendChild(make("td", "", dict["cie_mat_" + repo.maturity] || dict.not_verified));
      tr.appendChild(make("td", "", cieLevel(dict, item.declared)));
      const proven = item.state === "verified" || item.state === "below" || item.state === "failing";
      tr.appendChild(make("td", "", proven || item.state === "expired" ? cieLevel(dict, proven ? item.verified : "") : dict.not_verified));
      const st = make("td"); st.setAttribute("data-cie", item.state);
      const mark = make("span", "cie-st cie-" + item.state);
      mark.appendChild(make("span", "cie-glyph", CIE_GLYPH[item.state])).setAttribute("aria-hidden", "true");
      mark.appendChild(make("span", "", dict["cie_st_" + item.state]));
      st.appendChild(mark);
      if (item.reason && item.state !== "verified") { st.title = tpl(dict.cie_reason, { reason: item.reason }); }
      tr.appendChild(st);
      const run = make("td");
      if (item.date) {
        const safe = typeof item.url === "string" && /^https:\/\/github\.com\/[A-Za-z0-9._-]+\/[A-Za-z0-9._-]+\//.test(item.url);
        if (safe) {
          const a = make("a", "", item.date); a.href = item.url; a.target = "_blank"; a.rel = "noopener noreferrer";
          a.setAttribute("aria-label", tpl(dict.cie_link_aria, { name: name }) + " (" + item.date + ")");
          run.appendChild(a);
        } else { run.textContent = item.date; }
      } else { run.textContent = dict.cie_no_run; }
      tr.appendChild(run);
      body.appendChild(tr);
    });
    table.appendChild(body);
    const counter = document.getElementById("cie-matches");
    counter.textContent = tpl(dict.cie_matches, { shown: shown, total: names.length });
    counter.setAttribute("data-shown", String(shown)); counter.setAttribute("data-total", String(names.length));
    document.getElementById("cie-none").hidden = shown > 0 || names.length === 0;
    table.hidden = shown === 0;
  }
  document.querySelectorAll("[data-cie-state]").forEach(function (b) {
    b.addEventListener("click", function () { cieState.filter = b.getAttribute("data-cie-state"); ciRender(currentDict()); });
  });
"""
