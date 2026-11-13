#!/usr/bin/env python3
"""Regresiones adversariales LORE-05F (no son pruebas de gameplay)."""
import copy
import unittest
from validate_lore05_f import load_all, problems_for_data, validate, CHARACTERS


class TestLore05F(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = load_all()

    def mutation(self, fn):
        data = copy.deepcopy(self.reference)
        fn(data)
        self.assertTrue(problems_for_data(data), "La contradicción no fue detectada")

    def test_reference_passes(self):
        self.assertEqual(problems_for_data(self.reference), [])

    def test_repository_passes(self):
        self.assertEqual(validate(), [])

    def test_enterprise_cannot_change_class(self):
        self.mutation(lambda d: d["valhalla"]["subject"].update(class_id="valhalla"))

    def test_enterprise_cannot_change_registry(self):
        self.mutation(lambda d: d["valhalla"]["subject"].update(registry="NCC-1701-V"))

    def test_enterprise_cannot_be_guaranteed_in_2387(self):
        self.mutation(lambda d: d["valhalla"]["future"].update(readiness_2387_guaranteed=True))

    def test_enterprise_cannot_assign_player_automatically(self):
        self.mutation(lambda d: d["valhalla"]["academy"].update(player_assignment_automatic=True))

    def test_experimental_technology_not_assumed_installed(self):
        self.mutation(lambda d: d["valhalla"]["quantum_slipstream"].update(installed_on_enterprise_d_by_default=True))

    def test_wrong_start_year(self):
        self.mutation(lambda d: d["locations"].update(campaign_baseline_year=2401))

    def test_duplicate_location(self):
        self.mutation(lambda d: d["locations"]["locations"][1].update(id="earth"))

    def test_historical_colony_not_navigable(self):
        self.mutation(lambda d: next(x for x in d["locations"]["locations"] if x["id"] == "new_bajor").update(automatic_travel_enabled=True))

    def test_no_made_up_anchor(self):
        self.mutation(lambda d: d["locations"]["locations"][0].update(anchor_location_id="unknown_star_system"))

    def test_c_d_facility_reference(self):
        self.mutation(lambda d: next(x for x in d["locations"]["locations"] if x["id"] == "deep_space_9").update(facility_id="canon:facility:invented"))

    def test_defiant_original_stays_destroyed(self):
        self.mutation(lambda d: next(x for x in d["entities"]["ships"] if x["ship_id"] == "uss_defiant_nx_74205").update(documentary_state_2383="ACTIVE"))

    def test_no_identity_duplicate_ships(self):
        self.mutation(lambda d: d["entities"]["ships"][1].update(ship_id=d["entities"]["ships"][0]["ship_id"]))

    def test_ship_not_automatically_spawned(self):
        self.mutation(lambda d: d["entities"]["ships"][0].update(auto_spawn=True))

    def test_facility_not_copied(self):
        self.mutation(lambda d: d["entities"]["facilities"][0].update(auto_generate_duplicate=True))

    def test_civil_federation_not_starfleet(self):
        self.mutation(lambda d: d["entities"]["institution_profiles"][0].update(institution_id="starfleet"))

    def test_no_new_faction(self):
        self.mutation(lambda d: d["entities"]["factions"][0].update(faction_id="invented_polity"))

    def test_no_perfect_translator_state(self):
        self.mutation(lambda d: d["languages"]["translator_states"].append("magic_perfect"))

    def test_owner_communications_states(self):
        self.mutation(lambda d: d["languages"]["channel_states"].append("telepathy"))

    def test_delta_scope_remains_future(self):
        self.mutation(lambda d: next(x for x in d["languages"]["existing_languages"] if x["language_id"] == "kazon").update(availability_scope="MAIN_GAME"))

    def test_languages_not_auto_unlock(self):
        self.mutation(lambda d: d["languages"].update(automatic_dlc_unlock=True))

    def test_no_automatic_first_contact(self):
        self.mutation(lambda d: d["languages"].update(automatic_contact=True))

    def test_scenarios_not_runtime(self):
        self.mutation(lambda d: d["e_cases"].update(simulation_claimed=True))

    def test_case_never_writes_world(self):
        self.mutation(lambda d: d["d_cases"]["documentary_cases"][0].update(world_state_mutations=True))

    def test_roster_exact_twelve(self):
        self.mutation(lambda d: d["characters"].pop(CHARACTERS[-1]))

    def test_picard_ceremony_preserved(self):
        self.mutation(lambda d: d["characters"].update({CHARACTERS[0]: "# LORE-05B-01 — Picard GAME_ADDITION CoreRPG"}))

    def test_data_cannot_return_before_his_death(self):
        self.mutation(lambda d: d["characters"].update({CHARACTERS[6]: d["characters"][CHARACTERS[6]].replace("2390", "2380")}))

    def test_sisko_return_window_must_remain_explicit(self):
        self.mutation(lambda d: d["characters"].update({CHARACTERS[10]: d["characters"][CHARACTERS[10]].replace("2388", "2380")}))


if __name__ == "__main__":
    unittest.main()
