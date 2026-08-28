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
- The event contains only public repository name, commit SHA and ref.
- The central workflow validates public manifests independently and serializes
  publication through its existing concurrency group.
