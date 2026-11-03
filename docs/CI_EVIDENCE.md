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
