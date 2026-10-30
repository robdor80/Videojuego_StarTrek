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
    for addition in idx.get("game_additions", []):
        # Game additions may describe a technology programme rather than a hull.
        # Only real dated ship milestones contribute to historical-year coverage.
        for field in ("commissioning_target_year", "class_operational_by_year"):
            year = addition.get(field)
            if type(year) is int:
                covered.add(year)
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
    check(set(ships) >= {"valhalla","odyssey","sovereign"}, "Required ship class reservation lost")
    check(ships["odyssey"].get("service_entry_year") == 2383
          and ships["odyssey"].get("approved_year") is True
          and ships["odyssey"].get("operational_at_academy_start") is True
          and ships["odyssey"].get("exact_commissioning_date_pending") is True
          and ships["odyssey"].get("quantum_slipstream_default_equipment") is False,
          "Author-approved Odyssey 2383 or experimental technology boundary contradicted")
    check(ships["valhalla"].get("service_entry_year") == 2387
          and ships["valhalla"].get("approved_year") is True
          and ships["valhalla"].get("target_entry_year") == 2387
          and ships["valhalla"].get("construction_start_year") == 2380
          and ships["valhalla"].get("available_in_2383") is False
          and ships["valhalla"].get("exact_commissioning_date_pending") is True
          and ships["valhalla"].get("operational_by_cadet_graduation_target_year") == 2387,
          "Valhalla construction or commissioning target changed without author decision")
    check(ships.get("sovereign",{}).get("do_not_backdate") is True,"Sovereign backdate guard removed")
    check(w.get("campaign_start_year_proposed") == 2383
          and w.get("campaign_start_year_approved") == 2383
          and w.get("campaign_start_year_status") == "AUTHOR_APPROVED_YEAR_EXACT_DAY_PENDING"
          and w.get("expected_ensign_year") == 2387
          and w.get("academy_duration_years") == 4,
          "Academy continuity 2383-2387 or approved-year boundary broken")
    ga=idx.get("game_additions",[])
    additions={x.get("id"):x for x in ga}
    check(len(ga)==len(additions)==3
          and set(additions)=={"GAME_ADDITION_VALHALLA_POST_NEMESIS",
                              "GAME_ADDITION_ODYSSEY_2383",
                              "GAME_ADDITION_QUANTUM_SLIPSTREAM_ODYSSEY_VALHALLA"}
          and all(x.get("kind") == "GAME_ADDITION"
                  and x.get("gameplay_activated") is False for x in ga),
          "Unapproved game addition or premature runtime activation")
    val=additions["GAME_ADDITION_VALHALLA_POST_NEMESIS"]
    ody=additions["GAME_ADDITION_ODYSSEY_2383"]
    slip=additions["GAME_ADDITION_QUANTUM_SLIPSTREAM_ODYSSEY_VALHALLA"]
    check(val.get("construction_begins_target_year")==2380
          and val.get("commissioning_target_year")==2387
          and val.get("development_years_from_construction_start")==7
          and val.get("ship_commissioned_during_reference_2383")=="NO_NOT_YET_IN_SERVICE"
          and val.get("player_can_serve_on_valhalla_as_ensign") is True
          and val.get("do_not_assume_romulus_destroyed_in_2383") is True
          and val.get("quantum_slipstream_default_at_commissioning") is False,
          "Valhalla 2387 game addition, career or Romulus guard broken")
    check(ody.get("class_operational_by_year")==2383
          and ody.get("active_at_academy_start") is True
          and ody.get("enterprise_f_identity_not_inferred") is True
          and ody.get("quantum_slipstream_standard_on_all_ships") is False
          and ody.get("quantum_slipstream_experimental_on_selected_test_ships") is True,
          "Odyssey 2383 must not imply Enterprise-F or default slipstream")
    check(slip.get("prototype_odyssey_from_year")==2383
          and slip.get("valhalla_candidate_target_year")==2387
          and slip.get("valhalla_installed_at_commissioning_by_default") is False
          and slip.get("success_not_guaranteed") is True
          and slip.get("mission_arc_candidate") is True,
          "Experimental slipstream programme cannot be auto-installed or guaranteed")
    check((ROOT/"proyecto/docs/decisions/odyssey_valhalla_program_2383_2387_quantum_slipstream.md").is_file(),
          "General author-decision record missing")
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
    # LORE-03A must not freeze LORE-03B at TODO after an authorized merge.
    # Accept B as COMPLETE only when its documentary index records the real merge.
    b_todo = "| B — Conflictos, guerras y crisis | ⬜ TODO |" in text
    b_complete = "| B — Conflictos, guerras y crisis | ✅ COMPLETE |" in text
    check(b_todo or b_complete, "LORE-03B has an unknown administrative state")
    if b_complete:
        b = load("mundo/lore/conflicts/lore03b_dossier_index_v0.1.json")
        evidence = b.get("closure", {})
        check(b["status"] == "COMPLETE_DOCUMENTARY" and
              evidence.get("pr_number") == 41 and
              evidence.get("merge_commit_sha") == "2b1447d4469fb8f52c98486342be61c9a069b90a" and
              evidence.get("scope") == "DOCUMENTARY_ONLY" and
              evidence.get("runtime_activated") is False and
              b.get("gameplay_activated") is False,
              "LORE-03B marked COMPLETE without authoritative merge evidence")
    # LORE-03C may now be complete after PR #44; preserve an evidence-gated transition.
    c_todo = "| C — Consecuencias y memoria histórica | ⬜ TODO |" in text
    c_complete = "| C — Consecuencias y memoria histórica | ✅ COMPLETE |" in text
    check(c_todo != c_complete, "Unknown or ambiguous LORE-03C administrative state")
    if c_complete:
        c = load("mundo/lore/historical_events/lore03c_memory_casebook_v0.1.json")
        evidence = c.get("closure", {})
        check(c.get("status") == "COMPLETE_DOCUMENTARY"
              and evidence.get("pr_number") == 44
              and evidence.get("merge_commit_sha") == "56abff20c46d4614fb309e4258a44ed0eb9c33b9"
              and evidence.get("scope") == "DOCUMENTARY_ONLY"
              and evidence.get("runtime_activated") is False,
              "LORE-03C marked COMPLETE without valid GitHub merge evidence")
    # LORE-03D may be COMPLETE only after a documented, authorized PR #46 merge.
    d_todo = "| D — Continuidad/divergencia | ⬜ TODO |" in text
    d_complete = "| D — Continuidad/divergencia | ✅ COMPLETE |" in text
    check(d_todo != d_complete, "Unknown or ambiguous LORE-03D administrative state")
    if d_complete:
        d = load("proyecto/docs/roadmap/lore_03_d/D_escenarios_documentales_v0.1.json")
        closure = d.get("closure", {})
        check(d.get("status") == "COMPLETE_DOCUMENTARY"
              and closure.get("pr_number") == 46
              and closure.get("merge_commit_sha") == "6aafca0ef74787184c840c82a92386ff05f532f4"
              and closure.get("merged_at") == "2026-10-27T12:41:51Z"
              and closure.get("scope") == "DOCUMENTARY_ONLY"
              and closure.get("approved_merge") is True
              and closure.get("runtime_activated") is False
              and closure.get("checks_after_merge") == "success"
              and d.get("gameplay_activated") is False
              and d.get("auto_schedules_future_canon") is False,
              "LORE-03D marked COMPLETE without authorized merge evidence")
    e_todo = "| E — Auditoría global | ⬜ TODO |" in text
    e_complete = "| E — Auditoría global | ✅ COMPLETE |" in text
    check(e_complete and not e_todo, "LORE-03E must be administratively COMPLETE after PR #49")
    e = load("proyecto/docs/roadmap/lore_03_e/lore03_global_closure_evidence_v0.1.json")
    checks = e.get("post_merge_checks", [])
    check(e.get("phase_id") == "LORE-03E" and e.get("aggregate_id") == "LORE-03"
          and e.get("status") == "COMPLETE_DOCUMENTARY"
          and e.get("aggregate_status") == "COMPLETE_DOCUMENTARY"
          and e.get("merged_pr") == 49
          and e.get("merge_commit_sha") == "22b7e7db7a0fab138879927d6fb05ce7a43e16e7"
          and e.get("merged_at") == "2026-10-27T18:40:47Z"
          and e.get("author_approved_merge") is True
          and e.get("source_branch_deleted") is True
          and e.get("scope") == "DOCUMENTARY_ONLY"
          and e.get("runtime_verified") is False
          and e.get("gameplay_activated") is False
          and {row.get("run_id") for row in checks} == {40562209896, 40562209868}
          and all(row.get("head_sha") == e["merge_commit_sha"] and
                  row.get("conclusion") == "success" for row in checks),
          "LORE-03E closure lacks verified merger and post-merge CI evidence")
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
