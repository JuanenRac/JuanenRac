# =============================================================================
# JuanenRac profile - tests/test_dashboard_perf.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Speed (p50 / p95), queue and flaky runs of the Builds tab: the definitions, the figures per repository and for the account, and the same definitions as the monitor."""
import importlib.util
import os
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_actions as ac  # noqa: E402
import dashboard_actions_ui as ui  # noqa: E402
import dashboard_cover_texts as texts  # noqa: E402

NOW = datetime(2001, 12, 21, 12, 0, tzinfo=timezone.utc)
CONFIG = ac.check_config(None)[0]


def stamp(minutes_ago):
    return (NOW - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(workflow, conclusion, ago, seconds=60, wait=5, sha="a1", attempt=1, status="completed"):
    """A run that ended `ago` minutes ago, took `seconds`, waited `wait` seconds in the queue."""
    end = NOW - timedelta(minutes=ago)
    start = end - timedelta(seconds=seconds)
    created = start - timedelta(seconds=wait)
    return {"path": f".github/workflows/{workflow}", "name": workflow, "status": status, "conclusion": conclusion, "head_sha": sha, "run_attempt": attempt,
            "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"), "run_started_at": start.strftime("%Y-%m-%dT%H:%M:%SZ"), "updated_at": end.strftime("%Y-%m-%dT%H:%M:%SZ")}


class PercentileTests(unittest.TestCase):
    def test_nearest_rank(self):
        values = list(range(1, 101))
        self.assertEqual((ac.percentile(values, 50), ac.percentile(values, 95), ac.percentile(values, 100)), (50, 95, 100))
        self.assertEqual(ac.percentile([7], 95), 7)
        self.assertIsNone(ac.percentile([], 50))
        self.assertIsNone(ac.percentile([None, "x", True], 50))


class RepositoryFiguresTests(unittest.TestCase):
    def test_durations_and_waits_of_the_successful_runs(self):
        runs = [run("ci.yml", "success", 10 + i * 5, seconds=60 * (i + 1), wait=2 * (i + 1), sha=f"s{i}") for i in range(5)]
        record = ac.summarize(runs, NOW, CONFIG)
        self.assertEqual(record["pd"], [60, 120, 180, 240, 300])
        self.assertEqual(record["pq"], [2, 4, 6, 8, 10])
        row = record["pw"][0]
        self.assertEqual(row[:5], ["ci.yml", 5, 180, 300, 6])
        self.assertEqual((row[5], row[6], row[7]), (10, 0, 5))

    def test_only_successful_runs_set_the_duration_but_every_finished_run_waited(self):
        runs = [run("ci.yml", "success", 10, seconds=100, sha="a"), run("ci.yml", "failure", 20, seconds=5, sha="b"), run("ci.yml", "cancelled", 30, seconds=1, sha="c"),
                run("ci.yml", None, 5, status="in_progress", sha="d")]
        record = ac.summarize(runs, NOW, CONFIG)
        self.assertEqual(record["pd"], [100])
        self.assertEqual(len(record["pq"]), 3)

    def test_a_rerun_is_not_counted_in_the_queue(self):
        record = ac.summarize([run("ci.yml", "success", 10, wait=7200, attempt=2)], NOW, CONFIG)
        self.assertEqual(record["pq"], [])

    def test_flaky_is_a_failure_followed_by_a_pass_on_the_same_commit_or_a_retry_that_passed(self):
        runs = [run("ci.yml", "failure", 60, sha="x"), run("ci.yml", "success", 50, sha="x"),            # failed, then passed on the same commit: flaky
                run("ci.yml", "success", 40, sha="y", attempt=2),                                          # needed a re-run: flaky
                run("ci.yml", "failure", 30, sha="z"), run("ci.yml", "success", 20, sha="w"),              # failed on one commit, fixed on the next: not flaky
                run("ci.yml", "success", 10, sha="v")]
        row = ac.summarize(runs, NOW, CONFIG)["pw"][0]
        self.assertEqual((row[6], row[7]), (2, 6))

    def test_a_pass_followed_by_a_failure_on_the_same_commit_is_not_flaky(self):
        runs = [run("ci.yml", "success", 60, sha="x"), run("ci.yml", "failure", 50, sha="x"), run("ci.yml", "success", 40, sha="p"), run("ci.yml", "success", 30, sha="q")]
        self.assertEqual(ac.summarize(runs, NOW, CONFIG)["pw"][0][6], 0)

    def test_a_workflow_with_too_few_runs_is_left_out_unless_it_is_flaky(self):
        few = [run("a.yml", "success", 10, sha="1"), run("a.yml", "success", 20, sha="2")]
        self.assertEqual(ac.summarize(few, NOW, CONFIG)["pw"], [])
        flaky = [run("b.yml", "failure", 30, sha="x"), run("b.yml", "success", 20, sha="x"), run("b.yml", "success", 10, sha="y")]
        rows = ac.summarize(few + flaky, NOW, CONFIG)["pw"]
        self.assertEqual([r[0] for r in rows], ["b.yml"])

    def test_the_workflows_are_the_slowest_first_and_capped_and_the_samples_too(self):
        config = ac.check_config({"perf": {"workflows_max": 2, "samples_max": 10, "min_samples": 1}})[0]
        runs = [run(f"w{i}.yml", "success", 10 + i, seconds=100 * (i + 1), sha=f"s{i}") for i in range(4)]
        record = ac.summarize(runs, NOW, config)
        self.assertEqual([r[0] for r in record["pw"]], ["w3.yml", "w2.yml"])
        many = [run("ci.yml", "success", 10 + i, sha=f"m{i}") for i in range(30)]
        self.assertEqual(len(ac.summarize(many, NOW, config)["pd"]), 10)

    def test_runs_older_than_a_week_do_not_count(self):
        record = ac.summarize([run("ci.yml", "success", 60 * 24 * 8, sha="old")], NOW, CONFIG)
        self.assertEqual((record["pd"], record["pw"]), ([], []))


class AccountFiguresTests(unittest.TestCase):
    def repos(self):
        a = ac.summarize([run("ci.yml", "success", 10 + i, seconds=60 * (i + 1), wait=i + 1, sha=f"s{i}") for i in range(6)], NOW, CONFIG)
        b = ac.summarize([run("deploy.yml", "failure", 90, sha="x"), run("deploy.yml", "success", 80, sha="x", seconds=600), run("deploy.yml", "success", 70, sha="y", seconds=700),
                          run("deploy.yml", "success", 60, sha="z", seconds=800), run("deploy.yml", "success", 50, sha="w", seconds=900)], NOW, CONFIG)
        return {"A": a, "B": b, "C": {"state": "unread"}, "D": {"state": "none"}}

    def test_percentiles_over_every_read_repository(self):
        block = ac.perf_block(self.repos(), CONFIG)
        self.assertTrue(block["read"])
        self.assertEqual(block["runs"], 10)
        self.assertEqual((block["d50"], block["d95"]), (ac.percentile([60, 120, 180, 240, 300, 360, 600, 700, 800, 900], 50), 900))
        self.assertEqual(block["qn"], 11)
        self.assertEqual(block["slow"][0]["repo"], "B")
        self.assertEqual(block["flaky_workflows"], 1)
        self.assertEqual(block["flaky"][0]["wf"], "deploy.yml")

    def test_a_reading_without_the_figures_says_not_read_and_never_zero(self):
        self.assertEqual(ac.perf_block({"A": {"state": "ok", "n": [1, 0, 0, 0, 0]}}, CONFIG), {"read": False})
        self.assertEqual(ac.perf_block({}, CONFIG), {"read": False})

    def test_the_block_travels_in_the_page_data_and_the_cache_keeps_it(self):
        repos = self.repos()
        page = ac.build({"asof": "2001-12-21T12:00:00Z", "repos": repos, "errors": 0}, None, ["A", "B"], [], "2001-12-21", CONFIG)
        self.assertTrue(page["perf"]["read"])
        old = ac.build({"asof": "2001-12-21T12:00:00Z", "repos": {"A": {"state": "ok", "n": [1, 0, 0, 0, 0], "n7": [1, 0, 0, 0, 0], "min": 1}}, "errors": 0}, None, ["A"], [], "2001-12-21")
        self.assertEqual(old["perf"], {"read": False})

    def test_the_configuration_is_checked(self):
        config, problems = ac.check_config({"perf": {"min_samples": 0, "top": "x", "flaky_min_runs": 5}})
        self.assertEqual(len(problems), 2)
        self.assertEqual((config["perf"]["min_samples"], config["perf"]["flaky_min_runs"]), (3, 5))
        self.assertEqual(ac.check_config({"perf": []})[1], ["actions.perf: not an object"])
        shipped, shipped_problems = ac.load_config()
        self.assertEqual(shipped_problems, [])
        self.assertEqual(shipped["perf"], ac.DEFAULT_CONFIG["perf"])


class TabTests(unittest.TestCase):
    def test_the_card_is_in_the_tab_and_drawn(self):
        html = ui.panel_html()
        for part in ('data-testid="ac-perf"', 'id="ac-perf-kpis"', 'id="ac-perf-slow"', 'id="ac-perf-flaky"', 'id="ac-perf-none"'):
            self.assertIn(part, html)
        self.assertIn("function acPerf", ui.JS)
        self.assertIn("acPerf(dict)", ui.JS)

    def test_the_texts_are_in_the_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        keys = [key for key in texts.TEXTS["en"] if key.startswith("ac_perf_")]
        self.assertGreaterEqual(len(keys), 11)
        for code in ("es", "de", "fr", "ja", "zh"):
            for key in keys:
                self.assertNotEqual(texts.TEXTS[code][key], texts.TEXTS["en"][key], f"{code} {key}")


def monitor_analytics():
    candidates = [os.environ.get("MONITOR_ANALYTICS", ""), str(ROOT.parent / "TOOLS-GITHUB-ACTIONS-MONITOR" / "monitor" / "analytics.py")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            spec = importlib.util.spec_from_file_location("monitor_analytics", candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None


class MonitorParityTests(unittest.TestCase):
    def test_the_percentile_is_the_one_of_the_monitor(self):
        monitor = monitor_analytics()
        if monitor is None:
            self.skipTest("no copy of the monitor next to this repository")
        for values in ([5], [3, 1, 2], list(range(1, 21)), [10, 10, 10, 90], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]):
            for q in (50, 95, 100):
                self.assertEqual(ac.percentile(values, q), monitor.percentile(values, q), (values, q))

    def test_the_flaky_commits_are_the_ones_of_the_monitor(self):
        monitor = monitor_analytics()
        if monitor is None:
            self.skipTest("no copy of the monitor next to this repository")
        scenario = [("failure", 60, "x", 1), ("success", 50, "x", 1), ("success", 40, "y", 2), ("failure", 30, "z", 1), ("success", 20, "w", 1), ("success", 10, "v", 1), ("success", 5, "u", 1)]
        ours = ac.summarize([run("ci.yml", c, a, sha=s, attempt=t) for c, a, s, t in scenario], NOW, CONFIG)["pw"][0]
        theirs_runs = [{"repo": "r", "name": "ci.yml", "status": "completed", "conclusion": c, "sha": s, "attempt": t, "started": stamp(a)} for c, a, s, t in scenario]
        rows = monitor.flaky_rows(theirs_runs, min_runs=3)
        self.assertEqual(rows[0]["flaky"], ours[6])
        self.assertEqual(rows[0]["total"], ours[7])


if __name__ == "__main__":
    unittest.main()
