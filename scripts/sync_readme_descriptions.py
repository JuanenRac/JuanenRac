#!/usr/bin/env python3
# =============================================================================
# Electro Hobby 3D - scripts/sync_readme_descriptions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Fills in (and keeps current) the "Description" column of every project-catalog
# table in the eight README files from ONE source, ecosystem-descriptions.json:
# one entry per repository with its description in the eight languages. The
# Version column is filled the same way from each repository's own manifest by
# scripts/sync_readme_versions.py, so neither column is ever typed by hand in a
# README.
#
# --check fails (exit 1) when
#   - a description in a README differs from its source,
#   - a repository listed in a table has no entry (or lacks a language) in the
#     source - a new repository cannot be added to the catalogue without its
#     description,
#   - the source holds an entry no table lists any more, or an entry that is
#     malformed (empty, with a pipe, or an English text over 140 characters),
#   - the "Catalogue and versions" row of the status table is out of date.
#
# Repositories whose name starts with a prefix listed in "exempt_prefixes" of the
# source keep their own hand-written descriptions: their owner adopts the same
# file by adding their entries and removing the prefix.
#
# Usage:  python scripts/sync_readme_descriptions.py            # writes every README
#         python scripts/sync_readme_descriptions.py --check    # exit 1 if any is stale
# =============================================================================
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_readme_versions as versions  # noqa: E402  (same table reading as the Version column)

ROOT = versions.ROOT
SOURCE = ROOT / "ecosystem-descriptions.json"
LANG_OF = {
    "README.md": "en", "README_spa.md": "es", "README_deu.md": "de", "README_fra.md": "fr",
    "README_ita.md": "it", "README_jpn.md": "ja", "README_zho.md": "zh", "README_por.md": "pt",
}
LANGUAGES = tuple(LANG_OF.values())
MAX_ENGLISH = 140

# The "Catalogue and versions" row of the status table at the top of each README.
STATUS_ROW = {
    "README.md": "| Catalogue and versions | 🟢 | The Version and the Description of every project table are filled by scripts from each repository's own manifest and from one checked descriptions file, and the CI fails if either drifts. |",
    "README_spa.md": "| Catálogo y versiones | 🟢 | La Versión y la Descripción de cada tabla de proyectos se rellenan con scripts a partir del manifiesto de cada repositorio y de un único fichero de descripciones comprobado, y la CI falla si alguna se desvía. |",
    "README_deu.md": "| Katalog und Versionen | 🟢 | Version und Beschreibung jeder Projekttabelle werden von Skripten aus dem Manifest des jeweiligen Repositorys und aus einer einzigen geprüften Beschreibungsdatei gefüllt, und das CI schlägt fehl, wenn eines davon abweicht. |",
    "README_fra.md": "| Catalogue et versions | 🟢 | La Version et la Description de chaque tableau de projets sont remplies par des scripts à partir du manifeste de chaque dépôt et d'un unique fichier de descriptions vérifié, et le CI échoue si l'une d'elles dérive. |",
    "README_ita.md": "| Catalogo e versioni | 🟢 | La Versione e la Descrizione di ogni tabella di progetti sono compilate da script a partire dal manifesto di ciascun repository e da un unico file di descrizioni verificato, e la CI fallisce se una delle due si discosta. |",
    "README_jpn.md": "| カタログとバージョン | 🟢 | 各プロジェクト表のバージョンと説明は、スクリプトが各リポジトリ自身のマニフェストと、検査される 1 つの説明ファイルから埋めます。どちらかがずれると CI が失敗します。 |",
    "README_zho.md": "| 目录与版本 | 🟢 | 每张项目表的版本和说明都由脚本分别根据各仓库自己的清单和一个经过检查的说明文件填写；任何一项出现偏差，CI 就会失败。 |",
    "README_por.md": "| Catálogo e versões | 🟢 | A Versão e a Descrição de cada tabela de projetos são preenchidas por scripts a partir do manifesto de cada repositório e de um único ficheiro de descrições verificado, e o CI falha se alguma se desviar. |",
}


def load_source() -> tuple[dict[str, dict[str, str]], tuple[str, ...]]:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    return data["descriptions"], tuple(data.get("exempt_prefixes", ()))


def validate(descriptions: dict[str, dict[str, str]]) -> list[str]:
    problems: list[str] = []
    for name, texts in descriptions.items():
        for lang in LANGUAGES:
            text = texts.get(lang)
            if not isinstance(text, str) or not text.strip():
                problems.append(f"{name}: missing '{lang}' description")
            elif "|" in text or "\n" in text:
                problems.append(f"{name}: '{lang}' description contains a pipe or a line break")
        english = texts.get("en", "")
        if len(english) > MAX_ENGLISH:
            problems.append(f"{name}: English description is {len(english)} characters (maximum {MAX_ENGLISH})")
    return problems


def process(lines: list[str], lang: str, descriptions: dict[str, dict[str, str]],
            exempt: tuple[str, ...], seen: set[str]) -> tuple[list[str], int, list[str]]:
    out: list[str] = []
    changed = 0
    problems: list[str] = []
    for line in lines:
        cells = versions.split_row(line)
        match = versions.REPO_LINK.match(cells[0]) if cells else None
        if not match or len(cells) != 3:
            out.append(line)
            continue
        name = match.group(2)
        if name.startswith(exempt):
            out.append(line)
            continue
        seen.add(name)
        text = descriptions.get(name, {}).get(lang)
        if not text:
            problems.append(f"{name}: no '{lang}' description in {SOURCE.name}")
            out.append(line)
            continue
        new_line = f"| {cells[0]} | {cells[1]} | {text} |" if line.startswith("| ") else f"|{cells[0]}|{cells[1]}|{text}|"
        if new_line != line:
            changed += 1
        out.append(new_line)
    return out, changed, problems


def set_status_row(lines: list[str], filename: str) -> int:
    label = "| " + STATUS_ROW[filename].split("|")[1].strip() + " |"
    for index, line in enumerate(lines[:60]):
        if line.startswith(label):
            if line == STATUS_ROW[filename]:
                return 0
            lines[index] = STATUS_ROW[filename]
            return 1
    raise SystemExit(f"{filename}: the status row '{label}' was not found")


def main() -> int:
    check = "--check" in sys.argv
    descriptions, exempt = load_source()
    problems = validate(descriptions)
    stale: list[str] = []
    seen: set[str] = set()
    written = 0
    for filename, lang in LANG_OF.items():
        path = ROOT / filename
        raw = path.read_bytes()
        crlf = b"\r\n" in raw
        lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
        seen_here: set[str] = set()
        new_lines, changed, missing = process(lines, lang, descriptions, exempt, seen_here)
        seen |= seen_here
        problems.extend(missing)
        changed += set_status_row(new_lines, filename)
        if changed:
            stale.append(f"{filename} ({changed} row(s))")
            if not check:
                new_text = "\n".join(new_lines)
                path.write_bytes((new_text.replace("\n", "\r\n") if crlf else new_text).encode("utf-8"))
                written += changed
    for name in sorted(set(descriptions) - seen):
        problems.append(f"{name}: in {SOURCE.name} but listed in no catalogue table")
    problems = sorted(set(problems))
    if check:
        if stale or problems:
            if stale:
                print("SYNC_README_DESCRIPTIONS=STALE " + ", ".join(stale))
            for problem in problems:
                print("  " + problem)
            return 1
        print("SYNC_README_DESCRIPTIONS=CURRENT")
        return 0
    for problem in problems:
        print("  " + problem)
    print(f"SYNC_README_DESCRIPTIONS=DONE rows_updated={written}" + (f" problems={len(problems)}" if problems else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
