#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,heapq,json
from pathlib import Path
RULES_VERSION="academy_mentors_instructors_v0.2"
def make_graph(r):
 g={}
 for e in r.get("travel_edges",[]):
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
def find_window(ws,p,ref):return next((w for w in ws if w["participant_ref"]==p and w["window_ref"]==ref),None)
def session_feasible(r,mentor,cadet,q,g):
 caps={x["location_ref"]:set(x.get("capability_tags",[])) for x in r.get("locations",[])};loc=q["location_ref"]
 if "tutoring_or_mentoring_space" not in caps.get(loc,set()):return False,"location_capability_missing"
 mw=find_window(r.get("available_windows",[]),mentor,q["mentor_window_ref"]);cw=find_window(r.get("available_windows",[]),cadet,q["cadet_window_ref"])
 if not mw or not cw:return False,"missing_window"
 day,start,end=int(q["day_index"]),int(q["start_minute"]),int(q["end_minute"])
 if start>=end:return False,"invalid_interval"
 if int(mw["day_index"])!=day or int(cw["day_index"])!=day:return False,"window_day_mismatch"
 for w in (mw,cw):
  tin=travel(g,w["start_location_ref"],loc);tout=travel(g,loc,w["end_location_ref"])
  if tin is None or tout is None:return False,"travel_unavailable"
  if int(w["start_minute"])+tin>start or end+tout>int(w["end_minute"]):return False,"schedule_or_travel_conflict"
 return True,None
def resolve(r):
 instructors=copy.deepcopy(r["instructors"]);cadets=copy.deepcopy(r["cadets"]);iids=[x["instructor_id"] for x in instructors];slots=[x["population_slot_ref"] for x in cadets]
 if len(iids)!=len(set(iids)):raise ValueError("duplicate instructor_id")
 if len(slots)!=len(set(slots)):raise ValueError("duplicate cadet population_slot_ref")
 by_inst={x["instructor_id"]:x for x in instructors};by_cadet={x["population_slot_ref"]:x for x in cadets};players={x["population_slot_ref"] for x in cadets if x.get("is_player",False)}
 if len(players)>1:raise ValueError("multiple player cadets")
 max_per_cadet=int(r.get("max_active_mentors_per_cadet",1));g=make_graph(r);teaching=[]
 for a in copy.deepcopy(r.get("teaching_assignments",[])):
  iid=a["instructor_id"]
  if iid not in by_inst:raise ValueError("teaching assignment references unknown instructor")
  inst=by_inst[iid];state="active" if inst.get("active",True) and a["subject_id"] in set(inst.get("subject_ids",[])) else ("invalid_instructor_inactive" if not inst.get("active",True) else "invalid_subject_authority");teaching.append(dict(a,assignment_state=state))
 mentorships=[];rejected=[];declined=[];tutoring=[];mentoring=[];recs=[];active_by_mentor={i:0 for i in by_inst};active_by_cadet={s:0 for s in by_cadet};pairs=set()
 def add(iid,slot,scope,source,mid=None):
  k=(iid,slot)
  if k in pairs:raise ValueError("duplicate active mentorship pair")
  pairs.add(k);m={"mentorship_id":mid or f"mentor:{iid}:{slot}","mentor_instructor_id":iid,"mentee_population_slot_ref":slot,"professional_scope":scope,"state":"active","source":source,"friendship_effect":"none","grade_effect":"none","qualification_effect":"none","discipline_effect":"none","career_guarantee":"none"};mentorships.append(m);active_by_mentor[iid]+=1;active_by_cadet[slot]+=1
 for m in sorted(copy.deepcopy(r.get("existing_mentorships",[])),key=lambda x:(x["mentor_instructor_id"],x["mentee_population_slot_ref"])):
  iid,slot=m["mentor_instructor_id"],m["mentee_population_slot_ref"]
  if iid not in by_inst or slot not in by_cadet:raise ValueError("existing mentorship references unknown entity")
  if m.get("state","active")!="active":continue
  inst=by_inst[iid]
  if not inst.get("active",True):rejected.append({"kind":"existing_mentorship","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"mentor_inactive"});continue
  if m["professional_scope"] not in set(inst.get("mentor_scopes",[])):rejected.append({"kind":"existing_mentorship","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"mentor_scope_invalid"});continue
  if active_by_mentor[iid]>=int(inst.get("mentee_capacity",0)):raise ValueError("existing mentorships exceed mentor capacity")
  if active_by_cadet[slot]>=max_per_cadet:raise ValueError("existing mentorships exceed cadet mentor limit")
  add(iid,slot,m["professional_scope"],"existing_preserved",m.get("mentorship_id"))
 responses={(x["mentor_instructor_id"],x["cadet_slot_ref"]):x["response"] for x in r.get("player_mentorship_responses",[])}
 for p in sorted(copy.deepcopy(r.get("mentorship_proposals",[])),key=lambda x:(x["mentor_instructor_id"],x["cadet_slot_ref"])):
  iid,slot=p["mentor_instructor_id"],p["cadet_slot_ref"]
  if iid not in by_inst or slot not in by_cadet:rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"unknown_entity"});continue
  inst=by_inst[iid];scope=p["professional_scope"]
  if (iid,slot) in pairs:continue
  if not inst.get("active",True):rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"mentor_inactive"});continue
  if scope not in set(inst.get("mentor_scopes",[])):rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"mentor_scope_invalid"});continue
  if not p.get("cause_event_refs"):rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"missing_provenance"});continue
  if active_by_mentor[iid]>=int(inst.get("mentee_capacity",0)):rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"mentor_capacity_full"});continue
  if active_by_cadet[slot]>=max_per_cadet:rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"cadet_mentor_limit"});continue
  response=responses.get((iid,slot)) if slot in players else p.get("npc_response")
  if response=="decline":declined.append({"mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"explicit_player_decline" if slot in players else "represented_npc_decline"});continue
  if response!="accept":rejected.append({"kind":"mentorship_proposal","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"awaiting_explicit_player_response" if slot in players else "missing_npc_acceptance"});continue
  add(iid,slot,scope,"accepted_proposal")
 busy={};session_ids=set()
 def reserve_session(iid,slot,q):
  sid=q["session_id"]
  if sid in session_ids:raise ValueError("duplicate tutoring/mentoring session_id")
  day,start,end=int(q["day_index"]),int(q["start_minute"]),int(q["end_minute"])
  for who in (iid,slot):
   if any(d==day and s<end and start<e for d,s,e,_ in busy.get(who,[])):return False
  for who in (iid,slot):busy.setdefault(who,[]).append((day,start,end,sid))
  session_ids.add(sid);return True
 for q in copy.deepcopy(r.get("tutoring_requests",[])):
  iid,slot=q["instructor_id"],q["cadet_slot_ref"]
  if iid not in by_inst or slot not in by_cadet:rejected.append({"kind":"tutoring","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"unknown_entity"});continue
  inst=by_inst[iid]
  if not inst.get("active",True) or q["subject_id"] not in set(inst.get("subject_ids",[])):rejected.append({"kind":"tutoring","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"subject_or_instructor_invalid"});continue
  ok,reason=session_feasible(r,iid,slot,q,g)
  if not ok:rejected.append({"kind":"tutoring","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":reason});continue
  if not reserve_session(iid,slot,q):rejected.append({"kind":"tutoring","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"session_plan_conflict"});continue
  tutoring.append({"session_id":q["session_id"],"instructor_id":iid,"cadet_slot_ref":slot,"subject_id":q["subject_id"],"session_state":"planned","creates_mentorship":False,"attendance_state":"unresolved","academic_result_effect":"none_until_rule_result"})
 active_pairs=set(pairs)
 for q in copy.deepcopy(r.get("mentoring_session_requests",[])):
  iid,slot=q["mentor_instructor_id"],q["cadet_slot_ref"]
  if (iid,slot) not in active_pairs:rejected.append({"kind":"mentoring_session","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"no_active_mentorship"});continue
  ok,reason=session_feasible(r,iid,slot,q,g)
  if not ok:rejected.append({"kind":"mentoring_session","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":reason});continue
  if not reserve_session(iid,slot,q):rejected.append({"kind":"mentoring_session","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"session_plan_conflict"});continue
  mentoring.append({"session_id":q["session_id"],"mentor_instructor_id":iid,"cadet_slot_ref":slot,"session_state":"planned","attendance_state":"unresolved","automatic_friendship_effect":"none","automatic_grade_effect":"none","automatic_wellbeing_effect":"none"})
 for rr in copy.deepcopy(r.get("recommendation_requests",[])):
  iid,slot=rr["mentor_instructor_id"],rr["cadet_slot_ref"]
  if (iid,slot) not in active_pairs:rejected.append({"kind":"recommendation","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"no_active_mentorship"});continue
  if "recommendation" not in set(by_inst[iid].get("authority_scope",[])):rejected.append({"kind":"recommendation","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"no_recommendation_authority"});continue
  if not rr.get("basis_event_refs"):rejected.append({"kind":"recommendation","mentor_instructor_id":iid,"cadet_slot_ref":slot,"reason":"missing_recommendation_basis"});continue
  recs.append({"recommendation_candidate_id":rr["recommendation_candidate_id"],"mentor_instructor_id":iid,"cadet_slot_ref":slot,"professional_scope":rr["professional_scope"],"basis_event_refs":copy.deepcopy(rr["basis_event_refs"]),"effect":"evidence_candidate_only","guarantees_assignment":False,"guarantees_grade":False,"guarantees_qualification":False})
 return {"rules_version":RULES_VERSION,"teaching_assignments":sorted(teaching,key=lambda x:(x["instructor_id"],x["subject_id"])),"mentorships":sorted(mentorships,key=lambda x:(x["mentor_instructor_id"],x["mentee_population_slot_ref"])),"tutoring_sessions":sorted(tutoring,key=lambda x:x["session_id"]),"mentoring_sessions":sorted(mentoring,key=lambda x:x["session_id"]),"recommendation_candidates":sorted(recs,key=lambda x:x["recommendation_candidate_id"]),"declined":sorted(declined,key=lambda x:(x["mentor_instructor_id"],x["cadet_slot_ref"])),"rejected_or_unresolved":sorted(rejected,key=lambda x:(x["kind"],str(x.get("mentor_instructor_id")),str(x.get("cadet_slot_ref")),x["reason"])),"truth_semantics":"instruction_tutoring_mentorship_recommendation_are_distinct","automatic_grade_awards":[],"automatic_qualification_awards":[],"automatic_discipline_actions":[],"future_step_state":{"wellbeing_effects":[],"obligation_consequences":[],"campus_event_mutations":[],"offscreen_execution":[],"social_lod":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
