# =============================================================================
# JuanenRac profile - tests/test_readme_parity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The eight profile READMEs must stay parallel: same section structure,
same set of GitHub links and the same number of table rows, so a section
added or dropped in one language cannot go unnoticed."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS = ["README_spa.md", "README_deu.md", "README_fra.md", "README_ita.md", "README_jpn.md", "README_zho.md", "README_por.md"]


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


LIGHTS = ("🟢", "🟡", "🟠", "🔴")


def status_lights(path: Path):
    """The lights of the "Project status" table, or None when the section is missing or malformed.

    The section is the first `## ` heading of the profile README (right after the introduction), has the legend with the
    four lights and a table whose State column holds only a light."""
    lines = path.read_text(encoding="utf-8").splitlines()
    heads = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if len(heads) < 2 or not lines[heads[0]].startswith("## 🚦 "):
        return None
    block = lines[heads[0]:heads[1]]
    if not all(light in " ".join(block) for light in LIGHTS):
        return None
    lights = []
    for row in [line for line in block if line.startswith("|")][2:]:
        cells = [part.strip() for part in re.split(r"(?<!\\)\|", row.strip().strip("|"))]
        if len(cells) != 3 or cells[1] not in LIGHTS or not cells[0] or not cells[2]:
            return None
        lights.append(cells[1])
    return lights if len(lights) >= 3 else None


class ProjectStatusTests(unittest.TestCase):
    def test_every_readme_has_the_project_status_table(self):
        english = status_lights(ROOT / "README.md")
        self.assertIsNotNone(english, "README.md has no valid 'Project status' table before its first section")
        for name in TRANSLATIONS:
            with self.subTest(readme=name):
                self.assertEqual(status_lights(ROOT / name), english, "the 'Project status' table is missing or its lights differ")


if __name__ == "__main__":
    unittest.main()
