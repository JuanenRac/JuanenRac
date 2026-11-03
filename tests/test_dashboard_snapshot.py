# =============================================================================
# JuanenRac profile - tests/test_dashboard_snapshot.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Regression of the figures: the dashboard generated from the deterministic fixture must keep the same counts.

The fixture (e2e/fixture/build_fixture.py) is made-up data, so every figure below has a known origin. If a change of the generator moves one
of them, this test fails and prints the difference: when the change is intended, review it and regenerate the snapshot with

    UPDATE_SNAPSHOT=1 python -m unittest discover -s tests -p "test_dashboard_snapshot.py"
"""
import json
import os
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SNAPSHOT = HERE / "snapshots" / "dashboard_fixture.json"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "e2e" / "fixture"))
for sibling in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
    candidate = ROOT.parent / sibling / "src"
    if candidate.is_dir():
        sys.path.append(str(candidate))

try:
    import build_fixture as fixture  # noqa: E402
    IMPORT_ERROR = ""
except ImportError as exc:          # the updaters are not installed: the CI installs them before this test
    fixture, IMPORT_ERROR = None, str(exc)

_DATA = re.compile(r'<script type="application/json" id="dashboard-data">(.*?)</script>', re.S)


def tests_figures(data: dict) -> dict:
    """The tests declared per ecosystem, as the tab "Tests" adds them up: tests of the repositories that declare (or have a last known value), checks apart, states."""
    repos, block = data["repos"], data["tests"]["repos"]
    out: dict = {"series_days": len(data["tests"]["series"]), "stale_date": data["tests"]["staleDate"], "read": data["tests"]["read"], "ecosystems": {}}
    for eco in sorted({r["eco"] for r in repos.values()}):
        mine = {name: row for name, row in block.items() if repos[name]["eco"] == eco}
        out["ecosystems"][eco] = {
            "tests": sum(r["n"] for r in mine.values() if r["unit"] == "tests" and r["state"] in ("declared", "lastknown")),
            "checks": sum(r["n"] for r in mine.values() if r["unit"] == "checks" and r["state"] == "declared"),
            "states": dict(sorted(Counter(r["state"] for r in mine.values()).items())),
        }
    return out


def actions_figures(data: dict) -> dict:
    """The builds as the tab "Actions / Builds" adds them up: runs and minutes of the last 24 hours, open issues and the states, per ecosystem."""
    repos, block = data["repos"], data["actions"]
    out: dict = {"read": block["read"], "stale": block["stale"], "asof": block["asof"], "daily_days": len(block["daily"]), "ecosystems": {}}
    for eco in sorted({r["eco"] for r in repos.values()}):
        mine = {name: row for name, row in block["repos"].items() if repos[name]["eco"] == eco}
        ok = [row for row in mine.values() if row["state"] == "ok"]
        out["ecosystems"][eco] = {
            "runs24": sum(sum(row["n"]) for row in ok), "success24": sum(row["n"][0] for row in ok), "failure24": sum(row["n"][1] for row in ok), "minutes24": sum(row["min"] for row in ok),
            "build_failed": sum(row.get("bf", 0) for row in mine.values()), "build_stuck": sum(row.get("bs", 0) for row in mine.values()),
            "states": dict(sorted(Counter(row["state"] for row in mine.values()).items())),
        }
    return out


def page_figures(html: str) -> dict:
    """Every number the page states about the ecosystems, as plain data."""
    data = json.loads(_DATA.search(html).group(1))
    repos = data["repos"]
    ecosystems = sorted({r["eco"] for r in repos.values()})

    def tally(field: str) -> dict:
        return {eco: dict(sorted(Counter(r.get(field) or "unknown" for r in repos.values() if r["eco"] == eco).items())) for eco in ecosystems}

    kpi = lambda testid: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.search(rf'data-testid="{testid}"[^>]*>(.{{0,260}})', html, re.S).group(1))).strip()
    return {
        "repositories": {eco: sum(1 for r in repos.values() if r["eco"] == eco) for eco in ecosystems},
        "total": len(repos),
        "maturity": tally("maturity"),
        "evidence": tally("evidence"),
        "ci": tally("ci"),
        "hardware_bound": {eco: sum(1 for r in repos.values() if r["eco"] == eco and r["hardware"] is True) for eco in ecosystems},
        "with_release": {eco: sum(1 for r in repos.values() if r["eco"] == eco and r["release"]) for eco in ecosystems},
        "version_unresolved": sorted(name for name, r in repos.items() if r["version"] is None),
        "progress": data["snap"]["progress"],
        "areas": data["snap"]["areas"],
        "history_days": len(data["history"]),
        "checks": {name: list(row) for name, row in sorted(data["checks"].items())[:6]},
        "checks_verified": [sum(1 for row in data["checks"].values() if row[i] == 1) for i in range(7)],
        "ci_evidence": dict(sorted(Counter(v["state"] for v in data["ciEvidence"]["repos"].values()).items())),
        "tests": tests_figures(data),
        "actions": actions_figures(data),
        "kpi_total": kpi("kpi-total"),
        "kpi_errors": kpi("kpi-errors")[:40],
        "kpi_registry": kpi("kpi-percent"),
        "integrity_criterion": (lambda m: list(m.groups()) if m else None)(re.search(r'data-listed="(\d+)" data-public="(\d+)"', html)),
        "integrity_counts": re.findall(r'class="integrity-count">(\d+)<', html),
    }


@unittest.skipIf(fixture is None, f"the updaters are not importable: {IMPORT_ERROR}")
class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.figures = {name: page_figures(builder()) for name, builder in (("full", fixture.build_full), ("single", fixture.build_single))}
        cls.partial = page_figures_light(fixture.build_partial())

    def test_the_figures_of_the_fixture_dashboard_do_not_move_by_accident(self):
        current = {"full": self.figures["full"], "single": {"history_days": self.figures["single"]["history_days"], "total": self.figures["single"]["total"]}, "partial": self.partial}
        if os.environ.get("UPDATE_SNAPSHOT") == "1":
            SNAPSHOT.parent.mkdir(exist_ok=True)
            SNAPSHOT.write_text(json.dumps(current, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        expected = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        diffs = differences(expected, current)
        self.assertEqual(diffs, [], "the figures of the dashboard changed:\n  " + "\n  ".join(diffs) + "\nIf this is intended, regenerate the snapshot (see the top of this file).")

    def test_the_fixture_is_what_the_figures_say(self):
        full = self.figures["full"]
        self.assertEqual(full["repositories"], {"armor": 10, "eh3d": 10, "hydra-umc": 10, "urtc": 10})
        self.assertEqual(full["total"], 40)
        self.assertEqual(sum(full["ci_evidence"].values()), 40)

    def test_the_differences_are_reported_readably(self):
        self.assertEqual(differences({"a": {"b": 1}}, {"a": {"b": 2}}), ["a.b: expected 1, got 2"])
        self.assertEqual(differences({"a": 1}, {}), ["a: expected 1, missing now"])
        self.assertEqual(differences({}, {"a": 1}), ["a: new (1)"])
        self.assertEqual(differences({"a": [1, 2]}, {"a": [1, 2]}), [])


def page_figures_light(html: str) -> dict:
    """The page built from poor data: the counts that must stay at zero or unknown."""
    data = json.loads(_DATA.search(html).group(1))
    return {"total": len(data["repos"]), "ci_evidence": dict(sorted(Counter(v["state"] for v in data["ciEvidence"]["repos"].values()).items())),
            "ci_evidence_read": data["ciEvidence"]["read"], "history_days": len(data["history"]),
            "tests_read": data["tests"]["read"], "actions_read": data["actions"]["read"], "actions_states": dict(sorted(Counter(r["state"] for r in data["actions"]["repos"].values()).items())), "tests_states": dict(sorted(Counter(r["state"] for r in data["tests"]["repos"].values()).items()))}


def differences(expected, current, path: str = "") -> list:
    out: list = []
    if isinstance(expected, dict) and isinstance(current, dict):
        for key in sorted(set(expected) | set(current)):
            where = f"{path}.{key}" if path else str(key)
            if key not in current:
                out.append(f"{where}: expected {json.dumps(expected[key], ensure_ascii=False)}, missing now")
            elif key not in expected:
                out.append(f"{where}: new ({json.dumps(current[key], ensure_ascii=False)})")
            else:
                out += differences(expected[key], current[key], where)
    elif expected != current:
        out.append(f"{path}: expected {json.dumps(expected, ensure_ascii=False)}, got {json.dumps(current, ensure_ascii=False)}")
    return out


if __name__ == "__main__":
    unittest.main()
