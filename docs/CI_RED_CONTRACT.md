# The rule of red and the `ci_red.json` contract

## One rule

A workflow is **red** when the **last completed run of its file on the default branch** failed. [`scripts/ci_rules.py`](../scripts/ci_rules.py) is the single place that
says so, and the Sentinel tab, the Builds tab and the CI watch issue all use it.

| Conclusion of a completed run | Effect |
|---|---|
| `failure`, `timed_out`, `startup_failure`, `action_required` | red |
| `success` | green |
| `cancelled`, `skipped`, `neutral`, `stale`, or no conclusion yet | says nothing: the run before it decides, so an older failure is not hidden |
| a run of another branch | not looked at |
| a `dynamic` run (the internal jobs of dependency updates, with no workflow file of the repository) | never a build of the repository |

The streak of a red workflow is the number of failures in a row up to its last run, passing over the runs that say nothing.

`ci_rules.red_workflows(runs, default_branch)` is that rule written once. [`tests/fixtures/red_rule_cases.json`](../tests/fixtures/red_rule_cases.json) holds the
shared cases; `tests/test_red_rule_parity.py` runs them through the rule itself, the Sentinel tab and the CI watch issue, and, when a copy of the local Actions monitor
sits next to this repository (or `MONITOR_REDRULE` points at its `redrule.py`), through the monitor too. The file can be copied as it is into any other tool that
wants to apply the same rule.

## The snapshot of the local monitor

The local Actions monitor can write a small `ci_red.json` (schema 2) with the workflows in red per repository. **The dashboard does not read it**: the snapshot lives on
the machine of whoever runs the monitor and is never published, while the dashboard is built in GitHub Actions and works out the same facts by itself. What both sides
share is the rule above and the shape of the document, so that either can be checked against the other without being coupled to it.

| Field | Meaning |
|---|---|
| `schema` | `2`. Fields are only ever added, so read with `.get()` and ignore what you do not know |
| `generated`, `tool_version` | when and by which version of the monitor |
| `complete` | `false` while the monitor is still loading its first reading |
| `red_repos` | repositories with at least one red workflow |
| `repos.<name>.red[]` | `workflow`, `conclusion`, `since`, `streak`, `url` of each red workflow |
| `repos.<name>.ecosystem` | `armor`, `urtc`, `hydra`, `eh3d` or `other` |

`ci_rules.ci_red_problems(document)` returns what is wrong with a document of this contract (an empty list when it conforms); `tests/fixtures/ci_red_sample.json` is the
sample both sides test.
