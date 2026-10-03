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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-3-00E5FF.svg" alt="Three ecosystems">
</p>

Three independent engineering ecosystems, one author. **HYDRA-UMC** is a multi-layered industrial robotics platform, from real-time firmware to cognitive AI. **URTC** is its universal robot-tool subsystem: real-time firmware and desktop/web tooling for a robot's own end-effector, developed as its own product with independent versioning and maintenance tools. **A.R.M.O.R.** is a separate, public perimeter-security and home-automation ecosystem - radar presence detection, solar and electrical monitoring, and a central coordinator with web and mobile clients.

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
Windows) clones 13 core repositories - a hand-picked starting set, not
the full catalog below - as siblings in one directory: the standard
layout every cross-repo script here already assumes. Re-running it is
safe: anything already cloned is left untouched. From there,
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(one of the 13 just cloned) can check versions and build/update any of
the other projects in the full catalog below.

### 🧱 Platform Foundation & Contracts
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.4.7 | Raspberry Pi OS platform layer for CM5: reproducible profiles, configuration, diagnostics, service lifecycle and updates; not a new Linux distribution. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.2.8 | Shared versioned contracts, thin clients and conformance fixtures for services, UIs and CM5 adapters; it does not replace vendor APIs. |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.0 | Declarative adapter-manifest registry and validator for external-machine connectors; extends the SDK's own contract idea to external machines without replacing the industrial-gateway projects. |

### 💠 Core Control & Operator Clients
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.1.6 | Core motion control firmware for STM32H745/G474 with S-Curve kinematics. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.0.5 | Headless Node.js API and WebSocket backend for robotic orchestration. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.7.6 | Advanced React-based web dashboard for 3D robot monitoring and control. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.4 | High-performance Python/Qt desktop application for industrial automation. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.0 | Dedicated Flutter-based touch interface for 7" industrial displays (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.6.3 | Native Kotlin mobile app with biometric login for remote robot management. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.0 | Flutter mobile app for iOS/iPadOS with real-time WebSocket sync. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.0 | Graphical URDF editor to validate and push robot models to the catalog. |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.2 | Desktop STL model editor - transform, replace, remove and add real parts in the shared model catalog. |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.0 | High-speed perception node for 8x simultaneous USB 3.0 camera streams. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.1.6 | Optimized GStreamer/MediaMTX pipeline for industrial video relay. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.0.9 | Library of hardware-accelerated YOLO models for SMD and component QA. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.1 | Real-time AI intrusion detection for robotic work volume protection. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.4 | Image-based kinematic feedback for sub-millimetric pose correction. |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.1 | Semantic reasoning node for logical mission planning and voice control. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.4 | Vision-Language-Action model implementation for complex task execution. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.3 | Local, private STT/TTS pipeline for natural language operator interaction. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.0 | LLM-based mission orchestrator with context-aware error recovery. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.0 | RAG-based AI assistant trained on technical manuals and source code. |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.2 | Local, policy-gated AI maintenance technician: a fixed risk-level policy and tool allowlist today, with a real, tested defense proving a malicious retrieved document can never trigger a tool call or leak a secret - the AI never gets authority by generating a response. |

### 🐝 Orchestration & Swarm
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.3 | Fleet manager for multi-robot coordination and collision avoidance. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.1 | PTP (Precision Time Protocol) sync for nanosecond robot synchronization. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.0.7 | Distributed path optimizer for shared workspace robotic enjambres. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.1.8 | Priority-based task scheduler for heterogeneous robot fleets. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.4 | High-availability monitor with transparent mission failover. |

### 🎮 Digital Twin & Simulation
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.7 | High-fidelity physics simulation engine for risk-free robot testing. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.6 | Real-world physics simulation (MuJoCo/PhysX) of URDF chains. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.6 | Hardware-in-the-loop interface for real-vs-virtual command syncing. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.0.8 | Procedural generator of training datasets for Vision nodes. |

### 📊 Data & Analytics
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.3 | Big Data storage for massive industrial robotic data. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.4 | High-throughput ingester for CAN, WebSocket, and system logs. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.3 | Predictive maintenance engine based on motor vibration signatures. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.2 | Automated OEE and KPI generation for industrial plant management. |

### 🏭 Industrial Gateway
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.2 | Industry 4.0 interoperability bridge for factory standards (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.5 | Mapping of HydraState robotic objects to standard OPC-UA nodes. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.2 | Telemetry bridge for IoT integrations and external dashboards. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.4 | Standardized interface for machine tool and robot health monitoring. |

### 🌉 External Automation Bridges
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.0.7 | Bidirectional ROS 2 coordination boundary: topics for observation, services for inspection and cancellable actions for cell jobs. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.4 | Traceable PCB hand-off coordinator for OpenPnP and robot-assisted loading or unloading. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.3 | Safe bridge around native 3D-printer software; first adapter validates Moonraker readiness without replacing firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.4 | CNC cell auxiliary coordinator; controller trajectory and machine safety remain native. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.2 | Laser-cell auxiliary coordinator that cannot arm, fire or override laser interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.0.8 | Coordination boundary for legged/humanoid droids: named walk/pick/place action vocabulary gated through the shared safety contract; gait and balance stay on the droid's own controller. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.0.8 | Coordination boundary for AGV/AMR fleets: factory-to-local frame transform plus a VDA-5050-inspired order vocabulary; path planning stays with the AMR's own navigation. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.0.9 | Coordination boundary for camera-equipped UAVs: named flight-request vocabulary plus a deterministic heartbeat/link-loss failsafe watchdog. |

### 🛠️ Complementary Tools
| Repository | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.2 | Wearable emergency dashboard with haptic safety alerts. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.2 | Command-line interface for fleet automation, flashing, and devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.1 | AI extension for web dashboards providing natural language insights. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.3 | Cross-platform GUI/CLI tool to detect, install, and manually update every ecosystem project. |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.2.7 | Windows/Linux desktop tool that builds a ready-to-flash CM5 image pre-loaded with the ecosystem's most current versions and Raspberry-Pi-Imager-style first-boot configuration. |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.4 | Maintenance-incident coordinator: a low-privilege edge role collects a sanitized inventory/health snapshot, a control-plane role renders it read-only and asks an AI provider to suggest a diagnosis - never applies a patch or deploys anything. |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.3 | Reproducible development host: a policy-gated configuration schema and manifest inventory today, growing into an isolated task/workspace runner coordinated with OPS-AGENT - no task ever has deploy permission unless a document explicitly grants it. |

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

## 🏗️ How URTC Works

1. **Tool firmware**: URTC's own STM32 firmware runs each of 25+ specialized tool profiles (grippers, dispensers, probes, spindles and more), each with its own timing, limits and fault behaviour.
2. **Field update**: CAN-OTA pushes a new firmware image over the same CAN bus the tool already uses, with a full-chip SWD/JTAG path (URTC-FLASHER) as the fallback that never depends on the tool's own firmware being alive.
3. **Live diagnostics**: URTC-TESTER validates a tool's real-time CAN behaviour against its declared profile without a full workshop setup; URTC-WEB-STUDIO does the same from a browser tab over Web Serial, with nothing to install.
4. **Storage and lifecycle**: URTC-SMART-RACK holds tools between jobs, pre-heats one before a hand-off and keeps a lifecycle audit trail (cycles, faults, last calibration) per physical tool, not per tool type.
5. **Active QA**: URTC-VISION-TOOL is itself a tool - a toolhead with its own thermal and RGB cameras for in-process quality inspection, not an external camera bolted onto another tool.

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
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.1 | Universal Robot Tool Controller firmware for 25+ specialized tools. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.2.1 | GUI tool for CAN-OTA and full-chip SWD/JTAG firmware updates. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.2.2 | Diagnostic tool for real-time validation of URTC tool profiles over CAN. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.2.2 | Browser-based Web Serial tool for instant hardware testing and analysis. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.0 | Intelligent tool storage with automatic pre-heating and lifecycle audit. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.0.5 | Toolhead with integrated thermal and RGB cameras for active QA. |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="A.R.M.O.R. Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar & Multimodal Observation Range)** is a separate, public perimeter-security and home-automation ecosystem - no relation to HYDRA-UMC or URTC beyond the same author and the same engineering conventions (versioned manifests, a shared message contract, seven-language interfaces). Its field nodes watch a property's perimeter and its solar/electrical installation; its central server and clients let an operator see and act on what they report. The version and maturity notes below come straight from each repository's own manifest and capability matrix, the same honesty convention HYDRA-UMC's dashboard already uses.

## 🏗️ How A.R.M.O.R. Is Built

1. **Shared contract**: **ARMOR-COMMON** owns the message meaning - JSON Schema, a Python validator and generated TypeScript/Kotlin types every other repository consumes, never redefines.
2. **Field nodes**: ESP32-S3 firmware for radar/presence sensing (**ARMOR-RADAR**), solar inverter and battery monitoring (**ARMOR-SOLAR**), and electrical metering with switching (**ARMOR-ELECTRICAL**); a Python agent (**ARMOR-NETWORK**) watches the house's own local network and internet reachability from a machine already on it.
3. **Central coordinator**: **ARMOR-SERVER** holds state, users, alarms, automations and camera evidence; **ARMOR-SERVER-AI** and **ARMOR-VOICE-AI** add an explainable visual policy and offline voice intents that never actuate anything on their own.
4. **Operator clients**: **ARMOR-STUDIO** (web) and **ARMOR-ANDROID-CONTROL** (mobile) are clients of the central server, never of the field network directly. **ARMOR-HMI** is a touch panel on the wall (a Waveshare ESP32-S3-Touch-LCD-7C-BOX) that shows the state, arms and acknowledges, and will be where the voice assistant lives.
5. **Deployment and testing**: **ARMOR-DEVOPS** deploys the whole service graph; **ARMOR-SIMULATOR** replays scenarios and repeatable faults without real hardware; **ARMOR-HARDWARE** carries the enclosure design and its bench acceptance matrix.
6. **Ecosystem operations**: **ARMOR-UPDATER** discovers, installs and updates every A.R.M.O.R. repository on a machine, the same atomic-by-verification design as HYDRA-UMC-UPDATER; **ARMOR-DOCS** is the canonical architecture documentation and capability matrix.

## 🔒 Honesty and Safety

A.R.M.O.R. follows the same rule HYDRA-UMC's own dashboard already applies: a claim is real only when it is verified, and every repository says plainly what has and hasn't been run on real hardware yet. Nothing in this ecosystem currently controls mains electricity or physical access; field nodes observe and report, and any future switching capability is designed and reviewed before it is ever enabled.

## 📁 A.R.M.O.R. Project Catalog

| Repository | Version | Description |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.3.4 | Message contracts, validators, conformance vectors, generated types, OpenAPI, shared launcher. |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.4.8 | ESP32-S3 field-node firmware, decoders for the LD2450, LD2461 and presence sensors, and its host-tested core. |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.2.2 | Solar gateway node: the ESP32-S3 firmware and its panel (ten serial ports), and the protocols of Voltronic / MPP Solar inverters and Pylontech and ANT-BMS batteries. |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.1.6 | Electrical node: the firmware (sixteen PZEM meters on one serial line, web panel, MQTT), the meters' frames, the message of the network's readings and the rules for switching. |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.1.0 | Touch panel for the Waveshare ESP32-S3-Touch-LCD-7C-BOX: the system's state on a wall screen, arm/disarm/acknowledge, push-to-talk voice and the web page of a node; the firmware has never run on a board. |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.0.6 | Local network monitor: the devices on the house's network, the state of the internet (and whose side an outage is on), what changes; it only observes. |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.4.1 | Central state (persisted), users, event history, alarms, devices, automations, solar and electrical readings, the local network, system services, camera watchdog, cameras, evidence, audit. |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.1 | Visual profile selection, explainable fusion policy, engine registry. |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.2.1 | Offline voice intents with signed confirmation. |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.6.0 | Operations console, alarms, devices, automations, users, history, alert rules, PTZ, radar map, solar and electrical menus, the local network, system services, weather, a node finder and configuration, and a 2D/3D site designer. |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.4.0 | Android operator client: arm and disarm, alarms, devices, live radar, solar inverters and batteries, history and alarm notifications. |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.3 | Enclosure design and the bench acceptance matrix. |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.3.6 | Compose topology, central-server test-bench installer, backup and restore, TLS profile, own MQTT broker. |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.3 | Scenarios and repeatable faults. |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.0.4 | Detects, installs and updates the ecosystem's own repositories (atomic-by-verification, no GITHUB_TOKEN required). |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.5.5 | Canonical documentation and the capability matrix. |

---

## 🤝 Contributing
Each ecosystem is its own initiative with its own projects. Each project has its own contribution guidelines. Please refer to individual repositories for technical details.

Issue labels are standardized across every HYDRA-UMC repo from [`.github/labels.yml`](.github/labels.yml) in this same repo, synced out by [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - edit that one file to change a label everywhere at once, rather than by hand per repo. Unlike the dashboard below, this list is static (a real GitHub Actions matrix, not dynamic discovery) - a newly added repo needs an entry there too, not just a real `hydra-umc.project.json`.

A live status dashboard covering every public repo that declares `ecosystem: HYDRA-UMC` in its own `hydra-umc.project.json` (stack, deploy target, current version - read straight from each repo's own default branch, discovered dynamically with no fixed list) is regenerated hourly (and immediately on a relevant push) by [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) and served from `docs/` via GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. It adds a real maturity classification per project (scaffolding / functional / established / production, each decided from that project's own CHANGELOG - see [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)'s own module docstring for exactly how), its role (API / UI / CLI / firmware / library / service / tool), a real family/parent-child tree, and per-project notes on what's actually implemented today. URTC's and A.R.M.O.R.'s own repositories are discovered live on that same dashboard exactly the same way HYDRA-UMC's are (see `scripts/generate_dashboard.py`), each one declaring its own `ecosystem` field in its own `urtc.project.json`/`armor.project.json` - no fixed list for any of the three.

## 🧭 GitHub Collaboration

The [GitHub collaboration model](docs/GITHUB_COLLABORATION.md) defines one central Wiki, one ecosystem Project, Discussions scope, release criteria and the shared automation boundary. The centrally maintained [issue forms](.github/ISSUE_TEMPLATE/) and [pull-request template](.github/PULL_REQUEST_TEMPLATE.md) make software, hardware-validation and documentation work traceable without duplicating project manuals.

The community-health workflow is intentionally manual and dry-run by default. Once `COMMUNITY_HEALTH_SYNC_TOKEN` is configured, it can copy only these managed templates to every repository that publishes a HYDRA-UMC manifest; it never deletes a project-specific template.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.
