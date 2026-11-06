#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_pins_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the dependency pins card (Sentinel tab) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "pn_title": ("Shared contract pins", "Versiones fijadas de los contratos compartidos", "Gepinnte Versionen der gemeinsamen Verträge",
                 "Versions épinglées des contrats partagés", "Versioni fissate dei contratti condivisi", "共有コントラクトの固定バージョン",
                 "共享契约的固定版本", "Versões fixadas dos contratos partilhados"),
    "pn_hint": ("The version of the shared contracts each repository was last checked against, read from the files the repositories publish, compared with the current version of the contracts. A count of what is written there, not a test of compatibility.",
                "La versión de los contratos compartidos con la que se comprobó por última vez cada repositorio, leída de los archivos que publican los repositorios y comparada con la versión actual de los contratos. Es lo que está escrito allí, no una prueba de compatibilidad.",
                "Die Version der gemeinsamen Verträge, gegen die jedes Repository zuletzt geprüft wurde, gelesen aus den Dateien, die die Repositorys veröffentlichen, im Vergleich zur aktuellen Version der Verträge. Gezeigt wird, was dort steht, kein Kompatibilitätstest.",
                "La version des contrats partagés avec laquelle chaque dépôt a été vérifié en dernier, lue dans les fichiers que publient les dépôts et comparée à la version actuelle des contrats. C'est ce qui y est écrit, pas un test de compatibilité.",
                "La versione dei contratti condivisi con cui ogni repository è stato controllato l'ultima volta, letta dai file che i repository pubblicano e confrontata con la versione attuale dei contratti. È ciò che vi è scritto, non una prova di compatibilità.",
                "各リポジトリが最後に確認された共有コントラクトのバージョンを、リポジトリが公開するファイルから読み取り、現在のコントラクトのバージョンと比較します。記載内容を示すだけで、互換性のテストではありません。",
                "每个仓库最近一次核对所针对的共享契约版本,取自各仓库公开的文件,并与契约的当前版本比较。显示的是文件中所写内容,而非兼容性测试。",
                "A versão dos contratos partilhados com que cada repositório foi verificado pela última vez, lida dos ficheiros que os repositórios publicam e comparada com a versão atual dos contratos. É o que lá está escrito, não um teste de compatibilidade."),
    "pn_current": ("Current contracts version: {v}", "Versión actual de los contratos: {v}", "Aktuelle Version der Verträge: {v}",
                   "Version actuelle des contrats : {v}", "Versione attuale dei contratti: {v}", "現在のコントラクトのバージョン: {v}",
                   "契约当前版本:{v}", "Versão atual dos contratos: {v}"),
    "pn_col_pin": ("Pinned version", "Versión fijada", "Gepinnte Version", "Version épinglée", "Versione fissata", "固定バージョン", "固定版本", "Versão fixada"),
    "pn_col_state": ("Against the current", "Frente a la actual", "Gegenüber der aktuellen", "Par rapport à l'actuelle", "Rispetto all'attuale", "現在との比較", "与当前版本比较", "Face à atual"),
    "pn_s_current": ("Current", "Al día", "Aktuell", "À jour", "Aggiornata", "最新", "最新", "Atual"),
    "pn_s_behind": ("Behind", "Atrasada", "Veraltet", "En retard", "Indietro", "古い", "落后", "Atrasada"),
    "pn_s_ahead": ("Ahead", "Adelantada", "Voraus", "En avance", "Avanti", "先行", "超前", "Adiantada"),
    "pn_s_unknown": ("Unknown", "Desconocida", "Unbekannt", "Inconnue", "Sconosciuta", "不明", "未知", "Desconhecida"),
    "pn_no_source": ("No pins published in a machine readable file.", "No publica versiones fijadas en un archivo legible por máquina.",
                     "Keine gepinnten Versionen in einer maschinenlesbaren Datei veröffentlicht.", "Aucune version épinglée publiée dans un fichier lisible par machine.",
                     "Nessuna versione fissata pubblicata in un file leggibile da macchina.", "機械可読なファイルで固定バージョンは公開されていません。",
                     "未在机器可读文件中公开固定版本。", "Não publica versões fixadas num ficheiro legível por máquina."),
    "pn_partial": ("Some repositories could not be read; they are left out, not counted as current.", "Algunos repositorios no se pudieron leer; se omiten y no se cuentan como al día.",
                   "Einige Repositorys waren nicht lesbar; sie fehlen und zählen nicht als aktuell.", "Certains dépôts n'ont pas pu être lus ; ils sont omis et non comptés comme à jour.",
                   "Alcuni repository non si sono potuti leggere; sono omessi e non contati come aggiornati.", "読み取れなかったリポジトリは除外され、最新としては数えません。",
                   "部分仓库无法读取;它们被省略,不计为最新。", "Alguns repositórios não puderam ser lidos; ficam de fora e não contam como atuais."),
    "pn_none": ("No pins could be read.", "No se pudo leer ninguna versión fijada.", "Es konnten keine gepinnten Versionen gelesen werden.",
                "Aucune version épinglée n'a pu être lue.", "Non è stato possibile leggere nessuna versione fissata.", "固定バージョンを読み取れませんでした。",
                "无法读取任何固定版本。", "Não foi possível ler nenhuma versão fixada."),
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
