# =============================================================================
# JuanenRac profile - tests/test_dashboard_contrib.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The repositories behind each percentage of the dashboard, and the recent commits read for the repository panel."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_app as app  # noqa: E402
import dashboard_charts as charts  # noqa: E402
import dashboard_contrib as contrib  # noqa: E402
import ecosystem_status as status  # noqa: E402


def node(name, tags=3, files=("tests", "README.md"), readme="", ):
    return {"name": name, "refs": {"totalCount": tags}, "root": {"entries": [{"name": f} for f in files]}, "readme": {"text": readme}}


class SignalTests(unittest.TestCase):
    def test_tests_folder_readmes_and_tags(self):
        files = ["tests", "README.md"] + [f"README_{c}.md" for c in ("spa", "deu", "fra", "ita", "jpn", "zho", "por")]
        facts = contrib.parse_signals([node("A", 5, files)])["A"]
        self.assertEqual(facts, {"releases": 5, "readmes": 8, "tests": True})

    def test_a_tests_badge_in_the_readme_counts_only_when_not_zero(self):
        self.assertTrue(contrib.parse_signals([node("A", files=("src",), readme="![Tests-1,234 passing]")])["A"]["tests"])
        self.assertFalse(contrib.parse_signals([node("A", files=("src",), readme="Tests-0 passing")])["A"]["tests"])
        self.assertFalse(contrib.parse_signals([node("A", files=("src",), readme="")])["A"]["tests"])

    def test_an_unreadable_repository_is_left_out_not_guessed(self):
        found = contrib.parse_signals([{"name": "A", "refs": None, "root": None}, {"name": "B", "refs": {"totalCount": 0}, "root": {}}, node("C")])
        self.assertEqual(list(found), ["C"])

    def test_fetch_needs_a_token_and_survives_failures(self):
        self.assertEqual(contrib.fetch_signals("o", "", {}), {})
        self.assertEqual(contrib.fetch_signals("o", "t", {}, post=lambda body, headers: None), {})
        self.assertEqual(contrib.fetch_signals("o", "t", {}, post=lambda body, headers: {"errors": []}), {})

    def test_fetch_pages_and_adds_the_ci_state_from_the_activity(self):
        pages = [
            {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": True, "endCursor": "c"}, "nodes": [node("A")]}}}},
            {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [node("B")]}}}},
        ]
        calls = []

        def post(body, headers):
            calls.append(json.loads(body)["variables"]["cursor"])
            return pages[len(calls) - 1]
        found = contrib.fetch_signals("o", "t", {"A": charts.Activity(ci="success")}, post=post)
        self.assertEqual(calls, [None, "c"])
        self.assertIs(found["A"]["ci"], True)
        self.assertNotIn("ci", found["B"])


class FlagTests(unittest.TestCase):
    MANIFEST = {"maturity": "established", "evidence": "bench"}
    FACTS = {"releases": 2, "readmes": 8, "tests": True, "ci": True}

    def test_every_area_for_a_complete_repository(self):
        flags = contrib.area_flags(self.MANIFEST, self.FACTS)
        self.assertEqual(list(flags), list(charts.AREAS))
        self.assertTrue(all(flags.values()))

    def test_facts_that_were_not_read_are_none_not_false(self):
        flags = contrib.area_flags(self.MANIFEST, None)
        self.assertEqual([a for a, v in flags.items() if v is None], ["tests", "ci", "releases", "docs"])
        self.assertIsNone(contrib.area_flags(self.MANIFEST, {"releases": 1, "readmes": 8, "tests": True})["ci"])

    def test_hardware_is_left_out_when_the_repository_does_not_depend_on_it(self):
        self.assertNotIn("hardware", contrib.area_flags({**self.MANIFEST, "hardware_bound": False}, self.FACTS))
        self.assertFalse(contrib.area_flags({"maturity": "functional", "evidence": "simulator"}, self.FACTS)["hardware"])

    def test_thresholds_of_each_area(self):
        flags = contrib.area_flags({"maturity": "scaffolding", "evidence": "none"}, {"releases": 0, "readmes": 7, "tests": False, "ci": False})
        self.assertFalse(any(flags.values()))
        flags = contrib.area_flags({"maturity": "functional", "evidence": "simulator"}, self.FACTS)
        self.assertEqual((flags["software"], flags["production"], flags["simulation"], flags["hardware"]), (True, False, True, False))

    def test_counting_the_flags_gives_the_numbers_of_the_readme_table(self):
        """The list behind a percentage and the figure of the README come from the same rules: ecosystem_status.measure."""
        items = [
            ({"maturity": "production", "evidence": "field"}, {"releases": 3, "readmes": 8, "tests": True, "ci": True}),
            ({"maturity": "functional", "evidence": "simulator", "hardware_bound": False}, {"releases": 0, "readmes": 8, "tests": False, "ci": True}),
            ({"maturity": "scaffolding", "evidence": "none"}, {"releases": 1, "readmes": 2, "tests": True, "ci": False}),
            ({"maturity": "established", "evidence": "bench"}, None),
        ]
        measured = status.measure(items)
        flags = [contrib.area_flags(m, s) for m, s in items]
        for area in charts.AREAS:
            if area in ("tests", "ci", "releases", "docs"):
                known = [f[area] for f in flags if f[area] is not None]
            else:
                known = [f[area] for f in flags if area in f]
            self.assertEqual((sum(known), len(known)), measured[area][1:], area)


class BuildTests(unittest.TestCase):
    def test_groups_by_ecosystem_and_area_with_names_and_maturity(self):
        listed = {"B-2": "armor", "A-1": "armor", "U-1": "urtc", "X": "armor"}
        manifests = {"B-2": {"maturity": "functional", "evidence": "none"}, "A-1": {"maturity": "production", "evidence": "field"}, "U-1": {"maturity": "scaffolding"}, "X": None}
        signals = {"A-1": {"releases": 1, "readmes": 8, "tests": True, "ci": True}}
        out = contrib.build(listed, manifests, signals, ["armor", "urtc"], {"armor": {"tests": (1, 1)}})
        self.assertEqual([row[0] for row in out["armor"]["progress"]], ["A-1", "B-2"])      # best first; X has no manifest and is not counted
        tests = out["armor"]["areas"]["tests"]
        self.assertEqual((tests["yes"], tests["unknown"], tests["no"]), ([["A-1", "production"]], [["B-2", "functional"]], []))
        self.assertEqual(tests["readme"], [1, 1])
        self.assertEqual(out["armor"]["progress"][1][3], False)       # B-2 has no delivery facts
        self.assertEqual(out["urtc"]["progress"][0][1], "scaffolding")

    def test_the_whole_structure_is_json(self):
        out = contrib.build({"A": "armor"}, {"A": {"maturity": "x"}}, {}, ["armor"])
        self.assertEqual(json.loads(json.dumps(out)), out)
        self.assertEqual(out["armor"]["progress"][0][1], "x")


class CommitTests(unittest.TestCase):
    def test_recent_commits_are_read_and_redacted(self):
        nodes = [{"name": "R", "defaultBranchRef": {"target": {"committedDate": "2001-01-02T00:00:00Z", "statusCheckRollup": {"state": "SUCCESS"},
                  "history": {"nodes": [{"messageHeadline": "fix SECRET.txt thing", "committedDate": "2001-01-02T00:00:00Z", "url": "https://github.com/JuanenRac/R/commit/1"}, {"messageHeadline": ""}]}}}}]
        act = charts.parse_activity(nodes, redact=lambda text: text.replace("SECRET.txt", "a note"))["R"]
        self.assertEqual([(c.headline, c.date) for c in act.commits], [("fix a note thing", "2001-01-02T00:00:00Z")])

    def test_no_history_means_no_commits_not_an_error(self):
        self.assertEqual(charts.parse_activity([{"name": "R"}])["R"].commits, ())
        self.assertEqual(charts.parse_activity([{"name": "R", "defaultBranchRef": {"target": {"history": None}}}])["R"].commits, ())

    def test_the_query_asks_for_the_history(self):
        self.assertIn("history(first: 5)", charts.ACTIVITY_QUERY)


class PageDataTests(unittest.TestCase):
    def test_json_cannot_close_the_script_element(self):
        html = app.data_script({"x": "</script><!-- &  "})
        self.assertEqual(html.count("</script>"), 1)
        inner = html[html.index(">") + 1:html.rindex("</script>")]
        self.assertNotIn("<", inner)
        self.assertEqual(json.loads(inner), {"x": "</script><!-- &  "})


if __name__ == "__main__":
    unittest.main()
