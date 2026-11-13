#!/usr/bin/env python3
"""LORE-05D: validación documental sin dependencias ajenas a Python stdlib."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ENTITY = "mundo/lore/operations/lore05d_entities_v0.1.json"
CASES = "mundo/lore/operations/lore05d_validation_cases_v0.1.json"
SHIPS = "mundo/lore/starships/individual_ships/core_canonical_ships.json"
CLASSES = "mundo/lore/starships/classes/core_starship_classes.json"
PROJECT = "mundo/lore/starships/individual_ships/project_valhalla_enterprise_d_v0.1.json"
FACILITIES = "mundo/lore/stations_and_facilities/canonical_unique_facilities_v0.1.json"
DESIGNS = "mundo/lore/stations_and_facilities/canonical_station_design_catalogue_v0.1.json"
FACTIONS = "sistemas/gameplay/diplomacy/major_faction_catalogue.json"
REGISTRY = "mundo/sources/source_registry/source_registry.json"
GUIDE = "mundo/lore/operations/LORE05D_NAVES_INSTALACIONES_ORGANIZACIONES_20261113.md"
INDEX = "proyecto/docs/roadmap/lore_05_d/README.md"

def load(path: str):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def problems_for_data(d, cases, ships, classes, project, facilities, designs, factions, registry):
    problems=[]
    def problem(message): problems.append(message)
    if (d.get("scope"),d.get("campaign_baseline_year"),d.get("world_state_authority"))!=("LORE-05D",2383,"CoreRPG_ONLY"):
        problem("wrong scope/year/CoreRPG boundary")
    for flag in ("runtime_implemented","live_state_mutations","automatic_world_spawns","automatic_missions"):
        if d.get(flag) is not False: problem("unsafe top-level flag: "+flag)
    source_ids={x["source_id"] for x in registry["sources"]}
    ship_map={x["ship_id"]:x for x in ships["ships"]}
    class_ids={x["class_id"] for x in classes["classes"]}
    facility_map={x["facility_id"]:x for x in facilities["facilities"]}
    design_ids={x["design_id"] for x in designs["designs"]}
    faction_map=factions["factions"]
    ship_entries=d.get("ships",[])
    facility_entries=d.get("facilities",[])
    faction_entries=d.get("factions",[])
    if len(ship_entries)!=8 or {x.get("ship_id") for x in ship_entries}!=set(ship_map): problem("ships must match existing 8 unique IDs")
    if len(facility_entries)!=12 or {x.get("facility_id") for x in facility_entries}!=set(facility_map): problem("facilities must match reserved 12 unique IDs")
    if len(faction_entries)!=8 or {x.get("faction_id") for x in faction_entries}!=set(faction_map): problem("factions must match catalogue 8 unique IDs")
    if any(d.get(k)!=n for k,n in (("ship_count",8),("facility_count",12),("faction_count",8))): problem("declared counts wrong")
    for x in ship_entries:
        sid=x.get("ship_id","?")
        base=ship_map.get(sid,{})
        if x.get("class_id") != base.get("class_id") or x.get("class_id") not in class_ids: problem(sid+" incorrect class")
        if x.get("registry")!=base.get("registry") or x.get("registry_history") != base.get("registry_history"): problem(sid+" changed registry")
        if x.get("operator_reference")!=base.get("operator"): problem(sid+" changed operator")
        if set(x.get("provenance_refs",[])) - source_ids: problem(sid+" invalid source")
        for flag in ("world_state_known","auto_spawn","auto_assign_to_player","automatic_command_authority"):
            if x.get(flag) is not False: problem(sid+" unsafe flag "+flag)
        if not x.get("narrative_use") or not x.get("prohibited_inference") or not x.get("documentary_state_2383"): problem(sid+" incomplete narrative")
    by_ship={x.get("ship_id"):x for x in ship_entries}
    ent=by_ship.get("uss_enterprise_ncc_1701_d",{})
    defiant=by_ship.get("uss_defiant_nx_74205",{})
    if ent.get("class_id") != "galaxy" or ent.get("registry")!="NCC-1701-D" or ent.get("documentary_state_2383")!="PROYECTO_RECONSTRUCCION":
        problem("Enterprise D is Galaxy reconstruction project")
    if project.get("subject",{}).get("ship_id")!="uss_enterprise_ncc_1701_d" or project.get("project",{}).get("project_id")!="project_valhalla":
        problem("DEC-0020 source has changed")
    if defiant.get("documentary_state_2383")!="DESTRUIDA_ANTES_2383":
        problem("original Defiant NX-74205 cannot be active")
    for sid in ("uss_enterprise_ncc_1701","uss_enterprise_ncc_1701_a","uss_reliant_ncc_1864","uss_grissom_ncc_638"):
        if by_ship.get(sid,{}).get("documentary_state_2383")!="SOLO_REFERENCIA_HISTORICA":
            problem(sid+" historic ship suddenly active")
    for x in facility_entries:
        fid=x.get("facility_id","?")
        base=facility_map.get(fid,{})
        if x.get("design_ref")!=base.get("design_ref") or (x.get("design_ref") and x["design_ref"] not in design_ids):
            problem(fid+" invalid design")
        if x.get("identity_policy")!=base.get("identity_policy") or x.get("retained_playable_profiles")!=base.get("playable_profiles"):
            problem(fid+" identity/era mismatch")
        if set(x.get("source_refs",[]))-source_ids: problem(fid+" invalid source refs")
        for flag in ("unique_identity_respected",):
            if x.get(flag) is not True: problem(fid+" not reserved")
        for flag in ("auto_generate_duplicate","automatically_service_player"):
            if x.get(flag) is not False: problem(fid+" unsafe auto service")
        for field in ("operator_current","owner_current","inventory_current","staff_current","dock_capacity_current"):
            if x.get(field) is not None: problem(fid+" invented live facility state")
        if not x.get("narrative_use_and_limits") or not x.get("documentary_state_2383"): problem(fid+" lacks narrative")
    facmap={x.get("facility_id"):x for x in facility_entries}
    for fid in ("canon:facility:starbase_1","canon:facility:deep_space_station_k7","canon:facility:regula_i"):
        if facmap.get(fid,{}).get("documentary_state_2383")!="SOLO_REFERENCIA_HISTORICA":
            problem(fid+" historical-only unvalidated 2383")
    for x in faction_entries:
        id_=x.get("faction_id","?")
        base=faction_map.get(id_,{})
        if x.get("type")!=base.get("type") or x.get("display_name_es")!=base.get("display_name_es"):
            problem(id_+" faction identity mismatch")
        if x.get("organization_profile_refs")!=base.get("organization_profile_refs",[]):
            problem(id_+" lost profile refs")
        for path in x.get("organization_profile_refs",[]):
            if not (ROOT/path).is_file(): problem(id_+" missing profile")
        for f in ("jurisdiction_current","diplomatic_status_current","active_leadership_current"):
            if x.get(f) is not None: problem(id_+" fabricated current political state")
        for flag in ("automatic_treaty_or_war","automatic_membership"):
            if x.get(flag) is not False: problem(id_+" unauthorized mutation")
        if not x.get("documentary_interpretation_2383"): problem(id_+" empty interpretation")
    inst=d.get("institution_profiles",[])
    if len(inst)!=2 or {i.get("institution_id") for i in inst}!={"starfleet","federation_civil_government"}:
        problem("Federation government and Starfleet not distinguished")
    for i in inst:
        if not (ROOT/i.get("profile_ref","NON_EXISTENT")).is_file(): problem("missing institution profile")
    case_rows=cases.get("documentary_cases",[])
    if len(case_rows)!=18 or len({x.get("id") for x in case_rows})!=18: problem("expected 18 unique cases")
    if cases.get("simulation_claimed") is not False: problem("runtime claimed by cases")
    for x in case_rows:
        if x.get("kind")!="DOCUMENTARY_EXPECTED_BEHAVIOR" or x.get("world_state_mutations") is not False or x.get("core_runtime_test") is not False or not x.get("expected"):
            problem("invalid case")
    return problems

def validate():
    p=problems_for_data(load(ENTITY),load(CASES),load(SHIPS),load(CLASSES),load(PROJECT),load(FACILITIES),load(DESIGNS),load(FACTIONS),load(REGISTRY))
    for path in (GUIDE,INDEX):
        if not (ROOT/path).is_file(): p.append("missing documentation "+path)
    return p

if __name__=="__main__":
    failures=validate()
    for message in failures: print("ERROR:", message)
    if failures: raise SystemExit(1)
    print("LORE-05D PASS: 8 naves, 12 instalaciones, 8 facciones, 2 instituciones, 18 casos — documental")
