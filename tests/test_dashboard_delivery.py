# =============================================================================
# JuanenRac profile - tests/test_dashboard_delivery.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Signatures read from the latest release, the optional manifest fields of the delivery pipeline, its derived state, the optional alert and the texts."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_charts as charts  # noqa: E402
import dashboard_evo as evo  # noqa: E402
import dashboard_health as health  # noqa: E402
import dashboard_robust as robust  # noqa: E402
import dashboard_delivery as delivery  # noqa: E402
import dashboard_delivery_texts as texts  # noqa: E402
import dashboard_signatures_texts as sig_texts  # noqa: E402
import dashboard_delivery_ui as ui  # noqa: E402


class SignatureTests(unittest.TestCase):
    def test_a_signature_file_is_present_but_never_verified(self):
        for name in ("a.bin.sig", "A.ASC", "x.minisig"):
            self.assertEqual(delivery.signature_state(True, ["a.bin", name]), "present", name)

    def test_a_release_without_a_signature_file_is_none(self):
        self.assertEqual(delivery.signature_state(True, ["a.bin", "a.bin.sha256", "signature.txt"]), "none")
        self.assertEqual(delivery.signature_state(True, []), "none")

    def test_no_release_and_unreadable_answers(self):
        self.assertEqual(delivery.signature_state(False, []), "norelease")
        self.assertIsNone(delivery.signature_state(True, None))     # the assets were not in the answer: not verified
        self.assertIsNone(delivery.signature_state(None, None))

    def test_the_activity_query_asks_for_the_assets_and_keeps_the_state(self):
        self.assertIn("releaseAssets", charts.ACTIVITY_QUERY)
        nodes = [
            {"name": "A", "latestRelease": {"tagName": "v1", "publishedAt": "2001-01-01T00:00:00Z", "releaseAssets": {"nodes": [{"name": "a.sig"}]}}},
            {"name": "B", "latestRelease": {"tagName": "v1", "publishedAt": "2001-01-01T00:00:00Z", "releaseAssets": {"nodes": [{"name": "b.bin"}]}}},
            {"name": "C", "latestRelease": {"tagName": "v1", "publishedAt": "2001-01-01T00:00:00Z"}},
            {"name": "D", "latestRelease": None},
        ]
        found = charts.parse_activity(nodes)
        self.assertEqual([found[n].signature for n in "ABCD"], ["present", "none", None, "norelease"])

    def test_the_last_known_page_keeps_the_signature_state(self):
        html = '<script type="application/json" id="dashboard-data">' + json.dumps({"repos": {"A": {"known": True, "ci": "success", "release": {"tag": "v1", "date": "2001-01-01T00:00:00Z"}, "sig": "present"}, "B": {"known": True, "sig": "bogus"}}}) + "</script>"
        got = robust.activity_from_page(html)
        self.assertEqual(got["A"].signature, "present")
        self.assertIsNone(got["B"].signature)


class EvidenceTests(unittest.TestCase):
    MANIFEST = {"maturity": "functional", "evidence": "bench"}
    SIGNALS = {"tests": True, "ci": True, "releases": 2, "readmes": 8}

    def row(self, signature):
        out = evo.checks({"A": "urtc"}, {"A": self.MANIFEST}, {"A": self.SIGNALS}, {"A": signature})
        return out["A"][evo.ITEMS.index("signed")]

    def test_every_state_of_the_signature(self):
        self.assertEqual(self.row("present"), evo.PRESENT)
        self.assertEqual(self.row("none"), evo.NO)
        self.assertEqual(self.row("norelease"), evo.NO)
        self.assertIsNone(self.row(None))

    def test_without_signatures_nothing_is_claimed(self):
        out = evo.checks({"A": "urtc"}, {"A": self.MANIFEST}, {"A": self.SIGNALS})
        self.assertIsNone(out["A"][evo.ITEMS.index("signed")])


class ManifestFieldTests(unittest.TestCase):
    def test_known_values_only(self):
        got = delivery.manifest_fields({"built_on": "gha", "signature_kind": "release", "signed_on": "local", "last_build_artifact_url": "https://github.com/JuanenRac/X/actions/runs/1"})
        self.assertEqual(got, {"builtOn": "gha", "sigKind": "release", "signedOn": "local", "artifact": "https://github.com/JuanenRac/X/actions/runs/1"})
        bad = delivery.manifest_fields({"built_on": "docker", "signature_kind": 3, "signed_on": "cloud", "last_build_artifact_url": "javascript:alert(1)"})
        self.assertEqual(bad, {"builtOn": "", "sigKind": "", "signedOn": "", "artifact": ""})
        self.assertEqual(delivery.manifest_fields(None), {"builtOn": "", "sigKind": "", "signedOn": "", "artifact": ""})

    def test_an_address_outside_the_owner_or_with_markup_is_dropped(self):
        for url in ("https://example.com/x", "https://github.com/Other/x", 'https://github.com/JuanenRac/x"onclick=1', "https://github.com/JuanenRac/x y"):
            self.assertEqual(delivery.manifest_fields({"last_build_artifact_url": url})["artifact"], "", url)


class SchemaTests(unittest.TestCase):
    def test_the_schema_describes_the_fields_the_dashboard_reads(self):
        schema = json.loads((HERE.parent / "docs" / "evidence-schema.json").read_text(encoding="utf-8"))
        fields = schema["$defs"]["delivery_fields"]["properties"]
        self.assertEqual(set(fields), {"built_on", "last_build_artifact_url", "signature_kind", "signed_on"})
        self.assertEqual(tuple(fields["built_on"]["enum"]), delivery.BUILT_ON)
        self.assertEqual(tuple(fields["signature_kind"]["enum"]), delivery.SIGNATURE_KIND)
        self.assertEqual(tuple(fields["signed_on"]["enum"]), delivery.SIGNED_ON)
        for example in schema["$defs"]["delivery_fields"]["examples"]:
            got = delivery.manifest_fields(example)
            self.assertTrue(all(got.values()), got)


class PipelineTests(unittest.TestCase):
    def state(self, built="", kind="", signed="", release=True):
        return delivery.pipeline_state({"builtOn": built, "sigKind": kind, "signedOn": signed}, release)

    def test_the_stages(self):
        self.assertEqual(self.state(release=False), "undeclared")
        self.assertEqual(self.state(), "release_only")
        self.assertEqual(self.state(built="gha", release=False), "built")
        self.assertEqual(self.state(built="gha", kind="release", signed="local", release=False), "signed")
        self.assertEqual(self.state(built="gha", kind="release", signed="local"), "published")
        self.assertEqual(self.state(built="gha"), "published")

    def test_a_signature_that_is_none_or_of_unknown_place_is_not_a_signed_stage(self):
        self.assertEqual(self.state(kind="none", signed="local", release=False), "undeclared")
        self.assertEqual(self.state(kind="dev", signed="unknown", release=False), "undeclared")

    def test_an_unknown_release_does_not_count_as_published(self):
        self.assertEqual(delivery.pipeline_state({"builtOn": "gha"}, None), "built")


class AlertConfigTests(unittest.TestCase):
    def test_off_by_default(self):
        self.assertFalse(health.DEFAULT_CONFIG["signature_alert"]["enabled"])
        config, problems = health.parse_config({})
        self.assertEqual((config["signature_alert"], problems), ({"enabled": False, "after_days": 14}, []))

    def test_threshold_and_switch(self):
        config, problems = health.parse_config({"signature_alert": {"enabled": True, "after_days": 30}})
        self.assertEqual((config["signature_alert"], problems), ({"enabled": True, "after_days": 30}, []))

    def test_wrong_values_fall_back_and_are_named(self):
        config, problems = health.parse_config({"signature_alert": {"enabled": "yes", "after_days": 0}})
        self.assertEqual(config["signature_alert"], {"enabled": False, "after_days": 14})
        self.assertEqual(len(problems), 2)

    def test_the_real_file_keeps_the_alert_off(self):
        config, problems = health.load_config()
        self.assertEqual(problems, [])
        self.assertFalse(config["signature_alert"]["enabled"])


class TextTests(unittest.TestCase):
    def test_every_text_has_the_eight_languages(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(set(texts.TEXTS), set(texts.LANGUAGES))

    def test_every_text_the_script_uses_exists(self):
        import re
        used = set(re.findall(r'dict\.([a-z_0-9]+)', ui.JS)) | set(re.findall(r'dict\["([a-z_]+_)"', ui.JS))
        wanted = {key for key in used if key in texts.TEXTS["en"] or key.startswith(("hist_", "ev_why", "ev_sum", "pf_", "pipe_", "sig_", "alert_", "arch_", "ra_", "ts_checks"))}
        self.assertEqual([key for key in wanted if key not in texts.TEXTS["en"] and key not in sig_texts.TEXTS["en"] and key not in ("not_verified", "ev_item_", "ev_why_signed_", "ev_sum_", "pipe_", "pv_", "sig_", "sig_why_", "area_")], [])

    def test_the_pipeline_states_have_a_text_and_a_glyph(self):
        for state in ui.PIPE_STATES:
            self.assertIn("pipe_" + state, texts.TEXTS["en"])
            self.assertIn(state, ui.GLYPH)


if __name__ == "__main__":
    unittest.main()
