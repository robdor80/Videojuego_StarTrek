#!/usr/bin/env python3
"""LORE-03 A: integridad documental. NO valida el canon escena a escena ni ejecuta runtime."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = "lore/historical_events/lore03_a_chronology_index_v0.1.json"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def check(condition, msg):
    if not condition:
        raise AssertionError(msg)

def validate_index(idx, diplomacy_ids, registry, era_profiles):
    check(idx["scope"] == "tng_ds9_voyager_only", "Unexpected era scope")
    check(idx["authority"] == "CoreRPG_World_State_ONLY", "World authority regression")
    check(idx["status"] == "IN_PROGRESS_DOCUMENTARY", "A has not been approved/merged")
    check(idx["gameplay_activated"] is False, "Runtime activation without approval")
    check(idx["auto_bootstrap_future"] is False, "Forced future canon")
    check(idx["playable_time_travel"] is False, "Playable time travel forbidden")
    window = idx["reference_window"]
    check((window["start_year"], window["end_year"]) == (2364, 2378), "Era reference interval changed")
    check(window["campaign_start_date"] is None and window["date_is_author_approved"] is False, "Campaign date invented")
    check(era_profiles == {"pike": False, "kirk": False, "tng_ds9_voyager": True}, "Playable-era filter inconsistent")
    check(set(idx["prior_eras"]) == {"pike", "kirk"}, "Historical profiles purged")
    check(all(v == "HISTORICAL_REFERENCE_ONLY" for v in idx["prior_eras"].values()), "Old eras activated")

    check(len(idx["reused_catalogues"]) == 1, "Duplicate base collection")
    refs = idx["reused_catalogues"][0]
    check(refs["path"] == "lore/diplomacy/historical_events_v0.1.json", "Wrong LORE-01 D source")
    check(refs["usage"] == "READ_BY_REFERENCE_ONLY", "History copied into another source of truth")
    original = refs["retained_event_ids"]
    check(len(original) == len(set(original)), "Duplicate original ID")
    check(set(original) <= diplomacy_ids and len(original) >= 40, "Dropped or invented original events")
    check("tzenkethi_false_coup_report" in refs["false_claim_event_ids"], "Tzenkethi false report treated as fact")
    check(set(refs["false_claim_event_ids"]) <= set(original), "Unknown false-claim tag")

    new = idx["additional_historical_anchors"]
    check(len(new) >= 4, "Missing baseline event anchors")
    event_ids = [x["event_id"] for x in new]
    check(len(event_ids) == len(set(event_ids)) and not (set(event_ids) & diplomacy_ids), "Duplicate/additional IDs collide")
    for event in new:
        time = event["time_anchor"]
        check(time["precision"] == "YR_APPROXIMATE" and time["not_exact_date"] is True, "Fabricated exact date")
        check(window["start_year"] <= time["reference_year"] <= window["end_year"], "Event outside reference period")
        check(event["bootstrap_condition"] == "ONLY_IF_EVENT_PRECEDES_CAMPAIGN_START", "Forced initial event")
        check(event["must_never_force_poststart"] is True and event["runtime_state_change"] is False, "Live state mutation")
        check(event["knowledge_not_universal"] is True, "Knowledge leaked to everyone")
        check(len(event["provenance"]) >= 1, "Evidence missing")
        for p in event["provenance"]:
            check(p["source_id"] in registry and p["confidence"] in ("HIGH", "MEDIUM", "LOW"), "Unknown source/confidence")

    ship_reservations = {x["class_id"]: x for x in idx["ship_temporal_reservations"]}
    for ship in ("valhalla", "odyssey"):
        check(ship in ship_reservations, "Ship reservation missing")
        check(ship_reservations[ship]["service_entry_year"] is None and ship_reservations[ship]["approved_year"] is False, "Future ship backdated without approval")
    check(ship_reservations["sovereign"]["do_not_backdate"] is True, "Sovereign backdating risk")
    return {"reused_historical_refs": len(original), "new_anchors": len(new), "source_count": len(registry)}

def validate():
    idx = load(INDEX)
    diplomatic = load("lore/diplomacy/historical_events_v0.1.json")
    registry = {s["source_id"] for s in load("sources/source_registry/source_registry.json")["sources"]}
    era_profiles = {e: load(f"universe/chronology/era_profiles/{e}/era_profile.json")["playable"]
                    for e in ("pike", "kirk", "tng_ds9_voyager")}
    report = validate_index(idx, {e["event_id"] for e in diplomatic["events"]}, registry, era_profiles)
    decisions = (ROOT / "docs/decisions/playable_eras.md").read_text(encoding="utf-8")
    canon = (ROOT / "sources/canon_policy.md").read_text(encoding="utf-8")
    status = (ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    check("2026-10-23" in decisions and "única época jugable" in decisions, "Decision not registered")
    check("Only one playable era" in canon, "Canon policy scope not synced")
    check("LORE-03" in status and "IN_PROGRESS" in status, "A progress not registered")
    check((ROOT / "docs/roadmap/lore_03_master_plan_v0.1.md").is_file(), "Master plan missing")
    check((ROOT / "docs/roadmap/lore_03_a_baseline_audit_v0.1.md").is_file(), "A audit missing")
    return report

if __name__ == "__main__":
    print("LORE-03 A OK — documentary validation only", validate())
