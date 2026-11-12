# =============================================================================
# JuanenRac profile - tests/test_dashboard_sentinel.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The tab "Sentinel": the criterion of red, the releases ready, the report made by rules, the reading with its fallbacks, the stability of the file and,
above all, what must never be published (security alerts, titles of pull requests and issues, people, branches)."""
import json
import re
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_sentinel as sn  # noqa: E402
import dashboard_sentinel_texts as texts  # noqa: E402
import dashboard_evo as evo  # noqa: E402

NOW = datetime(2001, 12, 21, 12, 0, 0, tzinfo=timezone.utc)
CONFIG = sn.check_config(None)[0]
NAMES = ["ARMOR-A", "ARMOR-B", "URTC-C", "HYDRA-UMC-D", "EH3D-E"]
PR_TITLE = "Bump lodash from 4.17.20 to 4.17.21 in /secret-folder"
CODEQL_RULE = "py/clear-text-logging-sensitive-data"


def run(path, conclusion, minutes_ago):
    return {"path": f".github/workflows/{path}", "conclusion": conclusion, "at": (NOW - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")}


class RedCriterionTests(unittest.TestCase):
    def test_the_last_finished_run_of_each_workflow_decides(self):
        runs = [run("ci.yml", "failure", 300), run("ci.yml", "success", 200), run("build.yml", "success", 300), run("build.yml", "failure", 10)]
        red, checked = sn.red_workflows(runs)
        self.assertEqual([r["wf"] for r in red], ["build.yml"])
        self.assertEqual(checked, 2)

    def test_cancelled_and_skipped_runs_do_not_count_either_way(self):
        runs = [run("ci.yml", "failure", 300), run("ci.yml", "cancelled", 100), run("ci.yml", "skipped", 50)]
        red, _ = sn.red_workflows(runs)
        self.assertEqual(len(red), 1)                       # the last run that counts is still the failure
        self.assertEqual(sn.red_workflows([run("ci.yml", "success", 300), run("ci.yml", "cancelled", 10)])[0], [])

    def test_the_streak_counts_the_failures_in_a_row(self):
        runs = [run("ci.yml", "success", 500), run("ci.yml", "failure", 400), run("ci.yml", "timed_out", 300), run("ci.yml", "startup_failure", 200)]
        red, _ = sn.red_workflows(runs)
        self.assertEqual(red[0]["streak"], 3)
        self.assertEqual(red[0]["since"], (NOW - timedelta(minutes=200)).strftime("%Y-%m-%dT%H:%M:%SZ"))

    def test_a_deleted_workflow_is_not_red_for_ever(self):
        red, checked = sn.red_workflows([run("old.yml", "failure", 10), run("ci.yml", "success", 10)], current=["ci.yml"])
        self.assertEqual((red, checked), ([], 1))

    def test_a_run_without_a_conclusion_or_with_a_strange_path_is_ignored(self):
        runs = [run("ci.yml", None, 10), {"path": "not a workflow", "conclusion": "failure", "at": "2001-12-21T11:00:00Z"}, "text", None]
        self.assertEqual(sn.red_workflows(runs), ([], 0))


class ReleaseRuleTests(unittest.TestCase):
    def test_entries_under_unreleased_are_counted_until_the_next_version(self):
        text = "# Changelog\r\n\r\n## [Unreleased]\r\n\r\n- one\r\n* two\r\n  - nested\r\n\r\n## [1.0.0]\r\n- old\r\n"
        self.assertEqual(sn.unreleased_count(text), 3)
        self.assertEqual(sn.unreleased_count("## [1.0.0]\n- x\n"), 0)
        self.assertIsNone(sn.unreleased_count(None))

    def test_the_rule_of_the_owner(self):
        published = {"ARMOR-A": "2001-12-10T10:00:00Z", "ARMOR-B": "2001-12-20T10:00:00Z", "URTC-C": None, "HYDRA-UMC-D": "2001-12-19T11:59:00Z", "EH3D-E": None}
        tags = {"ARMOR-A": "0.1.1", "ARMOR-B": "0.2.0", "HYDRA-UMC-D": "0.3.0"}
        rows = sn.release_candidates({"ARMOR-A": 3, "ARMOR-B": 5, "URTC-C": 2, "HYDRA-UMC-D": 0, "EH3D-E": 9}, published, tags, NOW, 2.0, 1, ("EH3D-",))
        self.assertEqual([(r["repo"], r["entries"]) for r in rows], [("ARMOR-A", 3), ("URTC-C", 2)])    # B is too recent, D has no entry, E is skipped
        self.assertEqual(rows[0]["tag"], "0.1.1")
        self.assertEqual(rows[1]["tag"], "")                         # no release: no tag

    def test_the_limit_is_in_the_configuration(self):
        published = {"ARMOR-B": "2001-12-20T10:00:00Z"}
        self.assertEqual(sn.release_candidates({"ARMOR-B": 1}, published, {}, NOW, 2.0, 1), [])
        self.assertEqual(len(sn.release_candidates({"ARMOR-B": 1}, published, {}, NOW, 1.0, 1)), 1)
        self.assertEqual(sn.release_candidates({"ARMOR-B": 1}, {}, {}, NOW, 2.0, 2), [])


class ConfigTests(unittest.TestCase):
    def test_defaults_and_bad_values(self):
        config, problems = sn.check_config({"candidate_days": -1, "sections": {"ci": False, "nothing": True}, "list_max": "x", "enabled": "yes"})
        self.assertEqual(config["candidate_days"], 2.0)
        self.assertEqual(config["sections"]["ci"], True)             # the invalid block is ignored as a whole
        self.assertGreaterEqual(len(problems), 4)

    def test_valid_values_are_used(self):
        config, problems = sn.check_config({"enabled": False, "candidate_days": 5, "sections": {"hygiene": False}, "skip_candidate_prefixes": ["X-"]})
        self.assertEqual(problems, [])
        self.assertFalse(config["enabled"])
        self.assertEqual(config["candidate_days"], 5)
        self.assertFalse(config["sections"]["hygiene"])
        self.assertTrue(config["sections"]["ci"])
        self.assertEqual(config["skip_candidate_prefixes"], ["X-"])

    def test_the_shipped_configuration_is_valid(self):
        self.assertEqual(sn.load_config(ROOT / "dashboard-config.json")[1], [])

    def test_there_is_no_switch_for_security_alerts(self):
        """Not even a coarse count exists: the sentinel has no setting for it, so nothing can switch it on by mistake."""
        shipped = json.loads((ROOT / "dashboard-config.json").read_text(encoding="utf-8"))["sentinel"]
        self.assertFalse([k for k in list(shipped) + list(sn.DEFAULT_CONFIG) if "alert" in k.lower() or "codeql" in k.lower() or "secret" in k.lower()])


def record(**kw):
    base = {"state": "ok", "tag": None, "published": None, "entries": 0, "ci": [], "checked": 1, "rs": True, "perm": None}
    base.update(kw)
    return base


def read_of(**records):
    repos = {name: records.get(name.replace("-", "_"), record()) for name in NAMES}
    return {"asof": NOW.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": repos}


class AssembleTests(unittest.TestCase):
    def doc(self, read=None, signatures=None, actions=None, history=(), config=CONFIG):
        return sn.assemble(read or read_of(), NAMES, config, signatures or {}, actions, list(history), "2001-12-21")

    def test_a_quiet_situation_is_in_order(self):
        doc = self.doc(signatures={n: "verified" for n in NAMES})
        self.assertEqual(doc["ci"]["red_total"], 0)
        self.assertEqual([p["key"] for p in doc["parte"]], ["head", "all_ok", "settings"])
        self.assertEqual(doc["parte"][0]["level"], "ok")

    def test_everything_that_needs_a_decision_gets_a_line_and_the_worst_comes_first(self):
        read = read_of(ARMOR_A=record(ci=[{"wf": "ci.yml", "streak": 3, "since": "2001-12-20T10:00:00Z"}], entries=2, published="2001-12-01T00:00:00Z", tag="0.1.0"),
                       URTC_C=record(rs=False), HYDRA_UMC_D=record(state="unread"))
        actions = {"repos": {"ARMOR-A": {"state": "ok", "min": 20000, "min7": 40000}}}
        doc = self.doc(read, {"ARMOR-B": "invalid"}, actions)
        keys = [(p["key"], p["level"]) for p in doc["parte"]]
        self.assertEqual(keys, [("head", "bad"), ("sig", "bad"), ("red", "bad"), ("cand", "warn"), ("hyg", "warn"), ("settings", "info"), ("compute", "warn"), ("unread", "info")])
        self.assertEqual(doc["parte"][0]["p"], {"red": 1, "cand": 1, "bad": 1, "hyg": 1})
        self.assertEqual(doc["parte"][1]["p"]["list"], ["ARMOR-B"])

    def test_a_single_failure_is_a_warning_and_a_streak_a_problem(self):
        one = self.doc(read_of(ARMOR_A=record(ci=[{"wf": "ci.yml", "streak": 1, "since": "2001-12-20T10:00:00Z"}])))
        self.assertEqual([p["level"] for p in one["parte"] if p["key"] == "red"], ["warn"])
        many = self.doc(read_of(ARMOR_A=record(ci=[{"wf": "ci.yml", "streak": 2, "since": "2001-12-20T10:00:00Z"}])))
        self.assertEqual([p["level"] for p in many["parte"] if p["key"] == "red"], ["bad"])

    def test_what_could_not_be_read_is_never_in_order(self):
        read = read_of(ARMOR_A=record(state="unread"), ARMOR_B=record(state="unread"), URTC_C=record(state="unread"), HYDRA_UMC_D=record(state="unread"), EH3D_E=record(state="unread"))
        doc = self.doc(read)
        self.assertEqual(doc["read"], 0)
        self.assertNotIn("all_ok", [p["key"] for p in doc["parte"]])
        self.assertIsNone(sn.day_summary(doc))
        self.assertEqual(doc["hygiene"]["ruleset_checked"], 0)

    def test_the_ruleset_and_the_settings(self):
        read = read_of(ARMOR_A=record(rs=False, perm={"sha": False, "allowed": True}), ARMOR_B=record(rs=None), URTC_C=record(perm={"sha": True, "allowed": False}))
        hyg = self.doc(read)["hygiene"]
        self.assertEqual(hyg["ruleset_missing"], ["ARMOR-A"])
        self.assertEqual(hyg["ruleset_checked"], 4)                  # the unread one is not counted as checked
        self.assertEqual((hyg["sha_missing"], hyg["allowed_missing"], hyg["settings_checked"]), (["ARMOR-A"], ["URTC-C"], 2))
        self.assertEqual(hyg["gaps"], 2)

    def test_unknown_signature_states_count_as_not_verified(self):
        doc = self.doc(signatures={"ARMOR-A": "verified", "ARMOR-B": "present", "URTC-C": None})
        self.assertEqual((doc["signatures"]["verified"], doc["signatures"]["unverified"]), (1, 4))

    def test_computing_comes_from_the_builds_block_and_is_sorted(self):
        actions = {"repos": {"ARMOR-A": {"state": "ok", "min": 10, "min7": 50}, "ARMOR-B": {"state": "ok", "min": 30, "min7": 40}, "URTC-C": {"state": "unread"}, "OTHER": {"state": "ok", "min": 99, "min7": 99}}}
        comp = self.doc(actions=actions)["compute"]
        self.assertEqual([r["repo"] for r in comp["top"]], ["ARMOR-B", "ARMOR-A"])
        self.assertEqual((comp["total24"], comp["total7"], comp["warn"]), (40, 90, False))

    def test_a_section_switched_off_leaves_the_report(self):
        config = json.loads(json.dumps(CONFIG))
        config["sections"]["ci"] = False
        doc = self.doc(read_of(ARMOR_A=record(ci=[{"wf": "ci.yml", "streak": 3, "since": "2001-12-20T10:00:00Z"}])), config=config)
        self.assertNotIn("red", [p["key"] for p in doc["parte"]])

    def test_the_trend_adds_today_to_the_days_of_the_history(self):
        history = [{"date": "2001-12-19", "sentinel": {"red": 1, "cand": 2, "gaps": 3, "min": 4}}, {"date": "2001-12-20", "sentinel": {"red": 2, "cand": 2, "gaps": 3, "min": 5}},
                   {"date": "2001-12-18"}, {"date": "2001-12-17", "sentinel": {"red": "x"}}]
        trend = self.doc(history=history)["trend"]
        self.assertEqual(trend["dates"], ["2001-12-19", "2001-12-20", "2001-12-21"])
        self.assertEqual(trend["red"], [1, 2, 0])

    def test_no_reading_no_document(self):
        self.assertIsNone(sn.assemble(None, NAMES, CONFIG, {}, None, [], "2001-12-21"))

    def test_the_history_keeps_the_four_numbers_and_nothing_else(self):
        doc = self.doc(read_of(ARMOR_A=record(rs=False)))
        entry = evo.snapshot("2001-12-21", {"armor": (50, 100)}, {}, ["armor"], sentinel=sn.day_summary(doc))
        self.assertEqual(entry["sentinel"], {"red": 0, "cand": 0, "gaps": 1, "min": 0})
        self.assertNotIn("sentinel", evo.snapshot("2001-12-21", {"armor": (50, 100)}, {}, ["armor"], sentinel={"red": 1}))


class NothingSensitiveIsPublishedTests(unittest.TestCase):
    """The rule of the owner: no detail of the security alerts, no titles of pull requests or issues, no people, no branches, nothing from outsiders."""

    def poisoned(self):
        read = read_of(ARMOR_A=record(ci=[{"wf": "ci.yml", "streak": 2, "since": "2001-12-20T10:00:00Z"}], entries=1, published="2001-12-01T00:00:00Z", tag="0.1.0"))
        read["repos"]["ARMOR-A"].update({"alerts": [{"rule": CODEQL_RULE, "path": "src/secret.py", "line": 12}], "prs": [{"title": PR_TITLE, "author": "someone"}], "branch": "feature/private",
                                         "actor": {"login": "someone"}, "display_title": PR_TITLE})
        read["repos"]["ARMOR-A"]["ci"][0].update({"actor": "someone", "title": PR_TITLE, "branch": "feature/private"})
        return read

    def test_the_document_has_nothing_of_the_poisoned_input(self):
        doc = sn.assemble(self.poisoned(), NAMES, CONFIG, {}, {"repos": {"ARMOR-A": {"state": "ok", "min": 1, "min7": 2, "alerts": CODEQL_RULE, "title": PR_TITLE}}}, [], "2001-12-21")
        text = json.dumps(doc)
        for forbidden in (PR_TITLE, "lodash", CODEQL_RULE, "clear-text", "secret.py", "someone", "feature/private", "alerts", "codeql", "dependabot", "title", "actor", "login"):
            self.assertNotIn(forbidden.lower(), text.lower(), forbidden)

    def test_clean_throws_away_anything_outside_the_whitelist(self):
        dirty = {"asof": "2001-12-21T12:00:00Z", "repos": 5, "read": 5, "codeql": [{"rule": CODEQL_RULE}], "pull_requests": [{"title": PR_TITLE}],
                 "ci": {"checked": 1, "red": [{"repo": "ARMOR-A", "wf": "ci.yml", "streak": 1, "since": "2001-12-21T00:00:00Z", "title": PR_TITLE, "actor": "someone"},
                                              {"repo": "NOT-OURS", "wf": "ci.yml", "streak": 1}, {"repo": "ARMOR-A", "wf": PR_TITLE, "streak": 1}]},
                 "releases": {"candidates": [{"repo": "ARMOR-A", "entries": 2, "tag": PR_TITLE, "published": "yesterday"}]},
                 "parte": [{"key": "red", "level": "bad", "p": {"list": ["ARMOR-A", PR_TITLE, "NOT-OURS"], "text": PR_TITLE}}, {"key": "free_text", "level": "bad", "p": {}}]}
        out = sn.clean(dirty, NAMES)
        text = json.dumps(out)
        for forbidden in (PR_TITLE, CODEQL_RULE, "someone", "NOT-OURS", "pull_requests", "codeql", "yesterday"):
            self.assertNotIn(forbidden, text)
        self.assertEqual(out["ci"]["red"], [{"repo": "ARMOR-A", "wf": "ci.yml", "streak": 1, "since": "2001-12-21T00:00:00Z"}])
        self.assertEqual(out["releases"]["candidates"][0]["tag"], "")
        self.assertEqual(out["parte"], [{"key": "red", "level": "bad", "p": {"list": ["ARMOR-A"]}}])
        self.assertEqual(set(out), {"schema", "asof", "repos", "read", "ci", "releases", "signatures", "hygiene", "compute", "trend", "parte", "ecosystems", "unpublished", "tags", "events", "health"})

    def test_every_text_of_the_report_is_a_fixed_text_of_the_page(self):
        """The report holds the kind of line and its numbers; the words come from the translation table, never from the reading."""
        for key in sn.PARTE_KEYS:
            self.assertIn(f"sp_{key}", texts.TEXTS["en"])

    def test_the_published_file_is_clean(self):
        # A workflow FILE called codeql.yml may be red like any other and is named as such; what must never appear is a code-scanning alert (its rule, its text).
        path = ROOT / "data" / "sentinel.json"
        if not path.exists():
            self.skipTest("no data/sentinel.json yet")
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
        self.assertEqual(data["schema"], sn.SCHEMA)
        for pattern in (r"\bBump\b", r"\bfrom \d+\.\d+", r"\b(py|js|cpp|java|go|rb|cs)/[a-z][a-z0-9-]+", r"(?i)codeql(?!\.ya?ml\")", r"(?i)dependabot", r"(?i)secret.scanning", r"(?i)\"(title|actor|author|login|branch|rule|message)\""):
            self.assertIsNone(re.search(pattern, text), pattern)
        names = set(re.findall(r"\"repo\": \"([^\"]+)\"", text))
        self.assertTrue(all(sn.REPO_RE.match(n) for n in names))


class ReadingTests(unittest.TestCase):
    """read_all with a fake GitHub: what is asked, what is kept and how it fails."""

    def fake(self, workflows=("ci.yml",), runs=None, rulesets=None, perm=None, fail=()):
        calls = []
        node = lambda name: {"name": name, "isArchived": False, "defaultBranchRef": {"name": "main"},  # noqa: E731
                             "latestRelease": {"tagName": "v1.0.0", "publishedAt": "2001-12-01T00:00:00Z", "isDraft": False},
                             "changelog": {"text": "## [Unreleased]\n- a\n- b\n## [1.0.0]\n- c\n"}, "workflows": {"entries": [{"name": w} for w in workflows]}}

        def post(body, headers):
            calls.append(("graphql", json.loads(body)["query"]))
            return {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [node(n) for n in NAMES]}}}}

        def get(url):
            calls.append(("rest", url))
            if any(f in url for f in fail):
                return "error", "HTTP 500"
            if "/actions/runs" in url:
                return "ok", {"workflow_runs": runs if runs is not None else [{"path": ".github/workflows/ci.yml", "conclusion": "failure", "updated_at": "2001-12-21T10:00:00Z",
                                                                                 "display_title": PR_TITLE, "actor": {"login": "someone"}, "head_branch": "private"}]}
            if url.endswith("/rulesets"):
                return "ok", rulesets if rulesets is not None else [{"name": "protect-main", "enforcement": "active"}]
            if url.endswith("/actions/permissions"):
                return ("ok", perm) if perm else ("error", "HTTP 403")
            return "error", "unexpected"
        return post, get, calls

    def test_the_reading_keeps_only_what_the_rules_need(self):
        post, get, calls = self.fake()
        read = sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        record_ = read["repos"]["ARMOR-A"]
        self.assertEqual(record_["state"], "ok")
        self.assertEqual(record_["entries"], 2)
        self.assertEqual(record_["ci"], [{"wf": "ci.yml", "streak": 1, "since": "2001-12-21T10:00:00Z"}])
        self.assertIs(record_["rs"], True)
        self.assertIsNone(record_["perm"])
        text = json.dumps(read)
        for forbidden in (PR_TITLE, "someone", "private"):
            self.assertNotIn(forbidden, text)

    def test_the_runs_are_asked_for_the_default_branch_only_and_without_pull_requests(self):
        post, get, calls = self.fake()
        sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        urls = [u for kind, u in calls if kind == "rest" and "/actions/runs" in u]
        self.assertEqual(len(urls), len(NAMES))
        self.assertTrue(all("branch=main" in u and "status=completed" in u and "exclude_pull_requests=true" in u for u in urls))

    def test_the_settings_are_not_asked_again_when_the_first_three_are_refused(self):
        post, get, calls = self.fake()
        sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        self.assertEqual(sum(1 for kind, u in calls if u.endswith("/actions/permissions")), 3)

    def test_the_settings_are_read_when_the_token_may(self):
        post, get, _ = self.fake(perm={"sha_pinning_required": True, "allowed_actions": "all"})
        read = sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        self.assertEqual(read["repos"]["ARMOR-A"]["perm"], {"sha": True, "allowed": False})

    def test_the_settings_can_be_switched_off(self):
        config = json.loads(json.dumps(CONFIG))
        config["read_actions_settings"] = False
        post, get, calls = self.fake()
        sn.read_all("JuanenRac", NAMES, "token", config, NOW, post, get)
        self.assertFalse([u for kind, u in calls if u.endswith("/actions/permissions")])

    def test_a_failed_lookup_is_unread_and_never_green(self):
        post, get, _ = self.fake(fail=("/actions/runs",))
        read = sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        self.assertEqual({r["state"] for r in read["repos"].values()}, {"unread"})
        doc = sn.assemble(read, NAMES, CONFIG, {}, None, [], "2001-12-21")
        self.assertEqual(doc["read"], 0)

    def test_a_failed_ruleset_lookup_is_not_a_missing_ruleset(self):
        post, get, _ = self.fake(fail=("/rulesets",))
        read = sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        self.assertIsNone(read["repos"]["ARMOR-A"]["rs"])
        self.assertEqual(sn.assemble(read, NAMES, CONFIG, {}, None, [], "2001-12-21")["hygiene"]["ruleset_missing"], [])

    def test_a_ruleset_that_is_only_evaluating_does_not_protect(self):
        post, get, _ = self.fake(rulesets=[{"name": "protect-main", "enforcement": "evaluate"}, {"name": "other", "enforcement": "active"}])
        self.assertIs(sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)["repos"]["ARMOR-A"]["rs"], False)

    def test_no_token_or_no_answer_means_no_reading(self):
        post, get, _ = self.fake()
        self.assertIsNone(sn.read_all("JuanenRac", NAMES, "", CONFIG, NOW, post, get))
        self.assertIsNone(sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, lambda body, headers: None, get))

    def test_a_repository_that_the_listing_does_not_have_is_unread(self):
        post, get, _ = self.fake()
        read = sn.read_all("JuanenRac", NAMES + ["URTC-GHOST"], "token", CONFIG, NOW, post, get)
        self.assertEqual(read["repos"]["URTC-GHOST"], {"state": "unread"})

    def test_a_repository_without_workflows_has_nothing_red(self):
        post, get, _ = self.fake(workflows=())
        read = sn.read_all("JuanenRac", NAMES, "token", CONFIG, NOW, post, get)
        self.assertEqual((read["repos"]["ARMOR-A"]["ci"], read["repos"]["ARMOR-A"]["checked"]), ([], 0))


class FileAndStabilityTests(unittest.TestCase):
    def doc(self, minutes=0):
        return sn.assemble({"asof": (NOW + timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": read_of()["repos"]}, NAMES, CONFIG, {}, None, [], "2001-12-21")

    def test_an_unchanged_situation_keeps_the_saved_moment(self):
        saved, fresh = self.doc(), self.doc(30)
        self.assertEqual(sn.stabilize(fresh, saved)["asof"], saved["asof"])

    def test_a_change_or_an_old_reading_gives_the_fresh_one(self):
        saved = self.doc()
        changed = sn.assemble({"asof": "2001-12-21T12:30:00Z", "repos": read_of(ARMOR_A=record(rs=False))["repos"]}, NAMES, CONFIG, {}, None, [], "2001-12-21")
        self.assertEqual(sn.stabilize(changed, saved)["asof"], "2001-12-21T12:30:00Z")
        self.assertEqual(sn.stabilize(self.doc(60 * 7), saved)["asof"], self.doc(60 * 7)["asof"])
        self.assertIsNone(sn.stabilize(None, saved))
        self.assertEqual(sn.stabilize(saved, None), saved)

    def test_the_file_is_written_only_when_it_changes_and_reads_back_clean(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data" / "sentinel.json"
            doc = self.doc()
            self.assertTrue(sn.save(path, doc))
            self.assertFalse(sn.save(path, doc))
            self.assertFalse(sn.save(path, None))
            self.assertEqual(sn.load_saved(path, NAMES), doc)
            path.write_text("{ broken", encoding="utf-8")
            self.assertIsNone(sn.load_saved(path, NAMES))
            path.write_text(json.dumps({"schema": 99, "asof": "2001-12-21T12:00:00Z"}), encoding="utf-8")
            self.assertIsNone(sn.load_saved(path, NAMES))

    def test_the_block_of_the_page(self):
        doc = self.doc()
        self.assertEqual(sn.build(doc, None, CONFIG, "2001-12-21")["stale"], None)
        stale = sn.build(None, doc, CONFIG, "2001-12-21")
        self.assertEqual((stale["read"], stale["stale"]), (True, doc["asof"]))
        none = sn.build(None, None, CONFIG, "2001-12-21")
        self.assertEqual((none["read"], none["doc"]), (False, None))
        off = json.loads(json.dumps(CONFIG))
        off["enabled"] = False
        self.assertFalse(sn.build(doc, doc, off, "2001-12-21")["enabled"])


class HealthOfTheRefreshTests(unittest.TestCase):
    """The health block says how current the central panel is, in numbers and steps, never as a moment of its own."""

    def at(self, hhmmss: str) -> sn.datetime:
        return sn._parse(f"2001-12-21T{hhmmss}Z")

    def test_the_gap_is_the_time_between_the_two_last_readings_rounded_up_to_five_minutes(self):
        health = sn.health_of("2001-12-21T12:31:00Z", {"asof": "2001-12-21T12:00:00Z"}, self.at("12:34:00"), 0)
        self.assertEqual(health["gap_minutes"], 35)
        self.assertEqual(health["age_minutes"], 5)

    def test_the_wait_of_the_run_is_rounded_up_to_thirty_seconds_and_a_bad_value_is_zero(self):
        self.assertEqual(sn.health_of("2001-12-21T12:00:00Z", None, self.at("12:00:00"), 61)["build_queue_seconds"], 90)
        for bad in (None, "x", -5, True):
            self.assertEqual(sn.health_of("2001-12-21T12:00:00Z", None, self.at("12:00:00"), bad)["build_queue_seconds"], 0)

    def test_no_earlier_reading_means_no_gap(self):
        self.assertEqual(sn.health_of("2001-12-21T12:00:00Z", None, self.at("12:00:00"))["gap_minutes"], 0)

    def test_the_health_is_numbers_only_and_survives_the_whitelist(self):
        doc = {"asof": "2001-12-21T12:00:00Z", "health": {"age_minutes": 5, "gap_minutes": 30, "build_queue_seconds": 60, "extra": "who", "x": {"y": 1}}}
        self.assertEqual(sn.clean(doc, NAMES)["health"], {"age_minutes": 5, "gap_minutes": 30, "build_queue_seconds": 60})
        self.assertEqual(sn.clean({"asof": "2001-12-21T12:00:00Z", "health": "text"}, NAMES)["health"], {"age_minutes": 0, "gap_minutes": 0, "build_queue_seconds": 0})

    def test_an_unchanged_situation_keeps_the_saved_file_even_if_the_health_moves(self):
        saved = sn.with_health({"asof": "2001-12-21T12:00:00Z", "repos": 1}, None, self.at("12:03:00"), 0)
        fresh = dict(saved, asof="2001-12-21T12:30:00Z", health={"age_minutes": 15, "gap_minutes": 30, "build_queue_seconds": 600})
        self.assertEqual(sn.stabilize(fresh, saved, 1), saved)
        # after the limit the new moment is written (at most one bot commit an hour for a quiet situation)
        late = dict(fresh, asof="2001-12-21T13:05:00Z")
        self.assertEqual(sn.stabilize(late, saved, 1), late)

    def test_the_saved_health_is_kept_when_the_saved_document_is_kept(self):
        saved = {"asof": "2001-12-21T12:00:00Z", "health": {"age_minutes": 5, "gap_minutes": 30, "build_queue_seconds": 0}}
        self.assertEqual(sn.with_health(dict(saved), saved, self.at("12:50:00"), 900)["health"], saved["health"])

    def test_the_limit_of_a_late_panel_is_a_setting_and_reaches_the_page(self):
        self.assertEqual(sn.build(None, None, CONFIG, "2001-12-21")["behind_minutes"], 120)
        config, problems = sn.check_config({"behind_minutes": 90})
        self.assertEqual((config["behind_minutes"], problems), (90, []))
        self.assertTrue(sn.check_config({"behind_minutes": 5})[1])
        self.assertEqual(sn.DEFAULT_CONFIG["stale_hours"], 1)


class TextsTests(unittest.TestCase):
    def test_every_text_has_the_eight_languages_and_the_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.LANGUAGES), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})

    def test_portuguese_is_the_one_of_portugal(self):
        pt = " ".join(texts.TEXTS["pt"].values()).lower()
        for brazilian in ("arquivo", "tela ", "celular", "atualizar"):
            self.assertNotIn(brazilian, pt)
        self.assertIn("ficheiro", pt)

    def test_the_texts_name_no_alert_detail_and_no_audit(self):
        everything = " ".join(" ".join(t.values()) for t in texts.TEXTS.values()).lower()
        for word in ("audit", "claude", "sonnet", "openai"):
            self.assertNotIn(word, everything)


if __name__ == "__main__":
    unittest.main()
