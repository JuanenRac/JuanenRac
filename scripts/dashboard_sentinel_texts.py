#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_sentinel_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the tab "Sentinel" (a public-safe watch over the repositories, decided by rules) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. The report of the
tab is chosen from these texts by the page (the document only holds the kind of line and its figures). Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "tab_sentinel": ("Sentinel", "Centinela", "Wächter", "Sentinelle", "Sentinella", "センチネル", "哨兵", "Sentinela"),
    "sn_title": ("Sentinel: watch over the ecosystem", "Centinela: vigilancia del ecosistema", "Wächter: Überwachung des Ökosystems", "Sentinelle : veille sur l'écosystème",
                 "Sentinella: sorveglianza dell'ecosistema", "センチネル: エコシステムの監視", "哨兵:生态系统监视", "Sentinela: vigilância do ecossistema"),
    "sn_badge": ("Rules, no AI", "Reglas, sin IA", "Regeln, ohne KI", "Règles, sans IA", "Regole, senza IA", "ルールのみ(AI なし)", "仅规则,无 AI", "Regras, sem IA"),
    "sn_hint": (
        "A public-safe summary read when the page was generated: builds on the main branch, releases ready, signatures, public hygiene, computing and trends. It is decided by fixed rules, with no AI. Security alerts, pull requests, issues and people are deliberately not shown.",
        "Un resumen seguro para publicar, leído al generar la página: compilaciones en la rama principal, versiones listas, firmas, higiene pública, cómputo y tendencias. Lo deciden reglas fijas, sin IA. Las alertas de seguridad, las pull requests, las issues y las personas no se muestran a propósito.",
        "Eine für die Veröffentlichung unbedenkliche Zusammenfassung, gelesen beim Erzeugen der Seite: Builds auf dem Hauptzweig, bereite Versionen, Signaturen, öffentliche Hygiene, Rechenzeit und Trends. Feste Regeln entscheiden, keine KI. Sicherheitswarnungen, Pull Requests, Issues und Personen werden absichtlich nicht gezeigt.",
        "Un résumé sans risque pour le public, lu à la génération de la page : builds sur la branche principale, versions prêtes, signatures, hygiène publique, calcul et tendances. Des règles fixes décident, sans IA. Les alertes de sécurité, pull requests, issues et personnes ne sont volontairement pas affichées.",
        "Un riepilogo sicuro da pubblicare, letto alla generazione della pagina: build sul ramo principale, versioni pronte, firme, igiene pubblica, calcolo e tendenze. Lo decidono regole fisse, senza IA. Avvisi di sicurezza, pull request, issue e persone non vengono mostrati di proposito.",
        "ページ生成時に読み取った、公開しても安全な要約です。メインブランチのビルド、公開準備のできたバージョン、署名、公開リポジトリの衛生状態、計算時間、推移を扱います。判定は固定ルールで、AI は使いません。セキュリティアラート、プルリクエスト、Issue、個人は意図的に表示しません。",
        "页面生成时读取的、可安全公开的摘要:主分支构建、可发布版本、签名、公开仓库规范、计算用量和趋势。由固定规则判定,不使用 AI。安全警报、拉取请求、议题和个人信息有意不显示。",
        "Um resumo seguro para publicar, lido ao gerar a página: compilações no ramo principal, versões prontas, assinaturas, higiene pública, cálculo e tendências. Decidem regras fixas, sem IA. Os alertas de segurança, as pull requests, as issues e as pessoas não se mostram de propósito."),
    "sn_asof": ("Data as of {time} UTC", "Datos de las {time} UTC", "Stand {time} UTC", "Données de {time} UTC", "Dati delle {time} UTC", "{time} UTC 時点のデータ", "数据截至 {time} UTC", "Dados das {time} UTC"),
    "sn_stale": (
        "GitHub could not be read in the last generation: the last known reading of {date} is shown, not a current one.",
        "No se pudo leer GitHub en la última generación: se muestra la última lectura conocida del {date}, no una actual.",
        "GitHub konnte bei der letzten Erzeugung nicht gelesen werden: Es wird die letzte bekannte Lesung vom {date} gezeigt, keine aktuelle.",
        "GitHub n'a pas pu être lu à la dernière génération : la dernière lecture connue du {date} est affichée, pas une lecture actuelle.",
        "GitHub non è stato leggibile all'ultima generazione: si mostra l'ultima lettura nota del {date}, non una attuale.",
        "前回の生成で GitHub を読み取れなかったため、最後に読み取れた {date} のデータを表示しています(最新ではありません)。",
        "上次生成时无法读取 GitHub:显示的是 {date} 的最后一次已知读数,并非当前数据。",
        "Não foi possível ler o GitHub na última geração: mostra-se a última leitura conhecida de {date}, não uma atual."),
    "sn_not_read": ("The sentinel has no reading yet: not verified.", "El Centinela aún no tiene lectura: no verificado.", "Der Wächter hat noch keine Lesung: nicht geprüft.",
                    "La sentinelle n'a pas encore de lecture : non vérifié.", "La sentinella non ha ancora una lettura: non verificato.", "センチネルはまだ読み取りがありません。未検証です。",
                    "哨兵尚无读数:未验证。", "A Sentinela ainda não tem leitura: não verificado."),
    "sn_off": ("The sentinel is switched off in the configuration.", "El Centinela está desactivado en la configuración.", "Der Wächter ist in der Konfiguration abgeschaltet.",
               "La sentinelle est désactivée dans la configuration.", "La sentinella è disattivata nella configurazione.", "センチネルは設定で無効になっています。", "哨兵已在配置中关闭。",
               "A Sentinela está desativada na configuração."),
    "sn_off_section": ("This section is switched off in the configuration.", "Esta sección está desactivada en la configuración.", "Dieser Abschnitt ist in der Konfiguration abgeschaltet.",
                       "Cette section est désactivée dans la configuration.", "Questa sezione è disattivata nella configurazione.", "このセクションは設定で無効になっています。", "此部分已在配置中关闭。",
                       "Esta secção está desativada na configuração."),
    "sn_parte_title": ("Report (made by rules, no AI)", "Parte (hecho por reglas, sin IA)", "Bericht (nach Regeln, ohne KI)", "Rapport (par règles, sans IA)", "Rapporto (da regole, senza IA)",
                       "レポート(ルールで生成、AI なし)", "报告(由规则生成,无 AI)", "Parte (feito por regras, sem IA)"),
    "sn_lvl_ok": ("In order", "En orden", "In Ordnung", "En ordre", "In ordine", "問題なし", "正常", "Em ordem"),
    "sn_lvl_info": ("Note", "Nota", "Hinweis", "Note", "Nota", "注記", "提示", "Nota"),
    "sn_lvl_warn": ("Attention", "Atención", "Achtung", "Attention", "Attenzione", "要注意", "注意", "Atenção"),
    "sn_lvl_bad": ("Problem", "Problema", "Problem", "Problème", "Problema", "問題あり", "问题", "Problema"),
    "sp_head": (
        "{red} red workflows, {cand} releases ready, {bad} invalid signatures, {hyg} repositories with a hygiene gap.",
        "{red} flujos en rojo, {cand} versiones listas, {bad} firmas inválidas, {hyg} repositorios con un hueco de higiene.",
        "{red} rote Workflows, {cand} bereite Versionen, {bad} ungültige Signaturen, {hyg} Repositorys mit einer Hygienelücke.",
        "{red} workflows en rouge, {cand} versions prêtes, {bad} signatures invalides, {hyg} dépôts avec une lacune d'hygiène.",
        "{red} workflow in rosso, {cand} versioni pronte, {bad} firme non valide, {hyg} repository con una lacuna di igiene.",
        "赤のワークフロー {red} 件、公開準備のできたバージョン {cand} 件、無効な署名 {bad} 件、衛生上の不備があるリポジトリ {hyg} 件。",
        "红色工作流 {red} 个,可发布版本 {cand} 个,无效签名 {bad} 个,存在规范缺口的仓库 {hyg} 个。",
        "{red} fluxos a vermelho, {cand} versões prontas, {bad} assinaturas inválidas, {hyg} repositórios com uma falha de higiene."),
    "sp_all_ok": ("Everything that could be read is in order.", "Todo lo que se pudo leer está en orden.", "Alles, was gelesen werden konnte, ist in Ordnung.",
                  "Tout ce qui a pu être lu est en ordre.", "Tutto ciò che si è potuto leggere è in ordine.", "読み取れたものはすべて問題ありません。", "所有已读取的内容均正常。",
                  "Tudo o que se pôde ler está em ordem."),
    "sp_red": (
        "Red on the main branch: {list}. Decide: fix or run again.",
        "En rojo en la rama principal: {list}. Decidir: arreglar o relanzar.",
        "Rot auf dem Hauptzweig: {list}. Entscheiden: beheben oder erneut starten.",
        "En rouge sur la branche principale : {list}. À décider : corriger ou relancer.",
        "In rosso sul ramo principale: {list}. Decidere: correggere o rilanciare.",
        "メインブランチで赤: {list}。修正するか再実行するかを判断してください。",
        "主分支为红色:{list}。请决定:修复或重新运行。",
        "A vermelho no ramo principal: {list}. Decidir: corrigir ou voltar a executar."),
    "sp_cand": (
        "Ready for a new version: {list}.",
        "Listos para lanzar versión: {list}.",
        "Bereit für eine neue Version: {list}.",
        "Prêts pour une nouvelle version : {list}.",
        "Pronti per una nuova versione: {list}.",
        "新バージョンを出せる状態: {list}。",
        "可发布新版本:{list}。",
        "Prontos para lançar versão: {list}."),
    "sp_sig": (
        "INVALID signature of the latest release: {list}. Do not install it.",
        "Firma INVÁLIDA en la última versión: {list}. No instalarla.",
        "UNGÜLTIGE Signatur der letzten Version: {list}. Nicht installieren.",
        "Signature INVALIDE de la dernière version : {list}. Ne pas l'installer.",
        "Firma NON VALIDA dell'ultima versione: {list}. Non installarla.",
        "最新リリースの署名が無効です: {list}。インストールしないでください。",
        "最新版本的签名无效:{list}。请勿安装。",
        "Assinatura INVÁLIDA da última versão: {list}. Não a instalar."),
    "sp_hyg": (
        "No active ruleset protecting the main branch: {list}.",
        "Sin ruleset activo que proteja la rama principal: {list}.",
        "Kein aktives Regelwerk schützt den Hauptzweig: {list}.",
        "Aucun ruleset actif ne protège la branche principale : {list}.",
        "Nessun ruleset attivo protegge il ramo principale: {list}.",
        "メインブランチを保護する有効なルールセットがありません: {list}。",
        "没有保护主分支的有效规则集:{list}。",
        "Sem ruleset ativo a proteger o ramo principal: {list}."),
    "sp_settings": (
        "The Actions settings (actions pinned by SHA, allowed actions) cannot be read with the read-only token: not verified in {m} repositories.",
        "Los ajustes de Actions (acciones fijadas por SHA, acciones permitidas) no se pueden leer con el token de solo lectura: sin verificar en {m} repositorios.",
        "Die Actions-Einstellungen (per SHA fixierte Actions, erlaubte Actions) sind mit dem Nur-Lese-Token nicht lesbar: in {m} Repositorys nicht geprüft.",
        "Les réglages d'Actions (actions figées par SHA, actions autorisées) ne sont pas lisibles avec le jeton en lecture seule : non vérifié dans {m} dépôts.",
        "Le impostazioni di Actions (azioni fissate per SHA, azioni consentite) non sono leggibili con il token di sola lettura: non verificato in {m} repository.",
        "Actions の設定(SHA 固定、許可されたアクション)は読み取り専用トークンでは読めません。{m} 件のリポジトリで未検証です。",
        "只读令牌无法读取 Actions 设置(按 SHA 固定的动作、允许的动作):{m} 个仓库未验证。",
        "As definições do Actions (ações fixadas por SHA, ações permitidas) não se podem ler com o token só de leitura: por verificar em {m} repositórios."),
    "sp_compute": (
        "High computing: about {min} minutes in the last 24 hours.",
        "Cómputo alto: unos {min} minutos en las últimas 24 horas.",
        "Hoher Rechenaufwand: etwa {min} Minuten in den letzten 24 Stunden.",
        "Calcul élevé : environ {min} minutes sur les dernières 24 heures.",
        "Calcolo elevato: circa {min} minuti nelle ultime 24 ore.",
        "計算時間が多めです。直近24時間でおよそ {min} 分。",
        "计算用量偏高:最近 24 小时约 {min} 分钟。",
        "Cálculo elevado: cerca de {min} minutos nas últimas 24 horas."),
    "sp_unread": (
        "{n} of {m} repositories could not be read: they are not counted as in order.",
        "No se pudieron leer {n} de {m} repositorios: no se cuentan como en orden.",
        "{n} von {m} Repositorys konnten nicht gelesen werden: Sie zählen nicht als in Ordnung.",
        "{n} dépôts sur {m} n'ont pas pu être lus : ils ne comptent pas comme en ordre.",
        "{n} repository su {m} non sono stati leggibili: non contano come in ordine.",
        "{m} 件中 {n} 件のリポジトリを読み取れませんでした。正常としては数えません。",
        "{m} 个仓库中有 {n} 个无法读取:不计为正常。",
        "Não foi possível ler {n} de {m} repositórios: não contam como em ordem."),
    "sn_more": ("and {n} more", "y {n} más", "und {n} weitere", "et {n} de plus", "e altri {n}", "ほか {n} 件", "另有 {n} 个", "e mais {n}"),
    "sn_k_red": ("Red workflows", "Flujos en rojo", "Rote Workflows", "Workflows en rouge", "Workflow in rosso", "赤のワークフロー", "红色工作流", "Fluxos a vermelho"),
    "sn_k_cand": ("Releases ready", "Versiones listas", "Bereite Versionen", "Versions prêtes", "Versioni pronte", "公開準備済み", "可发布版本", "Versões prontas"),
    "sn_k_sig": ("Invalid signatures", "Firmas inválidas", "Ungültige Signaturen", "Signatures invalides", "Firme non valide", "無効な署名", "无效签名", "Assinaturas inválidas"),
    "sn_k_hyg": ("Hygiene gaps", "Huecos de higiene", "Hygienelücken", "Lacunes d'hygiène", "Lacune di igiene", "衛生上の不備", "规范缺口", "Falhas de higiene"),
    "sn_k_min": ("Computing, 24 h (approx.)", "Cómputo 24 h (aprox.)", "Rechenzeit 24 h (ca.)", "Calcul 24 h (approx.)", "Calcolo 24 h (appross.)", "計算時間 24時間(概算)", "计算用量 24 小时(约)", "Cálculo 24 h (aprox.)"),
    "sn_k_read": ("Repositories read", "Repositorios leídos", "Gelesene Repositorys", "Dépôts lus", "Repository letti", "読み取ったリポジトリ", "已读取仓库", "Repositórios lidos"),
    "sn_of": ("{n} of {m}", "{n} de {m}", "{n} von {m}", "{n} sur {m}", "{n} su {m}", "{m} 件中 {n} 件", "{m} 个中的 {n} 个", "{n} de {m}"),
    "sn_min": ("{n} min", "{n} min", "{n} Min.", "{n} min", "{n} min", "{n} 分", "{n} 分钟", "{n} min"),
    "sn_ago_min": ("{n} min ago", "hace {n} min", "vor {n} Min.", "il y a {n} min", "{n} min fa", "{n} 分前", "{n} 分钟前", "há {n} min"),
    "sn_ago_h": ("{n} h ago", "hace {n} h", "vor {n} Std.", "il y a {n} h", "{n} h fa", "{n} 時間前", "{n} 小时前", "há {n} h"),
    "sn_ago_d": ("{n} d ago", "hace {n} d", "vor {n} T.", "il y a {n} j", "{n} g fa", "{n} 日前", "{n} 天前", "há {n} d"),
    "sn_ci_title": ("Builds on the main branch", "Compilaciones en la rama principal", "Builds auf dem Hauptzweig", "Builds sur la branche principale", "Build sul ramo principale", "メインブランチのビルド", "主分支构建", "Compilações no ramo principal"),
    "sn_ci_none": ("No red workflow.", "Ningún flujo en rojo.", "Kein roter Workflow.", "Aucun workflow en rouge.", "Nessun workflow in rosso.", "赤のワークフローはありません。", "没有红色工作流。", "Nenhum fluxo a vermelho."),
    "sn_ci_summary": ("{n} workflows checked in {m} repositories.", "{n} flujos comprobados en {m} repositorios.", "{n} Workflows in {m} Repositorys geprüft.", "{n} workflows vérifiés dans {m} dépôts.",
                      "{n} workflow controllati in {m} repository.", "{m} 件のリポジトリで {n} 件のワークフローを確認しました。", "已检查 {m} 个仓库中的 {n} 个工作流。", "{n} fluxos verificados em {m} repositórios."),
    "sn_col_repo": ("Repository", "Repositorio", "Repository", "Dépôt", "Repository", "リポジトリ", "仓库", "Repositório"),
    "sn_col_wf": ("Workflow file", "Fichero del flujo", "Workflow-Datei", "Fichier du workflow", "File del workflow", "ワークフローファイル", "工作流文件", "Ficheiro do fluxo"),
    "sn_col_streak": ("In a row", "Seguidos", "In Folge", "D'affilée", "Di fila", "連続", "连续", "Seguidos"),
    "sn_col_since": ("Red since", "En rojo desde", "Rot seit", "Rouge depuis", "Rosso da", "赤になった時期", "红色起始", "A vermelho desde"),
    "sn_col_entries": ("Entries", "Entradas", "Einträge", "Entrées", "Voci", "項目", "条目", "Entradas"),
    "sn_col_last": ("Last release", "Última versión", "Letzte Version", "Dernière version", "Ultima versione", "最新リリース", "最新版本", "Última versão"),
    "sn_col_min24": ("24 h", "24 h", "24 Std.", "24 h", "24 h", "24時間", "24 小时", "24 h"),
    "sn_col_min7": ("7 days", "7 días", "7 Tage", "7 jours", "7 giorni", "7日間", "7 天", "7 dias"),
    "sn_rel_title": ("Releases ready", "Versiones listas", "Bereite Versionen", "Versions prêtes", "Versioni pronte", "公開準備済みのバージョン", "可发布版本", "Versões prontas"),
    "sn_rel_rule": (
        "Rule: at least {n} entry under [Unreleased] in the CHANGELOG and a last release older than {d} days (or none).",
        "Regla: al menos {n} entrada en [Unreleased] del CHANGELOG y una última versión de hace más de {d} días (o ninguna).",
        "Regel: mindestens {n} Eintrag unter [Unreleased] im CHANGELOG und eine letzte Version, die älter als {d} Tage ist (oder keine).",
        "Règle : au moins {n} entrée sous [Unreleased] dans le CHANGELOG et une dernière version de plus de {d} jours (ou aucune).",
        "Regola: almeno {n} voce in [Unreleased] del CHANGELOG e un'ultima versione di oltre {d} giorni (o nessuna).",
        "ルール: CHANGELOG の [Unreleased] に {n} 件以上の項目があり、最新リリースが {d} 日より前(またはなし)であること。",
        "规则:CHANGELOG 的 [Unreleased] 下至少有 {n} 条记录,且最近一次发布超过 {d} 天(或尚无发布)。",
        "Regra: pelo menos {n} entrada em [Unreleased] do CHANGELOG e uma última versão com mais de {d} dias (ou nenhuma)."),
    "sn_rel_none": ("No repository is waiting for a version.", "Ningún repositorio espera versión.", "Kein Repository wartet auf eine Version.", "Aucun dépôt n'attend de version.",
                    "Nessun repository attende una versione.", "バージョンを待っているリポジトリはありません。", "没有仓库在等待发布版本。", "Nenhum repositório espera versão."),
    "sn_rel_never": ("no release", "sin versión", "keine Version", "aucune version", "nessuna versione", "リリースなし", "无发布", "sem versão"),
    "sn_sig_title": ("Signature of the latest releases", "Firma de las últimas versiones", "Signatur der letzten Versionen", "Signature des dernières versions", "Firma delle ultime versioni", "最新リリースの署名", "最新版本的签名", "Assinatura das últimas versões"),
    "sn_sig_verified": ("Verified", "Verificada", "Geprüft", "Vérifiée", "Verificata", "検証済み", "已验证", "Verificada"),
    "sn_sig_invalid": ("Invalid", "Inválida", "Ungültig", "Invalide", "Non valida", "無効", "无效", "Inválida"),
    "sn_sig_unverifiable": ("Not verifiable here", "No verificable aquí", "Hier nicht prüfbar", "Non vérifiable ici", "Non verificabile qui", "ここでは検証不可", "此处无法验证", "Não verificável aqui"),
    "sn_sig_none": ("No signature", "Sin firma", "Keine Signatur", "Sans signature", "Senza firma", "署名なし", "无签名", "Sem assinatura"),
    "sn_sig_norelease": ("No release", "Sin versión", "Keine Version", "Sans version", "Senza versione", "リリースなし", "无发布", "Sem versão"),
    "sn_sig_unverified": ("Not verified", "No verificado", "Nicht geprüft", "Non vérifié", "Non verificato", "未検証", "未验证", "Não verificado"),
    "sn_sig_bad_note": ("Do not install: {list}", "No instalar: {list}", "Nicht installieren: {list}", "Ne pas installer : {list}", "Non installare: {list}", "インストールしないでください: {list}", "请勿安装:{list}", "Não instalar: {list}"),
    "sn_hyg_title": ("Public hygiene", "Higiene pública", "Öffentliche Hygiene", "Hygiène publique", "Igiene pubblica", "公開リポジトリの衛生状態", "公开仓库规范", "Higiene pública"),
    "sn_hyg_ruleset": (
        "Active ruleset protecting the main branch: {n} of {m} repositories read.",
        "Ruleset activo que protege la rama principal: {n} de {m} repositorios leídos.",
        "Aktives Regelwerk für den Hauptzweig: {n} von {m} gelesenen Repositorys.",
        "Ruleset actif protégeant la branche principale : {n} dépôts sur {m} lus.",
        "Ruleset attivo che protegge il ramo principale: {n} repository su {m} letti.",
        "メインブランチを保護する有効なルールセット: 読み取った {m} 件中 {n} 件。",
        "保护主分支的有效规则集:已读取的 {m} 个仓库中有 {n} 个。",
        "Ruleset ativo a proteger o ramo principal: {n} de {m} repositórios lidos."),
    "sn_hyg_missing": ("Missing in: {list}", "Falta en: {list}", "Fehlt in: {list}", "Absent dans : {list}", "Manca in: {list}", "ないリポジトリ: {list}", "缺少于:{list}", "Falta em: {list}"),
    "sn_hyg_settings": (
        "Actions settings (actions pinned by SHA, allowed actions): readable in {n} of {m} repositories. The settings need the admin right, so the rest are not verified, never shown as in order.",
        "Ajustes de Actions (acciones fijadas por SHA, acciones permitidas): legibles en {n} de {m} repositorios. Los ajustes exigen el derecho de administrador, así que el resto queda sin verificar, nunca como en orden.",
        "Actions-Einstellungen (per SHA fixierte Actions, erlaubte Actions): lesbar in {n} von {m} Repositorys. Die Einstellungen brauchen Administratorrechte; der Rest ist nicht geprüft und wird nie als in Ordnung gezeigt.",
        "Réglages d'Actions (actions figées par SHA, actions autorisées) : lisibles dans {n} dépôts sur {m}. Les réglages exigent le droit d'administrateur ; le reste n'est pas vérifié et jamais affiché comme en ordre.",
        "Impostazioni di Actions (azioni fissate per SHA, azioni consentite): leggibili in {n} repository su {m}. Le impostazioni richiedono il diritto di amministratore; il resto non è verificato e mai mostrato come in ordine.",
        "Actions の設定(SHA 固定、許可されたアクション): {m} 件中 {n} 件で読み取れました。設定には管理者権限が必要なため、残りは未検証で、正常とは表示しません。",
        "Actions 设置(按 SHA 固定的动作、允许的动作):{m} 个仓库中有 {n} 个可读取。设置需要管理员权限,其余未验证,绝不显示为正常。",
        "Definições do Actions (ações fixadas por SHA, ações permitidas): legíveis em {n} de {m} repositórios. As definições exigem o direito de administrador, por isso o resto fica por verificar, nunca como em ordem."),
    "sn_hyg_sha": ("SHA pinning not required: {list}", "Sin exigir fijar por SHA: {list}", "SHA-Fixierung nicht erzwungen: {list}", "Figement par SHA non exigé : {list}", "Fissaggio SHA non richiesto: {list}", "SHA 固定が必須でない: {list}", "未强制按 SHA 固定:{list}", "Sem exigir fixação por SHA: {list}"),
    "sn_hyg_allowed": ("Not limited to selected actions: {list}", "Sin limitar a acciones seleccionadas: {list}", "Nicht auf ausgewählte Actions beschränkt: {list}", "Non limité aux actions sélectionnées : {list}",
                       "Non limitato alle azioni selezionate: {list}", "選択したアクションに限定されていない: {list}", "未限制为所选动作:{list}", "Sem limitar a ações selecionadas: {list}"),
    "sn_hyg_ok": ("No gap found in what could be read.", "Ningún hueco en lo que se pudo leer.", "Keine Lücke in dem, was gelesen werden konnte.", "Aucune lacune dans ce qui a pu être lu.",
                  "Nessuna lacuna in ciò che si è potuto leggere.", "読み取れた範囲で不備はありません。", "已读取的内容中未发现缺口。", "Nenhuma falha no que se pôde ler."),
    "sn_cmp_title": ("Computing (approx.)", "Cómputo (aprox.)", "Rechenzeit (ca.)", "Calcul (approx.)", "Calcolo (appross.)", "計算時間(概算)", "计算用量(约)", "Cálculo (aprox.)"),
    "sn_cmp_total": ("Total: {a} min in 24 h, {b} min in 7 days", "Total: {a} min en 24 h, {b} min en 7 días", "Gesamt: {a} Min. in 24 Std., {b} Min. in 7 Tagen", "Total : {a} min en 24 h, {b} min en 7 jours",
                     "Totale: {a} min in 24 h, {b} min in 7 giorni", "合計: 24時間で {a} 分、7日間で {b} 分", "合计:24 小时 {a} 分钟,7 天 {b} 分钟", "Total: {a} min em 24 h, {b} min em 7 dias"),
    "sn_cmp_none": ("No computing recorded in the last 7 days.", "Sin cómputo registrado en los últimos 7 días.", "Keine Rechenzeit in den letzten 7 Tagen erfasst.", "Aucun calcul enregistré sur les 7 derniers jours.",
                    "Nessun calcolo registrato negli ultimi 7 giorni.", "直近7日間の計算時間の記録はありません。", "最近 7 天没有计算用量记录。", "Sem cálculo registado nos últimos 7 dias."),
    "sn_cmp_row": ("{repo}: {a} min in 24 h, {b} min in 7 days", "{repo}: {a} min en 24 h, {b} min en 7 días", "{repo}: {a} Min. in 24 Std., {b} Min. in 7 Tagen", "{repo} : {a} min en 24 h, {b} min en 7 jours",
                   "{repo}: {a} min in 24 h, {b} min in 7 giorni", "{repo}: 24時間で {a} 分、7日間で {b} 分", "{repo}:24 小时 {a} 分钟,7 天 {b} 分钟", "{repo}: {a} min em 24 h, {b} min em 7 dias"),
    "sn_trend_title": ("Daily trend", "Tendencia diaria", "Täglicher Verlauf", "Tendance quotidienne", "Andamento giornaliero", "日次の推移", "每日趋势", "Tendência diária"),
    "sn_trend_none": ("Fewer than two days recorded so far.", "Aún hay menos de dos días registrados.", "Bisher weniger als zwei Tage erfasst.", "Moins de deux jours enregistrés pour l'instant.",
                      "Finora meno di due giorni registrati.", "記録はまだ2日未満です。", "目前记录不足两天。", "Ainda há menos de dois dias registados."),
    "sn_trend_row": ("{name}: now {last}, from {min} to {max}; {values} (from {from} to {to})", "{name}: ahora {last}, de {min} a {max}; {values} (del {from} al {to})",
                     "{name}: jetzt {last}, von {min} bis {max}; {values} (vom {from} bis {to})", "{name} : maintenant {last}, de {min} à {max} ; {values} (du {from} au {to})",
                     "{name}: ora {last}, da {min} a {max}; {values} (dal {from} al {to})", "{name}: 現在 {last}、{min} から {max}。{values}({from} から {to})",
                     "{name}:当前 {last},范围 {min} 至 {max};{values}({from} 至 {to})", "{name}: agora {last}, de {min} a {max}; {values} (de {from} a {to})"),
    "sn_t_red": ("Red workflows", "Flujos en rojo", "Rote Workflows", "Workflows en rouge", "Workflow in rosso", "赤のワークフロー", "红色工作流", "Fluxos a vermelho"),
    "sn_t_cand": ("Releases ready", "Versiones listas", "Bereite Versionen", "Versions prêtes", "Versioni pronte", "公開準備済み", "可发布版本", "Versões prontas"),
    "sn_t_gaps": ("Hygiene gaps", "Huecos de higiene", "Hygienelücken", "Lacunes d'hygiène", "Lacune di igiene", "衛生上の不備", "规范缺口", "Falhas de higiene"),
    "sn_t_min": ("Computing minutes, 24 h", "Minutos de cómputo, 24 h", "Rechenminuten, 24 Std.", "Minutes de calcul, 24 h", "Minuti di calcolo, 24 h", "計算時間(分)24時間", "计算分钟数,24 小时", "Minutos de cálculo, 24 h"),
    "sn_excl_title": ("What this tab never shows", "Lo que esta pestaña nunca muestra", "Was dieser Tab nie zeigt", "Ce que cet onglet n'affiche jamais", "Ciò che questa scheda non mostra mai", "このタブが決して表示しないもの", "此标签页从不显示的内容", "O que este separador nunca mostra"),
    "sn_excl_body": (
        "Security alerts (code scanning, dependencies and secrets, not even a count), titles of pull requests and issues, people, branches and texts written by outsiders. They are left out on purpose so that nothing sensitive is published.",
        "Alertas de seguridad (análisis de código, dependencias y secretos, ni siquiera un recuento), títulos de pull requests e issues, personas, ramas y textos escritos por terceros. Se dejan fuera a propósito para no publicar nada sensible.",
        "Sicherheitswarnungen (Codeanalyse, Abhängigkeiten und Geheimnisse, nicht einmal eine Anzahl), Titel von Pull Requests und Issues, Personen, Branches und von Außenstehenden verfasste Texte. Sie fehlen absichtlich, damit nichts Sensibles veröffentlicht wird.",
        "Alertes de sécurité (analyse de code, dépendances et secrets, pas même un nombre), titres de pull requests et d'issues, personnes, branches et textes écrits par des tiers. Elles sont exclues volontairement pour ne rien publier de sensible.",
        "Avvisi di sicurezza (analisi del codice, dipendenze e segreti, nemmeno un conteggio), titoli di pull request e issue, persone, rami e testi scritti da esterni. Sono esclusi di proposito per non pubblicare nulla di sensibile.",
        "セキュリティアラート(コードスキャン、依存関係、シークレット。件数も含む)、プルリクエストや Issue のタイトル、個人、ブランチ、外部の人が書いた文章。機密情報を公開しないよう、意図的に除外しています。",
        "安全警报(代码扫描、依赖项和机密,连数量也不显示)、拉取请求和议题的标题、个人、分支以及外部人员撰写的文本。为避免公开任何敏感信息,有意不显示。",
        "Alertas de segurança (análise de código, dependências e segredos, nem sequer uma contagem), títulos de pull requests e issues, pessoas, ramos e textos escritos por terceiros. Ficam de fora de propósito para não publicar nada sensível."),
    "sn_help_summary": ("How it is calculated", "Cómo se calcula", "Wie es berechnet wird", "Comment c'est calculé", "Come si calcola", "計算方法", "计算方式", "Como se calcula"),
    "sn_help_body": (
        "Red: the last finished run of each workflow on the default branch decides (cancelled and skipped runs do not count; only the latest 100 finished runs are read, and workflows that no longer exist are ignored). Releases ready: the rule shown in its card. Signatures: the result of the verification done when the page was generated. Hygiene: the public rulesets, plus the Actions settings when the token may read them. Computing: wall-clock time of the finished runs, not the minutes GitHub bills. A repository that could not be read is shown as not verified, never as in order. Everything is decided by fixed rules; there is no AI.",
        "Rojo: decide el último run terminado de cada flujo en la rama por defecto (los cancelados y omitidos no cuentan; solo se leen los 100 últimos runs terminados y se ignoran los flujos que ya no existen). Versiones listas: la regla de su tarjeta. Firmas: el resultado de la verificación hecha al generar la página. Higiene: los rulesets públicos y, si el token puede leerlos, los ajustes de Actions. Cómputo: tiempo de reloj de los runs terminados, no los minutos que factura GitHub. Un repositorio que no se pudo leer se muestra como no verificado, nunca como en orden. Todo lo deciden reglas fijas; no hay IA.",
        "Rot: Der letzte beendete Lauf jedes Workflows auf dem Standardzweig entscheidet (abgebrochene und übersprungene zählen nicht; es werden nur die letzten 100 beendeten Läufe gelesen, nicht mehr vorhandene Workflows werden ignoriert). Bereite Versionen: die Regel in ihrer Karte. Signaturen: das Ergebnis der Prüfung bei der Erzeugung der Seite. Hygiene: die öffentlichen Regelwerke und, wenn der Token sie lesen darf, die Actions-Einstellungen. Rechenzeit: Uhrzeit der beendeten Läufe, nicht die von GitHub abgerechneten Minuten. Ein nicht lesbares Repository gilt als nicht geprüft, nie als in Ordnung. Alles entscheiden feste Regeln; es gibt keine KI.",
        "Rouge : le dernier run terminé de chaque workflow sur la branche par défaut décide (annulés et ignorés ne comptent pas ; seuls les 100 derniers runs terminés sont lus et les workflows disparus sont ignorés). Versions prêtes : la règle de sa carte. Signatures : le résultat de la vérification faite à la génération de la page. Hygiène : les rulesets publics et, si le jeton peut les lire, les réglages d'Actions. Calcul : durée réelle des runs terminés, pas les minutes facturées par GitHub. Un dépôt illisible est affiché comme non vérifié, jamais comme en ordre. Tout est décidé par des règles fixes ; il n'y a pas d'IA.",
        "Rosso: decide l'ultima esecuzione conclusa di ogni workflow sul ramo predefinito (annullate e saltate non contano; si leggono solo le ultime 100 esecuzioni concluse e i workflow non più esistenti sono ignorati). Versioni pronte: la regola nella sua scheda. Firme: il risultato della verifica fatta alla generazione della pagina. Igiene: i ruleset pubblici e, se il token può leggerle, le impostazioni di Actions. Calcolo: tempo reale delle esecuzioni concluse, non i minuti fatturati da GitHub. Un repository non leggibile appare come non verificato, mai come in ordine. Tutto è deciso da regole fisse; non c'è IA.",
        "赤: 各ワークフローの、デフォルトブランチで最後に終了した実行が判定します(キャンセルとスキップは対象外。読み取るのは直近100件の終了済み実行のみで、存在しないワークフローは無視します)。公開準備済み: カードに示したルール。署名: ページ生成時に行った検証の結果。衛生状態: 公開ルールセットと、トークンで読める場合は Actions の設定。計算時間: 終了した実行の実時間で、GitHub が課金する分ではありません。読み取れなかったリポジトリは未検証と表示し、正常とは表示しません。すべて固定ルールで判定し、AI は使いません。",
        "红色:以每个工作流在默认分支上最后一次已结束的运行为准(已取消和已跳过的不计;只读取最近 100 次已结束的运行,已不存在的工作流会被忽略)。可发布版本:见其卡片中的规则。签名:生成页面时所做验证的结果。规范:公开的规则集,以及令牌可读取时的 Actions 设置。计算用量:已结束运行的实际耗时,并非 GitHub 计费的分钟数。无法读取的仓库显示为未验证,绝不显示为正常。一切由固定规则判定,不使用 AI。",
        "Vermelho: decide a última execução terminada de cada fluxo no ramo por omissão (as canceladas e ignoradas não contam; só se leem as últimas 100 execuções terminadas e ignoram-se os fluxos que já não existem). Versões prontas: a regra do seu cartão. Assinaturas: o resultado da verificação feita ao gerar a página. Higiene: os rulesets públicos e, se o token os puder ler, as definições do Actions. Cálculo: tempo real das execuções terminadas, não os minutos faturados pelo GitHub. Um repositório que não se pôde ler aparece como não verificado, nunca como em ordem. Tudo é decidido por regras fixas; não há IA."),
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
