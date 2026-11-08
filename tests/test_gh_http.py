# =============================================================================
# JuanenRac profile - tests/test_gh_http.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Conditional reads with a saved copy: ETag, 304, a refused quota, an unreachable GitHub and the limits of the copy. No network: the opener is a stand-in."""
import email.message
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_integrity as integrity  # noqa: E402
import gh_http  # noqa: E402

URL = "https://api.github.com/users/o/repos?page=1"
HEADERS = {"User-Agent": "test"}


class Answer:
    def __init__(self, body, etag=None):
        self.body = body
        self.headers = email.message.Message()
        if etag:
            self.headers["ETag"] = etag

    def read(self, *_):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def http_error(code, headers=None, body=b""):
    msg = email.message.Message()
    for key, value in (headers or {}).items():
        msg[key] = value
    return urllib.error.HTTPError(URL, code, "x", msg, io.BytesIO(body))


class Script:
    """An opener that answers from a list, remembering what it was sent."""

    def __init__(self, *answers):
        self.answers = list(answers)
        self.sent = []

    def __call__(self, request, timeout=None):
        self.sent.append({key.lower(): value for key, value in request.header_items()})
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer


class Clock:
    def __init__(self, now=1_000_000):
        self.now = now

    def __call__(self):
        return self.now


class ConditionalReadTests(unittest.TestCase):
    def make(self, **config):
        self.clock = Clock()
        return gh_http.ConditionalGet(None, config, self.clock)

    def test_a_first_read_is_fresh_and_keeps_the_tag(self):
        cache = self.make()
        opener = Script(Answer(b'[{"name": "a"}]', 'W/"t1"'))
        reply = cache.get(URL, HEADERS, opener=opener)
        self.assertEqual((reply.how, reply.data), ("fresh", [{"name": "a"}]))
        self.assertNotIn("if-none-match", opener.sent[0])
        self.assertEqual(cache.entries[URL]["etag"], 'W/"t1"')

    def test_the_next_read_sends_the_tag_and_a_304_costs_nothing(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b"[1, 2]", '"t1"')))
        opener = Script(http_error(304))
        reply = cache.get(URL, HEADERS, opener=opener)
        self.assertEqual((reply.how, reply.data), ("not_modified", [1, 2]))
        self.assertEqual(opener.sent[0]["if-none-match"], '"t1"')
        self.assertEqual(cache.summary()["not_modified"], 1)

    def test_a_changed_answer_replaces_the_copy(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b"[1]", '"t1"')))
        reply = cache.get(URL, HEADERS, opener=Script(Answer(b"[1, 2]", '"t2"')))
        self.assertEqual(reply.data, [1, 2])
        self.assertEqual(cache.entries[URL]["etag"], '"t2"')

    def test_a_spent_quota_uses_the_saved_copy_and_says_how_old_it_is(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b'["old"]', '"t1"')))
        self.clock.now += 3 * 3600
        refusals = (http_error(429), http_error(403, {"X-RateLimit-Remaining": "0"}), http_error(403, {"Retry-After": "60"}),
                    http_error(403, body=b'{"message": "API rate limit exceeded"}'), http_error(403, body=b'{"message": "You have exceeded a secondary rate limit"}'))
        for refusal in refusals:
            reply = cache.get(URL, HEADERS, opener=Script(refusal))
            self.assertEqual((reply.how, reply.data, reply.age_seconds), ("stale", ["old"], 3 * 3600))
        self.assertEqual(cache.summary()["stale"], 5)
        self.assertEqual(cache.summary()["oldest_stale"], 3 * 3600)

    def test_an_unreachable_github_uses_the_saved_copy(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b'["old"]', '"t1"')))
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(urllib.error.URLError("down"))).how, "stale")
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(http_error(503))).how, "stale")

    def test_a_copy_that_is_too_old_is_not_used(self):
        cache = self.make(stale_max_hours=2)
        cache.get(URL, HEADERS, opener=Script(Answer(b'["old"]', '"t1"')))
        self.clock.now += 3 * 3600
        reply = cache.get(URL, HEADERS, opener=Script(http_error(429)))
        self.assertEqual((reply.how, reply.data), ("failed", None))

    def test_a_real_refusal_or_a_missing_page_is_not_hidden_by_the_copy(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b'["old"]', '"t1"')))
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(http_error(404))).how, "failed")
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(http_error(403, body=b'{"message": "Resource not accessible"}'))).how, "failed")

    def test_without_a_copy_a_refusal_is_a_failure(self):
        cache = self.make()
        reply = cache.get(URL, HEADERS, opener=Script(http_error(429)))
        self.assertEqual((reply.how, reply.data), ("failed", None))
        self.assertIn("quota", reply.reason)

    def test_an_answer_that_is_not_json_is_a_failure_and_is_not_kept(self):
        cache = self.make()
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(Answer(b"<html>", '"t"'))).how, "failed")
        self.assertNotIn(URL, cache.entries)

    def test_a_body_over_the_limit_is_used_but_not_kept(self):
        cache = self.make(max_body_bytes=1000)
        big = json.dumps(["x" * 2000]).encode()
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(Answer(big, '"t"'))).how, "fresh")
        self.assertNotIn(URL, cache.entries)

    def test_switched_off_it_sends_no_tag_and_keeps_nothing(self):
        cache = self.make(enabled=False)
        cache.get(URL, HEADERS, opener=Script(Answer(b"[1]", '"t"')))
        opener = Script(http_error(429))
        self.assertEqual(cache.get(URL, HEADERS, opener=opener).how, "failed")
        self.assertNotIn("if-none-match", opener.sent[0])

    def test_the_copy_is_saved_pruned_and_read_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data" / "etag-cache.json"
            cache = gh_http.ConditionalGet(path, {"max_entries": 10}, Clock())
            for number in range(14):
                cache.clock = Clock(1_000_000 + number)
                cache.get(f"https://api.github.com/x/{number}", HEADERS, opener=Script(Answer(b"[%d]" % number, f'"t{number}"')))
            self.assertTrue(cache.save())
            self.assertFalse(cache.save())
            again = gh_http.ConditionalGet(path, {}, Clock())
            self.assertEqual(len(again.entries), 10)
            self.assertIn("https://api.github.com/x/13", again.entries)
            self.assertNotIn("https://api.github.com/x/0", again.entries)

    def test_a_damaged_copy_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.json"
            for text in ("not json", "[]", json.dumps({"schema": 9, "entries": {}}), json.dumps({"schema": 1, "entries": {"u": {"etag": 1}}})):
                path.write_text(text, encoding="utf-8")
                self.assertEqual(gh_http.ConditionalGet(path, {}, Clock()).entries, {})


class NothingPushedTests(unittest.TestCase):
    def make(self, **config):
        self.clock = Clock(1_000_000)
        return gh_http.ConditionalGet(None, config, self.clock)

    def test_a_saved_answer_newer_than_the_last_push_needs_no_request(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b'["a"]', '"t1"')))
        opener = Script()          # any request would fail: the script has no answer
        reply = cache.get(URL, HEADERS, opener=opener, unchanged_since=1_000_000 - 3600)
        self.assertEqual((reply.how, reply.data, opener.sent), ("unchanged", ["a"], []))
        self.assertEqual(cache.summary()["skipped"], 1)
        self.assertEqual(cache.summary()["requests"], 1)

    def test_a_push_after_the_saved_answer_means_a_new_read(self):
        cache = self.make()
        cache.get(URL, HEADERS, opener=Script(Answer(b'["old"]', '"t1"')))
        self.clock.now += 600
        reply = cache.get(URL, HEADERS, opener=Script(Answer(b'["new"]', '"t2"')), unchanged_since=1_000_000 + 300)
        self.assertEqual((reply.how, reply.data), ("fresh", ["new"]))

    def test_a_push_within_the_margin_of_the_read_is_not_trusted(self):
        cache = self.make(unchanged_margin_seconds=120)
        cache.get(URL, HEADERS, opener=Script(Answer(b"[1]", '"t1"')))
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(Answer(b"[2]", '"t2"')), unchanged_since=1_000_000 - 60).how, "fresh")

    def test_without_a_saved_answer_or_a_known_push_the_read_goes_out(self):
        cache = self.make()
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(Answer(b"[1]", '"t1"')), unchanged_since=1).how, "fresh")
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(http_error(304))).how, "not_modified")

    def test_switched_off_it_never_skips(self):
        cache = self.make(enabled=False)
        cache.get(URL, HEADERS, opener=Script(Answer(b"[1]", '"t1"')))
        self.assertEqual(cache.get(URL, HEADERS, opener=Script(Answer(b"[1]", '"t1"')), unchanged_since=1).how, "fresh")

    def test_the_listing_reports_the_moment_of_the_last_push(self):
        pages = [{"name": "a", "pushed_at": "2001-12-21T11:00:00Z"}, {"name": "b", "pushed_at": "nonsense"}, {"name": "c"}]
        details = {}
        integrity.github_listing("o", "", reader=lambda url, headers, timeout=0: gh_http.Reply(pages, "fresh"), details=details)()
        self.assertEqual(details["pushed"], {"a": 1008932400})


class ConfigurationTests(unittest.TestCase):
    def test_defaults_and_valid_values(self):
        self.assertEqual(gh_http.check_config(None), (gh_http.DEFAULT_CONFIG, []))
        config, problems = gh_http.check_config({"enabled": False, "max_entries": 50, "stale_max_hours": 24, "path": "data/other.json"})
        self.assertEqual((config["enabled"], config["max_entries"], config["stale_max_hours"], config["path"], problems), (False, 50, 24, "data/other.json", []))

    def test_wrong_values_keep_the_default_and_are_named(self):
        config, problems = gh_http.check_config({"enabled": "yes", "max_entries": 1, "max_body_bytes": True, "stale_max_hours": 99999, "path": "../x.json"})
        self.assertEqual(config, gh_http.DEFAULT_CONFIG)
        self.assertEqual(len(problems), 5)
        self.assertEqual(gh_http.check_config([])[1], ["http_cache: not an object"])

    def test_the_repository_configuration_is_valid(self):
        config, problems = gh_http.load_config()
        self.assertEqual(problems, [])
        self.assertTrue(config["enabled"])

    def test_what_counts_as_a_quota_refusal(self):
        self.assertTrue(gh_http.is_quota_refusal(429, {}))
        self.assertTrue(gh_http.is_quota_refusal(403, {"x-ratelimit-remaining": "0"}))
        self.assertFalse(gh_http.is_quota_refusal(403, {"x-ratelimit-remaining": "42"}, "Forbidden"))
        self.assertFalse(gh_http.is_quota_refusal(404, {}))


class ListingTests(unittest.TestCase):
    def test_the_listing_reads_every_page_through_the_conditional_reader(self):
        pages = {1: [{"name": f"r{i}", "default_branch": "main"} for i in range(100)], 2: [{"name": "last", "archived": True}, {"name": "a-fork", "fork": True}]}
        calls = []

        def reader(url, headers, timeout=0):
            calls.append(url)
            return gh_http.Reply(pages[int(url.rsplit("=", 1)[1])], "fresh")
        details = {}
        found, error = integrity.github_listing("o", "", reader=reader, details=details)()
        self.assertEqual((len(found), error, len(calls)), (101, "", 2))
        self.assertEqual(details, {"archived": ["last"], "stale": False, "pushed": {}})
        self.assertIn(("last", "main"), found)

    def test_a_page_from_the_saved_copy_is_marked(self):
        details = {}
        reader = lambda url, headers, timeout=0: gh_http.Reply([{"name": "a"}], "stale", 60)  # noqa: E731
        found, error = integrity.github_listing("o", "", reader=reader, details=details)()
        self.assertEqual((found, error, details["stale"]), ([("a", "main")], "", True))

    def test_a_failed_page_reports_why(self):
        reader = lambda url, headers, timeout=0: gh_http.Reply(None, "failed", 0, "HTTP 403 (quota)")  # noqa: E731
        found, error = integrity.github_listing("o", "", reader=reader)()
        self.assertEqual(found, [])
        self.assertEqual(error, "HTTP 403 (quota) listing page 1")


if __name__ == "__main__":
    unittest.main()
