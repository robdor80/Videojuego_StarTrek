#!/usr/bin/env python3
"""Deterministic reference simulator for Procedural Conflict & War v0.1."""

from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

SIMULATOR_ID = "procedural_conflict_war_reference_simulator"
SIMULATOR_VERSION = "0.1.0"
ACTION_RANK = {
    "deescalate_or_negotiate": 0,
    "formal_pressure": 1,
    "covert_or_indirect_pressure_candidate": 2,
    "mobilize": 3,
    "limited_force_candidate": 4,
    "seek_war_authority": 5,
    "war_declaration_candidate": 6,
}

def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(value)))

def stable_fraction(*parts: Any) -> float:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    value = int(hashlib.sha256(payload).hexdigest()[:12], 16)
    return value / float(0xFFFFFFFFFFFF)

def validate_profile(profile: dict[str, Any]) -> None:
    forbidden = {"species_aggression", "species_war_bias", "species_hostility"}
    found = forbidden.intersection(profile)
    if found:
        raise ValueError(f"species-derived conflict bias forbidden: {sorted(found)}")
    required = {
        "force_acceptance", "diplomatic_patience", "prestige_sensitivity",
        "institutional_restraint", "casualty_aversion", "civilian_harm_constraint",
        "covert_or_indirect_preference"
    }
    missing = required.difference(profile)
    if missing:
        raise ValueError(f"missing doctrine fields: {sorted(missing)}")

def assess_response(profile: dict[str, Any], situation: dict[str, Any]) -> dict[str, Any]:
    validate_profile(profile)
    force_ratio = max(0, min(200, int(situation.get("relative_force_percent", 100))))
    readiness = clamp(situation.get("military_readiness", 50))
    logistics = clamp(situation.get("logistics_support", 50))
    exhaustion = clamp(situation.get("war_exhaustion", 0))
    expected_losses = clamp(situation.get("expected_loss_risk", 50))
    threat = clamp(situation.get("threat", 0))
    stakes = clamp(situation.get("stakes", 0))
    grievance = clamp(situation.get("grievance", 0))
    humiliation = clamp(situation.get("honor_or_reputation_challenge", 0))
    relation_tension = clamp(situation.get("relation_tension", 0))
    negotiation_open = clamp(situation.get("negotiation_opportunity", 50))
    pressure = (
        threat * 0.26 + stakes * 0.20 + grievance * 0.16 + relation_tension * 0.12
        + profile["force_acceptance"] * 0.15
        + profile["prestige_sensitivity"] * humiliation / 500.0
        + max(0, force_ratio - 100) * 0.08
        + max(0, readiness - 50) * 0.08
        + max(0, logistics - 50) * 0.05
        - profile["diplomatic_patience"] * negotiation_open / 650.0
        - profile["institutional_restraint"] * 0.07
        - profile["casualty_aversion"] * expected_losses / 650.0
        - exhaustion * 0.22
        - max(0, 100 - force_ratio) * 0.15
        - max(0, 50 - readiness) * 0.12
        - max(0, 50 - logistics) * 0.10
    )
    score = clamp(round(pressure))
    if score < 25:
        action = "deescalate_or_negotiate"
    elif score < 42:
        action = "formal_pressure"
    elif score < 58:
        action = "covert_or_indirect_pressure_candidate" if int(profile["covert_or_indirect_preference"]) >= 70 else "formal_pressure"
    elif score < 72:
        action = "mobilize"
    elif score < 86:
        action = "limited_force_candidate"
    else:
        has_cause = bool(situation.get("cause_refs"))
        has_objective = bool(situation.get("war_objective_refs"))
        action = "war_declaration_candidate" if has_cause and has_objective and situation.get("war_authority_granted", False) else "seek_war_authority"
    return {
        "escalation_score": score,
        "recommended_action": action,
        "action_rank": ACTION_RANK[action],
        "war_authority_granted": bool(situation.get("war_authority_granted", False)),
        "cause_refs": copy.deepcopy(situation.get("cause_refs", [])),
        "war_objective_refs": copy.deepcopy(situation.get("war_objective_refs", [])),
    }

def effective_force(force: dict[str, Any]) -> int:
    total = 0
    for unit in force.get("units", []):
        if unit.get("status") == "destroyed":
            continue
        total += max(0, int(unit["combat_power"])) * clamp(unit.get("readiness", 100)) * clamp(unit.get("logistics", 100)) // 10000
    return total

def resolve_operation(*, campaign_seed: str, operation_id: str, attacker: dict[str, Any],
                      defender: dict[str, Any], objective_ref: str, location_ref: str) -> dict[str, Any]:
    if not objective_ref or not location_ref:
        raise ValueError("operation requires objective and location")
    atk, dfn = copy.deepcopy(attacker), copy.deepcopy(defender)
    atk_power, def_power = effective_force(atk), effective_force(dfn)
    if atk_power <= 0 or def_power <= 0:
        raise ValueError("both sides require positive effective force")
    variance = 0.9 + stable_fraction(campaign_seed, operation_id, "variance") * 0.2
    ratio = (atk_power * variance) / def_power
    if ratio >= 1.35:
        outcome, atk_damage, def_damage = "attacker_advantage", 18, 42
    elif ratio <= 0.74:
        outcome, atk_damage, def_damage = "defender_advantage", 42, 18
    else:
        outcome, atk_damage, def_damage = "contested", 30, 30

    def apply_damage(force: dict[str, Any], damage_pct: int, side: str) -> list[dict[str, Any]]:
        effects = []
        for unit in sorted([u for u in force["units"] if u.get("status") != "destroyed"], key=lambda u: u["unit_id"]):
            local = max(0, min(100, damage_pct + round((stable_fraction(campaign_seed, operation_id, side, unit["unit_id"]) - 0.5) * 16)))
            prior = int(unit.get("integrity", 100))
            after = max(0, prior - local)
            unit["integrity"] = after
            if after == 0:
                unit["status"] = "destroyed"
            elif after < 45:
                unit["status"] = "heavily_damaged"
            elif after < 75:
                unit["status"] = "damaged"
            effects.append({"unit_id": unit["unit_id"], "integrity_before": prior, "integrity_after": after, "status": unit.get("status", "operational")})
        return effects

    atk_effects = apply_damage(atk, atk_damage, "attacker")
    def_effects = apply_damage(dfn, def_damage, "defender")
    return {
        "operation_id": operation_id, "objective_ref": objective_ref, "location_ref": location_ref,
        "outcome": outcome,
        "attacker_before_unit_ids": sorted(u["unit_id"] for u in attacker["units"]),
        "defender_before_unit_ids": sorted(u["unit_id"] for u in defender["units"]),
        "attacker_after": atk, "defender_after": dfn,
        "attacker_effects": atk_effects, "defender_effects": def_effects,
        "spawned_unit_ids": [], "sovereignty_changed": False,
        "control_change_candidate": outcome == "attacker_advantage",
    }

def apply_conflict_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    effects = event.get("effects", {})
    if effects.get("declare_war"):
        if not event.get("cause_refs") or not effects.get("war_objective_refs") or not effects.get("authority_ref"):
            raise ValueError("war declaration requires cause, objective and authority")
        next_state["conflict_state"] = "war"
        next_state["war_objective_refs"] = list(effects["war_objective_refs"])
    if effects.get("ceasefire"):
        next_state["conflict_state"] = "ceasefire"
    if effects.get("armistice"):
        next_state["conflict_state"] = "armistice"
    if effects.get("peace_settlement"):
        next_state["conflict_state"] = "peace"
    if "war_exhaustion_delta" in effects:
        next_state["war_exhaustion"] = clamp(int(next_state.get("war_exhaustion", 0)) + int(effects["war_exhaustion_delta"]))
    if effects.get("occupation_control_ref"):
        next_state["effective_control_ref"] = effects["occupation_control_ref"]
        next_state["occupation_state"] = "military_occupation"
    return next_state

def validate_operation(result: dict[str, Any]) -> list[str]:
    errors = []
    before_a = set(result["attacker_before_unit_ids"])
    after_a = {u["unit_id"] for u in result["attacker_after"]["units"]}
    before_d = set(result["defender_before_unit_ids"])
    after_d = {u["unit_id"] for u in result["defender_after"]["units"]}
    if before_a != after_a or before_d != after_d or result.get("spawned_unit_ids"):
        errors.append("strategic operation spawned or deleted force identities")
    if result.get("sovereignty_changed"):
        errors.append("operation cannot change sovereignty directly")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.input.read_text(encoding="utf-8"))
    if request["mode"] == "assess_response":
        result = assess_response(request["profile"], request["situation"])
    elif request["mode"] == "resolve_operation":
        result = resolve_operation(**request["input"])
        errors = validate_operation(result)
        if errors:
            raise SystemExit("; ".join(errors))
    else:
        raise ValueError(f"unknown mode: {request['mode']}")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
