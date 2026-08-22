# Versiones del ecosistema HYDRA-UMC / URTC

Índice de la versión actual de cada uno de los 12 proyectos. Todos siguen la
misma política de versionado ecosistema-wide: **incremental en cada build
real**, con la regla de "cuentakilómetros" en base 10 — el patch sube en 1;
si pasa de 9, se resetea a 0 y la minor sube en 1 (p. ej. `1.1.9` → `1.2.0`,
nunca `1.1.10`); si la minor también pasara de 9 tras ese acarreo, la misma
regla sube la major. Ningún componente de ningún proyecto es ya estático.

Este archivo es un snapshot para consulta rápida — la fuente de verdad real
de cada versión vive siempre en el propio proyecto (ver la columna
"Fuente"). No se actualiza automáticamente en cada build; refléjalo a mano
cuando quieras una foto actualizada, o consulta la fuente directamente.

## HYDRA-UMC (firmware — Robot Controller Board G474 + Kinematic Brain H745)

| Componente | Versión | Fuente |
|---|---|---|
| Robot Controller Board (G474) — firmware | 1.0.6 | `HYDRA-UMC/src/.../firmware_common.h` |
| Robot Controller Board (G474) — bootloader | 1.0.6 | `HYDRA-UMC/src/.../bootloader_common.h` |
| Kinematic Brain (H745, CM7) — firmware | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM7) — bootloader | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM4) — firmware | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |
| Kinematic Brain (H745, CM4) — bootloader | 1.0.6 | `HYDRA-UMC/firmware/firmware_manifest.json` |

Los 6 componentes son incrementales (app y bootloader por igual), mecanismo
`bump_version.py` + `build_firmware.sh`/`.bat`.

## URTC (firmware — Universal Robot Tool Controller)

| Componente | Versión | Fuente |
|---|---|---|
| Main board — firmware de aplicación | 1.1.8 | `URTC/src/F303-master/firmware_common.h` |
| Main board — bootloader | 1.2.7 | `URTC/src/F303-master/boot/bootloader_common.h` |
| Expansion slave — firmware de aplicación | 1.0.7 | `URTC/src/F303-slave/slave_common.h` |
| Expansion slave — bootloader | 1.1.0 | `URTC/src/F303-slave/boot/slaveboot_common.h` |

Los 4 componentes son incrementales. Cada bootloader mantiene además su
propia copia sincronizada de `FIRMWARE_VERSION_*` de la app correspondiente
(mecanismo de espejo de `bump_version.py`, ver `URTC/CHANGELOG.md`).

## Software / apps

| Proyecto | Versión | Fuente |
|---|---|---|
| HYDRA-UMC-STUDIO (cliente web, React/Vite) | 1.0.6 | `HYDRA-UMC-STUDIO/package.json` |
| HYDRA-UMC-SERVER (backend, Node/Express) | 1.0.3 | `HYDRA-UMC-SERVER/package.json` |
| URTC-WEB-STUDIO (Web Serial CAN Tester) | 1.1.8 | `URTC-WEB-STUDIO/package.json` |
| HYDRA-UMC-ANDROID-CONTROL | 1.0.9 (versionCode 10) | `HYDRA-UMC-ANDROID-CONTROL/app/version.properties` |
| HYDRA-UMC-IOS-CONTROL (Flutter) | 1.0.4+5 | `HYDRA-UMC-IOS-CONTROL/pubspec.yaml` |
| HYDRA-UMC-DSI (Flutter) | 1.0.2+3 | `HYDRA-UMC-DSI/pubspec.yaml` |
| HYDRA-UMC-SUITE (Python/PySide6) | 0.1.2 | `HYDRA-UMC-SUITE/hydra_suite/__init__.py` |
| HYDRA-UMC-EDITOR-URDF (Python/PySide6) | 1.0.0 | `HYDRA-UMC-EDITOR-URDF/hydra_editor_urdf/__init__.py` |
| URTC-FLASHER (Python/tkinter) | 1.1.0 | `URTC-FLASHER/flasher_config.py` |
| URTC-TESTER (Python/tkinter) | 1.1.0 | `URTC-TESTER/tester_config.py` |

## Mecanismo de bump por proyecto

| Proyecto | Script de bump | Disparado por |
|---|---|---|
| HYDRA-UMC | `bump_version.py` | `build_firmware.sh`/`.bat` (cada uno de los 6 componentes) |
| URTC | `bump_version.py` | `build_firmware.sh`/`.bat` (cada uno de los 4 componentes) |
| HYDRA-UMC-STUDIO | `scripts/bump-version.mjs` | `npm run build` |
| HYDRA-UMC-SERVER | `scripts/bump-version.mjs` | `npm run build` |
| URTC-WEB-STUDIO | `scripts/bump-version.mjs` | `npm run build` |
| HYDRA-UMC-ANDROID-CONTROL | lectura/escritura directa en `app/build.gradle.kts` | cualquier build Gradle real (evaluación de configuración) |
| HYDRA-UMC-IOS-CONTROL | `tool/bump_version.dart` | `build.sh`/`build.bat` |
| HYDRA-UMC-DSI | `tool/bump_version.dart` | `build.sh`/`build.bat`/`build_linux.sh` |
| HYDRA-UMC-SUITE | `bump_version.py` | `build_exe.sh`/`.bat` |
| HYDRA-UMC-EDITOR-URDF | `bump_version.py` | `build_exe.sh`/`.bat` |
| URTC-FLASHER | `bump_version.py` | `build_exe.sh`/`.bat` |
| URTC-TESTER | `bump_version.py` | `build_exe.sh`/`.bat` |

Detalle completo de cada mecanismo, historial y política en el
`CHANGELOG.md` de cada proyecto.
