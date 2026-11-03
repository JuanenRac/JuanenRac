#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_ci_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the view "declared against verified" (technical evidence published by the CI), in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "cie_title": ("Declared against verified", "Declarado frente a verificado", "Erklärt gegenüber geprüft", "Déclaré face à vérifié", "Dichiarato e verificato", "宣言と検証の比較", "声明与验证对照", "Declarado face a verificado"),
    "cie_hint": (
        "The manifest of each repository declares how far it has been proven. Here that claim is compared with the records its own CI publishes: a passing run on the main branch, not older than the limit of its kind, proves its level. Nothing published means not verified.",
        "El manifiesto de cada repositorio declara hasta dónde está demostrado. Aquí esa afirmación se compara con los registros que publica su propio CI: una ejecución correcta en la rama principal, no más antigua que el límite de su tipo, demuestra su nivel. Si no publica nada, no está verificado.",
        "Das Manifest jedes Repositorys erklärt, wie weit es belegt ist. Hier wird diese Angabe mit den Einträgen verglichen, die sein eigenes CI veröffentlicht: ein erfolgreicher Lauf auf dem Hauptzweig, nicht älter als die Grenze seiner Art, belegt die Stufe. Ohne Veröffentlichung gilt es als nicht geprüft.",
        "Le manifeste de chaque dépôt déclare jusqu'où il est prouvé. Ici, cette déclaration est comparée aux enregistrements que publie son propre CI : une exécution réussie sur la branche principale, pas plus ancienne que la limite de son type, prouve son niveau. Rien de publié signifie non vérifié.",
        "Il manifesto di ogni repository dichiara fin dove è dimostrato. Qui questa dichiarazione viene confrontata con i record pubblicati dalla sua CI: un'esecuzione riuscita sul ramo principale, non più vecchia del limite del suo tipo, dimostra il livello. Se non pubblica nulla, non è verificato.",
        "各リポジトリのマニフェストは、どこまで実証されたかを宣言します。ここでは、その宣言を各 CI が公開する記録と比較します。メインブランチでの成功した実行が、種類ごとの期限内であれば、そのレベルを裏付けます。何も公開されていなければ未確認です。",
        "每个仓库的清单声明其已证明到什么程度。这里将该声明与其自身 CI 发布的记录对比：主分支上的一次成功运行，且未超过该类型的期限，即可证明相应级别。未发布任何内容则为未验证。",
        "O manifesto de cada repositório declara até onde está demonstrado. Aqui essa declaração é comparada com os registos que o próprio CI publica: uma execução bem-sucedida no ramo principal, não mais antiga do que o limite do seu tipo, demonstra o nível. Se não publicar nada, não está verificado.",
    ),
    "cie_source": (
        "Records are read from the branch and file {source}. Limits in days: host test {host}, simulator {sim}, bench {bench}, field {field}.",
        "Los registros se leen de la rama y el archivo {source}. Límites en días: prueba en equipo {host}, simulador {sim}, banco {bench}, campo {field}.",
        "Die Einträge werden aus Zweig und Datei {source} gelesen. Grenzen in Tagen: Host-Test {host}, Simulator {sim}, Prüfstand {bench}, Feld {field}.",
        "Les enregistrements sont lus depuis la branche et le fichier {source}. Limites en jours : test hôte {host}, simulateur {sim}, banc {bench}, terrain {field}.",
        "I record vengono letti dal ramo e dal file {source}. Limiti in giorni: test su host {host}, simulatore {sim}, banco {bench}, campo {field}.",
        "記録はブランチとファイル {source} から読み取ります。期限（日数）：ホストテスト {host}、シミュレーター {sim}、ベンチ {bench}、フィールド {field}。",
        "记录从分支和文件 {source} 读取。期限（天）：主机测试 {host}、模拟器 {sim}、台架 {bench}、现场 {field}。",
        "Os registos são lidos do ramo e do ficheiro {source}. Limites em dias: teste no anfitrião {host}, simulador {sim}, bancada {bench}, terreno {field}.",
    ),
    "cie_not_read": (
        "No evidence was read in this build, so nothing is verified.",
        "En esta compilación no se leyó ninguna evidencia, así que nada está verificado.",
        "In diesem Build wurden keine Nachweise gelesen, daher ist nichts geprüft.",
        "Aucune preuve n'a été lue dans cette compilation : rien n'est vérifié.",
        "In questa build non è stata letta alcuna evidenza, quindi nulla è verificato.",
        "このビルドではエビデンスを読み取れなかったため、何も確認されていません。",
        "本次构建未读取任何证据，因此没有任何内容被验证。",
        "Nesta compilação não foi lida nenhuma evidência, por isso nada está verificado.",
    ),
    "cie_filter_title": ("State", "Estado", "Status", "État", "Stato", "状態", "状态", "Estado"),
    "cie_filter_all": ("All", "Todos", "Alle", "Tous", "Tutti", "すべて", "全部", "Todos"),
    "cie_st_verified": ("Verified", "Verificado", "Geprüft", "Vérifié", "Verificato", "確認済み", "已验证", "Verificado"),
    "cie_st_below": ("Declares more than it proves", "Declara más de lo que demuestra", "Erklärt mehr als belegt", "Déclare plus qu'il ne prouve", "Dichiara più di quanto dimostra", "実証以上を宣言", "声明超出已证明", "Declara mais do que demonstra"),
    "cie_st_failing": ("Failing", "Fallando", "Fehlschlag", "En échec", "In errore", "失敗中", "失败", "A falhar"),
    "cie_st_expired": ("Expired", "Caducado", "Abgelaufen", "Expiré", "Scaduto", "期限切れ", "已过期", "Caducado"),
    "cie_st_nodata": ("Not verified", "No verificado", "Nicht geprüft", "Non vérifié", "Non verificato", "未確認", "未验证", "Não verificado"),
    "cie_st_invalid": ("Invalid records", "Registros no válidos", "Ungültige Einträge", "Enregistrements non valides", "Record non validi", "無効な記録", "记录无效", "Registos inválidos"),
    "cie_st_unread": ("Could not be read", "No se pudo leer", "Nicht lesbar", "Lecture impossible", "Non leggibile", "読み取れません", "无法读取", "Não foi possível ler"),
    "cie_col_repo": ("Repository", "Repositorio", "Repository", "Dépôt", "Repository", "リポジトリ", "仓库", "Repositório"),
    "cie_col_maturity": ("Declared maturity", "Madurez declarada", "Erklärte Reife", "Maturité déclarée", "Maturità dichiarata", "宣言された成熟度", "声明的成熟度", "Maturidade declarada"),
    "cie_col_declared": ("Declared evidence", "Evidencia declarada", "Erklärter Nachweis", "Preuve déclarée", "Evidenza dichiarata", "宣言されたエビデンス", "声明的证据", "Evidência declarada"),
    "cie_col_verified": ("Verified evidence", "Evidencia verificada", "Geprüfter Nachweis", "Preuve vérifiée", "Evidenza verificata", "検証済みエビデンス", "已验证的证据", "Evidência verificada"),
    "cie_col_state": ("Result", "Resultado", "Ergebnis", "Résultat", "Esito", "結果", "结果", "Resultado"),
    "cie_col_run": ("Last run", "Última ejecución", "Letzter Lauf", "Dernière exécution", "Ultima esecuzione", "最後の実行", "最近一次运行", "Última execução"),
    "cie_link": ("Run", "Ejecución", "Lauf", "Exécution", "Esecuzione", "実行", "运行", "Execução"),
    "cie_link_aria": ("Open the run of {name}", "Abrir la ejecución de {name}", "Lauf von {name} öffnen", "Ouvrir l'exécution de {name}", "Apri l'esecuzione di {name}", "{name} の実行を開く", "打开 {name} 的运行", "Abrir a execução de {name}"),
    "cie_caption": ("Maturity and evidence declared by each repository against what its CI verified", "Madurez y evidencia declaradas por cada repositorio frente a lo que verificó su CI", "Von jedem Repository erklärte Reife und Nachweise gegenüber dem, was sein CI geprüft hat", "Maturité et preuves déclarées par chaque dépôt face à ce que son CI a vérifié", "Maturità ed evidenze dichiarate da ogni repository rispetto a ciò che la sua CI ha verificato", "各リポジトリが宣言した成熟度とエビデンスと、CI が検証した内容の比較", "各仓库声明的成熟度和证据与其 CI 验证内容的对照", "Maturidade e evidências declaradas por cada repositório face ao que o seu CI verificou"),
    "cie_matches": ("{shown} of {total} repositories", "{shown} de {total} repositorios", "{shown} von {total} Repositorys", "{shown} dépôts sur {total}", "{shown} repository su {total}", "{total} 件中 {shown} 件", "{total} 个仓库中的 {shown} 个", "{shown} de {total} repositórios"),
    "cie_none": ("No repository matches this state.", "Ningún repositorio tiene este estado.", "Kein Repository hat diesen Status.", "Aucun dépôt n'a cet état.", "Nessun repository ha questo stato.", "この状態のリポジトリはありません。", "没有仓库处于此状态。", "Nenhum repositório tem este estado."),
    "cie_no_run": ("no run", "sin ejecución", "kein Lauf", "aucune exécution", "nessuna esecuzione", "実行なし", "无运行", "sem execução"),
    "cie_reason": ("Reason: {reason}", "Motivo: {reason}", "Grund: {reason}", "Motif : {reason}", "Motivo: {reason}", "理由：{reason}", "原因：{reason}", "Motivo: {reason}"),
    "cie_mat_scaffolding": ("Scaffolding", "Esqueleto", "Gerüst", "Ébauche", "Impalcatura", "足場段階", "雏形", "Esqueleto"),
    "cie_mat_functional": ("Functional", "Funcional", "Funktionsfähig", "Fonctionnel", "Funzionale", "機能的", "可运行", "Funcional"),
    "cie_mat_established": ("Established", "Consolidado", "Etabliert", "Établi", "Consolidato", "確立済み", "已确立", "Consolidado"),
    "cie_mat_production": ("Production", "Producción", "Produktion", "Production", "Produzione", "本番", "生产", "Produção"),
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
