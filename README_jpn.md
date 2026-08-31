<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="HYDRA-UMC Ecosystem Banner" width="100%">
</p>

# HYDRA-UMC / URTC エコシステム 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  🇯🇵 <b>日本語</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

**HYDRA-UMC エコシステム** へようこそ。これは、低レベルのリアルタイムファームウェアから高度な認知 AI まで幅広くカバーする、多層構造の産業用ロボティクスプラットフォームです。本組織では、マイクロファクトリーの自動化と群制御ロボティクスのために、緊密に連携動作するよう設計された多数の専用プロジェクトをホストしています。

## 📈 エコシステムの進捗

`[█████████▊░░░░░░░░░░] 49%` — 目安です。100% の到達点は、実機上で動作する完全統合済みのエコシステムです。

---

## 🚀 主要機能とスケーラビリティ

- **マルチロボット対応のスケーラビリティ**：最大 8 台の分散ロボットユニットに対応（現時点で 3・4・5・6 自由度をサポート、今後のリリースでは 7・8・9 自由度およびデュアルロボット構成へ拡張予定）。
- **統合ローカルステージ**：HYDRA-UMC メインボードには、副ロボットや ATC（自動工具交換装置）タレット、コンベアベルト同期、XYZ テーブルガントリーなどの補助タスク向けに、オンボードの **6 軸ローカルステージ** を搭載しています。

---

## 🏗️ エコシステムのアーキテクチャ

v1.1 のエコシステムは階層化された製品プラットフォームです。既存の Linux と Raspberry Pi 技術を基盤とし、新しい OS を作ったりベンダー API を置き換えたりしません。

1.  **プラットフォーム基盤**：Raspberry Pi OS ARM64 と標準 Linux サービスが、サポート対象の CM5 基盤を提供します。
2.  **プラットフォームと契約**：**HYDRA-UMC-OS** は Raspberry Pi OS 上で再現可能なプロファイル、サービス、診断、更新を提供し、**HYDRA-UMC-SDK** はバージョン管理された契約、軽量クライアント、適合性テストを公開します。
3.  **リアルタイム実行**：STM32/MCU 上の **HYDRA-UMC** ファームウェアと URTC が、動作制限、ウォッチドッグ、安全停止を保持します。
4.  **協調と運用**：サーバーサービス、ジョブ配信、テレメトリ、設定が、MCU の安全境界を越えずにデバイスを協調させます。
5.  **オペレーターインターフェース**：Studio、Suite、DSI、Web、デスクトップ、モバイル、CLI は SDK 契約を使用します。
6.  **知覚とインテリジェンス**：Vision、Hailo、認知サービスは観測または計画を提案しますが、物理安全の権限は持ちません。
7.  **エンジニアリング、産業、データ**：デジタルツイン、HIL/物理、OPC-UA/MQTT/MTConnect ゲートウェイ、データサービスがシステムを検証・統合します。

開発は **HYDRA-UMC-OS** の公開アーキテクチャとサービスモデルから開始し、その後 **HYDRA-UMC-SDK** の契約と適合性ルールを使用します。すべてのフローで MCU/URTC の安全権限を維持します。

---

## 🛠️ 技術スタックとツール

本エコシステムは、ミッションクリティカルな信頼性を実現するために、最新の高性能スタックを採用しています。

### 💠 組み込み・リアルタイム系（実行層）
- **マイクロコントローラー**：STM32H745（デュアルコア 480MHz）、STM32G474（170MHz）、STM32F303。
- **フレームワーク**：FreeRTOS（AMP モード）、CMSIS-DSP、STM32 HAL/LL。
- **プロトコル**：FDCAN（1Mbps/5Mbps）、CAN-OTA、SPI（50MHz スレーブ IPC）、I2C、UART。
- **運動学**：S カーブプロファイル生成、リアルタイム逆運動学（IK）。

### 🧠 エッジ AI・知覚処理（インテリジェンス層）
- **アクセラレータ**：Hailo-8（26 TOPS）で 8 台同時カメラビジョン処理、Hailo-10（40 TOPS）で生成 AI 処理。
- **モデル**：YOLOv10（検出）、OpenVLA（動作生成）、Whisper（音声認識）、Llama-3（推論）。
- **ノード間通信**：Protobuf を用いた gRPC、および高速 SPI-DMA によるメタデータ交換。

### 🌐 バックエンド・協調系（協調層）
- **ランタイム**：Node.js 20+（API）、Rust 1.80+（オーケストレーター）、Go（CLI）。
- **インフラストラクチャ**：Express、Fastify、Socket.io（WebSocket）、gRPC。
- **データベース**：InfluxDB/TimescaleDB（テレメトリ）、Redis（状態管理）、SQLite。

### 💻 ダッシュボード・ユーザーインターフェース（インターフェース層）
- **Web**：React 19、Vite、Three.js（3D ビューポート）、Tailwind CSS。
- **ネイティブ**：Python 3.12/PySide6（Suite）、Kotlin（Android ネイティブ）、Flutter 3.x（iOS・DSI）。

---

## 📋 システム要件

- **コンピュートノード**：Raspberry Pi CM5（4GB 以上の RAM）、NVMe/eMMC ストレージ搭載。
- **AI ハードウェア**：Hailo-8/Hailo-10 M.2 モジュール（Key M）。
- **フィールドバス**：LAN 用ギガビットイーサネット、アクチュエータ用 FDCAN（ISO 11898-1:2015）。
- **クライアント OS**：Android 10 以降、iOS 15 以降、Windows 10/11（高 DPI 対応）、Ubuntu 22.04 LTS。

---

## 🔒 産業安全・セキュリティ

- **緊急停止（E-STOP）層**：ハードワイヤード緊急停止回路 + 高優先度 CAN 緊急フレーム（1ms 未満）。
- **AI セーフティ**：人の侵入を検知すると自動的にモータートルクを遮断する 3D セーフティゾーン。
- **サイバーセキュリティ**：JWT ベースのステートレス認証 + ノード間通信を保護する mTLS。
- **完全性（インテグリティ）**：工具のライフサイクル監査と状態復旧のための不揮発性 F-RAM。

---

## 🔧 ハードウェアハッキング：独自のキャリアボードを作る

ロボットコントローラーボードは **Raspberry Pi CM5** をベースに構築されており、CM5 自体が備える 2 系統の Hirose DF40 コネクタのピン配置は、固定・公式・公開されたもの（Raspberry Pi 公式 CM5 データシートの Table 5 に準拠）であり、本プロジェクト独自の定義ではありません。つまり、互換性のあるサードパーティ製キャリアボードの製作は、リバースエンジニアリングではなく、実現可能な現実的プロジェクトなのです。

- **まずはここから**：[`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) — 本ボードが実際に使用している CM5 の固定ピン（イーサネット、2 系統のネイティブ USB3 SuperSpeed PHY、CM5 側の冷却ファンヘッダー）とその理由を、公式ピン配置表を機能別に再整理してまとめたものです。
- **手軽な入り口**：標準の **Raspberry Pi 40 ピン GPIO ヘッダー**（2014 年以降変わっていない同一の「B+」レイアウト）は、通常の Raspberry Pi とまったく同様に本ボードから引き出されています。既存の RPi HAT や GPIO ツール類は改造なしでそのまま使用可能です。本ボード自身の STM32 通信がすでに使用しているごく一部のピン位置には、シルク印刷で注記がありますので、避けるべき箇所がひと目でわかります。
- **さらに深く知るには**：[`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) では、CM5、STM32H745「Kinematic Brain（運動学ブレイン）」、STM32G474「Robot Controller（ロボットコントローラー）」が実際にどのように通信しているか（SPI1 + FDCAN1 + CM7↔CM4 の IPC メールボックス）を解説しています。キャリアボードを再設計する際、本プロジェクトのファームウェアとの互換性を保つにはこの層を維持する必要があります。
- 各ピン配置ドキュメントには、そのピン割り当てが **CONFIRMED（確認済み）**（公式データシートの表から直接引用）なのか、**PROPOSED（提案）**（本プロジェクト独自の配線選択であり、派生キャリアボードでは異なる選択も可能）なのかが明記されています——ある信号割り当てを固定のものとみなす前に、必ずこのステータス行を確認してください。

これはガイド付きチュートリアルではありません（すべての用途に当てはまる唯一の「正解」となるキャリアボードは存在しません）——経験豊富なハードウェア設計者が、データシートだけを頼りにするのではなく、すでに検証済みのピンマップから設計を始めるために必要な、本物の参考資料です。

---

## 📁 プロジェクトカタログ

このエコシステムに初めて触れる方へ：`./starter-kit.sh`（Windows では
`starter-kit.bat`）を実行すると、13 個のコアリポジトリ——下記の完全な
カタログではなく、手作業で選んだ最初のセット——を、1 つのディレクトリ
内に兄弟フォルダとしてクローンできます。これは、本リポジトリ内のあら
ゆるクロスリポジトリスクリプトがすでに前提としている標準的なディレク
トリ構成です。再実行しても安全です（すでにクローン済みのものには一切
手を加えません）。その後は、
[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)
（今クローンしたばかりの 13 個のうちの 1 つ）を使って、下記の完全な
カタログにある他の任意のプロジェクトのバージョン確認やビルド・更新が
行えます。

### 🧱 プラットフォーム基盤と契約
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | CM5 向け Raspberry Pi OS プラットフォーム層：再現可能なプロファイル、設定、診断、サービスのライフサイクル、更新を提供。新しい Linux ディストリビューションではありません。 |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | サービス、UI、CM5 アダプター、URTC 向けの共有バージョン管理契約、軽量クライアント、適合性テスト。ベンダー API は置き換えません。 |

### 💠 コア制御とオペレータークライアント
| リポジトリ | 説明 |
| :--- | :--- |

### 💠 コア制御とオペレータークライアント
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | STM32H745/G474 向けのコアモーション制御ファームウェア。S カーブ運動学に対応。 |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | ロボットオーケストレーション用の、ヘッドレスな Node.js API・WebSocket バックエンド。 |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 3D ロボット監視・制御向けの、React ベースの高度な Web ダッシュボード。 |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 産業用オートメーション向けの、高性能な Python/Qt デスクトップアプリケーション。 |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 7インチ産業用ディスプレイ（CM5）専用の Flutter 製タッチインターフェース。 |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 生体認証ログイン対応のネイティブ Kotlin 製モバイルアプリ。リモートでのロボット管理向け。 |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | iOS/iPadOS 向けの Flutter 製モバイルアプリ。リアルタイム WebSocket 同期に対応。 |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | ロボットモデルの検証とカタログへのプッシュを行う、グラフィカルな URDF エディタ。 |


### 🔧 URTC コアとツール
| リポジトリ | 説明 |
| :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 25 種類以上の専用工具に対応する、Universal Robot Tool Controller ファームウェア。 |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | CAN-OTA および全チップ SWD/JTAG ファームウェア更新用の GUI ツール。 |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | CAN 経由で URTC 工具プロファイルをリアルタイムに検証する診断ツール。 |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | ブラウザベースの Web Serial ツール。即座のハードウェアテストと解析が可能。 |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 自動予熱とライフサイクル監査機能を備えた、インテリジェント工具保管ラック。 |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 熱画像・RGB カメラを内蔵したツールヘッド。能動的な品質検査向け。 |

### 👁️ Vision AI Node (Hailo-8 Optimized)
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 8 系統の USB 3.0 カメラストリームを同時処理する、高速知覚処理ノード。 |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 産業用映像中継のために最適化された GStreamer/MediaMTX パイプライン。 |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | SMD・部品検査向けの、ハードウェアアクセラレーション対応 YOLO モデルライブラリ。 |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | ロボット作業空間の保護を目的とした、リアルタイム AI 侵入検知。 |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | サブミリメートル単位の姿勢補正を実現する、画像ベースの運動学フィードバック。 |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 論理的なミッションプランニングと音声制御のための、意味理解推論ノード。 |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 複雑なタスク実行のための、Vision-Language-Action（VLA）モデル実装。 |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 自然言語によるオペレーター対話のための、ローカル完結・プライバシー重視の STT/TTS パイプライン。 |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 文脈を考慮したエラー復旧機能を備える、LLM ベースのミッションオーケストレーター。 |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 技術マニュアルとソースコードで学習させた、RAG ベースの AI アシスタント。 |

### 🐝 Orchestration & Swarm（オーケストレーション・群制御）
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | マルチロボットの協調と衝突回避を担う、フリートマネージャー。 |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | ナノ秒単位のロボット同期を実現する、PTP（高精度時刻同期プロトコル）。 |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 共有作業空間内のロボット群向けの、分散型経路最適化エンジン。 |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 異種混在のロボットフリート向け、優先度ベースのタスクスケジューラー。 |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | ミッションの透過的なフェイルオーバーを実現する、高可用性モニター。 |

### 🎮 Digital Twin & Simulation（デジタルツイン・シミュレーション）
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | リスクフリーなロボットテストのための、高忠実度物理シミュレーションエンジン。 |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | URDF 運動連鎖の実物理シミュレーション（MuJoCo/PhysX）。 |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 実機と仮想コマンドを同期させる、Hardware-in-the-Loop（HIL）インターフェース。 |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | Vision ノード向け学習データセットのプロシージャル生成ツール。 |

### 📊 Data & Analytics（データ・分析）
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 大量の産業用ロボットデータを格納する、ビッグデータストレージ。 |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | CAN・WebSocket・システムログ向けの、高スループット収集エンジン。 |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | モーター振動の特徴パターンに基づく、予知保全エンジン。 |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 工場の生産管理向けの、OEE・KPI 自動生成ツール。 |

### 🏭 Industrial Gateway（産業用ゲートウェイ）
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 工場標準規格（OPC-UA/MQTT）に対応する、インダストリー4.0 相互運用ブリッジ。 |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | HydraState のロボットオブジェクトを標準 OPC-UA ノードにマッピング。 |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | IoT 連携や外部ダッシュボード向けの、テレメトリブリッジ。 |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 工作機械・ロボットの稼働監視向けの、標準化されたインターフェース。 |

### 🌉 外部オートメーションブリッジ
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 双方向 ROS 2 協調境界：観測用トピック、検査用サービス、キャンセル可能なセル作業アクション。 |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | OpenPnP とロボット支援の搬入・搬出のための、追跡可能な PCB 受け渡しコーディネーター。 |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 3D プリンターソフトウェア周辺の安全なブリッジ。最初のアダプターはファームウェアを置き換えず Moonraker の準備状態を検証します。 |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | CNC セル補助のコーディネーター。軌道と安全性はネイティブコントローラーに残ります。 |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | レーザーセル補助のコーディネーター。レーザーのアーム、有効化、インターロックの迂回はできません。 |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 脚式/ヒューマノイドドロイド向け調整境界。共有安全コントラクトで検証される歩行/把持/設置の名前付きアクション語彙で、歩容とバランス制御はドロイド自身のコントローラーが担当します。 |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | AGV/AMR フリート向け調整境界。工場座標系からAMRのローカル座標系への変換と、VDA-5050 に着想を得た注文アクション語彙を備え、経路計画はAMR自身のナビゲーションが担当します。 |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | カメラ搭載UAV向け調整境界。名前付きの飛行リクエスト語彙と、決定論的なハートビート/リンク切断フェイルセーフ監視を備えます。 |

### 🛠️ Complementary Tools（補完ツール群）
| リポジトリ | 説明 |
| :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 触覚安全アラート機能を備えた、ウェアラブル緊急ダッシュボード。 |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | フリート自動化・ファームウェア書き込み・DevOps 向けのコマンドラインインターフェース。 |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 自然言語によるインサイトを Web ダッシュボードに提供する、AI 拡張機能。 |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | エコシステム内のあらゆるプロジェクトを検出・インストール・手動更新できる、クロスプラットフォーム GUI/CLI ツール。 |

---

## 🤝 コントリビューション
本エコシステムは、ハイテクロボティクス構想の一部です。各プロジェクトにはそれぞれ独自のコントリビューションガイドラインがあります。技術的な詳細については、各リポジトリを直接ご参照ください。

エコシステム全体のリポジトリの Issue ラベルは、本リポジトリの [`.github/labels.yml`](.github/labels.yml) から統一管理され、[`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) によって各リポジトリへ同期されています——このファイル 1 つを編集するだけで、リポジトリごとに手作業で行うことなく、すべてのラベルを一括更新できます。下記のダッシュボードとは異なり、このリストは静的です（実際の GitHub Actions マトリクスであり、動的な検出ではありません）——新しいリポジトリを追加する際は、実際の `hydra-umc.project.json` だけでなく、ここにもエントリが必要です。

自身の `hydra-umc.project.json` で `ecosystem: HYDRA-UMC` を宣言しているすべての公開リポジトリを対象とするライブステータスダッシュボード（技術スタック、デプロイ対象、現在のバージョン——各リポジトリのデフォルトブランチから直接取得、固定リストなしで動的に検出）は、[`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) によって毎時自動再生成され（関連するプッシュ後は即座にも実行されます）、GitHub Pages 経由で `docs/` から配信されています：**[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**。v3 では、各プロジェクトに実際の成熟度分類（scaffolding / functional / established / production。それぞれ各プロジェクト自身の実際の CHANGELOG に基づいて判定されています——正確な判定基準は [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) モジュール自身の docstring を参照）、その役割（API / UI / CLI / ファームウェア / ライブラリ / サービス / ツール）、実際のファミリー/親子関係ツリー、そして現在実際に何が実装されているかについてのプロジェクトごとの注記が追加されています。

## 🧭 GitHub コラボレーション

[GitHub コラボレーションモデル](docs/GITHUB_COLLABORATION.md)は、中央 Wiki、エコシステム共通 Project、Discussions の範囲、リリース基準、共有自動化の境界を定義します。中央の[Issue フォーム](.github/ISSUE_TEMPLATE/)と[プルリクエストテンプレート](.github/PULL_REQUEST_TEMPLATE.md)により、プロジェクトの手順書を複製せずにソフトウェア、ハードウェア検証、ドキュメント作業を追跡できます。

Community Health ワークフローは手動実行で、既定では dry-run です。`COMMUNITY_HEALTH_SYNC_TOKEN` を設定すると、HYDRA-UMC マニフェストを公開する各リポジトリへ管理対象テンプレートだけをコピーできます。プロジェクト固有のテンプレートは削除しません。
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.
