#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/changelog_stats.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Statistics of a CHANGELOG.md: versions, entries, and the kind of each entry. Standard library only.

The file layout read here is the one the repositories use:

    ## [Unreleased]
    - **Title:** text of the entry...
    ## [1.2.3] - Title of the version
    ### Fixed                       (optional Keep a Changelog sub-heading)
    - **Title:** text of the entry...

A level-2 heading with a bracketed name starts a section; `Unreleased` is the work not yet published, any other name is a published version. An entry is a
top-level list item ("- " or "* " at the start of the line, with its continuation lines). Dates are not read: the changelogs hold none, and the pace of
publishing comes from the releases and tags of GitHub (see code_stats.py).

Each entry is classified by words. The rules are in the `changelog` block of `code-stats-config.json` (kinds, their order, their keywords, their optional
`patterns` - regular expressions for the way an entry begins, tried only when no keyword matched - and the sub-headings that decide by themselves) and the first rule that matches wins, looking at the title of the entry first and at the whole text next. An entry that
no rule recognises is counted as `unclassified`, on purpose: the figures say how many entries the words could not place, they never guess.
"""
from __future__ import annotations

import re
from typing import Mapping, Sequence

UNCLASSIFIED = "unclassified"
SECTION = re.compile(r"^##\s+\[([^\]]+)\](?:\s*[-–—]\s*(.*))?\s*$")
SUBHEADING = re.compile(r"^###\s+(.+?)\s*$")
ENTRY = re.compile(r"^[-*]\s+(.*)$")
TITLE = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$", re.S)
VERSIONISH = re.compile(r"^v?\d+(\.\d+)*([-+][0-9A-Za-z.-]+)?$")


def check_rules(config: object) -> list[str]:
    """Problems of the `changelog` block of the configuration (an empty list when it is usable)."""
    if not isinstance(config, Mapping):
        return ["changelog is missing"]
    problems: list[str] = []
    kinds = config.get("kinds")
    if not isinstance(kinds, list) or not kinds or not all(isinstance(k, Mapping) and isinstance(k.get("key"), str) and isinstance(k.get("keywords"), list) for k in kinds):
        return ["changelog.kinds needs a list of {key, keywords}"]
    for k in kinds:
        for pattern in k.get("patterns", []):
            try:
                re.compile(pattern)
            except (re.error, TypeError):
                return ["changelog.kinds: %s has a pattern that is not a regular expression" % k["key"]]
    keys = [k["key"] for k in kinds]
    if len(set(keys)) != len(keys) or UNCLASSIFIED in keys:
        problems.append("changelog.kinds: keys must be distinct and not 'unclassified'")
    if not isinstance(config.get("headings"), Mapping) or any(v not in keys for v in config["headings"].values()):
        problems.append("changelog.headings must map a sub-heading to one of the kinds")
    if not isinstance(config.get("max_versions"), int) or config["max_versions"] <= 0:
        problems.append("changelog.max_versions must be a positive number")
    return problems


def kind_keys(config: Mapping) -> list[str]:
    """The kinds in the order the rules are tried, then `unclassified`."""
    return [k["key"] for k in config["kinds"]] + [UNCLASSIFIED]


def _compile(config: Mapping) -> list[tuple[str, "re.Pattern[str]", bool]]:
    """[(kind, pattern, weak)]: the keyword rules in the order of the kinds, then the `patterns` rules (weak ones, tried only when no keyword matched)."""
    strong, weak = [], []
    for kind in config["kinds"]:
        words = [w.strip().lower() for w in kind["keywords"] if isinstance(w, str) and w.strip()]
        if words:
            strong.append((kind["key"], re.compile(r"(?<![a-z0-9])(?:" + "|".join(re.escape(w) for w in words) + r")"), False))
        patterns = [p for p in kind.get("patterns", []) if isinstance(p, str) and p]        # regular expressions for the way a title or a text begins
        if patterns:
            weak.append((kind["key"], re.compile("|".join("(?:" + p + ")" for p in patterns)), True))
    return strong + weak


def classify(title: str, text: str, rules: Sequence[tuple], heading_kind: str | None = None, text_chars: int = 200) -> str:
    """The kind of an entry: the sub-heading it sits under, else the first keyword rule matching its title, else the first matching the start of its text,
    else (the same two looks) the first of the beginning-of-sentence patterns."""
    if heading_kind:
        return heading_kind
    for weak in (False, True):
        for part in (title, text[:text_chars]):
            lowered = part.lower()
            if not lowered.strip():
                continue
            for key, pattern, is_weak in rules:
                if is_weak == weak and pattern.search(lowered):
                    return key
    return UNCLASSIFIED


def parse(text: str) -> list[dict]:
    """[{name, unreleased, entries: [(title, text, heading)]}] in the order of the file (newest first, as the changelogs are written)."""
    sections: list[dict] = []
    current: dict | None = None
    heading: str | None = None
    entry: list[str] | None = None
    in_fence = False

    def close():
        nonlocal entry
        if entry is not None and current is not None:
            body = " ".join(part.strip() for part in entry if part.strip())
            match = TITLE.match(body)
            title, rest = (match.group(1).strip(" :"), match.group(2).strip()) if match else ("", body)
            current["entries"].append((title, rest, heading))
        entry = None

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        section = SECTION.match(line)
        if section:
            close()
            name = section.group(1).strip()
            current = {"name": name, "unreleased": name.lower() == "unreleased", "entries": []}
            sections.append(current)
            heading = None
            continue
        if line.startswith("## "):                      # a level-2 heading without brackets ends the sections we know
            close()
            current = None
            continue
        if current is None:
            continue
        sub = SUBHEADING.match(line)
        if sub:
            close()
            heading = sub.group(1).strip().lower()
            continue
        item = ENTRY.match(line)
        if item:
            close()
            entry = [item.group(1)]
            continue
        if entry is not None:
            if line.startswith((" ", "\t")) or (line and not line.startswith("#")):
                entry.append(line)
            elif not line.strip():
                close()
    close()
    return sections


def _label(title: str, body: str, limit: int) -> str:
    text = title or body
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def summarize(text: str | None, config: Mapping) -> dict | None:
    """The figures of one changelog, or None when the repository has none.

    {versions: published sections, entries: entries of published sections, unreleased: entries under [Unreleased], kinds: {kind: n} (published and
    unreleased together), published_kinds, avg: mean entries per published version, u: [[kind index, label]] entries of [Unreleased],
    v: [[name, entries, [n per kind], [[kind index, label]] for the newest `detail_versions`]] newest first, at most `max_versions`}.
    """
    if text is None:
        return None
    rules = _compile(config)
    keys = kind_keys(config)
    headings = {str(k).lower(): v for k, v in config["headings"].items()}
    limit = int(config.get("title_chars", 80))
    detail = int(config.get("detail_versions", 5))
    kinds = {k: 0 for k in keys}
    published_kinds = {k: 0 for k in keys}
    versions: list[list] = []
    waiting: list[list] = []
    published = unreleased = 0
    for section in parse(text):
        counts = {k: 0 for k in keys}
        listed: list[list] = []
        for title, body, heading in section["entries"]:
            kind = classify(title, body, rules, headings.get(heading or ""), int(config.get("text_chars", 200)))
            counts[kind] += 1
            listed.append([keys.index(kind), _label(title, body, limit)])
        n = len(section["entries"])
        if section["unreleased"]:
            unreleased += n
            waiting = listed[:60]
            for k, c in counts.items():
                kinds[k] += c
            continue
        if not VERSIONISH.match(section["name"]):          # a section that is not a version number is not a published version
            continue
        for k, c in counts.items():
            kinds[k] += c
            published_kinds[k] += c
        published += n
        row = [section["name"], n, [counts[k] for k in keys]]
        if len(versions) < detail:
            row.append(listed[:80])
        versions.append(row)
    count = len(versions)
    return {"versions": count, "entries": published, "unreleased": unreleased, "kinds": kinds, "published_kinds": published_kinds,
            "avg": round(published / count, 1) if count else 0, "u": waiting, "v": versions[: config["max_versions"]]}
