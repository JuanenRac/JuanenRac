<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

# HYDRA-UMC / URTC 生态系统 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  🇨🇳 <b>简体中文</b> |
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

欢迎来到 **HYDRA-UMC 生态系统**——一个覆盖底层实时固件到高层认知 AI 的多层工业机器人平台。本组织托管着众多专门项目，它们协同工作，共同服务于微工厂自动化与集群机器人应用。

---

## 🚀 核心特性与可扩展性

- **多机器人可扩展性**：支持最多 8 台分布式机器人单元（目前支持 3、4、5、6 自由度；未来版本将扩展至 7、8、9 自由度及双机器人架构）。
- **集成本地工作台**：HYDRA-UMC 主控板自带板载 **6 轴本地工作台**，可用于辅助任务，包括副机器人、ATC（自动换刀装置）转塔、传送带同步或 XYZ 工作台龙门架。

---

## 🏗️ 生态系统架构

整个生态系统分为 6 个功能层，共同实现自主、协同、智能的机器人操作：

1.  **执行层**：基于 STM32 的固件（H745/G474），实现亚毫米级精度与高速 FDCAN 驱动。
2.  **智能层**：由 **Hailo-8**（反射式感知）与 **Hailo-10**（认知推理）驱动的边缘 AI。
3.  **协调层**：独立运行的 Node.js 后端与分布式集群编排器。
4.  **接口层**：Web（React）、桌面端（Qt6）、移动端（Kotlin/Flutter）及 DSI 触摸仪表盘。
5.  **虚拟层**：高保真数字孪生引擎（Rust/Bevy），用于安全的物理前验证。
6.  **支持层**：工业 4.0 网关（OPC-UA/MQTT）与大数据预测性维护。

---

## 🛠️ 技术栈与工具

本生态系统采用现代化、高性能技术栈，以保证任务关键级的可靠性：

### 💠 嵌入式与实时系统（执行层）
- **微控制器**：STM32H745（双核 480MHz）、STM32G474（170MHz）、STM32F303。
- **框架**：FreeRTOS（AMP 模式）、CMSIS-DSP、STM32 HAL/LL。
- **协议**：FDCAN（1Mbps/5Mbps）、CAN-OTA、SPI（50MHz 从机 IPC）、I2C、UART。
- **运动学**：S 曲线轨迹规划、实时逆运动学（IK）。

### 🧠 边缘 AI 与感知（智能层）
- **加速器**：Hailo-8（26 TOPS）用于 8 路摄像头视觉，Hailo-10（40 TOPS）用于生成式 AI。
- **模型**：YOLOv10（检测）、OpenVLA（动作）、Whisper（语音）、Llama-3（推理）。
- **节点间通信**：基于 Protobuf 的 gRPC 与高速 SPI-DMA 元数据交换。

### 🌐 后端与协调（协调层）
- **运行时**：Node.js 20+（API）、Rust 1.80+（编排器）、Go（CLI）。
- **基础设施**：Express、Fastify、Socket.io（WebSocket）、gRPC。
- **数据库**：InfluxDB/TimescaleDB（遥测数据）、Redis（状态）、SQLite。

### 💻 仪表盘与用户界面（接口层）
- **Web 端**：React 19、Vite、Three.js（3D 视口）、Tailwind CSS。
- **原生端**：Python 3.12/PySide6（Suite）、Kotlin（Android 原生）、Flutter 3.x（iOS 与 DSI）。

---

## 📋 系统要求

- **计算节点**：Raspberry Pi CM5（4GB+ 内存），配备 NVMe/eMMC 存储。
- **AI 硬件**：Hailo-8/Hailo-10 M.2 模块（Key M）。
- **现场总线**：千兆以太网用于局域网，FDCAN（ISO 11898-1:2015）用于执行器。
- **客户端操作系统**：Android 10+、iOS 15+、Windows 10/11（高 DPI）、Ubuntu 22.04 LTS。

---

## 🔒 工业安全与安全性

- **急停层**：硬线急停回路 + 高优先级 CAN 紧急帧（延迟 <1ms）。
- **AI 安全**：3D 安全区域，检测到人员闯入时自动切断电机扭矩。
- **网络安全**：基于 JWT 的无状态身份验证 + mTLS 保障节点间通信安全。
- **完整性**：非易失性 F-RAM，用于工具生命周期审计与状态恢复。

---

## 🔧 硬件改造：搭建你自己的载板

机器人控制板围绕 **Raspberry Pi CM5** 构建，而 CM5 自带的双 Hirose DF40 连接器拥有固定、官方、公开的引脚定义（源自 Raspberry Pi 官方 CM5 数据手册的 Table 5）——这并非本项目自行定义的内容。这意味着，兼容的第三方载板是一个真实可行的项目，而非逆向工程：

- **从这里开始**：[`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT)——本板实际使用了 CM5 哪些固定引脚（以太网、2 路原生 USB3 SuperSpeed PHY、CM5 侧散热风扇接口）以及原因，按功能从官方引脚表重新整理而成。
- **最简便的切入点**：标准的 **树莓派 40 针 GPIO 排针**（自 2014 年以来未变的同一套 "B+" 布局）在本板上以与任何树莓派完全相同的方式引出——现有的 RPi HAT 扩展板与 GPIO 工具无需修改即可使用。极少数已被本板自身 STM32 通信占用的位置在丝印上有标注，方便你知道该跳过哪些。
- **深入了解**：[`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) 说明了 CM5、STM32H745「运动学大脑」与 STM32G474「机器人控制器」之间的实际通信方式（SPI1 + FDCAN1 + CM7↔CM4 IPC 邮箱）——如果重新设计的载板要与本项目固件保持兼容，就必须保留这一层。
- 每份引脚文档都明确标注是 **CONFIRMED（已确认）**（直接取自官方数据手册表格）还是 **PROPOSED（提议）**（本项目自身的走线选择，衍生载板上完全可以采用不同方案）——在把某个信号分配当作固定不变之前，请先读清楚这行状态标注。

这不是一份手把手的教程（不存在适用于所有场景的唯一「正确」载板方案）——它是一位经验丰富的硬件工程师真正需要的参考资料，让你从一份已验证可靠的引脚图出发，而不是仅凭一份数据手册摸索。

---

## 📁 项目目录

刚接触本生态系统？运行 `./starter-kit.sh`（Windows 上为
`starter-kit.bat`）即可将下表中全部 12 个仓库作为同级目录克隆到同一
文件夹中——这正是本仓库所有跨仓库脚本已经默认采用的标准目录结构。
重复运行是安全的：已经克隆的内容不会被改动。之后，
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
（12 个仓库之一）即可检查版本，并构建/更新任意项目。

### 💠 Core Ecosystem（核心生态 · 主控）
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 面向 STM32H745/G474 的核心运动控制固件，支持 S 曲线运动学。 |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 无头 Node.js API 与 WebSocket 后端，负责机器人编排。 |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 基于 React 的高级 Web 仪表盘，用于 3D 机器人监控与控制。 |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 高性能 Python/Qt 桌面应用，面向工业自动化场景。 |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 专为 7 英寸工业显示屏（CM5）打造的 Flutter 触控界面。 |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 原生 Kotlin 移动应用，支持生物识别登录，用于远程机器人管理。 |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 面向 iOS/iPadOS 的 Flutter 移动应用，支持实时 WebSocket 同步。 |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 图形化 URDF 编辑器，用于校验并推送机器人模型至目录。 |
| [URTC](https://github.com/JuanenRac/URTC) | Universal Robot Tool Controller 固件，支持 25+ 种专用工具。 |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 图形化工具，用于 CAN-OTA 及整芯片 SWD/JTAG 固件更新。 |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 诊断工具，用于通过 CAN 总线实时校验 URTC 工具配置。 |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 基于浏览器 Web Serial 的工具，用于即时硬件测试与分析。 |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 高速感知节点，支持 8 路 USB 3.0 摄像头同时取流。 |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 经过优化的 GStreamer/MediaMTX 管线，用于工业视频转发。 |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 硬件加速 YOLO 模型库，用于 SMD 及元器件质检。 |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 实时 AI 入侵检测，用于保护机器人作业空间。 |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 基于图像的运动学反馈，用于亚毫米级位姿修正。 |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 语义推理节点，用于逻辑任务规划与语音控制。 |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 视觉-语言-动作（VLA）模型实现，用于复杂任务执行。 |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 本地化、隐私优先的 STT/TTS 管线，用于自然语言操作员交互。 |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 基于 LLM 的任务编排器，具备上下文感知的错误恢复能力。 |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 基于 RAG 的 AI 助手，基于技术手册与源代码训练。 |

### 🐝 Orchestration & Swarm（编排与集群）
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 舰队管理器，用于多机器人协同与防碰撞。 |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | PTP（精确时间协议）同步，实现纳秒级机器人同步。 |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 分布式路径优化器，用于共享工作空间内的机器人集群。 |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 基于优先级的任务调度器，用于异构机器人舰队。 |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 高可用监控器，支持任务的透明故障转移。 |

### 🎮 Digital Twin & Simulation（数字孪生与仿真）
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 高保真物理仿真引擎，用于无风险的机器人测试。 |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | URDF 运动链的真实物理仿真（MuJoCo/PhysX）。 |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 硬件在环（HIL）接口，用于真实与虚拟指令的同步。 |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 面向 Vision 节点的训练数据集程序化生成器。 |

### 📊 Data & Analytics（数据与分析）
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 用于海量工业机器人数据的大数据存储。 |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 高吞吐量采集器，用于 CAN、WebSocket 及系统日志。 |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 基于电机振动特征的预测性维护引擎。 |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 面向工厂生产管理的自动化 OEE 与 KPI 生成工具。 |

### 🏭 Industrial Gateway（工业网关）
| 仓库 | 说明 |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 工业 4.0 互操作性网关，对接工厂标准（OPC-UA/MQTT）。 |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 将 HydraState 机器人对象映射为标准 OPC-UA 节点。 |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 遥测数据桥接器，用于 IoT 集成与外部仪表盘。 |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 标准化接口，用于机床与机器人健康监测。 |

### 🛠️ Complementary Tools（配套工具）
| 仓库 | 说明 |
| :--- | :--- |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 智能工具存放架，具备自动预热与生命周期审计功能。 |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 集成热成像与 RGB 摄像头的工具头，用于主动质检。 |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 可穿戴式应急仪表盘，具备触觉安全告警功能。 |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 命令行工具，用于舰队自动化、烧录与 DevOps。 |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 为 Web 仪表盘提供自然语言洞察的 AI 扩展。 |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 跨平台 GUI/CLI 工具，用于检测、安装并手动更新生态系统中的每一个项目。 |

---

## 🤝 贡献指南
本生态系统隶属于一项高科技机器人计划。每个项目都有各自的贡献指南，具体技术细节请参阅各仓库自身文档。

全部 45 个仓库的 Issue 标签均从本仓库的 [`.github/labels.yml`](.github/labels.yml) 统一同步，由 [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) 负责推送——只需修改这一份文件，即可一次性更新所有仓库的标签，无需逐个手动维护。

全部 45 个仓库的实时状态仪表盘（技术栈、部署目标、当前版本——直接从各仓库自身默认分支读取）由 [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) 每日自动生成，并通过 GitHub Pages 从 `docs/` 目录提供访问：**[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**。v3 为每个项目新增了真实的成熟度分类（scaffolding / functional / established / production，每一项都根据该项目自身真实的 CHANGELOG 决定——具体判定标准见[`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)模块自身的文档说明），以及其角色（API / UI / CLI / 固件 / 库 / 服务 / 工具）、真实的家族/父子关系树，以及每个项目关于当前实际实现内容的说明。

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.
