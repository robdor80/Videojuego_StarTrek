#!/usr/bin/env python3
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULE = HERE / "generate_academy_cadet_step2.py"
FIXTURE = ROOT / "validation" / "fixtures" / "academy_life" / "cadet_generation_baseline_v0.1.json"

spec = importlib.util.spec_from_file_location("academy_cadet_step2", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

def fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))

class AcademyCadetStep2Tests(unittest.TestCase):
    def test_locked_fixture_and_determinism(self):
        f = fixture()
        a = mod.generate_cadet(f["request"])
        b = mod.generate_cadet(f["request"])
        self.assertEqual(a, b)
        for key in ("character_id", "display_name", "species_id", "specialization", "personality_recipe_id"):
            self.assertEqual(a[key], f["expected"][key])

    def test_different_slot_produces_different_identity(self):
        f = fixture()["request"]
        other = copy.deepcopy(f)
        other["population_slot_ref"] = "cadet_4:latent:0038"
        self.assertNotEqual(mod.generate_cadet(f)["character_id"], mod.generate_cadet(other)["character_id"])

    def test_species_does_not_select_personality(self):
        f = fixture()["request"]
        human, vulcan = copy.deepcopy(f), copy.deepcopy(f)
        human["species_pool"] = [{"species_id": "human", "weight": 1}]
        vulcan["species_pool"] = [{"species_id": "vulcan", "weight": 1}]
        a, b = mod.generate_cadet(human), mod.generate_cadet(vulcan)
        self.assertEqual(a["personality_seed"], b["personality_seed"])
        self.assertEqual(a["personality_recipe_id"], b["personality_recipe_id"])

    def test_name_not_derived_from_species(self):
        f = fixture()["request"]
        human, vulcan = copy.deepcopy(f), copy.deepcopy(f)
        human["species_pool"] = [{"species_id": "human", "weight": 1}]
        vulcan["species_pool"] = [{"species_id": "vulcan", "weight": 1}]
        self.assertEqual(mod.generate_cadet(human)["display_name"], mod.generate_cadet(vulcan)["display_name"])

    def test_fourth_and_third_class_do_not_lock_specialization(self):
        f = fixture()["request"]
        for cadet_class in ("cadet_fourth_class", "cadet_third_class"):
            request = copy.deepcopy(f)
            request["cadet_class_id"] = cadet_class
            self.assertIsNone(mod.generate_cadet(request)["specialization"])

    def test_second_and_first_class_have_specialization_state(self):
        f = fixture()["request"]
        for cadet_class in ("cadet_second_class", "cadet_first_class"):
            request = copy.deepcopy(f)
            request["cadet_class_id"] = cadet_class
            self.assertIn(mod.generate_cadet(request)["specialization"], [b["branch_id"] for b in request["branch_pool"]])

    def test_future_steps_remain_unresolved(self):
        cadet = mod.generate_cadet(fixture()["request"])
        self.assertEqual(cadet["academy_relationship_refs"], [])
        self.assertEqual(cadet["class_group_refs"], [])
        self.assertIsNone(cadet["roommate_ref"])
        self.assertIsNone(cadet["schedule_state_ref"])

    def test_exact_age_not_invented_without_profile(self):
        cadet = mod.generate_cadet(fixture()["request"])
        self.assertTrue(cadet["adult_equivalent_status"])
        self.assertIsNone(cadet["exact_age_or_birth_date"])

    def test_reserved_name_is_filtered(self):
        request = copy.deepcopy(fixture()["request"])
        request["social_origin_context_pool"] = [{
            "context_id": "test",
            "origin_ref": "test",
            "culture_refs": [],
            "citizenship_refs": [],
            "name_candidates": ["Selar", "Safe Name"],
            "weight": 1
        }]
        self.assertEqual(mod.generate_cadet(request)["display_name"], "Safe Name")

    def test_materialization_conserves_population(self):
        registry = {"groups": [{
            "group_id": "cadet_4", "category": "cadet", "total_count": 100,
            "latent_count": 100, "materialized_character_ids": []
        }]}
        cadet = mod.generate_cadet(fixture()["request"])
        output = mod.materialize_into_registry(registry, cadet)
        self.assertEqual(output["groups"][0]["total_count"], 100)
        self.assertEqual(output["groups"][0]["latent_count"], 99)

    def test_same_slot_cannot_materialize_twice(self):
        registry = {"groups": [{
            "group_id": "cadet_4", "category": "cadet", "total_count": 100,
            "latent_count": 100, "materialized_character_ids": []
        }]}
        cadet = mod.generate_cadet(fixture()["request"])
        output = mod.materialize_into_registry(registry, cadet)
        with self.assertRaises(ValueError):
            mod.materialize_into_registry(output, cadet)

    def test_non_cadet_slot_rejected(self):
        request = copy.deepcopy(fixture()["request"])
        request["population_category"] = "visitor"
        with self.assertRaises(ValueError):
            mod.generate_cadet(request)

if __name__ == "__main__":
    unittest.main()
