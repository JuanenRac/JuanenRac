<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Bannière de l'écosystème HYDRA-UMC" width="100%">
</p>

# Écosystème HYDRA-UMC / URTC 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  🇫🇷 <b>Français</b> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Licence-GPL%203.0-blue.svg" alt="Licence GPL 3.0">
  <img src="https://img.shields.io/badge/Matériel-CERN%20OHL--S-orange.svg" alt="Matériel CERN OHL">
  <img src="https://img.shields.io/badge/Plateforme-STM32%20%7C%20CM5-red.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Puissance IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenue dans l'**Écosystème HYDRA-UMC**, une plateforme robotique industrielle multicouche allant du micrologiciel temps réel de bas niveau à l'IA cognitive de haut niveau. Cette organisation héberge de nombreux projets spécialisés conçus pour travailler en parfaite synchronie pour l'automatisation de micro-usines et la robotique en essaim.

---

## 🚀 Caractéristiques Clés et Évolutivité

- **Évolutivité Multi-Robot** : Prend en charge jusqu'à 8 unités robotiques distribuées (actuellement de 3, 4, 5 et 6 axes ; évolutif vers 7, 8, 9 axes et architectures de robots doubles dans les futures versions).
- **Étage Local Intégré** : La carte principale HYDRA-UMC dispose d'un **Étage Local à 6 axes** intégré pour des tâches auxiliaires, notamment des robots secondaires, des révolveds ATC (Automatic Tool Changer), la synchronisation de bandes transporteuses ou des portiques de tables XYZ.

---

## 🏗️ Architecture de l'Écosystème

L'écosystème est structuré en 6 couches fonctionnelles permettant des opérations robotiques autonomes, collaboratives et intelligentes :

1.  **Couche d'Exécution** : Micrologiciel basé sur STM32 (H745/G474) pour une précision submillimétrique et une action FDCAN haute vitesse.
2.  **Couche d'Intelligence** : IA de bord propulsée par **Hailo-8** (perception des réflexes) et **Hailo-10** (raisonnement cognitif).
3.  **Couche de Coordination** : Backends Node.js autonomes et orchestrateurs d'essaim distribués.
4.  **Couche d'Interface** : Tableaux de bord Web (React), Bureau (Qt6), Mobile (Kotlin/Flutter) et tactiles DSI.
5.  **Couche Virtuelle** : Moteurs de Jumeau Numérique haute fidélité (Rust/Bevy) pour une validation pré-physique sécurisée.
6.  **Couche de Support** : Passerelles Industrie 4.0 (OPC-UA/MQTT) et maintenance prédictive Big Data.

---

## 🛠️ Stack Technologique et Outils

L'écosystème exploite une pile moderne et performante pour une fiabilité critique :

### 💠 Embarqué et Temps Réel (Exécution)
- **Microcontrôleurs** : STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Frameworks** : FreeRTOS (mode AMP), CMSIS-DSP, STM32 HAL/LL.
- **Protocoles** : FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (IPC esclave 50MHz), I2C, UART.
- **Cinématique** : Génération de profils de courbe S, cinématique inverse (IK) en temps réel.

### 🧠 IA de Bord et Perception (Intelligence)
- **Accélérateurs** : Hailo-8 (26 TOPS) pour la vision à 8 caméras, Hailo-10 (40 TOPS) pour la GenAI.
- **Modèles** : YOLOv10 (détection), OpenVLA (action), Whisper (voix), Llama-3 (raisonnement).
- **Inter-nœud** : gRPC sur Protobuf et échange de métadonnées SPI-DMA haute vitesse.

### 🌐 Backend et Coordination (Coordination)
- **Runtimes** : Node.js 20+ (API), Rust 1.80+ (Orchestrateur), Go (CLI).
- **Infrastructure** : Express, Fastify, Socket.io (WebSocket), gRPC.
- **Base de données** : InfluxDB/TimescaleDB (Télémétrie), Redis (État), SQLite.

### 💻 Tableaux de Bord et Interface Utilisateur (Interface)
- **Web** : React 19, Vite, Three.js (Visionneuse 3D), Tailwind CSS.
- **Natif** : Python 3.12/PySide6 (Suite), Kotlin (Android natif), Flutter 3.x (iOS et DSI).

---

## 📋 Configuration Requise

- **Nœud de calcul** : Raspberry Pi CM5 (4 Go+ RAM) avec stockage NVMe/eMMC.
- **Matériel IA** : Modules M.2 Hailo-8/Hailo-10 (Clé M).
- **Bus de terrain** : Gigabit Ethernet pour le LAN et FDCAN (ISO 11898-1:2015) pour les actionneurs.
- **OS client** : Android 10+, iOS 15+, Windows 10/11 (Haute densité), Ubuntu 22.04 LTS.

---

## 🔒 Sécurité Industrielle

- **Couche E-STOP** : Ligne d'urgence câblée + Trames d'urgence CAN haute priorité (<1ms).
- **Sécurité IA** : Zones de sécurité 3D avec coupure automatique du couple moteur en cas d'intrusion humaine.
- **Cybersécurité** : Authentification sans état basée sur JWT + mTLS pour un trafic inter-nœuds sécurisé.
- **Intégrité** : F-RAM non volatile pour l'audit du cycle de vie des outils et la récupération d'état.

---

## 🔧 Hacking Matériel : Construire son Propre Carrier

La Robot Controller Board est construite autour d'un **Raspberry Pi CM5**, et le double connecteur Hirose DF40 de la CM5 a un brochage fixe, officiel et public (Tableau 5 de la fiche technique officielle de la CM5 de Raspberry Pi) - ce n'est pas quelque chose que ce projet définit. Cela signifie qu'un carrier compatible tiers est un projet réel et réalisable, pas un exercice de rétro-ingénierie :

- **Commencez ici** : [`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - quelles broches fixes de la CM5 cette carte utilise réellement (Ethernet, les 2 PHY USB3 SuperSpeed natifs, le connecteur de ventilateur de refroidissement côté CM5) et pourquoi, réorganisé par fonction à partir du tableau de brochage officiel.
- **La voie facile** : le **connecteur GPIO standard 40 broches de Raspberry Pi** (la même disposition « B+ » inchangée depuis 2014) est exposé sur cette carte exactement comme sur n'importe quel Raspberry Pi - les HAT et outils GPIO existants fonctionnent sans modification. Quelques positions déjà utilisées par la liaison STM32 propre à cette carte sont sérigraphiées/annotées pour savoir lesquelles éviter.
- **Pour aller plus loin** : [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) explique comment la CM5, le « Cerveau Cinématique » STM32H745 et le « Robot Controller » STM32G474 communiquent réellement entre eux (SPI1 + FDCAN1 + la boîte aux lettres IPC CM7↔CM4) - la couche qu'une refonte de carrier devrait préserver pour rester compatible avec le firmware propre à ce projet.
- Chaque document de brochage indique clairement s'il est **CONFIRMÉ** (tiré directement d'un tableau de fiche technique officielle) ou **PROPOSÉ** (un choix de routage propre à ce projet, pouvant être différent sur un carrier dérivé) - lisez cette ligne de statut avant de considérer une affectation de signal comme fixe.

Ce n'est pas un tutoriel guidé (il n'existe pas un unique carrier « correct » pour chaque cas d'usage) - c'est la documentation de référence réelle dont un concepteur matériel expérimenté a besoin pour partir d'une cartographie de broches déjà vérifiée plutôt que d'une simple fiche technique.

---

## 📁 Catalogue de Projets

Nouveau dans l'écosystème ? `./starter-kit.sh` (ou `starter-kit.bat`
sous Windows) clone les 12 dépôts du tableau ci-dessous comme dossiers
frères dans un même répertoire - la disposition standard que tout
script inter-dépôts ici suppose déjà. Le relancer est sûr : tout ce qui
est déjà cloné reste intact. À partir de là,
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(l'un des 12) peut vérifier les versions et compiler/mettre à jour
n'importe quel projet.

### 💠 Écosystème Core (Contrôle Principal)
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | Micrologiciel de contrôle de mouvement core pour STM32H745/G474 avec cinématique S-Curve. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | API Node.js headless et backend WebSocket pour l'orchestration robotique. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | Tableau de bord web avancé basé sur React pour la surveillance et le contrôle 3D. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | Application de bureau Python/Qt haute performance pour l'automatisation industrielle. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | Interface tactile Flutter pour écrans industriels 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | Application mobile native Kotlin avec login biométrique pour la gestion à distance. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | Application mobile Flutter pour iOS/iPadOS avec synchronisation WebSocket en temps réel. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | Éditeur graphique URDF pour valider et pousser les modèles de robots vers le catalogue. |
| [URTC](https://github.com/JuanenRac/URTC) | Micrologiciel de contrôleur d'outils universel pour plus de 25 outils spécialisés. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | Outil GUI pour les mises à jour de firmware CAN-OTA et SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Outil de diagnostic CAN-bus avec panneaux de télémétrie par outil. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Outil Web Serial pour les tests et l'analyse instantanée du matériel. |

### 👁️ Nœud d'IA de Vision (Optimisé pour Hailo-8)
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | Nœud de perception haute vitesse pour 8 flux de caméras USB 3.0 simultanés. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | Pipeline GStreamer/MediaMTX optimisé pour le relais vidéo industriel. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | Bibliothèque de modèles YOLO accélérés matériellement pour l'AQ des composants et du CMS. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | Détection d'intrusion par IA en temps réel pour la protection du volume de travail. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | Retour cinématique basé sur l'image pour une correction de pose sub-millimétrique. |

### 🧠 Nœud d'IA Cognitive (Optimisé pour Hailo-10)
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | Nœud de raisonnement sémantique pour la planification logique et le contrôle vocal. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | Implémentation du modèle Vision-Language-Action pour l'exécution de tâches complexes. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | Pipeline local STT/TTS pour l'interaction naturelle avec l'opérateur. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | Orchestrateur basé sur LLM avec récupération d'erreur contextuelle. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | Assistant IA basé sur RAG entraîné sur les manuels techniques et le code source. |

### 🐝 Orchestration & Essaim
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | Gestionnaire de flotte pour la coordination multi-robot et l'évitement de collision. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | Sincronisation PTP pour la coordination de robots avec précision nanoseconde. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | Optimiseur de trajectoire distribué pour les essaims en espace partagé. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | Planificateur de tâches basé sur les priorités pour flottes hétérogènes. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | Moniteur de haute disponibilité avec basculement transparent des missions. |

### 🎮 Jumeau Numérique & Simulation
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | Moteur de simulation physique haute fidélité pour des tests sans risque. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | Simulation physique réelle (MuJoCo/PhysX) des chaînes URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | Interface Hardware-in-the-loop pour la cohérence entre état réel et virtuel. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | Générateur de datasets procéduraux pour l'entraînement de modèles IA. |

### 📊 Données & Analytique
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | Stockage Big Data pour la télémétrie industrielle massive multi-robot. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | Ingesteur haut débit pour les logs CAN, WebSocket et système. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | Moteur de maintenance prédictive basé sur les signatures vibratoires. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | Génération automatisée d'OEE et KPI pour la gestion d'usine. |

### 🏭 Passerelle Industrielle
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | Pont d'interopérabilité pour les standards d'usine (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | Mapping des objets HydraState vers des nœuds standard OPC-UA. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | Pont de télémétrie pour les intégrations IoT et tableaux de bord externes. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | Interface standardisée pour le suivi de santé des machines et robots. |

### 🛠️ Outils Complémentaires
| Dépôt | Description |
| :--- | :--- |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | Stockage d'outils intelligent avec préchauffage et audit de cycle de vie. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | Tête d'outil avec caméras thermique et RGB intégrées pour l'AQ active. |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | Tableau de bord d'urgence portable avec alertes de sécurité haptiques. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | Interface en ligne de commande pour l'automatisation, le flashage et le devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | Extension IA pour tableaux de bord web fournissant des analyses textuelles. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | Outil GUI/CLI multiplateforme pour détecter, installer et mettre à jour manuellement chaque projet de l'écosystème. |

---

## 🤝 Contribuer
Cet écosystème fait partie d'une initiative robotique de haute technologie. Chaque projet a ses propres directives de contribution. Veuillez vous référer aux dépôts individuels pour les détails techniques.

Les labels d'issues sont standardisés sur les 45 dépôts à partir de [`.github/labels.yml`](.github/labels.yml) dans ce même dépôt, synchronisés par [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - modifiez ce seul fichier pour changer un label partout à la fois, plutôt qu'à la main dépôt par dépôt.

Un tableau de bord d'état en direct pour les 45 dépôts (stack, cible de déploiement, version actuelle - lue directement depuis la branche par défaut de chaque dépôt) est généré quotidiennement par [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) et servi depuis `docs/` via GitHub Pages : **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licence GPL-3.0.
