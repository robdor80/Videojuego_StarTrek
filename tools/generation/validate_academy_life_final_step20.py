#!/usr/bin/env python3
import argparse,json
from pathlib import Path
def validate(r):
 steps=r["steps"]
 if len(steps)!=20 or sorted(x["step"] for x in steps)!=list(range(1,21)):raise ValueError("steps 1..20 required")
 incomplete=[x["step"] for x in steps if x["status"]!="COMPLETE"]
 slots=r["population_slots"]
 if len(slots)!=len(set(slots)):raise ValueError("duplicate population slot")
 if r["player_optional_choice_auto_selected"]:raise ValueError("player agency violation")
 if r["plan_equals_execution"]:raise ValueError("truth separation violation")
 if r["lod_changes_truth"]:raise ValueError("LOD truth violation")
 if r["record_mutable"]:raise ValueError("append-only violation")
 if r["elapsed_time_grants_progression"]:raise ValueError("time progression violation")
 if r["romance_canon"]!="adult_heterosexual_only":raise ValueError("romance canon violation")
 if r["graduation_directly_assigns_posting"]:raise ValueError("assignment fabrication")
 return {"academy_life_complete":not incomplete,"incomplete_steps":incomplete,"population_conserved":True,"player_agency_preserved":True,"plan_execution_separated":True,"lod_truth_preserved":True,"record_append_only":True,"progression_evidence_required":True,"romance_canon_locked":True,"graduation_assignment_not_fabricated":True,"next_work_item":"Procedural Dynamic Universe Block 4 — Living Interplanetary / Interstellar Economy"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(validate(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
