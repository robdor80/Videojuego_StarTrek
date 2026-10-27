#!/usr/bin/env python3
"""Deterministic reference grouping for Academy Life Step 3."""
from __future__ import annotations
import argparse,copy,hashlib,json,math
from pathlib import Path
from typing import Any
RULES_VERSION="academy_grouping_v0.1";VALID_CLASSES={"cadet_fourth_class","cadet_third_class","cadet_second_class","cadet_first_class"}
def stable_hex(*parts:Any,size:int=16)->str:return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]
def stable_order(seed:str,subsystem:str,items:list[dict[str,Any]])->list[dict[str,Any]]:return sorted(copy.deepcopy(items),key=lambda item:stable_hex(seed,subsystem,item["population_slot_ref"],RULES_VERSION))
def chunks(items:list[Any],size:int)->list[list[Any]]:
    if size<=0:raise ValueError("group size must be positive")
    return [items[i:i+size] for i in range(0,len(items),size)]
def member_label(member:dict[str,Any])->str:
    if member.get("specialization"):return str(member["specialization"])
    interests=list(member.get("branch_interest_ids",[]));return str(interests[0]) if interests else "undecided"
def validate_roster(roster:list[dict[str,Any]])->list[str]:
    errors=[];slots=set();characters=set()
    for member in roster:
        slot=member.get("population_slot_ref")
        if not slot:errors.append("missing_population_slot_ref");continue
        if slot in slots:errors.append(f"duplicate_slot:{slot}")
        slots.add(slot)
        if member.get("cadet_class_id") not in VALID_CLASSES:errors.append(f"invalid_cadet_class:{slot}")
        cid=member.get("character_id")
        if cid:
            if cid in characters:errors.append(f"duplicate_character:{cid}")
            characters.add(cid)
    return errors
def generate_groups(request:dict[str,Any])->dict[str,Any]:
    roster=copy.deepcopy(request["roster"]);errors=validate_roster(roster)
    if errors:raise ValueError(";".join(errors))
    seed=request["campaign_seed"];cap=int(request.get("class_section_capacity",12));study_size=int(request.get("study_group_size",4));participation=int(request.get("study_group_participation_percent",100))
    if not 0<=participation<=100:raise ValueError("study_group_participation_percent must be 0..100")
    sections=[]
    for cls in sorted({m["cadet_class_id"] for m in roster}):
        members=stable_order(seed,f"class_section:{cls}",[m for m in roster if m["cadet_class_id"]==cls])
        for idx,group in enumerate(chunks(members,cap),1):sections.append({"group_id":f"section:{cls}:{idx:03d}","group_type":"class_section","cadet_class_id":cls,"member_slot_refs":[m["population_slot_ref"] for m in group],"automatic_relationship_effect":"none"})
    studies=[];by_slot={m["population_slot_ref"]:m for m in roster}
    for section in sections:
        eligible=[]
        for slot in section["member_slot_refs"]:
            if int(stable_hex(seed,"study_participation",slot,RULES_VERSION,size=8),16)%100<participation:eligible.append(by_slot[slot])
        eligible=stable_order(seed,f"study:{section['group_id']}",eligible)
        for idx,group in enumerate(chunks(eligible,study_size),1):
            if len(group)>=2:studies.append({"group_id":f"study:{section['cadet_class_id']}:{section['group_id'].split(':')[-1]}:{idx:03d}","group_type":"study_group","formation_mode":"academy_assigned_peer_study","parent_section_ref":section["group_id"],"member_slot_refs":[m["population_slot_ref"] for m in group],"automatic_relationship_effect":"none"})
    practical=[]
    for pc in request.get("practical_courses",[]):
        eligible=[m for m in roster if pc["course_id"] in m.get("course_ids",[]) and (not pc.get("cadet_class_id") or m["cadet_class_id"]==pc["cadet_class_id"])]
        size=int(pc.get("team_size",4));policy=pc.get("composition_policy","deterministic");teams=[]
        if policy=="specialization_aligned":
            buckets={}
            for m in eligible:buckets.setdefault(member_label(m),[]).append(m)
            for label in sorted(buckets):teams.extend(chunks(stable_order(seed,f"practice:{pc['course_id']}:{label}",buckets[label]),size))
        elif policy=="cross_branch":
            if eligible:
                count=math.ceil(len(eligible)/size);teams=[[] for _ in range(count)];buckets={}
                for m in eligible:buckets.setdefault(member_label(m),[]).append(m)
                cursor=0
                for label in sorted(buckets):
                    for m in stable_order(seed,f"practice_cross:{pc['course_id']}:{label}",buckets[label]):
                        candidates=[i for i,t in enumerate(teams) if len(t)<size]
                        best=min(candidates,key=lambda i:(sum(1 for x in teams[i] if member_label(x)==label),len(teams[i]),(i-cursor)%count));teams[best].append(m);cursor=(best+1)%count
        else:teams=chunks(stable_order(seed,f"practice:{pc['course_id']}",eligible),size)
        for idx,team in enumerate(teams,1):
            if team:practical.append({"group_id":f"practice:{pc['course_id']}:{idx:03d}","group_type":"practical_team","course_id":pc["course_id"],"cadet_class_id":pc.get("cadet_class_id"),"composition_policy":policy,"member_slot_refs":[m["population_slot_ref"] for m in team],"branch_labels":sorted({member_label(m) for m in team}),"automatic_relationship_effect":"none"})
    return {"rules_version":RULES_VERSION,"class_sections":sections,"study_groups":studies,"practical_teams":practical,"future_step_state":{"roommate_assignments":[],"personal_schedules":[],"social_relationship_changes":[],"romance_state":[]}}
def memberships_for_slot(result:dict[str,Any],slot:str)->list[str]:
    return sorted(g["group_id"] for c in ("class_sections","study_groups","practical_teams") for g in result.get(c,[]) if slot in g.get("member_slot_refs",[]))
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args();payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(generate_groups(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
