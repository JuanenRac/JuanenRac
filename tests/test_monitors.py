# =============================================================================
# Electro Hobby 3D - tests/test_monitors.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The monitoring scripts run against a fake GitHub: no network, no token."""
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import ci_watch  # noqa: E402
import ecosystem_inventory as inv  # noqa: E402
import health_matrix  # noqa: E402
import link_check  # noqa: E402
import release_digest  # noqa: E402

MANIFESTS = {"hydra-umc.project.json": "hydra-umc", "urtc.project.json": "urtc", "armor.project.json": "armor", "eh3d.project.json": "eh3d",
             "electro-hobby-3d.project.json": "electro-hobby-3d"}


class FakeApi:
    def __init__(self, routes):
        self.routes = routes
        self.sent = []

    def get(self, path):
        for prefix, value in self.routes.items():
            if path.startswith(prefix):
                return value(path) if callable(value) else value
        return None

    def paged(self, path):
        yield from self.get(path) or []

    def send(self, method, path, body):
        self.sent.append((method, path, body))
        return {"number": 1}


def tree(*paths):
    return {"tree": [{"path": p, "type": "blob"} for p in paths]}


class InventoryTests(unittest.TestCase):
    def test_every_repository_gets_the_ecosystem_of_its_manifest_and_its_files(self):
        api = FakeApi({
            "/users/o/repos": [{"name": "ARMOR-X", "default_branch": "main"}, {"name": "forked", "fork": True}, {"name": "random", "default_branch": "dev"}],
            "/repos/o/ARMOR-X/git/trees": tree("armor.project.json", "README.md"),
            "/repos/o/random/git/trees": tree("README.md"),
        })
        repos = inv.inventory(api, "o", MANIFESTS)
        self.assertEqual([r.name for r in repos], ["ARMOR-X", "random"])
        self.assertEqual(repos[0].ecosystem, "armor")
        self.assertIsNone(repos[1].ecosystem)
        self.assertEqual([r.name for r in inv.of_ecosystems(repos)], ["ARMOR-X"])

    def test_the_real_catalog_names_all_the_manifests(self):
        self.assertEqual(set(inv.manifest_files().values()), set(MANIFESTS.values()))

    def test_one_issue_per_report(self):
        api = FakeApi({"/repos/o/p/issues?state=open": []})
        self.assertEqual(inv.sync_issue(api, "o", "p", "lab", "T", "body"), "created")
        self.assertEqual(api.sent[-1][0], "POST")
        self.assertEqual(inv.sync_issue(api, "o", "p", "lab", "T", None), "nothing")
        api = FakeApi({"/repos/o/p/issues?state=open": [{"number": 7, "body": "same"}, {"number": 8, "body": "x", "pull_request": {}}]})
        self.assertEqual(inv.sync_issue(api, "o", "p", "lab", "T", "same"), "unchanged")
        self.assertEqual(inv.sync_issue(api, "o", "p", "lab", "T", "different"), "updated")
        self.assertEqual(api.sent[-1][1], "/repos/o/p/issues/7")
        self.assertEqual(inv.sync_issue(api, "o", "p", "lab", "T", None), "closed")
        self.assertEqual(api.sent[-1][2]["state"], "closed")


class CiWatchTests(unittest.TestCase):
    def runs(self, *items):
        return {"workflow_runs": [{"name": n, "workflow_id": hash(n.split("#")[0]) % 1000, "conclusion": c, "html_url": f"https://x/{n}", "head_sha": "abcdef123"} for n, c in items]}

    def test_the_newest_finished_run_of_each_workflow_decides(self):
        api = FakeApi({"/repos/o/r/actions/runs": self.runs(("CI", "success"), ("CI", "failure"), ("Docs", "failure"), ("Docs", "cancelled"), ("Lint", "skipped"))})
        got = ci_watch.latest_runs(api, "o", inv.Repo("r", "main", "armor"))
        self.assertEqual([(r.workflow, r.conclusion) for r in got], [("CI", "success"), ("Docs", "failure")])

    def test_an_old_run_of_the_same_workflow_under_another_name_does_not_count(self):
        # same workflow id: the newest (a success) wins over the older run that carried the file path as its name
        api = FakeApi({"/repos/o/r/actions/runs": {"workflow_runs": [
            {"name": "Pages", "workflow_id": 5, "conclusion": "success", "html_url": "u", "head_sha": "abc"},
            {"name": ".github/workflows/pages.yml", "workflow_id": 5, "conclusion": "failure", "html_url": "u", "head_sha": "abc"}]}})
        got = ci_watch.latest_runs(api, "o", inv.Repo("r", "main", "urtc"))
        self.assertEqual([(r.workflow, r.conclusion) for r in got], [("Pages", "success")])

    def test_a_red_workflow_makes_an_issue_body_and_green_makes_none(self):
        red = [ci_watch.Run("a", "armor", "CI", "failure", "u", "abc"), ci_watch.Run("b", "urtc", "CI", "success", "u", "def")]
        text, body = ci_watch.report(red, 2)
        self.assertIn("1 green, 1 red", text)
        self.assertIn("| a | armor |", body)
        self.assertNotIn("| b |", body)
        text, body = ci_watch.report(red[1:], 1)
        self.assertIsNone(body)
        self.assertIn("Everything is green", text)


class LinkCheckTests(unittest.TestCase):
    def test_links_inside_the_account_and_to_files_are_checked(self):
        repo = inv.Repo("r", "main", "armor", files={"docs/A.md", "images/b.svg", "README.md"})
        text = (
            "[ok](https://github.com/o/Other) [gone](https://github.com/o/Missing/issues) [out](https://example.com/x) "
            "[doc](docs/A.md#top) ![img](images/b.svg) [nofile](docs/Nope.md) [anchor](#here) <img src='images/none.svg'> [dir](docs)"
        )
        got = link_check.problems_in(text, "o", repo, {"other", "r"}, repo.files)
        self.assertEqual(len(got), 3, got)
        self.assertTrue(any("Missing" in p for p in got))
        self.assertTrue(any("docs/Nope.md" in p for p in got))
        self.assertTrue(any("images/none.svg" in p for p in got))

    def test_the_eight_readmes_are_read_and_a_missing_main_readme_is_reported(self):
        repo = inv.Repo("r", "main", "armor", files={"README.md", "README_spa.md"})
        pages = {"README.md": "[x](https://github.com/o/Nowhere)", "README_spa.md": "sin enlaces"}
        result = link_check.check("o", [repo], getter=lambda owner, r, name: pages.get(name), all_names={"r"})
        self.assertEqual(list(result), ["r"])
        self.assertEqual(len(result["r"]), 1)
        self.assertTrue(result["r"][0].startswith("README.md:"))
        self.assertEqual(link_check.check("o", [inv.Repo("e", "main", "armor")], getter=lambda *a: None, all_names={"e"})["e"], ["README.md: missing"])

    def test_report_is_empty_when_all_links_resolve(self):
        text, body = link_check.report({}, 3)
        self.assertIsNone(body)
        self.assertIn("resolves", text)


class ReleaseDigestTests(unittest.TestCase):
    def test_only_recent_published_releases_count(self):
        now = datetime.now(timezone.utc)
        iso = lambda days: (now - timedelta(days=days)).isoformat().replace("+00:00", "Z")  # noqa: E731
        api = FakeApi({"/repos/o/r/releases": [
            {"tag_name": "v2", "published_at": iso(1), "html_url": "u2"},
            {"tag_name": "v1", "published_at": iso(30), "html_url": "u1"},
            {"tag_name": "d", "published_at": iso(1), "draft": True},
            {"tag_name": "p", "published_at": iso(1), "prerelease": True},
        ]})
        got = release_digest.published_since(api, "o", inv.Repo("r", "main", "urtc"), now - timedelta(days=7))
        self.assertEqual([g["tag"] for g in got], ["v2"])
        text = release_digest.digest(got, 7)
        self.assertIn("### URTC", text)
        self.assertIn("[v2](u2)", text)
        self.assertIn("No release", release_digest.digest([], 7))


class HealthMatrixTests(unittest.TestCase):
    FULL = {"LICENSE", "SECURITY.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "SUPPORT.md", "CHANGELOG.md", ".github/workflows/ci.yml",
            ".github/ISSUE_TEMPLATE/bug.yml", ".github/PULL_REQUEST_TEMPLATE.md", "images/X_BANNER.svg", *health_matrix.READMES}

    def test_a_complete_repository_has_no_gap_and_a_missing_file_is_named(self):
        self.assertEqual(health_matrix.gaps(inv.Repo("a", "main", "armor", files=set(self.FULL))), [])
        partial = set(self.FULL) - {"SECURITY.md", "README_por.md", "images/X_BANNER.svg"}
        self.assertEqual(health_matrix.gaps(inv.Repo("a", "main", "armor", files=partial)), ["8 READMEs", "SECURITY.md", "a banner"])

    def test_report_lists_only_the_repositories_with_gaps(self):
        repos = [inv.Repo("good", "main", "armor", files=set(self.FULL)), inv.Repo("bad", "main", "urtc", files=set(self.FULL) - {"LICENSE"}), inv.Repo("old", "main", "urtc", archived=True)]
        text, body = health_matrix.report(repos)
        self.assertIn("| bad | urtc | licence |", body)
        self.assertNotIn("| good |", body)
        self.assertNotIn("| old |", body)
        self.assertIsNone(health_matrix.report(repos[:1])[1])


if __name__ == "__main__":
    unittest.main()
