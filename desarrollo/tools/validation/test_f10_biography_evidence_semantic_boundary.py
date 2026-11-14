#!/usr/bin/env python3
"""H06-P06-A3: contrato de diseño, nunca proveedor ni autoridad de producto."""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
REF = ROOT / "sistemas/gameplay/character_creation/f10_biography_evidence_semantic_boundary_v0.1.json"
INTERFACE = ROOT / "sistemas/gameplay/character_creation/f10_biography_validation_interface_v0.1.json"
MATURITY = ROOT / "sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json"
FACTORY = ROOT / "sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json"
HEADER = ROOT / "desarrollo/integration/host/src/f10/biography_validation.h"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class H06P06A3ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(REF)
        cls.interface = load(INTERFACE)
        cls.maturity = load(MATURITY)
        cls.factory = load(FACTORY)

    def test_design_only_and_current_core_pin(self):
        self.assertEqual(self.data["status"], "PROPOSED_DESIGN_ONLY_NOT_RUNTIME_CONNECTED")
        self.assertTrue(self.data["scope"]["no_unreal_or_core_write"])
        self.assertIn(self.factory["campaign"]["runtime_core_sha"], self.data["world_authority"])
        self.assertEqual(self.data["release_gate"]["current_runtime"], "REVIEW_UNAVAILABLE_WITHOUT_APPROVED_PROVIDERS")

    def test_current_cpp_interfaces_not_fabricated(self):
        header = HEADER.read_text(encoding="utf-8")
        for signature in ("class BiographyAuthority", "class SemanticEvaluator", "class BiographyValidator",
                          "ReviewEvidence review", "DomainDecision verify", "bool resolves", "bool eligible"):
            self.assertIn(signature, header)
        self.assertTrue(self.data["interface_alignment"]["this_contract_does_not_change_native_abi"])

    def test_references_are_existing_sources(self):
        for path in self.data["source_contract_paths"]:
            self.assertTrue((ROOT / path).is_file(), path)
        self.assertIn(str(MATURITY.relative_to(ROOT)), self.data["source_contract_paths"])

    def test_both_gates_and_provenance_boundary(self):
        interface = self.data["interface_alignment"]
        self.assertIn("BiographyAuthority::resolves", interface["objective_port"])
        self.assertIn("SemanticEvaluator::review", interface["semantic_port"])
        self.assertIn("BiographyAuthority::verify", interface["domain_final_review"])
        self.assertEqual(set(interface["exact_input_binding"]),
                         {"draft_sha256", "context_sha256", "ruleset", "policy"})
        self.assertTrue(self.data["evidence_model"]["internal_source_registry_required"])
        self.assertTrue(self.data["evidence_model"]["no_authority_from_client_strings"])

    def test_untrusted_input_not_equivalent_to_evidence(self):
        e = self.data["evidence_model"]
        self.assertEqual(e["client_payload_semantics"], "UNTRUSTED_PROPOSAL_ONLY")
        self.assertIn("PLAYER_DECLARATION", e["explicitly_untrusted_origins"])
        self.assertIn("MODEL_GENERATED_FACT", e["explicitly_untrusted_origins"])
        self.assertIn("F10_VALIDATED_INITIAL_BACKGROUND_SOURCE", e["accepted_internal_origin_types"])
        self.assertIn("draft_sha256", e["evidence_binding_required"])
        self.assertIn("source_version_or_world_revision", e["evidence_binding_required"])
        self.assertEqual(e["missing_or_conflicting_source"], "REVIEW_REQUIRED_NO_PERSON")

    def test_initial_person_does_not_need_preexisting_person_fact(self):
        self.assertIn("no pre-existing PERSON", self.data["evidence_model"]["initial_character_bootstrap"])
        self.assertIn("INDIVIDUAL_MATURITY",
                      [item["code"] for item in self.data["objective_categories"]])
        rule = next(item for item in self.data["objective_categories"] if item["code"] == "PLAYABLE_MINIMUM")
        self.assertEqual(rule["cannot_prove"], "INDIVIDUAL_ADULTHOOD")
        self.assertIn("RULE_FOR_TRUSTED_INITIAL_INDIVIDUAL_MATURITY_WITHOUT_PREEXISTING_PERSON",
                      self.data["unresolved_author_decisions"])

    def test_hard_rejections_not_resolvable_by_evidence_provider(self):
        expected = {"BELOW_PLAYABLE_AGE", "DLC_DELTA_UNAVAILABLE", "SPECIAL_MATURITY_RULE_REQUIRED",
                    "PLAYABLE_AGE_UNDECIDED", "NON_ADULT_DECLARED", "FORBIDDEN_AUTHORITY_FIELD"}
        self.assertTrue(expected.issubset(set(self.data["non_resolvable_by_general_evidence_provider"])))

    def test_semantic_review_is_local_first_and_not_selected(self):
        sem = self.data["semantic_review"]
        self.assertEqual(sem["provider_selection"], "NOT_SELECTED_NOT_APPROVED")
        self.assertFalse(sem["model_prompt_or_output_as_authority"])
        self.assertFalse(sem["external_network"] == "AUTHORIZED")
        self.assertFalse(sem["hidden_world_facts_disclosure"])
        self.assertIn("EXACT_REQUEST_BINDING", sem["domain_verifier_must_recheck"])
        self.assertIn("FULL_COMPLETION_AND_STRICT_SCHEMA", sem["domain_verifier_must_recheck"])
        self.assertEqual(sem["provider_missing_or_timeout"], "REVIEW_UNAVAILABLE_NO_PERSON")
        self.assertIn("CREATE_PERSON", sem["prohibited_effects"])
        self.assertEqual(sem["permitted_finding_types"], ["CONTRADICTION", "SUGGESTION"])

    def test_decision_matrix_never_creates_person(self):
        matrix = self.data["decision_matrix"]
        self.assertEqual(len(matrix), len({x["input"] for x in matrix}))
        self.assertGreaterEqual(len(matrix), 10)
        self.assertTrue(all("NO_PERSON" in x["publication"] for x in matrix))
        cases = {x["input"]: x for x in matrix}
        self.assertEqual(cases["PROVABLY_UNDER_MINIMUM"]["objective"], "CHANGES_REQUIRED")
        self.assertEqual(cases["OBJECTIVE_VALID_BUT_NO_SEMANTIC_PROVIDER"]["semantic"], "REVIEW_UNAVAILABLE")
        self.assertEqual(cases["BOTH_GATES_VERIFIED_IN_FUTURE"]["publication"],
                         "PRIVATE_RECEIPT_ONLY_NO_PERSON_UNTIL_FUTURE_COMMIT")

    def test_rule_and_provider_changes_invalidate_review(self):
        invalidations = set(self.data["receipt_and_lifecycle"]["stale_if"])
        self.assertTrue({"draft_changed", "campaign_context_changed", "maturity_policy_changed",
                         "objective_rules_changed", "semantic_policy_changed", "provider_identity_or_version_changed",
                         "issuer_or_generation_changed"}.issubset(invalidations))
        self.assertTrue(self.data["receipt_and_lifecycle"]["evaluation_is_read_only"])

    def test_calendar_specials_dlc_retained(self):
        self.assertEqual(self.data["scope"]["campaign_year"], self.maturity["scope"]["campaign_start_year"])
        self.assertEqual(self.data["scope"]["campaign_month_day"], "UNDECIDED_BY_AUTHOR")
        ids = {x["species_id"] for x in self.maturity["species"] if x["minimum_playable_age_earth_years"] is None}
        self.assertEqual(ids, {"changeling", "jem_hadar", "vorta"})
        self.assertEqual(sum(x["content_scope"] == "DLC_DELTA" for x in self.maturity["species"]), 5)
        self.assertTrue(self.data["release_gate"]["no_dlc_unlock"])

    def test_not_a_runtime_certification(self):
        rel = self.data["release_gate"]
        for key in ("h06_p06_a", "hu08", "m1"):
            self.assertEqual(rel[key], "PARTIAL")
        self.assertTrue(rel["no_h07_start"])
        self.assertEqual(rel["tests_for_this_cut"], "STATIC_CONTRACT_ONLY")


if __name__ == "__main__":
    unittest.main()
