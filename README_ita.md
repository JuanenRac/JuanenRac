<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Banner di Electro Hobby 3D" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  🇮🇹 <b>Italiano</b> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Licenza-GPL%203.0-blue.svg" alt="Licenza GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosistemi-3-00E5FF.svg" alt="Tre ecosistemi">
</p>

Tre ecosistemi ingegneristici indipendenti, un solo autore. **HYDRA-UMC** è una piattaforma di robotica industriale multistrato, dal firmware in tempo reale all'IA cognitiva. **URTC** è il suo sottosistema universale di utensili robotici: firmware in tempo reale e strumenti desktop/web per l'end-effector di un robot, sviluppato come prodotto proprio con versione e manutenzione indipendenti. **A.R.M.O.R.** è un ecosistema a parte, pubblico, di sicurezza perimetrale e domotica - rilevamento di presenza via radar, monitoraggio solare ed elettrico, e un coordinatore centrale con client web e mobile.

---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner dell'ecosistema HYDRA-UMC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Piattaforma-STM32%20%7C%20CM5-red.svg" alt="Piattaforma">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Potenza AI">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Benvenuti nell'**Ecosistema HYDRA-UMC**, una piattaforma di robotica industriale multistrato che spazia dal firmware in tempo reale di basso livello all'IA cognitiva di alto livello. Questa organizzazione ospita numerosi progetti specializzati progettati per lavorare in perfetta sincronia per l'automazione di micro-fabbriche e la robotica a sciame.

## 📈 Avanzamento dell'Ecosistema

`[██████████▊░░░░░░░░░] 54%` — Indicazione orientativa. Il traguardo 100% è un ecosistema integrato operante su hardware reale.

> [!IMPORTANT]
> 🛠️ **Progetto in pausa — costruzione dell'hardware reale.** Lo sviluppo attivo è sospeso mentre si costruisce davvero la cella fisica (telai, cablaggio, le vere schede CM5 e STM32), così che la prossima fase di lavoro abbia hardware reale su cui girare e validarsi, non solo una barra che sale. Il lavoro riprenderà una volta completata questa costruzione.

---

## 🚀 Caratteristiche Chiave e Scalabilità

- **Scalabilità Multi-Robot**: Supporta fino a 8 unità robotiche distribuite (attualmente a 3, 4, 5 e 6 assi; scalabile a 7, 8, 9 assi e architetture di robot duali nelle versioni future).
- **Stadio Locale Integrato**: La scheda principale HYDRA-UMC è dotata di uno **Stadio Locale a 6 assi** integrato per compiti ausiliari, inclusi robot secondari, revolver ATC (Automatic Tool Changer), sincronizzazione di nastri trasportatori o portali di tavole XYZ.

---

## 🏗️ Architettura dell'Ecosistema

L'ecosistema v1.1 è una piattaforma di prodotto a livelli: utilizza tecnologie Linux e Raspberry Pi consolidate, senza creare un nuovo sistema operativo né sostituire le API dei fornitori.

1.  **Base della piattaforma**: Raspberry Pi OS ARM64 e i servizi Linux standard forniscono la base CM5 supportata.
2.  **Piattaforma e contratti**: **HYDRA-UMC-OS** offre profili riproducibili, servizi, diagnostica e aggiornamenti su Raspberry Pi OS; **HYDRA-UMC-SDK** pubblica contratti versionati, client leggeri e verifiche di conformità.
3.  **Esecuzione in tempo reale**: firmware **HYDRA-UMC** e URTC su STM32/MCU mantengono limiti di movimento, watchdog e arresto sicuro.
4.  **Coordinamento e operazioni**: servizi server, distribuzione dei job, telemetria e configurazione coordinano i dispositivi senza aggirare il confine di sicurezza del MCU.
5.  **Interfacce operatore**: Studio, Suite, DSI, web, desktop, mobile e CLI usano i contratti SDK.
6.  **Percezione e intelligenza**: visione, Hailo e servizi cognitivi propongono osservazioni o piani; non hanno autorità sulla sicurezza fisica.
7.  **Ingegneria, industria e dati**: Digital Twin, HIL/fisica, gateway OPC-UA/MQTT/MTConnect e dati convalidano e integrano il sistema.

Lo sviluppo parte dall'architettura e dal modello di servizi pubblici di **HYDRA-UMC-OS**, quindi usa contratti e regole di conformità di **HYDRA-UMC-SDK**. L'autorità di sicurezza del MCU/URTC è preservata in ogni flusso.

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

## 🔧 Hardware Hacking: Costruisci il Tuo Carrier

La Robot Controller Board è costruita attorno a un **Raspberry Pi CM5**, e il connettore doppio Hirose DF40 della CM5 ha un pinout fisso, ufficiale e pubblico (Tabella 5 del datasheet ufficiale della CM5 di Raspberry Pi) - non è qualcosa che questo progetto definisce. Questo significa che un carrier compatibile di terze parti è un progetto reale e realizzabile, non un esercizio di reverse engineering:

- **Inizia qui**: [`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - quali pin fissi della CM5 usa davvero questa scheda (Ethernet, i 2 PHY USB3 SuperSpeed nativi, il connettore della ventola di raffreddamento lato CM5) e perché, riorganizzato per funzione a partire dalla tabella di pinout ufficiale.
- **La via facile**: l'**header GPIO standard a 40 pin di Raspberry Pi** (lo stesso layout "B+" invariato dal 2014) è esposto su questa scheda esattamente come su qualsiasi Raspberry Pi - gli HAT e gli strumenti GPIO esistenti funzionano senza modifiche. Alcune posizioni già usate dal collegamento STM32 proprio di questa scheda sono serigrafate/annotate per sapere quali evitare.
- **Andando oltre**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) spiega come comunicano davvero tra loro la CM5, il "Cervello Cinematico" STM32H745 e il "Robot Controller" STM32G474 (SPI1 + FDCAN1 + la mailbox IPC CM7↔CM4) - il livello che un redesign del carrier dovrebbe preservare per restare compatibile con il firmware proprio di questo progetto.
- Ogni documento di pinout indica chiaramente se è **CONFERMATO** (preso direttamente da una tabella di datasheet ufficiale) o **PROPOSTO** (una scelta di instradamento propria di questo progetto, aperta a essere diversa su un carrier derivato) - leggi quella riga di stato prima di trattare un'assegnazione di segnale come fissa.

Questo non è un tutorial guidato (non esiste un unico carrier "corretto" per ogni caso d'uso) - è il materiale di riferimento reale di cui un progettista hardware esperto ha bisogno per partire da una mappa dei pin già verificata invece che da un solo datasheet.

---

## 📁 Catalogo dei Progetti — HYDRA-UMC

Nuovo nell'ecosistema? `./starter-kit.sh` (o `starter-kit.bat` su
Windows) clona 13 repository core - un set iniziale scelto a mano, non
il catalogo completo qui sotto - come cartelle sorelle in un'unica
directory: la disposizione standard che ogni script tra repository qui
già presuppone. Rieseguirlo è sicuro: ciò che è già clonato resta
intatto. Da lì,
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(uno dei 13 appena clonati) può controllare le versioni e
compilare/aggiornare qualsiasi altro progetto del catalogo completo qui
sotto.

### 🧱 Fondazione della piattaforma e contratti
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.4.7 | Livello di piattaforma Raspberry Pi OS per CM5: profili riproducibili, configurazione, diagnostica, ciclo di vita dei servizi e aggiornamenti; non è una nuova distribuzione Linux. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.2.8 | Contratti versionati, client leggeri e verifiche di conformità condivisi per servizi, interfacce, adattatori CM5 e URTC; non sostituisce le API dei fornitori. |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.0 | Registro dichiarativo e validatore di manifesti adattatore per connettori di macchine esterne; estende la propria idea di contratto dell'SDK alle macchine esterne senza sostituire i progetti di gateway industriale. |

### 💠 Controllo core e client operatore
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.1.6 | Firmware di controllo movimento core per STM32H745/G474 con cinemática S-Curve. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.0.6 | API Node.js headless e backend WebSocket per l'orchestrazione robotica. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.7.6 | Dashboard web avanzata basata su React per il monitoraggio e il controllo 3D. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.4 | Applicazione desktop Python/Qt ad alte prestazioni per l'automazione industriale. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.0 | Interfaccia touch Flutter per display industriali da 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.6.3 | App mobile nativa Kotlin con login biometrico per la gestione remota. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.0 | App mobile Flutter per iOS/iPadOS con sincronizzazione WebSocket in tempo reale. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.0 | Editor grafico URDF per convalidare e caricare modelli di robot nel catalogo. |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.2 | Editor desktop di modelli STL - trasforma, sostituisce, rimuove e aggiunge veri pezzi nel catalogo di modelli condiviso. |


### 👁️ Nodo AI di Visione (Ottimizzato per Hailo-8)
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.0 | Nodo di percezione ad alta velocità per 8 flussi simultanei di telecamere USB 3.0. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.1.6 | Pipeline GStreamer/MediaMTX ottimizzata per il relay video industriale. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.0.9 | Libreria di modelli YOLO accelerati in hardware per QA di componenti e SMD. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.1 | Rilevamento intrusioni AI in tempo reale per la protezione del volume di lavoro. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.4 | Feedback cinematico basato su immagini per la correzione della posa sub-millimetrica. |

### 🧠 Nodo AI Cognitivo (Ottimizzato per Hailo-10)
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.1 | Nodo di ragionamento semantico per pianificazione logica e controllo vocale. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.4 | Implementazione del modello Vision-Language-Action per l'esecuzione di compiti complessi. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.3 | Pipeline locale STT/TTS per l'interazione naturale con l'operatore. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.0 | Orchestratore basato su LLM con recupero errori contestuale. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.0 | Assistente AI basato su RAG addestrato su manuali tecnici e codice sorgente. |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.2 | Tecnico IA locale con permessi controllati da politica: oggi una politica fissa dei livelli di rischio e una lista bianca di strumenti, con una difesa reale e testata che dimostra che un documento malevolo recuperato non può mai innescare una chiamata a uno strumento né rivelare un segreto - l'IA non ottiene mai autorità generando una risposta. |

### 🐝 Orchestrazione & Sciame
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.3 | Fleet manager per coordinamento multi-robot ed evitamento collisioni. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.1 | Sincronizzazione PTP per il coordinamento di robot con precisione nanosecondo. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.0.7 | Ottimizzatore di percorsi distribuito per sciami in spazi condivisi. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.1.8 | Scheduler di compiti basato su priorità per flotte eterogenee. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.4 | Monitor ad alta affidabilità con failover trasparente delle missioni. |

### 🎮 Digital Twin & Simulazione
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.7 | Motore di simulazione fisica ad alta fedeltà per test sicuri. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.6 | Simulazione fisica reale (MuJoCo/PhysX) di catene URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.6 | Interfaccia Hardware-in-the-loop per la coerenza tra stato reale e virtuale. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.0.8 | Generatore di dataset procedurali per l'addestramento di modelli AI. |

### 📊 Dati & Analisi
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.3 | Storage Big Data per telemetria industriale massiva multi-robot. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.4 | Ingestore ad alta velocità per log CAN, WebSocket e di sistema. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.3 | Motore di manutenzione predittiva basato sulle firme di vibrazione dei motori. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.2 | Generazione automatizzata di OEE e KPI per la gestione di impianti. |

### 🏭 Gateway Industriale
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.2 | Ponte di interoperabilità per standard di fabbrica (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.5 | Mappatura degli oggetti HydraState su nodi standard OPC-UA. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.2 | Ponte di telemetria per integrazioni IoT e dashboard esterne. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.4 | Interfaccia standardizzata per il monitoraggio dello stato di macchine e robot. |

### 🌉 Bridge di automazione esterna
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.0.7 | Confine di coordinamento ROS 2 bidirezionale: topic di osservazione, servizi di ispezione e azioni di cella annullabili. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.4 | Coordinatore tracciabile di passaggio PCB per OpenPnP e carico o scarico assistito da robot. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.3 | Bridge sicuro attorno al software di stampa 3D; il primo adattatore convalida Moonraker senza sostituire il firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.4 | Coordinatore di ausiliari della cella CNC; traiettoria e sicurezza restano del controller nativo. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.2 | Coordinatore di ausiliari della cella laser che non può armare, attivare o aggirare gli interlock. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.0.8 | Confine di coordinamento per droidi con gambe/umanoidi: vocabolario di azioni cammina/prendi/posa filtrato dal contratto di sicurezza condiviso; andatura ed equilibrio restano al controller nativo del droide. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.0.8 | Confine di coordinamento per flotte AGV/AMR: trasformazione dal sistema di riferimento di fabbrica a quello locale di un AMR più un vocabolario di ordini ispirato a VDA-5050; la pianificazione del percorso resta alla navigazione nativa dell'AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.0.9 | Confine di coordinamento per UAV con fotocamera: vocabolario di richieste di volo con nome più un watchdog deterministico di heartbeat/perdita di collegamento. |

### 🛠️ Strumenti Complementari
| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.2 | Dashboard di emergenza wearable con avvisi di sicurezza aptici. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.2 | Interfaccia a riga di comando per automazione flotta, flashing e devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.1 | Estensione AI per dashboard web per analisi in linguaggio naturale. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.6 | Strumento GUI/CLI multipiattaforma per rilevare, installare e aggiornare manualmente ogni progetto dell'ecosistema. |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.2.7 | Strumento desktop Windows/Linux che costruisce un'immagine della CM5 pronta da scrivere, precaricata con le versioni più aggiornate dell'ecosistema, con configurazione di primo avvio in stile Raspberry Pi Imager. |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.4 | Coordinatore di incidenti di manutenzione: un ruolo edge a basso privilegio raccoglie uno snapshot di inventario/salute sanificato, un ruolo control-plane lo rende in sola lettura e chiede a un provider di IA di suggerire una diagnosi - non applica mai una patch né distribuisce nulla. |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.3 | Server di sviluppo riproducibile: oggi uno schema di configurazione con permessi e un inventario di manifest, in crescita verso un esecutore di task/workspace isolato coordinato con OPS-AGENT - nessun task ha permesso di deploy a meno che un documento non lo conceda esplicitamente. |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="Banner dell'ecosistema URTC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Piattaforma-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Utensili-25%2B%20profili-blueviolet.svg" alt="Tools">
</p>

**URTC (Universal Robot Tool Controller)** è un prodotto proprio, non una cartella sottosistema di HYDRA-UMC: firmware in tempo reale e una famiglia di strumenti desktop/web per l'end-effector di un robot, sviluppato, versionato e mantenuto in modo indipendente. Un cambia-utensili equipaggiato con URTC si coordina con il controller di cella di HYDRA-UMC via FDCAN, ma il comportamento in tempo reale dell'utensile stesso, il suo watchdog e il suo stato sicuro sono autorità propria di URTC - il controller di cella non può aggirarla, e URTC non dipende da HYDRA-UMC per essere sviluppato, programmato o diagnosticato.

## 🏗️ Come Funziona URTC

1. **Firmware dell'utensile**: il firmware STM32 proprio di URTC esegue ciascuno dei 25+ profili di utensile specializzati (pinze, dosatori, sonde, mandrini e altro), ognuno con i propri tempi, limiti e comportamento in caso di guasto.
2. **Aggiornamento sul campo**: CAN-OTA invia una nuova immagine firmware sullo stesso bus CAN già usato dall'utensile, con una via completa via chip SWD/JTAG (URTC-FLASHER) come ripiego che non dipende mai dal firmware proprio dell'utensile.
3. **Diagnostica in tempo reale**: URTC-TESTER convalida il comportamento CAN in tempo reale di un utensile rispetto al suo profilo dichiarato senza bisogno di un'officina completa; URTC-WEB-STUDIO fa lo stesso da una scheda del browser via Web Serial, senza nulla da installare.
4. **Stoccaggio e ciclo di vita**: URTC-SMART-RACK conserva gli utensili tra un lavoro e l'altro, preriscalda un utensile prima di un cambio e mantiene un registro di audit del ciclo di vita (cicli, guasti, ultima calibrazione) per utensile fisico, non per tipo.
5. **QA attivo**: URTC-VISION-TOOL è essa stessa un utensile - una testa con proprie telecamere termica e RGB per l'ispezione di qualità durante il processo, non una telecamera esterna avvitata su un altro utensile.

## 🛠️ Stack Tecnologico

- **Firmware**: STM32, FDCAN (bus condiviso con il controller di cella), CAN-OTA, ripiego SWD/JTAG.
- **Strumenti desktop**: client GUI multipiattaforma per programmare e diagnosticare (URTC-FLASHER, URTC-TESTER).
- **Strumenti da browser**: la API Web Serial per test hardware senza installare nulla (URTC-WEB-STUDIO).
- **Dati di ciclo di vita**: registro di audit non volatile per utensile, con lo stesso criterio di integrità F-RAM di HYDRA-UMC.

## 🔒 Sicurezza

Ogni profilo di utensile porta il proprio watchdog e comportamento in caso di guasto, indipendente dallo strato E-STOP proprio del controller di cella - un utensile che perde il proprio margine di tempo o l'heartbeat CAN va al proprio stato sicuro dichiarato da solo, invece di attendere un comando esterno. Il preriscaldamento di URTC-SMART-RACK è limitato dagli stessi limiti termici per utensile dichiarati dal suo profilo, verificati nello stesso registro di ciclo di vita che un'officina usa per decidere se un utensile è ancora idoneo al servizio.

## 📁 Catalogo dei Progetti URTC

| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.1 | Firmware per controller utensili universale per oltre 25 utensili specializzati. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.2.2 | Strumento GUI per aggiornamenti firmware CAN-OTA e SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.2.3 | Strumento di diagnostica CAN-bus con pannelli di telemetria per utensile. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.2.2 | Strumento Web Serial per test e analisi istantanea dell'hardware. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.0 | Storage intelligente di utensili con preriscaldamento e audit del ciclo di vita. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.0.5 | Testa utensile con telecamere termica e RGB integrate per QA attiva. |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="Banner dell'ecosistema A.R.M.O.R." width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibilit%C3%A0-Pubblico-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar & Multimodal Observation Range)** è un ecosistema a parte, pubblico, di sicurezza perimetrale e domotica - senza relazione con HYDRA-UMC né con URTC oltre allo stesso autore e alle stesse convenzioni ingegneristiche (manifesti versionati, un contratto di messaggi condiviso, interfacce in sette lingue). I suoi nodi di campo sorvegliano il perimetro di una proprietà e il suo impianto solare/elettrico; il suo server centrale e i suoi client permettono a un operatore di vedere e agire su ciò che riportano. Le note di versione e maturità sotto provengono direttamente dal manifesto e dalla matrice delle capacità di ciascuna repository, la stessa convenzione di onestà già usata dalla dashboard di HYDRA-UMC.

## 🏗️ Come È Costruito A.R.M.O.R.

1. **Contratto condiviso**: **ARMOR-COMMON** possiede il significato dei messaggi - JSON Schema, un validatore in Python e tipi TypeScript/Kotlin generati che ogni altra repository consuma, mai ridefinisce.
2. **Nodi di campo**: firmware ESP32-S3 per rilevamento radar/presenza (**ARMOR-RADAR**), monitoraggio di inverter e batterie solari (**ARMOR-SOLAR**), e misurazione elettrica con manovra (**ARMOR-ELECTRICAL**); un agente Python (**ARMOR-NETWORK**) sorveglia la rete locale della casa e la raggiungibilità di internet da una macchina già collegata ad essa.
3. **Coordinatore centrale**: **ARMOR-SERVER** conserva stato, utenti, allarmi, automazioni ed evidenza delle telecamere; **ARMOR-SERVER-AI** e **ARMOR-VOICE-AI** aggiungono una politica visiva spiegabile e intenti vocali offline che non agiscono mai da soli.
4. **Client operatore**: **ARMOR-STUDIO** (web) e **ARMOR-ANDROID-CONTROL** (mobile) sono client del server centrale, mai della rete di campo direttamente. **ARMOR-HMI** è un pannello touch a parete (una Waveshare ESP32-S3-Touch-LCD-7C-BOX) che mostra lo stato, attiva e riconosce, e sarà la casa dell'assistente vocale.
5. **Distribuzione e test**: **ARMOR-DEVOPS** distribuisce l'intero grafo dei servizi; **ARMOR-SIMULATOR** riproduce scenari e guasti ripetibili senza hardware reale; **ARMOR-HARDWARE** porta il design dei contenitori e la sua matrice di accettazione da banco.
6. **Operazioni dell'ecosistema**: **ARMOR-UPDATER** scopre, installa e aggiorna ogni repository di A.R.M.O.R. su una macchina, lo stesso design atomico-per-verifica di HYDRA-UMC-UPDATER; **ARMOR-DOCS** è la documentazione di architettura canonica e la matrice delle capacità.

## 🔒 Onestà e Sicurezza

A.R.M.O.R. segue la stessa regola già applicata dalla dashboard di HYDRA-UMC: un'affermazione è reale solo quando è verificata, e ogni repository dice chiaramente cosa è stato provato su hardware reale e cosa no. Nulla in questo ecosistema controlla oggi la corrente elettrica di rete o l'accesso fisico; i nodi di campo osservano e riportano, e qualunque capacità di manovra futura viene progettata e rivista prima di essere attivata.

## 📁 Catalogo dei Progetti A.R.M.O.R.

| Repository | Versione | Descrizione |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.4.2 | Contratti dei messaggi, validatori, vettori di conformità e tipi generati |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.5.6 | Firmware del nodo di campo per ESP32-S3 con tre radar e un proprio pannello web |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.2.5 | Protocolli di inverter e batterie solari e messaggi di un nodo gateway |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.2.2 | Nodo elettrico: contatori, il messaggio delle letture della rete e le regole di manovra |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.1.4 | Pannello touch per la Waveshare ESP32-S3-Touch-LCD-7C-BOX: lo stato del sistema su uno schermo a parete, attiva/disattiva/riconosci, voce premi-per-parlare e la pagina web di un nodo; il firmware non è mai girato su una scheda. |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.0.6 | La rete locale: i suoi dispositivi, internet e ciò che cambia |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.5.1 | Coordinatore centrale: telemetria, allarmi, dispositivi, letture solari ed elettriche, la rete locale, i servizi di sistema e telecamere |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.3 | Politica di inferenza visiva che spiega le sue decisioni e non agisce mai |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.2.5 | Intenti vocali offline con una conferma impossibile da falsificare |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.6.8 | Console web: telecamere, radar, allarmi, menu solare ed elettrico, rete locale, servizi di sistema, meteo, un cercatore di nodi e il progettista del sito 2D/3D |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.4.9 | Client Android dell'operatore con radar 2D/3D in tempo reale |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.3 | Contenitori, elettronica e matrice di accettazione da banco |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.4.3 | Distribuzione, banco di prova del server centrale, backup e TLS |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.3 | Simulatore di telemetria offline con guasti ripetibili |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.0.7 | Rileva, installa e aggiorna i repository stessi dell'ecosistema |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.7.1 | Architettura, base di sicurezza e matrice delle capacità |

---

## 🤝 Contribuire
Questo ecosistema fa parte di un'iniziativa robotica ad alta tecnologia. Ogni progetto ha le proprie linee guida per il contributo. Fare riferimento ai singoli repository per i dettagli tecnici.

Le etichette delle issue sono standardizzate su tutti i repo dell'ecosistema a partire da [`.github/labels.yml`](.github/labels.yml) in questo stesso repo, sincronizzate da [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - modifica quel singolo file per cambiare un'etichetta ovunque in una volta, invece di farlo a mano repo per repo. A differenza della dashboard qui sotto, questo elenco è statico (una vera matrice GitHub Actions, non scoperta dinamica) - un nuovo repo richiede anche una voce lì, non solo un vero `hydra-umc.project.json`.

Una dashboard di stato in tempo reale che copre ogni repo pubblico che dichiara `ecosystem: HYDRA-UMC` nel proprio `hydra-umc.project.json` (stack, target di deployment, versione corrente - letta direttamente dal branch predefinito di ciascun repo, scoperta dinamicamente senza elenco fisso) viene rigenerata ogni ora (e immediatamente dopo un push rilevante) da [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) e servita da `docs/` tramite GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. Aggiunge una vera classificazione di maturità per progetto (scaffolding / functional / established / production, ciascuna decisa a partire dal CHANGELOG reale di quel progetto - vedi il docstring del modulo [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) per il criterio esatto), il suo ruolo (API / UI / CLI / firmware / libreria / servizio / strumento), un vero albero famiglia/genitore-figlio, e note per progetto su cosa è realmente implementato oggi. I repository propri di URTC e di A.R.M.O.R. vengono scoperti dal vivo sulla stessa dashboard esattamente come quelli di HYDRA-UMC (vedi `scripts/generate_dashboard.py`), ciascuno dichiarando il proprio campo `ecosystem` nel proprio `urtc.project.json`/`armor.project.json` - nessun elenco fisso per nessuno dei tre.

## 🧭 Collaborazione GitHub

Il [modello di collaborazione GitHub](docs/GITHUB_COLLABORATION.md) definisce un’unica Wiki centrale, un unico Project dell’ecosistema, l’ambito delle Discussions, i criteri di release e il confine dell’automazione condivisa. I [moduli delle issue](.github/ISSUE_TEMPLATE/) e il [modello di pull request](.github/PULL_REQUEST_TEMPLATE.md) centralizzati rendono tracciabile il lavoro software, la validazione hardware e la documentazione senza duplicare i manuali dei progetti.

Il workflow di community health è manuale e in simulazione per impostazione predefinita. Dopo aver configurato `COMMUNITY_HEALTH_SYNC_TOKEN`, può copiare solo questi modelli gestiti in ogni repository che pubblica un manifesto HYDRA-UMC; non elimina mai un modello specifico di progetto.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licenza GPL-3.0.

