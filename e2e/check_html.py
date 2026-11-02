# =============================================================================
# JuanenRac profile - e2e/check_html.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Structural validation of the generated dashboard page, with no dependency (Python standard library only).

Usage: python check_html.py [PAGE ...]      (default: ../docs/index.html)

Checks: balanced tags, duplicate ids, references to ids that do not exist (anchors, aria-*, label for, details targets,
tab / panel pairs), names of controls, required attributes (lang, charset, viewport, title, alt, rel on new-tab links),
the translation keys used by the page against the eight dictionaries embedded in it, duplicate keys in the Python
dictionaries that feed them, and the coherence of the data-* attributes the script relies on.
Exit code 0 = clean, 1 = problems (one per line).
"""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# Elements the HTML parser may leave open without it being a defect (optional end tags).
OPTIONAL_END = {"p", "li", "td", "th", "tr", "tbody", "thead", "tfoot", "option", "dt", "dd"}
MATURITY = {"scaffolding", "functional", "established", "production"}
ECOSYSTEMS = {"hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"}
REF_ATTRS = ("aria-controls", "aria-labelledby", "aria-describedby", "aria-owns")


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.problems: list[str] = []
        self.stack: list[tuple[str, int]] = []
        self.ids: Counter[str] = Counter()
        self.refs: list[tuple[str, str, int]] = []      # (kind, id, line)
        self.elements: list[dict] = []
        self.text_of: dict[int, str] = {}
        self._open: list[dict] = []
        self.title = ""
        self._in_title = False
        self._script = False
        self.scripts: list[str] = []
        self._script_buf: list[str] = []
        self.labels_for: set[str] = set()

    def problem(self, line: int, text: str) -> None:
        self.problems.append(f"line {line}: {text}")

    # ----- parsing -----
    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        a = {k: (v if v is not None else "") for k, v in attrs}
        el = {"tag": tag, "attrs": a, "line": line, "text": [], "children": []}
        self.elements.append(el)
        if self._open:
            self._open[-1]["children"].append(el)
        if "id" in a:
            self.ids[a["id"]] += 1
        for key in REF_ATTRS:
            for ident in a.get(key, "").split():
                self.refs.append((key, ident, line))
        if tag == "label" and a.get("for"):
            self.refs.append(("label for", a["for"], line))
            self.labels_for.add(a["for"])
        if tag == "a" and a.get("href", "").startswith("#") and len(a["href"]) > 1:
            self.refs.append(("href", a["href"][1:], line))
        if tag == "title":
            self._in_title = True
        if tag == "script":
            self._script = True
            self._script_buf = []
        if tag in VOID:
            return
        self.stack.append((tag, line))
        self._open.append(el)

    def handle_startendtag(self, tag, attrs):  # <svg ... /> and friends
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag in VOID:
            return
        if tag == "script":
            self._script = False
            self.scripts.append("".join(self._script_buf))
        if tag == "title":
            self._in_title = False
        while self.stack and self.stack[-1][0] != tag and self.stack[-1][0] in OPTIONAL_END:
            self.stack.pop()
            self._open.pop()
        if not self.stack or self.stack[-1][0] != tag:
            self.problem(line, f"</{tag}> closes nothing that is open (open: {self.stack[-1][0] if self.stack else 'none'})")
            return
        self.stack.pop()
        self._open.pop()

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._script:
            self._script_buf.append(data)
        for el in self._open:
            el["text"].append(data)


def text(el: dict) -> str:
    return "".join(el["text"]).strip()


def accessible_name(el: dict, by_id: dict[str, dict]) -> str:
    a = el["attrs"]
    if a.get("aria-label", "").strip():
        return a["aria-label"]
    for ident in a.get("aria-labelledby", "").split():
        if ident in by_id and text(by_id[ident]):
            return text(by_id[ident])
    if text(el):
        return text(el)
    for child in el["children"]:
        if child["tag"] == "svg" and (child["attrs"].get("aria-label") or any(c["tag"] == "title" for c in child["children"])):
            return "svg"
        if child["tag"] == "img" and child["attrs"].get("alt"):
            return child["attrs"]["alt"]
    return a.get("title", "").strip()


def duplicate_dict_keys(path: Path) -> list[str]:
    """Python keeps the last of two equal keys in a dict literal without a word; a duplicated translation key hides a text."""
    out: list[str] = []
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            for key, n in Counter(keys).items():
                if n > 1 and len(keys) > 5:
                    out.append(f"{path.name}: key {key!r} appears {n} times in the same dictionary (line {node.lineno})")
    return out


def check(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    page = Page()
    page.feed(raw)
    page.close()
    problems = list(page.problems)
    by_id = {el["attrs"]["id"]: el for el in page.elements if "id" in el["attrs"]}

    for tag, line in page.stack:
        if tag not in OPTIONAL_END and tag not in ("html", "body"):
            problems.append(f"line {line}: <{tag}> is never closed")
    if not re.match(r"\s*<!doctype html>", raw, re.I):
        problems.append("line 1: missing <!doctype html>")

    # --- document level ---
    html = next((e for e in page.elements if e["tag"] == "html"), None)
    if not html or not html["attrs"].get("lang"):
        problems.append("<html> has no lang attribute")
    if not any(e["tag"] == "meta" and e["attrs"].get("charset") for e in page.elements):
        problems.append("missing <meta charset>")
    if not any(e["tag"] == "meta" and e["attrs"].get("name") == "viewport" for e in page.elements):
        problems.append("missing <meta name=viewport>")
    if not page.title.strip():
        problems.append("empty <title>")
    for tag in ("h1", "main"):
        count = sum(1 for e in page.elements if e["tag"] == tag)
        if count != 1:
            problems.append(f"expected exactly one <{tag}>, found {count}")

    # --- ids ---
    for ident, n in page.ids.items():
        if n > 1:
            problems.append(f"duplicate id {ident!r} ({n} times)")
    for kind, ident, line in page.refs:
        if ident not in page.ids:
            problems.append(f"line {line}: {kind} refers to #{ident}, which does not exist")

    # --- controls and names ---
    for el in page.elements:
        tag, a, line = el["tag"], el["attrs"], el["line"]
        if tag == "a":
            if "href" not in a:
                problems.append(f"line {line}: <a> without href")
            if a.get("target") == "_blank" and "noopener" not in a.get("rel", ""):
                problems.append(f"line {line}: <a target=_blank href={a.get('href', '')[:60]!r}> without rel=noopener")
            if a.get("href", "").startswith("http://"):
                problems.append(f"line {line}: insecure link {a['href'][:60]!r}")
            if not accessible_name(el, by_id):
                problems.append(f"line {line}: link {a.get('href', '')[:60]!r} has no accessible name")
        elif tag == "button":
            if "type" not in a:
                problems.append(f"line {line}: <button> without type")
            if not accessible_name(el, by_id):
                problems.append(f"line {line}: <button id={a.get('id', '')!r}> has no accessible name")
        elif tag in ("input", "select", "textarea") and a.get("type") != "hidden":
            named = a.get("aria-label") or a.get("aria-labelledby") or (a.get("id") in page.labels_for) or a.get("title")
            if not named:
                problems.append(f"line {line}: <{tag} id={a.get('id', '')!r}> has no label")
        elif tag == "img":
            if "alt" not in a:
                problems.append(f"line {line}: <img> without alt")
        elif tag == "svg" and a.get("role") == "img":
            if not (a.get("aria-label") or a.get("aria-labelledby") or any(c["tag"] == "title" for c in el["children"])):
                problems.append(f"line {line}: <svg role=img> without a name")
        elif tag == "table":
            if not any(c["tag"] in ("thead", "tr") for c in el["children"]):
                problems.append(f"line {line}: <table> without rows")
        elif tag == "th" and not text(el) and not a.get("aria-label"):
            problems.append(f"line {line}: empty <th>")
        elif tag == "details" and not any(c["tag"] == "summary" for c in el["children"]):
            problems.append(f"line {line}: <details> without <summary>")

    # --- translations ---
    keys: set[str] = set()
    for el in page.elements:
        for name, value in el["attrs"].items():
            if name == "data-i18n" or (name.startswith("data-i18n-") and name != "data-i18n-template") or name == "data-i18n-template":
                keys.add(value)
    dictionaries = None
    for script in page.scripts:
        m = re.search(r"const I18N = (\{.*?\});\s*\n", script, re.S)
        if m:
            try:
                dictionaries = json.loads(m.group(1))
            except ValueError as exc:
                problems.append(f"the embedded translations are not valid JSON: {exc}")
    if dictionaries is None:
        problems.append("the embedded translations (const I18N) were not found")
    else:
        for lang in LANGS:
            if lang not in dictionaries:
                problems.append(f"the language {lang} is missing from the embedded translations")
                continue
            missing = sorted(k for k in keys if k not in dictionaries[lang])
            if missing:
                problems.append(f"{lang}: {len(missing)} translation key(s) used by the page are missing: {', '.join(missing[:8])}")
            empty = sorted(k for k, v in dictionaries[lang].items() if not str(v).strip())
            if empty:
                problems.append(f"{lang}: empty translation(s): {', '.join(empty[:8])}")
        reference = set(dictionaries.get("en", {}))
        for lang in LANGS:
            other = set(dictionaries.get(lang, {}))
            if other != reference:
                problems.append(f"{lang}: its keys differ from English ({len(other ^ reference)} different, e.g. {sorted(other ^ reference)[:5]})")

    # --- data-* coherence ---
    rows = [e for e in page.elements if "project-row" in e["attrs"].get("class", "").split()]
    details = {e["attrs"]["id"]: e for e in page.elements if "detail-row" in e["attrs"].get("class", "").split()}
    for row in rows:
        a, line = row["attrs"], row["line"]
        if a.get("data-status") not in ("ok", "error"):
            problems.append(f"line {line}: project row {a.get('data-name')!r} has data-status={a.get('data-status')!r}")
        if a.get("data-maturity") not in MATURITY:
            problems.append(f"line {line}: project row {a.get('data-name')!r} has data-maturity={a.get('data-maturity')!r}")
        if a.get("data-ecosystem") not in ECOSYSTEMS:
            problems.append(f"line {line}: project row {a.get('data-name')!r} has data-ecosystem={a.get('data-ecosystem')!r}")
        if ("status-" + a.get("data-status", "")) not in a.get("class", "").split():
            problems.append(f"line {line}: project row {a.get('data-name')!r}: class and data-status disagree")
        toggles = [c for c in _walk(row) if "details-toggle" in c["attrs"].get("class", "").split()]
        if len(toggles) != 1:
            problems.append(f"line {line}: project row {a.get('data-name')!r} has {len(toggles)} details toggles")
            continue
        target = toggles[0]["attrs"].get("data-details-target", "")
        detail = details.get(target)
        if detail is None:
            problems.append(f"line {line}: details toggle points to {target!r}, which is not a detail row")
        elif detail["attrs"].get("data-name") != a.get("data-name"):
            problems.append(f"line {line}: detail row {target!r} belongs to another project ({detail['attrs'].get('data-name')!r})")
        if toggles[0]["attrs"].get("aria-expanded") != "false":
            problems.append(f"line {line}: details toggle of {a.get('data-name')!r} does not start collapsed")
    names = Counter(r["attrs"].get("data-name") for r in rows)
    for name, n in names.items():
        if n > 1:
            problems.append(f"project {name!r} appears in {n} rows")

    present = {kind: {r["attrs"].get(f"data-{kind}") for r in rows} for kind in ("maturity", "role", "deploy", "ecosystem", "status")}
    for el in page.elements:
        for kind in ("maturity", "role", "deploy", "eco", "status"):
            value = el["attrs"].get(f"data-filter-{kind}")
            if value is not None and rows:
                have = present["ecosystem" if kind == "eco" else kind]
                if value not in have and value != "all":
                    counts = [text(c) for c in el["children"] if c["tag"] == "b"]
                    if counts and counts[-1] != "0":
                        problems.append(f"line {el['line']}: filter {kind}={value!r} matches no row but shows the count {counts[-1]!r}")

    tabs = {e["attrs"]["data-tab"]: e for e in page.elements if e["tag"] == "button" and "data-tab" in e["attrs"]}
    panels = {e["attrs"]["id"] for e in page.elements if e["attrs"].get("role") == "tabpanel"}
    for ident, el in tabs.items():
        if el["attrs"].get("aria-controls") != f"panel-{ident}" or f"panel-{ident}" not in panels:
            problems.append(f"line {el['line']}: tab {ident!r} and its panel do not match")
    for panel in panels:
        if panel.replace("panel-", "") not in tabs:
            problems.append(f"panel {panel!r} has no tab")
    for el in page.elements:
        goto = el["attrs"].get("data-goto-tab")
        if goto and goto not in tabs:
            problems.append(f"line {el['line']}: data-goto-tab={goto!r} is not a tab")
        eco = el["attrs"].get("data-show-eco")
        if eco and eco not in ECOSYSTEMS:
            problems.append(f"line {el['line']}: data-show-eco={eco!r} is not an ecosystem")
    for view_attr, panel_attr in (("data-arch-view", "data-arch-panel"), ("data-compat-view", "data-compat-panel")):
        views = {e["attrs"][view_attr] for e in page.elements if view_attr in e["attrs"]}
        pans = {e["attrs"][panel_attr] for e in page.elements if panel_attr in e["attrs"]}
        if views != pans:
            problems.append(f"{view_attr} {sorted(views)} and {panel_attr} {sorted(pans)} do not match")
    selected = [t for t in tabs.values() if t["attrs"].get("aria-selected") == "true"]
    if len(selected) > 1:
        problems.append("more than one tab starts selected")
    for t in tabs.values():
        if t["attrs"].get("aria-selected") not in ("true", "false"):
            problems.append(f"line {t['line']}: tab without aria-selected")
    return problems


def _walk(el: dict):
    for child in el["children"]:
        yield child
        yield from _walk(child)


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    pages = [Path(a) for a in argv] or [ROOT / "docs" / "index.html"]
    total = 0
    for path in pages:
        problems = check(path)
        print(f"{path}: {len(problems)} problem(s)")
        for problem in problems:
            print("  - " + problem)
        total += len(problems)
    sources = [ROOT / "scripts" / name for name in ("generate_dashboard.py", "dashboard_texts.py", "dashboard_app_texts.py", "dashboard_app.py", "dashboard_charts.py")]
    dupes = [p for source in sources if source.exists() for p in duplicate_dict_keys(source)]
    print(f"python sources: {len(dupes)} duplicate dictionary key(s)")
    for problem in dupes:
        print("  - " + problem)
    total += len(dupes)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
