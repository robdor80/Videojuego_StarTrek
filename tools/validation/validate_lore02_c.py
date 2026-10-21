#!/usr/bin/env python3
"""LORE-02 C: documentary consistency/authority checks. NO gameplay simulation."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATLAS = "lore/medicine/lore02_c_species_clinical_atlas_v0.1.json"
CONDITIONS = "lore/medicine/lore02_c_conditions_v0.1.json"
PROCEDURES = "lore/medicine/lore02_c_procedures_v0.1.json"
ORG = "lore/medicine/lore02_c_facilities_staff_v0.1.json"
SCENARIOS = "lore/medicine/lore02_c_adversarial_scenarios_v0.1.json"
FLOW = "gameplay/medical/lore02_c_diagnostic_workflow_v0.1.json"
REGISTRY = "sources/source_registry/source_registry.json"
DOSSIER = "docs/roadmap/lore_02_c_medicine_research_dossier_v0.1.md"
EQUIPMENT = "lore/equipment/lore02_b_equipment_catalogue_v0.1.json"
AGENTS = "lore/medicine/lore02_c_medical_agents_v0.1.json"
NAMES = (ATLAS, CONDITIONS, PROCEDURES, ORG, SCENARIOS, FLOW, REGISTRY, EQUIPMENT)
STATE = "EDITORIAL_NON_RUNTIME"
EXPECTED = {"species": 26, "conditions": 32, "procedures": 26, "agents": 12,
            "facilities": 9, "roles": 12, "cases": 56}

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def exists(rel):
    return isinstance(rel, str) and bool(rel) and not Path(rel).is_absolute() and ".." not in Path(rel).parts and (ROOT / rel).is_file()

def validate_agents(doc, registry, equipment):
    """Documentary checks for fictional medicines and specialist technologies."""
    errors = []
    def need(ok, msg):
        if not ok:
            errors.append(msg)
    source_types = {x["source_id"]: x["source_type"] for x in registry.get("sources", [])}
    med_eq = {x["equipment_id"] for x in equipment.get("records", [])
              if x.get("family") == "medical"}
    need(doc.get("schema_version") == "0.1.0" and
         doc.get("status") == "NEEDS_REVIEW" and
         doc.get("mode") == "EDITORIAL_NON_RUNTIME", "agent status falsely closed")
    need(doc.get("authority") == "CoreRPG_WORLD_STATE_ONLY", "agent authority leak")
    records = doc.get("records", [])
    need(len(records) == doc.get("record_count") == EXPECTED["agents"], "agent coverage")
    need(len({x.get("agent_id") for x in records}) == len(records), "duplicate agent")
    for a in records:
        name = a.get("agent_id", "?")
        sources = a.get("source_ids", [])
        need(bool(sources) and all(x in source_types for x in sources),
             name + " unknown medicinal source")
        classification = a.get("claim_class")
        need(classification in ("RELIABLE_SECONDARY", "OFFICIAL_REFERENCE", "SCREEN_CANON"),
             name + " invalid medicine authority")
        if classification == "OFFICIAL_REFERENCE":
            need(all(source_types.get(x) in ("OFFICIAL_REFERENCE", "SCREEN_CANON") for x in sources),
                 name + " source classification inflated")
        need(bool(a.get("episodic_indication_es")) and
             bool(a.get("clinical_limitation_es")) and
             len(a.get("required_evidence", [])) >= 6,
             name + " lacks patient-specific clinical limitation")
        need(a.get("species_compatibility") == "UNKNOWN_UNTIL_PATIENT_ASSESSED",
             name + " false universal species compatibility")
        ref = a.get("equipment_ref")
        need(ref is None or ref in med_eq, name + " unregistered medical equipment")
        need(a.get("availability") == "CONTEXTUAL_NOT_GRANTED_BY_CATALOGUE"
             and a.get("administerable_in_game_now") is False
             and a.get("gameplay_treatment_status") == "RESEARCH_REFERENCE_ONLY",
             name + " agent auto-granted or falsely implemented")
        need(a.get("dose", "MISSING") is None and
             a.get("universal_efficacy", "MISSING") is None and
             a.get("time_to_effect", "MISSING") is None,
             name + " invented medical dose/efficacy/timer")
    return errors

def validate_data(atlas, cond, proc, org, cases, flow, registry, eq, check_paths=True):
    errors = []
    def need(value, message):
        if not value:
            errors.append(message)
    for name, obj in ((ATLAS, atlas), (CONDITIONS, cond), (PROCEDURES, proc),
                      (ORG, org), (SCENARIOS, cases)):
        need(obj.get("schema_version") == "0.1.0", "schema: "+name)
        need(obj.get("status") == "NEEDS_REVIEW", "must await human review: "+name)
        need(obj.get("mode") == STATE, "false runtime claim: "+name)
    need(atlas.get("authority") == cond.get("authority") == proc.get("authority")
         == org.get("authority") == "CoreRPG_WORLD_STATE_ONLY", "world authority lost")
    need(flow.get("world_state_authority") == "CoreRPG_ONLY"
         and flow.get("runtime_implemented") is False, "workflow falsely executable")
    need(registry.get("last_updated", "") >= "2026-10-21", "stale provenance registry")
    ids = [s.get("source_id") for s in registry.get("sources", [])]
    source_map = {s.get("source_id"): s for s in registry.get("sources", [])}
    need(len(ids) == len(source_map), "duplicate source ID")
    for x in ("L02C_ST_TRILL", "L02C_ST_MED_ETHICS", "L02C_ST_QUICKENING",
              "L02C_ST_VIDIIAN", "L02C_ST_BENDII", "L02C_ST_MACRO"):
        need(x in source_map, "missing evidence source: " + x)
    need(len(atlas.get("records", [])) == atlas.get("species_count") == EXPECTED["species"],
         "species coverage")
    species = atlas.get("records", [])
    need(len(set(x.get("profile_id") for x in species)) == len(species),
         "duplicate species clinical profile")
    expected_species = [x.get("species_id") for x in species if x.get("species_id")]
    need(len(expected_species) == 25 and len(set(expected_species)) == 25, "taxonomy duplication")
    need(sum(x.get("entity_kind") == "MULTISPECIES_AUGMENTATION_NOT_SPECIES" for x in species) == 1,
         "Borg incorrectly modeled as a species")
    for s in species:
        k = s.get("profile_id","?")
        need(s.get("claim_class") in {"OFFICIAL_REFERENCE", "INFERRED"}, k+" evidence category")
        need(bool(s.get("documented_clinical_relevance_es")) and
             bool(s.get("uncertainty_and_individual_variation_es")), k+" shallow physiological note")
        need(s.get("allow_default_human_reference") is False and
             s.get("normal_vitals", "MISSING") is None and
             s.get("pharmacology", "MISSING") is None and
             s.get("species_specific_doses", "MISSING") is None,
             k+" invented medical numeric baseline")
        need(len(s.get("required_inputs", [])) >= 4, k+" missing individualization")
        need(all(x in source_map for x in s.get("source_ids", [])), k+" unknown source")
        if check_paths:
            need(exists(s.get("evidence_ref")), k+" missing LORE-01 evidence")
        if s.get("species_id"):
            need(s.get("evidence_ref") == "lore/species/evidence/"+s["species_id"]+"_v0.2.json",
                 k+" taxonomy evidence detached")
    equipment = {x.get("equipment_id"):x for x in eq.get("records", [])}
    need(len(eq.get("records", [])) == 73, "equipment B unexpectedly changed")
    need(len(cond.get("catalogue", [])) == cond.get("record_count") == EXPECTED["conditions"],
         "condition coverage")
    need(len(proc.get("records", [])) == proc.get("record_count") == EXPECTED["procedures"],
         "procedure coverage")
    cids = [x.get("condition_id") for x in cond.get("catalogue", [])]
    pids = [x.get("procedure_id") for x in proc.get("records", [])]
    need(len(set(cids)) == len(cids), "duplicate clinical condition")
    need(len(set(pids)) == len(pids), "duplicate clinical procedure")
    valid_classes = {"OFFICIAL_REFERENCE", "SCREEN_CANON", "RELIABLE_SECONDARY", "INFERRED", "GAME_ADDITION"}
    for c in cond.get("catalogue", []):
        key = c.get("condition_id", "?")
        need(c.get("claim_class") in valid_classes, key+" invalid evidence classification")
        need(bool(c.get("observable_clues_es")) and bool(c.get("diagnostic_differential_es"))
             and bool(c.get("scope_note_es")), key+" lacks differential")
        if c.get("claim_class") == "GAME_ADDITION":
            need(not c.get("source_ids"), key+" fake canonical evidence")
        else:
            need(bool(c.get("source_ids")), key+" missing canonical anchor")
        need(all(x in source_map for x in c.get("source_ids", [])), key+" unknown provenance")
        need(c.get("procedure_ref") in pids, key+" missing medical procedure")
        need(c.get("clinical_dose","MISSING") is None
             and c.get("canonical_recovery_time","MISSING") is None,
             key+" invented dosage or timetable")
        need(c.get("information_gate") == "OBSERVER_RESTRICTED"
             and c.get("world_state_authority") == "CoreRPG_ONLY",
             key+" diagnostic omniscience")
    contract = read("lore/medicine/medical_capability_contract.json") if check_paths else {
        "categories": ["diagnostic","treatment","surgery","emergency_care","xenomedicine",
                       "preventive","rehabilitation","medical_imaging","biological_analysis"]}
    categories = set(contract["categories"])
    for p in proc.get("records", []):
        key = p.get("procedure_id", "?")
        need(p.get("category") in categories, key+" violates base capability categories")
        need(p.get("classification") == "GAME_ADDITION", key+" false procedure canon")
        need(all(x in source_map for x in p.get("canon_basis_sources", [])),
             key+" unknown procedure anchor")
        need(bool(p.get("critical_limit_es")) and len(p.get("preconditions", [])) >= 5
             and len(p.get("information_gates", [])) >= 3, key+" lacks medical safeguards")
        need(all(x in equipment and equipment[x].get("family") == "medical"
                 for x in p.get("equipment_refs", [])), key+" unknown or nonmedical equipment")
        need(p.get("real_world_dosing","MISSING") is None
             and p.get("canonical_time_to_effect","MISSING") is None,
             key+" invented real clinical precision")
        need(p.get("ue5_implemented") is False
             and p.get("planned_core_action") == "HOST_VALIDATES_THEN_CORERPG_ACTION",
             key+" bypasses Core or falsely claims UE5")
    need(len(org.get("facilities", [])) == org.get("facility_count") == EXPECTED["facilities"],
         "facility coverage")
    need(len(org.get("professionals", [])) == org.get("professional_count") == EXPECTED["roles"],
         "medical staff coverage")
    for field, code in (("facilities","facility_id"), ("professionals","role_id")):
        seq = org.get(field, [])
        need(len({x.get(code) for x in seq}) == len(seq), "duplicate staff or facility")
    for fac in org.get("facilities", []):
        need(fac.get("auto_spawn") is False and "staff_on_duty" in fac.get("requires_live_state", [])
             and "energy" in fac.get("requires_live_state", []), "facility magic capacity")
        if check_paths:
            need(exists(fac.get("existing_ref")), "detached facility reference")
    for role in org.get("professionals", []):
        need(role.get("role_not_equal_individual_qualification") is True
             and role.get("full_medical_record_access") is False
             and len(role.get("requirements", [])) >= 4, "staff automatic authority")
    need(flow.get("privacy_source_of_truth") == "gameplay/records_and_logs/access_and_privacy_rules.json"
         and flow.get("medical_fitness_source_of_truth") == "lore/federation/starfleet/regulations/medical_authority.json",
         "duplicate/overridden privacy or CMO source")
    steps = flow.get("workflow", [])
    step_ids = [x.get("step_id") for x in steps]
    need(len(steps) == 11 and len(set(step_ids)) == 11
         and all(x.get("requires_current_context") and x.get("result_is_not_arbitrary_ai_decision") for x in steps),
         "diagnostic process bypass")
    need(flow.get("captain_visibility") == "minimum_fitness_and_operational_impact_only"
         and flow.get("ai_context_policy") == "HOST_AUTHORIZED_CONTEXT_ONLY"
         and flow.get("no_universal_dose_or_timers") is True, "medical privacy AI bypass")
    need(len(cases.get("cases", [])) == cases.get("case_count") == EXPECTED["cases"],
         "insufficient adversarial coverage")
    scids = [x.get("case_id") for x in cases.get("cases", [])]
    need(len(scids) == len(set(scids)), "duplicate medical scenario")
    fam = Counter(x.get("family") for x in cases.get("cases", []))
    need(len(fam) >= 12, "missing clinical scenario families")
    for ca in cases.get("cases", []):
        key = ca.get("case_id","?")
        need(not ca.get("condition_ref") or ca["condition_ref"] in cids, key+" unknown case condition")
        need(not ca.get("requested_intervention") or ca["requested_intervention"] in pids,
             key+" unknown case procedure")
        need(all(x in source_map for x in ca.get("source_ids",[])), key+" unknown scenario evidence")
        need(len(ca.get("preconditions",[])) >= 5
             and bool(ca.get("expected_design_response_es"))
             and bool(ca.get("forbidden_response_es")), key+" trivial test scenario")
        need(ca.get("status") == "SPECIFIED_NOT_EXECUTED"
             and ca.get("test_mode") == "NON_RUNTIME_DOCUMENTARY"
             and ca.get("state_authority") == "CoreRPG_ONLY", key+" falsely playtested or mutated")
    if check_paths:
        errors.extend(validate_agents(read(AGENTS), registry, eq))
        for ref in (*NAMES, AGENTS, DOSSIER, "lore/medicine/README.md",
                    "gameplay/medical/medical_state_model.json",
                    "gameplay/medical/species_medical_hooks.json",
                    "gameplay/records_and_logs/access_and_privacy_rules.json",
                    "lore/federation/starfleet/regulations/medical_authority.json"):
            need(exists(ref), "missing canonical reference: "+ref)
        status = (ROOT/"CONTENT_STATUS.md").read_text(encoding="utf-8")
        block = status.split("## LORE-02 —",1)[-1].split("## ",1)[0]
        need("B — Equipamiento personal y especializado | ✅ COMPLETE" in block,
             "LORE-02 B fusion not regularized")
        need("C — Medicina y xenobiología | 🟨 IN_PROGRESS" in block,
             "LORE-02 C falsely closed without author approval")
    return errors

def validate():
    args = [read(x) for x in NAMES]
    errors = validate_data(*args)
    if errors:
        raise AssertionError("\n".join(errors))
    return dict(EXPECTED, mode=STATE, workflow_steps=11, authority="CoreRPG_WORLD_STATE_ONLY")

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))
