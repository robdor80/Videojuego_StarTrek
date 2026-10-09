import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/'resolve_academy_mentors_instructors_step12.py';FIXTURE=ROOT/'validation/fixtures/academy_life/mentors_instructors_baseline_v0.1.json'
spec=importlib.util.spec_from_file_location('m',MODULE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def req():return json.loads(FIXTURE.read_text())['request']
def out():return m.resolve(req())
class T(unittest.TestCase):
 def test_01(self):self.assertEqual(out(),out())
 def test_02(self):self.assertTrue(all(x['assignment_state']=='active' for x in out()['teaching_assignments']))
 def test_03(self):self.assertFalse(any(x['mentee_population_slot_ref']=='PLAYER' for x in out()['mentorships']))
 def test_04(self):self.assertTrue(any(x['mentee_population_slot_ref']=='C1' for x in out()['mentorships']))
 def test_05(self):self.assertTrue(any(x['mentee_population_slot_ref']=='C2' for x in out()['mentorships']))
 def test_06(self):self.assertTrue(any(x['reason']=='awaiting_explicit_player_response' for x in out()['rejected_or_unresolved']))
 def test_07(self):
  r=req();r['player_mentorship_responses']=[{'mentor_instructor_id':'INST-SCI','cadet_slot_ref':'PLAYER','response':'accept'}];self.assertTrue(any(x['mentee_population_slot_ref']=='PLAYER' for x in m.resolve(r)['mentorships']))
 def test_08(self):
  r=req();r['player_mentorship_responses']=[{'mentor_instructor_id':'INST-SCI','cadet_slot_ref':'PLAYER','response':'decline'}];self.assertTrue(m.resolve(r)['declined'])
 def test_09(self):
  r=req();r['mentorship_proposals'][1]['cause_event_refs']=[];self.assertTrue(any(x['reason']=='missing_provenance' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_10(self):
  r=req();r['mentorship_proposals'][1]['professional_scope']='science';self.assertTrue(any(x['reason']=='mentor_scope_invalid' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_11(self):
  r=req();r['instructors'][1]['mentee_capacity']=0;self.assertTrue(any(x['reason']=='mentor_capacity_full' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_12(self):self.assertFalse(out()['tutoring_sessions'][0]['creates_mentorship'])
 def test_13(self):
  r=req();r['tutoring_requests'][0]['subject_id']='OPS-301';self.assertTrue(any(x['reason']=='subject_or_instructor_invalid' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_14(self):
  r=req();r['available_windows']=[x for x in r['available_windows'] if x['window_ref']!='P-W'];self.assertTrue(any(x['reason']=='missing_window' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_15(self):
  r=req();r['travel_edges']=[];self.assertTrue(any(x['reason']=='travel_unavailable' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_16(self):
  r=req();r['locations'][0]['capability_tags']=[];self.assertTrue(any(x['reason']=='location_capability_missing' for x in m.resolve(r)['rejected_or_unresolved']))
 def test_17(self):self.assertEqual(len(out()['mentoring_sessions']),1)
 def test_18(self):self.assertEqual(len(out()['recommendation_candidates']),1)
 def test_19(self):self.assertFalse(out()['recommendation_candidates'][0]['guarantees_assignment'])
 def test_20(self):self.assertEqual(out()['automatic_grade_awards'],[])
 def test_21(self):self.assertEqual(out()['automatic_qualification_awards'],[])
 def test_22(self):self.assertEqual(out()['automatic_discipline_actions'],[])
 def test_23(self):self.assertTrue(all(x['friendship_effect']=='none' for x in out()['mentorships']))
 def test_24(self):self.assertEqual(out()['truth_semantics'],'instruction_tutoring_mentorship_recommendation_are_distinct')
 def test_25(self):self.assertTrue(all(v==[] for v in out()['future_step_state'].values()))
 def test_26(self):
  r=req();r['cadets'].append(copy.deepcopy(r['cadets'][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_27(self):
  r=req();r['instructors'].append(copy.deepcopy(r['instructors'][0]))
  with self.assertRaises(ValueError):m.resolve(r)
 def test_28(self):
  r=req();x=copy.deepcopy(r)
  for c in x['cadets']:c['species_id']='changed';c['character_id']='mat:'+c['population_slot_ref']
  x['player_present']=True;self.assertEqual(m.resolve(r),m.resolve(x))
if __name__=='__main__':unittest.main()
