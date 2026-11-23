#!/usr/bin/env python3
"""LORE-05C: control de documentos, no de runtime; solo bibliotecas estándar."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOGUE = "mundo/lore/astrography/worlds/lore05c_priority_locations_v0.1.json"
SCENARIOS = "mundo/lore/astrography/worlds/lore05c_validation_cases_v0.1.json"
ANCHORS = "mundo/lore/astrography/systems/anchor_locations.json"
REGISTRY = "mundo/sources/source_registry/source_registry.json"
FACILITIES = "mundo/lore/stations_and_facilities/canonical_unique_facilities_v0.1.json"
GUIDE = "mundo/lore/astrography/worlds/lore05c_guia_localizaciones_2026-11-13.md"
INDEX = "proyecto/docs/roadmap/lore_05_c/README.md"

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def problems_for_data(data: dict, cases: dict, anchors: dict, registry: dict, facilities: dict) -> list[str]:
    problems: list[str] = []
    entries = data.get("locations", [])
    if len(entries) != 16 or len({x.get("id") for x in entries}) != 16:
        problems.append("Expected 16 unique location IDs")
    if data.get("campaign_baseline_year") != 2383 or data.get("authority") != "CoreRPG_World_State_ONLY":
        problems.append("Campaign year or authority incorrect")
    if data.get("no_new_coordinates") is not True or data.get("no_new_routes") is not True or data.get("no_live_mutations") is not True:
        problems.append("Illegal navigation/runtime mutation flags")
    known_anchors = {x["location_id"] for x in anchors["locations"]}
    known_sources = {x["source_id"] for x in registry["sources"]}
    known_facilities = {x["facility_id"] for x in facilities["facilities"]}
    for item in entries:
        id_ = item.get("id", "?")
        anchor = item.get("anchor_location_id")
        if anchor is not None and anchor not in known_anchors:
            problems.append(f"{id_}: anchor missing")
        facility = item.get("facility_id")
        if facility is not None and facility not in known_facilities:
            problems.append(f"{id_}: facility identity missing")
        path = item.get("depth_profile_ref")
        if path is not None and not (ROOT / path).is_file():
            problems.append(f"{id_}: depth profile missing")
        sources = item.get("source_refs")
        if not sources or not set(sources).issubset(known_sources):
            problems.append(f"{id_}: source unknown")
        if not all(item.get(k) for k in ("display_name_es","context_2383","gameplay_opportunities","hard_limits")):
            problems.append(f"{id_}: empty documentary field")
        if any(item.get(k) is not False for k in ("runtime_generation_enabled","automatic_travel_enabled","world_state_mutations")):
            problems.append(f"{id_}: automatic action not allowed")
        if any(k in item for k in ("coordinates","route_distance","owner_live","population_count","spawn_enabled")):
            problems.append(f"{id_}: unauthorized dynamic/geographic data")
    by_id = {x.get("id"): x for x in entries}
    expected = {
        "mars_utopia": ("SOL_CONTEXT_NO_PLANET_ANCHOR","sol_system"),
        "dorvan_v": ("HISTORICAL_REFERENCE_ONLY",None),
        "new_bajor": ("DESTROYED_REFERENCE_ONLY",None),
        "romulus": ("ANCHORED_DOCUMENTARY","romulus"),
        "bajor": ("ANCHORED_DOCUMENTARY","bajor"),
        "deep_space_9": ("ANCHORED_DOCUMENTARY","deep_space_9"),
    }
    for id_, (availability, anchor) in expected.items():
        row = by_id.get(id_, {})
        if row.get("availability") != availability or row.get("anchor_location_id") != anchor:
            problems.append(f"{id_}: history/availability/anchor broken")
    if by_id.get("mars_utopia",{}).get("facility_id") != "canon:facility:utopia_planitia_fleet_yards":
        problems.append("Mars facility not properly reserved")
    if by_id.get("deep_space_9",{}).get("facility_id") != "canon:facility:deep_space_9":
        problems.append("DS9 unique facility not reserved")
    cs = cases.get("scenarios", [])
    if len(cs) != 12 or len({c.get("id") for c in cs}) != 12:
        problems.append("Expected 12 unique validation scenarios")
    if cases.get("runtime_executed") is not False:
        problems.append("Must not claim runtime integration")
    for c in cs:
        if c.get("documentary_only") is not True or c.get("no_world_state_mutation") is not True or not c.get("expected"):
            problems.append("Invalid scenario boundary")
    return problems

def validate() -> list[str]:
    problems = problems_for_data(load(CATALOGUE),load(SCENARIOS),load(ANCHORS),load(REGISTRY),load(FACILITIES))
    for path in (GUIDE,INDEX):
        if not (ROOT / path).is_file():
            problems.append(f"Missing editorial file {path}")
    return problems

if __name__ == "__main__":
    errors = validate()
    if errors:
        for e in errors:
            print("ERROR:",e)
        raise SystemExit(1)
    print("LORE-05C: PASS; 16 documentary locations, 12 cases; no runtime proof")
