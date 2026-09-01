<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ökosystem Banner" width="100%">
</p>

# HYDRA-UMC / URTC Ökosystem 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  🇩🇪 <b>Deutsch</b> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Lizenz-GPL%203.0-blue.svg" alt="Lizenz GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Plattform-STM32%20%7C%20CM5-red.svg" alt="Plattform">
  <img src="https://img.shields.io/badge/KI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="KI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Willkommen im **HYDRA-UMC-Ökosystem**, einer mehrschichtigen industriellen Robotikplattform, die von Low-Level-Echtzeit-Firmware bis hin zu kognitiver High-Level-KI reicht. Diese Organisation umfasst zahlreiche spezialisierte Projekte, die für eine perfekte Synchronisation bei der Mikrofabrik-Automatisierung und Schwarmrobotik konzipiert sind.

## 📈 Ökosystemfortschritt

`[█████████▊░░░░░░░░░░] 49%` — Orientierungswert. Der Meilenstein 100 % ist ein vollständig integriertes Ökosystem auf realer Hardware.

---

## 🚀 Hauptmerkmale & Skalierbarkeit

- **Multi-Roboter-Skalierbarkeit**: Unterstützt bis zu 8 verteilte Robotereinheiten (derzeit 3, 4, 5 und 6 Achsen; skalierbar auf 7, 8, 9 Achsen und Dual-Roboter-Architekturen in zukünftigen Versionen).
- **Integrierte lokale Stufe**: Die HYDRA-UMC-Hauptplatine verfügt über eine integrierte **lokale 6-Achsen-Stufe** für Zusatzaufgaben, einschließlich Sekundärroboter, ATC-Revolver (automatischer Werkzeugwechsler), Förderbandsynchronisation oder XYZ-Tischportale.

---

## 🏗️ Ökosystem-Architektur

Das Ökosystem v1.1 ist eine geschichtete Produktplattform: Es baut auf etablierten Linux- und Raspberry-Pi-Technologien auf, ohne ein neues Betriebssystem zu entwickeln oder Hersteller-APIs zu ersetzen.

1.  **Plattformbasis**: Raspberry Pi OS ARM64 und Standard-Linux-Dienste bilden die unterstützte CM5-Grundlage.
2.  **Plattform und Verträge**: **HYDRA-UMC-OS** liefert reproduzierbare Profile, Dienste, Diagnose und Updates auf Raspberry Pi OS; **HYDRA-UMC-SDK** veröffentlicht versionierte Verträge, schlanke Clients und Konformitätsprüfungen.
3.  **Echtzeit-Ausführung**: **HYDRA-UMC**-Firmware und URTC auf STM32/MCU behalten Bewegungsgrenzen, Watchdogs und sicheren Stopp.
4.  **Koordination und Betrieb**: Serverdienste, Job-Verteilung, Telemetrie und Konfiguration koordinieren Geräte, ohne die MCU-Sicherheitsgrenze zu umgehen.
5.  **Bedienoberflächen**: Studio, Suite, DSI, Web, Desktop, Mobile und CLI verwenden die SDK-Verträge.
6.  **Wahrnehmung und Intelligenz**: Vision, Hailo und kognitive Dienste schlagen Beobachtungen oder Pläne vor; sie besitzen keine physische Sicherheitsautorität.
7.  **Engineering, Industrie und Daten**: Digital Twin, HIL/Physik, OPC-UA/MQTT/MTConnect-Gateways und Datendienste validieren und integrieren das System.

Die Entwicklung beginnt mit Architektur und öffentlichem Dienstmodell von **HYDRA-UMC-OS** und verwendet danach die Verträge und Konformitätsregeln von **HYDRA-UMC-SDK**. Die Sicherheitsautorität von MCU/URTC bleibt in jedem Ablauf erhalten.

---

## 🛠️ Technologie-Stack & Tools

Das Ökosystem nutzt einen modernen Hochleistungs-Stack für unternehmenskritische Zuverlässigkeit:

### 💠 Embedded & Echtzeit (Ausführung)
- **Mikrocontroller**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Frameworks**: FreeRTOS (AMP-Modus), CMSIS-DSP, STM32 HAL/LL.
- **Protokolle**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (50MHz Slave IPC), I2C, UART.
- **Kinematik**: S-Kurven-Profilgenerierung, Echtzeit-Inverse Kinematics (IK).

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
- **Cybersicherheit**: JWT-based stateless Authentifizierung + mTLS für sicheren Datenverkehr zwischen den Knoten.
- **Integrität**: Nichtflüchtiger F-RAM für die Überprüfung des Werkzeuglebenszyklus und die Statuswiederherstellung.

---

## 🔧 Hardware-Hacking: Bau deines eigenen Carriers

Die Robot Controller Board basiert auf einem **Raspberry Pi CM5**, und der eigene doppelte Hirose-DF40-Steckverbinder der CM5 hat ein festes, offizielles, öffentliches Pinout (Tabelle 5 im offiziellen CM5-Datenblatt von Raspberry Pi) - das ist nichts, was dieses Projekt selbst festlegt. Das bedeutet, ein kompatibler Carrier von Drittanbietern ist ein reales, erreichbares Projekt, kein Reverse-Engineering:

- **Hier anfangen**: [`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - welche festen CM5-Pins dieses Board tatsächlich nutzt (Ethernet, die 2 nativen USB3-SuperSpeed-PHYs, der CM5-seitige Kühllüfteranschluss) und warum, nach Funktion neu geordnet aus der offiziellen Pinout-Tabelle.
- **Der einfache Einstieg**: die **Standard-40-Pin-GPIO-Leiste von Raspberry Pi** (dasselbe "B+"-Layout, unverändert seit 2014) ist auf diesem Board genau wie bei jedem Raspberry Pi herausgeführt - bestehende RPi-HATs und GPIO-Tools funktionieren unverändert. Eine Handvoll Positionen, die die eigene STM32-Verbindung dieses Boards bereits nutzt, sind im Siebdruck/vermerkt, damit klar ist, welche auszulassen sind.
- **Weiterführend**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) beschreibt, wie CM5, das STM32H745 "Kinematic Brain" und der STM32G474 "Robot Controller" tatsächlich miteinander kommunizieren (SPI1 + FDCAN1 + die CM7↔CM4-IPC-Mailbox) - die Schicht, die ein Carrier-Redesign erhalten müsste, um mit der eigenen Firmware dieses Projekts kompatibel zu bleiben.
- Jedes Pinout-Dokument gibt klar an, ob es **BESTÄTIGT** (direkt aus einer offiziellen Datenblatt-Tabelle übernommen) oder **VORGESCHLAGEN** (eine eigene Routing-Entscheidung dieses Projekts, die auf einem abgeleiteten Carrier anders ausfallen kann) ist - lies diese Statuszeile, bevor du eine Signalzuweisung als fest behandelst.

Das ist kein geführtes Tutorial (es gibt keinen einzigen "richtigen" Carrier für jeden Anwendungsfall) - es ist das reale Referenzmaterial, das ein erfahrener Hardware-Entwickler braucht, um von einer bereits verifizierten Pin-Zuordnung statt nur einem Datenblatt auszugehen.

---

## 📁 Projektkatalog

Neu im Ökosystem? `./starter-kit.sh` (oder `starter-kit.bat` unter
Windows) klont 13 Kern-Repositories - eine handverlesene Startauswahl,
nicht den vollständigen Katalog unten - als Geschwisterverzeichnisse in
einem gemeinsamen Ordner: die Standardstruktur, die jedes
repoübergreifende Skript hier bereits voraussetzt. Erneutes Ausführen
ist sicher: bereits geklonte Repositories bleiben unangetastet. Von
dort aus kann
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(eines der 13 gerade geklonten) Versionen prüfen und jedes andere
Projekt aus dem vollständigen Katalog unten bauen/aktualisieren.

### 🧱 Plattformbasis und Verträge
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | Raspberry-Pi-OS-Plattformschicht für CM5: reproduzierbare Profile, Konfiguration, Diagnose, Dienstlebenszyklus und Updates; keine neue Linux-Distribution. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | Gemeinsame versionierte Verträge, schlanke Clients und Konformitätsprüfungen für Dienste, Oberflächen, CM5-Adapter und URTC; ersetzt keine Hersteller-APIs. |

### 💠 Kernsteuerung und Bedienclients
| Repository | Beschreibung |
| :--- | :--- |

### 💠 Kernsteuerung und Bedienclients
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | Kern-Bewegungssteuerungs-Firmware für STM32H745/G474 mit S-Curve-Kinematik. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | Headless Node.js API und WebSocket-Backend für die Roboter-Orchestrierung. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | Fortschrittliches React-basiertes Web-Dashboard für 3D-Roboter-Überwachung und -Steuerung. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | Hochleistungs-Python/Qt-Desktop-Anwendung für die industrielle Automatisierung. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | Flutter-basierte Touch-Schnittstelle für industrielle 7"-Displays (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | Native Kotlin-Mobile-App mit biometrischem Login für Fernmanagement. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | Flutter-Mobile-App für iOS/iPadOS mit Live-WebSocket-Synchronisation. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | Grafischer URDF-Editor zum Validieren und Hochladen von Robotermodellen. |


### 🔧 URTC-Kern und Werkzeuge
| Repository | Beschreibung |
| :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | Universelle Werkzeugsteuerungs-Firmware für über 25 spezialisierte Werkzeuge. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | GUI-Tool für CAN-OTA- und SWD/JTAG-Firmware-Updates. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | CAN-Bus-Diagnosetool mit Telemetrie-Panels pro Werkzeug. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Web-Serial-Tool für sofortige Hardware-Tests und -Analysen. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | Intelligente Werkzeuglagerung mit Vorwärmung und Lebenszyklusprüfung. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | Werkzeugkopf mit integrierten Thermal- und RGB-Kameras für aktive QS. |

### 👁️ Vision-KI-Knoten (Optimiert für Hailo-8)
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | Hochgeschwindigkeits-Perzeptionsknoten für 8 simultane USB-3.0-Kamerastreams. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | Optimierte GStreamer/MediaMTX-Pipeline für industrielle Videoweiterleitung. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | Bibliothek hardwarebeschleunigter YOLO-Modelle für SMD- und Komponenten-QS. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | Echtzeit-KI-Intrusionserkennung zum Schutz des Robotik-Arbeitsraums. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | Bildbasiertes kinematisches Feedback für submillimetergenaue Posenschärfung. |

### 🧠 Kognitiver KI-Knoten (Optimiert für Hailo-10)
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | Semantischer Denkknoten für logische Missionsplanung und Sprachsteuerung. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | Implementierung des Vision-Language-Action-Modells für komplexe Aufgaben. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | Lokale, private STT/TTS-Pipeline für natürliche Bedienerinteraktion. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | LLM-basierter Missions-Orchestrator mit kontextsensitiver Fehlerbehebung. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | RAG-basierter KI-Assistent, trainiert auf Handbüchern und Quellcode. |

### 🐝 Orchestrierung & Schwarm
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | Flottenmanager für Multi-Roboter-Koordination und Kollisionsvermeidung. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | PTP-Synchronisation für nanosekundengenaue Roboterkoordination. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | Verteilter Pfadoptimierer für Roboterschwärme in gemeinsam genutzten Räumen. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | Prioritätsbasierter Aufgabenplaner für heterogene Roboterflotten. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | Hochverfügbarkeitsmonitor mit transparentem Missions-Failover. |

### 🎮 Digitaler Zwilling & Simulation
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | Hochpräzise Physiksimulations-Engine für risikofreies Robotertesten. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | Reale Physiksimulation (MuJoCo/PhysX) von URDF-Ketten. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | Hardware-in-the-loop-Schnittstelle für Statuskonsistenz (real vs. virtuell). |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | Prozeduraler Datensatzgenerator zum Trainieren von Vision-KI-Modellen. |

### 📊 Daten & Analytik
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | Big-Data-Speicher für massive Multi-Roboter-Industrietelemetrie. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | Hochdurchsatz-Ingester für CAN-, WebSocket- und Systemprotokolle. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | Vorausschauende Wartung basierend auf Motorvibrationssignaturen. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | Automatisierte OEE- und KPI-Erstellung für das Fabrikmanagement. |

### 🏭 Industrielles Gateway
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | Interoperabilitätsbrücke für Fabrikstandards (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | Mapping von HydraState-Robotikobjekten auf Standard-OPC-UA-Knoten. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | Telemetriebrücke für IoT-Integrationen und externe Dashboards. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | Standardisierte Schnittstelle für die Zustandsüberwachung von Maschinen. |

### 🌉 Externe Automatisierungsbrücken
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | Bidirektionale ROS-2-Koordinationsgrenze: Topics für Beobachtung, Dienste zur Prüfung und abbrechbare Zellaktionen. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | Nachverfolgbarer PCB-Übergabekoordinator für OpenPnP sowie robotergestütztes Be- oder Entladen. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | Sichere Brücke um 3D-Drucksoftware; der erste Adapter prüft Moonraker ohne Firmware zu ersetzen. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | Koordinator für CNC-Zellenhilfen; Bahnplanung und Sicherheit bleiben im nativen Controller. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | Koordinator für Laserzellenhilfen, der weder Laser scharf schalten noch auslösen oder Interlocks umgehen kann. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | Koordinationsgrenze für Lauf-/Humanoid-Droiden: benanntes Aktionsvokabular (Laufen/Greifen/Ablegen), gefiltert durch den gemeinsamen Sicherheitsvertrag; Gangart und Balance bleiben beim eigenen Controller des Droiden. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | Koordinationsgrenze für AGV-/AMR-Flotten: Transformation vom Fabrik-Koordinatensystem ins lokale System eines AMR plus ein an VDA-5050 angelehntes Auftragsvokabular; die Bahnplanung bleibt bei der eigenen Navigation des AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | Koordinationsgrenze für kameratragende UAVs: benanntes Flugauftragsvokabular plus ein deterministischer Heartbeat-/Verbindungsverlust-Watchdog. |

### 🛠️ Ergänzende Tools
| Repository | Beschreibung |
| :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | Tragbares Notfall-Dashboard mit haptischen Sicherheitswarnungen. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | Befehlszeilenschnittstelle für Flottenautomatisierung, Flashen und DevOps. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | KI-Erweiterung für Web-Dashboards für Einblicke in natürlicher Sprache. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | Plattformübergreifendes GUI/CLI-Tool zum Erkennen, Installieren und manuellen Aktualisieren jedes Ökosystem-Projekts. |

---

## 🤝 Mitwirken
Dieses Ökosystem ist Teil einer High-Tech-Robotik-Initiative. Jedes Projekt hat seine eigenen Richtlinien für die Mitarbeit. Technische Details finden Sie in den einzelnen Repositories.

Issue-Labels sind über alle Repos des Ökosystems hinweg aus [`.github/labels.yml`](.github/labels.yml) in diesem selben Repo standardisiert und werden von [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) synchronisiert - bearbeiten Sie diese eine Datei, um ein Label überall auf einmal zu ändern, statt es von Hand pro Repo zu tun. Anders als das Dashboard unten ist diese Liste statisch (eine echte GitHub-Actions-Matrix, keine dynamische Erkennung) - ein neues Repo braucht dort ebenfalls einen Eintrag, nicht nur ein echtes `hydra-umc.project.json`.

Ein Live-Statusdashboard für jedes öffentliche Repo, das in seiner eigenen `hydra-umc.project.json` `ecosystem: HYDRA-UMC` deklariert (Stack, Deploy-Ziel, aktuelle Version - direkt aus dem eigenen Standard-Branch jedes Repos gelesen, dynamisch ohne feste Liste erkannt), wird stündlich (und sofort nach einem relevanten Push) von [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) generiert und über GitHub Pages aus `docs/` ausgeliefert: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. v3 fügt eine echte Reifegrad-Klassifizierung pro Projekt hinzu (scaffolding / functional / established / production, jede anhand des eigenen CHANGELOG dieses Projekts entschieden - siehe den Docstring des Moduls [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) für das genaue Kriterium), seine Rolle (API / UI / CLI / Firmware / Bibliothek / Service / Tool), einen echten Familie/Eltern-Kind-Baum sowie projektbezogene Notizen dazu, was heute tatsächlich implementiert ist.

## 🧭 GitHub-Zusammenarbeit

Das [GitHub-Zusammenarbeitsmodell](docs/GITHUB_COLLABORATION.md) definiert ein zentrales Wiki, ein gemeinsames Ecosystem-Project, den Rahmen für Discussions, Release-Kriterien und die Grenze gemeinsamer Automatisierung. Die zentralen [Issue-Formulare](.github/ISSUE_TEMPLATE/) und die [Pull-Request-Vorlage](.github/PULL_REQUEST_TEMPLATE.md) machen Softwarearbeit, Hardware-Validierung und Dokumentation nachvollziehbar, ohne Projekthandbücher zu duplizieren.

Der Community-Health-Workflow ist manuell und standardmäßig ein Dry-Run. Nach dem Konfigurieren von `COMMUNITY_HEALTH_SYNC_TOKEN` kann er nur diese verwalteten Vorlagen in jedes Repository mit HYDRA-UMC-Manifest kopieren; projektspezifische Vorlagen werden niemals gelöscht.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 Lizenz.
