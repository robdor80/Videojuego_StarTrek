#!/usr/bin/env python3
"""Deterministic reference extracurricular membership planner for Academy Life Step 7."""
from __future__ import annotations
import argparse,copy,hashlib,heapq,json
from pathlib import Path
from typing import Any

RULES_VERSION="academy_extracurricular_v0.1"

def stable_hex(*parts:Any,size:int=16)->str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def graph(request:dict[str,Any])->dict[str,list[tuple[str,int]]]:
    g={}
    for e in request.get("travel_edges",[]):
        a,b,m=e["from"],e["to"],int(e["minutes"])
        if m<0: raise ValueError("negative travel time")
        g.setdefault(a,[]).append((b,m))
        if e.get("bidirectional",True):g.setdefault(b,[]).append((a,m))
    return g

def travel(g,a,b):
    if a==b:return 0
    q=[(0,a)];seen={}
    while q:
        d,n=heapq.heappop(q)
        if n in seen and seen[n]<=d:continue
        seen[n]=d
        if n==b:return d
        for nxt,c in g.get(n,[]):heapq.heappush(q,(d+c,nxt))
    return None

def fits_session(slot:str,session:dict[str,Any],windows:list[dict[str,Any]],g)->bool:
    for w in windows:
        if w["population_slot_ref"]!=slot or int(w["day_index"])!=int(session["day_index"]):continue
        tin=travel(g,w["start_location_ref"],session["location_ref"])
        tout=travel(g,session["location_ref"],w["end_location_ref"])
        if tin is None or tout is None:continue
        if int(w["start_minute"])+tin<=int(session["start_minute"]) and int(session["end_minute"])+tout<=int(w["end_minute"]):
            return True
    return False

def eligible(cadet:dict[str,Any],act:dict[str,Any])->bool:
    allowed=act.get("allowed_cadet_class_ids")
    if allowed and cadet.get("cadet_class_id") not in allowed:return False
    required=set(act.get("required_qualification_refs",[]))
    if not required.issubset(set(cadet.get("qualification_refs",[]))):return False
    if act.get("required_specialization_ids") and cadet.get("specialization") not in act["required_specialization_ids"]:return False
    return True

def build_memberships(request:dict[str,Any])->dict[str,Any]:
    seed=request["campaign_seed"];cadets=copy.deepcopy(request["cadets"]);acts=copy.deepcopy(request["activities"])
    windows=copy.deepcopy(request["free_time_windows"]);g=graph(request)
    slots=[c["population_slot_ref"] for c in cadets]
    if len(slots)!=len(set(slots)):raise ValueError("duplicate cadet population_slot_ref")
    by_slot={c["population_slot_ref"]:c for c in cadets}
    loc_caps={x["location_ref"]:set(x.get("capability_tags",[])) for x in request.get("locations",[])}
    existing=copy.deepcopy(request.get("existing_memberships",[]))
    player_requests={(x["population_slot_ref"],x["extracurricular_id"]) for x in request.get("player_join_requests",[])}
    max_memberships=int(request.get("max_active_memberships_per_cadet",2))
    if max_memberships<0:raise ValueError("invalid membership limit")

    rosters={aid:[] for aid in acts};memberships=[];schedule_entries=[];rejected=[];player_options=[]
    active_count_by_slot={s:0 for s in slots}

    def act_feasible(slot,aid):
        a=acts[aid]
        if not eligible(by_slot[slot],a):return False,"ineligible"
        caps=set(a.get("required_location_capabilities",[]))
        if not caps.issubset(loc_caps.get(a["location_ref"],set())):return False,"facility_unavailable"
        for session in a.get("recurring_sessions",[]):
            s=dict(session);s["location_ref"]=a["location_ref"]
            if int(s["start_minute"])>=int(s["end_minute"]):raise ValueError("invalid recurring session")
            if not fits_session(slot,s,windows,g):return False,"schedule_or_travel_conflict"
        return True,None

    # Preserve valid existing active memberships first.
    for m in sorted(existing,key=lambda x:(x["extracurricular_id"],x["population_slot_ref"])):
        slot=m["population_slot_ref"];aid=m["extracurricular_id"]
        if slot not in by_slot or aid not in acts:raise ValueError("existing membership references unknown entity")
        if m.get("membership_state","active")!="active":continue
        cap=int(acts[aid]["capacity"])
        ok,reason=act_feasible(slot,aid)
        if not ok:rejected.append({"population_slot_ref":slot,"extracurricular_id":aid,"reason":"existing_membership_invalid_"+reason});continue
        if len(rosters[aid])>=cap:raise ValueError("existing memberships exceed extracurricular capacity")
        if active_count_by_slot[slot]>=max_memberships:raise ValueError("existing memberships exceed cadet membership limit")
        rosters[aid].append(slot);active_count_by_slot[slot]+=1
        memberships.append({"membership_id":m.get("membership_id",f"xm:{aid}:{slot}"),"extracurricular_id":aid,"population_slot_ref":slot,"membership_state":"active","source":"existing_preserved","automatic_relationship_effect":"none","automatic_skill_or_grade_effect":"none"})

    def options_for(slot):
        c=by_slot[slot];aff=set(c.get("hobby_refs",[]))|set(c.get("interest_refs",[]))|set(c.get("extracurricular_preference_refs",[]))
        opts=[]
        for aid in sorted(acts):
            if slot in rosters[aid]:continue
            ok,reason=act_feasible(slot,aid)
            if not ok:continue
            if len(rosters[aid])>=int(acts[aid]["capacity"]):continue
            score=len(aff & set(acts[aid].get("affinity_refs",[])))
            opts.append((aid,score,stable_hex(seed,"xm",slot,aid,RULES_VERSION)))
        return sorted(opts,key=lambda x:(-x[1],x[2],x[0]))

    # Player options and explicit requests.
    for slot in sorted(slots):
        c=by_slot[slot]
        if not c.get("is_player",False):continue
        for aid,score,_ in options_for(slot):
            player_options.append({"population_slot_ref":slot,"extracurricular_id":aid,"affinity_score":score,"state":"eligible_option"})
        requested=sorted(aid for s,aid in player_requests if s==slot)
        for aid in requested:
            if aid not in acts:
                rejected.append({"population_slot_ref":slot,"extracurricular_id":aid,"reason":"unknown_activity"});continue
            if active_count_by_slot[slot]>=max_memberships:
                rejected.append({"population_slot_ref":slot,"extracurricular_id":aid,"reason":"membership_limit"});continue
            valid={x[0] for x in options_for(slot)}
            if aid not in valid:
                ok,reason=act_feasible(slot,aid)
                if ok and len(rosters[aid])>=int(acts[aid]["capacity"]):reason="capacity_full"
                rejected.append({"population_slot_ref":slot,"extracurricular_id":aid,"reason":reason or "not_available"});continue
            rosters[aid].append(slot);active_count_by_slot[slot]+=1
            memberships.append({"membership_id":f"xm:{aid}:{slot}","extracurricular_id":aid,"population_slot_ref":slot,"membership_state":"active","source":"explicit_player_choice","automatic_relationship_effect":"none","automatic_skill_or_grade_effect":"none"})

    # NPC candidates compete globally by affinity then deterministic tiebreak.
    candidates=[]
    for slot in sorted(slots):
        if by_slot[slot].get("is_player",False):continue
        if active_count_by_slot[slot]>=max_memberships:continue
        for aid,score,tie in options_for(slot):candidates.append((-score,tie,slot,aid))
    for _,__,slot,aid in sorted(candidates):
        if active_count_by_slot[slot]>=max_memberships:continue
        if slot in rosters[aid]:continue
        if len(rosters[aid])>=int(acts[aid]["capacity"]):continue
        # One autonomous new enrollment per NPC in this reference pass unless existing membership already consumes limit.
        if any(m["population_slot_ref"]==slot and m["source"]=="npc_autonomous" for m in memberships):continue
        rosters[aid].append(slot);active_count_by_slot[slot]+=1
        memberships.append({"membership_id":f"xm:{aid}:{slot}","extracurricular_id":aid,"population_slot_ref":slot,"membership_state":"active","source":"npc_autonomous","automatic_relationship_effect":"none","automatic_skill_or_grade_effect":"none"})

    for m in memberships:
        aid=m["extracurricular_id"];slot=m["population_slot_ref"]
        for i,s in enumerate(acts[aid].get("recurring_sessions",[])):
            schedule_entries.append({"entry_id":f'extracurricular:{aid}:{slot}:{i}',"population_slot_ref":slot,"extracurricular_id":aid,"entry_type":"extracurricular_recurring","day_index":int(s["day_index"]),"start_minute":int(s["start_minute"]),"end_minute":int(s["end_minute"]),"location_ref":acts[aid]["location_ref"],"obligation_level":"voluntary_recurring_commitment","actual_attendance":"unresolved"})

    return {
      "rules_version":RULES_VERSION,
      "memberships":sorted(memberships,key=lambda x:(x["population_slot_ref"],x["extracurricular_id"])),
      "rosters":{aid:sorted(rosters[aid]) for aid in sorted(rosters)},
      "recurring_schedule_entries":sorted(schedule_entries,key=lambda x:(x["population_slot_ref"],x["day_index"],x["start_minute"],x["extracurricular_id"])),
      "player_eligible_options":sorted(player_options,key=lambda x:(x["population_slot_ref"],x["extracurricular_id"])),
      "rejected_or_unresolved":sorted(rejected,key=lambda x:(x["population_slot_ref"],x["extracurricular_id"],x["reason"])),
      "membership_truth_semantics":"membership_not_attendance",
      "automatic_relationship_effect":"none",
      "automatic_skill_grade_reputation_wellbeing_effect":"none",
      "future_step_state":{"conference_or_additional_course_assignments":[],"social_events":[],"romance_state":[],"relationship_changes":[],"mentor_changes":[],"wellbeing_effects":[],"disciplinary_consequences":[],"offscreen_execution":[]}
    }

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(build_memberships(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
