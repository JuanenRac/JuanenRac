# =============================================================================
# JuanenRac profile - tests/test_dashboard_actions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The builds (GitHub Actions runs): how they are summarized, what is kept (state and numbers only), what is never invented and how the page falls back."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_actions as ac  # noqa: E402
import dashboard_actions_texts as texts  # noqa: E402
import dashboard_evo as evo  # noqa: E402

NOW = datetime(2001, 12, 21, 12, 0, 0, tzinfo=timezone.utc)
CONFIG = ac.check_config(None)[0]


def run(minutes_ago_end, seconds=120, conclusion="success", status="completed", path=".github/workflows/ci.yml"):
    end = NOW - timedelta(minutes=minutes_ago_end)
    start = end - timedelta(seconds=seconds)
    return {"status": status, "conclusion": conclusion, "created_at": start.isoformat(), "run_started_at": start.isoformat(), "updated_at": end.isoformat(), "path": path,
            # the fields that must never be kept
            "actor": {"login": "someone"}, "head_branch": "secret-branch", "display_title": "a commit title", "head_commit": {"message": "a commit message"}}


class SummarizeTests(unittest.TestCase):
    def test_results_are_counted_by_window(self):
        runs = [run(10), run(50, conclusion="failure"), run(100, conclusion="cancelled"), run(200, conclusion="skipped"), run(3000), run(12000), run(5, status="in_progress", conclusion=None)]
        record = ac.summarize(runs, NOW, CONFIG)
        self.assertEqual(record["n"], [1, 1, 1, 1, 1])             # success, failure, cancelled, other, running in 24 h
        self.assertEqual(record["n7"], [2, 1, 1, 1, 1])             # the run of 3000 minutes is inside 7 days, the one of 12000 is not (10080 is the limit)
        self.assertEqual(record["running"], 1)

    def test_the_last_finished_run_and_the_last_success(self):
        record = ac.summarize([run(30, conclusion="failure", seconds=95), run(400), run(20, status="in_progress", conclusion=None)], NOW, CONFIG)
        self.assertEqual(record["last"], [30, "f", 95])
        self.assertEqual(record["lastOk"], 400)

    def test_a_repository_without_a_success_in_the_window_has_no_last_success(self):
        record = ac.summarize([run(30, conclusion="failure")], NOW, CONFIG)
        self.assertIsNone(record["lastOk"])

    def test_the_minutes_are_wall_clock_of_finished_runs_in_24_hours(self):
        record = ac.summarize([run(10, seconds=600), run(20, seconds=1200), run(30, seconds=300, status="in_progress", conclusion=None), run(3000, seconds=6000)], NOW, CONFIG)
        self.assertEqual(record["min"], 30)
        self.assertEqual(record["min7"], 130)

    def test_nothing_about_who_or_what_is_kept(self):
        record = ac.summarize([run(10), run(20, conclusion="failure")], NOW, CONFIG)
        text = json.dumps(record)
        for forbidden in ("someone", "secret-branch", "commit title", "commit message", "actor", "branch", "title", "message", "ci.yml"):
            self.assertNotIn(forbidden, text)

    def test_the_timeline_and_the_durations_are_capped_and_ordered(self):
        runs = [run(i * 5 + 1, seconds=10 + i) for i in range(60)]
        record = ac.summarize(runs, NOW, {**CONFIG, "timeline_max": 10, "durations_max": 4})
        self.assertEqual(len(record["tl"]), 10)
        self.assertEqual([age for age, _ in record["tl"]], sorted(age for age, _ in record["tl"]))
        self.assertEqual(len(record["dur"]), 4)
        self.assertEqual(record["dur"], sorted(record["dur"], reverse=True))        # oldest first: the shortest were the newest runs

    def test_ignored_workflows_are_left_out(self):
        record = ac.summarize([run(10, path=".github/workflows/build-dashboard.yml"), run(20)], NOW, CONFIG, [".github/workflows/build-dashboard.yml"])
        self.assertEqual(sum(record["n"]), 1)

    def test_timeouts_and_startup_failures_are_failures(self):
        for conclusion in ("timed_out", "startup_failure", "failure"):
            self.assertEqual(ac.code_of({"status": "completed", "conclusion": conclusion}), "f")
        self.assertEqual(ac.code_of({"status": "queued"}), "p")
        self.assertEqual(ac.code_of({"status": "completed", "conclusion": "neutral"}), "k")

    def test_a_broken_run_is_skipped_not_fatal(self):
        record = ac.summarize([None, "x", {"status": "completed"}, run(10)], NOW, CONFIG)
        self.assertEqual(sum(record["n"]), 1)

    def test_a_full_page_is_flagged_as_possibly_truncated(self):
        self.assertTrue(ac.summarize([run(i + 1) for i in range(100)], NOW, CONFIG)["truncated"])
        self.assertFalse(ac.summarize([run(i + 1) for i in range(5)], NOW, CONFIG)["truncated"])


def fake_post(nodes, ok=True):
    def post(body, headers):
        if not ok:
            return None
        return {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": nodes}}}}
    return post


def node(name, workflows=True, bf=0, bs=0):
    return {"name": name, "workflows": {"entries": [{"name": "ci.yml"}]} if workflows else None, "bf": {"totalCount": bf}, "bs": {"totalCount": bs}}


class ReadTests(unittest.TestCase):
    def setUp(self):
        self.urls = []

    def get(self, failing=()):
        def run_get(url):
            self.urls.append(url)
            repo = url.split("/repos/JuanenRac/")[1].split("/")[0]
            if repo in failing:
                return "error", "HTTP 502"
            return "ok", {"workflow_runs": [run(10), run(20, conclusion="failure")]}
        return run_get

    def test_the_four_states(self):
        nodes = [node("A", bf=2, bs=1), node("B", workflows=False, bf=1), node("C")]
        read = ac.read_all("JuanenRac", ["A", "B", "C", "D"], "token", CONFIG, NOW, fake_post(nodes), self.get(failing=("C",)))
        self.assertEqual(read["repos"]["A"]["state"], "ok")
        self.assertEqual((read["repos"]["A"]["bf"], read["repos"]["A"]["bs"]), (2, 1))
        self.assertEqual(read["repos"]["B"], {"state": "none", "bf": 1, "bs": 0})
        self.assertEqual(read["repos"]["C"]["state"], "unread")      # the lookup failed: never green
        self.assertEqual(read["repos"]["D"], {"state": "unread"})    # not listed by GitHub
        self.assertEqual(read["errors"], 2)
        self.assertEqual(read["asof"], "2001-12-21T12:00:00Z")

    def test_one_request_per_repository_with_workflows_and_none_for_the_rest(self):
        ac.read_all("JuanenRac", ["A", "B", "C"], "token", CONFIG, NOW, fake_post([node("A"), node("B", workflows=False), node("C")]), self.get())
        self.assertEqual(len(self.urls), 2)
        self.assertTrue(all("per_page=100" in url and "created=%3E%3D2001-12-14T12%3A00%3A00Z" in url for url in self.urls))

    def test_no_token_or_no_answer_reads_nothing(self):
        self.assertIsNone(ac.read_all("JuanenRac", ["A"], "", CONFIG, NOW, fake_post([node("A")]), self.get()))
        self.assertIsNone(ac.read_all("JuanenRac", ["A"], "token", CONFIG, NOW, fake_post([], ok=False), self.get()))
        self.assertEqual(self.urls, [])

    def test_an_answer_without_runs_is_unread_not_green(self):
        read = ac.read_all("JuanenRac", ["A"], "token", CONFIG, NOW, fake_post([node("A")]), lambda url: ("ok", {"message": "odd"}))
        self.assertEqual(read["repos"]["A"]["state"], "unread")

    def test_the_labels_come_from_the_configuration(self):
        seen = {}

        def post(body, headers):
            seen.update(json.loads(body)["variables"])
            return fake_post([])(body, headers)
        ac.read_all("JuanenRac", [], "token", {**CONFIG, "labels": {"failed": "x-failed", "stuck": "x-stuck"}}, NOW, post, self.get())
        self.assertEqual((seen["failed"], seen["stuck"]), (["x-failed"], ["x-stuck"]))


class CacheAndBuildTests(unittest.TestCase):
    def read(self, states=("ok", "ok", "unread")):
        repos = {}
        for name, state in zip("ABC", states):
            repos[name] = ac.summarize([run(10), run(40, conclusion="failure")], NOW, CONFIG) if state == "ok" else {"state": state}
            repos[name].update({"bf": 0, "bs": 0}) if state == "ok" else None
        return {"asof": "2001-12-21T12:00:00Z", "repos": repos, "errors": states.count("unread")}

    def test_the_cache_round_trips_and_is_only_written_when_something_was_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data" / "actions-cache.json"
            self.assertTrue(ac.save_cache(path, self.read()))
            self.assertFalse(ac.save_cache(path, self.read()))             # same content: not written again
            self.assertEqual(ac.load_cache(path)["repos"]["A"]["state"], "ok")
            self.assertFalse(ac.save_cache(path, self.read(("unread", "none", "unread"))))
            self.assertFalse(ac.save_cache(path, None))

    def test_a_damaged_cache_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.json"
            for text in ("not json", "[]", json.dumps({"schema": 9, "asof": "2001-12-21T12:00:00Z", "repos": {}}), json.dumps({"schema": 1, "asof": "yesterday", "repos": {}})):
                path.write_text(text, encoding="utf-8")
                self.assertIsNone(ac.load_cache(path))
            self.assertIsNone(ac.load_cache(Path(tmp) / "missing.json"))

    def test_the_block_of_a_fresh_read(self):
        block = ac.build(self.read(), None, "ABC", [], "2001-12-21")
        self.assertTrue(block["read"])
        self.assertIsNone(block["stale"])
        self.assertEqual(block["problems"], 1)
        today = block["daily"][-1]
        self.assertEqual((today["date"], today["runs"], today["ok"], today["fail"], today["other"]), ("2001-12-21", 4, 2, 2, 0))

    def test_without_a_read_the_last_known_one_is_shown_with_its_date(self):
        block = ac.build(None, self.read(), "ABC", [], "2001-12-22")
        self.assertTrue(block["read"])
        self.assertEqual(block["stale"], "2001-12-21T12:00:00Z")
        self.assertEqual(block["asof"], "2001-12-21T12:00:00Z")
        self.assertNotIn("2001-12-22", [d["date"] for d in block["daily"]])      # a day that was not read is not invented

    def test_without_a_read_and_without_a_cache_everything_is_not_verified(self):
        block = ac.build(None, None, "ABC", [], "2001-12-21")
        self.assertFalse(block["read"])
        self.assertEqual({r["state"] for r in block["repos"].values()}, {"unread"})
        self.assertEqual(block["daily"], [])

    def test_a_repository_that_is_not_in_the_read_is_not_verified(self):
        block = ac.build(self.read(), None, "ABCZ", [], "2001-12-21")
        self.assertEqual(block["repos"]["Z"], {"state": "unread"})

    def test_the_daily_history_comes_from_earlier_snapshots(self):
        history = [{"date": "2001-12-19", "actions": {"runs": 10, "ok": 8, "fail": 1, "other": 1, "min": 30}}, {"date": "2001-12-20"}, {"date": "2001-12-21", "actions": {"runs": 99, "ok": 99, "fail": 0, "other": 0, "min": 1}}]
        block = ac.build(self.read(), None, "ABC", history, "2001-12-21")
        self.assertEqual([d["date"] for d in block["daily"]], ["2001-12-19", "2001-12-21"])
        self.assertEqual(block["daily"][0]["runs"], 10)
        self.assertEqual(block["daily"][1]["runs"], 4)                  # today is the fresh read, not the old entry of the same day

    def test_day_summary(self):
        self.assertEqual(ac.day_summary(self.read())["runs"], 4)
        self.assertIsNone(ac.day_summary(None))
        self.assertIsNone(ac.day_summary(self.read(("unread", "none", "unread"))))


class StabilizeTests(unittest.TestCase):
    def read(self, now, extra=0, bf=0):
        record = ac.summarize([run(10), run(40, conclusion="failure")] + [run(50 + i) for i in range(extra)], now, CONFIG)
        record.update({"bf": bf, "bs": 0})
        return {"asof": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": {"A": record, "B": {"state": "none", "bf": 0, "bs": 0}}, "errors": 0}

    def test_nothing_new_keeps_the_saved_reading_and_so_the_page(self):
        old = self.read(NOW)
        kept = ac.stabilize(self.read(NOW + timedelta(minutes=30)), old)
        self.assertEqual(kept, old)

    def test_a_new_run_a_new_issue_or_an_old_cache_give_the_fresh_reading(self):
        old = self.read(NOW)
        for fresh in (self.read(NOW + timedelta(minutes=30), extra=1), self.read(NOW + timedelta(minutes=30), bf=1), self.read(NOW + timedelta(hours=7))):
            self.assertIs(ac.stabilize(fresh, old), fresh)

    def test_no_cache_or_no_read(self):
        fresh = self.read(NOW)
        self.assertIs(ac.stabilize(fresh, None), fresh)
        self.assertIsNone(ac.stabilize(None, fresh))

    def test_a_different_set_of_repositories_gives_the_fresh_reading(self):
        old = self.read(NOW)
        fresh = self.read(NOW + timedelta(minutes=30))
        fresh["repos"]["C"] = {"state": "unread"}
        self.assertIs(ac.stabilize(fresh, old), fresh)


class ConfigTests(unittest.TestCase):
    def test_defaults(self):
        config, problems = ac.check_config(None)
        self.assertEqual(problems, [])
        self.assertEqual(config["labels"], {"failed": "build-failed", "stuck": "build-stuck"})

    def test_a_bad_part_is_replaced_and_reported(self):
        config, problems = ac.check_config({"labels": {"failed": ""}, "timeline_max": 9999, "ignore_paths": "x"})
        self.assertEqual(len(problems), 3)
        self.assertEqual(config["timeline_max"], 40)

    def test_the_real_config_file_is_valid(self):
        config, problems = ac.load_config()
        self.assertEqual(problems, [])
        self.assertIn("build-dashboard.yml", " ".join(config["ignore_paths"].get("JuanenRac", [])))

    def test_not_an_object(self):
        self.assertEqual(len(ac.check_config([1])[1]), 1)


class SnapshotAndTextsTests(unittest.TestCase):
    def test_the_snapshot_keeps_the_compact_summary_only_when_it_is_valid(self):
        progress = {"armor": (50, 100)}
        entry = evo.snapshot("2001-12-21", progress, {}, ["armor"], actions={"runs": 4, "ok": 2, "fail": 2, "other": 0, "min": 8})
        self.assertEqual(entry["actions"], {"runs": 4, "ok": 2, "fail": 2, "other": 0, "min": 8})
        self.assertNotIn("actions", evo.snapshot("2001-12-21", progress, {}, ["armor"]))
        self.assertNotIn("actions", evo.snapshot("2001-12-21", progress, {}, ["armor"], actions={"runs": -1, "ok": 0, "fail": 0, "other": 0, "min": 0}))
        self.assertNotIn("actions", evo.snapshot("2001-12-21", progress, {}, ["armor"], actions={"runs": 1}))

    def test_the_eight_languages_are_complete(self):
        self.assertEqual(texts.problems(), [])
        for code in ("en", "es", "de", "fr", "it", "ja", "zh", "pt"):
            self.assertIn("tab_actions", texts.TEXTS[code])
        self.assertIn("compilações", texts.TEXTS["pt"]["tab_actions"].lower())         # the portuguese of Portugal
        self.assertIn("ficheiro", texts.TEXTS["pt"]["ac_sig_present"])


class WorkflowTests(unittest.TestCase):
    """The build-finished trigger: filtered to this owner, rate-limited, read-only, no new secret and the pins untouched."""

    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / ".github" / "workflows" / "build-dashboard.yml").read_text(encoding="utf-8")
        cls.gate = cls.text.split("\n  gate:\n", 1)[1].split("\n  build:\n", 1)[0]

    def test_the_event_is_accepted_and_goes_through_the_gate(self):
        self.assertIn("      - ecosystem_build_finished\n", self.text)
        self.assertIn("    needs: gate\n    if: needs.gate.outputs.go == 'true'\n", self.text)

    def test_the_gate_is_read_only_and_uses_no_secret_and_no_third_party_action(self):
        self.assertIn("    permissions:\n      contents: read\n", self.gate)
        self.assertNotIn("secrets.", self.gate)
        self.assertNotIn("uses:", self.gate)

    def test_the_payload_reaches_the_script_only_as_an_environment_variable(self):
        self.assertNotIn("${{ github.event.client_payload", self.gate.split("run: |", 1)[1])
        self.assertIn("SOURCE_REPO: ${{ github.event.client_payload.repository }}", self.gate)

    def test_it_filters_by_owner_and_rate_limits(self):
        self.assertIn('^${owner}/[A-Za-z0-9._-]+$', self.gate)
        self.assertIn('[ "$SOURCE_REPO" = "$THIS_REPO" ]', self.gate)
        self.assertIn('MIN_MINUTES: "15"', self.gate)

    def test_the_cache_travels_with_the_other_generated_files(self):
        self.assertEqual(self.text.count("data/actions-cache.json"), 2)

    def test_the_concurrency_group_and_the_updater_pins_are_untouched(self):
        self.assertIn("group: ${{ github.event_name == 'pull_request' && format('ecosystem-dashboard-pr-{0}', github.event.number) || 'ecosystem-dashboard' }}", self.text)
        for repo in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
            self.assertRegex(self.text, repo + r"\.git@[0-9a-f]{40}")


if __name__ == "__main__":
    unittest.main()
