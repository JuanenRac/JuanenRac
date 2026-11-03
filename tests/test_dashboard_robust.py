# =============================================================================
# JuanenRac profile - tests/test_dashboard_robust.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Manifest health, generation figures, last known data, the URTC rack page, the keyboard help and the breadcrumb."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_app as app  # noqa: E402
import dashboard_health as health  # noqa: E402
import dashboard_nav_ui as nav  # noqa: E402
import dashboard_rack as rack  # noqa: E402
import dashboard_robust as robust  # noqa: E402
import dashboard_robust_texts as texts  # noqa: E402

GOOD = {"maturity": "functional", "evidence": "bench"}


def issue(kind, repo):
    return SimpleNamespace(kind=kind, repo=repo, ecosystem="urtc", detail="")


class TextsTests(unittest.TestCase):
    def test_eight_languages_complete_with_the_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        reference = set(texts.TEXTS["en"])
        for values in texts.TEXTS.values():
            self.assertEqual(set(values), reference)

    def test_the_texts_are_translated_and_portuguese_is_the_one_of_portugal(self):
        en = texts.TEXTS["en"]
        for key, value in en.items():
            if key in ("tab_rack", "crumb_home"):
                continue
            different = [code for code in ("es", "de", "fr", "it", "ja", "zh", "pt") if texts.TEXTS[code][key] != value]
            self.assertGreaterEqual(len(different), 4, f"{key} is hardly translated: {different}")
        pt = " ".join(texts.TEXTS["pt"].values())
        self.assertNotIn("celular", pt)
        self.assertNotIn("arquivo", pt)
        self.assertIn("ecrã", pt)
        self.assertIn("Atalhos de teclado", texts.TEXTS["pt"]["help_open"])


class ManifestHealthTests(unittest.TestCase):
    def test_valid_manifests_over_repositories(self):
        raw = {"A": GOOD, "B": GOOD, "C": {"maturity": "bogus", "evidence": "bench"}, "D": GOOD}
        health_ = robust.manifest_health(["A", "B", "C", "D"], raw, [issue("unknown_maturity", "C")])
        self.assertEqual((health_["valid"], health_["repos"], health_["percent"]), (3, 4, 75.0))
        self.assertEqual(robust.percent_text(health_), "75%")

    def test_a_manifest_that_is_not_listed_counts_in_the_total_but_not_as_valid(self):
        raw = {"A": GOOD, "B": GOOD}
        found = robust.manifest_health(["A", "B"], raw, [issue("invalid_manifest", "GHOST"), issue("unlisted_manifest", "GHOST2"), issue("api", "scope")])
        self.assertEqual((found["valid"], found["repos"], found["percent"]), (2, 4, 50.0))

    def test_same_repository_twice_is_counted_once(self):
        found = robust.manifest_health(["A"], {"A": GOOD}, [issue("invalid_manifest", "X"), issue("invalid_manifest", "X")])
        self.assertEqual(found["repos"], 2)

    def test_nothing_read_is_not_a_percentage(self):
        found = robust.manifest_health(["A", "B"], {}, [])
        self.assertIsNone(found["percent"])
        self.assertTrue(found["unread"])
        self.assertEqual(robust.percent_text(found), "–")
        self.assertIsNone(robust.manifest_health([], {}, [])["percent"])

    def test_a_manifest_that_could_not_be_read_is_not_valid(self):
        found = robust.manifest_health(["A", "B"], {"A": GOOD, "B": SimpleNamespace(data=None, error="404")}, [])
        self.assertEqual((found["valid"], found["repos"]), (1, 2))

    def test_the_card_says_how_it_is_calculated_and_shows_not_verified_without_data(self):
        base = dict(total=2, ok=2, errors=0, success_percent_text="100%", ecosystem_by_name={}, maturity_labels={}, evidence_labels={}, status={}, progress={}, maturity={}, evidence={}, activity={})
        card = app.registry_card(app.AppData(**base, manifest={"valid": 1, "repos": 2, "percent": 50.0}))
        self.assertIn('id="health-percent">50%<', card)
        self.assertIn("registry_help", card)
        self.assertIn('data-ok="1" data-repos="2"', card)
        unknown = app.registry_card(app.AppData(**base, manifest={"valid": 0, "repos": 2, "percent": None}))
        self.assertIn(">–<", unknown)
        self.assertIn("not_verified", unknown)
        self.assertIn("kpi-none", unknown)


class GenerationTests(unittest.TestCase):
    def gen(self, seconds, built="2001-12-20T08:31:12", asof="2001-12-20", steps=None):
        return robust.Generation(built, seconds, tuple(steps or (("versions", 38, 40), ("manifests", 36, 41), ("commits", 20, 40), ("activity", 40, 40))), asof)

    def test_the_figures_are_between_the_stable_markers(self):
        html = robust.generation_html(self.gen(47.6))
        self.assertIn(health.GEN_BEGIN, html)
        self.assertIn(health.GEN_END, html)
        self.assertIn('data-seconds="48"', html)
        self.assertIn('data-ok="38" data-total="40"', html)
        self.assertIn('data-activity-asof="2001-12-20"', html)

    def test_a_run_that_only_moved_the_figures_keeps_the_published_page(self):
        page = lambda g: "<main>" + robust.generation_html(g) + "<p>same</p></main>"   # noqa: E731
        old, new = page(self.gen(40.0)), page(self.gen(55.0, built="2001-12-20T09:00:00"))
        self.assertEqual(health.merge_build_info(new, old), old)
        changed = "<main>" + robust.generation_html(self.gen(55.0)) + "<p>other</p></main>"
        self.assertEqual(health.merge_build_info(changed, old), changed)

    def test_without_figures_the_card_says_so(self):
        html = robust.generation_html(None)
        self.assertIn("gen_unknown", html)
        self.assertNotIn("data-seconds", html)

    def test_the_stale_banner_names_its_date_or_is_empty(self):
        self.assertEqual(robust.stale_banner_html(None), "")
        banner = robust.stale_banner_html("2001-12-19")
        self.assertIn('data-date="2001-12-19"', banner)
        self.assertIn("not current", banner)


def page_with(repos, asof=None, snap=None):
    data = {"repos": repos, "snap": snap}
    region = f'<div data-activity-asof="{asof}">' if asof is not None else ""
    return f'<html>{region}<script type="application/json" id="dashboard-data">{json.dumps(data)}</script></html>'


class LastKnownTests(unittest.TestCase):
    REPOS = {
        "URTC-A": {"eco": "urtc", "known": True, "ci": "failure", "release": {"tag": "v1", "date": "2001-12-01T00:00:00Z"}, "commitDate": "2001-12-10T00:00:00Z",
                   "commits": [["fix", "2001-12-10T00:00:00Z", "https://github.com/JuanenRac/URTC-A/commit/1"]]},
        "URTC-B": {"eco": "urtc", "known": False, "ci": None, "release": None, "commitDate": None, "commits": None},
        "ARMOR-C": {"eco": "armor", "known": True, "ci": "success", "release": None, "commitDate": "2001-12-11T00:00:00Z", "commits": None},
    }

    def test_the_activity_of_the_published_page_is_rebuilt(self):
        found = robust.activity_from_page(page_with(self.REPOS, "2001-12-18"))
        self.assertEqual(sorted(found), ["ARMOR-C", "URTC-A"])
        self.assertEqual(found["URTC-A"].ci, "failure")
        self.assertEqual(found["URTC-A"].release_tag, "v1")
        self.assertEqual(found["URTC-A"].commits[0].headline, "fix")
        self.assertEqual(found["ARMOR-C"].commits, ())
        self.assertIsNone(found["ARMOR-C"].release_date)

    def test_a_page_that_cannot_be_read_gives_nothing(self):
        for bad in (None, "", "<html></html>", '<script type="application/json" id="dashboard-data">{broken</script>', page_with([])):
            self.assertEqual(robust.activity_from_page(bad), {})

    def test_the_date_of_the_data_comes_from_the_marker_or_from_the_snapshot(self):
        self.assertEqual(robust.previous_asof(page_with(self.REPOS, "2001-12-18")), "2001-12-18")
        self.assertEqual(robust.previous_asof(page_with(self.REPOS, None, {"date": "2001-12-17"})), "2001-12-17")
        self.assertIsNone(robust.previous_asof(page_with(self.REPOS, None, {"date": "x"})))
        self.assertIsNone(robust.previous_asof(None))

    def test_an_ecosystem_that_could_not_be_read_is_not_replaced_by_an_empty_one(self):
        before = robust.previous_ecosystem_counts(page_with(self.REPOS))
        self.assertEqual(before, {"urtc": 2, "armor": 1})
        self.assertEqual(robust.lost_ecosystems(before, {"armor": 1}, ["urtc"]), ["urtc"])
        self.assertEqual(robust.lost_ecosystems(before, {"armor": 1, "urtc": 2}, ["urtc"]), [])
        self.assertEqual(robust.lost_ecosystems(before, {"armor": 1}, ["eh3d"]), [])   # it was not on the published page either
        self.assertEqual(robust.lost_ecosystems({}, {}, ["urtc"]), [])

    def test_the_stale_state_is_never_a_healthy_one(self):
        base = dict(total=2, ok=2, errors=0, success_percent_text="100%", ecosystem_by_name={}, maturity_labels={}, evidence_labels={}, status={}, progress={}, maturity={}, evidence={}, activity={})
        data = app.AppData(**base, incomplete=["activity_stale"], stale_date="2001-12-19")
        card = app.alerts_card(data)
        self.assertIn('data-state="incomplete"', card)
        self.assertIn('data-date="2001-12-19"', card)
        self.assertNotIn("alerts_none", card)


SNAPSHOT = {
    "schema": 1, "name": "rack <one>", "source": "simulation", "occupied": 2, "slot_count": 2, "heating": 1, "maintenance_due": 1,
    "alarms": ["slot 0: maintenance due for unit 0:7", "slot 1: thermal check says overshoot", "slot 1: pre-heat limit reached, the target was switched off", "something else"],
    "slots": [
        {"slot": 0, "occupied": True, "tool_id": 3, "unit": "0:7", "target_c": 0, "expired": False, "thermal": "idle_ok", "maintenance_due": True,
         "wear": {"cycles": 3, "heater_seconds": 90, "faults": 0, "maintenance": True}},
        {"slot": 1, "occupied": True, "tool_id": 4, "unit": None, "target_c": 250, "expired": True, "thermal": "overshoot", "maintenance_due": False, "wear": None},
    ],
}


class RackTests(unittest.TestCase):
    def test_a_snapshot_in_the_shape_of_urtc_common_is_accepted(self):
        snap, problem = rack.validate(json.loads(json.dumps(SNAPSHOT)))
        self.assertEqual(problem, "")
        self.assertEqual(rack.card(snap)["state"], "alarm")
        quiet = dict(SNAPSHOT, alarms=[])
        self.assertEqual(rack.card(rack.validate(quiet)[0])["state"], "ok")

    def test_anything_else_is_refused_with_the_reason(self):
        for bad, reason in ((None, "JSON object"), ({**SNAPSHOT, "schema": 2}, "schema"), ({**SNAPSHOT, "name": ""}, "name"), ({**SNAPSHOT, "occupied": -1}, "occupied"),
                            ({**SNAPSHOT, "slots": []}, "slots"), ({**SNAPSHOT, "alarms": "x"}, "alarms"), ({**SNAPSHOT, "slots": [{"slot": 0}]}, "slot"),
                            ({**SNAPSHOT, "slots": [dict(SNAPSHOT["slots"][0], wear={"cycles": -1})]}, "wear")):
            snap, problem = rack.validate(bad)
            self.assertIsNone(snap)
            self.assertIn(reason, problem)

    def test_load_distinguishes_no_file_broken_file_and_good_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rack.json"
            self.assertEqual(rack.load(path), (None, ""))
            path.write_text("{nope", encoding="utf-8")
            self.assertEqual(rack.load(path), (None, "not valid JSON"))
            path.write_text(json.dumps(SNAPSHOT), encoding="utf-8")
            self.assertEqual(rack.load(path)[1], "")
        self.assertEqual(rack.card(None)["state"], "nodata")

    def test_the_page_escapes_every_value_and_translates_the_alarms(self):
        html = rack.panel_html(SNAPSHOT)
        self.assertNotIn("<one>", html)
        self.assertIn("rack &lt;one&gt;", html)
        self.assertIn('data-verdict-key="rack_v_overshoot"', html)
        self.assertIn('data-i18n-template="rack_alarm_maintenance"', html)
        self.assertIn("<li data-testid=\"rack-alarm\">something else</li>", html)
        self.assertIn('data-testid="rack-sim"', html)
        self.assertEqual(html.count('data-testid="rack-slot"'), 2)
        self.assertIn('data-state="alarm"', html)

    def test_without_a_snapshot_nothing_about_a_rack_is_claimed(self):
        html = rack.panel_html(None)
        self.assertIn('data-state="nodata"', html)
        self.assertIn("rack_nodata", html)
        self.assertNotIn("rack-table", html)
        self.assertNotIn("rack_state_ok", html)
        invalid = rack.panel_html(None, "schema 2 is not 1")
        self.assertIn('data-reason="schema 2 is not 1"', invalid)

    def test_unknown_values_are_shown_as_not_verified_or_no_data(self):
        snap = json.loads(json.dumps(SNAPSHOT))
        snap["slots"][1]["thermal"] = None
        html = rack.panel_html(snap)
        self.assertIn("not_verified", html)
        self.assertIn('data-i18n="no_data"', html)

    def test_the_published_sample_is_valid_when_it_exists(self):
        if rack.SNAPSHOT_PATH.exists():
            snap, problem = rack.load()
            self.assertEqual(problem, "")
            self.assertIsNotNone(snap)


class NavigationTests(unittest.TestCase):
    def test_every_shortcut_has_a_text_in_the_eight_languages(self):
        for _keys, key in nav.SHORTCUTS:
            for code in texts.TEXTS:
                self.assertTrue(texts.TEXTS[code][key].strip(), f"{key} {code}")

    def test_the_help_lists_every_key_the_script_handles(self):
        dialog = nav.help_dialog()
        for key in ("/", "1", "4", "0", "?", "C", "P", "Esc"):
            self.assertIn(f"<kbd>{key}</kbd>", dialog)
        for needle in ('event.key === "Escape"', 'key === "?"', 'key === "/"', 'key === "0"', "ECO_KEYS"):
            self.assertIn(needle, nav.JS)

    def test_shortcuts_are_off_while_typing_with_a_modifier_or_when_turned_off(self):
        self.assertIn("input, select, textarea", nav.JS)
        self.assertIn("event.ctrlKey || event.altKey || event.metaKey", nav.JS)
        self.assertIn("!shortcutsOn", nav.JS)
        import dashboard_evo_ui
        self.assertIn("!shortcutsOn", dashboard_evo_ui.JS)    # the old C and P keys obey the same switch

    def test_the_breadcrumb_follows_the_tab_the_scope_and_the_repository_in_the_address(self):
        for needle in ("crumbHash", "navRepo", "aria-current", "scope=", "repo="):
            self.assertIn(needle, nav.JS)
        script = app.script()
        self.assertIn('query.push("repo="', script)
        self.assertIn("var navRepo = null", script)
        self.assertEqual(script.count("function openPanel"), 1)

    def test_the_new_tab_and_its_texts_exist(self):
        self.assertIn("rack", app.TAB_IDS)
        self.assertEqual(app.ENGLISH["tab_rack"], "Rack")
        self.assertIn("help-open", nav.help_button())
        self.assertIn('aria-current="page"', nav.crumbs())


class ActivityFetchTests(unittest.TestCase):
    def node(self, name):
        return {"name": name, "latestRelease": None, "defaultBranchRef": {"target": {"committedDate": "2001-12-10T00:00:00Z", "statusCheckRollup": {"state": "SUCCESS"}, "history": {"nodes": []}}}}

    def test_the_pages_are_small_enough_for_github_to_answer(self):
        import dashboard_charts as charts
        self.assertIn("repositories(first: 20,", charts.ACTIVITY_QUERY)

    def test_a_page_that_fails_once_is_asked_again_and_a_page_that_keeps_failing_gives_nothing(self):
        import dashboard_charts as charts
        calls = []

        def flaky(body, headers):
            calls.append(1)
            if len(calls) == 1:
                return None
            return {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": [self.node("URTC-A")]}}}}
        self.assertEqual(list(charts.fetch_activity("o", "t", post=flaky)), ["URTC-A"])
        self.assertEqual(len(calls), 2)
        self.assertEqual(charts.fetch_activity("o", "t", post=lambda b, h: None), {})


if __name__ == "__main__":
    unittest.main()
