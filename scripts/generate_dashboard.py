#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - scripts/generate_dashboard.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Generates docs/index.html - a static ecosystem status dashboard.
#
# The dashboard deliberately reuses HYDRA-UMC-UPDATER's:
#
#   - registry.py
#   - github_client.py
#   - version_parse.py
#
# instead of maintaining another project registry or another version parser.
#
# The generated page is completely static and therefore works directly from
# GitHub Pages without a backend/server.
#
# Dashboard features:
#
#   - ecosystem-wide project count
#   - successful version lookups
#   - failed lookups
#   - success percentage
#   - deployment target statistics
#   - project stack
#   - project version
#   - detailed error status
#   - project search
#   - deployment filters
#   - health/status filters
#   - direct links to repository / Actions / Issues
#
# IMPORTANT:
#
# No generation timestamp is written into the HTML. This prevents the daily
# scheduled workflow from producing an unnecessary Git commit when nothing
# actually changed.
# =============================================================================

from __future__ import annotations

import html
import sys
from pathlib import Path

from hydra_umc_updater.github_client import RemoteStatus, fetch_all
from hydra_umc_updater.registry import PROJECTS


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

OUT_DIR = Path(__file__).resolve().parent.parent / "docs"


# ---------------------------------------------------------------------------
# Deployment labels
# ---------------------------------------------------------------------------

DEPLOY_LABELS = {
    "cm5": "CM5",
    "user-pc": "User PC",
    "mobile": "Mobile",
    "wearable": "Wearable",
}

DEPLOY_ORDER = [
    "cm5",
    "user-pc",
    "mobile",
    "wearable",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(value: object) -> str:
    """HTML-escape a value before inserting it into generated HTML."""
    return html.escape(str(value), quote=True)


def repo_url(name: str) -> str:
    return f"https://github.com/JuanenRac/{name}"


def actions_url(name: str) -> str:
    return f"https://github.com/JuanenRac/{name}/actions"


def issues_url(name: str) -> str:
    return f"https://github.com/JuanenRac/{name}/issues"


def status_for(result: RemoteStatus | None) -> tuple[str, str, str]:
    """
    Return:

        status key
        human label
        CSS class

    Statuses:

        ok
        error
    """

    if result is not None and result.version is not None:
        return "ok", "OK", "status-ok"

    return "error", "ERROR", "status-error"


def error_text(result: RemoteStatus | None) -> str:
    """Return a human-readable error description."""

    if result is None:
        return "No result returned"

    if result.error:
        return result.error

    return "Version unavailable"


# ---------------------------------------------------------------------------
# Project rows
# ---------------------------------------------------------------------------

def render_project_rows(results: dict[str, RemoteStatus]) -> str:
    rows: list[str] = []

    for entry in PROJECTS:
        result = results.get(entry.name)

        status_key, status_label, status_class = status_for(result)

        if result and result.version is not None:
            version = str(result.version)
            detail = "Version successfully resolved"
        else:
            version = "—"
            detail = error_text(result)

        deploy_key = entry.deploy
        deploy_label = DEPLOY_LABELS.get(
            deploy_key,
            deploy_key,
        )

        project_name = esc(entry.name)
        stack = esc(entry.stack)
        deploy = esc(deploy_label)
        deploy_filter = esc(deploy_key)

        version_html = esc(version)
        detail_html = esc(detail)

        project_repo = esc(repo_url(entry.name))
        project_actions = esc(actions_url(entry.name))
        project_issues = esc(issues_url(entry.name))

        rows.append(
            f"""
            <tr
                class="project-row {status_class}"
                data-name="{project_name.lower()}"
                data-status="{esc(status_key)}"
                data-deploy="{deploy_filter}"
                data-stack="{stack.lower()}"
            >
              <td class="project-name">
                <div class="project-title">
                  <a
                    href="{project_repo}"
                    target="_blank"
                    rel="noopener noreferrer"
                  >{project_name}</a>
                </div>

                <div class="project-links">
                  <a
                    href="{project_actions}"
                    target="_blank"
                    rel="noopener noreferrer"
                  >Actions</a>

                  <a
                    href="{project_issues}"
                    target="_blank"
                    rel="noopener noreferrer"
                  >Issues</a>
                </div>
              </td>

              <td class="stack">
                {stack}
              </td>

              <td class="deploy">
                <span class="deploy-badge">
                  {deploy}
                </span>
              </td>

              <td class="version {status_class}">
                {version_html}
              </td>

              <td class="status-cell">
                <span class="status-badge {status_class}">
                  <span class="status-dot"></span>
                  {esc(status_label)}
                </span>

                <div class="status-detail">
                  {detail_html}
                </div>
              </td>
            </tr>
            """
        )

    return "".join(rows)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def calculate_statistics(
    results: dict[str, RemoteStatus],
) -> dict[str, object]:
    total = len(PROJECTS)

    ok = sum(
        1
        for entry in PROJECTS
        if results.get(entry.name)
        and results[entry.name].version is not None
    )

    errors = total - ok

    success_percent = (
        round((ok / total) * 100, 1)
        if total
        else 0.0
    )

    deploy_counts = {
        key: 0
        for key in DEPLOY_ORDER
    }

    stack_counts: dict[str, int] = {}

    for entry in PROJECTS:
        deploy_counts[entry.deploy] = (
            deploy_counts.get(entry.deploy, 0) + 1
        )

        stack_counts[entry.stack] = (
            stack_counts.get(entry.stack, 0) + 1
        )

    return {
        "total": total,
        "ok": ok,
        "errors": errors,
        "success_percent": success_percent,
        "deploy_counts": deploy_counts,
        "stack_counts": stack_counts,
    }


# ---------------------------------------------------------------------------
# Deployment cards
# ---------------------------------------------------------------------------

def render_deploy_cards(
    deploy_counts: dict[str, int],
) -> str:
    cards: list[str] = []

    for key in DEPLOY_ORDER:
        label = DEPLOY_LABELS.get(
            key,
            key,
        )

        count = deploy_counts.get(
            key,
            0,
        )

        cards.append(
            f"""
            <button
                class="deploy-card"
                type="button"
                data-filter-deploy="{esc(key)}"
            >
              <span class="deploy-count">
                {count}
              </span>

              <span class="deploy-label">
                {esc(label)}
              </span>
            </button>
            """
        )

    return "".join(cards)


# ---------------------------------------------------------------------------
# Stack cards
# ---------------------------------------------------------------------------

def render_stack_summary(
    stack_counts: dict[str, int],
) -> str:
    items = sorted(
        stack_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return "".join(
        f"""
        <div class="stack-item">
          <span>{esc(stack)}</span>
          <strong>{count}</strong>
        </div>
        """
        for stack, count in items
    )


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def render_html(
    results: dict[str, RemoteStatus],
) -> str:
    stats = calculate_statistics(results)

    total = int(stats["total"])
    ok = int(stats["ok"])
    errors = int(stats["errors"])
    success_percent = float(stats["success_percent"])

    deploy_counts = stats["deploy_counts"]
    stack_counts = stats["stack_counts"]

    rows = render_project_rows(results)

    deploy_cards = render_deploy_cards(
        deploy_counts,
    )

    stack_summary = render_stack_summary(
        stack_counts,
    )

    success_percent_text = (
        f"{success_percent:g}%"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta
  name="viewport"
  content="width=device-width, initial-scale=1"
>

<meta
  name="description"
  content="HYDRA-UMC / URTC ecosystem status dashboard"
>

<title>HYDRA-UMC / URTC Ecosystem Status</title>

<link
  rel="preconnect"
  href="https://fonts.googleapis.com"
>

<link
  rel="preconnect"
  href="https://fonts.gstatic.com"
  crossorigin
>

<link
  href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"
  rel="stylesheet"
>

<style>
  :root {{
    --bg: #f4f6f9;
    --surface: #ffffff;
    --surface-2: #f8fafc;
    --border: #dde3ea;
    --border-strong: #cbd5e1;
    --text: #16202c;
    --dim: #64748b;
    --accent: #0284c7;
    --accent-soft: #e0f2fe;
    --ok: #059669;
    --ok-soft: #d1fae5;
    --err: #e11d48;
    --err-soft: #ffe4e6;
    --shadow: 0 4px 18px rgba(15, 23, 42, .06);
  }}

  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #0a0e13;
      --surface: #10151d;
      --surface-2: #151c26;
      --border: #232c39;
      --border-strong: #334155;
      --text: #e8eef5;
      --dim: #93a3b8;
      --accent: #38bdf8;
      --accent-soft: #082f49;
      --ok: #34d399;
      --ok-soft: #064e3b;
      --err: #fb7185;
      --err-soft: #4c0519;
      --shadow: 0 4px 18px rgba(0, 0, 0, .25);
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  html {{
    scroll-behavior: smooth;
  }}

  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family:
      "IBM Plex Sans",
      system-ui,
      sans-serif;
  }}

  a {{
    color: var(--accent);
  }}

  button,
  input {{
    font: inherit;
  }}

  .wrap {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 36px 20px 80px;
  }}

  .header {{
    margin-bottom: 28px;
  }}

  .eyebrow {{
    color: var(--accent);
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  h1 {{
    font-family: "IBM Plex Mono", monospace;
    font-size: clamp(24px, 4vw, 34px);
    line-height: 1.15;
    margin: 0 0 8px;
  }}

  .subtitle {{
    color: var(--dim);
    margin: 0;
    font-size: 14px;
    line-height: 1.6;
  }}

  .subtitle a {{
    color: var(--accent);
    text-decoration: none;
  }}

  .subtitle a:hover {{
    text-decoration: underline;
  }}

  .health {{
    display: grid;
    grid-template-columns:
      repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
  }}

  .health-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    box-shadow: var(--shadow);
  }}

  .health-card .number {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 27px;
    font-weight: 700;
    line-height: 1;
  }}

  .health-card .label {{
    color: var(--dim);
    font-size: 12px;
    margin-top: 7px;
  }}

  .health-card.ok {{
    border-color: color-mix(
      in srgb,
      var(--ok) 35%,
      var(--border)
    );
  }}

  .health-card.error {{
    border-color: color-mix(
      in srgb,
      var(--err) 35%,
      var(--border)
    );
  }}

  .section {{
    margin-top: 24px;
  }}

  .section-title {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
  }}

  .deploy-grid {{
    display: grid;
    grid-template-columns:
      repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
  }}

  .deploy-card {{
    appearance: none;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    border-radius: 9px;
    padding: 13px 15px;
    text-align: left;
    cursor: pointer;
    box-shadow: var(--shadow);
    transition:
      border-color .15s ease,
      transform .15s ease;
  }}

  .deploy-card:hover {{
    border-color: var(--accent);
    transform: translateY(-1px);
  }}

  .deploy-card.active {{
    border-color: var(--accent);
    box-shadow:
      0 0 0 2px var(--accent-soft);
  }}

  .deploy-count {{
    display: block;
    font-family: "IBM Plex Mono", monospace;
    font-size: 21px;
    font-weight: 700;
  }}

  .deploy-label {{
    display: block;
    color: var(--dim);
    font-size: 12px;
    margin-top: 4px;
  }}

  .stack-summary {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
  }}

  .stack-item {{
    display: flex;
    align-items: center;
    gap: 9px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 10px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
  }}

  .stack-item strong {{
    color: var(--accent);
  }}

  .toolbar {{
    margin-top: 28px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
  }}

  .search {{
    flex: 1 1 300px;
  }}

  .search input {{
    width: 100%;
    padding: 11px 13px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--surface);
    color: var(--text);
    outline: none;
  }}

  .search input:focus {{
    border-color: var(--accent);
    box-shadow:
      0 0 0 3px var(--accent-soft);
  }}

  .filters {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
  }}

  .filter {{
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--dim);
    border-radius: 7px;
    padding: 8px 11px;
    cursor: pointer;
    font-size: 12px;
  }}

  .filter:hover {{
    color: var(--text);
    border-color: var(--accent);
  }}

  .filter.active {{
    color: var(--accent);
    border-color: var(--accent);
    background: var(--accent-soft);
  }}

  .table-wrapper {{
    margin-top: 14px;
    overflow-x: auto;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    box-shadow: var(--shadow);
  }}

  table {{
    width: 100%;
    min-width: 900px;
    border-collapse: collapse;
  }}

  th {{
    text-align: left;
    white-space: nowrap;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: var(--dim);
    padding: 11px 14px;
    border-bottom: 1px solid var(--border);
    background: var(--surface-2);
  }}

  td {{
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    vertical-align: top;
  }}

  tr:last-child td {{
    border-bottom: none;
  }}

  tr.project-row:hover td {{
    background: var(--surface-2);
  }}

  tr.project-row.hidden {{
    display: none;
  }}

  .project-title a {{
    color: var(--accent);
    font-weight: 600;
    text-decoration: none;
  }}

  .project-title a:hover {{
    text-decoration: underline;
  }}

  .project-links {{
    display: flex;
    gap: 9px;
    margin-top: 5px;
  }}

  .project-links a {{
    color: var(--dim);
    font-size: 10px;
    text-decoration: none;
  }}

  .project-links a:hover {{
    color: var(--accent);
  }}

  .stack {{
    color: var(--dim);
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
  }}

  .deploy {{
    white-space: nowrap;
  }}

  .deploy-badge {{
    display: inline-block;
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 4px 7px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 10px;
    color: var(--dim);
  }}

  .version {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
  }}

  .version.status-ok {{
    color: var(--ok);
  }}

  .version.status-error {{
    color: var(--err);
  }}

  .status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 999px;
    padding: 4px 8px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 10px;
    font-weight: 700;
  }}

  .status-badge.status-ok {{
    color: var(--ok);
    background: var(--ok-soft);
  }}

  .status-badge.status-error {{
    color: var(--err);
    background: var(--err-soft);
  }}

  .status-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
  }}

  .status-detail {{
    color: var(--dim);
    font-size: 10px;
    margin-top: 5px;
    max-width: 260px;
    line-height: 1.4;
  }}

  .empty {{
    display: none;
    padding: 30px;
    text-align: center;
    color: var(--dim);
    font-size: 13px;
  }}

  footer {{
    margin-top: 28px;
    color: var(--dim);
    font-size: 11px;
    line-height: 1.6;
  }}

  footer a {{
    color: var(--accent);
    text-decoration: none;
  }}

  footer a:hover {{
    text-decoration: underline;
  }}

  @media (max-width: 700px) {{
    .wrap {{
      padding: 25px 12px 60px;
    }}

    .health {{
      grid-template-columns:
        repeat(2, minmax(0, 1fr));
    }}

    .toolbar {{
      align-items: stretch;
    }}

    .filters {{
      width: 100%;
    }}
  }}
</style>
</head>

<body>

<div class="wrap">

  <header class="header">
    <div class="eyebrow">
      HYDRA-UMC / URTC ECOSYSTEM
    </div>

    <h1>
      Ecosystem Status Dashboard
    </h1>

    <p class="subtitle">
      {ok}/{total} repositories resolved successfully
      · {success_percent_text} healthy
      · versions are read from each project's own source file
      · dashboard generated by GitHub Actions
      · static GitHub Pages
    </p>
  </header>


  <!-- ================================================================
       HEALTH
       ================================================================ -->

  <section class="health">

    <div class="health-card">
      <div class="number">
        {total}
      </div>
      <div class="label">
        Total projects
      </div>
    </div>

    <div class="health-card ok">
      <div class="number">
        {ok}
      </div>
      <div class="label">
        Version resolved
      </div>
    </div>

    <div class="health-card error">
      <div class="number">
        {errors}
      </div>
      <div class="label">
        Errors / unknown
      </div>
    </div>

    <div class="health-card">
      <div class="number">
        {success_percent_text}
      </div>
      <div class="label">
        Registry health
      </div>
    </div>

  </section>


  <!-- ================================================================
       DEPLOYMENT
       ================================================================ -->

  <section class="section">

    <div class="section-title">
      Deployment targets
    </div>

    <div class="deploy-grid">
      {deploy_cards}
    </div>

  </section>


  <!-- ================================================================
       STACK SUMMARY
       ================================================================ -->

  <section class="section">

    <div class="section-title">
      Technology stacks
    </div>

    <div class="stack-summary">
      {stack_summary}
    </div>

  </section>


  <!-- ================================================================
       SEARCH / FILTERS
       ================================================================ -->

  <section class="toolbar">

    <div class="search">
      <input
        id="project-search"
        type="search"
        placeholder="Search project, stack or deployment..."
        autocomplete="off"
        aria-label="Search projects"
      >
    </div>

    <div class="filters">

      <button
        class="filter active"
        type="button"
        data-filter-status="all"
      >
        All
      </button>

      <button
        class="filter"
        type="button"
        data-filter-status="ok"
      >
        ✓ OK
      </button>

      <button
        class="filter"
        type="button"
        data-filter-status="error"
      >
        ⚠ Errors
      </button>

    </div>

  </section>


  <!-- ================================================================
       PROJECT TABLE
       ================================================================ -->

  <section class="table-wrapper">

    <table>

      <thead>
        <tr>
          <th>Project</th>
          <th>Stack</th>
          <th>Deploy target</th>
          <th>Version</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody id="project-table">
        {rows}
      </tbody>

    </table>

    <div
      id="empty-results"
      class="empty"
    >
      No projects match the current filters.
    </div>

  </section>


  <!-- ================================================================
       FOOTER
       ================================================================ -->

  <footer>

    Registry source:
    <a
      href="https://github.com/JuanenRac/HYDRA-UMC-UPDATER"
      target="_blank"
      rel="noopener noreferrer"
    >
      HYDRA-UMC-UPDATER
    </a>

    ·

    Dashboard generator:
    <a
      href="https://github.com/JuanenRac/JuanenRac/blob/main/scripts/generate_dashboard.py"
      target="_blank"
      rel="noopener noreferrer"
    >
      generate_dashboard.py
    </a>

    ·

    Workflow:
    <a
      href="https://github.com/JuanenRac/JuanenRac/blob/main/.github/workflows/build-dashboard.yml"
      target="_blank"
      rel="noopener noreferrer"
    >
      build-dashboard.yml
    </a>

    ·

    The registry remains the single source of truth for project/version
    locations.

  </footer>

</div>


<script>
(function () {{
  "use strict";

  const rows = Array.from(
    document.querySelectorAll(".project-row")
  );

  const searchInput =
    document.getElementById("project-search");

  const emptyResults =
    document.getElementById("empty-results");

  const statusFilters =
    Array.from(
      document.querySelectorAll("[data-filter-status]")
    );

  const deployFilters =
    Array.from(
      document.querySelectorAll("[data-filter-deploy]")
    );

  let activeStatus = "all";
  let activeDeploy = "all";


  function applyFilters() {{
    const query =
      searchInput.value
        .trim()
        .toLowerCase();

    let visible = 0;

    rows.forEach(function (row) {{
      const name =
        row.dataset.name || "";

      const status =
        row.dataset.status || "";

      const deploy =
        row.dataset.deploy || "";

      const stack =
        row.dataset.stack || "";

      const matchesSearch =
        !query ||
        name.includes(query) ||
        stack.includes(query) ||
        deploy.includes(query);

      const matchesStatus =
        activeStatus === "all" ||
        status === activeStatus;

      const matchesDeploy =
        activeDeploy === "all" ||
        deploy === activeDeploy;

      const show =
        matchesSearch &&
        matchesStatus &&
        matchesDeploy;

      row.classList.toggle(
        "hidden",
        !show
      );

      if (show) {{
        visible += 1;
      }}
    }});

    emptyResults.style.display =
      visible === 0
        ? "block"
        : "none";
  }}


  searchInput.addEventListener(
    "input",
    applyFilters
  );


  statusFilters.forEach(function (button) {{
    button.addEventListener(
      "click",
      function () {{

        activeStatus =
          button.dataset.filterStatus;

        statusFilters.forEach(
          function (item) {{
            item.classList.toggle(
              "active",
              item === button
            );
          }}
        );

        applyFilters();
      }}
    );
  }});


  deployFilters.forEach(function (button) {{
    button.addEventListener(
      "click",
      function () {{

        const selected =
          button.dataset.filterDeploy;

        if (activeDeploy === selected) {{
          activeDeploy = "all";
          button.classList.remove("active");
        }} else {{
          activeDeploy = selected;

          deployFilters.forEach(
            function (item) {{
              item.classList.toggle(
                "active",
                item === button
              );
            }}
          );
        }}

        applyFilters();
      }}
    );
  }});


  applyFilters();

}})();
</script>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    total = len(PROJECTS)

    print(
        f"Fetching latest GitHub version for "
        f"{total} projects...",
        file=sys.stderr,
    )

    results = fetch_all(PROJECTS)

    ok = sum(
        1
        for result in results.values()
        if result.version is not None
    )

    errors = total - ok

    print(
        f"{ok}/{total} resolved "
        f"({errors} errors/unknown).",
        file=sys.stderr,
    )

    # Print failures individually. This makes the GitHub Actions log useful
    # even before someone opens the generated dashboard.
    if errors:
        print(
            "\nUnresolved projects:",
            file=sys.stderr,
        )

        for entry in PROJECTS:
            result = results.get(entry.name)

            if result is None or result.version is None:
                print(
                    f"  - {entry.name}: "
                    f"{error_text(result)}",
                    file=sys.stderr,
                )

    OUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    index_path = OUT_DIR / "index.html"

    index_path.write_text(
        render_html(results),
        encoding="utf-8",
    )

    # Tell GitHub Pages that this is plain static HTML.
    (OUT_DIR / ".nojekyll").touch()

    print(
        f"Wrote {index_path}",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())