# Changelog

All notable changes to this profile repository are documented here.

## [Unreleased]

- **Sentinel tab, by ecosystem:** a table with the repositories, the red workflows, the releases ready and the unpublished versions of each ecosystem.
- **Sentinel tab, version raised but not published:** repositories whose manifest declares a version newer than their latest release are listed and appear in the short report.
- **Sentinel tab, recent changes:** a short feed (`sentinel.events_max`) of workflows that turned red or green again and of releases that appeared, kept in `data/sentinel.json`; see `docs/SENTINEL.md`.
- **One criterion for a red build:** the Sentinel tab, the Builds tab and the CI watch issue now share a single definition (`scripts/ci_rules.py`): `failure`, `timed_out`, `startup_failure` and `action_required` on the last finished run of a workflow on the default branch are red; cancelled, skipped, neutral and stale runs are passed over; runs generated for dependency updates never count.
- **The profile has a changelog:** the changes of the profile, the generated README and the status dashboard are listed here from now on.
