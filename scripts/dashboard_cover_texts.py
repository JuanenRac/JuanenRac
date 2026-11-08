#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_cover_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the coverage card, the notice of new / archived / disappeared repositories, the Tools group and the performance and lint additions of the status
dashboard, in the eight languages (portuguese is the one of Portugal).

Each entry is (en, es, de, fr, it, ja, zh, pt). generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    # ---- Coverage: owner / shown / without manifest ----
    "eco_unclassified": ("Unclassified", "Sin clasificar", "Nicht zugeordnet", "Non classés", "Non classificati", "未分類", "未分类", "Sem classificação"),
    "cover_counter": (
        "owner {owner} · shown {shown} · no manifest {without}",
        "propietario {owner} · mostrados {shown} · sin manifiesto {without}",
        "Inhaber {owner} · angezeigt {shown} · ohne Manifest {without}",
        "propriétaire {owner} · affichés {shown} · sans manifeste {without}",
        "proprietario {owner} · mostrati {shown} · senza manifesto {without}",
        "所有者 {owner} · 表示 {shown} · マニフェストなし {without}",
        "所有者 {owner} · 已显示 {shown} · 无清单 {without}",
        "proprietário {owner} · mostrados {shown} · sem manifesto {without}",
    ),
    "cover_title": (
        "Public repositories of the owner that no ecosystem lists (they have no manifest): {names}",
        "Repositorios públicos del propietario que ningún ecosistema lista (no tienen manifiesto): {names}",
        "Öffentliche Repositories des Inhabers, die kein Ökosystem listet (sie haben kein Manifest): {names}",
        "Dépôts publics du propriétaire qu'aucun écosystème ne liste (ils n'ont pas de manifeste) : {names}",
        "Repository pubblici del proprietario che nessun ecosistema elenca (non hanno un manifesto): {names}",
        "どのエコシステムにも掲載されていない所有者の公開リポジトリ(マニフェストなし):{names}",
        "所有者的公开仓库中未被任何生态系统列出的仓库(没有清单):{names}",
        "Repositórios públicos do proprietário que nenhum ecossistema lista (não têm manifesto): {names}",
    ),
    "cover_unknown": ("not verified", "no verificado", "nicht geprüft", "non vérifié", "non verificato", "未確認", "未验证", "não verificado"),
    "cover_unknown_title": (
        "The list of repositories of the owner could not be read in this run, so the count is not known.",
        "No se pudo leer la lista de repositorios del propietario en esta ejecución, así que no se conoce la cuenta.",
        "Die Liste der Repositories des Inhabers konnte in diesem Lauf nicht gelesen werden, die Anzahl ist daher unbekannt.",
        "La liste des dépôts du propriétaire n'a pas pu être lue lors de cette exécution : le nombre est donc inconnu.",
        "Non è stato possibile leggere l'elenco dei repository del proprietario in questa esecuzione, quindi il conteggio non è noto.",
        "今回の実行では所有者のリポジトリ一覧を読み取れなかったため、件数は不明です。",
        "本次运行未能读取所有者的仓库列表,因此数量未知。",
        "Não foi possível ler a lista de repositórios do proprietário nesta execução, por isso a contagem é desconhecida.",
    ),
    # ---- New / archived / disappeared repositories ----
    "changes_title": ("Changes in the account since the last run", "Cambios en la cuenta desde la última ejecución", "Änderungen am Konto seit dem letzten Lauf", "Changements du compte depuis la dernière exécution", "Modifiche all'account dall'ultima esecuzione", "前回の実行からのアカウントの変更", "自上次运行以来账户的变化", "Alterações na conta desde a última execução"),
    "changes_new": (
        "New repositories ({n}): {names}",
        "Repositorios nuevos ({n}): {names}",
        "Neue Repositories ({n}): {names}",
        "Nouveaux dépôts ({n}) : {names}",
        "Nuovi repository ({n}): {names}",
        "新しいリポジトリ({n}件):{names}",
        "新仓库({n} 个):{names}",
        "Repositórios novos ({n}): {names}",
    ),
    "changes_archived": (
        "Archived repositories ({n}): {names}",
        "Repositorios archivados ({n}): {names}",
        "Archivierte Repositories ({n}): {names}",
        "Dépôts archivés ({n}) : {names}",
        "Repository archiviati ({n}): {names}",
        "アーカイブされたリポジトリ({n}件):{names}",
        "已归档的仓库({n} 个):{names}",
        "Repositórios arquivados ({n}): {names}",
    ),
    "changes_gone": (
        "Repositories that disappeared ({n}): {names}",
        "Repositorios desaparecidos ({n}): {names}",
        "Verschwundene Repositories ({n}): {names}",
        "Dépôts disparus ({n}) : {names}",
        "Repository scomparsi ({n}): {names}",
        "なくなったリポジトリ({n}件):{names}",
        "已消失的仓库({n} 个):{names}",
        "Repositórios desaparecidos ({n}): {names}",
    ),
}

TEXTS: dict[str, dict[str, str]] = {
    code: {key: row[index] for key, row in _ROWS.items()} for index, code in enumerate(LANGUAGES)
}


def problems() -> list[str]:
    """Rows with a missing language, an empty text or placeholders that differ from the English one (used by the tests)."""
    out = []
    for key, row in _ROWS.items():
        if len(row) != len(LANGUAGES):
            out.append(f"{key}: {len(row)} languages")
            continue
        if any(not text.strip() for text in row):
            out.append(f"{key}: empty text")
            continue
        wanted = sorted(part for part in row[0].replace("}", "{").split("{")[1::2])
        for code, text in zip(LANGUAGES, row):
            if sorted(part for part in text.replace("}", "{").split("{")[1::2]) != wanted:
                out.append(f"{key}: placeholders of {code} differ from en")
    return out
