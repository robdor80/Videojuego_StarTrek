#!/usr/bin/env python3
"""Deterministic reference simulator for long-horizon civilization evolution.

This is a Star Trek content/rules reference implementation. It deliberately
does not own runtime scheduling, save/load, generic events, or authoritative
World State; those belong to CoreRPG 4.5+.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

SIMULATOR_ID = "civilization_evolution_reference_simulator"
SIMULATOR_VERSION = "0.1.0"


def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(value)))


def stable_token(*parts: Any, length: int = 16) -> str:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:length]


def relation_state(relation: dict[str, Any]) -> str:
    if relation.get("war_declared"):
        return "war"
    if relation["tension"] >= 80:
        return "hostile"
    if relation["tension"] >= 60 or relation["trust"] <= 25:
        return "strained"
    if relation["trust"] >= 70 and relation["tension"] <= 25:
        return "friendly"
    return "normal_relations"


def _validate_initial(initial: dict[str, Any]) -> None:
    required = [
        "population", "population_capacity", "natural_growth_basis_points",
        "legitimacy", "institutional_capacity", "social_cohesion",
        "economic_resilience", "capability_maturity", "government_id",
        "governance_state", "technology_band", "external_relations",
    ]
    missing = [field for field in required if field not in initial]
    if missing:
        raise ValueError(f"missing initial fields: {missing}")
    if int(initial["population"]) < 0:
        raise ValueError("population cannot be negative")
    if int(initial["population_capacity"]) <= 0:
        raise ValueError("population_capacity must be positive")


def simulate(*, campaign_seed: str, civilization_id: str, years: int,
             initial: dict[str, Any],
             scheduled_events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if years < 0 or years > 250:
        raise ValueError("years must be between 0 and 250")
    _validate_initial(initial)

    state = copy.deepcopy(initial)
    events = sorted(scheduled_events or [],
                    key=lambda row: (int(row["year"]), row.get("event_id", "")))
    events_by_year: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        year = int(event["year"])
        if year < 1 or year > years:
            raise ValueError(f"event year outside simulation window: {year}")
        events_by_year.setdefault(year, []).append(event)

    history: list[dict[str, Any]] = []
    snapshots: list[dict[str, Any]] = [{"year": 0, **copy.deepcopy(state)}]

    for year in range(1, years + 1):
        capacity = max(1, int(state["population_capacity"]))
        pressure = max(0, (int(state["population"]) * 100 // capacity) - 85)
        growth_bp = int(state["natural_growth_basis_points"])
        growth_bp += (int(state["economic_resilience"]) - 50) // 10
        growth_bp += (int(state["social_cohesion"]) - 50) // 20
        growth_bp -= pressure // 3
        growth_bp = max(-250, min(250, growth_bp))
        before = int(state["population"])
        state["population"] = max(0, before + (before * growth_bp) // 10000)

        maturity_gain = max(0, (int(state["institutional_capacity"]) - 40) // 25)
        state["capability_maturity"] = clamp(
            int(state["capability_maturity"]) + maturity_gain
        )

        for event in events_by_year.get(year, []):
            event_id = event.get("event_id") or (
                "gen:evolution_event:" + stable_token(
                    campaign_seed, civilization_id, year,
                    json.dumps(event, sort_keys=True)
                )
            )
            effects = event.get("effects", {})

            for field in ("legitimacy", "institutional_capacity", "social_cohesion",
                          "economic_resilience", "capability_maturity"):
                key = f"{field}_delta"
                if key in effects:
                    state[field] = clamp(int(state[field]) + int(effects[key]))

            if "population_delta" in effects:
                state["population"] = max(
                    0, int(state["population"]) + int(effects["population_delta"])
                )
            if "population_loss_basis_points" in effects:
                loss = max(0, min(10000, int(effects["population_loss_basis_points"])))
                pop = int(state["population"])
                state["population"] = max(0, pop - (pop * loss) // 10000)
            if "population_capacity_delta" in effects:
                state["population_capacity"] = max(
                    1, int(state["population_capacity"])
                    + int(effects["population_capacity_delta"])
                )

            recorded = False

            if "government_transition" in effects:
                transition = effects["government_transition"]
                old = state["government_id"]
                state["government_id"] = transition.get("new_government_id") or (
                    "gen:government:" + stable_token(
                        campaign_seed, civilization_id, "government", year, event_id
                    )
                )
                state["governance_state"] = transition["new_governance_state"]
                history.append({
                    "event_id": event_id, "year": year,
                    "type": "government_transition",
                    "cause_refs": event.get("cause_refs", []),
                    "old_government_id": old,
                    "new_government_id": state["government_id"],
                    "civilization_id_preserved": True,
                })
                recorded = True

            if effects.get("fragmentation_trigger"):
                state["political_fragmentation_state"] = "fragmentation_candidate"
                history.append({
                    "event_id": event_id, "year": year,
                    "type": "fragmentation_candidate",
                    "cause_refs": event.get("cause_refs", []),
                    "rule": "does_not_auto_create_successor_civilizations",
                })
                recorded = True

            if effects.get("extinction_confirmed"):
                state["population"] = 0
                state["civilization_status"] = "extinct"
                history.append({
                    "event_id": event_id, "year": year,
                    "type": "civilization_extinction",
                    "cause_refs": event.get("cause_refs", []),
                })
                recorded = True

            target = effects.get("relation_target_ref")
            if target:
                relation = next(
                    (row for row in state["external_relations"]
                     if row["party_ref"] == target), None
                )
                if relation is None:
                    raise ValueError(f"event targets unknown relation: {target}")
                relation["trust"] = clamp(
                    int(relation["trust"]) + int(effects.get("trust_delta", 0))
                )
                relation["tension"] = clamp(
                    int(relation["tension"]) + int(effects.get("tension_delta", 0))
                )
                if effects.get("war_declared") is True:
                    relation["war_declared"] = True
                relation["relation_state"] = relation_state(relation)
                history.append({
                    "event_id": event_id, "year": year,
                    "type": "relation_change", "party_ref": target,
                    "cause_refs": event.get("cause_refs", []),
                    "scope": relation.get("scope", "party_only"),
                    "relation_state": relation["relation_state"],
                })
                recorded = True

            if not recorded:
                history.append({
                    "event_id": event_id, "year": year,
                    "type": event.get("event_type", "state_change"),
                    "cause_refs": event.get("cause_refs", []),
                    "effects": copy.deepcopy(effects),
                })

        state["technology_transition_candidate"] = (
            int(state["capability_maturity"]) >= 100
        )
        if (int(state["social_cohesion"]) <= 20
                and int(state["institutional_capacity"]) <= 25
                and state.get("political_fragmentation_state")
                != "fragmentation_candidate"):
            state["political_fragmentation_state"] = "high_risk"
        elif state.get("political_fragmentation_state") not in {
            "fragmentation_candidate", "high_risk"
        }:
            state["political_fragmentation_state"] = "contained"

        state.setdefault("civilization_status", "active")
        if int(state["population"]) == 0 and state["civilization_status"] != "extinct":
            state["civilization_status"] = "critical_zero_population_unresolved"

        snapshots.append({"year": year, **copy.deepcopy(state)})

    return {
        "schema_version": "0.1.0",
        "simulator": {
            "simulator_id": SIMULATOR_ID,
            "simulator_version": SIMULATOR_VERSION,
            "algorithm": "causal_year_step_v1",
        },
        "campaign_seed": campaign_seed,
        "civilization_id": civilization_id,
        "years_simulated": years,
        "final_state": state,
        "history": history,
        "snapshots": snapshots,
        "runtime_boundary": (
            "Reference simulator only; CoreRPG owns authoritative scheduling, "
            "persistence, generic events and World State mutation."
        ),
    }


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    snapshots = payload.get("snapshots", [])
    if not payload.get("civilization_id"):
        errors.append("missing civilization_id")
    if not snapshots:
        errors.append("missing snapshots")
        return errors
    if any(int(row.get("population", 0)) < 0 for row in snapshots):
        errors.append("negative population")

    fields = ["legitimacy", "institutional_capacity", "social_cohesion",
              "economic_resilience", "capability_maturity"]
    for row in snapshots:
        for field in fields:
            if not 0 <= int(row.get(field, 0)) <= 100:
                errors.append(f"{field} escaped 0..100")
        for relation in row.get("external_relations", []):
            if (relation.get("scope") == "partial_polity"
                    and relation.get("planetary_binding", False)):
                errors.append("partial polity relation cannot bind whole planet")

    for event in payload.get("history", []):
        if (event.get("type") in {
            "government_transition", "relation_change",
            "civilization_extinction", "fragmentation_candidate"
        } and not event.get("cause_refs")):
            errors.append(
                f"major event missing cause_refs: {event.get('event_id', 'unknown')}"
            )

    technology_band = snapshots[0].get("technology_band")
    if any(row.get("technology_band") != technology_band for row in snapshots[1:]):
        errors.append("technology band changed inside Block 1")
    return sorted(set(errors))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    request = json.loads(args.input.read_text(encoding="utf-8"))
    payload = simulate(**request)
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
