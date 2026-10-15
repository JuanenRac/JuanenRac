# =============================================================================
# JuanenRac profile - tests/test_catalog_check.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from catalog_check import CATALOG_PATH, catalog_ecosystems, mismatches  # noqa: E402

DASHBOARD = [
    ("hydra-umc", "HYDRA-UMC", "hydra-umc.project.json"),
    ("urtc", "URTC", "urtc.project.json"),
    ("armor", "A.R.M.O.R.", "armor.project.json"),
    ("electro-hobby-3d", "Electro Hobby 3D", "electro-hobby-3d.project.json"),
]


class CatalogCheckTests(unittest.TestCase):
    def test_the_real_catalog_lists_every_ecosystem_the_dashboard_reports(self):
        self.assertEqual(mismatches(catalog_ecosystems(CATALOG_PATH.read_text(encoding="utf-8")), DASHBOARD), [])

    def test_the_real_catalog_keeps_the_hydra_umc_discovery_fields(self):
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data["ecosystem"], "HYDRA-UMC")
        self.assertEqual(data["manifest_file"], "hydra-umc.project.json")

    def test_missing_wrong_and_extra_ecosystems_are_reported(self):
        catalog = [("urtc", "URTC", "urtc.project.json"), ("old", "Old", "old.json"),
                   ("armor", "A.R.M.O.R.", "wrong.json")]
        problems = mismatches(catalog, DASHBOARD)
        self.assertTrue(any("'hydra-umc' but the catalog" in p for p in problems))
        self.assertTrue(any("lists 'old'" in p for p in problems))
        self.assertTrue(any("'armor'" in p and "wrong.json" in p for p in problems))

    def test_malformed_catalogs_are_rejected(self):
        with self.assertRaises(ValueError):
            catalog_ecosystems("{}")
        with self.assertRaises(ValueError):
            catalog_ecosystems(json.dumps({"ecosystems": [{"key": "x"}]}))


if __name__ == "__main__":
    unittest.main()
