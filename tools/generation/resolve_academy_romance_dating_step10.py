#!/usr/bin/env python3
"""Reference resolver for Academy Life Step 10 player↔NPC romance/dating."""
from __future__ import annotations
import argparse, copy, heapq, json
from pathlib import Path
from typing import Any

RULES_VERSION="academy_romance_dating_v0.1"

def make_graph(request:dict[str,Any])->dict[str,list[tuple[str,int]]]:
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

def opposite_binary_sex(a,b):
    return {a,b}=={"male","female"}

def eligible_pair(a,b):
    if not a.get("adult_equivalent",False) or not b.get("adult_equivalent",False):return False,"adult_only"
    if a.get("sex_category") not in {"male","female"} or b.get("sex_category") not in {"male","female"}:return False,"sex_category_unresolved"
    if not opposite_binary_sex(a["sex_category"],b["sex_category"]):return False,"heterosexual_canon_ineligible"
    if a.get("hard_romantic_boundary",False) or b.get("hard_romantic_boundary",False):return False,"hard_boundary"
    return True,None

def window_for(slot,window_ref,windows):
    for w in windows:
        if w["population_slot_ref"]==slot and w["window_ref"]==window_ref:return w
    return None

def bilateral_date_feasible(player,npc,proposal,windows,venues,g):
    venue=venues.get(proposal["venue_ref"])
    if not venue or "date_venue" not in set(venue.get("capability_tags",[])):return False,"venue_unavailable"
    pw=window_for(player["population_slot_ref"],proposal["player_window_ref"],windows)
    nw=window_for(npc["population_slot_ref"],proposal["npc_window_ref"],windows)
    if not pw or not nw:return False,"missing_window"
    day=int(proposal["day_index"]);start=int(proposal["start_minute"]);end=int(proposal["end_minute"])
    if start>=end:return False,"invalid_interval"
    if int(pw["day_index"])!=day or int(nw["day_index"])!=day:return False,"window_day_mismatch"
    for w in (pw,nw):
        inbound=travel(g,w["start_location_ref"],proposal["venue_ref"])
        outbound=travel(g,proposal["venue_ref"],w["end_location_ref"])
        if inbound is None or outbound is None:return False,"travel_unavailable"
        if int(w["start_minute"])+inbound>start or end+outbound>int(w["end_minute"]):return False,"schedule_or_travel_conflict"
    return True,None

def resolve(request:dict[str,Any])->dict[str,Any]:
    chars=copy.deepcopy(request["characters"])
    by_slot={c["population_slot_ref"]:c for c in chars}
    if len(by_slot)!=len(chars):raise ValueError("duplicate population_slot_ref")
    players=[c for c in chars if c.get("is_player",False)]
    if len(players)!=1:raise ValueError("Step 10 requires exactly one player")
    player=players[0]
    g=make_graph(request)
    windows=copy.deepcopy(request.get("available_windows",[]))
    venues={v["location_ref"]:v for v in request.get("venues",[])}
    npc_interest=copy.deepcopy(request.get("npc_romantic_interest_edges",[]))
    interest_by_npc={x["observer_slot_ref"]:x for x in npc_interest if x.get("subject_slot_ref")==player["population_slot_ref"]}
    player_actions=copy.deepcopy(request.get("player_romantic_actions",[]))
    npc_initiations=copy.deepcopy(request.get("npc_initiation_requests",[]))
    existing=copy.deepcopy(request.get("existing_date_plans",[]))

    invitations=[];date_plans=[];rejected=[];declined=[];transition_candidates=[]
    occupied={slot:[] for slot in by_slot}

    for p in existing:
        a,b=p["participant_slot_refs"]
        if a not in by_slot or b not in by_slot:raise ValueError("existing date plan references unknown character")
        date_plans.append(copy.deepcopy(p))
        occupied[a].append((int(p["day_index"]),int(p["start_minute"]),int(p["end_minute"])))
        occupied[b].append((int(p["day_index"]),int(p["start_minute"]),int(p["end_minute"])))

    def overlap(slot,day,start,end):
        return any(d==day and s<end and start<e for d,s,e in occupied.get(slot,[]))

    def create_date(initiator,recipient,proposal,source):
        ok,reason=eligible_pair(initiator,recipient)
        if not ok:return None,reason
        npc=recipient if recipient["population_slot_ref"]!=player["population_slot_ref"] else initiator
        ok,reason=bilateral_date_feasible(player,npc,proposal,windows,venues,g)
        if not ok:return None,reason
        day,start,end=int(proposal["day_index"]),int(proposal["start_minute"]),int(proposal["end_minute"])
        for slot in (player["population_slot_ref"],npc["population_slot_ref"]):
            if overlap(slot,day,start,end):return None,"date_plan_conflict"
        inv_id=f'rominv:{initiator["population_slot_ref"]}:{recipient["population_slot_ref"]}:{proposal["proposal_id"]}'
        plan={
          "date_plan_id":f'date:{proposal["proposal_id"]}',
          "participant_slot_refs":sorted([initiator["population_slot_ref"],recipient["population_slot_ref"]]),
          "invitation_ref":inv_id,"day_index":day,"start_minute":start,"end_minute":end,
          "venue_ref":proposal["venue_ref"],"plan_state":"scheduled","attendance_state":"unresolved",
          "completion_state":"unresolved","source":source
        }
        occupied[player["population_slot_ref"]].append((day,start,end));occupied[npc["population_slot_ref"]].append((day,start,end))
        return (inv_id,plan),None

    proposals={p["proposal_id"]:p for p in request.get("date_proposals",[])}

    # NPC may initiate only from authoritative present/expressed interest with provenance.
    for init in npc_initiations:
        npc=by_slot.get(init["npc_slot_ref"]);pid=init["proposal_id"]
        if not npc or pid not in proposals:
            rejected.append({"source":"npc_initiation","npc_slot_ref":init.get("npc_slot_ref"),"proposal_id":pid,"reason":"unknown_reference"});continue
        ok,reason=eligible_pair(player,npc)
        if not ok:
            rejected.append({"source":"npc_initiation","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":reason});continue
        edge=interest_by_npc.get(npc["population_slot_ref"])
        if not edge or edge.get("romantic_interest_state") not in {"present","expressed"} or not edge.get("cause_event_refs"):
            rejected.append({"source":"npc_initiation","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"no_authoritative_npc_interest"});continue
        invitations.append({"romantic_invitation_id":f'rominv:{npc["population_slot_ref"]}:{player["population_slot_ref"]}:{pid}',"initiator_slot_ref":npc["population_slot_ref"],"recipient_slot_ref":player["population_slot_ref"],"proposal_id":pid,"state":"awaiting_player_response","source":"npc_authoritative_interest"})

    # Explicit player actions: invite, accept_npc_invitation, decline_npc_invitation, withdraw_acceptance.
    for action in player_actions:
        typ=action["action_type"];npc=by_slot.get(action["npc_slot_ref"]);pid=action.get("proposal_id")
        if not npc or npc.get("is_player",False):
            rejected.append({"source":"player_action","npc_slot_ref":action.get("npc_slot_ref"),"proposal_id":pid,"reason":"invalid_npc"});continue
        if typ=="invite":
            if pid not in proposals:
                rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"unknown_proposal"});continue
            ok,reason=eligible_pair(player,npc)
            if not ok:
                rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":reason});continue
            response=action.get("npc_response")
            inv={"romantic_invitation_id":f'rominv:{player["population_slot_ref"]}:{npc["population_slot_ref"]}:{pid}',"initiator_slot_ref":player["population_slot_ref"],"recipient_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"state":"proposed","source":"explicit_player_invitation"}
            if response=="decline":
                inv["state"]="declined";invitations.append(inv);declined.append({"invitation_ref":inv["romantic_invitation_id"],"automatic_hostility_effect":"none"});continue
            if response!="accept":
                invitations.append(inv);continue
            edge=interest_by_npc.get(npc["population_slot_ref"])
            if not edge or edge.get("romantic_interest_state") not in {"present","expressed"}:
                inv["state"]="declined";invitations.append(inv);declined.append({"invitation_ref":inv["romantic_invitation_id"],"automatic_hostility_effect":"none","reason":"npc_no_romantic_interest"});continue
            made,reason=create_date(player,npc,proposals[pid],"explicit_player_invitation")
            if not made:
                rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":reason});continue
            inv_id,plan=made;inv["state"]="accepted";inv["romantic_invitation_id"]=inv_id;invitations.append(inv);date_plans.append(plan)
        elif typ=="accept_npc_invitation":
            if pid not in proposals:
                rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"unknown_proposal"});continue
            pending=next((x for x in invitations if x["initiator_slot_ref"]==npc["population_slot_ref"] and x["proposal_id"]==pid and x["state"]=="awaiting_player_response"),None)
            if not pending:
                rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"no_pending_npc_invitation"});continue
            made,reason=create_date(npc,player,proposals[pid],"explicit_player_acceptance")
            if not made:
                rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":reason});continue
            pending["state"]="accepted";_,plan=made;date_plans.append(plan)
        elif typ=="decline_npc_invitation":
            pending=next((x for x in invitations if x["initiator_slot_ref"]==npc["population_slot_ref"] and x["proposal_id"]==pid and x["state"]=="awaiting_player_response"),None)
            if pending:
                pending["state"]="declined";declined.append({"invitation_ref":pending["romantic_invitation_id"],"automatic_hostility_effect":"none"})
            else:rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"no_pending_npc_invitation"})
        else:
            rejected.append({"source":"player_action","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"unsupported_action"})

    # Completed-date/commitment evidence can create transition candidates but not mutate relationship here.
    for ev in request.get("romantic_completion_evidence",[]):
        if ev.get("evidence_type")=="completed_date" and ev.get("bilateral_confirmed",False):
            transition_candidates.append({"participant_slot_refs":sorted(ev["participant_slot_refs"]),"candidate":"romantic_history_advance","cause_event_refs":[ev["event_ref"]],"automatic_commitment":False})
        elif ev.get("evidence_type")=="reciprocal_commitment" and ev.get("bilateral_confirmed",False):
            transition_candidates.append({"participant_slot_refs":sorted(ev["participant_slot_refs"]),"candidate":"relationship_state_dating_or_established","cause_event_refs":[ev["event_ref"]],"automatic_commitment":False})

    return {
      "rules_version":RULES_VERSION,
      "invitations":sorted(invitations,key=lambda x:x["romantic_invitation_id"]),
      "date_plans":sorted(date_plans,key=lambda x:x["date_plan_id"]),
      "declined":sorted(declined,key=lambda x:x["invitation_ref"]),
      "rejected_or_unresolved":sorted(rejected,key=lambda x:(str(x.get("npc_slot_ref")),str(x.get("proposal_id")),x["reason"])),
      "relationship_transition_candidates":transition_candidates,
      "player_romantic_interest_inferred":False,
      "automatic_hostility_from_rejection":"none",
      "dating_truth_semantics":"invitation_not_acceptance_not_attendance_not_completion_not_commitment",
      "canon":{"adult_only":True,"romantic_orientation_policy":"heterosexual_only","sexual_relationship_policy":"heterosexual_only"},
      "future_step_state":{"npc_to_npc_relationship_evolution":[],"mentor_changes":[],"wellbeing_effects":[],"disciplinary_consequences":[],"campus_event_mutations":[],"offscreen_execution":[]}
    }

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(resolve(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
