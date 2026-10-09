import copy, importlib.util, json, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"resolve_academy_wellbeing_step13.py";FIXTURE=ROOT/"validation/fixtures/academy_life/wellbeing_balance_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("m",MODULE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def req():return json.loads(FIXTURE.read_text())["request"]
def out():return m.resolve(req())
def char(o,c):return next(x for x in o["character_wellbeing"] if x["character_id"]==c)
class T(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_player_balanced(self):self.assertEqual(char(out(),"PLAYER")["derived_state"]["balance_state"],"balanced")
 def test_03_good_balance_no_superhuman_bonus(self):self.assertFalse(char(out(),"PLAYER")["derived_state"]["superhuman_bonus"])
 def test_04_balanced_assistance_normal_not_boosted(self):self.assertEqual(char(out(),"PLAYER")["derived_state"]["character_side_assistance_band"],"normal")
 def test_05_one_bad_night_limited_longitudinal_effect(self):self.assertNotEqual(char(out(),"NPC-A")["derived_state"]["balance_state"],"severely_imbalanced")
 def test_06_sustained_overload_detected(self):self.assertIn(char(out(),"NPC-B")["derived_state"]["balance_state"],{"imbalanced","severely_imbalanced"})
 def test_07_sustained_overload_reduces_assistance(self):self.assertIn(char(out(),"NPC-B")["derived_state"]["character_side_assistance_band"],{"reduced","severely_reduced"})
 def test_08_actual_events_only(self):
  r=req();r["planned_activities"]=[{"character_id":"NPC-B","activity_family":"sleep","duration_minutes":9999}];self.assertEqual(m.resolve(r),m.resolve(req()))
 def test_09_unconfirmed_ignored_and_reported(self):
  r=req();r["confirmed_activity_events"].append({"event_id":"X","character_id":"PLAYER","activity_family":"sleep","end_hour":719,"duration_minutes":600,"confirmed":False,"cause_event_refs":[]});o=m.resolve(r);self.assertTrue(any(x["event_id"]=="X" for x in o["rejected_or_unresolved"]))
 def test_10_missing_provenance_ignored(self):
  r=req();r["confirmed_activity_events"].append({"event_id":"Y","character_id":"PLAYER","activity_family":"sleep","end_hour":719,"duration_minutes":600,"confirmed":True,"cause_event_refs":[]});self.assertTrue(any(x["reason"]=="missing_confirmed_provenance" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_11_preference_changes_recovery_weight(self):
  r=req();x=copy.deepcopy(r);x["characters"][0]["wellbeing_profile"]["preferred_recovery_activity_families"]=[];self.assertLess(char(m.resolve(x),"PLAYER")["window_metrics"]["weekly"]["preferred_weighted_recovery_minutes"],char(m.resolve(r),"PLAYER")["window_metrics"]["weekly"]["preferred_weighted_recovery_minutes"])
 def test_12_species_id_alone_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["characters"]:c["species_id"]="changed"
  self.assertEqual(m.resolve(r),m.resolve(x))
 def test_13_individual_sleep_profile_matters(self):
  r=req();x=copy.deepcopy(r);x["characters"][1]["wellbeing_profile"]["sleep_target_minutes_per_24h"]=600;self.assertNotEqual(char(m.resolve(r),"NPC-A")["derived_state"]["sleep_weekly"],char(m.resolve(x),"NPC-A")["derived_state"]["sleep_weekly"])
 def test_14_24h_window_exists(self):self.assertIn("acute",char(out(),"PLAYER")["window_metrics"])
 def test_15_7d_window_exists(self):self.assertIn("weekly",char(out(),"PLAYER")["window_metrics"])
 def test_16_30d_window_exists(self):self.assertIn("monthly",char(out(),"PLAYER")["window_metrics"])
 def test_17_routine_from_repetition(self):self.assertTrue(any(x["character_id"]=="PLAYER" and x["activity_or_pattern"]=="exercise" for x in out()["routine_observation_candidates"]))
 def test_18_no_routine_from_one_action(self):self.assertFalse(any(x["character_id"]=="NPC-A" and x["activity_or_pattern"]=="quiet_rest" for x in out()["routine_observation_candidates"]))
 def test_19_no_formal_consequences(self):self.assertEqual(out()["formal_academic_or_disciplinary_consequences"],[])
 def test_20_player_choices_not_forced(self):self.assertEqual(char(out(),"PLAYER")["forced_player_choices"],[])
 def test_21_world_truth_not_mutated(self):self.assertEqual(char(out(),"PLAYER")["world_truth_mutations"],[])
 def test_22_character_side_only(self):self.assertIn("character_side_assistance_band",char(out(),"PLAYER")["derived_state"])
 def test_23_future_step_14_empty(self):self.assertEqual(out()["future_step_state"]["obligations_and_consequences"],[])
 def test_24_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_25_unknown_character_event_rejected(self):
  r=req();r["confirmed_activity_events"].append({"event_id":"U","character_id":"NOPE","activity_family":"sleep","end_hour":719,"duration_minutes":60,"confirmed":True,"cause_event_refs":["u"]});self.assertTrue(any(x["reason"]=="unknown_character" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_26_negative_duration_rejected(self):
  r=req();r["confirmed_activity_events"][0]["duration_minutes"]=-1
  with self.assertRaises(ValueError):m.resolve(r)
 def test_27_duplicate_character_rejected(self):
  r=req();r["characters"].append(copy.deepcopy(r["characters"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_28_materialization_or_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["characters"]:c["materialized"]=True
  x["player_present"]=True;x["player_location_ref"]="gym";self.assertEqual(m.resolve(r),m.resolve(x))
 def test_29_social_activity_not_universal_bonus(self):
  r=req();r["confirmed_activity_events"].append({"event_id":"SOC","character_id":"PLAYER","activity_family":"social_leisure","end_hour":719,"duration_minutes":120,"confirmed":True,"cause_event_refs":["soc"],"stress_weight":0});o=m.resolve(r);self.assertFalse(char(o,"PLAYER")["derived_state"]["superhuman_bonus"])
 def test_30_truth_semantics(self):self.assertEqual(out()["truth_semantics"],"actual_confirmed_behavior_drives_wellbeing_not_plans")
if __name__=="__main__":unittest.main()
