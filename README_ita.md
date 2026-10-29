<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Electro Hobby 3D Banner" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  🇺🇸 <a href="README.md">English</a> |
  <a href="README\_spa.md">🇪🇸 Español</a> |
  <a href="README\_fra.md">🇫🇷 Français</a> |
  <b>🇮🇹 Italiano</b> |
  <a href="README\_deu.md">🇩🇪 Deutsch</a> |
  <a href="README\_zho.md">🇨🇳 简体中文</a> |
  <a href="README\_jpn.md">🇯🇵 日本語</a> |
  <a href="README\_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

Quattro ecosistemi ingegneristici indipendenti, un unico autore. **HYDRA-UMC** è una piattaforma di robotica industriale multistrato, che spazia dal firmware in tempo reale all'IA cognitiva. **URTC** è il suo sottosistema universale per gli strumenti robotici: firmware in tempo reale e strumenti desktop/web per l'effettore finale di un robot, sviluppato come prodotto autonomo con versionamento e strumenti di manutenzione indipendenti. **A.R.M.O.R.** è un ecosistema separato e pubblico di sicurezza perimetrale e domotica: rilevamento di presenza radar, monitoraggio solare ed elettrico, e un coordinatore centrale con client web e mobili. **EH3D Fabrication Suite** è un ecosistema software integrato per la prototipazione di PCB, la preparazione CAM, l'ispezione tramite visione artificiale, la gestione Pick \& Place e il controllo CNC/Laser interfacciato con l'hardware HYDRA-UMC e macchinari d'officina specializzati.


## 🚦 Stato del progetto

Ogni riga è una parte di questo repository e il semaforo dice a che punto è oggi. È scritta in base a ciò che il repository può mostrare (test, compilazioni, esecuzioni), non a ciò che è previsto.

🟢 Fatto e verificato · 🟡 Funziona, con limiti noti · 🟠 Fatto a metà o non ancora verificato · 🔴 Non fatto o non funzionante

| Area | Stato | Cosa significa qui |
|---|---|---|
| Dashboard e monitoraggio | 🟢 | Il dashboard di stato, il controllo della CI, la matrice di salute, il controllo dei link e il riepilogo dei rilasci girano in modo programmato in GitHub Actions e le loro ultime esecuzioni passano. |
| Test | 🟢 | 51 test passano (`python -m unittest discover -s tests`): il catalogo, il monitoraggio, i banner, la creazione della roadmap e la parità dei README. |
| Catalogo e versioni | 🟡 | La colonna Versione di ogni tabella di progetti è compilata da uno script a partire dal manifesto di ciascun repository e verificata, quindi non invecchia; le descrizioni di una riga sono scritte a mano. |
| Barre di avanzamento | 🟢 | La percentuale di ogni ecosistema è calcolata da `scripts/ecosystem_progress.py` con la maturità e la prova che ogni repository dichiara nel proprio manifesto, e si rinnova con il dashboard; il traguardo del 100% resta un ecosistema completamente integrato che funziona su hardware reale. |
| Parità in otto lingue | 🟢 | Gli otto file README mantengono le stesse sezioni, gli stessi link GitHub e lo stesso numero di righe di tabella, e un test fallisce se uno di essi diverge. |
| Hardware reale | 🟢 | Non applicabile: questo repository contiene il profilo e la sua automazione, nulla qui gira su hardware. |
| Documentazione | 🟢 | README in otto lingue con i quattro ecosistemi, la guida alla collaborazione su GitHub e i file della community. |

## 🧭 Su Electro Hobby 3D e il suo aggiornatore

**Electro Hobby 3D** è il laboratorio di JuanenRac: elettronica, robotica e software progettati, costruiti, programmati e provati nello stesso posto. Ogni repository si descrive con un manifest, ha la propria documentazione e dice cosa è stato provato e cosa no su hardware reale.

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) è **l'aggiornatore dei quattro ecosistemi**: una finestra e una riga di comando che passano il lavoro all'aggiornatore di ciascun ecosistema, i quali scoprono, installano e aggiornano i suoi repository. Ogni ecosistema qui sotto nomina il proprio.

| Ecosistema | Cos'è | Aggiornatore |
|---|---|---|
| **HYDRA-UMC** | Robotica industriale e controllo di macchine, dal firmware in tempo reale all'IA cognitiva | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | Firmware e strumenti per gli organi terminali di un robot | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | Sicurezza perimetrale e domotica | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | Prototipazione di PCB, CAM, CNC e laser, pick and place | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

\---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Benvenuti nell'**ecosistema HYDRA-UMC**, una piattaforma di robotica industriale multistrato che spazia dal firmware in tempo reale a basso livello all'IA cognitiva di alto livello. Questa organizzazione ospita molti progetti specializzati progettati per lavorare in perfetta sintonia per l'automazione di micro-fabbriche e la robotica a sciame.

**Aggiornatore:** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) rileva, installa e aggiorna i repository di questo ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo fa per tutti e quattro.

## 📈 Avanzamento dell'ecosistema

<!-- progress:hydra-umc -->
`\[█████████▎░░░░░░░░░░] 46%` — Calcolato da dati reali: la maturità e la prova che ciascuno dei suoi 56 repository dichiara nel proprio manifesto. Il traguardo del 100% è un ecosistema completamente integrato che funziona su hardware reale.
<!-- /progress:hydra-umc -->

> \[!IMPORTANT]
> 🛠️ \*\*Progetto in pausa — costruzione dell'hardware reale.\*\* Lo sviluppo attivo è temporaneamente sospeso mentre la cella robotica fisica (telai, cablaggi, le reali schede CM5 e STM32) viene assemblata concretamente, in modo che la prossima fase di lavoro disponga di hardware reale su cui eseguirsi e validarsi, e non solo di una barra di avanzamento. Il lavoro riprenderà una volta completato tale assemblaggio.

\---

## 🚀 Caratteristiche principali e scalabilità

* **Scalabilità multi-robot**: Supporta fino a 8 unità robotiche distribuite (3, 4, 5 e 6 DOF attuali; scalabile fino a 7, 8, 9 DOF e architetture a doppio robot nelle future versioni).
* **Fase locale integrata**: La scheda principale HYDRA-UMC dispone di una **Fase Locale a 6 assi** integrata per attività ausiliarie, tra cui robot secondari, revolver ATC (Automatic Tool Changer), sincronizzazione di nastri trasportatori o portali per tavole XYZ.

\---

## 🏗️ Architettura dell'ecosistema

L'ecosistema v1.1 è una piattaforma di prodotti a livelli: si basa su tecnologie consolidate Linux e Raspberry Pi anziché creare un nuovo sistema operativo o sostituire le API dei produttori.

1. **Base della piattaforma**: Raspberry Pi OS ARM64 e i servizi Linux standard forniscono la base CM5 supportata.
2. **Piattaforma e contratti**: **HYDRA-UMC-OS** raggruppa profili riproducibili, servizi, diagnostica e aggiornamenti su Raspberry Pi OS; **HYDRA-UMC-SDK** pubblica contratti con versione, client leggeri e banchi di conformità.
3. **Esecuzione in tempo reale**: Il firmware **HYDRA-UMC** gestisce i limiti di movimento, i watchdog e l'arresto di sicurezza su STM32/MCU; lo strumento stesso, e la sua autorità in tempo reale sull'effettore finale, appartengono al separato ecosistema **URTC** sottostante.
4. **Coordinamento e operazioni**: I servizi server, l'assegnazione dei lavori, la telemetria e la configurazione coordinano i dispositivi senza aggirare il limite di sicurezza della MCU.
5. **Interfacce operatore**: Studio, Suite, DSI, web, desktop, mobile e client CLI utilizzano i contratti dell'SDK.
6. **Percezione e intelligenza**: Visione, Hailo e i servizi cognitivi propongono osservazioni o piani; non possiedono alcuna autorità di sicurezza fisica.
7. **Ingegneria, industria e dati**: Digital Twin, HIL/fisica, gateway OPC-UA/MQTT/MTConnect e servizi di dati validano e integrano il sistema.

Per indicazioni sull'implementazione, iniziare con la documentazione pubblica di architettura e servizi in **HYDRA-UMC-OS**, quindi utilizzare i contratti e le regole di conformità in **HYDRA-UMC-SDK**. L'autorità di sicurezza della MCU è preservata in ogni flusso.

\---

## 🛠️ Stack tecnologico e Strumenti

L'ecosistema sfrutta uno stack moderno e ad alte prestazioni per un'affidabilità critica:

### 💠 Embedded e Tempo Reale (Esecuzione)

* **Microcontrollori**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
* **Framework**: FreeRTOS (modalità AMP), CMSIS-DSP, STM32 HAL/LL.
* **Protocolli**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (IPC Slave 50MHz), I2C, UART.
* **Cinematica**: Generazione profili ad S, Cinematica Inversa in tempo reale (IK).

### 🧠 IA Edge e Percezione (Intelligenza)

* **Acceleratori**: Hailo-8 (26 TOPS) per 8 flussi di telecamere simultanei, Hailo-10 (40 TOPS) per GenAI.
* **Modelli**: YOLOv10 (Rilevamento), OpenVLA (Azione), Whisper (Voce), Llama-3 (Ragionamento).
* **Inter-nodo**: gRPC su Protobuf e scambio di metadati SPI-DMA ad alta velocità.

### 🌐 Backend e Coordinamento (Coordinamento)

* **Runtime**: Node.js 20+ (API), Rust 1.80+ (Orchestratore), Go (CLI).
* **Infrastruttura**: Express, Fastify, Socket.io (WebSocket), gRPC.
* **Database**: InfluxDB/TimescaleDB (Telemetria), Redis (Stato), SQLite.

### 💻 Dashboard e Interfaccia Utente (Interfaccia)

* **Web**: React 19, Vite, Three.js (Viewport 3D), Tailwind CSS.
* **Nativo**: Python 3.12/PySide6 (Suite), Kotlin (Android Nativo), Flutter 3.x (iOS \& DSI).

\---

## 📋 Requisiti di sistema

* **Nodo di calcolo**: Raspberry Pi CM5 (4GB+ RAM) con memoria NVMe/eMMC.
* **Hardware IA**: Moduli M.2 Hailo-8/Hailo-10 (Key M).
* **Bus di campo**: Ethernet Gigabit per LAN e FDCAN (ISO 11898-1:2015) per gli attuatori.
* **OS Client**: Android 10+, iOS 15+, Windows 10/11 (High-DPI), Ubuntu 22.04 LTS.

\---

## 🔒 Sicurezza Industriale

* **Livello E-STOP**: Linea di emergenza cablata + Frame di emergenza CAN ad alta priorità (<1ms).
* **Sicurezza IA**: Zone di sicurezza 3D con interruzione automatica della coppia motore in caso di intrusione umana.
* **Sicurezza informatica**: Autenticazione stateless basata su JWT + mTLS per traffico inter-nodo sicuro.
* **Integrità**: F-RAM non volatile per l'audit del ciclo di vita degli strumenti e il ripristino dello stato.

\---

## 🔧 Hardware Hacking: Costruire la propria scheda carrier

La scheda di controllo del robot è basata su un **Raspberry Pi CM5**, e il doppio connettore Hirose DF40 del CM5 è un pinout fisso, ufficiale e pubblico (Tabella 5 del datasheet ufficiale CM5 di Raspberry Pi), non un aspetto definito da questo progetto. Ciò significa che una scheda carrier di terze parti compatibile è un progetto reale e realizzabile, non un esercizio di ingegneria inversa:

* **Inizia da qui**: [`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - quali pin fissi del CM5 questa scheda utilizza effettivamente (Ethernet, i 2 PHY USB3 SuperSpeed nativi, l'intestazione della ventola di raffreddamento lato CM5) e perché, riorganizzati per funzione dalla tabella ufficiale dei pin.
* **Il punto di accesso facile**: l'intestazione **GPIO standard a 40 pin del Raspberry Pi** (la stessa disposizione "B+" invariata dal 2014) è disposta su questa scheda esattamente come su qualsiasi Raspberry Pi: gli HAT RPi esistenti e gli strumenti GPIO funzionano senza modifiche. Alcune posizioni già utilizzate dal collegamento STM32 di questa scheda sono serigrafate/annotate per sapere quali saltare.
* **Per andare oltre**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) spiega come il CM5, il "Cervello Cinematico" STM32H745 e il "Controller Robot" STM32G474 comunicano tra loro (SPI1 + FDCAN1 + la casella di posta IPC CM7↔CM4) - il livello che la riprogettazione di una carrier deve preservare per rimanere compatibile con il firmware di questo progetto.
* Ciascun documento di pinout indica chiaramente se è **CONFERMATO** (preso direttamente da una tabella di datasheet ufficiale) o **PROPOSTO** (scelta di routing di questo progetto, aperta a variazioni su una carrier derivata) - leggere questa riga di stato prima di considerare un'assegnazione di segnale come definitiva.

Non si tratta di un tutorial guidato (non esiste una carrier "giusta" in assoluto per ogni caso d'uso), bensì del materiale di riferimento reale di cui un progettista hardware esperto ha bisogno per partire da una mappa di pin nota e funzionante anziché da un semplice datasheet.

\---

## 📁 Catalogo dei Progetti HYDRA-UMC

Nuovo nell'ecosistema? `./starter-kit.sh` (o `starter-kit.bat` su Windows) clona 13 repository principali — un set iniziale selezionato con cura — come directory sorelle all'interno di un'unica cartella: il layout standard presupposto da ogni script multi-repository qui presente. Un secondo argomento clona invece un intero ecosistema, rilevato dinamicamente tramite il suo manifesto: `hydra-umc`, `urtc`, `armor`, `eh3d` o `all` (ad esempio `./starter-kit.sh \~/work armor`). Eseguire nuovamente il comando è sicuro: tutto ciò che è già clonato rimane inalterato. Da lì, il programma di aggiornamento di ciascun ecosistema — o [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) per tutti e quattro — può verificare le versioni e compilare/aggiornare qualsiasi altro progetto.

### 🧱 Fondamenta della Piattaforma e Contratti

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.4|Livello di piattaforma Raspberry Pi OS per CM5: profili riproducibili, configurazione, diagnostica, ciclo di vita dei servizi e aggiornamenti; non è una nuova distribuzione Linux.|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.3.8|Contratti condivisi con versione, client leggeri e banchi di conformità per servizi, UI e adattatori CM5; non sostituisce le API dei produttori.|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.5|Registro dichiarativo di manifesti di adattatori e validatore per connettori di macchine esterne; estende l'idea di contratto dell'SDK alle macchine esterne senza sostituire i progetti di gateway industriale.|

### 💠 Controllo Principale e Client Operatore

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.3|Firmware di controllo del movimento principale per STM32H745/G474 con cinematica ad S.|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.2|API Node.js headless e backend WebSocket per l'orchestrazione robotica.|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.2|Dashboard web avanzata basata su React per il monitoraggio e il controllo 3D del robot.|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.7.1|Applicazione desktop Python/Qt ad alte prestazioni per l'automazione industriale.|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.7|Interfaccia tattile dedicata basata su Flutter per display industriali da 7" (CM5).|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.2|App mobile nativa in Kotlin con accesso biometrico per la gestione remota del robot.|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.7|App mobile Flutter per iOS/iPadOS con sincronizzazione WebSocket in tempo reale.|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.5|Editor URDF grafico per validare e inviare modelli di robot al catalogo.|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.7|Editor di modelli STL desktop — trasforma, sostituisce, rimuove e aggiunge parti reali nel catalogo di modelli condiviso.|

### 👁️ Nodo di Visione IA (Ottimizzato per Hailo-8)

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.6|Nodo di percezione ad alta velocità per 8 flussi di telecamere USB 3.0 simultanei.|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.1|Pipeline GStreamer/MediaMTX ottimizzata per il relay video industriale.|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.5|Libreria di modelli YOLO accelerati via hardware per il controllo qualità di componenti e SMD.|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.5|Rilevamento di intrusioni IA in tempo reale per la protezione del volume di lavoro robotico.|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.2.0|Feedback cinematico basato su immagini per la correzione della posa sub-millimetrica.|

### 🧠 Nodo di IA Cognitiva (Ottimizzato per Hailo-10)

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.5|Nodo di ragionamento semantico per la pianificazione logica delle missioni e il controllo vocale.|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.1.8|Implementazione del modello Vision-Language-Action per l'esecuzione di compiti complessi.|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.1.8|Pipeline STT/TTS locale e privata per l'interazione in linguaggio naturale con l'operatore.|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.4|Orchestratore di missioni basato su LLM con recupero degli errori contestuale.|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.5|Assistente IA basato su RAG addestrato su manuali tecnici e codice sorgente.|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.7|Tecnico di manutenzione IA locale e regolato da policy: una politica di livello di rischio fisso e una allowlist di strumenti oggi, con una difesa reale e testata che dimostra come un documento recuperato malevolo non possa mai attivare una chiamata di strumento o divulgare un segreto — l'IA non ottiene mai autorità generando una risposta.|

### 🐝 Orchestrazione e Sciame

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.1.9|Gestore di flotta per il coordinamento multi-robot e la prevenzione delle collisioni.|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.5|Sincronizzazione PTP (Precision Time Protocol) per la sincronizzazione dei robot al nanosecondo.|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.1|Ottimizzatore di percorsi distribuito per sciami di robot in spazi di lavoro condivisi.|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.3|Schedulatore di compiti basato su priorità per flotte di robot eterogenee.|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.1.9|Monitor ad alta disponibilità con failover trasparente delle missioni.|

### 🎮 Digital Twin e Simulazione

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.1.0|Motore di simulazione fisica ad alta fedeltà per test dei robot senza rischi.|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.0.9|Simulazione fisica del mondo reale (MuJoCo/PhysX) di catene URDF.|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.1.0|Interfaccia Hardware-in-the-loop per la sincronizzazione dei comandi reali vs virtuali.|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.1|Generatore procedurale di dataset di addestramento per i nodi di visione.|

### 📊 Dati e Analitica

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.1.9|Storage Big Data per enormi volumi di dati di robotica industriale.|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.8|Ingestore ad alto throughput per CAN, WebSocket e log di sistema.|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.1.8|Motore di manutenzione predittiva basato sulle firme di vibrazione dei motori.|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.6|Generazione automatizzata di OEE e KPI per la gestione di impianti industriali.|

### 🏭 Gateway Industriale

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.6|Bridge di interoperabilità Industria 4.0 per gli standard di fabbrica (OPC-UA/MQTT).|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.2.0|Mappatura degli oggetti robotici HydraState su nodi OPC-UA standard.|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.7|Bridge di telemetria per integrazioni IoT e dashboard esterne.|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.1.9|Interfaccia standardizzata per il monitoraggio dello stato di macchine utensili e robot.|

### 🌉 Bridge di Automazione Esterni

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.3|Confine di coordinamento bidirezionale ROS 2: topic per l'osservazione, servizi per l'ispezione e azioni annullabili per i lavori di cella.|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.2.0|Coordinatore tracciabile di passaggio PCB per OpenPnP e caricamento/scaricamento assistito da robot.|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.1.9|Bridge sicuro attorno al software nativo per stampanti 3D; il primo adattatore valida la prontezza di Moonraker senza sostituire il firmware.|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.2.0|Coordinatore ausiliario per cella CNC; la traiettoria del controller e la sicurezza della macchina rimangono native.|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.1.8|Coordinatore ausiliario per cella laser che non può armare, attivare o bypassare gli interblocchi laser.|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.3|Confine di coordinamento per droidi bipedi/umanoidi: vocabolario di azioni denominate (camminare/prendere/posare) regolato dal contratto di sicurezza condiviso; andatura e bilanciamento rimangono sul controller proprio del droide.|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.4|Confine di coordinamento per flotte AGV/AMR: trasformazione di coordinate da fabbrica a locale più un vocabolario di ordini ispirato a VDA-5050; la pianificazione del percorso rimane gestita dalla navigazione dell'AMR.|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.5|Confine di coordinamento per UAV dotati di telecamera: vocabolario di richieste di volo denominate più un watchdog deterministico di rilevamento perdita di battito cardiaco/connessione.|

### 🛠️ Strumenti Complementari

|Repository|Versione|Descrizione|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.6|Dashboard d'emergenza indossabile con avvisi di sicurezza aptici.|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.1.8|Interfaccia a riga di comando per l'automazione della flotta, il flashing e il devops.|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.7|Estensione IA per dashboard web che fornisce approfondimenti in linguaggio naturale.|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.4.9|Strumento GUI/CLI multi-piattaforma per rilevare, installare e aggiornare manualmente ogni progetto dell'ecosistema.|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.2|Strumento desktop Windows/Linux che compila un'immagine CM5 pronta per il flashing, precaricata con le versioni più recenti dell'ecosistema e configurazione al primo avvio in stile Raspberry-Pi-Imager.|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.1.9|Coordinatore di incidenti di manutenzione: un ruolo edge a basso privilegio raccoglie uno snapshot pulito di inventario/salute, un ruolo di piano di controllo lo rende di sola lettura e chiede a un fornitore di IA di suggerire una diagnosi — non applica mai patch o distribuisce alcunché.|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.1.9|Host di sviluppo riproducibile: uno schema di configurazione regolato da policy e un inventario di manifesti oggi, in evoluzione verso un esecutore isolato di task/workspace coordinato con OPS-AGENT — nessun task possiede mai permessi di deploy a meno che un documento non lo conceda esplicitamente.|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.4|Architettura, interfacce, baseline di sicurezza, matrice delle capacità e catalogo di progetti generato dell'ecosistema, oltre agli strumenti che confrontano tutte le repository.|

\---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="URTC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Tools-25%2B%20profiles-blueviolet.svg" alt="Tools">
</p>

**URTC (Universal Robot Tool Controller)** è un prodotto a sé stante e non una cartella di sottosistema di HYDRA-UMC: firmware in tempo reale e una famiglia di strumenti desktop/web per l'effettore finale di un robot, sviluppati, versionati e mantenuti in modo indipendente. Un cambia-utensili dotato di URTC si coordina con il controller di cella di HYDRA-UMC tramite FDCAN, ma il comportamento in tempo reale dell'utensile, il watchdog e lo stato sicuro sono di esclusiva competenza di URTC — il controller di cella non può aggirarli, e URTC non dipende da HYDRA-UMC per essere sviluppato, flashato o diagnosticato.

**Aggiornatore:** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) rileva, installa e aggiorna i repository di questo ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo fa per tutti e quattro.

<!-- progress:urtc -->
`\[███████▋░░░░░░░░░░░░] 38%` — Calcolato da dati reali: la maturità e la prova che ciascuno dei suoi 10 repository dichiara nel proprio manifesto. Il traguardo del 100% è un ecosistema completamente integrato che funziona su hardware reale.
<!-- /progress:urtc -->

## 🏗️ Come funziona URTC

1. **Firmware dell'utensile**: Il firmware STM32 proprietario di URTC esegue ciascuno dei 25+ profili di utensili specializzati (pinze, erogatori, sonde, mandrini e altro), ognuno con tempistiche, limiti e comportamenti in caso di guasto propri.
2. **Aggiornamento sul campo**: CAN-OTA invia una nuova immagine firmware sullo stesso bus CAN già utilizzato dall'utensile, con un percorso SWD/JTAG full-chip (URTC-FLASHER) come fallback che non dipende mai dal fatto che il firmware nativo dell'utensile sia operativo.
3. **Diagnostica in tempo reale**: URTC-TESTER valida il comportamento CAN in tempo reale di un utensile rispetto al suo profilo dichiarato senza richiedere un'officina completa; URTC-WEB-STUDIO fa lo stesso da una scheda del browser tramite Web Serial, senza alcuna installazione.
4. **Stoccaggio e ciclo di vita**: URTC-SMART-RACK custodisce gli utensili tra un lavoro e l'altro, ne pre-riscalda uno prima del passaggio e mantiene una traccia di audit del ciclo di vita (cicli, guasti, ultima calibrazione) per singolo utensile fisico, non per tipo di utensile.
5. **QA attiva**: URTC-VISION-TOOL è esso stesso uno strumento — una testa utensile con telecamere termiche e RGB integrate per l'ispezione della qualità in-process, non una telecamera esterna imbullonata su un altro utensile.
6. **Base condivisa**: **URTC-COMMON** contiene il protocollo CAN della testa utensile come dati, con codice generato e vettori di conformità; **URTC-DOCS** raccoglie l'architettura, la baseline di sicurezza e la matrice delle capacità.

## 🛠️ Stack tecnologico

* **Firmware**: STM32, FDCAN (bus condiviso con il controller di cella), CAN-OTA, fallback SWD/JTAG.
* **Strumenti desktop**: client GUI multi-piattaforma per flashing e diagnostica (URTC-FLASHER, URTC-TESTER).
* **Strumenti browser**: API Web Serial per test hardware senza installazione (URTC-WEB-STUDIO).
* **Dati del ciclo di vita**: traccia di audit non volatile per utensile, condivisa con l'approccio di integrità F-RAM di HYDRA-UMC.

## 🔒 Sicurezza

Ogni profilo di utensile gestisce il proprio watchdog e comportamento in caso di guasto, indipendentemente dal livello E-STOP del controller di cella — un utensile che perde il proprio budget temporale o l'heartbeat CAN passa autonomamente al proprio stato sicuro dichiarato, anziché attendere un comando esterno. Il preriscaldamento di URTC-SMART-RACK è limitato dagli stessi limiti termici per utensile dichiarati nel suo profilo, controllati nella stessa traccia del ciclo di vita utilizzata da un'officina per determinare se un utensile è ancora idoneo al servizio.

## 📁 Catalogo dei Progetti URTC

|Repository|Versione|Descrizione|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.4.1|Firmware del controller universale per utensili robotici per oltre 25 utensili specializzati.|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.4.1|Strumento GUI per aggiornamenti firmware CAN-OTA e SWD/JTAG full-chip.|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.4.2|Strumento diagnostico per la validazione in tempo reale dei profili utensile URTC su CAN.|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.3.7|Strumento Web Serial basato su browser per test e analisi hardware istantanei.|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.2.1|Stoccaggio intelligente di utensili con preriscaldamento automatico e audit del ciclo di vita.|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.5|Testa utensile con telecamere termiche e RGB integrate per QA attiva.|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.1.8|Rileva, installa e aggiorna le repository URTC su una macchina a partire dai relativi manifest.|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.1.1|Architettura, interfacce, baseline di sicurezza, matrice delle capacità, nota di studio del protocollo CAN e catalogo di progetti generato dell'ecosistema URTC, oltre agli strumenti che confrontano tutte le repository.|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.0.8|Il protocollo CAN della testa utensile come dati: una specifica, codice C, TypeScript e Python generato, vettori di conformità e trasporti Python.|
|[URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY)|0.0.2|Gateway davanti al bus CAN di URTC: elenco di identificatori consentiti, limite di frequenza e chiave di sessione.|

\---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ARMOR_BANNER.svg" alt="A.R.M.O.R. Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range)** è un ecosistema pubblico separato di sicurezza perimetrale e domotica — nessuna parentela con HYDRA-UMC o URTC se non per lo stesso autore e le stesse convenzioni ingegneristiche (manifest con versione, contratto di messaggistica condiviso, interfacce in otto lingue). I suoi nodi di campo sorvegliano il perimetro di una proprietà e il suo impianto solare/elettrico; il server centrale e i client permettono a un operatore di visualizzare e agire su ciò che essi segnalano. Le note di versione e maturità sottostanti derivano direttamente dal manifest e dalla matrice delle capacità di ciascuna repository, adottando la stessa convenzione di trasparenza già impiegata dalla dashboard di HYDRA-UMC.

**Aggiornatore:** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) rileva, installa e aggiorna i repository di questo ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo fa per tutti e quattro.

<!-- progress:armor -->
`\[█████████████░░░░░░░] 65%` — Calcolato da dati reali: la maturità e la prova che ciascuno dei suoi 18 repository dichiara nel proprio manifesto. Il traguardo del 100% è un ecosistema completamente integrato che funziona su hardware reale.
<!-- /progress:armor -->

## 🏗️ Come è costruito A.R.M.O.R.

1. **Contratto condiviso**: **ARMOR-COMMON** definisce il significato dei messaggi — JSON Schema, un validatore Python e tipi TypeScript/Kotlin generati che qualsiasi altra repository consuma senza ridefinirli mai.
2. **Nodi di campo**: Firmware ESP32-S3 per il rilevamento radar/presenza (**ARMOR-RADAR**), monitoraggio di inverter solari e batterie (**ARMOR-SOLAR**), misurazione elettrica con capacità di commutazione (**ARMOR-ELECTRICAL**), e il pannello d'allarme dell'abitazione (**ARMOR-ALARM**); un agente Python (**ARMOR-NETWORK**) monitora la rete locale della casa e la connettività Internet da una macchina già collegata ad essa.
3. **Coordinatore centrale**: **ARMOR-SERVER** gestisce stato, utenti, allarmi, automazioni ed evidenze video delle telecamere; **ARMOR-SERVER-AI** e **ARMOR-VOICE-AI** aggiungono una politica visiva spiegabile e intenti vocali offline che non azionano mai alcun attuatore in autonomia.
4. **Client operatore**: **ARMOR-STUDIO** (web) e **ARMOR-ANDROID-CONTROL** (mobile) sono client del server centrale e non dialogano mai direttamente con la rete di campo. **ARMOR-HMI** è un pannello touch a parete (uno Waveshare ESP32-S3-Touch-LCD-7C-BOX) che mostra lo stato, permette l'inserimento, il disinserimento e l'ack degli allarmi, e ospiterà l'assistente vocale.
5. **Deployment e test**: **ARMOR-DEVOPS** distribuisce l'intero grafo dei servizi; **ARMOR-SIMULATOR** riproduce scenari e guasti ripetibili in assenza di hardware reale; **ARMOR-HARDWARE** raccoglie il design dei cabinet e la relativa matrice di accettazione al banco.
6. **Operazioni dell'ecosistema**: **ARMOR-UPDATER** individua, installa e aggiorna ogni repository A.R.M.O.R. su una macchina, seguendo lo stesso design atomico basato su verifica di HYDRA-UMC-UPDATER; **ARMOR-DOCS** costituisce la documentazione d'architettura canonica e la matrice delle capacità. **ARMOR-STUDIO** è inoltre in grado di aggiornare i servizi sulla macchina centrale a partire da pacchetti firmati con la chiave di rilascio dell'ecosistema, verificando ciascuna firma prima dell'installazione.

## 🔒 Trasparenza e Sicurezza

A.R.M.O.R. segue la stessa regola già applicata dalla dashboard di HYDRA-UMC: un’affermazione è reale solo quando è verificata, e ciascuna repository dichiara apertamente cosa è stato o non è stato eseguito su hardware reale. Nessun componente di questo ecosistema controlla attualmente la rete elettrica domestica o accessi fisici; i nodi di campo osservano e segnalano, e qualsiasi futura capacità di commutazione viene progettata e verificata prima di essere abilitata.

## 📁 Catalogo dei Progetti A.R.M.O.R.

|Repository|Versione|Descrizione|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.7.7|Contratti di messaggio, validatori, vettori di conformità, tipi generati, OpenAPI, launcher condiviso.|
|[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)|0.8.0.5|Firmware per nodo di campo ESP32-S3, decoder per sensori di presenza LD2450, LD2461, core testato su host, aggiornamenti da GitHub con barra di avanzamento e mappa live.|
|[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)|0.5.9|Nodo gateway solare: firmware ESP32-S3 e relativo pannello (dieci porte seriali), protocolli per inverter Voltronic / MPP Solar e batterie Pylontech e ANT-BMS.|
|[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)|0.5.0|Nodo elettrico: firmware (sedici misuratori PZEM su una singola linea seriale, pannello web, MQTT), frame dei misuratori, messaggi delle letture di rete e regole di commutazione.|
|[ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM)|0.4.8|Nodo e pannello d'allarme: firmware (zone cablate, sirena, sensori e sirene Zigbee, pannello web in sette lingue) e regole di inserimento, ritardi, allarme e PIN, testato su computer; continua a sorvegliare e assume il controllo della radio Zigbee quando il server è offline. Mai eseguito su scheda fisica.|
|[ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI)|0.4.0|Pannello touch per Waveshare ESP32-S3-Touch-LCD-7C-BOX: stato del sistema su schermo a muro, inserimento/disinserimento/riconoscimento, voce push-to-talk e pagina web di un nodo; il firmware non è mai stato eseguito su scheda fisica.|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.4|Monitor di rete locale: dispositivi sulla rete domestica, stato di Internet (e di chi è la responsabilità di un'interruzione), variazioni; svolge solo funzioni di osservazione.|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.8.0.6|Stato centrale (persistito), utenti, cronologia eventi, allarmi, dispositivi, automazioni, letture solari ed elettriche, rete locale, servizi di sistema, watchdog telecamere, telecamere, prove video, audit, aggiornamenti firmware dei nodi firmati obbligatoriamente, notifiche Telegram e Home Assistant, comandi vocali e utilizzo da remoto (secondo fattore, sessioni terminabili, policy remota).|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.7|Servizio di monitoraggio del movimento, selezione del profilo visivo, policy di fusione spiegabile, registro dei motori.|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.3|Zone di telecamere, maschere e regole di rilevamento (loitering, un evento per visita); nessun modello di rilevamento integrato al momento.|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.1|Servizio vocale offline: quindici comandi in otto lingue, interazioni vocali del pannello a muro, inserimento e disinserimento confermati tramite token firmato.|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.1.0|Console operativa, allarmi, dispositivi, automazioni, utenti, cronologia, regole di avviso, PTZ, mappa radar, menu solari ed elettrici, rete locale, servizi di sistema, meteo, ricerca e configurazione nodi, aggiornamenti firmware dei nodi, notifiche e designer di siti 2D/3D.|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.7|Client operatore Android: inserimento e disinserimento, allarmi, dispositivi, radar live, inverter solari e batterie, cronologia, notifiche di allarme, assistente per comandi scritti e vocali e configuratore dei nodi.|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.6|Design dei cabinet (custodia d'angolo per radar; checklist per i nodi solari, elettrici e d'allarme) e matrice di accettazione al banco.|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.7|Topologia Compose, installer per banco di prova del server centrale, backup e ripristino, profilo TLS, broker MQTT dedicato, servizi di osservazione e vocali, agente amministrativo.|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.6|Scenari e guasti ripetibili.|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.5|Rileva, installa e aggiorna le repository dell'ecosistema (atomico tramite verifica, nessun GITHUB\_TOKEN richiesto).|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.1.2|Documentazione canonica e matrice delle capacità.|

\---

# ⚡ EH3D FABRICATION SUITE

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/EH3D_BANNER.svg" alt="EH3D Fabrication Suite Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Desktop%20%7C%20Embedded-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-C%2B%2B%20%7C%20Python%20%7C%20Qt-orange.svg" alt="Stack">
  <img src="https://img.shields.io/badge/Hardware-HYDRA--UMC%20%7C%20Bungard%20%7C%20ESP32-green.svg" alt="Hardware">
</p>

**EH3D Fabrication Suite** è un ecosistema software multi-repository dedicato, progettato su misura per la prototipazione rapida di circuiti stampati (PCB), la preparazione di percorsi utensile CAM, l'ispezione tramite visione artificiale, la gestione Pick \& Place (PnP) e il controllo CNC/Laser multi-macchina. Offre interoperabilità nativa con i nodi hardware **HYDRA-UMC** (STM32H7 + Jetson Orin NX + Hailo NPU) insieme a un parco macchine d'officina che comprende sistemi di fresatura industriali (Bungard CCD tramite gateway RS-232 ESP32-S3), router CNC (JuanenCNC) e incisori laser a diodo (JuanenLaser).

**Aggiornatore:** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) rileva, installa e aggiorna i repository di questo ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo fa per tutti e quattro.

<!-- progress:eh3d -->
`\[██░░░░░░░░░░░░░░░░░░] 10%` — Calcolato da dati reali: la maturità e la prova che ciascuno dei suoi 8 repository dichiara nel proprio manifesto. Il traguardo del 100% è un ecosistema completamente integrato che funziona su hardware reale.
<!-- /progress:eh3d -->

## 🏗️ Come funziona EH3D Fabrication Suite

1. **Gestione Centrale**: **EH3D-SUITE-LAUNCHER** individua i nodi hardware attivi sulla rete locale (gateway HYDRA-UMC ed ESP32), gestisce pacchetti unificati `.eh3dproj` e orchestra gli aggiornamenti degli strumenti.
2. **Pipeline di Elaborazione CAM**: Strumenti CAD/CAM specializzati gestiscono le singole fasi di fabbricazione:

   * **EH3D-ISOCAM**: Isolamento delle tracce Gerber RS-274X/X2, algoritmi di Voronoi e rimozione del rame residuo (rubout).
   * **EH3D-DRILLPRO**: Elaborazione foratura Excellon/NC Drill, tabelle punte e cicli di foratura profonda.
   * **EH3D-ROUTEPRO**: Fresatura contorno scheda, creazione linguette di supporto (tabs) e strategie di ingresso in rampa.
   * **EH3D-BUNGARD-GUI**: Interfaccia moderna per le macchine Bungard CCD: un launcher e un visualizzatore con le viste in pianta e isometrica del lavoro.
   * **EH3D-LASER-CAM**: Algoritmi di dithering raster e modulazione di potenza vettoriale per il taglio laser.
   * **EH3D-STENCILCAM**: Elaborazione di maschere di pasta saldante (pastemask) per la generazione di stencil SMD.
3. **Esecuzione e Controllo in Tempo Reale**: **EH3D-MOTIONCNC** pilota i movimenti della macchina tramite streaming ad alta velocità G-Code/HP-GL, integrato con **EH3D-AUTOLEVEL** per la mappatura topografica dell'asse Z e **EH3D-PENDANT-GUI** per lo zero manuale (G54/G55) e il jog portatile.
4. **IA Edge e Ispezione**: **EH3D-VISION-STUDIO** sfrutta la NPU Hailo di HYDRA-UMC per eseguire l'allineamento della telecamera in tempo reale, il rilevamento automatico di riferimenti (fiducial) e l'ispezione dell'usura degli utensili.
5. **Assemblaggio e Dati Ausiliari**: **EH3D-PNP-MANAGER** gestisce le coordinate centroidi Pick \& Place e i feeder, mentre **EH3D-TOOL-MANAGER** mantiene un database di magazzino utensili unificato tra tutti i moduli CAM.

## 📁 Catalogo dei Progetti EH3D Fabrication Suite

### 💠 Controllo centrale e client operatore
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|Dashboard principale dell'ecosistema per la gestione dei progetti (.eh3dproj), aggiornamenti, impostazioni globali e rilevamento nodi.|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.1|Schemi dati, specifiche di progetto unificate (.eh3dproj), costanti globali e asset grafici UI.|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.1|Documentazione dell'ecosistema, guide di assemblaggio, specifiche tecniche dei gateway e manuali di integrazione.|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.1|Libreria C++/Python condivisa contenente parser Gerber/Excellon/G-Code/HP-GL, geometria 2D/3D e protocolli.|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.1|Rileva, installa e aggiorna le repository dell'ecosistema (atomico tramite verifica, nessun GITHUB\_TOKEN richiesto).|
|[EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER)|0.0.1|Server in Rust con interfaccia REST e websocket: utenti, macchine e lavori, pianificazione di lavori di foratura e fresatura con le librerie di DRILLPRO e ROUTEPRO, un lavoro alla volta per macchina.|
|[EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)|0.0.1|Client web in Rust per EH3D-SERVER.|

### 💠 Progetti di foratura, contornatura e fresatura:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.3|App CAM Excellon/NC Drill, gestione punte da trapano, ottimizzazione percorsi e cicli di foratura profonda.|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.3|App CAM fresatura contorni scheda, svuotamento tasche (pocketing), linguette di tenuta e strategie di ingresso in rampa CNC.|
|[EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI)|0.0.1|Interfaccia moderna per le macchine Bungard CCD: un launcher dei programmi classici di foratura e fresatura e un visualizzatore del lavoro sul tavolo.|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.1|GUI di controllo numerico in tempo reale, visualizzatore G-code 3D, tastatura e supporto streaming multi-macchina.|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|Database di magazzino utensili condiviso per il monitoraggio delle ore d'usura, preset di taglio e avanzamenti su tutti i tool CAM EH3D.|

### 💠 Progetti laser:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|App CAM laser per dithering d'immagine, conversione raster/vettore e controllo dinamico della potenza PWM.|

### 💠 Progetti CAM:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|App di elaborazione CAM Gerber RS-274X/X2, isolamento tracce Voronoi/Offset, rubout e simulazione di incisione.|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|Simulatore 3D di percorsi utensile e rimozione materiale, rilevatore di collisioni e stima del tempo di ciclo G-Code/HP-GL.|

### 💠 Progetti Gerber:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|Strumento di ispezione CAM leggero per l'allineamento dei layer Gerber e la visualizzazione rapida.|

### 💠 Progetti Pick&Place:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|Utility di conversione pastemask per la generazione di percorsi di taglio per stencil SMD tramite laser e plotter.|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|Gestore di assemblaggio SMD ispirato a OpenPnP, lettore di centroidi, controllo feeder e centratura componenti via visione.|

### 💠 Progetti di nodi:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)|0.0.2|Nodo ESP32-S3 per la scatola di una macchina Bungard CCD: l'RS-232 della sua unità di controllo via Ethernet o Wi-Fi, con le lampade della macchina e l'azionamento del mandrino sulla stessa scheda.|
|[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)|0.0.1|Controller manuale touch da 10 pollici / mobile con ESP32-P4/ESP32-C6 per il jog in tempo reale, l'azzeramento (G54/G55) e l'arresto di emergenza delle macchine Bungard CCD.|
|[EH3D-NODE-HMI-GUI](https://github.com/JuanenRac/EH3D-NODE-HMI-GUI)|0.0.1|Controller manuale touch da 10 pollici / mobile di uso generale con ESP32-P4/ESP32-C6 per il jog in tempo reale, l'azzeramento (G54/G55) e l'arresto di emergenza.|

### 💠 Progetti FENIX:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-FENIX-PCB](https://github.com/JuanenRac/EH3D-FENIX-PCB)|0.0.1|Ambiente EDA: acquisizione di schemi, layout di PCB, strumenti di verifica, simulazione di circuiti e moduli specializzati per alimentatori switching (SMPS) e RF.|
|[EH3D-FENIX-CAD](https://github.com/JuanenRac/EH3D-FENIX-CAD)|0.0.1|CAD meccanico parametrico dedicato alla progettazione di contenitori, telai e dissipatori termici.|
|[EH3D-DESIGN-VERIFIER](https://github.com/JuanenRac/EH3D-DESIGN-VERIFIER)|0.0.1|Verificatore ingegneristico completo per le validazioni incrociate e il controllo di qualità del progetto.|
|[EH3D-VALIDATION-LAB](https://github.com/JuanenRac/EH3D-VALIDATION-LAB)|0.0.1|Ambiente di test incaricato di gestire i casi d'uso di riferimento e i test di regressione del sistema.|
|[EH3D-DESIGN-HISTORY](https://github.com/JuanenRac/EH3D-DESIGN-HISTORY)|0.0.1|Sistema di controllo di versione che conserva la storia semantica e l'evoluzione logica del progetto.|
|[EH3D-PROJECT-PASSPORT](https://github.com/JuanenRac/EH3D-PROJECT-PASSPORT)|0.0.1|Generatore del passaporto tecnico archiviabile e riproducibile per la verifica completa di un progetto.|
|[EH3D-COMPONENT-INTELLIGENCE](https://github.com/JuanenRac/EH3D-COMPONENT-INTELLIGENCE)|0.0.1|Database tecnico avanzato arricchito con metadati sui componenti elettronici.|
|[EH3D-MANUFACTURING-PROFILE](https://github.com/JuanenRac/EH3D-MANUFACTURING-PROFILE)|0.0.1|Gestore di profili per le capacità dei macchinari di ciascuna fabbrica e i vincoli tecnici dei fornitori.|
|[EH3D-THERMAL-LAB](https://github.com/JuanenRac/EH3D-THERMAL-LAB)|0.0.1|Laboratorio di simulazione termica progressiva accoppiato direttamente al progetto fisico.|
|[EH3D-LAB-BRIDGE](https://github.com/JuanenRac/EH3D-LAB-BRIDGE)|0.0.1|Modulo di correlazione che funge da ponte diretto tra i dati di simulazione e le misure reali di laboratorio.|
|[EH3D-DESIGN-EXPLORER](https://github.com/JuanenRac/EH3D-DESIGN-EXPLORER)|0.0.1|Ambiente di esplorazione per confrontare e analizzare alternative o rami del progetto.|

### 💠 Progetti ANDROID/IOS:
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-ANDROID-CONTROL](https://github.com/JuanenRac/EH3D-ANDROID-CONTROL)|0.0.1|App Android client di EH3D-SERVER.|
|[EH3D-IOS-CONTROL](https://github.com/JuanenRac/EH3D-IOS-CONTROL)|0.0.1|App iOS client di EH3D-SERVER.|

### 🛠️ Strumenti complementari
|Repository|Versione|Descrizione|
|-|-|-|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|Dashboard di visione Edge AI per allineamento telecamera, addestramento marker fiducial e ispezione visiva tramite HYDRA-UMC.|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|Processore di mesh per altezze topografiche (Z-Probing) e interpolazione G-code per la compensazione superficiale.|

\---

## 🤝 Contribuire

Ogni ecosistema rappresenta un'iniziativa autonoma con i propri progetti. Ciascun progetto adotta linee guida di contribuzione specifiche. Si prega di fare riferimento alle singole repository per i dettagli tecnici.

Le etichette delle issue sono standardizzate in ogni repository HYDRA-UMC tramite il file [`.github/labels.yml`](.github/labels.yml) presente in questa stessa repository e sincronizzato da [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) — è sufficiente modificare quel singolo file per aggiornare un'etichetta ovunque contemporaneamente, anziché agire manualmente per ogni repository. A differenza della dashboard sottostante, questo elenco è statico (una vera e propria matrice di GitHub Actions, non una scoperta dinamica): una repository appena aggiunta necessita anch'essa di una voce dedicata, e non solo di un file `hydra-umc.project.json`.

Una dashboard di stato in tempo reale che copre ogni repository pubblica dei quattro ecosistemi — ciascuna scoperta autonomamente tramite il proprio manifest (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`, più `electro-hobby-3d.project.json` per le repository cross-ecosistema), letta direttamente dal branch di default di ciascuna repository senza elenchi fissi — viene rigenerata da [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) immediatamente al push su un progetto (tramite il `dashboard-dispatch.yml` di ciascuna repository) e, come rete di sicurezza, due volte all'ora, venendo pubblicata da `docs/` tramite GitHub Pages: [**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/). Mostra stack, target di deploy e versione corrente, una classificazione reale della maturità per progetto (scaffolding / functional / established / production, determinata dal CHANGELOG di ogni progetto — vedi [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)), il relativo ruolo (API / UI / CLI / firmware / libreria / servizio / strumento), un albero genealogico genitore-figlio e note puntuali su ciò che risulta implementato alla data odierna. Il file [`ecosystem-catalog.json`](ecosystem-catalog.json) elenca tali ecosistemi e i relativi manifest in un unico posto, e la compilazione della dashboard si interrompe in caso di discrepanza.

## 🧭 Collaborazione su GitHub

Il [modello di collaborazione GitHub](docs/GITHUB_COLLABORATION.md) definisce una Wiki centrale, un Progetto di ecosistema, l'ambito delle Discussioni, i criteri di rilascio e il confine di automazione condiviso. I moduli per le issue gestiti centralmente ([`ISSUE\_TEMPLATE`](.github/ISSUE_TEMPLATE/)) e il template di pull-request ([`PULL\_REQUEST\_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)) rendono tracciabili il software, la validazione hardware e il lavoro di documentazione senza duplicare i manuali di progetto.

Il workflow di salute della community è intenzionalmente manuale e impostato in modalità dry-run per default. Una volta configurato il token `COMMUNITY\_HEALTH\_SYNC\_TOKEN`, è possibile copiare esclusivamente questi template gestiti in ogni repository che pubblica un manifest HYDRA-UMC; il sistema non cancella mai un template specifico di un progetto.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licenza GPL-3.0.

