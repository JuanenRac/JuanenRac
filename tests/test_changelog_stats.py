# =============================================================================
# JuanenRac profile - tests/test_changelog_stats.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The parser and the classifier of the changelogs, the totals of the changes and the pace of the tags. No network."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import changelog_stats as cl  # noqa: E402
import code_stats as cs  # noqa: E402

CONFIG = cs.load_config()["changelog"]
RULES = cl._compile(CONFIG)

SAMPLE = """# Changelog

Intro text that is not an entry.

## [Unreleased]

- **Fix:** the parser no longer crashes
  on an empty file.
- **Panel:** the figures of the day.

## [1.2.0] - Second version

### Added

- **Thing:** a plain item under Added.

### Fixed

- **Other thing:** a plain item under Fixed.

* **Star:** a star bullet with the word faster in the text.

## [1.1.0]

- **Security:** a path is checked before it is opened.
- Docs for the guide.
  - a nested item that belongs to the entry above

```
- not an entry, inside a fence
```

## [0.9.0-beta.1] - Pre-release
- **New:** adds support for a second format.

## [Notes]

- not a version
"""


class ParseTests(unittest.TestCase):
    def test_sections_and_entries(self):
        sections = cl.parse(SAMPLE)
        self.assertEqual([s["name"] for s in sections], ["Unreleased", "1.2.0", "1.1.0", "0.9.0-beta.1", "Notes"])
        self.assertTrue(sections[0]["unreleased"])
        self.assertEqual([len(s["entries"]) for s in sections], [2, 3, 2, 1, 1])

    def test_titles_texts_and_continuation_lines(self):
        first = cl.parse(SAMPLE)[0]["entries"][0]
        self.assertEqual(first[0], "Fix")
        self.assertEqual(first[1], "the parser no longer crashes on an empty file.")

    def test_an_entry_without_a_bold_title_has_an_empty_title(self):
        entries = cl.parse(SAMPLE)[2]["entries"]
        self.assertEqual(entries[1][0], "")
        self.assertTrue(entries[1][1].startswith("Docs for the guide."))

    def test_a_nested_item_and_a_fence_are_not_entries(self):
        self.assertEqual(len(cl.parse(SAMPLE)[2]["entries"]), 2)

    def test_the_sub_heading_is_kept_for_each_entry(self):
        entries = cl.parse(SAMPLE)[1]["entries"]
        self.assertEqual([e[2] for e in entries], ["added", "fixed", "fixed"])

    def test_empty_and_without_sections(self):
        self.assertEqual(cl.parse(""), [])
        self.assertEqual(cl.parse("# Changelog\n\n- an entry outside any section\n"), [])

    def test_a_line_with_unicode_dash_in_the_heading(self):
        self.assertEqual(cl.parse("## [2.0.0] – Title\n- x\n")[0]["name"], "2.0.0")


class ClassifyTests(unittest.TestCase):
    def kind(self, title, text="", heading=None):
        return cl.classify(title, text, RULES, heading)

    def test_the_kinds_by_the_title(self):
        self.assertEqual(self.kind("Fix"), "fix")
        self.assertEqual(self.kind("Security"), "security")
        self.assertEqual(self.kind("Tests"), "tests")
        self.assertEqual(self.kind("Documentation"), "docs")
        self.assertEqual(self.kind("Faster start"), "performance")
        self.assertEqual(self.kind("Cleanup"), "refactor")
        self.assertEqual(self.kind("Added"), "added")
        self.assertEqual(self.kind("Changed"), "changed")

    def test_the_title_wins_over_the_text(self):
        self.assertEqual(self.kind("Fix", "adds a new feature and tests"), "fix")

    def test_the_text_is_used_when_the_title_says_nothing(self):
        self.assertEqual(self.kind("Panel", "no longer crashes"), "fix")
        self.assertEqual(self.kind("", "adds support for a format"), "added")

    def test_only_the_start_of_the_text_counts(self):
        text = "x" * 300 + " security"
        self.assertEqual(self.kind("Panel", text), cl.UNCLASSIFIED)

    def test_the_sub_heading_decides_by_itself(self):
        self.assertEqual(self.kind("Fix", "security", heading="added"), "added")

    def test_what_nothing_recognises_is_unclassified(self):
        self.assertEqual(self.kind("Panel", "the figures of the day"), cl.UNCLASSIFIED)
        self.assertEqual(self.kind("", ""), cl.UNCLASSIFIED)

    def test_words_match_from_the_start_of_a_word_only(self):
        self.assertEqual(self.kind("Prefix", "prefixes of the lines"), cl.UNCLASSIFIED)        # "fix" inside "prefix" is not a fix
        self.assertEqual(self.kind("Fixed"), "fix")

    def test_the_rules_come_from_the_configuration(self):
        custom = dict(CONFIG, kinds=[{"key": "x", "keywords": ["panel"]}])
        self.assertEqual(cl.classify("Panel", "", cl._compile(custom)), "x")
        self.assertEqual(cl.kind_keys(custom), ["x", "unclassified"])


class SummarizeTests(unittest.TestCase):
    def setUp(self):
        self.got = cl.summarize(SAMPLE, CONFIG)
        self.keys = cl.kind_keys(CONFIG)

    def test_the_counts(self):
        self.assertEqual((self.got["versions"], self.got["entries"], self.got["unreleased"]), (3, 6, 2))
        self.assertEqual(self.got["avg"], 2.0)

    def test_a_section_that_is_not_a_version_is_not_counted(self):
        self.assertNotIn("Notes", [v[0] for v in self.got["v"]])

    def test_the_kinds_add_up(self):
        self.assertEqual(sum(self.got["kinds"].values()), 8)
        self.assertEqual(sum(self.got["published_kinds"].values()), 6)
        self.assertEqual(self.got["kinds"]["fix"], 3)                     # the entry waiting and the two under "Fixed"
        self.assertEqual(self.got["kinds"]["unclassified"], 1)           # "Panel"
        self.assertEqual(self.got["kinds"]["security"], 1)

    def test_the_versions_newest_first_with_counts_per_kind(self):
        names = [v[0] for v in self.got["v"]]
        self.assertEqual(names, ["1.2.0", "1.1.0", "0.9.0-beta.1"])
        self.assertEqual(sum(self.got["v"][0][2]), self.got["v"][0][1])
        self.assertEqual(len(self.got["v"][0][2]), len(self.keys))

    def test_the_text_of_the_entries_is_kept_for_the_newest_versions_only(self):
        small = dict(CONFIG, detail_versions=1)
        got = cl.summarize(SAMPLE, small)
        self.assertEqual(len(got["v"][0]), 4)
        self.assertEqual(len(got["v"][1]), 3)
        self.assertEqual(got["u"][0][1], "Fix")

    def test_a_long_title_is_cut(self):
        text = "## [1.0.0]\n- **" + "word " * 40 + "**\n"
        label = cl.summarize(text, CONFIG)["v"][0][3][0][1]
        self.assertLessEqual(len(label), CONFIG["title_chars"])
        self.assertTrue(label.endswith("…"))

    def test_the_versions_are_capped(self):
        text = "".join(f"## [1.0.{n}]\n- **Fix:** x\n" for n in range(60))
        got = cl.summarize(text, dict(CONFIG, max_versions=7))
        self.assertEqual(len(got["v"]), 7)
        self.assertEqual(got["versions"], 60)

    def test_no_changelog_is_none_and_an_empty_one_is_zero(self):
        self.assertIsNone(cl.summarize(None, CONFIG))
        empty = cl.summarize("# Changelog\n", CONFIG)
        self.assertEqual((empty["versions"], empty["entries"], empty["avg"]), (0, 0, 0))

    def test_the_result_is_plain_json(self):
        self.assertEqual(json.loads(json.dumps(self.got)), self.got)

    def test_the_real_changelog_of_this_repository(self):
        got = cl.summarize((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), CONFIG)
        self.assertGreater(got["unreleased"], 0)


class ConfigTests(unittest.TestCase):
    def test_the_real_rules_are_valid(self):
        self.assertEqual(cl.check_rules(CONFIG), [])

    def test_problems(self):
        self.assertTrue(cl.check_rules(None))
        self.assertTrue(cl.check_rules({"kinds": []}))
        bad = dict(CONFIG, headings={"fixed": "nothing"})
        self.assertTrue(any("headings" in p for p in cl.check_rules(bad)))
        dup = dict(CONFIG, kinds=[{"key": "a", "keywords": []}, {"key": "a", "keywords": []}])
        self.assertTrue(any("distinct" in p for p in cl.check_rules(dup)))
        self.assertTrue(any("max_versions" in p for p in cl.check_rules(dict(CONFIG, max_versions=0))))

    def test_every_kind_has_words_and_a_label_in_the_dashboard(self):
        import dashboard_code_texts as texts
        for kind in cl.kind_keys(CONFIG):
            self.assertIn("ch_kind_" + kind, texts.TEXTS["en"], kind)
        for kind in CONFIG["kinds"]:
            self.assertTrue(kind["keywords"], kind["key"])


class RealWordingTests(unittest.TestCase):
    """Entries written the way the changelogs of the repositories write them: (title, start of the text, kind)."""

    CASES = [
        # versions, copies, pins, licence and project metadata
        ("", "Build version synchronized with `project.json` and the repository-native version source.", "maintenance"),
        ("", "Successful incremental build: synchronized package metadata and `project.json`.", "maintenance"),
        ("", "The licence is written as GPL-3.0-or-later in every header and in the package metadata.", "maintenance"),
        ("", "Maturity is functional: nothing here has been verified on real hardware yet.", "maintenance"),
        ("", "The banner follows the animated style of the ecosystem banners, with the name, the kind and the technologies.", "maintenance"),
        ("The copies of the shared repository are refreshed", "the generated protocol module, the vectors and the file name table.", "maintenance"),
        ("The four updaters are pinned to their current commits", "(one release each).", "maintenance"),
        ("The manifest declares the health path of the service", "(`service.health_path: /health`).", "maintenance"),
        ("Not done", "the radio side has never talked to a node of any kind.", "maintenance"),
        # build, continuous integration and tools
        ("`build.sh` / `build.bat`", ", **`run.sh` / `run.bat`** - venv creation, editable install and compile-check.", "tooling"),
        ("The full CI runs every night", "a scheduled workflow runs the complete baseline again.", "tooling"),
        ("`pyproject.toml`", "- packaging metadata, no runtime dependencies yet.", "tooling"),
        ("`.github/workflows/ci.yml`", "- new step that installs the requirements and runs the suite.", "tooling"),
        # an entry that describes what the program has or can do
        ("Two-step sign-in", "when the account has the second factor on, the sign-in asks for the six-digit code.", "added"),
        ("A trust store of public keys with aliases", "(`trust_store.py`): a JSON document.", "added"),
        ("`GET /jobs/{id}`", "one job without downloading the whole list.", "added"),
        ("The History has tabs", "All, Alarms, Connections, Devices, System and Settings.", "added"),
        ("The registry can be signed", "`registry keygen`, `registry sign` and `registry verify` make and check a signature.", "added"),
        ("The command line", "`eh3d-gerberview` with `render`, `info`, `measure` and `check`.", "added"),
        ("", "Every node publishes a health report about once a minute.", "added"),
        # an entry that says how something that existed now behaves
        ("The settings of the server are signed", "the retained settings message carries a counter.", "changed"),
        ("The steps of the system jobs are named in the interface language.", "", "changed"),
        # the old keywords keep their meaning
        ("Bounded request bodies", "a `POST` body over 1 MiB is refused; it used to be read whole.", "fix"),
        ("The content is checked before the rate limiter is used", "a frame with a wrong reading used to use up the window.", "fix"),
        ("Security", "a path is checked before it is opened.", "security"),
        ("Dependencies are installed without their install scripts", "the build hooks pass `--ignore-scripts` to `npm ci`.", "security"),
        ("Faster start", "the index is cached.", "performance"),
        # a keyword always beats a way of beginning: "New ..." is not enough when the entry is about tests, a fix or the workflow
        ("A new test of the parser", "", "tests"),
        ("A workflow that builds the images", "", "tooling"),
        ("A crash on start", "", "fix"),
        # the pieces of a word are not words
        ("A circle is drawn", "with CI (a command of the plotter language) in the middle.", "added"),
        ("A critical circuit is an administrator's", "", "added"),
        # what really says nothing about the kind stays unclassified
        ("Simulator", "the whole job runs to the end without hardware.", cl.UNCLASSIFIED),
        ("Blinking tab", "the title of the browser tab blinks with the number of alarms that wait for a person.", cl.UNCLASSIFIED),
        ("Alarm sounds", "Configuration > Preferences chooses a sound for each severity.", cl.UNCLASSIFIED),
        ("Enter walks the form", "accepting a field goes on to the next one, as in the original.", cl.UNCLASSIFIED),
        ("Class ids are stable", "the class index came from the labels present in that package.", cl.UNCLASSIFIED),
        ("", "", cl.UNCLASSIFIED),
    ]

    def test_the_cases(self):
        for title, text, kind in self.CASES:
            with self.subTest(title=title, text=text[:40]):
                self.assertEqual(cl.classify(title, text, RULES), kind)

    def test_a_beginning_never_beats_a_keyword_of_the_text(self):
        # "a ..." is a way of beginning (added); "crash" in the text is a word (fix) and wins
        self.assertEqual(cl.classify("", "a crash when the file is empty", RULES), "fix")

    def test_the_beginning_patterns_are_tried_after_all_the_keywords(self):
        rules = cl._compile({"kinds": [{"key": "a", "keywords": [], "patterns": ["^the "]}, {"key": "b", "keywords": ["panel"]}]})
        self.assertEqual(cl.classify("The panel", "", rules), "b")
        self.assertEqual(cl.classify("The thing", "", rules), "a")

    def test_a_pattern_that_is_not_a_regular_expression_is_a_problem(self):
        bad = dict(CONFIG, kinds=[{"key": "a", "keywords": ["x"], "patterns": ["("]}])
        self.assertTrue(any("regular expression" in p for p in cl.check_rules(bad)))


class TotalsAndTagsTests(unittest.TestCase):
    def record(self, entries, fix, eco="armor", kind="tools", unclassified=0):
        keys = cl.kind_keys(CONFIG)
        kinds = {k: 0 for k in keys}
        kinds["fix"], kinds["unclassified"] = fix, unclassified
        return {"eco": eco, "type": kind, "state": "ok", "changes": {"versions": 2, "entries": entries, "unreleased": 1, "kinds": kinds}}

    def test_change_totals(self):
        repos = {"A": self.record(10, 3, unclassified=2), "B": self.record(4, 1, "urtc"), "C": {"eco": "urtc", "type": "tools", "state": "ok", "changes": None},
                 "D": {"eco": "urtc", "type": "tools", "state": "unread"}}
        whole = cs.change_totals(repos)
        self.assertEqual((whole["repos"], whole["versions"], whole["entries"], whole["unreleased"], whole["fix"], whole["unclassified"]), (2, 4, 14, 2, 4, 2))
        by_eco = cs.change_totals(repos, "eco")
        self.assertEqual(sorted(by_eco), ["armor", "urtc"])
        self.assertEqual(by_eco["urtc"]["entries"], 4)
        self.assertEqual(cs.change_totals({})["entries"], 0)

    def test_the_history_point_carries_the_changes(self):
        point = cs.snapshot_point("2001-12-21", {"A": dict(self.record(10, 3), files=1, size=1, code={"code": 1, "comment": 0, "blank": 0, "files": 1},
                                                           tests={"code": 0, "files": 0, "cases": 0}, docs={"lines": 0}, l10n={"files": 0}, data={"lines": 0})})
        self.assertEqual(point["c"]["entries"], 10)
        self.assertEqual(point["ce"]["armor"]["fix"], 3)

    def reply(self, body):
        class Reply:
            def __enter__(self_inner):
                return self_inner

            def __exit__(self_inner, *args):
                return False

            def read(self_inner):
                return json.dumps(body).encode()
        return lambda request, timeout: Reply()

    def test_the_pace_of_the_tags(self):
        nodes = [{"target": {"committedDate": f"2001-12-{d:02d}T10:00:00Z"}} for d in (20, 15, 10)]
        nodes.append({"target": {"tagger": {"date": "2001-09-01T00:00:00Z"}}})
        nodes.append({"target": {"target": {"committedDate": "2001-08-01T00:00:00Z"}}})
        body = {"data": {"repository": {"refs": {"totalCount": 9, "nodes": nodes}}}}
        got = cs.tag_info("o", "r", "tok", "2001-12-21", self.reply(body))
        self.assertEqual(got["tags"], 9)
        self.assertEqual(got["last"], "2001-12-20")
        self.assertEqual((got["d30"], got["d90"]), (3, 3))
        self.assertAlmostEqual(got["gap"], (5 + 5 + 100 + 31) / 4, places=1)

    def test_without_a_token_or_with_a_bad_answer_it_is_unknown_not_zero(self):
        self.assertIsNone(cs.tag_info("o", "r", None, "2001-12-21", self.reply({})))
        self.assertIsNone(cs.tag_info("o", "r", "tok", "2001-12-21", self.reply({"data": None})))
        self.assertIsNone(cs.tag_info("o", "r", "tok", "2001-12-21", self.reply({"data": {"repository": {"refs": {"totalCount": "x", "nodes": []}}}})))

        def broken(request, timeout):
            raise OSError("down")
        self.assertIsNone(cs.tag_info("o", "r", "tok", "2001-12-21", broken))

    def test_a_repository_without_tags(self):
        body = {"data": {"repository": {"refs": {"totalCount": 0, "nodes": []}}}}
        got = cs.tag_info("o", "r", "tok", "2001-12-21", self.reply(body))
        self.assertEqual((got["tags"], got["last"], got["gap"]), (0, None, None))

    def test_the_token_is_sent_as_a_header_only(self):
        seen = {}

        def opener(request, timeout):
            seen["url"], seen["auth"], seen["data"] = request.full_url, request.get_header("Authorization"), request.data.decode()
            return self.reply({"data": None})(request, timeout)
        cs.tag_info("o", "r", "secret-token", "2001-12-21", opener)
        self.assertNotIn("secret-token", seen["url"] + seen["data"])
        self.assertEqual(seen["auth"], "Bearer secret-token")


class RunAllChangesTests(unittest.TestCase):
    def test_a_run_reads_the_changelog_and_the_tags(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            clone = base / "clones" / "ARMOR-A"
            (clone / "src").mkdir(parents=True)
            (clone / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
            (clone / "CHANGELOG.md").write_text("## [Unreleased]\n- **Fix:** a thing\n## [0.1.0]\n- **Added:** a thing\n", encoding="utf-8")
            calls = []

            def tags(owner, name, token, today):
                calls.append((owner, name, today))
                return {"tags": 3, "last": "2001-12-19", "d30": 1, "d90": 2, "gap": 4.0}
            cs.run_all(cs.load_config(), base / "out", base, None, "2001-12-21", repos=[{"name": "ARMOR-A", "pushed": "2001-12-20"}],
                       local_root=base / "clones", tags=tags, log=lambda text: None)
            stats = json.loads((base / "out" / cs.STATS_FILE).read_text(encoding="utf-8"))
            history = json.loads((base / "out" / cs.HISTORY_FILE).read_text(encoding="utf-8"))
        record = stats["repos"]["ARMOR-A"]
        self.assertEqual((record["changes"]["entries"], record["changes"]["unreleased"], record["changes"]["kinds"]["fix"]), (1, 1, 1))
        self.assertEqual(record["rel"]["tags"], 3)
        self.assertEqual(calls, [("JuanenRac", "ARMOR-A", "2001-12-21")])
        self.assertEqual(stats["kinds"][-1], "unclassified")
        self.assertEqual(history["points"][0]["c"]["entries"], 1)


if __name__ == "__main__":
    unittest.main()
