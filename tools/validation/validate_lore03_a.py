#!/usr/bin/env python3
"""LORE-03 A: verifica integridad editorial, NO certifica pantalla ni implementa simulacion."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = "lore/historical_events/lore03_a_chronology_index_v0.1.json"
TIMELINE = "lore/historical_events/lore03_a_yearly_atlas_v0.2.md"
BOUNDARY = "lore/historical_events/lore03_a_date_boundary_cases_v0.2.md"
FINAL_REPORT = "docs/roadmap/lore_03_a_completion_audit_v0.2.md"
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
    check(type(campaign_year) is int and 2364 <= campaign_year <= 2378, "Campaign sample outside allowed reference window")
    y = event["time_anchor"]["reference_year"]
    if y < campaign_year:
        return "ESTABLISHED_BEFORE_D"
    if y > campaign_year:
        return "NOT_YET_AT_D"
    return "UNRESOLVED_SAME_YEAR"

def validate_index(idx, diplomatic, registry, eras):
    """Input objects kept injectable for negative mutation tests."""
    check(idx["status"] == "NEEDS_REVIEW_DOCUMENTARY", "A cannot be complete before author merge")
    check(idx["scope"] == "tng_ds9_voyager_only", "Wrong historical scope")
    check(idx["authority"] == "CoreRPG_World_State_ONLY", "CoreRPG authority missing")
    for prop in ("gameplay_activated", "auto_bootstrap_future", "playable_time_travel"):
        check(idx[prop] is False, "Unapproved gameplay feature: " + prop)
    check(eras == {"pike":False, "kirk":False, "tng_ds9_voyager":True}, "Unexpected playable-era flags")
    check(idx["prior_eras"] == {"pike":"HISTORICAL_REFERENCE_ONLY", "kirk":"HISTORICAL_REFERENCE_ONLY"},
          "Former campaigns no longer available; do not delete their history")
    w = idx["reference_window"]
    check((w["start_year"], w["end_year"]) == (2364,2378), "Reference window changed")
    check(w["campaign_start_date"] is None and w["date_is_author_approved"] is False, "Start date was invented")
    check(idx["same_year_boundary_rule"] == "UNKNOWN_UNTIL_DATE_ORDER_EVIDENCED", "Same-year event assumed historical")
    check(idx["date_precision_rule"] == "YEARS_ARE_EDITORIAL_APPROXIMATIONS; EXACT_DAY_NOT_ALLOWED_WITHOUT_PRIMARY_EVIDENCE",
          "Chronology falsely precise")

    refs = idx["reused_catalogues"]
    check(len(refs) == 1, "More than one inherited source of historical events")
    r = refs[0]
    check(r["path"] == "lore/diplomacy/historical_events_v0.1.json", "Broken reference to LORE-01 D")
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
    check(len(new) >= 20, "Insufficient chronology coverage")
    check(MUST_BE_PRESENT <= set(ids), "Critical chronology anchor lost")
    check(len(ids) == len(set(ids)) and not (set(ids) & set(diplomatic)), "New event ID collision with LORE-01 D")
    covered={x["time_anchor"]["reference_year"] for x in new} | {e["reference_year"] for e in diplomatic.values()}
    check(set(range(2364,2379)) <= covered, "A year of 2364–2378 lacks documentary coverage")
    allowed_hooks={"starfleet_career","political_state","ship_status","memory_history","science_research","navigation","civilian_culture"}
    for e in new:
        t=e["time_anchor"]
        check(type(t["reference_year"]) is int and 2364 <= t["reference_year"] <= 2378, "Invalid event year")
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
    return {"historical_refs":len(original_ids),"additional_anchors":len(new),"years":len(covered & set(range(2364,2379))),
            "predecessors":len(predecessors),"sources":len(registry)}

def validate():
    idx=load(INDEX)
    diplomatic={e["event_id"]:e for e in load("lore/diplomacy/historical_events_v0.1.json")["events"]}
    registry={e["source_id"] for e in load("sources/source_registry/source_registry.json")["sources"]}
    check(len(registry)==len(load("sources/source_registry/source_registry.json")["sources"]), "Duplicate source ID")
    eras={name:load(f"universe/chronology/era_profiles/{name}/era_profile.json")["playable"]
          for name in ("pike","kirk","tng_ds9_voyager")}
    stats=validate_index(idx,diplomatic,registry,eras)
    text=(ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    check("| A — Cronología y acontecimientos | 🟨 NEEDS_REVIEW |" in text, "Administrative gate not registered")
    check("| B — Conflictos, guerras y crisis | ⬜ TODO |" in text, "B started before approval")
    check("| C — Consecuencias y memoria histórica | ⬜ TODO |" in text,"C started without approval")
    check("| D — Continuidad/divergencia | ⬜ TODO |" in text,"D started without approval")
    check("| E — Auditoría global | ⬜ TODO |" in text,"E started without approval")
    decisions=(ROOT / "docs/decisions/playable_eras.md").read_text(encoding="utf-8")
    check("2026-10-23" in decisions and "única época jugable" in decisions.lower(), "Author decision not registered")
    check("Only one playable era" in (ROOT/"sources/canon_policy.md").read_text(encoding="utf-8"),
          "Canon-policy reference not updated")
    atlas=(ROOT/TIMELINE).read_text(encoding="utf-8")
    for year in range(2364,2379):
        check(f"| {year} |" in atlas,"Yearly atlas has a gap")
    for id in MUST_BE_PRESENT:
        check(id in atlas,"Indexed event missing from atlas: " + id)
    check("UNRESOLVED_SAME_YEAR" in (ROOT/BOUNDARY).read_text(encoding="utf-8"), "Missing same-year examples")
    check("NEEDS_REVIEW" in (ROOT/FINAL_REPORT).read_text(encoding="utf-8"), "Final audit absent")
    check((ROOT/"docs/roadmap/lore_03_master_plan_v0.1.md").is_file(), "Master plan missing")
    return stats

if __name__=="__main__":
    print("LORE-03 A DOCUMENTARY VALIDATION:",validate())
