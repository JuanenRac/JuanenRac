# =============================================================================
# Electro Hobby 3D - tests/test_project_banner.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The project banners are well formed, carry the name of the project and fit their text."""
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import project_banner as pb  # noqa: E402


def manifest(name="ARMOR-RADAR", role="firmware", technologies=("C++", "ESP-IDF", "MQTT", "UART", "I2C"), family="Field nodes"):
    return {"name": name, "role": role, "technologies": list(technologies), "family": family, "stack": "c++"}


class ProjectBannerTests(unittest.TestCase):
    def test_every_ecosystem_gives_well_formed_svg_with_the_name_and_four_chips_at_most(self):
        for key in pb.STYLES:
            svg = pb.banner_for(manifest("TEST-PROJECT"), key)
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.endswith("svg"))
            self.assertIn("TEST-PROJECT", svg)
            self.assertEqual(svg.count('r="4" fill="#') - 0, svg.count('r="4" fill="#'))   # chips are circles of radius 4
            chips = re.findall(r'<rect x="\d+" y="0" width="\d+" height="22" rx="11" fill="#161B22"', svg)
            self.assertEqual(len(chips), 4)
            for glow in (pb.STYLES[key].glow,) + ((pb.STYLES[key].gradient,) if pb.STYLES[key].gradient else ()):
                self.assertIn(f'id="{glow}"', svg, f"{key}: the template has no {glow}")

    def test_a_long_name_gets_a_smaller_font_and_a_short_one_keeps_the_big_one(self):
        long_svg = pb.banner_for(manifest("HYDRA-UMC-VISUAL-SERVOING-API"), "hydra-umc")
        short_svg = pb.banner_for(manifest("ARMOR-HMI"), "armor")
        size = lambda svg, name: int(re.search(rf'font-size="(\d+)"[^>]*>{name}</text>', svg).group(1))  # noqa: E731
        self.assertLess(size(long_svg, "HYDRA-UMC-VISUAL-SERVOING-API"), 40)
        self.assertEqual(size(short_svg, "ARMOR-HMI"), 56)

    def test_text_from_the_manifest_is_escaped(self):
        svg = pb.banner_for(manifest("A&B", technologies=("<script>", "R&D")), "urtc")
        ET.fromstring(svg)
        self.assertNotIn("<script>", svg)
        self.assertIn("A&amp;B", svg)

    def test_a_manifest_with_no_technologies_still_makes_a_banner(self):
        ET.fromstring(pb.banner_for(manifest(technologies=()), "eh3d"))

    def test_role_label_reads_enum_roles_and_free_text(self):
        self.assertEqual(pb.role_label({"role": "api"}), "SERVICE")
        self.assertEqual(pb.role_label({"role": "ui"}), "APP")
        self.assertEqual(pb.role_label({"role": "library"}), "LIBRARY")
        self.assertEqual(pb.role_label({"role": "Field node: ESP32-S3 radar firmware"}), "FIRMWARE")
        self.assertEqual(pb.role_label({"role": "Operator console", "name": "ARMOR-STUDIO"}), "APP")
        self.assertEqual(pb.role_label({"role": "something odd", "name": "X"}), "PROJECT")

    def test_the_same_manifest_always_gives_the_same_banner(self):
        self.assertEqual(pb.banner_for(manifest(), "armor"), pb.banner_for(manifest(), "armor"))


if __name__ == "__main__":
    unittest.main()
