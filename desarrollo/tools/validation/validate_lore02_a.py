#!/usr/bin/env python3
"""LORE-02 A: validación documental de fichas tecnológicas, no simulación CoreRPG/UE5."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOG = "mundo/lore/technology/ship_station_catalogue_v0.1.json"
SCENARIOS = "mundo/lore/technology/ship_station_cases_v0.1.json"

def load(rel: str):
    path = ROOT / rel
    return json.loads(path.read_text(encoding="utf-8"))

def require(ok: bool, reason: str):
    if not ok:
        raise AssertionError(reason)

def valid_path(rel: str) -> bool:
    return (
        isinstance(rel, str)
        and bool(rel)
        and not Path(rel).is_absolute()
        and ".." not in Path(rel).parts
        and (ROOT / rel).is_file()
    )

def validate() -> dict[str, int]:
    catalog = load(CATALOG)
    scenarios = load(SCENARIOS)
    tech = load("mundo/lore/technology/technology_definition_contract.json")
    matrix = load("sistemas/gameplay/ship_operations/era_technology_matrix.json")
    sources = {s["source_id"]: s for s in load("mundo/sources/source_registry/source_registry.json")["sources"]}
    delta = load("sistemas/universe/generation/lore01_tng_content_availability_v0.1.json")
    profiles = {p["id"]: p for p in matrix["profiles"]}

    require(catalog["status"] == "RESEARCH_IN_PROGRESS"
            and catalog["mode"] == "DOCUMENTARY_NOT_RUNTIME", "Premature closure/runtime")
    require(catalog["authority"] == "CoreRPG_World_State_ONLY"
            and catalog["runtime_import_allowed"] is False
            and catalog["delta_dlc_enabled"] is False, "World or Delta activation")
    require(catalog["era_source"] == "sistemas/gameplay/ship_operations/era_technology_matrix.json",
            "Duplicate era system")
    require(len(profiles) == len(matrix["profiles"]) == 5, "Era matrix drift")
    records = catalog["records"]
    ids = [r["technology_id"] for r in records]
    require(len(records) == catalog["records_count"] == 14, "Catalogue not consistent")
    require(len(set(ids)) == len(ids), "Duplicate technology ID")

    for item in records:
        uid = item["technology_id"]
        require(set(tech["required_fields"]).issubset(item), "Missing required fields: " + uid)
        require(uid.startswith("starfleet_") and item["display_name"]
                and item["category"], "Bad technology identity: " + uid)
        require(item["availability"] in tech["availability_values"], "Unknown availability state: " + uid)
        require(item["interpretation_class"] == "INFERRED"
                and len(item["prohibited_inference"]) >= 28, "Missing inference controls: " + uid)
        require(item["operator_or_civilization_validity"]
                and item["platform_compatibility"]
                and len(item["capabilities"][0]) >= 50
                and len(item["dependencies"]) >= 2
                and len(item["failure_modes"]) >= 2
                and len(item["operational_constraints"]) >= 2,
                "Underspecified system: " + uid)
        require(item["runtime"] == {
            "data_import_allowed": False,
            "ai_direct_world_mutation": False,
            "delta_dlc_unlock": False
        }, "Unauthorized runtime capability: " + uid)
        refs = item["gameplay_consumer_refs"]
        require(bool(refs) and all(valid_path(s) for s in refs), "Broken consumer ref: " + uid)
        provenance = item["provenance"]
        require(bool(provenance), "Missing provenance: " + uid)
        for ev in provenance:
            require(ev["source_id"] in sources
                    and sources[ev["source_id"]]["source_type"] == ev["source_type"]
                    and ev["confidence"] in ("HIGH", "MEDIUM", "LOW")
                    and len(ev["claim_scope"]) >= 40,
                    "Unregistered or unsupported provenance: " + uid)

        t = item["temporal_validity"]
        require(t["authority"] == catalog["era_source"] and
                t["unmapped_eras_mean"] == "NOT_RESEARCHED_NOT_UNAVAILABLE",
                "False era assertion: " + uid)
        aliases = t["known_matrix_keys"]
        require(bool(aliases), "No era evidence: " + uid)
        require(len({q["profile_id"] for q in aliases}) == len(aliases),
                "Repeated profile: " + uid)
        for alias in aliases:
            profile = profiles.get(alias["profile_id"])
            require(profile is not None and alias["capability_key"] in profile["capabilities"],
                    "Bad era-key reference: " + uid)
        check = next((q for q in aliases if q["profile_id"] == item["availability_profile_id"]), None)
        require(check is not None, "Availability not linked: " + uid)
        require(item["availability"] ==
                profiles[check["profile_id"]]["capabilities"][check["capability_key"]],
                "Cached availability drift: " + uid)
        require(item["availability_interpretation"] ==
                "derived_only_from_" + check["profile_id"] + "_upper_bound_not_installed_state",
                "Availability claimed as installed: " + uid)

    gaps = catalog["research_backlog"]
    require(len(gaps) >= 8 and len({q["id"] for q in gaps}) == len(gaps),
            "Missing or colliding research gaps")
    for q in gaps:
        require(len(q["missing"]) >= 50 and
                bool(q["references"]) and all(valid_path(p) for p in q["references"]),
                "Unsourced gap: " + q["id"])

    require(scenarios["status"] == "DOCUMENTARY_NOT_RUNTIME", "Executable scenarios")
    cases = scenarios["cases"]
    require(len(cases) == scenarios["case_count"] == 14
            and len({v["case_id"] for v in cases}) == 14, "Scenario count/ID")
    for c in cases:
        require(all(ref in ids for ref in c["technology_refs"]), "Broken case refs")
        require(c["era_profile_id"] in profiles, "Unknown era in case")
        require("observer_visible_information" in c["required_context"]
                and "individual_installed_capabilities" in c["required_context"]
                and "authenticated_actor_and_authority" in c["required_context"],
                "Case ignores installed state or knowledge boundary")
        require(c["result"] == "REQUIRES_HOST_AND_CORERPG_RESOLUTION"
                and c["ai_direct_world_mutation"] is False
                and c["delta_dlc_unlock"] is False, "Case prescribes unauthorized change")
        require(len(c["expected_documentary_reasoning"]) > 60
                and len(c["forbidden_conclusion"]) > 35, "Sparse case")

    require(delta["delta_dlc"]["status"] == "FUTURE_NOT_IMPLEMENTED"
            and delta["delta_dlc"]["default_main_game_spawn_allowed"] is False
            and delta["delta_dlc"]["planned_travel"]["entry_system_id"] is None,
            "Reserved DLC Delta activated")
    status = (ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    require("| E — Información operativa transversal | ✅ COMPLETE |" in status,
            "LORE-01 E administration still stale")
    require("| A — Tecnología de naves y estaciones | ✅ COMPLETE |" in status,
            "LORE-02 A merged in PR #31 must be administratively COMPLETE")
    require(all(valid_path(x) for x in (
        "proyecto/docs/roadmap/lore_02_master_plan_v0.1.md",
        "proyecto/docs/roadmap/lore_02_a_research_notes_v0.1.md",
        "mundo/lore/technology/ship_station_cases_v0.1.json",
    )), "Missing narrative report")
    valhalla = load("mundo/lore/technology/valhalla_tech_decisions_v0.1.json")
    require(valhalla["schema_version"] == "0.1.0"
            and valhalla["record_id"] == "valhalla_technology_decisions"
            and valhalla["runtime_implemented"] is False
            and valhalla["authoritative_world_state"] == "CoreRPG_ONLY",
            "Valhalla cannot become runtime authority")
    require(valhalla["class_identity"] == "NEW_VALHALLA_CLASS_GALAXY_INSPIRED_NOT_GALAXY_REFIT"
            and valhalla["auxiliary_yacht_active"] is False
            and valhalla["auxiliary_project"] == "IDEA-0010"
            and valhalla["year_of_commissioning"] is None,
            "Valhalla identity, yacht or commission year contradicted")
    choices = valhalla["decisions"]
    require(len(choices) == 16
            and [q["decision_id"] for q in choices]
            == [f"VAL-TEC-{i:02}" for i in range(1, 17)], "Valhalla decision register incomplete")
    for index, q in enumerate(choices):
        require(q["selection"] == "B" and q["topic"]
                and q["state"] == "APPROVED_DESIGN_NOT_RUNTIME"
                and q["decision_basis"]
                == ("AUTHOR_EXPLICIT_B" if index < 8 else "AUTHOR_DELEGATED_BALANCED_B"),
                "Valhalla choice/provenance mismatch")
    profile = (ROOT / valhalla["source_of_detail"]).read_text(encoding="utf-8")
    for needed in ("primarios", "secundarios", "terciarios", "ablativo",
                   "CoreRPG", "IDEA-0010", "sin fijar"):
        require(needed in profile, "Missing Valhalla safeguard: " + needed)

    evidence_rel = "proyecto/docs/roadmap/lore_02_a_eight_gaps_dossier_v0.2.md"
    require(valid_path(evidence_rel), "Eight-gap research dossier missing")
    evidence = (ROOT / evidence_rel).read_text(encoding="utf-8")
    require("RESEARCH_IN_PROGRESS" in evidence
            and "LORE-02 A permanece" in evidence
            and "CoreRPG" in evidence, "Research dossier prematurely claims implementation")
    for gap_id in (f"A-G{i:02}" for i in range(1, 9)):
        require(gap_id in evidence, "Missing evidence discussion for " + gap_id)

    return {"technology_records": len(records),
            "research_gaps": len(gaps), "negative_scenarios": len(cases),
            "matrix_profiles": len(profiles), "provenance_ids": len(sources)}

if __name__ == "__main__":
    print("LORE-02 A documental validada:", validate())
