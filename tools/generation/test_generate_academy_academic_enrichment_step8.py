#!/usr/bin/env python3
import copy, importlib.util, json, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MODULE=HERE/"generate_academy_academic_enrichment_step8.py"
FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"academic_enrichment_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_academic_enrichment_step8",MODULE)
mod=importlib.util.module_from_spec(spec); assert spec and spec.loader
sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
def req(): return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out(): return mod.build_registrations(req())
class AcademyAcademicEnrichmentStep8Tests(unittest.TestCase):
 def test_01_deterministic(self): self.assertEqual(out(),out())
 def test_02_input_order_independent(self):
  r=req(); x=copy.deepcopy(r); x["cadets"]=list(reversed(x["cadets"])); x["available_windows"]=list(reversed(x["available_windows"])); self.assertEqual(mod.build_registrations(r),mod.build_registrations(x))
 def test_03_existing_registration_preserved(self): self.assertIn("cadet4:03",out()["rosters"]["temporal_mechanics_optional_course"])
 def test_04_capacity_blocks_player_option_state(self):
  self.assertTrue(any(x["population_slot_ref"]=="cadet4:00" and x["offering_id"]=="temporal_mechanics_optional_course" and x["state"]=="waitlist_only" for x in out()["player_eligible_options"]))
 def test_05_player_not_auto_registered(self): self.assertFalse(any(x["population_slot_ref"]=="cadet4:00" for x in out()["registrations"]))
 def test_06_npc_affinity_registration(self):
  m={x["population_slot_ref"]:x["offering_id"] for x in out()["registrations"] if x["source"]=="npc_autonomous"}; self.assertEqual(m["cadet4:01"],"first_contact_guest_conference"); self.assertEqual(m["cadet4:02"],"advanced_warp_workshop")
 def test_07_full_player_request_waitlisted(self):
  r=req(); r["player_registration_requests"]=[{"population_slot_ref":"cadet4:00","offering_id":"temporal_mechanics_optional_course"}]; o=mod.build_registrations(r); self.assertTrue(any(x["population_slot_ref"]=="cadet4:00" and x["offering_id"]=="temporal_mechanics_optional_course" for x in o["waitlist"]))
 def test_08_valid_player_request_registered(self):
  r=req(); r["offerings"]["temporal_mechanics_optional_course"]["capacity"]=2; r["player_registration_requests"]=[{"population_slot_ref":"cadet4:00","offering_id":"temporal_mechanics_optional_course"}]; o=mod.build_registrations(r); self.assertTrue(any(x["population_slot_ref"]=="cadet4:00" and x["source"]=="explicit_player_choice" for x in o["registrations"]))
 def test_09_unknown_player_request_rejected(self):
  r=req(); r["player_registration_requests"]=[{"population_slot_ref":"cadet4:00","offering_id":"missing"}]; self.assertTrue(any(x["reason"]=="unknown_offering" for x in mod.build_registrations(r)["rejected_or_unresolved"]))
 def test_10_presenter_required(self):
  r=req(); r["offerings"]["first_contact_guest_conference"]["presenter_ref"]=None; o=mod.build_registrations(r); self.assertNotIn("cadet4:01",o["rosters"]["first_contact_guest_conference"])
 def test_11_presenter_schedule_required(self):
  r=req(); r["offerings"]["advanced_warp_workshop"]["presenter_available_session_ids"]=["WW-1"]; o=mod.build_registrations(r); self.assertNotIn("cadet4:02",o["rosters"]["advanced_warp_workshop"])
 def test_12_facility_required(self):
  r=req(); r["locations"]=[x for x in r["locations"] if x["location_ref"]!="command_school"]; o=mod.build_registrations(r); self.assertNotIn("cadet4:01",o["rosters"]["first_contact_guest_conference"])
 def test_13_all_sessions_must_fit(self):
  r=req(); r["available_windows"]=[x for x in r["available_windows"] if x["window_ref"]!="W2B"]; o=mod.build_registrations(r); self.assertNotIn("cadet4:02",o["rosters"]["advanced_warp_workshop"])
 def test_14_travel_required(self):
  r=req(); r["travel_edges"]=[e for e in r["travel_edges"] if "command_school" not in (e["from"],e["to"])]; o=mod.build_registrations(r); self.assertNotIn("cadet4:01",o["rosters"]["first_contact_guest_conference"])
 def test_15_species_not_selector(self):
  r=req(); x=copy.deepcopy(r)
  for c in x["cadets"]: c["species_id"]="changed_species"
  self.assertEqual(mod.build_registrations(r),mod.build_registrations(x))
 def test_16_player_proximity_irrelevant(self):
  r=req(); x=copy.deepcopy(r); x["player_present"]=True; x["player_location_ref"]="command_school"; self.assertEqual(mod.build_registrations(r),mod.build_registrations(x))
 def test_17_registration_not_completion(self):
  o=out(); self.assertEqual(o["registration_truth_semantics"],"registration_not_attendance_or_completion"); self.assertTrue(all(x["attendance_state"]=="unresolved" and x["completion_state"]=="not_evaluated" for x in o["registrations"]))
 def test_18_record_write_deferred(self): self.assertEqual(out()["completion_record_effect"],"deferred_step_19"); self.assertTrue(all(x["academic_record_effect"]=="deferred_step_19" for x in out()["registrations"]))
 def test_19_no_relationship_or_skill_reward(self): self.assertEqual(out()["automatic_relationship_effect"],"none"); self.assertEqual(out()["automatic_skill_grade_reputation_wellbeing_effect"],"none")
 def test_20_schedule_entries_created(self): self.assertTrue(out()["schedule_entries"]); self.assertTrue(all(x["attendance_state"]=="unresolved" for x in out()["schedule_entries"]))
 def test_21_future_steps_empty(self): self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_22_invalid_identity_type_or_capacity_rejected(self):
  r=req(); r["cadets"].append(copy.deepcopy(r["cadets"][0]))
  with self.assertRaises(ValueError): mod.build_registrations(r)
  r=req(); r["offerings"]["first_contact_guest_conference"]["offering_type"]="invalid"
  with self.assertRaises(ValueError): mod.build_registrations(r)
  r=req(); r["offerings"]["first_contact_guest_conference"]["capacity"]=-1
  with self.assertRaises(ValueError): mod.build_registrations(r)
if __name__=="__main__": unittest.main()
