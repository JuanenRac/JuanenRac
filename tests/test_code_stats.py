# =============================================================================
# JuanenRac profile - tests/test_code_stats.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The counter of code statistics: languages, comments, exclusions, classification, totals, history and the document. No network and no git."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import code_stats as cs  # noqa: E402

CONFIG = cs.load_config()


def lang(ext: str) -> cs.Language:
    return cs.BY_EXTENSION[ext]


class CountLinesTests(unittest.TestCase):
    def test_c_style_comments(self):
        text = "// line\nint a;\n\n/* block\n   still */\nint b; // trailing\n/* one */ int c;\n/* open */\n"
        self.assertEqual(cs.count_lines(text, lang("c")), (3, 4, 1))

    def test_a_comment_marker_after_code_is_code(self):
        self.assertEqual(cs.count_lines("x = 1  # note\n", lang("py")), (1, 0, 0))

    def test_hash_languages(self):
        self.assertEqual(cs.count_lines("# a\n\nimport os\n  # b\n", lang("py")), (1, 2, 1))
        self.assertEqual(cs.count_lines("#!/bin/sh\necho hi\n", lang("sh")), (1, 1, 0))

    def test_html_block_comment_over_lines(self):
        self.assertEqual(cs.count_lines("<!-- a\nb -->\n<p>x</p>\n", lang("html")), (1, 2, 0))

    def test_batch_and_sql_prefixes(self):
        self.assertEqual(cs.count_lines("REM hello\n:: other\necho x\n", lang("bat")), (1, 2, 0))
        self.assertEqual(cs.count_lines("-- a\nselect 1;\n", lang("sql")), (1, 1, 0))

    def test_block_that_never_closes_keeps_counting_comments(self):
        self.assertEqual(cs.count_lines("/* a\nb\nc\n", lang("rs")), (0, 3, 0))

    def test_the_text_without_final_newline_and_empty_text(self):
        self.assertEqual(cs.count_lines("a", lang("py")), (1, 0, 0))
        self.assertEqual(cs.count_lines("", lang("py")), (0, 0, 0))

    def test_every_language_has_a_name_and_extensions_do_not_clash(self):
        names = cs.language_names()
        self.assertIn("Python", names)
        self.assertIn("Rust", names)
        self.assertIn("Kotlin", names)
        self.assertEqual(len(names), len(set(names)))

    def test_cases_of_tests(self):
        self.assertEqual(cs.count_cases("def test_a():\n    pass\n  async def test_b():\n", lang("py")), 2)
        self.assertEqual(cs.count_cases("#[test]\nfn a() {}\n#[tokio::test]\nasync fn b() {}\n", lang("rs")), 2)
        self.assertEqual(cs.count_cases("TEST(A, b) {}\nTEST_CASE(\"x\") {}\n", lang("cpp")), 2)
        self.assertEqual(cs.count_cases("it('a', () => {});\ntest('b', () => {});\n", lang("ts")), 2)
        self.assertEqual(cs.count_cases("func main() {}\n", lang("go")), 0)


class ClassifyTests(unittest.TestCase):
    def kind(self, rel):
        return cs.classify(rel, CONFIG)

    def test_code_tests_docs_data(self):
        self.assertEqual(self.kind("src/main.rs"), "code")
        self.assertEqual(self.kind("tests/test_x.py"), "test")
        self.assertEqual(self.kind("pkg/foo_test.go"), "test")
        self.assertEqual(self.kind("web/app.spec.ts"), "test")
        self.assertEqual(self.kind("app/src/FooTest.kt"), "test")
        self.assertEqual(self.kind("e2e/tests/a.ts"), "test")
        self.assertEqual(self.kind("README.md"), "doc")
        self.assertEqual(self.kind("docs/guide.rst"), "doc")
        self.assertEqual(self.kind("config.json"), "data")
        self.assertEqual(self.kind("CMakeLists.txt"), "code")
        self.assertEqual(self.kind("requirements.txt"), "skip")

    def test_a_file_name_that_only_looks_like_a_test_is_code(self):
        self.assertEqual(self.kind("src/latest.py"), "code")
        self.assertEqual(self.kind("src/contest.rs"), "code")

    def test_skipped_names(self):
        for rel in ("logo.png", "icon.svg", "package-lock.json", "Cargo.lock", "app.min.js", "firmware.bin", "LICENSE.md", "a/b/model.stl", "x.pb.go"):
            self.assertEqual(self.kind(rel), "skip", rel)

    def test_translations(self):
        self.assertEqual(self.kind("app/i18n/es.json"), "l10n")
        self.assertEqual(self.kind("locales/de.ts"), "l10n")
        self.assertEqual(self.kind("android/res/values-es/strings.xml"), "l10n")
        self.assertEqual(self.kind("README_spa.md"), "doc")
        self.assertTrue(cs.is_readme_translation("README_spa.md"))
        self.assertTrue(cs.is_readme_translation("docs/README_jpn.md"))
        self.assertFalse(cs.is_readme_translation("README.md"))
        self.assertFalse(cs.is_readme_translation("README_spanish.md"))

    def test_unknown_extensions_are_not_counted(self):
        self.assertEqual(self.kind("thing.xyz"), "skip")
        self.assertEqual(self.kind("noextension"), "skip")


class GitattributesTests(unittest.TestCase):
    def test_generated_and_vendored_are_excluded(self):
        rules = cs.gitattributes_rules("*.gen.c linguist-generated\nthird/ linguist-vendored=true\ndocs/out/** linguist-generated=true\n# c\n*.txt text\n")
        self.assertTrue(cs.attributed("a/b.gen.c", rules))
        self.assertTrue(cs.attributed("third/x.c", rules))
        self.assertTrue(cs.attributed("sub/third/x.c", rules))
        self.assertTrue(cs.attributed("docs/out/page.html", rules))
        self.assertFalse(cs.attributed("src/a.c", rules))
        self.assertFalse(cs.attributed("docs/guide.md", rules))

    def test_unset_and_false_do_not_exclude_and_a_later_line_wins(self):
        rules = cs.gitattributes_rules("*.c -linguist-generated\n*.h linguist-generated=false\n*.rs linguist-generated\nkeep.rs -linguist-generated\n")
        self.assertFalse(cs.attributed("a.c", rules))
        self.assertFalse(cs.attributed("a.h", rules))
        self.assertTrue(cs.attributed("a.rs", rules))
        self.assertFalse(cs.attributed("keep.rs", rules))

    def test_an_anchored_pattern_only_matches_from_the_root(self):
        rules = cs.gitattributes_rules("/gen linguist-generated\n")
        self.assertTrue(cs.attributed("gen/a.c", rules))
        self.assertFalse(cs.attributed("sub/gen/a.c", rules))


def write(root: Path, rel: str, text: str | bytes) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8", newline="\n")


class ScanTreeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def build(self):
        write(self.root, "src/main.py", "# top\nimport os\n\nprint(1)\n")
        write(self.root, "src/lib.rs", "// c\nfn a() {}\nfn b() {}\n")
        write(self.root, "tests/test_main.py", "def test_a():\n    pass\n\ndef test_b():\n    pass\n")
        write(self.root, "README.md", "# Title\n\ntext\ntext\n")
        write(self.root, "README_spa.md", "# Titulo\n\ntexto\n")
        write(self.root, "docs/guide.md", "one\ntwo\n")
        write(self.root, "i18n/es.json", '{\n  "a": "b"\n}\n')
        write(self.root, "config.json", '{\n  "a": 1\n}\n')
        write(self.root, "node_modules/dep/index.js", "x = 1;\n" * 50)
        write(self.root, "build/out.c", "int a;\n")
        write(self.root, "vendor/lib.c", "int a;\n")
        write(self.root, "assets/logo.png", b"\x89PNG\r\n\x1a\n\0\0")
        write(self.root, "blob.py", b"x = 1\n\0\0\0")
        write(self.root, "gen/out.c", "int generated;\nint more;\n")
        write(self.root, ".gitattributes", "gen/** linguist-generated\n")
        write(self.root, "web/app.min.js", "a=1;\n")
        write(self.root, "web/bundle.js", "var a=1;" + "x" * 6000 + "\n")
        return cs.scan_tree(self.root, CONFIG)

    def test_code_is_counted_by_language_and_apart_from_tests(self):
        got = self.build()
        self.assertEqual(got["code"], {"files": 2, "code": 4, "comment": 2, "blank": 1})
        self.assertEqual(got["tests"]["files"], 1)
        self.assertEqual(got["tests"]["code"], 4)
        self.assertEqual(got["tests"]["blank"], 1)
        self.assertEqual(got["tests"]["cases"], 2)
        self.assertEqual(got["langs"]["Python"], {"files": 2, "code": 6, "comment": 1, "blank": 2})
        self.assertEqual(got["langs"]["Rust"], {"files": 1, "code": 2, "comment": 1, "blank": 0})

    def test_documentation_and_translations(self):
        got = self.build()
        self.assertEqual(got["docs"]["files"], 3)
        self.assertEqual(got["docs"]["lines"], 3 + 2 + 2)             # blank lines are kept apart
        self.assertEqual(got["docs"]["blank"], 2)
        self.assertEqual(got["l10n"]["files"], 2)                    # the translated README and the file of the folder i18n
        self.assertEqual(got["l10n"]["lines"], 2 + 3)

    def test_data_is_kept_apart_from_code(self):
        got = self.build()
        self.assertEqual(got["data"], {"files": 1, "lines": 3})
        self.assertNotIn("JSON", got["langs"])

    def test_nothing_excluded_is_counted(self):
        got = self.build()
        self.assertEqual(sorted(got["langs"]), ["Python", "Rust"])      # no node_modules, build, vendor, generated, minified, binary
        self.assertEqual(got["skipped"], 1)                           # the bundled file with a very long line
        self.assertEqual(got["files"], 2 + 1 + 3)

    def test_a_file_that_is_too_big_is_skipped(self):
        write(self.root, "big.py", "a = 1\n" * 10)
        small = dict(CONFIG, exclude=dict(CONFIG["exclude"], max_file_bytes=20))
        got = cs.scan_tree(self.root, small)
        self.assertEqual(got["skipped"], 1)
        self.assertEqual(got["code"]["files"], 0)

    def test_an_empty_tree(self):
        got = cs.scan_tree(self.root, CONFIG)
        self.assertEqual(got["files"], 0)
        self.assertEqual(got["langs"], {})
        self.assertEqual(got["code"]["code"], 0)

    def test_a_bom_and_crlf(self):
        write(self.root, "a.py", b"\xef\xbb\xbf# c\r\nx = 1\r\n\r\n")
        got = cs.scan_tree(self.root, CONFIG)
        self.assertEqual(got["code"], {"files": 1, "code": 1, "comment": 1, "blank": 1})


class ClassificationOfRepositoriesTests(unittest.TestCase):
    def test_tools_is_the_fifth_group(self):
        keys = [e["key"] for e in CONFIG["ecosystems"]]
        self.assertEqual(keys, ["hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"])
        self.assertEqual(CONFIG["ecosystems"][-1]["label"], "Tools")
        self.assertEqual(cs.check_config(CONFIG), [])
        # the updater of the suite is counted once, in Tools and not in EH3D
        owners = [e["key"] for e in CONFIG["ecosystems"] if any("ELECTRO-HOBBY-3D-UPDATER".startswith(p) for p in e["prefixes"])]
        self.assertEqual(owners, ["electro-hobby-3d"])
        repos = [{"name": n, "pushed": None, "archived": False, "fork": False} for n in ("TOOLS-GITHUB-ACTIONS-MONITOR", "ELECTRO-HOBBY-3D-UPDATER", "EH3D-SERVER")]
        chosen = {r["name"]: r["eco"] for r in cs.select(repos, CONFIG)}
        self.assertEqual(chosen, {"TOOLS-GITHUB-ACTIONS-MONITOR": "electro-hobby-3d", "ELECTRO-HOBBY-3D-UPDATER": "electro-hobby-3d", "EH3D-SERVER": "eh3d"})

    def test_ecosystems_by_prefix(self):
        eco = lambda n: cs.ecosystem_of(n, CONFIG)       # noqa: E731
        self.assertEqual(eco("ARMOR-SERVER"), "armor")
        self.assertEqual(eco("URTC"), "urtc")
        self.assertEqual(eco("URTC-DOCS"), "urtc")
        self.assertEqual(eco("HYDRA-UMC"), "hydra-umc")
        self.assertEqual(eco("HYDRA-UMC-SDK"), "hydra-umc")
        self.assertEqual(eco("EH3D-PHOENIX-PCB"), "eh3d")
        self.assertEqual(eco("ELECTRO-HOBBY-3D-UPDATER"), "electro-hobby-3d")
        self.assertEqual(eco("TOOLS-GITHUB-ACTIONS-MONITOR"), "electro-hobby-3d")
        self.assertIsNone(eco("JuanenRac"))
        self.assertIsNone(eco("random-project"))

    def test_types(self):
        typ = lambda n: cs.type_of(n, CONFIG)            # noqa: E731
        self.assertEqual(typ("ARMOR-NODE-RADAR"), "firmware")
        self.assertEqual(typ("EH3D-NODE-BUNGARD-AUX"), "firmware")
        self.assertEqual(typ("HYDRA-UMC"), "firmware")
        self.assertEqual(typ("ARMOR-ANDROID-CONTROL"), "apps")
        self.assertEqual(typ("HYDRA-UMC-WATCH"), "apps")
        self.assertEqual(typ("EH3D-PHOENIX-CAD"), "apps")
        self.assertEqual(typ("ARMOR-SERVER"), "services")
        self.assertEqual(typ("HYDRA-UMC-BRIDGE-CNC"), "services")
        self.assertEqual(typ("HYDRA-UMC-NODE-HEALING"), "services")
        self.assertEqual(typ("ARMOR-DOCS"), "docs")
        self.assertEqual(typ("HYDRA-UMC-DOCS-QA"), "docs")
        self.assertEqual(typ("URTC-UPDATER"), "tools")
        self.assertEqual(typ("anything-new"), "tools")                # the default

    def test_every_type_of_the_rules_is_declared(self):
        order = set(CONFIG["types"]["order"])
        self.assertTrue({r["type"] for r in CONFIG["types"]["rules"]} <= order)

    def test_the_selection_skips_forks_archived_and_excluded(self):
        listing = [{"name": "ARMOR-A", "pushed": "2001-01-02"}, {"name": "ARMOR-B", "fork": True}, {"name": "URTC-C", "archived": True},
                   {"name": "JuanenRac"}, {"name": ".github"}, {"name": "other"}, {"name": "EH3D-D"}]
        chosen = cs.select(listing, CONFIG)
        self.assertEqual([r["name"] for r in chosen], ["ARMOR-A", "EH3D-D"])
        self.assertEqual(chosen[0]["pushed"], "2001-01-02")


class ConfigTests(unittest.TestCase):
    def test_the_real_configuration_is_valid(self):
        self.assertEqual(cs.check_config(CONFIG), [])

    def test_problems_are_reported(self):
        broken = json.loads(json.dumps(CONFIG))
        del broken["exclude"]["dirs"]
        broken["types"]["default"] = "nothing"
        broken["history"]["max_points"] = 0
        problems = cs.check_config(broken)
        self.assertTrue(any("exclude.dirs" in p for p in problems))
        self.assertTrue(any("types.default" in p for p in problems))
        self.assertTrue(any("max_points" in p for p in problems))
        self.assertEqual(cs.check_config([]), ["not an object"])

    def test_the_exclusions_cover_what_is_always_generated_or_vendored(self):
        dirs = {d.lower() for d in CONFIG["exclude"]["dirs"]}
        for name in ("node_modules", "vendor", "build", "dist", "target", "__pycache__", "managed_components", ".git"):
            self.assertIn(name, dirs)


def record(code=0, tests=0, docs=0, eco="armor", kind="tools", state="ok", comment=0, files=1, cases=0, l10n=0):
    return {"eco": eco, "type": kind, "state": state, "files": files, "size": 10, "skipped": 0, "langs": {},
            "code": {"files": 1, "code": code, "comment": comment, "blank": 0}, "tests": {"files": 1, "code": tests, "comment": 0, "blank": 0, "cases": cases},
            "docs": {"files": 1, "lines": docs, "blank": 0}, "l10n": {"files": l10n, "lines": 0}, "data": {"files": 0, "lines": 0}}


class TotalsTests(unittest.TestCase):
    REPOS = {"A": record(100, 20, 30, "armor", "firmware", comment=5, cases=3, l10n=2), "B": record(50, 10, 5, "urtc", "apps", state="lastknown"),
             "C": {"eco": "urtc", "type": "apps", "state": "unread"}}

    def test_totals_skip_the_unread(self):
        t = cs.totals(self.REPOS)
        self.assertEqual((t["repos"], t["code"], t["comment"], t["tests"], t["docs"], t["cases"], t["l10n_files"]), (2, 150, 5, 30, 35, 3, 2))

    def test_groups(self):
        self.assertEqual(cs._group(self.REPOS, "eco"), {"armor": {"repos": 1, "code": 100, "tests": 20, "docs": 30}, "urtc": {"repos": 1, "code": 50, "tests": 10, "docs": 5}})
        self.assertEqual(sorted(cs._group(self.REPOS, "type")), ["apps", "firmware"])

    def test_the_point_of_the_history(self):
        point = cs.snapshot_point("2001-12-21", self.REPOS)
        self.assertEqual(point["d"], "2001-12-21")
        self.assertEqual(point["t"]["code"], 150)
        self.assertEqual(point["e"]["armor"]["code"], 100)
        self.assertEqual(json.loads(json.dumps(point)), point)

    def test_totals_of_nothing(self):
        self.assertEqual(cs.totals({})["code"], 0)

    def test_the_ratio_inputs_add_up_by_ecosystem_and_type(self):
        t = cs.totals(self.REPOS)
        for field in ("eco", "type"):
            groups = cs._group(self.REPOS, field)
            self.assertEqual(sum(g["code"] for g in groups.values()), t["code"])
            self.assertEqual(sum(g["tests"] for g in groups.values()), t["tests"])
            self.assertEqual(sum(g["docs"] for g in groups.values()), t["docs"])


class HistoryTests(unittest.TestCase):
    def points(self, days_back):
        from datetime import date, timedelta
        today = date(2001, 12, 21)
        return [{"d": (today - timedelta(days=n)).isoformat(), "t": {"code": n}} for n in days_back]

    def test_recent_days_are_kept_one_each(self):
        kept = cs.prune_history(self.points(range(0, 30)), "2001-12-21", CONFIG)
        self.assertEqual(len(kept), 30)

    def test_old_days_are_thinned_to_one_per_week_then_per_month(self):
        kept = cs.prune_history(self.points(range(0, 400)), "2001-12-21", CONFIG)
        self.assertLess(len(kept), 400)
        recent = [p for p in kept if p["d"] >= "2001-08-23"]
        self.assertEqual(len(recent), 121)                           # daily_days, the day itself included
        old = [p for p in kept if p["d"] < "2001-08-23"]
        weeks = {cs.date.fromisoformat(p["d"]).isocalendar()[:2] for p in old}
        self.assertEqual(len(weeks), len(old))                        # at most one per week

    def test_very_old_days_are_kept_one_per_month(self):
        kept = cs.prune_history(self.points(range(800, 1000)), "2001-12-21", CONFIG)
        months = {p["d"][:7] for p in kept}
        self.assertEqual(len(months), len(kept))

    def test_the_cap(self):
        small = dict(CONFIG, history=dict(CONFIG["history"], max_points=10))
        kept = cs.prune_history(self.points(range(0, 50)), "2001-12-21", small)
        self.assertEqual(len(kept), 10)
        self.assertEqual(kept[-1]["d"], "2001-12-21")

    def test_the_same_day_is_replaced_not_added(self):
        old = self.points(range(1, 4))
        merged = cs.merge_history(old, {"d": "2001-12-20", "t": {"code": 999}}, "2001-12-21", CONFIG)
        self.assertEqual(len(merged), 3)
        self.assertEqual([p for p in merged if p["d"] == "2001-12-20"][0]["t"]["code"], 999)

    def test_without_a_point_the_history_is_kept(self):
        old = self.points(range(1, 4))
        self.assertEqual(len(cs.merge_history(old, None, "2001-12-21", CONFIG)), 3)

    def test_invalid_points_are_dropped(self):
        kept = cs.prune_history([{"d": "nonsense"}, {"x": 1}, {"d": "2001-12-20", "t": {}}], "2001-12-21", CONFIG)
        self.assertEqual([p["d"] for p in kept], ["2001-12-20"])


class GitHubTests(unittest.TestCase):
    def test_the_token_goes_to_git_through_the_environment_only(self):
        env = cs.git_env("secret-token")
        self.assertIn("GIT_CONFIG_VALUE_0", env)
        self.assertNotIn("secret-token", env["GIT_CONFIG_VALUE_0"])        # it is base64 encoded inside the header
        self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")
        self.assertNotIn("GIT_CONFIG_COUNT", {k: v for k, v in cs.git_env(None).items() if k not in __import__("os").environ})

    def test_the_command_has_no_token_and_is_shallow(self):
        seen = {}

        def fake(command, **kwargs):
            seen["command"], seen["env"] = command, kwargs["env"]
            return subprocess.CompletedProcess(command, 0, "", "")
        self.assertTrue(cs.clone("JuanenRac", "ARMOR-A", Path("x"), "tok", 5, fake))
        self.assertIn("--depth", seen["command"])
        self.assertNotIn("tok", " ".join(seen["command"]))
        self.assertTrue(any(part.endswith("github.com/JuanenRac/ARMOR-A.git") for part in seen["command"]))

    def test_a_failed_clone_is_false(self):
        self.assertFalse(cs.clone("o", "n", Path("x"), None, 5, lambda c, **k: subprocess.CompletedProcess(c, 128, "", "boom")))

        def timeout(command, **kwargs):
            raise subprocess.TimeoutExpired(command, 1)
        self.assertFalse(cs.clone("o", "n", Path("x"), None, 5, timeout))

    def test_the_list_follows_the_pages(self):
        class Reply:
            def __init__(self, body):
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.body).encode()
        pages = [[{"name": f"ARMOR-{i}", "pushed_at": "2001-12-20T10:00:00Z", "fork": False, "archived": False} for i in range(100)],
                 [{"name": "URTC", "pushed_at": None}]]
        urls = []

        def opener(request, timeout):
            urls.append(request.full_url)
            return Reply(pages[len(urls) - 1])
        got = cs.list_repos("JuanenRac", None, opener)
        self.assertEqual(len(got), 101)
        self.assertEqual(got[0]["pushed"], "2001-12-20")
        self.assertIsNone(got[-1]["pushed"])
        self.assertEqual(len(urls), 2)

    def test_declared_tests_of_a_glance_file(self):
        text = json.dumps({"repos": {"A": {"tests": {"count": 162}}, "B": {"tests": {"count": "many"}}, "C": {}}})
        self.assertEqual(cs.declared_tests_from(text, "A"), 162)
        self.assertIsNone(cs.declared_tests_from(text, "B"))
        self.assertIsNone(cs.declared_tests_from(text, "C"))
        self.assertIsNone(cs.declared_tests_from(text, "Z"))
        self.assertIsNone(cs.declared_tests_from("not json", "A"))


class RunAllTests(unittest.TestCase):
    """The whole run over already-cloned directories (no git, no network)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.clones = self.base / "clones"
        self.out = self.base / "out"
        write(self.clones, "ARMOR-A/src/a.c", "int a;\n// c\n")
        write(self.clones, "ARMOR-A/tests/test_a.py", "def test_a():\n    pass\n")
        write(self.clones, "URTC-DOCS/README.md", "one\ntwo\n")
        write(self.clones, "URTC-DOCS/data/glance.json", json.dumps({"repos": {"ARMOR-A": {"tests": {"count": 7}}}}))
        self.listing = [{"name": "ARMOR-A", "pushed": "2001-12-19"}, {"name": "URTC-DOCS", "pushed": "2001-12-20"}, {"name": "URTC-GONE", "pushed": None}, {"name": "x"}]

    def run_it(self, day="2001-12-21", listing=None):
        quiet = []
        result = cs.run_all(CONFIG, self.out, self.base, None, day, repos=listing or self.listing, local_root=self.clones, log=quiet.append)
        return result, json.loads((self.out / cs.STATS_FILE).read_text(encoding="utf-8")), json.loads((self.out / cs.HISTORY_FILE).read_text(encoding="utf-8")), quiet

    def test_the_documents(self):
        result, stats, history, _ = self.run_it()
        self.assertEqual(result, {"fresh": 2, "wanted": 3, "history_written": True})
        self.assertEqual(stats["day"], "2001-12-21")
        self.assertEqual(sorted(stats["repos"]), ["ARMOR-A", "URTC-DOCS", "URTC-GONE"])
        self.assertEqual(stats["repos"]["ARMOR-A"]["code"]["code"], 1)
        self.assertEqual(stats["repos"]["ARMOR-A"]["tests"]["cases"], 1)
        self.assertEqual(stats["repos"]["ARMOR-A"]["declared_tests"], 7)       # from the glance file of the documentation repository
        self.assertEqual(stats["repos"]["URTC-DOCS"]["type"], "docs")
        self.assertEqual(stats["repos"]["URTC-GONE"]["state"], "unread")
        self.assertEqual(stats["totals"]["repos"], 2)
        self.assertEqual(stats["totals"]["docs"], 2)
        self.assertEqual([p["d"] for p in history["points"]], ["2001-12-21"])
        self.assertEqual(history["points"][0]["e"]["armor"]["code"], 1)

    def test_the_same_inputs_give_the_same_files(self):
        self.run_it()
        first = (self.out / cs.STATS_FILE).read_bytes(), (self.out / cs.HISTORY_FILE).read_bytes()
        self.run_it()
        self.assertEqual(first, ((self.out / cs.STATS_FILE).read_bytes(), (self.out / cs.HISTORY_FILE).read_bytes()))

    def test_the_next_day_adds_a_point(self):
        self.run_it("2001-12-21")
        _, _, history, _ = self.run_it("2001-12-22")
        self.assertEqual([p["d"] for p in history["points"]], ["2001-12-21", "2001-12-22"])

    def test_an_unreadable_repository_keeps_its_last_known_figures(self):
        self.run_it("2001-12-21")
        (self.clones / "ARMOR-A" / "src" / "a.c").unlink()
        import shutil
        shutil.rmtree(self.clones / "ARMOR-A")
        _, stats, _, log = self.run_it("2001-12-22")
        self.assertEqual(stats["repos"]["ARMOR-A"]["state"], "lastknown")
        self.assertEqual(stats["repos"]["ARMOR-A"]["code"]["code"], 1)
        self.assertTrue(any("last known" in line for line in log))

    def test_with_less_than_half_read_the_history_gets_no_false_dip(self):
        self.run_it("2001-12-21")
        import shutil
        shutil.rmtree(self.clones / "ARMOR-A")
        shutil.rmtree(self.clones / "URTC-DOCS")
        result, _, history, _ = self.run_it("2001-12-22")
        self.assertFalse(result["history_written"])
        self.assertEqual([p["d"] for p in history["points"]], ["2001-12-21"])

    def test_the_documents_hold_no_personal_or_private_text(self):
        self.run_it()
        for name in (cs.STATS_FILE, cs.HISTORY_FILE):
            text = (self.out / name).read_text(encoding="utf-8").lower()
            for word in ("sonnet", "claude", "token", "@"):
                self.assertNotIn(word, text)


if __name__ == "__main__":
    unittest.main()
