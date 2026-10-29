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
  <a href="README\_zho.md">🇨🇳 简体中文</a> |
  <b>🇯🇵 日本語</b> |
  <a href="README\_por.md">🇵🇹 Português</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

4つの独立したエンジニアリングエコシステム、1人の作者。**HYDRA-UMC**は、リアルタイムファームウェアから認知AIまで網羅する多層構造の産業用ロボティクスプラットフォームです。**URTC**は、ロボットののエンドエフェクター専用のユニバーサル・ロボットツール・サブシステムであり、リアルタイムファームウェアとデスクトップ/Webツールを提供し、独立したバージョン管理と保守ツールを持つ独自製品として開発されています。\*\*A.R.M.O.R.\*\*は、レーダーによるプレゼンス検知、ソーラーおよび電気モニタリング、Web/モバイルクライアントを備えた中央コーディネーターを含む、独立した公開型の境界セキュリティおよびホームオートメーションエコシステムです。**EH3D Fabrication Suite**は、基板（PCB）試作、CAM処理、コンピュータビジョン検査、ピック＆プレース管理、およびHYDRA-UMCハードウェアや専門の工房機械と連携するCNC/レーザー制御のための統合ソフトウェアエコシステムです。


## 🚦 プロジェクトの状況

各行はこのリポジトリの一部分で、信号は今日どこまで進んでいるかを示します。計画ではなく、リポジトリが示せるもの（テスト、ビルド、実行）に基づいて書かれています。

🟢 完了・検証済み · 🟡 動作する（既知の制限あり） · 🟠 一部のみ、または未検証 · 🔴 未実装または動作しない

| 領域 | 状態 | ここでの意味 |
|---|---|---|
| ダッシュボードと監視 | 🟢 | 状態ダッシュボード、CI 監視、ヘルスマトリクス、リンク検査、リリース要約は GitHub Actions で定期実行され、直近の実行は成功しています。 |
| テスト | 🟢 | 44 件のテストが通ります（`python -m unittest discover -s tests`）：カタログ、監視、バナー、ロードマップの初期投入、README の整合。 |
| カタログとバージョン | 🟡 | 各プロジェクト表のバージョン列は、スクリプトが各リポジトリ自身のマニフェストから埋めて検査するため古くなりません。1 行の説明は手書きです。 |
| 進捗バー | 🟠 | 各エコシステムの下のパーセンテージは手作業で設定した参考値です。100% の到達点は、完全に統合され実機で動作するエコシステムです。 |
| 8 言語の整合 | 🟢 | 8 つの README は同じ節、同じ GitHub リンク、同じ表の行数を保ち、どれかがずれるとテストが失敗します。 |
| 実機 | 🟢 | 該当なし：このリポジトリにはプロフィールとその自動化が入っており、ハードウェア上で動くものはありません。 |
| ドキュメント | 🟢 | 4 つのエコシステムを紹介する 8 言語の README、GitHub での協力ガイド、コミュニティ向けファイル。 |

## 🧭 Electro Hobby 3D とそのアップデーターについて

**Electro Hobby 3D** は JuanenRac の工房です。電子工作、ロボティクス、ソフトウェアを同じ場所で設計し、作り、プログラムし、テストします。各リポジトリはマニフェストで自身を記述し、独自のドキュメントを持ち、実機で試したものと試していないものを明記しています。

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) は**4つのエコシステムのアップデーター**です。1つのウィンドウと1つのコマンドラインから、各エコシステム専用のアップデーターに処理を引き渡し、リポジトリの検出・インストール・更新は各アップデーターが行います。以下の各エコシステムは、それぞれのアップデーターを示しています。

| エコシステム | 概要 | アップデーター |
|---|---|---|
| **HYDRA-UMC** | 産業用ロボティクスと機械制御。リアルタイムファームウェアから認知 AI まで | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | ロボットのエンドエフェクター向けファームウェアとツール | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | 境界防犯とホームオートメーション | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | 基板プロトタイピング、CAM、CNC とレーザー、ピックアンドプレース | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

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

**HYDRA-UMCエコシステム**へようこそ。これは、低レベルのリアルタイムファームウェアから高レベルの認知AIに及ぶ、多層構造の産業用ロボティクスプラットフォームです。この組織には、マイクロファクトリーの自動化や群ロボット工学において完璧に連携して動作するように設計された、多くの専門プロジェクトが集まっています。

**アップデーター：** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) がこのエコシステムのリポジトリを検出・インストール・更新します。[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) は4つすべてに対して同じことを行います。

## 📈 エコシステムの進捗状況

`\[██████████▊░░░░░░░░░] 54%` — 参考値です。100%のマイルストーンは、実機ハードウェア上で動作する完全に統合されたエコシステムです。

> \[!IMPORTANT]
> 🛠️ \*\*プロジェクト一時停止中 — 実機ハードウェアの構築中。\*\* バーの進行だけでなく、次の作業フェーズで実際に実行・検証できる実機（フレーム、配線、実際のCM5およびSTM32ボード）を物理的に組み立てるため、現在アクティブな開発は一時中断しています。組み立てが完了し次第、作業が再開されます。

\---

## 🚀 主な機能とスケーラビリティ

* **マルチロボットのスケーラビリティ**: 最大8台の分散型ロボットユニットをサポート（現在は3、4、5、6自由度; 将来のリリースでは7、8、9自由度およびデュアルロボットアーキテクチャに拡張予定）。
* **統合ローカルステージ**: メインのHYDRA-UMCボードには、補助タスク（サブロボット、ATC（自動工具交換装置）リボルバー、コンベアベルトの同期、XYZテーブルガントリーなど）用のオンボード**6軸ローカルステージ**が搭載されています。

\---

## 🏗️ エコシステムのアーキテクチャ

v1.1エコシステムは、新しいオペレーティングシステムの作成やベンダーAPIの置き換えではなく、確立されたLinuxおよびRaspberry Piテクノロジーを基盤とした階層型製品プラットフォームです。

1. **プラットフォームベース**: Raspberry Pi OS ARM64および標準的なLinuxサービスが、サポート対象のCM5基盤を提供します。
2. **プラットフォームと契約**: **HYDRA-UMC-OS**は、Raspberry Pi OS上の再現可能なプロファイル、サービス、診断、アップデートをパッケージ化します。**HYDRA-UMC-SDK**は、バージョン管理された契約、シンクライアント、および適合性フィクスチャを公開します。
3. **リアルタイム実行**: **HYDRA-UMC**ファームウェアは、STM32/MCU上の動作制限、ウォッチドッグ、安全停止を管理します。ツール自体およびエンドエフェクターに対する独自のリアルタイム権限は、下位の独立した**URTC**エコシステムに属します。
4. **調整と運用**: サーバーサービス、ジョブディスパッチ、テレメトリ、および構成は、MCUの安全境界をバイパスせずにデバイスを調整します。
5. **オペレーターインターフェース**: Studio、Suite、DSI、Web、デスクトップ、モバイル、およびCLIクライアントは、SDK契約を使用します。
6. **知覚と知能**: ビジョン、Hailo、および認知サービスは、観測やプランを提案しますが、物理的な安全権限は持ちません。
7. **エンジニアリング、産業、データ**: デジタルツイン、HIL/物理演算、OPC-UA/MQTT/MTConnectゲートウェイ、およびデータサービスがシステムを検証・統合します。

実装に関するガイダンスについては、まず**HYDRA-UMC-OS**の公開アーキテクチャおよびサービスドキュメントを参照し、次に**HYDRA-UMC-SDK**の契約と適合性ルールを使用してください。MCUの安全権限は、すべてのフローを通じて保持されます。

\---

## 🛠️ 技術スタックとツール

本エコシステムは、ミッションクリティカルな信頼性のために、最新かつ高性能なスタックを活用しています。

### 💠 組み込みとリアルタイム（実行）

* **マイクロコントローラ**: STM32H745（デュアルコア 480MHz）、STM32G474（170MHz）、STM32F303。
* **フレームワーク**: FreeRTOS（AMPモード）、CMSIS-DSP、STM32 HAL/LL。
* **プロトコル**: FDCAN（1Mbps/5Mbps）、CAN-OTA、SPI（50MHzスレーブIPC）、I2C、UART。
* **運動学**: S字プロファイル生成、リアルタイム逆運動学（IK）。

### 🧠 エッジAIと知覚（知能）

* **アクセラレータ**: Hailo-8（26 TOPS、8カメラビジョン用）、Hailo-10（40 TOPS、GenAI用）。
* **モデル**: YOLOv10（検出）、OpenVLA（アクション）、Whisper（音声）、Llama-3（推論）。
* **ノード間**: Protobuf上のgRPCおよび高速SPI-DMAメタデータ交換。

### 🌐 バックエンドと調整（調整）

* **ランタイム**: Node.js 20+（API）、Rust 1.80+（オーケストレーター）、Go（CLI）。
* **インフラストラクチャ**: Express、Fastify、Socket.io（WebSocket）、gRPC。
* **データベース**: InfluxDB/TimescaleDB（テレメトリ）、Redis（状態）、SQLite。

### 💻 ダッシュボードとユーザーインターフェース（インターフェース）

* **Web**: React 19、Vite、Three.js（3Dビューポート）、Tailwind CSS。
* **ネイティブ**: Python 3.12/PySide6（Suite）、Kotlin（Androidネイティブ）、Flutter 3.x（iOS \& DSI）。

\---

## 📋 システム要件

* **計算ノード**: Raspberry Pi CM5（4GB以上のRAM）、NVMe/eMMCストレージ。
* **AIハードウェア**: Hailo-8/Hailo-10 M.2モジュール（Key M）。
* **フィールドバス**: LAN用ギガビットイーサネット、アクチュエータ用FDCAN（ISO 11898-1:2015）。
* **クライアントOS**: Android 10+、iOS 15+、Windows 10/11（高DPI）、Ubuntu 22.04 LTS。

\---

## 🔒 産業安全とセキュリティ

* **E-STOP層**: ハードワイヤード緊急停止ライン ＋ 優先度の高いCAN緊急フレーム（<1ms）。
* **AIセーフティ**: 人体侵入時にモーターのトルクを自動切断する3Dセーフティゾーン。
* **サイバーセキュリティ**: 安全なノード間トラフィックのためのJWTベースのステートレス認証 ＋ mTLS。
* **整合性**: ツールライフサイクルの監査と状態復元のための不揮発性F-RAM。

\---

## 🔧 ハードウェアハッキング：独自のキャリアボードの構築

ロボットコントローラーボードは**Raspberry Pi CM5**を中心に構築されており、CM5独自のデュアルHirose DF40コネクタは、このプロジェクトが独自定義したものではなく、Raspberry Piの公式CM5データシートの表5にある固定された公式の公開ピン配置です。つまり、互換性のあるサードパーティ製キャリアは、リバースエンジニアリングの演習ではなく、現実的で実現可能なプロジェクトとなります。

* **ここから始める**: [`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - このボードが実際に使用しているCM5の固定ピン（イーサネット、2つのネイティブUSB3 SuperSpeed PHY、CM5側の冷却ファンヘッダー）とその理由が、公式ピン配置テーブルから機能別に再編成されています。
* **簡単な導入経路**: 標準の**Raspberry Pi 40ピンGPIOヘッダー**（2014年以降変更のない「B+」レイアウトと同じ）が、他のRaspberry Piと同様にこのボードに引き出されているため、既存のRPi HATやGPIOツールを変更なしで使用できます。このボード自体のSTM32リンクですでに使用されている少数の位置については、スキップすべき場所がわかるようにシルク印刷/注記されています。
* **さらに進める**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md)では、CM5、STM32H745「キネマティックブレイン」、STM32G474「ロボットコントローラー」が実際にどのように通信しているか（SPI1 + FDCAN1 + CM7↔CM4 IPCメールボックス）について説明しています。これは、キャリアの再設計において、本プロジェクトのファームウェアとの互換性を維持するために保持する必要があるレイヤーです。
* 各ピン配置ドキュメントには、それが**CONFIRMED（確認済み）**（公式データシートの表から直接取得）であるか、**PROPOSED（提案）**（派生キャリアで別の選択肢が可能な、本プロジェクト独自のルーティング選択）であるかが明記されています。信号割り当てを固定として扱う前に、そのステータス行を確認してください。

これはガイド付きチュートリアルではありません（すべてのユースケースに適した唯一の「正しい」キャリアというものはありません）。データシート単体ではなく、既知の正常なピンマップから作業を開始するために経験豊富なハードウェア設計者が必要とする実際の参考資料です。

\---

## 📁 HYDRA-UMC プロジェクトカタログ

エコシステムが初めてですか？ `./starter-kit.sh`（Windowsの場合は `starter-kit.bat`）を実行すると、厳選された13個のコアリポジトリが1つのディレクトリ内にシリーブディレクトリとしてクローンされます。これは、ここにあるすべてのクロスリポジトリスクリプトが前提とする標準レイアウトです。第2引数にマニフェストによって動的に検出されるエコシステムを指定すると、そのエコシステム全体をクローンできます（`hydra-umc`、`urtc`、`armor`、`eh3d`、または `all`。例: `./starter-kit.sh \~/work armor`）。再実行しても安全です。すでにクローンされているものは変更されません。そこから、各エコシステムのアップグレーダー（または4つすべてを対象とする [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)）を使用して、バージョンを確認し、他のプロジェクトをビルド/更新できます。

### 🧱 プラットフォーム基盤と契約

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.2|CM5用Raspberry Pi OSプラットフォーム層：再現可能なプロファイル、構成、診断、サービスライフサイクル、アップデート。新しいLinuxディストリビューションではありません。|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.3.4|サービス、UI、CM5アダプター用の共有バージョン付き契約、シンクライアント、適合性フィクスチャ。ベンダーAPIを置き換えるものではありません。|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.4|外部マシンコネクタ用の宣言型アダプターマニフェストレジストリおよびバリデーター。産業用ゲートウェイプロジェクトを置き換えることなく、SDKの契約概念を外部マシンに拡張します。|

### 💠 コア制御とオペレータークライアント

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.2|S字運動学を備えたSTM32H745/G474用コアモーション制御ファームウェア。|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.0|ロボットオーケストレーション用のヘッドレスNode.js APIおよびWebSocketバックエンド。|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.0|3Dロボット監視および制御用の高度なReactベースのWebダッシュボード。|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.6.9|産業オートメーション向けの高パフォーマンスPython/Qtデスクトップアプリケーション。|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.6|7インチ産業用ディスプレイ（CM5）向けの専用Flutterベースのタッチインターフェース。|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.1|リモートロボット管理用の生体認証を備えたネイティブKotlinモバイルアプリ。|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.6|リアルタイムWebSocket同期を備えたiOS/iPadOS用Flutterモバイルアプリ。|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.4|ロボットモデルを検証してカタログにプッシュするためのグラフィカルURDFエディター。|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.6|デスクトップSTLモデルエディター - 共有モデルカタログ内の実際のパーツの変換、置換、削除、追加を行います。|

### 👁️ ビジョンAIノード（Hailo-8最適化）

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.5|8つの同時USB 3.0カメラストリーム用高速知覚ノード。|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.0|産業用ビデオ中継用に最適化されたGStreamer/MediaMTXパイプライン。|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.4|SMDおよび部品QA用のハードウェアアクセラレーションYOLOモデルライブラリ。|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.4|ロボット作業領域保護のためのリアルタイムAI侵入検知。|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.1.9|サブミリ精度のポーズ補正のための画像ベースの運動学フィードバック。|

### 🧠 認知AIノード（Hailo-10最適化）

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.4|論理的ミッションプランニングおよび音声制御用の意味的推論ノード。|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.1.7|複雑なタスク実行のためのVision-Language-Actionモデルの実装。|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.1.7|オペレーターの自然言語インタラクションのためのローカルかつプライベートなSTT/TTSパイプライン。|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.3|コンテキスト認識エラー回復機能を備えたLLMベースのミッションオーケストレーター。|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.4|技術マニュアルとソースコードでトレーニングされたRAGベースのAIアシスタント。|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.6|ローカルのポリシー制御型AIメンテナンス技術者：本日の固定リスクレベルポリシーとツール許可リストにより、悪意のある取得ドキュメントがツール呼び出しのトリガーになったり機密情報を漏洩させたりすることが決してないことを証明する実際のテスト済み防御。AIが応答を生成することで権限を取得することはありません。|

### 🐝 オーケストレーションと群制御

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.1.8|マルチロボットの協調と衝突回避のためのフリートマネージャー。|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.4|ナノ秒単位のロボット同期のためのPTP（Precision Time Protocol）同期。|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.0|共有ワークスペース内のロボット群のための分散型パスオプティマイザー。|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.2|異種ロボットフリート向けの優先度ベースのタスクスケジューラー。|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.1.7|透明性の高いミッションフェイルオーバーを備えた高可用性モニター。|

### 🎮 デジタルツインとシミュレーション

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.0.9|リスクのないロボットテストのための高忠実度物理シミュレーションエンジン。|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.0.8|URDFチェーンの実世界物理シミュレーション（MuJoCo/PhysX）。|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.0.9|実コマンドと仮想コマンドの同期のためのHardware-in-the-Loopインターフェース。|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.0|ビジョンノード向けトレーニングデータセットの手続き型ジェネレーター。|

### 📊 データとアナリティクス

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.1.8|大規模な産業用ロボットデータのためのビッグデータストレージ。|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.7|CAN、WebSocket、システムログ用の高スループットインジェスター。|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.1.7|モーター振動シグネチャに基づく予知保全エンジン。|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.5|産業プラント管理向けの自動OEEおよびKPI生成。|

### 🏭 産業用ゲートウェイ

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.5|ファクトリー標準（OPC-UA/MQTT）のためのインダストリー4.0相互運用性ブリッジ。|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.1.9|HydraStateロボットオブジェクトの標準OPC-UAノードへのマッピング。|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.6|IoT統合および外部ダッシュボード向けのテレメトリブリッジ。|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.1.8|工作機械およびロボットの健康状態監視用の標準化されたインターフェース。|

### 🌉 外部自動化ブリッジ

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.2|双方向ROS 2協調境界：監視用トピック、検査用サービス、セルジョブ用のキャンセル可能なアクション。|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.1.9|OpenPnPおよびロボット支援によるローディング/アンローディングのための追跡可能なPCBハンドオフコーディネーター。|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.1.8|ネイティブ3Dプリンターソフトウェア周辺の安全なブリッジ。最初のアダプターはファームウェアを置き換えることなくMoonrakerの準備状態を検証します。|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.1.9|CNCセル補助コーディネーター。コントローラーの軌道とマシンの安全性はネイティブのまま維持されます。|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.1.7|レーザーインターロックのアーム、発火、バイパスができないレーザーセル補助コーディネーター。|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.2|歩行/把持/配置アクション語彙（共有安全性契約を介して制御）を持つ歩行型/ヒューマノイド・ドロイド用の協調境界。歩行とバランスはドロイド自身のコントローラー上で維持されます。|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.3|AGV/AMRフリート用の協調境界：ファクトリーからローカルへの座標変換と、VDA-5050にインスパイアされた注文語彙。経路計画はAMR自身のナビゲーションに保持されます。|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.4|カメラ搭載UAV用の協調境界：飛行リクエスト語彙と決定論的ハートビート/リンク喪失フェイルセーフウォッチドッグ。|

### 🛠️ 補完ツール

|リポジトリ|バージョン|説明|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.5|触覚による安全性アラートを備えたウェアラブル緊急ダッシュボード。|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.1.6|フリートの自動化、フラッシング、DevOpsのためのコマンドラインインターフェース。|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.6|自然言語による洞察を提供するWebダッシュボード用AI拡張。|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.4.8|すべてのエコシステムプロジェクトを検出し、インストールし、手動で更新するためのクロスプラットフォームGUI/CLIツール。|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.1|エコシステムの最新バージョンとRaspberry-Pi-Imagerスタイルの初回起動設定が事前ロードされた、フラッシュ準備完了のCM5イメージをビルドするWindows/Linuxデスクトップツール。|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.1.8|メンテナンスインシデントコーディネーター：特権の低いエッジロールがサニタイズされたインベントリ/ヘルススナップショットを収集し、コントロールプレーンロールがそれを読み取り専用にし、AIプロバイダーに診断の提案を求めます。パッチの適用やデプロイは一切行いません。|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.1.8|再現可能な開発ホスト：本日はポリシー制御型の構成スキーマとマニフェストインベントリですが、OPS-AGENTと連携した独立したタスク/ワークスペースランナーへと発展します。ドキュメントによって明示的に許可されていない限り、タスクにデプロイ権限が与えられることはありません。|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.3|エコシステムのアーキテクチャ、インターフェース、セキュリティベースライン、能力マトリックス、生成されたプロジェクトカタログ、および全リポジトリを比較するツール。|

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

\*\*URTC（Universal Robot Tool Controller）\*\*は、HYDRA-UMCのサブシステムフォルダではなく、独自の製品です。ロボットのエンドエフェクター用のリアルタイムファームウェアおよびデスクトップ/Webツールのファミリーであり、独自に開発、バージョン管理、保守が行われます。URTCを搭載したツールチェンジャーはFDCANを介してHYDRA-UMCのセルコントローラーと協調しますが、ツールのリアルタイム動作、ウォッチドッグ、安全状態はURTC独自の権限です。セルコントローラーがこれらをバイパスすることはできず、URTCは開発、フラッシュ、診断のためにHYDRA-UMCに依存しません。

**アップデーター：** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) がこのエコシステムのリポジトリを検出・インストール・更新します。[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) は4つすべてに対して同じことを行います。

## 🏗️ URTCの仕組み

1. **ツールファームウェア**: URTC独自のSTM32ファームウェアは、25種類以上の特殊ツールプロファイル（グリッパー、ディスペンサー、プローブ、スピンドルなど）のそれぞれを、独自のタイミング、制限、障害動作で実行します。
2. **フィールドアップデート**: CAN-OTAは、ツールが既に使用しているのと同じCANバス経由で新しいファームウェアイメージをプッシュします。ツールのファームウェア自体が機能していなくても依存しないフォールバックとして、フルチップSWD/JTAGパス（URTC-FLASHER）を備えています。
3. **ライブ診断**: URTC-TESTERは、完全な工房のセットアップを必要とせず、宣言されたプロファイルに対してツールのリアルタイムCAN動作を検証します。URTC-WEB-STUDIOは、インストール不要で、Web Serialを介したブラウザタブから同様の処理を行います。
4. **ストレージとライフサイクル**: URTC-SMART-RACKはジョブ間にツールを保持し、ハンドオフ前に1つを予熱し、ツールタイプごとではなく物理ツールごとにライフサイクル監査証跡（サイクル、障害、最後の校正）を維持します。
5. **アクティブQA**: URTC-VISION-TOOL自体がツールです。外部カメラを他のツールにボルト留めしたものではなく、プロセス内品質検査用の独自サーマルカメラおよびRGBカメラを備えたツールヘッドです。
6. **共有ベース**: **URTC-COMMON**は、生成されたコードと適合性ベクトルを持つデータとしてのツールヘッドのCANプロトコルを保持します。**URTC-DOCS**は、アーキテクチャ、セキュリティベースライン、能力マトリックスを保持します。

## 🛠️ 技術スタック

* **ファームウェア**: STM32、FDCAN（セルコントローラーと共有バス）、CAN-OTA、SWD/JTAGフォールバック。
* **デスクトップツール**: フラッシングおよび診断用のクロスプラットフォームGUIクライアント（URTC-FLASHER、URTC-TESTER）。
* **ブラウザツール**: インストール不要のハードウェアテスト用Web Serial API（URTC-WEB-STUDIO）。
* **ライフサイクルデータ**: HYDRA-UMC独自のFRAM整合性アプローチと共有される、ツールごとの不揮発性監査証跡。

## 🔒 安全性

各ツールプロファイルには、セルコントローラー自身のE-STOP層とは独立して、独自のウォッチドッグと障害動作が備わっています。タイミング予算やCANハートビートを失ったツールは、外部コマンドを待つのではなく、自律的に宣言された安全状態に移行します。URTC-SMART-RACKの予熱は、そのプロファイルが宣言するツールごとの熱的制限によって制限され、ツールがサービスにまだ適しているかどうかを工房が決定するために使用するのと同じライフサイクル証跡で監査されます。

## 📁 URTC プロジェクトカタログ

|リポジトリ|バージョン|説明|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.3.7|25種類以上の特殊ツール向けユニバーサルロボットツールコントローラーファームウェア。|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.3.3|CAN-OTAおよびフルチップSWD/JTAGファームウェアアップデート用GUIツール。|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.3.2|CAN経由でのURTCツールプロファイルのリアルタイム検証用診断ツール。|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.3.2|即時のハードウェアテストと分析のためのブラウザベースのWeb Serialツール。|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.1.7|自動予熱とライフサイクル監査を備えたインテリジェントなツールストレージ。|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.1|アクティブQA用にサーマルカメラとRGBカメラが統合されたツールヘッド。|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.1.5|マニフェストからマシン上のURTCリポジトリを検出し、インストールし、更新します。|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.0.6|URTCエコシステムのアーキテクチャ、インターフェース、セキュリティベースライン、能力マトリックス、CANプロトコルスタディノート、生成されたプロジェクトカタログ、および全リポジトリを比較するツール。|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.0.3|データとしてのツールヘッドのCANプロトコル：仕様、生成されたC、TypeScript、Pythonコード、適合性ベクトル、Pythonトランスポート。|
|[URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY)|0.0.1|URTC の CAN バスの前に置くゲートウェイ：許可する識別子のリスト、レート制限、セッション鍵。|

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

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range)** は、HYDRA-UMCやURTCとは、作者が同じであることとエンジニアリングの規約（バージョン管理されたマニフェスト、共有メッセージ契約、8言語対応インターフェース）が共通している点を除き、関係のない独立した公開型の境界セキュリティおよびホームオートメーションエコシステムです。そのフィールドノードは敷地の境界とソーラー/電気設備を監視し、中央サーバーとクライアントにより、オペレーターはそれらの報告を確認して対応することができます。以下のバージョンおよび成熟度の注記は、HYDRA-UMCのダッシュボードですでに使用されているのと同じ誠実さの規約に従い、各リポジトリ独自のマニフェストと能力マトリックスから直接取得されています。

**アップデーター：** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) がこのエコシステムのリポジトリを検出・インストール・更新します。[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) は4つすべてに対して同じことを行います。

## 🏗️ A.R.M.O.R. の構築方法

1. **共有契約**: **ARMOR-COMMON**は、JSON Schema、Pythonバリデーター、および他のすべてのリポジトリが再定義することなく消費する生成済みのTypeScript/Kotlin型など、メッセージの意味を所有します。
2. **フィールドノード**: レーダー/プレゼンス検知用ESP32-S3ファームウェア（**ARMOR-RADAR**）、ソーラーインバーターおよびバッテリー監視（**ARMOR-SOLAR**）、スイッチング付き電力計測（**ARMOR-ELECTRICAL**）、および家の警報パネル（**ARMOR-ALARM**）。Pythonエージェント（**ARMOR-NETWORK**）は、すでに接続されているマシンから家のローカルネットワークとインターネットの到達性を監視します。
3. **中央コーディネーター**: **ARMOR-SERVER**は、状態、ユーザー、アラーム、自動化、カメラのエビデンスを保持します。**ARMOR-SERVER-AI**および**ARMOR-VOICE-AI**は、説明可能な視覚ポリシーと、自律的に動作を行わないオフラインの音声インテントを追加します。
4. **オペレータークライアント**: **ARMOR-STUDIO**（Web）および **ARMOR-ANDROID-CONTROL**（モバイル）は中央サーバーのクライアントであり、フィールドネットワークと直接通信することはありません。**ARMOR-HMI**は壁面のタッチパネル（Waveshare ESP32-S3-Touch-LCD-7C-BOX）であり、状態の表示、武装、武装解除、確認を行い、音声アシスタントが常駐する場所となります。
5. **デプロイとテスト**: **ARMOR-DEVOPS**はサービスグラフ全体をデプロイします。**ARMOR-SIMULATOR**は実際のハードウェアなしでシナリオや再現可能な障害をリプレイします。**ARMOR-HARDWARE**は筐体設計とベンチ受け入れマトリックスを担います。
6. **エコシステム運用**: **ARMOR-UPDATER**は、HYDRA-UMC-UPDATERと同じ検証によるアトミック設計により、マシン上のすべてのA.R.M.O.R.リポジトリを検出し、インストールし、更新します。**ARMOR-DOCS**は正規のアーキテクチャドキュメントおよび能力マトリックスです。**ARMOR-STUDIO**は、エコシステムのリリースキーで署名されたパッケージから中央マシンのサービスを更新することもでき、インストール前に各署名を検証します。

## 🔒 誠実さと安全性

A.R.M.O.R.は、HYDRA-UMCのダッシュボードですでに適用されているのと同じルールに従っています。主張は検証された場合にのみ現実となり、各リポジトリは、実機ハードウェア上で何が実行され、何がまだ実行されていないかを率直に示しています。現在、このエコシステムのどのコンポーネントも主電源や物理的アクセスを制御していません。フィールドノードは観察して報告を行い、将来のスイッチング機能は、有効化される前に設計およびレビューされます。

## 📁 A.R.M.O.R. プロジェクトカタログ

|リポジトリ|バージョン|説明|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.6.7|メッセージ契約、バリデーター、適合性ベクトル、生成済み型、OpenAPI、共有ランチャー。|
|[ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR)|0.7.3|ESP32-S3フィールドノードファームウェア、LD2450・LD2461およびプレゼンスセンサー用デコーダー、ホストテスト済みのコア、プログレスバー付きのGitHubからのアップデート、ライブマップ。|
|[ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR)|0.4.9|ソーラーゲートウェイノード：ESP32-S3ファームウェアとそのパネル（10シリアルポート）、Voltronic/MPP SolarインバーターおよびPylontech/ANT-BMSバッテリーのプロトコル。|
|[ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL)|0.4.1|電気ノード：ファームウェア（1つのシリアルライン上の16個のPZEMメーター、Webパネル、MQTT）、メーターのフレーム、ネットワーク読み取り値のメッセージ、スイッチング規則。|
|[ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM)|0.3.9|警報ノードとパネル：ファームウェア（有線ゾーン、サイレン、Zigbeeセンサー/サイレン、7言語のWebパネル）および武装、遅延、アラーム、PINのルール。コンピュータ上でテスト済みであり、サーバーが不在のときも警戒を続け、Zigbee無線を引き継ぎます。ボード上で実行されたことはありません。|
|[ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI)|0.3.2|Waveshare ESP32-S3-Touch-LCD-7C-BOX用タッチパネル：壁面画面でのシステム状態、武装/武装解除/確認、プッシュトーク音声、ノードのWebページ。ファームウェアはボード上で実行されたことがありません。|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.3|ローカルネットワークモニター：家のネットワーク上のデバイス、インターネットの状態（および障害がどちら側にあるか）、変更点。観察のみを行います。|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.7.8|中央状態（永続化）、ユーザー、イベント履歴、アラーム、デバイス、自動化、ソーラーおよび電気の読み取り値、ローカルネットワーク、システムサービス、カメラウォッチドッグ、カメラ、エビデンス、監査、署名が必須のノードファームウェアアップデート、TelegramおよびHome Assistant通知、音声コマンド、外部からの利用（2要素認証、終了可能なセッション、リモートポリシー）。|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.6|モーション監視サービス、ビジュアルプロファイル選択、説明可能な融合ポリシー、エンジンレジストリ。|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.2|カメラゾーン、マスク、検出ルール（うろつき、1訪問につき1イベント）。検出器モデルはまだありません。|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.0|オフライン音声サービス：8言語の15コマンド、壁面パネルの音声ターン、署名付きトークンで確認された武装および武装解除。|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.0.3|操作コンソール、アラーム、デバイス、自動化、ユーザー、履歴、アラート規則、PTZ、レーダーマップ、ソーラーおよび電気メニュー、ローカルネットワーク、システムサービス、天気、ノードファインダーと設定、ノードファームウェアアップデート、通知、2D/3Dサイトデザイナー。|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.0|Androidオペレータークライアント：武装と武装解除、アラーム、デバイス、ライブレーダー、ソーラーインバーターとバッテリー、履歴、アラーム通知、書き言葉/話し言葉用コマンドアシスタント、ノード設定ツール。|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.4|筐体設計（レーダーコーナーエンクロージャー。ソーラー、電気、アラームノード用のチェックボックス付き）およびベンチ受け入れマトリックス。|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.3|Composeトポロジ、中央サーバーテストベンチインストーラー、バックアップと復元、TLSプロファイル、専用MQTTブローカー、観察および音声サービス、管理エージェント。|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.5|シナリオと再現可能な障害。|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.4|エコシステム自身のリポジトリを検出、インストール、更新します（検証によるアトミック、GITHUB\_TOKEN不要）。|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.0.4|正規のドキュメントおよび能力マトリックス。|

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

**EH3D Fabrication Suite** は、プリント基板（PCB）の迅速な試作、CAMツールパスの準備、コンピュータビジョン検査、ピック＆プレース（PnP）管理、およびマルチマシーンCNC/レーザー制御に特化した、専用のマルチリポジトリソフトウェアエコシステムです。**HYDRA-UMC**ハードウェアノード（STM32H7 + Jetson Orin NX + Hailo NPU）とのネイティブな相互運用性を提供し、産業用フライスシステム（ESP32-S3 RS-232ゲートウェイ経由のBungard CCD）、CNCルーター（JuanenCNC）、ダイオードレーザー彫刻機（JuanenLaser）を含む工房の機械群と連携します。

**アップデーター：** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) がこのエコシステムのリポジトリを検出・インストール・更新します。[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) は4つすべてに対して同じことを行います。

## 🏗️ EH3D Fabrication Suite の仕組み

1. **中央管理**: **EH3D-SUITE-LAUNCHER**は、ローカルネットワーク上のアクティブなハードウェアノード（HYDRA-UMCおよびESP32ゲートウェイ）を検出し、統一された`.eh3dproj`パッケージを管理し、ツールの更新をオーケストレートします。
2. **CAM処理パイプライン**: 特化したCAD/CAMツールが個々の製造ステージを処理します：

   * **EH3D-ISOCAM**: Gerber RS-274X/X2トレースのアイソレーション、ボロノイアルゴリズム、および余剰銅の除去（ラバウト）。
   * **EH3D-DRILLPRO**: Excellon/NCドリル処理、ドリルビットテーブル、ディープホール掘削サイクル。
   * **EH3D-ROUTEPRO**: 基板外形フライス加工、タブ作成、ランプエントリー戦略。
   * **EH3D-LASER-CAM**: レーザー切断用のラスターディザリングアルゴリズムとベクトル出力変調。
   * **EH3D-STENCILCAM**: SMDはんだペーストステンシル生成のためのペーストマスク処理。
3. **実行とリアルタイム制御**: **EH3D-MOTIONCNC**は、高速Gコード/HP-GLストリーミングを介して機械の動きを駆動し、地形Zプロービング用の**EH3D-AUTOLEVEL**および手動ゼロ設定（G54/G55）やジョギング用の**EH3D-PENDANT-GUI**と統合されています。
4. **エッジAIと検査**: **EH3D-VISION-STUDIO**は、HYDRA-UMCのHailo NPUを活用して、リアルタイムのカメラアライメント、自動位置合わせマーク（フィデューシャル）検出、およびツール摩耗検査を実行します。
5. **アセンブリと補助データ**: **EH3D-PNP-MANAGER**はセントロイドのピック＆プレース座標とフィーダーを管理し、**EH3D-TOOL-MANAGER**はすべてのCAMモジュール間で統一されたツール crib データベースを維持します。

## 📁 EH3D Fabrication Suite プロジェクトカタログ

### 💠 中核制御とオペレーター向けクライアント
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|プロジェクト管理（.eh3dproj）、アップデート、グローバル設定、ノード検出を行うメインのエコシステムダッシュボード。|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.1|データスキーマ、統一プロジェクト（.eh3dproj）仕様、グローバル定数、UIグラフィックアセット。|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.1|エコシステムのドキュメント、組立ガイド、ゲートウェイの技術仕様、統合マニュアル。|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.1|Gerber/Excellon/Gコード/HP-GLパーサー、2D/3Dジオメトリ、プロトコルを含む共有C++/Pythonライブラリ。|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.1|エコシステム自身のリポジトリを検出、インストール、更新します（検証によるアトミック、GITHUB\_TOKEN不要）。|
|[EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER)|0.0.1|REST と websocket のインターフェースを持つ Rust 製サーバー。ユーザー、機械、ジョブを管理し、DRILLPRO と ROUTEPRO のライブラリで穴あけ・ルーティングのジョブを計画し、機械ごとに一度に 1 つのジョブだけを実行します。|
|[EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)|0.0.1|EH3D-SERVER 向けの Rust 製 Web クライアント。|

### 💠 ドリル／ルーター／ミリングのプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.1|Excellon/NCドリルCAMアプリ、ドリルビット管理、パス最適化、ディープドリルサイクル。|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.1|基板輪郭フライス加工CAMアプリ、ポケティング、保持タブ、CNCランプエントリー戦略。|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.1|リアルタイム数値制御GUI、3D Gコードビジュアライザー、プロービング、マルチマシーンストリーミングサポート。|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|すべてのEH3D CAMツールにわたって摩耗時間、切削プリセット、送りを追跡する共有ツールcribデータベース。|

### 💠 レーザーのプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|画像ディザリング、ラスター/ベクター変換、動的PWM電力制御のためのレーザーCAMアプリ。|

### 💠 CAM のプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|Gerber RS-274X/X2 CAM処理アプリ、ボロノイ/オフセットトレースアイソレーション、ラバウト、彫刻シミュレーション。|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|3Dツールパスおよび材料除去シミュレーター、衝突検出器、Gコード/HP-GLサイクルタイムエスティメーター。|

### 💠 Gerber のプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|Gerberレイヤーの位置合わせと迅速な視覚化のための軽量CAM検査ツール。|

### 💠 Pick&Place のプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|レーザーおよびプロッターSMDステンシル製造用の切削ツールパスを生成するペーストマスク変換ユーティリティ。|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|OpenPnPにインスパイアされたSMDアセンブリマネージャー、セントロイドリーダー、フィーダー制御、ビジョンコンポーネント中心合わせ。|

### 💠 ノードのプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)|0.0.1|Bungard CCD 機械の筐体に取り付ける ESP32-S3 ノード。制御ユニットの RS-232 を Ethernet または Wi-Fi で扱い、機械のランプとスピンドルのドライブを同じ基板に載せます。|
|[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)|0.0.1|Bungard CCD マシン向けの ESP32-P4/ESP32-C6 搭載 10 インチタッチスクリーン／モバイル手動コントローラー。リアルタイムのジョグ、ゼロ設定（G54/G55）、非常停止に対応。|
|[EH3D-NODE-HMI-GUI](https://github.com/JuanenRac/EH3D-NODE-HMI-GUI)|0.0.1|汎用の ESP32-P4/ESP32-C6 搭載 10 インチタッチスクリーン／モバイル手動コントローラー。リアルタイムのジョグ、ゼロ設定（G54/G55）、非常停止に対応。|

### 💠 FENIX のプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-FENIX-PCB](https://github.com/JuanenRac/EH3D-FENIX-PCB)|0.0.1|EDA 環境：回路図入力、PCB レイアウト、検証ツール、回路シミュレーション、SMPS と RF 向けの専用モジュール。|
|[EH3D-FENIX-CAD](https://github.com/JuanenRac/EH3D-FENIX-CAD)|0.0.1|筐体、シャーシ、ヒートシンクの設計に特化したパラメトリック機械 CAD。|
|[EH3D-DESIGN-VERIFIER](https://github.com/JuanenRac/EH3D-DESIGN-VERIFIER)|0.0.1|相互検証と設計品質管理のための総合エンジニアリング検証ツール。|
|[EH3D-VALIDATION-LAB](https://github.com/JuanenRac/EH3D-VALIDATION-LAB)|0.0.1|基準となるユースケースとシステムのリグレッションテストを管理するテスト環境。|
|[EH3D-DESIGN-HISTORY](https://github.com/JuanenRac/EH3D-DESIGN-HISTORY)|0.0.1|設計の意味的な履歴と論理的な変遷を保存するバージョン管理システム。|
|[EH3D-PROJECT-PASSPORT](https://github.com/JuanenRac/EH3D-PROJECT-PASSPORT)|0.0.1|プロジェクトの完全な監査のために、保存・再現可能な技術パスポートを生成するジェネレーター。|
|[EH3D-COMPONENT-INTELLIGENCE](https://github.com/JuanenRac/EH3D-COMPONENT-INTELLIGENCE)|0.0.1|電子部品に関するメタデータで拡充された高度な技術データベース。|
|[EH3D-MANUFACTURING-PROFILE](https://github.com/JuanenRac/EH3D-MANUFACTURING-PROFILE)|0.0.1|各工場の機械の能力とサプライヤーの技術的制約を管理するプロファイルマネージャー。|
|[EH3D-THERMAL-LAB](https://github.com/JuanenRac/EH3D-THERMAL-LAB)|0.0.1|物理設計に直接連携する段階的な熱シミュレーションラボ。|
|[EH3D-LAB-BRIDGE](https://github.com/JuanenRac/EH3D-LAB-BRIDGE)|0.0.1|シミュレーションデータと実際のラボ測定値を直接つなぐ相関モジュール。|
|[EH3D-DESIGN-EXPLORER](https://github.com/JuanenRac/EH3D-DESIGN-EXPLORER)|0.0.1|設計の代替案やブランチを比較・分析するための探索環境。|

### 💠 ANDROID/IOS のプロジェクト：
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-ANDROID-CONTROL](https://github.com/JuanenRac/EH3D-ANDROID-CONTROL)|0.0.1|EH3D-SERVER 向けの Android アプリ（クライアント）。|
|[EH3D-IOS-CONTROL](https://github.com/JuanenRac/EH3D-IOS-CONTROL)|0.0.1|EH3D-SERVER 向けの iOS アプリ（クライアント）。|

### 🛠️ 補完ツール
|リポジトリ|バージョン|説明|
|-|-|-|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|カメラアライメント、フィデューシャルマーカーのトレーニング、HYDRA-UMC経由の視覚検査を行うエッジAIビジョンダッシュボード。|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|表面補正のための地形高さメッシュプロセッサー（Zプロービング）およびGコード補間。|

\---

## 🤝 貢献 (Contributing)

各エコシステムは、それぞれのプロジェクトを持つ独立したイニシアチブです。各プロジェクトには独自の貢献ガイドラインがあります。詳細については、各リポジトリをご参照ください。

Issueのラベルは、このリポジトリ内にある [`.github/labels.yml`](.github/labels.yml) からすべてのHYDRA-UMCリポジトリ間で標準化され、[`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) によって同期されます。リポジトリごとに手動で変更するのではなく、その1つのファイルを編集するだけで、すべての場所のラベルを一度に変更できます。以下のダッシュボードとは異なり、このリストは静的（動的検出ではなく、実際のGitHub Actionsマトリックス）です。そのため、新しく追加されたリポジトリには、実体の `hydra-umc.project.json` だけでなく、ここへのエントリも必要になります。

4つのエコシステムのすべてのパブリックリポジトリをカバーするリアルタイムのステータスダッシュボードは、各リポジトリ独自のマニフェスト（`hydra-umc.project.json`、`urtc.project.json`、`armor.project.json`、`eh3d.project.json`、およびクロスエコシステムリポジトリ用の `electro-hobby-3d.project.json`）によって自律的に検出され、固定リストなしで各リポジトリのデフォルトブランチから直接読み取られます。これは、プロジェクトのプッシュ時に（各リポジトリの `dashboard-dispatch.yml` を通じて）即座に、また安全ネットとして1時間に2回 [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) によって再生成され、GitHub Pagesを介して `docs/` から公開されます：[**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/)。これには、スタック、デプロイターゲット、現在のバージョン、プロジェクトごとの実際の成熟度分類（scaffolding / functional / established / production。各プロジェクト独自のCHANGELOGから決定されます - [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py) を参照）、その役割（API / UI / CLI / ファームウェア / ライブラリ / サービス / ツール）、親子関係のツリー、および今日実装されている内容に関するプロジェクトごとのメモが表示されます。[`ecosystem-catalog.json`](ecosystem-catalog.json) はそれらのエコシステムとそのマニフェストを1か所にまとめてリストしており、両者に不一致がある場合、ダッシュボードのビルドは実行を拒否します。

## 🧭 GitHub でのコラボレーション

[GitHubコラボレーションモデル](docs/GITHUB_COLLABORATION.md) では、中央のWiki1つ、エコシステムプロジェクト1つ、Discussionのスコープ、リリース基準、および共有自動化の境界を定義しています。中央管理されている [issueフォーム](.github/ISSUE_TEMPLATE/) および [プルリクエストテンプレート](.github/PULL_REQUEST_TEMPLATE.md) により、プロジェクトのマニュアルを複製することなく、ソフトウェア、ハードウェア検証、ドキュメント作成の作業を追跡可能にしています。

コミュニティヘルスのワークフローは意図的に手動であり、デフォルトではドライランに設定されています。`COMMUNITY\_HEALTH\_SYNC\_TOKEN` が設定されると、HYDRA-UMCマニフェストを公開するすべてのリポジトリにこれら管理されたテンプレートのみをコピーできます。プロジェクト固有のテンプレートが削除されることは決してありません。

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - GPL-3.0 License.

