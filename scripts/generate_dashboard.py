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
from hydra_umc_updater.registry import BY_FAMILY, FAMILY_PARENT, PROJECTS, ProjectEntry


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
    "python-bare": (
        '<path d="M12 2 21 7v10l-9 5-9-5V7l9-5Z"/>'
        '<path d="M3 7l9 5 9-5M12 12v9"/>'
        '<circle cx="12" cy="9" r="1.4"/>'
    ),
}

# ---------------------------------------------------------------------------
# Role icons (v3) - one per ProjectEntry.role, same "generic shape, not a
# trademark" convention as STACK_ICONS/DEPLOY_ICONS above.
# ---------------------------------------------------------------------------

ROLE_ICONS: dict[str, str] = {
    "api": (
        '<path d="M4 12h4M16 12h4M8 12a4 4 0 0 1 4-4M12 16a4 4 0 0 1-4-4"/>'
        '<circle cx="8" cy="12" r="2"/><circle cx="16" cy="12" r="2"/>'
    ),
    "ui": (
        '<rect x="3" y="4" width="18" height="13" rx="2"/>'
        '<path d="M8 21h8M12 17v4"/>'
    ),
    "cli": (
        '<rect x="3" y="4" width="18" height="16" rx="2"/>'
        '<path d="M7 9l3 3-3 3M13 15h4"/>'
    ),
    "firmware": (
        '<path d="M9 2v3M12 2v3M15 2v3M9 19v3M12 19v3M15 19v3'
        'M2 9h3M2 12h3M2 15h3M19 9h3M19 12h3M19 15h3"/>'
        '<rect x="6" y="6" width="12" height="12" rx="2"/>'
    ),
    "library": (
        '<path d="M4 4h4v16H4zM10 4h4v16h-4zM16 5l4-1v16l-4 1z"/>'
    ),
    "service": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M12 2v3M12 19v3M2 12h3M19 12h3'
        'M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/>'
    ),
    "tool": (
        '<path d="M14.7 6.3a4 4 0 0 1-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 1 5.4-5.4Z"/>'
    ),
}

ROLE_LABELS: dict[str, str] = {
    "api": "API",
    "ui": "UI",
    "cli": "CLI",
    "firmware": "Firmware",
    "library": "Library",
    "service": "Service",
    "tool": "Tool",
}

ROLE_ORDER = ["api", "ui", "cli", "firmware", "library", "service", "tool"]

# ---------------------------------------------------------------------------
# Maturity (v3) - see registry.py's own module docstring for exactly how
# each project was assigned one of these four levels; this dashboard only
# renders the classification, it doesn't decide it.
# ---------------------------------------------------------------------------

MATURITY_ORDER = ["production", "established", "functional", "scaffolding"]

MATURITY_LABELS: dict[str, str] = {
    "production": "Production",
    "established": "Established",
    "functional": "Functional",
    "scaffolding": "Scaffolding",
}

MATURITY_CLASSES: dict[str, str] = {
    "production": "maturity-production",
    "established": "maturity-established",
    "functional": "maturity-functional",
    "scaffolding": "maturity-scaffolding",
}

MATURITY_DESCRIPTIONS: dict[str, str] = {
    "production": "Real firmware for a real, physical PCB this ecosystem's own hardware docs describe.",
    "established": "Original, pre-2026-expansion project with a long real version history - trusted on that history, not re-audited this pass.",
    "functional": "Real, tested business logic - verified this pass (own test suite / real end-to-end smoke test / a real compiled protocol round-trip).",
    "scaffolding": "A real, compilable entry point exists; the feature the project exists for does not yet.",
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
# Project ordering (v3) - grouped by family, each family's own parent (if
# it has a single one) shown first with its children immediately after in
# their original registry order. Families with no single shared parent
# (only "Complementary Tools" today) render in plain registry order.
# ---------------------------------------------------------------------------

def ordered_projects() -> list[tuple[str, ProjectEntry | None, list[ProjectEntry]]]:
    """Returns [(family_name, parent_or_None, [children_in_family_order]), ...]
    in first-seen family order (i.e. the order families already appear in
    registry.py's own PROJECTS list)."""

    order: list[tuple[str, ProjectEntry | None, list[ProjectEntry]]] = []
    seen: dict[str, int] = {}

    for entry in PROJECTS:
        if entry.family not in seen:
            seen[entry.family] = len(order)
            order.append((entry.family, FAMILY_PARENT.get(entry.family), []))

        idx = seen[entry.family]
        parent = order[idx][1]
        if parent is not None and entry.name == parent.name:
            continue  # parent itself is stored separately, not in the children list
        order[idx][2].append(entry)

    return order


# ---------------------------------------------------------------------------
# Project rows
# ---------------------------------------------------------------------------

def _render_one_row(
    entry: ProjectEntry,
    *,
    results: dict[str, RemoteStatus],
    meta: dict[str, RepoMeta],
    is_child: bool,
) -> str:
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

    role_icon = render_icon(
        ROLE_ICONS.get(entry.role, ""),
        css_class="tech-icon role-icon",
    )
    role_label = esc(ROLE_LABELS.get(entry.role, entry.role))

    maturity_class = MATURITY_CLASSES.get(entry.maturity, "maturity-scaffolding")
    maturity_label = esc(MATURITY_LABELS.get(entry.maturity, entry.maturity))

    child_class = " child-row" if is_child else ""
    child_marker = '<span class="child-marker" aria-hidden="true">↳</span>' if is_child else ""

    tech_chips = "".join(
        f'<span class="tech-chip">{esc(t)}</span>' for t in entry.tech
    ) or '<span class="cell-muted">—</span>'

    notes_html = esc(entry.notes) if entry.notes else "No notes recorded for this project yet."
    build_note_html = esc(entry.note) if entry.note else "—"

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

    detail_row_id = f"detail-{project_name}"

    row = f"""
        <tr
            class="project-row {status_class}{child_class}"
            data-name="{project_name.lower()}"
            data-status="{esc(status_key)}"
            data-deploy="{deploy_filter}"
            data-stack="{stack.lower()}"
            data-maturity="{esc(entry.maturity)}"
            data-role="{esc(entry.role)}"
            data-family="{esc(entry.family.lower())}"
        >
          <td class="project-name">
            <button
                type="button"
                class="details-toggle"
                data-details-target="{detail_row_id}"
                aria-expanded="false"
                aria-label="Toggle notes for {project_name}"
            >▸</button>

            {child_marker}

            <div class="project-title-wrap">
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
            </div>
          </td>

          <td class="role-cell">
            <span class="role-badge role-{esc(entry.role)}">
              {role_icon}{role_label}
            </span>
          </td>

          <td class="maturity-cell">
            <span class="maturity-badge {maturity_class}">
              {maturity_label}
            </span>
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

        <tr
            class="detail-row"
            id="{detail_row_id}"
            data-name="{project_name.lower()}"
            data-status="{esc(status_key)}"
            data-deploy="{deploy_filter}"
            data-stack="{stack.lower()}"
            data-maturity="{esc(entry.maturity)}"
            data-role="{esc(entry.role)}"
            data-family="{esc(entry.family.lower())}"
            hidden
        >
          <td colspan="8">
            <div class="detail-panel">
              <div class="detail-block">
                <div class="detail-label">Notes</div>
                <div class="detail-text">{notes_html}</div>
              </div>

              <div class="detail-block">
                <div class="detail-label">Technology</div>
                <div class="tech-chips">{tech_chips}</div>
              </div>

              <div class="detail-block">
                <div class="detail-label">Build</div>
                <div class="detail-text">{build_note_html}</div>
              </div>
            </div>
          </td>
        </tr>
        """

    return row


def render_project_rows(
    results: dict[str, RemoteStatus],
    meta: dict[str, RepoMeta],
) -> str:
    rows: list[str] = []

    for family_name, parent, children in ordered_projects():
        # Same raw lower() value the project rows themselves stamp into
        # their own data-family attribute (and the family <select>'s own
        # option values use) - a data-* attribute value, not a CSS
        # id/class, so it doesn't need slug-sanitizing, and NOT
        # sanitizing it is what keeps the two sides matching in the JS
        # filter below.
        family_id = esc(family_name.lower())

        parent_repo_link = ""
        if parent is not None:
            parent_repo_link = (
                f' · <a href="{esc(repo_url(parent.name))}" target="_blank" '
                f'rel="noopener noreferrer">{esc(parent.name)}</a> is this family\'s '
                f"own integration parent"
            )

        rows.append(
            f"""
            <tr class="family-header-row" data-family-header="{family_id}">
              <td colspan="8">
                <span class="family-header-label">{esc(family_name)}</span>
                <span class="family-header-count">{len(children) + (1 if parent else 0)} project(s){parent_repo_link}</span>
              </td>
            </tr>
            """
        )

        if parent is not None:
            rows.append(
                _render_one_row(parent, results=results, meta=meta, is_child=False)
            )

        for child in children:
            rows.append(
                _render_one_row(child, results=results, meta=meta, is_child=parent is not None)
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

    maturity_counts = {
        key: 0
        for key in MATURITY_ORDER
    }

    role_counts = {
        key: 0
        for key in ROLE_ORDER
    }

    for entry in PROJECTS:
        deploy_counts[entry.deploy] = (
            deploy_counts.get(entry.deploy, 0) + 1
        )

        stack_counts[entry.stack] = (
            stack_counts.get(entry.stack, 0) + 1
        )

        maturity_counts[entry.maturity] = (
            maturity_counts.get(entry.maturity, 0) + 1
        )

        role_counts[entry.role] = (
            role_counts.get(entry.role, 0) + 1
        )

    return {
        "total": total,
        "ok": ok,
        "errors": errors,
        "success_percent": success_percent,
        "deploy_counts": deploy_counts,
        "stack_counts": stack_counts,
        "maturity_counts": maturity_counts,
        "role_counts": role_counts,
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
# Maturity cards (v3)
# ---------------------------------------------------------------------------

def render_maturity_cards(
    maturity_counts: dict[str, int],
) -> str:
    cards: list[str] = []

    for key in MATURITY_ORDER:
        count = maturity_counts.get(key, 0)
        label = MATURITY_LABELS.get(key, key)
        description = MATURITY_DESCRIPTIONS.get(key, "")
        css_class = MATURITY_CLASSES.get(key, "maturity-scaffolding")

        cards.append(
            f"""
            <button
                class="maturity-card {css_class}"
                type="button"
                data-filter-maturity="{esc(key)}"
                title="{esc(description)}"
            >
              <span class="maturity-count">{count}</span>
              <span class="maturity-card-label">{esc(label)}</span>
              <span class="maturity-card-desc">{esc(description)}</span>
            </button>
            """
        )

    return "".join(cards)


# ---------------------------------------------------------------------------
# Role summary (v3)
# ---------------------------------------------------------------------------

def render_role_summary(
    role_counts: dict[str, int],
) -> str:
    items = [
        (key, role_counts.get(key, 0))
        for key in ROLE_ORDER
        if role_counts.get(key, 0) > 0
    ]

    return "".join(
        f"""
        <button
            class="role-item"
            type="button"
            data-filter-role="{esc(key)}"
        >
          {render_icon(ROLE_ICONS.get(key, ""), css_class="tech-icon role-icon")}
          <span>{esc(ROLE_LABELS.get(key, key))}</span>
          <strong>{count}</strong>
        </button>
        """
        for key, count in items
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
    maturity_counts = stats["maturity_counts"]
    role_counts = stats["role_counts"]

    rows = render_project_rows(results, meta)

    deploy_cards = render_deploy_cards(
        deploy_counts,
    )

    stack_summary = render_stack_summary(
        stack_counts,
    )

    maturity_cards = render_maturity_cards(
        maturity_counts,
    )

    role_summary = render_role_summary(
        role_counts,
    )

    family_options = "".join(
        f'<option value="{esc(name.lower())}">{esc(name)} ({len(members)})</option>'
        for name, members in BY_FAMILY.items()
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
  content="HYDRA-UMC / URTC ecosystem status dashboard - maturity, role, family/parent tree, stack and version for all 44 projects"
>

<title>HYDRA-UMC / URTC Ecosystem Status v3</title>

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
    --maturity-production: #0f766e;
    --maturity-production-soft: #ccfbf1;
    --maturity-established: #4338ca;
    --maturity-established-soft: #e0e7ff;
    --maturity-scaffolding: #b45309;
    --maturity-scaffolding-soft: #fef3c7;
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
      --maturity-production: #2dd4bf;
      --maturity-production-soft: #0f3d3a;
      --maturity-established: #818cf8;
      --maturity-established-soft: #241f57;
      --maturity-scaffolding: #fbbf24;
      --maturity-scaffolding-soft: #4a3105;
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
    --maturity-production: #2dd4bf;
    --maturity-production-soft: #0f3d3a;
    --maturity-established: #818cf8;
    --maturity-established-soft: #241f57;
    --maturity-scaffolding: #fbbf24;
    --maturity-scaffolding-soft: #4a3105;
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
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .version-pill {{
    font-size: 13px;
    font-weight: 700;
    background: var(--accent-soft);
    color: var(--accent);
    border-radius: 999px;
    padding: 3px 11px;
    vertical-align: middle;
  }}

  .subtitle {{
    color: var(--dim);
    margin: 0;
    font-size: 14px;
    line-height: 1.6;
  }}

  .subtitle-v3 {{
    margin-top: 6px;
    font-size: 12.5px;
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

  .section-title-hint {{
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 400;
    font-size: 11px;
    color: var(--dim);
    margin-left: 8px;
    text-transform: none;
    letter-spacing: 0;
  }}

  /* --- Maturity cards (v3) ---------------------------------------------- */

  .maturity-grid {{
    display: grid;
    grid-template-columns:
      repeat(auto-fit, minmax(190px, 1fr));
    gap: 10px;
  }}

  .maturity-card {{
    appearance: none;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    border-radius: 9px;
    padding: 13px 15px;
    text-align: left;
    cursor: pointer;
    box-shadow: var(--shadow);
    border-left: 4px solid var(--maturity-scaffolding);
    transition:
      border-color .15s ease,
      transform .15s ease;
  }}

  .maturity-card:hover {{
    transform: translateY(-1px);
  }}

  .maturity-card.active {{
    box-shadow: 0 0 0 2px var(--accent-soft);
  }}

  .maturity-card.maturity-production {{ border-left-color: var(--maturity-production); }}
  .maturity-card.maturity-established {{ border-left-color: var(--maturity-established); }}
  .maturity-card.maturity-functional {{ border-left-color: var(--accent); }}
  .maturity-card.maturity-scaffolding {{ border-left-color: var(--maturity-scaffolding); }}

  .maturity-count {{
    display: block;
    font-family: "IBM Plex Mono", monospace;
    font-size: 21px;
    font-weight: 700;
  }}

  .maturity-card-label {{
    display: block;
    font-size: 12px;
    font-weight: 600;
    margin-top: 2px;
  }}

  .maturity-card-desc {{
    display: block;
    color: var(--dim);
    font-size: 11px;
    margin-top: 4px;
    line-height: 1.4;
  }}

  .maturity-badge {{
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 3px 9px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 10.5px;
    font-weight: 600;
    white-space: nowrap;
  }}

  .maturity-badge.maturity-production {{
    background: var(--maturity-production-soft);
    color: var(--maturity-production);
  }}

  .maturity-badge.maturity-established {{
    background: var(--maturity-established-soft);
    color: var(--maturity-established);
  }}

  .maturity-badge.maturity-functional {{
    background: var(--accent-soft);
    color: var(--accent);
  }}

  .maturity-badge.maturity-scaffolding {{
    background: var(--maturity-scaffolding-soft);
    color: var(--maturity-scaffolding);
  }}

  /* --- Role summary/badges (v3) ------------------------------------------ */

  .role-summary {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
  }}

  .role-item {{
    appearance: none;
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 11px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
    color: var(--text);
    cursor: pointer;
    transition: border-color .15s ease;
  }}

  .role-item:hover {{
    border-color: var(--accent);
  }}

  .role-item.active {{
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-soft);
  }}

  .role-item strong {{
    color: var(--accent);
  }}

  .role-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 6px;
    padding: 3px 8px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 10.5px;
    font-weight: 600;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--dim);
    white-space: nowrap;
  }}

  .role-icon {{
    color: var(--accent);
  }}

  /* --- Family filter (v3) ------------------------------------------------ */

  .family-filter {{
    display: flex;
    align-items: center;
    gap: 7px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
    color: var(--dim);
  }}

  .family-filter select {{
    padding: 9px 11px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--surface);
    color: var(--text);
    font-family: "IBM Plex Sans", sans-serif;
    font-size: 12.5px;
    max-width: 260px;
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
    min-width: 1220px;
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

  tr.project-row.hidden + tr.detail-row {{
    display: none;
  }}

  /* --- Family header rows (v3) -------------------------------------- */

  tr.family-header-row td {{
    background: var(--surface-2);
    border-bottom: 1px solid var(--border-strong);
    padding: 9px 14px;
    font-family: "IBM Plex Mono", monospace;
  }}

  tr.family-header-row.hidden {{
    display: none;
  }}

  .family-header-label {{
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .04em;
  }}

  .family-header-count {{
    color: var(--dim);
    font-size: 11px;
    margin-left: 10px;
  }}

  .family-header-count a {{
    color: var(--accent);
    text-decoration: none;
  }}

  /* --- Child rows (v3) - visually nested under their family's parent -- */

  tr.project-row.child-row .project-name {{
    padding-left: 6px;
  }}

  .child-marker {{
    color: var(--dim);
    font-family: "IBM Plex Mono", monospace;
    margin-right: 2px;
  }}

  /* --- Per-row notes toggle + detail panel (v3) ----------------------- */

  .project-name {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
  }}

  .details-toggle {{
    appearance: none;
    border: none;
    background: none;
    color: var(--dim);
    cursor: pointer;
    font-size: 11px;
    line-height: 1.6;
    padding: 0 2px;
    flex: 0 0 auto;
  }}

  .details-toggle:hover {{
    color: var(--accent);
  }}

  .project-title-wrap {{
    flex: 1 1 auto;
    min-width: 0;
  }}

  tr.detail-row td {{
    background: var(--surface-2);
    border-bottom: 1px solid var(--border);
    padding: 14px 14px 16px 40px;
  }}

  .detail-panel {{
    display: grid;
    grid-template-columns:
      repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
  }}

  .detail-label {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: var(--dim);
    margin-bottom: 5px;
  }}

  .detail-text {{
    font-size: 12.5px;
    line-height: 1.55;
  }}

  .tech-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}

  .tech-chip {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 3px 8px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 10.5px;
    white-space: nowrap;
  }}

  .role-cell,
  .maturity-cell {{
    white-space: nowrap;
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
      <span class="version-pill">v3</span>
    </h1>

    <p class="subtitle">
      {ok}/{total} repositories resolved successfully
      · {success_percent_text} healthy
      · versions are read from each project's own source file
      · dashboard generated by GitHub Actions
      · static GitHub Pages
    </p>

    <p class="subtitle subtitle-v3">
      v3: real maturity/role classification, family/parent trees and richer
      per-project notes - see the Maturity legend below for exactly how
      each level was decided.
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
       MATURITY (v3)
       ================================================================ -->

  <section class="section">

    <div class="section-title">
      Maturity
      <span class="section-title-hint">click a card to filter · hover for how it was decided</span>
    </div>

    <div class="maturity-grid">
      {maturity_cards}
    </div>

  </section>


  <!-- ================================================================
       ROLE (v3)
       ================================================================ -->

  <section class="section">

    <div class="section-title">
      Role
    </div>

    <div class="role-summary">
      {role_summary}
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

    <div class="family-filter">
      <label for="family-select">Family:</label>
      <select id="family-select">
        <option value="all">All families</option>
        {family_options}
      </select>
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
          <th>Type</th>
          <th>Maturity</th>
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

  const familyHeaderRows = Array.from(
    document.querySelectorAll(".family-header-row")
  );

  const searchInput =
    document.getElementById("project-search");

  const emptyResults =
    document.getElementById("empty-results");

  const familySelect =
    document.getElementById("family-select");

  const statusFilters =
    Array.from(
      document.querySelectorAll("[data-filter-status]")
    );

  const deployFilters =
    Array.from(
      document.querySelectorAll("[data-filter-deploy]")
    );

  const maturityFilters =
    Array.from(
      document.querySelectorAll("[data-filter-maturity]")
    );

  const roleFilters =
    Array.from(
      document.querySelectorAll("[data-filter-role]")
    );

  let activeStatus = "all";
  let activeDeploy = "all";
  let activeMaturity = "all";
  let activeRole = "all";


  function applyFilters() {{
    const query =
      searchInput.value
        .trim()
        .toLowerCase();

    const activeFamily =
      familySelect ? familySelect.value : "all";

    let visible = 0;
    const visibleFamilies = {{}};

    rows.forEach(function (row) {{
      const name =
        row.dataset.name || "";

      const status =
        row.dataset.status || "";

      const deploy =
        row.dataset.deploy || "";

      const stack =
        row.dataset.stack || "";

      const maturity =
        row.dataset.maturity || "";

      const role =
        row.dataset.role || "";

      const family =
        row.dataset.family || "";

      const matchesSearch =
        !query ||
        name.includes(query) ||
        stack.includes(query) ||
        deploy.includes(query) ||
        family.includes(query);

      const matchesStatus =
        activeStatus === "all" ||
        status === activeStatus;

      const matchesDeploy =
        activeDeploy === "all" ||
        deploy === activeDeploy;

      const matchesMaturity =
        activeMaturity === "all" ||
        maturity === activeMaturity;

      const matchesRole =
        activeRole === "all" ||
        role === activeRole;

      const matchesFamily =
        activeFamily === "all" ||
        family === activeFamily;

      const show =
        matchesSearch &&
        matchesStatus &&
        matchesDeploy &&
        matchesMaturity &&
        matchesRole &&
        matchesFamily;

      row.classList.toggle(
        "hidden",
        !show
      );

      // The detail row right after this project row shares its
      // visibility gate - a hidden project row's notes can't stay open.
      if (!show) {{
        const toggle = row.querySelector(".details-toggle");
        const targetId = toggle && toggle.dataset.detailsTarget;
        const target = targetId && document.getElementById(targetId);
        if (target) {{
          target.hidden = true;
        }}
        if (toggle) {{
          toggle.setAttribute("aria-expanded", "false");
          toggle.textContent = "▸";
        }}
      }}

      if (show) {{
        visible += 1;
        if (family) {{
          visibleFamilies[family] = true;
        }}
      }}
    }});

    familyHeaderRows.forEach(function (headerRow) {{
      const key = headerRow.dataset.familyHeader || "";
      headerRow.classList.toggle(
        "hidden",
        !visibleFamilies[key]
      );
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

  if (familySelect) {{
    familySelect.addEventListener(
      "change",
      applyFilters
    );
  }}


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


  maturityFilters.forEach(function (button) {{
    button.addEventListener(
      "click",
      function () {{

        const selected =
          button.dataset.filterMaturity;

        if (activeMaturity === selected) {{
          activeMaturity = "all";
          button.classList.remove("active");
        }} else {{
          activeMaturity = selected;

          maturityFilters.forEach(
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


  roleFilters.forEach(function (button) {{
    button.addEventListener(
      "click",
      function () {{

        const selected =
          button.dataset.filterRole;

        if (activeRole === selected) {{
          activeRole = "all";
          button.classList.remove("active");
        }} else {{
          activeRole = selected;

          roleFilters.forEach(
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


  // --- Per-row notes toggle --------------------------------------------

  Array.from(
    document.querySelectorAll(".details-toggle")
  ).forEach(function (button) {{
    button.addEventListener("click", function () {{
      const targetId = button.dataset.detailsTarget;
      const target = document.getElementById(targetId);
      if (!target) {{
        return;
      }}
      const nowOpen = target.hidden;
      target.hidden = !nowOpen;
      button.setAttribute("aria-expanded", nowOpen ? "true" : "false");
      button.textContent = nowOpen ? "▾" : "▸";
    }});
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