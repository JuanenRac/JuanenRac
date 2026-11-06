# Changelog

All notable changes to this profile repository are documented here.

## [Unreleased]

- **One criterion for a red build:** the Sentinel tab, the Builds tab and the CI watch issue now share a single definition (`scripts/ci_rules.py`): `failure`, `timed_out`, `startup_failure` and `action_required` on the last finished run of a workflow on the default branch are red; cancelled, skipped, neutral and stale runs are passed over; runs generated for dependency updates never count.
- **The profile has a changelog:** the changes of the profile, the generated README and the status dashboard are listed here from now on.
