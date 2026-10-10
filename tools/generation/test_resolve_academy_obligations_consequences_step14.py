import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"resolve_academy_obligations_consequences_step14.py";FIXTURE=ROOT/"validation/fixtures/academy_life/obligations_consequences_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("m",MODULE);m=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=m;spec.loader.exec_module(m)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return m.resolve(req())
def res(o,oid):return next(x for x in o["obligation_resolutions"] if x["obligation_id"]==oid)
class AcademyObligationsConsequencesStep14Tests(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_medical_excuse_no_fault(self):self.assertEqual(res(out(),"O1")["resolution"],"excused")
 def test_03_excused_can_require_makeup(self):self.assertTrue(any(x["obligation_id"]=="O1" and x["type"]=="make_up_required" for x in out()["non_disciplinary_consequences"]))
 def test_04_excused_not_disciplinary(self):self.assertFalse(any(x["obligation_id"]=="O1" for x in out()["formal_review_candidates"]))
 def test_05_unexcused_absence_detected(self):self.assertEqual(res(out(),"O2")["resolution"],"unexcused_absence")
 def test_06_recurrence_can_trigger_review(self):self.assertTrue(any(x["obligation_id"]=="O2" for x in out()["formal_review_candidates"]))
 def test_07_serious_conduct_review(self):self.assertTrue(any(x["obligation_id"]=="O3" and x["review_reason"]=="disobeyed_order" for x in out()["formal_review_candidates"]))
 def test_08_valid_formal_decision(self):self.assertTrue(any(x["decision_id"]=="D1" for x in out()["validated_disciplinary_actions"]))
 def test_09_voluntary_withdrawal_no_breach(self):self.assertEqual(res(out(),"O4")["resolution"],"withdrawn_without_breach")
 def test_10_within_tolerance_no_breach(self):self.assertEqual(res(out(),"O5")["resolution"],"fulfilled_within_tolerance")
 def test_11_incomplete_requires_remediation(self):self.assertTrue(any(x["obligation_id"]=="O6" and x["type"]=="remediation_required" for x in out()["non_disciplinary_consequences"]))
 def test_12_incomplete_not_automatic_misconduct(self):self.assertEqual(res(out(),"O6")["fault"],"not_assumed_misconduct")
 def test_13_wellbeing_not_auto_excuse(self):self.assertTrue(out()["wellbeing_is_context_not_automatic_excuse"])
 def test_14_no_universal_sentence_table(self):self.assertTrue(out()["no_universal_sentencing_table"])
 def test_15_no_record_write_step14(self):self.assertEqual(out()["record_writes"],[])
 def test_16_no_year_progression_step14(self):self.assertEqual(out()["year_progression_mutations"],[])
 def test_17_no_forced_player_choice(self):self.assertEqual(out()["player_choices_forced"],[])
 def test_18_invalid_justification_authority(self):
  r=req();r["justifications"][0]["authority_id"]="DEAN";r["authorities"][0]["scopes"]=["formal_discipline"];self.assertTrue(any(x["reason"]=="invalid_justification_authority" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_19_missing_evidence_unresolved(self):
  r=req();r["obligation_evidence"]=[x for x in r["obligation_evidence"] if x["obligation_id"]!="O5"];self.assertEqual(res(m.resolve(r),"O5")["resolution"],"missing_evidence")
 def test_20_unconfirmed_evidence_rejected(self):
  r=req();r["obligation_evidence"][1]["confirmed"]=False;self.assertTrue(any(x["reason"]=="missing_confirmed_provenance" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_21_late_beyond_tolerance_concern(self):
  r=req();next(x for x in r["obligation_evidence"] if x["obligation_id"]=="O5")["actual_start_minute"]=520;o=m.resolve(r);self.assertEqual(res(o,"O5")["resolution"],"late_breach")
 def test_22_institutional_conflict_no_fault(self):
  r=req();next(x for x in r["obligation_evidence"] if x["obligation_id"]=="O2")["reason_code"]="institutional_schedule_conflict";self.assertEqual(res(m.resolve(r),"O2")["resolution"],"no_fault_absence")
 def test_23_formal_measure_requires_review(self):
  r=req();r["disciplinary_decisions"][0]["obligation_id"]="O6";r["disciplinary_decisions"][0]["population_slot_ref"]="C1";self.assertTrue(any(x["reason"]=="no_formal_review_basis" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_24_formal_measure_requires_authority(self):
  r=req();r["disciplinary_decisions"][0]["authority_id"]="MEDICAL";self.assertTrue(any(x["reason"]=="invalid_discipline_authority" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_25_authority_severity_limit(self):
  r=req();r["disciplinary_decisions"][0]["measure_id"]="court_martial";self.assertTrue(any(x["reason"]=="authority_severity_exceeded" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_26_disproportionate_measure_rejected(self):
  r=req();r["authorities"][0]["max_measure_severity"]=5;r["disciplinary_decisions"][0]["measure_id"]="court_martial";self.assertTrue(any(x["reason"]=="measure_disproportionate_to_review_context" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_27_species_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["species_id"]="changed"
  self.assertEqual(m.resolve(r),m.resolve(x))
 def test_28_materialization_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["materialized"]=True
  x["player_present"]=True;x["player_location_ref"]="class";self.assertEqual(m.resolve(r),m.resolve(x))
 def test_29_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_30_duplicate_cadet_rejected(self):
  r=req();r["cadets"].append(copy.deepcopy(r["cadets"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_31_duplicate_obligation_rejected(self):
  r=req();r["obligations"].append(copy.deepcopy(r["obligations"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_32_invalid_interval_rejected(self):
  r=req();r["obligations"][0]["end_minute"]=r["obligations"][0]["start_minute"]
  with self.assertRaises(ValueError):m.resolve(r)
if __name__=="__main__":unittest.main()
