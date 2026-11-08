# How the dashboard reads GitHub

The dashboard is built in GitHub Actions with the read-only token of the workflow, whose quota is small. Two things keep a refused read from stopping the build.

## Saved reads: nothing pushed, ETag, and the saved copy

[`scripts/gh_http.py`](../scripts/gh_http.py) reads the REST API and keeps every answer in `data/etag-cache.json`. That file is **not committed**: the build restores and stores
it with the Actions cache. The generation card of the page shows the reads made, the ones that were saved and the ones answered from the saved copy.

* **Nothing pushed, nothing read.** The list of repositories gives the moment of the last push of each one. A repository that was not pushed since its saved commit was read is
  not read again: no request at all. This is the saving that works with the token of a workflow.
* **ETag.** A read that does go out sends `If-None-Match`; an unchanged answer is a `304`, which costs no quota. GitHub ties an ETag to the token that read it, so a new token
  in every run (the case of a workflow) does not get a `304` for what another token read; the ETag helps the reads repeated with the same token.
* **The saved copy.** When GitHub refuses a read because the quota is spent (`429`, or `403` with no requests left, a `Retry-After` or a message about the rate limit) or does
  not answer, the last good answer is used instead of failing, as long as it is not older than `stale_max_hours`. A real refusal (`403` for lack of permission, `404`) is
  never hidden by the copy.

The limits live in the `http_cache` block of [`dashboard-config.json`](../dashboard-config.json): `enabled` (switch it off and every read goes to GitHub as before),
`max_entries`, `max_body_bytes`, `stale_max_hours`, `unchanged_margin_seconds` (how much newer than the push the saved answer must be) and `path`.

## The progress bars and the status rows

`scripts/ecosystem_progress.py` and `scripts/ecosystem_status.py` read the tags, the files and the last builds of every repository. They use the same saved reads: the tags and
the files are not read again for a repository that was not pushed, and the second script gets most of its answers from the first one (same token, so the ETag works inside a
run). When GitHub refuses the reads because the quota is spent and no saved answer can stand in, the bars and the rows keep their last values, the step says so and the build
goes on; any other failure to read still stops it.

## When the discovery of the repositories cannot be read

If the discovery of an ecosystem fails because GitHub refused or did not answer, the build does **not** fail: the page that is published stays, with a notice at the top
of the summary that says it is the last good version and gives its date. Anything else (every manifest invalid, a parser that changed) is a real problem and still fails
the build.

## What the page says about its coverage

The card **Unclassified** next to the ecosystem counters gives the public repositories of the owner, how many the page lists and how many have no manifest, with their
names. A list that could not be read says "not verified", never zero. A notice lists the repositories that are new, archived or gone since the page that was published
before; it is only made when the list of this run was really read (not from the saved copy).
