<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Bannière Electro Hobby 3D" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  🇺🇸 <a href="README.md">English</a> |
  <a href="README\_spa.md">🇪🇸 Español</a> |
  <b>🇫🇷 Français</b> |
  <a href="README\_ita.md">🇮🇹 Italiano</a> |
  <a href="README\_deu.md">🇩🇪 Deutsch</a> |
  <a href="README\_zho.md">🇨🇳 简体中文</a> |
  <a href="README\_jpn.md">🇯🇵 日本語</a> |
  <a href="README\_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="Licence GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Matériel CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Quatre écosystèmes">
</p>

Quatre écosystèmes d'ingénierie indépendants, un seul auteur. **HYDRA-UMC** est une plateforme de robotique industrielle multicouche, allant du micrologiciel en temps réel à l'IA cognitive. **URTC** est son sous-système universel d'outils robotiques : micrologiciel en temps réel et outils de bureau/web pour l'effecteur final d'un robot, développé comme un produit à part entière avec un versionnage et des outils de maintenance indépendants. **A.R.M.O.R.** est un écosystème public distinct de sécurité périmétrique et de domotique : détection de présence par radar, surveillance solaire et électrique, et un coordinateur central avec des clients web et mobiles. **EH3D Fabrication Suite** est un écosystème logiciel intégré pour le prototypage de circuits imprimés (PCB), le traitement FAO (CAM), l'inspection par vision par ordinateur, la gestion Pick \& Place et le contrôle CNC/Laser s'interfaçant avec le matériel HYDRA-UMC et les machines d'atelier spécialisées.


## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Tableau de bord et surveillance | 🟢 | Le tableau de bord d'état, la surveillance de la CI, la matrice de santé, la vérification des liens et le résumé des versions s'exécutent de façon planifiée dans GitHub Actions, et leurs dernières exécutions réussissent. |
| Tests | 🟢 | 51 tests réussissent (`python -m unittest discover -s tests`) : le catalogue, la surveillance, les bannières, l'amorçage de la feuille de route et la parité des README. |
| Catalogue et versions | 🟡 | La colonne Version de chaque tableau de projets est remplie par un script à partir du manifeste de chaque dépôt et vérifiée, donc elle ne se périme pas ; les descriptions d'une ligne sont écrites à la main. |
| Barres de progression | 🟢 | Le pourcentage de chaque écosystème est calculé par `scripts/ecosystem_progress.py` à partir de la maturité et de la preuve que chaque dépôt déclare dans son propre manifeste, et renouvelé avec le tableau de bord ; le jalon de 100 % reste un écosystème entièrement intégré fonctionnant sur du matériel réel. |
| Parité en huit langues | 🟢 | Les huit fichiers README gardent les mêmes sections, les mêmes liens GitHub et le même nombre de lignes de tableau, et un test échoue si l'un d'eux dérive. |
| Matériel réel | 🟢 | Sans objet : ce dépôt contient le profil et son automatisation, rien ici ne tourne sur du matériel. |
| Documentation | 🟢 | README en huit langues avec les quatre écosystèmes, le guide de collaboration sur GitHub et les fichiers de communauté. |

## 🧭 À propos d'Electro Hobby 3D et de son outil de mise à jour

**Electro Hobby 3D** est l'atelier de JuanenRac : de l'électronique, de la robotique et du logiciel conçus, construits, programmés et testés au même endroit. Chaque dépôt se décrit par un manifeste, a sa propre documentation et dit ce qui a été essayé ou non sur du matériel réel.

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) est **l'outil de mise à jour des quatre écosystèmes** : une fenêtre et une ligne de commande qui passent la main à l'outil de chaque écosystème, lesquels découvrent, installent et mettent à jour ses dépôts. Chaque écosystème ci-dessous nomme le sien.

| Écosystème | Ce que c'est | Outil de mise à jour |
|---|---|---|
| **HYDRA-UMC** | Robotique industrielle et commande de machines, du firmware temps réel à l'IA cognitive | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | Firmware et outils pour les organes terminaux d'un robot | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | Sécurité périmétrique et domotique | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | Prototypage de circuits imprimés, FAO, CNC et laser, pick and place | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

\---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Bannière de l'écosystème HYDRA-UMC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Puissance IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Pile logicielle">
</p>

Bienvenue dans l'**écosystème HYDRA-UMC**, une plateforme de robotique industrielle multicouche allant du micrologiciel bas niveau en temps réel à l'IA cognitive de haut niveau. Cette organisation héberge de nombreux projets spécialisés conçus pour fonctionner en parfaite synchronie pour l'automatisation de micro-usines et la robotique en escarmouche (swarm robotics).

**Outil de mise à jour :** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) détecte, installe et met à jour les dépôts de cet écosystème ; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) le fait pour les quatre.

## 📈 Progression de l'écosystème

<!-- progress:hydra-umc -->
`\[█████████▎░░░░░░░░░░] 46%` — Calculé à partir de données réelles : la maturité et la preuve que chacun de ses 56 dépôts déclare dans son propre manifeste. Le jalon de 100 % est un écosystème entièrement intégré fonctionnant sur du matériel réel.
<!-- /progress:hydra-umc -->

> \[!IMPORTANT]
> 🛠️ \*\*Projet en pause — construction du matériel réel.\*\* Le développement actif est suspendu pendant que la cellule robotique physique (châssis, câblage, véritables cartes CM5 et STM32) est construite pour de vrai, afin que la prochaine phase de travail dispose de matériel réel pour s'exécuter et être validée, et non pas seulement d'une barre de progression qui avance. Le travail reprendra une fois cet assemblage en place.

\---

## 🚀 Caractéristiques principales et évolutivité

* **Évolutivité multi-robots** : Prend en charge jusqu'à 8 unités robotiques distribuées (3, 4, 5 et 6 axes actuellement ; passage à 7, 8, 9 axes et architectures multi-robots dans les versions futures).
* **Étape locale intégrée** : La carte principale HYDRA-UMC dispose d'une **étape locale à 6 axes** intégrée pour les tâches auxiliaires, notamment les robots secondaires, les changeurs d'outils automatiques (ATC) revolver, la synchronisation de bandes transporteuses ou les portiques de tables XYZ.

\---

## 🏗️ Architecture de l'écosystème

L'écosystème v1.1 est une plateforme de produits en couches : il s'appuie sur la technologie établie Linux et Raspberry Pi au lieu de créer un nouveau système d'exploitation ou de remplacer les API des fournisseurs.

1. **Base de la plateforme** : Raspberry Pi OS ARM64 et les services Linux standard fournissent la fondation CM5 prise en charge.
2. **Plateforme et contrats** : **HYDRA-UMC-OS** regroupe des profils reproductibles, des services, des diagnostics et des mises à jour sur Raspberry Pi OS ; **HYDRA-UMC-SDK** publie des contrats versionnés, des clients légers et des bancs de conformité.
3. **Exécution en temps réel** : Le micrologiciel **HYDRA-UMC** gère les limites de mouvement, les chiens de garde (watchdogs) et l'arrêt d'urgence sécurisé sur STM32/MCU ; l'outil lui-même et son autorité en temps réel sur l'effecteur final relèvent de l'écosystème distinct **URTC** ci-dessous.
4. **Coordination et opérations** : Les services serveur, la répartition des tâches, la télémétrie et la configuration coordonnent les appareils sans contourner la limite de sécurité du MCU.
5. **Interfaces opérateurs** : Studio, Suite, DSI, web, bureau, mobile et clients CLI utilisent les contrats du SDK.
6. **Perception et intelligence** : Vision, Hailo et les services cognitifs proposent des observations ou des plans ; ils n'ont aucune autorité de sécurité physique.
7. **Ingénierie, industrie et données** : Les passerelles et services de données Jumeau Numérique (Digital Twin), HIL/physique, OPC-UA/MQTT/MTConnect valident et intègrent le système.

Pour les conseils d'implémentation, commencez par la documentation publique d'architecture et de services dans **HYDRA-UMC-OS**, puis utilisez les contrats et les règles de conformité dans **HYDRA-UMC-SDK**. L'autorité de sécurité du MCU est préservée tout au long de chaque flux.

\---

## 🛠️ Pile technologique et Outils

L'écosystème s'appuie sur une pile moderne et haute performance pour une fiabilité critique :

### 💠 Embarqué et Temps Réel (Exécution)

* **Microcontrôleurs** : STM32H745 (Double cœur 480 MHz), STM32G474 (170 MHz), STM32F303.
* **Frameworks** : FreeRTOS (mode AMP), CMSIS-DSP, STM32 HAL/LL.
* **Protocoles** : FDCAN (1 Mbps / 5 Mbps), CAN-OTA, SPI (IPC Esclave 50 MHz), I2C, UART.
* **Cinématique** : Génération de profils en S, Cinématique Inverse en temps réel (IK).

### 🧠 IA de Bord et Perception (Intelligence)

* **Accélérateurs** : Hailo-8 (26 TOPS) pour 8 flux de caméras simultanés, Hailo-10 (40 TOPS) pour l'IA générative.
* **Modèles** : YOLOv10 (Détection), OpenVLA (Action), Whisper (Voix), Llama-3 (Raisonnement).
* **Inter-nœuds** : gRPC sur Protobuf et échange de métadonnées SPI-DMA haut débit.

### 🌐 Backend et Coordination (Coordination)

* **Runtimes** : Node.js 20+ (API), Rust 1.80+ (Orchestrateur), Go (CLI).
* **Infrastructure** : Express, Fastify, Socket.io (WebSocket), gRPC.
* **Base de données** : InfluxDB/TimescaleDB (Télémétrie), Redis (État), SQLite.

### 💻 Tableaux de bord et Interface utilisateur (Interface)

* **Web** : React 19, Vite, Three.js (Viewport 3D), Tailwind CSS.
* **Natif** : Python 3.12/PySide6 (Suite), Kotlin (Android Natif), Flutter 3.x (iOS \& DSI).

\---

## 📋 Configuration système requise

* **Nœud de calcul** : Raspberry Pi CM5 (4 Go+ de RAM) avec stockage NVMe/eMMC.
* **Matériel IA** : Modules M.2 Hailo-8 / Hailo-10 (Clé M).
* **Bus de terrain** : Ethernet Gigabit pour le LAN et FDCAN (ISO 11898-1:2015) pour les actionneurs.
* **OS Client** : Android 10+, iOS 15+, Windows 10/11 (Haute définition), Ubuntu 22.04 LTS.

\---

## 🔒 Sécurité Industrielle

* **Couche E-STOP (Arrêt d'urgence)** : Ligne d'urgence câblée en dur + Trames d'urgence CAN haute priorité (<1 ms).
* **Sécurité IA** : Zones de sécurité 3D avec coupure automatique du couple moteur en cas d'intrusion humaine.
* **Cybersécurité** : Authentification sans état basée sur JWT + mTLS pour un trafic inter-nœuds sécurisé.
* **Intégrité** : F-RAM non volatile pour l'audit du cycle de vie des outils et la récupération d'état.

\---

## 🔧 Hacking Matériel : Construire sa propre carte porteuse (Carrier)

La carte de contrôle du robot est construite autour d'un **Raspberry Pi CM5**, et le double connecteur Hirose DF40 du CM5 est un brochage (pinout) fixe, officiel et public (Tableau 5 de la fiche technique officielle du CM5 de Raspberry Pi) — ce n'est pas une spécification propre à ce projet. Cela signifie qu'une carte porteuse tierce compatible est un projet réel et réalisable, et non un exercice d'ingénierie inverse :

* **Commencez ici** : [`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) — indique quelles broches fixes du CM5 cette carte utilise réellement (Ethernet, les 2 PHYs natifs USB3 SuperSpeed, l'en-tête du ventilateur de refroidissement côté CM5) et pourquoi, réorganisées par fonction à partir du tableau officiel des broches.
* **L'accès facile** : l'en-tête **GPIO standard à 40 broches du Raspberry Pi** (la même disposition "B+" inchangée depuis 2014) est déporté sur cette carte exactement comme sur n'importe quel Raspberry Pi — les HATs RPi existants et les outils GPIO fonctionnent sans modification. Une poignée de positions déjà utilisées par la liaison STM32 de cette carte sont sérigraphiées/notées pour que vous sachiez lesquelles éviter.
* **Pour aller plus loin** : [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) explique comment le CM5, le "Cerveau Cinématique" STM32H745 et le "Contrôleur de Robot" STM32G474 communiquent entre eux (SPI1 + FDCAN1 + la boîte aux lettres IPC CM7↔CM4) — la couche qu'une refonte de carte porteuse devra préserver si elle souhaite rester compatible avec le micrologiciel de ce projet.
* Chaque document de brochage indique clairement s'il est **CONFIRMÉ** (tiré directement d'un tableau de fiche technique officiel) ou **PROPOSÉ** (choix de routage propre au projet, modifiable sur une carte dérivée) — lisez cette ligne d'état avant de considérer une assignation de signal comme figée.

Il ne s'agit pas d'un tutoriel guidé (il n'y a pas de carte porteuse "unique et idéale" pour chaque cas d'usage) — c'est le véritable matériel de référence dont un concepteur matériel expérimenté a besoin pour partir d'une table de routage saine plutôt que d'une simple fiche technique.

\---

## 📁 Catalogue des Projets HYDRA-UMC

Nouveau dans l'écosystème ? `./starter-kit.sh` (ou `starter-kit.bat` sous Windows) clone 13 référentiels principaux — un ensemble de départ trié sur le volet — en tant que dossiers frères dans un seul répertoire : la disposition standard que chaque script multi-dépôt suppose déjà. Un deuxième argument clone tout un écosystème à la place, découvert dynamiquement par son manifeste : `hydra-umc`, `urtc`, `armor`, `eh3d` ou `all` (par exemple `./starter-kit.sh \~/work armor`). Relancer le script est sans danger : tout ce qui est déjà cloné reste inchangé. À partir de là, le programme de mise à jour de chaque écosystème — ou [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) pour les quatre — peut vérifier les versions et compiler/mettre à jour n'importe quel autre projet.

### 🧱 Fondations de la Plateforme et Contrats

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.4|Couche de plateforme Raspberry Pi OS pour CM5 : profils reproductibles, configuration, diagnostics, cycle de vie des services et mises à jour ; ce n'est pas une nouvelle distribution Linux.|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.3.7|Contrats versionnés partagés, clients légers et bancs de conformité pour les services, IUs et adaptateurs CM5 ; ne remplace pas les API des fournisseurs.|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.5|Registre déclaratif de manifestes d'adaptateurs et validateur pour les connecteurs de machines externes ; étend l'idée de contrat du SDK aux machines externes sans remplacer les projets de passerelles industrielles.|

### 💠 Contrôle Principal et Clients Opérateurs

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.3|Micrologiciel principal de contrôle de mouvement pour STM32H745/G474 avec cinématique en S.|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.2|API Node.js sans tête (headless) et backend WebSocket pour l'orchestration robotique.|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.2|Tableau de bord web avancé basé sur React pour la surveillance et le contrôle 3D du robot.|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.7.1|Application de bureau haute performance Python/Qt pour l'automatisation industrielle.|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.7|Interface tactile dédiée basée sur Flutter pour écrans industriels de 7 pouces (CM5).|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.2|Application mobile native en Kotlin avec connexion biométrique pour la gestion à distance du robot.|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.7|Application mobile Flutter pour iOS/iPadOS avec synchronisation WebSocket en temps réel.|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.5|Éditeur URDF graphique pour valider et envoyer des modèles de robots au catalogue.|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.7|Éditeur de modèles STL de bureau — transformer, remplacer, supprimer et ajouter de vraies pièces dans le catalogue de modèles partagé.|

### 👁️ Nœud d'IA de Vision (Optimisé pour Hailo-8)

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.6|Nœud de perception haute vitesse pour 8 flux de caméras USB 3.0 simultanés.|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.1|Pipeline GStreamer/MediaMTX optimisé pour le relais vidéo industriel.|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.5|Bibliothèque de modèles YOLO accélérés par matériel pour le contrôle qualité des composants CMS et cartes.|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.5|Détection d'intrusion par IA en temps réel pour la protection du volume de travail robotique.|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.2.0|Rétroaction cinématique basée sur l'image pour la correction de pose submillimétrique.|

### 🧠 Nœud d'IA Cognitive (Optimisé pour Hailo-10)

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.5|Nœud de raisonnement sémantique pour la planification de mission logique et le contrôle vocal.|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.1.8|Implémentation du modèle Vision-Langage-Action (VLA) pour l'exécution de tâches complexes.|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.1.8|Pipeline STT/TTS local et privé pour l'interaction en langage naturel avec l'opérateur.|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.4|Orchestrateur de mission basé sur un LLM avec récupération d'erreur contextuelle.|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.5|Assistant IA basé sur RAG entraîné sur les manuels techniques et le code source.|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.7|Technicien de maintenance IA local et réglementé par des politiques : une politique de niveau de risque fixe et une liste blanche d'outils aujourd'hui, avec une défense réelle et testée prouvant qu'un document récupéré malveillant ne peut jamais déclencher un appel d'outil ou fuiter un secret — l'IA n'obtient jamais d'autorité en générant une réponse.|

### 🐝 Orchestration et Essaim (Swarm)

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.1.9|Gestionnaire de flotte pour la coordination multi-robots et l'évitement des collisions.|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.5|Synchronisation PTP (Precision Time Protocol) pour la synchronisation des robots à la nanoseconde.|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.1|Optimiseur de trajectoire distribué pour les essaims de robots en espace de travail partagé.|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.3|Planificateur de tâches basé sur les priorités pour les flottes de robots hétérogènes.|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.1.9|Moniteur de haute disponibilité avec basculement de mission transparent.|

### 🎮 Jumeau Numérique et Simulation

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.1.0|Moteur de simulation physique haute fidélité pour des tests de robots sans risque.|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.0.9|Simulation physique du monde réel (MuJoCo/PhysX) de chaînes URDF.|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.1.0|Interface Hardware-in-the-Loop (matériel dans la boucle) pour la synchronisation des commandes réelles vs virtuelles.|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.1|Générateur procédural de jeux de données d'entraînement pour les nœuds de vision.|

### 📊 Données et Analytique

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.1.9|Stockage Big Data pour les données massives de robotique industrielle.|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.8|Collecteur à haut débit pour CAN, WebSocket et journaux système.|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.1.8|Moteur de maintenance prédictive basé sur les signatures de vibration des moteurs.|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.6|Génération automatisée de TRS (OEE) et de KPI pour la gestion des usines industrielles.|

### 🏭 Passerelle Industrielle

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.6|Pont d'interopérabilité Industrie 4.0 pour les standards d'usine (OPC-UA/MQTT).|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.2.0|Mappage des objets robotiques HydraState vers des nœuds OPC-UA standard.|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.7|Passerelle de télémétrie pour les intégrations IoT et les tableaux de bord externes.|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.1.9|Interface standardisée pour la surveillance de l'état des machines-outils et des robots.|

### 🌉 Ponts d'Automatisation Externes

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.3|Limite de coordination ROS 2 bidirectionnelle : sujets pour l'observation, services pour l'inspection et actions annulables pour les tâches de cellule.|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.2.0|Coordinateur de transfert de PCB traçable pour OpenPnP et chargement/déchargement assisté par robot.|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.1.9|Pont sécurisé autour du logiciel d'imprimante 3D natif ; le premier adaptateur valide la disponibilité de Moonraker sans remplacer le micrologiciel.|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.2.0|Coordinateur auxiliaire de cellule CNC ; la trajectoire du contrôleur et la sécurité de la machine restent natives.|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.1.8|Coordinateur auxiliaire de cellule laser qui ne peut pas armer, déclencher ou contourner les interverrouillages laser.|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.3|Limite de coordination pour les droïdes bipèdes/humanoïdes : vocabulaire d'action nommé (marcher/prendre/poser) régi par le contrat de sécurité partagé ; la démarche et l'équilibre restent sur le contrôleur propre au droïde.|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.4|Limite de coordination pour les flottes AGV/AMR : transformation de repère usine-vers-local plus un vocabulaire d'ordres inspiré de VDA-5050 ; la planification de trajectoire reste gérée par la navigation propre à l'AMR.|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.5|Limite de coordination pour les drones (UAV) équipés de caméras : vocabulaire de demande de vol nommé plus un chien de garde (watchdog) de sécurité déterministe en cas de perte de battement de cœur/liaison.|

### 🛠️ Outils Complémentaires

|Dépôt|Version|Description|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.6|Tableau de bord d'urgence portable avec alertes de sécurité haptiques.|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.1.8|Interface en ligne de commande pour l'automatisation de flotte, le flashage et le devops.|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.7|Extension IA pour les tableaux de bord web fournissant des analyses en langage naturel.|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.4.9|Outil GUI/CLI multiplateforme pour détecter, installer et mettre à jour manuellement chaque projet de l'écosystème.|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.2|Outil de bureau Windows/Linux qui génère une image CM5 prête à flasher, préchargée avec les versions les plus récentes de l'écosystème et une configuration de premier démarrage de style Raspberry-Pi-Imager.|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.1.9|Coordinateur d'incidents de maintenance : un rôle de bord (edge) à faible privilège collecte un instantané d'inventaire/santé aseptisé, un rôle de plan de contrôle le rend en lecture seule et demande à un fournisseur d'IA de suggérer un diagnostic — n'applique jamais de correctif et ne déploie rien.|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.1.9|Hôte de développement reproductible : un schéma de configuration régi par des politiques et un inventaire de manifestes aujourd'hui, évoluant vers un exécuteur de tâches/espaces de travail isolé coordonné avec OPS-AGENT — aucune tâche n'a jamais l'autorisation de déploiement à moins qu'un document ne l'accorde explicitement.|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.4|Architecture, interfaces, base de référence de sécurité, matrice de capacités et catalogue de projets généré de l'écosystème, ainsi que les outils qui comparent tous les dépôts.|

\---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="Bannière de l'écosystème URTC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32-red.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Tools-25%2B%20profiles-blueviolet.svg" alt="Outils">
</p>

**URTC (Universal Robot Tool Controller)** est un produit à part entière, et non un dossier de sous-système HYDRA-UMC : micrologiciel en temps réel et une famille d'outils de bureau/web pour l'effecteur final d'un robot, développés, versionnés et maintenus de manière indépendante. Un changeur d'outils équipé d'URTC se coordonne avec le contrôleur de cellule d'HYDRA-UMC sur FDCAN, mais le comportement en temps réel, le chien de garde et l'état sûr de l'outil relèvent de la propre autorité d'URTC — le contrôleur de cellule ne peut pas contourner cela, et URTC ne dépend pas d'HYDRA-UMC pour être développé, flashé ou diagnostiqué.

**Outil de mise à jour :** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) détecte, installe et met à jour les dépôts de cet écosystème ; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) le fait pour les quatre.

<!-- progress:urtc -->
`\[███████▋░░░░░░░░░░░░] 38%` — Calculé à partir de données réelles : la maturité et la preuve que chacun de ses 10 dépôts déclare dans son propre manifeste. Le jalon de 100 % est un écosystème entièrement intégré fonctionnant sur du matériel réel.
<!-- /progress:urtc -->

## 🏗️ Comment fonctionne URTC

1. **Micrologiciel de l'outil** : Le micrologiciel STM32 propre à URTC exécute chacun des 25+ profils d'outils spécialisés (pinces, pondes, distributeurs, broches, etc.), chacun avec ses propres temporisations, limites et comportements en cas de défaut.
2. **Mise à jour sur le terrain** : CAN-OTA pousse une nouvelle image de micrologiciel sur le même bus CAN que l'outil utilise déjà, avec un chemin SWD/JTAG pleine puce (URTC-FLASHER) comme solution de secours qui ne dépend jamais du fait que le micrologiciel propre de l'outil soit actif.
3. **Diagnostics en direct** : URTC-TESTER valide le comportement CAN en temps réel d'un outil par rapport à son profil déclaré sans configuration d'atelier complète ; URTC-WEB-STUDIO fait de même depuis un onglet de navigateur via Web Serial, sans rien à installer.
4. **Stockage et cycle de vie** : URTC-SMART-RACK maintient les outils entre les tâches, en préchauffe un avant un transfert et conserve une piste d'audit du cycle de vie (cycles, défauts, dernière calibration) par outil physique, et non par type d'outil.
5. **AQ active (Assurance Qualité)** : URTC-VISION-TOOL est lui-même un outil — une tête d'outil dotée de ses propres caméras thermique et RVB pour l'inspection de qualité en cours de processus, et non une caméra externe boulonnée sur un autre outil.
6. **Base partagée** : **URTC-COMMON** contient le protocole CAN de la tête d'outil sous forme de données, avec du code généré et des vecteurs de conformité ; **URTC-DOCS** contient l'architecture, la base de référence de sécurité et la matrice de capacités.

## 🛠️ Pile technologique

* **Micrologiciel** : STM32, FDCAN (bus partagé avec le contrôleur de cellule), CAN-OTA, solution de secours SWD/JTAG.
* **Outils de bureau** : clients GUI multiplateformes pour le flashage et les diagnostics (URTC-FLASHER, URTC-TESTER).
* **Outils de navigateur** : l'API Web Serial pour des tests matériels sans installation (URTC-WEB-STUDIO).
* **Données de cycle de vie** : piste d'audit non volatile par outil, partagée avec l'approche d'intégrité F-RAM propre à HYDRA-UMC.

## 🔒 Sécurité

Chaque profil d'outil possède son propre chien de garde (watchdog) et son comportement en cas de défaut, indépendamment de la couche E-STOP du contrôleur de cellule — un outil qui perd son budget temporel ou son battement de cœur (heartbeat) CAN se met de lui-même dans son état sûr déclaré, au lieu d'attendre une commande externe. Le préchauffage d'URTC-SMART-RACK est limité par les mêmes limites thermiques par outil déclarées par son profil, audité dans la même piste de cycle de vie qu'un atelier utilise pour décider si un outil est toujours apte au service.

## 📁 Catalogue des Projets URTC

|Dépôt|Version|Description|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.4.1|Micrologiciel du contrôleur d'outils robotiques universel pour plus de 25 outils spécialisés.|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.4.1|Outil graphique pour les mises à jour de micrologiciel CAN-OTA et SWD/JTAG pleine puce.|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.4.2|Outil de diagnostic pour la validation en temps réel des profils d'outils URTC sur CAN.|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.3.7|Outil Web Serial basé sur le navigateur pour les tests et analyses matériels instantanés.|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.2.1|Stockage d'outils intelligent avec préchauffage automatique et audit du cycle de vie.|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.5|Tête d'outil avec caméras thermique et RVB intégrées pour l'AQ active.|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.1.8|Détecte, installe et met à jour les dépôts URTC sur une machine à partir de leurs propres manifestes.|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.1.1|Architecture, interfaces, base de référence de sécurité, matrice de capacités, note d'étude du protocole CAN et catalogue de projets généré de l'écosystème URTC, plus les outils qui comparent tous les dépôts.|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.0.8|Le protocole CAN de la tête d'outil sous forme de données : une spécification, du code généré en C, TypeScript et Python, des vecteurs de conformité et les transports Python.|
|[URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY)|0.0.2|Passerelle devant le bus CAN d'URTC : liste d'identifiants autorisés, limite de débit et clé de session.|

\---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ARMOR_BANNER.svg" alt="Bannière de l'écosystème A.R.M.O.R." width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Dépôts publics">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Pile logicielle">
</p>

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range)** est un écosystème public distinct de sécurité périmétrique et de domotique — aucun lien avec HYDRA-UMC ou URTC si ce n'est le même auteur et les mêmes conventions d'ingénierie (manifestes versionnés, contrat de message partagé, interfaces en huit langues). Ses nœuds de terrain surveillent le périmètre d'une propriété ainsi que son installation solaire/électrique ; son serveur central et ses clients permettent à un opérateur de voir et d'agir sur ce qu'ils signalent. Les notes de version et de maturité ci-dessous proviennent directement du manifeste et de la matrice de capacités de chaque dépôt, selon la même convention d'honnêteté qu'utilise déjà le tableau de bord d'HYDRA-UMC.

**Outil de mise à jour :** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) détecte, installe et met à jour les dépôts de cet écosystème ; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) le fait pour les quatre.

<!-- progress:armor -->
`\[█████████████░░░░░░░] 65%` — Calculé à partir de données réelles : la maturité et la preuve que chacun de ses 18 dépôts déclare dans son propre manifeste. Le jalon de 100 % est un écosystème entièrement intégré fonctionnant sur du matériel réel.
<!-- /progress:armor -->

## 🏗️ Comment est construit A.R.M.O.R.

1. **Contrat partagé** : **ARMOR-COMMON** détient la signification des messages — schéma JSON, validateur Python et types TypeScript/Kotlin générés que tous les autres dépôts consomment sans jamais les redéfinir.
2. **Nœuds de terrain** : Micrologiciel ESP32-S3 pour la détection radar/présence (**ARMOR-RADAR**), la surveillance d'onduleur solaire et de batterie (**ARMOR-SOLAR**), la mesure électrique avec commutation (**ARMOR-ELECTRICAL**), et le panneau d'alarme de la maison (**ARMOR-ALARM**) ; un agent Python (**ARMOR-NETWORK**) surveille le réseau local de la maison et l'accessibilité à Internet à partir d'une machine qui y est connectée.
3. **Coordinateur central** : **ARMOR-SERVER** stocke l'état, les utilisateurs, les alarmes, les automatisations et les preuves vidéo des caméras ; **ARMOR-SERVER-AI** et **ARMOR-VOICE-AI** ajoutent une politique visuelle explicable et des intentions vocales hors ligne qui n'actionnent jamais rien par elles-mêmes.
4. **Clients opérateurs** : **ARMOR-STUDIO** (web) et **ARMOR-ANDROID-CONTROL** (mobile) sont des clients du serveur central, jamais du réseau de terrain directement. **ARMOR-HMI** est un panneau tactile mural (un Waveshare ESP32-S3-Touch-LCD-7C-BOX) qui affiche l'état, permet d'armer et d'acquitter, et hébergera l'assistant vocal.
5. **Déploiement et test** : **ARMOR-DEVOPS** déploie l'ensemble du graphe de services ; **ARMOR-SIMULATOR** rejoue des scénarios et des pannes reproductibles sans matériel réel ; **ARMOR-HARDWARE** regroupe la conception du boîtier et sa matrice de recette en atelier.
6. **Opérations de l'écosystème** : **ARMOR-UPDATER** découvre, installe et met à jour chaque dépôt A.R.M.O.R. sur une machine, selon la même conception atomique par vérification que HYDRA-UMC-UPDATER ; **ARMOR-DOCS** est la documentation d'architecture canonique et la matrice de capacités. **ARMOR-STUDIO** peut également mettre à jour les services sur la machine centrale à partir de paquets signés avec la clé de version de l'écosystème, en vérifiant chaque signature avant l'installation.

## 🔒 Honnêteté et Sécurité

A.R.M.O.R. suit la même règle que le tableau de bord d'HYDRA-UMC applique déjà : une affirmation n'est vraie que lorsqu'elle est vérifiée, et chaque dépôt indique clairement ce qui a été exécuté ou non sur du matériel réel. Rien dans cet écosystème ne contrôle actuellement le secteur électrique (mains) ou l'accès physique ; les nœuds de terrain observent et rapportent, et toute future capacité de commutation est conçue et examinée avant d'être activée.

## 📁 Catalogue des Projets A.R.M.O.R.

|Dépôt|Version|Description|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.7.7|Contrats de message, validateurs, vecteurs de conformité, types générés, OpenAPI, lanceur partagé.|
|[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)|0.8.0.5|Micrologiciel de nœud de terrain ESP32-S3, décodeurs pour capteurs de présence LD2450, LD2461, son cœur testé sur hôte, mises à jour depuis GitHub avec barre de progression et carte en direct.|
|[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)|0.5.9|Nœud de passerelle solaire : micrologiciel ESP32-S3 et son panneau (dix ports série), protocoles des onduleurs Voltronic / MPP Solar et batteries Pylontech et ANT-BMS.|
|[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)|0.5.0|Nœud électrique : micrologiciel (seize compteurs PZEM sur une ligne série, panneau web, MQTT), trames des compteurs, message des relevés réseau et règles de commutation.|
|[ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM)|0.4.8|Nœud et panneau d'alarme : micrologiciel (zones câblées, sirène, capteurs et sirènes Zigbee, panneau web en sept langues) et règles d'armement, délais, alarme et code PIN, testés sur ordinateur ; continue de surveiller et prend le contrôle de la radio Zigbee lorsque le serveur est absent. N'a jamais tournè sur une carte.|
|[ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI)|0.4.0|Panneau tactile pour Waveshare ESP32-S3-Touch-LCD-7C-BOX : état du système sur écran mural, armement/désarmement/acquittement, voix push-to-talk et page web d'un nœud ; le micrologiciel n'a jamais tourné sur une carte.|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.4|Moniteur de réseau local : appareils sur le réseau de la maison, état d'Internet (et de quel côté se situe une panne), changements ; observe uniquement.|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.8.0.6|État central (persistant), utilisateurs, historique des événements, alarmes, appareils, automatisations, lectures solaires et électriques, réseau local, services système, surveillance de caméras, caméras, preuves, audit, mises à jour de micrologiciel de nœud obligatoirement signées, notifications Telegram et Home Assistant, commandes vocales, et utilisation extérieure (second facteur, sessions pouvant être terminées, politique distante).|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.7|Service de surveillance de mouvement, sélection de profil visuel, politique de fusion explicable, registre de moteurs.|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.3|Zones de caméras, masques et règles de détection (rôdage, un événement par visite) ; aucun modèle de détecteur pour l'instant.|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.1|Service vocal hors ligne : quinze commandes en huit langues, tours de parole du panneau mural, armement et désarmement confirmés par jeton signé.|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.1.0|Console d'opérations, alarmes, appareils, automatisations, utilisateurs, historique, règles d'alerte, PTZ, carte radar, menus solaires et électriques, réseau local, services système, météo, recherche et configuration de nœud, mises à jour de micrologiciel de nœud, notifications, et concepteur de site 2D/3D.|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.7|Client opérateur Android : armement et désarmement, alarmes, appareils, radar en direct, onduleurs solaires et batteries, historique, notifications d'alarme, assistant pour commandes écrites et vocales et configurateur des nœuds.|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.6|Conceptions de boîtiers (boîtier d'angle radar ; boîte cochée pour les nœuds solaires, électriques et d'alarme) et matrice de recette en atelier.|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.7|Topologie Compose, installateur de banc de test pour serveur central, sauvegarde et restauration, profil TLS, courtier MQTT propre, services d'observation et vocaux, agent d'administration.|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.6|Scénarios et pannes reproductibles.|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.5|Détecte, installe et met à jour les propres dépôts de l'écosystème (atomique par vérification, aucun GITHUB\_TOKEN requis).|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.1.2|Documentation canonique et matrice de capacités.|

\---

# ⚡ EH3D FABRICATION SUITE

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/EH3D_BANNER.svg" alt="Bannière EH3D Fabrication Suite" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Desktop%20%7C%20Embedded-blue.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/Stack-C%2B%2B%20%7C%20Python%20%7C%20Qt-orange.svg" alt="Pile logicielle">
  <img src="https://img.shields.io/badge/Hardware-HYDRA--UMC%20%7C%20Bungard%20%7C%20ESP32-green.svg" alt="Matériel">
</p>

**EH3D Fabrication Suite** est un écosystème logiciel multi-dépôt dédié, conçu sur mesure pour le prototypage rapide de circuits imprimés (PCB), la préparation de trajectoires d'outils FAO, l'inspection par vision par ordinateur, la gestion Pick \& Place (PnP) et le contrôle CNC/Laser multi-machines. Il offre une interopérabilité native avec les nœuds matériels **HYDRA-UMC** (STM32H7 + Jetson Orin NX + NPU Hailo) ainsi qu'une flotte de machines d'atelier comprenant des systèmes de fraisage industriels (Bungard CCD via passerelles RS-232 ESP32-S3), des routeurs CNC (JuanenCNC) et des graveurs laser à diode (JuanenLaser).

**Outil de mise à jour :** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) détecte, installe et met à jour les dépôts de cet écosystème ; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) le fait pour les quatre.

<!-- progress:eh3d -->
`\[██░░░░░░░░░░░░░░░░░░] 10%` — Calculé à partir de données réelles : la maturité et la preuve que chacun de ses 8 dépôts déclare dans son propre manifeste. Le jalon de 100 % est un écosystème entièrement intégré fonctionnant sur du matériel réel.
<!-- /progress:eh3d -->

## 🏗️ Comment fonctionne EH3D Fabrication Suite

1. **Gestion centrale** : **EH3D-SUITE-LAUNCHER** découvre les nœuds matériels actifs sur le réseau local (passerelles HYDRA-UMC et ESP32), gère les paquets unifiés `.eh3dproj` et orchestre les mises à jour d'outils.
2. **Pipeline de traitement FAO** : Des outils CAO/FAO spécialisés gèrent les étapes de fabrication individuelles :

   * **EH3D-ISOCAM** : Isolation de pistes Gerber RS-274X/X2, algorithmes de Voronoï et enlèvement de cuivre résiduel (rubout).
   * **EH3D-DRILLPRO** : Traitement des perçages Excellon/NC Drill, tables de forets et cycles de perçage profond.
   * **EH3D-ROUTEPRO** : Fraisage de contours de cartes, création d'onglets de maintien (tabs) et stratégies d'entrée en rampe.
   * **EH3D-LASER-CAM** : Algorithmes de tramage (dithering) raster et modulation de puissance vectorielle pour la découpe laser.
   * **EH3D-STENCILCAM** : Traitement de masques de pâte (pastemask) pour la génération de pochoirs de pâte à braser CMS.
3. **Exécution et Contrôle en Temps Réel** : **EH3D-MOTIONCNC** pilote le mouvement des machines via un streaming G-Code/HP-GL haute vitesse, intégré avec **EH3D-AUTOLEVEL** pour le palpage topographique en Z et **EH3D-PENDANT-GUI** pour la mise à l'origine manuelle (G54/G55) et les déplacements (jogging).
4. **IA de Bord et Inspection** : **EH3D-VISION-STUDIO** exploite le NPU Hailo d'HYDRA-UMC pour effectuer l'alignement de caméras en temps réel, la détection automatique de repères (fiducials) et l'inspection de l'usure des outils.
5. **Assemblage et Données Auxiliaires** : **EH3D-PNP-MANAGER** gère les coordonnées centroïdes Pick \& Place et les chargeurs (feeders), tandis que **EH3D-TOOL-MANAGER** maintient une base de données d'outils unifiée à travers tous les modules FAO.

## 📁 Catalogue des Projets EH3D Fabrication Suite

### 💠 Contrôle central et clients opérateur
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|Tableau de bord principal de l'écosystème pour la gestion de projets (.eh3dproj), les mises à jour, les paramètres globaux et la découverte de nœuds.|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.1|Schémas de données, spécifications de projets unifiés (.eh3dproj), constantes globales et actifs graphiques d'IU.|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.1|Documentation de l'écosystème, guides d'assemblage, spécifications techniques des passerelles et manuels d'intégration.|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.1|Bibliothèque C++/Python partagée contenant les analyseurs (parsers) Gerber/Excellon/G-Code/HP-GL, la géométrie 2D/3D et les protocoles.|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.1|Détecte, installe et met à jour les propres dépôts de l'écosystème (atomique par vérification, aucun GITHUB\_TOKEN requis).|
|[EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER)|0.0.1|Serveur en Rust avec interface REST et websocket : utilisateurs, machines et travaux, planification des travaux de perçage et de fraisage avec les bibliothèques de DRILLPRO et ROUTEPRO, un travail à la fois par machine.|
|[EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)|0.0.1|Client web en Rust pour EH3D-SERVER.|

### 💠 Projets de perçage, détourage et fraisage :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.2|Application FAO Excellon/NC Drill, gestion des forets, optimisation de trajectoire et cycles de perçage profond.|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.2|Application FAO de fraisage de contours de cartes, alésage de cavités (pocketing), onglets de maintien et stratégies d'entrée en rampe CNC.|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.1|GUI de commande numérique en temps réel, visualiseur de G-code 3D, palpage et support de streaming multi-machine.|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|Base de données de cribles d'outils partagée suivant les heures d'usure, les préréglages de coupe et les avances sur tous les outils FAO EH3D.|

### 💠 Projets laser :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|Application FAO laser pour le tramage d'images, la conversion raster/vecteur et le contrôle de puissance PWM dynamique.|

### 💠 Projets FAO :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|Application de traitement FAO Gerber RS-274X/X2, isolation de pistes Voronoï/Offset, rubout et simulation de gravure.|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|Simulateur de trajectoire d'outils et d'enlèvement de matière 3D, détecteur de collisions et estimateur de temps de cycle G-Code/HP-GL.|

### 💠 Projets Gerber :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|Outil d'inspection FAO léger pour l'alignement des couches Gerber et la visualisation rapide.|

### 💠 Projets Pick&Place :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|Utilitaire de conversion de masque de pâte générant des trajectoires de découpe pour la fabrication de pochoirs CMS par laser et traceur.|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|Gestionnaire d'assemblage CMS inspiré d'OpenPnP, lecteur de centroïdes, contrôle de chargeur et centrage de composants par vision.|

### 💠 Projets de nœuds :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)|0.0.2|Nœud ESP32-S3 pour le boîtier d'une machine Bungard CCD : le RS-232 de son unité de commande par Ethernet ou Wi-Fi, avec les lampes de la machine et le variateur de la broche sur la même carte.|
|[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)|0.0.1|Contrôleur manuel tactile 10 pouces / mobile à base d'ESP32-P4/ESP32-C6 pour le jog en temps réel, la mise à zéro (G54/G55) et l'arrêt d'urgence des machines Bungard CCD.|
|[EH3D-NODE-HMI-GUI](https://github.com/JuanenRac/EH3D-NODE-HMI-GUI)|0.0.1|Contrôleur manuel tactile 10 pouces / mobile polyvalent à base d'ESP32-P4/ESP32-C6 pour le jog en temps réel, la mise à zéro (G54/G55) et l'arrêt d'urgence.|

### 💠 Projets FENIX :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-FENIX-PCB](https://github.com/JuanenRac/EH3D-FENIX-PCB)|0.0.1|Environnement EDA : saisie de schémas, routage de circuits imprimés, outils de vérification, simulation de circuits et modules spécialisés pour les alimentations à découpage (SMPS) et la RF.|
|[EH3D-FENIX-CAD](https://github.com/JuanenRac/EH3D-FENIX-CAD)|0.0.1|CAO mécanique paramétrique dédiée à la conception de boîtiers, de châssis et de dissipateurs thermiques.|
|[EH3D-DESIGN-VERIFIER](https://github.com/JuanenRac/EH3D-DESIGN-VERIFIER)|0.0.1|Vérificateur d'ingénierie complet pour les validations croisées et le contrôle qualité de la conception.|
|[EH3D-VALIDATION-LAB](https://github.com/JuanenRac/EH3D-VALIDATION-LAB)|0.0.1|Environnement de test chargé de gérer les cas d'usage de référence et les tests de régression du système.|
|[EH3D-DESIGN-HISTORY](https://github.com/JuanenRac/EH3D-DESIGN-HISTORY)|0.0.1|Système de contrôle de version qui conserve l'historique sémantique et l'évolution logique de la conception.|
|[EH3D-PROJECT-PASSPORT](https://github.com/JuanenRac/EH3D-PROJECT-PASSPORT)|0.0.1|Générateur du passeport technique stockable et reproductible pour l'audit complet d'un projet.|
|[EH3D-COMPONENT-INTELLIGENCE](https://github.com/JuanenRac/EH3D-COMPONENT-INTELLIGENCE)|0.0.1|Base de données technique avancée enrichie de métadonnées sur les composants électroniques.|
|[EH3D-MANUFACTURING-PROFILE](https://github.com/JuanenRac/EH3D-MANUFACTURING-PROFILE)|0.0.1|Gestionnaire de profils des capacités des machines de chaque usine et des contraintes techniques des fournisseurs.|
|[EH3D-THERMAL-LAB](https://github.com/JuanenRac/EH3D-THERMAL-LAB)|0.0.1|Laboratoire de simulation thermique progressive directement couplé à la conception physique.|
|[EH3D-LAB-BRIDGE](https://github.com/JuanenRac/EH3D-LAB-BRIDGE)|0.0.1|Module de corrélation servant de pont direct entre les données de simulation et les mesures réelles de laboratoire.|
|[EH3D-DESIGN-EXPLORER](https://github.com/JuanenRac/EH3D-DESIGN-EXPLORER)|0.0.1|Environnement d'exploration pour comparer et analyser les alternatives ou les branches d'une conception.|

### 💠 Projets ANDROID/IOS :
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-ANDROID-CONTROL](https://github.com/JuanenRac/EH3D-ANDROID-CONTROL)|0.0.1|Application Android cliente d'EH3D-SERVER.|
|[EH3D-IOS-CONTROL](https://github.com/JuanenRac/EH3D-IOS-CONTROL)|0.0.1|Application iOS cliente d'EH3D-SERVER.|

### 🛠️ Outils complémentaires
|Dépôt|Version|Description|
|-|-|-|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|Tableau de bord de vision IA de bord pour l'alignement de caméras, l'apprentissage de repères fiduciels et l'inspection visuelle via HYDRA-UMC.|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|Processeur de maillage de hauteur topographique (palpage Z) et interpolation de G-code pour la compensation de surface.|

\---

## 🤝 Contribution

Chaque écosystème est une initiative indépendante avec ses propres projets. Chaque projet possède ses propres directives de contribution. Veuillez vous référer aux dépôts individuels pour les détails techniques.

Les étiquettes (labels) d'issues sont standardisées sur l'ensemble des dépôts HYDRA-UMC à partir du fichier [`.github/labels.yml`](.github/labels.yml) situé dans ce même dépôt, synchronisé par [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) — modifiez ce fichier unique pour modifier une étiquette partout à la fois, plutôt que manuellement dépôt par dépôt. Contrairement au tableau de bord ci-dessous, cette liste est statique (une véritable matrice GitHub Actions, et non une découverte dynamique) — un nouveau dépôt ajouté nécessite également une entrée ici, et pas seulement un véritable fichier `hydra-umc.project.json`.

Un tableau de bord d'état en direct couvrant chaque dépôt public des quatre écosystèmes — chacun découvert par son propre manifeste (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`, plus `electro-hobby-3d.project.json` pour les dépôts inter-écosystèmes), lu directement à partir de la branche par défaut de chaque dépôt sans liste fixe — est régénéré par [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) immédiatement lors d'un push sur un projet (via le `dashboard-dispatch.yml` propre à chaque dépôt) et, par mesure de sécurité, deux fois par an/heure, et servi depuis `docs/` via GitHub Pages : [**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/). Il indique la pile logicielle, la cible de déploiement et la version actuelle, une véritable classification de maturité par projet (scaffolding / functional / established / production, déterminée à partir du CHANGELOG de chaque projet — voir [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)), son rôle (API / UI / CLI / firmware / bibliothèque / service / outil), un arbre de famille parent-enfant et des notes par projet sur ce qui est implémenté aujourd'hui. Le fichier [`ecosystem-catalog.json`](ecosystem-catalog.json) répertorie ces écosystèmes et leurs manifestes en un seul endroit, et la construction du tableau de bord refuse de s'exécuter si les deux sont en désaccord.

## 🧭 Collaboration sur GitHub

Le [modèle de collaboration GitHub](docs/GITHUB_COLLABORATION.md) définit un Wiki central, un Projet d'écosystème, la portée des Discussions, les critères de sortie (release) et la limite d'automatisation partagée. Les formulaires d'issues gérés de manière centralisée ([`issuetemplate`](.github/ISSUE_TEMPLATE/)) et le modèle de pull-request ([`PULL\_REQUEST\_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)) permettent de rendre le travail logiciel, de validation matérielle et de documentation traçable sans dupliquer les manuels de projets.

Le workflow de santé de la communauté est intentionnellement manuel et en mode "dry-run" (simulation) par défaut. Une fois que `COMMUNITY\_HEALTH\_SYNC\_TOKEN` est configuré, il peut copier uniquement ces modèles gérés vers chaque dépôt publiant un manifeste HYDRA-UMC ; il ne supprime jamais un modèle spécifique à un projet.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licence GPL-3.0.

