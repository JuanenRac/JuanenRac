# =============================================================================
# JuanenRac profile - tests/test_dashboard_delivery_signals.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The delivery and supply chain cards of the Sentinel tab: the three delivery signals (a tag newer than the latest release, a release without notes, a CHANGELOG
that does not name the version released), their table by ecosystem for the five groups, the whitelist that keeps only counts and names of known repositories,
and the guarantee that a fact that was not read never raises a signal."""
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_sentinel as sn  # noqa: E402
import dashboard_sentinel_texts as texts  # noqa: E402
import dashboard_sentinel_ui as ui  # noqa: E402

CONFIG = sn.check_config(None)[0]
NAMES = ["ARMOR-A", "URTC-B", "HYDRA-UMC-C", "EH3D-D", "TOOLS-E", "TOOLS-F"]
ECO = {"ARMOR-A": "armor", "URTC-B": "urtc", "HYDRA-UMC-C": "hydra-umc", "EH3D-D": "eh3d", "TOOLS-E": "electro-hobby-3d", "TOOLS-F": "electro-hobby-3d"}


def record(tag="v1.2.0", notes=True, ntag="v1.2.0", clv="1.2.0"):
    return {"state": "ok", "tag": tag, "published": "2001-12-20T10:00:00Z", "entries": 0, "ci": [], "checked": 1, "rs": True, "perm": None, "notes": notes, "ntag": ntag, "clv": clv}


class ChangelogVersionTests(unittest.TestCase):
    def test_the_newest_released_section_is_found_and_unreleased_is_skipped(self):
        text = "# Changelog\n\n## [Unreleased]\n\n- x\n\n## [1.4.2] - 2001-01-01\n\n## [1.4.1]\n"
        self.assertEqual(sn.changelog_version(text), "1.4.2")
        self.assertEqual(sn.changelog_version("## v0.8.0.3\n- x\n"), "0.8.0.3")
        self.assertEqual(sn.changelog_version("## 2.0.1\r\n- x\r\n"), "2.0.1")

    def test_a_date_or_a_word_is_not_a_version(self):
        self.assertIsNone(sn.changelog_version("## 2001-12-21\n- x\n"))
        self.assertIsNone(sn.changelog_version("## [Unreleased]\n- x\n"))
        self.assertIsNone(sn.changelog_version(None))
        self.assertIsNone(sn.changelog_version(42))


class DeliverySignalTests(unittest.TestCase):
    def test_a_consistent_repository_raises_nothing(self):
        self.assertEqual(sn.delivery_signals({"A": record()}), {"tagahead": [], "nonotes": [], "clmis": []})

    def test_a_newer_tag_than_the_release_is_a_tag_without_release(self):
        out = sn.delivery_signals({"A": record(ntag="v1.3.0"), "B": record(ntag="v1.2.0"), "C": record(ntag="v1.1.9")})
        self.assertEqual(out["tagahead"], ["A"])

    def test_an_empty_description_is_a_release_without_notes(self):
        out = sn.delivery_signals({"A": record(notes=False), "B": record(notes=True), "C": record(notes=None)})
        self.assertEqual(out["nonotes"], ["A"])                 # None = not read: never a signal

    def test_a_changelog_that_names_another_version_differs(self):
        out = sn.delivery_signals({"A": record(clv="1.1.0"), "B": record(clv="1.2"), "C": record(clv=None)})
        self.assertEqual(out["clmis"], ["A"])                   # 1.2 equals 1.2.0, a CHANGELOG without a version is not read

    def test_without_a_release_nothing_can_be_compared(self):
        out = sn.delivery_signals({"A": record(tag=None, notes=None, ntag="v9.0.0", clv="9.0.0")})
        self.assertEqual(out, {"tagahead": [], "nonotes": [], "clmis": []})

    def test_the_table_has_a_row_for_each_ecosystem_and_counts_only_read_repositories(self):
        ok = {"ARMOR-A": record(ntag="v2.0.0"), "TOOLS-E": record(notes=False)}
        signals = sn.delivery_signals(ok)
        table = sn.delivery_table(NAMES, ECO, ok, signals)
        self.assertEqual(sorted(table), ["armor", "eh3d", "electro-hobby-3d", "hydra-umc", "urtc"])
        self.assertEqual(table["armor"], {"repos": 1, "read": 1, "tagahead": 1, "nonotes": 0, "clmis": 0})
        self.assertEqual(table["electro-hobby-3d"], {"repos": 2, "read": 1, "tagahead": 0, "nonotes": 1, "clmis": 0})
        self.assertEqual(table["urtc"]["read"], 0)


class AssembleTests(unittest.TestCase):
    def doc(self, repos):
        read = {"asof": "2001-12-21T12:00:00Z", "repos": repos}
        return sn.assemble(read, NAMES, CONFIG, {}, None, [], "2001-12-21", ECO)

    def test_the_document_carries_the_delivery_block_for_the_five_groups(self):
        repos = {n: record() for n in NAMES}
        repos["EH3D-D"] = record(ntag="v1.5.0")
        doc = self.doc(repos)
        self.assertEqual(doc["delivery"]["tagahead"], ["EH3D-D"])
        self.assertEqual(sorted(doc["delivery"]["eco"]), ["armor", "eh3d", "electro-hobby-3d", "hydra-umc", "urtc"])
        self.assertEqual(doc["delivery"]["eco"]["eh3d"]["tagahead"], 1)

    def test_an_unread_repository_is_not_counted_as_fine(self):
        repos = {n: record() for n in NAMES}
        repos["URTC-B"] = {"state": "unread"}
        doc = self.doc(repos)
        self.assertEqual(doc["delivery"]["eco"]["urtc"]["read"], 0)
        self.assertEqual(doc["delivery"]["eco"]["urtc"]["repos"], 1)

    def test_the_whitelist_drops_unknown_names_and_anything_that_is_not_a_count(self):
        raw = {"asof": "2001-12-21T12:00:00Z", "repos": 1, "read": 1,
               "delivery": {"eco": {"armor": {"repos": 1, "read": 1, "tagahead": 1, "nonotes": "x", "clmis": -3, "title": "Bump lodash in /secret"}, "Bad Key!": {"repos": 9}},
                            "tagahead": ["ARMOR-A", "NOT-MINE", "bad name"], "nonotes": "ARMOR-A", "clmis": []}}
        out = sn.clean(raw, NAMES)
        self.assertEqual(out["delivery"]["tagahead"], ["ARMOR-A"])
        self.assertEqual(out["delivery"]["nonotes"], [])
        self.assertEqual(list(out["delivery"]["eco"]), ["armor"])
        self.assertEqual(set(out["delivery"]["eco"]["armor"]), {"repos", "read", "tagahead", "nonotes", "clmis"})
        self.assertNotIn("secret", json.dumps(out))

    def test_an_older_document_without_the_block_stays_without_it(self):
        out = sn.clean({"asof": "2001-12-21T12:00:00Z", "repos": 1, "read": 1}, NAMES)
        self.assertNotIn("delivery", out)


class SectionAndTextTests(unittest.TestCase):
    def test_both_cards_can_be_switched_off_and_are_on_by_default(self):
        self.assertIn("supply", sn.SECTIONS)
        self.assertIn("delivery", sn.SECTIONS)
        self.assertTrue(CONFIG["sections"]["supply"] and CONFIG["sections"]["delivery"])
        config, problems = sn.check_config({"sections": {"supply": False, "delivery": False}})
        self.assertFalse(config["sections"]["supply"] or config["sections"]["delivery"])
        self.assertEqual(problems, [])

    def test_the_texts_exist_in_the_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        for key in ("sn_sup_title", "sn_sup_row", "sn_del_title", "sn_del_row", "sn_del_none", "sn_state_ok", "sn_state_review"):
            for code, values in texts.TEXTS.items():
                self.assertTrue(values.get(key), (key, code))

    def test_the_panel_lists_the_five_groups_and_reads_nothing_from_the_network(self):
        html = ui.panel_html()
        self.assertIn('data-testid="sn-card-sup"', html)
        self.assertIn('data-testid="sn-card-del"', html)
        self.assertIn('const SN_ECO_ORDER = ["hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"];', ui.JS)
        self.assertNotIn("fetch(", ui.JS)


if __name__ == "__main__":
    unittest.main()
