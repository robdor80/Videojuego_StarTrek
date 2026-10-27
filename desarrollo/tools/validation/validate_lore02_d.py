#!/usr/bin/env python3
"""LORE-02 D documentary gate. No runtime science or CoreRPG import."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "mundo/lore/science/"
FILES = {
    "disciplines": BASE + "lore02_d_disciplines_v0.1.json",
    "phenomena": BASE + "lore02_d_phenomena_atlas_v0.1.json",
    "methods": BASE + "lore02_d_research_methods_v0.1.json",
    "facilities": BASE + "lore02_d_facilities_roles_v0.1.json",
    "cases": BASE + "lore02_d_research_cases_v0.1.json",
    "legacy": BASE + "lore02_d_scientific_legacy_policy_v0.1.json",
    "adversarial": BASE + "lore02_d_adversarial_scenarios_v0.1.json",
    "registry": "mundo/sources/source_registry/source_registry.json",
    "tech": "mundo/lore/technology/lore02_a_system_atlas_v0.2.json",
    "equipment": "mundo/lore/equipment/lore02_b_equipment_catalogue_v0.1.json",
    "medical": "mundo/lore/medicine/lore02_c_facilities_staff_v0.1.json",
    "status": "CONTENT_STATUS.md",
}
EXPECTED = {"disciplines": 14, "phenomena": 20, "methods": 9,
            "facilities": 6, "roles": 10, "cases": 10, "adversarial": 40}
PROVENANCE = {"SCREEN_CANON", "OFFICIAL_REFERENCE", "INFERRED", "GAME_ADDITION"}
SOURCE_RANK = {"SCREEN_CANON", "OFFICIAL_REFERENCE", "LICENSED_NOVEL",
               "LICENSED_COMIC", "RELIABLE_SECONDARY", "GENERAL_WEB"}
APPROVED_STATES = {"UNKNOWN", "PENDING_REPLICATION", "INCONCLUSIVE", "DISPUTED",
                   "UNRESOLVED", "REJECTED_SAMPLE", "CASE_SPECIFIC"}
ANCHORS = ["mundo/lore/science/scientific_domain_contract.json",
           "sistemas/gameplay/science/sensor_analysis_model.json",
           "mundo/lore/astrography/atlas/anchor_atlas_v0.1.json",
           "mundo/lore/operations/cross_layer_reference_v0.1.json",
           "proyecto/docs/roadmap/lore_02_d_science_research_dossier_v0.1.md",
           "proyecto/docs/decisions/lore_to_game_rule.md",
           "proyecto/docs/decisions/lore_02_d_author_decisions_v0.1.md",
           "mundo/lore/medicine/lore02_c_conditions_v0.1.json",
           "sistemas/gameplay/ship_operations/era_technology_matrix.json"]

def read(path: str):
    if path == FILES["status"]:
        return (ROOT / path).read_text(encoding="utf-8")
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def inputs():
    return {key: read(path) for key, path in FILES.items()}

def file_exists(path):
    return isinstance(path, str) and bool(path) and not Path(path).is_absolute() and ".." not in Path(path).parts and (ROOT / path).is_file()

def validate_data(d, *, check_paths=True):
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
    for key in ("disciplines", "phenomena", "methods", "facilities", "cases", "adversarial", "legacy"):
        doc = d[key]
        need(doc.get("schema_version") == "0.1.0", key + ": schema")
        need(doc.get("phase") == "LORE-02 D", key + ": wrong phase")
        need(doc.get("status") == "NEEDS_REVIEW", key + ": premature approval")
        need(doc.get("mode") == "EDITORIAL_NON_RUNTIME" and
             doc.get("authority") == "CoreRPG_WORLD_STATE_ONLY" and
             doc.get("runtime_import_allowed") is False, key + ": authority leak")
    sources = d["registry"].get("sources", [])
    source_ids = [x.get("source_id") for x in sources]
    need(len(source_ids) == len(set(source_ids)), "duplicate source ID")
    s_types = {x.get("source_id"): x.get("source_type") for x in sources}
    need(len(s_types) >= 487, "source registry truncated")
    def provenance(item, ident):
        p = item.get("provenance", {})
        cl = p.get("claim_class")
        refs = p.get("source_ids", [])
        need(cl in PROVENANCE, ident + ": invalid provenance class")
        need(p.get("confidence") in ("HIGH","MEDIUM","LOW"), ident + ": invalid confidence")
        need(bool(p.get("claim_scope_es")), ident + ": missing source claim scope")
        need(isinstance(refs, list), ident + ": invalid source refs")
        if not isinstance(refs, list):
            return
        need(all(r in s_types for r in refs), ident + ": unknown source")
        if cl == "SCREEN_CANON":
            need(any(s_types.get(r) == "SCREEN_CANON" for r in refs), ident + ": inflated screen canon")
        if cl == "OFFICIAL_REFERENCE":
            need(bool(refs) and all(s_types.get(r) in ("SCREEN_CANON","OFFICIAL_REFERENCE") for r in refs), ident + ": inflated official")
        if cl == "INFERRED":
            need(bool(refs), ident + ": unsourced inference")
        if cl == "GAME_ADDITION":
            need(not refs, ident + ": game addition impersonates source")
    def collect(doc_key, array_key, id_key, count, name):
        entries = d[doc_key].get(array_key, [])
        need(isinstance(entries, list), name + ": malformed records")
        if not isinstance(entries, list):return []
        keys = [x.get(id_key) for x in entries]
        need(len(entries) >= count, name + ": record count below approved baseline")
        need(len(keys) == len(set(keys)) and all(isinstance(k, str) and k.startswith("l02d_") for k in keys),
             name + ": duplicate/bad ID")
        for row in entries:
            provenance(row, str(row.get(id_key)))
        return entries
    disciplines = collect("disciplines", "records", "discipline_id", EXPECTED["disciplines"], "disciplines")
    methods = collect("methods", "records", "method_id", EXPECTED["methods"], "methods")
    phenomena = collect("phenomena", "records", "phenomenon_id", EXPECTED["phenomena"], "phenomena")
    facilities = collect("facilities", "facilities", "facility_id", EXPECTED["facilities"], "facilities")
    roles = collect("facilities", "roles", "role_id", EXPECTED["roles"], "roles")
    cases = collect("cases", "records", "case_id", EXPECTED["cases"], "cases")
    scenarios = collect("adversarial", "records", "scenario_id", EXPECTED["adversarial"], "adversarial")
    for key, doc_key, arr in (
        ("disciplines","disciplines",disciplines),("phenomena","phenomena",phenomena),
        ("methods","methods",methods),("cases","cases",cases),
        ("adversarial","adversarial",scenarios)):
        need(d[doc_key].get("record_count") == len(arr), key + ": inconsistent record_count")
    need(d["facilities"].get("facility_count") == len(facilities) and
         d["facilities"].get("role_count") == len(roles), "staff/facility count")
    dids = {x["discipline_id"] for x in disciplines}
    mids = {x["method_id"] for x in methods}
    pids = {x["phenomenon_id"] for x in phenomena}
    rids = {x["role_id"] for x in roles}
    tids = {x["technology_id"] for x in d["tech"].get("records", [])}
    eids = {x["equipment_id"] for x in d["equipment"].get("records", [])}
    need(len(tids) >= 40 and len(eids) >= 73, "LORE-02 A/B regressions")
    need(len(d["medical"].get("facilities", [])) >= 9, "LORE-02 C regression")
    for x in disciplines:
        name = x.get("discipline_id", "?")
        need(x.get("runtime_enabled") is False and
             x.get("academy_or_staff_training") == "QUALIFICATION_CHECK_FUTURE", name + ": auto qualification")
        need(bool(x.get("observables")) and bool(x.get("epistemic_limit_es")),name + ": omniscient discipline")
    for x in methods:
        name = x.get("method_id","?")
        need(x.get("no_omniscience") is True and bool(x.get("known_failure_modes")),name + ": magical method")
        need(len(x.get("required_observations", []))>=2, name + ": evidence missing")
    for x in phenomena:
        name=x.get("phenomenon_id","?")
        need(bool(x.get("discipline_refs")) and all(r in dids for r in x.get("discipline_refs", [])),
             name+": orphan discipline")
        need(all(r in tids for r in x.get("technology_refs", [])),name+": orphan technology")
        need(all(r in eids for r in x.get("equipment_refs", [])),name+": orphan equipment")
        need(bool(x.get("observables")) and bool(x.get("hypothesis_alternatives")) and
             len(x.get("measurement_requirements",[]))>=4,name+": ungrounded analysis")
        need(x.get("knowledge_state") == "UNKNOWN_UNTIL_EVIDENCE",name+": hidden truth leak")
        need(x.get("presence_rule") == "CAN_EXIST_WITHOUT_PLAYER_INTERACTION",name+": player dependency")
        need(x.get("encounter_rule") == "NO_FORCED_MISSION_OR_THREAT",name+": forced mission")
        need(x.get("default_disposition") in ("not_intrinsically_hostile","context_dependent","hazard_if_confirmed"),
             name+": forced hostility")
        need(x.get("mechanics_status") == "PROPOSAL_ONLY_NOT_EXECUTABLE" and
             x.get("numeric_strength","ABSENT") is None and
             x.get("guaranteed_resolution","ABSENT") is None,name+": fabricated numeric/runtime")
        need(bool(x.get("source_bound_notice")),name+": missing epistemic warning")
    for x in facilities:
        name=x.get("facility_id","?")
        need(all(r in tids for r in x.get("technology_refs",[])),name+": orphan technology")
        need(all(r in eids for r in x.get("equipment_refs",[])),name+": orphan equipment")
        need(x.get("not_auto_spawned") is True and x.get("not_auto_operational") is True,
             name+": auto facility")
        need(len(x.get("required_live_checks",[]))>=5,name+": missing operational checks")
        if check_paths:need(file_exists(x.get("existing_ref")),name+": nonexistent existing_ref")
    for x in roles:
        name=x.get("role_id","?")
        need(x.get("no_inherent_command_authority") is True and
             x.get("not_auto_staffed") is True and x.get("access_policy")=="OBSERVER_NEED_TO_KNOW",
             name+": auto staff/access")
    for x in cases:
        name=x.get("case_id","?")
        need(x.get("phenomenon_ref") in pids,name+": orphan phenomenon")
        need(all(r in mids for r in x.get("method_refs",[])),name+": orphan method")
        need(all(r in rids for r in x.get("specialist_refs",[])),name+": orphan role")
        need(len(x.get("hypotheses_es",[]))>=2 and len(x.get("observations_es",[]))>=1,
             name+": no competing hypothesis")
        need(x.get("epistemic_assessment") in APPROVED_STATES,name+": fabricated conclusion")
        need(x.get("observer_view")=="PARTIAL_ONLY" and
             x.get("world_truth")=="NOT_ENCODED_IN_PUBLIC_CASE" and
             x.get("subject_can_be_offscreen") is True and
             x.get("false_positive_possible") is True,name+": hidden truth/offscreen")
    for x in scenarios:
        name=x.get("scenario_id","?")
        need(bool(x.get("injected_fault")) and bool(x.get("expected_guardrail")) and
             x.get("no_simulation_claim") is True,name+": invalid adversarial scenario")
    wf=d["methods"].get("workflow_states",[])
    need(wf[:2]==["QUESTION","OBSERVATION_REQUESTED"] and "INCONCLUSIVE_OR_REVISED" in wf,
         "scientific workflow knowledge leap")
    # Approved author decisions and future scientific legacy (not runtime).
    legacy = d["legacy"]
    choices = legacy.get("author_decisions", {})
    need(choices.get("scientific_catalogue") == "EXTENSIBLE" and
         choices.get("autonomous_science") == "YES" and
         choices.get("consequences") == "PERSISTENT_PROPORTIONATE",
         "legacy: author decisions")
    access = legacy.get("player_accessibility", {})
    need(access.get("captain_science_expertise_required") is False and
         access.get("real_world_formulas_required") is False and
         access.get("science_career_has_optional_depth") is True and
         access.get("scientists_present_findings_in_clear_language") is True,
         "legacy: required real-world science")
    stages = legacy.get("scientific_research_technology_transfer", [])
    stage_ids = [s.get("id") for s in stages]
    required_stages = ["DISCOVERY", "SUSTAINED_RESEARCH", "INDEPENDENT_VALIDATION",
                       "FLEET_EVALUATION", "ENGINEERING_ADAPTATION",
                       "SHIPYARD_INSTALLATION", "POST_REFIT_TRIALS",
                       "OPTIONAL_GRADUAL_FLEET_ADOPTION"]
    need(stage_ids == required_stages and all(s.get("may_fail") is True for s in stages),
         "legacy: incomplete shipyard transfer")
    leg = legacy.get("scientific_legacy", {})
    need(leg.get("can_name_after_discoverer") is True and
         leg.get("naming_is_not_automatic") is True and
         leg.get("official_name_requires_approval") is True and
         leg.get("recognized_team_credits_possible") is True,
         "legacy: automatic naming or missing attribution")
    need(leg.get("names_survive_years_passed") is True and
         leg.get("names_survive_character_career_change") is True and
         leg.get("conversation_requires_actor_knowledge") is True and
         leg.get("ship_must_have_commissioned_technology_to_claim_its_function") is True,
         "legacy: fictional fame or uninstalled technology")
    persistence = legacy.get("persistent_entities_future_contract", {})
    need(all(k in persistence and len(persistence[k]) >= 3
             for k in ("discovery", "technology", "ship_installation", "legacy")),
         "legacy: missing persistence concepts")
    exceptions = legacy.get("exception_rules", {})
    need(exceptions.get("playable_time_travel_allowed") is False and
         exceptions.get("time_travel_technology_unlock_allowed") is False,
         "legacy: playable time travel")
    omega = exceptions.get("omega", {})
    need(omega.get("author_mandatory_special_mission") is True and
         omega.get("minimum_authored_special_missions", 0) >= 1 and
         omega.get("mission_automatically_triggered_by_every_omega_observation") is False and
         omega.get("classified_information_access_required") is True and
         omega.get("normal_tech_transfer_allowed") is False,
         "legacy: omega mission or classification")
    worm = exceptions.get("wormholes", {})
    need(worm.get("traversal_allowed") is True and
         worm.get("rarity") == "RARE" and
         worm.get("routine_random_shortcuts_allowed") is False and
         worm.get("requires_valid_astrography_link") is True,
         "legacy: wormhole transit rarity")
    core = legacy.get("core_and_presentation", {})
    need(core.get("CoreRPG") == "sole_authority_for_knowledge_technology_ship_modifications_and_time" and
         core.get("AI") == "dialogue_from_actor_permitted_knowledge_only",
         "legacy: authority leak")
    if check_paths:
        need(file_exists(legacy.get("decision_ref")), "legacy: decision reference missing")
    st=d["status"]
    need("| C — Medicina y xenobiología | ✅ COMPLETE |" in st,"C status not regularized")
    need("| D — Ciencia y fenómenos | ✅ COMPLETE |" in st,"D merge not regularized")
    need("| E — Integración y auditoría A–D | ✅ COMPLETE |" in st,"E documentary closure not regularized")
    if check_paths:
        for anchor in ANCHORS:
            need(file_exists(anchor),"missing dependency: "+anchor)
        need(file_exists("mundo/lore/science/README.md"),"missing science index")
        need(file_exists(".github/workflows/lore02-d-science.yml"),"missing science CI")
    return errors

def validate():
    d = inputs()
    errors = validate_data(d)
    if errors:
        raise AssertionError("\n".join(errors))
    return {
        "disciplines": len(d["disciplines"]["records"]),
        "phenomena": len(d["phenomena"]["records"]),
        "methods": len(d["methods"]["records"]),
        "facilities": len(d["facilities"]["facilities"]),
        "roles": len(d["facilities"]["roles"]),
        "cases": len(d["cases"]["records"]),
        "adversarial": len(d["adversarial"]["records"]),
    }

if __name__ == "__main__":
    print("LORE02-D VALID:", validate())
