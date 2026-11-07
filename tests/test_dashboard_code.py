# =============================================================================
# JuanenRac profile - tests/test_dashboard_code.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The block "code" of the dashboard: what the page embeds, what it drops, the texts of the tab and its markup."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_code as dc  # noqa: E402
import dashboard_code_texts as texts  # noqa: E402
import dashboard_code_ui as ui  # noqa: E402


def repo(code=10, state="ok", eco="armor", kind="tools", **extra):
    base = {"eco": eco, "type": kind, "state": state, "pushed": "2001-12-20", "commit": "2001-12-19", "files": 3, "size": 100,
            "langs": {"Python": {"files": 1, "code": code, "comment": 1, "blank": 1}}, "code": {"files": 1, "code": code, "comment": 1, "blank": 1},
            "tests": {"files": 1, "code": 5, "comment": 0, "blank": 0, "cases": 2}, "docs": {"files": 1, "lines": 7, "blank": 1}, "l10n": {"files": 1, "lines": 3},
            "data": {"files": 0, "lines": 0}}
    base.update(extra)
    return base


def document(**repos):
    return {"schema": 1, "day": "2001-12-21", "ecosystems": [{"key": "armor", "label": "A.R.M.O.R."}, {"key": "urtc", "label": "URTC"}],
            "types": ["firmware", "tools"], "repos": repos, "totals": {"repos": len(repos), "code": 10}}


class BuildTests(unittest.TestCase):
    def test_a_good_document_is_embedded(self):
        got = dc.build(document(A=repo(), B=repo(30, eco="urtc", kind="firmware")), [{"d": "2001-12-20", "t": {"code": 5}, "e": {"armor": {"repos": 1, "code": 5, "tests": 1, "docs": 2}}, "y": {}}], "2001-12-21")
        self.assertTrue(got["read"])
        self.assertEqual(got["age"], 0)
        self.assertEqual(sorted(got["repos"]), ["A", "B"])
        self.assertEqual(got["repos"]["B"]["code"]["code"], 30)
        self.assertEqual(got["history"][0]["e"]["armor"]["code"], 5)
        self.assertEqual(json.loads(json.dumps(got)), got)

    def test_no_document_is_not_read(self):
        for bad in (None, [], {}, {"schema": 2, "repos": {}}, {"schema": 1, "repos": []}):
            got = dc.build(bad, None)
            self.assertFalse(got["read"])
            self.assertEqual(got["repos"], {})

    def test_only_unread_repositories_is_not_read(self):
        got = dc.build(document(A={"eco": "armor", "type": "tools", "state": "unread", "pushed": None}), [])
        self.assertFalse(got["read"])
        self.assertEqual(got["repos"]["A"], {"eco": "armor", "type": "tools", "state": "unread", "pushed": None})

    def test_unknown_things_are_dropped_and_bad_numbers_become_zero(self):
        weird = repo(secret="x", **{"tests": {"files": -4, "code": True, "comment": "7", "blank": 1.5, "cases": 10 ** 12}})
        got = dc.build(document(A=weird, **{"bad name": repo(), "C": repo(eco="nobody"), "D": repo(kind="nothing"), "E": repo(state="weird")}))
        self.assertEqual(sorted(got["repos"]), ["A"])
        self.assertNotIn("secret", got["repos"]["A"])
        self.assertEqual(got["repos"]["A"]["tests"], {"files": 0, "code": 0, "comment": 0, "blank": 0, "cases": 0})

    def test_dates_and_the_age(self):
        doc = document(A=repo(commit="not a date"))
        got = dc.build(doc, [], "2001-12-26")
        self.assertIsNone(got["repos"]["A"]["commit"])
        self.assertEqual(got["age"], 5)
        self.assertIsNone(dc.build(doc, [], "nonsense")["age"])

    def test_the_declared_tests_only_when_a_number(self):
        got = dc.build(document(A=repo(declared_tests=162), B=repo(declared_tests="many"), C=repo(declared_tests=True)))
        self.assertEqual(got["repos"]["A"]["declared_tests"], 162)
        self.assertNotIn("declared_tests", got["repos"]["B"])
        self.assertNotIn("declared_tests", got["repos"]["C"])

    def test_the_history_is_sorted_unique_and_capped(self):
        points = [{"d": f"2001-01-{n:02d}", "t": {}} for n in (5, 3, 3, 9)] + [{"d": "bad"}, "x"]
        got = dc.build(document(A=repo()), points)
        self.assertEqual([p["d"] for p in got["history"]], ["2001-01-03", "2001-01-05", "2001-01-09"])
        many = [{"d": f"{2000 + n // 365}-{(n % 365) // 31 + 1:02d}-{(n % 31) + 1:02d}", "t": {}} for n in range(2000)]
        self.assertLessEqual(len(dc.build(document(A=repo()), many)["history"]), dc.MAX_POINTS)

    def test_missing_files_give_nothing(self):
        self.assertIsNone(dc.load(ROOT / "nothing.json"))
        self.assertEqual(dc.load_history(ROOT / "nothing.json"), [])


class TextTests(unittest.TestCase):
    def test_eight_languages_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})

    def test_the_portuguese_is_the_one_of_portugal(self):
        blob = " ".join(texts.TEXTS["pt"].values()).lower()
        self.assertIn("ficheiro", blob)
        for word in ("arquivo", "tela", "celular", "repositório de código aberto"):
            self.assertNotIn(word, blob)

    def test_every_text_is_translated_for_real(self):
        en = texts.TEXTS["en"]
        for key in ("cd_title", "cd_hint", "cd_help_body", "cd_prop_title", "cd_lang_title", "cd_evo_title", "cd_top_title", "cd_table_hint"):
            for code in ("es", "de", "fr", "it", "ja", "zh", "pt"):
                self.assertNotEqual(texts.TEXTS[code][key], en[key], f"{code} {key}")

    def test_no_private_or_audit_wording(self):
        blob = " ".join(" ".join(row) for row in texts.TEXTS.values()).lower()
        for word in ("sonnet", "claude", "audit", "auditor"):
            self.assertNotIn(word, blob)

    def test_the_markup_uses_only_known_texts(self):
        html = ui.panel_html()
        import re
        for key in re.findall(r'data-i18n(?:-aria-label)?="([a-z0-9_]+)"', html):
            self.assertIn(key, texts.TEXTS["en"], key)
        self.assertIn('data-testid="code-root"', html)
        for ident in ("cd-prop-table", "cd-lang-table", "cd-evo-table", "cd-top-table"):       # every chart has its table
            self.assertIn(f'id="{ident}"', html)

    def test_the_script_uses_only_known_texts(self):
        import re
        for key in set(re.findall(r"dict\.(cd_[a-z0-9_]+)", ui.JS)):
            self.assertIn(key, texts.TEXTS["en"], key)
        for key in re.findall(r'"(cd_[a-z0-9_]+)"', ui.JS):
            if not key.endswith("_"):                  # a prefix completed at run time ("cd_type_" + the type)
                self.assertIn(key, texts.TEXTS["en"], key)

    def test_the_script_draws_nothing_from_a_library(self):
        self.assertNotIn("http://", ui.JS.replace("http://www.w3.org", ""))
        self.assertNotIn("innerHTML", ui.JS)


if __name__ == "__main__":
    unittest.main()
