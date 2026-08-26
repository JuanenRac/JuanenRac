"""Apply the public HYDRA-UMC Manual 1.1 relationship map to README files.

This one-shot maintenance utility keeps the profile catalog and every
repository's canonical related-project block aligned with the registry-driven
dashboard.  It deliberately preserves older historical overview sections.
"""
from __future__ import annotations

from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
PROFILE = WORKSPACE / "JuanenRac"
COMMON = ("HYDRA-UMC-OS", "HYDRA-UMC-SDK")

TITLES = {
    "README.md": "## Related Projects — Manual 1.1",
    "README_spa.md": "## Proyectos relacionados — Manual 1.1",
    "README_fra.md": "## Projets associés — Manuel 1.1",
    "README_ita.md": "## Progetti correlati — Manuale 1.1",
    "README_deu.md": "## Verwandte Projekte — Handbuch 1.1",
    "README_zho.md": "## 关联项目 — 手册 1.1",
    "README_jpn.md": "## 関連プロジェクト — マニュアル 1.1",
}


def direct_projects(name: str) -> list[str]:
    related = [*COMMON, "HYDRA-UMC-SERVER", "URTC"]
    groups = (
        (("VISION", "DETECTION", "SAFETY", "VISUAL-SERVOING"),
         ("HYDRA-UMC-VISION-NODE", "HYDRA-UMC-VISION-STREAMER", "HYDRA-UMC-DETECTION-HEF", "HYDRA-UMC-SAFETY-ZONES")),
        (("COGNITIVE", "VLA", "SEMANTIC", "VOICE", "PATH-PLANNER", "DOCS-QA"),
         ("HYDRA-UMC-COGNITIVE-NODE", "HYDRA-UMC-VLA-ENGINE", "HYDRA-UMC-SEMANTIC-PLANNER", "HYDRA-UMC-PATH-PLANNER-3D")),
        (("TWIN", "PHYSICS", "HIL", "SYNTHETIC", "EDITOR-URDF"),
         ("HYDRA-UMC-TWIN", "HYDRA-UMC-PHYSICS-REPLICA", "HYDRA-UMC-HIL-BRIDGE", "HYDRA-UMC-EDITOR-URDF")),
        (("DATALAKE", "TELEMETRY", "ANOMALY", "PRODUCTION", "DASHBOARD"),
         ("HYDRA-UMC-DATALAKE", "HYDRA-UMC-TELEMETRY-COLLECTOR", "HYDRA-UMC-ANOMALY-DETECTOR", "HYDRA-UMC-PRODUCTION-REPORTS")),
        (("GATEWAY", "OPCUA", "MQTT", "MTCONNECT"),
         ("HYDRA-UMC-GATEWAY-INDUSTRIAL", "HYDRA-UMC-OPCUA-SERVER", "HYDRA-UMC-MQTT-BROKER", "HYDRA-UMC-MTCONNECT-ADAPTER")),
        (("ORCHESTRATOR", "JOB-", "SWARM", "HEALING", "WATCH", "UPDATER"),
         ("HYDRA-UMC-ORCHESTRATOR", "HYDRA-UMC-JOB-DISPATCHER", "HYDRA-UMC-SWARM-SYNC", "HYDRA-UMC-NODE-HEALING", "HYDRA-UMC-UPDATER")),
        (("URTC",), ("URTC", "URTC-FLASHER", "URTC-TESTER", "URTC-WEB-STUDIO", "URTC-SMART-RACK")),
    )
    for tokens, additions in groups:
        if any(token in name for token in tokens):
            related.extend(additions)
    if name == "HYDRA-UMC":
        related.extend(("HYDRA-UMC-DSI", "HYDRA-UMC-STUDIO"))
    elif name in {"HYDRA-UMC-OS", "HYDRA-UMC-SDK"}:
        related.extend(("HYDRA-UMC", "HYDRA-UMC-UPDATER"))
    elif name in {"HYDRA-UMC-STUDIO", "HYDRA-UMC-SUITE", "HYDRA-UMC-DSI", "HYDRA-UMC-ANDROID-CONTROL", "HYDRA-UMC-IOS-CONTROL", "HYDRA-UMC-TOOL-CLI"}:
        related.extend(("HYDRA-UMC-STUDIO", "HYDRA-UMC-SUITE", "HYDRA-UMC-DSI"))
    return list(dict.fromkeys(project for project in related if project != name))


def link(name: str) -> str:
    return f"[{name}](https://github.com/JuanenRac/{name})"


def add_related_blocks() -> int:
    changed = 0
    for project in sorted(WORKSPACE.iterdir()):
        if not project.is_dir() or not project.name.startswith(("HYDRA-UMC", "URTC")):
            continue
        for readme in project.glob("README*.md"):
            text = readme.read_text(encoding="utf-8")
            if "Manual 1.1" in text or "Manuel 1.1" in text or "Manuale 1.1" in text or "Handbuch 1.1" in text or "手册 1.1" in text or "マニュアル 1.1" in text:
                continue
            direct = " · ".join(link(item) for item in direct_projects(project.name))
            block = "\n\n".join((
                TITLES.get(readme.name, TITLES["README.md"]),
                "> Canonical v1.1 relationship map; it supersedes earlier ecosystem overviews.",
                f"**Direct integrations:**\n{direct}",
                f"**Platform and contracts:**\n{link(COMMON[0])} · {link(COMMON[1])}",
                "**Rest of the ecosystem:**\nAll remaining public repositories are grouped by the seven Manual 1.1 layers in the [JuanenRac ecosystem dashboard](https://juanenrac.github.io/JuanenRac/).",
            ))
            readme.write_text(text.rstrip() + "\n\n" + block + "\n", encoding="utf-8", newline="\n")
            changed += 1
    return changed


def reorganize_profile_catalog() -> int:
    headings = {
        "README.md": ("### 🧱 Platform Foundation & Contracts", "### 💠 Core Control & Operator Clients"),
        "README_spa.md": ("### 🧱 Base de plataforma y contratos", "### 💠 Control core e interfaces de operador"),
        "README_fra.md": ("### 🧱 Fondation de plateforme et contrats", "### 💠 Contrôle central et clients opérateur"),
        "README_ita.md": ("### 🧱 Fondazione della piattaforma e contratti", "### 💠 Controllo core e client operatore"),
        "README_deu.md": ("### 🧱 Plattformbasis und Verträge", "### 💠 Kernsteuerung und Bedienclients"),
        "README_zho.md": ("### 🧱 平台基础与契约", "### 💠 核心控制与操作员客户端"),
        "README_jpn.md": ("### 🧱 プラットフォーム基盤と契約", "### 💠 コア制御とオペレータークライアント"),
    }
    changed = 0
    for readme in PROFILE.glob("README*.md"):
        lines = readme.read_text(encoding="utf-8").splitlines()
        os_index = next(i for i, line in enumerate(lines) if "[HYDRA-UMC-OS]" in line)
        end = next(i for i in range(os_index + 1, len(lines)) if lines[i].startswith("### ") and "Core" not in lines[i] and "平台" not in lines[i] and "Plataforma" not in lines[i] and "Plateforme" not in lines[i] and "Piattaforma" not in lines[i] and "Plattform" not in lines[i])
        start = max(i for i in range(os_index) if lines[i].startswith("### "))
        header = next(line for line in lines[start:end] if line.startswith("| ") and "---" not in line)
        alignment = next(line for line in lines[start:end] if line.startswith("| :"))
        rows = [line for line in lines[start:end] if line.startswith("| [")]
        os_row = next(line for line in rows if "[HYDRA-UMC-OS]" in line)
        sdk_row = next(line for line in rows if "[HYDRA-UMC-SDK]" in line)
        core_rows = [line for line in rows if line not in {os_row, sdk_row}]
        platform, core = headings[readme.name]
        replacement = [platform, header, alignment, os_row, sdk_row, "", core, header, alignment, *core_rows, ""]
        readme.write_text("\n".join([*lines[:start], *replacement, *lines[end:]]) + "\n", encoding="utf-8", newline="\n")
        changed += 1
    return changed


if __name__ == "__main__":
    print(f"profile catalogs reorganized: {reorganize_profile_catalog()}")
    print(f"canonical related-project blocks added: {add_related_blocks()}")
