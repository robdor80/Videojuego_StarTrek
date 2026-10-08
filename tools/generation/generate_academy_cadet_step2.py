#!/usr/bin/env python3
"""Deterministic reference generator for Academy Life Step 2 — procedural cadets."""

from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

RULES_VERSION = "academy_cadet_generation_v0.1"
VALID_CLASSES = {
    "cadet_fourth_class",
    "cadet_third_class",
    "cadet_second_class",
    "cadet_first_class",
}

def stable_hex(*parts: Any, size: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def stable_index(length: int, *parts: Any) -> int:
    if length <= 0:
        raise ValueError("empty candidate pool")
    return int(stable_hex(*parts, size=12), 16) % length

def weighted_pick(items: list[dict[str, Any]], *parts: Any) -> dict[str, Any]:
    if not items:
        raise ValueError("empty weighted pool")
    weights = [max(0, int(item.get("weight", 1))) for item in items]
    total = sum(weights)
    if total <= 0:
        raise ValueError("weighted pool has no positive weight")
    ticket = int(stable_hex(*parts, size=12), 16) % total
    cursor = 0
    for item, weight in zip(items, weights):
        cursor += weight
        if ticket < cursor:
            return copy.deepcopy(item)
    return copy.deepcopy(items[-1])

def pick_distinct(items: list[Any], count: int, *parts: Any) -> list[Any]:
    pool = list(items)
    output: list[Any] = []
    for index in range(min(count, len(pool))):
        choice = stable_index(len(pool), *parts, index)
        output.append(pool.pop(choice))
    return output

def generate_cadet(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("population_category") != "cadet":
        raise ValueError("academy cadet generation requires cadet population slot")
    if request.get("cadet_class_id") not in VALID_CLASSES:
        raise ValueError("invalid cadet class")
    for required in ("campaign_seed", "population_registry_id", "group_id", "population_slot_ref"):
        if not request.get(required):
            raise ValueError(f"missing {required}")

    character_id = "cadet:proc:" + stable_hex(
        request["campaign_seed"], request["population_registry_id"], request["group_id"],
        request["population_slot_ref"], "identity", RULES_VERSION
    )

    species = weighted_pick(
        request["species_pool"], request["campaign_seed"], character_id, "species", RULES_VERSION
    )

    contexts = [
        context for context in request["social_origin_context_pool"]
        if not context.get("allowed_species_ids") or species["species_id"] in context["allowed_species_ids"]
    ]
    if not contexts:
        raise ValueError("no eligible social/origin context")
    context = weighted_pick(
        contexts, request["campaign_seed"], character_id, "social_origin", RULES_VERSION
    )

    reserved = set(request.get("reserved_display_names", []))
    names = [name for name in context.get("name_candidates", []) if name not in reserved]
    if not names:
        raise ValueError("no non-colliding display name candidate")
    display_name = names[
        stable_index(
            len(names), request["campaign_seed"], character_id, "name",
            context["context_id"], RULES_VERSION
        )
    ]

    branch_ids = [entry["branch_id"] for entry in request["branch_pool"]]
    branch_interests = pick_distinct(
        branch_ids, 2, request["campaign_seed"], character_id, "branch_interests", RULES_VERSION
    )
    specialization = None
    if request["cadet_class_id"] in {"cadet_second_class", "cadet_first_class"}:
        specialization = branch_interests[0] if branch_interests else None

    recipes = list(request["personality_recipe_ids"])
    personality_recipe_id = recipes[
        stable_index(
            len(recipes), request["campaign_seed"], character_id,
            "personality_recipe", RULES_VERSION
        )
    ]

    return {
        "character_id": character_id,
        "display_name": display_name,
        "identity_type": "generated",
        "population_slot_ref": request["population_slot_ref"],
        "cadet_class_id": request["cadet_class_id"],
        "species_id": species["species_id"],
        "origin_ref": context.get("origin_ref"),
        "culture_refs": context.get("culture_refs", []),
        "citizenship_refs": context.get("citizenship_refs", []),
        "academy_entry_basis_ref": request.get("academy_entry_basis_ref"),
        "adult_equivalent_status": True,
        "exact_age_or_birth_date": species.get("exact_age_or_birth_date"),
        "prior_education_refs": pick_distinct(
            request.get("prior_education_pool", []), 1,
            request["campaign_seed"], character_id, "prior_education", RULES_VERSION
        ),
        "interest_refs": pick_distinct(
            request.get("interest_pool", []), 2,
            request["campaign_seed"], character_id, "interests", RULES_VERSION
        ),
        "hobby_refs": pick_distinct(
            request.get("hobby_pool", []), 2,
            request["campaign_seed"], character_id, "hobbies", RULES_VERSION
        ),
        "branch_interest_ids": branch_interests,
        "specialization": specialization,
        "personality_seed": stable_hex(
            request["campaign_seed"], character_id, "personality", RULES_VERSION, size=32
        ),
        "personality_recipe_id": personality_recipe_id,
        "knowledge_seed": stable_hex(
            request["campaign_seed"], character_id, "knowledge", RULES_VERSION, size=32
        ),
        "background_seed": stable_hex(
            request["campaign_seed"], character_id, "background", RULES_VERSION, size=32
        ),
        "base_visual_identity_id": "visual:" + character_id,
        "academy_relationship_refs": [],
        "class_group_refs": [],
        "roommate_ref": None,
        "schedule_state_ref": None,
        "generation_provenance": {
            "rules_version": RULES_VERSION,
            "population_registry_id": request["population_registry_id"],
            "group_id": request["group_id"],
        },
    }

def materialize_into_registry(registry: dict[str, Any], cadet: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(registry)
    group = next(
        group for group in output["groups"]
        if group["group_id"] == cadet["generation_provenance"]["group_id"]
    )
    if group.get("category") != "cadet":
        raise ValueError("target group is not cadet")
    bindings = group.setdefault("materialized_slot_bindings", {})
    slot_ref = cadet["population_slot_ref"]
    if slot_ref in bindings:
        raise ValueError("population slot already materialized")
    all_ids = {
        character_id
        for entry in output["groups"]
        for character_id in entry.get("materialized_character_ids", [])
    }
    if cadet["character_id"] in all_ids:
        raise ValueError("character already materialized")
    if group["latent_count"] <= 0:
        raise ValueError("no latent slot available")
    group["latent_count"] -= 1
    group["materialized_character_ids"].append(cadet["character_id"])
    bindings[slot_ref] = cadet["character_id"]
    return output

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    request = payload.get("request", payload)
    result = generate_cadet(request)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
