#!/usr/bin/env python3
"""Sensor Detection Resolution v0.1 for the Star Trek vertical slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ENGINE_ID = "sensor_detection_resolution"
ENGINE_VERSION = "0.1.0"

STRENGTH_SCORE = {
    "trace": 0.22,
    "weak": 0.38,
    "moderate": 0.58,
    "strong": 0.78,
    "extreme": 0.96,
}

STATE_THRESHOLDS = [
    (0.72, "resolved"),
    (0.54, "partially_resolved"),
    (0.38, "detected_unclassified"),
    (0.24, "trace_detected"),
]

STATE_RANK = {
    "not_detected": 0,
    "trace_detected": 1,
    "detected_unclassified": 2,
    "partially_resolved": 3,
    "resolved": 4,
}

RESOLUTION_RANK = {
    "general": 1,
    "standard": 2,
    "high": 3,
}

RANGE_PROFILES = {
    "short": {"max_range_au": 2.0, "sensitivity_bonus": 0.10},
    "long": {"max_range_au": 30.0, "sensitivity_bonus": 0.00},
    "focused": {"max_range_au": 50.0, "sensitivity_bonus": 0.16},
}

RESOLUTION_FACTORS = {
    "general": 0.94,
    "standard": 1.00,
    "high": 1.08,
}

SCAN_MODE_FACTORS = {
    "passive": 0.92,
    "active": 1.08,
}

INTERFERENCE_PENALTY = {
    "subspace_noise": 0.10,
    "charged_particles": 0.08,
    "gravimetric_turbulence": 0.10,
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def distance_au(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((float(a[i]) - float(b[i])) ** 2 for i in range(3)))


def contact_id(observer_id: str, entity_id: str) -> str:
    digest = hashlib.sha256(f"{observer_id}|{entity_id}".encode("utf-8")).hexdigest()[:14]
    return f"contact:{digest}"


def normalized_request(request: dict[str, Any]) -> dict[str, Any]:
    range_mode = request.get("range_mode", "long")
    resolution = request.get("resolution", "standard")
    scan_mode = request.get("scan_mode", "passive")
    filters = request.get("filters", ["all"])

    if range_mode not in RANGE_PROFILES:
        raise ValueError(f"unsupported range_mode: {range_mode}")
    if resolution not in RESOLUTION_RANK:
        raise ValueError(f"unsupported resolution: {resolution}")
    if scan_mode not in SCAN_MODE_FACTORS:
        raise ValueError(f"unsupported scan_mode: {scan_mode}")
    if not isinstance(filters, list) or not filters:
        raise ValueError("filters must be a non-empty list")

    sensor = request.get("sensor_profile", {})
    normalized = {
        "scan_id": str(request.get("scan_id", "scan:anonymous")),
        "observer_id": str(request.get("observer_id", "observer:unknown")),
        "operator_id": request.get("operator_id"),
        "origin_position_au": [float(v) for v in request.get("origin_position_au", [0.0, 0.0, 0.0])],
        "sector_id": request.get("sector_id"),
        "system_id": request.get("system_id"),
        "range_mode": range_mode,
        "scan_mode": scan_mode,
        "resolution": resolution,
        "filters": [str(v) for v in filters],
        "priority": request.get("priority"),
        "scan_duration_s": max(1.0, float(request.get("scan_duration_s", 10.0))),
        "sensor_profile": {
            "capability": clamp(float(sensor.get("capability", 0.75))),
            "power": clamp(float(sensor.get("power", 1.0))),
            "integrity": clamp(float(sensor.get("integrity", 1.0))),
        },
    }
    if len(normalized["origin_position_au"]) != 3:
        raise ValueError("origin_position_au must contain exactly 3 values")
    return normalized


def entity_is_in_scope(entity: dict[str, Any], request: dict[str, Any]) -> bool:
    spatial = entity.get("spatial_state", {})
    if request.get("sector_id") and spatial.get("sector_id") != request["sector_id"]:
        return False
    if request.get("system_id") and spatial.get("system_id") != request["system_id"]:
        return False
    return bool(entity.get("temporal_state", {}).get("active", True))


def distance_factor(distance: float, max_range: float) -> float:
    if distance > max_range:
        return 0.0
    ratio = distance / max_range if max_range > 0 else 1.0
    return clamp(1.0 - 0.55 * (ratio ** 1.35), 0.25, 1.0)


def duration_factor(seconds: float) -> float:
    return clamp(0.86 + 0.10 * math.log10(max(1.0, seconds)), 0.80, 1.08)


def filter_factor(signature_type: str, request: dict[str, Any]) -> float:
    filters = set(request["filters"])
    priority = request.get("priority")
    if "all" not in filters and signature_type not in filters:
        return 0.0
    factor = 1.0
    if signature_type in filters and "all" not in filters:
        factor += 0.14
    if priority == signature_type:
        factor += 0.12
    return factor


def interference_penalty(entity: dict[str, Any], signature: dict[str, Any]) -> float:
    env = entity.get("environmental_modifiers", {})
    penalty = 0.0
    for item in set(env.get("masking", []) + env.get("local_interference", [])):
        penalty += INTERFERENCE_PENALTY.get(item, 0.06)
    penalty += float(signature.get("detectability_modifiers", {}).get("masking", 0.0))
    return clamp(penalty, 0.0, 0.55)


def score_signature(
    entity: dict[str, Any],
    signature: dict[str, Any],
    request: dict[str, Any],
) -> tuple[float, float]:
    spatial = entity.get("spatial_state", {})
    position = spatial.get("position", {}).get("xyz")
    if not isinstance(position, list) or len(position) != 3:
        return 0.0, math.inf

    distance = distance_au(request["origin_position_au"], [float(v) for v in position])
    range_profile = RANGE_PROFILES[request["range_mode"]]
    if distance > range_profile["max_range_au"]:
        return 0.0, distance

    strength = STRENGTH_SCORE.get(signature.get("strength"), 0.30)
    filt = filter_factor(signature.get("signature_type", ""), request)
    if filt == 0.0:
        return 0.0, distance

    sensor = request["sensor_profile"]
    equipment = 0.45 + 0.55 * sensor["capability"]
    power = 0.55 + 0.45 * sensor["power"]
    integrity = 0.45 + 0.55 * sensor["integrity"]

    score = strength
    score *= distance_factor(distance, range_profile["max_range_au"])
    score *= equipment * power * integrity
    score *= SCAN_MODE_FACTORS[request["scan_mode"]]
    score *= RESOLUTION_FACTORS[request["resolution"]]
    score *= duration_factor(request["scan_duration_s"])
    score *= filt
    score += range_profile["sensitivity_bonus"]
    score -= interference_penalty(entity, signature)

    return clamp(score), distance


def state_for_score(score: float) -> str:
    for threshold, state in STATE_THRESHOLDS:
        if score >= threshold:
            return state
    return "not_detected"


def confidence_for_score(score: float) -> float:
    if score < 0.24:
        return 0.0
    return round(clamp((score - 0.18) / 0.72), 3)


def estimate_position(position: list[float], confidence: float) -> dict[str, Any]:
    if confidence >= 0.75:
        digits = 4
        precision = "high"
    elif confidence >= 0.50:
        digits = 2
        precision = "standard"
    else:
        digits = 1
        precision = "coarse"
    return {
        "unit": "AU",
        "xyz": [round(float(v), digits) for v in position],
        "precision": precision,
    }


def hidden_property_revealed(meta: dict[str, Any], request: dict[str, Any], state: str) -> bool:
    if STATE_RANK[state] < STATE_RANK["resolved"]:
        return False
    minimum = meta.get("minimum_resolution", "high")
    if RESOLUTION_RANK[request["resolution"]] < RESOLUTION_RANK.get(minimum, 3):
        return False
    preferred = meta.get("preferred_filter")
    if preferred:
        filters = set(request["filters"])
        if preferred not in filters and request.get("priority") != preferred:
            return False
    return True


def build_observation(
    entity: dict[str, Any],
    request: dict[str, Any],
    signature_results: list[dict[str, Any]],
) -> dict[str, Any] | None:
    visible = [s for s in signature_results if s["state"] != "not_detected"]
    if not visible:
        return None

    best = max(visible, key=lambda item: item["score"])
    state = best["state"]
    confidence = confidence_for_score(best["score"])
    ground = entity.get("ground_truth", {})
    position = entity.get("spatial_state", {}).get("position", {}).get("xyz", [0.0, 0.0, 0.0])

    observed: dict[str, Any] = {}
    if STATE_RANK[state] >= STATE_RANK["detected_unclassified"]:
        observed["estimated_position"] = estimate_position(position, confidence)
    if STATE_RANK[state] >= STATE_RANK["partially_resolved"]:
        observed["entity_type"] = entity.get("entity_type")
        observed["properties"] = dict(ground.get("properties", {}))
    if STATE_RANK[state] >= STATE_RANK["resolved"]:
        observed["classification"] = ground.get("classification")

    hidden_reveals: dict[str, Any] = {}
    if STATE_RANK[state] >= STATE_RANK["resolved"]:
        for key, meta in ground.get("hidden_properties", {}).items():
            if isinstance(meta, dict) and hidden_property_revealed(meta, request, state):
                hidden_reveals[key] = meta.get("value")
    if hidden_reveals:
        observed["resolved_hidden_properties"] = hidden_reveals

    return {
        "contact_id": contact_id(request["observer_id"], entity["entity_id"]),
        "resolution_state": state,
        "confidence": confidence,
        "distance_au": round(best["distance_au"], 6),
        "observed_signatures": [
            {
                "signature_type": s["signature_type"],
                "state": s["state"],
                "confidence": confidence_for_score(s["score"]),
            }
            for s in sorted(visible, key=lambda item: (-item["score"], item["signature_type"]))
        ],
        "observed": observed,
    }


def resolve_scan(world: dict[str, Any], raw_request: dict[str, Any]) -> dict[str, Any]:
    request = normalized_request(raw_request)
    detections: list[dict[str, Any]] = []
    in_scope = 0
    evaluated_signatures = 0

    for entity in world.get("entities", []):
        if not entity_is_in_scope(entity, request):
            continue
        in_scope += 1
        sig_results: list[dict[str, Any]] = []
        for sig in entity.get("signatures", []):
            evaluated_signatures += 1
            score, distance = score_signature(entity, sig, request)
            sig_results.append({
                "signature_type": sig.get("signature_type"),
                "score": round(score, 6),
                "state": state_for_score(score),
                "distance_au": distance,
            })
        observation = build_observation(entity, request, sig_results)
        if observation:
            detections.append(observation)

    detections.sort(key=lambda item: (item["distance_au"], item["contact_id"]))

    return {
        "schema_version": "0.1.0",
        "engine": {
            "engine_id": ENGINE_ID,
            "engine_version": ENGINE_VERSION,
            "model": "deterministic_normalized_gameplay_v1",
        },
        "scan": {
            "scan_id": request["scan_id"],
            "observer_id": request["observer_id"],
            "operator_id": request["operator_id"],
            "range_mode": request["range_mode"],
            "scan_mode": request["scan_mode"],
            "resolution": request["resolution"],
            "filters": request["filters"],
            "priority": request["priority"],
            "scan_duration_s": request["scan_duration_s"],
            "sector_id": request["sector_id"],
            "system_id": request["system_id"],
        },
        "summary": {
            "entities_in_scope": in_scope,
            "signatures_evaluated": evaluated_signatures,
            "contacts_detected": len(detections),
        },
        "detections": detections,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world", required=True, type=Path, help="Materialized world JSON.")
    parser.add_argument("--request", required=True, type=Path, help="Sensor scan request JSON.")
    parser.add_argument("--output", type=Path, help="Result JSON. Stdout if omitted.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    world = json.loads(args.world.read_text(encoding="utf-8"))
    request = json.loads(args.request.read_text(encoding="utf-8"))
    result = resolve_scan(world, request)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
