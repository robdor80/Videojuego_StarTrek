#!/usr/bin/env python3
import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"generate_academy_extracurricular_step7.py";FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"extracurricular_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_extracurricular_step7",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return mod.build_memberships(req())
class AcademyExtracurricularStep7Tests(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_input_order_independent(self):
  r=req();x=copy.deepcopy(r);x["cadets"]=list(reversed(x["cadets"]));x["free_time_windows"]=list(reversed(x["free_time_windows"]));self.assertEqual(mod.build_memberships(r),mod.build_memberships(x))
 def test_03_existing_membership_preserved(self):self.assertIn("cadet4:03",out()["rosters"]["strategy_games_society"])
 def test_04_capacity_preserved_before_new(self):self.assertEqual(out()["rosters"]["strategy_games_society"],["cadet4:03"])
 def test_05_player_not_auto_enrolled(self):self.assertFalse(any(m["population_slot_ref"]=="cadet4:00" for m in out()["memberships"]))
 def test_06_npc_affinity_enrollment(self):
  r={m["population_slot_ref"]:m["extracurricular_id"] for m in out()["memberships"] if m["source"]=="npc_autonomous"};self.assertEqual(r["cadet4:01"],"academy_fitness_team");self.assertEqual(r["cadet4:02"],"engineering_project_club")
 def test_07_full_activity_not_player_option(self):self.assertFalse(any(x["extracurricular_id"]=="strategy_games_society" for x in out()["player_eligible_options"]))
 def test_08_valid_player_choice(self):
  r=req();r["activities"]["strategy_games_society"]["capacity"]=2;r["player_join_requests"]=[{"population_slot_ref":"cadet4:00","extracurricular_id":"strategy_games_society"}];o=mod.build_memberships(r);self.assertTrue(any(m["population_slot_ref"]=="cadet4:00" and m["source"]=="explicit_player_choice" for m in o["memberships"]))
 def test_09_invalid_player_choice_not_substituted(self):
  r=req();r["player_join_requests"]=[{"population_slot_ref":"cadet4:00","extracurricular_id":"strategy_games_society"}];o=mod.build_memberships(r);self.assertFalse(any(m["population_slot_ref"]=="cadet4:00" for m in o["memberships"]));self.assertTrue(any(x["reason"]=="capacity_full" for x in o["rejected_or_unresolved"]))
 def test_10_facility_required(self):
  r=req();r["locations"]=[x for x in r["locations"] if x["location_ref"]!="athletics_area"];o=mod.build_memberships(r);self.assertNotIn("cadet4:01",o["rosters"]["academy_fitness_team"])
 def test_11_schedule_feasible_required(self):
  r=req();r["free_time_windows"]=[x for x in r["free_time_windows"] if x["population_slot_ref"]!="cadet4:02"];o=mod.build_memberships(r);self.assertNotIn("cadet4:02",o["rosters"]["engineering_project_club"])
 def test_12_travel_required(self):
  r=req();r["travel_edges"]=[e for e in r["travel_edges"] if "athletics_area" not in (e["from"],e["to"])];o=mod.build_memberships(r);self.assertNotIn("cadet4:01",o["rosters"]["academy_fitness_team"])
 def test_13_species_not_selector(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["species_id"]="changed_species"
  self.assertEqual(mod.build_memberships(r),mod.build_memberships(x))
 def test_14_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r);x["player_present"]=True;x["player_location_ref"]="athletics_area";self.assertEqual(mod.build_memberships(r),mod.build_memberships(x))
 def test_15_recurring_schedule_created(self):self.assertTrue(out()["recurring_schedule_entries"])
 def test_16_membership_not_attendance(self):self.assertEqual(out()["membership_truth_semantics"],"membership_not_attendance");self.assertTrue(all(e["actual_attendance"]=="unresolved" for e in out()["recurring_schedule_entries"]))
 def test_17_no_relationship_effect(self):self.assertEqual(out()["automatic_relationship_effect"],"none");self.assertTrue(all(m["automatic_relationship_effect"]=="none" for m in out()["memberships"]))
 def test_18_no_skill_grade_reward(self):self.assertEqual(out()["automatic_skill_grade_reputation_wellbeing_effect"],"none");self.assertTrue(all(m["automatic_skill_or_grade_effect"]=="none" for m in out()["memberships"]))
 def test_19_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_20_invalid_identity_or_capacity_rejected(self):
  r=req();r["cadets"].append(copy.deepcopy(r["cadets"][0]))
  with self.assertRaises(ValueError):mod.build_memberships(r)
  r=req();r["activities"]["strategy_games_society"]["capacity"]=0
  with self.assertRaises(ValueError):mod.build_memberships(r)
if __name__=="__main__":unittest.main()
