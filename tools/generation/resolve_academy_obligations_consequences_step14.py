#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, json
from pathlib import Path

RULES_VERSION="academy_obligations_consequences_v0.1"
FORMAL_MEASURES={"warning":1,"negative_note":2,"restriction":2,"formal_reprimand":3,"remove_from_position":3,"disciplinary_transfer":3,"demotion":4,"brig_confinement":4,"court_martial":5,"stripped_of_rank_or_commission":5}
NO_FAULT_REASONS={"approved_medical","authorized_leave","institutional_schedule_conflict","emergency_preemption","authorized_accommodation"}

def resolve(request):
    cadets=copy.deepcopy(request["cadets"]); obligations=copy.deepcopy(request["obligations"]); evidences=copy.deepcopy(request.get("obligation_evidence",[])); justifications=copy.deepcopy(request.get("justifications",[])); prior=copy.deepcopy(request.get("prior_consequence_history",[])); authorities={a["authority_id"]:a for a in request.get("authorities",[])}; decisions=copy.deepcopy(request.get("disciplinary_decisions",[]))
    slots=[c["population_slot_ref"] for c in cadets]
    if len(slots)!=len(set(slots)): raise ValueError("duplicate cadet population_slot_ref")
    by_slot={c["population_slot_ref"]:c for c in cadets}
    oids=[o["obligation_id"] for o in obligations]
    if len(oids)!=len(set(oids)): raise ValueError("duplicate obligation_id")
    by_ob={o["obligation_id"]:o for o in obligations}
    for o in obligations:
        if o["population_slot_ref"] not in by_slot: raise ValueError("obligation references unknown cadet")
        if int(o["start_minute"])>=int(o["end_minute"]): raise ValueError("invalid obligation interval")
        if int(o.get("tolerance_minutes",0))<0: raise ValueError("negative tolerance")
    ev_by_ob={}; rejected=[]
    for e in evidences:
        if e["obligation_id"] not in by_ob or e["population_slot_ref"] not in by_slot:
            rejected.append({"ref":e["event_id"],"reason":"unknown_obligation_or_cadet"}); continue
        if by_ob[e["obligation_id"]]["population_slot_ref"]!=e["population_slot_ref"]:
            rejected.append({"ref":e["event_id"],"reason":"obligation_cadet_mismatch"}); continue
        if not e.get("confirmed",False) or not e.get("cause_event_refs"):
            rejected.append({"ref":e["event_id"],"reason":"missing_confirmed_provenance"}); continue
        ev_by_ob.setdefault(e["obligation_id"],[]).append(e)
    just_by_ob={}
    for j in justifications:
        if j["obligation_id"] not in by_ob:
            rejected.append({"ref":j["justification_id"],"reason":"unknown_obligation"}); continue
        if j["population_slot_ref"]!=by_ob[j["obligation_id"]]["population_slot_ref"]:
            rejected.append({"ref":j["justification_id"],"reason":"justification_cadet_mismatch"}); continue
        if not j.get("cause_event_refs"):
            rejected.append({"ref":j["justification_id"],"reason":"missing_justification_provenance"}); continue
        if j.get("status")=="approved":
            auth=authorities.get(j.get("authority_id"))
            if not auth or "approve_justification" not in set(auth.get("scopes",[])):
                rejected.append({"ref":j["justification_id"],"reason":"invalid_justification_authority"}); continue
        just_by_ob.setdefault(j["obligation_id"],[]).append(j)
    history_count={}
    for h in prior:
        if h.get("counts_for_recurrence",False):
            key=(h["population_slot_ref"],h["obligation_family"]); history_count[key]=history_count.get(key,0)+1
    resolutions=[]; consequence_records=[]; reviews=[]
    for oid in sorted(by_ob):
        o=by_ob[oid]; slot=o["population_slot_ref"]; events=sorted(ev_by_ob.get(oid,[]),key=lambda x:x["event_id"]); js=just_by_ob.get(oid,[]); approved=next((j for j in js if j.get("status")=="approved"),None); pending=any(j.get("status")=="pending" for j in js)
        if not o.get("mandatory",True):
            withdrawn=next((e for e in events if e.get("outcome")=="authorized_withdrawal" and int(e.get("occurred_minute",o["start_minute"]))<=int(o.get("withdrawal_deadline_minute",o["start_minute"]))),None)
            if withdrawn:
                resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"withdrawn_without_breach","fault":"none","evidence_refs":[withdrawn["event_id"]]}); continue
        if approved and approved.get("reason_code") in NO_FAULT_REASONS:
            makeup=bool(o.get("makeup_required_when_excused",False)); resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"excused","fault":"none","justification_ref":approved["justification_id"],"makeup_required":makeup})
            if makeup: consequence_records.append({"consequence_id":f"makeup:{oid}","obligation_id":oid,"population_slot_ref":slot,"type":"make_up_required","disciplinary":False,"record_write":"deferred_step_19"})
            continue
        if pending and not events:
            resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"pending_justification","fault":"unresolved"}); continue
        if not events:
            resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"missing_evidence","fault":"unresolved"}); continue
        e=events[-1]; outcome=e["outcome"]
        if outcome=="completed": resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"fulfilled","fault":"none","evidence_refs":[e["event_id"]]})
        elif outcome=="late":
            delay=max(0,int(e.get("actual_start_minute",o["start_minute"]))-int(o["start_minute"]))
            if delay<=int(o.get("tolerance_minutes",0)): resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"fulfilled_within_tolerance","fault":"none","delay_minutes":delay})
            else:
                resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"late_breach","fault":"attributable","delay_minutes":delay}); consequence_records.append({"consequence_id":f"attendance:{oid}","obligation_id":oid,"population_slot_ref":slot,"type":"attendance_concern","disciplinary":False,"record_write":"deferred_step_19"})
        elif outcome in {"incomplete","failed_required_activity"}:
            resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"performance_breach","fault":"not_assumed_misconduct"}); consequence_records.append({"consequence_id":f"remediation:{oid}","obligation_id":oid,"population_slot_ref":slot,"type":"remediation_required","disciplinary":False,"record_write":"deferred_step_19"})
        elif outcome=="absent":
            if e.get("reason_code") in NO_FAULT_REASONS:
                resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"no_fault_absence","fault":"none"})
                if o.get("makeup_required_when_excused",False): consequence_records.append({"consequence_id":f"makeup:{oid}","obligation_id":oid,"population_slot_ref":slot,"type":"make_up_required","disciplinary":False,"record_write":"deferred_step_19"})
            else:
                resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"unexcused_absence","fault":"attributable"}); fam=o.get("obligation_family",o.get("obligation_type","other")); recurrence=history_count.get((slot,fam),0)+1; consequence_records.append({"consequence_id":f"attendance:{oid}","obligation_id":oid,"population_slot_ref":slot,"type":"attendance_concern","disciplinary":False,"recurrence_count":recurrence,"record_write":"deferred_step_19"})
                if recurrence>=int(o.get("formal_review_recurrence_threshold",999)): reviews.append({"review_id":f"review:{oid}","obligation_id":oid,"population_slot_ref":slot,"review_reason":"repeated_unexcused_obligation_failure","severity_candidate":min(3,1+recurrence//2),"status":"pending_authority_review"})
        elif outcome in {"misconduct","unsafe_conduct","disobeyed_order"}:
            severity=max(1,min(5,int(e.get("severity_candidate",1)))); resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"conduct_breach","fault":"review_required","intent":e.get("intent","unknown"),"harm_level":e.get("harm_level","none")}); reviews.append({"review_id":f"review:{oid}","obligation_id":oid,"population_slot_ref":slot,"review_reason":outcome,"severity_candidate":severity,"status":"pending_authority_review","context_refs":copy.deepcopy(e.get("cause_event_refs",[]))})
        elif outcome=="authorized_withdrawal": resolutions.append({"obligation_id":oid,"population_slot_ref":slot,"resolution":"authorized_withdrawal","fault":"none"})
        else: rejected.append({"ref":e["event_id"],"reason":"unsupported_obligation_outcome"})
    review_by_ob={r["obligation_id"]:r for r in reviews}; disciplinary_actions=[]
    for d in decisions:
        oid=d["obligation_id"]; slot=d["population_slot_ref"]
        if oid not in by_ob or slot not in by_slot or by_ob.get(oid,{}).get("population_slot_ref")!=slot:
            rejected.append({"ref":d["decision_id"],"reason":"invalid_disciplinary_reference"}); continue
        review=review_by_ob.get(oid)
        if not review:
            rejected.append({"ref":d["decision_id"],"reason":"no_formal_review_basis"}); continue
        if not d.get("confirmed",False) or not d.get("cause_event_refs"):
            rejected.append({"ref":d["decision_id"],"reason":"missing_disciplinary_provenance"}); continue
        measure=d["measure_id"]
        if measure not in FORMAL_MEASURES:
            rejected.append({"ref":d["decision_id"],"reason":"unknown_discipline_measure"}); continue
        auth=authorities.get(d.get("authority_id"))
        if not auth or "formal_discipline" not in set(auth.get("scopes",[])):
            rejected.append({"ref":d["decision_id"],"reason":"invalid_discipline_authority"}); continue
        sev=FORMAL_MEASURES[measure]
        if sev>int(auth.get("max_measure_severity",0)):
            rejected.append({"ref":d["decision_id"],"reason":"authority_severity_exceeded"}); continue
        if sev>int(review["severity_candidate"])+1:
            rejected.append({"ref":d["decision_id"],"reason":"measure_disproportionate_to_review_context"}); continue
        disciplinary_actions.append({"decision_id":d["decision_id"],"obligation_id":oid,"population_slot_ref":slot,"measure_id":measure,"severity":sev,"authority_id":d["authority_id"],"record_write":"deferred_step_19","year_progression_effect":"deferred_step_18"})
    return {"rules_version":RULES_VERSION,"obligation_resolutions":resolutions,"non_disciplinary_consequences":consequence_records,"formal_review_candidates":reviews,"validated_disciplinary_actions":disciplinary_actions,"rejected_or_unresolved":sorted(rejected,key=lambda x:(str(x["ref"]),x["reason"])),"wellbeing_is_context_not_automatic_excuse":True,"no_universal_sentencing_table":True,"player_choices_forced":[],"record_writes":[],"year_progression_mutations":[],"future_step_state":{"campus_events":[],"offscreen_execution":[],"social_lod":[],"year_progression":[],"academy_record_integration":[]}}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
    payload=json.loads(a.input.read_text(encoding="utf-8"));print(json.dumps(resolve(payload.get("request",payload)),ensure_ascii=False,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
