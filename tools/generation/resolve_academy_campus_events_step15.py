#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, heapq, json
from pathlib import Path
from typing import Any
RULES_VERSION="academy_campus_events_v0.1"
VALID_TYPES={"scheduled_institutional","emergent_incident","crisis_alert"}
VALID_ACCESS={"mandatory_scope","optional_open","invitation_only","role_assignment"}
PRIORITY={"low":0,"normal":1,"high":2,"emergency":3}
def stable_hex(*parts:Any,size:int=16)->str:return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]
def make_graph(request):
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
def fits(slot,event,windows,g):
 for w in windows:
  if w["population_slot_ref"]!=slot or int(w["day_index"])!=int(event["day_index"]):continue
  tin=travel(g,w["start_location_ref"],event["location_ref"]);tout=travel(g,event["location_ref"],w["end_location_ref"])
  if tin is None or tout is None:continue
  if int(w["start_minute"])+tin<=int(event["start_minute"]) and int(event["end_minute"])+tout<=int(w["end_minute"]):return True
 return False
def resolve(request):
 seed=request["campaign_seed"];cadets=copy.deepcopy(request["cadets"]);slots=[c["population_slot_ref"] for c in cadets]
 if len(slots)!=len(set(slots)):raise ValueError("duplicate cadet population_slot_ref")
 by_slot={c["population_slot_ref"]:c for c in cadets};authorities={a["authority_id"]:a for a in request.get("authorities",[])};known_external=set(request.get("known_external_entity_refs",[]));locations={x["location_ref"]:set(x.get("capability_tags",[])) for x in request.get("locations",[])};windows=copy.deepcopy(request.get("availability_windows",[]));graph=make_graph(request)
 event_records=[];rejected=[];obligations=[];player_options=[];npc_plans=[];schedule_revisions=[];schedule_conflicts=[];institutional_exception_candidates=[];rosters={}
 events=copy.deepcopy(request.get("campus_events",[]));ids=[e["campus_event_id"] for e in events]
 if len(ids)!=len(set(ids)):raise ValueError("duplicate campus_event_id")
 def validate_event(e):
  et=e.get("event_type");access=e.get("access_mode");auth=authorities.get(e.get("authority_id"))
  if et not in VALID_TYPES:return False,"invalid_event_type"
  if access not in VALID_ACCESS:return False,"invalid_access_mode"
  if int(e["start_minute"])>=int(e["end_minute"]):return False,"invalid_event_interval"
  if int(e.get("capacity",0))<0:return False,"negative_capacity"
  if e.get("priority","normal") not in PRIORITY:return False,"invalid_priority"
  if not set(e.get("required_location_capabilities",[])).issubset(locations.get(e["location_ref"],set())):return False,"location_capability_missing"
  if any(x not in known_external for x in e.get("external_participant_refs",[])):return False,"unknown_external_participant"
  if et=="scheduled_institutional":
   if not auth or "schedule_campus_event" not in set(auth.get("scopes",[])):return False,"invalid_scheduling_authority"
   if not e.get("source_ref"):return False,"missing_scheduled_source"
  elif et=="emergent_incident":
   if not e.get("cause_event_refs"):return False,"missing_emergent_cause"
   if not auth or "register_campus_incident" not in set(auth.get("scopes",[])):return False,"invalid_incident_authority"
  else:
   if not e.get("cause_event_refs"):return False,"missing_crisis_cause"
   if not auth or "activate_campus_alert" not in set(auth.get("scopes",[])):return False,"invalid_alert_authority"
  if e.get("status")=="cancelled":
   if not e.get("cancellation_event_ref"):return False,"missing_cancellation_provenance"
   if not auth or "cancel_campus_event" not in set(auth.get("scopes",[])):return False,"invalid_cancellation_authority"
  targets=set(e.get("target_slot_refs",[]))|set(e.get("invited_slot_refs",[]))|set(e.get("assigned_slot_refs",[]))
  if any(s not in by_slot for s in targets):return False,"unknown_cadet_target"
  if access in {"mandatory_scope","role_assignment"}:
   required=e.get("target_slot_refs",[]) if access=="mandatory_scope" else e.get("assigned_slot_refs",[])
   if int(e.get("capacity",0))<len(set(required)):return False,"mandatory_capacity_insufficient"
  return True,None
 valid={}
 for e in sorted(events,key=lambda x:(int(x["day_index"]),int(x["start_minute"]),x["campus_event_id"])):
  ok,reason=validate_event(e)
  if not ok:rejected.append({"ref":e["campus_event_id"],"reason":reason});continue
  valid[e["campus_event_id"]]=e;rosters[e["campus_event_id"]]=[]
  event_records.append({"campus_event_id":e["campus_event_id"],"event_type":e["event_type"],"event_family":e["event_family"],"status":e.get("status","scheduled"),"day_index":int(e["day_index"]),"start_minute":int(e["start_minute"]),"end_minute":int(e["end_minute"]),"location_ref":e["location_ref"],"priority":e.get("priority","normal"),"source_ref":e.get("source_ref"),"cause_event_refs":copy.deepcopy(e.get("cause_event_refs",[])),"cancellation_event_ref":e.get("cancellation_event_ref")})
 def eligible(slot,e):
  if e["access_mode"]=="mandatory_scope":return slot in set(e.get("target_slot_refs",[]))
  if e["access_mode"]=="role_assignment":return slot in set(e.get("assigned_slot_refs",[]))
  if e["access_mode"]=="invitation_only":return slot in set(e.get("invited_slot_refs",[]))
  target=e.get("target_slot_refs",[]);return not target or slot in set(target)
 for p in sorted(copy.deepcopy(request.get("existing_participation_plans",[])),key=lambda x:(x["campus_event_id"],x["population_slot_ref"])):
  eid,slot=p["campus_event_id"],p["population_slot_ref"]
  if eid not in valid or slot not in by_slot:raise ValueError("existing participation references unknown entity")
  e=valid[eid]
  if e.get("status")=="cancelled":continue
  if e["access_mode"] in {"mandatory_scope","role_assignment"}:raise ValueError("existing optional plan attached to mandatory event")
  if not eligible(slot,e):raise ValueError("existing participation no longer eligible")
  if not fits(slot,e,windows,graph):raise ValueError("existing participation no longer feasible")
  if len(rosters[eid])>=int(e["capacity"]):raise ValueError("existing participation exceeds capacity")
  rosters[eid].append(slot);npc_plans.append({"participation_plan_id":p.get("participation_plan_id",f"campus:{eid}:{slot}"),"campus_event_id":eid,"population_slot_ref":slot,"source":"existing_preserved","attendance_state":"unresolved","interaction_state":"unresolved"})
 for eid,e in sorted(valid.items()):
  if e.get("status")=="cancelled" or e["access_mode"] not in {"mandatory_scope","role_assignment"}:continue
  required=e.get("target_slot_refs",[]) if e["access_mode"]=="mandatory_scope" else e.get("assigned_slot_refs",[])
  for slot in sorted(set(required)):
   if fits(slot,e,windows,graph):
    obligations.append({"obligation_id":f"campus-obligation:{eid}:{slot}","campus_event_id":eid,"population_slot_ref":slot,"obligation_type":"campus_event","mandatory":True,"attendance_state":"unresolved","source_ref":eid})
   elif e["event_type"]=="crisis_alert" and e.get("preemption_policy")=="preempt_lower_priority":
    auth=authorities[e["authority_id"]]
    if "preempt_schedule" in set(auth.get("scopes",[])):
     schedule_revisions.append({"revision_candidate_id":f"campus-preempt:{eid}:{slot}","campus_event_id":eid,"population_slot_ref":slot,"reason":"authorized_crisis_preemption","apply_state":"candidate_only"})
     obligations.append({"obligation_id":f"campus-obligation:{eid}:{slot}","campus_event_id":eid,"population_slot_ref":slot,"obligation_type":"campus_event","mandatory":True,"attendance_state":"unresolved","source_ref":eid,"schedule_state":"pending_authorized_preemption"})
     institutional_exception_candidates.append({"population_slot_ref":slot,"campus_event_id":eid,"reason_code":"institutional_schedule_conflict","effect":"candidate_for_step14_justification"})
    else:schedule_conflicts.append({"conflict_id":f"campus-conflict:{eid}:{slot}","campus_event_id":eid,"population_slot_ref":slot,"reason":"preemption_not_authorized"})
   else:schedule_conflicts.append({"conflict_id":f"campus-conflict:{eid}:{slot}","campus_event_id":eid,"population_slot_ref":slot,"reason":"mandatory_event_schedule_or_travel_conflict"})
 max_optional=int(request.get("max_new_optional_campus_plans_per_npc",1));npc_new_count={s:0 for s in slots};candidates=[]
 for eid,e in sorted(valid.items()):
  if e.get("status")=="cancelled" or e["access_mode"] in {"mandatory_scope","role_assignment"}:continue
  for slot in sorted(slots):
   if not eligible(slot,e) or slot in rosters[eid] or not fits(slot,e,windows,graph):continue
   if by_slot[slot].get("is_player",False):
    state="available" if len(rosters[eid])<int(e["capacity"]) else "full";player_options.append({"population_slot_ref":slot,"campus_event_id":eid,"state":state})
   else:
    prefs=set(by_slot[slot].get("campus_event_preference_tags",[]))|set(by_slot[slot].get("interest_refs",[]));score=len(prefs&set(e.get("preference_tags",[])));candidates.append((-score,stable_hex(seed,"campus",slot,eid,RULES_VERSION),slot,eid))
 for _,__,slot,eid in sorted(candidates):
  if npc_new_count[slot]>=max_optional:continue
  e=valid[eid]
  if len(rosters[eid])>=int(e["capacity"]):continue
  rosters[eid].append(slot);npc_new_count[slot]+=1;npc_plans.append({"participation_plan_id":f"campus:{eid}:{slot}","campus_event_id":eid,"population_slot_ref":slot,"source":"npc_autonomous_optional_plan","attendance_state":"unresolved","interaction_state":"unresolved"})
 return {"rules_version":RULES_VERSION,"event_records":event_records,"mandatory_obligation_candidates":sorted(obligations,key=lambda x:(x["population_slot_ref"],x["campus_event_id"])),"player_optional_event_options":sorted(player_options,key=lambda x:(x["population_slot_ref"],x["campus_event_id"])),"npc_optional_participation_plans":sorted(npc_plans,key=lambda x:(x["population_slot_ref"],x["campus_event_id"])),"schedule_revision_candidates":sorted(schedule_revisions,key=lambda x:(x["population_slot_ref"],x["campus_event_id"])),"schedule_conflict_candidates":sorted(schedule_conflicts,key=lambda x:(x["population_slot_ref"],x["campus_event_id"])),"institutional_exception_candidates":sorted(institutional_exception_candidates,key=lambda x:(x["population_slot_ref"],x["campus_event_id"])),"rejected_or_unresolved":sorted(rejected,key=lambda x:(x["ref"],x["reason"])),"attendance_events":[],"relationship_mutations":[],"wellbeing_mutations":[],"academic_record_writes":[],"generated_events_not_in_input":[],"truth_semantics":"event_exists_before_participation_and_participation_plan_is_not_attendance","future_step_state":{"offscreen_execution":[],"social_lod":[],"year_progression":[],"academy_record_integration":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(resolve(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
