import copy,importlib.util,json,sys,unittest
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];M=H/"resolve_academy_offscreen_step16.py";F=R/"validation/fixtures/academy_life/offscreen_baseline_v0.1.json"
s=importlib.util.spec_from_file_location("m",M);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def req():return json.loads(F.read_text())["request"]
def out():return m.resolve(req())
class T(unittest.TestCase):
 def test_01(self):self.assertEqual(out(),out())
 def test_02(self):self.assertIn("E1",out()["executed_event_refs"])
 def test_03(self):self.assertNotIn("E4",out()["executed_event_refs"])
 def test_04(self):self.assertTrue(any(x["event_id"]=="E2" for x in out()["unresolved_player_choices"]))
 def test_05(self):self.assertTrue(any(x["event_id"]=="E3" for x in out()["explicit_consequential_events"]))
 def test_06(self):self.assertTrue(any(x["activity_family"]=="class" for x in out()["routine_aggregates"]))
 def test_07(self):self.assertEqual(out()["generated_events_not_in_input"],[])
 def test_08(self):self.assertEqual(out()["relationship_transitions_from_elapsed_time"],[])
 def test_09(self):self.assertEqual(out()["career_progression_from_elapsed_time"],[])
 def test_10(self):self.assertEqual(out()["checkpoint"]["to_time"],200)
 def test_11(self):
  r=req();r["scheduled_candidates"][0]["preconditions_satisfied"]=False;self.assertNotIn("E1",m.resolve(r)["executed_event_refs"])
 def test_12(self):
  r=req();r["scheduled_candidates"][0]["source_ref"]=None;self.assertNotIn("E1",m.resolve(r)["executed_event_refs"])
 def test_13(self):
  r=req();r["scheduled_candidates"][1]["explicit_player_authorization"]=True;self.assertIn("E2",m.resolve(r)["executed_event_refs"])
 def test_14(self):
  r=req();x=copy.deepcopy(r);x["population"][1]["materialized"]=True;self.assertEqual(m.resolve(r),m.resolve(x))
 def test_15(self):
  r=req();x=copy.deepcopy(r);x["player_location_ref"]="elsewhere";self.assertEqual(m.resolve(r),m.resolve(x))
 def test_16(self):
  r=req();r["scheduled_candidates"].append({"event_id":"E0","population_slot_ref":"N1","time":105,"activity_family":"class","duration_minutes":10,"preconditions_satisfied":True,"source_ref":"x"});self.assertEqual(m.resolve(r)["executed_event_refs"][0],"E0")
 def test_17(self):
  r=req();r["to_time"]=99
  with self.assertRaises(ValueError):m.resolve(r)
 def test_18(self):
  r=req();r["population"].append(copy.deepcopy(r["population"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_19(self):
  r=req();r["scheduled_candidates"][0]["population_slot_ref"]="NOPE"
  with self.assertRaises(ValueError):m.resolve(r)
 def test_20(self):self.assertEqual(out()["future_step_state"]["social_lod"],[])
 def test_21(self):self.assertEqual(out()["future_step_state"]["year_progression"],[])
 def test_22(self):self.assertEqual(out()["future_step_state"]["record_integration"],[])
 def test_23(self):self.assertEqual(out()["truth_semantics"],"offscreen_executes_authoritative_candidates_not_story_invention")
 def test_24(self):self.assertTrue(all(x["confirmed"] for x in out()["downstream_evidence_candidates"]))
if __name__=="__main__":unittest.main()
