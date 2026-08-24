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
#   - project stack (with a small stack icon)
#   - project version
#   - detailed error status
#   - latest commit subject per project (api.github.com, best-effort)
#   - project search
#   - deployment filters
#   - health/status filters
#   - manual dark/light theme toggle (remembered via localStorage)
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
import json
import os
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from hydra_umc_updater.github_client import RemoteStatus, fetch_all
from hydra_umc_updater.registry import PROJECTS


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

OUT_DIR = Path(__file__).resolve().parent.parent / "docs"


# ---------------------------------------------------------------------------
# GitHub REST metadata (latest commit subject per project)
# ---------------------------------------------------------------------------
#
# The version lookup above (fetch_all) reads raw.githubusercontent.com,
# which is not part of the GitHub REST API and is not meaningfully
# rate-limited. Commit messages, by contrast, only exist through
# api.github.com, which enforces a real 60 requests/hour limit for
# unauthenticated calls - far too low for 45 repos.
#
# GITHUB_TOKEN is the same token GitHub Actions already injects into every
# workflow run for the repo the workflow lives in. It has no special access
# to any of the OTHER 45 repos - it is used here purely as authentication to
# raise api.github.com's rate limit (an authenticated request gets ~5000/hour
# regardless of which repo it targets, as long as the data being read is
# public, which every project in this ecosystem is). If the token is absent
# (e.g. a local run outside CI), the calls still work, just capped at the
# public 60/hour ceiling - this whole feature degrades to "no metadata shown"
# rather than failing the build.
#
# A per-repo "last build time" (from each repo's own Actions runs) was
# tried and dropped: checked for real against the live GitHub API and none
# of the 45 project repos run their own Actions workflows (only this
# dashboard's own JuanenRac repo does) - every row would have shown "-"
# forever, which is worse than not having the column.
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

API_REQUEST_TIMEOUT_S = 10

API_MAX_CONCURRENT_REQUESTS = 8

API_USER_AGENT = "JuanenRac-dashboard"


@dataclass
class RepoMeta:
    """
    Extra, best-effort metadata for one project, shown alongside its
    version status. Both fields are None when the lookup failed or was
    skipped - the dashboard renders that as "-", the same convention
    already used for a failed version lookup.

    Note: an earlier version of this also tracked each repo's latest
    Actions run duration ("build time"). It was removed after checking
    real data: none of the 45 project repos run their own Actions
    workflows (only this dashboard's own JuanenRac repo does) - every
    row would have shown "-" forever, which is worse than not having the
    column. Commit metadata, checked the same way, does return real data
    for every public repo, so it stayed.
    """

    commit_subject: str | None = None
    commit_url: str | None = None


def _api_get(url: str) -> dict | list | None:
    """
    GET one api.github.com JSON endpoint. Returns None on any failure
    (network error, rate limit, 404, malformed JSON, ...) - metadata is
    optional decoration, never something that should abort the dashboard
    build.
    """

    headers = {
        "User-Agent": API_USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    request = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(
            request,
            timeout=API_REQUEST_TIMEOUT_S,
        ) as response:
            raw = response.read()

        return json.loads(raw.decode("utf-8", errors="replace"))

    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        socket.timeout,
        OSError,
        json.JSONDecodeError,
    ):
        return None


def _fetch_one_meta(repo_name: str) -> RepoMeta:
    meta = RepoMeta()

    # --- Latest commit on the default branch --------------------------
    commits = _api_get(
        f"https://api.github.com/repos/JuanenRac/{repo_name}/commits"
        f"?per_page=1"
    )

    if isinstance(commits, list) and commits:
        commit = commits[0]

        message = (
            commit.get("commit", {})
            .get("message", "")
            .strip()
        )

        if message:
            # First line only - a commit body is not meant for one table row.
            meta.commit_subject = message.splitlines()[0][:120]
            meta.commit_url = commit.get("html_url")

    return meta


def fetch_all_meta(
    entries: list,
    progress=None,
) -> dict[str, RepoMeta]:
    """
    Fetch commit metadata for every given registry entry, concurrently.
    Mirrors hydra_umc_updater.github_client.fetch_all's own shape (same
    concurrency cap, same "never raise, always return a result" contract)
    so the two data sources behave consistently.
    """

    results: dict[str, RepoMeta] = {}

    total = len(entries)
    done = 0

    if total == 0:
        return results

    with ThreadPoolExecutor(
        max_workers=API_MAX_CONCURRENT_REQUESTS,
        thread_name_prefix="dashboard-meta",
    ) as pool:

        futures = {
            pool.submit(_fetch_one_meta, entry.name): entry
            for entry in entries
        }

        for future in as_completed(futures):
            entry = futures[future]

            try:
                meta = future.result()

            except Exception:
                meta = RepoMeta()

            results[entry.name] = meta

            done += 1

            if progress is not None:
                progress(done, total)

    return results


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
# Icons
# ---------------------------------------------------------------------------
#
# Small inline glyphs (24x24 viewBox, single `currentColor` stroke) for each
# technology stack and deployment target. Inlined directly rather than
# fetched, so the dashboard stays a single static file with no extra
# requests. They intentionally do not reproduce any project's real logo -
# generic, license-free shapes loosely evoking each stack (a chip for
# firmware, a hexagon for Node, a gear for Rust, ...) rather than trademarked
# marks.
# ---------------------------------------------------------------------------

STACK_ICONS: dict[str, str] = {
    "firmware-c": (
        '<path d="M9 2v3M12 2v3M15 2v3M9 19v3M12 19v3M15 19v3'
        'M2 9h3M2 12h3M2 15h3M19 9h3M19 12h3M19 15h3"/>'
        '<rect x="6" y="6" width="12" height="12" rx="2"/>'
        '<rect x="9.5" y="9.5" width="5" height="5" rx="1"/>'
    ),
    "python": (
        '<path d="M12 2 21 7v10l-9 5-9-5V7l9-5Z"/>'
        '<path d="M3 7l9 5 9-5M12 12v9"/>'
    ),
    "node": (
        '<path d="M12 2 21 7v10l-9 5-9-5V7l9-5Z"/>'
    ),
    "rust": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M12 2v3M12 19v3M2 12h3M19 12h3'
        'M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/>'
    ),
    "go": (
        '<rect x="3" y="4" width="18" height="16" rx="2"/>'
        '<path d="M7 9l3 3-3 3M13 15h4"/>'
    ),
    "android": (
        '<rect x="7" y="2" width="10" height="20" rx="2"/>'
        '<path d="M11 18h2"/>'
    ),
    "flutter": (
        '<rect x="4" y="3" width="16" height="18" rx="2"/>'
        '<path d="M11 19h2"/>'
    ),
}

DEPLOY_ICONS: dict[str, str] = {
    "cm5": (
        '<rect x="4" y="4" width="16" height="16" rx="2"/>'
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M9 4V2M15 4V2M9 22v-2M15 22v-2'
        'M4 9H2M4 15H2M22 9h-2M22 15h-2"/>'
    ),
    "user-pc": (
        '<rect x="3" y="4" width="18" height="12" rx="2"/>'
        '<path d="M8 20h8M12 16v4"/>'
    ),
    "mobile": (
        '<rect x="7" y="2" width="10" height="20" rx="2"/>'
        '<path d="M11 18h2"/>'
    ),
    "wearable": (
        '<circle cx="12" cy="12" r="6"/>'
        '<path d="M12 9v3l1.8 1.8M9.5 4h5l-.8 3h-3.4L9.5 4Z'
        'M9.5 20h5l-.8-3h-3.4l-.8 3Z"/>'
    ),
}


def render_icon(inner: str, css_class: str = "tech-icon") -> str:
    return (
        f'<svg class="{css_class}" viewBox="0 0 24 24" width="14" '
        f'height="14" fill="none" stroke="currentColor" '
        f'stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
    )


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

def render_project_rows(
    results: dict[str, RemoteStatus],
    meta: dict[str, RepoMeta],
) -> str:
    rows: list[str] = []

    for entry in PROJECTS:
        result = results.get(entry.name)
        repo_meta = meta.get(entry.name, RepoMeta())

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

        stack_icon = render_icon(
            STACK_ICONS.get(entry.stack, ""),
        )

        deploy_icon = render_icon(
            DEPLOY_ICONS.get(deploy_key, ""),
        )

        # --- Last commit --------------------------------------------------
        if repo_meta.commit_subject:
            commit_text = esc(repo_meta.commit_subject)
            commit_url = esc(
                repo_meta.commit_url or project_repo
            )

            commit_html = (
                f'<a href="{commit_url}" target="_blank" '
                f'rel="noopener noreferrer" class="commit-link" '
                f'title="{commit_text}">{commit_text}</a>'
            )
        else:
            commit_html = '<span class="cell-muted">—</span>'

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
                {stack_icon}{stack}
              </td>

              <td class="deploy">
                <span class="deploy-badge">
                  {deploy_icon}{deploy}
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

              <td class="commit-cell">
                {commit_html}
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

        icon = render_icon(
            DEPLOY_ICONS.get(key, ""),
            css_class="tech-icon deploy-card-icon",
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
                {icon}{esc(label)}
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
    meta: dict[str, RepoMeta],
) -> str:
    stats = calculate_statistics(results)

    total = int(stats["total"])
    ok = int(stats["ok"])
    errors = int(stats["errors"])
    success_percent = float(stats["success_percent"])

    deploy_counts = stats["deploy_counts"]
    stack_counts = stats["stack_counts"]

    rows = render_project_rows(results, meta)

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

<script>
  // Applied synchronously, before first paint, so a saved manual theme
  // choice never causes a visible flash of the system-default theme.
  (function () {{
    try {{
      var saved = localStorage.getItem("hydra-dashboard-theme");

      if (saved === "dark" || saved === "light") {{
        document.documentElement.setAttribute("data-theme", saved);
      }}
    }} catch (e) {{
      // Private browsing / storage disabled - falls back to the
      // system theme, same as any other viewer without a saved choice.
    }}
  }})();
</script>

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
    :root:not([data-theme="light"]) {{
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

  /*
   * Explicit theme override (the toggle button). Repeats the same dark
   * token values as the media query above so a manual choice wins in both
   * directions - system says light + user picks dark, and vice versa.
   */
  :root[data-theme="dark"] {{
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

  .header-top {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
  }}

  .theme-toggle {{
    appearance: none;
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--dim);
    border-radius: 8px;
    cursor: pointer;
    box-shadow: var(--shadow);
    transition: border-color .15s ease, color .15s ease;
  }}

  .theme-toggle:hover {{
    border-color: var(--accent);
    color: var(--accent);
  }}

  .theme-toggle svg {{
    width: 17px;
    height: 17px;
  }}

  .theme-toggle .icon-moon {{
    display: none;
  }}

  :root[data-theme="dark"] .theme-toggle .icon-sun {{
    display: none;
  }}

  :root[data-theme="dark"] .theme-toggle .icon-moon {{
    display: block;
  }}

  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) .theme-toggle .icon-sun {{
      display: none;
    }}

    :root:not([data-theme="light"]) .theme-toggle .icon-moon {{
      display: block;
    }}
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
    min-width: 1040px;
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

  .tech-icon {{
    flex-shrink: 0;
    vertical-align: -2px;
    margin-right: 5px;
    color: var(--dim);
  }}

  .deploy-card-icon {{
    color: var(--accent);
  }}

  .deploy-label {{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 0;
  }}

  .commit-cell {{
    max-width: 220px;
  }}

  .commit-link {{
    color: var(--text);
    text-decoration: none;
    font-size: 12px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.4;
  }}

  .commit-link:hover {{
    color: var(--accent);
    text-decoration: underline;
  }}

  .cell-muted {{
    color: var(--dim);
    font-size: 12px;
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
    <div class="header-top">
      <div class="eyebrow">
        HYDRA-UMC / URTC ECOSYSTEM
      </div>

      <button
        id="theme-toggle"
        class="theme-toggle"
        type="button"
        aria-label="Toggle dark/light theme"
        title="Toggle dark/light theme"
      >
        <svg
          class="icon-sun"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        ><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>

        <svg
          class="icon-moon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        ><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"/></svg>
      </button>
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
          <th>Last commit</th>
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

  // --- Theme toggle ---------------------------------------------------

  const themeToggle =
    document.getElementById("theme-toggle");

  const THEME_KEY = "hydra-dashboard-theme";

  function currentTheme() {{
    var explicit =
      document.documentElement.getAttribute("data-theme");

    if (explicit === "dark" || explicit === "light") {{
      return explicit;
    }}

    return (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    )
      ? "dark"
      : "light";
  }}

  if (themeToggle) {{
    themeToggle.addEventListener("click", function () {{
      const next =
        currentTheme() === "dark" ? "light" : "dark";

      document.documentElement.setAttribute(
        "data-theme",
        next
      );

      try {{
        localStorage.setItem(THEME_KEY, next);
      }} catch (e) {{
        // Storage unavailable - the toggle still works for this
        // page view, it just won't be remembered next visit.
      }}
    }});
  }}

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

    print(
        f"Fetching latest commit for "
        f"{total} projects"
        + (
            " (authenticated)..."
            if GITHUB_TOKEN
            else " (unauthenticated, 60/hour ceiling)..."
        ),
        file=sys.stderr,
    )

    meta = fetch_all_meta(PROJECTS)

    meta_ok = sum(
        1
        for repo_meta in meta.values()
        if repo_meta.commit_subject is not None
    )

    print(
        f"{meta_ok}/{total} commit lookups resolved.",
        file=sys.stderr,
    )

    OUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    index_path = OUT_DIR / "index.html"

    index_path.write_text(
        render_html(results, meta),
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