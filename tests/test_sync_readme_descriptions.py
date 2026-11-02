import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_readme_descriptions as desc  # noqa: E402

TEXTS = {lang: f"text {lang}" for lang in desc.LANGUAGES}
SOURCE = {"HYDRA-UMC-X": TEXTS}
ROW = "| [HYDRA-UMC-X](https://github.com/JuanenRac/HYDRA-UMC-X) | 0.1.0 | old |"
COMPACT = "|[HYDRA-UMC-X](https://github.com/JuanenRac/HYDRA-UMC-X)|0.1.0|old|"
EXEMPT_ROW = "| [EH3D-Y](https://github.com/JuanenRac/EH3D-Y) | 0.0.1 | by hand |"


class ProcessTest(unittest.TestCase):
    def run_process(self, lines, source=SOURCE, lang="en"):
        seen = set()
        out, changed, problems = desc.process(lines, lang, source, ("EH3D-",), seen)
        return out, changed, problems, seen

    def test_rewrites_the_description_and_keeps_the_version(self):
        out, changed, problems, seen = self.run_process([ROW])
        self.assertEqual(out, ["| [HYDRA-UMC-X](https://github.com/JuanenRac/HYDRA-UMC-X) | 0.1.0 | text en |"])
        self.assertEqual((changed, problems, seen), (1, [], {"HYDRA-UMC-X"}))

    def test_keeps_the_compact_row_style_of_the_translations(self):
        out, _, _, _ = self.run_process([COMPACT], lang="es")
        self.assertEqual(out, ["|[HYDRA-UMC-X](https://github.com/JuanenRac/HYDRA-UMC-X)|0.1.0|text es|"])

    def test_a_current_row_is_not_counted(self):
        current, _, _, _ = self.run_process([ROW])
        _, changed, _, _ = self.run_process(current)
        self.assertEqual(changed, 0)

    def test_a_repository_without_an_entry_is_a_problem(self):
        out, changed, problems, _ = self.run_process([ROW], source={})
        self.assertEqual(out, [ROW])
        self.assertEqual(changed, 0)
        self.assertEqual(len(problems), 1)

    def test_a_missing_language_is_a_problem(self):
        source = {"HYDRA-UMC-X": {k: v for k, v in TEXTS.items() if k != "pt"}}
        self.assertEqual(len(self.run_process([ROW], source=source, lang="pt")[2]), 1)
        self.assertTrue(any("'pt'" in p for p in desc.validate(source)))

    def test_exempt_prefixes_stay_untouched(self):
        out, changed, problems, seen = self.run_process([EXEMPT_ROW])
        self.assertEqual((out, changed, problems, seen), ([EXEMPT_ROW], 0, [], set()))

    def test_other_lines_are_left_alone(self):
        lines = ["| Repository | Version | Description |", "| :--- | :--- | :--- |", "text"]
        self.assertEqual(self.run_process(lines)[0], lines)


class SourceTest(unittest.TestCase):
    def test_validation_flags_long_english_and_pipes(self):
        bad = {"A": dict(TEXTS, en="x" * 141), "B": dict(TEXTS, de="a | b")}
        problems = desc.validate(bad)
        self.assertEqual(len(problems), 2)

    def test_the_real_source_is_valid_and_complete(self):
        descriptions, exempt = desc.load_source()
        self.assertEqual(desc.validate(descriptions), [])
        self.assertTrue(descriptions)
        self.assertFalse([n for n in descriptions if n.startswith(exempt)])

    def test_every_language_has_a_status_row(self):
        self.assertEqual(set(desc.STATUS_ROW), set(desc.LANG_OF))
        for row in desc.STATUS_ROW.values():
            self.assertIn("🟢", row)

    def test_the_real_readmes_match_the_source(self):
        descriptions, exempt = desc.load_source()
        seen = set()
        for filename, lang in desc.LANG_OF.items():
            lines = (desc.ROOT / filename).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
            _, changed, problems = desc.process(lines, lang, descriptions, exempt, seen)
            self.assertEqual(problems, [], filename)
            self.assertEqual(changed, 0, filename)
        self.assertEqual(seen, set(descriptions))


if __name__ == "__main__":
    unittest.main()
