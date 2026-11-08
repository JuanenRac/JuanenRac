#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/gh_http.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""Conditional reads of the GitHub REST API with a saved copy, so that the quota is spared and a refused read does not stop the build.

  * Every answer that carries an `ETag` is kept (URL, tag, body, moment). The next read of the same URL sends `If-None-Match`; a `304 Not Modified` costs no quota
    and the saved body is used.
  * When GitHub refuses the read because the quota is spent (`429`, or `403` with no requests remaining, a `Retry-After`, or a message about the rate limit) or
    cannot be reached, the saved body is used instead of failing, as long as it is not older than `stale_max_hours`. The reply says it is a saved copy and how old
    it is, so the page can mark it; it is never presented as current.
  * With no saved body the failure is reported exactly as before (the caller decides).
  * A caller that knows when the thing it reads last changed (the `pushed_at` of a repository) says so with `unchanged_since`: when the saved body is newer than that moment
    it is used without any request at all, which is the saving that works with the token of a workflow (GitHub keys an ETag to the token that read it, so a new token
    in every run never gets a 304 for what another token read).

The saved copy is a small JSON file (`data/etag-cache.json`, not committed: the build restores and stores it with the Actions cache). Its limits (entries, size of a
body, age) are read from `http_cache` in dashboard-config.json. Stdlib only; the network is only touched through the `opener` argument, so the tests use none.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "dashboard-config.json"
CACHE_PATH = ROOT / "data" / "etag-cache.json"
SCHEMA = 1
DEFAULT_CONFIG: dict = {"enabled": True, "max_entries": 600, "max_body_bytes": 400000, "stale_max_hours": 72, "path": "data/etag-cache.json", "unchanged_margin_seconds": 120}
QUOTA_WORDS = ("rate limit", "abuse", "secondary", "quota")


def check_config(raw: object) -> tuple[dict, list[str]]:
    config = dict(DEFAULT_CONFIG)
    problems: list[str] = []
    if raw is None:
        return config, problems
    if not isinstance(raw, Mapping):
        return config, ["http_cache: not an object"]
    if "enabled" in raw:
        if isinstance(raw["enabled"], bool):
            config["enabled"] = raw["enabled"]
        else:
            problems.append("http_cache.enabled: needs true or false")
    for key, low, high in (("max_entries", 10, 5000), ("max_body_bytes", 1000, 1_000_000), ("stale_max_hours", 1, 24 * 30), ("unchanged_margin_seconds", 0, 86400)):
        if key in raw:
            value = raw[key]
            if isinstance(value, int) and not isinstance(value, bool) and low <= value <= high:
                config[key] = value
            else:
                problems.append(f"http_cache.{key}: needs an integer from {low} to {high}")
    if "path" in raw:
        value = raw["path"]
        if isinstance(value, str) and value.startswith("data/") and ".." not in value and not value.startswith("/") and value.endswith(".json"):
            config["path"] = value
        else:
            problems.append("http_cache.path: needs a .json file inside data/")
    return config, problems


def load_config(path: Path = CONFIG_PATH) -> tuple[dict, list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return check_config(None)
    except (OSError, ValueError) as exc:
        return check_config(None)[0], [f"{path.name} could not be read for the saved copy of the reads ({exc})"]
    return check_config(raw.get("http_cache") if isinstance(raw, Mapping) else None)


def is_quota_refusal(code: int, headers: Mapping | None, body: str = "") -> bool:
    """True when an HTTP refusal means "the quota is spent / slow down" and not "forbidden" or "not found"."""
    if code == 429:
        return True
    if code != 403:
        return False
    lowered = {str(k).lower(): str(v) for k, v in (headers or {}).items()}
    if lowered.get("x-ratelimit-remaining") == "0" or "retry-after" in lowered:
        return True
    text = body.lower()
    return any(word in text for word in QUOTA_WORDS)


@dataclass(frozen=True)
class Reply:
    """`how`: "fresh" (200), "not_modified" (304, the saved body is current), "unchanged" (no request: the saved body is newer than the last change), "stale" (refused or unreachable: the saved body, `age_seconds` old) or "failed"."""
    data: object
    how: str
    age_seconds: int = 0
    reason: str = ""


class ConditionalGet:
    def __init__(self, path: Path | None = None, config: Mapping | None = None, clock: Callable[[], float] = time.time):
        self.config = dict(DEFAULT_CONFIG, **(config or {}))
        self.path = Path(path) if path else None
        self.clock = clock
        self.lock = threading.Lock()
        self.entries: dict[str, dict] = {}
        self.stats = {"requests": 0, "fresh": 0, "not_modified": 0, "skipped": 0, "stale": 0, "failed": 0, "oldest_stale": 0, "refused": 0}
        self.dirty = False
        self._load()

    # -- the saved copy ------------------------------------------------------
    def _load(self) -> None:
        if not self.path:
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if not isinstance(raw, Mapping) or raw.get("schema") != SCHEMA or not isinstance(raw.get("entries"), Mapping):
            return
        for url, item in raw["entries"].items():
            if isinstance(url, str) and isinstance(item, Mapping) and isinstance(item.get("etag"), str) and isinstance(item.get("body"), str) and isinstance(item.get("at"), int):
                self.entries[url] = {"etag": item["etag"], "body": item["body"], "at": item["at"]}

    def save(self) -> bool:
        """Writes the saved copy (at most `max_entries`, the newest) when something changed. True when the file was written."""
        if not self.path or not self.dirty or not self.config["enabled"]:
            return False
        with self.lock:
            newest = sorted(self.entries.items(), key=lambda kv: -kv[1]["at"])[: self.config["max_entries"]]
            text = json.dumps({"schema": SCHEMA, "entries": dict(sorted(newest))}, ensure_ascii=False, separators=(",", ":")) + "\n"
            self.dirty = False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(text, encoding="utf-8", newline="\n")
        os.replace(tmp, self.path)
        return True

    # -- reading -------------------------------------------------------------
    def _saved(self, url: str) -> dict | None:
        item = self.entries.get(url)
        if item is None or not self.config["enabled"]:
            return None
        return item

    def _stale_reply(self, url: str, reason: str) -> Reply:
        item = self._saved(url)
        if item is not None:
            age = max(0, int(self.clock()) - item["at"])
            if age <= self.config["stale_max_hours"] * 3600:
                try:
                    data = json.loads(item["body"])
                except ValueError:
                    data = None
                if data is not None:
                    with self.lock:
                        self.stats["stale"] += 1
                        self.stats["oldest_stale"] = max(self.stats["oldest_stale"], age)
                    return Reply(data, "stale", age, reason)
        with self.lock:
            self.stats["failed"] += 1
        return Reply(None, "failed", 0, reason)

    def get(self, url: str, headers: Mapping[str, str], timeout: float = 20, opener: Callable = urllib.request.urlopen, unchanged_since: "int | None" = None) -> Reply:
        """`unchanged_since` (epoch seconds) is the moment the thing last changed, when the caller knows it: a saved body received after it (plus the margin of the
        configuration) is still current and is returned with no request."""
        sent = dict(headers)
        item = self._saved(url)
        if item is not None and unchanged_since is not None and item["at"] >= int(unchanged_since) + self.config["unchanged_margin_seconds"]:
            try:
                data = json.loads(item["body"])
            except ValueError:
                data = None
            if data is not None:
                with self.lock:
                    self.stats["skipped"] += 1
                return Reply(data, "unchanged", 0)
        if item is not None:
            sent["If-None-Match"] = item["etag"]
        with self.lock:
            self.stats["requests"] += 1
        request = urllib.request.Request(url, headers=sent, method="GET")
        try:
            with opener(request, timeout=timeout) as response:
                raw = response.read()
                etag = response.headers.get("ETag") if getattr(response, "headers", None) else None
        except urllib.error.HTTPError as exc:
            if exc.code == 304 and item is not None:
                with self.lock:
                    self.stats["not_modified"] += 1
                try:
                    return Reply(json.loads(item["body"]), "not_modified", 0)
                except ValueError:
                    return Reply(None, "failed", 0, "saved body unreadable")
            try:
                body = exc.read(2000).decode("utf-8", errors="replace")
            except Exception:  # noqa: BLE001 - the body of an error is only a hint
                body = ""
            if is_quota_refusal(exc.code, getattr(exc, "headers", None), body):
                with self.lock:
                    self.stats["refused"] += 1
                return self._stale_reply(url, f"HTTP {exc.code} (quota)")
            if exc.code in (500, 502, 503, 504):
                return self._stale_reply(url, f"HTTP {exc.code}")
            with self.lock:
                self.stats["failed"] += 1
            return Reply(None, "failed", 0, f"HTTP {exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return self._stale_reply(url, f"unreachable: {exc}")
        try:
            data = json.loads(raw.decode("utf-8", errors="replace"))
        except ValueError:
            with self.lock:
                self.stats["failed"] += 1
            return Reply(None, "failed", 0, "not JSON")
        with self.lock:
            self.stats["fresh"] += 1
            if etag and self.config["enabled"] and len(raw) <= self.config["max_body_bytes"]:
                self.entries[url] = {"etag": etag, "body": raw.decode("utf-8", errors="replace"), "at": int(self.clock())}
                self.dirty = True
        return Reply(data, "fresh", 0)

    def summary(self) -> dict:
        """Figures for the page: reads made, reads that cost nothing (304), reads answered from the saved copy and the age of the oldest of them."""
        with self.lock:
            return dict(self.stats)


_shared: ConditionalGet | None = None


def shared() -> ConditionalGet:
    """The one saved copy of this run (configured from dashboard-config.json, stored at the path it names)."""
    global _shared
    if _shared is None:
        config, _problems = load_config()
        _shared = ConditionalGet(ROOT / config["path"], config)
    return _shared


def reset_shared() -> None:
    global _shared
    _shared = None
