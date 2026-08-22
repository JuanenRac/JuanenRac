<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

# HYDRA-UMC / URTC Ecosystem 🤖🚀

<p align="center">
  🇺🇸 <b>English</b> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Welcome to the **HYDRA-UMC Ecosystem**, a multi-layered industrial robotics platform spanning from low-level real-time firmware to high-level cognitive AI. This organization hosts 44 specialized projects designed to work in perfect synchrony for micro-factory automation and swarm robotics.

---

## 🏗️ Ecosystem Architecture

The ecosystem is structured into 6 functional layers that enable autonomous, collaborative, and intelligent robotic operations:

1.  **Execution Layer**: STM32-based firmware (H745/G474) for sub-millimetric precision and high-speed FDCAN actuation.
2.  **Intelligence Layer**: Edge AI powered by **Hailo-8** (Reflex perception) and **Hailo-10** (Cognitive reasoning).
3.  **Coordination Layer**: Standalone Node.js backends and distributed swarm orchestrators.
4.  **Interface Layer**: Web (React), Desktop (Qt6), Mobile (Kotlin/Flutter), and DSI touch dashboards.
5.  **Virtual Layer**: High-fidelity Digital Twin engines (Rust/Bevy) for safe pre-physical validation.
6.  **Support Layer**: Industry 4.0 gateways (OPC-UA/MQTT) and Big Data predictive maintenance.

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

## 📁 Project Catalog

### 💠 Core Ecosystem (Main Control)
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
| [URTC](https://github.com/JuanenRac/URTC) | Universal Robot Tool Controller firmware for 25+ specialized tools. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | GUI tool for CAN-OTA and full-chip SWD/JTAG firmware updates. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Diagnostic tool for real-time validation of URTC tool profiles over CAN. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Browser-based Web Serial tool for instant hardware testing and analysis. |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-VISION-NODE** | High-speed perception node for 8x simultaneous USB 3.0 camera streams. |
| **HYDRA-UMC-VISION-STREAMER** | Optimized GStreamer/MediaMTX pipeline for industrial video relay. |
| **HYDRA-UMC-DETECTION-HEF** | Library of hardware-accelerated YOLO models for SMD and component QA. |
| **HYDRA-UMC-SAFETY-ZONES** | Real-time AI intrusion detection for robotic work volume protection. |
| **HYDRA-UMC-VISUAL-SERVOING-API** | Image-based kinematic feedback for sub-millimetric pose correction. |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-COGNITIVE-NODE** | Semantic reasoning node for logical mission planning and voice control. |
| **HYDRA-UMC-VLA-ENGINE** | Vision-Language-Action model implementation for complex task execution. |
| **HYDRA-UMC-VOICE-UI** | Local, private STT/TTS pipeline for natural language operator interaction. |
| **HYDRA-UMC-SEMANTIC-PLANNER** | LLM-based mission orchestrator with context-aware error recovery. |
| **HYDRA-UMC-DOCS-QA** | RAG-based AI assistant trained on technical manuals and source code. |

### 🐝 Orchestration & Swarm
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-ORCHESTRATOR** | Fleet manager for multi-robot coordination and collision avoidance. |
| **HYDRA-UMC-SWARM-SYNC** | PTP (Precision Time Protocol) sync for nanosecond robot synchronization. |
| **HYDRA-UMC-PATH-PLANNER-3D** | Distributed path optimizer for shared workspace robotic enjambres. |
| **HYDRA-UMC-JOB-DISPATCHER** | Priority-based task scheduler for heterogeneous robot fleets. |
| **HYDRA-UMC-NODE-HEALING** | High-availability monitor with transparent mission failover. |

### 🎮 Digital Twin & Simulation
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-TWIN** | High-fidelity physics simulation engine for risk-free robot testing. |
| **HYDRA-UMC-PHYSICS-REPLICA** | Real-world physics simulation (MuJoCo/PhysX) of URDF chains. |
| **HYDRA-UMC-HIL-BRIDGE** | Hardware-in-the-loop interface for real-vs-virtual command syncing. |
| **HYDRA-UMC-SYNTHETIC-DATA-GEN** | Procedural generator of training datasets for Vision nodes. |

### 📊 Data & Analytics
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-DATALAKE** | Big Data storage for massive multi-robot industrial telemetry. |
| **HYDRA-UMC-TELEMETRY-COLLECTOR** | High-throughput ingester for CAN, WebSocket, and system logs. |
| **HYDRA-UMC-ANOMALY-DETECTOR** | Predictive maintenance engine based on motor vibration signatures. |
| **HYDRA-UMC-PRODUCTION-REPORTS** | Automated OEE and KPI generation for industrial plant management. |

### 🏭 Industrial Gateway
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-GATEWAY-INDUSTRIAL** | Industry 4.0 interoperability bridge for factory standards (OPC-UA/MQTT). |
| **HYDRA-UMC-OPCUA-SERVER** | Mapping of HydraState robotic objects to standard OPC-UA nodes. |
| **HYDRA-UMC-MQTT-BROKER** | Telemetry bridge for IoT integrations and external dashboards. |
| **HYDRA-UMC-MTCONNECT-ADAPTER** | Standardized interface for machine tool and robot health monitoring. |

### 🛠️ Complementary Tools
| Repository | Description |
| :--- | :--- |
| **URTC-SMART-RACK** | Intelligent tool storage with automatic pre-heating and lifecycle audit. |
| **URTC-VISION-TOOL** | Toolhead with integrated thermal and RGB cameras for active QA. |
| **HYDRA-UMC-WATCH** | Wearable emergency dashboard with haptic safety alerts. |
| **HYDRA-UMC-TOOL-CLI** | Command-line interface for fleet automation, flashing, and devops. |
| **HYDRA-UMC-DASHBOARD-AI** | AI extension for web dashboards providing natural language insights. |

---

## 🤝 Contributing
This ecosystem is part of a high-tech robotic initiative. Each project has its own contribution guidelines. Please refer to individual repositories for technical details.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.
