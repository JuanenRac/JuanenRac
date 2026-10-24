<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Electro Hobby 3D Banner" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  🇺🇸 <b>English</b> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

Four independent engineering ecosystems, one author. **HYDRA-UMC** is a multi-layered industrial robotics platform, from real-time firmware to cognitive AI. **URTC** is its universal robot-tool subsystem: real-time firmware and desktop/web tooling for a robot's own end-effector, developed as its own product with independent versioning and maintenance tools. **A.R.M.O.R.** is a separate, public perimeter-security and home-automation ecosystem - radar presence detection, solar and electrical monitoring, and a central coordinator with web and mobile clients. **EH3D Fabrication Suite** is an integrated software ecosystem for PCB prototyping, CAM processing, computer vision inspection, Pick & Place management, and CNC/Laser control interfacing with HYDRA-UMC hardware and specialized workshop machinery.


## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Dashboard and monitors | 🟢 | The status dashboard, the CI watch, the health matrix, the link check and the release digest run on a schedule in GitHub Actions, and their latest runs pass. |
| Tests | 🟢 | 44 tests pass (`python -m unittest discover -s tests`): the catalogue, the monitors, the banners, the roadmap seed and the README parity. |
| Catalogue and versions | 🟡 | The Version column of every project table is filled from each repository's own manifest by a script and checked, so it does not go stale; the one-line descriptions are written by hand. |
| Progress bars | 🟠 | The percentages under each ecosystem are set by hand and are reference only: the 100% milestone is a fully integrated ecosystem working on real hardware. |
| Eight-language parity | 🟢 | The eight README files keep the same sections, the same GitHub links and the same number of table rows, and a test fails when one of them drifts. |
| Real hardware | 🟢 | Not applicable: this repository holds the profile and its automation, nothing here runs on hardware. |
| Documentation | 🟢 | README in eight languages with the four ecosystems, the guide to the collaboration on GitHub and the community files. |

## 🧭 About Electro Hobby 3D and its updater

**Electro Hobby 3D** is the workshop of JuanenRac: electronics, robotics and software that are designed, built, programmed and tested in one place. Every repository describes itself with a manifest, carries its own documentation and says what has and has not been tried on real hardware.

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) is **the updater of the four ecosystems**: one window and one command line that hand over to the updater of each ecosystem, and those are the ones that discover, install and update its repositories. Every ecosystem below names its own updater.

| Ecosystem | What it is | Updater |
|---|---|---|
| **HYDRA-UMC** | Industrial robotics and machine control, from real-time firmware to cognitive AI | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | Firmware and tools for a robot's end-effectors | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | Perimeter security and home automation | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | PCB prototyping, CAM, CNC and laser, pick and place | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Welcome to the **HYDRA-UMC Ecosystem**, a multi-layered industrial robotics platform spanning from low-level real-time firmware to high-level cognitive AI. This organization hosts many specialized projects designed to work in perfect synchrony for micro-factory automation and swarm robotics.

**Updater:** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) detects, installs and updates the repositories of this ecosystem; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) does it for all four.

## 📈 Ecosystem Progress

`[██████████▊░░░░░░░░░] 54%` — Reference only. The 100% milestone is a fully integrated ecosystem operating on real hardware.

> [!IMPORTANT]
> 🛠️ **Project on hold — building the real hardware.** Active development is paused while the physical robotics cell (frames, wiring, the real CM5 and STM32 boards) gets built for real, so the next phase of work has actual hardware to run and validate against, not just a bar going up. Work picks back up once that build is in place.

---

## 🚀 Key Features & Scalability

- **Multi-Robot Scalability**: Supports up to 8 distributed robotic units (3, 4, 5, and 6-DOF today; scaling up to 7, 8, 9-DOF and Dual-Robot architectures in future releases).
- **Integrated Local Stage**: The main HYDRA-UMC board features an onboard **6-axis Local Stage** for auxiliary tasks, including secondary robots, ATC (Automatic Tool Changer) revolvers, conveyor belt synchronization, or XYZ table gantries.

---

## 🏗️ Ecosystem Architecture

The v1.1 ecosystem is a layered product platform: it builds on established Linux and Raspberry Pi technology instead of creating a new operating system or replacing vendor APIs.

1.  **Platform base**: Raspberry Pi OS ARM64 and standard Linux services provide the supported CM5 foundation.
2.  **Platform and contracts**: **HYDRA-UMC-OS** packages reproducible profiles, services, diagnostics and updates on Raspberry Pi OS; **HYDRA-UMC-SDK** publishes versioned contracts, thin clients and conformance fixtures.
3.  **Real-time execution**: **HYDRA-UMC** firmware owns motion limits, watchdogs and safe stop on STM32/MCU; the tool itself, and its own real-time authority over the end-effector, belongs to the separate **URTC** ecosystem below.
4.  **Coordination and operations**: Server services, job dispatching, telemetry and configuration coordinate devices without bypassing the MCU safety boundary.
5.  **Operator interfaces**: Studio, Suite, DSI, web, desktop, mobile and CLI clients use the SDK contracts.
6.  **Perception and intelligence**: Vision, Hailo and cognitive services propose observations or plans; they have no physical safety authority.
7.  **Engineering, industrial and data**: Digital Twin, HIL/physics, OPC-UA/MQTT/MTConnect gateways and data services validate and integrate the system.

For implementation guidance, start with the public architecture and service documentation in **HYDRA-UMC-OS**, then use the contracts and conformance rules in **HYDRA-UMC-SDK**. The MCU safety authority is preserved throughout every flow.

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

## 📁 HYDRA-UMC Project Catalog

New to the ecosystem? `./starter-kit.sh` (or `starter-kit.bat` on
Windows) clones 13 core repositories - a hand-picked starting set - as
siblings in one directory: the standard layout every cross-repo script
here already assumes. A second argument clones a whole ecosystem instead,
discovered live by its manifest: `hydra-umc`, `urtc`, `armor`, `eh3d` or `all`
(for example `./starter-kit.sh ~/work armor`). Re-running it is safe:
anything already cloned is left untouched. From there, each ecosystem's
own updater - or [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)
for all four - can check versions and build/update any other project.

### 🧱 Platform Foundation & Contracts
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.5.3 | Raspberry Pi OS platform layer for CM5: reproducible profiles, configuration, diagnostics, service lifecycle and updates; not a new Linux distribution. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.3.6 | Shared versioned contracts, thin clients and conformance fixtures for services, UIs and CM5 adapters; it does not replace vendor APIs. |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.4 | Declarative adapter-manifest registry and validator for external-machine connectors; extends the SDK's own contract idea to external machines without replacing the industrial-gateway projects. |

### 💠 Core Control & Operator Clients
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.2.2 | Core motion control firmware for STM32H745/G474 with S-Curve kinematics. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.1.1 | Headless Node.js API and WebSocket backend for robotic orchestration. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.8.0.1 | Advanced React-based web dashboard for 3D robot monitoring and control. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.7.0 | High-performance Python/Qt desktop application for industrial automation. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.6 | Dedicated Flutter-based touch interface for 7" industrial displays (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.7.1 | Native Kotlin mobile app with biometric login for remote robot management. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.6 | Flutter mobile app for iOS/iPadOS with real-time WebSocket sync. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.4 | Graphical URDF editor to validate and push robot models to the catalog. |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.6 | Desktop STL model editor - transform, replace, remove and add real parts in the shared model catalog. |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.5 | High-speed perception node for 8x simultaneous USB 3.0 camera streams. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.2.0 | Optimized GStreamer/MediaMTX pipeline for industrial video relay. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.1.4 | Library of hardware-accelerated YOLO models for SMD and component QA. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.4 | Real-time AI intrusion detection for robotic work volume protection. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.9 | Image-based kinematic feedback for sub-millimetric pose correction. |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.4 | Semantic reasoning node for logical mission planning and voice control. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.7 | Vision-Language-Action model implementation for complex task execution. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.7 | Local, private STT/TTS pipeline for natural language operator interaction. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.3 | LLM-based mission orchestrator with context-aware error recovery. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.4 | RAG-based AI assistant trained on technical manuals and source code. |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.6 | Local, policy-gated AI maintenance technician: a fixed risk-level policy and tool allowlist today, with a real, tested defense proving a malicious retrieved document can never trigger a tool call or leak a secret - the AI never gets authority by generating a response. |

### 🐝 Orchestration & Swarm
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.8 | Fleet manager for multi-robot coordination and collision avoidance. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.4 | PTP (Precision Time Protocol) sync for nanosecond robot synchronization. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.1.0 | Distributed path optimizer for shared workspace robotic enjambres. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.2.2 | Priority-based task scheduler for heterogeneous robot fleets. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.8 | High-availability monitor with transparent mission failover. |

### 🎮 Digital Twin & Simulation
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.9 | High-fidelity physics simulation engine for risk-free robot testing. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.8 | Real-world physics simulation (MuJoCo/PhysX) of URDF chains. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.9 | Hardware-in-the-loop interface for real-vs-virtual command syncing. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.1.0 | Procedural generator of training datasets for Vision nodes. |

### 📊 Data & Analytics
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.8 | Big Data storage for massive industrial robotic data. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.7 | High-throughput ingester for CAN, WebSocket, and system logs. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.7 | Predictive maintenance engine based on motor vibration signatures. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.5 | Automated OEE and KPI generation for industrial plant management. |

### 🏭 Industrial Gateway
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.5 | Industry 4.0 interoperability bridge for factory standards (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.9 | Mapping of HydraState robotic objects to standard OPC-UA nodes. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.6 | Telemetry bridge for IoT integrations and external dashboards. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.8 | Standardized interface for machine tool and robot health monitoring. |

### 🌉 External Automation Bridges
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.1.2 | Bidirectional ROS 2 coordination boundary: topics for observation, services for inspection and cancellable actions for cell jobs. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.9 | Traceable PCB hand-off coordinator for OpenPnP and robot-assisted loading or unloading. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.8 | Safe bridge around native 3D-printer software; first adapter validates Moonraker readiness without replacing firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.9 | CNC cell auxiliary coordinator; controller trajectory and machine safety remain native. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.7 | Laser-cell auxiliary coordinator that cannot arm, fire or override laser interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.1.2 | Coordination boundary for legged/humanoid droids: named walk/pick/place action vocabulary gated through the shared safety contract; gait and balance stay on the droid's own controller. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.1.3 | Coordination boundary for AGV/AMR fleets: factory-to-local frame transform plus a VDA-5050-inspired order vocabulary; path planning stays with the AMR's own navigation. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.1.4 | Coordination boundary for camera-equipped UAVs: named flight-request vocabulary plus a deterministic heartbeat/link-loss failsafe watchdog. |

### 🛠️ Complementary Tools
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.5 | Wearable emergency dashboard with haptic safety alerts. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.7 | Command-line interface for fleet automation, flashing, and devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.6 | AI extension for web dashboards providing natural language insights. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.8 | Cross-platform GUI/CLI tool to detect, install, and manually update every ecosystem project. |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.3.1 | Windows/Linux desktop tool that builds a ready-to-flash CM5 image pre-loaded with the ecosystem's most current versions and Raspberry-Pi-Imager-style first-boot configuration. |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.8 | Maintenance-incident coordinator: a low-privilege edge role collects a sanitized inventory/health snapshot, a control-plane role renders it read-only and asks an AI provider to suggest a diagnosis - never applies a patch or deploys anything. |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.8 | Reproducible development host: a policy-gated configuration schema and manifest inventory today, growing into an isolated task/workspace runner coordinated with OPS-AGENT - no task ever has deploy permission unless a document explicitly grants it. |
| [HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS) | 0.0.3 | Architecture, interfaces, security baseline, capability matrix and generated project catalogue of the ecosystem, plus the tools that compare all repositories. |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="URTC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Tools-25%2B%20profiles-blueviolet.svg" alt="Tools">
</p>

**URTC (Universal Robot Tool Controller)** is its own product, not a HYDRA-UMC subsystem folder: real-time firmware and a family of desktop/web tools for a robot's end-effector, developed, versioned and maintained independently. A URTC-equipped tool changer coordinates with HYDRA-UMC's cell controller over FDCAN, but the tool's own real-time behaviour, watchdog and safe state are URTC's own authority - the cell controller cannot bypass it, and URTC does not depend on HYDRA-UMC to be developed, flashed or diagnosed.

**Updater:** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) detects, installs and updates the repositories of this ecosystem; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) does it for all four.

## 🏗️ How URTC Works

1. **Tool firmware**: URTC's own STM32 firmware runs each of 25+ specialized tool profiles (grippers, dispensers, probes, spindles and more), each with its own timing, limits and fault behaviour.
2. **Field update**: CAN-OTA pushes a new firmware image over the same CAN bus the tool already uses, with a full-chip SWD/JTAG path (URTC-FLASHER) as the fallback that never depends on the tool's own firmware being alive.
3. **Live diagnostics**: URTC-TESTER validates a tool's real-time CAN behaviour against its declared profile without a full workshop setup; URTC-WEB-STUDIO does the same from a browser tab over Web Serial, with nothing to install.
4. **Storage and lifecycle**: URTC-SMART-RACK holds tools between jobs, pre-heats one before a hand-off and keeps a lifecycle audit trail (cycles, faults, last calibration) per physical tool, not per tool type.
5. **Active QA**: URTC-VISION-TOOL is itself a tool - a toolhead with its own thermal and RGB cameras for in-process quality inspection, not an external camera bolted onto another tool.
6. **Shared base**: **URTC-COMMON** holds the CAN protocol of the tool head as data, with generated code and conformance vectors; **URTC-DOCS** holds the architecture, security baseline and capability matrix.

## 🛠️ Technology Stack

- **Firmware**: STM32, FDCAN (shared bus with the cell controller), CAN-OTA, SWD/JTAG fallback.
- **Desktop tooling**: cross-platform GUI clients for flashing and diagnostics (URTC-FLASHER, URTC-TESTER).
- **Browser tooling**: the Web Serial API for zero-install hardware testing (URTC-WEB-STUDIO).
- **Lifecycle data**: non-volatile per-tool audit trail, shared with HYDRA-UMC's own F-RAM integrity approach.

## 🔒 Safety

Each tool profile carries its own watchdog and fault behaviour, independent of the cell controller's own E-STOP layer - a tool that loses its own timing budget or CAN heartbeat goes to its declared safe state on its own, rather than waiting for an external command. URTC-SMART-RACK's pre-heating is bounded by the same per-tool thermal limits its profile declares, audited in the same lifecycle trail a workshop uses to decide whether a tool is still fit for service.

## 📁 URTC Project Catalog

| Repository | Version | Description |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.4.0 | Universal Robot Tool Controller firmware for 25+ specialized tools. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.4.0 | GUI tool for CAN-OTA and full-chip SWD/JTAG firmware updates. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.4.1 | Diagnostic tool for real-time validation of URTC tool profiles over CAN. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.3.6 | Browser-based Web Serial tool for instant hardware testing and analysis. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.2.0 | Intelligent tool storage with automatic pre-heating and lifecycle audit. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.1.4 | Toolhead with integrated thermal and RGB cameras for active QA. |
| [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) | 0.1.7 | Detects, installs and updates the URTC repositories on a machine from their own manifests. |
| [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) | 0.1.1 | Architecture, interfaces, security baseline, capability matrix, CAN protocol study note and generated project catalogue of the URTC ecosystem, plus the tools that compare all repositories. |
| [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) | 0.0.8 | The CAN protocol of the tool head as data: a specification, generated C, TypeScript and Python code, conformance vectors and the Python transports. |
| [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) | 0.0.2 | Gateway in front of the URTC CAN bus: allowed identifier list, rate limit and session key. |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ARMOR_BANNER.svg" alt="A.R.M.O.R. Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar & Multimodal Observation Range)** is a separate, public perimeter-security and home-automation ecosystem - no relation to HYDRA-UMC or URTC beyond the same author and the same engineering conventions (versioned manifests, a shared message contract, eight-language interfaces). Its field nodes watch a property's perimeter and its solar/electrical installation; its central server and clients let an operator see and act on what they report. The version and maturity notes below come straight from each repository's own manifest and capability matrix, the same honesty convention HYDRA-UMC's dashboard already uses.

**Updater:** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) detects, installs and updates the repositories of this ecosystem; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) does it for all four.

## 🏗️ How A.R.M.O.R. Is Built

1. **Shared contract**: **ARMOR-COMMON** owns the message meaning - JSON Schema, a Python validator and generated TypeScript/Kotlin types every other repository consumes, never redefines.
2. **Field nodes**: ESP32-S3 firmware for radar/presence sensing (**ARMOR-RADAR**), solar inverter and battery monitoring (**ARMOR-SOLAR**), electrical metering with switching (**ARMOR-ELECTRICAL**), and the house's alarm panel (**ARMOR-ALARM**); a Python agent (**ARMOR-NETWORK**) watches the house's own local network and internet reachability from a machine already on it.
3. **Central coordinator**: **ARMOR-SERVER** holds state, users, alarms, automations and camera evidence; **ARMOR-SERVER-AI** and **ARMOR-VOICE-AI** add an explainable visual policy and offline voice intents that never actuate anything on their own.
4. **Operator clients**: **ARMOR-STUDIO** (web) and **ARMOR-ANDROID-CONTROL** (mobile) are clients of the central server, never of the field network directly. **ARMOR-HMI** is a touch panel on the wall (a Waveshare ESP32-S3-Touch-LCD-7C-BOX) that shows the state, arms and acknowledges, and will be where the voice assistant lives.
5. **Deployment and testing**: **ARMOR-DEVOPS** deploys the whole service graph; **ARMOR-SIMULATOR** replays scenarios and repeatable faults without real hardware; **ARMOR-HARDWARE** carries the enclosure design and its bench acceptance matrix.
6. **Ecosystem operations**: **ARMOR-UPDATER** discovers, installs and updates every A.R.M.O.R. repository on a machine, the same atomic-by-verification design as HYDRA-UMC-UPDATER; **ARMOR-DOCS** is the canonical architecture documentation and capability matrix. **ARMOR-STUDIO** can also update the services on the central machine from packages signed with the ecosystem's release key, checking each signature before installing.

## 🔒 Honesty and Safety

A.R.M.O.R. follows the same rule HYDRA-UMC's own dashboard already applies: a claim is real only when it is verified, and every repository says plainly what has and hasn't been run on real hardware yet. Nothing in this ecosystem currently controls mains electricity or physical access; field nodes observe and report, and any future switching capability is designed and reviewed before it is ever enabled.

## 📁 A.R.M.O.R. Project Catalog

| Repository | Version | Description |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.7.6 | Message contracts, validators, conformance vectors, generated types, OpenAPI, shared launcher. |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.8.0.1 | ESP32-S3 field-node firmware, decoders for the LD2450, LD2461 and presence sensors, its host-tested core, updates from GitHub with a progress bar and a live map. |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.5.6 | Solar gateway node: the ESP32-S3 firmware and its panel (ten serial ports), and the protocols of Voltronic / MPP Solar inverters and Pylontech and ANT-BMS batteries. |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.4.7 | Electrical node: the firmware (sixteen PZEM meters on one serial line, web panel, MQTT), the meters' frames, the message of the network's readings and the rules for switching. |
| [ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM) | 0.4.5 | Alarm node and panel: its firmware (wired zones, the siren, Zigbee sensors and sirens, a web panel in seven languages) and the rules of arming, delays, alarm and PIN, tested on a computer; it keeps guarding, and takes the Zigbee radio over, when the server is away. Never run on a board. |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.3.8 | Touch panel for the Waveshare ESP32-S3-Touch-LCD-7C-BOX: the system's state on a wall screen, arm/disarm/acknowledge, push-to-talk voice and the web page of a node; the firmware has never run on a board. |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.1.4 | Local network monitor: the devices on the house's network, the state of the internet (and whose side an outage is on), what changes; it only observes. |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.8.0.5 | Central state (persisted), users, event history, alarms, devices, automations, solar and electrical readings, the local network, system services, camera watchdog, cameras, evidence, audit, node firmware updates that must be signed, Telegram and Home Assistant notices, voice commands, and use from outside the house (second factor, sessions that can be ended, a remote policy). |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.7 | Motion-watching service, visual profile selection, explainable fusion policy, engine registry. |
| [ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION) | 0.0.3 | Camera zones, masks and detection rules (loitering, one event per visit); no detector model yet. |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.3.1 | Offline voice service: fifteen commands in eight languages, the wall panel's spoken turns, arm and disarm confirmed with a signed token. |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.8.0.9 | Operations console, alarms, devices, automations, users, history, alert rules, PTZ, radar map, solar and electrical menus, the local network, system services, weather, a node finder and configuration, node firmware updates, notifications, and a 2D/3D site designer. |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.7.5 | Android operator client: arm and disarm, alarms, devices, live radar, solar inverters and batteries, history, alarm notifications, an assistant for written and spoken commands and the configurator of the nodes. |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.6 | Enclosure designs (the radar corner enclosure; a checked box for the solar, electrical and alarm nodes) and the bench acceptance matrix. |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.6.7 | Compose topology, central-server test-bench installer, backup and restore, TLS profile, own MQTT broker, observation and voice services, administration agent. |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.6 | Scenarios and repeatable faults. |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.1.5 | Detects, installs and updates the ecosystem's own repositories (atomic-by-verification, no GITHUB_TOKEN required). |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.8.1.2 | Canonical documentation and the capability matrix. |

---

# ⚡ EH3D FABRICATION SUITE

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/EH3D_BANNER.svg" alt="EH3D Fabrication Suite Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Desktop%20%7C%20Embedded-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-C%2B%2B%20%7C%20Python%20%7C%20Qt-orange.svg" alt="Stack">
  <img src="https://img.shields.io/badge/Hardware-HYDRA--UMC%20%7C%20Bungard%20%7C%20ESP32-green.svg" alt="Hardware">
</p>

**EH3D Fabrication Suite** is a dedicated, multi-repository software ecosystem tailored for rapid Printed Circuit Board (PCB) prototyping, CAM toolpath preparation, computer vision inspection, Pick & Place (PnP) management, and multi-machine CNC/Laser control. It provides native interoperability with **HYDRA-UMC** hardware nodes (STM32H7 + Jetson Orin NX + Hailo NPU) alongside a workshop machine fleet comprising industrial milling systems (Bungard CCD via ESP32-S3 RS-232 gateways), CNC routers (JuanenCNC), and diode laser engravers (JuanenLaser).

**Updater:** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) detects, installs and updates the repositories of this ecosystem; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) does it for all four.

## 🏗️ How EH3D Fabrication Suite Works

1. **Central Management**: **EH3D-SUITE-LAUNCHER** discovers active hardware nodes on the local network (HYDRA-UMC and ESP32 gateways), manages unified `.eh3dproj` packages, and orchestrates tool updates.
2. **CAM Processing Pipeline**: Specialized CAD/CAM tools handle individual fabrication stages:
   - **EH3D-ISOCAM**: Gerber RS-274X/X2 track isolation, Voronoi algorithms, and rubout copper removal.
   - **EH3D-DRILLPRO**: Excellon/NC Drill processing, drill bit tables, and deep hole drilling cycles.
   - **EH3D-ROUTEPRO**: Board edge milling, tab creation, and ramping entry strategies.
   - **EH3D-LASER-CAM**: Raster dithering algorithms and vector power modulation for laser cutting.
   - **EH3D-STENCILCAM**: Pastemask processing for SMD solder paste stencil generation.
3. **Execution & Real-Time Control**: **EH3D-MOTIONCNC** drives machine movement via high-speed G-Code/HP-GL streaming, integrated with **EH3D-AUTOLEVEL** for topographic Z-probing and **EH3D-PENDANT-GUI** for handheld zero-setting (G54/G55) and jogging.
4. **Edge AI & Inspection**: **EH3D-VISION-STUDIO** leverages HYDRA-UMC's Hailo NPU to perform real-time camera alignment, automatic fiducial detection, and tool wear inspection.
5. **Assembly & Auxiliary Data**: **EH3D-PNP-MANAGER** manages centroid Pick & Place coordinates and feeders, while **EH3D-TOOL-MANAGER** maintains a unified tool crib database across all CAM modules.

## 📁 EH3D Fabrication Suite Project Catalog

| Repository | Version | Description |
| :--- | :--- | :--- |
| [EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER) | 0.0.1 | Main ecosystem dashboard for project management (.eh3dproj), updates, global settings, and node discovery. |
| [EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM) | 0.0.1 | Gerber RS-274X/X2 CAM processing app, Voronoi/Offset track isolation, rubout, and engraving simulation. |
| [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) | 0.0.1 | Excellon/NC Drill CAM app, drill bit management, path optimization, and deep drilling cycles. |
| [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO) | 0.0.1 | Board contour milling CAM app, pocketing, holding tabs, and CNC ramp entry strategies. |
| [EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM) | 0.0.1 | Laser CAM app for image dithering, raster/vector conversion, and dynamic PWM power control. |
| [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC) | 0.0.1 | Real-time numerical control GUI, 3D G-code visualizer, probing, and multi-machine streaming support. |
| [EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL) | 0.0.1 | Topographic height mesh processor (Z-Probing) and G-code interpolation for surface compensation. |
| [EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER) | 0.0.1 | Lightweight CAM inspection tool for Gerber layer alignment and rapid visualization. |
| [EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM) | 0.0.1 | Pastemask conversion utility generating cutting toolpaths for laser and plotter SMD stencil fabrication. |
| [EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER) | 0.0.1 | OpenPnP-inspired SMD assembly manager, centroid reader, feeder control, and vision component centering. |
| [EH3D-PENDANT-GUI](https://github.com/JuanenRac/EH3D-PENDANT-GUI) | 0.0.1 | Touchscreen/mobile manual controller for real-time jogging, zero setting (G54/G55), and E-STOP. |
| [EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER) | 0.0.1 | 3D toolpath & material removal simulator, collision detector, and G-Code/HP-GL cycle time estimator. |
| [EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO) | 0.0.1 | Edge AI vision dashboard for camera alignment, fiducial marker training, and visual inspection via HYDRA-UMC. |
| [EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER) | 0.0.1 | Shared tool crib database tracking wear hours, cutting presets, and feeds across all EH3D CAM tools. |
| [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) | 0.0.1 | Rust server with a REST and websocket interface: users, machines and jobs, planning of drilling and routing jobs with the DRILLPRO and ROUTEPRO libraries, one job at a time per machine. |
| [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD) | 0.0.1 | ESP32-S3 node for the box of a Bungard CCD machine: RS-232 of its control unit over Ethernet or Wi-Fi, with the machine's lamps and the spindle drive on the same board. |
| [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS) | 0.0.1 | Shared C++/Python library containing Gerber/Excellon/G-Code/HP-GL parsers, 2D/3D geometry, and protocols. |
| [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON) | 0.0.1 | Data schemas, unified project (.eh3dproj) specifications, global constants, and UI graphic assets. |
| [EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS) | 0.0.1 | Ecosystem documentation, assembly guides, gateway technical specs, and integration manuals. |
| [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) | 0.0.1 | Detects, installs and updates the ecosystem's own repositories (atomic-by-verification, no GITHUB_TOKEN required). |

---

## 🤝 Contributing
Each ecosystem is its own initiative with its own projects. Each project has its own contribution guidelines. Please refer to individual repositories for technical details.

Issue labels are standardized across every HYDRA-UMC repo from [`.github/labels.yml`](.github/labels.yml) in this same repo, synced out by [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - edit that one file to change a label everywhere at once, rather than by hand per repo. Unlike the dashboard below, this list is static (a real GitHub Actions matrix, not dynamic discovery) - a newly added repo needs an entry there too, not just a real `hydra-umc.project.json`.

A live status dashboard covering every public repo of the four ecosystems - each one discovered by its own manifest (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`, plus `electro-hobby-3d.project.json` for the cross-ecosystem repos), read straight from each repo's own default branch with no fixed list - is regenerated by [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) immediately when a project pushes (each repo's own `dashboard-dispatch.yml`) and, as a safety net, twice an hour, and served from `docs/` via GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. It shows stack, deploy target and current version, a real maturity classification per project (scaffolding / functional / established / production, each decided from that project's own CHANGELOG - see [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)), its role (API / UI / CLI / firmware / library / service / tool), a family/parent-child tree and per-project notes on what is implemented today. [`ecosystem-catalog.json`](ecosystem-catalog.json) lists those ecosystems and their manifests in one place, and the dashboard build refuses to run if the two ever disagree.

## 🧭 GitHub Collaboration

The [GitHub collaboration model](docs/GITHUB_COLLABORATION.md) defines one central Wiki, one ecosystem Project, Discussions scope, release criteria and the shared automation boundary. The centrally maintained [issue forms](.github/ISSUE_TEMPLATE/) and [pull-request template](.github/PULL_REQUEST_TEMPLATE.md) make software, hardware-validation and documentation work traceable without duplicating project manuals.

The community-health workflow is intentionally manual and dry-run by default. Once `COMMUNITY_HEALTH_SYNC_TOKEN` is configured, it can copy only these managed templates to every repository that publishes a HYDRA-UMC manifest; it never deletes a project-specific template.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.