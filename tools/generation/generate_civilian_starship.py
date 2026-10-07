#!/usr/bin/env python3
"""Deterministic reference generator for procedural civilian starship designs and vessels.

This is a content/rules reference implementation. It demonstrates the crucial
DESIGN != INDIVIDUAL SHIP split. CoreRPG remains the future authoritative
runtime owner of persistent World State.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DESIGN_PROFILES = ROOT / "universe/generation/procedural_civilian_ship_design_profiles_v0.1.json"
LIFE_PROFILES = ROOT / "lore/starships/classes/shipboard_life/CIVILIAN_PROCEDURAL_SHIPBOARD_LIFE_PROFILES_v0.1.json"
STAFFING_GUIDANCE = ROOT / "universe/generation/ship_staffing_generation_guidance_v0.1.json"

GENERATOR_ID = "procedural_civilian_starship_reference_generator"
GENERATOR_VERSION = "0.1.0"


class DeterministicRng:
    def __init__(self, seed_material: str) -> None:
        self.seed_material = seed_material
        self.counter = 0

    def _u256(self) -> int:
        payload = f"{self.seed_material}|{self.counter}".encode("utf-8")
        self.counter += 1
        return int.from_bytes(hashlib.sha256(payload).digest(), "big")

    def randint(self, low: int, high: int) -> int:
        return low + self._u256() % (high - low + 1)

    def weighted_choice(self, entries: list[tuple[str, int]]) -> str:
        total = sum(weight for _, weight in entries)
        pick = self._u256() % total
        cursor = 0
        for value, weight in entries:
            cursor += weight
            if pick < cursor:
                return value
        return entries[-1][0]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def stable_token(*parts: str, length: int = 16) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:length]


def life_profiles_by_selector() -> dict[str, dict[str, Any]]:
    payload = load_json(LIFE_PROFILES)
    return {
        row["selector"]: row
        for row in payload.get("profiles", {}).values()
    }


def generic_watch_allocation(total: int, small: bool) -> dict[str, Any]:
    if small:
        if total <= 5:
            active = max(1, total // 2)
            secondary = max(0, total - active - 1)
            rest = total - active - secondary
            groups = {
                "active_control": active,
                "secondary_or_maintenance": secondary,
                "rest_or_relief": rest,
            }
        else:
            a = max(2, round(total * 0.40))
            b = max(2, round(total * 0.35))
            flex = total - a - b
            if flex < 1:
                b -= 1
                flex = 1
            groups = {"watch_group_a": a, "watch_group_b": b, "flex_or_relief": flex}
        return {
            "pattern": "custom_staggered_small_crew",
            "shipboard_cycle_hours": 24,
            "schedule_provenance": "GAME_ADDITION",
            "staggered_groups": groups,
            "allocation_total": sum(groups.values()),
        }

    fractions = {
        "watch_1": 0.34,
        "watch_2": 0.31,
        "watch_3": 0.30,
        "relief_or_float": 0.05,
    }
    raw = {key: total * value for key, value in fractions.items()}
    allocation = {key: int(value) for key, value in raw.items()}
    remaining = total - sum(allocation.values())
    order = sorted(
        allocation,
        key=lambda key: (raw[key] - allocation[key], key),
        reverse=True,
    )
    for key in order[:remaining]:
        allocation[key] += 1

    return {
        "pattern": "custom_three_watch_equivalent",
        "shipboard_cycle_hours": 24,
        "schedule_provenance": "GAME_ADDITION_NOT_CANON_LABELS",
        "definitions": [
            {"watch_id": "watch_1", "nominal_duration_hours": 8, "assigned_primary_personnel": allocation["watch_1"]},
            {"watch_id": "watch_2", "nominal_duration_hours": 8, "assigned_primary_personnel": allocation["watch_2"]},
            {"watch_id": "watch_3", "nominal_duration_hours": 8, "assigned_primary_personnel": allocation["watch_3"]},
        ],
        "relief_or_float": allocation["relief_or_float"],
        "allocation_total": sum(allocation.values()),
    }


def passenger_capacity(rng: DeterministicRng, role: str, size: str) -> tuple[int, int]:
    scale = {
        "micro": (0, 2),
        "small": (0, 12),
        "light": (0, 30),
        "medium": (0, 120),
        "large": (0, 500),
        "heavy": (0, 1800),
    }[size]
    low, high = scale
    if role == "passenger_liner":
        low = max(8, high // 4)
    elif role == "colony_transport":
        low = max(20, high // 3)
    elif role in {"personnel_transport", "medical"}:
        low = max(2, high // 6)
    else:
        high = min(high, max(0, high // 8))
    if high < low:
        high = low
    passengers = rng.randint(low, high) if high > 0 else 0
    civilians = 0
    return civilians, passengers


def generate(
    *,
    campaign_seed: str,
    need_id: str,
    era_id: str,
    campaign_date: str,
    role: str,
    operator_context: str = "independent_civilian",
) -> dict[str, Any]:
    profiles = load_json(DESIGN_PROFILES)
    role_profiles = profiles["role_profiles"]
    if role not in role_profiles:
        raise ValueError(f"Unsupported civilian role: {role}")
    if role == "criminal_or_smuggling_when_context_valid":
        raise ValueError("Smuggling role requires an explicit validated illegal-market context and is not enabled by this bare reference generator.")

    role_profile = role_profiles[role]

    design_seed = f"{campaign_seed}|{era_id}|{operator_context}|{role}|civilian_design_v0.1"
    design_rng = DeterministicRng(design_seed)
    size = design_rng.weighted_choice(list(role_profile["size_weights"].items()))
    design_id = f"gen:ship_design:{stable_token(design_seed, size)}"

    size_guidance = load_json(STAFFING_GUIDANCE)["procedural_design_size_bands"][size]
    crew_low, crew_high = size_guidance["target_duty_crew"]

    ship_seed = f"{campaign_seed}|{need_id}|{campaign_date}|{design_id}|civilian_ship"
    ship_rng = DeterministicRng(ship_seed)
    crew_count = ship_rng.randint(int(crew_low), int(crew_high))

    selector = role_profile["habitability_selector"]
    life_profile = life_profiles_by_selector()[selector]
    watch = generic_watch_allocation(
        crew_count,
        small=(selector == "micro_or_small" or crew_count <= 8),
    )
    civilians, passengers = passenger_capacity(ship_rng, role, size)

    ship_id = f"gen:starship:{stable_token(ship_seed, str(crew_count))}"
    designation = f"CIV-{stable_token(ship_id, length=7).upper()}"

    return {
        "schema_version": "0.1.0",
        "generator": {
            "generator_id": GENERATOR_ID,
            "generator_version": GENERATOR_VERSION,
            "algorithm": "sha256_counter_v1",
        },
        "generation_context": {
            "campaign_seed": campaign_seed,
            "need_id": need_id,
            "era_id": era_id,
            "campaign_date": campaign_date,
            "operator_context": operator_context,
            "role": role,
        },
        "design": {
            "design_id": design_id,
            "design_mode": "procedural_design",
            "role_family": role,
            "size_band": size,
            "crew_style": role_profile["crew_style"],
            "capacity_focus": role_profile["capacity_focus"],
            "habitability_selector": selector,
            "design_seed_hash": hashlib.sha256(design_seed.encode("utf-8")).hexdigest(),
            "reusable_across_individual_ships": True,
        },
        "ship": {
            "ship_id": ship_id,
            "designation": designation,
            "designation_status": "temporary_generated_designation",
            "design_id": design_id,
            "operator_context": operator_context,
            "role": role,
            "canonical_identity_reserved": False,
            "persistent": True,
        },
        "population": {
            "duty_crew_target": crew_count,
            "civilian_residents": civilians,
            "passengers": passengers,
            "total_people_aboard_initial": crew_count + civilians + passengers,
            "live_manifest_status": "TO_BE_MATERIALIZED_FROM_REAL_STAFFING_SLOTS",
        },
        "shipboard_life": {
            "life_profile_id": life_profile["life_profile_id"],
            "habitability_tier": life_profile["habitability_tier"],
            "privacy_level": life_profile["privacy_level"],
            "social_density": life_profile["social_density"],
            "family_civilian_policy": life_profile["family_civilian_policy"],
            "recreation_capabilities": life_profile["recreation_capabilities"],
            "life_character": life_profile["life_character"],
            "watch": watch,
        },
        "persistence": {
            "materialized": True,
            "reroll_on_reload": False,
            "design_reusable": True,
            "ship_history_independent_from_other_vessels_of_same_design": True,
        },
    }


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    design = payload.get("design", {})
    ship = payload.get("ship", {})
    pop = payload.get("population", {})
    watch = payload.get("shipboard_life", {}).get("watch", {})
    if not design.get("design_id", "").startswith("gen:ship_design:"):
        errors.append("missing procedural design id")
    if not ship.get("ship_id", "").startswith("gen:starship:"):
        errors.append("missing procedural ship id")
    if ship.get("design_id") != design.get("design_id"):
        errors.append("ship/design identity mismatch")
    if watch.get("allocation_total") != pop.get("duty_crew_target"):
        errors.append("watch allocation does not match duty crew")
    if ship.get("canonical_identity_reserved"):
        errors.append("civilian procedural ship cannot reserve canonical identity")
    if payload.get("persistence", {}).get("reroll_on_reload") is not False:
        errors.append("ship must not reroll on reload")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--era", default="tng_ds9_voyager")
    parser.add_argument("--date", default="2372-01-01")
    parser.add_argument("--role", required=True)
    parser.add_argument("--operator-context", default="independent_civilian")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = generate(
        campaign_seed=args.seed,
        need_id=args.need_id,
        era_id=args.era,
        campaign_date=args.date,
        role=args.role,
        operator_context=args.operator_context,
    )
    if args.validate:
        errors = validate(payload)
        if errors:
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
