<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner del Ecosistema HYDRA-UMC" width="100%">
</p>

# Ecosistema HYDRA-UMC / URTC 🤖🚀

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
  <img src="https://img.shields.io/badge/Plataforma-STM32%20%7C%20CM5-red.svg" alt="Plataforma">
  <img src="https://img.shields.io/badge/IA-Hailo--8%20%7C%20Hailo--10-green.svg" alt="Poder de IA">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenido al **Ecosistema HYDRA-UMC**, una plataforma de robótica industrial de múltiples capas que abarca desde firmware en tiempo real de bajo nivel hasta IA cognitiva de alto nivel. Esta organización alberga numerosos proyectos especializados diseñados para trabajar en perfecta sincronía para la automatización de micro-fábricas y robótica de enjambre.

## 📈 Progreso del Ecosistema

`[█████████▊░░░░░░░░░░] 49%` — Referencia orientativa. El 100% representa el ecosistema integrado funcionando sobre hardware real.

---

## 🚀 Características Clave y Escalabilidad

- **Escalabilidad Multi-Robot**: Soporta hasta 8 unidades robóticas distribuidas (actualmente de 3, 4, 5 y 6 ejes; escalable a 7, 8, 9 ejes y arquitecturas de robots duales en futuras versiones).
- **Etapa Local Integrada**: La placa principal HYDRA-UMC cuenta con una **Etapa Local de 6 ejes** integrada para tareas auxiliares, incluyendo robots secundarios, revólveres ATC (Cambiador Automático de Herramientas), sincronización de cintas transportadoras o pórticos de tablas XYZ.

---

## 🏗️ Arquitectura del Ecosistema

El ecosistema v1.1 es una plataforma de producto por capas: se apoya en tecnologías Linux y Raspberry Pi consolidadas, sin crear un sistema operativo nuevo ni sustituir las API de los fabricantes.

1.  **Base de plataforma**: Raspberry Pi OS ARM64 y los servicios Linux estándar proporcionan la base compatible para CM5.
2.  **Plataforma y contratos**: **HYDRA-UMC-OS** empaqueta perfiles reproducibles, servicios, diagnóstico y actualizaciones sobre Raspberry Pi OS; **HYDRA-UMC-SDK** publica contratos versionados, clientes ligeros y pruebas de conformidad.
3.  **Ejecución en tiempo real**: el firmware **HYDRA-UMC** y URTC sobre STM32/MCU mantienen los límites de movimiento, watchdogs y parada segura.
4.  **Coordinación y operaciones**: los servicios de servidor, despacho de trabajos, telemetría y configuración coordinan dispositivos sin saltarse el límite de seguridad del MCU.
5.  **Interfaces de operador**: Studio, Suite, DSI, web, escritorio, móvil y CLI consumen los contratos del SDK.
6.  **Percepción e inteligencia**: visión, Hailo y servicios cognitivos proponen observaciones o planes; no tienen autoridad de seguridad física.
7.  **Ingeniería, industria y datos**: Gemelo Digital, HIL/física, pasarelas OPC-UA/MQTT/MTConnect y datos validan e integran el sistema.

Para desarrollar, se parte de la arquitectura y el modelo de servicios públicos de **HYDRA-UMC-OS** y se usan los contratos y reglas de conformidad de **HYDRA-UMC-SDK**. La autoridad de seguridad del MCU/URTC se conserva en todos los flujos.

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

## 📁 Catálogo de Proyectos

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
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | Capa de plataforma Raspberry Pi OS para CM5: perfiles reproducibles, configuración, diagnóstico, ciclo de servicios y actualizaciones; no es una distribución Linux nueva. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | Contratos versionados, clientes ligeros y pruebas de conformidad compartidos para servicios, interfaces, adaptadores CM5 y URTC; no sustituye API de fabricantes. |

### 💠 Control core e interfaces de operador
| Repositorio | Descripción |
| :--- | :--- |

### 💠 Control core e interfaces de operador
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | Firmware de control de movimiento core para STM32H745/G474 con cinemática S-Curve. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | API Node.js headless y backend WebSocket para orquestación robótica. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | Dashboard web avanzado basado en React para monitoreo y control 3D. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | Aplicación de escritorio Python/Qt de alto rendimiento para automatización industrial. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | Interfaz táctil basada en Flutter para pantallas industriales de 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | App móvil nativa Kotlin con login biométrico para gestión remota. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | App móvil Flutter para iOS/iPadOS con sincronización WebSocket en tiempo real. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | Editor gráfico de URDF para validar y subir modelos de robots al catálogo. |


### 🔧 Núcleo y herramientas URTC
| Repositorio | Descripción |
| :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | Firmware de controlador de herramientas universal para más de 25 herramientas especializadas. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | Herramienta GUI para actualizaciones de firmware CAN-OTA y SWD/JTAG. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | Herramienta de diagnóstico CAN-bus con paneles de telemetría por herramienta. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | Herramienta Web Serial para pruebas y análisis instantáneo de hardware. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | Almacenamiento inteligente de herramientas con precalentamiento y auditoría. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | Cabezal con cámaras térmicas y RGB integradas para QA activo. |

### 👁️ Nodo de IA de Visión (Optimizado para Hailo-8)
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | Nodo de percepción de alta velocidad para 8 flujos simultáneos de cámaras USB 3.0. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | Pipeline optimizado de GStreamer/MediaMTX para retransmisión de video industrial. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | Librería de modelos YOLO acelerados por hardware para QA de componentes y SMD. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | Detección de intrusiones por IA en tiempo real para protección del volumen de trabajo. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | Feedback cinemático basado en imagen para corrección de pose submilimétrica. |

### 🧠 Nodo de IA Cognitiva (Optimizado para Hailo-10)
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | Nodo de razonamiento semántico para planificación lógica de misiones y control por voz. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | Implementación del modelo Vision-Language-Action para ejecución de tareas complejas. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | Pipeline local y privado de STT/TTS para interacción natural con el operador. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | Orquestador de misiones basado en LLM con recuperación de errores sensible al contexto. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | Asistente de IA basado en RAG entrenado con manuales técnicos y código fuente. |

### 🐝 Orquestación y Enjambre
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | Gestor de flota para coordinación multi-robot y prevención de colisiones. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | Sincronización PTP para coordinación de robots con precisión de nanosegundos. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | Optimizador de trayectorias distribuido para enjambres en espacios compartidos. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | Programador de tareas basado en prioridades para flotas heterogéneas. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | Monitor de alta disponibilidad con failover transparente de misiones. |

### 🎮 Gemelo Digital y Simulación
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | Motor de simulación física de alta fidelidad para pruebas sin riesgo. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | Simulación física real (MuJoCo/PhysX) de cadenas cinemáticas URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | Interfaz Hardware-in-the-loop para consistencia entre estado real y virtual. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | Generador de datasets procedimentales para entrenar modelos de IA de visión. |

### 📊 Datos y Analítica
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | Almacenamiento Big Data para telemetría industrial masiva multi-robot. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | Ingestor de alto rendimiento para logs de CAN, WebSocket y sistema. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | Motor de mantenimiento predictivo basado en firmas de vibración de motores. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | Generación automática de OEE y KPIs para gestión de planta industrial. |

### 🏭 Pasarela Industrial
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | Puente de interoperabilidad para estándares de fábrica (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | Mapeo de objetos robóticos HydraState a nodos estándar OPC-UA. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | Puente de telemetría para integraciones IoT y dashboards externos. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | Interfaz estandarizada para monitoreo de salud de máquinas y robots. |

### 🌉 Puentes de Automatización Externa
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | Límite de coordinación bidireccional ROS 2: topics para observación, servicios para inspección y acciones cancelables para trabajos de celda. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | Coordinador trazable de entrega de PCB para OpenPnP y carga o descarga asistida por robots. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | Puente seguro alrededor de software de impresión 3D; el primer adaptador valida Moonraker sin sustituir firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | Coordinador de auxiliares de celda CNC; la trayectoria y la seguridad siguen siendo nativas del controlador. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | Coordinador de auxiliares de celda láser que no puede armar, disparar ni anular interlocks. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | Límite de coordinación para droides con patas/humanoides: vocabulario de acciones caminar/coger/soltar filtrado por el contrato de seguridad compartido; la marcha y el equilibrio siguen siendo del propio controlador del droide. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | Límite de coordinación para flotas AGV/AMR: transformación de la trama de fábrica a la trama local más un vocabulario de órdenes inspirado en VDA-5050; la planificación de rutas sigue siendo de la propia navegación del AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | Límite de coordinación para UAV con cámara: vocabulario de solicitudes de vuelo con nombre más un watchdog determinista de heartbeat/pérdida de enlace. |

### 🛠️ Herramientas Complementarias
| Repositorio | Descripción |
| :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | Dashboard de emergencia wearable con alertas de seguridad hápticas. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | Interfaz de línea de comandos para automatización de flota, flasheo y devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | Extensión de IA para dashboards web que ofrece insights en lenguaje natural. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | Herramienta multiplataforma GUI/CLI para detectar, instalar y actualizar a mano cada proyecto del ecosistema. |

---

## 🤝 Contribuir
Este ecosistema es parte de una iniciativa robótica de alta tecnología. Cada proyecto tiene sus propias pautas de contribución. Consulte los repositorios individuales para detalles técnicos.

Las etiquetas de issues están estandarizadas en los 45 repos a partir de [`.github/labels.yml`](.github/labels.yml) en este mismo repo, sincronizadas por [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - edita ese único archivo para cambiar una etiqueta en todos a la vez, en vez de hacerlo a mano repo por repo.

Un dashboard de estado en vivo de los 45 repos (stack, destino de despliegue, versión actual - leído directamente de la rama por defecto de cada repo) se genera a diario mediante [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) y se sirve desde `docs/` vía GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. La v3 añade una clasificación real de madurez por proyecto (andamiaje / funcional / establecido / producción, cada una decidida a partir del propio CHANGELOG de ese proyecto - ver el docstring del propio módulo [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) para el criterio exacto), su rol (API / UI / CLI / firmware / librería / servicio / herramienta), un árbol real de familia/padre-hijo, y notas por proyecto sobre lo que está realmente implementado hoy.

## 🧭 Colaboración en GitHub

El [modelo de colaboración en GitHub](docs/GITHUB_COLLABORATION.md) define una única Wiki central, un único Project del ecosistema, el ámbito de Discussions, los criterios de release y el límite de la automatización compartida. Los [formularios de issues](.github/ISSUE_TEMPLATE/) y la [plantilla de pull request](.github/PULL_REQUEST_TEMPLATE.md) centralizados hacen trazable el trabajo de software, validación de hardware y documentación sin duplicar manuales de proyecto.

El workflow de salud comunitaria es manual y funciona en modo simulación por defecto. Cuando se configure `COMMUNITY_HEALTH_SYNC_TOKEN`, podrá copiar solo estas plantillas gestionadas a cada repositorio que publique un manifiesto HYDRA-UMC; nunca elimina una plantilla específica de proyecto.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licencia GPL-3.0.
