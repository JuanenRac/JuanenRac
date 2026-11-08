# =============================================================================
# JuanenRac profile - tests/test_dashboard_cover.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Coverage of the dashboard (owner / shown / without manifest), the notice of new, archived and disappeared repositories, the page kept when GitHub cannot be
read and the line with the reads of GitHub."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
# In CI the updaters are installed packages; next to this repository they are source checkouts.
for sibling in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
    candidate = ROOT.parent / sibling / "src"
    if candidate.is_dir():
        sys.path.append(str(candidate))

import dashboard_cover as cover  # noqa: E402
import dashboard_cover_texts as texts  # noqa: E402
import dashboard_integrity as integrity  # noqa: E402
import dashboard_robust as robust  # noqa: E402
import generate_dashboard as gen  # noqa: E402


class UnclassifiedCardTests(unittest.TestCase):
    def test_the_card_shows_the_three_figures_and_the_names(self):
        html = cover.unclassified_card(integrity.Coverage(listed=129, public=131, without_manifest=(".github", "NEW-REPO")))
        self.assertIn('class="number">2<', html)
        self.assertIn('data-owner="131"', html)
        self.assertIn('data-shown="129"', html)
        self.assertIn('data-without="2"', html)
        self.assertIn(".github, NEW-REPO", html)
        self.assertIn('data-state="gap"', html)

    def test_nothing_unclassified_is_a_zero_and_not_a_gap(self):
        html = cover.unclassified_card(integrity.Coverage(listed=10, public=10, without_manifest=()))
        self.assertIn('data-state="ok"', html)
        self.assertIn('class="number">0<', html)

    def test_a_listing_that_could_not_be_read_says_not_verified_never_zero(self):
        for unknown in (integrity.Coverage(listed=10, public=None, without_manifest=()), None):
            html = cover.unclassified_card(unknown)
            self.assertIn('data-state="unknown"', html)
            self.assertIn("–", html)
            self.assertNotIn('class="number">0<', html)

    def test_a_long_list_of_names_is_cut(self):
        names = tuple(f"repo-{i:02d}" for i in range(20))
        html = cover.unclassified_card(integrity.Coverage(listed=1, public=21, without_manifest=names))
        self.assertIn("(+8)", html)

    def test_a_name_is_escaped(self):
        html = cover.unclassified_card(integrity.Coverage(listed=1, public=2, without_manifest=('<b>"x"',)))
        self.assertNotIn("<b>", html)

    def test_the_ecosystem_cards_carry_the_card_only_when_a_coverage_exists(self):
        entries = []
        with_cover = gen.render_ecosystem_cards(entries, {}, integrity.Coverage(1, 2, ("x",)))
        self.assertIn("eco-unclassified", with_cover)
        self.assertNotIn("eco-unclassified", gen.render_ecosystem_cards(entries, {}, None))


class ChangesTests(unittest.TestCase):
    def test_new_archived_and_disappeared(self):
        found = cover.changes(["a", "b", "c", "d"], ["a", "b", "d", "e", "f"], archived=["b", "f"])
        self.assertEqual(found, {"new": ["e"], "archived": ["b"], "gone": ["c"]})

    def test_a_repository_born_archived_is_not_new_and_one_archived_before_is_not_reported_again(self):
        found = cover.changes(["a", "b"], ["a", "b", "z"], archived=["z", "a"])
        self.assertEqual(found, {"new": [], "archived": ["a"], "gone": []})
        again = cover.changes(["a", "b"], ["a", "b"], archived=["a"])
        self.assertEqual(again["archived"], ["a"])    # compared with the page, not remembered: the next page has it in its list and still names it once

    def test_nothing_is_claimed_without_a_reliable_comparison(self):
        empty = {"new": [], "archived": [], "gone": []}
        self.assertEqual(cover.changes(None, ["a"]), empty)
        self.assertEqual(cover.changes(["a"], None), empty)
        self.assertEqual(cover.changes(["a"], ["b"], reliable=False), empty)
        self.assertEqual(cover.changes([], ["b"]), empty)
        self.assertEqual(cover.changes(["a"], []), empty)

    def test_names_are_sorted_without_case(self):
        self.assertEqual(cover.changes(["z"], ["z", "b", "A", "c"])["new"], ["A", "b", "c"])

    def test_the_snapshot_is_replaced_only_by_a_reliable_listing(self):
        previous = {"repos": ["old"], "archived": []}
        self.assertEqual(cover.snapshot(["b", "A"], ["A"], True, previous), {"repos": ["A", "b"], "archived": ["A"]})
        self.assertEqual(cover.snapshot(["b"], [], False, previous), previous)
        self.assertEqual(cover.snapshot(None, [], True, previous), previous)
        self.assertIsNone(cover.snapshot(None, [], True, None))

    def test_the_notice_lists_each_kind_once_and_is_empty_without_changes(self):
        self.assertEqual(cover.changes_html({"new": [], "archived": [], "gone": []}), "")
        html = cover.changes_html({"new": ["a", "b"], "archived": [], "gone": ["c"]})
        self.assertIn('data-testid="changes-new"', html)
        self.assertIn('data-testid="changes-gone"', html)
        self.assertNotIn("changes-archived", html)
        self.assertIn('data-n="2"', html)

    def test_the_page_embeds_the_snapshot_and_reads_it_back(self):
        page = '<script type="application/json" id="dashboard-data">' + json.dumps({"cover": {"repos": ["a", "b"], "archived": ["b"]}}) + "</script>"
        self.assertEqual(robust.previous_cover(page), {"repos": ["a", "b"], "archived": ["b"]})
        self.assertIsNone(robust.previous_cover("<p>no data</p>"))
        self.assertIsNone(robust.previous_cover(None))
        bad = '<script type="application/json" id="dashboard-data">' + json.dumps({"cover": {"repos": [1]}}) + "</script>"
        self.assertIsNone(robust.previous_cover(bad))


class KeptPageTests(unittest.TestCase):
    PAGE = '<html><div class="summary-grid">\n  <section>x</section></div><p data-activity-asof="2001-12-20"></p></html>'

    def test_what_is_transient(self):
        for text in ("HTTP 403 listing page 1", "HTTP 429", "API rate limit exceeded", "lookup failed: timed out", "unable to list GitHub repositories for o", "HTTP 503"):
            self.assertTrue(robust.is_transient([text]), text)
        for text in ("x: invalid manifest: unknown field(s): foo", "HTTP 404", "schema_version must be 1.0"):
            self.assertFalse(robust.is_transient([text]), text)
        self.assertFalse(robust.is_transient([]))

    def test_the_banner_goes_first_once(self):
        marked = robust.mark_kept(self.PAGE, "2001-12-20")
        self.assertIn('data-testid="kept-banner"', marked)
        self.assertIn('data-date="2001-12-20"', marked)
        self.assertLess(marked.index("kept-banner"), marked.index("<section>"))
        self.assertEqual(robust.mark_kept(marked, "2001-12-21"), marked)
        self.assertEqual(robust.mark_kept("<p>other</p>", "2001-12-20"), "<p>other</p>")

    def test_keep_published_marks_the_page_and_does_not_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "index.html"
            self.assertEqual(gen.keep_published(self.PAGE, index, "HTTP 403", "2001-12-21"), 0)
            self.assertIn("kept-banner", index.read_text(encoding="utf-8"))
            self.assertEqual(gen.keep_published(None, Path(tmp) / "other.html", "HTTP 403", "2001-12-21"), 1)

    def test_the_line_of_reads_appears_only_when_something_was_read(self):
        self.assertEqual(robust.http_line(None), "")
        self.assertEqual(robust.http_line({"requests": 0}), "")
        line = robust.http_line({"requests": 140, "not_modified": 120, "stale": 3, "oldest_stale": 7300})
        for part in ('data-made="140"', 'data-saved="120"', 'data-served="3"', 'data-hours="2"'):
            self.assertIn(part, line)


class CommitLookupTests(unittest.TestCase):
    def test_the_lookup_of_the_commit_carries_the_moment_of_the_last_push(self):
        seen = {}
        original = gen._api_get
        gen._api_get = lambda url, unchanged_since=None: seen.update({url: unchanged_since}) or []
        try:
            gen.fetch_all_meta([type("E", (), {"name": "A"})(), type("E", (), {"name": "B"})()], pushed={"A": 1234})
        finally:
            gen._api_get = original
        self.assertEqual({url.split("/repos/JuanenRac/")[1].split("/")[0]: moment for url, moment in seen.items()}, {"A": 1234, "B": None})


class TextsTests(unittest.TestCase):
    def test_every_text_has_the_eight_languages_and_the_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        reference = set(texts.TEXTS["en"])
        for code, values in texts.TEXTS.items():
            self.assertEqual(set(values), reference, code)

    def test_the_texts_are_in_the_page_dictionary_in_every_language(self):
        for code in texts.LANGUAGES:
            for key in texts.TEXTS["en"]:
                self.assertEqual(gen.TRANSLATIONS[code][key], texts.TEXTS[code][key], f"{code} {key}")

    def test_no_visible_text_looks_like_an_untranslated_key(self):
        """The same pattern the browser tests use to find a key, an `undefined` or a placeholder that leaked into the page."""
        import re
        import dashboard_scripts_texts
        leftover = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+|[a-z]+\.[a-z]+_[a-z_0-9]+|undefined|NaN|\[object Object\]")
        rows = dict(texts._ROWS)
        rows.update({key: row for key, row in dashboard_scripts_texts.ROWS.items() if key.startswith(("sc_lint", "sc_lvl", "sc_rule", "sc_aria_lint", "sc_tip_lint"))})
        for key, row in rows.items():
            for code, text in zip(texts.LANGUAGES, row):
                self.assertIsNone(leftover.search(text), f"{code} {key}: {text[:60]}")

    def test_the_other_languages_are_not_copies_of_english(self):
        for key, english in texts.TEXTS["en"].items():
            for code in ("es", "de", "fr", "ja", "zh"):
                self.assertNotEqual(texts.TEXTS[code][key], english, f"{key} {code}")

    def test_the_new_texts_of_the_robust_module_are_complete(self):
        import dashboard_robust_texts as robust_texts
        self.assertEqual(robust_texts.problems(), [])
        for key in ("kept_banner", "gen_http"):
            for code in robust_texts.LANGUAGES:
                self.assertIn(key, robust_texts.TEXTS[code])


if __name__ == "__main__":
    unittest.main()
