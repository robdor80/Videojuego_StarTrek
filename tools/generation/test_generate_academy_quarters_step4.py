#!/usr/bin/env python3
import copy, importlib.util, json, sys, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MODULE=HERE/"generate_academy_quarters_step4.py"
FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"quarters_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_quarters_step4",MODULE)
mod=importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

def request():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]

class AcademyQuartersStep4Tests(unittest.TestCase):
    def test_deterministic(self):
        r=request(); self.assertEqual(mod.assign_quarters(r),mod.assign_quarters(r))
    def test_input_order_independent(self):
        r=request(); x=copy.deepcopy(r); x["cadets"]=list(reversed(x["cadets"])); self.assertEqual(mod.assign_quarters(r),mod.assign_quarters(x))
    def test_each_assigned_slot_occurs_once(self):
        out=mod.assign_quarters(request()); occupied=[s for room in out["rooms"] for s in room["occupant_slot_refs"]]; self.assertEqual(len(occupied),len(set(occupied)))
    def test_room_capacity_respected(self):
        out=mod.assign_quarters(request()); self.assertTrue(all(len(room["occupant_slot_refs"])<=room["capacity"] for room in out["rooms"]))
    def test_accessibility_requirement(self):
        self.assertEqual(mod.assign_quarters(request())["room_assignments"]["cadet4:08"],"Q-ACC01")
    def test_single_occupancy_requirement(self):
        out=mod.assign_quarters(request()); self.assertEqual(out["room_assignments"]["cadet4:09"],"Q-MED01"); self.assertEqual(out["roommate_slot_refs"]["cadet4:09"],[])
    def test_no_compatible_capacity_remains_unresolved(self):
        out=mod.assign_quarters(request()); self.assertEqual(out["unresolved_housing_needs"][0]["population_slot_ref"],"cadet4:10")
    def test_roommate_has_no_automatic_relationship_effect(self):
        self.assertEqual(mod.assign_quarters(request())["automatic_relationship_effect"],"none")
    def test_future_steps_remain_empty(self):
        future=mod.assign_quarters(request())["future_step_state"]; self.assertEqual(future["personal_schedules"],[]); self.assertEqual(future["social_relationship_changes"],[]); self.assertEqual(future["romance_state"],[])
    def test_materialization_does_not_change_assignment(self):
        r=request(); x=copy.deepcopy(r)
        for cadet in x["cadets"]: cadet["character_id"]="materialized:"+cadet["population_slot_ref"]
        self.assertEqual(mod.assign_quarters(r)["room_assignments"],mod.assign_quarters(x)["room_assignments"])
    def test_species_does_not_change_assignment(self):
        r=request(); x=copy.deepcopy(r)
        for cadet in x["cadets"]: cadet["species_id"]="changed_species"
        self.assertEqual(mod.assign_quarters(r)["room_assignments"],mod.assign_quarters(x)["room_assignments"])
    def test_personality_does_not_change_assignment(self):
        r=request(); x=copy.deepcopy(r)
        for cadet in x["cadets"]: cadet["personality_recipe_id"]="changed_personality"
        self.assertEqual(mod.assign_quarters(r)["room_assignments"],mod.assign_quarters(x)["room_assignments"])
    def test_duplicate_cadet_slot_rejected(self):
        x=request(); x["cadets"].append(copy.deepcopy(x["cadets"][0]))
        with self.assertRaises(ValueError): mod.assign_quarters(x)
    def test_duplicate_room_rejected(self):
        x=request(); x["rooms"].append(copy.deepcopy(x["rooms"][0]))
        with self.assertRaises(ValueError): mod.assign_quarters(x)
    def test_valid_existing_assignment_persists(self):
        r=request(); first=mod.assign_quarters(r); x=copy.deepcopy(r)
        for room in x["rooms"]:
            prior=next(prior for prior in first["rooms"] if prior["room_id"]==room["room_id"])
            room["occupant_slot_refs"]=list(prior["occupant_slot_refs"])
        self.assertEqual(first["room_assignments"],mod.assign_quarters(x)["room_assignments"])
    def test_roommate_symmetry(self):
        out=mod.assign_quarters(request())
        for a,others in out["roommate_slot_refs"].items():
            for b in others: self.assertIn(a,out["roommate_slot_refs"][b])

if __name__=="__main__":
    unittest.main()
