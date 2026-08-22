# Licensing Model: HYDRA-UMC / URTC Ecosystem 📜

The **HYDRA-UMC Ecosystem** is committed to the principles of Open Source Hardware and Software. Due to the diverse nature of the projects (firmware, hardware, desktop/mobile software, and documentation), we employ a **Hybrid Licensing Model** to ensure the best protection and freedom for each component.

Each repository in this organization contains its own `LICENSE` file. In the absence of a specific license file in a new or sub-project, the following defaults apply.

---

## 1. 💻 Software & Firmware (GPL-3.0)
All **source code**, including MCU firmware (C/C++), backends (Node.js/Rust/Go), and frontend applications (React/Kotlin/Flutter/Python), is licensed under the:
**[GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html)**

- **What this means:** You can run, study, share, and modify the software. If you distribute a modified version, you must also make the source code available under the same GPL-3.0 license.

## 2. 🏗️ Hardware Designs (CERN-OHL-S v2)
All **hardware-related files**, including Eagle schematics (.sch), PCB layouts (.brd), Gerbers, and 3D-printable parts (.stl/.step/.scad), are licensed under the:
**[CERN Open Hardware Licence v2 - Strongly Reciprocal (CERN-OHL-S v2)](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2)**

- **What this means:** This is the hardware equivalent of the GPL. You can manufacture the boards and modify the designs. If you distribute a modified version of the hardware, you must provide the source files under this same license.

## 3. 📖 Documentation (CC BY-SA 4.0)
All **documentation**, including README files, technical manuals, architecture diagrams, and service guides, is licensed under the:
**[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)**

- **What this means:** You are free to share and adapt the material for any purpose, even commercially, provided you give appropriate credit and distribute your contributions under the same license.

## 4. 📦 Third-Party Assets
The ecosystem redistributes several third-party assets which maintain their **original licenses**:
- **Robot Meshes:** 3D models from manufacturers (Universal Robots, FANUC, Kinova, etc.) are redistributed under their respective licenses (BSD-3-Clause, Apache-2.0, MIT). Check the `ATTRIBUTION.txt` file within each model folder.
- **Libraries:** Standard libraries and dependencies used in the projects (STM32 HAL, React, Flutter plugins, etc.) remain under the licenses specified by their respective authors.

---

## ⚖️ Summary Table

| Component Type | Applied License |
| :--- | :--- |
| **Firmware (STM32/G4/F3)** | GPL-3.0 |
| **Server/Backend Code** | GPL-3.0 |
| **Mobile & Desktop Apps** | GPL-3.0 |
| **PCB Designs (Eagle/Gerber)** | CERN-OHL-S v2 |
| **3D Printable Parts** | CERN-OHL-S v2 |
| **Guides & READMEs** | CC BY-SA 4.0 |

---

**Copyright (C) 2026 JuanenRac (Electro Hobby 3D)**. 
For licensing inquiries or commercial permissions beyond these terms, please contact: `electrohobby3d@gmail.com`.
