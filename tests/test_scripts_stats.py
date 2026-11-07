# =============================================================================
# JuanenRac profile - tests/test_scripts_stats.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The reader of the workflows and the own scripts of a repository, and the block the page embeds. No network."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_scripts as ds  # noqa: E402
import scripts_stats as ss  # noqa: E402

BLOCK_ON = """name: Build the thing
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "37 3 * * *"
  workflow_dispatch:
permissions: {}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: ./.github/actions/local
  deploy:
    runs-on: ${{ matrix.os }}
    needs: build
    steps:
      - uses: some/tool@main
      - uses: docker://alpine:3.19
"""


class TriggerTests(unittest.TestCase):
    def test_a_block_of_events(self):
        self.assertEqual(ss.trigger_names(BLOCK_ON.splitlines()), ["push", "pull_request", "schedule", "workflow_dispatch"])

    def test_a_list_and_a_single_event(self):
        self.assertEqual(ss.trigger_names(["on: [push, release]", "jobs:"]), ["push", "release"])
        self.assertEqual(ss.trigger_names(["on: workflow_dispatch"]), ["workflow_dispatch"])
        self.assertEqual(ss.trigger_names(['"on":', "  workflow_call:"]), ["workflow_call"])

    def test_an_unknown_event_is_other(self):
        self.assertEqual(ss.trigger_names(["on:", "  push:", "  issues:"]), ["push", "other"])

    def test_no_on_key(self):
        self.assertEqual(ss.trigger_names(["name: x", "jobs:", "  a:"]), [])

    def test_a_list_under_on(self):
        self.assertEqual(ss.trigger_names(["on:", "  - push", "  - pull_request"]), ["push", "pull_request"])


class WorkflowTests(unittest.TestCase):
    def test_jobs_and_runners(self):
        lines = BLOCK_ON.splitlines()
        self.assertEqual(ss.job_count(lines), 2)
        self.assertEqual(ss.runner_names(lines), ["matrix", "ubuntu-latest"])

    def test_the_pin_of_an_action(self):
        self.assertEqual(ss.pin_of("actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803"), "sha")
        self.assertEqual(ss.pin_of("actions/setup-python@v5"), "tag")
        self.assertEqual(ss.pin_of("actions/setup-python@v5.1.0"), "tag")
        self.assertEqual(ss.pin_of("some/tool@main"), "branch")
        self.assertEqual(ss.pin_of("some/tool"), "branch")
        self.assertEqual(ss.pin_of("./.github/actions/local"), "local")
        self.assertEqual(ss.pin_of("docker://alpine:3.19"), "docker")

    def test_a_workflow_record(self):
        record, uses = ss.workflow_record("build.yml", BLOCK_ON)
        self.assertEqual(record[:2], ["build.yml", "Build the thing"])
        self.assertEqual(record[3], 2)
        self.assertEqual(len(uses), 5)

    def test_a_trailing_comment_is_not_part_of_the_action(self):
        self.assertEqual(ss.action_uses(["      - uses: actions/checkout@abc # v6"]), ["actions/checkout@abc"])


class TreeTests(unittest.TestCase):
    def test_summarize_a_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text(BLOCK_ON, encoding="utf-8")
            (root / ".github" / "workflows" / "notes.txt").write_text("not a workflow", encoding="utf-8")
            (root / "tools").mkdir()
            (root / "tools" / "a.py").write_text("x = 1\ny = 2\n", encoding="utf-8")
            (root / "tools" / "b.sh").write_text("echo hi\n", encoding="utf-8")
            (root / "scripts" / "deep").mkdir(parents=True)
            (root / "scripts" / "deep" / "c.ps1").write_text("a\nb\nc\n", encoding="utf-8")
            (root / "scripts" / "run.cmd").write_text("@echo off\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print(1)\n", encoding="utf-8")        # not a script of the repository tools
            got = ss.summarize(root)
        self.assertEqual([w[0] for w in got["wf"]], ["ci.yml"])
        self.assertEqual(got["acts"]["actions/setup-python@v5"], [1, "tag"])
        self.assertEqual(got["acts"]["some/tool@main"], [1, "branch"])
        self.assertEqual(got["sc"], {"py": [1, 2], "sh": [1, 1], "ps1": [1, 3], "bat": [1, 1]})

    def test_a_repository_without_either(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(ss.summarize(Path(tmp)), {"wf": [], "acts": {}, "sc": {}})

    def test_the_totals(self):
        repos = {"a": {"scripts": {"wf": [["x.yml", "x", ["push"], 2, []]], "acts": {"u@v1": [3, "tag"], "u@" + "a" * 40: [2, "sha"]}, "sc": {"py": [2, 10]}}},
                 "b": {"scripts": None}, "c": {}}
        self.assertEqual(ss.totals(repos), {"repos": 1, "workflows": 1, "jobs": 2, "uses": 5, "unpinned": 3, "files": 2, "lines": 10})


class DocumentTests(unittest.TestCase):
    def test_the_document_keeps_the_last_known_scripts_of_a_repository_that_could_not_be_read_today(self):
        import code_stats as cs
        config = cs.load_config()
        records = {"ARMOR-A": {"eco": "armor", "type": "tools", "state": "ok", "scripts": {"wf": [], "acts": {}, "sc": {}}},
                   "ARMOR-B": {"eco": "armor", "type": "tools", "state": "lastknown"},
                   "ARMOR-C": {"eco": "armor", "type": "tools", "state": "lastknown"},
                   "ARMOR-D": {"eco": "armor", "type": "tools", "state": "unread"}}
        previous = {"ARMOR-B": {"scripts": {"wf": [["x.yml", "x", ["push"], 1, []]], "acts": {}, "sc": {}}}}
        doc = cs.scripts_document("2001-01-02", config, records, previous)
        self.assertEqual(doc["repos"]["ARMOR-A"]["scripts"], {"wf": [], "acts": {}, "sc": {}})
        self.assertEqual(doc["repos"]["ARMOR-B"]["state"], "lastknown")
        self.assertEqual(doc["repos"]["ARMOR-B"]["scripts"]["wf"][0][0], "x.yml")
        self.assertEqual(doc["repos"]["ARMOR-C"]["state"], "unread")                        # nothing known before: not read, never zero
        self.assertNotIn("scripts", doc["repos"]["ARMOR-D"])
        self.assertEqual(doc["owner"], config["owner"])


class BlockTests(unittest.TestCase):
    DOC = {"schema": 1, "day": "2001-01-02", "owner": "JuanenRac", "ecosystems": [{"key": "armor", "label": "A.R.M.O.R."}], "types": ["tools"],
           "repos": {"ARMOR-X": {"eco": "armor", "type": "tools", "state": "ok",
                                 "scripts": {"wf": [["ci.yml", "CI", ["push", "bogus"], 2, ["ubuntu-latest"]]], "acts": {"actions/checkout@v6": [1, "tag"], "x": [1, "weird"]},
                                             "sc": {"py": [2, 20], "rb": [1, 1]}}},
                     "NOPE": {"eco": "other", "type": "tools", "state": "ok", "scripts": {}},
                     "ARMOR-Y": {"eco": "armor", "type": "tools", "state": "unread"}}}

    def test_the_block_is_rebuilt_from_a_whitelist(self):
        got = ds.build(self.DOC, "2001-01-04")
        self.assertTrue(got["read"])
        self.assertEqual(got["age"], 2)
        self.assertEqual(sorted(got["repos"]), ["ARMOR-X", "ARMOR-Y"])
        block = got["repos"]["ARMOR-X"]["scripts"]
        self.assertEqual(block["wf"], [["ci.yml", "CI", ["push"], 2, ["ubuntu-latest"]]])      # an unknown trigger is dropped
        self.assertEqual(block["acts"], {"actions/checkout@v6": [1, "tag"]})                 # an unknown pin is dropped
        self.assertEqual(block["sc"], {"py": [2, 20]})                                         # an unknown language is dropped
        self.assertIsNone(got["repos"]["ARMOR-Y"].get("scripts"))

    def test_nothing_read_is_not_verified(self):
        self.assertFalse(ds.build(None)["read"])
        self.assertFalse(ds.build({"schema": 2, "repos": {}})["read"])
        self.assertFalse(ds.build({"schema": 1, "repos": {"A": {"eco": "x", "type": "t", "state": "unread"}}, "ecosystems": [], "types": []})["read"])

    def test_the_page_block_is_plain_json(self):
        import json
        got = ds.build(self.DOC, "2001-01-04")
        self.assertEqual(json.loads(json.dumps(got)), got)


if __name__ == "__main__":
    unittest.main()
