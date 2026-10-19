#!/usr/bin/env python3
"""Regresiones y casos adversariales de LORE-02 A."""
import unittest
from validate_lore02_a import validate, load

class Lore02ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = validate()
        cls.cat = load("lore/technology/ship_station_catalogue_v0.1.json")
        cls.by_id = {r["technology_id"]: r for r in cls.cat["records"]}
        cls.cases = {v["case_id"]: v for v in load(
            "lore/technology/ship_station_cases_v0.1.json")["cases"]}
        cls.matrix = {p["id"]:p["capabilities"] for p in load(
            "gameplay/ship_operations/era_technology_matrix.json")["profiles"]}

    def test_dimensions_present(self):
        self.assertEqual(self.summary["technology_records"], 14)
        self.assertEqual(self.summary["negative_scenarios"], 14)
        self.assertEqual(self.summary["research_gaps"], 8)

    def test_quantum_late_not_standard_everywhere(self):
        self.assertEqual(self.matrix["tng_2364_2370"]["quantum_torpedoes"], "unavailable")
        self.assertEqual(self.matrix["late_24c_2371_2378"]["quantum_torpedoes"], "available")
        self.assertIn("no demuestra", self.cases["A-CASE-04"]["expected_documentary_reasoning"])

    def test_bioneural_class_specific(self):
        self.assertEqual(self.by_id["starfleet_bio_neural_computing"]["availability"], "class_specific")
        self.assertIn("no", self.cases["A-CASE-05"]["forbidden_conclusion"].lower())

    def test_pike_holo_does_not_become_standard(self):
        self.assertEqual(self.matrix["pike_2259_2264"]["ship_holodeck"], "not_standard")
        self.assertEqual(self.matrix["pike_2259_2264"]["holographic_environment_simulation"],
                         "experimental")
        self.assertIn("no estándar", self.cases["A-CASE-01"]["expected_documentary_reasoning"])

    def test_food_synth_not_full_replicator(self):
        self.assertEqual(self.matrix["kirk_tos_2265_2269"]["food_synthesizer"], "standard")
        self.assertEqual(self.matrix["kirk_tos_2265_2269"]["full_replicator"], "not_standard")
        self.assertEqual(self.by_id["starfleet_food_synthesizer"]["availability_profile_id"],
                         "kirk_films_2278_2293")

    def test_observations_not_omniscient(self):
        self.assertIn("omnisciente", self.by_id["starfleet_ship_sensors"]["prohibited_inference"])
        self.assertIn("observaciones posibles", self.cases["A-CASE-06"]["expected_documentary_reasoning"])

    def test_transporter_does_not_duplicate(self):
        self.assertIn("duplicación", self.by_id["starfleet_personnel_transporter"]["prohibited_inference"])
        self.assertFalse(self.cases["A-CASE-13"]["ai_direct_world_mutation"])

    def test_privacy_still_limited(self):
        self.assertIn("secretos", self.by_id["starfleet_isolinear_computing"]["prohibited_inference"])
        self.assertIn("expediente", self.cases["A-CASE-11"]["expected_documentary_reasoning"])

    def test_missing_matrix_key_not_equivalent_unavailable(self):
        self.assertNotIn("site_to_site_transport", self.matrix["kirk_films_2278_2293"])
        self.assertIn("ausencia de clave", self.cases["A-CASE-08"]["expected_documentary_reasoning"])
        self.assertEqual(self.by_id["starfleet_site_to_site_transport"]["temporal_validity"]
                         ["unmapped_eras_mean"], "NOT_RESEARCHED_NOT_UNAVAILABLE")

    def test_all_cases_require_authority(self):
        for case in self.cases.values():
            self.assertIn("authenticated_actor_and_authority", case["required_context"])
            self.assertFalse(case["ai_direct_world_mutation"])
            self.assertFalse(case["delta_dlc_unlock"])

    def test_delta_portal_reserved(self):
        self.assertIn("IDEA-0011", self.cases["A-CASE-14"]["expected_documentary_reasoning"])
        self.assertFalse(self.cat["delta_dlc_enabled"])

    def test_no_false_numeric_performance(self):
        for item in self.cat["records"]:
            self.assertIn("No se proporcionan cifras", item["operational_constraints"][1])

if __name__ == "__main__":
    unittest.main(verbosity=2)
