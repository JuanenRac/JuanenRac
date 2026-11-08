# How the dashboard reads GitHub

The dashboard is built in GitHub Actions with the read-only token of the workflow, whose quota is small. Two things keep a refused read from stopping the build.

## Conditional reads (ETag)

[`scripts/gh_http.py`](../scripts/gh_http.py) reads the REST API with `If-None-Match`. An answer that has not changed is a `304`, which costs no quota, and the saved body
is used. The saved copy is `data/etag-cache.json`; it is **not committed**: the build restores and stores it with the Actions cache. The generation card of the page
shows the reads made, the ones that were free thanks to the ETag and the ones answered from the saved copy.

When GitHub refuses a read because the quota is spent (`429`, or `403` with no requests left, a `Retry-After` or a message about the rate limit) or does not answer, the
last good answer is used instead of failing, as long as it is not older than `stale_max_hours`. A real refusal (`403` for lack of permission, `404`) is never hidden by
the copy.

The limits live in the `http_cache` block of [`dashboard-config.json`](../dashboard-config.json): `enabled` (switch it off and every read goes to GitHub as before),
`max_entries`, `max_body_bytes`, `stale_max_hours` and `path`.

## When the discovery of the repositories cannot be read

If the discovery of an ecosystem fails because GitHub refused or did not answer, the build does **not** fail: the page that is published stays, with a notice at the top
of the summary that says it is the last good version and gives its date. Anything else (every manifest invalid, a parser that changed) is a real problem and still fails
the build.

## What the page says about its coverage

The card **Unclassified** next to the ecosystem counters gives the public repositories of the owner, how many the page lists and how many have no manifest, with their
names. A list that could not be read says "not verified", never zero. A notice lists the repositories that are new, archived or gone since the page that was published
before; it is only made when the list of this run was really read (not from the saved copy).
