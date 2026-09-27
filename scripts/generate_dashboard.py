#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - scripts/generate_dashboard.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Generates docs/index.html - a static ecosystem status dashboard.
#
# The dashboard uses HYDRA-UMC-UPDATER's dynamic GitHub discovery and the
# manifest contract. It never maintains a project catalogue in this file.
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
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from hydra_umc_updater.ecosystem_catalog import parse_catalog
from hydra_umc_updater.github_client import RemoteStatus, discover_remote_projects
from hydra_umc_updater.registry import ProjectEntry

# URTC and A.R.M.O.R. ship their own dedicated updater/discovery client too
# (urtc-updater, armor-updater) - each is public and needs no token, same as
# HYDRA-UMC's own discover_remote_projects above. Aliased on import: all
# three packages name this function identically, and ProjectEntry/
# RemoteStatus from all three are duck-type compatible with the renderers
# below (same field names: name/stack/deploy/tech/notes/maturity/role/
# family/parent/native_version) even though they are technically different
# classes - each one's own manifest schema is a superset or exact match of
# what this file actually reads.
from urtc_updater.github_client import discover_remote_projects as discover_urtc_projects
from armor_updater.github_client import discover_remote_projects as discover_armor_projects


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

OUT_DIR = Path(__file__).resolve().parent.parent / "docs"
CATALOG_PATH = Path(__file__).resolve().parent.parent / "ecosystem-catalog.json"


# ---------------------------------------------------------------------------
# GitHub REST metadata (latest commit subject per project)
# ---------------------------------------------------------------------------
#
# The manifest lookup above reads raw.githubusercontent.com,
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


# DOC-51 (P2):
# a real, historical commit subject pulled live from the GitHub API can
# itself name a private internal tracking document by filename (from
# before those references were cleaned out of every repo's own public
# files this same review pass) - the commit is real history and is
# never rewritten, but this dashboard is public presentation, so any
# such filename is redacted right here, at render time, the moment a
# subject is fetched. Case-insensitive; matches the exact filenames
# the same review pass's detector already found leaking into public files
# elsewhere in the ecosystem.
_PRIVATE_DOCUMENT_NAME_RE = re.compile(
    r"\b(mejoras_futuras\.txt|chat\.txt|auditoria_historial\.txt)\b",
    re.IGNORECASE,
)


def _redact_private_document_names(subject: str) -> str:
    """Replaces a bare private-tracking-document filename with a generic,
    self-sufficient placeholder - the rest of a real commit subject (e.g.
    "... sweep + real mDNS") stays intact and still tells a public reader
    something real happened, without naming a file they have no access
    to and were never meant to."""
    return _PRIVATE_DOCUMENT_NAME_RE.sub("an internal tracking note", subject)


# REV-033 (found in a review pass, P2): the CAT-01
# fix above (the live GitHub Actions badge.svg) answers "did the build
# succeed", but not "how long ago was that" - a check that passed the
# last time this workflow actually ran, whenever that was, looks
# pixel-identical to one that just ran a minute ago.
#
# This is deliberately NOT fetched here in Python and baked into the
# generated HTML as a string: that value changes on every single hourly
# run (this workflow's own cron) regardless of whether anything in the
# ecosystem actually changed, which would defeat the
# `git diff --cached --quiet` check build-dashboard.yml already uses to
# skip committing when nothing real changed (see this file's own header
# comment) - turning an occasional, meaningful commit into an hourly
# one, exactly the "commit just to update a clock" outcome this finding
# says not to reintroduce.
#
# Instead this queries the same GitHub Actions REST endpoint LIVE, from
# the viewer's own browser, every time the page is actually opened - the
# identical approach already used for the badge.svg <img> above, which
# is also never baked in and never causes a commit. See
# FRESHNESS_WORKFLOW_FILE/FRESHNESS_STALE_AFTER_HOURS (their own
# constants, since nothing here in Python needs them - the fetch and the
# staleness comparison both happen in the browser) in the page's
# <script> below.


def render_freshness_indicator() -> str:
    """A placeholder the page's own <script> replaces with a real state
    once its live fetch() of the Actions API resolves - see that
    script's own REV-033 comment. Three honest states, per this
    finding's own closure criteria: a stale-but-green result, a fresh
    result, and "can't tell right now" (never rendered as a false
    green). This initial markup is itself the fourth, transient state a
    reader sees only for the instant before that fetch resolves (or
    permanently, with JS disabled) - honestly labelled, never a
    placeholder pretending to be a real answer."""
    return (
        '<p id="dashboard-freshness" class="freshness-indicator freshness-pending" '
        'data-i18n="freshness_checking_now">'
        "Checking last build time..."
        "</p>"
    )


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
            meta.commit_subject = _redact_private_document_names(message.splitlines()[0][:120])
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
    "dev-server": "Dev Server",
    # A.R.M.O.R.'s own manifest keeps `deployment_target` as free text
    # rather than this same closed enum (see armor_updater.deploy_category,
    # this dashboard's own single source of truth for classifying it) -
    # these four are its real hardware-target categories, not present in
    # HYDRA-UMC/URTC. "workstation" is folded into "user-pc" above instead
    # of a fifth new one - the same real thing, a developer's own machine.
    "field-node": "Field Node",
    "server": "AI Server",
    "browser": "Browser Client",
    "shared": "Shared / Ecosystem-wide",
}

DEPLOY_ORDER = [
    "cm5",
    "field-node",
    "server",
    "user-pc",
    "mobile",
    "wearable",
    "browser",
    "dev-server",
    "shared",
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
    # A.R.M.O.R.'s own manifest keeps `role` as free text rather than this
    # same closed enum - "docs" and "hardware" are two real roles that
    # exist for real among its projects (ARMOR-DOCS, ARMOR-HARDWARE) with
    # no honest match in the enum above: neither is compiled/running code,
    # so forcing either into "tool" or "firmware" would misclassify it.
    "docs": (
        '<path d="M6 2h9l3 3v17H6z"/><path d="M15 2v3h3M9 9h6M9 13h6M9 17h4"/>'
    ),
    "hardware": (
        '<path d="M6 3v4M10 3v4M8 7v4M14 3v4M18 3v4M16 7v4'
        'M4 11h16v3a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4Z"/><path d="M10 18v3M14 18v3"/>'
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
    "docs": "Documentation",
    "hardware": "Hardware Design",
}

ROLE_ORDER = ["api", "ui", "cli", "firmware", "library", "service", "tool", "docs", "hardware"]

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
    # Previously gated on when a project was created ("original,
    # pre-2026-expansion"), a date no amount of real work can ever change -
    # every one of URTC's and A.R.M.O.R.'s own real projects, and several
    # of HYDRA-UMC's own newer ones, were permanently excluded from this
    # tier by birth date alone, regardless of how substantial their own
    # real record became. Redefined on real, checkable substance instead:
    # a long version history under this ecosystem's own odometer scheme
    # (each real build is one more digit, so the number itself is a real
    # count, not a claim) AND real, sustained use beyond a passing test
    # suite - deployed and actually operating, or actually depended on by
    # other real, shipped projects, not simulated or one-off.
    "established": "A real, substantial version history under this ecosystem's own odometer scheme, AND real, sustained use beyond a passing test suite - deployed and actually operating, or genuinely depended on by other real projects. Trusted on that record, not re-audited this pass.",
    "functional": "Real, tested business logic - verified this pass (own test suite / real end-to-end smoke test / a real compiled protocol round-trip).",
    "scaffolding": "A real, compilable entry point exists; the feature the project exists for does not yet.",
}


# ---------------------------------------------------------------------------
# Translations (v3) - the dashboard's own UI chrome and closed vocabulary
# (deploy targets, maturity levels + their tooltip descriptions, roles,
# real-vs-error status labels), in all 7 languages this ecosystem's own
# READMEs already ship. Deliberately does NOT translate project names,
# family names, or the free-text `notes`/`tech` content that comes straight
# from each repository manifest. `{ok}`/`{total}`/`{percent}`/`{count}` placeholders below are
# filled in client-side by the matching `data-*` attribute already on that
# element (computed once, at generation time, in whichever numbers this
# run actually found) - see applyLanguage() in the page's own <script>.
# ---------------------------------------------------------------------------

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "header_title": "Ecosystem Status Dashboard",
        "subtitle_main": "{ok}/{total} repositories resolved successfully · {percent} healthy · metadata and versions are read from each repository manifest · dashboard generated by GitHub Actions · static GitHub Pages",
        "subtitle_v3": "v3: real maturity/role classification, family/parent trees and richer per-project notes - see the Maturity legend below for exactly how each level was decided.",
        "freshness_checking_now": "Checking last build time...",
        "freshness_unknown": "Last check time unavailable right now (could not reach the GitHub Actions API).",
        "freshness_failed": "Last completed check: {conclusion} ({absolute}).",
        "freshness_checking": "Last successful check: {age} ago ({absolute}).",
        "theme_toggle": "Toggle dark/light theme",
        "health_total": "Total projects",
        "health_resolved": "Version resolved",
        "health_errors": "Errors / unknown",
        "health_registry": "Manifest health",
        "section_deploy": "Deployment targets",
        "section_stack": "Technology stacks",
        "section_maturity": "Maturity",
        "section_maturity_hint": "click a card to filter · hover for how it was decided",
        "section_role": "Role",
        "search_placeholder": "Search project, stack or deployment...",
        "search_aria": "Search projects",
        "filter_all": "All",
        "filter_ok": "✓ OK",
        "filter_error": "⚠ Errors",
        "family_label": "Family:",
        "family_all": "All families",
        "reset_filters": "⟲ Reset",
        "reset_filters_title": "Clear the search box and every active filter (status, deploy, maturity, role, family)",
        "th_project": "Project",
        "th_type": "Type",
        "th_maturity": "Maturity",
        "th_stack": "Stack",
        "th_deploy": "Deploy target",
        "th_version": "Version",
        "th_status": "Status",
        "th_commit": "Last commit",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "Notes",
        "detail_technology": "Technology",
        "detail_build": "Build",
        "notes_empty": "No notes recorded for this project yet.",
        "empty_results": "No projects match the current filters.",
        "family_count": "{count} project(s)",
        "family_parent_suffix": "is this family's own integration parent",
        "footer_registry": "Data source:",
        "footer_generator": "Dashboard generator:",
        "footer_workflow": "Workflow:",
        "footer_note": "Each repository manifest is the source of truth for its public metadata and version.",
        "version_status_ok": "OK",
        "version_status_error": "ERROR",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "User PC",
        "deploy_mobile": "Mobile",
        "deploy_wearable": "Wearable",
        "deploy_dev-server": "Dev Server",
        "deploy_field-node": "Field Node",
        "deploy_server": "AI Server",
        "deploy_browser": "Browser Client",
        "deploy_shared": "Shared / Ecosystem-wide",
        "maturity_production": "Production",
        "maturity_established": "Established",
        "maturity_functional": "Functional",
        "maturity_scaffolding": "Scaffolding",
        "maturity_desc_production": MATURITY_DESCRIPTIONS["production"],
        "maturity_desc_established": MATURITY_DESCRIPTIONS["established"],
        "maturity_desc_functional": MATURITY_DESCRIPTIONS["functional"],
        "maturity_desc_scaffolding": MATURITY_DESCRIPTIONS["scaffolding"],
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "Firmware",
        "role_library": "Library",
        "role_service": "Service",
        "role_tool": "Tool",
        "role_docs": "Documentation",
        "role_hardware": "Hardware Design",
    },
    "es": {
        "header_title": "Panel de Estado del Ecosistema",
        "subtitle_main": "{ok}/{total} repositorios resueltos correctamente · {percent} saludables · los metadatos y las versiones se leen del manifiesto de cada repositorio · panel generado por GitHub Actions · GitHub Pages estático",
        "subtitle_v3": "v3: clasificación real de madurez/rol, árboles de familia/padre-hijo y notas por proyecto más completas - ver la leyenda de Madurez más abajo para saber exactamente cómo se decidió cada nivel.",
        "freshness_checking_now": "Comprobando la hora de la última compilación...",
        "freshness_unknown": "Hora de la última comprobación no disponible ahora mismo (no se pudo contactar con la API de GitHub Actions).",
        "freshness_failed": "Última comprobación completada: {conclusion} ({absolute}).",
        "freshness_checking": "Última comprobación correcta: hace {age} ({absolute}).",
        "theme_toggle": "Cambiar tema claro/oscuro",
        "health_total": "Proyectos totales",
        "health_resolved": "Versión resuelta",
        "health_errors": "Errores / desconocido",
        "health_registry": "Estado de manifiestos",
        "section_deploy": "Destinos de despliegue",
        "section_stack": "Stacks tecnológicos",
        "section_maturity": "Madurez",
        "section_maturity_hint": "clic en una tarjeta para filtrar · pasa el ratón para ver cómo se decidió",
        "section_role": "Rol",
        "search_placeholder": "Buscar proyecto, stack o despliegue...",
        "search_aria": "Buscar proyectos",
        "filter_all": "Todos",
        "filter_ok": "✓ OK",
        "filter_error": "⚠ Errores",
        "family_label": "Familia:",
        "family_all": "Todas las familias",
        "reset_filters": "⟲ Restablecer",
        "reset_filters_title": "Limpia el buscador y todos los filtros activos (estado, despliegue, madurez, rol, familia)",
        "th_project": "Proyecto",
        "th_type": "Tipo",
        "th_maturity": "Madurez",
        "th_stack": "Stack",
        "th_deploy": "Destino de despliegue",
        "th_version": "Versión",
        "th_status": "Estado",
        "th_commit": "Último commit",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "Notas",
        "detail_technology": "Tecnología",
        "detail_build": "Build",
        "notes_empty": "Todavía no hay notas registradas para este proyecto.",
        "empty_results": "Ningún proyecto coincide con los filtros actuales.",
        "family_count": "{count} proyecto(s)",
        "family_parent_suffix": "es el padre de integración real de esta familia",
        "footer_registry": "Fuente de datos:",
        "footer_generator": "Generador del panel:",
        "footer_workflow": "Workflow:",
        "footer_note": "El manifiesto de cada repositorio es la fuente de verdad de sus metadatos públicos y su versión.",
        "version_status_ok": "OK",
        "version_status_error": "ERROR",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "PC del usuario",
        "deploy_mobile": "Móvil",
        "deploy_wearable": "Wearable",
        "deploy_dev-server": "Servidor de desarrollo",
        "deploy_field-node": "Nodo de campo",
        "deploy_server": "Servidor de IA",
        "deploy_browser": "Cliente de navegador",
        "deploy_shared": "Compartido / todo el ecosistema",
        "maturity_production": "Producción",
        "maturity_established": "Establecido",
        "maturity_functional": "Funcional",
        "maturity_scaffolding": "Andamiaje",
        "maturity_desc_production": "Firmware real para una placa física real que la propia documentación de hardware de este ecosistema describe.",
        "maturity_desc_established": "Proyecto original, previo a la expansión de 2026, con un largo historial de versiones real - confiado por ese historial, no reauditado en este pase.",
        "maturity_desc_functional": "Lógica de negocio real y probada - verificada en este pase (suite de tests propia / smoke test real de extremo a extremo / round-trip real de protocolo compilado).",
        "maturity_desc_scaffolding": "Existe un punto de entrada real y compilable; la función para la que existe el proyecto todavía no.",
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "Firmware",
        "role_library": "Librería",
        "role_service": "Servicio",
        "role_tool": "Herramienta",
        "role_docs": "Documentación",
        "role_hardware": "Diseño de hardware",
    },
    "fr": {
        "header_title": "Tableau de bord d'état de l'écosystème",
        "subtitle_main": "{ok}/{total} dépôts résolus avec succès · {percent} en bonne santé · les métadonnées et les versions sont lues depuis le manifeste de chaque dépôt · tableau de bord généré par GitHub Actions · GitHub Pages statique",
        "subtitle_v3": "v3 : classification réelle de maturité/rôle, arbres famille/parent-enfant et notes par projet plus complètes - voir la légende Maturité ci-dessous pour savoir exactement comment chaque niveau a été décidé.",
        "freshness_checking_now": "Vérification de l'heure de la dernière compilation...",
        "freshness_unknown": "Heure de la dernière vérification indisponible pour le moment (impossible de contacter l'API GitHub Actions).",
        "freshness_failed": "Dernière vérification terminée : {conclusion} ({absolute}).",
        "freshness_checking": "Dernière vérification réussie : il y a {age} ({absolute}).",
        "theme_toggle": "Basculer le thème clair/sombre",
        "health_total": "Projets au total",
        "health_resolved": "Version résolue",
        "health_errors": "Erreurs / inconnu",
        "health_registry": "État des manifestes",
        "section_deploy": "Cibles de déploiement",
        "section_stack": "Stacks technologiques",
        "section_maturity": "Maturité",
        "section_maturity_hint": "cliquez sur une carte pour filtrer · survolez pour voir comment c'est décidé",
        "section_role": "Rôle",
        "search_placeholder": "Rechercher un projet, un stack ou un déploiement...",
        "search_aria": "Rechercher des projets",
        "filter_all": "Tous",
        "filter_ok": "✓ OK",
        "filter_error": "⚠ Erreurs",
        "family_label": "Famille :",
        "family_all": "Toutes les familles",
        "reset_filters": "⟲ Réinitialiser",
        "reset_filters_title": "Efface le champ de recherche et tous les filtres actifs (statut, déploiement, maturité, rôle, famille)",
        "th_project": "Projet",
        "th_type": "Type",
        "th_maturity": "Maturité",
        "th_stack": "Stack",
        "th_deploy": "Cible de déploiement",
        "th_version": "Version",
        "th_status": "Statut",
        "th_commit": "Dernier commit",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "Notes",
        "detail_technology": "Technologie",
        "detail_build": "Build",
        "notes_empty": "Aucune note enregistrée pour ce projet pour l'instant.",
        "empty_results": "Aucun projet ne correspond aux filtres actuels.",
        "family_count": "{count} projet(s)",
        "family_parent_suffix": "est le véritable parent d'intégration de cette famille",
        "footer_registry": "Source des données :",
        "footer_generator": "Générateur du tableau de bord :",
        "footer_workflow": "Workflow :",
        "footer_note": "Le manifeste de chaque dépôt est la source de vérité de ses métadonnées publiques et de sa version.",
        "version_status_ok": "OK",
        "version_status_error": "ERREUR",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "PC utilisateur",
        "deploy_mobile": "Mobile",
        "deploy_wearable": "Wearable",
        "deploy_dev-server": "Serveur de développement",
        "deploy_field-node": "Nœud de terrain",
        "deploy_server": "Serveur IA",
        "deploy_browser": "Client navigateur",
        "deploy_shared": "Partagé / tout l'écosystème",
        "maturity_production": "Production",
        "maturity_established": "Établi",
        "maturity_functional": "Fonctionnel",
        "maturity_scaffolding": "Ébauche",
        "maturity_desc_production": "Firmware réel pour une carte physique réelle que la propre documentation matérielle de cet écosystème décrit.",
        "maturity_desc_established": "Projet original, antérieur à l'expansion 2026, avec un long historique de versions réel - fiable sur cet historique, non ré-audité lors de cette passe.",
        "maturity_desc_functional": "Logique métier réelle et testée - vérifiée lors de cette passe (suite de tests propre / test de bout en bout réel / aller-retour réel d'un protocole compilé).",
        "maturity_desc_scaffolding": "Un point d'entrée réel et compilable existe ; la fonctionnalité pour laquelle le projet existe n'existe pas encore.",
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "Firmware",
        "role_library": "Bibliothèque",
        "role_service": "Service",
        "role_tool": "Outil",
        "role_docs": "Documentation",
        "role_hardware": "Conception matérielle",
    },
    "it": {
        "header_title": "Dashboard di stato dell'ecosistema",
        "subtitle_main": "{ok}/{total} repository risolti correttamente · {percent} in salute · metadati e versioni sono letti dal manifesto di ciascun repository · dashboard generata da GitHub Actions · GitHub Pages statico",
        "subtitle_v3": "v3: classificazione reale di maturità/ruolo, alberi famiglia/genitore-figlio e note per progetto più ricche - vedi la legenda Maturità qui sotto per sapere esattamente come è stato deciso ogni livello.",
        "freshness_checking_now": "Verifica dell'orario dell'ultima build in corso...",
        "freshness_unknown": "Ora dell'ultimo controllo non disponibile al momento (impossibile contattare l'API di GitHub Actions).",
        "freshness_failed": "Ultimo controllo completato: {conclusion} ({absolute}).",
        "freshness_checking": "Ultimo controllo riuscito: {age} fa ({absolute}).",
        "theme_toggle": "Cambia tema chiaro/scuro",
        "health_total": "Progetti totali",
        "health_resolved": "Versione risolta",
        "health_errors": "Errori / sconosciuto",
        "health_registry": "Stato dei manifesti",
        "section_deploy": "Target di deployment",
        "section_stack": "Stack tecnologici",
        "section_maturity": "Maturità",
        "section_maturity_hint": "clicca su una scheda per filtrare · passa il mouse per sapere come è stato deciso",
        "section_role": "Ruolo",
        "search_placeholder": "Cerca progetto, stack o deployment...",
        "search_aria": "Cerca progetti",
        "filter_all": "Tutti",
        "filter_ok": "✓ OK",
        "filter_error": "⚠ Errori",
        "family_label": "Famiglia:",
        "family_all": "Tutte le famiglie",
        "reset_filters": "⟲ Reimposta",
        "reset_filters_title": "Cancella la casella di ricerca e tutti i filtri attivi (stato, deployment, maturità, ruolo, famiglia)",
        "th_project": "Progetto",
        "th_type": "Tipo",
        "th_maturity": "Maturità",
        "th_stack": "Stack",
        "th_deploy": "Target di deployment",
        "th_version": "Versione",
        "th_status": "Stato",
        "th_commit": "Ultimo commit",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "Note",
        "detail_technology": "Tecnologia",
        "detail_build": "Build",
        "notes_empty": "Nessuna nota registrata ancora per questo progetto.",
        "empty_results": "Nessun progetto corrisponde ai filtri attuali.",
        "family_count": "{count} progetto/i",
        "family_parent_suffix": "è il vero genitore di integrazione di questa famiglia",
        "footer_registry": "Fonte dati:",
        "footer_generator": "Generatore della dashboard:",
        "footer_workflow": "Workflow:",
        "footer_note": "Il manifesto di ogni repository è la fonte di verità per i metadati pubblici e la versione.",
        "version_status_ok": "OK",
        "version_status_error": "ERRORE",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "PC dell'utente",
        "deploy_mobile": "Mobile",
        "deploy_wearable": "Wearable",
        "deploy_dev-server": "Server di sviluppo",
        "deploy_field-node": "Nodo di campo",
        "deploy_server": "Server IA",
        "deploy_browser": "Client browser",
        "deploy_shared": "Condiviso / tutto l'ecosistema",
        "maturity_production": "Produzione",
        "maturity_established": "Consolidato",
        "maturity_functional": "Funzionale",
        "maturity_scaffolding": "Impalcatura",
        "maturity_desc_production": "Firmware reale per una scheda fisica reale che la documentazione hardware di questo ecosistema descrive.",
        "maturity_desc_established": "Progetto originale, precedente all'espansione 2026, con una lunga storia di versioni reale - fidato su quella storia, non riverificato in questo passaggio.",
        "maturity_desc_functional": "Logica di business reale e testata - verificata in questo passaggio (suite di test propria / smoke test reale end-to-end / round-trip reale di un protocollo compilato).",
        "maturity_desc_scaffolding": "Esiste un punto di ingresso reale e compilabile; la funzionalità per cui il progetto esiste ancora no.",
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "Firmware",
        "role_library": "Libreria",
        "role_service": "Servizio",
        "role_tool": "Strumento",
        "role_docs": "Documentazione",
        "role_hardware": "Progettazione hardware",
    },
    "de": {
        "header_title": "Ökosystem-Statusdashboard",
        "subtitle_main": "{ok}/{total} Repositories erfolgreich aufgelöst · {percent} gesund · Metadaten und Versionen werden aus dem Manifest jedes Repositorys gelesen · Dashboard generiert von GitHub Actions · statisches GitHub Pages",
        "subtitle_v3": "v3: echte Reifegrad-/Rollen-Klassifizierung, Familie/Eltern-Kind-Bäume und umfangreichere Notizen pro Projekt - siehe die Legende 'Reifegrad' unten für genau, wie jede Stufe entschieden wurde.",
        "freshness_checking_now": "Letzte Build-Zeit wird geprüft...",
        "freshness_unknown": "Zeitpunkt der letzten Prüfung derzeit nicht verfügbar (GitHub-Actions-API nicht erreichbar).",
        "freshness_failed": "Letzte abgeschlossene Prüfung: {conclusion} ({absolute}).",
        "freshness_checking": "Letzte erfolgreiche Prüfung: vor {age} ({absolute}).",
        "theme_toggle": "Hell-/Dunkelmodus umschalten",
        "health_total": "Projekte insgesamt",
        "health_resolved": "Version aufgelöst",
        "health_errors": "Fehler / unbekannt",
        "health_registry": "Manifest-Zustand",
        "section_deploy": "Deploy-Ziele",
        "section_stack": "Technologie-Stacks",
        "section_maturity": "Reifegrad",
        "section_maturity_hint": "Karte anklicken zum Filtern · Hover zeigt, wie es entschieden wurde",
        "section_role": "Rolle",
        "search_placeholder": "Projekt, Stack oder Deploy-Ziel suchen...",
        "search_aria": "Projekte durchsuchen",
        "filter_all": "Alle",
        "filter_ok": "✓ OK",
        "filter_error": "⚠ Fehler",
        "family_label": "Familie:",
        "family_all": "Alle Familien",
        "reset_filters": "⟲ Zurücksetzen",
        "reset_filters_title": "Löscht das Suchfeld und alle aktiven Filter (Status, Deploy-Ziel, Reifegrad, Rolle, Familie)",
        "th_project": "Projekt",
        "th_type": "Typ",
        "th_maturity": "Reifegrad",
        "th_stack": "Stack",
        "th_deploy": "Deploy-Ziel",
        "th_version": "Version",
        "th_status": "Status",
        "th_commit": "Letzter Commit",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "Notizen",
        "detail_technology": "Technologie",
        "detail_build": "Build",
        "notes_empty": "Für dieses Projekt sind noch keine Notizen erfasst.",
        "empty_results": "Kein Projekt entspricht den aktuellen Filtern.",
        "family_count": "{count} Projekt(e)",
        "family_parent_suffix": "ist der echte Integrations-Elternteil dieser Familie",
        "footer_registry": "Datenquelle:",
        "footer_generator": "Dashboard-Generator:",
        "footer_workflow": "Workflow:",
        "footer_note": "Das Manifest jedes Repositorys ist die verlässliche Quelle für öffentliche Metadaten und Version.",
        "version_status_ok": "OK",
        "version_status_error": "FEHLER",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "Benutzer-PC",
        "deploy_mobile": "Mobil",
        "deploy_wearable": "Wearable",
        "deploy_dev-server": "Entwicklungsserver",
        "deploy_field-node": "Feldknoten",
        "deploy_server": "KI-Server",
        "deploy_browser": "Browser-Client",
        "deploy_shared": "Gemeinsam / gesamtes Ökosystem",
        "maturity_production": "Produktion",
        "maturity_established": "Etabliert",
        "maturity_functional": "Funktional",
        "maturity_scaffolding": "Grundgerüst",
        "maturity_desc_production": "Echte Firmware für eine echte, physische Platine, die die eigene Hardware-Dokumentation dieses Ökosystems beschreibt.",
        "maturity_desc_established": "Ursprüngliches Projekt von vor der 2026er-Erweiterung mit einer langen echten Versionshistorie - vertraut aufgrund dieser Historie, in diesem Durchgang nicht neu geprüft.",
        "maturity_desc_functional": "Echte, getestete Geschäftslogik - in diesem Durchgang verifiziert (eigene Testsuite / echter End-to-End-Smoketest / ein echter kompilierter Protokoll-Roundtrip).",
        "maturity_desc_scaffolding": "Ein echter, kompilierbarer Einstiegspunkt existiert; die Funktion, für die das Projekt existiert, noch nicht.",
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "Firmware",
        "role_library": "Bibliothek",
        "role_service": "Dienst",
        "role_tool": "Werkzeug",
        "role_docs": "Dokumentation",
        "role_hardware": "Hardware-Design",
    },
    "zh": {
        "header_title": "生态系统状态仪表盘",
        "subtitle_main": "{ok}/{total} 个仓库成功解析 · {percent} 健康 · 元数据和版本号直接从各仓库的清单文件读取 · 仪表盘由 GitHub Actions 生成 · 静态 GitHub Pages",
        "subtitle_v3": "v3：新增真实的成熟度/角色分类、家族/父子关系树，以及更丰富的逐项目说明——具体每个等级是如何判定的，见下方的“成熟度”图例。",
        "freshness_checking_now": "正在检查上次构建时间...",
        "freshness_unknown": "目前无法获取上次检查时间(无法连接 GitHub Actions API)。",
        "freshness_failed": "上次完成的检查结果:{conclusion}({absolute})。",
        "freshness_checking": "上次成功检查:{age}前({absolute})。",
        "theme_toggle": "切换深色/浅色主题",
        "health_total": "项目总数",
        "health_resolved": "已解析版本",
        "health_errors": "错误/未知",
        "health_registry": "清单健康度",
        "section_deploy": "部署目标",
        "section_stack": "技术栈",
        "section_maturity": "成熟度",
        "section_maturity_hint": "点击卡片可筛选 · 悬停查看判定依据",
        "section_role": "角色",
        "search_placeholder": "搜索项目、技术栈或部署目标……",
        "search_aria": "搜索项目",
        "filter_all": "全部",
        "filter_ok": "✓ 正常",
        "filter_error": "⚠ 错误",
        "family_label": "家族：",
        "family_all": "所有家族",
        "reset_filters": "⟲ 重置",
        "reset_filters_title": "清除搜索框以及所有已激活的筛选条件（状态、部署目标、成熟度、角色、家族）",
        "th_project": "项目",
        "th_type": "类型",
        "th_maturity": "成熟度",
        "th_stack": "技术栈",
        "th_deploy": "部署目标",
        "th_version": "版本",
        "th_status": "状态",
        "th_commit": "最新提交",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "说明",
        "detail_technology": "技术",
        "detail_build": "构建",
        "notes_empty": "该项目目前还没有记录说明。",
        "empty_results": "没有项目匹配当前的筛选条件。",
        "family_count": "{count} 个项目",
        "family_parent_suffix": "是该家族真正的集成父项目",
        "footer_registry": "数据来源：",
        "footer_generator": "仪表盘生成器：",
        "footer_workflow": "工作流：",
        "footer_note": "每个仓库的清单文件是其公开元数据和版本号的唯一真实来源。",
        "version_status_ok": "正常",
        "version_status_error": "错误",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "用户电脑",
        "deploy_mobile": "移动端",
        "deploy_wearable": "可穿戴设备",
        "deploy_dev-server": "开发服务器",
        "deploy_field-node": "现场节点",
        "deploy_server": "AI 服务器",
        "deploy_browser": "浏览器客户端",
        "deploy_shared": "共享 / 整个生态系统",
        "maturity_production": "生产",
        "maturity_established": "成熟",
        "maturity_functional": "功能完备",
        "maturity_scaffolding": "脚手架",
        "maturity_desc_production": "真实的固件，对应本生态系统自身硬件文档中描述的真实物理电路板。",
        "maturity_desc_established": "2026 年扩展之前就存在的原始项目，拥有真实且长期的版本历史——基于该历史被信任，本轮未重新审计。",
        "maturity_desc_functional": "真实、经过测试的业务逻辑——已在本轮验证（自有测试套件 / 真实的端到端冒烟测试 / 真实的编译协议往返）。",
        "maturity_desc_scaffolding": "已有真实可编译的入口点；但该项目存在的目的所对应的功能尚未实现。",
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "固件",
        "role_library": "库",
        "role_service": "服务",
        "role_tool": "工具",
        "role_docs": "文档",
        "role_hardware": "硬件设计",
    },
    "ja": {
        "header_title": "エコシステム ステータスダッシュボード",
        "subtitle_main": "{ok}/{total} 個のリポジトリが正常に解決 · {percent} が健全 · メタデータとバージョンは各リポジトリのマニフェストから読み取り · ダッシュボードは GitHub Actions によって生成 · 静的な GitHub Pages",
        "subtitle_v3": "v3：実際の成熟度/役割分類、ファミリー/親子ツリー、そしてより充実したプロジェクトごとの注記を追加しました——各レベルが具体的にどう判定されたかは、下部の成熟度の凡例を参照してください。",
        "freshness_checking_now": "直近のビルド時刻を確認しています...",
        "freshness_unknown": "現在、直近のチェック時刻を取得できません(GitHub Actions API に接続できませんでした)。",
        "freshness_failed": "直近の完了したチェック結果:{conclusion}({absolute})。",
        "freshness_checking": "直近の成功したチェック:{age}前({absolute})。",
        "theme_toggle": "ダーク/ライトテーマを切り替え",
        "health_total": "プロジェクト総数",
        "health_resolved": "バージョン解決済み",
        "health_errors": "エラー / 不明",
        "health_registry": "マニフェストの健全性",
        "section_deploy": "デプロイ対象",
        "section_stack": "技術スタック",
        "section_maturity": "成熟度",
        "section_maturity_hint": "カードをクリックして絞り込み · ホバーで判定理由を表示",
        "section_role": "役割",
        "search_placeholder": "プロジェクト、スタック、デプロイ対象を検索...",
        "search_aria": "プロジェクトを検索",
        "filter_all": "すべて",
        "filter_ok": "✓ OK",
        "filter_error": "⚠ エラー",
        "family_label": "ファミリー：",
        "family_all": "すべてのファミリー",
        "reset_filters": "⟲ リセット",
        "reset_filters_title": "検索欄とすべてのアクティブなフィルター（状態、デプロイ対象、成熟度、役割、ファミリー）をクリアします",
        "th_project": "プロジェクト",
        "th_type": "種別",
        "th_maturity": "成熟度",
        "th_stack": "スタック",
        "th_deploy": "デプロイ対象",
        "th_version": "バージョン",
        "th_status": "ステータス",
        "th_commit": "最新コミット",
        "link_actions": "Actions",
        "link_issues": "Issues",
        "detail_notes": "注記",
        "detail_technology": "技術",
        "detail_build": "ビルド",
        "notes_empty": "このプロジェクトにはまだ注記が記録されていません。",
        "empty_results": "現在のフィルター条件に一致するプロジェクトはありません。",
        "family_count": "{count} 件のプロジェクト",
        "family_parent_suffix": "がこのファミリーの実際の統合親プロジェクトです",
        "footer_registry": "データソース：",
        "footer_generator": "ダッシュボード生成スクリプト：",
        "footer_workflow": "ワークフロー：",
        "footer_note": "各リポジトリのマニフェストは、公開メタデータとバージョンの唯一の信頼できる情報源です。",
        "version_status_ok": "OK",
        "version_status_error": "エラー",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "ユーザーPC",
        "deploy_mobile": "モバイル",
        "deploy_wearable": "ウェアラブル",
        "deploy_dev-server": "開発サーバー",
        "deploy_field-node": "フィールドノード",
        "deploy_server": "AIサーバー",
        "deploy_browser": "ブラウザクライアント",
        "deploy_shared": "共有 / エコシステム全体",
        "maturity_production": "本番",
        "maturity_established": "定着済み",
        "maturity_functional": "機能実装済み",
        "maturity_scaffolding": "骨組み",
        "maturity_desc_production": "この生態系自身のハードウェアドキュメントが説明する、実際の物理的な PCB 向けの本物のファームウェア。",
        "maturity_desc_established": "2026年の拡張以前から存在するオリジナルプロジェクトで、長く実際のバージョン履歴を持つ——その履歴に基づいて信頼されており、今回の作業で改めて監査されたわけではない。",
        "maturity_desc_functional": "実際にテストされた本物のビジネスロジック——今回の作業で検証済み（自前のテストスイート / 実際のエンドツーエンドのスモークテスト / 実際にコンパイルされたプロトコルの往復）。",
        "maturity_desc_scaffolding": "実際にコンパイル可能なエントリーポイントは存在するが、そのプロジェクトが本来目指す機能はまだ存在しない。",
        "role_api": "API",
        "role_ui": "UI",
        "role_cli": "CLI",
        "role_firmware": "ファームウェア",
        "role_library": "ライブラリ",
        "role_service": "サービス",
        "role_tool": "ツール",
        "role_docs": "ドキュメント",
        "role_hardware": "ハードウェア設計",
    },
}

# Architecture text is kept separate from the UI chrome above so that the
# public technical model stays equally available in every dashboard language.
ARCHITECTURE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "architecture_intro": "Electro Hobby 3D is three independent engineering ecosystems by the same author: HYDRA-UMC (industrial multi-robot platform), URTC (its universal robot-tool subsystem, an independent product with its own firmware) and A.R.M.O.R. (perimeter security and home automation). This dashboard discovers and lists every one of them live; each ecosystem's own family groups are labeled below, and HYDRA-UMC's own deeper architecture is detailed in the section right after this one.",
        "architecture_section": "HYDRA-UMC: System architecture", "architecture_platform_title": "Platform foundation", "architecture_platform_body": "Raspberry Pi OS ARM64 remains the operating-system base. The HYDRA-UMC layer adds device profiles, diagnostics and service lifecycle.",
        "architecture_contracts_title": "Contracts and operations", "architecture_contracts_body": "The SDK defines stable data and command contracts; Server, UI and tools use those contracts instead of raw hardware protocols.",
        "architecture_perception_title": "Perception and intelligence", "architecture_perception_body": "Vision and AI are optional capabilities. Their output is validated before it can influence a mission; they are never safety authority.",
        "architecture_engineering_title": "Engineering and industry", "architecture_engineering_body": "Simulation, telemetry and standards make the physical cell observable, testable and interoperable.",
        "architecture_flow_operator": "Operator interfaces", "architecture_flow_services": "Server and SDK", "architecture_flow_adapter": "CM5-MCU adapter", "architecture_flow_machine": "MCU / URTC / machine",
        "architecture_relationship_title": "HYDRA-UMC and URTC:", "architecture_relationship_body": "HYDRA-UMC is the platform and cell controller. URTC is its universal robot-tool subsystem, with independent firmware and maintenance tools. The MCU remains authoritative for physical limits and safe stop; UI, network and AI cannot bypass that boundary.",
        "table_hydra_umc_banner": "HYDRA-UMC - the industrial multi-robot platform and cell controller, this dashboard's first ecosystem.", "table_urtc_banner": "URTC - an independent product with its own firmware and maintenance tools, coordinated with HYDRA-UMC over FDCAN.", "table_armor_banner": "A.R.M.O.R. - a separate, public perimeter-security and home-automation ecosystem, same author.",
        "section_by_ecosystem": "Projects by ecosystem",
        "architecture_section_u": "URTC: System architecture",
        "architecture_u_card1_title": "Tool-head firmware", "architecture_u_card1_body": "An STM32F303 runs each tool head over CAN, reading its own 5-bit hardware address to auto-configure power stages, sensors and safety logic for one of 25 built-in tool profiles.",
        "architecture_u_card2_title": "Expansion and motion", "architecture_u_card2_body": "A 20-pin expansion connector adds a second stepper axis or sensor board through one of six interchangeable variants, sharing STEP/DIR/EN wiring between a TMC2209 and a TMC5160 driver.",
        "architecture_u_card3_title": "Maintenance tools", "architecture_u_card3_body": "URTC-FLASHER updates firmware over CAN without removing the board, URTC-TESTER exercises the protocol end to end and URTC-UPDATER keeps every desktop tool current from GitHub.",
        "architecture_u_card4_title": "Vision and operation", "architecture_u_card4_body": "URTC-VISION-TOOL adds camera-based tool inspection, URTC-WEB-STUDIO gives it a browser console and URTC-SMART-RACK stores and identifies tool heads between changes.",
        "architecture_u_flow_1": "Tool head", "architecture_u_flow_2": "STM32F303 firmware", "architecture_u_flow_3": "CAN bus", "architecture_u_flow_4": "HYDRA-UMC MCU / host",
        "architecture_u_rel_title": "URTC on its own, and paired with HYDRA-UMC:", "architecture_u_rel_body": "URTC is an independent, unofficial project - a CAN-based tool-head controller built to work with PAROL6/Faze4-style arms, with its own firmware, hardware and maintenance tools. When it is the tool subsystem of a HYDRA-UMC cell, HYDRA-UMC's own MCU keeps authority over physical limits and safe stop; URTC never bypasses that boundary.",
        "architecture_section_a": "A.R.M.O.R.: System architecture",
        "architecture_a_card1_title": "Network segmentation", "architecture_a_card1_body": "Field nodes and cameras sit on their own VLAN with no internet access; the MQTT broker and server live on a core VLAN; Studio and the Android app reach the server from a client VLAN.",
        "architecture_a_card2_title": "Field nodes", "architecture_a_card2_body": "ESP32-S3 radar, solar and electrical nodes publish sensor and equipment readings; the solar and electrical ones only read, never write to an inverter, battery or meter.",
        "architecture_a_card3_title": "Perception, never authority", "architecture_a_card3_body": "Visual and voice AI recommend a severity or an intent with reasons attached; authorizes_action is always false until the server itself authenticates and confirms.",
        "architecture_a_card4_title": "State and operator consoles", "architecture_a_card4_body": "ARMOR-SERVER is the only place that ever touches a camera password or an RTSP address; Studio and the Android app are its authenticated clients, and a phone can set a new node up over Bluetooth alone.",
        "architecture_a_flow_1": "Field nodes and cameras", "architecture_a_flow_2": "MQTT broker and server", "architecture_a_flow_3": "AI recommendation", "architecture_a_flow_4": "Authenticated client session",
        "architecture_a_rel_title": "A.R.M.O.R.'s own boundary:", "architecture_a_rel_body": "The server is the only component that authorises an action or holds a camera credential. Visual and voice AI only recommend; solar and electrical nodes only read - the rules for switching an electrical source are tested in software but not yet linked to any real hardware.",
    },
    "es": {
        "architecture_intro": "Electro Hobby 3D son tres ecosistemas de ingeniería independientes del mismo autor: HYDRA-UMC (plataforma industrial multi-robot), URTC (su subsistema universal de herramientas, un producto independiente con firmware propio) y A.R.M.O.R. (seguridad perimetral y automatización del hogar). Este panel descubre y lista los tres en vivo; los grupos de familia de cada ecosistema aparecen etiquetados más abajo, y la arquitectura propia de cada uno se detalla en su propia sección más abajo.",
        "architecture_section": "HYDRA-UMC: Arquitectura del sistema", "architecture_platform_title": "Base de plataforma", "architecture_platform_body": "Raspberry Pi OS ARM64 mantiene el papel de sistema operativo base. La capa HYDRA-UMC aporta perfiles de dispositivo, diagnóstico y ciclo de vida de servicios.",
        "architecture_contracts_title": "Contratos y operaciones", "architecture_contracts_body": "El SDK define contratos estables de datos y comandos; Server, las interfaces y las herramientas los usan en lugar de protocolos de hardware sin abstraer.",
        "architecture_perception_title": "Percepción e inteligencia", "architecture_perception_body": "La visión y la IA son capacidades opcionales. Su salida se valida antes de influir en una misión y nunca tiene autoridad de seguridad.",
        "architecture_engineering_title": "Ingeniería e industria", "architecture_engineering_body": "La simulación, la telemetría y los estándares hacen que la celda física sea observable, comprobable e interoperable.",
        "architecture_flow_operator": "Interfaces de operador", "architecture_flow_services": "Server y SDK", "architecture_flow_adapter": "Adaptador CM5-MCU", "architecture_flow_machine": "MCU / URTC / máquina",
        "architecture_relationship_title": "HYDRA-UMC y URTC:", "architecture_relationship_body": "HYDRA-UMC es la plataforma y el controlador de celda. URTC es su subsistema universal de herramientas robóticas, con firmware y utilidades de mantenimiento independientes. El MCU conserva la autoridad sobre límites físicos y parada segura; UI, red e IA no pueden saltarse esa frontera.",
        "table_hydra_umc_banner": "HYDRA-UMC - la plataforma industrial multi-robot y el controlador de celda, el primer ecosistema de este panel.", "table_urtc_banner": "URTC - un producto independiente con firmware y utilidades de mantenimiento propios, coordinado con HYDRA-UMC por FDCAN.", "table_armor_banner": "A.R.M.O.R. - un ecosistema aparte, publico, de seguridad perimetral y automatizacion del hogar, del mismo autor.",
        "section_by_ecosystem": "Proyectos por ecosistema",
        "architecture_section_u": "URTC: Arquitectura del sistema",
        "architecture_u_card1_title": "Firmware del cabezal de herramienta", "architecture_u_card1_body": "Un STM32F303 controla cada cabezal de herramienta por CAN, leyendo su propia dirección de 5 bits para autoconfigurar las etapas de potencia, los sensores y la lógica de seguridad de uno de 25 perfiles de herramienta integrados.",
        "architecture_u_card2_title": "Expansión y movimiento", "architecture_u_card2_body": "Un conector de expansión de 20 pines añade un segundo eje paso a paso o una placa de sensores mediante una de seis variantes intercambiables, compartiendo el cableado STEP/DIR/EN entre un driver TMC2209 y uno TMC5160.",
        "architecture_u_card3_title": "Herramientas de mantenimiento", "architecture_u_card3_body": "URTC-FLASHER actualiza el firmware por CAN sin desmontar la placa, URTC-TESTER ejercita el protocolo de extremo a extremo y URTC-UPDATER mantiene actualizadas todas las herramientas de escritorio desde GitHub.",
        "architecture_u_card4_title": "Visión y operación", "architecture_u_card4_body": "URTC-VISION-TOOL añade inspección de herramientas por cámara, URTC-WEB-STUDIO le da una consola de navegador y URTC-SMART-RACK almacena e identifica los cabezales entre cambios.",
        "architecture_u_flow_1": "Cabezal de herramienta", "architecture_u_flow_2": "Firmware STM32F303", "architecture_u_flow_3": "Bus CAN", "architecture_u_flow_4": "MCU / host HYDRA-UMC",
        "architecture_u_rel_title": "URTC solo, y emparejado con HYDRA-UMC:", "architecture_u_rel_body": "URTC es un proyecto independiente y no oficial: un controlador de cabezal por CAN pensado para brazos tipo PAROL6/Faze4, con firmware, hardware y herramientas de mantenimiento propios. Cuando actúa como subsistema de herramientas de una celda HYDRA-UMC, el MCU de HYDRA-UMC conserva la autoridad sobre los límites físicos y la parada segura; URTC nunca se salta esa frontera.",
        "architecture_section_a": "A.R.M.O.R.: Arquitectura del sistema",
        "architecture_a_card1_title": "Segmentación de red", "architecture_a_card1_body": "Los nodos de campo y las cámaras están en su propia VLAN sin acceso a internet; el broker MQTT y el servidor viven en una VLAN núcleo; Studio y la app Android llegan al servidor desde una VLAN de clientes.",
        "architecture_a_card2_title": "Nodos de campo", "architecture_a_card2_body": "Los nodos ESP32-S3 de radar, solares y eléctricos publican lecturas de sensores y equipos; los solares y eléctricos solo leen, nunca escriben en un inversor, una batería o un medidor.",
        "architecture_a_card3_title": "Percepción, nunca autoridad", "architecture_a_card3_body": "La IA visual y de voz recomiendan una gravedad o una intención con sus razones; authorizes_action siempre es falso hasta que el propio servidor autentica y confirma.",
        "architecture_a_card4_title": "Estado y consolas de operador", "architecture_a_card4_body": "ARMOR-SERVER es el único lugar que toca una contraseña de cámara o una dirección RTSP; Studio y la app Android son sus clientes autenticados, y un teléfono puede configurar un nodo nuevo solo por Bluetooth.",
        "architecture_a_flow_1": "Nodos de campo y cámaras", "architecture_a_flow_2": "Broker MQTT y servidor", "architecture_a_flow_3": "Recomendación de IA", "architecture_a_flow_4": "Sesión de cliente autenticada",
        "architecture_a_rel_title": "La frontera propia de A.R.M.O.R.:", "architecture_a_rel_body": "El servidor es el único componente que autoriza una acción o guarda una credencial de cámara. La IA visual y de voz solo recomiendan; los nodos solares y eléctricos solo leen - las reglas para maniobrar una fuente eléctrica están probadas en software pero aún no conectadas a ningún hardware real.",
    },
    "fr": {
        "architecture_intro": "Electro Hobby 3D regroupe trois écosystèmes d'ingénierie indépendants du même auteur : HYDRA-UMC (plateforme industrielle multi-robot), URTC (son sous-système universel d'outils, un produit indépendant avec son propre firmware) et A.R.M.O.R. (sécurité périmétrique et domotique). Ce tableau de bord découvre et liste les trois en direct ; les groupes de famille de chaque écosystème sont indiqués plus bas, et l'architecture propre de chacun est détaillée dans sa propre section plus bas.",
        "architecture_section": "HYDRA-UMC : Architecture du système", "architecture_platform_title": "Fondation de plateforme", "architecture_platform_body": "Raspberry Pi OS ARM64 reste la base du système d’exploitation. La couche HYDRA-UMC apporte profils d’appareil, diagnostic et cycle de vie des services.",
        "architecture_contracts_title": "Contrats et opérations", "architecture_contracts_body": "Le SDK définit des contrats stables de données et de commandes ; Server, les interfaces et les outils les utilisent au lieu de protocoles matériels bruts.",
        "architecture_perception_title": "Perception et intelligence", "architecture_perception_body": "La vision et l’IA sont des capacités optionnelles. Leur sortie est validée avant d’influencer une mission et n’a jamais autorité sur la sécurité.",
        "architecture_engineering_title": "Ingénierie et industrie", "architecture_engineering_body": "Simulation, télémétrie et standards rendent la cellule physique observable, testable et interopérable.",
        "architecture_flow_operator": "Interfaces opérateur", "architecture_flow_services": "Server et SDK", "architecture_flow_adapter": "Adaptateur CM5-MCU", "architecture_flow_machine": "MCU / URTC / machine",
        "architecture_relationship_title": "HYDRA-UMC et URTC :", "architecture_relationship_body": "HYDRA-UMC est la plateforme et le contrôleur de cellule. URTC est son sous-système universel d’outils robotiques, avec firmware et outils de maintenance indépendants. Le MCU garde l’autorité sur les limites physiques et l’arrêt sûr ; interface, réseau et IA ne peuvent pas contourner cette frontière.",
        "table_hydra_umc_banner": "HYDRA-UMC - la plateforme industrielle multi-robot et le contrôleur de cellule, le premier écosystème de ce tableau de bord.", "table_urtc_banner": "URTC - un produit indépendant avec son propre firmware et ses propres outils de maintenance, coordonné avec HYDRA-UMC via FDCAN.", "table_armor_banner": "A.R.M.O.R. - un écosystème séparé et public de sécurité périmétrique et de domotique, du même auteur.",
        "section_by_ecosystem": "Projets par écosystème",
        "architecture_section_u": "URTC : Architecture du système",
        "architecture_u_card1_title": "Firmware de la tête d'outil", "architecture_u_card1_body": "Un STM32F303 pilote chaque tête d'outil par CAN, en lisant sa propre adresse matérielle sur 5 bits pour configurer automatiquement les étages de puissance, les capteurs et la logique de sécurité de l'un des 25 profils d'outil intégrés.",
        "architecture_u_card2_title": "Extension et mouvement", "architecture_u_card2_body": "Un connecteur d'extension à 20 broches ajoute un second axe pas à pas ou une carte de capteurs via l'une des six variantes interchangeables, en partageant le câblage STEP/DIR/EN entre un driver TMC2209 et un TMC5160.",
        "architecture_u_card3_title": "Outils de maintenance", "architecture_u_card3_body": "URTC-FLASHER met à jour le firmware par CAN sans démonter la carte, URTC-TESTER teste le protocole de bout en bout et URTC-UPDATER maintient tous les outils de bureau à jour depuis GitHub.",
        "architecture_u_card4_title": "Vision et exploitation", "architecture_u_card4_body": "URTC-VISION-TOOL ajoute l'inspection des outils par caméra, URTC-WEB-STUDIO lui donne une console dans le navigateur et URTC-SMART-RACK stocke et identifie les têtes d'outil entre deux changements.",
        "architecture_u_flow_1": "Tête d'outil", "architecture_u_flow_2": "Firmware STM32F303", "architecture_u_flow_3": "Bus CAN", "architecture_u_flow_4": "MCU / hôte HYDRA-UMC",
        "architecture_u_rel_title": "URTC seul, et associé à HYDRA-UMC :", "architecture_u_rel_body": "URTC est un projet indépendant et non officiel : un contrôleur de tête d'outil par CAN conçu pour des bras de type PAROL6/Faze4, avec son propre firmware, son propre matériel et ses propres outils de maintenance. Lorsqu'il est le sous-système d'outils d'une cellule HYDRA-UMC, le MCU de HYDRA-UMC garde l'autorité sur les limites physiques et l'arrêt sûr ; URTC ne contourne jamais cette frontière.",
        "architecture_section_a": "A.R.M.O.R. : Architecture du système",
        "architecture_a_card1_title": "Segmentation réseau", "architecture_a_card1_body": "Les nœuds de terrain et les caméras se trouvent sur leur propre VLAN sans accès à internet ; le broker MQTT et le serveur vivent sur un VLAN cœur ; Studio et l'application Android atteignent le serveur depuis un VLAN clients.",
        "architecture_a_card2_title": "Nœuds de terrain", "architecture_a_card2_body": "Les nœuds ESP32-S3 radar, solaires et électriques publient les relevés des capteurs et des équipements ; les nœuds solaires et électriques ne font que lire, jamais écrire sur un onduleur, une batterie ou un compteur.",
        "architecture_a_card3_title": "Perception, jamais autorité", "architecture_a_card3_body": "L'IA visuelle et vocale recommande une gravité ou une intention avec ses raisons ; authorizes_action reste toujours faux tant que le serveur lui-même n'authentifie et ne confirme pas.",
        "architecture_a_card4_title": "État et consoles opérateur", "architecture_a_card4_body": "ARMOR-SERVER est le seul endroit qui touche un mot de passe de caméra ou une adresse RTSP ; Studio et l'application Android en sont les clients authentifiés, et un téléphone peut configurer un nouveau nœud uniquement par Bluetooth.",
        "architecture_a_flow_1": "Nœuds de terrain et caméras", "architecture_a_flow_2": "Broker MQTT et serveur", "architecture_a_flow_3": "Recommandation de l'IA", "architecture_a_flow_4": "Session client authentifiée",
        "architecture_a_rel_title": "La frontière propre d'A.R.M.O.R. :", "architecture_a_rel_body": "Le serveur est le seul composant à autoriser une action ou à détenir un identifiant de caméra. L'IA visuelle et vocale ne fait que recommander ; les nœuds solaires et électriques ne font que lire - les règles de manœuvre d'une source électrique sont testées en logiciel mais pas encore reliées à un matériel réel.",
    },
    "it": {
        "architecture_intro": "Electro Hobby 3D è composto da tre ecosistemi ingegneristici indipendenti dello stesso autore: HYDRA-UMC (piattaforma industriale multi-robot), URTC (il suo sottosistema universale di utensili, un prodotto indipendente con firmware proprio) e A.R.M.O.R. (sicurezza perimetrale e domotica). Questa dashboard scopre ed elenca tutti e tre dal vivo; i gruppi di famiglia di ogni ecosistema sono etichettati più sotto, e l'architettura propria di ciascuno è descritta nella sua sezione più sotto.",
        "architecture_section": "HYDRA-UMC: Architettura del sistema", "architecture_platform_title": "Fondazione della piattaforma", "architecture_platform_body": "Raspberry Pi OS ARM64 rimane la base del sistema operativo. Il livello HYDRA-UMC aggiunge profili dispositivo, diagnostica e ciclo di vita dei servizi.",
        "architecture_contracts_title": "Contratti e operazioni", "architecture_contracts_body": "L’SDK definisce contratti stabili per dati e comandi; Server, UI e strumenti li usano invece di protocolli hardware grezzi.",
        "architecture_perception_title": "Percezione e intelligenza", "architecture_perception_body": "Visione e IA sono capacità opzionali. Il loro output viene convalidato prima di influire su una missione e non ha mai autorità sulla sicurezza.",
        "architecture_engineering_title": "Ingegneria e industria", "architecture_engineering_body": "Simulazione, telemetria e standard rendono la cella fisica osservabile, verificabile e interoperabile.",
        "architecture_flow_operator": "Interfacce operatore", "architecture_flow_services": "Server e SDK", "architecture_flow_adapter": "Adattatore CM5-MCU", "architecture_flow_machine": "MCU / URTC / macchina",
        "architecture_relationship_title": "HYDRA-UMC e URTC:", "architecture_relationship_body": "HYDRA-UMC è la piattaforma e il controllore di cella. URTC è il suo sottosistema universale per utensili robotici, con firmware e strumenti di manutenzione indipendenti. Il MCU mantiene l’autorità sui limiti fisici e sull’arresto sicuro; UI, rete e IA non possono aggirare quel confine.",
        "table_hydra_umc_banner": "HYDRA-UMC - la piattaforma industriale multi-robot e il controllore di cella, il primo ecosistema di questa dashboard.", "table_urtc_banner": "URTC - un prodotto indipendente con firmware e strumenti di manutenzione propri, coordinato con HYDRA-UMC via FDCAN.", "table_armor_banner": "A.R.M.O.R. - un ecosistema a parte, pubblico, di sicurezza perimetrale e domotica, dello stesso autore.",
        "section_by_ecosystem": "Progetti per ecosistema",
        "architecture_section_u": "URTC: Architettura del sistema",
        "architecture_u_card1_title": "Firmware della testa utensile", "architecture_u_card1_body": "Uno STM32F303 pilota ogni testa utensile via CAN, leggendo il proprio indirizzo hardware a 5 bit per configurare automaticamente stadi di potenza, sensori e logica di sicurezza di uno dei 25 profili utensile integrati.",
        "architecture_u_card2_title": "Espansione e movimento", "architecture_u_card2_body": "Un connettore di espansione a 20 pin aggiunge un secondo asse passo-passo o una scheda sensori tramite una delle sei varianti intercambiabili, condividendo il cablaggio STEP/DIR/EN tra un driver TMC2209 e uno TMC5160.",
        "architecture_u_card3_title": "Strumenti di manutenzione", "architecture_u_card3_body": "URTC-FLASHER aggiorna il firmware via CAN senza smontare la scheda, URTC-TESTER verifica il protocollo end-to-end e URTC-UPDATER mantiene aggiornati tutti gli strumenti desktop da GitHub.",
        "architecture_u_card4_title": "Visione e operatività", "architecture_u_card4_body": "URTC-VISION-TOOL aggiunge l'ispezione degli utensili tramite telecamera, URTC-WEB-STUDIO offre una console da browser e URTC-SMART-RACK conserva e identifica le teste utensile tra un cambio e l'altro.",
        "architecture_u_flow_1": "Testa utensile", "architecture_u_flow_2": "Firmware STM32F303", "architecture_u_flow_3": "Bus CAN", "architecture_u_flow_4": "MCU / host HYDRA-UMC",
        "architecture_u_rel_title": "URTC da solo, e abbinato a HYDRA-UMC:", "architecture_u_rel_body": "URTC è un progetto indipendente e non ufficiale: un controllore di testa utensile via CAN pensato per bracci del tipo PAROL6/Faze4, con firmware, hardware e strumenti di manutenzione propri. Quando è il sottosistema utensili di una cella HYDRA-UMC, l'MCU di HYDRA-UMC mantiene l'autorità sui limiti fisici e sull'arresto sicuro; URTC non aggira mai questo confine.",
        "architecture_section_a": "A.R.M.O.R.: Architettura del sistema",
        "architecture_a_card1_title": "Segmentazione di rete", "architecture_a_card1_body": "I nodi di campo e le telecamere stanno su una propria VLAN senza accesso a internet; il broker MQTT e il server vivono su una VLAN core; Studio e l'app Android raggiungono il server da una VLAN client.",
        "architecture_a_card2_title": "Nodi di campo", "architecture_a_card2_body": "I nodi ESP32-S3 radar, solari ed elettrici pubblicano le letture di sensori ed equipaggiamenti; quelli solari ed elettrici solo leggono, mai scrivono su un inverter, una batteria o un contatore.",
        "architecture_a_card3_title": "Percezione, mai autorità", "architecture_a_card3_body": "L'IA visiva e vocale raccomanda una gravità o un'intenzione con le proprie motivazioni; authorizes_action è sempre falso finché il server stesso non autentica e conferma.",
        "architecture_a_card4_title": "Stato e console operatore", "architecture_a_card4_body": "ARMOR-SERVER è l'unico punto che tocca una password di telecamera o un indirizzo RTSP; Studio e l'app Android ne sono i client autenticati, e un telefono può configurare un nuovo nodo solo via Bluetooth.",
        "architecture_a_flow_1": "Nodi di campo e telecamere", "architecture_a_flow_2": "Broker MQTT e server", "architecture_a_flow_3": "Raccomandazione dell'IA", "architecture_a_flow_4": "Sessione client autenticata",
        "architecture_a_rel_title": "Il confine proprio di A.R.M.O.R.:", "architecture_a_rel_body": "Il server è l'unico componente che autorizza un'azione o detiene una credenziale di telecamera. L'IA visiva e vocale solo raccomanda; i nodi solari ed elettrici solo leggono - le regole per manovrare una fonte elettrica sono testate via software ma non ancora collegate a hardware reale.",
    },
    "de": {
        "architecture_intro": "Electro Hobby 3D besteht aus drei unabhängigen Engineering-Ökosystemen desselben Autors: HYDRA-UMC (industrielle Multi-Roboter-Plattform), URTC (dessen universelles Werkzeug-Subsystem, ein eigenständiges Produkt mit eigener Firmware) und A.R.M.O.R. (Perimetersicherheit und Hausautomation). Dieses Dashboard entdeckt und listet alle drei live auf; die Familiengruppen jedes Ökosystems sind weiter unten gekennzeichnet, und die eigene Architektur jedes Ökosystems wird in seinem eigenen Abschnitt weiter unten beschrieben.",
        "architecture_section": "HYDRA-UMC: Systemarchitektur", "architecture_platform_title": "Plattformbasis", "architecture_platform_body": "Raspberry Pi OS ARM64 bleibt die Betriebssystembasis. Die HYDRA-UMC-Schicht ergänzt Geräteprofile, Diagnose und den Lebenszyklus der Dienste.",
        "architecture_contracts_title": "Verträge und Betrieb", "architecture_contracts_body": "Das SDK definiert stabile Daten- und Befehlsverträge; Server, Oberflächen und Werkzeuge verwenden sie statt roher Hardwareprotokolle.",
        "architecture_perception_title": "Wahrnehmung und Intelligenz", "architecture_perception_body": "Vision und KI sind optionale Fähigkeiten. Ihre Ausgabe wird validiert, bevor sie eine Mission beeinflussen kann; sie besitzen nie Sicherheitsautorität.",
        "architecture_engineering_title": "Engineering und Industrie", "architecture_engineering_body": "Simulation, Telemetrie und Standards machen die physische Zelle beobachtbar, testbar und interoperabel.",
        "architecture_flow_operator": "Bedienoberflächen", "architecture_flow_services": "Server und SDK", "architecture_flow_adapter": "CM5-MCU-Adapter", "architecture_flow_machine": "MCU / URTC / Maschine",
        "architecture_relationship_title": "HYDRA-UMC und URTC:", "architecture_relationship_body": "HYDRA-UMC ist Plattform und Zellensteuerung. URTC ist das universelle Roboterwerkzeug-Subsystem mit unabhängiger Firmware und Wartungswerkzeugen. Der MCU behält die Autorität über physische Grenzen und sicheren Stopp; UI, Netzwerk und KI können diese Grenze nicht umgehen.",
        "table_hydra_umc_banner": "HYDRA-UMC - die industrielle Multi-Roboter-Plattform und Zellcontroller, das erste Ökosystem dieses Dashboards.", "table_urtc_banner": "URTC - ein eigenständiges Produkt mit eigener Firmware und eigenen Wartungswerkzeugen, über FDCAN mit HYDRA-UMC koordiniert.", "table_armor_banner": "A.R.M.O.R. - ein separates, öffentliches Ökosystem für Perimetersicherheit und Hausautomation desselben Autors.",
        "section_by_ecosystem": "Projekte nach Ökosystem",
        "architecture_section_u": "URTC: Systemarchitektur",
        "architecture_u_card1_title": "Werkzeugkopf-Firmware", "architecture_u_card1_body": "Ein STM32F303 steuert jeden Werkzeugkopf über CAN und liest seine eigene 5-Bit-Hardwareadresse aus, um Leistungsstufen, Sensoren und Sicherheitslogik für eines von 25 integrierten Werkzeugprofilen automatisch zu konfigurieren.",
        "architecture_u_card2_title": "Erweiterung und Bewegung", "architecture_u_card2_body": "Ein 20-poliger Erweiterungsstecker fügt über eine von sechs austauschbaren Varianten eine zweite Schrittmotorachse oder eine Sensorplatine hinzu und teilt sich die STEP/DIR/EN-Verkabelung zwischen einem TMC2209- und einem TMC5160-Treiber.",
        "architecture_u_card3_title": "Wartungswerkzeuge", "architecture_u_card3_body": "URTC-FLASHER aktualisiert die Firmware über CAN, ohne die Platine auszubauen, URTC-TESTER prüft das Protokoll durchgehend, und URTC-UPDATER hält alle Desktop-Werkzeuge von GitHub aus aktuell.",
        "architecture_u_card4_title": "Bildverarbeitung und Betrieb", "architecture_u_card4_body": "URTC-VISION-TOOL ergänzt die kamerabasierte Werkzeugprüfung, URTC-WEB-STUDIO gibt ihr eine Browser-Konsole, und URTC-SMART-RACK speichert und identifiziert Werkzeugköpfe zwischen den Wechseln.",
        "architecture_u_flow_1": "Werkzeugkopf", "architecture_u_flow_2": "STM32F303-Firmware", "architecture_u_flow_3": "CAN-Bus", "architecture_u_flow_4": "HYDRA-UMC-MCU / -Host",
        "architecture_u_rel_title": "URTC allein, und im Verbund mit HYDRA-UMC:", "architecture_u_rel_body": "URTC ist ein unabhängiges, inoffizielles Projekt - ein CAN-basierter Werkzeugkopf-Controller für Arme vom Typ PAROL6/Faze4, mit eigener Firmware, eigener Hardware und eigenen Wartungswerkzeugen. Als Werkzeug-Subsystem einer HYDRA-UMC-Zelle behält der MCU von HYDRA-UMC die Autorität über physische Grenzen und den sicheren Stopp; URTC umgeht diese Grenze nie.",
        "architecture_section_a": "A.R.M.O.R.: Systemarchitektur",
        "architecture_a_card1_title": "Netzwerksegmentierung", "architecture_a_card1_body": "Feldknoten und Kameras befinden sich in einem eigenen VLAN ohne Internetzugang; der MQTT-Broker und der Server laufen in einem Kern-VLAN; Studio und die Android-App erreichen den Server aus einem Client-VLAN.",
        "architecture_a_card2_title": "Feldknoten", "architecture_a_card2_body": "ESP32-S3-Radar-, Solar- und Elektroknoten veröffentlichen Sensor- und Anlagenwerte; die Solar- und Elektroknoten lesen nur, sie schreiben nie auf einen Wechselrichter, eine Batterie oder einen Zähler.",
        "architecture_a_card3_title": "Wahrnehmung, niemals Autorität", "architecture_a_card3_body": "Visuelle und Sprach-KI empfehlen einen Schweregrad oder eine Absicht samt Begründung; authorizes_action bleibt immer falsch, bis der Server selbst authentifiziert und bestätigt.",
        "architecture_a_card4_title": "Zustand und Bedienkonsolen", "architecture_a_card4_body": "ARMOR-SERVER ist die einzige Stelle, die je ein Kamerapasswort oder eine RTSP-Adresse berührt; Studio und die Android-App sind seine authentifizierten Clients, und ein Telefon kann einen neuen Knoten allein über Bluetooth einrichten.",
        "architecture_a_flow_1": "Feldknoten & Kameras", "architecture_a_flow_2": "MQTT-Broker & Server", "architecture_a_flow_3": "KI-Empfehlung", "architecture_a_flow_4": "Authentifizierte Client-Sitzung",
        "architecture_a_rel_title": "Die eigene Grenze von A.R.M.O.R.:", "architecture_a_rel_body": "Der Server ist die einzige Komponente, die eine Aktion autorisiert oder eine Kamera-Zugangsdaten hält. Visuelle und Sprach-KI empfehlen nur; Solar- und Elektroknoten lesen nur - die Regeln zum Schalten einer Stromquelle sind in Software getestet, aber noch mit keiner echten Hardware verbunden.",
    },
    "zh": {
        "architecture_intro": "Electro Hobby 3D 是同一作者打造的三个独立工程生态系统：HYDRA-UMC（工业多机器人平台）、URTC（其通用工具子系统，一个拥有自己固件的独立产品）和 A.R.M.O.R.（周界安防与家庭自动化）。本仪表板实时发现并列出这三者；下方按生态系统标注了各自的家族分组，每个生态系统自身的架构详见其下方的独立小节。",
        "architecture_section": "HYDRA-UMC：系统架构", "architecture_platform_title": "平台基础", "architecture_platform_body": "Raspberry Pi OS ARM64 仍是操作系统基础。HYDRA-UMC 层增加设备配置文件、诊断和服务生命周期。",
        "architecture_contracts_title": "契约与运维", "architecture_contracts_body": "SDK 定义稳定的数据和命令契约；Server、界面和工具使用这些契约，而不是原始硬件协议。",
        "architecture_perception_title": "感知与智能", "architecture_perception_body": "视觉和 AI 是可选能力。其输出在影响任务前必须经过验证，且永远不拥有安全权限。",
        "architecture_engineering_title": "工程与工业", "architecture_engineering_body": "仿真、遥测和标准使物理单元可观测、可测试且可互操作。",
        "architecture_flow_operator": "操作员界面", "architecture_flow_services": "Server 和 SDK", "architecture_flow_adapter": "CM5-MCU 适配器", "architecture_flow_machine": "MCU / URTC / 机器",
        "architecture_relationship_title": "HYDRA-UMC 与 URTC：", "architecture_relationship_body": "HYDRA-UMC 是平台和单元控制器。URTC 是其通用机器人工具子系统，拥有独立的固件和维护工具。MCU 保留物理限制和安全停止的权力；UI、网络和 AI 都不能绕过这一边界。",
        "table_hydra_umc_banner": "HYDRA-UMC —— 工业多机器人平台与单元控制器，本仪表盘的第一个生态系统。", "table_urtc_banner": "URTC - 一个独立产品，拥有自己的固件和维护工具，通过 FDCAN 与 HYDRA-UMC 协调。", "table_armor_banner": "A.R.M.O.R. —— 一个完全独立的公开生态系统，用于周界安防与家庭自动化，同一作者。",
        "section_by_ecosystem": "按生态系统划分的项目",
        "architecture_section_u": "URTC：系统架构",
        "architecture_u_card1_title": "工具头固件", "architecture_u_card1_body": "STM32F303 通过 CAN 总线驱动每个工具头，读取自身的 5 位硬件地址，自动为 25 种内置工具配置文件之一配置功率级、传感器和安全逻辑。",
        "architecture_u_card2_title": "扩展与运动", "architecture_u_card2_body": "20 针扩展接口通过六种可互换变体之一增加第二个步进轴或传感器板，在 TMC2209 和 TMC5160 驱动器之间共享 STEP/DIR/EN 接线。",
        "architecture_u_card3_title": "维护工具", "architecture_u_card3_body": "URTC-FLASHER 无需拆卸主板即可通过 CAN 更新固件，URTC-TESTER 对协议进行端到端测试，URTC-UPDATER 让所有桌面工具与 GitHub 保持同步。",
        "architecture_u_card4_title": "视觉与运行", "architecture_u_card4_body": "URTC-VISION-TOOL 增加基于摄像头的工具检测，URTC-WEB-STUDIO 提供浏览器控制台，URTC-SMART-RACK 在更换之间存放并识别工具头。",
        "architecture_u_flow_1": "工具头", "architecture_u_flow_2": "STM32F303 固件", "architecture_u_flow_3": "CAN 总线", "architecture_u_flow_4": "HYDRA-UMC MCU / 主机",
        "architecture_u_rel_title": "URTC 独立运行，以及与 HYDRA-UMC 配对时：", "architecture_u_rel_body": "URTC 是一个独立的非官方项目——一款为 PAROL6/Faze4 一类机械臂设计的基于 CAN 的工具头控制器，拥有自己的固件、硬件和维护工具。当它作为 HYDRA-UMC 单元的工具子系统时，HYDRA-UMC 自身的 MCU 保留对物理限位和安全停止的权力；URTC 从不绕过这一边界。",
        "architecture_section_a": "A.R.M.O.R.：系统架构",
        "architecture_a_card1_title": "网络分段", "architecture_a_card1_body": "现场节点和摄像头位于没有互联网访问的独立 VLAN 中；MQTT 代理和服务器运行在核心 VLAN 中；Studio 和 Android 应用从客户端 VLAN 访问服务器。",
        "architecture_a_card2_title": "现场节点", "architecture_a_card2_body": "ESP32-S3 雷达、太阳能和电力节点发布传感器和设备读数；太阳能和电力节点仅读取，从不向逆变器、电池或电表写入。",
        "architecture_a_card3_title": "感知，从不拥有权限", "architecture_a_card3_body": "视觉和语音 AI 会给出带理由的严重等级或意图建议；在服务器自身完成认证和确认之前，authorizes_action 始终为 false。",
        "architecture_a_card4_title": "状态与操作控制台", "architecture_a_card4_body": "ARMOR-SERVER 是唯一接触摄像头密码或 RTSP 地址的地方；Studio 和 Android 应用是它的已认证客户端，手机仅通过蓝牙即可设置新节点。",
        "architecture_a_flow_1": "现场节点与摄像头", "architecture_a_flow_2": "MQTT 代理与服务器", "architecture_a_flow_3": "AI 建议", "architecture_a_flow_4": "已认证的客户端会话",
        "architecture_a_rel_title": "A.R.M.O.R. 自身的边界：", "architecture_a_rel_body": "服务器是唯一授权操作或持有摄像头凭证的组件。视觉和语音 AI 只提出建议；太阳能和电力节点只读取——切换电源的规则已在软件中测试，但尚未连接任何真实硬件。",
    },
    "ja": {
        "architecture_intro": "Electro Hobby 3D は、同じ著者による3つの独立したエンジニアリングエコシステムです:HYDRA-UMC(産業用マルチロボットプラットフォーム)、URTC(その汎用ツールサブシステムで、独自のファームウェアを持つ独立した製品)、そして A.R.M.O.R.(周辺セキュリティとホームオートメーション)。このダッシュボードは3つ全てをライブで検出・一覧表示します。各エコシステムのファミリーグループは以下にラベル付けされており、それぞれの詳しいアーキテクチャは以下の各セクションで説明されます。",
        "architecture_section": "HYDRA-UMC:システムアーキテクチャ", "architecture_platform_title": "プラットフォーム基盤", "architecture_platform_body": "Raspberry Pi OS ARM64 は OS の基盤として残ります。HYDRA-UMC 層はデバイスプロファイル、診断、サービスライフサイクルを追加します。",
        "architecture_contracts_title": "契約と運用", "architecture_contracts_body": "SDK は安定したデータおよびコマンド契約を定義し、Server、UI、ツールは生のハードウェアプロトコルの代わりにそれを使用します。",
        "architecture_perception_title": "知覚とインテリジェンス", "architecture_perception_body": "Vision と AI は任意の能力です。出力はミッションに影響する前に検証され、安全権限を持つことはありません。",
        "architecture_engineering_title": "エンジニアリングと産業", "architecture_engineering_body": "シミュレーション、テレメトリ、標準により、物理セルは観測可能、テスト可能、相互運用可能になります。",
        "architecture_flow_operator": "オペレーターインターフェース", "architecture_flow_services": "Server と SDK", "architecture_flow_adapter": "CM5-MCU アダプター", "architecture_flow_machine": "MCU / URTC / 機械",
        "architecture_relationship_title": "HYDRA-UMC と URTC：", "architecture_relationship_body": "HYDRA-UMC はプラットフォームおよびセルコントローラーです。URTC は独立したファームウェアと保守ツールを持つ汎用ロボットツールサブシステムです。MCU は物理的な制限と安全停止の権限を維持し、UI、ネットワーク、AI はその境界を迂回できません。",
        "table_hydra_umc_banner": "HYDRA-UMC — 産業用マルチロボットプラットフォーム兼セル制御装置。本ダッシュボードの最初のエコシステムです。", "table_urtc_banner": "URTC - 独自のファームウェアと保守ツールを持つ独立した製品で、FDCAN 経由で HYDRA-UMC と協調します。", "table_armor_banner": "A.R.M.O.R. — 同じ作者による、別個の公開の周辺セキュリティ・ホームオートメーションエコシステムです。",
        "section_by_ecosystem": "エコシステム別プロジェクト",
        "architecture_section_u": "URTC：システムアーキテクチャ",
        "architecture_u_card1_title": "ツールヘッドファームウェア", "architecture_u_card1_body": "STM32F303 が CAN 経由で各ツールヘッドを制御し、自身の 5 ビットのハードウェアアドレスを読み取って、25 種類の内蔵ツールプロファイルの一つに合わせて電源段、センサー、安全ロジックを自動設定します。",
        "architecture_u_card2_title": "拡張と駆動", "architecture_u_card2_body": "20 ピンの拡張コネクタは、6 種類の交換可能なバリエーションのいずれかを通じて、第 2 のステッピング軸またはセンサーボードを追加し、TMC2209 と TMC5160 ドライバ間で STEP/DIR/EN 配線を共有します。",
        "architecture_u_card3_title": "メンテナンスツール", "architecture_u_card3_body": "URTC-FLASHER は基板を取り外さずに CAN 経由でファームウェアを更新し、URTC-TESTER はプロトコルをエンドツーエンドで検証し、URTC-UPDATER はすべてのデスクトップツールを GitHub から最新に保ちます。",
        "architecture_u_card4_title": "ビジョンと運用", "architecture_u_card4_body": "URTC-VISION-TOOL はカメラによるツール検査を追加し、URTC-WEB-STUDIO はブラウザコンソールを提供し、URTC-SMART-RACK は交換の間にツールヘッドを保管・識別します。",
        "architecture_u_flow_1": "ツールヘッド", "architecture_u_flow_2": "STM32F303 ファームウェア", "architecture_u_flow_3": "CAN バス", "architecture_u_flow_4": "HYDRA-UMC MCU / ホスト",
        "architecture_u_rel_title": "単体の URTC、そして HYDRA-UMC と組み合わせた場合：", "architecture_u_rel_body": "URTC は独立した非公式プロジェクトです — PAROL6/Faze4 系のアームに対応する CAN ベースのツールヘッドコントローラーで、独自のファームウェア、ハードウェア、メンテナンスツールを持ちます。HYDRA-UMC セルのツールサブシステムとして動作する場合、物理的な限界と安全停止の権限は HYDRA-UMC 自身の MCU が持ち続け、URTC がその境界を越えることはありません。",
        "architecture_section_a": "A.R.M.O.R.：システムアーキテクチャ",
        "architecture_a_card1_title": "ネットワークセグメンテーション", "architecture_a_card1_body": "フィールドノードとカメラはインターネットに接続されない専用 VLAN 上にあり、MQTT ブローカーとサーバーはコア VLAN 上で、Studio と Android アプリはクライアント VLAN からサーバーにアクセスします。",
        "architecture_a_card2_title": "フィールドノード", "architecture_a_card2_body": "ESP32-S3 のレーダー、ソーラー、電気ノードがセンサーと機器の値を送信します。ソーラーと電気ノードは読み取り専用で、インバーター、バッテリー、メーターに書き込むことはありません。",
        "architecture_a_card3_title": "認識するが権限は持たない", "architecture_a_card3_body": "映像・音声 AI は理由付きで重大度や意図を提案するだけで、サーバー自身が認証・確認するまで authorizes_action は常に false です。",
        "architecture_a_card4_title": "状態とオペレーターコンソール", "architecture_a_card4_body": "ARMOR-SERVER だけがカメラのパスワードや RTSP アドレスに触れます。Studio と Android アプリはその認証済みクライアントであり、新しいノードはスマートフォンから Bluetooth だけで設定できます。",
        "architecture_a_flow_1": "フィールドノードとカメラ", "architecture_a_flow_2": "MQTT ブローカーとサーバー", "architecture_a_flow_3": "AI の提案", "architecture_a_flow_4": "認証済みクライアントセッション",
        "architecture_a_rel_title": "A.R.M.O.R. 自身の境界：", "architecture_a_rel_body": "アクションを許可したり、カメラの認証情報を保持したりするのはサーバーだけです。映像・音声 AI は提案するだけであり、ソーラーと電気ノードは読み取るだけです — 電源切り替えのルールはソフトウェアではテスト済みですが、実際のハードウェアにはまだ接続されていません。",
    },
}

for language, values in ARCHITECTURE_TRANSLATIONS.items():
    TRANSLATIONS[language].update(values)


# ---------------------------------------------------------------------------
# Roadmap and compatibility matrix translations. Reuses the existing
# maturity_*/maturity_desc_* keys verbatim for each rung's own name and
# description - only the "what moves it to the next rung" sentences and the
# two section headers are new. Deliberately not a feature timeline with
# dates (see feedback_no_dates_public_docs): the real, already-practiced
# graduation path from one maturity tier to the next, same criteria this
# ecosystem's own review process already applies.
# ---------------------------------------------------------------------------

ROADMAP_COMPAT_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "roadmap_section": "Roadmap",
        "roadmap_intro": "Not a feature timeline with dates - the real path every project in this ecosystem follows, and exactly where each one sits on it right now (see the Maturity section above for the live counts).",
        "roadmap_advance_scaffolding": "Advances once real, tested business logic exists behind it: its own test suite, a real end-to-end smoke test, or a real protocol round-trip - never a mock standing in forever.",
        "roadmap_advance_functional": "Advances once a real consumer outside its own checkout - another real service, or a package actually installed rather than left editable - depends on it and proves that in a repeatable test, not just its own CLI or fixtures.",
        "roadmap_advance_established": "Advances only once real, physical hardware exists for it to run against - the exact board or machine this ecosystem's own hardware documentation describes.",
        "roadmap_advance_production": "The top of the ladder. Nothing advances past here - it just keeps shipping real fixes.",
        "compat_section": "Compatibility matrix",
        "compat_intro": "Real project counts by role and deployment target, spanning all three ecosystems (HYDRA-UMC, URTC and A.R.M.O.R.) and drawn straight from every repository's own manifest - A.R.M.O.R.'s own free-text role/deployment_target fields are classified into these same categories rather than a second, separate table. A count, not a claim that any two specific projects interoperate.",
        "compat_corner": "Role \\ Target",
    },
    "es": {
        "roadmap_section": "Hoja de ruta",
        "roadmap_intro": "No es un calendario de funciones con fechas - es el camino real que sigue cada proyecto de este ecosistema, y en qué punto exacto está cada uno ahora mismo (ver la sección Madurez de arriba para los recuentos en vivo).",
        "roadmap_advance_scaffolding": "Avanza en cuanto existe lógica de negocio real y probada detrás: su propia batería de pruebas, una prueba de humo real de extremo a extremo, o un ida-y-vuelta real de protocolo - nunca un simulacro que se queda para siempre.",
        "roadmap_advance_functional": "Avanza en cuanto un consumidor real fuera de su propio checkout - otro servicio real, o un paquete realmente instalado en vez de dejado editable - depende de él y lo demuestra en una prueba repetible, no solo su propio CLI o sus fixtures.",
        "roadmap_advance_established": "Avanza solo cuando existe hardware físico real contra el que funcionar - la placa o máquina exacta que la propia documentación de hardware de este ecosistema describe.",
        "roadmap_advance_production": "La cima de la escalera. Nada avanza más allá de aquí - solo sigue entregando arreglos reales.",
        "compat_section": "Matriz de compatibilidad",
        "compat_intro": "Recuentos reales de proyectos por rol y destino de despliegue, abarcando los tres ecosistemas (HYDRA-UMC, URTC y A.R.M.O.R.) y extraídos directamente del manifiesto propio de cada repositorio - los campos de rol/destino de despliegue en texto libre propios de A.R.M.O.R. se clasifican en estas mismas categorías en vez de usar una segunda tabla aparte. Un recuento, no una afirmación de que dos proyectos concretos interoperen.",
        "compat_corner": "Rol \\ Destino",
    },
    "fr": {
        "roadmap_section": "Feuille de route",
        "roadmap_intro": "Ce n'est pas un calendrier de fonctionnalités avec des dates - c'est le vrai chemin que suit chaque projet de cet écosystème, et l'endroit exact où se trouve chacun en ce moment (voir la section Maturité ci-dessus pour les comptages en direct).",
        "roadmap_advance_scaffolding": "Avance dès qu'une logique métier réelle et testée existe derrière lui : sa propre suite de tests, un vrai test de fumée de bout en bout, ou un véritable aller-retour de protocole - jamais un simulacre qui reste en place pour toujours.",
        "roadmap_advance_functional": "Avance dès qu'un véritable consommateur en dehors de son propre checkout - un autre service réel, ou un paquet réellement installé plutôt que laissé éditable - en dépend et le prouve dans un test reproductible, pas seulement sa propre CLI ou ses fixtures.",
        "roadmap_advance_established": "N'avance que lorsqu'un matériel physique réel existe pour qu'il puisse fonctionner face à lui - la carte ou la machine exacte que la documentation matérielle de cet écosystème décrit elle-même.",
        "roadmap_advance_production": "Le sommet de l'échelle. Rien n'avance au-delà d'ici - il continue simplement à livrer de vrais correctifs.",
        "compat_section": "Matrice de compatibilité",
        "compat_intro": "Comptages réels de projets par rôle et cible de déploiement, couvrant les trois écosystèmes (HYDRA-UMC, URTC et A.R.M.O.R.) et tirés directement du manifeste propre de chaque dépôt - les champs rôle/cible de déploiement en texte libre propres à A.R.M.O.R. sont classés dans ces mêmes catégories plutôt que dans un second tableau séparé. Un comptage, pas une affirmation que deux projets précis interopèrent.",
        "compat_corner": "Rôle \\ Cible",
    },
    "it": {
        "roadmap_section": "Tabella di marcia",
        "roadmap_intro": "Non è un calendario di funzionalità con date - è il percorso reale che segue ogni progetto di questo ecosistema, ed esattamente il punto in cui si trova ciascuno in questo momento (vedi la sezione Maturità sopra per i conteggi in tempo reale).",
        "roadmap_advance_scaffolding": "Avanza non appena esiste una logica di business reale e testata dietro di esso: la propria suite di test, un vero smoke test end-to-end, o un vero andata-e-ritorno di protocollo - mai un simulacro che resta per sempre.",
        "roadmap_advance_functional": "Avanza non appena un vero consumatore al di fuori del proprio checkout - un altro servizio reale, o un pacchetto realmente installato anziché lasciato editabile - dipende da esso e lo dimostra in un test ripetibile, non solo la propria CLI o le proprie fixture.",
        "roadmap_advance_established": "Avanza solo quando esiste hardware fisico reale contro cui funzionare - la scheda o la macchina esatta che la documentazione hardware di questo ecosistema descrive.",
        "roadmap_advance_production": "La cima della scala. Nulla avanza oltre questo punto - continua solo a distribuire correzioni reali.",
        "compat_section": "Matrice di compatibilità",
        "compat_intro": "Conteggi reali di progetti per ruolo e destinazione di distribuzione, che coprono tutti e tre gli ecosistemi (HYDRA-UMC, URTC e A.R.M.O.R.) e presi direttamente dal manifesto proprio di ogni repository - i campi ruolo/destinazione in testo libero propri di A.R.M.O.R. sono classificati in queste stesse categorie invece di usare una seconda tabella separata. Un conteggio, non un'affermazione che due progetti specifici interoperino.",
        "compat_corner": "Ruolo \\ Destinazione",
    },
    "de": {
        "roadmap_section": "Fahrplan",
        "roadmap_intro": "Kein Feature-Zeitplan mit Daten - der echte Weg, den jedes Projekt in diesem Ökosystem geht, und genau der Punkt, an dem jedes gerade steht (siehe den Abschnitt Reifegrad oben für die Live-Zahlen).",
        "roadmap_advance_scaffolding": "Steigt auf, sobald echte, getestete Geschäftslogik dahintersteckt: eine eigene Testsuite, ein echter End-to-End-Smoke-Test oder ein echter Protokoll-Hin-und-Rückweg - niemals ein Mock, der für immer bleibt.",
        "roadmap_advance_functional": "Steigt auf, sobald ein echter Verbraucher außerhalb des eigenen Checkouts - ein anderer echter Dienst, oder ein tatsächlich installiertes statt editierbar belassenes Paket - davon abhängt und das in einem wiederholbaren Test beweist, nicht nur in der eigenen CLI oder den eigenen Fixtures.",
        "roadmap_advance_established": "Steigt nur auf, sobald echte physische Hardware existiert, gegen die es laufen kann - genau die Platine oder Maschine, die die eigene Hardware-Dokumentation dieses Ökosystems beschreibt.",
        "roadmap_advance_production": "Die Spitze der Leiter. Nichts steigt hier weiter auf - es liefert einfach weiter echte Fixes.",
        "compat_section": "Kompatibilitätsmatrix",
        "compat_intro": "Echte Projektzahlen nach Rolle und Deployment-Ziel, über alle drei Ökosysteme hinweg (HYDRA-UMC, URTC und A.R.M.O.R.), direkt aus dem eigenen Manifest jedes Repositories entnommen - A.R.M.O.R.s eigene Freitext-Felder für Rolle/Deployment-Ziel werden in dieselben Kategorien eingeordnet statt in eine zweite, separate Tabelle. Eine Zählung, keine Behauptung, dass zwei bestimmte Projekte zusammenarbeiten.",
        "compat_corner": "Rolle \\ Ziel",
    },
    "zh": {
        "roadmap_section": "路线图",
        "roadmap_intro": "这不是带日期的功能时间表——而是本生态系统中每个项目真实走过的路径，以及此刻每个项目实际所处的位置(实时数量见上方“成熟度”一节)。",
        "roadmap_advance_scaffolding": "一旦其背后有了真实、经过测试的业务逻辑——自己的测试套件、真实的端到端冒烟测试，或真实的协议往返——就会晋级，绝不是永远留在原地的模拟。",
        "roadmap_advance_functional": "一旦有一个真实的、在其自身检出目录之外的消费者——另一个真实的服务，或一个真正被安装而非保持可编辑状态的包——依赖它，并在可重复的测试中证明这一点，而不仅仅是它自己的 CLI 或 fixture，就会晋级。",
        "roadmap_advance_established": "只有当真实的物理硬件存在、可供其运行时才会晋级——正是本生态系统自身硬件文档所描述的那块板卡或那台机器。",
        "roadmap_advance_production": "阶梯的顶端。到这里就不再晋级——只会持续交付真实的修复。",
        "compat_section": "兼容性矩阵",
        "compat_intro": "按角色和部署目标统计的真实项目数量，涵盖全部三个生态系统（HYDRA-UMC、URTC 和 A.R.M.O.R.），直接取自每个仓库自身的清单文件——A.R.M.O.R. 自身以自由文本形式填写的角色/部署目标字段被归入这同一套分类，而不是另立一张单独的表格。这是一个计数，而不是声称某两个具体项目能够互操作。",
        "compat_corner": "角色 \\ 目标",
    },
    "ja": {
        "roadmap_section": "ロードマップ",
        "roadmap_intro": "日付付きの機能予定表ではありません——このエコシステムのすべてのプロジェクトが実際にたどる道であり、今この瞬間、各プロジェクトが正確にどこに位置しているかです(リアルタイムの件数は上の「成熟度」セクションを参照してください)。",
        "roadmap_advance_scaffolding": "その裏に本物のテスト済みビジネスロジックができた時点で昇格します:自身のテストスイート、本物のエンドツーエンドのスモークテスト、または本物のプロトコルの往復——永遠にそこに居座るモックでは決してありません。",
        "roadmap_advance_functional": "自身のチェックアウトの外にある本物の利用者——別の本物のサービス、または編集可能なままではなく実際にインストールされたパッケージ——がそれに依存し、それを再現可能なテストで証明した時点で昇格します。自身の CLI やフィクスチャだけではありません。",
        "roadmap_advance_established": "本物の物理ハードウェアが存在し、それに対して実際に動作できるようになった時点でのみ昇格します——このエコシステム自身のハードウェアドキュメントが説明する、まさにそのボードやマシンです。",
        "roadmap_advance_production": "はしごの頂点です。ここから先に昇格することはありません——ただ本物の修正を届け続けるだけです。",
        "compat_section": "互換性マトリクス",
        "compat_intro": "役割とデプロイ対象ごとの本物のプロジェクト件数で、3つのエコシステム（HYDRA-UMC、URTC、A.R.M.O.R.）すべてにまたがり、各リポジトリ自身のマニフェストから直接取得しています。A.R.M.O.R. 自身の自由記述の役割/デプロイ対象フィールドは、別の表を作るのではなく同じ分類に振り分けられます。件数であり、特定の2つのプロジェクトが相互運用できるという主張ではありません。",
        "compat_corner": "役割 \\ 対象",
    },
}

for language, values in ROADMAP_COMPAT_TRANSLATIONS.items():
    TRANSLATIONS[language].update(values)

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
    "dev-server": (
        '<rect x="3" y="4" width="18" height="16" rx="2"/>'
        '<path d="M7 9l3 3-3 3M13 15h4"/>'
    ),
    "field-node": (
        '<circle cx="12" cy="12" r="2.5"/>'
        '<path d="M7 7a7 7 0 0 1 10 0M4.5 4.5a10.5 10.5 0 0 1 15 0'
        'M7 17a7 7 0 0 0 10 0M4.5 19.5a10.5 10.5 0 0 0 15 0"/>'
    ),
    "server": (
        '<rect x="4" y="3" width="16" height="7" rx="1.5"/>'
        '<rect x="4" y="14" width="16" height="7" rx="1.5"/>'
        '<path d="M8 6.5h.01M8 17.5h.01"/>'
    ),
    "browser": (
        '<rect x="3" y="4" width="18" height="16" rx="2"/>'
        '<path d="M3 8h18M6 6h.01M9 6h.01"/>'
    ),
    "shared": (
        '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/>'
        '<path d="M8 7.2 10.5 16M16 7.2 13.5 16"/>'
    ),
}


# ---------------------------------------------------------------------------
# Free-text role/deploy categorisation (A.R.M.O.R. only - HYDRA-UMC and
# URTC manifests already declare one of ROLE_ORDER/DEPLOY_ORDER's own
# closed enum values directly, so the functions below pass those straight
# through unchanged and never touch them).
# ---------------------------------------------------------------------------
#
# A.R.M.O.R.'s manifest schema deliberately keeps `role`/`deployment_target`
# as real, free-text descriptions instead (see ARMOR-UPDATER's own
# armor.project.json notes) - a raw dict-key lookup on either field, as the
# Deployment targets cards, the Role cards and the Compatibility matrix
# below all did before this, left every one of A.R.M.O.R.'s real projects
# invisible in all three sections at once (each one only ever counts an
# entry whose raw value already equals a known enum key), not just the one
# project a user went looking for under one specific filter and didn't
# find.

try:
    from armor_updater.deploy_category import categorize_deployment_target as _armor_categorize_deploy
except ImportError:  # pragma: no cover - armor-updater is a real, pinned CI dependency
    _armor_categorize_deploy = None


def categorize_deploy_for_stats(raw_deploy: str) -> str:
    """A known enum value passes straight through; anything else is
    A.R.M.O.R.'s own free text, classified by ARMOR-UPDATER's own real
    deploy_category rules (the same ones its desktop GUI filter uses, not
    a second, divergent copy) and folded into this dashboard's own set -
    "workstation" becomes "user-pc" here, the same real thing (a
    developer's own machine) under HYDRA-UMC/URTC's own existing name."""
    if raw_deploy in DEPLOY_LABELS:
        return raw_deploy
    if _armor_categorize_deploy is None:
        return raw_deploy
    category = _armor_categorize_deploy(raw_deploy)
    return "user-pc" if category == "workstation" else category


#: Ordered (keyword, category) rules for A.R.M.O.R.'s own free-text `role`,
#: checked top to bottom against the lower-cased text - the first match
#: wins. Order matters: e.g. ARMOR-SOLAR's role contains "node:", "gateway"
#: AND "library" all at once, and "node:" (a real field/gateway-node
#: firmware project, matching ARMOR-RADAR/-ELECTRICAL) is the meaningful
#: category here, not the incidental mention of "its own protocol library"
#: later in the same sentence.
_ARMOR_ROLE_KEYWORD_RULES: tuple[tuple[str, str], ...] = (
    ("android", "ui"),
    ("browser", "ui"),
    ("console", "ui"),
    ("client", "ui"),
    ("web api", "api"),
    ("event coordinator", "api"),
    ("firmware", "firmware"),
    ("node:", "firmware"),
    ("library", "library"),
    ("documentation", "docs"),
    ("architecture", "docs"),
    ("enclosure design", "hardware"),
    ("hardware", "hardware"),
    ("simulator", "tool"),
    ("deployment and operations", "tool"),
    ("installs and updates", "tool"),
    ("monitor", "service"),
    ("gateway", "service"),
    ("service", "service"),
)


def categorize_role_for_stats(raw_role: str) -> str:
    """A known enum value passes straight through; anything else is
    A.R.M.O.R.'s own free-text role, classified by real keyword content -
    the same spirit as armor_updater.deploy_category, kept here rather
    than in that module since no A.R.M.O.R. tool needs a role FILTER the
    way its own deploy filter needed a category - only this dashboard
    does. Falls back to "tool" (never silently uncounted) for a future
    role this ecosystem hasn't seen yet."""
    if raw_role in ROLE_LABELS:
        return raw_role
    text = raw_role.strip().lower()
    for needle, category in _ARMOR_ROLE_KEYWORD_RULES:
        if needle in text:
            return category
    return "tool"


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
# Project ordering - grouped by family, with every relationship read from
# repository manifests discovered on GitHub. Families with no single shared
# parent render in deterministic repository-name order.
# ---------------------------------------------------------------------------

def ordered_projects(
    entries: list[ProjectEntry],
) -> list[tuple[str, ProjectEntry | None, list[ProjectEntry]]]:
    """Returns [(family_name, parent_or_None, [children_in_family_order]), ...]
    in family/name order derived from the manifest-resolved project list.
    Ecosystem-agnostic on purpose - this only feeds the family filter
    <select>, a flat list where plain alphabetical order is the expected,
    conventional behavior of any dropdown, unlike the big project table
    (see `ordered_projects_by_ecosystem` below, used there instead)."""

    families: dict[str, list[ProjectEntry]] = {}
    for entry in entries:
        families.setdefault(entry.family, []).append(entry)

    order: list[tuple[str, ProjectEntry | None, list[ProjectEntry]]] = []
    for family in sorted(families, key=str.casefold):
        members = sorted(families[family], key=lambda entry: entry.name.casefold())
        roots = [entry for entry in members if entry.parent is None]
        parent = roots[0] if len(roots) == 1 else None
        children = [entry for entry in members if parent is None or entry.name != parent.name]
        order.append((family, parent, children))

    return order


def ordered_projects_by_ecosystem(
    entries: list[ProjectEntry],
    ecosystem_by_name: dict[str, str],
) -> list[tuple[str, str, list[tuple[str, ProjectEntry | None, list[ProjectEntry]]]]]:
    """Returns [(ecosystem_key, ecosystem_label, [(family, parent, children), ...]), ...]
    in `ECOSYSTEM_ORDER` order, each ecosystem's own families in family/name
    order - the big project table's own real grouping.

    Grouping by ecosystem FIRST (not just family, as `ordered_projects`
    does for the filter dropdown) matters for real here: several family
    names are shared across ecosystems by simple convention rather than by
    meaning - "Ecosystem Operations" alone now holds HYDRA-UMC-UPDATER,
    URTC-UPDATER AND ARMOR-UPDATER, three unrelated tools that happen to
    use the same family label - and merging them into one alphabetically-
    sorted list of ~20 unlabeled family headers from three different
    ecosystems at once is genuinely disordered to read, not just a
    cosmetic nit: nothing on the page told a reader whether "Clients" (an
    A.R.M.O.R. family) or "Core Backend & Clients" (a HYDRA-UMC one) was
    which ecosystem's, or that "Ecosystem Operations" was about to contain
    three unrelated tools back to back. Splitting the same family-name
    bucket per ecosystem instead means a repeated family name shows up
    once per ecosystem that actually uses it, each time under a clearly
    labeled ecosystem section, and never mixes projects that only share a
    label by coincidence.
    """
    entries_by_ecosystem: dict[str, list[ProjectEntry]] = {key: [] for key, _ in ECOSYSTEM_ORDER}
    for entry in entries:
        key = ecosystem_by_name.get(entry.name)
        if key in entries_by_ecosystem:
            entries_by_ecosystem[key].append(entry)

    return [
        (key, label, ordered_projects(entries_by_ecosystem[key]))
        for key, label in ECOSYSTEM_ORDER
    ]


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
    # The card buttons filter by CATEGORY (categorize_deploy_for_stats/
    # categorize_role_for_stats - see their own docstrings), not by this
    # row's own raw manifest text, so this attribute (never shown, only
    # matched against a clicked card's own data-filter-deploy) must be the
    # same category or clicking "Field Node"/"AI Server"/etc would never
    # match a single real A.R.M.O.R. row. The VISIBLE badge below (`deploy`/
    # `deploy_label`) is unaffected and still shows this project's own real
    # text.
    deploy_filter = esc(categorize_deploy_for_stats(deploy_key))
    role_filter = esc(categorize_role_for_stats(entry.role))

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

    # A.R.M.O.R.'s own `role`/`deployment_target` fields are real,
    # free-text one-line descriptions (up to ~140 characters), not the
    # short curated single/two-word enum HYDRA-UMC/URTC use for these same
    # two columns (`ROLE_LABELS`/`DEPLOY_LABELS`) - found for real the
    # first time this table actually rendered A.R.M.O.R. rows: the raw
    # value was used as a literal CSS class name (`role-{entry.role}`),
    # which a value containing spaces silently turns into several bogus,
    # unstyled class tokens instead of one, and both badges' own
    # `white-space: nowrap` (deliberately never wrapping a short label)
    # rendered a full sentence as one very long unbroken line - ballooning
    # the whole table's width far enough that Version/Status/Last commit,
    # near the row's right edge, needed a lot of hidden horizontal
    # scrolling to ever see. Fixed on both sides: a real, CSS-safe class
    # token here (falls back to a plain "other" modifier for anything
    # outside the curated enum), and `.role-badge`/`.deploy-badge` in the
    # stylesheet below now truncate with an ellipsis - never grow the
    # table - and carry the untruncated text in a real `title` tooltip.
    role_known = entry.role in ROLE_LABELS
    role_css_key = entry.role if role_known else "other"
    role_i18n_attr = f' data-i18n="role_{esc(entry.role)}"' if role_known else ""

    deploy_known = deploy_key in DEPLOY_LABELS
    deploy_i18n_attr = f' data-i18n="deploy_{deploy_filter}"' if deploy_known else ""

    maturity_class = MATURITY_CLASSES.get(entry.maturity, "maturity-scaffolding")
    maturity_label = esc(MATURITY_LABELS.get(entry.maturity, entry.maturity))

    child_class = " child-row" if is_child else ""
    child_marker = '<span class="child-marker" aria-hidden="true">↳</span>' if is_child else ""

    tech_chips = "".join(
        f'<span class="tech-chip">{esc(t)}</span>' for t in entry.tech
    ) or '<span class="cell-muted">—</span>'

    notes_html = (
        esc(entry.notes)
        if entry.notes
        else '<span data-i18n="notes_empty">No notes recorded for this project yet.</span>'
    )
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
            data-role="{role_filter}"
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
                  data-i18n="link_actions"
                >Actions</a>

                <a
                  href="{project_issues}"
                  target="_blank"
                  rel="noopener noreferrer"
                  data-i18n="link_issues"
                >Issues</a>
              </div>
            </div>
          </td>

          <td class="role-cell">
            <span class="role-badge role-{esc(role_css_key)}" title="{esc(entry.role)}">
              {role_icon}<span{role_i18n_attr}>{role_label}</span>
            </span>
          </td>

          <td class="maturity-cell">
            <span class="maturity-badge {maturity_class}" data-i18n="maturity_{esc(entry.maturity)}">
              {maturity_label}
            </span>
          </td>

          <td class="stack">
            {stack_icon}{stack}
          </td>

          <td class="deploy">
            <span class="deploy-badge" title="{deploy}">
              {deploy_icon}<span{deploy_i18n_attr}>{deploy}</span>
            </span>
          </td>

          <td class="version {status_class}">
            {version_html}
          </td>

          <td class="status-cell">
            <span class="status-badge {status_class}">
              <span class="status-dot"></span>
              <span data-i18n="version_status_{esc(status_key)}">{esc(status_label)}</span>
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
            data-role="{role_filter}"
            data-family="{esc(entry.family.lower())}"
            hidden
        >
          <td colspan="8">
            <div class="detail-panel">
              <div class="detail-block">
                <div class="detail-label" data-i18n="detail_notes">Notes</div>
                <div class="detail-text">{notes_html}</div>
              </div>

              <div class="detail-block">
                <div class="detail-label" data-i18n="detail_technology">Technology</div>
                <div class="tech-chips">{tech_chips}</div>
              </div>

              <div class="detail-block">
                <div class="detail-label" data-i18n="detail_build">Build</div>
                <div class="detail-text">{build_note_html}</div>
              </div>
            </div>
          </td>
        </tr>
        """

    return row


ECOSYSTEM_BANNER_I18N_KEY: dict[str, str] = {
    "hydra-umc": "table_hydra_umc_banner",
    "urtc": "table_urtc_banner",
    "armor": "table_armor_banner",
}

ECOSYSTEM_BANNER_FALLBACK_TEXT: dict[str, str] = {
    "hydra-umc": "HYDRA-UMC - the industrial multi-robot platform and cell controller, this dashboard's first ecosystem.",
    "urtc": "URTC - an independent product with its own firmware and maintenance tools, coordinated with HYDRA-UMC over FDCAN.",
    "armor": "A.R.M.O.R. - a separate, public perimeter-security and home-automation ecosystem, same author.",
}


def render_project_rows(
    entries: list[ProjectEntry],
    results: dict[str, RemoteStatus],
    meta: dict[str, RepoMeta],
    ecosystem_by_name: dict[str, str],
) -> str:
    rows: list[str] = []

    # Grouped by ecosystem first, each one's own families second (see
    # `ordered_projects_by_ecosystem`'s own docstring for why this is not
    # just cosmetic) - a real, visible banner marks the start of every
    # ecosystem's own block, not just URTC's the way this used to work
    # when the table only ever mixed two ecosystems together.
    for ecosystem_key, ecosystem_label, families in ordered_projects_by_ecosystem(entries, ecosystem_by_name):
        if not families:
            continue

        banner_key = ECOSYSTEM_BANNER_I18N_KEY[ecosystem_key]
        banner_text = esc(ECOSYSTEM_BANNER_FALLBACK_TEXT[ecosystem_key])
        rows.append(
            f'\n            <tr class="ecosystem-banner-row" data-ecosystem-banner="{esc(ecosystem_key)}">'
            f'\n              <td colspan="8">'
            f'\n                <span data-i18n="{banner_key}">{banner_text}</span>'
            f'\n              </td>'
            f'\n            </tr>\n            '
        )

        for family_name, parent, children in families:
            # Same raw lower() value the project rows themselves stamp into
            # their own data-family attribute (and the family <select>'s own
            # option values use) - a data-* attribute value, not a CSS
            # id/class, so it doesn't need slug-sanitizing, and NOT
            # sanitizing it is what keeps the two sides matching in the JS
            # filter below.
            family_id = esc(family_name.lower())
            member_count = len(children) + (1 if parent else 0)

            parent_repo_link = ""
            if parent is not None:
                parent_repo_link = (
                    f' · <a href="{esc(repo_url(parent.name))}" target="_blank" '
                    f'rel="noopener noreferrer">{esc(parent.name)}</a> '
                    f'<span data-i18n="family_parent_suffix">is this family\'s own integration parent</span>'
                )

            rows.append(
                f"""
            <tr class="family-header-row" data-family-header="{family_id}" data-ecosystem="{esc(ecosystem_key)}">
              <td colspan="8">
                <span class="family-header-label">{esc(family_name)}</span>
                <span class="family-header-count">
                    <span data-i18n-template="family_count" data-count="{member_count}">{member_count} project(s)</span>{parent_repo_link}
                </span>
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
    entries: list[ProjectEntry],
    results: dict[str, RemoteStatus],
) -> dict[str, object]:
    total = len(entries)

    ok = sum(
        1
        for entry in entries
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

    # Role x deployment-target cross-tab for the compatibility matrix -
    # real counts only, built the same way as the 4 single-axis counts
    # above. Never a claim that two specific projects interoperate, only
    # how many real projects of a given role target a given host.
    role_deploy_matrix: dict[str, dict[str, int]] = {
        role: {deploy: 0 for deploy in DEPLOY_ORDER}
        for role in ROLE_ORDER
    }

    for entry in entries:
        # Categorized, not the raw manifest value - see
        # categorize_deploy_for_stats/categorize_role_for_stats's own
        # docstrings for why a raw dict-key lookup here left every real
        # A.R.M.O.R. project invisible in every count below.
        deploy_category = categorize_deploy_for_stats(entry.deploy)
        role_category = categorize_role_for_stats(entry.role)

        deploy_counts[deploy_category] = (
            deploy_counts.get(deploy_category, 0) + 1
        )

        stack_counts[entry.stack] = (
            stack_counts.get(entry.stack, 0) + 1
        )

        maturity_counts[entry.maturity] = (
            maturity_counts.get(entry.maturity, 0) + 1
        )

        role_counts[role_category] = (
            role_counts.get(role_category, 0) + 1
        )

        if role_category in role_deploy_matrix and deploy_category in role_deploy_matrix[role_category]:
            role_deploy_matrix[role_category][deploy_category] += 1

    return {
        "total": total,
        "ok": ok,
        "errors": errors,
        "success_percent": success_percent,
        "deploy_counts": deploy_counts,
        "stack_counts": stack_counts,
        "maturity_counts": maturity_counts,
        "role_counts": role_counts,
        "role_deploy_matrix": role_deploy_matrix,
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
                {icon}<span data-i18n="deploy_{esc(key)}">{esc(label)}</span>
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
                data-i18n-title="maturity_desc_{esc(key)}"
            >
              <span class="maturity-count">{count}</span>
              <span class="maturity-card-label" data-i18n="maturity_{esc(key)}">{esc(label)}</span>
              <span class="maturity-card-desc" data-i18n="maturity_desc_{esc(key)}">{esc(description)}</span>
            </button>
            """
        )

    return "".join(cards)


# ---------------------------------------------------------------------------
# Per-ecosystem counters - HYDRA-UMC, URTC and A.R.M.O.R. are three real,
# independent ecosystems by the same author, each with its own dedicated
# discovery client (see this file's own import comment). This renders the
# grand total (all three combined, already shown by the health section
# above) broken down per ecosystem, reusing the same `.health-card` styling
# rather than introducing a fourth card class for what is visually the same
# kind of number. Deliberately not a filter control (unlike the maturity/
# deploy cards above): the project table's existing family/deploy/maturity
# filters already cut across all three ecosystems at once, and each
# ecosystem is already visually obvious from a project's own name prefix
# (HYDRA-UMC-*, URTC(-*) or ARMOR-*).
# ---------------------------------------------------------------------------

ECOSYSTEM_ORDER: tuple[tuple[str, str], ...] = (
    ("hydra-umc", "HYDRA-UMC"),
    ("urtc", "URTC"),
    ("armor", "A.R.M.O.R."),
)


def render_ecosystem_cards(
    entries: list[ProjectEntry],
    ecosystem_by_name: dict[str, str],
) -> str:
    counts = {key: 0 for key, _ in ECOSYSTEM_ORDER}
    for entry in entries:
        key = ecosystem_by_name.get(entry.name)
        if key in counts:
            counts[key] += 1

    cards: list[str] = []
    for key, label in ECOSYSTEM_ORDER:
        cards.append(
            f"""
            <div class="health-card">
              <div class="number">{counts[key]}</div>
              <div class="label">{esc(label)}</div>
            </div>
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
          <span data-i18n="role_{esc(key)}">{esc(ROLE_LABELS.get(key, key))}</span>
          <strong>{count}</strong>
        </button>
        """
        for key, count in items
    )


# ---------------------------------------------------------------------------
# Compatibility matrix (role x deployment target)
# ---------------------------------------------------------------------------
#
# A real cross-tab of the same two axes already computed above (role_counts,
# deploy_counts), not a new data source - see role_deploy_matrix in
# calculate_statistics(). Rows are roles that have at least one real
# project; a role with zero real projects on a given target simply shows
# an em dash rather than a fabricated zero-with-meaning.
# ---------------------------------------------------------------------------

def render_compatibility_matrix(
    role_deploy_matrix: dict[str, dict[str, int]],
    role_counts: dict[str, int],
) -> str:
    rows = [
        role
        for role in ROLE_ORDER
        if role_counts.get(role, 0) > 0
    ]

    header_cells = "".join(
        f'<th data-i18n="deploy_{esc(deploy)}">{esc(DEPLOY_LABELS.get(deploy, deploy))}</th>'
        for deploy in DEPLOY_ORDER
    )

    body_rows = []
    for role in rows:
        cells = []
        for deploy in DEPLOY_ORDER:
            count = role_deploy_matrix.get(role, {}).get(deploy, 0)
            cell_text = str(count) if count else "–"
            css_class = "compat-cell compat-cell-hit" if count else "compat-cell compat-cell-empty"
            cells.append(f'<td class="{css_class}">{cell_text}</td>')

        body_rows.append(
            f"""
            <tr>
              <th scope="row">
                {render_icon(ROLE_ICONS.get(role, ""), css_class="tech-icon role-icon")}
                <span data-i18n="role_{esc(role)}">{esc(ROLE_LABELS.get(role, role))}</span>
              </th>
              {"".join(cells)}
            </tr>
            """
        )

    return f"""
    <table class="compat-matrix">
      <thead>
        <tr>
          <th data-i18n="compat_corner">Role \\ Target</th>
          {header_cells}
        </tr>
      </thead>
      <tbody>
        {"".join(body_rows)}
      </tbody>
    </table>
    """


# ---------------------------------------------------------------------------
# Roadmap (v3) - the real maturity ladder, not a dated feature timeline.
# See feedback_no_dates_public_docs and ROADMAP_COMPAT_TRANSLATIONS above.
# ---------------------------------------------------------------------------

ROADMAP_ORDER = ["scaffolding", "functional", "established", "production"]

ROADMAP_ADVANCE_TEXT: dict[str, str] = {
    key: ROADMAP_COMPAT_TRANSLATIONS["en"][f"roadmap_advance_{key}"]
    for key in ROADMAP_ORDER
}

def render_roadmap(
    maturity_counts: dict[str, int],
) -> str:
    steps = []

    for key in ROADMAP_ORDER:
        count = maturity_counts.get(key, 0)
        label = MATURITY_LABELS.get(key, key)
        description = MATURITY_DESCRIPTIONS.get(key, "")
        advance = ROADMAP_ADVANCE_TEXT.get(key, "")
        css_class = MATURITY_CLASSES.get(key, "maturity-scaffolding")

        steps.append(
            f"""
            <li class="roadmap-step {css_class}">
              <div class="roadmap-step-head">
                <span class="maturity-badge {css_class}" data-i18n="maturity_{esc(key)}">{esc(label)}</span>
                <span class="roadmap-step-count">{count}</span>
              </div>
              <p class="roadmap-step-desc" data-i18n="maturity_desc_{esc(key)}">{esc(description)}</p>
              <p class="roadmap-step-advance" data-i18n="roadmap_advance_{esc(key)}">{esc(advance)}</p>
            </li>
            """
        )

    return "".join(steps)


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def render_html(
    entries: list[ProjectEntry],
    results: dict[str, RemoteStatus],
    meta: dict[str, RepoMeta],
    ecosystem_by_name: dict[str, str],
) -> str:
    stats = calculate_statistics(entries, results)

    total = int(stats["total"])
    ok = int(stats["ok"])
    errors = int(stats["errors"])
    success_percent = float(stats["success_percent"])

    deploy_counts = stats["deploy_counts"]
    stack_counts = stats["stack_counts"]
    maturity_counts = stats["maturity_counts"]
    role_counts = stats["role_counts"]
    role_deploy_matrix = stats["role_deploy_matrix"]

    rows = render_project_rows(entries, results, meta, ecosystem_by_name)

    ecosystem_cards = render_ecosystem_cards(entries, ecosystem_by_name)

    freshness_html = render_freshness_indicator()

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

    compatibility_matrix = render_compatibility_matrix(
        role_deploy_matrix,
        role_counts,
    )

    roadmap_steps = render_roadmap(
        maturity_counts,
    )

    family_options = "".join(
        f'<option value="{esc(name.lower())}">{esc(name)} ({len(children) + (1 if parent else 0)})</option>'
        for name, parent, children in ordered_projects(entries)
    )

    # Computed as a plain string, not built inside the f-string literal
    # below - the JSON itself is full of single `{`/`}` characters that
    # would otherwise collide with the f-string's own `{{`/`}}` escaping
    # convention. Substituting it in as one already-finished string value
    # (via `{i18n_json}` further down) sidesteps that entirely, since an
    # f-string only re-parses braces in its own literal text, never
    # inside an interpolated value.
    i18n_json = json.dumps(TRANSLATIONS, ensure_ascii=False)

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
  content="Electro Hobby 3D ecosystem status dashboard: live status for {total} projects across the HYDRA-UMC, URTC and A.R.M.O.R. ecosystems"
>

<title>Electro Hobby 3D - Ecosystem Status</title>

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
  /*
   * v3 palette: this ecosystem's own "HYDRA-UMC Studio Fasion" theme -
   * the same slate/steel-and-blue control-panel look HYDRA-UMC-STUDIO's
   * own theme picker ships as a named theme (see that project's own
   * src/index.css, body[data-theme="HYDRA-UMC Studio Fasion"]), and
   * HYDRA-UMC-SERVER's admin UI shares the same design language - muted
   * steel neutrals instead of a neon accent, emerald/blue/amber/red for
   * real semantic meaning (verified/trusted/pending/error) rather than
   * decoration, and beveled buttons + carved-in inputs (see .filter,
   * .deploy-card, .maturity-card, .role-item, .search input, the
   * selects, below) standing in for that theme's own embossed-metal
   * button treatment. Light mode is a real, independently-designed
   * complement (brushed steel, not a naive inversion) using the same
   * hue families at adjusted lightness for contrast on a light ground.
   */
  :root {{
    --bg: #e4e7ec;
    --surface: #f4f6f9;
    --surface-2: #e9ecf1;
    --border: #c7ccd6;
    --border-strong: #a8b0be;
    --text: #16202c;
    --dim: #5b6472;
    --accent: #3b82f6;
    --accent-soft: #dbeafe;
    --ok: #16a34a;
    --ok-soft: #dcfce7;
    --err: #dc2626;
    --err-soft: #fee2e2;
    --maturity-production: #16a34a;
    --maturity-production-soft: #dcfce7;
    --maturity-established: #3b82f6;
    --maturity-established-soft: #dbeafe;
    --maturity-scaffolding: #d97706;
    --maturity-scaffolding-soft: #fef3c7;
    --shadow: 0 4px 18px rgba(15, 23, 42, .08);
    --bevel-highlight: rgba(255, 255, 255, .55);
    --bevel-shadow: rgba(15, 23, 42, .25);
    --bg-texture: rgba(15, 23, 42, .025);
  }}

  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #0a0b10;
      --surface: #14161f;
      --surface-2: #202430;
      --border: #2e3444;
      --border-strong: #424a5e;
      --text: #f1f5f9;
      --dim: #94a3b8;
      --accent: #60a5fa;
      --accent-soft: #12233d;
      --ok: #22c55e;
      --ok-soft: #0f2e1c;
      --err: #ef4444;
      --err-soft: #2e1015;
      --maturity-production: #22c55e;
      --maturity-production-soft: #0f2e1c;
      --maturity-established: #60a5fa;
      --maturity-established-soft: #12233d;
      --maturity-scaffolding: #fbbf24;
      --maturity-scaffolding-soft: #3a2a08;
      --shadow: 0 4px 18px rgba(0, 0, 0, .4);
      --bevel-highlight: rgba(255, 255, 255, .16);
      --bevel-shadow: rgba(0, 0, 0, .6);
      --bg-texture: rgba(255, 255, 255, .02);
    }}
  }}

  /*
   * Explicit theme override (the toggle button). Repeats the same dark
   * token values as the media query above so a manual choice wins in both
   * directions - system says light + user picks dark, and vice versa.
   */
  :root[data-theme="dark"] {{
    --bg: #0a0b10;
    --surface: #14161f;
    --surface-2: #202430;
    --border: #2e3444;
    --border-strong: #424a5e;
    --text: #f1f5f9;
    --dim: #94a3b8;
    --accent: #60a5fa;
    --accent-soft: #12233d;
    --ok: #22c55e;
    --ok-soft: #0f2e1c;
    --err: #ef4444;
    --err-soft: #2e1015;
    --maturity-production: #22c55e;
    --maturity-production-soft: #0f2e1c;
    --maturity-established: #60a5fa;
    --maturity-established-soft: #12233d;
    --maturity-scaffolding: #fbbf24;
    --maturity-scaffolding-soft: #3a2a08;
    --shadow: 0 4px 18px rgba(0, 0, 0, .4);
    --bevel-highlight: rgba(255, 255, 255, .16);
    --bevel-shadow: rgba(0, 0, 0, .6);
    --bg-texture: rgba(255, 255, 255, .02);
  }}

  * {{
    box-sizing: border-box;
  }}

  html {{
    scroll-behavior: smooth;
  }}

  body {{
    margin: 0;
    background-color: var(--bg);
    /* The same subtle diagonal micro-pattern + radial vignette
       "HYDRA-UMC Studio Fasion" itself paints behind its own panels -
       here on `--bg`/`--surface` so it re-tints correctly for whichever
       theme (light/dark) is actually active, rather than the fixed
       dark-only hex pair that theme's own CSS hardcodes. */
    background-image:
      linear-gradient(45deg, var(--bg-texture) 25%, transparent 25%, transparent 50%, var(--bg-texture) 50%, var(--bg-texture) 75%, transparent 75%, transparent),
      radial-gradient(circle at center, var(--surface) 0%, var(--bg) 100%);
    background-size: 4px 4px, 100% 100%;
    background-attachment: fixed;
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

  /* REV-033: last-build freshness, distinct from the pass/fail badge
     above - a colored dot marks fresh/stale/failed/unknown at a glance,
     the text carries the real timestamp/age for anyone who wants it. */
  .freshness-indicator {{
    display: flex;
    align-items: center;
    gap: 7px;
    margin: 6px 0 0;
    font-size: 12.5px;
    color: var(--dim);
  }}

  .freshness-indicator::before {{
    content: "";
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 999px;
    flex-shrink: 0;
    background: var(--border-strong);
  }}

  .freshness-indicator.freshness-fresh::before {{
    background: var(--ok);
  }}

  .freshness-indicator.freshness-stale::before {{
    background: var(--maturity-scaffolding);
  }}

  .freshness-indicator.freshness-stale {{
    color: var(--maturity-scaffolding);
  }}

  .freshness-indicator.freshness-failed::before {{
    background: var(--err);
  }}

  .freshness-indicator.freshness-failed {{
    color: var(--err);
  }}

  .ecosystem-intro {{
    max-width: 930px;
    margin: 16px 0 0;
    padding: 14px 16px;
    color: var(--text);
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    box-shadow: var(--shadow);
    font-size: 14px;
    line-height: 1.65;
  }}

  .architecture-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
  }}

  .architecture-card {{
    min-height: 178px;
    padding: 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 8px;
    box-shadow: var(--shadow);
  }}

  .architecture-card h3 {{
    margin: 0 0 10px;
    color: var(--text);
    font-family: "IBM Plex Mono", monospace;
    font-size: 13px;
    letter-spacing: .06em;
    text-transform: uppercase;
  }}

  .architecture-card p {{
    margin: 0 0 10px;
    color: var(--dim);
    font-size: 12px;
    line-height: 1.5;
  }}

  .architecture-card ul {{
    margin: 0;
    padding-left: 17px;
    color: var(--text);
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
    line-height: 1.65;
  }}

  .architecture-flow {{
    display: flex;
    align-items: stretch;
    gap: 8px;
    margin-top: 14px;
    color: var(--dim);
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
  }}

  .architecture-flow span {{
    display: grid;
    place-items: center;
    flex: 1;
    min-height: 42px;
    padding: 7px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 6px;
    text-align: center;
  }}

  .architecture-flow b {{
    display: grid;
    place-items: center;
    color: var(--accent);
  }}

  .relationship-note {{
    margin: 14px 0 0;
    padding: 13px 16px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--surface-2);
    color: var(--dim);
    font-size: 12px;
    line-height: 1.6;
  }}

  .relationship-note strong {{
    color: var(--text);
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

  .header-controls {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }}

  .lang-select {{
    appearance: none;
    padding: 8px 10px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    border-radius: 8px;
    font-family: "IBM Plex Sans", sans-serif;
    font-size: 12.5px;
    cursor: pointer;
    box-shadow: var(--shadow);
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
    /* A.R.M.O.R.'s own role/deploy text is a real, free-text one-line
       description (up to ~140 characters), not a short curated word like
       HYDRA-UMC/URTC use for this same column - truncated here instead
       of blowing out this table's total width (which pushed Version/
       Status/Last commit far enough right to need a lot of hidden
       horizontal scrolling to ever see). The untruncated text is still
       real and reachable, in this same element's own `title` tooltip. */
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .role-icon {{
    color: var(--accent);
  }}

  /* --- Compatibility matrix (v3) ----------------------------------------- */

  .compat-matrix-wrapper {{
    overflow-x: auto;
  }}

  .compat-matrix {{
    border-collapse: collapse;
    width: 100%;
    font-family: "IBM Plex Mono", monospace;
    font-size: 12px;
  }}

  .compat-matrix th,
  .compat-matrix td {{
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: center;
    white-space: nowrap;
  }}

  .compat-matrix thead th {{
    background: var(--surface-2);
    color: var(--dim);
    font-weight: 600;
    font-size: 11px;
  }}

  .compat-matrix tbody th {{
    display: flex;
    align-items: center;
    gap: 8px;
    text-align: left;
    background: var(--surface-2);
    font-weight: 600;
    white-space: nowrap;
  }}

  .compat-cell-hit {{
    color: var(--accent);
    font-weight: 700;
    background: var(--accent-soft);
  }}

  .compat-cell-empty {{
    color: var(--dim);
    opacity: .5;
  }}

  /* --- Roadmap (v3) -------------------------------------------------------
   * Reuses the same maturity-* color tokens as the Maturity cards above -
   * the roadmap is that same classification, laid out as a ladder instead
   * of a filterable grid, not a second color scheme to keep in sync.
   */

  .roadmap-ladder {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 10px;
    list-style: none;
    margin: 0;
    padding: 0;
  }}

  .roadmap-step {{
    border: 1px solid var(--border);
    border-top: 4px solid var(--maturity-scaffolding);
    background: var(--surface);
    border-radius: 9px;
    padding: 13px 15px;
    box-shadow: var(--shadow);
  }}

  .roadmap-step.maturity-production {{ border-top-color: var(--maturity-production); }}
  .roadmap-step.maturity-established {{ border-top-color: var(--maturity-established); }}
  .roadmap-step.maturity-functional {{ border-top-color: var(--accent); }}
  .roadmap-step.maturity-scaffolding {{ border-top-color: var(--maturity-scaffolding); }}

  .roadmap-step-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }}

  .roadmap-step-count {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 18px;
    font-weight: 700;
    color: var(--dim);
  }}

  .roadmap-step-desc {{
    color: var(--text);
    font-size: 12px;
    line-height: 1.5;
    margin: 10px 0 0;
  }}

  .roadmap-step-advance {{
    color: var(--dim);
    font-size: 11.5px;
    line-height: 1.5;
    margin: 8px 0 0;
    padding-top: 8px;
    border-top: 1px dashed var(--border);
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

  .reset-filters {{
    appearance: none;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--dim);
    border-radius: 8px;
    padding: 9px 14px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 11.5px;
    cursor: pointer;
    transition:
      border-color .15s ease,
      color .15s ease;
  }}

  .reset-filters:hover {{
    border-color: var(--accent);
    color: var(--accent);
  }}

  .reset-filters:disabled {{
    opacity: .45;
    cursor: default;
    border-color: var(--border);
    color: var(--dim);
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

  .armor-section-intro {{
    color: var(--dim);
    font-size: 13px;
    max-width: 900px;
    margin: 0 0 14px;
  }}

  table.armor-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}

  table.armor-table th,
  table.armor-table td {{
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    text-align: left;
    vertical-align: top;
  }}

  table.armor-table th {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px;
    text-transform: uppercase;
    color: var(--dim);
  }}

  /* Marks the one point in the family list where URTC's own family
     ("URTC Tool Platform") begins - the same table, the same live scan,
     just a real visual boundary instead of an implicit alphabetical one. */
  tr.ecosystem-banner-row td {{
    background: var(--accent-soft);
    border-top: 2px solid var(--accent);
    border-bottom: 2px solid var(--accent);
    padding: 10px 14px;
    font-weight: 600;
    font-size: 12.5px;
    color: var(--accent);
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
    /* Same real free-text-description problem, and the same fix, as
       .role-badge above - see that rule's own comment. */
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: bottom;
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

  /*
   * "HYDRA-UMC Studio Fasion" button/input treatment (v3) - the same
   * embossed-metal look that theme's own body[data-theme="HYDRA-UMC
   * Studio Fasion"] CSS applies to every real <button>/<select>/<input>
   * in STUDIO (see that project's own src/index.css). Deliberately
   * layered on last, with `!important` on the gradient/shadow additions
   * only (never on background-color or the left accent border a card
   * like .maturity-card already carries), matching the exact reasoning
   * that source CSS itself needed `!important` for: real buttons/cards
   * on this page each set their OWN box-shadow/border-color earlier for
   * a real reason (the active-filter ring, the maturity accent stripe),
   * and a later same-specificity rule wouldn't otherwise beat that.
   */
  .filter,
  .deploy-card,
  .maturity-card,
  .role-item,
  .reset-filters,
  .theme-toggle {{
    background-image: linear-gradient(180deg, var(--bevel-highlight) 0%, transparent 45%, transparent 55%, var(--bevel-shadow) 100%) !important;
    box-shadow: inset 0 1px 0 var(--bevel-highlight), inset 0 -1px 2px var(--bevel-shadow) !important;
    border-top-color: var(--bevel-highlight) !important;
    border-bottom-color: var(--bevel-shadow) !important;
  }}

  .filter:hover,
  .deploy-card:hover,
  .maturity-card:hover,
  .role-item:hover,
  .reset-filters:hover:not(:disabled),
  .theme-toggle:hover {{
    filter: brightness(1.08);
  }}

  .filter:active,
  .deploy-card:active,
  .maturity-card:active,
  .role-item:active,
  .reset-filters:active:not(:disabled),
  .theme-toggle:active {{
    background-image: linear-gradient(180deg, var(--bevel-shadow) 0%, transparent 50%, var(--bevel-highlight) 100%) !important;
    box-shadow: inset 0 2px 3px var(--bevel-shadow) !important;
  }}

  .filter.active,
  .deploy-card.active,
  .maturity-card.active,
  .role-item.active {{
    box-shadow: inset 0 1px 0 var(--bevel-highlight), inset 0 -1px 2px var(--bevel-shadow), 0 0 0 2px var(--accent-soft) !important;
  }}

  /* Carved-in fields, the same theme's own select/input treatment -
     inverted gradient direction from the buttons above (recessed, not
     raised), same reasoning for the `!important`. */
  .search input,
  .family-filter select,
  .lang-select {{
    background-image: linear-gradient(180deg, var(--bevel-shadow) 0%, transparent 60%) !important;
    box-shadow: inset 0 2px 4px var(--bevel-shadow) !important;
  }}

  /* Panels get the same subtle top-highlight + inset shadow the source
     theme applies to .bg-slate-900/.bg-slate-950 - a slight embossed
     lift rather than a flat fill. */
  .health-card,
  .table-wrapper,
  .stack-item {{
    background-image: linear-gradient(180deg, var(--bevel-highlight) 0%, transparent 100%);
  }}

  @media (max-width: 700px) {{
    .wrap {{
      padding: 25px 12px 60px;
    }}

    .health {{
      grid-template-columns:
        repeat(2, minmax(0, 1fr));
    }}

    .architecture-grid {{
      grid-template-columns: 1fr;
    }}

    .architecture-flow {{
      flex-direction: column;
    }}

    .architecture-flow b {{
      transform: rotate(90deg);
      min-height: 18px;
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
        ELECTRO HOBBY 3D
      </div>

      <div class="header-controls">
        <select id="lang-select" class="lang-select" aria-label="Language / Idioma / Langue / Lingua / Sprache / 语言 / 言語">
          <option value="en">🇺🇸 English</option>
          <option value="es">🇪🇸 Español</option>
          <option value="fr">🇫🇷 Français</option>
          <option value="it">🇮🇹 Italiano</option>
          <option value="de">🇩🇪 Deutsch</option>
          <option value="zh">🇨🇳 简体中文</option>
          <option value="ja">🇯🇵 日本語</option>
        </select>

        <button
          id="theme-toggle"
          class="theme-toggle"
          type="button"
          aria-label="Toggle dark/light theme"
          title="Toggle dark/light theme"
          data-i18n-aria-label="theme_toggle"
          data-i18n-title="theme_toggle"
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
    </div>

    <h1>
      <span data-i18n="header_title">Ecosystem Status Dashboard</span>
      <span class="version-pill">v3</span>
    </h1>

    <!--
      CAT-01 (P2): "content unchanged" and "the hourly check has silently
      stopped running" used to look identical on this page - no
      generation timestamp is written here on purpose (see this
      script's own header comment on why), so there was no visible
      signal at all distinguishing the two. GitHub's own Actions status
      badge is a real, live, always-current answer to "did the last
      scheduled check actually run and succeed" - it needs no sidecar
      file/extra commit of its own to stay honest, unlike a timestamp
      baked into this static page would.
    -->
    <p class="subtitle">
      <a href="https://github.com/JuanenRac/JuanenRac/actions/workflows/build-dashboard.yml" target="_blank" rel="noopener">
        <img
          src="https://github.com/JuanenRac/JuanenRac/actions/workflows/build-dashboard.yml/badge.svg"
          alt="Ecosystem dashboard build status - click for the live run history"
        >
      </a>
    </p>

    {freshness_html}

    <p
        class="subtitle"
        data-i18n-template="subtitle_main"
        data-ok="{ok}"
        data-total="{total}"
        data-percent="{success_percent_text}"
    >
      {ok}/{total} repositories resolved successfully
      · {success_percent_text} healthy
      · metadata and versions are read from each repository manifest
      · dashboard generated by GitHub Actions
      · static GitHub Pages
    </p>

    <p class="subtitle subtitle-v3" data-i18n="subtitle_v3">
      v3: real maturity/role classification, family/parent trees and richer
      per-project notes - see the Maturity legend below for exactly how
      each level was decided.
    </p>

    <p class="ecosystem-intro" data-i18n="architecture_intro">
      Electro Hobby 3D is three independent engineering ecosystems by the
      same author: HYDRA-UMC (industrial multi-robot platform), URTC (its
      universal robot-tool subsystem, an independent product with its own
      firmware) and A.R.M.O.R. (perimeter security and home automation).
      This dashboard discovers and lists every one of them live; each
      ecosystem's own family groups are labeled below, and HYDRA-UMC's own
      deeper architecture is detailed in the section right after this one.
    </p>
  </header>


  <!-- ================================================================
       SYSTEM ARCHITECTURE
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="architecture_section">HYDRA-UMC: System architecture</div>

    <div class="architecture-grid">
      <article class="architecture-card">
        <h3 data-i18n="architecture_platform_title">Platform foundation</h3>
        <p data-i18n="architecture_platform_body">Raspberry Pi OS ARM64 remains the operating-system base. The
        HYDRA-UMC layer adds device profiles, diagnostics and service lifecycle.</p>
        <ul><li>HYDRA-UMC-OS</li><li>CM5 / Linux</li><li>systemd / udev</li><li>MCU / URTC boundary</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_contracts_title">Contracts and operations</h3>
        <p data-i18n="architecture_contracts_body">The SDK defines stable data and command contracts; Server, UI and
        tools use those contracts instead of raw hardware protocols.</p>
        <ul><li>HYDRA-UMC-SDK</li><li>Server / Studio / Suite</li><li>DSI / mobile / CLI</li><li>Job Dispatcher</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_perception_title">Perception and intelligence</h3>
        <p data-i18n="architecture_perception_body">Vision and AI are optional capabilities. Their output is validated
        before it can influence a mission; they are never safety authority.</p>
        <ul><li>Vision Streamer / Node</li><li>Detection HEF</li><li>Cognitive / VLA</li><li>Safety Zones</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_engineering_title">Engineering and industry</h3>
        <p data-i18n="architecture_engineering_body">Simulation, telemetry and standards make the physical cell
        observable, testable and interoperable.</p>
        <ul><li>Twin / Physics / HIL</li><li>Telemetry / DataLake</li><li>OPC-UA / MQTT</li><li>MTConnect / Gateway</li></ul>
      </article>
    </div>

    <div class="architecture-flow" aria-label="HYDRA-UMC control flow">
      <span data-i18n="architecture_flow_operator">Operator interfaces</span><b>→</b><span data-i18n="architecture_flow_services">Server and SDK</span><b>→</b><span data-i18n="architecture_flow_adapter">CM5-MCU adapter</span><b>→</b><span data-i18n="architecture_flow_machine">MCU / URTC / machine</span>
    </div>

    <div class="relationship-note">
      <strong data-i18n="architecture_relationship_title">HYDRA-UMC and URTC:</strong> <span data-i18n="architecture_relationship_body">HYDRA-UMC is the platform and cell
      controller. URTC is its universal robot-tool subsystem, with independent
      firmware and maintenance tools. The MCU remains authoritative for physical
      limits and safe stop; UI, network and AI cannot bypass that boundary.</span>
    </div>

  </section>


  <!-- ================================================================
       URTC SYSTEM ARCHITECTURE
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="architecture_section_u">URTC: System architecture</div>

    <div class="architecture-grid">
      <article class="architecture-card">
        <h3 data-i18n="architecture_u_card1_title">Tool-head firmware</h3>
        <p data-i18n="architecture_u_card1_body">An STM32F303 runs each tool head over CAN, reading its own 5-bit
        hardware address to auto-configure power stages, sensors and safety logic for one of 25 built-in tool profiles.</p>
        <ul><li>STM32F303</li><li>CAN bus</li><li>5-bit ID matrix</li><li>25 tool profiles</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_u_card2_title">Expansion and motion</h3>
        <p data-i18n="architecture_u_card2_body">A 20-pin expansion connector adds a second stepper axis or sensor
        board through one of six interchangeable variants, sharing STEP/DIR/EN wiring between a TMC2209 and a TMC5160 driver.</p>
        <ul><li>TMC2209 / TMC5160</li><li>6 expansion boards</li><li>F-RAM persistence</li><li>OLED diagnostics</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_u_card3_title">Maintenance tools</h3>
        <p data-i18n="architecture_u_card3_body">URTC-FLASHER updates firmware over CAN without removing the board,
        URTC-TESTER exercises the protocol end to end and URTC-UPDATER keeps every desktop tool current from GitHub.</p>
        <ul><li>URTC-FLASHER</li><li>URTC-TESTER</li><li>URTC-UPDATER</li><li>CAN-OTA</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_u_card4_title">Vision and operation</h3>
        <p data-i18n="architecture_u_card4_body">URTC-VISION-TOOL adds camera-based tool inspection, URTC-WEB-STUDIO
        gives it a browser console and URTC-SMART-RACK stores and identifies tool heads between changes.</p>
        <ul><li>URTC-VISION-TOOL</li><li>URTC-WEB-STUDIO</li><li>URTC-SMART-RACK</li></ul>
      </article>
    </div>

    <div class="architecture-flow" aria-label="URTC control flow">
      <span data-i18n="architecture_u_flow_1">Tool head</span><b>→</b><span data-i18n="architecture_u_flow_2">STM32F303 firmware</span><b>→</b><span data-i18n="architecture_u_flow_3">CAN bus</span><b>→</b><span data-i18n="architecture_u_flow_4">HYDRA-UMC MCU / host</span>
    </div>

    <div class="relationship-note">
      <strong data-i18n="architecture_u_rel_title">URTC on its own, and paired with HYDRA-UMC:</strong> <span data-i18n="architecture_u_rel_body">URTC is an independent, unofficial
      project - a CAN-based tool-head controller built to work with PAROL6/Faze4-style arms, with its own firmware,
      hardware and maintenance tools. When it is the tool subsystem of a HYDRA-UMC cell, HYDRA-UMC's own MCU keeps
      authority over physical limits and safe stop; URTC never bypasses that boundary.</span>
    </div>

  </section>


  <!-- ================================================================
       A.R.M.O.R. SYSTEM ARCHITECTURE
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="architecture_section_a">A.R.M.O.R.: System architecture</div>

    <div class="architecture-grid">
      <article class="architecture-card">
        <h3 data-i18n="architecture_a_card1_title">Network segmentation</h3>
        <p data-i18n="architecture_a_card1_body">Field nodes and cameras sit on their own VLAN with no internet
        access; the MQTT broker and server live on a core VLAN; Studio and the Android app reach the server from a client VLAN.</p>
        <ul><li>VLAN 10 field</li><li>VLAN 20 core</li><li>VLAN 30 clients</li><li>MQTT, one identity per node</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_a_card2_title">Field nodes</h3>
        <p data-i18n="architecture_a_card2_body">ESP32-S3 radar, solar and electrical nodes publish sensor and
        equipment readings; the solar and electrical ones only read, never write to an inverter, battery or meter.</p>
        <ul><li>ARMOR-RADAR</li><li>ARMOR-SOLAR</li><li>ARMOR-ELECTRICAL</li><li>ARMOR-NETWORK</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_a_card3_title">Perception, never authority</h3>
        <p data-i18n="architecture_a_card3_body">Visual and voice AI recommend a severity or an intent with reasons
        attached; authorizes_action is always false until the server itself authenticates and confirms.</p>
        <ul><li>ARMOR-SERVER-AI</li><li>ARMOR-VOICE-AI</li><li>Recommend, never act</li></ul>
      </article>
      <article class="architecture-card">
        <h3 data-i18n="architecture_a_card4_title">State and operator consoles</h3>
        <p data-i18n="architecture_a_card4_body">ARMOR-SERVER is the only place that ever touches a camera password
        or an RTSP address; Studio and the Android app are its authenticated clients, and a phone can set a new node up over Bluetooth alone.</p>
        <ul><li>ARMOR-SERVER</li><li>ARMOR-STUDIO</li><li>ARMOR-ANDROID-CONTROL</li><li>BLE set-up only</li></ul>
      </article>
    </div>

    <div class="architecture-flow" aria-label="A.R.M.O.R. control flow">
      <span data-i18n="architecture_a_flow_1">Field nodes and cameras</span><b>→</b><span data-i18n="architecture_a_flow_2">MQTT broker and server</span><b>→</b><span data-i18n="architecture_a_flow_3">AI recommendation</span><b>→</b><span data-i18n="architecture_a_flow_4">Authenticated client session</span>
    </div>

    <div class="relationship-note">
      <strong data-i18n="architecture_a_rel_title">A.R.M.O.R.'s own boundary:</strong> <span data-i18n="architecture_a_rel_body">The server is the only component that
      authorises an action or holds a camera credential. Visual and voice AI only recommend; solar and electrical
      nodes only read - the rules for switching an electrical source are tested in software but not yet linked to any real hardware.</span>
    </div>

  </section>


  <!-- ================================================================
       HEALTH
       ================================================================ -->

  <section class="health">

    <div class="health-card">
      <div id="health-total" class="number">
        {total}
      </div>
      <div class="label" data-i18n="health_total">
        Total projects
      </div>
    </div>

    <div class="health-card ok">
      <div id="health-resolved" class="number">
        {ok}
      </div>
      <div class="label" data-i18n="health_resolved">
        Version resolved
      </div>
    </div>

    <div class="health-card error">
      <div id="health-errors" class="number">
        {errors}
      </div>
      <div class="label" data-i18n="health_errors">
        Errors / unknown
      </div>
    </div>

    <div class="health-card">
      <div id="health-percent" class="number">
        {success_percent_text}
      </div>
      <div class="label" data-i18n="health_registry">
        Registry health
      </div>
    </div>

  </section>


  <!-- ================================================================
       PROJECTS BY ECOSYSTEM
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="section_by_ecosystem">
      Projects by ecosystem
    </div>

    <div class="health">
      {ecosystem_cards}
    </div>

  </section>


  <!-- ================================================================
       DEPLOYMENT
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="section_deploy">
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

    <div class="section-title" data-i18n="section_stack">
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
      <span data-i18n="section_maturity">Maturity</span>
      <span class="section-title-hint" data-i18n="section_maturity_hint">click a card to filter · hover for how it was decided</span>
    </div>

    <div class="maturity-grid">
      {maturity_cards}
    </div>

  </section>


  <!-- ================================================================
       ROLE (v3)
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="section_role">
      Role
    </div>

    <div class="role-summary">
      {role_summary}
    </div>

  </section>


  <!-- ================================================================
       COMPATIBILITY MATRIX (v3)
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="compat_section">
      Compatibility matrix
    </div>

    <p class="ecosystem-intro" data-i18n="compat_intro">
      Real project counts by role and deployment target, drawn straight
      from every repository's own manifest. A count, not a claim that any
      two specific projects interoperate.
    </p>

    <div class="compat-matrix-wrapper">
      {compatibility_matrix}
    </div>

  </section>


  <!-- ================================================================
       ROADMAP (v3)
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="roadmap_section">
      Roadmap
    </div>

    <p class="ecosystem-intro" data-i18n="roadmap_intro">
      Not a feature timeline with dates - the real path every project in
      this ecosystem follows, and exactly where each one sits on it right
      now (see the Maturity section above for the live counts).
    </p>

    <ol class="roadmap-ladder">
      {roadmap_steps}
    </ol>

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
        data-i18n-placeholder="search_placeholder"
        data-i18n-aria-label="search_aria"
      >
    </div>

    <div class="filters">

      <button
        class="filter active"
        type="button"
        data-filter-status="all"
        data-i18n="filter_all"
      >
        All
      </button>

      <button
        class="filter"
        type="button"
        data-filter-status="ok"
        data-i18n="filter_ok"
      >
        ✓ OK
      </button>

      <button
        class="filter"
        type="button"
        data-filter-status="error"
        data-i18n="filter_error"
      >
        ⚠ Errors
      </button>

    </div>

    <div class="family-filter">
      <label for="family-select" data-i18n="family_label">Family:</label>
      <select id="family-select">
        <option value="all" data-i18n="family_all">All families</option>
        {family_options}
      </select>
    </div>

    <button
        id="reset-filters"
        class="reset-filters"
        type="button"
        data-i18n="reset_filters"
        title="Clear the search box and every active filter (status, deploy, maturity, role, family)"
        data-i18n-title="reset_filters_title"
    >
      ⟲ Reset
    </button>

  </section>


  <!-- ================================================================
       PROJECT TABLE
       ================================================================ -->

  <section class="table-wrapper">

    <table>

      <thead>
        <tr>
          <th data-i18n="th_project">Project</th>
          <th data-i18n="th_type">Type</th>
          <th data-i18n="th_maturity">Maturity</th>
          <th data-i18n="th_stack">Stack</th>
          <th data-i18n="th_deploy">Deploy target</th>
          <th data-i18n="th_version">Version</th>
          <th data-i18n="th_status">Status</th>
          <th data-i18n="th_commit">Last commit</th>
        </tr>
      </thead>

      <tbody id="project-table">
        {rows}
      </tbody>

    </table>

    <div
      id="empty-results"
      class="empty"
      data-i18n="empty_results"
    >
      No projects match the current filters.
    </div>

  </section>

  <!-- ================================================================
       FOOTER
       ================================================================ -->

  <footer>

    <span data-i18n="footer_registry">Data source:</span>
    <a
      href="https://github.com/JuanenRac/HYDRA-UMC-UPDATER"
      target="_blank"
      rel="noopener noreferrer"
    >
      HYDRA-UMC-UPDATER
    </a>

    ·

    <span data-i18n="footer_generator">Dashboard generator:</span>
    <a
      href="https://github.com/JuanenRac/JuanenRac/blob/main/scripts/generate_dashboard.py"
      target="_blank"
      rel="noopener noreferrer"
    >
      generate_dashboard.py
    </a>

    ·

    <span data-i18n="footer_workflow">Workflow:</span>
    <a
      href="https://github.com/JuanenRac/JuanenRac/blob/main/.github/workflows/build-dashboard.yml"
      target="_blank"
      rel="noopener noreferrer"
    >
      build-dashboard.yml
    </a>

    ·

    <span data-i18n="footer_note">Each repository manifest is the source of truth for its public metadata
    and version.</span>

  </footer>

</div>


<script>
(function () {{
  "use strict";

  // --- Language (v3) ---------------------------------------------------
  //
  // I18N covers this page's own UI chrome and its closed vocabulary
  // (deploy targets, maturity levels + tooltips, roles, OK/ERROR) in all
  // 7 languages - see TRANSLATIONS's own module docstring in
  // generate_dashboard.py for exactly what is and isn't translated, and
  // why. Applied client-side (this script runs after every element below
  // it in the DOM has already parsed, so a brief flash of the English
  // fallback text before this runs is a real, accepted trade-off of a
  // static, no-backend page - the same reasoning the theme toggle's own
  // early <head> script exists to avoid for color, but can't for text
  // content that needs its element to exist first).

  const I18N = {i18n_json};

  const LANG_KEY = "hydra-dashboard-lang";

  const langSelect =
    document.getElementById("lang-select");

  function resolveInitialLang() {{
    try {{
      const saved = localStorage.getItem(LANG_KEY);
      if (saved && I18N[saved]) {{
        return saved;
      }}
    }} catch (e) {{
      // Private browsing / storage disabled - falls through to browser
      // language detection below, same as any other viewer without a
      // saved choice.
    }}

    const browserLang =
      (navigator.language || "en").slice(0, 2).toLowerCase();

    return I18N[browserLang] ? browserLang : "en";
  }}

  // Fills a translated template string's own `{{key}}` placeholders from
  // the SAME element's own `data-key` attribute (e.g. `{{ok}}` reads
  // `data-ok`) - those attributes are computed once in Python at
  // generation time (real counts from this actual run), so this never
  // needs to recompute anything, just relocate already-correct numbers
  // into whichever language's own sentence shape.
  function fillTemplate(template, el) {{
    return template.replace(/\\{{(\\w+)\\}}/g, function (_match, key) {{
      const value = el.getAttribute("data-" + key);
      return value !== null ? value : "";
    }});
  }}

  function applyLanguage(lang) {{
    const dict = I18N[lang] || I18N.en;

    document.documentElement.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {{
      const key = el.getAttribute("data-i18n");
      if (Object.prototype.hasOwnProperty.call(dict, key)) {{
        el.textContent = dict[key];
      }}
    }});

    document.querySelectorAll("[data-i18n-template]").forEach(function (el) {{
      const key = el.getAttribute("data-i18n-template");
      if (Object.prototype.hasOwnProperty.call(dict, key)) {{
        el.textContent = fillTemplate(dict[key], el);
      }}
    }});

    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {{
      const key = el.getAttribute("data-i18n-title");
      if (Object.prototype.hasOwnProperty.call(dict, key)) {{
        el.setAttribute("title", dict[key]);
      }}
    }});

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {{
      const key = el.getAttribute("data-i18n-placeholder");
      if (Object.prototype.hasOwnProperty.call(dict, key)) {{
        el.setAttribute("placeholder", dict[key]);
      }}
    }});

    document.querySelectorAll("[data-i18n-aria-label]").forEach(function (el) {{
      const key = el.getAttribute("data-i18n-aria-label");
      if (Object.prototype.hasOwnProperty.call(dict, key)) {{
        el.setAttribute("aria-label", dict[key]);
      }}
    }});

    if (langSelect) {{
      langSelect.value = lang;
    }}
  }}

  applyLanguage(resolveInitialLang());

  if (langSelect) {{
    langSelect.addEventListener("change", function () {{
      const next = langSelect.value;
      applyLanguage(next);

      try {{
        localStorage.setItem(LANG_KEY, next);
      }} catch (e) {{
        // Storage unavailable - the switch still works for this page
        // view, it just won't be remembered next visit.
      }}
    }});
  }}

  // --- Dashboard build freshness (REV-033) ------------------------------
  //
  // Fetched live, from the viewer's own browser, every time this page is
  // actually opened - the same live approach the Actions badge.svg <img>
  // above already uses. Deliberately NOT computed in Python and baked
  // into this file at generation time: see generate_dashboard.py's own
  // REV-033 comment on DASHBOARD_WORKFLOW_FILE for why (that value
  // changes on every hourly run regardless of real content changes,
  // which would turn an occasional real commit into an hourly one).

  const FRESHNESS_WORKFLOW_FILE = "build-dashboard.yml";
  const FRESHNESS_STALE_AFTER_HOURS = 4;

  function formatFreshnessAge(elapsedMs) {{
    const hours = Math.floor(elapsedMs / 3600000);
    if (hours < 1) {{
      const minutes = Math.max(1, Math.floor(elapsedMs / 60000));
      return minutes + "m";
    }}
    if (hours < 48) {{
      return hours + "h";
    }}
    return Math.floor(hours / 24) + "d";
  }}

  function renderFreshness(state) {{
    const el = document.getElementById("dashboard-freshness");
    if (!el) return;

    el.classList.remove(
      "freshness-pending", "freshness-fresh", "freshness-stale",
      "freshness-failed", "freshness-unknown"
    );
    el.removeAttribute("data-i18n");
    el.removeAttribute("data-i18n-template");

    if (state.kind === "unknown") {{
      el.classList.add("freshness-unknown");
      el.setAttribute("data-i18n", "freshness_unknown");
    }} else if (state.kind === "failed") {{
      el.classList.add("freshness-failed");
      el.setAttribute("data-conclusion", state.conclusion);
      el.setAttribute("data-absolute", state.absolute);
      el.setAttribute("data-i18n-template", "freshness_failed");
    }} else {{
      el.classList.add(state.stale ? "freshness-stale" : "freshness-fresh");
      el.setAttribute("data-age", state.age);
      el.setAttribute("data-absolute", state.absolute);
      el.setAttribute("data-i18n-template", "freshness_checking");
    }}

    // Re-run the same translation pass so this one element (now carrying
    // fresh data-* attributes/i18n key) renders in whichever language is
    // currently active - identical mechanism every other templated
    // string on this page already uses.
    applyLanguage(langSelect ? langSelect.value : resolveInitialLang());
  }}

  fetch(
    "https://api.github.com/repos/JuanenRac/JuanenRac/actions/workflows/" +
      FRESHNESS_WORKFLOW_FILE + "/runs?status=completed&per_page=1"
  )
    .then(function (response) {{
      if (!response.ok) throw new Error("freshness: bad response");
      return response.json();
    }})
    .then(function (payload) {{
      const runs = payload && payload.workflow_runs;
      if (!Array.isArray(runs) || runs.length === 0) {{
        throw new Error("freshness: no completed runs");
      }}
      const run = runs[0];
      const conclusion = run.conclusion;
      const updatedAt = run.updated_at;
      if (typeof conclusion !== "string" || typeof updatedAt !== "string") {{
        throw new Error("freshness: malformed run");
      }}

      if (conclusion !== "success") {{
        renderFreshness({{ kind: "failed", conclusion: conclusion, absolute: updatedAt }});
        return;
      }}

      const elapsedMs = Date.now() - new Date(updatedAt).getTime();
      renderFreshness({{
        kind: "ok",
        age: formatFreshnessAge(elapsedMs),
        absolute: updatedAt,
        stale: elapsedMs > FRESHNESS_STALE_AFTER_HOURS * 3600000,
      }});
    }})
    .catch(function () {{
      // Network error, rate limit, malformed payload - never guess or
      // leave the earlier "Checking..." placeholder standing forever;
      // this is the explicit, honest "can't tell right now" state.
      renderFreshness({{ kind: "unknown" }});
    }});


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

  const resetFiltersBtn =
    document.getElementById("reset-filters");

  const healthTotal =
    document.getElementById("health-total");

  const healthResolved =
    document.getElementById("health-resolved");

  const healthErrors =
    document.getElementById("health-errors");

  const healthPercent =
    document.getElementById("health-percent");

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
    let visibleOk = 0;
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
        if (status === "ok") {{
          visibleOk += 1;
        }}
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

    const visibleErrors = visible - visibleOk;
    const visiblePercent = visible
      ? Math.round((visibleOk / visible) * 1000) / 10
      : 0;

    if (healthTotal) {{ healthTotal.textContent = String(visible); }}
    if (healthResolved) {{ healthResolved.textContent = String(visibleOk); }}
    if (healthErrors) {{ healthErrors.textContent = String(visibleErrors); }}
    if (healthPercent) {{ healthPercent.textContent = String(visiblePercent) + "%"; }}

    if (resetFiltersBtn) {{
      const anyFilterActive =
        query.length > 0 ||
        activeStatus !== "all" ||
        activeDeploy !== "all" ||
        activeMaturity !== "all" ||
        activeRole !== "all" ||
        activeFamily !== "all";

      resetFiltersBtn.disabled = !anyFilterActive;
    }}
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

  if (resetFiltersBtn) {{
    resetFiltersBtn.addEventListener("click", function () {{
      searchInput.value = "";

      activeStatus = "all";
      activeDeploy = "all";
      activeMaturity = "all";
      activeRole = "all";

      statusFilters.forEach(function (item) {{
        item.classList.toggle(
          "active",
          item.dataset.filterStatus === "all"
        );
      }});

      deployFilters.forEach(function (item) {{
        item.classList.remove("active");
      }});

      maturityFilters.forEach(function (item) {{
        item.classList.remove("active");
      }});

      roleFilters.forEach(function (item) {{
        item.classList.remove("active");
      }});

      if (familySelect) {{
        familySelect.value = "all";
      }}

      applyFilters();
    }});
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
    catalog = parse_catalog(CATALOG_PATH.read_text(encoding="utf-8"))

    print(
        f"Discovering HYDRA-UMC repositories for "
        f"{catalog.github_owner} from GitHub...",
        file=sys.stderr,
    )

    discovery = discover_remote_projects(catalog.github_owner, token=GITHUB_TOKEN)
    statuses = [
        status
        for status in discovery.projects
        if status.entry.name not in catalog.dashboard_exclude
    ]
    results: dict[str, RemoteStatus] = {status.entry.name: status for status in statuses}
    entries: list[ProjectEntry] = [status.entry for status in statuses]
    ecosystem_by_name: dict[str, str] = {entry.name: "hydra-umc" for entry in entries}
    all_discovery_errors = list(discovery.errors)

    hydra_umc_total = len(entries)

    # Do not replace a working public dashboard with an empty page when the
    # API token, GitHub listing or manifests are temporarily unavailable.
    # An intentionally empty ecosystem is not a valid production state.
    if hydra_umc_total == 0:
        print(
            "ERROR: no valid HYDRA-UMC manifests were discovered; preserving the current dashboard.",
            file=sys.stderr,
        )
        return 1

    # URTC and A.R.M.O.R. each ship their own dedicated updater/discovery
    # client (see the import comment above) - both ecosystems are public, so
    # this needs no separate catalog file or token. A single ecosystem's own
    # discovery failing (a real GitHub outage, a bad manifest push) no
    # longer takes the whole dashboard down with it: it is logged as a
    # warning and that ecosystem's own count for this run is 0, same as any
    # other transient discovery error already handled per-project below -
    # only a HYDRA-UMC-wide failure (checked above) still preserves the
    # previous dashboard outright, since HYDRA-UMC never has zero real
    # projects and an empty result there is never legitimate.
    for ecosystem_key, ecosystem_label, discover in (
        ("urtc", "URTC", discover_urtc_projects),
        ("armor", "A.R.M.O.R.", discover_armor_projects),
    ):
        print(f"Discovering {ecosystem_label} repositories for {catalog.github_owner} from GitHub...", file=sys.stderr)
        try:
            sub_discovery = discover(catalog.github_owner, token=GITHUB_TOKEN or None)
        except Exception as exc:  # noqa: BLE001 - a real, unexpected client failure must not take down the other two ecosystems
            print(f"WARNING: {ecosystem_label} discovery failed: {exc}", file=sys.stderr)
            continue
        for status in sub_discovery.projects:
            results[status.entry.name] = status
            entries.append(status.entry)
            ecosystem_by_name[status.entry.name] = ecosystem_key
        all_discovery_errors.extend(sub_discovery.errors)
        print(f"{ecosystem_label}: {len(sub_discovery.projects)} project(s) discovered.", file=sys.stderr)

    total = len(entries)

    ok = sum(1 for result in results.values() if result.version is not None)

    errors = total - ok

    print(
        f"{ok}/{total} resolved "
        f"({errors} errors/unknown) across all three ecosystems.",
        file=sys.stderr,
    )

    # Invalid manifests are intentionally not rendered as projects. They are
    # still reported in CI so a repository cannot disappear silently.
    if all_discovery_errors:
        print(
            "\nDiscovery warnings:",
            file=sys.stderr,
        )
        for error in all_discovery_errors:
            print(f"  - {error}", file=sys.stderr)

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

    meta = fetch_all_meta(entries)

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

    # Template indentation must not leak as trailing whitespace into the
    # published static page. Normalising it here keeps local and CI-generated
    # output identical without manually editing generated HTML.
    rendered = render_html(entries, results, meta, ecosystem_by_name)
    clean_rendered = "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
    index_path.write_text(clean_rendered, encoding="utf-8")

    # Tell GitHub Pages that this is plain static HTML.
    (OUT_DIR / ".nojekyll").touch()

    print(
        f"Wrote {index_path}",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
