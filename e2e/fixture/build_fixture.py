# =============================================================================
# JuanenRac profile - e2e/fixture/build_fixture.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Renders the status dashboard from deterministic fixture data, with no network and no token.

Usage: python build_fixture.py [OUT_DIR]

Writes OUT_DIR/full/index.html (a complete dataset), OUT_DIR/healthy/index.html (a complete dataset with nothing wrong), OUT_DIR/minimal/index.html (one project, no activity),
OUT_DIR/partial/index.html (failed lookups and an unreachable API) and OUT_DIR/empty/index.html (nothing at all).
The data is made up: repository names are fake and live under a fixture owner, never queried.
"""
from __future__ import annotations

import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
# In CI the updaters are installed packages; next to this repository they are source checkouts.
for sibling in ("HYDRA-UMC-UPDATER", "URTC-UPDATER", "ARMOR-UPDATER"):
    candidate = ROOT.parent / sibling / "src"
    if candidate.is_dir():
        sys.path.append(str(candidate))

import changelog_stats  # noqa: E402
import code_stats  # noqa: E402
import dashboard_actions as actions_mod  # noqa: E402
import dataclasses  # noqa: E402
import dashboard_charts as charts  # noqa: E402
import dashboard_sentinel as sentinel_mod  # noqa: E402
import dashboard_health as health  # noqa: E402
import dashboard_presence as presence_mod  # noqa: E402
import dashboard_insight as insight_mod  # noqa: E402
import dashboard_integrity as integrity_mod  # noqa: E402
import generate_dashboard as gen  # noqa: E402
from hydra_umc_updater.registry import ProjectEntry  # noqa: E402

os.environ["DASHBOARD_TODAY"] = "2001-12-21"      # the fixture pages always carry the same day

ECOSYSTEMS = ("hydra-umc", "urtc", "armor", "eh3d")
PREFIX = {"hydra-umc": "HYDRA-UMC", "urtc": "URTC", "armor": "ARMOR", "eh3d": "EH3D"}
MATURITY = ("scaffolding", "functional", "established", "production")
EVIDENCE = ("none", "host-test", "simulator", "bench", "field")
ROLES = ("service", "library", "api", "firmware", "app")
STACKS = ("python", "rust", "typescript", "c")
DEPLOYS = ("cm5", "user-pc", "mcu", "mobile")
FAMILIES = ("Core", "Tools", "Network", "Docs")

README = """
<!-- progress:{key} -->
`[██████████▊░░░░░░░░░] {pct}%` - Calculated from real data: the maturity and the evidence that each of its {n} repositories declares.
<!-- /progress:{key} -->
<!-- status:{key} -->
### Ecosystem status

| Area | Status | Progress | Note |
| --- | :---: | --- | --- |
| Software | 🟢 | `█████████▌ 95%` | 9 of 10 repositories are at least functional. |
| Tests | 🟢 | `█████████▊ 98%` | 9 of 10 repositories have automated tests. |
| Continuous integration | 🟡 | `███████░░░ 70%` | 7 of 10 repositories have the last CI run green. |
| Releases | 🟢 | `█████████▊ 97%` | 9 of 10 repositories have published a release. |
| Documentation | 🟢 | `██████████ 100%` | 10 of 10 repositories have the README in the eight languages. |
| Simulation | 🔴 | `██▍░░░░░░░ 24%` | 2 of 10 repositories have been checked in a simulator. |
| Real hardware | 🔴 | `█▏░░░░░░░░ 11%` | 1 of 9 repositories that depend on hardware have been checked. |
| Production | 🔴 | `▊░░░░░░░░░ 8%` | 1 of 10 repositories are established or in production. |
<!-- /status:{key} -->
"""


def _node(name: str, index: int, healthy: bool = False) -> dict:
    """healthy: every CI green and every date within the last days before the fixed clock of the tests (2001-12-21)."""
    ci = "SUCCESS" if healthy else ("SUCCESS", "SUCCESS", "FAILURE", "PENDING")[index % 4]
    month = 12 if healthy else 1 + index % 10
    day = 10 + index % 8 if healthy else (index % 27) + 1
    commit = f"2001-{month:02d}-{day + 1:02d}T09:00:00Z"
    history = [{"messageHeadline": f"Fixture change {n} of {name}", "committedDate": commit, "url": f"https://github.com/JuanenRac/{name}/commit/c{n}"} for n in range(3)]
    if index % 6 == 5:
        history = []        # a repository whose recent commits were not returned
    # The assets of the latest release: a signature file for one in five, a minisig for another, none for another, and the assets not returned for another.
    kind = index % 5
    assets = {"nodes": [{"name": f"{name}.bin"}] + ([{"name": f"{name}.bin.sig"}] if kind == 0 else [{"name": f"{name}.bin.minisig"}] if kind == 3 else [])} if kind != 2 else None
    release = {"tagName": f"v0.{index % 7}.{index % 3}", "publishedAt": f"2001-{month:02d}-{day:02d}T10:00:00Z"}
    if assets is not None:
        release["releaseAssets"] = assets
    return {
        "name": name,
        "latestRelease": None if index % 5 == 4 and not healthy else release,
        "defaultBranchRef": {"target": {"committedDate": commit, "statusCheckRollup": {"state": ci}, "history": {"nodes": history}}},
    }


def dataset(per_ecosystem: int = 10, healthy: bool = False):
    entries, results, eco, raw, nodes = [], {}, {}, {}, []
    index = 0
    for key in ECOSYSTEMS:
        for number in range(per_ecosystem):
            name = f"{PREFIX[key]}-FIXTURE-{number:02d}"
            description = f"Fixture project number {number} of {key} (searchable text zzdesc{index})"
            entry = ProjectEntry(
                name=name, stack=STACKS[index % 4], version_file="VERSION", pattern=r"\d+\.\d+\.\d+",
                note=description, notes=description, deploy=DEPLOYS[index % 4], maturity=MATURITY[index % 4],
                role=ROLES[index % 5], family=FAMILIES[index % 4],
            )
            entries.append(entry)
            ok = index % 9 != 8
            results[name] = SimpleNamespace(version=f"0.{index % 7}.{index % 3}" if ok else None, error=None if ok else "not found", http_status=200 if ok else 404, url="https://example.invalid/" + name)
            eco[name] = key
            data = {"evidence": EVIDENCE[index % 5], "maturity": MATURITY[index % 4]}
            if index % 3 == 0:
                data["hardware_bound"] = True       # declares real hardware (some with no bench or field evidence)
            if index % 4 == 0:
                data.update({"built_on": "gha", "signature_kind": "release", "signed_on": "local", "last_build_artifact_url": f"https://github.com/JuanenRac/{name}/actions/runs/{index + 1}"})
            elif index % 4 == 1:
                data["built_on"] = "gha"                           # built on GitHub Actions, nothing declared about the signature
            elif index % 7 == 3:
                data.update({"signature_kind": "dev", "signed_on": "unknown", "built_on": "not-a-known-value"})
            deps = []
            if number % 2 == 1:
                deps.append(f"{PREFIX[key]}-FIXTURE-{number - 1:02d}")
            if key == "hydra-umc" and number == 0:
                deps.append(f"{PREFIX[key]}-FIXTURE-01")             # with 01 depending on 00: a cycle
            if key == "hydra-umc" and number == 7:
                deps.append("HYDRA-UMC-GHOST-REPO")                  # a repository that does not exist
            if key == "urtc" and number == 3:
                deps.append("HYDRA-UMC-FIXTURE-00")                  # another ecosystem
            if deps:
                data["depends_on"] = deps
            if number == 9:
                data["parent"] = f"{PREFIX[key]}-FIXTURE-00"
            raw[name] = integrity_mod.RawManifest(ecosystem=key, data=data)
            nodes.append(_node(name, index, healthy))
            index += 1
    return entries, results, eco, raw, _with_verification(_with_presence(charts.parse_activity(nodes)), healthy)


def _with_presence(activity: dict) -> dict:
    """The presence of the signature files comes from the names of the assets (no request); the attestations take turns to be present, absent, partial and
    unknown, the way the answers of the API would fall."""
    found, _cache = presence_mod.assess("JuanenRac", activity, None, {**presence_mod.DEFAULT_CONFIG, "attestations": False}, None, "2001-12-21")
    cycle = (("present", 1, 1), ("absent", 1, 0), ("partial", 2, 1), ("unknown", 0, 0))
    out = dict(activity)
    turn = 0
    for name in sorted(found):
        entry = dict(found[name])
        if entry["sg"] not in ("na", "unknown"):
            entry["at"], entry["an"], entry["ak"] = cycle[turn % 4]
            turn += 1
        out[name] = dataclasses.replace(activity[name], presence=entry)
    return out


def _with_verification(activity: dict, healthy: bool) -> dict:
    """What the verification of the signatures would have answered for the fixture (no network): the repositories with a .sig take turns to be verified, invalid
    (never in the healthy variant) and not verifiable; a .minisig is never verifiable here. The detail is the one dashboard_signatures.aggregate gives."""
    out = dict(activity)
    turn = 0
    for name in sorted(activity):
        act = activity[name]
        if act.signature != "present":
            continue
        names = [a[0] for a in act.assets]
        if any(n.endswith(".sig") for n in names):
            state = ("verified", "invalid", "unverifiable")[turn % 3]
            turn += 1
            if healthy and state == "invalid":
                state = "verified"
        else:
            state = "unverifiable"
        detail = {"verified": {"ok": 2, "bad": 0, "unk": 0, "sch": ["armor-fw/1", "armor-fw/1 (hash)"], "why": [], "ho": 0},
                  "invalid": {"ok": 1, "bad": 1, "unk": 0, "sch": ["armor-pkg/1"], "why": ["mismatch"], "ho": 0},
                  "unverifiable": {"ok": 0, "bad": 0, "unk": 1, "sch": [], "why": ["format" if not any(n.endswith(".sig") for n in names) else "family"], "ho": 0}}[state]
        out[name] = dataclasses.replace(act, signature=state, sigx=detail)
    return out


def builds_for(entries) -> dict:
    """The inferred builds (what dashboard_pipeline.read_all returns): every third repository has a green build with an artifact, one in six a green build whose
    artifact expired, the rest have no build workflow."""
    out = {}
    for index, entry in enumerate(entries):
        if index % 3 == 0:
            out[entry.name] = {"wf": "package-build.yml", "at": "2001-12-19T10:00:00Z", "url": f"https://github.com/JuanenRac/{entry.name}/actions/runs/{100 + index}", "art": True}
        elif index % 6 == 1:
            out[entry.name] = {"wf": "firmware-build.yml", "at": "2001-10-01T10:00:00Z", "url": f"https://github.com/JuanenRac/{entry.name}/actions/runs/{100 + index}", "art": False}
    return out


def signals_for(entries, activity) -> dict:
    """Delivery and quality facts of every repository but one in six (those stay unverified)."""
    out = {}
    for index, entry in enumerate(entries):
        if index % 6 == 3:
            continue
        out[entry.name] = {"releases": index % 25, "readmes": 8 if index % 7 else 3, "tests": index % 3 != 0, "ci": activity[entry.name].ci == "success"}
    return out


def ci_evidence_for(entries) -> dict:
    """What the CI of the repositories published (read at the fixed day 2001-12-21): one repository in eight shows each way of being verified or not."""
    type_of = {"none": "unit", "host-test": "host-test", "simulator": "simulator", "bench": "bench", "field": "field"}
    records, errors = {}, {}
    for index, entry in enumerate(entries):
        name = entry.name
        declared = EVIDENCE[index % 5]

        def record(test_type, result="pass", date="2001-12-15", branch="main"):
            data = {"repo": name, "workflow": "ci.yml", "commit": f"{index:040x}"[-40:], "branch": branch, "date": date + "T09:00:00Z", "version": "0.1.0",
                    "test_type": test_type, "result": result, "environment": "ubuntu-24.04", "hardware": None,
                    "url": f"https://github.com/JuanenRac/{name}/actions/runs/{1000 + index}"}
            if test_type in ("bench", "field"):
                data["hardware"] = {"bound": True, "device": "fixture board"}
            return data
        kind = index % 8
        if kind == 1:
            records[name] = [record(type_of[declared])]
        elif kind == 2:
            records[name] = [record("host-test")]
        elif kind == 3:
            records[name] = [record("host-test", date="2001-01-01")]
        elif kind == 4:
            records[name] = [record(type_of[declared], "fail")]
        elif kind == 5:
            broken = record("host-test")
            del broken["workflow"]
            records[name] = [broken]
        elif kind == 6:
            errors[name] = "HTTP 503"
        elif kind == 7:
            records[name] = [record("host-test", branch="feature")]
    return {"records": records, "errors": errors}


def facts_for(entries) -> dict:
    """Creation date, release dates and top-level files of every repository but one in seven (those stay unverified)."""
    out = {}
    for index, entry in enumerate(entries):
        if index % 7 == 6:
            continue
        files = ["README.md", "src"] + (["tests", "tests/integration"] if index % 3 == 0 else ["tests"] if index % 3 == 1 else [])
        out[entry.name] = {"created": f"2001-{1 + index % 9:02d}-{1 + index % 27:02d}T08:00:00Z",
                           "releases": [f"2001-12-{10 + index % 10:02d}T10:00:00Z"] if index % 5 != 4 else [], "files": files}
    return out


def weekly_for(entries) -> dict:
    """Commits per week for every repository but one in nine (the statistics of those were not ready)."""
    weeks = insight_mod.week_starts("2001-12-21")
    return {e.name: {w: (index * 3 + n * 2) % 11 for n, w in enumerate(weeks)} for index, e in enumerate(entries) if index % 9 != 4}


PLANNED = {
    "hydra-umc": [
        {"title": "Fixture card in progress", "repository": "HYDRA-UMC-FIXTURE-00", "status": "In progress", "priority": "High", "hardware": "None", "blocked": "None"},
        {"title": "Fixture card blocked", "repository": "HYDRA-UMC-FIXTURE-01", "status": "Blocked", "priority": "Normal", "hardware": "CM5", "blocked": "Needs a real board"},
        {"title": "Fixture card done", "repository": "", "status": "Done", "priority": "Low", "hardware": "None", "blocked": "None"},
    ],
    "urtc": [{"title": "Fixture URTC backlog card", "repository": "URTC-FIXTURE-00", "status": "Backlog", "priority": "Critical", "hardware": "None", "blocked": "None"}],
    "armor": [],
    "eh3d": [{"title": "Fixture EH3D ready card", "repository": "", "status": "Ready", "priority": "Normal", "hardware": "None", "blocked": "None"}],
}

def declared_tests(index: int) -> int:
    """The number of tests the fixture repository of this index declares today (a made-up, deterministic figure)."""
    return 12 + (index * 37) % 400


def tests_for(entries, eco, errors: bool = True) -> dict:
    """What dashboard_tests.read_all returns for the fixture: most repositories declare tests (the glance file for HYDRA-UMC and URTC, the README for the others),
    one in seven counts checks instead of tests, one in eleven declares nothing and (with `errors`) one in thirteen could not be read."""
    records, undeclared, failed = {}, [], {}
    for index, entry in enumerate(entries):
        name = entry.name
        if index % 11 == 10:
            undeclared.append(name)
        elif errors and index % 13 == 12:
            failed[name] = "HTTP 502"
        elif index % 7 == 6:
            records[name] = {"n": 40000 + index * 123, "unit": "checks", "src": "readme"}
        else:
            records[name] = {"n": declared_tests(index), "unit": "tests", "src": "glance" if eco[name] in ("hydra-umc", "urtc") else "readme"}
    return {"records": records, "undeclared": undeclared, "errors": failed, "glance": {}}


CODE_TYPES = ("firmware", "apps", "services", "tools", "docs")
CODE_LANGS = ("Python", "Rust", "C++", "TypeScript", "Kotlin")


ENTRY_TITLES = (
    "**Fix:** the parser no longer crashes on an empty file.", "**Added:** support for a second input format.", "**Security:** a path is checked before it is opened.",
    "**Faster start:** the cache is warmed once.", "**Documentation:** the guide explains the settings.", "**Tests:** more cases for the limits.",
    "**Cleanup:** the helpers moved to one module.", "**Changed:** the default is now stricter.", "**Panel:** shows the figures of the day.",
)


def _changelog_text(index: int, scale: int) -> str:
    """A CHANGELOG.md made up for the fixture: a few versions with entries of every kind, one with Keep a Changelog sub-headings."""
    lines = ["# Changelog", "", "## [Unreleased]", ""]
    for n in range(1 + index % 4):
        lines.append("- " + ENTRY_TITLES[(index + n * 2) % len(ENTRY_TITLES)])
    for v in range(max(1, (3 + index % 9) * scale // 100)):
        lines += ["", f"## [0.{(3 + index % 9) - v}.0] - Version {v}", ""]
        if index % 11 == 3 and v == 0:
            lines += ["### Fixed", "", "- **Crash:** a second fix.", "", "### Added", "", "- **Feature:** another item.", "- Plain item with no words of a kind.", ""]
            continue
        for n in range(2 + (index + v) % 6):
            lines.append("- " + ENTRY_TITLES[(index + v + n) % len(ENTRY_TITLES)])
    return chr(10).join(lines) + chr(10)


def _code_record(index: int, key: str, scale: int = 100) -> dict:
    """The figures of one repository of the fixture (counted by nothing: made up, but shaped like the real record and adding up the way the counter does)."""
    main = CODE_LANGS[index % 5]
    code, comment, blank = (1000 + index * 137) * scale // 100, (100 + index * 11) * scale // 100, (150 + index * 9) * scale // 100
    tests, docs = (300 + index * 53) * scale // 100, (400 + index * 41) * scale // 100
    minor = code // 10
    record = {
        "eco": key, "type": CODE_TYPES[index % 5], "state": "ok", "pushed": "2001-12-20", "commit": f"2001-12-{10 + index % 11:02d}",
        "files": 20 + index, "size": 90000 + index * 7919, "skipped": 0,
        "langs": {main: {"files": 8 + index % 5, "code": code - minor + tests, "comment": comment, "blank": blank},
                  "Shell": {"files": 2, "code": minor, "comment": 5, "blank": 3}},
        "code": {"files": 10 + index % 5, "code": code, "comment": comment, "blank": blank},
        "tests": {"files": 3 + index % 4, "code": tests, "comment": 20, "blank": 30, "cases": 40 + index * 3},
        "docs": {"files": 9 + index % 3, "lines": docs, "blank": 80}, "l10n": {"files": index % 9, "lines": (index % 9) * 12}, "data": {"files": 2, "lines": 300},
    }
    if index % 3 == 0:
        record["declared_tests"] = 90 + index * 5
    record["changes"] = changelog_stats.summarize(_changelog_text(index, scale), code_stats.load_config()["changelog"]) if index % 12 != 11 else None
    record["rel"] = {"tags": 4 + index % 9, "last": f"2001-12-{10 + index % 11:02d}", "d30": 1 + index % 4, "d90": 2 + index % 6, "gap": 3.5 + index % 5} if index % 10 != 9 else None
    return record


def code_for(entries, eco, history_days: int = 45, age_days: int = 0) -> tuple[dict, list]:
    """The documents of scripts/code_stats.py for the fixture: one repository in seventeen is a last known figure, one is not measured, and the history grows."""
    repos = {}
    for index, entry in enumerate(entries):
        record = _code_record(index, eco[entry.name])
        if index == 13:
            record = {"eco": eco[entry.name], "type": CODE_TYPES[index % 5], "state": "unread", "pushed": None}
        elif index % 17 == 5:
            record["state"] = "lastknown"
        repos[entry.name] = record
    config = code_stats.load_config()
    day = (date(2001, 12, 21) - timedelta(days=age_days)).isoformat()
    document = code_stats.make_document(day, config, repos)
    points = []
    for back in range(history_days, 0, -1):
        grown = {name: _code_record(i, eco[name], 60 + (history_days - back) * 40 // max(1, history_days)) for i, name in enumerate(repos) if repos[name]["state"] != "unread"}
        points.append(code_stats.snapshot_point((date(2001, 12, 21) - timedelta(days=back)).isoformat(), grown))
    points.append(code_stats.snapshot_point(day, repos))
    return document, points


SCRIPT_ACTIONS = [("actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803", "sha"), ("actions/setup-python@v5", "tag"), ("actions/upload-artifact@v4", "tag"),
                  ("softprops/action-gh-release@master", "branch"), ("JuanenRac/shared-checks@d23441a48e516b6c34aea4fa41551a30e30af803", "sha"), ("./.github/actions/setup", "local"),
                  ("docker://alpine:3.19", "docker"), ("pnpm/action-setup@v4", "tag")]
SCRIPT_TRIGGERS = [["push", "pull_request"], ["schedule", "workflow_dispatch"], ["release"], ["push", "workflow_dispatch", "workflow_run"], ["workflow_call"], ["push", "other"]]


def scripts_for(entries, eco, age_days: int = 0) -> dict:
    """The document of the workflows and own scripts for the fixture (made up, with the shape of scripts/scripts_stats.py): one repository in nine has none,
    one in seventeen is a last known figure, one is not read."""
    config = code_stats.load_config()
    records = {}
    for index, entry in enumerate(entries):
        record = {"eco": eco[entry.name], "type": CODE_TYPES[index % 5], "state": "ok"}
        if index == 13:
            record["state"] = "unread"
        else:
            if index % 17 == 5:
                record["state"] = "lastknown"
            workflows = [] if index % 9 == 8 else [[f"flow-{n}.yml", f"Flow {n}", SCRIPT_TRIGGERS[(index + n) % 6], 1 + (index + n) % 3, ["ubuntu-latest"]] for n in range(1 + index % 4)]
            acts: dict = {}
            for n in range(len(workflows) * 2):
                key, pin = SCRIPT_ACTIONS[(index + n) % len(SCRIPT_ACTIONS)]
                acts.setdefault(key, [0, pin])[0] += 1 + (n % 2)
            sc = {lang: [1 + (index + k) % 5, 20 + (index * 7 + k * 13) % 200] for k, lang in enumerate(("py", "sh", "ps1", "bat", "js")) if (index + k) % 3 != 2}
            record["scripts"] = {"wf": workflows, "acts": acts, "sc": sc}
        records[entry.name] = record
    day = (date(2001, 12, 21) - timedelta(days=age_days)).isoformat()
    return code_stats.scripts_document(day, config, records, {n: r for n, r in records.items() if r["state"] == "lastknown"})


ACTIONS_NOW = datetime(2001, 12, 21, 12, 0, 0, tzinfo=timezone.utc)


def actions_for(entries, healthy: bool = False) -> dict:
    """What dashboard_actions.read_all returns for the fixture, built with the real summary function from made-up runs: most repositories build every few hours,
    one in four fails now and then (never with `healthy`), one in nine has no workflows, one in twelve could not be read (never with `healthy`)."""
    config = actions_mod.check_config(None)[0]
    repos = {}
    for index, entry in enumerate(entries):
        if index % 9 == 8:
            repos[entry.name] = {"state": "none", "bf": 0, "bs": 0}
            continue
        if not healthy and index % 12 == 11:
            repos[entry.name] = {"state": "unread"}
            continue
        runs = []
        for k in range(1 + (index * 5) % 14):
            end = ACTIONS_NOW - timedelta(minutes=17 + k * (45 + (index % 5) * 30) + index)
            result = "success"
            if not healthy and index % 4 == 1 and k % 3 == 0:
                result = "failure"
            elif k % 7 == 6:
                result = "cancelled"
            started = end - timedelta(seconds=40 + (index * 37 + k * 11) % 900)
            runs.append({"status": "completed", "conclusion": result, "created_at": started.isoformat(), "run_started_at": started.isoformat(), "updated_at": end.isoformat(), "path": ".github/workflows/ci.yml"})
        if index % 10 == 3:
            runs.append({"status": "in_progress", "conclusion": None, "created_at": (ACTIONS_NOW - timedelta(minutes=3)).isoformat(), "run_started_at": (ACTIONS_NOW - timedelta(minutes=3)).isoformat(),
                         "updated_at": ACTIONS_NOW.isoformat(), "path": ".github/workflows/ci.yml"})
        record = actions_mod.summarize(runs, ACTIONS_NOW, config)
        record["bf"] = 0 if healthy else (2 if index % 4 == 1 else 0)
        record["bs"] = 1 if (not healthy and index % 13 == 5) else 0
        repos[entry.name] = record
    return {"asof": ACTIONS_NOW.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": repos, "errors": sum(1 for r in repos.values() if r["state"] == "unread")}


def sentinel_for(entries, eco, activity, history, actions, healthy: bool = False) -> dict:
    """The document of the tab Sentinel for the fixture, made with the real rules from a made-up reading: some repositories are red, some wait for a version (a
    CHANGELOG with entries and an old or no release), some lack the ruleset, a few settings are readable and one in twelve could not be read (never with `healthy`)."""
    config = sentinel_mod.check_config(None)[0]
    if healthy:
        config["compute_warn_minutes_24h"] = 100000      # the made-up builds of the fixture use more than a real day would
    repos = {}
    for index, entry in enumerate(entries):
        if not healthy and index % 12 == 11:
            repos[entry.name] = {"state": "unread"}
            continue
        red = [] if healthy or index % 5 != 2 else [{"wf": "ci.yml", "streak": 1 + index % 3, "since": f"2001-12-{19 + index % 3:02d}T0{index % 9}:15:00Z"}]
        published = None if index % 4 == 0 and index % 8 != 0 else ("2001-12-10T10:00:00Z" if index % 3 == 0 else "2001-12-20T10:00:00Z")
        record = {"state": "ok", "tag": None if published is None else f"0.1.{index % 7}", "published": published, "entries": (1 + index % 5) if index % 4 == 0 and not healthy else 0,
                  "ci": red, "checked": 1 + index % 2, "rs": True if healthy or index % 6 != 5 else False, "perm": None}
        if index % 7 == 0:
            record["perm"] = {"sha": healthy or index % 14 == 0, "allowed": healthy or index % 14 == 0}
        repos[entry.name] = record
    read = {"asof": ACTIONS_NOW.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": repos}
    return sentinel_mod.assemble(read, eco, config, {n: a.signature for n, a in activity.items()}, actions, history, "2001-12-21", ecosystem_of=eco)


def actions_block(entries, history, healthy: bool = False) -> dict:
    return gen.dashboard_actions.build(actions_for(entries, healthy), None, {e.name: 'x' for e in entries}, history, '2001-12-21')


def actions_history(days: int = 12) -> dict:
    """The compact daily summaries (by date) the fixture history carries."""
    return {(date(2001, 12, 21) - timedelta(days=back)).isoformat(): {"runs": 60 + back * 7 % 23, "ok": 50 + back * 5 % 17, "fail": 3 + back % 5, "other": 2, "min": 180 + back * 13}
            for back in range(1, days + 1) if back != 4}


AREAS = ("software", "tests", "ci", "releases", "docs", "simulation", "hardware", "production")


def history_for(days: int = 45) -> list[dict]:
    """One snapshot a day before 2001-12-21, rising a little every day; two days are missing (never filled in) and one area is unknown on one day."""
    today = date(2001, 12, 21)
    out = []
    for back in range(days, 0, -1):
        if back in (20, 21):
            continue
        day = today - timedelta(days=back)
        progress = {eco: max(0, 40 + 7 * i - back // 3) for i, eco in enumerate(ECOSYSTEMS)}
        areas = {eco: {area: max(0, 20 + 9 * j + 3 * i - back // 4) for j, area in enumerate(AREAS)} for i, eco in enumerate(ECOSYSTEMS)}
        if back == 10:
            del areas["urtc"]["ci"]
        out.append({"date": day.isoformat(), "progress": progress, "areas": areas, **({} if back == 44 else {"repos": repos_at(back)}),
                    **({"tests": tests_at(back)} if back <= 30 else {}),
                    **({"actions": actions_history()[day.isoformat()]} if day.isoformat() in actions_history() else {}),
                    **({"sentinel": {"red": 2 + back % 4, "cand": 1 + back % 3, "gaps": 4 + back % 2, "min": 200 + back * 11}} if 0 < back <= 12 and back != 4 else {})})   # the counts of the tests were recorded only in the last 30 days   # an old snapshot with no repositories
    return out


def tests_at(back: int) -> dict:
    """The tests the fixture repositories declared `back` days ago: fewer before, and the repositories with the index 5 mod 17 had not started to declare them yet."""
    out, index = {}, 0
    for key in ECOSYSTEMS:
        for number in range(10):
            if index % 7 != 6 and index % 11 != 10 and not (index % 17 == 5 and back > 12):
                out[f"{PREFIX[key]}-FIXTURE-{number:02d}"] = max(1, declared_tests(index) - back // 3 - (index % 4))
            index += 1
    return out


def repos_at(back: int) -> dict:
    """What the snapshot of `back` days ago recorded for each fixture repository: one in five was a level lower (and had an older version) before the last 20 days."""
    out, index = {}, 0
    for key in ECOSYSTEMS:
        for number in range(10):
            level = index % 4
            older = back > 20 and index % 5 == 0
            out[f"{PREFIX[key]}-FIXTURE-{number:02d}"] = [max(0, level - 1) if older else level, f"0.{index % 7}.{index % 3}" if not older else "0.0.0"]
            index += 1
    return out


def _rack(name: str, source: str, alarms: bool) -> dict:
    """A rack snapshot in the shape URTC-COMMON writes (rack_status.snapshot, schema 1); the values are made up for the tests."""
    slots = []
    for i in range(8):
        occupied = i < 3
        slots.append({"slot": i, "occupied": occupied, "tool_id": (i + 1) if occupied else None, "serial": (7 + i) if occupied else None,
                      "unit": f"{i + 1}:{7 + i}" if occupied else None, "target_c": 250 if i == 1 else 0, "expired": alarms and i == 2,
                      "wear": {"cycles": 3 + i, "heater_seconds": 90 * (i + 1), "faults": 0, "maintenance": alarms and i == 0} if occupied else None,
                      "thermal": ("overshoot" if alarms and i == 1 else "reached" if i == 1 else "idle_ok") if occupied else None,
                      "maintenance_due": bool(alarms and i == 0)})
    found = ([f"slot 0: maintenance due for unit 1:7", "slot 2: pre-heat limit reached, the target was switched off", "slot 1: thermal check says overshoot"] if alarms else [])
    return {"schema": 1, "name": name, "source": source, "occupied": 3, "slot_count": 8, "heating": 1, "maintenance_due": 1 if alarms else 0, "alarms": found, "slots": slots}


RACK_ALARM = (_rack("Fixture rack <b>", "simulation", True), "")
RACK_QUIET = (_rack("Fixture bench rack", "bench-log", False), "")
RACK_INVALID = (None, "schema 2 is not 1")

GENERATION = gen.dashboard_robust.Generation(built="2001-12-20T08:31:12", seconds=47.6, asof="2001-12-20", steps=(
    ("versions", 38, 40), ("manifests", 36, 41), ("commits", 20, 40), ("activity", 40, 40)))

PINS = {
    "armor": {"source": "contract_pins", "read": True, "current": "0.8.1.1", "rows": [
        {"repo": "ARMOR-FIXTURE-00", "pin": "0.8.0.7", "state": "behind"}, {"repo": "ARMOR-FIXTURE-01", "pin": "0.8.1.1", "state": "current"}]},
    "urtc": {"source": "lock_files", "read": True, "partial": True, "current": "0.2.3", "rows": [
        {"repo": "URTC-FIXTURE-00", "pin": "0.1.9", "state": "behind"}]},
    "hydra-umc": {"source": "none", "read": True, "current": None, "rows": []},
}

BUILD = health.BuildInfo("https://github.com/JuanenRac/JuanenRac/actions/runs/123456", "2001-12-20T08:30:00Z")


def build_full() -> str:
    entries, results, eco, raw, activity = dataset()
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    meta = {e.name: gen.RepoMeta(commit_subject=f"Fixture commit for {e.name}", commit_url=f"https://github.com/JuanenRac/{e.name}/commit/abc") for e in entries[:20]}
    issues = [
        integrity_mod.Issue("unlisted_manifest", "URTC-FIXTURE-GHOST", "urtc", "the repository has a manifest the dashboard did not list"),
        integrity_mod.Issue("invalid_manifest", "ARMOR-FIXTURE-BAD", "armor", "version file missing"),
    ]
    cover = integrity_mod.Coverage(len(entries), len(entries) + 3, ("JuanenRac", "fixture-plain-a", "fixture-plain-b"))
    return gen.render_html(entries, results, meta, eco, issues, cover, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=history_for(), facts=facts_for(entries), weekly=weekly_for(entries),
                           planned_milestones=PLANNED, generation=GENERATION, rack=RACK_ALARM, ci_evidence=ci_evidence_for(entries),
                           tests_read=tests_for(entries, eco), actions_read=actions_for(entries), builds=builds_for(entries),
                           sentinel_doc=sentinel_for(entries, eco, activity, history_for(), actions_block(entries, history_for())),
                           pins_doc=PINS, code_doc=code_for(entries, eco)[0], code_history=code_for(entries, eco)[1], scripts_doc=scripts_for(entries, eco))


def build_stale() -> str:
    """The full page when GitHub could not be read in the last generation: the CI, release and commit data are the last known version of 2001-12-19."""
    entries, results, eco, raw, activity = dataset()
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    generation = gen.dashboard_robust.Generation(built="2001-12-20T08:31:12", seconds=12.2, asof="2001-12-19", steps=(
        ("versions", 40, 40), ("manifests", 40, 40), ("commits", 0, 40), ("activity", 0, 40)))
    return gen.render_html(entries, results, {}, eco, [], None, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=history_for(), facts=facts_for(entries), weekly=weekly_for(entries),
                           planned_milestones=PLANNED, generation=generation, stale_date="2001-12-19", rack=RACK_QUIET, ci_evidence=ci_evidence_for(entries),
                           tests_read=None, actions_read=None, actions_cache=actions_for(entries),
                           sentinel_saved=sentinel_for(entries, eco, activity, history_for(), actions_block(entries, history_for())),
                           code_doc=code_for(entries, eco, age_days=4)[0], code_history=code_for(entries, eco, age_days=4)[1],
                           scripts_doc=scripts_for(entries, eco, age_days=4))


def build_single() -> str:
    """The full page with no earlier history: only today's snapshot exists, so no line can be drawn."""
    entries, results, eco, raw, activity = dataset()
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    return gen.render_html(entries, results, {}, eco, [], None, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=[], facts=facts_for(entries), weekly=weekly_for(entries),
                           planned_milestones=PLANNED, ci_evidence=ci_evidence_for(entries), tests_read=tests_for(entries, eco), actions_read=actions_for(entries), builds=builds_for(entries),
                           sentinel_doc=sentinel_for(entries, eco, activity, [], actions_block(entries, [])),
                           code_doc=code_for(entries, eco, history_days=0)[0], code_history=code_for(entries, eco, history_days=0)[1],
                           scripts_doc=scripts_for(entries, eco))


def build_healthy() -> str:
    """Every CI green, recent activity (with the clock at 2001-12-21), nothing unresolved and nothing unread: the only variant that may say "no alerts"."""
    entries, results, eco, raw, activity = dataset(healthy=True)
    for result in results.values():
        result.version, result.error, result.http_status = "0.1.0", None, 200
    readme = "".join(README.format(key=k, pct=40 + 7 * i, n=10) for i, k in enumerate(ECOSYSTEMS))
    cover = integrity_mod.Coverage(len(entries), len(entries), ())
    return gen.render_html(entries, results, {}, eco, [], cover, raw_manifests=raw, activity=activity, readme_text=readme,
                           signals=signals_for(entries, activity), build=BUILD, history=history_for(60), facts=facts_for(entries), weekly=weekly_for(entries),
                           planned_milestones=PLANNED, generation=GENERATION, rack=RACK_QUIET, tests_read=tests_for(entries, eco, errors=False), actions_read=actions_for(entries, healthy=True), builds=builds_for(entries),
                           sentinel_doc=sentinel_for(entries, eco, activity, history_for(60), actions_block(entries, history_for(60), healthy=True), healthy=True),
                           code_doc=code_for(entries, eco)[0], code_history=code_for(entries, eco)[1], scripts_doc=scripts_for(entries, eco))


def build_minimal() -> str:
    entries, results, eco, raw, _ = dataset(per_ecosystem=1)
    entries, eco = entries[:1], {entries[0].name: eco[entries[0].name]}
    results = {entries[0].name: results[entries[0].name]}
    results[entries[0].name].version = "0.1.0"
    return gen.render_html(entries, results, {}, eco, [], None, raw_manifests={}, activity={}, readme_text="")


def build_partial() -> str:
    entries, results, eco, raw, _ = dataset(per_ecosystem=4)
    for result in results.values():  # every version lookup failed
        result.version, result.error, result.http_status = None, "HTTP 403 rate limited", 403
    issues = [integrity_mod.Issue("api", "repository listing", "", "the GitHub API did not answer")]
    cover = integrity_mod.Coverage(len(entries), None, ())
    return gen.render_html(entries, results, {}, eco, issues, cover, raw_manifests={}, activity={}, readme_text="", rack=RACK_INVALID)


def build_empty() -> str:
    return gen.render_html([], {}, {}, {}, [], None, raw_manifests={}, activity={}, readme_text="")


BUILDERS = {"full": build_full, "stale": build_stale, "single": build_single, "healthy": build_healthy, "minimal": build_minimal, "partial": build_partial, "empty": build_empty}


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "out"
    for name, builder in BUILDERS.items():
        target = out / name
        target.mkdir(parents=True, exist_ok=True)
        text = builder()
        (target / "index.html").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
        print(f"{name}: {target / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
