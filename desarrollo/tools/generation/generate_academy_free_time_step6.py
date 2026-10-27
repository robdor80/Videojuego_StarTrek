#!/usr/bin/env python3
"""Deterministic reference free-time planner for Academy Life Step 6."""
from __future__ import annotations
import argparse, copy, hashlib, heapq, json
from pathlib import Path
from typing import Any

RULES_VERSION="academy_free_time_v0.1"

def stable_hex(*parts: Any,size:int=16)->str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def travel_graph(request:dict[str,Any])->dict[str,list[tuple[str,int]]]:
    g:dict[str,list[tuple[str,int]]]={}
    for e in request.get("travel_edges",[]):
        a,b,m=e["from"],e["to"],int(e["minutes"])
        if m<0: raise ValueError("negative travel time")
        g.setdefault(a,[]).append((b,m))
        if e.get("bidirectional",True): g.setdefault(b,[]).append((a,m))
    return g

def travel_minutes(g:dict[str,list[tuple[str,int]]],a:str,b:str)->int|None:
    if a==b:return 0
    q=[(0,a)];seen={}
    while q:
        d,n=heapq.heappop(q)
        if n in seen and seen[n]<=d:continue
        seen[n]=d
        if n==b:return d
        for nxt,c in g.get(n,[]):heapq.heappush(q,(d+c,nxt))
    return None

def overlaps(a:dict[str,Any],b:dict[str,Any])->bool:
    return a["day_index"]==b["day_index"] and a["start_minute"]<b["end_minute"] and b["start_minute"]<a["end_minute"]

def build_free_time(request:dict[str,Any])->dict[str,Any]:
    seed=request["campaign_seed"];cadets=copy.deepcopy(request["cadets"]);windows=copy.deepcopy(request["free_time_windows"])
    activities=copy.deepcopy(request["activities"]);locations=copy.deepcopy(request["locations"]);g=travel_graph(request)
    slots=[c["population_slot_ref"] for c in cadets]
    if len(slots)!=len(set(slots)):raise ValueError("duplicate cadet population_slot_ref")
    by_slot={c["population_slot_ref"]:c for c in cadets}
    loc_caps={x["location_ref"]:set(x.get("capability_tags",[])) for x in locations}
    authorized=set(request.get("authorized_leave_slot_refs",[]))
    player_choices={(x["population_slot_ref"],x["window_ref"]):x["activity_id"] for x in request.get("player_choice_requests",[])}
    capacity_usage:list[dict[str,Any]]=[];npc_plans=[];player_options=[];accepted_player=[];unresolved=[];remaining=[]

    def feasible(slot:str,w:dict[str,Any],activity_id:str)->list[dict[str,Any]]:
        a=activities[activity_id]
        if a.get("requires_authorized_leave",False) and slot not in authorized:return []
        out=[]
        for loc in sorted(loc_caps):
            if a.get("allowed_location_refs") and loc not in a["allowed_location_refs"]:continue
            if not set(a.get("required_capabilities",[])).issubset(loc_caps[loc]):continue
            tin=travel_minutes(g,w["start_location_ref"],loc);tout=travel_minutes(g,loc,w["end_location_ref"])
            if tin is None or tout is None:continue
            usable=int(w["end_minute"])-int(w["start_minute"])-tin-tout
            minimum=int(a["min_minutes"]);maximum=int(a["max_minutes"])
            if usable<minimum:continue
            duration=min(maximum,usable)
            start=int(w["start_minute"])+tin;end=start+duration
            cap=a.get("capacity")
            candidate={"population_slot_ref":slot,"window_ref":w["window_ref"],"activity_id":activity_id,
              "activity_family":a["family"],"location_ref":loc,"day_index":int(w["day_index"]),
              "start_minute":start,"end_minute":end,"travel_in_minutes":tin,"travel_out_minutes":tout,
              "plan_state":"candidate","automatic_relationship_effect":"none","actual_execution":"unresolved"}
            if cap is not None:
                concurrent=sum(1 for x in capacity_usage if x["activity_id"]==activity_id and x["location_ref"]==loc and overlaps(x,candidate))
                if concurrent>=int(cap):continue
            out.append(candidate)
        return out

    ordered_windows=sorted(windows,key=lambda w:(w["day_index"],w["start_minute"],w["population_slot_ref"],w["window_ref"]))
    for w in ordered_windows:
        slot=w["population_slot_ref"]
        if slot not in by_slot:raise ValueError("free-time window references unknown cadet")
        if int(w["start_minute"])>=int(w["end_minute"]):raise ValueError("invalid free-time window")
        cadet=by_slot[slot];is_player=bool(cadet.get("is_player",False))
        affinities=set(cadet.get("hobby_refs",[]))|set(cadet.get("interest_refs",[]))|set(cadet.get("free_time_preference_refs",[]))
        candidates=[]
        for aid in sorted(activities):
            for c in feasible(slot,w,aid):
                score=len(affinities & set(activities[aid].get("affinity_refs",[])))
                c["_affinity_score"]=score
                candidates.append(c)
        candidates.sort(key=lambda c:(-c["_affinity_score"],stable_hex(seed,"choice",slot,w["window_ref"],c["activity_id"],c["location_ref"],RULES_VERSION)))

        if is_player:
            for c in candidates:
                option={k:v for k,v in c.items() if not k.startswith("_")};option["plan_state"]="player_option";player_options.append(option)
            requested=player_choices.get((slot,w["window_ref"]))
            if requested is not None:
                valid=[c for c in candidates if c["activity_id"]==requested]
                if not valid:
                    unresolved.append({"population_slot_ref":slot,"window_ref":w["window_ref"],"reason":"invalid_player_choice","requested_activity_id":requested})
                else:
                    chosen=valid[0];entry={k:v for k,v in chosen.items() if not k.startswith("_")};entry["plan_state"]="accepted_player_choice";accepted_player.append(entry);capacity_usage.append(entry)
                    remaining.append({"population_slot_ref":slot,"window_ref":w["window_ref"],"classification":"partially_unallocated_or_consumed_by_player_choice"})
            else:
                remaining.append({"population_slot_ref":slot,"window_ref":w["window_ref"],"classification":"player_unallocated_pending_choice"})
            continue

        if not candidates:
            remaining.append({"population_slot_ref":slot,"window_ref":w["window_ref"],"classification":"unallocated_no_feasible_activity"})
            continue
        chosen=candidates[0];entry={k:v for k,v in chosen.items() if not k.startswith("_")};entry["plan_state"]="planned";npc_plans.append(entry);capacity_usage.append(entry)
        used=(entry["end_minute"]-entry["start_minute"])+entry["travel_in_minutes"]+entry["travel_out_minutes"]
        total=int(w["end_minute"])-int(w["start_minute"])
        if used<total:
            remaining.append({"population_slot_ref":slot,"window_ref":w["window_ref"],"classification":"partially_unallocated","remaining_minutes":total-used})

    return {
      "rules_version":RULES_VERSION,
      "npc_free_time_plans":sorted(npc_plans,key=lambda x:(x["population_slot_ref"],x["day_index"],x["start_minute"],x["activity_id"])),
      "player_feasible_options":sorted(player_options,key=lambda x:(x["window_ref"],x["activity_id"],x["location_ref"])),
      "accepted_player_choices":sorted(accepted_player,key=lambda x:(x["window_ref"],x["activity_id"])),
      "remaining_unallocated_intervals":sorted(remaining,key=lambda x:(x["population_slot_ref"],x["window_ref"])),
      "unresolved_choices":sorted(unresolved,key=lambda x:(x["population_slot_ref"],x["window_ref"])),
      "automatic_relationship_effect":"none",
      "plan_truth_semantics":"intention_not_actual_execution",
      "future_step_state":{"extracurricular_assignments":[],"conference_or_additional_course_assignments":[],"social_events":[],"romance_state":[],"relationship_changes":[],"wellbeing_effects":[],"disciplinary_consequences":[],"offscreen_execution":[]}
    }

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(build_free_time(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
