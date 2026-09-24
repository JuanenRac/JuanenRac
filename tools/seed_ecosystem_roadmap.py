#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - Roadmap seed automation
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Add evidence-based, software-only planning items to the central Roadmap.

Items are Project draft issues, not repository issues. They are intentionally
kept as planning records until their scope is accepted and a repository issue
is created. Re-running this script never duplicates a title already present in
the Project.

SEED_ITEMS below is a real, human-curated list, deliberately NOT an
automatic scan of every ecosystem repository - a real project existing does
not by itself mean a specific, scoped, evidence-based planning item is
ready to be written for it (that still takes a human deciding what the
actual next step is). What this script CAN do automatically, and does
every run: report which real public repositories under this account have
NO seed item mentioning them at all yet (see `uncovered_repositories()`
below) - a coverage signal for a human to act on, never a reason for this
script to invent one on its own.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

from bootstrap_ecosystem_project import PROJECT_TITLE, graphql, upsert_field, viewer_projects


SEED_ITEMS = (
    {
        "title": "Define SDK cross-client contract fixture suite",
        "repository": "HYDRA-UMC-SDK",
        "family": "SDK & Server",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Version common discovery, authentication, machine-state, error and compatibility fixtures for all primary SDK consumers.",
        "acceptance": "SDK fixtures are versioned; Server, Studio, Android Control, iOS Control, Suite, Watch and bridges can consume the same fixture without device access.",
    },
    {
        "title": "Validate release manifests before application updates",
        "repository": "HYDRA-UMC-UPDATER + Android Control + Watch + iOS Control + OS",
        "family": "Applications",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Define deterministic validation for update manifests before any download or installation path is accepted.",
        "acceptance": "Tests reject invalid semantic versions, non-HTTPS URLs, missing or mismatched hashes, unexpected signatures, excessive sizes and downgrades.",
    },
    {
        "title": "Prove firmware artifact inventory reproducibility",
        "repository": "HYDRA-UMC",
        "family": "Platform Foundation",
        "maturity": "Established",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Verify that declared sources and toolchain generate the expected firmware artifact inventory and checksums reproducibly.",
        "acceptance": "A non-mutating test compares the expected board, toolchain, artifact names and CRC inventory; public documentation states the supported matrix.",
    },
    {
        "title": "Harden Android update verification tests",
        "repository": "HYDRA-UMC-ANDROID-CONTROL",
        "family": "Applications",
        "maturity": "Established",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Cover the complete update decision path without installing an APK during automated tests.",
        "acceptance": "Tests cover downgrade, invalid hash, unexpected signing certificate and user cancellation; documentation distinguishes download, verification and Android-confirmed installation.",
    },
    {
        "title": "Version the ROS2 interface plan and compatibility fixture",
        "repository": "HYDRA-UMC-BRIDGE-ROS2",
        "family": "External Automation Bridges",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Freeze a versioned software-only plan for ROS2 topics, services, actions and expected QoS semantics.",
        "acceptance": "A JSON fixture and inverse-compatibility test prevent unreviewed topic, service, action or QoS changes before a real ROS2 adapter is introduced.",
    },
    {
        "title": "Fuzz OpenPnP profile parsing without machine I/O",
        "repository": "HYDRA-UMC-BRIDGE-OPENPNP",
        "family": "External Automation Bridges",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Harden machine XML and board-identity parsing against malformed or oversized local input.",
        "acceptance": "Deterministic malformed-input fixtures prove that no recipe or batch data is leaked and no machine I/O is attempted.",
    },
    {
        "title": "Fail-safe GRBL parsing and offline evidence schema",
        "repository": "HYDRA-UMC-BRIDGE-CNC",
        "family": "External Automation Bridges",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Make ambiguous, truncated and noisy GRBL responses fail safe in the CNC bridge.",
        "acceptance": "Fixtures prove that E-STOP and door state are never inferred from ambiguous text; a public JSON schema defines redacted offline evidence.",
    },
    {
        "title": "Add stale-interlock fixtures to the laser bridge",
        "repository": "HYDRA-UMC-BRIDGE-LASER",
        "family": "External Automation Bridges",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "High",
        "objective": "Validate malformed, expired and incomplete safety-state input before any future laser integration.",
        "acceptance": "Fixtures cover key, enclosure and interlock expiry or invalid types; tests document that this bridge cannot arm, fire or alter guards.",
    },
    {
        "title": "Bound Printer3D slicer and Moonraker parsing",
        "repository": "HYDRA-UMC-BRIDGE-PRINTER3D",
        "family": "External Automation Bridges",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Apply explicit size and time limits to slicer artefacts and Moonraker status parsing.",
        "acceptance": "Tests reject corrupt binary input, incomplete /printer/info responses and unknown API versions without executing G-code.",
    },
    {
        "title": "Sanitize untrusted content in Dashboard AI",
        "repository": "HYDRA-UMC-DASHBOARD-AI",
        "family": "Vision & AI",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Ensure untrusted text and metadata cannot alter dashboard rendering or leave the intended trust boundary.",
        "acceptance": "Sanitization tests cover hostile content; public documentation states what data may remain on a LAN and what must never be exported.",
    },
    {
        "title": "Test Datalake ordering, deduplication and retention",
        "repository": "HYDRA-UMC-DATALAKE",
        "family": "SDK & Server",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Exercise event ordering, duplicate delivery and retention policy with synthetic but realistic data volumes.",
        "acceptance": "Versioned event-schema fixtures cover out-of-order and duplicate events without using any production telemetry.",
    },
    {
        "title": "Define Cognitive Node inference budgets and cancellation",
        "repository": "HYDRA-UMC-COGNITIVE-NODE",
        "family": "Vision & AI",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Bound inference time and resource cost and define deterministic behaviour for cancellation, timeout and non-structured model output.",
        "acceptance": "Local tests prove cancellation and timeout paths return a bounded, structured failure without issuing physical commands.",
    },
    {
        "title": "Prove industrial gateway reconnect idempotence",
        "repository": "HYDRA-UMC-GATEWAY-INDUSTRIAL",
        "family": "SDK & Server",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Prevent duplicate command semantics during reconnect, back-pressure and retry handling.",
        "acceptance": "Tests cover duplicate messages, reconnection and queue pressure; the public contract defines idempotency behaviour for retries.",
    },
    {
        "title": "Harden MQTT broker ACL and slow-client behaviour",
        "repository": "HYDRA-UMC-MQTT-BROKER",
        "family": "SDK & Server",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Validate topic ACLs, oversized payload handling and client back-pressure deterministically.",
        "acceptance": "Tests cover denied topics, large payloads and slow consumers; public documentation defines QoS, retention and credential policy.",
    },
    {
        "title": "Expand HIL transport ordering and cancellation tests",
        "repository": "HYDRA-UMC-HIL-BRIDGE",
        "family": "Robotics & Simulation",
        "maturity": "Functional",
        "evidence": "Local test",
        "priority": "Normal",
        "objective": "Strengthen deterministic simulation transport coverage before any hardware-in-the-loop claim.",
        "acceptance": "Tests cover ordering, timeout, cancellation and transport failure; documentation states the evidence required for a real HIL validation.",
    },
)


def _item(
    title: str,
    repository: str,
    family: str,
    maturity: str,
    evidence: str,
    priority: str,
    objective: str,
    acceptance: str,
    status: str = "Backlog",
    hardware: str = "None",
    blocked_by: str = "None",
) -> dict:
    return {
        "title": title,
        "repository": repository,
        "family": family,
        "maturity": maturity,
        "evidence": evidence,
        "priority": priority,
        "objective": objective,
        "acceptance": acceptance,
        "status": status,
        "hardware": hardware,
        "blocked_by": blocked_by,
    }


# Work that has shipped, kept on the board so the Roadmap shows what moved and
# not only what is left. Each one names what is now true, in the repositories
# listed.
DELIVERED_ITEMS = (
    _item(
        "Open machines and robots correctly assembled in Editor STL",
        "HYDRA-UMC-EDITOR-STL",
        "Applications",
        "Scaffolding",
        "Local test",
        "High",
        "Show CNC, laser, pick-and-place and robot models assembled at their home pose instead of as loose parts.",
        "Delivered: assembled view driven by the Suite kinematics, floating icon toolbar, per-part delete, right-button pan; checked against rendered views of the CNC, PnP and arms.",
        status="Done",
    ),
    _item(
        "Reproducible content hashes for image profiles",
        "HYDRA-UMC-OS-REBUILDER",
        "Platform Foundation",
        "Scaffolding",
        "Local test",
        "High",
        "Make two builds of one frozen profile record the same per-project content hash.",
        "Delivered: two real builds compared; only git metadata and bytecode caches differed and are now excluded, so every project hashes identically. Profiles can also pin the shared SDK commit.",
        status="Done",
    ),
    _item(
        "Build bridge projects into an image",
        "HYDRA-UMC-OS-REBUILDER + HYDRA-UMC-BRIDGE-AMR + HYDRA-UMC-BRIDGE-DROIDS",
        "Platform Foundation",
        "Scaffolding",
        "Local test",
        "High",
        "Let projects that depend on the shared SDK build inside the image chroot.",
        "Delivered: the SDK is provided inside the image before each project build; a real chroot build of two bridge projects completed.",
        status="Done",
    ),
    _item(
        "Explicit AMR state table and simulated AMR",
        "HYDRA-UMC-BRIDGE-AMR",
        "External Automation Bridges",
        "Established",
        "Simulator",
        "High",
        "State which order action is legal from which AMR state and rehearse whole jobs without a vehicle.",
        "Delivered: transition table, stop and recovery from every state, and a simulated AMR that imports no transport; covered by tests.",
        status="Done",
    ),
    _item(
        "Platform capability profiles and simulated droid",
        "HYDRA-UMC-BRIDGE-DROIDS",
        "External Automation Bridges",
        "Established",
        "Simulator",
        "High",
        "Refuse action triggers a platform cannot perform and rehearse jobs without real motion.",
        "Delivered: mobile-only and mobile-manipulator profiles, a stop that is never blocked, and a simulated droid with no transport; covered by tests.",
        status="Done",
    ),
    _item(
        "Split the server entry point and publish a route inventory",
        "HYDRA-UMC-SERVER",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Make the server easier to change and describe its routes in a machine-readable file.",
        "Delivered: camera, metrics, ecosystem, Bluetooth and upstream-relay code moved into modules; an OpenAPI document lists every route with its access level, status codes and the field names it reads, and the test run fails when it is stale.",
        status="Done",
    ),
    _item(
        "Record calibration provenance for anomaly verdicts",
        "HYDRA-UMC-ANOMALY-DETECTOR",
        "Vision & AI",
        "Established",
        "Local test",
        "Normal",
        "Make an alarm explainable and reproducible.",
        "Delivered: every verdict reports how many healthy windows the baseline was calibrated from; the numbers are persisted with the baseline.",
        status="Done",
    ),
    _item(
        "Name who ran a zone calibration",
        "HYDRA-UMC-SAFETY-ZONES",
        "Robotics & Simulation",
        "Established",
        "Local test",
        "High",
        "Show who calibrated a zone set when a stale calibration blocks the cell.",
        "Delivered: optional calibrated-by field, validated when present, named in the reason a stale calibration inhibits the cell.",
        status="Done",
    ),
    _item(
        "Keep the seven README translations in step",
        "Every repository (including HYDRA-UMC-DOCS-QA)",
        "Platform Foundation",
        "Established",
        "Local test",
        "Normal",
        "Catch a translation that drifts from the English original.",
        "Delivered: the shared check compares section structure and the set of external links across all seven languages; three bridge repositories that had drifted were brought up to date.",
        status="Done",
    ),
    _item(
        "Keep every repository's CI green",
        "Every repository",
        "Platform Foundation",
        "Established",
        "Local test",
        "High",
        "Find and fix failing workflows across the whole ecosystem.",
        "Delivered: a sweep of every repository's latest workflow runs, the causes fixed at the source, and a scan that reports zero failing workflows.",
        status="Done",
    ),
)

# Software work that is scoped and ready, or already being worked on.
NEXT_ITEMS = (
    _item(
        "Verify Editor STL's move gizmo and part colours on screen",
        "HYDRA-UMC-EDITOR-STL",
        "Applications",
        "Scaffolding",
        "Local test",
        "High",
        "Confirm the gizmo, the assembled view and per-part colours behave as designed in the real window, and make the gizmo move parts along the same axes the Fix button applies.",
        "A recorded walkthrough for one robot, one machine and one variant category; the gizmo axes match the applied transform.",
        status="In progress",
    ),
    _item(
        "Split the remaining server routes into modules",
        "HYDRA-UMC-SERVER",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Move the camera, robot and system routes out of the entry point, one group at a time.",
        "Each group registers through its own module; the whole contract suite passes unchanged after each move.",
        status="Ready",
    ),
    _item(
        "Describe request and response types in the route inventory",
        "HYDRA-UMC-SERVER + HYDRA-UMC-SDK",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Derive body and response schemas from real types instead of only field names.",
        "The generated OpenAPI document carries typed bodies for the write routes and is checked against the SDK fixtures.",
    ),
    _item(
        "Separate telemetry, authorization and arming in the UAV bridge",
        "HYDRA-UMC-BRIDGE-UAV",
        "External Automation Bridges",
        "Established",
        "Simulator",
        "High",
        "Make states that must never be confused impossible to mix up with a real flight order.",
        "A state table and simulated vehicle like the AMR bridge's; tests show an order is refused from every state that does not allow it, and stop is never blocked.",
        status="Ready",
    ),
    _item(
        "Distinguish simulated, blocked and failed-delivery outcomes in the HIL bridge",
        "HYDRA-UMC-HIL-BRIDGE",
        "Robotics & Simulation",
        "Established",
        "Local test",
        "High",
        "Report which of the three happened on every public output and in the operational log.",
        "Three distinct result kinds, each with a test, and documentation of what each one means for a caller.",
    ),
    _item(
        "Prove restart-safe job execution in the dispatcher",
        "HYDRA-UMC-JOB-DISPATCHER",
        "SDK & Server",
        "Established",
        "Local test",
        "High",
        "Show that a job identity, its retries and a cancellation survive a restart without running an unsafe order twice.",
        "A restart test at every stage of a job; no order is executed twice and a cancelled job stays cancelled.",
    ),
    _item(
        "Persist orchestration state and cancellation across restarts",
        "HYDRA-UMC-ORCHESTRATOR",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Keep orchestration state and define what cancellation means after a restart.",
        "Restart tests for running, queued and cancelled work; documented cancellation semantics.",
    ),
    _item(
        "Publish a versioned connector schema and validator",
        "HYDRA-UMC-CONNECTOR-HUB",
        "Platform Foundation",
        "Scaffolding",
        "Local test",
        "High",
        "Describe connectors, pins, power and capabilities in one versioned schema and reject incompatible configurations before they reach a board or design tool.",
        "A schema with a compatibility fixture and a validator that refuses every incompatible combination in the fixture.",
    ),
    _item(
        "Define the incident contract for the local technician",
        "HYDRA-UMC-LOCAL-TECHNICIAN",
        "Vision & AI",
        "Scaffolding",
        "Local test",
        "Normal",
        "Fix the incident format, the minimum evidence, human approval and a diagnosis-only mode.",
        "A schema, a diagnosis-only default, and tests showing nothing is patched or updated without an approved, signed policy.",
    ),
    _item(
        "Split read, propose and execute permissions in the ops agent",
        "HYDRA-UMC-OPS-AGENT",
        "Vision & AI",
        "Scaffolding",
        "Local test",
        "Normal",
        "Limit the API to signed, approved, reversible plans with three separate permissions.",
        "Three permission levels enforced in the API and covered by tests; execution is refused for an unsigned or unapproved plan.",
        status="Blocked",
        blocked_by="Decision: which signing scheme the ecosystem adopts",
    ),
    _item(
        "Choose a shared signing scheme for releases",
        "HYDRA-UMC-UPDATER + HYDRA-UMC-ANDROID-CONTROL + HYDRA-UMC-OS-REBUILDER",
        "Platform Foundation",
        "Established",
        "Documentation",
        "High",
        "Pick one signing scheme (for example minisign or GPG) for release artefacts and image profiles.",
        "A written decision, the key-handling procedure, and a first artefact verified by the updater.",
        status="Blocked",
        blocked_by="Decision: signing scheme and key custody",
    ),
    _item(
        "Define the development API, local authentication and plugin lifecycle",
        "HYDRA-UMC-DEV-SERVER",
        "Platform Foundation",
        "Scaffolding",
        "Local test",
        "Low",
        "Turn the development host into a documented service with local authentication and a plugin lifecycle.",
        "An API description, local-only authentication tests and a plugin install, disable and remove test.",
    ),
    _item(
        "Restrict automatic repairs to reversible steps",
        "HYDRA-UMC-NODE-HEALING",
        "Platform Foundation",
        "Established",
        "Local test",
        "Normal",
        "Record a rollback decision before any repair runs and refuse steps that cannot be undone.",
        "Tests show each automatic step has a recorded rollback and an irreversible step is refused.",
    ),
    _item(
        "State frames, limits and rejection reasons in path planning",
        "HYDRA-UMC-PATH-PLANNER-3D",
        "Robotics & Simulation",
        "Established",
        "Local test",
        "Normal",
        "Make reference frames and kinematic limits explicit and say why a trajectory was rejected.",
        "Every rejection carries a machine-readable reason; frames and limits are part of the request and documented.",
    ),
    _item(
        "Version the physical parameters of the replica",
        "HYDRA-UMC-PHYSICS-REPLICA",
        "Robotics & Simulation",
        "Established",
        "Local test",
        "Low",
        "Present the replica as an estimate until calibration and bench evidence exist.",
        "Parameters carry a version; outputs are labelled as estimates; the calibration procedure is documented.",
    ),
    _item(
        "Add source, interval and version to every production report",
        "HYDRA-UMC-PRODUCTION-REPORTS",
        "SDK & Server",
        "Established",
        "Local test",
        "Low",
        "Make each report traceable to the data it was built from.",
        "Reports and exports include the source, the time window and the source version; covered by tests.",
    ),
    _item(
        "Normalize sample quality and stale state in the MTConnect adapter",
        "HYDRA-UMC-MTCONNECT-ADAPTER",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Give every sample an origin and quality, back off polling and mark stale values.",
        "Fixtures for good, missing and stale data; documented back-off; no value is shown as fresh after its source stops.",
    ),
    _item(
        "Build the per-robot OPC UA tree from live server state",
        "HYDRA-UMC-OPCUA-SERVER",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Replace the fixed placeholder tree with one generated from the server's robot state.",
        "Nodes appear and disappear with the robots; no dangerous write node is published; covered by a client test.",
    ),
    _item(
        "Bind each detection model to a runtime, checksum and accelerator class",
        "HYDRA-UMC-DETECTION-HEF + URTC-VISION-TOOL + HYDRA-UMC-VISION-NODE",
        "Vision & AI",
        "Established",
        "Local test",
        "Normal",
        "Show model, runtime version, checksum and accelerator class together, with a clear message when the device or model is invalid.",
        "One compatibility record per model checked before inference starts; tests for a missing device and a corrupt model.",
    ),
    _item(
        "Separate interpretation, proposal and authorization for language-driven actions",
        "HYDRA-UMC-VLA-ENGINE + HYDRA-UMC-SEMANTIC-PLANNER + HYDRA-UMC-VOICE-UI",
        "Vision & AI",
        "Established",
        "Local test",
        "High",
        "Require approval, cost limits and an explanation before a language-derived plan reaches an executor, with immediate cancellation and a trace per order.",
        "A three-stage flow with tests: nothing executes without an approval record, cancellation is immediate, every order has a trace.",
    ),
    _item(
        "Reject visual-servoing commands built on stale calibration",
        "HYDRA-UMC-VISUAL-SERVOING-API",
        "Vision & AI",
        "Established",
        "Local test",
        "High",
        "Version the coordinate transforms and refuse commands when the camera, target or calibration is out of date.",
        "Versioned transforms; tests refusing a stale calibration, a missing camera and an expired target.",
    ),
    _item(
        "Make telemetry back-pressure and drop policy explicit",
        "HYDRA-UMC-TELEMETRY-COLLECTOR",
        "SDK & Server",
        "Established",
        "Local test",
        "Normal",
        "Bound the buffer and drop lower-priority data first so telemetry can never slow a control path.",
        "A documented buffer limit and priority policy, with a load test showing control-path latency is unaffected.",
    ),
    _item(
        "Expose conflicts and sync age in the swarm sync",
        "HYDRA-UMC-SWARM-SYNC",
        "SDK & Server",
        "Established",
        "Local test",
        "Low",
        "Report conflicts, the winning writer and how old the last sync is as operational evidence.",
        "Conflict and age fields in the public status output, covered by a two-node test.",
    ),
    _item(
        "Make synthetic datasets reproducible and auditable",
        "HYDRA-UMC-SYNTHETIC-DATA-GEN",
        "Vision & AI",
        "Established",
        "Local test",
        "Low",
        "Store seed, configuration and asset provenance with each generated set.",
        "The same seed and configuration regenerate an identical set; the manifest records every asset's source and licence.",
    ),
    _item(
        "Guarantee stable JSON output and a non-interactive mode in the CLI",
        "HYDRA-UMC-TOOL-CLI",
        "Platform Foundation",
        "Established",
        "Local test",
        "Low",
        "Keep machine-readable output stable and never prompt for credentials in a log.",
        "A JSON output contract with a snapshot test and a non-interactive flag that fails instead of prompting.",
    ),
    _item(
        "Make the twin's compose file runnable or clearly a plan",
        "HYDRA-UMC-TWIN",
        "Robotics & Simulation",
        "Established",
        "Local test",
        "Normal",
        "Give every service in the compose file a real image definition, or mark the file as a non-runnable plan.",
        "`docker compose config` passes in CI and each service has a start command, or the file is documented as a plan.",
    ),
    _item(
        "Make the updater transactional",
        "HYDRA-UMC-UPDATER",
        "Applications",
        "Established",
        "Local test",
        "High",
        "Make download, validation, installation and rollback one transaction that leaves evidence of the hash, version before and version applied.",
        "Failure injection at each step leaves the previous version running; an evidence record is written for every attempt.",
    ),
    _item(
        "Show each child's state and version in the Suite launcher",
        "HYDRA-UMC-SUITE",
        "Applications",
        "Established",
        "Local test",
        "Normal",
        "Show state, version, start-up failures and recovery for every child, without treating an active launcher as a healthy service.",
        "A status view driven by each child's own health check; tests for a child that starts and then fails.",
    ),
    _item(
        "Show connection, companion version and server heartbeat before offering a critical action on the watch",
        "HYDRA-UMC-WATCH",
        "Applications",
        "Established",
        "Local test",
        "Normal",
        "Make the watch hide critical actions until the connection, companion version and heartbeat are confirmed.",
        "Tests for a lost connection, an old companion and a missing heartbeat, each hiding the critical action.",
    ),
    _item(
        "Define offline, loading and error states per device in Web Studio",
        "URTC-WEB-STUDIO",
        "URTC",
        "Established",
        "Local test",
        "Normal",
        "Keep configuration changes only after the server confirms them and show a state for every device.",
        "A state model with tests for each state and a change that is rolled back when the server refuses it.",
    ),
    _item(
        "Record adapter, firmware, bus and log artefact for every tester result",
        "URTC-TESTER",
        "URTC",
        "Established",
        "Local test",
        "Normal",
        "Make a PASS reproducible away from the computer that produced it.",
        "Each result stores the adapter, firmware, bus, outcome and log artefact; the record is exportable.",
    ),
    _item(
        "Verify target identity and firmware hash before declaring a flash successful",
        "URTC-FLASHER",
        "URTC",
        "Established",
        "Local test",
        "High",
        "Refuse to report success unless the target identity and firmware hash match.",
        "Tests for a wrong target and a wrong hash; a recovery procedure is documented for an interrupted flash.",
    ),
)

NEXT_ITEMS = NEXT_ITEMS + (
    _item(
        "Keep visual simulation apart from confirmation of real motion in Studio",
        "HYDRA-UMC-STUDIO",
        "Applications",
        "Established",
        "Local test",
        "High",
        "Make it impossible to read a simulated pose as a confirmed machine movement.",
        "Every motion control shows whether the pose is simulated or confirmed by the machine; tests cover both states.",
    ),
    _item(
        "Write a display compatibility matrix for the touch panel",
        "HYDRA-UMC-DSI",
        "Applications",
        "Established",
        "Documentation",
        "Low",
        "Document supported panels, orientation, refresh rate and the start-up sequence as a matrix to be filled in on hardware.",
        "A matrix in the documentation with every cell marked as measured or not yet measured.",
    ),
    _item(
        "Validate limits, axes, basic collisions and mesh paths when saving a URDF",
        "HYDRA-UMC-EDITOR-URDF",
        "Applications",
        "Established",
        "Local test",
        "Normal",
        "Refuse to save a model with impossible limits, unnormalized axes, colliding links or a missing mesh.",
        "A validator with one failing fixture per rule and a save that reports the first failure.",
    ),
    _item(
        "Show delivered, ready, blocked and hardware work on the Roadmap",
        "JuanenRac",
        "Platform Foundation",
        "Established",
        "Documentation",
        "Normal",
        "Make the Roadmap show what has moved and what is waiting, not only a backlog.",
        "Delivered: the seed carries a status, a hardware dependency and a blocker per item, and a re-run never moves a card that was moved by hand.",
        status="Done",
    ),
)

# Work that cannot be finished without hardware, an external tool or a person's
# decision. It stays visible so it is not forgotten and is never marked done on
# software evidence alone.
HARDWARE_ITEMS = (
    _item(
        "Bench-validate FDCAN, SPI and watchdog start-up",
        "HYDRA-UMC + URTC",
        "Platform Foundation",
        "Functional",
        "MCU",
        "High",
        "Turn the provisional clock, FDCAN check, SPI mode and watchdog timing into measured behaviour.",
        "A bench record for each path with the board, firmware version and measured values.",
        hardware="MCU",
    ),
    _item(
        "Validate the Hailo runtime path on the CM5",
        "HYDRA-UMC-DETECTION-HEF + HYDRA-UMC-VISION-NODE + HYDRA-UMC-VISION-STREAMER",
        "Vision & AI",
        "Established",
        "CM5",
        "High",
        "Run the accelerator wrappers against a real Hailo device.",
        "A recorded run with runtime version, model checksum and measured latency.",
        hardware="Vision/Hailo",
    ),
    _item(
        "Bring up the smart rack board and its presence sensors",
        "URTC-SMART-RACK",
        "URTC",
        "Established",
        "MCU",
        "Normal",
        "Replace simulated presence readings with a physical board.",
        "A bench record of the presence lines, tool identity and inventory limits on the first board.",
        hardware="MCU",
    ),
    _item(
        "Validate the legged-robot bridge against a real platform",
        "HYDRA-UMC-BRIDGE-DROIDS",
        "External Automation Bridges",
        "Established",
        "External machine",
        "Normal",
        "Exercise stand, sit, walk and hold against a real robot.",
        "A recorded session showing each action, the stop, and the refusal of an unsupported action.",
        hardware="Robot/actuator",
    ),
    _item(
        "Validate zone geometry and calibration on a physical cell",
        "HYDRA-UMC-SAFETY-ZONES + HYDRA-UMC-VISION-STREAMER",
        "Robotics & Simulation",
        "Established",
        "Safety validation",
        "Critical",
        "Confirm that a calibrated zone actually protects the space it describes.",
        "A safety validation record with the calibration, the measured coverage and an independent reviewer.",
        hardware="Robot/actuator",
    ),
    _item(
        "Rotate the IP camera administrator password",
        "HYDRA-UMC-SERVER + HYDRA-UMC-VISION-STREAMER",
        "Vision & AI",
        "Established",
        "External machine",
        "High",
        "Change the camera password without leaving the cameras unmanaged.",
        "The new password works on all four cameras and is stored only in the server's protected configuration.",
        status="Blocked",
        hardware="External machine",
        blocked_by="Needs the exact management command captured from the cameras' own app",
    ),
    _item(
        "Flash and first-boot a built image on a real CM5",
        "HYDRA-UMC-OS-REBUILDER + HYDRA-UMC-OS",
        "Platform Foundation",
        "Scaffolding",
        "CM5",
        "High",
        "Boot an image built from a frozen profile and check that every installed service starts.",
        "A recorded boot with the profile name, the installed versions and a health report.",
        hardware="CM5",
    ),
    _item(
        "Bench-test the laser interlock chain",
        "HYDRA-UMC-BRIDGE-LASER",
        "External Automation Bridges",
        "Established",
        "Safety validation",
        "Critical",
        "Prove key, door, extraction and alarm behave as the state machine says.",
        "A safety validation record for each interlock with an independent reviewer; nothing is armed by software.",
        hardware="External machine",
    ),
    _item(
        "Build and test the iOS control app",
        "HYDRA-UMC-IOS-CONTROL",
        "Applications",
        "Established",
        "Local test",
        "Normal",
        "Cover the native gaps (Bluetooth, notifications, widget, picture in picture) and confirm distribution.",
        "A build on a Mac, the native features exercised on a device, and the distribution route documented.",
        status="Blocked",
        blocked_by="Needs a Mac with Xcode and an iPhone",
    ),
)

SEED_ITEMS = SEED_ITEMS + DELIVERED_ITEMS + NEXT_ITEMS + HARDWARE_ITEMS



def discover_repository_names(token: str, owner: str) -> list[str]:
    """Every real, public, non-archived, non-fork repository name under
    `owner` - a plain paginated REST call (this script's own account-token
    already has the real access it needs; no separate discovery
    dependency, matching this script's own existing stdlib-only,
    urllib-based GraphQL calls above rather than adding
    hydra-umc-updater as a dependency here too)."""
    names: list[str] = []
    page = 1
    while True:
        request = urllib.request.Request(
            f"https://api.github.com/users/{owner}/repos?type=public&per_page=100&page={page}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2026-03-10",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                batch = json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"GitHub API HTTP {error.code} listing repositories for {owner!r}") from error
        if not batch:
            break
        names.extend(repo["name"] for repo in batch if not repo.get("archived") and not repo.get("fork"))
        if len(batch) < 100:
            break
        page += 1
    return names


def uncovered_repositories(token: str, owner: str) -> list[str]:
    """Real repositories with zero SEED_ITEMS mentioning them anywhere in
    their own `repository` field (a multi-repo item like the SDK contract
    one above lists several names in one string, so this checks
    substring membership, not an exact match) - a coverage report only,
    never a reason to fabricate a seed item for one of these on its own."""
    real_names = discover_repository_names(token, owner)
    covered = {
        name
        for name in real_names
        if any(name in item["repository"] for item in SEED_ITEMS)
    }
    return sorted(set(real_names) - covered)


def project(token: str) -> dict:
    _, projects = viewer_projects(token)
    result = next((candidate for candidate in projects if candidate["title"] == PROJECT_TITLE), None)
    if result is None:
        raise RuntimeError(f"Project {PROJECT_TITLE!r} does not exist; run the bootstrap workflow first.")
    return result


def project_fields(token: str, project_id: str) -> dict[str, dict]:
    data = graphql(
        token,
        """
        query ProjectFields($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 100) {
                nodes {
                  ... on ProjectV2FieldCommon { id name dataType }
                  ... on ProjectV2SingleSelectField { options { id name } }
                }
              }
            }
          }
        }
        """,
        {"projectId": project_id},
    )["node"]
    return {field["name"]: field for field in data["fields"]["nodes"] if field}


def existing_draft_items(token: str, project_id: str) -> dict[str, str]:
    data = graphql(
        token,
        """
        query ProjectItems($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100) {
                nodes {
                  id
                  content { ... on DraftIssue { title } }
                }
              }
            }
          }
        }
        """,
        {"projectId": project_id},
    )["node"]
    return {
        item["content"]["title"]: item["id"]
        for item in data["items"]["nodes"]
        if item.get("content") and item["content"].get("title")
    }


def items_without_status(token: str, project_id: str) -> set[str]:
    """Ids of items whose Status is empty - which is what a field re-creation
    leaves behind. Those get their default Status again; every item that has
    one keeps it."""
    data = graphql(
        token,
        """
        query ProjectItemStatus($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100) {
                nodes {
                  id
                  fieldValueByName(name: "Status") {
                    ... on ProjectV2ItemFieldSingleSelectValue { name }
                  }
                }
              }
            }
          }
        }
        """,
        {"projectId": project_id},
    )["node"]
    return {item["id"] for item in data["items"]["nodes"] if not item.get("fieldValueByName")}


def create_draft_item(token: str, project_id: str, item: dict) -> str:
    if item.get("hardware", "None") == "None":
        boundary = (
            "This is software-only work. It must not connect to, command or claim validation "
            "of physical hardware, external machinery or safety systems."
        )
    else:
        boundary = (
            f"This work needs: {item['hardware']}. Do not mark it done, or claim validation, "
            "without a recorded bench, device or safety record."
        )
    body = f"""## Objective
{item['objective']}

## Acceptance evidence
{item['acceptance']}

## Boundary
{boundary}
"""
    data = graphql(
        token,
        """
        mutation CreateDraft($input: AddProjectV2DraftIssueInput!) {
          addProjectV2DraftIssue(input: $input) { projectItem { id } }
        }
        """,
        {"input": {"projectId": project_id, "title": item["title"], "body": body}},
    )
    return data["addProjectV2DraftIssue"]["projectItem"]["id"]


def set_text(token: str, project_id: str, item_id: str, field_id: str, value: str) -> None:
    graphql(
        token,
        """
        mutation SetText($input: UpdateProjectV2ItemFieldValueInput!) {
          updateProjectV2ItemFieldValue(input: $input) { projectV2Item { id } }
        }
        """,
        {"input": {"projectId": project_id, "itemId": item_id, "fieldId": field_id, "value": {"text": value}}},
    )


def set_select(token: str, project_id: str, item_id: str, field: dict, option_name: str) -> None:
    option = next((candidate for candidate in field.get("options", []) if candidate["name"] == option_name), None)
    if option is None:
        raise RuntimeError(f"Project field {field['name']!r} has no option {option_name!r}.")
    graphql(
        token,
        """
        mutation SetSelect($input: UpdateProjectV2ItemFieldValueInput!) {
          updateProjectV2ItemFieldValue(input: $input) { projectV2Item { id } }
        }
        """,
        {
            "input": {
                "projectId": project_id,
                "itemId": item_id,
                "fieldId": field["id"],
                "value": {"singleSelectOptionId": option["id"]},
            }
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create missing draft items instead of reporting the plan.")
    args = parser.parse_args()
    token = os.environ.get("HYDRA_UMC_PROJECTS_TOKEN", "")
    if not token:
        print("ROADMAP_SEED=FAIL HYDRA_UMC_PROJECTS_TOKEN is not configured", file=sys.stderr)
        return 2

    viewer, _ = viewer_projects(token)
    target = project(token)
    existing = existing_draft_items(token, target["id"])
    empty_status = items_without_status(token, target["id"])
    missing = [item for item in SEED_ITEMS if item["title"] not in existing]
    print(f"ROADMAP_SEED=PLAN project={target['url']} existing={len(existing)} missing={len(missing)} apply={args.apply}")
    for item in missing:
        print(f"PLAN_ITEM={item['title']}")

    # Coverage-only, never blocking and never auto-fixed: SEED_ITEMS is a
    # real, human-curated list (see this module's own header) - a new
    # repository, or a repository whose real next step nobody has written
    # down yet, shows up here so a human can decide whether it needs one,
    # not so this script invents one on its own.
    uncovered = uncovered_repositories(token, viewer["login"])
    print(f"ROADMAP_SEED_COVERAGE=REPORT uncovered={len(uncovered)}")
    for name in uncovered:
        print(f"UNCOVERED_REPOSITORY={name}")

    if not args.apply:
        print("ROADMAP_SEED=DRY_RUN no Project item was created")
        return 0

    fields = project_fields(token, target["id"])
    if "Affected repositories" not in fields:
        upsert_field(token, target["id"], None, "Affected repositories", "TEXT")
        fields = project_fields(token, target["id"])
        print("FIELD=CREATED name=Affected repositories")
    required = {"Status", "Affected repositories", "Family", "Maturity", "Evidence", "Hardware dependency", "Priority", "Blocked by"}
    missing_fields = sorted(required.difference(fields))
    if missing_fields:
        raise RuntimeError(f"Roadmap is missing required fields: {', '.join(missing_fields)}")

    created = 0
    reconciled = 0
    for item in SEED_ITEMS:
        item_id = existing.get(item["title"])
        is_new = item_id is None
        if item_id is None:
            item_id = create_draft_item(token, target["id"], item)
            created += 1
            print(f"ROADMAP_ITEM=CREATED title={item['title']}")
        else:
            reconciled += 1
            print(f"ROADMAP_ITEM=RECONCILED title={item['title']}")
        # Status and "Blocked by" are set only when the item is created: they are
        # what people move on the board, and a re-run must not undo that.
        if is_new or item_id in empty_status:
            set_select(token, target["id"], item_id, fields["Status"], item.get("status", "Backlog"))
            set_text(token, target["id"], item_id, fields["Blocked by"]["id"], item.get("blocked_by", "None"))
        set_text(token, target["id"], item_id, fields["Affected repositories"]["id"], item["repository"])
        set_select(token, target["id"], item_id, fields["Family"], item["family"])
        set_select(token, target["id"], item_id, fields["Maturity"], item["maturity"])
        set_select(token, target["id"], item_id, fields["Evidence"], item["evidence"])
        set_select(token, target["id"], item_id, fields["Hardware dependency"], item.get("hardware", "None"))
        set_select(token, target["id"], item_id, fields["Priority"], item["priority"])
    print(f"ROADMAP_SEED=PASS created={created} reconciled={reconciled} url={target['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
