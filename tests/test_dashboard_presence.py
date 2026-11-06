# =============================================================================
# JuanenRac profile - tests/test_dashboard_presence.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Presence of signature files and of build attestations on the latest release: the files that count, the states, the cache, the budget of requests and the
refusal of the token. No network: the fetcher is a fake."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_charts as charts  # noqa: E402
import dashboard_presence as pr  # noqa: E402
import dashboard_presence_texts as texts  # noqa: E402
import dashboard_robust as robust  # noqa: E402
import dashboard_signatures as sigs  # noqa: E402

EXT = pr.DEFAULT_CONFIG["release_extensions"]
HEX = "0123456789abcdef" * 4


def digest(seed: str) -> str:
    return "sha256:" + (seed * 64)[:64]


def act(names, signature="none", tag="v1.0.0"):
    return charts.Activity(release_tag=tag, release_date="2001-01-01T00:00:00Z", signature=signature, assets=tuple((n, 1, "2001-01-01T00:00:00Z") for n in names))


class Fetch:
    """releases/latest gives the assets with digests; attestations/<digest> answers from `attested` (a set of digests), `refuse` (HTTP 403) or `fail`."""

    def __init__(self, releases, attested=(), refuse=False, fail=()):
        self.releases, self.attested, self.refuse, self.fail = releases, set(attested), refuse, set(fail)
        self.calls = []

    def rest(self, path):
        self.calls.append(path)
        parts = path.strip("/").split("/")
        if parts[3] == "releases":
            rel = self.releases.get(parts[2])
            return ("ok", rel) if rel is not None else ("absent", None)
        if self.refuse:
            return "error", "HTTP 403"
        d = parts[4]
        if d in self.fail:
            return "error", "lookup failed: boom"
        return ("ok", {"attestations": [{"bundle": {}}]}) if d in self.attested else ("absent", None)


def release(files):
    return {"tag_name": "v1.0.0", "assets": [{"name": n, "digest": digest(d)} for n, d in files.items()]}


class FilesAndSignatures(unittest.TestCase):
    def test_sidecars_are_not_release_files(self):
        names = ["a.bin", "a.bin.sig", "a.bin.sig2", "a.bin.hdr2", "a.bin.imgsig", "a.bin.sha256", "b.tgz", "notes.md", "manifest.json", "c.apk.sha256"]
        self.assertEqual(pr.primaries(names, EXT), ["a.bin", "b.tgz"])

    def test_signature_states(self):
        self.assertEqual(pr.signature_presence(["a.tgz", "a.tgz.sig", "a.tgz.sha256"], EXT), {"s": "present", "n": 1, "k": 1, "h": 1})
        self.assertEqual(pr.signature_presence(["a.tgz", "a.tgz.sig", "b.zip"], EXT)["s"], "partial")
        self.assertEqual(pr.signature_presence(["a.tgz", "b.zip"], EXT)["s"], "absent")
        self.assertEqual(pr.signature_presence(["README.md", "a.json"], EXT)["s"], "na")
        self.assertEqual(pr.signature_presence([], EXT)["s"], "na")
        self.assertEqual(pr.signature_presence(["fw.bin", "fw.bin.sig2"], EXT)["s"], "present")
        self.assertEqual(pr.signature_presence(["x.apk", "x.apk.minisig"], EXT)["s"], "present")

    def test_a_signature_without_its_file_is_not_a_signed_file(self):
        self.assertEqual(pr.signature_presence(["a.tgz.sig"], EXT)["s"], "na")

    def test_attestation_state(self):
        self.assertEqual(pr.attestation_state([True, True]), "present")
        self.assertEqual(pr.attestation_state([True, False]), "partial")
        self.assertEqual(pr.attestation_state([False, False]), "absent")
        self.assertEqual(pr.attestation_state([]), "unknown")
        self.assertEqual(pr.attestation_state([None]), "unknown")
        self.assertEqual(pr.attestation_state([False, None]), "unknown")
        self.assertEqual(pr.attestation_state([True, None]), "partial")


class Assess(unittest.TestCase):
    CONFIG = json.loads(json.dumps(pr.DEFAULT_CONFIG))

    def run_assess(self, activity, fetch, cache=None, config=None, today="2001-02-01"):
        return pr.assess("JuanenRac", activity, fetch, config or self.CONFIG, cache, today)

    def test_states_without_network_for_the_cases_that_need_none(self):
        activity = {"A": act([], "norelease"), "B": act(["only.md"]), "C": charts.Activity(signature=None)}
        found, cache = self.run_assess(activity, Fetch({}))
        self.assertEqual((found["A"]["sg"], found["A"]["at"]), ("na", "na"))
        self.assertEqual((found["B"]["sg"], found["B"]["at"]), ("na", "na"))
        self.assertEqual((found["C"]["sg"], found["C"]["at"]), ("unknown", "unknown"))
        self.assertEqual(cache, {})

    def test_present_partial_absent(self):
        releases = {"P": release({"p.tgz": "a", "p.tgz.sig": "b"}), "Q": release({"q.tgz": "c", "q.zip": "d"}), "R": release({"r.tgz": "e"})}
        fetch = Fetch(releases, attested={digest("a"), digest("c")})
        activity = {"P": act(["p.tgz", "p.tgz.sig"], "present"), "Q": act(["q.tgz", "q.zip"]), "R": act(["r.tgz"])}
        found, cache = self.run_assess(activity, fetch)
        self.assertEqual((found["P"]["sg"], found["P"]["at"], found["P"]["an"], found["P"]["ak"]), ("present", "present", 1, 1))
        self.assertEqual((found["Q"]["sg"], found["Q"]["at"], found["Q"]["an"], found["Q"]["ak"]), ("absent", "partial", 2, 1))
        self.assertEqual((found["R"]["sg"], found["R"]["at"]), ("absent", "absent"))
        self.assertEqual(set(cache), {"P", "Q", "R"})
        self.assertTrue(all(c.startswith("/repos/JuanenRac/") for c in fetch.calls))

    def test_the_digest_goes_in_the_path_as_github_holds_it(self):
        fetch = Fetch({"P": release({"p.tgz": "a"})}, attested={digest("a")})
        self.run_assess({"P": act(["p.tgz"])}, fetch)
        self.assertEqual(fetch.calls[1], f"/repos/JuanenRac/P/attestations/{digest('a')}")

    def test_cache_is_used_for_the_same_release_and_present_never_expires(self):
        releases = {"P": release({"p.tgz": "a"})}
        activity = {"P": act(["p.tgz"])}
        _found, cache = self.run_assess(activity, Fetch(releases, attested={digest("a")}))
        fetch = Fetch(releases)
        found, _ = self.run_assess(activity, fetch, {"presence": cache}, today="2009-01-01")
        self.assertEqual(found["P"]["at"], "present")
        self.assertEqual(fetch.calls, [])

    def test_absent_is_asked_again_after_the_recheck_days(self):
        releases = {"P": release({"p.tgz": "a"})}
        activity = {"P": act(["p.tgz"])}
        _f, cache = self.run_assess(activity, Fetch(releases), today="2001-02-01")
        again = Fetch(releases)
        self.run_assess(activity, again, {"presence": cache}, today="2001-02-02")
        self.assertEqual(again.calls, [])
        later = Fetch(releases, attested={digest("a")})
        found, _ = self.run_assess(activity, later, {"presence": cache}, today="2001-02-05")
        self.assertEqual(found["P"]["at"], "present")
        self.assertEqual(len(later.calls), 2)

    def test_a_new_release_is_not_answered_from_the_cache(self):
        releases = {"P": release({"p.tgz": "a"})}
        _f, cache = self.run_assess({"P": act(["p.tgz"], tag="v1")}, Fetch(releases, attested={digest("a")}))
        fetch = Fetch(releases)
        found, _ = self.run_assess({"P": act(["p.tgz"], tag="v2")}, fetch, {"presence": cache})
        self.assertEqual(found["P"]["at"], "absent")
        self.assertEqual(len(fetch.calls), 2)

    def test_the_budget_ends_in_unknown_never_in_absent(self):
        releases = {n: release({f"{n}.tgz": n.lower() * 2}) for n in "ABCD"}
        activity = {n: act([f"{n}.tgz"]) for n in "ABCD"}
        config = {**self.CONFIG, "api_budget": 4}
        found, cache = self.run_assess(activity, Fetch(releases), config=config)
        self.assertEqual([found[n]["at"] for n in "ABCD"], ["absent", "absent", "unknown", "unknown"])
        self.assertEqual(set(cache), {"A", "B"})
        self.assertEqual(found["C"]["sg"], "absent")         # the signature needs no request

    def test_the_limit_of_repositories_per_run(self):
        releases = {n: release({f"{n}.tgz": n.lower() * 2}) for n in "ABC"}
        activity = {n: act([f"{n}.tgz"]) for n in "ABC"}
        fetch = Fetch(releases)
        found, _ = self.run_assess(activity, fetch, config={**self.CONFIG, "max_repos_per_run": 1})
        self.assertEqual([found[n]["at"] for n in "ABC"], ["absent", "unknown", "unknown"])
        self.assertEqual(len(fetch.calls), 2)

    def test_files_per_release_is_a_sample(self):
        names = [f"f{i}.tgz" for i in range(5)]
        releases = {"P": release({n: str(i) for i, n in enumerate(names)})}
        fetch = Fetch(releases, attested={digest(str(i)) for i in range(5)})
        found, _ = self.run_assess({"P": act(names)}, fetch, config={**self.CONFIG, "attestation_files_per_release": 2})
        self.assertEqual((found["P"]["n"], found["P"]["an"], found["P"]["ak"], found["P"]["at"]), (5, 2, 2, "present"))
        self.assertEqual(len(fetch.calls), 3)

    def test_a_refused_token_stops_the_requests_and_is_unknown(self):
        releases = {n: release({f"{n}.tgz": n.lower() * 2}) for n in "AB"}
        fetch = Fetch(releases, refuse=True)
        found, cache = self.run_assess({n: act([f"{n}.tgz"]) for n in "AB"}, fetch)
        self.assertEqual([found[n]["at"] for n in "AB"], ["unknown", "unknown"])
        self.assertEqual(cache, {})
        self.assertEqual(len(fetch.calls), 2)       # the release of A and its attestation; nothing for B

    def test_a_failed_read_of_one_file_is_partial_or_unknown(self):
        releases = {"P": release({"a.tgz": "a", "b.tgz": "b"}), "Q": release({"q.tgz": "q"})}
        fetch = Fetch(releases, attested={digest("a")}, fail={digest("b"), digest("q")})
        found, cache = self.run_assess({"P": act(["a.tgz", "b.tgz"]), "Q": act(["q.tgz"])}, fetch)
        self.assertEqual(found["P"]["at"], "partial")
        self.assertEqual(found["Q"]["at"], "unknown")
        self.assertNotIn("Q", cache)

    def test_a_release_that_cannot_be_read_is_unknown(self):
        found, cache = self.run_assess({"P": act(["p.tgz"])}, Fetch({}))
        self.assertEqual((found["P"]["sg"], found["P"]["at"]), ("absent", "unknown"))
        self.assertEqual(cache, {})

    def test_attestations_can_be_switched_off(self):
        fetch = Fetch({"P": release({"p.tgz": "a"})})
        found, _ = self.run_assess({"P": act(["p.tgz"])}, fetch, config={**self.CONFIG, "attestations": False})
        self.assertEqual(found["P"]["at"], "unknown")
        self.assertEqual(fetch.calls, [])

    def test_a_digest_that_is_not_sha256_is_ignored(self):
        bad = {"tag_name": "v1", "assets": [{"name": "p.tgz", "digest": "md5:abc"}]}
        found, _ = self.run_assess({"P": act(["p.tgz"])}, Fetch({"P": bad}))
        self.assertEqual(found["P"]["at"], "unknown")

    def test_summary_by_ecosystem(self):
        presence = {"A": {"sg": "present", "at": "present"}, "B": {"sg": "absent", "at": "unknown"}, "C": {"sg": "na", "at": "na"}, "D": {"sg": "partial", "at": "partial"}}
        out = pr.summarize(presence, {"A": "armor", "B": "armor", "C": "armor", "D": "urtc"})
        self.assertEqual(out["armor"]["repos"], 2)
        self.assertEqual(out["armor"]["sg"]["absent"], 1)
        self.assertEqual(out["armor"]["at"]["unknown"], 1)
        self.assertEqual(out["urtc"]["sg"]["partial"], 1)


class ConfigAndCache(unittest.TestCase):
    def test_defaults_and_bad_values(self):
        config, problems = pr.check_config(None)
        self.assertEqual((config["api_budget"], problems), (120, []))
        config, problems = pr.check_config({"api_budget": -1, "enabled": "yes", "release_extensions": ["zip"], "recheck_days": 5})
        self.assertEqual(config["api_budget"], 120)
        self.assertEqual(config["recheck_days"], 5)
        self.assertEqual(len(problems), 3)
        self.assertEqual(pr.check_config("x")[1], ["presence: not an object"])

    def test_the_real_configuration_file_is_valid(self):
        config, problems = pr.load_config(HERE.parent / "dashboard-config.json")
        self.assertEqual(problems, [])
        self.assertTrue(config["enabled"])

    def test_cache_keeps_the_presence_part(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cache.json"
            sigs.save_cache(path, {"X": {"fp": "1", "r": {"s": "verified"}}}, {"Y": {"wf": "w"}}, {"P": {"fp": "f", "on": "2001-01-01", "r": {"at": "present"}}})
            sigs.save_cache(path, {}, None, None)
            body = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(body["presence"]["P"]["on"], "2001-01-01")
            self.assertEqual(body["builds"], {"Y": {"wf": "w"}})

    def test_the_published_page_keeps_the_presence_of_a_repository(self):
        self.assertEqual(pr.valid({"sg": "partial", "at": "unknown", "n": 3, "k": 1, "h": 0, "an": 0, "ak": 0})["sg"], "partial")
        self.assertIsNone(pr.valid({"sg": "maybe", "at": "present"}))
        self.assertIsNone(pr.valid("x"))
        page = ('<script type="application/json" id="dashboard-data">' + json.dumps({"repos": {"R": {"known": True, "prs": {"sg": "absent", "at": "present", "n": 2, "k": 0, "h": 1, "an": 1, "ak": 1}}}}) + "</script>")
        self.assertEqual(robust.activity_from_page(page)["R"].presence["at"], "present")


class Texts(unittest.TestCase):
    def test_eight_languages_and_same_placeholders(self):
        self.assertEqual(texts.problems(), [])
        self.assertEqual(sorted(texts.TEXTS), sorted(["en", "es", "de", "fr", "it", "ja", "zh", "pt"]))
        self.assertNotEqual(texts.TEXTS["pt"]["pr_col_files"], texts.TEXTS["es"]["pr_col_files"])
        for key in ("pr_s_present", "pr_s_partial", "pr_s_absent", "pr_s_na", "pr_s_unknown", "pr_hint"):
            self.assertTrue(all(texts.TEXTS[code][key].strip() for code in texts.TEXTS))


if __name__ == "__main__":
    unittest.main()
