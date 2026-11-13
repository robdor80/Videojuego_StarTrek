#!/usr/bin/env python3
"""LORE-05F: coherencia transversal DOCUMENTAL de A-E. Sin acceso ni mutacion WorldState."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILES = {
    "valhalla": "mundo/lore/starships/individual_ships/project_valhalla_enterprise_d_v0.1.json",
    "locations": "mundo/lore/astrography/worlds/lore05c_priority_locations_v0.1.json",
    "entities": "mundo/lore/operations/lore05d_entities_v0.1.json",
    "languages": "mundo/lore/languages/lore05e_reference_overlay_v0.1.json",
    "e_cases": "mundo/lore/exploration/lore05e_acceptance_cases_v0.1.json",
    "c_cases": "mundo/lore/astrography/worlds/lore05c_validation_cases_v0.1.json",
    "d_cases": "mundo/lore/operations/lore05d_validation_cases_v0.1.json",
    "ships_source": "mundo/lore/starships/individual_ships/core_canonical_ships.json",
    "anchors_source": "mundo/lore/astrography/systems/anchor_locations.json",
    "factions_source": "sistemas/gameplay/diplomacy/major_faction_catalogue.json",
    "languages_source": "sistemas/gameplay/languages/initial_language_catalogue.json",
    "translator_source": "sistemas/gameplay/languages/language_runtime_model.json",
    "subspace_source": "sistemas/gameplay/communications/subspace_communication_contract.json",
}
CHARACTERS = [
    "starfleet/jean_luc_picard_lore05b_v0.1.md",
    "starfleet/kathryn_janeway_lore05b_v0.1.md",
    "starfleet/william_t_riker_lore05b_v0.1.md",
    "starfleet/beverly_crusher_lore05b_v0.1.md",
    "starfleet/geordi_la_forge_lore05b_v0.1.md",
    "starfleet/worf_lore05b_v0.1.md",
    "starfleet/data_lore05b_v0.1.md",
    "starfleet/deanna_troi_lore05b_v0.1.md",
    "starfleet/seven_of_nine_lore05b_v0.1.md",
    "starfleet/tuvok_lore05b_v0.1.md",
    "starfleet/benjamin_sisko_lore05b_v0.1.md",
    "federation_civilians/guinan_lore05b_v0.1.md",
]


def load_all(root: Path = ROOT) -> dict:
    d = {key: json.loads((root / path).read_text(encoding="utf-8")) for key, path in FILES.items()}
    d["characters"] = {
        name: (root / "mundo/lore/characters" / name).read_text(encoding="utf-8")
        for name in CHARACTERS
    }
    return d


def problems_for_data(d: dict) -> list[str]:
    """Pure audit, suitable for adversarial mutation tests."""
    problems = []
    def issue(s): problems.append(s)
    def unique(items, key, scope):
        values = [item.get(key) for item in items]
        if len(values) != len(set(values)) or any(not v for v in values):
            issue("duplicated/empty " + scope)

    v = d["valhalla"]
    p = v.get("project", {})
    subj = v.get("subject", {})
    if (v.get("decision_id"), p.get("project_id"), p.get("director")) != (
        "DEC-0020", "project_valhalla", "geordi_la_forge"
    ):
        issue("Valhalla identity/director")
    if (subj.get("ship_id"), subj.get("registry"), subj.get("class_id"), subj.get("ship_is_renamed")) != (
        "uss_enterprise_ncc_1701_d", "NCC-1701-D", "galaxy", False
    ):
        issue("Enterprise-D identity/class/registry")
    years = {x.get("year"): x for x in v.get("chronology", [])}
    if not ({2371, 2379, 2380, 2383, 2387, 2401} <= set(years)):
        issue("chronology missing anchors")
    if years.get(2387, {}).get("campaign_initialization") != "conditional_future_only":
        issue("2387 forced as historical event")
    if v.get("future", {}).get("readiness_2387_guaranteed") is not False or (
        v.get("academy", {}).get("player_assignment_automatic") is not False
    ) or (v.get("academy", {}).get("captaincy_automatic") is not False):
        issue("automatic readiness/destination/command")
    if v.get("quantum_slipstream", {}).get("installed_on_enterprise_d_by_default") is not False:
        issue("unauthorized quantum slipstream")
    if v.get("runtime_implemented") is not False or v.get("authoritative_world_state") != "CoreRPG_ONLY":
        issue("A falsely claims runtime/world authority")

    c = d["locations"]
    locations = c.get("locations", [])
    anchors = {x["location_id"] for x in d["anchors_source"]["locations"]}
    if len(locations) != 16 or c.get("campaign_baseline_year") != 2383:
        issue("C inventory/baseline")
    unique(locations, "id", "location identity")
    for x in locations:
        if x.get("anchor_location_id") and x["anchor_location_id"] not in anchors:
            issue("unknown anchor " + str(x.get("id")))
        if x.get("facility_id") and x["facility_id"] not in {
            z["facility_id"] for z in d["entities"]["facilities"]
        }:
            issue("cross-reference facility missing " + str(x.get("id")))
        if any(x.get(flag) is not False for flag in (
            "runtime_generation_enabled", "automatic_travel_enabled", "world_state_mutations"
        )):
            issue("location illegally instantiated/traveled")
    for id_ in ("dorvan_v", "new_bajor"):
        rec = next((x for x in locations if x.get("id") == id_), {})
        if rec.get("anchor_location_id") is not None or rec.get("automatic_travel_enabled") is not False:
            issue("historical colony made navigable " + id_)
    if any(c.get(k) is not value for k, value in (
        ("no_new_coordinates", True), ("no_new_routes", True), ("no_live_mutations", True)
    )):
        issue("C creates coordinates/routes/state")

    e = d["entities"]
    if e.get("campaign_baseline_year") != 2383 or e.get("world_state_authority") != "CoreRPG_ONLY":
        issue("D temporal or authority boundary")
    for key, expected in (("ships", 8), ("facilities", 12), ("factions", 8), ("institution_profiles", 2)):
        if len(e.get(key, [])) != expected:
            issue("D count " + key)
    for k, n in (("ship_count", 8), ("facility_count", 12), ("faction_count", 8)):
        if e.get(k) != n:
            issue("D declared count " + k)
    for k in ("runtime_implemented", "live_state_mutations", "automatic_world_spawns", "automatic_missions"):
        if e.get(k) is not False:
            issue("D unsafe " + k)
    unique(e["ships"], "ship_id", "ship identity")
    unique(e["facilities"], "facility_id", "facility identity")
    unique(e["factions"], "faction_id", "faction identity")
    baseline_ships = {x["ship_id"]: x for x in d["ships_source"]["ships"]}
    for x in e["ships"]:
        src = baseline_ships.get(x["ship_id"])
        if not src or x.get("class_id") != src.get("class_id") or (
            x.get("registry") != src.get("registry") and (x.get("registry") or src.get("registry"))
        ) or x.get("registry_history") != src.get("registry_history", None):
            issue("ship provenance/class/registry " + str(x["ship_id"]))
        if any(x.get(flag) is not False for flag in (
            "world_state_known", "auto_spawn", "auto_assign_to_player", "automatic_command_authority"
        )):
            issue("ship automatically activated/assigned")
    enterprise = next((x for x in e["ships"] if x.get("ship_id") == subj.get("ship_id")), {})
    if (enterprise.get("registry"), enterprise.get("class_id"), enterprise.get("documentary_state_2383")) != (
        subj.get("registry"), subj.get("class_id"), "PROYECTO_RECONSTRUCCION"
    ):
        issue("A/D Enterprise divergence")
    defiant = next((x for x in e["ships"] if x.get("ship_id") == "uss_defiant_nx_74205"), {})
    if defiant.get("documentary_state_2383") != "DESTRUIDA_ANTES_2383":
        issue("original Defiant resurrected")
    for x in e["facilities"]:
        if x.get("unique_identity_respected") is not True or any(x.get(k) is not False for k in (
            "auto_generate_duplicate", "automatically_service_player"
        )):
            issue("facility clone or infinite service")
    source_factions = d["factions_source"]["factions"]
    if {x["faction_id"] for x in e["factions"]} != set(source_factions):
        issue("D faction identities diverge")
    if {x.get("institution_id") for x in e["institution_profiles"]} != {
        "federation_civil_government", "starfleet"
    }:
        issue("civil Federation and Starfleet conflated")
    if any(x.get("automatic_treaty_or_war") is not False or x.get("automatic_membership") is not False for x in e["factions"]):
        issue("automatic diplomacy")

    l = d["languages"]
    if l.get("campaign_baseline_year") != 2383 or l.get("world_state_authority") != "CoreRPG_ONLY":
        issue("E temporal/authority boundary")
    if l.get("translator_states") != d["translator_source"]["translation_states"]:
        issue("translator owner states diverge")
    if l.get("channel_states") != d["subspace_source"]["link_states"]:
        issue("subspace owner states diverge")
    reference_languages = {x["language_id"]: x for x in d["languages_source"]["languages"]}
    if len(l.get("existing_languages", [])) != 8:
        issue("E language count")
    unique(l["existing_languages"], "language_id", "language identity")
    for x in l["existing_languages"]:
        src = reference_languages.get(x["language_id"])
        if src is None or x.get("availability_scope") != src.get("availability_scope"):
            issue("E language ID/availability " + str(x["language_id"]))
        if any(x.get(k) is not False for k in (
            "auto_assume_fluency", "auto_assume_monolingual_species", "auto_unlock_dlc"
        )):
            issue("E unwarranted language assumption")
    for id_ in ("kazon", "talaxian"):
        rec = next((x for x in l["existing_languages"] if x.get("language_id") == id_), {})
        if rec.get("availability_scope") != "DLC_DELTA_FUTURE":
            issue("Delta DLC prematurely unlocked")
    for key in ("runtime_implemented", "world_state_mutations", "automatic_discoveries",
                "automatic_contact", "automatic_diplomacy", "automatic_dlc_unlock"):
        if l.get(key) is not False:
            issue("E unsafe " + key)
    if l.get("new_playable_language_definitions") != 0 or len(l.get("narrative_rules", [])) != 18:
        issue("E fabricated languages or incomplete rules")
    for key, names, count in (
        ("c_cases", "scenarios", 12), ("d_cases", "documentary_cases", 18),
        ("e_cases", "documentary_cases", 24)
    ):
        rec = d[key]
        if len(rec.get(names, [])) != count:
            issue("scenario inventory " + key)
        if rec.get("simulation_claimed") is True or rec.get("runtime_executed") is True:
            issue("documentary scenarios portrayed as runtime " + key)
        for x in rec.get(names, []):
            if x.get("world_state_mutations") is not False:
                issue("scenario mutates WorldState " + key)
            if key != "c_cases" and x.get("core_runtime_test") is not False:
                issue("scenario claims Core runtime " + key)

    characters = d.get("characters", {})
    if len(characters) != 12:
        issue("legendary NPC roster != 12")
    for i, name in enumerate(CHARACTERS, start=1):
        ctext = characters.get(name, "")
        if not ctext.startswith("# LORE-05B-%02d " % i):
            issue("missing/misnumbered NPC " + name)
        if "GAME_ADDITION" not in ctext or "CoreRPG" not in ctext:
            issue("NPC provenance/authority missing " + name)
    if "entrega personalmente los galones" not in characters.get(CHARACTERS[0], ""):
        issue("Picard personal promotion ceremony lost")
    if "2390" not in characters.get(CHARACTERS[6], "") or "2379" not in characters.get(CHARACTERS[6], ""):
        issue("Data death/return boundary lost")
    if "2388" not in characters.get(CHARACTERS[10], "") or "2375" not in characters.get(CHARACTERS[10], ""):
        issue("Sisko historical return boundary lost")
    if "HIPÓTESIS" not in characters.get(CHARACTERS[8], "").upper() or "2358" not in characters.get(CHARACTERS[8], ""):
        issue("Seven provisional age chronology lost")
    return problems


def validate(root: Path = ROOT) -> list[str]:
    problems = problems_for_data(load_all(root))
    overlay = json.loads((root / FILES["languages"]).read_text(encoding="utf-8"))
    for label, path in overlay.get("source_contracts", {}).items():
        if not (root / path).is_file():
            problems.append("missing owner contract " + label + ": " + path)
    required = [
        "CONTENT_STATUS.md",
        "proyecto/docs/roadmap/lore_05_a/ACTA_CIERRE_DOCUMENTAL_LORE05A_20261113.md",
        "mundo/lore/characters/LORE05B_AUDITORIA_PRECIERRE_2026-11-13.md",
        "proyecto/docs/roadmap/lore_05_c/ACTA_CIERRE_DOCUMENTAL_LORE05C_20261113.md",
        "proyecto/docs/roadmap/lore_05_d/ACTA_CIERRE_DOCUMENTAL_LORE05D_20261113.md",
        "proyecto/docs/roadmap/lore_05_e/ACTA_CIERRE_DOCUMENTAL_LORE05E_20261113.md",
        "proyecto/docs/roadmap/lore_05_f/ACTA_AUDITORIA_TRANSVERSAL_20261113.md",
    ]
    for path in required:
        if not (root / path).is_file():
            problems.append("missing documentary closure " + path)
    roadmap = root / "proyecto/docs/roadmap/README.md"
    if not (root / "mundo/lore/characters/lore05b_elenco_cerrado_2026-11-13.md").is_file():
        problems.append("legendary roster index missing")
    if not roadmap.is_file() or "../../mundo/lore/characters/lore05b" in roadmap.read_text(encoding="utf-8"):
        problems.append("roadmap 05B broken relative link")
    return problems


if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print("ERROR:", failure)
    if failures:
        raise SystemExit(1)
    print("LORE-05F PASS: 5 bloques, 12 NPC, 16 localizaciones, 8+12+8+2 entidades, 8 idiomas, 54 casos; autoridad CoreRPG y límites respetados")
