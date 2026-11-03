# =============================================================================
# JuanenRac profile - tests/test_dashboard_signatures.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Ed25519 verification, the messages each family signs, the verdict per release (valid, invalid, not verifiable, not read), the cache and the inferred pipeline.

Every key used here is ephemeral (made from os.urandom when the tests run and never written); no real key or signature of the owner is involved."""
import base64
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import dashboard_charts as charts  # noqa: E402
import dashboard_ed25519 as ed  # noqa: E402
import dashboard_evo as evo  # noqa: E402
import dashboard_pipeline as pipeline  # noqa: E402
import dashboard_signatures as sigs  # noqa: E402


def _compress(point):
    x, y, z, _t = point
    zi = ed._inv(z)
    x, y = x * zi % ed._P, y * zi % ed._P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def public_of(seed: bytes) -> bytes:
    h = hashlib.sha512(seed).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return _compress(ed._mul(a, ed._BASE))


def sign(seed: bytes, message: bytes) -> bytes:
    """RFC 8032 section 5.1.6, only to make test vectors with an ephemeral key."""
    h = hashlib.sha512(seed).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    public = _compress(ed._mul(a, ed._BASE))
    r = int.from_bytes(hashlib.sha512(h[32:] + message).digest(), "little") % ed._Q
    big_r = _compress(ed._mul(r, ed._BASE))
    k = int.from_bytes(hashlib.sha512(big_r + public + message).digest(), "little") % ed._Q
    return big_r + ((r + k * a) % ed._Q).to_bytes(32, "little")


SEEDS = {family: os.urandom(32) for family in ("armor", "urtc", "hydra")}
OTHER_SEED = os.urandom(32)
CONFIG = sigs.check_config({"keys": {family: public_of(seed).hex() for family, seed in SEEDS.items()}})[0]


class Ed25519Tests(unittest.TestCase):
    def test_rfc8032_vectors(self):
        vectors = [
            ("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
             "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
            ("3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
             "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
            ("fc51cd8e6218a0a38da47d6d7e5d2e1d1a3e0b1c9a4a6dc7f7b2f4d3c2b1a090", "", "00" * 64),
        ]
        self.assertTrue(ed.verify(bytes.fromhex(vectors[0][0]), bytes.fromhex(vectors[0][1]), bytes.fromhex(vectors[0][2])))
        self.assertTrue(ed.verify(bytes.fromhex(vectors[1][0]), bytes.fromhex(vectors[1][1]), bytes.fromhex(vectors[1][2])))
        self.assertFalse(ed.verify(bytes.fromhex(vectors[2][0]), b"", bytes.fromhex(vectors[2][2])))

    def test_a_valid_ephemeral_signature_verifies_and_every_change_breaks_it(self):
        seed = os.urandom(32)
        public, message = public_of(seed), b"armor-pkg/1|server|1.2.3|" + b"a" * 64
        signature = sign(seed, message)
        self.assertTrue(ed.verify(public, message, signature))
        self.assertFalse(ed.verify(public, message + b"x", signature))
        self.assertFalse(ed.verify(public_of(os.urandom(32)), message, signature))
        flipped = bytearray(signature)
        flipped[3] ^= 1
        self.assertFalse(ed.verify(public, message, bytes(flipped)))

    def test_malformed_input_is_refused(self):
        seed = os.urandom(32)
        public, signature = public_of(seed), sign(seed, b"m")
        self.assertFalse(ed.verify(public[:31], b"m", signature))
        self.assertFalse(ed.verify(public, b"m", signature[:63]))
        self.assertFalse(ed.verify(b"\xff" * 32, b"m", signature))
        malleable = signature[:32] + ((int.from_bytes(signature[32:], "little") + ed._Q) % (1 << 256)).to_bytes(32, "little")
        self.assertFalse(ed.verify(public, b"m", malleable))       # S not below the group order


class FakeFetch:
    """Answers of the REST API and the downloads from memory; counts the calls."""

    def __init__(self, releases=None, files=None):
        self.releases, self.files, self.rest_calls, self.downloads, self.fail_download = releases or {}, files or {}, [], [], set()

    def rest(self, path):
        self.rest_calls.append(path)
        if path in self.releases:
            value = self.releases[path]
            return ("error", "boom") if value is None else ("ok", value)
        return "absent", None

    def download(self, url, limit):
        self.downloads.append(url)
        if url in self.fail_download:
            raise sigs.ReadError("network")
        data = self.files[url]
        if len(data) > limit:
            raise sigs.ReadError("larger than the limit")
        return data


def asset(name, data=b"", size=None, digest=True, repo="R"):
    url = f"https://github.com/JuanenRac/{repo}/releases/download/v1/{name}"
    item = {"name": name, "size": len(data) if size is None else size, "browser_download_url": url}
    if digest:
        item["digest"] = "sha256:" + hashlib.sha256(data).hexdigest()
    return item, url, data


def release(tag, *entries):
    return {"tag_name": tag, "assets": [e[0] for e in entries]}, {e[1]: e[2] for e in entries}


def sig_text(family, message, hex_form=True):
    signature = sign(SEEDS[family], message)
    return (signature.hex() if hex_form else base64.b64encode(signature).decode()).encode() + b"\n"


def verdict(family, repo, rel, files, **kwargs):
    fetch = FakeFetch(files=files)
    return sigs.verify_release(family, repo, rel, fetch, kwargs.get("config", CONFIG)), fetch


class MessageTests(unittest.TestCase):
    def test_armor_package_firmware_and_hash(self):
        sha = "ab" * 32
        package = sigs.Asset("armor-server-0.8.1.5.tgz", 10, sha, "")
        self.assertEqual(sigs.messages("armor", package, "v0.8.1.5", sha, ".sig"), [("armor-pkg/1", f"armor-pkg/1|server|0.8.1.5|{sha}".encode())])
        image = sigs.Asset("armor_radar-s3-eth.bin", 10, sha, "")
        self.assertEqual(sigs.messages("armor", image, "v0.8.0.8", sha, ".sig"), [("armor-fw/1 (hash)", bytes.fromhex(sha))])
        self.assertEqual(sigs.messages("armor", image, "v0.8.0.8", sha, ".sig2"), [("armor-fw/1", f"armor-fw/1|armor_radar|s3-eth|0.8.0.8|{sha}".encode())])
        self.assertEqual(sigs.messages("armor", image, "nightly", sha, ".sig2"), [])      # no version to bind: nothing can be checked

    def test_urtc_release_and_package_and_common(self):
        sha = "cd" * 32
        text = sigs.Asset("URTC_MAIN_FIRMWARE_v0.4.4.bin", 5, sha, "")
        self.assertEqual(sigs.messages("urtc", text, "v0.4.4", sha, ".sig"), [("urtc-rel/1", f"urtc-rel/1|URTC_MAIN_FIRMWARE_v0.4.4.bin|{sha}".encode())])
        package = sigs.Asset("urtc-flasher-0.5.0-windows-x86_64.zip", 77, sha, "")
        found = dict(sigs.messages("urtc", package, "v0.5.0", sha, ".sig"))
        self.assertEqual(found["urtc-pkg/1"], f"urtc-pkg/1|urtc-flasher|0.5.0|windows-x86_64|{sha}|77".encode())
        wheel = sigs.Asset("urtc_common-0.1.9-py3-none-any.whl", 9, sha, "")
        self.assertIn(("urtc-pkg/1", f"urtc-pkg/1|urtc-common|0.1.9|py3-none-any|{sha}|9".encode()), sigs.messages("urtc", wheel, "v0.1.9", sha, ".sig"))
        header = sigs.Asset("urtc_can_ids.h", 3, sha, "")
        self.assertIn(("urtc-pkg/1", f"urtc-pkg/1|urtc-common|0.1.9|c-header|{sha}|3".encode()), sigs.messages("urtc", header, "v0.1.9", sha, ".sig"))

    def test_hydra_package_and_unknown_families(self):
        sha = "ef" * 32
        package = sigs.Asset("updater-0.5.5.tgz", 3, sha, "")
        self.assertEqual(sigs.messages("hydra", package, "v0.5.5", sha, ".sig"), [("hydra-pc-pkg/1", f"hydra-pc-pkg/1|updater|0.5.5|{sha}".encode())])
        self.assertEqual(sigs.messages("hydra", sigs.Asset("tool.exe", 1, sha, ""), "v1.0.0", sha, ".sig"), [])
        self.assertEqual(sigs.messages("eh3d", package, "v0.5.5", sha, ".sig"), [])

    def test_families_by_name(self):
        self.assertEqual([sigs.family_of(n) for n in ("ARMOR-SERVER", "URTC", "URTC-COMMON", "HYDRA-UMC", "HYDRA-UMC-SUITE", "EH3D-SERVER", "JuanenRac", "URTCX")],
                         ["armor", "urtc", "urtc", "hydra", "hydra", None, None, None])


class VerdictTests(unittest.TestCase):
    def test_a_valid_armor_package_is_verified(self):
        data = b"package bytes"
        sha = hashlib.sha256(data).hexdigest()
        pkg = asset("armor-server-1.2.3.tgz", data)
        sig = asset("armor-server-1.2.3.tgz.sig", sig_text("armor", f"armor-pkg/1|server|1.2.3|{sha}".encode()))
        rel, files = release("v1.2.3", pkg, sig)
        result, fetch = verdict("armor", "ARMOR-SERVER", rel, files)
        self.assertEqual((result["s"], result["ok"], result["bad"], result["sch"]), ("verified", 1, 0, ["armor-pkg/1"]))
        self.assertEqual(fetch.downloads, [sig[1]])             # only the signature is downloaded: the digest of GitHub binds the file

    def test_a_package_changed_after_signing_is_invalid(self):
        original = b"package bytes"
        sha = hashlib.sha256(original).hexdigest()
        changed = asset("armor-server-1.2.3.tgz", b"another content")
        sig = asset("armor-server-1.2.3.tgz.sig", sig_text("armor", f"armor-pkg/1|server|1.2.3|{sha}".encode()))
        rel, files = release("v1.2.3", changed, sig)
        self.assertEqual(verdict("armor", "ARMOR-SERVER", rel, files)[0]["s"], "invalid")

    def test_a_signature_made_with_another_key_is_invalid(self):
        data = b"x"
        sha = hashlib.sha256(data).hexdigest()
        message = f"armor-pkg/1|server|1.2.3|{sha}".encode()
        forged = base64.b16encode(sign(OTHER_SEED, message)).lower() + b"\n"
        rel, files = release("v1.2.3", asset("armor-server-1.2.3.tgz", data), asset("armor-server-1.2.3.tgz.sig", forged))
        result = verdict("armor", "ARMOR-SERVER", rel, files)[0]
        self.assertEqual((result["s"], result["bad"], result["why"]), ("invalid", 1, ["mismatch"]))

    def test_a_signature_for_another_version_or_name_is_invalid(self):
        data = b"x"
        sha = hashlib.sha256(data).hexdigest()
        for message in (f"armor-pkg/1|server|1.2.2|{sha}", f"armor-pkg/1|studio|1.2.3|{sha}", f"hydra-pc-pkg/1|server|1.2.3|{sha}"):
            rel, files = release("v1.2.3", asset("armor-server-1.2.3.tgz", data), asset("armor-server-1.2.3.tgz.sig", sig_text("armor", message.encode())))
            self.assertEqual(verdict("armor", "ARMOR-SERVER", rel, files)[0]["s"], "invalid", message)

    def test_one_bad_signature_makes_the_release_invalid_even_with_good_ones(self):
        good, bad = b"good", b"bad"
        rel, files = release(
            "v1.0.0",
            asset("armor-ai-1.0.0.tgz", good), asset("armor-ai-1.0.0.tgz.sig", sig_text("armor", f"armor-pkg/1|ai|1.0.0|{hashlib.sha256(good).hexdigest()}".encode())),
            asset("armor-voice-1.0.0.tgz", bad), asset("armor-voice-1.0.0.tgz.sig", sig_text("armor", b"armor-pkg/1|voice|1.0.0|" + b"0" * 64)))
        result = verdict("armor", "ARMOR-SERVER", rel, files)[0]
        self.assertEqual((result["s"], result["ok"], result["bad"]), ("invalid", 1, 1))

    def test_armor_firmware_signatures_of_the_manifest_and_of_the_hash(self):
        data = b"firmware image"
        sha = hashlib.sha256(data).hexdigest()
        rel, files = release(
            "v0.8.0.8", asset("armor_radar-s3-eth.bin", data),
            asset("armor_radar-s3-eth.bin.sig", base64.b16encode(sign(SEEDS["armor"], bytes.fromhex(sha))).lower()),
            asset("armor_radar-s3-eth.bin.sig2", sig_text("armor", f"armor-fw/1|armor_radar|s3-eth|0.8.0.8|{sha}".encode())))
        result = verdict("armor", "ARMOR-NODE-RADAR", rel, files)[0]
        self.assertEqual((result["s"], result["ok"], result["sch"]), ("verified", 2, ["armor-fw/1", "armor-fw/1 (hash)"]))

    def test_urtc_release_and_package_signatures(self):
        data = b"bootloader"
        sha = hashlib.sha256(data).hexdigest()
        rel, files = release("v0.4.6", asset("BOOT_v0.4.6.bin", data), asset("BOOT_v0.4.6.bin.sig", sig_text("urtc", f"urtc-rel/1|BOOT_v0.4.6.bin|{sha}".encode())))
        self.assertEqual(verdict("urtc", "URTC", rel, files)[0]["s"], "verified")
        package = b"zip bytes"
        sha = hashlib.sha256(package).hexdigest()
        message = f"urtc-pkg/1|urtc-tester|0.5.0|windows-x86_64|{sha}|{len(package)}".encode()
        rel, files = release("v0.5.0", asset("urtc-tester-0.5.0-windows-x86_64.zip", package), asset("urtc-tester-0.5.0-windows-x86_64.zip.sig", sig_text("urtc", message)))
        self.assertEqual(verdict("urtc", "URTC-TESTER", rel, files)[0]["sch"], ["urtc-pkg/1"])

    def test_hydra_package_in_hex_and_whole_file_in_base64(self):
        package = b"tgz"
        sha = hashlib.sha256(package).hexdigest()
        rel, files = release("v0.5.5", asset("updater-0.5.5.tgz", package), asset("updater-0.5.5.tgz.sig", sig_text("hydra", f"hydra-pc-pkg/1|updater|0.5.5|{sha}".encode())))
        self.assertEqual(verdict("hydra", "HYDRA-UMC-UPDATER", rel, files)[0]["s"], "verified")
        binary = b"a go binary" * 100
        rel, files = release("v0.2.0", asset("tool", binary), asset("tool.sig", sig_text("hydra", binary, hex_form=False)))
        result, fetch = verdict("hydra", "HYDRA-UMC-TOOL-CLI", rel, files)
        self.assertEqual((result["s"], result["sch"]), ("verified", ["hydra-sign"]))
        self.assertEqual(len(fetch.downloads), 2)               # the signature and the whole file
        rel, files = release("v0.2.0", asset("tool", binary + b"!"), asset("tool.sig", sig_text("hydra", binary, hex_form=False)))
        files[rel["assets"][0]["browser_download_url"]] = binary + b"!"
        self.assertEqual(verdict("hydra", "HYDRA-UMC-TOOL-CLI", rel, files)[0]["s"], "invalid")

    def test_a_file_too_large_to_download_is_unverifiable_for_a_whole_file_signature(self):
        binary = b"x" * 2000
        config = sigs.check_config({"max_asset_bytes": 1024})[0]
        config["keys"] = CONFIG["keys"]
        rel, files = release("v0.2.0", asset("tool", binary), asset("tool.sig", sig_text("hydra", binary, hex_form=False)))
        result, fetch = verdict("hydra", "HYDRA-UMC-TOOL-CLI", rel, files, config=config)
        self.assertEqual((result["s"], result["why"]), ("unverifiable", ["toobig"]))
        self.assertNotIn(rel["assets"][0]["browser_download_url"], fetch.downloads)

    def test_a_big_file_without_digest_is_proven_by_its_signed_sha256_only(self):
        data = b"x" * 3000
        sha = hashlib.sha256(data).hexdigest()
        config = sigs.check_config({"max_asset_bytes": 1024})[0]
        config["keys"] = CONFIG["keys"]
        side = asset("armor-server-1.0.0.tgz.sha256", f"{sha}  armor-server-1.0.0.tgz\n".encode(), digest=False)
        rel, files = release("v1.0.0", asset("armor-server-1.0.0.tgz", data, digest=False), side,
                             asset("armor-server-1.0.0.tgz.sig", sig_text("armor", f"armor-pkg/1|server|1.0.0|{sha}".encode())))
        result, fetch = verdict("armor", "ARMOR-SERVER", rel, files, config=config)
        self.assertEqual((result["s"], result["ho"]), ("verified", 1))
        self.assertNotIn(rel["assets"][0]["browser_download_url"], fetch.downloads)

    def test_unknown_formats_families_and_orphans_are_unverifiable_never_valid_or_invalid(self):
        data = b"x"
        for repo, names, why in (("EH3D-SERVER", ("a.tar.gz", "a.tar.gz.sig"), "family"), ("ARMOR-SERVER", ("a.bin", "a.bin.asc"), "format"),
                                 ("URTC", ("a.bin", "a.bin.minisig"), "format"), ("ARMOR-SERVER", ("lonely.sig",), "nofile")):
            entries = [asset(n, data if not n.endswith((".sig", ".asc", ".minisig")) else b"\n") for n in names]
            rel, files = release("v1.0.0", *entries)
            result = verdict(sigs.family_of(repo), repo, rel, files)[0]
            self.assertEqual((result["s"], result["ok"], result["bad"], result["why"]), ("unverifiable", 0, 0, [why]), repo)

    def test_garbage_in_a_signature_file_is_a_format_problem(self):
        data = b"x"
        rel, files = release("v1.0.0", asset("armor-ai-1.0.0.tgz", data), asset("armor-ai-1.0.0.tgz.sig", b"not a signature at all\n"))
        self.assertEqual(verdict("armor", "ARMOR-SERVER-AI", rel, files)[0]["why"], ["format"])

    def test_a_failed_download_is_not_a_verdict(self):
        data = b"x"
        sig = asset("armor-ai-1.0.0.tgz.sig", b"00" * 64)
        rel, files = release("v1.0.0", asset("armor-ai-1.0.0.tgz", data), sig)
        fetch = FakeFetch(files=files)
        fetch.fail_download.add(sig[1])
        self.assertIsNone(sigs.verify_release("armor", "ARMOR-SERVER-AI", rel, fetch, CONFIG))

    def test_a_release_without_signature_files_has_no_verdict(self):
        rel, files = release("v1.0.0", asset("a.bin", b"x"))
        self.assertIsNone(verdict("armor", "ARMOR-SERVER", rel, files)[0])


class ReadAllTests(unittest.TestCase):
    def setUp(self):
        data = b"pkg"
        sha = hashlib.sha256(data).hexdigest()
        self.rel, self.files = release("v1.0.0", asset("armor-ai-1.0.0.tgz", data, repo="ARMOR-SERVER-AI"),
                                       asset("armor-ai-1.0.0.tgz.sig", sig_text("armor", f"armor-pkg/1|ai|1.0.0|{sha}".encode()), repo="ARMOR-SERVER-AI"))
        self.inputs = {"ARMOR-SERVER-AI": ("v1.0.0", [("armor-ai-1.0.0.tgz", 3, "2001-01-01T00:00:00Z"), ("armor-ai-1.0.0.tgz.sig", 129, "2001-01-01T00:00:00Z")])}
        self.path = "/repos/JuanenRac/ARMOR-SERVER-AI/releases/latest"

    def test_a_release_is_read_once_and_then_taken_from_the_cache(self):
        fetch = FakeFetch({self.path: self.rel}, self.files)
        answers, cache = sigs.read_all("JuanenRac", self.inputs, fetch, CONFIG, {})
        self.assertEqual(answers["ARMOR-SERVER-AI"]["s"], "verified")
        self.assertEqual(len(fetch.rest_calls), 1)
        again = FakeFetch({self.path: self.rel}, self.files)
        answers2, cache2 = sigs.read_all("JuanenRac", self.inputs, again, CONFIG, {"signatures": cache})
        self.assertEqual(answers2, answers)
        self.assertEqual((again.rest_calls, again.downloads), ([], []))
        self.assertEqual(cache2, cache)

    def test_a_new_tag_or_a_replaced_asset_is_read_again(self):
        _a, cache = sigs.read_all("JuanenRac", self.inputs, FakeFetch({self.path: self.rel}, self.files), CONFIG, {})
        for changed in (("v1.0.1", self.inputs["ARMOR-SERVER-AI"][1]),
                        ("v1.0.0", [("armor-ai-1.0.0.tgz", 3, "2001-01-01T00:00:00Z"), ("armor-ai-1.0.0.tgz.sig", 129, "2002-02-02T00:00:00Z")])):
            fetch = FakeFetch({self.path: self.rel}, self.files)
            sigs.read_all("JuanenRac", {"ARMOR-SERVER-AI": changed}, fetch, CONFIG, {"signatures": cache})
            self.assertEqual(len(fetch.rest_calls), 1)

    def test_a_failed_read_is_not_verified_and_is_not_cached(self):
        fetch = FakeFetch({self.path: None}, self.files)
        answers, cache = sigs.read_all("JuanenRac", self.inputs, fetch, CONFIG, {})
        self.assertEqual((answers, cache), ({"ARMOR-SERVER-AI": None}, {}))

    def test_the_quota_per_run_is_respected(self):
        config = sigs.check_config({"max_repos_per_run": 1})[0]
        config["keys"] = CONFIG["keys"]
        many = {f"ARMOR-X{i}": ("v1.0.0", [("a.tgz", 1, "u"), ("a.tgz.sig", 129, "u")]) for i in range(3)}
        fetch = FakeFetch()
        answers, _cache = sigs.read_all("JuanenRac", many, fetch, config, {})
        self.assertEqual(len(fetch.rest_calls), 1)
        self.assertEqual(sum(1 for v in answers.values() if v is None), 3)      # nothing came back valid (the fake has no release), none is claimed

    def test_families_without_a_key_cost_no_request(self):
        fetch = FakeFetch()
        answers, _cache = sigs.read_all("JuanenRac", {"EH3D-SERVER": ("v1", [("a.tar.gz", 1, "u"), ("a.tar.gz.sig", 129, "u")])}, fetch, CONFIG, {})
        self.assertEqual((answers["EH3D-SERVER"]["s"], answers["EH3D-SERVER"]["unk"]), ("unverifiable", 1))
        self.assertEqual(fetch.rest_calls, [])

    def test_verify_activity_replaces_only_the_repositories_with_a_signature_file(self):
        activity = {
            "ARMOR-SERVER-AI": charts.Activity(release_tag="v1.0.0", signature="present", assets=tuple(self.inputs["ARMOR-SERVER-AI"][1])),
            "ARMOR-DOCS": charts.Activity(signature="none"), "ARMOR-HARDWARE": charts.Activity(signature="norelease"), "ARMOR-X": charts.Activity(signature=None)}
        out, cache = sigs.verify_activity("JuanenRac", activity, "t", CONFIG, {}, FakeFetch({self.path: self.rel}, self.files))
        self.assertEqual([out[n].signature for n in activity], ["verified", "none", "norelease", None])
        self.assertEqual(out["ARMOR-SERVER-AI"].sigx["ok"], 1)
        self.assertIn("ARMOR-SERVER-AI", cache)
        broken, _ = sigs.verify_activity("JuanenRac", activity, "t", CONFIG, {}, FakeFetch({self.path: None}, self.files))
        self.assertIsNone(broken["ARMOR-SERVER-AI"].signature)             # a failed read: not verified
        off = sigs.check_config({"enabled": False})[0]
        self.assertEqual(sigs.verify_activity("JuanenRac", activity, "t", off, {}, FakeFetch())[0]["ARMOR-SERVER-AI"].signature, "present")

    def test_the_cache_file_is_written_only_when_it_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data" / "delivery-cache.json"
            self.assertTrue(sigs.save_cache(path, {"A": {"fp": "1", "r": {"s": "verified"}}}, {"B": {"wf": "x"}}))
            self.assertFalse(sigs.save_cache(path, {"A": {"fp": "1", "r": {"s": "verified"}}}, {"B": {"wf": "x"}}))
            self.assertTrue(sigs.save_cache(path, {}))                       # the builds part is kept when none is given
            self.assertEqual(sigs.load_cache(path)["builds"], {"B": {"wf": "x"}})
            path.write_text("{ not json", encoding="utf-8")
            self.assertEqual(sigs.load_cache(path), {})


class ConfigTests(unittest.TestCase):
    def test_defaults_and_wrong_values(self):
        config, problems = sigs.check_config(None)
        self.assertEqual((problems, config["max_asset_bytes"], config["enabled"]), ([], 50 * 1024 * 1024, True))
        config, problems = sigs.check_config({"enabled": "yes", "max_asset_bytes": 5, "max_repos_per_run": True, "keys": {"armor": "nothex", "eh3d": "a" * 64}})
        self.assertEqual(len(problems), 5)
        self.assertEqual(config["keys"]["armor"], sigs.KEY_ARMOR)

    def test_the_real_file_has_valid_signature_settings(self):
        config, problems = sigs.load_config()
        self.assertEqual(problems, [])
        self.assertEqual(config["keys"], {"armor": sigs.KEY_ARMOR, "urtc": sigs.KEY_URTC, "hydra": sigs.KEY_HYDRA})

    def test_the_cache_travels_through_both_steps_of_the_workflow(self):
        text = (HERE.parent / ".github" / "workflows" / "build-dashboard.yml").read_text(encoding="utf-8")
        self.assertEqual(text.count("data/delivery-cache.json"), 2)

    def test_only_public_keys_are_pinned_in_the_code(self):
        text = (HERE.parent / "scripts" / "dashboard_signatures.py").read_text(encoding="utf-8")
        self.assertNotIn("BEGIN", text)
        self.assertNotIn("PRIVATE", text.upper().replace("PRIVATE ONES", "").replace("THE PRIVATE", ""))


class EvidenceTests(unittest.TestCase):
    def test_signature_states_in_the_checklist(self):
        def row(state):
            return evo.checks({"A": "armor"}, {"A": {"x": 1}}, {"A": {}}, {"A": state})["A"][3]
        self.assertEqual([row(s) for s in ("verified", "invalid", "unverifiable", "present", "none", "norelease", None)],
                         [evo.VERIFIED, evo.INVALID, evo.PRESENT, evo.PRESENT, evo.NO, evo.NO, None])


class PipelineTests(unittest.TestCase):
    NOW = pipeline.datetime(2001, 1, 2, 12, 0, 0, tzinfo=pipeline.timezone.utc)

    def fetch(self, runs=None, artifacts=None):
        urls = {}
        for wf, run in (runs or {}).items():
            urls[f"/repos/JuanenRac/R/actions/workflows/{wf}/runs?status=success&per_page=1&exclude_pull_requests=true"] = {"workflow_runs": [run] if run else []}
        for run_id, items in (artifacts or {}).items():
            urls[f"/repos/JuanenRac/R/actions/runs/{run_id}/artifacts?per_page=30"] = {"artifacts": items}
        return FakeFetch(urls)

    def run(self, run_id=7, at="2001-01-02T10:00:00Z"):
        return {"id": run_id, "updated_at": at, "html_url": f"https://github.com/JuanenRac/R/actions/runs/{run_id}", "actor": {"login": "someone"}, "head_branch": "secret-branch",
                "display_title": "a commit title"}

    def test_a_green_build_with_an_artifact_is_built(self):
        fetch = self.fetch({"package-build.yml": self.run()}, {7: [{"expired": False, "expires_at": "2001-02-01T00:00:00Z"}]})
        records, cache = pipeline.read_all("JuanenRac", {"R": ["package-build.yml", "ci.yml"]}, fetch, self.NOW)
        self.assertEqual(records["R"], {"wf": "package-build.yml", "at": "2001-01-02T10:00:00Z", "url": "https://github.com/JuanenRac/R/actions/runs/7", "art": True,
                                        "exp": "2001-02-01T00:00:00Z", "checked": True})
        self.assertEqual(cache, {"R": records["R"]})
        self.assertNotIn("someone", json.dumps(records))        # nothing about who started the run, the branch or the title is kept
        self.assertNotIn("secret-branch", json.dumps(records))
        self.assertNotIn("a commit title", json.dumps(records))

    def test_expired_artifacts_or_no_green_run_do_not_count(self):
        fetch = self.fetch({"apk-build.yml": self.run()}, {7: [{"expired": True, "expires_at": "2000-12-01T00:00:00Z"}]})
        records, _ = pipeline.read_all("JuanenRac", {"R": ["apk-build.yml"]}, fetch, self.NOW)
        self.assertFalse(records["R"]["art"])
        records, cache = pipeline.read_all("JuanenRac", {"R": ["exe-build.yml"], "S": ["ci.yml"]}, self.fetch({"exe-build.yml": None}), self.NOW)
        self.assertEqual((records, cache), ({"R": {}}, {}))       # S has no build workflow: not even asked

    def test_the_newest_of_several_build_workflows_wins(self):
        fetch = self.fetch({"package-build.yml": self.run(1, "2001-01-01T00:00:00Z"), "dist-build.yml": self.run(2, "2001-01-02T00:00:00Z")}, {2: []})
        records, _ = pipeline.read_all("JuanenRac", {"R": ["dist-build.yml", "package-build.yml"]}, fetch, self.NOW)
        self.assertEqual((records["R"]["wf"], records["R"]["art"]), ("dist-build.yml", False))

    def test_the_artifacts_are_not_asked_again_until_they_expire(self):
        fetch = self.fetch({"package-build.yml": self.run()}, {7: [{"expired": False, "expires_at": "2001-02-01T00:00:00Z"}]})
        _r, cache = pipeline.read_all("JuanenRac", {"R": ["package-build.yml"]}, fetch, self.NOW)
        again = self.fetch({"package-build.yml": self.run()})
        records, _ = pipeline.read_all("JuanenRac", {"R": ["package-build.yml"]}, again, self.NOW, {"builds": cache})
        self.assertTrue(records["R"]["art"])
        self.assertEqual(len(again.rest_calls), 1)               # only the list of runs
        later = pipeline.datetime(2001, 3, 1, tzinfo=pipeline.timezone.utc)
        fetch3 = self.fetch({"package-build.yml": self.run()}, {7: [{"expired": True, "expires_at": "2001-02-01T00:00:00Z"}]})
        records, _ = pipeline.read_all("JuanenRac", {"R": ["package-build.yml"]}, fetch3, later, {"builds": cache})
        self.assertFalse(records["R"]["art"])

    def test_a_failed_read_keeps_the_last_record_or_says_nothing(self):
        broken = FakeFetch({"/repos/JuanenRac/R/actions/workflows/package-build.yml/runs?status=success&per_page=1&exclude_pull_requests=true": None})
        last = {"wf": "package-build.yml", "at": "2001-01-01T00:00:00Z", "url": "u", "art": True, "exp": "2001-02-01T00:00:00Z", "checked": True}
        records, _ = pipeline.read_all("JuanenRac", {"R": ["package-build.yml"]}, broken, self.NOW, {"builds": {"R": last}})
        self.assertEqual(records["R"], last)
        records, _ = pipeline.read_all("JuanenRac", {"R": ["package-build.yml"]}, broken, self.NOW, {})
        self.assertIsNone(records["R"])

    def test_a_run_outside_the_repository_is_refused(self):
        run = self.run()
        run["html_url"] = "https://github.com/Other/R/actions/runs/7"
        records, _ = pipeline.read_all("JuanenRac", {"R": ["package-build.yml"]}, self.fetch({"package-build.yml": run}), self.NOW)
        self.assertIsNone(records["R"])

    def test_the_stages_and_what_is_inferred(self):
        built = {"art": True}
        none = {"builtOn": "", "sigKind": "", "signedOn": ""}
        self.assertEqual(pipeline.stages(none, False, None, None, "norelease"), {"state": "undeclared", "inferred": False, "built": None, "signed": None, "published": False})
        self.assertEqual(pipeline.stages(none, True, 3, None, "none")["state"], "release_only")
        got = pipeline.stages(none, True, 3, built, "none")
        self.assertEqual((got["state"], got["inferred"], got["built"]), ("published", True, "inferred"))
        got = pipeline.stages(none, True, 3, built, "verified")
        self.assertEqual((got["state"], got["signed"]), ("published", "inferred"))
        self.assertEqual(pipeline.stages(none, False, None, built, None)["state"], "built")
        self.assertEqual(pipeline.stages(none, True, 0, built, "none")["state"], "built")       # a release without assets is not a publication of the build
        self.assertEqual(pipeline.stages(none, True, 3, {"art": False}, "unverifiable")["state"], "release_only")

    def test_what_a_manifest_declares_is_never_overwritten(self):
        declared = {"builtOn": "local", "sigKind": "dev", "signedOn": "local"}
        got = pipeline.stages(declared, True, 2, {"art": True}, "verified")
        self.assertEqual((got["built"], got["signed"], got["state"]), ("inferred", "declared", "published"))   # built_on local is not gha: the inference may add a stage
        full = {"builtOn": "gha", "sigKind": "release", "signedOn": "local"}
        got = pipeline.stages(full, True, 2, {"art": True}, "verified")
        self.assertEqual((got["built"], got["signed"], got["inferred"]), ("declared", "declared", False))


if __name__ == "__main__":
    unittest.main()
