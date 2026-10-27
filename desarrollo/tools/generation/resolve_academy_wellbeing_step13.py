#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

RULES_VERSION = "academy_wellbeing_balance_v0.1"
WINDOWS = {"acute": 24, "weekly": 24*7, "monthly": 24*30}
RECOVERY_FAMILIES = {"quiet_rest","solitary_leisure","social_leisure","creative_activity","holodeck","romantic_time","consensual_intimacy","exercise"}
LOAD_FAMILIES = {"study","duty","emergency_duty"}
POSITIVE_ROUTINE_FAMILIES = {"sleep","meal","exercise","quiet_rest","solitary_leisure","social_leisure","creative_activity","study"}

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def classify_ratio(ratio, good=0.9, low=0.7):
    if ratio >= good: return "adequate"
    if ratio >= low: return "reduced"
    return "insufficient"

def band_high_bad(v):
    if v >= 0.75: return "high"
    if v >= 0.45: return "elevated"
    return "normal"

def resolve(request):
    now = int(request["observation_end_hour"])
    chars = request["characters"]
    ids = [c["character_id"] for c in chars]
    if len(ids) != len(set(ids)): raise ValueError("duplicate character_id")
    by_id = {c["character_id"]: c for c in chars}
    events = sorted(request.get("confirmed_activity_events", []), key=lambda e:(int(e["end_hour"]), e["event_id"]))
    results = []
    routine_candidates = []
    rejected = []

    for ev in events:
        if ev["character_id"] not in by_id:
            rejected.append({"event_id":ev["event_id"],"reason":"unknown_character"})
            continue
        if not ev.get("confirmed", False) or not ev.get("cause_event_refs"):
            rejected.append({"event_id":ev["event_id"],"reason":"missing_confirmed_provenance"})
            continue
        if int(ev["duration_minutes"]) < 0:
            raise ValueError("negative activity duration")

    valid_events = [e for e in events if e["character_id"] in by_id and e.get("confirmed",False) and e.get("cause_event_refs")]

    for c in chars:
        cid = c["character_id"]
        profile = c["wellbeing_profile"]
        sleep_target = float(profile["sleep_target_minutes_per_24h"])
        weekly_load_cap = float(profile["max_sustainable_load_minutes_per_7d"])
        preferred = set(profile.get("preferred_recovery_activity_families", []))
        char_events = [e for e in valid_events if e["character_id"] == cid]

        window_events = {}
        for wid,hours in WINDOWS.items():
            start = now - hours
            window_events[wid] = [e for e in char_events if start < int(e["end_hour"]) <= now]

        def mins(events, families):
            return sum(int(e["duration_minutes"]) for e in events if e["activity_family"] in families)
        def stress_points(events):
            return sum(float(e.get("stress_weight",0.0)) for e in events)
        def preferred_recovery_minutes(events):
            total=0
            for e in events:
                fam=e["activity_family"]
                if fam in RECOVERY_FAMILIES:
                    base=int(e["duration_minutes"])
                    total += base if fam in preferred else base*0.5
            return total

        acute = window_events["acute"]; weekly = window_events["weekly"]; monthly = window_events["monthly"]
        sleep_24 = mins(acute, {"sleep"})
        sleep_7 = mins(weekly, {"sleep"})
        target_7 = sleep_target*7
        load_7 = mins(weekly, LOAD_FAMILIES)
        load_30 = mins(monthly, LOAD_FAMILIES)
        recovery_7 = preferred_recovery_minutes(weekly)
        recovery_30 = preferred_recovery_minutes(monthly)
        emergency_7 = mins(weekly, {"emergency_duty"})
        stress_7 = stress_points(weekly)
        stress_30 = stress_points(monthly)

        acute_sleep_ratio = sleep_24/sleep_target if sleep_target else 1.0
        weekly_sleep_ratio = sleep_7/target_7 if target_7 else 1.0
        load_ratio = load_7/weekly_load_cap if weekly_load_cap else 0.0

        acute_fatigue_score = clamp((1.0-acute_sleep_ratio)*0.75 + min(1.0, mins(acute,LOAD_FAMILIES)/720.0)*0.25, 0.0, 1.0)
        accumulated_fatigue_score = clamp((1.0-weekly_sleep_ratio)*0.6 + max(0.0,load_ratio-0.75)*0.5, 0.0, 1.0)
        stress_load_score = clamp((stress_7/10.0)*0.65 + (stress_30/40.0)*0.2 + min(1.0,emergency_7/480.0)*0.15, 0.0, 1.0)
        recovery_ratio = recovery_7 / max(420.0, weekly_load_cap*0.18)
        recovery_capacity_score = clamp(recovery_ratio,0.0,1.0)

        strain = clamp(acute_fatigue_score*0.25 + accumulated_fatigue_score*0.35 + stress_load_score*0.25 + (1.0-recovery_capacity_score)*0.15,0.0,1.0)
        if strain >= 0.75:
            balance_state="severely_imbalanced"; assistance="severely_reduced"
        elif strain >= 0.55:
            balance_state="imbalanced"; assistance="reduced"
        elif strain >= 0.35:
            balance_state="strained"; assistance="mostly_normal"
        else:
            balance_state="balanced"; assistance="normal"

        derived = {
            "acute_fatigue": band_high_bad(acute_fatigue_score),
            "accumulated_fatigue": band_high_bad(accumulated_fatigue_score),
            "stress_load": band_high_bad(stress_load_score),
            "recovery_capacity": "good" if recovery_capacity_score>=0.75 else ("limited" if recovery_capacity_score>=0.4 else "poor"),
            "sleep_acute": classify_ratio(acute_sleep_ratio),
            "sleep_weekly": classify_ratio(weekly_sleep_ratio),
            "load_balance": "overloaded" if load_ratio>1.0 else ("heavy" if load_ratio>0.8 else "sustainable"),
            "balance_state": balance_state,
            "character_side_assistance_band": assistance,
            "superhuman_bonus": False
        }

        groups={}
        for e in monthly:
            fam=e["activity_family"]
            if fam not in POSITIVE_ROUTINE_FAMILIES: continue
            key=(fam,e.get("location_ref"),e.get("typical_time_bucket"))
            groups.setdefault(key,[]).append(e)
        for (fam,loc,bucket),es in sorted(groups.items(), key=lambda x:str(x[0])):
            distinct_days=len(set(int(e["end_hour"])//24 for e in es))
            if len(es)>=3 and distinct_days>=3:
                routine_candidates.append({
                    "character_id":cid,"activity_or_pattern":fam,"typical_location":loc,
                    "typical_time_window":bucket,"observed_frequency":len(es),
                    "continuity_window":"monthly","formed_from_event_refs":[e["event_id"] for e in es],
                    "confidence":"high" if len(es)>=6 else "medium"
                })

        results.append({
            "character_id":cid,
            "window_metrics":{
                "acute":{"sleep_minutes":sleep_24,"load_minutes":mins(acute,LOAD_FAMILIES)},
                "weekly":{"sleep_minutes":sleep_7,"load_minutes":load_7,"preferred_weighted_recovery_minutes":recovery_7,"stress_points":stress_7},
                "monthly":{"load_minutes":load_30,"preferred_weighted_recovery_minutes":recovery_30,"stress_points":stress_30}
            },
            "derived_state":derived,
            "formal_consequences":[],
            "forced_player_choices":[],
            "world_truth_mutations":[]
        })

    return {
        "rules_version":RULES_VERSION,
        "character_wellbeing":sorted(results,key=lambda x:x["character_id"]),
        "routine_observation_candidates":sorted(routine_candidates,key=lambda x:(x["character_id"],x["activity_or_pattern"],str(x["typical_location"]))),
        "rejected_or_unresolved":sorted(rejected,key=lambda x:(x["event_id"],x["reason"])),
        "truth_semantics":"actual_confirmed_behavior_drives_wellbeing_not_plans",
        "formal_academic_or_disciplinary_consequences":[],
        "future_step_state":{"obligations_and_consequences":[],"campus_events":[],"offscreen_execution":[],"social_lod":[],"year_progression":[],"academy_record_writes":[]}
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"))
    print(json.dumps(resolve(payload.get("request",payload)),indent=2,sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
