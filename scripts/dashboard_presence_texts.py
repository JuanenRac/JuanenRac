#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_presence_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the presence of signatures and build attestations (Sentinel tab and panel of a repository) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "pr_title": ("Signature and attestation of the latest release", "Firma y atestación de la última versión", "Signatur und Attestierung der letzten Version",
                 "Signature et attestation de la dernière version", "Firma e attestazione dell'ultima versione", "最新リリースの署名とアテステーション",
                 "最新版本的签名与构建证明", "Assinatura e atestação da última versão"),
    "pr_hint": ("Presence only: whether each release file has a signature file next to it and whether GitHub holds a build attestation for its digest. No key and no proof is verified here.",
                "Solo presencia: si cada archivo de la versión tiene un archivo de firma al lado y si GitHub guarda una atestación de compilación para su huella. Aquí no se verifica ninguna clave ni prueba.",
                "Nur Vorhandensein: ob zu jeder Release-Datei eine Signaturdatei gehört und ob GitHub eine Build-Attestierung für ihren Digest hält. Schlüssel und Nachweis werden hier nicht geprüft.",
                "Présence seulement : chaque fichier de la version a-t-il un fichier de signature à côté et GitHub détient-il une attestation de build pour son empreinte. Aucune clé ni preuve n'est vérifiée ici.",
                "Solo presenza: se ogni file della versione ha accanto un file di firma e se GitHub conserva un'attestazione di build per il suo digest. Qui non si verifica nessuna chiave né prova.",
                "存在のみを示します。各リリースファイルの隣に署名ファイルがあるか、そのダイジェストに対するビルドのアテステーションを GitHub が保持しているか。鍵や証明の検証はここでは行いません。",
                "仅表示是否存在:每个发布文件旁是否有签名文件,GitHub 是否保存有其摘要对应的构建证明。此处不验证任何密钥或证明。",
                "Apenas presença: se cada ficheiro da versão tem ao lado um ficheiro de assinatura e se o GitHub guarda uma atestação de compilação para o seu digest. Aqui não se verifica nenhuma chave nem prova."),
    "pr_unknown_note": ("Unknown means it could not be read (no release data, no digest, a refused token or the request budget used up); it is never shown as absent.",
                        "Desconocida significa que no se pudo leer (sin datos de la versión, sin huella, un token rechazado o el presupuesto de peticiones agotado); nunca se muestra como ausente.",
                        "Unbekannt heißt: nicht lesbar (keine Release-Daten, kein Digest, abgelehntes Token oder aufgebrauchtes Anfragebudget); es wird nie als fehlend gezeigt.",
                        "Inconnue signifie que la lecture a échoué (pas de données de version, pas d'empreinte, jeton refusé ou budget de requêtes épuisé) ; elle n'est jamais affichée comme absente.",
                        "Sconosciuta significa che non si è potuto leggere (nessun dato della versione, nessun digest, token rifiutato o budget di richieste esaurito); non è mai mostrata come assente.",
                        "「不明」は読み取れなかったことを示します(リリース情報なし、ダイジェストなし、トークン拒否、リクエスト予算の超過)。「なし」とは表示されません。",
                        "“未知”表示无法读取(无版本数据、无摘要、令牌被拒绝或请求预算用尽);绝不会显示为“无”。",
                        "Desconhecida significa que não foi possível ler (sem dados da versão, sem digest, token recusado ou orçamento de pedidos esgotado); nunca é mostrada como ausente."),
    "pr_col_files": ("Release files", "Archivos de la versión", "Release-Dateien", "Fichiers de la version", "File della versione", "リリースファイル", "发布文件", "Ficheiros da versão"),
    "pr_col_sig": ("Signature", "Firma", "Signatur", "Signature", "Firma", "署名", "签名", "Assinatura"),
    "pr_col_att": ("Attestation", "Atestación", "Attestierung", "Attestation", "Attestazione", "アテステーション", "构建证明", "Atestação"),
    "pr_s_present": ("Present", "Presente", "Vorhanden", "Présente", "Presente", "あり", "有", "Presente"),
    "pr_s_partial": ("Partial", "Parcial", "Teilweise", "Partielle", "Parziale", "一部", "部分", "Parcial"),
    "pr_s_absent": ("Absent", "Ausente", "Fehlt", "Absente", "Assente", "なし", "无", "Ausente"),
    "pr_s_na": ("Not applicable", "No aplica", "Nicht zutreffend", "Sans objet", "Non applicabile", "対象外", "不适用", "Não aplicável"),
    "pr_s_unknown": ("Unknown", "Desconocida", "Unbekannt", "Inconnue", "Sconosciuta", "不明", "未知", "Desconhecida"),
    "pr_sig_detail": ("{k} of {n} files have a signature file", "{k} de {n} archivos tienen archivo de firma", "{k} von {n} Dateien haben eine Signaturdatei",
                      "{k} fichiers sur {n} ont un fichier de signature", "{k} file su {n} hanno un file di firma", "{n} 個中 {k} 個のファイルに署名ファイルがあります",
                      "{n} 个文件中有 {k} 个带签名文件", "{k} de {n} ficheiros têm ficheiro de assinatura"),
    "pr_att_detail": ("{ak} of {an} checked files have an attestation", "{ak} de {an} archivos comprobados tienen atestación", "{ak} von {an} geprüften Dateien haben eine Attestierung",
                      "{ak} fichiers vérifiés sur {an} ont une attestation", "{ak} file controllati su {an} hanno un'attestazione", "確認した {an} 個中 {ak} 個にアテステーションがあります",
                      "已检查的 {an} 个文件中有 {ak} 个有构建证明", "{ak} de {an} ficheiros verificados têm atestação"),
    "pr_none": ("No repository has release files yet.", "Ningún repositorio tiene archivos de versión todavía.", "Noch kein Repository hat Release-Dateien.",
                "Aucun dépôt n'a encore de fichiers de version.", "Nessun repository ha ancora file di versione.", "リリースファイルを持つリポジトリはまだありません。",
                "还没有仓库带有发布文件。", "Nenhum repositório tem ainda ficheiros de versão."),
    "pr_repo_title": ("By repository", "Por repositorio", "Nach Repository", "Par dépôt", "Per repository", "リポジトリ別", "按仓库", "Por repositório"),
    "pf_prs_sig": ("Signature files", "Archivos de firma", "Signaturdateien", "Fichiers de signature", "File di firma", "署名ファイル", "签名文件", "Ficheiros de assinatura"),
    "pf_prs_att": ("Build attestation", "Atestación de compilación", "Build-Attestierung", "Attestation de build", "Attestazione di build", "ビルドのアテステーション", "构建证明", "Atestação de compilação"),
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
