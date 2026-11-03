# =============================================================================
# JuanenRac profile - tests/test_workflow_permissions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The workflows of the profile: no permission by default, write only where it is needed, third-party actions pinned to a full commit.

No YAML library is needed: the workflows have a fixed, simple layout, and the checks read it as text.
"""
import re
import unittest
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
FILES = sorted(WORKFLOWS.glob("*.yml"))

# The only jobs that may hold a write permission, and which. Anything else must be read-only.
WRITERS = {
    ("build-dashboard.yml", "publish"): {"contents": "write"},
    ("ecosystem-ci-watch.yml", "watch"): {"contents": "read", "issues": "write"},
    ("ecosystem-health-matrix.yml", "matrix"): {"contents": "read", "issues": "write"},
    ("ecosystem-link-check.yml", "links"): {"contents": "read", "issues": "write"},
}


def jobs_of(text: str) -> dict:
    """{job id: the text of the job}."""
    body = text.split("\njobs:\n", 1)[1]
    parts = re.split(r"(?m)^  ([A-Za-z][\w-]*):[ \t]*\n", body)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def permissions_of(job_text: str):
    """None when the job has no permissions key; {} for `permissions: {}`; otherwise {scope: level}."""
    flat = re.search(r"(?m)^    permissions:[ \t]*(\{\})?[ \t]*\n", job_text)
    if not flat:
        return None
    if flat.group(1):
        return {}
    block = re.match(r"(?:      [a-z-]+: (?:read|write|none)\n)+", job_text[flat.end():])
    return dict(line.strip().split(": ") for line in block.group(0).splitlines()) if block else {}


class EveryWorkflowTests(unittest.TestCase):
    def test_there_are_workflows(self):
        self.assertGreaterEqual(len(FILES), 10)

    def test_no_permission_by_default(self):
        for path in FILES:
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^permissions: \{\}[ \t]*$", f"{path.name}: the workflow must start with `permissions: {{}}`")

    def test_every_job_states_its_own_permissions(self):
        for path in FILES:
            for job, body in jobs_of(path.read_text(encoding="utf-8")).items():
                self.assertIsNotNone(permissions_of(body), f"{path.name}/{job} has no permissions")

    def test_write_exists_only_in_the_expected_jobs(self):
        for path in FILES:
            for job, body in jobs_of(path.read_text(encoding="utf-8")).items():
                perms = permissions_of(body) or {}
                expected = WRITERS.get((path.name, job))
                if expected is None:
                    self.assertNotIn("write", perms.values(), f"{path.name}/{job} writes but is not allowed to")
                else:
                    self.assertEqual(perms, expected, f"{path.name}/{job}")

    def test_a_job_that_checks_out_can_read_the_contents(self):
        for path in FILES:
            for job, body in jobs_of(path.read_text(encoding="utf-8")).items():
                if "actions/checkout" in body:
                    self.assertIn((permissions_of(body) or {}).get("contents"), ("read", "write"), f"{path.name}/{job}")

    def test_every_action_is_pinned_to_a_full_commit(self):
        for path in FILES:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = re.match(r"\s*(?:- )?uses:\s*(\S+)", line)
                if match and not match.group(1).startswith("./"):
                    self.assertRegex(match.group(1), r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$", f"{path.name}:{number} is not pinned to a full commit")

    def test_the_pin_says_which_release_it_is(self):
        for path in FILES:
            for line in path.read_text(encoding="utf-8").splitlines():
                if re.match(r"\s*(?:- )?uses:\s*\S+@[0-9a-f]{40}", line):
                    self.assertRegex(line, r"# v\d", line)


class BuildDashboardTests(unittest.TestCase):
    def setUp(self):
        self.text = (WORKFLOWS / "build-dashboard.yml").read_text(encoding="utf-8")
        self.jobs = jobs_of(self.text)

    def triggers(self) -> str:
        return self.text.split("\npermissions:", 1)[0]

    def test_it_runs_on_pull_requests_and_still_on_main_schedule_and_dispatch(self):
        triggers = self.triggers()
        for trigger in ("pull_request:", "push:", "schedule:", "workflow_dispatch:", "repository_dispatch:"):
            self.assertIn(f"\n  {trigger}", triggers)

    def test_two_jobs_and_only_the_publishing_one_writes(self):
        self.assertEqual(list(self.jobs), ["build", "publish"])
        self.assertEqual(permissions_of(self.jobs["build"]), {"contents": "read"})
        self.assertEqual(permissions_of(self.jobs["publish"]), {"contents": "write"})

    def test_the_publishing_job_never_runs_on_a_pull_request(self):
        self.assertRegex(self.jobs["publish"], r"(?m)^    if: github\.event_name != 'pull_request'$")
        self.assertRegex(self.jobs["publish"], r"(?m)^    needs: build$")

    def test_nothing_that_writes_to_the_repository_is_outside_the_publishing_job(self):
        build = self.jobs["build"]
        for forbidden in ("git push", "git commit", "git add", "contents: write"):
            self.assertNotIn(forbidden, build)
        self.assertIn("git push origin HEAD:main", self.jobs["publish"])

    def test_the_build_job_hands_over_files_only_when_it_is_not_a_pull_request(self):
        build = self.jobs["build"]
        self.assertEqual(build.count("if: github.event_name != 'pull_request'"), 2)

    def test_a_pull_request_has_a_concurrency_group_of_its_own(self):
        self.assertIn("ecosystem-dashboard-pr-", self.text)

    def test_the_integrity_test_runs_in_the_build(self):
        self.assertIn("python scripts/ecosystem_integrity_test.py", self.jobs["build"])

    def test_the_secret_token_is_not_used(self):
        self.assertNotIn("secrets.", re.sub(r"secrets\.GITHUB_TOKEN", "", self.text))


if __name__ == "__main__":
    unittest.main()
