#!/usr/bin/env python3
"""Deterministic reference social-life planner for Academy Life Step 9."""
from __future__ import annotations
import argparse, copy, hashlib, heapq, json
from pathlib import Path
from typing import Any

RULES_VERSION="academy_social_life_v0.1"
VALID_ACCESS={"open_gathering","invitation_required"}
ROMANTIC_FAMILIES={"romantic_expression","romantic_date","sexual_intimacy","dating"}

def stable_hex(*parts:Any,size:int=16)->str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def make_graph(request):
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

def window_fits(slot,opp,windows,g):
    for w in windows:
        if w["population_slot_ref"]!=slot or int(w["day_index"])!=int(opp["day_index"]):continue
        tin=travel(g,w["start_location_ref"],opp["location_ref"])
        tout=travel(g,opp["location_ref"],w["end_location_ref"])
        if tin is None or tout is None:continue
        if int(w["start_minute"])+tin<=int(opp["start_minute"]) and int(opp["end_minute"])+tout<=int(w["end_minute"]):
            return True
    return False

def build_social_plans(request):
    seed=request["campaign_seed"];cadets=copy.deepcopy(request["cadets"]);opps=copy.deepcopy(request["social_opportunities"])
    windows=copy.deepcopy(request["available_windows"]);g=make_graph(request)
    slots=[c["population_slot_ref"] for c in cadets]
    if len(slots)!=len(set(slots)):raise ValueError("duplicate cadet population_slot_ref")
    by_slot={c["population_slot_ref"]:c for c in cadets}
    loc_caps={x["location_ref"]:set(x.get("capability_tags",[])) for x in request.get("locations",[])}
    circles={x["social_circle_id"]:set(x.get("member_slot_refs",[])) for x in request.get("social_circles",[])}
    existing=copy.deepcopy(request.get("existing_social_plans",[]))
    player_responses={(x["population_slot_ref"],x["social_opportunity_id"]):x["response"] for x in request.get("player_rsvp_responses",[])}
    plans=[];declined=[];player_options=[];rejected=[];rosters={oid:[] for oid in opps}

    for oid,o in opps.items():
        if o.get("access_mode") not in VALID_ACCESS:raise ValueError("invalid social access mode")
        if o.get("event_family") in ROMANTIC_FAMILIES:raise ValueError("Step 9 cannot generate romantic/sexual social events")
        if int(o.get("capacity",0))<0:raise ValueError("negative social capacity")
        if int(o["start_minute"])>=int(o["end_minute"]):raise ValueError("invalid social interval")
        caps=set(o.get("required_location_capabilities",[]))
        if not caps.issubset(loc_caps.get(o["location_ref"],set())):o["_facility_valid"]=False
        else:o["_facility_valid"]=True

    def context_eligible(slot,oid):
        o=opps[oid]
        circles_req=o.get("eligible_circle_refs",[])
        if circles_req and not any(slot in circles.get(cid,set()) for cid in circles_req):return False
        if o["access_mode"]=="invitation_required" and slot not in set(o.get("invited_slot_refs",[])):return False
        return True

    def feasible(slot,oid):
        o=opps[oid]
        if not o["_facility_valid"]:return False,"facility_unavailable"
        if not context_eligible(slot,oid):return False,"not_invited_or_context_ineligible"
        if not window_fits(slot,o,windows,g):return False,"schedule_or_travel_conflict"
        return True,None

    def add_plan(slot,oid,source,plan_id=None):
        rosters[oid].append(slot)
        plans.append({
          "social_plan_id":plan_id or f"social:{oid}:{slot}","social_opportunity_id":oid,"population_slot_ref":slot,
          "plan_state":"planned","source":source,"attendance_state":"unresolved","interaction_state":"unresolved",
          "relationship_effect":"none_until_confirmed_interaction","romantic_or_sexual_effect":"prohibited_step_9"
        })

    for p in sorted(existing,key=lambda x:(x["social_opportunity_id"],x["population_slot_ref"])):
        slot=p["population_slot_ref"];oid=p["social_opportunity_id"]
        if slot not in by_slot or oid not in opps:raise ValueError("existing social plan references unknown entity")
        ok,reason=feasible(slot,oid)
        if not ok:
            rejected.append({"population_slot_ref":slot,"social_opportunity_id":oid,"reason":"existing_plan_invalid_"+str(reason)});continue
        if len(rosters[oid])>=int(opps[oid]["capacity"]):raise ValueError("existing social plans exceed capacity")
        add_plan(slot,oid,"existing_preserved",p.get("social_plan_id"))

    def options_for(slot):
        c=by_slot[slot]
        pref=set(c.get("social_preference_refs",[]))|set(c.get("interest_refs",[]))|set(c.get("hobby_refs",[]))
        out=[]
        for oid in sorted(opps):
            if slot in rosters[oid]:continue
            ok,_=feasible(slot,oid)
            if not ok:continue
            score=len(pref & set(opps[oid].get("preference_tags",[])))
            out.append((oid,score,stable_hex(seed,"social",slot,oid,RULES_VERSION)))
        return sorted(out,key=lambda x:(-x[1],x[2],x[0]))

    # Player sees options and explicitly RSVPs.
    for slot in sorted(slots):
        if not by_slot[slot].get("is_player",False):continue
        for oid,score,_ in options_for(slot):
            state="available" if len(rosters[oid])<int(opps[oid]["capacity"]) else "full"
            player_options.append({"population_slot_ref":slot,"social_opportunity_id":oid,"state":state,"affinity_score":score})
        for (s,oid),response in sorted(player_responses.items()):
            if s!=slot:continue
            if oid not in opps:
                rejected.append({"population_slot_ref":slot,"social_opportunity_id":oid,"reason":"unknown_opportunity"});continue
            if response=="decline":
                declined.append({"population_slot_ref":slot,"social_opportunity_id":oid,"source":"explicit_player_decline"});continue
            if response!="accept":
                rejected.append({"population_slot_ref":slot,"social_opportunity_id":oid,"reason":"invalid_player_response"});continue
            ok,reason=feasible(slot,oid)
            if not ok:
                rejected.append({"population_slot_ref":slot,"social_opportunity_id":oid,"reason":reason});continue
            if len(rosters[oid])>=int(opps[oid]["capacity"]):
                rejected.append({"population_slot_ref":slot,"social_opportunity_id":oid,"reason":"capacity_full"});continue
            add_plan(slot,oid,"explicit_player_acceptance")

    # NPCs may plan one new social opportunity in this reference pass.
    candidates=[]
    for slot in sorted(slots):
        if by_slot[slot].get("is_player",False):continue
        for oid,score,tie in options_for(slot):candidates.append((-score,tie,slot,oid))
    planned_new=set()
    for _,__,slot,oid in sorted(candidates):
        if slot in planned_new:continue
        if len(rosters[oid])>=int(opps[oid]["capacity"]):continue
        add_plan(slot,oid,"npc_autonomous")
        planned_new.add(slot)

    clean_opps=copy.deepcopy(opps)
    for o in clean_opps.values():o.pop("_facility_valid",None)
    return {
      "rules_version":RULES_VERSION,
      "social_plans":sorted(plans,key=lambda x:(x["population_slot_ref"],x["social_opportunity_id"])),
      "rosters":{oid:sorted(rosters[oid]) for oid in sorted(rosters)},
      "player_options":sorted(player_options,key=lambda x:(x["population_slot_ref"],x["social_opportunity_id"])),
      "declined":sorted(declined,key=lambda x:(x["population_slot_ref"],x["social_opportunity_id"])),
      "rejected_or_unresolved":sorted(rejected,key=lambda x:(x["population_slot_ref"],x["social_opportunity_id"],str(x["reason"]))),
      "interaction_evidence_candidates":[],
      "relationship_mutations":[],
      "romantic_or_sexual_events":[],
      "social_truth_semantics":"plan_not_attendance_not_interaction_not_relationship",
      "future_step_state":{"romance_and_dating":[],"npc_to_npc_relationship_changes":[],"mentor_changes":[],"wellbeing_effects":[],"disciplinary_consequences":[],"campus_event_mutations":[],"offscreen_execution":[]}
    }

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(build_social_plans(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
