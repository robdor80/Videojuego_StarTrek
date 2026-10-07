#!/usr/bin/env python3
"""Deterministic reference generator for persistent Star Trek ship instances.

This tool is a content/rules reference implementation. CoreRPG remains the future
authoritative runtime owner of persistent World State.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

STARFLEET_CLASSES = ROOT / "lore/starships/classes/core_starship_classes.json"
NON_STARFLEET_CLASSES = ROOT / "lore/starships/classes/non_starfleet_core_starship_classes.json"
STAFFING_GUIDANCE = ROOT / "universe/generation/ship_staffing_generation_guidance_v0.1.json"
LIFE_PROFILE_FILES = (
    ROOT / "lore/starships/classes/shipboard_life/STARFLEET_SHIPBOARD_LIFE_PROFILES_v0.1.json",
    ROOT / "lore/starships/classes/shipboard_life/KLINGON_SHIPBOARD_LIFE_PROFILES_v0.1.json",
    ROOT / "lore/starships/classes/shipboard_life/ROMULAN_SHIPBOARD_LIFE_PROFILES_v0.1.json",
    ROOT / "lore/starships/classes/shipboard_life/CARDASSIAN_SHIPBOARD_LIFE_PROFILES_v0.1.json",
)

GENERATOR_ID = "procedural_starship_reference_generator"
GENERATOR_VERSION = "0.1.0"

OPERATOR_MAP = {
    "starfleet": "starfleet",
    "klingon": "klingon_imperial_military",
    "romulan": "romulan_military",
    "cardassian": "cardassian_military",
}


class DeterministicRng:
    def __init__(self, seed_material: str) -> None:
        self.seed_material = seed_material
        self.counter = 0

    def _u256(self) -> int:
        payload = f"{self.seed_material}|{self.counter}".encode("utf-8")
        self.counter += 1
        return int.from_bytes(hashlib.sha256(payload).digest(), "big")

    def randint(self, low: int, high: int) -> int:
        if high < low:
            raise ValueError("high must be >= low")
        return low + self._u256() % (high - low + 1)

    def choice(self, values: list[Any]) -> Any:
        if not values:
            raise ValueError("choice requires values")
        return values[self._u256() % len(values)]

    def weighted_choice(self, entries: list[tuple[Any, int]]) -> Any:
        total = sum(weight for _, weight in entries)
        if total <= 0:
            raise ValueError("weights must sum to > 0")
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


def parse_year(campaign_date: str) -> int:
    return int(campaign_date.split("-", 1)[0])


def class_is_available(entry: dict[str, Any], era_id: str, year: int) -> bool:
    availability = entry.get("availability", {})
    retained = availability.get("retained_playable_profiles", [])
    if retained and era_id not in retained:
        return False

    if year < int(availability.get("operational_class_from_year", -10**9)):
        return False
    if year < int(availability.get("confirmed_active_by_year", -10**9)):
        return False
    if year < int(availability.get("confirmed_active_from_decade", -10**9)):
        return False
    return True


def all_classes() -> list[dict[str, Any]]:
    return (
        load_json(STARFLEET_CLASSES).get("classes", [])
        + load_json(NON_STARFLEET_CLASSES).get("classes", [])
    )


def choose_class(
    rng: DeterministicRng,
    operator: str,
    era_id: str,
    year: int,
    role: str | None,
) -> dict[str, Any]:
    actual_operator = OPERATOR_MAP[operator]
    valid = [
        row for row in all_classes()
        if row.get("operator") == actual_operator
        and class_is_available(row, era_id, year)
    ]
    if not valid:
        raise ValueError(f"No class available for operator={operator} era={era_id} year={year}")

    if role:
        matching = [
            row for row in valid
            if role in row.get("primary_gameplay_roles", [])
            or role in row.get("classifications", [])
        ]
        if matching:
            valid = matching

    weighted: list[tuple[dict[str, Any], int]] = []
    for row in valid:
        weight = 1
        if role in row.get("primary_gameplay_roles", []):
            weight += 8
        if role in row.get("classifications", []):
            weight += 4
        weighted.append((row, weight))
    return rng.weighted_choice(weighted)


def choose_configuration(
    rng: DeterministicRng,
    class_entry: dict[str, Any],
    era_id: str,
    year: int,
) -> tuple[str | None, str]:
    class_id = class_entry["class_id"]

    configs = class_entry.get("configuration_profiles", [])
    if configs:
        matching = []
        for config in configs:
            start, end = config.get("year_range", [-10**9, 10**9])
            if start <= year <= end and config.get("era_id", era_id) == era_id:
                matching.append(config)
        if matching:
            selected = matching[0]
            return selected["id"], f"{class_id}/{selected['id']}"

    if class_id == "klingon_bird_of_prey":
        if era_id == "kirk":
            variant = "brel"
        else:
            variant = rng.weighted_choice([("brel", 3), ("kvort", 2)])
        return variant, f"klingon_bird_of_prey/{variant}"

    return None, class_id


def life_profile_index() -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in LIFE_PROFILE_FILES:
        payload = load_json(path)
        for profile in payload.get("profiles", {}).values():
            ref = profile.get("class_or_configuration_ref")
            if ref:
                index[ref] = profile
    return index


def staffing_key(class_ref: str, year: int, role: str | None) -> str:
    if class_ref == "constitution/constitution_major_refit":
        return (
            "constitution/constitution_major_refit_2290s"
            if year >= 2290
            else "constitution/constitution_major_refit_2270s_2280s"
        )
    if class_ref == "miranda":
        return "miranda/24c" if year >= 2300 else "miranda/23c"
    if class_ref == "d7":
        return "d7/2250s" if year < 2260 else "d7/2260s_2270s"
    if class_ref == "galaxy":
        if role in {"fleet_operations", "combat", "troop_transport"}:
            return "galaxy/fleet_or_evacuative_assignment"
        return "galaxy/explorer_baseline"
    return class_ref


def generate_crew_count(
    rng: DeterministicRng,
    class_ref: str,
    year: int,
    role: str | None,
) -> tuple[int, dict[str, Any], str]:
    guidance = load_json(STAFFING_GUIDANCE).get("profiles", {})
    key = staffing_key(class_ref, year, role)
    row = guidance.get(key)
    if not row:
        raise ValueError(f"No staffing guidance for {class_ref} (resolved key {key})")
    low, high = row["target_duty_crew"]
    return rng.randint(int(low), int(high)), row, key


def allocate_by_fractions(
    total: int,
    fractions: dict[str, float],
) -> dict[str, int]:
    raw = {key: total * float(value) for key, value in fractions.items()}
    floors = {key: int(value) for key, value in raw.items()}
    remaining = total - sum(floors.values())
    order = sorted(
        fractions,
        key=lambda key: (raw[key] - floors[key], key),
        reverse=True,
    )
    for key in order[:remaining]:
        floors[key] += 1
    return floors


def custom_small_crew_allocation(total: int) -> dict[str, int]:
    if total <= 5:
        active = max(1, total // 2)
        secondary = max(1, total - active - 1) if total >= 3 else max(0, total - active)
        rest = max(0, total - active - secondary)
        return {"active_control": active, "secondary_or_maintenance": secondary, "rest_or_relief": rest}

    group_a = max(2, round(total * 0.40))
    group_b = max(2, round(total * 0.35))
    flex = total - group_a - group_b
    if flex < 1:
        group_b -= 1
        flex = 1
    return {"watch_group_a": group_a, "watch_group_b": group_b, "flex_or_relief": flex}


def hhmm(hour: int) -> str:
    return f"{hour % 24:02d}:00"


def make_watch_schedule(
    rng: DeterministicRng,
    operator: str,
    life_profile: dict[str, Any],
    crew_count: int,
    requested_pattern: str | None,
) -> dict[str, Any]:
    guidance = life_profile.get("watch_guidance", {})
    preferred = guidance.get("preferred_pattern", "custom")

    if operator == "starfleet":
        if requested_pattern in {"three_shift", "four_shift"}:
            pattern = requested_pattern
        else:
            pattern = "three_shift" if preferred == "three_shift" else preferred

        if pattern == "four_shift":
            labels = ["alpha", "beta", "gamma", "delta"]
            duration = 6
            anchor = rng.choice([0, 6])
            fractions = {
                "alpha": 0.26,
                "beta": 0.24,
                "gamma": 0.23,
                "delta": 0.22,
                "relief_or_float": 0.05,
            }
        else:
            pattern = "three_shift"
            labels = ["alpha", "beta", "gamma"]
            duration = 8
            anchor = rng.choice([0, 4, 8])
            fractions = guidance.get("routine_primary_watch_allocation", {})

        allocation = allocate_by_fractions(crew_count, fractions) if isinstance(fractions, dict) else {}
        definitions = []
        for index, label in enumerate(labels):
            start = anchor + index * duration
            definitions.append({
                "watch_id": label,
                "starts_at_ship_time": hhmm(start),
                "ends_at_ship_time": hhmm(start + duration),
                "nominal_duration_hours": duration,
                "assigned_primary_personnel": allocation.get(label, 0),
            })
        return {
            "pattern": pattern,
            "shipboard_cycle_hours": 24,
            "schedule_provenance": "GAME_ADDITION_INSTANCE_POLICY",
            "definitions": definitions,
            "relief_or_float": allocation.get("relief_or_float", 0),
            "allocation_total": sum(allocation.values()),
        }

    if "staggered_small_crew" in preferred:
        allocation = custom_small_crew_allocation(crew_count)
        return {
            "pattern": "custom_staggered_small_crew",
            "shipboard_cycle_hours": 24,
            "schedule_provenance": "GAME_ADDITION",
            "definitions": [],
            "staggered_groups": allocation,
            "allocation_total": sum(allocation.values()),
        }

    fractions = guidance.get("routine_primary_watch_allocation", {})
    allocation = allocate_by_fractions(crew_count, fractions) if isinstance(fractions, dict) else {}
    duration = 8
    anchor = rng.choice([0, 4, 8])
    definitions = []
    for index, label in enumerate(["watch_1", "watch_2", "watch_3"]):
        definitions.append({
            "watch_id": label,
            "starts_at_ship_time": hhmm(anchor + index * duration),
            "ends_at_ship_time": hhmm(anchor + (index + 1) * duration),
            "nominal_duration_hours": duration,
            "assigned_primary_personnel": allocation.get(label, 0),
        })
    return {
        "pattern": "custom_three_watch_equivalent",
        "shipboard_cycle_hours": 24,
        "schedule_provenance": "GAME_ADDITION_NOT_CANON_LABELS",
        "definitions": definitions,
        "relief_or_float": allocation.get("relief_or_float", 0),
        "allocation_total": sum(allocation.values()),
    }


def generate(
    *,
    campaign_seed: str,
    era_id: str,
    campaign_date: str,
    operator: str,
    role: str | None = None,
    requested_watch_pattern: str | None = None,
    need_id: str = "default",
) -> dict[str, Any]:
    if operator not in OPERATOR_MAP:
        raise ValueError(f"Unsupported operator alias: {operator}")

    year = parse_year(campaign_date)
    need_scope = "" if need_id == "default" else f"|{need_id}"
    seed_key = f"{campaign_seed}|{era_id}|{campaign_date}|{operator}|{role or 'auto'}|ship{need_scope}"
    rng = DeterministicRng(seed_key)

    class_entry = choose_class(rng, operator, era_id, year, role)
    configuration_id, class_ref = choose_configuration(rng, class_entry, era_id, year)

    life_profiles = life_profile_index()
    life_profile = life_profiles.get(class_ref)
    if not life_profile:
        raise ValueError(f"No shipboard life profile for {class_ref}")

    crew_count, staffing_row, staffing_key_value = generate_crew_count(
        rng, class_ref, year, role
    )
    watch = make_watch_schedule(
        rng, operator, life_profile, crew_count, requested_watch_pattern
    )

    ship_id = f"gen:starship:{stable_token(seed_key, class_ref, str(crew_count))}"
    designation = f"{operator.upper()}-{stable_token(ship_id, length=6).upper()}"

    civilians = 0
    passengers = 0
    if class_ref == "galaxy":
        c_range = staffing_row.get("civilian_resident_range", [0, 0])
        p_range = staffing_row.get("passenger_range", [0, 0])
        civilians = rng.randint(int(c_range[0]), int(c_range[1]))
        passengers = rng.randint(int(p_range[0]), int(p_range[1]))

    result = {
        "schema_version": "0.1.0",
        "generator": {
            "generator_id": GENERATOR_ID,
            "generator_version": GENERATOR_VERSION,
            "algorithm": "sha256_counter_v1",
        },
        "generation_context": {
            "campaign_seed": campaign_seed,
            "era_id": era_id,
            "campaign_date": campaign_date,
            "operator_alias": operator,
            "operator_id": OPERATOR_MAP[operator],
            "requested_role": role,
            "need_id": need_id,
            "seed_key_hash": hashlib.sha256(seed_key.encode("utf-8")).hexdigest(),
        },
        "ship": {
            "ship_id": ship_id,
            "designation": designation,
            "designation_status": "temporary_generated_designation",
            "class_id": class_entry["class_id"],
            "configuration_id": configuration_id,
            "class_or_configuration_ref": class_ref,
            "operator": class_entry["operator"],
            "role": role or rng.choice(class_entry.get("primary_gameplay_roles", ["unspecified"])),
            "canonical_identity_reserved": False,
            "persistent": True,
        },
        "population": {
            "duty_crew_target": crew_count,
            "civilian_residents": civilians,
            "passengers": passengers,
            "total_people_aboard_initial": crew_count + civilians + passengers,
            "staffing_guidance_key": staffing_key_value,
            "staffing_confidence": staffing_row.get("confidence"),
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
            "class_history_mutable_only_through_refit_or_reclassification_event": True,
            "crew_changes_append_history": True,
        },
    }
    return result


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    ship = payload.get("ship", {})
    pop = payload.get("population", {})
    life = payload.get("shipboard_life", {})
    watch = life.get("watch", {})

    if not ship.get("ship_id", "").startswith("gen:starship:"):
        errors.append("missing/invalid generated ship id")
    if not ship.get("class_id"):
        errors.append("missing class id")
    if pop.get("duty_crew_target", 0) <= 0:
        errors.append("non-positive duty crew target")
    if not life.get("life_profile_id"):
        errors.append("missing life profile")
    if watch.get("allocation_total") != pop.get("duty_crew_target"):
        errors.append(
            f"watch allocation {watch.get('allocation_total')} != duty crew {pop.get('duty_crew_target')}"
        )
    if pop.get("civilian_residents", 0) < 0 or pop.get("passengers", 0) < 0:
        errors.append("negative non-duty population")
    if ship.get("canonical_identity_reserved"):
        errors.append("procedural fixture cannot claim canonical identity")
    if payload.get("persistence", {}).get("reroll_on_reload") is not False:
        errors.append("generated ship must not reroll on reload")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--era", default="tng_ds9_voyager")
    parser.add_argument("--date", default="2372-01-01")
    parser.add_argument("--operator", choices=sorted(OPERATOR_MAP), default="starfleet")
    parser.add_argument("--role")
    parser.add_argument("--need-id", default="default", help="Stable causal need/event id used to distinguish vessels inside one campaign.")
    parser.add_argument("--watch-pattern", choices=["three_shift", "four_shift"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = generate(
        campaign_seed=args.seed,
        era_id=args.era,
        campaign_date=args.date,
        operator=args.operator,
        role=args.role,
        requested_watch_pattern=args.watch_pattern,
        need_id=args.need_id,
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
