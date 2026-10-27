#!/usr/bin/env python3
"""LORE-03 A: verifica integridad editorial, NO certifica pantalla ni implementa simulacion."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INDEX = "mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json"
TIMELINE = "mundo/lore/historical_events/lore03_a_yearly_atlas_v0.2.md"
BOUNDARY = "mundo/lore/historical_events/lore03_a_date_boundary_cases_v0.2.md"
FINAL_REPORT = "proyecto/docs/roadmap/lore_03_a_completion_audit_v0.2.md"
MUST_BE_PRESENT = {"wolf_359_battle", "bajoran_wormhole_discovery", "enterprise_d_veridian_loss",
                   "voyager_delta_displacement", "voyager_canonical_return", "sector_001_borg_invasion",
                   "ds9_operation_return", "defiant_chintoka_loss", "voyager_vaadwaur_encounter",
                   "voyager_unimatrix_zero", "sisko_joins_prophets", "klingon_civil_war_crisis"}

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def check(ok, reason):
    if not ok:
        raise AssertionError(reason)

def classify_by_year(event, campaign_year):
    """Only a documentary example: NEVER used to mutate WorldState."""
    check(type(campaign_year) is int and 2364 <= campaign_year <= 2383, "Campaign sample outside allowed reference window")
    y = event["time_anchor"]["reference_year"]
    if y < campaign_year:
        return "ESTABLISHED_BEFORE_D"
    if y > campaign_year:
        return "NOT_YET_AT_D"
    return "UNRESOLVED_SAME_YEAR"

def validate_index(idx, diplomatic, registry, eras):
    """Input objects kept injectable for negative mutation tests."""
    check(idx["status"] == "COMPLETE_DOCUMENTARY", "LORE-03 A administrative closure missing")
    check(idx["scope"] == "tng_ds9_voyager_only", "Wrong historical scope")
    check(idx.get("closure",{}).get("pr_number") == 38 and idx["closure"].get("merge_commit_sha") == "d0efab2c9d4b2451ad678b651bd6ecf2283d8235" and idx["closure"].get("runtime_activated") is False, "LORE-03 A closure evidence mismatch")
    check(idx["authority"] == "CoreRPG_World_State_ONLY", "CoreRPG authority missing")
    for prop in ("gameplay_activated", "auto_bootstrap_future", "playable_time_travel"):
        check(idx[prop] is False, "Unapproved gameplay feature: " + prop)
    check(eras == {"pike":False, "kirk":False, "tng_ds9_voyager":True}, "Unexpected playable-era flags")
    check(idx["prior_eras"] == {"pike":"HISTORICAL_REFERENCE_ONLY", "kirk":"HISTORICAL_REFERENCE_ONLY"},
          "Former campaigns no longer available; do not delete their history")
    w = idx["reference_window"]
    check((w["start_year"], w["end_year"]) == (2364,2383), "Reference window changed")
    check(w["campaign_start_date"] is None and w["date_is_author_approved"] is False, "Start date was invented")
    check(idx["same_year_boundary_rule"] == "UNKNOWN_UNTIL_DATE_ORDER_EVIDENCED", "Same-year event assumed historical")
    check(idx["date_precision_rule"] == "YEARS_ARE_EDITORIAL_APPROXIMATIONS; EXACT_DAY_NOT_ALLOWED_WITHOUT_PRIMARY_EVIDENCE",
          "Chronology falsely precise")

    refs = idx["reused_catalogues"]
    check(len(refs) == 1, "More than one inherited source of historical events")
    r = refs[0]
    check(r["path"] == "mundo/lore/diplomacy/historical_events_v0.1.json", "Broken reference to LORE-01 D")
    check(r["usage"] == "READ_BY_REFERENCE_ONLY" and r["source_of_truth"] == "LORE_01_D",
          "LORE-01 D facts copied or redefined")
    original_ids = r["retained_event_ids"]
    check(len(original_ids) == len(set(original_ids)), "Duplicate original event ID")
    check(set(original_ids) == set(diplomatic) and len(original_ids) >= 40,
          "Original event set changed, including omissions and duplications")
    check("tzenkethi_false_coup_report" in r["false_claim_event_ids"], "False Tzenkethi coup asserted")
    check(set(r["false_claim_event_ids"]) <= set(original_ids), "Unknown false information flag")
    check(diplomatic["tzenkethi_false_coup_report"]["status"] == "FALSE_CLAIM_NOT_HISTORICAL_EVENT",
          "False political claim reclassified as actual event")

    new=idx["additional_historical_anchors"]
    ids=[x["event_id"] for x in new]
    check(len(new) >= 26, "Insufficient chronology coverage")
    check(MUST_BE_PRESENT <= set(ids), "Critical chronology anchor lost")
    check(len(ids) == len(set(ids)) and not (set(ids) & set(diplomatic)), "New event ID collision with LORE-01 D")
    covered={x["time_anchor"]["reference_year"] for x in new} | {e["reference_year"] for e in diplomatic.values()}
    # 2383 tiene un hito GAME_ADDITION propio, no se declara canon de pantalla.
    covered.update(x["commissioning_target_year"] for x in idx.get("game_additions",[]))
    check(set(range(2364,2383)) <= covered, "A year of 2364–2382 lacks documentary coverage")
    allowed_hooks={"starfleet_career","political_state","ship_status","memory_history","science_research","navigation","civilian_culture"}
    for e in new:
        t=e["time_anchor"]
        check(type(t["reference_year"]) is int and 2364 <= t["reference_year"] <= 2383, "Invalid event year")
        check(t["precision"] == "YR_APPROXIMATE" and t["not_exact_date"] is True, "Invented exact historical date")
        check(e["bootstrap_condition"] == "ONLY_IF_EVENT_PRECEDES_CAMPAIGN_START", "Forced bootstrap")
        check(e["must_never_force_poststart"] is True and e["narrative_mandate"] is False, "Scripted television future")
        check(e["runtime_state_change"] is False and e["knowledge_not_universal"] is True, "Runtime/omniscience breach")
        check(e["source_era"] == "tng_ds9_voyager", "Pre-24th century campaign promoted")
        check(len(e["summary"]) >= 60, "Undocumented event claim")
        check(len(e["provenance"]) >= 1, "No evidence attached")
        for p in e["provenance"]:
            check(p["source_id"] in registry, "Unknown source " + str(p["source_id"]))
            check(p["confidence"] in {"HIGH","MEDIUM","LOW"}, "Invalid confidence")
            check("claim_scope" in p and len(p["claim_scope"]) >= 10, "Source granularity not declared")
        context=e["historical_context"]
        check(context["subject_names_are_ids"] is False and context["identity_resolution"] == "EDITORIAL_ONLY",
              "Made-up actor-instance references")
        check(len(context["named_subjects"]) >= 2, "Missing historical context")
        check(bool(e["possible_consequence_hooks"]) and set(e["possible_consequence_hooks"]) <= allowed_hooks,
              "Event hooks are invalid or executable")
        check(classify_by_year(e,t["reference_year"]) == "UNRESOLVED_SAME_YEAR", "Same-year forced history")

    predecessors=idx["historical_precedents"]
    check(len(predecessors)>=5 and len({p["precedent_id"] for p in predecessors})==len(predecessors),
          "Historical preconditions absent")
    for p in predecessors:
        check(len(p["interpretation"]) >= 60, "Historical precedent needs bounded interpretation")
        for ref in p.get("source_ids",[]):
            check(ref in registry,"Unknown predecessor evidence")
        if "source_event_id" in p:
            check(p["source_event_id"] in diplomatic,"Predecessor does not refer to existing event")

    reserves={s["source_event_id"]:s for s in idx["cross_reference_reservations"]}
    check({"borg_earth_offensive","tzenkethi_false_coup_report","dominion_cardassian_war_bajor"} <= reserves.keys(),
          "Required source conflicts not recorded")
    check(reserves["borg_earth_offensive"]["status"] == "REQUIRES_PRECISION_CHECK",
          "2366 Borg and 2367 Wolf difference concealed")
    check(reserves["tzenkethi_false_coup_report"]["status"] == "FALSE_ASSERTION_PROTECTED",
          "Tzenkethi false report reclassified")

    ships={s["class_id"]:s for s in idx["ship_temporal_reservations"]}
    for name in ("valhalla","odyssey"):
        check(name in ships and ships[name]["service_entry_year"] is None and ships[name]["approved_year"] is False,
              "Unapproved ship appears in chronology")
    check(ships.get("sovereign",{}).get("do_not_backdate") is True,"Sovereign backdate guard removed")
    check(w.get("campaign_start_year_proposed") == 2383 and w.get("expected_ensign_year") == 2387 and w.get("academy_duration_years") == 4,"Academy continuity 2383-2387 broken")
    check(ships["valhalla"].get("target_entry_year") == 2383 and ships["valhalla"].get("operational_by_cadet_graduation_target_year") == 2387,"Valhalla must be accessible to graduating ensign")
    ga=idx.get("game_additions",[])
    check(len(ga)==1 and ga[0]["kind"]=="GAME_ADDITION" and ga[0]["construction_begins_target_year"] == 2380 and ga[0]["commissioning_target_year"] == 2383, "Historical Valhalla project decision lost")
    check(ga[0]["player_can_serve_on_valhalla_as_ensign"] is True and ga[0]["do_not_assume_romulus_destroyed_in_2383"] is True,"Career or Romulus guard broken")
    check(ga[0]["gameplay_activated"] is False,"Valhalla lore unexpectedly changes runtime")
    npc={x["person"]:x for x in idx.get("npc_career_2383",[])}
    check(npc.get("Jean-Luc Picard",{}).get("post")=="almirante" and npc["Jean-Luc Picard"].get("not_permanent_valhalla_captain") is True,"Picard's 2383 rank reversed")
    check(npc.get("William Riker",{}).get("post")=="capitan_uss_titan","Riker's Titan captaincy lost")
    return {"historical_refs":len(original_ids),"additional_anchors":len(new),"years":len(covered & set(range(2364,2384))),
            "predecessors":len(predecessors),"sources":len(registry)}

def validate():
    idx=load(INDEX)
    diplomatic={e["event_id"]:e for e in load("mundo/lore/diplomacy/historical_events_v0.1.json")["events"]}
    registry={e["source_id"] for e in load("mundo/sources/source_registry/source_registry.json")["sources"]}
    check(len(registry)==len(load("mundo/sources/source_registry/source_registry.json")["sources"]), "Duplicate source ID")
    eras={name:load(f"sistemas/universe/chronology/era_profiles/{name}/era_profile.json")["playable"]
          for name in ("pike","kirk","tng_ds9_voyager")}
    stats=validate_index(idx,diplomatic,registry,eras)
    text=(ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    check("| A — Cronología y acontecimientos | ✅ COMPLETE |" in text, "Administrative closure not registered")
    check("| B — Conflictos, guerras y crisis | ⬜ TODO |" in text, "B started before approval")
    check("| C — Consecuencias y memoria histórica | ⬜ TODO |" in text,"C started without approval")
    check("| D — Continuidad/divergencia | ⬜ TODO |" in text,"D started without approval")
    check("| E — Auditoría global | ⬜ TODO |" in text,"E started without approval")
    decisions=(ROOT / "proyecto/docs/decisions/playable_eras.md").read_text(encoding="utf-8")
    check("2026-10-23" in decisions and "única época jugable" in decisions.lower(), "Author decision not registered")
    check("Only one playable era" in (ROOT/"mundo/sources/canon_policy.md").read_text(encoding="utf-8"),
          "Canon-policy reference not updated")
    atlas=(ROOT/TIMELINE).read_text(encoding="utf-8")
    for year in range(2364,2384):
        check(f"| {year} |" in atlas,"Yearly atlas has a gap")
    for id in MUST_BE_PRESENT:
        check(id in atlas,"Indexed event missing from atlas: " + id)
    check("UNRESOLVED_SAME_YEAR" in (ROOT/BOUNDARY).read_text(encoding="utf-8"), "Missing same-year examples")
    check("COMPLETE" in (ROOT/FINAL_REPORT).read_text(encoding="utf-8"), "Final audit administrative closure absent")
    check((ROOT/"proyecto/docs/roadmap/lore_03_master_plan_v0.1.md").is_file(), "Master plan missing")
    check((ROOT/"proyecto/docs/decisions/lore03a_valhalla_2383_academy.md").is_file(), "Valhalla 2383 decision missing")
    return stats

if __name__=="__main__":
    print("LORE-03 A DOCUMENTARY VALIDATION:",validate())
