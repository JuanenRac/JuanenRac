#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_actions_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the tab "Actions / Builds" (state and charts of the GitHub Actions runs) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "tab_actions": ("Builds", "Compilaciones", "Builds", "Builds", "Build", "ビルド", "构建", "Compilações"),
    "ac_title": (
        "Actions / Builds", "Actions / Compilaciones", "Actions / Builds", "Actions / Builds", "Actions / Build", "Actions / ビルド", "Actions / 构建", "Actions / Compilações"),
    "ac_badge": (
        "Near real time", "Casi en vivo", "Fast in Echtzeit", "Quasi en direct", "Quasi in tempo reale", "ほぼリアルタイム", "近乎实时", "Quase em direto"),
    "ac_hint": (
        "State and figures of the GitHub Actions runs of the last 24 hours and 7 days. Updated every 30 minutes and when a build of a repository of the ecosystem ends. No author, branch or commit text is kept.",
        "Estado y cifras de las ejecuciones de GitHub Actions de las últimas 24 horas y 7 días. Se actualiza cada 30 minutos y al terminar una compilación de un repositorio del ecosistema. No se guarda autor, rama ni texto de commit.",
        "Status und Zahlen der GitHub-Actions-Läufe der letzten 24 Stunden und 7 Tage. Aktualisierung alle 30 Minuten und wenn ein Build eines Repositorys des Ökosystems endet. Autor, Branch und Commit-Text werden nicht gespeichert.",
        "État et chiffres des exécutions GitHub Actions des dernières 24 heures et 7 jours. Mise à jour toutes les 30 minutes et à la fin d'un build d'un dépôt de l'écosystème. Ni auteur, ni branche, ni texte de commit ne sont conservés.",
        "Stato e cifre delle esecuzioni di GitHub Actions delle ultime 24 ore e 7 giorni. Aggiornato ogni 30 minuti e quando termina una build di un repository dell'ecosistema. Non si conservano autore, ramo né testo del commit.",
        "直近24時間と7日間の GitHub Actions 実行の状態と数値です。30分ごと、およびエコシステムのリポジトリのビルドが終わったときに更新されます。作者・ブランチ・コミット文は保持しません。",
        "最近 24 小时和 7 天内 GitHub Actions 运行的状态与数据。每 30 分钟更新一次,生态系统中仓库的构建结束时也会更新。不保存作者、分支或提交文本。",
        "Estado e valores das execuções do GitHub Actions das últimas 24 horas e 7 dias. Atualiza a cada 30 minutos e quando termina uma compilação de um repositório do ecossistema. Não se guarda autor, ramo nem texto de commit."),
    "ac_asof": (
        "Data as of {time} UTC", "Datos de las {time} UTC", "Stand {time} UTC", "Données de {time} UTC", "Dati delle {time} UTC", "{time} UTC 時点のデータ", "数据截至 {time} UTC", "Dados das {time} UTC"),
    "ac_compute_note": (
        "Computing minutes are approximate: wall-clock time of the finished runs of the last 24 hours, not the minutes GitHub bills (which depend on the runner and are rounded per job).",
        "Los minutos de cómputo son aproximados: tiempo de reloj de las ejecuciones terminadas en las últimas 24 horas, no los minutos que factura GitHub (dependen del runner y se redondean por trabajo).",
        "Die Rechenminuten sind ungefähr: Uhrzeit der beendeten Läufe der letzten 24 Stunden, nicht die von GitHub abgerechneten Minuten (sie hängen vom Runner ab und werden je Job gerundet).",
        "Les minutes de calcul sont approximatives : durée réelle des exécutions terminées dans les dernières 24 heures, pas les minutes facturées par GitHub (elles dépendent du runner et sont arrondies par job).",
        "I minuti di calcolo sono approssimati: tempo reale delle esecuzioni concluse nelle ultime 24 ore, non i minuti fatturati da GitHub (dipendono dal runner e sono arrotondati per job).",
        "計算時間は概算です。直近24時間に終了した実行の実時間であり、GitHub が課金する分(ランナーに依存し、ジョブごとに切り上げ)ではありません。",
        "计算分钟数为近似值:最近 24 小时内已完成运行的实际耗时,并非 GitHub 计费的分钟数(取决于运行器,且按作业取整)。",
        "Os minutos de cálculo são aproximados: tempo real das execuções terminadas nas últimas 24 horas, não os minutos faturados pelo GitHub (dependem do runner e são arredondados por trabalho)."),
    "ac_stale": (
        "GitHub could not be read in the last generation: the builds shown are the last known read, from {date}.",
        "No se pudo leer GitHub en la última generación: las compilaciones mostradas son la última lectura conocida, del {date}.",
        "GitHub konnte bei der letzten Erzeugung nicht gelesen werden: Die gezeigten Builds sind der letzte bekannte Stand vom {date}.",
        "GitHub n'a pas pu être lu lors de la dernière génération : les builds affichés sont la dernière lecture connue, du {date}.",
        "GitHub non è stato leggibile nell'ultima generazione: le build mostrate sono l'ultima lettura nota, del {date}.",
        "前回の生成で GitHub を読み取れませんでした。表示中のビルドは {date} の最後の既知の値です。",
        "上次生成时无法读取 GitHub:显示的构建是 {date} 的最近一次已知读取。",
        "Não foi possível ler o GitHub na última geração: as compilações mostradas são a última leitura conhecida, de {date}."),
    "ac_not_read": (
        "The builds could not be read in this generation and there is no earlier read: not verified.",
        "No se pudieron leer las compilaciones en esta generación y no hay lectura anterior: no verificado.",
        "Die Builds konnten bei dieser Erzeugung nicht gelesen werden und es gibt keinen früheren Stand: nicht geprüft.",
        "Les builds n'ont pas pu être lus lors de cette génération et il n'y a pas de lecture précédente : non vérifié.",
        "Le build non sono state leggibili in questa generazione e non c'è una lettura precedente: non verificato.",
        "今回の生成でビルドを読み取れず、以前の取得もありません:未確認です。",
        "本次生成无法读取构建,也没有更早的读取:未验证。",
        "Não foi possível ler as compilações nesta geração e não há leitura anterior: não verificado."),
    "ac_unverified": (
        "{n} repositories could not be read and are shown as not verified.",
        "{n} repositorios no se pudieron leer y se muestran como no verificados.",
        "{n} Repositories konnten nicht gelesen werden und erscheinen als nicht geprüft.",
        "{n} dépôts n'ont pas pu être lus et apparaissent comme non vérifiés.",
        "{n} repository non sono stati leggibili e risultano non verificati.",
        "{n} 件のリポジトリを読み取れず、未確認として表示しています。",
        "{n} 个仓库无法读取,显示为未验证。",
        "{n} repositórios não puderam ser lidos e aparecem como não verificados."),
    "ac_k_runs": ("Runs · 24 h", "Ejecuciones · 24 h", "Läufe · 24 h", "Exécutions · 24 h", "Esecuzioni · 24 h", "実行数 · 24時間", "运行次数 · 24 小时", "Execuções · 24 h"),
    "ac_k_rate": ("Success rate · 24 h", "Tasa de éxito · 24 h", "Erfolgsquote · 24 h", "Taux de réussite · 24 h", "Tasso di successo · 24 h", "成功率 · 24時間", "成功率 · 24 小时", "Taxa de sucesso · 24 h"),
    "ac_k_min": ("Computing · 24 h (approx.)", "Cómputo · 24 h (aprox.)", "Rechenzeit · 24 h (ca.)", "Calcul · 24 h (approx.)", "Calcolo · 24 h (appross.)", "計算時間 · 24時間(概算)", "计算时间 · 24 小时(约)", "Cálculo · 24 h (aprox.)"),
    "ac_k_failed": ("Open build-failed", "build-failed abiertas", "Offene build-failed", "build-failed ouvertes", "build-failed aperte", "未解決の build-failed", "未关闭的 build-failed", "build-failed abertas"),
    "ac_k_stuck": ("Open build-stuck", "build-stuck abiertas", "Offene build-stuck", "build-stuck ouvertes", "build-stuck aperte", "未解決の build-stuck", "未关闭的 build-stuck", "build-stuck abertas"),
    "ac_k_read": ("Repositories read", "Repositorios leídos", "Gelesene Repositories", "Dépôts lus", "Repository letti", "取得したリポジトリ", "已读取的仓库", "Repositórios lidos"),
    "ac_of": ("{n} of {m}", "{n} de {m}", "{n} von {m}", "{n} sur {m}", "{n} su {m}", "{m} 件中 {n} 件", "{m} 个中的 {n} 个", "{n} de {m}"),
    "ac_ring_title": ("Result · last 24 hours", "Resultado · últimas 24 horas", "Ergebnis · letzte 24 Stunden", "Résultat · dernières 24 heures", "Esito · ultime 24 ore", "結果 · 直近24時間", "结果 · 最近 24 小时", "Resultado · últimas 24 horas"),
    "ac_ring_aria": (
        "Results of the runs of the last 24 hours: {parts}", "Resultados de las ejecuciones de las últimas 24 horas: {parts}", "Ergebnisse der Läufe der letzten 24 Stunden: {parts}",
        "Résultats des exécutions des dernières 24 heures : {parts}", "Esito delle esecuzioni delle ultime 24 ore: {parts}", "直近24時間の実行結果:{parts}", "最近 24 小时的运行结果:{parts}",
        "Resultados das execuções das últimas 24 horas: {parts}"),
    "ac_ring_none": ("No runs in 24 hours", "Sin ejecuciones en 24 horas", "Keine Läufe in 24 Stunden", "Aucune exécution en 24 heures", "Nessuna esecuzione in 24 ore", "24時間以内の実行なし", "24 小时内没有运行", "Sem execuções em 24 horas"),
    "ac_ring_total": ("runs", "ejecuc.", "Läufe", "exéc.", "esec.", "実行", "运行", "execuç."),
    "ac_res_s": ("Success", "Correcto", "Erfolg", "Réussi", "Riuscito", "成功", "成功", "Sucesso"),
    "ac_res_f": ("Failure", "Fallo", "Fehler", "Échec", "Errore", "失敗", "失败", "Falha"),
    "ac_res_c": ("Cancelled", "Cancelado", "Abgebrochen", "Annulé", "Annullato", "キャンセル", "已取消", "Cancelado"),
    "ac_res_k": ("Other", "Otro", "Sonstige", "Autre", "Altro", "その他", "其他", "Outro"),
    "ac_res_p": ("Running", "En curso", "Läuft", "En cours", "In corso", "実行中", "运行中", "Em curso"),
    "ac_rate_title": ("Success rate · 7 days · lowest first", "Tasa de éxito · 7 días · las más bajas primero", "Erfolgsquote · 7 Tage · niedrigste zuerst", "Taux de réussite · 7 jours · les plus bas d'abord", "Tasso di successo · 7 giorni · prima i più bassi", "成功率 · 7日間 · 低い順", "成功率 · 7 天 · 由低到高", "Taxa de sucesso · 7 dias · as mais baixas primeiro"),
    "ac_rate_none": ("No finished runs in 7 days", "Sin ejecuciones terminadas en 7 días", "Keine beendeten Läufe in 7 Tagen", "Aucune exécution terminée en 7 jours", "Nessuna esecuzione conclusa in 7 giorni", "7日間に完了した実行なし", "7 天内没有已完成的运行", "Sem execuções terminadas em 7 dias"),
    "ac_rate_row": ("{name}: {p} % ({ok} of {all})", "{name}: {p} % ({ok} de {all})", "{name}: {p} % ({ok} von {all})", "{name} : {p} % ({ok} sur {all})", "{name}: {p} % ({ok} su {all})", "{name}:{p} %({all} 件中 {ok} 件)", "{name}:{p} %({all} 次中 {ok} 次)", "{name}: {p} % ({ok} de {all})"),
    "ac_dur_title": ("Duration of the last run · longest first", "Duración de la última ejecución · las más largas primero", "Dauer des letzten Laufs · längste zuerst", "Durée de la dernière exécution · les plus longues d'abord", "Durata dell'ultima esecuzione · prima le più lunghe", "直近の実行時間 · 長い順", "最近一次运行时长 · 由长到短", "Duração da última execução · as mais longas primeiro"),
    "ac_dur_row": ("{name}: {d}, {result}", "{name}: {d}, {result}", "{name}: {d}, {result}", "{name} : {d}, {result}", "{name}: {d}, {result}", "{name}:{d}、{result}", "{name}:{d},{result}", "{name}: {d}, {result}"),
    "ac_tl_title": ("Timeline · last 24 hours", "Línea de tiempo · últimas 24 horas", "Zeitleiste · letzte 24 Stunden", "Chronologie · dernières 24 heures", "Cronologia · ultime 24 ore", "タイムライン · 直近24時間", "时间线 · 最近 24 小时", "Linha do tempo · últimas 24 horas"),
    "ac_tl_aria": (
        "Timeline of the runs of the last 24 hours in {n} repositories; the table below has the same figures",
        "Línea de tiempo de las ejecuciones de las últimas 24 horas en {n} repositorios; la tabla de abajo tiene las mismas cifras",
        "Zeitleiste der Läufe der letzten 24 Stunden in {n} Repositories; die Tabelle darunter enthält dieselben Zahlen",
        "Chronologie des exécutions des dernières 24 heures dans {n} dépôts ; le tableau ci-dessous contient les mêmes chiffres",
        "Cronologia delle esecuzioni delle ultime 24 ore in {n} repository; la tabella sotto riporta le stesse cifre",
        "{n} 件のリポジトリの直近24時間の実行タイムラインです。下の表に同じ数値があります",
        "{n} 个仓库最近 24 小时运行的时间线;下表有相同的数据",
        "Linha do tempo das execuções das últimas 24 horas em {n} repositórios; a tabela abaixo tem os mesmos valores"),
    "ac_tl_none": ("No runs in the last 24 hours", "Sin ejecuciones en las últimas 24 horas", "Keine Läufe in den letzten 24 Stunden", "Aucune exécution dans les dernières 24 heures", "Nessuna esecuzione nelle ultime 24 ore", "直近24時間の実行はありません", "最近 24 小时没有运行", "Sem execuções nas últimas 24 horas"),
    "ac_tl_axis_start": ("24 h ago", "hace 24 h", "vor 24 h", "il y a 24 h", "24 h fa", "24時間前", "24 小时前", "há 24 h"),
    "ac_tl_axis_end": ("now", "ahora", "jetzt", "maintenant", "ora", "現在", "现在", "agora"),
    "ac_tl_dot": ("{name}: {result}, {ago} ago", "{name}: {result}, hace {ago}", "{name}: {result}, vor {ago}", "{name} : {result}, il y a {ago}", "{name}: {result}, {ago} fa", "{name}:{result}、{ago}前", "{name}:{result},{ago}前", "{name}: {result}, há {ago}"),
    "ac_trend_title": ("Runs per day", "Ejecuciones por día", "Läufe pro Tag", "Exécutions par jour", "Esecuzioni al giorno", "1日あたりの実行数", "每日运行次数", "Execuções por dia"),
    "ac_trend_col": ("{date}: {runs} runs, {ok} successful, {fail} failed", "{date}: {runs} ejecuciones, {ok} correctas, {fail} con fallo", "{date}: {runs} Läufe, {ok} erfolgreich, {fail} fehlgeschlagen", "{date} : {runs} exécutions, {ok} réussies, {fail} en échec", "{date}: {runs} esecuzioni, {ok} riuscite, {fail} con errore", "{date}:実行 {runs} 件、成功 {ok} 件、失敗 {fail} 件", "{date}:运行 {runs} 次,成功 {ok} 次,失败 {fail} 次", "{date}: {runs} execuções, {ok} com sucesso, {fail} com falha"),
    "ac_trend_none": (
        "The daily history starts with the first reading; it fills in one day at a time.",
        "El historial diario empieza con la primera lectura y se completa un día cada vez.",
        "Der Tagesverlauf beginnt mit der ersten Messung und füllt sich Tag für Tag.",
        "L'historique quotidien commence à la première lecture et se complète jour après jour.",
        "Lo storico giornaliero parte dalla prima lettura e si completa un giorno alla volta.",
        "日次の履歴は最初の取得から始まり、1日ずつ増えていきます。",
        "每日历史从第一次读取开始,每天增加一天。",
        "O histórico diário começa na primeira leitura e completa-se um dia de cada vez."),
    "ac_table_title": ("Repositories", "Repositorios", "Repositories", "Dépôts", "Repository", "リポジトリ", "仓库", "Repositórios"),
    "ac_table_caption": (
        "State of the builds of every repository", "Estado de las compilaciones de cada repositorio", "Status der Builds jedes Repositorys", "État des builds de chaque dépôt",
        "Stato delle build di ogni repository", "各リポジトリのビルドの状態", "各仓库的构建状态", "Estado das compilações de cada repositório"),
    "ac_search": ("Search a repository", "Buscar un repositorio", "Repository suchen", "Chercher un dépôt", "Cerca un repository", "リポジトリを検索", "搜索仓库", "Pesquisar um repositório"),
    "ac_filter_eco": ("Ecosystem", "Ecosistema", "Ökosystem", "Écosystème", "Ecosistema", "エコシステム", "生态系统", "Ecossistema"),
    "ac_all": ("All", "Todos", "Alle", "Tous", "Tutti", "すべて", "全部", "Todos"),
    "ac_matches": ("{shown} of {total} repositories", "{shown} de {total} repositorios", "{shown} von {total} Repositories", "{shown} sur {total} dépôts", "{shown} su {total} repository", "{total} 件中 {shown} 件のリポジトリ", "{total} 个仓库中的 {shown} 个", "{shown} de {total} repositórios"),
    "ac_none_match": ("No repository matches.", "Ningún repositorio coincide.", "Kein Repository passt.", "Aucun dépôt ne correspond.", "Nessun repository corrisponde.", "該当するリポジトリはありません。", "没有匹配的仓库。", "Nenhum repositório corresponde."),
    "ac_col_repo": ("Repository", "Repositorio", "Repository", "Dépôt", "Repository", "リポジトリ", "仓库", "Repositório"),
    "ac_col_result": ("Last result", "Último resultado", "Letztes Ergebnis", "Dernier résultat", "Ultimo esito", "直近の結果", "最近结果", "Último resultado"),
    "ac_col_ago": ("Ago", "Hace", "Vor", "Il y a", "Fa", "経過", "距今", "Há"),
    "ac_col_lastok": ("Last success", "Último éxito", "Letzter Erfolg", "Dernier succès", "Ultimo successo", "最後の成功", "最近成功", "Último sucesso"),
    "ac_col_ok24": ("Success 24 h", "Éxito 24 h", "Erfolg 24 h", "Réussite 24 h", "Successo 24 h", "成功 24時間", "成功 24 小时", "Sucesso 24 h"),
    "ac_col_min": ("Min 24 h (approx.)", "Min 24 h (aprox.)", "Min 24 h (ca.)", "Min 24 h (approx.)", "Min 24 h (appross.)", "分 24時間(概算)", "分钟 24 小时(约)", "Min 24 h (aprox.)"),
    "ac_col_issues": ("Open issues", "Issues abiertas", "Offene Issues", "Issues ouvertes", "Issue aperte", "未解決の課題", "未关闭的 Issue", "Issues abertas"),
    "ac_col_pipe": ("Pipeline · signature", "Proceso · firma", "Ablauf · Signatur", "Chaîne · signature", "Processo · firma", "工程 · 署名", "流程 · 签名", "Processo · assinatura"),
    "ac_issues_cell": ("failed {f} · stuck {s}", "fallo {f} · atascada {s}", "fehlgeschlagen {f} · hängend {s}", "échec {f} · bloquée {s}", "errore {f} · bloccata {s}", "失敗 {f} · 停滞 {s}", "失败 {f} · 卡住 {s}", "falha {f} · bloqueada {s}"),
    "ac_no_workflows": ("No workflows", "Sin workflows", "Keine Workflows", "Aucun workflow", "Nessun workflow", "ワークフローなし", "没有工作流", "Sem workflows"),
    "ac_no_runs": ("No runs in 7 days", "Sin ejecuciones en 7 días", "Keine Läufe in 7 Tagen", "Aucune exécution en 7 jours", "Nessuna esecuzione in 7 giorni", "7日間の実行なし", "7 天内没有运行", "Sem execuções em 7 dias"),
    "ac_over_week": (">7 d", ">7 d", ">7 T", ">7 j", ">7 g", ">7日", ">7 天", ">7 d"),
    "ac_ago_min": ("{n} min", "{n} min", "{n} Min.", "{n} min", "{n} min", "{n} 分", "{n} 分钟", "{n} min"),
    "ac_ago_h": ("{n} h", "{n} h", "{n} Std.", "{n} h", "{n} h", "{n} 時間", "{n} 小时", "{n} h"),
    "ac_ago_d": ("{n} d", "{n} d", "{n} T", "{n} j", "{n} g", "{n} 日", "{n} 天", "{n} d"),
    "ac_dur_min": ("{n} min", "{n} min", "{n} Min.", "{n} min", "{n} min", "{n} 分", "{n} 分钟", "{n} min"),
    "ac_dur_sec": ("{n} s", "{n} s", "{n} s", "{n} s", "{n} s", "{n} 秒", "{n} 秒", "{n} s"),
    "ac_dur_hour": ("{h} h {m} min", "{h} h {m} min", "{h} Std. {m} Min.", "{h} h {m} min", "{h} h {m} min", "{h} 時間 {m} 分", "{h} 小时 {m} 分钟", "{h} h {m} min"),
    "ac_approx_min": ("~{n} min", "~{n} min", "~{n} Min.", "~{n} min", "~{n} min", "約 {n} 分", "约 {n} 分钟", "~{n} min"),
    "ac_approx_h": ("~{n} h", "~{n} h", "~{n} Std.", "~{n} h", "~{n} h", "約 {n} 時間", "约 {n} 小时", "~{n} h"),
    "ac_total_min": ("Total about {n} min", "Total unos {n} min", "Insgesamt etwa {n} Min.", "Total environ {n} min", "Totale circa {n} min", "合計 約 {n} 分", "合计约 {n} 分钟", "Total cerca de {n} min"),
    "ac_row_aria": ("{name}: {summary}", "{name}: {summary}", "{name}: {summary}", "{name} : {summary}", "{name}: {summary}", "{name}:{summary}", "{name}:{summary}", "{name}: {summary}"),
    "ac_sig_present": ("signature file", "archivo de firma", "Signaturdatei", "fichier de signature", "file di firma", "署名ファイルあり", "有签名文件", "ficheiro de assinatura"),
    "ac_sig_none": ("no signature", "sin firma", "keine Signatur", "sans signature", "senza firma", "署名なし", "无签名", "sem assinatura"),
    "ac_sig_norelease": ("no release", "sin versión", "keine Version", "sans version", "senza versione", "リリースなし", "无版本", "sem versão"),
    "ac_sig_unverified": ("not verified", "no verificado", "nicht geprüft", "non vérifié", "non verificato", "未確認", "未验证", "não verificado"),
    "ac_help_summary": ("How it is calculated", "Cómo se calcula", "So wird gerechnet", "Comment c'est calculé", "Come si calcola", "計算方法", "计算方式", "Como é calculado"),
    "ac_help_body": (
        "Success rate = successful runs over finished runs that either succeeded or failed (cancelled, skipped and running runs are left out). Failure includes timeouts. The 24-hour window ends at the moment of the reading. Only the last 100 runs of the last 7 days of each repository are read, so a very busy repository may show fewer. Pipeline and signature come from the manifest and the latest release (a signature file is detected, not verified).",
        "Tasa de éxito = ejecuciones correctas entre las terminadas que acabaron bien o mal (las canceladas, omitidas y en curso no cuentan). Fallo incluye los tiempos agotados. La ventana de 24 horas termina en el momento de la lectura. Solo se leen las últimas 100 ejecuciones de los últimos 7 días de cada repositorio, así que uno muy activo puede mostrar menos. Proceso y firma salen del manifiesto y de la última versión (se detecta el archivo de firma, no se verifica).",
        "Erfolgsquote = erfolgreiche Läufe geteilt durch beendete Läufe mit Erfolg oder Fehler (abgebrochene, übersprungene und laufende zählen nicht). Fehler schließt Zeitüberschreitungen ein. Das 24-Stunden-Fenster endet im Moment der Messung. Je Repository werden nur die letzten 100 Läufe der letzten 7 Tage gelesen; ein sehr aktives kann weniger zeigen. Ablauf und Signatur stammen aus dem Manifest und dem letzten Release (die Signaturdatei wird erkannt, nicht geprüft).",
        "Taux de réussite = exécutions réussies sur les exécutions terminées en succès ou en échec (annulées, ignorées et en cours exclues). L'échec inclut les délais dépassés. La fenêtre de 24 heures se termine au moment de la lecture. Seules les 100 dernières exécutions des 7 derniers jours de chaque dépôt sont lues ; un dépôt très actif peut en montrer moins. La chaîne et la signature viennent du manifeste et de la dernière version (le fichier de signature est détecté, pas vérifié).",
        "Tasso di successo = esecuzioni riuscite sulle concluse con successo o errore (annullate, saltate e in corso escluse). L'errore include i timeout. La finestra di 24 ore termina al momento della lettura. Di ogni repository si leggono solo le ultime 100 esecuzioni degli ultimi 7 giorni, quindi uno molto attivo può mostrarne meno. Processo e firma derivano dal manifest e dall'ultima versione (il file di firma è rilevato, non verificato).",
        "成功率 = 成功した実行 ÷ 成功または失敗で終わった実行(キャンセル・スキップ・実行中は除外)。失敗にはタイムアウトを含みます。24時間の範囲は取得時点で終わります。各リポジトリは直近7日間の最新100件のみ読むため、非常に活発なリポジトリでは少なく表示されることがあります。工程と署名はマニフェストと最新リリースによるもので、署名ファイルは検出のみで検証はしていません。",
        "成功率 = 成功的运行 ÷ 以成功或失败结束的运行(已取消、已跳过和进行中的不计入)。失败包含超时。24 小时窗口截止于读取时刻。每个仓库只读取最近 7 天的最新 100 次运行,因此非常活跃的仓库可能显示更少。流程和签名来自清单和最新版本(只检测签名文件,不做验证)。",
        "Taxa de sucesso = execuções com sucesso a dividir pelas terminadas com sucesso ou falha (canceladas, ignoradas e em curso não contam). A falha inclui tempos esgotados. A janela de 24 horas termina no momento da leitura. De cada repositório só se leem as últimas 100 execuções dos últimos 7 dias, pelo que um muito ativo pode mostrar menos. Processo e assinatura vêm do manifesto e da última versão (o ficheiro de assinatura é detetado, não verificado)."),
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
