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

## 🚀 Caratteristiche Chiave e Scalabilità

- **Scalabilità Multi-Robot**: Supporta fino a 8 unità robotiche distribuite (attualmente a 3, 4, 5 e 6 assi; scalabile a 7, 8, 9 assi e architetture di robot duali nelle versioni future).
- **Stadio Locale Integrato**: La scheda principale HYDRA-UMC è dotata di uno **Stadio Locale a 6 assi** integrato per compiti ausiliari, inclusi robot secondari, revolver ATC (Automatic Tool Changer), sincronizzazione di nastri trasportatori o portali di tavole XYZ.

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

## 📁 Catalogo dei Progetti

### 💠 Core Ecosystem (Controllo Principale)
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | Firmware di controllo movimento core per STM32H745/G474 con cinemática S-Curve. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | API Node.js headless e backend WebSocket per l'orchestrazione robotica. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | Dashboard web avanzata basata su React per il monitoraggio e il controllo 3D. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | Applicazione desktop Python/Qt ad alte prestazioni per l'automazione industriale. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | Interfaccia touch Flutter per display industriali da 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | App mobile nativa Kotlin con login biometrico per la gestione remota. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | App mobile Flutter per iOS/iPadOS con sincronizzazione WebSocket in tempo reale. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | Editor grafico URDF per convalidare e caricare modelli di robot nel catalogo. |
| [URTC](https://github.com/JuanenRac/URTC) | Firmware per controller utensili universale per oltre 25 utensili specializzati. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | Strumento GUI per aggiornamenti firmware CAN-OTA e SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Strumento di diagnostica CAN-bus con pannelli di telemetria per utensile. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Strumento Web Serial per test e analisi istantanea dell'hardware. |

### 👁️ Nodo AI di Visione (Ottimizzato per Hailo-8)
| Repository | Descrizione |
| :--- | :--- |
| **HYDRA-UMC-VISION-NODE** | Nodo di percezione ad alta velocità per 8 flussi simultanei di telecamere USB 3.0. |
| **HYDRA-VISION-STREAMER** | Pipeline GStreamer/MediaMTX ottimizzata per il relay video industriale. |
| **HYDRA-DETECTION-HEF** | Libreria di modelli YOLO accelerati in hardware per QA di componenti e SMD. |
| **HYDRA-SAFETY-ZONES** | Rilevamento intrusioni AI in tempo reale per la protezione del volume di lavoro. |
| **HYDRA-VISUAL-SERVOING-API** | Feedback cinematico basato su immagini per la correzione della posa sub-millimetrica. |

### 🧠 Nodo AI Cognitivo (Ottimizzato per Hailo-10)
| Repository | Descrizione |
| :--- | :--- |
| **HYDRA-UMC-COGNITIVE-NODE** | Nodo di ragionamento semantico per pianificazione logica e controllo vocale. |
| **HYDRA-VLA-ENGINE** | Implementazione del modello Vision-Language-Action per l'esecuzione di compiti complessi. |
| **HYDRA-VOICE-UI** | Pipeline locale STT/TTS per l'interazione naturale con l'operatore. |
| **HYDRA-SEMANTIC-PLANNER** | Orchestratore basato su LLM con recupero errori contestuale. |
| **HYDRA-DOCS-QA** | Assistente AI basato su RAG addestrato su manuali tecnici e codice sorgente. |

### 🐝 Orchestrazione & Sciame
| Repository | Descrizione |
| :--- | :--- |
| **HYDRA-UMC-ORCHESTRATOR** | Fleet manager per coordinamento multi-robot ed evitamento collisioni. |
| **HYDRA-SWARM-SYNC** | Sincronizzazione PTP per il coordinamento di robot con precisione nanosecondo. |
| **HYDRA-PATH-PLANNER-3D** | Ottimizzatore di percorsi distribuito per sciami in spazi condivisi. |
| **HYDRA-JOB-DISPATCHER** | Scheduler di compiti basato su priorità per flotte eterogenee. |
| **HYDRA-NODE-HEALING** | Monitor ad alta affidabilità con failover trasparente delle missioni. |

### 🎮 Digital Twin & Simulazione
| Repository | Descrizione |
| :--- | :--- |
| **HYDRA-UMC-TWIN** | Motore di simulazione fisica ad alta fedeltà per test sicuri. |
| **HYDRA-PHYSICS-REPLICA** | Simulazione fisica reale (MuJoCo/PhysX) di catene URDF. |
| **HYDRA-HIL-BRIDGE** | Interfaccia Hardware-in-the-loop per la coerenza tra stato reale e virtuale. |
| **HYDRA-SYNTHETIC-DATA-GEN** | Generatore di dataset procedurali per l'addestramento di modelli AI. |

### 📊 Dati & Analisi
| Repository | Descrizione |
| :--- | :--- |
| **HYDRA-UMC-DATALAKE** | Storage Big Data per telemetria industriale massiva multi-robot. |
| **HYDRA-TELEMETRY-COLLECTOR** | Ingestore ad alta velocità per log CAN, WebSocket e di sistema. |
| **HYDRA-ANOMALY-DETECTOR** | Motore di manutenzione predittiva basato sulle firme di vibrazione dei motori. |
| **HYDRA-PRODUCTION-REPORTS** | Generazione automatizzata di OEE e KPI per la gestione di impianti. |

### 🏭 Gateway Industriale
| Repository | Descrizione |
| :--- | :--- |
| **HYDRA-UMC-GATEWAY-INDUSTRIAL** | Ponte di interoperabilità per standard di fabbrica (OPC-UA/MQTT). |
| **HYDRA-OPCUA-SERVER** | Mappatura degli oggetti HydraState su nodi standard OPC-UA. |
| **HYDRA-MQTT-BROKER** | Ponte di telemetria per integrazioni IoT e dashboard esterne. |
| **HYDRA-MTCONNECT-ADAPTER** | Interfaccia standardizzata per il monitoraggio dello stato di macchine e robot. |

### 🛠️ Strumenti Complementari
| Repository | Descrizione |
| :--- | :--- |
| **URTC-SMART-RACK** | Storage intelligente di utensili con preriscaldamento e audit del ciclo di vita. |
| **URTC-VISION-TOOL** | Testa utensile con telecamere termica e RGB integrate per QA attiva. |
| **HYDRA-UMC-WATCH** | Dashboard di emergenza wearable con avvisi di sicurezza aptici. |
| **HYDRA-UMC-TOOL-CLI** | Interfaccia a riga di comando per automazione flotta, flashing e devops. |
| **HYDRA-UMC-DASHBOARD-AI** | Estensione AI per dashboard web per analisi in linguaggio naturale. |

---

## 🤝 Contribuire
Questo ecosistema fa parte di un'iniziativa robotica ad alta tecnologia. Ogni progetto ha le proprie linee guida per il contributo. Fare riferimento ai singoli repository per i dettagli tecnici.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licenza GPL-3.0.
