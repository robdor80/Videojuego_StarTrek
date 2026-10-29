#!/usr/bin/env python3
"""Negative mutation tests of LORE-04A authoring documents/fixtures, no runtime simulation."""
import copy
import unittest
from validate_lore04_a import (validate,load,assert_evidence,assert_scenarios,
                               assert_invariants,assert_doc_files,ROOT,DOCS,DIR,MASTER,
                               REGISTRY,EVIDENCE,SCENARIOS,INVARIANTS)
class TestLore04A(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg=load(REGISTRY)
        cls.e=load(EVIDENCE)
        cls.s=load(SCENARIOS)
        cls.i=load(INVARIANTS)
        cls.master=(ROOT/MASTER).read_text(encoding="utf-8")
        cls.docs={k:(ROOT/(DIR+v)).read_text(encoding="utf-8") for k,v in DOCS.items()}
        cls.eids={x["id"] for x in cls.e["claims"]}
    def bad_e(self,fn):
        e=copy.deepcopy(self.e);fn(e)
        with self.assertRaises(AssertionError): assert_evidence(e,self.reg)
    def bad_s(self,fn):
        s=copy.deepcopy(self.s);fn(s)
        with self.assertRaises(AssertionError): assert_scenarios(s,self.eids)
    def bad_i(self,fn):
        i=copy.deepcopy(self.i);fn(i)
        with self.assertRaises(AssertionError): assert_invariants(i)
    def bad_docs(self,fn):
        d=copy.deepcopy(self.docs);fn(d)
        with self.assertRaises(AssertionError): assert_doc_files(d,self.master)
    def test_01_full_documentary(self): self.assertEqual(validate()["packages"],8)
    def test_02_registry_count(self): self.assertGreaterEqual(validate()["sources"],530)
    def test_03_claim_count(self): self.assertGreaterEqual(validate()["claims"],14)
    def test_04_scenario_count(self): self.assertEqual(validate()["scenarios"],16)
    def test_05_invariant_count(self): self.assertGreaterEqual(validate()["invariants"],14)
    def test_06_no_runtime(self): self.assertEqual(validate()["runtime"],"NOT_TESTED")
    def test_07_missing_A06(self): self.bad_docs(lambda d:d.pop("A06"))
    def test_08_wrong_A07_header(self): self.bad_docs(lambda d:d.update(A07="# NOT THE PACKAGE"))
    def test_09_truncated_A03(self): self.bad_docs(lambda d:d.update(A03="# LORE-04A / A03"))
    def test_10_duplicate_claim(self): self.bad_e(lambda d:d["claims"].append(copy.deepcopy(d["claims"][0])))
    def test_11_unknown_source(self): self.bad_e(lambda d:d["claims"][0].update(screen_source_id="NOT_REGISTERED"))
    def test_12_official_as_screen(self): self.bad_e(lambda d:d["claims"][0].update(screen_source_id="L04A_ST_FAMILY"))
    def test_13_screen_as_official(self): self.bad_e(lambda d:d["claims"][0].update(official_source_id="TNG_FAMILY"))
    def test_14_fake_scene_verified(self): self.bad_e(lambda d:d["claims"][0].update(screen_recheck="COMPLETE"))
    def test_15_missing_screen_limits(self): self.bad_e(lambda d:d["claims"][0].update(limits=""))
    def test_16_fake_confidence(self): self.bad_e(lambda d:d["claims"][0].update(confidence="DEFINITE"))
    def test_17_claim_noclass(self): self.bad_e(lambda d:d["claims"][0].update(classification="UNIVERSAL_CANON"))
    def test_18_promote_official_to_screen(self): self.bad_e(lambda d:d["claims"][11].update(classification="SCREEN_CANON"))
    def test_19_gameaddition_no_cause(self): self.bad_e(lambda d:d["claims"][12].update(game_need=""))
    def test_20_gameaddition_authorapproval(self): self.bad_e(lambda d:d["claims"][12].update(author_approval="APPROVED"))
    def test_21_duplicate_scenario(self): self.bad_s(lambda d:d["scenarios"].append(copy.deepcopy(d["scenarios"][0])))
    def test_22_missing_CIV16(self): self.bad_s(lambda d:d["scenarios"].pop())
    def test_23_live_simulation_claim(self): self.bad_s(lambda d:d["scenarios"][0].update(simulation_executed=True))
    def test_24_ai_authority(self): self.bad_s(lambda d:d["scenarios"][0].update(authority="AI"))
    def test_25_approved_fixture(self): self.bad_s(lambda d:d["scenarios"][0].update(classification="SCREEN_CANON"))
    def test_26_missing_precondition(self): self.bad_s(lambda d:d["scenarios"][0].update(preconditions=[]))
    def test_27_missing_forbidden(self): self.bad_s(lambda d:d["scenarios"][0].update(forbidden=[]))
    def test_28_missing_expected(self): self.bad_s(lambda d:d["scenarios"][0].update(expected=[]))
    def test_29_unknown_evidence(self): self.bad_s(lambda d:d["scenarios"][0].update(evidence_ids=["MISSING"]))
    def test_30_author_choice_bound(self): self.bad_s(lambda d:d["scenarios"][0].update(author_decision="AUTHOR_APPROVED"))
    def test_31_false_invariant_runtime(self): self.bad_i(lambda d:d.update(status="GAMEPLAY_IMPLEMENTED"))
    def test_32_false_ue5_runtime(self): self.bad_i(lambda d:d["test_execution"].update(integration_CoreRPG_UE5="PASS"))
    def test_33_false_case_execution(self): self.bad_i(lambda d:d["test_execution"].update(domain_cases="PASS"))
    def test_34_duplicate_invariant(self): self.bad_i(lambda d:d["cases"].append(copy.deepcopy(d["cases"][0])))
    def test_35_missing_invariant_expectation(self): self.bad_i(lambda d:d["cases"][0].update(expected=[]))
    def test_36_wrong_invariant_type(self): self.bad_i(lambda d:d["cases"][0].update(type="CANON"))
    def test_37_screen_label_not_official(self):
        reg=copy.deepcopy(self.reg)
        src=next(x for x in reg["sources"] if x["source_id"]=="L04A_ST_FAMILY")
        src["source_type"]="SCREEN_CANON"
        with self.assertRaises(AssertionError): assert_evidence(self.e,reg)
    def test_38_duplicate_registry_id(self):
        reg=copy.deepcopy(self.reg);reg["sources"].append(copy.deepcopy(reg["sources"][0]))
        with self.assertRaises(AssertionError): assert_evidence(self.e,reg)
    def test_39_claims_without_evidence(self): self.bad_e(lambda d:d.update(claims=[]))
    def test_40_lower_era_spread(self):
        self.assertIn("2383",self.docs["A08"])
        self.assertIn("Academia",self.docs["A03"])
if __name__=="__main__":
    unittest.main(verbosity=2)
