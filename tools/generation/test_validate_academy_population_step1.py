#!/usr/bin/env python3
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULE = HERE / "validate_academy_population_step1.py"
FIXTURE = ROOT / "validation" / "fixtures" / "academy_life" / "population_baseline_v0.1.json"

spec = importlib.util.spec_from_file_location("academy_population", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

def registry():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))

class AcademyPopulationStep1Tests(unittest.TestCase):
    def test_fixture_valid(self):
        self.assertEqual(mod.validate_registry(registry()), [])

    def test_materialization_conserves_total(self):
        r = registry()
        before = sum(g["total_count"] for g in r["groups"])
        out = mod.materialize_latent_slot(r, "cadet_4", "cadet:c")
        after = sum(g["total_count"] for g in out["groups"])
        self.assertEqual(before, after)
        self.assertEqual(out["groups"][0]["latent_count"], 97)

    def test_duplicate_materialized_identity_rejected(self):
        r = registry()
        with self.assertRaises(ValueError):
            mod.materialize_latent_slot(r, "cadet_4", "cadet:a")

    def test_accounting_mismatch_detected(self):
        r = registry()
        r["groups"][0]["latent_count"] += 1
        self.assertTrue(any(e.startswith("population_accounting_mismatch") for e in mod.validate_registry(r)))

    def test_noncadet_cannot_have_cadet_class(self):
        r = registry()
        r["groups"][4]["cadet_class_id"] = "cadet_fourth_class"
        self.assertTrue(any(e.startswith("noncadet_has_cadet_class") for e in mod.validate_registry(r)))

    def test_temporary_absence_does_not_change_membership(self):
        r = registry()
        group = r["groups"][1]
        self.assertGreater(group["temporarily_absent_count"], 0)
        self.assertEqual(group["total_count"], 100)

    def test_admission_changes_membership_explicitly(self):
        out = mod.apply_membership_event(registry(), {"type":"admit_latent","group_id":"cadet_4","count":3})
        self.assertEqual(out["groups"][0]["total_count"], 103)
        self.assertEqual(out["groups"][0]["latent_count"], 101)

    def test_materialized_departure_changes_membership(self):
        out = mod.apply_membership_event(registry(), {"type":"depart_materialized","group_id":"cadet_4","character_id":"cadet:a"})
        self.assertEqual(out["groups"][0]["total_count"], 99)
        self.assertNotIn("cadet:a", out["groups"][0]["materialized_character_ids"])

    def test_character_cannot_belong_to_two_groups(self):
        r = registry()
        r["groups"][1]["materialized_character_ids"] = ["cadet:a"]
        r["groups"][1]["latent_count"] = 99
        self.assertTrue(any(e.startswith("duplicate_character_membership") for e in mod.validate_registry(r)))

    def test_fixture_cadet_total(self):
        r = registry()
        self.assertEqual(sum(g["total_count"] for g in r["groups"] if g["category"] == "cadet"), 400)

if __name__ == "__main__":
    unittest.main()
