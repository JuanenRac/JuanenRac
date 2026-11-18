# =============================================================================
# JuanenRac profile - tests/test_sentinel_cli.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The command line that reads the Sentinel figures from the data files: the five groups of the catalogue in order, a group with nothing read as not verified, the six
formats, the exit codes and the guarantee that it never makes a request."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sentinel_cli as cli  # noqa: E402

ORDER = [("hydra-umc", "HYDRA-UMC"), ("urtc", "URTC"), ("armor", "A.R.M.O.R."), ("eh3d", "EH3D"), ("electro-hobby-3d", "Tools")]
SENTINEL = {
    "ecosystems": {"hydra-umc": {"repos": 3, "read": 3, "red": 1, "cand": 2, "unpub": 0}, "urtc": {"repos": 2, "read": 2, "red": 0, "cand": 0, "unpub": 0},
                   "armor": {"repos": 1, "read": 0, "red": 0, "cand": 0, "unpub": 0}},
    "delivery": {"eco": {"hydra-umc": {"repos": 3, "read": 3, "tagahead": 1, "nonotes": 0, "clmis": 0}, "urtc": {"repos": 2, "read": 2, "tagahead": 0, "nonotes": 0, "clmis": 0}}},
    "ci": {"red": [{"repo": "HYDRA-UMC-A", "wf": "ci.yml", "streak": 2, "since": "2001-12-20T10:00:00Z"}]},
    "releases": {"candidates": [{"repo": "HYDRA-UMC-B", "entries": 7, "tag": "v1.0.0", "published": "2001-12-01T10:00:00Z"}]},
}
SCRIPTS = {"repos": {
    "HYDRA-UMC-A": {"eco": "hydra-umc", "state": "ok", "scripts": {"acts": {"a/b@main": [2, "branch"], "a/c@v4": [3, "tag"], "a/d@" + "0" * 40: [5, "sha"]},
                                                                    "lint": {"rules": {"permissions": [0, 1, 0], "pr_target": [0, 0, 0]}}}},
    "URTC-A": {"eco": "urtc", "state": "ok", "scripts": {"acts": {"a/d@" + "0" * 40: [4, "sha"]}}},
    "URTC-B": {"eco": "urtc", "state": "unread"},
}}


def run(argv, data=None):
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv + (["--data", str(data)] if data else []), out, err)
    return code, out.getvalue(), err.getvalue()


class RowTests(unittest.TestCase):
    def test_the_groups_come_from_the_catalogue_in_order(self):
        self.assertEqual(cli.groups(), ORDER)

    def test_ecosystem_rows_list_all_five_and_never_show_zero_for_what_was_not_read(self):
        rows = cli.ecosystem_rows(SENTINEL, ORDER)
        self.assertEqual([r["group"] for r in rows], [g[1] for g in ORDER])
        self.assertEqual(rows[0]["state"], "to review")
        self.assertEqual(rows[1]["state"], "in order")
        for row in rows[2:]:
            self.assertEqual(row["state"], "not verified")
            self.assertEqual(row["red"], "not verified")

    def test_supply_rows_count_the_pins_and_the_findings_and_skip_unread_repositories(self):
        rows = cli.supply_rows(SCRIPTS, ORDER)
        self.assertEqual((rows[0]["read"], rows[0]["unpinned"], rows[0]["branch"], rows[0]["permissions"], rows[0]["pr_target"]), (1, 5, 2, 1, 0))
        self.assertEqual(rows[0]["state"], "to review")
        self.assertEqual((rows[1]["read"], rows[1]["unpinned"], rows[1]["state"]), (1, 0, "in order"))       # the unread repository is not counted
        self.assertEqual(rows[4]["state"], "not verified")

    def test_delivery_rows_and_the_reading_that_predates_them(self):
        rows = cli.delivery_rows(SENTINEL, ORDER)
        self.assertEqual(rows[0]["tag_without_release"], 1)
        self.assertEqual(rows[0]["state"], "to review")
        self.assertEqual(rows[2]["state"], "not verified")
        self.assertIsNone(cli.delivery_rows({"ecosystems": {}}, ORDER))

    def test_red_and_ready_lists(self):
        self.assertEqual(cli.red_rows(SENTINEL), [{"repository": "HYDRA-UMC-A", "workflow": "ci.yml", "in_a_row": 2, "since": "2001-12-20T10:00:00Z"}])
        self.assertEqual(cli.ready_rows(SENTINEL)[0]["entries"], 7)
        self.assertEqual(cli.red_rows({}), [])

    def test_garbage_in_the_data_is_counted_as_zero_and_never_raises(self):
        rows = cli.supply_rows({"repos": {"X": {"eco": "urtc", "state": "ok", "scripts": {"acts": {"k": "no", "j": [True, "branch"], "m": [-4, "tag"]}, "lint": "x"}}}}, ORDER)
        self.assertEqual(rows[1]["unpinned"], 0)


class FormatTests(unittest.TestCase):
    ROWS = [{"group": "URTC", "read": 2, "state": "in order"}, {"group": "Tools", "read": "not verified", "state": "not verified"}]

    def test_every_format(self):
        self.assertEqual(cli.render(self.ROWS, "json").count('"group"'), 2)
        lines = cli.render(self.ROWS, "ndjson").split("\n")
        self.assertEqual([json.loads(l)["group"] for l in lines], ["URTC", "Tools"])
        self.assertEqual(cli.render(self.ROWS, "csv").split("\n")[0], "group,read,state")
        self.assertEqual(cli.render(self.ROWS, "plain").split("\n")[0], "URTC\t2\tin order")
        table = cli.render(self.ROWS, "table").split("\n")
        self.assertTrue(table[1].startswith("-----"))
        self.assertEqual(len({len(line.rstrip()) for line in table[2:3]}), 1)
        self.assertEqual(cli.render(self.ROWS, "text").split("\n")[0], "group: URTC, read: 2, state: in order")

    def test_no_rows_is_an_empty_output_and_not_an_error(self):
        for fmt in cli.FORMATS:
            self.assertIsInstance(cli.render([], fmt), str)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        base = Path(self.dir.name)
        (base / "sentinel.json").write_text(json.dumps(SENTINEL), encoding="utf-8")
        (base / "scripts-stats.json").write_text(json.dumps(SCRIPTS), encoding="utf-8")
        self.base = base

    def tearDown(self):
        self.dir.cleanup()

    def test_each_command_prints_and_exits_zero(self):
        for command in cli.COMMANDS:
            code, out, err = run([command, "--format", "json"], self.base)
            self.assertEqual((code, err), (0, ""), command)
            self.assertIsInstance(json.loads(out), list)

    def test_strict_exits_with_three_when_something_is_to_review(self):
        self.assertEqual(run(["supply", "--strict"], self.base)[0], 3)
        self.assertEqual(run(["red", "--strict"], self.base)[0], 3)
        (self.base / "sentinel.json").write_text(json.dumps({"ci": {"red": []}}), encoding="utf-8")
        self.assertEqual(run(["red", "--strict"], self.base)[0], 0)

    def test_a_missing_file_exits_with_four_and_says_which(self):
        (self.base / "sentinel.json").unlink()
        code, out, err = run(["ecosystems"], self.base)
        self.assertEqual((code, out), (4, ""))
        self.assertIn("sentinel.json", err)
        self.assertEqual(run(["supply"], self.base)[0], 0)             # the other file is still read

    def test_a_reading_without_delivery_exits_with_four_and_says_not_verified(self):
        (self.base / "sentinel.json").write_text(json.dumps({"ecosystems": {}}), encoding="utf-8")
        code, _, err = run(["delivery"], self.base)
        self.assertEqual(code, 4)
        self.assertIn("not verified", err)

    def test_a_wrong_command_line_exits_with_two(self):
        self.assertEqual(run(["nothing"], self.base)[0], 2)
        self.assertEqual(run(["red", "--format", "xml"], self.base)[0], 2)

    def test_it_makes_no_request(self):
        text = (ROOT / "scripts" / "sentinel_cli.py").read_text(encoding="utf-8")
        for word in ("urllib", "http.client", "requests", "socket", "subprocess"):
            self.assertNotIn(word, text)

    def test_it_reads_the_real_data_files_of_the_repository(self):
        code, out, _ = run(["ecosystems", "--format", "ndjson"])
        self.assertEqual(code, 0)
        self.assertEqual([json.loads(l)["group"] for l in out.strip().split("\n")], [g[1] for g in ORDER])


if __name__ == "__main__":
    unittest.main()
