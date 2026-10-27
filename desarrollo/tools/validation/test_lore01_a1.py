#!/usr/bin/env python3
"""Pruebas de regresión negativas de LORE-01 A.1."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).with_name("validate_lore01_a1.py")
spec=importlib.util.spec_from_file_location("lore01_a1",HERE)
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

class CulturalBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources={r["source_id"]:r for r in mod.read_json(mod.ROOT/"mundo/sources/source_registry/source_registry.json")["sources"]}
        cls.vulcan=mod.read_json(mod.ROOT/mod.SUB/"profiles/vulcan_behavior_v0.1.json")
        cls.hirogen=mod.read_json(mod.ROOT/mod.SUB/"profiles/hirogen_behavior_v0.1.json")
        cls.pakled=mod.read_json(mod.ROOT/mod.SUB/"profiles/pakled_behavior_v0.1.json")

    def invalid(self,profile,id):
        return mod.validate_profile(profile,id,self.sources)

    def test_repo(self):
        self.assertEqual(mod.validate_repo(),[])

    def test_species_culture_autolock(self):
        p=copy.deepcopy(self.vulcan)
        p["culture_bindings"]["species_auto_attachment"]=True
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_multicultural_character_must_be_supported(self):
        p=copy.deepcopy(self.vulcan)
        p["culture_bindings"]["allowed_for_other_species_when_socialized"]=False
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_no_species_personality_weights(self):
        p=copy.deepcopy(self.vulcan)
        p["ai_application"]["no_generated_personality_scores"]=False
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_no_authority_transfer_to_llm(self):
        p=copy.deepcopy(self.vulcan)
        p["ai_application"]["decision_authority"]="AI"
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_delta_cannot_appear_main_game(self):
        p=copy.deepcopy(self.hirogen)
        p["content_gate"]="MAIN_GAME"
        self.assertTrue(self.invalid(p,"hirogen"))

    def test_pakled_cannot_have_collective_assumption(self):
        p=copy.deepcopy(self.pakled)
        p["prior_strength"]="STRONG_CONTEXTUAL_NORMS"
        self.assertTrue(self.invalid(p,"pakled"))

    def test_evidence_must_preexist_in_ledger(self):
        p=copy.deepcopy(self.vulcan)
        p["source_basis"]["anchors"][0]="DS9_DUET"
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_missing_culture_file_detected(self):
        p=copy.deepcopy(self.vulcan)
        p["culture_bindings"]["profile_ref"]="fake/path.json"
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_distinct_individual_outcomes(self):
        p=copy.deepcopy(self.vulcan)
        p["distinct_individual_outcomes_es"]=[]
        self.assertTrue(self.invalid(p,"vulcan"))

    def test_unauthorized_psychological_inference(self):
        p=copy.deepcopy(self.vulcan)
        p["ai_application"]["invalid_inferences"].remove("hostilidad")
        self.assertTrue(self.invalid(p,"vulcan"))

if __name__=="__main__":
    unittest.main()
