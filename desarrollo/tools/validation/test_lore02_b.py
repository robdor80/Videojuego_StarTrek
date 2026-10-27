#!/usr/bin/env python3
"""Regression and mutation tests for the documentary LORE-02 B gate."""
import copy
import unittest
from validate_lore02_b import CAT, PROFILES, CASES, REGISTRY, read, validate, validate_data

class Lore02BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = (read(CAT), read(PROFILES), read(CASES), read(REGISTRY))

    def mutate(self, fn):
        cat, prof, cases, registry = copy.deepcopy(self.base)
        fn(cat, prof, cases, registry)
        return validate_data(cat, prof, cases, registry, check_paths=False)

    def test_complete_positive_gate(self):
        self.assertEqual(validate()["equipment"], 73)

    def test_all_records_have_unique_ids(self):
        cat = self.base[0]
        self.assertEqual(len({x["equipment_id"] for x in cat["records"]}), 73)

    def test_role_distribution_covers_all_families(self):
        self.assertEqual(len({r["family"] for r in self.base[0]["records"]}), 7)

    def test_duplicate_equipment_rejected(self):
        self.assertTrue(any("duplicate equipment IDs" in s for s in self.mutate(
            lambda c,p,s,r: c["records"][0].update(equipment_id=c["records"][1]["equipment_id"]))))

    def test_unknown_source_rejected(self):
        self.assertTrue(any("unknown source" in s for s in self.mutate(
            lambda c,p,s,r: c["records"][0]["provenance"].update(source_ids=["NONEXISTENT"]))))

    def test_game_added_device_cannot_claim_canon_by_accident(self):
        self.assertTrue(any("game addition not separated" in s for s in self.mutate(
            lambda c,p,s,r: next(x for x in c["records"] if x["provenance"]["classification"] == "GAME_ADDITION")["provenance"].update(source_ids=["L02B_MA_PHASER"]))))

    def test_falsely_implemented_ui_rejected(self):
        self.assertTrue(any("falsely implemented" in s for s in self.mutate(
            lambda c,p,s,r: c["records"][0]["runtime"].update(implementation_status="UE5_READY"))))

    def test_ai_world_state_claim_rejected(self):
        self.assertTrue(any("falsely implemented" in s for s in self.mutate(
            lambda c,p,s,r: c["records"][0]["runtime"].update(ai_world_mutation_allowed=True))))

    def test_invented_numeric_precision_rejected(self):
        self.assertTrue(any("invented performance" in s for s in self.mutate(
            lambda c,p,s,r: c["records"][0].update(canonical_numeric_performance={"distance_m": 9999}))))

    def test_unknown_equipment_in_role_rejected(self):
        self.assertTrue(any("unknown equipment" in s for s in self.mutate(
            lambda c,p,s,r: p["profiles"][0]["typical_equipment_ids"].append("NONEXISTENT"))))

    def test_automatic_grant_rejected(self):
        self.assertTrue(any("automatic grant" in s for s in self.mutate(
            lambda c,p,s,r: p["profiles"][0].update(never_implies="GRANT_ALWAYS"))))

    def test_duplicate_adversarial_id_rejected(self):
        self.assertTrue(any("duplicate case IDs" in s for s in self.mutate(
            lambda c,p,s,r: s["cases"][0].update(case_id=s["cases"][1]["case_id"]))))

    def test_nonexistent_case_equipment_rejected(self):
        self.assertTrue(any("missing equipment" in s for s in self.mutate(
            lambda c,p,s,r: s["cases"][0].update(equipment_id="l02b_fake"))))

    def test_case_cannot_pretend_to_be_playtested(self):
        self.assertTrue(any("falsely executed" in s for s in self.mutate(
            lambda c,p,s,r: s["cases"][0].update(status="UE5_TEST_PASSED"))))

    def test_era_authority_cannot_change(self):
        self.assertTrue(any("duplicate or detached era policy" in s for s in self.mutate(
            lambda c,p,s,r: c.update(canonical_era_source="custom_era_table.json"))))

    def test_cannot_close_without_human_review(self):
        self.assertTrue(any("must await review" in s for s in self.mutate(
            lambda c,p,s,r: c.update(status="COMPLETE"))))

    def test_failures_are_expected_for_all_families(self):
        lookup = {x["equipment_id"]: x["family"] for x in self.base[0]["records"]}
        seen = {lookup[x["equipment_id"]] for x in self.base[2]["cases"]}
        self.assertEqual(len(seen), 7)

if __name__ == "__main__":
    unittest.main()
