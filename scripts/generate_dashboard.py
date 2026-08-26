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


# ---------------------------------------------------------------------------
# Translations (v3) - the dashboard's own UI chrome and closed vocabulary
# (deploy targets, maturity levels + their tooltip descriptions, roles,
# real-vs-error status labels), in all 7 languages this ecosystem's own
# READMEs already ship. Deliberately does NOT translate project names,
# family names, or the free-text `notes`/`tech` content that comes straight
# from HYDRA-UMC-UPDATER/registry.py - that content is real, specific
# engineering documentation with registry.py as its single source of
# truth; maintaining 7 parallel copies of it would make the registry stop
# being that. `{ok}`/`{total}`/`{percent}`/`{count}` placeholders below are
# filled in client-side by the matching `data-*` attribute already on that
# element (computed once, at generation time, in whichever numbers this
# run actually found) - see applyLanguage() in the page's own <script>.
# ---------------------------------------------------------------------------

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "header_title": "Ecosystem Status Dashboard",
        "subtitle_main": "{ok}/{total} repositories resolved successfully · {percent} healthy · versions are read from each project's own source file · dashboard generated by GitHub Actions · static GitHub Pages",
        "subtitle_v3": "v3: real maturity/role classification, family/parent trees and richer per-project notes - see the Maturity legend below for exactly how each level was decided.",
        "theme_toggle": "Toggle dark/light theme",
        "health_total": "Total projects",
        "health_resolved": "Version resolved",
        "health_errors": "Errors / unknown",
        "health_registry": "Registry health",
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
        "footer_registry": "Registry source:",
        "footer_generator": "Dashboard generator:",
        "footer_workflow": "Workflow:",
        "footer_note": "The registry remains the single source of truth for project/version locations.",
        "version_status_ok": "OK",
        "version_status_error": "ERROR",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "User PC",
        "deploy_mobile": "Mobile",
        "deploy_wearable": "Wearable",
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
    },
    "es": {
        "header_title": "Panel de Estado del Ecosistema",
        "subtitle_main": "{ok}/{total} repositorios resueltos correctamente · {percent} saludable · las versiones se leen del propio archivo fuente de cada proyecto · panel generado por GitHub Actions · GitHub Pages estático",
        "subtitle_v3": "v3: clasificación real de madurez/rol, árboles de familia/padre-hijo y notas por proyecto más completas - ver la leyenda de Madurez más abajo para saber exactamente cómo se decidió cada nivel.",
        "theme_toggle": "Cambiar tema claro/oscuro",
        "health_total": "Proyectos totales",
        "health_resolved": "Versión resuelta",
        "health_errors": "Errores / desconocido",
        "health_registry": "Salud del registro",
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
        "footer_registry": "Fuente del registro:",
        "footer_generator": "Generador del panel:",
        "footer_workflow": "Workflow:",
        "footer_note": "El registro sigue siendo la única fuente de verdad para las ubicaciones de proyecto/versión.",
        "version_status_ok": "OK",
        "version_status_error": "ERROR",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "PC del usuario",
        "deploy_mobile": "Móvil",
        "deploy_wearable": "Wearable",
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
    },
    "fr": {
        "header_title": "Tableau de bord d'état de l'écosystème",
        "subtitle_main": "{ok}/{total} dépôts résolus avec succès · {percent} en bonne santé · les versions sont lues depuis le propre fichier source de chaque projet · tableau de bord généré par GitHub Actions · GitHub Pages statique",
        "subtitle_v3": "v3 : classification réelle de maturité/rôle, arbres famille/parent-enfant et notes par projet plus complètes - voir la légende Maturité ci-dessous pour savoir exactement comment chaque niveau a été décidé.",
        "theme_toggle": "Basculer le thème clair/sombre",
        "health_total": "Projets au total",
        "health_resolved": "Version résolue",
        "health_errors": "Erreurs / inconnu",
        "health_registry": "Santé du registre",
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
        "footer_registry": "Source du registre :",
        "footer_generator": "Générateur du tableau de bord :",
        "footer_workflow": "Workflow :",
        "footer_note": "Le registre reste la seule source de vérité pour l'emplacement des projets/versions.",
        "version_status_ok": "OK",
        "version_status_error": "ERREUR",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "PC utilisateur",
        "deploy_mobile": "Mobile",
        "deploy_wearable": "Wearable",
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
    },
    "it": {
        "header_title": "Dashboard di stato dell'ecosistema",
        "subtitle_main": "{ok}/{total} repository risolti correttamente · {percent} in salute · le versioni sono lette dal file sorgente proprio di ciascun progetto · dashboard generata da GitHub Actions · GitHub Pages statico",
        "subtitle_v3": "v3: classificazione reale di maturità/ruolo, alberi famiglia/genitore-figlio e note per progetto più ricche - vedi la legenda Maturità qui sotto per sapere esattamente come è stato deciso ogni livello.",
        "theme_toggle": "Cambia tema chiaro/scuro",
        "health_total": "Progetti totali",
        "health_resolved": "Versione risolta",
        "health_errors": "Errori / sconosciuto",
        "health_registry": "Salute del registro",
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
        "footer_registry": "Fonte del registro:",
        "footer_generator": "Generatore della dashboard:",
        "footer_workflow": "Workflow:",
        "footer_note": "Il registro rimane l'unica fonte di verità per le posizioni di progetto/versione.",
        "version_status_ok": "OK",
        "version_status_error": "ERRORE",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "PC dell'utente",
        "deploy_mobile": "Mobile",
        "deploy_wearable": "Wearable",
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
    },
    "de": {
        "header_title": "Ökosystem-Statusdashboard",
        "subtitle_main": "{ok}/{total} Repositories erfolgreich aufgelöst · {percent} gesund · Versionen werden aus der eigenen Quelldatei jedes Projekts gelesen · Dashboard generiert von GitHub Actions · statisches GitHub Pages",
        "subtitle_v3": "v3: echte Reifegrad-/Rollen-Klassifizierung, Familie/Eltern-Kind-Bäume und umfangreichere Notizen pro Projekt - siehe die Legende 'Reifegrad' unten für genau, wie jede Stufe entschieden wurde.",
        "theme_toggle": "Hell-/Dunkelmodus umschalten",
        "health_total": "Projekte insgesamt",
        "health_resolved": "Version aufgelöst",
        "health_errors": "Fehler / unbekannt",
        "health_registry": "Registry-Zustand",
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
        "footer_registry": "Registry-Quelle:",
        "footer_generator": "Dashboard-Generator:",
        "footer_workflow": "Workflow:",
        "footer_note": "Die Registry bleibt die einzige verlässliche Quelle für Projekt-/Versionsorte.",
        "version_status_ok": "OK",
        "version_status_error": "FEHLER",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "Benutzer-PC",
        "deploy_mobile": "Mobil",
        "deploy_wearable": "Wearable",
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
    },
    "zh": {
        "header_title": "生态系统状态仪表盘",
        "subtitle_main": "{ok}/{total} 个仓库成功解析 · {percent} 健康 · 版本号直接从各项目自身的源文件读取 · 仪表盘由 GitHub Actions 生成 · 静态 GitHub Pages",
        "subtitle_v3": "v3：新增真实的成熟度/角色分类、家族/父子关系树，以及更丰富的逐项目说明——具体每个等级是如何判定的，见下方的“成熟度”图例。",
        "theme_toggle": "切换深色/浅色主题",
        "health_total": "项目总数",
        "health_resolved": "已解析版本",
        "health_errors": "错误/未知",
        "health_registry": "注册表健康度",
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
        "footer_registry": "注册表来源：",
        "footer_generator": "仪表盘生成器：",
        "footer_workflow": "工作流：",
        "footer_note": "该注册表仍然是项目/版本位置的唯一真实来源。",
        "version_status_ok": "正常",
        "version_status_error": "错误",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "用户电脑",
        "deploy_mobile": "移动端",
        "deploy_wearable": "可穿戴设备",
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
    },
    "ja": {
        "header_title": "エコシステム ステータスダッシュボード",
        "subtitle_main": "{ok}/{total} 個のリポジトリが正常に解決 · {percent} が健全 · バージョンは各プロジェクト自身のソースファイルから読み取り · ダッシュボードは GitHub Actions によって生成 · 静的な GitHub Pages",
        "subtitle_v3": "v3：実際の成熟度/役割分類、ファミリー/親子ツリー、そしてより充実したプロジェクトごとの注記を追加しました——各レベルが具体的にどう判定されたかは、下部の成熟度の凡例を参照してください。",
        "theme_toggle": "ダーク/ライトテーマを切り替え",
        "health_total": "プロジェクト総数",
        "health_resolved": "バージョン解決済み",
        "health_errors": "エラー / 不明",
        "health_registry": "レジストリの健全性",
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
        "footer_registry": "レジストリの情報源：",
        "footer_generator": "ダッシュボード生成スクリプト：",
        "footer_workflow": "ワークフロー：",
        "footer_note": "レジストリは引き続き、プロジェクト/バージョンの所在に関する唯一の信頼できる情報源です。",
        "version_status_ok": "OK",
        "version_status_error": "エラー",
        "deploy_cm5": "CM5",
        "deploy_user-pc": "ユーザーPC",
        "deploy_mobile": "モバイル",
        "deploy_wearable": "ウェアラブル",
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
    },
}

# Architecture text is kept separate from the UI chrome above so that the
# public technical model stays equally available in every dashboard language.
ARCHITECTURE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "architecture_intro": "HYDRA-UMC is a modular engineering ecosystem for multi-axis control, robotics, industrial connectivity, machine vision and edge intelligence. It keeps Raspberry Pi OS and official vendor APIs as its base, then adds a versioned HYDRA-UMC platform layer, shared contracts and optional services. This dashboard explains the system while the registry and table remain the source of project-specific facts.",
        "architecture_section": "System architecture", "architecture_platform_title": "Platform foundation", "architecture_platform_body": "Raspberry Pi OS ARM64 remains the operating-system base. The HYDRA-UMC layer adds device profiles, diagnostics and service lifecycle.",
        "architecture_contracts_title": "Contracts and operations", "architecture_contracts_body": "The SDK defines stable data and command contracts; Server, UI and tools use those contracts instead of raw hardware protocols.",
        "architecture_perception_title": "Perception and intelligence", "architecture_perception_body": "Vision and AI are optional capabilities. Their output is validated before it can influence a mission; they are never safety authority.",
        "architecture_engineering_title": "Engineering and industry", "architecture_engineering_body": "Simulation, telemetry and standards make the physical cell observable, testable and interoperable.",
        "architecture_flow_operator": "Operator interfaces", "architecture_flow_services": "Server and SDK", "architecture_flow_adapter": "CM5-MCU adapter", "architecture_flow_machine": "MCU / URTC / machine",
        "architecture_relationship_title": "HYDRA-UMC and URTC:", "architecture_relationship_body": "HYDRA-UMC is the platform and cell controller. URTC is its universal robot-tool subsystem, with independent firmware and maintenance tools. The MCU remains authoritative for physical limits and safe stop; UI, network and AI cannot bypass that boundary.",
    },
    "es": {
        "architecture_intro": "HYDRA-UMC es un ecosistema modular de ingeniería para control multieje, robótica, conectividad industrial, visión artificial e inteligencia de borde. Mantiene Raspberry Pi OS y las API oficiales de cada proveedor como base, y añade una capa de plataforma HYDRA-UMC versionada, contratos compartidos y servicios opcionales. Este panel explica el sistema; el registro y la tabla conservan los hechos específicos de cada proyecto.",
        "architecture_section": "Arquitectura del sistema", "architecture_platform_title": "Base de plataforma", "architecture_platform_body": "Raspberry Pi OS ARM64 mantiene el papel de sistema operativo base. La capa HYDRA-UMC aporta perfiles de dispositivo, diagnóstico y ciclo de vida de servicios.",
        "architecture_contracts_title": "Contratos y operaciones", "architecture_contracts_body": "El SDK define contratos estables de datos y comandos; Server, las interfaces y las herramientas los usan en lugar de protocolos de hardware sin abstraer.",
        "architecture_perception_title": "Percepción e inteligencia", "architecture_perception_body": "La visión y la IA son capacidades opcionales. Su salida se valida antes de influir en una misión y nunca tiene autoridad de seguridad.",
        "architecture_engineering_title": "Ingeniería e industria", "architecture_engineering_body": "La simulación, la telemetría y los estándares hacen que la celda física sea observable, comprobable e interoperable.",
        "architecture_flow_operator": "Interfaces de operador", "architecture_flow_services": "Server y SDK", "architecture_flow_adapter": "Adaptador CM5-MCU", "architecture_flow_machine": "MCU / URTC / máquina",
        "architecture_relationship_title": "HYDRA-UMC y URTC:", "architecture_relationship_body": "HYDRA-UMC es la plataforma y el controlador de celda. URTC es su subsistema universal de herramientas robóticas, con firmware y utilidades de mantenimiento independientes. El MCU conserva la autoridad sobre límites físicos y parada segura; UI, red e IA no pueden saltarse esa frontera.",
    },
    "fr": {
        "architecture_intro": "HYDRA-UMC est un écosystème d’ingénierie modulaire pour le contrôle multi-axes, la robotique, la connectivité industrielle, la vision et l’intelligence de périphérie. Il conserve Raspberry Pi OS et les API officielles comme base, puis ajoute une couche de plateforme HYDRA-UMC versionnée, des contrats partagés et des services optionnels. Ce tableau explique le système ; le registre et le tableau restent la source des faits par projet.",
        "architecture_section": "Architecture du système", "architecture_platform_title": "Fondation de plateforme", "architecture_platform_body": "Raspberry Pi OS ARM64 reste la base du système d’exploitation. La couche HYDRA-UMC apporte profils d’appareil, diagnostic et cycle de vie des services.",
        "architecture_contracts_title": "Contrats et opérations", "architecture_contracts_body": "Le SDK définit des contrats stables de données et de commandes ; Server, les interfaces et les outils les utilisent au lieu de protocoles matériels bruts.",
        "architecture_perception_title": "Perception et intelligence", "architecture_perception_body": "La vision et l’IA sont des capacités optionnelles. Leur sortie est validée avant d’influencer une mission et n’a jamais autorité sur la sécurité.",
        "architecture_engineering_title": "Ingénierie et industrie", "architecture_engineering_body": "Simulation, télémétrie et standards rendent la cellule physique observable, testable et interopérable.",
        "architecture_flow_operator": "Interfaces opérateur", "architecture_flow_services": "Server et SDK", "architecture_flow_adapter": "Adaptateur CM5-MCU", "architecture_flow_machine": "MCU / URTC / machine",
        "architecture_relationship_title": "HYDRA-UMC et URTC :", "architecture_relationship_body": "HYDRA-UMC est la plateforme et le contrôleur de cellule. URTC est son sous-système universel d’outils robotiques, avec firmware et outils de maintenance indépendants. Le MCU garde l’autorité sur les limites physiques et l’arrêt sûr ; interface, réseau et IA ne peuvent pas contourner cette frontière.",
    },
    "it": {
        "architecture_intro": "HYDRA-UMC è un ecosistema ingegneristico modulare per controllo multiasse, robotica, connettività industriale, visione artificiale e intelligenza edge. Mantiene Raspberry Pi OS e le API ufficiali dei fornitori come base, quindi aggiunge una piattaforma HYDRA-UMC versionata, contratti condivisi e servizi opzionali. Questa dashboard spiega il sistema; registro e tabella restano la fonte dei fatti per progetto.",
        "architecture_section": "Architettura del sistema", "architecture_platform_title": "Fondazione della piattaforma", "architecture_platform_body": "Raspberry Pi OS ARM64 rimane la base del sistema operativo. Il livello HYDRA-UMC aggiunge profili dispositivo, diagnostica e ciclo di vita dei servizi.",
        "architecture_contracts_title": "Contratti e operazioni", "architecture_contracts_body": "L’SDK definisce contratti stabili per dati e comandi; Server, UI e strumenti li usano invece di protocolli hardware grezzi.",
        "architecture_perception_title": "Percezione e intelligenza", "architecture_perception_body": "Visione e IA sono capacità opzionali. Il loro output viene convalidato prima di influire su una missione e non ha mai autorità sulla sicurezza.",
        "architecture_engineering_title": "Ingegneria e industria", "architecture_engineering_body": "Simulazione, telemetria e standard rendono la cella fisica osservabile, verificabile e interoperabile.",
        "architecture_flow_operator": "Interfacce operatore", "architecture_flow_services": "Server e SDK", "architecture_flow_adapter": "Adattatore CM5-MCU", "architecture_flow_machine": "MCU / URTC / macchina",
        "architecture_relationship_title": "HYDRA-UMC e URTC:", "architecture_relationship_body": "HYDRA-UMC è la piattaforma e il controllore di cella. URTC è il suo sottosistema universale per utensili robotici, con firmware e strumenti di manutenzione indipendenti. Il MCU mantiene l’autorità sui limiti fisici e sull’arresto sicuro; UI, rete e IA non possono aggirare quel confine.",
    },
    "de": {
        "architecture_intro": "HYDRA-UMC ist ein modulares Engineering-Ökosystem für Mehrachsensteuerung, Robotik, industrielle Konnektivität, maschinelles Sehen und Edge-Intelligenz. Raspberry Pi OS und offizielle Hersteller-APIs bleiben die Basis; darüber liegen eine versionierte HYDRA-UMC-Plattformschicht, gemeinsame Verträge und optionale Dienste. Dieses Dashboard erklärt das System, während Registry und Tabelle projektbezogene Fakten liefern.",
        "architecture_section": "Systemarchitektur", "architecture_platform_title": "Plattformbasis", "architecture_platform_body": "Raspberry Pi OS ARM64 bleibt die Betriebssystembasis. Die HYDRA-UMC-Schicht ergänzt Geräteprofile, Diagnose und den Lebenszyklus der Dienste.",
        "architecture_contracts_title": "Verträge und Betrieb", "architecture_contracts_body": "Das SDK definiert stabile Daten- und Befehlsverträge; Server, Oberflächen und Werkzeuge verwenden sie statt roher Hardwareprotokolle.",
        "architecture_perception_title": "Wahrnehmung und Intelligenz", "architecture_perception_body": "Vision und KI sind optionale Fähigkeiten. Ihre Ausgabe wird validiert, bevor sie eine Mission beeinflussen kann; sie besitzen nie Sicherheitsautorität.",
        "architecture_engineering_title": "Engineering und Industrie", "architecture_engineering_body": "Simulation, Telemetrie und Standards machen die physische Zelle beobachtbar, testbar und interoperabel.",
        "architecture_flow_operator": "Bedienoberflächen", "architecture_flow_services": "Server und SDK", "architecture_flow_adapter": "CM5-MCU-Adapter", "architecture_flow_machine": "MCU / URTC / Maschine",
        "architecture_relationship_title": "HYDRA-UMC und URTC:", "architecture_relationship_body": "HYDRA-UMC ist Plattform und Zellensteuerung. URTC ist das universelle Roboterwerkzeug-Subsystem mit unabhängiger Firmware und Wartungswerkzeugen. Der MCU behält die Autorität über physische Grenzen und sicheren Stopp; UI, Netzwerk und KI können diese Grenze nicht umgehen.",
    },
    "zh": {
        "architecture_intro": "HYDRA-UMC 是面向多轴控制、机器人、工业连接、机器视觉和边缘智能的模块化工程生态系统。它以 Raspberry Pi OS 与厂商官方 API 为基础，并增加版本化的 HYDRA-UMC 平台层、共享契约和可选服务。本仪表板说明系统；注册表和项目表仍是各项目事实的来源。",
        "architecture_section": "系统架构", "architecture_platform_title": "平台基础", "architecture_platform_body": "Raspberry Pi OS ARM64 仍是操作系统基础。HYDRA-UMC 层增加设备配置文件、诊断和服务生命周期。",
        "architecture_contracts_title": "契约与运维", "architecture_contracts_body": "SDK 定义稳定的数据和命令契约；Server、界面和工具使用这些契约，而不是原始硬件协议。",
        "architecture_perception_title": "感知与智能", "architecture_perception_body": "视觉和 AI 是可选能力。其输出在影响任务前必须经过验证，且永远不拥有安全权限。",
        "architecture_engineering_title": "工程与工业", "architecture_engineering_body": "仿真、遥测和标准使物理单元可观测、可测试且可互操作。",
        "architecture_flow_operator": "操作员界面", "architecture_flow_services": "Server 和 SDK", "architecture_flow_adapter": "CM5-MCU 适配器", "architecture_flow_machine": "MCU / URTC / 机器",
        "architecture_relationship_title": "HYDRA-UMC 与 URTC：", "architecture_relationship_body": "HYDRA-UMC 是平台和单元控制器。URTC 是其通用机器人工具子系统，拥有独立的固件和维护工具。MCU 保留物理限制和安全停止的权力；UI、网络和 AI 都不能绕过这一边界。",
    },
    "ja": {
        "architecture_intro": "HYDRA-UMC は、多軸制御、ロボティクス、産業接続、マシンビジョン、エッジインテリジェンスのためのモジュール型エンジニアリングエコシステムです。Raspberry Pi OS と公式ベンダー API を基盤に、バージョン管理された HYDRA-UMC プラットフォーム層、共有契約、任意のサービスを追加します。このダッシュボードはシステムを説明し、レジストリと表が各プロジェクトの事実の情報源です。",
        "architecture_section": "システムアーキテクチャ", "architecture_platform_title": "プラットフォーム基盤", "architecture_platform_body": "Raspberry Pi OS ARM64 は OS の基盤として残ります。HYDRA-UMC 層はデバイスプロファイル、診断、サービスライフサイクルを追加します。",
        "architecture_contracts_title": "契約と運用", "architecture_contracts_body": "SDK は安定したデータおよびコマンド契約を定義し、Server、UI、ツールは生のハードウェアプロトコルの代わりにそれを使用します。",
        "architecture_perception_title": "知覚とインテリジェンス", "architecture_perception_body": "Vision と AI は任意の能力です。出力はミッションに影響する前に検証され、安全権限を持つことはありません。",
        "architecture_engineering_title": "エンジニアリングと産業", "architecture_engineering_body": "シミュレーション、テレメトリ、標準により、物理セルは観測可能、テスト可能、相互運用可能になります。",
        "architecture_flow_operator": "オペレーターインターフェース", "architecture_flow_services": "Server と SDK", "architecture_flow_adapter": "CM5-MCU アダプター", "architecture_flow_machine": "MCU / URTC / 機械",
        "architecture_relationship_title": "HYDRA-UMC と URTC：", "architecture_relationship_body": "HYDRA-UMC はプラットフォームおよびセルコントローラーです。URTC は独立したファームウェアと保守ツールを持つ汎用ロボットツールサブシステムです。MCU は物理的な制限と安全停止の権限を維持し、UI、ネットワーク、AI はその境界を迂回できません。",
    },
}

for language, values in ARCHITECTURE_TRANSLATIONS.items():
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
            <span class="role-badge role-{esc(entry.role)}">
              {role_icon}<span data-i18n="role_{esc(entry.role)}">{role_label}</span>
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
            <span class="deploy-badge">
              {deploy_icon}<span data-i18n="deploy_{deploy_filter}">{deploy}</span>
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
            data-role="{esc(entry.role)}"
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
            <tr class="family-header-row" data-family-header="{family_id}">
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
  content="HYDRA-UMC / URTC ecosystem status dashboard - maturity, role, family/parent tree, stack and version for all 46 projects"
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
        HYDRA-UMC / URTC ECOSYSTEM
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

    <p
        class="subtitle"
        data-i18n-template="subtitle_main"
        data-ok="{ok}"
        data-total="{total}"
        data-percent="{success_percent_text}"
    >
      {ok}/{total} repositories resolved successfully
      · {success_percent_text} healthy
      · versions are read from each project's own source file
      · dashboard generated by GitHub Actions
      · static GitHub Pages
    </p>

    <p class="subtitle subtitle-v3" data-i18n="subtitle_v3">
      v3: real maturity/role classification, family/parent trees and richer
      per-project notes - see the Maturity legend below for exactly how
      each level was decided.
    </p>

    <p class="ecosystem-intro" data-i18n="architecture_intro">
      HYDRA-UMC is a modular engineering ecosystem for multi-axis control,
      robotics, industrial connectivity, machine vision and edge intelligence.
      It keeps Raspberry Pi OS and official vendor APIs as its base, then adds
      a versioned HYDRA-UMC platform layer, shared contracts and optional
      services. This dashboard explains the system while the registry and table
      remain the source of project-specific facts.
    </p>
  </header>


  <!-- ================================================================
       SYSTEM ARCHITECTURE
       ================================================================ -->

  <section class="section">

    <div class="section-title" data-i18n="architecture_section">System architecture</div>

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
       HEALTH
       ================================================================ -->

  <section class="health">

    <div class="health-card">
      <div class="number">
        {total}
      </div>
      <div class="label" data-i18n="health_total">
        Total projects
      </div>
    </div>

    <div class="health-card ok">
      <div class="number">
        {ok}
      </div>
      <div class="label" data-i18n="health_resolved">
        Version resolved
      </div>
    </div>

    <div class="health-card error">
      <div class="number">
        {errors}
      </div>
      <div class="label" data-i18n="health_errors">
        Errors / unknown
      </div>
    </div>

    <div class="health-card">
      <div class="number">
        {success_percent_text}
      </div>
      <div class="label" data-i18n="health_registry">
        Registry health
      </div>
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

    <span data-i18n="footer_registry">Registry source:</span>
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

    <span data-i18n="footer_note">The registry remains the single source of truth for project/version
    locations.</span>

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
