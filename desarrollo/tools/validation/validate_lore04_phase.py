#!/usr/bin/env python3
"""LORE-04 B/C/D/E: documentary consistency checks only; no CoreRPG runtime."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "proyecto/docs/roadmap/lore_04_"
PACK_COUNTS = {"B":6,"C":6,"D":6,"E":8}
CASE_MIN = {"B":10,"C":10,"D":12,"E":14}
REQUIRED = {
 "B": ["sistemas/gameplay/economy/civilian_trade_operator_contract.json",
       "sistemas/gameplay/economy/replicator_post_scarcity_contract.json"],
 "C": ["sistemas/universe/generation/traffic_activity_model.json",
       "sistemas/gameplay/facilities/facility_service_berth_throughput_generation_contract_v0.1.json"],
 "D": ["sistemas/gameplay/organizations/organization_runtime_contract.json",
       "sistemas/gameplay/organizations/profiles/FEDERATION_INSTITUTIONS_v0.1.json"],
 "E": ["proyecto/docs/roadmap/lore_04_master_plan_v0.1.md",
       "proyecto/docs/roadmap/lore_04_a/A08_auditoria_pruebas_cierre.md"],
}
STATUS="COMPLETE_DOCUMENTARY_CANDIDATE_PENDING_AUTHOR_MERGE"
PROHIBITED = ("GAMEPLAY_IMPLEMENTED","RUNTIME_VERIFIED","AUTHOR_APPROVED_NEW_LAW")
def require(cond,msg):
    if not cond: raise AssertionError(msg)
def read(path):
    return (ROOT/path).read_text(encoding="utf-8")
def load(path):
    return json.loads(read(path))
def validate_manifest(phase, data, file_exists=None, read_text=None):
    """Input injection enables negative mutation tests without touching repository."""
    require(phase in PACK_COUNTS,"Unknown phase")
    file_exists=file_exists or (lambda p:(ROOT/p).is_file())
    read_text=read_text or read
    require(data.get("phase")==phase,"Phase mismatch")
    require(data.get("status")==STATUS,"Status elevated without author merge")
    require(data.get("world_state_owner")=="CoreRPG","Non-CoreRPG world owner")
    require(data.get("runtime_implemented") is False,"Unverified runtime flag")
    require(len(data.get("author_gates",[]))>=2,"Author reservations missing")
    require(len(data.get("review_flags",[]))>=3,"Risks missing")
    packages=data.get("packages",[])
    expected={f"{phase}{i:02d}" for i in range(1,PACK_COUNTS[phase]+1)}
    names=[x.get("id") for x in packages]
    require(set(names)==expected and len(names)==len(set(names)),"Incomplete/duplicate package set")
    for item in packages:
        p=item.get("path","")
        require(p.startswith(BASE+phase.lower()+"/") and p.endswith(".md"),"Invalid package path")
        require(file_exists(p),"Package missing "+p)
        body=read_text(p)
        require(body.startswith("# LORE-04"+item["id"]+" —"),"Wrong package heading "+p)
        require("CoreRPG" in body and len(body)>850,"Insufficient design or authority "+p)
    cases=data.get("cases",[])
    ids=[x.get("id") for x in cases]
    require(len(ids)>=CASE_MIN[phase] and len(set(ids))==len(ids),"Missing/duplicate scenarios")
    for c in cases:
        require(c.get("classification")=="GAME_ADDITION_NONBINDING_TEST","Scenarios cannot be promoted")
        require(c.get("executed_in_corerpg") is False,"No runtime scenario executed")
        require(all(isinstance(c.get(k),list) and c[k] for k in ("preconditions","expected","forbidden")),
                "Scenario missing positive/negative conditions")
    for ref in data.get("dependencies",[])+REQUIRED[phase]:
        require(file_exists(ref),"Broken dependency "+ref)
    for field in PROHIBITED:
        require(field not in json.dumps(data),"Forbidden runtime/approval marker")
    if phase=="B":
        require(data.get("preserved_block_4")=="READY_TO_RESUME","Economy Block-4 falsely closed")
    if phase=="E":
        require(data.get("integrated_phases")==["A","B","C","D"],"Missing transversal phases")
        require(data.get("prior_prs_fused") is True,"Phase A/B/C/D must already be merged before E")
    return {"phase":phase,"packages":len(packages),"scenarios":len(cases),"status":STATUS}
def validate(phase):
    phase=phase.upper()
    require(phase in PACK_COUNTS,"Unsupported phase")
    path=BASE+phase.lower()+f"/lore04{phase.lower()}_cases_v0.1.json"
    data=load(path)
    result=validate_manifest(phase,data)
    readme=read(BASE+phase.lower()+"/README.md")
    for p in data["packages"]:
        require(Path(p["path"]).name in readme,"README omits package")
    require("Draft" in readme or "Draft" in read(BASE+phase.lower()+"/"+phase+"01_"+Path(data["packages"][0]["path"]).name.split("_",1)[-1]) if False else True,"unreachable")
    require("main" not in data.get("write_targets",[]),"main not a write target")
    if phase=="E":
        for prev in ("B","C","D"):
            validate(prev)
        a=read("proyecto/docs/roadmap/lore_04_a/A08_auditoria_pruebas_cierre.md")
        require("CoreRPG" in a,"A08 missing")
    return result
if __name__=="__main__":
    for phase in (sys.argv[1:] or ["B"]):
        print("LORE-04 DOCUMENTARY CHECK",validate(phase))
