#!/usr/bin/env python3
import argparse,json
from pathlib import Path
CLASS={1:"cadet_fourth_class",2:"cadet_third_class",3:"cadet_second_class",4:"cadet_first_class"}
RULES_VERSION="academy_year_progression_v0.2"
def resolve(r):
 y=int(r["academic_year"]);ev=r["evidence"];pol=r["policy"]
 if y not in CLASS:raise ValueError("invalid academic year")
 if r.get("authorized_leave_ref"):
  out="leave_of_absence"
 elif r.get("authorized_dismissal_ref"):
  out="dismissal"
 elif not ev.get("period_complete",False):
  return {"rules_version":RULES_VERSION,"outcome":"pending","reason":"period_not_complete","current_year":y,"current_class":CLASS[y],"mutations":[],"record_write":"deferred_step_19","truth_semantics":"progression_requires_evidence_not_elapsed_time","future_step_state":{"record_integration":[]}}
 else:
  fails=int(ev.get("failed_required_modules",0));rem=int(ev.get("remediation_open",0));pr=bool(ev.get("practical_requirements_complete",False));conduct=ev.get("conduct_status","good")
  if conduct=="blocks_progression":out="repeat_academic_year"
  elif fails==0 and pr and rem==0:out="graduation_pending" if y==4 else "advance"
  elif fails==0 and pr and rem>0:out="advance_with_remediation" if pol.get("allow_advance_with_remediation",False) and y<4 else "repeat_selected_modules"
  elif fails<=int(pol.get("max_failed_modules_for_selected_repeat",0)):out="repeat_selected_modules"
  else:out="repeat_academic_year"
 required=[];activation="resolved";target_year=(y+1 if out in {"advance","advance_with_remediation"} and y<4 else y);target_class=CLASS[target_year];active_year=target_year
 if y==2 and out in {"advance","advance_with_remediation"}:
  spec=r.get("specialization_selection")
  if not spec:
   required.append("specialization_selection");activation="pending_required_transition_action";active_year=y
  elif r.get("is_player",False) and not spec.get("explicit_player_choice",False):
   required.append("explicit_player_specialization_choice");activation="pending_required_transition_action";active_year=y
 if out=="graduation_pending":status="graduation_pending";active_year=4
 elif out=="leave_of_absence":status="leave_of_absence";active_year=y
 elif out=="dismissal":status="dismissed";active_year=y
 elif activation!="resolved":status="year_3_activation_pending_specialization"
 else:status=f"cadet_year_{target_year}"
 return {"rules_version":RULES_VERSION,"outcome":out,"current_year":y,"current_class":CLASS[y],"next_year":target_year,"next_class":target_class,"active_year_after_resolution":active_year,"active_class_after_resolution":CLASS[active_year],"next_academy_status":status,"activation_state":activation,"required_transition_actions":required,"identity_preserved":True,"history_preserved":True,"direct_rank_award":None,"direct_commission_award":None,"record_write":"deferred_step_19","truth_semantics":"progression_requires_evidence_not_elapsed_time","future_step_state":{"record_integration":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
