# =============================================================================
# JuanenRac profile - e2e/fixture/build_fixture.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Renders the status dashboard from deterministic fixture data, with no network and no token.

Usage: python build_fixture.py [OUT_DIR]

Writes OUT_DIR/full/index.html (a complete dataset), OUT_DIR/healthy/index.html (a complete dataset with nothing wrong), OUT_DIR/minimal/index.html (one project, no activity),
OUT_DIR/partial/index.html (failed lookups and an unreachable API) and OUT_DIR/empty/index.html (nothing at all).
The data is made up: repository names are fake and live under a fixture owner, never queried.
"""
from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
# In CI the updaters are installed packages; next to this repository they are source checkouts.
for sibling in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
    candidate = ROOT.parent / sibling / "src"
    if candidate.is_dir():
        sys.path.append(str(candidate))

import dashboard_charts as charts  # noqa: E402
import dashboard_health as health  # noqa: E402
import dashboard_integrity as integrity_mod  # noqa: E402
import generate_dashboard as gen  # noqa: E402
from hydra_umc_updater.registry import ProjectEntry  # noqa: E402

os.environ["DASHBOARD_TODAY"] = "2001-12-21"      # the fixture pages always carry the same day

ECOSYSTEMS = ("hydra-umc", "urtc", "armor", "eh3d")
PREFIX = {"hydra-umc": "HYDRA-UMC", "urtc": "URTC", "armor": "ARMOR", "eh3d": "EH3D"}
MATURITY = ("scaffolding", "functional", "established", "production")
EVIDENCE = ("none", "host-test", "simulator", "bench", "field")
ROLES = ("service", "library", "api", "firmware", "app")
STACKS = ("python", "rust", "typescript", "c")
DEPLOYS = ("cm5", "user-pc", "mcu", "mobile")
FAMILIES = ("Core", "Tools", "Network", "Docs")

README = """
<!-- progress:{key} -->
`[██████████▊░░░░░░░░░] {pct}%` - Calculated from real data: the maturity and the evidence that each of its {n} repositories declares.
<!-- /progress:{key} -->
<!-- status:{key} -->
### Ecosystem status

| Area | Status | Progress | Note |
| --- | :---: | --- | --- |
| Software | 🟢 | `█████████▌ 95%` | 9 of 10 repositories are at least functional. |
| Tests | 🟢 | `█████████▊ 98%` | 9 of 10 repositories have automated tests. |
| Continuous integration | 🟡 | `███████░░░ 70%` | 7 of 10 repositories have the last CI run green. |
| Releases | 🟢 | `█████████▊ 97%` | 9 of 10 repositories have published a release. |
| Documentation | 🟢 | `██████████ 100%` | 10 of 10 repositories have the README in the eight languages. |
| Simulation | 🔴 | `██▍░░░░░░░ 24%` | 2 of 10 repositories have been checked in a simulator. |
| Real hardware | 🔴 | `█▏░░░░░░░░ 11%` | 1 of 9 repositories that depend on hardware have been checked. |
| Production | 🔴 | `▊░░░░░░░░░ 8%` | 1 of 10 repositories are established or in production. |
<!-- /status:{key} -->
"""


def _node(name: str, index: int, healthy: bool = False) -> dict:
    """healthy: every CI green and every date within the last days before the fixed clock of the tests (2001-12-21)."""
    ci = "SUCCESS" if healthy else ("SUCCESS", "SUCCESS", "FAILURE", "PENDING")[index % 4]
    month = 12 if healthy else 1 + index % 10
    day = 10 + index % 8 if healthy else (index % 27) + 1
    commit = f"2001-{month:02d}-{day + 1:02d}T09:00:00Z"
    history = [{"messageHeadline": f"Fixture change {n} of {name}", "committedDate": commit, "url": f"https://github.com/JuanenRac/{name}/commit/c{n}"} for n in range(3)]
    if index % 6 == 5:
        history = []        # a repository whose recent commits were not returned
    return {
        "name": name,
        "latestRelease": None if index % 5 == 4 and not healthy else {"tagName": f"v0.{index % 7}.{index % 3}", "publishedAt": f"2001-{month:02d}-{day:02d}T10:00:00Z"},
        "defaultBranchRef": {"target": {"committedDate": commit, "statusCheckRollup": {"state": ci}, "history": {"nodes": history}}},
    }


def dataset(per_ecosystem: int = 10, healthy: bool = False):
    entries, results, eco, raw, nodes = [], {}, {}, {}, []
    index = 0
    for key in ECOSYSTEMS:
        for number in range(per_ecosystem):
            name = f"{PREFIX[key]}-FIXTURE-{number:02d}"
            description = f"Fixture project number {number} of {key} (searchable text zzdesc{index})"
            entry = ProjectEntry(
                name=name, stack=STACKS[index % 4], version_file="VERSION", pattern=r"\d+\.\d+\.\d+",
                note=description, notes=description, deploy=DEPLOYS[index % 4], maturity=MATURITY[index % 4],
                role=ROLES[index % 5], family=FAMILIES[index % 4],
            )
            entries.append(entry)
            ok = index % 9 != 8
            results[name] = SimpleNamespace(version=f"0.{index % 7}.{index % 3}" if ok else None, error=None if ok else "not found", http_status=200 if ok else 404, url="https://example.invalid/" + name)
            eco[name] = key
            raw[name] = integrity_mod.RawManifest(ecosystem=key, data={"evidence": EVIDENCE[index % 5], "maturity": MATURITY[index % 4]})
            nodes.append(_node(name, index, healthy))
            index += 1
    return entries, results, eco, raw, charts.parse_activity(nodes)


def signals_for(entries, activity) -> dict:
    """Delivery and quality facts of every repository but one in six (those stay unverified)."""
    out = {}
    for index, entry in enumerate(entries):
        if index % 6 == 3:
            continue
        out[entry.name] = {"releases": index % 25, "readmes": 8 if index % 7 else 3, "tests": index % 3 != 0, "ci": activity[entry.name].ci == "success"}
    return out


AREAS = ("software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production")


def history_for(days: int = 45) -> list[dict]:
    """One snapshot a day before 2001-12-21, rising a little every day; two days are missing (never filled in) and one area is unknown on one day."""
    today = date(2001, 12, 21)
    out = []
    for back in range(days, 0, -1):
        if back in (20, 21):
            continue
        day = today - timedelta(days=back)
        progress = {eco: max(0, 40 + 7 * i - back // 3) for i, eco in enumerate(ECOSYSTEMS)}
        areas = {eco: {area: max(0, 20 + 9 * j + 3 * i - back // 4) for j, area in enumerate(AREAS)} for i, eco in enumerate(ECOSYSTEMS)}
        if back == 10:
            del areas["urtc"]["ci"]
        out.append({"date": day.isoformat(), "progress": progress, "areas": areas})
    return out


BUILD = health.BuildInfo("https://github.com/JuanenRac/JuanenRac/actions/runs/123456", "2001-12-20T08:30:00Z")


def build_full() -> str:
    entries, results, eco, raw, activity = dataset()
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    meta = {e.name: gen.RepoMeta(commit_subject=f"Fixture commit for {e.name}", commit_url=f"https://github.com/JuanenRac/{e.name}/commit/abc") for e in entries[:20]}
    issues = [
        integrity_mod.Issue("unlisted_manifest", "URTC-FIXTURE-GHOST", "urtc", "the repository has a manifest the dashboard did not list"),
        integrity_mod.Issue("invalid_manifest", "ARMOR-FIXTURE-BAD", "armor", "version file missing"),
    ]
    cover = integrity_mod.Coverage(len(entries), len(entries) + 3, ("JuanenRac", "fixture-plain-a", "fixture-plain-b"))
    return gen.render_html(entries, results, meta, eco, issues, cover, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=history_for())


def build_single() -> str:
    """The full page with no earlier history: only today's snapshot exists, so no line can be drawn."""
    entries, results, eco, raw, activity = dataset()
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    return gen.render_html(entries, results, {}, eco, [], None, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=[])


def build_healthy() -> str:
    """Every CI green, recent activity (with the clock at 2001-12-21), nothing unresolved and nothing unread: the only variant that may say "no alerts"."""
    entries, results, eco, raw, activity = dataset(healthy=True)
    for result in results.values():
        result.version, result.error, result.http_status = "0.1.0", None, 200
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    cover = integrity_mod.Coverage(len(entries), len(entries), ())
    return gen.render_html(entries, results, {}, eco, [], cover, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=history_for(60))


def build_minimal() -> str:
    entries, results, eco, raw, _ = dataset(per_ecosystem=1)
    entries, eco = entries[:1], {entries[0].name: eco[entries[0].name]}
    results = {entries[0].name: results[entries[0].name]}
    results[entries[0].name].version = "0.1.0"
    return gen.render_html(entries, results, {}, eco, [], None, raw_manifests={}, activity={}, readme_text="")


def build_partial() -> str:
    entries, results, eco, raw, _ = dataset(per_ecosystem=4)
    for result in results.values():  # every version lookup failed
        result.version, result.error, result.http_status = None, "HTTP 403 rate limited", 403
    issues = [integrity_mod.Issue("api", "repository listing", "", "the GitHub API did not answer")]
    cover = integrity_mod.Coverage(len(entries), None, ())
    return gen.render_html(entries, results, {}, eco, issues, cover, raw_manifests={}, activity={}, readme_text="")


def build_empty() -> str:
    return gen.render_html([], {}, {}, {}, [], None, raw_manifests={}, activity={}, readme_text="")


BUILDERS = {"full": build_full, "single": build_single, "healthy": build_healthy, "minimal": build_minimal, "partial": build_partial, "empty": build_empty}


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "out"
    for name, builder in BUILDERS.items():
        target = out / name
        target.mkdir(parents=True, exist_ok=True)
        text = builder()
        (target / "index.html").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
        print(f"{name}: {target / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
