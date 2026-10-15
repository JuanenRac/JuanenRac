# =============================================================================
# JuanenRac profile - scripts/catalog_check.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Keeps ecosystem-catalog.json honest: its "ecosystems" list must name
exactly the ecosystems (key, label, manifest file) the dashboard actually
discovers. Stdlib only, so it runs before the updater packages are
installed and in the unit tests."""
from __future__ import annotations

import json
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parent.parent / "ecosystem-catalog.json"


def catalog_ecosystems(text: str) -> list[tuple[str, str, str]]:
    data = json.loads(text)
    items = data.get("ecosystems") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError("ecosystem-catalog.json has no 'ecosystems' list")
    out = []
    for item in items:
        if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item.get(k) for k in ("key", "label", "manifest_file")):
            raise ValueError(f"malformed ecosystem entry: {item!r}")
        out.append((item["key"], item["label"], item["manifest_file"]))
    return out


def mismatches(catalog: list[tuple[str, str, str]], dashboard: list[tuple[str, str, str]]) -> list[str]:
    """Human-readable differences between the catalog and what the dashboard
    discovers; empty when they agree (order does not matter)."""
    problems = []
    cat = {key: (label, manifest) for key, label, manifest in catalog}
    dash = {key: (label, manifest) for key, label, manifest in dashboard}
    for key in sorted(set(dash) - set(cat)):
        problems.append(f"the dashboard discovers '{key}' but the catalog does not list it")
    for key in sorted(set(cat) - set(dash)):
        problems.append(f"the catalog lists '{key}' but the dashboard does not discover it")
    for key in sorted(set(cat) & set(dash)):
        if cat[key] != dash[key]:
            problems.append(f"'{key}': catalog says {cat[key]}, dashboard uses {dash[key]}")
    return problems
