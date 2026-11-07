#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/check_data_read.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Refuses a dashboard whose data files were not read.

The Code, Changelog and Scripts tabs draw `data/code-stats.json` and `data/scripts-stats.json`, which the daily counter commits. A page generated before those files
exist (or from a file that cannot be read) shows "not verified" instead of figures; that is honest, but it must not be published silently. This script reads the page
the generator wrote and exits 1, naming the tabs, when a block it embeds has `read: false`.

    python scripts/check_data_read.py docs/index.html
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DATA = re.compile(r'<script type="application/json" id="dashboard-data">(.*?)</script>', re.S)
# the block of the page data, and the tabs that draw it
BLOCKS = {"code": ("Code", "Changelog"), "scripts": ("Scripts",)}


def unread_blocks(page: str) -> list[str]:
    """The names of the tabs whose data block of the page is not read ([] = every block was read). A page without data at all reports every tab."""
    match = DATA.search(page)
    tabs = [tab for names in BLOCKS.values() for tab in names]
    if not match:
        return tabs
    try:
        data = json.loads(match.group(1))
    except ValueError:
        return tabs
    out: list[str] = []
    for key, names in BLOCKS.items():
        block = data.get(key) if isinstance(data, dict) else None
        if not (isinstance(block, dict) and block.get("read") is True):
            out.extend(names)
    return out


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    path = Path(args[0]) if args else Path("docs/index.html")
    try:
        page = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"::error::{path} cannot be read ({type(error).__name__})")
        return 1
    missing = unread_blocks(page)
    if missing:
        print("::error::the page was generated without the figures of the tab(s) " + ", ".join(missing) + ": data/code-stats.json or data/scripts-stats.json was not read")
        return 1
    print("The Code, Changelog and Scripts figures were read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
