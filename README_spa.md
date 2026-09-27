<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Banner de Electro Hobby 3D" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  🇪🇸 <b>Español</b> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Licencia-GPL%203.0-blue.svg" alt="Licencia GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosistemas-3-00E5FF.svg" alt="Tres ecosistemas">
</p>

Tres ecosistemas de ingeniería independientes, un mismo autor. **HYDRA-UMC** es una plataforma de robótica industrial de múltiples capas, desde firmware en tiempo real hasta IA cognitiva. **URTC** es su subsistema universal de herramientas robóticas: firmware en tiempo real y herramientas de escritorio/web para el efector final de un robot, desarrollado como producto propio con versión y mantenimiento independientes. **A.R.M.O.R.** es un ecosistema aparte, privado, de seguridad perimetral y automatización del hogar - detección de presencia por radar, monitorización solar y eléctrica, y un coordinador central con clientes web y móvil.

---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner del Ecosistema HYDRA-UMC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-STM32%20%7C%20CM5-red.svg" alt="Plataforma">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Poder de IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenido al **Ecosistema HYDRA-UMC**, una plataforma de robótica industrial de múltiples capas que abarca desde firmware en tiempo real de bajo nivel hasta IA cognitiva de alto nivel. Esta organización alberga numerosos proyectos especializados diseñados para trabajar en perfecta sincronía para la automatización de micro-fábricas y robótica de enjambre.

## 📈 Progreso del Ecosistema

`[██████████▊░░░░░░░░░] 54%` — Referencia orientativa. El 100% representa el ecosistema integrado funcionando sobre hardware real.

> [!IMPORTANT]
> 🛠️ **Proyecto en pausa — construyendo el hardware real.** El desarrollo activo está detenido mientras se construye de verdad la célula física (bastidores, cableado, las placas CM5 y STM32 reales), para que la siguiente fase de trabajo tenga hardware real sobre el que correr y validar, no solo una barra que sube. El trabajo se retoma en cuanto esa construcción esté lista.

---

## 🚀 Características Clave y Escalabilidad

- **Escalabilidad Multi-Robot**: Soporta hasta 8 unidades robóticas distribuidas (actualmente de 3, 4, 5 y 6 ejes; escalable a 7, 8, 9 ejes y arquitecturas de robots duales en futuras versiones).
- **Etapa Local Integrada**: La placa principal HYDRA-UMC cuenta con una **Etapa Local de 6 ejes** integrada para tareas auxiliares, incluyendo robots secundarios, revólveres ATC (Cambiador Automático de Herramientas), sincronización de cintas transportadoras o pórticos de tablas XYZ.

---

## 🏗️ Arquitectura del Ecosistema

El ecosistema v1.1 es una plataforma de producto por capas: se apoya en tecnologías Linux y Raspberry Pi consolidadas, sin crear un sistema operativo nuevo ni sustituir las API de los fabricantes.

1.  **Base de plataforma**: Raspberry Pi OS ARM64 y los servicios Linux estándar proporcionan la base compatible para CM5.
2.  **Plataforma y contratos**: **HYDRA-UMC-OS** empaqueta perfiles reproducibles, servicios, diagnóstico y actualizaciones sobre Raspberry Pi OS; **HYDRA-UMC-SDK** publica contratos versionados, clientes ligeros y pruebas de conformidad.
3.  **Ejecución en tiempo real**: el firmware **HYDRA-UMC** mantiene los límites de movimiento, watchdogs y parada segura sobre STM32/MCU; la herramienta en sí, y su propia autoridad en tiempo real sobre el efector final, pertenece al ecosistema **URTC**, aparte, más abajo.
4.  **Coordinación y operaciones**: los servicios de servidor, despacho de trabajos, telemetría y configuración coordinan dispositivos sin saltarse el límite de seguridad del MCU.
5.  **Interfaces de operador**: Studio, Suite, DSI, web, escritorio, móvil y CLI consumen los contratos del SDK.
6.  **Percepción e inteligencia**: visión, Hailo y servicios cognitivos proponen observaciones o planes; no tienen autoridad de seguridad física.
7.  **Ingeniería, industria y datos**: Gemelo Digital, HIL/física, pasarelas OPC-UA/MQTT/MTConnect y datos validan e integran el sistema.

Para desarrollar, se parte de la arquitectura y el modelo de servicios públicos de **HYDRA-UMC-OS** y se usan los contratos y reglas de conformidad de **HYDRA-UMC-SDK**. La autoridad de seguridad del MCU se conserva en todos los flujos.

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
- **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orchestrator), Go (CLI).
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

## 🔧 Hacking de Hardware: Construye tu Propio Carrier

La placa Robot Controller Board se construye sobre un **Raspberry Pi CM5**, y el propio conector doble Hirose DF40 de la CM5 tiene un pinout fijo, oficial y público (Tabla 5 de la hoja de datos oficial de la CM5 de Raspberry Pi) - no es algo que este proyecto defina. Eso significa que un carrier compatible de terceros es un proyecto real y alcanzable, no un ejercicio de ingeniería inversa:

- **Empieza aquí**: [`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - qué pines fijos de la CM5 usa realmente esta placa (Ethernet, los 2 PHY USB3 SuperSpeed nativos, el conector de ventilador de refrigeración del lado CM5) y por qué, reorganizado por función a partir de la tabla oficial de pinout.
- **La vía fácil**: el **header GPIO estándar de 40 pines de Raspberry Pi** (el mismo layout "B+" sin cambios desde 2014) está expuesto en esta placa exactamente igual que en cualquier Raspberry Pi - los HATs y herramientas GPIO existentes funcionan sin modificar. Un puñado de posiciones que el propio enlace STM32 de esta placa ya usa están serigrafiadas/anotadas para saber cuáles evitar.
- **Yendo más lejos**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) cubre cómo se comunican realmente entre sí la CM5, el "Cerebro Cinemático" STM32H745 y el "Robot Controller" STM32G474 (SPI1 + FDCAN1 + el buzón IPC CM7↔CM4) - la capa que un rediseño de carrier necesitaría preservar si quiere seguir siendo compatible con el firmware propio de este proyecto.
- Cada documento de pinout indica claramente si es **CONFIRMADO** (tomado directamente de una tabla de hoja de datos oficial) o **PROPUESTO** (una elección de enrutado propia de este proyecto, abierta a ser distinta en un carrier derivado) - lee esa línea de estado antes de tratar una asignación de señal como fija.

Esto no es un tutorial guiado (no hay un único carrier "correcto" para cada caso de uso) - es el material de referencia real que un diseñador de hardware experimentado necesita para partir de un mapa de pines ya verificado en vez de solo una hoja de datos.

---

## 📁 Catálogo de Proyectos HYDRA-UMC

¿Nuevo en el ecosistema? `./starter-kit.sh` (o `starter-kit.bat` en
Windows) clona 13 repositorios core - un conjunto inicial seleccionado a
mano, no el catálogo completo de abajo - como carpetas hermanas en un
mismo directorio: la disposición estándar que ya asume cualquier script
entre repositorios de aquí. Volver a ejecutarlo es seguro: lo que ya
esté clonado se deja intacto. A partir de ahí,
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
(uno de los 13 recién clonados) puede comprobar versiones y
compilar/actualizar cualquiera de los demás proyectos del catálogo
completo de abajo.

### 🧱 Base de plataforma y contratos
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.4.7 | Capa de plataforma Raspberry Pi OS para CM5: perfiles reproducibles, configuración, diagnóstico, ciclo de servicios y actualizaciones; no es una distribución Linux nueva. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.2.8 | Contratos versionados, clientes ligeros y pruebas de conformidad compartidos para servicios, interfaces y adaptadores CM5; no sustituye API de fabricantes. |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.0 | Registro declarativo y validador de manifiestos de adaptador para conectores de máquinas externas; extiende la propia idea de contrato del SDK a máquinas externas sin sustituir a los proyectos de pasarela industrial. |

### 💠 Control core e interfaces de operador
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.1.6 | Firmware de control de movimiento core para STM32H745/G474 con cinemática S-Curve. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.0.5 | API Node.js headless y backend WebSocket para orquestación robótica. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.7.5 | Dashboard web avanzado basado en React para monitoreo y control 3D. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.3 | Aplicación de escritorio Python/Qt de alto rendimiento para automatización industrial. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.0 | Interfaz táctil basada en Flutter para pantallas industriales de 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.6.2 | App móvil nativa Kotlin con login biométrico para gestión remota. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.1.9 | App móvil Flutter para iOS/iPadOS con sincronización WebSocket en tiempo real. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.0 | Editor gráfico de URDF para validar y subir modelos de robots al catálogo. |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.2 | Editor de escritorio de modelos STL - transforma, reemplaza, quita y añade piezas reales en el catálogo de modelos compartido. |

### 👁️ Nodo de IA de Visión (Optimizado para Hailo-8)
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.0 | Nodo de percepción de alta velocidad para 8 flujos simultáneos de cámaras USB 3.0. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.1.6 | Pipeline optimizado de GStreamer/MediaMTX para retransmisión de video industrial. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.0.9 | Librería de modelos YOLO acelerados por hardware para QA de componentes y SMD. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.1 | Detección de intrusiones por IA en tiempo real para protección del volumen de trabajo. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.4 | Feedback cinemático basado en imagen para corrección de pose submilimétrica. |

### 🧠 Nodo de IA Cognitiva (Optimizado para Hailo-10)
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.1 | Nodo de razonamiento semántico para planificación lógica de misiones y control por voz. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.4 | Implementación del modelo Vision-Language-Action para ejecución de tareas complejas. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.3 | Pipeline local y privado de STT/TTS para interacción natural con el operador. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.0 | Orquestador de misiones basado en LLM con recuperación de errores sensible al contexto. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.0 | Asistente de IA basado en RAG entrenado con manuales técnicos y código fuente. |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.2 | Técnico de IA local con permisos controlados por política: hoy una política fija de niveles de riesgo y una lista blanca de herramientas, con una defensa real y probada que demuestra que un documento malicioso recuperado nunca puede disparar una llamada a herramienta ni filtrar un secreto - la IA nunca obtiene autoridad generando una respuesta. |

### 🐝 Orquestación y Enjambre
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.3 | Gestor de flota para coordinación multi-robot y prevención de colisiones. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.1 | Sincronización PTP para coordinación de robots con precisión de nanosegundos. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.0.7 | Optimizador de trayectorias distribuido para enjambres en espacios compartidos. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.1.8 | Programador de tareas basado en prioridades para flotas heterogéneas. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.4 | Monitor de alta disponibilidad con failover transparente de misiones. |

### 🎮 Gemelo Digital y Simulación
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.7 | Motor de simulación física de alta fidelidad para pruebas sin riesgo. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.6 | Simulación física real (MuJoCo/PhysX) de cadenas cinemáticas URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.6 | Interfaz Hardware-in-the-loop para consistencia entre estado real y virtual. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.0.8 | Generador de datasets procedimentales para entrenar modelos de IA de visión. |

### 📊 Datos y Analítica
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.3 | Almacenamiento Big Data para telemetría industrial masiva multi-robot. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.4 | Ingestor de alto rendimiento para logs de CAN, WebSocket y sistema. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.3 | Motor de mantenimiento predictivo basado en firmas de vibración de motores. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.2 | Generación automática de OEE y KPIs para gestión de planta industrial. |

### 🏭 Pasarela Industrial
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.2 | Puente de interoperabilidad para estándares de fábrica (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.5 | Mapeo de objetos robóticos HydraState a nodos estándar OPC-UA. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.2 | Puente de telemetría para integraciones IoT y dashboards externos. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.4 | Interfaz estandarizada para monitoreo de salud de máquinas y robots. |

### 🌉 Puentes de Automatización Externa
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.0.7 | Límite de coordinación bidireccional ROS 2: topics para observación, servicios para inspección y acciones cancelables para trabajos de celda. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.4 | Coordinador trazable de entrega de PCB para OpenPnP y carga o descarga asistida por robots. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.3 | Puente seguro alrededor de software de impresión 3D; el primer adaptador valida Moonraker sin sustituir firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.4 | Coordinador de auxiliares de celda CNC; la trayectoria y la seguridad siguen siendo nativas del controlador. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.2 | Coordinador de auxiliares de celda láser que no puede armar, disparar ni anular interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.0.8 | Límite de coordinación para droides con patas/humanoides: vocabulario de acciones caminar/coger/soltar filtrado por el contrato de seguridad compartido; la marcha y el equilibrio siguen siendo del propio controlador del droide. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.0.8 | Límite de coordinación para flotas AGV/AMR: transformación de la trama de fábrica a la trama local más un vocabulario de órdenes inspirado en VDA-5050; la planificación de rutas sigue siendo de la propia navegación del AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.0.9 | Límite de coordinación para UAV con cámara: vocabulario de solicitudes de vuelo con nombre más un watchdog determinista de heartbeat/pérdida de enlace. |

### 🛠️ Herramientas Complementarias
| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.2 | Dashboard de emergencia wearable con alertas de seguridad hápticas. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.2 | Interfaz de línea de comandos para automatización de flota, flasheo y devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.1 | Extensión de IA para dashboards web que ofrece insights en lenguaje natural. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.3 | Herramienta multiplataforma GUI/CLI para detectar, instalar y actualizar a mano cada proyecto del ecosistema. |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.2.7 | Herramienta de escritorio Windows/Linux que construye una imagen de la CM5 lista para grabar, precargada con las versiones más actuales del ecosistema, con configuración de primer arranque al estilo de Raspberry Pi Imager. |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.4 | Coordinador de incidencias de mantenimiento: un rol edge de bajo privilegio recopila un snapshot de inventario/salud saneado, un rol control-plane lo renderiza de solo lectura y pide a un proveedor de IA que sugiera un diagnóstico - nunca aplica un parche ni despliega nada. |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.3 | Servidor de desarrollo reproducible: hoy un esquema de configuración con permisos y un inventario de manifiestos, creciendo hacia un ejecutor de tareas/workspace aislado coordinado con OPS-AGENT - ninguna tarea tiene permiso de despliegue salvo que un documento lo conceda explícitamente. |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="Banner del Ecosistema URTC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-STM32-red.svg" alt="Plataforma">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Herramientas-25%2B%20perfiles-blueviolet.svg" alt="Herramientas">
</p>

**URTC (Universal Robot Tool Controller)** es un producto propio, no una carpeta subsistema de HYDRA-UMC: firmware en tiempo real y una familia de herramientas de escritorio/web para el efector final de un robot, desarrollado, versionado y mantenido de forma independiente. Un cambiador de herramientas equipado con URTC se coordina con el controlador de celda de HYDRA-UMC por FDCAN, pero el comportamiento en tiempo real de la propia herramienta, su watchdog y su estado seguro son autoridad propia de URTC - el controlador de celda no puede saltárselo, y URTC no depende de HYDRA-UMC para ser desarrollado, grabado o diagnosticado.

## 🏗️ Cómo Funciona URTC

1. **Firmware de herramienta**: el propio firmware STM32 de URTC ejecuta cada uno de más de 25 perfiles de herramienta especializados (pinzas, dosificadores, sondas, husillos y más), cada uno con su propio tiempo, límites y comportamiento ante fallos.
2. **Actualización en campo**: CAN-OTA envía una nueva imagen de firmware por el mismo bus CAN que ya usa la herramienta, con una vía completa por chip SWD/JTAG (URTC-FLASHER) como respaldo que nunca depende de que el firmware propio de la herramienta esté vivo.
3. **Diagnóstico en vivo**: URTC-TESTER valida el comportamiento CAN en tiempo real de una herramienta frente a su perfil declarado sin necesitar un taller completo; URTC-WEB-STUDIO hace lo mismo desde una pestaña del navegador por Web Serial, sin nada que instalar.
4. **Almacenamiento y ciclo de vida**: URTC-SMART-RACK guarda las herramientas entre trabajos, precalienta una antes de un cambio y mantiene un registro de auditoría de ciclo de vida (ciclos, fallos, última calibración) por herramienta física, no por tipo de herramienta.
5. **QA activo**: URTC-VISION-TOOL es en sí misma una herramienta - un cabezal con sus propias cámaras térmica y RGB para inspección de calidad durante el proceso, no una cámara externa atornillada a otra herramienta.

## 🛠️ Stack Tecnológico

- **Firmware**: STM32, FDCAN (bus compartido con el controlador de celda), CAN-OTA, respaldo SWD/JTAG.
- **Herramientas de escritorio**: clientes GUI multiplataforma para grabar y diagnosticar (URTC-FLASHER, URTC-TESTER).
- **Herramientas de navegador**: la API Web Serial para pruebas de hardware sin instalar nada (URTC-WEB-STUDIO).
- **Datos de ciclo de vida**: registro de auditoría no volátil por herramienta, con el mismo criterio de integridad F-RAM que usa HYDRA-UMC.

## 🔒 Seguridad

Cada perfil de herramienta lleva su propio watchdog y comportamiento ante fallos, independiente de la propia capa E-STOP del controlador de celda - una herramienta que pierde su propio margen de tiempo o el heartbeat CAN va a su estado seguro declarado por sí sola, en vez de esperar una orden externa. El precalentamiento de URTC-SMART-RACK está acotado por los mismos límites térmicos por herramienta que declara su perfil, auditados en el mismo registro de ciclo de vida que un taller usa para decidir si una herramienta sigue apta para servicio.

## 📁 Catálogo de Proyectos URTC

| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.1 | Firmware de controlador de herramientas universal para más de 25 herramientas especializadas. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.2.1 | Herramienta GUI para actualizaciones de firmware CAN-OTA y SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.2.2 | Herramienta de diagnóstico CAN-bus con paneles de telemetría por herramienta. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.2.2 | Herramienta Web Serial para pruebas y análisis instantáneo de hardware. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.0 | Almacenamiento inteligente de herramientas con precalentamiento y auditoría. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.0.5 | Cabezal con cámaras térmicas y RGB integradas para QA activo. |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="Banner del Ecosistema A.R.M.O.R." width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibilidad-Privado-lightgrey.svg" alt="Repositorios privados">
  <img src="https://img.shields.io/badge/Plataforma-ESP32--S3%20%7C%20Jetson-red.svg" alt="Plataforma">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar & Multimodal Observation Range)** es un ecosistema aparte, privado, de seguridad perimetral y automatización del hogar - sin relación con HYDRA-UMC ni URTC más allá del mismo autor y las mismas convenciones de ingeniería (manifiestos versionados, un contrato de mensajes compartido, interfaces en siete idiomas). Sus nodos de campo vigilan el perímetro de una propiedad y su instalación solar/eléctrica; su servidor central y sus clientes permiten a un operador ver y actuar sobre lo que reportan. Cada repositorio listado aquí es **privado**: los enlaces de abajo necesitan el acceso propio de la cuenta para abrirse, y las notas de versión y madurez salen directamente del manifiesto y la matriz de capacidades de cada repositorio, la misma convención de honestidad que ya usa el dashboard de HYDRA-UMC.

## 🏗️ Cómo Está Construido A.R.M.O.R.

1. **Contrato compartido**: **ARMOR-COMMON** es dueño del significado de los mensajes - JSON Schema, un validador en Python y tipos TypeScript/Kotlin generados que cada otro repositorio consume, nunca redefine.
2. **Nodos de campo**: firmware ESP32-S3 para detección por radar/presencia (**ARMOR-RADAR**), monitorización de inversores y baterías solares (**ARMOR-SOLAR**), y medición eléctrica con maniobra (**ARMOR-ELECTRICAL**); un agente en Python (**ARMOR-NETWORK**) vigila la propia red local de la casa y si hay internet desde una máquina ya conectada a ella.
3. **Coordinador central**: **ARMOR-SERVER** guarda el estado, usuarios, alarmas, automatizaciones y evidencia de cámaras; **ARMOR-SERVER-AI** y **ARMOR-VOICE-AI** añaden una política visual explicable e intenciones de voz sin conexión que nunca actúan por sí solas.
4. **Clientes de operador**: **ARMOR-STUDIO** (web) y **ARMOR-ANDROID-CONTROL** (móvil) son clientes del servidor central, nunca de la red de campo directamente.
5. **Despliegue y pruebas**: **ARMOR-DEVOPS** despliega todo el grafo de servicios; **ARMOR-SIMULATOR** reproduce escenarios y fallos repetibles sin hardware real; **ARMOR-HARDWARE** lleva el diseño de las cajas y su matriz de aceptación en banco.
6. **Operación del ecosistema**: **ARMOR-UPDATER** descubre, instala y actualiza cada repositorio de A.R.M.O.R. en una máquina, el mismo diseño atómico-por-verificación que HYDRA-UMC-UPDATER, adaptado para un ecosistema privado; **ARMOR-DOCS** es la documentación de arquitectura canónica y la matriz de capacidades.

## 🔒 Honestidad y Seguridad

A.R.M.O.R. sigue la misma regla que ya aplica el propio dashboard de HYDRA-UMC: una afirmación solo es real cuando está verificada, y cada repositorio dice con claridad qué se ha probado ya en hardware real y qué no. Nada en este ecosistema controla hoy la corriente eléctrica de la red ni el acceso físico; los nodos de campo observan y reportan, y cualquier capacidad de maniobra futura se diseña y revisa antes de activarse.

## 📁 Catálogo de Proyectos A.R.M.O.R.

| Repositorio | Versión | Descripción |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.2.6 | Contratos de mensajes, validadores, vectores de conformidad y tipos generados. |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.3.0 | Firmware del nodo de campo para ESP32-S3 con tres radares y su propio panel web. |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.0.9 | Protocolos de inversores y baterías solares y los mensajes de un nodo pasarela. |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.0.5 | Nodo eléctrico: contadores, el mensaje de las lecturas de la red y las reglas para maniobrar. |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.0.2 | La red local: sus dispositivos, internet y lo que cambia. |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.3.1 | Coordinador central: telemetría, alarmas, dispositivos, lecturas solares y cámaras. |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.1 | Política de inferencia visual que explica sus decisiones y nunca actúa. |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.2.1 | Intenciones de voz sin conexión con una confirmación imposible de falsificar. |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.3.8 | Consola web: cámaras, radar, alarmas, energía solar y el diseñador de sitio 2D/3D. |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.3.5 | Cliente Android del operador con radar 2D/3D en vivo. |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.2 | Cajas, electrónica y la matriz de aceptación en banco. |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.3.4 | Despliegue, el banco de pruebas del servidor central, copias de seguridad y TLS. |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.3 | Simulador de telemetría sin conexión con fallos repetibles. |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.0.2 | Detecta, instala y actualiza los propios repositorios del ecosistema. |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.4.8 | Arquitectura, base de seguridad y la matriz de capacidades. |

---

## 🤝 Contribuir
Cada ecosistema es su propia iniciativa con sus propios proyectos. Cada proyecto tiene sus propias pautas de contribución. Consulte los repositorios individuales para detalles técnicos.

Las etiquetas de issues están estandarizadas en todos los repos de HYDRA-UMC a partir de [`.github/labels.yml`](.github/labels.yml) en este mismo repo, sincronizadas por [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - edita ese único archivo para cambiar una etiqueta en todos a la vez, en vez de hacerlo a mano repo por repo. A diferencia del dashboard de abajo, esta lista es estática (una matriz real de GitHub Actions, no descubrimiento dinámico) - un repo nuevo necesita también una entrada ahí, no solo un `hydra-umc.project.json` real.

Un dashboard de estado en vivo que cubre todo repo público que declara `ecosystem: HYDRA-UMC` en su propio `hydra-umc.project.json` (stack, destino de despliegue, versión actual - leído directamente de la rama por defecto de cada repo, descubierto dinámicamente sin lista fija) se regenera cada hora (e inmediatamente tras un push relevante) mediante [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) y se sirve desde `docs/` vía GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. Añade una clasificación real de madurez por proyecto (andamiaje / funcional / establecido / producción, cada una decidida a partir del propio CHANGELOG de ese proyecto - ver el docstring del propio módulo [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) para el criterio exacto), su rol (API / UI / CLI / firmware / librería / servicio / herramienta), un árbol real de familia/padre-hijo, y notas por proyecto sobre lo que está realmente implementado hoy. Los propios repositorios de A.R.M.O.R. son privados y aparecen agrupados aparte en ese mismo dashboard, ya que necesitan el acceso propio de la cuenta para abrirse.

## 🧭 Colaboración en GitHub

El [modelo de colaboración en GitHub](docs/GITHUB_COLLABORATION.md) define una única Wiki central, un único Project del ecosistema, el ámbito de Discussions, los criterios de release y el límite de la automatización compartida. Los [formularios de issues](.github/ISSUE_TEMPLATE/) y la [plantilla de pull request](.github/PULL_REQUEST_TEMPLATE.md) centralizados hacen trazable el trabajo de software, validación de hardware y documentación sin duplicar manuales de proyecto.

El workflow de salud comunitaria es manual y funciona en modo simulación por defecto. Cuando se configure `COMMUNITY_HEALTH_SYNC_TOKEN`, podrá copiar solo estas plantillas gestionadas a cada repositorio que publique un manifiesto HYDRA-UMC; nunca elimina una plantilla específica de proyecto.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licencia GPL-3.0.
