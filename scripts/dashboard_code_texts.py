#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_code_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the tab "Code" (lines of code, tests and documentation per repository, ecosystem and type) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. generate_dashboard.py merges the result into its own tables. Stdlib only.
"""
from __future__ import annotations

LANGUAGES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")

_ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "tab_code": ("Code", "Código", "Code", "Code", "Codice", "コード", "代码", "Código"),
    "cd_title": (
        "Code statistics", "Estadísticas de código", "Code-Statistik", "Statistiques de code",
        "Statistiche del codice", "コード統計", "代码统计", "Estatísticas de código"),
    "cd_badge": (
        "Counted on shallow clones", "Contado sobre clones superficiales", "Auf flachen Klonen gezählt", "Compté sur des clones superficiels",
        "Contato su cloni superficiali", "浅いクローンで集計", "基于浅克隆统计", "Contado em clones superficiais"),
    "cd_hint": (
        "Lines of code, tests and documentation of every repository, counted once a day on a fresh shallow copy. Generated, vendored, dependency, binary and image files are left out.",
        "Líneas de código, pruebas y documentación de cada repositorio, contadas una vez al día sobre una copia superficial nueva. Se excluyen los archivos generados, vendorizados, de dependencias, binarios e imágenes.",
        "Zeilen an Code, Tests und Dokumentation jedes Repositorys, einmal täglich auf einer frischen flachen Kopie gezählt. Generierte, mitgelieferte, Abhängigkeits-, Binär- und Bilddateien bleiben außen vor.",
        "Lignes de code, de tests et de documentation de chaque dépôt, comptées une fois par jour sur une copie superficielle neuve. Les fichiers générés, embarqués, de dépendances, binaires et images sont exclus.",
        "Righe di codice, test e documentazione di ogni repository, contate una volta al giorno su una copia superficiale nuova. I file generati, inclusi da terzi, di dipendenze, binari e immagini sono esclusi.",
        "各リポジトリのコード、テスト、ドキュメントの行数を、毎日新しい浅いコピーで集計しています。生成物、同梱コード、依存関係、バイナリ、画像のファイルは除外します。",
        "各仓库的代码、测试和文档行数,每天在全新的浅克隆上统计一次。生成文件、内置第三方代码、依赖、二进制文件和图片不计入。",
        "Linhas de código, testes e documentação de cada repositório, contadas uma vez por dia numa cópia superficial nova. Os ficheiros gerados, incluídos de terceiros, de dependências, binários e imagens ficam de fora."),
    "cd_help_summary": (
        "How is this counted?", "¿Cómo se cuenta?", "Wie wird gezählt?", "Comment est-ce compté ?",
        "Come si conta?", "どのように数えていますか?", "如何统计?", "Como é contado?"),
    "cd_help_body": (
        "Once a day the repositories of the ecosystems are cloned with depth 1 and every file is classified by its path and extension. Code lines are the lines that are not blank and not only a comment; a line with code and a comment counts as code, and a docstring counts as code. Test files are those in a test folder or with a test name; their cases are counted by the test marker of each language. Documentation is Markdown, reStructuredText, AsciiDoc and text files, the translated READMEs included; translation files are counted apart. JSON, YAML and similar data files are shown as data and never added to the code. Generated and vendored files (including those a .gitattributes marks linguist-generated), dependencies, build output, binaries, images and very long minified lines are excluded. The rules, the ecosystems and the type of each repository are in code-stats-config.json. The figures of {day} cover {n} repositories.",
        "Una vez al día se clonan con profundidad 1 los repositorios de los ecosistemas y cada archivo se clasifica por su ruta y extensión. Las líneas de código son las que no están en blanco ni son solo un comentario; una línea con código y comentario cuenta como código, y un docstring cuenta como código. Los archivos de pruebas son los de una carpeta de pruebas o con nombre de prueba; sus casos se cuentan por la marca de prueba de cada lenguaje. La documentación es Markdown, reStructuredText, AsciiDoc y archivos de texto, con los README traducidos incluidos; los archivos de traducción se cuentan aparte. JSON, YAML y datos similares se muestran como datos y nunca se suman al código. Se excluyen los archivos generados y vendorizados (también los que un .gitattributes marca como linguist-generated), las dependencias, la salida de compilación, los binarios, las imágenes y las líneas larguísimas de código minificado. Las reglas, los ecosistemas y el tipo de cada repositorio están en code-stats-config.json. Las cifras del {day} cubren {n} repositorios.",
        "Einmal täglich werden die Repositorys der Ökosysteme mit Tiefe 1 geklont und jede Datei nach Pfad und Endung eingeordnet. Codezeilen sind Zeilen, die weder leer noch nur ein Kommentar sind; eine Zeile mit Code und Kommentar zählt als Code, ein Docstring ebenfalls. Testdateien liegen in einem Testordner oder tragen einen Testnamen; ihre Testfälle werden über die Testmarke der jeweiligen Sprache gezählt. Dokumentation sind Markdown-, reStructuredText-, AsciiDoc- und Textdateien samt übersetzten READMEs; Übersetzungsdateien werden getrennt gezählt. JSON, YAML und ähnliche Datendateien erscheinen als Daten und werden nie zum Code addiert. Ausgeschlossen sind generierte und mitgelieferte Dateien (auch die, die eine .gitattributes als linguist-generated markiert), Abhängigkeiten, Build-Ausgaben, Binärdateien, Bilder und sehr lange minifizierte Zeilen. Die Regeln, die Ökosysteme und der Typ jedes Repositorys stehen in code-stats-config.json. Die Zahlen vom {day} umfassen {n} Repositorys.",
        "Une fois par jour, les dépôts des écosystèmes sont clonés avec une profondeur de 1 et chaque fichier est classé selon son chemin et son extension. Les lignes de code sont celles qui ne sont ni vides ni seulement un commentaire ; une ligne avec du code et un commentaire compte comme code, et une docstring aussi. Les fichiers de tests sont ceux d'un dossier de tests ou portant un nom de test ; leurs cas sont comptés par la marque de test de chaque langage. La documentation comprend Markdown, reStructuredText, AsciiDoc et les fichiers texte, README traduits inclus ; les fichiers de traduction sont comptés à part. JSON, YAML et fichiers de données semblables sont affichés comme données et jamais ajoutés au code. Sont exclus les fichiers générés et embarqués (y compris ceux qu'un .gitattributes marque linguist-generated), les dépendances, les sorties de compilation, les binaires, les images et les très longues lignes minifiées. Les règles, les écosystèmes et le type de chaque dépôt sont dans code-stats-config.json. Les chiffres du {day} couvrent {n} dépôts.",
        "Una volta al giorno i repository degli ecosistemi vengono clonati con profondità 1 e ogni file è classificato dal percorso e dall'estensione. Le righe di codice sono quelle né vuote né solo un commento; una riga con codice e commento conta come codice, e una docstring pure. I file di test sono quelli in una cartella di test o con un nome di test; i casi si contano con il marcatore di test di ogni linguaggio. La documentazione comprende Markdown, reStructuredText, AsciiDoc e file di testo, con i README tradotti; i file di traduzione si contano a parte. JSON, YAML e dati simili sono mostrati come dati e mai sommati al codice. Sono esclusi i file generati e inclusi da terzi (anche quelli che un .gitattributes marca linguist-generated), le dipendenze, l'output di compilazione, i binari, le immagini e le righe lunghissime minificate. Le regole, gli ecosistemi e il tipo di ogni repository sono in code-stats-config.json. I dati del {day} riguardano {n} repository.",
        "エコシステムのリポジトリを1日1回、深さ1でクローンし、パスと拡張子で各ファイルを分類します。コード行は空行でもコメントだけの行でもない行です。コードとコメントが同じ行にあればコード、docstring もコードとして数えます。テストファイルはテスト用フォルダ内、またはテスト名のファイルで、ケース数は各言語のテスト印で数えます。ドキュメントは Markdown、reStructuredText、AsciiDoc、テキストファイル(翻訳済み README を含む)で、翻訳ファイルは別に数えます。JSON や YAML などのデータファイルはデータとして表示し、コードには加算しません。生成ファイルと同梱コード(.gitattributes で linguist-generated と指定されたものを含む)、依存関係、ビルド出力、バイナリ、画像、非常に長い圧縮行は除外します。ルール、エコシステム、各リポジトリの種類は code-stats-config.json にあります。{day} の数値は {n} 件のリポジトリが対象です。",
        "每天对各生态系统的仓库以深度 1 克隆一次,并按路径和扩展名对每个文件分类。代码行指既不是空行、也不只是注释的行;同一行既有代码又有注释算作代码,docstring 也算作代码。测试文件位于测试目录或使用测试命名,其用例数按各语言的测试标记统计。文档包括 Markdown、reStructuredText、AsciiDoc 和文本文件(含已翻译的 README);翻译文件单独统计。JSON、YAML 等数据文件显示为数据,绝不计入代码。生成文件和内置第三方文件(包括 .gitattributes 标记为 linguist-generated 的)、依赖、构建产物、二进制文件、图片和超长的压缩行均被排除。规则、生态系统以及每个仓库的类型都在 code-stats-config.json 中。{day} 的数据涵盖 {n} 个仓库。",
        "Uma vez por dia os repositórios dos ecossistemas são clonados com profundidade 1 e cada ficheiro é classificado pelo caminho e pela extensão. As linhas de código são as que não estão em branco nem são apenas um comentário; uma linha com código e comentário conta como código, tal como um docstring. Os ficheiros de testes são os de uma pasta de testes ou com nome de teste; os casos são contados pela marca de teste de cada linguagem. A documentação é Markdown, reStructuredText, AsciiDoc e ficheiros de texto, incluindo os README traduzidos; os ficheiros de tradução são contados à parte. JSON, YAML e dados semelhantes aparecem como dados e nunca se somam ao código. Ficam de fora os ficheiros gerados e incluídos de terceiros (também os que um .gitattributes marca como linguist-generated), as dependências, a saída de compilação, os binários, as imagens e as linhas muito longas minificadas. As regras, os ecossistemas e o tipo de cada repositório estão em code-stats-config.json. Os valores de {day} abrangem {n} repositórios."),
    "cd_not_read": (
        "No code statistics could be read in this build, so nothing is verified.", "En esta compilación no se pudo leer ninguna estadística de código, así que nada está verificado.",
        "In diesem Build konnte keine Code-Statistik gelesen werden, daher ist nichts geprüft.", "Aucune statistique de code n'a pu être lue dans cette compilation, donc rien n'est vérifié.",
        "In questa build non è stato possibile leggere alcuna statistica del codice, quindi nulla è verificato.", "このビルドではコード統計を読み取れなかったため、何も確認されていません。",
        "此次构建未能读取任何代码统计,因此没有任何内容经过验证。", "Nesta compilação não foi possível ler nenhuma estatística de código, pelo que nada está verificado."),
    "cd_stale": (
        "These figures are {days} days old (counted on {date}).", "Estas cifras tienen {days} días (contadas el {date}).",
        "Diese Zahlen sind {days} Tage alt (gezählt am {date}).", "Ces chiffres datent de {days} jours (comptés le {date}).",
        "Questi dati hanno {days} giorni (contati il {date}).", "この数値は {days} 日前のものです({date} 集計)。",
        "这些数据已有 {days} 天(统计于 {date})。", "Estes valores têm {days} dias (contados em {date})."),
    "cd_unread_note": (
        "Not measured (could not be read and no earlier figures): {n}.", "No medido (no se pudo leer y no hay cifras anteriores): {n}.",
        "Nicht gemessen (nicht lesbar und keine früheren Zahlen): {n}.", "Non mesuré (illisible et sans chiffres antérieurs) : {n}.",
        "Non misurato (non leggibile e nessun dato precedente): {n}.", "未計測(読み取れず、以前の数値もなし):{n}。",
        "未测量(无法读取且没有先前的数据):{n}。", "Não medido (não foi possível ler e sem valores anteriores): {n}."),
    "cd_lastknown_note": (
        "Last known figures are shown for {n} repositories that could not be read in the last count.",
        "Se muestran las últimas cifras conocidas de {n} repositorios que no se pudieron leer en el último recuento.",
        "Für {n} Repositorys, die beim letzten Zählen nicht lesbar waren, werden die letzten bekannten Zahlen gezeigt.",
        "Les derniers chiffres connus sont affichés pour {n} dépôts illisibles lors du dernier comptage.",
        "Per {n} repository non leggibili nell'ultimo conteggio sono mostrati gli ultimi dati noti.",
        "前回の集計で読み取れなかった {n} 件のリポジトリは、最後に判明した数値を表示しています。",
        "上次统计中无法读取的 {n} 个仓库显示其最后已知数据。",
        "Para {n} repositórios que não foi possível ler na última contagem, são mostrados os últimos valores conhecidos."),
    "cd_k_repos": ("Repositories", "Repositorios", "Repositorys", "Dépôts", "Repository", "リポジトリ", "仓库", "Repositórios"),
    "cd_k_code": ("Lines of code", "Líneas de código", "Codezeilen", "Lignes de code", "Righe di codice", "コード行", "代码行", "Linhas de código"),
    "cd_k_comment": ("Comment lines", "Líneas de comentarios", "Kommentarzeilen", "Lignes de commentaires", "Righe di commento", "コメント行", "注释行", "Linhas de comentários"),
    "cd_k_blank": ("Blank lines", "Líneas en blanco", "Leerzeilen", "Lignes vides", "Righe vuote", "空行", "空行", "Linhas em branco"),
    "cd_k_tests": ("Lines of tests", "Líneas de pruebas", "Testzeilen", "Lignes de tests", "Righe di test", "テスト行", "测试行", "Linhas de testes"),
    "cd_k_docs": ("Lines of documentation", "Líneas de documentación", "Dokumentationszeilen", "Lignes de documentation", "Righe di documentazione", "ドキュメント行", "文档行", "Linhas de documentação"),
    "cd_k_l10n": ("Translation files", "Archivos de traducción", "Übersetzungsdateien", "Fichiers de traduction", "File di traduzione", "翻訳ファイル", "翻译文件", "Ficheiros de tradução"),
    "cd_k_files": ("Files counted", "Archivos contados", "Gezählte Dateien", "Fichiers comptés", "File contati", "集計したファイル", "统计的文件", "Ficheiros contados"),
    "cd_k_size": ("Size of the files", "Tamaño de los archivos", "Größe der Dateien", "Taille des fichiers", "Dimensione dei file", "ファイルサイズ", "文件大小", "Tamanho dos ficheiros"),
    "cd_k_cases": ("Test cases found", "Casos de prueba hallados", "Gefundene Testfälle", "Cas de test trouvés", "Casi di test trovati", "検出したテストケース", "发现的测试用例", "Casos de teste encontrados"),
    "cd_k_declared": ("Declared tests", "Pruebas declaradas", "Erklärte Tests", "Tests déclarés", "Test dichiarati", "宣言されたテスト", "声明的测试", "Testes declarados"),
    "cd_prop_title": (
        "Code, tests and documentation", "Código, pruebas y documentación", "Code, Tests und Dokumentation", "Code, tests et documentation",
        "Codice, test e documentazione", "コード、テスト、ドキュメント", "代码、测试和文档", "Código, testes e documentação"),
    "cd_prop_hint": (
        "Share of each kind of line in the total of every group. Tests are test files; documentation is text files including the translated READMEs.",
        "Proporción de cada tipo de línea en el total de cada grupo. Las pruebas son archivos de pruebas; la documentación son archivos de texto con los README traducidos.",
        "Anteil jeder Zeilenart an der Summe jeder Gruppe. Tests sind Testdateien; Dokumentation sind Textdateien samt übersetzten READMEs.",
        "Part de chaque type de ligne dans le total de chaque groupe. Les tests sont des fichiers de tests ; la documentation, des fichiers texte avec les README traduits.",
        "Quota di ogni tipo di riga nel totale di ogni gruppo. I test sono file di test; la documentazione è fatta di file di testo con i README tradotti.",
        "各グループの合計に占める行の種類ごとの割合です。テストはテストファイル、ドキュメントは翻訳済み README を含むテキストファイルです。",
        "各类行数在每组总数中所占的比例。测试指测试文件;文档指文本文件,含已翻译的 README。",
        "Proporção de cada tipo de linha no total de cada grupo. Os testes são ficheiros de testes; a documentação são ficheiros de texto, incluindo os README traduzidos."),
    "cd_prop_aria": (
        "Stacked bars of code, tests and documentation for the whole ecosystem, each ecosystem and each type; the table below has the same figures",
        "Barras apiladas de código, pruebas y documentación del conjunto, de cada ecosistema y de cada tipo; la tabla de abajo tiene las mismas cifras",
        "Gestapelte Balken für Code, Tests und Dokumentation des Ganzen, jedes Ökosystems und jedes Typs; die Tabelle darunter enthält dieselben Zahlen",
        "Barres empilées de code, tests et documentation pour l'ensemble, chaque écosystème et chaque type ; le tableau ci-dessous contient les mêmes chiffres",
        "Barre impilate di codice, test e documentazione per l'insieme, ogni ecosistema e ogni tipo; la tabella sotto ha gli stessi dati",
        "全体、各エコシステム、各種類のコード、テスト、ドキュメントの積み上げ棒グラフ。下の表に同じ数値があります",
        "整体、各生态系统和各类型的代码、测试和文档堆叠条形图;下方表格含有相同数据",
        "Barras empilhadas de código, testes e documentação do conjunto, de cada ecossistema e de cada tipo; a tabela abaixo tem os mesmos valores"),
    "cd_series_code": ("Code", "Código", "Code", "Code", "Codice", "コード", "代码", "Código"),
    "cd_series_tests": ("Tests", "Pruebas", "Tests", "Tests", "Test", "テスト", "测试", "Testes"),
    "cd_series_docs": ("Documentation", "Documentación", "Dokumentation", "Documentation", "Documentazione", "ドキュメント", "文档", "Documentação"),
    "cd_prop_tip": (
        "{name}: {code} lines of code ({pc} %), {tests} of tests ({pt} %), {docs} of documentation ({pd} %)",
        "{name}: {code} líneas de código ({pc} %), {tests} de pruebas ({pt} %), {docs} de documentación ({pd} %)",
        "{name}: {code} Codezeilen ({pc} %), {tests} Testzeilen ({pt} %), {docs} Dokumentationszeilen ({pd} %)",
        "{name} : {code} lignes de code ({pc} %), {tests} de tests ({pt} %), {docs} de documentation ({pd} %)",
        "{name}: {code} righe di codice ({pc}%), {tests} di test ({pt}%), {docs} di documentazione ({pd}%)",
        "{name}:コード {code} 行({pc}%)、テスト {tests} 行({pt}%)、ドキュメント {docs} 行({pd}%)",
        "{name}:代码 {code} 行({pc}%),测试 {tests} 行({pt}%),文档 {docs} 行({pd}%)",
        "{name}: {code} linhas de código ({pc} %), {tests} de testes ({pt} %), {docs} de documentação ({pd} %)"),
    "cd_all": ("All repositories", "Todos los repositorios", "Alle Repositorys", "Tous les dépôts", "Tutti i repository", "すべてのリポジトリ", "所有仓库", "Todos os repositórios"),
    "cd_by_eco": ("By ecosystem", "Por ecosistema", "Je Ökosystem", "Par écosystème", "Per ecosistema", "エコシステム別", "按生态系统", "Por ecossistema"),
    "cd_by_type": ("By type", "Por tipo", "Je Typ", "Par type", "Per tipo", "種類別", "按类型", "Por tipo"),
    "cd_by_repo": ("By repository", "Por repositorio", "Je Repository", "Par dépôt", "Per repository", "リポジトリ別", "按仓库", "Por repositório"),
    "cd_lang_title": (
        "Languages", "Lenguajes", "Sprachen", "Langages", "Linguaggi", "言語", "语言", "Linguagens"),
    "cd_lang_hint": (
        "Lines of code per programming language (tests included), for the whole ecosystem and for each ecosystem. The smallest languages are grouped as Other.",
        "Líneas de código por lenguaje de programación (pruebas incluidas), del conjunto y de cada ecosistema. Los lenguajes más pequeños se agrupan como Otros.",
        "Codezeilen je Programmiersprache (Tests eingeschlossen), für das Ganze und für jedes Ökosystem. Die kleinsten Sprachen sind als Andere zusammengefasst.",
        "Lignes de code par langage de programmation (tests inclus), pour l'ensemble et pour chaque écosystème. Les plus petits langages sont regroupés sous Autres.",
        "Righe di codice per linguaggio di programmazione (test inclusi), per l'insieme e per ogni ecosistema. I linguaggi più piccoli sono raggruppati in Altri.",
        "プログラミング言語ごとのコード行数(テストを含む)を、全体と各エコシステムについて示します。小さな言語は「その他」にまとめています。",
        "按编程语言统计的代码行数(含测试),分别为整体和各生态系统。较小的语言归入“其他”。",
        "Linhas de código por linguagem de programação (testes incluídos), do conjunto e de cada ecossistema. As linguagens mais pequenas são agrupadas em Outras."),
    "cd_lang_aria": (
        "Bars of the lines of code per language for the whole ecosystem and for each ecosystem; the table below has the same figures",
        "Barras de las líneas de código por lenguaje del conjunto y de cada ecosistema; la tabla de abajo tiene las mismas cifras",
        "Balken der Codezeilen je Sprache für das Ganze und jedes Ökosystem; die Tabelle darunter enthält dieselben Zahlen",
        "Barres des lignes de code par langage pour l'ensemble et chaque écosystème ; le tableau ci-dessous contient les mêmes chiffres",
        "Barre delle righe di codice per linguaggio per l'insieme e ogni ecosistema; la tabella sotto ha gli stessi dati",
        "全体と各エコシステムの言語別コード行数の棒グラフ。下の表に同じ数値があります",
        "整体和各生态系统按语言划分的代码行数条形图;下方表格含有相同数据",
        "Barras das linhas de código por linguagem do conjunto e de cada ecossistema; a tabela abaixo tem os mesmos valores"),
    "cd_lang_other": ("Other", "Otros", "Andere", "Autres", "Altri", "その他", "其他", "Outras"),
    "cd_lang_tip": (
        "{lang}: {code} lines of code ({pc} %), {comment} of comments, {blank} blank, in {files} files",
        "{lang}: {code} líneas de código ({pc} %), {comment} de comentarios, {blank} en blanco, en {files} archivos",
        "{lang}: {code} Codezeilen ({pc} %), {comment} Kommentare, {blank} leer, in {files} Dateien",
        "{lang} : {code} lignes de code ({pc} %), {comment} de commentaires, {blank} vides, dans {files} fichiers",
        "{lang}: {code} righe di codice ({pc}%), {comment} di commento, {blank} vuote, in {files} file",
        "{lang}:コード {code} 行({pc}%)、コメント {comment} 行、空行 {blank} 行、{files} ファイル",
        "{lang}:代码 {code} 行({pc}%),注释 {comment} 行,空行 {blank} 行,共 {files} 个文件",
        "{lang}: {code} linhas de código ({pc} %), {comment} de comentários, {blank} em branco, em {files} ficheiros"),
    "cd_lang_col": ("Language", "Lenguaje", "Sprache", "Langage", "Linguaggio", "言語", "语言", "Linguagem"),
    "cd_lang_files": ("Files", "Archivos", "Dateien", "Fichiers", "File", "ファイル", "文件", "Ficheiros"),
    "cd_lang_share": ("Share", "Proporción", "Anteil", "Part", "Quota", "割合", "占比", "Proporção"),
    "cd_evo_title": ("Evolution", "Evolución", "Entwicklung", "Évolution", "Evoluzione", "推移", "演变", "Evolução"),
    "cd_evo_hint": (
        "Lines per day from the daily snapshots (recent days one by one, older ones thinned out to one per week or month).",
        "Líneas por día a partir de las fotos diarias (los días recientes uno a uno, los antiguos reducidos a uno por semana o mes).",
        "Zeilen pro Tag aus den täglichen Momentaufnahmen (neuere Tage einzeln, ältere auf einen pro Woche oder Monat ausgedünnt).",
        "Lignes par jour d'après les instantanés quotidiens (les jours récents un à un, les anciens réduits à un par semaine ou par mois).",
        "Righe per giorno dalle istantanee giornaliere (i giorni recenti uno a uno, i più vecchi ridotti a uno a settimana o al mese).",
        "毎日のスナップショットから得た日ごとの行数です(最近の日は1日ずつ、古いものは週または月に1点へ間引き)。",
        "根据每日快照得出的每日行数(近期逐日,较早的按周或按月各保留一个点)。",
        "Linhas por dia a partir dos registos diários (os dias recentes um a um, os antigos reduzidos a um por semana ou mês)."),
    "cd_evo_total_title": (
        "Whole ecosystem", "Conjunto", "Gesamt", "Ensemble", "Insieme", "全体", "整体", "Conjunto"),
    "cd_evo_eco_title": (
        "By ecosystem", "Por ecosistema", "Je Ökosystem", "Par écosystème", "Per ecosistema", "エコシステム別", "按生态系统", "Por ecossistema"),
    "cd_evo_metric": ("Kind of line", "Tipo de línea", "Zeilenart", "Type de ligne", "Tipo di riga", "行の種類", "行类型", "Tipo de linha"),
    "cd_evo_none": (
        "There is no history yet.", "Todavía no hay historial.", "Es gibt noch keinen Verlauf.", "Il n'y a pas encore d'historique.",
        "Non c'è ancora una cronologia.", "履歴はまだありません。", "目前还没有历史记录。", "Ainda não há histórico."),
    "cd_evo_one": (
        "Only one day is recorded so far ({date}); a line needs at least two.", "Solo hay un día registrado por ahora ({date}); una línea necesita al menos dos.",
        "Bisher ist nur ein Tag erfasst ({date}); für eine Linie braucht es mindestens zwei.", "Un seul jour est enregistré pour l'instant ({date}) ; une ligne en demande au moins deux.",
        "Finora è registrato un solo giorno ({date}); una linea ne richiede almeno due.", "記録は今のところ1日分({date})だけで、線には2日分以上が必要です。",
        "目前仅记录了一天({date});画线至少需要两天。", "Até agora só há um dia registado ({date}); uma linha precisa de pelo menos dois."),
    "cd_evo_aria": (
        "Line chart of {metric} from {first} to {last}; the table below has the same figures",
        "Gráfica de líneas de {metric} del {first} al {last}; la tabla de abajo tiene las mismas cifras",
        "Liniendiagramm für {metric} vom {first} bis {last}; die Tabelle darunter enthält dieselben Zahlen",
        "Courbes de {metric} du {first} au {last} ; le tableau ci-dessous contient les mêmes chiffres",
        "Grafico a linee di {metric} dal {first} al {last}; la tabella sotto ha gli stessi dati",
        "{first} から {last} までの {metric} の折れ線グラフ。下の表に同じ数値があります",
        "{first} 至 {last} 的{metric}折线图;下方表格含有相同数据",
        "Gráfico de linhas de {metric} de {first} a {last}; a tabela abaixo tem os mesmos valores"),
    "cd_evo_point": (
        "{series} on {date}: {n}", "{series} el {date}: {n}", "{series} am {date}: {n}", "{series} le {date} : {n}", "{series} il {date}: {n}",
        "{date} の{series}:{n}", "{date} 的{series}:{n}", "{series} em {date}: {n}"),
    "cd_evo_date": ("Date", "Fecha", "Datum", "Date", "Data", "日付", "日期", "Data"),
    "cd_top_title": (
        "Largest repositories", "Repositorios más grandes", "Größte Repositorys", "Plus grands dépôts", "Repository più grandi", "規模の大きいリポジトリ", "规模最大的仓库", "Maiores repositórios"),
    "cd_top_hint": (
        "The repositories with most lines, stacked by code, tests and documentation.", "Los repositorios con más líneas, apiladas en código, pruebas y documentación.",
        "Die Repositorys mit den meisten Zeilen, gestapelt nach Code, Tests und Dokumentation.", "Les dépôts ayant le plus de lignes, empilées en code, tests et documentation.",
        "I repository con più righe, impilate in codice, test e documentazione.", "行数の多いリポジトリを、コード、テスト、ドキュメントで積み上げて示します。",
        "行数最多的仓库,按代码、测试和文档堆叠。", "Os repositórios com mais linhas, empilhadas em código, testes e documentação."),
    "cd_top_n": ("How many", "Cuántos", "Wie viele", "Combien", "Quanti", "表示件数", "显示数量", "Quantos"),
    "cd_top_aria": (
        "Stacked bars of the {n} repositories with most lines; the table below has the same figures",
        "Barras apiladas de los {n} repositorios con más líneas; la tabla de abajo tiene las mismas cifras",
        "Gestapelte Balken der {n} Repositorys mit den meisten Zeilen; die Tabelle darunter enthält dieselben Zahlen",
        "Barres empilées des {n} dépôts ayant le plus de lignes ; le tableau ci-dessous contient les mêmes chiffres",
        "Barre impilate dei {n} repository con più righe; la tabella sotto ha gli stessi dati",
        "行数の多い上位 {n} 件のリポジトリの積み上げ棒グラフ。下の表に同じ数値があります",
        "行数最多的 {n} 个仓库的堆叠条形图;下方表格含有相同数据",
        "Barras empilhadas dos {n} repositórios com mais linhas; a tabela abaixo tem os mesmos valores"),
    "cd_table_title": ("Detail", "Detalle", "Detail", "Détail", "Dettaglio", "詳細", "明细", "Detalhe"),
    "cd_table_hint": (
        "Click a column heading to sort. Filter by ecosystem and type, search by name or group the rows.",
        "Pulsa el encabezado de una columna para ordenar. Filtra por ecosistema y tipo, busca por nombre o agrupa las filas.",
        "Auf eine Spaltenüberschrift klicken, um zu sortieren. Nach Ökosystem und Typ filtern, nach Namen suchen oder Zeilen gruppieren.",
        "Cliquez sur un en-tête de colonne pour trier. Filtrez par écosystème et type, cherchez par nom ou regroupez les lignes.",
        "Fai clic sull'intestazione di una colonna per ordinare. Filtra per ecosistema e tipo, cerca per nome o raggruppa le righe.",
        "列見出しをクリックして並べ替えます。エコシステムと種類で絞り込み、名前で検索し、行をグループ化できます。",
        "点击列标题进行排序。可按生态系统和类型筛选、按名称搜索或对行分组。",
        "Clique no cabeçalho de uma coluna para ordenar. Filtre por ecossistema e tipo, procure por nome ou agrupe as linhas."),
    "cd_filter_eco": ("Ecosystem", "Ecosistema", "Ökosystem", "Écosystème", "Ecosistema", "エコシステム", "生态系统", "Ecossistema"),
    "cd_filter_type": ("Type", "Tipo", "Typ", "Type", "Tipo", "種類", "类型", "Tipo"),
    "cd_filter_all": ("All", "Todos", "Alle", "Tous", "Tutti", "すべて", "全部", "Todos"),
    "cd_group": ("Group rows by", "Agrupar filas por", "Zeilen gruppieren nach", "Regrouper les lignes par", "Raggruppa le righe per", "行のグループ化", "行分组方式", "Agrupar linhas por"),
    "cd_search": ("Search a repository", "Buscar un repositorio", "Repository suchen", "Chercher un dépôt", "Cerca un repository", "リポジトリを検索", "搜索仓库", "Procurar um repositório"),
    "cd_matches": ("{shown} of {total} rows", "{shown} de {total} filas", "{shown} von {total} Zeilen", "{shown} lignes sur {total}", "{shown} righe su {total}", "{total} 行中 {shown} 行", "共 {total} 行,显示 {shown} 行", "{shown} de {total} linhas"),
    "cd_none": (
        "No row matches the filters.", "Ninguna fila coincide con los filtros.", "Keine Zeile passt zu den Filtern.", "Aucune ligne ne correspond aux filtres.",
        "Nessuna riga corrisponde ai filtri.", "条件に一致する行はありません。", "没有符合筛选条件的行。", "Nenhuma linha corresponde aos filtros."),
    "cd_total": ("Total", "Total", "Gesamt", "Total", "Totale", "合計", "合计", "Total"),
    "cd_sorted": (
        "Sorted by {col}, {dir}", "Ordenado por {col}, {dir}", "Sortiert nach {col}, {dir}", "Trié par {col}, {dir}", "Ordinato per {col}, {dir}", "{col} で並べ替え({dir})", "按{col}排序,{dir}", "Ordenado por {col}, {dir}"),
    "cd_asc": ("ascending", "ascendente", "aufsteigend", "croissant", "crescente", "昇順", "升序", "ascendente"),
    "cd_desc": ("descending", "descendente", "absteigend", "décroissant", "decrescente", "降順", "降序", "descendente"),
    "cd_col_name": ("Repository", "Repositorio", "Repository", "Dépôt", "Repository", "リポジトリ", "仓库", "Repositório"),
    "cd_col_eco": ("Ecosystem", "Ecosistema", "Ökosystem", "Écosystème", "Ecosistema", "エコシステム", "生态系统", "Ecossistema"),
    "cd_col_type": ("Type", "Tipo", "Typ", "Type", "Tipo", "種類", "类型", "Tipo"),
    "cd_col_repos": ("Repositories", "Repositorios", "Repositorys", "Dépôts", "Repository", "リポジトリ数", "仓库数", "Repositórios"),
    "cd_col_code": ("Code", "Código", "Code", "Code", "Codice", "コード", "代码", "Código"),
    "cd_col_comment": ("Comments", "Comentarios", "Kommentare", "Commentaires", "Commenti", "コメント", "注释", "Comentários"),
    "cd_col_blank": ("Blank", "En blanco", "Leer", "Vides", "Vuote", "空行", "空行", "Em branco"),
    "cd_col_tests": ("Test lines", "Líneas de pruebas", "Testzeilen", "Lignes de tests", "Righe di test", "テスト行", "测试行", "Linhas de testes"),
    "cd_col_testfiles": ("Test files", "Archivos de pruebas", "Testdateien", "Fichiers de tests", "File di test", "テストファイル", "测试文件", "Ficheiros de testes"),
    "cd_col_cases": ("Cases found", "Casos hallados", "Gefundene Fälle", "Cas trouvés", "Casi trovati", "検出ケース", "发现用例", "Casos encontrados"),
    "cd_col_declared": ("Declared tests", "Pruebas declaradas", "Erklärte Tests", "Tests déclarés", "Test dichiarati", "宣言テスト", "声明测试", "Testes declarados"),
    "cd_col_docs": ("Documentation", "Documentación", "Dokumentation", "Documentation", "Documentazione", "ドキュメント", "文档", "Documentação"),
    "cd_col_l10n": ("Translation files", "Archivos de traducción", "Übersetzungsdateien", "Fichiers de traduction", "File di traduzione", "翻訳ファイル", "翻译文件", "Ficheiros de tradução"),
    "cd_col_size": ("Size", "Tamaño", "Größe", "Taille", "Dimensione", "サイズ", "大小", "Tamanho"),
    "cd_col_commit": ("Last commit", "Último commit", "Letzter Commit", "Dernier commit", "Ultimo commit", "最終コミット", "最近提交", "Último commit"),
    "cd_col_mix": ("Code / tests / docs", "Código / pruebas / docs", "Code / Tests / Doku", "Code / tests / docs", "Codice / test / doc", "コード/テスト/文書", "代码/测试/文档", "Código / testes / docs"),
    "cd_col_state": ("State", "Estado", "Status", "État", "Stato", "状態", "状态", "Estado"),
    "cd_st_lastknown": ("Last known", "Último conocido", "Zuletzt bekannt", "Dernier connu", "Ultimo noto", "最後に判明", "最后已知", "Último conhecido"),
    "cd_st_unread": ("Not measured", "No medido", "Nicht gemessen", "Non mesuré", "Non misurato", "未計測", "未测量", "Não medido"),
    "cd_st_ok": ("Measured", "Medido", "Gemessen", "Mesuré", "Misurato", "計測済み", "已测量", "Medido"),
    "cd_row_aria": (
        "{name}: {code} lines of code, {tests} of tests, {docs} of documentation", "{name}: {code} líneas de código, {tests} de pruebas, {docs} de documentación",
        "{name}: {code} Codezeilen, {tests} Testzeilen, {docs} Dokumentationszeilen", "{name} : {code} lignes de code, {tests} de tests, {docs} de documentation",
        "{name}: {code} righe di codice, {tests} di test, {docs} di documentazione", "{name}:コード {code} 行、テスト {tests} 行、ドキュメント {docs} 行",
        "{name}:代码 {code} 行,测试 {tests} 行,文档 {docs} 行", "{name}: {code} linhas de código, {tests} de testes, {docs} de documentação"),
    "cd_type_firmware": ("Firmware", "Firmware", "Firmware", "Firmware", "Firmware", "ファームウェア", "固件", "Firmware"),
    "cd_type_apps": ("Apps", "Aplicaciones", "Apps", "Applications", "App", "アプリ", "应用", "Aplicações"),
    "cd_type_services": ("Services", "Servicios", "Dienste", "Services", "Servizi", "サービス", "服务", "Serviços"),
    "cd_type_tools": ("Tools", "Herramientas", "Werkzeuge", "Outils", "Strumenti", "ツール", "工具", "Ferramentas"),
    "cd_type_docs": ("Documentation", "Documentación", "Dokumentation", "Documentation", "Documentazione", "ドキュメント", "文档", "Documentação"),
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
