# Changelog

All notable changes to this profile repository are documented here.

## [Unreleased]

- **Signature and attestation of the latest release:** the Sentinel tab has a card, by ecosystem and by repository, and the panel of each repository two fields, that show whether the release files carry a signature file and a GitHub build attestation (present, partial, absent, not applicable or unknown), in the eight languages. Presence only; the attestation is read for a few files per release, inside the `presence` budget of requests and cache of `dashboard-config.json`, and what could not be read stays unknown. See `docs/SIGNATURE_PRESENCE.md`.
- **Sentinel tab, by ecosystem:** a table with the repositories, the red workflows, the releases ready and the unpublished versions of each ecosystem.
- **Sentinel tab, version raised but not published:** repositories whose manifest declares a version newer than their latest release are listed and appear in the short report.
- **Sentinel tab, recent changes:** a short feed (`sentinel.events_max`) of workflows that turned red or green again and of releases that appeared, kept in `data/sentinel.json`; see `docs/SENTINEL.md`.
- **One criterion for a red build:** the Sentinel tab, the Builds tab and the CI watch issue now share a single definition (`scripts/ci_rules.py`): `failure`, `timed_out`, `startup_failure` and `action_required` on the last finished run of a workflow on the default branch are red; cancelled, skipped, neutral and stale runs are passed over; runs generated for dependency updates never count.
- **The profile has a changelog:** the changes of the profile, the generated README and the status dashboard are listed here from now on.
