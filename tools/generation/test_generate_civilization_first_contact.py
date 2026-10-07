#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "generate_civilization_first_contact.py"
spec = importlib.util.spec_from_file_location("civgen", MODULE_PATH)
civgen = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = civgen
spec.loader.exec_module(civgen)


class CivilizationFirstContactTests(unittest.TestCase):
    def build(self, **overrides):
        args = dict(
            campaign_seed="civ_test_001",
            world_id="gen:planet:test_world",
            civilization_slot=0,
            era_id="tng_ds9_voyager",
            campaign_date="2372-01-01",
            environment_class="temperate",
            population_band="medium",
            technology_band="warp_threshold",
            warp_state="prototype_space_test",
            political_representation_state="single_planetary_authority",
            prior_alien_exposure=False,
            public_alien_awareness=False,
            active_internal_conflict=False,
            mutual_contact=False,
            language_samples=2,
            materialization_level="materialized",
        )
        args.update(overrides)
        return civgen.generate(**args)

    def test_deterministic(self):
        self.assertEqual(self.build(), self.build())

    def test_latent_and_materialized_share_civilization_identity(self):
        a = self.build(materialization_level="latent")
        b = self.build(materialization_level="materialized")
        self.assertEqual(a["world_truth"]["civilization_id"], b["world_truth"]["civilization_id"])

    def test_prewarp_no_exposure_is_observe_only(self):
        p = self.build(
            technology_band="advanced_prewarp",
            warp_state="active_research",
            materialization_level="observed",
        )
        self.assertEqual(p["first_contact"]["contact_eligibility"], "not_eligible_normal_contact")
        self.assertEqual(p["first_contact"]["prime_directive_state"], "strict_non_interference")

    def test_first_warp_is_candidate_not_auto_contact(self):
        p = self.build(
            technology_band="early_warp",
            warp_state="first_successful_warp_flight",
            materialization_level="first_contact_preparation",
            language_samples=5,
        )
        self.assertEqual(p["first_contact"]["contact_eligibility"], "formal_contact_candidate")
        self.assertTrue(p["first_contact"]["automatic_contact_forbidden"])
        self.assertEqual(civgen.validate(p), [])

    def test_divided_world_has_partial_representatives(self):
        p = self.build(
            technology_band="early_warp",
            warp_state="repeatable_warp_capability",
            political_representation_state="multiple_sovereign_states",
            materialization_level="first_contact_preparation",
            language_samples=4,
        )
        self.assertEqual(p["first_contact"]["recommended_contact_scope"], "polity_or_representative_limited")
        self.assertTrue(all(x["representation_scope"] == "partial_polity" for x in p["first_contact_preparation"]["representative_candidates"]))
        self.assertEqual(civgen.validate(p), [])

    def test_translation_improves_with_samples(self):
        a = self.build(language_samples=0)
        b = self.build(language_samples=5)
        self.assertEqual(a["observer_knowledge"]["translation_state"], "untranslated")
        self.assertEqual(b["observer_knowledge"]["translation_state"], "universal_translator_confident")

    def test_species_never_locks_personality(self):
        p = self.build()
        self.assertTrue(all(x["personality_lock"] is None for x in p["materialized_civilization"]["species"]))


    def test_locked_first_warp_fixture(self):
        p = civgen.generate(
            campaign_seed="first_contact_fixture_001",
            world_id="gen:planet:elyra_4",
            civilization_slot=0,
            era_id="tng_ds9_voyager",
            campaign_date="2372-06-18",
            environment_class="temperate",
            population_band="large",
            technology_band="early_warp",
            warp_state="first_successful_warp_flight",
            political_representation_state="single_planetary_authority",
            prior_alien_exposure=False,
            public_alien_awareness=False,
            active_internal_conflict=False,
            mutual_contact=False,
            language_samples=5,
            materialization_level="first_contact_preparation",
        )
        self.assertEqual(p["world_truth"]["civilization_id"], "gen:civilization:03fd61e37036005f")
        self.assertEqual(p["world_truth"]["population_estimate"], 3894320550)
        mat = p["materialized_civilization"]
        self.assertEqual(mat["civilization_self_name"], "Raerraith")
        self.assertEqual(mat["primary_language"]["planet_self_name"], "Thesqolqu")
        self.assertEqual(mat["species"][0]["morphology_family"], "nonhuman_bilateral")
        self.assertEqual(mat["species"][0]["surface_cover"], "fine_fur")
        self.assertEqual(mat["governments"][0]["government_type"], "unitary_republic")
        self.assertEqual(mat["governments"][0]["display_self_name"], "Mesikfis")
        rep = p["first_contact_preparation"]["representative_candidates"][0]
        self.assertEqual(rep["name"], "Bathsatim Sailairdak")
        self.assertEqual(rep["office"], "senior_civic_representative")
        self.assertEqual(p["first_contact"]["contact_eligibility"], "formal_contact_candidate")
        self.assertTrue(p["first_contact"]["automatic_contact_forbidden"])
        self.assertEqual(civgen.validate(p), [])


if __name__ == "__main__":
    unittest.main()
