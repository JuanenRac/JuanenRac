# =============================================================================
# JuanenRac profile - tests/test_dashboard_health.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Thresholds, health alerts, completeness of the picture and the stable stamp of the last good build."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_app as app  # noqa: E402
import dashboard_charts as charts  # noqa: E402
import dashboard_health as health  # noqa: E402


class ConfigTests(unittest.TestCase):
    def test_the_file_of_the_profile_is_valid_and_matches_the_defaults(self):
        config, problems = health.load_config()
        self.assertEqual(problems, [])
        self.assertEqual(config, health.DEFAULT_CONFIG)

    def test_a_wrong_part_falls_back_to_its_default_and_is_named(self):
        config, problems = health.parse_config({"activity_days": {"green_max": 40, "amber_max": 10}, "release_days": {"green_max": 5, "amber_max": 9}, "alert_after_days": "x"})
        self.assertEqual(config["activity_days"], health.DEFAULT_CONFIG["activity_days"])
        self.assertEqual(config["release_days"], {"green_max": 5, "amber_max": 9})
        self.assertEqual(config["alert_after_days"], 30)
        self.assertEqual(len(problems), 2)

    def test_booleans_negative_and_huge_numbers_are_rejected(self):
        for bad in ({"green_max": True, "amber_max": 3}, {"green_max": -1, "amber_max": 3}, {"green_max": 1, "amber_max": 99999}, "text", None):
            self.assertIsNone(health._ordered(bad, health.DEFAULT_CONFIG["activity_days"]))

    def test_missing_or_broken_file_gives_the_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, problems = health.load_config(Path(tmp) / "none.json")
            self.assertEqual(config, health.DEFAULT_CONFIG)
            self.assertEqual(len(problems), 1)
            broken = Path(tmp) / "broken.json"
            broken.write_text("{", encoding="utf-8")
            self.assertEqual(health.load_config(broken)[0], health.DEFAULT_CONFIG)
            self.assertEqual(health.load_config(broken)[1][0].split(":")[0], "broken.json")

    def test_the_defaults_are_not_shared_between_calls(self):
        a, _ = health.parse_config({})
        a["activity_days"]["green_max"] = 1
        self.assertEqual(health.DEFAULT_CONFIG["activity_days"]["green_max"], 14)


class DaysTests(unittest.TestCase):
    def test_classify_edges(self):
        self.assertEqual(health.classify(14, 14, 30), "good")
        self.assertEqual(health.classify(15, 14, 30), "warn")
        self.assertEqual(health.classify(30, 14, 30), "warn")
        self.assertEqual(health.classify(31, 14, 30), "bad")
        self.assertEqual(health.classify(None, 14, 30), "unknown")

    def test_days_between_counts_whole_days_and_rejects_nonsense(self):
        self.assertEqual(health.days_between("2001-12-01T10:00:00Z", "2001-12-21T09:00:00Z"), 19)
        self.assertEqual(health.days_between("2001-12-01", "2001-12-01"), 0)
        self.assertEqual(health.days_between("2001-12-21", "2001-12-01"), 0)
        self.assertIsNone(health.days_between(None, "2001-12-01"))
        self.assertIsNone(health.days_between("2001-13-45", "2001-12-01"))

    def test_last_activity_is_the_newer_of_commit_and_release(self):
        self.assertEqual(health.last_activity("2001-02-01T00:00:00Z", "2001-03-01T00:00:00Z"), "2001-03-01T00:00:00Z")
        self.assertEqual(health.last_activity(None, "2001-03-01T00:00:00Z"), "2001-03-01T00:00:00Z")
        self.assertIsNone(health.last_activity(None, None))


def _issue(kind, repo, detail="d"):
    return SimpleNamespace(kind=kind, repo=repo, detail=detail)


class AlertTests(unittest.TestCase):
    def test_red_ci_manifest_and_version_alerts_have_repo_reason_and_link(self):
        activity = {"A-1": charts.Activity(ci="failure"), "A-2": charts.Activity(ci="success"), "ghost": charts.Activity(ci="failure")}
        alerts = health.static_alerts(activity=activity, ecosystem_by_name={"A-1": "armor", "A-2": "armor"},
                                      issues=[_issue("invalid_manifest", "B-1", "bad json"), _issue("api", "listing"), _issue("unknown_maturity", "A-2", "maturity missing")],
                                      unresolved=[("A-3", "HTTP 404")])
        self.assertEqual([(a.kind, a.repo) for a in alerts], [("ci", "A-1"), ("manifest", "B-1"), ("manifest", "A-2"), ("version", "A-3")])
        self.assertTrue(all(a.url.startswith("https://github.com/JuanenRac/") for a in alerts))
        self.assertEqual(alerts[0].url, "https://github.com/JuanenRac/A-1/actions")
        self.assertEqual(alerts[3].detail, "HTTP 404")

    def test_no_alerts_when_everything_is_fine(self):
        self.assertEqual(health.static_alerts(activity={"A": charts.Activity(ci="success")}, ecosystem_by_name={"A": "armor"}, issues=[], unresolved=[]), [])

    def test_completeness_reasons(self):
        listed = {"A": "armor", "B": "urtc"}
        full = {"A": charts.Activity(), "B": charts.Activity()}
        self.assertEqual(health.completeness(total=2, activity=full, ecosystem_by_name=listed, issues=[]), [])
        self.assertEqual(health.completeness(total=2, activity={}, ecosystem_by_name=listed, issues=[]), ["activity_unread"])
        self.assertEqual(health.completeness(total=2, activity={"A": charts.Activity()}, ecosystem_by_name=listed, issues=[]), ["activity_partial"])
        self.assertEqual(health.completeness(total=2, activity=full, ecosystem_by_name=listed, issues=[_issue("api", "x")]), ["api"])
        self.assertEqual(health.completeness(total=0, activity={}, ecosystem_by_name={}, issues=[]), ["nothing_listed", "activity_unread"])


class AlertCardTests(unittest.TestCase):
    def data(self, **kw):
        base = dict(total=2, ok=2, errors=0, success_percent_text="100%", ecosystem_by_name={}, maturity_labels={}, evidence_labels={}, status={}, progress={}, maturity={}, evidence={}, activity={})
        base.update(kw)
        return app.AppData(**base)

    def test_ok_state_says_no_alerts(self):
        html = app.alerts_card(self.data())
        self.assertIn('data-state="ok"', html)
        self.assertIn('data-i18n="alerts_none"', html)
        self.assertNotIn("alerts_incomplete", html)

    def test_incomplete_is_never_ok_even_without_alerts(self):
        html = app.alerts_card(self.data(incomplete=["activity_unread"]))
        self.assertIn('data-state="incomplete"', html)
        self.assertIn('data-i18n="alerts_incomplete"', html)
        self.assertIn("alerts_why_activity_unread", html)
        self.assertNotIn("alerts_none", html)

    def test_incomplete_with_alerts_counts_them(self):
        alert = health.Alert("ci", "A-1", "", "https://github.com/JuanenRac/A-1/actions")
        html = app.alerts_card(self.data(alerts=[alert], incomplete=["api"]))
        self.assertIn('data-i18n-template="alerts_incomplete_some" data-n="1"', html)
        self.assertIn('href="https://github.com/JuanenRac/A-1/actions"', html)
        self.assertIn('data-static="1"', html)

    def test_alert_text_is_escaped(self):
        alert = health.Alert("manifest", "A<b>", "<script>x</script>", "https://github.com/JuanenRac/A")
        html = app.alerts_card(self.data(alerts=[alert]))
        self.assertNotIn("<script>x", html)
        self.assertIn("&lt;script&gt;x", html)


class BuildStampTests(unittest.TestCase):
    def test_known_build_has_time_and_link_and_unknown_says_not_verified(self):
        known = app.build_stamp(health.BuildInfo("https://github.com/JuanenRac/JuanenRac/actions/runs/5", "2001-12-20T08:30:11Z"))
        self.assertIn('datetime="2001-12-20T08:30:11Z"', known)
        self.assertIn("2001-12-20 08:30 UTC", known)
        self.assertIn('href="https://github.com/JuanenRac/JuanenRac/actions/runs/5"', known)
        unknown = app.build_stamp(None)
        self.assertIn('data-state="unknown"', unknown)
        self.assertIn("not_verified", unknown)

    def test_fetch_accepts_only_a_github_run(self):
        good = {"workflow_runs": [{"html_url": "https://github.com/JuanenRac/JuanenRac/actions/runs/9", "updated_at": "2001-12-20T08:30:00Z"}]}
        self.assertEqual(health.fetch_last_good_build("o/r", "w.yml", lambda url: good), health.BuildInfo("https://github.com/JuanenRac/JuanenRac/actions/runs/9", "2001-12-20T08:30:00Z"))
        for bad in (None, {}, {"workflow_runs": []}, {"workflow_runs": [{"html_url": "https://evil.example/x", "updated_at": "2001-12-20T08:30:00Z"}]},
                    {"workflow_runs": [{"html_url": "https://github.com/a", "updated_at": "yesterday"}]}, [], "x"):
            self.assertIsNone(health.fetch_last_good_build("o/r", "w.yml", lambda url, b=bad: b))

    def test_fetch_asks_for_the_successful_runs_of_main(self):
        seen = []
        health.fetch_last_good_build("JuanenRac/JuanenRac", "build-dashboard.yml", lambda url: seen.append(url))
        self.assertIn("/actions/workflows/build-dashboard.yml/runs?status=success&branch=main&per_page=1", seen[0])


class MergeBuildInfoTests(unittest.TestCase):
    def page(self, stamp, body="body"):
        return f"<main>{body}{health.BUILD_BEGIN}{stamp}{health.BUILD_END}</main>"

    def test_same_page_keeps_the_published_one_even_if_the_time_moved(self):
        old = self.page('<span data-state="known">t1</span>')
        new = self.page('<span data-state="known">t2</span>')
        self.assertEqual(health.merge_build_info(new, old), old)

    def test_a_real_change_writes_the_new_page_with_its_time(self):
        old = self.page('<span data-state="known">t1</span>', "a")
        new = self.page('<span data-state="known">t2</span>', "b")
        self.assertEqual(health.merge_build_info(new, old), new)

    def test_an_unread_build_keeps_the_old_stamp_in_a_changed_page(self):
        old = self.page('<span data-state="known">t1</span>', "a")
        new = self.page('<span data-state="unknown">?</span>', "b")
        merged = health.merge_build_info(new, old)
        self.assertIn(">t1<", merged)
        self.assertIn("b", merged)
        self.assertNotIn('data-state="unknown"', merged)

    def test_no_published_page_and_unknown_stays_unknown(self):
        new = self.page('<span data-state="unknown">?</span>')
        self.assertEqual(health.merge_build_info(new, None), new)
        self.assertEqual(health.merge_build_info(new, self.page('<span data-state="unknown">?</span>')), new)


if __name__ == "__main__":
    unittest.main()
