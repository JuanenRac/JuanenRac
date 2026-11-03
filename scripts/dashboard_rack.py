#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_rack.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""The URTC tool rack page of the status dashboard.

The snapshot is the one URTC-COMMON writes (`rack_status.snapshot`, schema 1): the slots with their tool, unit, target and thermal verdict, the wear of each
unit, the alarms and the counters. The dashboard never reads a rack: it shows the snapshot that is published in `data/rack-snapshot.json`, says where it
comes from and, when there is none or it cannot be used, says "no data" instead of any state. Every value is escaped; the text of the alarms and of the
thermal verdicts is translated by the page from the codes the snapshot carries.

Stdlib only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from dashboard_charts import esc

SNAPSHOT_PATH = Path(__file__).resolve().parent.parent / "data" / "rack-snapshot.json"
SCHEMA = 1
MAX_SLOTS = 64
VERDICTS = ("unknown", "empty_ok", "heater_in_empty_slot", "idle_ok", "still_hot", "heating", "reached", "not_reached", "overshoot")
_ALARM_MAINTENANCE = re.compile(r"^slot (\d+): maintenance due for unit (.{1,40})$")
_ALARM_EXPIRED = re.compile(r"^slot (\d+): pre-heat limit reached, the target was switched off$")
_ALARM_THERMAL = re.compile(r"^slot (\d+): thermal check says ([a-z_]{1,40})$")


def _int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate(raw: object) -> tuple[dict | None, str]:
    """(snapshot, "") when `raw` has the shape `rack_status.snapshot` writes, otherwise (None, the reason in English)."""
    if not isinstance(raw, dict):
        return None, "not a JSON object"
    if raw.get("schema") != SCHEMA:
        return None, f"schema {raw.get('schema')!r} is not {SCHEMA}"
    for key in ("name", "source"):
        if not isinstance(raw.get(key), str) or not raw[key].strip() or len(raw[key]) > 80:
            return None, f"{key} is missing or too long"
    for key in ("occupied", "slot_count", "heating", "maintenance_due"):
        if not _int(raw.get(key)):
            return None, f"{key} is not a whole number"
    slots, alarms = raw.get("slots"), raw.get("alarms")
    if not isinstance(slots, list) or len(slots) > MAX_SLOTS or not slots:
        return None, "slots is missing or too long"
    if not isinstance(alarms, list) or not all(isinstance(a, str) and len(a) < 200 for a in alarms) or len(alarms) > 4 * MAX_SLOTS:
        return None, "alarms is not a list of texts"
    for item in slots:
        if not isinstance(item, dict) or not _int(item.get("slot")) or not isinstance(item.get("occupied"), bool):
            return None, "a slot is malformed"
        if not isinstance(item.get("target_c"), (int, float)) or isinstance(item.get("target_c"), bool):
            return None, "a slot has no numeric target"
        for key in ("unit", "thermal"):
            if item.get(key) is not None and (not isinstance(item[key], str) or len(item[key]) > 40):
                return None, f"slot {item['slot']}: {key} is malformed"
        if item.get("tool_id") is not None and not _int(item["tool_id"]):
            return None, f"slot {item['slot']}: tool_id is malformed"
        wear = item.get("wear")
        if wear is not None and (not isinstance(wear, dict) or not all(_int(wear.get(k, 0)) for k in ("cycles", "heater_seconds"))):
            return None, f"slot {item['slot']}: wear is malformed"
    return raw, ""


def load(path: Path = SNAPSHOT_PATH) -> tuple[dict | None, str]:
    """(snapshot, "") | (None, "") when no snapshot is published | (None, reason) when the file cannot be used."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, ""
    except OSError as exc:
        return None, f"cannot be read: {exc.__class__.__name__}"
    try:
        raw = json.loads(text)
    except ValueError:
        return None, "not valid JSON"
    return validate(raw)


def card(snap: dict | None) -> dict:
    """The state of the rack as the overview needs it: 'alarm' | 'ok' | 'nodata' (the rule of rack_status.card, and nothing without a snapshot)."""
    if snap is None:
        return {"state": "nodata"}
    return {"state": "alarm" if snap["alarms"] else "ok"}


def _t(key: str, en: dict, **values: object) -> str:
    text = en[key]
    for name, value in values.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def _alarm_item(text: str, en: dict) -> str:
    for pattern, key, names in ((_ALARM_MAINTENANCE, "rack_alarm_maintenance", ("slot", "unit")), (_ALARM_EXPIRED, "rack_alarm_expired", ("slot",)),
                                (_ALARM_THERMAL, "rack_alarm_thermal", ("slot", "verdict"))):
        match = pattern.match(text)
        if match:
            values = dict(zip(names, match.groups()))
            verdict = values.get("verdict")
            if verdict is not None and verdict in VERDICTS:
                return (f'<li data-testid="rack-alarm" data-slot="{esc(values["slot"])}" data-verdict-key="rack_v_{esc(verdict)}" data-i18n-template="{key}" '
                        f'data-verdict="{esc(en["rack_v_" + verdict])}">{esc(_t(key, en, slot=values["slot"], verdict=en["rack_v_" + verdict]))}</li>')
            attrs = "".join(f' data-{n}="{esc(v)}"' for n, v in values.items())
            return f'<li data-testid="rack-alarm" data-i18n-template="{key}"{attrs}>{esc(_t(key, en, **values))}</li>'
    return f'<li data-testid="rack-alarm">{esc(text)}</li>'


def _verdict(value: str | None, en: dict) -> str:
    if not value or value == "unknown":
        return f'<span data-i18n="not_verified">Not verified</span>'
    if value in VERDICTS:
        return f'<span data-i18n="rack_v_{esc(value)}">{esc(en["rack_v_" + value])}</span>'
    return f"<span>{esc(value)}</span>"


def _wear(slot: dict, en: dict) -> str:
    if slot.get("maintenance_due"):
        return f'<span class="rack-flag" data-i18n="rack_wear_maintenance">{esc(en["rack_wear_maintenance"])}</span>'
    wear = slot.get("wear")
    if not wear:
        return '<span data-i18n="no_data">No data</span>'
    cycles, seconds = int(wear.get("cycles", 0)), int(wear.get("heater_seconds", 0))
    return (f'<span data-i18n-template="rack_wear" data-cycles="{cycles}" data-seconds="{seconds}">'
            f'{esc(_t("rack_wear", en, cycles=cycles, seconds=seconds))}</span>')


def panel_html(snap: dict | None, problem: str = "") -> str:
    """The content of the rack tab."""
    import dashboard_robust_texts
    en = dashboard_robust_texts.TEXTS["en"]
    head = (f'<header class="card-head"><h2 class="card-title" id="rack-t" data-i18n="rack_title">{esc(en["rack_title"])}</h2>'
            f'<p class="muted" data-i18n="rack_intro">{esc(en["rack_intro"])}</p></header>')
    state = card(snap)["state"]
    glyph = {"ok": "●", "alarm": "▲", "nodata": "?"}[state]
    if snap is None:
        reason = (f'<p class="muted" data-testid="rack-invalid" data-i18n-template="rack_invalid" data-reason="{esc(problem)}">{esc(_t("rack_invalid", en, reason=problem))}</p>'
                  if problem else "")
        return (f'<section class="card card-rack" aria-labelledby="rack-t" data-testid="rack" data-state="nodata">{head}'
                f'<p class="rack-state rack-nodata" role="status" data-testid="rack-state" data-state="nodata"><span class="rack-glyph" aria-hidden="true">{glyph}</span>'
                f'<span data-i18n="rack_state_nodata">{esc(en["rack_state_nodata"])}</span></p>'
                f'<p data-i18n="rack_nodata" data-testid="rack-nodata">{esc(en["rack_nodata"])}</p>{reason}</section>')
    slots = snap["slots"]
    rows = []
    for s in slots:
        tool = (f'<span>{esc(s["tool_id"])}</span>' if s.get("tool_id") is not None else f'<span class="muted" data-i18n="rack_empty">{esc(en["rack_empty"])}</span>')
        unit = esc(s["unit"]) if s.get("unit") else "–"
        rows.append(f'<tr data-testid="rack-slot" data-slot="{s["slot"]}"><th scope="row">{s["slot"]}</th><td>{tool}</td><td>{unit}</td>'
                    f'<td>{esc(s["target_c"])}</td><td>{_verdict(s.get("thermal"), en)}</td><td>{_wear(s, en)}</td></tr>')
    alarms = "".join(_alarm_item(a, en) for a in snap["alarms"]) or f'<li data-i18n="rack_alarms_none" data-testid="rack-no-alarms">{esc(en["rack_alarms_none"])}</li>'
    sim = (f'<p class="rack-sim" data-testid="rack-sim" data-i18n="rack_source_sim">{esc(en["rack_source_sim"])}</p>' if snap["source"].strip().lower() == "simulation" else "")
    cols = "".join(f'<th scope="col" data-i18n="rack_col_{k}">{esc(en["rack_col_" + k])}</th>' for k in ("slot", "tool", "unit", "target", "thermal", "wear"))
    return (
        f'<section class="card card-rack" aria-labelledby="rack-t" data-testid="rack" data-state="{state}">{head}'
        f'<p class="rack-state rack-{state}" role="status" data-testid="rack-state" data-state="{state}"><span class="rack-glyph" aria-hidden="true">{glyph}</span>'
        f'<span data-i18n="rack_state_{state}">{esc(en["rack_state_" + state])}</span> · <strong>{esc(snap["name"])}</strong></p>'
        f'<p class="muted" data-testid="rack-source" data-i18n-template="rack_source" data-source="{esc(snap["source"])}">{esc(_t("rack_source", en, source=snap["source"]))}</p>{sim}'
        f'<p data-testid="rack-summary" data-i18n-template="rack_summary" data-used="{snap["occupied"]}" data-slots="{snap["slot_count"]}" data-heating="{snap["heating"]}" '
        f'data-maintenance="{snap["maintenance_due"]}">{esc(_t("rack_summary", en, used=snap["occupied"], slots=snap["slot_count"], heating=snap["heating"], maintenance=snap["maintenance_due"]))}</p>'
        f'<h3 class="rack-sub" data-i18n="rack_alarms_title">{esc(en["rack_alarms_title"])}</h3><ul class="rack-alarms" data-testid="rack-alarms">{alarms}</ul>'
        f'<h3 class="rack-sub" data-i18n="rack_slots_title">{esc(en["rack_slots_title"])}</h3>'
        f'<div class="rack-scroll" tabindex="0" role="region" aria-labelledby="rack-t"><table class="rack-table" data-testid="rack-table">'
        f'<caption class="sr-only" data-i18n="rack_caption">{esc(en["rack_caption"])}</caption><thead><tr>{cols}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
        '</section>'
    )
