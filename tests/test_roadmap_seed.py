# =============================================================================
# JuanenRac profile - tests/test_roadmap_seed.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The pure parts of the Roadmap seeder: the board definitions, the explicit status decisions and the planning of what is created, renamed and updated."""
import importlib
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import bootstrap_ecosystem_project as bootstrap  # noqa: E402
import seed_ecosystem_roadmap as seed  # noqa: E402

BOARDS = ("hydra-umc", "urtc", "armor")


def load(board: str):
    """A fresh copy of both modules configured for one board (configure() changes module state, so no test depends on the order)."""
    importlib.reload(bootstrap)
    importlib.reload(seed)
    seed.configure(board)
    return seed, bootstrap


def card(status, blocked_by="None", title="x", body=""):
    return {"item_id": "i", "draft_id": "d", "title": title, "body": body, "status": status, "blocked_by": blocked_by}


class DefinitionTests(unittest.TestCase):
    def test_every_board_definition_is_consistent(self):
        for board in BOARDS:
            module, boot = load(board)
            problems = module.definition_problems(module.SEED_ITEMS, module.STATUS_UPDATES, module.RENAMES, boot.SELECT_FIELDS)
            self.assertEqual(problems, [], board)

    def test_no_duplicate_titles_on_a_board(self):
        for board in BOARDS:
            module, _ = load(board)
            titles = [item["title"] for item in module.SEED_ITEMS]
            self.assertEqual(len(titles), len(set(titles)), board)

    def test_every_option_an_item_uses_exists_on_its_board(self):
        for board in BOARDS:
            module, boot = load(board)
            options = {field: {name for name, _ in values} for field, values in boot.SELECT_FIELDS.items()}
            for item in module.SEED_ITEMS:
                self.assertIn(item["family"], options["Family"], (board, item["title"]))
                self.assertIn(item["evidence"], options["Evidence"], (board, item["title"]))
                self.assertIn(item["maturity"], options["Maturity"], (board, item["title"]))
                self.assertIn(item["priority"], options["Priority"], (board, item["title"]))
                self.assertIn(item.get("hardware", "None"), options["Hardware dependency"], (board, item["title"]))
                self.assertIn(item.get("status", "Backlog"), options["Status"], (board, item["title"]))

    def test_each_board_has_its_own_option_lists_and_a_none_hardware(self):
        seen = set()
        for board in BOARDS:
            _, boot = load(board)
            self.assertIn("None", {name for name, _ in boot.SELECT_FIELDS["Hardware dependency"]})
            seen.add(tuple(name for name, _ in boot.SELECT_FIELDS["Family"]))
        self.assertEqual(len(seen), 3)

    def test_every_status_decision_names_an_item_and_matches_its_definition(self):
        for board in BOARDS:
            module, _ = load(board)
            by_title = {item["title"]: item for item in module.SEED_ITEMS}
            for title, decision in module.STATUS_UPDATES.items():
                self.assertIn(title, by_title, (board, title))
                self.assertEqual(by_title[title].get("status", "Backlog"), decision["status"], (board, title))
                self.assertEqual(by_title[title].get("blocked_by", "None"), decision.get("blocked_by", "None"), (board, title))

    def test_a_blocked_item_says_what_blocks_it(self):
        for board in BOARDS:
            module, _ = load(board)
            for item in module.SEED_ITEMS:
                if item.get("status") == "Blocked":
                    self.assertNotIn(item.get("blocked_by", "None"), ("", "None"), (board, item["title"]))

    def test_nothing_physical_is_done_on_software_evidence(self):
        software = {"Documentation", "Local test", "Simulator", "Host harness", "Browser"}
        for board in BOARDS:
            module, _ = load(board)
            for item in module.SEED_ITEMS:
                if item.get("status") == "Done" and item.get("hardware", "None") != "None":
                    self.assertNotIn(item["evidence"], software, (board, item["title"]))

    def test_every_renamed_card_has_a_new_title_on_the_board_and_no_old_one(self):
        for board in BOARDS:
            module, _ = load(board)
            titles = {item["title"] for item in module.SEED_ITEMS}
            for old, new in module.RENAMES.items():
                self.assertNotIn(old, titles)
                self.assertIn(new, titles)

    def test_public_text_has_no_dates_audit_ids_or_internal_names(self):
        forbidden = [re.compile(pattern) for pattern in (r"\b20\d\d-\d\d-\d\d\b", r"\b[A-Z]{3,5}-(BUG|MEJ|DOC|SEG|REL|BAS|ARQ|TST|OPS|IDEA)-\d+", r"SONNET", r"(?i)claude", r"(?i)\bAI agent\b")]
        for board in BOARDS:
            module, _ = load(board)
            texts = []
            for item in module.SEED_ITEMS:
                texts.extend(str(value) for value in item.values())
            for decision in module.STATUS_UPDATES.values():
                texts.append(decision.get("blocked_by", ""))
            for text in texts:
                for pattern in forbidden:
                    self.assertIsNone(pattern.search(text), (board, text[:60]))

    def test_the_boards_cover_the_numbers_the_owner_asked_for(self):
        module, _ = load("armor")
        titles = {item["title"] for item in module.SEED_ITEMS}
        self.assertIn("Check the node firmwares on boards beyond the one RADAR board", titles)
        self.assertIn("Pylontech battery: counters, event log and profiles per model", titles)
        self.assertIn("Signed component updates from Studio, with rollback", titles)
        self.assertIn("HMI: pin the server certificate instead of skipping TLS verification", titles)
        module, _ = load("urtc")
        titles = {item["title"] for item in module.SEED_ITEMS}
        self.assertIn("Several tool heads on one CAN bus, behind a switch", titles)
        self.assertIn("Adopt URTC-COMMON in every URTC repository", titles)


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.module, self.boot = load("hydra-umc")

    def test_planning_creates_only_what_has_no_card_under_either_title(self):
        items = [{"title": "A"}, {"title": "B"}, {"title": "New name"}, {"title": "C"}]
        state = {"A": card("Done"), "Old name": card("Blocked", "x")}
        missing = self.module.plan_creation(state, items, {"Old name": "New name"})
        self.assertEqual([item["title"] for item in missing], ["B", "C"])

    def test_a_rename_is_planned_only_while_the_old_card_exists_and_the_new_title_is_free(self):
        renames = {"Old": "New", "Gone": "Other"}
        self.assertEqual(self.module.plan_renames({"Old": card("Done")}, renames), [("Old", "New")])
        self.assertEqual(self.module.plan_renames({"Old": card("Done"), "New": card("Done")}, renames), [])
        self.assertEqual(self.module.plan_renames({}, renames), [])

    def test_status_updates_touch_only_listed_cards_that_differ(self):
        state = {"A": card("Backlog"), "B": card("Done"), "C": card("Backlog"), "Unlisted": card("In progress")}
        updates = {"A": {"status": "Done", "blocked_by": "None"}, "B": {"status": "Done", "blocked_by": "None"}, "Missing": {"status": "Done", "blocked_by": "None"}}
        plan = self.module.plan_status_updates(state, updates, {})
        self.assertEqual([change["title"] for change in plan], ["A"])
        self.assertEqual(plan[0]["from"], "Backlog")
        self.assertEqual(plan[0]["to"], "Done")

    def test_a_different_blocker_is_an_update_even_with_the_same_status(self):
        state = {"A": card("Blocked", "old reason")}
        plan = self.module.plan_status_updates(state, {"A": {"status": "Blocked", "blocked_by": "new reason"}}, {})
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]["blocked_by"], "new reason")
        self.assertEqual(self.module.plan_status_updates(state, {"A": {"status": "Blocked", "blocked_by": "old reason"}}, {}), [])

    def test_an_empty_status_is_reported_and_a_renamed_card_is_found_under_its_old_title(self):
        state = {"Old": card(None)}
        plan = self.module.plan_status_updates(state, {"New": {"status": "Blocked", "blocked_by": "why"}}, {"Old": "New"})
        self.assertEqual(plan[0]["from"], "(empty)")

    def test_planning_is_idempotent_once_applied(self):
        updates = {"A": {"status": "Done", "blocked_by": "None"}}
        state = {"A": card("Done")}
        self.assertEqual(self.module.plan_status_updates(state, updates, {}), [])
        self.assertEqual(self.module.plan_creation(state, [{"title": "A"}], {}), [])

    def test_the_definition_check_reports_each_kind_of_mistake(self):
        select = self.boot.SELECT_FIELDS
        good = {"title": "T", "family": "Applications", "maturity": "Functional", "evidence": "Local test", "priority": "Normal", "status": "Backlog", "hardware": "None"}
        bad_family = dict(good, title="U", family="Nowhere")
        blocked = dict(good, title="V", status="Blocked")
        physical_done = dict(good, title="W", status="Done", hardware="CM5")
        problems = self.module.definition_problems([good, good, bad_family, blocked, physical_done],
                                                   {"Ghost": {"status": "Done", "blocked_by": "None"}}, {"V": "T"}, select)
        text = "\n".join(problems)
        self.assertIn("duplicate title: T", text)
        self.assertIn("not an option of Family", text)
        self.assertIn("Blocked without a blocker", text)
        self.assertIn("Done for hardware work on software evidence only", text)
        self.assertIn("unknown item: Ghost", text)
        self.assertIn("renamed from a title that is still an item: V", text)

    def test_apply_status_updates_gives_a_new_board_the_same_decision(self):
        items = [{"title": "A", "status": "Backlog", "blocked_by": "None"}, {"title": "B", "status": "Backlog"}]
        result = self.module.apply_status_updates(items, {"A": {"status": "Blocked", "blocked_by": "why"}})
        self.assertEqual(result[0]["status"], "Blocked")
        self.assertEqual(result[0]["blocked_by"], "why")
        self.assertEqual(result[1], items[1])

    def test_parse_state_reads_status_blocker_and_draft_ids(self):
        nodes = [
            {"id": "1", "content": {"id": "d1", "title": "A", "body": "text"}, "status": {"name": "Done"}, "blocked": {"text": "None"}},
            {"id": "2", "content": {"id": "d2", "title": "B", "body": None}, "status": None, "blocked": None},
            {"id": "3", "content": None},
        ]
        state = self.module.parse_state(nodes)
        self.assertEqual(sorted(state), ["A", "B"])
        self.assertEqual(state["A"]["draft_id"], "d1")
        self.assertEqual(state["A"]["status"], "Done")
        self.assertIsNone(state["B"]["status"])
        self.assertEqual(state["B"]["blocked_by"], "None")
        self.assertEqual(state["B"]["body"], "")

    def test_the_body_of_hardware_work_never_claims_validation(self):
        text = self.module.item_body({"objective": "o", "acceptance": "a", "hardware": "MCU"})
        self.assertIn("This work needs: MCU", text)
        self.assertIn("without a recorded bench", text)
        text = self.module.item_body({"objective": "o", "acceptance": "a"})
        self.assertIn("software-only", text)


class WorkflowTests(unittest.TestCase):
    def test_the_workflow_offers_the_reconcile_input_and_passes_the_flag(self):
        text = (ROOT / ".github" / "workflows" / "seed-ecosystem-roadmap.yml").read_text(encoding="utf-8")
        self.assertIn("reconcile_status:", text)
        self.assertIn("--reconcile-status", text)
        self.assertIn("tools/roadmap_defs.py", text)


if __name__ == "__main__":
    unittest.main()
