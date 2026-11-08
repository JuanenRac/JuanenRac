#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_cover_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the coverage card, the notice of new / archived / disappeared repositories, the Tools group and the performance additions of the status
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
    # ---- The Tools group ----
    "tools_progress": (
        "{percent} % · maturity, evidence and delivery of {count} tools",
        "{percent} % · madurez, evidencia y entrega de {count} herramientas",
        "{percent} % · Reife, Nachweis und Auslieferung von {count} Werkzeugen",
        "{percent} % · maturité, preuves et livraison de {count} outils",
        "{percent} % · maturità, prove e consegna di {count} strumenti",
        "{percent} % · {count} 件のツールの成熟度・検証・提供",
        "{percent} % · {count} 个工具的成熟度、验证依据和交付",
        "{percent} % · maturidade, evidência e entrega de {count} ferramentas",
    ),
    "tools_progress_unknown": ("progress not verified", "progreso no verificado", "Fortschritt nicht geprüft", "progression non vérifiée", "avanzamento non verificato", "進捗は未確認", "进度未验证", "progresso não verificado"),
    "tools_filter": ("Filter the table", "Filtrar la tabla", "Tabelle filtern", "Filtrer le tableau", "Filtra la tabella", "表を絞り込む", "筛选表格", "Filtrar a tabela"),
    # ---- Builds tab: speed, queue and flaky runs ----
    "ac_perf_title": ("Speed, queue and flaky runs", "Velocidad, cola y ejecuciones inestables", "Geschwindigkeit, Warteschlange und instabile Läufe", "Vitesse, file d'attente et exécutions instables", "Velocità, coda ed esecuzioni instabili", "速度・待ち時間・不安定な実行", "速度、排队和不稳定的运行", "Velocidade, fila e execuções instáveis"),
    "ac_perf_hint": (
        "The p50 and p95 of how long the successful runs of the last 7 days take and of how long a run waits before it starts, and the workflows that failed and then passed on the very same commit. Same definitions as the analytics of the local Actions monitor, taken per run; the label \"flaky\" never changes what counts as red.",
        "El p50 y el p95 de lo que tardan las ejecuciones correctas de los últimos 7 días y de lo que espera una ejecución antes de empezar, y los workflows que fallaron y luego pasaron en el mismo commit. Mismas definiciones que la analítica del monitor local de Actions, tomadas por ejecución; la etiqueta «inestable» nunca cambia lo que cuenta como rojo.",
        "Der p50 und p95 der Dauer der erfolgreichen Läufe der letzten 7 Tage und der Wartezeit eines Laufs vor dem Start sowie die Workflows, die auf demselben Commit erst fehlschlugen und dann durchliefen. Dieselben Definitionen wie in der Analyse des lokalen Actions-Monitors, je Lauf gemessen; die Markierung „instabil“ ändert nie, was als rot zählt.",
        "Le p50 et le p95 de la durée des exécutions réussies des 7 derniers jours et de l'attente d'une exécution avant son démarrage, et les workflows qui ont échoué puis réussi sur le même commit. Mêmes définitions que l'analytique du moniteur local d'Actions, prises par exécution ; l'étiquette « instable » ne change jamais ce qui compte comme rouge.",
        "Il p50 e il p95 della durata delle esecuzioni riuscite degli ultimi 7 giorni e dell'attesa di un'esecuzione prima dell'avvio, e i workflow che sono falliti e poi passati sullo stesso commit. Stesse definizioni dell'analitica del monitor locale di Actions, prese per esecuzione; l'etichetta «instabile» non cambia mai ciò che conta come rosso.",
        "直近 7 日間の成功した実行にかかった時間と、実行が開始までに待つ時間の p50 と p95、そして同じコミットで失敗した後に成功したワークフローです。ローカルの Actions モニターの分析と同じ定義で、実行ごとに集計します。「不安定」の印は、何を赤とみなすかを変えません。",
        "最近 7 天内成功运行的耗时、运行开始前的等待时间的 p50 和 p95,以及在同一提交上先失败后通过的工作流。定义与本地 Actions 监视器的分析相同,按运行计算;“不稳定”标记绝不改变什么算红色。",
        "O p50 e o p95 do tempo das execuções com sucesso dos últimos 7 dias e da espera de uma execução antes de começar, e os workflows que falharam e depois passaram no mesmo commit. As mesmas definições da análise do monitor local de Actions, tomadas por execução; a etiqueta «instável» nunca altera o que conta como vermelho.",
    ),
    "ac_perf_k_dur": ("Duration p50 · p95", "Duración p50 · p95", "Dauer p50 · p95", "Durée p50 · p95", "Durata p50 · p95", "所要時間 p50 · p95", "耗时 p50 · p95", "Duração p50 · p95"),
    "ac_perf_k_queue": ("Queue p50 · p95", "Cola p50 · p95", "Warteschlange p50 · p95", "File d'attente p50 · p95", "Coda p50 · p95", "待ち時間 p50 · p95", "排队 p50 · p95", "Fila p50 · p95"),
    "ac_perf_k_runs": ("Successful runs measured", "Ejecuciones correctas medidas", "Gemessene erfolgreiche Läufe", "Exécutions réussies mesurées", "Esecuzioni riuscite misurate", "計測した成功実行", "已测量的成功运行", "Execuções com sucesso medidas"),
    "ac_perf_k_flaky": ("Flaky workflows", "Workflows inestables", "Instabile Workflows", "Workflows instables", "Workflow instabili", "不安定なワークフロー", "不稳定的工作流", "Workflows instáveis"),
    "ac_perf_slow_title": ("Slowest workflows (p95)", "Workflows más lentos (p95)", "Langsamste Workflows (p95)", "Workflows les plus lents (p95)", "Workflow più lenti (p95)", "最も遅いワークフロー(p95)", "最慢的工作流(p95)", "Workflows mais lentos (p95)"),
    "ac_perf_flaky_title": ("Flaky workflows", "Workflows inestables", "Instabile Workflows", "Workflows instables", "Workflow instabili", "不安定なワークフロー", "不稳定的工作流", "Workflows instáveis"),
    "ac_perf_slow_row": (
        "{name}: p50 {p50}, p95 {p95}, {n} runs",
        "{name}: p50 {p50}, p95 {p95}, {n} ejecuciones",
        "{name}: p50 {p50}, p95 {p95}, {n} Läufe",
        "{name} : p50 {p50}, p95 {p95}, {n} exécutions",
        "{name}: p50 {p50}, p95 {p95}, {n} esecuzioni",
        "{name}:p50 {p50}、p95 {p95}、{n} 回",
        "{name}:p50 {p50},p95 {p95},{n} 次运行",
        "{name}: p50 {p50}, p95 {p95}, {n} execuções",
    ),
    "ac_perf_flaky_row": (
        "{name}: {fl} commits needed a retry in {runs} runs",
        "{name}: {fl} commits necesitaron un reintento en {runs} ejecuciones",
        "{name}: {fl} Commits brauchten einen Wiederholungslauf bei {runs} Läufen",
        "{name} : {fl} commits ont demandé une nouvelle tentative sur {runs} exécutions",
        "{name}: {fl} commit hanno richiesto un nuovo tentativo su {runs} esecuzioni",
        "{name}:{runs} 回の実行のうち {fl} 件のコミットで再試行が必要でした",
        "{name}:{runs} 次运行中有 {fl} 个提交需要重试",
        "{name}: {fl} commits precisaram de nova tentativa em {runs} execuções",
    ),
    "ac_perf_none": (
        "Not measured yet: the last reading does not carry these figures.",
        "Aún sin medir: la última lectura no trae estas cifras.",
        "Noch nicht gemessen: Die letzte Auslesung enthält diese Zahlen nicht.",
        "Pas encore mesuré : la dernière lecture ne contient pas ces chiffres.",
        "Non ancora misurato: l'ultima lettura non contiene questi numeri.",
        "未計測:直近の読み取りにはこれらの数値が含まれていません。",
        "尚未测量:最近一次读取不含这些数据。",
        "Ainda sem medição: a última leitura não traz estes números.",
    ),
    "ac_perf_empty": ("Nothing to show", "Nada que mostrar", "Nichts anzuzeigen", "Rien à afficher", "Niente da mostrare", "表示するものはありません", "没有可显示的内容", "Nada para mostrar"),
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
