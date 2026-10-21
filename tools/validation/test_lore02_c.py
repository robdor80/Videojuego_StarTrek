#!/usr/bin/env python3
"""Positive/negative documentary tests; no clinical simulation or medicine advice."""
import copy
import unittest
from validate_lore02_c import NAMES, EXPECTED, read, validate, validate_data

class Lore02C(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = [read(n) for n in NAMES]

    def mutate(self, edit, check_paths=False):
        a = copy.deepcopy(self.fixture)
        edit(*a)
        return validate_data(*a, check_paths=check_paths)

    def expect(self, fragment, edit, check_paths=False):
        errors = self.mutate(edit, check_paths)
        self.assertTrue(any(fragment in m for m in errors), errors)

    def test_positive_document_gate(self):
        self.assertEqual(validate()["conditions"], EXPECTED["conditions"])
        self.assertEqual(validate()["cases"], 56)

    def test_provenance_no_unknown_source(self):
        self.expect("unknown provenance",lambda a,c,p,o,s,w,r,e: c["catalogue"][0].update(source_ids=["FAKE"]))

    def test_no_duplicate_source(self):
        self.expect("duplicate source ID",lambda a,c,p,o,s,w,r,e: r["sources"].append(dict(r["sources"][-1])))

    def test_atlas_no_duplicate_profile(self):
        self.expect("duplicate species clinical profile",lambda a,c,p,o,s,w,r,e: a["records"][1].update(profile_id=a["records"][0]["profile_id"]))

    def test_borg_is_not_species(self):
        self.expect("Borg incorrectly modeled as a species",lambda a,c,p,o,s,w,r,e: a["records"][-1].update(entity_kind="HUMANOID"))

    def test_no_fabricated_baseline(self):
        self.expect("invented medical numeric baseline",lambda a,c,p,o,s,w,r,e: a["records"][0].update(normal_vitals={"pulse":72}))

    def test_no_fake_pharmacy(self):
        self.expect("invented medical numeric baseline",lambda a,c,p,o,s,w,r,e: a["records"][0].update(species_specific_doses={"fictional":55}))

    def test_no_unreviewed_atlas(self):
        self.expect("must await human review",lambda a,c,p,o,s,w,r,e: a.update(status="COMPLETE"))

    def test_no_condition_duplicate(self):
        self.expect("duplicate clinical condition",lambda a,c,p,o,s,w,r,e: c["catalogue"][1].update(condition_id=c["catalogue"][0]["condition_id"]))

    def test_no_false_game_canon(self):
        self.expect("fake canonical evidence",lambda a,c,p,o,s,w,r,e: next(x for x in c["catalogue"] if x["claim_class"]=="GAME_ADDITION").update(source_ids=["L02C_ST_TRILL"]))

    def test_no_condition_omniscience(self):
        self.expect("diagnostic omniscience",lambda a,c,p,o,s,w,r,e: c["catalogue"][0].update(information_gate="OMNISCIENT"))

    def test_no_invented_treatment_dose(self):
        self.expect("invented dosage or timetable",lambda a,c,p,o,s,w,r,e: c["catalogue"][0].update(clinical_dose="10 mg"))

    def test_missing_procedure_detected(self):
        self.expect("missing medical procedure",lambda a,c,p,o,s,w,r,e: c["catalogue"][0].update(procedure_ref="l02c_proc_MISSING"))

    def test_wrong_equipment_family(self):
        self.expect("unknown or nonmedical equipment",lambda a,c,p,o,s,w,r,e: p["records"][0]["equipment_refs"].append("l02b_phaser_type_2"))

    def test_proc_does_not_implement_ue5(self):
        self.expect("bypasses Core or falsely claims UE5",lambda a,c,p,o,s,w,r,e: p["records"][0].update(ue5_implemented=True))

    def test_proc_must_check_consent(self):
        self.expect("lacks medical safeguards",lambda a,c,p,o,s,w,r,e: p["records"][0].update(preconditions=["only_player_click"]))

    def test_proc_no_numeric_precision(self):
        self.expect("invented real clinical precision",lambda a,c,p,o,s,w,r,e: p["records"][0].update(real_world_dosing="always 1mL"))

    def test_facilities_need_staff(self):
        self.expect("facility magic capacity",lambda a,c,p,o,s,w,r,e: o["facilities"][0].update(auto_spawn=True))

    def test_captain_does_not_see_medical_record(self):
        self.expect("staff automatic authority",lambda a,c,p,o,s,w,r,e: o["professionals"][0].update(full_medical_record_access=True))

    def test_ai_cannot_bypass_privacy(self):
        self.expect("medical privacy AI bypass",lambda a,c,p,o,s,w,r,e: w.update(ai_context_policy="ALL_WORLD_FACTS"))

    def test_no_decorative_clinical_steps(self):
        self.expect("diagnostic process bypass",lambda a,c,p,o,s,w,r,e: w["workflow"][0].update(result_is_not_arbitrary_ai_decision=False))

    def test_no_fake_playtesting(self):
        self.expect("falsely playtested or mutated",lambda a,c,p,o,s,w,r,e: s["cases"][0].update(status="UE5_PASSED"))

    def test_no_duplicate_scenario(self):
        self.expect("duplicate medical scenario",lambda a,c,p,o,s,w,r,e: s["cases"][1].update(case_id=s["cases"][0]["case_id"]))

    def test_no_unknown_case_condition(self):
        self.expect("unknown case condition",lambda a,c,p,o,s,w,r,e: s["cases"][0].update(condition_ref="l02c_unknown"))

    def test_no_unknown_case_source(self):
        self.expect("unknown scenario evidence",lambda a,c,p,o,s,w,r,e: s["cases"][0].update(source_ids=["IMPOSSIBLE"]))

    def test_no_detached_lore01_species_reference(self):
        self.expect("taxonomy evidence detached",lambda a,c,p,o,s,w,r,e: a["records"][0].update(evidence_ref="lore/species/evidence/human_v0.2.json"))

    def test_all_cases_account_for_finite_resources(self):
        for s in self.fixture[4]["cases"]:
            self.assertIn("equipment_staff_stock_energy_and_facility",s["preconditions"])

if __name__ == "__main__":
    unittest.main()
