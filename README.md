<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

# HYDRA-UMC / URTC Ecosystem 🤖🚀

<p align="center">
  🇺🇸 <b>English</b> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Welcome to the **HYDRA-UMC Ecosystem**, a multi-layered industrial robotics platform spanning from low-level real-time firmware to high-level cognitive AI. This organization hosts many specialized projects designed to work in perfect synchrony for micro-factory automation and swarm robotics.

## 📈 Ecosystem Progress

`[████████░░░░░░░░░░░░] 40%` — Reference only. The 100% milestone is a fully integrated ecosystem operating on real hardware.

---

## 🚀 Key Features & Scalability

- **Multi-Robot Scalability**: Supports up to 8 distributed robotic units (3, 4, 5, and 6-DOF today; scaling up to 7, 8, 9-DOF and Dual-Robot architectures in future releases).
- **Integrated Local Stage**: The main HYDRA-UMC board features an onboard **6-axis Local Stage** for auxiliary tasks, including secondary robots, ATC (Automatic Tool Changer) revolvers, conveyor belt synchronization, or XYZ table gantries.

---

## 🏗️ Ecosystem Architecture

The v1.1 ecosystem is a layered product platform: it builds on established Linux and Raspberry Pi technology instead of creating a new operating system or replacing vendor APIs.

1.  **Platform base**: Raspberry Pi OS ARM64 and standard Linux services provide the supported CM5 foundation.
2.  **Platform and contracts**: **HYDRA-UMC-OS** packages reproducible profiles, services, diagnostics and updates on Raspberry Pi OS; **HYDRA-UMC-SDK** publishes versioned contracts, thin clients and conformance fixtures.
3.  **Real-time execution**: **HYDRA-UMC** firmware and URTC control on STM32/MCU own motion limits, watchdogs and safe stop.
4.  **Coordination and operations**: Server services, job dispatching, telemetry and configuration coordinate devices without bypassing the MCU safety boundary.
5.  **Operator interfaces**: Studio, Suite, DSI, web, desktop, mobile and CLI clients use the SDK contracts.
6.  **Perception and intelligence**: Vision, Hailo and cognitive services propose observations or plans; they have no physical safety authority.
7.  **Engineering, industrial and data**: Digital Twin, HIL/physics, OPC-UA/MQTT/MTConnect gateways and data services validate and integrate the system.

For implementation guidance, start with the public architecture and service documentation in **HYDRA-UMC-OS**, then use the contracts and conformance rules in **HYDRA-UMC-SDK**. The MCU/URTC safety authority is preserved throughout every flow.

---

## 🛠️ Technology Stack & Tools

The ecosystem leverages a modern, high-performance stack for mission-critical reliability:

### 💠 Embedded & Real-Time (Execution)
- **Microcontrollers**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Frameworks**: FreeRTOS (AMP mode), CMSIS-DSP, STM32 HAL/LL.
- **Protocols**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (50MHz Slave IPC), I2C, UART.
- **Kinematics**: S-Curve Profile Generation, Real-time Inverse Kinematics (IK).

### 🧠 Edge AI & Perception (Intelligence)
- **Accelerators**: Hailo-8 (26 TOPS) for 8x Camera Vision, Hailo-10 (40 TOPS) for GenAI.
- **Models**: YOLOv10 (Detection), OpenVLA (Action), Whisper (Voice), Llama-3 (Reasoning).
- **Inter-node**: gRPC over Protobuf and high-speed SPI-DMA metadata exchange.

### 🌐 Backend & Coordination (Coordination)
- **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orchestrator), Go (CLI).
- **Infrastructure**: Express, Fastify, Socket.io (WebSocket), gRPC.
- **Database**: InfluxDB/TimescaleDB (Telemetry), Redis (State), SQLite.

### 💻 Dashboards & User Interface (Interface)
- **Web**: React 19, Vite, Three.js (3D Viewport), Tailwind CSS.
- **Native**: Python 3.12/PySide6 (Suite), Kotlin (Android Native), Flutter 3.x (iOS & DSI).

---

## 📋 System Requirements

- **Compute Node**: Raspberry Pi CM5 (4GB+ RAM) with NVMe/eMMC storage.
- **AI Hardware**: Hailo-8/Hailo-10 M.2 modules (Key M).
- **Fieldbus**: Gigabit Ethernet for LAN and FDCAN (ISO 11898-1:2015) for actuators.
- **Client OS**: Android 10+, iOS 15+, Windows 10/11 (High-DPI), Ubuntu 22.04 LTS.

---

## 🔒 Industrial Safety & Security

- **E-STOP Layer**: Hard-wired emergency line + High-priority CAN emergency frames (<1ms).
- **AI Safety**: 3D Safety Zones with automatic motor torque-cut upon human intrusion.
- **Cybersecurity**: JWT-based stateless auth + mTLS for secure inter-node traffic.
- **Integrity**: Non-volatile F-RAM for tool lifecycle audit and state recovery.

---

## 🔧 Hardware Hacking: Building Your Own Carrier

The Robot Controller Board is built around a **Raspberry Pi CM5**, and CM5's own dual Hirose DF40 connector is a fixed, official, public pinout (Table 5 of Raspberry Pi's own CM5 datasheet) - not something this project defines. That means a compatible third-party carrier is a real, achievable project, not a reverse-engineering exercise:

- **Start here**: [`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - which of CM5's fixed pins this board actually uses (Ethernet, the 2 native USB3 SuperSpeed PHYs, the CM5-side cooling fan header) and why, reorganized by function from the official pinout table.
- **The easy on-ramp**: the standard **Raspberry Pi 40-pin GPIO header** (the same "B+" layout unchanged since 2014) is broken out on this board exactly like any Raspberry Pi - existing RPi HATs and GPIO tooling work unmodified. A handful of positions that this board's own STM32 link already uses are silkscreened/noted so you know which ones to skip.
- **Going further**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) covers how the CM5, the STM32H745 "Kinematic Brain", and the STM32G474 "Robot Controller" actually talk to each other (SPI1 + FDCAN1 + the CM7↔CM4 IPC mailbox) - the layer a carrier redesign would need to preserve if it's meant to stay compatible with this project's own firmware.
- Every pinout doc states plainly whether it's **CONFIRMED** (taken directly from an official datasheet table) or **PROPOSED** (this project's own routing choice, open to a different one on a derivative carrier) - read that status line before treating a signal assignment as fixed.

This isn't a guided tutorial (there's no single "right" carrier for every use case) - it's the real reference material an experienced hardware designer needs to start from a known-good pin map instead of a datasheet alone.

---

## 📁 Project Catalog

New to the ecosystem? `./starter-kit.sh` (or `starter-kit.bat` on
Windows) clones 13 core repositories - a hand-picked starting set, not
the full catalog below - as siblings in one directory: the standard
layout every cross-repo script here already assumes. Re-running it is
safe: anything already cloned is left untouched. From there,
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(one of the 13 just cloned) can check versions and build/update any of
the other projects in the full catalog below.

### 🧱 Platform Foundation & Contracts
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | Raspberry Pi OS platform layer for CM5: reproducible profiles, configuration, diagnostics, service lifecycle and updates; not a new Linux distribution. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | Shared versioned contracts, thin clients and conformance fixtures for services, UIs, CM5 adapters and URTC; it does not replace vendor APIs. |

### 💠 Core Control & Operator Clients
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | Core motion control firmware for STM32H745/G474 with S-Curve kinematics. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | Headless Node.js API and WebSocket backend for robotic orchestration. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | Advanced React-based web dashboard for 3D robot monitoring and control. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | High-performance Python/Qt desktop application for industrial automation. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | Dedicated Flutter-based touch interface for 7" industrial displays (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | Native Kotlin mobile app with biometric login for remote robot management. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | Flutter mobile app for iOS/iPadOS with real-time WebSocket sync. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | Graphical URDF editor to validate and push robot models to the catalog. |


### 🔧 URTC Core & Tooling
| Repository | Description |
| :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | Universal Robot Tool Controller firmware for 25+ specialized tools. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | GUI tool for CAN-OTA and full-chip SWD/JTAG firmware updates. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Diagnostic tool for real-time validation of URTC tool profiles over CAN. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Browser-based Web Serial tool for instant hardware testing and analysis. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | Intelligent tool storage with automatic pre-heating and lifecycle audit. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | Toolhead with integrated thermal and RGB cameras for active QA. |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | High-speed perception node for 8x simultaneous USB 3.0 camera streams. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | Optimized GStreamer/MediaMTX pipeline for industrial video relay. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | Library of hardware-accelerated YOLO models for SMD and component QA. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | Real-time AI intrusion detection for robotic work volume protection. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | Image-based kinematic feedback for sub-millimetric pose correction. |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | Semantic reasoning node for logical mission planning and voice control. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | Vision-Language-Action model implementation for complex task execution. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | Local, private STT/TTS pipeline for natural language operator interaction. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | LLM-based mission orchestrator with context-aware error recovery. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | RAG-based AI assistant trained on technical manuals and source code. |

### 🐝 Orchestration & Swarm
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | Fleet manager for multi-robot coordination and collision avoidance. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | PTP (Precision Time Protocol) sync for nanosecond robot synchronization. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | Distributed path optimizer for shared workspace robotic enjambres. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | Priority-based task scheduler for heterogeneous robot fleets. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | High-availability monitor with transparent mission failover. |

### 🎮 Digital Twin & Simulation
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | High-fidelity physics simulation engine for risk-free robot testing. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | Real-world physics simulation (MuJoCo/PhysX) of URDF chains. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | Hardware-in-the-loop interface for real-vs-virtual command syncing. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | Procedural generator of training datasets for Vision nodes. |

### 📊 Data & Analytics
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | Big Data storage for massive industrial robotic data. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | High-throughput ingester for CAN, WebSocket, and system logs. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | Predictive maintenance engine based on motor vibration signatures. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | Automated OEE and KPI generation for industrial plant management. |

### 🏭 Industrial Gateway
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | Industry 4.0 interoperability bridge for factory standards (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | Mapping of HydraState robotic objects to standard OPC-UA nodes. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | Telemetry bridge for IoT integrations and external dashboards. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | Standardized interface for machine tool and robot health monitoring. |

### 🌉 External Automation Bridges
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | Bidirectional ROS 2 coordination boundary: topics for observation, services for inspection and cancellable actions for cell jobs. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | Traceable PCB hand-off coordinator for OpenPnP and robot-assisted loading or unloading. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | Safe bridge around native 3D-printer software; first adapter validates Moonraker readiness without replacing firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | CNC cell auxiliary coordinator; controller trajectory and machine safety remain native. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | Laser-cell auxiliary coordinator that cannot arm, fire or override laser interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | Coordination boundary for legged/humanoid droids: named walk/pick/place action vocabulary gated through the shared safety contract; gait and balance stay on the droid's own controller. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | Coordination boundary for AGV/AMR fleets: factory-to-local frame transform plus a VDA-5050-inspired order vocabulary; path planning stays with the AMR's own navigation. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | Coordination boundary for camera-equipped UAVs: named flight-request vocabulary plus a deterministic heartbeat/link-loss failsafe watchdog. |

### 🛠️ Complementary Tools
| Repository | Description |
| :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | Wearable emergency dashboard with haptic safety alerts. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | Command-line interface for fleet automation, flashing, and devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | AI extension for web dashboards providing natural language insights. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | Cross-platform GUI/CLI tool to detect, install, and manually update every ecosystem project. |

---

## 🤝 Contributing
This ecosystem is part of a high-tech robotic initiative. Each project has its own contribution guidelines. Please refer to individual repositories for technical details.

Issue labels are standardized across all 45 repos from [`.github/labels.yml`](.github/labels.yml) in this same repo, synced out by [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - edit that one file to change a label everywhere at once, rather than by hand per repo.

A live status dashboard for all 46 repos (stack, deploy target, current version - read straight from each repo's own default branch) is generated daily by [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) and served from `docs/` via GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. v3 adds a real maturity classification per project (scaffolding / functional / established / production, each decided from that project's own CHANGELOG - see [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)'s own module docstring for exactly how), its role (API / UI / CLI / firmware / library / service / tool), a real family/parent-child tree, and per-project notes on what's actually implemented today.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.
