#!/usr/bin/env python3
"""Pruebas offline del precheck F10/H06-P06-A; NO validan una PERSON real."""
from __future__ import annotations

import copy
import unittest

from f10_biography_precheck import evaluate


def example() -> dict:
    return {
        "display_name": "Talia Ren",
        "species_id": "human",
        "age_or_birth_date": 20,
        "adult_equivalent_status": True,
        "origin": "colonia humana sin clasificar",
        "citizenship_context": "por acreditar",
        "culture_context": "sin presuposiciones",
        "appearance_profile": "descripción del jugador",
        "prior_education": ["estudios básicos"],
        "prior_activities_and_hobbies": [
            {"name": "karate", "started_at_or_age": 8,
             "ended_at_or_current": "current", "typical_frequency": "regular"}
        ],
        "prior_experience": ["afición a la astronomía"],
        "initial_long_term_objective": "ingresar en la Flota Estelar",
    }


class BiographyPrecheckTests(unittest.TestCase):
    def test_complete_example_requires_review_not_auto_admission(self):
        draft = example()
        original = copy.deepcopy(draft)
        out = evaluate(draft)
        self.assertEqual(out["status"], "REVIEW_REQUIRED")
        self.assertEqual(out["objective_gate"], "NOT_IMPLEMENTED")
        self.assertEqual(out["semantic_gate"], "PENDING")
        self.assertEqual(draft, original)
        self.assertFalse(out["person_created"])
        self.assertFalse(out["world_state_mutated"])
        self.assertFalse(out["effects_applied"])
        self.assertIsNone(out["validated_creation_ref"])

    def test_draft_without_required_field(self):
        draft = example()
        draft.pop("origin")
        out = evaluate(draft)
        self.assertEqual(out["status"], "CHANGES_REQUIRED")
        self.assertIn({"code": "MISSING_REQUIRED_FIELD", "field": "origin"}, out["issues"])

    def test_unknown_species_has_no_human_fallback(self):
        draft = example()
        draft["species_id"] = "invented_alien"
        out = evaluate(draft)
        self.assertEqual(out["status"], "CHANGES_REQUIRED")
        self.assertIn({"code": "UNKNOWN_SPECIES", "field": "species_id"}, out["issues"])

    def test_nonhuman_maturity_cannot_be_guessed(self):
        draft = example()
        draft["species_id"] = "vulcan"
        self.assertEqual(evaluate(draft)["status"], "REVIEW_REQUIRED")

    def test_declared_minor_requires_change(self):
        draft = example()
        draft["adult_equivalent_status"] = False
        self.assertIn({"code": "NON_ADULT_DECLARED", "field": "adult_equivalent_status"},
                      evaluate(draft)["issues"])

    def test_true_is_not_proof_of_adulthood(self):
        draft = example()
        draft["adult_equivalent_status"] = True
        out = evaluate(draft)
        self.assertEqual(out["status"], "REVIEW_REQUIRED")

    def test_date_after_campaign_year_is_rejected(self):
        draft = example()
        draft["age_or_birth_date"] = "2384-01-01"
        self.assertIn({"code": "BIRTH_AFTER_CAMPAIGN_YEAR", "field": "age_or_birth_date"},
                      evaluate(draft)["issues"])

    def test_invalid_calendar_date_is_rejected(self):
        draft = example()
        draft["age_or_birth_date"] = "2363-02-30"
        self.assertIn({"code": "UNSUPPORTED_BIRTH_VALUE", "field": "age_or_birth_date"},
                      evaluate(draft)["issues"])

    def test_age_bool_or_negative_is_rejected(self):
        draft = example()
        for value in (-1, True):
            draft["age_or_birth_date"] = value
            self.assertIn({"code": "UNSUPPORTED_BIRTH_VALUE", "field": "age_or_birth_date"},
                          evaluate(draft)["issues"])

    def test_activity_exceeds_current_age(self):
        draft = example()
        draft["prior_activities_and_hobbies"][0]["started_at_or_age"] = 21
        self.assertIn({"code": "PRIOR_ACTIVITY_AGE_CONFLICT",
                       "field": "prior_activities_and_hobbies[0]"}, evaluate(draft)["issues"])

    def test_activity_end_before_start(self):
        draft = example()
        draft["prior_activities_and_hobbies"][0]["ended_at_or_current"] = 3
        self.assertEqual(evaluate(draft)["status"], "CHANGES_REQUIRED")

    def test_no_client_authority(self):
        for forbidden in ("person_id", "validated_creation_ref", "admission_authorized", "rank"):
            with self.subTest(key=forbidden):
                draft = example()
                draft[forbidden] = "fake"
                self.assertIn("FORBIDDEN_AUTHORITY_FIELD",
                              [x["code"] for x in evaluate(draft)["issues"]])

    def test_no_hidden_client_authority(self):
        draft = example()
        draft["prior_experience"] = [{"issuer": "ADMIRAL", "rank": "captain"}]
        self.assertIn("FORBIDDEN_AUTHORITY_FIELD",
                      [x["code"] for x in evaluate(draft)["issues"]])

    def test_nickname_is_not_character_name_or_identity(self):
        draft = example()
        draft["nickname"] = "player123"
        self.assertIn("FORBIDDEN_AUTHORITY_FIELD",
                      [x["code"] for x in evaluate(draft)["issues"]])

    def test_year_is_not_arbitrarily_rewritten(self):
        self.assertIn({"code": "INVALID_CAMPAIGN_CONTEXT", "field": "campaign_year"},
                      evaluate(example(), 2387)["issues"])

    def test_hash_canonical_and_not_a_credential(self):
        a = example()
        b = dict(reversed(list(a.items())))
        original_hash = evaluate(a)["draft_sha256"]
        self.assertEqual(original_hash, evaluate(b)["draft_sha256"])
        b["display_name"] = "Otro nombre"
        self.assertNotEqual(original_hash, evaluate(b)["draft_sha256"])
        self.assertIsNone(evaluate(a)["validated_creation_ref"])

    def test_non_json_or_huge_input_fails_closed(self):
        draft = example()
        draft["appearance_profile"] = object()
        self.assertEqual(evaluate(draft)["status"], "CHANGES_REQUIRED")
        draft["appearance_profile"] = "x" * 66000
        self.assertEqual(evaluate(draft)["status"], "CHANGES_REQUIRED")

    def test_deeply_nested_draft_fails_closed(self):
        draft = example()
        nested = {}
        top = nested
        for i in range(30):
            nxt = {}
            top["inside"] = nxt
            top = nxt
        draft["prior_experience"] = [nested]
        out = evaluate(draft)
        self.assertEqual(out["status"], "CHANGES_REQUIRED")
        self.assertIn("MALFORMED_FIELD", [x["code"] for x in out["issues"]])
        self.assertFalse(out["person_created"])

    def test_citizenship_is_not_inferred_from_human_species(self):
        draft = example()
        draft["citizenship_context"] = "por acreditar"
        self.assertEqual(evaluate(draft)["status"], "REVIEW_REQUIRED")

    def test_precheck_never_succeeds_as_authority(self):
        for candidate in (example(), {}, [], {"trusted_origin": "CORE_HOST_VERIFIED"}):
            out = evaluate(candidate)
            self.assertIn(out["status"], ("CHANGES_REQUIRED", "REVIEW_REQUIRED"))
            self.assertFalse(out["person_created"])
            self.assertIsNone(out["validated_creation_ref"])


if __name__ == "__main__":
    unittest.main()
