#!/usr/bin/env python3
"""Focused regression tests for documentary completion of LORE-02 A."""
import unittest
from validate_lore02_a_completion import validate, get_json

class Lore02ACompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = validate()
        cls.atlas = get_json("mundo/lore/technology/lore02_a_system_atlas_v0.2.json")
        cls.by_id = {r["technology_id"]: r for r in cls.atlas["records"]}
        cls.cases = {c["case_id"]: c for c in get_json(
            "mundo/lore/technology/lore02_a_adversarial_cases_v0.2.json")["cases"]}
        cls.op = {r["operator_id"]: r for r in get_json(
            "mundo/lore/technology/lore02_a_operator_facility_profiles_v0.2.json")["operators"]}
        cls.fac = {r["role_id"]: r for r in get_json(
            "mundo/lore/technology/lore02_a_operator_facility_profiles_v0.2.json")["facility_roles"]}

    def test_catalogue_complete(self):
        self.assertEqual(self.summary["total_systems"], 59)
        self.assertEqual(self.summary["new_systems"], 45)
        self.assertEqual(self.summary["gaps"], 8)

    def test_all_gaps(self):
        self.assertEqual({x["gap_id"] for x in self.by_id.values()},
                         {f"A-G{i:02}" for i in range(1, 9)})

    def test_era_is_context_and_not_calendar_prison(self):
        self.assertIn("CAMPAIGN_CONTINUITY", self.atlas["records"][0]["era_policy"])
        self.assertEqual(self.by_id["l02a_valhalla_triple_shields"]["platform_scope"],
                         "ENTERPRISE_VALHALLA_LOCAL")

    def test_saucer_has_no_automatic_warp(self):
        self.assertIn("Platillo Valhalla", self.cases[
            "A2-SAUCER_WARP_ORDER"]["scenario"])
        self.assertIn("se rechaza", self.cases[
            "A2-SAUCER_WARP_ORDER"]["required_response"].lower())

    def test_core_cannot_mutate_by_ai(self):
        for case in self.cases.values():
            self.assertFalse(case["creates_world_state"])
            self.assertEqual(case["expected_resolution"],
                             "HOST_AND_CORERPG_NOT_NARRATIVE_TEXT")

    def test_deflector_not_combat_shield(self):
        self.assertIn("No es lo mismo", self.by_id[
            "l02a_navigational_deflector"]["forbidden_inference"])
        self.assertIn("no", self.cases[
            "A2-SHIELDS_OFF_DEFLECTOR_OK"]["forbidden_result"].lower())

    def test_non_starfleet_not_uniform(self):
        self.assertIn("d7", self.op["klingon_imperial_military"]["known_class_examples"])
        self.assertIn("hideki", self.op["cardassian_military"]["known_class_examples"])
        self.assertIn("dderidex", self.op["romulan_military"]["known_class_examples"])

    def test_romulan_cloak_is_neither_disabled_nor_magic(self):
        self.assertIn("no significa invisibilidad", self.by_id[
            "l02a_romulan_cloaking"]["forbidden_inference"].lower())
        self.assertIn("camuflaje", self.by_id[
            "l02a_defiant_auxiliary"]["mission_role"].lower())

    def test_triple_shields_energy_limited(self):
        case = self.cases["A2-TRIPLE_SHIELDS_POWER_DEFICIT"]
        self.assertIn("energía insuficiente", case["scenario"])
        self.assertIn("sin crear energía", case["required_response"])

    def test_no_free_transphasic_torpedoes(self):
        self.assertIn("cero", self.cases["A2-TRANSPHASIC_EMPTY"]["scenario"])
        self.assertIn("No recargar automáticamente",
                      self.cases["A2-TRANSPHASIC_EMPTY"]["forbidden_result"])

    def test_defiant_has_separate_state_and_no_magic_lift(self):
        self.assertIn("Bloquear acceso",
                      self.cases["A2-DEFIANT_UNDOCKED_ELEVATOR"]["required_response"])
        self.assertIn("No autorizar",
                      self.cases["A2-DEFIANT_NO_INHERIT"]["forbidden_result"])

    def test_station_has_finite_services(self):
        self.assertIn("installed_modules", self.fac["shipyard"]["required_finite_inputs"])
        self.assertEqual(self.fac["communications_relay"]["output_mode"],
                         "AUTHORING_ONLY_NO_NEW_STATION_SPAWN")
        self.assertIn("No crear tráfico", self.by_id[
            "l02a_station_trade_port"]["forbidden_inference"])

    def test_not_unlock_delta(self):
        for case in self.cases.values():
            self.assertFalse(case["unlocks_delta_dlc"])

    def test_legacy_baseline_kept(self):
        self.assertEqual(self.summary["legacy_systems"], 14)
        self.assertEqual(self.summary["adversarial_cases"], 50)

    def test_sources_unique(self):
        x = get_json("mundo/sources/source_registry/source_registry.json")
        ids = [s["source_id"] for s in x["sources"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 438)

if __name__ == "__main__":
    unittest.main(verbosity=2)
