#!/usr/bin/env python3
"""Crossphase mutation/negative tests, documentary only."""
import copy,unittest
from validate_lore04_e_crossphase import audit_crossphase,validate,PHASES
from validate_lore04_phase import load,BASE
class CrossPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data={p:load(BASE+p.lower()+f"/lore04{p.lower()}_cases_v0.1.json") for p in PHASES}
    def bad(self,fn):
        d=copy.deepcopy(self.data);fn(d)
        with self.assertRaises(AssertionError):audit_crossphase(d)
    def test_01_all(self):self.assertEqual(validate()["validated_phases"],list(PHASES))
    def test_02_count(self):self.assertGreaterEqual(validate()["total_design_cases"],52)
    def test_03_not_runtime(self):self.assertEqual(validate()["runtime"],"NOT_TESTED")
    def test_04_not_merged(self):self.assertEqual(validate()["author_merge"],"E_ONLY_AUTHORIZED_AND_PENDING")
    def test_05_no_B(self):self.bad(lambda d:d.pop("B"))
    def test_06_no_C(self):self.bad(lambda d:d.pop("C"))
    def test_07_no_D(self):self.bad(lambda d:d.pop("D"))
    def test_08_no_E(self):self.bad(lambda d:d.pop("E"))
    def test_09_ai_owns_world(self):self.bad(lambda d:d["B"].update(world_state_owner="AI"))
    def test_10_runtime_claim(self):self.bad(lambda d:d["D"].update(runtime_implemented=True))
    def test_11_block4_falsified(self):self.bad(lambda d:d["B"].update(preserved_block_4="COMPLETE"))
    def test_12_fake_merge(self):self.bad(lambda d:d["E"].update(prior_prs_fused=False))
    def test_13_wrong_core(self):self.bad(lambda d:d["E"].update(checked_corerpg_main_sha="fake"))
    def test_14_wrong_main(self):self.bad(lambda d:d["E"].update(checked_trek_main_sha="fake"))
    def test_15_missing_B_dependency_in_C(self):
        self.bad(lambda d:d["C"].update(dependencies=["sistemas/universe/generation/traffic_activity_model.json"]))
    def test_16_missing_C_dependency_in_D(self):self.bad(lambda d:d["D"].update(dependencies=[]))
    def test_17_missing_B_in_E(self):self.bad(lambda d:d["E"]["dependencies"].remove("proyecto/docs/roadmap/lore_04_b/lore04b_cases_v0.1.json"))
    def test_18_missing_C_in_E(self):self.bad(lambda d:d["E"]["dependencies"].remove("proyecto/docs/roadmap/lore_04_c/lore04c_cases_v0.1.json"))
    def test_19_missing_D_in_E(self):self.bad(lambda d:d["E"]["dependencies"].remove("proyecto/docs/roadmap/lore_04_d/lore04d_cases_v0.1.json"))
    def test_20_wrong_integrated(self):self.bad(lambda d:d["E"].update(integrated_phases=["A","B"]))
    def test_21_missing_e_cases(self):self.bad(lambda d:d["E"].update(cases=[]))
    def test_22_missing_b_cases(self):self.bad(lambda d:d["B"].update(cases=[]))
    def test_23_case_count(self):self.assertEqual(len(self.data["E"]["cases"]),18)
    def test_24_e_audit_readme(self):self.assertEqual(len(validate()["validated_phases"]),4)
if __name__=="__main__":unittest.main(verbosity=2)
