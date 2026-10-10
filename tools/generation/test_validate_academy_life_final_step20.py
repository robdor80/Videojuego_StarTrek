import copy,importlib.util,json,unittest
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];M=H/"validate_academy_life_final_step20.py";F=R/"validation/fixtures/academy_life/final_closure_baseline_v1.0.json"
s=importlib.util.spec_from_file_location("m",M);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def req():return json.loads(F.read_text())["request"]
class T(unittest.TestCase):
 def test_01(self):self.assertTrue(m.validate(req())["academy_life_complete"])
 def test_02(self):self.assertEqual(m.validate(req())["incomplete_steps"],[])
 def test_03(self):self.assertTrue(m.validate(req())["population_conserved"])
 def test_04(self):self.assertTrue(m.validate(req())["player_agency_preserved"])
 def test_05(self):self.assertTrue(m.validate(req())["plan_execution_separated"])
 def test_06(self):self.assertTrue(m.validate(req())["lod_truth_preserved"])
 def test_07(self):self.assertTrue(m.validate(req())["record_append_only"])
 def test_08(self):self.assertTrue(m.validate(req())["progression_evidence_required"])
 def test_09(self):self.assertTrue(m.validate(req())["romance_canon_locked"])
 def test_10(self):self.assertTrue(m.validate(req())["graduation_assignment_not_fabricated"])
 def test_11(self):
  r=req();r["steps"][5]["status"]="TODO";self.assertFalse(m.validate(r)["academy_life_complete"])
 def test_12(self):
  r=req();r["population_slots"].append("C1")
  with self.assertRaises(ValueError):m.validate(r)
 def test_13(self):
  r=req();r["player_optional_choice_auto_selected"]=True
  with self.assertRaises(ValueError):m.validate(r)
 def test_14(self):
  r=req();r["plan_equals_execution"]=True
  with self.assertRaises(ValueError):m.validate(r)
 def test_15(self):
  r=req();r["lod_changes_truth"]=True
  with self.assertRaises(ValueError):m.validate(r)
 def test_16(self):
  r=req();r["record_mutable"]=True
  with self.assertRaises(ValueError):m.validate(r)
 def test_17(self):
  r=req();r["elapsed_time_grants_progression"]=True
  with self.assertRaises(ValueError):m.validate(r)
 def test_18(self):
  r=req();r["romance_canon"]="other"
  with self.assertRaises(ValueError):m.validate(r)
 def test_19(self):
  r=req();r["graduation_directly_assigns_posting"]=True
  with self.assertRaises(ValueError):m.validate(r)
 def test_20(self):self.assertIn("Living Interplanetary",m.validate(req())["next_work_item"])
if __name__=="__main__":unittest.main()
