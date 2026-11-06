#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_presence_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Card of the Sentinel tab that shows, per ecosystem and per repository, whether the latest release has signature files and a build attestation, and the two
fields of the panel of a repository. Drawn in the browser from `DATA.repos[name].prs` (see dashboard_presence.py); the page makes no request. Every state has a
glyph and a word. The script shares the scope of the shell (`DATA`, `make`, `tpl`, `openPanel` and the helpers of the Sentinel tab). Stdlib only.
"""
from __future__ import annotations

import dashboard_presence_texts
from dashboard_charts import esc

EN = dashboard_presence_texts.TEXTS["en"]


def card() -> str:
    return (
        '<section class="card sn-card sn-wide" id="pr-card" aria-labelledby="pr-title" data-testid="pr-card"><header class="card-head">'
        f'<h3 class="card-title" id="pr-title" data-i18n="pr_title">{esc(EN["pr_title"])}</h3></header>'
        f'<p class="muted sn-small" data-i18n="pr_hint">{esc(EN["pr_hint"])}</p>'
        '<p class="no-data" id="pr-none" data-testid="pr-none" hidden></p>'
        '<div class="sn-scroll pr-scroll" tabindex="0" role="region" aria-labelledby="pr-title" id="pr-eco-wrap"><table class="ins-table sn-table" id="pr-eco-table" data-testid="pr-eco-table"><thead><tr><th scope="col" data-i18n="sn_col_eco">Ecosystem</th></tr></thead></table></div>'
        f'<h4 class="pr-sub" data-i18n="pr_repo_title">{esc(EN["pr_repo_title"])}</h4>'
        '<div class="sn-scroll pr-scroll" tabindex="0" role="region" aria-labelledby="pr-title" id="pr-repo-wrap"><table class="ins-table sn-table" id="pr-repo-table" data-testid="pr-repo-table"><thead><tr><th scope="col" data-i18n="sn_col_repo">Repository</th></tr></thead></table></div>'
        f'<p class="muted sn-small" data-i18n="pr_unknown_note">{esc(EN["pr_unknown_note"])}</p></section>'
    )


CSS = r"""
  /* ======================= Presence of signature and attestation ======================= */
  .pr-sub { margin: 6px 0 2px; font-size: 12.5px; }
  .pr-scroll { max-height: 190px; }
  .pr-st { display: inline-flex; align-items: center; gap: 5px; }
  .pr-st small { font-size: 11px; opacity: 0.8; }
"""

JS = r"""
  // ---------------- Presence of a signature file and of a build attestation on the latest release ----------------
  const PR_STATES = ["present", "partial", "absent", "na", "unknown"];
  const PR_GLYPH = { present: "✓", partial: "▲", absent: "✕", na: "–", unknown: "?" };
  const PR_LEVEL = { present: "ok", partial: "warn", absent: "bad", na: "info", unknown: "unknown" };
  const PR_RANK = { absent: 0, partial: 1, unknown: 2, present: 3, na: 4 };
  function prOf(name) { const r = DATA.repos && DATA.repos[name]; return r && r.prs && typeof r.prs === "object" ? r.prs : null; }
  function prState(value) { return PR_STATES.indexOf(value) >= 0 ? value : "unknown"; }
  function prDetail(p, kind, dict) {
    if (kind === "sg") { return p.sg === "na" || p.sg === "unknown" ? "" : tpl(dict.pr_sig_detail, { k: p.k || 0, n: p.n || 0 }); }
    return p.at === "na" || !p.an ? "" : tpl(dict.pr_att_detail, { ak: p.ak || 0, an: p.an || 0 });
  }
  function prCell(p, kind, dict) {
    const s = prState(kind === "sg" ? p.sg : p.at);
    const span = make("span", "pr-st"); span.setAttribute("data-state", s);
    const g = make("span", "sn-gl sn-l-" + PR_LEVEL[s], PR_GLYPH[s]); g.setAttribute("aria-hidden", "true");
    span.appendChild(g); span.appendChild(document.createTextNode(dict["pr_s_" + s]));
    const d = prDetail(p, kind, dict);
    if (d) { span.appendChild(make("small", "", d)); }
    return span;
  }
  function prRender(dict) {
    const ecoTable = document.getElementById("pr-eco-table"), repoTable = document.getElementById("pr-repo-table");
    if (!ecoTable || !repoTable) { return; }
    const none = document.getElementById("pr-none"), ecoWrap = document.getElementById("pr-eco-wrap"), repoWrap = document.getElementById("pr-repo-wrap");
    ecoTable.textContent = ""; repoTable.textContent = "";
    const all = Object.keys(DATA.repos || {});
    const names = all.filter(function (n) { const p = prOf(n); return p && !(p.sg === "na" && p.at === "na"); });
    const anyRead = all.some(function (n) { return prOf(n) !== null; });
    none.hidden = names.length > 0; ecoWrap.hidden = true; repoWrap.hidden = true;
    document.querySelectorAll("#pr-card .pr-sub").forEach(function (h) { h.hidden = names.length === 0; });
    if (!names.length) { none.textContent = anyRead ? dict.pr_none : dict.not_verified; return; }
    ecoWrap.hidden = false; repoWrap.hidden = false;
    // by ecosystem
    const eco = {};
    names.forEach(function (n) {
      const key = DATA.repos[n].eco || "", p = prOf(n);
      const row = eco[key] || (eco[key] = { repos: 0, sg: {}, at: {} });
      row.repos += 1; row.sg[prState(p.sg)] = (row.sg[prState(p.sg)] || 0) + 1; row.at[prState(p.at)] = (row.at[prState(p.at)] || 0) + 1;
    });
    const cols = ["present", "partial", "absent", "unknown"];
    const heads = [dict.sn_col_eco, dict.pr_col_files];
    cols.forEach(function (s) { heads.push(dict.pr_col_sig + " · " + dict["pr_s_" + s]); });
    cols.forEach(function (s) { heads.push(dict.pr_col_att + " · " + dict["pr_s_" + s]); });
    const hr = make("tr"); heads.forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const thead = make("thead"); thead.appendChild(hr); ecoTable.appendChild(thead);
    const body = make("tbody");
    Object.keys(eco).sort().forEach(function (k) {
      const r = eco[k], tr = make("tr"); tr.setAttribute("data-eco", k);
      const th = make("th", "", SN_ECO_NAMES[k] || k); th.setAttribute("scope", "row"); tr.appendChild(th);
      tr.appendChild(make("td", "num", String(r.repos)));
      cols.forEach(function (s) { tr.appendChild(make("td", "num", String(r.sg[s] || 0))); });
      cols.forEach(function (s) { tr.appendChild(make("td", "num", String(r.at[s] || 0))); });
      body.appendChild(tr);
    });
    ecoTable.appendChild(body);
    // by repository: the worst first
    const worst = function (n) { const p = prOf(n); return Math.min(PR_RANK[prState(p.sg)], PR_RANK[prState(p.at)]); };
    const rows = names.slice().sort(function (a, b) { return worst(a) - worst(b) || (a < b ? -1 : 1); });
    const hr2 = make("tr"); [dict.sn_col_repo, dict.pr_col_files, dict.pr_col_sig, dict.pr_col_att].forEach(function (h) { hr2.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
    const thead2 = make("thead"); thead2.appendChild(hr2); repoTable.appendChild(thead2);
    const body2 = make("tbody");
    rows.forEach(function (n) {
      const p = prOf(n), tr = make("tr"); tr.setAttribute("data-repo", n);
      const th = make("th"); th.setAttribute("scope", "row"); snRepoCell(n, th); tr.appendChild(th);
      tr.appendChild(make("td", "num", String(p.n || 0)));
      const a = make("td"); a.appendChild(prCell(p, "sg", dict)); tr.appendChild(a);
      const b = make("td"); b.appendChild(prCell(p, "at", dict)); tr.appendChild(b);
      body2.appendChild(tr);
    });
    repoTable.appendChild(body2);
  }
  // The two fields of the panel of a repository.
  function prPanel(name, dict) {
    const fields = document.getElementById("repo-fields"), p = prOf(name);
    if (!fields || !p) { return; }
    [["pf_prs_sig", "sg"], ["pf_prs_att", "at"]].forEach(function (pair) {
      fields.appendChild(make("dt", "", dict[pair[0]]));
      const dd = make("dd"); dd.appendChild(prCell(p, pair[1], dict)); fields.appendChild(dd);
    });
  }
"""
