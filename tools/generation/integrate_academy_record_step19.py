#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
MAP={"admission":"academy_admission","evaluation":"academic_evaluation","practical":"academic_evaluation","enrichment_completion":"academic_evaluation","specialization":"academy_specialization","remediation":"academy_remediation","discipline":"disciplinary_action","year_progression":"academy_year_progression","leave":"leave_of_absence","dismissal":"academy_dismissal","graduation":"academy_graduation","commission":"commission"}
SERVICE={"academy_admission","academic_evaluation","academy_year_progression","academy_specialization","academy_remediation","disciplinary_action","leave_of_absence","academy_dismissal","academy_graduation","commission"}
def rid(c,f,s):return "acadrec:"+hashlib.sha256(f"{c}|{f}|{s}".encode()).hexdigest()[:20]
def resolve(r):
 existing=list(r.get("existing_record_events",[]));seen={(x["event_type"],x["source_event_id"]) for x in existing};out=[];service=[];unlock=[]
 for e in sorted(r.get("evidence_events",[]),key=lambda x:(x.get("effective_date",""),x["source_event_id"])):
  if not e.get("confirmed",False) or not e.get("source_event_id"):continue
  fam=e["family"]
  if fam not in MAP:continue
  typ=MAP[fam];key=(typ,e["source_event_id"])
  if key in seen:continue
  rec={"record_event_id":rid(r["cadet_ref"],typ,e["source_event_id"]),"cadet_ref":r["cadet_ref"],"event_type":typ,"effective_date":e.get("effective_date"),"source_event_id":e["source_event_id"],"authority_id_if_any":e.get("authority_id"),"payload":e.get("payload",{})}
  if e.get("correction_of"):rec["supersedes_event_id_if_correction"]=e["correction_of"]
  out.append(rec);seen.add(key)
  if typ in SERVICE:service.append({"event_type":typ,"source_event_id":e["source_event_id"],"academy_record_event_ref":rec["record_event_id"]})
  if fam=="graduation" and r.get("is_player",False):
   unlock.append({"unlock_id":"academy-complete:"+r["cadet_ref"],"player_profile_ref":r.get("player_profile_ref"),"graduation_event_ref":e["source_event_id"],"era_profile_ref":e.get("payload",{}).get("era_profile_ref"),"specialization_if_any":e.get("payload",{}).get("specialization")})
 return {"appended_record_events":out,"service_record_bridge_candidates":service,"academy_completion_unlock_candidates":unlock,"modified_existing_events":[],"deleted_existing_events":[],"fabricated_first_assignments":[],"fabricated_commissions":[],"truth_semantics":"official_record_is_append_only_provenance_backed_and_idempotent","future_step_state":{"final_closure":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
