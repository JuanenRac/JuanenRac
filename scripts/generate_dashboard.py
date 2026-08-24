#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - scripts/generate_dashboard.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Generates docs/index.html - a static status dashboard (audit idea:
# "Implementar un Dashboard centralizado que muestre el estado de build
# de los 44 repositorios en tiempo real" -
# SONNET/AUDITORIA_COMPLETA_44_PROYECTOS.txt) served by GitHub Pages
# from this repo's own main/docs (see .github/workflows/build-
# dashboard.yml, which runs this on a schedule and commits the result).
#
# Deliberately reuses HYDRA-UMC-UPDATER's own registry.py/github_client.py
# (installed as a real pip dependency, not vendored/copied) rather than
# keeping a second list of "45 repos + how to read each one's version" -
# that list already exists as the ecosystem's own single source of
# truth (registry.py's own header comment says so explicitly), and a
# second copy here would be exactly the kind of two-places-that-must-
# stay-in-sync trap this ecosystem is otherwise careful to avoid.
#
# "Tiempo real" per the audit idea means "as fresh as the last scheduled
# run" here, not a live WebSocket feed - a static GitHub Pages site has
# no server process to hold one open. See the workflow's own schedule
# for how often that actually is.
# =============================================================================
from __future__ import annotations

import sys
from pathlib import Path

from hydra_umc_updater.registry import PROJECTS
from hydra_umc_updater.github_client import fetch_all

DEPLOY_LABELS = {
    "cm5": "CM5",
    "user-pc": "User PC",
    "mobile": "Mobile",
    "wearable": "Wearable",
}
DEPLOY_ORDER = ["cm5", "user-pc", "mobile", "wearable"]

OUT_DIR = Path(__file__).resolve().parent.parent / "docs"


def render_html(results: dict) -> str:
    rows = []
    counts = {k: 0 for k in DEPLOY_ORDER}
    ok_count = 0
    for entry in PROJECTS:
        r = results.get(entry.name)
        version = str(r.version) if r and r.version else "—"
        status_class = "ok" if (r and r.version) else "err"
        if r and r.version:
            ok_count += 1
        counts[entry.deploy] = counts.get(entry.deploy, 0) + 1
        rows.append(
            f'<tr class="{status_class}">'
            f'<td class="name"><a href="https://github.com/JuanenRac/{entry.name}">{entry.name}</a></td>'
            f'<td class="stack">{entry.stack}</td>'
            f'<td class="deploy">{DEPLOY_LABELS.get(entry.deploy, entry.deploy)}</td>'
            f'<td class="version">{version}</td>'
            f"</tr>"
        )

    stat_cards = "".join(
        f'<div class="stat"><span class="num">{counts.get(k, 0)}</span><span class="lbl">{DEPLOY_LABELS[k]}</span></div>'
        for k in DEPLOY_ORDER
    )

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HYDRA-UMC / URTC Ecosystem Status</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
  :root {{
    --bg:#f4f6f9; --surface:#fff; --border:#dde3ea; --text:#16202c; --dim:#57667a;
    --accent:#0284c7; --ok:#059669; --err:#e11d48;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#0a0e13; --surface:#10151d; --border:#232c39; --text:#e8eef5; --dim:#93a3b8; --accent:#38bdf8; --ok:#34d399; --err:#fb7185; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--text); font-family:"IBM Plex Sans",system-ui,sans-serif; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:40px 20px 80px; }}
  h1 {{ font-family:"IBM Plex Mono",monospace; font-size:26px; margin:0 0 6px; }}
  p.sub {{ color:var(--dim); margin:0 0 28px; font-size:14px; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:10px; margin-bottom:24px; }}
  .stat {{ background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:12px 14px; display:flex; flex-direction:column; }}
  .stat .num {{ font-family:"IBM Plex Mono",monospace; font-size:22px; font-weight:600; }}
  .stat .lbl {{ font-size:12px; color:var(--dim); }}
  table {{ width:100%; border-collapse:collapse; background:var(--surface); border:1px solid var(--border); border-radius:8px; overflow:hidden; }}
  th {{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--dim); padding:10px 14px; border-bottom:1px solid var(--border); }}
  td {{ padding:9px 14px; border-bottom:1px solid var(--border); font-size:13.5px; }}
  tr:last-child td {{ border-bottom:none; }}
  td.name a {{ color:var(--accent); text-decoration:none; font-weight:600; }}
  td.name a:hover {{ text-decoration:underline; }}
  td.stack, td.deploy {{ color:var(--dim); font-family:"IBM Plex Mono",monospace; font-size:12px; }}
  td.version {{ font-family:"IBM Plex Mono",monospace; }}
  tr.err td.version {{ color:var(--err); }}
  footer {{ margin-top:24px; color:var(--dim); font-size:12px; }}
</style>
</head><body>
<div class="wrap">
  <h1>HYDRA-UMC / URTC Ecosystem Status</h1>
  <p class="sub">{ok_count}/{len(PROJECTS)} repos answered · versions read live from each repo's own default branch on GitHub · regenerated by <a href="https://github.com/JuanenRac/JuanenRac/blob/main/.github/workflows/build-dashboard.yml">a scheduled GitHub Action</a>, not real-time</p>
  <div class="stats">{stat_cards}</div>
  <table>
    <thead><tr><th>Project</th><th>Stack</th><th>Deploy target</th><th>Version</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <footer>Generated by <a href="https://github.com/JuanenRac/JuanenRac/blob/main/scripts/generate_dashboard.py">scripts/generate_dashboard.py</a>, reusing <a href="https://github.com/JuanenRac/HYDRA-UMC-UPDATER">HYDRA-UMC-UPDATER</a>'s own registry - the ecosystem's single source of truth for where each project's version lives.</footer>
</div>
</body></html>
"""


def main() -> int:
    print(f"Fetching latest GitHub version for {len(PROJECTS)} projects...", file=sys.stderr)
    results = fetch_all(PROJECTS)
    ok = sum(1 for r in results.values() if r.version)
    print(f"{ok}/{len(PROJECTS)} resolved.", file=sys.stderr)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(render_html(results), encoding="utf-8")
    (OUT_DIR / ".nojekyll").touch()  # plain static HTML - tells GitHub Pages not to run it through Jekyll
    print(f"Wrote {OUT_DIR / 'index.html'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
