#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_toolspanel_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the own tab of the Tools group in the eight languages (portuguese is the one of Portugal).

Each entry is (en, es, de, fr, it, ja, zh, pt). generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "eco_intro_electro-hobby-3d": (
        "The programs that sit above the four ecosystems: the Actions monitor and the updater of the suite.",
        "Los programas que están por encima de los cuatro ecosistemas: el monitor de Actions y el actualizador de la suite.",
        "Die Programme oberhalb der vier Ökosysteme: der Actions-Monitor und der Updater der Suite.",
        "Les programmes au-dessus des quatre écosystèmes : le moniteur Actions et l'outil de mise à jour de la suite.",
        "I programmi sopra i quattro ecosistemi: il monitor di Actions e l'aggiornatore della suite.",
        "4つのエコシステムの上位にあるプログラム: Actions モニターとスイートのアップデーター。",
        "位于四个生态系统之上的程序:Actions 监视器和套件更新器。",
        "Os programas acima dos quatro ecossistemas: o monitor do Actions e o atualizador da suite."),
    "tl_title": (
        "Tools: the programs above the four ecosystems", "Herramientas: los programas por encima de los cuatro ecosistemas",
        "Werkzeuge: die Programme oberhalb der vier Ökosysteme", "Outils : les programmes au-dessus des quatre écosystèmes",
        "Strumenti: i programmi sopra i quattro ecosistemi", "ツール: 4つのエコシステムの上位にあるプログラム",
        "工具:位于四个生态系统之上的程序", "Ferramentas: os programas acima dos quatro ecossistemas"),
    "tl_hint": (
        "One row per tool: version, latest release, state of its CI and tests. Read when the page was generated; what could not be read is never shown as fine.",
        "Una fila por herramienta: versión, última versión publicada, estado de su CI y de sus pruebas. Se lee al generar la página; lo que no se pudo leer nunca se muestra como correcto.",
        "Eine Zeile je Werkzeug: Version, letzte Veröffentlichung, Zustand von CI und Tests. Gelesen beim Erzeugen der Seite; was nicht gelesen werden konnte, wird nie als in Ordnung gezeigt.",
        "Une ligne par outil : version, dernière publication, état de la CI et des tests. Lu à la génération de la page ; ce qui n'a pas pu être lu n'est jamais présenté comme correct.",
        "Una riga per strumento: versione, ultima pubblicazione, stato di CI e test. Letto alla generazione della pagina; ciò che non si è potuto leggere non è mai mostrato come a posto.",
        "ツールごとに 1 行: バージョン、最新リリース、CI とテストの状態。ページ生成時に読み取ります。読み取れなかったものを正常として表示することはありません。",
        "每个工具一行:版本、最新发布、CI 与测试状态。页面生成时读取;无法读取的内容绝不会显示为正常。",
        "Uma linha por ferramenta: versão, última publicação, estado da CI e dos testes. Lido ao gerar a página; o que não se conseguiu ler nunca é mostrado como correto."),
    "tl_none": ("No tool of the group could be listed.", "No se pudo listar ninguna herramienta del grupo.", "Es konnte kein Werkzeug der Gruppe aufgelistet werden.",
                "Aucun outil du groupe n'a pu être listé.", "Nessuno strumento del gruppo è stato elencato.", "グループのツールを一覧できませんでした。",
                "无法列出该组的任何工具。", "Não foi possível listar nenhuma ferramenta do grupo."),
    "tl_col_tool": ("Tool", "Herramienta", "Werkzeug", "Outil", "Strumento", "ツール", "工具", "Ferramenta"),
    "tl_col_version": ("Version", "Versión", "Version", "Version", "Versione", "バージョン", "版本", "Versão"),
    "tl_col_maturity": ("Maturity", "Madurez", "Reifegrad", "Maturité", "Maturità", "成熟度", "成熟度", "Maturidade"),
    "tl_col_release": ("Latest release", "Última versión publicada", "Letzte Veröffentlichung", "Dernière publication", "Ultima pubblicazione", "最新リリース", "最新发布", "Última publicação"),
    "tl_col_ci": ("CI", "CI", "CI", "CI", "CI", "CI", "CI", "CI"),
    "tl_col_tests": ("Tests", "Pruebas", "Tests", "Tests", "Test", "テスト", "测试", "Testes"),
    "tl_col_links": ("Links", "Enlaces", "Links", "Liens", "Link", "リンク", "链接", "Ligações"),
    "tl_ci_success": ("Green", "Verde", "Grün", "Vert", "Verde", "成功", "通过", "Verde"),
    "tl_ci_failure": ("Red", "Rojo", "Rot", "Rouge", "Rosso", "失敗", "失败", "Vermelho"),
    "tl_ci_pending": ("Pending", "Pendiente", "Ausstehend", "En attente", "In attesa", "保留中", "等待中", "Pendente"),
    "tl_ci_none": ("No CI / unknown", "Sin CI / desconocido", "Keine CI / unbekannt", "Pas de CI / inconnu", "Nessuna CI / sconosciuto", "CI なし / 不明", "无 CI / 未知", "Sem CI / desconhecido"),
    "tl_tests_none": ("not declared", "no declaradas", "nicht angegeben", "non déclarés", "non dichiarati", "未宣言", "未声明", "não declarados"),
    "tl_link_repo": ("Repository", "Repositorio", "Repository", "Dépôt", "Repository", "リポジトリ", "仓库", "Repositório"),
    "tl_link_releases": ("Releases", "Versiones", "Releases", "Publications", "Release", "リリース", "发布", "Publicações"),
    "tl_link_changelog": ("Changelog", "Cambios", "Änderungen", "Changements", "Modifiche", "変更履歴", "变更记录", "Alterações"),
    "tl_link_ai": ("Guide: connect an AI tool", "Guía: conectar una herramienta de IA", "Anleitung: ein KI-Werkzeug anbinden", "Guide : connecter un outil d'IA",
                   "Guida: collegare uno strumento di IA", "ガイド: AI ツールを接続する", "指南:连接 AI 工具", "Guia: ligar uma ferramenta de IA"),
    "tl_link_quota": ("Guide: more quota, less spending", "Guía: más cuota, menos gasto", "Anleitung: mehr Kontingent, weniger Verbrauch", "Guide : plus de quota, moins de dépense",
                      "Guida: più quota, meno consumo", "ガイド: クォータを増やし消費を減らす", "指南:更多配额,更少消耗", "Guia: mais quota, menos gasto"),
    "tl_mon_intro": (
        "Watches the workflows of every repository you own and shows what is red, stuck or waiting on one local page, in eight languages, with metrics for Grafana. A workflow is red when the last completed run of its file on the default branch failed; this dashboard uses the same rule (see the Sentinel tab).",
        "Vigila los workflows de todos tus repositorios y muestra qué está en rojo, atascado o esperando en una página local, en ocho idiomas, con métricas para Grafana. Un workflow está en rojo cuando falló la última ejecución terminada de su fichero en la rama principal; este panel usa la misma regla (ver la pestaña Centinela).",
        "Überwacht die Workflows aller deiner Repositories und zeigt auf einer lokalen Seite in acht Sprachen, was rot ist, hängt oder wartet, mit Metriken für Grafana. Ein Workflow ist rot, wenn der letzte abgeschlossene Lauf seiner Datei auf dem Hauptzweig fehlschlug; dieses Dashboard nutzt dieselbe Regel (siehe Tab Wächter).",
        "Surveille les workflows de tous vos dépôts et montre sur une page locale, en huit langues, ce qui est rouge, bloqué ou en attente, avec des métriques pour Grafana. Un workflow est rouge quand la dernière exécution terminée de son fichier sur la branche principale a échoué ; ce tableau de bord applique la même règle (voir l'onglet Sentinelle).",
        "Controlla i workflow di tutti i tuoi repository e mostra su una pagina locale, in otto lingue, cosa è rosso, bloccato o in attesa, con metriche per Grafana. Un workflow è rosso quando l'ultima esecuzione conclusa del suo file sul ramo principale è fallita; questo pannello usa la stessa regola (vedi la scheda Sentinella).",
        "所有リポジトリのワークフローを監視し、赤いもの・止まっているもの・待機中のものをローカルの1ページに8言語で表示します。Grafana 用のメトリクス付き。ワークフローは、メインブランチでそのファイルの最後に完了した実行が失敗したときに赤になります。このダッシュボードも同じルールを使います(センチネルのタブを参照)。",
        "监视你所有仓库的工作流,在本地页面上以八种语言显示哪些是红的、卡住的或在等待的,并提供用于 Grafana 的指标。当某个工作流文件在主分支上最近一次完成的运行失败时,它就是红色;本仪表盘使用相同的规则(见哨兵标签页)。",
        "Vigia os workflows de todos os seus repositórios e mostra, numa página local, em oito idiomas, o que está a vermelho, encravado ou à espera, com métricas para o Grafana. Um workflow está a vermelho quando a última execução concluída do seu ficheiro no ramo principal falhou; este painel usa a mesma regra (ver o separador Sentinela)."),
    "tl_mon_ed_title": ("Two editions", "Dos ediciones", "Zwei Ausgaben", "Deux éditions", "Due edizioni", "2 つのエディション", "两个版本", "Duas edições"),
    "tl_ed_complete": ("Complete", "Completa", "Vollständig", "Complète", "Completa", "完全版", "完整版", "Completa"),
    "tl_ed_lite": ("Lite", "Lite", "Lite", "Lite", "Lite", "Lite", "Lite", "Lite"),
    "tl_mon_ed_complete": (
        "the monitor and its five sentinels that never write to GitHub (CI with its checks A1 to A13, Collab, Security, Supply chain and Delivery), a score and the health of each repository and team, reports, wall screens, accounts with roles and an operation panel with backup and an updater.",
        "el monitor y sus cinco centinelas que nunca escriben en GitHub (CI con sus comprobaciones A1 a A13, Colaboración, Seguridad, Cadena de suministro y Entrega), una puntuación y la salud de cada repositorio y equipo, informes, pantallas de pared, cuentas con roles y un panel de operación con copia de seguridad y actualizador.",
        "der Monitor und seine fünf Wächter, die nie in GitHub schreiben (CI mit den Prüfungen A1 bis A13, Collab, Sicherheit, Lieferkette und Auslieferung), ein Score und der Zustand jedes Repositorys und Teams, Berichte, Wandbildschirme, Konten mit Rollen und ein Betriebspanel mit Sicherung und Updater.",
        "le moniteur et ses cinq sentinelles qui n'écrivent jamais dans GitHub (CI avec ses contrôles A1 à A13, Collab, Sécurité, Chaîne d'approvisionnement et Livraison), un score et la santé de chaque dépôt et équipe, des rapports, des écrans muraux, des comptes avec rôles et un panneau d'exploitation avec sauvegarde et outil de mise à jour.",
        "il monitor e le sue cinque sentinelle che non scrivono mai su GitHub (CI con i controlli da A1 ad A13, Collab, Sicurezza, Catena di fornitura e Consegna), un punteggio e lo stato di ogni repository e team, report, schermi a parete, account con ruoli e un pannello operativo con backup e updater.",
        "モニターと、GitHub に一切書き込まない 5 つのセンチネル(チェック A1~A13 の CI、Collab、セキュリティ、サプライチェーン、デリバリー)、スコアと各リポジトリ・チームの健全性、レポート、壁掛け画面、ロール付きアカウント、バックアップとアップデーターを備えた運用パネルが付きます。",
        "监视器加上五个从不写入 GitHub 的哨兵(带有检查 A1 至 A13 的 CI、协作、安全、供应链和交付)、评分以及每个仓库和团队的健康状况、报告、墙面屏幕、带角色的账户,以及含备份和更新器的运维面板。",
        "o monitor e as suas cinco sentinelas que nunca escrevem no GitHub (CI com as verificações A1 a A13, Colaboração, Segurança, Cadeia de abastecimento e Entrega), uma pontuação e a saúde de cada repositório e equipa, relatórios, ecrãs de parede, contas com funções e um painel de operação com cópia de segurança e atualizador."),
    "tl_mon_ed_lite": (
        "the monitor alone, with no sentinel; the connection with an AI tool is the same in both editions.",
        "solo el monitor, sin centinela; la conexión con una herramienta de IA es la misma en las dos ediciones.",
        "nur der Monitor, ohne Wächter; die Anbindung eines KI-Werkzeugs ist in beiden Ausgaben gleich.",
        "le moniteur seul, sans sentinelle ; la connexion avec un outil d'IA est la même dans les deux éditions.",
        "solo il monitor, senza sentinella; il collegamento con uno strumento di IA è lo stesso in entrambe le edizioni.",
        "モニターのみでセンチネルはありません。AI ツールとの接続は両エディションで同じです。",
        "仅监视器,不含哨兵;与 AI 工具的连接在两个版本中相同。",
        "só o monitor, sem sentinela; a ligação com uma ferramenta de IA é a mesma nas duas edições."),
    "tl_mon_ai_title": ("Connect an AI tool", "Conectar una herramienta de IA", "Ein KI-Werkzeug anbinden", "Connecter un outil d'IA", "Collegare uno strumento di IA", "AI ツールを接続する", "连接 AI 工具", "Ligar uma ferramenta de IA"),
    "tl_mon_ai_body": (
        "Five channels, the same in both editions: a brief of what to do now, a feed of alerts, the state as data, a stream of events and MCP tools, plus a gate script that adds the brief to the session of the AI. Everything is read only unless you allow an action.",
        "Cinco canales, los mismos en las dos ediciones: un resumen de qué hacer ahora, un registro de alertas, el estado como datos, un flujo de eventos y herramientas MCP, además de un script de control que añade el resumen a la sesión de la IA. Todo es de solo lectura salvo que permitas una acción.",
        "Fünf Kanäle, in beiden Ausgaben gleich: eine Kurzfassung dessen, was jetzt zu tun ist, ein Feed der Alarme, der Zustand als Daten, ein Ereignisstrom und MCP-Werkzeuge, dazu ein Gate-Skript, das die Kurzfassung in die Sitzung der KI einfügt. Alles ist nur lesend, solange du keine Aktion erlaubst.",
        "Cinq canaux, les mêmes dans les deux éditions : un résumé de ce qu'il faut faire maintenant, un flux d'alertes, l'état sous forme de données, un flux d'événements et des outils MCP, plus un script de garde qui ajoute le résumé à la session de l'IA. Tout est en lecture seule sauf si vous autorisez une action.",
        "Cinque canali, gli stessi in entrambe le edizioni: un riepilogo di cosa fare ora, un feed di avvisi, lo stato come dati, un flusso di eventi e strumenti MCP, più uno script di controllo che aggiunge il riepilogo alla sessione dell'IA. Tutto è in sola lettura salvo che tu consenta un'azione.",
        "両エディション共通の 5 つのチャネル: 今やるべきことの要約、アラートのフィード、データとしての状態、イベントのストリーム、MCP ツール。さらに、要約を AI のセッションに追加するゲートスクリプトがあります。操作を許可しない限りすべて読み取り専用です。",
        "两个版本相同的五个通道:现在该做什么的简报、警报订阅、作为数据的状态、事件流和 MCP 工具,另有一个把简报加入 AI 会话的闸门脚本。除非你允许某项操作,否则一切均为只读。",
        "Cinco canais, os mesmos nas duas edições: um resumo do que fazer agora, um feed de alertas, o estado como dados, um fluxo de eventos e ferramentas MCP, mais um script de controlo que junta o resumo à sessão da IA. Tudo é só de leitura, a menos que permita uma ação."),
    "tl_mon_quota_title": ("Quota and refresh", "Cuota y refresco", "Kontingent und Aktualisierung", "Quota et rafraîchissement", "Quota e aggiornamento", "クォータと更新", "配额与刷新", "Quota e atualização"),
    "tl_mon_quota_body": (
        "The monitor spends little: conditional reads (an unchanged answer, a 304, costs nothing), batched GraphQL queries and saved reads. The central panel of this page is refreshed at least every half hour, and the Sentinel tab warns when it is more than two hours behind.",
        "El monitor gasta poco: lecturas condicionales (una respuesta sin cambios, un 304, no cuesta nada), consultas GraphQL por lotes y lecturas guardadas. El panel central de esta página se refresca al menos cada media hora y la pestaña Centinela avisa si va más de dos horas atrasado.",
        "Der Monitor verbraucht wenig: bedingte Abfragen (eine unveränderte Antwort, ein 304, kostet nichts), gebündelte GraphQL-Abfragen und gespeicherte Lesungen. Das zentrale Panel dieser Seite wird mindestens alle 30 Minuten erneuert, und der Tab Wächter warnt, wenn es mehr als zwei Stunden zurückliegt.",
        "Le moniteur dépense peu : lectures conditionnelles (une réponse inchangée, un 304, ne coûte rien), requêtes GraphQL groupées et lectures sauvegardées. Le panneau central de cette page est rafraîchi au moins toutes les demi-heures et l'onglet Sentinelle avertit s'il a plus de deux heures de retard.",
        "Il monitor consuma poco: letture condizionali (una risposta invariata, un 304, non costa nulla), query GraphQL a blocchi e letture salvate. Il pannello centrale di questa pagina viene aggiornato almeno ogni mezz'ora e la scheda Sentinella avvisa se è in ritardo di più di due ore.",
        "モニターの消費は小さく、条件付き読み取り(変更なしの応答 304 は消費ゼロ)、GraphQL の一括クエリ、保存済みの読み取りを使います。このページの中央パネルは少なくとも 30 分ごとに更新され、2 時間以上遅れるとセンチネルのタブが警告します。",
        "监视器消耗很少:条件读取(未变化的响应 304 不耗配额)、批量 GraphQL 查询和已保存的读取。本页的中央面板至少每半小时刷新一次,落后超过两小时时哨兵标签页会发出警告。",
        "O monitor gasta pouco: leituras condicionais (uma resposta sem alterações, um 304, não custa nada), consultas GraphQL em lote e leituras guardadas. O painel central desta página é atualizado pelo menos de meia em meia hora e o separador Sentinela avisa se estiver mais de duas horas atrasado."),
    "tl_mon_next_title": ("In the next version", "En la próxima versión", "In der nächsten Version", "Dans la prochaine version", "Nella prossima versione", "次のバージョンでは", "下一个版本", "Na próxima versão"),
    "tl_mon_next_body": (
        "Not published yet: a comparison of a period against the one before (share of failed runs, duration, time to resolve alerts, score), an operator command line with table, plain, JSON, NDJSON and CSV formats, a watch command, shell completions and a kiosk profile with larger type and high contrast for wall screens. This dashboard takes the same ideas of the sentinels in its own way: the Supply chain and Delivery cards of the Sentinel tab.",
        "Aún sin publicar: la comparación de un periodo con el anterior (porcentaje de ejecuciones fallidas, duración, tiempo en resolver alertas, puntuación), una línea de órdenes de operador con formatos de tabla, texto plano, JSON, NDJSON y CSV, un comando de vigilancia, autocompletado del intérprete y un perfil de quiosco con letra mayor y alto contraste para pantallas de pared. Este panel toma a su manera las ideas de los centinelas: las tarjetas Cadena de suministro y Entrega de la pestaña Centinela.",
        "Noch nicht veröffentlicht: der Vergleich eines Zeitraums mit dem davor (Anteil fehlgeschlagener Läufe, Dauer, Zeit bis zur Lösung von Warnungen, Score), eine Operator-Kommandozeile mit Tabellen-, Klartext-, JSON-, NDJSON- und CSV-Format, ein Watch-Befehl, Shell-Vervollständigungen und ein Kiosk-Profil mit größerer Schrift und hohem Kontrast für Wandbildschirme. Dieses Dashboard übernimmt die Ideen der Wächter auf seine Weise: die Karten Lieferkette und Auslieferung im Tab Wächter.",
        "Pas encore publié : la comparaison d'une période avec la précédente (part des exécutions échouées, durée, délai de résolution des alertes, score), une ligne de commande d'opérateur avec formats tableau, texte brut, JSON, NDJSON et CSV, une commande de surveillance, des complétions de shell et un profil kiosque avec police plus grande et contraste élevé pour les écrans muraux. Ce tableau de bord reprend à sa façon les idées des sentinelles : les cartes Chaîne d'approvisionnement et Livraison de l'onglet Sentinelle.",
        "Non ancora pubblicato: il confronto di un periodo con quello precedente (quota di esecuzioni fallite, durata, tempo di risoluzione degli avvisi, punteggio), una riga di comando da operatore con formati tabella, testo semplice, JSON, NDJSON e CSV, un comando di sorveglianza, completamenti della shell e un profilo chiosco con testo più grande e alto contrasto per gli schermi a parete. Questo pannello riprende a modo suo le idee delle sentinelle: le schede Catena di fornitura e Consegna della scheda Sentinella.",
        "未公開: ある期間を直前の期間と比較する機能(失敗した実行の割合、所要時間、アラートの解決時間、スコア)、表・プレーンテキスト・JSON・NDJSON・CSV の形式を持つオペレーター用コマンドライン、監視コマンド、シェル補完、壁掛け画面向けに文字を大きく高コントラストにしたキオスクプロファイル。このダッシュボードもセンチネルの発想を独自に取り入れています。センチネルタブのサプライチェーンとデリバリーのカードです。",
        "尚未发布:将某个时段与前一时段比较(失败运行占比、时长、警报解决时间、评分)、支持表格、纯文本、JSON、NDJSON 和 CSV 格式的运维命令行、监视命令、Shell 补全,以及面向墙面屏幕、字体更大且高对比度的展台配置。本仪表盘以自己的方式采用了哨兵的思路:哨兵标签页中的供应链和交付卡片。",
        "Ainda não publicado: a comparação de um período com o anterior (percentagem de execuções falhadas, duração, tempo de resolução dos alertas, pontuação), uma linha de comandos de operador com formatos de tabela, texto simples, JSON, NDJSON e CSV, um comando de vigilância, preenchimento automático da shell e um perfil de quiosque com letra maior e alto contraste para ecrãs de parede. Este painel adota à sua maneira as ideias das sentinelas: os cartões Cadeia de abastecimento e Entrega do separador Sentinela."),
    "tl_upd_body": (
        "One window and one command line that hand over to the updater of each ecosystem (HYDRA-UMC-UPDATER, URTC-UPDATER, ARMOR-UPDATER and EH3D-UPDATER).",
        "La ventana y la línea de órdenes únicas que ceden el trabajo al actualizador de cada ecosistema (HYDRA-UMC-UPDATER, URTC-UPDATER, ARMOR-UPDATER y EH3D-UPDATER).",
        "Das eine Fenster und die eine Kommandozeile, die an den Updater jedes Ökosystems übergeben (HYDRA-UMC-UPDATER, URTC-UPDATER, ARMOR-UPDATER und EH3D-UPDATER).",
        "La fenêtre et la ligne de commande uniques qui passent la main à l'outil de mise à jour de chaque écosystème (HYDRA-UMC-UPDATER, URTC-UPDATER, ARMOR-UPDATER et EH3D-UPDATER).",
        "L'unica finestra e riga di comando che passano il lavoro all'aggiornatore di ogni ecosistema (HYDRA-UMC-UPDATER, URTC-UPDATER, ARMOR-UPDATER ed EH3D-UPDATER).",
        "各エコシステムのアップデーター(HYDRA-UMC-UPDATER、URTC-UPDATER、ARMOR-UPDATER、EH3D-UPDATER)に処理を引き渡す、共通のウィンドウとコマンドライン。",
        "统一的窗口和命令行,把工作交给各个生态系统的更新器(HYDRA-UMC-UPDATER、URTC-UPDATER、ARMOR-UPDATER 和 EH3D-UPDATER)。",
        "A janela e a linha de comandos únicas que passam o trabalho ao atualizador de cada ecossistema (HYDRA-UMC-UPDATER, URTC-UPDATER, ARMOR-UPDATER e EH3D-UPDATER)."),
}

TEXTS: dict[str, dict[str, str]] = {code: {key: row[index] for key, row in _ROWS.items()} for index, code in enumerate(LANGUAGES)}


def problems() -> list[str]:
    """Rows with a missing language or an empty text (used by the tests)."""
    out = []
    for key, row in _ROWS.items():
        if len(row) != len(LANGUAGES):
            out.append(f"{key}: {len(row)} languages")
        elif any(not text.strip() for text in row):
            out.append(f"{key}: empty text")
    return out
