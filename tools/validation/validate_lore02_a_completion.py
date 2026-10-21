#!/usr/bin/env python3
"""LORE-02 A closure gate: cross-references, provenance and adversarial evidence.
Only validates documentary data; does not run UE5 nor claim CoreRPG integration.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATLAS = "lore/technology/lore02_a_system_atlas_v0.2.json"
PROFILES = "lore/technology/lore02_a_operator_facility_profiles_v0.2.json"
CASES = "lore/technology/lore02_a_adversarial_cases_v0.2.json"
ADDENDUM = "lore/technology/valhalla_creative_addendum_2026-10-21.md"
GAPS = {f"A-G{i:02}" for i in range(1, 9)}
GAP_COUNTS = {"A-G01": 4, "A-G02": 6, "A-G03": 5, "A-G04": 5,
              "A-G05": 5, "A-G06": 8, "A-G07": 4, "A-G08": 8}

def get_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def file_exists(rel):
    return (isinstance(rel, str) and rel and not Path(rel).is_absolute()
            and ".." not in Path(rel).parts and (ROOT / rel).is_file())

def require(condition: bool, reason: str):
    if not condition:
        raise AssertionError(reason)

def validate() -> dict:
    atlas, profiles, cases = (get_json(p) for p in (ATLAS, PROFILES, CASES))
    registry = get_json("sources/source_registry/source_registry.json")
    initial = get_json("lore/technology/ship_station_catalogue_v0.1.json")
    matrix = get_json("gameplay/ship_operations/era_technology_matrix.json")
    nonfleet = get_json("lore/starships/classes/non_starfleet_core_starship_classes.json")
    grammar = get_json("universe/generation/procedural_station_design_grammar_v0.1.json")
    roster = get_json("lore/technology/valhalla_tech_decisions_v0.1.json")
    delta = get_json("universe/generation/lore01_tng_content_availability_v0.1.json")
    registered = {s["source_id"]: s for s in registry["sources"]}
    require(len(registered) == len(registry["sources"]), "Duplicated source ID")
    require(len(registered) >= 438, "Official research source registration incomplete")
    require(registry["last_updated"] >= "2026-10-21", "Source registry stale")
    require(atlas["schema_version"] == profiles["schema_version"] == cases["schema_version"] == "0.2.0",
            "Wrong documentary schema version")
    require(atlas["mode"] == "EDITORIAL_NON_RUNTIME"
            and cases["status"] == "EDITORIAL_NON_RUNTIME",
            "False runtime claim")
    require(atlas["authority"] == "CoreRPG_WORLD_STATE_ONLY"
            and profiles["authority"] == "CoreRPG_ONLY", "World-state authority leak")
    require(atlas["era_matrix"] == "gameplay/ship_operations/era_technology_matrix.json",
            "Duplicate temporal matrix")
    require(len(matrix["profiles"]) == 5 and len(initial["records"]) == 14,
            "Altered legacy contracts/corpus")
    for rel in (atlas["companion_catalogue"], atlas["source_registry"], atlas["era_matrix"],
                profiles["existing_classes"], profiles["facility_grammar"], ADDENDUM):
        require(file_exists(rel), "Broken master reference: " + rel)

    records = atlas["records"]
    ids = [r["technology_id"] for r in records]
    require(len(records) == atlas["record_count"] == 45, "Record count mismatch")
    require(len(ids) == len(set(ids)), "Duplicate new technology ID")
    require(set(atlas["covered_gaps"]) == GAPS
            and dict(Counter(x["gap_id"] for x in records)) == GAP_COUNTS,
            "Eight gaps not fully covered")
    combined_ids = set(ids) | {x["technology_id"] for x in initial["records"]}
    approved_sources = {"OFFICIAL_REFERENCE", "RELIABLE_SECONDARY", "SCREEN_CANON"}
    for item in records:
        uid = item["technology_id"]
        require(uid.startswith("l02a_") and bool(item["display_name"]) and bool(item["mission_role"]),
                "Invalid definition: " + uid)
        require(item["gap_id"] in GAPS and len(item["dependencies"]) >= 3,
                "Missing gap / dependencies: " + uid)
        require(len(item["failure_mode"]) >= 45 and len(item["forbidden_inference"]) >= 30,
                "Missing actual failure or safety limit: " + uid)
        require(item["classification"] in ("SOURCE_BOUNDED_INFERENCE",
                "INFERRED_FROM_REFERENCES", "GAME_ADDITION"),
                "Unsupported evidence claim: " + uid)
        require(item["real_numeric_specs"] is None and item["runtime_mutation_allowed"] is False,
                "Fabricated performance or executable data: " + uid)
        require(item["platform_scope"] in ("CLASS_ERA_OPERATOR_SPECIFIC",
                "STATION_DESIGN_SPECIFIC", "ENTERPRISE_VALHALLA_LOCAL"),
                "Availability overgeneralized: " + uid)
        require(len(item["observable_state"]) >= 4
                and "observer_data_freshness" in item["observable_state"],
                "Knowledge/visibility not handled: " + uid)
        require(item["source_ids"] and all(s in registered and
                registered[s]["source_type"] in approved_sources for s in item["source_ids"]),
                "Unknown source / type: " + uid)
        require(item["gameplay_consumers"] and all(file_exists(x)
                for x in item["gameplay_consumers"]), "Broken gameplay consumer: " + uid)
        if item["gap_id"] == "A-G07":
            require(item["classification"] == "GAME_ADDITION"
                    and item["platform_scope"] == "ENTERPRISE_VALHALLA_LOCAL",
                    "Valhalla game-specific tech mislabeled: " + uid)
        if item["gap_id"] == "A-G08":
            require(item["platform_scope"] == "STATION_DESIGN_SPECIFIC",
                    "Station capabilities generalized: " + uid)

    require(profiles["status"] == "RESEARCH_IN_PROGRESS"
            and profiles["facility_generation_allowed"] is False
            and profiles["delta_dlc_enabled"] is False, "Operator/facility atlas grants runtime powers")
    operators, facilities = profiles["operators"], profiles["facility_roles"]
    require(len(operators) == profiles["operators_count"] == 9
            and len({x["operator_id"] for x in operators}) == 9,
            "Operator profiles incomplete")
    class_ids = {x["class_id"] for x in nonfleet["classes"]}
    for o in operators:
        require(o["technology_refs"] and set(o["technology_refs"]) <= combined_ids,
                "Operator has dangling tech ref: " + o["operator_id"])
        require(set(o["source_ids"]) <= set(registered)
                and set(o["known_class_examples"]) <= class_ids,
                "Operator source / class invalid: " + o["operator_id"])
        require(o["completeness"] == "REPRESENTATIVE_NOT_EXHAUSTIVE"
                and o["no_runtime_unlock"] is True
                and len(o["anti_generalisation"]) >= 55,
                "Operator universal-installation leak: " + o["operator_id"])
    require(len(facilities) == profiles["facility_roles_count"] == 14
            and {x["role_id"] for x in facilities} == set(grammar["role_families"]),
            "Facility profiles diverge from procedural grammar")
    for f in facilities:
        require(set(f["technology_refs"]) <= combined_ids
                and set(f["source_ids"]) <= set(registered), "Dangling facility dependency")
        require("installed_modules" in f["required_finite_inputs"]
                and "supply_inventory" in f["required_finite_inputs"]
                and f["output_mode"] == "AUTHORING_ONLY_NO_NEW_STATION_SPAWN"
                and len(f["negative_invariant"]) >= 35,
                "Facility can materialize/cure without cause")

    require(cases["status"] == "EDITORIAL_NON_RUNTIME"
            and cases["case_count"] == len(cases["cases"]) == 36,
            "Adversarial matrix too small/inconsistent")
    require(len({x["case_id"] for x in cases["cases"]}) == 36,
            "Duplicated adversarial ID")
    require({x["gap_id"] for x in cases["cases"]} == GAPS
            and min(Counter(x["gap_id"] for x in cases["cases"]).values()) >= 4,
            "Missing case families")
    for case in cases["cases"]:
        require(set(case["technology_refs"]) <= set(ids)
                and case["gap_id"] in GAPS
                and all(x in case["preconditions"] for x in (
                    "campaign_continuity", "platform_class_and_installed_modules",
                    "real_power_damage_resources_and_staff", "authenticated_actor_authority",
                    "observer_knowledge_timestamp")),
                "Test bypasses state/authority/visibility")
        require(len(case["required_response"]) > 48
                and len(case["forbidden_result"]) >= 30,
                "Scenario trivial or lacks negative conclusion: " + case["case_id"])
        require(case["expected_resolution"] == "HOST_AND_CORERPG_NOT_NARRATIVE_TEXT"
                and case["creates_world_state"] is False
                and case["unlocks_delta_dlc"] is False,
                "Scenario enables runtime or DLC")

    decision_ids = [x["decision_id"] for x in roster["decisions"]]
    require(decision_ids == [f"VAL-TEC-{i:02}" for i in range(1, 17)],
            "VAL-TEC 01-16 not consolidated")
    addendum = (ROOT / ADDENDUM).read_text(encoding="utf-8")
    for needle in ("continuidad propia", "No se fija año", "NCC-1701-G",
                   "clase Defiant", "camuflaje romulano excelente", "anillo/platillo",
                   "sección de batalla", "cubierta circular", "Sala de Ingeniería",
                   "IDEA-0004"):
        require(needle.lower() in addendum.lower(), "New author decision missing: " + needle)
    idea = (ROOT / "ideas/IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md").read_text(encoding="utf-8")
    require("ACTUALIZACIÓN DE AUTOR (21-10-2026)" in idea,
            "Historical IDEA-0010 supersession not visible")
    require(delta["delta_dlc"]["status"] == "FUTURE_NOT_IMPLEMENTED"
            and delta["delta_dlc"]["default_main_game_spawn_allowed"] is False,
            "DLC Delta inadvertently activated")
    status = (ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    require("| A — Tecnología de naves y estaciones | 🟧 NEEDS_REVIEW |" in status,
            "LORE-02 A must stay pending human review until merge")
    require("| B — Equipamiento personal y especializado | ⬜ TODO |" in status
            and "| C — Medicina y xenobiología | ⬜ TODO |" in status,
            "Unrelated blocks closed")
    return {
        "legacy_systems": len(initial["records"]),
        "new_systems": len(records),
        "total_systems": len(records) + len(initial["records"]),
        "operator_profiles": len(operators),
        "facility_role_profiles": len(facilities),
        "adversarial_cases": len(cases) + 14,
        "research_source_ids": len(registered),
        "gaps": len(GAPS),
        "status": "NEEDS_REVIEW",
    }

if __name__ == "__main__":
    print("LORE-02 A full review gate:", json.dumps(validate(), ensure_ascii=False))
