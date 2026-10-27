#!/usr/bin/env python3
"""LORE-03B: revisión estructural de conflictos históricos. Sin cambios de WorldState."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
INDEX = "lore/conflicts/lore03b_dossier_index_v0.1.json"
SCENARIOS = "docs/roadmap/lore_03_b/B06_escenarios_emergentes_v0.1.json"

class InvalidLore03B(ValueError):
    pass

def demand(condition, reason):
    if not condition:
        raise InvalidLore03B(reason)

def load(path, root=ROOT):
    return json.loads((root / path).read_text(encoding="utf-8"))

def reference_context(root=ROOT):
    diplomatic = load("lore/diplomacy/historical_events_v0.1.json", root)
    chron = load("lore/historical_events/lore03_a_chronology_index_v0.1.json", root)
    factions = load("lore/diplomacy/relation_index_v0.1.json", root)
    agreements = load("lore/diplomacy/agreements_conflicts_v0.1.json", root)
    registry = load("sources/source_registry/source_registry.json", root)
    return {
        "events": {x["event_id"] for x in diplomatic["events"]} |
                  {x["event_id"] for x in chron["additional_historical_anchors"]},
        "false_events": set(chron["reused_catalogues"][0]["false_claim_event_ids"]),
        "sources": {x["source_id"] for x in registry["sources"]},
        "factions": set(factions["entity_ids"]),
        "treaties": {x["treaty_id"] for x in agreements["agreements"]},
        "counts": (len(diplomatic["events"]), len(chron["additional_historical_anchors"]))
    }

def validate_dossier(d, context):
    did = d.get("conflict_id")
    demand(isinstance(did, str) and did, "Missing conflict ID")
    for key in ("gameplay_activated", "auto_bootstrap_future",
                "auto_start_conflict", "is_compulsory_future_script",
                "runtime_state_mutation"):
        demand(d.get(key) is False, f"{did} unexpectedly enables {key}")
    demand(d.get("world_state_authority") == "CoreRPG_ONLY", f"{did}: authority")
    demand(d.get("campaign_start_year_proposed") == 2383 and
           d.get("campaign_start_exact_date") is None, f"{did}: fabricated campaign date")
    demand(d.get("historical_contract_ref") ==
           "lore/conflicts/conflict_definition_contract.json", f"{did}: contract")
    demand(d.get("runtime_design_ref") ==
           "gameplay/conflict/conflict_war_index_v0.1.json", f"{did}: duplicate engine")
    demand(set(d.get("participant_refs", [])) <= context["factions"], f"{did}: invalid faction")
    demand(set(d.get("major_event_refs", [])) <= context["events"], f"{did}: invalid event")
    demand(set(d.get("treaty_refs", [])) <= context["treaties"], f"{did}: invalid treaty")
    demand(bool(d.get("source_refs")) and
           set(d["source_refs"]) <= context["sources"], f"{did}: invalid source")
    demand({p.get("source_id") for p in d.get("provenance", [])} ==
           set(d["source_refs"]), f"{did}: missing provenance")
    years = [d[k]["reference_year"] for k in ("start_date_or_range", "end_date_or_range")]
    demand(all(y is None or type(y) is int for y in years), f"{did}: invalid year")
    demand(years[0] is None or years[1] is None or
           years[0] <= years[1], f"{did}: reversed years")
    demand(all(d[k].get("precision") == "YEAR_APPROXIMATE_OR_UNKNOWN"
               for k in ("start_date_or_range","end_date_or_range")),
           f"{did}: falsely precise dates")
    for key in ("origin_and_causes", "historical_development",
                "uncertainty_and_canon_limits", "game_addition_example"):
        demand(len(d.get(key, "")) >= 35, f"{did}: insufficient {key}")
    return did

def validate_index(idx, scenarios, dossiers, context):
    demand(idx["status"] == "NEEDS_REVIEW_DOCUMENTARY", "Unapproved final status")
    demand(idx["authority"] == "CoreRPG_ONLY", "Index authority")
    demand(idx["campaign_start_year_proposed"] == 2383 and
           idx["campaign_start_exact_date"] is None, "Campaign date invented")
    for key in ("gameplay_activated", "auto_start_conflicts", "auto_bootstrap_future"):
        demand(idx[key] is False, f"Index enables {key}")
    demand(idx["source_contract"] == "lore/conflicts/conflict_definition_contract.json",
           "Second historical contract")
    demand(idx["runtime_reference"] == "gameplay/conflict/conflict_war_index_v0.1.json",
           "New runtime engine")
    demand(idx["original_conflict_registry"] ==
           "lore/diplomacy/agreements_conflicts_v0.1.json", "Original events registry lost")
    entries = idx["dossiers"]
    demand(len(entries) == idx["expected_dossiers"] == len(dossiers) == 22,
           "Dossier count mismatch")
    demand(len(set(dossiers)) == len(dossiers), "Duplicated dossier ID")
    demand("dominion_war" in dossiers and "cardassian_resistance_2375" in dossiers,
           "Dominion war or resistance missing")
    dw = dossiers["dominion_war"]
    demand(set(dw["shared_war_events_not_separate_conflicts"]) ==
           {"dominion_war_begins", "dominion_cardassian_war_bajor"},
           "One Dominion war turned into two")
    demand(dw["coalition_membership"] == "CHANGES_OVER_TIME", "Fixed coalitions")
    demand(dw["subconflicts"] == ["cardassian_resistance_2375"], "Subconflict not linked")
    demand(dossiers["cardassian_resistance_2375"]["parent_conflict_id"] == "dominion_war",
           "Reverse subconflict link")
    false = dossiers["tzenkethi_border_provocation_2372"]
    demand(false["asserted_tzenkethi_coup_happened"] is False and
           false["false_claim_event_refs"] == ["tzenkethi_false_coup_report"],
           "False Tzenkethi coup asserted as historical")
    demand("tzenkethi_false_coup_report" not in
           dossiers["federation_tzenkethi_prior_war"]["major_event_refs"],
           "False coup included in historical prior war")
    demand(len(context["false_events"]) >= 1 and
           "tzenkethi_false_coup_report" in context["false_events"],
           "LORE-03A false report classification lost")
    demand(context["counts"] == (40,26), "LORE-01D/03A event snapshot changed")
    demand(scenarios["status"] == "DOCUMENTARY_EXAMPLES_ONLY" and
           scenarios["authority"] == "CORE_RPG_ONLY", "Scenario status wrong")
    demand(scenarios["auto_trigger"] is False and
           scenarios["new_missions_created"] is False, "Scenario auto activation")
    demand(len(scenarios["scenarios"]) == scenarios["scenario_count"] == 12,
           "Scenario count mismatch")
    demand(len({x["seed_id"] for x in scenarios["scenarios"]}) == 12,
           "Scenario IDs duplicate")
    for x in scenarios["scenarios"]:
        demand(x["not_canon"] is True and
               x["worldstate_mutation"] is False and
               x["automatic_war"] is False and
               len(x["peaceful_route"]) > 6, "Scenario forces war or mutates world")
    return True

def validate(root=ROOT):
    context = reference_context(root)
    index = load(INDEX,root)
    scenarios = load(SCENARIOS,root)
    dossiers = {}
    for item in index["dossiers"]:
        p = Path(item["ref"])
        demand(p.parts[:3] == ("lore","conflicts","dossiers") and
               p.suffix == ".json", "Unsafe/invalid path")
        demand((root/p).is_file(), f"Missing {p}")
        d = load(p,root)
        did = validate_dossier(d,context)
        demand(did == item["conflict_id"] and did not in dossiers, "Index ID mismatch/duplicate")
        mp = Path(item["document_ref"])
        demand(mp == p.with_suffix(".md") and (root/mp).is_file(), f"Missing dossier Markdown {mp}")
        markdown = (root/mp).read_text(encoding="utf-8")
        demand("## Referencias existentes" in markdown and len(markdown) > 700,
               f"Insufficient documentary record {did}")
        dossiers[did] = d
    validate_index(index, scenarios, dossiers, context)
    for file in ("B01_clasificacion_y_decisiones.md",
                 "B02_grandes_guerras_historicas.md",
                 "B03_crisis_regionales_y_politicas.md",
                 "B04_diplomacia_alianzas_y_paz.md",
                 "B05_horizonte_2383_consecuencias.md",
                 "B06_conflictos_emergentes_documental.md",
                 "B07_integracion_y_migracion_diferida.md",
                 "B08_auditoria_y_criterios.md"):
        demand((root/"docs/roadmap/lore_03_b"/file).is_file(), f"Missing subphase {file}")
    return {"dossiers":len(dossiers), "scenarios":len(scenarios["scenarios"]),
            "prior_events":context["counts"], "status":"NEEDS_REVIEW_DOCUMENTARY"}

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
