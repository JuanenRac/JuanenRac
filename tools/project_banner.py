# =============================================================================
# Electro Hobby 3D - tools/project_banner.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
#
# The banner of one project, in the style of the ecosystem banners of this repository (HYDRA_BANNER.svg, URTC_BANNER.svg,
# ARMOR_BANNER.svg, EH3D_BANNER.svg): the background, the animated emblem and the frame are the ecosystem's own, and the text block is
# made for the project - its name, what it is, its technologies - from the manifest of the repository.
#
#     python tools/project_banner.py ../ARMOR-RADAR              # writes images/<its banner file> in that repository
#     python tools/project_banner.py --check ../ARMOR-RADAR      # exit 1 when the banner is not the one this tool makes
#
# Standard library only.
# =============================================================================
from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FONT = "'Inter', 'Segoe UI', 'Roboto', sans-serif"
BLOCK_START = "<!-- MAIN TYPOGRAPHY / TITLE BLOCK -->"
BLOCK_END = "<!-- Top Right Status / Version Indicator -->"


@dataclass(frozen=True)
class Style:
    template: str            # the ecosystem banner in this repository
    short: str               # how the ecosystem is called in the kicker
    accent: str              # the colour of the kicker and of the frame
    gradient: str | None     # id of the gradient of the accent line (None: flat accent colour)
    glow: str                # id of the glow filter of the accent line
    dots: tuple[str, str, str, str]
    pill_x: int
    pill_w: int


STYLES = {
    "hydra-umc": Style("HYDRA_BANNER.svg", "HYDRA-UMC", "#00E5FF", None, "glowCyan", ("#00E5FF", "#0088FF", "#00FF88", "#FF0055"), 1060, 105),
    "urtc": Style("URTC_BANNER.svg", "URTC", "#00E5FF", "goldGlow", "glowGold", ("#00E5FF", "#FF9900", "#00FF88", "#FF0055"), 1060, 105),
    "armor": Style("ARMOR_BANNER.svg", "A.R.M.O.R.", "#00FF88", "greenGlow", "glowGreen", ("#00FF88", "#FF9900", "#00E5FF", "#FF0055"), 1050, 115),
    "eh3d": Style("EH3D_BANNER.svg", "EH3D", "#00E5FF", "goldGlow", "glowGold", ("#00E5FF", "#FFB300", "#00FF88", "#FF0055"), 1060, 105),
}
MANIFESTS = {"hydra-umc.project.json": "hydra-umc", "urtc.project.json": "urtc", "armor.project.json": "armor", "eh3d.project.json": "eh3d"}

ROLE_WORDS = (("firmware", "FIRMWARE"), ("node", "FIRMWARE"), ("library", "LIBRARY"), ("server", "SERVICE"), ("service", "SERVICE"), ("backend", "SERVICE"),
              ("api", "SERVICE"), ("studio", "APP"), ("android", "APP"), ("ios", "APP"), ("app", "APP"), ("ui", "APP"), ("gui", "APP"), ("console", "APP"),
              ("desktop", "APP"), ("cli", "TOOL"), ("tool", "TOOL"), ("updater", "TOOL"), ("doc", "DOCS"), ("hardware", "HARDWARE"), ("simulator", "TOOL"))


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def role_label(manifest: dict) -> str:
    """One word for the kind of project; the manifests of A.R.M.O.R. write the role as free text, so it is read by its keywords."""
    role = str(manifest.get("role", "")).lower()
    if role in {"api", "service"}:
        return "SERVICE"
    if role in {"ui"}:
        return "APP"
    if role in {"cli", "tool"}:
        return "TOOL"
    if role in {"firmware", "library"}:
        return role.upper()
    text = f"{role} {manifest.get('name', '')}".lower()
    for word, label in ROLE_WORDS:
        if re.search(rf"\b{re.escape(word)}", text):
            return label
    return "PROJECT"


def fit(text: str, base: int, minimum: int, width: int, spacing: float, ratio: float = 0.64) -> tuple[int, float]:
    """Largest font size (down to `minimum`) at which `text` is estimated to fit in `width` pixels, and the letter spacing for it."""
    n = max(1, len(text))
    size = base
    while size > minimum and n * (ratio * size + spacing) > width:
        size -= 1
    return size, spacing if size >= base * 0.75 else max(1.0, spacing / 2)


def chips(technologies: list[str], dots: tuple[str, ...]) -> str:
    out = []
    x = 0
    seen: set[str] = set()
    for tech in technologies:
        label = tech.upper()
        if label in seen or len(out) == 4:
            continue
        seen.add(label)
        width = int(34 + len(label) * 6.6)
        i = len(out)
        out.append(
            f'      <rect x="{x}" y="0" width="{width}" height="22" rx="11" fill="#161B22" stroke="#30363D" stroke-width="1"/>\n'
            f'      <circle cx="{x + 11}" cy="11" r="4" fill="{dots[i]}">\n        <animate attributeName="opacity" values="0.5;1;0.5" dur="{2 + i * 0.2:.1f}s" repeatCount="indefinite"/>\n      </circle>\n'
            f'      <text x="{x + 22}" y="15" font-family="sans-serif" font-weight="600" font-size="10" fill="#C9D1D9" letter-spacing="0.5">{esc(label)}</text>'
        )
        x += width + 10
    return "\n".join(out)


def text_block(style: Style, manifest: dict) -> str:
    name = str(manifest["name"]).upper()
    kicker = f"{style.short} · {role_label(manifest)}"
    kicker_w = int(24 + len(kicker) * 9.9)
    size, spacing = fit(name, 56, 24, 590, 5.0)
    family = str(manifest.get("family") or manifest.get("stack") or "").upper()
    accent_size, accent_spacing = fit(family, 22, 13, 590, 4.0)
    techs = [str(t) for t in manifest.get("technologies", []) if str(t).strip()]
    line = " · ".join(t.upper() for t in techs)
    if len(line) > 68:
        line = line[:65].rstrip(" ·,") + "..."
    fill = f"url(#{style.gradient})" if style.gradient else style.accent
    return f"""{BLOCK_START}
  <g transform="translate(380, 0)">
    <g transform="translate(0, 82)">
      <rect x="0" y="-18" width="{kicker_w}" height="24" rx="4" fill="{style.accent}" fill-opacity="0.1" stroke="{style.accent}" stroke-opacity="0.4" stroke-width="1">
        <animate attributeName="stroke-opacity" values="0.3;0.8;0.3" dur="4s" repeatCount="indefinite"/>
      </rect>
      <text x="12" y="-2" font-family="{FONT}" font-weight="700" font-size="11" fill="{style.accent}" letter-spacing="2.5">{esc(kicker)}</text>
    </g>

    <text x="0" y="142" font-family="{FONT}" font-weight="900" font-size="{size}" fill="#FFFFFF" letter-spacing="{spacing:g}">{esc(name)}</text>

    <text x="0" y="182" font-family="{FONT}" font-weight="700" font-size="{accent_size}" fill="{fill}" letter-spacing="{accent_spacing:g}" filter="url(#{style.glow})">{esc(family)}</text>

    <text x="0" y="212" font-family="{FONT}" font-weight="500" font-size="12" fill="#8B949E" letter-spacing="1.5">{esc(line)}</text>

    <g transform="translate(0, 232)">
{chips(techs, style.dots)}
    </g>
  </g>

  """


def pill(style: Style, manifest: dict) -> str:
    label = role_label(manifest)
    return f"""{BLOCK_END}
  <g transform="translate({style.pill_x}, 42)">
    <rect x="-10" y="-14" width="{style.pill_w}" height="24" rx="12" fill="#0D1117" stroke="{style.accent}" stroke-opacity="0.3" stroke-width="1"/>
    <circle cx="2" cy="-2" r="4" fill="{style.accent}" filter="url(#{style.glow})">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <text x="14" y="2" font-family="monospace" font-weight="700" font-size="11" fill="{style.accent}" letter-spacing="1">{esc(label)}</text>
  </g>
</svg>
"""


def banner_for(manifest: dict, ecosystem: str, templates_dir: Path = ROOT) -> str:
    style = STYLES[ecosystem]
    base = (templates_dir / style.template).read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    start = base.index(BLOCK_START)
    end = base.index(BLOCK_END)
    return base[:start] + text_block(style, manifest) + pill(style, manifest)


def read_manifest(repo: Path) -> tuple[dict, str]:
    for filename, ecosystem in MANIFESTS.items():
        path = repo / filename
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8")), ecosystem
    raise SystemExit(f"{repo}: no ecosystem manifest found")


def banner_path(repo: Path) -> Path | None:
    found = sorted((repo / "images").glob("*BANNER*.svg")) if (repo / "images").is_dir() else []
    return found[0] if found else None


def main(argv: list[str]) -> int:
    check = "--check" in argv
    repos = [Path(a) for a in argv if not a.startswith("--")]
    if not repos:
        print(__doc__)
        return 2
    status = 0
    for repo in repos:
        manifest, ecosystem = read_manifest(repo)
        target = banner_path(repo) or repo / "images" / f"{manifest['name'].replace('-', '_')}_BANNER.svg"
        svg = banner_for(manifest, ecosystem)
        current = target.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n") if target.is_file() else ""
        if check:
            if current != svg:
                print(f"{repo.name}: banner differs from the generated one")
                status = 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(svg, encoding="utf-8", newline="\n")
        print(f"{repo.name}: {target.relative_to(repo)} ({len(svg)} bytes)")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
