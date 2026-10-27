#!/usr/bin/env python3
"""Reference resolver for Academy Life Step 10 player↔NPC romance/dating."""
from __future__ import annotations
import argparse,copy,heapq,json
from pathlib import Path
from typing import Any
RULES_VERSION="academy_romance_dating_v0.2"
def make_graph(request:dict[str,Any])->dict[str,list[tuple[str,int]]]:
 g={}
 for e in request.get("travel_edges",[]):
  a,b,m=e["from"],e["to"],int(e["minutes"])
  if m<0:raise ValueError("negative travel time")
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
def eligible_pair(a,b):
 if not a.get("adult_equivalent",False) or not b.get("adult_equivalent",False):return False,"adult_only"
 sa,sb=a.get("sex_category"),b.get("sex_category")
 if sa not in {"male","female"} or sb not in {"male","female"}:return False,"sex_category_unresolved"
 if {sa,sb}!={"male","female"}:return False,"heterosexual_canon_ineligible"
 if a.get("hard_romantic_boundary",False) or b.get("hard_romantic_boundary",False):return False,"hard_boundary"
 return True,None
def window_for(slot,ref,windows):
 return next((w for w in windows if w["population_slot_ref"]==slot and w["window_ref"]==ref),None)
def bilateral_date_feasible(player,npc,p,windows,venues,g):
 venue=venues.get(p["venue_ref"])
 if not venue or "date_venue" not in set(venue.get("capability_tags",[])):return False,"venue_unavailable"
 pw=window_for(player["population_slot_ref"],p["player_window_ref"],windows);nw=window_for(npc["population_slot_ref"],p["npc_window_ref"],windows)
 if not pw or not nw:return False,"missing_window"
 day,start,end=int(p["day_index"]),int(p["start_minute"]),int(p["end_minute"])
 if start>=end:return False,"invalid_interval"
 if int(pw["day_index"])!=day or int(nw["day_index"])!=day:return False,"window_day_mismatch"
 for w in (pw,nw):
  tin=travel(g,w["start_location_ref"],p["venue_ref"]);tout=travel(g,p["venue_ref"],w["end_location_ref"])
  if tin is None or tout is None:return False,"travel_unavailable"
  if int(w["start_minute"])+tin>start or end+tout>int(w["end_minute"]):return False,"schedule_or_travel_conflict"
 return True,None
def resolve(request):
 chars=copy.deepcopy(request["characters"]);by_slot={c["population_slot_ref"]:c for c in chars}
 if len(by_slot)!=len(chars):raise ValueError("duplicate population_slot_ref")
 players=[c for c in chars if c.get("is_player",False)]
 if len(players)!=1:raise ValueError("Step 10 requires exactly one player")
 player=players[0];ps=player["population_slot_ref"];g=make_graph(request);windows=copy.deepcopy(request.get("available_windows",[]));venues={v["location_ref"]:v for v in request.get("venues",[])}
 interest_by_npc={x["observer_slot_ref"]:x for x in copy.deepcopy(request.get("npc_romantic_interest_edges",[])) if x.get("subject_slot_ref")==ps}
 proposals_list=copy.deepcopy(request.get("date_proposals",[]));pids=[p["proposal_id"] for p in proposals_list]
 if len(pids)!=len(set(pids)):raise ValueError("duplicate proposal_id")
 proposals={p["proposal_id"]:p for p in proposals_list}
 invitations=[];date_plans=[];rejected=[];declined=[];withdrawn=[];transition_candidates=[];occupied={s:[] for s in by_slot}
 def overlap(slot,day,start,end):
  return any(d==day and s<end and start<e for _,d,s,e in occupied.get(slot,[]))
 def reserve(plan):
  if plan.get("plan_state","scheduled")!="scheduled":return
  day,start,end=int(plan["day_index"]),int(plan["start_minute"]),int(plan["end_minute"])
  for slot in plan["participant_slot_refs"]:occupied[slot].append((plan["date_plan_id"],day,start,end))
 def release(plan):
  pid=plan["date_plan_id"]
  for slot in plan["participant_slot_refs"]:occupied[slot]=[x for x in occupied[slot] if x[0]!=pid]
 for p in copy.deepcopy(request.get("existing_date_plans",[])):
  refs=p.get("participant_slot_refs",[])
  if len(refs)!=2 or len(set(refs))!=2 or any(x not in by_slot for x in refs):raise ValueError("invalid existing date participants")
  if ps not in refs:raise ValueError("Step 10 existing date plan must include player")
  npc=by_slot[refs[0] if refs[1]==ps else refs[1]]
  ok,reason=eligible_pair(player,npc)
  if not ok:raise ValueError("existing date plan violates romantic canon: "+reason)
  start,end=int(p["start_minute"]),int(p["end_minute"])
  if start>=end:raise ValueError("invalid existing date interval")
  if p.get("plan_state","scheduled")=="scheduled":
   day=int(p["day_index"])
   if any(overlap(slot,day,start,end) for slot in refs):raise ValueError("existing date plans overlap")
  date_plans.append(p);reserve(p)
 def create_date(initiator,recipient,p,source):
  ok,reason=eligible_pair(initiator,recipient)
  if not ok:return None,reason
  npc=recipient if recipient["population_slot_ref"]!=ps else initiator
  ok,reason=bilateral_date_feasible(player,npc,p,windows,venues,g)
  if not ok:return None,reason
  day,start,end=int(p["day_index"]),int(p["start_minute"]),int(p["end_minute"])
  if any(overlap(slot,day,start,end) for slot in (ps,npc["population_slot_ref"])):return None,"date_plan_conflict"
  iid=f'rominv:{initiator["population_slot_ref"]}:{recipient["population_slot_ref"]}:{p["proposal_id"]}'
  plan={"date_plan_id":f'date:{p["proposal_id"]}',"participant_slot_refs":sorted([initiator["population_slot_ref"],recipient["population_slot_ref"]]),"invitation_ref":iid,"day_index":day,"start_minute":start,"end_minute":end,"venue_ref":p["venue_ref"],"plan_state":"scheduled","attendance_state":"unresolved","completion_state":"unresolved","source":source}
  reserve(plan);return (iid,plan),None
 for init in copy.deepcopy(request.get("npc_initiation_requests",[])):
  npc=by_slot.get(init["npc_slot_ref"]);pid=init["proposal_id"]
  if not npc or pid not in proposals:rejected.append({"source":"npc_initiation","npc_slot_ref":init.get("npc_slot_ref"),"proposal_id":pid,"reason":"unknown_reference"});continue
  ok,reason=eligible_pair(player,npc)
  if not ok:rejected.append({"source":"npc_initiation","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":reason});continue
  edge=interest_by_npc.get(npc["population_slot_ref"])
  if not edge or edge.get("romantic_interest_state") not in {"present","expressed"} or not edge.get("cause_event_refs"):
   rejected.append({"source":"npc_initiation","npc_slot_ref":npc["population_slot_ref"],"proposal_id":pid,"reason":"no_authoritative_npc_interest"});continue
  invitations.append({"romantic_invitation_id":f'rominv:{npc["population_slot_ref"]}:{ps}:{pid}',"initiator_slot_ref":npc["population_slot_ref"],"recipient_slot_ref":ps,"proposal_id":pid,"state":"awaiting_player_response","source":"npc_authoritative_interest"})
 for action in copy.deepcopy(request.get("player_romantic_actions",[])):
  typ=action["action_type"];npc=by_slot.get(action["npc_slot_ref"]);pid=action.get("proposal_id")
  if not npc or npc.get("is_player",False):rejected.append({"source":"player_action","npc_slot_ref":action.get("npc_slot_ref"),"proposal_id":pid,"reason":"invalid_npc"});continue
  ns=npc["population_slot_ref"]
  if typ=="invite":
   if pid not in proposals:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":"unknown_proposal"});continue
   ok,reason=eligible_pair(player,npc)
   if not ok:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":reason});continue
   response=action.get("npc_response");inv={"romantic_invitation_id":f'rominv:{ps}:{ns}:{pid}',"initiator_slot_ref":ps,"recipient_slot_ref":ns,"proposal_id":pid,"state":"proposed","source":"explicit_player_invitation"}
   if response=="decline":inv["state"]="declined";invitations.append(inv);declined.append({"invitation_ref":inv["romantic_invitation_id"],"automatic_hostility_effect":"none"});continue
   if response!="accept":invitations.append(inv);continue
   edge=interest_by_npc.get(ns)
   if not edge or edge.get("romantic_interest_state") not in {"present","expressed"}:
    inv["state"]="declined";invitations.append(inv);declined.append({"invitation_ref":inv["romantic_invitation_id"],"automatic_hostility_effect":"none","reason":"npc_no_romantic_interest"});continue
   made,reason=create_date(player,npc,proposals[pid],"explicit_player_invitation")
   if not made:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":reason});continue
   iid,plan=made;inv["state"]="accepted";inv["romantic_invitation_id"]=iid;invitations.append(inv);date_plans.append(plan)
  elif typ=="accept_npc_invitation":
   if pid not in proposals:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":"unknown_proposal"});continue
   pending=next((x for x in invitations if x["initiator_slot_ref"]==ns and x["proposal_id"]==pid and x["state"]=="awaiting_player_response"),None)
   if not pending:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":"no_pending_npc_invitation"});continue
   made,reason=create_date(npc,player,proposals[pid],"explicit_player_acceptance")
   if not made:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":reason});continue
   pending["state"]="accepted";_,plan=made;date_plans.append(plan)
  elif typ=="decline_npc_invitation":
   pending=next((x for x in invitations if x["initiator_slot_ref"]==ns and x["proposal_id"]==pid and x["state"]=="awaiting_player_response"),None)
   if pending:pending["state"]="declined";declined.append({"invitation_ref":pending["romantic_invitation_id"],"automatic_hostility_effect":"none"})
   else:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":"no_pending_npc_invitation"})
  elif typ=="withdraw_acceptance":
   wanted=action.get("date_plan_id")
   plan=next((x for x in date_plans if x.get("plan_state","scheduled")=="scheduled" and ps in x["participant_slot_refs"] and ns in x["participant_slot_refs"] and ((wanted and x["date_plan_id"]==wanted) or (not wanted and pid and (x["date_plan_id"]==f"date:{pid}" or x.get("invitation_ref","").endswith(":"+pid))))),None)
   if not plan:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":"no_scheduled_date_to_withdraw"});continue
   plan["plan_state"]="cancelled_by_player";plan["cancellation_source"]="explicit_player_withdrawal";release(plan)
   inv=next((x for x in invitations if x["romantic_invitation_id"]==plan.get("invitation_ref")),None)
   if inv and inv.get("state")=="accepted":inv["state"]="withdrawn"
   withdrawn.append({"date_plan_ref":plan["date_plan_id"],"automatic_hostility_effect":"none"})
  else:rejected.append({"source":"player_action","npc_slot_ref":ns,"proposal_id":pid,"reason":"unsupported_action"})
 for ev in request.get("romantic_completion_evidence",[]):
  if ev.get("evidence_type")=="completed_date" and ev.get("bilateral_confirmed",False):transition_candidates.append({"participant_slot_refs":sorted(ev["participant_slot_refs"]),"candidate":"romantic_history_advance","cause_event_refs":[ev["event_ref"]],"automatic_commitment":False})
  elif ev.get("evidence_type")=="reciprocal_commitment" and ev.get("bilateral_confirmed",False):transition_candidates.append({"participant_slot_refs":sorted(ev["participant_slot_refs"]),"candidate":"relationship_state_dating_or_established","cause_event_refs":[ev["event_ref"]],"automatic_commitment":False})
 return {"rules_version":RULES_VERSION,"invitations":sorted(invitations,key=lambda x:x["romantic_invitation_id"]),"date_plans":sorted(date_plans,key=lambda x:x["date_plan_id"]),"declined":sorted(declined,key=lambda x:x["invitation_ref"]),"withdrawn":sorted(withdrawn,key=lambda x:x["date_plan_ref"]),"rejected_or_unresolved":sorted(rejected,key=lambda x:(str(x.get("npc_slot_ref")),str(x.get("proposal_id")),x["reason"])),"relationship_transition_candidates":transition_candidates,"player_romantic_interest_inferred":False,"automatic_hostility_from_rejection":"none","dating_truth_semantics":"invitation_not_acceptance_not_attendance_not_completion_not_commitment","canon":{"adult_only":True,"romantic_orientation_policy":"heterosexual_only","sexual_relationship_policy":"heterosexual_only"},"future_step_state":{"npc_to_npc_relationship_evolution":[],"mentor_changes":[],"wellbeing_effects":[],"disciplinary_consequences":[],"campus_event_mutations":[],"offscreen_execution":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
