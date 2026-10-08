#!/usr/bin/env python3
import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"generate_academy_free_time_step6.py";FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"free_time_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_free_time_step6",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return mod.build_free_time(req())
class AcademyFreeTimeStep6Tests(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_input_order_independent(self):
  r=req();x=copy.deepcopy(r);x["cadets"]=list(reversed(x["cadets"]));x["free_time_windows"]=list(reversed(x["free_time_windows"]));self.assertEqual(mod.build_free_time(r),mod.build_free_time(x))
 def test_03_player_not_autoplayed(self):self.assertFalse(any(x["population_slot_ref"]=="cadet4:00" for x in out()["npc_free_time_plans"]));self.assertEqual(out()["accepted_player_choices"],[])
 def test_04_player_gets_options(self):self.assertTrue(any(x["population_slot_ref"]=="cadet4:00" for x in out()["player_feasible_options"]))
 def test_05_valid_player_choice_accepted(self):
  r=req();r["player_choice_requests"]=[{"population_slot_ref":"cadet4:00","window_ref":"W-P0","activity_id":"reading_recreation"}];self.assertEqual(len(mod.build_free_time(r)["accepted_player_choices"]),1)
 def test_06_invalid_player_choice_not_substituted(self):
  r=req();r["player_choice_requests"]=[{"population_slot_ref":"cadet4:00","window_ref":"W-P0","activity_id":"city_leave"}];o=mod.build_free_time(r);self.assertEqual(o["accepted_player_choices"],[]);self.assertTrue(o["unresolved_choices"])
 def test_07_npcs_choose_autonomously(self):self.assertEqual(len(out()["npc_free_time_plans"]),3)
 def test_08_affinity_guides_choice(self):
  p={x["population_slot_ref"]:x["activity_id"] for x in out()["npc_free_time_plans"]};self.assertEqual(p["cadet4:01"],"physical_exercise");self.assertEqual(p["cadet4:02"],"reading_recreation")
 def test_09_authorized_leave_required(self):
  p={x["population_slot_ref"]:x["activity_id"] for x in out()["npc_free_time_plans"]};self.assertEqual(p["cadet4:03"],"city_leave")
  r=req();r["authorized_leave_slot_refs"]=[];self.assertNotEqual({x["population_slot_ref"]:x["activity_id"] for x in mod.build_free_time(r)["npc_free_time_plans"]}.get("cadet4:03"),"city_leave")
 def test_10_facility_capability_required(self):
  r=req();r["locations"]=[x for x in r["locations"] if x["location_ref"]!="athletics_area"];p={x["population_slot_ref"]:x["activity_id"] for x in mod.build_free_time(r)["npc_free_time_plans"]};self.assertNotEqual(p.get("cadet4:01"),"physical_exercise")
 def test_11_travel_must_fit(self):
  r=req();r["travel_edges"]=[e for e in r["travel_edges"] if "athletics_area" not in (e["from"],e["to"])];p={x["population_slot_ref"]:x["activity_id"] for x in mod.build_free_time(r)["npc_free_time_plans"]};self.assertNotEqual(p.get("cadet4:01"),"physical_exercise")
 def test_12_species_not_selector(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["species_id"]="changed_species"
  self.assertEqual(mod.build_free_time(r),mod.build_free_time(x))
 def test_13_personality_not_raw_selector(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["personality_recipe_id"]="changed_personality"
  self.assertEqual(mod.build_free_time(r),mod.build_free_time(x))
 def test_14_player_presence_not_npc_bias(self):
  r=req();x=copy.deepcopy(r);x["player_present"]=True;x["player_current_location_ref"]="athletics_area";self.assertEqual(mod.build_free_time(r),mod.build_free_time(x))
 def test_15_no_relationship_effect(self):self.assertEqual(out()["automatic_relationship_effect"],"none");self.assertTrue(all(x["automatic_relationship_effect"]=="none" for x in out()["npc_free_time_plans"]))
 def test_16_plan_not_actual_execution(self):self.assertEqual(out()["plan_truth_semantics"],"intention_not_actual_execution");self.assertTrue(all(x["actual_execution"]=="unresolved" for x in out()["npc_free_time_plans"]))
 def test_17_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_18_bad_identity_or_window_rejected(self):
  r=req();r["cadets"].append(copy.deepcopy(r["cadets"][0]))
  with self.assertRaises(ValueError):mod.build_free_time(r)
  r=req();r["free_time_windows"][0]["end_minute"]=r["free_time_windows"][0]["start_minute"]
  with self.assertRaises(ValueError):mod.build_free_time(r)
if __name__=="__main__":unittest.main()
