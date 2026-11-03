#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_tests.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""How many automated tests each repository declares, per repository and per ecosystem, for the "Tests" tab of the status dashboard.

The count is DECLARED by each repository (the `tests.count` of the glance file of its ecosystem, or the `Tests` row of the quick-facts table of its README); the
dashboard never runs the tests. What counts as verified by a CI run is the business of dashboard_ci_evidence.py.

Which source each ecosystem uses is in `dashboard-config.json` (key `tests`). Nothing is invented:

  * a source that answered and has the count      -> "declared" (with where it was read),
  * a source that answered and has no count       -> "undeclared" (not a zero),
  * a lookup that failed                          -> "unread"; the last count of the daily history is shown instead as "lastknown", with its date, when there is one,
  * a count that is not a number of tests (the nodes count "checks" of their host programs) -> unit "checks": listed apart, never added to the tests.

Stdlib only.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

CONFIG_PATH = Path(__file__).resolve().parent.parent / "dashboard-config.json"
ECOSYSTEMS: tuple[str, ...] = ("hydra-umc", "urtc", "armor", "eh3d")
DEFAULT_CONFIG: dict = {
    "sources": {
        "hydra-umc": {"glance": "HYDRA-UMC-DOCS/data/glance.json", "readme": True},
        "urtc": {"glance": "URTC-DOCS/data/glance.json", "readme": True},
        "armor": {"readme": True},
        "eh3d": {"readme": True},
        "electro-hobby-3d": {"readme": True},
    },
}
MAX_COUNT = 10_000_000

# fetch(path in the owner's namespace "repo/file", kind) -> ("ok", text) | ("absent", None) | ("error", reason)
Fetch = Callable[[str], "tuple[str, object]"]


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def check_config(raw: object) -> tuple[dict, list[str]]:
    """(config, problems). An unusable part is replaced by the default and reported."""
    config = {"sources": {key: dict(value) for key, value in DEFAULT_CONFIG["sources"].items()}}
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["tests: not an object"]
    sources = raw.get("sources")
    if sources is None:
        return config, problems
    if not isinstance(sources, Mapping):
        return config, ["tests.sources: not an object"]
    for eco, source in sources.items():
        if not isinstance(source, Mapping):
            problems.append(f"tests.sources.{eco}: not an object")
            continue
        glance = source.get("glance")
        readme = source.get("readme", False)
        if glance is not None and not (isinstance(glance, str) and re.fullmatch(r"[A-Za-z0-9._-]+/[A-Za-z0-9._/-]+", glance) and ".." not in glance):
            problems.append(f"tests.sources.{eco}.glance: not a path 'repository/file'")
            continue
        if not isinstance(readme, bool):
            problems.append(f"tests.sources.{eco}.readme: not true or false")
            continue
        if glance is None and not readme:
            problems.append(f"tests.sources.{eco}: no source")
            continue
        config["sources"][str(eco)] = {**({"glance": glance} if glance else {}), "readme": readme}
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return check_config(None)
    except (OSError, ValueError) as exc:
        config, _ = check_config(None)
        return config, [f"{path.name} could not be read for the tests ({exc})"]
    return check_config(raw.get("tests") if isinstance(raw, Mapping) else None)


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

_ROW = re.compile(r"^\|\s*Tests\s*\|\s*(.+?)\s*\|\s*$", re.M)
_NUMBER = re.compile(r"^\s*(\d[\d,]*)")


def _int(text: str) -> int | None:
    try:
        value = int(text.replace(",", ""))
    except ValueError:
        return None
    return value if 0 <= value <= MAX_COUNT else None


def parse_readme(text: str) -> dict | None:
    """The `Tests` row of the quick-facts table of a README -> {"n", "unit"} or None when the README declares no count.
    "134 (`python -m unittest`)" is 134 tests; "11979 checks in 20 host programs" is 11979 checks; "7 host test programs (173749 checks counted)" is 173749 checks;
    "unit tests on the JVM" declares no number."""
    row = _ROW.search(text or "")
    if not row:
        return None
    value = row.group(1)
    found = _NUMBER.match(value)
    if not found:
        return None
    number = _int(found.group(1))
    rest = value[found.end():].strip().lower()
    if number is None:
        return None
    if rest.startswith("checks"):
        return {"n": number, "unit": "checks"}
    if rest.startswith("host"):
        inner = re.search(r"([\d,]+)\s+checks", rest)
        counted = _int(inner.group(1)) if inner else None
        return {"n": counted, "unit": "checks"} if counted is not None else None
    return {"n": number, "unit": "tests"}


def parse_glance(payload: object) -> dict[str, dict | None]:
    """{repository: {"n", "unit"} or None} of a glance file (`repos.<name>.tests.count`). A repository whose entry has no count is None, not zero."""
    repos = payload.get("repos") if isinstance(payload, Mapping) else None
    out: dict[str, dict | None] = {}
    if not isinstance(repos, Mapping):
        return out
    for name, item in repos.items():
        count = ((item or {}).get("tests") or {}).get("count") if isinstance(item, Mapping) and isinstance(item.get("tests"), Mapping) else None
        out[str(name)] = {"n": count, "unit": "tests"} if isinstance(count, int) and not isinstance(count, bool) and 0 <= count <= MAX_COUNT else None
    return out


def read_all(ecosystem_by_name: Mapping[str, str], fetch: Fetch, config: Mapping, workers: int = 8) -> dict:
    """{"records": {repo: {"n", "unit", "src"}}, "undeclared": [repo], "errors": {repo: reason}, "glance": {eco: "ok"|reason}}.
    Per repository: the glance file of its ecosystem first, the README when the glance file has no count or could not be read. A repository found nowhere is
    "undeclared" only when a source answered; when every lookup failed it is in "errors"."""
    sources = config["sources"]
    glance_state: dict[str, str] = {}
    glance_data: dict[str, dict] = {}
    for eco in sorted({eco for eco in ecosystem_by_name.values()}):
        path = (sources.get(eco) or {}).get("glance")
        if not path:
            continue
        status, payload = fetch(path)
        if status == "ok":
            try:
                glance_data[eco] = parse_glance(json.loads(payload) if isinstance(payload, str) else payload)
                glance_state[eco] = "ok"
            except ValueError as exc:
                glance_state[eco] = f"not valid JSON: {exc}"
        else:
            glance_state[eco] = "not found" if status == "absent" else str(payload)
    result: dict = {"records": {}, "undeclared": [], "errors": {}, "glance": glance_state}

    def one(name: str):
        eco = ecosystem_by_name[name]
        source = sources.get(eco) or {}
        glance = glance_data.get(eco)
        if glance is not None and glance.get(name):
            return name, {**glance[name], "src": "glance"}, "", False
        has_glance = bool(source.get("glance"))
        # The glance file is the first source: when it could not be read, a README without the row does not prove that the repository declares nothing.
        answered = glance is not None and name in glance
        reason = ""
        if source.get("readme"):
            status, text = fetch(f"{name}/README.md")
            if status == "ok":
                parsed = parse_readme(text if isinstance(text, str) else "")
                if parsed and parsed["n"] is not None:
                    return name, {**parsed, "src": "readme"}, "", False
                answered = answered or not has_glance
            elif status == "absent":
                answered = answered or not has_glance
            else:
                reason = str(text)
        if answered:
            return name, None, "", True
        return name, None, reason or glance_state.get(eco, "no source") or "no source", False

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for name, record, error, undeclared in pool.map(one, sorted(ecosystem_by_name)):
            if record:
                result["records"][name] = record
            elif undeclared:
                result["undeclared"].append(name)
            else:
                result["errors"][name] = error
    return result


def raw_fetch(owner: str, timeout: float = 15) -> Fetch:
    """A `fetch` for `read_all`: one file of the default branch of a repository of `owner` from raw.githubusercontent.com (no API quota)."""
    def run(path: str):
        repo, _, rest = path.partition("/")
        request = urllib.request.Request(f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{rest}", headers={"User-Agent": "JuanenRac-dashboard-tests"})
        outcome: tuple[str, object] = ("error", "no attempt")
        for _attempt in range(2):                      # one more try: a single slow answer must not make a repository "not verified"
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    return "ok", response.read(3_000_000).decode("utf-8", errors="replace")
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    return "absent", None
                outcome = ("error", f"HTTP {exc.code}")
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                outcome = ("error", f"lookup failed: {exc}")
        return outcome
    return run


def fresh_counts(read: Mapping | None) -> dict[str, int]:
    """{repository: tests} that were read in THIS run, for the daily snapshot: only counts of tests, never a last known value, never checks."""
    out: dict[str, int] = {}
    for name, record in ((read or {}).get("records") or {}).items():
        if isinstance(record, Mapping) and record.get("unit") == "tests" and isinstance(record.get("n"), int) and not isinstance(record.get("n"), bool):
            out[name] = record["n"]
    return out


# ---------------------------------------------------------------------------
# What the page embeds
# ---------------------------------------------------------------------------

def _last_known(history: Sequence[Mapping], name: str, before: str | None) -> tuple[int, str] | None:
    for entry in sorted(history, key=lambda e: str(e.get("date")), reverse=True):
        counts = entry.get("tests")
        if isinstance(counts, Mapping) and isinstance(counts.get(name), int) and (before is None or str(entry.get("date")) < before):
            return counts[name], str(entry["date"])
    return None


def series(history: Sequence[Mapping], ecosystem_by_name: Mapping[str, str], ecosystems: Iterable[str] = ECOSYSTEMS,
           carried: Mapping[str, int] | None = None, today: str | None = None) -> list[dict]:
    """The evolution: one point per day that has counts, {"date", "eco": {eco: {"n": total of the tests declared that day, "k": repositories that declared}}}.
    Snapshots from before the counts were recorded have no "tests" and give no point (no zero is invented). `carried` are the last known counts of the repositories
    that could not be read today: they complete the point of `today`, as they complete the bars, so the end of the line and the bar say the same."""
    points: list[dict] = []
    for entry in sorted(history, key=lambda e: str(e.get("date"))):
        counts = entry.get("tests")
        if not isinstance(counts, Mapping) or not counts:
            continue
        if carried and str(entry.get("date")) == today:
            counts = {**carried, **counts}
        per: dict[str, dict] = {}
        for eco in ecosystems:
            mine = [value for name, value in counts.items() if ecosystem_by_name.get(name) == eco and isinstance(value, int)]
            if mine:
                per[eco] = {"n": sum(mine), "k": len(mine)}
        if per:
            points.append({"date": str(entry["date"]), "eco": per})
    return points


def build(read: Mapping | None, ecosystem_by_name: Mapping[str, str], history: Sequence[Mapping], today: str, config: Mapping | None = None) -> dict:
    """The "tests" block of the page data. `read` is None when this build did not look (the fixture, a failed run): every repository then shows its last known count
    or "not verified"."""
    config = config or check_config(None)[0]
    records = (read or {}).get("records") or {}
    undeclared = set((read or {}).get("undeclared") or [])
    errors = (read or {}).get("errors") or {}
    older = [entry for entry in history if str(entry.get("date")) < today]
    repos: dict[str, dict] = {}
    carried: dict[str, int] = {}
    stale_dates: list[str] = []
    for name in sorted(ecosystem_by_name):
        record = records.get(name)
        if record:
            repos[name] = {"n": record["n"], "unit": record["unit"], "state": "declared", "src": record["src"], "asof": None}
        elif name in undeclared:
            repos[name] = {"n": None, "unit": None, "state": "undeclared", "src": None, "asof": None}
        else:
            known = _last_known(older, name, None)
            if known:
                repos[name] = {"n": known[0], "unit": "tests", "state": "lastknown", "src": None, "asof": known[1]}
                stale_dates.append(known[1])
                carried[name] = known[0]
            else:
                repos[name] = {"n": None, "unit": None, "state": "unread", "src": None, "asof": None}
    return {
        "read": bool(records or undeclared),
        "sources": {eco: dict(value) for eco, value in config["sources"].items()},
        "repos": repos,
        "series": series(history, ecosystem_by_name, carried=carried, today=today),
        "staleDate": max(stale_dates) if stale_dates else None,
        "problems": len(errors),
    }
