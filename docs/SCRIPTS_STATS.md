# Scripts tab

The Scripts tab of the status dashboard shows what every repository of the four ecosystems and of the Tools group runs: its GitHub workflows (when they run, which actions they use and how the
version of each action is fixed) and the scripts of its `tools/` and `scripts/` folders by language. Nothing is run and nothing is asked of GitHub for it: a script
reads the files of the same fresh shallow copy that the Code tab counts.

## Where the figures come from

* `scripts/scripts_stats.py` (standard library only) reads one working tree. The YAML of a workflow is not loaded as YAML: the few keys that matter (`on`,
  `jobs`, `runs-on`, `uses`) are read line by line, so a workflow is never executed or evaluated.
* `scripts/code_stats.py` calls it for every repository in its daily run (workflow `code-stats.yml`) and writes `data/scripts-stats.json` next to the code figures. A
  repository that cannot be read keeps its last known figures, marked as such; one that was never read is shown as not read, never as zero.
* `scripts/dashboard_scripts.py` rebuilds the block the page embeds from a whitelist (an unknown trigger, pin or language is dropped, a number that is not a plain
  number becomes zero) and `scripts/dashboard_scripts_ui.py` draws it in the browser, with the stacked bars, the legend, the table of each chart and the tooltip of
  the other tabs.

| Figure | What it is |
|---|---|
| Workflows, jobs | the files of `.github/workflows` and the entries under `jobs:` |
| Triggers | the events under `on:`: push, pull request, schedule, by hand (`workflow_dispatch`), release, after another workflow (`workflow_run`), called by another (`workflow_call`) and any other event; a workflow with several triggers counts once for each |
| Uses of actions | every `uses:` of the steps and of the reusable workflows |
| How an action is pinned | **commit** (a full 40-character commit, which cannot move), **version tag** (such as `v4`), **branch or no version** (anything else), **this repository** (a path) and **container image** |
| Not pinned to a commit | the uses of actions of other owners whose version is a tag or a branch |
| Scripts | the `.py`, `.sh`, `.ps1`, `.bat`/`.cmd` and `.js`/`.mjs`/`.cjs`/`.ts` files under `tools/` and `scripts/`, with their lines |

Whether a pinned action is out of date is not known without asking GitHub, so the tab does not say it.

## What the tab shows

* Seven figures: repositories with workflows, workflows, jobs, uses of actions, uses not pinned to a commit (with their share), script files and script lines.
* Stacked bars of the triggers, of how the actions are pinned and of the scripts by language, for the whole, each ecosystem and each type.
* The most used actions (10, 15 or 30), stacked by how their version is fixed, and the repositories with most workflows, stacked by trigger.
* The list of the actions of other owners that are not pinned to a commit, with the number of uses and of repositories.
* A table by repository, ecosystem or type that can be sorted, filtered by ecosystem and type, searched by name and grouped, with a total.

Every chart has a table with the same figures, a name for assistive technology and a tooltip on hover and on keyboard focus; the texts are in the eight languages.
A document older than three days says how old it is, and a build that could not read it says "not verified" instead of drawing zeros.

## Lint of the workflows

The same daily count runs a small linter over every workflow file ([`scripts/workflow_lint.py`](../scripts/workflow_lint.py)), with the rules and the three levels of the
local Actions monitor: **information**, **warning** and **error** (the monitor calls its highest level "bad"). Only counts are kept, per repository, per level and per rule:
never a value, a name or a line.

| Rule | What it finds | Default level |
|---|---|---|
| `unpinned_uses` | an action or reusable workflow whose version is a tag or a branch, not a full commit | warning |
| `permissions` | no `permissions:` block at all, or `write-all` | warning |
| `secrets_in_clear` | something that looks like a secret written in the file (a known token format or a long high-entropy string is an error, an unclear value a warning, a readable filler only information) | error |
| `injection` | a text controlled by someone else (an issue title, a branch name...) pasted into a `run:` script | warning |
| `pr_target` | `pull_request_target` together with a checkout of the code of the pull request | error |

The `lint` block of [`code-stats-config.json`](../code-stats-config.json) switches the whole check or a rule off, gives a rule another level, and lists exemptions as
`repository:file:rule` (with `*`). A finding is also silenced where it is, with a comment on its line or the one before: `# lint: ignore <rule> because ...`
(the `# monitor-lint: ignore ...` form of the monitor works too). A repository whose last count does not carry the figures shows "not verified" in the tab, never zero.

