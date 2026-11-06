# =============================================================================
# JuanenRac profile - tests/test_dashboard_pins.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Pins of the shared contracts: version comparison, the reading of the published files, what is never guessed, and the eight-language texts. No network."""
import base64
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import dashboard_pins as pins  # noqa: E402
import dashboard_pins_texts as texts  # noqa: E402


def contents(doc):
    return "ok", {"content": base64.b64encode(json.dumps(doc).encode()).decode()}


def make_fetch(files):
    def fetch(path):
        for suffix, value in files.items():
            if path.endswith(suffix):
                return value if isinstance(value, tuple) else contents(value)
        return "absent", None
    return fetch


class CompareTest(unittest.TestCase):
    def test_states(self):
        self.assertEqual(pins.compare("0.8.1.1", "0.8.1.1"), "current")
        self.assertEqual(pins.compare("0.8.0.7", "0.8.1.1"), "behind")
        self.assertEqual(pins.compare("0.9.0", "0.8.1.1"), "ahead")
        self.assertEqual(pins.compare("0.8.1", "0.8.1.0"), "current")

    def test_unreadable_is_unknown(self):
        for bad in (None, "", "latest", 3, "1.x"):
            self.assertEqual(pins.compare(bad, "0.8.1.1"), "unknown")
        self.assertEqual(pins.compare("0.8.1.1", None), "unknown")


class ReadTest(unittest.TestCase):
    def test_armor(self):
        fetch = make_fetch({"armor.project.json": {"version": "0.8.1.1"},
                            "contract_pins.json": {"consumers": {"ARMOR-B": "0.8.1.1", "ARMOR-A": "0.8.0.7", "ARMOR-C": "junk"}}})
        out = pins.read_armor(fetch, "o")
        self.assertTrue(out["read"])
        self.assertEqual([(r["repo"], r["state"]) for r in out["rows"]], [("ARMOR-A", "behind"), ("ARMOR-C", "unknown"), ("ARMOR-B", "current")])
        self.assertIsNone(out["rows"][1]["pin"])

    def test_armor_unreadable_is_not_current(self):
        out = pins.read_armor(make_fetch({"armor.project.json": ("error", "HTTP 403")}), "o")
        self.assertFalse(out["read"])
        self.assertEqual(out["rows"], [])

    def test_urtc_skips_repos_without_lock_and_flags_errors(self):
        fetch = make_fetch({"urtc.project.json": {"version": "0.2.3"},
                            "URTC-A/contents/tools/urtc_common.lock.json": {"urtc_common_version": "0.1.9"},
                            "URTC-B/contents/tools/urtc_common.lock.json": ("error", "HTTP 500")})
        out = pins.read_urtc(fetch, "o", ["URTC-A", "URTC-B", "URTC-C", "URTC-COMMON"])
        self.assertEqual([(r["repo"], r["state"]) for r in out["rows"]], [("URTC-A", "behind")])
        self.assertTrue(out["partial"])

    def test_hydra_has_no_source_and_build_filters(self):
        doc = pins.read_all("o", {}, make_fetch({}))
        self.assertEqual(doc["hydra-umc"]["source"], "none")
        built = pins.build({"armor": {"source": "x", "read": True, "current": "1.0", "rows": [{"repo": "a", "state": "weird"}, {"repo": "b", "pin": "1.0", "state": "current"}]}})
        self.assertEqual(len(built["eco"]["armor"]["rows"]), 1)
        self.assertEqual(pins.build(None), {"eco": {}})


class TextsTest(unittest.TestCase):
    def test_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})


if __name__ == "__main__":
    unittest.main()
