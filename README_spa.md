<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner del Ecosistema HYDRA-UMC" width="100%">
</p>

# Ecosistema HYDRA-UMC / URTC 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  🇪🇸 <b>Español</b> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Licencia-GPL%203.0-blue.svg" alt="Licencia GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Plataforma-STM32%20%7C%20CM5-red.svg" alt="Plataforma">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Poder de IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenido al **Ecosistema HYDRA-UMC**, una plataforma de robótica industrial de múltiples capas que abarca desde firmware en tiempo real de bajo nivel hasta IA cognitiva de alto nivel. Esta organización alberga 44 proyectos especializados diseñados para trabajar en perfecta sincronía para la automatización de micro-fábricas y robótica de enjambre.

---

## 🏗️ Arquitectura del Ecosistema

El ecosistema está estructurado en 6 capas funcionales que permiten operaciones robóticas autónomas, colaborativas e inteligentes:

1.  **Capa de Ejecución**: Firmware basado en STM32 (H745/G474) para precisión submilimétrica y actuación FDCAN de alta velocidad.
2.  **Capa de Inteligencia**: IA de borde potenciada por **Hailo-8** (percepción de reflejos) y **Hailo-10** (razonamiento cognitivo).
3.  **Capa de Coordinación**: Backends independientes en Node.js y orquestadores de enjambre distribuidos.
4.  **Capa de Interfaz**: Paneles de control web (React), escritorio (Qt6), móvil (Kotlin/Flutter) y táctiles DSI.
5.  **Capa Virtual**: Motores de Gemelo Digital de alta fidelidad (Rust/Bevy) para validación previa a lo físico.
6.  **Capa de Soporte**: Pasarelas de Industria 4.0 (OPC-UA/MQTT) y mantenimiento predictivo Big Data.

---

## 🛠️ Stack Tecnológico y Herramientas

El ecosistema aprovecha un stack moderno y de alto rendimiento para una fiabilidad de misión crítica:

### 💠 Embebido y Tiempo Real (Ejecución)
- **Microcontroladores**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Frameworks**: FreeRTOS (modo AMP), CMSIS-DSP, STM32 HAL/LL.
- **Protocolos**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (IPC esclavo de 50MHz), I2C, UART.
- **Cinemática**: Generación de perfiles de curva S, cinemática inversa (IK) en tiempo real.

### 🧠 IA de Borde y Percepción (Inteligencia)
- **Aceleradores**: Hailo-8 (26 TOPS) para visión de 8 cámaras, Hailo-10 (40 TOPS) para GenAI.
- **Modelos**: YOLOv10 (detección), OpenVLA (acción), Whisper (voz), Llama-3 (razonamiento).
- **Inter-nodo**: gRPC sobre Protobuf e intercambio de metadatos SPI-DMA de alta velocidad.

### 🌐 Backend y Coordinación (Coordinación)
- **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orquestador), Go (CLI).
- **Infraestructura**: Express, Fastify, Socket.io (WebSocket), gRPC.
- **Base de Datos**: InfluxDB/TimescaleDB (Telemetría), Redis (Estado), SQLite.

### 💻 Paneles e Interfaz de Usuario (Interfaz)
- **Web**: React 19, Vite, Three.js (Visor 3D), Tailwind CSS.
- **Nativo**: Python 3.12/PySide6 (Suite), Kotlin (Android Nativo), Flutter 3.x (iOS y DSI).

---

## 📋 Requisitos del Sistema

- **Nodo de Cómputo**: Raspberry Pi CM5 (4GB+ RAM) con almacenamiento NVMe/eMMC.
- **Hardware de IA**: Módulos M.2 Hailo-8/Hailo-10 (Llave M).
- **Bus de Campo**: Gigabit Ethernet para LAN y FDCAN (ISO 11898-1:2015) para actuadores.
- **SO de Cliente**: Android 10+, iOS 15+, Windows 10/11 (Alta Densidad), Ubuntu 22.04 LTS.

---

## 🔒 Seguridad Industrial

- **Capa E-STOP**: Línea de emergencia cableada + Tramas de emergencia CAN de alta prioridad (<1ms).
- **Seguridad por IA**: Zonas de Seguridad 3D con corte automático de par motor ante intrusión humana.
- **Ciberseguridad**: Autenticación apátrida basada en JWT + mTLS para tráfico seguro inter-nodo.
- **Integridad**: F-RAM no volátil para auditoría de ciclo de vida de herramientas y recuperación de estado.

---

## 🤝 Contribuir
Este ecosistema es parte de una iniciativa robótica de alta tecnología. Cada proyecto tiene sus propias pautas de contribución. Consulte los repositorios individuales para detalles técnicos.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licencia GPL-3.0.
