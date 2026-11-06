# =============================================================================
# JuanenRac profile - tests/test_ci_rules.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""One definition of a red run for the Sentinel tab, the Builds tab and the CI watch issue."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import ci_rules  # noqa: E402
import ci_watch  # noqa: E402
import dashboard_actions as actions  # noqa: E402
import dashboard_sentinel as sn  # noqa: E402
import ecosystem_inventory as inv  # noqa: E402


class Api:
    def __init__(self, payload):
        self.payload = payload

    def get(self, path):
        return self.payload


class CriterionTests(unittest.TestCase):
    def test_the_four_red_conclusions(self):
        for conclusion in ("failure", "timed_out", "startup_failure", "action_required"):
            self.assertTrue(ci_rules.is_red(conclusion), conclusion)
        for conclusion in ("success", "cancelled", "skipped", "neutral", "stale", "", None):
            self.assertFalse(ci_rules.is_red(conclusion), conclusion)

    def test_what_says_nothing(self):
        for conclusion in ("cancelled", "skipped", "neutral", "stale", "", None):
            self.assertTrue(ci_rules.says_nothing(conclusion), conclusion)
        self.assertFalse(ci_rules.says_nothing("success"))
        self.assertFalse(ci_rules.says_nothing("action_required"))

    def test_dynamic_runs_never_decide(self):
        self.assertTrue(ci_rules.is_dynamic({"event": "dynamic", "path": "dynamic/dependabot/dependabot-updates"}))
        self.assertTrue(ci_rules.is_dynamic({"path": "dynamic/github-actions"}))
        self.assertFalse(ci_rules.is_dynamic({"event": "push", "path": ".github/workflows/ci.yml"}))
        self.assertFalse(ci_rules.decides({"event": "dynamic", "conclusion": "failure", "path": ".github/workflows/x.yml"}))
        self.assertTrue(ci_rules.decides({"event": "push", "conclusion": "failure", "path": ".github/workflows/x.yml"}))


class ThreePlacesAgreeTests(unittest.TestCase):
    CONCLUSIONS = ("success", "failure", "timed_out", "startup_failure", "action_required", "cancelled", "skipped", "neutral", "stale")

    def test_sentinel_builds_tab_and_ci_watch_call_the_same_runs_red(self):
        for conclusion in self.CONCLUSIONS:
            run = {"path": ".github/workflows/ci.yml", "conclusion": conclusion, "at": "2001-12-21T11:00:00Z"}
            sentinel_red = bool(sn.red_workflows([run])[0])
            tab_red = actions.code_of({"status": "completed", "conclusion": conclusion}) == "f"
            payload = {"workflow_runs": [{"name": "CI", "workflow_id": 1, "conclusion": conclusion, "html_url": "u", "head_sha": "abc"}]}
            watch_red = any(r.conclusion in ci_watch.RED for r in ci_watch.latest_runs(Api(payload), "o", inv.Repo("r", "main", "armor")))
            self.assertEqual((sentinel_red, tab_red, watch_red), (ci_rules.is_red(conclusion),) * 3, conclusion)

    def test_an_unapproved_run_is_red_and_a_dynamic_failure_is_not(self):
        self.assertEqual([r["wf"] for r in sn.red_workflows([{"path": ".github/workflows/ci.yml", "conclusion": "action_required", "at": "2001-12-21T11:00:00Z"}])[0]], ["ci.yml"])
        dynamic = {"path": ".github/workflows/ci.yml", "event": "dynamic", "conclusion": "failure", "at": "2001-12-21T11:00:00Z"}
        self.assertEqual(sn.red_workflows([dynamic]), ([], 0))
        payload = {"workflow_runs": [{"name": "Updates", "workflow_id": 9, "event": "dynamic", "conclusion": "failure", "html_url": "u", "head_sha": "abc"}]}
        self.assertEqual(ci_watch.latest_runs(Api(payload), "o", inv.Repo("r", "main", "armor")), [])

    def test_the_slimmed_runs_keep_the_event(self):
        slim = sn._slim_runs({"workflow_runs": [{"path": "p", "conclusion": "failure", "event": "dynamic", "updated_at": "2001-12-21T11:00:00Z"}]})
        self.assertEqual(slim[0]["event"], "dynamic")


if __name__ == "__main__":
    unittest.main()
