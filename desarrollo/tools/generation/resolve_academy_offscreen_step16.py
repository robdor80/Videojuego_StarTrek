#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
RULES_VERSION="academy_offscreen_v0.1"
OPTIONAL_PLAYER={"free_time","social_optional","romance","extracurricular_optional","enrichment_optional","campus_optional"}
CONSEQUENTIAL={"evaluation","discipline_review","relationship_major","campus_crisis","injury","graduation_gate"}
def resolve(r):
 start,end=int(r["from_time"]),int(r["to_time"])
 if end<start:raise ValueError("invalid catchup interval")
 people={x["population_slot_ref"]:x for x in r["population"]}
 if len(people)!=len(r["population"]):raise ValueError("duplicate population slot")
 events=[]
 for e in r.get("scheduled_candidates",[]):
  if e["population_slot_ref"] not in people:raise ValueError("unknown participant")
  t=int(e["time"])
  if start<=t<end:events.append(e)
 events.sort(key=lambda x:(int(x["time"]),x["event_id"]))
 executed=[];explicit=[];unresolved=[];evidence=[];aggregates={}
 for e in events:
  p=people[e["population_slot_ref"]]
  if p.get("is_player",False) and e.get("choice_class") in OPTIONAL_PLAYER and not e.get("explicit_player_authorization",False):
   unresolved.append({"event_id":e["event_id"],"reason":"player_optional_choice_not_auto_resolved"});continue
  if not e.get("preconditions_satisfied",False):
   continue
  if not e.get("source_ref") and not e.get("cause_event_refs"):
   continue
  rec={"event_id":e["event_id"],"population_slot_ref":e["population_slot_ref"],"time":t,"activity_family":e["activity_family"],"source_ref":e.get("source_ref"),"cause_event_refs":e.get("cause_event_refs",[])}
  if e.get("consequence_class") in CONSEQUENTIAL:
   explicit.append(rec)
  else:
   k=(e["population_slot_ref"],e["activity_family"])
   aggregates[k]=aggregates.get(k,0)+int(e.get("duration_minutes",0))
  executed.append(e["event_id"])
  evidence.append({"event_id":e["event_id"],"evidence_family":e.get("evidence_family","activity"),"confirmed":True})
 return {
  "rules_version":RULES_VERSION,
  "executed_event_refs":executed,
  "routine_aggregates":[{"population_slot_ref":k[0],"activity_family":k[1],"duration_minutes":v} for k,v in sorted(aggregates.items())],
  "explicit_consequential_events":explicit,
  "unresolved_player_choices":unresolved,
  "downstream_evidence_candidates":evidence,
  "generated_events_not_in_input":[],
  "relationship_transitions_from_elapsed_time":[],
  "career_progression_from_elapsed_time":[],
  "checkpoint":{"from_time":start,"to_time":end,"last_event_ref":executed[-1] if executed else None},
  "truth_semantics":"offscreen_executes_authoritative_candidates_not_story_invention",
  "future_step_state":{"social_lod":[],"year_progression":[],"record_integration":[]}
 }
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
