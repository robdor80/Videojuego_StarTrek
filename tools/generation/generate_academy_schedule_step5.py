#!/usr/bin/env python3
"""Deterministic reference scheduler for Academy Life Step 5."""
from __future__ import annotations
import argparse, copy, hashlib, heapq, json
from pathlib import Path
from typing import Any

RULES_VERSION = "academy_personal_schedule_v0.1"

def stable_hex(*parts: Any, size: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def _validate_interval(item: dict[str, Any]) -> None:
    if int(item["start_minute"]) < 0 or int(item["end_minute"]) > 1440 or int(item["start_minute"]) >= int(item["end_minute"]):
        raise ValueError("invalid schedule interval")

def _travel_graph(request: dict[str, Any]) -> dict[str, list[tuple[str,int]]]:
    graph: dict[str, list[tuple[str,int]]] = {}
    for edge in request.get("travel_edges", []):
        a,b,m=edge["from"],edge["to"],int(edge["minutes"])
        if m < 0: raise ValueError("negative travel time")
        graph.setdefault(a,[]).append((b,m))
        if edge.get("bidirectional", True): graph.setdefault(b,[]).append((a,m))
    return graph

def travel_minutes(graph: dict[str,list[tuple[str,int]]], a: str, b: str) -> int | None:
    if a == b: return 0
    q=[(0,a)]; seen={}
    while q:
        d,node=heapq.heappop(q)
        if node in seen and seen[node] <= d: continue
        seen[node]=d
        if node == b: return d
        for nxt,cost in graph.get(node,[]): heapq.heappush(q,(d+cost,nxt))
    return None

def _no_overlap(entries: list[dict[str,Any]], candidate: dict[str,Any]) -> bool:
    return all(
        e["day_index"] != candidate["day_index"]
        or candidate["end_minute"] <= e["start_minute"]
        or candidate["start_minute"] >= e["end_minute"]
        for e in entries
    )

def _travel_feasible(entries: list[dict[str,Any]], candidate: dict[str,Any], graph: dict[str,list[tuple[str,int]]]) -> bool:
    same=sorted([e for e in entries if e["day_index"]==candidate["day_index"]]+[candidate],key=lambda x:(x["start_minute"],x["end_minute"],x["entry_id"]))
    for prev,nxt in zip(same,same[1:]):
        if prev["end_minute"] > nxt["start_minute"]: return False
        minutes=travel_minutes(graph,prev["location_ref"],nxt["location_ref"])
        if minutes is None or prev["end_minute"] + minutes > nxt["start_minute"]: return False
    return True

def build_schedules(request: dict[str,Any]) -> dict[str,Any]:
    seed=request["campaign_seed"]
    slots=[c["population_slot_ref"] for c in request["cadets"]]
    if len(slots)!=len(set(slots)): raise ValueError("duplicate cadet population_slot_ref")
    known=set(slots)
    graph=_travel_graph(request)
    day_start=int(request.get("day_start_minute",420)); day_end=int(request.get("day_end_minute",1320))
    if not 0 <= day_start < day_end <= 1440: raise ValueError("invalid day bounds")
    gran=int(request.get("slot_granularity_minutes",15))
    if gran <= 0: raise ValueError("invalid slot granularity")

    schedules={slot:[] for slot in slots}
    shared=copy.deepcopy(request.get("shared_commitments",[]))
    individual=copy.deepcopy(request.get("individual_commitments",[]))
    fixed=[]

    for item in shared:
        _validate_interval(item)
        for slot in sorted(item["member_slot_refs"]):
            if slot not in known: raise ValueError("shared commitment references unknown cadet")
            fixed.append({
                "entry_id":f'{item["commitment_id"]}:{slot}',"entry_type":item["entry_type"],
                "source_ref":item["commitment_id"],"population_slot_ref":slot,
                "day_index":int(item["day_index"]),"start_minute":int(item["start_minute"]),
                "end_minute":int(item["end_minute"]),"location_ref":item["location_ref"],
                "obligation_level":item.get("obligation_level","required"),"derived":False
            })
    for item in individual:
        _validate_interval(item)
        slot=item["population_slot_ref"]
        if slot not in known: raise ValueError("individual commitment references unknown cadet")
        fixed.append({
            "entry_id":item["commitment_id"],"entry_type":item["entry_type"],"source_ref":item["commitment_id"],
            "population_slot_ref":slot,"day_index":int(item["day_index"]),
            "start_minute":int(item["start_minute"]),"end_minute":int(item["end_minute"]),
            "location_ref":item["location_ref"],"obligation_level":item.get("obligation_level","required"),"derived":False
        })

    fixed.sort(key=lambda e:(e["population_slot_ref"],e["day_index"],e["start_minute"],e["entry_id"]))
    conflicts=[]
    for entry in fixed:
        slot=entry["population_slot_ref"]
        if not _no_overlap(schedules[slot],entry):
            conflicts.append({"population_slot_ref":slot,"type":"overlap","entry_ref":entry["entry_id"]})
        schedules[slot].append(entry)

    flexible=copy.deepcopy(request.get("flexible_requirements",[]))
    flexible.sort(key=lambda r:(len(r.get("allowed_windows",[])),r["population_slot_ref"],r["requirement_id"]))
    unresolved=[]
    for req in flexible:
        slot=req["population_slot_ref"]
        if slot not in known: raise ValueError("flexible requirement references unknown cadet")
        duration=int(req["duration_minutes"])
        candidates=[]
        for window in req.get("allowed_windows",[]):
            start=int(window["start_minute"]); end=int(window["end_minute"]); day=int(window["day_index"])
            if start < day_start or end > day_end or start >= end: raise ValueError("invalid flexible window")
            for s in range(start,end-duration+1,gran):
                c={"entry_id":f'{req["requirement_id"]}:{slot}',"entry_type":req["entry_type"],"source_ref":req["requirement_id"],
                   "population_slot_ref":slot,"day_index":day,"start_minute":s,"end_minute":s+duration,
                   "location_ref":req["location_ref"],"obligation_level":"required_flexible","derived":False}
                if _no_overlap(schedules[slot],c) and _travel_feasible(schedules[slot],c,graph):
                    candidates.append(c)
        if not candidates:
            unresolved.append({"population_slot_ref":slot,"requirement_ref":req["requirement_id"],"reason":"no_feasible_window"})
            continue
        chosen=min(candidates,key=lambda c:stable_hex(seed,"flex",slot,req["requirement_id"],c["day_index"],c["start_minute"],RULES_VERSION))
        schedules[slot].append(chosen)

    for slot in schedules: schedules[slot].sort(key=lambda e:(e["day_index"],e["start_minute"],e["entry_id"]))

    # Validate travel between final non-transit commitments, then derive just-in-time transit blocks.
    for slot,entries in schedules.items():
        for day in sorted({e["day_index"] for e in entries}):
            daily=[e for e in entries if e["day_index"]==day]
            for prev,nxt in zip(daily,daily[1:]):
                if prev["end_minute"] > nxt["start_minute"]: continue
                m=travel_minutes(graph,prev["location_ref"],nxt["location_ref"])
                if m is None:
                    conflicts.append({"population_slot_ref":slot,"type":"no_travel_path","from_entry_ref":prev["entry_id"],"to_entry_ref":nxt["entry_id"]})
                elif prev["end_minute"] + m > nxt["start_minute"]:
                    conflicts.append({"population_slot_ref":slot,"type":"insufficient_travel_time","from_entry_ref":prev["entry_id"],"to_entry_ref":nxt["entry_id"],"required_minutes":m})
                elif m > 0:
                    entries.append({
                        "entry_id":f'transit:{prev["entry_id"]}->{nxt["entry_id"]}',"entry_type":"transit","source_ref":"derived_travel",
                        "population_slot_ref":slot,"day_index":day,"start_minute":nxt["start_minute"]-m,
                        "end_minute":nxt["start_minute"],"location_ref":f'{prev["location_ref"]}->{nxt["location_ref"]}',
                        "from_location_ref":prev["location_ref"],"to_location_ref":nxt["location_ref"],
                        "obligation_level":"derived_required","derived":True
                    })
        entries.sort(key=lambda e:(e["day_index"],e["start_minute"],e["end_minute"],e["entry_id"]))

    free={}
    days=[int(d) for d in request.get("day_indices",[0,1,2,3,4])]
    for slot,entries in schedules.items():
        free[slot]=[]
        for day in days:
            busy=sorted([(e["start_minute"],e["end_minute"]) for e in entries if e["day_index"]==day])
            merged=[]
            for a,b in busy:
                if not merged or a>merged[-1][1]: merged.append([a,b])
                else: merged[-1][1]=max(merged[-1][1],b)
            cursor=day_start
            for a,b in merged:
                if cursor<a: free[slot].append({"day_index":day,"start_minute":cursor,"end_minute":a,"classification":"uncommitted"})
                cursor=max(cursor,b)
            if cursor<day_end: free[slot].append({"day_index":day,"start_minute":cursor,"end_minute":day_end,"classification":"uncommitted"})

    return {
        "rules_version":RULES_VERSION,
        "schedules":{slot:schedules[slot] for slot in sorted(schedules)},
        "uncommitted_intervals":{slot:free[slot] for slot in sorted(free)},
        "schedule_conflicts":sorted(conflicts,key=lambda x:json.dumps(x,sort_keys=True)),
        "unresolved_flexible_requirements":sorted(unresolved,key=lambda x:(x["population_slot_ref"],x["requirement_ref"])),
        "schedule_truth_semantics":"expected_not_actual_presence",
        "future_step_state":{"free_time_activity_assignments":[],"extracurricular_assignments":[],"social_events":[],"romance_state":[],"wellbeing_consequences":[],"disciplinary_consequences":[]}
    }

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(build_schedules(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0

if __name__=="__main__": raise SystemExit(main())
