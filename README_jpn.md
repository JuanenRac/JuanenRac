<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Electro Hobby 3D バナー" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

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
  <img src="https://img.shields.io/badge/%E3%82%A8%E3%82%B3%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0-3-00E5FF.svg" alt="3 つのエコシステム">
</p>

3 つの独立したエンジニアリングエコシステムを、一人の作者が手がけています。**HYDRA-UMC** はリアルタイムファームウェアから認知 AI まで及ぶ、多層的な産業用ロボティクスプラットフォームです。**URTC** はその汎用ロボットツールサブシステムです：ロボットのエンドエフェクタ向けのリアルタイムファームウェアとデスクトップ／Web ツール群を、独自のバージョン管理と保守体制を持つ独立した製品として開発しています。**A.R.M.O.R.** は、HYDRA-UMC とも URTC とも無関係な、別個の公開の周辺セキュリティ・ホームオートメーションエコシステムです - レーダーによる存在検知、太陽光・電気の監視、そして Web・モバイルクライアントを備えた中央コーディネーターから成ります。

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

**HYDRA-UMC エコシステム** へようこそ。これは、低レベルのリアルタイムファームウェアから高度な認知 AI まで幅広くカバーする、多層構造の産業用ロボティクスプラットフォームです。本組織では、マイクロファクトリーの自動化と群制御ロボティクスのために、緊密に連携動作するよう設計された多数の専用プロジェクトをホストしています。

## 📈 エコシステムの進捗

`[██████████▊░░░░░░░░░] 54%` — 目安です。100% の到達点は、実機上で動作する完全統合済みのエコシステムです。

> [!IMPORTANT]
> 🛠️ **プロジェクト一時停止中 — 実機ハードウェアを構築しています。** 次の開発フェーズが本物のハードウェア上で実際に動作・検証できるよう、物理セル(フレーム、配線、実際のCM5・STM32基板)を本当に組み上げている間、積極的な開発は一時停止しています。単に進捗バーを伸ばすためではありません。この構築が完了次第、開発を再開します。

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

## 📁 プロジェクトカタログ — HYDRA-UMC

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
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.4.7 | CM5 向け Raspberry Pi OS プラットフォーム層：再現可能なプロファイル、設定、診断、サービスのライフサイクル、更新を提供。新しい Linux ディストリビューションではありません。 |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.2.8 | サービス、UI、CM5 アダプター、URTC 向けの共有バージョン管理契約、軽量クライアント、適合性テスト。ベンダー API は置き換えません。 |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.0 | 外部マシン用コネクタのための宣言的アダプターマニフェストのレジストリとバリデーター。SDK 自身の契約という発想を外部マシンにまで拡張し、産業用ゲートウェイ系のプロジェクトを置き換えることはありません。 |

### 💠 コア制御とオペレータークライアント
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.1.6 | STM32H745/G474 向けのコアモーション制御ファームウェア。S カーブ運動学に対応。 |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.0.5 | ロボットオーケストレーション用の、ヘッドレスな Node.js API・WebSocket バックエンド。 |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.7.6 | 3D ロボット監視・制御向けの、React ベースの高度な Web ダッシュボード。 |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.4 | 産業用オートメーション向けの、高性能な Python/Qt デスクトップアプリケーション。 |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.0 | 7インチ産業用ディスプレイ（CM5）専用の Flutter 製タッチインターフェース。 |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.6.3 | 生体認証ログイン対応のネイティブ Kotlin 製モバイルアプリ。リモートでのロボット管理向け。 |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.0 | iOS/iPadOS 向けの Flutter 製モバイルアプリ。リアルタイム WebSocket 同期に対応。 |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.0 | ロボットモデルの検証とカタログへのプッシュを行う、グラフィカルな URDF エディタ。 |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.2 | 共有モデルカタログ内で実在するパーツを変換・置換・削除・追加するデスクトップ STL モデルエディタ。 |


### 👁️ Vision AI Node (Hailo-8 Optimized)
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.0 | 8 系統の USB 3.0 カメラストリームを同時処理する、高速知覚処理ノード。 |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.1.6 | 産業用映像中継のために最適化された GStreamer/MediaMTX パイプライン。 |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.0.9 | SMD・部品検査向けの、ハードウェアアクセラレーション対応 YOLO モデルライブラリ。 |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.1 | ロボット作業空間の保護を目的とした、リアルタイム AI 侵入検知。 |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.4 | サブミリメートル単位の姿勢補正を実現する、画像ベースの運動学フィードバック。 |

### 🧠 Cognitive AI Node (Hailo-10 Optimized)
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.1 | 論理的なミッションプランニングと音声制御のための、意味理解推論ノード。 |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.4 | 複雑なタスク実行のための、Vision-Language-Action（VLA）モデル実装。 |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.3 | 自然言語によるオペレーター対話のための、ローカル完結・プライバシー重視の STT/TTS パイプライン。 |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.0 | 文脈を考慮したエラー復旧機能を備える、LLM ベースのミッションオーケストレーター。 |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.0 | 技術マニュアルとソースコードで学習させた、RAG ベースの AI アシスタント。 |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.2 | ポリシーで権限を制御されたローカルAI技術者: 現在は固定のリスクレベル・ポリシーとツール許可リストであり、悪意ある取得ドキュメントが決してツール呼び出しを引き起こしたり機密情報を漏らしたりできないことを証明する、実際にテストされた防御を備える - AIは応答を生成することによって権限を得ることは決してない。 |

### 🐝 オーケストレーションと群制御（オーケストレーション・群制御）
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.3 | マルチロボットの協調と衝突回避を担う、フリートマネージャー。 |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.1 | ナノ秒単位のロボット同期を実現する、PTP（高精度時刻同期プロトコル）。 |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.0.7 | 共有作業空間内のロボット群向けの、分散型経路最適化エンジン。 |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.1.8 | 異種混在のロボットフリート向け、優先度ベースのタスクスケジューラー。 |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.4 | ミッションの透過的なフェイルオーバーを実現する、高可用性モニター。 |

### 🎮 デジタルツインとシミュレーション（デジタルツイン・シミュレーション）
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.7 | リスクフリーなロボットテストのための、高忠実度物理シミュレーションエンジン。 |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.6 | URDF 運動連鎖の実物理シミュレーション（MuJoCo/PhysX）。 |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.6 | 実機と仮想コマンドを同期させる、Hardware-in-the-Loop（HIL）インターフェース。 |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.0.8 | Vision ノード向け学習データセットのプロシージャル生成ツール。 |

### 📊 データと分析（データ・分析）
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.3 | 大量の産業用ロボットデータを格納する、ビッグデータストレージ。 |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.4 | CAN・WebSocket・システムログ向けの、高スループット収集エンジン。 |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.3 | モーター振動の特徴パターンに基づく、予知保全エンジン。 |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.2 | 工場の生産管理向けの、OEE・KPI 自動生成ツール。 |

### 🏭 産業用ゲートウェイ（産業用ゲートウェイ）
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.2 | 工場標準規格（OPC-UA/MQTT）に対応する、インダストリー4.0 相互運用ブリッジ。 |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.5 | HydraState のロボットオブジェクトを標準 OPC-UA ノードにマッピング。 |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.2 | IoT 連携や外部ダッシュボード向けの、テレメトリブリッジ。 |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.4 | 工作機械・ロボットの稼働監視向けの、標準化されたインターフェース。 |

### 🌉 外部オートメーションブリッジ
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.0.7 | 双方向 ROS 2 協調境界：観測用トピック、検査用サービス、キャンセル可能なセル作業アクション。 |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.4 | OpenPnP とロボット支援の搬入・搬出のための、追跡可能な PCB 受け渡しコーディネーター。 |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.3 | 3D プリンターソフトウェア周辺の安全なブリッジ。最初のアダプターはファームウェアを置き換えず Moonraker の準備状態を検証します。 |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.4 | CNC セル補助のコーディネーター。軌道と安全性はネイティブコントローラーに残ります。 |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.2 | レーザーセル補助のコーディネーター。レーザーのアーム、有効化、インターロックの迂回はできません。 |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.0.8 | 脚式/ヒューマノイドドロイド向け調整境界。共有安全コントラクトで検証される歩行/把持/設置の名前付きアクション語彙で、歩容とバランス制御はドロイド自身のコントローラーが担当します。 |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.0.8 | AGV/AMR フリート向け調整境界。工場座標系からAMRのローカル座標系への変換と、VDA-5050 に着想を得た注文アクション語彙を備え、経路計画はAMR自身のナビゲーションが担当します。 |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.0.9 | カメラ搭載UAV向け調整境界。名前付きの飛行リクエスト語彙と、決定論的なハートビート/リンク切断フェイルセーフ監視を備えます。 |

### 🛠️ 補完ツール（補完ツール群）
| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.2 | 触覚安全アラート機能を備えた、ウェアラブル緊急ダッシュボード。 |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.2 | フリート自動化・ファームウェア書き込み・DevOps 向けのコマンドラインインターフェース。 |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.1 | 自然言語によるインサイトを Web ダッシュボードに提供する、AI 拡張機能。 |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.6 | エコシステム内のあらゆるプロジェクトを検出・インストール・手動更新できる、クロスプラットフォーム GUI/CLI ツール。 |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.2.7 | エコシステムの最新バージョンをプリロードし、Raspberry Pi Imager方式の初回起動設定を備えた、書き込み可能なCM5イメージを構築するWindows/Linuxデスクトップツール。 |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.4 | 保守インシデントコーディネーター: 低権限のエッジ役割がサニタイズされたインベントリ/ヘルスのスナップショットを収集し、コントロールプレーン役割がそれを読み取り専用でレンダリングして AI プロバイダーに診断の提案を依頼します - パッチを適用することも、何かをデプロイすることも決してありません。 |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.3 | 再現可能な開発サーバー: 現在は権限制御された設定スキーマとマニフェストの棚卸しであり、OPS-AGENTと連携した分離タスク/ワークスペースランナーへと成長していく - 文書が明示的に許可しない限り、どのタスクもデプロイ権限を持たない。 |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="URTC エコシステムバナー" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/%E3%83%97%E3%83%A9%E3%83%83%E3%83%88%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/%E3%83%90%E3%82%B9-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/%E3%83%84%E3%83%BC%E3%83%AB-25%2B%E3%83%97%E3%83%AD%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB-blueviolet.svg" alt="Tools">
</p>

**URTC（Universal Robot Tool Controller）**は HYDRA-UMC のサブシステムフォルダーではなく、それ自体が独立した製品です：ロボットのエンドエフェクタ向けのリアルタイムファームウェアと、独立して開発・バージョン管理・保守されるデスクトップ／Web ツール群です。URTC を搭載したツールチェンジャーは FDCAN 経由で HYDRA-UMC のセルコントローラーと協調しますが、ツール自身のリアルタイム挙動、ウォッチドッグ、安全状態は URTC 自身の権限であり、セルコントローラーはそれを迂回できません。また URTC の開発・書き込み・診断は HYDRA-UMC に依存しません。

## 🏗️ URTC の仕組み

1. **ツールファームウェア**：URTC 自身の STM32 ファームウェアが、25 種類以上ある専用ツールプロファイル（グリッパー、ディスペンサー、プローブ、スピンドルなど）のそれぞれを実行し、各プロファイルは独自のタイミング、制限、故障時の挙動を持ちます。
2. **フィールドでの更新**：CAN-OTA はツールがすでに使用している同じ CAN バス経由で新しいファームウェアイメージを送信し、ツール自身のファームウェアが生きていることに一切依存しないフォールバックとして、チップ全体を書き換える SWD/JTAG 経路（URTC-FLASHER）を備えます。
3. **ライブ診断**：URTC-TESTER は、完全な作業場を用意しなくても、宣言されたプロファイルに対してツールの実際の CAN 挙動をリアルタイムで検証し、URTC-WEB-STUDIO はブラウザのタブから Web Serial 経由で同じことを、何もインストールせずに行います。
4. **保管とライフサイクル**：URTC-SMART-RACK は作業と作業の間にツールを保管し、受け渡し前に予熱し、ツールの種類ではなく物理的なツール個体ごとにライフサイクル監査記録（サイクル数、故障、最終校正）を保持します。
5. **アクティブな QA**：URTC-VISION-TOOL はそれ自体が一つのツールです - 別のツールに外付けされたカメラではなく、独自のサーマルおよび RGB カメラを備え、工程中に品質検査を行うツールヘッドです。

## 🛠️ 技術スタック

- **ファームウェア**：STM32、FDCAN（セルコントローラーと共有するバス）、CAN-OTA、SWD/JTAG フォールバック。
- **デスクトップツール**：書き込みと診断のためのクロスプラットフォーム GUI クライアント（URTC-FLASHER、URTC-TESTER）。
- **ブラウザツール**：インストール不要のハードウェアテストのための Web Serial API（URTC-WEB-STUDIO）。
- **ライフサイクルデータ**：HYDRA-UMC と同じ F-RAM による整合性の考え方に基づく、ツールごとの不揮発性監査記録。

## 🔒 安全性

各ツールプロファイルは、セルコントローラー自身の E-STOP 層とは独立した、それぞれ固有のウォッチドッグと故障時の挙動を持ちます - 自身のタイムバジェットや CAN のハートビートを失ったツールは、外部からの指令を待つのではなく、自ら宣言された安全状態へと移行します。URTC-SMART-RACK の予熱は、そのプロファイルが宣言するのと同じツールごとの熱的制限に縛られ、あるツールがまだ使用に適しているかを作業場が判断するのと同じライフサイクル監査記録に記録されます。

## 📁 URTC プロジェクトカタログ

| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.1 | 25 種類以上の専用工具に対応する、Universal Robot Tool Controller ファームウェア。 |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.2.1 | CAN-OTA および全チップ SWD/JTAG ファームウェア更新用の GUI ツール。 |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.2.2 | CAN 経由で URTC 工具プロファイルをリアルタイムに検証する診断ツール。 |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.2.2 | ブラウザベースの Web Serial ツール。即座のハードウェアテストと解析が可能。 |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.0 | 自動予熱とライフサイクル監査機能を備えた、インテリジェント工具保管ラック。 |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.0.5 | 熱画像・RGB カメラを内蔵したツールヘッド。能動的な品質検査向け。 |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="A.R.M.O.R. エコシステムバナー" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/%E5%85%AC%E9%96%8B%E7%AF%84%E5%9B%B2-%E9%9D%9E%E5%85%AC%E9%96%8B-lightgrey.svg" alt="Private repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

**A.R.M.O.R.（Autonomous Radar & Multimodal Observation Range）**は、同じ作者と同じエンジニアリング上の慣習（バージョン管理されたマニフェスト、共有のメッセージ契約、7 言語のインターフェース）を除けば HYDRA-UMC とも URTC とも無関係な、別個の公開の周辺セキュリティ・ホームオートメーションエコシステムです。そのフィールドノードは物件の周辺と太陽光・電気設備を監視し、中央サーバーとクライアントはオペレーターがそれらの報告内容を見て対応できるようにします。バージョンと成熟度の注記は各リポジトリ自身のマニフェストと機能マトリクスからそのまま取られています - これは HYDRA-UMC のダッシュボードがすでに用いているのと同じ誠実さの慣習です。

## 🏗️ A.R.M.O.R. の構成

1. **共有契約**：**ARMOR-COMMON** がメッセージの意味を所有します - JSON Schema、Python の検証器、そして他のあらゆるリポジトリが消費するだけで再定義することのない、生成された TypeScript/Kotlin の型です。
2. **フィールドノード**：レーダー・存在検知用の ESP32-S3 ファームウェア（**ARMOR-RADAR**）、太陽光インバーターとバッテリーの監視（**ARMOR-SOLAR**）、開閉機能を備えた電力計測（**ARMOR-ELECTRICAL**）；Python 製のエージェント（**ARMOR-NETWORK**）が、すでにその家のローカルネットワークに接続されたマシンから、そのネットワーク自体とインターネットの到達性を監視します。
3. **中央コーディネーター**：**ARMOR-SERVER** が状態、ユーザー、アラーム、自動化、カメラの証跡を保持し、**ARMOR-SERVER-AI** と **ARMOR-VOICE-AI** が、説明可能な視覚ポリシーと、決して自ら動作しないオフライン音声インテントを追加します。
4. **オペレータークライアント**：**ARMOR-STUDIO**（Web）と **ARMOR-ANDROID-CONTROL**（モバイル）は中央サーバーのクライアントであり、フィールドネットワークに直接接続することはありません。 **ARMOR-HMI** は壁掛けのタッチパネル（Waveshare ESP32-S3-Touch-LCD-7C-BOX）で、状態の表示、警戒、確認を行い、将来は音声アシスタントの拠点になります。
5. **デプロイとテスト**：**ARMOR-DEVOPS** がサービス全体のグラフをデプロイし、**ARMOR-SIMULATOR** が実機なしでシナリオと再現可能な故障を再生し、**ARMOR-HARDWARE** が筐体設計とそのベンチ受け入れマトリクスを担います。
6. **エコシステム運用**：**ARMOR-UPDATER** が、HYDRA-UMC-UPDATER と同じ検証済みでのみ確定する原子的な設計で、マシン上のあらゆる A.R.M.O.R. リポジトリを検出・インストール・更新します；**ARMOR-DOCS** が正式なアーキテクチャ文書と機能マトリクスです。

## 🔒 誠実さと安全性

A.R.M.O.R. は、HYDRA-UMC のダッシュボードがすでに適用しているのと同じ規則に従います：主張は検証されて初めて本物になり、各リポジトリは実機で何がすでに動作確認され、何がまだかを率直に述べます。このエコシステムのいずれも、現時点では商用電源や物理的な立ち入りを制御していません。フィールドノードは観測して報告するだけであり、将来のいかなる開閉能力も、有効化される前に設計とレビューを経ます。

## 📁 A.R.M.O.R. プロジェクトカタログ

| リポジトリ | バージョン | 説明 |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.3.6 | メッセージ契約、検証器、適合性ベクトル、生成された型 |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.5.2 | ESP32-S3 用フィールドノードのファームウェア。レーダー 3 基と独自の Web パネル付き |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.2.3 | 太陽光インバーターとバッテリーのプロトコル、およびゲートウェイノードのメッセージ |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.1.8 | 電気ノード：電力量計、電力網の計測メッセージ、開閉のルール |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.1.2 | Waveshare ESP32-S3-Touch-LCD-7C-BOX 用タッチパネル：壁面ディスプレイでのシステム状態表示、警戒・解除・確認、プッシュトゥトーク音声、ノードのWebページ。ファームウェアはボード上で一度も動作していません。 |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.0.6 | ローカルネットワーク：機器、インターネット、そして変化 |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.4.3 | 中央コーディネーター：テレメトリ、アラーム、デバイス、太陽光と電気の測定値、ローカルネットワーク、システムサービス、カメラ |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.1 | 判断を説明し、決して動作しない視覚推論ポリシー |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.2.2 | 偽造できない確認を備えたオフライン音声インテント |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.6.1 | Web コンソール：カメラ、レーダー、アラーム、太陽光と電気のメニュー、ローカルネットワーク、システムサービス、天気、ノード検索、2D/3D サイト設計 |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.4.5 | リアルタイム 2D/3D レーダー付きの Android オペレータークライアント |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.3 | 筐体、電子部品、ベンチ受け入れマトリクス |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.3.8 | デプロイ、中央サーバーのテストベンチ、バックアップ、TLS |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.3 | 再現可能な故障を備えたオフラインのテレメトリシミュレーター |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.0.7 | エコシステム自身のリポジトリを検出し、インストールし、更新する |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.5.9 | アーキテクチャ、セキュリティ基準、機能マトリクス |

---

## 🤝 コントリビューション
本エコシステムは、ハイテクロボティクス構想の一部です。各プロジェクトにはそれぞれ独自のコントリビューションガイドラインがあります。技術的な詳細については、各リポジトリを直接ご参照ください。

エコシステム全体のリポジトリの Issue ラベルは、本リポジトリの [`.github/labels.yml`](.github/labels.yml) から統一管理され、[`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) によって各リポジトリへ同期されています——このファイル 1 つを編集するだけで、リポジトリごとに手作業で行うことなく、すべてのラベルを一括更新できます。下記のダッシュボードとは異なり、このリストは静的です（実際の GitHub Actions マトリクスであり、動的な検出ではありません）——新しいリポジトリを追加する際は、実際の `hydra-umc.project.json` だけでなく、ここにもエントリが必要です。

自身の `hydra-umc.project.json` で `ecosystem: HYDRA-UMC` を宣言しているすべての公開リポジトリを対象とするライブステータスダッシュボード（技術スタック、デプロイ対象、現在のバージョン——各リポジトリのデフォルトブランチから直接取得、固定リストなしで動的に検出）は、[`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) によって毎時自動再生成され（関連するプッシュ後は即座にも実行されます）、GitHub Pages 経由で `docs/` から配信されています：**[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**。各プロジェクトに実際の成熟度分類（scaffolding / functional / established / production。それぞれ各プロジェクト自身の実際の CHANGELOG に基づいて判定されています——正確な判定基準は [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) モジュール自身の docstring を参照）、その役割（API / UI / CLI / ファームウェア / ライブラリ / サービス / ツール）、実際のファミリー/親子関係ツリー、そして現在実際に何が実装されているかについてのプロジェクトごとの注記が追加されています。URTC と A.R.M.O.R. 自身のリポジトリも、HYDRA-UMC とまったく同じ方法でこの同じダッシュボード上でライブに検出されます（`scripts/generate_dashboard.py` を参照）。それぞれが自身の `urtc.project.json`/`armor.project.json` の中で自身の `ecosystem` フィールドを宣言しており、3つのどれについても固定リストはありません。

## 🧭 GitHub コラボレーション

[GitHub コラボレーションモデル](docs/GITHUB_COLLABORATION.md)は、中央 Wiki、エコシステム共通 Project、Discussions の範囲、リリース基準、共有自動化の境界を定義します。中央の[Issue フォーム](.github/ISSUE_TEMPLATE/)と[プルリクエストテンプレート](.github/PULL_REQUEST_TEMPLATE.md)により、プロジェクトの手順書を複製せずにソフトウェア、ハードウェア検証、ドキュメント作業を追跡できます。

Community Health ワークフローは手動実行で、既定では dry-run です。`COMMUNITY_HEALTH_SYNC_TOKEN` を設定すると、HYDRA-UMC マニフェストを公開する各リポジトリへ管理対象テンプレートだけをコピーできます。プロジェクト固有のテンプレートは削除しません。
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.

