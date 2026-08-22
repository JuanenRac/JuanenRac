<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner dell'ecosistema HYDRA-UMC" width="100%">
</p>

# Ecosistema HYDRA-UMC / URTC 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  🇮🇹 <b>Italiano</b> |
  <a href="README_deu.md">🇩🇪 Deutsch</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Licenza-GPL%203.0-blue.svg" alt="Licenza GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Piattaforma-STM32%20%7C%20CM5-red.svg" alt="Piattaforma">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Potenza AI">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Benvenuti nell'**Ecosistema HYDRA-UMC**, una piattaforma di robotica industriale multistrato che spazia dal firmware in tempo reale di basso livello all'IA cognitiva di alto livello. Questa organizzazione ospita 44 progetti specializzati progettati per lavorare in perfetta sincronia per l'automazione di micro-fabbriche e la robotica a sciame.

---

## 🏗️ Architettura dell'Ecosistema

L'ecosistema è strutturato in 6 strati funzionali che consentono operazioni robotiche autonome, collaborative e intelligenti:

1.  **Strato di Esecuzione**: Firmware basato su STM32 (H745/G474) per precisione submillimetrica e attuazione FDCAN ad alta velocità.
2.  **Strato di Intelligenza**: AI di bordo alimentata da **Hailo-8** (percezione dei riflessi) e **Hailo-10** (ragionamento cognitivo).
3.  **Strato di Coordinamento**: Backend Node.js standalone e orchestratori di sciami distribuiti.
4.  **Strato di Interfaccia**: Dashboard web (React), Desktop (Qt6), Mobile (Kotlin/Flutter) e touch DSI.
5.  **Strato Virtuale**: Motori Digital Twin ad alta fedeltà (Rust/Bevy) per una validazione pre-fisica sicura.
6.  **Strato di Supporto**: Gateway Industria 4.0 (OPC-UA/MQTT) e manutenzione predittiva Big Data.

---

## 🛠️ Stack Tecnologico e Strumenti

L'ecosistema sfrutta uno stack moderno e ad alte prestazioni per un'affidabilità mission-critical:

### 💠 Embedded e Tempo Reale (Esecuzione)
- **Microcontrollori**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Framework**: FreeRTOS (modalità AMP), CMSIS-DSP, STM32 HAL/LL.
- **Protocolli**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (IPC slave a 50MHz), I2C, UART.
- **Cinematica**: Generazione di profili S-Curve, cinematica inversa (IK) in tempo reale.

### 🧠 AI di Bordo e Percezione (Intelligenza)
- **Acceleratori**: Hailo-8 (26 TOPS) per visione a 8 telecamere, Hailo-10 (40 TOPS) per GenAI.
- **Modelli**: YOLOv10 (rilevamento), OpenVLA (azione), Whisper (voce), Llama-3 (ragionamento).
- **Inter-nodo**: gRPC su Protobuf e scambio metadati SPI-DMA ad alta velocità.

### 🌐 Backend e Coordinamento (Coordinamento)
- **Runtime**: Node.js 20+ (API), Rust 1.80+ (Orchestratore), Go (CLI).
- **Infrastruttura**: Express, Fastify, Socket.io (WebSocket), gRPC.
- **Database**: InfluxDB/TimescaleDB (Telemetria), Redis (Stato), SQLite.

### 💻 Dashboard e Interfaccia Utente (Interfaccia)
- **Web**: React 19, Vite, Three.js (Visualizzatore 3D), Tailwind CSS.
- **Nativo**: Python 3.12/PySide6 (Suite), Kotlin (Android Nativo), Flutter 3.x (iOS e DSI).

---

## 📋 Requisiti del Sistema

- **Nodo di Calcolo**: Raspberry Pi CM5 (4GB+ RAM) con storage NVMe/eMMC.
- **Hardware AI**: Moduli M.2 Hailo-8/Hailo-10 (Key M).
- **Bus di Campo**: Gigabit Ethernet per LAN e FDCAN (ISO 11898-1:2015) per attuatori.
- **SO Client**: Android 10+, iOS 15+, Windows 10/11 (Alta Densità), Ubuntu 22.04 LTS.

---

## 🔒 Sicurezza Industriale

- **Strato E-STOP**: Linea di emergenza cablata + Frame di emergenza CAN ad alta priorità (<1ms).
- **Sicurezza AI**: Zone di sicurezza 3D con taglio automatico della coppia motore in caso di intrusione umana.
- **Cybersicurezza**: Autenticazione stateless basata su JWT + mTLS per traffico inter-nodo sicuro.
- **Integrità**: F-RAM non volatile per audit del ciclo di vita degli strumenti e recupero dello stato.

---

## 🤝 Contribuire
Questo ecosistema fa parte di un'iniziativa robotica ad alta tecnologia. Ogni progetto ha le proprie linee guida per il contributo. Fare riferimento ai singoli repository per i dettagli tecnici.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licenza GPL-3.0.
