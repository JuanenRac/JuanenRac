import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ecosystem_progress as progress  # noqa: E402


class PointsTest(unittest.TestCase):
    def test_a_project_counts_for_its_maturity_and_for_the_evidence_of_its_manifest(self):
        self.assertEqual(progress.project_points({"maturity": "scaffolding"}), 5)
        self.assertEqual(progress.project_points({"maturity": "functional", "evidence": "host-test"}), 23)
        self.assertEqual(progress.project_points({"maturity": "functional", "evidence": "simulator"}), 28)
        self.assertEqual(progress.project_points({"maturity": "established", "evidence": "bench"}), 50)
        self.assertEqual(progress.project_points({"maturity": "production", "evidence": "field"}), 70)
        self.assertEqual(progress.project_points({}), 0)

    def test_a_repository_that_is_not_bound_to_hardware_counts_as_tried_on_the_bench_once_it_is_functional(self):
        self.assertEqual(progress.project_points({"maturity": "functional", "evidence": "none", "hardware_bound": False}), 35)
        self.assertEqual(progress.project_points({"maturity": "scaffolding", "evidence": "none", "hardware_bound": False}), 5)

    def test_releases_tests_a_green_ci_and_the_eight_readmes_add_their_points(self):
        for releases, points in ((0, 0), (1, 4), (2, 4), (3, 8), (6, 11), (10, 13), (19, 13), (20, 15), (40, 15)):
            self.assertEqual(progress.delivery_points(releases), points, releases)
        full = {"releases": 20, "tests": True, "ci": True, "readmes": 8}
        self.assertEqual(progress.project_points({"maturity": "production", "evidence": "field"}, full), 100)
        self.assertEqual(progress.project_points({"maturity": "scaffolding", "evidence": "none"}, {"releases": 0, "tests": False, "ci": False, "readmes": 1}), 5)
        self.assertEqual(progress.project_points({"maturity": "scaffolding", "evidence": "host-test"}, {"releases": 6, "tests": True, "ci": True, "readmes": 8}), 5 + 3 + 11 + 15)

    def test_the_ecosystem_is_the_mean_of_the_projects_whose_manifest_can_be_read(self):
        manifests = {"a": {"maturity": "established"}, "b": {"maturity": "scaffolding"}, "c": None}
        self.assertEqual(progress.ecosystem_percent(["a", "b", "c"], manifests.get), (20, 2))
        self.assertEqual(progress.ecosystem_percent(["c"], manifests.get), (0, 0))


class BarTest(unittest.TestCase):
    def test_the_bar_has_twenty_cells_and_the_partial_block_of_the_eighths(self):
        self.assertEqual(progress.bar(0), "░" * 20)
        self.assertEqual(progress.bar(100), "█" * 20)
        self.assertEqual(progress.bar(54), "██████████▊░░░░░░░░░")
        for percent in range(0, 101):
            self.assertEqual(len(progress.bar(percent)), 20, percent)


class ReadmeTest(unittest.TestCase):
    NUMBERS = {eco: (50, 3) for eco in progress.ECOSYSTEMS}

    def sample(self):
        return "# Title\n\n## Status\n\n# H\n\ntext\n\n## 📈 Progress\n\n`[██████████▊░░░░░░░░░] 54%` — old\n\n# U\n\n**Updater:** x\n\n## How\n\n# A\n\n**Updater:** y\n\n## How\n\n# E\n\n**Updater:** z\n\n## How\n\n# T\n\n**Updater:** w\n\n## How\n"

    def test_the_blocks_are_created_once_and_then_only_refreshed(self):
        first = progress.update_readme(self.sample(), "README.md", self.NUMBERS)
        for eco in progress.ECOSYSTEMS:
            self.assertEqual(first.count(f"<!-- progress:{eco} -->"), 1)
        self.assertNotIn("old", first)
        again = progress.update_readme(first, "README.md", {**self.NUMBERS, "urtc": (80, 9)})
        self.assertIn("] 80%", again)
        self.assertEqual(again.count("<!-- progress:urtc -->"), 1)
        self.assertEqual(progress.update_readme(again, "README.md", {**self.NUMBERS, "urtc": (80, 9)}), again)

    def test_every_language_has_its_sentence_and_its_status_row(self):
        for name in progress.README_FILES:
            self.assertIn("{n}", progress.TEXT[name], name)
            self.assertTrue(progress.STATUS_ROW[name].startswith("| "), name)
            self.assertEqual(progress.STATUS_ROW[name].count("|"), 4, name)

    def test_the_real_readmes_are_up_to_date_with_the_manifests_next_to_them(self):
        repos = progress.ecosystem_repos((progress.ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(list(repos), list(progress.ECOSYSTEMS))
        self.assertTrue(all(repos[eco] for eco in progress.ECOSYSTEMS))
        for name in progress.README_FILES:
            text = (progress.ROOT / name).read_text(encoding="utf-8")
            for eco in progress.ECOSYSTEMS:
                self.assertIn(f"<!-- progress:{eco} -->", text, f"{name} {eco}")


if __name__ == "__main__":
    unittest.main()
