# =============================================================================
# JuanenRac profile - tests/test_workflow_lint.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE.md
# =============================================================================
"""The linter of the workflows with the three levels of the local Actions monitor (info, warn, error), what the Scripts block keeps of it and how the tab draws it."""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import code_stats  # noqa: E402
import dashboard_code_texts as code_texts  # noqa: E402
import dashboard_scripts as ds  # noqa: E402
import dashboard_scripts_ui as ui  # noqa: E402
import scripts_stats as ss  # noqa: E402
import workflow_lint as wl  # noqa: E402

SHA = "a" * 40
CLEAN = f"""name: Clean
on: push
permissions: {{}}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@{SHA} # v6
      - run: echo hello
"""


def levels(text, config=None):
    return [(f["rule"], f["level"]) for f in wl.lint_text(text, config)]


class RuleTests(unittest.TestCase):
    def test_a_clean_workflow_has_no_finding(self):
        self.assertEqual(wl.lint_text(CLEAN), [])

    def test_an_action_pinned_to_a_tag_or_a_branch_is_a_warning(self):
        text = CLEAN + "      - uses: actions/setup-python@v5\n      - uses: some/tool@main\n      - uses: ./local\n      - uses: docker://alpine:3\n"
        self.assertEqual(levels(text), [("unpinned_uses", "warn"), ("unpinned_uses", "warn")])

    def test_no_permissions_block_is_a_warning_and_write_all_too(self):
        self.assertEqual(levels("on: push\njobs:\n  a:\n    steps:\n      - run: x\n"), [("permissions", "warn")])
        self.assertEqual(levels("permissions: write-all\non: push\njobs:\n  a:\n    steps: []\n"), [("permissions", "warn")])
        self.assertEqual(levels("on: push\njobs:\n  a:\n    permissions:\n      contents: read\n    steps: []\n"), [])

    def test_a_known_token_format_is_an_error_a_filler_only_information(self):
        token = "ghp_" + "A1b2C3d4" * 5
        self.assertEqual(levels(CLEAN + f"      - run: curl -H 'x-token: {token}' https://example.invalid\n"), [("secrets_in_clear", "error")])
        self.assertEqual(levels(CLEAN + "    env:\n      API_TOKEN: placeholder-value\n"), [("secrets_in_clear", "info")])
        self.assertEqual(levels(CLEAN + "    env:\n      MY_PASSWORD: Zx9fWq3mT7rLpV\n"), [("secrets_in_clear", "warn")])
        self.assertEqual(levels(CLEAN + "    env:\n      API_TOKEN: ${{ secrets.TOKEN }}\n"), [])

    def test_a_text_of_an_outsider_in_a_script_is_a_warning(self):
        text = CLEAN + "      - run: |\n          echo ${{ github.event.issue.title }}\n"
        self.assertIn(("injection", "warn"), levels(text))

    def test_pull_request_target_that_checks_out_the_pull_request_is_an_error(self):
        text = (f"on:\n  pull_request_target:\npermissions: {{}}\njobs:\n  a:\n    steps:\n      - uses: actions/checkout@{SHA}\n        with:\n"
                "          ref: ${{ github.event.pull_request.head.sha }}\n")
        self.assertEqual(levels(text), [("pr_target", "error")])

    def test_a_comment_silences_a_rule_on_its_line_or_the_next_one_and_the_monitor_form_is_understood(self):
        base = CLEAN + "      - uses: some/tool@main\n"
        self.assertEqual(levels(base.replace("some/tool@main", "some/tool@main # lint: ignore unpinned_uses because it is ours")), [])
        self.assertEqual(levels(base.replace("      - uses: some", "      # monitor-lint: ignore unpinned_uses\n      - uses: some")), [])
        self.assertEqual(levels(base.replace("      - uses: some", "      # lint: ignore all\n      - uses: some")), [])
        self.assertEqual(levels(base.replace("      - uses: some", "      # lint: ignore injection\n      - uses: some")), [("unpinned_uses", "warn")])

    def test_a_finding_keeps_no_value_no_name_and_no_text(self):
        token = "ghp_" + "Z9y8X7w6" * 5
        found = wl.lint_text(CLEAN + f"    env:\n      GH_TOKEN: {token}\n")
        self.assertEqual(set(found[0]), {"line", "rule", "level"})
        self.assertNotIn(token, json.dumps(found))

    def test_a_line_it_cannot_understand_is_skipped(self):
        self.assertEqual(wl.lint_text("\x00\x01 not yaml at all {{{\n:::\n"), [])
        self.assertEqual(wl.lint_text(""), [])


class ConfigurationTests(unittest.TestCase):
    def test_the_shipped_configuration_is_valid_and_has_the_defaults(self):
        raw = json.loads((ROOT / "code-stats-config.json").read_text(encoding="utf-8"))
        config, problems = wl.check_config(raw["lint"])
        self.assertEqual(problems, [])
        self.assertEqual({rule: item["level"] for rule, item in config["rules"].items()}, wl.DEFAULT_LEVEL)
        self.assertEqual(code_stats.check_config(raw), [])

    def test_a_rule_can_be_switched_off_or_given_another_level(self):
        config, problems = wl.check_config({"rules": {"unpinned_uses": {"enabled": False}, "permissions": {"level": "error"}, "injection": {"level": "bad"}}})
        self.assertEqual(problems, [])
        text = "on: push\njobs:\n  a:\n    steps:\n      - uses: some/tool@main\n"
        self.assertEqual(levels(text, config), [("permissions", "error")])
        self.assertEqual(config["rules"]["injection"]["level"], "error")     # the monitor says "bad" for the highest level

    def test_wrong_values_are_named_and_keep_the_default(self):
        config, problems = wl.check_config({"enabled": "no", "rules": {"nope": {}, "permissions": {"level": "loud", "enabled": 3}}})
        self.assertEqual(len(problems), 4)
        self.assertEqual(config["rules"]["permissions"], {"enabled": True, "level": "warn"})
        self.assertEqual(wl.check_config([])[1], ["lint: not an object"])
        self.assertEqual(wl.check_config(None)[1], [])


class ExemptionTests(unittest.TestCase):
    def test_an_exemption_names_repository_file_and_rule(self):
        patterns = ["URTC-*:codeql.yml:unpinned_uses", "ARMOR-SERVER:*:permissions"]
        self.assertTrue(wl.exempt("URTC-DOCS", "codeql.yml", "unpinned_uses", patterns))
        self.assertTrue(wl.exempt("ARMOR-SERVER", "ci.yml", "permissions", patterns))
        self.assertFalse(wl.exempt("URTC-DOCS", "ci.yml", "unpinned_uses", patterns))
        self.assertFalse(wl.exempt("URTC-DOCS", "codeql.yml", "permissions", patterns))
        self.assertFalse(wl.exempt("X", "a.yml", "injection", []))

    def test_the_configuration_checks_the_form_of_each_exemption(self):
        config, problems = wl.check_config({"ignore": ["R:f.yml:permissions", "nope", 3]})
        self.assertEqual(config["ignore"], ["R:f.yml:permissions"])
        self.assertEqual(len(problems), 2)
        self.assertEqual(wl.check_config({"ignore": "x"})[1], ["lint.ignore: not a list"])

    def test_an_exempt_finding_is_not_counted_in_the_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "a.yml").write_text("on: push\njobs:\n  a:\n    steps:\n      - uses: some/tool@main\n", encoding="utf-8")
            config, _ = wl.check_config({"ignore": ["MyRepo:a.yml:unpinned_uses"]})
            self.assertEqual(ss.summarize(Path(tmp), config, "MyRepo")["lint"]["rules"], {"permissions": [0, 1, 0]})
            self.assertEqual(ss.summarize(Path(tmp), config, "Other")["lint"]["warn"], 2)


class TallyAndBlockTests(unittest.TestCase):
    def test_the_tally_counts_by_level_and_rule(self):
        found = [{"line": 1, "rule": "permissions", "level": "warn"}, {"line": 2, "rule": "permissions", "level": "warn"}, {"line": 3, "rule": "secrets_in_clear", "level": "error"}]
        self.assertEqual(wl.tally(found), {"info": 0, "warn": 2, "error": 1, "rules": {"permissions": [0, 2, 0], "secrets_in_clear": [0, 0, 1]}})

    def test_a_repository_is_summarized_with_its_lint_and_the_switch_turns_it_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "a.yml").write_text("on: push\njobs:\n  a:\n    steps:\n      - uses: some/tool@main\n", encoding="utf-8")
            summary = ss.summarize(Path(tmp))
            self.assertEqual(summary["lint"]["warn"], 2)
            self.assertEqual(summary["lint"]["rules"], {"unpinned_uses": [0, 1, 0], "permissions": [0, 1, 0]})
            off, _ = wl.check_config({"enabled": False})
            self.assertNotIn("lint", ss.summarize(Path(tmp), off))
        with tempfile.TemporaryDirectory() as empty:
            self.assertNotIn("lint", ss.summarize(Path(empty)))

    def test_the_block_of_the_page_keeps_only_counts_of_known_rules(self):
        doc = {"schema": 1, "day": "2001-12-21", "owner": "o", "ecosystems": [{"key": "armor", "label": "A"}], "types": ["tools"],
               "repos": {"R": {"eco": "armor", "type": "tools", "state": "ok", "scripts": {
                   "wf": [], "acts": {}, "sc": {}, "lint": {"info": 1, "warn": 2, "error": 3, "rules": {"permissions": [0, 2, 0], "made_up": [9, 9, 9], "injection": [1]}, "secret": "value"}}}}}
        block = ds.build(doc, "2001-12-21")["repos"]["R"]["scripts"]["lint"]
        self.assertEqual(block, {"info": 1, "warn": 2, "error": 3, "rules": {"permissions": [0, 2, 0]}})

    def test_a_repository_without_lint_stays_without_it(self):
        doc = {"schema": 1, "day": "2001-12-21", "owner": "o", "ecosystems": [{"key": "armor", "label": "A"}], "types": ["tools"],
               "repos": {"R": {"eco": "armor", "type": "tools", "state": "ok", "scripts": {"wf": [], "acts": {}, "sc": {}}}}}
        self.assertNotIn("lint", ds.build(doc)["repos"]["R"]["scripts"])


class TabTests(unittest.TestCase):
    def test_the_tab_has_the_lint_card_and_draws_it(self):
        html = ui.panel_html()
        for part in ('id="sc-lint-chart"', 'id="sc-lintrule-chart"', 'id="sc-lint-none"'):
            self.assertIn(part, html)
        self.assertIn("function scRenderLint", ui.JS)
        self.assertIn("scRenderLint(dict)", ui.JS)

    def test_every_text_of_the_card_exists_in_the_eight_languages(self):
        keys = ["sc_lint_title", "sc_lint_hint", "sc_lint_none", "sc_lint_by_rule", "sc_aria_lint", "sc_aria_lintrule", "sc_tip_lint", "sc_col_lerr", "sc_col_lwarn",
                "sc_k_lint_err", "sc_k_lint_warn"] + [f"sc_lvl_{level}" for level in wl.LEVELS] + [f"sc_rule_{rule}" for rule in wl.RULES]
        for code in ("en", "es", "de", "fr", "it", "ja", "zh", "pt"):
            for key in keys:
                self.assertTrue(code_texts.TEXTS[code].get(key), f"{code} {key}")
        for key in ("sc_lint_title", "sc_lint_hint", "sc_lint_none", "sc_lint_by_rule", "sc_aria_lint", "sc_aria_lintrule"):
            for code in ("es", "de", "fr", "it", "ja", "zh", "pt"):
                self.assertNotEqual(code_texts.TEXTS[code][key], code_texts.TEXTS["en"][key], f"{code} {key}")

    def test_the_js_names_the_same_rules_and_levels_as_the_linter(self):
        for rule in wl.RULES:
            self.assertIn(f'"{rule}"', ui.JS)
        for level in wl.LEVELS:
            self.assertIn(f'"{level}"', ui.JS)


def monitor_linter():
    candidates = [os.environ.get("MONITOR_LINT", ""), str(ROOT.parent / "TOOLS-GITHUB-ACTIONS-MONITOR" / "monitor" / "lint_workflows.py")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            sys.path.insert(0, str(Path(candidate).parent))
            spec = importlib.util.spec_from_file_location("monitor_lint_workflows", candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None


class MonitorParityTests(unittest.TestCase):
    """The same findings, at the same level, as the linter of the local monitor (when a copy of it is next to this repository)."""

    SAMPLES = [
        CLEAN,
        CLEAN + "      - uses: actions/setup-python@v5\n      - uses: some/tool@main\n",
        "on: push\njobs:\n  a:\n    steps:\n      - run: x\n",
        "permissions: write-all\non: push\njobs:\n  a:\n    steps: []\n",
        CLEAN + "    env:\n      API_TOKEN: placeholder-value\n      MY_PASSWORD: Zx9fWq3mT7rLpV\n      OTHER_SECRET: xK3mQ9vL2pR8tY5nB7cZ4wD6\n",
        CLEAN + "      - run: |\n          echo ${{ github.event.issue.title }}\n          echo ${{ github.head_ref }}\n",
        f"on:\n  pull_request_target:\npermissions: {{}}\njobs:\n  a:\n    steps:\n      - uses: actions/checkout@{SHA}\n        with:\n          ref: ${{{{ github.event.pull_request.head.sha }}}}\n",
        CLEAN + "      - uses: some/tool@main # monitor-lint: ignore unpinned_uses because it is ours\n",
    ]

    def test_the_same_findings_and_levels(self):
        monitor = monitor_linter()
        if monitor is None:
            self.skipTest("no copy of the monitor next to this repository")
        names = {"bad": "error"}
        for number, text in enumerate(self.SAMPLES):
            with self.subTest(sample=number):
                theirs = sorted((f["line"], f["rule"], names.get(f["severity"], f["severity"])) for f in monitor.lint_text(text, "w.yml"))
                ours = sorted((f["line"], f["rule"], f["level"]) for f in wl.lint_text(text))
                self.assertEqual(ours, theirs)

    def test_the_same_rules(self):
        monitor = monitor_linter()
        if monitor is None:
            self.skipTest("no copy of the monitor next to this repository")
        self.assertEqual(tuple(monitor.RULES), wl.RULES)
        self.assertEqual({r: names for r, names in monitor.DEFAULT_SEVERITY.items()}, {r: {"error": "bad"}.get(l, l) for r, l in wl.DEFAULT_LEVEL.items()})


if __name__ == "__main__":
    unittest.main()
