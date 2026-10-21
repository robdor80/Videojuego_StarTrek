#!/usr/bin/env python3
"""LORE-02 B documentary gate. Does not execute UE5 or CoreRPG gameplay."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAT = "lore/equipment/lore02_b_equipment_catalogue_v0.1.json"
PROFILES = "lore/equipment/lore02_b_roles_loadouts_v0.1.json"
CASES = "lore/equipment/lore02_b_adversarial_scenarios_v0.1.json"
REGISTRY = "sources/source_registry/source_registry.json"
DOSSIER = "docs/roadmap/lore_02_b_equipment_research_dossier_v0.1.md"
EXPECTED = {"science": 12, "security": 9, "medical": 9, "engineering": 10,
            "environment": 10, "communications": 7, "alien": 16}

def read(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def exists(rel):
    return (isinstance(rel, str) and rel
            and not Path(rel).is_absolute()
            and ".." not in Path(rel).parts
            and (ROOT / rel).is_file())

def validate_data(cat, profiles, cases, registry, check_paths=True):
    """Pure documentary checks: errors are returned, never silently normalized."""
    errors = []
    def need(value, reason):
        if not value:
            errors.append(reason)

    for obj, name in ((cat, "catalogue"), (profiles, "profiles"), (cases, "cases")):
        need(obj.get("schema_version") == "0.1.0", name + " schema")
        need(obj.get("status") == "NEEDS_REVIEW", name + " must await review")
    need(cat.get("mode") == "EDITORIAL_NON_RUNTIME", "runtime false claim")
    need(cat.get("authority") == "CoreRPG_WORLD_STATE_ONLY", "authority lost")
    need(cat.get("canonical_era_source") == "gameplay/ship_operations/era_technology_matrix.json",
         "duplicate or detached era policy")
    need(cat.get("record_count") == len(cat.get("records", [])) == 73,
         "equipment count")
    need(profiles.get("catalogue") == CAT and cases.get("catalogue") == CAT,
         "broken catalogue link")
    need(len(profiles.get("profiles", [])) == 15, "role coverage")
    need(len(profiles.get("loadout_templates", [])) == 6, "loadout coverage")
    need(cases.get("case_count") == len(cases.get("cases", [])) == 45, "case coverage")
    need(registry.get("last_updated", "") >= "2026-10-21", "source registry stale")
    sourceids = [r.get("source_id") for r in registry.get("sources", [])]
    need(len(sourceids) == len(set(sourceids)), "duplicate source ID")
    sources = set(sourceids)
    for expected_id in ("L02B_MA_TRICORDER", "L02B_MA_PHASER", "L02B_MA_MED_TRICORDER",
                        "L02B_ST_MED_PROPS", "L02B_MA_EV_SUIT", "L02B_MA_COMMS",
                        "L02B_MA_BAJORAN_RIFLE", "L02B_MA_BORG_NANOPROBE"):
        need(expected_id in sources, "missing registered source " + expected_id)

    records = cat.get("records", [])
    ids = [r.get("equipment_id") for r in records]
    need(len(ids) == len(set(ids)), "duplicate equipment IDs")
    need(dict(Counter(r.get("family") for r in records)) == EXPECTED,
         "family counts changed")
    valid_class = {"SOURCE_BOUNDED_INFERENCE", "GAME_ADDITION"}
    for rec in records:
        rid = rec.get("equipment_id", "?")
        for name in ("display_name_es", "role_and_mechanism", "authorization_and_prerequisites",
                     "resource_and_maintenance", "possible_failure", "operator_scope"):
            need(bool(rec.get(name)), rid + " empty " + name)
        need(isinstance(rec.get("proposed_interactions"), list)
             and bool(rec["proposed_interactions"]), rid + " empty interactions")
        need(len(rec.get("operational_state_checks", [])) >= 3,
             rid + " lacks state checks")
        need(rec.get("canonical_numeric_performance", "MISSING") is None,
             rid + " invented performance number")
        runtime = rec.get("runtime", {})
        need(runtime.get("implementation_status") == "NOT_IMPLEMENTED"
             and runtime.get("data_import_allowed") is False
             and runtime.get("ai_world_mutation_allowed") is False,
             rid + " falsely implemented")
        p = rec.get("provenance", {})
        cl = p.get("classification")
        need(cl in valid_class, rid + " wrong provenance classification")
        anchors = p.get("source_ids", [])
        if cl == "SOURCE_BOUNDED_INFERENCE":
            need(bool(anchors) and all(a in sources for a in anchors),
                 rid + " unknown source")
        if cl == "GAME_ADDITION":
            need(not anchors and bool(p.get("design_rationale")),
                 rid + " game addition not separated")
        need(bool(p.get("claim_scope")), rid + " missing claim scope")
        for ref in rec.get("gameplay_consumer_refs", []) + rec.get("object_model_refs", []):
            if check_paths:
                need(exists(ref), rid + " broken consumer reference: " + str(ref))
    known = set(ids)
    profids = [p.get("profile_id") for p in profiles.get("profiles", [])]
    need(len(profids) == len(set(profids)), "duplicate role ID")
    for prof in profiles.get("profiles", []):
        pid = prof.get("profile_id", "?")
        refs = prof.get("typical_equipment_ids", []) + prof.get("conditional_equipment_ids", [])
        need(bool(refs) and all(x in known for x in refs), pid + " unknown equipment")
        need(prof.get("never_implies") == "NO_AUTO_GRANT_OR_STATE_MUTATION",
             pid + " automatic grant")
        need(len(prof.get("decision_order", [])) >= 5, pid + " insufficient issue guards")
    for kit in profiles.get("loadout_templates", []):
        need(all(x in profids for x in kit.get("profile_refs", [])),
             str(kit.get("loadout_id")) + " unknown profile")
        need(kit.get("authority") == "AUTHORING_GUIDANCE_NOT_INVENTORY",
             str(kit.get("loadout_id")) + " automatic inventory")
    caseids = [c.get("case_id") for c in cases.get("cases", [])]
    need(len(caseids) == len(set(caseids)), "duplicate case IDs")
    family_tested = set()
    by_id = {r.get("equipment_id"): r for r in records}
    for case in cases.get("cases", []):
        key = case.get("case_id", "?")
        cid = case.get("equipment_id")
        need(cid in known, key + " missing equipment")
        if cid in by_id:
            family_tested.add(by_id[cid]["family"])
        need(bool(case.get("scenario")) and bool(case.get("expected_design_response"))
             and bool(case.get("forbidden_response")), key + " incomplete failure test")
        need(case.get("status") == "SPECIFIED_NOT_EXECUTED"
             and case.get("test_mode") == "NON_RUNTIME_DOCUMENTARY",
             key + " falsely executed")
        need("CoreRPG" in case.get("core_policy", ""), key + " authority omitted")
    need(family_tested == set(EXPECTED), "missing adversarial family")
    if check_paths:
        for p in [CAT, PROFILES, CASES, REGISTRY, DOSSIER,
                  "gameplay/ship_operations/era_technology_matrix.json",
                  "gameplay/characters/character_runtime_model.json",
                  "gameplay/inventory/persistent_unique_object_contract.json",
                  "gameplay/logistics/resource_inventory_state.json"]:
            need(exists(p), "missing anchor: " + p)
        status = (ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
        section = status.split("## LORE-02 —", 1)[-1].split("## ", 1)[0]
        need("A — Tecnología de naves y estaciones | ✅ COMPLETE" in section,
             "merged A not regularized")
        need("B — Equipamiento personal y especializado | ✅ COMPLETE" in section,
             "merged B not regularized")
    return errors

def validate():
    errors = validate_data(read(CAT), read(PROFILES), read(CASES), read(REGISTRY))
    if errors:
        raise AssertionError("\n".join(errors))
    return {"equipment": 73, "families": len(EXPECTED), "profiles": 15,
            "loadouts": 6, "adversarial": 45, "mode": "EDITORIAL_NON_RUNTIME"}

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))
