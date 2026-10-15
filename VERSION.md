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
want an up-to-date snapshot, or check the source directly. The live
dashboard (https://juanenrac.github.io/JuanenRac/) always shows the
current version of every project.

Snapshot taken 2026-10-11 from each repository's own manifest and
`firmware/firmware_manifest.json`.

## HYDRA-UMC (firmware — Robot Controller Board G474 + Kinematic Brain H745)

| Component | Version | Source |
|---|---|---|
| Robot Controller Board (G474) — firmware | 0.1.5 | `HYDRA-UMC/src/.../firmware_common.h` |
| Robot Controller Board (G474) — bootloader | 0.1.4 | `HYDRA-UMC/src/.../bootloader_common.h` |
| Kinematic Brain (H745, CM7) — firmware | 0.1.3 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM7) — bootloader | 0.1.3 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM4) — firmware | 0.1.3 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM4) — bootloader | 0.1.3 | `HYDRA-UMC/firmware/firmware_manifest.json` |

All 6 components are incremental (application and bootloader alike),
`bump_version.py` + `build_firmware.sh`/`.bat` mechanism.

## URTC (firmware — Universal Robot Tool Controller)

| Component | Version | Source |
|---|---|---|
| Main board — application firmware | 0.3.3 | `URTC/src/F303-master/firmware_common.h` |
| Main board — bootloader | 0.3.8 | `URTC/src/F303-master/boot/bootloader_common.h` |
| Expansion slave — application firmware | 0.1.9 | `URTC/src/F303-slave/slave_common.h` |
| Expansion slave — bootloader | 0.2.2 | `URTC/src/F303-slave/boot/slaveboot_common.h` |

All 4 components are incremental. Each bootloader also keeps its own
synced copy of the matching application's `FIRMWARE_VERSION_*`
(`bump_version.py`'s own mirroring mechanism, see `URTC/CHANGELOG.md`).

## Software / apps

| Project | Version | Source |
|---|---|---|
| HYDRA-UMC-STUDIO (web client, React/Vite) | 0.7.6 | `HYDRA-UMC-STUDIO/package.json` |
| HYDRA-UMC-SERVER (backend, Node/Express) | 0.8.0.6 | `HYDRA-UMC-SERVER/package.json` |
| URTC-WEB-STUDIO (Web Serial CAN Tester) | 0.2.4 | `URTC-WEB-STUDIO/package.json` |
| HYDRA-UMC-ANDROID-CONTROL | 0.6.3 | `HYDRA-UMC-ANDROID-CONTROL/app/version.properties` |
| HYDRA-UMC-IOS-CONTROL (Flutter) | 0.2.0 | `HYDRA-UMC-IOS-CONTROL/pubspec.yaml` |
| HYDRA-UMC-DSI (Flutter) | 0.2.0 | `HYDRA-UMC-DSI/pubspec.yaml` |
| HYDRA-UMC-SUITE (Python/PySide6) | 0.6.4 | `HYDRA-UMC-SUITE/hydra_suite/__init__.py` |
| HYDRA-UMC-EDITOR-URDF (Python/PySide6) | 0.1.0 | `HYDRA-UMC-EDITOR-URDF/hydra_editor_urdf/__init__.py` |
| URTC-FLASHER (Python, Qt Quick + Tk) | 0.2.4 | `URTC-FLASHER/flasher_config.py` |
| URTC-TESTER (Python, Qt Quick + Tk) | 0.2.4 | `URTC-TESTER/tester_config.py` |
| HYDRA-UMC-UPDATER (Python) | 0.4.6 | `HYDRA-UMC-UPDATER/src/hydra_umc_updater/__init__.py` |
| URTC-UPDATER (Python) | 0.0.7 | `URTC-UPDATER/src/urtc_updater/__init__.py` |

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
| HYDRA-UMC-TOOL-CLI | 1.0.0 | Go | *(in development)* |
| HYDRA-UMC-DASHBOARD-AI | 1.0.0 | TypeScript/React | *(in development)* |
| HYDRA-UMC-MQTT-BROKER | 1.0.0 | Node/TypeScript | *(in development)* |
| HYDRA-UMC-PRODUCTION-REPORTS | 1.0.0 | Python | *(in development)* |
| HYDRA-UMC-MTCONNECT-ADAPTER | 1.0.0 | Node/TypeScript | *(in development)* |
| HYDRA-UMC-OPCUA-SERVER | 1.0.0 | Node/TypeScript | *(in development)* |
| HYDRA-UMC-GATEWAY-INDUSTRIAL (parent) | 1.0.0 | Node/TypeScript | *(in development)* |
| HYDRA-UMC-TELEMETRY-COLLECTOR | 1.0.0 | Go | *(in development)* |
| HYDRA-UMC-NODE-HEALING | 1.0.0 | Go | *(in development)* |
| HYDRA-UMC-JOB-DISPATCHER | 1.0.0 | Go | *(in development)* |
| HYDRA-UMC-DATALAKE (parent) | 1.0.0 | Python | *(in development)* |
| HYDRA-UMC-DOCS-QA | 1.0.0 | Python | *(in development)* |
| HYDRA-UMC-VOICE-UI | 0.1.3 | Python | *(in development)* |
| HYDRA-UMC-WATCH | 0.2.2 | Kotlin (WearOS) | *(in development)* |
| HYDRA-UMC-SWARM-SYNC | 0.1.1 | Rust | *(in development)* |
| HYDRA-UMC-ANOMALY-DETECTOR | 0.1.3 | Python | *(in development)* |
| HYDRA-UMC-SEMANTIC-PLANNER | 0.1.0 | Python | *(in development)* |
| HYDRA-UMC-PATH-PLANNER-3D | 0.0.7 | Rust | *(in development)* |
| HYDRA-UMC-ORCHESTRATOR (parent) | 0.1.3 | Rust | *(in development)* |
| HYDRA-UMC-COGNITIVE-NODE (parent) | 0.1.1 | Python | *(in development)* |
| HYDRA-UMC-SYNTHETIC-DATA-GEN | 0.0.8 | Python | *(in development)* |
| HYDRA-UMC-VISUAL-SERVOING-API | 0.1.4 | Python | *(in development)* |
| HYDRA-UMC-SAFETY-ZONES | 0.1.1 | Python | *(in development)* |
| HYDRA-UMC-DETECTION-HEF | 0.0.9 | Python | *(in development)* |
| HYDRA-UMC-VISION-STREAMER | 0.1.6 | Python | *(in development)* |
| HYDRA-UMC-VISION-NODE (parent) | 0.1.0 | Python | *(in development)* |
| HYDRA-UMC-VLA-ENGINE | 0.1.4 | Python | *(in development)* |
| URTC-SMART-RACK | 0.1.1 | C (STM32G4) | *(in development)* |
| URTC-VISION-TOOL | 0.0.5 | C (STM32) + Python | *(in development)* |
| HYDRA-UMC-PHYSICS-REPLICA | 0.0.6 | Rust | *(in development)* |
| HYDRA-UMC-HIL-BRIDGE | 0.0.6 | Rust | *(in development)* |
| HYDRA-UMC-TWIN (parent) | 0.0.7 | Rust (Bevy) | *(in development)* |

These projects are being built one at a time, following an internal work
order (easiest/most fun → hardest).

## Bump mechanism per project

| Project | Bump script | Triggered by |
|---|---|---|
| HYDRA-UMC | `bump_version.py` | `build_firmware.sh`/`.bat` (each of the 6 components) |
| URTC | `bump_version.py` | `build_firmware.sh`/`.bat` (each of the 4 components) |
| HYDRA-UMC-STUDIO | `scripts/bump-version.mjs` | `npm run build` |
| HYDRA-UMC-SERVER | `scripts/bump-version.mjs` | `npm run build` |
| URTC-WEB-STUDIO | `bump_manifest_version.py` | `build.sh`/`.bat` |
| HYDRA-UMC-ANDROID-CONTROL | direct read/write on `app/build.gradle.kts` | any real Gradle build (configuration evaluation) |
| HYDRA-UMC-IOS-CONTROL | `tool/bump_version.dart` | `build.sh`/`build.bat` |
| HYDRA-UMC-DSI | `tool/bump_version.dart` | `build.sh`/`build.bat`/`build_linux.sh` |
| HYDRA-UMC-SUITE | `bump_version.py` | `build_exe.sh`/`.bat` |
| HYDRA-UMC-EDITOR-URDF | `bump_version.py` | `build_exe.sh`/`.bat` |
| URTC-FLASHER | `bump_version.py` | `build_exe.sh`/`.bat` |
| URTC-TESTER | `bump_version.py` | `build_exe.sh`/`.bat` |
| HYDRA-UMC-UPDATER | `bump_version.py` | `build.sh`/`.bat` |
| URTC-UPDATER | `bump_version.py` | `build.sh`/`.bat` |
| URTC-SMART-RACK | `bump_version.py` | `build_firmware.sh`/`.bat` |
| URTC-VISION-TOOL | `bump_version.py` | `build_firmware.sh`/`.bat` |

Full detail on each mechanism, history, and policy lives in each project's
own `CHANGELOG.md`.
