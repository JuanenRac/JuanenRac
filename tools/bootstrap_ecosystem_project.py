#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - GitHub Project bootstrap
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Create or reconcile the public HYDRA-UMC Roadmap Project.

The script is deliberately idempotent: it finds the project by title before
creating it, adds only missing custom fields and creates only missing views.
It never creates issues or claims hardware validation.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections.abc import Mapping


API_URL = "https://api.github.com/graphql"
PROJECT_TITLE = "HYDRA-UMC Roadmap"
PROJECT_DESCRIPTION = "Central planning board for actionable HYDRA-UMC and URTC ecosystem work."
PROJECT_README = """# HYDRA-UMC Roadmap

Central planning board for actionable ecosystem work.

A repository is not a task.
A Discussion is a conversation.
An Issue is scoped work.
A Pull Request is the reviewed implementation.
This Project shows priority, evidence, maturity and blockers.

Physical completion must always link to actual validation evidence.
"""

SELECT_FIELDS = {
    "Status": [
        ("Backlog", "GRAY"),
        ("Ready", "BLUE"),
        ("In progress", "YELLOW"),
        ("Blocked", "RED"),
        ("Done", "GREEN"),
    ],
    "Family": [
        ("Platform Foundation", "BLUE"),
        ("SDK & Server", "PURPLE"),
        ("Robotics & Simulation", "ORANGE"),
        ("Vision & AI", "PINK"),
        ("URTC", "GREEN"),
        ("External Automation Bridges", "YELLOW"),
        ("Applications", "GRAY"),
    ],
    "Maturity": [
        ("Scaffold", "GRAY"),
        ("Functional", "BLUE"),
        ("Established", "GREEN"),
        ("Production", "PURPLE"),
    ],
    "Evidence": [
        ("Documentation", "GRAY"),
        ("Local test", "BLUE"),
        ("Simulator", "PURPLE"),
        ("CM5", "YELLOW"),
        ("MCU", "ORANGE"),
        ("External machine", "PINK"),
        ("Safety validation", "RED"),
    ],
    "Hardware dependency": [
        ("None", "GREEN"),
        ("CM5", "YELLOW"),
        ("MCU", "ORANGE"),
        ("Vision/Hailo", "PURPLE"),
        ("Robot/actuator", "RED"),
        ("External machine", "PINK"),
    ],
    "Priority": [
        ("Critical", "RED"),
        ("High", "ORANGE"),
        ("Normal", "BLUE"),
        ("Low", "GRAY"),
    ],
}
TEXT_FIELDS = ("Repository", "Blocked by")
VIEWS = (
    ("Ecosystem Backlog", "TABLE"),
    ("Active Work", "BOARD"),
    ("Software toward 95%", "TABLE"),
    ("Awaiting Hardware", "TABLE"),
    ("Safety Validation", "TABLE"),
)


def graphql(token: str, query: str, variables: Mapping[str, object] | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2026-03-10",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API HTTP {error.code}: {detail[:500]}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"GitHub API connection error: {error.reason}") from error

    if result.get("errors"):
        messages = "; ".join(error.get("message", "unknown GraphQL error") for error in result["errors"])
        raise RuntimeError(f"GitHub GraphQL error: {messages}")
    return result["data"]


def viewer_projects(token: str) -> tuple[dict, list[dict]]:
    data = graphql(
        token,
        """
        query ViewerProjects {
          viewer {
            id
            login
            projectsV2(first: 100) {
              nodes { id number title url }
            }
          }
        }
        """,
    )
    viewer = data["viewer"]
    return viewer, viewer["projectsV2"]["nodes"]


def create_project(token: str, owner_id: str) -> dict:
    data = graphql(
        token,
        """
        mutation CreateProject($input: CreateProjectV2Input!) {
          createProjectV2(input: $input) {
            projectV2 { id number title url }
          }
        }
        """,
        {"input": {"ownerId": owner_id, "title": PROJECT_TITLE}},
    )
    return data["createProjectV2"]["projectV2"]


def update_project_settings(token: str, project_id: str) -> None:
    graphql(
        token,
        """
        mutation UpdateProject($input: UpdateProjectV2Input!) {
          updateProjectV2(input: $input) { projectV2 { id } }
        }
        """,
        {
            "input": {
                "projectId": project_id,
                "title": PROJECT_TITLE,
                "public": True,
                "shortDescription": PROJECT_DESCRIPTION,
                "readme": PROJECT_README,
            }
        },
    )


def project_structure(token: str, project_id: str) -> tuple[dict[str, dict], dict[str, dict]]:
    data = graphql(
        token,
        """
        query ProjectStructure($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 100) {
                nodes {
                  ... on ProjectV2FieldCommon { id name dataType }
                }
              }
              views(first: 100) { nodes { id name layout } }
            }
          }
        }
        """,
        {"projectId": project_id},
    )["node"]
    fields = {field["name"]: field for field in data["fields"]["nodes"] if field}
    views = {view["name"]: view for view in data["views"]["nodes"]}
    return fields, views


def upsert_field(token: str, project_id: str, field: dict | None, name: str, data_type: str, options: list[tuple[str, str]] | None = None) -> None:
    if field is None:
        input_value: dict[str, object] = {"projectId": project_id, "name": name, "dataType": data_type}
        if options:
            input_value["singleSelectOptions"] = [
                {"name": option_name, "color": color, "description": option_name}
                for option_name, color in options
            ]
        graphql(
            token,
            """
            mutation CreateField($input: CreateProjectV2FieldInput!) {
              createProjectV2Field(input: $input) { projectV2Field { __typename } }
            }
            """,
            {"input": input_value},
        )
        print(f"FIELD=CREATED name={name}")
        return

    if options:
        graphql(
            token,
            """
            mutation UpdateField($input: UpdateProjectV2FieldInput!) {
              updateProjectV2Field(input: $input) { projectV2Field { __typename } }
            }
            """,
            {
                "input": {
                    "fieldId": field["id"],
                    "name": name,
                    "singleSelectOptions": [
                        {"name": option_name, "color": color, "description": option_name}
                        for option_name, color in options
                    ],
                }
            },
        )
        print(f"FIELD=RECONCILED name={name}")
    else:
        print(f"FIELD=EXISTS name={name}")


def upsert_views(token: str, project_id: str, views: dict[str, dict]) -> None:
    if "Ecosystem Backlog" not in views and views:
        default_view = next(iter(views.values()))
        graphql(
            token,
            """
            mutation RenameView($input: UpdateProjectV2ViewInput!) {
              updateProjectV2View(input: $input) { projectV2View { id } }
            }
            """,
            {"input": {"viewId": default_view["id"], "name": "Ecosystem Backlog", "layout": "TABLE"}},
        )
        views["Ecosystem Backlog"] = default_view
        print("VIEW=RENAMED name=Ecosystem Backlog")

    for name, layout in VIEWS:
        if name in views:
            graphql(
                token,
                """
                mutation ReconcileView($input: UpdateProjectV2ViewInput!) {
                  updateProjectV2View(input: $input) { projectV2View { id } }
                }
                """,
                {"input": {"viewId": views[name]["id"], "name": name, "layout": layout}},
            )
            print(f"VIEW=RECONCILED name={name}")
            continue
        graphql(
            token,
            """
            mutation CreateView($input: CreateProjectV2ViewInput!) {
              createProjectV2View(input: $input) { projectV2View { id } }
            }
            """,
            {"input": {"projectId": project_id, "name": name, "layout": layout}},
        )
        print(f"VIEW=CREATED name={name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create or reconcile the Project instead of reporting the plan.")
    args = parser.parse_args()
    token = os.environ.get("HYDRA_UMC_PROJECTS_TOKEN", "")
    if not token:
        print("PROJECT_BOOTSTRAP=FAIL HYDRA_UMC_PROJECTS_TOKEN is not configured", file=sys.stderr)
        return 2

    viewer, projects = viewer_projects(token)
    project = next((candidate for candidate in projects if candidate["title"] == PROJECT_TITLE), None)
    state = "existing" if project else "absent"
    print(f"PROJECT_BOOTSTRAP=PLAN owner={viewer['login']} project={PROJECT_TITLE!r} state={state} apply={args.apply}")
    if not args.apply:
        print("PROJECT_BOOTSTRAP=DRY_RUN no GitHub Project was changed")
        return 0

    if project is None:
        project = create_project(token, viewer["id"])
        print(f"PROJECT=CREATED url={project['url']}")
    else:
        print(f"PROJECT=EXISTS url={project['url']}")

    update_project_settings(token, project["id"])
    fields, views = project_structure(token, project["id"])
    for name, options in SELECT_FIELDS.items():
        upsert_field(token, project["id"], fields.get(name), name, "SINGLE_SELECT", options)
    for name in TEXT_FIELDS:
        upsert_field(token, project["id"], fields.get(name), name, "TEXT")
    _, views = project_structure(token, project["id"])
    upsert_views(token, project["id"], views)
    print(f"PROJECT_BOOTSTRAP=PASS url={project['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
