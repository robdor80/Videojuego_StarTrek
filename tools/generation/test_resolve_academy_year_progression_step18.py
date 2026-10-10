import copy,importlib.util,json,unittest
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];M=H/"resolve_academy_year_progression_step18.py";F=R/"validation/fixtures/academy_life/year_progression_baseline_v0.1.json"
s=importlib.util.spec_from_file_location("m",M);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def req():return json.loads(F.read_text())["request"]
class T(unittest.TestCase):
 def test_01(self):self.assertEqual(m.resolve(req()),m.resolve(req()))
 def test_02(self):self.assertEqual(m.resolve(req())["outcome"],"advance")
 def test_03(self):self.assertIn("specialization_selection",m.resolve(req())["required_transition_actions"])
 def test_04(self):self.assertEqual(m.resolve(req())["activation_state"],"pending_required_transition_action")
 def test_05(self):
  r=req();r["specialization_selection"]={"id":"sensors","explicit_player_choice":True};self.assertEqual(m.resolve(r)["activation_state"],"resolved")
 def test_06(self):
  r=req();r["academic_year"]=1;self.assertEqual(m.resolve(r)["next_class"],"cadet_third_class")
 def test_07(self):
  r=req();r["academic_year"]=3;self.assertEqual(m.resolve(r)["next_class"],"cadet_first_class")
 def test_08(self):
  r=req();r["academic_year"]=4;self.assertEqual(m.resolve(r)["outcome"],"graduation_pending")
 def test_09(self):
  r=req();r["academic_year"]=4;self.assertIsNone(m.resolve(r)["direct_rank_award"])
 def test_10(self):
  r=req();r["evidence"]["period_complete"]=False;self.assertEqual(m.resolve(r)["outcome"],"pending")
 def test_11(self):
  r=req();r["evidence"]["remediation_open"]=1;self.assertEqual(m.resolve(r)["outcome"],"advance_with_remediation")
 def test_12(self):
  r=req();r["policy"]["allow_advance_with_remediation"]=False;r["evidence"]["remediation_open"]=1;self.assertEqual(m.resolve(r)["outcome"],"repeat_selected_modules")
 def test_13(self):
  r=req();r["evidence"]["failed_required_modules"]=2;self.assertEqual(m.resolve(r)["outcome"],"repeat_selected_modules")
 def test_14(self):
  r=req();r["evidence"]["failed_required_modules"]=3;self.assertEqual(m.resolve(r)["outcome"],"repeat_academic_year")
 def test_15(self):
  r=req();r["authorized_leave_ref"]="leave:1";self.assertEqual(m.resolve(r)["outcome"],"leave_of_absence")
 def test_16(self):
  r=req();r["authorized_dismissal_ref"]="dismiss:1";self.assertEqual(m.resolve(r)["outcome"],"dismissal")
 def test_17(self):
  r=req();r["evidence"]["conduct_status"]="blocks_progression";self.assertEqual(m.resolve(r)["outcome"],"repeat_academic_year")
 def test_18(self):self.assertTrue(m.resolve(req())["identity_preserved"])
 def test_19(self):self.assertTrue(m.resolve(req())["history_preserved"])
 def test_20(self):self.assertEqual(m.resolve(req())["record_write"],"deferred_step_19")
 def test_21(self):self.assertEqual(m.resolve(req())["future_step_state"]["record_integration"],[])
 def test_22(self):self.assertEqual(m.resolve(req())["truth_semantics"],"progression_requires_evidence_not_elapsed_time")
 def test_23(self):
  r=req();r["elapsed_time_years"]=99;self.assertEqual(m.resolve(r)["outcome"],"advance")
 def test_24(self):
  r=req();r["academic_year"]=0
  with self.assertRaises(ValueError):m.resolve(r)
 def test_25(self):
  r=req();r["is_player"]=False;r["specialization_selection"]={"id":"engineering"};self.assertEqual(m.resolve(r)["activation_state"],"resolved")
 def test_26(self):
  r=req();r["specialization_selection"]={"id":"science","explicit_player_choice":False};self.assertIn("explicit_player_specialization_choice",m.resolve(r)["required_transition_actions"])
 def test_27(self):
  r=req();r["academic_year"]=4;self.assertEqual(m.resolve(r)["next_academy_status"],"graduation_pending")
 def test_28(self):
  r=req();r["academic_year"]=4;self.assertIsNone(m.resolve(r)["direct_commission_award"])
if __name__=="__main__":unittest.main()
