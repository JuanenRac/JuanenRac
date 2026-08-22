<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Bannière de l'écosystème HYDRA-UMC" width="100%">
</p>

# Écosystème HYDRA-UMC / URTC 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  🇫🇷 <b>Français</b> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Licence-GPL%203.0-blue.svg" alt="Licence GPL 3.0">
  <img src="https://img.shields.io/badge/Matériel-CERN%20OHL--S-orange.svg" alt="Matériel CERN OHL">
  <img src="https://img.shields.io/badge/Plateforme-STM32%20%7C%20CM5-red.svg" alt="Plateforme">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Puissance IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenue dans l'**Écosystème HYDRA-UMC**, une plateforme robotique industrielle multicouche allant du micrologiciel temps réel de bas niveau à l'IA cognitive de haut niveau. Cette organisation héberge 44 projets spécialisés conçus pour travailler en parfaite synchronie pour l'automatisation de micro-usines et la robotique en essaim.

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

## 🤝 Contribuer
Cet écosystème fait partie d'une initiative robotique de haute technologie. Chaque projet a ses propres directives de contribution. Veuillez vous référer aux dépôts individuels pour les détails techniques.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licence GPL-3.0.
