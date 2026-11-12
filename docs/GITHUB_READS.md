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

## The queue time of the builds

The queue time shown in the Builds tab is the one of the **run** (from its creation to the start of the run), which comes in the list of runs that is read anyway. The local Actions monitor
measures the queue of each **job**, which needs one more read per run; the dashboard does not make those reads, so its figure can be higher than the monitor's when a run has jobs
that start one after the other.

## Quota: how the dashboard and the local monitor spend it

The two share the same ideas, so that neither starves the other:

* **Conditional reads.** An unchanged answer is a `304` and costs nothing (ETag, see above); a repository that was not pushed is not read at all.
* **Batched GraphQL.** The Sentinel and the activity read twenty repositories per query (release, changelog, workflow list, last commit and state of the checks) instead of
  several REST calls each.
* **Low mode of the monitor** (next version, not published yet). Besides Normal, Fast and Turbo, a Low mode reads only the hot repositories often and the rest rarely, and says in
  its bar how old its figures can be. It starts by itself when the allowance is low and ends when it renews.
* **A read-only GitHub App** has its own allowance, separate from the one of the user and larger with more repositories; writes keep the token of the user.
* **The central panel as a base line.** The monitor can read `data/sentinel.json` of this repository (a plain fetch or the raw file) and only ask the API live about what the panel
  marks as red or running. For that to be useful the file is refreshed at least every half hour (see [DASHBOARD_UPDATES.md](DASHBOARD_UPDATES.md)) and ignored when it is more than two
  hours old.
* **A used-up allowance is one notice.** The reads stop until the renewal and the list says "allowance used up until the renewal" once, grouped, instead of one error per
  repository; nothing turns red for it.
