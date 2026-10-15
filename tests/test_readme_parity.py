# =============================================================================
# JuanenRac profile - tests/test_readme_parity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The seven profile READMEs must stay parallel: same section structure,
same set of GitHub links and the same number of table rows, so a section
added or dropped in one language cannot go unnoticed."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS = ["README_spa.md", "README_deu.md", "README_fra.md", "README_ita.md", "README_jpn.md", "README_zho.md"]


def shape(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return {
        "headings": [len(m.group(1)) for m in re.finditer(r"^(#{1,6}) ", text, re.M)],
        "links": sorted(set(re.findall(r"https://github\.com/JuanenRac/[A-Za-z0-9._-]+", text))),
        "table_rows": len(re.findall(r"^\|", text, re.M)),
    }


class ReadmeParityTests(unittest.TestCase):
    def test_every_translation_has_the_english_structure(self):
        english = shape(ROOT / "README.md")
        for name in TRANSLATIONS:
            with self.subTest(readme=name):
                other = shape(ROOT / name)
                self.assertEqual(other["headings"], english["headings"], "heading levels/order differ")
                self.assertEqual(other["links"], english["links"], "GitHub links differ")
                self.assertEqual(other["table_rows"], english["table_rows"], "table row count differs")


if __name__ == "__main__":
    unittest.main()
