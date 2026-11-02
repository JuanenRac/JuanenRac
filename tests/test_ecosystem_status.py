import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ecosystem_status as status  # noqa: E402


def item(maturity="functional", evidence="simulator", bound=True, **signals):
    manifest = {"maturity": maturity, "evidence": evidence}
    if not bound:
        manifest["hardware_bound"] = False
    base = {"releases": 1, "tests": True, "ci": True, "readmes": 8}
    base.update(signals)
    return manifest, base


class LightTest(unittest.TestCase):
    def test_the_light_follows_the_thresholds(self):
        self.assertEqual(status.light(1.0), "🟢")
        self.assertEqual(status.light(0.9), "🟢")
        self.assertEqual(status.light(0.89), "🟡")
        self.assertEqual(status.light(0.6), "🟡")
        self.assertEqual(status.light(0.59), "🟠")
        self.assertEqual(status.light(0.3), "🟠")
        self.assertEqual(status.light(0.29), "🔴")
        self.assertEqual(status.light(0.0), "🔴")


class MeasureTest(unittest.TestCase):
    def test_every_area_is_counted_from_the_manifests_and_the_signals(self):
        items = [item("production", "field"), item("functional", "simulator"), item("scaffolding", "none", releases=0, tests=False, ci=False, readmes=3)]
        rows = status.measure(items)
        self.assertEqual(set(rows), set(status.AREAS))
        self.assertEqual(rows["software"][1:], (2, 3))
        self.assertEqual(rows["tests"][1:], (2, 3))
        self.assertEqual(rows["ci"][1:], (2, 3))
        self.assertEqual(rows["releases"][1:], (2, 3))
        self.assertEqual(rows["docs"][1:], (2, 3))
        self.assertEqual(rows["simulation"][1:], (2, 3))
        self.assertEqual(rows["production"][1:], (1, 3))

    def test_the_hardware_area_counts_only_what_depends_on_hardware_and_is_never_green_without_field_evidence(self):
        rows = status.measure([item("production", "bench"), item("production", "bench"), item("functional", "simulator", bound=False)])
        self.assertEqual(rows["hardware"][1:], (2, 2))
        self.assertEqual(rows["hardware"][0], "🟡")
        rows = status.measure([item("production", "field"), item("production", "field")])
        self.assertEqual(rows["hardware"][0], "🟢")
        rows = status.measure([item("functional", "simulator"), item("functional", "host-test")])
        self.assertEqual(rows["hardware"], ("🔴", 0, 2))

    def test_a_signal_that_could_not_be_read_does_not_count_for_or_against_the_signal_areas(self):
        rows = status.measure([(item()[0], None), item()])
        self.assertEqual(rows["tests"][1:], (1, 1))
        self.assertEqual(rows["software"][1:], (2, 2))


class RenderTest(unittest.TestCase):
    def rows(self):
        return status.measure([item("production", "field"), item("functional", "simulator")])

    def test_the_bar_is_ten_cells_and_the_percent_is_rounded(self):
        self.assertEqual(status.mini_bar(0), "░" * 10)
        self.assertEqual(status.mini_bar(100), "█" * 10)
        self.assertEqual(len(status.mini_bar(37)), 10)
        self.assertEqual(status.percent_of(1, 3), 33)
        self.assertEqual(status.percent_of(2, 3), 67)
        self.assertEqual(status.percent_of(0, 0), 0)

    def test_every_language_has_every_text_with_its_placeholders(self):
        for area in status.AREAS:
            for lang in status.LANGS:
                self.assertIn("{k}", status.NOTE[area][lang], (area, lang))
                self.assertIn("{n}", status.NOTE[area][lang], (area, lang))
                self.assertTrue(status.LABEL[area][lang], (area, lang))
        for lang in status.LANGS:
            self.assertEqual(len(status.COLUMNS[lang]), 4, lang)
            self.assertTrue(status.HEADING[lang] and status.INTRO[lang], lang)

    def test_the_table_has_one_line_per_area_and_the_light_the_bar_and_the_count(self):
        text = status.table("es", self.rows())
        lines = text.split("\n")
        self.assertEqual(len(lines), 2 + len(status.AREAS))
        self.assertIn("| Pruebas |", text)
        self.assertIn("2 de 2 repositorios tienen pruebas automáticas.", text)
        self.assertIn("100%", text)

    def test_the_block_is_created_after_the_progress_bar_and_rewritten_in_place(self):
        base = "# Title\n\n<!-- progress:hydra-umc -->\nbar\n<!-- /progress:hydra-umc -->\n\ntext\n"
        text = base
        for eco in status.ECOSYSTEMS:
            text += f"\n<!-- progress:{eco} -->\nbar\n<!-- /progress:{eco} -->\n" if eco != "hydra-umc" else ""
        rows = {eco: self.rows() for eco in status.ECOSYSTEMS}
        once = status.update_readme(text, "README.md", rows)
        self.assertIn("<!-- status:hydra-umc -->", once)
        self.assertIn("### 🚦 Ecosystem status", once)
        self.assertLess(once.index("<!-- /progress:hydra-umc -->"), once.index("<!-- status:hydra-umc -->"))
        self.assertEqual(status.update_readme(once, "README.md", rows), once)
        spanish = status.update_readme(text, "README_spa.md", rows)
        self.assertIn("### 🚦 Estado del ecosistema", spanish)
        changed = dict(rows)
        changed["urtc"] = status.measure([item("scaffolding", "none", releases=0, tests=False, ci=False, readmes=1)])
        self.assertNotEqual(status.update_readme(once, "README.md", changed), once)

    def test_every_readme_file_has_a_language(self):
        self.assertEqual(set(status.FILE_LANG), set(status.README_FILES))
        self.assertEqual(sorted(status.FILE_LANG.values()), sorted(status.LANGS))


if __name__ == "__main__":
    unittest.main()
