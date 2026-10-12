#!/usr/bin/env python3
"""F06: prueba de referencia de Sensores; NO es un runtime ni persiste World State.

Reutiliza resolve_sensor_scan.py sin modificarlo. Las salidas son propuestas de
proyección/commit para un futuro adaptador Core, no eventos confirmados.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ENGINE_PATH = ROOT / "tools/simulation/resolve_sensor_scan.py"
spec = importlib.util.spec_from_file_location("f06_existing_sensor_engine", ENGINE_PATH)
assert spec is not None and spec.loader is not None
sensor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sensor)

SIGNATURE_TYPES = {
    "all", "electromagnetic", "subspace", "gravimetric", "thermal",
    "ionizing_radiation", "particle", "biological", "warp",
    "artificial_transponder",
}
RANGE_COST = {"short": 0.12, "long": 0.28, "focused": 0.35}


def finite_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def authorization_binding_valid(request: dict[str, Any], context: dict[str, Any]) -> bool:
    """Correlación de referencia; jamás acredita autorización Core/Host real."""
    b = context.get("authorization_binding")
    if not isinstance(b, dict):
        return False
    expected = {
        "source": "F05_REFERENCE", "decision": "ALLOW_REFERENCE",
        "actor_id": request.get("operator_id"), "action_id": "sensor_scan",
        "station_id": context.get("station_id"), "ship_id": context.get("ship_id"),
        "state_revision": context.get("state_revision"),
    }
    if any(b.get(k) != v for k, v in expected.items()):
        return False
    now, start, end = context.get("current_tick"), b.get("issued_tick"), b.get("expires_tick")
    return all(type(x) is int for x in (now, start, end, context.get("state_revision"))) and start <= now < end


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:18]
    return f"{prefix}:{digest}"


def blocked(reason: str, operation_id: str | None = None) -> dict[str, Any]:
    return {
        "status": "blocked",
        "reason": reason,
        "operation_id": operation_id,
        "authoritative": False,
        "effects_applied": 0,
        "events": [],
        "event_candidates": [],
        "dossier_candidates": [],
        "result": None,
    }


def validate_request(request: dict[str, Any], context: dict[str, Any]) -> str | None:
    """La autorización es una precondición del Core, jamás se infiere del rango."""
    if context.get("authorization_decision") != "ALLOW_REFERENCE":
        return "authorization_not_proven"
    if not context.get("authorization_ref") or not context.get("station_id"):
        return "authorization_or_station_missing"
    if not authorization_binding_valid(request, context):
        return "authorization_binding_invalid_or_stale"
    if context.get("occupied_station") is not True:
        return "station_not_occupied"
    if not request.get("scan_id") or not request.get("observer_id") or not request.get("operator_id"):
        return "missing_identity"
    if not context.get("campaign_time") or not context.get("ship_id"):
        return "missing_time_or_ship"
    if request.get("range_mode") not in RANGE_COST:
        return "unsupported_range_mode"
    if request.get("scan_mode") not in {"passive", "active"}:
        return "unsupported_scan_mode"
    if request.get("resolution") not in {"general", "standard", "high"}:
        return "unsupported_resolution"
    if not isinstance(request.get("filters"), list) or not request["filters"]:
        return "invalid_filters"
    if any(not isinstance(f, str) or f not in SIGNATURE_TYPES for f in request["filters"]):
        return "invalid_filters"
    if "all" in request["filters"] and len(request["filters"]) > 1:
        return "mixed_all_filter"
    if request.get("priority") is not None and (
        not isinstance(request["priority"], str) or request["priority"] not in SIGNATURE_TYPES
    ):
        return "invalid_priority"
    try:
        duration = request["scan_duration_s"]
        profile = request["sensor_profile"]
        coords = request["origin_position_au"]
        if not isinstance(coords, (list, tuple)) or len(coords) != 3:
            return "invalid_origin"
        if not all(finite_number(x) for x in coords):
            return "invalid_origin"
        if not finite_number(duration) or not 0 < duration <= 7200:
            return "invalid_duration"
        if not isinstance(profile, dict) or not all(
            k in profile and finite_number(profile[k]) and 0 <= profile[k] <= 1
            for k in ("capability", "power", "integrity")
        ):
            return "invalid_sensor_profile"
        power = context.get("available_power")
        if not finite_number(power) or not 0 <= power <= 1:
            return "invalid_available_power"
        if power < RANGE_COST[request["range_mode"]]:
            return "insufficient_power"
        if any(profile[k] == 0 for k in ("capability", "power", "integrity")):
            return "sensors_unavailable"
    except (KeyError, TypeError, ValueError, OverflowError):
        return "invalid_numeric_parameters"
    if context.get("selected_array_state") != "operational":
        return "sensor_array_offline"
    if not isinstance(context.get("supported_range_modes"), (list, tuple, set)):
        return "missing_capability_list"
    if request["range_mode"] not in context["supported_range_modes"]:
        return "unsupported_ship_capability"
    if request["range_mode"] == "focused":
        cid = request.get("target_contact_id")
        if not cid or cid not in context.get("known_contact_ids", []):
            return "focused_target_not_known"
    return None


def event(event_type: str, index: int, scan_id: str,
          context: dict[str, Any], operator_id: str, subjects: dict[str, str],
          parent_id: str | None) -> dict[str, Any]:
    eid = stable_id("event", scan_id, event_type, str(index))
    result = {
        "event_id": eid,
        "event_type": event_type,
        "occurred_at": context["campaign_time"],
        "scope": {
            "ship_id": context["ship_id"],
            "station_id": context["station_id"],
            "console_family": "sensors",
        },
        "actor_refs": [operator_id],
        "subject_refs": subjects,
        "provenance": {"system": "f06_reference_only", "authorization_ref": context["authorization_ref"]},
        "visibility": {"audience": "ship_authorized", "projection_required": True},
    }
    if parent_id:
        result["causal_refs"] = [parent_id]
    return result


def dossier_candidates(detections: list[dict[str, Any]],
                       request: dict[str, Any], campaign_time: str) -> list[dict[str, Any]]:
    """Nunca usa entity_id; no fusiona contradicciones ni escribe memoria persistente."""
    records = []
    for d in detections:
        observation_id = stable_id("obs", request["scan_id"], d["contact_id"])
        records.append({
            "contact_id": d["contact_id"],
            "status": "active",
            "first_seen_candidate": campaign_time,
            "last_seen_candidate": campaign_time,
            "observations": [{
                "observation_id": observation_id,
                "source_system": "sensors",
                "operator_id": request["operator_id"],
                "campaign_time": campaign_time,
                "confidence": d["confidence"],
                "data": copy.deepcopy(d["observed"]),
                "provenance": {"scan_id": request["scan_id"], "observer_id": request["observer_id"]},
            }],
            "known_facts_candidates": [
                {"key": key, "value": copy.deepcopy(value),
                 "observation_id": observation_id, "confidence": d["confidence"]}
                for key, value in d["observed"].items()
            ],
            "classification_history_candidate": (
                [{"observation_id": observation_id,
                  "classification": d["observed"]["classification"]}]
                if "classification" in d["observed"] else []
            ),
        })
    return records


def run_reference_scan(world: dict[str, Any], request: dict[str, Any],
                       context: dict[str, Any]) -> dict[str, Any]:
    """Prepara snapshots y eventos candidatos. Core debe revalidar y confirmar TODO."""
    reason = validate_request(request, context)
    if reason:
        return blocked(reason, request.get("scan_id"))
    if not isinstance(world, dict) or not isinstance(world.get("entities"), list):
        return blocked("world_not_materialized", request["scan_id"])
    # Contrato de entrada: no permitir magnitudes no finitas ni objetos rotos
    # antes de invocar un motor de referencia que presupone entradas fiables.
    try:
        json.dumps(world, allow_nan=False)
        if any(not isinstance(entity, dict) or not isinstance(entity.get("entity_id"), str)
               or not entity["entity_id"] or not isinstance(entity.get("signatures", []), list)
               for entity in world["entities"]):
            return blocked("invalid_world", request["scan_id"])
        result = sensor.resolve_scan(world, request)
    except (ValueError, TypeError, KeyError, AttributeError, IndexError, OverflowError):
        return blocked("invalid_world", request["scan_id"])
    partial_request = copy.deepcopy(request)
    partial_request["scan_duration_s"] = max(1.0, float(request["scan_duration_s"]) / 3)
    partial = sensor.resolve_scan(world, partial_request)
    if request["range_mode"] == "focused":
        cid = request["target_contact_id"]
        result["detections"] = [d for d in result["detections"] if d["contact_id"] == cid]
        partial["detections"] = [d for d in partial["detections"] if d["contact_id"] == cid]
    # Nunca exponer métricas del motor sobre entidades/firmas NO detectadas:
    # esas cuentas internas permitirían inferir verdad oculta.
    result["summary"] = {"contacts_detected": len(result["detections"])}
    partial["summary"] = {"contacts_detected": len(partial["detections"])}

    # La lectura parcial no puede revelar más campos que el resultado final.
    result["scan"]["target_contact_id"] = request.get("target_contact_id")
    partial["scan"]["target_contact_id"] = request.get("target_contact_id")
    result_id = stable_id("result", request["observer_id"], request["scan_id"])
    stream = []
    previous = None
    subject = {"operation_id": request["scan_id"]}
    if context.get("order_id"):
        subject["order_id"] = context["order_id"]
    # Un cálculo local NO confirma aceptación de orden, ejecución, reporte ni commit.
    # Estos dos candidatos requieren que Core valide y confirme hechos separados.
    sequence = ["ACTION_STARTED", "RESULT_CREATED"]
    for i, event_type in enumerate(sequence):
        refs = dict(subject)
        if event_type in {"RESULT_CREATED", "REPORT_MADE", "ACTION_COMPLETED"}:
            refs["result_id"] = result_id
        item = event(event_type, i, request["scan_id"], context,
                     request["operator_id"], refs, previous)
        item["candidate_only"] = True
        item["requires_core_confirmation"] = True
        stream.append(item)
        previous = item["event_id"]

    return {
        "status": "reference_completed",
        "operation_id": request["scan_id"],
        "result_id": result_id,
        "authoritative": False,
        "effects_applied": 0,
        "resource_estimate": {
            "power_fraction": RANGE_COST[request["range_mode"]],
            "elapsed_game_seconds": float(request["scan_duration_s"]),
            "reservation_applied": False,
        },
        "partial_result": partial,
        "result": result,
        "dossier_candidates": dossier_candidates(
            result["detections"], request, context["campaign_time"]
        ),
        "events": [],  # No hay eventos autoritativos confirmados.
        "event_candidates": stream,
        "report_pending": {"status": "not_reported", "operator_confirmation_required": True},
        "note": "Candidates only; Core must authorize, reserve, commit, project and persist.",
    }


def science_handoff_candidate(contact_id: str, observation_ids: list[str],
                              dossier: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    """Paquete conocido por la nave; no conoce el mundo ni interpreta ciencia."""
    if dossier.get("contact_id") != contact_id or not observation_ids:
        raise ValueError("unknown_contact_or_empty_selection")
    observed = {o["observation_id"]: o for o in dossier.get("observations", [])}
    if len(observation_ids) != len(set(observation_ids)):
        raise ValueError("duplicate_observations")
    if any(i not in observed for i in observation_ids):
        raise ValueError("unknown_observation")
    if not all(metadata.get(key) for key in ("ship_id", "created_at", "operator_id", "requested_analysis")):
        raise ValueError("missing_handoff_context")
    if metadata.get("priority", "normal") not in {"routine", "normal", "high", "urgent"}:
        raise ValueError("invalid_handoff_priority")
    transfer_id = stable_id("handoff", metadata["ship_id"], contact_id,
                            ",".join(sorted(observation_ids)), metadata["created_at"])
    return {
        "handoff_id": transfer_id,
        "contact_id": contact_id,
        "source_system": "sensors",
        "source_operator_id": metadata["operator_id"],
        "target_system": "science",
        "created_at": metadata["created_at"],
        "priority": metadata.get("priority", "normal"),
        "included_observation_ids": list(observation_ids),
        "requested_analysis": metadata["requested_analysis"],
        "status": "queued",
        "known_observations": copy.deepcopy([observed[i] for i in observation_ids]),
        "provenance": {"ship_id": metadata["ship_id"], "source": "ship_memory"},
        "authoritative": False,
        "effects_applied": 0,
    }


if __name__ == "__main__":
    raise SystemExit("Import run_reference_scan / science_handoff_candidate from tests or adapters.")
