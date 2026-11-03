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

import json
from dataclasses import dataclass, field
from typing import Mapping, Sequence

import dashboard_app_texts
import dashboard_charts as charts
import dashboard_ci_ui
import dashboard_tests_ui
import dashboard_actions_ui
import dashboard_evo_ui
import dashboard_health
import dashboard_insight_ui
import dashboard_nav_ui
import dashboard_delivery_ui
import dashboard_delivery_texts
import dashboard_robust
import dashboard_robust_texts
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
    ("tests", "tab_tests", ""),
    ("actions", "tab_actions", ""),
    ("insight", "tab_insight", ""),
    ("inventory", "tab_inventory", ""),
    ("rack", "tab_rack", ""),
    ("architecture", "tab_architecture", ""),
    ("errors", "tab_errors", ""),
)
TAB_IDS = tuple(tab[0] for tab in TABS)
ENGLISH = {"tab_summary": "Summary", "tab_projects": "Projects", "tab_evidence": "Evidence", "tab_tests": "Tests", "tab_actions": "Builds", "tab_insight": "Analysis", "tab_inventory": "Inventory", "tab_rack": "Rack",
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
    alerts: Sequence[object] = field(default_factory=list)          # dashboard_health.Alert for what does not depend on today's date
    incomplete: Sequence[str] = field(default_factory=list)         # dashboard_health.completeness codes; empty = the picture is complete
    build: object | None = None                                     # dashboard_health.BuildInfo of the last good build, None = not verified
    page_data: Mapping[str, object] = field(default_factory=dict)  # what the script reads: config, repos, contrib
    manifest: Mapping[str, object] = field(default_factory=dict)   # dashboard_robust.manifest_health: valid, repos, percent (None = not verified)
    generation_html: str = ""                                      # dashboard_robust.generation_html: the figures of the generation
    stale_date: str | None = None                                  # the CI, release and commit data are the last known version of this date
    rack_html: str = ""                                            # dashboard_rack.panel_html


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


def live_ci_note(data: "AppData", eco: str) -> str:
    """The latest run of main of every repository of the ecosystem as this page read it: next to the bar of the README, which was measured earlier."""
    if not data.activity:
        return ""
    names = [n for n, key in data.ecosystem_by_name.items() if key == eco and n in data.activity]
    if not names:
        return ""
    green = sum(1 for n in names if data.activity[n].ci == "success")
    red = sum(1 for n in names if data.activity[n].ci == "failure")
    en = dashboard_delivery_texts.TEXTS["en"]
    title = esc(en["ci_live_title"])
    return (f'<p class="area-live" data-testid="ci-live-{esc(eco)}" title="{title}" data-i18n-title="ci_live_title" data-i18n-template="ci_live_note" '
            f'data-g="{green}" data-n="{len(names)}" data-r="{red}">{esc(en["ci_live_note"].format(g=green, n=len(names), r=red))}</p>')


def meter_rows(areas: Mapping[str, Area] | None, eco_label: str, big: bool = False, ctx: str = "s", live_ci: str = "") -> str:
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
        counts_attr = f' data-a-n="{value.count}" data-a-total="{value.total}"' if value.count is not None else ""
        panel_id = f"contrib-{ctx}-{esc(eco_label)}-{area}"
        rows.append(
            f'<li class="area area-{state}" data-area="{area}" data-testid="area-{esc(eco_label)}-{area}">'
            f'<button type="button" class="area-name area-btn" aria-expanded="false" aria-controls="{panel_id}" data-contrib-eco="{esc(eco_label)}" data-contrib-area="{area}" data-testid="contrib-btn-{esc(eco_label)}-{area}">'
            f'<span class="area-glyph" aria-hidden="true">{LIGHT_GLYPH[state]}</span><span data-i18n="area_{area}">{AREA_ENGLISH[area]}</span><span class="area-caret" aria-hidden="true">▸</span></button>'
            f'<span class="area-bar" role="img" aria-label="{esc(label)}" data-aria="pct" data-a-name-key="area_{area}" data-a-name="{AREA_ENGLISH[area]}" data-a-pct="{value.percent}"{counts_attr}>'
            f'<span class="area-fill" style="width:{value.percent}%"></span></span>'
            f'<span class="area-num"><b>{value.percent}%</b><small>{count}</small></span>'
            f'{live_ci if area == "ci" else ""}'
            f'<div class="contrib" id="{panel_id}" data-testid="contrib-{esc(eco_label)}-{area}" hidden></div></li>'
        )
    return f'<ul class="areas{" areas-big" if big else ""}">{"".join(rows)}</ul>'


def progress_card(data: AppData, eco: str, label: str, big: bool = False, link_tab: bool = True, ctx: str = "s") -> str:
    percent, counted = data.progress.get(eco, (None, None))
    ring = charts.ring_svg(percent, f"ring-{eco}", size=124 if big else 104)
    counted_html = (f'<span class="muted" data-i18n-template="sum_repos_counted" data-n="{counted}">{counted} repositories counted</span>' if counted is not None else "")
    head = f'<button type="button" class="link-btn" data-goto-tab="{esc(eco)}">{esc(label)}</button>' if link_tab else f"<span>{esc(label)}</span>"
    summary = f"{label}: {percent}%" if percent is not None else f"{label}: no data"
    pct_attr = f' data-a-pct="{percent}"' if percent is not None else ""
    panel_id = f"contrib-{ctx}-{esc(eco)}-progress"
    toggle = (f'<button type="button" class="link-btn contrib-toggle" aria-expanded="false" aria-controls="{panel_id}" data-contrib-eco="{esc(eco)}" data-contrib-area="progress" '
              f'data-testid="contrib-btn-{esc(eco)}-progress"><span data-i18n="contrib_repos">Repositories</span><span class="area-caret" aria-hidden="true">▸</span></button>')
    return (
        f'<article class="eco-card eco-{esc(eco)}" data-testid="progress-{esc(eco)}">'
        f'<header class="eco-head"><div class="ring-wrap" role="img" tabindex="0" aria-label="{esc(summary)}" data-aria="pct" data-a-name="{esc(label)}"{pct_attr}>{ring}</div>'
        f'<div class="eco-title"><h3>{head}</h3><span class="muted" data-i18n="sum_overall">overall progress</span>{counted_html}{toggle}</div></header>'
        f'{meter_rows(data.status.get(eco), eco, big, ctx, live_ci_note(data, eco))}'
        f'<div class="contrib contrib-progress" id="{panel_id}" data-testid="contrib-{esc(eco)}-progress" hidden></div></article>'
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
    chart = charts.stacked_bars_svg(rows, all_keys, prefix, i18n_prefix=i18n_prefix, names=labels, **({"width": 780, "label_width": 96} if wide else {}))
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
    chart = charts.stacked_bars_svg(rows, charts.CI_KEYS, "ci", width=780 if len(ecosystems) == 1 else 480, bar_height=22, gap=10, label_width=96 if len(ecosystems) == 1 else 76,
                                    i18n_prefix="ci_", names=CI_LABELS)
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


def registry_card(data: AppData) -> str:
    """Manifest health: valid manifests over repositories (the same problems the Errors / unknown indicator counts), with how it is calculated in a dropdown.
    With no repository, or when no manifest could be read, there is no percentage: it says it is not verified."""
    m = dict(data.manifest)
    valid, repos, percent = int(m.get("valid", 0) or 0), int(m.get("repos", 0) or 0), m.get("percent")
    en = dashboard_robust_texts.TEXTS["en"]
    if percent is None:
        state, number = "none", "–"
        sub = f'<small data-i18n="not_verified">{esc(_en("not_verified"))}</small>'
    else:
        state = "ok" if valid == repos else ("bad" if valid == 0 else "mid")
        number = f"{percent:g}%"
        sub = (f'<small data-i18n-template="registry_sub" data-ok="{valid}" data-repos="{repos}">{esc(en["registry_sub"].replace("{ok}", str(valid)).replace("{repos}", str(repos)))}</small>')
    face = (f'<span class="kpi-number" id="health-percent">{esc(number)}</span>'
            f'<span class="kpi-label"><b data-i18n="health_registry">Registry health</b>{sub}</span>')
    return (f'<details class="kpi kpi-{state} kpi-drop kpi-registry" data-testid="kpi-percent" data-valid="{valid}" data-repos="{repos}"><summary>{face}</summary>'
            f'<div class="kpi-drop-panel kpi-help-panel"><p data-i18n="registry_help" data-testid="registry-help">{esc(en["registry_help"])}</p></div></details>')


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
# Health alerts, last good build, activity cell and the repository panel
# ---------------------------------------------------------------------------

_EN_ELSEWHERE = {"link_actions": "Actions", "link_issues": "Issues"}   # keys the generator itself translates


def _en(key: str) -> str:
    return dashboard_app_texts.TEXTS["en"].get(key) or _EN_ELSEWHERE[key]


ALERT_GLYPH = {"ci": "✕", "manifest": "⚠", "version": "?", "inactive": "◷"}


def alert_item(alert: object, repo_url: str) -> str:
    kind = getattr(alert, "kind", "")
    detail = getattr(alert, "detail", "")
    why = (f'<span class="alert-why" data-i18n="alert_why_ci">{esc(_en("alert_why_ci"))}</span>' if kind == "ci"
           else f'<span class="alert-why">{esc(detail)}</span>' if detail
           else f'<span class="alert-why" data-i18n="alert_why_no_detail">{esc(_en("alert_why_no_detail"))}</span>')
    return (f'<li class="alert alert-{esc(kind)}" data-kind="{esc(kind)}" data-testid="alert-{esc(kind)}">'
            f'<span class="alert-kind"><span class="alert-glyph" aria-hidden="true">{ALERT_GLYPH.get(kind, "!")}</span><span data-i18n="alert_kind_{esc(kind)}">{esc(_en("alert_kind_" + kind))}</span></span>'
            f'<a href="{esc(getattr(alert, "url", "") or repo_url + getattr(alert, "repo", ""))}" target="_blank" rel="noopener noreferrer">{esc(getattr(alert, "repo", ""))}</a>{why}</li>')


def build_stamp(build: object | None) -> str:
    """The time and the run of the last good build. The region between the two comments is what scripts/dashboard_health.merge_build_info keeps stable."""
    label = f'<span class="build-label" data-i18n="build_label">{esc(_en("build_label"))}</span> '
    if build is None:
        inner = f'<span class="build-info" data-state="unknown">{label}<span data-i18n="not_verified">{esc(_en("not_verified"))}</span></span>'
    else:
        finished = str(getattr(build, "finished", ""))
        shown = finished.replace("T", " ")[:16] + " UTC"
        inner = (f'<span class="build-info" data-state="known">{label}<time datetime="{esc(finished)}">{esc(shown)}</time> · '
                 f'<a href="{esc(getattr(build, "url", ""))}" target="_blank" rel="noopener noreferrer" data-i18n="build_run">{esc(_en("build_run"))}</a></span>')
    return f'<p class="build-stamp muted" data-testid="build-stamp">{dashboard_health.BUILD_BEGIN}{inner}{dashboard_health.BUILD_END}</p>'


def alerts_card(data: AppData) -> str:
    """Health alerts: red CI, a manifest that cannot be read, a version that did not resolve, and (raised by the script, which knows today's date) no
    activity for too long. The state is never "no alerts" when the picture is incomplete: a failed read says "incomplete data"."""
    static = list(data.alerts)
    incomplete = list(data.incomplete)
    state = "incomplete" if incomplete else ("alerts" if static else "ok")
    key = {"ok": "alerts_none", "alerts": "alerts_some", "incomplete": "alerts_incomplete_some" if static else "alerts_incomplete"}[state]
    template = f' data-i18n-template="{key}" data-n="{len(static)}"' if key.endswith("some") else f' data-i18n="{key}"'
    glyph = {"ok": "●", "alerts": "▲", "incomplete": "?"}[state]
    status_text = _en(key).replace("{n}", str(len(static)))
    def why_item(code: str) -> str:
        if code == "activity_stale" and data.stale_date:
            return (f'<li data-i18n-template="alerts_why_activity_stale" data-date="{esc(data.stale_date)}">'
                    f'{esc(dashboard_robust_texts.TEXTS["en"]["alerts_why_activity_stale"].replace("{date}", data.stale_date))}</li>')
        return f'<li data-i18n="alerts_why_{esc(code)}">{esc(_en("alerts_why_" + code))}</li>'
    why = "".join(why_item(code) for code in incomplete)
    why_html = f'<ul class="alerts-why-list" data-testid="alerts-why">{why}</ul>' if why else ""
    items = "".join(alert_item(alert, data.repo_url) for alert in static)
    return (
        f'<section class="card card-alerts" aria-labelledby="alerts-t" data-testid="health-alerts" data-state="{state}" data-incomplete="{1 if incomplete else 0}" data-static="{len(static)}">'
        f'<header class="card-head"><h2 class="card-title" id="alerts-t" data-i18n="alerts_title">{esc(_en("alerts_title"))}</h2>'
        f'<p class="alerts-status alerts-{state}" id="alerts-status" role="status" data-testid="alerts-status" data-state="{state}">'
        f'<span class="alerts-glyph" aria-hidden="true">{glyph}</span><span id="alerts-status-text"{template}>{esc(status_text)}</span></p></header>'
        f'{why_html}'
        f'<div class="alerts-scroll" tabindex="0" role="region" aria-labelledby="alerts-t"><ul class="alerts-list" id="alerts-list" data-testid="alerts-list">{items}</ul></div>'
        f'{build_stamp(data.build)}</section>'
    )


def activity_cell(act: Activity | None) -> str:
    """The cell of the projects table: the script writes the badges (days, colour, glyph, text) from the dates of the last activity and of the last release."""
    if act is None:
        return ('<td class="activity-cell" data-known="0"><span class="act-badge act-unknown"><span class="act-glyph" aria-hidden="true">?</span>'
                f'<span data-i18n="not_verified">{esc(_en("not_verified"))}</span></span></td>')
    last = dashboard_health.last_activity(act.commit_date, act.release_date) or ""
    return (f'<td class="activity-cell" data-known="1" data-activity="{esc(last)}" data-release="{esc(act.release_date or "")}">'
            f'<span class="act-badge" data-kind="activity"></span><span class="act-badge" data-kind="release"></span></td>')


def repo_panel() -> str:
    """The side panel of a repository: one element for the whole page, filled by the script from the data embedded in the page."""
    def h(key: str) -> str:
        return f'data-i18n="{key}">{esc(_en(key))}'
    return (
        '<aside class="repo-panel" id="repo-panel" role="dialog" aria-modal="false" aria-labelledby="repo-panel-title" data-testid="repo-panel" hidden>'
        '<header class="repo-panel-head"><h2 id="repo-panel-title" tabindex="-1" data-testid="repo-panel-title"></h2>'
        f'<button type="button" class="btn btn-ghost" id="repo-panel-close" data-testid="repo-panel-close" data-i18n-aria-label="panel_close" aria-label="{esc(_en("panel_close"))}"><span aria-hidden="true">✕</span></button></header>'
        '<div class="repo-panel-body">'
        f'<section aria-labelledby="rp-manifest-t"><h3 id="rp-manifest-t" {h("panel_manifest")}</h3><dl class="repo-fields" id="repo-fields" data-testid="repo-fields"></dl></section>'
        f'<section aria-labelledby="rp-ci-t"><h3 id="rp-ci-t" {h("panel_ci")}</h3><p id="rp-ci" data-testid="repo-ci"></p></section>'
        f'<section aria-labelledby="rp-commits-t"><h3 id="rp-commits-t" {h("panel_commits")}</h3><ul class="repo-commits" id="rp-commits" data-testid="repo-commits"></ul>'
        f'<p class="muted" id="rp-commits-none" data-testid="repo-commits-none" hidden {h("panel_commits_none")}</p></section>'
        f'{dashboard_evo_ui.panel_evidence()}'
        f'<nav aria-labelledby="rp-links-t"><h3 id="rp-links-t" {h("panel_links")}</h3><ul class="repo-links" id="rp-links" data-testid="repo-links">'
        f'<li><a data-link="actions" href="https://github.com/JuanenRac/" target="_blank" rel="noopener noreferrer" {h("link_actions")}</a></li>'
        f'<li><a data-link="issues" href="https://github.com/JuanenRac/" target="_blank" rel="noopener noreferrer" {h("link_issues")}</a></li>'
        f'<li><a data-link="releases" href="https://github.com/JuanenRac/" target="_blank" rel="noopener noreferrer" {h("link_releases")}</a></li>'
        f'<li><a data-link="readme" href="https://github.com/JuanenRac/" target="_blank" rel="noopener noreferrer" {h("link_readme")}</a></li></ul></nav>'
        '</div></aside>'
    )


def data_script(payload: Mapping[str, object]) -> str:
    """The data the script reads (thresholds, repositories, contributing repositories) as JSON that cannot close the script element."""
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    text = text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return f'<script type="application/json" id="dashboard-data">{text}</script>'


# ---------------------------------------------------------------------------
# Panels
# ---------------------------------------------------------------------------

def summary_panel(data: AppData, ecosystem_cards_html: str) -> str:
    cards = "".join(progress_card(data, key, label, ctx="s") for key, label in ECOSYSTEMS)
    latest, oldest = releases_lists(data, None, 7)
    # Green only when every listed project resolved its version; red when none did; neutral otherwise (and with nothing listed).
    resolved_state = "none" if not data.total else ("ok" if data.ok == data.total else "bad" if data.ok == 0 else "mid")
    kpis = (
        f'<div class="kpi" data-testid="kpi-total"><span class="kpi-number" id="health-total">{data.total}</span><span class="kpi-label"><b data-i18n="health_total">Total projects</b></span></div>'
        f'<div class="kpi kpi-{resolved_state}" data-testid="kpi-resolved"><span class="kpi-number" id="health-resolved">{data.ok}</span><span class="kpi-label"><b data-i18n="health_resolved">Version resolved</b></span></div>'
        f'{errors_card(data)}'
        f'{registry_card(data)}'
    )
    banner = dashboard_robust.stale_banner_html(data.stale_date)
    return f"""
    <div class="summary-grid">
      {banner}
      {dashboard_evo_ui.visit_card()}
      {alerts_card(data)}
      <section class="kpi-strip" aria-label="Key figures" data-i18n-aria-label="aria_key_figures">{kpis}</section>
      <section class="card card-eco-counts" aria-labelledby="eco-counts-t">
        <h2 class="card-title" id="eco-counts-t" data-i18n="section_by_ecosystem">Projects by ecosystem</h2>
        <div class="eco-counts">{ecosystem_cards_html}</div>
      </section>
      <section class="card card-progress" aria-labelledby="progress-t">
        <header class="card-head"><h2 class="card-title" id="progress-t" data-i18n="sum_progress_title">Progress and status by ecosystem</h2>
          <span class="muted" data-i18n="sum_progress_hint">Same figures as the README.</span></header>
        <div class="eco-grid">{cards}</div>
      </section>
      <section class="card card-ci" aria-label="Continuous integration" data-i18n-aria-label="sum_ci_title">
        {ci_figure(data, ECOSYSTEMS)}
        {red_ci_list(data, None)}
        {months_figure(data, None)}
      </section>
      <section class="card card-maturity">{stacked_figure("maturity", data, ECOSYSTEMS)}</section>
      <section class="card card-evidence">{stacked_figure("evidence", data, ECOSYSTEMS)}</section>
      <section class="card card-releases"><h2 class="card-title" data-i18n="sum_releases_title">Latest releases</h2>{latest}</section>
      <section class="card card-oldest"><h2 class="card-title" data-i18n="sum_oldest_title">Longest without a release</h2>{oldest}</section>
      {dashboard_evo_ui.history_card()}
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
        {progress_card(data, eco, label, big=True, link_tab=False, ctx="e")}
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
    return f'<div class="errors-panel" data-testid="errors-panel">{data.generation_html}{integrity_html.replace("<details class=", "<details open class=", 1)}{unresolved}</div>'


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
    <aside class="sidebar" id="sidebar" aria-labelledby="filters-t">
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


SCOPES: tuple[tuple[str, str, str], ...] = (
    ("all", "scope_all", "All"),
    ("hydra-umc", "", "HYDRA-UMC"),
    ("urtc", "", "URTC"),
    ("armor", "", "A.R.M.O.R."),
    ("eh3d", "", "EH3D"),
    ("electro-hobby-3d", "scope_cross", "Cross-cutting"),
)


def scope_bar(eco_counts: Mapping[str, int], total: int) -> str:
    """The bar over the project table: All / the four ecosystems / Cross-cutting, with the families (or types) of the chosen one under it.
    Each button is a toggle (aria-pressed) and carries the number of projects of its scope; the script fills the second row."""
    buttons = []
    for ident, key, text in SCOPES:
        count = total if ident == "all" else eco_counts.get(ident, 0)
        label = f'<span data-i18n="{key}">{esc(text)}</span>' if key else f"<span>{esc(text)}</span>"
        buttons.append(f'<button type="button" class="chip scope-btn" data-scope="{esc(ident)}" aria-pressed="false" data-testid="scope-{esc(ident)}">{label}<b>{count}</b></button>')
    return (
        '<div class="scope" data-testid="scope-bar">'
        '<div class="scope-row" role="group" aria-labelledby="scope-t"><span class="scope-title" id="scope-t" data-i18n="scope_label">Scope</span>' + "".join(buttons) + '</div>'
        '<div class="scope-row scope-sub" role="group" aria-labelledby="scope-sub-t"><span class="scope-title" id="scope-sub-t" data-i18n="scope_sub_label">Families</span>'
        '<span class="scope-sub-hint" id="scope-sub-hint" data-i18n="scope_all_hint">Pick an ecosystem to browse its families.</span>'
        '<span class="chip-row" id="scope-sub-chips" data-testid="scope-sub"></span></div>'
        + dashboard_delivery_ui.pipeline_filter() + '</div>'
    )


def pager() -> str:
    """Previous / next buttons and the range shown; the script hides the bar when everything fits in one page."""
    return (
        '<nav class="pager" id="pager" aria-label="Project list pages" data-i18n-aria-label="pager_label" data-testid="pager" hidden>'
        '<button type="button" class="btn btn-ghost" id="pager-prev" data-i18n="pager_prev" data-testid="pager-prev">Previous</button>'
        '<span class="pager-info" id="pager-info" aria-live="polite" data-i18n-template="pager_info" data-page="1" data-pages="1">Page 1 of 1</span>'
        '<span id="pager-range" data-i18n-template="pager_range" data-from="0" data-to="0" data-n="0"></span>'
        '<button type="button" class="btn btn-ghost" id="pager-next" data-i18n="pager_next" data-testid="pager-next">Next</button></nav>'
    )


def tab_list() -> str:
    buttons = []
    for ident, key, literal in TABS:
        text = f'<span data-i18n="{key}">{ENGLISH[key]}</span>' if key else f"<span>{esc(literal)}</span>"
        accent = f" tab-eco tab-{ident}" if not key else ""
        buttons.append(
            f'<button type="button" role="tab" class="tab{accent}" id="tab-{ident}" aria-controls="panel-{ident}" aria-selected="false" tabindex="-1" '
            f'data-tab="{ident}" data-testid="tab-{ident}">{text}</button>'
        )
    more = ('<button type="button" class="tabs-more tabs-more-{d}" data-tabs-scroll="{s}" data-i18n-aria-label="tabs_scroll_{d}" aria-label="{e}" hidden tabindex="-1" data-testid="tabs-scroll-{d}">{g}</button>')
    return (f'<div class="tabs-wrap">' + more.format(d="prev", s="-1", e="Show the previous sections", g="‹")
            + f'<nav class="tabs" aria-label="Dashboard sections" data-i18n-aria-label="tabs_label"><div role="tablist" aria-orientation="horizontal" id="tablist">{"".join(buttons)}</div></nav>'
            + more.format(d="next", s="1", e="Show the next sections", g="›") + '</div>')


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
  .topbar { flex-wrap: wrap; row-gap: 4px; padding-bottom: 4px; }
  .top-actions { margin-left: auto; }
  .tabs-wrap { order: 3; flex: 1 1 100%; min-width: 0; display: flex; align-items: center; position: relative; }
  .tabs-wrap.over .tabs { padding-inline: 34px; }
  .tabs { flex: 1 1 auto; min-width: 0; overflow-x: auto; scrollbar-width: none; scroll-behavior: smooth; }
  .tabs::-webkit-scrollbar { display: none; }
  .tabs-more { position: absolute; top: 50%; transform: translateY(-50%); z-index: 2; appearance: none; background: var(--panel-2); color: var(--text); border: 1px solid var(--border-strong); border-radius: 8px; width: 28px; height: 32px; font-size: 18px; line-height: 1; cursor: pointer; }
  .tabs-more[hidden] { display: none; } .tabs-more-prev { left: 0; } .tabs-more-next { right: 0; }
  @media (prefers-reduced-motion: reduce) { .tabs { scroll-behavior: auto; } }
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
    .tabs-wrap { order: 3; flex: 1 1 100%; }
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
    .tabs-wrap { order: 3; flex: 1 1 100%; }
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

  /* ======================= Charts: relief, hover and entrance ======================= */
  .bar-row, .col-g { outline-offset: 3px; }
  .bar-depth { fill: #000; opacity: .3; }
  :root[data-theme="light"] .bar-depth { opacity: .16; }
  .bar-nums, .seg-count, .col-value, .chart-label, .chart-total { pointer-events: none; }
  .seg-bevel { fill: #000; opacity: .16; pointer-events: none; }
  .seg-edge { fill: #fff; opacity: .45; pointer-events: none; }
  .seg { transition: opacity .15s ease, filter .15s ease; cursor: default; }
  .seg:hover, .bar-row:focus-visible .seg { stroke: var(--text); stroke-width: 2; filter: brightness(1.14); }
  .chart-stacked:has(.seg:hover) .seg:not(:hover) { opacity: .62; }
  .ring-value { filter: drop-shadow(0 2px 2px rgba(0,0,0,.45)); }
  .ring-sheen { stroke: #fff; opacity: .34; pointer-events: none; }
  .ring-wrap { border-radius: 50%; transition: transform .2s ease; }
  .ring-wrap:hover, .ring-wrap:focus-visible { transform: scale(1.05); }
  .col-top { fill: #fff; opacity: .34; }
  .col-side { fill: #000; opacity: .3; }
  .col-g { cursor: default; }
  .col-g:hover .col, .col-g:focus-visible .col { filter: brightness(1.22); }
  .col-g:hover .col-value, .col-g:focus-visible .col-value { font-size: 13.5px; }
  .area-bar { box-shadow: inset 0 1px 2px rgba(0,0,0,.38); }
  .area-fill { background-image: linear-gradient(rgba(255,255,255,.3), rgba(255,255,255,0) 55%, rgba(0,0,0,.18)); transform-origin: left center; }
  .area:hover .area-bar { outline: 1px solid var(--text); outline-offset: 1px; }
  .eco-card { transition: transform .2s ease, box-shadow .2s ease; }
  .eco-card:hover { transform: translateY(-2px); box-shadow: 0 8px 18px rgba(0,0,0,.28); }
  .chart-tip { position: fixed; z-index: 100; max-width: min(360px, 90vw); padding: 6px 10px; border-radius: 8px; font-size: 12.5px; line-height: 1.35; font-variant-numeric: tabular-nums;
               background: var(--panel-2); color: var(--text); border: 1px solid var(--border-strong); box-shadow: 0 6px 18px rgba(0,0,0,.35); }
  .chart-tip[hidden] { display: none; }
  @keyframes t25-grow-x { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  @keyframes t25-grow-y { from { transform: scaleY(0); } to { transform: scaleY(1); } }
  @keyframes t25-fade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes t25-ring { from { stroke-dashoffset: var(--dash); } to { stroke-dashoffset: 0; } }
  @keyframes t25-rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
  @media (prefers-reduced-motion: no-preference) {
    .bar-fill { animation: t25-grow-x .7s cubic-bezier(.2,.7,.2,1) both; animation-delay: calc(var(--i, 0) * 90ms); }
    .bar-nums, .col-value { animation: t25-fade .45s ease both; animation-delay: calc(var(--i, 0) * 90ms + 380ms); }
    .col-body { animation: t25-grow-y .65s cubic-bezier(.2,.7,.2,1) both; animation-delay: calc(var(--i, 0) * 80ms); }
    .ring-value, .ring-sheen { animation: t25-ring 1s cubic-bezier(.2,.7,.2,1) both; }
    .area-fill { animation: t25-grow-x .8s cubic-bezier(.2,.7,.2,1) both; }
    .eco-grid > .eco-card { animation: t25-rise .5s ease both; }
    .eco-grid > .eco-card:nth-child(2) { animation-delay: 70ms; } .eco-grid > .eco-card:nth-child(3) { animation-delay: 140ms; } .eco-grid > .eco-card:nth-child(4) { animation-delay: 210ms; }
  }

  /* ======================= Projects: scope bar and pager ======================= */
  #panel-projects .panel-inner { display: flex; flex-direction: column; gap: 10px; }
  #panel-projects .table-wrapper { flex: 1 1 auto; min-height: 0; }
  .scope { display: grid; gap: 8px; padding: 10px 12px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); flex: 0 0 auto; }
  .scope-row { display: flex; flex-wrap: wrap; gap: 6px 8px; align-items: center; min-width: 0; }
  .scope-title { font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); font-weight: 700; margin-right: 4px; }
  .scope-btn { padding: 6px 12px; font-size: 13px; font-weight: 600; }
  .scope-btn[data-scope]:not([data-scope="all"])::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--eco-color, var(--c-electro-hobby-3d)); display: inline-block; }
  .scope-btn[data-scope="hydra-umc"] { --eco-color: var(--c-hydra-umc); } .scope-btn[data-scope="urtc"] { --eco-color: var(--c-urtc); }
  .scope-btn[data-scope="armor"] { --eco-color: var(--c-armor); } .scope-btn[data-scope="eh3d"] { --eco-color: var(--c-eh3d); }
  .scope-sub-hint { font-size: 12px; color: var(--dim); }
  .scope-sub .chip { font-size: 12px; }
  .pager { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; justify-content: center; font-size: 12.5px; color: var(--dim); flex: 0 0 auto; }
  .pager[hidden] { display: none; }
  .pager .btn { min-width: 84px; }
  .pager-info { color: var(--text); font-variant-numeric: tabular-nums; }

  /* ======================= Health alerts, activity badges, contributing repositories, repository panel ======================= */
  :root { --warn-ink: #fbbf24; }
  :root[data-theme="light"] { --warn-ink: #8a5a00; }
  @media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) { --warn-ink: #8a5a00; } }
  .card-alerts { grid-column: span 12; display: grid; gap: 8px; }
  .card-alerts .card-head { margin-bottom: 0; align-items: center; }
  .alerts-status { margin: 0; display: inline-flex; gap: 8px; align-items: center; font-weight: 700; font-size: 13px; padding: 4px 12px; border-radius: 999px; border: 1px solid currentColor; }
  .alerts-ok { color: var(--ok); } .alerts-alerts { color: var(--err); } .alerts-incomplete { color: var(--warn-ink); }
  .alerts-why-list { margin: 0; padding-left: 20px; font-size: 12.5px; color: var(--warn-ink); }
  .alerts-scroll { max-height: 148px; overflow: auto; border-radius: 8px; }
  .alerts-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 4px; }
  .alerts-list:empty { display: none; }
  .alerts-scroll:has(.alerts-list:empty) { display: none; }
  .alert { display: grid; grid-template-columns: 190px minmax(160px, 280px) minmax(0, 1fr); gap: 4px 12px; align-items: baseline; font-size: 12.5px; padding: 4px 8px; border: 1px solid var(--border); border-left: 4px solid var(--err); border-radius: 8px; background: var(--bg); }
  .alert-manifest, .alert-version { border-left-color: var(--warn-ink); } .alert-inactive { border-left-color: var(--dim); }
  .alert-kind { display: inline-flex; gap: 6px; font-weight: 700; } .alert-ci .alert-kind { color: var(--err); } .alert-manifest .alert-kind, .alert-version .alert-kind { color: var(--warn-ink); }
  .alert a { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .alert-why { color: var(--dim); min-width: 0; overflow-wrap: anywhere; }
  .build-stamp { margin: 0; }
  .build-stamp a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }

  .activity-cell { white-space: nowrap; }
  .act-badge { display: inline-flex; gap: 5px; align-items: center; font-size: 11.5px; font-weight: 600; padding: 1px 8px; margin: 1px 4px 1px 0; border-radius: 999px; border: 1px solid currentColor; font-variant-numeric: tabular-nums; }
  .act-badge:empty { display: none; }
  .act-good { color: var(--ok); } .act-warn { color: var(--warn-ink); } .act-bad { color: var(--err); } .act-unknown, .act-none { color: var(--dim); }
  .activity-cell .act-badge { display: flex; width: max-content; }
  .activity-cell .act-badge:empty { display: none; }

  .area-btn { appearance: none; background: none; border: 0; padding: 0; margin: 0; color: inherit; font: inherit; cursor: pointer; text-align: left; border-radius: 6px; }
  .area-btn:hover .area-caret, .contrib-toggle:hover .area-caret { color: var(--text); }
  .area-caret { margin-left: auto; color: var(--dim); transition: transform .15s ease; display: inline-block; }
  .contrib-toggle .area-caret { margin-left: 4px; }
  [aria-expanded="true"] > .area-caret { transform: rotate(90deg); }
  .area-bar { cursor: pointer; }
  .contrib-toggle { margin-top: 4px; font-size: 12px; align-self: flex-start; }
  .area { grid-template-areas: "name num" "bar bar" "contrib contrib"; }
  .contrib { grid-area: contrib; margin-top: 6px; padding: 8px 10px; border: 1px solid var(--border-strong); border-radius: 8px; background: var(--bg); font-size: 12.5px; min-width: 0; }
  .contrib[hidden] { display: none; }
  .contrib-progress { margin-top: 10px; }
  .card-eco-main .contrib-progress { grid-column: 1 / -1; }
  .contrib-head { margin: 0 0 6px; font-weight: 700; }
  .contrib-note { margin: 0 0 6px; color: var(--warn-ink); font-size: 12px; }
  .contrib-scroll { max-height: 190px; overflow: auto; }
  .contrib-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 3px; }
  .contrib-list li { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; border-bottom: 1px dashed var(--border); padding: 2px 0; }
  .contrib-list a { overflow-wrap: anywhere; }
  .contrib-mat { font-size: 11px; color: var(--dim); border: 1px solid var(--border-strong); border-radius: 6px; padding: 0 6px; }
  .contrib-pts { margin-left: auto; font-variant-numeric: tabular-nums; color: var(--dim); font-size: 11.5px; }
  .contrib-more { margin-top: 6px; } .contrib-more > summary { cursor: pointer; color: var(--dim); min-height: 24px; display: flex; align-items: center; }

  tr.project-row { cursor: pointer; }
  .panel-open { appearance: none; background: transparent; color: var(--accent); border: 1px solid var(--border-strong); border-radius: 8px; padding: 2px 10px; min-height: 24px; font-size: 11.5px; cursor: pointer; margin-left: 6px; }
  .panel-open:hover { border-color: var(--accent); }
  .repo-panel { position: fixed; top: 0; right: 0; bottom: 0; width: min(440px, 100vw); z-index: 70; background: var(--panel); border-left: 1px solid var(--border-strong); box-shadow: -10px 0 30px rgba(0,0,0,.35); display: flex; flex-direction: column; }
  .repo-panel[hidden] { display: none; }
  .repo-panel-head { display: flex; gap: 10px; align-items: center; justify-content: space-between; padding: 12px 14px; border-bottom: 1px solid var(--border); }
  .repo-panel-head h2 { margin: 0; font-size: 16px; overflow-wrap: anywhere; }
  .repo-panel-body { overflow-y: auto; padding: 10px 14px 20px; display: grid; gap: 14px; align-content: start; }
  .repo-panel h3 { margin: 0 0 6px; font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); }
  .repo-fields { margin: 0; display: grid; grid-template-columns: minmax(90px, 140px) minmax(0, 1fr); gap: 4px 12px; font-size: 13px; }
  .repo-fields dt { color: var(--dim); } .repo-fields dd { margin: 0; overflow-wrap: anywhere; }
  .repo-commits, .repo-links { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; font-size: 13px; }
  .repo-commits time { color: var(--dim); font-size: 11.5px; display: block; }
  .repo-links { grid-auto-flow: column; justify-content: start; gap: 8px; } .repo-links a { display: inline-block; padding: 4px 12px; border: 1px solid var(--border-strong); border-radius: 999px; }
  .repo-ci { font-weight: 700; }
  @media (max-width: 1100px) { .alert { grid-template-columns: 1fr; } .alert a { white-space: normal; } }
  @keyframes t27-slide { from { transform: translateX(24px); opacity: 0; } to { transform: none; opacity: 1; } }
  @media (prefers-reduced-motion: no-preference) { .repo-panel:not([hidden]) { animation: t27-slide .22s ease both; } }
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

  const FILTER_KINDS = ["status", "eco", "maturity", "role", "deploy", "pipeline"];
  const state = { status: "all", eco: "all", maturity: "all", role: "all", deploy: "all", pipeline: "all" };
  const ROW_FIELD = { status: "status", eco: "ecosystem", maturity: "maturity", role: "role", deploy: "deploy", pipeline: "pipeline" };

  function syncButtons(kind) {
    document.querySelectorAll("[data-filter-" + kind + "]").forEach(function (button) {
      const on = button.getAttribute("data-filter-" + kind) === state[kind];
      button.classList.toggle("active", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function currentDict() { return I18N[document.documentElement.lang] || I18N.en; }

  const PAGE_SIZE = 25;
  let page = 1;
  const pagerNav = document.getElementById("pager");
  const pagerPrev = document.getElementById("pager-prev");
  const pagerNext = document.getElementById("pager-next");
  const pagerInfo = document.getElementById("pager-info");
  const pagerRange = document.getElementById("pager-range");
  const subChips = document.getElementById("scope-sub-chips");
  const subHint = document.getElementById("scope-sub-hint");
  let subBuiltFor = null;

  // The scope is the ecosystem chosen in the bar over the table (state.eco); the families (or the types when an ecosystem has no families)
  // of that scope are listed under it.
  function buildSubChips() {
    if (!subChips) { return; }
    subBuiltFor = state.eco;
    subChips.textContent = "";
    if (subHint) { subHint.hidden = state.eco !== "all"; }
    if (state.eco === "all") { return; }
    const scoped = rows.filter(function (row) { return row.dataset.ecosystem === state.eco; });
    function collect(field) {
      const found = {};
      scoped.forEach(function (row) { const v = row.dataset[field] || ""; if (v) { found[v] = (found[v] || 0) + 1; } });
      return found;
    }
    let kind = "family";
    let found = collect("family");
    if (!Object.keys(found).length) { kind = "role"; found = collect("role"); }
    Object.keys(found).sort().forEach(function (value) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "chip";
      button.setAttribute("data-sub-" + kind, value);
      button.setAttribute("aria-pressed", "false");
      button.setAttribute("data-testid", "scope-sub-" + value);
      const label = document.createElement("span");
      if (kind === "family") {
        const option = familySelect && Array.from(familySelect.options).find(function (o) { return o.value === value; });
        label.textContent = option ? option.textContent.replace(/\s*\(\d+\)\s*$/, "") : value;
      } else {
        const source = document.querySelector("[data-filter-role='" + value + "'] span");
        label.textContent = source ? source.textContent : value;
        label.setAttribute("data-i18n", "role_" + value);
      }
      const count = document.createElement("b");
      count.textContent = String(found[value]);
      button.appendChild(label);
      button.appendChild(count);
      button.addEventListener("click", function () {
        if (kind === "family") {
          if (familySelect) { familySelect.value = familySelect.value === value ? "all" : value; }
        } else {
          state.role = state.role === value ? "all" : value;
          syncButtons("role");
        }
        applyFilters();
      });
      subChips.appendChild(button);
    });
  }

  function syncSubChips() {
    if (!subChips) { return; }
    Array.from(subChips.querySelectorAll("button")).forEach(function (button) {
      const family = button.getAttribute("data-sub-family");
      const on = family !== null ? (familySelect && familySelect.value === family) : state.role === button.getAttribute("data-sub-role");
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function applyFilters(keepPage) {
    const query = searchInput.value.trim().toLowerCase();
    const activeFamily = familySelect ? familySelect.value : "all";
    let visible = 0;
    let visibleOk = 0;
    const visibleFamilies = {};
    const visibleEcosystems = {};
    if (subBuiltFor !== state.eco) { buildSubChips(); }

    // 1. which projects match the scope, the search and the filters (all of them, whatever page they are on)
    const matched = [];
    rows.forEach(function (row) {
      const name = row.dataset.name || "";
      const status = row.dataset.status || "";
      const deploy = row.dataset.deploy || "";
      const stack = row.dataset.stack || "";
      const family = row.dataset.family || "";
      const notes = row.dataset.notes || "";
      let show = !query || name.includes(query) || stack.includes(query) || deploy.includes(query) || family.includes(query) || notes.includes(query);
      FILTER_KINDS.forEach(function (kind) {
        if (state[kind] !== "all" && (row.dataset[ROW_FIELD[kind]] || (kind === "pipeline" ? "undeclared" : "")) !== state[kind]) { show = false; }
      });
      if (activeFamily !== "all" && family !== activeFamily) { show = false; }
      row.dataset.match = show ? "1" : "0";
      if (show) { matched.push(row); }
    });

    // 2. only the page being looked at is painted
    const pages = Math.max(1, Math.ceil(matched.length / PAGE_SIZE));
    page = keepPage === true ? Math.min(Math.max(1, page), pages) : 1;
    const first = (page - 1) * PAGE_SIZE;
    const onPage = new Set(matched.slice(first, first + PAGE_SIZE));
    rows.forEach(function (row) {
      const show = onPage.has(row);
      row.classList.toggle("hidden", !show);
      if (!show) {
        const toggle = row.querySelector(".details-toggle");
        const targetId = toggle && toggle.dataset.detailsTarget;
        const target = targetId && document.getElementById(targetId);
        if (target) { target.hidden = true; }
        if (toggle) { toggle.setAttribute("aria-expanded", "false"); toggle.textContent = "▸"; }
      } else {
        const family = row.dataset.family || "";
        if (family) { visibleFamilies[(row.dataset.ecosystem || "") + "|" + family] = true; }
        if (row.dataset.ecosystem) { visibleEcosystems[row.dataset.ecosystem] = true; }
      }
    });
    matched.forEach(function (row) { visible += 1; if (row.dataset.status === "ok") { visibleOk += 1; } });

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
    if (countLabel) {
      countLabel.setAttribute("data-shown", String(visible));
      countLabel.setAttribute("data-total", String(rows.length));
      countLabel.textContent = fillTemplate(currentDict().filters_matches || "{shown} / {total}", countLabel);
    }
    if (pagerNav) {
      pagerNav.hidden = visible <= PAGE_SIZE;
      pagerNav.setAttribute("data-page", String(page));
      pagerNav.setAttribute("data-pages", String(pages));
      if (pagerPrev) { pagerPrev.disabled = page <= 1; }
      if (pagerNext) { pagerNext.disabled = page >= pages; }
      [pagerInfo, pagerRange].forEach(function (el) {
        if (!el) { return; }
        el.setAttribute("data-page", String(page));
        el.setAttribute("data-pages", String(pages));
        el.setAttribute("data-from", String(visible ? first + 1 : 0));
        el.setAttribute("data-to", String(Math.min(visible, first + PAGE_SIZE)));
        el.setAttribute("data-n", String(visible));
        el.textContent = fillTemplate(currentDict()[el.getAttribute("data-i18n-template")] || "", el);
      });
    }
    syncScope();
    syncSubChips();
    if (typeof onScopeOrPageChanged === "function") { onScopeOrPageChanged(); }
    if (resetFiltersBtn) {
      const anyFilterActive = query.length > 0 || activeFamily !== "all" || FILTER_KINDS.some(function (kind) { return state[kind] !== "all"; });
      resetFiltersBtn.disabled = !anyFilterActive;
    }
  }

  function syncScope() {
    document.querySelectorAll("[data-scope]").forEach(function (button) {
      button.setAttribute("aria-pressed", button.getAttribute("data-scope") === state.eco ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-scope]").forEach(function (button) {
    button.addEventListener("click", function () {
      state.eco = button.getAttribute("data-scope");
      if (familySelect) { familySelect.value = "all"; }
      FILTER_KINDS.forEach(syncButtons);
      applyFilters();
    });
  });
  if (pagerPrev) { pagerPrev.addEventListener("click", function () { page -= 1; applyFilters(true); scrollTable(); }); }
  if (pagerNext) { pagerNext.addEventListener("click", function () { page += 1; applyFilters(true); scrollTable(); }); }
  function scrollTable() { const w = document.querySelector("#panel-projects .table-wrapper"); if (w) { w.scrollTop = 0; } }

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


  // ---------------- Scope and page in the address, and the remembered scope ----------------
  const SCOPE_KEY = "hydra-dashboard-scope";
  const SCOPES = Array.from(document.querySelectorAll("[data-scope]")).map(function (b) { return b.getAttribute("data-scope"); });
  var currentTab = "summary";
  var shortcutsOn = true;      // single-key shortcuts (the help dialog switches them off)
  var navRepo = null;          // the repository whose panel is open, for the breadcrumb and the address
  var crumbRefresh = null;
  var hashReady = false;
  var hashWriters = [];        // functions that add parameters to the address (filters, search, period...)
  var hashAppliers = [];       // functions that read those parameters back
  var scopeRestored = false;
  var modes = { compact: false, present: false, fromHash: false };

  function parseHash() {
    const raw = location.hash.replace(/^#/, "");
    const q = raw.indexOf("?");
    const params = {};
    if (q >= 0) {
      raw.slice(q + 1).split("&").forEach(function (part) {
        const kv = part.split("=");
        try { if (kv[0]) { params[decodeURIComponent(kv[0])] = decodeURIComponent(kv[1] || ""); } } catch (e) { /* malformed escape: ignored */ }
      });
    }
    return { tab: q >= 0 ? raw.slice(0, q) : raw, params: params };
  }

  function writeHash() {
    let wanted = "#" + currentTab;
    const query = [];
    if (currentTab === "projects") {
      if (state.eco !== "all") { query.push("scope=" + encodeURIComponent(state.eco)); }
      if (page > 1) { query.push("page=" + page); }
    }
    if (navRepo) { query.push("repo=" + encodeURIComponent(navRepo)); }
    if (modes.compact) { query.push("view=compact"); }
    if (modes.present) { query.push("mode=present"); }
    hashWriters.forEach(function (write) { write(query); });
    if (query.length) { wanted += "?" + query.join("&"); }
    if (location.hash !== wanted) {
      try { history.replaceState(null, "", wanted); } catch (e) { location.hash = wanted.slice(1); }
    }
  }

  function onScopeOrPageChanged() {
    if (!hashReady) { return; }
    safeSet(SCOPE_KEY, state.eco);
    if (currentTab === "projects") { writeHash(); }
    if (crumbRefresh) { crumbRefresh(); }
  }

  function applyHashState(parsed) {
    hashAppliers.forEach(function (apply) { apply(parsed.params); });
    if (parsed.params.view === "compact") { modes.compact = true; modes.fromHash = true; }
    if (parsed.params.mode === "present") { modes.present = true; }
    const scope = parsed.params.scope;
    if (scope && SCOPES.indexOf(scope) >= 0) {
      scopeRestored = true;
      if (scope !== state.eco) {
        state.eco = scope;
        if (familySelect) { familySelect.value = "all"; }
        FILTER_KINDS.forEach(syncButtons);
        applyFilters();
      }
    }
    const n = parseInt(parsed.params.page, 10);
    if (n > 1) { page = n; applyFilters(true); }
  }

  // The scope of the last visit comes back the first time the projects are opened, unless the address already names one.
  function restoreScope() {
    if (scopeRestored) { return; }
    scopeRestored = true;
    const stored = safeGet(SCOPE_KEY);
    if (stored && stored !== "all" && SCOPES.indexOf(stored) >= 0 && state.eco === "all") {
      state.eco = stored;
      FILTER_KINDS.forEach(syncButtons);
      applyFilters();
    }
  }

  // ---------------- Charts: names in the language of the page, tooltip ----------------
  function tpl(text, values) {
    return String(text || "").replace(/\{(\w+)\}/g, function (_m, key) { return values[key] !== undefined ? values[key] : ""; });
  }
  function chartName(el, dict) {
    const key = el.getAttribute("data-name-key") || el.getAttribute("data-a-name-key");
    if (key && Object.prototype.hasOwnProperty.call(dict, key)) { return dict[key]; }
    return el.getAttribute("data-name") || el.getAttribute("data-a-name") || "";
  }
  function pctOf(n, total) { return total > 0 ? Math.round(n * 100 / total) : 0; }
  function chartText(el, dict) {
    const kind = el.getAttribute("data-aria");
    if (kind === "pct") {
      const name = chartName(el, dict);
      const pct = el.getAttribute("data-a-pct");
      if (pct === null) { return tpl(dict.aria_no_data, { name: name }); }
      const n = el.getAttribute("data-a-n");
      return n !== null ? tpl(dict.aria_pct_counts, { name: name, pct: pct, n: n, total: el.getAttribute("data-a-total") }) : tpl(dict.aria_pct, { name: name, pct: pct });
    }
    if (kind === "col" || el.classList.contains("seg")) {
      const n = Number(el.getAttribute("data-n"));
      const total = Number(el.getAttribute("data-total"));
      return tpl(dict.tip_count, { name: chartName(el, dict), n: n, total: total, pct: pctOf(n, total) });
    }
    if (kind === "row") {
      const row = el.getAttribute("data-row") || "";
      const segs = Array.from(el.querySelectorAll(".seg"));
      if (!segs.length) { return tpl(dict.aria_no_data, { name: row }); }
      return tpl(dict.aria_row, { row: row, parts: segs.map(function (s) { return chartName(s, dict) + " " + s.getAttribute("data-n"); }).join(", ") });
    }
    return "";
  }
  function applyChartLabels(dict) {
    document.querySelectorAll("[data-aria]").forEach(function (el) {
      const text = chartText(el, dict);
      if (text) { el.setAttribute("aria-label", text); }
    });
  }

  const tip = document.createElement("div");
  tip.id = "chart-tip";
  tip.className = "chart-tip";
  tip.setAttribute("role", "tooltip");
  tip.hidden = true;
  document.body.appendChild(tip);
  let tipFor = null;
  function hideTip() { tip.hidden = true; tipFor = null; }
  function showTip(target) {
    tipFor = target;
    const text = chartText(target, currentDict());
    if (!text) { hideTip(); return; }
    tip.textContent = text;
    tip.hidden = false;
    const r = target.getBoundingClientRect();
    const w = tip.offsetWidth;
    const h = tip.offsetHeight;
    const left = Math.max(8, Math.min(r.left + r.width / 2 - w / 2, window.innerWidth - w - 8));
    const top = r.top - h >= 8 ? r.top - h : Math.min(r.bottom, window.innerHeight - h - 8);
    tip.style.left = left + "px";
    tip.style.top = top + "px";
  }
  function tipTarget(node) { return node && node.closest ? node.closest(".seg, .col-g, .ring-wrap, .area-bar, .bar-row") : null; }
  document.addEventListener("mouseover", function (event) {
    if (tip.contains(event.target)) { return; }
    const target = tipTarget(event.target);
    if (target) { showTip(target); } else { hideTip(); }
  });
  document.addEventListener("focusin", function (event) { const target = tipTarget(event.target); if (target) { showTip(target); } else { hideTip(); } });
  document.addEventListener("focusout", hideTip);
  document.addEventListener("keydown", function (event) { if (event.key === "Escape") { hideTip(); } });
  // Scrolling moves the tooltip with its chart; it goes away when the pointer or the focus leaves the chart (the browser sends a mouse event after a scroll).
  document.addEventListener("scroll", function () { if (tipFor && !tip.hidden) { showTip(tipFor); } }, true);

  function safeGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function safeSet(key, value) { try { localStorage.setItem(key, value); } catch (e) { /* storage blocked */ } }

  function revealTab(tab) {
    const bar = tab.closest("nav");
    if (!bar) { return; }
    const t = tab.getBoundingClientRect();
    const b = bar.getBoundingClientRect();
    if (t.left < b.left + 40) { bar.scrollLeft -= b.left + 40 - t.left; }
    else if (t.right > b.right - 40) { bar.scrollLeft += t.right - (b.right - 40); }
  }

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
        revealTab(tab);
      }
    });
    panels.forEach(function (panel) { panel.hidden = panel.id !== "panel-" + id; });
    safeSet(TAB_KEY, id);
    currentTab = id;
    if (options.updateHash !== false) { writeHash(); }
    if (crumbRefresh) { crumbRefresh(); }
    if (id === "projects") { restoreScope(); }
  }

  // Scroll arrows of the tab bar: they appear only when some tabs do not fit (the bar keeps working with the arrow keys either way).
  (function () {
    const bar = document.querySelector(".tabs");
    const prev = document.querySelector("[data-tabs-scroll='-1']");
    const next = document.querySelector("[data-tabs-scroll='1']");
    if (!bar || !prev || !next) { return; }
    function refresh() {
      const over = bar.firstElementChild.offsetWidth > bar.parentNode.clientWidth + 1;
      const was = bar.parentNode.classList.contains("over");
      bar.parentNode.classList.toggle("over", over);
      if (over && !was) { const on = document.querySelector("[role='tab'][aria-selected='true']"); if (on) { revealTab(on); } }
      prev.hidden = !over || bar.scrollLeft <= 2;
      next.hidden = !over || bar.scrollLeft + bar.clientWidth >= bar.scrollWidth - 2;
    }
    [prev, next].forEach(function (button) {
      button.addEventListener("click", function () { bar.scrollLeft += Number(button.dataset.tabsScroll) * Math.max(120, bar.clientWidth * 0.6); setTimeout(refresh, 400); });
    });
    bar.addEventListener("scroll", refresh);
    window.addEventListener("resize", refresh);
    window.addEventListener("load", refresh);
    refresh();
    setTimeout(refresh, 300);
  })();

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
    const parsed = parseHash();
    if (TAB_IDS.indexOf(parsed.tab) >= 0) { activateTab(parsed.tab, { updateHash: false }); applyHashState(parsed); }
  });

  const startHash = parseHash();
  const hashId = startHash.tab;
  applyHashState(startHash);
  activateTab(TAB_IDS.indexOf(hashId) >= 0 ? hashId : (safeGet(TAB_KEY) || "summary"), { updateHash: TAB_IDS.indexOf(hashId) >= 0 });
  hashReady = true;

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
"""

JS_HEALTH = r"""
  // ---------------- Health alerts, activity badges, contributing repositories and the repository panel ----------------
  // Everything here comes from the JSON embedded in the page (no request leaves the browser); the days are counted here, with today's date, so the page itself
  // never changes only because time passes. Every text is built from the dictionary of the language in use and rebuilt when the language changes.
  var dynReady = false;
  let DATA = { config: {}, repos: {}, contrib: {} };
  try { DATA = JSON.parse(document.getElementById("dashboard-data").textContent); } catch (e) { /* the page still works without it */ }
  const CFG = DATA.config || {};
  const REPO_URL = CFG.repoUrl || "https://github.com/JuanenRac/";
  const GLYPH = { good: "●", warn: "▲", bad: "✕", unknown: "?", none: "–" };

  function dayCount(iso) {
    const t = Date.parse(iso || "");
    return isNaN(t) ? null : Math.max(0, Math.floor((Date.now() - t) / 86400000));
  }
  function levelOf(days, band) {
    if (days === null || !band) { return "unknown"; }
    return days <= band.green_max ? "good" : days <= band.amber_max ? "warn" : "bad";
  }
  function newer(a, b) { return a && b ? (a > b ? a : b) : (a || b || ""); }
  function lastOf(repo) { return newer(repo.commitDate, repo.release && repo.release.date); }
  function make(tag, className, text) {
    const el = document.createElement(tag);
    if (className) { el.className = className; }
    if (text !== undefined) { el.textContent = text; }
    return el;
  }
  function badge(level, text) {
    const el = make("span", "act-badge act-" + level);
    el.appendChild(make("span", "act-glyph", GLYPH[level]));
    el.lastChild.setAttribute("aria-hidden", "true");
    el.appendChild(make("span", "", text));
    return el;
  }

  // The exact UTC moment behind a number of days (the days are whole days elapsed since it, counted in the browser).
  function utcStamp(iso) { return String(iso).replace("T", " ").slice(0, 16) + " UTC"; }

  // ---- Activity badges of the project table ----
  function paintBadges(dict) {
    document.querySelectorAll("td.activity-cell[data-known='1']").forEach(function (cell) {
      const last = cell.getAttribute("data-activity");
      const release = cell.getAttribute("data-release");
      const first = cell.querySelector("[data-kind='activity']");
      const second = cell.querySelector("[data-kind='release']");
      const days = dayCount(last);
      const relDays = dayCount(release);
      const a = days === null ? badge("unknown", dict.not_verified) : badge(levelOf(days, CFG.activity_days), tpl(dict.act_badge, { n: days }));
      const r = !release ? badge("none", dict.rel_none) : relDays === null ? badge("unknown", dict.not_verified) : badge(levelOf(relDays, CFG.release_days), tpl(dict.rel_badge, { n: relDays }));
      first.className = a.className; first.replaceChildren.apply(first, Array.from(a.childNodes));
      second.className = r.className; second.replaceChildren.apply(second, Array.from(r.childNodes));
      first.title = last ? tpl(dict.act_utc, { date: utcStamp(last), n: days === null ? "?" : days }) : "";
      second.title = release ? tpl(dict.rel_utc, { date: utcStamp(release), n: relDays === null ? "?" : relDays }) : "";
    });
  }

  // ---- Health alerts: the static ones come in the page, the ones about days without activity are raised here ----
  function paintAlerts(dict) {
    const card = document.querySelector(".card-alerts");
    const list = document.getElementById("alerts-list");
    if (!card || !list) { return; }
    Array.from(list.querySelectorAll("li[data-kind='inactive'], li[data-kind='unsigned'], li[data-kind='badsig']")).forEach(function (li) { li.remove(); });
    const badSignatures = deliveryBadSignatureAlerts(list, dict);        // a fact, not a threshold: before the alerts that depend on the date
    const limit = CFG.alert_after_days;
    const found = [];
    Object.keys(DATA.repos || {}).forEach(function (name) {
      const last = lastOf(DATA.repos[name]);
      const days = dayCount(last);
      if (last && days !== null && limit && days > limit) { found.push({ name: name, days: days, last: last }); }
    });
    found.sort(function (x, y) { return y.days - x.days || (x.name < y.name ? -1 : 1); });
    found.forEach(function (item) {
      const li = make("li", "alert alert-inactive");
      li.setAttribute("data-kind", "inactive");
      li.setAttribute("data-testid", "alert-inactive");
      const kind = make("span", "alert-kind");
      kind.appendChild(make("span", "alert-glyph", "◷"));
      kind.firstChild.setAttribute("aria-hidden", "true");
      kind.appendChild(make("span", "", dict.alert_kind_inactive));
      const link = make("a", "", item.name);
      link.href = REPO_URL + item.name + "/commits";
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      li.appendChild(kind); li.appendChild(link);
      li.appendChild(make("span", "alert-why", tpl(dict.alert_why_inactive, { n: item.days, date: item.last.slice(0, 10) })));
      list.appendChild(li);
    });
    const total = Number(card.getAttribute("data-static") || "0") + found.length + badSignatures + deliveryUnsignedAlerts(list, dict);
    const incomplete = card.getAttribute("data-incomplete") === "1";
    const state = incomplete ? "incomplete" : total ? "alerts" : "ok";
    card.setAttribute("data-state", state);
    const status = document.getElementById("alerts-status");
    status.className = "alerts-status alerts-" + state;
    status.setAttribute("data-state", state);
    const text = document.getElementById("alerts-status-text");
    const key = state === "ok" ? "alerts_none" : state === "alerts" ? "alerts_some" : total ? "alerts_incomplete_some" : "alerts_incomplete";
    ["data-i18n", "data-i18n-template", "data-n"].forEach(function (name) { text.removeAttribute(name); });
    if (key.slice(-4) === "some") { text.setAttribute("data-i18n-template", key); text.setAttribute("data-n", String(total)); text.textContent = tpl(dict[key], { n: total }); }
    else { text.setAttribute("data-i18n", key); text.textContent = dict[key]; }
    status.firstChild.textContent = state === "ok" ? "●" : state === "alerts" ? "▲" : "?";
  }

  // ---- Which repositories make up a percentage ----
  const openContribs = [];
  function fillContrib(panel, dict) {
    const block = (DATA.contrib || {})[panel.getAttribute("data-eco")];
    const area = panel.getAttribute("data-area");
    panel.textContent = "";
    if (!block) { panel.appendChild(make("p", "no-data", dict.no_data)); return; }
    function item(name, maturity, extra) {
      const li = make("li");
      const link = make("a", "", name);
      link.href = REPO_URL + name; link.target = "_blank"; link.rel = "noopener noreferrer";
      li.appendChild(link);
      li.appendChild(make("span", "contrib-mat", dict["maturity_" + maturity] || dict.unknown));
      if (extra) { li.appendChild(extra); }
      return li;
    }
    function listOf(rows, build) {
      const ul = make("ul", "contrib-list");
      rows.forEach(function (row) { ul.appendChild(build(row)); });
      return ul;
    }
    function scroll(content, label) {
      const box = make("div", "contrib-scroll");
      box.tabIndex = 0; box.setAttribute("role", "region"); box.setAttribute("aria-label", label);
      box.appendChild(content);
      return box;
    }
    const areaName = area === "progress" ? dict.sum_progress_title : dict["area_" + area];
    const label = tpl(dict.contrib_list_label, { name: areaName });
    if (area === "progress") {
      panel.appendChild(make("p", "contrib-head", tpl(dict.contrib_progress_summary, { n: block.progress.length })));
      panel.appendChild(scroll(listOf(block.progress, function (row) {
        const extra = make("span", "contrib-pts", tpl(dict.contrib_points, { p: row[2] }) + (row[3] ? "" : " · " + dict.contrib_partial));
        return item(row[0], row[1], extra);
      }), label));
      return;
    }
    const a = block.areas[area];
    const known = a.yes.length + a.no.length;
    panel.appendChild(make("p", "contrib-head", tpl(dict.contrib_summary, { n: a.yes.length, total: known })));
    if (a.readme && (a.readme[0] !== a.yes.length || a.readme[1] !== known)) {
      panel.appendChild(make("p", "contrib-note", tpl(dict.contrib_readme_diff, { k: a.readme[0], n: a.readme[1] })));
    }
    if (a.yes.length) { panel.appendChild(scroll(listOf(a.yes, function (row) { return item(row[0], row[1]); }), label)); }
    else { panel.appendChild(make("p", "no-data", dict.contrib_none)); }
    [["no", "contrib_no"], ["unknown", "contrib_unknown"]].forEach(function (pair) {
      const rows = a[pair[0]];
      if (!rows.length) { return; }
      const details = make("details", "contrib-more");
      details.appendChild(make("summary", "", tpl(dict[pair[1]], { n: rows.length })));
      details.appendChild(listOf(rows, function (row) { return item(row[0], row[1]); }));
      panel.appendChild(details);
    });
  }
  function toggleContrib(button) {
    const panel = document.getElementById(button.getAttribute("aria-controls"));
    if (!panel) { return; }
    const open = button.getAttribute("aria-expanded") !== "true";
    button.setAttribute("aria-expanded", open ? "true" : "false");
    panel.hidden = !open;
    const at = openContribs.indexOf(panel);
    if (at >= 0) { openContribs.splice(at, 1); }
    if (open) {
      panel.setAttribute("data-eco", button.getAttribute("data-contrib-eco"));
      panel.setAttribute("data-area", button.getAttribute("data-contrib-area"));
      openContribs.push(panel);
      fillContrib(panel, currentDict());
    }
  }
  document.querySelectorAll("button[data-contrib-area]").forEach(function (button) { button.addEventListener("click", function () { toggleContrib(button); }); });
  document.querySelectorAll(".area-bar").forEach(function (bar) {
    bar.addEventListener("click", function () { const button = bar.closest("li.area").querySelector("button[data-contrib-area]"); if (button) { toggleContrib(button); } });
  });
  document.querySelectorAll(".ring-wrap").forEach(function (ring) {
    ring.addEventListener("click", function () { const button = ring.closest("article").querySelector("button.contrib-toggle"); if (button) { toggleContrib(button); } });
  });

  // ---- The panel of a repository ----
  const repoPanel = document.getElementById("repo-panel");
  const panelTitle = document.getElementById("repo-panel-title");
  let panelFor = null;
  let panelOpener = null;

  function renderPanel(dict) {
    const repo = DATA.repos[panelFor];
    if (!repo) { return; }
    panelTitle.textContent = panelFor;
    const fields = document.getElementById("repo-fields");
    fields.textContent = "";
    function field(label, value) {
      fields.appendChild(make("dt", "", label));
      fields.appendChild(make("dd", "", value === "" || value === null || value === undefined ? dict.not_verified : value));
    }
    const lastDate = lastOf(repo);
    const lastDays = dayCount(lastDate);
    field(dict.panel_f_ecosystem, repo.ecoLabel);
    field(dict.th_version, repo.version);
    field(dict.th_maturity, dict["maturity_" + repo.maturity] || repo.maturity);
    field(dict.panel_f_evidence, repo.evidence ? (dict["evidence_" + repo.evidence] || repo.evidence) : dict.not_verified);
    field(dict.th_type, repo.roleKey ? dict["role_" + repo.roleKey] : repo.role);
    field(dict.th_stack, repo.stack);
    field(dict.th_deploy, repo.deployKey ? dict["deploy_" + repo.deployKey] : repo.deploy);
    if (repo.family) { field(dict.panel_f_family, repo.family); }
    if (repo.parent) { field(dict.panel_f_parent, repo.parent); }
    field(dict.panel_f_hardware, repo.hardware === true ? dict.panel_hw_yes : repo.hardware === false ? dict.panel_hw_no : dict.panel_hw_unset);
    field(dict.panel_f_activity, lastDate ? lastDate.slice(0, 10) + " · " + tpl(dict.act_badge, { n: lastDays }) : null);
    field(dict.panel_f_release, repo.release ? repo.release.tag + (repo.release.date ? " · " + repo.release.date.slice(0, 10) : "") : repo.known ? dict.rel_none : null);
    field(dict.ts_panel_field, tsPanelText(panelFor, dict));

    const ci = document.getElementById("rp-ci");
    ci.textContent = "";
    if (!repo.known) { ci.textContent = dict.not_verified; }
    else {
      const level = repo.ci === "success" ? "good" : repo.ci === "failure" ? "bad" : repo.ci === "pending" ? "warn" : "none";
      ci.appendChild(badge(level, dict["ci_" + repo.ci] || dict.not_verified));
    }
    const commits = document.getElementById("rp-commits");
    const none = document.getElementById("rp-commits-none");
    commits.textContent = "";
    const list = repo.commits || [];
    none.hidden = list.length > 0;
    list.forEach(function (c) {
      const li = make("li");
      const link = make("a", "", c[0]);
      if (c[2]) { link.href = c[2]; link.target = "_blank"; link.rel = "noopener noreferrer"; }
      li.appendChild(c[2] ? link : make("span", "", c[0]));
      if (c[1]) { const t = make("time", "", c[1].slice(0, 10)); t.setAttribute("datetime", c[1]); li.appendChild(t); }
      commits.appendChild(li);
    });
    const base = REPO_URL + panelFor;
    repoPanel.querySelectorAll("[data-link]").forEach(function (a) {
      const kind = a.getAttribute("data-link");
      a.href = kind === "readme" ? base + "#readme" : base + "/" + kind;
    });
    evPanel(panelFor, dict);
    deliveryPanel(panelFor, dict);
  }
  function openPanel(name, opener) {
    if (!DATA.repos[name]) { return; }
    panelFor = name;
    navRepo = name;
    panelOpener = opener || null;
    repoPanel.hidden = false;
    renderPanel(currentDict());
    panelTitle.focus();
    if (hashReady) { writeHash(); }
    if (crumbRefresh) { crumbRefresh(); }
  }
  function closePanel() {
    if (repoPanel.hidden) { return; }
    repoPanel.hidden = true;
    panelFor = null;
    navRepo = null;
    if (hashReady) { writeHash(); }
    if (crumbRefresh) { crumbRefresh(); }
    const back = panelOpener && document.contains(panelOpener) && panelOpener.offsetParent !== null ? panelOpener : document.getElementById("main");
    panelOpener = null;
    if (back) { back.focus(); }
  }
  document.querySelectorAll("button[data-open-repo]").forEach(function (button) {
    button.addEventListener("click", function () { openPanel(button.getAttribute("data-open-repo"), button); });
  });
  document.querySelectorAll("tr.project-row").forEach(function (row) {
    row.addEventListener("click", function (event) {
      if (event.target.closest("a, button, input, select, textarea, summary")) { return; }
      const button = row.querySelector("button[data-open-repo]");
      if (button) { openPanel(button.getAttribute("data-open-repo"), button); }
    });
  });
  document.getElementById("repo-panel-close").addEventListener("click", closePanel);
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !repoPanel.hidden) { event.preventDefault(); closePanel(); }
  });

  function onLanguageApplied(dict) {
    if (!dynReady) { return; }
    paintBadges(dict);
    paintAlerts(dict);
    openContribs.forEach(function (panel) { fillContrib(panel, dict); });
    if (panelFor) { renderPanel(dict); }
    evoApplied(dict);
    rackApplied(dict);
    deliveryApplied(dict);
    if (crumbRefresh) { crumbRefresh(dict); }
  }
  // The thermal verdict inside an alarm of the rack is a code the snapshot carries: it is translated here, in the sentence of the alarm.
  function rackApplied(dict) {
    document.querySelectorAll("li[data-verdict-key]").forEach(function (li) {
      const verdict = dict[li.getAttribute("data-verdict-key")] || li.getAttribute("data-verdict") || "";
      li.textContent = tpl(dict.rack_alarm_thermal, { slot: li.getAttribute("data-slot"), verdict: verdict });
    });
  }
  dynReady = true;
  applyLanguage(langSelect ? langSelect.value : resolveInitialLang());
"""

CSS = CSS + dashboard_ci_ui.CSS + dashboard_tests_ui.CSS + dashboard_actions_ui.CSS + dashboard_evo_ui.CSS + dashboard_insight_ui.CSS + dashboard_nav_ui.CSS + dashboard_delivery_ui.CSS + r"""
  /* ======================= Last known data, generation figures, manifest health and rack ======================= */
  .stale-banner { grid-column: 1 / -1; margin: 0; padding: 10px 14px; border: 1px solid var(--k-pending); border-left-width: 6px; border-radius: var(--radius); background: var(--panel-2); color: var(--text); font-weight: 600; }
  .stale-glyph { color: var(--k-pending); margin-right: 6px; }
  .card-gen { margin-bottom: 14px; }
  .gen-steps { margin: 6px 0 10px; padding-left: 18px; display: grid; gap: 2px; font-size: 13px; }
  .kpi-registry .kpi-drop-panel { left: auto; right: 0; width: min(520px, 90vw); border-color: var(--border-strong); }
  .kpi-registry .kpi-drop-panel p { margin: 0; font-size: 12.5px; line-height: 1.45; }
  .rack-state { display: inline-flex; gap: 8px; align-items: center; margin: 0 0 6px; font-weight: 700; padding: 4px 10px; border: 1px solid var(--border-strong); border-radius: 999px; }
  .rack-glyph { font-size: 14px; }
  .rack-state[data-state="alarm"] .rack-glyph { color: var(--err); }
  .rack-state[data-state="ok"] .rack-glyph { color: var(--ok); }
  .rack-sub { margin: 14px 0 6px; font-size: 13px; }
  .rack-sim { margin: 4px 0; padding: 6px 10px; border-left: 4px solid var(--k-pending); background: var(--panel-2); border-radius: 6px; }
  .rack-scroll { overflow-x: auto; }
  .rack-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .rack-table th, .rack-table td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); }
  .rack-table thead th { color: var(--dim); font-size: 11px; letter-spacing: .08em; text-transform: uppercase; }
  .rack-flag { font-weight: 700; color: var(--err); }
  .rack-alarms { margin: 0; padding-left: 18px; display: grid; gap: 3px; font-size: 13px; }
"""


def script() -> str:
    """The filters and the shell, ready to be placed inside the page's own script."""
    import json
    marker = "  dynReady = true;\n  applyLanguage("
    assert JS_HEALTH.count(marker) == 1
    return JS_FILTERS + JS.replace("__TAB_IDS__", json.dumps(list(TAB_IDS))) + JS_HEALTH.replace(marker, dashboard_ci_ui.JS + dashboard_tests_ui.JS + dashboard_actions_ui.JS + dashboard_evo_ui.JS + dashboard_insight_ui.JS + dashboard_nav_ui.JS + dashboard_delivery_ui.JS + marker)


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
        '<div class="architecture-flow" aria-label="EH3D flow" data-i18n-aria-label="aria_eh3d_flow"><span data-i18n="architecture_e_flow_1">Gerber, Excellon and images</span><b>→</b>'
        '<span data-i18n="architecture_e_flow_2">Parsers and CAM tools</span><b>→</b><span data-i18n="architecture_e_flow_3">G-code and simulation</span><b>→</b>'
        '<span data-i18n="architecture_e_flow_4">Machine</span></div>'
        f'<div class="relationship-note"><strong data-i18n="architecture_e_rel_title">{esc(en["architecture_e_rel_title"])}</strong> '
        f'<span data-i18n="architecture_e_rel_body">{esc(en["architecture_e_rel_body"])}</span></div></section>'
    )
