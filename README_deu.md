<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO\_HOBBY\_3D\_BANNER.svg" alt="Electro Hobby 3D Banner" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README\_spa.md">🇪🇸 Español</a> |
  <a href="README\_fra.md">🇫🇷 Français</a> |
  <a href="README\_ita.md">🇮🇹 Italiano</a> |
  <b>🇩🇪 Deutsch</b> |
  <a href="README\_zho.md">🇨🇳 简体中文</a> |
  <a href="README\_jpn.md">🇯🇵 日本語</a> |
  <a href="README\_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

Vier unabhängige Ingenieur-Ökosysteme, ein Autor. **HYDRA-UMC** ist eine mehrschichtige industrielle Robotikplattform, die von Echtzeit-Firmware bis hin zu kognitiver KI reicht. **URTC** ist sein universelles Roboter-Werkzeug-Subsystem: Echtzeit-Firmware und Desktop-/Web-Tools für den Endeffektor eines Roboters, entwickelt als eigenständiges Produkt mit unabhängiger Versionierung und Wartungstools. **A.R.M.O.R.** ist ein separates, öffentliches Perimetersicherheits- und Heimautomatisierungs-Ökosystem – Radardraumerfassung, Solar- und Stromüberwachung sowie ein zentraler Koordinator mit Web- und Mobilclients. **EH3D Fabrication Suite** ist ein integriertes Software-Ökosystem für Leiterplatten-Prototyping, CAM-Verarbeitung, Computer-Vision-Inspektion, Pick-\&-Place-Management und CNC-/Laser-Steuerungsschnittstellen, das mit HYDRA-UMC-Hardware und spezialisierten Werkstattmaschinen verbunden ist.

\---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA\_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Willkommen im **HYDRA-UMC-Ökosystem**, einer mehrschichtigen industriellen Robotikplattform, die von hardwarenaher Echtzeit-Firmware bis hin zu kognitiver KI auf hoher Ebene reicht. Diese Organisation beherbergt viele spezialisierte Projekte, die für die Automatisierung von Mikrofabriken und Schwarmrobotik perfekt synchronisiert arbeiten.

## 📈 Ökosystem-Fortschritt

`\[██████████▊░░░░░░░░░] 54%` — Nur als Referenz. Der 100%-Meilenstein ist ein vollständig integriertes Ökosystem, das auf echter Hardware betrieben wird.

> \[!IMPORTANT]
> 🛠️ \*\*Projekt pausiert — physische Hardware wird gebaut.\*\* Die aktive Entwicklung ruht, während die physische Robotikzelle (Rahmen, Verkabelung, die echten CM5- und STM32-Platinen) real aufgebaut wird. So hat die nächste Arbeitsphase echte Hardware zum Ausführen und Validieren, anstatt nur eines Balkens, der nach oben geht. Die Arbeit wird fortgesetzt, sobald dieser Aufbau steht.

\---

## 🚀 Hauptmerkmale und Skalierbarkeit

* **Multi-Roboter-Skalierbarkeit**: Unterstützt bis zu 8 verteilte Robotereinheiten (derzeit 3, 4, 5 und 6 DOF; Skalierung auf 7, 8, 9 DOF und Dual-Robot-Architekturen in zukünftigen Versionen).
* **Integrierte lokale Stufe**: Die Hauptplatine von HYDRA-UMC verfügt über eine integrierte **6-Achsen-Lokale-Stufe** für Hilfsaufgaben, einschließlich sekundärer Roboter, ATC-Revolvern (Automatic Tool Changer), Förderbandsynchronisation oder XYZ-Tischportalen.

\---

## 🏗️ Ökosystem-Architektur

Das v1.1-Ökosystem ist eine geschichtete Produktplattform: Es baut auf etablierter Linux- und Raspberry Pi-Technologie auf, anstatt ein neues Betriebssystem zu entwickeln oder Hersteller-APIs zu ersetzen.

1. **Plattformbasis**: Raspberry Pi OS ARM64 und Standard-Linux-Dienste bilden die unterstützte CM5-Grundlage.
2. **Plattform und Verträge**: **HYDRA-UMC-OS** verpackt reproduzierbare Profile, Dienste, Diagnosen und Updates auf Raspberry Pi OS; **HYDRA-UMC-SDK** veröffentlicht versionierte Verträge, Thin Clients und Konformitätstests.
3. **Echtzeitausführung**: Die **HYDRA-UMC**-Firmware verwaltet Bewegungslimits, Watchdogs und sicheren Stopp auf STM32/MCU; das Werkzeug selbst und seine eigene Echtzeit-Autorität über den Endeffektor gehören zum separaten **URTC**-Ökosystem unten.
4. **Koordination und Betrieb**: Serverdienste, Auftragsdisposition, Telemetrie und Konfiguration koordinieren Geräte, ohne die MCU-Sicherheitsgrenze zu umgehen.
5. **Bedienerschnittstellen**: Studio-, Suite-, DSI-, Web-, Desktop-, Mobil- und CLI-Clients verwenden die SDK-Verträge.
6. **Wahrnehmung und Intelligenz**: Vision-, Hailo- und kognitive Dienste schlagen Beobachtungen oder Pläne vor; sie haben keine physische Sicherheitsautorität.
7. **Ingenieurwesen, Industrie und Daten**: Digitaler Zwilling, HIL/Physik, OPC-UA/MQTT/MTConnect-Gateways und Datendienste validieren und integrieren das System.

Beginnen Sie für Implementierungsanleitungen mit der öffentlichen Architektur- und Servicedokumentation in **HYDRA-UMC-OS** und verwenden Sie dann die Verträge und Konformitätsregeln in **HYDRA-UMC-SDK**. Die MCU-Sicherheitsautorität wird bei jedem Ablauf gewahrt.

\---

## 🛠️ Technologiestack und Tools

Das Ökosystem nutzt einen modernen, leistungsstarken Stack für mission-critical Zuverlässigkeit:

### 💠 Eingebettet und Echtzeit (Ausführung)

* **Mikrocontroller**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
* **Frameworks**: FreeRTOS (AMP-Modus), CMSIS-DSP, STM32 HAL/LL.
* **Protokolle**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (50MHz Slave IPC), I2C, UART.
* **Kinematik**: S-Kurven-Profilgenerierung, Echtzeit-Inverskinematik (IK).

### 🧠 Edge KI und Wahrnehmung (Intelligenz)

* **Beschleuniger**: Hailo-8 (26 TOPS) für 8x Kameravision, Hailo-10 (40 TOPS) für GenAI.
* **Modelle**: YOLOv10 (Erkennung), OpenVLA (Aktion), Whisper (Sprache), Llama-3 (Schlussfolgerung).
* **Zwischenknoten**: gRPC über Protobuf und High-Speed-SPI-DMA-Metadatenaustausch.

### 🌐 Backend und Koordination (Koordination)

* **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orchestrator), Go (CLI).
* **Infrastruktur**: Express, Fastify, Socket.io (WebSocket), gRPC.
* **Datenbank**: InfluxDB/TimescaleDB (Telemetrie), Redis (Status), SQLite.

### 💻 Dashboards und Benutzeroberfläche (Schnittstelle)

* **Web**: React 19, Vite, Three.js (3D-Ansichtsfenster), Tailwind CSS.
* **Nativ**: Python 3.12/PySide6 (Suite), Kotlin (Android Nativ), Flutter 3.x (iOS \& DSI).

\---

## 📋 Systemanforderungen

* **Rechenknoten**: Raspberry Pi CM5 (4 GB+ RAM) mit NVMe-/eMMC-Speicher.
* **KI-Hardware**: Hailo-8 / Hailo-10 M.2-Module (Key M).
* **Feldbus**: Gigabit-Ethernet für LAN und FDCAN (ISO 11898-1:2015) für Aktoren.
* **Client-Betriebssystem**: Android 10+, iOS 15+, Windows 10/11 (High-DPI), Ubuntu 22.04 LTS.

\---

## 🔒 Industrielle Sicherheit

* **E-STOP-Schicht**: Fest verdrahtete Notfallleitung + Prioritäre CAN-Notfall-Frames (<1ms).
* **KI-Sicherheit**: 3D-Sicherheitszonen mit automatischem Motor-Drehmoment-Stopp bei menschlichem Eindringen.
* **Cybersicherheit**: JWT-basierte zustandslose Authentifizierung + mTLS für sicheren Zwischenknotenverkehr.
* **Integrität**: Nichtflüchtiges F-RAM für Werkzeuglebenszyklus-Audit und Statuswiederherstellung.

\---

## 🔧 Hardware-Hacking: Bauen Sie Ihren eigenen Carrier

Die Roboter-Controller-Platine basiert auf einem **Raspberry Pi CM5**, und der duale Hirose DF40-Anschluss des CM5 ist eine feste, offizielle, öffentliche Pinbelegung (Tabelle 5 des offiziellen CM5-Datenblatts von Raspberry Pi) – nichts, was dieses Projekt definiert. Das bedeutet, dass ein kompatibler Träger von Drittanbietern ein reales, machbares Projekt ist und keine Reverse-Engineering-Übung:

* **Hier beginnen**: [`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) – welche der festen Pins des CM5 diese Platine tatsächlich verwendet (Ethernet, die 2 nativen USB3 SuperSpeed PHYs, die CM5-seitige Lüfter-Stiftleiste) und warum, nach Funktion aus der offiziellen Pinbelegungstabelle neu geordnet.
* **Der einfache Einstieg**: Die standardmäßige **Raspberry Pi 40-Pin-GPIO-Stiftleiste** (dasselbe „B+“-Layout, unverändert seit 2014) ist auf dieser Platine genau wie bei jedem Raspberry Pi herausgeführt – bestehende RPi-HATs und GPIO-Tools funktionieren unverändert. Einige Positionen, die die STM32-Verbindung dieser Platine bereits verwendet, sind aufgedruckt/vermerkt, damit Sie wissen, welche übersprungen werden müssen.
* **Weitergehen**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) beschreibt, wie der CM5, das STM32H745 „Kinematic Brain“ und der STM32G474 „Robot Controller“ tatsächlich miteinander kommunizieren (SPI1 + FDCAN1 + das CM7↔CM4 IPC-Postfach) – die Schicht, die ein Carrier-Redesign beibehalten muss, wenn es kompatibel bleiben soll mit der Firmware dieses Projekts.
* Jedes Pinbelegungsdokument gibt klar an, ob es **BESTÄTIGT** (direkt aus einer offiziellen Datenblatttabelle übernommen) oder **VGESCHLAGEN** ist (die eigene Routing-Wahl dieses Projekts, offen für eine andere auf einem abgeleiteten Carrier) – lesen Sie diese Statuszeile, bevor Sie eine Signalzuordnung als fest betrachten.

Dies ist kein geführtes Tutorial (es gibt keinen einzigen „richtigen“ Carrier für jeden Anwendungsfall) – es ist das reale Referenzmaterial, das ein erfahrener Hardwaredesigner benötigt, um von einer bekannten, guten Pin-Map anstelle eines reinen Datenblatts aus zu starten.

\---

## 📁 HYDRA-UMC Projektkatalog

Neu im Ökosystem? `./starter-kit.sh` (oder `starter-kit.bat` unter Windows) klont 13 Kern-Repositories – ein handverlesenes Startset – als Geschwister in einem Verzeichnis: das Standardlayout, das jedes skriptübergreifende Repo hier bereits voraussetzt. Ein zweites Argument klont stattdessen ein ganzes Ökosystem, das live anhand seines Manifests entdeckt wird: `hydra-umc`, `urtc`, `armor`, `eh3d` oder `all` (zum Beispiel `./starter-kit.sh \~/work armor`). Ein erneutes Ausführen ist sicher: Bereits geklonte Elemente bleiben unverändert. Von dort aus kann der Updater jedes Ökosystems – oder [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) für alle vier – Versionen überprüfen und jedes andere Projekt erstellen/aktualisieren.

### 🧱 Plattform-Grundlage und Verträge

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.2|Raspberry Pi OS-Plattformschicht für CM5: reproduzierbare Profile, Konfiguration, Diagnosen, Dienstlebenszyklus und Updates; keine neue Linux-Distribution.|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.3.4|Geteilte versionierte Verträge, Thin Clients und Konformitätstests für Dienste, Benutzeroberflächen und CM5-Adapter; ersetzt keine Hersteller-APIs.|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.4|Deklaratives Adapter-Manifest-Register und Validator für externe Maschinen-Connectors; erweitert die vertragliche Idee des SDKs auf externe Maschinen, ohne die Industrie-Gateway-Projekte zu ersetzen.|

### 💠 Kernsteuerung und Bediener-Clients

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.2|Kern-Bewegungssteuerungs-Firmware für STM32H745/G474 mit S-Kurven-Kinematik.|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.0|Headless Node.js-API und WebSocket-Backend für die robotergestützte Orchestrierung.|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.0|Fortgeschrittenes React-basiertes Web-Dashboard zur 3D-Roboterüberwachung und -steuerung.|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.6.9|Leistungsstarke Python/Qt-Desktop-Anwendung für die Industrieautomation.|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.6|Dedizierte Flutter-basierte Touch-Schnittstelle für 7"-Industrieprodukte (CM5).|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.1|Native Kotlin-Mobil-App mit biometrischem Login für die Fernverwaltung von Robotern.|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.6|Flutter-Mobil-App für iOS/iPadOS mit Echtzeit-WebSocket-Synchronisierung.|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.4|Grafischer URDF-Editor zum Validieren und Hochladen von Robotermodellen in den Katalog.|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.6|Desktop-STL-Modell-Editor – Transformieren, Ersetzen, Entfernen und Hinzufügen realer Teile im gemeinsamen Modellkatalog.|

### 👁️ Vision-KI-Knoten (Optimiert für Hailo-8)

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.5|Hochgeschwindigkeits-Wahrnehmungsknoten für 8 gleichzeitige USB 3.0-Kameraströme.|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.0|Optimierte GStreamer/MediaMTX-Pipeline für die industrielle Videoübertragung.|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.4|Bibliothek hardwarebeschleunigter YOLO-Modelle für SMD- und Bauteil-QS.|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.4|Echtzeit-KI-Einbrucherkennung für den Schutz des Roboter-Arbeitsvolumens.|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.1.9|Bildbasiertes kinematisches Feedback für eine Posenkorrektur im Submillimeterbereich.|

### 🧠 Kognitiver KI-Knoten (Optimiert für Hailo-10)

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.4|Semantischer Argumentationsknoten für logische Missionsplanung und Sprachsteuerung.|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.1.7|Vision-Language-Action-Modellimplementierung für komplexe Aufgabenabläufe.|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.1.7|Lokale, private STT/TTS-Pipeline für natürliche Sprachinteraktion mit dem Bediener.|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.3|LLM-basierter Missions-Orchestrator mit kontextbewusster Fehlerbehebung.|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.4|RAG-basierter KI-Assistent, trainiert auf technischen Handbüchern und Quellcode.|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.6|Lokaler, richtliniengesteuerter KI-Wartungstechniker: heute eine Richtlinie mit festem Risikoniveau und Werkzeug-Allowlist, mit einem echten, getesteten Schutz, der beweist, dass ein bösartiges, abgerufenes Dokument niemals einen Werkzeugaufruf auslösen oder ein Geheimnis preisgeben kann – die KI erhält niemals Autorisierung durch das Generieren einer Antwort.|

### 🐝 Orchestrierung und Schwarm

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.1.8|Flottenmanager für Multi-Roboter-Koordination und Kollisionsvermeidung.|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.4|PTP-Synchronisation (Precision Time Protocol) für Roboter-Synchronisation im Nanosekundenbereich.|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.0|Verteilter Pfadoptimierer für Roboter-Schwärme in gemeinsamen Arbeitsbereichen.|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.2|Prioritätsbasierter Task-Scheduler für heterogene Roboterflotten.|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.1.7|Hochverfügbarkeitsmonitor mit transparentem Missions-Failover.|

### 🎮 Digitaler Zwilling und Simulation

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.0.9|High-Fidelity-Physiksimulations-Engine für risikofreie Robotertests.|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.0.8|Echtwelt-Physiksimulation (MuJoCo/PhysX) von URDF-Ketten.|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.0.9|Hardware-in-the-Loop-Schnittstelle für die Befehlssynchronisierung zwischen Real und Virtuell.|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.0|Prozeduraler Generator von Trainingsdatensätzen für Vision-Knoten.|

### 📊 Daten und Analytik

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.1.8|Big-Data-Speicher für massive industrielle Robotikdaten.|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.7|Hochdurchsatz-Ingester für CAN, WebSocket und Systemprotokolle.|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.1.7|Predictive-Maintenance-Engine basierend auf Motorschwingungssignaturen.|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.5|Automatisierte OEE- und KPI-Generierung für die Industrieanlagenverwaltung.|

### 🏭 Industrie-Gateway

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.5|Industrie 4.0-Interoperabilitätsbrücke für Fabrikstandards (OPC-UA/MQTT).|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.1.9|Zuordnung von HydraState-Roboterobjekten zu Standard-OPC-UA-Knoten.|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.6|Telemetriebrücke für IoT-Integrationen und externe Dashboards.|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.1.8|Standardisierte Schnittstelle für die Maschinenwerkzeug- und Roboter-Gesundheitsüberwachung.|

### 🌉 Externe Automatisierungsbrücken

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.2|Bidirektionale ROS 2-Koordinationsgrenze: Topics für Beobachtung, Services für Inspektion und abbrechbare Aktionen für Zellenjobs.|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.1.9|Nachverfolgbarer Leiterplatten-Übergabekoordinator für OpenPnP und robotergestütztes Be- oder Entladen.|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.1.8|Sichere Brücke um native 3D-Druckersoftware; erster Adapter validiert die Moonraker-Bereitschaft, ohne die Firmware zu ersetzen.|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.1.9|Hilfskoordinator für CNC-Zellen; Reglerbahn und Maschinensicherheit bleiben nativ.|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.1.7|Hilfskoordinator für Laserzellen, der Lasersicherheitskreise weder scharfschalten, abfeuern noch übersteuern kann.|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.2|Koordinationsgrenze für beidige/humanoide Droiden: benanntes Walk-/Pick-/Place-Aktionsvokabular, geschützt durch den gemeinsamen Sicherheitsvertrag; Gang und Balance verbleiben auf dem eigenen Controller des Droiden.|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.3|Koordinationsgrenze für AGV/AMR-Flotten: Fabrik-zu-lokaler-Rahmen-Transform plus ein VDA-5050-inspiriertes Auftragsvokabular; Pfadplanung verbleibt bei der eigenen Navigation des AMR.|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.4|Koordinationsgrenze für kamerabewehrte UAVs: benanntes Fluganfragevokabular plus ein deterministischer Heartbeat-/Link-Loss-Fehlsicherungs-Watchdog.|

### 🛠️ Ergänzende Tools

|Repository|Version|Beschreibung|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.5|Tragbares Notfalldashboard mit haptischen Sicherheitswarnungen.|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.1.6|Befehlszeilenschnittstelle für Flottenautomatisierung, Flashen und DevOps.|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.6|KI-Erweiterung für Web-Dashboards, die Einblicke in natürlicher Sprache bietet.|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.4.8|Plattformübergreifendes GUI/CLI-Tool zum Erkennen, Installieren und manuellen Aktualisieren aller Ökosystemprojekte.|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.1|Windows/Linux-Desktop-Tool, das ein flashbereites CM5-Image erstellt, das mit den aktuellsten Versionen des Ökosystems und der Erststartkonfiguration im Raspberry-Pi-Imager-Stil vorinstalliert ist.|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.1.8|Wartungsunfall-Koordinator: Eine Edge-Rolle mit geringen Rechten sammelt eine bereinigte Bestands-/Gesundheitssnahaufnahme, eine Control-Plane-Rolle macht sie schreibgeschützt und bittet einen KI-Anbieter, eine Diagnose vorzuschlagen – sie wendet niemals einen Patch an oder stellt etwas bereit.|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.1.8|Reproduzierbarer Entwicklungshost: Ein richtliniengesteuertes Konfigurationsschema und Manifestverzeichnis, das zu einem isolierten Task-/Workspace-Runner wächst, der mit dem OPS-AGENT koordiniert wird – kein Task hat jemals Bereitstellungsberechtigung, es sei denn, ein Dokument gewährt sie ausdrücklich.|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.3|Architektur, Schnittstellen, Sicherheitsbasislinie, Fähigkeitsmatrix und generierter Projektkatalog des Ökosystems sowie die Tools, die alle Repositories vergleichen.|

\---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC\_BANNER.svg" alt="URTC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Tools-25%2B%20profiles-blueviolet.svg" alt="Tools">
</p>

**URTC (Universal Robot Tool Controller)** ist ein eigenständiges Produkt und kein HYDRA-UMC-Subsystemordner: Echtzeit-Firmware und eine Familie von Desktop-/Web-Tools für den Endeffektor eines Roboters, unabhängig entwickelt, versioniert und gewartet. Ein mit URTC ausgestatteter Werkzeugwechsler koordiniert sich über FDCAN mit dem Zellcontroller von HYDRA-UMC, aber das Echtzeitverhalten, der Watchdog und der sichere Zustand des Werkzeugs unterliegen der alleinigen Autorität von URTC – der Zellcontroller kann sie nicht umgehen, und URTC ist nicht von HYDRA-UMC abhängig, um entwickelt, geflasht oder diagnostiziert zu werden.

## 🏗️ Funktionsweise von URTC

1. **Werkzeug-Firmware**: Die eigene STM32-Firmware von URTC führt über 25+ spezialisierte Werkzeugprofile aus (Greifer, Dosierer, Sonden, Spindeln und mehr), jedes mit eigenen Timings, Grenzwerten und Fehlerverhalten.
2. **Feld-Update**: CAN-OTA überträgt ein neues Firmware-Image über denselben CAN-Bus, den das Werkzeug bereits verwendet, mit einem vollständigen SWD/JTAG-Pfad (URTC-FLASHER) als Fallback, der niemals von der eigenen Firmware des Werkzeugs abhängig ist.
3. **Live-Diagnose**: URTC-TESTER validiert das Echtzeit-CAN-Verhalten eines Werkzeugs anhand seines deklarierten Profils ohne vollständigen Werkstattaufbau; URTC-WEB-STUDIO tut dasselbe über einen Browser-Tab über Web Serial, ohne dass etwas installiert werden muss.
4. **Lagerung und Lebenszyklus**: URTC-SMART-RACK hält Werkzeuge zwischen Aufträgen bereit, wärmt eines vor einer Übergabe vor und führt ein Lebenszyklus-Auditprotokoll (Zyklen, Fehler, letzte Kalibrierung) pro physischem Werkzeug und nicht pro Werkzeugtyp.
5. **Aktive QS**: URTC-VISION-TOOL ist selbst ein Werkzeug – ein Werkzeugkopf mit eigenen Thermal- und RGB-Kameras für die Qualitätsinspektion im Prozess, keine externe Kamera, die an ein anderes Werkzeug geschraubt ist.
6. **Gemeinsame Basis**: **URTC-COMMON** hält das CAN-Protokoll des Werkzeugkopfes als Daten, mit generiertem Code und Konformitätsvektoren; **URTC-DOCS** enthält die Architektur, Sicherheitsbasislinie und Fähigkeitsmatrix.

## 🛠️ Technologiestack

* **Firmware**: STM32, FDCAN (gemeinsamer Bus mit dem Zellcontroller), CAN-OTA, SWD/JTAG-Fallback.
* **Desktop-Tools**: Plattformübergreifende GUI-Clients für Flashen und Diagnose (URTC-FLASHER, URTC-TESTER).
* **Browser-Tools**: Die Web Serial API für null-installations-Hardware-Tests (URTC-WEB-STUDIO).
* **Lebenszyklusdaten**: Nichtflüchtiges, werkzeugbezogenes Audit-Protokoll, geteilt mit dem F-RAM-Integritätsansatz von HYDRA-UMC.

## 🔒 Sicherheit

Jedes Werkzeugprofil trägt seinen eigenen Watchdog und sein eigenes Fehlerverhalten, unabhängig von der E-STOP-Schicht des Zellcontrollers – ein Werkzeug, das sein eigenes Zeitbudget oder den CAN-Heartbeat verliert, wechselt eigenständig in seinen deklarierten sicheren Zustand, anstatt auf einen externen Befehl zu warten. Das Vorwärmen von URTC-SMART-RACK ist durch dieselben werkzeugspezifischen thermischen Grenzwerte begrenzt, die sein Profil deklariert, und wird im selben Lebenszyklusprotokoll überwacht, mit dem eine Werkstatt entscheidet, ob ein Werkzeug noch betriebsbereit ist.

## 📁 URTC Projektkatalog

|Repository|Version|Beschreibung|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.3.7|Universal Robot Tool Controller-Firmware für über 25 spezialisierte Werkzeuge.|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.3.3|GUI-Tool für CAN-OTA und Vollchip-SWD/JTAG-Firmware-Updates.|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.3.2|Diagnose-Tool zur Echtzeit-Validierung von URTC-Werkzeugprofilen über CAN.|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.3.2|Browserbasiertes Web-Serial-Tool für sofortige Hardware-Tests und Analysen.|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.1.7|Intelligente Werkzeugaufbewahrung mit automatischer Vorwärmung und Lebenszyklus-Audit.|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.1|Werkzeugkopf mit integrierten Thermal- und RGB-Kameras für aktive QS.|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.1.5|Erkennt, installiert und aktualisiert die URTC-Repositories auf einer Maschine aus deren eigenen Manifesten.|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.0.6|Architektur, Schnittstellen, Sicherheitsbasislinie, Fähigkeitsmatrix, CAN-Protokoll-Studiennotiz und generierter Projektkatalog des URTC-Ökosystems sowie die Tools, die alle Repositories vergleichen.|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.0.3|Das CAN-Protokoll des Werkzeugkopfes als Daten: eine Spezifikation, generierter C-, TypeScript- und Python-Code, Konformitätsvektoren und die Python-Transports.|

\---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ARMOR\_BANNER.svg" alt="A.R.M.O.R. Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range)** ist ein separates, öffentliches Perimetersicherheits- und Heimautomatisierungs-Ökosystem – keine Verbindung zu HYDRA-UMC oder URTC außer demselben Autor und denselben Engineering-Konventionen (versionierte Manifeste, ein gemeinsam genutzter Nachrichtenvertrag, achtsprachige Schnittstellen). Seine Feldknoten überwachen den Perimeter eines Anwesens und dessen Solar-/Elektroinstallation; sein zentraler Server und seine Clients ermöglichen es einem Bediener, zu sehen und zu handeln, was diese melden. Die Versions- und Reifehinweise unten stammen direkt aus den eigenen Manifesten und der Fähigkeitsmatrix jedes Repositories, derselben Ehrlichkeitstronvention, die das Dashboard von HYDRA-UMC bereits verwendet.

## 🏗️ Wie A.R.M.O.R. aufgebaut ist

1. **Gemeinsamer Vertrag**: **ARMOR-COMMON** besitzt die Nachrichtenbedeutung – JSON Schema, einen Python-Validator und generierte TypeScript-/Kotlin-Typen, die jedes andere Repository konsumiert und niemals neu definiert.
2. **Feldknoten**: ESP32-S3-Firmware für Radar-/Präsenzerfassung (**ARMOR-RADAR**), Solarwechselrichter- und Batterieüberwachung (**ARMOR-SOLAR**), elektrische Messung mit Schaltung (**ARMOR-ELECTRICAL**) und das Alarmanlagen-Bedienteil des Hauses (**ARMOR-ALARM**); ein Python-Agent (**ARMOR-NETWORK**) überwacht das lokale Netzwerk und die Internet-Erreichbarkeit des Hauses von einer bereits darin befindlichen Maschine aus.
3. **Zentraler Koordinator**: **ARMOR-SERVER** speichert Status, Benutzer, Alarme, Automatisierungen und Kamerabeweise; **ARMOR-SERVER-AI** und **ARMOR-VOICE-AI** fügen eine erklärbare visuelle Richtlinie und Offline-Sprachbefehle hinzu, die niemals eigenständig etwas steuern.
4. **Bediener-Clients**: **ARMOR-STUDIO** (Web) und **ARMOR-ANDROID-CONTROL** (Mobil) sind Clients des zentralen Servers, niemals direkt des Feldnetzwerks. **ARMOR-HMI** ist ein Touch-Panel an der Wand (ein Waveshare ESP32-S3-Touch-LCD-7C-BOX), das den Status anzeigt, scharfschaltet und quittiert, und der Ort sein wird, an dem der Sprachassistent wohnt.
5. **Bereitstellung und Tests**: **ARMOR-DEVOPS** stellt den gesamten Dienstegraphen bereit; **ARMOR-SIMULATOR** spielt Szenarien und wiederholbare Fehler ohne echte Hardware ab; **ARMOR-HARDWARE** trägt das Gehäusedesign und seine Bank-Abnahmematrix.
6. **Ökosystembetrieb**: **ARMOR-UPDATER** entdeckt, installiert und aktualisiert jedes A.R.M.O.R.-Repository auf einer Maschine, dasselbe atomare Verifizierungsdesign wie HYDRA-UMC-UPDATER; **ARMOR-DOCS** ist die kanonische Architekturdokumentation und Fähigkeitsmatrix. **ARMOR-STUDIO** kann auch die Dienste auf der Zentralmaschine von mit dem Freigabeschlüssel des Ökosystems signierten Paketen aktualisieren, wobei jede Signatur vor der Installation überprüft wird.

## 🔒 Ehrlichkeit und Sicherheit

A.R.M.O.R. folgt derselben Regel, die das eigene Dashboard von HYDRA-UMC bereits anwendet: Eine Behauptung ist nur dann real, wenn sie verifiziert wurde, und jedes Repository gibt offen an, was bereits auf echter Hardware ausgeführt wurde und was nicht. Nichts in diesem Ökosystem steuert derzeit Netzstrom oder physischen Zugang; Feldknoten beobachten und melden, und jede zukünftige Schaltfähigkeit wird entworfen und überprüft, bevor sie jemals aktiviert wird.

## 📁 A.R.M.O.R. Projektkatalog

|Repository|Version|Beschreibung|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.6.7|Nachrichtenverträge, Validatoren, Konformitätsvektoren, generierte Typen, OpenAPI, gemeinsamer Launcher.|
|[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)|0.7.3|ESP32-S3-Feldknoten-Firmware, Decoder für LD2450-, LD2461- und Präsenzsensoren, sein hostgetesteter Kern, Updates von GitHub mit Fortschrittsleiste und Live-Karte.|
|[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)|0.4.9|Solar-Gateway-Knoten: Die ESP32-S3-Firmware und ihr Panel (zehn serielle Anschlüsse) sowie die Protokolle von Voltronic-/MPP-Solar-Wechselrichtern und Pylontech- und ANT-BMS-Batterien.|
|[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)|0.4.1|Elektro-Knoten: Die Firmware (sechzehn PZEM-Messgeräte an einer seriellen Leitung, Web-Panel, MQTT), die Frames der Messgeräte, die Nachricht der Netzwerkmesswerte und die Regeln zum Schalten.|
|[ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM)|0.3.9|Alarmknoten und Bedienteil: Seine Firmware (verdrahtete Zonen, Sirene, Zigbee-Sensoren und -Sirenen, Web-Panel in sieben Sprachen) und die Regeln für Scharfschaltung, Verzögerungen, Alarm und PIN, auf einem Computer getestet; es überwacht weiter und übernimmt das Zigbee-Funkmodul, wenn der Server abwesend ist. Wurde nie auf einer Platine ausgeführt.|
|[ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI)|0.3.2|Touch-Panel für das Waveshare ESP32-S3-Touch-LCD-7C-BOX: Der Systemstatus auf einem Wandbildschirm, scharfschalten/unscharfschalten/quittieren, Push-to-Talk-Sprache und die Web-Seite eines Knotens; die Firmware wurde nie auf einer Platine ausgeführt.|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.3|Lokaler Netzwerkmonitor: Die Geräte im Heimnetzwerk, der Status des Internets (und auf wessen Seite ein Ausfall liegt), was sich ändert; es beobachtet nur.|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.7.8|Zentraler Status (persistent), Benutzer, Ereignisverlauf, Alarme, Geräte, Automatisierungen, Solar- und Strommesswerte, das lokale Netzwerk, Systemdienste, Kamera-Watchdog, Kameras, Beweise, Audit, Knotenfirmware-Updates, die signiert sein müssen, Telegram- und Home-Assistant-Hinweise, Sprachbefehle und Verwendung von außerhalb des Hauses (Zweiter Faktor, beendbare Sitzungen, Remote-Richtlinie).|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.6|Bewegungserfassungsdienst, Auswahl visueller Profile, erklärbare Fusionsrichtlinie, Engine-Register.|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.2|Kamerazonen, Masken und Erkennungsregeln (Herumlungern, ein Ereignis pro Besuch); noch kein Detektormodell.|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.0|Offline-Sprachdienst: Fünfzehn Befehle in acht Sprachen, gesprochene Runden des Wandpanels, Scharf- und Unscharfschaltung bestätigt mit einem signierten Token.|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.0.3|Betriebskonsole, Alarme, Geräte, Automatisierungen, Benutzer, Verlauf, Alarmregeln, PTZ, Radarkarte, Solar- und Strommenüs, lokales Netzwerk, Systemdienste, Wetter, Knotensucher und -konfiguration, Knotenfirmware-Updates, Benachrichtigungen und ein 2D-/3D-Standortdesigner.|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.0|Android-Bedienclient: Scharf- und Unscharfschaltung, Alarme, Geräte, Live-Radar, Solarwechselrichter und Batterien, Verlauf, Alarmbenachrichtigungen, ein Assistent für geschriebene und gesprochene Befehle sowie der Konfigurator der Knoten.|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.4|Gehäusedesigns (das Radareckgehäuse; eine geprüfte Box für Solar-, Elektro- und Alarmknoten) und die Bank-Abnahmematrix.|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.3|Compose-Topologie, Testbench-Installer für den zentralen Server, Backup und Wiederherstellung, TLS-Profil, eigener MQTT-Broker, Beobachtungs- und SprachDienste, Verwaltungsagent.|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.5|Szenarien und wiederholbare Fehler.|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.4|Erkennt, installiert und aktualisiert die eigenen Repositories des Ökosystems (atomar durch Verifizierung, kein GITHUB\_TOKEN erforderlich).|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.0.4|Kanonische Dokumentation und die Fähigkeitsmatrix.|

\---

# ⚡ EH3D FABRICATION SUITE

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/EH3D\_BANNER.svg" alt="EH3D Fabrication Suite Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Desktop%20%7C%20Embedded-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-C%2B%2B%20%7C%20Python%20%7C%20Qt-orange.svg" alt="Stack">
  <img src="https://img.shields.io/badge/Hardware-HYDRA--UMC%20%7C%20Bungard%20%7C%20ESP32-green.svg" alt="Hardware">
</p>

**EH3D Fabrication Suite** ist ein dediziertes, aus mehreren Repositories bestehendes Software-Ökosystem, das auf schnelles Leiterplatten-Prototyping (PCB), CAM-Werkzeugwegvorbereitung, Computer-Vision-Inspektion, Pick-\&-Place-Management (PnP) und CNC-/Laser-Steuerung über mehrere Maschinen hinweg zugeschnitten ist. Es bietet native Interoperabilität mit **HYDRA-UMC**-Hardwareknoten (STM32H7 + Jetson Orin NX + Hailo NPU) neben einem Werkstatt-Maschinenpark, der industrielle Frässysteme (Bungard CCD über ESP32-S3 RS-232-Gateways), CNC-Fräsen (JuanenCNC) und Diodenlaser-Engraver (JuanenLaser) umfasst.

## 🏗️ Funktionsweise der EH3D Fabrication Suite

1. **Zentrale Verwaltung**: **EH3D-SUITE-LAUNCHER** entdeckt aktive Hardwareknoten im lokalen Netzwerk (HYDRA-UMC und ESP32-Gateways), verwaltet einheitliche `.eh3dproj`-Pakete und orchestriert Tool-Updates.
2. **CAM-Verarbeitungspipeline**: Spezielle CAD/CAM-Tools behandeln einzelne Fertigungsstufen:

   * **EH3D-ISOCAM**: Gerber RS-274X/X2-Leiterbahnisolierung, Voronoi-Algorithmen und Restkupferentfernung (Rubout).
   * **EH3D-DRILLPRO**: Excellon-/NC-Bohrverarbeitung, Bohrer-Tabellen und Tiefbohrzyklen.
   * **EH3D-ROUTEPRO**: Platinenkantenfräsen, Laschenerstellung (Tabs) und Rampeneingangsstrategien.
   * **EH3D-LASER-CAM**: Raster-Dithering-Algorithmen und Vektor-Leistungsmodulation für das Laserschneiden.
   * **EH3D-STENCILCAM**: Lötmaskenverarbeitung (Pastemask) zur Erstellung von SMD-Lötpastenschablonen.
3. **Ausführung und Echtzeitsteuerung**: **EH3D-MOTIONCNC** steuert die Maschinenbewegung über Hochgeschwindigkeits-G-Code/HP-GL-Streaming, integriert mit **EH3D-AUTOLEVEL** für die topografische Z-Abtastung und **EH3D-PENDANT-GUI** für das manuelle Nullsetzen (G54/G55) und Verfahren.
4. **Edge KI \& Inspektion**: **EH3D-VISION-STUDIO** nutzt die Hailo-NPU von HYDRA-UMC, um Echtzeit-Kameraausrichtung, automatische Passmarkenerkennung (Fiducials) und Werkzeugverschleißinspektion durchzuführen.
5. **Bestückung und Hilfsdaten**: **EH3D-PNP-MANAGER** verwaltet SMD-Bestückungskoordinaten nach Zentroide und Zubringer (Feeders), während **EH3D-TOOL-MANAGER** eine einheitliche Werkzeugkasten-Datenbank über alle CAM-Module hinweg pflegt.

## 📁 EH3D Fabrication Suite Projektkatalog

|Repository|Version|Beschreibung|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|Haupt-Ökosystem-Dashboard für Projektverwaltung (.eh3dproj), Updates, globale Einstellungen und Knotenerkennung.|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|Gerber RS-274X/X2 CAM-Verarbeitungs-App, Voronoi-/Offset-Bahnisolierung, Restkaufentfernung und Gravursimulation.|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.1|Excellon-/NC-Bohr-CAM-App, Bohrerverwaltung, Pfadoptimierung und Tiefbohrzyklen.|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.1|Platinenkonturfräs-CAM-App, Taschenfräsen, Haltestege und CNC-Rampeneingangsstrategien.|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|Laser-CAM-App für Bild-Dithering, Raster-/Vektorkonvertierung und dynamische PWM-Leistungsregelung.|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.1|Echtzeit-Nummerierungs-GUI, 3D-G-Code-Visualisierer, Antastung und Multi-Maschinen-Streaming-Unterstützung.|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|Topografischer Höhennetz-Prozessor (Z-Probing) und G-Code-Interpolation für den Oberflächenausgleich.|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|Leichtgewichtige CAM-Inspektionstool für Gerber-Ebenenausrichtung und schnelle Visualisierung.|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|Pastemasken-Konvertierungsprogramm, das Schneidwerkzeugwege für die Laser- und Plotter-SMD-Schablonenfertigung generiert.|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|OpenPnP-inspiriertes SMD-Bestückungsmanagement, Zentroid-Reader, Zubringersteuerung und visuelle Bauteilzentrierung.|
|[EH3D-PENDANT-GUI](https://github.com/JuanenRac/EH3D-PENDANT-GUI)|0.0.1|Touchscreen-/Mobil-Handsteuerung für Echtzeit-Verfahren, Nullsetzen (G54/G55) und E-STOP.|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|3D-Werkzeugweg- und Materialabtragssimulator, Kollisionsdetektor und G-Code-/HP-GL-Zykluszeitschätzer.|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|Edge-KI-Visions-Dashboard für Kameraausrichtung, Passmarkentraining und visuelle Inspektion über HYDRA-UMC.|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|Geteilte Werkzeugkasten-Datenbank zur Nachverfolgung von Verschleißstunden, Schnittvoreinstellungen und Vorschüben über alle EH3D-CAM-Tools hinweg.|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.1|Geteilte C++/Python-Bibliothek mit Gerber-, Excellon-, G-Code- und HP-GL-Parsern, 2D/3D-Geometrie und Protokollen.|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.1|Datenschemas, einheitliche Projekt-Spezifikationen (.eh3dproj), globale Konstanten und UI-Grafik-Assets.|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.1|Ökosystemdokumentation, Montageanleitungen, Gateway-technische Spezifikationen und Integrationshandbücher.|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.1|Erkennt, installiert und aktualisiert die eigenen Repositories des Ökosystems (atomar durch Verifizierung, kein GITHUB\_TOKEN erforderlich).|

\---

## 🤝 Mitwirken

Jedes Ökosystem ist eine eigene Initiative mit eigenen Projekten. Jedes Projekt hat seine eigenen Mitrichtlinien. Bitte beachten Sie einzelne Repositories für technische Details.

Issue-Labels sind über jedes HYDRA-UMC-Repository hinweg von [`.github/labels.yml`](.github/labels.yml) in demselben Repository standardisiert und durch [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) synchronisiert – bearbeiten Sie diese eine Datei, um ein Label überall auf einmal zu ändern, anstatt manuell pro Repository. Im Gegensatz zum Dashboard unten ist diese Liste statisch (eine echte GitHub Actions-Matrix, keine dynamische Erkennung) – ein neu hinzugefügtes Repository benötigt dort ebenfalls einen Eintrag und nicht nur ein echtes `hydra-umc.project.json`.

Ein Live-Status-Dashboard, das jedes öffentliche Repository der vier Ökosysteme abdeckt – jedes einzelne entdeckt durch sein eigenes Manifest (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json` sowie `electro-hobby-3d.project.json` für die übergeordneten Ökosystem-Repositories), direkt aus dem Standard-Branch jedes Repositories ohne feste Liste gelesen –, wird von [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) unmittelbar bei einem Push eines Projekts (das repo-eigene `dashboard-dispatch.yml`) und als Sicherheitsnetz zweimal pro Stunde neu generiert und über GitHub Pages von `docs/` bereitgestellt: [**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/). Es zeigt Stack, Bereitstellungsziel und aktuelle Version, eine echte Reifeklassifizierung pro Projekt (Scaffolding / Functional / Established / Production, jeweils bestimmt aus dem CHANGELOG des Projekts – siehe [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)), seine Rolle (API / UI / CLI / Firmware / Library / Service / Tool), einen Familie/Eltern-Kind-Baum und projektbezogene Hinweise dazu, was heute implementiert ist. [`ecosystem-catalog.json`](ecosystem-catalog.json) listet diese Ökosysteme und ihre Manifeste an einem Ort auf, und der Dashboard-Build verweigert die Ausführung, wenn jemals beide voneinander abweichen.

## 🧭 GitHub-Zusammenarbeit

Das [GitHub-Kollaborationsmodell](docs/GITHUB_COLLABORATION.md) definiert ein zentrales Wiki, ein Ökosystem-Projekt, Diskussionsbereiche, Freigabekriterien und die gemeinsame Automatisierungsgrenze. Die zentral gepflegten [Issue-Formulare](.github/ISSUE_TEMPLATE/) und die [Pull-Request-Vorlage](.github/PULL_REQUEST_TEMPLATE.md) machen Software-, Hardware-Validierungs- und Dokumentationsarbeiten nachvollziehbar, ohne Projekthandbücher zu duplizieren.

Der Community-Health-Workflow ist standardmäßig manuell und erfolgt als Trockenlauf. Sobald `COMMUNITY\_HEALTH\_SYNC\_TOKEN` konfiguriert ist, kann er nur diese verwalteten Vorlagen in jedes Repository kopieren, das ein HYDRA-UMC-Manifest veröffentlicht; er löscht niemals eine projektspezifische Vorlage.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** – GPL-3.0-Lizenz.

