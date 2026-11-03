#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_t86_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Texts of the delivery pipeline, signatures, legends and navigation parts of the status dashboard in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt) (portuguese is the one of Portugal). generate_dashboard.py merges TEXTS into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "tabs_scroll_prev": ("Show the previous sections", "Mostrar las secciones anteriores", "Vorherige Bereiche anzeigen", "Afficher les sections précédentes", "Mostra le sezioni precedenti", "前のセクションを表示", "显示前面的栏目", "Mostrar as secções anteriores"),
    "tabs_scroll_next": ("Show the next sections", "Mostrar las secciones siguientes", "Nächste Bereiche anzeigen", "Afficher les sections suivantes", "Mostra le sezioni successive", "次のセクションを表示", "显示后面的栏目", "Mostrar as secções seguintes"),
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
