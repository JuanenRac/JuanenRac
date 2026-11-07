# =============================================================================
# JuanenRac profile - tests/test_dashboard_life.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The life of the charts of the Code, Changelog, Scripts and Builds tabs: figures that count up, a discreet pulse on what is red or running, a highlight on hover.
All of it must stop with prefers-reduced-motion and must never change the text a figure ends with."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_actions_ui as actions  # noqa: E402
import dashboard_changes_ui as changes  # noqa: E402
import dashboard_code_ui as code  # noqa: E402
import dashboard_scripts_ui as scripts  # noqa: E402


class CountUp(unittest.TestCase):
    def test_the_helper_respects_reduced_motion_and_ends_with_the_exact_text(self):
        js = code.JS
        body = js.split("function cdLiveFigure(text)", 1)[1].split("function cdLegendItem", 1)[0]
        self.assertIn("prefers-reduced-motion: reduce", body)
        self.assertIn("requestAnimationFrame", body)
        self.assertRegex(body, r"k < 1 \? cdNum\(Math\.round\(to \* e\)\) \+ m\[2\] : text")     # the last frame is the text it was given
        self.assertIn("digits.length <= 9", body)

    def test_every_key_figure_of_the_four_tabs_uses_it(self):
        for module in (code, changes, scripts, actions):
            self.assertIn("cdLiveFigure(it[1])", module.JS)
            self.assertNotIn('li.appendChild(make("b", "", it[1]))', module.JS)


class Motion(unittest.TestCase):
    def test_the_pulses_are_inside_the_no_preference_query(self):
        css = code.CSS
        for name in ("cd-pulse-bad", "cd-breath"):
            at = css.index("@keyframes " + name)
            query = css.rfind("@media (prefers-reduced-motion: no-preference)", 0, at)
            self.assertGreaterEqual(query, 0, name)
            self.assertNotIn("@media", css[query + 10:at])
        for use in (".ac-kpi.ac-bad { animation:", ".ac-sw.ac-c-p { animation:"):
            self.assertIn(use, css)

    def test_hovering_a_segment_dims_the_others(self):
        self.assertIn(".cd-chart:has(.cd-seg:hover) .cd-seg:not(:hover) { opacity: .62; }", code.CSS)
        self.assertIn(".ac-bar:hover .ac-fill { filter: brightness(1.2); }", code.CSS)

    def test_every_animation_of_the_new_css_is_in_a_reduced_motion_query(self):
        for module in (code, changes, scripts):
            css = module.CSS
            for match in re.finditer(r"\banimation:", css):
                query = css.rfind("@media (prefers-reduced-motion", 0, match.start())
                self.assertGreaterEqual(query, 0, css[match.start() - 60:match.start() + 40])


if __name__ == "__main__":
    unittest.main()
