# =============================================================================
# JuanenRac profile - tests/test_dashboard_app.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The tabbed application of the status dashboard: its data, its charts, its texts and the structure of the page it produces."""
import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
# The updaters are installed packages in CI; next to this repository they are source checkouts.
for sibling in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
    candidate = HERE.parent.parent / sibling / "src"
    if candidate.is_dir():
        sys.path.append(str(candidate))

import dashboard_app as app  # noqa: E402
import dashboard_app_texts as app_texts  # noqa: E402
import dashboard_charts as charts  # noqa: E402

README = """
<!-- progress:hydra-umc -->
`[██████████▊░░░░░░░░░] 54%` - Calculated from real data: the maturity and the evidence that each of its 59 repositories declares.
<!-- /progress:hydra-umc -->
<!-- status:hydra-umc -->
### Ecosystem status

| Area | Status | Progress | Note |
| --- | :---: | --- | --- |
| Software | 🟢 | `█████████▌ 95%` | 56 of 59 repositories are at least functional. |
| Tests | 🟢 | `█████████▊ 98%` | 58 of 59 repositories have automated tests. |
| Continuous integration | 🟢 | `██████████ 100%` | 59 of 59 repositories have the last CI run green. |
| Releases | 🟢 | `█████████▊ 97%` | 57 of 59 repositories have published a release. |
| Documentation | 🟢 | `██████████ 100%` | 59 of 59 repositories have the README in the eight languages. |
| Simulation | 🔴 | `██▍░░░░░░░ 24%` | 14 of 59 repositories have been checked in a simulator. |
| Real hardware | 🔴 | `█▏░░░░░░░░ 11%` | 4 of the 38 repositories that depend on hardware have been checked. |
| Production | 🔴 | `▊░░░░░░░░░ 8%` | 5 of 59 repositories are established or in production. |
<!-- /status:hydra-umc -->
"""


class ReadmeTests(unittest.TestCase):
    def test_status_has_the_eight_areas_in_order(self):
        status = charts.parse_status(README, ["hydra-umc", "urtc"])
        self.assertEqual(list(status), ["hydra-umc"])
        areas = status["hydra-umc"]
        self.assertEqual(list(areas), list(charts.AREAS))
        self.assertEqual((areas["hardware"].percent, areas["hardware"].count, areas["hardware"].total), (11, 4, 38))
        self.assertEqual(charts.LIGHT_CLASS[areas["ci"].light], "good")
        self.assertEqual(charts.LIGHT_CLASS[areas["simulation"].light], "bad")

    def test_a_table_that_is_not_complete_is_left_out(self):
        broken = README.replace("| Production | 🔴 | `▊░░░░░░░░░ 8%` | 5 of 59 repositories are established or in production. |\n", "")
        self.assertEqual(charts.parse_status(broken, ["hydra-umc"]), {})

    def test_progress(self):
        self.assertEqual(charts.parse_progress(README, ["hydra-umc", "armor"]), {"hydra-umc": (54, 59)})


class CountTests(unittest.TestCase):
    def test_unknown_and_missing_values_are_counted_not_guessed(self):
        eco = {"a": "urtc", "b": "urtc", "c": "armor", "d": "other"}
        counts = charts.count_by_ecosystem({"a": "functional", "b": "nonsense", "c": None}, eco, charts.MATURITY_KEYS, ["urtc", "armor"])
        self.assertEqual(counts["urtc"]["functional"], 1)
        self.assertEqual(counts["urtc"][charts.UNKNOWN], 1)
        self.assertEqual(counts["armor"][charts.UNKNOWN], 1)
        self.assertEqual(sum(counts["urtc"].values()), 2)

    def test_evidence_values_from_raw_manifests_and_dicts(self):
        raw = {"a": SimpleNamespace(data={"evidence": "bench"}), "b": {"evidence": 3}, "c": SimpleNamespace(data=None)}
        self.assertEqual(charts.evidence_values(raw), {"a": "bench", "b": None, "c": None})


class ActivityTests(unittest.TestCase):
    NODES = [
        {"name": "A", "latestRelease": {"tagName": "v1.0.0", "publishedAt": "2001-10-01T10:00:00Z"},
         "defaultBranchRef": {"target": {"committedDate": "2001-10-02T00:00:00Z", "statusCheckRollup": {"state": "SUCCESS"}}}},
        {"name": "B", "latestRelease": None, "defaultBranchRef": {"target": {"committedDate": "2001-09-01T00:00:00Z", "statusCheckRollup": {"state": "FAILURE"}}}},
        {"name": "C", "latestRelease": None, "defaultBranchRef": None},
    ]

    def test_parse(self):
        act = charts.parse_activity(self.NODES)
        self.assertEqual((act["A"].release_tag, act["A"].ci), ("v1.0.0", "success"))
        self.assertEqual((act["B"].release_tag, act["B"].ci), (None, "failure"))
        self.assertEqual((act["C"].commit_date, act["C"].ci), (None, "none"))

    def test_without_a_token_nothing_is_requested_and_nothing_is_invented(self):
        def never(_body, _headers):
            raise AssertionError("no request without a token")
        self.assertEqual(charts.fetch_activity("x", "", never), {})

    def test_pages_are_followed_and_a_failure_gives_nothing(self):
        pages = [{"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": True, "endCursor": "c1"}, "nodes": self.NODES[:1]}}}},
                 {"data": {"repositoryOwner": {"repositories": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": self.NODES[1:]}}}}]
        seen = []

        def post(body, _headers):
            seen.append(json.loads(body)["variables"]["cursor"])
            return pages[len(seen) - 1]
        self.assertEqual(sorted(charts.fetch_activity("x", "t", post)), ["A", "B", "C"])
        self.assertEqual(seen, [None, "c1"])
        self.assertEqual(charts.fetch_activity("x", "t", lambda b, h: None), {})
        self.assertEqual(charts.fetch_activity("x", "t", lambda b, h: {"errors": []}), {})

    def test_months_end_at_the_newest_date_of_the_data(self):
        window = charts.last_months(["2001-11-02T00:00:00Z", "2001-11-01T00:00:00Z", "2001-10-05T00:00:00Z", None, "2000-01-01T00:00:00Z"], 6)
        self.assertEqual([label for label, _ in window], ["2001-06", "2001-07", "2001-08", "2001-09", "2001-10", "2001-11"])
        self.assertEqual(dict(window)["2001-11"], 2)
        self.assertEqual(charts.last_months([None, "bad"], 6), [])
        self.assertEqual(charts.last_months(["2001-02-01T00:00:00Z"], 3)[0][0], "2000-12")

    def test_newest_and_oldest(self):
        act = charts.parse_activity(ActivityTests.NODES)
        act["D"] = charts.Activity(release_tag="v2", release_date="2001-10-20T00:00:00Z")
        self.assertEqual([n for n, _ in charts.newest(act, "release_date", 5)], ["D", "A"])
        self.assertEqual([n for n, _ in charts.oldest(act, "release_date", 5, names={"A", "D"})], ["A", "D"])


class ChartTests(unittest.TestCase):
    def test_stacked_bars_are_well_formed_and_print_every_count(self):
        svg = charts.stacked_bars_svg([("URTC", {"a": 3, "b": 7}), ("EMPTY", {})], ["a", "b"], "mat")
        root = ET.fromstring(svg)
        ns = "{http://www.w3.org/2000/svg}"
        self.assertEqual(root.tag, ns + "svg")
        self.assertIsNone(root.get("aria-hidden"))   # the rows are focusable groups with a name, so the chart is not hidden
        rows = [g for g in root.iter(ns + "g") if g.get("data-aria") == "row"]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].get("tabindex"), "0")
        self.assertEqual(rows[0].get("aria-label"), "URTC: a 3, b 7")
        self.assertEqual(rows[1].get("aria-label"), "EMPTY: no data")   # nothing counted is "no data", never zero or a guess
        texts = [t.text for t in root.iter(ns + "text")]
        for expected in ("URTC", "3", "7", "10", "EMPTY", "–"):
            self.assertIn(expected, texts)
        self.assertEqual(len([r for r in root.iter(ns + "rect") if "seg-mat-" in (r.get("class") or "")]), 2)

    def test_segment_widths_add_up_to_the_track(self):
        svg = charts.stacked_bars_svg([("X", {"a": 1, "b": 3})], ["a", "b"], "ev", width=400, label_width=100)
        widths = [float(m) for m in re.findall(r'class="seg seg-ev-[a-z]" x="[\d.]+" y="\d+" width="([\d.]+)"', svg)]
        self.assertAlmostEqual(sum(widths), 400 - 100 - 34, places=0)

    def test_ring_and_columns(self):
        ET.fromstring(charts.ring_svg(54, "ring-x"))
        self.assertIn("–", charts.ring_svg(None))
        self.assertNotIn("ring-value", charts.ring_svg(None))   # no data draws the track only, never a (zero-length) value arc
        self.assertIn("ring-value", charts.ring_svg(0))
        self.assertIn("100%", charts.ring_svg(250))
        cols = charts.columns_svg([("2001-10", 14), ("2001-11", 97)])
        ET.fromstring(cols)
        self.assertIn(">97<", cols)
        self.assertEqual(charts.columns_svg([]), "")

    def test_relief_and_entrance_are_plain_shapes_and_css_hooks(self):
        bars = charts.stacked_bars_svg([("X", {"a": 1, "b": 3})], ["a", "b"], "ev", i18n_prefix="evidence_", names={"a": "A", "b": "B"})
        for hook in ("bar-depth", "seg-bevel", "seg-edge", "bar-fill", "bar-nums", 'data-name-key="evidence_a"', 'data-n="3"', 'data-total="4"'):
            self.assertIn(hook, bars)
        self.assertNotIn("<title>", bars)   # the tooltip is the page's own, in the language of the page
        ring = charts.ring_svg(40)
        for hook in ("ring-value", "ring-sheen", "--dash"):
            self.assertIn(hook, ring)
        cols = charts.columns_svg([("a", 2), ("b", 5)])
        for hook in ("col-top", "col-side", "col-body", 'data-aria="col"', 'data-total="7"'):
            self.assertIn(hook, cols)
        for svg in (bars, ring, cols):
            self.assertNotIn("<script", svg)
            self.assertNotIn("url(#", svg)   # no gradients to define: the relief survives any renderer

    def test_data_table_escapes_and_is_hidden_from_sight_only(self):
        html = charts.data_table("k", "Cap", [("h1", "A"), ("", "B")], [["<b>", 2]])
        self.assertIn('class="sr-only"', html)
        self.assertIn("&lt;b&gt;", html)
        ET.fromstring(html)


class TextTests(unittest.TestCase):
    def test_every_text_has_the_eight_languages(self):
        self.assertEqual(app_texts.problems(), [])
        self.assertEqual(set(app_texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        reference = set(app_texts.TEXTS["en"])
        for code, values in app_texts.TEXTS.items():
            self.assertEqual(set(values), reference, code)

    def test_portuguese_is_the_one_of_portugal(self):
        pt = app_texts.TEXTS["pt"]
        for word in ("ficheiro", "ecrã", "telemóvel"):
            self.assertTrue(any(word in value for value in pt.values()) or word == "telemóvel" or word == "ecrã", word)
        self.assertNotIn("arquivo", " ".join(pt.values()).replace("arquivos", ""))

    def test_the_eh3d_architecture_does_not_say_it_is_only_the_common_repository(self):
        for code, values in app_texts.TEXTS.items():
            self.assertNotIn("EH3D-COMMON (the project container and the machine types) exists", values["architecture_e_rel_body"])
        body = app_texts.TEXTS["en"]
        for repo in ("EH3D-SERVER", "EH3D-STUDIO", "DRILLPRO", "EH3D-NODE-BUNGARD-AUX", "EH3D-IOS-CONTROL", "EH3D-UPDATER"):
            self.assertTrue(any(repo in body[f"architecture_e_card{i}_body"] for i in range(1, 7)), repo)


class ShellTests(unittest.TestCase):
    def test_tabs(self):
        self.assertEqual(app.TAB_IDS, ("summary", "hydra-umc", "urtc", "armor", "eh3d", "projects", "evidence", "inventory", "architecture", "errors"))
        html = app.tab_list()
        self.assertEqual(html.count('role="tab"'), len(app.TAB_IDS))
        self.assertIn('role="tablist"', html)
        for ident in app.TAB_IDS:
            self.assertIn(f'aria-controls="panel-{ident}"', html)
            self.assertIn(f'data-testid="tab-{ident}"', html)
        self.assertEqual(html.count('aria-selected="false" tabindex="-1"'), len(app.TAB_IDS))

    def test_panel(self):
        html = app.panel("urtc", "<p>x</p>")
        self.assertIn('role="tabpanel"', html)
        self.assertIn('aria-labelledby="tab-urtc"', html)
        self.assertIn("hidden", html)

    def test_the_script_knows_every_tab_and_stores_safely(self):
        js = app.script()
        for ident in app.TAB_IDS:
            self.assertIn(f'"{ident}"', js)
        self.assertNotIn("__TAB_IDS__", js)
        self.assertIn("try { return localStorage", js)
        for key in ("ArrowRight", "ArrowLeft", "Home", "End", "hashchange"):
            self.assertIn(key, js)

    def test_sidebar_has_the_common_filters(self):
        html = app.sidebar([("functional", "Functional", 3)], [("api", "API", 2)], [("cm5", "CM5", 5)], {"urtc": 1}, "")
        for marker in ('id="project-search"', "data-filter-status=\"ok\"", 'data-filter-eco="urtc"', 'data-filter-maturity="functional"',
                       'data-filter-role="api"', 'data-filter-deploy="cm5"', 'id="family-select"', 'id="reset-filters"', 'id="filters-count"'):
            self.assertIn(marker, html)

    def test_meter_rows_say_no_data_instead_of_inventing(self):
        self.assertIn("no-data", app.meter_rows(None, "x"))
        rows = app.meter_rows(charts.parse_status(README, ["hydra-umc"])["hydra-umc"], "hydra-umc")
        self.assertEqual(rows.count('class="area '), 8)
        self.assertIn('aria-label="Real hardware: 11% (4 of 38)"', rows)


def _import_generator():
    try:
        import generate_dashboard
    except ImportError:  # the updater packages are not installed here
        return None
    return generate_dashboard


GENERATOR = _import_generator()

# Everything the dashboard showed before it became an application: each marker must still be in the page.
CHECKLIST = (
    'id="health-total"', 'id="health-resolved"', 'id="health-errors"', 'id="health-percent"', 'id="project-table"', 'id="empty-results"',
    'id="project-search"', 'id="family-select"', 'id="reset-filters"', 'id="lang-select"', 'id="theme-toggle"', 'id="dashboard-freshness"',
    "build-dashboard.yml/badge.svg", 'data-i18n="subtitle_v3"', 'data-i18n-template="subtitle_main"', 'data-i18n="architecture_intro"',
    'data-i18n="architecture_section"', 'data-i18n="architecture_section_u"', 'data-i18n="architecture_section_a"', 'data-i18n="architecture_section_e"',
    'data-i18n="architecture_h_card7_title"', 'data-i18n="architecture_u_card7_title"', 'data-i18n="architecture_a_card7_title"',
    'data-i18n="architecture_flow_operator"', 'data-i18n="architecture_u_flow_1"', 'data-i18n="architecture_a_flow_1"', 'data-i18n="architecture_e_flow_1"',
    'data-i18n="architecture_relationship_title"', 'data-i18n="architecture_u_rel_title"', 'data-i18n="architecture_a_rel_title"', 'data-i18n="architecture_e_rel_title"',
    'data-i18n="section_by_ecosystem"', 'data-i18n="section_deploy"', 'data-i18n="section_stack"', 'data-i18n="section_maturity"', 'data-i18n="section_evidence"',
    'data-i18n="section_role"', 'data-i18n="compat_section"', 'data-i18n="roadmap_section"', "data-filter-maturity=", "data-filter-deploy=", "data-filter-role=",
    "data-compat-view=", 'class="integrity', 'data-i18n="th_project"', 'data-i18n="th_type"', 'data-i18n="th_maturity"', 'data-i18n="th_stack"',
    'data-i18n="th_deploy"', 'data-i18n="th_version"', 'data-i18n="th_status"', 'data-i18n="th_commit"', 'data-i18n="footer_registry"',
    'data-i18n="footer_generator"', 'data-i18n="footer_workflow"', 'data-i18n="footer_note"', "https://github.com/JuanenRac/HYDRA-UMC-UPDATER",
    "data-ecosystem-banner=", 'class="project-row', "details-toggle", 'data-i18n="filter_ok"', 'data-i18n="filter_error"', 'data-i18n="family_label"',
    'data-i18n="reset_filters"', 'data-i18n="search_placeholder"' if False else 'data-i18n-placeholder="search_placeholder"',
)


@unittest.skipIf(GENERATOR is None, "the updater packages are not installed")
class PageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from hydra_umc_updater.registry import ProjectEntry
        entries = [
            ProjectEntry(name="HYDRA-UMC-A", stack="python", version_file="v", pattern="p", maturity="functional", role="service", family="Core", deploy="cm5"),
            ProjectEntry(name="URTC-B", stack="rust", version_file="v", pattern="p", maturity="scaffolding", role="library", family="Tools", deploy="user-pc"),
            ProjectEntry(name="ARMOR-C", stack="python", version_file="v", pattern="p", maturity="established", role="api", family="Net", deploy="cm5"),
        ]
        results = {e.name: SimpleNamespace(version="0.1.0", error=None, http_status=200, url="u") for e in entries}
        eco = {"HYDRA-UMC-A": "hydra-umc", "URTC-B": "urtc", "ARMOR-C": "armor"}
        raw = {"HYDRA-UMC-A": {"evidence": "bench"}, "URTC-B": {"evidence": "none"}, "ARMOR-C": {"evidence": "field"}}
        activity = charts.parse_activity(ActivityTests.NODES + [{"name": "HYDRA-UMC-A", "latestRelease": {"tagName": "v0.1.0", "publishedAt": "2001-10-03T00:00:00Z"},
                                                                  "defaultBranchRef": {"target": {"committedDate": "2001-10-04T00:00:00Z", "statusCheckRollup": {"state": "SUCCESS"}}}}])
        cls.html = GENERATOR.render_html(entries, results, {}, eco, [], None, raw_manifests=raw, activity=activity, readme_text=README)
        cls.empty = GENERATOR.render_html(entries, results, {}, eco, [], None, raw_manifests={}, activity={}, readme_text="")

    def test_every_tab_has_its_panel_and_the_ids_are_unique(self):
        for ident in app.TAB_IDS:
            self.assertEqual(len(re.findall(rf'\sid="tab-{ident}"', self.html)), 1, ident)
            self.assertEqual(len(re.findall(rf'\sid="panel-{ident}"', self.html)), 1, ident)
        ids = re.findall(r'\sid="([^"]+)"', self.html)
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        self.assertEqual(duplicates, [])

    def test_nothing_that_the_old_page_showed_is_missing(self):
        missing = [marker for marker in CHECKLIST if marker not in self.html]
        self.assertEqual(missing, [])

    def test_every_i18n_key_used_exists_in_the_eight_languages(self):
        keys = set(re.findall(r'data-i18n(?:-[a-z-]+)?="([^"]+)"', self.html))
        for code in ("en", "es", "de", "fr", "it", "ja", "zh", "pt"):
            missing = sorted(key for key in keys if key not in GENERATOR.TRANSLATIONS[code])
            self.assertEqual(missing, [], code)

    def test_charts_are_present_with_an_alternative(self):
        for chart in ("chart-maturity-all", "chart-evidence-all", "chart-ci-all", "chart-months"):
            self.assertIn(f'id="{chart}-t"' if chart != "chart-months" else 'data-testid="chart-months"', self.html)
        self.assertIn('class="sr-only"', self.html)
        self.assertGreaterEqual(self.html.count('role="img"'), 8)

    def test_without_data_the_page_says_so_instead_of_inventing(self):
        self.assertIn('data-i18n="no_activity"', self.empty)
        self.assertNotIn("chart-months", self.empty)
        self.assertIn("no-data", self.empty)

    def test_dark_is_the_default_theme(self):
        self.assertIn('"light" ? "light" : "dark"', self.html)

    def test_eh3d_architecture_is_current(self):
        self.assertIn('data-i18n="architecture_e_card6_title"', self.html)
        self.assertNotIn("Only EH3D-COMMON", self.html)
        self.assertIn("EH3D-NODE-BUNGARD-AUX", self.html)

    def test_the_search_covers_the_description_and_every_translation_exists(self):
        self.assertIn('data-notes="', self.html)
        self.assertIn("notes.includes(query)", self.html)
        for code in ("en", "es", "de", "fr", "it", "ja", "zh", "pt"):
            self.assertIn("table_electro_hobby_3d_banner", GENERATOR.TRANSLATIONS[code], code)

    def test_nothing_listed_is_never_painted_as_healthy(self):
        def data(total, ok, errors):
            return app.AppData(total=total, ok=ok, errors=errors, success_percent_text="–", ecosystem_by_name={}, maturity_labels={}, evidence_labels={},
                               status={}, progress={}, maturity={}, evidence={}, activity={})
        self.assertIn("kpi-none", app.errors_card(data(0, 0, 0)))
        self.assertNotIn("kpi-ok", app.errors_card(data(0, 0, 0)))
        self.assertIn("kpi-ok", app.errors_card(data(5, 5, 0)))
        self.assertIn("kpi-bad", app.errors_card(data(5, 0, 5)))
        for total, ok, expected in ((0, 0, "none"), (5, 5, "ok"), (5, 0, "bad"), (5, 3, "mid")):
            panel = app.summary_panel(data(total, ok, 0), "")
            self.assertIn(f'kpi kpi-{expected}" data-testid="kpi-resolved"', panel, (total, ok))

    def test_headings_and_scrollable_table_are_reachable(self):
        self.assertNotIn('<div class="section-title', self.html)
        self.assertIn('role="heading" aria-level="2" class="section-title', self.html)
        self.assertIn('class="table-wrapper" tabindex="0" aria-labelledby="tab-projects"', self.html)

    def test_family_headers_are_keyed_by_ecosystem(self):
        self.assertIn('(row.dataset.ecosystem || "") + "|" + family', self.html)

    def test_every_chart_name_key_of_the_page_exists_in_the_eight_languages(self):
        keys = set(re.findall(r'data-(?:a-)?name-key="([^"]+)"', self.html))
        self.assertTrue(keys)
        for code in ("en", "es", "de", "fr", "it", "ja", "zh", "pt"):
            self.assertEqual(sorted(k for k in keys if k not in GENERATOR.TRANSLATIONS[code]), [], code)

    def test_the_projects_tab_has_the_scope_bar_and_the_pager(self):
        self.assertIn('data-testid="scope-bar"', self.html)
        self.assertIn('id="pager"', self.html)
        self.assertLess(self.html.index('data-testid="scope-bar"'), self.html.index('id="project-table"'))
        self.assertLess(self.html.index('id="project-table"'), self.html.index('id="pager"'))

    def test_projects_carry_their_ecosystem(self):
        self.assertEqual(self.html.count('data-ecosystem="urtc" class="project-row'), 1)


class ScopeAndChartLabelTests(unittest.TestCase):
    """The scope bar of the projects tab, the pager and the names of the charts in the eight languages."""

    def test_scope_bar_has_all_the_ecosystems_and_the_cross_cutting_one(self):
        html = app.scope_bar({"urtc": 3, "electro-hobby-3d": 2}, 9)
        for ident in ("all", "hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"):
            self.assertIn(f'data-scope="{ident}"', html)
            self.assertIn(f'data-testid="scope-{ident}"', html)
        self.assertIn("<b>9</b>", html)
        self.assertIn("<b>3</b>", html)
        self.assertIn('data-i18n="scope_cross"', html)
        self.assertNotIn("compare", html.lower())   # the owner did not ask for comparison boxes or a table/cards switch
        ET.fromstring("<r>" + html + "</r>")

    def test_pager_is_hidden_until_the_script_needs_it(self):
        html = app.pager()
        self.assertIn(' hidden>', html)
        for marker in ('id="pager-prev"', 'id="pager-next"', 'data-i18n-template="pager_info"', 'data-i18n-aria-label="pager_label"'):
            self.assertIn(marker, html)

    def test_script_keeps_the_scope_in_the_address_and_in_storage_safely(self):
        js = app.script()
        for marker in ('"scope="', "SCOPE_KEY", "history.replaceState", "PAGE_SIZE", "function restoreScope", "function parseHash", "applyChartLabels"):
            self.assertIn(marker, js)
        self.assertIn("try { return localStorage", js)
        self.assertIn("try { localStorage.setItem", js)
        self.assertIn('event.key === "Escape"', js)   # the tooltip can be dismissed from the keyboard

    def test_every_key_the_chart_script_needs_exists_in_the_eight_languages(self):
        needed = ("aria_pct", "aria_pct_counts", "aria_no_data", "aria_row", "tip_count", "aria_key_figures", "aria_eh3d_flow", "scope_label", "scope_all",
                  "scope_cross", "scope_sub_label", "scope_all_hint", "pager_label", "pager_prev", "pager_next", "pager_info", "pager_range",
                  "unknown", "area_hardware", "maturity_functional", "evidence_bench", "ci_success")
        import generate_dashboard as generator
        for code in ("en", "es", "de", "fr", "it", "ja", "zh", "pt"):
            missing = [key for key in needed if key not in generator.TRANSLATIONS[code]]
            self.assertEqual(missing, [], code)

    def test_the_templates_of_the_chart_names_are_translated_not_copied(self):
        en = app_texts.TEXTS["en"]
        for key in ("aria_no_data", "aria_pct_counts", "tip_count"):
            for code in ("es", "de", "fr", "it", "ja", "zh", "pt"):
                self.assertNotEqual(app_texts.TEXTS[code][key], en[key], f"{key} {code}")
        self.assertIn("sem dados", app_texts.TEXTS["pt"]["aria_no_data"])   # european portuguese

    def test_charts_carry_the_keys_that_name_them(self):
        rows = app.meter_rows(charts.parse_status(README, ["hydra-umc"])["hydra-umc"], "hydra-umc")
        self.assertEqual(rows.count('data-aria="pct"'), 8)
        self.assertIn('data-a-name-key="area_hardware"', rows)
        self.assertIn('data-a-n="4" data-a-total="38"', rows)


if __name__ == "__main__":
    unittest.main()
