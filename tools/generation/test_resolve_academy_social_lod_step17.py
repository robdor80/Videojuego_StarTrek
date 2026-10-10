import copy,importlib.util,json,unittest
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];M=H/"resolve_academy_social_lod_step17.py";F=R/"validation/fixtures/academy_life/social_lod_baseline_v0.1.json"
s=importlib.util.spec_from_file_location("m",M);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def req():return json.loads(F.read_text())["request"]
def out():return m.resolve(req())
def row(o,s):return next(x for x in o["lod_states"] if x["population_slot_ref"]==s)
class T(unittest.TestCase):
 def test_01(self):self.assertEqual(out(),out())
 def test_02(self):self.assertEqual(row(out(),"A1")["lod"],"A")
 def test_03(self):self.assertEqual(row(out(),"B1")["lod"],"B")
 def test_04(self):self.assertEqual(row(out(),"C1")["lod"],"C")
 def test_05(self):self.assertEqual(row(out(),"D1")["lod"],"B")
 def test_06(self):self.assertEqual(row(out(),"A1")["history_refs"],["h1"])
 def test_07(self):self.assertFalse(row(out(),"A1")["truth_changed"])
 def test_08(self):self.assertEqual(out()["fabricated_major_events"],[])
 def test_09(self):self.assertEqual(out()["erased_history_refs"],[])
 def test_10(self):
  r=req();x=copy.deepcopy(r);x["people"][2]["player_nearby"]=True;self.assertEqual(m.resolve(r),m.resolve(x))
 def test_11(self):
  r=req();r["people"][2]["known_persistent_identity"]=True;self.assertEqual(row(m.resolve(r),"C1")["lod"],"B")
 def test_12(self):
  r=req();r["people"][2]["mentor_or_mentee"]=True;self.assertEqual(row(m.resolve(r),"C1")["lod"],"B")
 def test_13(self):
  r=req();r["people"][2]["mentor_or_mentee"]=True;r["people"][2]["close_relationship"]=True;self.assertEqual(row(m.resolve(r),"C1")["lod"],"A")
 def test_14(self):self.assertTrue(all(x["effect"]=="simulation_detail_only" for x in out()["transitions"]))
 def test_15(self):self.assertEqual(out()["future_step_state"]["year_progression"],[])
 def test_16(self):self.assertEqual(out()["future_step_state"]["record_integration"],[])
 def test_17(self):
  r=req();r["people"].append(copy.deepcopy(r["people"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_18(self):self.assertEqual(out()["truth_semantics"],"lod_changes_detail_not_identity_or_history")
 def test_19(self):
  r=req();r["people"][1]["materialized"]=True;self.assertEqual(row(m.resolve(r),"B1")["lod"],"B")
 def test_20(self):
  r=req();r["people"][1]["species_id"]="changed";self.assertEqual(m.resolve(r),m.resolve(req()))
 def test_21(self):
  r=req();r["people"][2]["consequential_shared_history"]=True;self.assertEqual(row(m.resolve(r),"C1")["lod"],"B")
 def test_22(self):
  r=req();r["people"][2]["recurring_shared_activity"]=True;self.assertEqual(row(m.resolve(r),"C1")["lod"],"B")
 def test_23(self):self.assertEqual(row(out(),"D1")["identity_ref"],"npc:D1")
 def test_24(self):self.assertEqual(row(out(),"D1")["history_refs"],["h3"])
if __name__=="__main__":unittest.main()
