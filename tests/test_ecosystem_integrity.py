# =============================================================================
# JuanenRac profile - tests/test_ecosystem_integrity.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The reconciliation of inventory, manifests, README (8 languages), catalogue, dashboard and progress, and the rules every manifest must follow."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import ecosystem_integrity_test as it  # noqa: E402
import ecosystem_progress as progress  # noqa: E402

ECOS4 = ("hydra-umc", "urtc", "armor", "eh3d")
PREFIX = {"hydra-umc": "HYDRA-UMC", "urtc": "URTC", "armor": "ARMOR", "eh3d": "EH3D", "electro-hobby-3d": "TOOLS"}
LABEL = {"hydra-umc": "HYDRA-UMC", "urtc": "URTC", "armor": "A.R.M.O.R.", "eh3d": "EH3D", "electro-hobby-3d": "ELECTRO-HOBBY-3D"}
CATALOG = {"ecosystems": [
    {"key": "hydra-umc", "label": "HYDRA-UMC", "manifest_file": "hydra-umc.project.json"},
    {"key": "urtc", "label": "URTC", "manifest_file": "urtc.project.json"},
    {"key": "armor", "label": "A.R.M.O.R.", "manifest_file": "armor.project.json"},
    {"key": "eh3d", "label": "EH3D", "manifest_file": "eh3d.project.json"},
    {"key": "electro-hobby-3d", "label": "Electro Hobby 3D", "manifest_file": "electro-hobby-3d.project.json"},
]}


def names_of(eco, n=2):
    return [f"{PREFIX[eco]}-ITEM-{i}" for i in range(n)]


def manifest(eco, name, **extra):
    data = {"name": name, "ecosystem": LABEL[eco], "family": "Core", "role": "library", "maturity": "functional", "evidence": "bench", "version": "0.1.0", "parent": None}
    data.update(extra)
    return data


def readme(file, rows):
    out = ["# Title", ""]
    for eco in rows:
        out += [f"# Section {eco}", f"<!-- progress:{eco} -->", "`[███░░] 10%` — " + progress.TEXT[file].format(n=len(rows[eco])), f"<!-- /progress:{eco} -->",
                "| Repository | Version | Description |", "| --- | --- | --- |"]
        out += [f"| [{n}](https://github.com/JuanenRac/{n}) | {v} | text |" for n, v in rows[eco].items()]
        out.append("")
    return "\n".join(out)


def repo_page(name, eco, version="0.1.0", release="v0.1.0"):
    return {"eco": eco, "version": version, "release": {"tag": release, "date": "2001-01-01"} if release else None}


def good_sources():
    repos, manifests, rows, page = [it.RepoInfo("JuanenRac")], {"JuanenRac": it.ManifestRead("absent")}, {}, {}
    for eco in ECOS4:
        rows[eco] = {}
        for n in names_of(eco):
            repos.append(it.RepoInfo(n))
            manifests[n] = it.ManifestRead("ok", eco, manifest(eco, n))
            rows[eco][n] = "0.1.0"
            page[n] = repo_page(n, eco)
    readmes = {f: readme(f, rows) for f in progress.README_FILES}
    history = {"entries": [{"date": "2001-01-01", "repos": {n: [2, "0.1.0"] for n in page}}]}
    return it.Sources("JuanenRac", repos, manifests, readmes, CATALOG, {"repos": page}, (), (len(page), len(page) + 1), history)


def states(report, check=None, subject=None):
    return [(f.check, f.state, f.subject) for f in report.findings if (check is None or f.check == check) and (subject is None or f.subject == subject)]


class ConsistentWorldTests(unittest.TestCase):
    def test_everything_agrees(self):
        report = it.reconcile(good_sources())
        self.assertEqual(report.by_state(it.FAILED), [], report.by_state(it.FAILED))
        self.assertEqual(report.by_state(it.UNVERIFIED), [])
        self.assertEqual(report.verdict, "CONSISTENT")
        self.assertEqual(report.exit_code, 0)

    def test_the_figures_explain_each_number(self):
        report = it.reconcile(good_sources())
        figures = {f.label: f for f in report.figures}
        self.assertEqual(figures["Public repositories"].value, "9")
        self.assertEqual(figures["Projects"].value, "8")
        self.assertIn("JuanenRac (profile repository)", figures["Projects"].why)
        self.assertEqual(figures["Valid manifests"].value, "8 of 8")
        self.assertEqual(figures["Listed by the dashboard"].value, "8 of 8")
        self.assertEqual(figures["URTC"].value, "2")
        self.assertIn("2 in the README catalogue", figures["URTC"].why)

    def test_text_and_markdown_reports_carry_the_figures_and_the_verdict(self):
        report = it.reconcile(good_sources())
        text, md = it.render_text(report), it.render_markdown(report)
        for fragment in ("ECOSYSTEM INTEGRITY: CONSISTENT", "Projects: 8", "Valid manifests: 8 of 8"):
            self.assertIn(fragment, text)
        self.assertIn("### Figures and where they come from", md)
        self.assertNotIn("### Findings that need attention", md)
        self.assertEqual(it.to_json(report)["exit_code"], 0)


class NeverHealthyWhenNotVerifiedTests(unittest.TestCase):
    def test_a_listing_failure_is_unverified_not_healthy(self):
        src = good_sources()
        src.repos, src.errors = None, {"listing": "HTTP 502 listing page 1"}
        report = it.reconcile(src)
        self.assertIn(("inventory", it.UNVERIFIED, "JuanenRac"), states(report))
        self.assertNotEqual(report.verdict, "CONSISTENT")
        self.assertTrue(report.verdict.startswith("INCOMPLETE"))
        self.assertEqual(report.by_state(it.FAILED), [])
        self.assertEqual(it.reconcile(src).figures[0].value, "not verified")

    def test_one_unreadable_manifest_is_unverified_and_the_count_says_or_more(self):
        src = good_sources()
        src.manifests["URTC-ITEM-0"] = it.ManifestRead("error", detail="HTTP 503")
        report = it.reconcile(src)
        self.assertIn(("manifest-read", it.UNVERIFIED, "URTC-ITEM-0"), states(report))
        self.assertEqual(report.exit_code, 0)
        self.assertTrue(report.verdict.startswith("INCOMPLETE"))
        projects = next(f for f in report.figures if f.label == "Projects")
        self.assertIn("could not be checked", projects.why)
        # nothing is said about its fields or its dependencies
        self.assertEqual(states(report, "manifest-fields", "URTC-ITEM-0"), [])

    def test_the_dashboard_that_cannot_be_read_is_unverified(self):
        src = good_sources()
        src.dashboard, src.errors = None, {"dashboard": "no such file"}
        report = it.reconcile(src)
        self.assertIn(("dashboard", it.UNVERIFIED, "docs/index.html"), states(report))
        self.assertIn(("version", it.UNVERIFIED, "URTC-ITEM-0"), states(report))
        self.assertTrue(report.verdict.startswith("INCOMPLETE"))

    def test_nothing_verified_at_all_exits_2(self):
        report = it.Report([it.Finding("inventory", it.UNVERIFIED, "x", "down")], [])
        self.assertEqual(report.exit_code, 2)

    def test_missing_history_and_catalogue_are_unverified(self):
        src = good_sources()
        src.history, src.catalog_json, src.errors = None, None, {"history": "gone", "catalog": "gone"}
        report = it.reconcile(src)
        self.assertIn(("history", it.UNVERIFIED, "data/history.json"), states(report))
        self.assertIn(("catalog-json", it.UNVERIFIED, "ecosystem-catalog.json"), states(report))


class ManifestRulesTests(unittest.TestCase):
    def test_a_name_that_is_not_the_repository_fails(self):
        src = good_sources()
        src.manifests["ARMOR-ITEM-0"] = it.ManifestRead("ok", "armor", manifest("armor", "ARMOR-OTHER"))
        report = it.reconcile(src)
        self.assertEqual(states(report, "manifest-fields", "ARMOR-ITEM-0")[0][1], it.FAILED)
        self.assertEqual(report.exit_code, 1)

    def test_the_declared_ecosystem_must_match_the_file(self):
        src = good_sources()
        src.manifests["ARMOR-ITEM-0"] = it.ManifestRead("ok", "armor", manifest("armor", "ARMOR-ITEM-0", ecosystem="URTC"))
        self.assertEqual(states(it.reconcile(src), "manifest-fields", "ARMOR-ITEM-0")[0][1], it.FAILED)

    def test_ecosystem_names_compare_without_punctuation(self):
        self.assertEqual(it._plain("A.R.M.O.R."), it._plain("ARMOR"))
        self.assertEqual(it._plain("ELECTRO-HOBBY-3D"), it._plain("Electro Hobby 3D"))

    def test_family_role_maturity_evidence_and_version_are_required(self):
        for field, value in (("family", ""), ("role", None), ("maturity", "great"), ("evidence", "none?"), ("version", "latest")):
            src = good_sources()
            data = manifest("urtc", "URTC-ITEM-0")
            data[field] = value
            src.manifests["URTC-ITEM-0"] = it.ManifestRead("ok", "urtc", data)
            self.assertEqual(states(it.reconcile(src), "manifest-fields", "URTC-ITEM-0")[0][1], it.FAILED, field)

    def test_the_parent_must_exist(self):
        src = good_sources()
        src.manifests["URTC-ITEM-1"] = it.ManifestRead("ok", "urtc", manifest("urtc", "URTC-ITEM-1", parent="URTC-NOPE"))
        self.assertEqual(states(it.reconcile(src), "manifest-fields", "URTC-ITEM-1")[0][1], it.FAILED)
        src.manifests["URTC-ITEM-1"] = it.ManifestRead("ok", "urtc", manifest("urtc", "URTC-ITEM-1", parent="URTC-ITEM-0"))
        self.assertEqual(states(it.reconcile(src), "manifest-fields", "URTC-ITEM-1")[0][1], it.OK)

    def test_depends_on_must_name_existing_repositories(self):
        src = good_sources()
        src.manifests["EH3D-ITEM-0"] = it.ManifestRead("ok", "eh3d", manifest("eh3d", "EH3D-ITEM-0", depends_on=["EH3D-ITEM-1", "ARMOR-ITEM-0"]))
        self.assertEqual(states(it.reconcile(src), "depends-on", "EH3D-ITEM-0")[0][1], it.OK)
        src.manifests["EH3D-ITEM-0"] = it.ManifestRead("ok", "eh3d", manifest("eh3d", "EH3D-ITEM-0", depends_on=["EH3D-GHOST"]))
        out = it.reconcile(src)
        self.assertEqual(states(out, "depends-on", "EH3D-ITEM-0")[0][1], it.FAILED)
        self.assertIn("EH3D-GHOST", [f.detail for f in out.findings if f.check == "depends-on"][0])

    def test_a_dependency_on_an_empty_repository_is_pending_and_on_itself_fails(self):
        src = good_sources()
        src.repos.append(it.RepoInfo("EH3D-PLAN", empty=True))
        src.manifests["EH3D-PLAN"] = it.ManifestRead("absent")
        src.manifests["EH3D-ITEM-0"] = it.ManifestRead("ok", "eh3d", manifest("eh3d", "EH3D-ITEM-0", depends_on=["EH3D-PLAN"]))
        self.assertEqual(states(it.reconcile(src), "depends-on", "EH3D-ITEM-0")[0][1], it.PENDING)
        src.manifests["EH3D-ITEM-0"] = it.ManifestRead("ok", "eh3d", manifest("eh3d", "EH3D-ITEM-0", depends_on=["EH3D-ITEM-0"]))
        self.assertEqual(states(it.reconcile(src), "depends-on", "EH3D-ITEM-0")[0][1], it.FAILED)

    def test_an_invalid_manifest_and_two_manifests_fail(self):
        src = good_sources()
        src.manifests["URTC-ITEM-0"] = it.ManifestRead("invalid", "urtc", None, "the manifest is not a JSON object")
        src.manifests["URTC-ITEM-1"] = it.ManifestRead("ok", "urtc", manifest("urtc", "URTC-ITEM-1"), also=("armor",))
        report = it.reconcile(src)
        self.assertEqual(states(report, "manifest-read", "URTC-ITEM-0")[0][1], it.FAILED)
        self.assertEqual(states(report, "manifest-read", "URTC-ITEM-1")[0][1], it.FAILED)


class VersionTests(unittest.TestCase):
    def test_manifest_and_version_file_must_agree(self):
        src = good_sources()
        src.dashboard["repos"]["ARMOR-ITEM-0"]["version"] = "0.0.9"
        self.assertEqual(states(it.reconcile(src), "version", "ARMOR-ITEM-0")[0][1], it.FAILED)

    def test_trailing_zeros_do_not_matter(self):
        src = good_sources()
        src.dashboard["repos"]["ARMOR-ITEM-0"]["version"] = "0.1.0.0"
        self.assertEqual(states(it.reconcile(src), "version", "ARMOR-ITEM-0")[0][1], it.OK)

    def test_the_readme_table_must_agree(self):
        src = good_sources()
        src.readmes["README.md"] = src.readmes["README.md"].replace("| [ARMOR-ITEM-1](https://github.com/JuanenRac/ARMOR-ITEM-1) | 0.1.0 |", "| [ARMOR-ITEM-1](https://github.com/JuanenRac/ARMOR-ITEM-1) | 0.0.5 |")
        report = it.reconcile(src)
        self.assertEqual(states(report, "version", "ARMOR-ITEM-1")[0][1], it.FAILED)

    def test_a_release_older_than_the_version_is_pending_and_newer_fails(self):
        src = good_sources()
        src.dashboard["repos"]["URTC-ITEM-0"]["release"]["tag"] = "v0.0.9"
        self.assertEqual(states(it.reconcile(src), "version", "URTC-ITEM-0")[0][1], it.PENDING)
        src.dashboard["repos"]["URTC-ITEM-0"]["release"]["tag"] = "v0.2.0"
        self.assertEqual(states(it.reconcile(src), "version", "URTC-ITEM-0")[0][1], it.FAILED)

    def test_no_release_and_unread_version_file(self):
        src = good_sources()
        src.dashboard["repos"]["URTC-ITEM-0"]["release"] = None
        self.assertEqual(states(it.reconcile(src), "version", "URTC-ITEM-0")[0][1], it.OK)
        src.dashboard["repos"]["URTC-ITEM-0"]["version"] = None
        self.assertEqual(states(it.reconcile(src), "version", "URTC-ITEM-0")[0][1], it.UNVERIFIED)


class ReadmeAndCatalogueTests(unittest.TestCase):
    def test_a_translation_with_a_different_catalogue_fails(self):
        src = good_sources()
        text = src.readmes["README_por.md"]
        src.readmes["README_por.md"] = "\n".join(line for line in text.splitlines() if "URTC-ITEM-1" not in line)
        report = it.reconcile(src)
        self.assertEqual(states(report, "readme-parity", "README_por.md")[0][1], it.FAILED)
        self.assertEqual(states(report, "readme-parity", "README_jpn.md")[0][1], it.OK)

    def test_a_progress_sentence_with_a_wrong_count_fails_in_any_language(self):
        for file in progress.README_FILES:
            src = good_sources()
            src.readmes[file] = src.readmes[file].replace(progress.TEXT[file].format(n=2), progress.TEXT[file].format(n=3), 1)
            self.assertEqual(states(it.reconcile(src), "progress-count", file)[0][1], it.FAILED, file)

    def test_a_missing_translation_is_unverified(self):
        src = good_sources()
        del src.readmes["README_zho.md"]
        self.assertEqual(states(it.reconcile(src), "readme-parity", "README_zho.md")[0][1], it.UNVERIFIED)

    def test_a_manifest_the_catalogue_does_not_list_fails(self):
        src = good_sources()
        src.repos.append(it.RepoInfo("URTC-NEW"))
        src.manifests["URTC-NEW"] = it.ManifestRead("ok", "urtc", manifest("urtc", "URTC-NEW"))
        src.dashboard["repos"]["URTC-NEW"] = repo_page("URTC-NEW", "urtc")
        self.assertEqual(states(it.reconcile(src), "readme-catalogue", "URTC-NEW")[0][1], it.FAILED)

    def test_the_updater_of_the_suite_counts_in_the_tools_section(self):
        src = good_sources()
        name = "ELECTRO-HOBBY-3D-UPDATER"
        src.repos.append(it.RepoInfo(name))
        src.manifests[name] = it.ManifestRead("ok", "electro-hobby-3d", manifest("eh3d", name, ecosystem="ELECTRO-HOBBY-3D"))
        src.dashboard["repos"][name] = repo_page(name, "electro-hobby-3d")
        src.dashboard_cover = (9, 10)
        for file in progress.README_FILES:
            rows = {eco: {n: "0.1.0" for n in names_of(eco)} for eco in ECOS4}
            rows["electro-hobby-3d"] = {name: "0.1.0"}
            src.readmes[file] = readme(file, rows)
        report = it.reconcile(src)
        self.assertEqual(report.by_state(it.FAILED), [], report.by_state(it.FAILED))

    def test_catalogue_entry_of_an_empty_repository_is_pending_and_of_a_ghost_fails(self):
        src = good_sources()
        src.repos.append(it.RepoInfo("EH3D-SOON", empty=True))
        src.manifests["EH3D-SOON"] = it.ManifestRead("absent")
        for file in progress.README_FILES:
            rows = {eco: {n: "0.1.0" for n in names_of(eco)} for eco in ECOS4}
            rows["eh3d"]["EH3D-SOON"] = "-"
            rows["eh3d"]["EH3D-GHOST"] = "-"
            src.readmes[file] = readme(file, rows)
        report = it.reconcile(src)
        self.assertEqual(states(report, "readme-catalogue", "EH3D-SOON")[0][1], it.PENDING)
        self.assertEqual(states(report, "readme-catalogue", "EH3D-GHOST")[0][1], it.FAILED)

    def test_catalog_json_is_checked_against_the_dashboard(self):
        src = good_sources()
        src.catalog_json = copy.deepcopy(CATALOG)
        src.catalog_json["ecosystems"][1]["manifest_file"] = "other.json"
        self.assertEqual(states(it.reconcile(src), "catalog-json")[0][1], it.FAILED)
        src.catalog_json = {"ecosystems": CATALOG["ecosystems"][:2]}
        self.assertEqual(states(it.reconcile(src), "catalog-json")[0][1], it.FAILED)


class DashboardTests(unittest.TestCase):
    def test_a_valid_manifest_missing_from_the_dashboard_fails_with_the_reason_of_the_page(self):
        src = good_sources()
        del src.dashboard["repos"]["HYDRA-UMC-ITEM-1"]
        src.dashboard_issues = (("HYDRA-UMC-ITEM-1", "invalid_manifest", "unknown field(s) in service: grpc_port"),)
        report = it.reconcile(src)
        found = [f for f in report.findings if f.check == "dashboard" and f.subject == "HYDRA-UMC-ITEM-1"]
        self.assertEqual(found[0].state, it.FAILED)
        self.assertIn("grpc_port", found[0].detail)
        figures = {f.label: f for f in report.figures}
        self.assertEqual(figures["Valid manifests"].value, "8 of 8")
        self.assertEqual(figures["Listed by the dashboard"].value, "7 of 8")
        self.assertIn("HYDRA-UMC-ITEM-1 (unknown field(s) in service: grpc_port)", figures["Listed by the dashboard"].why)

    def test_a_listed_repository_that_vanished_or_is_in_the_wrong_ecosystem_fails(self):
        src = good_sources()
        src.dashboard["repos"]["GONE"] = repo_page("GONE", "urtc")
        src.dashboard["repos"]["URTC-ITEM-0"]["eco"] = "armor"
        report = it.reconcile(src)
        self.assertEqual(states(report, "dashboard", "GONE")[0][1], it.FAILED)
        self.assertEqual(states(report, "dashboard", "URTC-ITEM-0")[0][1], it.FAILED)

    def test_the_count_the_page_states_must_match_its_data(self):
        src = good_sources()
        src.dashboard_cover = (99, 100)
        self.assertTrue(any(f.state == it.FAILED and f.check == "dashboard" for f in it.reconcile(src).findings))

    def test_history_differences_are_pending_not_failed(self):
        src = good_sources()
        del src.history["entries"][0]["repos"]["URTC-ITEM-0"]
        report = it.reconcile(src)
        self.assertEqual(states(report, "history")[0][1], it.PENDING)
        self.assertEqual(report.by_state(it.FAILED), [])

    def test_the_page_is_read_for_data_issues_and_coverage(self):
        html = ('<p data-listed="126" data-public="129"></p><ul class="integrity-list">'
                '<li><code>X-1</code> <span class="integrity-kind" data-i18n="integrity_kind_invalid_manifest">invalid_manifest</span> <span class="integrity-eco">URTC</span> '
                '<span class="integrity-detail">bad &amp; broken</span></li></ul>'
                '<script type="application/json" id="dashboard-data">{"repos": {"A": {}}}</script>')
        data, issues, cover = it.page_sources(html)
        self.assertEqual(data["repos"], {"A": {}})
        self.assertEqual(issues, (("X-1", "invalid_manifest", "bad &amp; broken"),))
        self.assertEqual(cover, (126, 129))
        self.assertEqual(it.page_sources("<html></html>"), (None, (), None))
        self.assertEqual(it.page_sources('<script type="application/json" id="dashboard-data">{broken</script>')[0], None)


class CollectTests(unittest.TestCase):
    def test_collect_reads_every_source_and_never_hides_a_failed_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "docs").mkdir()
            (root / "ecosystem-catalog.json").write_text(json.dumps(CATALOG), encoding="utf-8")
            (root / "data" / "history.json").write_text("{not json", encoding="utf-8")

            repos = [it.RepoInfo("A", "main"), it.RepoInfo("B", "main"), it.RepoInfo("C", "main"), it.RepoInfo("D", "main", empty=True), it.RepoInfo("E", "main")]

            def fetch(repo, branch, file):
                table = {("A", "urtc.project.json"): ("ok", {"name": "A"}), ("B", "urtc.project.json"): ("ok", {"name": "B"}),
                         ("B", "armor.project.json"): ("ok", {"name": "B"}), ("C", "urtc.project.json"): ("error", "HTTP 500"),
                         ("E", "eh3d.project.json"): ("ok", ["not", "an", "object"])}
                return table.get((repo, file), ("absent", None))

            src = it.collect("JuanenRac", "", lambda: (repos, ""), fetch, root=root)
            self.assertEqual(src.manifests["A"].status, "ok")
            self.assertEqual(src.manifests["A"].ecosystem, "urtc")
            self.assertEqual(src.manifests["B"].also, ("armor",))
            self.assertEqual(src.manifests["C"].status, "error")
            self.assertEqual(src.manifests["D"].status, "absent")
            self.assertEqual(src.manifests["E"].status, "invalid")
            self.assertIsNone(src.history)
            self.assertIn("history", src.errors)
            self.assertIn("dashboard", src.errors)
            self.assertEqual(src.readmes, {})
            report = it.reconcile(src)
            self.assertIn(("manifest-read", it.UNVERIFIED, "C"), states(report))
            self.assertIn(("manifest-read", it.PENDING, "D"), states(report))
            self.assertEqual(report.exit_code, 1)

    def test_a_failed_listing_gives_no_repositories(self):
        src = it.collect("JuanenRac", "", lambda: ([], "HTTP 403"), lambda *a: ("absent", None), root=Path(tempfile.gettempdir()) / "t19_nowhere")
        self.assertIsNone(src.repos)
        self.assertEqual(src.errors["listing"], "HTTP 403")


class TheRealRepositoryTests(unittest.TestCase):
    """The files of this repository itself, offline."""

    def test_the_readme_files_parse_and_agree_with_each_other(self):
        root = HERE.parent
        readmes = {f: (root / f).read_text(encoding="utf-8") for f in progress.README_FILES}
        base = it.catalogue_rows(readmes["README.md"])
        self.assertTrue(all(base[eco] for eco in ECOS4))
        for file, text in readmes.items():
            rows = it.catalogue_rows(text)
            for eco in ECOS4:
                self.assertEqual(set(rows[eco]), set(base[eco]), f"{file} {eco}")
            counts = it.progress_counts(file, text)
            for eco in ECOS4:
                self.assertEqual(counts[eco], len(base[eco]), f"{file} {eco}")


if __name__ == "__main__":
    unittest.main()
