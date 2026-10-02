<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Electro Hobby 3D 横幅" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

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
  <img src="https://img.shields.io/badge/生态系统-3-00E5FF.svg" alt="三个生态系统">
</p>

三个独立的工程生态系统，同一个作者。**HYDRA-UMC** 是一个多层的工业机器人平台，从底层实时固件到高层认知 AI。**URTC** 是它的通用机器人工具子系统：为机器人末端执行器提供的实时固件和桌面/网页工具，作为独立产品开发，拥有自己的版本和维护体系。**A.R.M.O.R.** 是一个完全独立的公开生态系统，用于周界安防与家庭自动化——雷达存在检测、太阳能与电力监测，以及带网页和移动客户端的中央协调器。

---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

欢迎来到 **HYDRA-UMC 生态系统**——一个覆盖底层实时固件到高层认知 AI 的多层工业机器人平台。本组织托管着众多专门项目，它们协同工作，共同服务于微工厂自动化与集群机器人应用。

## 📈 生态系统进度

`[██████████▊░░░░░░░░░] 54%` —— 仅作参考。100% 里程碑是完整集成并在真实硬件上运行的生态系统。

> [!IMPORTANT]
> 🛠️ **项目暂停——正在搭建真实硬件。** 当前开发工作暂停，团队正在真正搭建物理单元(机架、布线、真实的 CM5 和 STM32 板卡)，这样下一阶段的开发才有真实硬件可以运行和验证，而不只是一条不断上升的进度条。搭建完成后即恢复开发。

---

## 🚀 核心特性与可扩展性

- **多机器人可扩展性**：支持最多 8 台分布式机器人单元（目前支持 3、4、5、6 自由度；未来版本将扩展至 7、8、9 自由度及双机器人架构）。
- **集成本地工作台**：HYDRA-UMC 主控板自带板载 **6 轴本地工作台**，可用于辅助任务，包括副机器人、ATC（自动换刀装置）转塔、传送带同步或 XYZ 工作台龙门架。

---

## 🏗️ 生态系统架构

v1.1 生态系统是一套分层产品平台：它建立在成熟的 Linux 与 Raspberry Pi 技术之上，不重新开发操作系统，也不替代厂商 API。

1.  **平台基础**：Raspberry Pi OS ARM64 与标准 Linux 服务构成受支持的 CM5 基础。
2.  **平台与契约**：**HYDRA-UMC-OS** 在 Raspberry Pi OS 上提供可复现的配置文件、服务、诊断与更新；**HYDRA-UMC-SDK** 发布版本化契约、轻量客户端和一致性测试。
3.  **实时执行**：运行于 STM32/MCU 的 **HYDRA-UMC** 固件和 URTC 保有运动限制、看门狗与安全停止权。
4.  **协调与运维**：服务器服务、任务分发、遥测与配置负责协调设备，且不会绕过 MCU 的安全边界。
5.  **操作员界面**：Studio、Suite、DSI、Web、桌面、移动端和 CLI 均使用 SDK 契约。
6.  **感知与智能**：视觉、Hailo 与认知服务提出观测或计划；它们不具备物理安全权限。
7.  **工程、工业与数据**：数字孪生、HIL/物理、OPC-UA/MQTT/MTConnect 网关和数据服务用于验证和集成系统。

开发应从 **HYDRA-UMC-OS** 的公共架构与服务模型开始，再使用 **HYDRA-UMC-SDK** 的契约和一致性规则。所有流程都保留 MCU/URTC 的安全权限。

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

## 📁 项目目录 — HYDRA-UMC

刚接触本生态系统？运行 `./starter-kit.sh`（Windows 上为
`starter-kit.bat`）即可将 13 个核心仓库——一份手工挑选的起步集合，
并非下方的完整目录——作为同级目录克隆到同一文件夹中：这正是本仓库
所有跨仓库脚本已经默认采用的标准目录结构。重复运行是安全的：已经
克隆的内容不会被改动。之后，
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
（刚刚克隆的 13 个仓库之一）即可检查版本，并构建/更新下方完整目录中
的其他任意项目。

### 🧱 平台基础与契约
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.4.7 | 面向 CM5 的 Raspberry Pi OS 平台层：可复现配置、诊断、服务生命周期与更新；并非新的 Linux 发行版。 |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.2.8 | 面向服务、界面、CM5 适配器和 URTC 的共享版本化契约、轻量客户端与一致性测试；不替代厂商 API。 |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.0 | 面向外部机器连接器的声明式适配器清单注册与校验工具；把 SDK 自身的契约理念扩展到外部机器，而不取代工业网关类项目。 |

### 💠 核心控制与操作员客户端
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.1.6 | 面向 STM32H745/G474 的核心运动控制固件，支持 S 曲线运动学。 |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.0.5 | 无头 Node.js API 与 WebSocket 后端，负责机器人编排。 |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.7.6 | 基于 React 的高级 Web 仪表盘，用于 3D 机器人监控与控制。 |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.4 | 高性能 Python/Qt 桌面应用，面向工业自动化场景。 |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.0 | 专为 7 英寸工业显示屏（CM5）打造的 Flutter 触控界面。 |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.6.3 | 原生 Kotlin 移动应用，支持生物识别登录，用于远程机器人管理。 |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.0 | 面向 iOS/iPadOS 的 Flutter 移动应用，支持实时 WebSocket 同步。 |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.0 | 图形化 URDF 编辑器，用于校验并推送机器人模型至目录。 |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.2 | 桌面 STL 模型编辑器 - 在共享模型目录中变换、替换、移除和添加真实部件。 |


### 👁️ Vision AI Node (Hailo-8 Optimized)
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.0 | 高速感知节点，支持 8 路 USB 3.0 摄像头同时取流。 |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.1.6 | 经过优化的 GStreamer/MediaMTX 管线，用于工业视频转发。 |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.0.9 | 硬件加速 YOLO 模型库，用于 SMD 及元器件质检。 |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.1 | 实时 AI 入侵检测，用于保护机器人作业空间。 |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.4 | 基于图像的运动学反馈，用于亚毫米级位姿修正。 |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.1 | 语义推理节点，用于逻辑任务规划与语音控制。 |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.4 | 视觉-语言-动作（VLA）模型实现，用于复杂任务执行。 |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.3 | 本地化、隐私优先的 STT/TTS 管线，用于自然语言操作员交互。 |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.0 | 基于 LLM 的任务编排器，具备上下文感知的错误恢复能力。 |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.0 | 基于 RAG 的 AI 助手，基于技术手册与源代码训练。 |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.2 | 由策略限权的本地 AI 技术员：目前是固定的风险等级策略与工具白名单，具备真实且经过测试的防御，证明恶意的被检索文档永远无法触发工具调用或泄露密钥——AI 永远不会因生成一段回复而获得权限。 |

### 🐝 编排与集群（编排与集群）
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.3 | 舰队管理器，用于多机器人协同与防碰撞。 |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.1 | PTP（精确时间协议）同步，实现纳秒级机器人同步。 |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.0.7 | 分布式路径优化器，用于共享工作空间内的机器人集群。 |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.1.8 | 基于优先级的任务调度器，用于异构机器人舰队。 |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.4 | 高可用监控器，支持任务的透明故障转移。 |

### 🎮 数字孪生与仿真（数字孪生与仿真）
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.7 | 高保真物理仿真引擎，用于无风险的机器人测试。 |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.6 | URDF 运动链的真实物理仿真（MuJoCo/PhysX）。 |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.6 | 硬件在环（HIL）接口，用于真实与虚拟指令的同步。 |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.0.8 | 面向 Vision 节点的训练数据集程序化生成器。 |

### 📊 数据与分析（数据与分析）
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.3 | 用于海量工业机器人数据的大数据存储。 |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.4 | 高吞吐量采集器，用于 CAN、WebSocket 及系统日志。 |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.3 | 基于电机振动特征的预测性维护引擎。 |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.2 | 面向工厂生产管理的自动化 OEE 与 KPI 生成工具。 |

### 🏭 工业网关（工业网关）
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.2 | 工业 4.0 互操作性网关，对接工厂标准（OPC-UA/MQTT）。 |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.5 | 将 HydraState 机器人对象映射为标准 OPC-UA 节点。 |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.2 | 遥测数据桥接器，用于 IoT 集成与外部仪表盘。 |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.4 | 标准化接口，用于机床与机器人健康监测。 |

### 🌉 外部自动化桥接器
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.0.7 | 双向 ROS 2 协调边界：主题用于观测，服务用于检查，可取消动作用于单元任务。 |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.4 | 面向 OpenPnP 及机器人辅助上下料的可追溯 PCB 交接协调器。 |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.3 | 围绕 3D 打印软件的安全桥接器；首个适配器验证 Moonraker 就绪状态而不替换固件。 |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.4 | CNC 单元辅助协调器；轨迹和安全性仍由原生控制器负责。 |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.2 | 激光单元辅助协调器，不能解锁、发射或绕过激光互锁。 |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.0.8 | 面向腿式/仿人机器人的协调边界：通过共享安全契约校验的行走/抓取/放置动作词表，步态与平衡控制仍由机器人自身控制器负责。 |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.0.8 | 面向AGV/AMR车队的协调边界：从工厂坐标系到AMR本地坐标系的变换，加上受VDA-5050启发的订单动作词表，路径规划仍由AMR自身导航负责。 |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.0.9 | 面向搭载摄像头的无人机的协调边界：命名飞行请求词表，加上确定性的心跳/失联故障保护看门狗。 |

### 🛠️ 配套工具（配套工具）
| 仓库 | 版本 | 说明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.2 | 可穿戴式应急仪表盘，具备触觉安全告警功能。 |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.2 | 命令行工具，用于舰队自动化、烧录与 DevOps。 |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.1 | 为 Web 仪表盘提供自然语言洞察的 AI 扩展。 |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.3 | 跨平台 GUI/CLI 工具，用于检测、安装并手动更新生态系统中的每一个项目。 |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.2.7 | 构建即刻可烧录、预装生态系统最新版本的 CM5 镜像的 Windows/Linux 桌面工具，具备 Raspberry Pi Imager 风格的首次启动配置。 |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.4 | 维护事件协调器：一个低权限的边缘角色采集经过脱敏的库存/健康快照，一个控制面角色以只读方式渲染它，并请求某个 AI 提供方给出诊断建议——从不应用补丁，也从不部署任何内容。 |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.3 | 可复现的开发服务器：目前是一套具有权限控制的配置模式和清单库存，正逐步发展为与 OPS-AGENT 协同的隔离任务/工作区执行器——除非文档明确授予，否则任何任务都没有部署权限。 |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="URTC 生态系统横幅" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/平台-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/总线-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/工具-25%2B%E7%A7%8D%E9%85%8D%E7%BD%AE-blueviolet.svg" alt="Tools">
</p>

**URTC（通用机器人工具控制器）**是一个独立的产品，而不是 HYDRA-UMC 的子系统文件夹：为机器人末端执行器提供的实时固件，以及一整套桌面/网页工具，独立开发、独立发布版本、独立维护。配备 URTC 的换刀器通过 FDCAN 与 HYDRA-UMC 的单元控制器协调，但工具自身的实时行为、看门狗和安全状态是 URTC 自己的权限——单元控制器无法绕过它，URTC 的开发、烧录或诊断也不依赖 HYDRA-UMC。

## 🏗️ URTC 的工作原理

1. **工具固件**：URTC 自己的 STM32 固件运行 25 种以上专用工具配置文件中的每一种（夹爪、点胶器、探头、主轴等），每种都有自己的时序、限值和故障行为。
2. **现场更新**：CAN-OTA 通过工具已在使用的同一条 CAN 总线推送新的固件镜像，并以完整芯片级 SWD/JTAG（URTC-FLASHER）作为后备通道，永远不依赖工具自身固件是否存活。
3. **实时诊断**：URTC-TESTER 在不需要完整工作台的情况下，对照声明的配置文件校验工具的实时 CAN 行为；URTC-WEB-STUDIO 通过 Web Serial 在浏览器标签页里做同样的事，无需安装任何东西。
4. **存储与生命周期**：URTC-SMART-RACK 在工作之间存放工具，在交接前预热工具，并按每个物理工具（而非工具型号）维护生命周期审计记录（循环次数、故障、上次校准）。
5. **主动质检**：URTC-VISION-TOOL 本身就是一种工具——一个带有自己热成像与 RGB 摄像头的工具头，用于过程中的质量检查，而不是拧在另一个工具上的外接摄像头。

## 🛠️ 技术栈

- **固件**：STM32、FDCAN（与单元控制器共用总线）、CAN-OTA、SWD/JTAG 后备通道。
- **桌面工具**：用于烧录和诊断的跨平台 GUI 客户端（URTC-FLASHER、URTC-TESTER）。
- **浏览器工具**：通过 Web Serial API 实现零安装的硬件测试（URTC-WEB-STUDIO）。
- **生命周期数据**：按工具存储的非易失性审计记录，采用与 HYDRA-UMC 相同的 F-RAM 完整性方案。

## 🔒 安全

每个工具配置文件都携带自己的看门狗和故障行为，独立于单元控制器自身的 E-STOP 层——当一个工具失去自己的时间预算或 CAN 心跳时，会自行进入其声明的安全状态，而不是等待外部命令。URTC-SMART-RACK 的预热受其配置文件声明的同一套每工具热限值约束，并记录在同一份生命周期审计中，供车间据此判断一个工具是否仍适合使用。

## 📁 URTC 项目目录

| 仓库 | 版本 | 描述 |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.1 | Universal Robot Tool Controller 固件，支持 25+ 种专用工具。 |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.2.1 | 图形化工具，用于 CAN-OTA 及整芯片 SWD/JTAG 固件更新。 |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.2.2 | 诊断工具，用于通过 CAN 总线实时校验 URTC 工具配置。 |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.2.2 | 基于浏览器 Web Serial 的工具，用于即时硬件测试与分析。 |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.0 | 智能工具存放架，具备自动预热与生命周期审计功能。 |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.0.5 | 集成热成像与 RGB 摄像头的工具头，用于主动质检。 |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="A.R.M.O.R. 生态系统横幅" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/可见性-公开-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R.（Autonomous Radar & Multimodal Observation Range）**是一个完全独立的公开生态系统，用于周界安防与家庭自动化——除了同一作者和相同的工程惯例（有版本的清单、共享的消息契约、七种语言的界面）之外，与 HYDRA-UMC 或 URTC 没有任何关系。它的现场节点监视物业的周界及其太阳能/电力系统；它的中央服务器和客户端让操作员看到并处理这些节点报告的内容。下面的版本和成熟度说明直接来自每个仓库自己的清单和能力矩阵，与 HYDRA-UMC 仪表板已经使用的诚实原则相同。

## 🏗️ A.R.M.O.R. 的构成

1. **共享契约**：**ARMOR-COMMON** 拥有消息含义的所有权——JSON Schema、一个 Python 验证器，以及每个其他仓库只消费、从不重新定义的生成的 TypeScript/Kotlin 类型。
2. **现场节点**：用于雷达/存在检测的 ESP32-S3 固件（**ARMOR-RADAR**）、太阳能逆变器与电池监测（**ARMOR-SOLAR**）、带开关功能的电力计量（**ARMOR-ELECTRICAL**）；一个 Python 代理（**ARMOR-NETWORK**）从已接入房屋本地网络的一台机器上监视这个网络本身及互联网是否可达。
3. **中央协调器**：**ARMOR-SERVER** 保存状态、用户、报警、自动化和摄像头证据；**ARMOR-SERVER-AI** 和 **ARMOR-VOICE-AI** 增加了一个可解释的视觉策略和从不自行执行动作的离线语音意图。
4. **操作员客户端**：**ARMOR-STUDIO**（网页端）和 **ARMOR-ANDROID-CONTROL**（移动端）都是中央服务器的客户端，从不直接对接现场网络。 **ARMOR-HMI** 是挂在墙上的触摸面板（Waveshare ESP32-S3-Touch-LCD-7C-BOX），显示状态、布防和确认，并将成为语音助手的所在。
5. **部署与测试**：**ARMOR-DEVOPS** 部署整个服务图；**ARMOR-SIMULATOR** 在没有真实硬件的情况下回放场景和可重复的故障；**ARMOR-HARDWARE** 负责外壳设计及其台架验收矩阵。
6. **生态系统运维**：**ARMOR-UPDATER** 在一台机器上发现、安装并更新每一个 A.R.M.O.R. 仓库，采用与 HYDRA-UMC-UPDATER 相同的以验证为准的原子化设计；**ARMOR-DOCS** 是权威的架构文档和能力矩阵。

## 🔒 诚实与安全

A.R.M.O.R. 遵循与 HYDRA-UMC 仪表板相同的规则：只有经过验证的说法才是真实的，每个仓库都清楚地说明目前哪些已经在真实硬件上运行过、哪些还没有。这个生态系统目前不控制市电或物理门禁；现场节点只观察和报告，任何未来的开关能力都会先设计和审查，再决定是否启用。

## 📁 A.R.M.O.R. 项目目录

| 仓库 | 版本 | 描述 |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.3.4 | 消息契约、验证器、一致性向量和生成的类型 |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.4.5 | 适用于 ESP32-S3 的现场节点固件，带三个雷达和自带网页面板 |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.1.9 | 太阳能逆变器与电池的协议，以及网关节点的消息 |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.1.5 | 电气节点：电表、电网读数消息和开关规则 |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.0.9 | 适用于 Waveshare ESP32-S3-Touch-LCD-7C-BOX 的触摸面板：墙面屏幕上的系统状态、布防/撤防/确认、按键说话语音以及节点网页；固件从未在开发板上运行。 |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.0.6 | 本地网络：其设备、互联网以及变化 |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.4.1 | 中央协调器：遥测、报警、设备、太阳能与电气读数、本地网络、系统服务和摄像头 |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.1 | 会解释决策且从不执行动作的视觉推理策略 |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.2.1 | 带无法伪造确认的离线语音意图 |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.6.0 | 网页控制台：摄像头、雷达、报警、太阳能与电气菜单、本地网络、系统服务、天气、节点查找器和 2D/3D 场地设计器 |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.4.0 | 带实时 2D/3D 雷达的 Android 操作员客户端 |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.3 | 外壳、电子器件和台架验收矩阵 |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.3.6 | 部署、中央服务器测试台、备份与 TLS |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.3 | 带可重复故障的离线遥测模拟器 |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.0.4 | 发现、安装并更新生态系统自身的仓库 |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.5.5 | 架构、安全基线和能力矩阵 |

---

## 🤝 贡献指南
本生态系统隶属于一项高科技机器人计划。每个项目都有各自的贡献指南，具体技术细节请参阅各仓库自身文档。

生态系统内所有仓库的 Issue 标签均从本仓库的 [`.github/labels.yml`](.github/labels.yml) 统一同步，由 [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) 负责推送——只需修改这一份文件，即可一次性更新所有仓库的标签，无需逐个手动维护。与下方的仪表盘不同，这份列表是静态的（一个真实的 GitHub Actions 矩阵，而非动态发现）——新增仓库也需要在其中添加一条记录，仅有真实的 `hydra-umc.project.json` 是不够的。

覆盖每一个在自身 `hydra-umc.project.json` 中声明 `ecosystem: HYDRA-UMC` 的公开仓库的实时状态仪表盘（技术栈、部署目标、当前版本——直接从各仓库自身默认分支读取，动态发现、无固定列表）由 [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) 每小时自动重新生成（并在相关推送后立即触发），并通过 GitHub Pages 从 `docs/` 目录提供访问：**[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**。它为每个项目新增了真实的成熟度分类（scaffolding / functional / established / production，每一项都根据该项目自身真实的 CHANGELOG 决定——具体判定标准见[`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)模块自身的文档说明），以及其角色（API / UI / CLI / 固件 / 库 / 服务 / 工具）、真实的家族/父子关系树，以及每个项目关于当前实际实现内容的说明。URTC 和 A.R.M.O.R. 自身的仓库在同一个仪表盘上以和 HYDRA-UMC 完全相同的方式被实时发现（见 `scripts/generate_dashboard.py`），各自在自己的 `urtc.project.json`/`armor.project.json` 中声明自己的 `ecosystem` 字段——三者都没有固定列表。

## 🧭 GitHub 协作

[GitHub 协作模型](docs/GITHUB_COLLABORATION.md)定义了一个中央 Wiki、一个生态系统 Project、Discussions 的使用范围、Release 标准及共享自动化边界。中央[Issue 表单](.github/ISSUE_TEMPLATE/)和[Pull Request 模板](.github/PULL_REQUEST_TEMPLATE.md)让软件、硬件验证和文档工作可追溯，同时不复制各项目的技术手册。

社区健康工作流仅手动运行，默认采用 dry-run。配置 `COMMUNITY_HEALTH_SYNC_TOKEN` 后，它只会将这些受管理模板复制到发布 HYDRA-UMC 清单的仓库；绝不会删除项目专用模板。
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.

