# CI evidence contract

The manifest of every repository **declares** how far it has been proven (`evidence`: `none`, `host-test`, `simulator`, `bench`, `field`).
A claim is not a proof. A repository can let the status dashboard **verify** that claim by publishing, from its own continuous integration,
a small JSON record of what ran. The dashboard then shows the two side by side in the Evidence tab ("Declared against verified").

* Nothing published is shown as **not verified**. It is never shown as verified and never as failed.
* A record that cannot be read, or that breaks the schema, proves nothing and the dashboard says why.
* Old records expire: a run proves its level only for a limited number of days (set in `dashboard-config.json`, `ci_evidence.expire_days`).

## Where the file lives

One file per repository, on a branch that only holds evidence:

| Setting | Default | Where it is set |
| --- | --- | --- |
| Branch | `ci-evidence` | `dashboard-config.json`, `ci_evidence.branch` |
| File | `ci-evidence.json` | `dashboard-config.json`, `ci_evidence.path` |
| Only counts when the tested branch is | `main` | `ci_evidence.default_branches` |
| Days a record proves its level | host test 14, simulator 30, bench 180, field 365 | `ci_evidence.expire_days` |

The dashboard reads `https://raw.githubusercontent.com/JuanenRac/<repository>/ci-evidence/ci-evidence.json` (no API quota is used).
A missing file (HTTP 404) means "the repository publishes no evidence"; any other failure means "could not be read" and is shown as such.

## The format

The schema is [`evidence-schema.json`](evidence-schema.json) (JSON Schema 2020-12). In short:

```json
{
  "schema_version": "1.0",
  "records": [
    {
      "repo": "EXAMPLE-REPOSITORY",
      "workflow": "ci.yml",
      "commit": "0123456789abcdef0123456789abcdef01234567",
      "branch": "main",
      "date": "2000-01-01T12:00:00Z",
      "version": "1.2.3",
      "test_type": "host-test",
      "result": "pass",
      "environment": "ubuntu-24.04",
      "hardware": null,
      "url": "https://github.com/JuanenRac/EXAMPLE-REPOSITORY/actions/runs/1"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `repo` | The repository that publishes the record. A record that names another repository is refused. |
| `workflow` | File name of the workflow that ran. |
| `commit`, `branch` | What was tested. Only the default branch counts. |
| `date` | When the run finished (ISO 8601, UTC). |
| `version` | Version of the project that was tested. |
| `test_type` | `unit`, `integration` and `host-test` prove the **host-test** level; `simulator`, `bench` and `field` prove their own. |
| `result` | `pass`, `fail`, `partial` or `skipped`. Only `pass` proves a level. |
| `environment` | Where it ran (runner image, simulator, bench). |
| `hardware` | `null`, or `{ "bound": true, "device": "..." }`. **Required** for `bench` and `field`: a run that does not name the real hardware cannot prove it. |
| `url` | Link to the run, inside the repository that publishes the record. |
| `details` | Optional. Anything else worth keeping; the dashboard does not read it. |

Keep the latest record of each workflow and kind of test (at most 50 records in the file).

## How the verdict is decided

The **verified level** is the highest level proven by a passing record on the default branch that has not expired.

| State shown | When |
| --- | --- |
| Verified | the verified level reaches the declared one |
| Declares more than it proves | the verified level is lower than the declared one |
| Failing | the latest relevant run failed |
| Expired | the repository only has records older than their limit |
| Not verified | nothing is published (or nothing on the default branch) |
| Invalid records | every record breaks the schema |
| Could not be read | the file could not be fetched in this build |

## Adopting it in a repository

A job at the end of the CI, with write permission **only in that job**, writes the file to the evidence branch. This is a template; pin every
third-party action to a full commit SHA, as the workflows of this repository do.

```yaml
permissions: {}

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      # ... checkout, run the tests ...

  publish-evidence:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      contents: write          # only this job may write, and only to the evidence branch
    steps:
      - name: Publish the evidence record
        env:
          GH_TOKEN: ${{ github.token }}
          RESULT: ${{ needs.test.result == 'success' && 'pass' || 'fail' }}
        run: |
          set -euo pipefail
          git clone --quiet --depth 1 "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" repo
          cd repo
          if git ls-remote --exit-code --heads origin ci-evidence >/dev/null; then
            git fetch --quiet --depth 1 origin ci-evidence && git checkout --quiet ci-evidence
          else
            git checkout --quiet --orphan ci-evidence && git rm -rf --quiet . || true
          fi
          python3 - <<'PY'
          import json, os, pathlib
          path = pathlib.Path("ci-evidence.json")
          data = json.loads(path.read_text()) if path.exists() else {"schema_version": "1.0", "records": []}
          record = {
              "repo": os.environ["GITHUB_REPOSITORY"].split("/")[1],
              "workflow": os.environ["GITHUB_WORKFLOW_REF"].split("/")[-1].split("@")[0],
              "commit": os.environ["GITHUB_SHA"],
              "branch": "main",
              "date": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "version": pathlib.Path("VERSION").read_text().strip() if pathlib.Path("VERSION").exists() else "unknown",
              "test_type": "host-test",
              "result": os.environ["RESULT"],
              "environment": os.environ.get("ImageOS", "ubuntu"),
              "hardware": None,
              "url": f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
          }
          data["records"] = [r for r in data["records"] if (r["workflow"], r["test_type"]) != (record["workflow"], record["test_type"])] + [record]
          path.write_text(json.dumps(data, indent=1) + "\n")
          PY
          git add ci-evidence.json
          git -c user.name="github-actions[bot]" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" commit --quiet -m "Update CI evidence"
          git push --quiet origin HEAD:ci-evidence
```

A bench or field run is published by whoever operates the bench (a self-hosted runner, or a person), with `test_type` `bench` or `field`,
`hardware.bound` `true` and the board in `hardware.device`. The dashboard never invents it: no record, no proof.

## Delivery pipeline: where a release was built and signed

The dashboard also shows how each release was made: built on GitHub Actions, signed on the owner's computer, then published. Two things feed it.

**What the dashboard reads itself, nothing to declare.** The assets of the latest release of every repository. A release without a signature file (`.sig`,
`.sig2`, `.asc` or `.minisig`) is shown as "no signature"; no release means there is nothing to sign; assets that could not be read are "not verified". The
column "Signed release" of the evidence tab and its summary use this. A cell that is missing, invalid or not verified explains why when it is pressed and links
to the repository.

**Signatures are verified, not only detected.** In the job that builds the page (read-only token, no secret) the generator checks the Ed25519 signature of the
latest release of the repositories of the three families that sign their releases, with the PUBLIC key that each family pins (the private keys never leave the
owner's computer). The check is written in pure Python (`scripts/dashboard_ed25519.py`, RFC 8032): nothing is installed. It reads the release once through the
REST API (which gives the SHA-256 that GitHub itself holds for every asset), downloads only the small signature files, rebuilds the message the family signs and
verifies it:

| Family | Signed message | Files |
| --- | --- | --- |
| A.R.M.O.R. packages | `armor-pkg/1\|<component>\|<version>\|<sha256>` | `armor-<component>-<version>.tgz` and its `.sig` |
| A.R.M.O.R. firmware | `armor-fw/1\|<project>\|<board>\|<version>\|<sha256>` (`.sig2`) and the 32 bytes of the SHA-256 (`.sig`) | `<project>-<board>.bin` |
| URTC releases | `urtc-rel/1\|<file name>\|<sha256>` | any asset with a `.sig` |
| URTC packages | `urtc-pkg/1\|<app>\|<version>\|<platform>\|<sha256>\|<size>` | `<app>-<version>-<platform>.zip` or `.tar.gz`, and the files of URTC-COMMON |
| HYDRA-UMC packages | `hydra-pc-pkg/1\|<project>\|<version>\|<sha256>` | `<project>-<version>.tgz` |
| HYDRA-UMC binaries | the whole file, signature in base64 | the file is downloaded (up to the configured size) |

The answer for a repository is one of: **signature verified** (every signature that could be checked is valid for the pinned key and for the hash GitHub holds),
**signature INVALID** (a well formed signature does not verify: the file changed after it was signed, or another key, name or version; this is always a health
alert), **present but not verifiable here** (a family without a pinned key, a `.asc` or `.minisig` file, an unknown message, or a file too large to download),
**no signature** and **not verified** (a read failed; it is never reported as a good or a bad signature). A repository of any other family that publishes a
signature file is "not verifiable here" until its scheme and public key are added to the generator.

`dashboard-config.json` has a `signatures` block: `enabled`, `max_asset_bytes` (50 MB by default: a larger file is not downloaded; its GitHub digest still
verifies a hash-only scheme, and a whole-file signature is reported with the reason "too large, check the signed .sha256"), `max_repos_per_run` (the quota of
requests of one run) and `keys` (the pinned public key of each family, 64 hexadecimal digits). The answer is cached by tag plus a fingerprint of the assets in
`data/delivery-cache.json`, so a release is read once and only a new release costs requests.

**Optional fields of the project manifest** (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`...). They are never
required: what is not declared is shown as "not declared". The formal description is `$defs.delivery_fields` of [`evidence-schema.json`](evidence-schema.json).

| Field | Values | Meaning |
| --- | --- | --- |
| `built_on` | `gha`, `local`, `unknown` | where the binary of the release was built |
| `last_build_artifact_url` | `https://github.com/JuanenRac/<repository>/...` | the last green build that produced the artifact (a run or its artifact page) |
| `signature_kind` | `none`, `dev`, `release` | unsigned, signed with a development key, signed with the release key |
| `signed_on` | `local`, `unknown` | where the signing was done |

From them, from the real release and from what is inferred (below) the dashboard derives one state per repository, shown as a column and a filter of the projects
tab and in the panel of the repository: `built`, `signed`, `published` (a release with assets exists and a build or a signature is proven), `release_only` (a
release, nothing known about how it was made) and `undeclared`. A value outside the lists is ignored.

**Inferred without waiting for a manifest.** `built` is also proven when the latest successful run of a build workflow of the repository (`firmware-build.yml`,
`binaries-build.yml`, `package-build.yml`, `apk-build.yml`, `exe-build.yml`, `dist-build.yml`, `site-build.yml`, `release-files-build.yml`) still has an artifact
that has not expired; `signed` is also proven by a verified signature (above). An inferred value is only used where the manifest declares nothing, is marked
"inferred" (the word appears in the table and in the panel) and never replaces a declared one. Only the state, the workflow file, the time and the address of the run
are kept: never who started it, the branch or a commit title.

**Optional alert.** `dashboard-config.json` has `signature_alert` (`enabled`, off by default, and `after_days`, or `after_hours` which replaces it): when it is
on, a repository built on GitHub Actions (declared or inferred) with a green CI and no signature on its latest release raises a health alert once the green build
with an artifact is older than the threshold (without a known build, the last commit is used). A signature that does not verify raises an alert always.
`history_min_days` sets the days of history the analysis views need before they stop saying "insufficient history".
