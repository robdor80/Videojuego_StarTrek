#!/usr/bin/env python3
"""LORE-01 D: valida documentos, no simula diplomacia ni avala visión de escenas."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "lore/diplomacy"
FILES = [
    "relation_index_v0.1.json", "relation_evidence_v0.1.json",
    "historical_events_v0.1.json", "agreements_conflicts_v0.1.json",
    "geopolitical_layers_v0.1.json", "player_npc_cases_v0.1.json",
    "open_questions_v0.1.json",
]
DELTA = {"kazon", "ocampan", "talaxian", "vidiian", "hirogen"}

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def check(ok, message):
    if not ok:
        raise AssertionError(message)

def validate():
    data = {name: load("lore/diplomacy/" + name) for name in FILES}
    b = load("lore/factions/LORE01_B_civilizations_index_v0.1.json")
    known = {e["civilization_id"] for e in b["main_game_entries"]}
    registry = {e["source_id"] for e in load("sources/source_registry/source_registry.json")["sources"]}
    check(len(known) == 16, "LORE-01 B base changed")
    for name, block in data.items():
        check(block["authority"] == "CoreRPG_World_State_ONLY", name + " authority")
        check(block["status"] == "DOCUMENTARY_NOT_RUNTIME", name + " runtime activation")
        check(block["gameplay_activated"] is False and block["autonomous_future_script"] is False, name + " automatic activation")
    index = data[FILES[0]]
    evidence = data[FILES[1]]
    events = data[FILES[2]]
    other = data[FILES[3]]
    geo = data[FILES[4]]
    cases = data[FILES[5]]
    questions = data[FILES[6]]
    check(set(index["entity_ids"]) == known, "16 identities not preserved")
    rels = evidence["relations"]
    relids = {e["relation_id"] for e in rels}
    check(len(relids) == len(rels) == index["relation_count"] == evidence["relation_count"], "Duplicate/missing relationship")
    check({x["relation_id"] for x in index["relations"]} == relids, "Index/evidence mismatch")
    eventids = {x["event_id"] for x in events["events"]}
    check(len(eventids) == events["event_count"] == len(events["events"]), "Duplicate event")
    check(not (known & DELTA), "Delta species imported to B")
    for rel in rels:
        check(len(rel["participants"]) == 2 and set(rel["participants"]) <= known, "Foreign entity or invalid pair")
        check(rel["gameplay_activated"] is False and rel["canonical_future_not_guaranteed"] is True, "Forced canon future")
        check(set(rel["source_refs"]) <= registry, "Unknown relation source")
        path = BASE / "dossiers" / (rel["relation_id"] + "_v0.1.md")
        check(path.is_file() and len(path.read_text(encoding="utf-8")) > 800, "Missing or sparse dossier " + rel["relation_id"])
        for anchor in rel["anchors"]:
            check(anchor["precision"] != "EXACT_DAY", "False date precision")
            check(anchor["effective_after_event_id"] in eventids, "Missing event")
            check(anchor["automatic_future_transition"] is False, "Forced timeline")
            check(set(anchor["source_refs"]) <= registry, "Unknown anchor source")
    for event in events["events"]:
        check(set(event["source_refs"]) <= registry, "Unknown chronology source")
        check(set(event["relation_refs"]) <= relids, "Chronology relation broken")
        check(event["is_compulsory_future_script"] is False, "Future episode forced")
        if event["event_id"] == "tzenkethi_false_coup_report":
            check(event["status"] == "FALSE_CLAIM_NOT_HISTORICAL_EVENT", "Tzenkethi false coup asserted")
    for entry in other["agreements"]:
        check(set(entry["parties"]) <= known, "Unknown treaty party")
        check(set(entry["source_refs"]) <= registry, "Unregistered agreement source")
        check(entry["automatic_campaign_activation"] is False and entry["precise_border_geometry"] is None, "Treaty imported to runtime")
    for entry in other["conflicts"]:
        check(set(entry["participants"]) <= known and set(entry["source_refs"]) <= registry, "Invalid conflict")
        check(entry["gameplay_runtime_definition"] is False, "Conflict simulation added")
    check(geo["no_political_polygons"] is True, "Political polygon invented")
    for entry in geo["layers"]:
        check(entry["geometry"] is None and not entry["automatic_world_state_mutation"], "Political geometry/mutation")
        check(set(entry["source_refs"]) <= registry, "Unregistered geo source")
    for case in cases["cases"]:
        check(set(case["source_refs"]) <= registry, "Unregistered NPC source")
        check(not any(case[k] for k in ("ai_can_mutate_world_state", "auto_create_treaty", "auto_declare_war", "auto_rewrite_border", "delta_dlc_unlock")), "AI bypass")
    check(len(questions["issues"]) >= 10, "Not enough uncertainties")
    status=(ROOT/"CONTENT_STATUS.md").read_text(encoding="utf-8")
    check("| C — Cartografía/astrogeografía | ✅ COMPLETE |" in status, "C closure missing")
    check("| D — Relaciones diplomáticas | ✅ COMPLETE |" in status, "D merged closure missing")
    return {"relations":len(rels),"events":len(eventids),"agreements":len(other["agreements"]),"conflicts":len(other["conflicts"]),"cases":len(cases["cases"])}

if __name__ == "__main__":
    print("LORE-01 D OK", validate())
