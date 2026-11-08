#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_robust_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Texts of the keyboard help, the breadcrumb, the figures of the generation, the last known data and the URTC rack page, in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    # ---- Keyboard help ----
    "help_open": ("Keyboard shortcuts", "Atajos de teclado", "Tastenkürzel", "Raccourcis clavier", "Scorciatoie da tastiera", "キーボードショートカット", "键盘快捷键", "Atalhos de teclado"),
    "help_open_title": ("Keyboard shortcuts (press ?)", "Atajos de teclado (pulsa ?)", "Tastenkürzel (? drücken)", "Raccourcis clavier (touche ?)", "Scorciatoie da tastiera (premi ?)", "キーボードショートカット(? キー)", "键盘快捷键(按 ?)", "Atalhos de teclado (prima ?)"),
    "help_intro": (
        "Single keys work anywhere on the page except while you type in a field. They never replace the keys of your browser or of your screen reader, and you can turn them off below.",
        "Las teclas sueltas funcionan en toda la página salvo mientras escribes en un campo. Nunca sustituyen a las teclas del navegador ni del lector de pantalla, y puedes desactivarlas abajo.",
        "Einzelne Tasten funktionieren überall auf der Seite, außer beim Tippen in einem Feld. Sie ersetzen nie die Tasten Ihres Browsers oder Screenreaders und lassen sich unten abschalten.",
        "Les touches seules fonctionnent partout sur la page, sauf pendant la saisie dans un champ. Elles ne remplacent jamais les touches du navigateur ni du lecteur d'écran, et vous pouvez les désactiver ci-dessous.",
        "I tasti singoli funzionano ovunque nella pagina tranne mentre scrivi in un campo. Non sostituiscono mai i tasti del browser o dello screen reader e puoi disattivarli qui sotto.",
        "単独のキーは、入力欄に入力している間を除き、ページのどこでも使えます。ブラウザーやスクリーンリーダーのキーを置き換えることはなく、下で無効にできます。",
        "单个按键在页面任何位置都有效,但在输入框中输入时除外。它们不会取代浏览器或屏幕阅读器的按键,并且可以在下方关闭。",
        "As teclas simples funcionam em toda a página, exceto enquanto escreve num campo. Nunca substituem as teclas do navegador nem do leitor de ecrã e pode desativá-las abaixo.",
    ),
    "help_col_key": ("Key", "Tecla", "Taste", "Touche", "Tasto", "キー", "按键", "Tecla"),
    "help_col_action": ("Action", "Acción", "Aktion", "Action", "Azione", "動作", "操作", "Ação"),
    "help_k_search": ("Focus the search box", "Ir al cuadro de búsqueda", "Zum Suchfeld springen", "Aller à la zone de recherche", "Vai alla casella di ricerca", "検索欄に移動", "跳到搜索框", "Ir para a caixa de pesquisa"),
    "help_k_eco": ("Open HYDRA-UMC, URTC, A.R.M.O.R. or EH3D", "Abrir HYDRA-UMC, URTC, A.R.M.O.R. o EH3D", "HYDRA-UMC, URTC, A.R.M.O.R. oder EH3D öffnen", "Ouvrir HYDRA-UMC, URTC, A.R.M.O.R. ou EH3D", "Apri HYDRA-UMC, URTC, A.R.M.O.R. o EH3D", "HYDRA-UMC、URTC、A.R.M.O.R.、EH3D を開く", "打开 HYDRA-UMC、URTC、A.R.M.O.R. 或 EH3D", "Abrir HYDRA-UMC, URTC, A.R.M.O.R. ou EH3D"),
    "help_k_summary": ("Open the summary", "Abrir el resumen", "Übersicht öffnen", "Ouvrir le résumé", "Apri il riepilogo", "概要を開く", "打开概览", "Abrir o resumo"),
    "help_k_help": ("Open or close this help", "Abrir o cerrar esta ayuda", "Diese Hilfe öffnen oder schließen", "Ouvrir ou fermer cette aide", "Apri o chiudi questa guida", "このヘルプを開く/閉じる", "打开或关闭此帮助", "Abrir ou fechar esta ajuda"),
    "help_k_compact": ("Switch the compact mode", "Alternar el modo compacto", "Kompaktmodus umschalten", "Basculer le mode compact", "Attiva o disattiva la modalità compatta", "コンパクト表示を切り替え", "切换紧凑模式", "Alternar o modo compacto"),
    "help_k_present": ("Switch the presentation mode", "Alternar el modo presentación", "Präsentationsmodus umschalten", "Basculer le mode présentation", "Attiva o disattiva la modalità presentazione", "プレゼンテーション表示を切り替え", "切换演示模式", "Alternar o modo de apresentação"),
    "help_k_tabs": ("Move between the tabs (with a tab focused)", "Moverse entre las pestañas (con una pestaña enfocada)", "Zwischen den Tabs wechseln (bei fokussiertem Tab)", "Se déplacer entre les onglets (onglet sélectionné)", "Spostarsi tra le schede (con una scheda attiva)", "タブ間を移動(タブにフォーカス中)", "在标签页之间移动(焦点在标签页上时)", "Mover entre os separadores (com um separador em foco)"),
    "help_k_esc": ("Close the help, the repository panel or the presentation mode", "Cerrar la ayuda, el panel del repositorio o el modo presentación", "Hilfe, Repository-Panel oder Präsentationsmodus schließen", "Fermer l'aide, le panneau du dépôt ou le mode présentation", "Chiudi la guida, il pannello del repository o la modalità presentazione", "ヘルプ、リポジトリのパネル、プレゼンテーション表示を閉じる", "关闭帮助、仓库面板或演示模式", "Fechar a ajuda, o painel do repositório ou o modo de apresentação"),
    "help_toggle": ("Single-key shortcuts are on", "Atajos de una sola tecla activados", "Einzeltasten-Kürzel sind aktiv", "Raccourcis à une touche activés", "Scorciatoie a tasto singolo attive", "単独キーのショートカットを有効にする", "启用单键快捷键", "Atalhos de uma só tecla ativados"),
    "help_close": ("Close", "Cerrar", "Schließen", "Fermer", "Chiudi", "閉じる", "关闭", "Fechar"),
    # ---- Breadcrumb ----
    "crumb_label": ("You are here", "Dónde estás", "Sie sind hier", "Vous êtes ici", "Sei qui", "現在地", "当前位置", "Está aqui"),
    "crumb_home": ("Dashboard", "Panel", "Dashboard", "Tableau de bord", "Pannello", "ダッシュボード", "仪表盘", "Painel"),
    # ---- Manifest health card ----
    "registry_sub": ("{ok} of {repos} valid", "{ok} de {repos} válidos", "{ok} von {repos} gültig", "{ok} sur {repos} valides", "{ok} su {repos} validi", "{repos} 件中 {ok} 件が有効", "{repos} 个中 {ok} 个有效", "{ok} de {repos} válidos"),
    "registry_help": (
        "How it is calculated: valid manifests divided by repositories. A repository counts as valid when its manifest was read and declares a known maturity and evidence. A repository whose manifest cannot be read, or has a manifest that was not listed, counts in the total but not as valid. It is the same set of problems as the Errors / unknown indicator.",
        "Cómo se calcula: manifiestos válidos dividido entre repositorios. Un repositorio cuenta como válido cuando se leyó su manifiesto y declara una madurez y una evidencia conocidas. Un repositorio cuyo manifiesto no se puede leer, o que tiene un manifiesto sin listar, cuenta en el total pero no como válido. Son los mismos problemas que cuenta el indicador de Errores / desconocido.",
        "So wird es berechnet: gültige Manifeste geteilt durch Repositorys. Ein Repository gilt als gültig, wenn sein Manifest gelesen wurde und einen bekannten Reifegrad und Nachweis erklärt. Ein Repository mit nicht lesbarem oder nicht gelistetem Manifest zählt zur Gesamtzahl, aber nicht als gültig. Es sind dieselben Probleme wie bei der Anzeige Fehler / unbekannt.",
        "Calcul : manifestes valides divisés par les dépôts. Un dépôt est valide quand son manifeste a été lu et déclare une maturité et des preuves connues. Un dépôt dont le manifeste est illisible, ou dont le manifeste n'a pas été listé, compte dans le total mais pas comme valide. Ce sont les mêmes problèmes que ceux de l'indicateur Erreurs / inconnu.",
        "Come si calcola: manifesti validi divisi per i repository. Un repository è valido quando il suo manifesto è stato letto e dichiara una maturità e un'evidenza note. Un repository con manifesto illeggibile, o con un manifesto non elencato, conta nel totale ma non come valido. Sono gli stessi problemi dell'indicatore Errori / sconosciuto.",
        "計算方法:有効なマニフェストの数 ÷ リポジトリ数。マニフェストが読み取れ、既知の成熟度とエビデンスを宣言しているリポジトリを有効とみなします。マニフェストが読めない、または未掲載のリポジトリは、合計には入りますが有効には数えません。「エラー / 不明」の指標と同じ問題を対象にしています。",
        "计算方式:有效清单数除以仓库数。仓库的清单已读取并声明了已知的成熟度和证据时,才算有效。清单无法读取或清单未列出的仓库计入总数,但不算有效。问题范围与“错误 / 未知”指标一致。",
        "Como é calculado: manifestos válidos a dividir pelos repositórios. Um repositório conta como válido quando o seu manifesto foi lido e declara uma maturidade e uma evidência conhecidas. Um repositório cujo manifesto não se consegue ler, ou que tem um manifesto por listar, conta no total mas não como válido. São os mesmos problemas do indicador Erros / desconhecido.",
    ),
    # ---- Generation figures and last known data ----
    "gen_title": ("Generation of this page", "Generación de esta página", "Erzeugung dieser Seite", "Génération de cette page", "Generazione di questa pagina", "このページの生成", "本页面的生成情况", "Geração desta página"),
    "gen_built": (
        "Generated {when} UTC in {seconds} s (the latest generation that changed the page).",
        "Generada el {when} UTC en {seconds} s (la última generación que cambió la página).",
        "Erzeugt am {when} UTC in {seconds} s (die letzte Erzeugung, die die Seite verändert hat).",
        "Générée le {when} UTC en {seconds} s (la dernière génération qui a modifié la page).",
        "Generata il {when} UTC in {seconds} s (l'ultima generazione che ha cambiato la pagina).",
        "{when} UTC に {seconds} 秒で生成(ページを変更した直近の生成)。",
        "于 {when} UTC 生成,用时 {seconds} 秒(最近一次改变页面的生成)。",
        "Gerada em {when} UTC em {seconds} s (a última geração que alterou a página).",
    ),
    "gen_step_versions": ("Versions resolved: {ok} of {total} repositories", "Versiones resueltas: {ok} de {total} repositorios", "Aufgelöste Versionen: {ok} von {total} Repositorys", "Versions résolues : {ok} dépôts sur {total}", "Versioni risolte: {ok} repository su {total}", "バージョンを取得できたリポジトリ: {total} 件中 {ok} 件", "已解析版本:{total} 个仓库中的 {ok} 个", "Versões resolvidas: {ok} de {total} repositórios"),
    "gen_step_manifests": ("Valid manifests: {ok} of {total} repositories", "Manifiestos válidos: {ok} de {total} repositorios", "Gültige Manifeste: {ok} von {total} Repositorys", "Manifestes valides : {ok} dépôts sur {total}", "Manifesti validi: {ok} repository su {total}", "有効なマニフェスト: {total} 件中 {ok} 件", "有效清单:{total} 个仓库中的 {ok} 个", "Manifestos válidos: {ok} de {total} repositórios"),
    "gen_step_commits": ("Last-commit lookups answered: {ok} of {total}", "Consultas del último commit respondidas: {ok} de {total}", "Beantwortete Abfragen des letzten Commits: {ok} von {total}", "Requêtes du dernier commit abouties : {ok} sur {total}", "Richieste dell'ultimo commit riuscite: {ok} su {total}", "最新コミットの取得に成功: {total} 件中 {ok} 件", "最新提交查询成功:{total} 个中的 {ok} 个", "Consultas do último commit respondidas: {ok} de {total}"),
    "gen_step_activity": ("CI and release records read: {ok} of {total} repositories", "Registros de CI y versiones leídos: {ok} de {total} repositorios", "Gelesene CI- und Release-Daten: {ok} von {total} Repositorys", "Données de CI et de versions lues : {ok} dépôts sur {total}", "Dati di CI e versioni letti: {ok} repository su {total}", "CI とリリースの情報を取得: {total} 件中 {ok} 件", "已读取 CI 与发布记录:{total} 个仓库中的 {ok} 个", "Registos de CI e versões lidos: {ok} de {total} repositórios"),
    "gen_errors_hint": (
        "The exact reason of every manifest that could not be read, of every lookup that failed and of every GitHub failure is listed by repository below.",
        "El motivo exacto de cada manifiesto que no se pudo leer, de cada consulta fallida y de cada fallo de GitHub se lista a continuación por repositorio.",
        "Der genaue Grund jedes nicht lesbaren Manifests, jeder fehlgeschlagenen Abfrage und jedes GitHub-Fehlers steht unten je Repository.",
        "La raison exacte de chaque manifeste illisible, de chaque requête échouée et de chaque échec de GitHub est listée ci-dessous par dépôt.",
        "Il motivo esatto di ogni manifesto non leggibile, di ogni richiesta fallita e di ogni errore di GitHub è elencato qui sotto per repository.",
        "読み取れなかったマニフェスト、失敗した取得、GitHub の障害の正確な理由を、下でリポジトリごとに一覧しています。",
        "无法读取的清单、失败的查询以及 GitHub 故障的具体原因,在下方按仓库逐一列出。",
        "O motivo exato de cada manifesto que não se conseguiu ler, de cada consulta falhada e de cada falha do GitHub está listado abaixo por repositório.",
    ),
    "gen_unknown": ("The figures of the generation are not available in this page.", "Las cifras de la generación no están disponibles en esta página.", "Die Zahlen der Erzeugung sind in dieser Seite nicht verfügbar.", "Les chiffres de la génération ne sont pas disponibles dans cette page.", "I dati della generazione non sono disponibili in questa pagina.", "このページには生成時の数値がありません。", "本页面没有生成时的数据。", "Os números da geração não estão disponíveis nesta página."),
    "stale_banner": (
        "Last known version of the CI, release and commit data, from {date}. GitHub could not be read in the latest generation, so these data are not current.",
        "Última versión conocida de los datos de CI, versiones y commits, del {date}. No se pudo leer GitHub en la última generación, así que estos datos no son actuales.",
        "Zuletzt bekannte Fassung der CI-, Release- und Commit-Daten vom {date}. GitHub konnte bei der letzten Erzeugung nicht gelesen werden, daher sind diese Daten nicht aktuell.",
        "Dernière version connue des données de CI, de versions et de commits, du {date}. GitHub n'a pas pu être lu lors de la dernière génération : ces données ne sont donc pas à jour.",
        "Ultima versione nota dei dati di CI, versioni e commit, del {date}. Non è stato possibile leggere GitHub nell'ultima generazione, quindi questi dati non sono attuali.",
        "CI・リリース・コミットのデータは {date} 時点の最後に確認できた版です。直近の生成で GitHub を読み取れなかったため、現在の状態ではありません。",
        "CI、发布和提交数据为 {date} 的最后已知版本。最近一次生成时无法读取 GitHub,因此这些数据并非当前数据。",
        "Última versão conhecida dos dados de CI, versões e commits, de {date}. Não foi possível ler o GitHub na última geração, por isso estes dados não são atuais.",
    ),
    "kept_banner": (
        "Last good version of this page, from {date}. GitHub could not be read in the latest generation (quota spent or no answer), so nothing here is newer than that.",
        "Última versión buena de esta página, del {date}. No se pudo leer GitHub en la última generación (cuota agotada o sin respuesta), así que nada de lo que ves es más reciente.",
        "Letzte gute Fassung dieser Seite vom {date}. GitHub konnte bei der letzten Erzeugung nicht gelesen werden (Kontingent aufgebraucht oder keine Antwort), nichts hier ist neuer.",
        "Dernière bonne version de cette page, du {date}. GitHub n'a pas pu être lu lors de la dernière génération (quota épuisé ou pas de réponse) : rien ici n'est plus récent.",
        "Ultima versione buona di questa pagina, del {date}. Non è stato possibile leggere GitHub nell'ultima generazione (quota esaurita o nessuna risposta): nulla qui è più recente.",
        "このページの最後の正常な版({date})です。直近の生成で GitHub を読み取れなかった(クォータ超過または応答なし)ため、これより新しい情報はありません。",
        "本页的最后一个正常版本,日期为 {date}。最近一次生成时无法读取 GitHub(配额用尽或无响应),因此这里没有更新的内容。",
        "Última versão boa desta página, de {date}. Não foi possível ler o GitHub na última geração (quota esgotada ou sem resposta), por isso nada aqui é mais recente.",
    ),
    "gen_http": (
        "Reads of GitHub: {made}; free thanks to ETag: {saved}; answered from the saved copy: {stale} (oldest {hours} h)",
        "Lecturas de GitHub: {made}; gratis gracias a ETag: {saved}; respondidas con la copia guardada: {stale} (la más antigua, {hours} h)",
        "Lesezugriffe auf GitHub: {made}; kostenlos dank ETag: {saved}; aus der gespeicherten Kopie beantwortet: {stale} (älteste {hours} Std.)",
        "Lectures de GitHub : {made} ; gratuites grâce à l'ETag : {saved} ; servies par la copie enregistrée : {stale} (la plus ancienne, {hours} h)",
        "Letture di GitHub: {made}; gratuite grazie all'ETag: {saved}; servite dalla copia salvata: {stale} (la più vecchia, {hours} h)",
        "GitHub の読み取り:{made} 回、ETag により無料:{saved} 回、保存コピーで応答:{stale} 回(最古 {hours} 時間)",
        "GitHub 读取:{made} 次;借助 ETag 免费:{saved} 次;由保存副本应答:{stale} 次(最旧 {hours} 小时)",
        "Leituras do GitHub: {made}; grátis graças ao ETag: {saved}; respondidas com a cópia guardada: {stale} (a mais antiga, {hours} h)",
    ),
    "alerts_why_activity_stale": (
        "The CI, release and commit data are the last known version from {date}, not current",
        "Los datos de CI, versiones y commits son la última versión conocida del {date}, no los actuales",
        "Die CI-, Release- und Commit-Daten sind die zuletzt bekannte Fassung vom {date}, nicht aktuell",
        "Les données de CI, de versions et de commits sont la dernière version connue du {date}, pas les actuelles",
        "I dati di CI, versioni e commit sono l'ultima versione nota del {date}, non quelli attuali",
        "CI・リリース・コミットのデータは {date} 時点の最後に確認できた版で、現在のものではありません",
        "CI、发布和提交数据是 {date} 的最后已知版本,并非当前数据",
        "Os dados de CI, versões e commits são a última versão conhecida de {date}, não os atuais",
    ),
    # ---- URTC rack page ----
    "tab_rack": ("Rack", "Rack", "Rack", "Rack", "Rack", "ラック", "机架", "Rack"),
    "rack_title": ("URTC tool rack", "Rack de herramientas URTC", "URTC-Werkzeugrack", "Rack d'outils URTC", "Rack utensili URTC", "URTC ツールラック", "URTC 工具机架", "Rack de ferramentas URTC"),
    "rack_intro": (
        "State of the tool rack as the snapshot of URTC-COMMON describes it: slots, heads, maintenance and alarms. This page only shows a published snapshot; it never reads a rack.",
        "Estado del rack de herramientas tal como lo describe la instantánea de URTC-COMMON: ranuras, cabezales, mantenimiento y alarmas. Esta página solo muestra una instantánea publicada; nunca lee un rack.",
        "Zustand des Werkzeugracks, wie ihn der Snapshot von URTC-COMMON beschreibt: Slots, Köpfe, Wartung und Alarme. Diese Seite zeigt nur einen veröffentlichten Snapshot; sie liest nie ein Rack.",
        "État du rack d'outils tel que le décrit l'instantané d'URTC-COMMON : emplacements, têtes, maintenance et alarmes. Cette page n'affiche qu'un instantané publié ; elle ne lit jamais un rack.",
        "Stato del rack utensili come lo descrive lo snapshot di URTC-COMMON: slot, teste, manutenzione e allarmi. Questa pagina mostra solo uno snapshot pubblicato; non legge mai un rack.",
        "URTC-COMMON のスナップショットが示すツールラックの状態(スロット、ヘッド、保守、アラーム)です。このページは公開済みのスナップショットを表示するだけで、ラックを読み取ることはありません。",
        "URTC-COMMON 快照所描述的工具机架状态:槽位、刀头、维护与告警。本页面仅显示已发布的快照,从不读取机架。",
        "Estado do rack de ferramentas tal como o descreve o instantâneo do URTC-COMMON: ranhuras, cabeças, manutenção e alarmes. Esta página só mostra um instantâneo publicado; nunca lê um rack.",
    ),
    "rack_source": ("Source: {source}", "Fuente: {source}", "Quelle: {source}", "Source : {source}", "Fonte: {source}", "出典: {source}", "来源:{source}", "Fonte: {source}"),
    "rack_source_sim": (
        "This is simulation data published as an example, not a real rack.",
        "Son datos de simulación publicados como ejemplo, no un rack real.",
        "Das sind als Beispiel veröffentlichte Simulationsdaten, kein echtes Rack.",
        "Ce sont des données de simulation publiées en exemple, pas un vrai rack.",
        "Sono dati di simulazione pubblicati come esempio, non un rack reale.",
        "これは例として公開されたシミュレーションのデータで、実際のラックではありません。",
        "这是作为示例发布的仿真数据,不是真实的机架。",
        "São dados de simulação publicados como exemplo, não um rack real.",
    ),
    "rack_nodata": (
        "No data: this page has no rack snapshot, so no state of any rack is shown.",
        "Sin datos: esta página no tiene ninguna instantánea de un rack, así que no se muestra el estado de ningún rack.",
        "Keine Daten: Diese Seite enthält keinen Rack-Snapshot, daher wird kein Rack-Zustand angezeigt.",
        "Sans données : cette page n'a aucun instantané de rack, aucun état de rack n'est donc affiché.",
        "Nessun dato: questa pagina non ha alcuno snapshot di un rack, quindi non viene mostrato lo stato di nessun rack.",
        "データなし: このページにはラックのスナップショットがないため、ラックの状態は表示されません。",
        "无数据:本页面没有机架快照,因此不显示任何机架状态。",
        "Sem dados: esta página não tem nenhum instantâneo de um rack, por isso não se mostra o estado de nenhum rack.",
    ),
    "rack_invalid": (
        "The published rack snapshot could not be used ({reason}), so no state is shown.",
        "No se pudo usar la instantánea publicada del rack ({reason}), así que no se muestra ningún estado.",
        "Der veröffentlichte Rack-Snapshot war nicht verwendbar ({reason}), daher wird kein Zustand angezeigt.",
        "L'instantané publié du rack était inutilisable ({reason}), aucun état n'est donc affiché.",
        "Lo snapshot pubblicato del rack non era utilizzabile ({reason}), quindi non viene mostrato alcuno stato.",
        "公開されたラックのスナップショットを利用できなかった({reason})ため、状態は表示されません。",
        "已发布的机架快照无法使用({reason}),因此不显示任何状态。",
        "Não foi possível usar o instantâneo publicado do rack ({reason}), por isso não se mostra nenhum estado.",
    ),
    "rack_state_ok": ("No alarms", "Sin alarmas", "Keine Alarme", "Aucune alarme", "Nessun allarme", "アラームなし", "无告警", "Sem alarmes"),
    "rack_state_alarm": ("Alarm", "Alarma", "Alarm", "Alarme", "Allarme", "アラーム", "告警", "Alarme"),
    "rack_state_nodata": ("No data", "Sin datos", "Keine Daten", "Sans données", "Nessun dato", "データなし", "无数据", "Sem dados"),
    "rack_summary": (
        "Slots in use: {used} of {slots} · heating: {heating} · maintenance due: {maintenance}",
        "Ranuras en uso: {used} de {slots} · calentando: {heating} · mantenimiento pendiente: {maintenance}",
        "Belegte Slots: {used} von {slots} · heizend: {heating} · Wartung fällig: {maintenance}",
        "Emplacements utilisés : {used} sur {slots} · en chauffe : {heating} · maintenance due : {maintenance}",
        "Slot in uso: {used} su {slots} · in riscaldamento: {heating} · manutenzione dovuta: {maintenance}",
        "使用中のスロット: {slots} 中 {used} · 加熱中: {heating} · 保守が必要: {maintenance}",
        "使用中槽位:{slots} 个中的 {used} 个 · 加热中:{heating} · 待维护:{maintenance}",
        "Ranhuras em uso: {used} de {slots} · a aquecer: {heating} · manutenção pendente: {maintenance}",
    ),
    "rack_alarms_title": ("Alarms", "Alarmas", "Alarme", "Alarmes", "Allarmi", "アラーム", "告警", "Alarmes"),
    "rack_alarms_none": ("There are no alarms in the snapshot.", "No hay alarmas en la instantánea.", "Der Snapshot enthält keine Alarme.", "L'instantané ne contient aucune alarme.", "Lo snapshot non contiene allarmi.", "スナップショットにアラームはありません。", "快照中没有告警。", "O instantâneo não tem alarmes."),
    "rack_alarm_maintenance": ("Slot {slot}: maintenance due for unit {unit}", "Ranura {slot}: mantenimiento pendiente de la unidad {unit}", "Slot {slot}: Wartung der Einheit {unit} fällig", "Emplacement {slot} : maintenance due pour l'unité {unit}", "Slot {slot}: manutenzione dovuta per l'unità {unit}", "スロット {slot}: ユニット {unit} の保守が必要", "槽位 {slot}:单元 {unit} 待维护", "Ranhura {slot}: manutenção pendente da unidade {unit}"),
    "rack_alarm_expired": ("Slot {slot}: pre-heat limit reached, the target was switched off", "Ranura {slot}: se alcanzó el límite de precalentamiento y se apagó el objetivo", "Slot {slot}: Vorheizgrenze erreicht, das Ziel wurde abgeschaltet", "Emplacement {slot} : limite de préchauffage atteinte, la consigne a été coupée", "Slot {slot}: limite di preriscaldamento raggiunto, il target è stato spento", "スロット {slot}: 予熱の上限に達し、目標を停止しました", "槽位 {slot}:已达预热上限,目标已关闭", "Ranhura {slot}: limite de pré-aquecimento atingido, o alvo foi desligado"),
    "rack_alarm_thermal": ("Slot {slot}: thermal check says {verdict}", "Ranura {slot}: la comprobación térmica dice {verdict}", "Slot {slot}: Wärmeprüfung meldet {verdict}", "Emplacement {slot} : le contrôle thermique indique {verdict}", "Slot {slot}: il controllo termico indica {verdict}", "スロット {slot}: 温度チェックの結果は {verdict}", "槽位 {slot}:热检查结果为 {verdict}", "Ranhura {slot}: a verificação térmica indica {verdict}"),
    "rack_slots_title": ("Slots", "Ranuras", "Slots", "Emplacements", "Slot", "スロット", "槽位", "Ranhuras"),
    "rack_col_slot": ("Slot", "Ranura", "Slot", "Emplacement", "Slot", "スロット", "槽位", "Ranhura"),
    "rack_col_tool": ("Tool", "Herramienta", "Werkzeug", "Outil", "Utensile", "ツール", "工具", "Ferramenta"),
    "rack_col_unit": ("Unit", "Unidad", "Einheit", "Unité", "Unità", "ユニット", "单元", "Unidade"),
    "rack_col_target": ("Target °C", "Objetivo °C", "Ziel °C", "Consigne °C", "Target °C", "目標 °C", "目标 °C", "Alvo °C"),
    "rack_col_thermal": ("Thermal check", "Comprobación térmica", "Wärmeprüfung", "Contrôle thermique", "Controllo termico", "温度チェック", "热检查", "Verificação térmica"),
    "rack_col_wear": ("Wear", "Desgaste", "Verschleiß", "Usure", "Usura", "摩耗", "磨损", "Desgaste"),
    "rack_caption": ("Slots of the rack with the tool, the unit, the target and the thermal check", "Ranuras del rack con la herramienta, la unidad, el objetivo y la comprobación térmica", "Slots des Racks mit Werkzeug, Einheit, Ziel und Wärmeprüfung", "Emplacements du rack avec l'outil, l'unité, la consigne et le contrôle thermique", "Slot del rack con utensile, unità, target e controllo termico", "ツール、ユニット、目標、温度チェックを含むラックのスロット", "机架的槽位及其工具、单元、目标与热检查", "Ranhuras do rack com a ferramenta, a unidade, o alvo e a verificação térmica"),
    "rack_empty": ("Empty", "Vacía", "Leer", "Vide", "Vuoto", "空", "空", "Vazia"),
    "rack_wear": ("{cycles} cycles, {seconds} s of heater", "{cycles} ciclos, {seconds} s de calentador", "{cycles} Zyklen, {seconds} s Heizung", "{cycles} cycles, {seconds} s de chauffe", "{cycles} cicli, {seconds} s di riscaldatore", "{cycles} サイクル、ヒーター {seconds} 秒", "{cycles} 次循环,加热 {seconds} 秒", "{cycles} ciclos, {seconds} s de aquecedor"),
    "rack_wear_maintenance": ("Maintenance due", "Mantenimiento pendiente", "Wartung fällig", "Maintenance due", "Manutenzione dovuta", "保守が必要", "待维护", "Manutenção pendente"),
    "rack_v_empty_ok": ("empty and cold", "vacía y fría", "leer und kalt", "vide et froid", "vuoto e freddo", "空で低温", "空且冷", "vazia e fria"),
    "rack_v_heater_in_empty_slot": ("heater on in an empty slot", "calentador encendido en una ranura vacía", "Heizung in leerem Slot an", "chauffage actif dans un emplacement vide", "riscaldatore acceso in uno slot vuoto", "空のスロットでヒーターがオン", "空槽位中加热器开启", "aquecedor ligado numa ranhura vazia"),
    "rack_v_idle_ok": ("idle and cold", "inactiva y fría", "untätig und kalt", "au repos et froid", "inattivo e freddo", "待機中で低温", "空闲且冷", "inativa e fria"),
    "rack_v_still_hot": ("still hot", "aún caliente", "noch heiß", "encore chaud", "ancora caldo", "まだ高温", "仍然很热", "ainda quente"),
    "rack_v_heating": ("heating", "calentando", "heizt", "en chauffe", "in riscaldamento", "加熱中", "加热中", "a aquecer"),
    "rack_v_reached": ("target reached", "objetivo alcanzado", "Ziel erreicht", "consigne atteinte", "target raggiunto", "目標に到達", "已达到目标", "alvo atingido"),
    "rack_v_not_reached": ("target not reached", "objetivo no alcanzado", "Ziel nicht erreicht", "consigne non atteinte", "target non raggiunto", "目標に未到達", "未达到目标", "alvo não atingido"),
    "rack_v_overshoot": ("overshoot", "sobretemperatura", "Überschwingen", "dépassement", "superamento", "オーバーシュート", "超调", "ultrapassagem"),
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
