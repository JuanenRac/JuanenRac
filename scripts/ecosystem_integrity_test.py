#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/ecosystem_integrity_test.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Reconciles every place the ecosystem is counted and explains each figure.

The same family of repositories is described by several sources that are written by different
means: the public repositories of the owner, the manifest each one carries, the catalogue of the
profile README and its seven translations, ecosystem-catalog.json, the published dashboard and the
progress numbers. This tool reads them all and answers two questions:

  * do they agree? (every difference is a finding with its reason), and
  * where does each number come from? (the "figures" part of the report: why N projects, why M
    valid manifests, how many of them each ecosystem has).

Every finding has one of four states, and a failure to read is never turned into health:

  ok          checked, and it agrees
  failed      checked, and it is a real incoherence (the exit code is 1)
  pending     known and expected to be completed later (an empty repository, a release not yet made)
  unverified  it could not be checked (an API error, a missing source): says nothing about health

The decision logic (`reconcile`) is pure and takes plain data; the network sits in `collect`,
which takes the fetch functions as arguments so the tests can simulate every case.
Stdlib only.

Usage:
  python scripts/ecosystem_integrity_test.py                  # reads GitHub, prints the report
  python scripts/ecosystem_integrity_test.py --json out.json  # also writes the machine-readable report
  python scripts/ecosystem_integrity_test.py --fail-on-unverified
Exit code: 0 no incoherence (unverified and pending items are listed), 1 a real incoherence,
2 nothing could be verified or --fail-on-unverified found items that could not be checked.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import catalog_check  # noqa: E402
import dashboard_integrity as di  # noqa: E402
import ecosystem_progress as progress  # noqa: E402

OK, FAILED, PENDING, UNVERIFIED = "ok", "failed", "pending", "unverified"
STATES = (FAILED, UNVERIFIED, PENDING, OK)

# The ecosystem section of the README a manifest key belongs to: the updater of the suite lives in the EH3D section.
SECTION_OF = {"hydra-umc": "hydra-umc", "urtc": "urtc", "armor": "armor", "eh3d": "eh3d", "electro-hobby-3d": "eh3d"}
LABEL_OF = {"hydra-umc": "HYDRA-UMC", "urtc": "URTC", "armor": "A.R.M.O.R.", "eh3d": "EH3D", "electro-hobby-3d": "Tools"}
VERSION_RE = re.compile(r"^\d+(\.\d+){1,3}$")
TAG_RE = re.compile(r"^v?(\d+(?:\.\d+){1,3})")
_DATA_RE = re.compile(r'<script type="application/json" id="dashboard-data">(.*?)</script>', re.S)
_ISSUE_RE = re.compile(r'<li><code>([^<]*)</code> <span class="integrity-kind"[^>]*>([^<]*)</span> <span class="integrity-eco">[^<]*</span> <span class="integrity-detail">([^<]*)</span></li>')
_COVER_RE = re.compile(r'data-listed="(\d+)" data-public="(\d+)"')


@dataclass(frozen=True)
class Finding:
    check: str
    state: str
    subject: str
    detail: str


@dataclass(frozen=True)
class Figure:
    label: str
    value: str
    why: str


@dataclass(frozen=True)
class RepoInfo:
    name: str
    branch: str = "main"
    empty: bool = False
    archived: bool = False


@dataclass(frozen=True)
class ManifestRead:
    """status: ok (a JSON object was read) | invalid (found, not a JSON object) | absent (no manifest of any ecosystem) | error (it could not be read)."""
    status: str
    ecosystem: str = ""
    data: "dict | None" = None
    detail: str = ""
    also: tuple = ()       # further ecosystems whose manifest file the repository carries too


@dataclass
class Sources:
    owner: str
    repos: "list[RepoInfo] | None"
    manifests: dict = field(default_factory=dict)         # repo name -> ManifestRead
    readmes: dict = field(default_factory=dict)           # file name -> text
    catalog_json: "dict | None" = None
    dashboard: "dict | None" = None                       # the data the page embeds for its script
    dashboard_issues: tuple = ()                          # (repo, kind, detail) of the "Errors / unknown" list of the page
    dashboard_cover: "tuple | None" = None                # (listed, public) the page states
    history: "dict | None" = None                         # data/history.json
    errors: dict = field(default_factory=dict)            # source -> why it could not be read


@dataclass
class Report:
    findings: list
    figures: list

    def by_state(self, state: str) -> list:
        return [f for f in self.findings if f.state == state]

    @property
    def exit_code(self) -> int:
        if self.by_state(FAILED):
            return 1
        if self.findings and all(f.state == UNVERIFIED for f in self.findings):
            return 2
        return 0

    @property
    def verdict(self) -> str:
        if self.by_state(FAILED):
            return f"FAILED: {len(self.by_state(FAILED))} real incoherence(s)"
        if self.by_state(UNVERIFIED):
            return f"INCOMPLETE: no incoherence found, but {len(self.by_state(UNVERIFIED))} item(s) could not be verified"
        if self.by_state(PENDING):
            return f"CONSISTENT with {len(self.by_state(PENDING))} pending item(s)"
        return "CONSISTENT"

    def counts(self) -> dict:
        return {state: len(self.by_state(state)) for state in STATES}


# --------------------------------------------------------------------------- parsing helpers

def catalogue_rows(text: str) -> dict:
    """{section: {repo: version}} of the catalogue tables of one README (the first cell links the repository, the second is its version)."""
    starts = [m.start() for m in progress.H1.finditer(text)]
    sections = [text[a:b] for a, b in zip(starts[1:], starts[2:] + [len(text)])]
    result: dict = {}
    for eco, section in zip(progress.ECOSYSTEMS, sections):
        rows: dict = {}
        for line in section.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            match = progress.REPO_LINK.match(cells[0]) if cells else None
            if match and match.group(2) not in rows:
                rows[match.group(2)] = cells[1] if len(cells) > 1 else ""
        result[eco] = rows
    return result


def progress_counts(file: str, text: str) -> dict:
    """{section: n} from the sentence of the progress block ("each of its N repositories"), in the language of the file; None when it is not found."""
    pre, _, post = progress.TEXT[file].partition("{n}")
    pattern = re.compile(re.escape(pre[-40:]) + r"(\d+)" + re.escape(post[:30]))
    result: dict = {}
    for eco in progress.ECOSYSTEMS:
        block = re.search(rf"<!-- progress:{re.escape(eco)} -->(.*?)<!-- /progress:{re.escape(eco)} -->", text, re.S)
        match = pattern.search(block.group(1)) if block else None
        result[eco] = int(match.group(1)) if match else None
    return result


def page_sources(html: str) -> "tuple[dict | None, tuple, tuple | None]":
    """(embedded data, the issues the page lists, (listed, public) the page states) of a generated dashboard."""
    match = _DATA_RE.search(html or "")
    data = None
    if match:
        try:
            parsed = json.loads(match.group(1))
            data = parsed if isinstance(parsed, dict) else None
        except ValueError:
            data = None
    issues = tuple((r, k, d) for r, k, d in _ISSUE_RE.findall(html or ""))
    cover = _COVER_RE.search(html or "")
    return data, issues, ((int(cover.group(1)), int(cover.group(2))) if cover else None)


def _plain(text: str) -> str:
    """The name of an ecosystem without case, spaces, dots or hyphens (A.R.M.O.R. = ARMOR, Electro Hobby 3D = ELECTRO-HOBBY-3D)."""
    return re.sub(r"[^a-z0-9]", "", text.casefold())


def version_key(text: str) -> "tuple | None":
    match = TAG_RE.match(str(text or "").strip())
    return tuple(int(p) for p in match.group(1).split(".")) if match else None


def _padded(a: tuple, b: tuple) -> "tuple[tuple, tuple]":
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)), b + (0,) * (width - len(b))


# --------------------------------------------------------------------------- the checks

def reconcile(src: Sources) -> Report:
    findings: list = []
    figures: list = []

    def add(check: str, state: str, subject: str, detail: str) -> None:
        findings.append(Finding(check, state, subject, detail))

    # ---- 1. The repositories of the owner and their manifests
    names = {r.name: r for r in (src.repos or [])}
    if src.repos is None:
        add("inventory", UNVERIFIED, src.owner, f"the public repositories could not be listed: {src.errors.get('listing', 'unknown reason')}")
    else:
        add("inventory", OK, src.owner, f"{len(names)} public repositories listed")

    reads = src.manifests
    ecosystem_repos: dict = {}      # repo -> manifest key, only for manifests read as a JSON object
    manifest_repos: set = set()     # repos that carry a manifest file (readable or not)
    unreadable: list = []
    for name in sorted(names, key=str.casefold):
        read = reads.get(name)
        if read is None:
            add("manifest-read", UNVERIFIED, name, "the manifest was not looked for")
            unreadable.append(name)
        elif read.status == "error":
            add("manifest-read", UNVERIFIED, name, f"the manifest could not be read: {read.detail}")
            unreadable.append(name)
        elif read.status == "absent":
            if names[name].empty:
                add("manifest-read", PENDING, name, "the repository is empty: no manifest yet")
            elif name.casefold() == src.owner.casefold():
                add("manifest-read", OK, name, "the profile repository carries no manifest: it is not a project of an ecosystem")
            else:
                add("manifest-read", PENDING, name, "public repository without the manifest of any ecosystem: not part of the family yet")
        elif read.status == "invalid":
            manifest_repos.add(name)
            add("manifest-read", FAILED, name, read.detail or "the manifest is not a JSON object")
        else:
            manifest_repos.add(name)
            ecosystem_repos[name] = read.ecosystem
            if read.also:
                add("manifest-read", FAILED, name, f"the repository carries the manifest of {read.ecosystem} and also of {', '.join(read.also)}: its ecosystem is ambiguous")
    stray = sorted((set(reads) - set(names)) if src.repos is not None else (), key=str.casefold)
    for name in stray:
        add("manifest-read", FAILED, name, "a manifest was read for a repository that is not among the public repositories")

    # ---- 2. The fields every manifest must carry (the same rules in the four ecosystems)
    cat_labels = {}
    if src.catalog_json:
        try:
            cat_labels = {k: label for k, label, _file in catalog_check.catalog_ecosystems(json.dumps(src.catalog_json))}
        except ValueError:
            cat_labels = {}
    dashboard_version = {n: r.get("version") for n, r in ((src.dashboard or {}).get("repos") or {}).items()}
    dashboard_release = {n: r.get("release") for n, r in ((src.dashboard or {}).get("repos") or {}).items()}
    for name, eco in sorted(ecosystem_repos.items(), key=lambda kv: kv[0].casefold()):
        data = reads[name].data or {}
        problems: list = []
        if data.get("name") != name:
            problems.append(f"name {data.get('name')!r} is not the repository name")
        expected = cat_labels.get(eco) or LABEL_OF.get(eco)
        declared = data.get("ecosystem")
        if not isinstance(declared, str) or not declared.strip():
            problems.append("ecosystem is missing")
        elif expected and _plain(declared) != _plain(expected):
            problems.append(f"ecosystem {declared!r} does not match the manifest file ({expected})")
        for key in ("family", "role"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                problems.append(f"{key} is missing or empty")
        if data.get("maturity") not in di.MATURITIES:
            problems.append(f"maturity {data.get('maturity')!r} is not one of {'|'.join(di.MATURITIES)}")
        if data.get("evidence") not in di.EVIDENCES:
            problems.append(f"evidence {data.get('evidence')!r} is not one of {'|'.join(di.EVIDENCES)}")
        if not isinstance(data.get("version"), str) or not VERSION_RE.match(data["version"]):
            problems.append(f"version {data.get('version')!r} is not a dotted number")
        parent = data.get("parent")
        if parent not in (None, "") and src.repos is not None and parent not in names:
            problems.append(f"parent {parent!r} is not a public repository")
        if parent == name:
            problems.append("the repository is its own parent")
        add("manifest-fields", FAILED if problems else OK, name, "; ".join(problems) if problems else "name, ecosystem, family, role, maturity, evidence, version and parent are coherent")

        # dependencies must exist (an empty repository is a plan, not an error)
        deps = data.get("depends_on")
        if deps is not None:
            if not isinstance(deps, list) or not all(isinstance(d, str) for d in deps):
                add("depends-on", FAILED, name, "depends_on must be a list of repository names")
            elif src.repos is not None:
                missing = [d for d in deps if d not in names]
                empty = [d for d in deps if d in names and names[d].empty]
                if name in deps:
                    add("depends-on", FAILED, name, "the repository depends on itself")
                elif missing:
                    add("depends-on", FAILED, name, f"depends_on names repositories that do not exist: {', '.join(missing)}")
                elif empty:
                    add("depends-on", PENDING, name, f"depends on repositories that are still empty: {', '.join(empty)}")
                else:
                    add("depends-on", OK, name, f"{len(deps)} dependencies, all existing")

    # ---- 3. Versions: manifest, version file read by the dashboard, README table and last release
    readme_main = src.readmes.get("README.md")
    readme_versions: dict = {}
    if readme_main:
        for rows in catalogue_rows(readme_main).values():
            readme_versions.update(rows)
    for name, eco in sorted(ecosystem_repos.items(), key=lambda kv: kv[0].casefold()):
        manifest_version = (reads[name].data or {}).get("version")
        notes: list = []
        state = OK
        if not isinstance(manifest_version, str) or not VERSION_RE.match(manifest_version or ""):
            continue    # already reported by manifest-fields
        wanted = version_key(manifest_version)
        file_version = dashboard_version.get(name)
        if src.dashboard is None:
            state, notes = UNVERIFIED, ["the dashboard data could not be read"]
        elif name not in dashboard_version:
            pass        # the dashboard check names it
        elif file_version is None:
            state, notes = UNVERIFIED, ["the dashboard could not read the version file of the repository"]
        else:
            got = version_key(file_version)
            if got is not None and wanted is not None and _padded(got, wanted)[0] != _padded(got, wanted)[1]:
                state, notes = FAILED, [f"manifest says {manifest_version}, the version file says {file_version}"]
        shown = readme_versions.get(name)
        if readme_main is None:
            if state == OK:
                state, notes = UNVERIFIED, ["the profile README could not be read"]
        elif shown is None:
            pass        # the catalogue check names it
        else:
            got = version_key(shown)
            if got is not None and wanted is not None and _padded(got, wanted)[0] != _padded(got, wanted)[1]:
                state = FAILED
                notes.append(f"the README table says {shown}, the manifest {manifest_version}")
        release = dashboard_release.get(name)
        if src.dashboard is not None and name in dashboard_version and release and release.get("tag") and wanted is not None:
            tag = version_key(release["tag"])
            if tag is not None:
                a, b = _padded(tag, wanted)
                if a > b:
                    state = FAILED
                    notes.append(f"the last release ({release['tag']}) is newer than the version ({manifest_version})")
                elif a < b and state != FAILED:
                    state = PENDING
                    notes.append(f"version {manifest_version} is not released yet (last release {release['tag']})")
        add("version", state, name, "; ".join(notes) if notes else f"{manifest_version} agrees in the manifest, the version file, the README and the last release")

    # ---- 4. The README catalogue and its seven translations
    sections: dict = {}
    if not src.readmes:
        add("readme", UNVERIFIED, "README", "no README could be read")
    else:
        missing_files = [f for f in progress.README_FILES if f not in src.readmes]
        for f in missing_files:
            add("readme-parity", UNVERIFIED, f, "the file could not be read")
        for file, text in src.readmes.items():
            sections[file] = catalogue_rows(text)
        base = sections.get("README.md")
        if base is not None:
            for file, rows in sorted(sections.items()):
                if file == "README.md":
                    continue
                diff = [f"{eco}: {sorted(set(base[eco]) ^ set(rows.get(eco, {})))}" for eco in progress.ECOSYSTEMS if set(base[eco]) != set(rows.get(eco, {}))]
                add("readme-parity", FAILED if diff else OK, file, ("the catalogue differs from README.md in " + "; ".join(diff)) if diff else "lists the same repositories as README.md in the four ecosystems")
            for file in sorted(src.readmes):
                counts = progress_counts(file, src.readmes[file]) if file in progress.TEXT else {}
                wrong = [f"{eco}: {counts.get(eco)} instead of {len(base[eco])}" for eco in progress.ECOSYSTEMS if counts.get(eco) != len(base[eco])]
                add("progress-count", FAILED if wrong else OK, file, ("the number of repositories of the progress sentence differs from the catalogue: " + "; ".join(wrong)) if wrong else "the progress sentences count the repositories of the catalogue")
            if src.repos is not None:
                for eco in progress.ECOSYSTEMS:
                    listed = set(base[eco])
                    carried = {n for n, e in ecosystem_repos.items() if SECTION_OF.get(e) == eco}
                    carried |= {n for n in manifest_repos if n not in ecosystem_repos and reads[n].ecosystem and SECTION_OF.get(reads[n].ecosystem) == eco}
                    for n in sorted(listed - carried, key=str.casefold):
                        if n in unreadable:
                            continue
                        if n not in names:
                            add("readme-catalogue", FAILED, n, f"listed in the {LABEL_OF[eco]} catalogue but it is not a public repository")
                        elif names[n].empty:
                            add("readme-catalogue", PENDING, n, f"listed in the {LABEL_OF[eco]} catalogue; the repository is still empty")
                        else:
                            add("readme-catalogue", FAILED, n, f"listed in the {LABEL_OF[eco]} catalogue but carries no manifest of that ecosystem")
                    for n in sorted(carried - listed, key=str.casefold):
                        add("readme-catalogue", FAILED, n, f"carries a {LABEL_OF[eco]} manifest but the README catalogue does not list it")
                    ok_count = len(listed & carried)
                    if ok_count:
                        add("readme-catalogue", OK, LABEL_OF[eco], f"{ok_count} repositories agree between the manifests and the catalogue")

    # ---- 5. ecosystem-catalog.json
    if src.catalog_json is None:
        add("catalog-json", UNVERIFIED, "ecosystem-catalog.json", f"it could not be read: {src.errors.get('catalog', 'unknown reason')}")
    else:
        try:
            entries = catalog_check.catalog_ecosystems(json.dumps(src.catalog_json))
        except ValueError as exc:
            add("catalog-json", FAILED, "ecosystem-catalog.json", str(exc))
            entries = None
        if entries is not None:
            known = {k: (label, f) for k, label, f in entries}
            expected_files = di.MANIFEST_FILES
            diff = [f"'{k}' has {known[k][1]} but the dashboard reads {expected_files[k]}" for k in expected_files if k in known and known[k][1] != expected_files[k]]
            diff += [f"'{k}' is read by the dashboard but not in the catalogue" for k in expected_files if k not in known]
            diff += [f"'{k}' is in the catalogue but the dashboard does not read it" for k in known if k not in expected_files]
            diff += [f"{n} carries the manifest of '{e}', which the catalogue does not list" for n, e in sorted(ecosystem_repos.items()) if e not in known]
            add("catalog-json", FAILED if diff else OK, "ecosystem-catalog.json", "; ".join(diff) if diff else f"lists the {len(known)} ecosystems the manifests and the dashboard use")

    # ---- 6. The dashboard
    listed_dash: set = set()
    page_issues = {r: (k, d) for r, k, d in src.dashboard_issues}
    if src.dashboard is None:
        add("dashboard", UNVERIFIED, "docs/index.html", f"the dashboard data could not be read: {src.errors.get('dashboard', 'unknown reason')}")
    else:
        listed_dash = set((src.dashboard.get("repos") or {}))
        if src.repos is not None:
            for n in sorted(ecosystem_repos, key=str.casefold):
                if n in listed_dash:
                    if (src.dashboard["repos"][n].get("eco") or "") != ecosystem_repos[n]:
                        add("dashboard", FAILED, n, f"the dashboard places it in '{src.dashboard['repos'][n].get('eco')}' but its manifest is '{ecosystem_repos[n]}'")
                    continue
                reason = page_issues.get(n)
                add("dashboard", FAILED, n, "has a readable manifest but the dashboard does not list it" + (f" (the page reports: {reason[1]})" if reason else " (and the page does not report why)"))
            for n in sorted(manifest_repos - set(ecosystem_repos), key=str.casefold):
                if n not in listed_dash:
                    reason = page_issues.get(n)
                    add("dashboard", FAILED, n, "its manifest is unusable and the dashboard does not list it" + (f" (the page reports: {reason[1]})" if reason else ""))
            for n in sorted(listed_dash - set(names), key=str.casefold):
                add("dashboard", FAILED, n, "listed by the dashboard but it is not a public repository any more")
            for n in sorted((set(names) - manifest_repos - set(unreadable) - listed_dash) & listed_dash):
                add("dashboard", FAILED, n, "listed by the dashboard but the repository has no manifest")
            agreeing = len(listed_dash & set(ecosystem_repos))
            if agreeing:
                add("dashboard", OK, "docs/index.html", f"{agreeing} repositories listed by the dashboard agree with the manifests")
            if src.dashboard_cover and src.dashboard_cover[0] != len(listed_dash):
                add("dashboard", FAILED, "docs/index.html", f"the page says {src.dashboard_cover[0]} repositories are listed but its data holds {len(listed_dash)}")

    # ---- 7. The progress history
    if src.history is None:
        add("history", UNVERIFIED, "data/history.json", f"it could not be read: {src.errors.get('history', 'unknown reason')}")
    else:
        entries_h = src.history.get("entries") or []
        last = entries_h[-1] if entries_h else None
        if not last:
            add("history", PENDING, "data/history.json", "no daily snapshot yet")
        elif src.dashboard is not None:
            snap_repos = set(last.get("repos") or {})
            extra, lost = sorted(snap_repos - listed_dash, key=str.casefold), sorted(listed_dash - snap_repos, key=str.casefold)
            if extra or lost:
                add("history", PENDING, f"data/history.json ({last.get('date')})", f"the last snapshot differs from the dashboard (only in the snapshot: {extra or '-'}; only in the dashboard: {lost or '-'}); the next build writes a new one")
            else:
                add("history", OK, f"data/history.json ({last.get('date')})", f"the last daily snapshot holds the same {len(snap_repos)} repositories as the dashboard")

    figures = explain(src, names, ecosystem_repos, manifest_repos, unreadable, listed_dash, sections.get("README.md"), page_issues)
    order = {state: index for index, state in enumerate(STATES)}
    findings.sort(key=lambda f: (order[f.state], f.check, f.subject.casefold()))
    return Report(findings, figures)


# --------------------------------------------------------------------------- the figures

def explain(src: Sources, names: dict, ecosystem_repos: dict, manifest_repos: set, unreadable: list, listed_dash: set, readme_rows: "dict | None", page_issues: "dict | None" = None) -> list:
    out: list = []
    if src.repos is None:
        out.append(Figure("Public repositories", "not verified", "the listing of the repositories of the owner could not be read, so no figure that depends on it can be explained"))
        return out
    total = len(names)
    out.append(Figure("Public repositories", str(total), f"every public, non-fork repository of {src.owner} (archived ones included)"))
    projects = len(manifest_repos)
    without = sorted((n for n in names if n not in manifest_repos and n not in unreadable), key=str.casefold)
    why_without = ", ".join(f"{n} ({'empty' if names[n].empty else 'profile repository' if n.casefold() == src.owner.casefold() else 'no manifest'})" for n in without) or "none"
    suffix = f"; {len(unreadable)} could not be checked" if unreadable else ""
    out.append(Figure("Projects", f"{projects}" + (" or more" if unreadable else ""),
                      f"public repositories that carry the manifest of an ecosystem. The other {total - projects}: {why_without}{suffix}"))
    valid = [n for n in ecosystem_repos if (src.manifests[n].data or {}).get("maturity") in di.MATURITIES and (src.manifests[n].data or {}).get("evidence") in di.EVIDENCES and (src.manifests[n].data or {}).get("name") == n]
    bad = sorted(set(manifest_repos) - set(valid), key=str.casefold)
    out.append(Figure("Valid manifests", f"{len(valid)} of {projects}",
                      "the manifest is a JSON object, names its own repository and declares a known maturity and evidence" + (f"; not valid: {', '.join(bad)}" if bad else "")))
    if src.dashboard is not None:
        not_listed = sorted(set(valid) - listed_dash, key=str.casefold)
        reasons = page_issues or {}
        detail = ", ".join(f"{n} ({reasons[n][1]})" if n in reasons else n for n in not_listed)
        out.append(Figure("Listed by the dashboard", f"{len(listed_dash)} of {projects}" if projects else f"{len(listed_dash)}",
                          "repositories whose manifest the updaters pinned in the workflows accept (the 'registry health' card of the page)"
                          + (f"; valid by the rules above but not listed: {detail}" if not_listed else "")))
    else:
        out.append(Figure("Listed by the dashboard", "not verified", "the dashboard data could not be read"))
    for key in ("hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"):
        members = sorted(n for n, e in ecosystem_repos.items() if e == key)
        if not members and key == "electro-hobby-3d":
            continue
        in_dash = len([n for n in members if n in listed_dash])
        bits = [f"{len(members)} manifests"]
        if src.dashboard is not None:
            bits.append(f"{in_dash} on the dashboard")
        if readme_rows is not None and key in readme_rows:
            bits.append(f"{len(readme_rows[key])} in the README catalogue")
        out.append(Figure(LABEL_OF[key], str(len(members)), ", ".join(bits) + (" (the updater of the suite is counted in the EH3D section of the README)" if key == "electro-hobby-3d" else "")))
    return out


# --------------------------------------------------------------------------- the report

GLYPH = {OK: "OK        ", FAILED: "FAILED    ", PENDING: "PENDING   ", UNVERIFIED: "UNVERIFIED"}


def render_text(report: Report, quiet_ok: bool = True) -> str:
    lines = [f"ECOSYSTEM INTEGRITY: {report.verdict}", "", "Figures and where they come from:"]
    for fig in report.figures:
        lines.append(f"  - {fig.label}: {fig.value}. {fig.why}")
    counts = report.counts()
    lines += ["", "Findings: " + ", ".join(f"{counts[s]} {s}" for s in STATES)]
    for finding in report.findings:
        if quiet_ok and finding.state == OK:
            continue
        lines.append(f"  [{GLYPH[finding.state]}] {finding.check}: {finding.subject}: {finding.detail}")
    if quiet_ok and counts[OK]:
        lines.append(f"  ({counts[OK]} checks passed and are not listed)")
    return "\n".join(lines)


def render_markdown(report: Report) -> str:
    counts = report.counts()
    out = [f"## Ecosystem integrity: {report.verdict}", "", "| State | Count |", "| --- | ---: |"]
    out += [f"| {s} | {counts[s]} |" for s in STATES]
    out += ["", "### Figures and where they come from", "", "| Figure | Value | Why |", "| --- | --- | --- |"]
    out += [f"| {f.label} | {f.value} | {f.why.replace('|', '/')} |" for f in report.figures]
    shown = [f for f in report.findings if f.state != OK]
    if shown:
        out += ["", "### Findings that need attention", "", "| State | Check | Subject | Detail |", "| --- | --- | --- | --- |"]
        out += [f"| {f.state} | {f.check} | `{f.subject}` | {f.detail.replace('|', '/')} |" for f in shown]
    return "\n".join(out)


def to_json(report: Report) -> dict:
    return {"verdict": report.verdict, "exit_code": report.exit_code, "counts": report.counts(),
            "figures": [vars(f) for f in report.figures], "findings": [vars(f) for f in report.findings]}


# --------------------------------------------------------------------------- the network

def collect(owner: str, token: str, listing, fetch, workers: int = 8, root: Path = ROOT) -> Sources:
    """Read every source. `listing()` returns ([RepoInfo], error); `fetch(repo, branch, file)` is the one of dashboard_integrity.raw_fetcher."""
    errors: dict = {}
    repos, error = listing()
    if error:
        errors["listing"] = error
    src = Sources(owner=owner, repos=None if error else repos, errors=errors)

    def read_one(repo: RepoInfo) -> "tuple[str, ManifestRead]":
        found: list = []
        failures: list = []
        for eco, file in di.MANIFEST_FILES.items():
            status, payload = fetch(repo.name, repo.branch, file)
            if status == "ok":
                found.append((eco, payload))
            elif status == "error":
                failures.append(f"{file}: {payload}")
        if found:
            eco, payload = found[0]
            also = tuple(e for e, _ in found[1:])
            if isinstance(payload, dict):
                return repo.name, ManifestRead("ok", eco, payload, also=also)
            return repo.name, ManifestRead("invalid", eco, None, "the manifest is not a JSON object", also)
        if failures:
            return repo.name, ManifestRead("error", detail="; ".join(failures))
        return repo.name, ManifestRead("absent")

    if src.repos is not None:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            src.manifests = dict(pool.map(read_one, [r for r in src.repos if not r.empty]))
        for r in src.repos:
            src.manifests.setdefault(r.name, ManifestRead("absent"))

    for file in progress.README_FILES:
        try:
            src.readmes[file] = (root / file).read_text(encoding="utf-8")
        except OSError as exc:
            errors[file] = str(exc)
    try:
        src.catalog_json = json.loads((root / "ecosystem-catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors["catalog"] = str(exc)
    try:
        html = (root / "docs" / "index.html").read_text(encoding="utf-8")
        src.dashboard, src.dashboard_issues, src.dashboard_cover = page_sources(html)
        if src.dashboard is None:
            errors["dashboard"] = "the page carries no readable data block"
    except OSError as exc:
        errors["dashboard"] = str(exc)
    try:
        src.history = json.loads((root / "data" / "history.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors["history"] = str(exc)
    return src


def github_repo_listing(owner: str, token: str, timeout: float = 20):
    """A `listing` for `collect`: public non-fork repositories with their default branch, size (0 = empty) and archived flag; the first failure is reported."""
    def run() -> "tuple[list[RepoInfo], str]":
        found: list = []
        page = 1
        while True:
            headers = {"User-Agent": "JuanenRac-integrity-test", "Accept": "application/vnd.github+json"}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            request = urllib.request.Request(f"https://api.github.com/users/{owner}/repos?type=owner&per_page=100&page={page}", headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    payload = json.load(response)
            except urllib.error.HTTPError as exc:
                return [], f"HTTP {exc.code} listing page {page}"
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                return [], f"listing page {page} failed: {exc}"
            if not isinstance(payload, list):
                return [], f"unexpected answer listing page {page}"
            for item in payload:
                if isinstance(item, dict) and isinstance(item.get("name"), str) and item.get("fork") is not True:
                    found.append(RepoInfo(item["name"], item.get("default_branch") or "main", item.get("size") == 0, bool(item.get("archived"))))
            if len(payload) < 100:
                return found, ""
            page += 1
    return run


def main(argv: "list[str] | None" = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--owner", default="JuanenRac")
    parser.add_argument("--json", help="also write the machine-readable report here")
    parser.add_argument("--fail-on-unverified", action="store_true", help="exit 2 when anything could not be verified")
    parser.add_argument("--all", action="store_true", help="list the checks that passed too")
    args = parser.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    src = collect(args.owner, token, github_repo_listing(args.owner, token), di.raw_fetcher(args.owner))
    report = reconcile(src)
    print(render_text(report, quiet_ok=not args.all))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write(render_markdown(report) + "\n")
    if args.json:
        Path(args.json).write_text(json.dumps(to_json(report), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.fail_on_unverified and report.by_state(UNVERIFIED) and report.exit_code == 0:
        return 2
    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
