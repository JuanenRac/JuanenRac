# =============================================================================
# JuanenRac profile - tests/test_dashboard_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The Tools group of the dashboard: its name, the card with the version of each tool and the progress bar, the filter and the badge of the profile."""
import json
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
# In CI the updaters are installed packages; next to this repository they are source checkouts.
for sibling in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
    candidate = ROOT.parent / sibling / "src"
    if candidate.is_dir():
        sys.path.append(str(candidate))

import dashboard_app  # noqa: E402
import dashboard_cover_texts as texts  # noqa: E402
import dashboard_tools as tools  # noqa: E402
import ecosystem_progress  # noqa: E402
import generate_dashboard as gen  # noqa: E402

README_FILES = ["README.md", "README_spa.md", "README_deu.md", "README_fra.md", "README_ita.md", "README_jpn.md", "README_zho.md", "README_por.md"]
BY_NAME = {"TOOLS-GITHUB-ACTIONS-MONITOR": "electro-hobby-3d", "ELECTRO-HOBBY-3D-UPDATER": "electro-hobby-3d", "ARMOR-SERVER": "armor"}
RESULTS = {"TOOLS-GITHUB-ACTIONS-MONITOR": SimpleNamespace(version="1.6.2"), "ELECTRO-HOBBY-3D-UPDATER": SimpleNamespace(version="0.1.5"), "ARMOR-SERVER": SimpleNamespace(version="0.9.0")}


class GroupTests(unittest.TestCase):
    def test_the_group_is_called_tools_everywhere(self):
        catalog = json.loads((ROOT / "ecosystem-catalog.json").read_text(encoding="utf-8"))
        labels = {e["key"]: e["label"] for e in catalog["ecosystems"]}
        self.assertEqual(labels["electro-hobby-3d"], "Tools")
        self.assertEqual(dict(gen.ECOSYSTEM_ORDER)["electro-hobby-3d"], "Tools")
        self.assertEqual(dict(dashboard_app.ECOSYSTEM_FILTERS)["electro-hobby-3d"], "Tools")
        self.assertEqual([label for key, _i18n, label in dashboard_app.SCOPES if key == "electro-hobby-3d"], ["Tools"])
        self.assertEqual(dashboard_app_texts_scope("en"), "Tools")

    def test_the_name_of_the_group_follows_the_readme_in_every_language(self):
        names = {"en": "Tools", "es": "Herramientas", "de": "Werkzeuge", "fr": "Outils", "it": "Strumenti", "ja": "ツール", "zh": "工具", "pt": "Ferramentas"}
        for code, name in names.items():
            self.assertEqual(dashboard_app_texts_scope(code), name)

    def test_the_block_lists_the_tools_with_their_version(self):
        group = tools.block(BY_NAME, RESULTS, (67, 2))
        self.assertEqual(group, {"tools": [{"name": "ELECTRO-HOBBY-3D-UPDATER", "version": "0.1.5"}, {"name": "TOOLS-GITHUB-ACTIONS-MONITOR", "version": "1.6.2"}], "percent": 67, "count": 2})

    def test_a_tool_without_a_version_and_a_progress_that_is_unknown_are_not_invented(self):
        group = tools.block(BY_NAME, {"TOOLS-GITHUB-ACTIONS-MONITOR": SimpleNamespace(version=None)}, None)
        self.assertEqual(group["percent"], None)
        self.assertEqual([t["version"] for t in group["tools"]], [None, None])
        html = tools.card_html(group)
        self.assertIn("progress not verified", html)
        self.assertNotIn("role=\"progressbar\"", html)
        self.assertEqual(tools.block(BY_NAME, RESULTS, (50, 0))["percent"], None)

    def test_the_card_has_the_versions_the_bar_and_the_filter(self):
        html = tools.card_html(tools.block(BY_NAME, RESULTS, (67, 2)))
        for part in ('data-testid="eco-tools"', "<b>1.6.2</b>", "<b>0.1.5</b>", 'role="progressbar"', 'aria-valuenow="67"', "--w:67%",
                     'data-scope="electro-hobby-3d"', 'data-goto-tab="projects"', 'data-percent="67"', 'class="number">2<'):
            self.assertIn(part, html)

    def test_the_cards_of_the_summary_show_the_group_card_instead_of_the_plain_one(self):
        entries = [SimpleNamespace(name=n) for n in BY_NAME]
        html = gen.render_ecosystem_cards(entries, BY_NAME, None, tools=tools.block(BY_NAME, RESULTS, (67, 2)))
        self.assertEqual(html.count('data-testid="eco-tools"'), 1)
        self.assertEqual(html.count('class="health-card'), 5)      # the four ecosystems and the group
        plain = gen.render_ecosystem_cards(entries, BY_NAME, None)
        self.assertNotIn("eco-tools", plain)

    def test_the_animated_bar_stops_with_reduced_motion(self):
        self.assertIn("prefers-reduced-motion: no-preference", tools.CSS)
        self.assertIn(tools.CSS, dashboard_app.CSS)


def dashboard_app_texts_scope(code):
    import dashboard_app_texts
    return dashboard_app_texts.TEXTS[code]["scope_cross"]


class ProgressTests(unittest.TestCase):
    def test_the_progress_is_worked_out_like_the_four_ecosystems(self):
        manifests = {"A": {"maturity": "functional", "evidence": "host-test", "hardware_bound": False}, "B": {"maturity": "scaffolding", "evidence": "none"}}
        percent, counted = ecosystem_progress.ecosystem_percent(["A", "B"], lambda n: manifests.get(n), None)
        self.assertEqual(counted, 2)
        self.assertEqual(percent, round((ecosystem_progress.project_points(manifests["A"]) + ecosystem_progress.project_points(manifests["B"])) / 2))

    def test_the_helper_of_the_page_returns_none_when_nothing_can_be_read(self):
        self.assertIsNone(gen.tools_progress({"X": "armor"}, {}))
        original = ecosystem_progress.read_signals
        ecosystem_progress.read_signals = lambda name: None
        try:
            self.assertIsNone(gen.tools_progress({"T": "electro-hobby-3d"}, {}))
        finally:
            ecosystem_progress.read_signals = original

    def test_the_helper_of_the_page_uses_the_manifests_and_the_signals(self):
        raw = {"T": SimpleNamespace(data={"maturity": "functional", "evidence": "host-test", "hardware_bound": False})}
        original = ecosystem_progress.read_signals
        ecosystem_progress.read_signals = lambda name: {"releases": 3, "readmes": 8, "ci": True, "tests": True}
        try:
            percent, counted = gen.tools_progress({"T": "electro-hobby-3d"}, raw)
        finally:
            ecosystem_progress.read_signals = original
        self.assertEqual(counted, 1)
        self.assertGreater(percent, 40)


class TextsAndBadgeTests(unittest.TestCase):
    def test_every_text_of_the_group_is_in_the_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        for key in ("tools_progress", "tools_progress_unknown", "tools_filter"):
            for code in texts.LANGUAGES:
                self.assertTrue(texts.TEXTS[code][key])
            for code in ("es", "de", "fr", "ja", "zh"):
                self.assertNotEqual(texts.TEXTS[code][key], texts.TEXTS["en"][key])

    def test_the_badge_of_the_profile_counts_the_four_ecosystems_and_the_tools(self):
        for name in README_FILES:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertRegex(text, r"badge/Ecosystems-4%20%2B%20Tools-00E5FF\.svg", name)
            self.assertIsNone(re.search(r"badge/Ecosystems-4-00E5FF", text), name)
        self.assertEqual(tools.badge_alt(), "Four ecosystems + Tools")


if __name__ == "__main__":
    unittest.main()
