#!/usr/bin/env python3
import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"resolve_academy_npc_relationships_step11.py";FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"npc_relationships_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_npc_relationships_step11",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return mod.resolve(req())
def edge(o,a,b):return next(x for x in o["directional_edges"] if x["observer_population_slot_ref"]==a and x["subject_population_slot_ref"]==b)
class AcademyNpcRelationshipsStep11Tests(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_input_order_independent(self):
  r=req();x=copy.deepcopy(r);x["characters"]=list(reversed(x["characters"]));self.assertEqual(mod.resolve(r),mod.resolve(x))
 def test_03_player_not_mutated(self):self.assertFalse(out()["player_edges_mutated"]);self.assertFalse(any("PLAYER" in (x["observer_population_slot_ref"],x["subject_population_slot_ref"]) for x in out()["directional_edges"]))
 def test_04_first_meeting_familiarity(self):
  r=req();r["confirmed_events"]=r["confirmed_events"][:1];self.assertEqual(edge(mod.resolve(r),"A","B")["familiarity"],"recognized")
 def test_05_repeated_encounter_familiarity(self):
  r=req();r["confirmed_events"]=r["confirmed_events"][:2];self.assertEqual(edge(mod.resolve(r),"A","B")["familiarity"],"acquainted")
 def test_06_support_changes_trust_affinity(self):
  r=req();r["confirmed_events"]=r["confirmed_events"][:3];e=edge(mod.resolve(r),"A","B");self.assertEqual(e["personal_trust"],"positive");self.assertEqual(e["personal_affinity"],"positive")
 def test_07_friendship_requires_sustained_history(self):self.assertEqual(edge(out(),"A","B")["friendship_state"],"friend")
 def test_08_friendship_rejects_insufficient_history(self):
  r=req();r["confirmed_events"]=[{"event_id":"F","occurred_at":"1","event_type":"friendship_develops","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["x"],"positive_shared_history_refs":["x"]}];self.assertTrue(any(x["reason"]=="insufficient_friendship_history" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_09_successful_collaboration_only_respect(self):
  r=req();r["confirmed_events"]=[{"event_id":"P","occurred_at":"1","event_type":"successful_collaboration","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["p"]}];e=edge(mod.resolve(r),"A","B");self.assertEqual(e["professional_respect"],"positive");self.assertEqual(e["friendship_state"],"none")
 def test_10_conflict_directional(self):self.assertEqual(edge(out(),"C","B")["conflict_state"],"repairing");self.assertFalse(any(x["observer_population_slot_ref"]=="B" and x["subject_population_slot_ref"]=="C" for x in out()["directional_edges"]))
 def test_11_apology_preserves_conflict_history(self):self.assertIn("E08",edge(out(),"C","B")["shared_history_refs"]);self.assertIn("E09",edge(out(),"C","B")["shared_history_refs"])
 def test_12_reconciliation_partial_not_erase(self):
  r=req();r["confirmed_events"]=[{"event_id":"C1","occurred_at":"1","event_type":"conflict","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"severity":"major","cause_event_refs":["c"]},{"event_id":"R1","occurred_at":"2","event_type":"reconciliation_attempt","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"accepted":True,"cause_event_refs":["r"]}];e=edge(mod.resolve(r),"A","B");self.assertEqual(e["conflict_state"],"reconciled_unresolved_history");self.assertIn("C1",e["shared_history_refs"])
 def test_13_romantic_interest_directional(self):self.assertEqual(edge(out(),"A","B")["romantic_interest"],"present")
 def test_14_romantic_interest_not_automatically_reciprocal(self):
  r=req();r["confirmed_events"]=r["confirmed_events"][:5];o=mod.resolve(r);self.assertEqual(edge(o,"A","B")["romantic_interest"],"present");self.assertFalse(any(x["observer_population_slot_ref"]=="B" and x["subject_population_slot_ref"]=="A" for x in o["directional_edges"]))
 def test_15_same_sex_romance_rejected(self):
  r=req();r["confirmed_events"]=[{"event_id":"R","occurred_at":"1","event_type":"romantic_interest_emergence","actor_slot_ref":"B","target_slot_ref":"DUMMY","confirmed":True,"cause_event_refs":["r"]}];r["characters"].append({"population_slot_ref":"DUMMY","is_player":False,"adult_equivalent":True,"sex_category":"male","species_id":"human"});self.assertTrue(any(x["reason"]=="heterosexual_canon_ineligible" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_16_nonadult_romance_rejected(self):
  r=req();r["confirmed_events"]=[{"event_id":"R","occurred_at":"1","event_type":"romantic_interest_emergence","actor_slot_ref":"A","target_slot_ref":"D","confirmed":True,"cause_event_refs":["r"]}];self.assertTrue(any(x["reason"]=="adult_only" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_17_reciprocal_commitment_requires_both_interest(self):
  r=req();r["confirmed_events"]=[{"event_id":"I","occurred_at":"1","event_type":"romantic_interest_emergence","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["i"]},{"event_id":"K","occurred_at":"2","event_type":"reciprocal_commitment","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"bilateral_confirmed":True,"cause_event_refs":["k"]}];o=mod.resolve(r);self.assertTrue(any(x["reason"]=="commitment_not_reciprocal" for x in o["rejected_or_unresolved"]));self.assertFalse(any(x["observer_population_slot_ref"]=="B" and x["subject_population_slot_ref"]=="A" for x in o["directional_edges"]))
 def test_18_reciprocal_commitment_sets_both(self):self.assertEqual(edge(out(),"A","B")["relationship_state"],"dating");self.assertEqual(edge(out(),"B","A")["relationship_state"],"dating")
 def test_19_completed_date_not_auto_commitment(self):
  r=req();r["confirmed_events"]=[{"event_id":"I1","occurred_at":"1","event_type":"romantic_interest_emergence","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["i1"]},{"event_id":"D1","occurred_at":"2","event_type":"completed_date","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"bilateral_confirmed":True,"cause_event_refs":["d1"]}];self.assertEqual(edge(mod.resolve(r),"A","B")["relationship_state"],"none")
 def test_20_rejection_no_hostility(self):
  r=req();r["confirmed_events"]=[{"event_id":"I","occurred_at":"1","event_type":"romantic_interest_emergence","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["i"]},{"event_id":"X","occurred_at":"2","event_type":"romantic_expression","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["x"]},{"event_id":"Y","occurred_at":"3","event_type":"romantic_rejection","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["y"]}];e=edge(mod.resolve(r),"A","B");self.assertEqual(e["conflict_state"],"none");self.assertEqual(e["personal_affinity"],"neutral")
 def test_21_separation_preserves_history(self):
  r=req();r["existing_edges"]=[dict(mod.default_edge("A","B"),relationship_state="established",shared_history_refs=["old"])];r["confirmed_events"]=[{"event_id":"S","occurred_at":"1","event_type":"separation","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":["s"]}];e=edge(mod.resolve(r),"A","B");self.assertEqual(e["relationship_state"],"separated");self.assertIn("old",e["shared_history_refs"]);self.assertIn("S",e["shared_history_refs"])
 def test_22_species_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["characters"]:c["species_id"]="changed"
  self.assertEqual(mod.resolve(r),mod.resolve(x))
 def test_23_materialization_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["characters"]:c["character_id"]="materialized:"+c["population_slot_ref"]
  self.assertEqual(mod.resolve(r),mod.resolve(x))
 def test_24_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r);x["player_present"]=True;x["player_location_ref"]="academy";self.assertEqual(mod.resolve(r),mod.resolve(x))
 def test_25_missing_provenance_rejected(self):
  r=req();r["confirmed_events"]=[{"event_id":"Z","occurred_at":"1","event_type":"support_given","actor_slot_ref":"A","target_slot_ref":"B","confirmed":True,"cause_event_refs":[]}];self.assertTrue(any(x["reason"]=="missing_confirmed_provenance" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_26_player_event_rejected(self):
  r=req();r["confirmed_events"]=[{"event_id":"Z","occurred_at":"1","event_type":"support_given","actor_slot_ref":"A","target_slot_ref":"PLAYER","confirmed":True,"cause_event_refs":["z"]}];self.assertTrue(any(x["reason"]=="player_excluded_step_11" for x in mod.resolve(r)["rejected_or_unresolved"]))
 def test_27_no_mentor_changes(self):self.assertEqual(out()["future_step_state"]["mentor_changes"],[])
 def test_28_no_wellbeing_or_discipline(self):self.assertEqual(out()["future_step_state"]["wellbeing_effects"],[]);self.assertEqual(out()["future_step_state"]["disciplinary_consequences"],[])
 def test_29_future_steps_empty(self):self.assertTrue(all(v==[] for v in out()["future_step_state"].values()))
 def test_30_duplicate_identity_rejected(self):
  r=req();r["characters"].append(copy.deepcopy(r["characters"][1]))
  with self.assertRaises(ValueError):mod.resolve(r)
if __name__=="__main__":unittest.main()
