# HYDRA-UMC Ecosystem Dashboard Update Protocol

The public dashboard at `https://juanenrac.github.io/JuanenRac/` is generated
from the public `hydra-umc.project.json` manifests that each ecosystem
repository publishes.

## Update paths

1. **Immediate, event-driven refresh.** Each product repository contains
   `.github/workflows/dashboard-dispatch.yml`. A successful push to `main`
   sends a `repository_dispatch` event to this repository, which regenerates
   the dashboard without waiting for a polling interval.
2. **Scheduled recovery.** `build-dashboard.yml` also runs on a schedule. It
   is a recovery mechanism for a missed remote event and for a repository
   added before its notifier workflow is enabled.
3. **Manual recovery.** `Build ecosystem status dashboard` remains available
   from the Actions page when an operator needs an explicit refresh.

4. **Build finished (Builds tab).** A project may also send the event type
   `ecosystem_build_finished` when one of its workflows ends, so the Builds tab
   (state, results, durations and open `build-failed` / `build-stuck` issues of every
   repository) is almost live. The event is optional: without it the tab is refreshed
   by the schedule every 30 minutes. A small gate job in `build-dashboard.yml`
   lets the event through only when the repository named in the payload belongs to
   this owner and is not this repository, and not when the dashboard was built less
   than 15 minutes earlier (the schedule catches up); the run then uses the same
   concurrency group as every other trigger, so runs never pile up. The gate is
   read-only, uses no secret and no third-party action. The notifier of a project
   only needs a `workflow_run` trigger next to its existing push trigger:

   ```yaml
   on:
     workflow_run:
       workflows: ["CI"]            # the name of the project's build workflow
       types: [completed]
   ```

   and the same dispatch step it already has, with `event_type` set to
   `ecosystem_build_finished` and `client_payload` holding `{"repository": "<owner>/<name>"}`.

5. **Sentinel tab.** The same build also reads, with the read-only token of the
   workflow, a small public-safe picture of the repositories: red workflows
   (the last finished run of each workflow on the default branch), releases
   ready (entries under `[Unreleased]` and the age of the last release), the
   state of the signature already verified, the public rulesets and, when the
   token may read them, the Actions settings, and the approximate computing
   minutes. The result is a short report made by fixed rules (no AI) and is
   written to `data/sentinel.json`, which is rebuilt from a whitelist: security
   alerts (not even a count), titles of pull requests and issues, people and
   branches are never kept or shown. Thresholds and sections are set in the
   `sentinel` block of `dashboard-config.json`.

The generator never trusts a repository-dispatch payload as dashboard data.
It independently discovers public repositories and reads their manifests, so
one malformed or stale notification cannot publish invented project metadata.

## One-time GitHub configuration

The dispatching workflow intentionally has no embedded credential. Create a
fine-grained personal access token for the `JuanenRac` resource owner,
restricted to the single `JuanenRac/JuanenRac` repository, with only the
**Contents: Read and write** repository permission. GitHub requires Contents
write to create a repository-dispatch event. Store it as the Actions secret
named
`ECOSYSTEM_DASHBOARD_DISPATCH_TOKEN` in every product repository that should
notify the dashboard.

Until that secret exists, each notifier exits successfully with an explicit
"not configured" message. Project builds and tests are therefore never made
dependent on dashboard credentials.

## Security boundary

- The token is exposed only to the single dispatch step and is never printed.
- Fork pull requests do not trigger the notifier because it listens only to
  pushes on the repository's `main` branch.
- The event contains only public repository name, commit SHA and ref (the build-finished event, only the repository name).
- The Builds tab keeps state and numbers only: the result and duration of each run and the minutes of computing; never who started a run, the branch or the text of a commit.
- The signatures of the releases are verified in the same read-only job, with public keys only (see `CI_EVIDENCE.md`); the page itself never calls GitHub and holds no key.
- `data/delivery-cache.json` (the verdict per release and the inferred builds) travels with the other generated files and is written only when its content changes.
- The central workflow validates public manifests independently and serializes
  publication through its existing concurrency group.

## When GitHub cannot be read

The generator never replaces what is published with a gap:

- If the CI, release and commit data cannot be read, the page keeps the last
  known version of them (read back from the page that is published), marks
  them with the date of that version and never shows them as current or as
  "no alerts".
- If an ecosystem that is on the published page cannot be read at all, the
  published page is kept as it is until GitHub answers again.
- The Errors / unknown tab lists the exact reason for each repository and
  shows when the page was generated, how long it took and how many
  repositories were resolved out of those attempted.
- The URTC rack tab shows the snapshot published in `data/rack-snapshot.json`
  (the format written by URTC-COMMON). Without that file, or with an unusable
  one, it says there is no data and shows no state.
