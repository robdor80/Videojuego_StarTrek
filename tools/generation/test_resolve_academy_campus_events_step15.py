import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"resolve_academy_campus_events_step15.py";FIXTURE=ROOT/"validation/fixtures/academy_life/campus_events_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("m",MODULE);m=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=m;spec.loader.exec_module(m)
def req():return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out():return m.resolve(req())
class AcademyCampusEventsStep15Tests(unittest.TestCase):
 def test_01_deterministic(self):self.assertEqual(out(),out())
 def test_02_three_event_records(self):self.assertEqual(len(out()["event_records"]),3)
 def test_03_scheduled_event_requires_authority(self):
  r=req();r["campus_events"][0]["authority_id"]="ACADEMY_ALERT";self.assertTrue(any(x["reason"]=="invalid_scheduling_authority" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_04_scheduled_event_requires_source(self):
  r=req();r["campus_events"][0]["source_ref"]=None;self.assertTrue(any(x["reason"]=="missing_scheduled_source" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_05_crisis_requires_cause(self):
  r=req();r["campus_events"][2]["cause_event_refs"]=[];self.assertTrue(any(x["reason"]=="missing_crisis_cause" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_06_crisis_requires_alert_authority(self):
  r=req();r["campus_events"][2]["authority_id"]="ACADEMY_ADMIN";self.assertTrue(any(x["reason"]=="invalid_alert_authority" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_07_location_capability_required(self):
  r=req();r["locations"][0]["capability_tags"]=[];self.assertTrue(any(x["reason"]=="location_capability_missing" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_08_external_participant_must_preexist(self):
  r=req();r["campus_events"][0]["external_participant_refs"]=["visitor:missing"];self.assertTrue(any(x["reason"]=="unknown_external_participant" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_09_mandatory_event_creates_obligations(self):self.assertEqual(sum(1 for x in out()["mandatory_obligation_candidates"] if x["campus_event_id"]=="EV-CER"),3)
 def test_10_mandatory_event_not_attendance(self):self.assertTrue(all(x["attendance_state"]=="unresolved" for x in out()["mandatory_obligation_candidates"]))
 def test_11_player_optional_not_auto_attending(self):self.assertEqual(out()["attendance_events"],[]);self.assertTrue(any(x["population_slot_ref"]=="PLAYER" and x["campus_event_id"]=="EV-COMP" for x in out()["player_optional_event_options"]))
 def test_12_npc_optional_can_plan(self):self.assertTrue(any(x["population_slot_ref"]=="C1" and x["campus_event_id"]=="EV-COMP" for x in out()["npc_optional_participation_plans"]))
 def test_13_optional_plan_not_attendance(self):self.assertTrue(all(x["attendance_state"]=="unresolved" for x in out()["npc_optional_participation_plans"]))
 def test_14_crisis_can_create_preemption_candidates(self):self.assertEqual(len(out()["schedule_revision_candidates"]),3)
 def test_15_crisis_preemption_candidate_not_applied(self):self.assertTrue(all(x["apply_state"]=="candidate_only" for x in out()["schedule_revision_candidates"]))
 def test_16_crisis_creates_institutional_exception_candidates(self):self.assertEqual(len(out()["institutional_exception_candidates"]),3)
 def test_17_no_preemption_without_authority_scope(self):
  r=req();r["authorities"][1]["scopes"]=["activate_campus_alert","cancel_campus_event"];o=m.resolve(r);self.assertEqual(o["schedule_revision_candidates"],[]);self.assertTrue(any(x["reason"]=="preemption_not_authorized" for x in o["schedule_conflict_candidates"]))
 def test_18_mandatory_capacity_insufficient_rejected(self):
  r=req();r["campus_events"][0]["capacity"]=2;self.assertTrue(any(x["reason"]=="mandatory_capacity_insufficient" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_19_cancelled_event_needs_provenance(self):
  r=req();r["campus_events"][0]["status"]="cancelled";self.assertTrue(any(x["reason"]=="missing_cancellation_provenance" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_20_cancelled_valid_event_creates_no_obligation(self):
  r=req();r["campus_events"][0]["status"]="cancelled";r["campus_events"][0]["cancellation_event_ref"]="cancel:1";o=m.resolve(r);self.assertFalse(any(x["campus_event_id"]=="EV-CER" for x in o["mandatory_obligation_candidates"]))
 def test_21_quiet_period_valid(self):
  r=req();r["campus_events"]=[];r["existing_participation_plans"]=[];o=m.resolve(r);self.assertEqual(o["event_records"],[]);self.assertEqual(o["generated_events_not_in_input"],[])
 def test_22_no_direct_relationship_mutation(self):self.assertEqual(out()["relationship_mutations"],[])
 def test_23_no_direct_wellbeing_mutation(self):self.assertEqual(out()["wellbeing_mutations"],[])
 def test_24_no_academic_record_write(self):self.assertEqual(out()["academic_record_writes"],[])
 def test_25_offscreen_deferred(self):self.assertEqual(out()["future_step_state"]["offscreen_execution"],[])
 def test_26_social_lod_deferred(self):self.assertEqual(out()["future_step_state"]["social_lod"],[])
 def test_27_year_progression_deferred(self):self.assertEqual(out()["future_step_state"]["year_progression"],[])
 def test_28_record_integration_deferred(self):self.assertEqual(out()["future_step_state"]["academy_record_integration"],[])
 def test_29_player_proximity_irrelevant(self):
  r=req();x=copy.deepcopy(r);x["player_present"]=True;x["player_location_ref"]="parade_grounds";self.assertEqual(m.resolve(r),m.resolve(x))
 def test_30_species_irrelevant(self):
  r=req();x=copy.deepcopy(r)
  for c in x["cadets"]:c["species_id"]="changed"
  self.assertEqual(m.resolve(r),m.resolve(x))
 def test_31_duplicate_cadet_rejected(self):
  r=req();r["cadets"].append(copy.deepcopy(r["cadets"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_32_duplicate_event_rejected(self):
  r=req();r["campus_events"].append(copy.deepcopy(r["campus_events"][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_33_invalid_interval_rejected(self):
  r=req();r["campus_events"][0]["end_minute"]=r["campus_events"][0]["start_minute"];self.assertTrue(any(x["reason"]=="invalid_event_interval" for x in m.resolve(r)["rejected_or_unresolved"]))
 def test_34_truth_semantics(self):self.assertEqual(out()["truth_semantics"],"event_exists_before_participation_and_participation_plan_is_not_attendance")
if __name__=="__main__":unittest.main()
