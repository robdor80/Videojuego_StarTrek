import copy,importlib.util,json,unittest
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];M=H/"integrate_academy_record_step19.py";F=R/"validation/fixtures/academy_life/record_integration_baseline_v0.1.json"
s=importlib.util.spec_from_file_location("m",M);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def req():return json.loads(F.read_text())["request"]
def out():return m.resolve(req())
class T(unittest.TestCase):
 def test_01(self):self.assertEqual(out(),out())
 def test_02(self):self.assertEqual(len(out()["appended_record_events"]),3)
 def test_03(self):self.assertFalse(any(x["source_event_id"]=="admit:1" for x in out()["appended_record_events"]))
 def test_04(self):self.assertTrue(any(x["event_type"]=="academic_evaluation" for x in out()["appended_record_events"]))
 def test_05(self):self.assertTrue(any(x["event_type"]=="academy_specialization" for x in out()["appended_record_events"]))
 def test_06(self):self.assertTrue(any(x["event_type"]=="academy_graduation" for x in out()["appended_record_events"]))
 def test_07(self):self.assertEqual(len(out()["academy_completion_unlock_candidates"]),1)
 def test_08(self):self.assertEqual(out()["fabricated_first_assignments"],[])
 def test_09(self):self.assertEqual(out()["fabricated_commissions"],[])
 def test_10(self):self.assertEqual(out()["modified_existing_events"],[])
 def test_11(self):self.assertEqual(out()["deleted_existing_events"],[])
 def test_12(self):
  r=req();r["evidence_events"].append(copy.deepcopy(r["evidence_events"][1]));self.assertEqual(len(m.resolve(r)["appended_record_events"]),3)
 def test_13(self):
  r=req();r["is_player"]=False;self.assertEqual(m.resolve(r)["academy_completion_unlock_candidates"],[])
 def test_14(self):
  r=req();r["evidence_events"][1]["confirmed"]=False;self.assertFalse(any(x["source_event_id"]=="eval:1" for x in m.resolve(r)["appended_record_events"]))
 def test_15(self):
  r=req();r["evidence_events"].append({"family":"discipline","source_event_id":"disc:1","confirmed":True});self.assertTrue(any(x["event_type"]=="disciplinary_action" for x in m.resolve(r)["appended_record_events"]))
 def test_16(self):
  r=req();r["evidence_events"].append({"family":"year_progression","source_event_id":"yr:1","confirmed":True});self.assertTrue(any(x["event_type"]=="academy_year_progression" for x in m.resolve(r)["appended_record_events"]))
 def test_17(self):
  r=req();r["evidence_events"].append({"family":"commission","source_event_id":"com:1","confirmed":True});self.assertTrue(any(x["event_type"]=="commission" for x in m.resolve(r)["appended_record_events"]))
 def test_18(self):
  r=req();r["evidence_events"].append({"family":"remediation","source_event_id":"rem:1","confirmed":True});self.assertTrue(any(x["event_type"]=="academy_remediation" for x in m.resolve(r)["appended_record_events"]))
 def test_19(self):
  r=req();r["evidence_events"].append({"family":"leave","source_event_id":"leave:1","confirmed":True});self.assertTrue(any(x["event_type"]=="leave_of_absence" for x in m.resolve(r)["appended_record_events"]))
 def test_20(self):
  r=req();r["evidence_events"].append({"family":"dismissal","source_event_id":"dis:1","confirmed":True});self.assertTrue(any(x["event_type"]=="academy_dismissal" for x in m.resolve(r)["appended_record_events"]))
 def test_21(self):
  r=req();r["evidence_events"].append({"family":"evaluation","source_event_id":"corr:1","confirmed":True,"correction_of":"old-eval"});self.assertEqual(next(x for x in m.resolve(r)["appended_record_events"] if x["source_event_id"]=="corr:1")["supersedes_event_id_if_correction"],"old-eval")
 def test_22(self):self.assertTrue(len(out()["service_record_bridge_candidates"])>=1)
 def test_23(self):self.assertEqual(out()["future_step_state"]["final_closure"],[])
 def test_24(self):self.assertEqual(out()["truth_semantics"],"official_record_is_append_only_provenance_backed_and_idempotent")
 def test_25(self):
  r=req();r["elapsed_time_years"]=100;self.assertEqual(m.resolve(r),out())
 def test_26(self):
  r=req();r["ai_summary"]="graduated with honors";self.assertEqual(m.resolve(r),out())
 def test_27(self):self.assertEqual(out()["academy_completion_unlock_candidates"][0]["specialization_if_any"],"sensors")
 def test_28(self):self.assertEqual(out()["academy_completion_unlock_candidates"][0]["player_profile_ref"],"profile:1")
if __name__=="__main__":unittest.main()
