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

## 📈 Progression de l'Écosystème

`[██████████▊░░░░░░░░░] 54%` — Indication de référence. Le jalon 100 % correspond à un écosystème intégré fonctionnant sur du matériel réel.

---

## 🚀 Caractéristiques Clés et Évolutivité

- **Évolutivité Multi-Robot** : Prend en charge jusqu'à 8 unités robotiques distribuées (actuellement de 3, 4, 5 et 6 axes ; évolutif vers 7, 8, 9 axes et architectures de robots doubles dans les futures versions).
- **Étage Local Intégré** : La carte principale HYDRA-UMC dispose d'un **Étage Local à 6 axes** intégré pour des tâches auxiliaires, notamment des robots secondaires, des révolveds ATC (Automatic Tool Changer), la synchronisation de bandes transporteuses ou des portiques de tables XYZ.

---

## 🏗️ Architecture de l'Écosystème

L'écosystème v1.1 est une plateforme produit en couches : il s'appuie sur les technologies Linux et Raspberry Pi existantes, sans créer un nouveau système d'exploitation ni remplacer les API des fournisseurs.

1.  **Base de plateforme** : Raspberry Pi OS ARM64 et les services Linux standard fournissent la base CM5 prise en charge.
2.  **Plateforme et contrats** : **HYDRA-UMC-OS** fournit des profils reproductibles, services, diagnostics et mises à jour sur Raspberry Pi OS ; **HYDRA-UMC-SDK** publie des contrats versionnés, clients légers et tests de conformité.
3.  **Exécution temps réel** : le firmware **HYDRA-UMC** et URTC sur STM32/MCU conservent limites de mouvement, watchdogs et arrêt sûr.
4.  **Coordination et opérations** : services serveur, distribution des tâches, télémétrie et configuration coordonnent les équipements sans contourner la frontière de sécurité du MCU.
5.  **Interfaces opérateur** : Studio, Suite, DSI, Web, bureau, mobile et CLI utilisent les contrats du SDK.
6.  **Perception et intelligence** : vision, Hailo et services cognitifs proposent des observations ou plans ; ils n'ont aucune autorité de sécurité physique.
7.  **Ingénierie, industrie et données** : Jumeau Numérique, HIL/physique, passerelles OPC-UA/MQTT/MTConnect et données valident et intègrent le système.

Le développement commence par l'architecture et le modèle de services publics de **HYDRA-UMC-OS**, puis utilise les contrats et règles de conformité de **HYDRA-UMC-SDK**. L'autorité de sécurité du MCU/URTC est maintenue dans tous les flux.

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
sous Windows) clone 13 dépôts principaux - un ensemble de départ choisi
à la main, pas le catalogue complet ci-dessous - comme dossiers frères
dans un même répertoire : la disposition standard que tout script
inter-dépôts ici suppose déjà. Le relancer est sûr : tout ce qui est
déjà cloné reste intact. À partir de là,
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(l'un des 13 dépôts qui viennent d'être clonés) peut vérifier les
versions et compiler/mettre à jour n'importe lequel des autres projets
du catalogue complet ci-dessous.

### 🧱 Fondation de plateforme et contrats
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | Couche de plateforme Raspberry Pi OS pour CM5 : profils reproductibles, configuration, diagnostic, cycle de vie des services et mises à jour ; ce n'est pas une nouvelle distribution Linux. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | Contrats versionnés, clients légers et tests de conformité communs pour services, interfaces, adaptateurs CM5 et URTC ; ne remplace pas les API des fournisseurs. |

### 💠 Contrôle central et clients opérateur
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


### 🔧 Cœur et outils URTC
| Dépôt | Description |
| :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | Micrologiciel de contrôleur d'outils universel pour plus de 25 outils spécialisés. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | Outil GUI pour les mises à jour de firmware CAN-OTA et SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Outil de diagnostic CAN-bus avec panneaux de télémétrie par outil. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Outil Web Serial pour les tests et l'analyse instantanée du matériel. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | Stockage d'outils intelligent avec préchauffage et audit de cycle de vie. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | Tête d'outil avec caméras thermique et RGB intégrées pour l'AQ active. |

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

### 🌉 Ponts d'automatisation externe
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | Limite de coordination ROS 2 bidirectionnelle : topics d'observation, services d'inspection et actions de cellule annulables. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | Coordinateur traçable de transfert de PCB pour OpenPnP et chargement ou déchargement robotisé. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | Pont sûr autour d'un logiciel d'impression 3D ; le premier adaptateur valide Moonraker sans remplacer le firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | Coordinateur d'auxiliaires de cellule CNC ; trajectoire et sécurité restent natives au contrôleur. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | Coordinateur d'auxiliaires de cellule laser qui ne peut ni armer, ni tirer, ni contourner les interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | Frontière de coordination pour droïdes à pattes/humanoïdes : vocabulaire d'actions marcher/prendre/poser filtré par le contrat de sécurité partagé ; la marche et l'équilibre restent du ressort du contrôleur propre au droïde. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | Frontière de coordination pour flottes AGV/AMR : transformation du repère usine vers le repère local d'un AMR, plus un vocabulaire d'ordres inspiré de VDA-5050 ; la planification de trajectoire reste du ressort de la navigation propre à l'AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | Frontière de coordination pour drones équipés de caméra : vocabulaire de requêtes de vol nommées plus un watchdog déterministe de heartbeat/perte de liaison. |

### 🛠️ Outils Complémentaires
| Dépôt | Description |
| :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | Tableau de bord d'urgence portable avec alertes de sécurité haptiques. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | Interface en ligne de commande pour l'automatisation, le flashage et le devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | Extension IA pour tableaux de bord web fournissant des analyses textuelles. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | Outil GUI/CLI multiplateforme pour détecter, installer et mettre à jour manuellement chaque projet de l'écosystème. |

---

## 🤝 Contribuer
Cet écosystème fait partie d'une initiative robotique de haute technologie. Chaque projet a ses propres directives de contribution. Veuillez vous référer aux dépôts individuels pour les détails techniques.

Les labels d'issues sont standardisés sur tous les dépôts de l'écosystème à partir de [`.github/labels.yml`](.github/labels.yml) dans ce même dépôt, synchronisés par [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - modifiez ce seul fichier pour changer un label partout à la fois, plutôt qu'à la main dépôt par dépôt. Contrairement au tableau de bord ci-dessous, cette liste est statique (une vraie matrice GitHub Actions, pas une découverte dynamique) - un nouveau dépôt y nécessite aussi une entrée, pas seulement un vrai `hydra-umc.project.json`.

Un tableau de bord d'état en direct couvrant chaque dépôt public déclarant `ecosystem: HYDRA-UMC` dans son propre `hydra-umc.project.json` (stack, cible de déploiement, version actuelle - lue directement depuis la branche par défaut de chaque dépôt, découvert dynamiquement sans liste fixe) est régénéré toutes les heures (et immédiatement après un push pertinent) par [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) et servi depuis `docs/` via GitHub Pages : **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. La v3 ajoute une véritable classification de maturité par projet (scaffolding / functional / established / production, chacune décidée à partir du propre CHANGELOG de ce projet - voir le docstring du module [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) pour le critère exact), son rôle (API / UI / CLI / firmware / bibliothèque / service / outil), un véritable arbre famille/parent-enfant, et des notes par projet sur ce qui est réellement implémenté aujourd'hui.

## 🧭 Collaboration GitHub

Le [modèle de collaboration GitHub](docs/GITHUB_COLLABORATION.md) définit un Wiki central unique, un Project unique pour l’écosystème, le périmètre des Discussions, les critères de release et la limite de l’automatisation partagée. Les [formulaires d’issues](.github/ISSUE_TEMPLATE/) et le [modèle de pull request](.github/PULL_REQUEST_TEMPLATE.md) centralisés rendent le travail logiciel, la validation matérielle et la documentation traçables sans dupliquer les manuels des projets.

Le workflow de santé communautaire est manuel et en simulation par défaut. Une fois `COMMUNITY_HEALTH_SYNC_TOKEN` configuré, il peut copier uniquement ces modèles gérés dans chaque dépôt publiant un manifeste HYDRA-UMC ; il ne supprime jamais un modèle spécifique à un projet.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licence GPL-3.0.
