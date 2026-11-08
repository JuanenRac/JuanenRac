#!/usr/bin/env python3
# =============================================================================
# Electro Hobby 3D - scripts/ecosystem_status.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Keeps the "Ecosystem status" table of every ecosystem section, in the eight
# README files, with real data and never by hand: one line per area with a
# light and the count behind it ("12 of 57 repositories ...").
#
# The areas and where each light comes from:
#   Software        the maturity each repository declares in its own manifest (functional or better)
#   Tests           the repository has a tests folder or a test counter in its README
#   CI              the last finished run on the main branch is green
#   Releases        at least one published tag
#   Documentation   the README exists in the eight languages
#   Simulation      the evidence declared is a simulator or better
#   Real hardware   only the repositories that depend on hardware: bench or field evidence.
#                   Never green unless the field evidence is almost everywhere
#   Production      maturity established or production
# A light: green from 90 %, yellow from 60 %, orange from 30 %, red below.
#
# The facts are read like scripts/ecosystem_progress.py does (manifest from the
# local sibling checkout or raw.githubusercontent.com, GitHub API with the token
# of the CI), so the two scripts always speak about the same repositories.
#
# Usage:  python scripts/ecosystem_status.py            # writes every README
#         python scripts/ecosystem_status.py --check    # exit 1 if any is stale
#         python scripts/ecosystem_status.py --show     # print the numbers only
# =============================================================================
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ecosystem_progress as progress  # noqa: E402

ROOT = progress.ROOT
README_FILES = progress.README_FILES
ECOSYSTEMS = progress.ECOSYSTEMS
LIGHTS = ("🟢", "🟡", "🟠", "🔴")
SIMULATED = ("simulator", "bench", "field")
BENCH = ("bench", "field")
AREAS = ("software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production")
LANGS = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")
FILE_LANG = dict(zip(README_FILES, ("en", "es", "fr", "it", "de", "zh", "ja", "pt")))

HEADING = {
    "en": "Ecosystem status", "es": "Estado del ecosistema", "de": "Status des Ökosystems", "fr": "État de l'écosystème",
    "it": "Stato dell'ecosistema", "ja": "エコシステムの状態", "zh": "生态系统状态", "pt": "Estado do ecossistema",
}
COLUMNS = {
    "en": ("Area", "Status", "Progress", "Note"), "es": ("Área", "Estado", "Avance", "Nota"), "de": ("Bereich", "Status", "Fortschritt", "Hinweis"),
    "fr": ("Domaine", "État", "Avancement", "Note"), "it": ("Area", "Stato", "Avanzamento", "Nota"), "ja": ("分野", "状態", "進捗", "備考"),
    "zh": ("领域", "状态", "进度", "说明"), "pt": ("Área", "Estado", "Progresso", "Nota"),
}
MINI_WIDTH = 10
EIGHTHS = progress.EIGHTHS
INTRO = {
    "en": "Calculated for the whole ecosystem from real data, never typed by hand; a light turns green from 90 % of the repositories, yellow from 60 %, orange from 30 %.",
    "es": "Calculado para todo el ecosistema con datos reales, nunca a mano; una bombilla pasa a verde desde el 90 % de los repositorios, a amarillo desde el 60 % y a naranja desde el 30 %.",
    "de": "Für das gesamte Ökosystem aus realen Daten berechnet, nie von Hand; eine Ampel wird ab 90 % der Repositories grün, ab 60 % gelb und ab 30 % orange.",
    "fr": "Calculé pour tout l'écosystème à partir de données réelles, jamais à la main ; un voyant passe au vert dès 90 % des dépôts, au jaune dès 60 % et à l'orange dès 30 %.",
    "it": "Calcolato per l'intero ecosistema da dati reali, mai a mano; una spia diventa verde dal 90 % dei repository, gialla dal 60 % e arancione dal 30 %.",
    "ja": "エコシステム全体について実際のデータから算出しており、手作業では書いていません。リポジトリの 90 % 以上で緑、60 % 以上で黄、30 % 以上でオレンジになります。",
    "zh": "针对整个生态系统，根据真实数据计算，绝不手写；90 % 以上的仓库达标为绿灯，60 % 以上为黄灯，30 % 以上为橙灯。",
    "pt": "Calculado para todo o ecossistema com dados reais, nunca à mão; uma luz passa a verde a partir de 90 % dos repositórios, a amarelo a partir de 60 % e a laranja a partir de 30 %.",
}
LABEL = {
    "software": dict(en="Software", es="Software", de="Software", fr="Logiciel", it="Software", ja="ソフトウェア", zh="软件", pt="Software"),
    "tests": dict(en="Tests", es="Pruebas", de="Tests", fr="Tests", it="Test", ja="テスト", zh="测试", pt="Testes"),
    "ci": dict(en="Continuous integration", es="Integración continua", de="Kontinuierliche Integration", fr="Intégration continue", it="Integrazione continua", ja="継続的インテグレーション", zh="持续集成", pt="Integração contínua"),
    "releases": dict(en="Releases", es="Versiones publicadas", de="Veröffentlichte Versionen", fr="Versions publiées", it="Versioni pubblicate", ja="公開リリース", zh="已发布版本", pt="Versões publicadas"),
    "docs": dict(en="Documentation", es="Documentación", de="Dokumentation", fr="Documentation", it="Documentazione", ja="ドキュメント", zh="文档", pt="Documentação"),
    "simulation": dict(en="Simulation", es="Simulación", de="Simulation", fr="Simulation", it="Simulazione", ja="シミュレーション", zh="仿真", pt="Simulação"),
    "hardware": dict(en="Real hardware", es="Hardware real", de="Echte Hardware", fr="Matériel réel", it="Hardware reale", ja="実機", zh="真实硬件", pt="Hardware real"),
    "production": dict(en="Production", es="Producción", de="Produktion", fr="Production", it="Produzione", ja="本番運用", zh="生产", pt="Produção"),
}
NOTE = {
    "software": dict(
        en="{k} of {n} repositories are at least functional, by the maturity each declares in its own manifest.",
        es="{k} de {n} repositorios son al menos funcionales, según la madurez que cada uno declara en su propio manifiesto.",
        de="{k} von {n} Repositories sind mindestens funktionsfähig, nach der Reife, die jedes in seinem eigenen Manifest angibt.",
        fr="{k} dépôts sur {n} sont au moins fonctionnels, selon la maturité que chacun déclare dans son propre manifeste.",
        it="{k} repository su {n} sono almeno funzionali, secondo la maturità che ciascuno dichiara nel proprio manifesto.",
        ja="{n} 件中 {k} 件のリポジトリが、各自のマニフェストで宣言した成熟度で少なくとも「機能する」段階です。",
        zh="{n} 个仓库中有 {k} 个至少达到可用阶段，依据是各自清单中声明的成熟度。",
        pt="{k} de {n} repositórios são pelo menos funcionais, segundo a maturidade que cada um declara no seu próprio manifesto."),
    "tests": dict(
        en="{k} of {n} repositories have automated tests.",
        es="{k} de {n} repositorios tienen pruebas automáticas.",
        de="{k} von {n} Repositories haben automatische Tests.",
        fr="{k} dépôts sur {n} ont des tests automatiques.",
        it="{k} repository su {n} hanno test automatici.",
        ja="{n} 件中 {k} 件のリポジトリに自動テストがあります。",
        zh="{n} 个仓库中有 {k} 个有自动化测试。",
        pt="{k} de {n} repositórios têm testes automáticos."),
    "ci": dict(
        en="{k} of {n} repositories have the last CI run on the main branch green.",
        es="{k} de {n} repositorios tienen en verde la última ejecución de la CI en la rama principal.",
        de="{k} von {n} Repositories haben den letzten CI-Lauf auf dem Hauptzweig grün.",
        fr="{k} dépôts sur {n} ont la dernière exécution de la CI sur la branche principale au vert.",
        it="{k} repository su {n} hanno l'ultima esecuzione della CI sul ramo principale verde.",
        ja="{n} 件中 {k} 件のリポジトリで、メインブランチの直近の CI 実行が成功しています。",
        zh="{n} 个仓库中有 {k} 个在主分支上最近一次 CI 运行为绿色。",
        pt="{k} de {n} repositórios têm a última execução do CI no ramo principal em verde."),
    "releases": dict(
        en="{k} of {n} repositories have published at least one release.",
        es="{k} de {n} repositorios han publicado al menos una versión.",
        de="{k} von {n} Repositories haben mindestens eine Version veröffentlicht.",
        fr="{k} dépôts sur {n} ont publié au moins une version.",
        it="{k} repository su {n} hanno pubblicato almeno una versione.",
        ja="{n} 件中 {k} 件のリポジトリが、少なくとも 1 つのリリースを公開しています。",
        zh="{n} 个仓库中有 {k} 个至少发布过一个版本。",
        pt="{k} de {n} repositórios publicaram pelo menos uma versão."),
    "docs": dict(
        en="{k} of {n} repositories have the README in the eight languages.",
        es="{k} de {n} repositorios tienen el README en los ocho idiomas.",
        de="{k} von {n} Repositories haben die README in den acht Sprachen.",
        fr="{k} dépôts sur {n} ont le README dans les huit langues.",
        it="{k} repository su {n} hanno il README nelle otto lingue.",
        ja="{n} 件中 {k} 件のリポジトリに、8 言語すべての README があります。",
        zh="{n} 个仓库中有 {k} 个提供八种语言的 README。",
        pt="{k} de {n} repositórios têm o README nas oito línguas."),
    "simulation": dict(
        en="{k} of {n} repositories have been checked at least in a simulator.",
        es="{k} de {n} repositorios se han comprobado al menos en un simulador.",
        de="{k} von {n} Repositories wurden mindestens in einem Simulator geprüft.",
        fr="{k} dépôts sur {n} ont été vérifiés au moins dans un simulateur.",
        it="{k} repository su {n} sono stati verificati almeno in un simulatore.",
        ja="{n} 件中 {k} 件のリポジトリが、少なくともシミュレーターで検証されています。",
        zh="{n} 个仓库中有 {k} 个至少在仿真器中验证过。",
        pt="{k} de {n} repositórios foram verificados pelo menos num simulador."),
    "hardware": dict(
        en="{k} of the {n} repositories that depend on hardware have been checked on a bench or in the field; the rest have never run on the real thing.",
        es="{k} de los {n} repositorios que dependen de hardware se han comprobado en banco o en campo; el resto nunca ha funcionado con el equipo real.",
        de="{k} der {n} Repositories, die von Hardware abhängen, wurden auf dem Prüfstand oder im Feld geprüft; der Rest lief nie mit der echten Ausrüstung.",
        fr="{k} des {n} dépôts qui dépendent du matériel ont été vérifiés au banc ou sur le terrain ; les autres n'ont jamais fonctionné avec l'équipement réel.",
        it="{k} dei {n} repository che dipendono dall'hardware sono stati verificati al banco o sul campo; gli altri non hanno mai funzionato con l'apparecchiatura reale.",
        ja="ハードウェアに依存する {n} 件のうち {k} 件が、ベンチまたは現場で検証されています。残りは実機で動かしたことがありません。",
        zh="依赖硬件的 {n} 个仓库中有 {k} 个在台架或现场验证过；其余从未在真实设备上运行。",
        pt="{k} dos {n} repositórios que dependem de hardware foram verificados em bancada ou no terreno; os restantes nunca funcionaram com o equipamento real."),
    "production": dict(
        en="{k} of {n} repositories are established or in production.",
        es="{k} de {n} repositorios están consolidados o en producción.",
        de="{k} von {n} Repositories sind etabliert oder im Produktivbetrieb.",
        fr="{k} dépôts sur {n} sont établis ou en production.",
        it="{k} repository su {n} sono consolidati o in produzione.",
        ja="{n} 件中 {k} 件のリポジトリが、確立済みまたは本番運用の段階です。",
        zh="{n} 个仓库中有 {k} 个已成熟或已投入生产。",
        pt="{k} de {n} repositórios estão consolidados ou em produção."),
}


def light(share: float) -> str:
    """Green from 90 %, yellow from 60 %, orange from 30 %, red below."""
    if share >= 0.9:
        return LIGHTS[0]
    if share >= 0.6:
        return LIGHTS[1]
    if share >= 0.3:
        return LIGHTS[2]
    return LIGHTS[3]


def mini_bar(percent: int) -> str:
    """Ten cells with the partial block of the eighths, like the bar of the progress of each ecosystem."""
    cells = percent * MINI_WIDTH * 8 / 100
    full, rest = int(cells // 8), int(round(cells % 8))
    if rest == 8:
        full, rest = full + 1, 0
    body = "█" * full + (EIGHTHS[rest] if rest and full < MINI_WIDTH else "")
    return body + "░" * (MINI_WIDTH - len(body))


def percent_of(count: int, total: int) -> int:
    return int(count * 100 / total + 0.5) if total else 0


def measure(items: list[tuple[dict, dict | None]]) -> dict[str, tuple[str, int, int]]:
    """For each area: (light, repositories that meet it, repositories counted) from the manifests and the signals read."""
    result: dict[str, tuple[str, int, int]] = {}
    n = len(items)

    def share(name: str, count: int, total: int, cap: str | None = None) -> None:
        value = light(count / total) if total else LIGHTS[3]
        if cap and LIGHTS.index(value) < LIGHTS.index(cap):
            value = cap
        result[name] = (value, count, total)

    maturity = [str(m.get("maturity", "")).lower() for m, _ in items]
    evidence = [str(m.get("evidence", "")).lower() for m, _ in items]
    share("software", sum(x in ("functional", "established", "production") for x in maturity), n)
    with_signals = [s for _, s in items if s is not None]
    total_signals = len(with_signals)
    share("tests", sum(bool(s.get("tests")) for s in with_signals), total_signals)
    share("ci", sum(bool(s.get("ci")) for s in with_signals), total_signals)
    share("releases", sum(int(s.get("releases", 0)) >= 1 for s in with_signals), total_signals)
    share("docs", sum(int(s.get("readmes", 0)) >= 8 for s in with_signals), total_signals)
    share("simulation", sum(x in SIMULATED for x in evidence), n)
    bound = [(m, e) for (m, _), e in zip(items, evidence) if m.get("hardware_bound") is not False]
    benched = sum(e in BENCH for _, e in bound)
    fielded = sum(e == "field" for _, e in bound)
    total_bound = len(bound)
    if total_bound and fielded / total_bound >= 0.9:
        result["hardware"] = (LIGHTS[0], benched, total_bound)
    else:
        share("hardware", benched, total_bound, cap=LIGHTS[1])
    share("production", sum(x in ("established", "production") for x in maturity), n)
    return result


def table(lang: str, rows: dict[str, tuple[str, int, int]]) -> str:
    head = COLUMNS[lang]
    lines = [f"| {head[0]} | {head[1]} | {head[2]} | {head[3]} |", "| --- | :---: | --- | --- |"]
    for area in AREAS:
        value, count, total = rows[area]
        percent = percent_of(count, total)
        lines.append(f"| {LABEL[area][lang]} | {value} | `{mini_bar(percent)} {percent}%` | {NOTE[area][lang].format(k=count, n=total)} |")
    return "\n".join(lines)


def block(eco: str, lang: str, rows: dict[str, tuple[str, int, int]]) -> str:
    return (f"<!-- status:{eco} -->\n### 🚦 {HEADING[lang]}\n\n{INTRO[lang]}\n\n{table(lang, rows)}\n<!-- /status:{eco} -->")


def update_readme(text: str, file: str, rows_by_eco: dict[str, dict[str, tuple[str, int, int]]]) -> str:
    """Rewrites (or creates, the first time, right after the progress bar) the status table of every ecosystem."""
    lang = FILE_LANG[file]
    for eco in ECOSYSTEMS:
        fresh = block(eco, lang, rows_by_eco[eco])
        pattern = re.compile(rf"<!-- status:{re.escape(eco)} -->.*?<!-- /status:{re.escape(eco)} -->", re.S)
        if pattern.search(text):
            text = pattern.sub(lambda _: fresh, text, count=1)
            continue
        anchor = f"<!-- /progress:{eco} -->"
        position = text.find(anchor)
        if position < 0:
            raise SystemExit(f"{file}: the progress bar of {eco} is missing, run scripts/ecosystem_progress.py first")
        end = position + len(anchor)
        text = text[:end] + "\n\n" + fresh + text[end:]
    return text


def compute(reader: Callable[[str], "dict | None"] = progress.read_manifest,
            signals: Callable[[str], "dict | None"] | None = progress.read_signals) -> dict[str, dict[str, tuple[str, int, int]]]:
    repos = progress.ecosystem_repos((ROOT / "README.md").read_text(encoding="utf-8"))
    cache: dict[str, dict | None] = {}
    if signals is progress.read_signals:
        missing = total = 0
        pushed = progress.pushed_map()
        for names in repos.values():
            for name in names:
                total += 1
                cache[name] = progress.read_signals(name, pushed.get(name))
                missing += cache[name] is None
        if total and missing / total > 1 - progress.ONLINE_MINIMUM:
            raise progress.FactsUnavailable(f"ERROR: the delivery and quality facts could not be read for {missing} of {total} repositories; nothing written", progress.QUOTA["hit"])
    out: dict[str, dict[str, tuple[str, int, int]]] = {}
    for eco in ECOSYSTEMS:
        items = []
        for name in repos.get(eco, []):
            manifest = reader(name)
            if manifest is None:
                continue
            items.append((manifest, cache.get(name) if cache else (signals(name) if signals else None)))
        if not items:
            raise SystemExit(f"ERROR: no manifest could be read for {eco}; nothing written")
        out[eco] = measure(items)
    return out


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        rows_by_eco = compute()
    except progress.FactsUnavailable as exc:
        if not exc.quota:
            raise
        # GitHub refused for the quota: the status rows keep their last values (nothing is written), the build goes on, and the next run reads again.
        print(f"WARNING: {exc} (the quota of the GitHub API is spent; the status rows keep their last values).", file=sys.stderr)
        return 0
    finally:
        progress.gh_http.shared().save()
    if "--show" in argv:
        for eco, rows in rows_by_eco.items():
            print(eco + ": " + ", ".join(f"{area} {rows[area][0]} {rows[area][1]}/{rows[area][2]}" for area in AREAS))
        return 0
    stale = 0
    for file in README_FILES:
        path = ROOT / file
        with open(path, encoding="utf-8", newline="") as handle:
            original = handle.read()
        newline = "\r\n" if "\r\n" in original else "\n"
        fresh = update_readme(original.replace("\r\n", "\n"), file, rows_by_eco).replace("\n", newline)
        if fresh != original:
            stale += 1
            if "--check" not in argv:
                with open(path, "w", encoding="utf-8", newline="") as handle:
                    handle.write(fresh)
    if "--check" in argv:
        print(f"ECOSYSTEM_STATUS={'FAIL' if stale else 'PASS'} {stale} README file(s) out of date")
        return 1 if stale else 0
    print(f"ECOSYSTEM_STATUS=WRITTEN {stale} README file(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
