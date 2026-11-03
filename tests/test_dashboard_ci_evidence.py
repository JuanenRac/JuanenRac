# =============================================================================
# JuanenRac profile - tests/test_dashboard_ci_evidence.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Technical evidence published by the CI: the schema, the verdict declared against verified, the expiry, the reader and the texts."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_ci_evidence as ce  # noqa: E402
import dashboard_ci_texts as texts  # noqa: E402
import dashboard_ci_ui as ui  # noqa: E402

TODAY = "2001-12-21"
CONFIG = json.loads(json.dumps(ce.DEFAULT_CONFIG))


def record(test_type="host-test", result="pass", date="2001-12-15T09:00:00Z", branch="main", repo="URTC-X", **extra):
    data = {"repo": repo, "workflow": "ci.yml", "commit": "a" * 40, "branch": branch, "date": date, "version": "0.1.0", "test_type": test_type,
            "result": result, "environment": "ubuntu-24.04", "hardware": None, "url": f"https://github.com/JuanenRac/{repo}/actions/runs/1"}
    if test_type in ("bench", "field"):
        data["hardware"] = {"bound": True, "device": "bench board"}
    data.update(extra)
    return data


def verdict(declared, records, error="", repo="URTC-X"):
    return ce.evaluate(declared, records, repo=repo, owner="JuanenRac", today=TODAY, config=CONFIG, error=error)


class SchemaFileTests(unittest.TestCase):
    """docs/evidence-schema.json must describe exactly what the reader requires."""

    def setUp(self):
        self.schema = json.loads((HERE.parent / "docs" / "evidence-schema.json").read_text(encoding="utf-8"))
        self.item = self.schema["$defs"]["record"]

    def test_the_required_fields_are_the_ones_the_reader_requires(self):
        self.assertEqual(set(self.item["required"]), set(ce.REQUIRED))
        self.assertEqual(set(self.item["properties"]), set(ce.REQUIRED) | {"details"})
        self.assertIs(self.item["additionalProperties"], False)

    def test_the_enumerations_match_the_reader(self):
        self.assertEqual(self.item["properties"]["test_type"]["enum"], list(ce.TEST_TYPES))
        self.assertEqual(self.item["properties"]["result"]["enum"], list(ce.RESULTS))
        self.assertEqual(self.schema["properties"]["schema_version"]["const"], ce.SCHEMA_VERSION)

    def test_the_example_of_the_schema_is_accepted_by_the_reader(self):
        for example in self.schema["examples"]:
            for rec in example["records"]:
                clean, problems = ce.validate_record(rec, rec["repo"], "JuanenRac")
                self.assertEqual(problems, [], rec)
                self.assertIsNotNone(clean)

    def test_the_config_of_the_repository_is_valid(self):
        config, problems = ce.load_config()
        self.assertEqual(problems, [])
        self.assertEqual(config["expire_days"].keys(), CONFIG["expire_days"].keys())


class ValidationTests(unittest.TestCase):
    def test_a_good_record_is_accepted(self):
        clean, problems = ce.validate_record(record(), "URTC-X", "JuanenRac")
        self.assertEqual(problems, [])
        self.assertEqual(set(clean), set(ce.REQUIRED))

    def test_every_required_field_is_required(self):
        for key in ce.REQUIRED:
            rec = record()
            del rec[key]
            self.assertIsNone(ce.validate_record(rec, "URTC-X", "JuanenRac")[0], key)

    def test_wrong_values_are_refused(self):
        bad = [record(repo="URTC-Y"), record(commit="zzz"), record(date="yesterday"), record(date="2001-13-40"), record(test_type="magic"), record(result="great"),
               record(url="https://example.com/x"), record(url="https://github.com/JuanenRac/OTHER/actions/runs/1"), record(workflow=" "), record(hardware="yes"),
               record(hardware={"bound": "yes"})]
        for rec in bad:
            self.assertIsNone(ce.validate_record(rec, "URTC-X", "JuanenRac")[0], rec)
        self.assertIsNone(ce.validate_record("text", "URTC-X", "JuanenRac")[0])

    def test_bench_and_field_need_the_hardware(self):
        for kind in ("bench", "field"):
            rec = record(kind)
            for hardware in (None, {"bound": False, "device": "x"}, {"bound": True}, {"bound": True, "device": " "}):
                rec["hardware"] = hardware
                self.assertIsNone(ce.validate_record(rec, "URTC-X", "JuanenRac")[0], (kind, hardware))
        self.assertIsNotNone(ce.validate_record(record("simulator"), "URTC-X", "JuanenRac")[0])

    def test_dates_with_and_without_time(self):
        for text in ("2001-12-15", "2001-12-15T09:00:00Z", "2001-12-15T09:00:00+02:00", "2001-12-15T09:00:00.123Z"):
            self.assertIsNotNone(ce.parse_date(text), text)
        self.assertIsNone(ce.parse_date(None))


class VerdictTests(unittest.TestCase):
    def test_nothing_published_is_not_verified(self):
        out = verdict("bench", None)
        self.assertEqual((out["state"], out["verified"]), ("nodata", ""))
        self.assertEqual(verdict("bench", [])["state"], "nodata")

    def test_a_read_failure_is_unread_never_verified(self):
        out = verdict("host-test", [record()], error="HTTP 503")
        self.assertEqual(out["state"], "unread")
        self.assertEqual(out["reason"], "HTTP 503")

    def test_a_passing_run_of_the_declared_level_verifies_it(self):
        for declared, kind in (("host-test", "unit"), ("host-test", "integration"), ("simulator", "simulator"), ("bench", "bench"), ("field", "field")):
            out = verdict(declared, [record(kind)])
            self.assertEqual(out["state"], "verified", (declared, kind))
            self.assertEqual(out["verified"], ce.LEVEL_OF_TYPE[kind])
            self.assertEqual(out["date"], "2001-12-15")
            self.assertTrue(out["url"].startswith("https://github.com/JuanenRac/URTC-X/"))

    def test_a_higher_proof_covers_a_lower_declaration(self):
        self.assertEqual(verdict("host-test", [record("bench")])["state"], "verified")

    def test_declaring_more_than_proved_is_below(self):
        out = verdict("bench", [record("host-test")])
        self.assertEqual((out["state"], out["declared"], out["verified"]), ("below", "bench", "host-test"))
        self.assertEqual(verdict("field", [record("bench")])["state"], "below")

    def test_declaring_none_is_verified_by_any_passing_run_and_a_missing_declaration_never_fails(self):
        self.assertEqual(verdict("none", [record()])["state"], "verified")
        self.assertEqual(verdict(None, [record()])["state"], "verified")
        self.assertEqual(verdict("bogus", [record()])["declared"], "")

    def test_a_failing_run_is_failing(self):
        self.assertEqual(verdict("simulator", [record("simulator", "fail")])["state"], "failing")
        self.assertEqual(verdict("simulator", [record("host-test"), record("simulator", "fail")])["state"], "failing")
        # a lower failure does not hide a higher pass
        self.assertEqual(verdict("host-test", [record("bench"), record("host-test", "fail")])["state"], "verified")

    def test_old_records_expire_with_the_limit_of_their_kind(self):
        old = "2001-12-01T09:00:00Z"                 # 20 days before the day
        self.assertEqual(verdict("host-test", [record("host-test", date=old)])["state"], "expired")     # limit 14
        self.assertEqual(verdict("simulator", [record("simulator", date=old)])["state"], "verified")    # limit 30
        very_old = "2001-01-01T00:00:00Z"
        self.assertEqual(verdict("bench", [record("bench", date=very_old)])["state"], "expired")
        self.assertEqual(verdict("bench", [record("bench", date="2001-07-01T00:00:00Z")])["state"], "verified")   # limit 180
        out = verdict("host-test", [record("host-test", date=old)])
        self.assertEqual(out["verified"], "none")
        self.assertEqual(out["date"], "2001-12-01")

    def test_the_limits_come_from_the_configuration(self):
        config = copy.deepcopy(CONFIG)
        config["expire_days"]["host-test"] = 30
        out = ce.evaluate("host-test", [record(date="2001-12-01T09:00:00Z")], repo="URTC-X", owner="JuanenRac", today=TODAY, config=config)
        self.assertEqual(out["state"], "verified")

    def test_a_date_in_the_future_proves_nothing(self):
        self.assertEqual(verdict("host-test", [record(date="2002-03-01T00:00:00Z")])["state"], "expired")

    def test_other_branches_do_not_count(self):
        out = verdict("host-test", [record(branch="feature")])
        self.assertEqual(out["state"], "nodata")
        self.assertEqual(verdict("host-test", [record(branch="feature"), record()])["state"], "verified")

    def test_invalid_records_prove_nothing_and_say_why(self):
        broken = record()
        del broken["workflow"]
        out = verdict("host-test", [broken])
        self.assertEqual((out["state"], out["invalid"]), ("invalid", 1))
        self.assertIn("workflow", out["reason"])
        mixed = verdict("host-test", [broken, record()])
        self.assertEqual((mixed["state"], mixed["invalid"]), ("verified", 1))

    def test_a_record_of_another_repository_is_refused(self):
        self.assertEqual(verdict("host-test", [record(repo="URTC-OTHER")])["state"], "invalid")

    def test_partial_and_skipped_runs_prove_nothing(self):
        self.assertEqual(verdict("host-test", [record("host-test", "partial")])["state"], "below")
        self.assertEqual(verdict("none", [record("host-test", "skipped")])["state"], "nodata")

    def test_the_number_of_records_looked_at_is_limited(self):
        many = [record("host-test", "pass", date="2001-12-15T09:00:00Z") for _ in range(ce.MAX_RECORDS + 5)]
        self.assertEqual(verdict("host-test", many)["state"], "verified")
        self.assertLessEqual(len(verdict("host-test", many)["tests"]), 8)


class BuildAndReadTests(unittest.TestCase):
    def test_build_marks_everything_unread_when_nothing_was_read(self):
        block = ce.build({"A": "bench", "B": "none"}, None, owner="JuanenRac", today=TODAY, config=CONFIG)
        self.assertFalse(block["read"])
        self.assertEqual({v["state"] for v in block["repos"].values()}, {"unread"})
        self.assertEqual(ce.counts(block)["verified"], 0)

    def test_build_and_counts(self):
        read = {"records": {"A": [record(repo="A", test_type="bench")], "B": [record(repo="B")]}, "errors": {"C": "HTTP 500"}}
        block = ce.build({"A": "bench", "B": "simulator", "C": "bench", "D": "bench"}, read, owner="JuanenRac", today=TODAY, config=CONFIG)
        self.assertTrue(block["read"])
        self.assertEqual(block["source"], "ci-evidence:ci-evidence.json")
        tally = ce.counts(block)
        self.assertEqual((tally["verified"], tally["below"], tally["unread"], tally["nodata"]), (1, 1, 1, 1))
        self.assertEqual(sum(tally.values()), 4)

    def test_read_all_separates_absent_files_from_failures(self):
        files = {
            "A": ("ok", {"schema_version": "1.0", "records": [record(repo="A")]}),
            "B": ("absent", None),
            "C": ("error", "HTTP 503"),
            "D": ("ok", {"schema_version": "9.9", "records": []}),
            "E": ("ok", ["not", "an", "object"]),
        }
        out = ce.read_all("JuanenRac", list(files), lambda repo, branch, path: files[repo], CONFIG)
        self.assertEqual(list(out["records"]), ["A"])
        self.assertEqual(set(out["errors"]), {"C", "D", "E"})
        self.assertIn("schema_version", out["errors"]["D"])

    def test_read_all_asks_for_the_configured_branch_and_file(self):
        asked = []
        ce.read_all("JuanenRac", ["A"], lambda repo, branch, path: asked.append((repo, branch, path)) or ("absent", None), CONFIG)
        self.assertEqual(asked, [("A", "ci-evidence", "ci-evidence.json")])


class ConfigTests(unittest.TestCase):
    def test_defaults_and_overrides(self):
        config, problems = ce.parse_config(None)
        self.assertEqual((config["branch"], problems), ("ci-evidence", []))
        config, problems = ce.parse_config({"expire_days": {"simulator": 10}, "branch": "evidence"})
        self.assertEqual((config["expire_days"]["simulator"], config["expire_days"]["bench"], config["branch"], problems), (10, 180, "evidence", []))

    def test_wrong_parts_fall_back_and_are_named(self):
        for raw in ({"expire_days": {"simulator": 0}}, {"expire_days": {"magic": 3}}, {"branch": "../x"}, {"path": "/etc"}, {"default_branches": []}, "text"):
            config, problems = ce.parse_config(raw)
            self.assertTrue(problems, raw)
            self.assertEqual(config, CONFIG)

    def test_a_missing_file_gives_defaults_and_a_problem(self):
        config, problems = ce.load_config(Path(tempfile.gettempdir()) / "t19_missing_config.json")
        self.assertEqual(config, CONFIG)
        self.assertTrue(problems)


class TextsAndMarkupTests(unittest.TestCase):
    def test_eight_languages_complete_with_the_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        reference = set(texts.TEXTS["en"])
        for values in texts.TEXTS.values():
            self.assertEqual(set(values), reference)

    def test_translated_and_portuguese_is_the_one_of_portugal(self):
        en = texts.TEXTS["en"]
        for code, values in texts.TEXTS.items():
            if code != "en":
                self.assertNotEqual(values["cie_title"], en["cie_title"], code)
        pt = texts.TEXTS["pt"]
        self.assertIn("ficheiro", pt["cie_source"])
        for word in ("arquivo", "usuário"):
            self.assertNotIn(word, " ".join(pt.values()).lower())

    def test_every_state_has_a_text_a_chip_and_a_glyph(self):
        markup = ui.view()
        for state in ce.STATES:
            self.assertIn(f"cie_st_{state}", texts.TEXTS["en"])
            self.assertIn(f'data-cie-state="{state}"', markup)
            self.assertIn(f"{state}:", ui.JS)

    def test_the_markup_uses_only_known_keys(self):
        import re
        for key in re.findall(r'data-i18n="([a-z_]+)"', ui.view()):
            self.assertTrue(key in texts.TEXTS["en"] or key in ("filter_ecosystem",), key)


if __name__ == "__main__":
    unittest.main()
