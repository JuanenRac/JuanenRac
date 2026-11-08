# =============================================================================
# JuanenRac profile - tests/test_red_rule_parity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""One rule of "red on the default branch" in every place that applies it, checked on the same cases.

The cases live in tests/fixtures/red_rule_cases.json. The rule of scripts/ci_rules.py, the Sentinel tab, the CI watch issue and (when a copy of the local monitor is
next to this repository, or MONITOR_REDRULE points at its redrule.py) the monitor must call the same workflows red, with the same streak.
"""
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import ci_rules  # noqa: E402
import ci_watch  # noqa: E402
import dashboard_sentinel as sn  # noqa: E402
import ecosystem_inventory as inv  # noqa: E402

CASES = json.loads((ROOT / "tests" / "fixtures" / "red_rule_cases.json").read_text(encoding="utf-8"))["cases"]
SAMPLE = json.loads((ROOT / "tests" / "fixtures" / "ci_red_sample.json").read_text(encoding="utf-8"))


def monitor_rule():
    """The redrule.py of the local monitor, or None when it is not there (the CI of this repository has no copy of it)."""
    candidates = [os.environ.get("MONITOR_REDRULE", ""), str(ROOT.parent / "TOOLS-GITHUB-ACTIONS-MONITOR" / "monitor" / "redrule.py")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            spec = importlib.util.spec_from_file_location("monitor_redrule", candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None


class Api:
    def __init__(self, payload):
        self.payload = payload

    def get(self, path):
        return self.payload


def expected(case):
    return [(row["workflow"], row["conclusion"], row["streak"]) for row in case["red"]]


class SharedRuleTests(unittest.TestCase):
    def test_every_case_is_decided_by_the_single_rule(self):
        for case in CASES:
            with self.subTest(case["name"]):
                found = ci_rules.red_workflows(case["runs"], case["default_branch"])
                self.assertEqual([(r["workflow"], r["conclusion"], r["streak"]) for r in found], expected(case))

    def test_the_sentinel_tab_agrees(self):
        for case in CASES:
            with self.subTest(case["name"]):
                finished = [{"path": r["path"], "conclusion": r["conclusion"], "event": r["event"], "at": r["started"]}
                            for r in case["runs"] if r["status"] == "completed" and r["branch"] == case["default_branch"]]
                red, _checked = sn.red_workflows(finished)
                self.assertEqual([(r["wf"], r["streak"]) for r in red], [(w, s) for w, _c, s in expected(case)])

    def test_the_ci_watch_issue_agrees(self):
        for case in CASES:
            with self.subTest(case["name"]):
                # the API lists the newest run first
                runs = [r for r in reversed(case["runs"]) if r["status"] == "completed" and r["branch"] == case["default_branch"]]
                payload = {"workflow_runs": [{"name": r["name"], "workflow_id": r["name"], "path": r["path"], "event": r["event"], "conclusion": r["conclusion"],
                                              "html_url": r["url"], "head_sha": r["sha"]} for r in runs]}
                found = ci_watch.latest_runs(Api(payload), "owner", inv.Repo("repo", case["default_branch"], "armor"))
                red = sorted(run.workflow for run in found if run.conclusion in ci_watch.RED)
                self.assertEqual(red, sorted(w for w, _c, _s in expected(case)))

    def test_the_monitor_agrees(self):
        rule = monitor_rule()
        if rule is None:
            self.skipTest("no copy of the monitor next to this repository")
        for case in CASES:
            if case["skip_monitor"]:
                continue
            with self.subTest(case["name"]):
                runs = [{"name": r["name"], "path": r["path"], "status": r["status"], "branch": r["branch"], "conclusion": r["conclusion"],
                         "started": r["started"], "url": r["url"], "sha": r["sha"]} for r in case["runs"]]
                rows, _approx = rule.red_workflows({"repo": runs}, {"repo": case["default_branch"]})
                self.assertEqual([(r["workflow"], r["conclusion"], r["streak"]) for r in rows], expected(case))

    def test_the_conclusions_are_the_same_as_the_monitor(self):
        rule = monitor_rule()
        if rule is None:
            self.skipTest("no copy of the monitor next to this repository")
        self.assertEqual(set(rule.BAD), set(ci_rules.RED_CONCLUSIONS))
        self.assertEqual(set(rule.IGNORED), set(ci_rules.IGNORED_CONCLUSIONS))

    def test_the_cases_cover_the_rule(self):
        names = {case["name"] for case in CASES}
        for wanted in ("cancelled_does_not_hide_a_failure", "dynamic_runs_are_not_builds", "other_branches_do_not_count", "recovered_is_green", "action_required_is_red"):
            self.assertIn(wanted, names)
        for conclusion in ci_rules.RED_CONCLUSIONS:
            if conclusion != "failure":
                self.assertIn(f"{conclusion}_is_red", names)
        for conclusion in ci_rules.IGNORED_CONCLUSIONS:
            self.assertIn(f"{conclusion}_does_not_hide_a_failure", names)


class CiRedContractTests(unittest.TestCase):
    """The dashboard does not read ci_red.json (the monitor is local and never publishes it); both sides test their samples against the same contract."""

    def test_the_sample_conforms(self):
        self.assertEqual(ci_rules.ci_red_problems(SAMPLE), [])

    def test_a_broken_document_is_described(self):
        broken = json.loads(json.dumps(SAMPLE))
        broken["schema"] = 1
        del broken["complete"]
        broken["repos"]["EXAMPLE-REPO"]["red"][0].pop("streak")
        broken["red_repos"] = 5
        text = " | ".join(ci_rules.ci_red_problems(broken))
        for part in ("missing field: complete", "schema is 1", "streak", "red_repos is 5"):
            self.assertIn(part, text)
        self.assertEqual(ci_rules.ci_red_problems([]), ["the document is not an object"])

    def test_a_new_field_does_not_break_a_consumer(self):
        newer = json.loads(json.dumps(SAMPLE))
        newer["something_added_later"] = {"x": 1}
        newer["repos"]["OTHER-REPO"]["extra"] = True
        self.assertEqual(ci_rules.ci_red_problems(newer), [])

    def test_the_sample_of_the_monitor_schema_has_the_same_required_fields(self):
        schema = ROOT.parent / "TOOLS-GITHUB-ACTIONS-MONITOR" / "monitor" / "docs" / "schemas" / "ci_red.schema.json"
        if not schema.is_file():
            self.skipTest("no copy of the monitor next to this repository")
        required = set(json.loads(schema.read_text(encoding="utf-8")).get("required", []))
        self.assertTrue(required <= set(ci_rules.CI_RED_REQUIRED) | {"pending_sign_repos", "pending_sign_hours_threshold"}, required)


if __name__ == "__main__":
    unittest.main()
