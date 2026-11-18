# Sentinel tab

The Sentinel tab of the status dashboard is a public-safe watch over the repositories of the four ecosystems. It is read once, in the job that builds the
page, with the read-only token of the workflow, and it is decided by fixed rules (no AI). Settings live in the `sentinel` block of
`dashboard-config.json`; every section can be switched off in `sentinel.sections`.

## One definition of a red build

`scripts/ci_rules.py` is the single place that says what a red build is. The Sentinel tab, the Builds tab and the CI watch issue all use it.

| Conclusion of the last finished run of a workflow on the default branch | Counts as |
|---|---|
| `failure`, `timed_out`, `startup_failure`, `action_required` | red |
| `success` | green |
| `cancelled`, `skipped`, `neutral`, `stale`, none | passed over: the run before it decides |

Runs that GitHub generates for dependency updates (event `dynamic`, no workflow file of the repository) never decide the state of a workflow.

## Table by ecosystem

One row per ecosystem: repositories, repositories with a red workflow, repositories ready for a new version and repositories whose manifest declares a
version that was never published. Repositories that could not be read are counted in the first column only.

## Version raised, not published

A repository is listed when the version declared by its manifest is newer than the tag of its latest release. A repository without any release, or with
a version that is not numeric, is not listed. The prefixes of `sentinel.skip_candidate_prefixes` are skipped here too, and the line also appears in the
short report of the tab.

## Recent changes

A short feed kept in `data/sentinel.json`: a workflow that turned red, a workflow that is green again and a release that appeared, newest first. Each
event is only created by comparing two readings, so nothing is invented for the first run, and a repository that could not be read cannot "recover". The
length is `sentinel.events_max` (5 to 200, default 30).

## Releases ready: the threshold

A repository is a release candidate when `[Unreleased]` holds at least `candidate_min_entries` entries (5, the same threshold as the panel A5 of the local monitor) and its last
release is older than `candidate_days`. The prefixes of `skip_candidate_prefixes` are never candidates.

## Health of the refresh

The file carries a `health` block of numbers (`gap_minutes`, `age_minutes`, `build_queue_seconds`, in steps) and the tab warns when the reading is older than
`behind_minutes`; see [DASHBOARD_UPDATES.md](DASHBOARD_UPDATES.md) for how the panel is kept current.

## Supply chain and delivery

Two cards of the tab take the ideas of the supply chain and delivery sentinels of the local monitor (see below) and keep to what is safe to publish: counts by ecosystem
for the five groups (HYDRA-UMC, URTC, A.R.M.O.R., EH3D and Tools), never a line, a value or a person. A group with nothing read is shown as not verified, never as in order.

### Supply chain

Read from the same daily copy of the repositories as the Scripts tab (no extra request). One row per group, with the repositories read and, summed over their workflows:

| Column | What it counts |
|---|---|
| Not fixed to a commit | the `uses:` of an action whose version is a tag or a branch instead of a full commit |
| Follow a branch | the `uses:` that follow a branch such as `main` |
| Permissions | the findings of the linter rule that looks for a workflow without a `permissions:` block or with `write-all` |
| `pull_request_target` | the findings of the linter rule that looks for `pull_request_target` with a checkout of the pull request |

The state is **In order** only when all four are zero and **To review** otherwise. `sections.supply` switches the card off.

### Delivery

Read in the same GraphQL call as the rest of the tab (the latest release, its description, the newest version tag and the CHANGELOG), so it costs no extra request. The description and
the CHANGELOG are reduced to a yes or no and a version number on the spot; their text is never kept.

| Column | What it counts |
|---|---|
| Tag without release | a version tag newer than the latest release |
| Release without notes | the latest release has an empty description |
| CHANGELOG differs | the newest released section of the CHANGELOG is not the version of the latest release |
| Version raised, not published | the manifest declares a version newer than the latest release (the card above) |

A repository without a published release, or whose fact could not be read, never raises a signal. A reading saved before these checks existed has no delivery block, and the card
then says so instead of showing zeros. `sections.delivery` switches the card off.

## The local Actions monitor and this panel

The local monitor (`TOOLS-GITHUB-ACTIONS-MONITOR`, of the Tools group) and this tab answer the same question with the same rule of red (see
[CI_RED_CONTRACT.md](CI_RED_CONTRACT.md)); they differ in where they run. The monitor reads from the machine of its owner; its complete edition has five sentinels that never write to
GitHub (CI with its checks A1 to A13, Collab, Security, Supply chain and Delivery) and its lite edition has none. The dashboard reads in GitHub Actions with the read-only token of the
workflow and publishes only what is safe.

| Sentinel of the monitor | What it checks | In this tab |
|---|---|---|
| CI (A1, A2, A12, A13) | builds stuck or queued, red CI by the single rule, durations and flaky workflows, the workflow linter | red workflows, Builds tab, Scripts tab |
| CI (A5) | releases: candidate (5 or more entries under `[Unreleased]`), green release build, waiting for a signature | releases ready, signatures |
| CI (A6, A10) | hygiene (ruleset, labels, required files, pinned actions) and the surface of Actions | hygiene, partly the Scripts tab |
| CI (A7) | usage: Actions minutes, budgets, allowance left | computing |
| Collab | issues and pull requests that need a person | never shown: it would publish titles and people |
| Security | Dependabot, code scanning and secret scanning alerts, branch protection | never shown: nothing about security alerts is published, not even a count |
| Supply chain | actions not pinned to a commit or following a branch, wide or missing permissions, `pull_request_target` | Supply chain card |
| Delivery | unreleased entries, tags without a release, releases without notes, versions that disagree, pins behind a shared contract | Delivery card, version raised and not published, shared contract pins |

The monitor also reads this panel (`data/sentinel.json` of the profile repository) as a base line that spends no allowance: it ignores the file when it is more than two hours old and
says so. That is why the file is refreshed every half hour and why this tab warns when it is behind. A used-up allowance is reported as one notice, not one error per repository.

### Connecting an AI tool to the monitor

Both editions share the same five channels: a brief of what to do now, a feed of alerts, the state as data (`/api/ai/state`), a stream of events (complete edition) and MCP
tools, plus a gate script (`ai-hook`) that adds the brief to the session of the AI. Everything is read only unless an action is allowed. The guide
[AI_CONNECTION](https://github.com/JuanenRac/TOOLS-GITHUB-ACTIONS-MONITOR/blob/main/monitor/docs/AI_CONNECTION.md) explains each step.

## Reading it from a terminal

`scripts/sentinel_cli.py` prints the same figures from the data files the page is built from (`data/sentinel.json` and `data/scripts-stats.json`), with no request to GitHub:

```
python scripts/sentinel_cli.py ecosystems --format table
python scripts/sentinel_cli.py supply --format csv
python scripts/sentinel_cli.py delivery --format json --strict
```

| Command | What it prints |
|---|---|
| `ecosystems` | repositories, red workflows, releases ready and versions raised without a release for each of the five groups |
| `supply` | the Supply chain card |
| `delivery` | the Delivery card |
| `red` | the red workflows (repository, workflow file, failures in a row, since when) |
| `ready` | the repositories ready for a version |

`--format` is `text` (a sentence per row, the default), `table`, `plain` (tab separated, no header, for scripts), `json`, `ndjson` or `csv`. A group with nothing read says `not verified`, never zero.
Exit codes: `0` all read, `3` with `--strict` when something is to review, `4` when a data file is missing or the reading has no delivery data yet, `2` for a wrong command line.

## What is still never shown

Security alerts (not even a count), titles of pull requests and issues, people, branches and texts written by outsiders. The document is rebuilt from a
whitelist on every write, so none of them can get through whatever the input holds.

## Settings

| Key | Default | Meaning |
|---|---|---|
| `events_max` | 30 | length of the feed of changes |
| `sections.ecosystems` | true | table by ecosystem |
| `sections.events` | true | feed of changes |
| `sections.supply` | true | supply chain card |
| `sections.delivery` | true | delivery card |
| `sections.releases` | true | releases ready and versions raised without a release |
| `candidate_min_entries` | 5 | entries under `[Unreleased]` that make a repository a release candidate |
| `stale_hours` | 1 | how long an unchanged reading keeps its moment (so a quiet panel is written at most once an hour) |
| `behind_minutes` | 120 | age of the reading from which the tab says the panel is behind |
