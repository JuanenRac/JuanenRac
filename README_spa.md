<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Electro Hobby 3D Banner" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  🇪🇸 <b>Español</b> |
  <a href="README\_fra.md">🇫🇷 Français</a> |
  <a href="README\_ita.md">🇮🇹 Italiano</a> |
  <a href="README\_deu.md">🇩🇪 Deutsch</a> |
  <a href="README\_zho.md">🇨🇳 简体中文</a> |
  <a href="README\_jpn.md">🇯🇵 日本語</a> |
  <a href="README\_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

Cuatro ecosistemas de ingeniería independientes, un solo autor. **HYDRA-UMC** es una plataforma de robótica industrial multicapa, desde firmware en tiempo real hasta IA cognitiva. **URTC** es su subsistema universal de herramientas robotizadas: firmware en tiempo real y herramientas de escritorio/web para el efector final de un robot, desarrollado como un producto propio con versionado independiente y herramientas de mantenimiento. **A.R.M.O.R.** es un ecosistema público y separado de seguridad perimetral y domótica: detección de presencia por radar, monitorización solar y eléctrica, y un controlador central con clientes web y móviles. **EH3D Fabrication Suite** es un ecosistema de software integrado para la creación de prototipos de PCB, procesamiento CAM, inspección por visión artificial, gestión de Pick \& Place y control de CNC/láser que interactúa con el hardware de HYDRA-UMC y maquinaria de taller especializada.


## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Se escribe con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo previsto.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Hecho a medias o sin verificar · 🔴 Sin hacer o sin funcionar

| Área | Estado | Qué significa aquí |
|---|---|---|
| Panel y vigilancia | 🟢 | El panel de estado, la vigilancia de CI, la matriz de salud, la comprobación de enlaces y el resumen de versiones se ejecutan de forma programada en GitHub Actions, y sus últimas ejecuciones pasan. |
| Pruebas | 🟢 | Pasan 59 pruebas (`python -m unittest discover -s tests`): el catálogo, la vigilancia, los banners, la siembra de la hoja de ruta de los cuatro tableros (HYDRA-UMC, URTC, A.R.M.O.R. y EH3D) y la paridad de los README. |
| Catálogo y versiones | 🟡 | La columna Versión de cada tabla de proyectos se rellena con un script a partir del manifiesto de cada repositorio y se comprueba, así que no queda desfasada; las descripciones de una línea se escriben a mano. |
| Barras de progreso | 🟢 | El porcentaje de cada ecosistema lo calcula `scripts/ecosystem_progress.py` con la madurez y la evidencia que cada repositorio declara en su propio manifiesto, y se renueva con el panel; el hito del 100% sigue siendo un ecosistema totalmente integrado funcionando en hardware real. |
| Paridad en ocho idiomas | 🟢 | Los ocho README mantienen las mismas secciones, los mismos enlaces de GitHub y el mismo número de filas de tabla, y una prueba falla si uno se desvía. |
| Hardware real | 🟢 | No aplica: este repositorio contiene el perfil y su automatización, nada aquí se ejecuta en hardware. |
| Documentación | 🟢 | README en ocho idiomas con los cuatro ecosistemas, la guía de colaboración en GitHub y los ficheros de comunidad. |

## 🧭 Sobre Electro Hobby 3D y su actualizador

**Electro Hobby 3D** es el taller de JuanenRac: electrónica, robótica y software que se diseñan, construyen, programan y prueban en un mismo sitio. Cada repositorio se describe con un manifiesto, lleva su propia documentación y dice qué se ha probado y qué no en hardware real.

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) es **el actualizador de los cuatro ecosistemas**: una ventana y una línea de órdenes que ceden el trabajo al actualizador de cada ecosistema, que son los que descubren, instalan y actualizan sus repositorios. Cada ecosistema de abajo nombra el suyo.

| Ecosistema | Qué es | Actualizador |
|---|---|---|
| **HYDRA-UMC** | Robótica industrial y control de máquinas, del firmware en tiempo real a la IA cognitiva | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | Firmware y herramientas para los efectores de un robot | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | Seguridad perimetral y domótica | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | Prototipado de PCB, CAM, CNC y láser, pick and place | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

\---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bienvenido al **Ecosistema HYDRA-UMC**, una plataforma de robótica industrial multicapa que abarca desde el firmware de bajo nivel en tiempo real hasta la IA cognitiva de alto nivel. Esta organización alberga muchos proyectos especializados diseñados para trabajar en perfecta sintonía para la automatización de microfábricas y la robótica de enjambres.

**Actualizador:** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) detecta, instala y actualiza los repositorios de este ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo hace para los cuatro.

## 📈 Progreso del Ecosistema

<!-- progress:hydra-umc -->
`\[█████████▎░░░░░░░░░░] 46%` — Calculado con datos reales: la madurez y la evidencia que cada uno de sus 57 repositorios declara en su propio manifiesto. El hito del 100% es un ecosistema totalmente integrado operando sobre hardware real.
<!-- /progress:hydra-umc -->

> \[!IMPORTANT]
> 🛠️ \*\*Proyecto en pausa — construyendo el hardware real.\*\* El desarrollo activo está pausado mientras se construye físicamente la celda de robótica (chasis, cableado, las placas reales CM5 y STM32), de modo que la siguiente fase de trabajo tenga hardware real sobre el cual ejecutarse y validarse, y no solo una barra de progreso que aumenta. El trabajo se reanudará una vez que dicha construcción esté lista.

\---

## 🚀 Características Clave y Escalabilidad

* **Escalabilidad Multi-Robot**: Soporta hasta 8 unidades robóticas distribuidas (3, 4, 5 y 6-DOF actuales; escalando a 7, 8, 9-DOF y arquitecturas de doble robot en futuras versiones).
* **Plataforma Local Integrada**: La placa principal HYDRA-UMC cuenta con una **Plataforma Local de 6 ejes** integrada para tareas auxiliares, incluyendo robots secundarios, revólveres ATC (Cambio Automático de Herramientas), sincronización de cintas transportadoras o pórticos de mesa XYZ.

\---

## 🏗️ Arquitectura del Ecosistema

El ecosistema v1.1 es una plataforma de productos en capas: se basa en tecnología Linux y Raspberry Pi establecida en lugar de crear un nuevo sistema operativo o reemplazar las API de los fabricantes.

1. **Base de la plataforma**: Raspberry Pi OS ARM64 y los servicios estándar de Linux proporcionan la base CM5 soportada.
2. **Plataforma y contratos**: **HYDRA-UMC-OS** empaqueta perfiles reproducibles, servicios, diagnósticos y actualizaciones en Raspberry Pi OS; **HYDRA-UMC-SDK** publica contratos versionados, clientes ligeros y accesorios de conformidad.
3. **Ejecución en tiempo real**: El firmware de **HYDRA-UMC** gestiona los límites de movimiento, temporizadores de vigilancia (watchdogs) y parada segura en STM32/MCU; la herramienta en sí, y su propia autoridad en tiempo real sobre el efector final, pertenece al ecosistema independiente **URTC** detallado más abajo.
4. **Coordinación y operaciones**: Servicios de servidor, distribución de trabajos, telemetría y configuración coordinan los dispositivos sin saltarse el límite de seguridad de la MCU.
5. **Interfaces de operador**: Studio, Suite, DSI, web, escritorio, móvil y clientes CLI utilizan los contratos del SDK.
6. **Percepción e inteligencia**: La visión, Hailo y los servicios cognitivos proponen observaciones o planes; no tienen autoridad de seguridad física.
7. **Ingeniería, industrial y datos**: Gemelo digital, HIL/física, pasarelas OPC-UA/MQTT/MTConnect y servicios de datos validan e integran el sistema.

Para obtener orientación de implementación, comience con la arquitectura pública y la documentación de servicios en **HYDRA-UMC-OS**, luego utilice los contratos y las reglas de conformidad en **HYDRA-UMC-SDK**. La autoridad de seguridad de la MCU se preserva en todo momento y flujo.

\---

## 🛠️ Pila Tecnológica y Herramientas

El ecosistema aprovecha una pila moderna y de alto rendimiento para garantizar la fiabilidad en misiones críticas:

### 💠 Embebido y Tiempo Real (Ejecución)

* **Microcontroladores**: STM32H745 (Doble Núcleo 480MHz), STM32G474 (170MHz), STM32F303.
* **Frameworks**: FreeRTOS (modo AMP), CMSIS-DSP, STM32 HAL/LL.
* **Protocolos**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (Esclavo IPC 50MHz), I2C, UART.
* **Cinemática**: Generación de perfiles en curva S, Cinemática Inversa en Tiempo Real (IK).

### 🧠 Edge AI y Percepción (Inteligencia)

* **Aceleradores**: Hailo-8 (26 TOPS) para visión de 8 cámaras simultáneas, Hailo-10 (40 TOPS) para GenAI.
* **Modelos**: YOLOv10 (Detección), OpenVLA (Acción), Whisper (Voz), Llama-3 (Razonamiento).
* **Inter-nodo**: gRPC sobre Protobuf e intercambio de metadatos SPI-DMA de alta velocidad.

### 🌐 Backend y Coordinación (Coordinación)

* **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orquestador), Go (CLI).
* **Infraestructura**: Express, Fastify, Socket.io (WebSocket), gRPC.
* **Base de datos**: InfluxDB/TimescaleDB (Telemetría), Redis (Estado), SQLite.

### 💻 Paneles e Interfaz de Usuario (Interfaz)

* **Web**: React 19, Vite, Three.js (Visor 3D), Tailwind CSS.
* **Nativa**: Python 3.12/PySide6 (Suite), Kotlin (Android Nativo), Flutter 3.x (iOS y DSI).

\---

## 📋 Requisitos del Sistema

* **Nodo de Computación**: Raspberry Pi CM5 (4GB+ RAM) con almacenamiento NVMe/eMMC.
* **Hardware de IA**: Módulos M.2 Hailo-8/Hailo-10 (Key M).
* **Bus de Campo**: Ethernet Gigabit para LAN y FDCAN (ISO 11898-1:2015) para actuadores.
* **SO Cliente**: Android 10+, iOS 15+, Windows 10/11 (Alta DPI), Ubuntu 22.04 LTS.

\---

## 🔒 Seguridad Industrial

* **Capa E-STOP**: Línea de emergencia cableada físicamente + tramas de emergencia CAN de alta prioridad (<1ms).
* **Seguridad por IA**: Zonas de seguridad 3D con corte automático de par en los motores ante la intrusión humana.
* **Ciberseguridad**: Autenticación sin estado basada en JWT + mTLS para el tráfico seguro entre nodos.
* **Integridad**: F-RAM no volátil para la auditoría del ciclo de vida de las herramientas y recuperación de estados.

\---

## 🔧 Hacking de Hardware: Construyendo tu Propia Placa Portadora (Carrier)

La Placa Controladora de Robot está construida alrededor de una **Raspberry Pi CM5**, y el doble conector Hirose DF40 propio de la CM5 es un patillaje fijo, oficial y público (Tabla 5 de la propia hoja de datos de la CM5 de Raspberry Pi), no algo que este proyecto invente. Esto significa que una placa portadora de terceros compatible es un proyecto real y factible, no un ejercicio de ingeniería inversa:

* **Empieza aquí**: [`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) — qué pines fijos de la CM5 utiliza realmente esta placa (Ethernet, los 2 PHYs USB3 SuperSpeed nativos, el cabezal del ventilador de refrigeración del lado de la CM5) y por qué, reorganizados por función a partir de la tabla oficial de patillaje.
* **El acceso fácil**: el **conector GPIO estándar de 40 pines de Raspberry Pi** (la misma disposición "B+" inalterada desde 2014) está disponible en esta placa exactamente igual que en cualquier Raspberry Pi; los HATs de RPi existentes y las herramientas GPIO funcionan sin modificar. Un puñado de posiciones que el propio enlace STM32 de esta placa ya utiliza están serigrafiadas/anotadas para que sepas cuáles debes omitir.
* **Ir más allá**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) cubre cómo se comunican en realidad la CM5, el STM32H745 "Cerebro Cinemático" y el STM32G474 "Controlador de Robot" (SPI1 + FDCAN1 + el buzón IPC CM7↔CM4): la capa que un rediseño de placa portadora necesitaría preservar si pretende seguir siendo compatible con el firmware propio de este proyecto.
* Cada documento de patillaje indica claramente si está **CONFIRMADO** (extraído directamente de una tabla de la hoja de datos oficial) o **PROPUESTO** (elección de enrutamiento propia de este proyecto, abierta a una diferente en una placa derivativa); lee esa línea de estado antes de tratar una asignación de señal como fija.

Esto no es un tutorial guiado (no existe una única placa portadora "correcta" para cada caso de uso): es el material de referencia real que un diseñador de hardware experimentado necesita para partir de un mapa de pines conocido y fiable en lugar de depender únicamente de una hoja de datos.

\---

## 📁 Catálogo de Proyectos HYDRA-UMC

¿Eres nuevo en el ecosistema? `./starter-kit.sh` (o `starter-kit.bat` en Windows) clona 13 repositorios principales —un conjunto de inicio seleccionado a mano— como hermanos en un mismo directorio: la disposición estándar que cada script multi-repositorio aquí ya asume. Un segundo argumento clona un ecosistema entero en su lugar, descubierto en vivo por su manifiesto: `hydra-umc`, `urtc`, `armor`, `eh3d` o `all` (por ejemplo, `./starter-kit.sh \~/work armor`). Volver a ejecutarlo es seguro: cualquier cosa ya clonada se deja intacta. A partir de ahí, el actualizador propio de cada ecosistema —o [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) para los cuatro— puede comprobar versiones y compilar/actualizar cualquier otro proyecto.

### 🧱 Base de la Plataforma y Contratos

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.6|Capa de plataforma de Raspberry Pi OS para CM5: perfiles reproducibles, configuración, diagnóstico, ciclo de vida de servicios y actualizaciones; no es una nueva distribución de Linux.|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.4.3|Contratos versionados compartidos, clientes ligeros y accesorios de conformidad para servicios, interfaces de usuario y adaptadores CM5; no reemplaza las API de los fabricantes.|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.6|Registro declarativo de manifiestos de adaptadores y validador para conectores de máquinas externas; extiende la idea de contrato del SDK a máquinas externas sin reemplazar los proyectos de pasarelas industriales.|

### 💠 Control Central y Clientes de Operador

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.4|Firmware central de control de movimiento para STM32H745/G474 con cinemática de curva S.|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.7|API sin cabeza (headless) en Node.js y backend WebSocket para la orquestación robótica.|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.7|Panel de control web avanzado basado en React para monitorización y control de robots 3D.|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.7.6|Aplicación de escritorio de alto rendimiento en Python/Qt para automatización industrial.|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.9|Interfaz táctil dedicada basada en Flutter para pantallas industriales de 7" (CM5).|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.5|Aplicación móvil nativa en Kotlin con inicio de sesión biométrico para la gestión remota de robots.|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.9|Aplicación móvil en Flutter para iOS/iPadOS con sincronización por WebSocket en tiempo real.|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.8|Editor gráfico URDF para validar y enviar modelos de robots al catálogo.|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.9|Editor de modelos STL de escritorio: transforma, reemplaza, elimina y añade piezas reales en el catálogo de modelos compartido.|
| [HYDRA-UMC-MESHES](https://github.com/JuanenRac/HYDRA-UMC-MESHES) | 0.1.0 | Mallas 3D compartidas (STL y GLB) de las aplicaciones de escritorio y web, publicadas una sola vez como paquete de release con sumas de comprobación. |

### 👁️ Nodo de Visión por IA (Optimizado para Hailo-8)

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.8|Nodo de percepción de alta velocidad para 8 flujos simultáneos de cámaras USB 3.0.|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.3|Canalización optimizada GStreamer/MediaMTX para retransmisión de vídeo industrial.|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.7|Librería de modelos YOLO acelerados por hardware para control de calidad (QA) de componentes y SMD.|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.8|Detección de intrusiones por IA en tiempo real para la protección del volumen de trabajo robótico.|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.2.2|Retroalimentación cinemática basada en imágenes para la corrección de poses submilimétricas.|

### 🧠 Nodo de IA Cognitiva (Optimizado para Hailo-10)

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.6|Nodo de razonamiento semántico para la planificación lógica de misiones y control por voz.|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.2.0|Implementación de modelo Visión-Lenguaje-Acción para la ejecución de tareas complejas.|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.2.0|Canalización local y privada de STT/TTS para la interacción del operador en lenguaje natural.|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.6|Orquestador de misiones basado en LLM con recuperación de errores contextual.|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.6|Asistente de IA basado en RAG entrenado en manuales técnicos y código fuente.|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.9|Técnico de mantenimiento de IA local controlado por políticas: una política de nivel de riesgo fijo y lista blanca de herramientas hoy, con una defensa real y probada que demuestra que un documento recuperado malicioso nunca puede activar una llamada a herramienta ni filtrar un secreto; la IA nunca obtiene autoridad generando una respuesta.|

### 🐝 Orquestación y Enjambres

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.2.2|Gestor de flotas para la coordinación multi-robot y prevención de colisiones.|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.7|Sincronización PTP (Precision Time Protocol) para la sincronización de robots a nivel de nanosegundos.|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.2|Optimizado de rutas distribuido para enjambres robóticos de espacio de trabajo compartido.|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.5|Programador de tareas basado en prioridades para flotas de robots heterogéneas.|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.2.1|Monitor de alta disponibilidad con conmutación por error (failover) de misiones transparente.|

### 🎮 Gemelo Digital y Simulación

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.1.2|Motor de simulación física de alta fidelidad para pruebas de robots libres de riesgos.|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.1.1|Simulación de física del mundo real (MuJoCo/PhysX) de cadenas URDF.|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.1.2|Interfaz Hardware-in-the-Loop para la sincronización de comandos reales frente a virtuales.|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.2|Generador procedimental de conjuntos de datos de entrenamiento para nodos de visión.|

### 📊 Datos y Analítica

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.2.1|Almacenamiento Big Data para datos masivos de robótica industrial.|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.9|Ingestor de alto rendimiento para CAN, WebSocket y registros del sistema.|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.2.0|Motor de mantenimiento predictivo basado en firmas de vibración de motores.|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.8|Generación automatizada de OEE y KPIs para la gestión de plantas industriales.|

### 🏭 Pasarela Industrial

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.8|Puente de interoperabilidad de Industria 4.0 para estándares de fábrica (OPC-UA/MQTT).|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.2.3|Mapeo de objetos robóticos HydraState a nodos OPC-UA estándar.|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.9|Puente de telemetría para integraciones IoT y paneles de control externos.|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.2.1|Interfaz estandarizada para la monitorización de salud de herramientas de máquinas y robots.|

### 🌉 Puentes de Automatización Externa

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.5|Límite de coordinación bidireccional ROS 2: temas para observación, servicios para inspección y acciones cancelables para trabajos de celdas.|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.2.2|Coordinador de transferencia de PCB rastreable para OpenPnP y carga o descarga asistida por robot.|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.2.1|Puente seguro en torno al software nativo de impresoras 3D; el primer adaptador valida la preparación de Moonraker sin reemplazar el firmware.|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.2.3|Coordinador auxiliar de celdas CNC; la trayectoria del controlador y la seguridad de la máquina se mantienen nativas.|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.2.0|Coordinador auxiliar de celdas láser que no puede armar, disparar ni anular los enclavamientos del láser.|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.4|Límite de coordinación para droides cuadrúpedos/humanoides: vocabulario de acciones de caminar/recoger/colocar con nombre regulado a través del contrato de seguridad compartido; la marcha y el equilibrio permanecen en el controlador propio del droide.|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.6|Límite de coordinación para flotas de AGV/AMR: transformación de marco de fábrica a local más un vocabulario de órdenes inspirado en VDA-5050; la planificación de rutas permanece en la navegación propia del AMR.|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.7|Límite de coordinación para UAVs equipados con cámaras: vocabulario de solicitudes de vuelo con nombre más un sistema de vigilancia de seguridad (watchdog) determinista de latido/pérdida de enlace.|

### 🛠️ Herramientas Complementarias

|Repositorio|Versión|Descripción|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.7|Panel de emergencia portátil (wearable) con alertas de seguridad hápticas.|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.2.0|Interfaz de línea de comandos para automatización de flotas, flasheo y DevOps.|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.9|Extensión de IA para paneles web que proporciona información en lenguaje natural.|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.5.1|Herramienta GUI/CLI multiplataforma para detectar, instalar y actualizar manualmente cada proyecto del ecosistema.|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.4|Herramienta de escritorio para Windows/Linux que compila una imagen CM5 lista para flashear precargada con las versiones más actuales del ecosistema y configuración de primer arranque estilo Raspberry-Pi-Imager.|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.2.1|Coordinador de incidentes de mantenimiento: un rol de borde con bajos privilegios recopila una instantánea desinfectada de inventario/salud, un rol de plano de control la procesa en modo de solo lectura y solicita a un proveedor de IA que sugiera un diagnóstico; nunca aplica un parche ni despliega nada.|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.2.0|Host de desarrollo reproducible: un esquema de configuración regulado por políticas e inventario de manifiestos hoy en día, evolucionando hacia un ejecutor aislado de tareas/espacios de trabajo coordinado con OPS-AGENT; ninguna tarea tiene nunca permiso de despliegue a menos que un documento lo conceda explícitamente.|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.6|Arquitectura, interfaces, línea base de seguridad, matriz de capacidades y catálogo de proyectos generado del ecosistema, además de las herramientas que comparan todos los repositorios.|

\---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="URTC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Tools-25%2B%20profiles-blueviolet.svg" alt="Tools">
</p>

**URTC (Universal Robot Tool Controller - Controlador Universal de Herramientas de Robot)** es un producto propio, no una carpeta de subsistema de HYDRA-UMC: firmware en tiempo real y una familia de herramientas de escritorio/web para el efector final de un robot, desarrollado, versionado y mantenido de forma independiente. Un cambiador de herramientas equipado con URTC se coordina con el controlador de celda de HYDRA-UMC a través de FDCAN, pero el comportamiento en tiempo real, el watchdog y el estado seguro de la propia herramienta son competencia exclusiva de URTC; el controlador de celda no puede omitirlos, y URTC no depende de HYDRA-UMC para ser desarrollado, flasheado o diagnosticado.

**Actualizador:** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) detecta, instala y actualiza los repositorios de este ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo hace para los cuatro.

<!-- progress:urtc -->
`\[███████░░░░░░░░░░░░░] 35%` — Calculado con datos reales: la madurez y la evidencia que cada uno de sus 11 repositorios declara en su propio manifiesto. El hito del 100% es un ecosistema totalmente integrado operando sobre hardware real.
<!-- /progress:urtc -->

## 🏗️ Cómo Funciona URTC

1. **Firmware de la herramienta**: El firmware STM32 propio de URTC ejecuta cada uno de los más de 25 perfiles de herramientas especializados (pinzas, dispensadores, sondas, husillos y más), cada uno con sus propios tiempos, límites y comportamiento ante fallos.
2. **Actualización de campo**: CAN-OTA envía una nueva imagen de firmware a través del mismo bus CAN que la herramienta ya utiliza, con una ruta SWD/JTAG de chip completo (URTC-FLASHER) como alternativa de respaldo que nunca depende de que el propio firmware de la herramienta esté operativo.
3. **Diagnóstico en vivo**: URTC-TESTER valida el comportamiento CAN en tiempo real de una herramienta frente a su perfil declarado sin necesidad de una configuración completa de taller; URTC-WEB-STUDIO hace lo mismo desde una pestaña del navegador a través de Web Serial, sin necesidad de instalar nada.
4. **Almacenamiento y ciclo de vida**: URTC-SMART-RACK almacena las herramientas entre tareas, precalienta una antes de una transferencia y mantiene un registro de auditoría del ciclo de vida (ciclos, fallos, última calibración) por herramienta física, no por tipo de herramienta.
5. **Control de calidad activo**: URTC-VISION-TOOL es en sí misma una herramienta: un cabezal de herramienta con cámaras térmicas y RGB integradas para la inspección de calidad en proceso, no una cámara externa acoplada a otra herramienta.
6. **Base compartida**: **URTC-COMMON** contiene el protocolo CAN del cabezal de la herramienta como datos, con código generado y vectores de conformidad; **URTC-DOCS** contiene la arquitectura, la línea base de seguridad y la matriz de capacidades. **URTC-DEVTOOLS** guarda como un solo conjunto versionado las herramientas de repositorio que comparte toda la familia.

## 🛠️ Pila Tecnológica

* **Firmware**: STM32, FDCAN (bus compartido con el controlador de celda), CAN-OTA, alternativa SWD/JTAG.
* **Herramientas de escritorio**: Clientes GUI multiplataforma para flasheo y diagnóstico (URTC-FLASHER, URTC-TESTER).
* **Herramientas de navegador**: La API Web Serial para pruebas de hardware sin instalación (URTC-WEB-STUDIO).
* **Datos del ciclo de vida**: Registro de auditoría no volátil por herramienta, compartido con el enfoque de integridad F-RAM propio de HYDRA-UMC.

## 🔒 Seguridad

Cada perfil de herramienta cuenta con su propio watchdog y comportamiento ante fallos, independiente de la capa E-STOP del controlador de celda; una herramienta que pierde su presupuesto de tiempo o su latido CAN pasa a su estado seguro declarado por sí sola, en lugar de esperar un comando externo. El precalentamiento de URTC-SMART-RACK está acotado por los mismos límites térmicos por herramienta que declara su perfil, auditados en el mismo registro de ciclo de vida que un taller utiliza para decidir si una herramienta sigue siendo apta para el servicio.

## 📁 Catálogo de Proyectos URTC

|Repositorio|Versión|Descripción|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.4.2|Firmware de Controlador Universal de Herramientas de Robot para más de 25 herramientas especializadas.|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.4.4|Herramienta GUI para actualizaciones de firmware CAN-OTA y SWD/JTAG de chip completo.|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.4.5|Herramienta de diagnóstico para la validación en tiempo real de perfiles de herramientas URTC a través de CAN.|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.4.0|Herramienta Web Serial basada en navegador para pruebas y análisis instantáneos de hardware.|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.2.3|Almacenamiento inteligente de herramientas con precalentamiento automático y auditoría del ciclo de vida.|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.6|Cabezal de herramienta con cámaras térmicas y RGB integradas para control de calidad activo.|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.2.1|Detecta, instala y actualiza los repositorios URTC en una máquina a partir de sus propios manifiestos.|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.1.3|Arquitectura, interfaces, línea base de seguridad, matriz de capacidades, nota de estudio del protocolo CAN y catálogo de proyectos generado del ecosistema URTC, además de las herramientas que comparan todos los repositorios.|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.1.2|El protocolo CAN del cabezal de la herramienta como datos: una especificación, código C, TypeScript y Python generado, vectores de conformidad y transportes en Python.|
|[URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY)|0.0.4|Pasarela delante del bus CAN de URTC: lista de identificadores permitidos, límite de tasa y clave de sesión.|
|[URTC-DEVTOOLS](https://github.com/JuanenRac/URTC-DEVTOOLS)|0.0.1|Las herramientas de repositorio compartidas de la familia URTC como un solo conjunto versionado, con un fichero de bloqueo en cada repositorio.|

\---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ARMOR_BANNER.svg" alt="A.R.M.O.R. Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range - Rango de Observación Multimodal y Radar Autónomo)** es un ecosistema público y separado de seguridad perimetral y domótica, sin relación con HYDRA-UMC o URTC más allá de tener el mismo autor y las mismas convenciones de ingeniería (manifiestos versionados, un contrato de mensajes compartido, interfaces en ocho idiomas). Sus nodos de campo vigilan el perímetro de una propiedad y su instalación solar y eléctrica; su servidor central y clientes permiten a un operador ver y actuar sobre lo que informan. Las notas de versión y madurez que se muestran a continuación provienen directamente del manifiesto propio de cada repositorio y de su matriz de capacidades, siguiendo la misma convención de honestidad que ya utiliza el panel de control de HYDRA-UMC.

**Actualizador:** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) detecta, instala y actualiza los repositorios de este ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo hace para los cuatro.

<!-- progress:armor -->
`\[████████████▍░░░░░░░] 62%` — Calculado con datos reales: la madurez y la evidencia que cada uno de sus 19 repositorios declara en su propio manifiesto. El hito del 100% es un ecosistema totalmente integrado operando sobre hardware real.
<!-- /progress:armor -->

## 🏗️ Cómo Está Construido A.R.M.O.R.

1. **Contrato compartido**: **ARMOR-COMMON** contiene el significado de los mensajes (JSON Schema, un validador en Python y tipos generados en TypeScript/Kotlin) que todos los demás repositorios consumen y nunca redefinen.
2. **Nodos de campo**: Firmware ESP32-S3 para detección de radar/presencia (**ARMOR-NODE-RADAR**), monitorización de inversores solares y baterías (**ARMOR-NODE-SOLAR**), medición eléctrica con conmutación (**ARMOR-NODE-ELECTRICAL**), y el panel de alarma de la casa (**ARMOR-NODE-ALARM**); un agente en Python (**ARMOR-NETWORK**) supervisa la red local y la accesibilidad a internet de la casa desde una máquina ya conectada a ella.
3. **Coordinador central**: **ARMOR-SERVER** mantiene el estado, usuarios, alarmas, automatizaciones y evidencias de cámara; **ARMOR-SERVER-AI** y **ARMOR-VOICE-AI** añaden una política visual explicable y comandos de voz offline que nunca accionan nada por sí mismos.
4. **Clientes de operador**: **ARMOR-STUDIO** (web), **ARMOR-ANDROID-CONTROL** (móvil) y **ARMOR-IOS-CONTROL** (iPhone) son clientes del servidor central, nunca de la red de campo directamente. **ARMOR-NODE-HMI** es un panel táctil en la pared (un Waveshare ESP32-S3-Touch-LCD-7C-BOX) que muestra el estado, arma y reconoce alertas, y será donde resida el asistente de voz.
5. **Despliegue y pruebas**: **ARMOR-DEVOPS** despliega el grafo completo de servicios; **ARMOR-SIMULATOR** reproduce escenarios y fallos repetibles sin hardware real; **ARMOR-HARDWARE** contiene el diseño de la carcasa y su matriz de aceptación en banco.
6. **Operaciones del ecosistema**: **ARMOR-UPDATER** descubre, instala y actualiza cada repositorio de A.R.M.O.R. en una máquina, con el mismo diseño atómico por verificación que HYDRA-UMC-UPDATER; **ARMOR-DOCS** es la documentación de arquitectura canónica y la matriz de capacidades. **ARMOR-STUDIO** también puede actualizar los servicios de la máquina central a partir de paquetes firmados con la clave de lanzamiento del ecosistema, verificando cada firma antes de la instalación.

## 🔒 Honestidad y Seguridad

A.R.M.O.R. sigue la misma regla que ya aplica el panel de control propio de HYDRA-UMC: una afirmación solo es real cuando está verificada, y cada repositorio indica claramente qué se ha ejecutado y qué no en hardware real todavía. Actualmente, nada en este ecosistema controla la red eléctrica general ni el acceso físico; los nodos de campo observan e informan, y cualquier capacidad de conmutación futura se diseña y revisa antes de ser habilitada.

## 📁 Catálogo de Proyectos A.R.M.O.R.

|Repositorio|Versión|Descripción|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.8.0.0|Contratos de mensajes, validadores, vectores de conformidad, tipos generados, OpenAPI, lanzador compartido.|
|[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)|0.8.0.7|Firmware de nodo de campo ESP32-S3, descodificadores para LD2450, LD2461 y sensores de presencia, su núcleo probado en host, actualizaciones desde GitHub con barra de progreso y mapa en vivo.|
|[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)|0.6.1|Nodo pasarela solar: el firmware ESP32-S3 y su panel (diez puertos serie), y los protocolos de inversores Voltronic / MPP Solar y baterías Pylontech y ANT-BMS.|
|[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)|0.5.2|Nodo eléctrico: el firmware (dieciséis medidores PZEM en una línea serie, panel web, MQTT), las tramas de los medidores, el mensaje de las lecturas de la red y las reglas de conmutación.|
|[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)|0.5.0|Nodo y panel de alarma: su firmware (zonas cableadas, la sirena, sensores y sirenas Zigbee, panel web en siete idiomas) y las reglas de armado, retrasos, alarma y PIN, probado en un ordenador; sigue vigilando y toma el control de la radio Zigbee cuando el servidor no está presente. Nunca se ha ejecutado en una placa.|
|[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)|0.4.2|Panel táctil para el Waveshare ESP32-S3-Touch-LCD-7C-BOX: el estado del sistema en una pantalla de pared, armar/desarmar/reconocer, voz presionar para hablar (push-to-talk) y la página web de un nodo; el firmware nunca se ha ejecutado en una placa.|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.6|Monitor de red local: los dispositivos en la red de la casa, el estado de internet (y de qué lado está un fallo), qué cambia; solo observa.|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.8.0.9|Estado central (persistido), usuarios, historial de eventos, alarmas, dispositivos, automatizaciones, lecturas solares y eléctricas, red local, servicios del sistema, monitorización de cámaras, cámaras, evidencias, auditoría, actualizaciones de firmware de nodos que deben estar firmadas, avisos de Telegram y Home Assistant, comandos de voz y uso desde fuera de la casa (segundo factor, sesiones que se pueden finalizar, política remota).|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.9|Servicio de vigilancia de movimiento, selección de perfil visual, política de fusión explicable, registro de motores.|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.5|Zonas de cámara, máscaras y reglas de detección (merodeo, un evento por visita); sin modelo de detector todavía.|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.2|Servicio de voz offline: quince comandos en ocho idiomas, los turnos hablados del panel de pared, armado y desarmado confirmados con un token firmado.|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.1.3|Consola de operaciones, alarmas, dispositivos, automatizaciones, usuarios, historial, reglas de alerta, PTZ, mapa de radar, menús solares y eléctricos, red local, servicios del sistema, clima, buscador y configuración de nodos, actualizaciones de firmware de nodos, notificaciones y diseñador de emplazamientos 2D/3D.|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.8|Cliente operador para Android: armar y desarmar, alarmas, dispositivos, radar en vivo, inversores solares y baterías, historial, notificaciones de alarma, asistente para comandos escritos y hablados y configurador de nodos.|
|[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)|0.0.1|Cliente de operador para iPhone: estado, armado, alarmas, paneles de alarma, cámaras y el asistente, en ocho idiomas.|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.7|Diseños de carcasas (la carcasa de esquina para radar; una caja marcada para los nodos solar, eléctrico y de alarma) y matriz de aceptación en banco.|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.9|Topología Compose, instalador de banco de pruebas para el servidor central, copia de seguridad y restauración, perfil TLS, broker MQTT propio, servicios de observación y voz, agente de administración.|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.9|Escenarios y fallos repetibles.|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.7|Detecta, instala y actualiza los repositorios propios del ecosistema (atómico por verificación, sin necesidad de GITHUB\_TOKEN).|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.1.4|Documentación canónica y matriz de capacidades.|

\---

# ⚡ EH3D FABRICATION SUITE

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/EH3D_BANNER.svg" alt="EH3D Fabrication Suite Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Desktop%20%7C%20Embedded-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-C%2B%2B%20%7C%20Python%20%7C%20Qt-orange.svg" alt="Stack">
  <img src="https://img.shields.io/badge/Hardware-HYDRA--UMC%20%7C%20Bungard%20%7C%20ESP32-green.svg" alt="Hardware">
</p>

**EH3D Fabrication Suite** es un ecosistema de software dedicado y multi-repositorio diseñado específicamente para la creación rápida de prototipos de placas de circuito impreso (PCB), preparación de trayectorias CAM, inspección por visión artificial, gestión de Pick \& Place (PnP) y control multi-máquina de CNC/láser. Proporciona interoperabilidad nativa con los nodos de hardware de **HYDRA-UMC** (STM32H7 + Jetson Orin NX + Hailo NPU) junto con una flota de maquinaria de taller que comprende sistemas de fresado industrial (Bungard CCD a través de pasarelas ESP32-S3 RS-232), routers CNC (JuanenCNC) y grabadoras láser de diodo (JuanenLaser).

**Actualizador:** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) detecta, instala y actualiza los repositorios de este ecosistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) lo hace para los cuatro.

<!-- progress:eh3d -->
`\[██░░░░░░░░░░░░░░░░░░] 10%` — Calculado con datos reales: la madurez y la evidencia que cada uno de sus 26 repositorios declara en su propio manifiesto. El hito del 100% es un ecosistema totalmente integrado operando sobre hardware real.
<!-- /progress:eh3d -->

## 🏗️ Cómo Funciona EH3D Fabrication Suite

1. **Gestión Central**: **EH3D-SUITE-LAUNCHER** encuentra los programas de la suite por sus manifiestos, los arranca y gestiona el fichero de proyecto unificado `.eh3dproj`; el descubrimiento de máquinas en la red (HYDRA-UMC y pasarelas ESP32) y la orquestación de las actualizaciones están previstos.
2. **Canalización de Procesamiento CAM**: Herramientas CAD/CAM especializadas gestionan las etapas de fabricación individuales:

   * **EH3D-ISOCAM**: Aislamiento del cobre de capas Gerber con desplazamientos exactos y varias pasadas; el desbaste del cobre y la estrategia Voronoi están previstos.
   * **EH3D-DRILLPRO**: Procesamiento de taladros Excellon/NC, tablas de brocas y ciclos de perforación de agujeros profundos.
   * **EH3D-ROUTEPRO**: Fresado de contornos de placas, creación de pestañas de sujeción (tabs) y estrategias de entrada en rampa.
   * **EH3D-BUNGARD-GUI**: Interfaz moderna para las máquinas Bungard CCD: un lanzador y un visor con las vistas en planta e isométrica del trabajo.
   * **EH3D-LASER-CAM**: Algoritmos de tramado (dithering) de imágenes y modulación vectorial de potencia para corte láser.
   * **EH3D-STENCILCAM**: Procesamiento de máscaras de pasta para la generación de plantillas de pasta de soldadura SMD.
3. **Ejecución y Control en Tiempo Real**: **EH3D-MOTIONCNC** maneja una máquina desde una sola ventana (jog, puesta a cero, ejecución de código G, vista de la trayectoria; hoy sobre una máquina simulada) y es la base de los programas de control de máquina, integrado con **EH3D-SERVER**, que planifica y ejecuta trabajos de taladrado y fresado a través del nodo de la máquina, con **EH3D-AUTOLEVEL** para el sondeo topográfico de altura Z y **EH3D-NODE-HMI-GUI** para el establecimiento de ceros manuales (G54/G55) y desplazamiento (jogging).
4. **Edge AI e Inspección**: **EH3D-VISION-STUDIO** aprovecha la NPU Hailo de HYDRA-UMC para realizar alineación de cámaras en tiempo real, detección automática de marcas fiduciales e inspección de desgaste de herramientas.
5. **Ensamblaje y Datos Auxiliares**: **EH3D-PNP-MANAGER** gestiona las coordenadas de centroides para Pick \& Place y alimentadores, mientras que **EH3D-TOOL-MANAGER** mantiene una base de datos unificada de bancos de herramientas en todos los módulos CAM.

## 📁 Catálogo de Proyectos EH3D Fabrication Suite

### 💠 Control central y clientes del operador
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|Encuentra los programas de la suite por sus manifiestos, los arranca y guarda los proyectos recientes y el fichero de proyecto (.eh3dproj) con el SHA-256 de sus ficheros; la ventana y el descubrimiento de máquinas en la red están previstos.|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.7|Modelo de datos compartido: el contenedor de proyecto .eh3dproj con comprobaciones de integridad, los tipos de telemetría de máquina y la base de firmware que copia cada nodo ESP32.|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.2|Documentación del ecosistema, guías de ensamblaje, especificaciones técnicas de pasarelas y manuales de integración.|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.2|Lectores en Rust para Gerber RS-274X, ficheros de taladrado Excellon y código G (dialectos GRBL, Marlin y PlanetCNC), tolerantes a ficheros dañados.|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.2|Detecta, instala y actualiza los repositorios propios del ecosistema (atómico por verificación, sin necesidad de GITHUB\_TOKEN).|
|[EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER)|0.0.2|Servidor en Rust con interfaz REST y websocket: usuarios, máquinas y trabajos, planificación de taladrado y fresado con las librerías de DRILLPRO y ROUTEPRO, un trabajo a la vez por máquina.|
|[EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)|0.0.2|Cliente web en Rust de EH3D-SERVER.|

### 💠 Proyectos de taladrado, fresado y contorneado:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.8|Reimplementación en Rust del flujo de taladrado del software clásico de DOS para máquinas Bungard CCD: interfaz en modo texto en ocho idiomas, simulador o máquina real.|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.8|Reimplementación en Rust del flujo de fresado del software clásico de DOS para máquinas Bungard CCD, a partir de ficheros de trazado HP-GL: interfaz en modo texto en ocho idiomas, simulador o máquina real.|
|[EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI)|0.1.2|Interfaz moderna para las máquinas Bungard CCD: un lanzador de los programas clásicos de taladrado y fresado y un visor del trabajo sobre la mesa.|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.4|Base común de los programas de control de máquina de EH3D: una ventana que maneja una máquina simulada con jog, puesta a cero, ejecución de código G y vista de la trayectoria, en ocho idiomas.|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|Base de datos compartida de bancos de herramientas que rastrea horas de desgaste, ajustes de corte y avances en todas las herramientas EH3D CAM.|

### 💠 Proyectos láser:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|Aplicación CAM láser para tramado de imágenes, conversión ráster/vector y control dinámico de potencia PWM.|

### 💠 Proyectos CAM:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|Fresado de aislamiento del cobre de una capa Gerber: desplazamientos exactos del cobre, varias pasadas, comprobación de huecos que la herramienta no puede cortar y G-code; la ventana, el desbaste del cobre y la estrategia Voronoi están previstos.|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|Revisa un programa G-code antes de llegar a una máquina: su tiempo con la aceleración de la máquina y alertas por movimientos rápidos al material, movimientos fuera de la mesa, cortes con el husillo parado y cabezales sobre pinzas; la simulación 3D está prevista.|

### 💠 Proyectos Gerber:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|Herramienta de inspección CAM ligera para la alineación de capas Gerber y visualización rápida.|

### 💠 Proyectos Pick&Place:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|Utilidad de conversión de máscaras de pasta que genera trayectorias de corte para la fabricación de plantillas SMD con láser y plotter.|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|Montaje pick and place: ficheros de posiciones de KiCad y CSV, alimentadores y el orden de colocación para un cabezal de una a seis boquillas; la cámara y el control de la máquina están previstos.|

### 💠 Proyectos de nodos:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)|0.0.4|Nodo ESP32-S3 para la caja de una máquina Bungard CCD: el RS-232 de su unidad de control por Ethernet o Wi-Fi, con las lámparas de la máquina y el variador del husillo en la misma placa.|
|[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)|0.0.3|Pantalla táctil de 10,1 pulgadas con un ESP32-P4 que controla una máquina Bungard CCD: las pantallas del programa de escritorio, alertas y órdenes habladas en ocho idiomas y una parada por hardware que no pasa por la pantalla.|
|[EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX)|0.0.5|Nodo ESP32-S3 para el cabezal de taladro de una máquina Bungard CCD: el vídeo de su cámara (OV2640 u OV5640) como cámara IP (RTSP y ONVIF), la altura de la mesa medida con un láser, la velocidad y la temperatura del husillo y una salida de protección.|
|[EH3D-NODE-HMI-GUI](https://github.com/JuanenRac/EH3D-NODE-HMI-GUI)|0.0.1|Controlador manual táctil de 10 pulgadas / móvil de uso general con ESP32-P4/ESP32-C6 para el movimiento en tiempo real (jog), la puesta a cero (G54/G55) y la parada de emergencia.|

### 💠 Proyectos FENIX:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-FENIX-PCB](https://github.com/JuanenRac/EH3D-FENIX-PCB)|0.0.1|Entorno EDA: captura de esquemas, diseño de PCB, herramientas de verificación, simulación de circuitos y módulos especializados para fuentes conmutadas (SMPS) y RF.|
|[EH3D-FENIX-CAD](https://github.com/JuanenRac/EH3D-FENIX-CAD)|0.0.1|CAD mecánico paramétrico centrado en el diseño de carcasas, chasis y disipadores térmicos.|
|[EH3D-DESIGN-VERIFIER](https://github.com/JuanenRac/EH3D-DESIGN-VERIFIER)|0.0.1|Verificador de ingeniería integral para validaciones cruzadas y control de calidad del diseño.|
|[EH3D-VALIDATION-LAB](https://github.com/JuanenRac/EH3D-VALIDATION-LAB)|0.0.1|Entorno de pruebas encargado de gestionar los casos de uso de referencia y las pruebas de regresión del sistema.|
|[EH3D-DESIGN-HISTORY](https://github.com/JuanenRac/EH3D-DESIGN-HISTORY)|0.0.1|Sistema de control de versiones que guarda el historial semántico y la evolución lógica del diseño.|
|[EH3D-PROJECT-PASSPORT](https://github.com/JuanenRac/EH3D-PROJECT-PASSPORT)|0.0.1|Generador del pasaporte técnico almacenable y reproducible para la auditoría completa de un proyecto.|
|[EH3D-COMPONENT-INTELLIGENCE](https://github.com/JuanenRac/EH3D-COMPONENT-INTELLIGENCE)|0.0.1|Base de datos técnica avanzada enriquecida con metadatos sobre componentes electrónicos.|
|[EH3D-MANUFACTURING-PROFILE](https://github.com/JuanenRac/EH3D-MANUFACTURING-PROFILE)|0.0.1|Gestor de perfiles de las capacidades de la maquinaria de cada fábrica y de las restricciones técnicas de los proveedores.|
|[EH3D-THERMAL-LAB](https://github.com/JuanenRac/EH3D-THERMAL-LAB)|0.0.1|Laboratorio de simulación térmica progresiva acoplado directamente al diseño físico.|
|[EH3D-LAB-BRIDGE](https://github.com/JuanenRac/EH3D-LAB-BRIDGE)|0.0.1|Módulo de correlación que sirve de puente directo entre los datos de simulación y las mediciones reales de laboratorio.|
|[EH3D-DESIGN-EXPLORER](https://github.com/JuanenRac/EH3D-DESIGN-EXPLORER)|0.0.1|Entorno de exploración para comparar y analizar alternativas o ramas del diseño.|

### 💠 Proyectos ANDROID/IOS:
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-ANDROID-CONTROL](https://github.com/JuanenRac/EH3D-ANDROID-CONTROL)|0.0.2|Aplicación Android cliente de EH3D-SERVER.|
|[EH3D-IOS-CONTROL](https://github.com/JuanenRac/EH3D-IOS-CONTROL)|0.0.2|Aplicación iOS cliente de EH3D-SERVER.|

### 🛠️ Herramientas complementarias
|Repositorio|Versión|Descripción|
|-|-|-|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|Encuentra marcas fiduciales redondas en una imagen, convierte píxeles en milímetros, corrige la distorsión de la lente y calcula el giro y el desplazamiento de una placa; la cámara en vivo, la red neuronal y la ventana están previstas.|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|Procesador de malla de altura topográfica (sondeo Z) e interpolación de código G para compensación de superficies.|

\---

## 🤝 Contribución

Cada ecosistema es una iniciativa independiente con sus propios proyectos. Cada proyecto cuenta con sus propias directrices de contribución. Por favor, consulta los repositorios individuales para conocer los detalles técnicos.

Las etiquetas de incidencias (issue labels) están estandarizadas en todos los repositorios de HYDRA-UMC a partir de [`.github/labels.yml`](.github/labels.yml) en este mismo repositorio, sincronizadas mediante [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml): edita ese único archivo para cambiar una etiqueta en todas partes a la vez, en lugar de hacerlo manualmente por repositorio. A diferencia del panel de control que se muestra a continuación, esta lista es estática (una matriz real de GitHub Actions, no un descubrimiento dinámico); un repositorio recién añadido también necesita una entrada allí, no solo un archivo real `hydra-umc.project.json`.

Un panel de control de estado en vivo que cubre todos los repositorios públicos de los cuatro ecosistemas —cada uno descubierto por su propio manifiesto (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`, además de `electro-hobby-3d.project.json` para los repositorios multi-ecosistema), leído directamente de la rama predeterminada de cada repositorio sin una lista fija— es regenerado por [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) inmediatamente cuando un proyecto realiza un `push` (el `dashboard-dispatch.yml` propio de cada repositorio) y, como red de seguridad, dos veces por hora, sirviéndose desde `docs/` a través de GitHub Pages: [**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/). Muestra la pila tecnológica, el objetivo de despliegue y la versión actual, una clasificación de madurez real por proyecto (scaffolding / functional / established / production, decidida cada una a partir del CHANGELOG de ese proyecto —ver [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py))--, su rol (API / UI / CLI / firmware / librería / servicio / herramienta), un árbol de familia/padre-hijo y notas por proyecto sobre lo que está implementado hoy en día. [`ecosystem-catalog.json`](ecosystem-catalog.json) enumera dichos ecosistemas y sus manifiestos en un solo lugar, y la compilación del panel rechaza ejecutarse si ambos alguna vez difieren.

## 🧭 Colaboración en GitHub

El [modelo de colaboración de GitHub](docs/GITHUB_COLLABORATION.md) define una única Wiki central, un proyecto de ecosistema, el ámbito de las discusiones, criterios de lanzamiento y el límite de automatización compartido. Las [plantillas de incidencias](.github/ISSUE_TEMPLATE/) y la [plantilla de pull-request](.github/PULL_REQUEST_TEMPLATE.md) mantenidas de manera centralizada hacen que el trabajo de software, validación de hardware y documentación sea rastreable sin duplicar los manuales de los proyectos.

El flujo de trabajo de salud de la comunidad es intencionalmente manual y de prueba (dry-run) por defecto. Una vez que se configura `COMMUNITY\_HEALTH\_SYNC\_TOKEN`, puede copiar únicamente estas plantillas gestionadas a cada repositorio que publique un manifiesto de HYDRA-UMC; nunca elimina una plantilla específica de un proyecto.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licencia GPL-3.0.

