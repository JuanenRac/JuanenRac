# Code tab

The Code tab of the status dashboard shows how much code, how many tests and how much documentation every repository of the four ecosystems has, and how
that changes day by day. The figures are counted, not declared: a script reads the files of a fresh shallow copy of each repository.

## Where the figures come from

| Piece | What it does |
|---|---|
| `scripts/code_stats.py` | Lists the public repositories of the owner, takes a shallow clone (`git clone --depth 1`) of each one in a temporary directory of its own, counts the lines and deletes the clone. Standard library only. |
| `code-stats-config.json` | The rules: which ecosystem a repository belongs to (by name prefix), its type, what is excluded, what is a test or a translation, and how the history is thinned out. Nothing of this is in the code. |
| `.github/workflows/code-stats.yml` | Runs the script every day and on demand. The counting job has a read-only token; only the publishing job can write, and it commits the two data files. Every action is pinned to a full commit. |
| `data/code-stats.json` | The figures of the last run: one record per repository. |
| `data/code-history.json` | One snapshot per day (totals, by ecosystem and by type), thinned out as it gets older. |
| `scripts/dashboard_code*.py` | Reads the two files when the dashboard is built, checks them against a whitelist and embeds them in the page; the tab draws everything in the browser. |

The dashboard reads the files in its next regular build, so a new count appears there within the hour.

## What is counted

For every repository the script keeps:

* **Code**: files and lines of the programming languages (code, comment and blank lines, by language), outside test files.
* **Tests**: the same for test files (a test folder or a test file name from the configuration), plus the number of test cases found by the test marker of
  each language. When the documentation repository of an ecosystem publishes a count of tests for a repository (the glance file), it is kept as the
  declared count and shown next to the counted cases; the tab falls back to the count the Tests tab already reads.
* **Documentation**: Markdown, reStructuredText, AsciiDoc and text files, the translated READMEs included.
* **Translation files**: files in translation folders or with translation names, and the translated READMEs. They are counted apart.
* **Data**: JSON, YAML, TOML and similar files, in a separate figure that is never added to the code.
* **Size** of the counted files and the **last commit** day.

A line that has code and a comment counts as code. A docstring counts as code. A repository that could not be read keeps its last known figures and says so;
one that was never read is shown as not measured. If fewer than half of the repositories can be read in a run, that day's point is not added to the history,
so a GitHub outage does not draw a false dip.

## What is left out

Generated files (a `.gitattributes` that marks them `linguist-generated`, and generated names), vendored code (`linguist-vendored`), dependencies, build
output, binaries, images, lock files, files that are too big and files with a very long line (minified or bundled). The lists are in the `exclude` block of
`code-stats-config.json`.

## Types and ecosystems

An ecosystem is a list of name prefixes. The type of a repository (firmware, apps, services, tools or documentation) is the first rule of `types.rules`
whose pattern matches its name; anything else is `tools`. Adding a repository needs no change unless it must be something other than the default.

## The tab

* Ten figures for the whole ecosystem.
* Stacked bars of code, tests and documentation for the whole, for each ecosystem and for each type.
* The mix of programming languages, for the whole and for each ecosystem.
* Lines over time (whole and by ecosystem, chosen kind of line) from the daily history.
* The largest repositories, stacked (10, 20 or 30).
* A table by repository, ecosystem or type that can be sorted by any column and filtered by ecosystem, type and name, with its total.

Every chart has a table with the same figures, a name for assistive technology and a tooltip on hover and on keyboard focus. Nothing relies on colour alone,
and the colours of the charts have a version for the light and the dark theme. The texts are in the eight languages of the dashboard.

## Running it by hand

```
python scripts/code_stats.py --out data
```

needs `git` and, to read more than the public limit of the API, a `GITHUB_TOKEN` in the environment (it is handed to git through the environment, never in a
command). `--local-root DIR` counts directories that are already cloned (`DIR/<repository>`) instead of cloning. The tests of the counter are in
`tests/test_code_stats.py` and run without network.
