# =============================================================================
# JuanenRac profile - tests/test_dashboard_ecosystem_parity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Every ecosystem of the catalogue is shown at the same level in every tab.

The catalogue (ecosystem-catalog.json) lists the groups the dashboard reports. Each list of ecosystems that the generator or the scripts of a tab keep for themselves
(the tabs, the scope bar, the filters, the charts of the evolution, the analysis, the tests, the builds, the Sentinel, the shortcuts, the architecture switcher, the
colours) must hold exactly those keys in that order, so that a group is never left out of one tab while the others show it."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dashboard_app as app  # noqa: E402
import dashboard_charts as charts  # noqa: E402
import dashboard_evo  # noqa: E402
import dashboard_pins as pins  # noqa: E402
import dashboard_tests as tests_mod  # noqa: E402
import ecosystem_progress as progress  # noqa: E402

CATALOG = json.loads((ROOT / "ecosystem-catalog.json").read_text(encoding="utf-8"))
KEYS = [e["key"] for e in CATALOG["ecosystems"]]
LABELS = {e["key"]: e["label"] for e in CATALOG["ecosystems"]}


def source(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8")


def js_list(text: str, name: str) -> list[str]:
    found = re.search(r"const " + re.escape(name) + r" = \[([^\]]*)\];", text)
    assert found, name
    return re.findall(r'"([^"]+)"', found.group(1))


class CatalogTests(unittest.TestCase):
    def test_the_catalogue_has_the_five_groups(self):
        self.assertEqual(KEYS, ["hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"])

    def test_the_python_lists_hold_the_catalogue(self):
        self.assertEqual([k for k, _ in app.ECOSYSTEMS], KEYS)
        self.assertEqual({k: v for k, v in app.ECOSYSTEMS}, LABELS)
        self.assertEqual(list(charts.ECOSYSTEM_KEYS), KEYS)
        self.assertEqual(list(tests_mod.ECOSYSTEMS), KEYS)
        self.assertEqual(list(progress.ECOSYSTEMS), KEYS)
        self.assertEqual([k for k, *_ in app.SCOPES if k != "all"], KEYS)
        self.assertEqual(sorted(dashboard_evo.ECO_RGB), sorted(KEYS))

    def test_every_group_has_a_tab_a_colour_and_a_class(self):
        for key in KEYS:
            self.assertIn(key, app.TAB_IDS)
            self.assertIn(f"--c-{key}:", app.CSS)
            self.assertIn(f".eco-{key} {{", app.CSS)

    def test_the_pins_card_names_every_group(self):
        doc = pins.read_all("o", {}, lambda path: ("absent", None))
        self.assertEqual(sorted(doc), sorted(KEYS))


class ScriptListTests(unittest.TestCase):
    def test_each_chart_script_lists_the_catalogue_in_order(self):
        for name, const in (("dashboard_evo_ui.py", "EVO_ECOS"), ("dashboard_evo_ui.py", "EV_ECOS"), ("dashboard_insight_ui.py", "INS_ECOS"),
                            ("dashboard_tests_ui.py", "TS_ECOS"), ("dashboard_actions_ui.py", "AC_ECOS")):
            self.assertEqual(js_list(source(name), const), KEYS, f"{name} {const}")

    def test_each_label_map_names_every_group(self):
        for name, const in (("dashboard_evo_ui.py", "EVO_LABEL"), ("dashboard_insight_ui.py", "INS_LABEL"), ("dashboard_tests_ui.py", "TS_LABEL"),
                            ("dashboard_actions_ui.py", "AC_LABEL"), ("dashboard_sentinel_ui.py", "SN_ECO_NAMES")):
            found = re.search(r"const " + const + r" = \{([^}]*)\};", source(name))
            self.assertTrue(found, f"{name} {const}")
            pairs = dict(re.findall(r'"?([a-z0-9-]+)"?: "([^"]+)"', found.group(1)))
            self.assertEqual(pairs, LABELS, f"{name} {const}")

    def test_the_series_of_the_evolution_charts_have_a_colour_each(self):
        css = source("dashboard_evo_ui.py")
        for key in KEYS:
            self.assertIn(f".evo-s-{key} {{", css)

    def test_the_number_keys_open_the_groups_in_order(self):
        found = re.search(r"const ECO_KEYS = \{([^}]*)\};", source("dashboard_nav_ui.py"))
        self.assertTrue(found)
        mapping = dict(re.findall(r'"(\d)": "([a-z0-9-]+)"', found.group(1)))
        self.assertEqual([mapping[str(i)] for i in range(1, len(KEYS) + 1)], KEYS)
        import dashboard_nav_ui
        listed = [keys for keys, key in dashboard_nav_ui.SHORTCUTS if key == "help_k_eco"][0]
        self.assertEqual(list(listed), [str(i) for i in range(1, len(KEYS) + 1)])

    def test_the_markers_of_the_charts_are_not_the_same_for_two_groups(self):
        for name, marker in (("dashboard_evo_ui.py", "kind === 3"), ("dashboard_insight_ui.py", "kind === 3")):
            self.assertIn(marker, source(name))
        self.assertIn('"3 3 9 3"', source("dashboard_insight_ui.py"))           # a fifth dash pattern for the radars, so a line is told apart without colour


class ArchitectureTests(unittest.TestCase):
    def test_the_switcher_and_the_panels_cover_the_catalogue(self):
        text = source("generate_dashboard.py")
        for key in KEYS:
            self.assertIn(f'data-arch-view="{key}"', text)
            self.assertIn(f'data-arch-panel="{key}"', text)

    def test_the_tools_section_is_made_of_the_same_parts_as_the_one_of_eh3d(self):
        eh3d, tools = app.eh3d_architecture_section(), app.tools_architecture_section()
        for part in ("architecture-grid", "architecture-flow", "relationship-note", "architecture-card"):
            self.assertIn(part, eh3d)
            self.assertIn(part, tools)
        self.assertGreaterEqual(tools.count("<article"), 3)           # one card for each of the three repositories of the group
        self.assertEqual(eh3d.count("<b>→</b>"), tools.count("<b>→</b>"))

    def test_the_texts_of_the_tools_section_exist_in_the_eight_languages(self):
        import dashboard_app_texts
        self.assertEqual(dashboard_app_texts.problems(), [])
        for key in ("architecture_section_t", "architecture_t_card1_title", "architecture_t_card3_body", "architecture_t_flow_4", "architecture_t_rel_body", "aria_tools_flow"):
            for code, values in dashboard_app_texts.TEXTS.items():
                self.assertTrue(values[key], (key, code))


if __name__ == "__main__":
    unittest.main()
