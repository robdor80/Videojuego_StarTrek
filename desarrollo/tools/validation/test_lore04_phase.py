#!/usr/bin/env python3
"""Data-level adversarial tests per LORE-04 phase. Not an execution of WorldState."""
import copy
import sys
import unittest
from validate_lore04_phase import validate,validate_manifest,load,BASE,STATUS,PACK_COUNTS
P=sys.argv[1].upper() if len(sys.argv)>1 else "B"
if len(sys.argv)>1: sys.argv=sys.argv[:1]
class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load(BASE+P.lower()+f"/lore04{P.lower()}_cases_v0.1.json")
    def reject(self,fn):
        d=copy.deepcopy(self.data);fn(d)
        with self.assertRaises(AssertionError): validate_manifest(P,d)
    def test_01_full(self):self.assertEqual(validate(P)["phase"],P)
    def test_02_packages(self):self.assertEqual(validate(P)["packages"],PACK_COUNTS[P])
    def test_03_runtime_false(self):self.assertFalse(self.data["runtime_implemented"])
    def test_04_not_merged(self):self.assertEqual(self.data["status"],STATUS)
    def test_05_bad_phase(self):self.reject(lambda d:d.update(phase="Z"))
    def test_06_fake_closed(self):self.reject(lambda d:d.update(status="MERGED"))
    def test_07_wrong_authority(self):self.reject(lambda d:d.update(world_state_owner="AI"))
    def test_08_runtime_fake(self):self.reject(lambda d:d.update(runtime_implemented=True))
    def test_09_missing_pkg(self):self.reject(lambda d:d["packages"].pop())
    def test_10_duplicate_pkg(self):self.reject(lambda d:d["packages"].append(copy.deepcopy(d["packages"][0])))
    def test_11_wrong_pkg_name(self):self.reject(lambda d:d["packages"][0].update(id="Z99"))
    def test_12_missing_pkg_path(self):self.reject(lambda d:d["packages"][0].update(path="missing.md"))
    def test_13_no_author_gates(self):self.reject(lambda d:d.update(author_gates=[]))
    def test_14_no_risk_flags(self):self.reject(lambda d:d.update(review_flags=[]))
    def test_15_no_cases(self):self.reject(lambda d:d.update(cases=[]))
    def test_16_duplicate_case(self):self.reject(lambda d:d["cases"].append(copy.deepcopy(d["cases"][0])))
    def test_17_scenario_canonized(self):self.reject(lambda d:d["cases"][0].update(classification="SCREEN_CANON"))
    def test_18_runtime_case_claim(self):self.reject(lambda d:d["cases"][0].update(executed_in_corerpg=True))
    def test_19_no_preconditions(self):self.reject(lambda d:d["cases"][0].update(preconditions=[]))
    def test_20_no_expected(self):self.reject(lambda d:d["cases"][0].update(expected=[]))
    def test_21_no_forbidden(self):self.reject(lambda d:d["cases"][0].update(forbidden=[]))
    def test_22_missing_dependency(self):self.reject(lambda d:d["dependencies"].append("unknown/path.json"))
    def test_23_forbidden_runtime_marker(self):self.reject(lambda d:d.update(extra="GAMEPLAY_IMPLEMENTED"))
    def test_24_no_main_write(self):self.assertNotIn("main",self.data.get("write_targets",[]))
    def test_25_phase_specific(self):
        if P=="B":self.reject(lambda d:d.update(preserved_block_4="COMPLETE"))
        elif P=="E":self.reject(lambda d:d.update(prior_prs_fused=False))
        else:self.assertEqual(validate(P)["status"],STATUS)
if __name__=="__main__":unittest.main(verbosity=2)
