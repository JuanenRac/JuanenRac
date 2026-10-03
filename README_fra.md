<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Bannière Electro Hobby 3D" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

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
  <img src="https://img.shields.io/badge/%C3%89cosyst%C3%A8mes-3-00E5FF.svg" alt="Trois écosystèmes">
</p>

Trois écosystèmes d'ingénierie indépendants, un seul auteur. **HYDRA-UMC** est une plateforme robotique industrielle multicouche, du firmware temps réel jusqu'à l'IA cognitive. **URTC** est son sous-système universel d'outils robotiques : firmware temps réel et outils de bureau/web pour l'effecteur d'un robot, développé comme un produit propre avec sa propre version et sa propre maintenance. **A.R.M.O.R.** est un écosystème à part, public, de sécurité périmétrique et de domotique - détection de présence par radar, surveillance solaire et électrique, et un coordinateur central avec des clients web et mobile.

---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Bannière de l'écosystème HYDRA-UMC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plateforme-STM32%20%7C%20CM5-red.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Puissance IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenue dans l'**Écosystème HYDRA-UMC**, une plateforme robotique industrielle multicouche allant du micrologiciel temps réel de bas niveau à l'IA cognitive de haut niveau. Cette organisation héberge de nombreux projets spécialisés conçus pour travailler en parfaite synchronie pour l'automatisation de micro-usines et la robotique en essaim.

## 📈 Progression de l'Écosystème

`[██████████▊░░░░░░░░░] 54%` — Indication de référence. Le jalon 100 % correspond à un écosystème intégré fonctionnant sur du matériel réel.

> [!IMPORTANT]
> 🛠️ **Projet en pause — construction du matériel réel.** Le développement actif est suspendu le temps de construire pour de vrai la cellule physique (châssis, câblage, les vraies cartes CM5 et STM32), afin que la prochaine phase de travail dispose d'un matériel réel sur lequel s'exécuter et se valider, pas seulement d'une barre qui progresse. Le travail reprendra une fois cette construction en place.

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

## 📁 Catalogue de Projets — HYDRA-UMC

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
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.4.7 | Couche de plateforme Raspberry Pi OS pour CM5 : profils reproductibles, configuration, diagnostic, cycle de vie des services et mises à jour ; ce n'est pas une nouvelle distribution Linux. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.2.8 | Contrats versionnés, clients légers et tests de conformité communs pour services, interfaces, adaptateurs CM5 et URTC ; ne remplace pas les API des fournisseurs. |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.0 | Registre déclaratif et validateur de manifestes d'adaptateur pour les connecteurs de machines externes ; étend la propre idée de contrat du SDK aux machines externes sans remplacer les projets de passerelle industrielle. |

### 💠 Contrôle central et clients opérateur
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.1.6 | Micrologiciel de contrôle de mouvement core pour STM32H745/G474 avec cinématique S-Curve. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.0.5 | API Node.js headless et backend WebSocket pour l'orchestration robotique. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.7.6 | Tableau de bord web avancé basé sur React pour la surveillance et le contrôle 3D. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.4 | Application de bureau Python/Qt haute performance pour l'automatisation industrielle. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.0 | Interface tactile Flutter pour écrans industriels 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.6.3 | Application mobile native Kotlin avec login biométrique pour la gestion à distance. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.0 | Application mobile Flutter pour iOS/iPadOS avec synchronisation WebSocket en temps réel. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.0 | Éditeur graphique URDF pour valider et pousser les modèles de robots vers le catalogue. |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.2 | Éditeur de bureau de modèles STL - transforme, remplace, retire et ajoute de vraies pièces dans le catalogue de modèles partagé. |


### 👁️ Nœud d'IA de Vision (Optimisé pour Hailo-8)
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.0 | Nœud de perception haute vitesse pour 8 flux de caméras USB 3.0 simultanés. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.1.6 | Pipeline GStreamer/MediaMTX optimisé pour le relais vidéo industriel. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.0.9 | Bibliothèque de modèles YOLO accélérés matériellement pour l'AQ des composants et du CMS. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.1 | Détection d'intrusion par IA en temps réel pour la protection du volume de travail. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.4 | Retour cinématique basé sur l'image pour une correction de pose sub-millimétrique. |

### 🧠 Nœud d'IA Cognitive (Optimisé pour Hailo-10)
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.1 | Nœud de raisonnement sémantique pour la planification logique et le contrôle vocal. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.4 | Implémentation du modèle Vision-Language-Action pour l'exécution de tâches complexes. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.3 | Pipeline local STT/TTS pour l'interaction naturelle avec l'opérateur. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.0 | Orchestrateur basé sur LLM avec récupération d'erreur contextuelle. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.0 | Assistant IA basé sur RAG entraîné sur les manuels techniques et le code source. |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.2 | Technicien IA local à permissions contrôlées par politique : aujourd'hui une politique fixe de niveaux de risque et une liste blanche d'outils, avec une défense réelle et testée prouvant qu'un document malveillant récupéré ne peut jamais déclencher un appel d'outil ni divulguer un secret - l'IA n'obtient jamais d'autorité en générant une réponse. |

### 🐝 Orchestration & Essaim
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.3 | Gestionnaire de flotte pour la coordination multi-robot et l'évitement de collision. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.1 | Sincronisation PTP pour la coordination de robots avec précision nanoseconde. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.0.7 | Optimiseur de trajectoire distribué pour les essaims en espace partagé. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.1.8 | Planificateur de tâches basé sur les priorités pour flottes hétérogènes. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.4 | Moniteur de haute disponibilité avec basculement transparent des missions. |

### 🎮 Jumeau Numérique & Simulation
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.7 | Moteur de simulation physique haute fidélité pour des tests sans risque. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.6 | Simulation physique réelle (MuJoCo/PhysX) des chaînes URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.6 | Interface Hardware-in-the-loop pour la cohérence entre état réel et virtuel. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.0.8 | Générateur de datasets procéduraux pour l'entraînement de modèles IA. |

### 📊 Données & Analytique
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.3 | Stockage Big Data pour la télémétrie industrielle massive multi-robot. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.4 | Ingesteur haut débit pour les logs CAN, WebSocket et système. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.3 | Moteur de maintenance prédictive basé sur les signatures vibratoires. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.2 | Génération automatisée d'OEE et KPI pour la gestion d'usine. |

### 🏭 Passerelle Industrielle
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.2 | Pont d'interopérabilité pour les standards d'usine (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.5 | Mapping des objets HydraState vers des nœuds standard OPC-UA. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.2 | Pont de télémétrie pour les intégrations IoT et tableaux de bord externes. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.4 | Interface standardisée pour le suivi de santé des machines et robots. |

### 🌉 Ponts d'automatisation externe
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.0.7 | Limite de coordination ROS 2 bidirectionnelle : topics d'observation, services d'inspection et actions de cellule annulables. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.4 | Coordinateur traçable de transfert de PCB pour OpenPnP et chargement ou déchargement robotisé. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.3 | Pont sûr autour d'un logiciel d'impression 3D ; le premier adaptateur valide Moonraker sans remplacer le firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.4 | Coordinateur d'auxiliaires de cellule CNC ; trajectoire et sécurité restent natives au contrôleur. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.2 | Coordinateur d'auxiliaires de cellule laser qui ne peut ni armer, ni tirer, ni contourner les interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.0.8 | Frontière de coordination pour droïdes à pattes/humanoïdes : vocabulaire d'actions marcher/prendre/poser filtré par le contrat de sécurité partagé ; la marche et l'équilibre restent du ressort du contrôleur propre au droïde. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.0.8 | Frontière de coordination pour flottes AGV/AMR : transformation du repère usine vers le repère local d'un AMR, plus un vocabulaire d'ordres inspiré de VDA-5050 ; la planification de trajectoire reste du ressort de la navigation propre à l'AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.0.9 | Frontière de coordination pour drones équipés de caméra : vocabulaire de requêtes de vol nommées plus un watchdog déterministe de heartbeat/perte de liaison. |

### 🛠️ Outils Complémentaires
| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.2 | Tableau de bord d'urgence portable avec alertes de sécurité haptiques. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.2 | Interface en ligne de commande pour l'automatisation, le flashage et le devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.1 | Extension IA pour tableaux de bord web fournissant des analyses textuelles. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.3 | Outil GUI/CLI multiplateforme pour détecter, installer et mettre à jour manuellement chaque projet de l'écosystème. |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.2.7 | Outil de bureau Windows/Linux qui construit une image de la CM5 prête à graver, préchargée avec les versions les plus actuelles de l'écosystème, avec une configuration de premier démarrage façon Raspberry Pi Imager. |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.4 | Coordinateur d'incidents de maintenance : un rôle edge à faible privilège collecte un instantané d'inventaire/santé assaini, un rôle control-plane le rend en lecture seule et demande à un fournisseur d'IA de suggérer un diagnostic - n'applique jamais de correctif ni ne déploie rien. |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.3 | Serveur de développement reproductible : aujourd'hui un schéma de configuration à permissions et un inventaire de manifestes, évoluant vers un exécuteur de tâches/espace de travail isolé coordonné avec OPS-AGENT - aucune tâche n'a de permission de déploiement sauf si un document l'accorde explicitement. |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="Bannière de l'écosystème URTC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plateforme-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Outils-25%2B%20profils-blueviolet.svg" alt="Tools">
</p>

**URTC (Universal Robot Tool Controller)** est un produit à part entière, pas un dossier sous-système de HYDRA-UMC : firmware temps réel et une famille d'outils de bureau/web pour l'effecteur d'un robot, développés, versionnés et maintenus de façon indépendante. Un changeur d'outils équipé d'URTC se coordonne avec le contrôleur de cellule de HYDRA-UMC via FDCAN, mais le comportement temps réel de l'outil lui-même, son watchdog et son état sûr relèvent de l'autorité propre d'URTC - le contrôleur de cellule ne peut pas la contourner, et URTC ne dépend pas de HYDRA-UMC pour être développé, flashé ou diagnostiqué.

## 🏗️ Comment Fonctionne URTC

1. **Firmware de l'outil** : le firmware STM32 propre à URTC exécute chacun des plus de 25 profils d'outils spécialisés (pinces, doseurs, sondes, broches et plus), chacun avec son propre timing, ses propres limites et son propre comportement en cas de défaillance.
2. **Mise à jour sur le terrain** : CAN-OTA envoie une nouvelle image de firmware sur le même bus CAN déjà utilisé par l'outil, avec une voie complète par puce SWD/JTAG (URTC-FLASHER) comme repli qui ne dépend jamais du firmware propre de l'outil pour être vivant.
3. **Diagnostic en direct** : URTC-TESTER valide le comportement CAN temps réel d'un outil par rapport à son profil déclaré sans nécessiter un atelier complet ; URTC-WEB-STUDIO fait de même depuis un onglet de navigateur via Web Serial, sans rien à installer.
4. **Stockage et cycle de vie** : URTC-SMART-RACK conserve les outils entre deux travaux, préchauffe un outil avant un échange et tient un registre d'audit de cycle de vie (cycles, pannes, dernier étalonnage) par outil physique, pas par type d'outil.
5. **AQ active** : URTC-VISION-TOOL est elle-même un outil - une tête avec ses propres caméras thermique et RGB pour l'inspection qualité pendant le processus, pas une caméra externe vissée sur un autre outil.

## 🛠️ Stack Technologique

- **Firmware** : STM32, FDCAN (bus partagé avec le contrôleur de cellule), CAN-OTA, repli SWD/JTAG.
- **Outils de bureau** : clients GUI multiplateformes pour flasher et diagnostiquer (URTC-FLASHER, URTC-TESTER).
- **Outils de navigateur** : l'API Web Serial pour des tests matériels sans rien installer (URTC-WEB-STUDIO).
- **Données de cycle de vie** : registre d'audit non volatile par outil, avec le même critère d'intégrité F-RAM que HYDRA-UMC.

## 🔒 Sécurité

Chaque profil d'outil porte son propre watchdog et son propre comportement en cas de défaillance, indépendamment de la propre couche E-STOP du contrôleur de cellule - un outil qui perd son propre budget de temps ou le heartbeat CAN passe à son état sûr déclaré de lui-même, plutôt que d'attendre une commande externe. Le préchauffage d'URTC-SMART-RACK est borné par les mêmes limites thermiques par outil déclarées par son profil, auditées dans le même registre de cycle de vie qu'un atelier utilise pour décider si un outil est encore apte au service.

## 📁 Catalogue de Projets URTC

| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.1 | Micrologiciel de contrôleur d'outils universel pour plus de 25 outils spécialisés. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.2.1 | Outil GUI pour les mises à jour de firmware CAN-OTA et SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.2.2 | Outil de diagnostic CAN-bus avec panneaux de télémétrie par outil. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.2.2 | Outil Web Serial pour les tests et l'analyse instantanée du matériel. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.0 | Stockage d'outils intelligent avec préchauffage et audit de cycle de vie. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.0.5 | Tête d'outil avec caméras thermique et RGB intégrées pour l'AQ active. |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="Bannière de l'écosystème A.R.M.O.R." width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibilit%C3%A9-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar & Multimodal Observation Range)** est un écosystème à part, public, de sécurité périmétrique et de domotique - sans relation avec HYDRA-UMC ni URTC au-delà du même auteur et des mêmes conventions d'ingénierie (manifestes versionnés, un contrat de messages partagé, des interfaces en sept langues). Ses nœuds de terrain surveillent le périmètre d'une propriété et son installation solaire/électrique ; son serveur central et ses clients permettent à un opérateur de voir et d'agir sur ce qu'ils rapportent. Les notes de version et de maturité ci-dessous proviennent directement du manifeste et de la matrice de capacités de chaque dépôt, la même convention d'honnêteté déjà utilisée par le tableau de bord de HYDRA-UMC.

## 🏗️ Comment A.R.M.O.R. Est Construit

1. **Contrat partagé** : **ARMOR-COMMON** possède le sens des messages - JSON Schema, un validateur en Python et des types TypeScript/Kotlin générés que chaque autre dépôt consomme, sans jamais les redéfinir.
2. **Nœuds de terrain** : firmware ESP32-S3 pour la détection radar/présence (**ARMOR-RADAR**), la surveillance des onduleurs et batteries solaires (**ARMOR-SOLAR**), et la mesure électrique avec manœuvre (**ARMOR-ELECTRICAL**) ; un agent Python (**ARMOR-NETWORK**) surveille le propre réseau local de la maison et l'accessibilité d'internet depuis une machine déjà connectée à ce réseau.
3. **Coordinateur central** : **ARMOR-SERVER** conserve l'état, les utilisateurs, les alarmes, les automatisations et les preuves des caméras ; **ARMOR-SERVER-AI** et **ARMOR-VOICE-AI** ajoutent une politique visuelle explicable et des intentions vocales hors ligne qui n'agissent jamais d'elles-mêmes.
4. **Clients opérateur** : **ARMOR-STUDIO** (web) et **ARMOR-ANDROID-CONTROL** (mobile) sont des clients du serveur central, jamais du réseau de terrain directement. **ARMOR-HMI** est un panneau tactile mural (une Waveshare ESP32-S3-Touch-LCD-7C-BOX) qui montre l'état, arme et acquitte, et sera la maison de l'assistant vocal.
5. **Déploiement et tests** : **ARMOR-DEVOPS** déploie tout le graphe de services ; **ARMOR-SIMULATOR** rejoue des scénarios et des pannes reproductibles sans matériel réel ; **ARMOR-HARDWARE** porte la conception des boîtiers et sa matrice d'acceptation au banc.
6. **Opérations de l'écosystème** : **ARMOR-UPDATER** découvre, installe et met à jour chaque dépôt A.R.M.O.R. sur une machine, la même conception atomique-par-vérification que HYDRA-UMC-UPDATER ; **ARMOR-DOCS** est la documentation d'architecture canonique et la matrice de capacités.

## 🔒 Honnêteté et Sécurité

A.R.M.O.R. suit la même règle déjà appliquée par le tableau de bord de HYDRA-UMC : une affirmation n'est réelle que lorsqu'elle est vérifiée, et chaque dépôt indique clairement ce qui a déjà été testé sur du matériel réel et ce qui ne l'a pas été. Rien dans cet écosystème ne contrôle aujourd'hui le courant secteur ni l'accès physique ; les nœuds de terrain observent et rapportent, et toute future capacité de manœuvre est conçue et revue avant d'être jamais activée.

## 📁 Catalogue de Projets A.R.M.O.R.

| Dépôt | Version | Description |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.3.4 | Contrats de messages, validateurs, vecteurs de conformité et types générés |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.4.8 | Firmware du nœud de terrain pour ESP32-S3 avec trois radars et son propre panneau web |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.2.2 | Protocoles des onduleurs et batteries solaires et les messages d'un nœud passerelle |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.1.6 | Nœud électrique : compteurs, le message des relevés du réseau et les règles de manœuvre |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.1.0 | Panneau tactile pour la Waveshare ESP32-S3-Touch-LCD-7C-BOX : l'état du système sur un écran mural, armer/désarmer/acquitter, voix en appuyer-pour-parler et la page web d'un nœud ; le firmware n'a jamais tourné sur une carte. |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.0.6 | Le réseau local : ses appareils, internet et ce qui change |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.4.1 | Coordinateur central : télémétrie, alarmes, appareils, relevés solaires et électriques, le réseau local, les services système et caméras |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.1 | Politique d'inférence visuelle qui explique ses décisions et n'agit jamais |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.2.1 | Intentions vocales hors ligne avec une confirmation impossible à falsifier |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.6.0 | Console web : caméras, radar, alarmes, menus solaire et électrique, réseau local, services système, météo, un chercheur de nœuds et le concepteur de site 2D/3D |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.4.0 | Client Android de l'opérateur avec radar 2D/3D en direct |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.3 | Boîtiers, électronique et la matrice d'acceptation au banc |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.3.6 | Déploiement, banc de test du serveur central, sauvegarde et TLS |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.3 | Simulateur de télémétrie hors ligne avec pannes reproductibles |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.0.4 | Détecte, installe et met à jour les propres dépôts de l'écosystème |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.5.5 | Architecture, base de sécurité et la matrice des capacités |

---

## 🤝 Contribuer
Cet écosystème fait partie d'une initiative robotique de haute technologie. Chaque projet a ses propres directives de contribution. Veuillez vous référer aux dépôts individuels pour les détails techniques.

Les labels d'issues sont standardisés sur tous les dépôts de l'écosystème à partir de [`.github/labels.yml`](.github/labels.yml) dans ce même dépôt, synchronisés par [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - modifiez ce seul fichier pour changer un label partout à la fois, plutôt qu'à la main dépôt par dépôt. Contrairement au tableau de bord ci-dessous, cette liste est statique (une vraie matrice GitHub Actions, pas une découverte dynamique) - un nouveau dépôt y nécessite aussi une entrée, pas seulement un vrai `hydra-umc.project.json`.

Un tableau de bord d'état en direct couvrant chaque dépôt public déclarant `ecosystem: HYDRA-UMC` dans son propre `hydra-umc.project.json` (stack, cible de déploiement, version actuelle - lue directement depuis la branche par défaut de chaque dépôt, découvert dynamiquement sans liste fixe) est régénéré toutes les heures (et immédiatement après un push pertinent) par [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) et servi depuis `docs/` via GitHub Pages : **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. Il ajoute une véritable classification de maturité par projet (scaffolding / functional / established / production, chacune décidée à partir du propre CHANGELOG de ce projet - voir le docstring du module [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) pour le critère exact), son rôle (API / UI / CLI / firmware / bibliothèque / service / outil), un véritable arbre famille/parent-enfant, et des notes par projet sur ce qui est réellement implémenté aujourd'hui. Les propres dépôts d'URTC et d'A.R.M.O.R. sont découverts en direct sur ce même tableau de bord exactement de la même façon que ceux de HYDRA-UMC (voir `scripts/generate_dashboard.py`), chacun déclarant son propre champ `ecosystem` dans son propre `urtc.project.json`/`armor.project.json` - aucune liste fixe pour aucun des trois.

## 🧭 Collaboration GitHub

Le [modèle de collaboration GitHub](docs/GITHUB_COLLABORATION.md) définit un Wiki central unique, un Project unique pour l’écosystème, le périmètre des Discussions, les critères de release et la limite de l’automatisation partagée. Les [formulaires d’issues](.github/ISSUE_TEMPLATE/) et le [modèle de pull request](.github/PULL_REQUEST_TEMPLATE.md) centralisés rendent le travail logiciel, la validation matérielle et la documentation traçables sans dupliquer les manuels des projets.

Le workflow de santé communautaire est manuel et en simulation par défaut. Une fois `COMMUNITY_HEALTH_SYNC_TOKEN` configuré, il peut copier uniquement ces modèles gérés dans chaque dépôt publiant un manifeste HYDRA-UMC ; il ne supprime jamais un modèle spécifique à un projet.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licence GPL-3.0.

