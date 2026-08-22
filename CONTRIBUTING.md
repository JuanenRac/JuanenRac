# Contributing to the HYDRA-UMC / URTC Ecosystem 🤖🤝

First off, thank you for considering contributing to the HYDRA-UMC ecosystem! It's people like you that help build the future of open-source industrial robotics.

This document provides guidelines for contributing to any of the repositories within this ecosystem.

---

## 🏗️ Ecosystem Philosophy

The HYDRA-UMC ecosystem is built on **modular isolation and tight integration**. 
- **Modularity**: Each component (Firmware, Desktop, Mobile, AI) should be able to run or be tested independently.
- **Safety**: Industrial safety is paramount. Any change affecting motion or thermal control must be rigorously validated.
- **Consistency**: We use unified communication protocols (REMOTE_API.md) across all clients.

## 🚀 How Can I Contribute?

### 1. Reporting Bugs
- Use the **GitHub Issues** tab in the relevant repository.
- Describe the bug precisely: what happened vs. what was expected.
- Include logs (from the App's Telemetry screen, SUITE logs, or `server.log`).
- Specify your hardware (e.g., Raspberry Pi CM5, STM32H7, Android version).

### 2. Suggesting Enhancements
- Open an issue with the tag `enhancement`.
- Explain why this feature would be useful for industrial automation or micro-factories.

### 3. Code Contributions (Pull Requests)
1. **Fork** the repository you want to work on.
2. **Create a branch** with a descriptive name (e.g., `fix/fdcan-jitter` or `feat/voice-command-ui`).
3. **Keep it atomic**: One PR per fix or feature.
4. **Follow the stack**:
   - **Firmware**: Pure C (C11), follow the existing MISRA-adjacent style.
   - **Frontend**: React 19 + TypeScript (strict mode).
   - **Mobile**: Kotlin/Jetpack Compose or Flutter 3.x.
   - **Desktop**: Python 3.12+ with PySide6.
5. **Document your changes**: Update the README or the internal `docs/` folder if you change an API or a pinout.

## 🛠️ Development Setup

Each repository contains a `README.md` with specific build instructions. Generally:
- **MCU Firmware**: Requires `arm-none-eabi-gcc` and the provided `build_firmware.sh/.bat` scripts. No IDE project files required.
- **Web/Server**: Requires Node.js 20+.
- **Python Tools**: Use virtual environments (`venv`) and the `requirements.txt`.

## 🔒 Security & Safety Guidelines
If you are contributing to the **Execution Layer** (Firmware) or **Coordination Layer** (Server):
- **Watchdogs**: Never disable or bypass hardware or software watchdogs.
- **Authentication**: Ensure every new API route is gated by the `authenticate` middleware.
- **Validation**: Sanitize all incoming JSON/CAN data to prevent buffer overflows or logic injection.

## 💬 Communication
For deep technical discussions or architecture proposals, feel free to reach out via:
- **Email**: electrohobby3d@gmail.com
- **YouTube**: [youtube.com/@electrohobby3d](https://youtube.com/@electrohobby3d)

---

**By contributing, you agree that your code will be licensed under the GPL-3.0 License (Firmware/Software) or CERN-OHL-S v2 (Hardware).**

Happy coding! 🚀🦾
