# =============================================================================
# JuanenRac profile - tests/test_dashboard_evo.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The evidence checklist, the history of the progress, the share images and the texts of the new views."""
import json
import re
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_evo as evo  # noqa: E402
import dashboard_evo_texts as texts  # noqa: E402
import dashboard_evo_ui as ui  # noqa: E402

ECOS = ("hydra-umc", "urtc", "armor", "eh3d")


def area(percent):
    return SimpleNamespace(percent=percent)


class ChecksTests(unittest.TestCase):
    def test_every_item_is_verified_missing_or_not_verified(self):
        manifests = {"A": {"maturity": "production", "evidence": "field"}, "B": {"maturity": "scaffolding", "evidence": "none"}}
        signals = {"A": {"tests": True, "ci": True, "releases": 3, "readmes": 8}, "B": {"tests": False, "ci": False, "releases": 0, "readmes": 2}}
        out = evo.checks({"A": "urtc", "B": "urtc"}, manifests, signals)
        self.assertEqual(out["A"], [1, 1, 1, None, 1, 1, 1])
        self.assertEqual(out["B"], [0, 0, 0, 0, 0, 0, 0])

    def test_a_signed_release_is_never_claimed(self):
        out = evo.checks({"A": "urtc"}, {"A": {"maturity": "production", "evidence": "field"}}, {"A": {"tests": True, "ci": True, "releases": 9, "readmes": 8}})
        self.assertIsNone(out["A"][evo.ITEMS.index("signed")])

    def test_without_a_manifest_nothing_is_verified(self):
        self.assertEqual(evo.checks({"A": "urtc"}, {"A": None}, {})["A"], [None] * 7)

    def test_without_signals_only_the_manifest_facts_are_known(self):
        out = evo.checks({"A": "urtc"}, {"A": {"maturity": "functional", "evidence": "bench"}}, {})["A"]
        self.assertEqual(out[:5], [None, None, None, None, None])
        self.assertEqual(out[5:], [1, 1])

    def test_hardware_that_does_not_apply_is_marked_so(self):
        out = evo.checks({"A": "urtc"}, {"A": {"maturity": "functional", "evidence": "none", "hardware_bound": False}}, {})["A"]
        self.assertEqual(out[evo.ITEMS.index("hw")], evo.NA)


class SnapshotTests(unittest.TestCase):
    def test_a_snapshot_keeps_only_real_values(self):
        entry = evo.snapshot("2001-01-02", {"urtc": (40, 10), "armor": (None, None)}, {"urtc": {"tests": area(90), "bogus": area(5), "ci": area(None)}}, ECOS)
        self.assertEqual(entry, {"date": "2001-01-02", "progress": {"urtc": 40}, "areas": {"urtc": {"tests": 90}}})

    def test_nothing_real_means_no_snapshot(self):
        self.assertIsNone(evo.snapshot("2001-01-02", {}, {}, ECOS))
        self.assertIsNone(evo.snapshot("2001-01-02", {"urtc": (None, None)}, {}, ECOS))

    def test_one_entry_per_day_the_last_wins(self):
        a = {"date": "2001-01-02", "progress": {"urtc": 1}, "areas": {}}
        b = {"date": "2001-01-02", "progress": {"urtc": 2}, "areas": {}}
        out = evo.add_snapshot([a], b, "2001-01-02")
        self.assertEqual(out, [b])

    def test_the_history_is_cut_to_90_days(self):
        old = [{"date": f"2001-{m:02d}-01", "progress": {}, "areas": {}} for m in (1, 2, 3)]
        out = evo.add_snapshot(old, {"date": "2001-06-01", "progress": {"urtc": 1}, "areas": {}}, "2001-06-01")
        self.assertEqual([e["date"] for e in out], ["2001-06-01"])
        edge = [{"date": "2001-03-04", "progress": {}, "areas": {}}, {"date": "2001-03-03", "progress": {}, "areas": {}}]
        self.assertEqual([e["date"] for e in evo.normalize(edge, "2001-06-01")], ["2001-03-04"])   # 89 days before is the 90th day, 90 before is out

    def test_entries_are_sorted_and_invalid_ones_dropped(self):
        raw = [{"date": "2001-01-03", "progress": {}, "areas": {}}, {"date": "nope", "progress": {}, "areas": {}}, "x", {"date": "2001-01-01", "progress": {}, "areas": {}},
               {"date": "2001-01-02", "progress": []}]
        self.assertEqual([e["date"] for e in evo.normalize(raw, "2001-01-05")], ["2001-01-01", "2001-01-03"])

    def test_future_days_are_dropped(self):
        self.assertEqual(evo.normalize([{"date": "2002-01-01", "progress": {}, "areas": {}}], "2001-01-05"), [])


class FileTests(unittest.TestCase):
    def test_round_trip_and_atomic_write(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data" / "history.json"
            entries = [{"date": "2001-01-02", "progress": {"urtc": 3}, "areas": {"urtc": {"tests": 4}}}]
            self.assertTrue(evo.save_history(path, entries))
            self.assertFalse(evo.save_history(path, entries), "an unchanged history is not rewritten")
            self.assertEqual(sorted(p.name for p in path.parent.iterdir()), ["history.json"], "no temporary file is left behind")
            loaded, problems = evo.load_history(path, "2001-01-02")
            self.assertEqual((loaded, problems), (entries, []))

    def test_missing_file_is_an_empty_history(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(evo.load_history(Path(folder) / "none.json", "2001-01-02"), ([], []))

    def test_a_broken_file_is_reported_not_trusted(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "history.json"
            for text in ("{not json", '{"entries": 5}', "[1, 2"):
                path.write_text(text, encoding="utf-8")
                entries, problems = evo.load_history(path, "2001-01-02")
                self.assertEqual(entries, [])
                self.assertEqual(len(problems), 1, text)

    def test_the_file_is_stable_text(self):
        text = evo.render_history([{"date": "2001-01-02", "progress": {"b": 1, "a": 2}, "areas": {}}])
        self.assertTrue(text.endswith("\n"))
        self.assertEqual(json.loads(text)["schema"], evo.SCHEMA)
        self.assertEqual(text, evo.render_history(json.loads(text)["entries"]))


class ImageTests(unittest.TestCase):
    def decode(self, data):
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        pos, chunks = 8, {}
        while pos < len(data):
            size = struct.unpack(">I", data[pos:pos + 4])[0]
            kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + size]
            self.assertEqual(struct.unpack(">I", data[pos + 8 + size:pos + 12 + size])[0], zlib.crc32(kind + body) & 0xFFFFFFFF)
            chunks[kind] = body
            pos += 12 + size
        return struct.unpack(">II", chunks[b"IHDR"][:8]), zlib.decompress(chunks[b"IDAT"])

    def test_the_card_is_a_valid_png_of_the_right_size(self):
        (width, height), raw = self.decode(evo.og_png({"urtc": (50, 10)}, ECOS))
        self.assertEqual((width, height), (1200, 630))
        self.assertEqual(len(raw), 630 * (1 + 1200 * 3))

    def test_the_bar_is_as_long_as_the_progress(self):
        def filled(percent):
            _, raw = self.decode(evo.og_png({"hydra-umc": (percent, 1)}, ("hydra-umc",)))
            row = raw[(630 // 2) * (1 + 3600) + 1:(630 // 2 + 1) * (1 + 3600)]
            return sum(1 for x in range(1200) if tuple(row[x * 3:x * 3 + 3]) == evo.ECO_RGB["hydra-umc"])
        self.assertEqual(filled(0), 0)
        self.assertEqual(filled(50), 480)
        self.assertEqual(filled(100), 960)

    def test_an_unknown_progress_draws_no_fill(self):
        _, raw = self.decode(evo.og_png({}, ECOS))
        self.assertNotIn(bytes(evo.ECO_RGB["urtc"]), raw)

    def test_the_card_is_deterministic(self):
        self.assertEqual(evo.og_png({"urtc": (50, 1)}, ECOS), evo.og_png({"urtc": (50, 1)}, ECOS))

    def test_the_favicon_is_a_data_uri_without_quotes(self):
        uri = evo.favicon_data_uri()
        self.assertTrue(uri.startswith("data:image/svg+xml,"))
        self.assertNotRegex(uri, r"[\"'<> ]")


class TextTests(unittest.TestCase):
    def test_every_text_exists_in_the_eight_languages_with_the_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})

    def test_portuguese_is_the_one_of_portugal(self):
        pt = texts.TEXTS["pt"]
        self.assertIn("Em falta", pt["ev_st_no"])
        self.assertNotIn("Arquivo", " ".join(pt.values()))
        self.assertNotIn("tela", " ".join(pt.values()))

    def test_no_text_is_a_key_or_empty(self):
        for lang, values in texts.TEXTS.items():
            for key, value in values.items():
                self.assertFalse(re.fullmatch(r"[a-z]+(_[a-z0-9]+)+", value), (lang, key))

    def test_every_key_the_markup_and_the_script_use_exists(self):
        html = ui.evidence_view() + ui.history_card() + ui.visit_card() + ui.mode_buttons() + ui.print_header() + ui.panel_evidence()
        used = set(re.findall(r'data-i18n(?:-title|-aria-label)?="([a-z_0-9]+)"', html)) | set(re.findall(r'dict\.([a-z_0-9]+)', ui.JS))
        used |= {m for m in re.findall(r'dict\["([a-z_]+)"', ui.JS)}
        known = set(texts.TEXTS["en"]) | {"scope_all", "scope_cross", "filter_ecosystem", "not_verified", "area_software", "area_tests", "area_ci", "area_releases", "area_docs",
                                          "area_simulation", "area_hardware", "area_production"}
        missing = {key for key in used if key not in known and not key.endswith("_")}
        self.assertEqual(missing, set())


class MarkupTests(unittest.TestCase):
    def test_the_head_tags_name_an_absolute_image_and_escape_the_text(self):
        tags = ui.head_tags(5, 'a "quoted" <text>', "https://example.test/x/")
        self.assertIn('property="og:image" content="https://example.test/x/og-image.png"', tags)
        self.assertIn('name="twitter:card" content="summary_large_image"', tags)
        self.assertNotIn('"quoted"', tags)
        self.assertNotIn("<text>", tags)

    def test_the_filters_are_buttons_with_aria_pressed(self):
        html = ui.evidence_view()
        self.assertEqual(html.count("aria-pressed"), html.count("<button") - 1)   # every button but the reset one
        for item in evo.ITEMS:
            if item != "signed":
                self.assertIn(f'data-ev-missing="{item}"', html)

    def test_the_chart_has_an_accessible_name_and_a_table(self):
        html = ui.history_card()
        self.assertIn('role="img" aria-label=', html)
        self.assertIn('<div class="sr-only"><table id="evo-table"', html)

    def test_the_motion_is_only_for_those_who_accept_it(self):
        css = ui.CSS
        self.assertIn("@media (prefers-reduced-motion: no-preference)", css)
        inside = css[css.index("@media (prefers-reduced-motion: no-preference)"):]
        self.assertIn("animation: evo-draw", inside)
        self.assertNotIn("animation: evo-draw", css[:css.index("@media (prefers-reduced-motion: no-preference)")])

    def test_the_print_rules_hide_the_controls_and_show_every_report_panel(self):
        css = ui.CSS
        block = css[css.index("@media print"):]
        for hidden in (".sidebar", ".tabs", ".top-actions", "#panel-projects"):
            self.assertIn(hidden, block)
        self.assertIn(".panel[hidden]", block)


if __name__ == "__main__":
    unittest.main()
