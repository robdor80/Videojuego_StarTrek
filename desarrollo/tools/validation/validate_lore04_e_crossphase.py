#!/usr/bin/env python3
"""Crossphase LORE-04 editorial-integrity gate; not a live CoreRPG/UE5 test."""
from pathlib import Path
import json
from validate_lore04_phase import ROOT,validate,load,BASE,require
PHASES=("B","C","D","E")
DEPS={"B":"sistemas/gameplay/economy/replicator_post_scarcity_contract.json",
      "C":"sistemas/universe/generation/traffic_activity_model.json",
      "D":"sistemas/gameplay/organizations/organization_runtime_contract.json",
      "E":"proyecto/docs/roadmap/lore_04_a/A08_auditoria_pruebas_cierre.md"}
CORE_SHA="4f282863737bcd8f5add401202a9e1064c133672"
BASE_MAIN_SHA="1eea14b8257811c0a06e4f3e08c2032eed9c5d1f"
def audit_crossphase(manifests:dict):
    require(set(manifests)==set(PHASES),"B/C/D/E not all included")
    info={}
    for phase in PHASES:
        data=manifests[phase]
        require(data.get("phase")==phase,"Wrong phase object")
        require(data.get("world_state_owner")=="CoreRPG","CoreRPG owner lost")
        require(data.get("runtime_implemented") is False,"Fictitious runtime claim")
        require(len(data.get("cases",[]))>=({"B":10,"C":12,"D":12,"E":18}[phase]),"Missing test cases")
        info[phase]=len(data["cases"])
    require(manifests["B"].get("preserved_block_4")=="READY_TO_RESUME","Block 4 falsified")
    require(manifests["E"].get("integrated_phases")==["A","B","C","D"],"Integrated phases mismatch")
    require(manifests["E"].get("prior_prs_fused") is False,"Premature BCD merge assertion")
    require(manifests["E"].get("checked_corerpg_main_sha")==CORE_SHA,"CoreRPG audit snapshot mismatch")
    require(manifests["E"].get("checked_trek_main_sha")==BASE_MAIN_SHA,"Star Trek baseline mismatch")
    require("proyecto/docs/roadmap/lore_04_b/lore04b_cases_v0.1.json" in manifests["C"]["dependencies"],
           "C does not depend on economic documentation")
    require("proyecto/docs/roadmap/lore_04_c/lore04c_cases_v0.1.json" in manifests["D"]["dependencies"],
           "D does not depend on transport/infrastructure")
    for ph in ("B","C","D"):
        require("proyecto/docs/roadmap/lore_04_"+ph.lower()+"/lore04"+ph.lower()+"_cases_v0.1.json" in manifests["E"]["dependencies"],"E missing "+ph)
    civil=ROOT/"proyecto/docs/roadmap/lore_04_a/A08_auditoria_pruebas_cierre.md"
    require(civil.exists(),"A source not retained")
    require("CoreRPG" in civil.read_text(encoding="utf-8"),"A authority lost")
    require((ROOT/"proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md").read_text(encoding="utf-8").count("READY_TO_RESUME")>=1,
            "Economy dynamic block state changed")
    for phase,path in DEPS.items():
        require((ROOT/path).is_file(),"Dependency absent: "+path)
    for phase in ("B","C","D","E"):
        readme=(ROOT/(BASE+phase.lower()+"/README.md")).read_text(encoding="utf-8")
        require("CoreRPG" in readme or "WorldState" in readme,"README authority missing "+phase)
        require("sin merge" in readme.lower() or "no merge" in readme.lower() or "sin fusionar" in readme.lower(),
                "README prematurely claims merge "+phase)
    return {"cases_by_phase":info,"total_design_cases":sum(info.values()),"runtime":"NOT_TESTED","author_merge":"REQUIRED"}
def validate():
    items={p:load(BASE+p.lower()+f"/lore04{p.lower()}_cases_v0.1.json") for p in PHASES}
    results=[validate(p) for p in PHASES]
    x=audit_crossphase(items)
    x["validated_phases"]=[r["phase"] for r in results]
    x["A_in_main"]=True
    return x
if __name__=="__main__":
    print("LORE-04 E TRANSVERSAL DOCUMENTARY AUDIT:",validate())
