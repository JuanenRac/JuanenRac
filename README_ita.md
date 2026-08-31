<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner dell'ecosistema HYDRA-UMC" width="100%">
</p>

# Ecosistema HYDRA-UMC / URTC 🤖🚀

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
  <img src="https://img.shields.io/badge/Piattaforma-STM32%20%7C%20CM5-red.svg" alt="Piattaforma">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Potenza AI">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Benvenuti nell'**Ecosistema HYDRA-UMC**, una piattaforma di robotica industriale multistrato che spazia dal firmware in tempo reale di basso livello all'IA cognitiva di alto livello. Questa organizzazione ospita numerosi progetti specializzati progettati per lavorare in perfetta sincronia per l'automazione di micro-fabbriche e la robotica a sciame.

## 📈 Avanzamento dell'Ecosistema

`[█████████▊░░░░░░░░░░] 49%` — Indicazione orientativa. Il traguardo 100% è un ecosistema integrato operante su hardware reale.

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

## 📁 Catalogo dei Progetti

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
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | Livello di piattaforma Raspberry Pi OS per CM5: profili riproducibili, configurazione, diagnostica, ciclo di vita dei servizi e aggiornamenti; non è una nuova distribuzione Linux. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | Contratti versionati, client leggeri e verifiche di conformità condivisi per servizi, interfacce, adattatori CM5 e URTC; non sostituisce le API dei fornitori. |

### 💠 Controllo core e client operatore
| Repository | Descrizione |
| :--- | :--- |

### 💠 Controllo core e client operatore
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


### 🔧 Core e strumenti URTC
| Repository | Descrizione |
| :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | Firmware per controller utensili universale per oltre 25 utensili specializzati. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | Strumento GUI per aggiornamenti firmware CAN-OTA e SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Strumento di diagnostica CAN-bus con pannelli di telemetria per utensile. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Strumento Web Serial per test e analisi istantanea dell'hardware. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | Storage intelligente di utensili con preriscaldamento e audit del ciclo di vita. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | Testa utensile con telecamere termica e RGB integrate per QA attiva. |

### 👁️ Nodo AI di Visione (Ottimizzato per Hailo-8)
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | Nodo di percezione ad alta velocità per 8 flussi simultanei di telecamere USB 3.0. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | Pipeline GStreamer/MediaMTX ottimizzata per il relay video industriale. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | Libreria di modelli YOLO accelerati in hardware per QA di componenti e SMD. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | Rilevamento intrusioni AI in tempo reale per la protezione del volume di lavoro. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | Feedback cinematico basato su immagini per la correzione della posa sub-millimetrica. |

### 🧠 Nodo AI Cognitivo (Ottimizzato per Hailo-10)
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | Nodo di ragionamento semantico per pianificazione logica e controllo vocale. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | Implementazione del modello Vision-Language-Action per l'esecuzione di compiti complessi. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | Pipeline locale STT/TTS per l'interazione naturale con l'operatore. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | Orchestratore basato su LLM con recupero errori contestuale. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | Assistente AI basato su RAG addestrato su manuali tecnici e codice sorgente. |

### 🐝 Orchestrazione & Sciame
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | Fleet manager per coordinamento multi-robot ed evitamento collisioni. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | Sincronizzazione PTP per il coordinamento di robot con precisione nanosecondo. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | Ottimizzatore di percorsi distribuito per sciami in spazi condivisi. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | Scheduler di compiti basato su priorità per flotte eterogenee. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | Monitor ad alta affidabilità con failover trasparente delle missioni. |

### 🎮 Digital Twin & Simulazione
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | Motore di simulazione fisica ad alta fedeltà per test sicuri. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | Simulazione fisica reale (MuJoCo/PhysX) di catene URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | Interfaccia Hardware-in-the-loop per la coerenza tra stato reale e virtuale. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | Generatore di dataset procedurali per l'addestramento di modelli AI. |

### 📊 Dati & Analisi
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | Storage Big Data per telemetria industriale massiva multi-robot. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | Ingestore ad alta velocità per log CAN, WebSocket e di sistema. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | Motore di manutenzione predittiva basato sulle firme di vibrazione dei motori. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | Generazione automatizzata di OEE e KPI per la gestione di impianti. |

### 🏭 Gateway Industriale
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | Ponte di interoperabilità per standard di fabbrica (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | Mappatura degli oggetti HydraState su nodi standard OPC-UA. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | Ponte di telemetria per integrazioni IoT e dashboard esterne. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | Interfaccia standardizzata per il monitoraggio dello stato di macchine e robot. |

### 🌉 Bridge di automazione esterna
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | Confine di coordinamento ROS 2 bidirezionale: topic di osservazione, servizi di ispezione e azioni di cella annullabili. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | Coordinatore tracciabile di passaggio PCB per OpenPnP e carico o scarico assistito da robot. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | Bridge sicuro attorno al software di stampa 3D; il primo adattatore convalida Moonraker senza sostituire il firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | Coordinatore di ausiliari della cella CNC; traiettoria e sicurezza restano del controller nativo. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | Coordinatore di ausiliari della cella laser che non può armare, attivare o aggirare gli interlock. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | Confine di coordinamento per droidi con gambe/umanoidi: vocabolario di azioni cammina/prendi/posa filtrato dal contratto di sicurezza condiviso; andatura ed equilibrio restano al controller nativo del droide. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | Confine di coordinamento per flotte AGV/AMR: trasformazione dal sistema di riferimento di fabbrica a quello locale di un AMR più un vocabolario di ordini ispirato a VDA-5050; la pianificazione del percorso resta alla navigazione nativa dell'AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | Confine di coordinamento per UAV con fotocamera: vocabolario di richieste di volo con nome più un watchdog deterministico di heartbeat/perdita di collegamento. |

### 🛠️ Strumenti Complementari
| Repository | Descrizione |
| :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | Dashboard di emergenza wearable con avvisi di sicurezza aptici. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | Interfaccia a riga di comando per automazione flotta, flashing e devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | Estensione AI per dashboard web per analisi in linguaggio naturale. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | Strumento GUI/CLI multipiattaforma per rilevare, installare e aggiornare manualmente ogni progetto dell'ecosistema. |

---

## 🤝 Contribuire
Questo ecosistema fa parte di un'iniziativa robotica ad alta tecnologia. Ogni progetto ha le proprie linee guida per il contributo. Fare riferimento ai singoli repository per i dettagli tecnici.

Le etichette delle issue sono standardizzate su tutti i repo dell'ecosistema a partire da [`.github/labels.yml`](.github/labels.yml) in questo stesso repo, sincronizzate da [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - modifica quel singolo file per cambiare un'etichetta ovunque in una volta, invece di farlo a mano repo per repo. A differenza della dashboard qui sotto, questo elenco è statico (una vera matrice GitHub Actions, non scoperta dinamica) - un nuovo repo richiede anche una voce lì, non solo un vero `hydra-umc.project.json`.

Una dashboard di stato in tempo reale che copre ogni repo pubblico che dichiara `ecosystem: HYDRA-UMC` nel proprio `hydra-umc.project.json` (stack, target di deployment, versione corrente - letta direttamente dal branch predefinito di ciascun repo, scoperta dinamicamente senza elenco fisso) viene rigenerata ogni ora (e immediatamente dopo un push rilevante) da [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) e servita da `docs/` tramite GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. La v3 aggiunge una vera classificazione di maturità per progetto (scaffolding / functional / established / production, ciascuna decisa a partire dal CHANGELOG reale di quel progetto - vedi il docstring del modulo [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) per il criterio esatto), il suo ruolo (API / UI / CLI / firmware / libreria / servizio / strumento), un vero albero famiglia/genitore-figlio, e note per progetto su cosa è realmente implementato oggi.

## 🧭 Collaborazione GitHub

Il [modello di collaborazione GitHub](docs/GITHUB_COLLABORATION.md) definisce un’unica Wiki centrale, un unico Project dell’ecosistema, l’ambito delle Discussions, i criteri di release e il confine dell’automazione condivisa. I [moduli delle issue](.github/ISSUE_TEMPLATE/) e il [modello di pull request](.github/PULL_REQUEST_TEMPLATE.md) centralizzati rendono tracciabile il lavoro software, la validazione hardware e la documentazione senza duplicare i manuali dei progetti.

Il workflow di community health è manuale e in simulazione per impostazione predefinita. Dopo aver configurato `COMMUNITY_HEALTH_SYNC_TOKEN`, può copiare solo questi modelli gestiti in ogni repository che pubblica un manifesto HYDRA-UMC; non elimina mai un modello specifico di progetto.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licenza GPL-3.0.
