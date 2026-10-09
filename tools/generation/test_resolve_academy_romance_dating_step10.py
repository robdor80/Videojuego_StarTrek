#!/usr/bin/env python3
import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"resolve_academy_romance_dating_step10.py";FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"romance_dating_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_romance_dating_step10",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return mod.resolve(req())
class AcademyRomanceDatingStep10Tests(unittest.TestCase):
 def test_01_npc_interest_can_create_invitation(self):self.assertTrue(any(x["initiator_slot_ref"]=="cadet4:A" for x in out()["invitations"]))
 def test_02_player_never_auto_accepts(self):self.assertTrue(any(x["state"]=="awaiting_player_response" for x in out()["invitations"]));self.assertEqual(out()["date_plans"],[])
 def test_03_player_interest_never_inferred(self):self.assertFalse(out()["player_romantic_interest_inferred"])
 def test_04_locked_heterosexual_canon(self):self.assertEqual(out()["canon"]["romantic_orientation_policy"],"heterosexual_only")
 def test_05_adult_only_canon(self):self.assertTrue(out()["canon"]["adult_only"])
 def test_06_same_sex_player_invite_rejected(self):
  r=req();r["player_romantic_actions"]=[{"action_type":"invite","npc_slot_ref":"cadet4:B","proposal_id":"DATE-B1","npc_response":"accept"}];self.assertTrue(any(x["reason"]=="heterosexual_canon_ineligible" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_07_non_adult_player_invite_rejected(self):
  r=req();r["player_romantic_actions"]=[{"action_type":"invite","npc_slot_ref":"cadet4:C","proposal_id":"DATE-C1","npc_response":"accept"}];self.assertTrue(any(x["reason"]=="adult_only" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_08_missing_sex_unresolved(self):
  r=req();r["characters"][1].pop("sex_category");o=mod.resolve(r);self.assertTrue(any(x["reason"]=="sex_category_unresolved" for x in o["rejected_or_unresolved"]))
 def test_09_npc_interest_requires_provenance(self):
  r=req();r["npc_romantic_interest_edges"][0]["cause_event_refs"]=[];self.assertTrue(any(x["reason"]=="no_authoritative_npc_interest" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_10_npc_interest_required_for_player_invite_acceptance(self):
  r=req();r["npc_romantic_interest_edges"]=[];r["npc_initiation_requests"]=[];r["player_romantic_actions"]=[{"action_type":"invite","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1","npc_response":"accept"}];o=mod.resolve(r);self.assertTrue(o["declined"]);self.assertEqual(o["date_plans"],[])
 def test_11_player_can_accept_npc_invitation(self):
  r=req();r["player_romantic_actions"]=[{"action_type":"accept_npc_invitation","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1"}];o=mod.resolve(r);self.assertEqual(len(o["date_plans"]),1)
 def test_12_player_can_decline_without_hostility(self):
  r=req();r["player_romantic_actions"]=[{"action_type":"decline_npc_invitation","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1"}];o=mod.resolve(r);self.assertTrue(o["declined"]);self.assertEqual(o["automatic_hostility_from_rejection"],"none")
 def test_13_player_invite_can_be_accepted(self):
  r=req();r["npc_initiation_requests"]=[];r["player_romantic_actions"]=[{"action_type":"invite","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1","npc_response":"accept"}];self.assertEqual(len(mod.resolve(r)["date_plans"]),1)
 def test_14_player_invite_can_be_declined_without_hostility(self):
  r=req();r["npc_initiation_requests"]=[];r["player_romantic_actions"]=[{"action_type":"invite","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1","npc_response":"decline"}];o=mod.resolve(r);self.assertTrue(o["declined"]);self.assertEqual(o["automatic_hostility_from_rejection"],"none")
 def test_15_venue_capability_required(self):
  r=req();r["venues"][0]["capability_tags"]=[];r["player_romantic_actions"]=[{"action_type":"accept_npc_invitation","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1"}];self.assertTrue(any(x["reason"]=="venue_unavailable" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_16_both_schedules_required(self):
  r=req();r["available_windows"]=[x for x in r["available_windows"] if x["window_ref"]!="A-W1"];r["player_romantic_actions"]=[{"action_type":"accept_npc_invitation","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1"}];self.assertTrue(any(x["reason"]=="missing_window" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_17_travel_required(self):
  r=req();r["travel_edges"]=[];r["player_romantic_actions"]=[{"action_type":"accept_npc_invitation","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1"}];self.assertTrue(any(x["reason"]=="travel_unavailable" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_18_existing_date_conflict_blocks_new(self):
  r=req();r["existing_date_plans"]=[{"date_plan_id":"date:old","participant_slot_refs":["cadet4:PLAYER","cadet4:A"],"day_index":5,"start_minute":1130,"end_minute":1240,"venue_ref":"campus_garden","plan_state":"scheduled","attendance_state":"unresolved","completion_state":"unresolved"}];r["player_romantic_actions"]=[{"action_type":"accept_npc_invitation","npc_slot_ref":"cadet4:A","proposal_id":"DATE-A1"}];self.assertTrue(any(x["reason"]=="date_plan_conflict" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_19_plan_not_attendance_completion_commitment(self):self.assertEqual(out()["dating_truth_semantics"],"invitation_not_acceptance_not_attendance_not_completion_not_commitment")
 def test_20_completed_date_only_transition_candidate(self):
  r=req();r["romantic_completion_evidence"]=[{"evidence_type":"completed_date","bilateral_confirmed":True,"participant_slot_refs":["cadet4:PLAYER","cadet4:A"],"event_ref":"date_event:1"}];o=mod.resolve(r);self.assertEqual(o["relationship_transition_candidates"][0]["candidate"],"romantic_history_advance");self.assertFalse(o["relationship_transition_candidates"][0]["automatic_commitment"])
 def test_21_reciprocal_commitment_candidate(self):
  r=req();r["romantic_completion_evidence"]=[{"evidence_type":"reciprocal_commitment","bilateral_confirmed":True,"participant_slot_refs":["cadet4:PLAYER","cadet4:A"],"event_ref":"commitment:1"}];self.assertEqual(mod.resolve(r)["relationship_transition_candidates"][0]["candidate"],"relationship_state_dating_or_established")
 def test_22_species_irrelevant_to_eligibility(self):
  r=req();x=copy.deepcopy(r);x["characters"][1]["species_id"]="changed_species";self.assertEqual(mod.resolve(r),mod.resolve(x))
 def test_23_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r);x["player_present"]=True;x["player_location_ref"]="campus_garden";self.assertEqual(mod.resolve(r),mod.resolve(x))
 def test_24_no_npc_to_npc_evolution(self):self.assertEqual(out()["future_step_state"]["npc_to_npc_relationship_evolution"],[])
 def test_25_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_26_invalid_player_count_or_duplicate_rejected(self):
  r=req();r["characters"].append(copy.deepcopy(r["characters"][0]))
  with self.assertRaises(ValueError):mod.resolve(r)
  r=req();r["characters"][1]["population_slot_ref"]="cadet4:PLAYER"
  with self.assertRaises(ValueError):mod.resolve(r)
if __name__=="__main__":unittest.main()
