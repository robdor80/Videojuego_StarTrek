#!/usr/bin/env python3
"""LORE-03D: pure editorial gate checks. NOT a WorldState engine or CoreRPG test."""
from pathlib import Path
import json
from datetime import date

ROOT = Path(__file__).resolve().parents[3]
CASEBOOK = "proyecto/docs/roadmap/lore_03_d/D_escenarios_documentales_v0.1.json"
DOCROOT = "proyecto/docs/roadmap/lore_03_d"
BASE = "mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json"
ALLOWED = {"ALLOW", "REJECT", "UNRESOLVED"}
KINDS = {"historical_rewrite","future_canon","initial_context","same_year","autonomous_event",
         "knowledge","save_isolation","roundtrip","identity_roundtrip","death_continuity",
         "career","assignment","technology","false_report","time_travel"}
REQUIRED = {
  "historical_rewrite": ("event_ref","effective_year","changes_verified_past"),
  "future_canon": ("event_label","effective_year","source","mandatory"),
  "initial_context": ("start_year","romulus_exists","picard_rank","riker_ship"),
  "same_year": ("event_year","start_year","event_exact_date","cutoff_exact_date","order_evidence"),
  "autonomous_event": ("effective_year","cause_refs","authorizer","resource_evidence","actor_available"),
  "knowledge": ("event_year","learned_year","channel","classified","has_clearance"),
  "save_isolation": ("campaign_id","source_campaign_id"),
  "roundtrip": ("history_prefix_before","history_prefix_after","replays_effects"),
  "identity_roundtrip": ("entity_id_before","entity_id_after","rules_migrated"),
  "death_continuity": ("identity_retained","universal_grief"),
  "career": ("effective_year","event_type","authority_ref","performance_ref"),
  "assignment": ("graduation_year","required_qualification","authorized_vacancy","guaranteed_assignment"),
  "technology": ("candidate_name","validated_research","institutional_approval","ship_installation"),
  "false_report": ("event_ref","claims_actual_coup"),
  "time_travel": ("player_time_rewrite",)
}

class InvalidLore03D(ValueError):
    pass

def demand(cond, message):
    if not cond:
        raise InvalidLore03D(message)

def load(relpath, root=ROOT):
    return json.loads((root / relpath).read_text(encoding="utf-8"))

def classification(year, start_year=2383, order=None):
    """Editorial three-way comparison; never invent a day within the same year."""
    demand(type(year) is int and type(start_year) is int, "Bad year")
    if year < start_year: return "PAST_YEAR"
    if year > start_year: return "FUTURE_YEAR"
    if order == "BEFORE" or order == "AFTER": return order
    return "UNRESOLVED_SAME_YEAR"

def judge(s):
    """Does not produce events; accepts/rejects illustrative input only."""
    kind, p = s["kind"], s["input"]
    demand(kind in KINDS, "Unknown scenario kind")
    demand(isinstance(p, dict) and set(REQUIRED[kind]) <= set(p), "Missing scenario evidence")
    if kind == "historical_rewrite":
        demand(p["event_ref"] == "wolf_359_battle", "Unknown fixture historical anchor")
        demand(type(p["effective_year"]) is int and p["effective_year"] < 2383, "Not prestart")
        return "REJECT" if p["changes_verified_past"] else "ALLOW"
    if kind == "future_canon":
        demand(p["source"] == "SCREEN_CANON_FUTURE" and p["effective_year"] > 2383, "Not screen future")
        return "REJECT" if p["mandatory"] else "ALLOW"
    if kind == "initial_context":
        demand(p["start_year"] == 2383, "Unknown baseline")
        return "ALLOW" if p["romulus_exists"] is True and p["picard_rank"] == "admiral" and p["riker_ship"] == "USS Titan" else "REJECT"
    if kind == "same_year":
        demand(p["event_year"] == p["start_year"] == 2383, "Test is not same-year")
        if not p["order_evidence"] or not p["event_exact_date"] or not p["cutoff_exact_date"]:
            return "UNRESOLVED"
        a,b=date.fromisoformat(p["event_exact_date"]),date.fromisoformat(p["cutoff_exact_date"])
        demand(a.year == b.year == 2383, "Fabricated wrong-year exact dates")
        return "ALLOW" if a < b else "REJECT"
    if kind == "autonomous_event":
        demand(type(p["effective_year"]) is int and p["effective_year"] > 2383, "Not future")
        if p.get("requires_player_presence") is True: return "REJECT"
        return "ALLOW" if p["cause_refs"] and p["authorizer"] == "CoreRPG" and p["resource_evidence"] is True and p["actor_available"] is True else "REJECT"
    if kind == "knowledge":
        demand(p["channel"] in {"authorized_report","direct_observation","rumor"}, "Unknown channel")
        if p["learned_year"] < p["event_year"]: return "REJECT"
        if p["classified"] and (not p["has_clearance"] or p["channel"] == "rumor"): return "REJECT"
        return "ALLOW"
    if kind == "save_isolation":
        return "ALLOW" if p["campaign_id"] == p["source_campaign_id"] else "REJECT"
    if kind == "roundtrip":
        return "ALLOW" if p["history_prefix_before"] == p["history_prefix_after"] and p["replays_effects"] is False else "REJECT"
    if kind == "identity_roundtrip":
        return "ALLOW" if p["entity_id_before"] == p["entity_id_after"] and not p["rules_migrated"] else "REJECT"
    if kind == "death_continuity":
        return "ALLOW" if p["identity_retained"] is True and p["universal_grief"] is False else "REJECT"
    if kind == "career":
        demand(p["event_type"] == "promotion", "Only promotion fixture supported")
        return "ALLOW" if p["authority_ref"] and p["performance_ref"] else "REJECT"
    if kind == "assignment":
        return "ALLOW" if p["required_qualification"] and p["authorized_vacancy"] and not p["guaranteed_assignment"] else "REJECT"
    if kind == "technology":
        demand(p["candidate_name"] == "Sensores Rise", "Unexpected example")
        return "ALLOW" if p["validated_research"] and p["institutional_approval"] and p["ship_installation"] else "REJECT"
    if kind == "false_report":
        demand(p["event_ref"] == "tzenkethi_false_coup_report", "Not the known false report")
        return "REJECT" if p["claims_actual_coup"] else "ALLOW"
    if kind == "time_travel":
        return "REJECT" if p["player_time_rewrite"] else "ALLOW"
    raise InvalidLore03D("Unreachable")

def validate_scenario(s):
    demand(isinstance(s.get("id"),str) and s["id"].startswith("T") and
           s.get("kind") in KINDS and s.get("expected_decision") in ALLOWED and
           len(s.get("title","")) >= 12 and s.get("non_runtime_hypothetical") is True,
           "Bad case identity or status")
    result=judge(s)
    demand(result == s["expected_decision"], s["id"]+": expected "+s["expected_decision"]+", got "+result)
    return result

def validate_closure(pack):
    """Validate immutable documentary merge evidence, not live GitHub state."""
    e=pack.get("closure", {})
    demand(pack.get("status") == "COMPLETE_DOCUMENTARY", "D is not administratively closed")
    demand(e.get("pr_number") == 46 and e.get("merged_to") == "main"
           and e.get("merged_at") == "2026-10-27T12:41:51Z"
           and e.get("merge_commit_sha") == "6aafca0ef74787184c840c82a92386ff05f532f4"
           and e.get("source_head_sha") == "4db0dc7d3ccdb468594d9fde6789beae83ddfe7f",
           "LORE-03D merge identity was fabricated")
    demand(e.get("scope") == "DOCUMENTARY_ONLY"
           and e.get("approved_merge") is True
           and e.get("runtime_activated") is False
           and e.get("branch_deleted_at_audit") is False
           and e.get("checks_after_merge") == "success"
           and e.get("check_run_ids") == [40505811905, 40505812149]
           and e.get("tests_documentary") == 45
           and e.get("scenario_count") == 35,
           "LORE-03D closure misstates scope, CI, tests or branch deletion")
    return e

def validate(root=ROOT):
    pack=load(CASEBOOK,root)
    validate_closure(pack)
    demand(pack["status"] == "COMPLETE_DOCUMENTARY" and
           pack["scope"] == "EDITORIAL_REFERENCE_ONLY" and
           pack["world_state_authority"] == "CoreRPG_ONLY", "Invalid authority or status")
    demand(pack["campaign_start_year_proposed"] == 2383 and
           pack["campaign_start_exact_date"] is None and
           pack["era"] == "tng_ds9_voyager", "Invented date/era")
    for field in ("playable_time_travel","gameplay_activated","creates_runtime_events",
                  "creates_new_canonical_events","auto_schedules_future_canon","changes_historical_sources"):
        demand(pack[field] is False, "Runtime or future was enabled: "+field)
    refs=pack["sources"]
    demand(len(refs) >= 10 and len(set(refs)) == len(refs), "Missing source coverage/duplicate reference")
    for f in refs: demand((root / f).is_file(), "Missing existing owner: "+f)
    history=load("mundo/lore/diplomacy/historical_events_v0.1.json",root)["events"]
    timeline=load(BASE,root)["additional_historical_anchors"]
    b=load("mundo/lore/conflicts/lore03b_dossier_index_v0.1.json",root)
    c=load("mundo/lore/historical_events/lore03c_memory_casebook_v0.1.json",root)
    demand(len(history)==40 and len(timeline)==26 and b["expected_dossiers"]==22 and
           c["status"]=="COMPLETE_DOCUMENTARY" and len(c["cases"])==13,
           "Earlier phase corpus changed")
    demand(any(e["event_id"]=="wolf_359_battle" for e in timeline), "Missing Wolf 359")
    demand(any(e["event_id"]=="tzenkethi_false_coup_report" and
               e["status"]=="FALSE_CLAIM_NOT_HISTORICAL_EVENT" for e in history), "False coup promoted")
    docs=("README.md", "D01_auditoria_y_arquitectura.md", "D02_estado_inicial_corte_temporal.md",
          "D03_divergencia_futuro_abierto.md", "D04_autonomia_galactica.md",
          "D05_causalidad_y_consecuencias.md", "D06_npc_naves_organizaciones.md",
          "D07_historia_por_partida.md", "D08_auditoria_y_cierre.md")
    for f in docs:
        file=root / DOCROOT / f
        demand(file.is_file() and len(file.read_text(encoding="utf-8"))>1000, "Missing D document: "+f)
    scenarios=pack["scenarios"]
    demand(len(scenarios)>=30, "Insufficient negative coverage")
    ids=[s.get("id") for s in scenarios]
    demand(len(ids)==len(set(ids)) and set(ids)>=set("T%02d"%i for i in range(1,19)), "Duplicate/missing mandatory scenarios")
    outcomes=[validate_scenario(s) for s in scenarios]
    demand(all(k in {s["kind"] for s in scenarios} for k in KINDS), "Missing type coverage")
    demand(outcomes.count("REJECT")>=16 and outcomes.count("ALLOW")>=12 and outcomes.count("UNRESOLVED")>=2, "Insufficient outcome coverage")
    demand(classification(2383)=="UNRESOLVED_SAME_YEAR"
           and classification(2378)=="PAST_YEAR"
           and classification(2387)=="FUTURE_YEAR", "Temporal cutoff regression")
    return {"status":"COMPLETE_DOCUMENTARY","cases":len(scenarios),
            "rejected":outcomes.count("REJECT"),"allowed":outcomes.count("ALLOW"),
            "unresolved":outcomes.count("UNRESOLVED"),"earlier_dossiers":22,
            "authority":"CoreRPG_ONLY","runtime_verified":False}

if __name__ == "__main__":
    print(json.dumps(validate(),ensure_ascii=False,indent=2))
