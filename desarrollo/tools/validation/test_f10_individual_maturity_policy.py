#!/usr/bin/env python3
"""H06-P06-A7: política y referencias seguras, sin autoridad real."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from f10_individual_maturity_reference import evaluate_reference

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "sistemas/gameplay/character_creation/f10_individual_maturity_policy_v0.1.json"
S = ROOT / "sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json"
BIO = ROOT / "sistemas/gameplay/character_creation/f10_initial_background_policy_v0.1.json"
LIFE = ROOT / "sistemas/gameplay/species/character_lifecycle_contract.json"
HEADER = ROOT / "desarrollo/integration/host/src/f10/biography_evidence.h"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def draft(species_id="human", age_or_birth_date=20, **extra):
    return {"species_id": species_id, "age_or_birth_date": age_or_birth_date,
            "adult_equivalent_status": True, **extra}


class F10IndividualMaturityPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load(P)
        cls.species = load(S)
        cls.biology = load(LIFE)

    def result(self, value):
        r = evaluate_reference(value, policy=self.policy, species_policy=self.species)
        self.assertFalse(r["individual_maturity_attested"])
        for flag in ("objective_valid", "semantic_review_executed", "person_created",
                     "cadet_admitted", "rank_issued"):
            self.assertFalse(r[flag])
        self.assertIn(r["outcome"], ("CHANGES_REQUIRED", "REVIEW_REQUIRED"))
        return r

    def test_design_only(self):
        self.assertEqual(self.policy["status"], "PROPOSED_DESIGN_NOT_RUNTIME_ENFORCED")
        self.assertEqual(self.policy["tests_scope"], "OFFLINE_REFERENCE_AND_CONTRACT_ONLY_NOT_REAL_MATURITY_ATTESTATION")

    def test_all_policy_refs_exist(self):
        for path in self.policy["source_refs"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_25_registered_species_still_separate(self):
        rows = self.species["species"]
        self.assertEqual(len(rows), 25)
        self.assertEqual(sum(s["minimum_playable_age_earth_years"] is not None for s in rows), 22)
        self.assertEqual(sum(s["minimum_playable_age_earth_years"] is None for s in rows), 3)
        self.assertEqual(sum(s["content_scope"] == "DLC_DELTA" for s in rows), 5)
        for row in rows:
            self.assertTrue((ROOT / row["profile_ref"]).is_file())

    def test_no_fabricated_stage_rule(self):
        reg = self.policy["stage_rule_registry"]
        self.assertEqual(reg["entries"], [])
        self.assertEqual(reg["empty_registry_behavior"], "REVIEW_REQUIRED_NO_PERSON")
        self.assertIn("NO_AGE_ONLY_PREDICATE", reg["registration_requirements"])
        self.assertIn("AUTHOR_APPROVAL_OR_EXPLICIT_PREEXISTING_DOMAIN_AUTHORITY", reg["registration_requirements"])

    def test_true_adulthood_client_flag_not_evidence(self):
        r = self.result(draft())
        self.assertEqual(r["outcome"], "REVIEW_REQUIRED")
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", r["issue_codes"])

    def test_human_17_must_correct(self):
        r = self.result(draft(age_or_birth_date=17))
        self.assertEqual(r["outcome"], "CHANGES_REQUIRED")
        self.assertIn("BELOW_PLAYABLE_AGE", r["issue_codes"])

    def test_human_18_still_waits_for_stage(self):
        r = self.result(draft(age_or_birth_date=18))
        self.assertEqual(r["outcome"], "REVIEW_REQUIRED")
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", r["issue_codes"])

    def test_human_45_no_age_only_shortcut(self):
        r = self.result(draft(age_or_birth_date=45))
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", r["issue_codes"])

    def test_vulcan_24_and_25(self):
        self.assertIn("BELOW_PLAYABLE_AGE", self.result(draft("vulcan", 24))["issue_codes"])
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", self.result(draft("vulcan", 25))["issue_codes"])

    def test_andorian_20(self):
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", self.result(draft("andorian", 20))["issue_codes"])

    def test_ocampan_two_is_not_main_game(self):
        r = self.result(draft("ocampan", 2))
        self.assertEqual(r["outcome"], "CHANGES_REQUIRED")
        self.assertIn("DLC_DELTA_UNAVAILABLE", r["issue_codes"])

    def test_three_special_species_never_inferred(self):
        for sid in ("changeling", "jem_hadar", "vorta"):
            with self.subTest(species=sid):
                r = self.result(draft(sid, 100))
                self.assertEqual(r["outcome"], "REVIEW_REQUIRED")
                self.assertIn("SPECIAL_MATURITY_RULE_REQUIRED", r["issue_codes"])

    def test_all_five_delta_rejected(self):
        for sid in self.policy["exceptions"]["five_delta_species"]:
            with self.subTest(species=sid):
                self.assertIn("DLC_DELTA_UNAVAILABLE", self.result(draft(sid, 100))["issue_codes"])

    def test_human_2365_birthyear_is_undecided_even_first_january(self):
        for stamp in ("2365-01-01","2365-06-15","2365-12-31"):
            r = self.result(draft(age_or_birth_date=stamp))
            self.assertIn("PLAYABLE_AGE_UNDECIDED", r["issue_codes"])

    def test_2364_birthdate_passes_only_floor(self):
        r = self.result(draft(age_or_birth_date="2364-12-31"))
        self.assertNotIn("PLAYABLE_AGE_UNDECIDED", r["issue_codes"])
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", r["issue_codes"])

    def test_2366_birthdate_is_under_floor(self):
        r = self.result(draft(age_or_birth_date="2366-01-01"))
        self.assertIn("BELOW_PLAYABLE_AGE", r["issue_codes"])

    def test_false_adulthood_flag_rejects(self):
        r = self.result(draft(adult_equivalent_status=False))
        self.assertIn("NON_ADULT_DECLARED", r["issue_codes"])
        self.assertEqual(r["outcome"], "CHANGES_REQUIRED")

    def test_absent_or_invalid_stage_flag_rejects(self):
        d = draft()
        d.pop("adult_equivalent_status")
        self.assertIn("MALFORMED_ADULT_STATUS", self.result(d)["issue_codes"])
        self.assertIn("MALFORMED_ADULT_STATUS", self.result(draft(adult_equivalent_status="true"))["issue_codes"])

    def test_no_real_medical_paperwork_needed(self):
        self.assertTrue(self.policy["individual_stage_claim"]["no_real_world_documents_or_medical_files_required"])
        self.assertTrue(self.policy["individual_stage_claim"]["no_existing_core_person_required"])

    def test_appearance_uniform_and_rite_not_proof(self):
        r = self.result(draft(appearance_profile={"looks_adult":True}, cultural_rite="ascension"))
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", r["issue_codes"])
        self.assertIn("APPEARANCE_ADULT", self.policy["individual_stage_claim"]["stage_sources_never_sufficient"])
        self.assertTrue(self.policy["exceptions"]["no_cultural_rite_as_universal_maturity"])

    def test_client_can_not_inject_internal_attestation(self):
        for field in ("adult_stage_attested","maturity_evidence_approved","stage_rule_id","person_id"):
            with self.subTest(field=field):
                r = self.result(draft(**{field:"approved"}))
                self.assertEqual(r["outcome"], "CHANGES_REQUIRED")
                self.assertIn("FORBIDDEN_AUTHORITY_FIELD", r["issue_codes"])

    def test_nested_injection_rejected(self):
        r = self.result(draft(family_context={"nested":[{"source_identity":"fake"}]}))
        self.assertIn("FORBIDDEN_AUTHORITY_FIELD", r["issue_codes"])

    def test_unknown_species_no_human_fallback(self):
        r = self.result(draft("unknown_species", 90))
        self.assertIn("UNKNOWN_SPECIES", r["issue_codes"])

    def test_no_age_maximum_invented(self):
        r = self.result(draft(age_or_birth_date=200))
        self.assertNotIn("BELOW_PLAYABLE_AGE", r["issue_codes"])
        self.assertEqual(r["outcome"], "REVIEW_REQUIRED")
        self.assertTrue(self.policy["exceptions"]["no_fixed_maximum_playable_age"])

    def test_invalid_birth_date_rejected(self):
        r = self.result(draft(age_or_birth_date="2365-02-30"))
        self.assertIn("MALFORMED_BIRTH_DATE", r["issue_codes"])

    def test_unsupported_age_shape_rejected(self):
        for value in (True, -1, "adult", None):
            with self.subTest(value=value):
                r=self.result(draft(age_or_birth_date=value))
                self.assertIn("MALFORMED_AGE_OR_BIRTH_DATE",r["issue_codes"])

    def test_existing_native_evidence_type_only_not_connected(self):
        h=HEADER.read_text(encoding="utf-8")
        self.assertIn("RegisteredBiographyAuthority",h)
        self.assertIn("VALIDATED_INITIAL_BACKGROUND",h)
        self.assertIn("MATURITY_EVIDENCE_REQUIRED", (ROOT/"desarrollo/integration/host/src/f10/biography_validation.h").read_text(encoding="utf-8"))

    def test_other_gate_still_required(self):
        self.assertEqual(self.policy["canonical_outcomes"]["valid_stage_source_but_no_semantic_reviewer"], "REVIEW_UNAVAILABLE_NO_PERSON")
        self.assertTrue(self.policy["review_security"]["mandatory_double_gate"])
        self.assertTrue(self.policy["review_security"]["no_core_rpg_or_unreal_mutation"])

    def test_lifecycle_not_age_human_fallback(self):
        self.assertTrue(load(ROOT/"sistemas/gameplay/species/species_biology_contract.json")[
            "development_and_aging"]["chronological_age_must_not_be_interpreted_using_human_stage_thresholds_without_profile_support"])
        self.assertIn("Stage thresholds come from species/entity profiles, not a universal human age table.",
                      self.biology["rules"])

    def test_empty_rule_registry_never_approves_through_reference(self):
        for x in self.species["species"]:
            sid=x["species_id"]
            age=x["minimum_playable_age_earth_years"]
            if age is None: age=99
            r=self.result(draft(sid, age))
            self.assertFalse(r["individual_maturity_attested"])

    def test_remaining_h06_gate_not_certified(self):
        self.assertEqual(self.policy["phase_completion_status"]["h06_p06_a"], "PARTIAL")
        self.assertEqual(self.policy["phase_completion_status"]["m1"], "PARTIAL")
        self.assertEqual(self.policy["phase_completion_status"]["h07"], "NOT_STARTED")


if __name__ == "__main__":
    unittest.main()
