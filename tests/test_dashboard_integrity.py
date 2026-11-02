# =============================================================================
# JuanenRac profile - tests/test_dashboard_integrity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The "Errors / unknown" count of the dashboard, with simulated repositories and a simulated GitHub."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import dashboard_integrity as di  # noqa: E402

GOOD = {"maturity": "functional", "evidence": "host-test"}


def evaluate(**kwargs):
    base = dict(catalog={}, listed={}, discovery_errors=[], raw_manifests={}, owner_repos=[], api_failures=[])
    base.update(kwargs)
    return di.evaluate(**base)


def kinds(issues):
    return sorted((issue.kind, issue.repo) for issue in issues)


class EvaluateTests(unittest.TestCase):
    def test_nothing_wrong_gives_no_issue(self):
        issues = evaluate(catalog={"urtc": ["URTC-A"]}, listed={"URTC-A": "urtc"}, owner_repos=["URTC-A"],
                          raw_manifests={"URTC-A": di.RawManifest("urtc", GOOD)})
        self.assertEqual(issues, [])
        self.assertEqual(di.report(issues).split()[0], "INTEGRITY=OK")

    def test_a_catalogue_repository_missing_from_the_dashboard(self):
        issues = evaluate(catalog={"armor": ["ARMOR-A", "ARMOR-B"]}, listed={"ARMOR-A": "armor"}, owner_repos=["ARMOR-A", "ARMOR-B"],
                          raw_manifests={"ARMOR-A": di.RawManifest("armor", GOOD)})
        self.assertEqual(kinds(issues), [("catalog_missing", "ARMOR-B")])
        self.assertTrue(issues[0].in_catalog)
        self.assertEqual(di.blocking(issues), issues)

    def test_a_catalogue_repository_that_does_not_exist(self):
        issues = evaluate(catalog={"armor": ["ARMOR-GONE"]}, owner_repos=["ARMOR-A"])
        self.assertIn("not among the public repositories", issues[0].detail)

    def test_an_unreadable_manifest_is_named_once_with_its_reason(self):
        issues = evaluate(catalog={"eh3d": ["EH3D-X"]}, owner_repos=["EH3D-X"],
                          discovery_errors=["EH3D-X: invalid manifest: depends_on must be a list"],
                          raw_manifests={"EH3D-X": di.RawManifest("eh3d", {"maturity": "functional"})})
        self.assertEqual(kinds(issues), [("invalid_manifest", "EH3D-X")])
        self.assertIn("depends_on", issues[0].detail)
        self.assertTrue(issues[0].in_catalog)

    def test_a_manifest_the_dashboard_did_not_list_and_nobody_explained(self):
        issues = evaluate(owner_repos=["HYDRA-UMC-NEW"], raw_manifests={"HYDRA-UMC-NEW": di.RawManifest("hydra-umc", GOOD)})
        self.assertEqual(kinds(issues), [("unlisted_manifest", "HYDRA-UMC-NEW")])
        self.assertFalse(issues[0].in_catalog)
        self.assertEqual(di.blocking(issues), [])

    def test_an_unknown_maturity_and_an_unknown_evidence(self):
        issues = evaluate(listed={"A": "eh3d", "B": "eh3d", "C": "eh3d"}, owner_repos=["A", "B", "C"], raw_manifests={
            "A": di.RawManifest("eh3d", {"evidence": "host-test"}),                       # no maturity
            "B": di.RawManifest("eh3d", {"maturity": "beta", "evidence": "hardware"}),    # both outside the vocabulary
            "C": di.RawManifest("eh3d", GOOD),
        })
        self.assertEqual(kinds(issues), [("unknown_evidence", "B"), ("unknown_maturity", "A"), ("unknown_maturity", "B")])
        self.assertIn("missing", issues[0].detail)
        self.assertIn("'beta'", issues[1].detail)

    def test_every_known_value_is_accepted(self):
        raw = {f"R{i}-{j}": di.RawManifest("urtc", {"maturity": m, "evidence": e})
               for i, m in enumerate(di.MATURITIES) for j, e in enumerate(di.EVIDENCES)}
        self.assertEqual(evaluate(listed={name: "urtc" for name in raw}, raw_manifests=raw, owner_repos=list(raw)), [])

    def test_a_discovery_failure_that_names_no_repository_is_an_api_failure(self):
        issues = evaluate(discovery_errors=["unable to list GitHub repositories for JuanenRac: HTTP 403 rate limit"])
        self.assertEqual(kinds(issues), [("api", "discovery")])
        self.assertEqual(di.blocking(issues), issues)

    def test_api_failures_are_carried(self):
        issues = evaluate(api_failures=[("repository list", "HTTP 502 listing page 2")])
        self.assertEqual(kinds(issues), [("api", "repository list")])

    def test_counts_by_ecosystem(self):
        issues = evaluate(catalog={"urtc": ["U1"], "armor": ["A1", "A2"]}, owner_repos=[])
        counts = di.counts_by_ecosystem(issues, ["hydra-umc", "urtc", "armor"])
        self.assertEqual((counts["urtc"], counts["armor"], counts["hydra-umc"]), (1, 2, 0))


class GatherTests(unittest.TestCase):
    """`gather` against a simulated GitHub, including a second page of the repository list."""

    def run_gather(self, files, listing, listed=None, failing=()):
        calls = []

        def fetch(repo, branch, file):
            calls.append((repo, file))
            if (repo, file) in failing:
                return "error", "HTTP 500"
            if (repo, file) in files:
                return "ok", files[(repo, file)]
            return "absent", None

        return di.gather(owner="o", listed=listed or {}, list_repos=lambda: listing, fetch=fetch), calls

    def test_a_repository_of_the_second_page_with_a_manifest_is_found(self):
        page_one = [(f"R{i}", "main") for i in range(100)]
        listing = (page_one + [("HYDRA-UMC-LATE", "main")], "")
        (raw, owner, failures), _ = self.run_gather({("HYDRA-UMC-LATE", "hydra-umc.project.json"): GOOD}, listing)
        self.assertEqual(list(raw), ["HYDRA-UMC-LATE"])
        self.assertEqual(len(owner), 101)
        self.assertEqual(failures, [])
        issues = evaluate(raw_manifests=raw, owner_repos=owner)
        self.assertEqual(kinds(issues), [("unlisted_manifest", "HYDRA-UMC-LATE")])

    def test_a_failed_listing_is_reported_and_the_owner_list_is_unknown(self):
        (raw, owner, failures), _ = self.run_gather({}, ([("A", "main")], "HTTP 502 listing page 2"))
        self.assertIsNone(owner)
        self.assertEqual(failures[0][0], "repository list")
        issues = evaluate(catalog={"urtc": ["U1"]}, owner_repos=owner, api_failures=failures)
        self.assertEqual({issue.kind for issue in issues}, {"catalog_missing", "api"})

    def test_a_manifest_that_cannot_be_read_is_an_api_failure_and_not_an_absence(self):
        (raw, owner, failures), _ = self.run_gather({}, ([("A", "main")], ""), failing={("A", "hydra-umc.project.json")})
        self.assertEqual(raw, {})
        self.assertEqual(failures[0][0], "A")
        self.assertIn("HTTP 500", failures[0][1])

    def test_a_listed_repository_reads_only_the_file_of_its_ecosystem(self):
        (raw, _, _), calls = self.run_gather({("U", "urtc.project.json"): GOOD}, ([("U", "main")], ""), listed={"U": "urtc"})
        self.assertEqual(calls, [("U", "urtc.project.json")])
        self.assertEqual(raw["U"].ecosystem, "urtc")

    def test_a_repository_without_any_manifest_is_not_a_problem_by_itself(self):
        (raw, owner, failures), calls = self.run_gather({}, ([("PLAIN", "main")], ""))
        self.assertEqual((raw, failures), ({}, []))
        self.assertEqual(len(calls), len(di.MANIFEST_FILES))
        self.assertEqual(evaluate(raw_manifests=raw, owner_repos=owner), [])


class CoverageTests(unittest.TestCase):
    """The count is the number of public repositories that carry a manifest - never a number written in the code."""

    def test_the_listed_count_follows_the_manifests_found(self):
        listed = {"HYDRA-UMC-A": "hydra-umc", "ARMOR-A": "armor", "EH3D-A": "eh3d"}
        owner = ["HYDRA-UMC-A", "ARMOR-A", "EH3D-A", "JuanenRac", "NOTES"]
        raw = {name: di.RawManifest(eco, GOOD) for name, eco in listed.items()}
        cover = di.coverage(listed, owner, raw)
        self.assertEqual((cover.listed, cover.public), (3, 5))
        self.assertEqual(cover.without_manifest, ("JuanenRac", "NOTES"))
        # one more repository with a manifest changes the count without touching any number in the code
        listed["URTC-A"] = "urtc"
        owner.append("URTC-A")
        raw["URTC-A"] = di.RawManifest("urtc", GOOD)
        cover = di.coverage(listed, owner, raw)
        self.assertEqual((cover.listed, cover.public, len(cover.without_manifest)), (4, 6, 2))

    def test_a_repository_with_a_manifest_the_dashboard_lost_is_not_called_manifest_free(self):
        owner = ["LOST", "PLAIN"]
        raw = {"LOST": di.RawManifest("eh3d", GOOD)}
        cover = di.coverage({}, owner, raw)
        self.assertEqual(cover.without_manifest, ("PLAIN",))
        self.assertEqual(kinds(evaluate(owner_repos=owner, raw_manifests=raw)), [("unlisted_manifest", "LOST")])

    def test_an_unknown_listing_gives_no_count(self):
        self.assertIsNone(di.coverage({"A": "urtc"}, None, {}).public)


class LenientParsingTests(unittest.TestCase):
    """The dashboard keeps a repository whose manifest only carries what the pinned updater does not know."""

    def setUp(self):
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
            import generate_dashboard  # noqa: F401
        except Exception as exc:  # the updater packages are installed in CI only
            self.skipTest(f"generator not importable here: {exc}")
        self.gd = generate_dashboard

    def manifest(self, **extra):
        data = {"schema_version": "1.0", "ecosystem": "HYDRA-UMC", "name": "HYDRA-UMC-X", "version": "0.0.1", "role": "library", "stack": "python",
                "technologies": ["Python"], "deployment_target": "user-pc", "maturity": "scaffolding", "family": "F", "parent": None,
                "build": "b", "notes": "n", "native_version": {"file": "VERSION", "pattern": "^([0-9]+)[.]([0-9]+)[.]([0-9]+)"}}
        data.update(extra)
        return data

    def test_unknown_fields_and_a_later_schema_revision_are_set_aside(self):
        parsed = self.gd.parse_leniently(self.manifest(schema_version="1.1", some_new_field=1, depends_on=["EH3D-A"]), "HYDRA-UMC-X")
        self.assertEqual(parsed.version, "0.0.1")

    def test_a_manifest_that_is_wrong_in_what_is_shown_still_fails(self):
        with self.assertRaises(Exception):
            self.gd.parse_leniently(self.manifest(maturity="beta"), "HYDRA-UMC-X")


class TextsTests(unittest.TestCase):
    def test_every_text_exists_in_the_eight_languages(self):
        import dashboard_texts
        self.assertEqual(dashboard_texts.problems(), [])
        self.assertEqual(set(dashboard_texts.TEXTS), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})
        for kind in dashboard_texts.INTEGRITY_KINDS:
            self.assertIn(f"integrity_kind_{kind}", dashboard_texts.TEXTS["en"])
        for key in dashboard_texts.EVIDENCE_KEYS:
            self.assertIn(f"evidence_desc_{key}", dashboard_texts.TEXTS["pt"])


if __name__ == "__main__":
    unittest.main()
