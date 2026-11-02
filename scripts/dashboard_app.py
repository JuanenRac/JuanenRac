#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_app.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The application shell of the status dashboard: tabs, side panel of filters and the panels that hold charts.

generate_dashboard.py keeps producing every table, card and section it always produced; this module only adds the shell around them
(tab list, filter panel) and the summary and ecosystem panels, drawn on the server from the data the generator already has plus
scripts/dashboard_charts.py. The style sheet and the script are plain strings, not templates, and are placed into the page as they are.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

import dashboard_app_texts
import dashboard_charts as charts
from dashboard_charts import Activity, Area, esc

ECOSYSTEMS: tuple[tuple[str, str], ...] = (
    ("hydra-umc", "HYDRA-UMC"),
    ("urtc", "URTC"),
    ("armor", "A.R.M.O.R."),
    ("eh3d", "EH3D"),
)
ECOSYSTEM_FILTERS: tuple[tuple[str, str], ...] = ECOSYSTEMS + (("electro-hobby-3d", "Electro Hobby 3D"),)

# (id, i18n key of the label, literal label when it is a name and not a word)
TABS: tuple[tuple[str, str, str], ...] = (
    ("summary", "tab_summary", ""),
    ("hydra-umc", "", "HYDRA-UMC"),
    ("urtc", "", "URTC"),
    ("armor", "", "A.R.M.O.R."),
    ("eh3d", "", "EH3D"),
    ("projects", "tab_projects", ""),
    ("evidence", "tab_evidence", ""),
    ("inventory", "tab_inventory", ""),
    ("architecture", "tab_architecture", ""),
    ("errors", "tab_errors", ""),
)
TAB_IDS = tuple(tab[0] for tab in TABS)
ENGLISH = {"tab_summary": "Summary", "tab_projects": "Projects", "tab_evidence": "Evidence", "tab_inventory": "Inventory",
           "tab_architecture": "Architecture", "tab_errors": "Errors / unknown"}
CI_LABELS = {"success": "Green", "failure": "Red", "pending": "Pending", "none": "No CI / unknown"}
LIGHT_GLYPH = {"good": "●", "fair": "◐", "poor": "◔", "bad": "○"}
AREA_ENGLISH = {"software": "Software", "tests": "Tests", "ci": "Continuous integration", "releases": "Releases", "docs": "Documentation",
                "simulation": "Simulation", "hardware": "Real hardware", "production": "Production"}


@dataclass
class AppData:
    """Everything the panels draw; built by generate_dashboard.render_html."""
    total: int
    ok: int
    errors: int
    success_percent_text: str
    ecosystem_by_name: Mapping[str, str]
    maturity_labels: Mapping[str, str]
    evidence_labels: Mapping[str, str]
    status: Mapping[str, Mapping[str, Area]]
    progress: Mapping[str, tuple[int, int | None]]
    maturity: Mapping[str, Mapping[str, int]]
    evidence: Mapping[str, Mapping[str, int]]
    activity: Mapping[str, Activity]
    issues: Sequence[object] = field(default_factory=list)
    unresolved: Sequence[tuple[str, str]] = field(default_factory=list)   # (repository, reason) for a listed project without a version
    repo_url: str = "https://github.com/JuanenRac/"


# ---------------------------------------------------------------------------
# Small pieces
# ---------------------------------------------------------------------------

def _names_of(data: AppData, eco: str | None) -> set[str] | None:
    if eco is None:
        return None
    return {name for name, key in data.ecosystem_by_name.items() if key == eco}


def legend(keys: Sequence[str], prefix: str, i18n_prefix: str, labels: Mapping[str, str], extra: Sequence[tuple[str, str, str]] = ()) -> str:
    """A legend whose every entry is text with a swatch (never colour alone)."""
    items = [f'<li><span class="swatch sw-{prefix}-{esc(key)}" aria-hidden="true"></span><span data-i18n="{i18n_prefix}{esc(key)}">{esc(labels.get(key, key))}</span></li>' for key in keys]
    items += [f'<li><span class="swatch sw-{prefix}-{esc(key)}" aria-hidden="true"></span><span data-i18n="{esc(i18n)}">{esc(text)}</span></li>' for key, i18n, text in extra]
    return f'<ul class="legend">{"".join(items)}</ul>'


def figure(title_key: str, title: str, desc_key: str, desc: str, chart: str, table: str, legend_html: str = "", fig_id: str = "", testid: str = "") -> str:
    """A chart with a visible title, a description that is also its accessible name and a hidden data table."""
    ident = esc(fig_id)
    desc = desc or dashboard_app_texts.TEXTS["en"].get(desc_key, "")
    return (
        f'<figure class="chart-figure" role="group" aria-labelledby="{ident}-t" aria-describedby="{ident}-d" data-testid="{esc(testid or fig_id)}">'
        f'<figcaption><span class="card-title" id="{ident}-t" data-i18n="{esc(title_key)}">{esc(title)}</span>'
        f'<span class="sr-only" id="{ident}-d" data-i18n="{esc(desc_key)}">{esc(desc)}</span></figcaption>'
        f'{chart}{legend_html}{table}</figure>'
    )


def no_data(text_key: str = "no_data", text: str = "No data") -> str:
    return f'<p class="no-data" data-i18n="{esc(text_key)}">{esc(text)}</p>'


def meter_rows(areas: Mapping[str, Area] | None, eco_label: str, big: bool = False) -> str:
    """The eight status areas of one ecosystem as labelled bars: name, glyph for the light, percentage and k/n."""
    if not areas:
        return no_data()
    rows = []
    for area in charts.AREAS:
        value = areas.get(area)
        if value is None:
            rows.append(f'<li class="area"><span class="area-name" data-i18n="area_{area}">{AREA_ENGLISH[area]}</span><span class="area-bar"></span><span class="area-num">–</span></li>')
            continue
        state = charts.LIGHT_CLASS.get(value.light, "bad")
        count = f"{value.count}/{value.total}" if value.count is not None else ""
        label = f"{AREA_ENGLISH[area]}: {value.percent}%" + (f" ({value.count} of {value.total})" if value.count is not None else "")
        rows.append(
            f'<li class="area area-{state}" data-area="{area}" data-testid="area-{esc(eco_label)}-{area}">'
            f'<span class="area-name"><span class="area-glyph" aria-hidden="true">{LIGHT_GLYPH[state]}</span><span data-i18n="area_{area}">{AREA_ENGLISH[area]}</span></span>'
            f'<span class="area-bar" role="img" aria-label="{esc(label)}"><span class="area-fill" style="width:{value.percent}%"></span></span>'
            f'<span class="area-num"><b>{value.percent}%</b><small>{count}</small></span></li>'
        )
    return f'<ul class="areas{" areas-big" if big else ""}">{"".join(rows)}</ul>'


def progress_card(data: AppData, eco: str, label: str, big: bool = False, link_tab: bool = True) -> str:
    percent, counted = data.progress.get(eco, (None, None))
    ring = charts.ring_svg(percent, f"ring-{eco}", size=124 if big else 104)
    counted_html = (f'<span class="muted" data-i18n-template="sum_repos_counted" data-n="{counted}">{counted} repositories counted</span>' if counted is not None else "")
    head = f'<button type="button" class="link-btn" data-goto-tab="{esc(eco)}">{esc(label)}</button>' if link_tab else f"<span>{esc(label)}</span>"
    summary = f"{label}: {percent}%" if percent is not None else f"{label}: no data"
    return (
        f'<article class="eco-card eco-{esc(eco)}" data-testid="progress-{esc(eco)}">'
        f'<header class="eco-head"><div class="ring-wrap" role="img" aria-label="{esc(summary)}">{ring}</div>'
        f'<div class="eco-title"><h3>{head}</h3><span class="muted" data-i18n="sum_overall">overall progress</span>{counted_html}</div></header>'
        f'{meter_rows(data.status.get(eco), eco, big)}</article>'
    )


def _rows_for(counts: Mapping[str, Mapping[str, int]], ecosystems: Sequence[tuple[str, str]]) -> list[tuple[str, dict[str, int]]]:
    return [(label, dict(counts.get(key, {}))) for key, label in ecosystems]


def stacked_figure(kind: str, data: AppData, ecosystems: Sequence[tuple[str, str]], wide: bool = False) -> str:
    """The maturity or the evidence chart for the given ecosystems."""
    if kind == "maturity":
        keys, counts, labels, prefix = charts.MATURITY_KEYS, data.maturity, data.maturity_labels, "mat"
        title_key, title, desc_key = "sum_maturity_title", "Maturity by ecosystem", "chart_maturity_desc"
        i18n_prefix = "maturity_"
    else:
        keys, counts, labels, prefix = charts.EVIDENCE_KEYS, data.evidence, data.evidence_labels, "ev"
        title_key, title, desc_key = "sum_evidence_title", "Evidence by ecosystem", "chart_evidence_desc"
        i18n_prefix = "evidence_"
    all_keys = (*keys, charts.UNKNOWN)
    rows = _rows_for(counts, ecosystems)
    wide = wide or len(ecosystems) == 1
    chart = charts.stacked_bars_svg(rows, all_keys, prefix, **({"width": 780, "label_width": 96} if wide else {}))
    head = [("chart_ecosystem_col", "Ecosystem")] + [(f"{i18n_prefix}{k}" if k != charts.UNKNOWN else "unknown", labels.get(k, "Unknown")) for k in all_keys] + [("chart_total_col", "Total")]
    table = charts.data_table(title_key, title, head, [[label, *(row.get(k, 0) for k in all_keys), sum(row.get(k, 0) for k in all_keys)] for label, row in rows])
    leg = legend(keys, prefix, i18n_prefix, labels, [(charts.UNKNOWN, "unknown", "Unknown")])
    return figure(title_key, title, desc_key, "", chart, table, leg, fig_id=f"chart-{kind}-{('all-wide' if wide else 'all') if len(ecosystems) > 1 else ecosystems[0][0]}",
                  testid=f"chart-{kind}")


def ci_figure(data: AppData, ecosystems: Sequence[tuple[str, str]]) -> str:
    if not data.activity:
        return f'<div class="chart-figure" data-testid="chart-ci"><span class="card-title" data-i18n="sum_ci_title">Continuous integration</span>{no_data("no_activity", "No release or CI data")}</div>'
    counts = {key: {k: 0 for k in charts.CI_KEYS} for key, _ in ecosystems}
    for name, eco in data.ecosystem_by_name.items():
        if eco in counts:
            counts[eco][data.activity.get(name, Activity()).ci] += 1
    rows = _rows_for(counts, ecosystems)
    chart = charts.stacked_bars_svg(rows, charts.CI_KEYS, "ci", width=780 if len(ecosystems) == 1 else 480, bar_height=22, gap=10, label_width=96 if len(ecosystems) == 1 else 76)
    table = charts.data_table("sum_ci_title", "Continuous integration", [("chart_ecosystem_col", "Ecosystem")] + [(f"ci_{k}", CI_LABELS[k]) for k in charts.CI_KEYS],
                              [[label, *(row[k] for k in charts.CI_KEYS)] for label, row in rows])
    leg = legend(charts.CI_KEYS, "ci", "ci_", CI_LABELS)
    return figure("sum_ci_title", "Continuous integration", "chart_ci_desc", "", chart, table, leg, fig_id=f"chart-ci-{'all' if len(ecosystems) > 1 else ecosystems[0][0]}", testid="chart-ci")


def months_figure(data: AppData, names: set[str] | None, fig_id: str = "chart-months") -> str:
    if not data.activity:
        return ""
    values = [act.release_date for name, act in data.activity.items() if names is None or name in names]
    items = charts.last_months(values, 6)
    if not items or not any(v for _l, v in items):
        return ""
    chart = charts.columns_svg(items)
    table = charts.data_table("sum_months_title", "Repositories by month of their latest release", [("chart_month_col", "Month"), ("chart_repos_col", "Repositories")], [[l, v] for l, v in items])
    return figure("sum_months_title", "Repositories by month of their latest release", "chart_months_desc", "", chart, table, fig_id=fig_id, testid="chart-months")


def _time_item(name: str, act: Activity, field_name: str, repo_url: str) -> str:
    iso = getattr(act, field_name) or ""
    tag = f'<span class="tag">{esc(act.release_tag)}</span>' if field_name == "release_date" and act.release_tag else ""
    return (f'<li><a href="{esc(repo_url + name)}" target="_blank" rel="noopener noreferrer">{esc(name)}</a>{tag}'
            f'<time datetime="{esc(iso)}">{esc(iso[:10])}</time>'
            f'<span class="age" data-iso="{esc(iso)}" data-i18n-template="age_days" data-n=""></span></li>')


def releases_lists(data: AppData, names: set[str] | None, limit: int = 7, prefix: str = "") -> tuple[str, str]:
    """(latest releases card, longest without a release card)."""
    if not data.activity:
        empty = f'<div class="card-body">{no_data("no_activity", "No release or CI data")}</div>'
        return empty, empty
    latest = charts.newest(data.activity, "release_date", limit, names)
    old = charts.oldest(data.activity, "release_date", limit, names)
    scope = [n for n in data.activity if (names is None or n in names) and n in data.ecosystem_by_name]
    never = sum(1 for n in scope if not data.activity[n].release_date)
    latest_html = "".join(_time_item(n, a, "release_date", data.repo_url) for n, a in latest) or f"<li>{no_data()}</li>"
    old_html = "".join(_time_item(n, a, "release_date", data.repo_url) for n, a in old) or f"<li>{no_data()}</li>"
    never_html = (f'<p class="muted note" data-i18n-template="never_published" data-n="{never}">{never} repositories have never published a release</p>' if never else "")
    return (f'<ul class="time-list" data-testid="{prefix}latest-releases">{latest_html}</ul>',
            f'<ul class="time-list" data-testid="{prefix}oldest-releases">{old_html}</ul>{never_html}')


def red_ci_list(data: AppData, names: set[str] | None) -> str:
    if not data.activity:
        return ""
    red = sorted(n for n, a in data.activity.items() if a.ci == "failure" and n in data.ecosystem_by_name and (names is None or n in names))
    if not red:
        return '<p class="muted note ok-note" data-i18n="ci_all_green" data-testid="ci-red-none">No repository has a red CI.</p>'
    links = "".join(f'<li><a href="{esc(data.repo_url + n)}/actions" target="_blank" rel="noopener noreferrer">{esc(n)}</a></li>' for n in red)
    return f'<div class="red-ci" data-testid="ci-red"><span class="card-subtitle" data-i18n="ci_red_title">Repositories with a red CI</span><ul class="chip-list">{links}</ul></div>'


def errors_card(data: AppData) -> str:
    """The indicator of errors / unknown: the reconciled count and, when it is not zero, a dropdown with each repository and its reason."""
    # Nothing listed is not "all good": with no project at all the indicator stays neutral and says there is no data.
    state = "bad" if data.errors else ("ok" if data.total else "none")
    hint = ('<span data-i18n="errors_card_hint">Open the detail: each repository and the reason.</span>' if data.errors
            else '<span data-i18n="errors_none_card">Nothing is missing or unknown</span>' if data.total
            else '<span data-i18n="no_data">No data</span>')
    face = (f'<span class="kpi-number" id="health-errors">{data.errors}</span>'
            f'<span class="kpi-label"><b data-i18n="health_errors">Errors / unknown</b><small>{hint}</small></span>')
    if not data.issues:
        return f'<div class="kpi kpi-{state} kpi-errors" data-testid="kpi-errors">{face}</div>'
    items = "".join(
        f'<li><code>{esc(getattr(issue, "repo", ""))}</code> <span class="integrity-kind" data-i18n="integrity_kind_{esc(getattr(issue, "kind", ""))}">{esc(getattr(issue, "kind", ""))}</span>'
        f' <span class="integrity-detail">{esc(getattr(issue, "detail", ""))}</span></li>' for issue in data.issues)
    return (f'<details class="kpi kpi-{state} kpi-errors kpi-drop" data-testid="kpi-errors"><summary>{face}</summary>'
            f'<div class="kpi-drop-panel"><ul class="integrity-list">{items}</ul>'
            f'<button type="button" class="btn btn-ghost" data-goto-tab="errors" data-i18n="tab_errors">Errors / unknown</button></div></details>')


# ---------------------------------------------------------------------------
# Panels
# ---------------------------------------------------------------------------

def summary_panel(data: AppData, ecosystem_cards_html: str) -> str:
    cards = "".join(progress_card(data, key, label) for key, label in ECOSYSTEMS)
    latest, oldest = releases_lists(data, None, 7)
    # Green only when every listed project resolved its version; red when none did; neutral otherwise (and with nothing listed).
    resolved_state = "none" if not data.total else ("ok" if data.ok == data.total else "bad" if data.ok == 0 else "mid")
    kpis = (
        f'<div class="kpi" data-testid="kpi-total"><span class="kpi-number" id="health-total">{data.total}</span><span class="kpi-label"><b data-i18n="health_total">Total projects</b></span></div>'
        f'<div class="kpi kpi-{resolved_state}" data-testid="kpi-resolved"><span class="kpi-number" id="health-resolved">{data.ok}</span><span class="kpi-label"><b data-i18n="health_resolved">Version resolved</b></span></div>'
        f'{errors_card(data)}'
        f'<div class="kpi" data-testid="kpi-percent"><span class="kpi-number" id="health-percent">{esc(data.success_percent_text)}</span><span class="kpi-label"><b data-i18n="health_registry">Registry health</b></span></div>'
    )
    return f"""
    <div class="summary-grid">
      <section class="kpi-strip" aria-label="Key figures">{kpis}</section>
      <section class="card card-eco-counts" aria-labelledby="eco-counts-t">
        <h2 class="card-title" id="eco-counts-t" data-i18n="section_by_ecosystem">Projects by ecosystem</h2>
        <div class="eco-counts">{ecosystem_cards_html}</div>
      </section>
      <section class="card card-progress" aria-labelledby="progress-t">
        <header class="card-head"><h2 class="card-title" id="progress-t" data-i18n="sum_progress_title">Progress and status by ecosystem</h2>
          <span class="muted" data-i18n="sum_progress_hint">Same figures as the README.</span></header>
        <div class="eco-grid">{cards}</div>
      </section>
      <section class="card card-ci" aria-label="CI">
        {ci_figure(data, ECOSYSTEMS)}
        {red_ci_list(data, None)}
        {months_figure(data, None)}
      </section>
      <section class="card card-maturity">{stacked_figure("maturity", data, ECOSYSTEMS)}</section>
      <section class="card card-evidence">{stacked_figure("evidence", data, ECOSYSTEMS)}</section>
      <section class="card card-releases"><h2 class="card-title" data-i18n="sum_releases_title">Latest releases</h2>{latest}</section>
      <section class="card card-oldest"><h2 class="card-title" data-i18n="sum_oldest_title">Longest without a release</h2>{oldest}</section>
    </div>
    """


def ecosystem_panel(data: AppData, eco: str, label: str, extra_html: str = "") -> str:
    names = _names_of(data, eco)
    one = ((eco, label),)
    latest, oldest = releases_lists(data, names, 8, prefix=f"{eco}-")
    return f"""
    <div class="eco-panel eco-{esc(eco)}">
      <section class="card card-eco-main">
        <header class="card-head"><div><h2 class="card-title">{esc(label)}</h2><p class="muted" data-i18n="eco_intro_{esc(eco)}">{esc(dashboard_app_texts.TEXTS["en"].get("eco_intro_" + eco, ""))}</p></div>
          <button type="button" class="btn" data-show-eco="{esc(eco)}" data-testid="show-projects-{esc(eco)}" data-i18n="eco_view_projects">View the projects of this ecosystem</button></header>
        {progress_card(data, eco, label, big=True, link_tab=False)}
      </section>
      <section class="card">{stacked_figure("maturity", data, one)}</section>
      <section class="card">{stacked_figure("evidence", data, one)}</section>
      <section class="card">{ci_figure(data, one)}{red_ci_list(data, names)}</section>
      <section class="card"><h2 class="card-title" data-i18n="sum_releases_title">Latest releases</h2>{latest}</section>
      <section class="card"><h2 class="card-title" data-i18n="sum_oldest_title">Longest without a release</h2>{oldest}</section>
      {extra_html}
    </div>
    """


def errors_panel(data: AppData, integrity_html: str) -> str:
    rows = "".join(f'<li><code>{esc(name)}</code> <span class="integrity-detail">{esc(reason)}</span></li>' for name, reason in data.unresolved)
    unresolved = (f'<details class="integrity bad" open><summary><span data-i18n="th_status">Status</span> · <span data-i18n="health_errors">Errors / unknown</span> '
                  f'<span class="integrity-count">{len(data.unresolved)}</span></summary><ul class="integrity-list">{rows}</ul></details>' if rows else "")
    return f'<div class="errors-panel" data-testid="errors-panel">{integrity_html.replace("<details class=", "<details open class=", 1)}{unresolved}</div>'


def sidebar(maturity_keys: Sequence[tuple[str, str, int]], roles: Sequence[tuple[str, str, int]], deploys: Sequence[tuple[str, str, int]],
            eco_counts: Mapping[str, int], family_options: str) -> str:
    """The search and the filters shared by every tab. Each chip is a toggle button that carries data-filter-<kind>."""
    def chips(kind: str, items: Sequence[tuple[str, str, int]], i18n_prefix: str) -> str:
        return "".join(
            f'<button type="button" class="chip" data-filter-{kind}="{esc(key)}" aria-pressed="false" data-testid="filter-{kind}-{esc(key)}">'
            f'<span data-i18n="{i18n_prefix}{esc(key)}">{esc(label)}</span><b>{count}</b></button>' for key, label, count in items)

    eco_chips = "".join(
        f'<button type="button" class="chip" data-filter-eco="{esc(key)}" aria-pressed="false" data-testid="filter-eco-{esc(key)}"><span>{esc(label)}</span><b>{eco_counts.get(key, 0)}</b></button>'
        for key, label in ECOSYSTEM_FILTERS)
    return f"""
    <aside class="sidebar" aria-labelledby="filters-t">
      <button type="button" class="filters-toggle" id="filters-toggle" aria-expanded="false" aria-controls="filters-body"><span id="filters-t" data-i18n="filters_title">Search and filters</span><span aria-hidden="true">▾</span></button>
      <div class="filters-body" id="filters-body">
        <div class="side-search">
          <input id="project-search" type="search" placeholder="Search project, description, stack or deployment..." autocomplete="off" aria-label="Search projects"
                 data-i18n-placeholder="search_placeholder" data-i18n-aria-label="search_aria" data-testid="project-search">
        </div>
        <div class="side-group" role="group" aria-labelledby="fg-status"><h2 id="fg-status" data-i18n="filter_status_title">Status</h2>
          <div class="chip-row">
            <button type="button" class="chip" data-filter-status="ok" aria-pressed="false" data-i18n="filter_ok" data-testid="filter-status-ok">✓ OK</button>
            <button type="button" class="chip" data-filter-status="error" aria-pressed="false" data-i18n="filter_error" data-testid="filter-status-error">⚠ Errors</button>
          </div></div>
        <div class="side-group" role="group" aria-labelledby="fg-eco"><h2 id="fg-eco" data-i18n="filter_ecosystem">Ecosystem</h2><div class="chip-row">{eco_chips}</div></div>
        <div class="side-group" role="group" aria-labelledby="fg-mat"><h2 id="fg-mat" data-i18n="filter_maturity">Maturity</h2><div class="chip-row">{chips("maturity", maturity_keys, "maturity_")}</div></div>
        <div class="side-group" role="group" aria-labelledby="fg-type"><h2 id="fg-type" data-i18n="filter_type">Type</h2><div class="chip-row">{chips("role", roles, "role_")}</div></div>
        <div class="side-group" role="group" aria-labelledby="fg-target"><h2 id="fg-target" data-i18n="filter_target">Deploy target</h2><div class="chip-row">{chips("deploy", deploys, "deploy_")}</div></div>
        <div class="side-group family-filter"><label for="family-select" data-i18n="family_label">Family:</label>
          <select id="family-select" data-testid="filter-family"><option value="all" data-i18n="family_all">All families</option>{family_options}</select></div>
        <div class="side-foot">
          <p class="matches" id="filters-count" aria-live="polite" data-i18n-template="filters_matches" data-shown="" data-total=""></p>
          <button id="reset-filters" class="btn btn-ghost" type="button" data-i18n="reset_filters" title="Clear the search box and every active filter (status, deploy, maturity, role, family)"
                  data-i18n-title="reset_filters_title" data-testid="reset-filters">⟲ Reset</button>
          <button type="button" class="btn" data-goto-tab="projects" data-i18n="filters_show" data-testid="show-projects">Show the projects</button>
        </div>
      </div>
    </aside>
    """


def tab_list() -> str:
    buttons = []
    for ident, key, literal in TABS:
        text = f'<span data-i18n="{key}">{ENGLISH[key]}</span>' if key else f"<span>{esc(literal)}</span>"
        accent = f" tab-eco tab-{ident}" if not key else ""
        buttons.append(
            f'<button type="button" role="tab" class="tab{accent}" id="tab-{ident}" aria-controls="panel-{ident}" aria-selected="false" tabindex="-1" '
            f'data-tab="{ident}" data-testid="tab-{ident}">{text}</button>'
        )
    return f'<nav class="tabs" aria-label="Dashboard sections" data-i18n-aria-label="tabs_label"><div role="tablist" aria-orientation="horizontal" id="tablist">{"".join(buttons)}</div></nav>'


def panel(ident: str, inner: str) -> str:
    return (f'<section role="tabpanel" class="panel" id="panel-{ident}" aria-labelledby="tab-{ident}" tabindex="0" hidden data-testid="panel-{ident}">'
            f'<div class="panel-inner">{inner}</div></section>')


# ---------------------------------------------------------------------------
# Style sheet and script (plain strings; placed into the page unchanged)
# ---------------------------------------------------------------------------

CSS = r"""
  /* ======================= Application shell ======================= */
  :root {
    --c-hydra-umc: #4ea1ff; --c-urtc: #b48cff; --c-armor: #34d399; --c-eh3d: #fbbf24; --c-electro-hobby-3d: #94a3b8;
    --panel: var(--surface); --panel-2: var(--surface-2); --radius: 12px;
    --m-scaffolding: #f59e0b; --m-functional: #38bdf8; --m-established: #34d399; --m-production: #a78bfa; --m-unknown: #94a3b8;
    --e-none: #64748b; --e-host-test: #38bdf8; --e-simulator: #818cf8; --e-bench: #fbbf24; --e-field: #34d399; --e-unknown: #94a3b8;
    --k-success: #34d399; --k-failure: #f87171; --k-pending: #fbbf24; --k-none: #64748b;
    --ink-on-fill: #0b0e14; --focus: #fbbf24;
  }
  :root[data-theme="light"] {
    --c-hydra-umc: #1d6fd6; --c-urtc: #7c4dd6; --c-armor: #0f8f68; --c-eh3d: #b45f06; --c-electro-hobby-3d: #566176;
    --m-scaffolding: #f59e0b; --m-functional: #38bdf8; --m-established: #34d399; --m-production: #a78bfa;
    --focus: #1d4ed8;
    /* Darker accent, error and ok colours: the palette of the base page does not reach 4.5:1 for text on the light surfaces. */
    --accent: #1d4ed8; --err: #b91c1c; --ok: #166534; --dim: #4b5563;
  }
  /* A link inside a sentence must be told apart from the text without relying on colour alone. */
  .app-footer a, .subtitle a, .detail-text a, .relationship-note a { text-decoration: underline; text-underline-offset: 2px; }
  html, body { height: 100%; }
  body { margin: 0; }
  .skip-link { position: absolute; left: 8px; top: -48px; background: var(--accent); color: #fff; padding: 8px 12px; border-radius: 8px; z-index: 50; }
  .skip-link:focus { top: 8px; }
  .sr-only { position: absolute !important; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
  :focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; border-radius: 6px; }
  .app { display: grid; grid-template-columns: 272px minmax(0, 1fr); grid-template-rows: auto minmax(0, 1fr) auto; height: 100vh; height: 100dvh; overflow: hidden;
         grid-template-areas: "top top" "side main" "foot foot"; }
  .topbar { grid-area: top; display: flex; align-items: center; gap: 18px; padding: 8px 18px; background: var(--panel); border-bottom: 1px solid var(--border); min-width: 0; }
  .brand { display: flex; flex-direction: column; flex: 0 0 auto; line-height: 1.15; }
  .brand .eyebrow { margin: 0; font-size: 10px; letter-spacing: .22em; color: var(--dim); font-weight: 600; }
  .brand h1 { margin: 2px 0 0; font-size: 17px; display: flex; gap: 8px; align-items: center; white-space: nowrap; }
  .brand .version-pill { font-size: 10px; }
  .tabs { flex: 1 1 auto; min-width: 0; overflow-x: auto; scrollbar-width: thin; }
  [role="tablist"] { display: flex; gap: 4px; width: max-content; }
  .tab { appearance: none; background: transparent; border: 1px solid transparent; color: var(--dim); padding: 8px 14px; border-radius: 9px; cursor: pointer; font-weight: 600; font-size: 13px; white-space: nowrap; position: relative; }
  .tab:hover { color: var(--text); background: var(--panel-2); }
  .tab[aria-selected="true"] { color: var(--text); background: var(--panel-2); border-color: var(--border-strong); box-shadow: inset 0 -3px 0 var(--accent); }
  .tab-eco[aria-selected="true"] { box-shadow: inset 0 -3px 0 var(--tab-color, var(--accent)); }
  .tab-hydra-umc { --tab-color: var(--c-hydra-umc); } .tab-urtc { --tab-color: var(--c-urtc); } .tab-armor { --tab-color: var(--c-armor); } .tab-eh3d { --tab-color: var(--c-eh3d); }
  .tab-eco::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--tab-color); margin-right: 7px; }
  .top-actions { display: flex; align-items: center; gap: 10px; flex: 0 0 auto; }
  .top-actions .freshness-indicator { margin: 0; font-size: 11px; max-width: 260px; }
  .top-actions img { display: block; height: 20px; }
  .lang-select { background: var(--panel-2); color: var(--text); border: 1px solid var(--border-strong); border-radius: 8px; padding: 6px 8px; }
  .sidebar { grid-area: side; border-right: 1px solid var(--border); background: var(--panel); overflow-y: auto; min-height: 0; padding: 14px 14px 18px; }
  .filters-toggle { display: none; }
  .side-search input { width: 100%; font-size: 13px; padding: 10px 12px; border-radius: 9px; border: 1px solid var(--border-strong); background: var(--bg); color: var(--text); }
  .side-group { margin-top: 14px; }
  .side-group h2 { font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); margin: 0 0 6px; font-weight: 700; }
  .chip-row { display: flex; flex-wrap: wrap; gap: 5px; }
  .chip { appearance: none; display: inline-flex; gap: 6px; align-items: center; padding: 4px 9px; border-radius: 999px; border: 1px solid var(--border-strong); background: var(--bg); color: var(--text); cursor: pointer; font-size: 12px; }
  .chip b { font-weight: 600; color: var(--dim); font-variant-numeric: tabular-nums; }
  .chip:hover { border-color: var(--accent); }
  .chip[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: #fff; }
  .chip[aria-pressed="true"] b { color: #fff; }
  :root[data-theme="dark"] .chip[aria-pressed="true"], :root:not([data-theme="light"]) .chip[aria-pressed="true"] { color: #08111f; }
  :root[data-theme="dark"] .chip[aria-pressed="true"] b, :root:not([data-theme="light"]) .chip[aria-pressed="true"] b { color: #08111f; }
  .family-filter { display: flex; flex-direction: column; gap: 5px; }
  .family-filter label { font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); font-weight: 700; }
  .family-filter select { background: var(--bg); color: var(--text); border: 1px solid var(--border-strong); border-radius: 8px; padding: 7px; width: 100%; }
  .side-foot { margin-top: 16px; display: flex; flex-direction: column; gap: 8px; position: sticky; bottom: -18px; background: var(--panel); padding: 8px 0 18px; border-top: 1px solid var(--border); }
  .matches { margin: 0; font-size: 12px; color: var(--dim); }
  .btn { appearance: none; border: 1px solid var(--accent); background: var(--accent); color: #fff; padding: 8px 12px; border-radius: 9px; cursor: pointer; font-weight: 600; font-size: 12.5px; }
  :root[data-theme="dark"] .btn, :root:not([data-theme="light"]) .btn { color: #08111f; }
  .btn-ghost { background: transparent; color: var(--text) !important; border-color: var(--border-strong); }
  .btn:disabled { opacity: .45; cursor: default; }
  .link-btn { appearance: none; background: none; border: 0; padding: 0; color: inherit; font: inherit; cursor: pointer; text-decoration: underline; text-decoration-color: var(--border-strong); text-underline-offset: 3px; }
  main.content { grid-area: main; min-width: 0; min-height: 0; position: relative; }
  .panel { height: 100%; overflow-y: auto; overflow-x: hidden; padding: 16px 20px 20px; scrollbar-width: thin; }
  .panel[hidden] { display: none; }
  .panel-inner { max-width: 1760px; margin: 0 auto; }
  .app-footer { grid-area: foot; border-top: 1px solid var(--border); background: var(--panel); padding: 5px 18px; font-size: 11px; color: var(--dim); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .app-footer a { color: var(--accent); }
  .app-footer .freshness-indicator { display: inline-flex; gap: 6px; margin: 0; font-size: 11px; }

  .card { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; min-width: 0; box-shadow: var(--shadow); }
  .card-title { font-size: 13px; font-weight: 700; margin: 0 0 8px; letter-spacing: .02em; display: block; }
  .card-subtitle { font-size: 11px; color: var(--dim); font-weight: 700; text-transform: uppercase; letter-spacing: .1em; }
  .card-head { display: flex; justify-content: space-between; gap: 14px; align-items: baseline; flex-wrap: wrap; margin-bottom: 8px; }
  .card-head .card-title { margin: 0; font-size: 14px; }
  .muted { color: var(--dim); font-size: 12px; margin: 0; }
  .note { margin-top: 8px; }
  .no-data { color: var(--dim); font-style: italic; margin: 6px 0; font-size: 12.5px; }

  .summary-grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; }
  .kpi-strip { grid-column: span 7; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
  .card-eco-counts { grid-column: span 5; padding: 10px 14px; }
  .card-eco-counts .card-title { margin-bottom: 6px; }
  .eco-counts { display: flex; gap: 10px; flex-wrap: wrap; }
  .eco-counts .health-card { flex: 1 1 90px; padding: 6px 10px; text-align: left; box-shadow: none; }
  .eco-counts .health-card .number { font-size: 22px; }
  .eco-counts .health-card .label { font-size: 11px; }
  .card-progress { grid-column: span 8; }
  .card-ci { grid-column: span 4; display: flex; flex-direction: column; gap: 6px; }
  .card-maturity, .card-evidence { grid-column: span 3; }
  .card-releases, .card-oldest { grid-column: span 3; }
  .kpi { display: flex; align-items: center; gap: 12px; padding: 12px 14px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; color: var(--text); box-shadow: var(--shadow); min-width: 0; }
  .kpi-number { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 28px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .kpi-label { display: flex; flex-direction: column; font-size: 12px; min-width: 0; }
  .kpi-label small { color: var(--dim); font-size: 11px; line-height: 1.25; }
  .kpi-ok .kpi-number { color: var(--ok); }
  .kpi-bad { border-color: var(--err); background: var(--err-soft); }
  .kpi-bad .kpi-number { color: var(--err); }
  a.kpi:hover { border-color: var(--accent); }
  .kpi-drop { display: block; position: relative; padding: 0; }
  .kpi-drop > summary { display: flex; align-items: center; gap: 12px; padding: 12px 14px; cursor: pointer; list-style: none; }
  .kpi-drop > summary::-webkit-details-marker { display: none; }
  .kpi-drop-panel { position: absolute; z-index: 30; left: 0; top: calc(100% + 6px); width: min(720px, 90vw); max-height: 60vh; overflow: auto; background: var(--panel); border: 1px solid var(--err); border-radius: var(--radius); padding: 12px 14px; box-shadow: var(--shadow); display: grid; gap: 10px; }
  tr.ecosystem-banner-row.hidden { display: none; }
  .eco-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
  .eco-card { border: 1px solid var(--border); border-top: 3px solid var(--eco-color, var(--accent)); border-radius: 10px; padding: 10px 12px; background: var(--bg); min-width: 0; }
  .eco-hydra-umc { --eco-color: var(--c-hydra-umc); } .eco-urtc { --eco-color: var(--c-urtc); } .eco-armor { --eco-color: var(--c-armor); } .eco-eh3d { --eco-color: var(--c-eh3d); }
  .eco-head { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
  .eco-title { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .eco-title h3 { margin: 0; font-size: 15px; }
  .ring-wrap { width: 84px; flex: 0 0 84px; }
    .ring-wrap .chart-ring { width: 100%; height: auto; display: block; }
  .areas { list-style: none; margin: 0; padding: 0; display: grid; gap: 5px; }
  .area { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "name num" "bar bar"; align-items: end; gap: 3px 8px; font-size: 12.5px; }
  .area-name { grid-area: name; display: flex; gap: 6px; align-items: center; min-width: 0; }
  .area-glyph { color: var(--eco-color, var(--accent)); width: 1em; flex: 0 0 auto; }
  .area-bar { grid-area: bar; height: 7px; border-radius: 5px; background: var(--border); overflow: hidden; display: block; }
  .area-fill { display: block; height: 100%; background: var(--eco-color, var(--accent)); border-radius: 5px; }
  .area-bad .area-fill { background: var(--err); } .area-poor .area-fill { background: #f97316; } .area-fair .area-fill { background: #eab308; } .area-good .area-fill { background: var(--ok); }
  .area-num { grid-area: num; text-align: right; font-variant-numeric: tabular-nums; display: flex; gap: 6px; align-items: baseline; }
  .area-num small { color: var(--dim); font-size: 10.5px; }
  .areas { gap: 7px; }
  .areas-big { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 28px !important; }
  .areas-big .area { font-size: 14px; }
  .areas-big .area-bar { height: 11px; }

  .chart-figure { margin: 0; }
  .chart { width: 100%; height: auto; display: block; overflow: visible; }
  .chart-label { fill: var(--text); font-size: 12px; font-family: "IBM Plex Sans", system-ui, sans-serif; }
  .chart-total { fill: var(--dim); font-size: 12px; font-variant-numeric: tabular-nums; }
  .chart-track { fill: var(--border); opacity: .55; }
  .chart-axis { stroke: var(--border-strong); stroke-width: 1; }
  .seg { stroke: var(--panel); stroke-width: 1.5; }
  .seg-count { fill: var(--ink-on-fill); font-size: 11.5px; font-weight: 700; font-family: "IBM Plex Mono", monospace; }
  .seg-mat-scaffolding, .sw-mat-scaffolding { fill: var(--m-scaffolding); background: var(--m-scaffolding); }
  .seg-mat-functional, .sw-mat-functional { fill: var(--m-functional); background: var(--m-functional); }
  .seg-mat-established, .sw-mat-established { fill: var(--m-established); background: var(--m-established); }
  .seg-mat-production, .sw-mat-production { fill: var(--m-production); background: var(--m-production); }
  .seg-mat-unknown, .sw-mat-unknown, .seg-ev-unknown, .sw-ev-unknown { fill: var(--m-unknown); background: var(--m-unknown); }
  .seg-ev-none, .sw-ev-none { fill: var(--e-none); background: var(--e-none); }
  .seg-ev-host-test, .sw-ev-host-test { fill: var(--e-host-test); background: var(--e-host-test); }
  .seg-ev-simulator, .sw-ev-simulator { fill: var(--e-simulator); background: var(--e-simulator); }
  .seg-ev-bench, .sw-ev-bench { fill: var(--e-bench); background: var(--e-bench); }
  .seg-ev-field, .sw-ev-field { fill: var(--e-field); background: var(--e-field); }
  .seg-ci-success, .sw-ci-success { fill: var(--k-success); background: var(--k-success); }
  .seg-ci-failure, .sw-ci-failure { fill: var(--k-failure); background: var(--k-failure); }
  .seg-ci-pending, .sw-ci-pending { fill: var(--k-pending); background: var(--k-pending); }
  .seg-ci-none, .sw-ci-none { fill: var(--k-none); background: var(--k-none); }
  .seg-count-ev-none, .seg-count-ci-none { fill: #fff; }
  .seg-ev-unknown, .seg-mat-unknown, .sw-mat-unknown, .sw-ev-unknown { background-image: repeating-linear-gradient(45deg, rgba(0,0,0,.35) 0 2px, transparent 2px 6px); }
  .col { fill: var(--accent); } .col-value { fill: var(--text); font-size: 12px; font-weight: 700; font-family: "IBM Plex Mono", monospace; }
  .ring-track { stroke: var(--border); } .ring-value { stroke: var(--eco-color, var(--accent)); } .ring-text { fill: var(--text); font-size: 25px; font-weight: 700; font-family: "IBM Plex Mono", monospace; }
  .legend { list-style: none; margin: 8px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 11px; color: var(--dim); }
  .legend li { display: inline-flex; gap: 5px; align-items: center; }
  .swatch { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
  .time-list { list-style: none; padding: 0; margin: 0; font-size: 12.5px; }
  .time-list li { display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 8px; padding: 5px 0; border-bottom: 1px dashed var(--border); align-items: baseline; }
  .time-list li:last-child { border-bottom: 0; }
  .time-list a { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .time-list time, .time-list .age { color: var(--dim); font-variant-numeric: tabular-nums; font-size: 11.5px; }
  .time-list .tag { font-family: "IBM Plex Mono", monospace; font-size: 11px; color: var(--text); background: var(--panel-2); border: 1px solid var(--border); border-radius: 6px; padding: 0 5px; margin-left: 6px; }
  .time-list li { grid-template-columns: minmax(0, 1fr) auto auto auto; }
  .chip-list { list-style: none; padding: 0; margin: 6px 0 0; display: flex; gap: 6px; flex-wrap: wrap; }
  .chip-list a { display: inline-block; padding: 2px 9px; border-radius: 999px; border: 1px solid var(--err); color: var(--err); font-size: 12px; text-decoration: none; }
  .red-ci .chip-list a::before { content: "✕ "; }
  .ok-note { color: var(--ok); }

  .eco-panel { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; }
  .eco-panel > .card-eco-main { grid-column: span 12; }
  .eco-panel > .card:nth-of-type(2), .eco-panel > .card:nth-of-type(3) { grid-column: span 6; }
  .eco-panel > .card:nth-of-type(4) { grid-column: span 6; }
  .eco-panel > .card:nth-of-type(5), .eco-panel > .card:nth-of-type(6) { grid-column: span 3; }
  .card-eco-main .eco-card { border: 0; background: transparent; padding: 0; display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 20px; align-items: start; }
  .card-eco-main .eco-head { flex-direction: column; align-items: flex-start; }
  .card-eco-main .ring-wrap { width: 140px; flex-basis: 140px; }
  .arch-switch { display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap; }
  .arch-switch .chip[aria-pressed="true"] { background: var(--accent); }
  .arch-panel[hidden] { display: none; }
  .errors-panel { max-width: 1100px; display: grid; gap: 14px; }
  .evidence-split { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
  .inv-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; align-items: start; }
  .inv-grid .span-2 { grid-column: span 2; }
  .inv-grid > *, .evidence-split > * { min-width: 0; }
  .panel .compat-matrix-wrapper { overflow-x: auto; max-width: 100%; }
  .panel-inner { min-width: 0; }
  .panel .section { margin: 0 0 16px; }
  .panel .section:last-child { margin-bottom: 0; }
  .panel .section, .panel .table-wrapper { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; }
  .panel .table-wrapper { padding: 0; overflow: auto; max-height: 100%; }
  .panel .table-wrapper table thead th { position: sticky; top: 0; z-index: 2; background: var(--panel-2); }
  #panel-projects .panel-inner { height: 100%; max-width: none; }
  #panel-projects { padding-bottom: 12px; }
  .empty { padding: 20px; text-align: center; color: var(--dim); }

  /* ---- laptop: the tabs go to their own row and the summary is two columns wide ---- */
  @media (max-width: 1500px) {
    .topbar { flex-wrap: wrap; row-gap: 4px; padding-bottom: 4px; }
    .tabs { order: 3; flex: 1 1 100%; }
    .top-actions { margin-left: auto; }
    .kpi-strip, .card-eco-counts, .card-progress, .card-ci { grid-column: span 12; }
    .card-maturity, .card-evidence, .card-releases, .card-oldest { grid-column: span 6; }
    .card-ci { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px 24px; }
    .card-ci > .chart-figure:first-child { grid-column: 1; }
    .eco-counts .health-card { flex: 1 1 140px; }
  }
  /* ---- tablet and phone: one column, the page scrolls, tabs scroll sideways ---- */
  @media (max-width: 1100px) {
    .summary-grid > *, .eco-panel > * { grid-column: span 12 !important; }
    .kpi-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .eco-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .evidence-split, .inv-grid { grid-template-columns: 1fr; }
    .inv-grid .span-2 { grid-column: auto; }
  }
  @media (max-width: 960px) {
    html, body { height: auto; }
    .app { display: block; height: auto; overflow: visible; }
    .topbar { position: sticky; top: 0; z-index: 20; flex-wrap: wrap; gap: 8px 12px; padding: 8px 12px; }
    .tabs { order: 3; flex: 1 1 100%; }
    .top-actions { margin-left: auto; flex-wrap: wrap; max-width: 100%; }
    .top-actions .lang-select { max-width: 150px; }
    .top-actions .freshness-indicator { display: none; }
    .brand h1 { font-size: 15px; }
    .sidebar { border-right: 0; border-bottom: 1px solid var(--border); padding: 8px 12px; overflow: visible; }
    .filters-toggle { display: flex; width: 100%; justify-content: space-between; background: var(--bg); color: var(--text); border: 1px solid var(--border-strong); border-radius: 9px; padding: 9px 12px; font-weight: 600; }
    .filters-body { display: none; padding-top: 6px; }
    .filters-body.open { display: block; }
    .panel { height: auto; overflow: visible; padding: 12px; }
    #panel-projects .panel-inner { height: auto; }
    .panel .table-wrapper { max-height: none; overflow-x: auto; }
    .app-footer { white-space: normal; padding: 10px 12px; }
    .eco-grid, .kpi-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .card-ci { display: flex; }
    .card-eco-main .eco-card { grid-template-columns: 1fr; }
  }
  @media (max-width: 560px) {
    .eco-grid { grid-template-columns: 1fr; }
    .kpi-number { font-size: 22px; }
  }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; scroll-behavior: auto !important; } }
"""

JS_FILTERS = r"""
  // ---------------- Filters (search, status, ecosystem, maturity, type, target, family) ----------------
  const rows = Array.from(document.querySelectorAll(".project-row"));
  const familyHeaderRows = Array.from(document.querySelectorAll(".family-header-row"));
  const bannerRows = Array.from(document.querySelectorAll(".ecosystem-banner-row"));
  const searchInput = document.getElementById("project-search");
  const emptyResults = document.getElementById("empty-results");
  const familySelect = document.getElementById("family-select");
  const resetFiltersBtn = document.getElementById("reset-filters");
  const healthTotal = document.getElementById("health-total");
  const healthResolved = document.getElementById("health-resolved");
  const healthPercent = document.getElementById("health-percent");
  const countLabel = document.getElementById("filters-count");

  const FILTER_KINDS = ["status", "eco", "maturity", "role", "deploy"];
  const state = { status: "all", eco: "all", maturity: "all", role: "all", deploy: "all" };
  const ROW_FIELD = { status: "status", eco: "ecosystem", maturity: "maturity", role: "role", deploy: "deploy" };

  function syncButtons(kind) {
    document.querySelectorAll("[data-filter-" + kind + "]").forEach(function (button) {
      const on = button.getAttribute("data-filter-" + kind) === state[kind];
      button.classList.toggle("active", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function currentDict() { return I18N[document.documentElement.lang] || I18N.en; }

  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();
    const activeFamily = familySelect ? familySelect.value : "all";
    let visible = 0;
    let visibleOk = 0;
    const visibleFamilies = {};
    const visibleEcosystems = {};

    rows.forEach(function (row) {
      const name = row.dataset.name || "";
      const status = row.dataset.status || "";
      const deploy = row.dataset.deploy || "";
      const stack = row.dataset.stack || "";
      const family = row.dataset.family || "";
      const notes = row.dataset.notes || "";
      let show = !query || name.includes(query) || stack.includes(query) || deploy.includes(query) || family.includes(query) || notes.includes(query);
      FILTER_KINDS.forEach(function (kind) {
        if (state[kind] !== "all" && (row.dataset[ROW_FIELD[kind]] || "") !== state[kind]) { show = false; }
      });
      if (activeFamily !== "all" && family !== activeFamily) { show = false; }

      row.classList.toggle("hidden", !show);
      if (!show) {
        const toggle = row.querySelector(".details-toggle");
        const targetId = toggle && toggle.dataset.detailsTarget;
        const target = targetId && document.getElementById(targetId);
        if (target) { target.hidden = true; }
        if (toggle) { toggle.setAttribute("aria-expanded", "false"); toggle.textContent = "▸"; }
      } else {
        visible += 1;
        if (status === "ok") { visibleOk += 1; }
        if (family) { visibleFamilies[(row.dataset.ecosystem || "") + "|" + family] = true; }
        if (row.dataset.ecosystem) { visibleEcosystems[row.dataset.ecosystem] = true; }
      }
    });

    familyHeaderRows.forEach(function (headerRow) {
      headerRow.classList.toggle("hidden", !visibleFamilies[(headerRow.dataset.ecosystem || "") + "|" + (headerRow.dataset.familyHeader || "")]);
    });
    bannerRows.forEach(function (banner) {
      banner.classList.toggle("hidden", !visibleEcosystems[banner.dataset.ecosystemBanner || ""]);
    });
    emptyResults.style.display = visible === 0 ? "block" : "none";

    const visiblePercent = visible ? Math.round((visibleOk / visible) * 1000) / 10 : 0;
    if (healthTotal) { healthTotal.textContent = String(visible); }
    if (healthResolved) { healthResolved.textContent = String(visibleOk); }
    if (healthPercent) { healthPercent.textContent = String(visiblePercent) + "%"; }
    if (countLabel) {
      countLabel.setAttribute("data-shown", String(visible));
      countLabel.setAttribute("data-total", String(rows.length));
      countLabel.textContent = fillTemplate(currentDict().filters_matches || "{shown} / {total}", countLabel);
    }
    if (resetFiltersBtn) {
      const anyFilterActive = query.length > 0 || activeFamily !== "all" || FILTER_KINDS.some(function (kind) { return state[kind] !== "all"; });
      resetFiltersBtn.disabled = !anyFilterActive;
    }
  }

  function showProjects() { if (typeof activateTab === "function") { activateTab("projects"); } }

  FILTER_KINDS.forEach(function (kind) {
    document.querySelectorAll("[data-filter-" + kind + "]").forEach(function (button) {
      button.addEventListener("click", function () {
        const value = button.getAttribute("data-filter-" + kind);
        state[kind] = state[kind] === value ? "all" : value;
        syncButtons(kind);
        applyFilters();
        showProjects();
      });
    });
  });

  searchInput.addEventListener("input", function () { applyFilters(); if (searchInput.value.trim()) { showProjects(); } });
  if (familySelect) { familySelect.addEventListener("change", function () { applyFilters(); showProjects(); }); }

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener("click", function () {
      searchInput.value = "";
      FILTER_KINDS.forEach(function (kind) { state[kind] = "all"; syncButtons(kind); });
      if (familySelect) { familySelect.value = "all"; }
      applyFilters();
    });
  }

  document.querySelectorAll("[data-show-eco]").forEach(function (button) {
    button.addEventListener("click", function () {
      state.eco = button.dataset.showEco;
      syncButtons("eco");
      applyFilters();
      showProjects();
    });
  });

  const compatButtons = Array.from(document.querySelectorAll("[data-compat-view]"));
  const compatPanels = Array.from(document.querySelectorAll("[data-compat-panel]"));
  compatButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const view = button.dataset.compatView;
      compatButtons.forEach(function (other) { other.classList.toggle("active", other === button); });
      compatPanels.forEach(function (panel) { panel.hidden = panel.dataset.compatPanel !== view; });
    });
  });

  Array.from(document.querySelectorAll(".details-toggle")).forEach(function (button) {
    button.addEventListener("click", function () {
      const target = document.getElementById(button.dataset.detailsTarget);
      if (!target) { return; }
      const nowOpen = target.hidden;
      target.hidden = !nowOpen;
      button.setAttribute("aria-expanded", nowOpen ? "true" : "false");
      button.textContent = nowOpen ? "▾" : "▸";
    });
  });

  FILTER_KINDS.forEach(syncButtons);
  applyFilters();
"""

JS = r"""
  // ---------------- Application shell: tabs, filters, ages ----------------
  const TAB_IDS = __TAB_IDS__;
  const TAB_KEY = "hydra-dashboard-tab";
  const tabs = Array.from(document.querySelectorAll("[role='tab']"));
  const panels = Array.from(document.querySelectorAll("[role='tabpanel']"));

  function safeGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function safeSet(key, value) { try { localStorage.setItem(key, value); } catch (e) { /* storage blocked */ } }

  function activateTab(id, options) {
    options = options || {};
    if (TAB_IDS.indexOf(id) < 0) { id = "summary"; }
    tabs.forEach(function (tab) {
      const on = tab.dataset.tab === id;
      tab.setAttribute("aria-selected", on ? "true" : "false");
      tab.tabIndex = on ? 0 : -1;
      if (on) {
        if (options.focus) { tab.focus(); }
        // Scrolls the tab bar by hand: scrollIntoView() would move the starting point of keyboard navigation to this tab, so the first Tab
        // press of a visitor would skip the skip link and everything before the selected tab.
        const bar = tab.closest("nav");
        if (bar) {
          const t = tab.getBoundingClientRect();
          const b = bar.getBoundingClientRect();
          if (t.left < b.left) { bar.scrollLeft -= b.left - t.left + 12; }
          else if (t.right > b.right) { bar.scrollLeft += t.right - b.right + 12; }
        }
      }
    });
    panels.forEach(function (panel) { panel.hidden = panel.id !== "panel-" + id; });
    safeSet(TAB_KEY, id);
    if (options.updateHash !== false && location.hash !== "#" + id) {
      try { history.replaceState(null, "", "#" + id); } catch (e) { location.hash = id; }
    }
  }

  tabs.forEach(function (tab, index) {
    tab.addEventListener("click", function () { activateTab(tab.dataset.tab); });
    tab.addEventListener("keydown", function (event) {
      let next = null;
      if (event.key === "ArrowRight") { next = (index + 1) % tabs.length; }
      else if (event.key === "ArrowLeft") { next = (index - 1 + tabs.length) % tabs.length; }
      else if (event.key === "Home") { next = 0; }
      else if (event.key === "End") { next = tabs.length - 1; }
      if (next !== null) { event.preventDefault(); activateTab(tabs[next].dataset.tab, { focus: true }); }
    });
  });

  document.querySelectorAll("[data-goto-tab]").forEach(function (el) {
    el.addEventListener("click", function (event) { event.preventDefault(); activateTab(el.dataset.gotoTab); });
  });

  window.addEventListener("hashchange", function () {
    const id = location.hash.replace("#", "");
    if (TAB_IDS.indexOf(id) >= 0) { activateTab(id, { updateHash: false }); }
  });

  const hashId = location.hash.replace("#", "");
  activateTab(TAB_IDS.indexOf(hashId) >= 0 ? hashId : (safeGet(TAB_KEY) || "summary"), { updateHash: TAB_IDS.indexOf(hashId) >= 0 });

  // Architecture switcher
  const archButtons = Array.from(document.querySelectorAll("[data-arch-view]"));
  const archPanels = Array.from(document.querySelectorAll("[data-arch-panel]"));
  archButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      archButtons.forEach(function (other) { other.setAttribute("aria-pressed", other === button ? "true" : "false"); });
      archPanels.forEach(function (panel) { panel.hidden = panel.dataset.archPanel !== button.dataset.archView; });
    });
  });

  // Filters panel on small screens
  const filtersToggle = document.getElementById("filters-toggle");
  const filtersBody = document.getElementById("filters-body");
  if (filtersToggle && filtersBody) {
    filtersToggle.addEventListener("click", function () {
      const open = !filtersBody.classList.contains("open");
      filtersBody.classList.toggle("open", open);
      filtersToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Ages of the dates (computed in the browser so the page itself never changes just because time passes)
  document.querySelectorAll(".age[data-iso]").forEach(function (el) {
    const when = Date.parse(el.dataset.iso);
    if (!isNaN(when)) { el.dataset.n = String(Math.max(0, Math.floor((Date.now() - when) / 86400000))); }
  });
  applyLanguage(langSelect ? langSelect.value : resolveInitialLang());
"""


def script() -> str:
    """The filters and the shell, ready to be placed inside the page's own script."""
    import json
    return JS_FILTERS + JS.replace("__TAB_IDS__", json.dumps(list(TAB_IDS)))


# ---------------------------------------------------------------------------
# EH3D architecture (texts in dashboard_app_texts, English as the fallback written into the page)
# ---------------------------------------------------------------------------

EH3D_CARD_LISTS: tuple[tuple[str, ...], ...] = (
    ("EH3D-COMMON", ".eh3dproj", "SHA-256 integrity", "Shared crates"),
    ("EH3D-CORE-LIBS", "Gerber / Excellon / G-code", "EH3D-DOCS"),
    ("EH3D-ISOCAM", "EH3D-DRILLPRO", "EH3D-ROUTEPRO", "EH3D-MOTIONCNC", "EH3D-GERBERVIEWER"),
    ("EH3D-SERVER", "EH3D-STUDIO", "Simulator / GRBL"),
    ("EH3D-NODE-BUNGARD", "EH3D-NODE-BUNGARD-AUX", "EH3D-NODE-BUNGARD-HMI", "EH3D-NODE-HMI-GUI"),
    ("EH3D-ANDROID-CONTROL", "EH3D-IOS-CONTROL", "EH3D-SUITE-LAUNCHER", "EH3D-UPDATER"),
)


def eh3d_architecture_section() -> str:
    """The architecture of EH3D as the same kind of cards the other ecosystems have; every text is looked up by key so the 8 languages apply."""
    import dashboard_app_texts
    en = dashboard_app_texts.TEXTS["en"]
    cards = []
    for index, items in enumerate(EH3D_CARD_LISTS, start=1):
        lis = "".join(f"<li>{esc(item)}</li>" for item in items)
        cards.append(
            f'<article class="architecture-card"><h3 data-i18n="architecture_e_card{index}_title">{esc(en[f"architecture_e_card{index}_title"])}</h3>'
            f'<p data-i18n="architecture_e_card{index}_body">{esc(en[f"architecture_e_card{index}_body"])}</p><ul>{lis}</ul></article>'
        )
    return (
        '<section class="section"><div role="heading" aria-level="2" class="section-title" data-i18n="architecture_section_e">EH3D: System architecture</div>'
        f'<div class="architecture-grid">{"".join(cards)}</div>'
        '<div class="architecture-flow" aria-label="EH3D flow"><span data-i18n="architecture_e_flow_1">Gerber, Excellon and images</span><b>→</b>'
        '<span data-i18n="architecture_e_flow_2">Parsers and CAM tools</span><b>→</b><span data-i18n="architecture_e_flow_3">G-code and simulation</span><b>→</b>'
        '<span data-i18n="architecture_e_flow_4">Machine</span></div>'
        f'<div class="relationship-note"><strong data-i18n="architecture_e_rel_title">{esc(en["architecture_e_rel_title"])}</strong> '
        f'<span data-i18n="architecture_e_rel_body">{esc(en["architecture_e_rel_body"])}</span></div></section>'
    )
