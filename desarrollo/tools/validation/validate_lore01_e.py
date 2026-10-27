#!/usr/bin/env python3
"""Validación documental de LORE-01 A–E. No evalúa escenas ni ejecuta CoreRPG/UE5."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "mundo/lore/operations"
AREAS = set("ABCDEFGH")
DELTA = {"kazon", "ocampan", "talaxian", "vidiian", "hirogen"}

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def path_exists(ref):
    path = ref.split("#", 1)[0]
    return bool(path) and (ROOT / path).is_file()

def validate():
    species = load("mundo/lore/species/LORE01_TNG_species_depth_index_v0.2.json")
    culture = load("mundo/lore/cultures/ai_behavior/species_behavior_index_v0.1.json")
    b = load("mundo/lore/factions/LORE01_B_civilizations_index_v0.1.json")
    c = load("mundo/lore/astrography/atlas/anchor_atlas_v0.1.json")
    d = load("mundo/lore/diplomacy/relation_index_v0.1.json")
    e = load("mundo/lore/diplomacy/historical_events_v0.1.json")
    sources = load("mundo/sources/source_registry/source_registry.json")
    gate = load("sistemas/universe/generation/lore01_tng_content_availability_v0.1.json")
    ops = load(BASE + "/operational_evidence_v0.1.json")
    queries = load(BASE + "/query_scenarios_v0.1.json")
    cross = load(BASE + "/cross_layer_reference_v0.1.json")
    gaps = load(BASE + "/uncertainty_ledger_v0.1.json")
    src = {v["source_id"] for v in sources["sources"]}
    entities = {v["civilization_id"] for v in b["main_game_entries"]}
    locs = {v["location_id"]: v for v in c["locations"]}
    relations = {v["relation_id"] for v in d["relations"]}
    events = {v["event_id"]: v for v in e["events"]}

    require(len(species["profiles"]) == 25 and len(culture["profiles"]) == 25,
            "A and A.1 baseline mismatch")
    require(culture["no_personality_by_species"] is True, "Culture is personality")
    require(len(entities) == len(b["main_game_entries"]) == 16, "B mismatch")
    require(len(locs) == c["location_count"] == 30, "C mismatch")
    require(len(relations) == d["relation_count"] == 27, "D relations mismatch")
    require(len(events) == e["event_count"] == 40, "D events mismatch")
    require(ops["status"] == queries["status"] == cross["status"]
            == gaps["status"] == "DOCUMENTARY_NOT_RUNTIME", "Runtime imported")
    require(ops["authority"] == queries["authority"] == cross["authority"]
            == "CoreRPG_World_State_ONLY", "World authority bypass")
    require(cross["runtime_import_allowed"] is False, "Execution declared")
    require(not ops["gameplay_activated"] and not ops["autonomous_future_script"]
            and not ops["delta_dlc_enabled"], "Gameplay activation")

    recs = ops["records"]
    ids = {row["record_id"] for row in recs}
    require(len(ids) == len(recs) == ops["record_count"] == 32, "Record ID/count collision")
    require(Counter(row["area"] for row in recs) == {area: 4 for area in AREAS},
            "Missing A–H domain")
    for row in recs:
        rid = row["record_id"]
        require(bool(re.fullmatch(r"OP-[A-H][0-9]{2}", rid)), "Invalid record ID: " + rid)
        require(all(isinstance(row[k], str) and len(row[k]) >= 35
                    for k in ("documented_observation", "operational_interpretation", "prohibited_inference")),
                "Sparse documentation: " + rid)
        require(row["provenance_class"] == "SCREEN_CANON"
                and row["interpretation_class"] == "INFERRED"
                and row["confidence"] in {"HIGH", "MEDIUM", "LOW"}, "Provenance misclassified: " + rid)
        require(bool(row["source_refs"]) and set(row["source_refs"]) <= src, "Source unregistered: " + rid)
        require(set(row["entities"]) <= entities, "Unknown B entity: " + rid)
        require(set(row["locations"]) <= locs.keys(), "Unknown C anchor: " + rid)
        require(set(row["relations"]) <= relations, "Unknown D relation: " + rid)
        t = row["temporal"]
        require(t["precision"] != "EXACT_DAY", "False temporal precision: " + rid)
        if t["not_before_event_id"]:
            require(t["not_before_event_id"] in events, "Unknown event: " + rid)
            require(t["reference_year"] >= events[t["not_before_event_id"]]["reference_year"],
                    "Anachronistic event: " + rid)
        require(row["knowledge"]["requires_observer_projection"] is True
                and row["knowledge"]["is_universal_public_knowledge"] is False
                and row["knowledge"]["access_or_authority_must_be_checked_at_use"] is True,
                "Omniscient record: " + rid)
        require(all(row["runtime"][k] is False for k in
                    ("gameplay_activated", "auto_transition", "ai_can_execute", "delta_dlc_unlock")),
                "Autonomous activation: " + rid)
        require(not any(locs[x]["documentary_availability"] != "MAIN_GAME_REFERENCE"
                        for x in row["locations"]), "Delta location promoted: " + rid)

    case_ids = set()
    require(len(queries["cases"]) == queries["case_count"] >= 12, "Not enough scenarios")
    for case in queries["cases"]:
        require(case["case_id"] not in case_ids, "Duplicate scenario")
        case_ids.add(case["case_id"])
        require(len(case["operational_record_refs"]) >= 2
                and set(case["operational_record_refs"]) <= ids, "Broken case refs")
        require("observer_known_facts" in case["mandatory_context"]
                and "actor_identity_role_and_assignment" in case["mandatory_context"],
                "No observer/role boundary")
        require("ai_direct_world_mutation" in case["forbidden_outputs"]
                and "delta_dlc_activation" in case["forbidden_outputs"]
                and case["result"] == "DOCUMENTARY_CONSULTATION_ONLY", "Executable scenario")
    require({v["phase"] for v in cross["layers"]} == {"A","A.1","B","C","D","E"},
            "Missing A–E crosswalk")
    for layer in cross["layers"]:
        require(all(path_exists(ref) for ref in layer["stable_refs"]), "Broken crosswalk")
    require(all(path_exists(ref) for ref in cross["contracts_not_to_mutate"]),
            "Unknown protected contract")

    require(len(gaps["issues"]) >= 15, "Uncertainty ledger too small")
    require(len({v["issue_id"] for v in gaps["issues"]}) == len(gaps["issues"]),
            "Duplicate uncertainty")
    for q in gaps["issues"]:
        require(path_exists(q["reference"]), "Unknown uncertainty reference")
        if "#" in q["reference"] and q["reference"].split("#")[1].startswith("OP-"):
            require(q["reference"].split("#")[1] in ids, "Broken gap/operational ref")
        require(q["requires_author_decision"] is False
                and q["status"] == "OPEN_DOCUMENTARY_LIMITATION",
                "Unsanctioned canon/decision closure")

    require(len(DELTA & set(gate["main_game"]["species_ids_existing"]
                            + gate["main_game"]["species_ids_added"])) == 0,
            "DLC species imported to main")
    require(set(gate["delta_dlc"]["species_ids"]) == DELTA
            and gate["delta_dlc"]["status"] == "FUTURE_NOT_IMPLEMENTED"
            and gate["delta_dlc"]["default_main_game_spawn_allowed"] is False
            and gate["delta_dlc"]["planned_travel"]["implementation_status"] == "NOT_IN_THIS_PHASE"
            and gate["delta_dlc"]["planned_travel"]["entry_system_id"] is None,
            "Delta gate altered")
    require(all((ROOT / file).is_file() for file in
                (BASE + "/README.md", BASE + "/INTERPRETACIONES_A_H.md",
                 BASE + "/MODELO_DE_CONSULTA.md",
                 "proyecto/docs/roadmap/lore_01_e_global_audit_v0.1.md")), "Missing narrative documentation")
    status = (ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    require("| D — Relaciones diplomáticas | ✅ COMPLETE |" in status, "D not administratively merged")
    require("| E — Información operativa transversal | ✅ COMPLETE |" in status,
            "E already merged in PR #30: administrative closure missing")
    return {"phase_A_species":len(species["profiles"]),"phase_A1_guides":len(culture["profiles"]),
            "phase_B_powers":len(entities),"phase_C_anchors":len(locs),
            "phase_D_relations":len(relations),"phase_D_events":len(events),
            "phase_E_records":len(recs),"phase_E_scenarios":len(case_ids),
            "open_uncertainties":len(gaps["issues"])}

if __name__ == "__main__":
    print("LORE-01 A–E DOCUMENTARY INTEGRITY OK:", validate())
