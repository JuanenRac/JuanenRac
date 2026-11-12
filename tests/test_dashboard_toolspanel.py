# =============================================================================
# JuanenRac profile - tests/test_dashboard_toolspanel.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The own tab of the Tools group: the data of the rows, the page it draws, its texts in eight languages and that the Tools are the fifth ecosystem of the shell."""
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import dashboard_app as app  # noqa: E402
import dashboard_toolspanel as tp  # noqa: E402
import dashboard_toolspanel_texts as texts  # noqa: E402

ECO = {"TOOLS-GITHUB-ACTIONS-MONITOR": "electro-hobby-3d", "ELECTRO-HOBBY-3D-UPDATER": "electro-hobby-3d", "ARMOR-SERVER": "armor"}
MANIFESTS = {"TOOLS-GITHUB-ACTIONS-MONITOR": {"maturity": "functional", "evidence": "host-test"}, "ELECTRO-HOBBY-3D-UPDATER": {"maturity": "functional"}}


def activity(ci="success", tag="v1.0.0", date="2001-12-20T08:00:00Z"):
    return SimpleNamespace(ci=ci, release_tag=tag, release_date=date)


def build(**over):
    args = dict(ecosystem_by_name=ECO, versions={"TOOLS-GITHUB-ACTIONS-MONITOR": "1.7.6", "ELECTRO-HOBBY-3D-UPDATER": "0.1.5"},
                activity={"TOOLS-GITHUB-ACTIONS-MONITOR": activity(), "ELECTRO-HOBBY-3D-UPDATER": activity("pending", "v0.1.5")},
                tests_read={"records": {"TOOLS-GITHUB-ACTIONS-MONITOR": {"n": 1200}}}, sentinel_doc={"ci": {"red": []}}, manifest_of=lambda n: MANIFESTS.get(n))
    args.update(over)
    return tp.build(**args)


class RowsTests(unittest.TestCase):
    def test_only_the_tools_in_name_order_with_their_facts(self):
        block = build()
        self.assertEqual([r["name"] for r in block["rows"]], ["ELECTRO-HOBBY-3D-UPDATER", "TOOLS-GITHUB-ACTIONS-MONITOR"])
        monitor = block["rows"][1]
        self.assertEqual((monitor["version"], monitor["tag"], monitor["published"], monitor["ci"], monitor["tests"], monitor["maturity"]),
                         ("1.7.6", "v1.0.0", "2001-12-20", "success", 1200, "functional"))
        self.assertEqual(block["rows"][0]["ci"], "pending")
        self.assertIsNone(block["rows"][0]["tests"])

    def test_a_red_workflow_of_the_sentinel_makes_the_tool_red_whatever_the_last_commit_says(self):
        red = {"ci": {"red": [{"repo": "TOOLS-GITHUB-ACTIONS-MONITOR", "wf": "ci.yml", "streak": 2}]}}
        row = build(sentinel_doc=red)["rows"][1]
        self.assertEqual((row["ci"], row["red"]), ("failure", 1))

    def test_what_could_not_be_read_is_never_green(self):
        block = build(activity={}, tests_read=None, sentinel_doc=None)
        for row in block["rows"]:
            self.assertEqual((row["ci"], row["tests"], row["red"], row["tag"]), ("none", None, None, None))
        self.assertEqual(block["read"], {"activity": False, "tests": False, "sentinel": False})

    def test_an_unknown_state_is_none(self):
        self.assertEqual(build(activity={"TOOLS-GITHUB-ACTIONS-MONITOR": activity("weird")})["rows"][1]["ci"], "none")

    def test_no_tool_listed(self):
        self.assertEqual(build(ecosystem_by_name={"ARMOR-SERVER": "armor"})["rows"], [])


class PageTests(unittest.TestCase):
    def setUp(self):
        self.html = tp.panel_html(build(), texts.TEXTS["en"])

    def test_the_cards_and_the_testids_the_browser_tests_use(self):
        for testid in ("tools-table-card", "tools-table", "tools-monitor", "tools-editions", "tools-ai", "tools-quota", "tools-next", "tools-updater",
                       "tools-row-TOOLS-GITHUB-ACTIONS-MONITOR", "tools-ci-ELECTRO-HOBBY-3D-UPDATER", "tools-ai-guide"):
            self.assertIn(f'data-testid="{testid}"', self.html, testid)

    def test_the_next_version_is_not_written_as_published_and_has_no_date_or_number(self):
        self.assertIn("Not published yet", texts.TEXTS["en"]["tl_mon_next_body"])
        self.assertNotRegex(texts.TEXTS["en"]["tl_mon_next_body"], r"\d+\.\d+|\b20\d\d\b")

    def test_every_link_goes_to_the_owner(self):
        for href in re.findall(r'href="([^"]+)"', self.html):
            self.assertTrue(href.startswith("https://github.com/JuanenRac/"), href)

    def test_no_tool_says_so_and_still_has_the_monitor_card(self):
        html = tp.panel_html({"rows": [], "read": {}}, texts.TEXTS["en"])
        self.assertIn('data-testid="tools-empty"', html)
        self.assertIn("tools-monitor", html)

    def test_a_name_with_markup_is_escaped(self):
        row = {"name": '<b onmouseover="x">', "version": "<i>", "maturity": None, "tag": None, "published": "", "ci": "none", "red": None, "tests": None}
        html = tp.panel_html({"rows": [row], "read": {}}, texts.TEXTS["en"])
        self.assertNotIn("<b onmouseover", html)
        self.assertNotIn("<i>", html)

    def test_every_key_it_uses_exists(self):
        for key in set(re.findall(r'data-i18n="([^"]+)"', self.html)):
            self.assertIn(key, texts.TEXTS["en"], key)


class TextsTests(unittest.TestCase):
    def test_eight_languages_no_empty_text(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        self.assertEqual({len(v) for v in texts.TEXTS.values()}, {len(texts.TEXTS["en"])})

    def test_portuguese_is_the_one_of_portugal(self):
        pt = " ".join(texts.TEXTS["pt"].values()).lower()
        for brazilian in ("arquivo", "tela ", "celular", "atualizar "):
            self.assertNotIn(brazilian, pt)

    def test_nothing_private_in_the_texts(self):
        everything = " ".join(" ".join(t.values()) for t in texts.TEXTS.values()).lower()
        for word in ("audit", "claude", "sonnet", "openai", "c:\\"):
            self.assertNotIn(word, everything)


class ShellTests(unittest.TestCase):
    def test_tools_are_the_fifth_ecosystem_with_a_tab_after_eh3d(self):
        self.assertEqual([k for k, _ in app.ECOSYSTEMS], ["hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"])
        self.assertEqual(app.TAB_IDS[app.TAB_IDS.index("eh3d") + 1], "electro-hobby-3d")
        self.assertEqual(app.ECOSYSTEM_FILTERS, app.ECOSYSTEMS)


if __name__ == "__main__":
    unittest.main()
