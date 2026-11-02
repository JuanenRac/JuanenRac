# =============================================================================
# JuanenRac profile - tests/test_dashboard_insight.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The analysis tab: maturity funnel, areas side by side, weekly activity, dependencies, milestones, comparing dates and technical debt."""
import json
import re
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_evo as evo  # noqa: E402
import dashboard_health as health  # noqa: E402
import dashboard_insight as ins  # noqa: E402
import dashboard_insight_texts as texts  # noqa: E402
import dashboard_insight_ui as ui  # noqa: E402

ECOS = ("hydra-umc", "urtc", "armor", "eh3d")
TODAY = "2001-12-21"


def area(percent):
    return SimpleNamespace(percent=percent)


def repos_of(**levels):
    return {name: {"eco": "urtc", "maturity": level} for name, level in levels.items()}


class DateTests(unittest.TestCase):
    def test_the_weeks_start_on_sunday_and_end_with_the_current_one(self):
        weeks = ins.week_starts("2001-12-21")           # a Friday
        self.assertEqual(len(weeks), ins.WEEKS)
        self.assertEqual(weeks[-1], "2001-12-16")
        self.assertTrue(all(datetime.fromisoformat(w).weekday() == 6 for w in weeks))
        self.assertEqual(ins.week_starts("2001-12-16")[-1], "2001-12-16")   # a Sunday is its own week

    def test_months_between_counts_whole_months(self):
        from datetime import date
        self.assertEqual(ins.months_between(date(2001, 1, 31), date(2001, 2, 28)), 0)
        self.assertEqual(ins.months_between(date(2001, 1, 15), date(2001, 7, 15)), 6)
        self.assertEqual(ins.months_between(date(2001, 1, 16), date(2001, 7, 15)), 5)


class FunnelTests(unittest.TestCase):
    def history(self, days_ago, repos):
        from datetime import date, timedelta
        return {"date": (date(2001, 12, 21) - timedelta(days=days_ago)).isoformat(), "progress": {}, "areas": {}, "repos": repos}

    def test_counts_by_level_and_unknown_maturity(self):
        out = ins.funnel({"A": {"eco": "urtc", "maturity": "scaffolding"}, "B": {"eco": "urtc", "maturity": "production"}, "C": {"eco": "urtc", "maturity": "weird"}},
                         ("urtc",), [], TODAY)
        self.assertEqual(out["eco"]["urtc"]["counts"], [1, 0, 0, 1])
        self.assertEqual(out["eco"]["urtc"]["unknown"], 1)
        self.assertEqual(out["eco"]["urtc"]["total"], 3)

    def test_without_a_snapshot_with_repositories_nothing_is_counted_as_moved(self):
        out = ins.funnel(repos_of(A="functional"), ("urtc",), [{"date": "2001-12-01", "progress": {}, "areas": {}}], TODAY)
        self.assertIsNone(out["since"])
        self.assertIsNone(out["eco"]["urtc"]["up"])
        self.assertIsNone(out["eco"]["urtc"]["down"])

    def test_moves_up_and_down_against_the_snapshot_of_a_month_ago(self):
        hist = [self.history(30, {"A": [0, "1"], "B": [3, "1"], "C": [1, "1"]}), self.history(5, {"A": [1, "1"], "B": [3, "1"], "C": [1, "1"]})]
        out = ins.funnel(repos_of(A="functional", B="established", C="functional", D="functional"), ("urtc",), hist, TODAY)
        self.assertEqual(out["since"], {"date": "2001-11-21", "days": 30})
        row = out["eco"]["urtc"]
        self.assertEqual((row["up"], row["down"], row["compared"]), (1, 1, 3))     # D is new: neither up nor down

    def test_a_short_history_uses_the_oldest_snapshot_and_says_how_old(self):
        out = ins.funnel(repos_of(A="functional"), ("urtc",), [self.history(3, {"A": [0, ""]})], TODAY)
        self.assertEqual(out["since"]["days"], 3)
        self.assertEqual(out["eco"]["urtc"]["up"], 1)

    def test_the_snapshot_of_today_is_never_the_baseline(self):
        self.assertIsNone(ins.baseline([self.history(0, {"A": [0, ""]})], TODAY))

    def test_a_damaged_level_in_a_snapshot_is_ignored(self):
        out = ins.funnel(repos_of(A="functional"), ("urtc",), [self.history(30, {"A": ["x", ""]})], TODAY)
        self.assertEqual(out["eco"]["urtc"]["compared"], 0)


class RadarTests(unittest.TestCase):
    def test_the_eight_areas_and_a_missing_one_is_none(self):
        out = ins.radar({"urtc": {"software": area(90), "tests": area(None), "ci": area(120)}}, ("urtc", "armor"))
        self.assertEqual(list(out["urtc"]), list(ins.AREAS))
        self.assertEqual((out["urtc"]["software"], out["urtc"]["tests"], out["urtc"]["ci"], out["urtc"]["docs"]), (90, None, None, None))
        self.assertTrue(all(v is None for v in out["armor"].values()))


class ActivityTests(unittest.TestCase):
    def test_parse_commit_weeks(self):
        sunday = int(datetime(2001, 12, 16, tzinfo=timezone.utc).timestamp())
        self.assertEqual(ins.parse_commit_weeks([{"week": sunday, "total": 7, "days": [0] * 7}]), {"2001-12-16": 7})
        for bad in (None, {}, [{"week": "x", "total": 1}], [{"week": sunday, "total": -1}]):
            self.assertIsNone(ins.parse_commit_weeks(bad))

    def test_without_a_token_nothing_is_asked_and_nothing_is_invented(self):
        calls = []
        self.assertEqual(ins.fetch_commit_weeks("o", ["A"], "", get=lambda *a: calls.append(a) or (200, [])), {})
        self.assertEqual(calls, [])

    def test_202_is_asked_again_and_a_failure_leaves_the_repository_out(self):
        sunday = int(datetime(2001, 12, 16, tzinfo=timezone.utc).timestamp())
        seen = {"A": 0}

        def get(url, headers):
            name = url.split("/")[-3]
            if name == "A":
                seen["A"] += 1
                return (202, None) if seen["A"] < 3 else (200, [{"week": sunday, "total": 4}])
            if name == "B":
                return 202, None            # never ready
            return 500, None
        out = ins.fetch_commit_weeks("o", ["A", "B", "C"], "tok", get=get, sleep=lambda _s: None, workers=1)
        self.assertEqual(out, {"A": {"2001-12-16": 4}})

    def test_heatmap_sums_only_the_repositories_that_were_read(self):
        eco = {"A": "urtc", "B": "urtc", "C": "armor"}
        weekly = {"A": {"2001-12-16": 3, "2001-12-09": 1}, "B": {"2001-12-16": 2}}
        facts = {"A": {"releases": ["2001-12-17T10:00:00Z", "2001-08-01T10:00:00Z"]}, "B": {"releases": []}, "C": {"releases": None}}
        out = ins.heatmap(eco, ("urtc", "armor"), weekly, facts, TODAY)
        urtc = out["eco"]["urtc"]
        self.assertEqual(urtc["commits"][-1], 5)
        self.assertEqual(urtc["commits"][-2], 1)
        self.assertEqual(urtc["releases"][-1], 1)
        self.assertEqual(sum(urtc["releases"]), 1)             # the release of August is older than the twelve weeks
        self.assertEqual((urtc["commitRepos"], urtc["releaseRepos"], urtc["repos"]), (2, 2, 2))
        armor = out["eco"]["armor"]
        self.assertEqual(armor["commits"], [None] * ins.WEEKS)      # nothing read: not verified, never zero
        self.assertEqual(armor["releases"], [None] * ins.WEEKS)

    def test_parse_and_fetch_facts(self):
        node = {"name": "A", "createdAt": "2001-01-02T00:00:00Z", "releases": {"nodes": [{"publishedAt": "2001-05-05T00:00:00Z"}]},
                "root": {"entries": [{"name": "src"}]}, "tests": {"entries": [{"name": "integration"}]}, "test": None}
        got = ins.parse_facts([node, {"name": "B", "createdAt": "x", "root": None, "releases": None}, "junk"])
        self.assertEqual(got["A"], {"created": "2001-01-02T00:00:00Z", "releases": ["2001-05-05T00:00:00Z"], "files": ["src", "tests/integration"]})
        self.assertIsNone(got["B"]["files"])
        self.assertIsNone(got["B"]["releases"])
        pages = [{"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": True, "endCursor": "c"}, "nodes": [node]}}}},
                 {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [{"name": "Z", "createdAt": "2001-01-01T00:00:00Z", "root": {"entries": []}, "releases": {"nodes": []}}]}}}}]
        self.assertEqual(sorted(ins.fetch_facts("o", "tok", post=lambda body, headers: pages.pop(0))), ["A", "Z"])
        self.assertEqual(ins.fetch_facts("o", "", post=lambda *a: pages), {})
        self.assertEqual(ins.fetch_facts("o", "tok", post=lambda *a: None), {})
        self.assertEqual(ins.fetch_facts("o", "tok", post=lambda *a: {"errors": []}), {})


class DependencyTests(unittest.TestCase):
    ECO = {"A": "urtc", "B": "urtc", "C": "urtc", "D": "urtc", "X": "armor", "Y": "armor"}

    def test_uses_used_by_missing_and_cycles(self):
        manifests = {"A": {"depends_on": ["B", "Ghost"]}, "B": {"depends_on": ["C"]}, "C": {"depends_on": ["B"]}, "D": {"parent": "A"}, "X": {"depends_on": ["A"]}, "Y": None}
        out = ins.dependencies(manifests, self.ECO, ECOS)
        self.assertEqual(out["repos"]["A"]["uses"], ["B"])
        self.assertEqual(out["repos"]["A"]["missing"], ["Ghost"])
        self.assertEqual(out["repos"]["B"]["usedBy"], ["A", "C"])
        self.assertEqual(out["repos"]["A"]["usedBy"], ["X"])
        self.assertEqual(out["repos"]["D"]["parent"], "A")
        self.assertEqual(out["repos"]["A"]["children"], ["D"])
        self.assertEqual(out["cycles"], [["B", "C"]])
        self.assertEqual(out["missing"], [["A", "Ghost"]])
        self.assertEqual((out["edges"], out["declaring"]), (4, 4))
        self.assertNotIn("Y", out["repos"])

    def test_a_repository_that_depends_on_itself_is_a_cycle(self):
        out = ins.dependencies({"A": {"depends_on": ["A"]}}, {"A": "urtc"}, ECOS)
        self.assertEqual(out["cycles"], [["A"]])

    def test_the_diagram_has_the_used_repository_on_the_left_and_cycles_share_a_column(self):
        manifests = {"A": {"depends_on": ["B"]}, "B": {"depends_on": ["C"]}, "C": {}, "D": {"depends_on": ["A", "X"]}}
        eco = {**self.ECO}
        diagram = ins.dependencies(manifests, eco, ECOS)["diagram"]["urtc"]
        layer = {name: lay for name, lay, _row in diagram["nodes"]}
        self.assertEqual((layer["C"], layer["B"], layer["A"], layer["D"]), (0, 1, 2, 3))
        self.assertIn(["D", "A", 0], diagram["edges"])
        self.assertNotIn(["D", "X", 0], diagram["edges"])           # X belongs to another ecosystem: only in the list
        cyc = ins.dependencies({"A": {"depends_on": ["B"]}, "B": {"depends_on": ["A"]}}, {"A": "urtc", "B": "urtc"}, ECOS)["diagram"]["urtc"]
        self.assertEqual({n[1] for n in cyc["nodes"]}, {0})
        self.assertTrue(all(e[2] == 1 for e in cyc["edges"]))

    def test_no_dependencies_at_all(self):
        out = ins.dependencies({"A": {}, "B": {"depends_on": "oops"}}, {"A": "urtc", "B": "urtc"}, ECOS)
        self.assertEqual((out["repos"], out["cycles"], out["missing"], out["edges"], out["declaring"]), ({}, [], [], 0, 0))
        self.assertEqual(out["diagram"]["urtc"], {"nodes": [], "edges": []})

    def test_a_long_chain_does_not_recurse(self):
        names = [f"R{n:04d}" for n in range(3000)]
        manifests = {n: {"depends_on": [names[i + 1]]} for i, n in enumerate(names[:-1])}
        out = ins.dependencies(manifests, {n: "urtc" for n in names}, ECOS)
        self.assertEqual(out["cycles"], [])


class MilestoneTests(unittest.TestCase):
    PLAN = {"urtc": [{"title": "b", "status": "Blocked", "priority": "High"}, {"title": "a", "status": "In progress", "priority": "Low"},
                     {"title": "z", "status": "Done", "priority": "High"}, {"title": "c", "status": "Backlog", "priority": "Critical"},
                     {"title": "d", "status": "Backlog", "priority": "Low"}]}

    def test_open_items_by_status_then_priority_and_done_are_counted(self):
        out = ins.milestones(None, self.PLAN, ECOS)
        self.assertEqual(out["source"], "plans")
        self.assertEqual([i["title"] for i in out["eco"]["urtc"]["open"]], ["a", "c", "d", "b"])
        self.assertEqual((out["eco"]["urtc"]["done"], out["eco"]["urtc"]["total"]), (1, 5))
        self.assertEqual(out["eco"]["armor"], {"open": [], "done": 0, "total": 0})

    def test_the_projects_win_over_the_plans_and_nothing_means_not_verified(self):
        self.assertEqual(ins.milestones({"armor": [{"title": "x", "status": "Ready", "priority": ""}]}, self.PLAN, ECOS)["source"], "projects")
        self.assertEqual(ins.milestones(None, None, ECOS), {"source": "none", "eco": {}})
        self.assertEqual(ins.milestones({}, {}, ECOS)["source"], "none")

    def test_parse_projects_reads_the_board_of_each_ecosystem_and_rejects_errors(self):
        payload = {"data": {"user": {"projectsV2": {"nodes": [
            {"title": "A.R.M.O.R. Roadmap", "items": {"nodes": [{"content": {"title": "One"}, "status": {"name": "Ready"}, "priority": {"name": "High"}}, {"content": {}}, None]}},
            {"title": "Unrelated", "items": {"nodes": [{"content": {"title": "No"}}]}}]}}}}
        got = ins.parse_projects(payload)
        self.assertEqual(list(got), ["armor"])
        self.assertEqual((got["armor"][0]["title"], got["armor"][0]["status"], got["armor"][0]["priority"]), ("One", "Ready", "High"))
        self.assertIsNone(ins.parse_projects({"data": {"user": None}, "errors": [{"type": "FORBIDDEN"}]}))
        self.assertIsNone(ins.parse_projects(None))
        self.assertIsNone(ins.fetch_projects("o", "", post=lambda *a: payload))
        self.assertEqual(list(ins.fetch_projects("o", "tok", post=lambda *a: payload)), ["armor"])

    def test_the_plans_of_this_repository_are_read(self):
        got = ins.planned_items(HERE.parent / "tools")
        self.assertIsNotNone(got)
        self.assertEqual(set(got), {"hydra-umc", "urtc", "armor", "eh3d"})
        self.assertTrue(all(item["title"] for items in got.values() for item in items))


class DebtTests(unittest.TestCase):
    def test_the_three_rules_and_what_cannot_be_judged(self):
        repos = {
            "Old": {"maturity": "scaffolding"}, "Young": {"maturity": "scaffolding"}, "Unknown": {"maturity": "scaffolding"},
            "NoInt": {"maturity": "functional"}, "WithInt": {"maturity": "functional"}, "NoFiles": {"maturity": "functional"},
            "HwNo": {"maturity": "established", "hardware": True}, "HwYes": {"maturity": "established", "hardware": True}, "HwUnk": {"maturity": "established", "hardware": True},
            "NoHw": {"maturity": "established", "hardware": False},
        }
        facts = {"Old": {"created": "2001-01-01T00:00:00Z"}, "Young": {"created": "2001-11-01T00:00:00Z"}, "Unknown": {"created": None},
                 "NoInt": {"files": ["src", "tests"]}, "WithInt": {"files": ["tests/integration"]}, "NoFiles": {"files": None}}
        manifests = {"HwNo": {"evidence": "host-test"}, "HwYes": {"evidence": "bench"}, "HwUnk": None}
        out = ins.debt(repos, manifests, facts, TODAY, 6)
        self.assertEqual(out["scaffolding"], {"items": [["Old", 11]], "unverified": ["Unknown"]})
        self.assertEqual(out["integration"], {"items": ["NoInt"], "unverified": ["NoFiles"]})
        self.assertEqual(out["hardware"], {"items": [["HwNo", "host-test"]], "unverified": ["HwUnk"]})
        self.assertEqual(out["months"], 6)

    def test_with_no_data_read_every_judgment_is_not_verified(self):
        out = ins.debt({"A": {"maturity": "scaffolding"}, "B": {"maturity": "functional"}}, {}, {}, TODAY, 6)
        self.assertEqual((out["scaffolding"]["items"], out["scaffolding"]["unverified"]), ([], ["A"]))
        self.assertEqual((out["integration"]["items"], out["integration"]["unverified"]), ([], ["B"]))

    def test_integration_test_names(self):
        self.assertTrue(ins.has_integration_tests(["tests/test_Integration.py"]))
        self.assertTrue(ins.has_integration_tests(["e2e"]))
        self.assertFalse(ins.has_integration_tests(["tests", "src"]))
        self.assertIsNone(ins.has_integration_tests(None))

    def test_the_limit_comes_from_the_configuration(self):
        config, problems = health.parse_config({"scaffolding_months": 3})
        self.assertEqual((config["scaffolding_months"], problems), (3, []))
        for bad in (0, 121, "3", True, 2.5):
            config, problems = health.parse_config({"scaffolding_months": bad})
            self.assertEqual(config["scaffolding_months"], 6)
            self.assertEqual(len(problems), 1)
        self.assertEqual(health.load_config()[0]["scaffolding_months"], json.loads((HERE.parent / "dashboard-config.json").read_text())["scaffolding_months"])


class BuildTests(unittest.TestCase):
    def test_everything_together_with_nothing_read_is_json_and_honest(self):
        out = ins.build(repos=repos_of(A="functional"), eco_by_name={"A": "urtc"}, manifests={"A": {}}, status={}, history=[], today=TODAY, config={}, ecosystems=ECOS,
                        facts=None, weekly=None, live=None, planned=None)
        json.dumps(out)
        self.assertFalse(out["facts"])
        self.assertEqual(out["miles"]["source"], "none")
        self.assertEqual(out["debt"]["months"], 6)
        self.assertIsNone(out["funnel"]["since"])
        self.assertEqual(out["heat"]["eco"]["urtc"]["commits"], [None] * ins.WEEKS)


class HistoryTests(unittest.TestCase):
    def test_the_snapshot_keeps_the_maturity_and_the_version_of_each_repository(self):
        entries = [SimpleNamespace(name="A", maturity="functional"), SimpleNamespace(name="B", maturity="weird"), SimpleNamespace(name="C", maturity="production")]
        results = {"A": SimpleNamespace(version="1.2.3"), "C": SimpleNamespace(version=None)}
        repos = evo.repo_facts(entries, results)
        self.assertEqual(repos, {"A": [1, "1.2.3"], "C": [3, ""]})
        snap = evo.snapshot("2001-12-21", {"urtc": (50, 3)}, {}, ECOS, repos=repos)
        self.assertEqual(snap["repos"], {"A": [1, "1.2.3"], "C": [3, ""]})
        self.assertNotIn("repos", evo.snapshot("2001-12-21", {"urtc": (50, 3)}, {}, ECOS))
        self.assertEqual(evo.add_snapshot([], snap, "2001-12-21")[0]["repos"], snap["repos"])


class TextsAndMarkupTests(unittest.TestCase):
    def test_every_text_exists_in_the_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        self.assertEqual(len({frozenset(v) for v in texts.TEXTS.values()}), 1)

    def test_portuguese_is_the_one_of_portugal(self):
        pt = " ".join(texts.TEXTS["pt"].values()).lower()
        for brazilian in ("arquivo", "tela ", "celular", "usuário", "atualizar "):
            self.assertNotIn(brazilian, pt)

    def test_every_key_the_markup_and_the_script_use_has_a_text(self):
        markup = ui.panel_html()
        for key in re.findall(r'data-i18n(?:-aria-label)?="([a-z_0-9]+)"', markup):
            self.assertIn(key, texts.TEXTS["en"], key)
        used = set(re.findall(r"dict\.([a-z]{2}_[a-z_0-9]+)", ui.JS))
        used |= {f"{prefix}{name}" for prefix, names in (("mi_st_", ("in_progress", "ready", "backlog", "blocked", "other")), ("mi_pr_", ("critical", "high", "normal", "low")),
                                                         ("he_", ("commits", "releases"))) for name in names}
        known = set(texts.TEXTS["en"]) | {"not_verified", "evo_metric_overall"}
        for key in used:
            self.assertIn(key, known, key)

    def test_every_view_has_a_button_and_a_section(self):
        markup = ui.panel_html()
        for view in ui.VIEWS:
            self.assertIn(f'data-ins-view="{view}"', markup)
            self.assertIn(f'data-ins-section="{view}"', markup)
        self.assertEqual(markup.count("data-ins-view="), len(ui.VIEWS))

    def test_the_script_never_writes_markup_from_data_and_never_asks_the_network(self):
        for forbidden in ("innerHTML", "insertAdjacentHTML", "fetch(", "XMLHttpRequest", "eval("):
            self.assertNotIn(forbidden, ui.JS)

    def test_the_motion_is_switched_off_when_the_visitor_asks_for_it(self):
        css = ui.CSS
        for name in ("ins-grow", "ins-pop", "ins-fade"):
            first = css.index(f"animation: {name}") if f"animation: {name}" in css else css.index(name)
            before = css[:first]
            self.assertGreater(before.rfind("@media (prefers-reduced-motion: no-preference)"), before.rfind("}\n  @media (max-width"), name)


if __name__ == "__main__":
    unittest.main()
