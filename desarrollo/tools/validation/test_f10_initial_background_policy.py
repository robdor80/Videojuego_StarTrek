#!/usr/bin/env python3
"""F10 H06-P06-A5: tests de contrato y escenarios de triaje SIN autoridad runtime."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from f10_initial_background_reference import evaluate_reference

ROOT = Path(__file__).resolve().parents[3]
POLICY = ROOT / "sistemas/gameplay/character_creation/f10_initial_background_policy_v0.1.json"
MATURITY = ROOT / "sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json"
EVIDENCE = ROOT / "sistemas/gameplay/character_creation/f10_biography_evidence_semantic_boundary_v0.1.json"
CREATION = ROOT / "sistemas/gameplay/character_creation/character_creation_contract_v1_0.json"
PRIOR = ROOT / "sistemas/gameplay/character_creation/prior_activity_model.json"
F10_HEADER = ROOT / "desarrollo/integration/host/src/f10/biography_evidence.h"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class InitialBackgroundPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = load(POLICY)
        cls.m = load(MATURITY)
        cls.e = load(EVIDENCE)

    def test_contract_design_not_runtime(self):
        self.assertEqual(self.p["status"], "DESIGN_PROPOSAL_NOT_RUNTIME_AUTHORITY")
        self.assertEqual(self.p["phase"], "H06-P06-A5")
        self.assertTrue(self.p["guardrails"]["no_core_unreal_f11_changes"])
        self.assertTrue(self.p["guardrails"]["no_person_creation_or_admission"])

    def test_source_refs_exist_and_locked_baselines_unchanged(self):
        for path in self.p["source_refs"]:
            self.assertTrue((ROOT / path).is_file(), path)
        self.assertEqual(load(CREATION)["status"], "locked_baseline")
        self.assertEqual(load(PRIOR)["status"], "locked_baseline")

    def test_no_extra_biography_fields_added_to_locked_contract(self):
        allowed = set(load(CREATION)["required_character_fields"] + load(CREATION)["optional_character_fields"])
        self.assertTrue(set(self.p["canonical_field_links"]).issubset(allowed))
        self.assertIn("prior_activities_and_hobbies", self.p["canonical_field_links"])

    def test_source_registry_reuses_native_port(self):
        h = F10_HEADER.read_text(encoding="utf-8")
        for s in ("class RegisteredBiographyAuthority", "struct BiographyClaimEvidence",
                  "VALIDATED_INITIAL_BACKGROUND", "bool resolves"):
            self.assertIn(s, h)
        self.assertEqual(self.p["initial_background_attestation"]["origin_type"], "VALIDATED_INITIAL_BACKGROUND")
        self.assertTrue(self.p["initial_background_attestation"]["pre_person_stage_supported"])

    def test_no_external_documents_for_personal_hobbies(self):
        classes = {v["code"]: v for v in self.p["claim_classes"]}
        for kind in ("PERSONAL_ACTIVITY", "PERSONAL_INTEREST", "FAMILY_ORIGIN_CONTEXT"):
            self.assertEqual(classes[kind]["tier"], "PERSONAL_BACKGROUND")
            self.assertFalse(classes[kind]["external_document_required"])
        self.assertFalse(classes["FORMAL_CERTIFICATION"]["external_document_required"])
        self.assertIn("PROFESSIONAL_LICENSE", classes["FORMAL_CERTIFICATION"]["no_automatic_effects"])

    def test_professional_and_rank_not_free(self):
        classes = {v["code"]: v for v in self.p["claim_classes"]}
        self.assertEqual(classes["STARFLEET_COMMISSION_OR_CLEARANCE"]["tier"], "INSTITUTIONAL_AUTHORITY")
        self.assertIn("RANK", classes["STARFLEET_COMMISSION_OR_CLEARANCE"]["no_automatic_effects"])
        self.assertIn("LOYALTY", classes["CITIZENSHIP_OR_LEGAL_STATUS"]["no_automatic_effects"])

    def test_age_not_equivalent_to_biological_maturity(self):
        rule = self.p["maturity_policy_proposal"]
        self.assertTrue(rule["numeric_playable_floor_required"])
        self.assertTrue(rule["lifetime_stage_must_have_species_support_or_explicit_author_approved_f10_rule"])
        self.assertTrue(rule["self_declared_adult_equivalent_is_an_input_not_evidence"])
        self.assertEqual(rule["age_above_floor_without_lifecycle_support"], "REVIEW_REQUIRED_NO_PERSON")
        self.assertEqual(rule["special_species_without_specific_rule"], "SPECIAL_MATURITY_RULE_REQUIRED_NO_PERSON")

    def test_unresolved_calendar_and_dlc(self):
        self.assertEqual(self.p["campaign"]["start_year"], 2383)
        self.assertEqual(self.p["campaign"]["start_month_day"], "UNDECIDED_BY_AUTHOR")
        self.assertEqual(sum(v["content_scope"] == "DLC_DELTA" for v in self.m["species"]), 5)
        self.assertTrue(self.p["guardrails"]["no_H07_start"])

    def test_all_author_examples(self):
        for x in self.p["examples"]:
            with self.subTest(example=x["id"]):
                got = evaluate_reference(x, policy=self.p, maturity=self.m)
                self.assertEqual(got["outcome"], x["reference_outcome"])
                self.assertEqual(got["tier"], x["expected_tier"])
                self.assertIn(x["issue_code"], got["issues"])
                self.assertFalse(got["person_created"])
                self.assertFalse(got["evidence_issued"])

    def test_birthyear_threshold_is_pending_even_january(self):
        for day in ("2365-01-01", "2365-08-10", "2365-12-31"):
            # La referencia no interpreta fecha completa: el ano exacto obliga a revisarla.
            x={"species_id":"human","birth_year":int(day[:4]),"claim_class":"PERSONAL_INTEREST"}
            got=evaluate_reference(x,policy=self.p,maturity=self.m)
            self.assertIn("PLAYABLE_AGE_UNDECIDED", got["issues"])
            self.assertEqual(got["outcome"], "REVIEW_REQUIRED")

    def test_no_mortality_from_lifespan(self):
        x={"species_id":"human","age_years":1200,"claim_class":"PERSONAL_INTEREST"}
        got=evaluate_reference(x,policy=self.p,maturity=self.m)
        self.assertNotIn("BELOW_PLAYABLE_AGE",got["issues"])
        self.assertEqual(got["outcome"], "REVIEW_REQUIRED")

    def test_no_synthetic_evidence_by_client_flag(self):
        x={"species_id":"human","age_years":20,"claim_class":"PERSONAL_ACTIVITY",
           "started_at_age":8,"validated_creation_ref":"fake"}
        got=evaluate_reference(x,policy=self.p,maturity=self.m)
        self.assertIn("FORBIDDEN_AUTHORITY_FIELD",got["issues"])
        self.assertEqual(got["outcome"],"CHANGES_REQUIRED")
        self.assertFalse(got["evidence_issued"])

    def test_nested_client_forgery_rejected(self):
        x={"species_id":"human","age_years":20,"claim_class":"PERSONAL_INTEREST",
           "details":{"notes":[{"authority_grant_id":"pretend"}]}}
        self.assertIn("FORBIDDEN_AUTHORITY_FIELD",evaluate_reference(x,policy=self.p,maturity=self.m)["issues"])

    def test_unsupported_claim_fails_pending(self):
        x={"species_id":"human","age_years":20,"claim_class":"FAKE_DIPLOMA"}
        got=evaluate_reference(x,policy=self.p,maturity=self.m)
        self.assertIn("CLAIM_CLASS_NOT_SUPPORTED",got["issues"])
        self.assertEqual(got["outcome"],"REVIEW_REQUIRED")

    def test_inconsistent_activity_rejected_without_ai(self):
        x={"species_id":"human","age_years":20,"claim_class":"PERSONAL_ACTIVITY",
           "started_at_age":17,"ended_at_age":12}
        got=evaluate_reference(x,policy=self.p,maturity=self.m)
        self.assertIn("ACTIVITY_TIME_CONFLICT",got["issues"])
        self.assertEqual(got["outcome"],"CHANGES_REQUIRED")
        self.assertFalse(got["semantic_review_executed"])

    def test_boolean_age_is_not_integer(self):
        x={"species_id":"human","age_years":True,"claim_class":"PERSONAL_INTEREST"}
        self.assertIn("AGE_CONTEXT_NOT_SUPPORTED",evaluate_reference(x,policy=self.p,maturity=self.m)["issues"])

    def test_unknown_species_no_fallback_to_human(self):
        x={"species_id":"dragonfolk","age_years":20,"claim_class":"PERSONAL_INTEREST"}
        got=evaluate_reference(x,policy=self.p,maturity=self.m)
        self.assertIn("UNKNOWN_SPECIES",got["issues"])
        self.assertEqual(got["outcome"],"CHANGES_REQUIRED")

    def test_no_automatic_admission_or_skills(self):
        p=self.p["principles"]
        for flag in ("no_numeric_skill_points_from_authored_text","no_automatic_person_rank_admission_from_biography",
                     "double_gate_objective_then_semantic_required", "no_semantic_ai_self_approval",
                     "no_auto_rewrite_of_player_story"):
            self.assertTrue(p[flag])
        forbidden=set(self.p["initial_background_attestation"]["must_not_confer"])
        self.assertTrue({"PERSON","F11_RANK","F05_BINDING","ADMISSION","SKILL_POINTS"}.issubset(forbidden))

    def test_offline_never_valid_or_approved(self):
        for x in self.p["examples"]:
            result=evaluate_reference(x,policy=self.p,maturity=self.m)
            self.assertIn(result["outcome"],("CHANGES_REQUIRED","REVIEW_REQUIRED"))
            self.assertFalse(result["evidence_issued"])
            self.assertFalse(result["person_created"])
        self.assertEqual(self.p["review_outcomes"]["reference_layer"],["CHANGES_REQUIRED","REVIEW_REQUIRED"])

    def test_semantic_provider_and_integration_remain_pending(self):
        self.assertEqual(self.e["semantic_review"]["provider_selection"],"NOT_SELECTED_NOT_APPROVED")
        self.assertEqual(self.p["next_code_cut"]["status"],"PENDING")
        self.assertIn("SEMANTIC_PROVIDER_CONNECTION",self.p["next_code_cut"]["explicit_not_covered"])
        self.assertEqual(self.p["next_code_cut"]["suggested_model"],"GPT-6")


if __name__ == "__main__":
    unittest.main()
