#!/usr/bin/env python3
import argparse,json
from pathlib import Path
CLASS={1:"cadet_fourth_class",2:"cadet_third_class",3:"cadet_second_class",4:"cadet_first_class"}
def resolve(r):
 y=int(r["academic_year"]);ev=r["evidence"];pol=r["policy"]
 if y not in CLASS:raise ValueError("invalid academic year")
 if not ev.get("period_complete",False):return {"outcome":"pending","reason":"period_not_complete","mutations":[]}
 if r.get("authorized_leave_ref"):out="leave_of_absence"
 elif r.get("authorized_dismissal_ref"):out="dismissal"
 else:
  fails=int(ev.get("failed_required_modules",0));rem=int(ev.get("remediation_open",0));pr=bool(ev.get("practical_requirements_complete",False));conduct=ev.get("conduct_status","good")
  if conduct=="blocks_progression":out="repeat_academic_year"
  elif fails==0 and pr and rem==0:out="graduation_pending" if y==4 else "advance"
  elif fails==0 and pr and rem>0:out="advance_with_remediation" if pol.get("allow_advance_with_remediation",False) and y<4 else "repeat_selected_modules"
  elif fails<=int(pol.get("max_failed_modules_for_selected_repeat",0)):out="repeat_selected_modules"
  else:out="repeat_academic_year"
 required=[];activation="resolved"
 if y==2 and out in {"advance","advance_with_remediation"}:
  spec=r.get("specialization_selection")
  if not spec:
   required.append("specialization_selection");activation="pending_required_transition_action"
  elif r.get("is_player",False) and not spec.get("explicit_player_choice",False):
   required.append("explicit_player_specialization_choice");activation="pending_required_transition_action"
 next_year=(y+1 if out in {"advance","advance_with_remediation"} and y<4 else y)
 next_class=(CLASS[next_year] if y<4 or out!="graduation_pending" else CLASS[4])
 next_status=("graduation_pending" if out=="graduation_pending" else ("leave_of_absence" if out=="leave_of_absence" else ("dismissed" if out=="dismissal" else f"cadet_year_{next_year}")))
 return {"outcome":out,"current_year":y,"current_class":CLASS[y],"next_year":next_year,"next_class":next_class,"next_academy_status":next_status,"activation_state":activation,"required_transition_actions":required,"identity_preserved":True,"history_preserved":True,"direct_rank_award":None,"direct_commission_award":None,"record_write":"deferred_step_19","truth_semantics":"progression_requires_evidence_not_elapsed_time","future_step_state":{"record_integration":[]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);a=p.parse_args();x=json.loads(a.input.read_text());print(json.dumps(resolve(x.get("request",x)),indent=2,sort_keys=True))
if __name__=="__main__":main()
