#!/usr/bin/env python3
"""LORE-02 E: cross-domain documentary consistency gate. No runtime integration."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "technology": "lore/technology/lore02_a_system_atlas_v0.2.json",
    "legacy_technology": "lore/technology/ship_station_catalogue_v0.1.json",
    "operators": "lore/technology/lore02_a_operator_facility_profiles_v0.2.json",
    "equipment": "lore/equipment/lore02_b_equipment_catalogue_v0.1.json",
    "loadouts": "lore/equipment/lore02_b_roles_loadouts_v0.1.json",
    "conditions": "lore/medicine/lore02_c_conditions_v0.1.json",
    "procedures": "lore/medicine/lore02_c_procedures_v0.1.json",
    "agents": "lore/medicine/lore02_c_medical_agents_v0.1.json",
    "medical_matrix": "lore/medicine/lore02_c_clinical_decision_matrix_v0.1.json",
    "species": "lore/medicine/lore02_c_species_clinical_atlas_v0.1.json",
    "medical_facilities": "lore/medicine/lore02_c_facilities_staff_v0.1.json",
    "civilizations": "lore/medicine/lore02_c_civilization_medical_profiles_v0.1.json",
    "disciplines": "lore/science/lore02_d_disciplines_v0.1.json",
    "phenomena": "lore/science/lore02_d_phenomena_atlas_v0.1.json",
    "methods": "lore/science/lore02_d_research_methods_v0.1.json",
    "science_facilities": "lore/science/lore02_d_facilities_roles_v0.1.json",
    "science_cases": "lore/science/lore02_d_research_cases_v0.1.json",
    "legacy_policy": "lore/science/lore02_d_scientific_legacy_policy_v0.1.json",
    "source_registry": "sources/source_registry/source_registry.json",
    "status": "CONTENT_STATUS.md",
}

REQUIRED_ANCHORS = [
    "docs/decisions/lore_02_d_author_decisions_v0.1.md",
    "docs/decisions/lore_to_game_rule.md",
    "docs/roadmap/lore_02_master_plan_v0.1.md",
    "docs/roadmap/master/AUDITORIA_F07_F15_2026-10-15.md",
    "docs/roadmap/lore_01_e_global_audit_v0.1.md",
    "lore/operations/cross_layer_reference_v0.1.json",
    "gameplay/ship_operations/era_technology_matrix.json",
    "gameplay/ship_operations/system_state_model.json",
    "gameplay/ship_operations/sensor_resolution/sensor_result_contract.json",
    "gameplay/medical/medical_state_model.json",
    "gameplay/medical/lore02_c_diagnostic_workflow_v0.1.json",
    "gameplay/records_and_logs/access_and_privacy_rules.json",
    "gameplay/science/sensor_analysis_model.json",
    "gameplay/inventory/persistent_unique_object_contract.json",
    "gameplay/logistics/resource_inventory_state.json",
    ".github/workflows/lore02-a-technology.yml",
    ".github/workflows/lore02-b-equipment.yml",
    ".github/workflows/lore02-c-medicine.yml",
    ".github/workflows/lore02-d-science.yml",
]
# D1: baseline minimum, not a closed list of future scientific records.
EXTENSIBLE = {"disciplines", "phenomena", "methods", "science_cases"}
EXPECTED = {
    "technology": 45, "legacy_technology": 14, "equipment": 73,
    "loadouts": 15, "conditions": 38, "procedures": 26, "agents": 13,
    "medical_matrix": 38, "species": 26, "disciplines": 14,
    "phenomena": 20, "methods": 9, "science_cases": 10,
}


def read(name):
    path = ROOT / FILES[name]
    content = path.read_text(encoding="utf-8")
    return content if name == "status" else json.loads(content)


def inputs():
    return {key: read(key) for key in FILES}


def validate_data(data, *, check_paths=True):
    errors = []
    checked = 0
    def need(condition, message):
        if not condition:
            errors.append(message)
    def records(name, field, id_field):
        rows = data[name].get(field, [])
        if not isinstance(rows, list):
            need(False, name + ": malformed collection")
            return [], set()
        ids = [r.get(id_field) for r in rows]
        need(len(ids) == len(set(ids)) and all(isinstance(x, str) and bool(x) for x in ids),
             name + ": duplicate or empty identifier")
        if name in EXPECTED:
            minimum = EXPECTED[name]
            need(len(rows) >= minimum if name in EXTENSIBLE else len(rows) == minimum,
                 name + ": catalogue count regression")
        return rows, set(ids)
    a, a_ids = records("technology", "records", "technology_id")
    a0, a0_ids = records("legacy_technology", "records", "technology_id")
    b, b_ids = records("equipment", "records", "equipment_id")
    loads, load_ids = records("loadouts", "profiles", "profile_id")
    cond, cond_ids = records("conditions", "catalogue", "condition_id")
    proc, proc_ids = records("procedures", "records", "procedure_id")
    agents, agent_ids = records("agents", "records", "agent_id")
    matrix, _ = records("medical_matrix", "records", "condition_ref")
    species, species_profile_ids = records("species", "records", "profile_id")
    disc, disc_ids = records("disciplines", "records", "discipline_id")
    phen, phen_ids = records("phenomena", "records", "phenomenon_id")
    methods, method_ids = records("methods", "records", "method_id")
    cases, case_ids = records("science_cases", "records", "case_id")
    science_fac, science_fac_ids = records("science_facilities", "facilities", "facility_id")
    science_roles, science_role_ids = records("science_facilities", "roles", "role_id")
    med_fac, med_fac_ids = records("medical_facilities", "facilities", "facility_id")
    med_roles, med_role_ids = records("medical_facilities", "professionals", "role_id")
    operator_rows, operator_ids = records("operators", "operators", "operator_id")
    civil_rows, civil_ids = records("civilizations", "records", "operator_id")
    technology_ids = a_ids | a0_ids
    need(not (a_ids & a0_ids), "technology: duplicate between initial and extension")
    need(len(technology_ids) == 59, "technology: total count regression")
    need(len(science_fac) >= 6 and len(science_roles) >= 10, "science facilities/roles count")
    need(len(med_fac) == 9 and len(med_roles) == 12, "medical facilities/roles count")
    need(len(operator_rows) == 9 and len(civil_rows) == 13,
         "technology/medicine: organizational profile regression")
    need(len(species_profile_ids) == len(species), "species: identifier collision")
    need(len(cases) == len(case_ids), "science cases: identifier collision")

    def link(source, field, valid, family, *, objects=False):
        nonlocal checked
        value = source.get(field, [])
        if value is None:
            return
        items = value if isinstance(value, list) else [value]
        for item in items:
            target = item.get("agent_ref") if objects and isinstance(item, dict) else item
            checked += 1
            need(isinstance(target, str) and target in valid,
                 family + ": orphan " + field + " -> " + str(target))

    for r in loads:
        for k in ("typical_equipment_ids", "conditional_equipment_ids"):
            link(r, k, b_ids, r["profile_id"])
    for r in data["loadouts"]["loadout_templates"]:
        link(r, "profile_refs", load_ids, r["loadout_id"])
    for r in cond:
        link(r, "procedure_ref", proc_ids, r["condition_id"])
        need(r.get("world_state_authority") == "CoreRPG_ONLY",
             r["condition_id"] + ": medical authority")
        need(r.get("clinical_dose") is None, r["condition_id"] + ": unsupported dose")
    for r in proc:
        link(r, "equipment_refs", b_ids, r["procedure_id"])
        need(r.get("ue5_implemented") is False and r.get("real_world_dosing") is None,
             r["procedure_id"] + ": false implemented medical procedure")
    for r in agents:
        link(r, "equipment_ref", b_ids, r["agent_id"])
        need(r.get("administerable_in_game_now") is False and r.get("dose") is None
             and r.get("universal_efficacy") is None,
             r["agent_id"] + ": unsafe automatic medicine")
    for r in matrix:
        ident = r["condition_ref"]
        link(r, "condition_ref", cond_ids, ident)
        link(r, "initial_response_ref", proc_ids, ident)
        link(r, "possible_agent_links", agent_ids, ident, objects=True)
        need(r.get("privacy") == "MEDICAL_AUTHORIZED_MINIMUM_NECESSARY",
             ident + ": medical privacy leak")
        need(r.get("cross_species_reuse") == "FORBIDDEN_WITHOUT_VALIDATION",
             ident + ": unjustified cross-species reuse")
    for r in phen:
        ident = r["phenomenon_id"]
        link(r, "discipline_refs", disc_ids, ident)
        link(r, "technology_refs", technology_ids, ident)
        link(r, "equipment_refs", b_ids, ident)
        need(r.get("presence_rule") == "CAN_EXIST_WITHOUT_PLAYER_INTERACTION",
             ident + ": player-dependent science")
        need(r.get("knowledge_state") == "UNKNOWN_UNTIL_EVIDENCE",
             ident + ": revealed hidden world truth")
        need(r.get("mechanics_status") == "PROPOSAL_ONLY_NOT_EXECUTABLE",
             ident + ": fake running science")
    for r in science_fac:
        ident = r["facility_id"]
        link(r, "technology_refs", technology_ids, ident)
        link(r, "equipment_refs", b_ids, ident)
        need(r.get("not_auto_spawned") is True and r.get("not_auto_operational") is True,
             ident + ": invented installation")
    for r in cases:
        ident = r["case_id"]
        link(r, "phenomenon_ref", phen_ids, ident)
        link(r, "method_refs", method_ids, ident)
        link(r, "specialist_refs", science_role_ids, ident)
        need(r.get("observer_view") == "PARTIAL_ONLY" and
             r.get("world_truth") == "NOT_ENCODED_IN_PUBLIC_CASE",
             ident + ": actor omniscience")
    for r in species:
        need(r.get("allow_default_human_reference") is False,
             r["profile_id"] + ": biological universality")
        need(r.get("normal_vitals") is None and r.get("species_specific_doses") is None,
             r["profile_id"] + ": fabricated physiology")

    # IDs of evidence sources are registry IDs, not free prose.
    sources = data["source_registry"].get("sources", [])
    source_ids = [s.get("source_id") for s in sources]
    need(len(source_ids) == len(set(source_ids)) and len(sources) >= 501,
         "source registry: missing/duplicate sources")
    registry = set(source_ids)
    for name in ("legacy_technology", "technology", "operators", "equipment",
                 "conditions", "procedures", "agents", "medical_matrix", "species",
                 "civilizations", "disciplines", "phenomena", "methods",
                 "science_facilities", "science_cases"):
        doc = data[name]
        rows = [v for v in doc.values() if isinstance(v, list)]
        for group in rows:
            for r in group:
                if not isinstance(r, dict):
                    continue
                provenance = r.get("provenance", {})
                ids = list(r.get("source_ids", [])) + list(r.get("canon_basis_sources", []))
                if isinstance(provenance, dict):
                    ids += list(provenance.get("source_ids", []))
                elif isinstance(provenance, list):
                    ids += [x.get("source_id") for x in provenance if isinstance(x, dict)]
                for identifier in ids:
                    checked += 1
                    need(isinstance(identifier, str) and identifier in registry,
                         name + ": unregistered provenance " + str(identifier))
    for name in ("technology", "equipment", "conditions", "agents", "disciplines", "phenomena"):
        need(data[name].get("mode") == "EDITORIAL_NON_RUNTIME",
             name + ": runtime boundary breach")

    policy = data["legacy_policy"]
    need(policy.get("runtime_import_allowed") is False and
         policy.get("authority") == "CoreRPG_WORLD_STATE_ONLY",
         "legacy: fake imported CoreRPG content")
    choice = policy.get("author_decisions", {})
    need(choice.get("scientific_catalogue") == "EXTENSIBLE"
         and choice.get("autonomous_science") == "YES"
         and choice.get("research_accessibility") == "HYBRID_A_PLUS_B"
         and choice.get("consequences") == "PERSISTENT_PROPORTIONATE",
         "legacy: changed author decisions")
    legacy = policy.get("scientific_legacy", {})
    for flag in ("naming_is_not_automatic", "official_name_requires_approval",
                 "recognized_team_credits_possible", "names_survive_years_passed",
                 "names_survive_character_career_change", "conversation_requires_actor_knowledge",
                 "ship_must_have_commissioned_technology_to_claim_its_function"):
        need(legacy.get(flag) is True, "legacy: missing persistent naming safeguard " + flag)
    stages = policy.get("scientific_research_technology_transfer", [])
    need([x.get("id") for x in stages] == [
        "DISCOVERY", "SUSTAINED_RESEARCH", "INDEPENDENT_VALIDATION",
        "FLEET_EVALUATION", "ENGINEERING_ADAPTATION", "SHIPYARD_INSTALLATION",
        "POST_REFIT_TRIALS", "OPTIONAL_GRADUAL_FLEET_ADOPTION"
    ] and all(x.get("may_fail") is True for x in stages),
        "legacy: instant or incomplete shipyard process")
    rules = policy.get("exception_rules", {})
    need(rules.get("playable_time_travel_allowed") is False and
         rules.get("time_travel_technology_unlock_allowed") is False,
         "legacy: forbidden time travel")
    omega = rules.get("omega", {})
    need(omega.get("author_mandatory_special_mission") is True and
         omega.get("minimum_authored_special_missions", 0) >= 1 and
         omega.get("normal_tech_transfer_allowed") is False and
         omega.get("classified_information_access_required") is True,
         "legacy: Omega exception weakened")
    worm = rules.get("wormholes", {})
    need(worm.get("traversal_allowed") is True and worm.get("rarity") == "RARE"
         and worm.get("requires_valid_astrography_link") is True,
         "legacy: unrestricted wormholes")
    status = data["status"]
    need("| D — Ciencia y fenómenos | ✅ COMPLETE |" in status,
         "status: D merge not regularized")
    need("| E — Integración y auditoría A–D | 🟨 IN_PROGRESS |" in status,
         "status: E wrongly closed before author approval")
    need("LORE-02 nunca es runtime por sí sola" in status,
         "status: false runtime completion")

    if check_paths:
        for path in REQUIRED_ANCHORS:
            need((ROOT / path).is_file(), "missing cross-phase contract: " + path)
        for r in species:
            need((ROOT / r["evidence_ref"]).is_file(), "species: missing evidence " + r["evidence_ref"])
        for r in science_fac:
            need((ROOT / r["existing_ref"]).is_file(), "science: missing facility " + r["existing_ref"])
        for r in b:
            for ref in r.get("gameplay_consumer_refs", []) + r.get("object_model_refs", []):
                checked += 1
                need((ROOT / ref).is_file(), "equipment: broken consumer " + ref)
    return errors, checked


def validate():
    errs, checked = validate_data(inputs())
    if errs:
        raise AssertionError("\n".join(errs))
    return {"cross_reference_checks": checked, **{k: v for k, v in EXPECTED.items()}}


if __name__ == "__main__":
    print("LORE-02 E AUDIT OK:", json.dumps(validate(), ensure_ascii=False))
