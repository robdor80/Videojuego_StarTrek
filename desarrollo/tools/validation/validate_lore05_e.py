#!/usr/bin/env python3
"""LORE-05E: pruebas de consistencia documental; stdlib, sin estado de campaña."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OVERLAY = "mundo/lore/languages/lore05e_reference_overlay_v0.1.json"
CASES = "mundo/lore/exploration/lore05e_acceptance_cases_v0.1.json"
SOURCE = "sistemas/gameplay/languages/initial_language_catalogue.json"
LANGMODEL = "sistemas/gameplay/languages/language_runtime_model.json"
SUBSPACE = "sistemas/gameplay/communications/subspace_communication_contract.json"
GUIDES = [
    "mundo/lore/languages/LORE05E_TRADUCCION_Y_COMUNICACION_20261113.md",
    "mundo/lore/exploration/LORE05E_EXPLORACION_Y_PRIMER_CONTACTO_20261113.md",
    "proyecto/docs/roadmap/lore_05_e/README.md",
]

def load(path: str):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def problems_for_data(d, cases, source, language_model, subspace):
    p=[]
    def bad(s): p.append(s)
    if (d.get("scope"),d.get("campaign_baseline_year"),d.get("world_state_authority"),d.get("kind")) != ("LORE-05E",2383,"CoreRPG_ONLY","DOCUMENTARY_REFERENCE"):
        bad("invalid scope/year/authority/kind")
    for flag in ("runtime_implemented","world_state_mutations","automatic_discoveries","automatic_contact","automatic_diplomacy","automatic_dlc_unlock"):
        if d.get(flag) is not False: bad("unsafe "+flag)
    for k in ("canonical_faction_or_civilization_additions","new_playable_language_definitions"):
        if d.get(k) != 0: bad("new entities forbidden: "+k)
    refs=d.get("source_contracts",{})
    if len(refs)<17 or len(set(refs.values()))!=len(refs):
        bad("incomplete or duplicate source references")
    for key,path in refs.items():
        if not isinstance(path,str) or not (ROOT/path).is_file(): bad("missing reference "+key)
    allowed={x["language_id"]:x for x in source["languages"]}
    overlay=d.get("existing_languages",[])
    if len(overlay)!=8 or {x.get("language_id") for x in overlay}!=set(allowed):
        bad("language ids must reuse the exact eight existing records")
    if len({x.get("language_id") for x in overlay})!=len(overlay):
        bad("duplicate language identity")
    for x in overlay:
        ref=allowed.get(x.get("language_id"),{})
        if x.get("display_name_es")!=ref.get("display_name_es"): bad("language name divergence")
        if x.get("availability_scope") != ref.get("availability_scope"): bad("language availability changed")
        if x.get("source_catalogue_ref")!=SOURCE: bad("language source changed")
        for k in ("auto_assume_fluency","auto_assume_monolingual_species","auto_unlock_dlc"):
            if x.get(k) is not False: bad("unsafe language inference "+k)
    for id_ in ("kazon","talaxian"):
        rec=next((x for x in overlay if x.get("language_id")==id_),{})
        if rec.get("availability_scope")!="DLC_DELTA_FUTURE": bad("Delta DLC gate lost")
    if d.get("translator_states")!=language_model["translation_states"]:
        bad("translator states must exactly preserve owner contract")
    if d.get("channel_states")!=subspace["link_states"]:
        bad("channel states must exactly preserve owner contract")
    rules=d.get("narrative_rules",[])
    if len(rules)!=18 or len({x.get("id") for x in rules})!=18: bad("expected eighteen distinct narrative rules")
    for x in rules:
        if not x.get("area") or len(x.get("rule_es",""))<30: bad("incomplete narrative rule")
    items=cases.get("documentary_cases",[])
    if cases.get("scope")!="LORE-05E" or cases.get("simulation_claimed") is not False:
        bad("cases claim runtime")
    if cases.get("expected_case_count") != 24 or len(items)!=24 or len({x.get("id") for x in items})!=24:
        bad("expected twenty-four distinct cases")
    domains={"LINGUISTIC","TRANSMISSION","FIRST_CONTACT","EXPLORATION","KNOWLEDGE","AUTHORITY"}
    if {x.get("domain") for x in items}!=domains or any(sum(y.get("domain")==d for y in items)!=4 for d in domains):
        bad("expected four cases for each of six areas")
    for x in items:
        if (x.get("kind"),x.get("world_state_mutations"),x.get("core_runtime_test"))!=("DOCUMENTARY_EXPECTED_BEHAVIOR",False,False):
            bad("scenario must be documentary")
        if not x.get("query_es") or not x.get("expected"): bad("missing expected scenario behavior")
    return p

def validate():
    failures=problems_for_data(load(OVERLAY),load(CASES),load(SOURCE),load(LANGMODEL),load(SUBSPACE))
    for path in GUIDES:
        if not (ROOT/path).is_file(): failures.append("missing guide "+path)
    return failures

if __name__=="__main__":
    problems=validate()
    for p in problems: print("ERROR:",p)
    if problems: raise SystemExit(1)
    print("LORE-05E PASS: 8 existing languages, 18 rules, 24 documentary cases, owner contracts unchanged")
