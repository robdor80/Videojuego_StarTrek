#!/usr/bin/env python3
"""F09: verificador de transferencia de DATOS; sin Core, persistencia ni UE5.

'trust' es una instantánea confiable de Core/Host; NUNCA debe venir del
cliente, de un prompt de IA ni de campos incluidos en el paquete de datos.
Las decisiones ACCEPT_DATA_ONLY no realizan acciones ni crean hechos.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "sistemas/gameplay/ship_operations/consoles/f09_reference_matrix_v0.1.json"

CANONICAL = (
    "command", "conn", "navigation", "operations", "sensors", "science",
    "tactical", "security", "engineering", "communications", "mission_ops",
    "transporter", "medical", "environmental", "flight_deck", "computer",
)
REQUIRED = ("package_id", "source_system", "target_system",
            "created_at", "payload_refs", "provenance")
# Sólo metadatos/refs del contrato existente; no aceptar datos sensibles inline.
ALLOWED = frozenset(REQUIRED + (
    "source_station", "source_operator_id", "priority",
    "operator_note", "requested_action", "status",
))
PRIORITIES = frozenset(("routine", "normal", "high", "urgent"))
STATUSES = frozenset(("queued", "delivered", "accepted", "rejected", "completed"))
RESULT_ACCEPT = "ACCEPT_DATA_ONLY"
RESULT_DENY = "DENY"
RESULT_CLARIFY = "CLARIFY_TARGET"


def catalog_errors(matrix: dict[str, Any], root: Path = ROOT) -> list[str]:
    """Validación estática del registro contra los 16 directorios reales."""
    errors: list[str] = []
    entries = matrix.get("families")
    if not isinstance(entries, list):
        return ["families debe ser una lista"]
    ids = [x.get("id") for x in entries if isinstance(x, dict)]
    if len(entries) != 16 or len(ids) != 16 or tuple(ids) != CANONICAL:
        errors.append("exactamente las 16 familias canónicas, sin duplicados")
    if matrix.get("family_count") != 16:
        errors.append("family_count debe ser 16")
    if matrix.get("status") != "reference_only_not_runtime":
        errors.append("la referencia no puede anunciar runtime")
    for item in entries:
        if not isinstance(item, dict):
            errors.append("entrada de familia inválida")
            continue
        name = item.get("id")
        if name not in CANONICAL:
            errors.append("familia desconocida")
            continue
        if item.get("status") != "design_reference":
            errors.append(f"{name}: status impropio")
        if item.get("step") not in ("P01", "P02", "P03", "BASE"):
            errors.append(f"{name}: paso inválido")
        if not (root / f"sistemas/gameplay/ship_operations/consoles/{name}/README.md").is_file():
            errors.append(f"{name}: directorio base inexistente")
        refs = item.get("existing_contract_refs")
        if not isinstance(refs, list) or not refs or any(
            not isinstance(p, str) or not (root / p).is_file() for p in refs
        ):
            errors.append(f"{name}: referencia inexistente")
        targets = item.get("allowed_data_handoff_targets")
        if not isinstance(targets, list) or not targets or any(not isinstance(t, str) for t in targets) or len(set(targets)) != len(targets) or any(
            t not in CANONICAL or t == name for t in targets
        ):
            errors.append(f"{name}: destinos inválidos")
        if not isinstance(item.get("operations_proposed_es"), list) or not item["operations_proposed_es"]:
            errors.append(f"{name}: faltan operaciones propuestas")
    return errors


def load_catalog(path: Path = MATRIX) -> dict[str, Any]:
    matrix = json.loads(path.read_text(encoding="utf-8"))
    errors = catalog_errors(matrix)
    if errors:
        raise ValueError("; ".join(errors))
    return matrix


def assess_handoff(packet: Any, trust: Any, matrix: dict[str, Any]) -> dict[str, str]:
    """Decisión pura sobre la transferencia, NO autorización para actuar.

    trust se supone emitido por un sistema fiable: known_refs y
    permitted_routes son instantáneas pertinentes al actor/contexto.
    Revalidar contra Core al ejecutar; jamás usar esta respuesta como token.
    """
    def result(decision: str, reason: str) -> dict[str, str]:
        return {"decision": decision, "reason": reason}

    if not isinstance(packet, dict) or not isinstance(trust, dict):
        return result(RESULT_DENY, "invalid_input")
    if not all(key in packet for key in REQUIRED):
        return result(RESULT_DENY, "missing_required_fields")
    if set(packet) - ALLOWED:
        return result(RESULT_DENY, "inline_or_unrecognized_fields")
    source, target = packet["source_system"], packet["target_system"]
    if target in matrix.get("legacy_target_values_requiring_explicit_resolution", []):
        return result(RESULT_CLARIFY, "ambiguous_legacy_target")
    if not isinstance(source, str) or not isinstance(target, str) or source not in CANONICAL or target not in CANONICAL:
        return result(RESULT_DENY, "unknown_console")
    if source == target:
        return result(RESULT_DENY, "same_family_not_handoff")
    entries = {x["id"]: x for x in matrix["families"]}
    if target not in entries[source]["allowed_data_handoff_targets"]:
        return result(RESULT_DENY, "route_not_designed")
    if not all(isinstance(packet[key], str) and 0 < len(packet[key]) <= 128
               for key in ("package_id", "created_at")):
        return result(RESULT_DENY, "invalid_identity_or_time")
    if not isinstance(packet.get("priority", "normal"), str) or packet.get("priority", "normal") not in PRIORITIES:
        return result(RESULT_DENY, "unknown_priority")
    if not isinstance(packet.get("status", "queued"), str) or packet.get("status", "queued") not in STATUSES:
        return result(RESULT_DENY, "unknown_status")
    refs = packet["payload_refs"]
    if (not isinstance(refs, list) or not 1 <= len(refs) <= 32 or
        any(not isinstance(ref, str) or not 1 <= len(ref) <= 128 for ref in refs) or
        len(set(refs)) != len(refs)):
        return result(RESULT_DENY, "invalid_payload_refs")
    provenance = packet["provenance"]
    if (not isinstance(provenance, dict) or
        set(provenance) != {"source_refs", "source_system", "confidence"} or
        provenance["source_system"] != source or
        provenance["source_refs"] != refs or
        not isinstance(provenance["confidence"], str) or provenance["confidence"] not in ("low", "medium", "high")):
        return result(RESULT_DENY, "invalid_provenance")
    known, permitted = trust.get("known_refs"), trust.get("permitted_routes")
    if (not isinstance(known, (list, tuple, set)) or
        not isinstance(permitted, (list, tuple, set))):
        return result(RESULT_DENY, "no_trusted_context")
    if any(not isinstance(ref, str) for ref in known):
        return result(RESULT_DENY, "invalid_trusted_knowledge")
    if not set(refs).issubset(set(known)):
        return result(RESULT_DENY, "unobserved_or_forbidden_refs")
    if f"{source}->{target}" not in permitted:
        return result(RESULT_DENY, "route_not_authorized")
    return result(RESULT_ACCEPT, "metadata_transfer_only")


if __name__ == "__main__":
    import sys
    failures = catalog_errors(json.loads(MATRIX.read_text(encoding="utf-8")))
    if failures:
        print("FAIL: " + "; ".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print("PASS F09: 16 familias y referencias verificadas; NO Core/UE5.")
