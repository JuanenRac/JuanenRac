# HYDRA-UMC / URTC Ecosystem Versions

Quick-reference index of the current version of each of the 12 core
projects. All of them follow the same ecosystem-wide versioning policy:
**incremental on every real build**, with a base-10 "odometer" carry rule —
patch goes up by 1; if it passes 9, it resets to 0 and minor goes up by 1
(e.g. `1.1.9` → `1.2.0`, never `1.1.10`); if minor also passes 9 after that
carry, the same rule bumps major. No component in any project is static
anymore.

This file is a snapshot for quick lookup — the real source of truth for
each version always lives in the project itself (see the "Source" column).
It is not updated automatically on every build; refresh it by hand when you
want an up-to-date snapshot, or check the source directly.

## HYDRA-UMC (firmware — Robot Controller Board G474 + Kinematic Brain H745)

| Component | Version | Source |
|---|---|---|
| Robot Controller Board (G474) — firmware | 1.0.6 | `HYDRA-UMC/src/.../firmware_common.h` |
| Robot Controller Board (G474) — bootloader | 1.0.6 | `HYDRA-UMC/src/.../bootloader_common.h` |
| Kinematic Brain (H745, CM7) — firmware | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM7) — bootloader | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM4) — firmware | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM4) — bootloader | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |

All 6 components are incremental (application and bootloader alike),
`bump_version.py` + `build_firmware.sh`/`.bat` mechanism.

## URTC (firmware — Universal Robot Tool Controller)

| Component | Version | Source |
|---|---|---|
| Main board — application firmware | 1.1.8 | `URTC/src/F303-master/firmware_common.h` |
| Main board — bootloader | 1.2.7 | `URTC/src/F303-master/boot/bootloader_common.h` |
| Expansion slave — application firmware | 1.0.7 | `URTC/src/F303-slave/slave_common.h` |
| Expansion slave — bootloader | 1.1.0 | `URTC/src/F303-slave/boot/slaveboot_common.h` |

All 4 components are incremental. Each bootloader also keeps its own
synced copy of the matching application's `FIRMWARE_VERSION_*`
(`bump_version.py`'s own mirroring mechanism, see `URTC/CHANGELOG.md`).

## Software / apps

| Project | Version | Source |
|---|---|---|
| HYDRA-UMC-STUDIO (web client, React/Vite) | 1.0.6 | `HYDRA-UMC-STUDIO/package.json` |
| HYDRA-UMC-SERVER (backend, Node/Express) | 1.0.3 | `HYDRA-UMC-SERVER/package.json` |
| URTC-WEB-STUDIO (Web Serial CAN Tester) | 1.1.8 | `URTC-WEB-STUDIO/package.json` |
| HYDRA-UMC-ANDROID-CONTROL | 1.0.9 (versionCode 10) | `HYDRA-UMC-ANDROID-CONTROL/app/version.properties` |
| HYDRA-UMC-IOS-CONTROL (Flutter) | 1.0.4+5 | `HYDRA-UMC-IOS-CONTROL/pubspec.yaml` |
| HYDRA-UMC-DSI (Flutter) | 1.0.2+3 | `HYDRA-UMC-DSI/pubspec.yaml` |
| HYDRA-UMC-SUITE (Python/PySide6) | 0.1.2 | `HYDRA-UMC-SUITE/hydra_suite/__init__.py` |
| HYDRA-UMC-EDITOR-URDF (Python/PySide6) | 1.0.0 | `HYDRA-UMC-EDITOR-URDF/hydra_editor_urdf/__init__.py` |
| URTC-FLASHER (Python/tkinter) | 1.1.0 | `URTC-FLASHER/flasher_config.py` |
| URTC-TESTER (Python/tkinter) | 1.1.0 | `URTC-TESTER/tester_config.py` |
| HYDRA-UMC-UPDATER (Python/tkinter) | 0.0.4 | `HYDRA-UMC-UPDATER/src/hydra_umc_updater/__init__.py` |

## New projects (scaffolding stage)

These new projects are cataloged in this same repo (`README.md`, "Project
Catalog" section). All of them start at **1.0.0**, same incremental policy
as the rest. As things stand, they're scaffolding only (the owner's own
template: `.git`, README + 4 translations, community-health files, empty
folders) — the real version "Source" (`package.json`/`Cargo.toml`/
`go.mod`/`version.h` depending on the stack) doesn't exist yet for most of
them; it gets created once each project reaches its turn in the internal
work plan. This table will be updated with the real source as that
happens.

| Project | Version | Decided stack | Source |
|---|---|---|---|
| HYDRA-UMC-TOOL-CLI | 1.0.0 | Go | *(pending)* |
| HYDRA-UMC-DASHBOARD-AI | 1.0.0 | TypeScript/React | *(pending)* |
| HYDRA-UMC-MQTT-BROKER | 1.0.0 | Node/TypeScript | *(pending)* |
| HYDRA-UMC-PRODUCTION-REPORTS | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-MTCONNECT-ADAPTER | 1.0.0 | Node/TypeScript | *(pending)* |
| HYDRA-UMC-OPCUA-SERVER | 1.0.0 | Node/TypeScript | *(pending)* |
| HYDRA-UMC-GATEWAY-INDUSTRIAL (parent) | 1.0.0 | Node/TypeScript | *(pending)* |
| HYDRA-UMC-TELEMETRY-COLLECTOR | 1.0.0 | Go | *(pending)* |
| HYDRA-UMC-NODE-HEALING | 1.0.0 | Go | *(pending)* |
| HYDRA-UMC-JOB-DISPATCHER | 1.0.0 | Go | *(pending)* |
| HYDRA-UMC-DATALAKE (parent) | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-DOCS-QA | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-VOICE-UI | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-WATCH | 1.0.0 | Kotlin (WearOS) | *(pending)* |
| HYDRA-UMC-SWARM-SYNC | 1.0.0 | Rust | *(pending)* |
| HYDRA-UMC-ANOMALY-DETECTOR | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-SEMANTIC-PLANNER | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-PATH-PLANNER-3D | 1.0.0 | Rust | *(pending)* |
| HYDRA-UMC-ORCHESTRATOR (parent) | 1.0.0 | Rust | *(pending)* |
| HYDRA-UMC-COGNITIVE-NODE (parent) | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-SYNTHETIC-DATA-GEN | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-VISUAL-SERVOING-API | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-SAFETY-ZONES | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-DETECTION-HEF | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-VISION-STREAMER | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-VISION-NODE (parent) | 1.0.0 | Python | *(pending)* |
| HYDRA-UMC-VLA-ENGINE | 1.0.0 | Python | *(pending)* |
| URTC-SMART-RACK | 1.0.0 | C (STM32G4) | *(pending)* |
| URTC-VISION-TOOL | 1.0.0 | C (STM32) + Python | *(pending)* |
| HYDRA-UMC-PHYSICS-REPLICA | 1.0.0 | Rust | *(pending)* |
| HYDRA-UMC-HIL-BRIDGE | 1.0.0 | Rust | *(pending)* |
| HYDRA-UMC-TWIN (parent) | 1.0.0 | Rust (Bevy) | *(pending)* |

These projects are being built one at a time, following an internal work
order (easiest/most fun → hardest).

## Bump mechanism per project

| Project | Bump script | Triggered by |
|---|---|---|
| HYDRA-UMC | `bump_version.py` | `build_firmware.sh`/`.bat` (each of the 6 components) |
| URTC | `bump_version.py` | `build_firmware.sh`/`.bat` (each of the 4 components) |
| HYDRA-UMC-STUDIO | `scripts/bump-version.mjs` | `npm run build` |
| HYDRA-UMC-SERVER | `scripts/bump-version.mjs` | `npm run build` |
| URTC-WEB-STUDIO | `scripts/bump-version.mjs` | `npm run build` |
| HYDRA-UMC-ANDROID-CONTROL | direct read/write on `app/build.gradle.kts` | any real Gradle build (configuration evaluation) |
| HYDRA-UMC-IOS-CONTROL | `tool/bump_version.dart` | `build.sh`/`build.bat` |
| HYDRA-UMC-DSI | `tool/bump_version.dart` | `build.sh`/`build.bat`/`build_linux.sh` |
| HYDRA-UMC-SUITE | `bump_version.py` | `build_exe.sh`/`.bat` |
| HYDRA-UMC-EDITOR-URDF | `bump_version.py` | `build_exe.sh`/`.bat` |
| URTC-FLASHER | `bump_version.py` | `build_exe.sh`/`.bat` |
| URTC-TESTER | `bump_version.py` | `build_exe.sh`/`.bat` |
| HYDRA-UMC-UPDATER | `bump_version.py` | `build.sh`/`.bat` |

Full detail on each mechanism, history, and policy lives in each project's
own `CHANGELOG.md`.
