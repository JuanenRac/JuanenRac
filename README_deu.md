<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ökosystem Banner" width="100%">
</p>

# HYDRA-UMC / URTC Ökosystem 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  🇩🇪 <b>Deutsch</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Lizenz-GPL%203.0-blue.svg" alt="Lizenz GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Plattform-STM32%20%7C%20CM5-red.svg" alt="Plattform">
  <img src="https://img.shields.io/badge/KI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="KI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Willkommen im **HYDRA-UMC-Ökosystem**, einer mehrschichtigen industriellen Robotikplattform, die von Low-Level-Echtzeit-Firmware bis hin zu kognitiver High-Level-KI reicht. Diese Organisation umfasst 44 spezialisierte Projekte, die für eine perfekte Synchronisation bei der Mikrofabrik-Automatisierung und Schwarmrobotik konzipiert sind.

---

## 🏗️ Ökosystem-Architektur

Das Ökosystem ist in 6 funktionale Schichten unterteilt, die autonome, kollaborative und intelligente Roboteroperationen ermöglichen:

1.  **Ausführungsschicht**: STM32-basierte Firmware (H745/G474) für submillimetergenaue Präzision und Hochgeschwindigkeits-FDCAN-Ansteuerung.
2.  **Intelligenzschicht**: Edge-KI, angetrieben durch **Hailo-8** (Reflexwahrnehmung) und **Hailo-10** (kognitives Denken).
3.  **Koordinationsschicht**: Eigenständige Node.js-Backends und verteilte Schwarm-Orchestratoren.
4.  **Schnittstellenschicht**: Web- (React), Desktop- (Qt6), Mobil- (Kotlin/Flutter) und DSI-Touch-Dashboards.
5.  **Virtuelle Schicht**: Hochpräzise Digital Twin-Engines (Rust/Bevy) für eine sichere Vor-Validierung.
6.  **Unterstützungsschicht**: Industrie 4.0-Gateways (OPC-UA/MQTT) und vorausschauende Big-Data-Wartung.

---

## 🛠️ Technologie-Stack & Tools

Das Ökosystem nutzt einen modernen Hochleistungs-Stack für unternehmenskritische Zuverlässigkeit:

### 💠 Embedded & Echtzeit (Ausführung)
- **Mikrocontroller**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Frameworks**: FreeRTOS (AMP-Modus), CMSIS-DSP, STM32 HAL/LL.
- **Protokolle**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (50MHz Slave IPC), I2C, UART.
- **Kinematik**: S-Kurven-Profilgenerierung, Echtzeit-Inverse Kinematik (IK).

### 🧠 Edge-KI & Wahrnehmung (Intelligenz)
- **Beschleuniger**: Hailo-8 (26 TOPS) für 8-Kamera-Vision, Hailo-10 (40 TOPS) for GenAI.
- **Modelle**: YOLOv10 (Erkennung), OpenVLA (Aktion), Whisper (Stimme), Llama-3 (Denken).
- **Inter-Knoten**: gRPC über Protobuf und Hochgeschwindigkeits-SPI-DMA-Metadatenaustausch.

### 🌐 Backend & Koordination (Koordination)
- **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orchestrator), Go (CLI).
- **Infrastruktur**: Express, Fastify, Socket.io (WebSocket), gRPC.
- **Datenbank**: InfluxDB/TimescaleDB (Telemetrie), Redis (Status), SQLite.

### 💻 Dashboards & Benutzeroberfläche (Schnittstelle)
- **Web**: React 19, Vite, Three.js (3D Viewport), Tailwind CSS.
- **Nativ**: Python 3.12/PySide6 (Suite), Kotlin (Android Native), Flutter 3.x (iOS & DSI).

---

## 📋 Systemvoraussetzungen

- **Rechenknoten**: Raspberry Pi CM5 (4GB+ RAM) mit NVMe/eMMC-Speicher.
- **KI-Hardware**: Hailo-8/Hailo-10 M.2 Module (Key M).
- **Feldbus**: Gigabit-Ethernet für LAN und FDCAN (ISO 11898-1:2015) für Aktoren.
- **Client-Betriebssystem**: Android 10+, iOS 15+, Windows 10/11 (High-DPI), Ubuntu 22.04 LTS.

---

## 🔒 Industrielle Sicherheit

- **E-STOP-Schicht**: Fest verdrahtete Not-Aus-Leitung + hochpriore CAN-Notfall-Frames (<1ms).
- **KI-Sicherheit**: 3D-Sicherheitszonen mit automatischer Abschaltung des Motordrehmoments bei menschlichem Eindringen.
- **Cybersicherheit**: JWT-basierte stateless Authentifizierung + mTLS für sicheren Datenverkehr zwischen den Knoten.
- **Integrität**: Nichtflüchtiger F-RAM für die Überprüfung des Werkzeuglebenszyklus und die Statuswiederherstellung.

---

## 🤝 Mitwirken
Dieses Ökosystem ist Teil einer High-Tech-Robotik-Initiative. Jedes Projekt hat seine eigenen Richtlinien für die Mitarbeit. Technische Details finden Sie in den einzelnen Repositories.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 Lizenz.
