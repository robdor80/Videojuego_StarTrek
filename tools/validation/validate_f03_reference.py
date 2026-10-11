#!/usr/bin/env python3
"""F03: validador de un fixture INERTE. NO es CoreRPG, generador ni save/load real."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "validation/fixtures/f03/continuity_reference_v0.1.json"
EVENTS = ROOT / "gameplay/ship_operations/operational_event_log/sensors_vertical_slice_example.json"
ACCEPTANCE = ROOT / "validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json"
RESULT_CONTRACT = ROOT / "gameplay/ship_operations/sensor_resolution/sensor_result_contract.json"
PERSISTENCE = ROOT / "gameplay/persistence/persistent_state_roundtrip_contract.json"

class ContractError(ValueError):
    """Un fixture de referencia incumple una invariante documentada."""

def ensure(ok: bool, message: str) -> None:
    if not ok:
        raise ContractError(message)

def timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError) as exc:
        raise ContractError("timestamp inválido: " + str(value)) from exc

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def contains_forbidden(value, keys: set[str]) -> bool:
    if isinstance(value, dict):
        return any(k in keys or contains_forbidden(v, keys) for k, v in value.items())
    if isinstance(value, list):
        return any(contains_forbidden(v, keys) for v in value)
    return False

def validate_reference(data: dict, events: dict | None = None) -> dict:
    """Invariantes de un escenario estructurado; no simula ni muta el World State."""
    ensure(data.get("schema_version") == "0.1.0", "versión de fixture incompatible")
    ensure(data.get("classification") == "INERT_CONTRACT_FIXTURE_NOT_CORE_RUNTIME", "falta clasificación")
    campaign = data["campaign"]
    ensure(campaign["era_id"] == "tng_ds9_voyager", "era no prevista para este fixture")
    ensure(campaign["campaign_date"] == campaign["timeline_start"][:10], "fecha incoherente")
    ensure(timestamp(campaign["timeline_start"]) <= timestamp(campaign["timeline_cursor"]), "cursor retrocede")
    ensure(bool(campaign["campaign_seed"]) and bool(campaign["generator_version"]), "semilla/versión obligatorias")

    entities = data["materialized_entities"]
    by_id = {e["entity_id"]: e for e in entities}
    ensure(len(by_id) == len(entities), "entidad duplicada")
    ensure(all(e["entity_id"] and e["origin_seed"] and e["creation_provenance"]
               and e["history_ref"] and timestamp(e["materialized_at"]) <= timestamp(campaign["timeline_cursor"])
               for e in entities), "identidad/materialización inválida")
    ensure(len({e["history_ref"] for e in entities}) == len(entities), "historial compartido en entidades distintas")
    pop = data["population"]
    slots = pop["slots"]
    ensure(len(slots) == pop["total_slots"], "aumento/pérdida de población")
    ensure(len({s["slot_id"] for s in slots}) == len(slots), "slot duplicado")
    chars = [s["character_id"] for s in slots if s["character_id"] is not None]
    ensure(len(set(chars)) == len(chars), "NPC duplicado")
    ensure(all((s["tier"] == "C") == (s["character_id"] is None) for s in slots), "promoción C-B inconsistente")

    projections = data["observer_projections"]
    private = data["projection_links_private"]
    visible_keys = set(data["roundtrip_expectations"]["forbidden_player_fields"])
    visible_keys.update(load_json(RESULT_CONTRACT)["forbidden_player_fields"])
    ensure(not contains_forbidden(projections, visible_keys), "filtración de verdad/identidad a proyección")
    projection_keys = [(p["observer_id"], p["contact_id"]) for p in projections]
    ensure(len(set(projection_keys)) == len(projection_keys), "contacto duplicado dentro de observador")
    link_keys = [(p["observer_id"], p["contact_id"]) for p in private]
    ensure(set(link_keys) == set(projection_keys), "asociación privada de contactos incompleta")
    ensure(all(l["entity_id"] in by_id for l in private), "observación de entidad inexistente")
    for p in projections:
        observed = p["observed"]
        resolution = p["resolution_state"]
        ensure(resolution in ("trace_detected", "detected_unclassified", "partially_resolved", "resolved"), "nivel inválido")
        ensure(0 <= p["confidence"] <= 1, "confianza inválida")
        ensure(timestamp(p["acquired_at"]) <= timestamp(campaign["timeline_cursor"]), "observación futura")
        target = by_id[next(l["entity_id"] for l in private if
            (l["observer_id"], l["contact_id"]) == (p["observer_id"], p["contact_id"]))]
        ensure(timestamp(target["materialized_at"]) <= timestamp(p["acquired_at"]), "observación antes de existir realidad")
        if resolution in ("trace_detected", "detected_unclassified"):
            ensure("entity_type" not in observed and "classification" not in observed and
                   "properties" not in observed, "revelación sin resolución")
        if resolution != "resolved":
            ensure("classification" not in observed, "clasificación precoz")
        if "resolved_hidden_properties" in observed:
            ensure(resolution == "resolved" and p.get("revealed_property_refs"), "ocultos sin evidencia")

    event_log = events if events is not None else load_json(EVENTS)
    evs = event_log["events"]
    event_ids = [e["event_id"] for e in evs]
    ensure(len(event_ids) == len(set(event_ids)), "evento duplicado")
    ensure(data["operational_state"]["event_ids"] == event_ids, "historia no coincide")
    earlier = set()
    last_time = timestamp(campaign["timeline_start"])
    for event in evs:
        when = timestamp(event["occurred_at"])
        ensure(last_time <= when <= timestamp(campaign["timeline_cursor"]), "evento fuera de orden")
        ensure(set(event.get("causal_refs", [])).issubset(earlier), "causa inexistente/futura")
        ensure(event.get("event_type") and event.get("visibility"), "evento sin tipo/visibilidad")
        earlier.add(event["event_id"])
        last_time = when

    ops = data["operational_state"]
    keys = [o["idempotency_key"] for o in ops["orders"]]
    ensure(len(keys) == len(set(keys)), "clave de idempotencia duplicada")
    for order in ops["orders"]:
        ensure(order["state"] in ("pending", "in_flight", "completed", "cancelled", "failed"), "estado de orden inválido")
        if order["state"] == "completed":
            ensure(order["result_id"] is not None and order["last_committed_event_id"] in earlier,
                   "orden completada sin evento/result")
        if order["state"] == "pending":
            ensure(order["result_id"] is None, "orden pendiente tiene resultado prematuro")

    assignments = ops["exclusive_assignments"]
    for i, a in enumerate(assignments):
        start, end = timestamp(a["start"]), timestamp(a["end"])
        ensure(start < end, "intervalo de agenda inválido")
        for b in assignments[i + 1:]:
            if a["character_id"] == b["character_id"]:
                ensure(end <= timestamp(b["start"]) or timestamp(b["end"]) <= start,
                       "ocupación simultánea incompatible")
    known_contacts = {(p["observer_id"], p["contact_id"]) for p in projections}
    for knowledge in ops["knowledge_state"]:
        ensure(all((knowledge["observer_id"], ref) in known_contacts
                   for ref in knowledge["contact_refs"]), "conocimiento de contacto ajeno")
        ensure(set(knowledge["source_event_refs"]).issubset(earlier), "memoria de evento no registrado")
    return {"entities": len(entities), "contacts": len(projections), "events": len(evs),
            "orders": len(ops["orders"]), "slots": len(slots)}

def validate_sources() -> dict:
    """Comprueba que las fuentes reales siguen existiendo y tienen requisitos acordados."""
    mandatory = [
        "universe/generation/persistent_entity_identity_contract.json",
        "universe/generation/persistent_population_materialization_rules.json",
        "universe/generation/civilization_latent_observed_materialized_pipeline_v0.1.json",
        "universe/chronology/temporal_anchors/temporal_anchors.json",
        "gameplay/ship_operations/operational_event_log/visibility_projection_rules.json",
        "universe/generation/ship_facility_offscreen_simulation_contract.json",
        "gameplay/persistence/persistent_state_roundtrip_contract.json",
        "docs/decisions/universal_stardate_system.md",
    ]
    for p in mandatory:
        ensure((ROOT / p).is_file(), "fuente original ausente: " + p)
    acceptance = load_json(ACCEPTANCE)
    ids = [row["id"] for row in acceptance["must_pass"]]
    ensure(len(ids) == 13 and len(set(ids)) == 13, "fixture sensores no conserva 13 invariantes")
    persistence = load_json(PERSISTENCE)
    ensure("same_entity_id" in persistence["roundtrip_invariants"],
           "persistencia ya no garantiza identidad")
    result = load_json(RESULT_CONTRACT)
    ensure({"ground_truth", "authoritative_entity_id"}.issubset(set(result["forbidden_player_fields"])),
           "contrato de sensores deja filtrar verdad")
    return {"sources_checked": len(mandatory), "sensor_invariants": len(ids)}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    args = parser.parse_args()
    result = validate_reference(load_json(args.fixture))
    result.update(validate_sources())
    print("F03 reference fixture: PASS (STATIC ONLY, NOT CORE/UE5) " + json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
