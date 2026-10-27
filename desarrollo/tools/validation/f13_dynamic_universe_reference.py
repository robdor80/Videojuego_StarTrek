#!/usr/bin/env python3
"""F13: referencia offline de universo dinámico. NO es CoreRPG y no escribe World State."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

BLOCKED = "BLOCKED"
REVIEW = "REVIEW_REQUIRED"
NO_MISSION = "NO_MISSION"
AUTHORITY = "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION"
BLOCK_ORDER = tuple(range(1, 11))
VALID_BLOCK_STATES = {"COMPLETE", "READY_TO_RESUME", "IN_PROGRESS", "TODO", "REFERENCE_COMPLETE"}
VALID_WARP = {"prewarp", "warp_capable", "postwarp"}
VALID_ROUTE = {"open", "restricted", "blocked"}
VALID_SEVERITY = {"low", "medium", "high", "critical"}
VALID_EVENT_TYPES = {
    "production", "consumption", "trade", "disruption_start", "disruption_end",
    "conflict_supply_loss", "discovery", "contact_state", "need_open", "need_closed",
}


def outcome(status, *reasons, **details):
    return {"status": status, "reasons": sorted(set(reasons)), "authority": AUTHORITY, **details}


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def ids(value, nonempty=True):
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(nonblank(v) for v in value)
        and len(value) == len(set(value))
    )


def positive_number(value):
    return type(value) in (int, float) and value > 0


def nonnegative_number(value):
    return type(value) in (int, float) and value >= 0


def valid_tick(value):
    return type(value) is int and 0 <= value <= 10_000_000


def audit_layers(summary):
    """P01: comprueba la foto 001-120 sin reinterpretar contratos como runtime."""
    if not isinstance(summary, dict):
        return outcome(BLOCKED, "invalid_layer_summary")
    if summary.get("complete_range") != [1, 118]:
        return outcome(BLOCKED, "layers_001_118_not_declared_complete")
    if summary.get("layer_119") != "PARTIAL":
        return outcome(BLOCKED, "layer_119_must_remain_partial")
    if summary.get("layer_120") != "BLOCKED_RUNTIME":
        return outcome(BLOCKED, "layer_120_must_remain_runtime_blocked")
    refs = summary.get("source_refs")
    if not ids(refs) or "proyecto/docs/roadmap/procedural_layers_master_plan_v0.1.md" not in refs:
        return outcome(BLOCKED, "missing_source_provenance")
    return outcome(
        REVIEW,
        "design_contract_status_only",
        complete_layers=118,
        partial_layers=[119],
        runtime_blocked_layers=[120],
    )


def gate_dynamic_blocks(states, requested_block):
    """P02: impide saltar del bloque 4 a 5-10 mientras 4 no esté cerrado."""
    if not isinstance(states, dict) or type(requested_block) is not int or requested_block not in BLOCK_ORDER:
        return outcome(BLOCKED, "invalid_block_request")
    normalized = {}
    for block in BLOCK_ORDER:
        raw = states.get(str(block), states.get(block))
        if raw not in VALID_BLOCK_STATES:
            return outcome(BLOCKED, "invalid_block_state")
        normalized[block] = raw
    if any(normalized[b] not in {"COMPLETE", "REFERENCE_COMPLETE"} for b in (1, 2, 3)):
        return outcome(BLOCKED, "blocks_1_3_reference_baseline_missing")
    first_open = next((b for b in range(4, 11) if normalized[b] not in {"COMPLETE", "REFERENCE_COMPLETE"}), None)
    if first_open is None:
        return outcome(REVIEW, "all_dynamic_blocks_reference_closed", requested_block=requested_block)
    if requested_block != first_open:
        return outcome(BLOCKED, "out_of_order_dynamic_block", expected_block=first_open)
    if requested_block == 4 and normalized[4] not in {"READY_TO_RESUME", "IN_PROGRESS"}:
        return outcome(BLOCKED, "block_4_not_ready")
    return outcome(REVIEW, "block_order_respected", active_reference_block=first_open)


def audit_repository(root=None):
    """Contrasta F13 con las fuentes canónicas del roadmap, no con una copia del fixture."""
    base = Path(__file__).resolve().parents[3] if root is None else Path(root)
    status_path = base / "proyecto/docs/roadmap/procedural_layers_status_v0.1.json"
    master_path = base / "proyecto/docs/roadmap/procedural_layers_master_plan_v0.1.md"
    blocks_path = base / "proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md"
    if not all(p.is_file() for p in (status_path, master_path, blocks_path)):
        return outcome(BLOCKED, "canonical_roadmap_sources_missing")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    summary = status.get("summary")
    expected_summary = {"total_layers": 120, "complete": 118, "partial": 1, "blocked_runtime": 1, "other": 0}
    if summary != expected_summary:
        return outcome(BLOCKED, "canonical_layer_summary_changed_review_required")
    layers = status.get("layers")
    if not isinstance(layers, list) or len(layers) != 120:
        return outcome(BLOCKED, "canonical_layer_inventory_invalid")
    expected_ids = [f"{i:03d}" for i in range(1, 121)]
    if [item.get("layer_id") for item in layers if isinstance(item, dict)] != expected_ids:
        return outcome(BLOCKED, "canonical_layer_ids_invalid")
    if any(layers[i]["status"] != "COMPLETE" for i in range(118)):
        return outcome(BLOCKED, "canonical_layers_001_118_changed_review_required")
    if layers[118].get("status") != "PARTIAL" or layers[119].get("status") != "BLOCKED_RUNTIME":
        return outcome(BLOCKED, "canonical_runtime_frontier_changed_review_required")
    if status.get("plan_ref") != "proyecto/docs/roadmap/procedural_layers_master_plan_v0.1.md":
        return outcome(BLOCKED, "canonical_plan_reference_mismatch")
    block_text = blocks_path.read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*(\d+)\s*\|[^|]+\|\s*([A-Z_]+)\s*\|\s*$", block_text, re.MULTILINE)
    states = {int(number): state for number, state in rows if 1 <= int(number) <= 10}
    if set(states) != set(BLOCK_ORDER):
        return outcome(BLOCKED, "dynamic_block_plan_unparseable")
    gate = gate_dynamic_blocks(states, 4)
    if gate["status"] != REVIEW or gate.get("active_reference_block") != 4:
        return outcome(BLOCKED, "dynamic_block_frontier_changed_review_required")
    return outcome(
        REVIEW,
        "canonical_roadmap_sources_consistent",
        complete_layers=118,
        partial_layers=[119],
        runtime_blocked_layers=[120],
        active_reference_block=4,
    )


def validate_world(world):
    if not isinstance(world, dict):
        raise ValueError("invalid_world")
    required_maps = (
        "systems", "planets", "civilizations", "stations", "routes", "traffic",
        "inventories", "ships", "needs", "diplomacy", "contacts",
    )
    for key in required_maps:
        if not isinstance(world.get(key), dict):
            raise ValueError("missing_" + key)
    for sid, system in world["systems"].items():
        if not nonblank(sid) or not isinstance(system, dict) or system.get("system_id") != sid:
            raise ValueError("invalid_system")
    for pid, planet in world["planets"].items():
        if not isinstance(planet, dict) or planet.get("planet_id") != pid or planet.get("system_id") not in world["systems"]:
            raise ValueError("invalid_planet")
    for cid, civ in world["civilizations"].items():
        if not isinstance(civ, dict) or civ.get("civilization_id") != cid:
            raise ValueError("invalid_civilization")
        if civ.get("home_planet_id") not in world["planets"] or civ.get("warp_state") not in VALID_WARP:
            raise ValueError("invalid_civilization_context")
    for stid, station in world["stations"].items():
        if not isinstance(station, dict) or station.get("station_id") != stid or station.get("system_id") not in world["systems"]:
            raise ValueError("invalid_station")
    known_endpoints = set(world["systems"]) | set(world["stations"]) | set(world["planets"])
    for rid, route in world["routes"].items():
        if not isinstance(route, dict) or route.get("route_id") != rid or route.get("status") not in VALID_ROUTE:
            raise ValueError("invalid_route")
        if not nonblank(route.get("origin_ref")) or not nonblank(route.get("destination_ref")):
            raise ValueError("invalid_route_endpoint")
        if route["origin_ref"] not in known_endpoints or route["destination_ref"] not in known_endpoints:
            raise ValueError("unknown_route_endpoint")
    for iid, inv in world["inventories"].items():
        if not isinstance(inv, dict) or inv.get("inventory_id") != iid or not nonblank(inv.get("owner_ref")):
            raise ValueError("invalid_inventory")
        stocks = inv.get("stocks")
        if not isinstance(stocks, dict) or any(not nonblank(k) or not nonnegative_number(v) for k, v in stocks.items()):
            raise ValueError("invalid_stock")
    for tid, traffic in world["traffic"].items():
        if not isinstance(traffic, dict) or traffic.get("traffic_id") != tid:
            raise ValueError("invalid_traffic")
        if traffic.get("route_ref") not in world["routes"] or not nonblank(traffic.get("purpose")) or not nonblank(traffic.get("cause_ref")):
            raise ValueError("uncausal_traffic")
    for ship_id, ship in world["ships"].items():
        if not isinstance(ship, dict) or ship.get("ship_id") != ship_id or not ids(ship.get("capabilities", []), False):
            raise ValueError("invalid_ship")
    for nid, need in world["needs"].items():
        if not isinstance(need, dict) or need.get("need_id") != nid or not nonblank(need.get("cause_ref")):
            raise ValueError("invalid_need")
        if need.get("status") not in {"open", "resolved"} or not ids(need.get("required_capabilities", []), False):
            raise ValueError("invalid_need_state")
    return True


def screen_economic_transfer(world, tx):
    """P03/Bloque 4: transferencia candidata, sin cambiar inventarios."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if not isinstance(tx, dict):
        return outcome(BLOCKED, "invalid_trade")
    required = (
        "trade_id", "buyer_inventory_ref", "seller_inventory_ref", "resource",
        "route_ref", "source_need_ref", "operator_ref",
    )
    if any(not nonblank(tx.get(k)) for k in required) or not positive_number(tx.get("quantity")):
        return outcome(BLOCKED, "invalid_trade")
    buyer = world["inventories"].get(tx["buyer_inventory_ref"])
    seller = world["inventories"].get(tx["seller_inventory_ref"])
    if not buyer or not seller or buyer is seller:
        return outcome(BLOCKED, "invalid_trade_parties")
    route = world["routes"].get(tx["route_ref"])
    if not route:
        return outcome(BLOCKED, "unknown_route")
    if route["status"] == "blocked":
        return outcome(BLOCKED, "route_blocked")
    need = world["needs"].get(tx["source_need_ref"])
    if not need or need["status"] != "open":
        return outcome(BLOCKED, "missing_live_demand")
    qty = tx["quantity"]
    available = seller["stocks"].get(tx["resource"], 0)
    if available < qty:
        return outcome(BLOCKED, "insufficient_stock")
    return outcome(
        REVIEW,
        "requires_core_inventory_and_contract_authorization",
        trade_id=tx["trade_id"],
        transferable_quantity=qty,
        route_status=route["status"],
    )


def project_disruption(world, crisis):
    """P03/P05: calcula efectos candidatos de una disrupción causal."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if (
        not isinstance(crisis, dict)
        or not nonblank(crisis.get("crisis_id"))
        or crisis.get("severity") not in VALID_SEVERITY
        or not ids(crisis.get("cause_event_refs"))
        or not ids(crisis.get("affected_route_refs"))
    ):
        return outcome(BLOCKED, "invalid_crisis")
    unknown = [r for r in crisis["affected_route_refs"] if r not in world["routes"]]
    if unknown:
        return outcome(BLOCKED, "unknown_affected_route")
    affected = sorted(
        tid for tid, traffic in world["traffic"].items()
        if traffic["route_ref"] in crisis["affected_route_refs"]
    )
    needs = sorted(
        nid for nid, need in world["needs"].items()
        if need["status"] == "open" and need.get("route_ref") in crisis["affected_route_refs"]
    )
    return outcome(
        REVIEW,
        "network_effects_are_candidates_until_core_applies_event",
        affected_traffic=affected,
        exposed_needs=needs,
    )


def assess_contact(world, req):
    """P04: lectura conservadora de contacto/Primera Directriz."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if not isinstance(req, dict) or not nonblank(req.get("civilization_ref")) or not nonblank(req.get("requested_scope")):
        return outcome(BLOCKED, "invalid_contact_request")
    civ = world["civilizations"].get(req["civilization_ref"])
    if not civ:
        return outcome(BLOCKED, "unknown_civilization")
    if not nonblank(req.get("mission_authority_ref")):
        return outcome(BLOCKED, "missing_mission_authority")
    scope = req["requested_scope"]
    if scope not in {"observe", "limited_contact", "formal_contact"}:
        return outcome(BLOCKED, "invalid_contact_scope")
    if civ["warp_state"] == "prewarp":
        exposure = bool(civ.get("public_alien_awareness")) or bool(req.get("mutual_exposure"))
        if scope == "observe":
            return outcome(REVIEW, "observe_only_prime_directive_context", recommended_scope="observe")
        if not exposure:
            return outcome(
                REVIEW,
                "prime_directive_noninterference_warning",
                recommended_scope="observe",
                captain_decision_required=True,
            )
        return outcome(
            REVIEW,
            "contamination_or_mutual_exposure_requires_mitigation_review",
            recommended_scope="limited_contact",
            captain_decision_required=True,
        )
    return outcome(
        REVIEW,
        "warp_threshold_is_candidate_not_mandatory_contact",
        recommended_scope="formal_contact_candidate",
        captain_decision_required=True,
    )


def derive_mission_candidate(world, need_ref, candidate_ship_ref):
    """P04/Bloque 9 boundary: misión solo desde necesidad ya existente."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if not nonblank(need_ref) or not nonblank(candidate_ship_ref):
        return outcome(BLOCKED, "invalid_mission_request")
    need = world["needs"].get(need_ref)
    if not need or need["status"] != "open":
        return outcome(NO_MISSION, "no_live_world_state_need")
    ship = world["ships"].get(candidate_ship_ref)
    if not ship:
        return outcome(NO_MISSION, "unknown_candidate_unit")
    missing = sorted(set(need["required_capabilities"]) - set(ship["capabilities"]))
    if missing:
        return outcome(NO_MISSION, "unit_lacks_capability", missing_capabilities=missing)
    if need.get("legal_access_required") and not need.get("legal_access_ref"):
        return outcome(NO_MISSION, "legal_access_unresolved")
    return outcome(
        REVIEW,
        "authority_must_task_candidate_unit",
        mission_source_need=need_ref,
        candidate_ship=candidate_ship_ref,
        cause_ref=need["cause_ref"],
    )


def replay_reference(world, events, days):
    """P05: replay determinista de ledger/eventos. No genera historia ni hace save Core."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if type(days) is not int or not 1 <= days <= 3650 or not isinstance(events, list):
        return outcome(BLOCKED, "invalid_horizon")
    state = copy.deepcopy(world)
    seen, audit = set(), []
    last_tick = -1

    def inventory(ref):
        inv = state["inventories"].get(ref)
        if inv is None:
            raise ValueError("unknown_inventory")
        return inv

    for evt in events:
        if not isinstance(evt, dict) or not nonblank(evt.get("event_id")):
            return outcome(BLOCKED, "invalid_stream_event")
        eid = evt["event_id"]
        tick = evt.get("tick")
        kind = evt.get("event_type")
        if (
            eid in seen
            or not valid_tick(tick)
            or tick < last_tick
            or tick >= days * 24
            or kind not in VALID_EVENT_TYPES
        ):
            return outcome(BLOCKED, "duplicate_disordered_or_invalid_event")
        if not ids(evt.get("cause_refs")):
            return outcome(BLOCKED, "event_without_cause")
        seen.add(eid)
        last_tick = tick
        try:
            if kind in {"production", "consumption", "conflict_supply_loss"}:
                inv = inventory(evt.get("inventory_ref"))
                resource = evt.get("resource")
                amount = evt.get("amount")
                if not nonblank(resource) or not positive_number(amount):
                    raise ValueError("invalid_resource_delta")
                current = inv["stocks"].get(resource, 0)
                delta = amount if kind == "production" else -amount
                if current + delta < 0:
                    raise ValueError("negative_stock")
                inv["stocks"][resource] = current + delta
            elif kind == "trade":
                tx = evt.get("trade")
                checked = screen_economic_transfer(state, tx)
                if checked["status"] != REVIEW:
                    raise ValueError("invalid_trade_event")
                qty, resource = tx["quantity"], tx["resource"]
                seller = inventory(tx["seller_inventory_ref"])
                buyer = inventory(tx["buyer_inventory_ref"])
                seller["stocks"][resource] = seller["stocks"].get(resource, 0) - qty
                buyer["stocks"][resource] = buyer["stocks"].get(resource, 0) + qty
            elif kind == "disruption_start":
                for route_ref in evt.get("route_refs", []):
                    if route_ref not in state["routes"]:
                        raise ValueError("unknown_route")
                    state["routes"][route_ref]["status"] = "blocked"
            elif kind == "disruption_end":
                for route_ref in evt.get("route_refs", []):
                    if route_ref not in state["routes"]:
                        raise ValueError("unknown_route")
                    state["routes"][route_ref]["status"] = "open"
            elif kind == "discovery":
                if not nonblank(evt.get("subject_ref")) or not nonblank(evt.get("observer_ref")):
                    raise ValueError("invalid_discovery")
                state.setdefault("knowledge_events", []).append(
                    {"event_id": eid, "observer_ref": evt["observer_ref"], "subject_ref": evt["subject_ref"]}
                )
            elif kind == "contact_state":
                civ_ref = evt.get("civilization_ref")
                if civ_ref not in state["civilizations"] or not nonblank(evt.get("contact_state")):
                    raise ValueError("invalid_contact_event")
                state["contacts"][civ_ref] = evt["contact_state"]
            elif kind == "need_open":
                need = evt.get("need")
                if not isinstance(need, dict) or not nonblank(need.get("need_id")) or not nonblank(need.get("cause_ref")):
                    raise ValueError("invalid_need_event")
                if need["need_id"] in state["needs"]:
                    raise ValueError("duplicate_need")
                if not ids(need.get("required_capabilities", []), False):
                    raise ValueError("invalid_need_capabilities")
                state["needs"][need["need_id"]] = {**need, "status": "open"}
            elif kind == "need_closed":
                ref = evt.get("need_ref")
                if ref not in state["needs"] or state["needs"][ref]["status"] != "open":
                    raise ValueError("invalid_need_close")
                state["needs"][ref]["status"] = "resolved"
        except (ValueError, TypeError, KeyError):
            return outcome(BLOCKED, "event_breaks_world_coherence", event_id=eid)
        audit.append({"event_id": eid, "event_type": kind, "tick": tick})

    candidates = []
    for need_id, need in sorted(state["needs"].items()):
        if need["status"] != "open":
            continue
        for ship_id in sorted(state["ships"]):
            candidate = derive_mission_candidate(state, need_id, ship_id)
            if candidate["status"] == REVIEW:
                candidates.append({"need_ref": need_id, "ship_ref": ship_id, "cause_ref": need["cause_ref"]})
                break

    compact = {
        "inventories": state["inventories"],
        "routes": state["routes"],
        "contacts": state["contacts"],
        "needs": state["needs"],
        "knowledge_events": state.get("knowledge_events", []),
        "audit": audit,
        "mission_candidates": candidates,
    }
    digest = hashlib.sha256(
        json.dumps(compact, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return outcome(
        REVIEW,
        "not_core_save_or_authoritative_galactic_simulation",
        elapsed_days=days,
        processed_events=len(audit),
        mission_candidates=candidates,
        final_inventories={k: v["stocks"] for k, v in sorted(state["inventories"].items())},
        final_routes={k: v["status"] for k, v in sorted(state["routes"].items())},
        sha256=digest,
    )


def run_scenarios(path):
    fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    world = fixture["world"]
    failures, results = [], []
    for case in fixture["cases"]:
        op, data = case["operation"], case.get("input", {})
        if op == "layers":
            got = audit_layers(data)
        elif op == "block_gate":
            got = gate_dynamic_blocks(data["states"], data["requested_block"])
        elif op == "economy":
            got = screen_economic_transfer(world, data)
        elif op == "disruption":
            got = project_disruption(world, data)
        elif op == "contact":
            got = assess_contact(world, data)
        elif op == "mission":
            got = derive_mission_candidate(world, data["need_ref"], data["ship_ref"])
        elif op == "replay":
            got = replay_reference(world, data["events"], data["days"])
        else:
            raise ValueError("unknown_operation")
        ok = got["status"] == case["expected_status"]
        if "expected_reason" in case:
            ok = ok and case["expected_reason"] in got.get("reasons", [])
        results.append({"id": case["id"], "ok": ok, "actual": got["status"]})
        if not ok:
            failures.append(case["id"])
    report = {
        "scope": AUTHORITY,
        "scenario_count": len(results),
        "passed": sum(x["ok"] for x in results),
        "failed_ids": failures,
        "results": results,
    }
    report["sha256"] = hashlib.sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = run_scenarios(args.scenario)
    report["repository_audit"] = audit_repository()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": report["scenario_count"], "passed": report["passed"], "sha256": report["sha256"]}))
    if report["repository_audit"]["status"] == BLOCKED:
        raise SystemExit("F13 canonical roadmap audit blocked: " + ", ".join(report["repository_audit"]["reasons"]))
    if report["failed_ids"]:
        raise SystemExit("F13 FAILED: " + ", ".join(report["failed_ids"]))
