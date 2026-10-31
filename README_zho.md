<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Electro Hobby 3D Banner" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  🇺🇸 <a href="README.md">English</a> |
  <a href="README\_spa.md">🇪🇸 Español</a> |
  <a href="README\_fra.md">🇫🇷 Français</a> |
  <a href="README\_ita.md">🇮🇹 Italiano</a> |
  <a href="README\_deu.md">🇩🇪 Deutsch</a> |
  <b>🇨🇳 简体中文</b> |
  <a href="README\_jpn.md">🇯🇵 日本語</a> |
  <a href="README\_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

四个独立的工程生态系统，出自同一位作者。**HYDRA-UMC** 是一个多层工业机器人平台，涵盖从实时固件到认知 AI 的全栈技术。**URTC** 是其通用的机器人工具子系统：专为机器人的末端执行器开发的实时固件和桌面/Web 工具，作为独立产品开发，拥有独立版本控制和维护工具。**A.R.M.O.R.** 是一个独立且公开的周界安全与家庭自动化生态系统——雷达存在检测、太阳能与电力监测，以及带有网页端和移动端客户端的中央协调器。**EH3D Fabrication Suite** 是一个集成的软件生态系统，用于 PCB 原型制作、CAM 处理、计算机视觉检测、贴片机（Pick \& Place）管理以及与 HYDRA-UMC 硬件和专用车间机械对接的 CNC/激光控制。


## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 仪表板与监控 | 🟢 | 状态仪表板、CI 监控、健康矩阵、链接检查和发布摘要都在 GitHub Actions 中定时运行，最近一次运行均已通过。 |
| 测试 | 🟢 | 59 项测试通过（`python -m unittest discover -s tests`）：目录、监控、横幅、四个看板（HYDRA-UMC、URTC、A.R.M.O.R. 和 EH3D）的路线图初始化和 README 一致性。 |
| 目录与版本 | 🟡 | 每张项目表的版本列由脚本根据各仓库自己的清单填写并检查，因此不会过时；一行说明则是手写的。 |
| 进度条 | 🟢 | 每个生态系统的百分比由 `scripts/ecosystem_progress.py` 根据各仓库在自己的清单中声明的成熟度和验证依据计算，并随仪表盘一起刷新；100% 的里程碑仍然是一个完全集成并在真实硬件上运行的生态系统。 |
| 八种语言一致性 | 🟢 | 八份 README 保持相同的章节、相同的 GitHub 链接和相同的表格行数，其中任何一份偏离时测试都会失败。 |
| 真实硬件 | 🟢 | 不适用：本仓库保存的是个人主页及其自动化，没有任何部分在硬件上运行。 |
| 文档 | 🟢 | 八种语言的 README，介绍四个生态系统，并附有 GitHub 协作指南和社区文件。 |

## 🧭 关于 Electro Hobby 3D 及其更新器

**Electro Hobby 3D** 是 JuanenRac 的工坊：电子、机器人和软件都在同一个地方设计、制造、编程和测试。每个仓库都用清单描述自己，带有自己的文档，并说明哪些在真实硬件上试过、哪些没有。

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) 是**四个生态系统的更新器**：一个窗口和一个命令行，把工作交给各个生态系统自己的更新器，由后者发现、安装和更新其仓库。下面的每个生态系统都会点明自己的更新器。

| 生态系统 | 是什么 | 更新器 |
|---|---|---|
| **HYDRA-UMC** | 工业机器人与机器控制，从实时固件到认知 AI | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | 机器人末端执行器的固件与工具 | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | 周界安防与家庭自动化 | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | PCB 原型制作、CAM、CNC 与激光、贴片 | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

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

欢迎来到 **HYDRA-UMC 生态系统**，这是一个多层工业机器人平台，跨越了从底层实时固件到高层认知 AI 的各个领域。该组织托管了许多专门的项目，旨在完美协同工作，以实现微型工厂自动化和群集机器人技术。

**更新器：** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) 检测、安装并更新该生态系统的仓库；[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) 则对全部四个生态系统这样做。

## 📈 生态系统进展

<!-- progress:hydra-umc -->
`\[█████████▎░░░░░░░░░░] 46%` — 根据真实数据计算：其 56 个仓库各自在自己的清单中声明的成熟度和验证依据。100% 的里程碑是一个完全集成并在真实硬件上运行的生态系统。
<!-- /progress:hydra-umc -->

> \[!IMPORTANT]
> 🛠️ \*\*项目暂缓 — 正在构建真实硬件。\*\* 活跃开发已暂时搁置，同时正在切实构建物理机器人单元（框架、接线、真实的 CM5 和 STM32 板），以便下一阶段的工作有实际的硬件可供运行和验证，而不仅仅是一个上升的进度条。一旦该构建到位，工作将重新恢复。

\---

## 🚀 核心特性与可扩展性

* **多机器人可扩展性**：支持最多 8 个分布式机器人单元（目前支持 3、4、5 和 6 自由度；未来版本将扩展到 7、8、9 自由度以及双机器人架构）。
* **集成局部工作台**：主 HYDRA-UMC 板集成了板载 **6 轴局部工作台**，用于辅助任务，包括辅助机器人、ATC（自动换刀）转盘、传送带同步或 XYZ 表格龙门架。

\---

## 🏗️ 生态系统架构

v1.1 生态系统是一个分层的产品平台：它构建在成熟的 Linux 和 Raspberry Pi 技术之上，而不是创建一个新的操作系统或替代供应商的 API。

1. **平台基础**：Raspberry Pi OS ARM64 和标准的 Linux 服务提供了受支持的 CM5 基础。
2. **平台与契约**：**HYDRA-UMC-OS** 在 Raspberry Pi OS 上打包了可重现的配置文件、服务、诊断和更新；**HYDRA-UMC-SDK** 发布了版本化的契约、瘦客户端和一致性夹具（conformance fixtures）。
3. **实时执行**：**HYDRA-UMC** 固件在 STM32/MCU 上管理运动限制、看门狗和安全停止；工具本身及其对末端执行器的实时控制权属于下方独立的 **URTC** 生态系统。
4. **协调与运维**：服务器服务、任务调度、遥测和配置在不绕过 MCU 安全边界的情况下协调设备。
5. **操作员界面**：Studio、Suite、DSI、Web、桌面、移动和 CLI 客户端均使用 SDK 契约。
6. **感知与智能**：视觉、Hailo 和认知服务提出观察结果或计划；它们不具有物理安全权限。
7. **工程、工业与数据**：数字孪生（Digital Twin）、HIL/物理引擎、OPC-UA/MQTT/MTConnect 网关和数据服务验证并集成系统。

有关实现指导，请从 **HYDRA-UMC-OS** 中的公共架构和服务文档开始，然后使用 **HYDRA-UMC-SDK** 中的契约和一致性规则。MCU 的安全权限在每个流程中都得到严格维护。

\---

## 🛠️ 技术栈与工具

该生态系统利用了现代的高性能技术栈，以确保关键任务的可靠性：

### 💠 嵌入式与实时（执行层）

* **微控制器**：STM32H745（双核 480MHz）、STM32G474（170MHz）、STM32F303。
* **框架**：FreeRTOS（AMP 模式）、CMSIS-DSP、STM32 HAL/LL。
* **协议**：FDCAN (1Mbps/5Mbps)、CAN-OTA、SPI（50MHz 从机 IPC）、I2C、UART。
* **运动学**：S曲线配置文件生成、实时逆运动学（IK）。

### 🧠 边缘 AI 与感知（智能层）

* **加速器**：Hailo-8（26 TOPS，用于 8 路摄像头视觉）、Hailo-10（40 TOPS，用于生成式 AI）。
* **模型**：YOLOv10（检测）、OpenVLA（动作）、Whisper（语音）、Llama-3（推理）。
* **节点间通信**：基于 Protobuf 的 gRPC 和高速 SPI-DMA 元数据交换。

### 🌐 后端与协调（协调层）

* **运行时**：Node.js 20+ (API)、Rust 1.80+ (编排器)、Go (CLI)。
* **基础设施**：Express、Fastify、Socket.io (WebSocket)、gRPC。
* **数据库**：InfluxDB/TimescaleDB (遥测)、Redis (状态)、SQLite。

### 💻 仪表板与用户界面（交互层）

* **Web 端**：React 19、Vite、Three.js (3D 视口)、Tailwind CSS。
* **原生端**：Python 3.12/PySide6 (Suite)、Kotlin (Android 原生)、Flutter 3.x (iOS \& DSI)。

\---

## 📋 系统要求

* **计算节点**：配有 NVMe/eMMC 存储的 Raspberry Pi CM5（4GB+ RAM）。
* **AI 硬件**：Hailo-8/Hailo-10 M.2 模块（Key M）。
* **现场总线**：用于局域网的千兆以太网以及用于执行器的 FDCAN (ISO 11898-1:2015)。
* **客户端操作系统**：Android 10+、iOS 15+、Windows 10/11（高DPI）、Ubuntu 22.04 LTS。

\---

## 🔒 工业安全与保障

* **E-STOP 层**：硬接线紧急停止线路 + 高优先级 CAN 紧急帧（<1ms）。
* **AI 安全**：3D 安全区域，在检测到人类闯入时自动切断电机扭矩。
* **网络安全**：基于 JWT 的无状态认证 + 用于安全节点间流量的 mTLS。
* **完整性**：用于工具生命周期审计和状态恢复的非易失性 F-RAM。

\---

## 🔧 硬件极客：构建您自己的载板（Carrier Board）

机器人控制器板围绕 **Raspberry Pi CM5** 构建，CM5 自身的双 Hirose DF40 连接器是一个固定的、官方的、公开的引脚排列（Raspberry Pi 官方 CM5 数据手册表 5），并非由本项目定义。这意味着兼容的第三方载板是一个切实可行、能够完成的项目，而不是逆向工程练习：

* **从这里开始**：[`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) —— 该板实际使用了哪些 CM5 的固定引脚（以太网、2 个原生的 USB3 SuperSpeed PHY、CM5 侧的冷却风扇接头）以及原因，已根据官方引脚表按功能重新整理。
* **轻松上手的途径**：标准的 **Raspberry Pi 40 引脚 GPIO 接头**（自 2014 年以来保持不变的“B+”布局）在该板上的引出方式与任何 Raspberry Pi 完全相同——现有的 RPi HAT 和 GPIO 工具无需修改即可工作。该板自身的 STM32 链路已经使用的少数几个位置已进行了丝网印刷/注释，以便您知道跳过哪些位置。
* **深入了解**：[`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) 涵盖了 CM5、STM32H745“运动大脑”以及 STM32G474“机器人控制器”之间实际的通信方式（SPI1 + FDCAN1 + CM7↔CM4 IPC 邮箱）——如果要保持与本项目自身固件的兼容性，重新设计载板时必须保留这一层。
* 每个引脚排列文档都清楚地说明它是 **CONFIRMED（已确认）**（直接取自官方数据手册表）还是 **PROPOSED（建议）**（本项目自身的布线选择，在衍生载板上可以采用不同的选择）——在将信号分配视为固定之前，请先阅读该状态行。

这不是一个引导式教程（没有适合每个用例的单一“正确”载板）——它是经验丰富的硬件设计人员需要的基础参考材料，使他们能够从已知良好的引脚图开始，而不是仅依靠数据手册。

\---

## 📁 HYDRA-UMC 项目目录

生态系统新手？执行 `./starter-kit.sh`（或在 Windows 上执行 `starter-kit.bat`）会克隆 13 个核心仓库——一个精心挑选的起始集——作为同一目录下的同级目录：这里每个跨仓库脚本都已经假定的标准布局。第二个 argumento（第二个参数）会通过其清单动态发现并克隆整个生态系统：`hydra-umc`、`urtc`、`armor`、`eh3d` 或 `all`（例如 `./starter-kit.sh \~/work armor`）。重新运行它是安全的：任何已经克隆的内容都不会被触动。从那里开始，每个生态系统的更新程序——或者适用于所有四个的 [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)——可以检查版本并构建/更新任何其他项目。

### 🧱 平台基础与契约

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.5|针对 CM5 的 Raspberry Pi OS 平台层：可重现的配置、配置、诊断、服务生命周期和更新；不是新的 Linux 发行版。|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.4.1|针对服务、UI 和 CM5 适配器的共享版本化契约、瘦客户端和一致性测试夹具；它不会替代供应商的 API。|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.6|外部机器连接器的声明式适配器清单注册表和验证器；将 SDK 自身的契约概念扩展到外部机器，而无需替换工业网关项目。|

### 💠 核心控制与操作员客户端

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.4|适用于 STM32H745/G474 且带 S 曲线运动学的核心运动控制固件。|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.3|用于机器人编排的无头（Headless）Node.js API 和 WebSocket 后端。|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.3|用于 3D 机器人监控和控制的高级基于 React 的 Web 仪表板。|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.7.3|用于工业自动化的高性能 Python/Qt 桌面应用程序。|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.8|专为 7 英寸工业显示器（CM5）设计的基于 Flutter 的触摸界面。|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.4|带生物识别登录的远程机器人管理原生 Kotlin 移动应用。|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.8|带实时 WebSocket 同步的 iOS/iPadOS 专用 Flutter 移动应用。|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.6|用于验证机器人模型并将其推送到目录中的图形化 URDF 编辑器。|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.8|桌面 STL 模型编辑器——在共享模型目录中转换、替换、移除和添加真实部件。|

### 👁️ 视觉 AI 节点（Hailo-8 优化）

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.7|用于 8 路同时接入的 USB 3.0 相机流的高速感知节点。|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.2|针对工业视频中继优化的 GStreamer/MediaMTX 管道。|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.6|用于 SMD 和元件质量保证（QA）的硬件加速 YOLO 模型库。|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.6|用于机器人工作空间保护的实时 AI 入侵检测。|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.2.1|用于亚毫米级位姿校正的基于图像的运动学反馈。|

### 🧠 认知 AI 节点（Hailo-10 优化）

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.6|用于逻辑任务规划和语音控制的语义推理节点。|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.1.9|用于复杂任务执行的视觉-语言-动作（Vision-Language-Action）模型实现。|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.1.9|用于自然语言操作员交互的本地私有 STT/TTS 管道。|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.5|具有上下文感知错误恢复功能的基于 LLM 的任务编排器。|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.6|经技术手册和源代码训练的基于 RAG 的 AI 助手。|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.8|本地策略门控 AI 维护技师：当前的固定风险级别策略和工具白名单，拥有经实际测试的防御机制，证明恶意检索到的文档绝不会触发工具调用或泄露机密——AI 绝不会通过生成响应来获取权限。|

### 🐝 编排与群控

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.2.0|用于多机器人协调和防碰撞的车队管理器。|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.6|纳秒级机器人同步的 PTP（精时协议）同步。|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.2|共享工作空间机器人群的分布式路径优化器。|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.4|异构机器人车队的基于优先级的任务调度程序。|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.2.0|具备透明任务故障转移的高可用性监视器。|

### 🎮 数字孪生与仿真

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.1.1|用于无风险机器人测试的高保真物理仿真引擎。|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.1.0|URDF 链的真实世界物理仿真（MuJoCo/PhysX）。|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.1.1|用于真实与虚拟命令同步的硬件在环（Hardware-in-the-loop）接口。|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.2|视觉节点训练数据集的过程生成器。|

### 📊 数据与分析

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.2.0|用于海量工业机器人数据的大数据存储。|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.9|用于 CAN、WebSocket 和系统日志的高吞吐量摄取器。|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.1.9|基于电机振动特征的预测性维护引擎。|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.7|用于工业工厂管理的自动化 OEE 和 KPI 生成。|

### 🏭 工业网关

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.7|适配工厂标准（OPC-UA/MQTT）的工业 4.0 互操作性桥梁。|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.2.1|将 HydraState 机器人对象映射到标准 OPC-UA 节点。|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.8|用于 IoT 集成和外部仪表板的遥测桥接器。|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.2.0|用于机床和机器人健康监测的标准化接口。|

### 🌉 外部自动化桥接

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.4|双向 ROS 2 协调边界：用于观察的主题、用于检查的服务以及用于单元任务的可取消操作。|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.2.1|适用于 OpenPnP 和机器人辅助上下料的可追溯 PCB 交接协调器。|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.2.0|围绕原生 3D 打印机软件的安全桥接；首个适配器在不替换固件的情况下验证 Moonraker 的就绪状态。|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.2.1|CNC 单元辅助协调器；控制器轨迹和机器安全性保持原生状态。|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.1.9|激光单元辅助协调器，无法对激光联锁进行布防、发射或越权。|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.4|针对足式/人形机器人的协调边界：通过共享安全契约门控的命名走/抓/放动作词汇；步态和平衡保持在机器人自身的控制器上。|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.5|AGV/AMR 车队协调边界：工厂到本地坐标系转换加上受到 VDA-5050 启发的指令词汇；路径规划由 AMR 自身的导航负责。|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.6|配备相机的无人机（UAV）协调边界：命名的飞行请求词汇加上确定性的心跳/链路丢失故障保护看门狗。|

### 🛠️ 辅助工具

|仓库|版本|描述|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.7|具备触觉安全警报的可穿戴紧急仪表板。|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.1.9|用于车队自动化、刷机（flashing）和运维的命令行界面。|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.8|为 Web 仪表板提供自然语言见解的 AI 扩展。|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.5.0|用于检测、安装和手动更新每个生态系统项目的跨平台 GUI/CLI 工具。|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.4|Windows/Linux 桌面工具，构建预加载了生态系统最新版本和 Raspberry-Pi-Imager 风格首次启动配置的可烧录 CM5 镜像。|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.2.0|维护事件协调器：低特权边缘角色收集经过净化的库存/健康快照，控制平面角色将其设为只读并请求 AI 提供商建议诊断——绝不应用补丁或部署任何内容。|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.2.0|可重现的开发主机：当前是受策略门控的配置架构和清单库存，正在发展成为与 OPS-AGENT 协调的隔离任务/工作区运行器——除非文档明确授予，否则任何任务都没有部署权限。|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.6|生态系统的架构、接口、安全基线、能力矩阵以及生成的项目目录，外加比较所有仓库的工具。|

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

**URTC (Universal Robot Tool Controller)** 是一个独立的产品，而不是 HYDRA-UMC 的子系统文件夹：它是针对机器人末端执行器的实时固件及一系列桌面/Web 工具，由独立开发、版本控制和维护。配备 URTC 的换刀装置通过 FDCAN 与 HYDRA-UMC 的单元控制器进行协调，但工具自身的实时行为、看门狗和安全状态属于 URTC 自己的权限——单元控制器无法绕过它，且 URTC 的开发、烧录或诊断也不依赖于 HYDRA-UMC。

**更新器：** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) 检测、安装并更新该生态系统的仓库；[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) 则对全部四个生态系统这样做。

<!-- progress:urtc -->
`\[███████░░░░░░░░░░░░░] 35%` — 根据真实数据计算：其 11 个仓库各自在自己的清单中声明的成熟度和验证依据。100% 的里程碑是一个完全集成并在真实硬件上运行的生态系统。
<!-- /progress:urtc -->

## 🏗️ URTC 的工作原理

1. **工具固件**：URTC 专有的 STM32 固件运行 25 种以上的专用工具配置文件（夹爪、分配器、探针、主轴等），每种工具都有其自己的时序、限制和故障行为。
2. **现场更新**：CAN-OTA 通过工具已经在使用的同一条 CAN 总线推送新的固件镜像，并提供全芯片 SWD/JTAG 路径（URTC-FLASHER）作为后备方案，该方案绝不依赖于工具自身固件的存活状态。
3. **实时诊断**：URTC-TESTER 无需完整的车间设置，即可根据其声明的配置文件验证工具的实时 CAN 行为；URTC-WEB-STUDIO 则通过 Web Serial 从浏览器标签页执行相同的操作，无需安装任何软件。
4. **存储与生命周期**：URTC-SMART-RACK 在作业之间存放工具，在交接前预热工具，并针对每个物理工具（而非工具类型）维护生命周期审计追踪（循环次数、故障、最后校准）。
5. **主动 QA**：URTC-VISION-TOOL 本身就是一个工具——一个带有集成热成像和 RGB 相机的工具头，用于在线质量检查，而不是螺栓固定在其他工具上的外部摄像头。
6. **共享基础**：**URTC-COMMON** 将工具头的 CAN 协议作为数据保存，并带有生成的代码和一致性向量；**URTC-DOCS** 包含架构、安全基线和能力矩阵。 **URTC-DEVTOOLS** 将整个家族共享的仓库工具作为一个带版本的集合保存。

## 🛠️ 技术栈

* **固件**：STM32、FDCAN（与单元控制器共享总线）、CAN-OTA、SWD/JTAG 后备。
* **桌面工具**：用于刷机和诊断的跨平台 GUI 客户端（URTC-FLASHER、URTC-TESTER）。
* **浏览器工具**：用于零安装硬件测试的 Web Serial API（URTC-WEB-STUDIO）。
* **生命周期数据**：非易失性的每个工具审计追踪，与 HYDRA-UMC 自身的 F-RAM 完整性方法共享。

## 🔒 安全性

每个工具配置文件都带有其自己的看门狗和故障行为，独立于单元控制器自身的 E-STOP 层——失去其时间预算或 CAN 心搏（heartbeat）的工具会自行进入其声明的安全状态，而无需等待外部命令。URTC-SMART-RACK 的预热受限于其配置文件所声明的每个工具热限制，并在车间用于决定工具是否仍适合使用的同一生命周期追踪中进行审计。

## 📁 URTC 项目目录

|仓库|版本|描述|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.4.2|适用于 25+ 种专用工具的通用机器人工具控制器固件。|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.4.2|用于 CAN-OTA 和全芯片 SWD/JTAG 固件更新的 GUI 工具。|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.4.3|用于在 CAN 上实时验证 URTC 工具配置文件的诊断工具。|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.3.8|用于即时硬件测试和分析的基于浏览器的 Web Serial 工具。|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.2.2|具备自动预热和生命周期审计功能的智能工具存储。|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.6|集成热成像和 RGB 相机以实现主动 QA 的工具头。|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.1.9|根据自身的清单检测、安装和更新机器上的 URTC 仓库。|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.1.2|URTC 生态系统的架构、接口、安全基线、能力矩阵、CAN 协议研究笔记和生成的项目目录，外加比较所有仓库的工具。|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.1.0|作为数据的工具头 CAN 协议：规范、生成的 C、TypeScript 和 Python 代码、一致性向量以及 Python 传输层。|
|[URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY)|0.0.3|URTC CAN 总线前的网关：允许的标识符列表、速率限制和会话密钥。|
|[URTC-DEVTOOLS](https://github.com/JuanenRac/URTC-DEVTOOLS)|0.0.1|URTC 家族共享的仓库工具，作为一个带版本的集合，每个仓库中有一个锁定文件。|

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

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range)** 是一个独立的公开周界安全与家庭自动化生态系统——除了相同的作者和相同的工程惯例（版本化清单、共享消息契约、八语言接口）外，与 HYDRA-UMC 或 URTC 无关。其现场节点监视物业的周界以及太阳能/电气设施；其中央服务器和客户端允许操作员查看其报告的内容并采取行动。以下版本和成熟度说明直接来自各个仓库自身的清单和能力矩阵，这与 HYDRA-UMC 仪表板已经使用的诚实原则完全一致。

**更新器：** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) 检测、安装并更新该生态系统的仓库；[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) 则对全部四个生态系统这样做。

<!-- progress:armor -->
`\[████████████▍░░░░░░░] 62%` — 根据真实数据计算：其 19 个仓库各自在自己的清单中声明的成熟度和验证依据。100% 的里程碑是一个完全集成并在真实硬件上运行的生态系统。
<!-- /progress:armor -->

## 🏗️ A.R.M.O.R. 是如何构建的

1. **共享契约**：**ARMOR-COMMON** 拥有消息含义——JSON Schema、Python 验证器以及所有其他仓库消费且从不重新定义的生成的 TypeScript/Kotlin 类型。
2. **现场节点**：用于雷达/存在感测的 ESP32-S3 固件（**ARMOR-NODE-RADAR**）、太阳能逆变器和电池监控（**ARMOR-NODE-SOLAR**）、带开关控制的电量计量（**ARMOR-NODE-ELECTRICAL**）以及房屋的报警面板（**ARMOR-NODE-ALARM**）；Python 代理（**ARMOR-NETWORK**）从已连接的机器上监视房屋自身的局域网和互联网连通性。
3. **中央协调器**：**ARMOR-SERVER** 保存状态、用户、警报、自动化和相机证据；**ARMOR-SERVER-AI** 和 **ARMOR-VOICE-AI** 添加了可解释的视觉策略和离线语音意图，这些意图绝不会自行触发任何动作。
4. **操作员客户端**：**ARMOR-STUDIO**（Web 端）和 **ARMOR-ANDROID-CONTROL**（移动端）、**ARMOR-IOS-CONTROL**（iPhone）是中央服务器的客户端，绝不直接连接现场网络。**ARMOR-NODE-HMI** 是墙上的触摸屏面板（Waveshare ESP32-S3-Touch-LCD-7C-BOX），显示系统状态、布防、撤防和确认，并将成为语音助理的驻留地。
5. **部署与测试**：**ARMOR-DEVOPS** 部署整个服务图；**ARMOR-SIMULATOR** 在没有真实硬件的情况下重放场景和可重复的故障；**ARMOR-HARDWARE** 承载外壳设计及其台架验收矩阵。
6. **生态系统运维**：**ARMOR-UPDATER** 在机器上发现、安装和更新每个 A.R.M.O.R. 仓库，采用与 HYDRA-UMC-UPDATER 相同的通过验证实现原子化的设计；**ARMOR-DOCS** 是规范的架构文档和能力矩阵。**ARMOR-STUDIO** 还可以使用生态系统发布密钥签名的软件包更新中央机器上的服务，在安装前检查每个签名。

## 🔒 诚实与安全

A.R.M.O.R. 遵循 HYDRA-UMC 自身仪表板已经应用的相同规则：一项声明只有经过验证才是真实的，每个仓库都明确说明了哪些内容已经在真实硬件上运行过，哪些还没有。目前，该生态系统中的任何组件都不控制市电（mains electricity）或物理访问；现场节点负责观察和报告，任何未来的开关控制能力在启用之前都经过了设计和审查。

## 📁 A.R.M.O.R. 项目目录

|仓库|版本|描述|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.7.8|消息契约、验证器、一致性向量、生成的类型、OpenAPI、共享启动器。|
|[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)|0.8.0.7|ESP32-S3 现场节点固件、LD2450/LD2461 及存在传感器的解码器、其经主机测试的核心、带进度条和实时地图的 GitHub 更新。|
|[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)|0.6.1|太阳能网关节点：ESP32-S3 固件及其面板（十个串口），以及 Voltronic/MPP Solar 逆变器和 Pylontech/ANT-BMS 电池的协议。|
|[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)|0.5.2|电气节点：固件（单个串口上的 16 个 PZEM 电表、Web 面板、MQTT）、电表帧、网络读数消息以及开关切换规则。|
|[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)|0.5.0|报警节点及面板：其固件（有线防区、警报器、Zigbee 传感器及警报器、七种语言的 Web 面板）以及布防、延迟、报警和 PIN 码规则，已在计算机上测试；在服务器离线时继续警戒并接管 Zigbee 无线电。从未在板卡上运行过。|
|[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)|0.4.2|Waveshare ESP32-S3-Touch-LCD-7C-BOX 触摸面板：壁挂屏幕上的系统状态、布防/撤防/确认、一键通（push-to-talk）语音以及节点的网页；该固件从未在板卡上运行过。|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.5|局域网监视器：家中网络上的设备、互联网状态（以及中断归咎于哪一方）、变化情况；仅具备观察功能。|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.8.0.7|中央状态（持久化）、用户、事件历史记录、警报、设备、自动化、太阳能和电气读数、局域网、系统服务、相机看门狗、相机、证据、审计、必须签名的节点固件更新、Telegram 和 Home Assistant 通知、语音命令以及从外部使用（双因素认证、可终止的会话、远程策略）。|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.8|运动监视服务、视觉配置文件选择、可解释的融合策略、引擎注册表。|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.4|相机区域、遮罩和检测规则（徘徊、每次访问一个事件）；暂无检测器模型。|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.2|离线语音服务：八种语言的十五条命令、壁挂面板的语音交互、通过签名令牌确认的布防和撤防。|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.1.1|操作控制台、警报、设备、自动化、用户、历史记录、警报规则、PTZ、雷达地图、太阳能和电气菜单、局域网、系统服务、天气、节点查找器与配置、节点固件更新、通知以及 2D/3D 站点设计器。|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.8|Android 操作员客户端：布防和撤防、警报、设备、实时雷达、太阳能逆变器和电池、历史记录、警报通知、书面和口头命令助手以及节点配置器。|
|[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)|0.0.1|iPhone 操作员客户端：状态、布防、告警、报警面板、摄像头和助理，提供八种语言。|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.7|外壳设计（雷达角落外壳；太阳能、电气和报警节点的勾选框）以及台架验收矩阵。|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.8|Compose 拓扑、中央服务器测试台安装程序、备份与恢复、TLS 配置文件、自有 MQTT 经纪商、观察和语音服务、管理代理。|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.7|场景和可重复故障。|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.6|检测、安装和更新生态系统自身的仓库（通过验证实现原子化，无需 GITHUB\_TOKEN）。|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.1.3|规范文档和能力矩阵。|

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

**EH3D Fabrication Suite** 是一个专门的、多仓库的软件生态系统，专为印制电路板（PCB）快速原型制作、CAM 刀具路径准备、计算机视觉检查、贴片机（PnP）管理以及多机 CNC/激光控制而定制。它提供与 **HYDRA-UMC** 硬件节点（STM32H7 + Jetson Orin NX + Hailo NPU）的原生互操作性，同时拥有一支车间机械车队，包括工业铣削系统（通过 ESP32-S3 RS-232 网关连接的 Bungard CCD）、CNC 雕刻机（JuanenCNC）和二极管激光雕刻机（JuanenLaser）。

**更新器：** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) 检测、安装并更新该生态系统的仓库；[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) 则对全部四个生态系统这样做。

<!-- progress:eh3d -->
`\[██░░░░░░░░░░░░░░░░░░] 10%` — 根据真实数据计算：其 12 个仓库各自在自己的清单中声明的成熟度和验证依据。100% 的里程碑是一个完全集成并在真实硬件上运行的生态系统。
<!-- /progress:eh3d -->

## 🏗️ EH3D Fabrication Suite 的工作原理

1. **中央管理**：**EH3D-SUITE-LAUNCHER** 发现本地网络上的活动硬件节点（HYDRA-UMC 和 ESP32 网关），管理统一的 `.eh3dproj` 软件包，并编排工具更新。
2. **CAM 处理管道**：专用的 CAD/CAM 工具处理各个制造阶段：

   * **EH3D-ISOCAM**：Gerber RS-274X/X2 走线隔离、Voronoi 算法和清除铜箔（rubout）。
   * **EH3D-DRILLPRO**：Excellon/NC 钻孔处理、钻头表和深孔钻孔循环。
   * **EH3D-ROUTEPRO**：板边铣削、夹持凸耳（tab）创建和斜坡切入（ramping entry）策略。
   * **EH3D-BUNGARD-GUI**：Bungard CCD 机器的现代界面：启动器，以及显示作业平面图和等轴测图的查看器。
   * **EH3D-LASER-CAM**：用于激光切割的光栅抖动（dithering）算法和矢量功率调制。
   * **EH3D-STENCILCAM**：用于 SMD 焊膏钢网生成的阻焊膏掩模（pastemask）处理。
3. **执行与实时控制**：**EH3D-MOTIONCNC** 在一个窗口中驱动机器（点动、置零、G 代码运行、路径显示；目前针对模拟机器），是机器控制程序的基础，并与通过机器节点规划和运行钻孔与铣削任务的 **EH3D-SERVER**、用于地形 Z 探测的 **EH3D-AUTOLEVEL** 以及用于手持置零（G54/G55）和慢动微调（jogging）的 **EH3D-NODE-HMI-GUI** 集成。
4. **边缘 AI 与检测**：**EH3D-VISION-STUDIO** 利用 HYDRA-UMC 的 Hailo NPU 执行实时相机对准、自动基准点（fiducial）检测和工具磨损检测。
5. **组装与辅助数据**：**EH3D-PNP-MANAGER** 管理质心贴片（Pick \& Place）坐标和供料器（feeder），而 **EH3D-TOOL-MANAGER** 在所有 CAM 模块中维护统一的刀具库（tool crib）数据库。

## 📁 EH3D Fabrication Suite 项目目录

### 💠 核心控制与操作员客户端
|仓库|版本|描述|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|用于项目管理（.eh3dproj）、更新、全局设置和节点发现的主生态系统仪表板。|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.5|共享数据模型：带完整性校验的 .eh3dproj 项目容器、机器遥测类型，以及每个 ESP32 节点复用的固件基础。|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.2|生态系统文档、组装指南、网关技术规范和集成手册。|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.2|用 Rust 编写的 Gerber RS-274X、Excellon 钻孔文件和 G 代码（GRBL、Marlin 与 PlanetCNC 方言）读取器，可容忍损坏的文件。|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.2|检测、安装和更新生态系统自身的仓库（通过验证实现原子化，无需 GITHUB\_TOKEN）。|
|[EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER)|0.0.1|带有 REST 和 websocket 接口的 Rust 服务器：管理用户、机器和作业，使用 DRILLPRO 和 ROUTEPRO 的库规划钻孔和铣削作业，每台机器同一时间只运行一个作业。|
|[EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)|0.0.2|EH3D-SERVER 的 Rust Web 客户端。|

### 💠 钻孔／铣边／铣削项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.7|用 Rust 重新实现 Bungard CCD 机器经典 DOS 软件的钻孔流程：八种语言的文本模式界面，可用模拟器或真实机器。|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.7|用 Rust 重新实现 Bungard CCD 机器经典 DOS 软件的铣削流程，输入为 HP-GL 绘图文件：八种语言的文本模式界面，可用模拟器或真实机器。|
|[EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI)|0.0.5|Bungard CCD 机器的现代界面：经典钻孔和铣削程序的启动器，以及显示工作台上作业的查看器。|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.4|EH3D 机器控制程序的共享基础：一个驱动模拟机器的窗口，支持点动、置零、G 代码运行和路径显示，提供八种语言。|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|跨所有 EH3D CAM 工具跟踪磨损小时数、切削预设和进给速率的共享刀具库数据库。|

### 💠 激光项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|用于图像抖动、光栅/矢量转换和动态 PWM 功率控制的激光 CAM 应用。|

### 💠 CAM 项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|Gerber RS-274X/X2 CAM 处理应用、Voronoi/偏移走线隔离、rubout 及雕刻仿真。|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|3D 刀具路径与材料去除模拟器、碰撞检测器以及 G-Code/HP-GL 周期时间估计器。|

### 💠 Gerber 项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|用于 Gerber 图层对齐和快速可视化的轻量级 CAM 检查工具。|

### 💠 贴片（Pick&Place）项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|生成用于激光和绘图仪 SMD 钢网制造的切割刀具路径的阻焊膏掩模转换实用程序。|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|受 OpenPnP 启发 SMD 组装管理器、质心读取器、供料器控制和视觉元件居中。|

### 💠 节点项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)|0.0.4|用于 Bungard CCD 机器机箱的 ESP32-S3 节点：通过以太网或 Wi-Fi 访问其控制单元的 RS-232，机器的指示灯和主轴驱动器在同一块板上。|
|[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)|0.0.1|基于 ESP32-P4 的 10.1 英寸触摸屏，用于控制 Bungard CCD 机器：桌面程序的各个界面、八种语言的语音提示与语音指令，以及不经过屏幕的硬件急停。|
|[EH3D-NODE-HMI-GUI](https://github.com/JuanenRac/EH3D-NODE-HMI-GUI)|0.0.1|通用的 ESP32-P4/ESP32-C6 10 英寸触摸屏／移动手动控制器，支持实时点动、归零设置（G54/G55）和急停。|

### 💠 FENIX 项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-FENIX-PCB](https://github.com/JuanenRac/EH3D-FENIX-PCB)|0.0.1|EDA 环境：原理图捕获、PCB 布局、验证工具、电路仿真，以及面向开关电源（SMPS）和射频的专用模块。|
|[EH3D-FENIX-CAD](https://github.com/JuanenRac/EH3D-FENIX-CAD)|0.0.1|专注于外壳、机箱和散热器设计的参数化机械 CAD。|
|[EH3D-DESIGN-VERIFIER](https://github.com/JuanenRac/EH3D-DESIGN-VERIFIER)|0.0.1|用于交叉验证和设计质量控制的综合工程验证器。|
|[EH3D-VALIDATION-LAB](https://github.com/JuanenRac/EH3D-VALIDATION-LAB)|0.0.1|负责管理参考用例和系统回归测试的测试环境。|
|[EH3D-DESIGN-HISTORY](https://github.com/JuanenRac/EH3D-DESIGN-HISTORY)|0.0.1|保存设计语义历史和逻辑演进的版本控制系统。|
|[EH3D-PROJECT-PASSPORT](https://github.com/JuanenRac/EH3D-PROJECT-PASSPORT)|0.0.1|生成可存档、可复现的技术护照，用于项目的完整审计。|
|[EH3D-COMPONENT-INTELLIGENCE](https://github.com/JuanenRac/EH3D-COMPONENT-INTELLIGENCE)|0.0.1|富含电子元器件元数据的高级技术数据库。|
|[EH3D-MANUFACTURING-PROFILE](https://github.com/JuanenRac/EH3D-MANUFACTURING-PROFILE)|0.0.1|管理各工厂机器能力和供应商技术限制的配置文件管理器。|
|[EH3D-THERMAL-LAB](https://github.com/JuanenRac/EH3D-THERMAL-LAB)|0.0.1|与实体设计直接耦合的渐进式热仿真实验室。|
|[EH3D-LAB-BRIDGE](https://github.com/JuanenRac/EH3D-LAB-BRIDGE)|0.0.1|在仿真数据与实际实验室测量之间直接建立桥梁的关联模块。|
|[EH3D-DESIGN-EXPLORER](https://github.com/JuanenRac/EH3D-DESIGN-EXPLORER)|0.0.1|用于比较和分析设计备选方案或分支的探索环境。|

### 💠 ANDROID/IOS 项目：
|仓库|版本|描述|
|-|-|-|
|[EH3D-ANDROID-CONTROL](https://github.com/JuanenRac/EH3D-ANDROID-CONTROL)|0.0.1|EH3D-SERVER 的 Android 应用客户端。|
|[EH3D-IOS-CONTROL](https://github.com/JuanenRac/EH3D-IOS-CONTROL)|0.0.1|EH3D-SERVER 的 iOS 应用客户端。|

### 🛠️ 辅助工具
|仓库|版本|描述|
|-|-|-|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|用于相机对准、基准标记训练以及通过 HYDRA-UMC 进行视觉检查的边缘 AI 视觉仪表板。|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|地形高度网格处理器（Z 探测）和用于表面补偿的 G代码插值。|

\---

## 🤝 贡献 (Contributing)

每个生态系统都是其自身项目的独立倡议。每个项目都有自己的贡献指南。有关技术详情，请参考各个独立的仓库。

Issue 标签在所有 HYDRA-UMC 仓库中都是统一标准化的，其来源是本仓库中的 [`.github/labels.yml`](.github/labels.yml)，并通过 [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) 进行同步——只需修改这单个文件即可同时更改所有地方的标签，而无需在每个仓库中手动修改。与下方的仪表板不同，此列表是静态的（真正的 GitHub Actions 矩阵，而非动态发现）——新添加的仓库不仅需要真实的 `hydra-umc.project.json`，还需要在那里添加一个条目。

一个覆盖四个生态系统所有公共仓库的实时状态仪表板——每个仓库通过其自身的清单（`hydra-umc.project.json`、`urtc.project.json`、`armor.project.json`、`eh3d.project.json`，以及用于跨生态系统仓库的 `electro-hobby-3d.project.json`）被自律发现，直接从每个仓库自身的默认分支读取，没有固定列表——由 [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) 在项目推送时（通过每个仓库自身的 `dashboard-dispatch.yml`）立即重新生成，并且作为安全网每小时运行两次，通过 GitHub Pages 从 `docs/` 提供服务：[**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/)。它展示了技术栈、部署目标和当前版本、每个项目的真实成熟度分类（scaffolding / functional / established / production，每个分类根据该项目自身的 CHANGELOG 决定——参见 [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)）、其角色（API / UI / CLI / 固件 / 库 / 服务 / 工具）、家族/父子树以及关于当前已实现功能的按项目注释。[ecosystem-catalog.json](ecosystem-catalog.json) 在一个地方列出了这些生态系统及其清单，如果两者不一致，仪表板构建将拒绝运行。

## 🧭 GitHub 协作

[GitHub 协作模型](docs/GITHUB_COLLABORATION.md) 定义了一个中央 Wiki、一个生态系统 Project、Discussion 范围、发布标准以及共享的自动化边界。集中维护的 [issue 表单](.github/ISSUE_TEMPLATE/) 和 [PR 模板](.github/PULL_REQUEST_TEMPLATE.md) 使得软件、硬件验证和文档工作具有可追溯性，而无需重复编写项目手册。

社区健康工作流程默认有意设置为手动和乾跑（dry-run）模式。配置 `COMMUNITY\_HEALTH\_SYNC\_TOKEN` 后，它只能将这些受管理的模板复制到发布 HYDRA-UMC 清单的每个仓库中；它绝不会删除特定于项目的模板。

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.

