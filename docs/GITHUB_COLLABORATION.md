<!--
=============================================================================
HYDRA-UMC / URTC Ecosystem - GitHub collaboration model
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
GPL-3.0 - see LICENSE.md
=============================================================================
-->

# GitHub collaboration model

## Single source of public technical documentation

`README.md`, its six translations and each repository's `docs/` directory are
the versioned technical source of truth. They are reviewed with the code and
checked by the project baseline. A GitHub Wiki must never copy protocol,
build, safety or API manuals from those files.

## One ecosystem Wiki, not fifty-five

Enable a Wiki only on `JuanenRac/JuanenRac`. Its purpose is navigation and
long-lived ecosystem context:

1. **Home:** what HYDRA-UMC and URTC are, the 47% global reference and the
   boundary between software readiness and hardware evidence.
2. **Architecture map:** links to HYDRA-UMC-OS, HYDRA-UMC-SDK, firmware,
   Server and the public dashboard.
3. **Operator glossary:** terms such as CM5, URTC, bridge, fail-safe and
   maturity labels.
4. **Decision log:** concluded cross-repository decisions, each linking back
   to its issue, pull request or versioned document.

The Wiki is a navigation layer. When it needs a technical detail, it links to
the canonical repository file instead of duplicating it.

## Central GitHub Project: HYDRA-UMC Roadmap

Create one organization/account Project named **HYDRA-UMC Roadmap**. Add the
following fields:

| Field | Type | Purpose |
| --- | --- | --- |
| Repository | text | Exact affected repository name. |
| Family | single select | Manifest family, such as Platform Foundation or External Automation Bridges. |
| Maturity | single select | Scaffolding, Functional, Established, Production. |
| Evidence | single select | Local software, Simulator, CM5, MCU, Machine, Safety validation. |
| Hardware dependency | single select | None, CM5, MCU, Vision/Hailo, Robot/actuator, External machine. |
| Priority | single select | Critical, High, Normal, Low. |
| Blocked by | text | Issue, pull request, delivery or physical dependency. |

Use three views: **Software 95%**, **Awaiting hardware**, and **Safety
validation**. Do not use a Project field to declare a physical feature done
without an evidence link.

## Issues, pull requests and Discussions

The central issue forms in `.github/ISSUE_TEMPLATE/` collect reproducible
software defects, controlled hardware validation, improvements and public
documentation corrections. The pull-request template keeps versioning,
translations and safety boundaries visible during review. The matching
discussion forms in `.github/DISCUSSION_TEMPLATE/` guide announcements,
questions, ideas, integration validation and documentation conversations.

The synchronization workflow validates these shared templates before it writes
to a project. Its template-only commits carry `[skip ci]`, so they do not
launch a full project build for an administrative metadata-only update.

Enable Discussions only on `JuanenRac/JuanenRac` (or a future dedicated
community repository), never across every component. Recommended categories:

- **Announcements** for releases and dashboard changes.
- **Ideas** for architecture proposals before they become bounded issues.
- **Q&A** for public support, with accepted answers.
- **Integrations & Validation** for compatibility and evidence-based tests.
- **Documentation & Ecosystem** for public architecture and catalogue topics.

Issues remain for actionable, traceable work; Discussions remain for open
conversation and decisions.

## Releases and update channels

Create a GitHub Release only for an artefact that can be downloaded and
verified: APK, Wear APK, desktop package, CLI archive, firmware package or
future HYDRA-UMC-OS image/profile bundle. Every release must contain:

1. A tag matching the manifest version.
2. Human release notes derived from `CHANGELOG.md`.
3. The artefact and a `SHA256SUMS.txt` file.
4. Explicit target/platform and rollback or compatibility notes.
5. No credentials, machine backups, private logs or hardware claims not
   evidenced by a controlled test.

Android Control may use public release metadata as its update feed only after
the APK signature, package identifier and version checks succeed locally.

## Shared automation boundary

The current per-project CI keeps each stack's test command explicit. A future
reusable workflow may centralize only the deterministic common baseline;
firmware, Android, Rust, Flutter and bridge-specific tests remain in their
own repositories. Any caller must pin the reusable workflow deliberately and
retain least-privilege permissions.
