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
"""

from __future__ import annotations

import argparse
import os
import sys

from bootstrap_ecosystem_project import PROJECT_TITLE, graphql, viewer_projects


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


def existing_draft_titles(token: str, project_id: str) -> set[str]:
    data = graphql(
        token,
        """
        query ProjectItems($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100) {
                nodes {
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
        item["content"]["title"]
        for item in data["items"]["nodes"]
        if item.get("content") and item["content"].get("title")
    }


def create_draft_item(token: str, project_id: str, item: dict) -> str:
    body = f"""## Objective
{item['objective']}

## Acceptance evidence
{item['acceptance']}

## Boundary
This is software-only work. It must not connect to, command or claim validation
of physical hardware, external machinery or safety systems.
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

    target = project(token)
    existing = existing_draft_titles(token, target["id"])
    missing = [item for item in SEED_ITEMS if item["title"] not in existing]
    print(f"ROADMAP_SEED=PLAN project={target['url']} existing={len(existing)} missing={len(missing)} apply={args.apply}")
    for item in missing:
        print(f"PLAN_ITEM={item['title']}")
    if not args.apply:
        print("ROADMAP_SEED=DRY_RUN no Project item was created")
        return 0

    fields = project_fields(token, target["id"])
    required = {"Status", "Repository", "Family", "Maturity", "Evidence", "Hardware dependency", "Priority", "Blocked by"}
    missing_fields = sorted(required.difference(fields))
    if missing_fields:
        raise RuntimeError(f"Roadmap is missing required fields: {', '.join(missing_fields)}")

    for item in missing:
        item_id = create_draft_item(token, target["id"], item)
        set_select(token, target["id"], item_id, fields["Status"], "Backlog")
        set_text(token, target["id"], item_id, fields["Repository"]["id"], item["repository"])
        set_select(token, target["id"], item_id, fields["Family"], item["family"])
        set_select(token, target["id"], item_id, fields["Maturity"], item["maturity"])
        set_select(token, target["id"], item_id, fields["Evidence"], item["evidence"])
        set_select(token, target["id"], item_id, fields["Hardware dependency"], "None")
        set_select(token, target["id"], item_id, fields["Priority"], item["priority"])
        set_text(token, target["id"], item_id, fields["Blocked by"]["id"], "None")
        print(f"ROADMAP_ITEM=CREATED title={item['title']}")

    print(f"ROADMAP_SEED=PASS created={len(missing)} skipped={len(SEED_ITEMS) - len(missing)} url={target['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
