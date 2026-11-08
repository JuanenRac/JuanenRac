# =============================================================================
# JuanenRac profile - tests/test_check_data_read.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""A page generated without the figures of the Code, Changelog or Scripts tabs is refused, and the workflows chain so that it is regenerated once they exist."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_data_read as cdr  # noqa: E402


def page(code: bool, scripts: bool) -> str:
    data = {"code": {"read": code, "repos": {}}, "scripts": {"read": scripts, "repos": {}}}
    return '<html><script type="application/json" id="dashboard-data">' + json.dumps(data) + "</script></html>"


class UnreadBlocks(unittest.TestCase):
    def test_a_page_with_every_block_read_passes(self):
        self.assertEqual(cdr.unread_blocks(page(True, True)), [])

    def test_the_tabs_of_an_unread_block_are_named(self):
        self.assertEqual(cdr.unread_blocks(page(False, True)), ["Code", "Changelog"])
        self.assertEqual(cdr.unread_blocks(page(True, False)), ["Scripts"])
        self.assertEqual(cdr.unread_blocks(page(False, False)), ["Code", "Changelog", "Scripts"])

    def test_a_page_without_data_or_with_broken_data_is_refused(self):
        self.assertEqual(len(cdr.unread_blocks("<html></html>")), 3)
        self.assertEqual(len(cdr.unread_blocks('<script type="application/json" id="dashboard-data">{broken</script>')), 3)
        self.assertEqual(len(cdr.unread_blocks('<script type="application/json" id="dashboard-data">[]</script>')), 3)

    def test_read_must_be_true_not_just_present(self):
        data = {"code": {"read": "yes"}, "scripts": {"read": 1}}
        self.assertEqual(len(cdr.unread_blocks('<script type="application/json" id="dashboard-data">' + json.dumps(data) + "</script>")), 3)

    def test_the_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            good, bad = Path(tmp) / "good.html", Path(tmp) / "bad.html"
            good.write_text(page(True, True), encoding="utf-8")
            bad.write_text(page(True, False), encoding="utf-8")
            self.assertEqual(cdr.main([str(good)]), 0)
            self.assertEqual(cdr.main([str(bad)]), 1)
            self.assertEqual(cdr.main([str(Path(tmp) / "missing.html")]), 1)

    def test_the_real_generator_embeds_read_true_when_the_data_files_are_there(self):
        import dashboard_code
        import dashboard_scripts
        if dashboard_code.load() is None or dashboard_scripts.load() is None:
            self.skipTest("the data files are not in this checkout")
        self.assertTrue(dashboard_code.build(dashboard_code.load(), dashboard_code.load_history(), "2001-01-01")["read"])
        self.assertTrue(dashboard_scripts.build(dashboard_scripts.load(), "2001-01-01")["read"])


class Chain(unittest.TestCase):
    """The counter commits its data with the token of its own workflow, which does not start a push run: the dashboard is rebuilt when the counter ends instead."""
    build = (ROOT / ".github" / "workflows" / "build-dashboard.yml").read_text(encoding="utf-8")
    count = (ROOT / ".github" / "workflows" / "code-stats.yml").read_text(encoding="utf-8")

    def test_the_dashboard_follows_the_counter(self):
        self.assertIn("workflow_run:", self.build)
        self.assertIn('- "Count the code of the ecosystems"', self.build)
        self.assertIn("completed", self.build.split("workflow_run:", 1)[1][:200])
        self.assertIn("name: Count the code of the ecosystems", self.count)

    def test_no_loop(self):
        # the counter never reacts to the dashboard: it runs on a schedule or by hand only
        triggers = self.count.split("on:", 1)[1].split("concurrency:", 1)[0]
        for forbidden in ("workflow_run", "push:", "pull_request", "repository_dispatch"):
            self.assertNotIn(forbidden, triggers)

    def test_a_failed_counter_does_not_rebuild(self):
        self.assertIn("github.event.workflow_run.conclusion == 'success'", self.build)

    def test_the_figures_of_all_groups_travel_together(self):
        # one counter writes the three documents (code, history, scripts) in one run and the publishing job commits them in one commit, so the
        # dashboard that follows it never finds the Scripts tab without its figures, whatever the number of groups counted
        for name in ("code-stats.json", "code-history.json", "scripts-stats.json"):
            self.assertIn(f'cp "$workdir/{name}" data/{name}', self.count)
        self.assertIn("git add data/code-stats.json data/code-history.json data/scripts-stats.json", self.count)
        self.assertIn("needs: count", self.count)
        self.assertIn("python scripts/code_stats.py --out", self.count)

    def test_the_build_checks_that_the_figures_were_read(self):
        self.assertIn("python scripts/check_data_read.py docs/index.html", self.build)


if __name__ == "__main__":
    unittest.main()
