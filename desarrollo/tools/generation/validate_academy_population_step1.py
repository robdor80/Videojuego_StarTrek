#!/usr/bin/env python3
"""Reference validation utilities for Academy Life Step 1 — population."""

from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
from typing import Any

VALID_CLASSES = {
    "cadet_fourth_class",
    "cadet_third_class",
    "cadet_second_class",
    "cadet_first_class",
}
VALID_CATEGORIES = {
    "cadet",
    "instructional_staff",
    "operational_support_staff",
    "attached_training_personnel",
    "visitor",
}

def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen_characters: set[str] = set()
    seen_groups: set[str] = set()
    for group in registry.get("groups", []):
        gid = group["group_id"]
        if gid in seen_groups:
            errors.append(f"duplicate_group:{gid}")
        seen_groups.add(gid)
        total = int(group["total_count"])
        latent = int(group["latent_count"])
        absent = int(group.get("temporarily_absent_count", 0))
        materialized = list(group.get("materialized_character_ids", []))
        if min(total, latent, absent) < 0:
            errors.append(f"negative_count:{gid}")
        if latent + len(materialized) != total:
            errors.append(f"population_accounting_mismatch:{gid}")
        if absent > total:
            errors.append(f"absence_exceeds_membership:{gid}")
        if group["category"] not in VALID_CATEGORIES:
            errors.append(f"invalid_category:{gid}")
        if group["category"] == "cadet":
            if group.get("cadet_class_id") not in VALID_CLASSES:
                errors.append(f"invalid_cadet_class:{gid}")
        elif group.get("cadet_class_id") is not None:
            errors.append(f"noncadet_has_cadet_class:{gid}")
        for character_id in materialized:
            if character_id in seen_characters:
                errors.append(f"duplicate_character_membership:{character_id}")
            seen_characters.add(character_id)
    return errors

def materialize_latent_slot(registry: dict[str, Any], group_id: str, character_id: str) -> dict[str, Any]:
    result = copy.deepcopy(registry)
    all_ids = {
        cid
        for group in result["groups"]
        for cid in group.get("materialized_character_ids", [])
    }
    if character_id in all_ids:
        raise ValueError("character_id already materialized in registry")
    group = next(group for group in result["groups"] if group["group_id"] == group_id)
    if group["latent_count"] <= 0:
        raise ValueError("no latent slot available")
    group["latent_count"] -= 1
    group["materialized_character_ids"].append(character_id)
    return result

def apply_membership_event(registry: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(registry)
    group = next(group for group in result["groups"] if group["group_id"] == event["group_id"])
    event_type = event["type"]
    if event_type == "admit_latent":
        count = int(event.get("count", 1))
        group["total_count"] += count
        group["latent_count"] += count
    elif event_type == "depart_latent":
        count = int(event.get("count", 1))
        if count > group["latent_count"]:
            raise ValueError("not enough latent members")
        group["total_count"] -= count
        group["latent_count"] -= count
    elif event_type == "depart_materialized":
        character_id = event["character_id"]
        if character_id not in group["materialized_character_ids"]:
            raise ValueError("character is not a member of the group")
        group["materialized_character_ids"].remove(character_id)
        group["total_count"] -= 1
    else:
        raise ValueError(f"unsupported event type: {event_type}")
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    registry = json.loads(args.input.read_text(encoding="utf-8"))
    errors = validate_registry(registry)
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
