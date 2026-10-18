<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/ELECTRO_HOBBY_3D_BANNER.svg" alt="Banner da Electro Hobby 3D" width="100%">
</p>

# Electro Hobby 3D 🤖🚀

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  🇵🇹 <b>Português</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="License GPL 3.0">
  <img src="https://img.shields.io/badge/Hardware-CERN%20OHL--S-orange.svg" alt="Hardware CERN OHL">
  <img src="https://img.shields.io/badge/Ecosystems-3-00E5FF.svg" alt="Three ecosystems">
</p>

Três ecossistemas de engenharia independentes, um só autor. O **HYDRA-UMC** é uma plataforma de robótica industrial em várias camadas, desde o firmware em tempo real até à IA cognitiva. O **URTC** é o seu subsistema universal de ferramentas para robôs: firmware em tempo real e ferramentas de ambiente de trabalho/web para o efetuador final do próprio robô, desenvolvido como produto próprio, com versões independentes e ferramentas de manutenção próprias. O **A.R.M.O.R.** é um ecossistema separado e público de segurança perimetral e domótica - deteção de presença por radar, monitorização solar e elétrica, e um coordenador central com clientes web e móveis.

---

# 🐙 HYDRA-UMC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/HYDRA_BANNER.svg" alt="Banner do ecossistema HYDRA-UMC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32%20%7C%20CM5-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Hailo--8%20%7C%20Hailo--10-green.svg" alt="AI Power">
  <img src="https://img.shields.io/badge/Stack-React%20%7C%20Flutter%20%7C%20Python-blueviolet.svg" alt="Stack">
</p>

Bem-vindo ao **ecossistema HYDRA-UMC**, uma plataforma de robótica industrial em várias camadas que abrange desde o firmware de baixo nível em tempo real até à IA cognitiva de alto nível. Esta organização aloja muitos projetos especializados, concebidos para funcionar em perfeita sincronia na automatização de microfábricas e na robótica de enxame.

## 📈 Progresso do ecossistema

`[██████████▊░░░░░░░░░] 54%` — Apenas como referência. O marco dos 100% é um ecossistema totalmente integrado a funcionar em hardware real.

> [!IMPORTANT]
> 🛠️ **Projeto em pausa — a construir o hardware real.** O desenvolvimento ativo está parado enquanto se constrói de verdade a célula robótica física (estruturas, cablagem, as placas CM5 e STM32 reais), para que a fase seguinte do trabalho tenha hardware real onde correr e validar, e não apenas uma barra a subir. O trabalho retoma quando essa construção estiver concluída.

---

## 🚀 Funcionalidades principais e escalabilidade

- **Escalabilidade multirrobô**: Suporta até 8 unidades robóticas distribuídas (de 3, 4, 5 e 6 GDL atualmente; com escalamento para 7, 8, 9 GDL e arquiteturas de robô duplo em versões futuras).
- **Estágio local integrado**: A placa principal do HYDRA-UMC inclui um **estágio local de 6 eixos** integrado para tarefas auxiliares, como robôs secundários, revólveres ATC (trocador automático de ferramentas), sincronização de tapetes transportadores ou pórticos de mesa XYZ.

---

## 🏗️ Arquitetura do ecossistema

O ecossistema v1.1 é uma plataforma de produto em camadas: assenta em tecnologia Linux e Raspberry Pi consolidada, em vez de criar um novo sistema operativo ou substituir as APIs dos fabricantes.

1.  **Base da plataforma**: o Raspberry Pi OS ARM64 e os serviços Linux padrão fornecem a base suportada do CM5.
2.  **Plataforma e contratos**: o **HYDRA-UMC-OS** empacota perfis reproduzíveis, serviços, diagnósticos e atualizações no Raspberry Pi OS; o **HYDRA-UMC-SDK** publica contratos versionados, clientes leves e dados de conformidade.
3.  **Execução em tempo real**: o firmware do **HYDRA-UMC** é responsável pelos limites de movimento, pelos watchdogs e pela paragem segura no STM32/MCU; a ferramenta em si, e a sua própria autoridade em tempo real sobre o efetuador final, pertence ao ecossistema **URTC**, separado, descrito abaixo.
4.  **Coordenação e operações**: os serviços do servidor, o despacho de tarefas, a telemetria e a configuração coordenam os dispositivos sem contornar o limite de segurança do MCU.
5.  **Interfaces do operador**: os clientes Studio, Suite, DSI, web, ambiente de trabalho, móveis e CLI usam os contratos do SDK.
6.  **Perceção e inteligência**: os serviços de visão, Hailo e cognitivos propõem observações ou planos; não têm autoridade de segurança física.
7.  **Engenharia, indústria e dados**: o Digital Twin, o HIL/física, as gateways OPC-UA/MQTT/MTConnect e os serviços de dados validam e integram o sistema.

Para orientação sobre a implementação, comece pela documentação pública de arquitetura e serviços do **HYDRA-UMC-OS** e depois use os contratos e as regras de conformidade do **HYDRA-UMC-SDK**. A autoridade de segurança do MCU é preservada em todos os fluxos.

---

## 🛠️ Stack tecnológica e ferramentas

O ecossistema aproveita uma stack moderna e de alto desempenho para uma fiabilidade crítica para a missão:

### 💠 Embebido e tempo real (Execução)
- **Microcontroladores**: STM32H745 (Dual-Core 480MHz), STM32G474 (170MHz), STM32F303.
- **Frameworks**: FreeRTOS (modo AMP), CMSIS-DSP, STM32 HAL/LL.
- **Protocolos**: FDCAN (1Mbps/5Mbps), CAN-OTA, SPI (IPC escravo a 50MHz), I2C, UART.
- **Cinemática**: geração de perfis em curva S, cinemática inversa (IK) em tempo real.

### 🧠 IA de borda e perceção (Inteligência)
- **Aceleradores**: Hailo-8 (26 TOPS) para visão com 8 câmaras, Hailo-10 (40 TOPS) para IA generativa.
- **Modelos**: YOLOv10 (deteção), OpenVLA (ação), Whisper (voz), Llama-3 (raciocínio).
- **Entre nós**: gRPC sobre Protobuf e troca de metadados SPI-DMA de alta velocidade.

### 🌐 Backend e coordenação (Coordenação)
- **Runtimes**: Node.js 20+ (API), Rust 1.80+ (Orquestrador), Go (CLI).
- **Infraestrutura**: Express, Fastify, Socket.io (WebSocket), gRPC.
- **Base de dados**: InfluxDB/TimescaleDB (telemetria), Redis (estado), SQLite.

### 💻 Painéis e interface de utilizador (Interface)
- **Web**: React 19, Vite, Three.js (viewport 3D), Tailwind CSS.
- **Nativo**: Python 3.12/PySide6 (Suite), Kotlin (Android nativo), Flutter 3.x (iOS e DSI).

---

## 📋 Requisitos do sistema

- **Nó de computação**: Raspberry Pi CM5 (4GB+ de RAM) com armazenamento NVMe/eMMC.
- **Hardware de IA**: módulos M.2 Hailo-8/Hailo-10 (Key M).
- **Barramento de campo**: Gigabit Ethernet para a LAN e FDCAN (ISO 11898-1:2015) para os atuadores.
- **SO dos clientes**: Android 10+, iOS 15+, Windows 10/11 (High-DPI), Ubuntu 22.04 LTS.

---

## 🔒 Segurança industrial e cibersegurança

- **Camada de E-STOP**: linha de emergência cablada + tramas de emergência CAN de alta prioridade (<1ms).
- **Segurança da IA**: zonas de segurança 3D com corte automático do binário dos motores perante intrusão humana.
- **Cibersegurança**: autenticação sem estado baseada em JWT + mTLS para um tráfego entre nós seguro.
- **Integridade**: F-RAM não volátil para auditoria do ciclo de vida da ferramenta e recuperação do estado.

---

## 🔧 Hardware Hacking: construir a sua própria placa de suporte

A Robot Controller Board é construída em torno de um **Raspberry Pi CM5**, e o conector duplo Hirose DF40 do próprio CM5 tem uma disposição de pinos fixa, oficial e pública (Tabela 5 da folha de dados do CM5 da própria Raspberry Pi) - não é algo que este projeto defina. Isso significa que uma placa de suporte compatível de terceiros é um projeto real e exequível, e não um exercício de engenharia inversa:

- **Comece aqui**: [`HYDRA-UMC/docs/PINOUT_CM5_CARRIER.TXT`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/PINOUT_CM5_CARRIER.TXT) - quais dos pinos fixos do CM5 esta placa utiliza de facto (Ethernet, os 2 PHY nativos USB3 SuperSpeed, o conector da ventoinha de refrigeração do lado do CM5) e porquê, reorganizados por função a partir da tabela oficial de pinos.
- **A porta de entrada fácil**: o **conector GPIO de 40 pinos do Raspberry Pi** padrão (a mesma disposição "B+" inalterada desde 2014) está exposto nesta placa exatamente como em qualquer Raspberry Pi - os HATs de RPi e as ferramentas de GPIO existentes funcionam sem modificações. Algumas posições que a própria ligação STM32 desta placa já utiliza estão serigrafadas/assinaladas para saber quais evitar.
- **Ir mais longe**: [`docs/architecture.md`](https://github.com/JuanenRac/HYDRA-UMC/blob/main/docs/architecture.md) explica como o CM5, o "Kinematic Brain" STM32H745 e o "Robot Controller" STM32G474 comunicam de facto entre si (SPI1 + FDCAN1 + a caixa de correio IPC CM7↔CM4) - a camada que um redesenho da placa de suporte teria de preservar para se manter compatível com o firmware deste projeto.
- Cada documento de pinout indica com clareza se está **CONFIRMED** (tirado diretamente de uma tabela oficial da folha de dados) ou **PROPOSED** (uma escolha de encaminhamento própria deste projeto, aberta a outra diferente numa placa derivada) - leia essa linha de estado antes de tratar uma atribuição de sinal como fixa.

Isto não é um tutorial guiado (não existe uma única placa de suporte "certa" para todos os casos de uso) - é o material de referência real de que um projetista de hardware experiente precisa para partir de um mapa de pinos fiável, em vez de apenas de uma folha de dados.

---

## 📁 Catálogo de projetos HYDRA-UMC

É novo no ecossistema? O `./starter-kit.sh` (ou `starter-kit.bat` no
Windows) clona 13 repositórios essenciais - um conjunto inicial escolhido a
dedo - como irmãos numa mesma pasta: a disposição padrão que todos os
scripts entre repositórios aqui já assumem. Um segundo argumento clona um
ecossistema inteiro, descoberto em direto pelo seu manifesto: `hydra-umc`,
`urtc`, `armor` ou `all` (por exemplo `./starter-kit.sh ~/work armor`).
Voltar a executá-lo é seguro: tudo o que já estiver clonado fica intacto. A
partir daí, o atualizador de cada ecossistema - ou o
[ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)
para os três - pode verificar versões e compilar/atualizar qualquer outro projeto.

### 🧱 Base da plataforma e contratos
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-OS](https://github.com/JuanenRac/HYDRA-UMC-OS) | 0.5.2 | Camada de plataforma Raspberry Pi OS para o CM5: perfis reproduzíveis, configuração, diagnósticos, ciclo de vida dos serviços e atualizações; não é uma nova distribuição Linux. |
| [HYDRA-UMC-SDK](https://github.com/JuanenRac/HYDRA-UMC-SDK) | 0.3.4 | Contratos versionados partilhados, clientes leves e dados de conformidade para serviços, interfaces e adaptadores CM5; não substitui as APIs dos fabricantes. |
| [HYDRA-UMC-CONNECTOR-HUB](https://github.com/JuanenRac/HYDRA-UMC-CONNECTOR-HUB) | 0.1.4 | Registo e validador declarativos de manifestos de adaptadores para conectores de máquinas externas; estende a própria ideia de contrato do SDK a máquinas externas sem substituir os projetos de gateway industrial. |

### 💠 Controlo central e clientes do operador
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC) | 0.2.2 | Firmware central de controlo de movimento para STM32H745/G474 com cinemática em curva S. |
| [HYDRA-UMC-SERVER](https://github.com/JuanenRac/HYDRA-UMC-SERVER) | 0.8.1.0 | Backend headless de API e WebSocket em Node.js para a orquestração robótica. |
| [HYDRA-UMC-STUDIO](https://github.com/JuanenRac/HYDRA-UMC-STUDIO) | 0.8.0.0 | Painel web avançado baseado em React para a monitorização e o controlo 3D de robôs. |
| [HYDRA-UMC-SUITE](https://github.com/JuanenRac/HYDRA-UMC-SUITE) | 0.6.9 | Aplicação de ambiente de trabalho de alto desempenho em Python/Qt para automatização industrial. |
| [HYDRA-UMC-DSI](https://github.com/JuanenRac/HYDRA-UMC-DSI) | 0.2.6 | Interface tátil dedicada, baseada em Flutter, para ecrãs industriais de 7" (CM5). |
| [HYDRA-UMC-ANDROID-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-ANDROID-CONTROL) | 0.7.1 | Aplicação móvel nativa em Kotlin com início de sessão biométrico para a gestão remota de robôs. |
| [HYDRA-UMC-IOS-CONTROL](https://github.com/JuanenRac/HYDRA-UMC-IOS-CONTROL) | 0.2.6 | Aplicação móvel Flutter para iOS/iPadOS com sincronização WebSocket em tempo real. |
| [HYDRA-UMC-EDITOR-URDF](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-URDF) | 0.1.4 | Editor gráfico de URDF para validar e enviar modelos de robôs para o catálogo. |
| [HYDRA-UMC-EDITOR-STL](https://github.com/JuanenRac/HYDRA-UMC-EDITOR-STL) | 0.1.6 | Editor de modelos STL para ambiente de trabalho - transforma, substitui, remove e adiciona peças reais no catálogo de modelos partilhado. |

### 👁️ Nó de IA de visão (otimizado para Hailo-8)
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-VISION-NODE](https://github.com/JuanenRac/HYDRA-UMC-VISION-NODE) | 0.1.5 | Nó de perceção de alta velocidade para 8 fluxos simultâneos de câmaras USB 3.0. |
| [HYDRA-UMC-VISION-STREAMER](https://github.com/JuanenRac/HYDRA-UMC-VISION-STREAMER) | 0.2.0 | Pipeline GStreamer/MediaMTX otimizado para a retransmissão de vídeo industrial. |
| [HYDRA-UMC-DETECTION-HEF](https://github.com/JuanenRac/HYDRA-UMC-DETECTION-HEF) | 0.1.4 | Biblioteca de modelos YOLO acelerados por hardware para o controlo de qualidade de SMD e componentes. |
| [HYDRA-UMC-SAFETY-ZONES](https://github.com/JuanenRac/HYDRA-UMC-SAFETY-ZONES) | 0.1.4 | Deteção de intrusão por IA em tempo real para proteger o volume de trabalho do robô. |
| [HYDRA-UMC-VISUAL-SERVOING-API](https://github.com/JuanenRac/HYDRA-UMC-VISUAL-SERVOING-API) | 0.1.9 | Retroalimentação cinemática baseada em imagem para correção de pose submilimétrica. |

### 🧠 Nó de IA cognitiva (otimizado para Hailo-10)
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-COGNITIVE-NODE](https://github.com/JuanenRac/HYDRA-UMC-COGNITIVE-NODE) | 0.1.4 | Nó de raciocínio semântico para o planeamento lógico de missões e o controlo por voz. |
| [HYDRA-UMC-VLA-ENGINE](https://github.com/JuanenRac/HYDRA-UMC-VLA-ENGINE) | 0.1.7 | Implementação de modelos Vision-Language-Action para a execução de tarefas complexas. |
| [HYDRA-UMC-VOICE-UI](https://github.com/JuanenRac/HYDRA-UMC-VOICE-UI) | 0.1.7 | Pipeline STT/TTS local e privado para a interação do operador em linguagem natural. |
| [HYDRA-UMC-SEMANTIC-PLANNER](https://github.com/JuanenRac/HYDRA-UMC-SEMANTIC-PLANNER) | 0.1.3 | Orquestrador de missões baseado em LLM com recuperação de erros sensível ao contexto. |
| [HYDRA-UMC-DOCS-QA](https://github.com/JuanenRac/HYDRA-UMC-DOCS-QA) | 0.1.4 | Assistente de IA baseado em RAG treinado com manuais técnicos e código-fonte. |
| [HYDRA-UMC-LOCAL-TECHNICIAN](https://github.com/JuanenRac/HYDRA-UMC-LOCAL-TECHNICIAN) | 0.1.6 | Técnico de manutenção de IA local e sujeito a políticas: hoje uma política fixa de níveis de risco e uma lista de ferramentas permitidas, com uma defesa real e testada que prova que um documento malicioso recuperado nunca pode desencadear uma chamada a uma ferramenta nem divulgar um segredo - a IA nunca obtém autoridade por gerar uma resposta. |

### 🐝 Orquestração e enxame
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-ORCHESTRATOR](https://github.com/JuanenRac/HYDRA-UMC-ORCHESTRATOR) | 0.1.8 | Gestor de frota para a coordenação multirrobô e a prevenção de colisões. |
| [HYDRA-UMC-SWARM-SYNC](https://github.com/JuanenRac/HYDRA-UMC-SWARM-SYNC) | 0.1.4 | Sincronização PTP (Precision Time Protocol) para a sincronização de robôs ao nanossegundo. |
| [HYDRA-UMC-PATH-PLANNER-3D](https://github.com/JuanenRac/HYDRA-UMC-PATH-PLANNER-3D) | 0.1.0 | Otimizador distribuído de trajetórias para enxames de robôs em espaços de trabalho partilhados. |
| [HYDRA-UMC-JOB-DISPATCHER](https://github.com/JuanenRac/HYDRA-UMC-JOB-DISPATCHER) | 0.2.2 | Escalonador de tarefas por prioridade para frotas de robôs heterogéneas. |
| [HYDRA-UMC-NODE-HEALING](https://github.com/JuanenRac/HYDRA-UMC-NODE-HEALING) | 0.1.7 | Monitor de alta disponibilidade com failover transparente de missões. |

### 🎮 Gémeo digital e simulação
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-TWIN](https://github.com/JuanenRac/HYDRA-UMC-TWIN) | 0.0.9 | Motor de simulação física de alta fidelidade para testar robôs sem riscos. |
| [HYDRA-UMC-PHYSICS-REPLICA](https://github.com/JuanenRac/HYDRA-UMC-PHYSICS-REPLICA) | 0.0.8 | Simulação física do mundo real (MuJoCo/PhysX) de cadeias URDF. |
| [HYDRA-UMC-HIL-BRIDGE](https://github.com/JuanenRac/HYDRA-UMC-HIL-BRIDGE) | 0.0.9 | Interface de hardware-in-the-loop para sincronizar comandos reais e virtuais. |
| [HYDRA-UMC-SYNTHETIC-DATA-GEN](https://github.com/JuanenRac/HYDRA-UMC-SYNTHETIC-DATA-GEN) | 0.1.0 | Gerador procedimental de conjuntos de dados de treino para os nós de visão. |

### 📊 Dados e análise
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-DATALAKE](https://github.com/JuanenRac/HYDRA-UMC-DATALAKE) | 0.1.8 | Armazenamento Big Data para dados robóticos industriais massivos. |
| [HYDRA-UMC-TELEMETRY-COLLECTOR](https://github.com/JuanenRac/HYDRA-UMC-TELEMETRY-COLLECTOR) | 0.1.7 | Recetor de alto débito para registos de CAN, WebSocket e do sistema. |
| [HYDRA-UMC-ANOMALY-DETECTOR](https://github.com/JuanenRac/HYDRA-UMC-ANOMALY-DETECTOR) | 0.1.7 | Motor de manutenção preditiva baseado nas assinaturas de vibração dos motores. |
| [HYDRA-UMC-PRODUCTION-REPORTS](https://github.com/JuanenRac/HYDRA-UMC-PRODUCTION-REPORTS) | 0.1.5 | Geração automática de OEE e KPI para a gestão de fábricas industriais. |

### 🏭 Gateway industrial
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-GATEWAY-INDUSTRIAL](https://github.com/JuanenRac/HYDRA-UMC-GATEWAY-INDUSTRIAL) | 0.1.5 | Ponte de interoperabilidade da Indústria 4.0 para os padrões de fábrica (OPC-UA/MQTT). |
| [HYDRA-UMC-OPCUA-SERVER](https://github.com/JuanenRac/HYDRA-UMC-OPCUA-SERVER) | 0.1.9 | Mapeamento dos objetos robóticos HydraState para nós OPC-UA padrão. |
| [HYDRA-UMC-MQTT-BROKER](https://github.com/JuanenRac/HYDRA-UMC-MQTT-BROKER) | 0.1.6 | Ponte de telemetria para integrações IoT e painéis externos. |
| [HYDRA-UMC-MTCONNECT-ADAPTER](https://github.com/JuanenRac/HYDRA-UMC-MTCONNECT-ADAPTER) | 0.1.8 | Interface normalizada para a monitorização do estado de máquinas-ferramenta e robôs. |

### 🌉 Pontes de automatização externas
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-BRIDGE-ROS2](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-ROS2) | 0.1.2 | Fronteira bidirecional de coordenação com o ROS 2: tópicos para observação, serviços para inspeção e ações canceláveis para as tarefas da célula. |
| [HYDRA-UMC-BRIDGE-OPENPNP](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-OPENPNP) | 0.1.9 | Coordenador rastreável de entrega de PCB para o OpenPnP e para o carregamento ou descarregamento assistido por robô. |
| [HYDRA-UMC-BRIDGE-PRINTER3D](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-PRINTER3D) | 0.1.8 | Ponte segura em torno do software nativo de impressoras 3D; o primeiro adaptador valida a disponibilidade do Moonraker sem substituir o firmware. |
| [HYDRA-UMC-BRIDGE-CNC](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-CNC) | 0.1.9 | Coordenador auxiliar da célula CNC; a trajetória do controlador e a segurança da máquina continuam a ser nativas. |
| [HYDRA-UMC-BRIDGE-LASER](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-LASER) | 0.1.7 | Coordenador auxiliar da célula laser que não pode armar, disparar nem anular os intertravamentos do laser. |
| [HYDRA-UMC-BRIDGE-DROIDS](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-DROIDS) | 0.1.2 | Fronteira de coordenação para droides com pernas/humanoides: vocabulário de ações nomeadas de andar/pegar/pousar controlado pelo contrato de segurança partilhado; a marcha e o equilíbrio permanecem no controlador do próprio droide. |
| [HYDRA-UMC-BRIDGE-AMR](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-AMR) | 0.1.3 | Fronteira de coordenação para frotas de AGV/AMR: transformação de coordenadas da fábrica para as locais mais um vocabulário de ordens inspirado no VDA-5050; o planeamento de trajetórias continua na navegação própria do AMR. |
| [HYDRA-UMC-BRIDGE-UAV](https://github.com/JuanenRac/HYDRA-UMC-BRIDGE-UAV) | 0.1.4 | Fronteira de coordenação para UAV equipados com câmara: vocabulário de pedidos de voo nomeados mais um watchdog determinista de failsafe por heartbeat/perda de ligação. |

### 🛠️ Ferramentas complementares
| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [HYDRA-UMC-WATCH](https://github.com/JuanenRac/HYDRA-UMC-WATCH) | 0.2.5 | Painel de emergência para dispositivos vestíveis com alertas de segurança hápticos. |
| [HYDRA-UMC-TOOL-CLI](https://github.com/JuanenRac/HYDRA-UMC-TOOL-CLI) | 0.1.6 | Interface de linha de comandos para a automatização de frotas, o flash e o devops. |
| [HYDRA-UMC-DASHBOARD-AI](https://github.com/JuanenRac/HYDRA-UMC-DASHBOARD-AI) | 0.1.6 | Extensão de IA para painéis web que fornece informações em linguagem natural. |
| [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER) | 0.4.8 | Ferramenta multiplataforma GUI/CLI para detetar, instalar e atualizar manualmente todos os projetos do ecossistema. |
| [HYDRA-UMC-OS-REBUILDER](https://github.com/JuanenRac/HYDRA-UMC-OS-REBUILDER) | 0.3.1 | Ferramenta de ambiente de trabalho para Windows/Linux que constrói uma imagem de CM5 pronta a gravar, pré-carregada com as versões mais recentes do ecossistema e com configuração de primeiro arranque ao estilo do Raspberry Pi Imager. |
| [HYDRA-UMC-OPS-AGENT](https://github.com/JuanenRac/HYDRA-UMC-OPS-AGENT) | 0.1.8 | Coordenador de incidentes de manutenção: um papel de borda com poucos privilégios recolhe um instantâneo sanitizado de inventário/estado, um papel de plano de controlo mostra-o apenas para leitura e pede a um fornecedor de IA que sugira um diagnóstico - nunca aplica um patch nem implanta nada. |
| [HYDRA-UMC-DEV-SERVER](https://github.com/JuanenRac/HYDRA-UMC-DEV-SERVER) | 0.1.8 | Anfitrião de desenvolvimento reproduzível: hoje um esquema de configuração sujeito a políticas e um inventário de manifestos, a evoluir para um executor isolado de tarefas/espaços de trabalho coordenado com o OPS-AGENT - nenhuma tarefa tem permissão de implantação a menos que um documento a conceda explicitamente. |
| [HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS) | 0.0.3 | Arquitetura, interfaces, base de segurança, matriz de capacidades e catálogo de projetos gerado do ecossistema, mais as ferramentas que comparam todos os repositórios. |

---

# 🔧 URTC

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/JuanenRac/main/URTC_BANNER.svg" alt="Banner do ecossistema URTC" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-STM32-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Bus-CAN%20%2F%20CAN--OTA-orange.svg" alt="Bus">
  <img src="https://img.shields.io/badge/Tools-25%2B%20profiles-blueviolet.svg" alt="Tools">
</p>

O **URTC (Universal Robot Tool Controller)** é um produto próprio, e não uma pasta de subsistema do HYDRA-UMC: firmware em tempo real e uma família de ferramentas de ambiente de trabalho/web para o efetuador final de um robô, desenvolvidos, versionados e mantidos de forma independente. Um trocador de ferramentas equipado com URTC coordena-se com o controlador de célula do HYDRA-UMC através de FDCAN, mas o comportamento em tempo real da própria ferramenta, o seu watchdog e o seu estado seguro são autoridade do próprio URTC - o controlador de célula não o pode contornar, e o URTC não depende do HYDRA-UMC para ser desenvolvido, gravado ou diagnosticado.

## 🏗️ Como funciona o URTC

1. **Firmware da ferramenta**: o firmware STM32 próprio do URTC executa cada um de mais de 25 perfis de ferramentas especializadas (pinças, doseadores, sondas, fusos e mais), cada um com os seus tempos, limites e comportamento perante falhas.
2. **Atualização em campo**: o CAN-OTA envia uma nova imagem de firmware pelo mesmo barramento CAN que a ferramenta já usa, com um caminho SWD/JTAG de chip completo (URTC-FLASHER) como alternativa que nunca depende de o firmware da própria ferramenta estar ativo.
3. **Diagnóstico em direto**: o URTC-TESTER valida o comportamento CAN em tempo real de uma ferramenta contra o seu perfil declarado, sem precisar de uma bancada de oficina completa; o URTC-WEB-STUDIO faz o mesmo a partir de um separador do navegador através de Web Serial, sem nada para instalar.
4. **Armazenamento e ciclo de vida**: o URTC-SMART-RACK guarda as ferramentas entre trabalhos, pré-aquece uma antes da entrega e mantém um registo de auditoria do ciclo de vida (ciclos, falhas, última calibração) por ferramenta física, e não por tipo de ferramenta.
5. **Controlo de qualidade ativo**: o URTC-VISION-TOOL é, ele próprio, uma ferramenta - um cabeçote com câmaras térmica e RGB próprias para a inspeção de qualidade durante o processo, e não uma câmara externa acoplada a outra ferramenta.
6. **Base comum**: o **URTC-COMMON** guarda o protocolo CAN da cabeça de ferramenta como dados, com código gerado e vetores de conformidade; o **URTC-DOCS** guarda a arquitetura, a base de segurança e a matriz de capacidades.

## 🛠️ Stack tecnológica

- **Firmware**: STM32, FDCAN (barramento partilhado com o controlador de célula), CAN-OTA, alternativa SWD/JTAG.
- **Ferramentas de ambiente de trabalho**: clientes GUI multiplataforma para flash e diagnóstico (URTC-FLASHER, URTC-TESTER).
- **Ferramentas de navegador**: a API Web Serial para testes de hardware sem instalação (URTC-WEB-STUDIO).
- **Dados do ciclo de vida**: registo de auditoria não volátil por ferramenta, partilhado com a abordagem de integridade por F-RAM do próprio HYDRA-UMC.

## 🔒 Segurança

Cada perfil de ferramenta tem o seu próprio watchdog e comportamento perante falhas, independentes da camada de E-STOP do controlador de célula - uma ferramenta que perca o seu orçamento de tempo ou o heartbeat CAN passa por si própria ao estado seguro declarado, em vez de esperar por um comando externo. O pré-aquecimento do URTC-SMART-RACK está limitado pelos mesmos limites térmicos por ferramenta que o seu perfil declara, auditado no mesmo registo de ciclo de vida que uma oficina usa para decidir se uma ferramenta ainda está apta para o serviço.

## 📁 Catálogo de projetos URTC

| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.6 | Firmware do Universal Robot Tool Controller para mais de 25 ferramentas especializadas. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.3.2 | Ferramenta GUI para atualizações de firmware por CAN-OTA e SWD/JTAG de chip completo. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.3.1 | Ferramenta de diagnóstico para a validação em tempo real dos perfis de ferramentas URTC através de CAN. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.3.1 | Ferramenta Web Serial no navegador para testes e análises instantâneos de hardware. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.6 | Armazenamento inteligente de ferramentas com pré-aquecimento automático e auditoria do ciclo de vida. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.1.0 | Cabeçote com câmaras térmica e RGB integradas para controlo de qualidade ativo. |
| [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) | 0.1.4 | Deteta, instala e atualiza num computador os repositórios do URTC a partir dos seus próprios manifestos. |
| [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) | 0.0.5 | Arquitetura, interfaces, base de segurança, matriz de capacidades, nota de estudo do protocolo CAN e catálogo de projetos gerado do ecossistema URTC, mais as ferramentas que comparam todos os repositórios. |
| [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) | 0.0.3 | O protocolo CAN da cabeça de ferramenta como dados: uma especificação, código C, TypeScript e Python gerado, vetores de conformidade e os transportes Python. |

---

# 🛡️ A.R.M.O.R.

<p align="center">
  <img src="https://raw.githubusercontent.com/JuanenRac/ARMOR-DOCS/main/images/ARMOR_BANNER.svg" alt="Banner do ecossistema A.R.M.O.R." width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Visibility-Public-brightgreen.svg" alt="Public repositories">
  <img src="https://img.shields.io/badge/Platform-ESP32--S3%20%7C%20Jetson-red.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Stack-TypeScript%20%7C%20Kotlin%20%7C%20C%2B%2B-blueviolet.svg" alt="Stack">
</p>

O **A.R.M.O.R. (Autonomous Radar & Multimodal Observation Range)** é um ecossistema separado e público de segurança perimetral e domótica - sem relação com o HYDRA-UMC nem com o URTC para além do mesmo autor e das mesmas convenções de engenharia (manifestos versionados, um contrato de mensagens partilhado, interfaces em oito idiomas). Os seus nós de campo vigiam o perímetro de uma propriedade e a sua instalação solar/elétrica; o seu servidor central e os seus clientes permitem a um operador ver e agir sobre o que estes comunicam. As notas de versão e de maturidade abaixo vêm diretamente do manifesto e da matriz de capacidades de cada repositório, a mesma convenção de honestidade que o painel do HYDRA-UMC já utiliza.

## 🏗️ Como o A.R.M.O.R. é construído

1. **Contrato partilhado**: o **ARMOR-COMMON** é dono do significado das mensagens - JSON Schema, um validador em Python e tipos TypeScript/Kotlin gerados que todos os outros repositórios consomem e nunca redefinem.
2. **Nós de campo**: firmware ESP32-S3 para a deteção de radar/presença (**ARMOR-RADAR**), a monitorização de inversores e baterias solares (**ARMOR-SOLAR**), a medição elétrica com comutação (**ARMOR-ELECTRICAL**) e o painel de alarme da casa (**ARMOR-ALARM**); um agente em Python (**ARMOR-NETWORK**) vigia a rede local da casa e a acessibilidade à internet a partir de uma máquina que já esteja nela.
3. **Coordenador central**: o **ARMOR-SERVER** guarda o estado, os utilizadores, os alarmes, as automatizações e as provas das câmaras; o **ARMOR-SERVER-AI** e o **ARMOR-VOICE-AI** acrescentam uma política visual explicável e intenções de voz offline que nunca acionam nada por si próprias.
4. **Clientes do operador**: o **ARMOR-STUDIO** (web) e o **ARMOR-ANDROID-CONTROL** (móvel) são clientes do servidor central, nunca da rede de campo diretamente. O **ARMOR-HMI** é um painel tátil na parede (um Waveshare ESP32-S3-Touch-LCD-7C-BOX) que mostra o estado, arma e reconhece, e será onde viverá o assistente de voz.
5. **Implantação e testes**: o **ARMOR-DEVOPS** implanta todo o grafo de serviços; o **ARMOR-SIMULATOR** reproduz cenários e falhas repetíveis sem hardware real; o **ARMOR-HARDWARE** contém o desenho da caixa e a sua matriz de aceitação em bancada.
6. **Operações do ecossistema**: o **ARMOR-UPDATER** descobre, instala e atualiza num computador todos os repositórios do A.R.M.O.R., com o mesmo desenho atómico por verificação do HYDRA-UMC-UPDATER; o **ARMOR-DOCS** é a documentação canónica de arquitetura e a matriz de capacidades. O **ARMOR-STUDIO** também pode atualizar os serviços da máquina central a partir de pacotes assinados com a chave de lançamento do ecossistema, verificando cada assinatura antes de instalar.

## 🔒 Honestidade e segurança

O A.R.M.O.R. segue a mesma regra que o painel do próprio HYDRA-UMC já aplica: uma afirmação só é real quando está verificada, e cada repositório diz com clareza o que já foi e o que ainda não foi executado em hardware real. Nada neste ecossistema controla atualmente a eletricidade da rede nem o acesso físico; os nós de campo observam e comunicam, e qualquer futura capacidade de comutação é projetada e revista antes de ser ativada.

## 📁 Catálogo de projetos A.R.M.O.R.

| Repositório | Versão | Descrição |
| :--- | :--- | :--- |
| [ARMOR-COMMON](https://github.com/JuanenRac/ARMOR-COMMON) | 0.6.7 | Contratos de mensagens, validadores, vetores de conformidade, tipos gerados, OpenAPI, lançador partilhado. |
| [ARMOR-RADAR](https://github.com/JuanenRac/ARMOR-RADAR) | 0.7.3 | Firmware do nó de campo ESP32-S3, descodificadores para o LD2450, o LD2461 e sensores de presença, o seu núcleo testado no anfitrião, atualiza-se a partir do GitHub com barra de progresso e mapa em direto. |
| [ARMOR-SOLAR](https://github.com/JuanenRac/ARMOR-SOLAR) | 0.4.9 | Nó gateway solar: o firmware ESP32-S3 e o seu painel (dez portas série), e os protocolos dos inversores Voltronic / MPP Solar e das baterias Pylontech e ANT-BMS. |
| [ARMOR-ELECTRICAL](https://github.com/JuanenRac/ARMOR-ELECTRICAL) | 0.4.1 | Nó elétrico: o firmware (dezasseis medidores PZEM numa só linha série, painel web, MQTT), as tramas dos medidores, a mensagem das leituras da rede e as regras de comutação. |
| [ARMOR-ALARM](https://github.com/JuanenRac/ARMOR-ALARM) | 0.3.9 | Nó e painel de alarme: o seu firmware (zonas cabladas, a sirene, sensores e sirenes Zigbee, um painel web em sete idiomas) e as regras de armar, atrasos, alarme e PIN, testadas num computador; continua a vigiar, e assume o rádio Zigbee, quando o servidor está ausente. Nunca foi executado numa placa. |
| [ARMOR-HMI](https://github.com/JuanenRac/ARMOR-HMI) | 0.3.2 | Painel tátil para o Waveshare ESP32-S3-Touch-LCD-7C-BOX: o estado do sistema num ecrã de parede, armar/desarmar/reconhecer, voz push-to-talk e a página web de um nó; o firmware nunca foi executado numa placa. |
| [ARMOR-NETWORK](https://github.com/JuanenRac/ARMOR-NETWORK) | 0.1.3 | Monitor de rede local: os dispositivos da rede da casa, o estado da internet (e de que lado está uma falha), o que muda; apenas observa. |
| [ARMOR-SERVER](https://github.com/JuanenRac/ARMOR-SERVER) | 0.7.7 | Estado central (persistido), utilizadores, histórico de eventos, alarmes, dispositivos, automatizações, leituras solares e elétricas, a rede local, serviços do sistema, watchdog de câmaras, câmaras, provas, auditoria, atualizações de firmware dos nós que têm de ser assinadas, avisos por Telegram e Home Assistant, comandos de voz e utilização a partir do exterior da casa (segundo fator, sessões que podem ser terminadas, uma política remota). |
| [ARMOR-SERVER-AI](https://github.com/JuanenRac/ARMOR-SERVER-AI) | 0.2.6 | Serviço de vigilância de movimento, seleção de perfil visual, política de fusão explicável, registo de motores. |
| [ARMOR-VISION](https://github.com/JuanenRac/ARMOR-VISION) | 0.0.2 | Zonas de câmara, máscaras e regras de deteção (permanência prolongada, um evento por visita); ainda sem modelo detetor. |
| [ARMOR-VOICE-AI](https://github.com/JuanenRac/ARMOR-VOICE-AI) | 0.3.0 | Serviço de voz offline: quinze comandos em oito idiomas, os turnos falados do painel de parede, armar e desarmar confirmados com um token assinado. |
| [ARMOR-STUDIO](https://github.com/JuanenRac/ARMOR-STUDIO) | 0.8.0.3 | Consola de operações, alarmes, dispositivos, automatizações, utilizadores, histórico, regras de alerta, PTZ, mapa do radar, menus solar e elétrico, a rede local, serviços do sistema, meteorologia, um localizador de nós e configuração, atualizações de firmware dos nós, notificações e um desenhador de locais 2D/3D. |
| [ARMOR-ANDROID-CONTROL](https://github.com/JuanenRac/ARMOR-ANDROID-CONTROL) | 0.6.9 | Cliente de operador Android: armar e desarmar, alarmes, dispositivos, radar em direto, inversores e baterias solares, histórico, notificações de alarme, um assistente para comandos escritos e falados e o configurador dos nós. |
| [ARMOR-HARDWARE](https://github.com/JuanenRac/ARMOR-HARDWARE) | 0.2.4 | Desenhos de caixas (a caixa de canto do radar; uma caixa verificada para os nós solar, elétrico e de alarme) e a matriz de aceitação em bancada. |
| [ARMOR-DEVOPS](https://github.com/JuanenRac/ARMOR-DEVOPS) | 0.6.3 | Topologia Compose, instalador de bancada de testes do servidor central, cópia de segurança e restauro, perfil TLS, broker MQTT próprio, serviços de observação e voz, agente de administração. |
| [ARMOR-SIMULATOR](https://github.com/JuanenRac/ARMOR-SIMULATOR) | 0.2.5 | Cenários e falhas repetíveis. |
| [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER) | 0.1.4 | Deteta, instala e atualiza os repositórios do próprio ecossistema (atómico por verificação, sem necessidade de GITHUB_TOKEN). |
| [ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS) | 0.8.0.4 | Documentação canónica e matriz de capacidades. |

---

## 🤝 Contribuir
Cada ecossistema é uma iniciativa própria, com os seus projetos. Cada projeto tem as suas próprias diretrizes de contribuição. Consulte os repositórios individuais para obter os detalhes técnicos.

As etiquetas das issues estão normalizadas em todos os repositórios HYDRA-UMC a partir de [`.github/labels.yml`](.github/labels.yml) neste mesmo repositório, e são distribuídas por [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) - edite esse único ficheiro para alterar uma etiqueta em todo o lado de uma só vez, em vez de o fazer à mão em cada repositório. Ao contrário do painel abaixo, esta lista é estática (uma matriz real do GitHub Actions, e não uma descoberta dinâmica) - um repositório recém-adicionado também precisa de uma entrada ali, e não apenas de um `hydra-umc.project.json` real.

Um painel de estado em direto que abrange todos os repositórios públicos dos três ecossistemas - cada um descoberto pelo seu próprio manifesto (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, mais `electro-hobby-3d.project.json` para os repositórios transversais aos ecossistemas), lido diretamente do ramo predefinido de cada repositório, sem lista fixa - é regenerado por [`.github/workflows/build-dashboard.yml`](.github/workflows/build-dashboard.yml) imediatamente quando um projeto faz push (o `dashboard-dispatch.yml` de cada repositório) e, como rede de segurança, duas vezes por hora, e é servido a partir de `docs/` através do GitHub Pages: **[juanenrac.github.io/JuanenRac](https://juanenrac.github.io/JuanenRac/)**. Mostra a stack, o destino de implantação e a versão atual, uma classificação real de maturidade por projeto (scaffolding / functional / established / production, cada uma decidida a partir do CHANGELOG do próprio projeto - veja [`HYDRA-UMC-UPDATER/registry.py`](https://github.com/JuanenRac/HYDRA-UMC-UPDATER/blob/main/src/hydra_umc_updater/registry.py)), o seu papel (API / UI / CLI / firmware / biblioteca / serviço / ferramenta), uma árvore de família/pai-filho e notas por projeto sobre o que está implementado hoje. O [`ecosystem-catalog.json`](ecosystem-catalog.json) lista esses ecossistemas e os seus manifestos num único sítio, e a construção do painel recusa-se a correr se os dois alguma vez discordarem.

## 🧭 Colaboração no GitHub

O [modelo de colaboração no GitHub](docs/GITHUB_COLLABORATION.md) define uma Wiki central, um Project do ecossistema, o âmbito das Discussions, os critérios de lançamento e o limite de automatização partilhado. Os [formulários de issues](.github/ISSUE_TEMPLATE/) e o [modelo de pull request](.github/PULL_REQUEST_TEMPLATE.md), mantidos centralmente, tornam rastreável o trabalho de software, de validação de hardware e de documentação sem duplicar os manuais dos projetos.

O workflow de saúde da comunidade é intencionalmente manual e funciona em modo de simulação por predefinição. Quando o `COMMUNITY_HEALTH_SYNC_TOKEN` estiver configurado, poderá copiar apenas estes modelos geridos para todos os repositórios que publiquem um manifesto HYDRA-UMC; nunca elimina um modelo específico de um projeto.
**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)** - Licença GPL-3.0.
