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
