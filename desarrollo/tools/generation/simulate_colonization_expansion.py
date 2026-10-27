#!/usr/bin/env python3
"""Deterministic reference implementation for Block 2 colonization/expansion."""

from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

SIMULATOR_ID = "colonization_expansion_reference_simulator"
SIMULATOR_VERSION = "0.1.0"

def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(value)))

def stable_token(*parts: Any, length: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:length]

def evaluate_candidate(candidate: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    loc = candidate["location_id"]
    def reject(reason: str) -> dict[str, Any]:
        return {"location_id": loc, "eligible": False, "score": -999, "reason": reason, "warnings": []}
    if not candidate.get("known", False):
        return reject("unknown_target")
    if not candidate.get("reachable", False):
        return reject("unreachable_target")
    if candidate.get("hazard_prohibited", False):
        return reject("prohibited_hazard")
    if int(candidate.get("habitability", 0)) < int(policy.get("min_habitability", 35)):
        return reject("insufficient_habitability")
    inhabited = candidate.get("inhabited_state", "uninhabited")
    rights = candidate.get("settlement_rights", "none")
    if inhabited in {"sapient_pre_contact", "protected_prewarp"}:
        return reject("prime_directive_or_indigenous_protection")
    if inhabited in {"sapient_contacted", "inhabited_sovereign"} and rights not in {
        "treaty_grant", "invited_settlement", "joint_colony"
    }:
        return reject("no_settlement_rights")
    warnings: list[str] = []
    if candidate.get("existing_claimant_refs") and rights not in {"treaty_grant", "joint_colony"}:
        warnings.append("existing_claim_dispute_risk")
    score = (
        int(candidate.get("habitability", 0)) * 3
        + int(candidate.get("logistics_access", 0)) * 3
        + int(candidate.get("motive_fit", 0)) * 2
        + int(candidate.get("strategic_or_scientific_value", 0))
        - int(candidate.get("hazard_risk", 0)) * 2
        - int(candidate.get("distance_cost", 0)) * 2
        - (40 if warnings else 0)
    )
    return {"location_id": loc, "eligible": True, "score": score, "reason": "eligible", "warnings": warnings}

def select_target(candidates: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    evaluations = [evaluate_candidate(c, policy) for c in candidates]
    eligible = [e for e in evaluations if e["eligible"]]
    selected = sorted(eligible, key=lambda e: (-int(e["score"]), e["location_id"]))[0] if eligible else None
    return {"evaluations": evaluations, "selected_location_id": selected["location_id"] if selected else None}

def resolve_claim_overlap(claims: list[dict[str, Any]]) -> dict[str, Any]:
    active = [c for c in claims if c.get("active", True)]
    controllers = sorted({c.get("controller_ref") for c in active if c.get("effective_control") and c.get("controller_ref")})
    claimants = sorted({c["claimant_ref"] for c in active if c.get("claimant_ref")})
    if len(claimants) <= 1:
        return {"border_status": "undisputed", "claimant_refs": claimants, "controller_refs": controllers, "war_created": False}
    return {"border_status": "disputed_space", "claimant_refs": claimants, "controller_refs": controllers,
            "diplomatic_dispute_candidate": True, "war_created": False}

def stage_for(state: dict[str, Any]) -> str:
    if state.get("abandoned"):
        return "abandoned"
    pop, ss, infra = int(state["colony_population"]), int(state["self_sufficiency"]), int(state["infrastructure_maturity"])
    if pop < 5000:
        return "pioneer_outpost"
    if ss < 60:
        return "dependent_colony"
    if pop >= 20000 and ss >= 80 and infra >= 70:
        return "self_sustaining_colony"
    if pop >= 20000 and ss >= 60:
        return "established_colony"
    return "dependent_colony"

def simulate_project(*, campaign_seed: str, civilization_id: str, project_id: str, years: int,
                     initial: dict[str, Any], scheduled_events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if years < 0 or years > 250:
        raise ValueError("years must be between 0 and 250")
    state = copy.deepcopy(initial)
    founding = int(state["founding_population"])
    if founding <= 0 or founding > int(state["origin_population"]):
        raise ValueError("invalid founding population")
    state["origin_population"] = int(state["origin_population"]) - founding
    state["colony_population"] = founding
    state["migrants_transferred_total"] = founding
    state["natural_births_total"] = 0
    state["abandoned"] = False
    state["effective_control"] = True
    state.setdefault("claim_state", "settlement_presence")
    state.setdefault("autonomy_pressure", 0)
    state.setdefault("governance_status", "home_administered")
    state["stage"] = stage_for(state)

    events = sorted(scheduled_events or [], key=lambda e: (int(e["year"]), e.get("event_id", "")))
    by_year: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        year = int(event["year"])
        if year < 1 or year > years:
            raise ValueError(f"event year outside simulation window: {year}")
        by_year.setdefault(year, []).append(event)

    history: list[dict[str, Any]] = []
    snapshots: list[dict[str, Any]] = [{"year": 0, **copy.deepcopy(state)}]

    for year in range(1, years + 1):
        if not state["abandoned"]:
            migrants = min(int(state["annual_migrants"]), int(state["origin_population"]))
            state["origin_population"] -= migrants
            state["colony_population"] += migrants
            state["migrants_transferred_total"] += migrants
            births = (int(state["colony_population"]) * int(state["natural_growth_basis_points"])) // 10000
            state["colony_population"] += births
            state["natural_births_total"] += births
            required = math.ceil(int(state["colony_population"]) / 1000) * max(0, 100 - int(state["self_sufficiency"]))
            supplied = int(state["annual_support_capacity"])
            support_ratio = 100 if required <= 0 else min(100, (supplied * 100) // required)
            if support_ratio >= 100:
                state["self_sufficiency"] = clamp(int(state["self_sufficiency"]) + int(state["development_rate"]))
                state["infrastructure_maturity"] = clamp(int(state["infrastructure_maturity"]) + max(1, int(state["development_rate"]) // 2))
                state["governance_maturity"] = clamp(int(state["governance_maturity"]) + 1)
            elif support_ratio >= 60:
                state["self_sufficiency"] = clamp(int(state["self_sufficiency"]) + max(0, int(state["development_rate"]) // 2))
            else:
                state["self_sufficiency"] = clamp(int(state["self_sufficiency"]) - 5)
                state["infrastructure_maturity"] = clamp(int(state["infrastructure_maturity"]) - 3)

        for event in by_year.get(year, []):
            effects = event.get("effects", {})
            if "annual_support_capacity_set" in effects:
                state["annual_support_capacity"] = int(effects["annual_support_capacity_set"])
            if "annual_migrants_set" in effects:
                state["annual_migrants"] = int(effects["annual_migrants_set"])
            if "autonomy_pressure_delta" in effects:
                state["autonomy_pressure"] = clamp(int(state["autonomy_pressure"]) + int(effects["autonomy_pressure_delta"]))
            recorded = False
            if effects.get("declare_claim"):
                state["claim_state"] = "declared_claim"
                history.append({"event_id": event["event_id"], "year": year, "type": "claim_declared",
                                "cause_refs": event.get("cause_refs", []), "claim_scope": state["target_location_id"]})
                recorded = True
            if effects.get("evacuate_all"):
                evacuated = int(state["colony_population"])
                state["origin_population"] += evacuated
                state["colony_population"] = 0
                state["abandoned"] = True
                state["effective_control"] = False
                history.append({"event_id": event["event_id"], "year": year, "type": "colony_abandoned",
                                "cause_refs": event.get("cause_refs", []), "evacuated_population": evacuated})
                recorded = True
            if effects.get("independence_recognized"):
                state["governance_status"] = "independent_polity"
                state["effective_controller_ref"] = effects.get("new_polity_ref", f"gen:polity:{stable_token(project_id, year)}")
                history.append({"event_id": event["event_id"], "year": year, "type": "independence_recognized",
                                "cause_refs": event.get("cause_refs", []), "civilization_id_preserved": True})
                recorded = True
            if not recorded:
                history.append({"event_id": event["event_id"], "year": year, "type": event.get("event_type", "state_change"),
                                "cause_refs": event.get("cause_refs", []), "effects": copy.deepcopy(effects)})

        state["autonomy_candidate"] = (
            int(state["autonomy_pressure"]) >= 80
            and int(state["governance_maturity"]) >= 70
            and not state["abandoned"]
        )
        state["stage"] = stage_for(state)
        snapshots.append({"year": year, **copy.deepcopy(state)})

    return {"schema_version": "0.1.0",
            "simulator": {"simulator_id": SIMULATOR_ID, "simulator_version": SIMULATOR_VERSION},
            "campaign_seed": campaign_seed, "civilization_id": civilization_id, "project_id": project_id,
            "years_simulated": years, "final_state": state, "history": history, "snapshots": snapshots,
            "runtime_boundary": "Reference only; CoreRPG owns authoritative scheduling, persistence and World State mutation."}

def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    snapshots = payload.get("snapshots", [])
    if not snapshots:
        return ["missing snapshots"]
    for row in snapshots:
        if int(row.get("origin_population", 0)) < 0 or int(row.get("colony_population", 0)) < 0:
            errors.append("negative population")
        if row.get("claim_state") == "declared_claim" and not row.get("target_location_id"):
            errors.append("claim without location scope")
        if row.get("abandoned") and row.get("effective_control"):
            errors.append("abandoned colony cannot retain effective control without separate presence")
    for event in payload.get("history", []):
        if event.get("type") in {"claim_declared", "colony_abandoned", "independence_recognized"} and not event.get("cause_refs"):
            errors.append(f"major event missing cause_refs: {event.get('event_id')}")
    return sorted(set(errors))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    request = json.loads(args.input.read_text(encoding="utf-8"))
    if request.get("mode") == "select_target":
        payload, errors = select_target(request["candidates"], request.get("policy", {})), []
    else:
        payload = simulate_project(**request["input"] if "input" in request else request)
        errors = validate(payload)
    if args.validate and errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
