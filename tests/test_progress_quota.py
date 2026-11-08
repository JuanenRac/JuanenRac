# =============================================================================
# JuanenRac profile - tests/test_progress_quota.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The progress bars and the status rows when the quota of the GitHub API is spent: they keep their last values and the build goes on; any other failure still stops it."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import ecosystem_progress as progress  # noqa: E402
import ecosystem_status as status  # noqa: E402
import gh_http  # noqa: E402


class Fake:
    """Replaces a module attribute for the length of a test."""

    def __init__(self, target, name, value):
        self.target, self.name, self.value = target, name, value

    def __enter__(self):
        self.old = getattr(self.target, self.name)
        setattr(self.target, self.name, self.value)

    def __exit__(self, *_):
        setattr(self.target, self.name, self.old)


def raiser(quota):
    def run(*_args, **_kwargs):
        raise progress.FactsUnavailable("ERROR: the delivery and quality facts could not be read for 128 of 128 repositories; nothing written", quota)
    return run


class SpentQuotaTests(unittest.TestCase):
    def test_a_spent_quota_keeps_the_last_bars_and_does_not_stop_the_build(self):
        with Fake(progress, "compute", raiser(True)):
            self.assertEqual(progress.main([]), 0)

    def test_any_other_failure_still_stops_the_build(self):
        with Fake(progress, "compute", raiser(False)):
            with self.assertRaises(progress.FactsUnavailable):
                progress.main([])

    def test_the_same_for_the_status_rows(self):
        with Fake(status, "compute", raiser(True)):
            self.assertEqual(status.main([]), 0)
        with Fake(status, "compute", raiser(False)):
            with self.assertRaises(progress.FactsUnavailable):
                status.main([])

    def test_the_failure_is_a_system_exit_with_its_message(self):
        error = progress.FactsUnavailable("ERROR: x", True)
        self.assertIsInstance(error, SystemExit)
        self.assertTrue(error.quota)
        self.assertEqual(str(error), "ERROR: x")

    def test_too_many_unreadable_repositories_raise_with_the_quota_flag(self):
        repos = {"hydra-umc": ["A"], "urtc": ["B"], "armor": ["C"], "eh3d": ["D"]}
        progress.QUOTA["hit"] = True
        try:
            with Fake(progress, "ecosystem_repos", lambda _text: repos), Fake(progress, "pushed_map", lambda *_: {}), Fake(progress, "read_signals", lambda *_: None):
                with self.assertRaises(progress.FactsUnavailable) as raised:
                    progress.compute(reader=lambda _name: {"maturity": "functional", "evidence": "none"}, signals=progress.read_signals)
        finally:
            progress.QUOTA["hit"] = False
        self.assertTrue(raised.exception.quota)


class SavedReadsTests(unittest.TestCase):
    def test_the_signals_skip_the_tags_and_the_files_of_a_repository_that_was_not_pushed(self):
        asked = []

        def fake_api(path, unchanged_since=None):
            asked.append((path.split("/")[-1].split("?")[0], unchanged_since))
            if path.endswith("tags?per_page=100"):
                return [{"name": "v1"}]
            if path.endswith("/contents"):
                return [{"name": "tests"}, {"name": "README.md"}]
            return {"workflow_runs": [{"conclusion": "success"}]}
        with Fake(progress, "_api", fake_api), Fake(progress, "_fetch_raw", lambda *_: ""):
            signals = progress.read_signals("R", 1234)
        self.assertEqual(signals["releases"], 1)
        self.assertEqual(asked, [("tags", 1234), ("contents", 1234), ("runs", None)])    # the last builds are always read

    def test_the_moment_of_the_last_push_comes_from_the_list_of_repositories(self):
        pages = [[{"name": "A", "pushed_at": "2001-12-21T11:00:00Z"}, {"name": "B", "pushed_at": "nonsense"}, {"name": "C"}]]
        with Fake(progress, "_api", lambda path, unchanged_since=None: pages.pop(0) if pages else None):
            self.assertEqual(progress.pushed_map("o"), {"A": 1008932400})
        with Fake(progress, "_api", lambda path, unchanged_since=None: None):
            self.assertEqual(progress.pushed_map("o"), {})

    def test_a_refused_read_with_no_saved_answer_flags_the_quota(self):
        cache = gh_http.ConditionalGet(None, {})
        old_shared, gh_http._shared = gh_http._shared, cache
        import os
        old_token, os.environ["GITHUB_TOKEN"] = os.environ.get("GITHUB_TOKEN"), "x"
        cache.get = lambda url, headers, timeout=0, unchanged_since=None: gh_http.Reply(None, "failed", 0, "HTTP 403 (quota)")
        progress.QUOTA["hit"] = False
        try:
            self.assertIsNone(progress._api("repos/o/r/tags"))
            self.assertTrue(progress.QUOTA["hit"])
        finally:
            progress.QUOTA["hit"] = False
            gh_http._shared = old_shared
            if old_token is None:
                os.environ.pop("GITHUB_TOKEN", None)
            else:
                os.environ["GITHUB_TOKEN"] = old_token


if __name__ == "__main__":
    unittest.main()
