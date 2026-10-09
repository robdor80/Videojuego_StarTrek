#!/usr/bin/env python3
"""Deterministic reference resolver for Academy Life Step 11 NPC-to-NPC relationships."""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path
from typing import Any

RULES_VERSION="academy_npc_relationships_v0.1"
SCALE=["strong_negative","negative","neutral","positive","strong_positive"]
FAMILIARITY=["unknown","recognized","acquainted","familiar","close"]

def bump(value:str, ordered:list[str], delta:int)->str:
    if value not in ordered:value=ordered[0]
    i=max(0,min(len(ordered)-1,ordered.index(value)+delta))
    return ordered[i]

def pair_key(a:str,b:str)->str:
    return f"{a}->{b}"

def default_edge(a:str,b:str)->dict[str,Any]:
    return {
      "edge_id":f"rel:{a}:{b}","observer_population_slot_ref":a,"subject_population_slot_ref":b,
      "familiarity":"unknown","personal_affinity":"neutral","personal_trust":"neutral",
      "professional_respect":"neutral","friendship_state":"none","conflict_state":"none",
      "emotional_intimacy":"neutral","romantic_interest":"none","relationship_state":"none",
      "shared_history_refs":[],"last_updated_event_ref":None
    }

def romantic_eligible(a:dict[str,Any],b:dict[str,Any])->tuple[bool,str|None]:
    if not a.get("adult_equivalent",False) or not b.get("adult_equivalent",False):return False,"adult_only"
    sa,sb=a.get("sex_category"),b.get("sex_category")
    if sa not in {"male","female"} or sb not in {"male","female"}:return False,"sex_category_unresolved"
    if {sa,sb}!={"male","female"}:return False,"heterosexual_canon_ineligible"
    if a.get("hard_romantic_boundary",False) or b.get("hard_romantic_boundary",False):return False,"hard_boundary"
    return True,None

def resolve(request:dict[str,Any])->dict[str,Any]:
    chars=copy.deepcopy(request["characters"])
    slots=[c["population_slot_ref"] for c in chars]
    if len(slots)!=len(set(slots)):raise ValueError("duplicate population_slot_ref")
    by_slot={c["population_slot_ref"]:c for c in chars}
    player_slots={c["population_slot_ref"] for c in chars if c.get("is_player",False)}
    edges={}
    for e in request.get("existing_edges",[]):
        a,b=e["observer_population_slot_ref"],e["subject_population_slot_ref"]
        if a not in by_slot or b not in by_slot or a==b:raise ValueError("invalid existing relationship edge")
        if a in player_slots or b in player_slots:raise ValueError("Step 11 existing edge cannot include player")
        edges[pair_key(a,b)]=copy.deepcopy(e)

    events=sorted(copy.deepcopy(request.get("confirmed_events",[])),key=lambda x:(str(x.get("occurred_at","")),x["event_id"]))
    rejected=[];changes=[]

    def edge(a,b):
        k=pair_key(a,b)
        if k not in edges:edges[k]=default_edge(a,b)
        return edges[k]

    def history(e,event_id):
        if event_id not in e["shared_history_refs"]:e["shared_history_refs"].append(event_id)
        e["last_updated_event_ref"]=event_id

    for ev in events:
        a,b=ev["actor_slot_ref"],ev["target_slot_ref"]
        if a not in by_slot or b not in by_slot or a==b:
            rejected.append({"event_id":ev["event_id"],"reason":"invalid_participant"});continue
        if a in player_slots or b in player_slots:
            rejected.append({"event_id":ev["event_id"],"reason":"player_excluded_step_11"});continue
        if not ev.get("confirmed",False) or not ev.get("cause_event_refs"):
            rejected.append({"event_id":ev["event_id"],"reason":"missing_confirmed_provenance"});continue
        typ=ev["event_type"];e=edge(a,b);before=copy.deepcopy(e);applied=True

        if typ=="first_meeting":
            e["familiarity"]=bump(e["familiarity"],FAMILIARITY,1)
        elif typ=="repeated_encounter":
            e["familiarity"]=bump(e["familiarity"],FAMILIARITY,1)
        elif typ=="successful_collaboration":
            e["professional_respect"]=bump(e["professional_respect"],SCALE,1)
            e["familiarity"]=bump(e["familiarity"],FAMILIARITY,1)
        elif typ=="professional_failure":
            e["professional_respect"]=bump(e["professional_respect"],SCALE,-1)
        elif typ=="support_given":
            e["personal_trust"]=bump(e["personal_trust"],SCALE,1)
            e["personal_affinity"]=bump(e["personal_affinity"],SCALE,1)
        elif typ=="confidences_shared":
            e["personal_trust"]=bump(e["personal_trust"],SCALE,1)
            e["emotional_intimacy"]=bump(e["emotional_intimacy"],SCALE,1)
            e["familiarity"]=bump(e["familiarity"],FAMILIARITY,1)
        elif typ=="conflict":
            e["conflict_state"]="active_conflict" if ev.get("severity")=="major" else "tension"
            e["personal_trust"]=bump(e["personal_trust"],SCALE,-1)
            e["personal_affinity"]=bump(e["personal_affinity"],SCALE,-1)
        elif typ=="apology":
            if e["conflict_state"] in {"tension","active_conflict"}:
                e["conflict_state"]="repairing"
                if ev.get("accepted",False):e["personal_trust"]=bump(e["personal_trust"],SCALE,1)
        elif typ=="reconciliation_attempt":
            if ev.get("accepted",False):
                e["conflict_state"]="reconciled_unresolved_history"
                e["personal_trust"]=bump(e["personal_trust"],SCALE,1)
        elif typ=="friendship_develops":
            positive_refs=ev.get("positive_shared_history_refs",[])
            if FAMILIARITY.index(e["familiarity"])<FAMILIARITY.index("acquainted") or len(set(positive_refs))<2:
                applied=False;rejected.append({"event_id":ev["event_id"],"reason":"insufficient_friendship_history"})
            else:e["friendship_state"]="friend"
        elif typ=="close_friendship_develops":
            if e["friendship_state"]!="friend" or len(set(ev.get("positive_shared_history_refs",[])))<2:
                applied=False;rejected.append({"event_id":ev["event_id"],"reason":"insufficient_close_friendship_history"})
            else:e["friendship_state"]="close_friend"
        elif typ=="romantic_interest_emergence":
            ok,reason=romantic_eligible(by_slot[a],by_slot[b])
            if not ok:
                applied=False;rejected.append({"event_id":ev["event_id"],"reason":reason})
            else:e["romantic_interest"]="present"
        elif typ=="romantic_expression":
            ok,reason=romantic_eligible(by_slot[a],by_slot[b])
            if not ok or e["romantic_interest"] not in {"present","expressed"}:
                applied=False;rejected.append({"event_id":ev["event_id"],"reason":reason or "no_directional_interest"})
            else:e["romantic_interest"]="expressed"
        elif typ=="romantic_rejection":
            if e["romantic_interest"]=="expressed":e["romantic_interest"]=ev.get("interest_after_rejection","present")
        elif typ=="completed_date":
            ok,reason=romantic_eligible(by_slot[a],by_slot[b])
            if not ok or not ev.get("bilateral_confirmed",False):
                applied=False;rejected.append({"event_id":ev["event_id"],"reason":reason or "date_not_bilateral"})
            else:
                e["personal_affinity"]=bump(e["personal_affinity"],SCALE,1)
                e["familiarity"]=bump(e["familiarity"],FAMILIARITY,1)
        elif typ=="reciprocal_commitment":
            ok,reason=romantic_eligible(by_slot[a],by_slot[b])
            rev=edge(b,a)
            if not ok or not ev.get("bilateral_confirmed",False) or e["romantic_interest"] not in {"present","expressed"} or rev["romantic_interest"] not in {"present","expressed"}:
                applied=False;rejected.append({"event_id":ev["event_id"],"reason":reason or "commitment_not_reciprocal"})
            else:
                state=ev.get("relationship_state","dating")
                if state not in {"dating","established"}:raise ValueError("invalid commitment relationship state")
                e["relationship_state"]=state;rev["relationship_state"]=state
                history(rev,ev["event_id"])
        elif typ=="relationship_strain":
            if e["relationship_state"] in {"dating","established"}:e["relationship_state"]="strained"
            else:e["conflict_state"]="tension"
        elif typ=="separation":
            if e["relationship_state"] in {"dating","established","strained"}:e["relationship_state"]="separated"
            else:e["relationship_state"]="former_partner"
        else:
            applied=False;rejected.append({"event_id":ev["event_id"],"reason":"unsupported_event_type"})

        if applied:
            history(e,ev["event_id"])
            changes.append({
              "relationship_event_id":ev["event_id"],"observer_population_slot_ref":a,
              "subject_population_slot_ref":b,"event_type":typ,
              "changed":before!=e,"cause_event_refs":copy.deepcopy(ev["cause_event_refs"])
            })

    return {
      "rules_version":RULES_VERSION,
      "directional_edges":sorted(edges.values(),key=lambda x:(x["observer_population_slot_ref"],x["subject_population_slot_ref"])),
      "applied_changes":changes,
      "rejected_or_unresolved":sorted(rejected,key=lambda x:(x["event_id"],x["reason"])),
      "player_edges_mutated":False,
      "relationship_truth_semantics":"confirmed_events_mutate_directional_persistent_edges",
      "canon":{"adult_only":True,"romantic_orientation_policy":"heterosexual_only","sexual_relationship_policy":"heterosexual_only"},
      "future_step_state":{"mentor_changes":[],"wellbeing_effects":[],"disciplinary_consequences":[],"campus_event_mutations":[],"offscreen_catchup":[],"social_lod":[]}
    }

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(resolve(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
