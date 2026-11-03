#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_tests_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the tab "Tests" (automated tests declared per ecosystem and per project) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "tab_tests": ("Tests", "Pruebas", "Tests", "Tests", "Test", "テスト", "测试", "Testes"),
    "th_tests": ("Tests", "Pruebas", "Tests", "Tests", "Test", "テスト", "测试", "Testes"),
    "ts_title": (
        "Automated tests by ecosystem", "Pruebas automáticas por ecosistema", "Automatisierte Tests je Ökosystem", "Tests automatisés par écosystème",
        "Test automatici per ecosistema", "エコシステム別の自動テスト", "各生态系统的自动化测试", "Testes automáticos por ecossistema"),
    "ts_hint": (
        "Number of automated tests that each repository declares in its own README or glance file. It is a declared figure: the dashboard reads it and does not run the tests.",
        "Número de pruebas automáticas que cada repositorio declara en su propio README o archivo glance. Es una cifra declarada: el dashboard la lee y no ejecuta las pruebas.",
        "Anzahl der automatisierten Tests, die jedes Repository in seiner eigenen README oder Glance-Datei angibt. Die Zahl ist erklärt: Das Dashboard liest sie und führt die Tests nicht aus.",
        "Nombre de tests automatisés que chaque dépôt déclare dans son propre README ou fichier glance. C'est un chiffre déclaré : le tableau de bord le lit et n'exécute pas les tests.",
        "Numero di test automatici che ogni repository dichiara nel proprio README o file glance. È un dato dichiarato: la dashboard lo legge e non esegue i test.",
        "各リポジトリが自身の README または glance ファイルで宣言している自動テストの数です。宣言された数値であり、ダッシュボードは読み取るだけでテストは実行しません。",
        "各仓库在自己的 README 或 glance 文件中声明的自动化测试数量。这是声明值：仪表板只读取，不运行测试。",
        "Número de testes automáticos que cada repositório declara no seu próprio README ou ficheiro glance. É um valor declarado: o painel lê-o e não executa os testes."),
    "ts_badge": (
        "Declared, not run here", "Declarado, no ejecutado aquí", "Erklärt, hier nicht ausgeführt", "Déclaré, non exécuté ici",
        "Dichiarato, non eseguito qui", "宣言値(ここでは未実行)", "声明值,此处未运行", "Declarado, não executado aqui"),
    "ts_help_summary": (
        "How is this calculated?", "¿Cómo se calcula?", "Wie wird das berechnet?", "Comment est-ce calculé ?",
        "Come viene calcolato?", "どのように算出していますか?", "这是如何计算的?", "Como é calculado?"),
    "ts_help_body": (
        "Count declared by each repository in its README or glance file, not run by the dashboard. The source of each ecosystem is set in dashboard-config.json: {sources}. A repository whose source has no number is shown as not declared (never as zero); a lookup that fails is shown as not verified, or as the last known value with its date. Nodes count checks of their host programs: those are listed apart and never added to the tests. This is not evidence from a CI run: that is in the Evidence tab.",
        "Recuento declarado por cada repositorio en su README o archivo glance, no ejecutado por el dashboard. La fuente de cada ecosistema se fija en dashboard-config.json: {sources}. Un repositorio cuya fuente no trae número se muestra como no declarado (nunca como cero); una consulta que falla se muestra como no verificado, o como el último valor conocido con su fecha. Los nodos cuentan comprobaciones de sus programas de host: se listan aparte y nunca se suman a las pruebas. No es evidencia de una ejecución de CI: eso está en la pestaña Evidencia.",
        "Von jedem Repository in seiner README oder Glance-Datei erklärte Anzahl, vom Dashboard nicht ausgeführt. Die Quelle jedes Ökosystems steht in dashboard-config.json: {sources}. Ein Repository, dessen Quelle keine Zahl enthält, gilt als nicht erklärt (nie als null); eine fehlgeschlagene Abfrage gilt als nicht geprüft oder als letzter bekannter Wert mit Datum. Knoten zählen Prüfungen ihrer Host-Programme: Diese werden getrennt aufgeführt und nie zu den Tests addiert. Das ist kein Nachweis eines CI-Laufs: Der steht im Tab Nachweise.",
        "Nombre déclaré par chaque dépôt dans son README ou fichier glance, non exécuté par le tableau de bord. La source de chaque écosystème est fixée dans dashboard-config.json : {sources}. Un dépôt dont la source n'a pas de nombre est affiché comme non déclaré (jamais comme zéro) ; une requête qui échoue est affichée comme non vérifiée, ou comme dernière valeur connue avec sa date. Les nœuds comptent des vérifications de leurs programmes hôte : elles sont listées à part et jamais ajoutées aux tests. Ce n'est pas une preuve d'une exécution CI : elle se trouve dans l'onglet Preuves.",
        "Numero dichiarato da ogni repository nel proprio README o file glance, non eseguito dalla dashboard. La fonte di ogni ecosistema è fissata in dashboard-config.json: {sources}. Un repository la cui fonte non riporta un numero è mostrato come non dichiarato (mai come zero); una richiesta fallita è mostrata come non verificata, o come ultimo valore noto con la sua data. I nodi contano verifiche dei loro programmi host: sono elencate a parte e mai sommate ai test. Non è la prova di un'esecuzione CI: quella è nella scheda Evidenza.",
        "各リポジトリが README または glance ファイルで宣言した数で、ダッシュボードは実行しません。各エコシステムの取得元は dashboard-config.json で設定します:{sources}。取得元に数値がないリポジトリは「未宣言」と表示し(ゼロにはしません)、取得に失敗した場合は「未確認」または日付付きの最後に判明した値を表示します。ノードはホストプログラムのチェック数を数えますが、これは別に表示し、テスト数には加算しません。CI 実行の証拠ではありません。それは「エビデンス」タブにあります。",
        "各仓库在其 README 或 glance 文件中声明的数量,仪表板不运行测试。各生态系统的来源在 dashboard-config.json 中设定:{sources}。来源中没有数字的仓库显示为未声明(绝不显示为零);查询失败则显示为未验证,或带日期的最后已知值。节点统计其主机程序的检查数:单独列出,绝不计入测试总数。这不是 CI 运行的证据:那在“证据”标签页中。",
        "Número declarado por cada repositório no seu README ou ficheiro glance, não executado pelo painel. A fonte de cada ecossistema é definida em dashboard-config.json: {sources}. Um repositório cuja fonte não traz número aparece como não declarado (nunca como zero); uma consulta que falha aparece como não verificada, ou como o último valor conhecido com a data. Os nós contam verificações dos seus programas de anfitrião: são listadas à parte e nunca somadas aos testes. Não é prova de uma execução de CI: essa está no separador Evidência."),
    "ts_not_read": (
        "No test count could be read in this build, so nothing is verified.", "En esta compilación no se pudo leer ningún recuento de pruebas, así que nada está verificado.",
        "In diesem Build konnte keine Testanzahl gelesen werden, daher ist nichts geprüft.", "Aucun nombre de tests n'a pu être lu dans cette compilation, donc rien n'est vérifié.",
        "In questa build non è stato possibile leggere alcun numero di test, quindi nulla è verificato.", "このビルドではテスト数を読み取れなかったため、何も確認されていません。",
        "此次构建未能读取任何测试数量,因此没有任何内容经过验证。", "Nesta compilação não foi possível ler nenhuma contagem de testes, pelo que nada está verificado."),
    "ts_stale": (
        "GitHub could not be read now, so the last known count is shown (the newest is from {date}). Repositories affected: {n}.",
        "Ahora no se pudo leer GitHub, así que se muestra el último recuento conocido (el más reciente es del {date}). Repositorios afectados: {n}.",
        "GitHub konnte jetzt nicht gelesen werden, daher wird die letzte bekannte Anzahl gezeigt (die neueste vom {date}). Betroffene Repositorys: {n}.",
        "GitHub n'a pas pu être lu maintenant, le dernier nombre connu est donc affiché (le plus récent date du {date}). Dépôts concernés : {n}.",
        "Ora non è stato possibile leggere GitHub, quindi viene mostrato l'ultimo numero noto (il più recente è del {date}). Repository interessati: {n}.",
        "GitHub を今回読み取れなかったため、最後に判明した数を表示しています(最新は {date})。対象リポジトリ:{n}。",
        "此次无法读取 GitHub,因此显示最后已知数量(最新为 {date})。受影响的仓库:{n}。",
        "Agora não foi possível ler o GitHub, por isso é mostrada a última contagem conhecida (a mais recente é de {date}). Repositórios afetados: {n}."),
    "ts_unverified_note": (
        "Not verified (could not be read and no earlier value): {n}.", "No verificado (no se pudo leer y no hay valor anterior): {n}.",
        "Nicht geprüft (nicht lesbar und kein früherer Wert): {n}.", "Non vérifié (illisible et sans valeur antérieure) : {n}.",
        "Non verificato (non leggibile e nessun valore precedente): {n}.", "未確認(読み取れず、以前の値もなし):{n}。",
        "未验证(无法读取且没有先前的值):{n}。", "Não verificado (não foi possível ler e sem valor anterior): {n}."),
    "ts_eco_title": (
        "Total tests per ecosystem", "Total de pruebas por ecosistema", "Tests insgesamt je Ökosystem", "Total des tests par écosystème",
        "Totale dei test per ecosistema", "エコシステム別のテスト総数", "各生态系统的测试总数", "Total de testes por ecossistema"),
    "ts_eco_aria": (
        "Bar chart of the tests declared by each ecosystem; the table below has the same figures",
        "Gráfica de barras de las pruebas declaradas por cada ecosistema; la tabla de abajo tiene las mismas cifras",
        "Balkendiagramm der je Ökosystem erklärten Tests; die Tabelle darunter enthält dieselben Zahlen",
        "Diagramme en barres des tests déclarés par chaque écosystème ; le tableau ci-dessous contient les mêmes chiffres",
        "Grafico a barre dei test dichiarati da ogni ecosistema; la tabella sotto ha gli stessi dati",
        "各エコシステムが宣言したテストの棒グラフ。下の表に同じ数値があります", "各生态系统声明的测试数量柱状图;下方表格含有相同数据",
        "Gráfico de barras dos testes declarados por cada ecossistema; a tabela abaixo tem os mesmos valores"),
    "ts_bar_tip": (
        "{eco}: {n} tests declared by {k} of {total} repositories", "{eco}: {n} pruebas declaradas por {k} de {total} repositorios",
        "{eco}: {n} Tests, erklärt von {k} von {total} Repositorys", "{eco} : {n} tests déclarés par {k} dépôts sur {total}",
        "{eco}: {n} test dichiarati da {k} repository su {total}", "{eco}:{total} 件中 {k} 件のリポジトリが宣言した {n} テスト",
        "{eco}:{total} 个仓库中有 {k} 个声明了 {n} 个测试", "{eco}: {n} testes declarados por {k} de {total} repositórios"),
    "ts_col_eco": ("Ecosystem", "Ecosistema", "Ökosystem", "Écosystème", "Ecosistema", "エコシステム", "生态系统", "Ecossistema"),
    "ts_col_tests": ("Tests", "Pruebas", "Tests", "Tests", "Test", "テスト", "测试", "Testes"),
    "ts_col_checks": (
        "Host-program checks (apart)", "Comprobaciones de programas de host (aparte)", "Prüfungen von Host-Programmen (getrennt)", "Vérifications de programmes hôte (à part)", "Verifiche di programmi host (a parte)", "ホストプログラムのチェック数(別枠)", "主机程序检查数(另计)", "Verificações de programas de anfitrião (à parte)"),
    "ts_col_declared": (
        "Repositories that declare", "Repositorios que declaran", "Deklarierende Repositorys", "Dépôts qui déclarent", "Repository che dichiarano", "宣言しているリポジトリ", "已声明的仓库", "Repositórios que declaram"),
    "ts_col_undeclared": (
        "Not declared", "No declaran", "Nicht erklärt", "Non déclarés", "Non dichiarati", "未宣言", "未声明", "Não declaram"),
    "ts_col_unread": (
        "Not verified", "No verificado", "Nicht geprüft", "Non vérifié", "Non verificato", "未確認", "未验证", "Não verificado"),
    "ts_eco_caption": (
        "Tests declared per ecosystem", "Pruebas declaradas por ecosistema", "Erklärte Tests je Ökosystem", "Tests déclarés par écosystème",
        "Test dichiarati per ecosistema", "エコシステム別の宣言テスト数", "各生态系统声明的测试数", "Testes declarados por ecossistema"),
    "ts_evo_title": (
        "Evolution of the total", "Evolución del total", "Entwicklung der Gesamtzahl", "Évolution du total", "Evoluzione del totale", "合計の推移", "总数的变化", "Evolução do total"),
    "ts_evo_hint": (
        "One point per day with a snapshot. A day without a snapshot breaks the line. The total can rise because a repository starts to declare its tests, not only because tests were written.",
        "Un punto por día con instantánea. Un día sin instantánea corta la línea. El total puede subir porque un repositorio empieza a declarar sus pruebas, no solo porque se escribieran pruebas.",
        "Ein Punkt je Tag mit Schnappschuss. Ein Tag ohne Schnappschuss unterbricht die Linie. Die Summe kann steigen, weil ein Repository seine Tests erst jetzt angibt, nicht nur weil Tests geschrieben wurden.",
        "Un point par jour avec un instantané. Un jour sans instantané coupe la ligne. Le total peut augmenter parce qu'un dépôt commence à déclarer ses tests, pas seulement parce que des tests ont été écrits.",
        "Un punto per ogni giorno con istantanea. Un giorno senza istantanea interrompe la linea. Il totale può salire perché un repository inizia a dichiarare i suoi test, non solo perché sono stati scritti test.",
        "スナップショットがある日ごとに 1 点。スナップショットのない日は線が途切れます。合計は、テストが書かれたためだけでなく、リポジトリが宣言を始めたためにも増えます。",
        "有快照的每一天一个点。没有快照的日子会使线条中断。总数上升可能是因为某个仓库开始声明其测试,而不仅仅是写了新测试。",
        "Um ponto por dia com instantâneo. Um dia sem instantâneo interrompe a linha. O total pode subir porque um repositório começa a declarar os seus testes, e não apenas porque foram escritos testes."),
    "ts_evo_none": (
        "Missing data: no daily snapshot has the test counts yet.", "Faltan datos: ninguna instantánea diaria tiene todavía los recuentos de pruebas.",
        "Daten fehlen: Noch kein Tagesschnappschuss enthält die Testanzahlen.", "Données manquantes : aucun instantané quotidien ne contient encore les nombres de tests.",
        "Dati mancanti: nessuna istantanea giornaliera contiene ancora i numeri di test.", "データ不足:テスト数を含む日次スナップショットはまだありません。",
        "缺少数据:还没有任何每日快照包含测试数量。", "Faltam dados: nenhum instantâneo diário tem ainda as contagens de testes."),
    "ts_evo_one": (
        "Only one snapshot has the counts ({date}); a line needs at least two days.", "Solo una instantánea tiene los recuentos ({date}); una línea necesita al menos dos días.",
        "Nur ein Schnappschuss enthält die Zahlen ({date}); eine Linie braucht mindestens zwei Tage.", "Un seul instantané contient les nombres ({date}) ; une ligne demande au moins deux jours.",
        "Solo un'istantanea contiene i numeri ({date}); una linea richiede almeno due giorni.", "数値を含むスナップショットは 1 件のみ({date})。線には少なくとも 2 日分が必要です。",
        "只有一个快照包含这些数量({date});折线至少需要两天的数据。", "Apenas um instantâneo tem as contagens ({date}); uma linha precisa de pelo menos dois dias."),
    "ts_evo_aria": (
        "Line chart of the total tests declared by each ecosystem from {first} to {last}; the table has the same figures",
        "Gráfica de líneas del total de pruebas declaradas por cada ecosistema del {first} al {last}; la tabla tiene las mismas cifras",
        "Liniendiagramm der insgesamt erklärten Tests je Ökosystem vom {first} bis {last}; die Tabelle enthält dieselben Zahlen",
        "Graphique linéaire du total des tests déclarés par chaque écosystème du {first} au {last} ; le tableau contient les mêmes chiffres",
        "Grafico a linee del totale dei test dichiarati da ogni ecosistema dal {first} al {last}; la tabella ha gli stessi dati",
        "{first} から {last} までの各エコシステムの宣言テスト総数の折れ線グラフ。表に同じ数値があります", "{first} 至 {last} 各生态系统声明测试总数的折线图;表格含有相同数据",
        "Gráfico de linhas do total de testes declarados por cada ecossistema de {first} a {last}; a tabela tem os mesmos valores"),
    "ts_evo_point": (
        "{eco} · {date} · {n} tests ({k} repositories)", "{eco} · {date} · {n} pruebas ({k} repositorios)", "{eco} · {date} · {n} Tests ({k} Repositorys)",
        "{eco} · {date} · {n} tests ({k} dépôts)", "{eco} · {date} · {n} test ({k} repository)", "{eco} · {date} · {n} テスト({k} リポジトリ)",
        "{eco} · {date} · {n} 个测试({k} 个仓库)", "{eco} · {date} · {n} testes ({k} repositórios)"),
    "ts_col_date": ("Date", "Fecha", "Datum", "Date", "Data", "日付", "日期", "Data"),
    "ts_evo_cell": ("{n} ({k} repos)", "{n} ({k} repos)", "{n} ({k} Repos)", "{n} ({k} dépôts)", "{n} ({k} repo)", "{n}({k} 件)", "{n}({k} 个)", "{n} ({k} repos)"),
    "ts_proj_title": (
        "Tests per project", "Pruebas por proyecto", "Tests je Projekt", "Tests par projet", "Test per progetto", "プロジェクト別のテスト", "各项目的测试", "Testes por projeto"),
    "ts_proj_hint": (
        "Horizontal bars ordered by the declared count. Select a project to open its panel.",
        "Barras horizontales ordenadas por el recuento declarado. Elige un proyecto para abrir su panel.",
        "Horizontale Balken nach erklärter Anzahl geordnet. Ein Projekt auswählen, um sein Panel zu öffnen.",
        "Barres horizontales triées selon le nombre déclaré. Choisissez un projet pour ouvrir son panneau.",
        "Barre orizzontali ordinate per numero dichiarato. Scegli un progetto per aprire il suo pannello.",
        "宣言された数の順に並べた横棒です。プロジェクトを選ぶとパネルが開きます。", "按声明数量排序的横向条形图。选择一个项目可打开其面板。",
        "Barras horizontais ordenadas pela contagem declarada. Escolha um projeto para abrir o seu painel."),
    "ts_filter_eco": ("Ecosystem", "Ecosistema", "Ökosystem", "Écosystème", "Ecosistema", "エコシステム", "生态系统", "Ecossistema"),
    "ts_filter_all": ("All", "Todos", "Alle", "Tous", "Tutti", "すべて", "全部", "Todos"),
    "ts_filter_family": ("Family", "Familia", "Familie", "Famille", "Famiglia", "ファミリー", "系列", "Família"),
    "ts_filter_family_all": ("All families", "Todas las familias", "Alle Familien", "Toutes les familles", "Tutte le famiglie", "すべてのファミリー", "所有系列", "Todas as famílias"),
    "ts_search": ("Search a project", "Buscar un proyecto", "Projekt suchen", "Rechercher un projet", "Cerca un progetto", "プロジェクトを検索", "搜索项目", "Procurar um projeto"),
    "ts_matches": (
        "{shown} of {total} projects", "{shown} de {total} proyectos", "{shown} von {total} Projekten", "{shown} projets sur {total}", "{shown} progetti su {total}",
        "{total} 件中 {shown} 件のプロジェクト", "{total} 个项目中的 {shown} 个", "{shown} de {total} projetos"),
    "ts_none": (
        "No project matches the filters.", "Ningún proyecto coincide con los filtros.", "Kein Projekt entspricht den Filtern.", "Aucun projet ne correspond aux filtres.",
        "Nessun progetto corrisponde ai filtri.", "条件に一致するプロジェクトはありません。", "没有项目符合筛选条件。", "Nenhum projeto corresponde aos filtros."),
    "ts_proj_caption": (
        "Tests declared per project", "Pruebas declaradas por proyecto", "Erklärte Tests je Projekt", "Tests déclarés par projet", "Test dichiarati per progetto",
        "プロジェクト別の宣言テスト数", "各项目声明的测试数", "Testes declarados por projeto"),
    "ts_col_project": ("Project", "Proyecto", "Projekt", "Projet", "Progetto", "プロジェクト", "项目", "Projeto"),
    "ts_col_state": ("State", "Estado", "Status", "État", "Stato", "状態", "状态", "Estado"),
    "ts_col_source": ("Declared in", "Declarado en", "Erklärt in", "Déclaré dans", "Dichiarato in", "宣言元", "声明位置", "Declarado em"),
    "ts_st_declared": ("Declared", "Declarado", "Erklärt", "Déclaré", "Dichiarato", "宣言済み", "已声明", "Declarado"),
    "ts_st_undeclared": (
        "Not declared", "No declarado", "Nicht erklärt", "Non déclaré", "Non dichiarato", "未宣言", "未声明", "Não declarado"),
    "ts_st_unread": (
        "Not verified", "No verificado", "Nicht geprüft", "Non vérifié", "Non verificato", "未確認", "未验证", "Não verificado"),
    "ts_st_lastknown": (
        "Last known ({date})", "Último conocido ({date})", "Zuletzt bekannt ({date})", "Dernier connu ({date})", "Ultimo noto ({date})", "最後に判明した値({date})",
        "最后已知({date})", "Último conhecido ({date})"),
    "ts_unit_checks": (
        "{n} host-program checks (not unit tests)", "{n} comprobaciones de programas de host (no son pruebas unitarias)", "{n} Prüfungen von Host-Programmen (keine Unit-Tests)", "{n} vérifications de programmes hôte (pas des tests unitaires)", "{n} verifiche di programmi host (non test unitari)", "ホストプログラムのチェック {n} 件(単体テストではありません)", "{n} 项主机程序检查(不是单元测试)", "{n} verificações de programas de anfitrião (não são testes unitários)"),
    "ts_row_aria": (
        "{name}: {value}. Open its panel", "{name}: {value}. Abrir su panel", "{name}: {value}. Panel öffnen", "{name} : {value}. Ouvrir son panneau",
        "{name}: {value}. Apri il pannello", "{name}:{value}。パネルを開く", "{name}:{value}。打开其面板", "{name}: {value}. Abrir o painel"),
    "ts_value_tests": ("{n} tests", "{n} pruebas", "{n} Tests", "{n} tests", "{n} test", "{n} テスト", "{n} 个测试", "{n} testes"),
    "ts_tip_source": (
        "Declared in the {src} of the repository", "Declarado en el {src} del repositorio", "Im {src} des Repositorys erklärt", "Déclaré dans le {src} du dépôt",
        "Dichiarato nel {src} del repository", "リポジトリの {src} で宣言", "在仓库的 {src} 中声明", "Declarado no {src} do repositório"),
    "ts_panel_field": (
        "Tests (declared)", "Pruebas (declaradas)", "Tests (erklärt)", "Tests (déclarés)", "Test (dichiarati)", "テスト(宣言)", "测试(声明)", "Testes (declarados)"),
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
