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

## The local Actions monitor and this panel

The local monitor (`TOOLS-GITHUB-ACTIONS-MONITOR`, of the Tools group) and this tab answer the same question with the same rule of red (see
[CI_RED_CONTRACT.md](CI_RED_CONTRACT.md)); they differ in where they run. The monitor reads from the machine of its owner, in a complete edition with the sentinel and its
thirteen checks A1 to A13 and in a lite edition without it; the dashboard reads in GitHub Actions with the read-only token of the workflow and publishes only what is safe.

| Panel of the monitor | What it checks | In this tab |
|---|---|---|
| A1 | builds stuck or queued for too long, `build-failed` and `build-stuck` issues | Builds tab |
| A2 | red CI by the single rule | red workflows |
| A3 | security alerts (CodeQL, Dependabot, secret scanning) | never shown here: nothing about security alerts is published |
| A4 | Dependabot pull requests | not shown |
| A5 | releases: candidate (5 or more entries under `[Unreleased]`), green release build, waiting for a signature | releases ready, signatures |
| A6 | hygiene: ruleset, labels, required files, pinned actions | hygiene |
| A7 | usage: Actions minutes, budgets, allowance left | computing |
| A8 | state of the work-round files of the owner | not applicable |
| A9 | roadmap boards alive | not shown |
| A10 | surface of Actions and releases (twenty-five checks) | partly, in the Scripts tab |
| A11 | readiness and health score per ecosystem, dependency pins | table by ecosystem |
| A12 | analytics: p50 and p95, slower and flaky workflows | Builds tab |
| A13 | workflow linter | Scripts tab |

The next version of the monitor (not published yet) gives the panels A1 to A13 as data, with one inventory of signals that say whether to act, watch or just know, so an AI
tool does not have to read the page. It also adds a Low mode that saves the allowance, a read-only GitHub App with an allowance of its own, and reads this panel
(`data/sentinel.json` of the profile repository) as a base line that spends no allowance: it ignores the file when it is more than two hours old and says so. That is why
the file is refreshed every half hour and why this tab warns when it is behind. A used-up allowance is reported as one notice, not one error per repository.

### Connecting an AI tool to the monitor

Both editions share the same five channels: a brief of what to do now, a feed of alerts, the state as data (`/api/ai/state`), a stream of events (complete edition) and MCP
tools, plus a gate script (`ai-hook`) that adds the brief to the session of the AI. Everything is read only unless an action is allowed. The guide
[AI_CONNECTION](https://github.com/JuanenRac/TOOLS-GITHUB-ACTIONS-MONITOR/blob/main/monitor/docs/AI_CONNECTION.md) explains each step.

## What is still never shown

Security alerts (not even a count), titles of pull requests and issues, people, branches and texts written by outsiders. The document is rebuilt from a
whitelist on every write, so none of them can get through whatever the input holds.

## Settings

| Key | Default | Meaning |
|---|---|---|
| `events_max` | 30 | length of the feed of changes |
| `sections.ecosystems` | true | table by ecosystem |
| `sections.events` | true | feed of changes |
| `sections.releases` | true | releases ready and versions raised without a release |
| `candidate_min_entries` | 5 | entries under `[Unreleased]` that make a repository a release candidate |
| `stale_hours` | 1 | how long an unchanged reading keeps its moment (so a quiet panel is written at most once an hour) |
| `behind_minutes` | 120 | age of the reading from which the tab says the panel is behind |
