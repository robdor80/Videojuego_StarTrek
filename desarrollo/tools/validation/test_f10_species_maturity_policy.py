#!/usr/bin/env python3
"""F10 H06-P06-A: verifica el contrato de madurez APROBADO, no la validación nativa."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = ROOT / "sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json"
PROFILES = ROOT / "sistemas/gameplay/species/profiles"
EXPECTED_MINIMUMS = {
    "aenar": 20,
    "andorian": 20,
    "bajoran": 18,
    "benzite": 18,
    "betazoid": 18,
    "bolian": 18,
    "breen": 20,
    "cardassian": 18,
    "el_aurian": 18,
    "ferengi": 18,
    "hirogen": 20,
    "human": 18,
    "kazon": 18,
    "klingon": 18,
    "ocampan": 2,
    "pakled": 18,
    "romulan": 25,
    "talaxian": 18,
    "tellarite": 18,
    "trill": 18,
    "vidiian": 18,
    "vulcan": 25
}
EXPECTED_SPECIALS = set(["changeling","jem_hadar","vorta"])
EXPECTED_DLC = set(["hirogen","kazon","ocampan","talaxian","vidiian"])
EXPECTED_SPECIES_COUNT = 25


class F10SpeciesMaturityPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        cls.species = cls.policy["species"]
        cls.by_id = {s["species_id"]: s for s in cls.species}

    def test_all_registered_species_and_only_species(self):
        registered = set()
        for path in PROFILES.glob("*_v0.1.json"):
            profile = json.loads(path.read_text(encoding="utf-8"))
            if "species_id" in profile:
                registered.add(profile["species_id"])
            else:
                self.assertEqual(profile.get("profile_type"), "transformative_character_state_not_species")
        self.assertEqual(len(registered), EXPECTED_SPECIES_COUNT)
        self.assertEqual(set(self.by_id), registered)
        self.assertEqual(len(self.species), len(registered))
        self.assertNotIn("borg_assimilated_character", self.by_id)

    def test_author_approved_age_floor_no_implicit_human_fallback(self):
        self.assertEqual(
            {s["species_id"]: s["minimum_playable_age_earth_years"]
             for s in self.species if s["age_rule_type"] == "NUMERIC_PLAYABLE_FLOOR"},
            EXPECTED_MINIMUMS,
        )
        self.assertEqual(
            {s["species_id"] for s in self.species if s["age_rule_type"] == "SPECIAL_REVIEW_REQUIRED"},
            EXPECTED_SPECIALS,
        )

    def test_specials_have_no_auto_eligibility(self):
        for species_id in EXPECTED_SPECIALS:
            row = self.by_id[species_id]
            self.assertIsNone(row["minimum_playable_age_earth_years"])
            self.assertTrue(row["special_blocker"])
            self.assertFalse(row["automatic_player_eligibility"])
            self.assertFalse(row["maturity_evidence_required"])

    def test_no_maximum_and_no_auto_approval_for_any_species(self):
        for row in self.species:
            self.assertIsNone(row["maximum_playable_age_earth_years"], row["species_id"])
            self.assertFalse(row["automatic_player_eligibility"], row["species_id"])
            self.assertFalse(row["maturity_evidence_required"], row["species_id"])
        rules = self.policy["rules"]
        self.assertTrue(rules["player_declared_age_is_accepted_as_fictional_character_fact"])
        self.assertTrue(rules["age_minimum_is_sufficient_to_pass_age_check"])
        self.assertTrue(rules["no_additional_individual_maturity_evidence_required"])
        self.assertTrue(rules["no_auto_admission_or_cadet_slot"])
        self.assertTrue(rules["no_runtime_authority_or_core_mutation_in_this_policy"])

    def test_delta_dlc_is_never_unlocked_by_maturity(self):
        self.assertEqual(
            {s["species_id"] for s in self.species if s["content_scope"] == "DLC_DELTA"},
            EXPECTED_DLC,
        )
        self.assertEqual(self.policy["content_gates"]["DLC_DELTA"], "NOT_AVAILABLE_IN_MAIN_GAME_DLC_NOT_IMPLEMENTED")
        for row in self.species:
            self.assertIn(row["content_scope"], ("MAIN_GAME", "DLC_DELTA"))

    def test_source_profile_refs_match_existing_identifiers(self):
        for row in self.species:
            expected = f"sistemas/gameplay/species/profiles/{row['species_id']}_v0.1.json"
            self.assertEqual(row["profile_ref"], expected)
            self.assertEqual(json.loads((ROOT / expected).read_text(encoding="utf-8"))["species_id"],
                             row["species_id"])

    def test_campaign_year_only_boundary_and_separate_academy(self):
        scope = self.policy["scope"]
        self.assertEqual(scope["campaign_start_year"], 2383)
        self.assertEqual(scope["campaign_start_month_day"], "UNDECIDED_BY_AUTHOR")
        self.assertEqual(scope["age_unit"], "EARTH_YEARS")
        rules = self.policy["rules"]
        self.assertEqual(rules["date_threshold_ambiguous_without_campaign_month_day"], "REVIEW_REQUIRED")
        self.assertEqual(rules["under_age_with_provable_context"], "CHANGES_REQUIRED")
        self.assertEqual(rules["at_or_above_minimum"], "AGE_CHECK_PASSED_OTHER_F10_GATES_INDEPENDENT")
        self.assertTrue(rules["npc_age_policy_independent_of_player_minimum"])
        self.assertTrue(self.by_id["human"]["minimum_playable_age_earth_years"] == 18)
        self.assertTrue(self.by_id["ocampan"]["minimum_playable_age_earth_years"] == 2)

    def test_status_is_not_a_runtime_authority(self):
        self.assertEqual(self.policy["status"], "AUTHOR_APPROVED_PLAYER_DECLARED_AGE_GATE")
        self.assertEqual(self.policy["schema_version"], "0.1.1")
        self.assertTrue(self.policy["integration"]["semantic_ai_review_still_mandatory"])
        self.assertTrue(self.policy["integration"]["no_auto_adoption_by_core_unreal_or_h03_h04"])
        self.assertNotIn("validated_creation_ref", self.policy)


if __name__ == "__main__":
    unittest.main()
