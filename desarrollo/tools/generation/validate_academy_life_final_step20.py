#!/usr/bin/env python3
from __future__ import annotations
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EXPECTED_STEP_ANCHORS=[
"sistemas/gameplay/careers/academy_path/life/academy_population_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_cadet_generation_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_academic_group_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_quarters_housing_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_personal_schedule_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_free_time_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_extracurricular_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_academic_enrichment_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_social_life_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_romance_dating_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_npc_relationship_evolution_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_mentor_instructor_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_wellbeing_balance_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_obligation_consequence_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_campus_event_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_offscreen_life_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_social_lod_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_year_progression_continuity_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_record_integration_contract_v0.1.json",
"sistemas/gameplay/careers/academy_path/life/academy_life_final_closure_contract_v1.0.json"]
CANONICAL_RECORD_FAMILIES={"academy_admission","academic_evaluation","practical_evaluation","enrichment_completion","specialization_selected","remediation_result","validated_disciplinary_action","academy_year_progression","leave_of_absence","academy_dismissal","academy_graduation","commission"}
def load(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def collect_file_refs(v,out):
 if isinstance(v,str) and "/" in v and v.endswith((".json",".md",".py")):out.add(v)
 elif isinstance(v,list):
  for x in v:collect_file_refs(x,out)
 elif isinstance(v,dict):
  for x in v.values():collect_file_refs(x,out)
def import_module(rel,name):
 p=ROOT/rel;spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(m);return m
def audit_repo(root=ROOT):
 global ROOT;ROOT=Path(root)
 errors=[];json_errors=[];refs=set()
 json_paths=list((ROOT/"sistemas/gameplay/careers/academy_path/life").glob("*.json"))+list((ROOT/"desarrollo/validation/fixtures/academy_life").glob("*.json"))+list((ROOT/"desarrollo/validation/consistency").glob("academy_*.json"))
 core=["sistemas/gameplay/careers/academy_path/academy_state.json","sistemas/gameplay/careers/academy_path/cadet_progression.json","sistemas/gameplay/careers/academy_path/graduation_model.json","sistemas/gameplay/social/adult_heterosexual_relationship_canon_v0.1.json","sistemas/gameplay/careers/service_record/service_record_model.json"]
 for p in json_paths:
  try:collect_file_refs(json.loads(p.read_text(encoding="utf-8")),refs)
  except Exception as e:json_errors.append({"path":str(p.relative_to(ROOT)),"error":str(e)})
 for rel in core:
  try:collect_file_refs(load(rel),refs)
  except Exception as e:json_errors.append({"path":rel,"error":str(e)})
 broken=sorted(x for x in refs if not (ROOT/x).is_file())
 status=load("proyecto/docs/roadmap/academy_life_social_simulation_status_v0.1.json")
 summary=status["summary"];steps=status["steps"]
 status_ok=summary=={"total_steps":20,"complete":20,"partial":0,"todo":0,"current_step":20} and len(steps)==20 and all(x["status"]=="COMPLETE" for x in steps)
 if not status_ok:errors.append("academy status is not clean 20/20")
 anchors_missing=[x for x in EXPECTED_STEP_ANCHORS if not (ROOT/x).is_file()]
 if anchors_missing:errors.append("missing step anchors")
 canon=load("sistemas/gameplay/social/adult_heterosexual_relationship_canon_v0.1.json")
 canon_ok=canon.get("status")=="AUTHOR_CANON_LOCKED" and canon.get("immutability")=="FIXED_BY_AUTHOR" and canon.get("principles",{}).get("romantic_orientation_policy")=="heterosexual_only" and canon.get("principles",{}).get("sexual_relationship_policy")=="heterosexual_only"
 if not canon_ok:errors.append("relationship canon lock mismatch")
 state=load("sistemas/gameplay/careers/academy_path/academy_state.json")
 state_ok=state.get("schema_version")=="1.0.0" and state.get("academy_life_final_closure_ref")=="sistemas/gameplay/careers/academy_path/life/academy_life_final_closure_contract_v1.0.json"
 if not state_ok:errors.append("academy_state final closure mismatch")
 record=load("sistemas/gameplay/careers/academy_path/life/academy_record_model_v0.1.json")
 record_ok=record.get("mutable_history") is False and record.get("narrative_summary_is_derived") is True and "source_family" in record.get("event_fields",[])
 if not record_ok:errors.append("academy record is not append-only/source-family safe")
 record_contract=load("sistemas/gameplay/careers/academy_path/life/academy_record_integration_contract_v0.1.json")
 record_families=set(record_contract.get("recordable_families",[]))
 record_family_ok=record_families==CANONICAL_RECORD_FAMILIES
 if not record_family_ok:errors.append("recordable family contract drift")
 recmod=import_module("desarrollo/tools/generation/integrate_academy_record_step19.py","academy_record_step19_audit")
 resolver_family_ok=set(recmod.CANONICAL_TO_EVENT)==CANONICAL_RECORD_FAMILIES
 if not resolver_family_ok:errors.append("record resolver family drift")
 progression=load("sistemas/gameplay/careers/academy_path/cadet_progression.json")
 progression_ok="graduation_pending" in progression.get("possible_year_outcomes",[])
 if not progression_ok:errors.append("graduation_pending missing from progression")
 service=load("sistemas/gameplay/careers/service_record/service_record_model.json")
 required_service={"academy_admission","academic_evaluation","academy_year_progression","academy_specialization","academy_remediation","disciplinary_action","leave_of_absence","academy_dismissal","academy_graduation","commission"}
 service_ok=required_service.issubset(set(service.get("event_types",[])))
 if not service_ok:errors.append("service-record Academy bridge event types incomplete")
 manifest=load("desarrollo/validation/consistency/academy_life_final_acceptance_manifest_v1.0.json")
 scripts=manifest.get("test_scripts",[]);missing_scripts=[x for x in scripts if not (ROOT/x).is_file()]
 count=sum(len(re.findall(r"^\s*def test_", (ROOT/x).read_text(encoding="utf-8"), flags=re.M)) for x in scripts if (ROOT/x).is_file())
 manifest_ok=len(scripts)==20 and not missing_scripts and count==manifest.get("total_defined_tests")
 if not manifest_ok:errors.append("test manifest/count drift")
 py_errors=[]
 for p in sorted((ROOT/"desarrollo/tools/generation").glob("*.py")):
  if "academy" not in p.name and "cadet" not in p.name:continue
  try:compile(p.read_text(encoding="utf-8"),str(p),"exec")
  except SyntaxError as e:py_errors.append({"path":str(p.relative_to(ROOT)),"error":str(e)})
 if py_errors:errors.append("Python syntax errors")
 workflow=(ROOT/".github/workflows/academy-life-closure.yml").read_text(encoding="utf-8")
 workflow_ok="validate_academy_life_final_step20.py" in workflow and "run_academy_life_suite.py" in workflow
 if not workflow_ok:errors.append("CI workflow not wired to validator+suite runner")
 plan=(ROOT/"proyecto/docs/roadmap/academy_life_social_simulation_plan_v0.1.md").read_text(encoding="utf-8")
 dyn=(ROOT/"proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md").read_text(encoding="utf-8")
 content=(ROOT/"CONTENT_STATUS.md").read_text(encoding="utf-8")
 life=(ROOT/"sistemas/gameplay/careers/academy_path/life/README.md").read_text(encoding="utf-8")
 gate_ok=status.get("deferred_after_step_20",{}).get("status")=="READY_TO_RESUME" and "READY_TO_RESUME" in plan and "READY_TO_RESUME" in dyn and "READY_TO_RESUME" in content
 if not gate_ok:errors.append("Dynamic Universe Block 4 gate is inconsistent")
 docs_ok="Final closure remains Step 20." not in life
 if not docs_ok:errors.append("obsolete Step-20 README wording remains")
 closure=load("sistemas/gameplay/careers/academy_path/life/academy_life_final_closure_contract_v1.0.json")
 closure_ok=closure.get("status")=="ACADEMY_LIFE_20_OF_20_COMPLETE" and closure.get("runtime_ownership",{}).get("core_rpg")
 if not closure_ok:errors.append("final closure/runtime boundary mismatch")
 if json_errors:errors.append("JSON parse errors")
 if broken:errors.append("broken repository file references")
 return {"ok":not errors,"errors":errors,"status_ok":status_ok,"json_parse_errors":json_errors,"broken_file_refs":broken,"missing_step_anchors":anchors_missing,"canon_ok":canon_ok,"academy_state_ok":state_ok,"record_model_ok":record_ok,"record_family_contract_ok":record_family_ok,"record_resolver_family_ok":resolver_family_ok,"progression_ok":progression_ok,"service_record_bridge_ok":service_ok,"manifest_ok":manifest_ok,"manifest_test_script_count":len(scripts),"defined_test_count":count,"missing_test_scripts":missing_scripts,"python_syntax_errors":py_errors,"workflow_ok":workflow_ok,"dynamic_universe_gate_ok":gate_ok,"docs_ok":docs_ok,"closure_ok":closure_ok,"next_work_item":manifest.get("next_work_item")}
def main():
 p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=ROOT);a=p.parse_args();r=audit_repo(a.root);print(json.dumps(r,indent=2,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
