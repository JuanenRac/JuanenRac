# HYDRA-UMC / URTC Ecosystem 🤖🚀

Welcome to the **HYDRA-UMC Ecosystem**, a multi-layered industrial robotics platform spanning from low-level real-time firmware to high-level cognitive AI. This organization hosts 44 specialized projects designed to work in perfect synchrony.

---

## 🏗️ Ecosystem Architecture

The ecosystem is structured into 6 functional layers that enable autonomous, collaborative, and intelligent robotic operations:

1.  **Execution Layer**: STM32-based firmware for sub-millimetric precision and tool control.
2.  **Intelligence Layer**: Edge AI powered by **Hailo-8** (Perception) and **Hailo-10** (Cognition).
3.  **Coordination Layer**: Headless servers and swarm orchestrators.
4.  **Interface Layer**: Web, Desktop, Mobile, and Wearable control dashboards.
5.  **Virtual Layer**: High-fidelity Digital Twin and physics simulation.
6.  **Support & Industrial Layer**: Industry 4.0 gateways (OPC-UA/MQTT) and predictive analytics.

---

## 🛠️ Technology Stack & Tools

The ecosystem leverages a modern and high-performance stack across all layers:

### 💠 Embedded & Real-Time (Execution)
- **Microcontrollers**: STM32H745 (Dual-Core), STM32G474 (High-Resolution PWM), STM32F303.
- **Frameworks**: FreeRTOS, STM32 HAL/LL, CMSIS-DSP.
- **Communication**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (50MHz IPC), I2C, UART.
- **Kinematics**: S-Curve Profile Generation, Inverse Kinematics (IK) solvers in C.

### 🧠 Edge AI & Perception (Intelligence)
- **AI Accelerators**: Hailo-8 (26 TOPS) for Vision, Hailo-10 (40 TOPS) for GenAI.
- **Models**: YOLOv8/v10 (Object Detection), OpenVLA (Multimodal), Whisper (STT), Llama-3 (Reasoning).
- **Tooling**: Hailo Dataflow Compiler (HEF), TFLite, OpenCV, GStreamer.
- **Inter-node Comms**: gRPC over Protobuf for low-latency metadata.

### 🌐 Backend & Orchestration (Coordination)
- **Runtimes**: Node.js, Rust (Orchestrator), Go (CLI).
- **APIs**: Express, Fastify, Socket.io (WebSocket), gRPC.
- **Data**: InfluxDB/TimescaleDB (Telemetry), Redis (State caching), SQLite.
- **Discovery**: mDNS/Bonjour, Subnet Scanning.

---

## 📋 System Requirements

To deploy and run the HYDRA-UMC ecosystem effectively, the following hardware and software baselines are required:

- **Computing Nodes**: Raspberry Pi CM5 (4GB+ RAM recommended) with eMMC or NVMe storage.
- **AI Acceleration**: Hailo-8 / Hailo-10 M.2 modules for perception and cognitive tasks.
- **Robotic Control**: STM32H745ZIT6 (Kinematic Brain), STM32G474 (Actuators), STM32F303 (Tools).
- **Industrial Networking**: Dedicated Gigabit Ethernet LAN and FDCAN (ISO 11898-1:2015) actuator bus.
- **Client Platforms**: Android 10+ (API 29), iOS 15+, Windows 10/11 (DPI-scaled), Ubuntu 22.04 LTS.

---

## 🔒 Industrial Safety & Security

Safety is the core of the HYDRA-UMC architecture. We implement multi-level protection strategies:

- **Hardware Safety**: Real-time hard-wired E-STOP line + high-priority CAN emergency broadcast (<1ms).
- **Perception Safety**: AI-driven 3D safety zones with automatic motor torque-cut upon human intrusion.
- **Network Security**: JWT-based stateless authentication + mTLS (Mutual TLS) for secure inter-node comms.
- **Data Reliability**: ECC memory support on STM32H7 + non-volatile F-RAM for tool lifecycle audit.
- **Traceability**: Comprehensive industrial logging with microsecond precision for all robotic trajectories.

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
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | Native Kotlin mobile app for real-time remote robot management. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | Cross-platform Flutter mobile app for iOS/iPadOS robotic control. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | Python-based visual editor for creating and validating URDF models. |
| [URTC](https://github.com/JuanenRac/URTC) | Universal Robot Tool Controller firmware for multi-functional end-effectors. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | Comprehensive firmware update tool for CAN-based tool controllers. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Diagnostic tool for real-time validation of URTC tool profiles over CAN. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Browser-based serial and CAN analyzer for instant hardware testing. |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-VISION-NODE** | High-speed perception node powered by Hailo-8 and CM5. |
| **HYDRA-UMC-VISION-STREAMER** | Optimized GStreamer pipeline for 8x USB 3.0 camera streams. |
| **HYDRA-UMC-DETECTION-HEF** | Library of hardware-accelerated YOLO models for industrial detection. |
| **HYDRA-UMC-SAFETY-ZONES** | Real-time 3D intrusion detection system for robotic safe-working areas. |
| **HYDRA-UMC-VISUAL-SERVOING-API** | Close-loop kinematic correction system based on image feedback. |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-COGNITIVE-NODE** | Semantic reasoning and GenAI node powered by Hailo-10. |
| **HYDRA-UMC-VLA-ENGINE** | Vision-Language-Action multimodal model implementation for robotics. |
| **HYDRA-UMC-VOICE-UI** | Local hardware-accelerated Speech-to-Action pipeline (STT/TTS). |
| **HYDRA-UMC-SEMANTIC-PLANNER** | LLM-based logical mission planner and error recovery system. |
| **HYDRA-UMC-DOCS-QA** | RAG-based AI technical assistant for on-site hardware maintenance. |

### 🐝 Orchestration & Swarm
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-ORCHESTRATOR** | Distributed system manager for multi-robot swarm coordination. |
| **HYDRA-UMC-SWARM-SYNC** | Precision Time Protocol (PTP) implementation for multi-node sync. |
| **HYDRA-UMC-PATH-PLANNER-3D** | Centralized multi-robot collision avoidance and path optimizer. |
| **HYDRA-UMC-JOB-DISPATCHER** | Priority-based mission queue for heterogeneous robot fleets. |
| **HYDRA-UMC-NODE-HEALING** | High-availability monitor and failover manager for HydraNodes. |

### 🎮 Digital Twin & Simulation
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-TWIN** | Physics-based Digital Twin engine for safe robotic simulation. |
| **HYDRA-UMC-PHYSICS-REPLICA** | High-fidelity MuJoCo/PhysX simulation of URDF kinematic chains. |
| **HYDRA-UMC-HIL-BRIDGE** | Hardware-in-the-loop interface for real-vs-virtual command syncing. |
| **HYDRA-UMC-SYNTHETIC-DATA-GEN** | Procedural generator of training datasets for Vision nodes. |

### 📊 Data & Analytics
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-DATALAKE** | Scalable time-series storage for massive industrial robotic data. |
| **HYDRA-UMC-TELEMETRY-COLLECTOR** | High-throughput ingestion node for CAN and WebSocket logs. |
| **HYDRA-UMC-ANOMALY-DETECTOR** | AI-driven predictive maintenance based on motor vibration signatures. |
| **HYDRA-UMC-PRODUCTION-REPORTS** | Automated KPI and OEE reporting engine for plant managers. |

### 🏭 Industrial Gateway
| Repository | Description |
| :--- | :--- |
| **HYDRA-UMC-GATEWAY-INDUSTRIAL** | Industry 4.0 interoperability bridge for factory standards. |
| **HYDRA-UMC-OPCUA-SERVER** | Full mapping of HydraState objects to OPC-UA address spaces. |
| **HYDRA-UMC-MQTT-BROKER** | Lightweight telemetry bridge for IoT and external integrations. |
| **HYDRA-UMC-MTCONNECT-ADAPTER** | Standardized XML/HTTP interface for machine tool monitoring. |

### 🛠️ Complementary Tools
| Repository | Description |
| :--- | :--- |
| **URTC-SMART-RACK** | Intelligent end-effector storage with lifecycle and thermal tracking. |
| **URTC-VISION-TOOL** | Integrated end-effector tool combining thermal and RGB sensors. |
| **HYDRA-UMC-WATCH** | Wearable safety dashboard and haptic emergency alert system. |
| **HYDRA-UMC-TOOL-CLI** | Powerful command-line interface for fleet DevOps and automation. |
| **HYDRA-UMC-DASHBOARD-AI** | AI-powered analytical extension for the STUDIO web dashboard. |

---

## 🤝 Contributing
This ecosystem is part of a high-tech robotic initiative. Each project has its own contribution guidelines. Please refer to individual repositories for technical details.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.
