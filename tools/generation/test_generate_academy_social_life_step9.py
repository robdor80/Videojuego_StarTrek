#!/usr/bin/env python3
import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"generate_academy_social_life_step9.py";FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"social_life_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_social_life_step9",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return mod.build_social_plans(req())
class AcademySocialLifeStep9Tests(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_input_order_independent(self):
  r=req();x=copy.deepcopy(r);x["cadets"]=list(reversed(x["cadets"]));x["available_windows"]=list(reversed(x["available_windows"]));self.assertEqual(mod.build_social_plans(r),mod.build_social_plans(x))
 def test_03_existing_plan_preserved(self):self.assertIn("cadet4:03",out()["rosters"]["evening_shared_meal"])
 def test_04_player_not_auto_socialized(self):self.assertFalse(any(x["population_slot_ref"]=="cadet4:00" for x in out()["social_plans"]))
 def test_05_player_has_feasible_options(self):self.assertTrue(any(x["population_slot_ref"]=="cadet4:00" for x in out()["player_options"]))
 def test_06_player_acceptance(self):
  r=req();r["player_rsvp_responses"]=[{"population_slot_ref":"cadet4:00","social_opportunity_id":"quiet_common_time","response":"accept"}];self.assertTrue(any(x["population_slot_ref"]=="cadet4:00" and x["source"]=="explicit_player_acceptance" for x in mod.build_social_plans(r)["social_plans"]))
 def test_07_player_decline(self):
  r=req();r["player_rsvp_responses"]=[{"population_slot_ref":"cadet4:00","social_opportunity_id":"quiet_common_time","response":"decline"}];o=mod.build_social_plans(r);self.assertTrue(o["declined"]);self.assertFalse(any(x["population_slot_ref"]=="cadet4:00" for x in o["social_plans"]))
 def test_08_invitation_required(self):
  r=req();r["social_opportunities"]["strategy_small_group"]["invited_slot_refs"]=["cadet4:00"];o=mod.build_social_plans(r);self.assertNotIn("cadet4:02",o["rosters"]["strategy_small_group"])
 def test_09_circle_context_required(self):
  r=req();r["social_circles"][0]["member_slot_refs"]=["cadet4:00","cadet4:03"];o=mod.build_social_plans(r);self.assertNotIn("cadet4:01",o["rosters"]["quiet_common_time"])
 def test_10_npc_preference_guides_plan(self):
  p={x["population_slot_ref"]:x["social_opportunity_id"] for x in out()["social_plans"] if x["source"]=="npc_autonomous"};self.assertEqual(p["cadet4:01"],"quiet_common_time");self.assertEqual(p["cadet4:02"],"strategy_small_group")
 def test_11_capacity_respected(self):self.assertLessEqual(len(out()["rosters"]["evening_shared_meal"]),2)
 def test_12_full_event_rejects_player(self):
  r=req();r["social_opportunities"]["evening_shared_meal"]["capacity"]=1;r["player_rsvp_responses"]=[{"population_slot_ref":"cadet4:00","social_opportunity_id":"evening_shared_meal","response":"accept"}];self.assertTrue(any(x["reason"]=="capacity_full" for x in mod.build_social_plans(r)["rejected_or_unresolved"]))
 def test_13_facility_required(self):
  r=req();r["locations"]=[x for x in r["locations"] if x["location_ref"]!="library_study"];o=mod.build_social_plans(r);self.assertNotIn("cadet4:01",o["rosters"]["quiet_common_time"])
 def test_14_travel_required(self):
  r=req();r["travel_edges"]=[e for e in r["travel_edges"] if "simulation_complex" not in (e["from"],e["to"])];o=mod.build_social_plans(r);self.assertNotIn("cadet4:02",o["rosters"]["strategy_small_group"])
 def test_15_schedule_window_required(self):
  r=req();r["available_windows"]=[x for x in r["available_windows"] if x["population_slot_ref"]!="cadet4:01"];o=mod.build_social_plans(r);self.assertNotIn("cadet4:01",o["rosters"]["quiet_common_time"])
 def test_16_species_not_nonromantic_selector(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["species_id"]="changed_species"
  self.assertEqual(mod.build_social_plans(r),mod.build_social_plans(x))
 def test_17_sex_not_nonromantic_selector(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["sex_category"]="changed"
  self.assertEqual(mod.build_social_plans(r),mod.build_social_plans(x))
 def test_18_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r);x["player_present"]=True;x["player_location_ref"]="library_study";self.assertEqual(mod.build_social_plans(r),mod.build_social_plans(x))
 def test_19_plan_not_attendance_interaction_relationship(self):
  o=out();self.assertEqual(o["social_truth_semantics"],"plan_not_attendance_not_interaction_not_relationship");self.assertTrue(all(x["attendance_state"]=="unresolved" and x["interaction_state"]=="unresolved" for x in o["social_plans"]))
 def test_20_no_relationship_mutation(self):self.assertEqual(out()["relationship_mutations"],[]);self.assertEqual(out()["interaction_evidence_candidates"],[])
 def test_21_no_romance_or_sex_step9(self):self.assertEqual(out()["romantic_or_sexual_events"],[])
 def test_22_romantic_event_family_rejected(self):
  r=req();r["social_opportunities"]["quiet_common_time"]["event_family"]="romantic_date"
  with self.assertRaises(ValueError):mod.build_social_plans(r)
 def test_23_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_24_invalid_identity_access_or_capacity_rejected(self):
  r=req();r["cadets"].append(copy.deepcopy(r["cadets"][0]))
  with self.assertRaises(ValueError):mod.build_social_plans(r)
  r=req();r["social_opportunities"]["quiet_common_time"]["access_mode"]="bad"
  with self.assertRaises(ValueError):mod.build_social_plans(r)
  r=req();r["social_opportunities"]["quiet_common_time"]["capacity"]=-1
  with self.assertRaises(ValueError):mod.build_social_plans(r)
if __name__=="__main__":unittest.main()
