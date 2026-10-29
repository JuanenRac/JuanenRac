#!/usr/bin/env python3
# =============================================================================
# Electro Hobby 3D - scripts/ecosystem_progress.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Calculates the progress bar of every ecosystem from real data instead of a
# number typed by hand, and writes it into the eight README files.
#
# For each ecosystem the repositories are the ones its catalogue lists in
# README.md; each repository's own manifest says how mature it is
# ("maturity") and, when it has been tried, on what ("evidence"). A
# repository counts for the points of its maturity (scaffolding 10,
# functional 45, established 75, production 90), plus 10 when its evidence is
# real hardware; the bar is the mean over the repositories of the ecosystem.
# 100% therefore means every repository is in production and was tried on
# real hardware - the milestone the profile has always named.
#
# The manifest is read from the local sibling checkout when there is one and
# otherwise from raw.githubusercontent.com (the only path in CI), exactly as
# scripts/sync_readme_versions.py does.
#
# Usage:  python scripts/ecosystem_progress.py            # writes every README
#         python scripts/ecosystem_progress.py --check    # exit 1 if any is stale
#         python scripts/ecosystem_progress.py --show     # print the numbers only
# =============================================================================
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
SIBLINGS = ROOT.parent
USER_AGENT = "JuanenRac-ecosystem-progress"
RAW_TIMEOUT_S = 10

README_FILES = [
    "README.md", "README_spa.md", "README_fra.md", "README_ita.md",
    "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md",
]

# The order of the ecosystem sections (one H1 each) after the title of the profile.
ECOSYSTEMS = ("hydra-umc", "urtc", "armor", "eh3d")
MANIFEST_CANDIDATES = (
    "hydra-umc.project.json", "urtc.project.json", "armor.project.json",
    "eh3d.project.json", "electro-hobby-3d.project.json",
)
MATURITY_POINTS = {"scaffolding": 10, "functional": 45, "established": 75, "production": 90}
HARDWARE_BONUS = 10
BAR_WIDTH = 20
EIGHTHS = " ▏▎▍▌▋▊▉"

REPO_LINK = re.compile(r"^\[([A-Za-z0-9.\-]+)\]\(https://github\.com/JuanenRac/([A-Za-z0-9.\-]+)\)")
H1 = re.compile(r"^# ", re.M)
OLD_BAR = re.compile(r"^`\\?\[[█▉▊▋▌▍▎▏░]+\] \d+%`.*$", re.M)

# The sentence after the bar, in the eight languages. {n} is the number of repositories.
TEXT = {
    "README.md": "Calculated from real data: the maturity and the evidence that each of its {n} repositories declares in its own manifest. The 100% milestone is a fully integrated ecosystem operating on real hardware.",
    "README_spa.md": "Calculado con datos reales: la madurez y la evidencia que cada uno de sus {n} repositorios declara en su propio manifiesto. El hito del 100% es un ecosistema totalmente integrado operando sobre hardware real.",
    "README_deu.md": "Aus realen Daten berechnet: die Reife und der Nachweis, die jedes seiner {n} Repositories in seinem eigenen Manifest angibt. Der 100%-Meilenstein ist ein vollständig integriertes Ökosystem auf echter Hardware.",
    "README_fra.md": "Calculé à partir de données réelles : la maturité et la preuve que chacun de ses {n} dépôts déclare dans son propre manifeste. Le jalon de 100 % est un écosystème entièrement intégré fonctionnant sur du matériel réel.",
    "README_ita.md": "Calcolato da dati reali: la maturità e la prova che ciascuno dei suoi {n} repository dichiara nel proprio manifesto. Il traguardo del 100% è un ecosistema completamente integrato che funziona su hardware reale.",
    "README_jpn.md": "実際のデータから算出しています。{n} 件のリポジトリがそれぞれ自分のマニフェストで宣言している成熟度と検証の根拠が元です。100% は、完全に統合され実機で動作するエコシステムを指します。",
    "README_zho.md": "根据真实数据计算：其 {n} 个仓库各自在自己的清单中声明的成熟度和验证依据。100% 的里程碑是一个完全集成并在真实硬件上运行的生态系统。",
    "README_por.md": "Calculado a partir de dados reais: a maturidade e a evidência que cada um dos seus {n} repositórios declara no seu próprio manifesto. O marco de 100% é um ecossistema totalmente integrado a funcionar em hardware real.",
}
# The row of the status table at the top of each README.
STATUS_ROW = {
    "README.md": "| Progress bars | 🟢 | The percentage of every ecosystem is calculated by `scripts/ecosystem_progress.py` from the maturity and the evidence that each repository declares in its own manifest, and refreshed with the dashboard; the 100% milestone is still a fully integrated ecosystem working on real hardware. |",
    "README_spa.md": "| Barras de progreso | 🟢 | El porcentaje de cada ecosistema lo calcula `scripts/ecosystem_progress.py` con la madurez y la evidencia que cada repositorio declara en su propio manifiesto, y se renueva con el panel; el hito del 100% sigue siendo un ecosistema totalmente integrado funcionando en hardware real. |",
    "README_deu.md": "| Fortschrittsbalken | 🟢 | Der Prozentwert jedes Ökosystems wird von `scripts/ecosystem_progress.py` aus der Reife und dem Nachweis berechnet, die jedes Repository in seinem eigenen Manifest angibt, und mit dem Dashboard erneuert; der 100%-Meilenstein bleibt ein vollständig integriertes Ökosystem auf echter Hardware. |",
    "README_fra.md": "| Barres de progression | 🟢 | Le pourcentage de chaque écosystème est calculé par `scripts/ecosystem_progress.py` à partir de la maturité et de la preuve que chaque dépôt déclare dans son propre manifeste, et renouvelé avec le tableau de bord ; le jalon de 100 % reste un écosystème entièrement intégré fonctionnant sur du matériel réel. |",
    "README_ita.md": "| Barre di avanzamento | 🟢 | La percentuale di ogni ecosistema è calcolata da `scripts/ecosystem_progress.py` con la maturità e la prova che ogni repository dichiara nel proprio manifesto, e si rinnova con il dashboard; il traguardo del 100% resta un ecosistema completamente integrato che funziona su hardware reale. |",
    "README_jpn.md": "| 進捗バー | 🟢 | 各エコシステムのパーセンテージは、各リポジトリが自分のマニフェストで宣言している成熟度と検証の根拠から `scripts/ecosystem_progress.py` が算出し、ダッシュボードとともに更新されます。100% の基準は、完全に統合され実機で動作するエコシステムのままです。 |",
    "README_zho.md": "| 进度条 | 🟢 | 每个生态系统的百分比由 `scripts/ecosystem_progress.py` 根据各仓库在自己的清单中声明的成熟度和验证依据计算，并随仪表盘一起刷新；100% 的里程碑仍然是一个完全集成并在真实硬件上运行的生态系统。 |",
    "README_por.md": "| Barras de progresso | 🟢 | A percentagem de cada ecossistema é calculada por `scripts/ecosystem_progress.py` com a maturidade e a evidência que cada repositório declara no seu próprio manifesto, e renovada com o painel; o marco de 100% continua a ser um ecossistema totalmente integrado a funcionar em hardware real. |",
}

ManifestReader = Callable[[str], "dict | None"]


def _fetch_raw(name: str, candidate: str) -> str | None:
    url = f"https://raw.githubusercontent.com/JuanenRac/{name}/main/{candidate}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=RAW_TIMEOUT_S) as response:
            return response.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def read_manifest(name: str) -> dict | None:
    """The manifest of a repository: the local sibling checkout first, GitHub otherwise."""
    for candidate in MANIFEST_CANDIDATES:
        path = SIBLINGS / name / candidate
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
            return data if isinstance(data, dict) else None
    for candidate in MANIFEST_CANDIDATES:
        raw = _fetch_raw(name, candidate)
        if raw is not None:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return None
            return data if isinstance(data, dict) else None
    return None


def ecosystem_repos(readme_text: str) -> dict[str, list[str]]:
    """The repositories that the catalogue of each ecosystem section links, once each, in order."""
    starts = [match.start() for match in H1.finditer(readme_text)]
    sections = [readme_text[a:b] for a, b in zip(starts[1:], starts[2:] + [len(readme_text)])]
    result: dict[str, list[str]] = {}
    for eco, section in zip(ECOSYSTEMS, sections):
        seen: list[str] = []
        for line in section.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            match = REPO_LINK.match(cells[0]) if line.strip().startswith("|") and cells else None
            if match and match.group(2) not in seen:
                seen.append(match.group(2))
        result[eco] = seen
    return result


def project_points(manifest: dict) -> int:
    points = MATURITY_POINTS.get(str(manifest.get("maturity", "")).lower(), 0)
    if str(manifest.get("evidence", "")).lower() == "hardware":
        points += HARDWARE_BONUS
    return min(100, points)


def ecosystem_percent(repos: list[str], reader: ManifestReader) -> tuple[int, int]:
    """(percent, repositories counted): the mean points of the repositories whose manifest could be read."""
    points = [project_points(manifest) for name in repos if (manifest := reader(name)) is not None]
    if not points:
        return 0, 0
    return int(sum(points) / len(points) + 0.5), len(points)


def bar(percent: int) -> str:
    """Twenty cells; the last full one has the partial block of the eighths."""
    cells = percent * BAR_WIDTH * 8 / 100
    full, rest = int(cells // 8), int(round(cells % 8))
    if rest == 8:
        full, rest = full + 1, 0
    body = "█" * full + (EIGHTHS[rest] if rest and full < BAR_WIDTH else "")
    return body + "░" * (BAR_WIDTH - len(body))


def block(eco: str, percent: int, count: int, file: str) -> str:
    opening = "\\[" if file != "README.md" else "["
    return (f"<!-- progress:{eco} -->\n`{opening}{bar(percent)}] {percent}%` — {TEXT[file].format(n=count)}\n<!-- /progress:{eco} -->")


def update_readme(text: str, file: str, numbers: dict[str, tuple[int, int]]) -> str:
    """Rewrites (or creates, the first time) the progress block of every ecosystem section and the status row."""
    for eco in ECOSYSTEMS:
        percent, count = numbers[eco]
        fresh = block(eco, percent, count, file)
        pattern = re.compile(rf"<!-- progress:{re.escape(eco)} -->.*?<!-- /progress:{re.escape(eco)} -->", re.S)
        if pattern.search(text):
            text = pattern.sub(lambda _: fresh, text, count=1)
            continue
        starts = [match.start() for match in H1.finditer(text)]
        index = ECOSYSTEMS.index(eco) + 1
        begin = starts[index]
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        section = text[begin:end]
        old = OLD_BAR.search(section)
        if old:
            section = section[:old.start()] + fresh + section[old.end():]
        else:
            second = section.find("\n## ")
            if second < 0:
                raise SystemExit(f"{file}: no place for the bar of {eco}")
            section = section[:second].rstrip("\n") + f"\n\n{fresh}\n" + section[second:]
        text = text[:begin] + section + text[end:]
    lines = text.split("\n")
    label = "| " + STATUS_ROW[file].split("|")[1].strip() + " |"
    for index, line in enumerate(lines[:60]):
        if line.startswith(label):
            lines[index] = STATUS_ROW[file]
            break
    return "\n".join(lines)


def compute(reader: ManifestReader = read_manifest) -> dict[str, tuple[int, int]]:
    repos = ecosystem_repos((ROOT / "README.md").read_text(encoding="utf-8"))
    return {eco: ecosystem_percent(repos.get(eco, []), reader) for eco in ECOSYSTEMS}


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    numbers = compute()
    if "--show" in argv:
        for eco, (percent, count) in numbers.items():
            print(f"{eco}: {percent}% ({count} repositories) {bar(percent)}")
        return 0
    if any(count == 0 for _, count in numbers.values()):
        print("ERROR: no manifest could be read for an ecosystem; nothing written", file=sys.stderr)
        return 1
    stale = 0
    for file in README_FILES:
        path = ROOT / file
        original = path.read_text(encoding="utf-8", newline="")
        newline = "\r\n" if "\r\n" in original else "\n"
        fresh = update_readme(original.replace("\r\n", "\n"), file, numbers).replace("\n", newline)
        if fresh != original:
            stale += 1
            if "--check" not in argv:
                path.write_text(fresh, encoding="utf-8", newline="")
    if "--check" in argv:
        print(f"ECOSYSTEM_PROGRESS={'FAIL' if stale else 'PASS'} {stale} README file(s) out of date")
        return 1 if stale else 0
    print(f"ECOSYSTEM_PROGRESS=WRITTEN {stale} README file(s) changed; " + ", ".join(f"{eco} {pct}%" for eco, (pct, _) in numbers.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
