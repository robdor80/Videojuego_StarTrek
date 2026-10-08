#!/usr/bin/env python3
import copy,importlib.util,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MODULE=HERE/"generate_academy_groups_step3.py";FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"grouping_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_groups_step3",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def fixture():return json.loads(FIXTURE.read_text(encoding="utf-8"))
class T(unittest.TestCase):
 def test_deterministic(self):r=fixture()["request"];self.assertEqual(mod.generate_groups(r),mod.generate_groups(r))
 def test_order(self):r=fixture()["request"];x=copy.deepcopy(r);x["roster"]=list(reversed(x["roster"]));self.assertEqual(mod.generate_groups(r),mod.generate_groups(x))
 def test_one_section(self):
  f=fixture();r=mod.generate_groups(f["request"]);c={m["population_slot_ref"]:0 for m in f["request"]["roster"]}
  for s in r["class_sections"]:
   for x in s["member_slot_refs"]:c[x]+=1
  self.assertTrue(all(v==1 for v in c.values()))
 def test_class_purity(self):
  f=fixture();r=mod.generate_groups(f["request"]);b={m["population_slot_ref"]:m for m in f["request"]["roster"]}
  self.assertTrue(all(all(b[x]["cadet_class_id"]==s["cadet_class_id"] for x in s["member_slot_refs"]) for s in r["class_sections"]))
 def test_capacity(self):
  f=fixture();r=mod.generate_groups(f["request"]);self.assertTrue(all(len(s["member_slot_refs"])<=f["request"]["class_section_capacity"] for s in r["class_sections"]))
 def test_study_parent(self):
  f=fixture();r=mod.generate_groups(f["request"]);s={x["group_id"]:set(x["member_slot_refs"]) for x in r["class_sections"]};self.assertTrue(all(set(g["member_slot_refs"]).issubset(s[g["parent_section_ref"]]) for g in r["study_groups"]))
 def test_no_relationship(self):
  r=mod.generate_groups(fixture()["request"]);self.assertTrue(all(g["automatic_relationship_effect"]=="none" for k in ("class_sections","study_groups","practical_teams") for g in r[k]));self.assertEqual(r["future_step_state"]["social_relationship_changes"],[])
 def test_course(self):
  f=fixture();r=mod.generate_groups(f["request"]);b={m["population_slot_ref"]:m for m in f["request"]["roster"]};self.assertTrue(all(all(t["course_id"] in b[x]["course_ids"] for x in t["member_slot_refs"]) for t in r["practical_teams"]))
 def test_aligned(self):t=[x for x in mod.generate_groups(fixture()["request"])["practical_teams"] if x["course_id"]=="PRA-201"];self.assertTrue(t and all(len(x["branch_labels"])==1 for x in t))
 def test_cross(self):t=[x for x in mod.generate_groups(fixture()["request"])["practical_teams"] if x["course_id"]=="INT-CROSS"];self.assertTrue(t and all(len(x["branch_labels"])>=2 for x in t))
 def test_latent(self):
  f=fixture();self.assertTrue(any(m.get("character_id") is None for m in f["request"]["roster"]));r=mod.generate_groups(f["request"]);g={x for s in r["class_sections"] for x in s["member_slot_refs"]};self.assertTrue(all(m["population_slot_ref"] in g for m in f["request"]["roster"]))
 def test_materialization_preserves(self):
  f=fixture();slot="cadet_3:slot:08";before=mod.memberships_for_slot(mod.generate_groups(f["request"]),slot);x=copy.deepcopy(f["request"])
  for m in x["roster"]:
   if m["population_slot_ref"]==slot:m["character_id"]="cadet:newly:materialized"
  self.assertEqual(before,mod.memberships_for_slot(mod.generate_groups(x),slot))
 def test_species_irrelevant(self):
  r=fixture()["request"];x=copy.deepcopy(r)
  for m in x["roster"]:m["species_id"]="test_species"
  self.assertEqual(mod.generate_groups(r),mod.generate_groups(x))
 def test_player_irrelevant(self):r=fixture()["request"];x=copy.deepcopy(r);x["player_present"]=True;x["player_slot_ref"]="cadet_3:slot:00";self.assertEqual(mod.generate_groups(r),mod.generate_groups(x))
 def test_future_empty(self):r=mod.generate_groups(fixture()["request"]);self.assertEqual(r["future_step_state"]["roommate_assignments"],[]);self.assertEqual(r["future_step_state"]["personal_schedules"],[]);self.assertEqual(r["future_step_state"]["romance_state"],[])
if __name__=="__main__":unittest.main()
