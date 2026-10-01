# =============================================================================
# HYDRA-UMC / URTC / A.R.M.O.R. Ecosystem - Roadmap definitions
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""What differs between the three Roadmap Projects: the title, the text, the families and the work items.

HYDRA-UMC keeps its definitions where they always were (bootstrap_ecosystem_project.py and seed_ecosystem_roadmap.py). URTC and A.R.M.O.R. each have their own board, with the
same fields and views as that one (so a person who knows one knows all three) but their own families, hardware dependencies and a human-curated list of planning items. As in
the HYDRA-UMC board, an item is a record of a scoped, evidence-based next step; it is never a claim that something physical was validated.
"""

from __future__ import annotations

from typing import Any


def _item(title: str, repository: str, family: str, maturity: str, evidence: str, priority: str, objective: str, acceptance: str,
          status: str = "Backlog", hardware: str = "None", blocked_by: str = "None") -> dict[str, str]:
    return {"title": title, "repository": repository, "family": family, "maturity": maturity, "evidence": evidence, "priority": priority,
            "objective": objective, "acceptance": acceptance, "status": status, "hardware": hardware, "blocked_by": blocked_by}


# ---- URTC -----------------------------------------------------------------------------------------------------------------------------------

URTC_FAMILIES = [("Firmware", "BLUE"), ("Tool Platform", "GREEN"), ("Smart Rack & Vision", "ORANGE"), ("Ecosystem Operations", "GRAY")]
URTC_HARDWARE = [("None", "GREEN"), ("STM32 / PCB", "ORANGE"), ("CAN bus", "YELLOW"), ("Thermal + RGB sensors", "PURPLE"), ("Soldering tools", "RED"), ("HYDRA-UMC machine", "PINK")]
URTC_EVIDENCE = [("Documentation", "GRAY"), ("Local test", "BLUE"), ("Host harness", "PURPLE"), ("Browser", "YELLOW"), ("MCU", "ORANGE"), ("Real tool", "RED")]

URTC_ITEMS = (
    _item("Validate the web studio against a real SLCAN adapter", "URTC-WEB-STUDIO", "Tool Platform", "Established", "Browser", "High",
          "Run the serial-CAN session (connect, frames, pacing, disconnect) against a physical adapter and a live bus, not only the parser tests.",
          "A recorded session with a real adapter; the slave-data pacing is measured and either confirmed or corrected; the findings are in the documentation.",
          status="Blocked", hardware="CAN bus", blocked_by="Needs a real SLCAN adapter on a live CAN bus"),
    _item("Test the serial transport of the web studio without hardware", "URTC-WEB-STUDIO", "Tool Platform", "Established", "Local test", "Normal",
          "Cover connect, send, wait and disconnect of the serial CAN transport with a scripted fake port.",
          "Tests prove ordering, timeouts and a clean disconnect; no browser or adapter is needed."),
    _item("Replace the stand-in screenshots with real ones", "URTC-FLASHER + URTC-TESTER", "Tool Platform", "Established", "Documentation", "Low",
          "The README images of the Flasher and the Tester should be real captures of the running applications.",
          "Both READMEs show a current capture taken from the real window; the seven translations point at the same images."),
    _item("Build the Smart Rack on its real board", "URTC-SMART-RACK", "Smart Rack & Vision", "Established", "Real tool", "Normal",
          "Tool tracking (5-bit ID or F-RAM), pre-heating logic for the T12 and hot-air tools, and lifecycle logs in F-RAM all wait for the real PCB.",
          "Each of the three is implemented against the real chip and exercised with a real tool; the protocol tests stay green.",
          status="Blocked", hardware="Soldering tools", blocked_by="Needs the designed PCB with F-RAM and a real T12 / hot-air tool"),
    _item("Real thermal and RGB capture for the vision tool", "URTC-VISION-TOOL", "Smart Rack & Vision", "Established", "Real tool", "Normal",
          "Replace the simulated MLX9064x and camera frames with real captures and time-align the thermal and the RGB frames.",
          "A capture session with real sensors; the alignment error is measured and documented.",
          status="Blocked", hardware="Thermal + RGB sensors", blocked_by="Needs the MLX9064x sensor and an RGB camera on the board"),
    _item("CAN integration of the vision tool with the STM32 firmware", "URTC-VISION-TOOL + URTC", "Smart Rack & Vision", "Functional", "MCU", "Normal",
          "Carry the vision tool's frames and settings over the same CAN protocol the other tools use.",
          "The protocol is specified, the host harness covers it, and a real board answers it.",
          hardware="STM32 / PCB", blocked_by="Needs an STM32 board running the firmware"),
    _item("Pick-and-place tool changes over CAN with the HYDRA-UMC motion brain", "URTC-SMART-RACK + HYDRA-UMC", "Smart Rack & Vision", "Functional", "Local test", "Low",
          "Specify how the automatic tool changer asks the rack for a tool and how the rack answers.",
          "A versioned message specification with conformance vectors both sides run in tests, before any machine is involved.", hardware="HYDRA-UMC machine"),
    _item("Shrink the firmware binary", "URTC", "Firmware", "Functional", "Local test", "Low",
          "Measure what takes the flash and remove what is not needed, without changing behaviour.",
          "A size report per module before and after; the host harness and the CAN readback tests pass unchanged."),
    _item("Generate a signed release manifest with the CRC of every artifact", "URTC-SMART-RACK + URTC-FLASHER + URTC-UPDATER", "Ecosystem Operations", "Functional", "Local test", "Normal",
          "One script produces the manifest the Flasher and the Updater check, from the built files.",
          "The manifest is reproducible from a clean build; the Flasher refuses a file whose digest is not in it."),
    _item("Automatic version bump step for the vision tool build", "URTC-VISION-TOOL", "Smart Rack & Vision", "Established", "Local test", "Low",
          "The build should take the version from the manifest instead of a constant edited by hand.",
          "One place holds the version; the build, the about box and the manifest all read it."),
    _item("Host-native harness for the whole CAN dispatch table", "URTC", "Firmware", "Functional", "Host harness", "Normal",
          "Run every handler of the general CAN dispatch table against recorded frames on the PC.",
          "A handler without a recorded case fails the build; the readback tests keep their black-box form.", status="In progress"),
)

# ---- A.R.M.O.R. -----------------------------------------------------------------------------------------------------------------------------

ARMOR_FAMILIES = [("Core: Server, Common, Studio", "BLUE"), ("Field Nodes", "GREEN"), ("Apps & Panels", "PINK"), ("AI & Voice", "PURPLE"), ("Operations & Docs", "GRAY")]
ARMOR_HARDWARE = [("None", "GREEN"), ("CM5", "YELLOW"), ("ESP32-S3", "ORANGE"), ("Jetson Orin NX", "PURPLE"), ("Solar equipment", "RED"), ("Phone / panel", "PINK")]
ARMOR_EVIDENCE = [("Documentation", "GRAY"), ("Local test", "BLUE"), ("Simulator", "PURPLE"), ("CM5", "YELLOW"), ("ESP32 board", "ORANGE"), ("Real equipment", "RED")]

ARMOR_ITEMS = (
    # ---- shipped (so the board shows what moved) ----
    _item("Sessions that last and a design that cannot be lost", "ARMOR-SERVER + ARMOR-STUDIO", "Core: Server, Common, Studio", "Established", "CM5", "High",
          "Sliding sessions, cookies that cannot shadow each other, and versions of the site, electrical and network designs.",
          "An administrator stays one; a design saved by mistake as empty can be recovered from its versions.", status="Done", hardware="CM5"),
    _item("Alarms that say what happened", "ARMOR-SERVER + ARMOR-STUDIO", "Core: Server, Common, Studio", "Established", "CM5", "High",
          "Facts in each alarm (device, address, MAC, port), deletion one by one, a record that can be emptied for good, and a degraded-line warning that waits.",
          "Each alarm names the machines and ports involved; disarming settles the intrusion alarms.", status="Done", hardware="CM5"),
    _item("Orders for the network node", "ARMOR-NETWORK + ARMOR-SERVER + ARMOR-STUDIO", "Field Nodes", "Established", "CM5", "High",
          "Sweep now, ping, traceroute, wake-up, port and web-page looks, hide a device and be told when it returns.",
          "Orders travel in the node's own answers (the node never listens) and are bounded and audited.", status="Done", hardware="CM5"),
    _item("The machine, live", "ARMOR-SERVER + ARMOR-STUDIO", "Core: Server, Common, Studio", "Established", "CM5", "Normal",
          "Processor, memory, temperatures, disks and network cards with charts, like a task manager.",
          "The System menu shows them from the real machine, sampled every two seconds.", status="Done", hardware="CM5"),
    _item("Reboot loop of the radar node on the Ethernet board", "ARMOR-RADAR + ARMOR-COMMON", "Field Nodes", "Established", "ESP32 board", "Critical",
          "The main task overflowed its stack while generating the TLS certificate.",
          "The board boots, serves its web page and joins the server; the fix is in the shared firmware base.", status="Done", hardware="ESP32-S3"),
    # ---- in progress ----
    _item("ARMOR-HMI: a touch panel that talks to the server", "ARMOR-HMI", "Apps & Panels", "Scaffolding", "Documentation", "High",
          "A 7-inch ESP32-S3 touch panel with microphone and speakers: a node with its own configuration page that behaves toward the server like another client (Android, Studio).",
          "Documented like the other projects, a firmware that boots and shows the status, its web page for settings, and a registration against ARMOR-SERVER.",
          status="In progress", hardware="ESP32-S3"),
    _item("Network node: inspect a device with its own login", "ARMOR-NETWORK + ARMOR-SERVER + ARMOR-STUDIO", "Field Nodes", "Functional", "Local test", "High",
          "A device can be given an administrator login (kept in the server's vault) so the node reads its parameters and suggests settings.",
          "Credentials never travel in the clear nor reach a log; the node reads a router and a camera in a lab network and Studio shows what it found.", status="In progress"),
    _item("Site Designer: garage door, pools, planters, masts, solar on roofs", "ARMOR-STUDIO", "Core: Server, Common, Studio", "Established", "Local test", "Normal",
          "Garage doors, arched wall openings, removable roofs, panels on roofs or on the ground with tilt, terraces and balconies, pools of any shape, planters, masts with antennas and dishes.",
          "Each object can be placed, edited, saved and recovered from the versions of the design.", status="In progress"),
    # ---- next ----
    _item("Rollback of a bad firmware update on every node", "ARMOR-COMMON (firmware base)", "Field Nodes", "Functional", "ESP32 board", "High",
          "Mark a new image valid only after it has reached the server; otherwise the bootloader returns to the previous one.",
          "A deliberately broken image is replaced by the previous one by itself on a real board; a good one is kept.", hardware="ESP32-S3"),
    _item("Health telemetry in every node", "ARMOR-COMMON (firmware base) + ARMOR-SERVER + ARMOR-STUDIO", "Field Nodes", "Functional", "ESP32 board", "High",
          "Reason of the last reset, free memory, lowest free memory and the stack margin of each task, sent with the node's messages and shown in Studio.",
          "A stack that is about to overflow shows as a warning before the node resets.", hardware="ESP32-S3"),
    _item("Flash and set the Wi-Fi from a web page", "ARMOR-COMMON + ARMOR-RADAR + ARMOR-SOLAR + ARMOR-ELECTRICAL", "Field Nodes", "Functional", "ESP32 board", "Normal",
          "Support the Improv protocol over serial and Bluetooth so a browser can install the firmware and give the node its Wi-Fi.",
          "A node is installed and joined to a network from a browser alone.", hardware="ESP32-S3"),
    _item("Both ESP32-S3 firmwares (Ethernet and Wi-Fi) rebuilt and checked on the board", "ARMOR-RADAR + ARMOR-SOLAR + ARMOR-ELECTRICAL", "Field Nodes", "Established", "ESP32 board", "High",
          "Rebuild with the stack fix and the quiet missing-sensor log, one build at a time, and flash and read the log of each.",
          "Each image boots, shows the node page and reaches the server; the log has no loop and no wall of bus errors.", hardware="ESP32-S3", status="Ready"),
    _item("Zones and masks drawn over each camera", "ARMOR-SERVER + ARMOR-STUDIO", "Core: Server, Common, Studio", "Functional", "Local test", "Normal",
          "Polygons per camera: where a detection counts and where movement is ignored, with a filter by kind of object.",
          "Zones are saved with the camera, edited in the Cameras menu and used by the alarm rules."),
    _item("Detection on the Jetson: movement first, the model only where it moves", "ARMOR-VISION (new)", "AI & Voice", "Scaffolding", "Documentation", "Normal",
          "Cheap motion detection decides where to look and the detector runs only there, on a low-resolution stream, publishing detections to the server.",
          "A person in a zone raises an alarm with a snapshot; CPU and GPU use are measured per camera.",
          status="Blocked", hardware="Jetson Orin NX", blocked_by="Needs the Jetson Orin NX"),
    _item("Live view with low latency (WebRTC)", "ARMOR-SERVER + ARMOR-STUDIO + ARMOR-ANDROID-CONTROL", "Core: Server, Common, Studio", "Functional", "CM5", "Low",
          "One connection per camera, re-streamed to Studio, the apps and the recorder instead of one per viewer.",
          "Latency is measured against the current MJPEG view on the real cameras.", hardware="CM5"),
    _item("TLS for the LAN and the Internet at once", "ARMOR-SERVER + ARMOR-STUDIO + ARMOR-ANDROID-CONTROL", "Core: Server, Common, Studio", "Established", "CM5", "High",
          "Plain HTTP on the local network (the apps use the IP) and HTTPS with a real certificate for the domain; or pinned certificates in the apps.",
          "The Android apps work on the LAN and from outside, and the browser warns about nothing at the domain.", hardware="CM5"),
    _item("Verify the Android app against a node on a real phone", "ARMOR-ANDROID-CONTROL", "Apps & Panels", "Established", "Real equipment", "Normal",
          "Use the app on a phone with the ESP32-S3 node and the server on the CM5.",
          "Sync with the node is confirmed or the failure is reproduced and fixed.", status="Blocked", hardware="Phone / panel", blocked_by="Needs a phone in front of the node"),
    _item("Switching of the electrical installation", "ARMOR-ELECTRICAL + ARMOR-SERVER", "Field Nodes", "Functional", "Local test", "Low",
          "The contract (arm, token, close; shut-off in firmware, server and access list) exists and is not wired to anything.",
          "Wire it to a bench lamp with a person present, never to the house, and write the safety validation.", status="Blocked", hardware="ESP32-S3", blocked_by="Needs the protections of the installation and a safety review"),
    _item("Solar equipment: writing settings, not only reading", "ARMOR-SOLAR", "Field Nodes", "Functional", "Real equipment", "Low",
          "Reading the configuration of the inverters and batteries works; writing is a decision for later.",
          "A written design of what may be changed, with confirmation and an audit record; nothing is written until it is accepted.", status="Blocked", hardware="Solar equipment", blocked_by="A decision of the owner and the real equipment"),
    _item("Export and import the whole installation", "ARMOR-SERVER + ARMOR-STUDIO", "Core: Server, Common, Studio", "Functional", "Local test", "Low",
          "Cameras, zones, rules, designs and settings (never passwords) in one file that can be restored on another server.",
          "A round trip on two servers gives the same installation."),
    _item("A written threat model", "ARMOR-DOCS", "Operations & Docs", "Functional", "Documentation", "Normal",
          "Server, nodes, apps and the network node that carries out orders: what is trusted, what is exposed and what stops each abuse.",
          "A document in the public documentation reviewed against the code, with the tests that back each claim."),
)

ROADMAPS: dict[str, dict[str, Any]] = {
    "urtc": {
        "title": "URTC Roadmap",
        "description": "Planning board for the URTC tool platform: firmware, the host tools, the Smart Rack and the vision tool.",
        "readme": "# URTC Roadmap\n\nPlanning board for the URTC tool platform.\n\nA repository is not a task.\nA Discussion is a conversation.\nAn Issue is scoped work.\nA Pull Request is the reviewed implementation.\nThis Project shows priority, evidence, maturity and blockers.\n\nPhysical completion must always link to actual validation evidence.\n",
        "families": URTC_FAMILIES, "hardware": URTC_HARDWARE, "evidence": URTC_EVIDENCE, "prefixes": ("URTC",), "items": URTC_ITEMS,
    },
    "armor": {
        "title": "A.R.M.O.R. Roadmap",
        "description": "Planning board for A.R.M.O.R.: the server, Studio, the field nodes, the apps and panels, and the AI.",
        "readme": "# A.R.M.O.R. Roadmap\n\nPlanning board for the A.R.M.O.R. ecosystem.\n\nA repository is not a task.\nA Discussion is a conversation.\nAn Issue is scoped work.\nA Pull Request is the reviewed implementation.\nThis Project shows priority, evidence, maturity and blockers.\n\nPhysical completion must always link to actual validation evidence.\n",
        "families": ARMOR_FAMILIES, "hardware": ARMOR_HARDWARE, "evidence": ARMOR_EVIDENCE, "prefixes": ("ARMOR",), "items": ARMOR_ITEMS,
    },
}
