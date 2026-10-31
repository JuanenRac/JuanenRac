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
  <a href="README\_jpn.md">🇯🇵 日本語</a> |
  <b>🇵🇹 Português</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-4-00E5FF.svg" alt="Four ecosystems">
</p>

Quatro ecossistemas de engenharia independentes, um único autor. **HYDRA-UMC** é uma plataforma de robótica industrial multicamadas, desde o firmware em tempo real até a IA cognitiva. **URTC** é o seu subsistema universal de ferramentas robóticas: firmware em tempo real e ferramentas de desktop/web para o próprio efetuador final de um robô, desenvolvido como um produto próprio com versionamento e ferramentas de manutenção independentes. **A.R.M.O.R.** é um ecossistema separado e público de segurança perimetral e automação residencial - deteção de presença por radar, monitorização solar e elétrico, e um coordenador central com clientes web e móveis. **EH3D Fabrication Suite** é um ecossistema de software integrado para prototipagem de PCB, processamento CAM, inspeção por visão computacional, gestão de Pick \& Place e controlo CNC/Laser interagindo com o hardware HYDRA-UMC e maquinário de oficina especializado.


## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Painel e vigilância | 🟢 | O painel de estado, a vigilância do CI, a matriz de saúde, a verificação de ligações e o resumo de versões correm de forma agendada no GitHub Actions, e as últimas execuções passam. |
| Testes | 🟢 | Passam 59 testes (`python -m unittest discover -s tests`): o catálogo, a vigilância, os banners, a criação do roteiro dos quatro quadros (HYDRA-UMC, URTC, A.R.M.O.R. e EH3D) e a paridade dos README. |
| Catálogo e versões | 🟡 | A coluna Versão de cada tabela de projetos é preenchida por um script a partir do manifesto de cada repositório e verificada, por isso não fica desatualizada; as descrições de uma linha são escritas à mão. |
| Barras de progresso | 🟢 | A percentagem de cada ecossistema é calculada por `scripts/ecosystem_progress.py` com a maturidade e a evidência que cada repositório declara no seu próprio manifesto, e renovada com o painel; o marco de 100% continua a ser um ecossistema totalmente integrado a funcionar em hardware real. |
| Paridade em oito idiomas | 🟢 | Os oito README mantêm as mesmas secções, as mesmas ligações do GitHub e o mesmo número de linhas de tabela, e um teste falha quando um deles se desvia. |
| Hardware real | 🟢 | Não se aplica: este repositório contém o perfil e a sua automatização, nada aqui corre em hardware. |
| Documentação | 🟢 | README em oito idiomas com os quatro ecossistemas, o guia de colaboração no GitHub e os ficheiros da comunidade. |

## 🧭 Sobre a Electro Hobby 3D e o seu atualizador

**Electro Hobby 3D** é a oficina de JuanenRac: eletrónica, robótica e software que se desenham, constroem, programam e testam no mesmo sítio. Cada repositório descreve-se com um manifesto, tem a sua própria documentação e diz o que foi experimentado e o que não foi em hardware real.

[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) é **o atualizador dos quatro ecossistemas**: uma janela e uma linha de comandos que passam o trabalho ao atualizador de cada ecossistema, que são os que descobrem, instalam e atualizam os seus repositórios. Cada ecossistema abaixo nomeia o seu.

| Ecossistema | O que é | Atualizador |
|---|---|---|
| **HYDRA-UMC** | Robótica industrial e controlo de máquinas, do firmware em tempo real à IA cognitiva | [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) |
| **URTC** | Firmware e ferramentas para os efetores de um robô | [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) |
| **A.R.M.O.R.** | Segurança perimetral e domótica | [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) |
| **EH3D Fabrication Suite** | Prototipagem de PCB, CAM, CNC e laser, pick and place | [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) |

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

Bem-vindo ao **Ecossistema HYDRA-UMC**, uma plataforma de robótica industrial multicamadas que abrange desde o firmware de baixo nível em tempo real até a IA cognitiva de alto nível. Esta organização hospeda muitos projetos especializados concebidos para trabalhar em perfeita sincronia para automação de microfábricas e robótica de enxame.

**Atualizador:** [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) deteta, instala e atualiza os repositórios deste ecossistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) faz o mesmo para os quatro.

## 📈 Progresso do Ecossistema

<!-- progress:hydra-umc -->
`\[█████████▎░░░░░░░░░░] 46%` — Calculado a partir de dados reais: a maturidade e a evidência que cada um dos seus 57 repositórios declara no seu próprio manifesto. O marco de 100% é um ecossistema totalmente integrado a funcionar em hardware real.
<!-- /progress:hydra-umc -->

> \[!IMPORTANT]
> 🛠️ \*\*Projeto em pausa — construindo o hardware real.\*\* O desenvolvimento ativo está pausado enquanto a célula robótica física (estruturas, fiação, as placas reais CM5 e STM32) é construída de verdade, para que a próxima fase de trabalho tenha hardware real para executar e validar, e não apenas uma barra subindo. O trabalho recomeça assim que essa construção estiver pronta.

\---

## 🚀 Principais Recursos e Escalabilidade

* **Escalabilidade Multi-Robô**: Suporta até 8 unidades robóticas distribuídas (3, 4, 5 e 6-DOF atualmente; escalando para arquiteturas de 7, 8, 9-DOF e Duplo Robô em versões futuras).
* **Estágio Local Integrado**: A placa principal HYDRA-UMC possui um **Estágio Local de 6 eixos** integrado para tarefas auxiliares, incluindo robôs secundários, revólveres ATC (Automatic Tool Changer), sincronização de esteira transportadora ou pórticos de mesa XYZ.

\---

## 🏗️ Arquitetura do Ecossistema

O ecossistema v1.1 é uma plataforma de produtos em camadas: baseia-se na tecnologia estabelecida Linux e Raspberry Pi em vez de criar um novo sistema operativo ou substituir as APIs de fornecedores.

1. **Base da plataforma**: Raspberry Pi OS ARM64 e serviços Linux padrão fornecem a fundação CM5 suportada.
2. **Plataforma e contratos**: **HYDRA-UMC-OS** empacota perfis reprodutíveis, serviços, diagnósticos e atualizações no Raspberry Pi OS; **HYDRA-UMC-SDK** publica contratos versionados, clientes leves e acessórios de conformidade.
3. **Execução em tempo real**: O firmware **HYDRA-UMC** possui limites de movimento, watchdogs e parada segura em STM32/MCU; a ferramenta em si, e sua própria autoridade em tempo real sobre o efetuador final, pertence ao ecossistema separado **URTC** abaixo.
4. **Coordenação e operações**: Serviços de servidor, despacho de trabalhos, telemetria e configuração coordenam dispositivos sem burlar o limite de segurança da MCU.
5. **Interfaces de operador**: Studio, Suite, DSI, web, desktop, clientes móveis e CLI usam os contratos do SDK.
6. **Percepção e inteligência**: Visão, Hailo e serviços cognitivos propõem observações ou planos; eles não têm autoridade de segurança física.
7. **Engenharia, industrial e dados**: Gêmeo Digital (Digital Twin), HIL/física, gateways OPC-UA/MQTT/MTConnect e serviços de dados validam e integram o sistema.

Para orientações de implementação, comece com a arquitetura pública e documentação de serviço em **HYDRA-UMC-OS**, depois use os contratos e regras de conformidade em **HYDRA-UMC-SDK**. A autoridade de segurança da MCU é preservada ao longo de todo o fluxo.

\---

## 🛠️ Pilha Tecnológica e Ferramentas

O ecossistema aproveita uma pilha moderna e de alto desempenho para confiabilidade de missão crítica:

### 💠 Embarcado e Tempo Real (Execução)

* **Microcontroladores**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
* **Frameworks**: FreeRTOS (modo AMP), CMSIS-DSP, STM32 HAL/LL.
* **Protocolos**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (IPC Escravo 50MHz), I2C, UART.
* **Cinemática**: Geração de Perfil em Curva S, Cinemática Inversa em Tempo Real (IK).

### 🧠 IA de Borda e Percepção (Inteligência)

* **Aceleradores**: Hailo-8 (26 TOPS) para visão de 8 câmaras, Hailo-10 (40 TOPS) para GenAI.
* **Modelos**: YOLOv10 (Deteção), OpenVLA (Ação), Whisper (Voz), Llama-3 (Raciocínio).
* **Inter-nós**: gRPC sobre Protobuf e troca de metadagos SPI-DMA de alta velocidade.

### 🌐 Backend e Coordenação (Coordenação)

* **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orquestrador), Go (CLI).
* **Infraestrutura**: Express, Fastify, Socket.io (WebSocket), gRPC.
* **Banco de Dados**: InfluxDB/TimescaleDB (Telemetria), Redis (Estado), SQLite.

### 💻 Dashboards e Interface do Utilizador (Interface)

* **Web**: React 19, Vite, Three.js (Viewport 3D), Tailwind CSS.
* **Nativo**: Python 3.12/PySide6 (Suite), Kotlin (Android Nativo), Flutter 3.x (iOS \& DSI).

\---

## 📋 Requisitos do Sistema

* **Nó de Computação**: Raspberry Pi CM5 (4GB+ RAM) com armazenamento NVMe/eMMC.
* **Hardware de IA**: Módulos M.2 Hailo-8/Hailo-10 (Key M).
* **Barramento de Campo**: Ethernet Gigabit para LAN e FDCAN (ISO 11898-1:2015) para atuadores.
* **SO do Cliente**: Android 10+, iOS 15+, Windows 10/11 (Alta resolução), Ubuntu 22.04 LTS.

\---

## 🔒 Segurança Industrial

* **Camada E-STOP**: Linha de emergência cabeada + Quadros de emergência CAN de alta prioridade (<1ms).
* **Segurança de IA**: Zonas de segurança 3D com corte automático do torque do motor em caso de intrusão humana.
* **Cibersegurança**: Autenticação sem estado baseada em JWT + mTLS para tráfego seguro entre nós.
* **Integridade**: F-RAM não volátil para auditoria do ciclo de vida da ferramenta e recuperação de estado.

\---

## 🔧 Hacking de Hardware: Construindo sua Própria Placa de Suporte (Carrier)

A Placa Controladora do Robô é construída em torno de um **Raspberry Pi CM5**, e o conector dual Hirose DF40 do próprio CM5 é um pinout fixo, oficial e público (Tabela 5 da folha de dados oficial do CM5 da Raspberry Pi) - não algo definido por este projeto. Isso significa que uma placa de suporte de terceiros compatível é um projeto real e viável, não um exercício de engenharia reversa:

* **Comece por aqui**: [`HYDRA-UMC/docs/PINOUT\_CM5\_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - quais pinos fixos do CM5 esta placa realmente usa (Ethernet, os 2 PHYs USB3 SuperSpeed nativos, o cabeçalho do ventilador de refrigeração do lado do CM5) e por quê, reorganizados por função a partir da tabela oficial de pinos.
* **A entrada fácil**: o **cabeçalho GPIO padrão de 40 pinos do Raspberry Pi** (o mesmo layout "B+" inalterado desde 2014) está disponibilizado nesta placa exatamente como qualquer Raspberry Pi - HATs RPi existentes e ferramentas GPIO funcionam sem modificações. Um punhado de posições que o link STM32 desta placa já usa são serigrafadas/anotadas para que tu saiba quais pular.
* **Indo mais longe**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) aborda como o CM5, o "Cérebro Cinemático" STM32H745 e o "Controlador de Robô" STM32G474 conversam entre si (SPI1 + FDCAN1 + a caixa de correio IPC CM7↔CM4) - a camada que um redesign de placa de suporte precisaria preservar se for mantida compatível com o firmware deste projeto.
* Cada documento de pinout indica claramente se é **CONFIRMADO** (retirado diretamente de uma tabela oficial de datasheet) ou **PROPOSTO** (a escolha de roteamento própria deste projeto, aberta a uma diferente numa placa derivada) - leia essa linha de status antes de tratar uma atribuição de sinal como fixa.

Isto não é um tutorial guiado (não existe uma placa "certa" única para cada caso de uso) - é o material de referência real que um designer de hardware experiente precisa para começar a partir de um mapa de pinos conhecido e bom, em vez de apenas uma folha de dados.

\---

## 📁 Catálogo de Projetos HYDRA-UMC

Novo no ecossistema? `./starter-kit.sh` (ou `starter-kit.bat` no Windows) clona 13 repositórios principais - um conjunto inicial escolhido a dedo - como diretórios irmãos num diretório: o layout padrão que cada script multi-repositório aqui já assume. Um segundo argumento clona um ecossistema inteiro, descoberto dinamicamente pelo seu manifesto: `hydra-umc`, `urtc`, `armor`, `eh3d` ou `all` (por exemplo `./starter-kit.sh \~/work armor`). Reexecutá-lo é seguro: qualquer coisa já clonada é deixada intocada. A partir daí, o atualizador de cada ecossistema - ou [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) para todos os quatro - pode verificar versões e compilar/atualizar qualquer outro projeto.

### 🧱 Fundação da Plataforma e Contratos

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS)|0.5.6|Camada de plataforma Raspberry Pi OS para CM5: perfis reprodutíveis, configuração, diagnósticos, ciclo de vida de serviços e atualizações; não é uma nova distribuição Linux.|
|[HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK)|0.4.3|Contratos versionados partilhados, clientes leves e acessórios de conformidade para serviços, UIs e adaptadores CM5; não substitui APIs de fornecedores.|
|[HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB)|0.1.6|Registo declarativo de manifesto de adaptadores e validador para conectores de máquinas externas; estende a ideia de contrato do SDK para máquinas externas sem substituir os projetos de gateway industrial.|

### 💠 Controlo Central e Clientes Operadores

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)|0.2.4|Firmware principal de controlo de movimento para STM32H745/G474 com cinemática de Curva S.|
|[HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER)|0.8.1.7|API Node.js sem interface (headless) e backend WebSocket para orquestração robótica.|
|[HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO)|0.8.0.7|Dashboard web avançado baseado em React para monitorização e controlo 3D de robôs.|
|[HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE)|0.7.6|Aplicação de desktop Python/Qt de alto desempenho para automação industrial.|
|[HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI)|0.2.9|Interface de toque dedicada baseada em Flutter para displays industriais de 7" (CM5).|
|[HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL)|0.7.5|Aplicação móvel nativa em Kotlin com login biométrico para gestão remota de robôs.|
|[HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL)|0.2.9|Aplicação móvel Flutter para iOS/iPadOS com sincronização WebSocket em tempo real.|
|[HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF)|0.1.8|Editor gráfico URDF para validar e enviar modelos de robôs para o catálogo.|
|[HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL)|0.1.9|Editor de modelos STL de desktop - transforma, substitui, remove e adiciona peças reais no catálogo de modelos partilhado.|
| [HYDRA-UMC-MESHES](https://github.com/JuanenRac/HYDRA-UMC-MESHES) | 0.1.0 | Malhas 3D partilhadas (STL e GLB) das aplicações de ambiente de trabalho e web, publicadas uma só vez como pacote de release com somas de verificação. |

### 👁️ Nó de IA de Visão (Otimizado para Hailo-8)

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE)|0.1.8|Nó de percepção de alta velocidade para 8 fluxos de câmara USB 3.0 simultâneos.|
|[HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER)|0.2.3|Pipeline GStreamer/MediaMTX otimizado para retransmissão de vídeo industrial.|
|[HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF)|0.1.7|Biblioteca de modelos YOLO acelerados por hardware para controlo de qualidade de componentes e SMD.|
|[HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES)|0.1.8|Deteção de intrusão por IA em tempo real para proteção do volume de trabalho robótico.|
|[HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API)|0.2.2|Feedback cinemático baseado em imagem para correção de pose submétrica.|

### 🧠 Nó de IA Cognitiva (Otimizado para Hailo-10)

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE)|0.1.6|Nó de raciocínio semântico para planeamento lógico de missões e controlo de voz.|
|[HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE)|0.2.0|Implementação de modelo Vision-Language-Action para execução de tarefas complexas.|
|[HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI)|0.2.0|Pipeline STT/TTS local e privado para interação de operador em linguagem natural.|
|[HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER)|0.1.6|Orquestrador de missões baseado em LLM com recuperação de erros consciente do contexto.|
|[HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA)|0.1.6|Assistente de IA baseado em RAG treinado em manuais técnicos e código-fonte.|
|[HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN)|0.1.9|Técnico de manutenção de IA local regulado por políticas: uma política de nível de risco fixo e lista de permissões de ferramentas hoje, com uma defesa real e testada provando que um documento recuperado malicioso nunca pode acionar uma chamada de ferramenta ou vazar um segredo — a IA nunca obtém autoridade gerando uma resposta.|

### 🐝 Orquestração e Enxame

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR)|0.2.2|Gestor de frota para coordenação multi-robô e prevenção de colisões.|
|[HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC)|0.1.7|Sincronização PTP (Precision Time Protocol) para sincronização de robôs em nanossegundos.|
|[HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D)|0.1.2|Otimizador de caminhos distribuído para enxames robóticos em espaço de trabalho partilhado.|
|[HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER)|0.2.5|Agendador de tarefas baseado em prioridade para frotas de robôs heterogêneas.|
|[HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING)|0.2.1|Monitor de alta disponibilidade com failover de missão transparente.|

### 🎮 Gêmeo Digital e Simulação

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN)|0.1.2|Mecanismo de simulação física de alta fidelidade para testes de robôs sem riscos.|
|[HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA)|0.1.1|Simulação de física do mundo real (MuJoCo/PhysX) de correntes URDF.|
|[HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE)|0.1.2|Interface Hardware-in-the-loop para sincronização de comandos reais vs virtuais.|
|[HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN)|0.1.2|Gerador procedural de conjuntos de dados de treinamento para nós de visão.|

### 📊 Dados e Análise

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE)|0.2.1|Armazenamento Big Data para dados massivos de robótica industrial.|
|[HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR)|0.1.9|Coletor de alta vazão para CAN, WebSocket e logs do sistema.|
|[HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR)|0.2.0|Mecanismo de manutenção preditiva baseado em assinaturas de vibração de motores.|
|[HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS)|0.1.8|Geração automatizada de OEE e KPI para gestão de plantas industriais.|

### 🏭 Gateway Industrial

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL)|0.1.8|Ponte de interoperabilidade da Indústria 4.0 para padrões de fábrica (OPC-UA/MQTT).|
|[HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER)|0.2.3|Mapeamento de objetos robóticos HydraState para nós OPC-UA padrão.|
|[HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER)|0.1.9|Ponte de telemetria para integrações IoT e dashboards externos.|
|[HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER)|0.2.1|Interface normalizada para monitorização da saúde de máquinas-ferramenta e robôs.|

### 🌉 Pontes de Automação Externas

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2)|0.1.5|Fronteira de coordenação bidirecional ROS 2: tópicos para observação, serviços para inspeção e ações canceláveis para trabalhos de célula.|
|[HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP)|0.2.2|Coordenador de transferência de PCB rastreável para OpenPnP e carregamento/descarregamento assistido por robô.|
|[HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D)|0.2.1|Ponte segura em torno do software nativo de impressora 3D; o primeiro adaptador valida a prontidão do Moonraker sem substituir o firmware.|
|[HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC)|0.2.3|Coordenador auxiliar de célula CNC; a trajetória do controlador e a segurança da máquina permanecem nativas.|
|[HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER)|0.2.0|Coordenador auxiliar de célula a laser que não pode armar, disparar ou sobrepor intertravamentos a laser.|
|[HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS)|0.1.4|Fronteira de coordenação para droides bípedes/humanoides: vocabulário de ação nomeado (andar/pegar/colocar) intermediado pelo contrato de segurança partilhado; marcha e equilíbrio permanecem no controlador próprio do droide.|
|[HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR)|0.1.6|Fronteira de coordenação para frotas AGV/AMR: transformação de referencial de fábrica para local mais um vocabulário de ordens inspirado em VDA-5050; o planeamento de caminhos permanece com a navegação do próprio AMR.|
|[HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV)|0.1.7|Fronteira de coordenação para UAVs equipados com câmara: vocabulário de solicitação de voo nomeado mais um watchdog determinístico de falha por perda de heartbeat/ligação.|

### 🛠️ Ferramentas Complementares

|Repositório|Versão|Descrição|
|-|-|-|
|[HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH)|0.2.7|Dashboard de emergência vestível com alertas de segurança hápticos.|
|[HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI)|0.2.0|Interface de linha de comando para automação de frotas, flashing e devops.|
|[HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI)|0.1.9|Extensão de IA para dashboards web fornecendo insights em linguagem natural.|
|[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)|0.5.1|Ferramenta GUI/CLI multiplataforma para detectar, instalar e atualizar manualmente cada projeto do ecossistema.|
|[HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER)|0.3.4|Ferramenta de desktop Windows/Linux que compila uma imagem CM5 pronta para flash, pré-carregada com as versões mais atuais do ecossistema e configuração de primeiro boot estilo Raspberry-Pi-Imager.|
|[HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT)|0.2.1|Coordenador de incidentes de manutenção: um papel de borda (edge) de baixo privilégio recolhe um instantâneo higienizado de inventário/saúde, um papel de plano de controlo o torna apenas leitura e pede a um provedor de IA para sugerir um diagnóstico — nunca aplica patch ou implanta nada.|
|[HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER)|0.2.0|Host de desenvolvimento reprodutível: um esquema de configuração protegido por políticas e inventário de manifestos hoje, evoluindo para um executor isolado de tarefas/espaço de trabalho coordenado com o OPS-AGENT — nenhuma tarefa tem permissão de implementação a menos que um documento conceda explicitamente.|
|[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)|0.0.6|Arquitetura, interfaces, linha de base de segurança, matriz de capacidades e catálogo de projetos gerado do ecossistema, além das ferramentas que comparam todos os repositórios.|

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

**URTC (Universal Robot Tool Controller)** é um produto próprio, não uma pasta de subsistema do HYDRA-UMC: firmware em tempo real e uma família de ferramentas desktop/web para o efetuador final de um robô, desenvolvidas, versionadas e mantidas de forma independente. Um trocador de ferramentas equipado com URTC se coordena com o controlador de célula do HYDRA-UMC via FDCAN, mas o comportamento em tempo real da própria ferramenta, o watchdog e o estado seguro são autoridade própria do URTC — o controlador de célula não pode burlá-lo, e o URTC não depende do HYDRA-UMC para ser desenvolvido, gravado ou diagnosticado.

**Atualizador:** [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) deteta, instala e atualiza os repositórios deste ecossistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) faz o mesmo para os quatro.

<!-- progress:urtc -->
`\[███████░░░░░░░░░░░░░] 35%` — Calculado a partir de dados reais: a maturidade e a evidência que cada um dos seus 11 repositórios declara no seu próprio manifesto. O marco de 100% é um ecossistema totalmente integrado a funcionar em hardware real.
<!-- /progress:urtc -->

## 🏗️ Como o URTC Funciona

1. **Firmware da ferramenta**: O firmware STM32 próprio do URTC executa cada um dos mais de 25 perfis de ferramentas especializados (garras, dispensadores, sondas, fusos e mais), cada um com seu próprio tempo, limites e comportamento de falha.
2. **Atualização de campo**: O CAN-OTA envia uma nova imagem de firmware sobre o mesmo barramento CAN que a ferramenta já usa, com um caminho SWD/JTAG de chip completo (URTC-FLASHER) como fallback que nunca depende do firmware da própria ferramenta estar ativo.
3. **Diagnóstico ao vivo**: O URTC-TESTER valida o comportamento CAN em tempo real de uma ferramenta contra seu perfil declarado sem uma configuração completa de oficina; o URTC-WEB-STUDIO faz o mesmo a partir de uma aba do navegador via Web Serial, sem nada para instalar.
4. **Armazenamento e ciclo de vida**: O URTC-SMART-RACK segura as ferramentas entre os trabalhos, pré-aquece uma antes de uma transferência e mantém uma trilho de auditoria do ciclo de vida (ciclos, falhas, última calibração) por ferramenta física, não por tipo de ferramenta.
5. **QA Ativa**: O URTC-VISION-TOOL é em si uma ferramenta — uma cabeça de ferramenta com suas próprias câmaras térmica e RGB para inspeção de qualidade em processo, não uma câmara externa parafusada em outra ferramenta.
6. **Base partilhada**: **URTC-COMMON** contém o protocolo CAN da cabeça de ferramenta como dados, com código gerado e vetores de conformidade; **URTC-DOCS** contém a arquitetura, linha de base de segurança e matriz de capacidades. **URTC-DEVTOOLS** guarda, num só conjunto versionado, as ferramentas de repositório que toda a família partilha.

## 🛠️ Pilha Tecnológica

* **Firmware**: STM32, FDCAN (barramento partilhado com o controlador de célula), CAN-OTA, fallback SWD/JTAG.
* **Ferramentas de desktop**: clientes GUI multiplataforma para flashing e diagnósticos (URTC-FLASHER, URTC-TESTER).
* **Ferramentas de navegador**: a API Web Serial para testes de hardware sem instalação (URTC-WEB-STUDIO).
* **Dados de ciclo de vida**: trilho de auditoria não volátil por ferramenta, partilhada com a abordagem de integridade F-RAM própria do HYDRA-UMC.

## 🔒 Segurança

Cada perfil de ferramenta carrega seu próprio watchdog e comportamento de falha, independentemente da camada E-STOP do controlador de célula — uma ferramenta que perde seu orçamento de tempo ou heartbeat CAN vai para seu estado seguro declarado por conta própria, em vez de esperar por um comando externo. O pré-aquecimento do URTC-SMART-RACK é limitado pelos mesmos limites térmicos por ferramenta que seu perfil declara, auditado na mesma trilho de ciclo de vida que uma oficina usa para decidir se uma ferramenta ainda está apta para serviço.

## 📁 Catálogo de Projetos URTC

|Repositório|Versão|Descrição|
|-|-|-|
|[URTC](https://github.com/JuanenRac/URTC)|0.4.2|Firmware do Controlador Universal de Ferramentas de Robô para mais de 25 ferramentas especializadas.|
|[URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER)|0.4.4|Ferramenta GUI para atualizações de firmware CAN-OTA e SWD/JTAG de chip completo.|
|[URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER)|0.4.5|Ferramenta de diagnóstico para validação em tempo real de perfis de ferramentas URTC via CAN.|
|[URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)|0.4.0|Ferramenta Web Serial baseada em navegador para testes e análises de hardware instantâneos.|
|[URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK)|0.2.3|Armazenamento inteligente de ferramentas com pré-aquecimento automático e auditoria de ciclo de vida.|
|[URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL)|0.1.6|Cabeça de ferramenta com câmaras térmica e RGB integradas para QA ativa.|
|[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)|0.2.1|Detecta, instala e atualiza os repositórios URTC numa máquina a partir de seus próprios manifestos.|
|[URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS)|0.1.3|Arquitetura, interfaces, linha de base de segurança, matriz de capacidades, nota de estudo do protocolo CAN e catálogo de projetos gerado do ecossistema URTC, além das ferramentas que comparam todos os repositórios.|
|[URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON)|0.1.2|O protocolo CAN da cabeça de ferramenta como dados: uma especificação, código C, TypeScript e Python gerados, vetores de conformidade e transportes em Python.|
|[URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY)|0.0.4|Gateway à frente do barramento CAN do URTC: lista de identificadores permitidos, limite de taxa e chave de sessão.|
|[URTC-DEVTOOLS](https://github.com/JuanenRac/URTC-DEVTOOLS)|0.0.1|As ferramentas de repositório partilhadas da família URTC num só conjunto versionado, com um ficheiro de bloqueio em cada repositório.|

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

**A.R.M.O.R. (Autonomous Radar \& Multimodal Observation Range)** é um ecossistema público separado de segurança perimetral e automação residencial - sem relação com o HYDRA-UMC ou URTC além do mesmo autor e das mesmas convenções de engenharia (manifestos versionados, contrato de mensagem partilhado, interfaces em oito idiomas). Seus nós de campo monitorizam o perímetro de uma propriedade e sua instalação solar/elétrica; seu servidor central e clientes permitem que um operador veja e atue sobre o que eles relatam. As notas de versão e maturidade abaixo vêm diretamente do manifesto e da matriz de capacidades de cada repositório, a mesma convenção de honestidade que o dashboard do HYDRA-UMC já usa.

**Atualizador:** [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) deteta, instala e atualiza os repositórios deste ecossistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) faz o mesmo para os quatro.

<!-- progress:armor -->
`\[████████████▍░░░░░░░] 62%` — Calculado a partir de dados reais: a maturidade e a evidência que cada um dos seus 19 repositórios declara no seu próprio manifesto. O marco de 100% é um ecossistema totalmente integrado a funcionar em hardware real.
<!-- /progress:armor -->

## 🏗️ Como o A.R.M.O.R. é Construído

1. **Contrato partilhado**: **ARMOR-COMMON** possui o significado da mensagem - JSON Schema, um validador Python e tipos TypeScript/Kotlin gerados que todos os outros repositórios consomem, nunca redefinem.
2. **Nós de campo**: Firmware ESP32-S3 para deteção de radar/presença (**ARMOR-NODE-RADAR**), monitorização de inversor solar e bateria (**ARMOR-NODE-SOLAR**), medição elétrica com comutação (**ARMOR-NODE-ELECTRICAL**), e o painel de alarme da casa (**ARMOR-NODE-ALARM**); um agente Python (**ARMOR-NETWORK**) monitora a rede local da própria casa e a acessibilidade à internet a partir de uma máquina já conectada a ela.
3. **Coordenador central**: **ARMOR-SERVER** mantém estado, utilizadores, alarmes, automações e evidências de câmara; **ARMOR-SERVER-AI** e **ARMOR-VOICE-AI** adicionam uma política visual explicável e intenções de voz offline que nunca acionam nada por conta própria.
4. **Clientes operadores**: **ARMOR-STUDIO** (web), **ARMOR-ANDROID-CONTROL** (móvel) e **ARMOR-IOS-CONTROL** (iPhone) são clientes do servidor central, nunca da rede de campo diretamente. **ARMOR-NODE-HMI** é um painel de toque na parede (um Waveshare ESP32-S3-Touch-LCD-7C-BOX) que mostra o estado, arma e reconhece, e será onde o assistente de voz viverá.
5. **Implementação e testes**: **ARMOR-DEVOPS** implementa todo o gráfico de serviços; **ARMOR-SIMULATOR** reproduz cenários e falhas repetíveis sem hardware real; **ARMOR-HARDWARE** carrega o design do invólucro e sua matriz de aceitação de bancada.
6. **Operações do ecossistema**: **ARMOR-UPDATER** descobre, instala e atualiza cada repositório A.R.M.O.R. numa máquina, o mesmo design atômico por verificação que o HYDRA-UMC-UPDATER; **ARMOR-DOCS** é a documentação de arquitetura canônica e a matriz de capacidades. O **ARMOR-STUDIO** também pode atualizar os serviços na máquina central a partir de pacotes assinados com a chave de lançamento do ecossistema, verificando cada assinatura antes de instalar.

## 🔒 Honestidade e Segurança

O A.R.M.O.R. segue a mesma regra que o próprio dashboard do HYDRA-UMC já aplica: uma afirmação é real apenas quando é verificada, e cada repositório diz claramente o que foi e o que não foi executado em hardware real ainda. Nada neste ecossistema atualmente controla eletricidade da rede (mains) ou acesso físico; os nós de campo observam e relatam, e qualquer capacidade de comutação futura é projetada e revisada antes de ser ativada.

## 📁 Catálogo de Projetos A.R.M.O.R.

|Repositório|Versão|Descrição|
|-|-|-|
|[ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON)|0.8.0.0|Contratos de mensagem, validadores, vetores de conformidade, tipos gerados, OpenAPI, lançador partilhado.|
|[ARMOR-NODE-RADAR](https://github.com/JuanenRac/ARMOR-NODE-RADAR)|0.8.0.7|Firmware de nó de campo ESP32-S3, decodificadores para sensores LD2450, LD2461 e presença, seu núcleo testado em host, atualizações do GitHub com barra de progresso e mapa ao vivo.|
|[ARMOR-NODE-SOLAR](https://github.com/JuanenRac/ARMOR-NODE-SOLAR)|0.6.1|Nó de gateway solar: o firmware ESP32-S3 e seu painel (dez portas seriais), e os protocolos de inversores Voltronic / MPP Solar e baterias Pylontech e ANT-BMS.|
|[ARMOR-NODE-ELECTRICAL](https://github.com/JuanenRac/ARMOR-NODE-ELECTRICAL)|0.5.2|Nó elétrico: o firmware (dezasseis medidores PZEM numa linha serial, painel web, MQTT), as tramas dos medidores, a mensagem das leituras da rede e as regras para comutação.|
|[ARMOR-NODE-ALARM](https://github.com/JuanenRac/ARMOR-NODE-ALARM)|0.5.0|Nó de alarme e painel: seu firmware (zonas cabeadas, sirene, sensores e sirenes Zigbee, painel web em sete idiomas) e as regras de armamento, atrasos, alarme e PIN, testado em computador; continua guardando e assume o rádio Zigbee quando o servidor está ausente. Nunca rodou numa placa.|
|[ARMOR-NODE-HMI](https://github.com/JuanenRac/ARMOR-NODE-HMI)|0.4.2|Painel de toque para o Waveshare ESP32-S3-Touch-LCD-7C-BOX: o estado do sistema num ecrã de parede, armar/desarmar/reconhecer, voz push-to-talk e a página web de um nó; o firmware nunca rodou numa placa.|
|[ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK)|0.1.6|Monitor de rede local: os dispositivos na rede da casa, o estado da internet (e de qual lado é uma queda), o que muda; ele apenas observa.|
|[ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER)|0.8.0.9|Estado central (persistido), utilizadores, histórico de eventos, alarmes, dispositivos, automações, leituras solares e elétricas, rede local, serviços de sistema, watchdog de câmara, câmaras, evidências, auditoria, atualizações de firmware de nó que devem ser assinadas, avisos do Telegram e Home Assistant, comandos de voz e uso de fora de casa (segundo fator, sessões que podem ser encerradas, política remota).|
|[ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI)|0.2.9|Serviço de monitorização de movimento, seleção de perfil visual, política de fusão explicável, registo de motor.|
|[ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION)|0.0.5|Zonas de câmara, máscaras e regras de deteção (vadiagem, um evento por visita); nenhum modelo detector ainda.|
|[ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI)|0.3.2|Serviço de voz offline: quinze comandos em oito idiomas, turnos falados do painel de parede, armar e desarmar confirmados com um token assinado.|
|[ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO)|0.8.1.3|Console de operações, alarmes, dispositivos, automações, utilizadores, histórico, regras de alerta, PTZ, mapa de radar, menus solares e elétricos, rede local, serviços de sistema, clima, localizador e configuração de nós, atualizações de firmware de nós, notificações e um designer de site 2D/3D.|
|[ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL)|0.7.8|Cliente operador Android: armar e desarmar, alarmes, dispositivos, radar ao vivo, inversores solares e baterias, histórico, notificações de alarme, assistente para comandos escritos e falados e o configurador dos nós.|
|[ARMOR-IOS-CONTROL](https://github.com/JuanenRac/ARMOR-IOS-CONTROL)|0.0.1|Cliente de operador para iPhone: estado, armar, alarmes, painéis de alarme, câmaras e o assistente, em oito idiomas.|
|[ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE)|0.2.7|Designs de gabinetes (o gabinete de canto de radar; caixa marcada para os nós solar, elétrico e de alarme) e a matriz de aceitação de bancada.|
|[ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS)|0.6.9|Topologia Compose, instalador de bancada de teste de servidor central, backup e restauração, perfil TLS, broker MQTT próprio, serviços de observação e voz, agente de administração.|
|[ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR)|0.2.9|Cenários e falhas repetíveis.|
|[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)|0.1.7|Detecta, instala e atualiza os repositórios próprios do ecossistema (atômico por verificação, sem necessidade de GITHUB\_TOKEN).|
|[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)|0.8.1.4|Documentação canônica e matriz de capacidades.|

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

**EH3D Fabrication Suite** é um ecossistema de software dedicado e multi-repositório adaptado para prototipagem rápida de placas de circuito impresso (PCB), preparação de caminhos de ferramenta CAM, inspeção por visão computacional, gestão de Pick \& Place (PnP) e controlo CNC/Laser multi-máquina. Ele fornece interoperabilidade nativa com nós de hardware **HYDRA-UMC** (STM32H7 + Jetson Orin NX + Hailo NPU) juntamente com uma frota de máquinas de oficina compreendendo sistemas de fresagem industrial (Bungard CCD via gateways RS-232 ESP32-S3), roteadores CNC (JuanenCNC) e gravadores a laser de diodo (JuanenLaser).

**Atualizador:** [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) deteta, instala e atualiza os repositórios deste ecossistema; [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) faz o mesmo para os quatro.

<!-- progress:eh3d -->
`\[██░░░░░░░░░░░░░░░░░░] 10%` — Calculado a partir de dados reais: a maturidade e a evidência que cada um dos seus 26 repositórios declara no seu próprio manifesto. O marco de 100% é um ecossistema totalmente integrado a funcionar em hardware real.
<!-- /progress:eh3d -->

## 🏗️ Como a EH3D Fabrication Suite Funciona

1. **Gestão Central**: **EH3D-SUITE-LAUNCHER** encontra os programas da suíte pelos seus manifestos, arranca-os e gere o ficheiro de projeto unificado `.eh3dproj`; a descoberta de máquinas na rede (HYDRA-UMC e gateways ESP32) e a orquestração das atualizações estão previstas.
2. **Pipeline de Processamento CAM**: Ferramentas CAD/CAM especializadas lidam com estágios individuais de fabricação:

   * **EH3D-ISOCAM**: Isolamento do cobre de camadas Gerber com deslocamentos exatos e várias passagens; o desbaste do cobre e a estratégia Voronoi estão previstos.
   * **EH3D-DRILLPRO**: Processamento Excellon/NC Drill, tabelas de brocas e ciclos de furação profunda.
   * **EH3D-ROUTEPRO**: Fresagem de contorno de placa, criação de abas (tabs) e estratégias de entrada em rampa.
   * **EH3D-BUNGARD-GUI**: Interface moderna para as máquinas Bungard CCD: um lançador e um visualizador com as vistas em planta e isométrica do trabalho.
   * **EH3D-LASER-CAM**: Algoritmos de tramagem (dithering) raster e modulação de potência vetorial para corte a laser.
   * **EH3D-STENCILCAM**: Processamento de máscara de pasta para geração de stencils de pasta de solda SMD.
3. **Execução e Controlo em Tempo Real**: **EH3D-MOTIONCNC** comanda uma máquina a partir de uma só janela (jog, definição de zero, execução de G-code, vista do trajeto; hoje sobre uma máquina simulada) e é a base dos programas de controlo de máquina, integrado com o **EH3D-SERVER**, que planeia e executa trabalhos de furação e fresagem através do nó da máquina, com o **EH3D-AUTOLEVEL** para o apalpamento topográfico em Z e o **EH3D-NODE-HMI-GUI** para a definição manual de zero (G54/G55) e jogging.
4. **IA de Borda e Inspeção**: **EH3D-VISION-STUDIO** aproveita a NPU Hailo do HYDRA-UMC para realizar alinhamento de câmara em tempo real, deteção automática de fiduciais e inspeção de desgaste de ferramentas.
5. **Montagem e Dados Auxiliares**: **EH3D-PNP-MANAGER** gere coordenadas centroides Pick \& Place e alimentadores (feeders), enquanto **EH3D-TOOL-MANAGER** mantém um base de dados de ferramentas unificado em todos os módulos CAM.

## 📁 Catálogo de Projetos EH3D Fabrication Suite

### 💠 Controlo central e clientes do operador
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-SUITE-LAUNCHER](https://github.com/JuanenRac/EH3D-SUITE-LAUNCHER)|0.0.1|Encontra os programas da suíte pelos seus manifestos, arranca-os e guarda os projetos recentes e o ficheiro de projeto (.eh3dproj) com o SHA-256 dos seus ficheiros; a janela e a descoberta de máquinas na rede estão previstas.|
|[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)|0.0.7|Modelo de dados partilhado: o contentor de projeto .eh3dproj com verificações de integridade, os tipos de telemetria da máquina e a base de firmware copiada por cada nó ESP32.|
|[EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS)|0.0.2|Documentação do ecossistema, guias de montagem, especificações técnicas de gateway e manuais de integração.|
|[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)|0.0.2|Leitores em Rust para Gerber RS-274X, ficheiros de furação Excellon e G-code (dialetos GRBL, Marlin e PlanetCNC), tolerantes a ficheiros danificados.|
|[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)|0.0.2|Detecta, instala e atualiza os próprios repositórios do ecossistema (atômico por verificação, sem necessidade de GITHUB\_TOKEN).|
|[EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER)|0.0.2|Servidor em Rust com interface REST e websocket: utilizadores, máquinas e trabalhos, planeamento de trabalhos de furação e fresagem com as bibliotecas do DRILLPRO e do ROUTEPRO, um trabalho de cada vez por máquina.|
|[EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)|0.0.2|Cliente web em Rust do EH3D-SERVER.|

### 💠 Projetos de furação, contorno e fresagem:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO)|0.0.8|Reimplementação em Rust do fluxo de furação do software DOS clássico para as máquinas Bungard CCD: interface em modo de texto em oito idiomas, simulador ou máquina real.|
|[EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)|0.0.8|Reimplementação em Rust do fluxo de fresagem do software DOS clássico para as máquinas Bungard CCD, a partir de ficheiros de traçado HP-GL: interface em modo de texto em oito idiomas, simulador ou máquina real.|
|[EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI)|0.1.2|Interface moderna para as máquinas Bungard CCD: um lançador dos programas clássicos de furação e fresagem e um visualizador do trabalho sobre a mesa.|
|[EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)|0.0.4|Base comum dos programas de controlo de máquina do EH3D: uma janela que comanda uma máquina simulada com jog, definição de zero, execução de G-code e vista do trajeto, em oito idiomas.|
|[EH3D-TOOL-MANAGER](https://github.com/JuanenRac/EH3D-TOOL-MANAGER)|0.0.1|Base de dados de ferramentas partilhado a rastrear horas de desgaste, predefinições de corte e avanços em todas as ferramentas CAM EH3D.|

### 💠 Projetos laser:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-LASER-CAM](https://github.com/JuanenRac/EH3D-LASER-CAM)|0.0.1|Aplicação CAM a laser para dithering de imagem, conversão raster/vetor e controlo dinâmico de potência PWM.|

### 💠 Projetos CAM:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-ISOCAM](https://github.com/JuanenRac/EH3D-ISOCAM)|0.0.1|Fresagem de isolamento do cobre de uma camada Gerber: deslocamentos exatos do cobre, várias passagens, verificação de espaços que a ferramenta não consegue cortar e G-code; a janela, o desbaste do cobre e a estratégia Voronoi estão previstos.|
|[EH3D-CAM-DEBUGGER](https://github.com/JuanenRac/EH3D-CAM-DEBUGGER)|0.0.1|Verifica um programa G-code antes de chegar a uma máquina: o seu tempo com a aceleração da máquina e alertas para movimentos rápidos para o material, movimentos fora da mesa, cortes com o fuso parado e cabeçotes sobre grampos; a simulação 3D está prevista.|

### 💠 Projetos Gerber:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-GERBERVIEWER](https://github.com/JuanenRac/EH3D-GERBERVIEWER)|0.0.1|Ferramenta de inspeção CAM leve para alinhamento de camadas Gerber e visualização rápida.|

### 💠 Projetos Pick&Place:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-STENCILCAM](https://github.com/JuanenRac/EH3D-STENCILCAM)|0.0.1|Utilitário de conversão de máscara de pasta gerando caminhos de corte para fabricação de stencils SMD a laser e plotter.|
|[EH3D-PNP-MANAGER](https://github.com/JuanenRac/EH3D-PNP-MANAGER)|0.0.1|Montagem pick and place: ficheiros de posições do KiCad e CSV, alimentadores e a ordem de colocação para um cabeçote de um a seis bicos; a câmara e o controlo da máquina estão previstos.|

### 💠 Projetos de nós:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)|0.0.4|Nó ESP32-S3 para a caixa de uma máquina Bungard CCD: o RS-232 da sua unidade de controlo por Ethernet ou Wi-Fi, com as lâmpadas da máquina e o variador do fuso na mesma placa.|
|[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)|0.0.3|Ecrã tátil de 10,1 polegadas com um ESP32-P4 que controla uma máquina Bungard CCD: os ecrãs do programa de secretária, alertas e ordens faladas em oito idiomas e uma paragem por hardware que não passa pelo ecrã.|
|[EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX)|0.0.5|Nó ESP32-S3 para a cabeça de furação de uma máquina Bungard CCD: o vídeo da sua câmara (OV2640 ou OV5640) como câmara IP (RTSP e ONVIF), a altura da mesa medida com um laser, a velocidade e a temperatura do fuso e uma saída de proteção.|
|[EH3D-NODE-HMI-GUI](https://github.com/JuanenRac/EH3D-NODE-HMI-GUI)|0.0.1|Controlador manual tátil de 10 polegadas / móvel de uso geral com ESP32-P4/ESP32-C6 para o movimento em tempo real (jog), a colocação a zero (G54/G55) e a paragem de emergência.|

### 💠 Projetos FENIX:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-FENIX-PCB](https://github.com/JuanenRac/EH3D-FENIX-PCB)|0.0.1|Ambiente EDA: captura de esquemas, desenho de PCB, ferramentas de verificação, simulação de circuitos e módulos especializados para fontes comutadas (SMPS) e RF.|
|[EH3D-FENIX-CAD](https://github.com/JuanenRac/EH3D-FENIX-CAD)|0.0.1|CAD mecânico paramétrico centrado no projeto de caixas, chassis e dissipadores térmicos.|
|[EH3D-DESIGN-VERIFIER](https://github.com/JuanenRac/EH3D-DESIGN-VERIFIER)|0.0.1|Verificador de engenharia abrangente para validações cruzadas e controlo de qualidade do projeto.|
|[EH3D-VALIDATION-LAB](https://github.com/JuanenRac/EH3D-VALIDATION-LAB)|0.0.1|Ambiente de testes responsável por gerir os casos de uso de referência e os testes de regressão do sistema.|
|[EH3D-DESIGN-HISTORY](https://github.com/JuanenRac/EH3D-DESIGN-HISTORY)|0.0.1|Sistema de controlo de versões que guarda o histórico semântico e a evolução lógica do projeto.|
|[EH3D-PROJECT-PASSPORT](https://github.com/JuanenRac/EH3D-PROJECT-PASSPORT)|0.0.1|Gerador do passaporte técnico armazenável e reproduzível para a auditoria completa de um projeto.|
|[EH3D-COMPONENT-INTELLIGENCE](https://github.com/JuanenRac/EH3D-COMPONENT-INTELLIGENCE)|0.0.1|Base de dados técnica avançada enriquecida com metadados sobre componentes eletrónicos.|
|[EH3D-MANUFACTURING-PROFILE](https://github.com/JuanenRac/EH3D-MANUFACTURING-PROFILE)|0.0.1|Gestor de perfis das capacidades da maquinaria de cada fábrica e das restrições técnicas dos fornecedores.|
|[EH3D-THERMAL-LAB](https://github.com/JuanenRac/EH3D-THERMAL-LAB)|0.0.1|Laboratório de simulação térmica progressiva acoplado diretamente ao projeto físico.|
|[EH3D-LAB-BRIDGE](https://github.com/JuanenRac/EH3D-LAB-BRIDGE)|0.0.1|Módulo de correlação que serve de ponte direta entre os dados de simulação e as medições reais de laboratório.|
|[EH3D-DESIGN-EXPLORER](https://github.com/JuanenRac/EH3D-DESIGN-EXPLORER)|0.0.1|Ambiente de exploração para comparar e analisar alternativas ou ramos do projeto.|

### 💠 Projetos ANDROID/IOS:
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-ANDROID-CONTROL](https://github.com/JuanenRac/EH3D-ANDROID-CONTROL)|0.0.2|Aplicação Android cliente do EH3D-SERVER.|
|[EH3D-IOS-CONTROL](https://github.com/JuanenRac/EH3D-IOS-CONTROL)|0.0.2|Aplicação iOS cliente do EH3D-SERVER.|

### 🛠️ Ferramentas complementares
|Repositório|Versão|Descrição|
|-|-|-|
|[EH3D-VISION-STUDIO](https://github.com/JuanenRac/EH3D-VISION-STUDIO)|0.0.1|Encontra marcas fiduciais redondas numa imagem, converte píxeis em milímetros, corrige a distorção da lente e calcula a rotação e o deslocamento de uma placa; a câmara em direto, a rede neuronal e a janela estão previstas.|
|[EH3D-AUTOLEVEL](https://github.com/JuanenRac/EH3D-AUTOLEVEL)|0.0.1|Processador de malha de altura topográfica (Z-Probing) e interpolação de G-code para compensação de superfície.|

\---

## 🤝 Contribuindo

Cada ecossistema é sua própria iniciativa com seus próprios projetos. Cada projeto tem suas próprias diretrizes de contribuição. Consulte os repositórios individuais para detalhes técnicos.

Os rótulos (labels) de issues são padronizados em cada repositório HYDRA-UMC a partir do ficheiro [`.github/labels.yml`](.github/labels.yml) neste mesmo repositório, sincronizado por [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) — edite esse único ficheiro para alterar um rótulo em todos os lugares de uma só vez, em vez de manualmente por repositório. Ao contrário do dashboard abaixo, esta lista é estática (uma matriz real do GitHub Actions, não descoberta dinâmica) - um repositório recém-adicionado precisa de uma entrada lá também, não apenas de um `hydra-umc.project.json` real.

Um dashboard de status ao vivo cobrindo cada repositório público dos quatro ecossistemas - cada um descoberto pelo seu próprio manifesto (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`, mais `electro-hobby-3d.project.json` para os repositórios inter-ecossistemas), lido direto do branch padrão de cada repositório sem lista fixa - é regenerado por [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) imediatamente quando um projeto faz push (o `dashboard-dispatch.yml` próprio de cada repositório) e, como rede de segurança, duas vezes por hora, e servido a partir de `docs/` via GitHub Pages: [**juanenrac.github.io/JuanenRac**](https://juanenrac.github.io/JuanenRac/). Ele mostra pilha, alvo de implementação e versão atual, uma classificação real de maturidade por projeto (scaffolding / functional / established / production, cada uma decidida a partir do CHANGELOG desse projeto — veja [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)), seu papel (API / UI / CLI / firmware / biblioteca / serviço / ferramenta), uma árvore de família pai-filho e notas por projeto sobre o que está implementado hoje. O ficheiro [`ecosystem-catalog.json`](ecosystem-catalog.json) lista esses ecossistemas e seus manifestos num só lugar, e a construção do dashboard recusa-se a executar se os dois discordarem.

## 🧭 Colaboração no GitHub

O [modelo de colaboração do GitHub](docs/GITHUB_COLLABORATION.md) define uma Wiki central, um Projeto de ecossistema, escopo de Discussões, critérios de lançamento e a fronteira de automação partilhada. Os formulários de issue mantidos centralmente ([`ISSUE\_TEMPLATE`](.github/ISSUE_TEMPLATE/)) e o modelo de pull-request ([`PULL\_REQUEST\_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)) tornam o trabalho de software, validação de hardware e documentação rastreável sem duplicar manuais de projetos.

O workflow de saúde da comunidade é intencionalmente manual e de simulação (dry-run) por defeito. Uma vez que o `COMMUNITY\_HEALTH\_SYNC\_TOKEN` esteja configurado, ele pode copiar apenas estes modelos geridos para cada repositório que publica um manifesto HYDRA-UMC; ele nunca exclui um modelo específico de projeto.

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licença GPL-3.0.

