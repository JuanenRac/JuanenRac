# Declared tests

The tab **Tests** of the dashboard shows how many automated tests each repository declares, per ecosystem and per project. It is a **declared** figure: every repository states its own count and the dashboard reads it. The dashboard does not run any test. What a CI run proved is shown in the Evidence tab ([CI evidence](CI_EVIDENCE.md)).

## Where the count comes from

`dashboard-config.json`, key `tests.sources`, says which source each ecosystem uses:

```json
"tests": {
  "sources": {
    "hydra-umc": { "glance": "HYDRA-UMC-DOCS/data/glance.json", "readme": true },
    "urtc":      { "glance": "URTC-DOCS/data/glance.json", "readme": true },
    "armor":     { "readme": true },
    "eh3d":      { "readme": true }
  }
}
```

* `glance`: `repository/path` of a glance file; the count of a repository is `repos.<name>.tests.count`. It is read first.
* `readme`: when the glance file has no count for the repository (or there is no glance file), the row `| Tests | ... |` of the quick-facts table of the README of the repository is used. A leading number is the count (`134 (...)`, `110 tests (...)`). A row that counts the checks of host programs (`11979 checks in 20 host programs`) is kept as **checks**: it is listed apart and never added to the tests.

Everything is read from `raw.githubusercontent.com` (no API quota) at build time; the page makes no request of its own.

## What is never invented

| Situation | What the page shows |
| --- | --- |
| The source answered and has a number | the number, with where it was read (README or glance.json) |
| The source answered and has no number | *Not declared* (never a zero) |
| The lookup failed | the last known count of the daily history with its date and a banner, or *Not verified* when there is none |
| The README counts checks, not tests | the checks, apart, without a bar and outside the totals |

The daily history (`data/history.json`) records, for every snapshot, the tests declared in that run (`tests`: `{repository: number}`). A last known value is never written into the history, and snapshots from before the field existed stay valid: they simply give no point to the evolution chart. The total of an ecosystem can rise because a repository starts to declare its tests, not only because tests were written.
