# Signature and attestation presence

The Sentinel tab has a card, and the panel of every repository two fields, that say whether the latest release of a repository carries a signature and a build
attestation. It only says whether they are THERE: no key and no proof is verified by this part (the signature check against a pinned public key is a separate
step, shown in the evidence tab).

## What is looked at

- **Release files:** the assets of the latest release that are not a sidecar and end with one of `release_extensions` (`.bin`, `.tgz`, `.zip`, `.apk`, ...).
  Sidecars are `.sha256`, `.sig`, `.sig2`, `.imgsig`, `.hdr2`, `.asc` and `.minisig`. A repository without release files is "not applicable".
- **Signature:** every release file has a signature file next to it (`<file>.sig`, `.sig2`, `.imgsig`, `.asc` or `.minisig`). Decided from the names of the assets, with
  no request.
- **Attestation:** GitHub keeps the build provenance written by `actions/attest-build-provenance` and returns it for the SHA-256 digest of a file, from
  `/repos/{owner}/{repo}/attestations/{digest}`. Only its existence is read, for up to `attestation_files_per_release` files of the release, with the digest GitHub
  holds for the asset. The endpoint answers for public repositories with the read-only token of the workflow.

## States

| State | Meaning |
|---|---|
| present | all the files asked have it |
| partial | some have it |
| absent | none has it |
| not applicable | the repository has no release files |
| unknown | it could not be read: no release data, no digest, a refused token, a failed request or the budget of requests used up |

Unknown is never shown as absent. If the token is refused (HTTP 401 or 403) no further attestation request is made in that pass and every attestation that
was not read stays unknown.

## Settings

The `presence` block of `dashboard-config.json`:

| Key | Default | Meaning |
|---|---|---|
| `enabled` | true | switches the whole part off |
| `attestations` | true | when false the attestation is always unknown and no request is made |
| `max_repos_per_run` | 30 | repositories that may need requests in one pass |
| `api_budget` | 120 | requests of the pass (one per release read plus one per attestation) |
| `attestation_files_per_release` | 3 | files of a release whose attestation is asked |
| `recheck_days` | 3 | days before an attestation that is not present is asked again |
| `release_extensions` | see file | extensions that make an asset a release file |

## Cache

The answer is kept in `data/delivery-cache.json` (key `presence`) with the tag and a fingerprint of the assets, so a release already read is not asked again;
"present" does not expire, any other answer is asked again after `recheck_days`. A new tag or a changed asset list always starts again. When GitHub could not be read
in a pass, the last published page keeps the presence it had.
