#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_scripts_texts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Texts of the tab "Scripts" (the workflows and own scripts of every repository) in the eight languages.

Each entry is (en, es, de, fr, it, ja, zh, pt); portuguese is the one of Portugal. dashboard_code_texts.py merges these rows into its own table, which is
the one the page generator reads (the shared words of the Code tab - columns, filters, grouping, total - are used from there). Stdlib only.
"""
from __future__ import annotations

ROWS: dict[str, tuple[str, str, str, str, str, str, str, str]] = {
    "tab_scripts": ("Scripts", "Scripts", "Skripte", "Scripts", "Script", "スクリプト", "脚本", "Scripts"),
    "sc_title": (
        "Workflows and scripts", "Workflows y scripts", "Workflows und Skripte", "Workflows et scripts", "Workflow e script", "ワークフローとスクリプト", "工作流与脚本", "Workflows e scripts"),
    "sc_badge": (
        "Read from the repositories", "Leído de los repositorios", "Aus den Repositorys gelesen", "Lu dans les dépôts", "Letto dai repository", "リポジトリから取得", "读取自各仓库", "Lido dos repositórios"),
    "sc_hint": (
        "The GitHub workflows of every repository (when they run, the actions they use and how the version of each action is fixed) and the scripts of its tools/ and scripts/ folders by language. Read once a day from a fresh shallow copy; nothing is run.",
        "Los workflows de GitHub de cada repositorio (cuándo se ejecutan, las acciones que usan y cómo se fija la versión de cada acción) y los scripts de sus carpetas tools/ y scripts/ por lenguaje. Se leen una vez al día de una copia superficial nueva; no se ejecuta nada.",
        "Die GitHub-Workflows jedes Repositorys (wann sie laufen, welche Actions sie nutzen und wie die Version jeder Action festgelegt ist) und die Skripte aus tools/ und scripts/ nach Sprache. Einmal täglich aus einer frischen flachen Kopie gelesen; nichts wird ausgeführt.",
        "Les workflows GitHub de chaque dépôt (quand ils s'exécutent, les actions utilisées et comment la version de chaque action est fixée) et les scripts de ses dossiers tools/ et scripts/ par langage. Lus une fois par jour sur une copie superficielle neuve ; rien n'est exécuté.",
        "I workflow GitHub di ogni repository (quando vengono eseguiti, le azioni usate e come è fissata la versione di ogni azione) e gli script delle cartelle tools/ e scripts/ per linguaggio. Letti una volta al giorno da una copia superficiale nuova; non viene eseguito nulla.",
        "各リポジトリの GitHub ワークフロー(実行のタイミング、使用するアクション、各アクションのバージョンの固定方法)と、tools/ と scripts/ フォルダーのスクリプトを言語別に表示します。毎日新しい浅いコピーから読み取り、何も実行しません。",
        "各仓库的 GitHub 工作流(何时运行、使用的动作以及每个动作的版本如何固定),以及 tools/ 和 scripts/ 文件夹中按语言划分的脚本。每天从全新的浅克隆读取一次,不会运行任何内容。",
        "Os workflows do GitHub de cada repositório (quando correm, as ações que usam e como a versão de cada ação é fixada) e os scripts das pastas tools/ e scripts/ por linguagem. Lidos uma vez por dia numa cópia superficial nova; nada é executado."),
    "sc_help_summary": (
        "How is this counted?", "¿Cómo se cuenta?", "Wie wird gezählt?", "Comment est-ce compté ?", "Come si conta?", "どのように数えますか?", "如何统计?", "Como se conta?"),
    "sc_help_body": (
        "A workflow is a file of .github/workflows. Its triggers are the events under on:, its jobs the entries under jobs:, and every uses: of its steps is an action; the version of an action is fixed to a full commit (sha), to a version tag such as v4 (tag), or to a branch or nothing (branch). Whether a pinned action is out of date is not known without asking GitHub, so it is not said. Scripts are the .py, .sh, .ps1, .bat/.cmd and .js/.ts files under tools/ and scripts/. Counted on {n} repositories, last read on {day}.",
        "Un workflow es un archivo de .github/workflows. Sus disparadores son los eventos bajo on:, sus jobs las entradas bajo jobs:, y cada uses: de sus pasos es una acción; la versión de una acción se fija a un commit completo (sha), a una etiqueta de versión como v4 (tag) o a una rama o a nada (branch). Si una acción fijada está desactualizada no se sabe sin preguntar a GitHub, así que no se dice. Los scripts son los archivos .py, .sh, .ps1, .bat/.cmd y .js/.ts de tools/ y scripts/. Contado en {n} repositorios, última lectura el {day}.",
        "Ein Workflow ist eine Datei in .github/workflows. Seine Auslöser sind die Ereignisse unter on:, seine Jobs die Einträge unter jobs:, und jedes uses: seiner Schritte ist eine Action; die Version einer Action ist an einen vollständigen Commit (sha), an einen Versions-Tag wie v4 (tag) oder an einen Branch bzw. nichts (branch) gebunden. Ob eine festgelegte Action veraltet ist, lässt sich ohne Anfrage an GitHub nicht sagen, daher wird es nicht behauptet. Skripte sind die Dateien .py, .sh, .ps1, .bat/.cmd und .js/.ts unter tools/ und scripts/. Gezählt in {n} Repositorys, zuletzt gelesen am {day}.",
        "Un workflow est un fichier de .github/workflows. Ses déclencheurs sont les événements sous on:, ses jobs les entrées sous jobs:, et chaque uses: de ses étapes est une action ; la version d'une action est fixée à un commit complet (sha), à une étiquette de version comme v4 (tag) ou à une branche ou à rien (branch). Savoir si une action fixée est périmée exige d'interroger GitHub, donc ce n'est pas dit. Les scripts sont les fichiers .py, .sh, .ps1, .bat/.cmd et .js/.ts de tools/ et scripts/. Compté sur {n} dépôts, dernière lecture le {day}.",
        "Un workflow è un file di .github/workflows. I suoi trigger sono gli eventi sotto on:, i suoi job le voci sotto jobs:, e ogni uses: dei suoi passi è un'azione; la versione di un'azione è fissata a un commit completo (sha), a un tag di versione come v4 (tag) o a un ramo o a nulla (branch). Se un'azione fissata sia obsoleta non si sa senza interrogare GitHub, quindi non lo si dice. Gli script sono i file .py, .sh, .ps1, .bat/.cmd e .js/.ts in tools/ e scripts/. Contati su {n} repository, ultima lettura il {day}.",
        "ワークフローは .github/workflows のファイルです。トリガーは on: の下のイベント、ジョブは jobs: の下の項目、各ステップの uses: がアクションです。アクションのバージョンは、完全なコミット(sha)、v4 のようなバージョンタグ(tag)、またはブランチか指定なし(branch)で固定されます。固定されたアクションが古いかどうかは GitHub に問い合わせないと分からないため、表示しません。スクリプトは tools/ と scripts/ の .py、.sh、.ps1、.bat/.cmd、.js/.ts ファイルです。{n} 件のリポジトリを集計、最終読み取り {day}。",
        "工作流是 .github/workflows 中的文件。触发器是 on: 下的事件,作业是 jobs: 下的条目,步骤中的每个 uses: 是一个动作;动作的版本固定为完整提交(sha)、v4 这样的版本标签(tag),或分支或未指定(branch)。已固定的动作是否过期必须询问 GitHub 才能知道,因此不作说明。脚本是 tools/ 和 scripts/ 下的 .py、.sh、.ps1、.bat/.cmd 和 .js/.ts 文件。统计了 {n} 个仓库,最近读取于 {day}。",
        "Um workflow é um ficheiro de .github/workflows. Os seus disparadores são os eventos em on:, os jobs as entradas em jobs:, e cada uses: dos seus passos é uma ação; a versão de uma ação é fixada a um commit completo (sha), a uma etiqueta de versão como v4 (tag) ou a um ramo ou a nada (branch). Saber se uma ação fixada está desatualizada exige perguntar ao GitHub, por isso não se diz. Os scripts são os ficheiros .py, .sh, .ps1, .bat/.cmd e .js/.ts de tools/ e scripts/. Contado em {n} repositórios, última leitura em {day}."),
    "sc_not_read": (
        "No workflow or script figures could be read in this build, so nothing is verified.", "En esta compilación no se pudo leer ninguna cifra de workflows o scripts, así que nada está verificado.",
        "In diesem Build konnten keine Workflow- oder Skriptzahlen gelesen werden, daher ist nichts geprüft.", "Aucun chiffre de workflows ou de scripts n'a pu être lu dans cette compilation, donc rien n'est vérifié.",
        "In questa build non è stato possibile leggere alcuna cifra di workflow o script, quindi nulla è verificato.", "このビルドではワークフローとスクリプトの数値を読み取れなかったため、何も確認されていません。",
        "此次构建未能读取任何工作流或脚本数据,因此没有任何内容经过验证。", "Nesta compilação não foi possível ler nenhum número de workflows ou scripts, pelo que nada está verificado."),
    "sc_stale": (
        "The figures are {days} days old (read on {date}).", "Las cifras tienen {days} días (leídas el {date}).", "Die Zahlen sind {days} Tage alt (gelesen am {date}).",
        "Les chiffres datent de {days} jours (lus le {date}).", "Le cifre hanno {days} giorni (lette il {date}).", "数値は {days} 日前のものです({date} に読み取り)。",
        "数据已有 {days} 天(读取于 {date})。", "Os números têm {days} dias (lidos em {date})."),
    "sc_k_repos": ("Repositories with workflows", "Repositorios con workflows", "Repositorys mit Workflows", "Dépôts avec workflows", "Repository con workflow", "ワークフローのあるリポジトリ", "有工作流的仓库", "Repositórios com workflows"),
    "sc_k_workflows": ("Workflows", "Workflows", "Workflows", "Workflows", "Workflow", "ワークフロー", "工作流", "Workflows"),
    "sc_k_jobs": ("Jobs", "Jobs", "Jobs", "Jobs", "Job", "ジョブ", "作业", "Jobs"),
    "sc_k_uses": ("Uses of actions", "Usos de acciones", "Verwendete Actions", "Usages d'actions", "Usi di azioni", "アクションの使用", "动作使用次数", "Usos de ações"),
    "sc_k_unpinned": ("Not pinned to a commit", "Sin fijar a un commit", "Nicht an einen Commit gebunden", "Non fixées à un commit", "Non fissate a un commit", "コミットに固定されていない", "未固定到提交", "Sem fixar a um commit"),
    "sc_k_files": ("Own script files", "Archivos de script propios", "Eigene Skriptdateien", "Fichiers de script propres", "File di script propri", "独自のスクリプトファイル", "自有脚本文件", "Ficheiros de script próprios"),
    "sc_k_lines": ("Script lines", "Líneas de script", "Skriptzeilen", "Lignes de script", "Righe di script", "スクリプトの行数", "脚本行数", "Linhas de script"),
    "sc_trig_push": ("Push", "Push", "Push", "Push", "Push", "プッシュ", "推送", "Push"),
    "sc_trig_pull_request": ("Pull request", "Pull request", "Pull Request", "Pull request", "Pull request", "プルリクエスト", "拉取请求", "Pull request"),
    "sc_trig_schedule": ("Schedule", "Programado", "Zeitplan", "Planifié", "Pianificato", "スケジュール", "定时", "Agendado"),
    "sc_trig_workflow_dispatch": ("By hand", "A mano", "Von Hand", "À la main", "A mano", "手動", "手动", "Manual"),
    "sc_trig_release": ("Release", "Release", "Release", "Release", "Release", "リリース", "发布", "Release"),
    "sc_trig_workflow_run": ("After another workflow", "Tras otro workflow", "Nach einem anderen Workflow", "Après un autre workflow", "Dopo un altro workflow", "別のワークフローの後", "在另一工作流之后", "Após outro workflow"),
    "sc_trig_workflow_call": ("Called by another", "Llamado por otro", "Von einem anderen aufgerufen", "Appelé par un autre", "Chiamato da un altro", "他から呼び出し", "被其他调用", "Chamado por outro"),
    "sc_trig_other": ("Other event", "Otro evento", "Anderes Ereignis", "Autre événement", "Altro evento", "その他のイベント", "其他事件", "Outro evento"),
    "sc_pin_sha": ("Pinned to a commit", "Fijada a un commit", "An einen Commit gebunden", "Fixée à un commit", "Fissata a un commit", "コミットに固定", "固定到提交", "Fixada a um commit"),
    "sc_pin_tag": ("Version tag", "Etiqueta de versión", "Versions-Tag", "Étiquette de version", "Tag di versione", "バージョンタグ", "版本标签", "Etiqueta de versão"),
    "sc_pin_branch": ("Branch or no version", "Rama o sin versión", "Branch oder keine Version", "Branche ou sans version", "Ramo o senza versione", "ブランチまたは指定なし", "分支或无版本", "Ramo ou sem versão"),
    "sc_pin_local": ("This repository", "Este repositorio", "Dieses Repository", "Ce dépôt", "Questo repository", "このリポジトリ", "本仓库", "Este repositório"),
    "sc_pin_docker": ("Container image", "Imagen de contenedor", "Container-Image", "Image de conteneur", "Immagine del container", "コンテナイメージ", "容器镜像", "Imagem de contentor"),
    "sc_lang_py": ("Python", "Python", "Python", "Python", "Python", "Python", "Python", "Python"),
    "sc_lang_sh": ("Shell", "Shell", "Shell", "Shell", "Shell", "シェル", "Shell", "Shell"),
    "sc_lang_ps1": ("PowerShell", "PowerShell", "PowerShell", "PowerShell", "PowerShell", "PowerShell", "PowerShell", "PowerShell"),
    "sc_lang_bat": ("Batch", "Batch", "Batch", "Batch", "Batch", "バッチ", "批处理", "Batch"),
    "sc_lang_js": ("JavaScript / TypeScript", "JavaScript / TypeScript", "JavaScript / TypeScript", "JavaScript / TypeScript", "JavaScript / TypeScript", "JavaScript / TypeScript", "JavaScript / TypeScript", "JavaScript / TypeScript"),
    "sc_trig_title": (
        "When the workflows run", "Cuándo se ejecutan los workflows", "Wann die Workflows laufen", "Quand les workflows s'exécutent", "Quando vengono eseguiti i workflow", "ワークフローの実行タイミング", "工作流何时运行", "Quando correm os workflows"),
    "sc_trig_hint": (
        "Workflows per trigger for the whole, each ecosystem and each type; a workflow with several triggers counts once for each.",
        "Workflows por disparador para el conjunto, cada ecosistema y cada tipo; un workflow con varios disparadores cuenta una vez por cada uno.",
        "Workflows je Auslöser für das Ganze, jedes Ökosystem und jeden Typ; ein Workflow mit mehreren Auslösern zählt für jeden einmal.",
        "Workflows par déclencheur pour l'ensemble, chaque écosystème et chaque type ; un workflow à plusieurs déclencheurs compte une fois pour chacun.",
        "Workflow per trigger per l'insieme, ogni ecosistema e ogni tipo; un workflow con più trigger conta una volta per ciascuno.",
        "全体、各エコシステム、各種類のトリガーごとのワークフロー数。複数のトリガーを持つワークフローはそれぞれに 1 回数えます。",
        "整体、各生态系统和各类型按触发器统计的工作流;有多个触发器的工作流对每个触发器各计一次。",
        "Workflows por disparador para o conjunto, cada ecossistema e cada tipo; um workflow com vários disparadores conta uma vez por cada um."),
    "sc_pin_title": (
        "How the actions are pinned", "Cómo se fijan las acciones", "Wie die Actions festgelegt sind", "Comment les actions sont fixées", "Come sono fissate le azioni", "アクションの固定方法", "动作如何固定", "Como as ações são fixadas"),
    "sc_pin_hint": (
        "Uses of actions by how their version is fixed, for the whole, each ecosystem and each type. A full commit cannot move; a tag or a branch can.",
        "Usos de acciones según cómo se fija su versión, para el conjunto, cada ecosistema y cada tipo. Un commit completo no se puede mover; una etiqueta o una rama sí.",
        "Verwendete Actions danach, wie ihre Version festgelegt ist, für das Ganze, jedes Ökosystem und jeden Typ. Ein vollständiger Commit kann sich nicht ändern; ein Tag oder ein Branch schon.",
        "Usages d'actions selon la façon dont leur version est fixée, pour l'ensemble, chaque écosystème et chaque type. Un commit complet ne peut pas bouger ; une étiquette ou une branche, si.",
        "Usi di azioni secondo come è fissata la loro versione, per l'insieme, ogni ecosistema e ogni tipo. Un commit completo non può spostarsi; un tag o un ramo sì.",
        "バージョンの固定方法ごとのアクション使用数(全体、各エコシステム、各種類)。完全なコミットは動きませんが、タグやブランチは動きます。",
        "按版本固定方式统计的动作使用次数(整体、各生态系统和各类型)。完整提交不会移动,标签或分支则可能移动。",
        "Usos de ações segundo a forma como a versão é fixada, para o conjunto, cada ecossistema e cada tipo. Um commit completo não se move; uma etiqueta ou um ramo pode mover-se."),
    "sc_top_title": (
        "Most used actions", "Acciones más usadas", "Am häufigsten genutzte Actions", "Actions les plus utilisées", "Azioni più usate", "最もよく使われるアクション", "使用最多的动作", "Ações mais usadas"),
    "sc_top_hint": (
        "The actions used most often (the repository of the owner included), stacked by how their version is fixed.",
        "Las acciones más usadas (incluidas las del propio titular), apiladas según cómo se fija su versión.",
        "Die am häufigsten genutzten Actions (auch die des Eigentümers), gestapelt danach, wie ihre Version festgelegt ist.",
        "Les actions les plus utilisées (celles du propriétaire comprises), empilées selon la façon dont leur version est fixée.",
        "Le azioni più usate (comprese quelle del titolare), impilate secondo come è fissata la loro versione.",
        "最もよく使われるアクション(所有者自身のものを含む)を、バージョンの固定方法ごとに積み上げて表示します。",
        "使用最多的动作(含所有者自己的),按版本固定方式堆叠。",
        "As ações mais usadas (incluindo as do próprio titular), empilhadas segundo a forma como a versão é fixada."),
    "sc_lang_title": (
        "Scripts by language", "Scripts por lenguaje", "Skripte nach Sprache", "Scripts par langage", "Script per linguaggio", "言語別のスクリプト", "按语言划分的脚本", "Scripts por linguagem"),
    "sc_lang_hint": (
        "Files of tools/ and scripts/ by language, for the whole and for each ecosystem.",
        "Archivos de tools/ y scripts/ por lenguaje, para el conjunto y para cada ecosistema.",
        "Dateien aus tools/ und scripts/ nach Sprache, für das Ganze und für jedes Ökosystem.",
        "Fichiers de tools/ et scripts/ par langage, pour l'ensemble et pour chaque écosystème.",
        "File di tools/ e scripts/ per linguaggio, per l'insieme e per ogni ecosistema.",
        "tools/ と scripts/ のファイルを言語別に、全体と各エコシステムについて表示します。",
        "tools/ 和 scripts/ 中按语言划分的文件,整体及各生态系统。",
        "Ficheiros de tools/ e scripts/ por linguagem, para o conjunto e para cada ecossistema."),
    "sc_rank_title": (
        "Repositories with most workflows", "Repositorios con más workflows", "Repositorys mit den meisten Workflows", "Dépôts avec le plus de workflows", "Repository con più workflow", "ワークフローが最も多いリポジトリ", "工作流最多的仓库", "Repositórios com mais workflows"),
    "sc_rank_hint": (
        "The repositories with most workflows, stacked by trigger.", "Los repositorios con más workflows, apilados por disparador.", "Die Repositorys mit den meisten Workflows, gestapelt nach Auslöser.",
        "Les dépôts avec le plus de workflows, empilés par déclencheur.", "I repository con più workflow, impilati per trigger.", "ワークフローが最も多いリポジトリを、トリガー別に積み上げて表示します。",
        "工作流最多的仓库,按触发器堆叠。", "Os repositórios com mais workflows, empilhados por disparador."),
    "sc_unp_title": (
        "Actions not pinned to a commit", "Acciones sin fijar a un commit", "Actions ohne Bindung an einen Commit", "Actions non fixées à un commit", "Azioni non fissate a un commit", "コミットに固定されていないアクション", "未固定到提交的动作", "Ações sem fixar a um commit"),
    "sc_unp_hint": (
        "Actions of other owners whose version is a tag or a branch, with the number of uses and of repositories.",
        "Acciones de otros titulares cuya versión es una etiqueta o una rama, con el número de usos y de repositorios.",
        "Actions anderer Eigentümer, deren Version ein Tag oder ein Branch ist, mit der Zahl der Verwendungen und der Repositorys.",
        "Actions d'autres propriétaires dont la version est une étiquette ou une branche, avec le nombre d'usages et de dépôts.",
        "Azioni di altri titolari la cui versione è un tag o un ramo, con il numero di usi e di repository.",
        "バージョンがタグまたはブランチである他の所有者のアクションを、使用回数とリポジトリ数とともに表示します。",
        "版本为标签或分支的其他所有者的动作,附使用次数和仓库数。",
        "Ações de outros titulares cuja versão é uma etiqueta ou um ramo, com o número de usos e de repositórios."),
    "sc_unp_none": (
        "Every action of another owner is pinned to a commit.", "Todas las acciones de otros titulares están fijadas a un commit.", "Jede Action anderer Eigentümer ist an einen Commit gebunden.",
        "Toutes les actions d'autres propriétaires sont fixées à un commit.", "Ogni azione di altri titolari è fissata a un commit.", "他の所有者のアクションはすべてコミットに固定されています。",
        "其他所有者的所有动作均已固定到提交。", "Todas as ações de outros titulares estão fixadas a um commit."),
    "sc_unp_row": (
        "{n} uses in {r} repositories", "{n} usos en {r} repositorios", "{n} Verwendungen in {r} Repositorys", "{n} usages dans {r} dépôts", "{n} usi in {r} repository", "{r} 件のリポジトリで {n} 回使用", "在 {r} 个仓库中使用 {n} 次", "{n} usos em {r} repositórios"),
    "sc_table_title": (
        "Workflows and scripts by repository", "Workflows y scripts por repositorio", "Workflows und Skripte je Repository", "Workflows et scripts par dépôt", "Workflow e script per repository", "リポジトリ別のワークフローとスクリプト", "按仓库统计的工作流与脚本", "Workflows e scripts por repositório"),
    "sc_table_hint": (
        "Sort with the column headings, filter by ecosystem or type, search by name, and group the rows by ecosystem or type.",
        "Ordena con los encabezados de columna, filtra por ecosistema o tipo, busca por nombre y agrupa las filas por ecosistema o tipo.",
        "Mit den Spaltenköpfen sortieren, nach Ökosystem oder Typ filtern, nach Namen suchen und die Zeilen nach Ökosystem oder Typ gruppieren.",
        "Triez avec les en-têtes de colonne, filtrez par écosystème ou type, cherchez par nom et regroupez les lignes par écosystème ou type.",
        "Ordina con le intestazioni di colonna, filtra per ecosistema o tipo, cerca per nome e raggruppa le righe per ecosistema o tipo.",
        "列見出しで並べ替え、エコシステムや種類で絞り込み、名前で検索し、行をエコシステムや種類でまとめられます。",
        "可用列标题排序,按生态系统或类型筛选,按名称搜索,并按生态系统或类型分组。",
        "Ordene com os cabeçalhos das colunas, filtre por ecossistema ou tipo, pesquise por nome e agrupe as linhas por ecossistema ou tipo."),
    "sc_col_wf": ("Workflows", "Workflows", "Workflows", "Workflows", "Workflow", "ワークフロー", "工作流", "Workflows"),
    "sc_col_jobs": ("Jobs", "Jobs", "Jobs", "Jobs", "Job", "ジョブ", "作业", "Jobs"),
    "sc_col_acts": ("Action uses", "Usos de acciones", "Action-Verwendungen", "Usages d'actions", "Usi di azioni", "アクション使用", "动作使用", "Usos de ações"),
    "sc_col_unp": ("Not pinned", "Sin fijar", "Nicht gebunden", "Non fixées", "Non fissate", "未固定", "未固定", "Sem fixar"),
    "sc_col_sched": ("Scheduled", "Programados", "Zeitgesteuert", "Planifiés", "Pianificati", "スケジュール", "定时", "Agendados"),
    "sc_col_manual": ("By hand", "A mano", "Von Hand", "À la main", "A mano", "手動", "手动", "Manual"),
    "sc_col_files": ("Script files", "Archivos de script", "Skriptdateien", "Fichiers de script", "File di script", "スクリプトファイル", "脚本文件", "Ficheiros de script"),
    "sc_col_lines": ("Script lines", "Líneas de script", "Skriptzeilen", "Lignes de script", "Righe di script", "スクリプト行数", "脚本行数", "Linhas de script"),
    "sc_col_mix": ("Languages", "Lenguajes", "Sprachen", "Langages", "Linguaggi", "言語", "语言", "Linguagens"),
    "sc_tip_trig": (
        "{name}: {n} workflows ({pc} %)", "{name}: {n} workflows ({pc} %)", "{name}: {n} Workflows ({pc} %)", "{name} : {n} workflows ({pc} %)", "{name}: {n} workflow ({pc} %)", "{name}: {n} ワークフロー({pc} %)", "{name}:{n} 个工作流({pc} %)", "{name}: {n} workflows ({pc} %)"),
    "sc_tip_pin": (
        "{name}: {n} uses ({pc} %)", "{name}: {n} usos ({pc} %)", "{name}: {n} Verwendungen ({pc} %)", "{name} : {n} usages ({pc} %)", "{name}: {n} usi ({pc} %)", "{name}: {n} 回({pc} %)", "{name}:{n} 次({pc} %)", "{name}: {n} usos ({pc} %)"),
    "sc_tip_lang": (
        "{name}: {n} files ({pc} %)", "{name}: {n} archivos ({pc} %)", "{name}: {n} Dateien ({pc} %)", "{name} : {n} fichiers ({pc} %)", "{name}: {n} file ({pc} %)", "{name}: {n} ファイル({pc} %)", "{name}:{n} 个文件({pc} %)", "{name}: {n} ficheiros ({pc} %)"),
    "sc_aria_trig": (
        "Workflows by trigger", "Workflows por disparador", "Workflows nach Auslöser", "Workflows par déclencheur", "Workflow per trigger", "トリガー別のワークフロー", "按触发器统计的工作流", "Workflows por disparador"),
    "sc_aria_pin": (
        "Uses of actions by how the version is fixed", "Usos de acciones según cómo se fija la versión", "Verwendete Actions nach Festlegung der Version", "Usages d'actions selon la fixation de la version", "Usi di azioni secondo la fissazione della versione", "バージョンの固定方法別のアクション使用", "按版本固定方式统计的动作使用", "Usos de ações segundo a fixação da versão"),
    "sc_aria_top": (
        "Most used actions", "Acciones más usadas", "Am häufigsten genutzte Actions", "Actions les plus utilisées", "Azioni più usate", "最もよく使われるアクション", "使用最多的动作", "Ações mais usadas"),
    "sc_aria_lang": (
        "Script files by language", "Archivos de script por lenguaje", "Skriptdateien nach Sprache", "Fichiers de script par langage", "File di script per linguaggio", "言語別のスクリプトファイル", "按语言划分的脚本文件", "Ficheiros de script por linguagem"),
    "sc_aria_rank": (
        "Repositories with most workflows", "Repositorios con más workflows", "Repositorys mit den meisten Workflows", "Dépôts avec le plus de workflows", "Repository con più workflow", "ワークフローが最も多いリポジトリ", "工作流最多的仓库", "Repositórios com mais workflows"),
    'sc_lint_title': ('Workflow lint: three levels', 'Lint de workflows: tres niveles', 'Workflow-Lint: drei Stufen', 'Lint des workflows : trois niveaux', 'Lint dei workflow: tre livelli', 'ワークフローの lint:3 段階', '工作流检查:三个级别', 'Lint dos workflows: três níveis'),
    'sc_lint_hint': (
        'The same rules and the same three levels as the local Actions monitor: information, warning and error. Actions not pinned to a commit, workflows with no permissions block, what looks like a secret written in the file, text of outsiders pasted into a script and a pull-request-target that checks out the pull request. Only counts are kept: never a value, a name or a line.',
        'Las mismas reglas y los mismos tres niveles que el monitor local de Actions: información, aviso y error. Acciones sin fijar a un commit, workflows sin bloque de permisos, lo que parece un secreto escrito en el archivo, texto de terceros pegado en un script y un pull-request-target que descarga el pull request. Solo se guardan recuentos: nunca un valor, un nombre ni una línea.',
        'Dieselben Regeln und dieselben drei Stufen wie der lokale Actions-Monitor: Information, Warnung und Fehler. Actions ohne Bindung an einen Commit, Workflows ohne permissions-Block, etwas, das wie ein Geheimnis in der Datei aussieht, fremder Text in einem Skript und ein pull-request-target, der den Pull Request auscheckt. Gespeichert werden nur Zahlen: nie ein Wert, ein Name oder eine Zeile.',
        "Les mêmes règles et les trois mêmes niveaux que le moniteur local d'Actions : information, avertissement et erreur. Actions non fixées à un commit, workflows sans bloc de permissions, ce qui ressemble à un secret écrit dans le fichier, texte de tiers collé dans un script et un pull-request-target qui récupère la pull request. Seuls des totaux sont conservés : jamais une valeur, un nom ni une ligne.",
        'Le stesse regole e gli stessi tre livelli del monitor locale di Actions: informazione, avviso ed errore. Azioni non fissate a un commit, workflow senza blocco permissions, ciò che sembra un segreto scritto nel file, testo di terzi incollato in uno script e un pull-request-target che scarica la pull request. Si conservano solo conteggi: mai un valore, un nome o una riga.',
        'ローカルの Actions モニターと同じルール、同じ 3 段階(情報・警告・エラー)です。コミットに固定されていないアクション、permissions ブロックのないワークフロー、ファイルに書かれた秘密情報らしきもの、第三者のテキストのスクリプトへの貼り付け、プルリクエストをチェックアウトする pull-request-target を対象にします。保存するのは件数だけで、値・名前・行は保持しません。',
        '与本地 Actions 监视器相同的规则和相同的三个级别:信息、警告和错误。涉及未固定到提交的动作、没有 permissions 块的工作流、文件中疑似密钥的内容、粘贴进脚本的外部文本,以及检出拉取请求的 pull-request-target。只保留数量:绝不保留值、名称或行。',
        'As mesmas regras e os mesmos três níveis do monitor local de Actions: informação, aviso e erro. Ações não fixadas a um commit, workflows sem bloco de permissões, o que parece um segredo escrito no ficheiro, texto de terceiros colado num script e um pull-request-target que obtém o pull request. Guardam-se apenas contagens: nunca um valor, um nome ou uma linha.',
    ),
    'sc_lint_none': (
        'Not verified yet: the figures of the daily count do not carry the lint findings until the next count runs.',
        'Aún no verificado: las cifras del recuento diario no traen los hallazgos del lint hasta que se ejecute el siguiente recuento.',
        'Noch nicht geprüft: Die Zahlen der täglichen Zählung enthalten die Lint-Funde erst nach dem nächsten Lauf.',
        'Pas encore vérifié : les chiffres du comptage quotidien ne contiennent pas les constats du lint avant le prochain comptage.',
        'Non ancora verificato: i numeri del conteggio giornaliero non contengono i rilievi del lint finché non viene eseguito il prossimo conteggio.',
        '未確認:次回の集計が実行されるまで、日次集計の数値には lint の結果が含まれません。',
        '尚未验证:在下一次统计运行之前,每日统计数据中不含检查结果。',
        'Ainda não verificado: os números da contagem diária não trazem os resultados do lint até correr a próxima contagem.',
    ),
    'sc_lint_by_rule': ('Findings by rule', 'Hallazgos por regla', 'Funde nach Regel', 'Constats par règle', 'Rilievi per regola', 'ルール別の結果', '按规则统计的结果', 'Resultados por regra'),
    'sc_aria_lint': ('Lint findings by level', 'Hallazgos del lint por nivel', 'Lint-Funde nach Stufe', 'Constats du lint par niveau', 'Rilievi del lint per livello', 'レベル別の lint 結果', '按级别统计的检查结果', 'Resultados do lint por nível'),
    'sc_aria_lintrule': ('Lint findings by rule', 'Hallazgos del lint por regla', 'Lint-Funde nach Regel', 'Constats du lint par règle', 'Rilievi del lint per regola', 'ルール別の lint 結果', '按规则统计的检查结果', 'Resultados do lint por regra'),
    'sc_tip_lint': ('{name}: {n} findings ({pc} %)', '{name}: {n} hallazgos ({pc} %)', '{name}: {n} Funde ({pc} %)', '{name} : {n} constats ({pc} %)', '{name}: {n} rilievi ({pc} %)', '{name}: {n} 件({pc} %)', '{name}:{n} 项({pc} %)', '{name}: {n} resultados ({pc} %)'),
    'sc_lvl_info': ('Information', 'Información', 'Information', 'Information', 'Informazione', '情報', '信息', 'Informação'),
    'sc_lvl_warn': ('Warning', 'Aviso', 'Warnung', 'Avertissement', 'Avviso', '警告', '警告', 'Aviso'),
    'sc_lvl_error': ('Error', 'Error', 'Fehler', 'Erreur', 'Errore', 'エラー', '错误', 'Erro'),
    'sc_rule_unpinned_uses': ('Action not pinned to a commit', 'Acción sin fijar a un commit', 'Action nicht an einen Commit gebunden', 'Action non fixée à un commit', 'Azione non fissata a un commit', 'コミットに固定されていないアクション', '动作未固定到提交', 'Ação não fixada a um commit'),
    'sc_rule_permissions': ('No permissions block', 'Sin bloque de permisos', 'Kein permissions-Block', 'Pas de bloc de permissions', 'Nessun blocco permissions', 'permissions ブロックなし', '没有 permissions 块', 'Sem bloco de permissões'),
    'sc_rule_secrets_in_clear': ('Secret written in the file', 'Secreto escrito en el archivo', 'Geheimnis in der Datei', 'Secret écrit dans le fichier', 'Segreto scritto nel file', 'ファイルに書かれた秘密情報', '文件中的明文密钥', 'Segredo escrito no ficheiro'),
    'sc_rule_injection': ('Outsider text in a script', 'Texto de terceros en un script', 'Fremder Text in einem Skript', 'Texte de tiers dans un script', 'Testo di terzi in uno script', 'スクリプト内の第三者テキスト', '脚本中的外部文本', 'Texto de terceiros num script'),
    'sc_rule_pr_target': ('pull-request-target with the pull request', 'pull-request-target con el pull request', 'pull-request-target mit dem Pull Request', 'pull-request-target avec la pull request', 'pull-request-target con la pull request', 'プルリクエストを使う pull-request-target', '检出拉取请求的 pull-request-target', 'pull-request-target com o pull request'),
    'sc_col_lerr': ('Lint errors', 'Errores de lint', 'Lint-Fehler', 'Erreurs de lint', 'Errori di lint', 'lint エラー', '检查错误', 'Erros de lint'),
    'sc_col_lwarn': ('Lint warnings', 'Avisos de lint', 'Lint-Warnungen', 'Avertissements de lint', 'Avvisi di lint', 'lint 警告', '检查警告', 'Avisos de lint'),
    'sc_k_lint_err': ('Lint errors', 'Errores de lint', 'Lint-Fehler', 'Erreurs de lint', 'Errori di lint', 'lint エラー', '检查错误', 'Erros de lint'),
    'sc_k_lint_warn': ('Lint warnings', 'Avisos de lint', 'Lint-Warnungen', 'Avertissements de lint', 'Avvisi di lint', 'lint 警告', '检查警告', 'Avisos de lint'),
}
