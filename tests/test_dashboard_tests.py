# =============================================================================
# JuanenRac profile - tests/test_dashboard_tests.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tests declared by each repository: how they are read, what the page embeds and what is never invented."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_evo as evo  # noqa: E402
import dashboard_tests as ts  # noqa: E402
import dashboard_tests_texts as texts  # noqa: E402

ECO = {"HYDRA-UMC-A": "hydra-umc", "HYDRA-UMC-B": "hydra-umc", "URTC-A": "urtc", "ARMOR-A": "armor", "ARMOR-B": "armor", "EH3D-A": "eh3d"}
GLANCE = {"repos": {"HYDRA-UMC-A": {"tests": {"count": 162}}, "HYDRA-UMC-B": {"hardware": "not_run"}}}
README = {
    "HYDRA-UMC-B": "| Tests | 20 (`pytest`) |\n",
    "URTC-A": "| Tests | 2,066 |\n",
    "ARMOR-A": "| Tests | 11979 checks in 20 host programs and 7 Python checks (`ctest`) |\n",
    "ARMOR-B": "| Status | none |\n",
}


def fake_fetch(failing=()):
    def run(path):
        if path.endswith("glance.json"):
            return ("ok", json.dumps(GLANCE)) if path.startswith("HYDRA-UMC-DOCS/") else ("absent", None)
        repo = path.split("/")[0]
        if repo in failing:
            return "error", "HTTP 502"
        return ("ok", README[repo]) if repo in README else ("absent", None)
    return run


class ParseTests(unittest.TestCase):
    def test_readme_row(self):
        cases = {
            "| Tests | 134 (`python -m unittest discover -s tests`) |": {"n": 134, "unit": "tests"},
            "| Tests | 110 tests (`npm test`) |": {"n": 110, "unit": "tests"},
            "| Tests | 1,363 (`npm test`) |": {"n": 1363, "unit": "tests"},
            "| Tests | 489145 checks in 21 host programs and 5 Python checks |": {"n": 489145, "unit": "checks"},
            "| Tests | 7 host test programs (173749 checks counted) |": {"n": 173749, "unit": "checks"},
            "| Tests | 11 host test programs |": None,
            "| Tests | unit tests on the JVM |": None,
            "| Tests | 99999999999 |": None,
            "| Other | 5 |": None,
            "": None,
        }
        for text, expected in cases.items():
            self.assertEqual(ts.parse_readme(text), expected, text)

    def test_only_the_first_tests_row_counts_and_it_must_start_the_row(self):
        self.assertEqual(ts.parse_readme("text | Tests | 5 |\n| Tests | 7 |\n"), {"n": 7, "unit": "tests"})

    def test_glance(self):
        got = ts.parse_glance(GLANCE)
        self.assertEqual(got["HYDRA-UMC-A"], {"n": 162, "unit": "tests"})
        self.assertIsNone(got["HYDRA-UMC-B"])
        for bad in (None, [], {"repos": []}, {"repos": {"X": {"tests": {"count": True}}}}, {"repos": {"X": {"tests": {"count": -1}}}}, {"repos": {"X": {"tests": {"count": "9"}}}}):
            self.assertEqual({k: v for k, v in ts.parse_glance(bad).items() if v}, {})

    def test_config(self):
        config, problems = ts.check_config(None)
        self.assertEqual(problems, [])
        self.assertEqual(config["sources"]["hydra-umc"]["glance"], "HYDRA-UMC-DOCS/data/glance.json")
        for raw in ({"sources": {"urtc": {"glance": "../x"}}}, {"sources": {"urtc": {"readme": "yes"}}}, {"sources": {"urtc": {}}}, {"sources": []}, "text"):
            config, problems = ts.check_config(raw)
            self.assertTrue(problems, raw)
            self.assertIn("urtc", config["sources"])
        config, problems = ts.check_config({"sources": {"armor": {"readme": False, "glance": "ARMOR-DOCS/data/glance.json"}}})
        self.assertEqual((problems, config["sources"]["armor"]), ([], {"glance": "ARMOR-DOCS/data/glance.json", "readme": False}))

    def test_the_real_configuration_is_valid_and_names_every_ecosystem(self):
        config, problems = ts.load_config()
        self.assertEqual(problems, [])
        self.assertEqual(set(config["sources"]), {"hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"})
        self.assertEqual(config["sources"]["armor"], {"readme": True})

    def test_a_configuration_file_that_cannot_be_read_gives_the_defaults_and_a_problem(self):
        config, problems = ts.load_config(ROOT / "does-not-exist.json")
        self.assertEqual(problems, [])
        self.assertIn("hydra-umc", config["sources"])


class ReadTests(unittest.TestCase):
    def setUp(self):
        self.config = ts.check_config(None)[0]

    def test_glance_first_then_readme_then_undeclared(self):
        got = ts.read_all(ECO, fake_fetch(), self.config)
        self.assertEqual(got["records"]["HYDRA-UMC-A"], {"n": 162, "unit": "tests", "src": "glance"})
        self.assertEqual(got["records"]["HYDRA-UMC-B"], {"n": 20, "unit": "tests", "src": "readme"})
        self.assertEqual(got["records"]["URTC-A"], {"n": 2066, "unit": "tests", "src": "readme"})
        self.assertEqual(got["records"]["ARMOR-A"], {"n": 11979, "unit": "checks", "src": "readme"})
        self.assertEqual(sorted(got["undeclared"]), ["ARMOR-B", "EH3D-A"])
        self.assertEqual(got["errors"], {})
        self.assertEqual(got["glance"]["hydra-umc"], "ok")

    def test_a_failing_lookup_is_an_error_never_a_zero_and_never_undeclared(self):
        got = ts.read_all(ECO, fake_fetch(failing={"ARMOR-A", "EH3D-A"}), self.config)
        self.assertEqual(got["errors"], {"ARMOR-A": "HTTP 502", "EH3D-A": "HTTP 502"})
        self.assertNotIn("ARMOR-A", got["records"])
        self.assertNotIn("EH3D-A", got["undeclared"])

    def test_a_glance_file_that_fails_falls_back_to_the_readme_and_is_reported(self):
        def fetch(path):
            return ("error", "HTTP 500") if path.endswith("glance.json") else fake_fetch()(path)
        got = ts.read_all(ECO, fetch, self.config)
        self.assertEqual(got["glance"]["hydra-umc"], "HTTP 500")
        self.assertEqual(got["records"]["HYDRA-UMC-B"]["src"], "readme")
        self.assertIn("HYDRA-UMC-A", got["errors"])        # no README row for it and the glance file could not be read: not verified
        self.assertNotIn("HYDRA-UMC-A", got["undeclared"])

    def test_a_repository_missing_from_a_glance_file_that_was_read_is_undeclared_when_its_readme_has_no_count(self):
        eco = {**ECO, "HYDRA-UMC-C": "hydra-umc"}                  # not in the glance file of the fake, no README row either
        got = ts.read_all(eco, fake_fetch(), self.config)
        self.assertIn("HYDRA-UMC-C", got["undeclared"])
        self.assertNotIn("HYDRA-UMC-C", got["errors"])

    def test_a_glance_file_that_is_not_json_is_reported(self):
        def fetch(path):
            return ("ok", "not json") if path.endswith("glance.json") else fake_fetch()(path)
        got = ts.read_all(ECO, fetch, self.config)
        self.assertTrue(got["glance"]["hydra-umc"].startswith("not valid JSON"))

    def test_nothing_readable_means_nothing_declared(self):
        got = ts.read_all(ECO, lambda path: ("error", "offline"), self.config)
        self.assertEqual((got["records"], got["undeclared"]), ({}, []))
        self.assertEqual(set(got["errors"]), set(ECO))

    def test_readme_source_switched_off(self):
        config = ts.check_config({"sources": {"urtc": {"glance": "URTC-DOCS/data/glance.json", "readme": False}}})[0]
        got = ts.read_all(ECO, fake_fetch(), config)
        self.assertNotIn("URTC-A", got["records"])          # URTC-DOCS has no glance file in the fake and the README is not a source
        self.assertIn("URTC-A", got["errors"])

    def test_fresh_counts_are_only_tests_read_now(self):
        got = ts.read_all(ECO, fake_fetch(), self.config)
        self.assertEqual(ts.fresh_counts(got), {"HYDRA-UMC-A": 162, "HYDRA-UMC-B": 20, "URTC-A": 2066})
        self.assertEqual(ts.fresh_counts(None), {})
        self.assertEqual(ts.fresh_counts({"records": {"X": {"n": True, "unit": "tests"}}}), {})


class BuildTests(unittest.TestCase):
    HISTORY = [
        {"date": "2001-12-18", "progress": {}, "areas": {}, "tests": {"HYDRA-UMC-A": 150, "URTC-A": 2000, "ARMOR-B": 9}},
        {"date": "2001-12-19", "progress": {}, "areas": {}, "tests": {"HYDRA-UMC-A": 155, "URTC-A": 2010, "ARMOR-B": 9}},
        {"date": "2001-12-17", "progress": {}, "areas": {}},                                   # a snapshot from before the counts existed
    ]

    def test_states(self):
        got = ts.read_all(ECO, fake_fetch(failing={"ARMOR-B"}), ts.check_config(None)[0])
        data = ts.build(got, ECO, self.HISTORY, "2001-12-21")
        self.assertTrue(data["read"])
        states = {name: row["state"] for name, row in data["repos"].items()}
        self.assertEqual(states, {"HYDRA-UMC-A": "declared", "HYDRA-UMC-B": "declared", "URTC-A": "declared", "ARMOR-A": "declared", "ARMOR-B": "lastknown", "EH3D-A": "undeclared"})
        self.assertEqual(data["repos"]["ARMOR-B"], {"n": 9, "unit": "tests", "state": "lastknown", "src": None, "asof": "2001-12-19"})
        self.assertEqual(data["staleDate"], "2001-12-19")
        self.assertEqual(data["repos"]["EH3D-A"]["n"], None)             # not declared is not zero

    def test_an_unread_repository_without_history_is_not_verified(self):
        data = ts.build({"records": {}, "undeclared": [], "errors": {n: "x" for n in ECO}}, ECO, [], "2001-12-21")
        self.assertFalse(data["read"])
        self.assertEqual({row["state"] for row in data["repos"].values()}, {"unread"})
        self.assertIsNone(data["staleDate"])
        self.assertEqual(data["series"], [])

    def test_no_read_at_all_uses_the_last_known_values(self):
        data = ts.build(None, ECO, self.HISTORY, "2001-12-21")
        self.assertFalse(data["read"])
        self.assertEqual(data["repos"]["HYDRA-UMC-A"]["state"], "lastknown")
        self.assertEqual(data["repos"]["HYDRA-UMC-A"]["n"], 155)           # the newest snapshot wins
        self.assertEqual(data["repos"]["ARMOR-A"]["state"], "unread")      # never declared in the history

    def test_today_never_feeds_its_own_last_known_value(self):
        today = {"date": "2001-12-21", "progress": {}, "areas": {}, "tests": {"URTC-A": 1}}
        data = ts.build(None, ECO, [*self.HISTORY, today], "2001-12-21")
        self.assertEqual(data["repos"]["URTC-A"]["n"], 2010)

    def test_the_series_has_a_point_only_for_days_with_counts(self):
        points = ts.series(self.HISTORY, ECO)
        self.assertEqual([p["date"] for p in points], ["2001-12-18", "2001-12-19"])
        self.assertEqual(points[0]["eco"], {"hydra-umc": {"n": 150, "k": 1}, "urtc": {"n": 2000, "k": 1}, "armor": {"n": 9, "k": 1}})
        self.assertNotIn("eh3d", points[0]["eco"])
        self.assertEqual(ts.series([], ECO), [])
        self.assertEqual(ts.series([{"date": "2001-12-18", "tests": {}}], ECO), [])

    def test_the_last_point_carries_the_last_known_counts_so_it_matches_the_bars(self):
        got = ts.read_all(ECO, fake_fetch(failing={"ARMOR-B"}), ts.check_config(None)[0])
        today = {"date": "2001-12-21", "progress": {}, "areas": {}, "tests": ts.fresh_counts(got)}
        data = ts.build(got, ECO, [*self.HISTORY, today], "2001-12-21")
        self.assertEqual(data["series"][-1]["eco"]["armor"], {"n": 9, "k": 1})
        self.assertEqual(data["series"][-1]["eco"]["hydra-umc"], {"n": 182, "k": 2})
        self.assertEqual(data["series"][0]["eco"]["armor"], {"n": 9, "k": 1})

    def test_checks_are_not_tests(self):
        got = ts.read_all(ECO, fake_fetch(), ts.check_config(None)[0])
        data = ts.build(got, ECO, [], "2001-12-21")
        self.assertEqual(data["repos"]["ARMOR-A"]["unit"], "checks")
        self.assertNotIn("ARMOR-A", ts.fresh_counts(got))

    def test_the_block_is_plain_json(self):
        data = ts.build(None, ECO, self.HISTORY, "2001-12-21")
        self.assertEqual(json.loads(json.dumps(data)), data)


class SnapshotTests(unittest.TestCase):
    def test_the_snapshot_carries_the_counts_and_old_ones_stay_valid(self):
        snap = evo.snapshot("2001-12-21", {"urtc": (50, 10)}, {}, ["urtc"], tests={"B": 2, "A": 1, "C": True, "D": -3})
        self.assertEqual(snap["tests"], {"A": 1, "B": 2})
        self.assertNotIn("tests", evo.snapshot("2001-12-21", {"urtc": (50, 10)}, {}, ["urtc"]))
        self.assertNotIn("tests", evo.snapshot("2001-12-21", {"urtc": (50, 10)}, {}, ["urtc"], tests={}))
        old = {"date": "2001-12-20", "progress": {"urtc": 40}, "areas": {}}
        kept = evo.add_snapshot([old], snap, "2001-12-21")
        self.assertEqual([e["date"] for e in kept], ["2001-12-20", "2001-12-21"])
        self.assertNotIn("tests", kept[0])

    def test_the_history_file_round_trips_the_counts(self):
        snap = evo.snapshot("2001-12-21", {"urtc": (50, 10)}, {}, ["urtc"], tests={"A": 1})
        loaded = json.loads(evo.render_history([snap]))["entries"][0]
        self.assertEqual(loaded["tests"], {"A": 1})


class TextTests(unittest.TestCase):
    def test_eight_languages_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})

    def test_the_portuguese_is_the_one_of_portugal(self):
        pt = texts.TEXTS["pt"]
        self.assertIn("ficheiro", " ".join(pt.values()))
        for word in ("arquivo", "tela", "celular"):
            self.assertNotIn(word, " ".join(pt.values()).lower())

    def test_the_text_says_declared_not_run(self):
        for code, values in texts.TEXTS.items():
            self.assertIn("{sources}", values["ts_help_body"], code)
        self.assertIn("not run", texts.TEXTS["en"]["ts_badge"])
        self.assertIn("dashboard-config.json", texts.TEXTS["en"]["ts_help_body"])

    def test_no_private_or_audit_wording(self):
        blob = " ".join(" ".join(row) for row in texts.TEXTS.values()).lower()
        for word in ("sonnet", "claude", "audit", "auditor"):
            self.assertNotIn(word, blob)


if __name__ == "__main__":
    unittest.main()
