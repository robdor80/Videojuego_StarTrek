#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
RULES_VERSION="academy_record_integration_v0.2"
CANONICAL_TO_EVENT={
 "academy_admission":"academy_admission",
 "academic_evaluation":"academic_evaluation",
 "practical_evaluation":"academic_evaluation",
 "enrichment_completion":"academic_evaluation",
 "specialization_selected":"academy_specialization",
 "remediation_result":"academy_remediation",
 "validated_disciplinary_action":"disciplinary_action",
 "academy_year_progression":"academy_year_progression",
 "leave_of_absence":"leave_of_absence",
 "academy_dismissal":"academy_dismissal",
 "academy_graduation":"academy_graduation",
 "commission":"commission"
}
ALIASES={
 "admission":"academy_admission","evaluation":"academic_evaluation","practical":"practical_evaluation",
 "specialization":"specialization_selected","remediation":"remediation_result","discipline":"validated_disciplinary_action",
 "year_progression":"academy_year_progression","leave":"leave_of_absence","dismissal":"academy_dismissal","graduation":"academy_graduation"
}
EVENT_TO_LEGACY_FAMILY={"academy_admission":"academy_admission","academic_evaluation":"academic_evaluation","academy_specialization":"specialization_selected","academy_remediation":"remediation_result","disciplinary_action":"validated_disciplinary_action","academy_year_progression":"academy_year_progression","leave_of_absence":"leave_of_absence","academy_dismissal":"academy_dismissal","academy_graduation":"academy_graduation","commission":"commission"}
SERVICE=set(CANONICAL_TO_EVENT.values())
def canonical_family(v):return ALIASES.get(v,v)
def rid(c,f,s):return "acadrec:"+hashlib.sha256(f"{c}|{f}|{s}".encode()).hexdigest()[:20]
def existing_family(e):return e.get("source_family") or EVENT_TO_LEGACY_FAMILY.get(e.get("event_type"),e.get("event_type"))
def resolve(r):
 existing=list(r.get("existing_record_events",[]));seen={(existing_family(x),x["source_event_id"]) for x in existing};out=[];service=[];unlock=[];rejected=[]
 evidence=sorted(r.get("evidence_events",[]),key=lambda x:(str(x.get("effective_date","")),str(x.get("source_event_id","")),str(x.get("family",""))))
 for e in evidence:
  if not e.get("confirmed",False):continue
  if not e.get("source_event_id"):
   rejected.append({"family":e.get("family"),"reason":"missing_source_event_id"});continue
  fam=canonical_family(e.get("family"))
  if fam not in CANONICAL_TO_EVENT:
   rejected.append({"source_event_id":e["source_event_id"],"family":e.get("family"),"reason":"unknown_record_family"});continue
  typ=CANONICAL_TO_EVENT[fam];key=(fam,e["source_event_id"])
  if key in seen:continue
  rec={"record_event_id":rid(r["cadet_ref"],fam,e["source_event_id"]),"cadet_ref":r["cadet_ref"],"event_type":typ,"source_family":fam,"effective_date":e.get("effective_date"),"source_event_id":e["source_event_id"],"authority_id_if_any":e.get("authority_id"),"payload":e.get("payload",{})}
  if e.get("correction_of"):rec["supersedes_event_id_if_correction"]=e["correction_of"]
  out.append(rec);seen.add(key)
  if typ in SERVICE:service.append({"event_type":typ,"source_family":fam,"source_event_id":e["source_event_id"],"academy_record_event_ref":rec["record_event_id"]})
  if fam=="academy_graduation" and r.get("is_player",False):
   unlock.append({"unlock_id":"academy-complete:"+r["cadet_ref"],"player_profile_ref":r.get("player_profile_ref"),"graduation_event_ref":e["source_event_id"],"era_profile_ref":e.get("payload",{}).get("era_profile_ref"),"specialization_if_any":e.get("payload",{}).get("specialization")})
 return {"rules_version":RULES_VERSION,"appended_record_events":out,"service_record_bridge_candidates":service,"academy_completion_unlock_candidates":unlock,"rejected_or_unresolved":rejected,"modified_existing_events":[],"deleted_existing_events":[],"fabricated_first_assignments":[],"fabricated_commissions":[],"truth_semantics":"official_record_is_append_only_provenance_backed_and_idempotent","future_step_state":{"final_closure":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
