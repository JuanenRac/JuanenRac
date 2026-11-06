#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_pins_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Card of the Sentinel tab with the shared-contract pins of every ecosystem (see dashboard_pins.py). Drawn in the browser from `DATA.pins`; the page makes no
request. Every state has a glyph and a word. The script shares the scope of the shell (`DATA`, `make`, `tpl` and the helpers of the Sentinel tab). Stdlib only.
"""
from __future__ import annotations

import dashboard_pins_texts
from dashboard_charts import esc

EN = dashboard_pins_texts.TEXTS["en"]


def card() -> str:
    return (
        '<section class="card sn-card sn-wide" id="pn-card" aria-labelledby="pn-title" data-testid="pn-card"><header class="card-head">'
        f'<h3 class="card-title" id="pn-title" data-i18n="pn_title">{esc(EN["pn_title"])}</h3></header>'
        f'<p class="muted sn-small" data-i18n="pn_hint">{esc(EN["pn_hint"])}</p>'
        '<div id="pn-body" data-testid="pn-body"></div></section>'
    )


CSS = r"""
  /* ======================= Shared contract pins ======================= */
  .pn-eco { margin: 8px 0 2px; font-size: 12.5px; }
  .pn-scroll { max-height: 190px; }
  @media print {
    .pn-scroll { max-height: none; overflow: visible; }
    #panel-sentinel #pn-card .sn-table { width: 100%; table-layout: fixed; }
    #panel-sentinel #pn-card .sn-table th, #panel-sentinel #pn-card .sn-table td { white-space: normal; overflow-wrap: anywhere; height: auto; }
  }
"""

JS = r"""
  // ---------------- Pins of the shared contracts (read from the files the repositories publish) ----------------
  const PN_GLYPH = { current: "✓", behind: "▲", ahead: "●", unknown: "?" };
  const PN_LEVEL = { current: "ok", behind: "warn", ahead: "info", unknown: "unknown" };
  function pnRender(dict) {
    const body = document.getElementById("pn-body");
    if (!body) { return; }
    body.textContent = "";
    const eco = DATA.pins && DATA.pins.eco && typeof DATA.pins.eco === "object" ? DATA.pins.eco : {};
    const keys = Object.keys(eco);
    if (!keys.length) { body.appendChild(make("p", "no-data", dict.not_verified)); return; }
    keys.forEach(function (k) {
      const e = eco[k], box = make("div", "pn-block"); box.setAttribute("data-eco", k);
      box.appendChild(make("h4", "pn-eco", SN_ECO_NAMES[k] || k));
      if (e.source === "none") { box.appendChild(make("p", "muted sn-small", dict.pn_no_source)); body.appendChild(box); return; }
      if (!e.read) { box.appendChild(make("p", "no-data", dict.not_verified)); body.appendChild(box); return; }
      box.appendChild(make("p", "muted sn-small", tpl(dict.pn_current, { v: e.current })));
      if (e.partial) { box.appendChild(make("p", "muted sn-small", dict.pn_partial)); }
      if (!e.rows.length) { box.appendChild(make("p", "no-data", dict.pn_none)); body.appendChild(box); return; }
      const wrap = make("div", "sn-scroll pn-scroll"); wrap.setAttribute("tabindex", "0"); wrap.setAttribute("role", "region");
      const table = make("table", "ins-table sn-table"); table.setAttribute("data-testid", "pn-table-" + k);
      const hr = make("tr"); [dict.sn_col_repo, dict.pn_col_pin, dict.pn_col_state].forEach(function (h) { hr.appendChild(make("th", "", h)).setAttribute("scope", "col"); });
      const thead = make("thead"); thead.appendChild(hr); table.appendChild(thead);
      const tb = make("tbody");
      e.rows.forEach(function (r) {
        const tr = make("tr"); tr.setAttribute("data-repo", r.repo); tr.setAttribute("data-state", r.state);
        const th = make("th", "", r.repo); th.setAttribute("scope", "row"); tr.appendChild(th);
        tr.appendChild(make("td", "num", r.pin || "–"));
        const td = make("td"), span = make("span", "pr-st");
        const g = make("span", "sn-gl sn-l-" + PN_LEVEL[r.state], PN_GLYPH[r.state]); g.setAttribute("aria-hidden", "true");
        span.appendChild(g); span.appendChild(document.createTextNode(dict["pn_s_" + r.state])); td.appendChild(span); tr.appendChild(td);
        tb.appendChild(tr);
      });
      table.appendChild(tb); wrap.appendChild(table); box.appendChild(wrap); body.appendChild(box);
    });
  }
"""
