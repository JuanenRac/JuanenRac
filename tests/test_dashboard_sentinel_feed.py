# =============================================================================
# JuanenRac profile - tests/test_dashboard_sentinel_feed.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Sentinel": the table by ecosystem, the versions raised without a release and the short feed of changes."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_sentinel as sn  # noqa: E402
import dashboard_sentinel_texts as texts  # noqa: E402

CONFIG = sn.check_config(None)[0]
NAMES = ["ARMOR-A", "ARMOR-B", "URTC-C", "HYDRA-UMC-D", "EH3D-E"]
ECO = {"ARMOR-A": "armor", "ARMOR-B": "armor", "URTC-C": "urtc", "HYDRA-UMC-D": "hydra-umc", "EH3D-E": "eh3d"}
RED = [{"wf": "ci.yml", "streak": 1, "since": "2001-12-21T11:00:00Z"}]


def record(**kw):
    base = {"state": "ok", "tag": None, "published": None, "entries": 0, "ci": [], "checked": 1, "rs": True, "perm": None}
    base.update(kw)
    return base


def reading(at="2001-12-21T12:00:00Z", **records):
    return {"asof": at, "repos": {name: records.get(name.replace("-", "_"), record()) for name in NAMES}}


def doc_of(read, saved=None, versions=None, config=CONFIG):
    return sn.assemble(read, NAMES, config, {}, None, [], "2001-12-21", ecosystem_of=ECO, versions=versions, saved=saved)


class VersionTests(unittest.TestCase):
    def test_keys_compare_as_numbers(self):
        self.assertEqual(sn.version_key("v0.8.0.1"), (0, 8, 0, 1))
        self.assertEqual(sn.version_key("0.10.0"), (0, 10))
        self.assertGreater(sn.version_key("0.10.0"), sn.version_key("0.9.9"))
        self.assertEqual(sn.version_key("1.0"), sn.version_key("1.0.0"))
        self.assertIsNone(sn.version_key("nightly"))
        self.assertIsNone(sn.version_key(None))

    def test_only_a_raised_version_over_a_published_one_is_listed(self):
        rows = sn.unpublished_versions({"A": "0.3.1", "B": "0.3.0", "C": "0.2.0", "D": "1.0.0", "E": "x", "EH3D-F": "9.0.0", "G": None},
                                       {"A": "0.3.0", "B": "v0.3.0", "C": "0.3.0", "E": "0.1.0", "EH3D-F": "0.1.0"}, ("EH3D-",))
        self.assertEqual(rows, [{"repo": "A", "version": "0.3.1", "tag": "0.3.0"}])       # D has no release, C is behind, E is not numeric, F is skipped


class EcosystemTableTests(unittest.TestCase):
    def test_counts_add_up_and_unread_repositories_are_not_counted_as_read(self):
        doc = doc_of(reading(ARMOR_A=record(ci=RED, entries=2), URTC_C={"state": "unread"}))
        table = doc["ecosystems"]
        self.assertEqual(sum(row["repos"] for row in table.values()), 5)
        self.assertEqual(table["armor"], {"repos": 2, "read": 2, "red": 1, "cand": 1, "unpub": 0})
        self.assertEqual(table["urtc"]["read"], 0)

    def test_without_a_map_everything_is_other(self):
        doc = sn.assemble(reading(), NAMES, CONFIG, {}, None, [], "2001-12-21")
        self.assertEqual(list(doc["ecosystems"]), ["other"])

    def test_a_strange_key_cannot_get_through(self):
        out = sn.clean({"ecosystems": {"armor": {"repos": 2}, "Bad Key": {"repos": 1}, "<x>": {"repos": 1}}}, NAMES)
        self.assertEqual(list(out["ecosystems"]), ["armor"])


class UnpublishedTests(unittest.TestCase):
    def test_the_report_names_the_versions_raised_without_a_release(self):
        doc = doc_of(reading(URTC_C=record(tag="0.2.0", published="2001-12-01T00:00:00Z")), versions={"URTC-C": "0.2.1", "ARMOR-A": "0.1.0"})
        self.assertEqual(doc["unpublished"]["rows"], [{"repo": "URTC-C", "version": "0.2.1", "tag": "0.2.0"}])
        self.assertIn("unpub", [line["key"] for line in doc["parte"]])
        self.assertEqual(doc["ecosystems"]["urtc"]["unpub"], 1)

    def test_a_repository_that_could_not_be_read_is_not_judged(self):
        doc = doc_of(reading(URTC_C={"state": "unread"}), versions={"URTC-C": "9.9.9"})
        self.assertEqual(doc["unpublished"]["rows"], [])

    def test_the_section_switch_hides_the_line(self):
        config = sn.check_config({"sections": {"releases": False}})[0]
        doc = doc_of(reading(URTC_C=record(tag="0.2.0")), versions={"URTC-C": "0.2.1"}, config=config)
        self.assertNotIn("unpub", [line["key"] for line in doc["parte"]])


class FeedTests(unittest.TestCase):
    def test_no_previous_reading_means_no_invented_events(self):
        self.assertEqual(doc_of(reading(ARMOR_A=record(ci=RED, tag="0.1.0")))["events"], [])

    def test_a_workflow_that_turns_red_then_green_and_a_new_release(self):
        first = doc_of(reading(ARMOR_A=record(tag="0.1.0")))
        second = doc_of(reading("2001-12-21T13:00:00Z", ARMOR_A=record(ci=RED, tag="0.1.0")), saved=first)
        self.assertEqual(second["events"], [{"at": "2001-12-21T13:00:00Z", "kind": "red_new", "repo": "ARMOR-A", "wf": "ci.yml"}])
        third = doc_of(reading("2001-12-21T14:00:00Z", ARMOR_A=record(tag="0.1.1")), saved=second)
        kinds = [(e["kind"], e["repo"]) for e in third["events"]]
        self.assertEqual(kinds, [("red_ok", "ARMOR-A"), ("released", "ARMOR-A"), ("red_new", "ARMOR-A")])     # the older event stays after the new ones
        self.assertEqual(third["events"][1]["tag"], "0.1.1")

    def test_an_unread_repository_cannot_recover(self):
        first = doc_of(reading(ARMOR_A=record(ci=RED)))
        second = doc_of(reading("2001-12-21T13:00:00Z", ARMOR_A={"state": "unread"}), saved=first)
        self.assertEqual(second["events"], [])

    def test_an_unchanged_situation_adds_nothing_and_keeps_the_file_stable(self):
        first = doc_of(reading(ARMOR_A=record(ci=RED, tag="0.1.0")))
        again = doc_of(reading("2001-12-21T12:30:00Z", ARMOR_A=record(ci=RED, tag="0.1.0")), saved=first)
        self.assertEqual(again["events"], [])
        self.assertEqual(sn.stabilize(again, first), first)

    def test_the_feed_is_cut_to_the_configured_length(self):
        config = sn.check_config({"events_max": 5})[0]
        saved = {"ci": {"red": [], "red_total": 0}, "tags": {}, "events": []}
        names = [f"R{i}" for i in range(9)]
        read = {"asof": "2001-12-21T12:00:00Z", "repos": {n: record(ci=RED) for n in names}}
        doc = sn.assemble(read, names, config, {}, None, [], "2001-12-21", saved=saved)
        self.assertEqual(len(doc["events"]), 5)

    def test_clean_drops_unknown_kinds_repositories_and_free_text(self):
        events = [{"at": "2001-12-21T12:00:00Z", "kind": "red_new", "repo": "ARMOR-A", "wf": "ci.yml", "title": "secret"},
                  {"at": "2001-12-21T12:00:00Z", "kind": "alert", "repo": "ARMOR-A", "wf": "ci.yml"},
                  {"at": "2001-12-21T12:00:00Z", "kind": "red_new", "repo": "UNKNOWN", "wf": "ci.yml"},
                  {"at": "2001-12-21T12:00:00Z", "kind": "released", "repo": "ARMOR-A", "tag": "a b c"},
                  {"at": "yesterday", "kind": "red_new", "repo": "ARMOR-A", "wf": "ci.yml"}]
        out = sn.clean({"events": events}, NAMES)
        self.assertEqual(out["events"], [{"at": "2001-12-21T12:00:00Z", "kind": "red_new", "repo": "ARMOR-A", "wf": "ci.yml"}])


class TextsAndConfigTests(unittest.TestCase):
    def test_the_new_texts_exist_in_the_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        for key in ("sn_eco_title", "sn_unpub_title", "sp_unpub", "sn_ev_title", "sn_ev_red_new", "sn_ev_red_ok", "sn_ev_released"):
            for code in texts.LANGUAGES:
                self.assertTrue(texts.TEXTS[code][key].strip(), (key, code))

    def test_the_events_length_and_the_sections_are_configurable(self):
        config, problems = sn.check_config({"events_max": 12, "sections": {"events": False, "ecosystems": False}})
        self.assertEqual((config["events_max"], problems), (12, []))
        self.assertFalse(config["sections"]["events"])
        self.assertEqual(sn.check_config({"events_max": 0})[1], ["sentinel.events_max: needs an integer from 5 to 200"])


if __name__ == "__main__":
    unittest.main()
