#!/usr/bin/env python3
"""Deterministic reference quarters assignment for Academy Life Step 4."""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from typing import Any

RULES_VERSION = "academy_quarters_v0.1"

def stable_hex(*parts: Any, size: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def compatible(cadet: dict[str, Any], room: dict[str, Any]) -> bool:
    required = set(cadet.get("hard_housing_requirement_tags", []))
    capabilities = set(room.get("capability_tags", []))
    if not required.issubset(capabilities):
        return False
    if cadet.get("single_occupancy_required") and int(room["capacity"]) != 1:
        return False
    allowed = room.get("allowed_cadet_class_ids")
    return not allowed or cadet.get("cadet_class_id") in allowed

def assign_quarters(request: dict[str, Any]) -> dict[str, Any]:
    seed = request["campaign_seed"]
    cadets = copy.deepcopy(request["cadets"])
    rooms = copy.deepcopy(request["rooms"])

    if len({c["population_slot_ref"] for c in cadets}) != len(cadets):
        raise ValueError("duplicate cadet population_slot_ref")
    if len({r["room_id"] for r in rooms}) != len(rooms):
        raise ValueError("duplicate room_id")

    for room in rooms:
        if int(room["capacity"]) <= 0:
            raise ValueError("room capacity must be positive")
        room.setdefault("occupant_slot_refs", [])
        if len(room["occupant_slot_refs"]) > int(room["capacity"]):
            raise ValueError("room over capacity before assignment")

    existing = [slot for room in rooms for slot in room["occupant_slot_refs"]]
    if len(existing) != len(set(existing)):
        raise ValueError("slot already occupies multiple rooms")

    assignments = {slot: room["room_id"] for room in rooms for slot in room["occupant_slot_refs"]}
    by_slot = {c["population_slot_ref"]: c for c in cadets}

    def scarcity_key(cadet: dict[str, Any]):
        compatible_room_count = sum(1 for room in rooms if compatible(cadet, room))
        return (
            compatible_room_count,
            stable_hex(seed, "cadet_order", cadet["population_slot_ref"], RULES_VERSION),
        )

    unassigned = sorted(
        [c for c in cadets if c["population_slot_ref"] not in assignments],
        key=scarcity_key,
    )

    for cadet in unassigned:
        candidates = [
            room for room in rooms
            if len(room["occupant_slot_refs"]) < int(room["capacity"]) and compatible(cadet, room)
        ]
        if not candidates:
            continue

        scored = []
        for room in candidates:
            same_class_preference = 0
            if request.get("prefer_same_cadet_class_roommates", False) and room["occupant_slot_refs"]:
                same_class_preference = int(all(
                    by_slot[slot].get("cadet_class_id") == cadet.get("cadet_class_id")
                    for slot in room["occupant_slot_refs"] if slot in by_slot
                ))
            soft_matches = len(
                set(cadet.get("soft_housing_preference_tags", []))
                & set(room.get("preference_tags", []))
            )
            scored.append((
                -same_class_preference,
                -soft_matches,
                stable_hex(seed, "room_choice", cadet["population_slot_ref"], room["room_id"], RULES_VERSION),
                room,
            ))
        room = min(scored, key=lambda item: item[:3])[3]
        room["occupant_slot_refs"].append(cadet["population_slot_ref"])
        assignments[cadet["population_slot_ref"]] = room["room_id"]

    roommate_map = {}
    for room in rooms:
        occupants = list(room["occupant_slot_refs"])
        for slot in occupants:
            roommate_map[slot] = sorted(other for other in occupants if other != slot)

    unresolved = [
        {
            "population_slot_ref": cadet["population_slot_ref"],
            "reason": "no_compatible_capacity",
            "hard_housing_requirement_tags": list(cadet.get("hard_housing_requirement_tags", [])),
            "single_occupancy_required": bool(cadet.get("single_occupancy_required", False)),
        }
        for cadet in cadets
        if cadet["population_slot_ref"] not in assignments
    ]

    return {
        "rules_version": RULES_VERSION,
        "room_assignments": dict(sorted(assignments.items())),
        "roommate_slot_refs": dict(sorted(roommate_map.items())),
        "rooms": sorted(rooms, key=lambda room: room["room_id"]),
        "unresolved_housing_needs": unresolved,
        "automatic_relationship_effect": "none",
        "future_step_state": {
            "personal_schedules": [],
            "social_relationship_changes": [],
            "romance_state": [],
        },
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    request = payload.get("request", payload)
    print(json.dumps(assign_quarters(request), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
