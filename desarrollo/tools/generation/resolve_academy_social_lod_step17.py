#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ORDER={"C":0,"B":1,"A":2}
def resolve(r):
 people=r["people"];ids=[x["population_slot_ref"] for x in people]
 if len(ids)!=len(set(ids)):raise ValueError("duplicate slot")
 out=[];trans=[]
 for p in sorted(people,key=lambda x:x["population_slot_ref"]):
  cur=p.get("current_lod","C");score=0
  score+=min(3,int(p.get("direct_interaction_count",0)))
  score+=3 if p.get("close_relationship",False) else 0
  score+=3 if p.get("mentor_or_mentee",False) else 0
  score+=2 if p.get("consequential_shared_history",False) else 0
  score+=1 if p.get("recurring_shared_activity",False) else 0
  target="A" if score>=5 else ("B" if score>=1 else "C")
  if p.get("known_persistent_identity",False) and target=="C":target="B"
  if p.get("allow_detail_reduction",False) and p.get("relevance_stale",False) and cur=="A" and target=="A":target="B"
  out.append({"population_slot_ref":p["population_slot_ref"],"lod":target,"identity_ref":p.get("identity_ref"),"history_refs":p.get("history_refs",[]),"truth_changed":False})
  if target!=cur:trans.append({"population_slot_ref":p["population_slot_ref"],"from":cur,"to":target,"effect":"simulation_detail_only"})
 return {"lod_states":out,"transitions":trans,"fabricated_major_events":[],"erased_history_refs":[],"truth_semantics":"lod_changes_detail_not_identity_or_history","future_step_state":{"year_progression":[],"record_integration":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
